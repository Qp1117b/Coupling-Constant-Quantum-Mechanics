import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# BCS coefficient / omega_log convention check

BCS (Webb Eq.1): k_B T_c = 1.13 hbar omega_D exp(-1/lam) -- coefficient 1.13
with Debye CUTOFF.  McMillan (Eq.2): omega_log with coefficient 1/1.2.
CQM goal.2 uses 1.13 * omega_log = 1.13 * e^{-1/3} omega_D -- a mix, giving a
e^{-1/3} scale factor vs BCS.  KEY: the gap ratio 2Delta/(k_B T*) = 2pi/e^gamma
is INDEPENDENT of the prefactor frequency omega (shape vs scale).

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.BCSCoefficient

/-- Gap ratio: 2 Delta/(k_B T*) = 4/r where r=2e^gamma/pi, independent of the
    prefactor frequency omega.  Formal: the ratio expression has no omega. -/
theorem gap_ratio_independent_of_omega (r kbTstar : ℝ)
    (hr : 0 < r) (hT : kbTstar ≠ 0) :
    2 * ((2 / r) * kbTstar) / kbTstar = 4 / r := by
  field_simp [ne_of_gt hr, hT]
  norm_num

/-- Prefactor scale difference: BCS 1.13*omega_D vs CQM 1.13*e^{-1/3}*omega_D.
    CQM/BCS = e^{-1/3} (the scale factor). -/
theorem prefactor_scale_factor (wd : ℝ) (hwd : 0 < wd) :
    (1.13 * Real.exp (-(1/3 : ℝ)) * wd) / (1.13 * wd) = Real.exp (-(1/3 : ℝ)) := by
  field_simp [ne_of_gt hwd]

/-- e^{-1/3} < 1 (CQM prefactor smaller than BCS cutoff prefactor). -/
theorem scale_factor_lt_one : Real.exp (-(1/3 : ℝ)) < 1 := by
  exact Real.exp_lt_one_iff.mpr (by norm_num)

/-- The sector structure gap Delta(1/lam)=1/3 is unaffected by a constant
    prefactor change c: log(c A theta/T) - log(c A e^{-1/3} theta/T) = 1/3. -/
theorem sector_gap_prefactor_independent (c x : ℝ) (hc : 0 < c) (hx : 0 < x) :
    Real.log (c * x) - Real.log (c * x * Real.exp (-(1/3 : ℝ))) = 1 / 3 := by
  rw [Real.log_mul (mul_ne_zero hc.ne' hx.ne') (Real.exp_ne_zero _), Real.log_exp]
  ring

end CQM.BCSCoefficient
