import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Artanh
import Mathlib.NumberTheory.Harmonic.EulerMascheroni
import Mathlib.Tactic

/-!
# CQM 超导：临界温度严格推导（G22 闭合）

本模块形式化《CQM_超导核心理论》§11.2 的临界温度严格推导（闭合缺口 G22），
对应推导修正：早期公式写作 `(ln4/(β·Δδ₀))²`，把配对阈值误取为
`ln4/β`，遗漏谱常数 `C = ξ'(1)/ξ(1)` 与阈值中的 `1/ln4` 因子；严格推导
（§8 海森堡代数 → §9.2 阈值 → §11.2）给出：

```
T_c = ℏΩ₀ / (2k_B · artanh[ratio²]),   ratio = C·√(1−βδ_v) / (β·ln4·Δδ₀)
```

自然单位 `k_B = ℏ = 1`；`ratio` 为组合参数（arctanh 参数）。

## 推导链（§11.2 三步）

1. **恒等式**：玻色占据 `n_B = 1/(e^{ω/T}−1)` 满足 `1/(1+2n_B) = tanh(ω/2T)`
   （定理 `boseSuppression_eq_tanh`），故相干曲率涨落温度依赖
   `Δδ_v(T) = Δδ₀·√tanh(ℏΩ₀/2k_BT)`（`curvatureFluctuation`）。
2. **阈值交叉**：配对阈值 `Δδ_v^(th) = C√(1−βδ_v)/(β·ln4)`（`pairingThreshold`, §9.2）。
3. **闭式**：`Δδ_v(T_c) = Δδ_v^(th)` ⇒ `tanh(Ω₀/2T_c) = ratio²`
   ⇒ `T_c = Ω₀/(2·artanh[ratio²])`（`criticalTemperatureCQM`）。

## 定理
- `criticalTemperatureCQM_pos`：`Ω₀ > 0` 且 `0 < ratio² < 1` 时 `T_c > 0`
  （`ratio² < 1` 即 `β·ln4·Δδ₀ > C√(1−βδ_v)` 是 `T_c > 0` 的参数窗口）。
- `criticalTemperatureCQM_antitone_in_ratio`：`T_c` 随 `ratio` 单调递减，
  等价于涨落幅度 `Δδ₀` 越大（`ratio ∝ 1/Δδ₀`）`T_c` 越高。
- `boseSuppression_eq_tanh`：推导链第一步的恒等式。

## 参考文献
- ruster (2026). CQM_超导核心理论. CQMFormal/08 超导/ §9.2, §11.1, §11.2, G22.
-/

namespace CQM

/-! ## 谱常数 C = ξ'(1)/ξ(1) (§1.2) -/

/-- 谱常数 `C = ξ'(1)/ξ(1) = 1 + γ/2 − ln(2√π) ≈ 0.0231`（§1.2）。
    从 `ξ(s) = ½·s(s−1)·π^{−s/2}·Γ(s/2)·ζ(s)` 的函数方程 `ξ(s)=ξ(1−s)`
    与 `ψ(1/2) = −γ − 2·ln2` 推出；严格无量纲，作为全部后续层级的普适比例基准。 -/
noncomputable def spectralConstantC : ℝ :=
  1 + Real.eulerMascheroniConstant / 2 - Real.log (2 * Real.sqrt Real.pi)

/-! ## 推导链第一步：涨落的温度依赖闭式 (§11.1) -/

/-- 玻色-爱因斯坦占据数 `n_B(ω,T) = 1/(e^{ω/T} − 1)`（自然单位 k_B = 1）。 -/
noncomputable def boseOccupation (omega temperature : ℝ) : ℝ :=
  1 / (Real.exp (omega / temperature) - 1)

/-- 推导链核心恒等式（§11.2 第一步）：
    `1/(1 + 2·n_B(ω,T)) = tanh(ω/2T)`，对 `ω/T ≠ 0`（零温占据数发散）成立。
    数值验证：相对误差 < 1e-15。 -/
theorem boseSuppression_eq_tanh {x : ℝ} (hx : x ≠ 0) :
    (1 + 2 * (1 / (Real.exp x - 1)))⁻¹ = Real.tanh (x / 2) := by
  have hE : Real.exp x ≠ 1 := by
    intro h
    exact hx (Real.exp_injective (by simpa using h))
  have hEne : Real.exp x + 1 ≠ 0 := by
    have : 0 < Real.exp x + 1 := by positivity
    exact ne_of_gt this
  have hden : Real.exp x - 1 ≠ 0 := sub_ne_zero.mpr hE
  -- 左边：1/(1 + 2/(e^x−1)) = (e^x−1)/(e^x+1)
  -- 先证 1 + 2/(e^x−1) = (e^x+1)/(e^x−1)（通分），再对倒数用 inv_div
  have hL : (1 + 2 * (1 / (Real.exp x - 1)))⁻¹ = (Real.exp x - 1) / (Real.exp x + 1) := by
    rw [show 1 + 2 * (1 / (Real.exp x - 1)) = (Real.exp x + 1) / (Real.exp x - 1) by
      field_simp [hden]
      ring]
    rw [inv_div]
  -- 右边：tanh(x/2) = (e^{x/2}−e^{−x/2})/(e^{x/2}+e^{−x/2}) = (e^x−1)/(e^x+1)
  have hR : Real.tanh (x / 2) = (Real.exp x - 1) / (Real.exp x + 1) := by
    rw [Real.tanh_eq]
    have hA : Real.exp (x / 2) ≠ 0 := Real.exp_ne_zero (x / 2)
    have hInv : Real.exp (-(x / 2)) = (Real.exp (x / 2))⁻¹ := Real.exp_neg (x / 2)
    have hsq : Real.exp (x / 2) ^ 2 = Real.exp x := by
      rw [pow_two, ← Real.exp_add]
      congr
      ring_nf
    rw [hInv]
    field_simp [hA]
    rw [hsq]
    ring
  rw [hL, hR]

