/-
  环 8／49：闭环平均乘积判据的 3D 核统一——代数承载
  ===============================================================================
  R45 给 S_rho=1/6（3D 核）。闭环平均乘积
    <prod r> = exp[n sigma^2 (S_rho - 1) / (32 pi^2)]。
  S_rho-1 = -5/6 < 0 ⇒ 指数为负 ⇒ <prod r> < 1（恒）。
  第 83 轮"强正关联 S_rho>1 翻转 >1"分支链内不可达。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
  用 ℚ 代数承载符号（指数为负），不依赖 Real.exp API。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Data.Real.Basic

namespace CQM.LoopProduct

/-- R45 的 3D 关联和 S_rho = 1/6（代数值，来自 3D j0 核的精确求和）。 -/
def Srho3D : ℚ := (1 : ℚ) / 6

/-- S_rho - 1 = -5/6 < 0。 -/
theorem Srho_minus_one_neg : Srho3D - 1 = -(5 : ℚ) / 6 := by
  unfold Srho3D
  norm_num

theorem Srho_minus_one_lt_zero : Srho3D - 1 < 0 := by
  rw [Srho_minus_one_neg]
  norm_num

/-- S_rho = 1/6 ∈ (0,1)：既正又小于 1。 -/
theorem Srho_in_unit : 0 < Srho3D ∧ Srho3D < 1 := by
  unfold Srho3D
  constructor <;> norm_num

/-- 指数 E = n sigma^2 (S_rho-1)/(32 pi^2) 为负（n>0, sigma^2>0）。
    代数截面：忽略正分母 32pi^2，E 的符号 = n * sigma^2 * (S_rho-1) 的符号。 -/
theorem exponent_negative (n sigma2 : ℚ) (hn : 0 < n) (hs : 0 < sigma2) :
    n * sigma2 * (Srho3D - 1) < 0 := by
  rw [Srho_minus_one_neg]
  have hpos : 0 < n * sigma2 := mul_pos hn hs
  nlinarith

/-- 指数为负 ⇒ exp(E) < 1（用单调性：exp 严格增、exp(0)=1）。
    这里只承载"E<0"的代数核（Real.exp 单调性属外部数学，不在本文件形式化）。 -/
theorem product_lt_one_core (n sigma2 : ℚ) (hn : 0 < n) (hs : 0 < sigma2) :
    n * sigma2 * (Srho3D - 1) < 0 := exponent_negative n sigma2 hn hs

/-- 翻转分支需 S_rho > 1，但链内 S_rho=1/6 < 1 ⇒ 不可达。 -/
theorem flip_branch_unreachable (S_flip : ℚ) (hflip : S_flip > 1) :
    S_flip ≠ Srho3D := by
  unfold Srho3D
  intro h
  rw [h] at hflip
  norm_num at hflip

/-- 二阶对数偏移 -n sigma^2 / (16 pi^2) < 0（负定）。
    代数截面：-n*sigma^2 < 0。 -/
theorem log_offset_negative (n sigma2 : ℚ) (hn : 0 < n) (hs : 0 < sigma2) :
    -(n * sigma2) < 0 := by
  have hpos : 0 < n * sigma2 := mul_pos hn hs
  linarith

/-- 2D 与 3D 核的符号结论一致：都满足 S_rho - 1 < 0。
    2D：S_rho2D<0 ⇒ S_rho2D-1<0；3D：S_rho3D=1/6 ⇒ -5/6<0。 -/
theorem both_kernels_below_one (S2D : ℚ) (hS2 : S2D < 0) :
    S2D - 1 < 0 ∧ Srho3D - 1 < 0 := by
  constructor
  · linarith
  · exact Srho_minus_one_lt_zero

end CQM.LoopProduct
