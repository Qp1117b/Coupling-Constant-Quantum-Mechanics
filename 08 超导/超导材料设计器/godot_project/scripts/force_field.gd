extends RefCounted
class_name ForceField

const KB = 1.0
const DEFAULT_BOND_K = 100.0
const DEFAULT_ANGLE_K = 50.0
const LJ_EPSILON = 0.01
const LJ_SIGMA = 2.5
## LJ 对势截断因子: r > 3.5σ 处 (1/3.5)^6 ≈ 1.5e-4, 相对贡献可忽略 (标准分子动力学做法)
const LJ_TRUNCATION = 3.5

static func compute_energy(atoms: Array, bonds: Array, angles: Array = []) -> float:
	var e_bond = _bond_energy(atoms, bonds)
	var e_angle = _angle_energy(atoms, angles)
	var e_lj = _lennard_jones_energy(atoms)
	return e_bond + e_angle + e_lj

static func _bond_energy(atoms: Array, bonds: Array) -> float:
	var e = 0.0
	for bond in bonds:
		var a = int(bond.get("a", 0))
		var b = int(bond.get("b", 0))
		if a < 0 or a >= atoms.size() or b < 0 or b >= atoms.size():
			continue
		var pos_a = _get_pos(atoms[a])
		var pos_b = _get_pos(atoms[b])
		var r = pos_a.distance_to(pos_b)
		var r0 = float(bond.get("r0", 1.0))
		var k = float(bond.get("k", DEFAULT_BOND_K))
		e += k * (r - r0) * (r - r0)
	return e

static func _angle_energy(atoms: Array, angles: Array) -> float:
	var e = 0.0
	for angle in angles:
		var i = int(angle.get("i", 0))
		var j = int(angle.get("j", 0))
		var k_idx = int(angle.get("k", 0))
		if i < 0 or i >= atoms.size() or j < 0 or j >= atoms.size() or k_idx < 0 or k_idx >= atoms.size():
			continue
		var vi = _get_pos(atoms[i]) - _get_pos(atoms[j])
		var vk = _get_pos(atoms[k_idx]) - _get_pos(atoms[j])
		if vi.length() < 0.01 or vk.length() < 0.01:
			continue
		var cos_theta = vi.normalized().dot(vk.normalized())
		cos_theta = clamp(cos_theta, -1.0, 1.0)
		var theta = acos(cos_theta)
		var theta0 = float(angle.get("theta0", PI * 109.47 / 180.0))
		var k = float(angle.get("k_angle", DEFAULT_ANGLE_K))
		e += k * (theta - theta0) * (theta - theta0)
	return e

static func _lj_cutoff(atoms: Array) -> float:
	var max_sigma = 0.0
	for a in atoms:
		max_sigma = max(max_sigma, _get_lj_sigma(a))
	return max(max_sigma * LJ_TRUNCATION, LJ_SIGMA * LJ_TRUNCATION)

static func _build_lj_hash(atoms: Array) -> SpatialHash:
	var grid = SpatialHash.new(max(_lj_cutoff(atoms), 1.0))
	for i in range(atoms.size()):
		grid.insert(i, _get_pos(atoms[i]))
	return grid

static func _lennard_jones_energy(atoms: Array) -> float:
	var e = 0.0
	var n = atoms.size()
	if n < 2:
		return 0.0
	var cutoff = _lj_cutoff(atoms)
	var grid = _build_lj_hash(atoms)
	for i in range(n):
		var pos_i = _get_pos(atoms[i])
		for j in grid.query_radius(pos_i, cutoff):
			if j <= i:
				continue
			var r = pos_i.distance_to(_get_pos(atoms[j]))
			if r < 0.1:
				continue
			var sigma_i = _get_lj_sigma(atoms[i])
			var sigma_j = _get_lj_sigma(atoms[j])
			var eps_i = _get_lj_epsilon(atoms[i])
			var eps_j = _get_lj_epsilon(atoms[j])
			var sigma = (sigma_i + sigma_j) / 2.0
			var eps = sqrt(eps_i * eps_j)
			if r > LJ_TRUNCATION * sigma:
				continue
			var sr = sigma / r
			var sr6 = sr * sr * sr * sr * sr * sr
			var sr12 = sr6 * sr6
			e += 4.0 * eps * (sr12 - sr6)
	return e

