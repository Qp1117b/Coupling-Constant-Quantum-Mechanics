import SuperconductivityChain.Basic
import Mathlib.Data.Fintype.Card
import Mathlib.Algebra.Order.BigOperators.Group.Finset

/-!
# 阶段 2：时间与差异（环 5–7）

形式化全对历史分量 `H_ij = τ_i - τ_j` 的反对称与上闭链、历史冻结判据、
平均固有时与方差非负。差异生产率的驱动方程不写，登记 `临-1`。

缺口：`M5`、`审-1`、`临-1`、`G19`、`临-24`、`临-25`。
-/

namespace CQM.SuperconductivityChain

open scoped BigOperators

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- 环 6：节点固有时差，`H_ij = τ_i − τ_j`。 -/
def Hpair (τ : V → ℝ) (i j : V) : ℝ := τ i - τ j

/-- 自差为零。 -/
theorem Hpair_self (τ : V → ℝ) (i : V) : Hpair τ i i = 0 := by
  unfold Hpair
  ring

/-- 反对称：`H_ij = −H_ji`。 -/
theorem Hpair_antisymm (τ : V → ℝ) (i j : V) : Hpair τ i j = - Hpair τ j i := by
  unfold Hpair
  ring

/-- 上闭链：`H_ij + H_jk = H_ik`。 -/
theorem Hpair_add (τ : V → ℝ) (i j k : V) :
    Hpair τ i j + Hpair τ j k = Hpair τ i k := by
  unfold Hpair
  ring

/-- 环 7：差异生产率 `Ḣ_ij = v_i − v_j`。 -/
def historyRate (v : V → ℝ) (i j : V) : ℝ := v i - v j

/-- 差异生产率反对称。 -/
theorem historyRate_antisymm (v : V → ℝ) (i j : V) :
    historyRate v i j = - historyRate v j i := by
  unfold historyRate
  ring

/-- 环 20：`Ḣ_ij=0` 等价于两端速度相等。 -/
theorem historyRate_eq_zero_iff (v : V → ℝ) (i j : V) :
    historyRate v i j = 0 ↔ v i = v j := by
  unfold historyRate
  constructor <;> intro h <;> linarith

/-- 环 6：历史冻结条件，所有节点对的固有时差为零。 -/
def HistoryFreeze (τ : V → ℝ) : Prop := ∀ i j, Hpair τ i j = 0

/-- 历史冻结等价于所有节点固有时相等；不涉及起点或积分是否可实现。 -/
theorem historyFreeze_iff (τ : V → ℝ) :
    HistoryFreeze τ ↔ ∀ i j, τ i = τ j := by
  constructor
  · intro h i j
    exact sub_eq_zero.mp (h i j)
  · intro h
    unfold HistoryFreeze Hpair
    intro i j
    rw [h i j, sub_self]

/-- 环 6：平均固有时。 -/
noncomputable def meanProperTime (τ : V → ℝ) : ℝ :=
  (∑ i, τ i) / (Fintype.card V : ℝ)

/-- 环 6：固有时速方差的节点平均形式。 -/
noncomputable def properTimeVariance (τ : V → ℝ) : ℝ :=
  (∑ i, (τ i - meanProperTime τ) ^ 2) / (Fintype.card V : ℝ)

/-- 方差非负；非空节点集是必要前提。 -/
theorem properTimeVariance_nonneg (τ : V → ℝ) (h : 0 < Fintype.card V) :
    0 ≤ properTimeVariance τ := by
  unfold properTimeVariance
  have hden : (0 : ℝ) < (Fintype.card V : ℝ) := by exact_mod_cast h
  exact div_nonneg (Finset.sum_nonneg (fun i _ => sq_nonneg _)) hden.le

end CQM.SuperconductivityChain
