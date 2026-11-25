/-
  环 22／26／53：空间退相干 vs 时间退相干——代数承载
  ===============================================================================
  空间（临-17，高斯、静态）：R_n = exp(-gamma^2 sigma_a^2 / 2)
  时间（26.1b，指数、动态）：exp(-Gamma_n t), Gamma_n = gamma^2 sigma_v^2 tau_g
  截止 gamma_*^a = 1/sigma_a；gamma_*^v(t) = 1/sqrt(2 sigma_v^2 tau_g t)
  交叉 t_x = 1/(2 sigma_v^2 tau_g sigma_a^2)
  窗口 gamma_* = min(...)

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
  用 ℚ 代数承载指数（截面）与 min/交叉恒等式；sigma 等材料参数外生。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Data.Real.Basic

namespace CQM.TwoDecoh

/-- 空间退相干指数（高斯型截面）：gamma^2 sigma_a^2 / 2。 -/
def spatial_exp (gamma sa : ℚ) : ℚ := gamma^2 * sa^2 / 2

/-- 时间退相干指数（指数型截面）：gamma^2 sigma_v^2 tau_g t。 -/
def temporal_exp (gamma sv tg t : ℚ) : ℚ := gamma^2 * sv^2 * tg * t

/-- 两类退相干数学型不同（结构性）：空间指数在时间冻结后不含 t；时间指数含 t。
    截面：spatial_exp 无 t 参数，temporal_exp 对 t 线性。 -/
theorem different_types (gamma _sa sv tg : ℚ) (hg : gamma ≠ 0)
    (hsv : 0 < sv) (htg : 0 < tg) :
    temporal_exp gamma sv tg 1 < temporal_exp gamma sv tg 2 := by
  unfold temporal_exp
  have hpos : 0 < gamma^2 * sv^2 * tg := by positivity
  nlinarith

/-- 交叉时刻 t_x = sigma_a^2/(2 sigma_v^2 tau_g)（已回改：初稿误置 sa^2 于分母）。
    验证：2 sigma_v^2 tau_g t_x = sigma_a^2。 -/
theorem cross_time (sv tg sa : ℚ) (hsv : sv ≠ 0) (htg : tg ≠ 0) :
    2 * sv^2 * tg * (sa^2 / (2 * sv^2 * tg)) = sa^2 := by
  field_simp [hsv, htg]

/-- 窗口取小：gamma_* = min(spatial 截止, temporal 截止) ≤ 二者。 -/
theorem window_min (ga gt : ℚ) : min ga gt ≤ ga ∧ min ga gt ≤ gt := by
  constructor
  · exact min_le_left ga gt
  · exact min_le_right ga gt

/-- 短时 vs 长时主导：若 t < t_x 则时间截止 > 空间截止（空间主导）；
    截面用 gamma_*^a=1/sa、gamma_*^v=1/sqrt(2 sv^2 tg t) 的平方比较避免 sqrt：
    空间主导 ⇔ (1/sa)^2 < (1/(2 sv^2 tg t)) ⇔ 2 sv^2 tg t < sa^2 ⇔ t < t_x·sa^4? 
    用简化截面：直接以 gamma_*^v^2 = 1/(2 sv^2 tg t) 与 gamma_*^a^2 = 1/sa^2 比较。 -/
theorem short_time_spatial_dominates (sa sv tg t : ℚ)
    (hsa : 0 < sa) (hsv : 0 < sv) (htg : 0 < tg) (ht : 0 < t)
    (hlt : 2 * sv^2 * tg * t < sa^2) :
    (1 / sa^2 : ℚ) < 1 / (2 * sv^2 * tg * t) := by
  have hden1 : 0 < sa^2 := by positivity
  have hden2 : 0 < 2 * sv^2 * tg * t := by positivity
  field_simp [hden1.ne', hden2.ne']
  exact hlt

/-- 长时时间主导（截止更小）：时间截止平方 < 空间截止平方。 -/
theorem long_time_temporal_dominates (sa sv tg t : ℚ)
    (hsa : 0 < sa) (hsv : 0 < sv) (htg : 0 < tg) (ht : 0 < t)
    (hgt : sa^2 < 2 * sv^2 * tg * t) :
    (1 / (2 * sv^2 * tg * t) : ℚ) < 1 / sa^2 := by
  have hden1 : 0 < sa^2 := by positivity
  have hden2 : 0 < 2 * sv^2 * tg * t := by positivity
  field_simp [hden1.ne', hden2.ne']
  exact hgt

end CQM.TwoDecoh
