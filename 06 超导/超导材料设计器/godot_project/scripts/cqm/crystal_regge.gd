extends RefCounted
class_name CrystalRegge

## 晶胞作为Regge单元的离散Regge曲率作用量
## 理论: 晶胞等效为Regge单元，构造离散Regge曲率作用量
## S_Regge = Σ_h ε_h · A_h  (h为hinge/边, ε_h=亏角, A_h=对偶面积)
## 压强-Regge曲率作用量是三条链中链A的"生成"作用量

static func compute_discrete_curvature(cell_positions: Array, cell_adjacency: Array, pressure: float = 0.0) -> Dictionary:
	var n = cell_positions.size()
	if n < 4:
		return {"regge_action": 0.0, "mean_curvature": 0.0, "total_deficit": 0.0, "tetrahedra": [], "pressure_term": 0.0}
	var tetrahedra = _find_tetrahedra(cell_positions)
	var edge_deficits = _compute_edge_deficits(cell_positions, tetrahedra)
	var dual_areas = _compute_dual_areas(cell_positions, tetrahedra)
	var regge_action = 0.0
	var total_deficit = 0.0
	for h in range(edge_deficits.size()):
		var deficit = edge_deficits[h]
		var area = dual_areas[h] if h < dual_areas.size() else 0.0
		regge_action += deficit * area
		total_deficit += deficit
	var pressure_term = pressure * _compute_volume(cell_positions)
	regge_action += pressure_term
	var mean_curvature = total_deficit / max(n, 1)
	var max_deficit = 0.0
	for d in edge_deficits:
		if abs(d) > abs(max_deficit):
			max_deficit = d
	return {
		"regge_action": regge_action,
		"mean_curvature": mean_curvature,
		"total_deficit": total_deficit,
		"max_deficit": max_deficit,
		"tetrahedra_count": tetrahedra.size(),
		"edge_count": edge_deficits.size(),
		"pressure_term": pressure_term,
		"tetrahedra": tetrahedra,
		"edge_deficits": edge_deficits,
		"dual_areas": dual_areas
	}

static func compute_from_cartan_chain(chain_result: Dictionary, pressure: float = 0.0, atom_positions: Array = []) -> Dictionary:
	var regge_data = chain_result.get("regge", {})
	var deficit_angles: Array = regge_data.get("deficit_angles", [])
	var regge_action = 0.0
	var total_deficit = 0.0
	var source = "cartan_chain"
	if atom_positions.size() >= 4:
		var tetrahedra = _find_tetrahedra(atom_positions)
		if tetrahedra.size() > 0:
			var edge_deficits = _compute_edge_deficits(atom_positions, tetrahedra)
			var dual_areas = _compute_dual_areas(atom_positions, tetrahedra)
			for h in range(edge_deficits.size()):
				var area = dual_areas[h] if h < dual_areas.size() else 0.0
				regge_action += abs(edge_deficits[h]) * area
				total_deficit += abs(edge_deficits[h])
			var pressure_term = pressure * _compute_volume(atom_positions)
			regge_action += pressure_term
			if regge_action > 0:
				source = "geometric"
				return {
					"regge_action": regge_action,
					"total_deficit": total_deficit,
					"mean_curvature": total_deficit / max(float(edge_deficits.size()), 1.0),
					"pressure_term": pressure_term,
					"source": source,
					"tetrahedra_count": tetrahedra.size(),
					"grain_distribution": regge_data.get("grain_distribution", "single_crystal")
				}
	var geom_factor = _compute_geometry_factor(atom_positions)
	for d in deficit_angles:
		var area = geom_factor
		regge_action += d * area
		total_deficit += d
	var pressure_term = pressure * float(regge_data.get("dimension", 1))
	regge_action += pressure_term
	return {
		"regge_action": regge_action,
		"total_deficit": total_deficit,
		"mean_curvature": total_deficit / max(float(deficit_angles.size()), 1.0),
		"pressure_term": pressure_term,
		"source": source,
		"geometry_factor": geom_factor,
		"grain_distribution": regge_data.get("grain_distribution", "single_crystal")
	}

