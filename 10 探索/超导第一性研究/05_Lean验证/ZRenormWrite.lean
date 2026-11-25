import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# Authorized revision: write Z=1+lambda into goal.2 (shape-neutral)

T* = 1.13 hbar omega_log exp(-(1+lam)/lam)  (goal.2')
Three cores: (1) 0.312 = e^{-7/6} = e^{-1}*e^{-1/6}; (2) gap ratio invariant
under Z (same factor cancels); (3) inverse lambda algebra for both exponents.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.ZRenormWrite

/-- 0.312 exact: e^{-7/6} = e^{-1} * e^{-1/6}. -/
theorem ratio_e_decomp :
    Real.exp (-(7 / 6 : ℝ)) = Real.exp (-(1 : ℝ)) * Real.exp (-(1 / 6 : ℝ)) := by
  rw [← Real.exp_add]
  congr 1
  norm_num

/-- Shape neutrality: if T* and Delta both scale by same positive z, gap ratio
    unchanged: 2*(z*Delta)/(z*T) = 2*Delta/T. -/
theorem shape_neutral (z d t : ℝ) (hz : z ≠ 0) (ht : t ≠ 0) :
    2 * (z * d) / (z * t) = 2 * d / t := by
  field_simp [hz, ht]

/-- The renormalized T* = e^{-1} times bare T* (same omega, same prefactor). -/
theorem tstar_renorm_factor (lam : ℝ) (hl : lam ≠ 0) :
    Real.exp (-(1 + lam) / lam) = Real.exp (-1) * Real.exp (-1 / lam) := by
  rw [← Real.exp_add]
  congr 1
  field_simp [hl]
  ring

/-- Inverse lambda for renormalized exponent: 1/lam = log(A theta/T) - 1.
    Core: from T = P * exp(-(1+lam)/lam), log(P/T) = (1+lam)/lam = 1/lam + 1. -/
theorem inverse_lambda_renorm (P T lam : ℝ) (hP : 0 < P) (hT : 0 < T)
    (hEq : T = P * Real.exp (-(1 + lam) / lam)) (hl : 0 < lam) :
    Real.log (P / T) = 1 / lam + 1 := by
  have hlog : Real.log T = Real.log P + (-(1 + lam) / lam) := by
    rw [hEq, Real.log_mul (ne_of_gt hP) (ne_of_gt (Real.exp_pos _)), Real.log_exp]
  rw [Real.log_div (ne_of_gt hP) (ne_of_gt hT)]
  rw [hlog]
  field_simp [ne_of_gt hl]
  ring

end CQM.ZRenormWrite
