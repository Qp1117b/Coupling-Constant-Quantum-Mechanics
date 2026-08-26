import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Block
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic
import CartanAlgebra.Basic
import Superconductivity.Reduction
/-- 相位再生产锁定因子 e^{−Γ|τ|}：稳定性维持。
     恒正，用于序参量各通道的衰减调制。 -/
noncomputable def phaseLockingFactor (GammaPhase dotTau : ℝ) : ℝ :=
  Real.exp (-GammaPhase * |dotTau|)

theorem phaseLockingFactor_pos (GammaPhase dotTau : ℝ) : phaseLockingFactor GammaPhase dotTau > 0 := by
  unfold phaseLockingFactor
  exact Real.exp_pos _

/-!
# CQM 超导：嘉当张量超导方程 (Cartan Superconductivity)

本模块形式化**张量超导方程**：将 CQM 张量涌现结构
（因果结构 𝒞 理想化为 SU(5) 嘉当矩阵 A₄ 的本征子空间）应用到超导序参量。
对应理论文档《CQM_超导核心理论》§9 库珀对跃迁。依据《CQM_数学_嘉当结构》（07 推导与数学）：
- **A₄ 同时是离散哈密顿量**（§2.1 嘉当方程，A₄ 作为离散 Laplacian）与
  **能动张量的谱结构**（§3.1，⟨T_μν⟩ 由谱结构 E_n 确定）；
- 本征值 λ_k = 2 − 2cos(kπ/5)（§2.2），谱间隙为最小本征值
  λ₁ = (3−√5)/2 ≈ 0.382；
- 序参量在 A₄ 本征基上展开为 4 个本征通道（k = 1..4），
  每个通道 = 谱权重 × 因果潜能系数 × 再生产锁定因子 e^{−Γτ}。

**理想化与退化约定**（本模块全部定理均在此约定下成立）：
1. 因果投影 𝒫̂_𝒞 理想化为"投影到 A₄ 全部 4 个本征通道"（因果结构
   𝒞 = A₄ 本征子空间，无遗漏通道；A₄ 本征向量的显式构造
   属 CartanAlgebra 待办，本模块以本征值谱 [cartanEigenvalue] 为输入）；
2. 基础自由度 𝒟 在 A₄ 本征基的系数取谱系数 [spectralCoeff]
   （正数 = 原料层可实际化），因果潜能 𝒫 的权重取谱权重
   [cartanEigenvalue]（A₄ 本征值，均正）；
3. 可观测序参量 = 张量迹（对全部 4 通道求和，类比 §6.8 的 Tr_𝒞）；
4. **谱间隙退化**：BCS 晶格扇区对应 A₄ 的谱间隙通道（k = 1），
   谱间隙同时缩放能隙 Δ 与临界温度 T_c（[bcsGapInGapChannel]、
   [bcsTcInGapChannel]），普适能隙比不变（[gapChannel_gapRatio_invariant]）。

## 定理一览
- [spectralGap_pos] / [spectralGap_lt_one] / [spectralGap_lt_all]：
  谱间隙为正、小于 1、严格小于其余全部本征值
- [stressEnergyTrace_eq_eight]：能动张量迹 = A₄ 谱和 = 8
- [cartanHamiltonian_trace_eq_stressEnergyTrace]：A₄ 作为离散哈密顿量的
  迹 = 能动张量迹（同一谱的两种角色）
- [cartanHamiltonianEnergy_pos]：A₄ 谱能量评估在正序参量上为正
- [superconductingOrderComponent_pos] /
  [superconductingOrderTensor_pos] /
  [superconductingOrderTensor_cartanWeights_pos]：张量超导序参量
  逐通道与全体严格为正（超导态在 A₄ 谱上确实涌现）
- [bcsGapInGapChannel_pos] / [gapChannel_gapRatio_invariant]：
  谱间隙通道退化到 BCS 能隙方程解，能隙比不受谱间隙缩放影响
