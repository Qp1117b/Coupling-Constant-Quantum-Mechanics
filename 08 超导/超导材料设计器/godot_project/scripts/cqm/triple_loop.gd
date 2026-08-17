extends RefCounted
class_name CQMTripleLoop

# CQM 三方因果闭环强度 C_triple(k) — §5.4.3
# CQM最具原创性的项：两个电子不能直接配对，需晶格作为因果中介
# 电子1扰动晶格(发射虚声子) → 虚声子传播 → 电子2吸收 → 状态反向传播 → 因果闭环
#
# C_triple(k) ≈ |g_k|² · D(k,ω) · Θ_loop
#   |g_k|²    : 电子-声子耦合顶点
#   D(k,ω)    : 声子传播子
#   Θ_loop    : 闭环条件函数 [G10未闭合，动力学形式待定]
#
# BCS退化: C_triple → V_eff(k,k') 费米面平均

static func evaluate(k_vec: Vector3, omega_k: float, spectral_gap: float,
					 g_squared: float = 0.0, phonon_spectrum: float = 0.0) -> float:
	var gsq = g_squared if g_squared > 0 else _default_coupling_vertex(k_vec, spectral_gap)
	var D = phonon_spectrum if phonon_spectrum > 0 else _default_phonon_propagator(k_vec, omega_k)
	var theta = _loop_condition(k_vec, omega_k, spectral_gap)
	return gsq * D * theta

static func _default_coupling_vertex(k_vec: Vector3, spectral_gap: float) -> float:
	var k_mag = k_vec.length()
	var a4_gap = CQMConfig.get_spectral_gap()
	var gap_ratio = spectral_gap / a4_gap if a4_gap > 0 else 1.0
	return 0.5 * exp(-k_mag * k_mag) * (1.0 + gap_ratio)

static func _default_phonon_propagator(k_vec: Vector3, omega_k: float) -> float:
	if omega_k <= 0:
		return 0.0
	var _k_mag = k_vec.length()
	var omega_0 = 20.0
	return 2.0 * omega_0 / (omega_k * omega_k - omega_0 * omega_0 + 1.0) if omega_k != omega_0 else 0.0

static func _loop_condition(_k_vec: Vector3, omega_k: float, spectral_gap: float) -> float:
	var omega_causal = CQMCausalKernel.causal_cutoff_frequency(spectral_gap)
	return 1.0 if omega_k <= omega_causal else 0.0

static func bcs_degradation(spectral_gap: float, dos_fermi: float) -> float:
	var a4_gap = CQMConfig.get_spectral_gap()
	var V0 = 1.0 / (1.0 + spectral_gap / a4_gap) if a4_gap > 0 else 0.5
	return dos_fermi * V0

static func fermi_surface_average(eigenvalues: Array, spectral_gap: float, dos_fermi: float) -> float:
	if eigenvalues.is_empty():
		return bcs_degradation(spectral_gap, dos_fermi)
	var sum_g = 0.0
	for ev in eigenvalues:
		var k_mag = sqrt(abs(float(ev)))
		sum_g += _default_coupling_vertex(Vector3(k_mag, 0, 0), spectral_gap)
	return (sum_g / eigenvalues.size()) * dos_fermi