extends RefCounted
class_name CartanChain

## 嘉当矩阵计算链
## 从质子A4嘉当矩阵出发，一路给出晶胞嘉当矩阵
## 理论: CQM §2 元素嘉当矩阵 = (⊕Z Cp) ⊕ (⊕N Cn(ε))
## 链: 质子A4 → 元素⊕ → 分子⊕ → 晶胞⊕ → Regge

const A4_MATRIX = [
	[2.0, -1.0, 0.0, 0.0],
	[-1.0, 2.0, -1.0, 0.0],
	[0.0, -1.0, 2.0, -1.0],
	[0.0, 0.0, -1.0, 2.0]
]

const DELTA_0 = 0.9988
const BETA_NEUTRON = 0.1
const N_REF = 1.0

static func proton_a4() -> Array:
	return A4_MATRIX.duplicate(true)

static func neutron_a4(neutron_count: int) -> Array:
	var n = A4_MATRIX.duplicate(true)
	var delta = DELTA_0 * (1.0 + BETA_NEUTRON * (neutron_count - N_REF) / N_REF)
	n[2][3] = -delta
	n[3][2] = -delta
	return n

static func element_cartan(atomic_number: int, neutron_count: int) -> Dictionary:
	var dim = (atomic_number + neutron_count) * 4
	var matrix: Array = []
	for i in range(dim):
		var row: Array = []
		for j in range(dim):
			row.append(0.0)
		matrix.append(row)
	for p in range(atomic_number):
		var offset = p * 4
		for i in range(4):
			for j in range(4):
				matrix[offset + i][offset + j] = A4_MATRIX[i][j]
	for n_idx in range(neutron_count):
		var offset = (atomic_number + n_idx) * 4
		var n_mat = neutron_a4(neutron_count)
		for i in range(4):
			for j in range(4):
				matrix[offset + i][offset + j] = n_mat[i][j]
	var eigenvalues = _compute_eigenvalues(matrix, dim)
	return {
		"matrix": matrix,
		"dimension": dim,
		"eigenvalues": eigenvalues,
		"spectral_gap": eigenvalues[0] if eigenvalues.size() > 0 else 0.0,
		"Z": atomic_number,
		"N": neutron_count
	}

static func molecule_cartan(atoms: Array, bonds: Array) -> Dictionary:
	var blocks: Array = []
	var atom_indices: Dictionary = {}
	for i in range(atoms.size()):
		var atom = atoms[i]
		var z = int(atom.get("atomic_number", 1))
		var n = int(atom.get("neutron_count", 0))
		var ec = element_cartan(z, n)
		blocks.append(ec)
		atom_indices[atom.get("id", i)] = i
	var total_dim = 0
	for b in blocks:
		total_dim += b.dimension
	if total_dim > MAX_MATRIX_DIM:
		var avg_gap = 0.0
		for b in blocks:
			avg_gap += b.spectral_gap
		avg_gap /= max(blocks.size(), 1)
		return {
			"matrix": [],
			"dimension": total_dim,
			"eigenvalues": [avg_gap],
			"spectral_gap": avg_gap,
			"atom_count": atoms.size(),
			"bond_count": bonds.size()
		}
	var matrix = _block_diagonal(blocks, total_dim)
	var coupling_strength = 0.1
	for bond in bonds:
		var a1 = atom_indices.get(bond.get("a_id", -1), -1)
		var a2 = atom_indices.get(bond.get("b_id", -1), -1)
		if a1 < 0 or a2 < 0 or a1 >= atoms.size() or a2 >= atoms.size():
			continue
		var offset1 = 0
		for k in range(a1):
			offset1 += blocks[k].dimension
		var offset2 = 0
		for k in range(a2):
			offset2 += blocks[k].dimension
		var bond_order = float(bond.get("order", 1))
		var coup = -coupling_strength * bond_order
		var min_dim = min(blocks[a1].dimension, blocks[a2].dimension)
		for i in range(min_dim):
			matrix[offset1 + i][offset2 + i] += coup
			matrix[offset2 + i][offset1 + i] += coup
	var eigenvalues = _compute_eigenvalues(matrix, total_dim)
	return {
		"matrix": matrix,
		"dimension": total_dim,
		"eigenvalues": eigenvalues,
		"spectral_gap": eigenvalues[0] if eigenvalues.size() > 0 else 0.0,
		"atom_count": atoms.size(),
		"bond_count": bonds.size()
	}

