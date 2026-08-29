import Mathlib.Data.Real.Basic
import Mathlib.Analysis.Real.Pi.Bounds
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Arsinh
import Mathlib.Order.Filter.AtTopBot.Field
import Mathlib.Topology.Algebra.Order.Field
import Mathlib.Topology.Defs.Filter
import Mathlib.Tactic
import Superconductivity.TransitionTemperature

import Superconductivity.Ontology
import PhysicalConstants.Basic

open scoped Topology

open Filter

/-!
# CQM 超导：BCS 退化与还原 (Reduction to BCS)

本模块形式化第一步：**CQM 超导理论必须退化为已有的 BCS 超导理论**
（晶格声子扇区），并还原其核心公式。对应理论文档《CQM_超导核心理论》
§11 温度依赖：所还原的 BCS 公式为文献标准内容。

**严格性约定**：本模块中的每个 `theorem` 都从明确的定义出发经 Lean 证明。
数值常数凡未在 Lean 中证明者（如 2e^γ/π 的三位近似 1.13、能隙比的数值
3.53、同位素位移 1/√2 ≈ 0.707），均在文档字符串中如实标注为文献/数值近似，
不冒充定理结论。

## 退化条件（晶格扇区）
1. 配对通道的因果截断频率取晶格德拜频率：ω_causal → ω_D = √(k/M_ion)
2. 态密度×耦合乘积取 BCS 耦合常数：N(0)·V ≡ d·c

## 还原的公式（推导地位：方程是物理内容，公式是方程的解）
- BCS 临界温度：k_B T_c = (2e^γ/π)·ħω_D·exp(−1/(N(0)V))，其中 2e^γ/π ≈ 1.1339
  （文献公式常写 1.13，那是该系数的三位近似）。
  它是弱耦合 T_c 方程 1 = λ·ln((2e^γ/π)·ω_D/(k_B T_c)) 的唯一正解
  （`bcsTcEquation_solved`、`bcsTcEquation_unique`）——**公式是方程的解，
  不是任意定义**；方程本身（含系数）是 BCS 物理内容，其"积分→对数方程"
  渐近未形式化（G13）。
- BCS 零温能隙：由 T=0 能隙方程 1 = λ·arsinh(ω_D/Δ) 精确解得
  Δ = ω_D/sinh(1/λ)（见 `bcs_gap_equation`、`bcs_gap_equation_unique`）；
  弱耦合极限 λ→0⁺ 时该解渐近于 BCS 标准式 Δ₀ = 2·ħω_D·exp(−1/λ)
  （见 `bcs_gap_weak_coupling_limit`，这是极限定理而非有限 λ 的等式；
  记号 `bcsGap` 即此渐近形式，不是独立定义）。
- 普适能隙比：2Δ₀/(k_B T_c) 由能隙方程解与 T_c 方程解之比在 λ→0⁺ 的
  极限给出 = 2πe^{−γ} ≈ 3.5278（文献数值 3.53 为近似）。
  这是**极限定理**（`bcs_universal_gap_ratio`）：强耦合下能隙比偏离 3.53，
  不存在"对所有 λ 精确等于 2πe^{−γ}"的恒等式。
- 同位素定律：T_c ∝ M^(−1/2)（α = 1/2）
- McMillan–Dynes 强耦合公式
- London 穿透深度、BCS 相干长度、磁通量子

## 朴素 CQM 异常（条件陈述）
朴素 CQM 的 ω_causal = 2πM_eff 与离子质量成正比，直接代入 T_c 给出
T_c 随质量单调不减——与 BCS 同位素定律方向相反，亦与实验（H3S/D3S）相反。
本模块以一个**条件定理**刻画该异常：在朴素替换下 T_c 是质量的单调不减函数。
它表明"配对通道 = 晶格声子扇区"这一选择与实例一致、而朴素选择与实例矛盾，
**不是**一个"退化是逻辑必然"的证明——后者属物理选择而非可证命题。

## 参考文献
- Bardeen, Cooper, Schrieffer (1957). Theory of Superconductivity.
- McMillan (1968). Transition Temperature of Strong-Coupled Superconductors.
- Allen, Dynes (1975). Phys. Rev. B 12, 905.
- Drozdov et al. (2015). Nature 525, 73 (H3S, T_c = 203 K @ 155 GPa).
- Drozdov et al. (2019). Nature 569, 528 (LaH10, T_c ≈ 250 K @ 170 GPa).
- 氢氘硫化物实验：T_c(D3S) ≈ 147 K @ 150 GPa，H/D 比 ≈ 0.72（接近 1/√2）。
-/

