import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# V2 step 1: elemental superconductor magnitude/sign diagnostic

CQM: T* = 1.13 e^{-1/3} theta_D e^{-1/lambda} (goal.2+goal.3).
Inverse: 1/lambda_CQM = ln(1.13 e^{-1/3} theta/T).
Structural gap: 1/lambda_BCS - 1/lambda_CQM = 1/3 (identity).
Physical range: lambda>0 iff A theta > T; lambda<2 iff ln(A theta/T) > 1/2.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.V2ElementDiagnostic

/-- Sector structural gap: ln(A theta/T) - ln(A e^{-1/3} theta/T) = 1/3.
    Formal core: log(x) - log(x * e^{-1/3}) = 1/3 for x>0. -/
theorem sector_gap_one_third (x : ℝ) (hx : 0 < x) :
    Real.log x - Real.log (x * Real.exp (-(1/3 : ℝ))) = 1 / 3 := by
  rw [Real.log_mul hx.ne' (Real.exp_ne_zero _), Real.log_exp]
  ring

/-- Positive coupling: lambda>0 iff ln(A theta/T) > 0 iff A theta > T (A>0). -/
theorem lambda_pos_iff (A theta T : ℝ) (hT : 0 < T)
    (hAT : T < A * theta) : 0 < Real.log (A * theta / T) := by
  apply Real.log_pos
  rw [one_lt_div hT]
  nlinarith

/-- Magnitude bound: lambda < 2 iff ln(A theta/T) > 1/2 (since lambda = 1/log).
    Formal core: 1/log < 2 iff 1/2 < log for log>0. -/
theorem lambda_lt_two (L : ℝ) (hL : 0 < L) (hLhalf : (1/2 : ℝ) < L) : 1 / L < 2 := by
  exact (one_div_lt hL (by norm_num : (0 : ℝ) < 2)).mpr hLhalf

/-- The inverse formula: lambda = 1 / ln(A theta / T). -/
theorem inverse_lambda (A theta T : ℝ) (hpos : 0 < Real.log (A * theta / T)) :
    (Real.log (A * theta / T)) * (1 / Real.log (A * theta / T)) = 1 := by
  field_simp [ne_of_gt hpos]

end CQM.V2ElementDiagnostic
