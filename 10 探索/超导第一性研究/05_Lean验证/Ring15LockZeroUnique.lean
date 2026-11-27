-- Ring15LockZeroUnique.lean（第 213 轮）：零点唯一性的条件合成
-- 若 Q = lambda/R(delta) 在 [1/10,1] 上严格单增，则 D 在该区间内恰有一个零点。
-- 只 import Spec ＋已证模块；无 sorry／admit／自造 axiom。
import Ring15Spec
import Ring15LockZeroExists
import Ring15LockLambda

namespace CQM.Ring15.LockZeroUnique

open CQM.Ring15.Spec

noncomputable section

/-- 判据差为零时，$Q=\lambda/R$ 等于 1。只消费 $\lambda>0$（`targetPropLambdaBounds`）。 -/
private lemma ratioOverLambda_eq_one_of_gap_zero (T : ℝ) (hT : 0 < T)
    (h : criterionGap T = 0) : ratioOverLambda T = 1 := by
  have hb := CQM.Ring15.LockLambda.targetPropLambdaBounds T hT
  have hpos : 0 < endpointLambda T := hb.1
  have h' := h
  unfold criterionGap at h'
  have heq : endpointLambda T = deficitRatio T := by linarith
  have hne : deficitRatio T ≠ 0 := by
    rw [← heq]
    exact ne_of_gt hpos
  unfold ratioOverLambda
  rw [heq]
  exact div_self hne

theorem targetPropGapZeroUniqueOfRatioMono : TargetPropGapZeroUniqueOfRatioMono := by
  intro hmono
  obtain ⟨T0, hT0a, hT0b, hT0c⟩ := CQM.Ring15.LockZeroExists.targetPropGapZeroExists
  have hT0 : (0 : ℝ) < T0 := lt_trans (by norm_num) hT0a
  have hQ0 : ratioOverLambda T0 = 1 := ratioOverLambda_eq_one_of_gap_zero T0 hT0 hT0c
  refine ⟨T0, ⟨⟨hT0a, hT0b, hT0c⟩, ?_⟩⟩
  intro y hy
  obtain ⟨hy1, hy2, hy3⟩ := hy
  have hypos : (0 : ℝ) < y := lt_trans (by norm_num) hy1
  have hQy : ratioOverLambda y = 1 := ratioOverLambda_eq_one_of_gap_zero y hypos hy3
  rcases lt_trichotomy y T0 with hlt | heq | hgt
  · exfalso
    have hm := hmono y T0 (le_of_lt hy1) hlt (le_of_lt hT0b)
    linarith
  · exact heq
  · exfalso
    have hm := hmono T0 y (le_of_lt hT0a) hgt (le_of_lt hy2)
    linarith

end

end CQM.Ring15.LockZeroUnique

