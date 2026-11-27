-- Ring15LockTanhTools.lean（第 217 轮）：$\tanh$ 的工具引理集（公开、可跨模块引用）＋三阶下界命题。
-- 只 import Ring15Spec 与基线里的积分基本定理、双曲函数导数；不 import 任何证明模块。
import Ring15Spec
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic

namespace CQM.Ring15.LockTanhTools

open MeasureTheory
open scoped Interval
open CQM.Ring15.Spec

/-- $\tanh$ 连续。 -/
theorem continuous_tanh : Continuous Real.tanh := by
  have h : Continuous fun y : ℝ => Real.sinh y / Real.cosh y :=
    Real.continuous_sinh.div Real.continuous_cosh (fun y => (Real.cosh_pos y).ne')
  exact h.congr (fun y => (Real.tanh_eq_sinh_div_cosh y).symm)

/-- $\mathrm{sech}^2$ 连续。 -/
theorem cont_sechSq : Continuous sechSq := by
  unfold sechSq
  exact continuous_const.div (Real.continuous_cosh.pow 2)
    (fun y => (pow_pos (Real.cosh_pos y) 2).ne')

/-- $\mathrm{sech}^2>0$。 -/
theorem sechSq_pos (x : ℝ) : 0 < sechSq x := by
  unfold sechSq
  exact one_div_pos.mpr (pow_pos (Real.cosh_pos x) 2)

/-- $\mathrm{sech}^2\le1$。 -/
theorem sechSq_le_one (x : ℝ) : sechSq x ≤ 1 := by
  have hc : Real.cosh x ^ 2 = Real.sinh x ^ 2 + 1 := Real.cosh_sq x
  have hp : 0 < Real.cosh x ^ 2 := pow_pos (Real.cosh_pos x) 2
  rw [sechSq, div_le_one hp]
  nlinarith [hc, sq_nonneg (Real.sinh x)]

/-- $\tanh$ 的导数：$\tanh'=\mathrm{sech}^2$。 -/
theorem tanhHasDerivAt (x : ℝ) : HasDerivAt Real.tanh (sechSq x) x := by
  have hdiv : HasDerivAt (fun y : ℝ => Real.sinh y / Real.cosh y)
      ((Real.cosh x * Real.cosh x - Real.sinh x * Real.sinh x) / Real.cosh x ^ 2) x :=
    (Real.hasDerivAt_sinh x).div (Real.hasDerivAt_cosh x) (Real.cosh_pos x).ne'
  have hfun : (fun y : ℝ => Real.sinh y / Real.cosh y) = Real.tanh := by
    funext y; exact (Real.tanh_eq_sinh_div_cosh y).symm
  have hv : (Real.cosh x * Real.cosh x - Real.sinh x * Real.sinh x) / Real.cosh x ^ 2
      = sechSq x := by
    have hc := Real.cosh_sq_sub_sinh_sq x
    unfold sechSq
    field_simp
    nlinarith [hc]
  rw [hfun, hv] at hdiv
  exact hdiv

/-- $\mathrm{sech}^2=1-\tanh^2$（把 $G$ 化成 $(T,h)$ 有理式的关键一步）。 -/
theorem sechSq_eq_one_sub_tanh_sq (x : ℝ) : sechSq x = 1 - Real.tanh x ^ 2 := by
  have hc : Real.cosh x ^ 2 = Real.sinh x ^ 2 + 1 := Real.cosh_sq x
  have hpos : 0 < Real.cosh x := Real.cosh_pos x
  have ht : Real.tanh x = Real.sinh x / Real.cosh x := Real.tanh_eq_sinh_div_cosh x
  have hsq : Real.tanh x ^ 2 = Real.sinh x ^ 2 / Real.cosh x ^ 2 := by
    rw [ht]; field_simp
  rw [hsq, sechSq]
  field_simp
  nlinarith [hc]

/-- $\tanh>0$（$x>0$）。 -/
theorem tanh_pos_of_pos {x : ℝ} (hx : 0 < x) : 0 < Real.tanh x := by
  rw [Real.tanh_eq_sinh_div_cosh]
  exact div_pos (Real.sinh_pos_iff.mpr hx) (Real.cosh_pos x)

/-- $\tanh x<x$（$x>0$）：$\tanh x=x-\int_0^x(1-\mathrm{sech}^2)$，被减项 $\int\tanh^2>0$。 -/
theorem tanhLtSelf {x : ℝ} (hx : 0 < x) : Real.tanh x < x := by
  have hIntS : IntervalIntegrable (fun t : ℝ => sechSq t) volume (0 : ℝ) x :=
    cont_sechSq.intervalIntegrable 0 x
  have htanh : ∫ t in (0 : ℝ)..x, sechSq t = Real.tanh x := by
    have hd : ∀ z ∈ Set.uIcc (0 : ℝ) x, HasDerivAt Real.tanh (sechSq z) z :=
      fun z _ => tanhHasDerivAt z
    have h := intervalIntegral.integral_eq_sub_of_hasDerivAt hd hIntS
    simpa using h
  have hpos : 0 < ∫ t in (0 : ℝ)..x, (1 - sechSq t) := by
    have hcont : Continuous fun t : ℝ => 1 - sechSq t :=
      continuous_const.sub cont_sechSq
    refine intervalIntegral.integral_pos hx hcont.continuousOn (fun t ht => ?_)
      ⟨x / 2, ⟨by linarith [hx], by linarith [hx]⟩, ?_⟩
    · have h1 : sechSq t ≤ 1 := sechSq_le_one t
      linarith
    · have hxp : 0 < x / 2 := by linarith [hx]
      have hs : 0 < Real.sinh (x / 2) := Real.sinh_pos_iff.mpr hxp
      have hltt : sechSq (x / 2) < 1 := by
        unfold sechSq
        rw [div_lt_one (pow_pos (Real.cosh_pos (x / 2)) 2)]
        nlinarith [Real.cosh_sq (x / 2), sq_pos_of_pos hs]
      linarith
  have hsub : ∫ t in (0 : ℝ)..x, (1 - sechSq t)
      = x - ∫ t in (0 : ℝ)..x, sechSq t := by
    rw [intervalIntegral.integral_sub (continuous_const.intervalIntegrable 0 x) hIntS]
    simp
  rw [hsub, htanh] at hpos
  linarith

/-- **$\tanh$ 的三阶下界**（本环主定理）：$\forall x\ge0,\ x-\dfrac{x^3}{3}\le\tanh x$。 -/
theorem targetPropTanhCubic : CQM.Ring15.Spec.TargetPropTanhCubic := by
  intro x hx
  rcases lt_or_eq_of_le hx with hpos | hzero
  · have hIntA : IntervalIntegrable (fun t : ℝ => 1 - sechSq t) volume (0 : ℝ) x :=
      (continuous_const.sub cont_sechSq).intervalIntegrable 0 x
    have hIntB : IntervalIntegrable (fun t : ℝ => t ^ 2) volume (0 : ℝ) x :=
      (continuous_id.pow 2).intervalIntegrable 0 x
    have hIntS : IntervalIntegrable (fun t : ℝ => sechSq t) volume (0 : ℝ) x :=
      cont_sechSq.intervalIntegrable 0 x
    have htanh : ∫ t in (0 : ℝ)..x, sechSq t = Real.tanh x := by
      have hd : ∀ z ∈ Set.uIcc (0 : ℝ) x, HasDerivAt Real.tanh (sechSq z) z :=
        fun z _ => tanhHasDerivAt z
      have h := intervalIntegral.integral_eq_sub_of_hasDerivAt hd hIntS
      simpa using h
    have hsub : ∫ t in (0 : ℝ)..x, (1 - sechSq t) = x - Real.tanh x := by
      rw [intervalIntegral.integral_sub (continuous_const.intervalIntegrable 0 x) hIntS, htanh]
      simp
    have hint_sq : ∫ t in (0 : ℝ)..x, t ^ 2 = x ^ 3 / 3 := by
      rw [integral_pow]
      norm_num
    have hmono : ∫ t in (0 : ℝ)..x, (1 - sechSq t) ≤ ∫ t in (0 : ℝ)..x, t ^ 2 := by
      refine intervalIntegral.integral_mono_on hx hIntA hIntB ?_
      intro t ht
      have hid : 1 - sechSq t = Real.tanh t ^ 2 := by
        rw [sechSq_eq_one_sub_tanh_sq]; ring
      rw [hid]
      rcases lt_or_eq_of_le ht.1 with ht0 | htz
      · have hp : 0 < Real.tanh t := tanh_pos_of_pos ht0
        have hltt : Real.tanh t < t := tanhLtSelf ht0
        nlinarith [hp, hltt, ht0]
      · subst htz
        simp [Real.tanh_zero]
    have hgap : x - Real.tanh x ≤ x ^ 3 / 3 := by
      rw [← hsub, ← hint_sq]
      exact hmono
    linarith
  · subst hzero
    simp
