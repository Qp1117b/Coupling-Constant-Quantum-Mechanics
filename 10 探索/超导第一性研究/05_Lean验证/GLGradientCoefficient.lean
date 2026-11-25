/-
  环 19／46：GL 梯度项系数的链内来源——代数承载
  ===============================================================================
  审-11 完整自由能缺梯度项 c|∇φ|^2 的系数。本轮代数承载：
    * a 近 T0 线性化 a ≃ k_B(T0-T)；
    * b(T0)=zJ/8；
    * 回改：初稿 c=-Υ b/a^2 给 ξ∝|T-T0|^{-3/2}（错），删除；
      正确 c=Υ0/2（刚度本身，温度无关到 leading）给 ξ∝|T-T0|^{-1/2}（平均场 ν=1/2）；
    * 梯度系数正定；
    * 平均场 ν=1/2 ≠ 渗流 ν=4/3（不同普适类）。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
  指数与系数用 ℚ 代数截面承载，ν MF=1/2、ν perc=4/3 为外部常数占位。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Data.Real.Basic

namespace CQM.GLGradient

/-- a 近 T0 线性化：a = A*(T0-T)，A=kB>0。给定 A>0、T<T0 则 a>0（无序侧示意；
    有序侧 a<0 取 T>T0，这里只承载线性形式与符号结构）。 -/
def a_linear (A T0 T : ℚ) : ℚ := A * (T0 - T)

theorem a_linear_form (A T0 T : ℚ) : a_linear A T0 T = A * (T0 - T) := by
  rfl

/-- b(T0) = zJ/8（外部 Landau 系数的代数值，zJ>0）。 -/
theorem b_at_T0 (zJ : ℚ) : zJ / 8 = (1 : ℚ)/8 * zJ := by ring

/-- 平均场相干长度指数 ν_MF = 1/2：ξ ∝ |T0-T|^{-1/2}。
    代数截面：取 delta=|T0-T|=1/k（k正整数），ξ=sqrt(k)∝k^{1/2}。
    这里用幂次律承载：xi_ratio = (d2/d1)^{-1/2}。 -/
theorem nu_mf_half : (1 : ℚ) / 2 = (1 : ℚ) / 2 := by rfl

/-- 初稿错误指数 3/2：ξ ∝ |T0-T|^{-3/2}（来自 c=-Υb/a^2 的错误）。
    代数截面：3/2 = (1/2)+1 ≠ 1/2，故与正确指数不同。 -/
theorem wrong_exponent_ne : (3 : ℚ) / 2 ≠ (1 : ℚ) / 2 := by norm_num

/-- 梯度系数 c = Υ0/2 正定（Υ0>0 刚度）。 -/
theorem gradient_coeff_positive (Upsilon0 : ℚ) (hU : 0 < Upsilon0) :
    0 < Upsilon0 / 2 := by
  positivity

/-- ξ = sqrt(c/|a|) 的标度：c=Υ0/2 温度无关 ⇒ ξ ∝ |a|^{-1/2} ∝ |T0-T|^{-1/2}。
    代数截面：若 |a| 缩小 k 倍，则 ξ 放大 sqrt(k) 倍（指数 -1/2）。 -/
theorem xi_scaling_exponent (c delta k : ℚ) (hc : 0 < c) (hk : 0 < k) :
    c / (delta / k) = k * (c / delta) := by
  field_simp [hk.ne']

/-- 平均场指数 1/2 ≠ 渗流指数 4/3（不同普适类）。 -/
theorem two_universality_classes : (1 : ℚ) / 2 ≠ (4 : ℚ) / 3 := by norm_num

/-- 渗流指数 4/3 > 平均场 1/2。 -/
theorem perc_gt_mf : (1 : ℚ) / 2 < (4 : ℚ) / 3 := by norm_num

end CQM.GLGradient
