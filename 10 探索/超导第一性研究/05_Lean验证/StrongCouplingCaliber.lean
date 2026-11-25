/-
  预注册判定 R10：强耦合修正式的结构骨架（B 类，外部 Mitrović 式）
  =================================================================
  链内贡献只有弱耦合截距 R1 = 2 pi / e^gamma（C5）；修正项系数 12.5
  是外部 Eliashberg 拟合常数（不拟合）。本文件只承载可严格证明的
  结构关系：
    (1) R1 正性；
    (2) 修正项 12.5 x^2 ln(1/(2x)) 在 0<x<1/2 为正；
    (3) 强耦合修正使 gap ratio 严格大于弱耦合截距（R1 是下界）。
  数值与文献对照由 04_计算验证/R10_强耦合截距检验.py 完成。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

namespace CQM.StrongCouplingCaliber

noncomputable section

/-- 欧拉常数指数与链内弱耦合截距、外部拟合系数。 -/
def eGamma : ℝ := 1.7810724179901979
def R1 : ℝ := 2 * Real.pi / eGamma
def cMit : ℝ := 12.5

/-- 链内弱耦合截距正性。 -/
lemma R1_pos : 0 < R1 := by
  unfold R1 eGamma
  apply div_pos
  · positivity
  · norm_num

/-- 对数修正项在 0<x<1/2 为正：ln(1/(2x)) > 0。 -/
lemma log_term_pos {x : ℝ} (hx0 : 0 < x) (hx1 : 2 * x < 1) :
    0 < Real.log (1 / (2 * x)) := by
  apply Real.log_pos
  have h2x : 0 < 2 * x := by nlinarith
  rw [lt_div_iff₀ h2x]
  nlinarith

/-- 修正项 12.5 x^2 ln(1/(2x)) > 0（强耦合方向上扬）。 -/
lemma correction_pos {x : ℝ} (hx0 : 0 < x) (hx1 : 2 * x < 1) :
    0 < cMit * x ^ 2 * Real.log (1 / (2 * x)) := by
  unfold cMit
  have hx2 : 0 < x ^ 2 := sq_pos_of_ne_zero (by nlinarith)
  have hlog : 0 < Real.log (1 / (2 * x)) := log_term_pos hx0 hx1
  positivity

/-- 强耦合修正使 gap ratio 严格超过弱耦合截距：R1 是下界。 -/
lemma exceeds_R1 {x : ℝ} (hx0 : 0 < x) (hx1 : 2 * x < 1) :
    R1 < R1 * (1 + cMit * x ^ 2 * Real.log (1 / (2 * x))) := by
  have hc : 0 < cMit * x ^ 2 * Real.log (1 / (2 * x)) := correction_pos hx0 hx1
  have hprod : 0 < R1 * (cMit * x ^ 2 * Real.log (1 / (2 * x))) := mul_pos R1_pos hc
  nlinarith

end
end CQM.StrongCouplingCaliber
