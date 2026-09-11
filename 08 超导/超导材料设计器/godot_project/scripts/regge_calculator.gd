extends RefCounted
class_name ReggeCalculator

## Regge 微积分计算引擎 (3D 空间剖分)
## 亏角: ε_l = 2π − Σ_{围绕边 l 的四面体} θ_二面角
## Regge 作用量: Σ_l ε_l · l_l
## 输出 hinge 数据 (边亏角/长度) 供链A几何计算与 G16 桥接使用

static func compute_regge_3d(atom_positions: Array, bond_pairs: Array, scale: int = 1) -> Dictionary:
	var scale_factor = float(scale)
	var scale_name = "%dx" % scale

	if atom_positions.size() < 4:
		return _empty_result(scale_name, scale_factor, bond_pairs.size())

	var adj = _build_adjacency(atom_positions.size(), bond_pairs)
	var tetrahedra = _find_tetrahedra(atom_positions, adj)

	if tetrahedra.is_empty():
		return _empty_result(scale_name, scale_factor, bond_pairs.size())

	var edge_tetra_map: Dictionary = {}
	for tet in tetrahedra:
		for edge in tet["edges"]:
			var key = "%d_%d" % [edge[0], edge[1]]
			if not edge_tetra_map.has(key):
				edge_tetra_map[key] = {"a": edge[0], "b": edge[1], "tets": []}
			edge_tetra_map[key]["tets"].append(tet)

	var regge_action: float = 0.0
	var total_deficit: float = 0.0
	var max_deficit: float = 0.0
	var edges_with_deficit: int = 0
	var total_dihedral: float = 0.0
	var dihedral_count: int = 0
	var hinges: Array = []

	for edge_key in edge_tetra_map.keys():
		var edge_info = edge_tetra_map[edge_key]
		var a_idx = edge_info["a"]
		var b_idx = edge_info["b"]
		var pos_a = atom_positions[a_idx]
		var pos_b = atom_positions[b_idx]
		var edge_length = pos_a.distance_to(pos_b)

		var sum_dihedral: float = 0.0
		for tet in edge_info["tets"]:
			var dihedral = _dihedral_angle(atom_positions, tet, a_idx, b_idx)
			sum_dihedral += dihedral
			total_dihedral += dihedral
			dihedral_count += 1

		var deficit = TAU - sum_dihedral
		if abs(deficit) > 1e-6:
			edges_with_deficit += 1
		total_deficit += deficit
		max_deficit = max(max_deficit, abs(deficit))

		regge_action += edge_length * deficit
		hinges.append({
			"edge": [a_idx, b_idx],
			"key": edge_key,
			"deficit_angle": deficit,
			"length": edge_length,
			"dihedral_sum": sum_dihedral,
			"tet_count": edge_info["tets"].size(),
			"opposite_verts": _opposite_verts(edge_info["tets"], a_idx, b_idx),
		})

	var mean_dihedral = total_dihedral / dihedral_count if dihedral_count > 0 else 0.0

	var tets_out: Array = []
	for tet in tetrahedra:
		var verts = tet["verts"]
		tets_out.append({
			"verts": verts,
			"edges": tet["edges"],
			"volume": tet["volume"],
			"circumradius": _tet_circumradius(atom_positions, verts[0], verts[1], verts[2], verts[3]),
			"hinges": _tet_hinges_for(hinges, tet),
		})

	return {
		"regge_action": regge_action,
		"regge_action_scaled": regge_action * scale_factor,
		"tetrahedra_count": tetrahedra.size(),
		"edge_count": edge_tetra_map.size(),
		"edges_with_deficit": edges_with_deficit,
		"total_deficit": total_deficit,
		"max_deficit": max_deficit,
		"scale_name": scale_name,
		"scale_factor": scale_factor,
		"mean_dihedral": mean_dihedral,
		"hinges": hinges,
		"tetrahedra": tets_out,
	}

static func _tet_hinges_for(hinges: Array, tet: Dictionary) -> Array:
	var result: Array = []
	var vert_set = {}
	for v in tet["verts"]:
		vert_set[v] = true
	for h in hinges:
		var e = h["edge"]
		if vert_set.has(e[0]) and vert_set.has(e[1]):
			result.append(h)
	return result

## 环绕 hinge 的各四面体对面顶点对 (hinge 和乐环路计算用)
static func _opposite_verts(tets: Array, a_idx: int, b_idx: int) -> Array:
	var result: Array = []
	for tet in tets:
		var pair: Array = []
		for v in tet["verts"]:
			if v != a_idx and v != b_idx:
				pair.append(v)
		if pair.size() == 2:
			result.append(pair)
	return result

