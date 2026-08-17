extends RefCounted
class_name CQMStepwiseTransition

# CQM 分步相变 — §10.3
# A4根系各简单根方向凝聚温度不同 → 分步相变
#   T > T_c1: 常规态, Δ=0
#   T_c2 < T < T_c1: 通道1凝聚, Δ1≠0
#   T_c3 < T < T_c2: 通道1,2凝聚
#   T_c4 < T < T_c3: 通道1,2,3凝聚
#   T < T_c4: 全部通道凝聚, 完全超导态
#
# 实验契合点: LaH₁₀四极T₂g相变 ↔ CQM分步相变 (2026最新探索)
# 多芯涡旋结构: 每个涡旋包含多个A4根系分量子涡旋

static func compute(eigenvalues: Array, tc: float) -> Dictionary:
	if eigenvalues.is_empty() or tc <= 0:
		return {"transitions": [], "has_stepwise": false}

	var sorted_ev = eigenvalues.duplicate()
	sorted_ev.sort()

	var transitions: Array = []
	var n_channels = min(4, sorted_ev.size())
	var max_ev = float(sorted_ev[sorted_ev.size() - 1]) if sorted_ev.size() > 0 else 1.0

	for k in range(n_channels):
		var lambda_k = float(sorted_ev[k])
		var tc_k = tc * sqrt(lambda_k / max_ev) if max_ev > 0 else 0.0
		transitions.append({
			"channel": k + 1,
			"tc_channel": tc_k,
			"eigenvalue": lambda_k,
			"amplitude": sqrt(max(0.0, lambda_k))
		})

	transitions.sort_custom(func(a, b): return float(a.tc_channel) > float(b.tc_channel))

	var has_stepwise = false
	if transitions.size() >= 2:
		var tc_max = float(transitions[0].tc_channel)
		var tc_min = float(transitions[transitions.size() - 1].tc_channel)
		if tc_max > 0:
			has_stepwise = (tc_max - tc_min) / tc_max > 0.05

	return {
		"transitions": transitions,
		"has_stepwise": has_stepwise,
		"n_channels": n_channels,
		"tc_highest": float(transitions[0].tc_channel) if transitions.size() > 0 else 0.0,
		"tc_lowest": float(transitions[transitions.size() - 1].tc_channel) if transitions.size() > 0 else 0.0
	}

static func condensate_state(temperature: float, transitions: Array) -> Dictionary:
	var condensed_channels: Array = []
	var normal_channels: Array = []
	for t in transitions:
		if temperature < float(t.tc_channel):
			condensed_channels.append(int(t.channel))
		else:
			normal_channels.append(int(t.channel))
	return {
		"condensed": condensed_channels,
		"normal": normal_channels,
		"n_condensed": condensed_channels.size(),
		"n_total": transitions.size(),
		"partial_condensation": condensed_channels.size() > 0 and normal_channels.size() > 0,
		"fully_superconducting": normal_channels.is_empty() and not condensed_channels.is_empty(),
		"normal_state": condensed_channels.is_empty()
	}

static func multi_core_vortex(_field: float, transitions: Array) -> Dictionary:
	if transitions.is_empty():
		return {"vortex_cores": [], "multi_core": false}
	var cores: Array = []
	for t in transitions:
		cores.append({
			"channel": int(t.channel),
			"tc_channel": float(t.tc_channel),
			"vortex_radius": 1.0 / sqrt(max(0.01, float(t.eigenvalue)))
		})
	return {
		"vortex_cores": cores,
		"multi_core": cores.size() > 1,
		"n_cores": cores.size()
	}

static func lah10_quadrupole_check(eigenvalues: Array, tc: float) -> Dictionary:
	var result = compute(eigenvalues, tc)
	var has_4_channels = result.n_channels >= 4
	var stepwise = result.has_stepwise
	return {
		"matches_lah10_quadrupole": has_4_channels and stepwise,
		"n_channels": result.n_channels,
		"has_stepwise": stepwise,
		"tc_spread": result.tc_highest - result.tc_lowest
	}