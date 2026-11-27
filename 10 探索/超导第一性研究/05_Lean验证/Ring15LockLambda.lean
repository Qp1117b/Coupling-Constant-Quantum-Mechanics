-- Ring15LockLambda.lean（第 203 轮）：判据两侧的单调性——λ 严格单增、R 严格单增、λ 的值域（G-188b-2h）
-- 只 import Spec ＋已证模块 ＋基线库子模块；无 sorry／admit／自造 axiom。
import Ring15Spec
import Ring15LockDeficit
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp

namespace CQM.Ring15.LockLambda

open MeasureTheory
open scoped Interval
open CQM.Ring15.Spec

noncomputable section

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

/-- $\tanh'=\mathrm{sech}^2$（商法则＋$\cosh^2-\sinh^2=1$）。 -/
private lemma hasDerivAt_tanh (x : ℝ) : HasDerivAt Real.tanh (sechSq x) x := by
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

/-- $\tanh x<x$（$x>0$）：$\tanh x=\int_0^x\mathrm{sech}^2$，而 $\int_0^x(1-\mathrm{sech}^2)=\int_0^x\tanh^2>0$。 -/
private lemma tanh_lt_self {x : ℝ} (hx : 0 < x) : Real.tanh x < x := by
  have hInt : IntervalIntegrable (fun t : ℝ => sechSq t) volume (0 : ℝ) x :=
    cont_sechSq.intervalIntegrable 0 x
  have htanh : ∫ t in (0 : ℝ)..x, sechSq t = Real.tanh x := by
    have hd : ∀ z ∈ Set.uIcc (0 : ℝ) x, HasDerivAt Real.tanh (sechSq z) z :=
      fun z _ => hasDerivAt_tanh z
    have h := intervalIntegral.integral_eq_sub_of_hasDerivAt hd hInt
    simpa using h
  have hpos : 0 < ∫ t in (0 : ℝ)..x, (1 - sechSq t) := by
    have hcont : Continuous fun t : ℝ => 1 - sechSq t :=
      continuous_const.sub cont_sechSq
    refine intervalIntegral.integral_pos hx hcont.continuousOn (fun t ht => ?_)
      ⟨x / 2, ⟨by linarith [hx], by linarith [hx]⟩, ?_⟩
    · have h1 : sechSq t ≤ 1 := sechSq_le_one t
      linarith
    · have hlt : sechSq (x / 2) < 1 := by
        have hxp : 0 < x / 2 := by linarith [hx]
        have hs : 0 < Real.sinh (x / 2) := Real.sinh_pos_iff.mpr hxp
        unfold sechSq
        rw [div_lt_one (pow_pos (Real.cosh_pos (x / 2)) 2)]
        have hc := Real.cosh_sq (x / 2)
        nlinarith [hs, hc]
      simp only [sub_pos]
      exact hlt
  have hsplit : ∫ t in (0 : ℝ)..x, (1 - sechSq t) = x - ∫ t in (0 : ℝ)..x, sechSq t := by
    rw [intervalIntegral.integral_sub intervalIntegrable_const hInt]
    simp
  nlinarith [hpos, hsplit, htanh]

/-- $x<\sinh x$（$x>0$）：由 $\sinh x-x$ 的严格单调性（`Real.sinh_sub_id_strictMono`）。 -/
private lemma self_lt_sinh {x : ℝ} (hx : 0 < x) : x < Real.sinh x := by
  have h := Real.sinh_sub_id_strictMono hx
  simpa using h

/-- $\lambda(T)=F(1/T)$，$F(s)=s/\sinh s$。 -/
private noncomputable def shapeF (s : ℝ) : ℝ := s / Real.sinh s

private lemma F_deriv {s : ℝ} (hs : 0 < s) :
    HasDerivAt shapeF ((Real.sinh s - s * Real.cosh s) / Real.sinh s ^ 2) s := by
  have hne : Real.sinh s ≠ 0 := (Real.sinh_pos_iff.mpr hs).ne'
  have h := (hasDerivAt_id s).div (Real.hasDerivAt_sinh s) hne
  simpa [shapeF] using h

