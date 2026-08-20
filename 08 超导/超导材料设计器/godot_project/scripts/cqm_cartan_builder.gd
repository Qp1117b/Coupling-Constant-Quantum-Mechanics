extends RefCounted
class_name CQMCartanBuilder

static func A4() -> PackedFloat32Array:
	return CQMConfig.get_A4()

static func A4_eigenvalues() -> PackedFloat32Array:
	return CQMConfig.get_eigenvalues()

static func spectral_gap() -> float:
	return CQMConfig.get_spectral_gap()

static func defect_matrix(delta: float) -> PackedFloat32Array:
	var mat = A4()
	var defect_type = CQMConfig.get_defect_type()
	match defect_type:
		"off_diagonal_alpha4":
			var pos = CQMConfig.get_defect_position()
			var i = int(pos[0])
			var j = int(pos[1])
			mat[i * 4 + j] = -delta
			mat[j * 4 + i] = -delta
		"diagonal":
			var pattern = CQMConfig.get_defect_pattern()
			for i in range(4):
				mat[i * 4 + i] -= delta * float(pattern[i])
	return mat

static func proton_matrix() -> PackedFloat32Array:
	match CQMConfig.get_proton_model_type():
		"pure_A4":
			return A4()
	return A4()

static func neutron_defect(N: int, symbol: String) -> float:
	var ov = CQMConfig.get_element_override(symbol)
	if ov.has("force_neutron_defect"):
		return float(ov.force_neutron_defect)

	var delta_0 = CQMConfig.get_delta_0()
	var beta = CQMConfig.get_beta()
	var N_ref = _estimate_N_ref(symbol)
	if N_ref == 0:
		return 0.0

	match CQMConfig.get_defect_function_type():
		"linear":
			return delta_0 * (1.0 + beta * float(N - N_ref) / float(N_ref))
		"quadratic":
			var dN = float(N - N_ref) / float(N_ref)
			return delta_0 * (1.0 + beta * dN * dN)
		"exponential":
			return delta_0 * exp(beta * float(N - N_ref) / float(N_ref))
	return delta_0

static func element_cartan(Z: int, N: int, symbol: String) -> Dictionary:
	var eps = neutron_defect(N, symbol)
	var size = 4 * (Z + N)
	var mat = PackedFloat32Array()
	mat.resize(size * size)
	mat.fill(0.0)

	var cp = proton_matrix()
	for i in range(Z):
		_place_block(mat, size, cp, 4 * i)

	var cn = defect_matrix(eps)
	for j in range(N):
		_place_block(mat, size, cn, 4 * (Z + j))

	return {"matrix": mat, "size": size, "Z": Z, "N": N, "delta": eps}

static func _place_block(mat: PackedFloat32Array, size: int,
						  block: PackedFloat32Array, offset: int):
	for i in range(4):
		for j in range(4):
			mat[(offset + i) * size + (offset + j)] = block[i * 4 + j]

static func _estimate_N_ref(symbol: String) -> int:
	var isotopes = ElementDB.get_isotopes(symbol)
	if isotopes.is_empty():
		return 1
	var best = isotopes[0]
	for iso in isotopes:
		if float(iso.get("abundance", 0)) > float(best.get("abundance", 0)):
			best = iso
	return int(best.get("neutrons", 1))

static func eigenvalues_jacobi(mat: PackedFloat32Array, size: int,
								max_iter: int = 200, tol: float = 1e-8) -> PackedFloat32Array:
	if size <= 1:
		return PackedFloat32Array([mat[0]]) if size == 1 else PackedFloat32Array()

	var a = mat.duplicate()
	var n = size

	for _iteration in range(max_iter):
		var p = 0
		var q = 1
		var max_val = 0.0
		for i in range(n):
			for j in range(i + 1, n):
				var val = abs(a[i * n + j])
				if val > max_val:
					max_val = val
					p = i
					q = j

		if max_val < tol:
			break

		var app = a[p * n + p]
		var aqq = a[q * n + q]
		var apq = a[p * n + q]
		var phi = 0.5 * atan2(2.0 * apq, app - aqq)
		var c = cos(phi)
		var s = sin(phi)

		for i in range(n):
			var aip = a[i * n + p]
			var aiq = a[i * n + q]
			a[i * n + p] = c * aip + s * aiq
			a[i * n + q] = -s * aip + c * aiq
		for j in range(n):
			var apj = a[p * n + j]
			var aqj = a[q * n + j]
			a[p * n + j] = c * apj + s * aqj
			a[q * n + j] = -s * apj + c * aqj

	var eigenvals = PackedFloat32Array()
	for i in range(n):
		eigenvals.append(a[i * n + i])
	eigenvals.sort()
	return eigenvals

static func spectral_gap_from_eigenvalues(eigenvalues: PackedFloat32Array) -> float:
	if eigenvalues.size() < 2:
		return 0.0
	for v in eigenvalues:
		if v > 1e-10:
			return v
	return 0.0
