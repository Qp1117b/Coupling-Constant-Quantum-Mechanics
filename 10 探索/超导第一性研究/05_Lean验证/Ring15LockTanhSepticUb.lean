-- Ring15LockTanhSepticUb.lean（第 222 轮）：$\tanh$ 的七阶上界。
-- 输入：v44 七阶下界 $P$、v42 五阶上界 $S_2$、217 FTC 形 $\tanh s=s-\int\tanh^2$。
-- 路线：$\tanh^2\ge P^2$，而 $P=S_2-\frac{17t^7}{315}$、$S_2\le t$ ⇒
--   $P^2=S_2^2-\frac{34t^8}{315}+\bigl(\frac{17t^7}{315}\bigr)^2\ \ge\ S_2^2-\frac{34t^8}{315}$，
-- 积分得 $\int\tanh^2\ge\frac{s^3}{3}-\frac{2s^5}{15}+\frac{17s^7}{315}-\frac{62s^9}{2835}+\frac{4s^{11}}{2475}$，
-- 故 $\tanh s\le s-\bigl(\frac{s^3}{3}-\frac{2s^5}{15}+\frac{17s^7}{315}-\frac{62s^9}{2835}\bigr)$。
import Ring15Spec
import Ring15LockTanhTools
import Ring15LockTanhQuintic
import Ring15LockTanhSeptic
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic

namespace CQM.Ring15.LockTanhSepticUb

open MeasureTheory
open scoped Interval
open CQM.Ring15.Spec
open CQM.Ring15.LockTanhTools
open CQM.Ring15.LockTanhQuintic
open CQM.Ring15.LockTanhSeptic