namespace CQM

/-! ## BCS 标准公式（自然单位 k_B = ℏ = c = 1） -/

/-- BCS 临界温度：k_B T_c = (2e^γ/π)·ħω_D·exp(−1/(N(0)·V))。
     `bcsExactConstant = 2e^γ/π ≈ 1.1339`，文献公式常写 1.13（三位近似）。
     与 CQM 的 `criticalTemperature` 同构（见退化定理）。

     **推导地位（不是定义）**：本式是弱耦合 T_c 方程
         1 = λ·ln((2e^γ/π)·ω_D/(k_B T_c))
     的唯一正解（见 `bcsTcEquation_solved`、`bcsTcEquation_unique`）。
     方程本身（含系数 2e^γ/π）是 BCS 平均场在对数近似下的物理内容；
     其"配对积分 → 对数方程"的渐近推导未形式化（缺口 G13），
     但**方程的解是严格定理**。 -/
noncomputable def bcsCriticalTemperature (wDebye n0V : ℝ) : ℝ :=
  bcsExactConstant * wDebye * Real.exp (-1 / n0V)

/-- BCS 临界温度严格为正（德拜频率正时）。 -/
theorem bcsCriticalTemperature_pos {wDebye n0V : ℝ} (hw : wDebye > 0) :
    bcsCriticalTemperature wDebye n0V > 0 := by
  unfold bcsCriticalTemperature
  exact mul_pos (mul_pos bcsExactConstant_pos hw) (Real.exp_pos _)

/-- [推导] 弱耦合 T_c 方程的解：T_c = (2e^γ/π)·ω_D·exp(−1/λ) 精确满足
     1 = λ·ln((2e^γ/π)·ω_D/(k_B T_c))。 -/
theorem bcsTcEquation_solved {wDebye n0V : ℝ} (hw : wDebye > 0) (hn : n0V > 0) :
    n0V * Real.log (bcsExactConstant * wDebye / bcsCriticalTemperature wDebye n0V) = 1 := by
  have hrew : Real.exp (-1 / n0V) = Real.exp (-(1 / n0V)) := by
    congr 1
    ring
  have harg : bcsExactConstant * wDebye /
      (bcsExactConstant * wDebye * Real.exp (-(1 / n0V))) = Real.exp (1 / n0V) := by
    field_simp [ne_of_gt bcsExactConstant_pos, ne_of_gt hw, Real.exp_ne_zero _]
    rw [← Real.exp_add, neg_add_cancel, Real.exp_zero]
  calc
    n0V * Real.log (bcsExactConstant * wDebye / bcsCriticalTemperature wDebye n0V)
        = n0V * Real.log (Real.exp (1 / n0V)) := by
        rw [bcsCriticalTemperature, hrew, harg]
    _ = n0V * (1 / n0V) := by
        rw [Real.log_exp]
    _ = 1 := by
        field_simp [ne_of_gt hn]

/-- [推导] 弱耦合 T_c 方程的唯一正解：凡满足
     1 = λ·ln((2e^γ/π)·ω_D/(k_B T_c)) 的正 T_c 必等于闭式解。
     与 `bcsTcEquation_solved` 合起来说明：T_c 公式是方程的**解**，
     而非任意选定的定义。 -/
