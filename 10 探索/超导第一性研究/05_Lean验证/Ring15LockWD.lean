-- Ring15LockWD.lean（第 196 轮）：$w$ 的导数表示（G-190c）——导数恒等式与导数负性
-- 只 import Spec ＋三条基线库模块；无 sorry／admit／自造 axiom。
import Ring15Spec
import Mathlib.Analysis.Calculus.ParametricIntervalIntegral
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp

namespace CQM.Ring15.LockWD

open MeasureTheory
open Filter
open scoped Interval
open CQM.Ring15.Spec

noncomputable section

private lemma continuous_tanh : Continuous Real.tanh := by
  have h : Continuous fun y : ℝ => Real.sinh y / Real.cosh y :=
    Real.continuous_sinh.div Real.continuous_cosh (fun y => (Real.cosh_pos y).ne')
  exact h.congr (fun y => (Real.tanh_eq_sinh_div_cosh y).symm)

private lemma hasDerivAt_tanh' (x : ℝ) : HasDerivAt Real.tanh (1 / Real.cosh x ^ 2) x := by
  have hdiv : HasDerivAt (fun y : ℝ => Real.sinh y / Real.cosh y)
      ((Real.cosh x * Real.cosh x - Real.sinh x * Real.sinh x) / Real.cosh x ^ 2) x :=
    (Real.hasDerivAt_sinh x).div (Real.hasDerivAt_cosh x) (Real.cosh_pos x).ne'
  have hfun : (fun y : ℝ => Real.sinh y / Real.cosh y) = Real.tanh := by
    funext y; exact (Real.tanh_eq_sinh_div_cosh y).symm
  have hv : (Real.cosh x * Real.cosh x - Real.sinh x * Real.sinh x) / Real.cosh x ^ 2
      = 1 / Real.cosh x ^ 2 := by
    have hc := Real.cosh_sq x
    field_simp
    nlinarith [hc]
  rw [hfun, hv] at hdiv
  exact hdiv

open CQM.Ring15.Spec in
private lemma cont_F (x : ℝ) : Continuous fun t : ℝ => 2 * t * Real.tanh (t / (2 * x)) := by
  refine (continuous_const.mul continuous_id).mul ?_
  exact continuous_tanh.comp (continuous_id.div_const (2 * x))

private lemma cont_sechSq : Continuous sechSq := by
  unfold sechSq
  exact continuous_const.div (Real.continuous_cosh.pow 2)
    (fun x => pow_ne_zero 2 (Real.cosh_pos x).ne')

private lemma sechSq_pos (x : ℝ) : 0 < sechSq x := by
  unfold sechSq
  exact div_pos one_pos (pow_pos (Real.cosh_pos x) 2)

private lemma sechSq_le_one (x : ℝ) : sechSq x ≤ 1 := by
  unfold sechSq
  have hc : 1 ≤ Real.cosh x ^ 2 := by
    have h1 := Real.one_le_cosh x
    have hp := Real.cosh_pos x
    nlinarith [h1, hp]
  rw [div_le_iff₀ (pow_pos (Real.cosh_pos x) 2)]
  nlinarith [hc]

private lemma cont_F' (x : ℝ) :
    Continuous fun t : ℝ => -(t ^ 2 / x ^ 2) * sechSq (t / (2 * x)) := by
  have h1 : Continuous fun t : ℝ => t ^ 2 / x ^ 2 := (continuous_id.pow 2).div_const (x ^ 2)
  exact h1.neg.mul (cont_sechSq.comp (continuous_id.div_const (2 * x)))

/-- $F(x,t)=2t\tanh\frac{t}{2x}$ 对 $x$ 的导数（含 $x\ne0$；$\tanh'=\mathrm{sech}^2$ 自足重证）。 -/
private lemma deriv_F (t x : ℝ) (hx : x ≠ 0) :
    HasDerivAt (fun y : ℝ => 2 * t * Real.tanh (t / (2 * y)))
      (-(t ^ 2 / x ^ 2) * sechSq (t / (2 * x))) x := by
  have hinner : HasDerivAt (fun y : ℝ => t / (2 * y)) (-(t / (2 * x ^ 2))) x := by
    have hinv : HasDerivAt (fun y : ℝ => y⁻¹) (-(x ^ 2)⁻¹) x := hasDerivAt_inv hx
    have hmul := hinv.const_mul (t / 2)
    have hfun : (fun y : ℝ => (t / 2) * y⁻¹) = fun y : ℝ => t / (2 * y) := by
      funext y; ring
    have hval : (t / 2) * (-(x ^ 2)⁻¹) = -(t / (2 * x ^ 2)) := by
      field_simp
    rw [hfun, hval] at hmul
    exact hmul
  have htanh : HasDerivAt Real.tanh (sechSq (t / (2 * x))) (t / (2 * x)) :=
    hasDerivAt_tanh' (t / (2 * x))
  have hcomp : HasDerivAt (fun y : ℝ => Real.tanh (t / (2 * y)))
      (sechSq (t / (2 * x)) * (-(t / (2 * x ^ 2)))) x := by
    simpa [Function.comp] using htanh.comp x hinner
  have hscaled := hcomp.const_mul (2 * t)
  have hval2 : (2 * t) * (sechSq (t / (2 * x)) * (-(t / (2 * x ^ 2))))
      = -(t ^ 2 / x ^ 2) * sechSq (t / (2 * x)) := by
    field_simp
  rw [hval2] at hscaled
  exact hscaled

theorem targetPropWGapDeriv : CQM.Ring15.Spec.TargetPropWGapDeriv := by
  intro T hT
  have hTpos : (0 : ℝ) < T := hT
  have hhalf : (0 : ℝ) < T / 2 := by linarith
  have hnhds : Set.Ioo (T / 2) (2 * T) ∈ nhds T :=
    Ioo_mem_nhds (by linarith [hTpos]) (by linarith [hTpos])
  have hmain := intervalIntegral.hasDerivAt_integral_of_dominated_loc_of_deriv_le
    (μ := (volume : Measure ℝ)) (a := (0 : ℝ)) (b := 1) (x₀ := T)
    (s := Set.Ioo (T / 2) (2 * T)) (bound := fun t : ℝ => 4 / T ^ 2 * t ^ 2)
    (F := fun x t : ℝ => 2 * t * Real.tanh (t / (2 * x)))
    (F' := fun x t : ℝ => -(t ^ 2 / x ^ 2) * sechSq (t / (2 * x)))
    hnhds
    (Filter.Eventually.of_forall (fun x => (cont_F x).aestronglyMeasurable))
    ((cont_F T).intervalIntegrable 0 1)
    ((cont_F' T).aestronglyMeasurable)
    (Filter.Eventually.of_forall (fun t ht x hx => by
      rw [Set.uIoc_of_le (by norm_num : (0 : ℝ) ≤ 1)] at ht
      have ht0 : (0 : ℝ) < t := ht.1
      have ht1 : t ≤ 1 := ht.2
      have hxT : T / 2 < x := hx.1
      have hxpos : (0 : ℝ) < x := by linarith
      have hx2 : (T / 2) ^ 2 ≤ x ^ 2 := by nlinarith [hxT, hhalf, hxpos]
      have hfac : t ^ 2 / x ^ 2 ≤ t ^ 2 / (T / 2) ^ 2 :=
        div_le_div_of_nonneg_left (sq_nonneg t) (pow_pos hhalf 2) hx2
      have hfac' : t ^ 2 / (T / 2) ^ 2 = 4 / T ^ 2 * t ^ 2 := by
        field_simp
        ring
      have hs1 : sechSq (t / (2 * x)) ≤ 1 := sechSq_le_one _
      have hsn : (0 : ℝ) ≤ sechSq (t / (2 * x)) := le_of_lt (sechSq_pos _)
      have hfn : (0 : ℝ) ≤ t ^ 2 / x ^ 2 :=
        div_nonneg (sq_nonneg t) (le_of_lt (pow_pos hxpos 2))
      have hnn : (0 : ℝ) ≤ t ^ 2 / x ^ 2 * sechSq (t / (2 * x)) := mul_nonneg hfn hsn
      show ‖-(t ^ 2 / x ^ 2) * sechSq (t / (2 * x))‖ ≤ 4 / T ^ 2 * t ^ 2
      rw [Real.norm_eq_abs,
        show -(t ^ 2 / x ^ 2) * sechSq (t / (2 * x)) = -(t ^ 2 / x ^ 2 * sechSq (t / (2 * x))) by
          ring,
        abs_neg, abs_of_nonneg hnn]
      calc t ^ 2 / x ^ 2 * sechSq (t / (2 * x))
          ≤ t ^ 2 / x ^ 2 * 1 := by
            exact mul_le_mul_of_nonneg_left hs1 hfn
        _ ≤ 4 / T ^ 2 * t ^ 2 := by
            rw [mul_one, ← hfac']
            exact hfac))
    ((continuous_const.mul (continuous_id.pow 2)).intervalIntegrable 0 1)
    (Filter.Eventually.of_forall (fun t ht x hx =>
      deriv_F t x (by linarith [hx.1, hhalf])))
  obtain ⟨_, hderiv⟩ := hmain
  have hcongr : ∀ t : ℝ,
      -(t ^ 2 / T ^ 2) * sechSq (t / (2 * T))
        = -(1 / T ^ 2) * (t ^ 2 * sechSq (t / (2 * T))) := by
    intro t
    field_simp
  have hint : (∫ t in (0 : ℝ)..1, -(t ^ 2 / T ^ 2) * sechSq (t / (2 * T))) = wGapDeriv T := by
    rw [show (fun t : ℝ => -(t ^ 2 / T ^ 2) * sechSq (t / (2 * T)))
        = fun t : ℝ => -(1 / T ^ 2) * (t ^ 2 * sechSq (t / (2 * T))) from
      funext fun t => hcongr t]
    rw [intervalIntegral.integral_const_mul]
    rfl
  rw [hint] at hderiv
  simpa [wGap] using hderiv

theorem targetPropWGapDerivNeg : CQM.Ring15.Spec.TargetPropWGapDerivNeg := by
  intro T hT
  have hcont : Continuous fun u : ℝ => u ^ 2 * sechSq (u / (2 * T)) :=
    (continuous_id.pow 2).mul (cont_sechSq.comp (continuous_id.div_const (2 * T)))
  have hpos : 0 < ∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T)) := by
    refine intervalIntegral.integral_pos (a := (0 : ℝ)) (b := 1) (by norm_num)
      hcont.continuousOn (fun x hx => ?_) ⟨1 / 2, ⟨by norm_num, by norm_num⟩, ?_⟩
    · exact mul_nonneg (sq_nonneg x) (le_of_lt (sechSq_pos _))
    · exact mul_pos (by norm_num) (sechSq_pos _)
  have hT2 : (0 : ℝ) < T ^ 2 := pow_pos hT 2
  have h1 : (0 : ℝ) < 1 / T ^ 2 := one_div_pos.mpr hT2
  rw [wGapDeriv]
  nlinarith [hpos, h1]

end

end CQM.Ring15.LockWD
