-- Ring15LockWD2.lean（第 198 轮）：$w$ 的二阶导数与形状项导数（G-188b 第一步）
-- 只 import Spec ＋ 上游证明模块 ＋ 基线库模块；无 sorry／admit／自造 axiom。
import Ring15Spec
import Ring15LockWD
import Mathlib.Analysis.Calculus.ParametricIntervalIntegral
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp

namespace CQM.Ring15.LockWD2

open MeasureTheory
open Filter
open scoped Interval
open CQM.Ring15.Spec

noncomputable section

private lemma continuous_tanh : Continuous Real.tanh := by
  have h : Continuous fun y : ℝ => Real.sinh y / Real.cosh y :=
    Real.continuous_sinh.div Real.continuous_cosh (fun y => (Real.cosh_pos y).ne')
  exact h.congr (fun y => (Real.tanh_eq_sinh_div_cosh y).symm)

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

private lemma tanh_pos_of_pos {x : ℝ} (h : 0 < x) : 0 < Real.tanh x := by
  rw [Real.tanh_eq_sinh_div_cosh]
  exact div_pos (Real.sinh_pos_iff.mpr h) (Real.cosh_pos x)

private lemma cont_F (x : ℝ) : Continuous fun t : ℝ => t ^ 2 * sechSq (t / (2 * x)) :=
  (continuous_id.pow 2).mul (cont_sechSq.comp (continuous_id.div_const (2 * x)))

private lemma cont_F' (x : ℝ) :
    Continuous fun t : ℝ => (t ^ 3 / x ^ 2) * sechSq (t / (2 * x)) * Real.tanh (t / (2 * x)) := by
  have h1 : Continuous fun t : ℝ => t ^ 3 / x ^ 2 := (continuous_id.pow 3).div_const (x ^ 2)
  have h2 : Continuous fun t : ℝ => sechSq (t / (2 * x)) :=
    cont_sechSq.comp (continuous_id.div_const (2 * x))
  have h3 : Continuous fun t : ℝ => Real.tanh (t / (2 * x)) :=
    continuous_tanh.comp (continuous_id.div_const (2 * x))
  exact (h1.mul h2).mul h3

/-- $F(x,t)=t^2\mathrm{sech}^2\frac{t}{2x}$ 对 $x$ 的导数（$x\ne0$）。 -/
private lemma deriv_F (t x : ℝ) (hx : x ≠ 0) :
    HasDerivAt (fun y : ℝ => t ^ 2 * sechSq (t / (2 * y)))
      ((t ^ 3 / x ^ 2) * sechSq (t / (2 * x)) * Real.tanh (t / (2 * x))) x := by
  have hinner : HasDerivAt (fun y : ℝ => t / (2 * y)) (-(t / (2 * x ^ 2))) x := by
    have hinv : HasDerivAt (fun y : ℝ => y⁻¹) (-(x ^ 2)⁻¹) x := hasDerivAt_inv hx
    have hmul := hinv.const_mul (t / 2)
    have hfun : (fun y : ℝ => (t / 2) * y⁻¹) = fun y : ℝ => t / (2 * y) := by
      funext y; ring
    have hval : (t / 2) * (-(x ^ 2)⁻¹) = -(t / (2 * x ^ 2)) := by
      field_simp
    rw [hfun, hval] at hmul
    exact hmul
  -- cosh 的链式导数：d/dy cosh(t/(2y)) = sinh(t/(2x)) * (-(t/(2x^2)))
  have hcosh : HasDerivAt (fun y : ℝ => Real.cosh (t / (2 * y)))
      (Real.sinh (t / (2 * x)) * (-(t / (2 * x ^ 2)))) x := by
    have h := (Real.hasDerivAt_cosh (t / (2 * x))).comp x hinner
    simpa [Function.comp] using h
  have hcne : Real.cosh (t / (2 * x)) ≠ 0 := (Real.cosh_pos (t / (2 * x))).ne'
  have hsq : HasDerivAt (fun y : ℝ => Real.cosh (t / (2 * y)) ^ 2)
      (2 * Real.cosh (t / (2 * x)) * (Real.sinh (t / (2 * x)) * (-(t / (2 * x ^ 2))))) x := by
    have := hcosh.pow 2
    simpa [pow_one] using this
  have hne : Real.cosh (t / (2 * x)) ^ 2 ≠ 0 := pow_ne_zero 2 hcne
  have hinv2 : HasDerivAt (fun y : ℝ => (Real.cosh (t / (2 * y)) ^ 2)⁻¹)
      (-(2 * Real.cosh (t / (2 * x)) * (Real.sinh (t / (2 * x)) * (-(t / (2 * x ^ 2)))))
        / (Real.cosh (t / (2 * x)) ^ 2) ^ 2) x := hsq.inv hne
  have hscaled := hinv2.const_mul (t ^ 2)
  have hfun2 : (fun y : ℝ => t ^ 2 * (Real.cosh (t / (2 * y)) ^ 2)⁻¹)
      = fun y : ℝ => t ^ 2 * sechSq (t / (2 * y)) := by
    funext y
    simp [sechSq]
  have hval2 : t ^ 2 * (-(2 * Real.cosh (t / (2 * x))
        * (Real.sinh (t / (2 * x)) * (-(t / (2 * x ^ 2)))))
        / (Real.cosh (t / (2 * x)) ^ 2) ^ 2)
      = (t ^ 3 / x ^ 2) * sechSq (t / (2 * x)) * Real.tanh (t / (2 * x)) := by
    simp only [sechSq, Real.tanh_eq_sinh_div_cosh]
    field_simp
  rw [hfun2, hval2] at hscaled
  exact hscaled

theorem targetPropWGapDeriv2 : CQM.Ring15.Spec.TargetPropWGapDeriv2 := by
  intro T hT
  have hhalf : (0 : ℝ) < T / 2 := by linarith
  have hnhds : Set.Ioo (T / 2) (2 * T) ∈ nhds T :=
    Ioo_mem_nhds (by linarith [hT]) (by linarith [hT])
  set Bfun : ℝ → ℝ := fun x => ∫ t in (0 : ℝ)..1, t ^ 2 * sechSq (t / (2 * x)) with hBfun
  have hmain := intervalIntegral.hasDerivAt_integral_of_dominated_loc_of_deriv_le
    (μ := (volume : Measure ℝ)) (a := (0 : ℝ)) (b := 1) (x₀ := T)
    (s := Set.Ioo (T / 2) (2 * T)) (bound := fun t : ℝ => 4 / T ^ 2 * t ^ 3)
    (F := fun x t : ℝ => t ^ 2 * sechSq (t / (2 * x)))
    (F' := fun x t : ℝ => (t ^ 3 / x ^ 2) * sechSq (t / (2 * x)) * Real.tanh (t / (2 * x)))
    hnhds
    (Filter.Eventually.of_forall (fun x => (cont_F x).aestronglyMeasurable))
    ((cont_F T).intervalIntegrable 0 1)
    ((cont_F' T).aestronglyMeasurable)
    (Filter.Eventually.of_forall (fun t ht x hx => by
      rw [Set.uIoc_of_le (by norm_num : (0 : ℝ) ≤ 1)] at ht
      have ht0 : (0 : ℝ) < t := ht.1
      have hxT : T / 2 < x := hx.1
      have hxpos : (0 : ℝ) < x := by linarith
      have hx2 : (T / 2) ^ 2 ≤ x ^ 2 := by nlinarith [hxT, hhalf, hxpos]
      have hfac : t ^ 3 / x ^ 2 ≤ t ^ 3 / (T / 2) ^ 2 :=
        div_le_div_of_nonneg_left (by positivity) (pow_pos hhalf 2) hx2
      have hfac' : t ^ 3 / (T / 2) ^ 2 = 4 / T ^ 2 * t ^ 3 := by
        field_simp
        ring
      have hs1 : sechSq (t / (2 * x)) ≤ 1 := sechSq_le_one _
      have htp : (0 : ℝ) < Real.tanh (t / (2 * x)) := tanh_pos_of_pos (by positivity)
      have ht1 : Real.tanh (t / (2 * x)) ≤ 1 := le_of_lt (Real.tanh_lt_one _)
      have hfn : (0 : ℝ) ≤ t ^ 3 / x ^ 2 :=
        div_nonneg (by positivity) (le_of_lt (pow_pos hxpos 2))
      have hnn : (0 : ℝ) ≤ t ^ 3 / x ^ 2 * sechSq (t / (2 * x)) * Real.tanh (t / (2 * x)) :=
        mul_nonneg (mul_nonneg hfn (le_of_lt (sechSq_pos _))) (le_of_lt htp)
      show ‖(t ^ 3 / x ^ 2) * sechSq (t / (2 * x)) * Real.tanh (t / (2 * x))‖
          ≤ 4 / T ^ 2 * t ^ 3
      rw [Real.norm_eq_abs, abs_of_nonneg hnn]
      calc t ^ 3 / x ^ 2 * sechSq (t / (2 * x)) * Real.tanh (t / (2 * x))
          ≤ t ^ 3 / x ^ 2 * 1 * 1 := by
            apply mul_le_mul
            · exact mul_le_mul_of_nonneg_left hs1 hfn
            · exact ht1
            · exact le_of_lt htp
            · positivity
        _ = t ^ 3 / x ^ 2 := by ring
        _ ≤ 4 / T ^ 2 * t ^ 3 := by
            rw [← hfac']
            exact hfac))
    ((continuous_const.mul (continuous_id.pow 3)).intervalIntegrable 0 1)
    (Filter.Eventually.of_forall (fun t ht x hx =>
      deriv_F t x (by linarith [hx.1, hhalf])))
  obtain ⟨hInt, hderiv⟩ := hmain
  have hBfunD : HasDerivAt Bfun
      (∫ t in (0 : ℝ)..1, (t ^ 3 / T ^ 2) * sechSq (t / (2 * T)) * Real.tanh (t / (2 * T))) T := by
    simpa [hBfun] using hderiv
  -- ∫ t^2 sechSq = -T^2 · w'
  have hBval : Bfun T = -(T ^ 2) * wGapDeriv T := by
    show (∫ t in (0 : ℝ)..1, t ^ 2 * sechSq (t / (2 * T))) = -(T ^ 2) * wGapDeriv T
    rw [wGapDeriv]
    field_simp
  -- ∫ (t^3/T^2) sechSq tanh = (1/T^2) ∫ t^3 sechSq tanh
  have hB'val : (∫ t in (0 : ℝ)..1,
        (t ^ 3 / T ^ 2) * sechSq (t / (2 * T)) * Real.tanh (t / (2 * T)))
      = (1 / T ^ 2) * (∫ t in (0 : ℝ)..1,
          t ^ 3 * sechSq (t / (2 * T)) * Real.tanh (t / (2 * T))) := by
    rw [show (fun t : ℝ => (t ^ 3 / T ^ 2) * sechSq (t / (2 * T)) * Real.tanh (t / (2 * T)))
        = fun t : ℝ => (1 / T ^ 2) *
          (t ^ 3 * sechSq (t / (2 * T)) * Real.tanh (t / (2 * T))) from by
      funext t; field_simp]
    rw [intervalIntegral.integral_const_mul]
  -- d/dT (-(1/T^2)) = 2/T^3
  have hinvder : HasDerivAt (fun x : ℝ => -(1 / x ^ 2)) (2 / T ^ 3) T := by
    have hx2 : HasDerivAt (fun x : ℝ => x ^ 2) (2 * T) T := by
      simpa using (hasDerivAt_id T).pow 2
    have hx2ne : T ^ 2 ≠ 0 := pow_ne_zero 2 (ne_of_gt hT)
    have hinv' : HasDerivAt (fun x : ℝ => (x ^ 2)⁻¹) (-(2 * T) / (T ^ 2) ^ 2) T :=
      hx2.inv hx2ne
    have hinvneg := hinv'.neg
    have hval : -( -(2 * T) / (T ^ 2) ^ 2) = 2 / T ^ 3 := by
      field_simp
    rw [hval] at hinvneg
    simpa [one_div] using hinvneg
  have hquot : HasDerivAt (fun x : ℝ => -(1 / x ^ 2) * Bfun x) (wGapDeriv2 T) T := by
    have hmul := hinvder.mul hBfunD
    have hval : (2 / T ^ 3) * Bfun T + (-(1 / T ^ 2)) * (∫ t in (0 : ℝ)..1,
        (t ^ 3 / T ^ 2) * sechSq (t / (2 * T)) * Real.tanh (t / (2 * T))) = wGapDeriv2 T := by
      rw [hBval, hB'val]
      unfold wGapDeriv2
      field_simp
      ring
    rw [hval] at hmul
    exact hmul
  have hcongr : (fun x : ℝ => -(1 / x ^ 2) * Bfun x) = wGapDeriv := by
    funext x
    simp only [hBfun, wGapDeriv]
  rw [hcongr] at hquot
  exact hquot

theorem targetPropShapeDeriv : CQM.Ring15.Spec.TargetPropShapeDeriv := by
  intro T hT
  have hneg : wGapDeriv T < 0 := CQM.Ring15.LockWD.targetPropWGapDerivNeg T hT
  have h2 := targetPropWGapDeriv2 T hT
  have hd : HasDerivAt (fun T' : ℝ => -(wGapDeriv T')) (-(wGapDeriv2 T)) T := h2.neg
  have hne : -(wGapDeriv T) ≠ 0 := by
    intro h
    exact (ne_of_lt hneg) (neg_eq_zero.mp h)
  have hbase : HasDerivAt (fun T' : ℝ => wGap T' / -(wGapDeriv T')) (shapeDeriv T) T := by
    have h := (CQM.Ring15.LockWD.targetPropWGapDeriv T hT).div hd hne
    have hval : (wGapDeriv T * -(wGapDeriv T) - wGap T * -(wGapDeriv2 T))
        / (-(wGapDeriv T)) ^ 2 = shapeDeriv T := by
      unfold shapeDeriv
      field_simp
      ring
    rw [hval] at h
    exact h
  have heq : (fun T' : ℝ => wGap T' / |wGapDeriv T'|)
      =ᶠ[nhds T] (fun T' : ℝ => wGap T' / -(wGapDeriv T')) := by
    filter_upwards [show Set.Ioo (0 : ℝ) (2 * T) ∈ nhds T from
      Ioo_mem_nhds (by linarith) (by linarith)] with T' hT'
    have hp : (0 : ℝ) < T' := by linarith [hT'.1]
    rw [abs_of_neg (CQM.Ring15.LockWD.targetPropWGapDerivNeg T' hp)]
  exact hbase.congr_of_eventuallyEq heq

end

end CQM.Ring15.LockWD2