- [cartanInvTrace_eq_four]：Tr(A₄⁻¹) = 4（勘误：07 嘉当结构文档
  §4.2 记 Tr(A⁻¹) = 2，与直接计算不符；1/Tr(A⁻¹) = 1/4 恰为
  谱间隙 E₀ = c²/4 所需的 1/4）
- [cartanA4Stack_*]：A₄ 直接拼接（大量金属氢）——块对角拼接保持
  2-自环、块内仍为 A₄、跨质子零耦合、迹 = 8·n、det = 5ⁿ
  （禁闭几何尺度按质子数线性累加，不因拼接稀释）

## 参考文献
- ruster (2026). CQM_数学_嘉当结构（07 推导与数学）§2.1–§4.2.
- ruster (2026). CQM_超导核心理论（08 超导）.
-/

namespace CQM

open scoped BigOperators

/-! ## A₄ 作为离散哈密顿量 + 能动张量谱 -/

/-- A₄ 嘉当矩阵的 ℝ 提升：SU(5) 的离散哈密顿量（07 嘉当结构 §2.1，
    A₄ 作为离散 Laplacian；连续极限 A₄/a² → −∂_u² + ∂_u = Ĥ_∞/c²）。 -/
noncomputable def cartanHamiltonian : Matrix (Fin 4) (Fin 4) ℝ :=
  fun i j => (cartanA4 i j : ℝ)

/-- A₄ 谱间隙 = 最小本征值 λ₁ = (3−√5)/2 ≈ 0.382（07 嘉当结构 §2.2，
    紫外起始扇区；对应谱间隙 E₀ = c²/4 的离散侧）。 -/
noncomputable def spectralGap : ℝ := eigenvalue1

/-- A₄ 本征值谱作为序参量展开的权重函数：k = 1..4 对应
    eigenvalue1..4（λ_k = 2 − 2cos(kπ/5)）。本模块以本征值谱为输入
    （A₄ 本征向量的显式构造属 CartanAlgebra 待办，理想化约定 1）。 -/
noncomputable def cartanEigenvalue (k : Fin 4) : ℝ :=
  if k = 0 then eigenvalue1
  else if k = 1 then eigenvalue2
  else if k = 2 then eigenvalue3
  else eigenvalue4

/-- 能动张量迹（理想化）：⟨T⟩ 的迹 = A₄ 谱和 = λ₁+λ₂+λ₃+λ₄
    （07 嘉当结构 §3.1：谱结构 E_n 确定系统能级；A₄ 同一谱同时充当
    哈密顿量与能动张量）。 -/
noncomputable def stressEnergyTrace : ℝ :=
  eigenvalue1 + eigenvalue2 + eigenvalue3 + eigenvalue4

/-- A₄ 谱能量评估（哈密顿量对序参量向量的作用，本征基理想化）：
    能量 = Σ_k λ_k·v_k。 -/
noncomputable def cartanHamiltonianEnergy (v : Fin 4 → ℝ) : ℝ :=
  ∑ k : Fin 4, cartanEigenvalue k * v k

/-! ## 谱结构定理 -/

/-- 谱间隙严格为正（A₄ 正定 → 离散哈密顿量谱非负、无零模）。 -/
theorem spectralGap_pos : 0 < spectralGap := by
  unfold spectralGap
  exact eigenvalue1_pos

/-- 谱间隙小于 1（离散 Laplacian 的最低谱在 (0,1) 内，紫外截断稳定）。 -/
theorem spectralGap_lt_one : spectralGap < 1 := by
  unfold spectralGap
  unfold eigenvalue1 sqrt5
  have h : 1 < Real.sqrt 5 := sqrt5_gt_1
  nlinarith

/-- 谱间隙严格小于其余全部本征值（唯一最小，谱间隙是真实的隙）。 -/
theorem spectralGap_lt_all : spectralGap < eigenvalue2 ∧ spectralGap < eigenvalue3 ∧
    spectralGap < eigenvalue4 := by
  have h12 := eigenvalues_ordered.1
  have h23 := eigenvalues_ordered.2.1
  have h34 := eigenvalues_ordered.2.2
  constructor
  · exact h12
  · constructor
    · exact lt_trans h12 h23
    · exact lt_trans (lt_trans h12 h23) h34

