/-
  预注册判定 R12：热力学临界场斜率纯数（A 类，严格热力学＋链内两纯数）
  =================================================================
    kappa = 2 sqrt(2) e^gamma / sqrt(7 zeta3) = 1.73666
  来源：链内 gap ratio (e^gamma) ＋ 比热跳变 (12/7 zeta3) ＋ Rutgers 公式。
  本文件承载代数恒等式；数值与 Al 实验对照由 R12 脚本完成。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

namespace CQM.CriticalFieldSlope

noncomputable section

def eGamma : ℝ := 1.7810724179901979
def zeta3 : ℝ := 1.202056903159594
def kappa : ℝ := 2 * Real.sqrt 2 * eGamma / Real.sqrt (7 * zeta3)
def beta : ℝ := (4 - kappa) / 2

lemma eGamma_pos : 0 < eGamma := by unfold eGamma; norm_num
lemma zeta3_pos : 0 < zeta3 := by unfold zeta3; norm_num
lemma seven_zeta3_nonneg : 0 ≤ 7 * zeta3 := by
  exact mul_nonneg (by norm_num) (le_of_lt zeta3_pos)

/-- kappa^2 = 8 e^{2gamma} / (7 zeta3)（精确代数恒等式）。 -/
lemma kappa_sq : kappa ^ 2 = 8 * eGamma ^ 2 / (7 * zeta3) := by
  unfold kappa
  rw [div_pow, mul_pow, mul_pow, Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2),
      Real.sq_sqrt seven_zeta3_nonneg]
  ring

/-- beta = 2 - kappa/2（Taylor 拟合参数与 kappa 的关系）。 -/
lemma beta_eq : beta = 2 - kappa / 2 := by
  unfold beta
  ring

/-- 两流体 kappa=2 被链内否定：kappa^2 = 8e^{2g}/(7 zeta3) < 4。 -/
lemma kappa_sq_lt_four : kappa ^ 2 < 4 := by
  rw [kappa_sq]
  -- 8 e^{2g}/(7 zeta3) < 4  <=> 2 e^{2g} < 7 zeta3
  have hden : 0 < 7 * zeta3 := mul_pos (by norm_num) zeta3_pos
  rw [div_lt_iff₀ hden]
  unfold eGamma zeta3
  norm_num

/-- 低温展开系数 e^{2gamma}/3（Molinari，Molinari BCS 讲义）。 -/
def lowTCoeff : ℝ := eGamma ^ 2 / 3
lemma lowTCoeff_gt_one : 1 < lowTCoeff := by
  unfold lowTCoeff eGamma
  norm_num

end
end CQM.CriticalFieldSlope
