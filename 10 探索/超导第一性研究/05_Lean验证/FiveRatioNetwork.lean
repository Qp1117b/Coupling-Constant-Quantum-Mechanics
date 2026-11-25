/-
  预注册判定 R13：五纯数一致性网络（A 类，链内内部恒等式）
  =========================================================
  链内五个无参数纯数：
    R1 = 2 pi / e^gamma（gap ratio，C5）
    R2 = 12/(7 zeta3)（比热跳变，第95轮）
    R3 = 2 sqrt(pi)（临界场比，第89轮）
    R4 = 3/(4 e^{2gamma})（凝聚能比，第97轮）
    kappa = 2 sqrt(2) e^gamma / sqrt(7 zeta3)（临界场斜率，第102轮）
  核心恒等式：R4 * 2 * kappa^2 = R2（e^{2gamma} 精确消去）。
  两生成元：e^gamma 与 zeta3 —— 2 生成元普适类。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

namespace CQM.FiveRatioNetwork

noncomputable section

def eGamma : ℝ := 1.7810724179901979
def zeta3 : ℝ := 1.202056903159594

def R2 : ℝ := 12 / (7 * zeta3)
def R4 : ℝ := 3 / (4 * eGamma ^ 2)
def kappa : ℝ := 2 * Real.sqrt 2 * eGamma / Real.sqrt (7 * zeta3)

lemma eGamma_ne : eGamma ≠ 0 := by unfold eGamma; norm_num
lemma zeta3_ne : zeta3 ≠ 0 := by unfold zeta3; norm_num

/-- kappa^2 = 8 e^{2gamma}/(7 zeta3)。 -/
lemma kappa_sq : kappa ^ 2 = 8 * eGamma ^ 2 / (7 * zeta3) := by
  unfold kappa
  rw [div_pow, mul_pow, mul_pow, Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2),
      Real.sq_sqrt (mul_nonneg (by norm_num) (le_of_lt (by unfold zeta3; norm_num : (0:ℝ) < zeta3)))]
  ring

/-- 核心：R4 * 2 * kappa^2 = R2（e^{2gamma} 精确消去）。 -/
lemma five_ratio_identity : R4 * 2 * kappa ^ 2 = R2 := by
  rw [kappa_sq]
  unfold R4 R2
  field_simp [eGamma_ne, zeta3_ne]
  ring

/-- R3=2 sqrt(pi) 平方 = 4 pi（临界场比）。 -/
def R3 : ℝ := 2 * Real.sqrt Real.pi
lemma R3_sq : R3 ^ 2 = 4 * Real.pi := by
  unfold R3
  rw [mul_pow, Real.sq_sqrt (le_of_lt Real.pi_pos)]
  ring

/-- R1=2pi/e^gamma 与 R4 的积只含 zeta3 与 e^gamma 幂次（两生成元结构）。 -/
def R1 : ℝ := 2 * Real.pi / eGamma
lemma R1_over_R4 : R1 / R4 = 8 * Real.pi * eGamma / 3 := by
  unfold R1 R4
  field_simp [eGamma_ne]
  ring

end
end CQM.FiveRatioNetwork
