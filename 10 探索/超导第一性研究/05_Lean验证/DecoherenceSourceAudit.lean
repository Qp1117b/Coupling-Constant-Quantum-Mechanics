/-
  R29：拍频退相干来源审计——单拍频不退相干，退相位由展宽控制
  ============================================================
  链内前提（06 L1328/L1332/L1336/L1350；§10.2；12.A3）：
    多模叠加、拍频、Tc 处 λ2=λ1、空间不均匀、高模权重压制但非零。
  B 类对照：自由进动不是退相干；静态展宽给 T2* 型退相位（可逆）。

  本文件承载：
    (1) 确定两模拍频的相干幅度平方恒为 w1*w2（相位振荡但不衰减）；
    (2) 方差为零（单一频率）时包络恒 1，无有限 τ；
    (3) 高模权重非零且劈裂不同 ⇒ 即使 Δλ=0 展宽仍正 ⇒ τ 有限；
    (4) 要从 τ=√2ħ/σ 得 τ∝1/|Δλ| 须额外前提 σ=κ|Δλ|（κ 外生）。

  不证明：不可逆退相干定理；环境耦合的具体形式；06 L1350 的严格证明。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

namespace CQM.DecoherenceSourceAudit

noncomputable section

/-- (1) 两模相对相位以 $\\Delta\\lambda/\\hbar$ 振荡，但相干幅度平方恒为 $w_1w_2$。 -/
theorem beat_amplitude_sq_const (w1 w2 phi : ℝ) (h1 : 0 ≤ w1) (h2 : 0 ≤ w2) :
    (Real.sqrt (w1 * w2) * Real.cos phi) ^ 2 +
      (Real.sqrt (w1 * w2) * Real.sin phi) ^ 2 = w1 * w2 := by
  have hw : 0 ≤ w1 * w2 := mul_nonneg h1 h2
  rw [show (Real.sqrt (w1 * w2) * Real.cos phi) ^ 2 =
        (Real.sqrt (w1 * w2)) ^ 2 * (Real.cos phi) ^ 2 by ring]
  rw [show (Real.sqrt (w1 * w2) * Real.sin phi) ^ 2 =
        (Real.sqrt (w1 * w2)) ^ 2 * (Real.sin phi) ^ 2 by ring]
  rw [Real.sq_sqrt hw]
  nlinarith [Real.sin_sq_add_cos_sq phi]

/-- (2) 频率展宽为零（单一频率）时，包络幅度恒为 1：无退相位。 -/
theorem zero_spread_no_decay (phi : ℝ) :
    (Real.cos phi) ^ 2 + (Real.sin phi) ^ 2 = 1 := by
  nlinarith [Real.sin_sq_add_cos_sq phi]

/-- (3) 两拍频值 $d_1\\ne d_2$ 且权重均正 ⇒ 方差正（高模非零则展宽不消失）。 -/
theorem spread_positive (d1 d2 p : ℝ) (hp0 : 0 < p) (hp1 : p < 1) (hne : d1 ≠ d2) :
    0 < p * (1 - p) * (d1 - d2) ^ 2 := by
  have hppos : 0 < p * (1 - p) := mul_pos hp0 (by linarith)
  have hsquare : 0 < (d1 - d2) ^ 2 := sq_pos_of_ne_zero (sub_ne_zero.mpr hne)
  exact mul_pos hppos hsquare

/-- (3′) 12.A3 高模权重压制但非零 ⇒ $T_c$ 处（$\\Delta\\lambda=0$）展宽仍正。 -/
theorem high_mode_keeps_spread (L : ℝ) (p : ℝ) (hp0 : 0 < p) (hp1 : p < 1) (hL : 0 < L) :
    0 < p * (1 - p) * L ^ 2 := by
  convert spread_positive 0 L p hp0 hp1 (by linarith) using 1
  ring

/-- (4) 条件结构：若额外假设 $\\sigma=\\kappa|\\Delta\\lambda|$，则 $\\tau=\\sqrt2\\hbar/(\\kappa|\\Delta\\lambda|)$。 -/
theorem tau_scaling_needs_kappa (hbar sigma kappa d : ℝ)
    (hsigma : sigma = kappa * d) :
    Real.sqrt 2 * hbar / sigma = Real.sqrt 2 * hbar / (kappa * d) := by
  rw [hsigma]

end
end CQM.DecoherenceSourceAudit
