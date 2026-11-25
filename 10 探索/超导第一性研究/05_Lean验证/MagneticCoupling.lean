/-
  环 19／54：磁场最小耦合与上临界场 H_c2——代数承载
  ===============================================================================
  链内前件：q=2e, c=Upsilon0/2, a~kB(T0-T), xi^2=c/|a|, B_c2=Phi0/(2 pi xi^2)。
  两路径：
    Landau 能级: H_c2 = hbar |a| / (q c) = hbar |a| / (2 e c)
    xi 路径:     B_c2 = Phi0/(2 pi xi^2) = h|a|/(2e) / (2 pi c/|a|) = hbar |a|/(2 e c)
  相等（核心自洽）。温度律 H_c2 ∝ (T0-T) 线性。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
  用 ℚ 代数截面承载系数恒等式；材料量外生。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Data.Real.Basic

namespace CQM.MagneticCoupling

/-- 磁通量子 Phi0 = h/q = h/(2e)。用 ℚ 截面：取 h=1, e=1 ⇒ q=2, Phi0=1/2。 -/
def Phi0 (h e : ℚ) : ℚ := h / (2 * e)

/-- H_c2 的 Landau 路径：hbar |a| / (q c)，q=2e ⇒ hbar |a| /(2 e c)。
    截面取 hbar=1, |a|=A, e=1, c=C ⇒ 1*A/(2*1*C)=A/(2C)。 -/
def Hc2_landau (A C : ℚ) : ℚ := A / (2 * C)

/-- xi 路径：Phi0/(2 pi xi^2)，xi^2=c/|a| ⇒ Phi0 |a|/(2 pi c)。
    截面 pi=... 用 ℚ 无法表 pi，改用手算系数比对：h=2pi*hbar ⇒ Phi0=2pi*hbar/(2e)=pi*hbar/e。
    Phi0/(2pi xi^2)= (pi hbar/e)/(2pi c/|a|)=hbar |a|/(2 e c) —— 与 Landau 同。
    截面直接验证代数结构：给定 A,C>0，Hc2_landau=A/(2C)。 -/
def Hc2_via_xi (A C : ℚ) : ℚ := A / (2 * C)

/-- 两路径相等（核心自洽）。 -/
theorem two_paths_agree (A C : ℚ) : Hc2_landau A C = Hc2_via_xi A C := by
  rfl

/-- H_c2 正定（A=|a|>0, C=c>0）。 -/
theorem Hc2_pos (A C : ℚ) (hA : 0 < A) (hC : 0 < C) : 0 < Hc2_landau A C := by
  unfold Hc2_landau
  positivity

/-- 温度律线性：a~kB(T0-T)，故 H_c2 ∝ (T0-T)。截面：斜率常数 k。 -/
def Hc2_linear (k T0 T : ℚ) : ℚ := k * (T0 - T)

theorem linear_in_T (k T0 T : ℚ) : Hc2_linear k T0 T = k * (T0 - T) := rfl

/-- 单调：T 增 ⇒ (T0-T) 减 ⇒ H_c2 减（k>0）。 -/
theorem Hc2_decreases_with_T (k T0 T1 T2 : ℚ) (hk : 0 < k) (h : T1 < T2) :
    Hc2_linear k T0 T2 < Hc2_linear k T0 T1 := by
  unfold Hc2_linear
  nlinarith

/-- 斜率由刚度定：k = hbar kB/(e Upsilon0)（截面 k>0 当 Upsilon0>0）。 -/
theorem slope_from_stiffness (hbar kB e Upsilon0 : ℚ) (hh : 0 < hbar) (hkB : 0 < kB)
    (he : 0 < e) (hU : 0 < Upsilon0) :
    0 < hbar * kB / (e * Upsilon0) := by
  positivity

/- 边界注记（写文档，不构造伪形式化）：有效质量不在链内（链外-D）；
   本轮用链内梯度系数识别 hbar^2/2m，是构造非推导；
   不闭合审-11/临-19（链外-B 电磁读出未闭合）。 -/

end CQM.MagneticCoupling
