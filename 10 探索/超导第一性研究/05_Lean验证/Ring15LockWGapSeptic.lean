-- Ring15LockWGapSeptic.lean（第 223 轮）：$w$ 的七阶双侧界（T ≥ 1/2）。
-- 输入：v44 七阶下界 $S_3$、v45 七阶上界 $S_4$（均在 $s\in[0,1]$）、`wGap` 的积分定义。
-- 路线：$u\in[0,1]$、$T\ge\frac12$ ⇒ $\frac{u}{2T}\in[0,1]$，逐点 $S_3\le\tanh\le S_4$，
--   乘 $2u\ge0$ 后 `integral_mono_on`，两支的积分闭式由逐项 `integral_pow` 给出。
import Ring15Spec
import Ring15LockTanhTools
import Ring15LockTanhSeptic
import Ring15LockTanhSepticUb
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic

namespace CQM.Ring15.LockWGapSeptic

open MeasureTheory
open scoped Interval
open CQM.Ring15.Spec
open CQM.Ring15.LockTanhTools
open CQM.Ring15.LockTanhSeptic
open CQM.Ring15.LockTanhSepticUb

/-- $\int_0^1 2u\,S_3\bigl(\frac{u}{2T}\bigr)du=\frac{1}{3T}-\frac{1}{60T^3}+\frac{1}{840T^5}-\frac{17}{181440T^7}$。 -/
theorem integralS3 (T : ℝ) (hT : 0 < T) :
    (∫ u in (0 : ℝ)..1,
        2 * u * (u / (2 * T) - (u / (2 * T)) ^ 3 / 3 + 2 * (u / (2 * T)) ^ 5 / 15
          - 17 * (u / (2 * T)) ^ 7 / 315))
      = 1 / (3 * T) - 1 / (60 * T ^ 3) + 1 / (840 * T ^ 5) - 17 / (181440 * T ^ 7) := by
  have hcongr : (∫ u in (0 : ℝ)..1,
        2 * u * (u / (2 * T) - (u / (2 * T)) ^ 3 / 3 + 2 * (u / (2 * T)) ^ 5 / 15
          - 17 * (u / (2 * T)) ^ 7 / 315))
      = ∫ u in (0 : ℝ)..1,
          (u ^ 2 / T - u ^ 4 / (12 * T ^ 3) + u ^ 6 / (120 * T ^ 5) - 17 * u ^ 8 / (20160 * T ^ 7)) := by
    refine intervalIntegral.integral_congr (fun u _ => ?_)
    field_simp
    ring
  rw [hcongr]
  have h2 : IntervalIntegrable (fun u : ℝ => u ^ 2 / T) volume (0 : ℝ) 1 :=
    ((continuous_id.pow 2).div_const T).intervalIntegrable 0 1
  have h4 : IntervalIntegrable (fun u : ℝ => u ^ 4 / (12 * T ^ 3)) volume (0 : ℝ) 1 :=
    ((continuous_id.pow 4).div_const (12 * T ^ 3)).intervalIntegrable 0 1
  have h6 : IntervalIntegrable (fun u : ℝ => u ^ 6 / (120 * T ^ 5)) volume (0 : ℝ) 1 :=
    ((continuous_id.pow 6).div_const (120 * T ^ 5)).intervalIntegrable 0 1
  have h8 : IntervalIntegrable (fun u : ℝ => 17 * u ^ 8 / (20160 * T ^ 7)) volume (0 : ℝ) 1 :=
    ((continuous_const.mul (continuous_id.pow 8)).div_const (20160 * T ^ 7)).intervalIntegrable 0 1
  have hA : IntervalIntegrable (fun u : ℝ => u ^ 2 / T - u ^ 4 / (12 * T ^ 3)) volume (0 : ℝ) 1 :=
    h2.sub h4
  have hB : IntervalIntegrable (fun u : ℝ => (u ^ 2 / T - u ^ 4 / (12 * T ^ 3)) + u ^ 6 / (120 * T ^ 5))
      volume (0 : ℝ) 1 := hA.add h6
  have e1 : (∫ u in (0 : ℝ)..1, (u ^ 2 / T - u ^ 4 / (12 * T ^ 3)))
      = (∫ u in (0 : ℝ)..1, u ^ 2 / T) - ∫ u in (0 : ℝ)..1, u ^ 4 / (12 * T ^ 3) :=
    intervalIntegral.integral_sub h2 h4
  have e2 : (∫ u in (0 : ℝ)..1, (u ^ 2 / T - u ^ 4 / (12 * T ^ 3) + u ^ 6 / (120 * T ^ 5)))
      = (∫ u in (0 : ℝ)..1, (u ^ 2 / T - u ^ 4 / (12 * T ^ 3)))
        + ∫ u in (0 : ℝ)..1, u ^ 6 / (120 * T ^ 5) :=
    intervalIntegral.integral_add hA h6
  have e3 : (∫ u in (0 : ℝ)..1,
        (u ^ 2 / T - u ^ 4 / (12 * T ^ 3) + u ^ 6 / (120 * T ^ 5) - 17 * u ^ 8 / (20160 * T ^ 7)))
      = (∫ u in (0 : ℝ)..1, (u ^ 2 / T - u ^ 4 / (12 * T ^ 3) + u ^ 6 / (120 * T ^ 5)))
        - ∫ u in (0 : ℝ)..1, 17 * u ^ 8 / (20160 * T ^ 7) :=
    intervalIntegral.integral_sub hB h8
  rw [e3, e2, e1]
  have hq2 : (∫ u in (0 : ℝ)..1, u ^ 2) = 1 / 3 := by
    rw [integral_pow]; norm_num
  have hq4 : (∫ u in (0 : ℝ)..1, u ^ 4) = 1 / 5 := by
    rw [integral_pow]; norm_num
  have hq6 : (∫ u in (0 : ℝ)..1, u ^ 6) = 1 / 7 := by
    rw [integral_pow]; norm_num
  have hq8 : (∫ u in (0 : ℝ)..1, u ^ 8) = 1 / 9 := by
    rw [integral_pow]; norm_num
  have hm2 : (∫ u in (0 : ℝ)..1, u ^ 2 / T) = (∫ u in (0 : ℝ)..1, u ^ 2) / T := by
    rw [intervalIntegral.integral_div]
  have hm4 : (∫ u in (0 : ℝ)..1, u ^ 4 / (12 * T ^ 3))
      = (∫ u in (0 : ℝ)..1, u ^ 4) / (12 * T ^ 3) := by
    rw [intervalIntegral.integral_div]
  have hm6 : (∫ u in (0 : ℝ)..1, u ^ 6 / (120 * T ^ 5))
      = (∫ u in (0 : ℝ)..1, u ^ 6) / (120 * T ^ 5) := by
    rw [intervalIntegral.integral_div]
  have hm8 : (∫ u in (0 : ℝ)..1, 17 * u ^ 8 / (20160 * T ^ 7))
      = 17 * (∫ u in (0 : ℝ)..1, u ^ 8) / (20160 * T ^ 7) := by
    rw [intervalIntegral.integral_div, intervalIntegral.integral_const_mul]
  rw [hm2, hq2, hm4, hq4, hm6, hq6, hm8, hq8]
  field_simp
  ring

