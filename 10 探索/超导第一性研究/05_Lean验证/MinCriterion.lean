import Mathlib.Tactic.Linarith
import Mathlib.Data.Real.Basic

/-!
# R16: (目标.1) ≤min 判据结构的代数核（依据历史唯物主义 §2.3 回溯必然）

- 回溯必然：P ⇒ C1 ∧ C2 ∧ C3
- 条件给温度上限：Ci ⇒ T ≤ Ti
- 合取 ⇒ T ≤ min{T1,T2,T3}
- 前瞻偶然：C_i 全真但 P 假 是可能的（不推出等号）
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.MinCriterion

noncomputable section

/-- 三个温度上限的合取 ⇒ T ≤ min。 -/
theorem three_uppers_to_min (T T1 T2 T3 : ℝ)
    (h1 : T ≤ T1) (h2 : T ≤ T2) (h3 : T ≤ T3) :
    T ≤ min T1 (min T2 T3) := by
  exact le_min h1 (le_min h2 h3)

/-- 回溯必然的三条件合取：P ⇒ (C1 ∧ C2 ∧ C3) ⇒ 三个温度上限。 -/
theorem backward_necessity
    (P C1 C2 C3 : Prop) (T T1 T2 T3 : ℝ)
    (hPC : P → C1 ∧ C2 ∧ C3)
    (hC1 : C1 → T ≤ T1) (hC2 : C2 → T ≤ T2) (hC3 : C3 → T ≤ T3) :
    P → T ≤ min T1 (min T2 T3) := by
  intro hP
  have hc := hPC hP
  exact three_uppers_to_min T T1 T2 T3 (hC1 hc.1) (hC2 hc.2.1) (hC3 hc.2.2)

/-- 前瞻偶然：条件全具备并不推出相变发生（等号不可由回溯必然得）。 -/
-- 用一个谓词模型承载：C1∧C2∧C3 真而 P 假是可能的。
theorem forward_contingency_possible :
    ∃ (P C1 C2 C3 : Prop), (C1 ∧ C2 ∧ C3) ∧ ¬ P := by
  refine ⟨False, True, True, True, ?_⟩
  exact ⟨⟨trivial, trivial, trivial⟩, by simp⟩

/-- min 的温度上限语义：“相变温度不超过最严的那支”。 -/
theorem tc_upper_by_min (Tc Tstar TBKT Ttheta : ℝ)
    (h : Tc ≤ min Tstar (min TBKT Ttheta)) :
    Tc ≤ Tstar ∧ Tc ≤ TBKT ∧ Tc ≤ Ttheta := by
  constructor
  · exact le_trans h (min_le_left _ _)
  constructor
  · exact le_trans h (le_trans (min_le_right _ _) (min_le_left _ _))
  · exact le_trans h (le_trans (min_le_right _ _) (min_le_right _ _))

end
end CQM.MinCriterion
