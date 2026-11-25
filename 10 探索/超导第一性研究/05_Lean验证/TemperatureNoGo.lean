import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Data.Real.Basic

/-!
# R7: 环节⑨ 温度侧 no-go 的代数核

链唯一 T 入口 = coth（玻色），隙方程热核 = tanh（费米）。
以 a = exp(2x) > 1 参数化：coth=(a+1)/(a-1)、tanh=(a-1)/(a+1)。
证明 coth > 1 > tanh > 0、二者互倒数、永不相等；
以及 Matsubara 整数格与半整数格不交（2n ≠ 2m+1）。
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.TemperatureNoGo

noncomputable section

/-- a = exp(2x) > 1 时 coth > 1 且 0 < tanh < 1。 -/
theorem coth_gt_one_tanh_lt_one (a : ℝ) (ha : 1 < a) :
    1 < (a + 1) / (a - 1) ∧ 0 < (a - 1) / (a + 1) ∧ (a - 1) / (a + 1) < 1 := by
  have hden1 : 0 < a - 1 := by linarith
  have hden2 : 0 < a + 1 := by linarith
  constructor
  · rw [lt_div_iff₀ hden1]
    nlinarith
  constructor
  · exact div_pos hden1 hden2
  · rw [div_lt_iff₀ hden2]
    nlinarith

/-- coth 与 tanh 互倒数。 -/
theorem coth_tanh_reciprocal (a : ℝ) (ha : 1 < a) :
    ((a + 1) / (a - 1)) * ((a - 1) / (a + 1)) = 1 := by
  have h1 : a - 1 ≠ 0 := by linarith
  have h2 : a + 1 ≠ 0 := by linarith
  field_simp [h1, h2]

/-- 链热核 ≠ 隙方程热核：coth ≠ tanh 对一切 a>1 成立。 -/
theorem coth_ne_tanh (a : ℝ) (ha : 1 < a) :
    (a + 1) / (a - 1) ≠ (a - 1) / (a + 1) := by
  have h := coth_gt_one_tanh_lt_one a ha
  intro heq
  rw [heq] at h
  linarith [h.1, h.2.2]

/-- Matsubara 格点不交：整数倍 2n 不等于半整数 2m+1。 -/
theorem matsubara_grids_disjoint (n m : ℤ) : 2 * n ≠ 2 * m + 1 := by
  intro h
  omega

end
end CQM.TemperatureNoGo
