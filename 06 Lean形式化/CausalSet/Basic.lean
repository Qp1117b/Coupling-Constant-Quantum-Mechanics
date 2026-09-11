import Mathlib.Data.Set.Basic
import Mathlib.Data.Set.Finite.Basic
import Mathlib.Data.Set.Countable

/-!
# 因果集 (Causal Set)

CQM 的本体论基础：因果集是偏序的再生产事件集合，满足局部有限性。

## 公理
1. `≺` 是严格偏序（反自反、传递）
2. 局部有限性：任意两点之间的 Alexandrov 区间是有限集
3. 再生产算符 `μ̂` 满足 `μ̂² = μ̂`（幂等性）

## 参考文献
- Bombelli, Lee, Meyer, Sorkin (1987). "Space-time as a causal set."
- ruster (2026). CNT 完整研究. Zenodo. DOI: 10.5281/zenodo.20804380.
-/

open Set

/-- 因果集：偏序的再生产事件集合，满足局部有限性。
    `α` 是事件类型，`≺` 表示因果前导关系。 -/
class CausalSet (α : Type*) where
  /-- 因果前导关系：`x ≺ y` 表示 x 在因果上先于 y -/
  prec : α → α → Prop
  /-- 反自反性：没有任何事件在因果上先于自身 -/
  irrefl : ∀ x, ¬ prec x x
  /-- 传递性：因果前导关系是传递的 -/
  trans : ∀ {x y z}, prec x y → prec y z → prec x z
  /-- 局部有限性：任意两点之间的 Alexandrov 区间是有限集 -/
  locallyFinite : ∀ x y, Set.Finite {z | prec x z ∧ prec z y}

namespace CausalSet

variable {α : Type*} [CausalSet α]

/-- 因果前导的符号缩写 -/
scoped infix:50 " ≺ " => CausalSet.prec

/-- 非对称性：如果 x ≺ y，则 ¬ y ≺ x -/
theorem asymm {x y : α} (h : x ≺ y) : ¬ y ≺ x := by
  intro h'
  have h_trans := CausalSet.trans h h'
  exact CausalSet.irrefl x h_trans

/-- Alexandrov 区间：x 和 y 之间所有事件的集合 -/
def interval (x y : α) : Set α := {z | x ≺ z ∧ z ≺ y}

/-- Alexandrov 区间是有限集 -/
theorem interval_finite (x y : α) : Set.Finite (interval x y) :=
  CausalSet.locallyFinite x y

/-- 因果未来：x 的因果未来是 {y | x ≺ y} -/
def causalFuture (x : α) : Set α := {y | x ≺ y}

/-- 因果过去：x 的因果过去是 {y | y ≺ x} -/
def causalPast (x : α) : Set α := {y | y ≺ x}

/-- 因果无关：x 和 y 因果无关，记作 x ‖ y -/
def spacelike (x y : α) : Prop := ¬ (x ≺ y) ∧ ¬ (y ≺ x) ∧ x ≠ y

/-- 如果 x ≺ y，则 x ≠ y -/
theorem ne_of_prec {x y : α} (h : x ≺ y) : x ≠ y := by
  intro h_eq
  rw [h_eq] at h
  exact CausalSet.irrefl y h

/-- 因果集是可数的（Sprinkling 可数性）。
    在 CQM 中，有限体积内的因果集事件是可数的。 -/
class CountableCausalSet (α : Type*) extends CausalSet α where
  countable_eventSet : Set.Countable (Set.univ : Set α)

end CausalSet