/-- $\int_0^1 2u\,S_4\bigl(\frac{u}{2T}\bigr)du=\frac{1}{3T}-\frac{1}{60T^3}+\frac{1}{840T^5}-\frac{17}{181440T^7}+\frac{31}{3991680T^9}$。 -/
theorem integralS4 (T : ℝ) (hT : 0 < T) :
    (∫ u in (0 : ℝ)..1,
        2 * u * (u / (2 * T) - (u / (2 * T)) ^ 3 / 3 + 2 * (u / (2 * T)) ^ 5 / 15
          - 17 * (u / (2 * T)) ^ 7 / 315 + 62 * (u / (2 * T)) ^ 9 / 2835))
      = 1 / (3 * T) - 1 / (60 * T ^ 3) + 1 / (840 * T ^ 5) - 17 / (181440 * T ^ 7)
        + 31 / (3991680 * T ^ 9) := by
  have hcongr : (∫ u in (0 : ℝ)..1,
        2 * u * (u / (2 * T) - (u / (2 * T)) ^ 3 / 3 + 2 * (u / (2 * T)) ^ 5 / 15
          - 17 * (u / (2 * T)) ^ 7 / 315 + 62 * (u / (2 * T)) ^ 9 / 2835))
      = ∫ u in (0 : ℝ)..1,
          (u ^ 2 / T - u ^ 4 / (12 * T ^ 3) + u ^ 6 / (120 * T ^ 5) - 17 * u ^ 8 / (20160 * T ^ 7)
            + 31 * u ^ 10 / (362880 * T ^ 9)) := by
    refine intervalIntegral.integral_congr (fun u _ => ?_)
    field_simp
    ring
  rw [hcongr]
  have h2 : IntervalIntegrable (fun u : ℝ => u ^ 2 / T) volume (0 : ℝ) 1 :=
    ((continuous_id.pow 2).div_const T).intervalIntegrable 0 1
  have h4 : IntervalIntegrable (fun u : ℝ => u ^ 4 / (12 * T ^ 3)) volume (0 : ℝ) 1 :=
    ((continuous_id.pow 4).div_const (12 * T ^ 3)).intervalIntegrable 0 1
  have h6 : IntervalIntegrable (fun u : ℝ => u ^ 6 / (120 * T ^ 5)) volume (0 : ℝ) 1 :=
    ((continuous_id.pow 6).div_const (120 * T ^ 5)).intervalIntegrable 0 1
  have h8 : IntervalIntegrable (fun u : ℝ => 17 * u ^ 8 / (20160 * T ^ 7)) volume (0 : ℝ) 1 :=
    ((continuous_const.mul (continuous_id.pow 8)).div_const (20160 * T ^ 7)).intervalIntegrable 0 1
  have h10 : IntervalIntegrable (fun u : ℝ => 31 * u ^ 10 / (362880 * T ^ 9)) volume (0 : ℝ) 1 :=
    ((continuous_const.mul (continuous_id.pow 10)).div_const (362880 * T ^ 9)).intervalIntegrable 0 1
  have hA : IntervalIntegrable (fun u : ℝ => u ^ 2 / T - u ^ 4 / (12 * T ^ 3)) volume (0 : ℝ) 1 :=
    h2.sub h4
  have hB : IntervalIntegrable (fun u : ℝ => (u ^ 2 / T - u ^ 4 / (12 * T ^ 3)) + u ^ 6 / (120 * T ^ 5))
      volume (0 : ℝ) 1 := hA.add h6
  have hC : IntervalIntegrable
      (fun u : ℝ => ((u ^ 2 / T - u ^ 4 / (12 * T ^ 3)) + u ^ 6 / (120 * T ^ 5)) - 17 * u ^ 8 / (20160 * T ^ 7))
      volume (0 : ℝ) 1 := hB.sub h8
  have e1 : (∫ u in (0 : ℝ)..1, (u ^ 2 / T - u ^ 4 / (12 * T ^ 3)))
      = (∫ u in (0 : ℝ)..1, u ^ 2 / T) - ∫ u in (0 : ℝ)..1, u ^ 4 / (12 * T ^ 3) :=
    intervalIntegral.integral_sub h2 h4
  have e2 : (∫ u in (0 : ℝ)..1, (u ^ 2 / T - u ^ 4 / (12 * T ^ 3) + u ^ 6 / (120 * T ^ 5)))
      = (∫ u in (0 : ℝ)..1, (u ^ 2 / T - u ^ 4 / (12 * T ^ 3)))
        + ∫ u in (0 : ℝ)..1, u ^ 6 / (120 * T ^ 5) :=
    intervalIntegral.integral_add hA h6
  have e3 : (∫ u in (0 : ℝ)..1,
        (u ^ 2 / T - u ^ 4 / (12 * T ^ 3) + u ^ 6 / (120 * T ^ 5) - 17 * u ^ 8 / (20160 * T ^ 7)))
      = (∫ u in (0 : ℝ)..1, (u ^ 2 / T - u ^ 4 / (12 * T ^ 3) + u ^ 6 / (120 * T ^ 5)))
        - ∫ u in (0 : ℝ)..1, 17 * u ^ 8 / (20160 * T ^ 7) :=
    intervalIntegral.integral_sub hB h8
  have e4 : (∫ u in (0 : ℝ)..1,
        (u ^ 2 / T - u ^ 4 / (12 * T ^ 3) + u ^ 6 / (120 * T ^ 5) - 17 * u ^ 8 / (20160 * T ^ 7)
          + 31 * u ^ 10 / (362880 * T ^ 9)))
      = (∫ u in (0 : ℝ)..1,
          (u ^ 2 / T - u ^ 4 / (12 * T ^ 3) + u ^ 6 / (120 * T ^ 5) - 17 * u ^ 8 / (20160 * T ^ 7)))
        + ∫ u in (0 : ℝ)..1, 31 * u ^ 10 / (362880 * T ^ 9) :=
    intervalIntegral.integral_add hC h10
  rw [e4, e3, e2, e1]
  have hq2 : (∫ u in (0 : ℝ)..1, u ^ 2) = 1 / 3 := by rw [integral_pow]; norm_num
  have hq4 : (∫ u in (0 : ℝ)..1, u ^ 4) = 1 / 5 := by rw [integral_pow]; norm_num
  have hq6 : (∫ u in (0 : ℝ)..1, u ^ 6) = 1 / 7 := by rw [integral_pow]; norm_num
  have hq8 : (∫ u in (0 : ℝ)..1, u ^ 8) = 1 / 9 := by rw [integral_pow]; norm_num
  have hq10 : (∫ u in (0 : ℝ)..1, u ^ 10) = 1 / 11 := by rw [integral_pow]; norm_num
  have hm2 : (∫ u in (0 : ℝ)..1, u ^ 2 / T) = (∫ u in (0 : ℝ)..1, u ^ 2) / T := by
    rw [intervalIntegral.integral_div]
  have hm4 : (∫ u in (0 : ℝ)..1, u ^ 4 / (12 * T ^ 3))
      = (∫ u in (0 : ℝ)..1, u ^ 4) / (12 * T ^ 3) := by rw [intervalIntegral.integral_div]
  have hm6 : (∫ u in (0 : ℝ)..1, u ^ 6 / (120 * T ^ 5))
      = (∫ u in (0 : ℝ)..1, u ^ 6) / (120 * T ^ 5) := by rw [intervalIntegral.integral_div]
  have hm8 : (∫ u in (0 : ℝ)..1, 17 * u ^ 8 / (20160 * T ^ 7))
      = 17 * (∫ u in (0 : ℝ)..1, u ^ 8) / (20160 * T ^ 7) := by
    rw [intervalIntegral.integral_div, intervalIntegral.integral_const_mul]
  have hm10 : (∫ u in (0 : ℝ)..1, 31 * u ^ 10 / (362880 * T ^ 9))
      = 31 * (∫ u in (0 : ℝ)..1, u ^ 10) / (362880 * T ^ 9) := by
    rw [intervalIntegral.integral_div, intervalIntegral.integral_const_mul]
  rw [hm2, hq2, hm4, hq4, hm6, hq6, hm8, hq8, hm10, hq10]
  field_simp
  ring

