import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-!
# R13: BKT 因子化数据核对的代数核

- 普适跳变：pi * (2T/pi) = 2T
- 因子化代回还原普适线
- Q <= 1 当 jump <= bare
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.BKTDataCheck

noncomputable section

open Real

/-- 普适跳变代数核：pi * (2 T / pi) = 2 T。 -/
theorem universal_jump (T : ℝ) : Real.pi * (2 * T / Real.pi) = 2 * T := by
  field_simp [ne_of_gt Real.pi_pos]

/-- 因子化代回：Q = jump/bare ⇒ (pi/2) bare Q = (pi/2) jump = T。 -/
theorem factorization_identity (T bare : ℝ) (hbare : bare ≠ 0) :
    (Real.pi / 2) * bare * ((2 * T / Real.pi) / bare) = T := by
  field_simp [hbare, ne_of_gt Real.pi_pos]

/-- Q <= 1 当 jump <= bare（跳变刚度不超过裸刚度）。 -/
theorem Q_le_one {jump bare : ℝ} (hbare : 0 < bare) (hjle : jump ≤ bare) :
    jump / bare ≤ 1 := by
  rw [div_le_iff₀ hbare]
  nlinarith

end
end CQM.BKTDataCheck
