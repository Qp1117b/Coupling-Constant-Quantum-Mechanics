extends RefCounted
class_name CQMEmergenceIntegral

# CQM 超导涌现积分 — §5
# ψ(r,T) = ∫_BZ d³k D_lattice(k) · P_electron(k,T) · C_triple(k) · K_causal(k) · e^{-Γ_φ(T)|τ|}
#
# 各项本体论地位:
#   D_lattice  : 原料层, 晶格因果潜能谱, 不依赖温度
#   P_electron : 被动载体, 电子配对倾向权重, BCS极限≈f(E)(1-f(E))
#   C_triple   : CQM最具原创性项, 三方因果闭环建立强度
#   K_causal   : 因果截断核, 引力因果限制场筛选
#   e^{-Γ|τ|} : 相位再生产锁定因子, 稳定性维持
#
# 强引力推广(§5.6): 追加 T_grav(g_μν) 因子
# BCS退化: C_triple→V_eff, K_causal→Θ(ω_D-ω), F[Top]→1, B̂→I

const HBAR = 1.055e-34
const BOLTZMANN = 1.381e-23

enum Precision { FAST, NORMAL, HIGH }

static func evaluate(eigenvalues: Array, spectral_gap: float,
					 temperature: float, dos_fermi: float,
					 tc: float = 0.0, precision: int = Precision.NORMAL,
					 topology_factor: float = 1.0,
					 metric_g00: float = -1.0) -> Dictionary:
	var D = compute_D_lattice(eigenvalues, spectral_gap)
	var P = compute_P_electron(temperature, tc, dos_fermi)
	var C_triple = compute_C_triple(eigenvalues, spectral_gap, dos_fermi)
	var K_causal = compute_K_causal(spectral_gap)
	var phase_lock = compute_phase_locking(temperature, tc)
	var F_top = topology_factor
	var T_grav = CQMGravityFactor.evaluate(metric_g00, spectral_gap)

	var integrand = D * P * C_triple * K_causal * phase_lock * F_top * T_grav

	return {
		"psi": integrand,
		"D_lattice": D,
		"P_electron": P,
		"C_triple": C_triple,
		"K_causal": K_causal,
		"phase_locking": phase_lock,
		"topology_factor": F_top,
		"gravity_factor": T_grav,
		"precision": precision
	}

static func compute_D_lattice(eigenvalues: Array, spectral_gap: float) -> float:
	if eigenvalues.is_empty():
		return 0.5
	var sum_ev = 0.0
	for ev in eigenvalues:
		sum_ev += float(ev)
	var avg = sum_ev / eigenvalues.size()
	return avg * spectral_gap if spectral_gap > 0 else avg

static func compute_P_electron(temperature: float, tc: float, dos_fermi: float) -> float:
	if tc <= 0:
		return 0.0
	if temperature >= tc:
		return 0.0
	var t_ratio = temperature / tc
	var max_pairing = 0.25
	var thermal_broadening = 1.0 - t_ratio * t_ratio
	return max_pairing * thermal_broadening * dos_fermi

static func compute_C_triple(eigenvalues: Array, spectral_gap: float, dos_fermi: float) -> float:
	return CQMTripleLoop.fermi_surface_average(eigenvalues, spectral_gap, dos_fermi)

static func compute_K_causal(spectral_gap: float) -> float:
	var _omega_causal = CQMCausalKernel.causal_cutoff_frequency(spectral_gap)
	var omega_typical = 1e13
	return CQMCausalKernel.evaluate(omega_typical, spectral_gap)

static func compute_phase_locking(temperature: float, tc: float) -> float:
	if tc <= 0:
		return 0.0
	if temperature >= tc:
		return 0.0
	var t_ratio = temperature / tc
	var gamma_phi = -log(max(0.001, 1.0 - t_ratio)) / tc
	var tau = 1.0 / tc
	return exp(-gamma_phi * tau)

static func evaluate_full_bz(cartan_matrix: Array, matrix_size: int,
							 temperature: float, tc: float, spectral_gap: float,
							 k_points: int = 16) -> Dictionary:
	var psi_total = 0.0
	var D_total = 0.0
	var P_total = 0.0
	var C_total = 0.0
	var K_total = 0.0
	var weight = 1.0 / float(k_points * k_points * k_points)
	var _dos_f = 0.5

	for i in range(k_points):
		for j in range(k_points):
			for k in range(k_points):
				var kx = (float(i) + 0.5) / k_points - 0.5
				var ky = (float(j) + 0.5) / k_points - 0.5
				var kz = (float(k) + 0.5) / k_points - 0.5
				var k_vec = Vector3(kx, ky, kz)
				var omega_k = k_vec.length() * 1e13

				var D = _lattice_propagator(k_vec, cartan_matrix, matrix_size)
				var P = _electron_propagator(k_vec, temperature, tc)
				var C = CQMTripleLoop.evaluate(k_vec, omega_k, spectral_gap)
				var K = CQMCausalKernel.evaluate(omega_k, spectral_gap)

				var integrand = D * P * C * K
				psi_total += integrand * weight
				D_total += D * weight
				P_total += P * weight
				C_total += C * weight
				K_total += K * weight

	return {
		"psi": psi_total,
		"D_lattice_avg": D_total,
		"P_electron_avg": P_total,
		"C_triple_avg": C_total,
		"K_causal_avg": K_total,
		"k_points": k_points * k_points * k_points
	}

static func _lattice_propagator(k_vec: Vector3, _cartan_matrix: Array, _size: int) -> float:
	var k_sq = k_vec.length_squared()
	return 1.0 / (1.0 + k_sq)

static func _electron_propagator(k_vec: Vector3, temperature: float, tc: float) -> float:
	if tc <= 0 or temperature >= tc:
		return 0.0
	var k_sq = k_vec.length_squared()
	var xi_sq = 1.0 - temperature / tc
	return 1.0 / (k_sq + max(0.01, xi_sq))

static func bcs_degradation(_eigenvalues: Array, spectral_gap: float,
							dos_fermi: float, _tc: float) -> Dictionary:
	var T_causal = HBAR * CQMCausalKernel.causal_cutoff_frequency(spectral_gap) / BOLTZMANN
	var a4_gap = CQMConfig.get_spectral_gap()
	var V0 = 1.0 / (1.0 + spectral_gap / a4_gap) if a4_gap > 0 else 0.5
	var coupling = dos_fermi * V0
	var bcs_exp = exp(-1.0 / coupling) if coupling > 0 else 0.0
	var prefactor = CQMConfig.get_bcs_prefactor()
	return {
		"tc_bcs": prefactor * T_causal * bcs_exp,
		"T_causal": T_causal,
		"coupling": coupling,
		"bcs_exp": bcs_exp,
		"degraded": true
	}