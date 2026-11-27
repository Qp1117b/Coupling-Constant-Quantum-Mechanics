-- Ring15LockSecant.lean（第 210 轮）：tanh 割线不等式 → δ≤1/3 → 尾段最终排除
-- 只 import Spec ＋已证模块 ＋基线库；无 sorry／admit／自造 axiom。
-- 内容：①tanh(au)≥u·tanh a（u∈[0,1]）；②δ(T)≤1/3；③T≥1 ⇒ D(T)<0。
import Ring15Spec
import Ring15LockIbp
import Ring15LockDeficit
import Ring15LockTailRatio
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.Analysis.Complex.Trigonometric

namespace CQM.Ring15.LockSecant

open MeasureTheory
open scoped Interval
open CQM.Ring15.Spec

noncomputable section

private lemma continuous_tanh : Continuous Real.tanh := by
  have h : Continuous fun y : ℝ => Real.sinh y / Real.cosh y :=
    Real.continuous_sinh.div Real.continuous_cosh (fun y => (Real.cosh_pos y).ne')
  exact h.congr (fun y => (Real.tanh_eq_sinh_div_cosh y).symm)

private lemma hasDerivAt_tanh (x : ℝ) : HasDerivAt Real.tanh (sechSq x) x := by
  have hdiv : HasDerivAt (fun y : ℝ => Real.sinh y / Real.cosh y)
      ((Real.cosh x * Real.cosh x - Real.sinh x * Real.sinh x) / Real.cosh x ^ 2) x :=
    (Real.hasDerivAt_sinh x).div (Real.hasDerivAt_cosh x) (Real.cosh_pos x).ne'
  have hfun : (fun y : ℝ => Real.sinh y / Real.cosh y) = Real.tanh := by
    funext y; exact (Real.tanh_eq_sinh_div_cosh y).symm
  have hv : (Real.cosh x * Real.cosh x - Real.sinh x * Real.sinh x) / Real.cosh x ^ 2
      = sechSq x := by
    have hc : Real.cosh x ^ 2 = Real.sinh x ^ 2 + 1 := Real.cosh_sq x
    unfold sechSq
    field_simp
    nlinarith [hc]
  rw [hfun, hv] at hdiv
  exact hdiv

private lemma shapeH_pos {T : ℝ} (hT : 0 < T) : 0 < shapeH T := by
  unfold shapeH
  rw [Real.tanh_eq_sinh_div_cosh]
  exact div_pos (Real.sinh_pos_iff.mpr (div_pos one_pos (by positivity))) (Real.cosh_pos _)

private lemma tanh_secant_core {a : ℝ} (ha : 0 < a) (u : ℝ) (hu : 0 < u) (hu1 : u < 1) :
    u * Real.tanh a ≤ Real.tanh (a * u) := by
  have hmono : ∀ x ∈ Set.Ioi (0 : ℝ), HasDerivWithinAt (fun v : ℝ => Real.tanh (a * v) / v)
      ((sechSq (a * x) * a * x - Real.tanh (a * x)) / x ^ 2) (Set.Ioi (0 : ℝ)) x := by
    intro x hx
    have hx0 : x ≠ 0 := ne_of_gt hx
    have h1 : HasDerivAt (fun v : ℝ => Real.tanh (a * v)) (sechSq (a * x) * a) x := by
      have h := (hasDerivAt_tanh (a * x)).comp x ((hasDerivAt_id x).const_mul a)
      simpa using h
    have h2 : HasDerivAt (fun v : ℝ => v) 1 x := hasDerivAt_id x
    have hdiv := h1.div h2 hx0
    simpa [mul_one] using hdiv.hasDerivWithinAt
  have hneg : ∀ x ∈ Set.Ioi (0 : ℝ), (sechSq (a * x) * a * x - Real.tanh (a * x)) / x ^ 2 < 0 := by
    intro x hx
    have hy : 0 < a * x := mul_pos ha hx
    have hsinh : Real.sinh (2 * (a * x)) = 2 * Real.sinh (a * x) * Real.cosh (a * x) :=
      Real.sinh_two_mul (a * x)
    have hbig : 2 * (a * x) < Real.sinh (2 * (a * x)) := by
      have h := Real.sinh_sub_id_strictMono hy
      simpa using h
    have hcosh : 0 < Real.cosh (a * x) := Real.cosh_pos (a * x)
    have hnum : (a * x) * sechSq (a * x) - Real.tanh (a * x) < 0 := by
      have hkey : (a * x) < Real.sinh (a * x) * Real.cosh (a * x) := by nlinarith [hsinh, hbig]
      have hnum' : (a * x) * sechSq (a * x) - Real.tanh (a * x)
          = ((a * x) - Real.sinh (a * x) * Real.cosh (a * x)) / Real.cosh (a * x) ^ 2 := by
        rw [Real.tanh_eq_sinh_div_cosh]
        unfold sechSq
        field_simp
        try ring
      rw [hnum']
      exact div_neg_of_neg_of_pos (by linarith) (pow_pos hcosh 2)
    have hval : sechSq (a * x) * a * x - Real.tanh (a * x)
        = (a * x) * sechSq (a * x) - Real.tanh (a * x) := by ring
    rw [hval]
    have hxpos : 0 < x := hx
    exact div_neg_of_neg_of_pos hnum (pow_pos hxpos 2)
  have hcont : ContinuousOn (fun v : ℝ => Real.tanh (a * v) / v) (Set.Ioi (0 : ℝ)) := by
    have h1 : ContinuousOn (fun v : ℝ => Real.tanh (a * v)) (Set.Ioi (0 : ℝ)) :=
      (continuous_tanh.comp (continuous_const.mul continuous_id)).continuousOn
    have h2 : ContinuousOn (fun v : ℝ => v) (Set.Ioi (0 : ℝ)) := continuous_id.continuousOn
    exact h1.div h2 (fun x hx => (ne_of_gt hx))
  have hanti : StrictAntiOn (fun v : ℝ => Real.tanh (a * v) / v) (Set.Ioi (0 : ℝ)) := by
    refine strictAntiOn_of_hasDerivWithinAt_neg (D := Set.Ioi (0 : ℝ))
      (f := fun v : ℝ => Real.tanh (a * v) / v)
      (f' := fun x : ℝ => (sechSq (a * x) * a * x - Real.tanh (a * x)) / x ^ 2)
      (convex_Ioi (0 : ℝ)) hcont ?_ ?_
    · intro x hx
      have hx' : x ∈ Set.Ioi (0 : ℝ) := by
        have hi : interior (Set.Ioi (0 : ℝ)) = Set.Ioi (0 : ℝ) := isOpen_Ioi.interior_eq
        rwa [hi] at hx
      have hi : interior (Set.Ioi (0 : ℝ)) = Set.Ioi (0 : ℝ) := isOpen_Ioi.interior_eq
      rw [hi]
      exact hmono x hx'
    · intro x hx
      have hx' : x ∈ Set.Ioi (0 : ℝ) := by
        have hi : interior (Set.Ioi (0 : ℝ)) = Set.Ioi (0 : ℝ) := isOpen_Ioi.interior_eq
        rwa [hi] at hx
      exact hneg x hx'
  have hmem1 : (1 : ℝ) ∈ Set.Ioi (0 : ℝ) := by norm_num
  have hmemu : u ∈ Set.Ioi (0 : ℝ) := hu
  have hlt : Real.tanh (a * 1) / 1 < Real.tanh (a * u) / u := hanti hmemu hmem1 hu1
  have hmul := mul_lt_mul_of_pos_left hlt hu
  have hleft : u * (Real.tanh (a * 1) / 1) = u * Real.tanh a := by
    rw [mul_one a, div_one]
  have hright : u * (Real.tanh (a * u) / u) = Real.tanh (a * u) :=
    mul_div_cancel₀ _ (ne_of_gt hu)
  rw [hleft, hright] at hmul
  exact hmul.le

theorem targetPropTanhSecant : TargetPropTanhSecant := by
  unfold TargetPropTanhSecant
  intro a u ha hu
  rcases hu with ⟨hu0, hu1⟩
  rcases eq_or_lt_of_le hu0 with h0 | h0
  · rw [← h0]
    simp
  · rcases eq_or_lt_of_le hu1 with h1 | h1
    · rw [h1]
      simp
    · exact tanh_secant_core ha u h0 h1

theorem targetPropDeficitLeThird : TargetPropDeficitLeThird := by
  unfold TargetPropDeficitLeThird
  intro T hT
  have ha : 0 < 1 / (2 * T) := by positivity
  have hpt : ∀ u ∈ Set.Icc (0 : ℝ) 1,
      2 * u * (u * shapeH T) ≤ 2 * u * Real.tanh (u / (2 * T)) := by
    intro u hu
    have hsec := targetPropTanhSecant (1 / (2 * T)) u ha hu
    have hsec' : u * shapeH T ≤ Real.tanh (u / (2 * T)) := by
      unfold shapeH
      have harg : (1 / (2 * T)) * u = u / (2 * T) := by
        field_simp
        try ring
      rw [← harg]
      exact hsec
    exact mul_le_mul_of_nonneg_left hsec' (by linarith [hu.1])
  have hcont1 : Continuous fun u : ℝ => 2 * u * (u * shapeH T) := by fun_prop
  have hcont1i : IntervalIntegrable (fun u : ℝ => 2 * u * (u * shapeH T)) volume 0 1 :=
    hcont1.intervalIntegrable 0 1
  have hcont2 : IntervalIntegrable (fun u : ℝ => 2 * u * Real.tanh (u / (2 * T))) volume 0 1 :=
    (((continuous_const.mul continuous_id).mul
      (continuous_tanh.comp (continuous_id.div_const (2 * T))))).intervalIntegrable 0 1
  have hmono : ∫ u in (0 : ℝ)..1, 2 * u * (u * shapeH T)
      ≤ ∫ u in (0 : ℝ)..1, 2 * u * Real.tanh (u / (2 * T)) := by
    refine intervalIntegral.integral_mono_on (a := (0 : ℝ)) (b := 1) (by norm_num)
      hcont1i hcont2 ?_
    intro x hx
    exact hpt x hx
  have hcalc : ∫ u in (0 : ℝ)..1, 2 * u * (u * shapeH T) = (2 / 3) * shapeH T := by
    have hrew : (fun u : ℝ => 2 * u * (u * shapeH T)) = (fun u : ℝ => (2 * shapeH T) * u ^ 2) := by
      funext u; ring
    rw [hrew, intervalIntegral.integral_const_mul, integral_pow]
    ring_nf
  have hw : (2 / 3) * shapeH T ≤ wGap T := by
    unfold wGap
    have hstep : (2 / 3) * shapeH T ≤ ∫ u in (0 : ℝ)..1, 2 * u * Real.tanh (u / (2 * T)) :=
      hcalc ▸ hmono
    linarith [hstep]
  have hh : 0 < shapeH T := shapeH_pos hT
  have hratio : (2 : ℝ) / 3 ≤ wGap T / shapeH T := by
    rw [le_div_iff₀ hh]
    linarith
  have hratio' : (2 : ℝ) / 3 ≤ wGap T / Real.tanh (1 / (2 * T)) := by
    simpa [shapeH] using hratio
  unfold deficitFrac shapePhi
  linarith [hratio']

theorem targetPropGapNegTail : TargetPropGapNegTail := by
  unfold TargetPropGapNegTail
  intro T hT hT1
  exact CQM.Ring15.LockTailRatio.targetPropGapNegOfDeficitLeThird T hT
    (targetPropDeficitLeThird T hT) hT1

end

end CQM.Ring15.LockSecant
