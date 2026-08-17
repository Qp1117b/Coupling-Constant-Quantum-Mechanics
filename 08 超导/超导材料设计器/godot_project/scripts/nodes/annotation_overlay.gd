extends Node3D
class_name AnnotationOverlay

# 3D 可视化标注覆盖层
# 原子标签、键长标注、角度弧、测量值持久显示

var _label_root: Node3D
var _atom_labels: Dictionary = {}
var _bond_labels: Dictionary = {}
var _angle_arcs: Dictionary = {}
var _measure_labels: Array = []
var _label_font_size: int = 16
var _show_atom_labels: bool = true
var _show_bond_labels: bool = false
var _show_angle_arcs: bool = true
var _label_bg_color: Color = Color(0.08, 0.1, 0.15, 0.85)
var _label_fg_color: Color = Color(0.85, 0.9, 1.0)
var _bond_label_color: Color = Color(0.4, 0.9, 0.5)
var _measure_color: Color = Color(0.95, 0.8, 0.2)

func _ready():
	_label_root = Node3D.new()
	_label_root.name = "AnnotationLabels"
	add_child(_label_root)

func set_show_atom_labels(visible: bool):
	_show_atom_labels = visible
	for label in _atom_labels.values():
		if is_instance_valid(label):
			label.visible = visible

func set_show_bond_labels(visible: bool):
	_show_bond_labels = visible
	for label in _bond_labels.values():
		if is_instance_valid(label):
			label.visible = visible

func set_show_angle_arcs(visible: bool):
	_show_angle_arcs = visible
	for arc in _angle_arcs.values():
		if is_instance_valid(arc):
			arc.visible = visible

# === 原子标签 ===

func add_atom_label(atom: Node, text: String = "", color: Color = Color(0, 0, 0, 0)):
	if not is_instance_valid(atom):
		return
	var key = atom.get_instance_id()
	if _atom_labels.has(key):
		update_atom_label(atom, text, color)
		return
	if text.is_empty():
		text = "%s%d" % [atom.element_symbol, atom.isotope_mass]
	var label = _create_label_3d(text, color if color != Color(0, 0, 0, 0) else _label_fg_color)
	label.position = atom.global_position + Vector3(0, atom.atom_radius + 0.15, 0)
	_atom_labels[key] = label
	_label_root.add_child(label)
	label.visible = _show_atom_labels

func update_atom_label(atom: Node, text: String = "", color: Color = Color(0, 0, 0, 0)):
	if not is_instance_valid(atom):
		return
	var key = atom.get_instance_id()
	if not _atom_labels.has(key):
		add_atom_label(atom, text, color)
		return
	var label = _atom_labels[key]
	if is_instance_valid(label):
		label.position = atom.global_position + Vector3(0, atom.atom_radius + 0.15, 0)
		if not text.is_empty():
			label.text = text

func remove_atom_label(atom: Node):
	if not is_instance_valid(atom):
		return
	var key = atom.get_instance_id()
	if _atom_labels.has(key):
		var label = _atom_labels[key]
		if is_instance_valid(label):
			label.queue_free()
		_atom_labels.erase(key)

func clear_atom_labels():
	for label in _atom_labels.values():
		if is_instance_valid(label):
			label.queue_free()
	_atom_labels.clear()

# === 键长标注 ===

func add_bond_label(bond: Node, color: Color = Color(0, 0, 0, 0)):
	if not is_instance_valid(bond):
		return
	var key = bond.get_instance_id()
	if _bond_labels.has(key):
		return
	var mid = (bond.atom_a.global_position + bond.atom_b.global_position) / 2.0
	var text = "%.3f Å" % bond.bond_length
	var label = _create_label_3d(text, color if color != Color(0, 0, 0, 0) else _bond_label_color)
	label.position = mid + Vector3(0, 0.1, 0)
	_bond_labels[key] = label
	_label_root.add_child(label)
	label.visible = _show_bond_labels

