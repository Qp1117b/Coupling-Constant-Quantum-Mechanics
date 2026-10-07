extends RefCounted
class_name CQMGravityFactor

# CQM 强引力拓扑因子 T_grav(g_μν) — §5.6
# 调制因果分辨率: τ_res → τ_res·√(-g_00)
# 弱引力极限: T_grav → 1
# 强引力场(中子星表面等): 打开新因果截断通道，改变涌现
#
# ψ(r,T,g) = ∫d³k D·P·C_triple·K_causal·T_grav(g)·e^{-Γ|τ|}
#
# G12未闭合: T_grav完整度规依赖形式待定

const SPEED_OF_LIGHT = 2.998e8
const HBAR = 1.055e-34

static func evaluate(metric_g00: float = -1.0, spectral_gap: float = 0.0) -> float:
	var sqrt_neg_g00 = sqrt(abs(metric_g00))
	if sqrt_neg_g00 < 1e-10:
		return 1.0
	if abs(sqrt_neg_g00 - 1.0) < 1e-10:
		return 1.0
	var a4_gap = CQMConfig.get_spectral_gap()
	var gap_ratio = spectral_gap / a4_gap if a4_gap > 0 and spectral_gap > 0 else 1.0
	return 1.0 / sqrt_neg_g00 * (1.0 + 0.1 * (sqrt_neg_g00 - 1.0) * gap_ratio)

static func corrected_causal_resolution(tau_res: float, metric_g00: float) -> float:
	return tau_res * sqrt(abs(metric_g00))

static func corrected_omega_causal(omega_causal: float, metric_g00: float) -> float:
	var sqrt_neg_g00 = sqrt(abs(metric_g00))
	if sqrt_neg_g00 < 1e-10:
		return omega_causal
	return omega_causal / sqrt_neg_g00

static func weak_gravity_limit() -> float:
	return 1.0

static func neutron_star_surface() -> Dictionary:
	var g00_ns = -0.7
	return {
		"metric_g00": g00_ns,
		"T_grav": evaluate(g00_ns),
		"tau_res_correction": sqrt(abs(g00_ns)),
		"omega_causal_correction": 1.0 / sqrt(abs(g00_ns))
	}

static func schwarzschild_metric(r: float, r_s: float) -> float:
	if r <= r_s:
		return 0.0
	return -(1.0 - r_s / r)

static func is_strong_gravity(metric_g00: float) -> bool:
	return abs(abs(metric_g00) - 1.0) > 0.01