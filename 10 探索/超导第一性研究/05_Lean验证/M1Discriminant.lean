/-
  M1 判别子核对／60：零点相邻比数值一致性的代数核
  ===============================================================================
  主链第634行登记 gamma_{n+1}/gamma_1 = 1.4873/1.7695/2.1525（4位）。
  Python 用标准零点虚部核对到 6 位吻合。本文件用 ℚ 截面承载比值结构与
  "判别子 = 标准零点比"的核对逻辑（数值精确值在 Python）。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Data.Real.Basic

namespace CQM.M1Disc

/-- 比值 r = g2/g1 的截面（ℚ 近似到 4 位）。 -/
def ratio48 (g1 g2 : ℚ) : ℚ := g2 / g1

/-- 比值正定（零点虚部>0）。 -/
theorem ratio_pos (g1 g2 : ℚ) (hg1 : 0 < g1) (hg2 : 0 < g2) : 0 < ratio48 g1 g2 := by
  unfold ratio48
  positivity

/-- 比值 > 1（gamma_2 > gamma_1 ⇒ 比 > 1）。 -/
theorem ratio_gt_one (g1 g2 : ℚ) (hg1 : 0 < g1) (h : g1 < g2) : 1 < ratio48 g1 g2 := by
  unfold ratio48
  rw [one_lt_div hg1]
  exact h

/-- 判别子三比值互异（结构：三个不同零点给三个不同比）。 -/
theorem three_ratios_distinct (g1 g2 g3 g4 : ℚ)
    (_h12 : g1 < g2) (h23 : g2 < g3) (h34 : g3 < g4) (hg1 : 0 < g1) :
    ratio48 g1 g2 < ratio48 g1 g3 ∧ ratio48 g1 g3 < ratio48 g1 g4 := by
  unfold ratio48
  constructor
  · exact div_lt_div_of_pos_right h23 hg1
  · exact div_lt_div_of_pos_right h34 hg1

-- 边界注记（写文档，不构造伪形式化）：
-- 精确数值核对（4位吻合）在 Python；本文件只载比值结构与单调性。
-- 判别子数学正确性 ≠ M1 物理证实（后者需实验给出材料实际比值）。

end CQM.M1Disc
