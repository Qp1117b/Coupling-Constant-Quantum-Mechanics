import Mathlib.Analysis.Complex.Exponential
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-!
# `临-12`: zero-point shift of the memory kernel

Moving the integration lower limit t0 -> t0 + delta changes the node proper time
tau_i -> tau_i - Delta_i.  Substituting into (14.1)(14.2) gives a per-mode phase
factor exp(-i gamma_n Delta_i), i.e. a spectrum-dependent distortion, not a global
phase.  In the frozen case Delta_i = Delta_j the holonomy H_ij is unchanged while
the reading (phase reference) shifts.  Judgment-level quantities are zero-point
independent.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.ZeroPointShift

/-- Phase at a node: Phi = gamma * tau. -/
noncomputable def phase (gamma tau : ℝ) : ℝ := gamma * tau

/-- Shift of the proper time: tau' = tau - Delta. -/
noncomputable def tauShift (tau Delta : ℝ) : ℝ := tau - Delta

/-- Helper: exp(i(a+b)) = exp(ia) exp(ib) for real a b. -/
lemma exp_I_add (a b : ℝ) :
    Complex.exp (((a + b : ℝ) : ℂ) * Complex.I) =
      Complex.exp ((a : ℂ) * Complex.I) * Complex.exp ((b : ℂ) * Complex.I) := by
  rw [show (((a + b : ℝ) : ℂ) * Complex.I) = (a : ℂ) * Complex.I + (b : ℂ) * Complex.I by
    push_cast
    ring]
  exact Complex.exp_add _ _

/-- Phase under the shift: gamma*(tau-Delta) = gamma*tau - gamma*Delta. -/
theorem phase_shift (gamma tau Delta : ℝ) :
    phase gamma (tauShift tau Delta) = phase gamma tau - gamma * Delta := by
  unfold phase tauShift
  ring

/-- Per-mode factor: exp(i gamma (tau-Delta)) = exp(-i gamma Delta) exp(i gamma tau). -/
theorem mode_factor (gamma tau Delta : ℝ) :
    Complex.exp ((phase gamma (tauShift tau Delta) : ℝ) * Complex.I) =
      Complex.exp ((-(gamma * Delta) : ℝ) * Complex.I) *
        Complex.exp ((phase gamma tau : ℝ) * Complex.I) := by
  unfold phase tauShift
  rw [show gamma * (tau - Delta) = -(gamma * Delta) + gamma * tau by ring]
  exact exp_I_add (-(gamma * Delta)) (gamma * tau)

/-- General holonomy shift: H' = H - (Di - Dj). -/
theorem h_shift (tau_i tau_j Di Dj : ℝ) :
    (tau_i - Di) - (tau_j - Dj) = (tau_i - tau_j) - (Di - Dj) := by
  ring

/-- Frozen holonomy: equal shifts leave H_ij unchanged. -/
theorem frozen_h_invariant (tau_i tau_j D : ℝ) :
    (tau_i - D) - (tau_j - D) = tau_i - tau_j := by
  ring

/-- Two-point correlation: zero-point phase cancels, leaving the lag phase exp(i gamma (taup-tau)). -/
theorem corr_zero_point_free (gamma tau taup Delta : ℝ) :
    Complex.exp (((gamma * (tauShift taup Delta)) : ℝ) * Complex.I) *
        Complex.exp ((-(gamma * (tauShift tau Delta)) : ℝ) * Complex.I) =
      Complex.exp ((gamma * (taup - tau) : ℝ) * Complex.I) := by
  rw [← Complex.exp_add]
  apply congrArg Complex.exp
  unfold tauShift
  push_cast
  ring

/-- Frozen (14.2) difference carries the per-mode factor exp(-i gamma Delta).
    The weights 1/rho_n are common, so we isolate the algebraic exponential identity. -/
theorem diff_shift_frozen (gamma Phij H Del : ℝ) :
    Complex.exp (((Phij - gamma * Del) : ℝ) * Complex.I) *
        (Complex.exp ((gamma * H : ℝ) * Complex.I) - 1) =
      Complex.exp ((-(gamma * Del) : ℝ) * Complex.I) *
        (Complex.exp ((Phij : ℝ) * Complex.I) *
          (Complex.exp ((gamma * H : ℝ) * Complex.I) - 1)) := by
  rw [show (Phij - gamma * Del : ℝ) = -(gamma * Del) + Phij by ring]
  rw [exp_I_add]
  ring

/-- The modulus squared of the per-mode factor is one (residue spectrum unchanged). -/
theorem modulus_sq_one (gamma Delta : ℝ) :
    (Complex.exp ((-(gamma * Delta) : ℝ) * Complex.I)).re ^ 2 +
      (Complex.exp ((-(gamma * Delta) : ℝ) * Complex.I)).im ^ 2 = 1 := by
  rw [Complex.exp_re, Complex.exp_im]
  simp [Complex.ofReal_neg]

end CQM.ZeroPointShift
