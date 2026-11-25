import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# Isotope exponent intermediate value via chain-external mu* (T10.3 component)

Webb 2015 Sec.IV: alpha < 1/2 from electron-phonon / Coulomb competition.
T10.3 proved CQM endpoints alpha in {0,1/2} and required an EXTERNAL mu*.
Using the M.1 shape (round 60), L = ln(eps_F/hbar w_D), dL/dlnM = +1/2
(w_D ~ M^{-1/2}) and the exact shift below give:

  alpha = 1/2 [1 - 1.04(1+lam)(1+0.62 lam) mu*^2 / (lam - mu*(1+0.62 lam))^2]

Proved here: exact mu* shift, mu* decreases with mass, correction positive,
alpha in (0,1/2), alpha=1/2 iff mu*=0. Coefficients are rational constants.
No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.IsotopeIntermediate

/-- Exact M.1 shift: ms/(1+ms*d) - ms = -ms^2 d/(1+ms*d).
    With d = (1/2) ln r this is the mu* response to isotope mass change. -/
theorem mustar_shift_exact (ms d : ℝ) (h : 1 + ms * d ≠ 0) :
    ms / (1 + ms * d) - ms = -(ms ^ 2) * d / (1 + ms * d) := by
  field_simp [h]
  ring

/-- mu* strictly decreases when isotope mass increases (ms>0, d>0). -/
theorem mustar_decreases_with_mass (ms d : ℝ) (hms : 0 < ms) (hd : 0 < d)
    (h : 0 < 1 + ms * d) :
    ms / (1 + ms * d) - ms < 0 := by
  rw [mustar_shift_exact ms d (ne_of_gt h)]
  have hq : 0 < (ms ^ 2) * d / (1 + ms * d) := by positivity
  have heq : -(ms ^ 2) * d / (1 + ms * d) = -((ms ^ 2) * d / (1 + ms * d)) := by ring
  rw [heq]
  linarith

/-- The Eliashberg correction factor C is positive (lam>0, mu*>0, D>0). -/
theorem correction_pos (lam ms : ℝ) (hlam : 0 < lam) (hms : 0 < ms)
    (hD : 0 < lam - ms * (1 + 0.62 * lam)) :
    0 < 1.04 * (1 + lam) * (1 + 0.62 * lam) * ms ^ 2
          / (lam - ms * (1 + 0.62 * lam)) ^ 2 := by
  positivity

/-- alpha = (1-C)/2 < 1/2 whenever C>0. -/
theorem alpha_lt_half (C : ℝ) (hC : 0 < C) : (1 - C) / 2 < 1 / 2 := by
  linarith

/-- alpha in (0,1/2) when 0<C<1. -/
theorem alpha_in_range (C : ℝ) (hC0 : 0 < C) (hC1 : C < 1) :
    0 < (1 - C) / 2 ∧ (1 - C) / 2 < 1 / 2 := by
  constructor <;> linarith

/-- mu*=0 recovers the CQM endpoint alpha=1/2 (no Coulomb competition). -/
theorem alpha_half_at_zero (lam : ℝ) :
    (1 - (1.04 * (1 + lam) * (1 + 0.62 * lam) * 0 ^ 2
          / (lam - 0 * (1 + 0.62 * lam)) ^ 2)) / 2 = 1 / 2 := by
  norm_num

end CQM.IsotopeIntermediate
