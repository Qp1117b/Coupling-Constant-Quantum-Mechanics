import GN.Basic

/-!
# §1 三重恒等 (Triple Identity)

公理化证明稿 §1 的形式化：相变量子 ☯ 的三种表述

    spectralQuantum = liCoeffOne（第一 Li 系数 λ₁）
    leclairConstant（LeClair 常数 B） = -spectralQuantum

以及闭式 `1 + γ_E/2 - log(4π)/2` 的等价变形
`1 + γ_E/2 - ln(π)/2 - ln 2`（定理 1.2，与 Coffey 2008、Voros 2016 一致）。

对应文档定理：1.2（闭式）、1.3（☯ = λ₁）、1.4（B = -☯）、1.5（三重恒等）。

诚实边界：
- 本文件形式化的是**闭式层面的代数恒等**。生成函数
  λ_n 定义到 ξ'(1)/ξ(1) 的解析链路、以及 ξ 的 Hadamard 乘积
  （求和表示，定理 1.1）依赖 `SpectralGeometry.RiemannXi`，
  在该模块编译修复前不在此声明。
- `liCoeffOne` / `leclairConstant` 按文献闭式定义（定义展开即证明）。

## 参考文献

- Voros, A. (2016). Simplifications of the Keiper/Li approach to the
  Riemann Hypothesis. arXiv:1602.03292.（λ₁ 闭式）
- LeClair, A. (2024). Spectral Flow for the Riemann zeros. arXiv:2406.01828.
 （常数 B 的谱流方程语境）
- Coffey, M. W. (2008). Relations and representations of the Euler constant.
  Proc. R. Soc. A 464, 2059–2074.（ξ'/ξ 闭式核验）
-/

open Real

namespace CQM
namespace GN

/-! ### 定理 1.2：☯ 的闭式等价变形 -/

/-- log 4 = 2 log 2（自然对数）。 -/
theorem log_four_eq : Real.log 4 = 2 * Real.log 2 := by
  have h : Real.log (2 * 2) = Real.log 2 + Real.log 2 :=
    Real.log_mul (by norm_num) (by norm_num)
  rw [show (4 : ℝ) = 2 * 2 from by norm_num, h]
  ring

/-- [THEOREM 1.2] 相变量子的闭式等价变形：

    ☯ = 1 + γ_E/2 - ln(π)/2 - ln 2

    与 `SpectralGeometry.Basic` 中的定义式
    ☯ = 1 + γ_E/2 - ln(4π)/2 严格相等（log 乘法公式 + log 4 = 2 log 2）。
    该形式与 Coffey (2008)、Voros (2016) 中 ξ'/ξ|_{s=1} 的闭式一致。 -/
