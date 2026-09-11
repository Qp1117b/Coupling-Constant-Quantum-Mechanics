extends RefCounted
class_name CQMReproductionAction

# CQM 再生产作用量 S_reproduction — §7(固有时流速) + §11(温度依赖)
# 温度-因果时动力学 (耦合空间曲率机制)
# S = ∫dt Σ_T tr(T_T ∘ (D_t + F[curv]·Γ_0·e^{-E_gap/kT}) · T_T) + Σ_T tr(T_T∘T_T†/g_eff[Γ_T])
#
# T_T     : A4根系多分量序参量, 4×4复矩阵
# D_t     : 坐标时协变导数, 固有时流速 dτ/dt = 1+βδ_v
# F[curv] : 曲率涨落调制因子 (旧称拓扑增强因子)
# g_eff   : 由嘉当矩阵谱决定的等效耦合强度
#
# 两步操作:
#   1. 相容性筛选(唯一性): FG退相干场对叠加态的几何-拓扑测试
#   2. 再生产锁定(确定性): 筛选出的分支能否持续存在

const BOLTZMANN = 1.381e-23

static func compute(causal_tensor: Array, eigenvalues: Array,
					temperature: float, topology_factor: float = 1.0,
					energy_gap: float = 0.0) -> Dictionary:
	var s_kinetic = _kinetic_term(causal_tensor, temperature)
	var s_reproduction = _reproduction_term(causal_tensor, topology_factor, energy_gap, temperature)
	var s_coupling = _coupling_term(causal_tensor, eigenvalues)
	var s_total = s_kinetic + s_reproduction + s_coupling
	return {
		"S_reproduction": s_total,
		"S_kinetic": s_kinetic,
		"S_reproduction_core": s_reproduction,
		"S_coupling": s_coupling,
		"topology_factor": topology_factor
	}

static func _kinetic_term(causal_tensor: Array, temperature: float) -> float:
	if causal_tensor.is_empty():
		return 0.0
	var total = 0.0
	for T_T in causal_tensor:
		var norm_sq = _tensor_norm_squared(T_T)
		total += norm_sq * temperature
	return total

static func _reproduction_term(causal_tensor: Array, topology_factor: float,
								energy_gap: float, temperature: float) -> float:
	if causal_tensor.is_empty():
		return 0.0
	var gamma_0 = 1.0
	var boltzmann_factor = 1.0
	if temperature > 0 and energy_gap > 0:
		boltzmann_factor = exp(-energy_gap / (BOLTZMANN * temperature))
	var total = 0.0
	for T_T in causal_tensor:
		var norm_sq = _tensor_norm_squared(T_T)
		total += topology_factor * gamma_0 * boltzmann_factor * norm_sq
	return total

static func _coupling_term(causal_tensor: Array, eigenvalues: Array) -> float:
	if causal_tensor.is_empty() or eigenvalues.is_empty():
		return 0.0
	var total = 0.0
	for i in range(causal_tensor.size()):
		var norm_sq = _tensor_norm_squared(causal_tensor[i])
		var g_eff = _effective_coupling(i, eigenvalues)
		if g_eff > 0:
			total += norm_sq / g_eff
	return total

static func _tensor_norm_squared(tensor) -> float:
	if tensor is Array:
		var sum = 0.0
		for row in tensor:
			if row is Array:
				for val in row:
					sum += float(val) * float(val)
			else:
				sum += float(row) * float(row)
		return sum
	return float(tensor) * float(tensor)

static func _effective_coupling(channel: int, eigenvalues: Array) -> float:
	if channel < eigenvalues.size():
		return max(float(eigenvalues[channel]), 0.01)
	return 1.0

static func compatibility_filter(_eigenvalues: Array, spectral_gap: float) -> Dictionary:
	var a4_gap = CQMConfig.get_spectral_gap()
	var compatibility = 1.0
	if a4_gap > 0:
		compatibility = min(1.0, spectral_gap / a4_gap)
	return {
		"passed": compatibility > 0.01,
		"compatibility_score": compatibility,
		"unique_branch": compatibility > 0.5
	}

static func reproduction_locking(temperature: float, tc: float) -> Dictionary:
	if tc <= 0:
		return {"locked": false, "gamma_phi": 1e10}
	var t_ratio = temperature / tc
	if t_ratio >= 1.0:
		return {"locked": false, "gamma_phi": 1e10}
	var gamma_phi = -log(max(0.001, 1.0 - t_ratio)) / tc
	return {"locked": gamma_phi < 1.0, "gamma_phi": gamma_phi}

static func bcs_degradation(_eigenvalues: Array) -> Dictionary:
	return {"S_reproduction": 0.0, "topology_factor": 1.0}