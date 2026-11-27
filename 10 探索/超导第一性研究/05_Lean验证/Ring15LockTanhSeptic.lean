-- Ring15LockTanhSeptic.lean（第 221 轮）：$\tanh$ 的七阶下界。
-- 输入：v42 五阶上界 $S(t)=t-\frac{t^3}{3}+\frac{2t^5}{15}$、217 FTC 形 $\tanh s=s-\int\tanh^2$。
-- 路线：$\tanh^2\le S^2$，而 $S^2=t^2-\frac{2t^4}{3}+\frac{17t^6}{45}+\frac{4t^8}{45}\bigl(\frac{t^2}{5}-1\bigr)\le t^2-\frac{2t^4}{3}+\frac{17t^6}{45}$（$t\le1$），
-- 积分即得 $\tanh s\ge s-\frac{s^3}{3}+\frac{2s^5}{15}-\frac{17s^7}{315}$。
import Ring15Spec
import Ring15LockTanhTools
import Ring15LockTanhQuintic
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic

namespace CQM.Ring15.LockTanhSeptic

open MeasureTheory
open scoped Interval
open CQM.Ring15.Spec
open CQM.Ring15.LockTanhTools
open CQM.Ring15.LockTanhQuintic

/-- $\tanh s=s-\int_0^s\tanh^2$。 -/
theorem tanhEqSubIntegral (s : ℝ) :
    Real.tanh s = s - ∫ t in (0 : ℝ)..s, Real.tanh t ^ 2 := by
  have hs_int : IntervalIntegrable (fun t : ℝ => sechSq t) volume (0 : ℝ) s :=
    cont_sechSq.intervalIntegrable 0 s
  have htanh : ∫ t in (0 : ℝ)..s, sechSq t = Real.tanh s := by
    have hd : ∀ z ∈ Set.uIcc (0 : ℝ) s, HasDerivAt Real.tanh (sechSq z) z :=
      fun z _ => tanhHasDerivAt z
    have h := intervalIntegral.integral_eq_sub_of_hasDerivAt hd hs_int
    simpa using h
  have hcongr : ∫ t in (0 : ℝ)..s, Real.tanh t ^ 2 = ∫ t in (0 : ℝ)..s, (1 - sechSq t) := by
    refine intervalIntegral.integral_congr (fun t _ => ?_)
    rw [sechSq_eq_one_sub_tanh_sq]; ring
  have hIntOne : IntervalIntegrable (fun t : ℝ => 1 - sechSq t) volume (0 : ℝ) s :=
    (continuous_const.sub cont_sechSq).intervalIntegrable 0 s
  have hsub : ∫ t in (0 : ℝ)..s, (1 - sechSq t) = s - ∫ t in (0 : ℝ)..s, sechSq t := by
    rw [intervalIntegral.integral_sub (continuous_const.intervalIntegrable 0 s) hs_int]
    simp
  have hval : ∫ t in (0 : ℝ)..s, Real.tanh t ^ 2 = s - Real.tanh s := by
    rw [hcongr, hsub, htanh]
  linarith

/-- 三阶截断积分：$\int_0^s\bigl(t^2-\frac{2t^4}{3}+\frac{17t^6}{45}\bigr)
= \frac{s^3}{3}-\frac{2s^5}{15}+\frac{17s^7}{315}$。 -/
theorem integralTrunc (s : ℝ) :
    (∫ t in (0 : ℝ)..s, (t ^ 2 - 2 * t ^ 4 / 3 + 17 * t ^ 6 / 45))
      = s ^ 3 / 3 - 2 * s ^ 5 / 15 + 17 * s ^ 7 / 315 := by
  have h2 : IntervalIntegrable (fun t : ℝ => t ^ 2) volume (0 : ℝ) s :=
    (continuous_id.pow 2).intervalIntegrable 0 s
  have h4 : IntervalIntegrable (fun t : ℝ => 2 * t ^ 4 / 3) volume (0 : ℝ) s :=
    ((continuous_const.mul (continuous_id.pow 4)).div_const 3).intervalIntegrable 0 s
  have h6 : IntervalIntegrable (fun t : ℝ => 17 * t ^ 6 / 45) volume (0 : ℝ) s :=
    ((continuous_const.mul (continuous_id.pow 6)).div_const 45).intervalIntegrable 0 s
  have hAB : IntervalIntegrable (fun t : ℝ => t ^ 2 - 2 * t ^ 4 / 3) volume (0 : ℝ) s :=
    h2.sub h4
  have hABint : (∫ t in (0 : ℝ)..s, (t ^ 2 - 2 * t ^ 4 / 3))
      = (∫ t in (0 : ℝ)..s, t ^ 2) - ∫ t in (0 : ℝ)..s, 2 * t ^ 4 / 3 :=
    intervalIntegral.integral_sub h2 h4
  have hgoal : (∫ t in (0 : ℝ)..s, (t ^ 2 - 2 * t ^ 4 / 3 + 17 * t ^ 6 / 45))
      = (∫ t in (0 : ℝ)..s, (t ^ 2 - 2 * t ^ 4 / 3)) + ∫ t in (0 : ℝ)..s, 17 * t ^ 6 / 45 :=
    intervalIntegral.integral_add hAB h6
  rw [hgoal, hABint]
  have hq2 : (∫ t in (0 : ℝ)..s, t ^ 2) = s ^ 3 / 3 := by rw [integral_pow]; norm_num
  have hq4 : (∫ t in (0 : ℝ)..s, t ^ 4) = s ^ 5 / 5 := by rw [integral_pow]; norm_num
  have hq6 : (∫ t in (0 : ℝ)..s, t ^ 6) = s ^ 7 / 7 := by rw [integral_pow]; norm_num
  have hm4 : (∫ t in (0 : ℝ)..s, 2 * t ^ 4 / 3) = 2 * (∫ t in (0 : ℝ)..s, t ^ 4) / 3 := by
    rw [intervalIntegral.integral_div, intervalIntegral.integral_const_mul]
  have hm6 : (∫ t in (0 : ℝ)..s, 17 * t ^ 6 / 45) = 17 * (∫ t in (0 : ℝ)..s, t ^ 6) / 45 := by
    rw [intervalIntegral.integral_div, intervalIntegral.integral_const_mul]
  rw [hq2, hm4, hq4, hm6, hq6]
  ring

