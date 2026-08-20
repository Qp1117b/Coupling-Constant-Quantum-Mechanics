extends RefCounted
class_name CQMTopologyFactor

# CQM 曲率涨落调制因子 F[curv] — §5(精细引力纤维丛)
# 从Regge几何导出曲率刚度:
#   K_ij,kl = δ²S_constraint / δR_ij δR_kl |_{R̄}  (曲率刚度矩阵)
#   S_top = -Tr(ρ_top · ln(ρ_top))  (冯·诺依曼熵, ρ_top = K/Tr(K))
#   F[curv] = exp(-S_top)
#
# 非周期拼接(Q>0) → 能隙 → S_top > 0 → F[curv] < 1
# 平庸极限(周期晶格) → S_top = 0 → F[curv] = 1

static func compute_from_stiffness(stiffness_matrix: Array) -> float:
	if stiffness_matrix.is_empty():
		return 1.0
	var n = stiffness_matrix.size()
	var trace_K = 0.0
	for i in range(n):
		var row = stiffness_matrix[i]
		if row is Array and i < row.size():
			trace_K += float(row[i])
	if trace_K <= 0:
		return 1.0
	var s_top = _von_neumann_entropy(stiffness_matrix, trace_K)
	return exp(-s_top)

static func _von_neumann_entropy(stiffness_matrix: Array, trace_K: float) -> float:
	var n = stiffness_matrix.size()
	var entropy = 0.0
	for i in range(n):
		var row = stiffness_matrix[i]
		if row is Array and i < row.size():
			var eigenval = float(row[i]) / trace_K
			if eigenval > 1e-15:
				entropy -= eigenval * log(eigenval)
	return entropy

static func compute_from_spectral_gap(spectral_gap: float, a4_gap: float = 0.0) -> float:
	if a4_gap <= 0:
		a4_gap = CQMConfig.get_spectral_gap()
	var Q = abs(spectral_gap - a4_gap) / a4_gap if a4_gap > 0 else 0.0
	if Q <= 0:
		return 1.0
	var s_top = -log(1.0 - min(0.99, Q))
	return exp(-s_top)

static func compute_from_nonperiodicity(Q: float) -> float:
	if Q <= 0:
		return 1.0
	var s_top = -log(1.0 - min(0.99, Q))
	return exp(-s_top)

static func bcs_degradation() -> float:
	return 1.0

static func build_stiffness_matrix(eigenvalues: Array) -> Array:
	var n = min(eigenvalues.size(), 4)
	var matrix: Array = []
	for i in range(n):
		var row: Array = []
		for j in range(n):
			if i == j:
				var ev = float(eigenvalues[i]) if i < eigenvalues.size() else 1.0
				row.append(max(ev, 0.01))
			else:
				row.append(0.0)
		matrix.append(row)
	return matrix