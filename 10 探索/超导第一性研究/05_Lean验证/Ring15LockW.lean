-- Ring15LockW.lean（第 190 轮）：$w(T)=2\int_0^1 u\tanh\frac{u}{2T}du$ 的正性、单调不增与上界。
-- 只 import Ring15Spec（＋基线里的积分基本定理与双曲导数），不 import 任何证明模块。
import Ring15Spec
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp

namespace CQM.Ring15.LockW

open MeasureTheory
open scoped Interval
open CQM.Ring15.Spec

private lemma continuous_tanh : Continuous Real.tanh := by
  have h : Continuous fun y : ℝ => Real.sinh y / Real.cosh y :=
    Real.continuous_sinh.div Real.continuous_cosh (fun y => (Real.cosh_pos y).ne')
  exact h.congr (fun y => (Real.tanh_eq_sinh_div_cosh y).symm)

private lemma hasDerivAt_tanh (x : ℝ) : HasDerivAt Real.tanh (1 / Real.cosh x ^ 2) x := by
  have hdiv : HasDerivAt (fun y : ℝ => Real.sinh y / Real.cosh y)
      ((Real.cosh x * Real.cosh x - Real.sinh x * Real.sinh x) / Real.cosh x ^ 2) x :=
    (Real.hasDerivAt_sinh x).div (Real.hasDerivAt_cosh x) (Real.cosh_pos x).ne'
  have hfun : (fun y : ℝ => Real.sinh y / Real.cosh y) = Real.tanh := by
    funext y; exact (Real.tanh_eq_sinh_div_cosh y).symm
  have hv : (Real.cosh x * Real.cosh x - Real.sinh x * Real.sinh x) / Real.cosh x ^ 2
      = 1 / Real.cosh x ^ 2 := by
    have hc : Real.cosh x ^ 2 = Real.sinh x ^ 2 + 1 := Real.cosh_sq x
    field_simp
    nlinarith [hc]
  rw [hfun, hv] at hdiv
  exact hdiv

private lemma tanh_strictMono : StrictMono Real.tanh := by
  refine strictMono_of_deriv_pos (fun x => ?_)
  rw [(hasDerivAt_tanh x).deriv]
  exact one_div_pos.mpr (pow_pos (Real.cosh_pos x) 2)

private lemma tanh_pos_of_pos {x : ℝ} (hx : 0 < x) : 0 < Real.tanh x := by
  have h := tanh_strictMono hx
  simpa [Real.tanh_zero] using h

private lemma tanh_nonneg_of_nonneg {x : ℝ} (hx : 0 ≤ x) : 0 ≤ Real.tanh x := by
  rcases lt_or_eq_of_le hx with h | h
  · exact (tanh_pos_of_pos h).le
  · subst h
    simp [Real.tanh_zero]

private lemma tanh_le_tanh {x y : ℝ} (h : x ≤ y) : Real.tanh x ≤ Real.tanh y :=
  tanh_strictMono.monotone h

private lemma cont_integrand (T : ℝ) :
    Continuous fun u : ℝ => 2 * u * Real.tanh (u / (2 * T)) := by
  refine (continuous_const.mul continuous_id).mul ?_
  exact continuous_tanh.comp (continuous_id.div_const (2 * T))

theorem targetPropWGapPos : CQM.Ring15.Spec.TargetPropWGapPos := by
  intro T hT
  refine intervalIntegral.integral_pos (a := (0 : ℝ)) (b := 1) (by norm_num)
    (cont_integrand T).continuousOn ?_ ?_
  · intro x hx
    have hx0 : 0 ≤ x := hx.1.le
    have harg : 0 ≤ x / (2 * T) := div_nonneg hx0 (by linarith)
    have ht : 0 ≤ Real.tanh (x / (2 * T)) := tanh_nonneg_of_nonneg harg
    have h2x : 0 ≤ 2 * x := by linarith
    exact mul_nonneg h2x ht
  · refine ⟨1, ⟨by norm_num, le_rfl⟩, ?_⟩
    have harg : 0 < (1 : ℝ) / (2 * T) := div_pos one_pos (by linarith)
    have ht : 0 < Real.tanh ((1 : ℝ) / (2 * T)) := tanh_pos_of_pos harg
    have h2 : 0 < 2 * (1 : ℝ) := by norm_num
    exact mul_pos h2 ht

theorem targetPropWGapAnti : CQM.Ring15.Spec.TargetPropWGapAnti := by
  intro T1 T2 h1 h12
  have hle : (0 : ℝ) ≤ 1 := by norm_num
  refine intervalIntegral.integral_mono_on hle
    ((cont_integrand T2).intervalIntegrable 0 1)
    ((cont_integrand T1).intervalIntegrable 0 1) ?_
  intro x hx
  have hx0 : 0 ≤ x := hx.1
  have h2T : 0 < 2 * T1 := by linarith
  have hden : 2 * T1 ≤ 2 * T2 := by linarith
  have harg : x / (2 * T2) ≤ x / (2 * T1) :=
    div_le_div_of_nonneg_left hx0 h2T hden
  have htanh : Real.tanh (x / (2 * T2)) ≤ Real.tanh (x / (2 * T1)) := tanh_le_tanh harg
  have h2x : 0 ≤ 2 * x := by linarith
  exact mul_le_mul_of_nonneg_left htanh h2x

theorem targetPropWGapLeOne : CQM.Ring15.Spec.TargetPropWGapLeOne := by
  intro T hT
  have hInt : ∫ u in (0 : ℝ)..1, (2 : ℝ) * u = 1 := by
    have hd : ∀ x ∈ Set.uIcc (0 : ℝ) 1, HasDerivAt (fun y : ℝ => y ^ 2) (2 * x) x := by
      intro x _
      simpa using (hasDerivAt_pow 2 x)
    have hcont : ContinuousOn (fun y : ℝ => y ^ 2) (Set.uIcc (0 : ℝ) 1) := by fun_prop
    have hder : IntervalIntegrable (fun u : ℝ => 2 * u) volume 0 1 :=
      (continuous_const.mul continuous_id).intervalIntegrable 0 1
    have := intervalIntegral.integral_eq_sub_of_hasDerivAt hd hder
    simpa using this
  calc wGap T ≤ ∫ u in (0 : ℝ)..1, (2 : ℝ) * u := by
        refine intervalIntegral.integral_mono_on (a := (0 : ℝ)) (b := 1) (by norm_num)
          ((cont_integrand T).intervalIntegrable 0 1)
          ((continuous_const.mul continuous_id).intervalIntegrable 0 1) ?_
        intro x hx
        have hx0 : 0 ≤ x := hx.1
        have h2x : 0 ≤ 2 * x := by linarith
        have ht : Real.tanh (x / (2 * T)) ≤ 1 := (Real.tanh_lt_one _).le
        simpa using mul_le_mul_of_nonneg_left ht h2x
    _ = 1 := hInt

end CQM.Ring15.LockW
