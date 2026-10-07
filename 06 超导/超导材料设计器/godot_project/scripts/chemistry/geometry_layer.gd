extends RefCounted
class_name GeometryLayer

## 第三层：相对位置 (Relative Position / Geometry)
## 在结合方式固定后，原子在三维空间中的精确几何排布
## 包括键长、键角、二面角、手性构型、顺反异构、构象
## 可控性：部分可控 — 构型可控(手性/顺反)，构象统计(热力学系综)

signal geometry_changed()
signal position_set(atom_id: int, position: Vector3)

var _positions: Dictionary = {}  # atom_id -> Vector3
var _bond_lengths: Dictionary = {}  # "a_b" -> float
var _bond_angles: Dictionary = {}  # "a_b_c" -> float (degrees)
var _dihedral_angles: Dictionary = {}  # "a_b_c_d" -> float (degrees)

var _conformation: String = "unknown"  # chair, boat, staggered, eclipsed, etc.
var _chirality: String = "none"  # R, S, none
var _cis_trans: String = "none"  # cis, trans, none

func get_layer_name() -> String:
	return "相对位置"

func get_layer_index() -> int:
	return 3

func get_controllability() -> String:
	return "部分可控 (构型可控, 构象统计)"

func get_description() -> String:
	return "分子内三维几何排布。决定立体化学、精细物性、生物活性。结合方式提供骨架，相对位置是骨架的姿势。"

func set_position(atom_id: int, pos: Vector3) -> void:
	_positions[atom_id] = pos
	position_set.emit(atom_id, pos)
	geometry_changed.emit()

func get_position(atom_id: int) -> Vector3:
	return _positions.get(atom_id, Vector3.ZERO)

func set_all_positions(positions: Dictionary) -> void:
	_positions = positions.duplicate()
	geometry_changed.emit()

func get_all_positions() -> Dictionary:
	return _positions.duplicate()

func compute_bond_length(a_id: int, b_id: int) -> float:
	var pa = _positions.get(a_id)
	var pb = _positions.get(b_id)
	if pa == null or pb == null:
		return 0.0
	return pa.distance_to(pb)

func compute_bond_angle(a_id: int, b_id: int, c_id: int) -> float:
	var pa = _positions.get(a_id)
	var pb = _positions.get(b_id)
	var pc = _positions.get(c_id)
	if pa == null or pb == null or pc == null:
		return 0.0
	var v1 = (pa - pb).normalized()
	var v2 = (pc - pb).normalized()
	var dot = clampf(v1.dot(v2), -1.0, 1.0)
	return rad_to_deg(acos(dot))

func compute_dihedral_angle(a_id: int, b_id: int, c_id: int, d_id: int) -> float:
	var pa = _positions.get(a_id)
	var pb = _positions.get(b_id)
	var pc = _positions.get(c_id)
	var pd = _positions.get(d_id)
	if pa == null or pb == null or pc == null or pd == null:
		return 0.0
	var b1 = (pb - pa).normalized()
	var b2 = (pc - pb).normalized()
	var b3 = (pd - pc).normalized()
	var n1 = b1.cross(b2).normalized()
	var n2 = b2.cross(b3).normalized()
	var dot = clampf(n1.dot(n2), -1.0, 1.0)
	return rad_to_deg(acos(dot))

func update_all_geometric_params(bonds: Array, angles: Array, dihedrals: Array) -> void:
	_bond_lengths.clear()
	for b in bonds:
		var key = "%d_%d" % [min(b.a_id, b.b_id), max(b.a_id, b.b_id)]
		_bond_lengths[key] = compute_bond_length(b.a_id, b.b_id)
	_bond_angles.clear()
	for a in angles:
		var key = "%d_%d_%d" % [a.a_id, a.b_id, a.c_id]
		_bond_angles[key] = compute_bond_angle(a.a_id, a.b_id, a.c_id)
	_dihedral_angles.clear()
	for d in dihedrals:
		var key = "%d_%d_%d_%d" % [d.a_id, d.b_id, d.c_id, d.d_id]
		_dihedral_angles[key] = compute_dihedral_angle(d.a_id, d.b_id, d.c_id, d.d_id)

func get_bond_length(a_id: int, b_id: int) -> float:
	var key = "%d_%d" % [min(a_id, b_id), max(a_id, b_id)]
	return _bond_lengths.get(key, 0.0)

func get_bond_angle(a_id: int, b_id: int, c_id: int) -> float:
	var key = "%d_%d_%d" % [a_id, b_id, c_id]
	return _bond_angles.get(key, 0.0)

func get_dihedral_angle(a_id: int, b_id: int, c_id: int, d_id: int) -> float:
	var key = "%d_%d_%d_%d" % [a_id, b_id, c_id, d_id]
	return _dihedral_angles.get(key, 0.0)

func set_conformation(conf: String) -> void:
	_conformation = conf
	geometry_changed.emit()

func get_conformation() -> String:
	return _conformation

func set_chirality(ch: String) -> void:
	_chirality = ch
	geometry_changed.emit()

func get_chirality() -> String:
	return _chirality

func set_cis_trans(ct: String) -> void:
	_cis_trans = ct
	geometry_changed.emit()

func get_cis_trans() -> String:
	return _cis_trans

func compute_molecular_center() -> Vector3:
	if _positions.is_empty():
		return Vector3.ZERO
	var center = Vector3.ZERO
	for id in _positions:
		center += _positions[id]
	return center / _positions.size()

func compute_dipole_moment(charges: Dictionary = {}) -> Vector3:
	var dipole = Vector3.ZERO
	for id in _positions:
		var q = charges.get(id, 0.0)
		dipole += _positions[id] * q
	return dipole

func translate(offset: Vector3) -> void:
	for id in _positions:
		_positions[id] += offset
	geometry_changed.emit()

func rotate(axis: Vector3, angle: float) -> void:
	var center = compute_molecular_center()
	var norm_axis = axis.normalized()
	for id in _positions:
		_positions[id] = center + (_positions[id] - center).rotated(norm_axis, angle)
	geometry_changed.emit()

func scale(factor: float) -> void:
	var center = compute_molecular_center()
	for id in _positions:
		_positions[id] = center + (_positions[id] - center) * factor
	geometry_changed.emit()

func to_dict() -> Dictionary:
	var pos_dict: Dictionary = {}
	for id in _positions:
		pos_dict[id] = {"x": _positions[id].x, "y": _positions[id].y, "z": _positions[id].z}
	return {
		"layer": "geometry",
		"positions": pos_dict,
		"bond_lengths": _bond_lengths.duplicate(),
		"bond_angles": _bond_angles.duplicate(),
		"dihedral_angles": _dihedral_angles.duplicate(),
		"conformation": _conformation,
		"chirality": _chirality,
		"cis_trans": _cis_trans,
	}

func from_dict(data: Dictionary) -> void:
	_positions.clear()
	var pos_data = data.get("positions", {})
	for id in pos_data:
		var p = pos_data[id]
		_positions[int(id)] = Vector3(p.x, p.y, p.z)
	_conformation = data.get("conformation", "unknown")
	_chirality = data.get("chirality", "none")
	_cis_trans = data.get("cis_trans", "none")
	geometry_changed.emit()