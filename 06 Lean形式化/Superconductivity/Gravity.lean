import Mathlib.Data.Real.Basic
import Mathlib.Analysis.Real.Pi.Bounds
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic
import PhysicalConstants.Basic
import Decoherence.Basic

/-!
# CQM 超导：引力因果限制场与退相干核 (Gravitational Causal-Limiting Field)

本模块形式化《CQM 超导核心理论》的引力因果限制场（原"涌现论"第三层已并入该统一文档 §3 引力因果限制）。引力场 = 因果限制退相干场。

## 核心定义（自然单位 ℏ = c = 1）
- **因果分辨率** τ_res = ℏ/(M c²) = 1/M
- **因果截断频率** ω_causal = 2π M c²/ℏ = 2π M（满足 ω_causal = 2π/τ_res）
- **阶梯截断核** K_causal = Θ(ω_causal − ω_k)
- **因果共振窗口** exp[−(Δτ − τ_res)²/(2σ²)]

## 定理
- 因果分辨率严格为正，且随质量增大而缩小（宏观确定性的根源）
- 因果截断频率严格为正，且随有效质量单调不减
- 强引力（增强有效质量）**不降低**因果截断频率 ⇒ 引力本身不破坏超导
- 共振窗口严格为正（退相干筛选权重）

## 参考文献
- ruster (2026). CQM 超导核心理论. CQMFormal/08 超导/.
- ruster (2026). CQM 退相干 引力因果场. CQMFormal/03 引力与退相干/.
-/

namespace CQM

/-! ## 因果分辨率 -/

/-- 命题 3.2：因果分辨率 τ_res(M) = ℏ/(M c²)。
    自然单位（ℏ = c = 1）下 τ_res(M) = 1/M。 -/
noncomputable def causalResolutionTime (M : ℝ) : ℝ := 1 / M

/-- 因果分辨率严格为正（质量严格为正时）。 -/
theorem causalResolutionTime_pos {M : ℝ} (hM : M > 0) : causalResolutionTime M > 0 := by
  unfold causalResolutionTime
  exact div_pos (by norm_num) hM

/-- 质子的因果分辨率：τ_res ~ 10⁻²⁴ s 量级。自然单位 1/m_p。 -/
noncomputable def protonCausalResolution : ℝ := causalResolutionTime protonMass

/-- 质子因果分辨率严格为正。 -/
theorem protonCausalResolution_pos : protonCausalResolution > 0 := by
  unfold protonCausalResolution
  exact causalResolutionTime_pos protonMass_pos

/-- 宏观探测器（M_eff ≫ m_p）的因果分辨率远小于质子：
    物体之所以"确定"量子态，是因为其有效质量大 → τ_res 极小 → 因果分辨率极高。 -/
noncomputable def detectorCausalResolution (detectorMass : ℝ) : ℝ := causalResolutionTime detectorMass

/-! ## 因果截断频率 -/

/-- 命题 3.2 推论 + 第七层：因果截断频率 ω_causal = 2π M_eff c²/ℏ。
    自然单位：ω_causal = 2π M_eff。 -/
noncomputable def causalCutoffFrequency (M : ℝ) : ℝ := 2 * Real.pi * M

/-- 因果截断频率严格为正。 -/
theorem causalCutoffFrequency_pos {M : ℝ} (hM : M > 0) : causalCutoffFrequency M > 0 := by
  unfold causalCutoffFrequency
  exact mul_pos (mul_pos (by norm_num) (lt_trans (by norm_num : (0 : ℝ) < 3) Real.pi_gt_three)) hM

/-- 因果截断频率与因果分辨率的一致性：ω_causal = 2π/τ_res。
    即配对因果时差 Δτ = 2π/ω_q 达到晶格因果分辨率 τ_res 的等价条件。 -/
theorem causalCutoff_eq_two_pi_over_resolution {M : ℝ} (hM : M ≠ 0) :
    causalCutoffFrequency M = 2 * Real.pi / causalResolutionTime M := by
  unfold causalCutoffFrequency causalResolutionTime
  field_simp [hM]

/-- 因果截断频率随有效质量单调不减（同位素效应对照：ω_causal ∝ M_eff，
    与 Debye 频率 ω_D ∝ M^(−1/2) 的标度相反）。 -/
