/-
  第 139 轮：环 4→5→9 的接口——ε 的矩到 v_τ 的矩
  ==========================================================================
  前件：R147 判 ε 的统计归 FG／材料。于是链只能经 (ε̄, σ²) 与关联 ρ 见到 ε。

  本文件承载纯代数部分：

    * 有理化恒等式 √a - √b = (a-b)/(√a+√b)：给出**精确**的一阶传递，
      故 v_τ'(ε₀) = -1/(4π v₀) 不是近似；
    * 凹性两点形式：√((a+b)/2) ≥ (√a+√b)/2（Jensen 的离散核），
      故 ⟨v_τ⟩ ≤ v₀ ——涨落使平均钟速变慢；
    * κ_f = 1/(4π v₀²) 与 v_τ' = -κ_f v₀ 的代数一致性（环 9 用同一个 κ_f）。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Order.Basic

namespace CQM.MomentTransfer

/-! ### 一、有理化恒等式 -/

/-- $\sqrt a-\sqrt b=\dfrac{a-b}{\sqrt a+\sqrt b}$（$a,b>0$）。 -/
theorem sqrt_sub_sqrt (a b : ℝ) (ha : 0 < a) (hb : 0 < b) :
    Real.sqrt a - Real.sqrt b = (a - b) / (Real.sqrt a + Real.sqrt b) := by
  have h1 : Real.sqrt a * Real.sqrt a = a := Real.mul_self_sqrt (le_of_lt ha)
  have h2 : Real.sqrt b * Real.sqrt b = b := Real.mul_self_sqrt (le_of_lt hb)
  have hkey : (Real.sqrt a - Real.sqrt b) * (Real.sqrt a + Real.sqrt b) = a - b := by
    nlinarith
  have hpos : 0 < Real.sqrt a + Real.sqrt b := by positivity
  field_simp
  linarith [hkey]

/-- 推论：$|\sqrt a-\sqrt b|=\dfrac{|a-b|}{\sqrt a+\sqrt b}$。 -/
theorem abs_sqrt_sub_sqrt (a b : ℝ) (ha : 0 < a) (hb : 0 < b) :
    |Real.sqrt a - Real.sqrt b| = |a - b| / (Real.sqrt a + Real.sqrt b) := by
  rw [sqrt_sub_sqrt a b ha hb, abs_div]
  have : 0 < Real.sqrt a + Real.sqrt b := by positivity
  rw [abs_of_pos this]

/-! ### 二、$v_\tau$ 的一阶系数 -/

/-- $v_\tau(\varepsilon)=\sqrt{1-\varepsilon/2\pi}$。 -/
noncomputable def vtau (eps : ℝ) : ℝ := Real.sqrt (1 - eps / (2 * Real.pi))

/-- 有理化形式下的一阶差分：$v_\tau(\varepsilon+\delta)-v_\tau(\varepsilon)
     =-\dfrac{\delta/2\pi}{v_\tau(\varepsilon+\delta)+v_\tau(\varepsilon)}$。 -/
theorem vtau_diff (eps delta : ℝ)
    (h1 : 0 < 1 - (eps + delta) / (2 * Real.pi))
    (h2 : 0 < 1 - eps / (2 * Real.pi)) :
    vtau (eps + delta) - vtau eps =
      -((eps + delta) / (2 * Real.pi) - eps / (2 * Real.pi)) /
        (vtau (eps + delta) + vtau eps) := by
  unfold vtau
  rw [sqrt_sub_sqrt _ _ h1 h2]
  congr 1
  ring

/-- 一阶系数与 $\kappa_f$ 的一致性：若 $v'=-\kappa_f v_0$、$\kappa_f=1/(4\pi v_0^2)$，
    则 $v'=-1/(4\pi v_0)$。 -/
theorem slope_consistency (v0 : ℝ) (hv : 0 < v0) :
    -(1 / (4 * Real.pi * v0 ^ 2)) * v0 = -(1 / (4 * Real.pi * v0)) := by
  field_simp

/-! ### 三、Jensen：凹性两点形式 -/

/-- $\dfrac{\sqrt a+\sqrt b}{2}\le\sqrt{\dfrac{a+b}{2}}$（$a,b\ge0$）。 -/
theorem sqrt_concave_two (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) :
    (Real.sqrt a + Real.sqrt b) / 2 ≤ Real.sqrt ((a + b) / 2) := by
  have h1 : Real.sqrt a * Real.sqrt a = a := Real.mul_self_sqrt ha
  have h2 : Real.sqrt b * Real.sqrt b = b := Real.mul_self_sqrt hb
  have hsq : ((Real.sqrt a + Real.sqrt b) / 2) ^ 2 ≤ (a + b) / 2 := by
    nlinarith [sq_nonneg (Real.sqrt a - Real.sqrt b)]
  have hnonneg : 0 ≤ (Real.sqrt a + Real.sqrt b) / 2 := by positivity
  have h := Real.sqrt_le_sqrt hsq
  rwa [Real.sqrt_sq hnonneg] at h

/-- 推论（两态涨落的 Jensen）：若 $v_1,v_2\ge0$，则其平均不超过
    「平均亏角处的 $v_\tau$」——涨落使平均钟速变慢。 -/
theorem jensen_slowdown (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) :
    (Real.sqrt a + Real.sqrt b) / 2 ≤ Real.sqrt ((a + b) / 2) :=
  sqrt_concave_two a b ha hb

/-- 两态版本的减慢量为正：$\sqrt{(a+b)/2}-\dfrac{\sqrt a+\sqrt b}{2}\ge0$。 -/
theorem slowdown_nonneg (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) :
    0 ≤ Real.sqrt ((a + b) / 2) - (Real.sqrt a + Real.sqrt b) / 2 := by
  have := sqrt_concave_two a b ha hb
  linarith

end CQM.MomentTransfer
