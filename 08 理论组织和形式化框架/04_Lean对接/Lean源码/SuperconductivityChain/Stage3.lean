import SuperconductivityChain.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset

/-!
# 阶段 3：耦合与配对强度（环 8–10）

形式化 `C_ij = f(ε_i−ε_j)` 的反对称性（给定 `f` 奇）、弱耦合配对势的负性、
以及 `λ = N(0) Σ|V|` 的非负性。分布式不对易的代数地位与 `A12` 不证。

缺口：`E4`、`A12`、`M5`、`审-2`、`审-3`、`链外-A`、`M2`–`M4`。
-/

namespace CQM.SuperconductivityChain

open scoped BigOperators

variable {V : Type*} [Fintype V]

/-- 环 8：由亏角差给出的关联矩阵，`C_ij = f(ε_i−ε_j)`。 -/
def couplingMatrix (f : ℝ → ℝ) (ε : V → ℝ) (i j : V) : ℝ :=
  f (ε i - ε j)

/-- 若 `f` 为奇函数，则 `C` 反对称。 -/
theorem couplingMatrix_antisymm (f : ℝ → ℝ) (ε : V → ℝ)
    (hf : ∀ x, f (-x) = - f x) (i j : V) :
    couplingMatrix f ε i j = - couplingMatrix f ε j i := by
  unfold couplingMatrix
  rw [show ε j - ε i = -(ε i - ε j) by ring]
  rw [hf]
  ring

/-- 环 9：关联方差 `2κ_f²σ²(1−ρ)`；`ρ → 1` 时归零。 -/
noncomputable def couplingVariance (κ σ ρ : ℝ) : ℝ :=
  2 * κ ^ 2 * σ ^ 2 * (1 - ρ)

/-- `ρ ≤ 1` 时方差非负；这不证明 `σ²` 的零点/热方差归属（`审-3`）。 -/
theorem couplingVariance_nonneg {κ σ ρ : ℝ} (hρ : ρ ≤ 1) :
    0 ≤ couplingVariance κ σ ρ := by
  unfold couplingVariance
  have hκ : 0 ≤ κ ^ 2 := sq_nonneg κ
  have hσ : 0 ≤ σ ^ 2 := sq_nonneg σ
  have h1 : 0 ≤ 1 - ρ := sub_nonneg.mpr hρ
  have h2 : 0 ≤ 2 * κ ^ 2 := mul_nonneg (by norm_num) hκ
  exact mul_nonneg (mul_nonneg h2 hσ) h1

/-- 环 10：弱耦合配对势 `V = −g²/κ`。 -/
noncomputable def pairPotential (g κ : ℝ) : ℝ :=
  - (g ^ 2 / κ)

/-- 非零耦合、正刚度时配对势为负。 -/
theorem pairPotential_neg {g κ : ℝ} (hg : g ≠ 0) (hκ : 0 < κ) :
    pairPotential g κ < 0 := by
  unfold pairPotential
  have hnum : 0 < g ^ 2 := sq_pos_of_ne_zero hg
  have hfrac : 0 < g ^ 2 / κ := div_pos hnum hκ
  linarith

/-- 环 10：`λ = N(0) Σ_j |V_j|` 的节点求和形式。 -/
noncomputable def lambdaCoupling (N0 : ℝ) (Vj : V → ℝ) : ℝ :=
  N0 * ∑ j, |Vj j|

/-- `N(0) ≥ 0` 时 `λ ≥ 0`；绝对系数仍由 `审-2` 卡住。 -/
theorem lambdaCoupling_nonneg (N0 : ℝ) (Vj : V → ℝ) (hN : 0 ≤ N0) :
    0 ≤ lambdaCoupling N0 Vj := by
  unfold lambdaCoupling
  exact mul_nonneg hN (Finset.sum_nonneg (fun j _ => abs_nonneg _))

end CQM.SuperconductivityChain
