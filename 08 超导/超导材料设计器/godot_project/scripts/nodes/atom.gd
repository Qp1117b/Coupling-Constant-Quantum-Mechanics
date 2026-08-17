extends MeshInstance3D
class_name Atom3D

@export var element_symbol: String = "H"
@export var isotope_mass: int = 1

# === 以氢原子特征尺度为基准的物理化学尺度系统 ===
# 氢原子共价半径 (pm) — 基准单位, H ≡ 1.0
const H_COVALENT_RADIUS_PM: float = 31.0
# 基准视觉尺度 (Godot单位) — 氢原子在ball-stick模式下的球体半径
const ATOM_BASE_SCALE: float = 0.22
# Bondi 范德华半径 (pm) — 用于space-filling (CPK) 模式
const VDW_RADII_PM: Dictionary = {
	"H": 120, "He": 140, "Li": 182, "Be": 153, "B": 192, "C": 170, "N": 155, "O": 152, "F": 147, "Ne": 154,
	"Na": 227, "Mg": 173, "Al": 184, "Si": 210, "P": 180, "S": 180, "Cl": 175, "Ar": 188,
	"K": 275, "Ca": 231, "Sc": 215, "Ti": 211, "V": 205, "Cr": 205, "Mn": 205, "Fe": 204,
	"Co": 200, "Ni": 163, "Cu": 140, "Zn": 139, "Ga": 187, "Ge": 211, "As": 185, "Se": 190,
	"Br": 185, "Kr": 202, "Rb": 320, "Sr": 249, "Y": 220, "Zr": 218, "Nb": 208, "Mo": 209,
	"Tc": 209, "Ru": 205, "Rh": 205, "Pd": 163, "Ag": 172, "Cd": 158, "In": 193, "Sn": 217,
	"Sb": 206, "Te": 206, "I": 198, "Xe": 216, "Cs": 343, "Ba": 268, "La": 250, "Ce": 250,
	"Pr": 249, "Nd": 249, "Hf": 223, "Ta": 222, "W": 222, "Re": 219, "Os": 216, "Ir": 216,
	"Pt": 175, "Au": 166, "Hg": 155, "Tl": 196, "Pb": 202, "Bi": 207, "Po": 197, "At": 202,
	"Rn": 220, "U": 240, "Np": 221, "Pu": 243, "Am": 244, "Cm": 245, "Bk": 244, "Cf": 245,
}

var atomic_number: int = 1
var neutron_count: int = 0
var atom_radius: float = 0.22
var vdw_radius: float = 0.85
var element_color: Color = Color.WHITE
var neutron_defect: float = 0.0
var cartan_info: Dictionary = {}

var is_brush_material: bool = false
var brush_scale_level: int = 0
var is_boundary: bool = false

var _material: StandardMaterial3D
var _is_hovered: bool = false
var _is_selected: bool = false
var _is_secondary: bool = false

signal atom_clicked(atom)
signal atom_hovered(atom)

static func compute_atom_radius(symbol: String) -> float:
	var data = ElementDB.get_element(symbol)
	var covalent_r = float(data.get("covalent_radius_pm", H_COVALENT_RADIUS_PM))
	return ATOM_BASE_SCALE * (covalent_r / H_COVALENT_RADIUS_PM)

static func compute_vdw_radius(symbol: String) -> float:
	var vdw_r = VDW_RADII_PM.get(symbol, 0)
	if vdw_r == 0:
		var data = ElementDB.get_element(symbol)
		var covalent_r = float(data.get("covalent_radius_pm", H_COVALENT_RADIUS_PM))
		vdw_r = covalent_r * 1.4
	return ATOM_BASE_SCALE * (float(vdw_r) / H_COVALENT_RADIUS_PM)

func _ready():
	_load_element_data()
	_setup_mesh()
	_build_cartan()

func _load_element_data():
	var data = ElementDB.get_element(element_symbol)
	if data.is_empty():
		return
	atomic_number = int(data.get("atomic_number", 1))
	element_color = Color.from_string(data.get("color", "#FFFFFF"), Color.WHITE)
	var covalent_r = float(data.get("covalent_radius_pm", H_COVALENT_RADIUS_PM))
	atom_radius = ATOM_BASE_SCALE * (covalent_r / H_COVALENT_RADIUS_PM)
	var vdw_r = VDW_RADII_PM.get(element_symbol, 0)
	if vdw_r == 0:
		vdw_r = covalent_r * 1.4
	vdw_radius = ATOM_BASE_SCALE * (float(vdw_r) / H_COVALENT_RADIUS_PM)
	neutron_count = isotope_mass - atomic_number

