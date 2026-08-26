import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.NumberTheory.Harmonic.EulerMascheroni
import Mathlib.Tactic

/-!
# BCS 标准 T_c 公式 (Transition Temperature)

本模块提供 BCS 弱耦合标准公式（精确常数 `bcsExactConstant = 2e^γ/π`），
供 `Reduction.lean` 等 BCS 退化证明使用。

CQM 专属的 $T_c$ 严格推导见 `TransitionTemperatureCQM.lean`（arctanh 闭式，G22 闭合）。

## 核心公式（自然单位 k_B = ℏ = 1）
k_B T_c = (2e^γ/π) · ℏ ω_D · exp(−1/(N(0)·V₀))

其中 γ 为欧拉-马歇罗尼常数（`eulerMascheroniConstant`），系数 2e^γ/π ≈ 1.1339。
Lean 内一律用精确常数 `bcsExactConstant`，数值近似仅在文档字符串中标注、不作为定理结论。

## 定理
- 临界温度严格为正
- 临界温度随截断频率单调不减

## 参考文献
- Bardeen, Cooper, Schrieffer (1957). Theory of Superconductivity.
- ruster (2026). CQM_超导核心理论. CQMFormal/08 超导/.
-/

namespace CQM

/-! ## BCS 弱耦合精确常数 -/

/-- BCS 弱耦合临界温度的精确系数：2e^γ/π ≈ 1.1339，其中 γ 为欧拉-马歇罗尼
    常数（≈ 0.5772）。文献公式常以三位近似 1.13 代替；本模块一律使用精确常数，
    数值近似仅在文档字符串中标注、不作为定理结论。 -/
noncomputable def bcsExactConstant : ℝ :=
  2 * Real.exp Real.eulerMascheroniConstant / Real.pi

/-- BCS 精确常数严格为正。 -/
theorem bcsExactConstant_pos : 0 < bcsExactConstant := by
  unfold bcsExactConstant
  exact div_pos (mul_pos (by norm_num) (Real.exp_pos _)) Real.pi_pos

/-! ## 临界温度公式 -/

/-- BCS 弱耦合极限下的临界温度（CQM 截断替换）：
    k_B T_c = (2e^γ/π) · ħω_causal · exp(−1/(N(0)·V₀))。
    自然单位 k_B = ℏ = 1；系数为精确值 `bcsExactConstant`（文献常写 1.13）。 -/
noncomputable def criticalTemperature (wCausal densityOfStates coupling : ℝ) : ℝ :=
  bcsExactConstant * wCausal * Real.exp (-1 / (densityOfStates * coupling))

/-- 临界温度严格为正（截断频率为正时；态密度与耦合仅影响指数因子，exp 恒正）。 -/
theorem criticalTemperature_pos (wCausal densityOfStates coupling : ℝ)
    (hw : wCausal > 0) :
    criticalTemperature wCausal densityOfStates coupling > 0 := by
  unfold criticalTemperature
  have h1 : bcsExactConstant * wCausal > 0 := mul_pos bcsExactConstant_pos hw
  exact mul_pos h1 (Real.exp_pos _)

/-- 临界温度随因果截断频率单调不减：因果截断越高（有效质量越大），
    T_c 越高。这与"强引力增强有效质量 → 不降 T_c"的命题相容。 -/
theorem criticalTemperature_monotone_in_cutoff (w₁ w₂ d c : ℝ) (hmono : w₁ ≤ w₂) :
    criticalTemperature w₁ d c ≤ criticalTemperature w₂ d c := by
  unfold criticalTemperature
  have hE : Real.exp (-1 / (d * c)) ≥ 0 := le_of_lt (Real.exp_pos _)
  have hc : (0 : ℝ) ≤ bcsExactConstant := le_of_lt bcsExactConstant_pos
  have hmul : bcsExactConstant * w₁ ≤ bcsExactConstant * w₂ := mul_le_mul_of_nonneg_left hmono hc
  exact mul_le_mul_of_nonneg_right hmul hE


end CQM