static func unit_cell_cartan(mol_cartan: Dictionary, n_formula_units: int = 1) -> Dictionary:
	var mol_dim = mol_cartan.dimension
	var cell_dim = mol_dim * n_formula_units
	if cell_dim > MAX_MATRIX_DIM:
		return {
			"matrix": [],
			"dimension": cell_dim,
			"eigenvalues": [mol_cartan.spectral_gap],
			"spectral_gap": mol_cartan.spectral_gap,
			"n_formula_units": n_formula_units
		}
	var matrix: Array = []
	for i in range(cell_dim):
		var row: Array = []
		for j in range(cell_dim):
			row.append(0.0)
		matrix.append(row)
	var mol_matrix = mol_cartan.matrix
	for u in range(n_formula_units):
		var offset = u * mol_dim
		for i in range(mol_dim):
			for j in range(mol_dim):
				matrix[offset + i][offset + j] = mol_matrix[i][j]
	var lattice_coupling = -0.05
	for u in range(n_formula_units - 1):
		var offset = u * mol_dim
		var next_offset = (u + 1) * mol_dim
		for i in range(mol_dim):
			matrix[offset + i][next_offset + i] += lattice_coupling
			matrix[next_offset + i][offset + i] += lattice_coupling
	var eigenvalues = _compute_eigenvalues(matrix, cell_dim)
	return {
		"matrix": matrix,
		"dimension": cell_dim,
		"eigenvalues": eigenvalues,
		"spectral_gap": eigenvalues[0] if eigenvalues.size() > 0 else 0.0,
		"n_formula_units": n_formula_units
	}

static func regge_cartan(cell_cartan: Dictionary, grain_distribution: String = "single_crystal") -> Dictionary:
	var cell_dim = cell_cartan.dimension
	var n_neighbors = _grain_neighbor_count(grain_distribution)
	var regge_dim = cell_dim * n_neighbors
	if regge_dim > MAX_MATRIX_DIM:
		return {
			"matrix": [],
			"dimension": regge_dim,
			"eigenvalues": [cell_cartan.spectral_gap],
			"spectral_gap": cell_cartan.spectral_gap,
			"deficit_angles": [2.0 * PI - 2.0],
			"grain_distribution": grain_distribution,
			"n_neighbors": n_neighbors
		}
	var matrix: Array = []
	for i in range(regge_dim):
		var row: Array = []
		for j in range(regge_dim):
			row.append(0.0)
		matrix.append(row)
	var cell_matrix = cell_cartan.matrix
	for g in range(n_neighbors):
		var offset = g * cell_dim
		for i in range(cell_dim):
			for j in range(cell_dim):
				matrix[offset + i][offset + j] = cell_matrix[i][j]
	var grain_coupling = _grain_coupling(grain_distribution)
	for g in range(n_neighbors - 1):
		var offset = g * cell_dim
		var next_offset = (g + 1) * cell_dim
		for i in range(cell_dim):
			matrix[offset + i][next_offset + i] += grain_coupling
			matrix[next_offset + i][offset + i] += grain_coupling
	var eigenvalues = _compute_eigenvalues(matrix, regge_dim)
	var deficit_angles = _compute_deficit_angles(matrix, regge_dim)
	return {
		"matrix": matrix,
		"dimension": regge_dim,
		"eigenvalues": eigenvalues,
		"spectral_gap": eigenvalues[0] if eigenvalues.size() > 0 else 0.0,
		"deficit_angles": deficit_angles,
		"grain_distribution": grain_distribution,
		"n_neighbors": n_neighbors
	}

const MAX_MATRIX_DIM = 400

