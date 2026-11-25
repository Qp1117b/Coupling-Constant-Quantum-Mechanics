-- 环 15 / 审-6：m_lock=1 的证明模块（第 162 轮）
-- 独立路径：import Ring15Spec（spec 只含定义），主定理类型由 Spec 的 TargetProp 给出，
-- 保证"证明的对象"与"Spec 写的目标"是同一个 Prop（非同名重定义）。
import Ring15Spec

set_option autoImplicit false

open CQM.Ring15.Spec

namespace CQM.Ring15.LockMult

/-- 键的基数最多为 1：`Finset.filter (· = y)` 的基数上界（简单图编码的直接后果）。 -/
theorem card_filter_le_one (edges : BondGraph) (y : Edge) :
    (edges.filter (fun e => e = y)).card ≤ 1 := by
  have hsub : edges.filter (fun e => e = y) ⊆ {y} := by
    intro x hx
    rw [Finset.mem_singleton]
    exact (Finset.mem_filter.mp hx).2
  have h := Finset.card_le_card hsub
  simpa using h

/-- 锁定重数恒不超过 1（`m_lock ≤ 1` 这一半由键图编码承担，不由 0/1 值函数承担）。 -/
theorem lockMult_le_one (edges : BondGraph) (a b : ℕ) : lockMult edges a b ≤ 1 := by
  unfold lockMult
  by_cases hab : a = b
  · rw [if_pos hab]
    exact Nat.zero_le 1
  · rw [if_neg hab]
    exact card_filter_le_one edges (Sym2.mk a b)

/-- 锁定重数恰为 1 当且仅当该对之间存在键（`m_lock ≥ 1` 这一半要求键存在，不再是定义展开）。 -/
theorem lockMult_eq_one_iff (edges : BondGraph) (a b : ℕ) (hab : a ≠ b) :
    lockMult edges a b = 1 ↔ Adj edges a b := by
  unfold lockMult
  rw [if_neg hab]
  constructor
  · intro h
    have hpos : 0 < (edges.filter (fun e => e = Sym2.mk a b)).card := by
      rw [h]
      exact Nat.zero_lt_one
    have hne : (edges.filter (fun e => e = Sym2.mk a b)).Nonempty := Finset.card_pos.mp hpos
    obtain ⟨x, hx⟩ := hne
    rw [Finset.mem_filter] at hx
    show Sym2.mk a b ∈ edges
    rw [← hx.2]
    exact hx.1
  · intro h
    have hmem : Sym2.mk a b ∈ edges.filter (fun e => e = Sym2.mk a b) := by
      rw [Finset.mem_filter]
      exact ⟨h, rfl⟩
    have hpos : 0 < (edges.filter (fun e => e = Sym2.mk a b)).card :=
      Finset.card_pos.mpr ⟨_, hmem⟩
    have hle := card_filter_le_one edges (Sym2.mk a b)
    exact Nat.le_antisymm hle (Nat.succ_le_of_lt hpos)

/-- 本环主定理：与 Spec 的 `TargetProp` 同一命题（非同名重定义）。 -/
theorem targetProp : TargetProp := by
  intro edges a b hab
  exact ⟨lockMult_eq_one_iff edges a b hab, lockMult_le_one edges a b⟩

/-- 第 159 轮声称的 `m_lock = 1`：由已占相邻两点间的诱导键给出，且消费 `TargetProp` 的 iff 那一半。 -/
theorem mLock_eq_one (s : ℕ → Bool) (edges : BondGraph) (a b : ℕ)
    (hab : a ≠ b) (hb : InducedBond s edges a b) : lockMult edges a b = 1 :=
  (lockMult_eq_one_iff edges a b hab).mpr hb.1

end CQM.Ring15.LockMult

#print axioms CQM.Ring15.LockMult.targetProp
#print axioms CQM.Ring15.LockMult.mLock_eq_one
#print axioms CQM.Ring15.LockMult.lockMult_eq_one_iff
#check @CQM.Ring15.LockMult.targetProp
