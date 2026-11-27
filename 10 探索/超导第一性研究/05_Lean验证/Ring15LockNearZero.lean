-- Ring15LockNearZero.lean（第 211 轮）：近零端 D>0（G-188b-2k 近零端）
-- 只 import Spec ＋已证模块 ＋基线库；无 sorry／admit／自造 axiom。
-- 内容：①δ(T) ≥ (8/15)T²（T≤1/10）；②λ(T) ≤ T²/3；③D(T)>0（T≤1/10）。
import Ring15Spec
import Ring15LockIbp
import Ring15LockDeficit
import Ring15LockWD
import Ring15LockSecant
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.Analysis.Complex.Trigonometric

namespace CQM.Ring15.LockNearZero

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

private lemma sechSq_le_one (x : ℝ) : sechSq x ≤ 1 := by
  unfold sechSq
  have hc : (1 : ℝ) ≤ Real.cosh x ^ 2 := by
    have h := Real.cosh_sq x
    nlinarith [sq_nonneg (Real.sinh x)]
  exact div_le_one_of_le₀ hc (by positivity)

private lemma tanh_le_self {x : ℝ} (hx : 0 ≤ x) : Real.tanh x ≤ x := by
  have hmono : MonotoneOn (fun y : ℝ => y - Real.tanh y) (Set.Ici (0 : ℝ)) := by
    refine monotoneOn_of_hasDerivWithinAt_nonneg (D := Set.Ici (0 : ℝ))
      (f := fun y : ℝ => y - Real.tanh y) (f' := fun y : ℝ => 1 - sechSq y)
      (convex_Ici (0 : ℝ)) ?_ ?_ ?_
    · exact (continuous_id.sub continuous_tanh).continuousOn
    · intro x hx'
      have hx0 : x ∈ Set.Ioi (0 : ℝ) := by
        have hi : interior (Set.Ici (0 : ℝ)) = Set.Ioi (0 : ℝ) := interior_Ici
        rwa [hi] at hx'
      have hder : HasDerivAt (fun y : ℝ => y - Real.tanh y) (1 - sechSq x) x :=
        (hasDerivAt_id x).sub (hasDerivAt_tanh x)
      have hi : interior (Set.Ici (0 : ℝ)) = Set.Ioi (0 : ℝ) := interior_Ici
      rw [hi]
      exact hder.hasDerivWithinAt
    · intro x hx'
      have hle : sechSq x ≤ 1 := sechSq_le_one x
      linarith
  have h0 : (0 : ℝ) ∈ Set.Ici (0 : ℝ) := by norm_num
  have hx' : x ∈ Set.Ici (0 : ℝ) := hx
  have := hmono h0 hx' hx
  simpa using this

private lemma tanh_nonneg {y : ℝ} (hy : 0 ≤ y) : 0 ≤ Real.tanh y := by
  rw [Real.tanh_eq_sinh_div_cosh]
  have hsinh : 0 ≤ Real.sinh y := by
    rw [Real.sinh_eq]
    have h1 : Real.exp (-y) ≤ Real.exp y := Real.exp_le_exp.mpr (by linarith)
    linarith
  exact div_nonneg hsinh (Real.cosh_pos y).le

private lemma sechSq_ge_one_sub_sq {y : ℝ} (hy0 : 0 ≤ y) : 1 - y ^ 2 ≤ sechSq y := by
  have htanh_nonneg : 0 ≤ Real.tanh y := tanh_nonneg hy0
  have hsq : Real.tanh y ^ 2 ≤ y ^ 2 :=
    pow_le_pow_left₀ htanh_nonneg (tanh_le_self hy0) 2
  have hid : sechSq y = 1 - Real.tanh y ^ 2 := by
    unfold sechSq
    rw [Real.tanh_eq_sinh_div_cosh]
    have hc : Real.cosh y ^ 2 = Real.sinh y ^ 2 + 1 := Real.cosh_sq y
    field_simp
    nlinarith [hc]
  linarith

private lemma integral_u_sq_sechSq_ge {T : ℝ} (hT : 0 < T) (hT1 : T ≤ 1 / 10) :
    (16 / 15) * T ^ 3 ≤ ∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T)) := by
  have h2T0 : (0 : ℝ) ≤ 2 * T := by linarith
  have h2T1 : 2 * T ≤ 1 := by linarith
  have hsech : Continuous fun u : ℝ => sechSq (u / (2 * T)) := by
    unfold sechSq
    exact continuous_const.div
      ((Real.continuous_cosh.comp (continuous_id.div_const (2 * T))).pow 2)
      (fun u => (pow_pos (Real.cosh_pos _) 2).ne')
  have hcontf : Continuous fun u : ℝ => u ^ 2 * sechSq (u / (2 * T)) :=
    (continuous_id.pow 2).mul hsech
  have hcontg : Continuous fun u : ℝ => u ^ 2 * (1 - (u / (2 * T)) ^ 2) := by fun_prop
  have hfint1 : IntervalIntegrable (fun u : ℝ => u ^ 2 * sechSq (u / (2 * T))) volume 0 (2 * T) :=
    hcontf.intervalIntegrable 0 (2 * T)

  have hpt : ∀ u ∈ Set.Ioc (0 : ℝ) (2 * T),
      u ^ 2 * (1 - (u / (2 * T)) ^ 2) ≤ u ^ 2 * sechSq (u / (2 * T)) := by
    intro u hu
    have hz0 : 0 ≤ u / (2 * T) := div_nonneg (le_of_lt hu.1) (by positivity)
    have h := sechSq_ge_one_sub_sq hz0
    exact mul_le_mul_of_nonneg_left h (sq_nonneg u)
  have hsub : ∫ u in (0 : ℝ)..(2 * T), u ^ 2 * (1 - (u / (2 * T)) ^ 2)
      ≤ ∫ u in (0 : ℝ)..(2 * T), u ^ 2 * sechSq (u / (2 * T)) := by
    refine intervalIntegral.integral_mono_on (a := (0 : ℝ)) (b := 2 * T) h2T0
      (hcontg.intervalIntegrable 0 (2 * T)) hfint1 ?_
    intro x hx
    rcases eq_or_lt_of_le hx.1 with h0 | hpos
    · subst h0
      simp
    · exact hpt x ⟨hpos, hx.2⟩
  have hmono01 : ∫ u in (0 : ℝ)..(2 * T), u ^ 2 * sechSq (u / (2 * T))
      ≤ ∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T)) := by
    refine intervalIntegral.integral_mono_interval (c := (0 : ℝ)) (d := 1)
      (a := (0 : ℝ)) (b := 2 * T) (by norm_num) h2T0 h2T1 ?_ (hcontf.intervalIntegrable 0 1)
    exact Filter.Eventually.of_forall (fun x => by
      refine mul_nonneg (sq_nonneg x) ?_
      unfold sechSq
      exact div_nonneg zero_le_one (pow_pos (Real.cosh_pos _) 2).le)
  have hcalc : ∫ u in (0 : ℝ)..(2 * T), u ^ 2 * (1 - (u / (2 * T)) ^ 2) = (16 / 15) * T ^ 3 := by
    have h1 : IntervalIntegrable (fun u : ℝ => u ^ 2) volume 0 (2 * T) :=
      (by fun_prop : Continuous fun u : ℝ => u ^ 2).intervalIntegrable 0 (2 * T)
    have h2 : IntervalIntegrable (fun u : ℝ => (1 / (4 * T ^ 2)) * u ^ 4) volume 0 (2 * T) :=
      (by fun_prop : Continuous fun u : ℝ => (1 / (4 * T ^ 2)) * u ^ 4).intervalIntegrable 0 (2 * T)
    have hrew : (fun u : ℝ => u ^ 2 * (1 - (u / (2 * T)) ^ 2))
        = (fun u : ℝ => u ^ 2 - (1 / (4 * T ^ 2)) * u ^ 4) := by
      funext u
      field_simp
      ring
    rw [hrew, intervalIntegral.integral_sub h1 h2, intervalIntegral.integral_const_mul,
      integral_pow, integral_pow]
    field_simp
    ring
  have hmain : (16 / 15) * T ^ 3 ≤ ∫ u in (0 : ℝ)..(2 * T), u ^ 2 * sechSq (u / (2 * T)) := by
    linarith [hsub, hcalc]
  linarith [hmain, hmono01]