/-- **本环主定理（下界）**：$T\ge\frac12$ 时 $w_{\rm lb}(T)\le w(T)$。 -/
theorem wGapLowerBound (T : ℝ) (hT : 1 / 2 ≤ T) :
    wGapLowerSeptic T ≤ wGap T := by
  have hpos : 0 < T := by linarith
  have hcongr : wGap T = ∫ u in (0 : ℝ)..1, 2 * u * Real.tanh (u / (2 * T)) := rfl
  have hcontA : Continuous fun u : ℝ =>
      2 * u * (u / (2 * T) - (u / (2 * T)) ^ 3 / 3 + 2 * (u / (2 * T)) ^ 5 / 15
        - 17 * (u / (2 * T)) ^ 7 / 315) := by fun_prop
  have hcontB : Continuous fun u : ℝ => 2 * u * Real.tanh (u / (2 * T)) :=
  (continuous_const.mul continuous_id).mul
    (continuous_tanh.comp (continuous_id.div_const (2 * T)))
  have hIntA : IntervalIntegrable
      (fun u : ℝ => 2 * u * (u / (2 * T) - (u / (2 * T)) ^ 3 / 3 + 2 * (u / (2 * T)) ^ 5 / 15
        - 17 * (u / (2 * T)) ^ 7 / 315)) volume (0 : ℝ) 1 := hcontA.intervalIntegrable 0 1
  have hIntB : IntervalIntegrable (fun u : ℝ => 2 * u * Real.tanh (u / (2 * T)))
      volume (0 : ℝ) 1 := hcontB.intervalIntegrable 0 1
  have hmono : (∫ u in (0 : ℝ)..1,
        2 * u * (u / (2 * T) - (u / (2 * T)) ^ 3 / 3 + 2 * (u / (2 * T)) ^ 5 / 15
          - 17 * (u / (2 * T)) ^ 7 / 315))
      ≤ ∫ u in (0 : ℝ)..1, 2 * u * Real.tanh (u / (2 * T)) := by
    refine intervalIntegral.integral_mono_on (by norm_num : (0 : ℝ) ≤ 1) hIntA hIntB ?_
    intro u hu
    have hu0 : 0 ≤ u := hu.1
    have hu1 : u ≤ 1 := hu.2
    have hx0 : 0 ≤ u / (2 * T) := by positivity
    have hx1 : u / (2 * T) ≤ 1 := by
      rw [div_le_one (by linarith : (0 : ℝ) < 2 * T)]
      linarith
    have hS := tanhSepticLower (u / (2 * T)) hx0 hx1
    have h2u : 0 ≤ 2 * u := by positivity
    exact mul_le_mul_of_nonneg_left hS h2u
  have hval : (∫ u in (0 : ℝ)..1,
        2 * u * (u / (2 * T) - (u / (2 * T)) ^ 3 / 3 + 2 * (u / (2 * T)) ^ 5 / 15
          - 17 * (u / (2 * T)) ^ 7 / 315))
      = 1 / (3 * T) - 1 / (60 * T ^ 3) + 1 / (840 * T ^ 5) - 17 / (181440 * T ^ 7) :=
    integralS3 T hpos
  rw [hval, ← hcongr] at hmono
  simpa [wGapLowerSeptic] using hmono

