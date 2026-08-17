extends RefCounted
class_name CQMCausalKernel

# CQM 因果截断核 K_causal(k) — §5.4.4
# 引力因果限制场的筛选函数：配对因果时差须达到晶格因果分辨率
# ω_q ≤ ω_causal = 2π·M_eff·c²/ℏ
#
# 两种形式：
#   阶梯函数: K = Θ(ω_causal - ω_k)           [已实现]
#   高斯共振窗口: K = exp[-(Δτ-τ_res)²/2σ²]   [G9未闭合，σ来源待定]
#
# CQM vs BCS 关键区别：
#   BCS: ω_D (德拜频率, ∝ M^{-1/2})
#   CQM: ω_causal (∝ M_eff, 引力因果限制)

const HBAR = 1.055e-34
const SPEED_OF_LIGHT = 2.998e8

enum KernelForm { STEP, GAUSSIAN_RESONANCE }

static func causal_cutoff_frequency(spectral_gap: float) -> float:
	var C = CQMConfig.get_spectral_quantum_c()
	var base = C * SPEED_OF_LIGHT / 1.616e-35
	var a4_gap = CQMConfig.get_spectral_gap()
	var correction = spectral_gap / a4_gap if a4_gap > 0 else 1.0
	return base * correction

static func causal_resolution_time(m_eff_kg: float) -> float:
	return HBAR / (m_eff_kg * SPEED_OF_LIGHT * SPEED_OF_LIGHT)

static func evaluate(omega_k: float, spectral_gap: float,
					 form: int = KernelForm.STEP, sigma: float = 0.0) -> float:
	var omega_causal = causal_cutoff_frequency(spectral_gap)
	match form:
		KernelForm.STEP:
			return 1.0 if omega_k <= omega_causal else 0.0
		KernelForm.GAUSSIAN_RESONANCE:
			if sigma <= 0:
				return 1.0 if omega_k <= omega_causal else 0.0
			var tau_res = 2.0 * PI / omega_causal
			var delta_tau = 2.0 * PI / omega_k if omega_k > 0 else tau_res
			return exp(-(delta_tau - tau_res) * (delta_tau - tau_res) / (2.0 * sigma * sigma))
		_:
			return 1.0 if omega_k <= omega_causal else 0.0

static func isotope_exponent_cqm() -> float:
	return 1.0

static func isotope_exponent_bcs() -> float:
	return -0.5

static func bcs_degradation_check(omega_debye: float, spectral_gap: float) -> Dictionary:
	var omega_causal = causal_cutoff_frequency(spectral_gap)
	return {
		"omega_causal": omega_causal,
		"omega_debye": omega_debye,
		"ratio": omega_causal / omega_debye if omega_debye > 0 else 0.0,
		"degraded": abs(omega_causal - omega_debye) / max(omega_causal, omega_debye) < 0.1
	}