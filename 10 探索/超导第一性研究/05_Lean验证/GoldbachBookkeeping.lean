import Mathlib.Data.Int.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Card
import Mathlib.Tactic.Ring

/-!
# R34: 13.A5 配对供给的有限集组合记账（临-26 子项·隔离区）

用整数 ℤ 做 M-p（避免 Nat 减法饱和）。S 为有限标号集（质数化∪孤狼）。
- r_ord(M,S) = #{p∈S : M-p∈S}（有序表示数）
- 上界 r_ord ≤ |S|（单射 p↦(p,M-p)）
- 对称性 p∈set ⟺ M-p∈set（对合）
- 对角对存在：若 M=2m 且 m∈S，则 m 是表示
Goldbach 按外部假设使用，本文件只做条件内部的组合记账。
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.GoldbachBookkeeping

/-- 有序表示数集合：{p∈S : M-p∈S}。 -/
def reprSet (M : ℤ) (S : Finset ℤ) : Finset ℤ := S.filter (fun p => M - p ∈ S)

/-- 有序表示数。 -/
def rOrd (M : ℤ) (S : Finset ℤ) : ℕ := (reprSet M S).card

/-- 上界：r_ord ≤ |S|（filter 是子集）。 -/
theorem rOrd_le_card (M : ℤ) (S : Finset ℤ) : rOrd M S ≤ S.card := by
  unfold rOrd reprSet
  exact Finset.card_filter_le S (fun p => M - p ∈ S)

/-- 对称性：p 在表示集中 ⟺ M-p 在表示集中（对合 p↦M-p）。 -/
theorem symm_mem (M p : ℤ) (S : Finset ℤ) : p ∈ reprSet M S ↔ M - p ∈ reprSet M S := by
  unfold reprSet
  simp only [Finset.mem_filter]
  have hinv : M - (M - p) = p := by ring
  constructor
  · intro h
    rcases h with ⟨hpS, hMpS⟩
    exact ⟨hMpS, by simpa [hinv] using hpS⟩
  · intro h
    rcases h with ⟨hMpS, hpS⟩
    exact ⟨by simpa [hinv] using hpS, hMpS⟩

/-- 对角对存在：若 M=2m 且 m∈S，则 m∈reprSet（因为 M-m=m∈S）。 -/
theorem diagonal_mem (M m : ℤ) (S : Finset ℤ) (hM : M = 2 * m) (hm : m ∈ S) :
    m ∈ reprSet M S := by
  unfold reprSet
  simp only [Finset.mem_filter]
  constructor
  · exact hm
  · rw [hM]
    have : 2 * m - m = m := by ring
    rwa [this]

/-- 上界推论：r_ord ≤ |S| 的具体数值情形（|S|=3）。 -/
theorem rOrd_le_three (M : ℤ) (S : Finset ℤ) (hS : S.card = 3) : rOrd M S ≤ 3 := by
  rw [← hS]
  exact rOrd_le_card M S

end CQM.GoldbachBookkeeping