/-- 五阶上界平方的积分：$\int_0^s\bigl(t^2-\frac{2t^4}{3}+\frac{17t^6}{45}-\frac{4t^8}{45}+\frac{4t^{10}}{225}\bigr)
=\frac{s^3}{3}-\frac{2s^5}{15}+\frac{17s^7}{315}-\frac{4s^9}{405}+\frac{4s^{11}}{2475}$。 -/
theorem integralFive (s : ℝ) :
    (∫ t in (0 : ℝ)..s, (t ^ 2 - 2 * t ^ 4 / 3 + 17 * t ^ 6 / 45 - 4 * t ^ 8 / 45 + 4 * t ^ 10 / 225))
      = s ^ 3 / 3 - 2 * s ^ 5 / 15 + 17 * s ^ 7 / 315 - 4 * s ^ 9 / 405 + 4 * s ^ 11 / 2475 := by
  have h2 : IntervalIntegrable (fun t : ℝ => t ^ 2) volume (0 : ℝ) s :=
    (continuous_id.pow 2).intervalIntegrable 0 s
  have h4 : IntervalIntegrable (fun t : ℝ => 2 * t ^ 4 / 3) volume (0 : ℝ) s :=
    ((continuous_const.mul (continuous_id.pow 4)).div_const 3).intervalIntegrable 0 s
  have h6 : IntervalIntegrable (fun t : ℝ => 17 * t ^ 6 / 45) volume (0 : ℝ) s :=
    ((continuous_const.mul (continuous_id.pow 6)).div_const 45).intervalIntegrable 0 s
  have h8 : IntervalIntegrable (fun t : ℝ => 4 * t ^ 8 / 45) volume (0 : ℝ) s :=
    ((continuous_const.mul (continuous_id.pow 8)).div_const 45).intervalIntegrable 0 s
  have h10 : IntervalIntegrable (fun t : ℝ => 4 * t ^ 10 / 225) volume (0 : ℝ) s :=
    ((continuous_const.mul (continuous_id.pow 10)).div_const 225).intervalIntegrable 0 s
  have hA : IntervalIntegrable (fun t : ℝ => t ^ 2 - 2 * t ^ 4 / 3) volume (0 : ℝ) s :=
    h2.sub h4
  have hB : IntervalIntegrable (fun t : ℝ => (t ^ 2 - 2 * t ^ 4 / 3) + 17 * t ^ 6 / 45)
      volume (0 : ℝ) s := hA.add h6
  have hC : IntervalIntegrable (fun t : ℝ => ((t ^ 2 - 2 * t ^ 4 / 3) + 17 * t ^ 6 / 45) - 4 * t ^ 8 / 45)
      volume (0 : ℝ) s := hB.sub h8
  have e1 : (∫ t in (0 : ℝ)..s, (t ^ 2 - 2 * t ^ 4 / 3))
      = (∫ t in (0 : ℝ)..s, t ^ 2) - ∫ t in (0 : ℝ)..s, 2 * t ^ 4 / 3 :=
    intervalIntegral.integral_sub h2 h4
  have e2 : (∫ t in (0 : ℝ)..s, (t ^ 2 - 2 * t ^ 4 / 3 + 17 * t ^ 6 / 45))
      = (∫ t in (0 : ℝ)..s, (t ^ 2 - 2 * t ^ 4 / 3)) + ∫ t in (0 : ℝ)..s, 17 * t ^ 6 / 45 :=
    intervalIntegral.integral_add hA h6
  have e3 : (∫ t in (0 : ℝ)..s, (t ^ 2 - 2 * t ^ 4 / 3 + 17 * t ^ 6 / 45 - 4 * t ^ 8 / 45))
      = (∫ t in (0 : ℝ)..s, (t ^ 2 - 2 * t ^ 4 / 3 + 17 * t ^ 6 / 45))
        - ∫ t in (0 : ℝ)..s, 4 * t ^ 8 / 45 :=
    intervalIntegral.integral_sub hB h8
  have e4 : (∫ t in (0 : ℝ)..s,
        (t ^ 2 - 2 * t ^ 4 / 3 + 17 * t ^ 6 / 45 - 4 * t ^ 8 / 45 + 4 * t ^ 10 / 225))
      = (∫ t in (0 : ℝ)..s, (t ^ 2 - 2 * t ^ 4 / 3 + 17 * t ^ 6 / 45 - 4 * t ^ 8 / 45))
        + ∫ t in (0 : ℝ)..s, 4 * t ^ 10 / 225 :=
    intervalIntegral.integral_add hC h10
  rw [e4, e3, e2, e1]
  have hq2 : (∫ t in (0 : ℝ)..s, t ^ 2) = s ^ 3 / 3 := by rw [integral_pow]; norm_num
  have hq4 : (∫ t in (0 : ℝ)..s, t ^ 4) = s ^ 5 / 5 := by rw [integral_pow]; norm_num
  have hq6 : (∫ t in (0 : ℝ)..s, t ^ 6) = s ^ 7 / 7 := by rw [integral_pow]; norm_num
  have hq8 : (∫ t in (0 : ℝ)..s, t ^ 8) = s ^ 9 / 9 := by rw [integral_pow]; norm_num
  have hq10 : (∫ t in (0 : ℝ)..s, t ^ 10) = s ^ 11 / 11 := by rw [integral_pow]; norm_num
  have hm4 : (∫ t in (0 : ℝ)..s, 2 * t ^ 4 / 3) = 2 * (∫ t in (0 : ℝ)..s, t ^ 4) / 3 := by
    rw [intervalIntegral.integral_div, intervalIntegral.integral_const_mul]
  have hm6 : (∫ t in (0 : ℝ)..s, 17 * t ^ 6 / 45) = 17 * (∫ t in (0 : ℝ)..s, t ^ 6) / 45 := by
    rw [intervalIntegral.integral_div, intervalIntegral.integral_const_mul]
  have hm8 : (∫ t in (0 : ℝ)..s, 4 * t ^ 8 / 45) = 4 * (∫ t in (0 : ℝ)..s, t ^ 8) / 45 := by
    rw [intervalIntegral.integral_div, intervalIntegral.integral_const_mul]
  have hm10 : (∫ t in (0 : ℝ)..s, 4 * t ^ 10 / 225) = 4 * (∫ t in (0 : ℝ)..s, t ^ 10) / 225 := by
    rw [intervalIntegral.integral_div, intervalIntegral.integral_const_mul]
  rw [hq2, hm4, hq4, hm6, hq6, hm8, hq8, hm10, hq10]
  ring

