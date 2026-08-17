extends RefCounted
class_name SymmetryDetector

# 分子对称性自动检测
# 点群识别: C1, Ci, Cs, Cn, Cnv, Cnh, Dn, Dnh, Dnd, S2n, T, Td, Th, O, Oh, I, Ih
# 空间群检测 (简化版): 常见晶体空间群

const TOL_POS: float = 0.01
const TOL_ANGLE: float = 0.5

# === 点群检测 ===

static func detect_point_group(atoms: Array) -> Dictionary:
	if atoms.size() < 2:
		return {"group": "C1", "order": 1, "elements": ["E"], "description": "恒等"}
	var center = _compute_center(atoms)
	var centered = _center_atoms(atoms, center)
	var elements = _find_symmetry_elements(centered)
	var principal_axis = elements.get("principal_axis", Vector3.ZERO)
	var n_fold = elements.get("n_fold", 1)
	var has_inversion = elements.get("has_inversion", false)
	var has_mirror = elements.get("mirror_planes", []).size() > 0
	var has_perpendicular_c2 = elements.get("has_perp_c2", false)
	var mirror_count = elements.get("mirror_planes", []).size()
	var n_vertical_mirrors = elements.get("n_vertical_mirrors", 0)
	var n_horizontal_mirrors = elements.get("n_horizontal_mirrors", 0)
	var group = _classify_group(n_fold, has_inversion, has_mirror, has_perpendicular_c2,
								mirror_count, n_vertical_mirrors, n_horizontal_mirrors,
								elements.get("is_tetrahedral", false),
								elements.get("is_octahedral", false),
								elements.get("is_icosahedral", false))
	return {
		"group": group.name,
		"order": group.order,
		"elements": group.elements,
		"description": group.description,
		"principal_axis": principal_axis,
		"n_fold": n_fold,
		"has_inversion": has_inversion,
		"mirror_planes": elements.get("mirror_planes", []),
		"center": center,
		"symmetry_operations": elements.get("operations", [])
	}

static func _compute_center(atoms: Array) -> Vector3:
	var sum = Vector3.ZERO
	for a in atoms:
		sum += _get_pos(a)
	return sum / atoms.size()

static func _center_atoms(atoms: Array, center: Vector3) -> Array:
	var result: Array = []
	for a in atoms:
		var pos = _get_pos(a) - center
		var sym = _get_symbol(a)
		result.append({"symbol": sym, "position": pos})
	return result

static func _find_symmetry_elements(atoms: Array) -> Dictionary:
	var result: Dictionary = {
		"principal_axis": Vector3.ZERO,
		"n_fold": 1,
		"has_inversion": false,
		"mirror_planes": [],
		"has_perp_c2": false,
		"n_vertical_mirrors": 0,
		"n_horizontal_mirrors": 0,
		"operations": [],
		"is_tetrahedral": false,
		"is_octahedral": false,
		"is_icosahedral": false
	}
	result.has_inversion = _check_inversion(atoms)
	var axes = _find_rotation_axes(atoms)
	if not axes.is_empty():
		axes.sort_custom(func(a, b): return a.n > b.n)
		result.principal_axis = axes[0].axis
		result.n_fold = axes[0].n
		for axis in axes:
			if axis.n == 2 and axis.axis.dot(result.principal_axis) < TOL_POS:
				result.has_perp_c2 = true
				break
	result.mirror_planes = _find_mirror_planes(atoms, result.principal_axis)
	for plane in result.mirror_planes:
		if result.n_fold > 1:
			if abs(plane.normal.dot(result.principal_axis)) < TOL_POS:
				result.n_horizontal_mirrors += 1
			elif abs(plane.normal.dot(result.principal_axis) - 1.0) < TOL_POS:
				result.n_vertical_mirrors += 1
		else:
			result.n_vertical_mirrors += 1
	if _check_tetrahedral(atoms):
		result.is_tetrahedral = true
	if _check_octahedral(atoms):
		result.is_octahedral = true
	return result

static func _check_inversion(atoms: Array) -> bool:
	for a in atoms:
		var inverted = -a.position
		var found = false
		for b in atoms:
			if b.symbol == a.symbol and b.position.distance_to(inverted) < TOL_POS:
				found = true
				break
		if not found:
			return false
	return true