theorem causalCutoff_frequency_monotone_in_mass {M₁ M₂ : ℝ} (hm : M₁ ≤ M₂) :
    causalCutoffFrequency M₁ ≤ causalCutoffFrequency M₂ := by
  unfold causalCutoffFrequency
  have h2pi : (0 : ℝ) ≤ 2 * Real.pi := le_of_lt (mul_pos (by norm_num) (lt_trans (by norm_num : (0 : ℝ) < 3) Real.pi_gt_three))
  exact mul_le_mul_of_nonneg_left hm h2pi

/-- 强引力（第 5.1 命题的形式化）：引力通过减速固有时等效增强有效质量
    M → M·g（g ≥ 1），从而**不降低**因果截断频率。
    引力是退相干筛选与锁定机制，强引力只把因果截断推向更深耦合区域，
    因而不破坏超导（这一命题的其余部分在 Mechanism 模块展开）。 -/
theorem strong_gravity_does_not_lower_causal_cutoff {M g : ℝ} (hM : M > 0) (hg : g ≥ 1) :
    causalCutoffFrequency (M * g) ≥ causalCutoffFrequency M := by
  have hMle : M ≤ M * g := by
    calc
      M = 1 * M := by ring
      _ ≤ g * M := mul_le_mul_of_nonneg_right hg (le_of_lt hM)
      _ = M * g := by ring
  have h2pi : (0 : ℝ) ≤ 2 * Real.pi := le_of_lt (mul_pos (by norm_num) (lt_trans (by norm_num : (0 : ℝ) < 3) Real.pi_gt_three))
  unfold causalCutoffFrequency
  exact mul_le_mul_of_nonneg_left hMle h2pi

/-! ## 因果截断核 -/

/-- 阶梯因果截断核：K_causal = Θ(ω_causal − ω_k)。
    只有配对频率不超过因果截断频率的模式（Δτ ≥ τ_res）被锁定。 -/
noncomputable def causalCutoffKernel (w wCausal : ℝ) : ℝ :=
  if w ≤ wCausal then 1 else 0

/-- 截断核在可分辨窗口内为 1：配对因果时差达到因果分辨率的模式被锁定。 -/
theorem causalCutoffKernel_locks_when_resolvable {w wCausal : ℝ} (hw : w ≤ wCausal) :
    causalCutoffKernel w wCausal = 1 := by
  unfold causalCutoffKernel
  rw [if_pos hw]

/-- 截断核在窗口外为 0：配对太快（Δτ ≪ τ_res），因果模糊，被截断。 -/
theorem causalCutoffKernel_cuts_when_unresolvable {w wCausal : ℝ} (hw : wCausal < w) :
    causalCutoffKernel w wCausal = 0 := by
  unfold causalCutoffKernel
  rw [if_neg (not_le.mpr hw)]

/-- 截断核非负（作为退相干筛选权重，它是 0 或 1）。 -/
theorem causalCutoffKernel_nonneg (w wCausal : ℝ) : causalCutoffKernel w wCausal ≥ 0 := by
  by_cases h : w ≤ wCausal
  · rw [causalCutoffKernel_locks_when_resolvable h]
    norm_num
  · rw [causalCutoffKernel_cuts_when_unresolvable (lt_of_not_ge h)]

/-- 因果共振窗口（高斯）：exp[−(Δτ − τ_res)²/(2σ²)]。
    配对因果时差越接近晶格因果分辨率，因果耦合越"共振"，越容易被锁定。 -/
noncomputable def causalResonanceWindow (deltaTau tauRes sigma : ℝ) : ℝ :=
  Real.exp (- (deltaTau - tauRes) ^ 2 / (2 * sigma ^ 2))

/-- 因果共振窗口严格为正：退相干核作为筛选权重恒为正。 -/
theorem causalResonanceWindow_pos (deltaTau tauRes sigma : ℝ) :
    causalResonanceWindow deltaTau tauRes sigma > 0 := by
  unfold causalResonanceWindow
  exact Real.exp_pos _

/-- 因果共振窗口在共振点达到其最大值 1（Δτ = τ_res 时为精确共振锁定）。 -/
theorem causalResonanceWindow_peak_at_resonance (tauRes sigma : ℝ) :
    causalResonanceWindow tauRes tauRes sigma = 1 := by
  unfold causalResonanceWindow
  ring_nf
  rw [Real.exp_zero]

end CQM