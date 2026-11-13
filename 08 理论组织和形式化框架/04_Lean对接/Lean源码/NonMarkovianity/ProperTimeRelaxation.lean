import NonMarkovianity.Basic
import Superconductivity.CouplingSpace

/-!
# N1：角亏—固有时流速—弛豫时标 (ProperTimeRelaxation)

对应研究文档 `04 前沿研究/CQM_前沿研究_分布式不对易关系与非马尔可夫性.md` §5.7。

文档的【待推】命题 N1 提出：记忆核的空间不均匀性可写为局域弛豫时标

$$\tau_{\mathrm{relax}}(v)\ \propto\ \left(\frac{d\tau}{dt}\right)^{-1}_{v}
=\bigl(1-\beta\,\delta_v\bigr)^{-1/2}.$$

本模块只形式化这一**接口的结构部分**，不声称系数已由框架确定：

- `relaxationTime` 直接以既有固有时流速 `CQM.properTimeFlow` 为定义，
  即 $\tau_{\mathrm{relax}}=1/v_\tau$，比例系数取 1；
- 证明正性、闭式（平方根形式）、平直极限、随角亏单调、角亏使弛豫变慢。

## 边界（如实标注）

比例系数的来源、以及“弛豫时标”与因果截断不等式
$\Delta\tau\ge\tau_{\mathrm{res}}=\hbar/(Mc^2)$ 的衔接，属文档 §9.1 的【待推】N1，
**未在此证明**，也没有用 `axiom` 冒充。本模块不含任何数值校验。
-/

namespace CQM
namespace NonMarkovianity

/-- 局域弛豫时标（文档 §5.7 命题 N1 的接口形式）：
$$\tau_{\mathrm{relax}}=\frac{1}{v_\tau},\qquad v_\tau=\sqrt{1-\beta\,\delta}.$$ -/
noncomputable def relaxationTime (β δ : ℝ) : ℝ :=
  1 / CQM.properTimeFlow β δ

/-- N1 的比例关系：弛豫时标是固有时流速的倒数（系数取 1 的接口形式）。 -/
theorem relaxationTime_eq_inv_properTimeFlow (β δ : ℝ) :
    relaxationTime β δ = (CQM.properTimeFlow β δ)⁻¹ := by
  unfold relaxationTime
  rw [one_div]

/-- 与原文闭式一致：$\tau_{\mathrm{relax}}=(1-\beta\delta)^{-1/2}$，以平方根写出。 -/
theorem relaxationTime_eq_inv_sqrt (β δ : ℝ) :
    relaxationTime β δ = (Real.sqrt (1 - β * δ))⁻¹ := by
  unfold relaxationTime CQM.properTimeFlow
  rw [one_div]

/-- 弛豫时标正性：$\beta>0$、$0\le\delta<1/\beta$ 时 $\tau_{\mathrm{relax}}>0$。 -/
theorem relaxationTime_pos {β δ : ℝ} (hβ : 0 < β) (hδ : 0 ≤ δ)
    (hbound : δ < 1 / β) : 0 < relaxationTime β δ := by
  unfold relaxationTime
  exact div_pos one_pos (CQM.properTimeFlow_pos hβ hδ hbound)

/-- 平直极限（无角亏）：$\delta=0$ 时 $\tau_{\mathrm{relax}}=1$。 -/
theorem relaxationTime_at_zero (β : ℝ) : relaxationTime β 0 = 1 := by
  unfold relaxationTime CQM.properTimeFlow
  simp

/-- 角亏越大，弛豫越慢（非严格单调）：
$\delta_1\le\delta_2$ 且 $\beta\delta_2<1$ 时
$\tau_{\mathrm{relax}}(\delta_1)\le\tau_{\mathrm{relax}}(\delta_2)$。 -/
theorem relaxationTime_monotone {β δ₁ δ₂ : ℝ} (hβ : 0 < β) (hδ : δ₁ ≤ δ₂)
    (hbound : β * δ₂ < 1) : relaxationTime β δ₁ ≤ relaxationTime β δ₂ := by
  have hβδ : β * δ₁ ≤ β * δ₂ := mul_le_mul_of_nonneg_left hδ hβ.le
  have hpos₂ : 0 < 1 - β * δ₂ := by linarith
  have hle : Real.sqrt (1 - β * δ₂) ≤ Real.sqrt (1 - β * δ₁) :=
    Real.sqrt_le_sqrt (by linarith)
  have hsqrtpos : 0 < Real.sqrt (1 - β * δ₂) := Real.sqrt_pos.mpr hpos₂
  have h := one_div_le_one_div_of_le hsqrtpos hle
  unfold relaxationTime CQM.properTimeFlow
  exact h

/-- 角亏严格增大时弛豫严格变慢。 -/
theorem relaxationTime_strictMono {β δ₁ δ₂ : ℝ} (hβ : 0 < β) (hδ : δ₁ < δ₂)
    (hbound : β * δ₂ < 1) : relaxationTime β δ₁ < relaxationTime β δ₂ := by
  have hβδ : β * δ₁ < β * δ₂ := mul_lt_mul_of_pos_left hδ hβ
  have hpos₂ : 0 < 1 - β * δ₂ := by linarith
  have hlt : Real.sqrt (1 - β * δ₂) < Real.sqrt (1 - β * δ₁) :=
    Real.sqrt_lt_sqrt (by linarith) (by linarith)
  have hsqrtpos : 0 < Real.sqrt (1 - β * δ₂) := Real.sqrt_pos.mpr hpos₂
  have h := one_div_lt_one_div_of_lt hsqrtpos hlt
  unfold relaxationTime CQM.properTimeFlow
  exact h

/-- 正角亏使弛豫慢于平直情形：$\beta>0$、$0<\delta<1/\beta$ 时
$\tau_{\mathrm{relax}}>1$。 -/
theorem relaxationTime_gt_one {β δ : ℝ} (hβ : 0 < β) (hδ : 0 < δ)
    (hbound : β * δ < 1) : 1 < relaxationTime β δ := by
  have hx : 0 < 1 - β * δ := by linarith
  have hx1 : 1 - β * δ < 1 := by nlinarith [mul_pos hβ hδ]
  have hlt : Real.sqrt (1 - β * δ) < 1 := by
    have h := Real.sqrt_lt_sqrt hx.le hx1
    simpa using h
  have h := one_div_lt_one_div_of_lt (Real.sqrt_pos.mpr hx) hlt
  unfold relaxationTime CQM.properTimeFlow
  simpa using h

end NonMarkovianity
end CQM