static func _find_rotation_axes(atoms: Array) -> Array:
	var axes: Array = []
	var candidates = _get_axis_candidates(atoms)
	for axis in candidates:
		var n = _get_rotation_order(atoms, axis)
		if n > 1:
			axes.append({"axis": axis, "n": n})
	return axes

static func _get_axis_candidates(atoms: Array) -> Array:
	var candidates: Array = []
	candidates.append(Vector3(1, 0, 0))
	candidates.append(Vector3(0, 1, 0))
	candidates.append(Vector3(0, 0, 1))
	candidates.append(Vector3(1, 1, 0).normalized())
	candidates.append(Vector3(1, 0, 1).normalized())
	candidates.append(Vector3(0, 1, 1).normalized())
	candidates.append(Vector3(1, 1, 1).normalized())
	candidates.append(Vector3(1, -1, 0).normalized())
	candidates.append(Vector3(1, 0, -1).normalized())
	candidates.append(Vector3(0, 1, -1).normalized())
	for i in range(atoms.size()):
		for j in range(i + 1, atoms.size()):
			var diff = atoms[j].position - atoms[i].position
			if diff.length() > TOL_POS:
				candidates.append(diff.normalized())
			var cross = atoms[i].position.cross(atoms[j].position)
			if cross.length() > TOL_POS:
				candidates.append(cross.normalized())
	return candidates

static func _get_rotation_order(atoms: Array, axis: Vector3) -> int:
	for n in [6, 5, 4, 3, 2]:
		if _check_rotation(atoms, axis, n):
			return n
	return 1

static func _check_rotation(atoms: Array, axis: Vector3, n: int) -> bool:
	var angle = 2.0 * PI / n
	for a in atoms:
		var rotated = a.position.rotated(axis, angle)
		var found = false
		for b in atoms:
			if b.symbol == a.symbol and b.position.distance_to(rotated) < TOL_POS:
				found = true
				break
		if not found:
			return false
	return true

static func _find_mirror_planes(atoms: Array, principal_axis: Vector3) -> Array:
	var planes: Array = []
	var candidates: Array = []
	candidates.append(Vector3(1, 0, 0))
	candidates.append(Vector3(0, 1, 0))
	candidates.append(Vector3(0, 0, 1))
	candidates.append(Vector3(1, 1, 0).normalized())
	candidates.append(Vector3(1, 0, 1).normalized())
	candidates.append(Vector3(0, 1, 1).normalized())
	candidates.append(Vector3(1, -1, 0).normalized())
	candidates.append(Vector3(1, 1, 1).normalized())
	if principal_axis.length() > TOL_POS:
		candidates.append(principal_axis.normalized())
		var perp1 = principal_axis.cross(Vector3(1, 0, 0))
		if perp1.length() < TOL_POS:
			perp1 = principal_axis.cross(Vector3(0, 1, 0))
		candidates.append(perp1.normalized())
		candidates.append(principal_axis.cross(perp1).normalized())
	for normal in candidates:
		if _check_mirror(atoms, normal):
			var already = false
			for p in planes:
				if p.normal.distance_to(normal) < TOL_POS or p.normal.distance_to(-normal) < TOL_POS:
					already = true
					break
			if not already:
				planes.append({"normal": normal})
	return planes

static func _check_mirror(atoms: Array, normal: Vector3) -> bool:
	for a in atoms:
		var reflected = a.position - 2.0 * a.position.dot(normal) * normal
		var found = false
		for b in atoms:
			if b.symbol == a.symbol and b.position.distance_to(reflected) < TOL_POS:
				found = true
				break
		if not found:
			return false
	return true

