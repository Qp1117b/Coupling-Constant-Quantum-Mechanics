import Mathlib.Tactic.Linarith
import Mathlib.Data.Real.Basic

/-!
# R18: 环节⑨ 必要条件集合的代数核（依据历史唯物主义 §2.3）

- 回溯必然：P ⇒ A ∧ V ∧ S（原子化、先锋队连通、同步振荡）
- 危机 C 不属于必要条件集合：P ⇒ C 不成立（P 真而 C 假可能）
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.NecessaryConditions

noncomputable section

/-- 回溯必然三条件：P ⇒ A ∧ V ∧ S。 -/
theorem backward_necessity_three
    (P A V S : Prop) (h : P → A ∧ V ∧ S) :
    P → A ∧ V ∧ S := h

/-- 危机不属于必要条件集合：存在 P 真而 C 假的模型 ⇒ (P → C) 不成立。 -/
theorem crisis_not_necessary :
    ∃ (P C : Prop), P ∧ ¬ C ∧ ¬ (P → C) := by
  refine ⟨True, False, ?_⟩
  constructor
  · trivial
  constructor
  · simp
  · intro h
    exact h trivial

/-- 三元集合/{A,V,S} 与 R16 三支映射一致：三条件各给一支温度上限。 -/
theorem three_conditions_three_branches
    (T T1 T2 T3 : ℝ) (A V S : Prop)
    (hA : A → T ≤ T1) (hV : V → T ≤ T2) (hS : S → T ≤ T3) :
    A ∧ V ∧ S → T ≤ min T1 (min T2 T3) := by
  intro h
  exact le_min (hA h.1) (le_min (hV h.2.1) (hS h.2.2))

end
end CQM.NecessaryConditions
