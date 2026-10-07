extends Node

const MAX_VALENCE: Dictionary = {
	"H": 1, "F": 1, "Cl": 1, "Br": 1, "I": 1, "At": 1,
	"O": 2, "S": 6, "Se": 6, "Te": 6,
	"N": 4, "P": 5, "As": 5, "Sb": 5, "Bi": 5,
	"C": 4, "Si": 4, "Ge": 4, "Sn": 4, "Pb": 4,
	"B": 3, "Al": 6, "Ga": 3, "In": 3, "Tl": 3,
	"Be": 4, "Mg": 6, "Ca": 6, "Sr": 6, "Ba": 6,
	"Li": 4, "Na": 6, "K": 6, "Rb": 6, "Cs": 6,
	"Zn": 4, "Cd": 4, "Hg": 4,
	"Cu": 4, "Ag": 4, "Au": 4,
	"Fe": 6, "Co": 6, "Ni": 6, "Mn": 6, "Cr": 6,
	"Ti": 6, "V": 6, "Zr": 6, "Nb": 6, "Mo": 6, "W": 6, "Ta": 6,
	"Ru": 6, "Rh": 6, "Pd": 4, "Os": 6, "Ir": 6, "Pt": 4,
	"Y": 8, "La": 8, "Ce": 8, "U": 8,
	"Sc": 6, "Tc": 6, "Re": 6, "Hf": 6,
	"Nd": 8, "Sm": 8, "Eu": 8, "Gd": 8, "Tb": 8, "Dy": 8,
	"Ho": 8, "Er": 8, "Tm": 8, "Yb": 8, "Lu": 8,
	"Ne": 0, "Ar": 0, "Kr": 2, "Xe": 2, "Rn": 2
}

const VSEPR_ANGLES: Dictionary = {
	2: 180.0,
	3: 120.0,
	4: 109.47,
	5: 90.0,
	6: 90.0
}

const BOND_TOLERANCE_GOOD: float = 0.10
const BOND_TOLERANCE_WARN: float = 0.25
const BOND_MIN_FACTOR: float = 0.5
const BOND_MAX_FACTOR: float = 2.0

func ideal_bond_length(sym_a: String, sym_b: String) -> float:
	var data_a = ElementDB.get_element(sym_a)
	var data_b = ElementDB.get_element(sym_b)
	var r_a = float(data_a.get("covalent_radius_pm", 50)) / 100.0
	var r_b = float(data_b.get("covalent_radius_pm", 50)) / 100.0
	return r_a + r_b

func validate_bond(sym_a: String, sym_b: String, actual_length: float) -> Dictionary:
	var ideal = ideal_bond_length(sym_a, sym_b)
	if ideal <= 0.0 or actual_length <= 0.0:
		return {
			"valid": false,
			"reason": "无效长度",
			"ideal_len": ideal,
			"actual_len": actual_length,
			"deviation": 1.0,
			"color": Color(0.5, 0.5, 0.5)
		}
	var dev = abs(actual_length - ideal) / ideal
	var color: Color
	var reason: String
	if dev <= BOND_TOLERANCE_GOOD:
		color = Color(0.2, 0.85, 0.3)
		reason = "理想"
	elif dev <= BOND_TOLERANCE_WARN:
		color = Color(0.9, 0.75, 0.2)
		reason = "偏差较大"
	else:
		color = Color(0.9, 0.25, 0.2)
		reason = "偏差过大"
	return {
		"valid": dev <= BOND_TOLERANCE_WARN,
		"reason": reason,
		"ideal_len": ideal,
		"actual_len": actual_length,
		"deviation": dev,
		"color": color
	}

func max_valence(symbol: String) -> int:
	return int(MAX_VALENCE.get(symbol, 6))

func current_valence(atom, bonds: Array) -> int:
	var count = 0
	for bond in bonds:
		if not is_instance_valid(bond):
			continue
		if bond.atom_a == atom or bond.atom_b == atom:
			count += 1
	return count

func can_add_bond(atom, bonds: Array) -> bool:
	return current_valence(atom, bonds) < max_valence(atom.element_symbol)

func valence_status(atom, bonds: Array) -> Dictionary:
	var current = current_valence(atom, bonds)
	var max_v = max_valence(atom.element_symbol)
	return {
		"current": current,
		"max": max_v,
		"remaining": max_v - current,
		"full": current >= max_v
	}

func ideal_bond_angle(n_neighbors: int) -> float:
	return float(VSEPR_ANGLES.get(n_neighbors, 0.0))