/-- 全部 4 个本征通道的谱权重严格为正。 -/
theorem cartanEigenvalue_pos (k : Fin 4) : 0 < cartanEigenvalue k := by
  unfold cartanEigenvalue
  fin_cases k
  · simpa using eigenvalue1_pos
  · simpa using eigenvalue2_pos
  · simpa using eigenvalue3_pos
  · simpa using eigenvalue4_pos

/-- A₄ 谱和（全部本征通道）= 8 = Tr(A₄)。 -/
theorem cartanEigenvalues_sum_eq_eight : (∑ k : Fin 4, cartanEigenvalue k) = 8 := by
  unfold cartanEigenvalue
  have hsum : (∑ k : Fin 4,
      if k = 0 then eigenvalue1 else if k = 1 then eigenvalue2
      else if k = 2 then eigenvalue3 else eigenvalue4) =
      eigenvalue1 + eigenvalue2 + eigenvalue3 + eigenvalue4 := by
    simp [Fin.sum_univ_succ]
    ring
  rw [hsum]
  simpa [add_assoc] using eigenvalue_sum_eq_trace

/-- 能动张量迹 = 8（= Tr(A₄)）。 -/
theorem stressEnergyTrace_eq_eight : stressEnergyTrace = 8 := by
  unfold stressEnergyTrace
  exact eigenvalue_sum_eq_trace

/-- A₄ 双重角色的一致性：离散哈密顿量的迹 = 能动张量的迹
    （同一个谱 {λ₁..λ₄} 同时充当哈密顿量与能动张量）。 -/
theorem cartanHamiltonian_trace_eq_stressEnergyTrace :
    (∑ i : Fin 4, cartanHamiltonian i i) = stressEnergyTrace := by
  unfold cartanHamiltonian
  have h : (∑ i : Fin 4, (cartanA4 i i : ℝ)) = 8 := by
    have hsum : (∑ i : Fin 4, (cartanA4 i i : ℝ)) = ((∑ i : Fin 4, cartanA4 i i) : ℝ) := by
      simp
    rw [hsum]
    exact_mod_cast cartanA4_trace
  rw [h, stressEnergyTrace_eq_eight]

/-- 哈密顿量对角元全为 2（离散 Laplacian 的势能形式）。 -/
theorem cartanHamiltonian_diag_two (i : Fin 4) : cartanHamiltonian i i = 2 := by
  unfold cartanHamiltonian
  rw [cartanA4_diag i]
  norm_num

/-- A₄ 谱能量评估的正性：序参量向量各分量严格为正时，
    哈密顿量谱能量严格为正（禁闭哈密顿量不产生负能量模）。 -/
theorem cartanHamiltonianEnergy_pos {v : Fin 4 → ℝ} (hv : ∀ k : Fin 4, 0 < v k) :
    cartanHamiltonianEnergy v > 0 := by
  unfold cartanHamiltonianEnergy
  apply Finset.sum_pos
  · intro k hk
    exact mul_pos (cartanEigenvalue_pos k) (hv k)
  · exact ⟨0, Finset.mem_univ 0⟩

/-! ## 张量超导序参量（§6.8 公式在 A₄ 谱上的展开） -/

/-- 单个本征通道的序参量分量（§6.8 的 𝒯_emergent 在通道 k 的分量）：
    谱权重（因果潜能 𝒫）× 谱系数（基础自由度 𝒟 的本征基系数）×
    再生产锁定因子 e^{−Γτ}。 -/
noncomputable def superconductingOrderComponent
    (weights : Fin 4 → ℝ) (spectralCoeff GammaPhase dotTau : ℝ) (k : Fin 4) : ℝ :=
  weights k * spectralCoeff * phaseLockingFactor GammaPhase dotTau

