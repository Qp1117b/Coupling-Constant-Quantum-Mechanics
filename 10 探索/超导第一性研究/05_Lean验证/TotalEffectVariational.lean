/-
  环 25／51：总效应的变分原理——Hilbert 最小二乘投影（代数承载）
  ===============================================================================
  二次泛函 F[x] = ||x||^2 - 2 Re<x,k>。完全平方：
    F[x] = ||x-k||^2 - ||k||^2 >= -||k||^2，等号 iff x=k。
  故 k 是唯一极小元，极小值 -||k||^2 = -Xi（承 R50）。
  这是结构刻画（Hilbert 投影），非物理定律。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
  用 ℝ 的可加/有序域结构纯代数承载；Xi 为权威常数占位。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Data.Real.Basic

namespace CQM.TotalEffectVar

/-- 一维截面：F(x) = x^2 - 2*k*x（k 固定）。完全平方 F(x)=(x-k)^2 - k^2。 -/
def functional (x k : ℝ) : ℝ := x^2 - 2*k*x

theorem functional_complete_square (x k : ℝ) :
    functional x k = (x - k)^2 - k^2 := by
  unfold functional
  ring

/-- F(x) >= -k^2（因为 (x-k)^2 >= 0）。 -/
theorem functional_lower_bound (x k : ℝ) : functional x k ≥ -k^2 := by
  rw [functional_complete_square]
  nlinarith [sq_nonneg (x - k)]

/-- F(k) = -k^2（代入 x=k）。 -/
theorem functional_at_min (k : ℝ) : functional k k = -k^2 := by
  unfold functional
  ring

/-- 极小值 = -k^2。 -/
theorem minimum_value (k : ℝ) : functional k k = -k^2 := functional_at_min k

/-- 唯一极小元：若 F(x)=F(k)，则 x=k（因 (x-k)^2=0）。 -/
theorem unique_minimizer (x k : ℝ) (h : functional x k = functional k k) : x = k := by
  rw [functional_complete_square] at h
  rw [functional_at_min] at h
  have hs : (x - k)^2 = 0 := by linarith [sq_nonneg (x - k)]
  nlinarith [sq_eq_zero_iff.mp hs]

/-- 严格凸截面（一维）：x≠k ⇒ F(x)>F(k)。 -/
theorem strict_convex (x k : ℝ) (h : x ≠ k) : functional x k > functional k k := by
  rw [functional_complete_square, functional_at_min]
  have hs : (x - k)^2 > 0 := sq_pos_of_ne_zero (sub_ne_zero.mpr h)
  linarith

/-- Xi 权威常数占位（README 定义）。极小值 -k^2 在 k^2=Xi 时 = -Xi。 -/
def Xi : ℝ := 0.02309570897

theorem min_is_negative_Xi (k : ℝ) (hk : k^2 = Xi) : functional k k = -Xi := by
  rw [functional_at_min, hk]

/-- 守恒量 = |变分极小值|（R50 守恒 ↔ R51 变分的连接）。 -/
theorem conservation_variational_link (k : ℝ) :
    k^2 = |functional k k| := by
  rw [functional_at_min]
  rw [abs_of_nonpos]
  · ring
  · nlinarith [sq_nonneg k]

-- 边界注记（不形式化为伪定理，承 R28/R30 教训）：变分是 Hilbert 投影的
-- 结构刻画，"极小元存在"不蕴含"存在物理最小作用量原理"——此"不能推出"
-- 写在推导卡 §2.5，Lean 不强行为之构造形式证明。

end CQM.TotalEffectVar
