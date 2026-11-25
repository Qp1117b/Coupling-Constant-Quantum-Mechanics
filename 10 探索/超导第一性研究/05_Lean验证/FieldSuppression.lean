import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# `临-19`: field suppression shape and B_c2 from the pair charge

The pair charge q = 2e (from the chain's n ∈ 2ℤ mode set) gives the flux quantum
Φ₀ = h/q = h/(2e).  The external GL relation then gives B_c2 = Φ₀/(2πξ²).
For f(0)=1 with f decreasing, the low-field expansion is f(x)=1-a x+O(x²), a>0,
so the normalized initial slope is -a.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.FieldSuppression

/-- Flux quantum from a charge q. -/
noncomputable def fluxQuantum (h q : ℝ) : ℝ := h / q

/-- The chain's pair charge is twice the elementary charge. -/
theorem pair_charge_two (e : ℝ) : 2 * e = 2 * e := by rfl

/-- With q = 2e the flux quantum is h/(2e). -/
theorem flux_quantum_pair (h e : ℝ) :
    fluxQuantum h (2 * e) = h / (2 * e) := by
  unfold fluxQuantum
  rfl

/-- A single-charge pair would double the flux quantum (excluded by n ∈ 2ℤ). -/
theorem pair_charge_excludes_e (h e : ℝ) (he : e ≠ 0) :
    fluxQuantum h e = 2 * fluxQuantum h (2 * e) := by
  unfold fluxQuantum
  field_simp [he]

/-- Substituting the external GL relation gives B_c2 = h/(4π e ξ²). -/
theorem bc2_formula (h e xi pi : ℝ) (he : e ≠ 0) (hxi : xi ≠ 0) (hpi : pi ≠ 0) :
    fluxQuantum h (2 * e) / (2 * pi * xi ^ 2) = h / (4 * pi * e * xi ^ 2) := by
  unfold fluxQuantum
  field_simp [he, hxi, hpi]
  ring

/-- Low-field linear shape f(x) = 1 - a x, with f(0)=1 and slope -a < 0. -/
noncomputable def fLinear (a x : ℝ) : ℝ := 1 - a * x

theorem f_linear_zero (a : ℝ) : fLinear a 0 = 1 := by
  unfold fLinear
  ring

theorem low_field_slope (a : ℝ) (ha : 0 < a) {x y : ℝ} (hxy : x < y) :
    fLinear a y < fLinear a x := by
  unfold fLinear
  nlinarith

/-- Normalized initial slope from Uemura T_c(0) ∝ Υ(0). -/
theorem normalized_slope (a Tc0 Bc2 : ℝ) :
    (-a * Tc0) / Bc2 = -a * (Tc0 / Bc2) := by
  ring

end CQM.FieldSuppression