func update_bond_label(bond: Node):
	if not is_instance_valid(bond):
		return
	var key = bond.get_instance_id()
	if not _bond_labels.has(key):
		return
	var label = _bond_labels[key]
	if is_instance_valid(label):
		var mid = (bond.atom_a.global_position + bond.atom_b.global_position) / 2.0
		label.position = mid + Vector3(0, 0.1, 0)
		label.text = "%.3f Å" % bond.bond_length

func remove_bond_label(bond: Node):
	if not is_instance_valid(bond):
		return
	var key = bond.get_instance_id()
	if _bond_labels.has(key):
		var label = _bond_labels[key]
		if is_instance_valid(label):
			label.queue_free()
		_bond_labels.erase(key)

func clear_bond_labels():
	for label in _bond_labels.values():
		if is_instance_valid(label):
			label.queue_free()
	_bond_labels.clear()

# === 角度弧 ===

func add_angle_arc(atom_a: Node3D, center: Node3D, atom_b: Node3D, color: Color = Color(0, 0, 0, 0)):
	var key = str(atom_a.get_instance_id()) + "_" + str(center.get_instance_id()) + "_" + str(atom_b.get_instance_id())
	if _angle_arcs.has(key):
		return
	var arc = _create_angle_arc(atom_a, center, atom_b, color)
	if arc:
		_angle_arcs[key] = arc
		_label_root.add_child(arc)
		arc.visible = _show_angle_arcs

func _create_angle_arc(a: Node3D, center: Node3D, b: Node3D, color: Color) -> MeshInstance3D:
	var va = a.global_position - center.global_position
	var vb = b.global_position - center.global_position
	var angle = va.angle_to(vb)
	if angle < 0.01 or angle > PI - 0.01:
		return null
	var radius = min(va.length(), vb.length()) * 0.3
	var segments = max(8, int(angle * 16))
	var points: Array = []
	for i in range(segments + 1):
		var t = float(i) / segments
		var theta = t * angle
		var dir = va.normalized().rotated(va.cross(vb).normalized(), theta)
		points.append(center.global_position + dir * radius)
	var imm_mesh = ImmediateMesh.new()
	imm_mesh.surface_begin(Mesh.PRIMITIVE_LINE_STRIP)
	var c = color if color != Color(0, 0, 0, 0) else Color(0.5, 0.7, 1.0, 0.8)
	imm_mesh.surface_set_color(c)
	for p in points:
		imm_mesh.surface_add_vertex(p)
	imm_mesh.surface_end()
	var mi = MeshInstance3D.new()
	mi.mesh = imm_mesh
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	return mi

func clear_angle_arcs():
	for arc in _angle_arcs.values():
		if is_instance_valid(arc):
			arc.queue_free()
	_angle_arcs.clear()

# === 测量值持久显示 ===

func add_measurement_label(pos: Vector3, text: String, color: Color = Color(0, 0, 0, 0)):
	var label = _create_label_3d(text, color if color != Color(0, 0, 0, 0) else _measure_color)
	label.position = pos
	_measure_labels.append(label)
	_label_root.add_child(label)

func clear_measurement_labels():
	for label in _measure_labels:
		if is_instance_valid(label):
			label.queue_free()
	_measure_labels.clear()

# === 标签创建 ===

func _create_label_3d(text: String, color: Color) -> Label3D:
	var label = Label3D.new()
	label.text = text
	label.font_size = _label_font_size
	label.outline_size = 4
	label.outline_modulate = Color(0, 0, 0, 0.9)
	label.modulate = color
	label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	label.shaded = false
	label.no_depth_test = true
	label.render_priority = 10
	return label

func clear_all():
	clear_atom_labels()
	clear_bond_labels()
	clear_angle_arcs()
	clear_measurement_labels()

func update_all_atom_labels(atoms: Array):
	for atom in atoms:
		if is_instance_valid(atom):
			update_atom_label(atom)

func update_all_bond_labels(bonds: Array):
	for bond in bonds:
		if is_instance_valid(bond):
			update_bond_label(bond)