/-- 张量超导序参量（§6.8 的 Tr_𝒞：对因果相容子空间 𝒞 求张量迹，
    本模块理想化为对全部 4 个 A₄ 本征通道求和）。 -/
noncomputable def superconductingOrderTensor
    (weights : Fin 4 → ℝ) (spectralCoeff GammaPhase dotTau : ℝ) : ℝ :=
  ∑ k : Fin 4, superconductingOrderComponent weights spectralCoeff GammaPhase dotTau k

/-- 逐通道正性：谱权重与谱系数为正时，每个本征通道的序参量分量
    严格为正（锁定因子 e^{−Γτ} 恒正，无需求 Γ ≥ 0）。 -/
theorem superconductingOrderComponent_pos {weights : Fin 4 → ℝ}
    {spectralCoeff GammaPhase dotTau : ℝ} {k : Fin 4}
    (hw : 0 < weights k) (hs : 0 < spectralCoeff) :
    superconductingOrderComponent weights spectralCoeff GammaPhase dotTau k > 0 := by
  unfold superconductingOrderComponent
  exact mul_pos (mul_pos hw hs) (phaseLockingFactor_pos GammaPhase dotTau)

/-- 张量序参量正性：全部 4 个通道的权重与谱系数为正时，
    超导序参量张量的迹严格为正（超导态确实涌现）。 -/
theorem superconductingOrderTensor_pos {weights : Fin 4 → ℝ}
    {spectralCoeff GammaPhase dotTau : ℝ}
    (hw : ∀ k : Fin 4, 0 < weights k) (hs : 0 < spectralCoeff) :
    superconductingOrderTensor weights spectralCoeff GammaPhase dotTau > 0 := by
  unfold superconductingOrderTensor
  apply Finset.sum_pos
  · intro k hk
    exact superconductingOrderComponent_pos (hw k) hs
  · exact ⟨0, Finset.mem_univ 0⟩

/-- A₄ 谱权重版本：因果潜能取 A₄ 本征值谱 [cartanEigenvalue] 时，
    张量超导序参量严格为正（A₄ 正定谱支撑超导序参量）。 -/
theorem superconductingOrderTensor_cartanWeights_pos
    {spectralCoeff GammaPhase dotTau : ℝ} (hs : 0 < spectralCoeff) :
    superconductingOrderTensor cartanEigenvalue spectralCoeff GammaPhase dotTau > 0 := by
  apply superconductingOrderTensor_pos
  · exact cartanEigenvalue_pos
  · exact hs

/-! ## 谱间隙退化：CQM 张量序参量 → BCS 晶格扇区 -/

/-- 能隙方程闭式解为正：Δ(λ) = ω_D/sinh(1/λ) > 0。 -/
lemma bcsGapFromGapEquation_pos {w lam : ℝ} (hw : 0 < w) (hl : 0 < lam) :
    0 < bcsGapFromGapEquation w lam := by
  unfold bcsGapFromGapEquation
  have hx : 0 < 1 / lam := div_pos (by norm_num) hl
  have h1 : 1 < Real.exp (1 / lam) := (Real.one_lt_exp_iff).2 hx
  have h2 : Real.exp (-(1 / lam)) < 1 := by
    rw [Real.exp_lt_one_iff]
    exact neg_lt_zero.mpr hx
  have hsub : 0 < Real.exp (1 / lam) - Real.exp (-(1 / lam)) :=
    sub_pos.mpr (lt_trans h2 h1)
  rw [Real.sinh_eq]
  have hD : 0 < (Real.exp (1 / lam) - Real.exp (-(1 / lam))) / 2 :=
    div_pos hsub (by norm_num)
  exact div_pos hw hD

/-- 谱间隙通道的序参量（理想化退化）：BCS 能隙方程解 Δ(λ) 乘以
    A₄ 谱间隙权重 λ₁（"序参量被谱间隙投影缩放"的退化解读）。 -/
noncomputable def bcsGapInGapChannel (wDebye lam : ℝ) : ℝ :=
  spectralGap * bcsGapFromGapEquation wDebye lam