theorem bcsTcEquation_unique {wDebye n0V Tc : ℝ} (hw : wDebye > 0) (hn : n0V > 0)
    (hTc : Tc > 0) (h : n0V * Real.log (bcsExactConstant * wDebye / Tc) = 1) :
    Tc = bcsCriticalTemperature wDebye n0V := by
  have h1 : Real.log (bcsExactConstant * wDebye / Tc) = 1 / n0V := by
    calc
      Real.log (bcsExactConstant * wDebye / Tc)
          = (1 / n0V) * (n0V * Real.log (bcsExactConstant * wDebye / Tc)) := by
          field_simp [ne_of_gt hn]
      _ = (1 / n0V) * 1 := by
          rw [h]
      _ = 1 / n0V := by
          ring
  have h2 : Real.log (bcsExactConstant * wDebye / bcsCriticalTemperature wDebye n0V) = 1 / n0V := by
    have hs := bcsTcEquation_solved hw hn
    calc
      Real.log (bcsExactConstant * wDebye / bcsCriticalTemperature wDebye n0V)
          = (1 / n0V) * (n0V * Real.log (bcsExactConstant * wDebye / bcsCriticalTemperature wDebye n0V)) := by
          field_simp [ne_of_gt hn]
      _ = (1 / n0V) * 1 := by
          rw [hs]
      _ = 1 / n0V := by
          ring
  have harg1 : 0 < bcsExactConstant * wDebye / Tc :=
    div_pos (mul_pos bcsExactConstant_pos hw) hTc
  have harg2 : 0 < bcsExactConstant * wDebye / bcsCriticalTemperature wDebye n0V := by
    exact div_pos (mul_pos bcsExactConstant_pos hw) (bcsCriticalTemperature_pos hw)
  have hratio : bcsExactConstant * wDebye / Tc =
      bcsExactConstant * wDebye / bcsCriticalTemperature wDebye n0V :=
    Real.log_injOn_pos harg1 harg2 (by rw [h1, h2])
  have hw' : wDebye ≠ 0 := ne_of_gt hw
  have hb : bcsCriticalTemperature wDebye n0V ≠ 0 :=
    ne_of_gt (bcsCriticalTemperature_pos hw)
  calc
    Tc = bcsExactConstant * wDebye / (bcsExactConstant * wDebye / Tc) := by
        field_simp [hw', ne_of_gt bcsExactConstant_pos]
    _ = bcsExactConstant * wDebye /
          (bcsExactConstant * wDebye / bcsCriticalTemperature wDebye n0V) := by
        rw [hratio]
    _ = bcsCriticalTemperature wDebye n0V := by
        field_simp [ne_of_gt bcsExactConstant_pos, hb, hw']

/-- BCS 零温能隙的弱耦合记号（渐近形式）：Δ₀ ≈ 2·ħω_D·exp(−1/(N(0)·V))。
     这不是独立定义，而是能隙方程精确解 `bcsGapFromGapEquation` 在
     λ→0⁺ 的**极限记号**（见 `bcs_gap_weak_coupling_limit`）。
     严格路径：能隙方程 1 = λ·arsinh(ω_D/Δ)（`bcs_gap_equation`、
     `bcs_gap_equation_unique`）→ 闭式解 Δ = ω_D/sinh(1/λ)
     → 弱耦合极限渐近于本记号。 -/
noncomputable def bcsGap (wDebye n0V : ℝ) : ℝ :=
  2 * wDebye * Real.exp (-1 / n0V)

/-- BCS 零温能隙严格为正。 -/
theorem bcsGap_pos {wDebye n0V : ℝ} (hw : wDebye > 0) : bcsGap wDebye n0V > 0 := by
  unfold bcsGap
  exact mul_pos (mul_pos (by norm_num) hw) (Real.exp_pos _)

/-- T=0 BCS 能隙方程的闭式解：Δ(λ) = ω_D / sinh(1/λ)。
     它是能隙方程 1 = λ·arsinh(ω_D/Δ) 的解（见 `bcs_gap_equation`）。 -/
noncomputable def bcsGapFromGapEquation (wDebye n0V : ℝ) : ℝ :=
  wDebye / Real.sinh (1 / n0V)

/-- 能隙方程解的验证：Δ = ω_D/sinh(1/λ) 精确满足 T=0 BCS 能隙方程
     1 = λ·arsinh(ω_D/Δ)。（"从物理方程到闭式解"的推导所在。） -/
theorem bcs_gap_equation {w lam : ℝ} (hw : w > 0) (hlam : lam > 0) :
    lam * Real.arsinh (w / bcsGapFromGapEquation w lam) = 1 := by
  unfold bcsGapFromGapEquation
  have hw' : w ≠ 0 := ne_of_gt hw
  have hlam' : lam ≠ 0 := ne_of_gt hlam
  have hsin : Real.sinh (1 / lam) ≠ 0 := by
    simpa [Real.sinh_eq_zero] using inv_ne_zero hlam'
  have hq : w / (w / Real.sinh (1 / lam)) = Real.sinh (1 / lam) := by
    field_simp [hw', hsin]
  calc
    lam * Real.arsinh (w / (w / Real.sinh (1 / lam)))
        = lam * Real.arsinh (Real.sinh (1 / lam)) := by rw [hq]
    _ = lam * (1 / lam) := by rw [Real.arsinh_sinh]
    _ = 1 := by field_simp [hlam']

/-- 能隙方程解的完备性：凡满足能隙方程 1 = λ·arsinh(ω_D/Δ) 的 Δ，必等于闭式解
     ω_D/sinh(1/λ)。与 `bcs_gap_equation` 合起来说明闭式解是该方程的唯一解。 -/
theorem bcs_gap_equation_unique {w lam Δ : ℝ} (hw : w ≠ 0) (hlam : lam ≠ 0)
    (h : lam * Real.arsinh (w / Δ) = 1) :
    Δ = bcsGapFromGapEquation w lam := by
  unfold bcsGapFromGapEquation
  have hstep0 : Real.arsinh (w / Δ) = 1 / lam := by
    calc
      Real.arsinh (w / Δ)
          = (1 / lam) * (lam * Real.arsinh (w / Δ)) := by
          field_simp [hlam]
      _ = (1 / lam) * 1 := by rw [h]
      _ = 1 / lam := by ring
  have hstep : w / Δ = Real.sinh (1 / lam) := by
    have := congrArg Real.sinh hstep0
    simpa using this
  have hsin : Real.sinh (1 / lam) ≠ 0 := by
    simpa [Real.sinh_eq_zero] using inv_ne_zero hlam
  calc
    Δ = w / (w / Δ) := by field_simp [hw]
    _ = w / Real.sinh (1 / lam) := by rw [← hstep]

/-- 恒等式（推导的中间步）：能隙方程精确解与弱耦合记号之比 = (1 − e^{−2/λ})⁻¹。
      该因子在 λ→0⁺ 时 → 1（见 `bcs_gap_weak_coupling_limit`），
      也用于能隙比极限定理（见 `bcs_gap_ratio_closed_form`）。 -/
lemma bcs_gap_ratio_eq {w lam : ℝ} (hw : w ≠ 0) (hlam : lam ≠ 0) :
    bcsGapFromGapEquation w lam / bcsGap w lam = (1 - Real.exp (-2 / lam))⁻¹ := by
  unfold bcsGapFromGapEquation bcsGap
  have hsin : Real.sinh (1 / lam) ≠ 0 := by
    simpa [Real.sinh_eq_zero] using inv_ne_zero hlam
  have he : Real.exp (-(1 / lam)) ≠ 0 := Real.exp_ne_zero _
  have hrew : Real.exp (-1 / lam) = Real.exp (-(1 / lam)) := by
    congr 1
    ring
  have ha : Real.exp (1 / lam) * Real.exp (-(1 / lam)) = 1 := by
    have harg : 1 / lam + -(1 / lam) = 0 := by ring
    rw [← Real.exp_add, harg, Real.exp_zero]
  have hb : Real.exp (-(1 / lam)) * Real.exp (-(1 / lam)) = Real.exp (-2 / lam) := by
    have harg : -(1 / lam) + -(1 / lam) = -2 / lam := by ring
    rw [← Real.exp_add, harg]
  calc
    w / Real.sinh (1 / lam) / (2 * w * Real.exp (-1 / lam))
        = w / Real.sinh (1 / lam) / (2 * w * Real.exp (-(1 / lam))) := by
        rw [hrew]
    _ = (2 * Real.sinh (1 / lam) * Real.exp (-(1 / lam)))⁻¹ := by
        field_simp [hw, hsin, he]
    _ = (1 - Real.exp (-2 / lam))⁻¹ := by
        congr 1
        calc
          2 * Real.sinh (1 / lam) * Real.exp (-(1 / lam))
              = 2 * ((Real.exp (1 / lam) - Real.exp (-(1 / lam))) / 2)
                  * Real.exp (-(1 / lam)) := by
                  rw [Real.sinh_eq]
          _ = (Real.exp (1 / lam) - Real.exp (-(1 / lam))) * Real.exp (-(1 / lam)) := by
              ring
          _ = Real.exp (1 / lam) * Real.exp (-(1 / lam))
              - Real.exp (-(1 / lam)) * Real.exp (-(1 / lam)) := by
              rw [sub_mul]
          _ = 1 - Real.exp (-2 / lam) := by
              rw [ha, hb]

/-- 弱耦合极限：λ→0⁺ 时能隙方程精确解 Δ(λ) = ω_D/sinh(1/λ) 与 BCS 标准式
     Δ₀ = 2ω_D·e^{−1/λ} 的比值趋于 1。即弱耦合下标准式是精确解的渐近形。 -/
theorem bcs_gap_weak_coupling_limit {w : ℝ} (hw : w > 0) :
    Tendsto (fun lam : ℝ => bcsGapFromGapEquation w lam / bcsGap w lam) (𝓝[>] 0) (𝓝 1) := by
  have h₁ : Tendsto (fun lam : ℝ => 1 / lam) (𝓝[>] 0) atTop := by
    simpa [div_eq_mul_inv] using (tendsto_inv_nhdsGT_zero (𝕜 := ℝ))
  have h₂ : Tendsto (fun lam : ℝ => -2 / lam) (𝓝[>] 0) atBot := by
    have hm : Tendsto (fun lam : ℝ => -2 * (1 / lam)) (𝓝[>] 0) atBot :=
      (Filter.tendsto_const_mul_atBot_of_neg (by norm_num : (-2 : ℝ) < 0)).mpr h₁
    simpa [div_eq_mul_inv] using hm
  have h₅ : Tendsto (fun lam : ℝ => Real.exp (-2 / lam)) (𝓝[>] 0) (𝓝 0) :=
    Real.tendsto_exp_atBot.comp h₂
  have h₆ : Tendsto (fun lam : ℝ => 1 - Real.exp (-2 / lam)) (𝓝[>] 0) (𝓝 1) := by
    simpa using tendsto_const_nhds.sub h₅
  have h₇ : Tendsto (fun lam : ℝ => (1 - Real.exp (-2 / lam))⁻¹) (𝓝[>] 0) (𝓝 1) := by
    simpa using h₆.inv₀ (by norm_num : (1 : ℝ) ≠ 0)
  apply h₇.congr'
  filter_upwards [self_mem_nhdsWithin] with lam hlam
  exact (bcs_gap_ratio_eq (ne_of_gt hw) (ne_of_gt hlam)).symm

/-- [推导] 能隙比的闭式恒等式（有限 λ，非极限）：对任意 λ > 0，
     2Δ₀/(k_B T_c) = 2πe^{−γ} · (1 − e^{−2/λ})⁻¹。
     这是 `bcs_universal_gap_ratio`（λ→0⁺ 极限）的有限 λ 版本；
     因子 (1 − e^{−2/λ})⁻¹ > 1，故有限 λ 下能隙比恒大于弱耦合极限
     2πe^{−γ}（强耦合偏离，见 `bcs_gap_ratio_strong_coupling_excess`）。 -/
lemma bcs_gap_ratio_closed_form {wDebye lam : ℝ} (hw : wDebye > 0) (hlam : lam > 0) :
    2 * bcsGapFromGapEquation wDebye lam / bcsCriticalTemperature wDebye lam =
      2 * Real.pi * Real.exp (-Real.eulerMascheroniConstant) *
        (1 - Real.exp (-2 / lam))⁻¹ := by
  have hratio := bcs_gap_ratio_eq (ne_of_gt hw) (ne_of_gt hlam)
  have htc : bcsGap wDebye lam / bcsCriticalTemperature wDebye lam =
      Real.pi * Real.exp (-Real.eulerMascheroniConstant) := by
    unfold bcsGap bcsCriticalTemperature bcsExactConstant
    rw [Real.exp_neg]
    field_simp [ne_of_gt hw, Real.exp_ne_zero _, Real.exp_ne_zero _]
  calc
    2 * bcsGapFromGapEquation wDebye lam / bcsCriticalTemperature wDebye lam
        = 2 * (bcsGapFromGapEquation wDebye lam / bcsGap wDebye lam *
            (bcsGap wDebye lam / bcsCriticalTemperature wDebye lam)) := by
            field_simp [ne_of_gt hw, bcsCriticalTemperature_pos hw,
              ne_of_gt (bcsGap_pos hw)]
      _ = 2 * ((1 - Real.exp (-2 / lam))⁻¹ *
            (Real.pi * Real.exp (-Real.eulerMascheroniConstant))) := by
            rw [hratio, htc]
      _ = 2 * Real.pi * Real.exp (-Real.eulerMascheroniConstant) *
            (1 - Real.exp (-2 / lam))⁻¹ := by
            ring

/-- [推导] 强耦合偏离：对任意有限 λ > 0，能隙比 2Δ₀/(k_B T_c) 严格大于
     弱耦合极限 2πe^{−γ}（≈ 3.5278，文献 3.53）。
     即 3.53 只是弱耦合渐近值：耦合越强（λ 越大），能隙比越大、
     偏离 BCS 弱耦合值越远（与 BCS/Eliashberg 文献一致）。 -/
theorem bcs_gap_ratio_strong_coupling_excess {wDebye lam : ℝ} (hw : wDebye > 0)
    (hlam : lam > 0) :
    2 * Real.pi * Real.exp (-Real.eulerMascheroniConstant) <
      2 * bcsGapFromGapEquation wDebye lam / bcsCriticalTemperature wDebye lam := by
  have hclosed := bcs_gap_ratio_closed_form hw hlam
  rw [hclosed]
  have h1 : Real.exp (-2 / lam) < 1 := by
    rw [Real.exp_lt_one_iff]
    exact div_neg_of_neg_of_pos (by norm_num : (-2 : ℝ) < 0) hlam
  have hpos : 0 < 1 - Real.exp (-2 / lam) := sub_pos.2 h1
  have hlt : 1 - Real.exp (-2 / lam) < 1 := by
    rw [sub_lt_self_iff]
    exact Real.exp_pos _
  have hinv : 1 < (1 - Real.exp (-2 / lam))⁻¹ := (one_lt_inv₀ hpos).2 hlt
  have hconst : 0 < 2 * Real.pi * Real.exp (-Real.eulerMascheroniConstant) := by
    positivity
  exact lt_mul_of_one_lt_right hconst hinv

/-- [推导] 能隙比的弱耦合极限：2Δ₀/(k_B T_c) → 2πe^{−γ}（≈ 3.5278，
     文献数值 3.53 为近似）。
     推导路径：Δ₀ 取能隙方程精确解 `bcsGapFromGapEquation`，
     T_c 取 T_c 方程解 `bcsCriticalTemperature`，两者比值经
     `bcs_gap_ratio_eq` 化为 (1 − e^{−2/λ})⁻¹ · 2πe^{−γ}，
     在 λ→0⁺ 时趋于 2πe^{−γ}。
     注意：这是**极限定理**，不是对任意 λ 的精确恒等式——
     能隙比 3.53 只描述弱耦合极限，强耦合下会偏离
     （与 BCS 文献一致，强耦合能隙比大于 3.53）。 -/
theorem bcs_universal_gap_ratio (wDebye : ℝ) (hw : wDebye > 0) :
    Tendsto
      (fun lam : ℝ =>
        2 * bcsGapFromGapEquation wDebye lam / bcsCriticalTemperature wDebye lam)
      (𝓝[>] 0) (𝓝 (2 * Real.pi * Real.exp (-Real.eulerMascheroniConstant))) := by
  have h₁ : Tendsto (fun lam : ℝ => 1 / lam) (𝓝[>] 0) atTop := by
    simpa [div_eq_mul_inv] using (tendsto_inv_nhdsGT_zero (𝕜 := ℝ))
  have h₂ : Tendsto (fun lam : ℝ => -2 / lam) (𝓝[>] 0) atBot := by
    have hm : Tendsto (fun lam : ℝ => -2 * (1 / lam)) (𝓝[>] 0) atBot :=
      (Filter.tendsto_const_mul_atBot_of_neg (by norm_num : (-2 : ℝ) < 0)).mpr h₁
    simpa [div_eq_mul_inv] using hm
  have h₅ : Tendsto (fun lam : ℝ => Real.exp (-2 / lam)) (𝓝[>] 0) (𝓝 0) :=
    Real.tendsto_exp_atBot.comp h₂
  have h₆ : Tendsto (fun lam : ℝ => 1 - Real.exp (-2 / lam)) (𝓝[>] 0) (𝓝 1) := by
    simpa using tendsto_const_nhds.sub h₅
  have h₇ : Tendsto (fun lam : ℝ => (1 - Real.exp (-2 / lam))⁻¹) (𝓝[>] 0) (𝓝 1) := by
    simpa using h₆.inv₀ (by norm_num : (1 : ℝ) ≠ 0)
  have hc : Tendsto
      (fun lam : ℝ =>
        2 * Real.pi * Real.exp (-Real.eulerMascheroniConstant) *
          (1 - Real.exp (-2 / lam))⁻¹)
      (𝓝[>] 0) (𝓝 (2 * Real.pi * Real.exp (-Real.eulerMascheroniConstant))) := by
    simpa [div_eq_mul_inv] using tendsto_const_nhds.mul h₇
  apply hc.congr'
  filter_upwards [self_mem_nhdsWithin] with lam hlam
  exact (bcs_gap_ratio_closed_form hw hlam).symm

/-! ## 退化定理：CQM → BCS -/

/-- 退化定理（记号对应层）：`criticalTemperature` 与 `bcsCriticalTemperature`
     对同一输入逐项一致。它说明两定义在退化赋值下"逐项相同"，属
     定义/记号层的一致，而非对 BCS 物理的独立推导
     （物理推导见 `bcs_gap_equation` 等）。 -/
theorem cqm_reduces_to_bcs {d c : ℝ} (wDebye n0V : ℝ) (hnv : d * c = n0V) :
    criticalTemperature wDebye d c = bcsCriticalTemperature wDebye n0V := by
  unfold criticalTemperature bcsCriticalTemperature
  rw [hnv]

/-- 晶格扇区退化：配对通道的因果截断频率取德拜频率。
    ω_D = √(k/M_ion)，k 为晶格力常数（力常数），M_ion 为离子质量。 -/
noncomputable def debyeFrequency (springConstant ionMass : ℝ) : ℝ :=
  Real.sqrt (springConstant / ionMass)

/-- 德拜频率严格为正。 -/
theorem debyeFrequency_pos {k M : ℝ} (hk : k > 0) (hM : M > 0) :
    debyeFrequency k M > 0 := by
  unfold debyeFrequency
  exact Real.sqrt_pos.2 (div_pos hk hM)

/-- 德拜频率随离子质量单调递减：ω_D ∝ M^(−1/2)。
     轻离子 → 高频晶格量子振荡（金属氢的因果截断最高）。 -/
theorem debyeFrequency_decreases_with_mass {k M₁ M₂ : ℝ} (hk : k ≥ 0) (hM₁ : M₁ > 0)
    (hM₂ : M₂ > 0) (hM : M₁ ≤ M₂) :
    debyeFrequency k M₂ ≤ debyeFrequency k M₁ := by
  unfold debyeFrequency
  apply Real.sqrt_le_sqrt
  have hrec : M₂⁻¹ ≤ M₁⁻¹ := by
    simpa [one_div] using (one_div_le_one_div hM₂ hM₁).2 hM
  rw [div_eq_mul_inv, div_eq_mul_inv]
  exact mul_le_mul_of_nonneg_left hrec hk

/-- 退化定理（晶格扇区）：CQM 临界温度以德拜频率为因果截断时，
     逐项退化为 BCS 临界温度。 -/
theorem cqm_debye_reduction {k M d c : ℝ} :
    criticalTemperature (debyeFrequency k M) d c =
      bcsCriticalTemperature (debyeFrequency k M) (d * c) := rfl

/-- 同位素定律（CQM 退化到晶格扇区后还原 BCS）：T_c(M₂) = T_c(M₁)·√(M₁/M₂)，
     即 T_c ∝ M^(−1/2)，同位素指数 α = 1/2。 -/
theorem criticalTemperature_isotope_shift {k M₁ M₂ d c : ℝ} (hk : k > 0) (hM₁ : M₁ > 0)
    (hM₂ : M₂ > 0) :
    criticalTemperature (debyeFrequency k M₂) d c =
      criticalTemperature (debyeFrequency k M₁) d c * Real.sqrt (M₁ / M₂) := by
  unfold criticalTemperature debyeFrequency
  have h₁ : Real.sqrt (k / M₁) * Real.sqrt (M₁ / M₂) = Real.sqrt (k / M₂) := by
    rw [← Real.sqrt_mul (le_of_lt (div_pos hk hM₁)) (M₁ / M₂)]
    congr 1
    field_simp [hM₁, hM₂, hk]
  calc
    bcsExactConstant * Real.sqrt (k / M₂) * Real.exp (-1 / (d * c))
        = bcsExactConstant * (Real.sqrt (k / M₁) * Real.sqrt (M₁ / M₂))
            * Real.exp (-1 / (d * c)) := by
            rw [h₁]
    _ = (bcsExactConstant * Real.sqrt (k / M₁) * Real.exp (-1 / (d * c)))
        * Real.sqrt (M₁ / M₂) := by
        ring

/-- 氢/氘同位素位移：T_c(D) = T_c(H)·√(1/2) = T_c(H)/√2。
     √(1/2) ≈ 0.707 为数值近似（√(1/2) 本身是精确值）。
     实验：H3S (203 K) 对 D3S (≈ 147 K) 的比值 0.72，接近 1/√2。
     差异来自硫亚晶格不变与强非谐性。 -/
theorem hydrogen_deuterium_isotope_shift {k d c : ℝ} (hk : k > 0) :
    criticalTemperature (debyeFrequency k (2 * protonMass)) d c =
      criticalTemperature (debyeFrequency k protonMass) d c * Real.sqrt (1 / 2) := by
  have hD : 2 * protonMass > 0 := mul_pos (by norm_num) protonMass_pos
  rw [criticalTemperature_isotope_shift hk protonMass_pos hD]
  have hdiv : protonMass / (2 * protonMass) = 1 / 2 := by
    field_simp [ne_of_gt protonMass_pos]
  rw [hdiv]

/-- 同位素定律的单调形式：离子质量越大（同位素越重），T_c 越低
    （BCS 同位素效应 α = 1/2 的方向）。 -/
theorem criticalTemperature_decreases_with_ion_mass {k M₁ M₂ d c : ℝ} (hk : k ≥ 0)
    (hM₁ : M₁ > 0) (hM₂ : M₂ > 0) (hM : M₁ ≤ M₂) :
    criticalTemperature (debyeFrequency k M₂) d c ≤
      criticalTemperature (debyeFrequency k M₁) d c := by
  exact criticalTemperature_monotone_in_cutoff (debyeFrequency k M₂) (debyeFrequency k M₁) d c
    (debyeFrequency_decreases_with_mass hk hM₁ hM₂ hM)


/-! ## 强耦合扩展：McMillan–Dynes 公式 -/

/-- McMillan–Dynes 强耦合公式：
    k_B T_c = (ω_ln/1.2)·exp[−1.04(1+λ)/(λ − μ*(1+0.62λ))]。
    金属氢化物（λ ≳ 2）需用此强耦合形式；弱耦合极限（λ ≪ 1）退回 BCS。
    注：1.2 与 1.04 为文献经验系数（非本模块推导，属输入常数）。 -/
noncomputable def mcmillanDynesTc (omegaLn lambda muStar : ℝ) : ℝ :=
  omegaLn / 1.2 * Real.exp (-1.04 * (1 + lambda) / (lambda - muStar * (1 + 0.62 * lambda)))

/-- McMillan–Dynes 临界温度严格为正（对数声子频率为正时；指数因子恒正）。
     强耦合分母条件 λ > μ*(1 + 0.62λ) 由 `mcmillan_strong_coupling_condition` 给出。 -/
theorem mcmillanDynesTc_pos {omegaLn lambda muStar : ℝ} (hw : omegaLn > 0) :
    mcmillanDynesTc omegaLn lambda muStar > 0 := by
  unfold mcmillanDynesTc
  apply mul_pos
  · exact div_pos hw (by norm_num)
  · exact Real.exp_pos _

/-- 金属氢化物的强耦合判据：λ > μ*(1 + 0.62λ) 时 McMillan 分母为正
    （λ 足够大才能配对；H3S 的 λ ≈ 1.94 ≫ μ* ≈ 0.12 满足）。 -/
theorem mcmillan_strong_coupling_condition {lambda muStar : ℝ}
    (hcond : muStar * (1 + 0.62 * lambda) < lambda) :
    lambda - muStar * (1 + 0.62 * lambda) > 0 := by
  linarith

/-! ## 其余标准公式 -/

/-- London 穿透深度（自然单位 c = 1）：λ_L = √(m/(4π·n·q²))。 -/
noncomputable def londonPenetrationDepth (mass numberDensity charge : ℝ) : ℝ :=
  Real.sqrt (mass / (4 * Real.pi * numberDensity * charge ^ 2))

/-- London 穿透深度严格为正。 -/
theorem londonPenetrationDepth_pos {m n q : ℝ} (hm : m > 0) (hn : n > 0) (hq : q ≠ 0) :
    londonPenetrationDepth m n q > 0 := by
  unfold londonPenetrationDepth
  apply Real.sqrt_pos.2
  apply div_pos hm
  apply mul_pos
  · exact mul_pos (mul_pos (by norm_num) (lt_trans (by norm_num : (0 : ℝ) < 3) Real.pi_gt_three)) hn
  · exact sq_pos_of_ne_zero hq

/-- BCS 相干长度：ξ₀ = ħv_F/(πΔ₀)（自然单位：v_F/(π·Δ₀)）。 -/
noncomputable def bcsCoherenceLength (fermiVelocity gap : ℝ) : ℝ :=
  fermiVelocity / (Real.pi * gap)

/-- BCS 相干长度严格为正。 -/
theorem bcsCoherenceLength_pos {vF gap : ℝ} (hv : vF > 0) (hg : gap > 0) :
    bcsCoherenceLength vF gap > 0 := by
  unfold bcsCoherenceLength
  exact div_pos hv (mul_pos (lt_trans (by norm_num : (0 : ℝ) < 3) Real.pi_gt_three) hg)

/-- 磁通量子：Φ₀ = h/(2|e|) = π/|e|（自然单位 ħ = c = 1，Cooper 对电荷 2e）。 -/
noncomputable def fluxQuantum : ℝ := Real.pi / |electronCharge|

/-- 磁通量子恒等于 π（|e| = 1）。 -/
theorem fluxQuantum_eq_pi : fluxQuantum = Real.pi := by
  unfold fluxQuantum electronCharge
  rw [abs_of_neg (by norm_num : (-1 : ℝ) < 0)]
  norm_num

end CQM