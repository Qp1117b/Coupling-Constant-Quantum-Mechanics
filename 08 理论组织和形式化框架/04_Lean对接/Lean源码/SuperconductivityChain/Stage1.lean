import SuperconductivityChain.Basic
import Mathlib.Data.Real.Sqrt
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Algebra.Order.BigOperators.Group.Finset

/-!
# 阶段 1：入口与几何（环 1–4）

形式化定义层：二次型基态方差、声子零点幅度、Bose 占据数与亏角涨落方差、
固有时流速的几何定义、Regge 刚度的对称/零行和/半正定条件。
正则对易子本身没有 Hilbert 空间载体；声子场的完整算符展开、热截断位置不证。

缺口：`W-3`、`临-18`、`审-10`、`M7`。
-/

namespace CQM.SuperconductivityChain

open scoped BigOperators

/-- 环 1：二次型基态方差 `⟨X²⟩₀ = ℏ/(2mω)`；只记定义层，不从对易子推量子化。 -/
noncomputable def groundVariance (hbar m omega : ℝ) : ℝ :=
  hbar / (2 * m * omega)

/-- 正参数下基态方差为正。 -/
theorem groundVariance_pos {hbar m omega : ℝ}
    (hh : 0 < hbar) (hm : 0 < m) (ho : 0 < omega) :
    0 < groundVariance hbar m omega := by
  unfold groundVariance
  positivity

/-- 环 2：声子零点幅度 `sqrt(ℏ/(2ρ_mω))`，对应 (2.1) 的系数。 -/
noncomputable def phononAmplitude (hbar rho omega : ℝ) : ℝ :=
  Real.sqrt (hbar / (2 * rho * omega))

/-- 声子幅度的平方等于根号内表达式。 -/
theorem phononAmplitude_sq {hbar rho omega : ℝ}
    (h : 0 ≤ hbar / (2 * rho * omega)) :
    phononAmplitude hbar rho omega ^ 2 = hbar / (2 * rho * omega) := by
  unfold phononAmplitude
  exact Real.sq_sqrt h

/-- 正参数下声子零点幅度为正。 -/
theorem phononAmplitude_pos {hbar rho omega : ℝ}
    (hh : 0 < hbar) (hr : 0 < rho) (ho : 0 < omega) :
    0 < phononAmplitude hbar rho omega := by
  unfold phononAmplitude
  apply Real.sqrt_pos.2
  positivity

/-- 环 4：Bose 占据数 `n_B = 1/(e^{ℏω/k_BT}−1)`。 -/
noncomputable def boseOccupancy (hbar omega kB T : ℝ) : ℝ :=
  1 / (Real.exp (hbar * omega / (kB * T)) - 1)

/-- 正参数下 Bose 占据数非负。 -/
theorem boseOccupancy_nonneg {hbar omega kB T : ℝ}
    (hh : 0 < hbar) (ho : 0 < omega) (hk : 0 < kB) (ht : 0 < T) :
    0 ≤ boseOccupancy hbar omega kB T := by
  unfold boseOccupancy
  have hx : 0 < hbar * omega / (kB * T) := by positivity
  have hden : 0 < Real.exp (hbar * omega / (kB * T)) - 1 :=
    sub_pos.mpr (Real.one_lt_exp_iff.mpr hx)
  exact le_of_lt (div_pos zero_lt_one hden)

/-- 环 4：单条边的亏角方差 `Σ_k G_ek² ℏ/(2ρ_mω_k) [1+2n_B(ω_k)]`。 -/
noncomputable def deficitVariance {ι : Type*} [Fintype ι]
    (G : ι → ℝ) (omega : ι → ℝ) (hbar rho kB T : ℝ) : ℝ :=
  ∑ k, G k ^ 2 * (hbar / (2 * rho * omega k)) *
    (1 + 2 * boseOccupancy hbar (omega k) kB T)

/-- 正参数下亏角方差非负；不证明 `G` 的显式与截断位置。 -/
theorem deficitVariance_nonneg {ι : Type*} [Fintype ι]
    (G : ι → ℝ) (omega : ι → ℝ) (hbar rho kB T : ℝ)
    (hh : 0 < hbar) (hr : 0 < rho) (ho : ∀ k, 0 < omega k)
    (hk : 0 < kB) (ht : 0 < T) :
    0 ≤ deficitVariance G omega hbar rho kB T := by
  unfold deficitVariance
  apply Finset.sum_nonneg
  intro k _
  have hbase : 0 ≤ hbar / (2 * rho * omega k) := by
    have hok : 0 < omega k := ho k
    have hden : 0 < 2 * rho * omega k := by positivity
    exact div_nonneg hh.le hden.le
  have hocc : 0 ≤ boseOccupancy hbar (omega k) kB T :=
    boseOccupancy_nonneg hh (ho k) hk ht
  have hfactor : 0 ≤ 1 + 2 * boseOccupancy hbar (omega k) kB T := by
    nlinarith
  exact mul_nonneg (mul_nonneg (sq_nonneg (G k)) hbase) hfactor

/-- 环 3：Regge 亏角 `ε = 2π − Σθ`；`Σθ` 是围绕一条边的三角形内角和。 -/
noncomputable def deficitAngle (angleSum : ℝ) : ℝ :=
  2 * Real.pi - angleSum

/-- 角度和非负时，亏角不超过 `2π`。 -/
theorem deficitAngle_le_two_pi {s : ℝ} (hs : 0 ≤ s) :
    deficitAngle s ≤ 2 * Real.pi := by
  unfold deficitAngle
  linarith

/-- 内角和不超过 `2π` 时，亏角非负。 -/
theorem deficitAngle_nonneg {s : ℝ} (hs : s ≤ 2 * Real.pi) :
    0 ≤ deficitAngle s := by
  unfold deficitAngle
  linarith

/-- 环 5 的几何接口：由亏角定义的固有时流速。 -/
noncomputable def deficitSpeed (ε : ℝ) : ℝ :=
  Real.sqrt (1 - ε / (2 * Real.pi))

/-- `deficitSpeed` 的平方恒等式；定义域由 `h` 给出。 -/
theorem deficitSpeed_sq {ε : ℝ} (h : 0 ≤ 1 - ε / (2 * Real.pi)) :
    deficitSpeed ε ^ 2 = 1 - ε / (2 * Real.pi) := by
  unfold deficitSpeed
  exact Real.sq_sqrt h

/-- 在物理分支 `0 ≤ 1 - ε/(2π)` 上，`deficitSpeed` 非负。 -/
theorem deficitSpeed_nonneg {ε : ℝ} (_h : 0 ≤ 1 - ε / (2 * Real.pi)) :
    0 ≤ deficitSpeed ε := by
  unfold deficitSpeed
  exact Real.sqrt_nonneg _

/-- 环 3 的 Regge 刚度矩阵：对称、零行和、半正定。
这些是 (3.2) 的四性质中的三条；单零模未作为字段，属缺口 `W-3`。 -/
structure ReggeStiffness (V : Type*) [Fintype V] where
  L : V → V → ℝ
  symmetric : ∀ i j, L i j = L j i
  row_sum_zero : ∀ i, (∑ j, L i j) = 0
  positive_semidefinite : ∀ x : V → ℝ, 0 ≤ ∑ i, ∑ j, x i * L i j * x j

end CQM.SuperconductivityChain
