extends RefCounted
class_name ConnectivityLayer

## 第二层：结合方式 (Connectivity / Constitution)
## 原子之间的连接拓扑 — 谁与谁成键、键的类型、环系结构、官能团排布
## 可控性：高度可控 — 有机合成/无机合成的核心战场

signal topology_changed()
signal bond_added(bond_info: Dictionary)
signal bond_removed(bond_info: Dictionary)

var _atoms: Array = []  # List of atom info dicts: {symbol, id, ...}
var _bonds: Array = []  # List of bond info dicts: {a_id, b_id, order, type}

func get_layer_name() -> String:
	return "结合方式"

func get_layer_index() -> int:
	return 2

func get_controllability() -> String:
	return "高度可控"

func get_description() -> String:
	return "原子间连接拓扑。决定化学身份、反应性、基础物性。化学式是原料清单，结合方式是装配图纸。"

func set_from_formula(composition: Dictionary) -> void:
	_atoms.clear()
	_bonds.clear()
	var atom_id = 0
	for sym in composition:
		for i in range(composition[sym]):
			_atoms.append({"id": atom_id, "symbol": sym, "index": i})
			atom_id += 1
	topology_changed.emit()

func add_atom(symbol: String) -> int:
	var atom_id = _atoms.size()
	_atoms.append({"id": atom_id, "symbol": symbol, "index": 0})
	topology_changed.emit()
	return atom_id

func remove_atom(atom_id: int) -> void:
	_atoms = _atoms.filter(func(a): return a.id != atom_id)
	_bonds = _bonds.filter(func(b): return b.a_id != atom_id and b.b_id != atom_id)
	topology_changed.emit()

func add_bond(a_id: int, b_id: int, order: int = 1) -> void:
	if a_id == b_id:
		return
	for b in _bonds:
		if (b.a_id == a_id and b.b_id == b_id) or (b.a_id == b_id and b.b_id == a_id):
			return
	var bond_info = {"a_id": a_id, "b_id": b_id, "order": order, "type": _bond_type_name(order)}
	_bonds.append(bond_info)
	bond_added.emit(bond_info)
	topology_changed.emit()

func remove_bond(a_id: int, b_id: int) -> void:
	for i in range(_bonds.size()):
		var b = _bonds[i]
		if (b.a_id == a_id and b.b_id == b_id) or (b.a_id == b_id and b.b_id == a_id):
			bond_removed.emit(b)
			_bonds.remove_at(i)
			topology_changed.emit()
			return

func get_bond_order(a_id: int, b_id: int) -> int:
	for b in _bonds:
		if (b.a_id == a_id and b.b_id == b_id) or (b.a_id == b_id and b.b_id == a_id):
			return b.order
	return 0

func get_neighbors(atom_id: int) -> Array:
	var result: Array = []
	for b in _bonds:
		if b.a_id == atom_id:
			result.append(b.b_id)
		elif b.b_id == atom_id:
			result.append(b.a_id)
	return result

func get_adjacency_matrix() -> Array:
	var n = _atoms.size()
	var matrix: Array = []
	for i in range(n):
		var row: Array = []
		for j in range(n):
			row.append(0)
		matrix.append(row)
	for b in _bonds:
		matrix[b.a_id][b.b_id] = b.order
		matrix[b.b_id][b.a_id] = b.order
	return matrix

func detect_rings() -> Array:
	var n = _atoms.size()
	if n < 3:
		return []
	var visited: Array = []
	for i in range(n):
		visited.append(false)
	var parent: Array = []
	for i in range(n):
		parent.append(-1)
	var rings: Array = []
	_find_rings_dfs(0, -1, visited, parent, rings)
	return rings

func _find_rings_dfs(u: int, p: int, visited: Array, parent: Array, rings: Array) -> void:
	visited[u] = true
	parent[u] = p
	for v in get_neighbors(u):
		if v == p:
			continue
		if visited[v]:
			var ring = _extract_ring(u, v, parent)
			if ring.size() >= 3:
				rings.append(ring)
		else:
			_find_rings_dfs(v, u, visited, parent, rings)

func _extract_ring(u: int, v: int, parent: Array) -> Array:
	var ring: Array = [u]
	var cur = u
	while cur != v and cur != -1:
		cur = parent[cur]
		ring.append(cur)
	return ring

func detect_functional_groups() -> Array:
	var groups: Array = []
	var n = _atoms.size()
	for i in range(n):
		var sym = _atoms[i].symbol
		var neighbors = get_neighbors(i)
		if sym == "O" and neighbors.size() == 1:
			var order = get_bond_order(i, neighbors[0])
			if order == 2:
				groups.append({"type": "carbonyl", "center": i})
			else:
				var n_sym = _atoms[neighbors[0]].symbol
				if n_sym == "H":
					groups.append({"type": "hydroxyl", "oxygen": i})
		elif sym == "N" and neighbors.size() == 2:
			groups.append({"type": "amine", "nitrogen": i})
	return groups

func get_degree(atom_id: int) -> int:
	return get_neighbors(atom_id).size()

func is_graph_connected() -> bool:
	if _atoms.is_empty():
		return true
	var visited: Array = []
	for i in range(_atoms.size()):
		visited.append(false)
	_dfs_connectivity(0, visited)
	return visited.all(func(v): return v)

func _dfs_connectivity(u: int, visited: Array) -> void:
	visited[u] = true
	for v in get_neighbors(u):
		if not visited[v]:
			_dfs_connectivity(v, visited)

func get_connected_components() -> Array:
	var n = _atoms.size()
	var visited: Array = []
	for i in range(n):
		visited.append(false)
	var components: Array = []
	for i in range(n):
		if not visited[i]:
			var comp: Array = []
			_dfs_component(i, visited, comp)
			components.append(comp)
	return components

func _dfs_component(u: int, visited: Array, comp: Array) -> void:
	visited[u] = true
	comp.append(u)
	for v in get_neighbors(u):
		if not visited[v]:
			_dfs_component(v, visited, comp)

func _bond_type_name(order: int) -> String:
	match order:
		1: return "single"
		2: return "double"
		3: return "triple"
		4: return "aromatic"
		_: return "unknown"

func to_dict() -> Dictionary:
	return {
		"layer": "connectivity",
		"atoms": _atoms.duplicate(true),
		"bonds": _bonds.duplicate(true),
		"rings": detect_rings(),
		"functional_groups": detect_functional_groups(),
	}

func from_dict(data: Dictionary) -> void:
	_atoms = data.get("atoms", []).duplicate(true)
	_bonds = data.get("bonds", []).duplicate(true)
	topology_changed.emit()