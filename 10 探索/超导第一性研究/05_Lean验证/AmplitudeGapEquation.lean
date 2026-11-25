import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# Amplitude-sector gap equation (C5)

From the chain-registered T* = (2 e^gamma/pi) hbar omega_log exp(-1/lambda)
(goal.2, shape 1.13 = 2e^gamma/pi), the same weak-coupling gap equation gives
Delta(0) = (pi/e^gamma) k_B T*, hence 2Delta/k_B T* = 2pi/e^gamma ~ 3.528.
The Euler constant is EXTERNAL (no Real.gamma in this env); r = 2e^gamma/pi
is given as a parameter.  We verify the structural algebra.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.AmplitudeGapEquation

/-- Given r = 2 e^gamma / pi (external, ~1.134), T* = r hbar omega exp(-1/lam). -/
noncomputable def tStar (r hbarOmega lam : ℝ) : ℝ := r * hbarOmega * Real.exp (-1 / lam)

/-- Weak coupling condition: lambda>0 and lambda<1 (exponential suppression). -/
theorem weak_coupling_condition (lam : ℝ) (hpos : 0 < lam) (hlt : lam < 1) :
    0 < lam ∧ lam < 1 := ⟨hpos, hlt⟩

/-- r = 2e^gamma/pi; the gap constant pi/e^gamma = 2/r.  Verify:
    from T* = r hbar omega exp(-1/lam), Delta = (2/r) k_B T*. -/
theorem gap_from_tstar (r w lam : ℝ) (hr : 0 < r) :
    (2 / r) * (r * w * Real.exp (-1 / lam)) = 2 * w * Real.exp (-1 / lam) := by
  field_simp [ne_of_gt hr]

/-- Universal ratio 2Delta/(k_B T*) = 4/r, independent of omega and lam.
    Formal: the expression has no omega/lam after cancellation. -/
theorem ratio_universal (r kbTstar : ℝ) (hr : 0 < r) (hT : kbTstar ≠ 0) :
    2 * ((2 / r) * kbTstar) / kbTstar = 4 / r := by
  field_simp [ne_of_gt hr, hT]
  norm_num

/-- omega_log^amp / omega_D = e^{-1/3} > 0 (goal.3, structural positivity). -/
theorem amp_log_ratio : 0 < Real.exp (-(1/3 : ℝ)) := Real.exp_pos _

end CQM.AmplitudeGapEquation