func validate_bond_angles(atom, bonds: Array) -> Array:
	var neighbors = []
	for bond in bonds:
		if not is_instance_valid(bond):
			continue
		if bond.atom_a == atom:
			neighbors.append(bond.atom_b)
		elif bond.atom_b == atom:
			neighbors.append(bond.atom_a)
	var issues = []
	if neighbors.size() < 2:
		return issues
	var ideal = ideal_bond_angle(neighbors.size())
	if ideal <= 0.0:
		return issues
	for i in range(neighbors.size()):
		for j in range(i + 1, neighbors.size()):
			var v1 = neighbors[i].global_position - atom.global_position
			var v2 = neighbors[j].global_position - atom.global_position
			if v1.length() < 0.01 or v2.length() < 0.01:
				continue
			var cos_angle = v1.normalized().dot(v2.normalized())
			cos_angle = clamp(cos_angle, -1.0, 1.0)
			var angle_deg = rad_to_deg(acos(cos_angle))
			var dev = abs(angle_deg - ideal)
			if dev > 15.0:
				issues.append({
					"atom_a": neighbors[i].element_symbol,
					"atom_b": neighbors[j].element_symbol,
					"actual_angle": angle_deg,
					"ideal_angle": ideal,
					"deviation": dev
				})
	return issues

func constrain_position(atom, new_pos: Vector3, bonds: Array) -> Vector3:
	var constrained = new_pos
	for bond in bonds:
		if not is_instance_valid(bond):
			continue
		var other = null
		if bond.atom_a == atom:
			other = bond.atom_b
		elif bond.atom_b == atom:
			other = bond.atom_a
		if other == null:
			continue
		var ideal = ideal_bond_length(atom.element_symbol, other.element_symbol)
		var min_len = ideal * BOND_MIN_FACTOR
		var max_len = ideal * BOND_MAX_FACTOR
		var offset = constrained - other.global_position
		var dist = offset.length()
		if dist < 0.001:
			continue
		if dist < min_len:
			constrained = other.global_position + offset.normalized() * min_len
		elif dist > max_len:
			constrained = other.global_position + offset.normalized() * max_len
	return constrained

func get_bond_color(deviation: float) -> Color:
	if deviation <= BOND_TOLERANCE_GOOD:
		return Color(0.2, 0.85, 0.3)
	elif deviation <= BOND_TOLERANCE_WARN:
		return Color(0.9, 0.75, 0.2)
	else:
		return Color(0.9, 0.25, 0.2)

enum LatticeType { AMORPHOUS, SC, BCC, FCC, HCP, DIAMOND }

const LATTICE_NAMES: Array = ["无定形", "简单立方", "体心立方", "面心立方", "六方密堆", "金刚石"]

const TARGET_MIN_POINTS: int = 8
const TARGET_MAX_POINTS: int = 50
const OPTIMAL_POINTS: int = 20

func get_lattice_spacing(symbol: String) -> float:
	var data = ElementDB.get_element(symbol)
	var covalent_r = float(data.get("covalent_radius_pm", 50)) / 100.0
	return covalent_r * 2.0

func gen_lattice_points(lattice_type: int, size: float, spacing: float, center: Vector3) -> Array:
	var pts: Array = []
	match lattice_type:
		LatticeType.SC:
			pts = _gen_sc_lattice(size, spacing, center)
		LatticeType.BCC:
			pts = _gen_bcc_lattice(size, spacing, center)
		LatticeType.FCC:
			pts = _gen_fcc_lattice(size, spacing, center)
		LatticeType.HCP:
			pts = _gen_hcp_lattice(size, spacing, center)
		LatticeType.DIAMOND:
			pts = _gen_diamond_lattice(size, spacing, center)
		_:
			pts = _gen_amorphous_lattice(size, spacing, center)
	return optimize_point_count(pts)

func _gen_sc_lattice(size: float, spacing: float, center: Vector3) -> Array:
	var pts: Array = []
	var n = max(int(size / spacing), 1)
	for i in range(-n, n + 1):
		for j in range(-n, n + 1):
			for k in range(-n, n + 1):
				var p = Vector3(i, j, k) * spacing
				if p.length() <= size:
					pts.append(center + p)
	return pts

func _gen_bcc_lattice(size: float, spacing: float, center: Vector3) -> Array:
	var pts: Array = []
	var n = max(int(size / spacing), 1)
	for i in range(-n, n + 1):
		for j in range(-n, n + 1):
			for k in range(-n, n + 1):
				var p1 = Vector3(i, j, k) * spacing
				if p1.length() <= size:
					pts.append(center + p1)
				var p2 = Vector3(i + 0.5, j + 0.5, k + 0.5) * spacing
				if p2.length() <= size:
					pts.append(center + p2)
	return pts

func _gen_fcc_lattice(size: float, spacing: float, center: Vector3) -> Array:
	var pts: Array = []
	var n = max(int(size / spacing), 1)
	for i in range(-n, n + 1):
		for j in range(-n, n + 1):
			for k in range(-n, n + 1):
				for offset in [[0.0, 0.0, 0.0], [0.5, 0.5, 0.0], [0.5, 0.0, 0.5], [0.0, 0.5, 0.5]]:
					var p = Vector3(i + offset[0], j + offset[1], k + offset[2]) * spacing
					if p.length() <= size:
						pts.append(center + p)
	return pts

