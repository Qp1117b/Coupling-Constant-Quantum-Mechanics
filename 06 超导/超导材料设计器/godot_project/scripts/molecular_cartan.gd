extends RefCounted
class_name MolecularCartan

const A4_CARTAN: Array = [
	[2.0, -1.0, 0.0, 0.0],
	[-1.0, 2.0, -1.0, 0.0],
	[0.0, -1.0, 2.0, -1.0],
	[0.0, 0.0, -1.0, 2.0],
]

static func compute_molecular_cartan(atoms: Array, bonds: Array) -> Dictionary:
	var n = atoms.size()
	if n == 0:
		return _empty_result()

	var dim = 4 * n
	var matrix: Array = []
	for i in range(dim):
		var row: Array = []
		for j in range(dim):
			row.append(0.0)
		matrix.append(row)

	for a in range(n):
		var atom = atoms[a]
		var defect = float(atom.get("neutron_defect", 0.0))
		var scale = 1.0 + abs(defect) * 0.1
		for i in range(4):
			for j in range(4):
				matrix[a * 4 + i][a * 4 + j] = A4_CARTAN[i][j] * scale

	for bond in bonds:
		var a = bond.get("a", 0)
		var b = bond.get("b", 0)
		var order = bond.get("order", 1)
		var length = float(bond.get("length", 1.0))
		var r_a = float(bond.get("r_a", 0.5))
		var r_b = float(bond.get("r_b", 0.5))
		var r0 = r_a + r_b
		var beta = float(order) * exp(-1.5 * abs(length - r0))
		var coupling = -beta

		for i2 in range(4):
			matrix[a * 4 + i2][b * 4 + i2] = coupling
			matrix[b * 4 + i2][a * 4 + i2] = coupling

	var eigenvalues = _jacobi_eigenvalues(matrix, dim)
	eigenvalues.sort()

	var spectral_gap = _compute_spectral_gap(eigenvalues)
	var trace = 0.0
	var det = 1.0
	for ev in eigenvalues:
		trace += ev
		det *= ev

	return {
		"eigenvalues": eigenvalues,
		"spectral_gap": spectral_gap,
		"trace": trace,
		"determinant": det,
		"dimension": dim,
		"atom_count": n,
		"bond_count": bonds.size(),
	}

static func _jacobi_eigenvalues(matrix: Array, dim: int) -> Array:
	var a: Array = []
	for i in range(dim):
		var row: Array = []
		for j in range(dim):
			row.append(matrix[i][j])
		a.append(row)

	var max_iter = 100 * dim * dim
	var tol = 1e-10

	for _iter in range(max_iter):
		var p = 0
		var q = 1
		var max_val = 0.0
		for i in range(dim):
			for j in range(i + 1, dim):
				if abs(a[i][j]) > max_val:
					max_val = abs(a[i][j])
					p = i
					q = j

		if max_val < tol:
			break

		var app = a[p][p]
		var aqq = a[q][q]
		var apq = a[p][q]
		var theta = 0.0
		if abs(app - aqq) < 1e-15:
			theta = PI / 4.0
		else:
			theta = 0.5 * atan2(2.0 * apq, app - aqq)
		var c = cos(theta)
		var s = sin(theta)

		for i1 in range(dim):
			var aip = a[i1][p]
			var aiq = a[i1][q]
			a[i1][p] = c * aip + s * aiq
			a[i1][q] = -s * aip + c * aiq
		for i1 in range(dim):
			var api = a[p][i1]
			var aqi = a[q][i1]
			a[p][i1] = c * api + s * aqi
			a[q][i1] = -s * api + c * aqi

	var eigenvalues: Array = []
	for i in range(dim):
		eigenvalues.append(a[i][i])
	return eigenvalues

static func _compute_spectral_gap(eigenvalues: Array) -> float:
	if eigenvalues.size() < 2:
		return 0.0
	var min_gap = abs(eigenvalues[1] - eigenvalues[0])
	for i in range(1, eigenvalues.size() - 1):
		var gap = abs(eigenvalues[i + 1] - eigenvalues[i])
		if gap < min_gap:
			min_gap = gap
	return min_gap

static func _empty_result() -> Dictionary:
	return {
		"eigenvalues": [],
		"spectral_gap": 0.0,
		"trace": 0.0,
		"determinant": 0.0,
		"dimension": 0,
		"atom_count": 0,
		"bond_count": 0,
	}