private lemma exp_ten_gt : (12000 : ℝ) < Real.exp 10 := by
  have h1 : (2.7182818283 : ℝ) < Real.exp 1 := Real.exp_one_gt_d9
  have h2 : (2.7182818283 : ℝ) ^ 10 < (Real.exp 1) ^ 10 :=
    pow_lt_pow_left₀ h1 (by norm_num) (by norm_num : (10 : ℕ) ≠ 0)
  have h3 : (12000 : ℝ) < (2.7182818283 : ℝ) ^ 10 := by norm_num
  have h4 : (Real.exp 1) ^ 10 = Real.exp 10 := by
    rw [← Real.exp_nat_mul (1 : ℝ) 10]
    norm_num
  linarith

private lemma exp_ge_twelve_cube {s : ℝ} (hs : 10 ≤ s) : 12 * s ^ 3 ≤ Real.exp s := by
  have hspos : 0 < s := by linarith
  have hmono : MonotoneOn (fun y : ℝ => Real.exp y / y ^ 3) (Set.Ici (10 : ℝ)) := by
    refine monotoneOn_of_hasDerivWithinAt_nonneg (D := Set.Ici (10 : ℝ))
      (f := fun y : ℝ => Real.exp y / y ^ 3)
      (f' := fun y : ℝ => (Real.exp y * (y - 3)) / y ^ 4)
      (convex_Ici (10 : ℝ)) ?_ ?_ ?_
    · have hcont : ContinuousOn (fun y : ℝ => Real.exp y / y ^ 3) (Set.Ici (10 : ℝ)) := by
        refine ContinuousOn.div Real.continuous_exp.continuousOn (continuous_id.pow 3).continuousOn ?_
        intro y hy
        have hy10 : (0 : ℝ) < y := by linarith [Set.mem_Ici.1 hy]
        exact (pow_pos hy10 3).ne'
      exact hcont
    · intro x hx'
      have hx10 : 10 < x := by
        have hi : interior (Set.Ici (10 : ℝ)) = Set.Ioi (10 : ℝ) := interior_Ici
        rwa [hi] at hx'
      have hx0 : (0 : ℝ) < x := by linarith
      have hden : x ^ 3 ≠ 0 := (pow_pos hx0 3).ne'
      have hd0 := (Real.hasDerivAt_exp x).div (hasDerivAt_pow 3 x) hden
      have hd : HasDerivAt (fun y : ℝ => Real.exp y / y ^ 3)
          ((Real.exp x * (x - 3)) / x ^ 4) x := by
        convert hd0 using 1
        field_simp
        ring
      have hi : interior (Set.Ici (10 : ℝ)) = Set.Ioi (10 : ℝ) := interior_Ici
      rw [hi]
      exact hd.hasDerivWithinAt
    · intro x hx'
      have hx10 : 10 < x := by
        have hi : interior (Set.Ici (10 : ℝ)) = Set.Ioi (10 : ℝ) := interior_Ici
        rwa [hi] at hx'
      have hx0 : (0 : ℝ) < x := by linarith
      exact div_nonneg (mul_nonneg (Real.exp_pos x).le (by linarith : (0 : ℝ) ≤ x - 3)) (pow_pos hx0 4).le
  have hmem10 : (10 : ℝ) ∈ Set.Ici (10 : ℝ) := by norm_num
  have hmem : s ∈ Set.Ici (10 : ℝ) := hs
  have h := hmono hmem10 hmem hs
  have hval : (12 : ℝ) < Real.exp 10 / (10 : ℝ) ^ 3 := by
    have hgt := exp_ten_gt
    norm_num
    linarith
  have h12 : (12 : ℝ) < Real.exp s / s ^ 3 := lt_of_lt_of_le hval h
  rw [lt_div_iff₀ (pow_pos hspos 3)] at h12
  linarith

private lemma sinh_ge_three_cube {s : ℝ} (hs : 10 ≤ s) : 3 * s ^ 3 ≤ Real.sinh s := by
  have hspos : 0 < s := by linarith
  have hexp : 12 * s ^ 3 ≤ Real.exp s := exp_ge_twelve_cube hs
  have h2s : (2 : ℝ) ≤ Real.exp (2 * s) := by
    have h := Real.add_one_le_exp (2 * s)
    linarith
  have hsq : (2 : ℝ) ≤ Real.exp s * Real.exp s := by
    have h2' : (2 : ℝ) ≤ Real.exp (s + s) := by
      simpa [show s + s = 2 * s by ring] using h2s
    rwa [Real.exp_add] at h2'
  have hneg : Real.exp (-s) ≤ Real.exp s / 2 := by
    rw [Real.exp_neg, ← one_div]
    have he : 0 < Real.exp s := Real.exp_pos s
    rw [div_le_iff₀ he]
    have h2' : (2 : ℝ) ≤ Real.exp s * Real.exp s := hsq
    calc (1 : ℝ) = 2 / 2 := by norm_num
      _ ≤ (Real.exp s * Real.exp s) / 2 := by linarith
      _ = (Real.exp s / 2) * Real.exp s := by ring
  have hsinh : Real.exp s / 4 ≤ Real.sinh s := by
    rw [Real.sinh_eq]
    linarith
  linarith

private lemma shapeH_pos {T : ℝ} (hT : 0 < T) : 0 < shapeH T := by
  unfold shapeH
  rw [Real.tanh_eq_sinh_div_cosh]
  exact div_pos (Real.sinh_pos_iff.mpr (div_pos one_pos (by positivity))) (Real.cosh_pos _)

theorem targetPropDeficitGeSq : TargetPropDeficitGeSq := by
  unfold TargetPropDeficitGeSq
  intro T hT hT1
  have hh : 0 < shapeH T := shapeH_pos hT
  have hh1 : shapeH T ≤ 1 := (Real.tanh_lt_one _).le
  have hint := integral_u_sq_sechSq_ge hT hT1
  have hwdef : wGapDeriv T = -(1 / T ^ 2) * ∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T)) := rfl
  have hneg : -wGapDeriv T = (1 / T ^ 2) * ∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T)) := by
    rw [hwdef]
    ring
  have hwabs : (16 / 15) * T ≤ -wGapDeriv T := by
    rw [hneg]
    have hT2 : 0 < T ^ 2 := pow_pos hT 2
    have hdiv : (1 / T ^ 2) * (∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T)))
        = (∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T))) / T ^ 2 := by ring
    rw [hdiv, le_div_iff₀ hT2]
    nlinarith [hint]
  have hend := CQM.Ring15.LockIbp.targetPropShapeEnd T hT
  have habs : |wGapDeriv T| = -wGapDeriv T :=
    abs_of_neg (CQM.Ring15.LockWD.targetPropWGapDerivNeg T hT)
  have hhmw : (8 / 15) * T ^ 2 ≤ shapeH T - wGap T := by
    have heq : shapeH T - wGap T = (T / 2) * (-wGapDeriv T) := by
      unfold shapeH
      rw [← hend, habs]
    rw [heq]
    nlinarith [hwabs, hT]
  have hge : (8 / 15) * T ^ 2 ≤ 1 - wGap T / shapeH T := by
    have hdiv : shapeH T - wGap T ≤ (shapeH T - wGap T) / shapeH T := by
      rw [le_div_iff₀ hh]
      nlinarith [hhmw, hh1]
    have heq2 : (shapeH T - wGap T) / shapeH T = 1 - wGap T / shapeH T := by
      field_simp
    linarith [hdiv, heq2]
  unfold deficitFrac shapePhi
  simpa [shapeH] using hge

