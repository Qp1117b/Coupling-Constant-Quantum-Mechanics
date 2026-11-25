/-
  预注册判定 R16：临界场全程曲线的骨架（A 类贯通＋B 类工具）
  ==============================================================
  Hc(t)/Hc(0) = sqrt( ∫_t^1 [t'-S_es]dt' / ∫_0^1 [t'-S_es]dt' )
  分母 = R4 = 3/(4 e^{2gamma})（第89轮凝聚能＋R14 熵闭合）。
  两流体近似 1-t^2 全程高估（κ=2 vs 链内 κ=1.7367）。
  本文件承载代数骨架；全程积分盲测由 R16 脚本完成。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

namespace CQM.CriticalFieldCurve

noncomputable section

def eGamma : ℝ := 1.7810724179901979
def zeta3 : ℝ := 1.202056903159594
def R4 : ℝ := 3 / (4 * eGamma ^ 2)
def kappa : ℝ := 2 * Real.sqrt 2 * eGamma / Real.sqrt (7 * zeta3)

lemma eGamma_ne : eGamma ≠ 0 := by unfold eGamma; norm_num
lemma zeta3_pos : 0 < zeta3 := by unfold zeta3; norm_num

/-- 两流体 κ=2 被链内否定：kappa^2 < 4。 -/
lemma kappa_sq_lt_four : kappa ^ 2 < 4 := by
  unfold kappa
  rw [div_pow, mul_pow, mul_pow, Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2),
      Real.sq_sqrt (mul_nonneg (by norm_num) (le_of_lt zeta3_pos))]
  have hden : 0 < 7 * zeta3 := mul_pos (by norm_num) zeta3_pos
  rw [div_lt_iff₀ hden]
  unfold eGamma zeta3
  norm_num

/-- 凝聚能分母 R4 = 3/(4 e^{2gamma}) 正。 -/
lemma eGamma_pos : 0 < eGamma := by unfold eGamma; norm_num
lemma R4_pos : 0 < R4 := by
  unfold R4
  apply div_pos
  · norm_num
  · exact mul_pos (by norm_num) (pow_pos eGamma_pos 2)

/-- 近 Tc：Hc(t) ~ sqrt(2)(1-t)（由 kappa·(1-t)，kappa 有界）；
    两流体 1-t^2 ~ 2(1-t) 高估因子 2/kappa ≈ 1.15。 -/
def twofluid_over : ℝ := 2 / kappa
lemma twofluid_over_gt_one : 1 < twofluid_over := by
  unfold twofluid_over
  -- 2/kappa > 1 <=> 2 > kappa <=> 4 > kappa^2（已证）
  have hpos : 0 < kappa := by
    unfold kappa
    apply div_pos
    · exact mul_pos (mul_pos (by norm_num) (Real.sqrt_pos.2 (by norm_num))) eGamma_pos
    · exact Real.sqrt_pos.2 (mul_pos (by norm_num) zeta3_pos)
  rw [one_lt_div hpos]
  nlinarith [kappa_sq_lt_four, sq_nonneg (kappa - 2)]

end
end CQM.CriticalFieldCurve