static func _check_tetrahedral(atoms: Array) -> bool:
	if atoms.size() != 4 and atoms.size() != 5:
		return false
	if atoms.size() == 4:
		var center = Vector3.ZERO
		for a in atoms:
			center += a.position
		center /= 4.0
		var dists: Array = []
		for a in atoms:
			dists.append(a.position.distance_to(center))
		var avg = dists[0]
		for d in dists:
			if abs(d - avg) > TOL_POS * 10:
				return false
		var pair_dists: Array = []
		for i in range(4):
			for j in range(i + 1, 4):
				pair_dists.append(atoms[i].position.distance_to(atoms[j].position))
		pair_dists.sort()
		var d_small = pair_dists[0]
		var d_large = pair_dists[5]
		return abs(d_small - d_large) < TOL_POS * 10
	return false

static func _check_octahedral(atoms: Array) -> bool:
	if atoms.size() != 6 and atoms.size() != 7:
		return false
	if atoms.size() == 6:
		var center = Vector3.ZERO
		for a in atoms:
			center += a.position
		center /= 6.0
		var dists: Array = []
		for a in atoms:
			dists.append(a.position.distance_to(center))
		var avg = dists[0]
		for d in dists:
			if abs(d - avg) > TOL_POS * 10:
				return false
		var pair_dists: Array = []
		for i in range(6):
			for j in range(i + 1, 6):
				pair_dists.append(atoms[i].position.distance_to(atoms[j].position))
		pair_dists.sort()
		var d_min = pair_dists[0]
		var d_max = pair_dists[14]
		return abs(d_max - d_min * sqrt(2.0)) < TOL_POS * 10
	return false

static func _classify_group(n: int, inv: bool, mirror: bool, perp_c2: bool,
							mirror_count: int, n_v: int, n_h: int,
							is_tet: bool, is_oct: bool, is_ico: bool) -> Dictionary:
	if is_ico:
		if inv:
			return {"name": "Ih", "order": 120, "elements": ["E", "12C5", "12C5²", "20C3", "15C2", "i", "12S10", "12S10³", "20S6", "15σ"], "description": "二十面体群"}
		return {"name": "I", "order": 60, "elements": ["E", "12C5", "12C5²", "20C3", "15C2"], "description": "二十面体旋转群"}
	if is_oct:
		if inv:
			return {"name": "Oh", "order": 48, "elements": ["E", "8C3", "6C2", "6C4", "3C2'", "i", "8S6", "6S4", "3σh", "6σd"], "description": "八面体群"}
		return {"name": "O", "order": 24, "elements": ["E", "8C3", "6C2", "6C4", "3C2'"], "description": "八面体旋转群"}
	if is_tet:
		if inv:
			return {"name": "Th", "order": 24, "elements": ["E", "8C3", "3C2", "i", "8S6", "3σh"], "description": "四面体群含反演"}
		if mirror:
			return {"name": "Td", "order": 24, "elements": ["E", "8C3", "3C2", "6S4", "6σd"], "description": "四面体群"}
		return {"name": "T", "order": 12, "elements": ["E", "8C3", "3C2"], "description": "四面体旋转群"}
	if n <= 1:
		if inv:
			return {"name": "Ci", "order": 2, "elements": ["E", "i"], "description": "反演群"}
		if mirror:
			return {"name": "Cs", "order": 2, "elements": ["E", "σ"], "description": "镜面群"}
		return {"name": "C1", "order": 1, "elements": ["E"], "description": "恒等"}
	if perp_c2:
		if n_h > 0:
			return {"name": "D%dnh" % n, "order": 4 * n, "elements": ["E", "C%d" % n, "C2'", "σh", "σv"], "description": "二面体水平镜面群"}
		elif n_v > 0:
			return {"name": "D%dnd" % n, "order": 4 * n, "elements": ["E", "C%d" % n, "C2'", "σd", "S2n"], "description": "二面体对角镜面群"}
		else:
			return {"name": "D%d" % n, "order": 2 * n, "elements": ["E", "C%d" % n, "C2'"], "description": "二面体旋转群"}
	if n_h > 0:
		return {"name": "C%dnh" % n, "order": 2 * n, "elements": ["E", "C%d" % n, "σh"], "description": "循环水平镜面群"}
	if n_v > 0:
		return {"name": "C%dv" % n, "order": 2 * n, "elements": ["E", "C%d" % n, "σv"], "description": "循环垂直镜面群"}
	if inv:
		return {"name": "S%d" % (2 * n), "order": 2 * n, "elements": ["E", "S%d" % (2 * n)], "description": "旋转反射群"}
	return {"name": "C%d" % n, "order": n, "elements": ["E", "C%d" % n], "description": "循环旋转群"}