theorem targetPropLambdaLeSq : TargetPropLambdaLeSq := by
  unfold TargetPropLambdaLeSq
  intro T hT hT1
  have hs : (10 : ℝ) ≤ 1 / T := by
    rw [le_div_iff₀ hT]
    linarith
  have hsinh := sinh_ge_three_cube hs
  have hform := CQM.Ring15.LockDeficit.targetPropLambdaForm T hT
  rw [hform]
  have hspos : 0 < Real.sinh (1 / T) := Real.sinh_pos_iff.mpr (div_pos one_pos hT)
  have hden : 0 < T * Real.sinh (1 / T) := mul_pos hT hspos
  rw [div_le_iff₀ hden]
  have hcube : (3 : ℝ) ≤ T ^ 3 * Real.sinh (1 / T) := by
    have h3 : 3 * (1 / T) ^ 3 ≤ Real.sinh (1 / T) := hsinh
    have hp : 0 < T ^ 3 := pow_pos hT 3
    have hmul := mul_le_mul_of_nonneg_left h3 (le_of_lt hp)
    have he : T ^ 3 * (3 * (1 / T) ^ 3) = 3 := by
      field_simp
    linarith [hmul, he]
  nlinarith [hcube]

theorem targetPropGapPosNearZero : TargetPropGapPosNearZero := by
  unfold TargetPropGapPosNearZero
  intro T hT hT1
  have hδ : (8 / 15) * T ^ 2 ≤ deficitFrac T := targetPropDeficitGeSq T hT hT1
  have hlam : endpointLambda T ≤ T ^ 2 / 3 := targetPropLambdaLeSq T hT hT1
  have hδpos : 0 < deficitFrac T := by
    have hsq : 0 < T ^ 2 := sq_pos_of_pos hT
    linarith
  have hδle : deficitFrac T ≤ 1 / 3 := CQM.Ring15.LockSecant.targetPropDeficitLeThird T hT
  have hR : deficitFrac T ≤ deficitRatio T := by
    have hdiff : deficitRatio T - deficitFrac T = 2 * deficitFrac T ^ 2 / (1 - deficitFrac T) := by
      have hne : (1 - deficitFrac T) ≠ 0 := by linarith
      unfold deficitRatio
      field_simp [hne]
      try ring_nf
    have hnonneg : 0 ≤ 2 * deficitFrac T ^ 2 / (1 - deficitFrac T) := by
      refine div_nonneg (by positivity) ?_
      linarith
    linarith
  unfold criterionGap
  nlinarith [hδ, hlam, hR]

end

end CQM.Ring15.LockNearZero
