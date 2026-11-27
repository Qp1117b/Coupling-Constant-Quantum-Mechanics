-- Ring15LockTanhQuintic.lean（第 218 轮）：$\tanh$ 的五阶上界（由 217 的三阶下界平方后积分得到）。
-- 只 import Ring15Spec 与 217 的工具模块；不 import 任何其它证明模块。
import Ring15Spec
import Ring15LockTanhTools
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic

namespace CQM.Ring15.LockTanhQuintic

open MeasureTheory
open scoped Interval
open CQM.Ring15.Spec
open CQM.Ring15.LockTanhTools

/-- **$\tanh$ 的五阶上界**：$\forall 0\le s\le1,\ \tanh s\le s-\frac{s^3}{3}+\frac{2s^5}{15}$。
路线：$\tanh s=s-\int_0^s\tanh^2$，而 $\tanh^2t\ge(t-\frac{t^3}{3})^2\ge t^2-\frac{2t^4}{3}$（三阶下界取自 217）。 -/
theorem tanhQuintic (s : ℝ) (hs0 : 0 ≤ s) (hs1 : s ≤ 1) :
    Real.tanh s ≤ s - s ^ 3 / 3 + 2 * s ^ 5 / 15 := by
  have hs_int : IntervalIntegrable (fun t : ℝ => sechSq t) volume (0 : ℝ) s :=
    cont_sechSq.intervalIntegrable 0 s
  have htanh : ∫ t in (0 : ℝ)..s, sechSq t = Real.tanh s := by
    have hd : ∀ z ∈ Set.uIcc (0 : ℝ) s, HasDerivAt Real.tanh (sechSq z) z :=
      fun z _ => tanhHasDerivAt z
    have h := intervalIntegral.integral_eq_sub_of_hasDerivAt hd hs_int
    simpa using h
  have hIntTanh : IntervalIntegrable (fun t : ℝ => Real.tanh t ^ 2) volume (0 : ℝ) s :=
    (continuous_tanh.pow 2).intervalIntegrable 0 s
  have hIntPoly : IntervalIntegrable (fun t : ℝ => t ^ 2 - 2 * t ^ 4 / 3) volume (0 : ℝ) s := by
    have h1 : IntervalIntegrable (fun t : ℝ => t ^ 2) volume (0 : ℝ) s :=
      (continuous_id.pow 2).intervalIntegrable 0 s
    have h2 : IntervalIntegrable (fun t : ℝ => 2 * t ^ 4 / 3) volume (0 : ℝ) s :=
      ((continuous_const.mul (continuous_id.pow 4)).div_const 3).intervalIntegrable 0 s
    exact h1.sub h2
  have htanh_sq : ∫ t in (0 : ℝ)..s, Real.tanh t ^ 2 = s - Real.tanh s := by
    have hcongr : ∫ t in (0 : ℝ)..s, Real.tanh t ^ 2 = ∫ t in (0 : ℝ)..s, (1 - sechSq t) := by
      refine intervalIntegral.integral_congr (fun t _ => ?_)
      rw [sechSq_eq_one_sub_tanh_sq]; ring
    have hIntOne : IntervalIntegrable (fun t : ℝ => 1 - sechSq t) volume (0 : ℝ) s :=
      (continuous_const.sub cont_sechSq).intervalIntegrable 0 s
    have hsub : ∫ t in (0 : ℝ)..s, (1 - sechSq t) = s - ∫ t in (0 : ℝ)..s, sechSq t := by
      rw [intervalIntegral.integral_sub (continuous_const.intervalIntegrable 0 s) hs_int]
      simp
    rw [hcongr, hsub, htanh]
  have hmono : (∫ t in (0 : ℝ)..s, t ^ 2 - 2 * t ^ 4 / 3)
      ≤ ∫ t in (0 : ℝ)..s, Real.tanh t ^ 2 := by
    refine intervalIntegral.integral_mono_on hs0 hIntPoly hIntTanh ?_
    intro t ht
    have ht0 : 0 ≤ t := ht.1
    have ht1 : t ≤ s := ht.2
    have htle1 : t ≤ 1 := le_trans ht1 hs1
    have hcub := targetPropTanhCubic t ht0
    have hnonneg : 0 ≤ t - t ^ 3 / 3 := by
      have h1 : t ^ 2 ≤ 1 := by nlinarith [ht0, htle1]
      nlinarith [ht0, h1]
    have hsq : (t - t ^ 3 / 3) ^ 2 ≤ Real.tanh t ^ 2 := by
      nlinarith [hcub, hnonneg, sq_nonneg (Real.tanh t - (t - t ^ 3 / 3))]
    nlinarith [hsq, sq_nonneg t, pow_nonneg ht0 4, pow_nonneg ht0 6]
  have hintpoly : ∫ t in (0 : ℝ)..s, t ^ 2 - 2 * t ^ 4 / 3 = s ^ 3 / 3 - 2 * s ^ 5 / 15 := by
    have h2 : IntervalIntegrable (fun t : ℝ => t ^ 2) volume (0 : ℝ) s :=
      (continuous_id.pow 2).intervalIntegrable 0 s
    have h4 : IntervalIntegrable (fun t : ℝ => t ^ 4) volume (0 : ℝ) s :=
      (continuous_id.pow 4).intervalIntegrable 0 s
    have h2c : IntervalIntegrable (fun t : ℝ => 2 * t ^ 4 / 3) volume (0 : ℝ) s :=
      ((continuous_const.mul (continuous_id.pow 4)).div_const 3).intervalIntegrable 0 s
    rw [intervalIntegral.integral_sub h2 h2c]
    have hq : ∫ t in (0 : ℝ)..s, t ^ 2 = s ^ 3 / 3 := by rw [integral_pow]; norm_num
    have h4v : ∫ t in (0 : ℝ)..s, t ^ 4 = s ^ 5 / 5 := by rw [integral_pow]; norm_num
    rw [hq]
    have hmul : ∫ t in (0 : ℝ)..s, 2 * t ^ 4 / 3 = 2 * (∫ t in (0 : ℝ)..s, t ^ 4) / 3 := by
      rw [intervalIntegral.integral_div, intervalIntegral.integral_const_mul]
    rw [hmul, h4v]
    ring
  rw [htanh_sq] at hmono
  rw [hintpoly] at hmono
  linarith

/-- **五阶上界的 Spec 对齐版**（主定理名按目录规范）：`tanhQuintic` 的命题形态。 -/
theorem targetPropTanhQuintic : CQM.Ring15.Spec.TargetPropTanhQuintic := by
  intro s hs0 hs1
  exact tanhQuintic s hs0 hs1