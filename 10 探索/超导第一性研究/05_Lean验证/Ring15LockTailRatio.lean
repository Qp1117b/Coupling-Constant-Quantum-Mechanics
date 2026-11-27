-- Ring15LockTailRatio.lean（第 209 轮）：尾段的代数合成（G-188b-2k 前件）
-- 只 import Spec ＋已证模块 ＋基线库子模块；无 sorry／admit／自造 axiom。
-- 内容：R(x)≤2/3（x≤1/3）；δ≤1/3 且 T≥1 ⇒ D<0。
-- 限界：**不含** δ≤1/3 的证明（需 tanh 凹性），故尾段排除仍差这一件。
import Ring15Spec
import Ring15LockIbp
import Ring15LockTail
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp

namespace CQM.Ring15.LockTailRatio

open CQM.Ring15.Spec

noncomputable section

/-- $h(T)=\tanh\frac1{2T}>0$（$T>0$）。 -/
private lemma shapeH_pos {T : ℝ} (hT : 0 < T) : 0 < shapeH T := by
  unfold shapeH
  rw [Real.tanh_eq_sinh_div_cosh]
  exact div_pos (Real.sinh_pos_iff.mpr (div_pos one_pos (by positivity))) (Real.cosh_pos _)

/-- $\delta(T)>0$（$T>0$）：端点严格高于窗口平均（`TargetPropShapeEndGt`）。 -/
private lemma deficit_pos {T : ℝ} (hT : 0 < T) : 0 < deficitFrac T := by
  unfold deficitFrac shapePhi
  have hw : wGap T < shapeH T := CQM.Ring15.LockIbp.targetPropShapeEndGt T hT
  have hh : 0 < shapeH T := shapeH_pos hT
  have hlt : wGap T / shapeH T < 1 := by
    rw [div_lt_iff₀ hh]
    simpa using hw
  have hlt' : wGap T / Real.tanh (1 / (2 * T)) < 1 := by simpa [shapeH] using hlt
  linarith

/-- $0<x\le\frac13\Rightarrow\frac{x(1+x)}{1-x}\le\frac23$。 -/
theorem targetPropRatioLeOfLeThird : TargetPropRatioLeOfLeThird := by
  unfold TargetPropRatioLeOfLeThird ratioFun
  intro x hx hx3
  have h1 : (0 : ℝ) < 1 - x := by linarith
  rw [div_le_iff₀ h1]
  have hsq : 3 * x ^ 2 ≤ x := by nlinarith [hx, hx3]
  have hpoly : 3 * x ^ 2 + 5 * x - 2 ≤ 0 := by nlinarith [hsq, hx3]
  nlinarith [hpoly]

/-- $\delta\le\frac13$ 且 $T\ge1$ $\Rightarrow D(T)<0$。 -/
theorem targetPropGapNegOfDeficitLeThird : TargetPropGapNegOfDeficitLeThird := by
  unfold TargetPropGapNegOfDeficitLeThird
  intro T hT hδ hT1
  have hδpos : 0 < deficitFrac T := deficit_pos hT
  have hR : deficitRatio T ≤ 2 / 3 := by
    have h := targetPropRatioLeOfLeThird (deficitFrac T) hδpos hδ
    simpa [deficitRatio, ratioFun] using h
  have hlam : 2 / 3 < endpointLambda T := CQM.Ring15.LockTail.targetPropLambdaTailGt T hT1
  unfold criterionGap
  linarith

end

end CQM.Ring15.LockTailRatio
