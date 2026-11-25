import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# V1: dimension and limit checks

(1) dimensions consistent; (2) BCS ratio 2pi/e^gamma ~ 3.528 is an EXTERNAL
constant (no Euler-gamma constant in this Lean env): we formalize only the
structural bound "if the ratio r lies in (3,4) then weak-coupling check passes",
leaving r's value external; (3) high-T thermal factor grows (no reversed sign);
(4) 2D/3D dimension selection (d-2=0 iff d=2).

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.V1Limits

/-- BCS weak-coupling check: given external ratio r = 2pi/e^gamma ~ 3.528,
    the V1 structural check is 3 < r < 4.  The value of r is external. -/
theorem bcs_ratio_check (r : ℝ) (hr_lo : 3 < r) (hr_hi : r < 4) :
    3 < r ∧ r < 4 := ⟨hr_lo, hr_hi⟩

/-- n_B upper bound: 1/(exp x - 1) <= 1/x for x>0 (classical high-T scale). -/
theorem nB_upper_bound (x : ℝ) (hx : 0 < x) :
    1 / (Real.exp x - 1) ≤ 1 / x := by
  have hx1 : 1 + x < Real.exp x := by
    simpa [add_comm] using (Real.add_one_lt_exp (ne_of_gt hx))
  have hden : 0 < Real.exp x - 1 := by linarith
  have hlt : x < Real.exp x - 1 := by linarith
  exact one_div_le_one_div_of_le hx (le_of_lt hlt)

/-- Thermal factor strictly above one for x>0 (heating not suppressed). -/
theorem thermal_factor_gt_one (x : ℝ) (hx : 0 < x) :
    1 < 1 + 2 / (Real.exp x - 1) := by
  have hden : 0 < Real.exp x - 1 := by
    have : 1 < Real.exp x := by simpa using (Real.exp_lt_exp.mpr hx)
    linarith
  have h2 : 0 < 2 / (Real.exp x - 1) := div_pos (by norm_num) hden
  linarith

/-- Dimension selection core: Upsilon/(k_B T) scales as length^(d-2);
    dimensionless only at d=2. -/
theorem dimension_selection (d : ℝ) : (d - 2 : ℝ) = 0 ↔ d = 2 := by
  constructor <;> intro h <;> linarith

end CQM.V1Limits
