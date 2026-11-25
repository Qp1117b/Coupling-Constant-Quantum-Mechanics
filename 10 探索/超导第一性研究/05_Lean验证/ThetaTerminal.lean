import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# `D1`: the theta terminal T_theta

The per-zero phase-relaxation temperature is defined as
  T_{θ,n} = (ℏ/k_B) Γ_n = C · γ_n²       (C = ℏ σ_v² τ_g / k_B > 0).
Since γ_n increases, the minimum over modes is the first zero.  Uniformity of
all T_{θ,n} is equivalent to uniformity of the damping rates, which `临-22`
proved cannot be supplied by the physical side.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.ThetaTerminal

/-- Per-zero theta temperature, with C collecting the external constants. -/
noncomputable def thetaTemp (C g : ℝ) : ℝ := C * g ^ 2

/-- Damping is monotone in the squared ordinate. -/
theorem gamma_sq_monotone {g1 g2 : ℝ} (hg1 : 0 ≤ g1) (h : g1 ≤ g2) :
    g1 ^ 2 ≤ g2 ^ 2 := by
  nlinarith

/-- Positive C preserves the order of theta temperatures. -/
theorem theta_monotone {C g1 g2 : ℝ} (hC : 0 < C) (hg1 : 0 ≤ g1) (h : g1 ≤ g2) :
    thetaTemp C g1 ≤ thetaTemp C g2 := by
  unfold thetaTemp
  have hs := gamma_sq_monotone hg1 h
  nlinarith

/-- For the first three zeros (explicit positive increasing numbers) the minimum
is the first one. -/
theorem min_selects_first (C : ℝ) (hC : 0 < C) :
    thetaTemp C 14.134725141 ≤ thetaTemp C 21.022039639 ∧
    thetaTemp C 14.134725141 ≤ thetaTemp C 25.010857580 := by
  constructor
  · apply theta_monotone hC (by norm_num) (by norm_num)
  · apply theta_monotone hC (by norm_num) (by norm_num)

/-- Uniform theta temperatures iff uniform damping rates. -/
theorem uniform_iff_same_theta {C g1 g2 : ℝ} (hC : 0 < C) :
    thetaTemp C g1 = thetaTemp C g2 ↔ g1 ^ 2 = g2 ^ 2 := by
  unfold thetaTemp
  constructor
  · intro h
    exact (mul_left_cancel₀ (ne_of_gt hC) h)
  · intro h
    rw [h]

/-- Substituting τ_g = c / ω_D gives the algebraic scaling form. -/
theorem theta_scaling (hbar kB c omegaD sigma2 gamma C : ℝ)
    (hC : C = hbar * sigma2 * (c / omegaD) / kB) :
    thetaTemp C gamma = (hbar / kB) * gamma ^ 2 * sigma2 * (c / omegaD) := by
  rw [thetaTemp, hC]
  ring

end CQM.ThetaTerminal