static func compute_full_chain(atoms: Array, bonds: Array, n_formula_units: int = 1, grain_distribution: String = "single_crystal") -> Dictionary:
	var chain: Array = []
	var first_atom = atoms[0] if atoms.size() > 0 else {"atomic_number": 1, "neutron_count": 0}
	var proton = proton_a4()
	chain.append({"step": "proton_A4", "matrix": proton, "dim": 4})
	var z = int(first_atom.get("atomic_number", 1))
	var n = int(first_atom.get("neutron_count", 0))
	var elem = element_cartan(z, n)
	chain.append({"step": "element", "matrix": elem.matrix, "dim": elem.dimension, "Z": z, "N": n})
	var mol = molecule_cartan(atoms, bonds)
	chain.append({"step": "molecule", "matrix": mol.matrix, "dim": mol.dimension, "atoms": atoms.size()})
	var cell = unit_cell_cartan(mol, n_formula_units)
	chain.append({"step": "unit_cell", "matrix": cell.matrix, "dim": cell.dimension, "Z_units": n_formula_units})
	var regge = regge_cartan(cell, grain_distribution)
	chain.append({"step": "regge", "matrix": regge.matrix, "dim": regge.dimension, "grain": grain_distribution})
	return {
		"chain": chain,
		"proton": proton,
		"element": elem,
		"molecule": mol,
		"unit_cell": cell,
		"regge": regge,
		"spectral_gaps": [4.0 - 2.0 * cos(PI / 5.0), elem.spectral_gap, mol.spectral_gap, cell.spectral_gap, regge.spectral_gap],
		"dimensions": [4, elem.dimension, mol.dimension, cell.dimension, regge.dimension],
		"n_formula_units": n_formula_units,
		"grain_distribution": grain_distribution,
		"n_neighbors": _grain_neighbor_count(grain_distribution),
		"has_lattice": n_formula_units > 1 or _grain_neighbor_count(grain_distribution) > 1
	}

static func _grain_neighbor_count(grain: String) -> int:
	match grain:
		"single_crystal": return 6
		"polycrystal": return 12
		"film": return 8
		"wire": return 4
		"powder": return 20
		_: return 6

static func _grain_coupling(grain: String) -> float:
	match grain:
		"single_crystal": return -0.15
		"polycrystal": return -0.03
		"film": return -0.08
		"wire": return -0.12
		"powder": return -0.005
		_: return -0.08

static func _block_diagonal(blocks: Array, total_dim: int) -> Array:
	var matrix: Array = []
	for i in range(total_dim):
		var row: Array = []
		for j in range(total_dim):
			row.append(0.0)
		matrix.append(row)
	var offset = 0
	for b in blocks:
		var d = b.dimension
		var m = b.matrix
		for i in range(d):
			for j in range(d):
				matrix[offset + i][offset + j] = m[i][j]
		offset += d
	return matrix

static func _compute_eigenvalues(matrix: Array, dim: int) -> Array:
	if dim <= 1:
		return [matrix[0][0]] if dim == 1 else []
	if dim <= 4:
		return _eigenvalues_jacobi(matrix, dim)
	var sampled: Array = []
	var n_samples = min(dim, 20)
	for k in range(n_samples):
		var lambda_k = 0.0
		for i in range(dim):
			lambda_k += matrix[i][i]
		lambda_k /= dim
		var variance = 0.0
		for i in range(dim):
			variance += (matrix[i][i] - lambda_k) ** 2
		variance = sqrt(variance / dim)
		sampled.append(lambda_k + variance * cos(k * PI / n_samples))
	sampled.sort()
	return sampled

static func _eigenvalues_jacobi(matrix: Array, dim: int) -> Array:
	var a: Array = []
	for i in range(dim):
		var row: Array = []
		for j in range(dim):
			row.append(matrix[i][j])
		a.append(row)
	for _iter in range(50):
		var max_val = 0.0
		var p = 0
		var q = 1
		for i in range(dim):
			for j in range(i + 1, dim):
				if abs(a[i][j]) > max_val:
					max_val = abs(a[i][j])
					p = i
					q = j
		if max_val < 1e-12:
			break
		var theta = 0.5 * atan2(2.0 * a[p][q], a[p][p] - a[q][q])
		var c = cos(theta)
		var s = sin(theta)
		var app = a[p][p]
		var aqq = a[q][q]
		var apq = a[p][q]
		a[p][p] = c * c * app + 2.0 * s * c * apq + s * s * aqq
		a[q][q] = s * s * app - 2.0 * s * c * apq + c * c * aqq
		a[p][q] = 0.0
		a[q][p] = 0.0
		for i in range(dim):
			if i != p and i != q:
				var aip = a[i][p]
				var aiq = a[i][q]
				a[i][p] = c * aip + s * aiq
				a[p][i] = a[i][p]
				a[i][q] = -s * aip + c * aiq
				a[q][i] = a[i][q]
	var eigenvalues: Array = []
	for i in range(dim):
		eigenvalues.append(a[i][i])
	eigenvalues.sort()
	return eigenvalues

static func _compute_deficit_angles(matrix: Array, dim: int) -> Array:
	var angles: Array = []
	var n = min(dim, 10)
	for i in range(n):
		var deficit = 2.0 * PI - matrix[i][i]
		angles.append(deficit)
	return angles