/-- $F$ 在 $(0,\infty)$ 上严格减：$F'<0\iff\sinh s<s\cosh s\iff\tanh s<s$。 -/
private lemma F_strictAnti : StrictAntiOn shapeF (Set.Ioi 0) := by
  have hcont : ContinuousOn shapeF (Set.Ioi 0) :=
    continuous_id.continuousOn.div Real.continuous_sinh.continuousOn
      (fun x hx => (Real.sinh_pos_iff.mpr hx).ne')
  refine strictAntiOn_of_hasDerivWithinAt_neg (D := Set.Ioi 0) (f := shapeF)
    (f' := fun s => (Real.sinh s - s * Real.cosh s) / Real.sinh s ^ 2)
    (convex_Ioi 0) hcont ?_ ?_
  · intro x hx
    have hx' : (0 : ℝ) < x := by simpa using hx
    exact (F_deriv hx').hasDerivWithinAt
  · intro x hx
    have hx' : (0 : ℝ) < x := by simpa using hx
    have hcosh : 0 < Real.cosh x := Real.cosh_pos x
    have hsinh : 0 < Real.sinh x := Real.sinh_pos_iff.mpr hx'
    have hlt : Real.sinh x < x * Real.cosh x := by
      have ht : Real.tanh x < x := tanh_lt_self hx'
      have : Real.sinh x / Real.cosh x < x := by
        rwa [Real.tanh_eq_sinh_div_cosh] at ht
      exact (div_lt_iff₀ hcosh).mp this
    exact div_neg_of_neg_of_pos (by linarith) (by positivity)

/-- **G-188b-2h-2 落地：$\lambda$ 严格单增**。
$\lambda(T)=F(1/T)$（`TargetPropLambdaForm` 的右端改写），$F$ 在 $(0,\infty)$ 严格减、$1/T$ 严格减，
复合即严格增；$\lambda$ 从此是 $T$ 的严格增函数。 -/
theorem targetPropLambdaStrictMono : CQM.Ring15.Spec.TargetPropLambdaStrictMono := by
  intro T₁ T₂ h1 h2
  have hlt : 1 / T₂ < 1 / T₁ := one_div_lt_one_div_of_lt h1 h2
  have hu1 : (1 / T₁ : ℝ) ∈ Set.Ioi 0 := by
    show (0 : ℝ) < 1 / T₁
    exact one_div_pos.mpr h1
  have hu2 : (1 / T₂ : ℝ) ∈ Set.Ioi 0 := by
    show (0 : ℝ) < 1 / T₂
    exact one_div_pos.mpr (lt_trans h1 h2)
  have hanti := F_strictAnti hu2 hu1 hlt
  have hl1 := CQM.Ring15.LockDeficit.targetPropLambdaForm T₁ h1
  have hl2 := CQM.Ring15.LockDeficit.targetPropLambdaForm T₂ (lt_trans h1 h2)
  have e1 : endpointLambda T₁ = shapeF (1 / T₁) := by
    rw [hl1]
    unfold shapeF
    field_simp
  have e2 : endpointLambda T₂ = shapeF (1 / T₂) := by
    rw [hl2]
    unfold shapeF
    field_simp
  rw [e1, e2]
  exact hanti

/-- **G-188b-2h-3 落地：$0<\lambda(T)<1$**。
$\lambda=s/\sinh s$，$s=1/T>0$；$0<s<\sinh s$ 给出下界与上界各一条。 -/
theorem targetPropLambdaBounds : CQM.Ring15.Spec.TargetPropLambdaBounds := by
  intro T hT
  have hx : 0 < 1 / T := by positivity
  have hsinh : 0 < Real.sinh (1 / T) := Real.sinh_pos_iff.mpr hx
  have hl := CQM.Ring15.LockDeficit.targetPropLambdaForm T hT
  constructor
  · rw [hl]
    exact div_pos one_pos (mul_pos hT hsinh)
  · rw [hl, div_lt_one (mul_pos hT hsinh)]
    have hsinhgt : (1 : ℝ) / T < Real.sinh (1 / T) := self_lt_sinh hx
    have hmul : (1 : ℝ) < T * Real.sinh (1 / T) := by
      have h := mul_lt_mul_of_pos_left hsinhgt hT
      have hT1 : T * (1 / T) = 1 := by field_simp
      rwa [hT1] at h
    exact hmul

/-- **G-188b-2h-1 落地：$R(\delta)$ 在 $(0,1)$ 上严格单增**。
差 $=\dfrac{(b-a)(1+a+b-ab)}{(1-a)(1-b)}$，$b-a>0$、$1+a+b-ab>0$（因 $ab<b<1$）、分母 $>0$。 -/
theorem targetPropDeficitRatioMono : CQM.Ring15.Spec.TargetPropDeficitRatioMono := by
  intro a b ha hab hb1
  have h1 : 0 < 1 - a := by linarith
  have h2 : 0 < 1 - b := by linarith
  rw [div_lt_div_iff₀ h1 h2]
  have hab1 : a * b < 1 := by
    have h : a * b < a * 1 := by
      exact mul_lt_mul_of_pos_left hb1 ha
    linarith
  have key : 0 < (b - a) * (1 + a + b - a * b) := by
    have hba : 0 < b - a := by linarith
    have : 0 < 1 + a + b - a * b := by nlinarith [ha, hb1, hab1]
    exact mul_pos hba this
  nlinarith [key]

end

end CQM.Ring15.LockLambda