/-- **本环主定理**：$0\le s\le1$ 时
$\tanh s\le s-\frac{s^3}{3}+\frac{2s^5}{15}-\frac{17s^7}{315}+\frac{62s^9}{2835}$。 -/
theorem tanhSepticUpper (s : ℝ) (hs0 : 0 ≤ s) (hs1 : s ≤ 1) :
    Real.tanh s ≤ s - s ^ 3 / 3 + 2 * s ^ 5 / 15 - 17 * s ^ 7 / 315 + 62 * s ^ 9 / 2835 := by
  have htanh : Real.tanh s = s - ∫ t in (0 : ℝ)..s, Real.tanh t ^ 2 := tanhEqSubIntegral s
  -- 点态：$P^2\ge S_2^2-\frac{34t^8}{315}$，$P\le\tanh$ ⇒ $P^2\le\tanh^2$
  have hcontF : Continuous fun t : ℝ =>
      ((t - t ^ 3 / 3 + 2 * t ^ 5 / 15) ^ 2 - 34 * t ^ 8 / 315) := by fun_prop
  have hIntF : IntervalIntegrable
      (fun t : ℝ => ((t - t ^ 3 / 3 + 2 * t ^ 5 / 15) ^ 2 - 34 * t ^ 8 / 315))
      volume (0 : ℝ) s := hcontF.intervalIntegrable 0 s
  have hIntT : IntervalIntegrable (fun t : ℝ => Real.tanh t ^ 2) volume (0 : ℝ) s :=
    (continuous_tanh.pow 2).intervalIntegrable 0 s
  have hmono : (∫ t in (0 : ℝ)..s,
        ((t - t ^ 3 / 3 + 2 * t ^ 5 / 15) ^ 2 - 34 * t ^ 8 / 315))
      ≤ ∫ t in (0 : ℝ)..s, Real.tanh t ^ 2 := by
    refine intervalIntegral.integral_mono_on hs0 hIntF hIntT ?_
    intro t ht
    have ht0 : 0 ≤ t := ht.1
    have ht1 : t ≤ 1 := le_trans ht.2 hs1
    have hP_le : t - t ^ 3 / 3 + 2 * t ^ 5 / 15 - 17 * t ^ 7 / 315 ≤ Real.tanh t :=
      tanhSepticLower t ht0 ht1
    have ht2 : t ^ 2 ≤ 1 := by nlinarith [ht0, ht1]
    -- P ≥ 0：$t-\frac{t^3}{3}\ge0$ 且 $\frac{2t^5}{15}\ge\frac{17t^7}{315}$
    have hp5 : 0 ≤ t - t ^ 3 / 3 := by nlinarith [ht0, ht2]
    have hcmp : 17 * t ^ 7 / 315 ≤ 2 * t ^ 5 / 15 := by
      have ht5 : 0 ≤ t ^ 5 := pow_nonneg ht0 5
      have h7 : t ^ 7 ≤ t ^ 5 := by nlinarith [ht5, ht2]
      nlinarith [h7, ht5]
    have hPpos : 0 ≤ t - t ^ 3 / 3 + 2 * t ^ 5 / 15 - 17 * t ^ 7 / 315 := by
      linarith [hp5, hcmp]
    -- P^2 = S2^2 - 2*S2*C + C^2 ≥ S2^2 - 2*t*C = S2^2 - 34 t^8/315
    have hS2pos : 0 ≤ t - t ^ 3 / 3 + 2 * t ^ 5 / 15 := by
      linarith [hp5, pow_nonneg ht0 5]
    have hS2le : t - t ^ 3 / 3 + 2 * t ^ 5 / 15 ≤ t := by
      have h3 : 0 ≤ t ^ 3 / 3 := by positivity
      have h5 : 0 ≤ 2 * t ^ 5 / 15 := by positivity
      nlinarith [ht2, h5, pow_nonneg ht0 3]
    have hC : 0 ≤ 17 * t ^ 7 / 315 := by positivity
    have hmon : (t - t ^ 3 / 3 + 2 * t ^ 5 / 15) * (17 * t ^ 7 / 315) ≤ t * (17 * t ^ 7 / 315) :=
      mul_le_mul_of_nonneg_right hS2le hC
    have hexp : (t - t ^ 3 / 3 + 2 * t ^ 5 / 15 - 17 * t ^ 7 / 315) ^ 2
        = (t - t ^ 3 / 3 + 2 * t ^ 5 / 15) ^ 2
          - 2 * ((t - t ^ 3 / 3 + 2 * t ^ 5 / 15) * (17 * t ^ 7 / 315))
          + (17 * t ^ 7 / 315) ^ 2 := by
      ring
    have hP2 : (t - t ^ 3 / 3 + 2 * t ^ 5 / 15) ^ 2 - 34 * t ^ 8 / 315
        ≤ (t - t ^ 3 / 3 + 2 * t ^ 5 / 15 - 17 * t ^ 7 / 315) ^ 2 := by
      have hsq : 0 ≤ (17 * t ^ 7 / 315) ^ 2 := sq_nonneg _
      -- 2*S2*C ≤ 2*t*C = 34 t^8/315
      have h2mon : 2 * ((t - t ^ 3 / 3 + 2 * t ^ 5 / 15) * (17 * t ^ 7 / 315))
          ≤ 34 * t ^ 8 / 315 := by
        have := mul_le_mul_of_nonneg_left hmon (by norm_num : (0 : ℝ) ≤ 2)
        calc 2 * ((t - t ^ 3 / 3 + 2 * t ^ 5 / 15) * (17 * t ^ 7 / 315))
            = 2 * ((t - t ^ 3 / 3 + 2 * t ^ 5 / 15) * (17 * t ^ 7 / 315)) := rfl
          _ ≤ 2 * (t * (17 * t ^ 7 / 315)) := this
          _ = 34 * t ^ 8 / 315 := by ring
      linarith [hexp, hsq, h2mon]
    have htanh_nonneg : 0 ≤ Real.tanh t := by
      rcases eq_or_lt_of_le ht0 with h | h
      · rw [← h]; simp
      · exact le_of_lt (tanh_pos_of_pos h)
    have hP2le : (t - t ^ 3 / 3 + 2 * t ^ 5 / 15 - 17 * t ^ 7 / 315) ^ 2 ≤ Real.tanh t ^ 2 := by
      simpa [pow_two] using mul_self_le_mul_self hPpos hP_le
    linarith [hP2, hP2le]
  -- 积分值的合成
  have hval5 : (∫ t in (0 : ℝ)..s,
        (t ^ 2 - 2 * t ^ 4 / 3 + 17 * t ^ 6 / 45 - 4 * t ^ 8 / 45 + 4 * t ^ 10 / 225))
      = s ^ 3 / 3 - 2 * s ^ 5 / 15 + 17 * s ^ 7 / 315 - 4 * s ^ 9 / 405 + 4 * s ^ 11 / 2475 :=
    integralFive s
  -- S2^2 展开成五项
  have hcongr : (∫ t in (0 : ℝ)..s, (t - t ^ 3 / 3 + 2 * t ^ 5 / 15) ^ 2)
      = ∫ t in (0 : ℝ)..s,
          (t ^ 2 - 2 * t ^ 4 / 3 + 17 * t ^ 6 / 45 - 4 * t ^ 8 / 45 + 4 * t ^ 10 / 225) := by
    refine intervalIntegral.integral_congr (fun t _ => ?_)
    ring
  have hInt8 : (∫ t in (0 : ℝ)..s, t ^ 8) = s ^ 9 / 9 := by
    rw [integral_pow]; norm_num
  have hIntC : IntervalIntegrable (fun t : ℝ => 34 * t ^ 8 / 315) volume (0 : ℝ) s :=
    ((continuous_const.mul (continuous_id.pow 8)).div_const 315).intervalIntegrable 0 s
  have hScont : Continuous fun t : ℝ => (t - t ^ 3 / 3 + 2 * t ^ 5 / 15) ^ 2 := by fun_prop
  have hS : IntervalIntegrable (fun t : ℝ => (t - t ^ 3 / 3 + 2 * t ^ 5 / 15) ^ 2)
      volume (0 : ℝ) s := hScont.intervalIntegrable 0 s
  have hsplit : (∫ t in (0 : ℝ)..s, ((t - t ^ 3 / 3 + 2 * t ^ 5 / 15) ^ 2 - 34 * t ^ 8 / 315))
      = (∫ t in (0 : ℝ)..s, (t - t ^ 3 / 3 + 2 * t ^ 5 / 15) ^ 2) - 34 * s ^ 9 / 2835 := by
    rw [intervalIntegral.integral_sub hS hIntC]
    have hm : (∫ t in (0 : ℝ)..s, 34 * t ^ 8 / 315) = 34 * (∫ t in (0 : ℝ)..s, t ^ 8) / 315 := by
      rw [intervalIntegral.integral_div, intervalIntegral.integral_const_mul]
    rw [hm, hInt8]
    ring
  rw [hsplit] at hmono
  rw [hcongr, hval5] at hmono
  have hmono' : s ^ 3 / 3 - 2 * s ^ 5 / 15 + 17 * s ^ 7 / 315 - 4 * s ^ 9 / 405 + 4 * s ^ 11 / 2475
      - 34 * s ^ 9 / 2835 ≤ ∫ t in (0 : ℝ)..s, Real.tanh t ^ 2 := by
    linarith [hmono]
  have htail : s ^ 3 / 3 - 2 * s ^ 5 / 15 + 17 * s ^ 7 / 315 - 62 * s ^ 9 / 2835
      ≤ s ^ 3 / 3 - 2 * s ^ 5 / 15 + 17 * s ^ 7 / 315 - 4 * s ^ 9 / 405 + 4 * s ^ 11 / 2475
        - 34 * s ^ 9 / 2835 := by
    have hs11 : 0 ≤ s ^ 11 := pow_nonneg hs0 11
    nlinarith [hs11]
  linarith [htanh, hmono', htail]

/-- **Spec 对齐版**（主定理名按目录规范）。 -/
theorem targetPropTanhSeptic : CQM.Ring15.Spec.TargetPropTanhSeptic := by
  intro s hs0 hs1
  exact tanhSepticUpper s hs0 hs1
