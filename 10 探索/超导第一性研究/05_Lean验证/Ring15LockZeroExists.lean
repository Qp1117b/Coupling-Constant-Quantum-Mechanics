-- Ring15LockZeroExists.lean（第 212 轮）：判据差在 (1/10,1) 内的零点存在性
-- 只 import Spec ＋已证模块 ＋基线库；无 sorry／admit／自造 axiom。
import Ring15Spec
import Ring15LockGapDeriv
import Ring15LockSecant
import Ring15LockNearZero
import Mathlib.Topology.Order.IntermediateValue

namespace CQM.Ring15.LockZeroExists

open CQM.Ring15.Spec

noncomputable section

theorem targetPropGapZeroExists : TargetPropGapZeroExists := by
  have hcont : ContinuousOn criterionGap (Set.Icc (1 / 10 : ℝ) 1) := by
    intro x hx
    have hx0 : (0 : ℝ) < x := lt_of_lt_of_le (by norm_num) hx.1
    exact (CQM.Ring15.LockGapDeriv.targetPropCriterionGapDeriv x hx0).continuousAt.continuousWithinAt
  have hpos : 0 < criterionGap (1 / 10 : ℝ) :=
    CQM.Ring15.LockNearZero.targetPropGapPosNearZero (1 / 10) (by norm_num) (by norm_num)
  have hneg : criterionGap 1 < 0 :=
    CQM.Ring15.LockSecant.targetPropGapNegTail 1 (by norm_num) (by norm_num)
  have hmem : (0 : ℝ) ∈ Set.Icc (criterionGap 1) (criterionGap (1 / 10 : ℝ)) := by
    constructor
    · exact le_of_lt hneg
    · exact le_of_lt hpos
  have hsub := intermediate_value_Icc' (show (1 / 10 : ℝ) ≤ 1 by norm_num) hcont
  obtain ⟨x, hx, hval⟩ := hsub hmem
  refine ⟨x, ?_, ?_, hval⟩
  · rcases lt_or_eq_of_le hx.1 with hlt | heq
    · exact hlt
    · exfalso
      rw [heq.symm] at hval
      linarith
  · rcases lt_or_eq_of_le hx.2 with hlt | heq
    · exact hlt
    · exfalso
      rw [heq] at hval
      linarith

end

end CQM.Ring15.LockZeroExists