static func compute_forces(atoms: Array, bonds: Array, angles: Array = []) -> Array:
	var n = atoms.size()
	var forces: Array = []
	for i in range(n):
		forces.append(Vector3.ZERO)
	_bond_forces(atoms, bonds, forces)
	_angle_forces(atoms, angles, forces)
	_lj_forces(atoms, forces)
	return forces

static func _bond_forces(atoms: Array, bonds: Array, forces: Array):
	for bond in bonds:
		var a = int(bond.get("a", 0))
		var b = int(bond.get("b", 0))
		if a < 0 or a >= atoms.size() or b < 0 or b >= atoms.size():
			continue
		var pos_a = _get_pos(atoms[a])
		var pos_b = _get_pos(atoms[b])
		var diff = pos_a - pos_b
		var r = diff.length()
		if r < 0.001:
			continue
		var r0 = float(bond.get("r0", 1.0))
		var k = float(bond.get("k", DEFAULT_BOND_K))
		var f_mag = -2.0 * k * (r - r0)
		var f_dir = diff / r
		forces[a] += f_dir * f_mag
		forces[b] -= f_dir * f_mag

static func _angle_forces(atoms: Array, angles: Array, forces: Array):
	for angle in angles:
		var i = int(angle.get("i", 0))
		var j = int(angle.get("j", 0))
		var k_idx = int(angle.get("k", 0))
		if i < 0 or i >= atoms.size() or j < 0 or j >= atoms.size() or k_idx < 0 or k_idx >= atoms.size():
			continue
		var pi = _get_pos(atoms[i])
		var pj = _get_pos(atoms[j])
		var pk = _get_pos(atoms[k_idx])
		var vi = pi - pj
		var vk = pk - pj
		var ri = vi.length()
		var rk = vk.length()
		if ri < 0.01 or rk < 0.01:
			continue
		var cos_theta = vi.dot(vk) / (ri * rk)
		cos_theta = clamp(cos_theta, -0.9999, 0.9999)
		var theta = acos(cos_theta)
		var theta0 = float(angle.get("theta0", PI * 109.47 / 180.0))
		var k = float(angle.get("k_angle", DEFAULT_ANGLE_K))
		var dtheta = theta - theta0
		var sin_theta = sin(theta)
		if abs(sin_theta) < 0.001:
			continue
		var fi = (vk / (ri * rk) - vi * cos_theta / (ri * ri)) / sin_theta
		var fk = (vi / (ri * rk) - vk * cos_theta / (rk * rk)) / sin_theta
		var fj = -(fi + fk)
		var f_mag = -2.0 * k * dtheta
		forces[i] += fi * f_mag
		forces[j] += fj * f_mag
		forces[k_idx] += fk * f_mag

static func _lj_forces(atoms: Array, forces: Array):
	var n = atoms.size()
	if n < 2:
		return
	var cutoff = _lj_cutoff(atoms)
	var grid = _build_lj_hash(atoms)
	for i in range(n):
		var pos_i = _get_pos(atoms[i])
		for j in grid.query_radius(pos_i, cutoff):
			if j <= i:
				continue
			var diff = pos_i - _get_pos(atoms[j])
			var r = diff.length()
			if r < 0.1:
				continue
			var sigma_i = _get_lj_sigma(atoms[i])
			var sigma_j = _get_lj_sigma(atoms[j])
			var eps_i = _get_lj_epsilon(atoms[i])
			var eps_j = _get_lj_epsilon(atoms[j])
			var sigma = (sigma_i + sigma_j) / 2.0
			var eps = sqrt(eps_i * eps_j)
			if r > LJ_TRUNCATION * sigma:
				continue
			var sr = sigma / r
			var sr6 = sr * sr * sr * sr * sr * sr
			var sr12 = sr6 * sr6
			var f_mag = 24.0 * eps / r * (2.0 * sr12 - sr6)
			var f_dir = diff / r
			forces[i] += f_dir * f_mag
			forces[j] -= f_dir * f_mag