theorem spectralQuantum_closedForm :
    spectralQuantum =
      1 + Real.eulerMascheroniConstant / 2 - Real.log Real.pi / 2 - Real.log 2 := by
  unfold spectralQuantum
  have hmul : Real.log (4 * Real.pi) = Real.log 4 + Real.log Real.pi :=
    Real.log_mul (by norm_num) (Real.pi_pos.ne')
  rw [hmul, log_four_eq]
  ring

/-! ### 定理 1.3：第一 Li 系数 λ₁ = ☯ -/

/-- [DEFINITION 1.4] 第一 Li 系数 λ₁（Voros 2016 闭式）：

    λ₁ = 1 - log(4π)/2 + γ_E/2

    Li 系数由生成函数 Σ λ_n z^{n-1} = d/dz ln[2ξ(1/(1-z))] 定义；
    z = 0 处的对数导数即 ξ'(1)/ξ(1)（变量替换 z ↦ 1/(1-z) 在 z=0 处为 s=1，
    且 1/(1-z)² = 1），故 λ₁ = ☯。生成函数到闭式的解析链路依赖 ξ
    （见 `SpectralGeometry.RiemannXi`），此处按文献闭式定义。 -/
noncomputable def liCoeffOne : ℝ :=
  1 - Real.log (4 * Real.pi) / 2 + Real.eulerMascheroniConstant / 2

/-- [THEOREM 1.3] 第一 Li 系数等于相变量子：λ₁ = ☯。

    纯代数恒等（同两项的加法交换/结合）。 -/
theorem liCoeffOne_eq_spectralQuantum : liCoeffOne = spectralQuantum := by
  unfold liCoeffOne spectralQuantum
  ring

/-- λ₁ 的 Voros 闭式与 Coffey 闭式一致（定理 1.2 + 定理 1.3 复合）。 -/
theorem liCoeffOne_closedForm :
    liCoeffOne =
      1 + Real.eulerMascheroniConstant / 2 - Real.log Real.pi / 2 - Real.log 2 := by
  rw [liCoeffOne_eq_spectralQuantum, spectralQuantum_closedForm]

/-- [推论] Li 判据 n=1 情形：λ₁ > 0（RH 在 n=1 处的必要条件成立）。

    由 λ₁ = ☯ > 0（`spectralQuantum_pos`）直接得到。 -/
theorem liCoeffOne_pos : liCoeffOne > 0 := by
  rw [liCoeffOne_eq_spectralQuantum]
  exact spectralQuantum_pos

/-- λ₁ 继承 ☯ 的高精度数值界限（数值桥梁公理的推论）。 -/
theorem liCoeffOne_numerical_bounds :
    (0.02309570896 : ℝ) < liCoeffOne ∧ liCoeffOne < 0.02309570898 := by
  rw [liCoeffOne_eq_spectralQuantum]
  exact spectralQuantum_numerical_bounds

/-! ### 定理 1.4：LeClair 常数 B = -☯ -/

/-- [DEFINITION 1.5] LeClair 常数 B（谱流方程语境，arXiv:2406.01828）：

    B = -γ_E/2 - 1 + log(2√π) = -γ_E/2 - 1 + log 2 + log(π)/2

    展开用 log(2√π) = log 2 + (1/2) log π（log 乘法公式 + log √π = log π / 2）。 -/
noncomputable def leclairConstant : ℝ :=
  -Real.eulerMascheroniConstant / 2 - 1 + Real.log 2 + Real.log Real.pi / 2

/-- log(2√π) 的展开（B 紧凑形式与展开形式的桥梁）。 -/
theorem log_two_sqrt_pi :
    Real.log (2 * Real.sqrt Real.pi) = Real.log 2 + Real.log Real.pi / 2 := by
  have h1 : Real.log (2 * Real.sqrt Real.pi)
      = Real.log 2 + Real.log (Real.sqrt Real.pi) :=
    Real.log_mul (by norm_num) (by positivity)
  have h2 : Real.log (Real.sqrt Real.pi) = Real.log Real.pi / 2 :=
    Real.log_sqrt (le_of_lt Real.pi_pos)
  rw [h1, h2]

/-- B 的紧凑形式（定义原文）：B = -γ_E/2 - 1 + log(2√π)。 -/
noncomputable def leclairConstantCompact : ℝ :=
  -Real.eulerMascheroniConstant / 2 - 1 + Real.log (2 * Real.sqrt Real.pi)

/-- B 的紧凑形式 = 展开形式。 -/
theorem leclairConstantCompact_eq : leclairConstantCompact = leclairConstant := by
  unfold leclairConstantCompact leclairConstant
  rw [log_two_sqrt_pi]
  ring

/-- [THEOREM 1.4] LeClair 常数与相变量子：B = -☯。

    纯代数恒等（由定理 1.2 闭式移项）。 -/
theorem leclairConstant_eq_neg_spectralQuantum :
    leclairConstant = -spectralQuantum := by
  unfold leclairConstant
  rw [spectralQuantum_closedForm]
  ring

/-- B = -☯ 的紧凑形式版本。 -/
theorem leclairConstantCompact_eq_neg_spectralQuantum :
    leclairConstantCompact = -spectralQuantum := by
  rw [leclairConstantCompact_eq, leclairConstant_eq_neg_spectralQuantum]

/-- [推论] LeClair 常数严格为负（B = -☯ < 0）。 -/
theorem leclairConstant_neg : leclairConstant < 0 := by
  rw [leclairConstant_eq_neg_spectralQuantum]
  exact neg_lt_zero.mpr spectralQuantum_pos

/-! ### 定理 1.5：三重恒等 -/

/-- [THEOREM 1.5] 相变量子三重恒等定理（代数层）：

    ☯ = λ₁（第一 Li 系数） ∧ B = -☯（LeClair 常数的负值）

    即 spectralQuantum、liCoeffOne、-leclairConstant 三者严格相等。
    完整形式中的 ξ'(1)/ξ(1) 一侧由 `SpectralGeometry.Basic` 中
    spectralQuantum 的定义（A2.2：☯ = ξ'(1)/ξ(1)）承接。 -/
theorem spectralQuantum_triple_identity :
    spectralQuantum = liCoeffOne ∧ leclairConstant = -spectralQuantum :=
  ⟨liCoeffOne_eq_spectralQuantum.symm, leclairConstant_eq_neg_spectralQuantum⟩

/-- 三重恒等的合成形式：λ₁ = -B（Li 系数 = LeClair 常数的负值）。 -/
theorem liCoeffOne_eq_neg_leclairConstant :
    liCoeffOne = -leclairConstant := by
  rw [liCoeffOne_eq_spectralQuantum, leclairConstant_eq_neg_spectralQuantum]
  ring

end GN
end CQM