/-- 谱间隙通道的临界温度（理想化退化）：BCS 临界温度 T_c(λ) 乘以
    同一谱间隙权重（谱间隙同时缩放 Δ 与 T_c）。 -/
noncomputable def bcsTcInGapChannel (wDebye lam : ℝ) : ℝ :=
  spectralGap * bcsCriticalTemperature wDebye lam

/-- 谱间隙通道序参量严格为正。 -/
theorem bcsGapInGapChannel_pos {wDebye lam : ℝ} (hw : 0 < wDebye) (hl : 0 < lam) :
    0 < bcsGapInGapChannel wDebye lam := by
  unfold bcsGapInGapChannel
  exact mul_pos spectralGap_pos (bcsGapFromGapEquation_pos hw hl)

/-- 谱间隙缩放不变性：谱间隙同时缩放 Δ 与 T_c 时，能隙比
    2Δ/(k_B T_c) 不变（谱间隙通道的普适能隙比 = BCS 普适能隙比，
    与 §6.8 的"唯一性（筛选）与确定性（锁定）同时达成"相容）。 -/
theorem gapChannel_gapRatio_invariant {wDebye lam : ℝ} (hw : wDebye > 0) (hl : lam > 0) :
    2 * bcsGapInGapChannel wDebye lam / bcsTcInGapChannel wDebye lam =
      2 * bcsGapFromGapEquation wDebye lam / bcsCriticalTemperature wDebye lam := by
  unfold bcsGapInGapChannel bcsTcInGapChannel
  have hsg : spectralGap ≠ 0 := ne_of_gt spectralGap_pos
  have htc : bcsCriticalTemperature wDebye lam ≠ 0 := ne_of_gt (bcsCriticalTemperature_pos hw)
  have hgap : bcsGapFromGapEquation wDebye lam ≠ 0 :=
    ne_of_gt (bcsGapFromGapEquation_pos hw hl)
  field_simp [hsg, htc, hgap]

/-- [定理] 谱间隙通道临界温度的精确闭式（将文档断言提升为可证定理）：
      T_c^gap = λ₁·(2e^γ/π)·ω_D·exp(−1/λ)。
    纯代数恒等，由 `bcsCriticalTemperature` 与 `bcsExactConstant = 2e^γ/π` 展开得到。 -/
theorem bcsTcInGapChannel_closedForm (wDebye lam : ℝ) :
    bcsTcInGapChannel wDebye lam =
      spectralGap * (2 * Real.exp Real.eulerMascheroniConstant / Real.pi) * wDebye *
        Real.exp (-1 / lam) := by
  unfold bcsTcInGapChannel bcsCriticalTemperature bcsExactConstant
  ring

/-- [定理] 谱间隙通道能隙的精确闭式（将文档断言提升为可证定理）：
      Δ^gap = λ₁·ω_D / sinh(1/λ)。
    纯代数恒等，由 `bcsGapInGapChannel` 与 `bcsGapFromGapEquation` 展开得到。 -/
theorem bcsGapInGapChannel_closedForm (wDebye lam : ℝ) :
    bcsGapInGapChannel wDebye lam = spectralGap * wDebye / Real.sinh (1 / lam) := by
  unfold bcsGapInGapChannel bcsGapFromGapEquation
  rw [← mul_div_assoc]

/-! ## 逆嘉当矩阵的迹（勘误） -/

/-- 逆嘉当矩阵 A₄⁻¹ 的迹（对角元 (4+6+6+4)/5 = 20/5 = 4）。 -/
noncomputable def cartanInvTrace : ℚ :=
  ∑ i : Fin 4, cartanA4_inv_entry i.val i.val

