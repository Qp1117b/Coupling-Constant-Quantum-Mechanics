import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# FE03 CANDIDATE (NOT LANDED): full absolute Tc -- FE01 scale + mu* + moment choice
Core algebra: moment ratio e^{1/6}; mu* denominator positivity; Tc linear in
omega_ln; monotonicity of the Allen-Dynes exponent.  No axiom/sorry/admit/native_decide/unsafe.
-/

namespace CQM.FE03

/-- Moment ratio: omega_CQM/omega_Eliash = e^{-1/3}/e^{-1/2} = e^{1/6}. -/
theorem moment_ratio :
    Real.exp (-(1 / 3 : ℝ)) / Real.exp (-(1 / 2 : ℝ)) = Real.exp (1 / 6 : ℝ) := by
  rw [← Real.exp_sub]
  congr 1
  norm_num

/-- Tc is linear in omega_ln (prefactor): Tc(w1)/Tc(w2)=w1/w2 when exponent identical. -/
theorem tc_linear_in_omega (w1 w2 E : ℝ) (hE : E ≠ 0)
    (hw2 : w2 ≠ 0) :
    (w1 * E) / (w2 * E) = w1 / w2 := by
  field_simp [hE, hw2]

/-- CQM-moment Tc is e^{1/6} times Eliash-moment Tc (systematic 18.1% overestimate). -/
theorem tc_moment_bias (w E : ℝ) (hw : w ≠ 0) (hE : E ≠ 0) :
    ((Real.exp (-(1 / 3 : ℝ)) * w) * E) / ((Real.exp (-(1 / 2 : ℝ)) * w) * E)
      = Real.exp (1 / 6 : ℝ) := by
  field_simp [hw, hE, Real.exp_ne_zero _]
  rw [← Real.exp_add]
  congr 1
  norm_num

/-- Allen-Dynes denominator positivity: lambda - mu*(1+0.62 lambda) > 0
    when mu* < lambda/(1+0.62 lambda) and lambda>0. -/
theorem ad_denom_pos (lam ms : ℝ) (hlam : 0 < lam)
    (hms : ms < lam / (1 + 0.62 * lam)) :
    0 < lam - ms * (1 + 0.62 * lam) := by
  have hb : 0 < 1 + 0.62 * lam := by positivity
  rw [lt_div_iff₀ hb] at hms
  nlinarith

/-- AD exponent -1.04(1+lam)/denom is strictly decreasing in denom (denom>0):
    larger Coulomb pseudopotential (smaller denom) lowers Tc. -/
theorem ad_exp_monotone (lam den1 den2 : ℝ) (hlam : 0 < lam)
    (hd1 : 0 < den1) (hd2 : 0 < den2) (hlt : den1 < den2) :
    -1.04 * (1 + lam) / den1 < -1.04 * (1 + lam) / den2 := by
  have hnum : 0 < 1.04 * (1 + lam) := by positivity
  rw [div_lt_div_iff₀ hd1 hd2]
  nlinarith [mul_pos (sub_pos.mpr hlt) hnum]

end CQM.FE03