static func _compute_geometry_factor(positions: Array) -> float:
	if positions.size() < 2:
		return 1.0
	var total_dist = 0.0
	var count = 0
	var i = 0
	while i < positions.size():
		var j = i + 1
		while j < positions.size():
			total_dist += positions[i].distance_to(positions[j])
			count += 1
			j += 1
		i += 1
	var mean_dist = total_dist / max(count, 1)
	var spread = 0.0
	i = 0
	while i < positions.size():
		var j = i + 1
		while j < positions.size():
			var d = positions[i].distance_to(positions[j])
			spread += (d - mean_dist) ** 2
			j += 1
		i += 1
	spread = sqrt(spread / max(count, 1))
	return 1.0 + mean_dist * 0.5 + spread * 0.3

static func _generate_lattice_positions(atom_positions: Array, n_units: int) -> Array:
	var positions: Array = []
	var lattice_vectors = [Vector3(2.0, 0, 0), Vector3(0, 2.0, 0), Vector3(0, 0, 2.0)]
	for ux in range(-n_units + 1, n_units):
		for uy in range(-n_units + 1, n_units):
			for uz in range(-n_units + 1, n_units):
				var offset = lattice_vectors[0] * ux + lattice_vectors[1] * uy + lattice_vectors[2] * uz
				for p in atom_positions:
					positions.append(p + offset)
	return positions

static func _find_tetrahedra(points: Array) -> Array:
	var n = points.size()
	var tetrahedra: Array = []
	var max_tetra = 100
	for i in range(n):
		for j in range(i + 1, n):
			for k in range(j + 1, n):
				for l in range(k + 1, n):
					var vol = _tetra_volume(points[i], points[j], points[k], points[l])
					if abs(vol) > 1e-8:
						tetrahedra.append([i, j, k, l])
						if tetrahedra.size() >= max_tetra:
							return tetrahedra
	return tetrahedra

static func _compute_edge_deficits(points: Array, tetrahedra: Array) -> Array:
	var edge_map: Dictionary = {}
	for tet in tetrahedra:
		for a in range(4):
			for b in range(a + 1, 4):
				var e = [tet[a], tet[b]]
				var key = str(e[0]) + "_" + str(e[1])
				if not edge_map.has(key):
					edge_map[key] = {"dihedral_sum": 0.0, "count": 0}
				var dihedral = _dihedral_angle(points, tet, a, b)
				edge_map[key].dihedral_sum += dihedral
				edge_map[key].count += 1
	var deficits: Array = []
	for key in edge_map:
		var info = edge_map[key]
		var deficit = 2.0 * PI - info.dihedral_sum
		deficits.append(deficit)
	return deficits

static func _dihedral_angle(points: Array, tet: Array, a: int, b: int) -> float:
	var others: Array = []
	for i in range(4):
		if i != a and i != b:
			others.append(i)
	if others.size() < 2:
		return 0.0
	var p1 = points[tet[a]]
	var p2 = points[tet[b]]
	var p3 = points[tet[others[0]]]
	var p4 = points[tet[others[1]]]
	var edge = p2 - p1
	var n1 = _normal_to_edge(p1, p2, p3)
	var n2 = _normal_to_edge(p1, p2, p4)
	if n1.length() < 1e-10 or n2.length() < 1e-10:
		return 0.0
	n1 = n1.normalized()
	n2 = n2.normalized()
	var cos_angle = n1.dot(n2)
	cos_angle = clampf(cos_angle, -1.0, 1.0)
	return acos(cos_angle)

static func _normal_to_edge(p1: Vector3, p2: Vector3, p3: Vector3) -> Vector3:
	var edge = (p2 - p1).normalized()
	var v = p3 - p1
	return v - edge * v.dot(edge)

static func _compute_dual_areas(points: Array, tetrahedra: Array) -> Array:
	var areas: Array = []
	for i in range(tetrahedra.size()):
		var tet = tetrahedra[i]
		var vol = _tetra_volume(points[tet[0]], points[tet[1]], points[tet[2]], points[tet[3]])
		areas.append(abs(vol) ** (2.0 / 3.0))
	return areas

static func _tetra_volume(a: Vector3, b: Vector3, c: Vector3, d: Vector3) -> float:
	return abs((b - a).dot((c - a).cross(d - a))) / 6.0

static func _compute_volume(points: Array) -> float:
	if points.size() < 4:
		return 0.0
	var center = Vector3.ZERO
	for p in points:
		center += p
	center /= points.size()
	var vol = 0.0
	var n = points.size()
	for i in range(n):
		for j in range(i + 1, n):
			for k in range(j + 1, n):
				vol += _tetra_volume(center, points[i], points[j], points[k])
	return vol