func _setup_mesh():
	var sphere_mesh = SphereMesh.new()
	sphere_mesh.radius = atom_radius
	sphere_mesh.height = atom_radius * 2.0
	sphere_mesh.radial_segments = 32
	sphere_mesh.rings = 16
	self.mesh = sphere_mesh

	_material = StandardMaterial3D.new()
	_material.albedo_color = element_color
	_material.metallic = 0.2
	_material.roughness = 0.35
	_material.emission_enabled = true
	_material.emission = element_color * 0.15
	_material.emission_energy_multiplier = 1.0
	material_override = _material

	var collision = CollisionShape3D.new()
	var shape = SphereShape3D.new()
	shape.radius = atom_radius * 1.2
	collision.shape = shape
	add_child(collision)

func _build_cartan():
	neutron_defect = CQMCartanBuilder.neutron_defect(neutron_count, element_symbol)
	cartan_info = CQMCartanBuilder.element_cartan(atomic_number, neutron_count, element_symbol)

func _input_event(_camera: Camera3D, event: InputEvent,
                  _position: Vector3, _normal: Vector3, _shape_idx: int):
	if event is InputEventMouseButton and event.pressed:
		if event.button_index == MOUSE_BUTTON_LEFT:
			atom_clicked.emit(self)

func _mouse_enter():
	_is_hovered = true
	_update_material()
	atom_hovered.emit(self)

func _mouse_exit():
	_is_hovered = false
	_update_material()

func set_selected(sel: bool):
	_is_selected = sel
	_update_material()

func set_secondary(sel: bool):
	_is_secondary = sel
	_update_material()

func set_brush_material(val: bool, scale_level: int = 0):
	is_brush_material = val
	brush_scale_level = scale_level
	var sphere_mesh = self.mesh as SphereMesh
	if sphere_mesh:
		if is_brush_material or is_boundary:
			sphere_mesh.radius = atom_radius * 0.3
			sphere_mesh.height = atom_radius * 0.6
		else:
			sphere_mesh.radius = atom_radius
			sphere_mesh.height = atom_radius * 2.0
	_update_material()

func set_boundary(val: bool):
	is_boundary = val
	var sphere_mesh = self.mesh as SphereMesh
	if sphere_mesh:
		if is_boundary or is_brush_material:
			sphere_mesh.radius = atom_radius * 0.3
			sphere_mesh.height = atom_radius * 0.6
		else:
			sphere_mesh.radius = atom_radius
			sphere_mesh.height = atom_radius * 2.0
	_update_material()

func _update_material():
	if _is_secondary:
		_material.emission = Color(1.0, 0.55, 0.0)
		_material.emission_energy_multiplier = 3.0
	elif _is_selected:
		_material.emission = Color.CYAN
		_material.emission_energy_multiplier = 2.0
	elif _is_hovered:
		_material.emission = element_color * 0.4
		_material.emission_energy_multiplier = 2.0
	elif is_boundary:
		_material.emission = Color(0.3, 0.5, 1.0)
		_material.emission_energy_multiplier = 1.2
	elif is_brush_material:
		_material.emission = Color(0.2, 0.8, 0.3)
		_material.emission_energy_multiplier = 0.8
	else:
		_material.emission = element_color * 0.15
		_material.emission_energy_multiplier = 1.0

func get_info_text() -> String:
	return "%s (Z=%d, A=%d, N=%d, ε=%.6f)" % [
		element_symbol, atomic_number, isotope_mass, neutron_count, neutron_defect
	]

func set_render_mode(mode: String):
	match mode:
		"ball_stick":
			var m = SphereMesh.new()
			m.radius = atom_radius
			m.height = atom_radius * 2.0
			m.radial_segments = 32
			m.rings = 16
			self.mesh = m
		"space_filling":
			var m2 = SphereMesh.new()
			m2.radius = vdw_radius
			m2.height = vdw_radius * 2.0
			m2.radial_segments = 32
			m2.rings = 16
			self.mesh = m2
		"wireframe":
			_material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
			return
	_material.shading_mode = BaseMaterial3D.SHADING_MODE_PER_PIXEL