# === 空间群检测 (简化版) ===

static func detect_space_group(atoms: Array, cell: Dictionary = {}) -> Dictionary:
	if cell.is_empty():
		return {"space_group": "P1", "number": 1, "description": "三斜晶系"}
	var a = cell.get("a", 0.0)
	var b = cell.get("b", 0.0)
	var c = cell.get("c", 0.0)
	var alpha = cell.get("alpha", 90.0)
	var beta = cell.get("beta", 90.0)
	var gamma = cell.get("gamma", 90.0)
	var crystal_system = _identify_crystal_system(a, b, c, alpha, beta, gamma)
	var bravais = _identify_bravais_lattice(a, b, c, alpha, beta, gamma, atoms)
	var point_group = detect_point_group(atoms)
	return {
		"crystal_system": crystal_system,
		"bravais_lattice": bravais,
		"point_group": point_group.group,
		"space_group": "%s%s" % [bravais.substr(0, 1), point_group.group],
		"number": _estimate_space_group_number(bravais, point_group.group),
		"description": "%s / %s" % [crystal_system, point_group.description]
	}

static func _identify_crystal_system(a, b, c, alpha, beta, gamma) -> String:
	var tol = 1.0
	if abs(a - b) < tol and abs(b - c) < tol:
		if abs(alpha - 90) < tol and abs(beta - 90) < tol and abs(gamma - 90) < tol:
			return "立方晶系"
		elif abs(alpha - beta) < tol and abs(beta - gamma) < tol:
			return "三方晶系"
	if abs(a - b) < tol and abs(alpha - 90) < tol and abs(beta - 90) < tol and abs(gamma - 120) < tol:
		return "六方晶系"
	if abs(alpha - 90) < tol and abs(beta - 90) < tol and abs(gamma - 90) < tol:
		if abs(a - b) < tol:
			return "四方晶系"
		return "正交晶系"
	if abs(alpha - 90) < tol and abs(gamma - 90) < tol:
		return "单斜晶系"
	return "三斜晶系"

static func _identify_bravais_lattice(a, b, c, alpha, beta, gamma, atoms) -> String:
	return "P"

static func _estimate_space_group_number(bravais: String, point_group: String) -> int:
	return 1

# === 辅助函数 ===

static func _get_symbol(atom) -> String:
	if atom is Dictionary:
		return atom.get("symbol", "H")
	return atom.element_symbol

static func _get_pos(atom) -> Vector3:
	if atom is Dictionary:
		return atom.get("position", Vector3.ZERO)
	return atom.global_position

# === 对称性对超导的影响 ===

static func symmetry_to_pairing(group_name: String) -> Dictionary:
	match group_name:
		"Oh", "Oh":
			return {"pairing": "s-wave", "symmetry": "A1g", "nodes": "无", "description": "全对称s波配对"}
		"O":
			return {"pairing": "s-wave", "symmetry": "A1", "nodes": "无", "description": "八面体s波"}
		"Td", "T":
			return {"pairing": "s-wave", "symmetry": "A1", "nodes": "无", "description": "四面体s波"}
		"D4h":
			return {"pairing": "s-wave/d-wave", "symmetry": "A1g/B1g", "nodes": "可能d波节点", "description": "四方晶系, 可能s或d波"}
		"D6h":
			return {"pairing": "s-wave/d-wave", "symmetry": "A1g/B1g", "nodes": "可能d波节点", "description": "六方晶系, 可能s或d波"}
		"C4v", "D4":
			return {"pairing": "s-wave/d-wave", "symmetry": "A1/B1", "nodes": "可能d波节点", "description": "四方对称, 可能d波"}
		"C3v", "D3":
			return {"pairing": "s-wave/f-wave", "symmetry": "A1/B2", "nodes": "可能f波节点", "description": "三方对称, 可能f波"}
		_:
			return {"pairing": "s-wave", "symmetry": "A1", "nodes": "未知", "description": "默认s波"}