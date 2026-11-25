/-
  预注册判定 R11：普适 gap 曲线的纯数骨架（A 类，链内 C5 隙方程）
  =================================================================
  本文件承载可严格证明的代数关系，数值积分由 R11 脚本完成：
    F0 = pi / e^gamma        （零温截距，C5 gap ratio 一半）
    sqrtF1 = pi sqrt(8/(7 zeta3))（近-Tc 斜率，由 gap ratio＋比热跳变导出）
    DeltaC = 12/(7 zeta3)   （比热跳变，第95轮）
  关键：a = 2/3 是代数恒等式 8/(7 zeta3) = (2/3) DeltaC，
        故 sqrtF1^2 = (2/3) DeltaC pi^2，Gross(1980) 的 a=2/3 非拟合参数。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

namespace CQM.UniversalGapCurve

noncomputable section

def eGamma : ℝ := 1.7810724179901979
def zeta3 : ℝ := 1.202056903159594
def F0 : ℝ := Real.pi / eGamma
def DeltaC : ℝ := 12 / (7 * zeta3)
def sqrtF1 : ℝ := Real.pi * Real.sqrt (8 / (7 * zeta3))

lemma eGamma_pos : 0 < eGamma := by unfold eGamma; norm_num
lemma zeta3_pos : 0 < zeta3 := by unfold zeta3; norm_num

/-- 零温截距两倍 = C5 gap ratio 2pi/e^gamma。 -/
lemma two_F0 : 2 * F0 = 2 * Real.pi / eGamma := by
  unfold F0
  ring

/-- Gross 系数 a=2/3 的来源：8/(7 zeta3) = (2/3) DeltaC（精确代数恒等式）。 -/
lemma gross_a_two_thirds : 8 / (7 * zeta3) = (2 / 3 : ℝ) * DeltaC := by
  unfold DeltaC
  ring

/-- 8/(7 zeta3) 非负（供 sqrt 平方用）。 -/
lemma eight_over_seven_zeta3_nonneg : 0 ≤ 8 / (7 * zeta3) := by
  apply div_nonneg
  · norm_num
  · exact mul_nonneg (by norm_num) (le_of_lt zeta3_pos)

/-- 近-Tc 斜率平方 = pi^2 * 8/(7 zeta3)。 -/
lemma sqrtF1_sq : sqrtF1 ^ 2 = Real.pi ^ 2 * (8 / (7 * zeta3)) := by
  unfold sqrtF1
  rw [mul_pow, Real.sq_sqrt eight_over_seven_zeta3_nonneg]

/-- 近-Tc 斜率平方 = (2/3) DeltaC pi^2（接比热跳变的链内纯数）。 -/
lemma sqrtF1_sq_via_deltaC : sqrtF1 ^ 2 = (2 / 3 : ℝ) * DeltaC * Real.pi ^ 2 := by
  rw [sqrtF1_sq, gross_a_two_thirds]
  ring

/-- 斜率与截距之比 = e^gamma * sqrt(8/(7 zeta3))（结构关系）。 -/
lemma slope_over_F0 : sqrtF1 / F0 = eGamma * Real.sqrt (8 / (7 * zeta3)) := by
  unfold sqrtF1 F0
  field_simp [eGamma_pos.ne']

/-- DeltaC 正性。 -/
lemma DeltaC_pos : 0 < DeltaC := by
  unfold DeltaC
  apply div_pos
  · norm_num
  · exact mul_pos (by norm_num) zeta3_pos

end
end CQM.UniversalGapCurve
