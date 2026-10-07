extends RefCounted
class_name CrystalFormLayer

## L3 第四层：晶胞 (Unit Cell)
## 分子间/多面体间的周期性堆积：空间群、布拉维格子、晶格参数、Wyckoff位坐标
## 晶胞是具体参数化实体（晶型是分类标签如"晶型I/II"）
## 可控性：模式库 — 从已知超导家族提取堆积经验规则

signal crystal_form_changed()
signal polymorph_detected(polymorph_id: String)

var _cell_params: Dictionary = {
	"a": 1.0, "b": 1.0, "c": 1.0,
	"alpha": 90.0, "beta": 90.0, "gamma": 90.0
}
var _space_group: int = 1  # ITA number (1-230)
var _space_group_name: String = "P1"
var _asymmetric_unit: Array = []  # List of {atom_id, position, occupancy}
var _polymorph_id: String = "default"
var _intermolecular_bonds: Array = []  # H-bonds, van der Waals, pi-pi stacking
var _z: int = 1  # Number of formula units per unit cell

func get_layer_name() -> String:
	return "晶胞"

func get_layer_index() -> int:
	return 4

func get_controllability() -> String:
	return "模式库 (从已知超导家族提取堆积经验)"

func get_description() -> String:
	return "分子间周期性堆积方式。决定溶解度、熔点、密度、固态稳定性。相对位置是单个分子形状，晶胞是一堆分子怎么抱团。晶胞分布可作为Regge单元（嘉当矩阵），角亏场直接给出FG退相干场强度。"

func set_cell_parameters(a: float, b: float, c: float, alpha: float, beta: float, gamma: float) -> void:
	_cell_params = {"a": a, "b": b, "c": c, "alpha": alpha, "beta": beta, "gamma": gamma}
	crystal_form_changed.emit()

func get_cell_parameters() -> Dictionary:
	return _cell_params.duplicate()

func set_space_group(ita_number: int, sg_name: String = "") -> void:
	_space_group = clampi(ita_number, 1, 230)
	_space_group_name = sg_name if sg_name != "" else _lookup_space_group_name(_space_group)
	crystal_form_changed.emit()

func get_space_group() -> int:
	return _space_group

func get_space_group_name() -> String:
	return _space_group_name

func set_z(z: int) -> void:
	_z = maxi(z, 1)
	crystal_form_changed.emit()

func get_z() -> int:
	return _z

func compute_cell_volume() -> float:
	var a = _cell_params.a
	var b = _cell_params.b
	var c = _cell_params.c
	var alpha = deg_to_rad(_cell_params.alpha)
	var beta = deg_to_rad(_cell_params.beta)
	var gamma = deg_to_rad(_cell_params.gamma)
	return a * b * c * sqrt(1.0
		- cos(alpha) ** 2
		- cos(beta) ** 2
		- cos(gamma) ** 2
		+ 2.0 * cos(alpha) * cos(beta) * cos(gamma))

func compute_density(molecular_weight: float) -> float:
	var vol = compute_cell_volume()
	if vol <= 0:
		return 0.0
	var n_avogadro = 6.02214076e23
	var vol_cm3 = vol * 1e-24  # Å³ to cm³
	return (_z * molecular_weight) / (n_avogadro * vol_cm3)

func set_asymmetric_unit(atoms: Array) -> void:
	_asymmetric_unit = atoms.duplicate(true)
	crystal_form_changed.emit()

func get_asymmetric_unit() -> Array:
	return _asymmetric_unit.duplicate(true)

func add_intermolecular_bond(bond_info: Dictionary) -> void:
	_intermolecular_bonds.append(bond_info)
	crystal_form_changed.emit()

func get_intermolecular_bonds() -> Array:
	return _intermolecular_bonds.duplicate(true)

func detect_polymorph() -> String:
	var fingerprint = _compute_polymorph_fingerprint()
	if fingerprint == _polymorph_id:
		return _polymorph_id
	_polymorph_id = fingerprint
	polymorph_detected.emit(fingerprint)
	return fingerprint

func _compute_polymorph_fingerprint() -> String:
	return "SG%d_Z%d_V%.2f" % [_space_group, _z, compute_cell_volume()]

func get_crystal_system() -> String:
	match _space_group:
		1, 2: return "triclinic"
		3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15: return "monoclinic"
		16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74: return "orthorhombic"
		75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142: return "tetragonal"
		143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167: return "trigonal"
		168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194: return "hexagonal"
		195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230: return "cubic"
		_: return "unknown"

func _lookup_space_group_name(ita: int) -> String:
	var names = {
		1: "P1", 2: "P-1",
		15: "C2/c", 14: "P21/c",
		19: "P212121",
		33: "Pna21",
		62: "Pnma",
		167: "R-3c",
		176: "P63/m",
		194: "P63/mmc",
		225: "Fm-3m", 227: "Fd-3m",
	}
	return names.get(ita, "SG#%d" % ita)

func to_dict() -> Dictionary:
	return {
		"layer": "crystal_form",
		"cell_params": _cell_params.duplicate(),
		"space_group": _space_group,
		"space_group_name": _space_group_name,
		"z": _z,
		"asymmetric_unit": _asymmetric_unit.duplicate(true),
		"intermolecular_bonds": _intermolecular_bonds.duplicate(true),
		"polymorph_id": _polymorph_id,
		"cell_volume": compute_cell_volume(),
		"crystal_system": get_crystal_system(),
	}

func from_dict(data: Dictionary) -> void:
	_cell_params = data.get("cell_params", _cell_params).duplicate()
	_space_group = data.get("space_group", 1)
	_space_group_name = data.get("space_group_name", "P1")
	_z = data.get("z", 1)
	_asymmetric_unit = data.get("asymmetric_unit", []).duplicate(true)
	_intermolecular_bonds = data.get("intermolecular_bonds", []).duplicate(true)
	_polymorph_id = data.get("polymorph_id", "default")
	crystal_form_changed.emit()