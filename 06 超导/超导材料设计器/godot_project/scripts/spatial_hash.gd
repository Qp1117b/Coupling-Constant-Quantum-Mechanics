extends RefCounted
class_name SpatialHash

# 空间哈希表 - 用于加速原子拾取、邻居查找、碰撞检测
# 将O(N²)降为O(N)平均复杂度

var _cell_size: float = 2.0
var _grid: Dictionary = {}
var _items: Dictionary = {}

func _init(cell_size: float = 2.0):
	_cell_size = cell_size

func clear():
	_grid.clear()
	_items.clear()

func insert(item_id: int, position: Vector3):
	var key = _hash_key(position)
	if not _grid.has(key):
		_grid[key] = []
	_grid[key].append(item_id)
	_items[item_id] = position

func remove(item_id: int):
	if not _items.has(item_id):
		return
	var pos = _items[item_id]
	var key = _hash_key(pos)
	if _grid.has(key):
		_grid[key].erase(item_id)
		if _grid[key].is_empty():
			_grid.erase(key)
	_items.erase(item_id)

func update_position(item_id: int, new_pos: Vector3):
	remove(item_id)
	insert(item_id, new_pos)

func query_radius(position: Vector3, radius: float) -> Array:
	var result: Array = []
	var min_cell = _hash_key(position - Vector3(radius, radius, radius))
	var max_cell = _hash_key(position + Vector3(radius, radius, radius))
	for x in range(min_cell[0], max_cell[0] + 1):
		for y in range(min_cell[1], max_cell[1] + 1):
			for z in range(min_cell[2], max_cell[2] + 1):
				var key = [x, y, z]
				if _grid.has(key):
					for item_id in _grid[key]:
						var item_pos = _items[item_id]
						if item_pos.distance_to(position) <= radius:
							result.append(item_id)
	return result

func query_nearest(position: Vector3, max_radius: float = 10.0) -> int:
	var best_id = -1
	var best_dist = max_radius * max_radius
	var r = _cell_size
	while r <= max_radius:
		var candidates = query_radius(position, r)
		for item_id in candidates:
			var d = _items[item_id].distance_squared_to(position)
			if d < best_dist:
				best_dist = d
				best_id = item_id
		if best_id >= 0:
			return best_id
		r += _cell_size
	return -1

func get_all_positions() -> Dictionary:
	return _items.duplicate()

func size() -> int:
	return _items.size()

func _hash_key(pos: Vector3) -> Array:
	return [int(floor(pos.x / _cell_size)), int(floor(pos.y / _cell_size)), int(floor(pos.z / _cell_size))]


# === 邻居列表 (用于力场计算) ===

class NeighborList:
	var _positions: Array = []
	var _neighbors: Array = []
	var _cutoff: float = 5.0
	var _skin: float = 1.0
	var _last_positions: Array = []
	var _needs_rebuild: bool = true

	func _init(cutoff: float = 5.0, skin: float = 1.0):
		_cutoff = cutoff
		_skin = skin

	func set_positions(positions: Array):
		_positions = positions
		if _last_positions.size() != positions.size():
			_needs_rebuild = true
		else:
			var max_disp = 0.0
			for i in range(positions.size()):
				var disp = positions[i].distance_to(_last_positions[i])
				if disp > max_disp:
					max_disp = disp
			if max_disp > _skin * 0.5:
				_needs_rebuild = true

	func build():
		_needs_rebuild = false
		_last_positions = _positions.duplicate()
		_neighbors.clear()
		_neighbors.resize(_positions.size())
		for i in range(_positions.size()):
			_neighbors[i] = []
		var grid = SpatialHash.new(_cutoff + _skin)
		for i in range(_positions.size()):
			grid.insert(i, _positions[i])
		for i in range(_positions.size()):
			var nearby = grid.query_radius(_positions[i], _cutoff + _skin)
			for j in nearby:
				if j <= i:
					continue
				var dist = _positions[i].distance_to(_positions[j])
				if dist <= _cutoff + _skin:
					_neighbors[i].append({"index": j, "distance": dist})
					_neighbors[j].append({"index": i, "distance": dist})

	func get_neighbors(i: int) -> Array:
		if _needs_rebuild:
			build()
		if i < 0 or i >= _neighbors.size():
			return []
		return _neighbors[i]

	func needs_rebuild() -> bool:
		return _needs_rebuild

	func get_cutoff() -> float:
		return _cutoff

# === 矩阵降维 (PCA) ===

static func pca_reduce(matrix: Array, target_dim: int) -> Dictionary:
	var n = matrix.size()
	if n <= target_dim:
		return {"matrix": matrix, "size": n, "reduced": false}
	var mean = _compute_mean(matrix)
	var centered = _center_matrix(matrix, mean)
	var cov = _covariance(centered)
	var eigenvalues = _jacobi_eigenvalues(cov, cov.size())
	eigenvalues.sort()
	eigenvalues.reverse()
	var top_indices = range(min(target_dim, eigenvalues.size()))
	var reduced: Array = []
	for i in top_indices:
		reduced.append(eigenvalues[i])
	return {"matrix": reduced, "size": reduced.size(), "reduced": true, "original_size": n}

static func _compute_mean(matrix: Array) -> Array:
	var n = matrix.size()
	var dim = matrix[0].size() if n > 0 else 0
	var mean: Array = []
	mean.resize(dim)
	mean.fill(0.0)
	for row in matrix:
		for j in range(dim):
			mean[j] += row[j]
	for j in range(dim):
		mean[j] /= n
	return mean

static func _center_matrix(matrix: Array, mean: Array) -> Array:
	var result: Array = []
	for row in matrix:
		var centered = row.duplicate()
		for j in range(row.size()):
			centered[j] -= mean[j]
		result.append(centered)
	return result

static func _covariance(centered: Array) -> Array:
	var n = centered.size()
	var dim = centered[0].size() if n > 0 else 0
	var cov: Array = []
	for i in range(dim):
		var row: Array = []
		row.resize(dim)
		row.fill(0.0)
		cov.append(row)
	for vec in centered:
		for i in range(dim):
			for j in range(dim):
				cov[i][j] += vec[i] * vec[j]
	for i in range(dim):
		for j in range(dim):
			cov[i][j] /= n
	return cov

static func _jacobi_eigenvalues(mat: Array, dim: int, max_iter: int = 100) -> Array:
	var a: Array = []
	for row in mat:
		a.append(row.duplicate())
	for _iter in range(max_iter):
		var p = 0
		var q = 1
		var max_val = 0.0
		for i in range(dim):
			for j in range(i + 1, dim):
				var val = abs(a[i][j])
				if val > max_val:
					max_val = val
					p = i
					q = j
		if max_val < 1e-10:
			break
		var app = a[p][p]
		var aqq = a[q][q]
		var apq = a[p][q]
		var theta = 0.5 * atan2(2.0 * apq, app - aqq)
		var c = cos(theta)
		var s = sin(theta)
		for i in range(dim):
			var aip = a[i][p]
			var aiq = a[i][q]
			a[i][p] = c * aip + s * aiq
			a[i][q] = -s * aip + c * aiq
		for j in range(dim):
			var apj = a[p][j]
			var aqj = a[q][j]
			a[p][j] = c * apj + s * aqj
			a[q][j] = -s * apj + c * aqj
	var eigenvals: Array = []
	for i in range(dim):
		eigenvals.append(a[i][i])
	return eigenvals