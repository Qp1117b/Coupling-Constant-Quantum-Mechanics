import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# Forward gap ratio (first end-to-end verification, non-fitting)

Webb 2015 Eq6 (Mitrovic): 2Delta_0/(kB Tc) = 3.53[1 + 12.5 x^2 ln(1/(2x))],
x = Tc/omega_ln.  CQM supplies omega_log = e^{-1/3} theta_D (goal.3) with no
mu*.  Core algebra: x>0, correction >=0, ratio -> 3.53 as x->0.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.ForwardGapRatio

/-- Mitrovic correction factor is nonnegative for 0 < x < 1/2 (physical range):
    12.5 x^2 ln(1/(2x)) >= 0 iff ln(1/(2x)) >= 0 iff x <= 1/2. -/
theorem correction_nonneg (x : ℝ) (hx0 : 0 < x) (hx : x ≤ 1 / 2) :
    0 ≤ 12.5 * x ^ 2 * Real.log (1 / (2 * x)) := by
  have hlog : 0 ≤ Real.log (1 / (2 * x)) := by
    apply Real.log_nonneg
    rw [one_le_div (by positivity : (0 : ℝ) < 2 * x)]
    nlinarith
  nlinarith [sq_nonneg x]

/-- Gap ratio at weak coupling x->0 approaches 3.53 (structural: correction -> 0).
    Formal core: x^2 log(1/(2x)) -> 0 as x -> 0 needs analysis (external);
    we verify the factorized form and that the bracket >= 1. -/
theorem ratio_ge_bcs (x : ℝ) (hx0 : 0 < x) (hx : x ≤ 1 / 2) :
    3.53 ≤ 3.53 * (1 + 12.5 * x ^ 2 * Real.log (1 / (2 * x))) := by
  have hc := correction_nonneg x hx0 hx
  nlinarith

/-- x = Tc/omega_log with omega_log = e^{-1/3} theta_D (goal.3):
    x = Tc/(e^{-1/3} theta) = e^{1/3} Tc/theta.  Algebraic core. -/
theorem x_from_theta (tc theta : ℝ) (ht : 0 < theta) :
    tc / (Real.exp (-(1/3 : ℝ)) * theta) = Real.exp (1/3 : ℝ) * tc / theta := by
  field_simp [Real.exp_ne_zero _, ne_of_gt ht]
  have hexp : Real.exp (-(1/3 : ℝ)) * Real.exp (1/3 : ℝ) = 1 := by
    rw [← Real.exp_add]
    norm_num
  calc
    tc = tc * 1 := by ring
    _ = tc * (Real.exp (-(1/3 : ℝ)) * Real.exp (1/3 : ℝ)) := by rw [hexp]
    _ = tc * Real.exp (-(1/3 : ℝ)) * Real.exp (1/3 : ℝ) := by ring

/-- Log argument: 1/(2x) = omega_ln/(2 Tc) (Webb Eq6 argument). -/
theorem log_argument (x : ℝ) (hx : x ≠ 0) : 1 / (2 * x) = (1 / x) / 2 := by
  field_simp [hx]

end CQM.ForwardGapRatio
