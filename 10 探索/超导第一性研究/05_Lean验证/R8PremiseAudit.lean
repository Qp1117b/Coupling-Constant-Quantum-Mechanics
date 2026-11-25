import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Data.Real.Basic

/-!
# R40: R8 前提推广审计的代数核（隔离区）

审计：换用几何权重 q^k 后，第一档占比 = 1-q；要让对数 ln(1/(1-q)) 匹配
BCS 对数 ln(100)，需 q≈0.99 ⇒ 第一档占比≈0.01（权重极宽，与"第一档主导"矛盾）。
代数核：第一档占比 1-q 随 q 单调减、q→1 时 →0。
对数生成函数 sum q^k/k = -ln(1-q) 由外部标准数学保证，数值脚本核对。
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.R8PremiseAudit

noncomputable section

/-- 第一档归一占比 p1 = 1-q。 -/
def firstShare (q : ℝ) : ℝ := 1 - q

/-- q 增 ⇒ 第一档占比减（权重变宽）。 -/
theorem firstShare_decreasing (q1 q2 : ℝ) (h12 : q1 < q2) :
    firstShare q2 < firstShare q1 := by
  unfold firstShare
  linarith

/-- q∈(0,1) ⇒ 第一档占比∈(0,1)。 -/
theorem firstShare_range (q : ℝ) (hq0 : 0 < q) (hq1 : q < 1) :
    0 < firstShare q ∧ firstShare q < 1 := by
  unfold firstShare
  constructor <;> linarith

/-- 要匹配 BCS 对数 ln(100)≈4.6，需 1/(1-q)=100 ⇒ q=0.99 ⇒ 第一档占比 0.01。 -/
theorem match_bcs_log_share : firstShare (99 / 100 : ℝ) = 1 / 100 := by
  unfold firstShare
  norm_num

/-- 物理区 q≤1/2 时第一档占比 ≥1/2（第一档确实主导）。 -/
theorem first_dominant_in_physical_range (q : ℝ) (hq : q ≤ 1 / 2) :
    1 / 2 ≤ firstShare q := by
  unfold firstShare
  linarith

/-- 对比：q=0.99 的第一档占比 0.01 < 1/2 ⇒ 脱离第一档主导区。 -/
theorem broad_weight_not_dominant : firstShare (99 / 100 : ℝ) < 1 / 2 := by
  rw [match_bcs_log_share]
  norm_num

end
end CQM.R8PremiseAudit
