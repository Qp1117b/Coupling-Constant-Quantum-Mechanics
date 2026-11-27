-- Ring15LockTail.lean（第 208 轮）：尾段下界的 λ 一侧（G-188b-2k 前件）
-- 只 import Spec ＋已证模块 ＋基线库子模块；无 sorry／admit／自造 axiom。
-- 内容：sinh 1 < 3/2、λ(1)=1/sinh 1、T≥1 ⇒ 2/3 < λ(T)。
-- 限界：本模块**不含** R(δ)<2/3 一侧，故不构成 T≥1 ⇒ D<0 的完整证明。
import Ring15Spec
import Ring15LockDeficit
import Ring15LockLambda
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp
import Mathlib.Algebra.Order.GroupWithZero.Unbundled.Basic

namespace CQM.Ring15.LockTail

open CQM.Ring15.Spec

noncomputable section

/-- $\sinh1<3/2$：$\sinh1=\frac{e-e^{-1}}2$，由 $e<3$ 与 $e^{-1}>0$ 夹住。 -/
theorem targetPropSinhOneLt : TargetPropSinhOneLt := by
  unfold TargetPropSinhOneLt
  rw [Real.sinh_eq]
  have h3 : Real.exp 1 < 3 := Real.exp_one_lt_three
  have hp : 0 < Real.exp (-1) := Real.exp_pos (-1)
  linarith

/-- $\lambda(1)=1/\sinh1$：由 `TargetPropLambdaForm` 在 $T=1$ 处取值。 -/
theorem targetPropLambdaOne : TargetPropLambdaOne := by
  unfold TargetPropLambdaOne
  have h := CQM.Ring15.LockDeficit.targetPropLambdaForm 1 (by norm_num)
  simpa using h

/-- $T\ge1\Rightarrow\frac23<\lambda(T)$：$\lambda(1)=\frac1{\sinh1}>\frac23$ ＋ $\lambda$ 严格单增。 -/
theorem targetPropLambdaTailGt : TargetPropLambdaTailGt := by
  unfold TargetPropLambdaTailGt
  intro T hT
  have hs3 : Real.sinh 1 < 3 / 2 := targetPropSinhOneLt
  have hp : 0 < Real.sinh 1 := Real.sinh_pos_iff.mpr (by norm_num)
  have hval : (2 : ℝ) / 3 < endpointLambda 1 := by
    rw [targetPropLambdaOne]
    rw [div_lt_div_iff₀ (by norm_num : (0 : ℝ) < 3) hp]
    linarith
  rcases lt_or_eq_of_le hT with hlt | heq
  · have hmono := CQM.Ring15.LockLambda.targetPropLambdaStrictMono 1 T (by norm_num) hlt
    linarith
  · rw [show T = 1 from heq.symm]
    exact hval

end

end CQM.Ring15.LockTail