/-- [勘误] Tr(A₄⁻¹) = 4。
    07 嘉当结构文档 §4.2 记 Tr(A⁻¹) = 2，与直接计算不符：
    A₄⁻¹ 对角元为 (1/5)·[4, 6, 6, 4]，迹 = 20/5 = 4。
    修正后 1/Tr(A⁻¹) = 1/4 恰为谱间隙 E₀ = c²/4 中的 1/4，
    该文档谱间隙公式自洽（原 2 反而给出 1/2，不自洽）。 -/
theorem cartanInvTrace_eq_four : cartanInvTrace = 4 := by
  unfold cartanInvTrace
  simp [cartanA4_inv_entry, Fin.sum_univ_succ]
  norm_num

/-! ## A₄ 直接拼接（大量金属氢：每个质子一块正四单纯型） -/

/-- A₄ 直接拼接：n 个质子（有限本体）的晶格嘉当矩阵 = n 份 A₄ 的块对角拼接。
    索引 = (块内顶点, 质子号) = Fin 4 × Fin n；块间零耦合——
    不同质子的禁闭几何正交（关系网络由声子介导另建，见 08 超导 金属氢 §3.6）。
    这正对应"大量金属氢 = 单个质子有限本体的 A₄ 直接拼接"。 -/
noncomputable def cartanA4Stack (n : ℕ) : Matrix (Fin 4 × Fin n) (Fin 4 × Fin n) ℤ :=
  Matrix.blockDiagonal fun _ : Fin n => cartanA4

/-- 拼接 = 跨质子零耦合：不同质子（k ≠ k'）的顶点之间无矩阵元，
    A₄ 直接拼接不引入跨本体耦合（网络关系由声子通道另建）。 -/
theorem cartanA4Stack_zero_of_proton_ne {n : ℕ} {i j : Fin 4} {k k' : Fin n}
    (h : k ≠ k') : cartanA4Stack n ⟨i, k⟩ ⟨j, k'⟩ = 0 := by
  unfold cartanA4Stack
  rw [Matrix.blockDiagonal_apply']
  simp [h]

/-- 同一质子块内子矩阵仍为 A₄：拼接不改变单个质子的禁闭几何。 -/
theorem cartanA4Stack_block_eq {n : ℕ} (k : Fin n) :
    (fun i j => cartanA4Stack n ⟨i, k⟩ ⟨j, k⟩) = cartanA4 := by
  funext i j
  unfold cartanA4Stack
  rw [Matrix.blockDiagonal_apply']
  simp

/-- 每个质子位保持 2-自环（正四单纯型顶点自环不因拼接改变）。 -/
theorem cartanA4Stack_diag {n : ℕ} (i : Fin 4) (k : Fin n) :
    cartanA4Stack n ⟨i, k⟩ ⟨i, k⟩ = 2 := by
  unfold cartanA4Stack
  rw [Matrix.blockDiagonal_apply']
  simp [cartanA4_diag]

/-- 迹的拼接：Tr(⨁ₖ A₄) = 8·n——A₄ 谱和（能动张量迹）按质子数线性累加，
    禁闭几何的能量尺度随网络规模（金属氢密度）线性增长。 -/
theorem cartanA4Stack_trace_eq {n : ℕ} : Matrix.trace (cartanA4Stack n) = 8 * n := by
  unfold cartanA4Stack
  rw [Matrix.trace_blockDiagonal]
  simp [Matrix.trace, cartanA4_trace, Finset.sum_const, mul_comm]

/-- A₄ 的 Matrix.det（统一行列式入口）= 5（与显式公式 det4 一致）。 -/
theorem cartanA4_det_matrix : (cartanA4 : Matrix (Fin 4) (Fin 4) ℤ).det = 5 := by
  native_decide

/-- 行列式的拼接：det(⨁ₖ A₄) = 5ⁿ——每块仍为 det(A₄) = 5
    （正四单纯型"禁闭体积"尺度不因拼接稀释；n = 质子数）。 -/
theorem cartanA4Stack_det_eq {n : ℕ} : (cartanA4Stack n).det = 5 ^ n := by
  unfold cartanA4Stack
  rw [Matrix.det_blockDiagonal]
  simp [cartanA4_det_matrix]

end CQM
