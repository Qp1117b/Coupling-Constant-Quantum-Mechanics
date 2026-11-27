-- Ring15LockGapDeriv.lean（第 205 轮）：判据差的导数结构——λ 的导数、阈值函数的导数与 D 的导数（G-188b-2j 前件）
-- 只 import Spec ＋已证模块 ＋基线库子模块；无 sorry／admit／自造 axiom。
import Ring15Spec
import Ring15LockDeficitMono
import Ring15LockLambda
import Ring15LockDeficit
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp

namespace CQM.Ring15.LockGapDeriv

open CQM.Ring15.Spec

noncomputable section

/-- $h(T)=\tanh\frac1{2T}>0$（$T>0$）。 -/
private lemma shapeH_pos' {T : ℝ} (hT : 0 < T) : 0 < shapeH T := by
  unfold shapeH
  rw [Real.tanh_eq_sinh_div_cosh]
  exact div_pos ((Real.sinh_pos_iff).mpr (div_pos one_pos (by positivity))) (Real.cosh_pos (1 / (2 * T)))

/-- $\delta=1-\Phi=1-w/h$（定义展开）。 -/
private lemma deficit_eq' (T : ℝ) : deficitFrac T = 1 - wGap T / shapeH T := by
  unfold deficitFrac shapePhi
  rfl

/-- $\lambda$ 的写法 $1/(T\sinh\frac1T)$ 对 $T$ 的导数（`TargetPropLambdaForm` 的右端）。 -/
private lemma hasDerivAt_lambdaVal {T : ℝ} (hT : 0 < T) :
    HasDerivAt (fun T : ℝ => 1 / (T * Real.sinh (1 / T)))
      ((Real.cosh (1 / T) / T - Real.sinh (1 / T)) / (T * Real.sinh (1 / T)) ^ 2) T := by
  have hTne : T ≠ 0 := ne_of_gt hT
  have hinv : HasDerivAt (fun T : ℝ => T⁻¹) (-(T ^ 2)⁻¹) T := hasDerivAt_inv hTne
  have hsinh : HasDerivAt (fun s : ℝ => Real.sinh s) (Real.cosh (T⁻¹)) (T⁻¹) :=
    Real.hasDerivAt_sinh (T⁻¹)
  have hcomp := hsinh.comp T hinv
  have hprod := (hasDerivAt_id T).mul hcomp
  have hv : (1 * (((fun s : ℝ => Real.sinh s)) ∘ Inv.inv) T
        + id T * (Real.cosh (T⁻¹) * (-(T ^ 2)⁻¹)))
      = Real.sinh (T⁻¹) + T * (Real.cosh (T⁻¹) * (-(T ^ 2)⁻¹)) := by
    simp only [Function.comp_apply, id_eq, one_mul]
  rw [hv] at hprod
  have hval0 : (Real.sinh (T⁻¹) + T * (Real.cosh (T⁻¹) * (-(T ^ 2)⁻¹)))
      = Real.sinh (T⁻¹) - Real.cosh (T⁻¹) / T := by
    have hsq : T ^ 2 ≠ 0 := pow_ne_zero 2 hTne
    field_simp
    ring
  rw [hval0] at hprod
  have hsinhne : Real.sinh (T⁻¹) ≠ 0 :=
    ne_of_gt ((Real.sinh_pos_iff).mpr (by simpa using (inv_pos.mpr hT)))
  have hne : T * Real.sinh (T⁻¹) ≠ 0 := mul_ne_zero hTne hsinhne
  have hdiv0 := (hasDerivAt_const (x := T) (c := 1)).div hprod hne
  have hdiv' : HasDerivAt (fun T : ℝ => 1 / (T * Real.sinh (T⁻¹)))
      ((0 * (T * Real.sinh (T⁻¹))
        - 1 * (Real.sinh (T⁻¹) - Real.cosh (T⁻¹) / T))
      / (T * Real.sinh (T⁻¹)) ^ 2) T := hdiv0
  have hfun : (fun T : ℝ => 1 / (T * Real.sinh (T⁻¹)))
      = (fun T : ℝ => 1 / (T * Real.sinh (1 / T))) := by
    funext x
    simp only [one_div]
  rw [hfun] at hdiv'
  have hval : (0 * (T * Real.sinh (T⁻¹))
        - 1 * (Real.sinh (T⁻¹) - Real.cosh (T⁻¹) / T))
      / (T * Real.sinh (T⁻¹)) ^ 2
      = (Real.cosh (1 / T) / T - Real.sinh (1 / T)) / (T * Real.sinh (1 / T)) ^ 2 := by
    rw [one_div]
    have hsq : (T * Real.sinh (T⁻¹)) ^ 2 ≠ 0 := pow_ne_zero 2 hne
    field_simp
    ring
  rw [hval] at hdiv'
  exact hdiv'