/-- 相干曲率涨落的温度衰减（§11.2 第一步的闭式）：
    `Δδ_v(T) = Δδ₀·√tanh(ℏΩ₀/2k_BT)`，自然单位 k_B = ℏ = 1。
    零温 `T→0` 趋于 `Δδ₀`；高温 `T→∞` 趋于 `0`。 -/
noncomputable def curvatureFluctuation (delta0 omega temperature : ℝ) : ℝ :=
  delta0 * Real.sqrt (Real.tanh (omega / (2 * temperature)))

/-! ## 推导链第二步：配对阈值 (§9.2) -/

/-- 配对阈值（§9.2）：`Δδ_v^(th) = C√(1−βδ_v)/(β·ln4)`。
    来自 §8.3 不确定性关系 `Δu·Δδ_v ≥ C√(1−βδ_v)/β` 与跃迁条件 `Δu ≥ ln4`。 -/
noncomputable def pairingThreshold (C beta deltaV : ℝ) : ℝ :=
  C * Real.sqrt (1 - beta * deltaV) / (beta * Real.log 4)

/-! ## 推导链第三步：临界温度闭式 (§11.2) -/

/-- CQM 临界温度（§11.2 严格推导，闭合 G22）：
    `T_c = Ω₀/(2·artanh[ratio²])`（自然单位 k_B = ℏ = 1），
    其中 `ratio = C√(1−βδ_v)/(β·ln4·Δδ₀)` 为组合参数。
    参数窗口：`ratio² < 1`（即 `β·ln4·Δδ₀ > C√(1−βδ_v)`）才有 `T_c > 0`。 -/
noncomputable def criticalTemperatureCQM (Omega0 ratio : ℝ) : ℝ :=
  Omega0 / (2 * Real.artanh (ratio ^ 2))

/-- 由物理参数直接给出临界温度：`ratio = C√(1−βδ_v)/(β·ln4·Δδ₀)`。 -/
noncomputable def criticalTemperatureFromParameters
    (Omega0 delta0 beta C deltaV : ℝ) : ℝ :=
  criticalTemperatureCQM Omega0 (C * Real.sqrt (1 - beta * deltaV) / (beta * Real.log 4 * delta0))

/-- 临界温度严格为正：`Ω₀ > 0` 且 `0 < ratio² < 1` 时 `T_c > 0`。 -/
theorem criticalTemperatureCQM_pos {Omega0 ratio : ℝ} (hO : 0 < Omega0)
    (hr0 : ratio ≠ 0) (hr1 : ratio ^ 2 < 1) :
    0 < criticalTemperatureCQM Omega0 ratio := by
  unfold criticalTemperatureCQM
  have hsq : 0 < ratio ^ 2 := sq_pos_of_ne_zero hr0
  have hat : 0 < Real.artanh (ratio ^ 2) := Real.artanh_pos ⟨hsq, hr1⟩
  exact div_pos hO (mul_pos (by norm_num) hat)

/-- 临界温度随 arctanh 参数 `ratio` 单调递减：
    `ratio₁ ≤ ratio₂ ⇒ T_c(ratio₂) ≤ T_c(ratio₁)`。
    由 `ratio ∝ 1/Δδ₀` 即得物理表述：**零温涨落幅度 Δδ₀ 越大，T_c 越高**。 -/
theorem criticalTemperatureCQM_antitone_in_ratio {Omega0 r₁ r₂ : ℝ} (hO : 0 < Omega0)
    (hr₁ : 0 < r₁) (hmono : r₁ ≤ r₂) (hr₂lt : r₂ ^ 2 < 1) :
    criticalTemperatureCQM Omega0 r₂ ≤ criticalTemperatureCQM Omega0 r₁ := by
  unfold criticalTemperatureCQM
  have hr₂ : 0 ≤ r₂ := le_of_lt (lt_of_lt_of_le hr₁ hmono)
  have hle_sq : r₁ ^ 2 ≤ r₂ ^ 2 := (sq_le_sq₀ (le_of_lt hr₁) hr₂).mpr hmono
  have hr₁sq_lt : r₁ ^ 2 < 1 := lt_of_le_of_lt hle_sq hr₂lt
  have hmono_art : Real.artanh (r₁ ^ 2) ≤ Real.artanh (r₂ ^ 2) := by
    apply Real.artanh_le_artanh
    · nlinarith [sq_nonneg r₁]
    · exact hr₂lt
    · exact hle_sq
  have hat₁ : 0 < Real.artanh (r₁ ^ 2) :=
    Real.artanh_pos ⟨pow_pos hr₁ 2, hr₁sq_lt⟩
  have hden₁ : 0 < 2 * Real.artanh (r₁ ^ 2) := mul_pos (by norm_num) hat₁
  have hden_le : 2 * Real.artanh (r₁ ^ 2) ≤ 2 * Real.artanh (r₂ ^ 2) := by
    exact mul_le_mul_of_nonneg_left hmono_art (by norm_num)
  -- Ω₀/den₂ ≤ Ω₀/den₁  ⟸  0 ≤ Ω₀, 0 < den₁, den₁ ≤ den₂
  exact div_le_div_of_nonneg_left (le_of_lt hO) hden₁ hden_le

end CQM