static func _tet_circumradius(positions: Array, a: int, b: int, c: int, d: int) -> float:
	var pa = positions[a]
	var pb = (positions[b] - pa) as Vector3
	var pc = (positions[c] - pa) as Vector3
	var pd = (positions[d] - pa) as Vector3

	var m: Array = []
	m.append([pb.x, pb.y, pb.z])
	m.append([pc.x, pc.y, pc.z])
	m.append([pd.x, pd.y, pd.z])

	var rhs: Array = [
		pb.length_squared() / 2.0,
		pc.length_squared() / 2.0,
		pd.length_squared() / 2.0,
	]

	var det = _det3(m)
	if abs(det) < 1e-12:
		return 0.0

	var m_x = _replace_col(m, 0, rhs)
	var m_y = _replace_col(m, 1, rhs)
	var m_z = _replace_col(m, 2, rhs)
	var x = _det3(m_x) / det
	var y = _det3(m_y) / det
	var z = _det3(m_z) / det
	return sqrt(x * x + y * y + z * z)

static func _replace_col(m: Array, col: int, vals: Array) -> Array:
	var out: Array = []
	for r in range(3):
		var row = [m[r][0], m[r][1], m[r][2]]
		row[col] = vals[r]
		out.append(row)
	return out

static func _det3(m: Array) -> float:
	return m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) \
		- m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) \
		+ m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])

static func _build_adjacency(n: int, bond_pairs: Array) -> Dictionary:
	var adj: Dictionary = {}
	for i in range(n):
		adj[i] = []
	for pair in bond_pairs:
		var a = pair[0]
		var b = pair[1]
		if a >= 0 and a < n and b >= 0 and b < n:
			adj[a].append(b)
			adj[b].append(a)
	return adj

static func _find_tetrahedra(positions: Array, adj: Dictionary) -> Array:
	var tetrahedra: Array = []
	var seen: Dictionary = {}

	var n = positions.size()
	for a in range(n):
		var neighbors_a = adj.get(a, [])
		for b in neighbors_a:
			if b <= a:
				continue
			var common_ab = _common_neighbors(adj, a, b)
			for i in range(common_ab.size()):
				var c = common_ab[i]
				if c <= b:
					continue
				for j in range(i + 1, common_ab.size()):
					var d = common_ab[j]
					if d <= c:
						continue
					if not _are_bonded(adj, c, d):
						continue
					var key = "%d_%d_%d_%d" % [a, b, c, d]
					if seen.has(key):
						continue
					seen[key] = true
					var vol = _tet_volume(positions, a, b, c, d)
					if abs(vol) < 1e-8:
						continue
					var edges = [
						[a, b], [a, c], [a, d],
						[b, c], [b, d], [c, d]
					]
					tetrahedra.append({
						"verts": [a, b, c, d],
						"edges": edges,
						"volume": vol,
					})
	return tetrahedra

static func _common_neighbors(adj: Dictionary, a: int, b: int) -> Array:
	var neighbors_a = adj.get(a, [])
	var neighbors_b = adj.get(b, [])
	var set_b: Dictionary = {}
	for x in neighbors_b:
		set_b[x] = true
	var result: Array = []
	for x in neighbors_a:
		if x != b and set_b.has(x):
			result.append(x)
	return result

static func _are_bonded(adj: Dictionary, a: int, b: int) -> bool:
	for x in adj.get(a, []):
		if x == b:
			return true
	return false

static func _tet_volume(positions: Array, a: int, b: int, c: int, d: int) -> float:
	var ab = positions[b] - positions[a]
	var ac = positions[c] - positions[a]
	var ad = positions[d] - positions[a]
	return ab.dot(ac.cross(ad)) / 6.0

static func _dihedral_angle(atom_positions: Array, tet: Dictionary, a_idx: int, b_idx: int) -> float:
	var verts = tet["verts"]

	var a_local = -1
	var b_local = -1
	var others: Array = []
	for i in range(4):
		if verts[i] == a_idx:
			a_local = i
		elif verts[i] == b_idx:
			b_local = i
		else:
			others.append(i)

	if a_local < 0 or b_local < 0 or others.size() < 2:
		return 0.0

	var pa = atom_positions[verts[a_local]]
	var pb = atom_positions[verts[b_local]]
	var pc = atom_positions[verts[others[0]]]
	var pd = atom_positions[verts[others[1]]]

	var ab = pb - pa
	var ac = pc - pa
	var ad = pd - pa

	var n1 = ab.cross(ac)
	var n2 = ab.cross(ad)

	var len1 = n1.length()
	var len2 = n2.length()
	if len1 < 1e-10 or len2 < 1e-10:
		return 0.0

	var cos_angle = n1.dot(n2) / (len1 * len2)
	cos_angle = clampf(cos_angle, -1.0, 1.0)

	return PI - acos(cos_angle)

static func _empty_result(scale_name: String = "—", scale_factor: float = 1.0, edge_count: int = 0) -> Dictionary:
	return {
		"regge_action": 0.0,
		"regge_action_scaled": 0.0,
		"tetrahedra_count": 0,
		"edge_count": edge_count,
		"edges_with_deficit": 0,
		"total_deficit": 0.0,
		"max_deficit": 0.0,
		"scale_name": scale_name,
		"scale_factor": scale_factor,
		"mean_dihedral": 0.0,
	}