/-- **本环主定理（上界）**：$T\ge\frac12$ 时 $w(T)\le w_{\rm ub}(T)$。 -/
theorem wGapUpperBound (T : ℝ) (hT : 1 / 2 ≤ T) :
    wGap T ≤ wGapUpperSeptic T := by
  have hpos : 0 < T := by linarith
  have hcongr : wGap T = ∫ u in (0 : ℝ)..1, 2 * u * Real.tanh (u / (2 * T)) := rfl
  have hcontA : Continuous fun u : ℝ => 2 * u * Real.tanh (u / (2 * T)) :=
  (continuous_const.mul continuous_id).mul
    (continuous_tanh.comp (continuous_id.div_const (2 * T)))
  have hcontB : Continuous fun u : ℝ =>
      2 * u * (u / (2 * T) - (u / (2 * T)) ^ 3 / 3 + 2 * (u / (2 * T)) ^ 5 / 15
        - 17 * (u / (2 * T)) ^ 7 / 315 + 62 * (u / (2 * T)) ^ 9 / 2835) := by fun_prop
  have hIntA : IntervalIntegrable (fun u : ℝ => 2 * u * Real.tanh (u / (2 * T)))
      volume (0 : ℝ) 1 := hcontA.intervalIntegrable 0 1
  have hIntB : IntervalIntegrable
      (fun u : ℝ => 2 * u * (u / (2 * T) - (u / (2 * T)) ^ 3 / 3 + 2 * (u / (2 * T)) ^ 5 / 15
        - 17 * (u / (2 * T)) ^ 7 / 315 + 62 * (u / (2 * T)) ^ 9 / 2835)) volume (0 : ℝ) 1 :=
    hcontB.intervalIntegrable 0 1
  have hmono : (∫ u in (0 : ℝ)..1, 2 * u * Real.tanh (u / (2 * T)))
      ≤ ∫ u in (0 : ℝ)..1,
          2 * u * (u / (2 * T) - (u / (2 * T)) ^ 3 / 3 + 2 * (u / (2 * T)) ^ 5 / 15
            - 17 * (u / (2 * T)) ^ 7 / 315 + 62 * (u / (2 * T)) ^ 9 / 2835) := by
    refine intervalIntegral.integral_mono_on (by norm_num : (0 : ℝ) ≤ 1) hIntA hIntB ?_
    intro u hu
    have hu0 : 0 ≤ u := hu.1
    have hu1 : u ≤ 1 := hu.2
    have hx0 : 0 ≤ u / (2 * T) := by positivity
    have hx1 : u / (2 * T) ≤ 1 := by
      rw [div_le_one (by linarith : (0 : ℝ) < 2 * T)]
      linarith
    have hS := tanhSepticUpper (u / (2 * T)) hx0 hx1
    have h2u : 0 ≤ 2 * u := by positivity
    exact mul_le_mul_of_nonneg_left hS h2u
  have hval : (∫ u in (0 : ℝ)..1,
        2 * u * (u / (2 * T) - (u / (2 * T)) ^ 3 / 3 + 2 * (u / (2 * T)) ^ 5 / 15
          - 17 * (u / (2 * T)) ^ 7 / 315 + 62 * (u / (2 * T)) ^ 9 / 2835))
      = 1 / (3 * T) - 1 / (60 * T ^ 3) + 1 / (840 * T ^ 5) - 17 / (181440 * T ^ 7)
        + 31 / (3991680 * T ^ 9) :=
    integralS4 T hpos
  rw [hval, ← hcongr] at hmono
  simpa [wGapUpperSeptic, wGapLowerSeptic] using hmono

/-- **Spec 对齐版（下界）**。 -/
theorem targetPropWGapLowerBound : CQM.Ring15.Spec.TargetPropWGapLowerBound := by
  intro T hT
  exact wGapLowerBound T hT

/-- **Spec 对齐版（上界）**。 -/
theorem targetPropWGapUpperBound : CQM.Ring15.Spec.TargetPropWGapUpperBound := by
  intro T hT
  exact wGapUpperBound T hT
