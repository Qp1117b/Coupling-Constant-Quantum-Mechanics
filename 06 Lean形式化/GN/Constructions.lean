import GN.Basic
import GN.SimplexSpectrum
import GN.AdeleJacobian
import SpectralGeometry.Basic
import PhysicalConstants.Basic

/-!
# §8–§11 启发式构造的代数层 (Constructions)

公理化证明稿第三部分（启发式构造与开放问题）中**可代数化**的部分：

- 构造 8.1 / 命题 8.1：κ 的分解 `κ = (N_faces + ☯)/N_cycle = 31/30 + ☯/30`
- 构造 11.1：`G_N` 乘积公式各因子的正性与形式记录
- 构造 9.1 / 10.1：以显式**条件/构造性假设**出现，不冒充定理

对应文档：§8、§11；§9/§10 仅作接口占位。

## 诚实边界

- κ 的**数值定义** `spectralCorrection = (31 + ☯)/30` 位于
  `SpectralGeometry.Basic`；本文件将其与 §2 组合量
  `N_faces = 31`、`N_cycle = Tr(M) = 30` 连接，使
  「构造 8.1」成为可复核的定理，而非字面量巧合。
- 为何 `+☯` 在分子、为何取该函数形式：开放问题 8.1，
  仍为缺口。
- `𝔠₁ = 1/4 + γ₁²` 的 n=1 精确等同（构造 9.1）：超出
  Sierra-CQM 渐近定理范围，此处仅记录构造性假设。
- `G_N` 乘积结构的变分原理（开放问题 11.1）：未解决。

## 参考文献

- 证明稿：`04 前沿研究/CQM_前沿研究_GN第一性推导_公理化证明稿.md`
- SpectralGeometry.Basic：`spectralCorrection`、`firstCoupling`
- PhysicalConstants.Basic：`GN_spectral_formula`
-/

open Real

namespace CQM
namespace GN

/-! ### §8 构造 8.1：κ 的组合-谱构造 -/

/-- [CONSTRUCTION 8.1] κ 的组合-谱构造（与数值定义一致）：

    `κ = (N_faces + ☯) / N_cycle`

    其中 `N_faces = 31`（§2 推论 2.1）、`N_cycle = 30`
    （`SpectralGeometry.adeleCycle`，亦 = Tr(M)）。 -/
theorem spectralCorrection_combinatorial :
    spectralCorrection
      = (simplexNonemptyFaces + spectralQuantum) / (adeleCycle : ℝ) := by
  unfold spectralCorrection adeleCycle
  rw [simplexNonemptyFaces_eq_31]
  norm_num

/-- κ 的分母取曲率算符的迹：`N_cycle = Tr(M) = 30`。 -/
theorem spectralCorrection_trace_denominator :
    spectralCorrection
      = (simplexNonemptyFaces + spectralQuantum) / (edgeFaceMatrix.trace : ℝ) := by
  rw [spectralCorrection_combinatorial]
  have hz : (adeleCycle : ℕ) = Int.toNat edgeFaceMatrix.trace := by
    have h1 : (adeleCycle : ℕ) = 30 := adeleCycle_eq_30
    have h2 : Int.toNat edgeFaceMatrix.trace = 30 := kappa_denominator_trace
    omega
  have hcast :
      ((adeleCycle : ℕ) : ℝ) = ((edgeFaceMatrix.trace : ℤ) : ℝ) := by
    have h1 : (adeleCycle : ℕ) = 30 := adeleCycle_eq_30
    have h2 : (edgeFaceMatrix.trace : ℤ) = 30 := edgeFaceMatrix_trace_eq_30
    rw [h1, h2]
    norm_num
  rw [hcast]

/-! [PROPOSITION 8.1] κ 的主项 + 修正项分解 -/

/-- [PROPOSITION 8.1] κ 可精确分解：

    `κ = 31/30 + ☯/30`

    即主项 `N_faces / N_cycle` 加修正项 `☯ / N_cycle`
    （离散→连续过渡修正）。 -/
theorem spectralCorrection_eq_main_add_correction :
    spectralCorrection
      = (31 : ℝ) / 30 + spectralQuantum / 30 := by
  unfold spectralCorrection
  ring

/-- 构造 8.1 分解的组合形式：主项 = `N_faces / N_cycle`。 -/
theorem spectralCorrection_main_is_face_ratio :
    (31 : ℝ) / 30
      = (simplexNonemptyFaces : ℝ) / (adeleCycle : ℝ) := by
  rw [simplexNonemptyFaces_eq_31, adeleCycle_eq_30]
  norm_num

/-- 构造 8.1 分解的组合形式：修正项 = `☯ / N_cycle`。 -/
theorem spectralCorrection_term_is_qi_over_cycle :
    spectralQuantum / 30 = spectralQuantum / (adeleCycle : ℝ) := by
  rw [adeleCycle_eq_30]
  norm_num

/-- 命题 8.1 的组合标记版本：

    `κ = N_faces/N_cycle + ☯/N_cycle`。 -/
theorem spectralCorrection_combinatorial_decomposition :
    spectralCorrection
      = (simplexNonemptyFaces : ℝ) / (adeleCycle : ℝ)
        + spectralQuantum / (adeleCycle : ℝ) := by
  rw [spectralCorrection_eq_main_add_correction,
    spectralCorrection_main_is_face_ratio,
    spectralCorrection_term_is_qi_over_cycle]

/-- κ 的主项严格大于 1（`31/30 > 1`），故 `κ > 1` 有组合来源。 -/
theorem spectralCorrection_main_gt_one : (31 : ℝ) / 30 > 1 := by
  norm_num