/-- **G-188b-2j-1 落地**：`endpointLambda` 的导数即 `lambdaDeriv`（用 `TargetPropLambdaForm` 转到 $1/(T\sinh\frac1T)$ 写法）。 -/
private lemma hasDerivAt_endpointLambda {T : ℝ} (hT : 0 < T) :
    HasDerivAt (fun T : ℝ => endpointLambda T) (lambdaDeriv T) T := by
  have hbase := hasDerivAt_lambdaVal hT
  have hmem : Set.Ioi (0 : ℝ) ∈ nhds T := isOpen_Ioi.mem_nhds hT
  have hEq : (fun T : ℝ => endpointLambda T)
      =ᶠ[nhds T] (fun T : ℝ => 1 / (T * Real.sinh (1 / T))) :=
    Filter.Eventually.mono hmem
      (fun s hs => CQM.Ring15.LockDeficit.targetPropLambdaForm s (by simpa using hs))
  exact hbase.congr_of_eventuallyEq hEq

/-- **G-188b-2j-2 落地**：阈值函数 $x\mapsto x(1+x)/(1-x)$ 的导数 $=(1+2x-x^2)/(1-x)^2$。 -/
private lemma hasDerivAt_ratioFun {x : ℝ} (hx : x ≠ 1) :
    HasDerivAt ratioFun (ratioFunDeriv x) x := by
  have hone : HasDerivAt (fun y : ℝ => 1 + y) 1 x := by
    have h := (hasDerivAt_const (x := x) (c := 1)).add (hasDerivAt_id x)
    have hf : ((fun _ : ℝ => (1 : ℝ)) + id) = fun y : ℝ => 1 + y := by funext y; simp
    have hv : (0 : ℝ) + 1 = 1 := by norm_num
    rw [hf, hv] at h
    exact h
  have hn : HasDerivAt (fun y : ℝ => y * (1 + y)) (1 + 2 * x) x := by
    have h := (hasDerivAt_id x).mul hone
    have hf : (id * fun y : ℝ => 1 + y) = fun y : ℝ => y * (1 + y) := by funext y; simp
    have hv : (1 * (1 + x) + id x * 1) = 1 + 2 * x := by simp only [id_eq]; ring
    rw [hf, hv] at h
    exact h
  have hd : HasDerivAt (fun y : ℝ => 1 - y) (-1) x := by
    have h := (hasDerivAt_const (x := x) (c := 1)).sub (hasDerivAt_id x)
    have hf : ((fun _ : ℝ => (1 : ℝ)) - id) = fun y : ℝ => 1 - y := by funext y; simp
    have hv : (0 : ℝ) - 1 = -1 := by norm_num
    rw [hf, hv] at h
    exact h
  have hxne : 1 - x ≠ 0 := by
    intro h
    exact hx (by linarith)
  have hq := hn.div hd hxne
  have hval : ((1 + 2 * x) * (1 - x) - x * (1 + x) * (-1)) / (1 - x) ^ 2
      = ratioFunDeriv x := by
    unfold ratioFunDeriv
    have hsq : (1 - x) ^ 2 ≠ 0 := pow_ne_zero 2 hxne
    field_simp
    ring
  rw [hval] at hq
  exact hq

/-- 阈值与亏损分数的复合：`deficitRatio` 即 `ratioFun ∘ deficitFrac` 的导数。 -/
private lemma hasDerivAt_deficitRatio {T : ℝ} (hT : 0 < T) :
    HasDerivAt (fun T : ℝ => deficitRatio T)
      (ratioFunDeriv (deficitFrac T) * deficitDeriv T) T := by
  have hwpos : 0 < wGap T := CQM.Ring15.LockW.targetPropWGapPos T hT
  have hhpos : 0 < shapeH T := shapeH_pos' hT
  have hδne : deficitFrac T ≠ 1 := by
    intro h
    have hq : wGap T / shapeH T = 0 := by
      rw [deficit_eq' T] at h
      linarith
    exact (div_ne_zero (ne_of_gt hwpos) (ne_of_gt hhpos)) hq
  have hR := (hasDerivAt_ratioFun hδne).comp T
    (CQM.Ring15.LockDeficitMono.targetPropDeficitDeriv T hT)
  have hfun : (ratioFun ∘ deficitFrac) = (fun T : ℝ => deficitRatio T) := rfl
  rw [hfun] at hR
  exact hR

/-- **G-188b-2j-3 落地**：判据差 $D=R(\delta)-\lambda$ 的导数 $=R'(\delta)\delta'-\lambda'$。 -/
private lemma hasDerivAt_criterionGap {T : ℝ} (hT : 0 < T) :
    HasDerivAt criterionGap (criterionGapDeriv T) T := by
  have hR := hasDerivAt_deficitRatio hT
  have hl := hasDerivAt_endpointLambda hT
  exact hR.sub hl

theorem targetPropLambdaDeriv : CQM.Ring15.Spec.TargetPropLambdaDeriv := by
  intro T hT
  exact hasDerivAt_endpointLambda hT

theorem targetPropRatioFunDeriv : CQM.Ring15.Spec.TargetPropRatioFunDeriv := by
  intro x hx
  exact hasDerivAt_ratioFun hx

theorem targetPropCriterionGapDeriv : CQM.Ring15.Spec.TargetPropCriterionGapDeriv := by
  intro T hT
  exact hasDerivAt_criterionGap hT

end

end CQM.Ring15.LockGapDeriv
