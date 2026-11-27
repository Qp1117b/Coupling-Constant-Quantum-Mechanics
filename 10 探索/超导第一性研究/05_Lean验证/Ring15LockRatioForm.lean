-- Ring15LockRatioForm.lean（第 214 轮）：R(delta) 与 Q = lambda/R(delta) 的正性
-- 只 import Spec ＋已证模块；无 sorry／admit／自造 axiom。
import Ring15Spec
import Ring15LockW
import Ring15LockIbp
import Ring15LockLambda

namespace CQM.Ring15.LockRatioForm

open CQM.Ring15.Spec

noncomputable section

private lemma tanh_pos_of_pos {x : ℝ} (hx : 0 < x) : 0 < Real.tanh x := by
  rw [Real.tanh_eq_sinh_div_cosh]
  exact div_pos (Real.sinh_pos_iff.mpr hx) (Real.cosh_pos x)

/-- $R(\delta)>0$：$\delta\in(0,1)$ ⇒ $\dfrac{\delta(1+\delta)}{1-\delta}>0$。 -/
theorem targetPropDeficitRatioPos : TargetPropDeficitRatioPos := by
  intro T hT
  have harg : 0 < 1 / (2 * T) := by positivity
  have hh : 0 < shapeH T := by
    unfold shapeH
    exact tanh_pos_of_pos harg
  have hw : 0 < wGap T := CQM.Ring15.LockW.targetPropWGapPos T hT
  have hlt : wGap T < shapeH T := by
    unfold shapeH
    exact CQM.Ring15.LockIbp.targetPropShapeEndGt T hT
  have hltT : wGap T < Real.tanh (1 / (2 * T)) := hlt
  have hdiv : wGap T / Real.tanh (1 / (2 * T)) < 1 := (div_lt_one hh).mpr hltT
  have hd : 0 < deficitFrac T := by
    simp only [deficitFrac, shapePhi]
    linarith
  have hphi : 0 < shapePhi T := by
    simp only [shapePhi]
    exact div_pos hw hh
  have hack : 0 < 1 - deficitFrac T := by
    simp only [deficitFrac]
    linarith
  have hd1 : (0 : ℝ) < 1 + deficitFrac T := by linarith
  unfold deficitRatio
  exact div_pos (mul_pos hd hd1) hack

/-- $Q>0$：$\lambda>0$（202 界）与 $R>0$（本环上一条）⇒ 商正。 -/
theorem targetPropRatioOverLambdaPos : TargetPropRatioOverLambdaPos := by
  intro T hT
  have hlam : 0 < endpointLambda T :=
    (CQM.Ring15.LockLambda.targetPropLambdaBounds T hT).1
  have hR : 0 < deficitRatio T := targetPropDeficitRatioPos T hT
  unfold ratioOverLambda
  exact div_pos hlam hR

end

end CQM.Ring15.LockRatioForm