/-- κ 修正项严格为正（`☯ > 0`）。 -/
theorem spectralCorrection_qi_term_pos : spectralQuantum / 30 > 0 :=
  div_pos spectralQuantum_pos (by norm_num)

/-! ### §9 构造 9.1：𝔠₁ 精确等同（构造性假设） -/

/-- [CONSTRUCTION 9.1 — 构造性假设，非定理] 第一耦级精确等于
    第一黎曼零点对应的谱值：

    `firstCoupling = 1/4 + riemannZero1²`

    Sierra-CQM 定理（定理 5.1）只给出 n ≥ 1 的渐近
    `𝔠_n = 1/4 + γ_n² + O(γ_n²/n)`，n = 1 时相对误差为 O(1)。
    精确等同**超出定理范围**（开放问题 9.1）。

    本假设以 `Prop` 形式记录，供后续研究引用；当前状态：
    数值验证 `|firstCoupling_sierraCQM − firstCoupling| < 1e-8`
    （见 `SpectralGeometry.Basic`），非严格证明。 -/
noncomputable def firstCouplingExact : Prop :=
  firstCoupling = 1 / 4 + riemannZero1 ^ 2

/-- 构造 9.1 的数值旁证（非证明）：Sierra 公式与 `firstCoupling`
    字面量偏差 < 10⁻⁸。 -/
theorem firstCouplingExact_numerical_support :
    |(1 / 4 + riemannZero1 ^ 2) - firstCoupling| < 1e-8 :=
  firstCoupling_sierraCQM_deviation

/-! ### §11 构造 11.1：G_N 乘积结构（形式记录与正性） -/

/-- [CONSTRUCTION 11.1] `G_N` 谱公式的无量纲核（不含 `I`、`λ_c`、`m_p`）：

    `F = ☯² · 𝔠₁ · exp(−2/☯) · (1 + κ☯)`

    与 `SpectralGeometry.GNFactor_at_C` 同一表达式。 -/
noncomputable def gnProductCore : ℝ :=
  spectralQuantum ^ 2 * firstCoupling
    * Real.exp (-2 / spectralQuantum)
    * (1 + spectralCorrection * spectralQuantum)

/-- 乘积核与既有 `GNFactor_at_C` 一致。 -/
theorem gnProductCore_eq_GNFactor_at_C : gnProductCore = GNFactor_at_C := by
  unfold gnProductCore GNFactor_at_C
  ring

/-- [构造 11.1 正性] 乘积核严格为正（各因子 > 0）。 -/
theorem gnProductCore_pos : gnProductCore > 0 := by
  rw [gnProductCore_eq_GNFactor_at_C]
  exact GNFactor_at_C_pos

/-- 构造 10.1 条件下的层级因子等同（组合到 `GN.AdeleJacobian`）。 -/
theorem gn_hierarchyFactor_eq_adeleJacobian
    (hself : detDinf * detDprod = 1) (hpos : 0 < detDprod)
    (hqi : adeleSpectralLog_eq_inv_qi) :
    Real.exp (-2 / spectralQuantum) = adeleJacobian :=
  (adeleJacobian_eq_hierarchyFactor hself hpos hqi).symm

/-- 乘积核的对数形式（供开放问题 11.1 的变分结构研究）：

    `ln F = 2 ln ☯ + ln 𝔠₁ − 2/☯ + ln(1 + κ☯)` -/
theorem gnProductCore_log (hpos : spectralQuantum > 0) :
    Real.log gnProductCore
      = 2 * Real.log spectralQuantum + Real.log firstCoupling
        - 2 / spectralQuantum
        + Real.log (1 + spectralCorrection * spectralQuantum) := by
  have hC : spectralQuantum ≠ 0 := ne_of_gt hpos
  have hC2 : spectralQuantum ^ 2 ≠ 0 := pow_ne_zero 2 hC
  have hfc : firstCoupling ≠ 0 := ne_of_gt firstCoupling_pos
  have hexp : Real.exp (-2 / spectralQuantum) ≠ 0 := Real.exp_ne_zero _
  have hcorr : 1 + spectralCorrection * spectralQuantum ≠ 0 := by
    have h1 : spectralCorrection > 0 := by linarith [spectralCorrection_gt_one]
    have h2 : spectralCorrection * spectralQuantum > 0 := mul_pos h1 hpos
    linarith
  unfold gnProductCore
  rw [Real.log_mul (mul_ne_zero (mul_ne_zero hC2 hfc) hexp) hcorr,
    Real.log_mul (mul_ne_zero hC2 hfc) hexp,
    Real.log_mul hC2 hfc,
    Real.log_pow, Real.log_exp]
  ring

/-- [构造 11.1 — 公式记录] `G_N` 谱公式（与
    `PhysicalConstants.GN_spectral_formula` 同一乘积结构）：

    `G_N = I · λ_c · ☯² · 𝔠₁ · exp(−2/☯) · (1+κ☯) / m_p²`

    各因子已严格为正（`dynkinIndex_pos`、`mathieuCritical_pos`、
    `gnProductCore_pos`、`protonMass_pos`）；乘积**作为公式**
    的第一性推导（变分原理）是开放问题 11.1。 -/
theorem gn_factors_all_pos :
    dynkinIndex > 0 ∧ mathieuCritical > 0 ∧ gnProductCore > 0
      ∧ protonMass > 0 := by
  refine ⟨dynkinIndex_pos, mathieuCritical_pos, gnProductCore_pos,
    protonMass_pos⟩

end GN
end CQM