static func minimize(atoms: Array, bonds: Array, angles: Array = [],
					 max_iter: int = 200, step_size: float = 0.001,
					 tol: float = 1e-6) -> Dictionary:
	var positions: Array = []
	for a in atoms:
		positions.append(_get_pos(a))
	var e_prev = compute_energy(atoms, bonds, angles)
	var converged = false
	var iter_done = 0
	var max_force = 0.0
	for iter in range(max_iter):
		iter_done = iter + 1
		var forces = compute_forces(atoms, bonds, angles)
		max_force = 0.0
		for f in forces:
			max_force = max(max_force, f.length())
		if max_force < tol:
			converged = true
			break
		var eta = step_size
		for i in range(atoms.size()):
			var new_pos = _get_pos(atoms[i]) + forces[i] * eta
			_set_pos(atoms[i], new_pos)
		var e_new = compute_energy(atoms, bonds, angles)
		if e_new > e_prev:
			eta *= 0.5
			for i in range(atoms.size()):
				var new_pos = positions[i]
				_set_pos(atoms[i], new_pos)
			if eta < 1e-8:
				converged = true
				break
		else:
			e_prev = e_new
			for i in range(atoms.size()):
				positions[i] = _get_pos(atoms[i])
	return {
		"converged": converged,
		"iterations": iter_done,
		"final_energy": e_prev,
		"max_force": max_force if iter_done > 0 else 0.0
	}

static func build_bonds_with_ideal(atoms: Array, bond_pairs: Array) -> Array:
	var result: Array = []
	for bp in bond_pairs:
		var a = bp[0]
		var b = bp[1]
		var sym_a = _get_symbol(atoms[a])
		var sym_b = _get_symbol(atoms[b])
		var data_a = ElementDB.get_element(sym_a)
		var data_b = ElementDB.get_element(sym_b)
		var r_a = float(data_a.get("covalent_radius_pm", 50)) / 100.0
		var r_b = float(data_b.get("covalent_radius_pm", 50)) / 100.0
		result.append({"a": a, "b": b, "r0": r_a + r_b, "k": DEFAULT_BOND_K})
	return result

static func build_angles_from_bonds(atoms: Array, bonds: Array) -> Array:
	var adj: Dictionary = {}
	for i in range(atoms.size()):
		adj[i] = []
	for bond in bonds:
		var a = int(bond.get("a", 0))
		var b = int(bond.get("b", 0))
		adj[a].append(b)
		adj[b].append(a)
	var angles: Array = []
	for j in range(atoms.size()):
		var neighbors = adj[j]
		if neighbors.size() < 2:
			continue
		for ii in range(neighbors.size()):
			for jj in range(ii + 1, neighbors.size()):
				var n_count = neighbors.size()
				var theta0 = 109.47
				match n_count:
					2: theta0 = 180.0
					3: theta0 = 120.0
					4: theta0 = 109.47
					_: theta0 = 90.0
				angles.append({
					"i": neighbors[ii], "j": j, "k": neighbors[jj],
					"theta0": theta0 * PI / 180.0, "k_angle": DEFAULT_ANGLE_K
				})
	return angles

static func _get_pos(atom) -> Vector3:
	if atom is Dictionary:
		return atom.get("position", Vector3.ZERO)
	return atom.position

static func _set_pos(atom, pos: Vector3):
	if atom is Dictionary:
		atom["position"] = pos
	else:
		atom.position = pos

static func _get_symbol(atom) -> String:
	if atom is Dictionary:
		return atom.get("symbol", "H")
	return atom.element_symbol

static func _get_lj_sigma(atom) -> float:
	var sym = _get_symbol(atom)
	var data = ElementDB.get_element(sym)
	var r = float(data.get("atomic_radius_pm", 100)) / 100.0
	return r * 2.0

static func _get_lj_epsilon(_atom) -> float:
	return LJ_EPSILON