func _gen_hcp_lattice(size: float, spacing: float, center: Vector3) -> Array:
	var pts: Array = []
	var n = max(int(size / spacing), 1)
	var h = spacing * sqrt(2.0 / 3.0)
	var s32 = spacing * sqrt(3.0) / 2.0
	for layer in range(-n, n + 1):
		var z = layer * h
		var x_off = spacing * 0.5 if layer % 2 != 0 else 0.0
		var y_off = s32 / 3.0 if layer % 2 != 0 else 0.0
		for i in range(-n, n + 1):
			for j in range(-n, n + 1):
				var x = i * spacing + (spacing * 0.5 if j % 2 != 0 else 0.0) + x_off
				var y = j * s32 + y_off
				var p = Vector3(x, y, z)
				if p.length() <= size:
					pts.append(center + p)
	return pts

func _gen_diamond_lattice(size: float, spacing: float, center: Vector3) -> Array:
	var pts: Array = []
	var n = max(int(size / spacing), 1)
	var _q = spacing * 0.25
	for i in range(-n, n + 1):
		for j in range(-n, n + 1):
			for k in range(-n, n + 1):
				for offset in [[0.0, 0.0, 0.0], [0.5, 0.5, 0.0], [0.5, 0.0, 0.5], [0.0, 0.5, 0.5]]:
					for sub in [[0.0, 0.0, 0.0], [0.25, 0.25, 0.25]]:
						var p = Vector3(i + offset[0] + sub[0], j + offset[1] + sub[1], k + offset[2] + sub[2]) * spacing
						if p.length() <= size:
							pts.append(center + p)
	return pts

func _gen_amorphous_lattice(size: float, spacing: float, center: Vector3) -> Array:
	var pts: Array = []
	var vol = 4.0 * PI * pow(size, 3.0) / 3.0
	var n_target = max(int(vol / pow(spacing, 3.0)), TARGET_MIN_POINTS)
	n_target = min(n_target, TARGET_MAX_POINTS * 2)
	var attempts = 0
	var max_attempts = n_target * 20
	while pts.size() < n_target and attempts < max_attempts:
		attempts += 1
		var r = size * pow(randf(), 1.0 / 3.0)
		var theta = randf() * TAU
		var phi = acos(2.0 * randf() - 1.0)
		var p = center + Vector3(r * sin(phi) * cos(theta), r * sin(phi) * sin(theta), r * cos(phi))
		var ok = true
		for existing in pts:
			if p.distance_to(existing) < spacing * 0.8:
				ok = false
				break
		if ok:
			pts.append(p)
	return pts

func optimize_point_count(pts: Array) -> Array:
	if pts.size() <= TARGET_MAX_POINTS:
		if pts.size() < TARGET_MIN_POINTS:
			return pts
		return pts
	var step = float(pts.size()) / OPTIMAL_POINTS
	var result: Array = []
	for i in range(OPTIMAL_POINTS):
		var idx = int(i * step)
		if idx < pts.size():
			result.append(pts[idx])
	return result

func count_tetrahedra(pts: Array, bond_dist: float) -> int:
	var n = pts.size()
	if n < 4:
		return 0
	var count = 0
	for a in range(n):
		for b in range(a + 1, n):
			if pts[a].distance_to(pts[b]) > bond_dist:
				continue
			for c in range(b + 1, n):
				if pts[a].distance_to(pts[c]) > bond_dist or pts[b].distance_to(pts[c]) > bond_dist:
					continue
				for d in range(c + 1, n):
					if pts[a].distance_to(pts[d]) <= bond_dist and pts[b].distance_to(pts[d]) <= bond_dist and pts[c].distance_to(pts[d]) <= bond_dist:
						count += 1
	return count

func evaluate_distribution(pts: Array, bond_dist: float) -> Dictionary:
	var n = pts.size()
	if n == 0:
		return {"score": 0.0, "reason": "无点"}
	var coord_sum = 0
	for i in range(n):
		var c = 0
		for j in range(n):
			if i != j and pts[i].distance_to(pts[j]) <= bond_dist:
				c += 1
		coord_sum += c
	var avg_coord = float(coord_sum) / n
	var tet = count_tetrahedra(pts, bond_dist)
	var score = 0.0
	if avg_coord >= 2.0:
		score += 0.3
	if avg_coord >= 4.0:
		score += 0.2
	if tet >= 1:
		score += 0.3
	if n >= TARGET_MIN_POINTS:
		score += 0.2
	return {
		"score": score,
		"avg_coord": avg_coord,
		"tetrahedra": tet,
		"point_count": n
	}