/-- **本环主定理**：$0\le s\le1$ 时 $\tanh s\ge s-\frac{s^3}{3}+\frac{2s^5}{15}-\frac{17s^7}{315}$。 -/
theorem tanhSepticLower (s : ℝ) (hs0 : 0 ≤ s) (hs1 : s ≤ 1) :
    s - s ^ 3 / 3 + 2 * s ^ 5 / 15 - 17 * s ^ 7 / 315 ≤ Real.tanh s := by
  have htanh : Real.tanh s = s - ∫ t in (0 : ℝ)..s, Real.tanh t ^ 2 := tanhEqSubIntegral s
  have hcontS : Continuous fun t : ℝ => t ^ 2 - 2 * t ^ 4 / 3 + 17 * t ^ 6 / 45 := by fun_prop
  have hIntS : IntervalIntegrable (fun t : ℝ => t ^ 2 - 2 * t ^ 4 / 3 + 17 * t ^ 6 / 45)
      volume (0 : ℝ) s := hcontS.intervalIntegrable 0 s
  have hIntT : IntervalIntegrable (fun t : ℝ => Real.tanh t ^ 2) volume (0 : ℝ) s :=
    (continuous_tanh.pow 2).intervalIntegrable 0 s
  have hmono : (∫ t in (0 : ℝ)..s, Real.tanh t ^ 2)
      ≤ ∫ t in (0 : ℝ)..s, (t ^ 2 - 2 * t ^ 4 / 3 + 17 * t ^ 6 / 45) := by
    refine intervalIntegral.integral_mono_on hs0 hIntT hIntS ?_
    intro t ht
    have ht0 : 0 ≤ t := ht.1
    have ht1 : t ≤ 1 := le_trans ht.2 hs1
    have hq := targetPropTanhQuintic t ht0 ht1
    have ht2 : t ^ 2 ≤ 1 := by nlinarith [ht0, ht1]
    have hnonnegTanh : 0 ≤ Real.tanh t := by
      rcases eq_or_lt_of_le ht0 with h | h
      · rw [← h]; simp
      · exact le_of_lt (tanh_pos_of_pos h)
    have hsq : Real.tanh t ^ 2 ≤ (t - t ^ 3 / 3 + 2 * t ^ 5 / 15) ^ 2 := by
      simpa [pow_two] using mul_self_le_mul_self hnonnegTanh hq
    have hexp : (t - t ^ 3 / 3 + 2 * t ^ 5 / 15) ^ 2
        = (t ^ 2 - 2 * t ^ 4 / 3 + 17 * t ^ 6 / 45) + 4 * t ^ 8 / 45 * (t ^ 2 / 5 - 1) := by
      ring
    have hneg : 4 * t ^ 8 / 45 * (t ^ 2 / 5 - 1) ≤ 0 := by
      have h8 : 0 ≤ 4 * t ^ 8 / 45 := by positivity
      have ht5 : t ^ 2 / 5 - 1 ≤ 0 := by nlinarith [ht2]
      nlinarith [h8, ht5]
    calc Real.tanh t ^ 2 ≤ (t - t ^ 3 / 3 + 2 * t ^ 5 / 15) ^ 2 := hsq
      _ = (t ^ 2 - 2 * t ^ 4 / 3 + 17 * t ^ 6 / 45) + 4 * t ^ 8 / 45 * (t ^ 2 / 5 - 1) := hexp
      _ ≤ t ^ 2 - 2 * t ^ 4 / 3 + 17 * t ^ 6 / 45 := by linarith
  have hval : (∫ t in (0 : ℝ)..s, (t ^ 2 - 2 * t ^ 4 / 3 + 17 * t ^ 6 / 45))
      = s ^ 3 / 3 - 2 * s ^ 5 / 15 + 17 * s ^ 7 / 315 := integralTrunc s
  have hmono' : (∫ t in (0 : ℝ)..s, Real.tanh t ^ 2)
      ≤ s ^ 3 / 3 - 2 * s ^ 5 / 15 + 17 * s ^ 7 / 315 := by
    rw [← hval]
    exact hmono
  linarith [htanh, hmono']

/-- **Spec 对齐版**（主定理名按目录规范）。 -/
theorem targetPropTanhSepticLower : CQM.Ring15.Spec.TargetPropTanhSepticLower := by
  intro s hs0 hs1
  exact tanhSepticLower s hs0 hs1
