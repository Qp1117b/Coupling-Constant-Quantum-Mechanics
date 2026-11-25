import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# `审-2`: the coupling κ_f from the FG interface

The FG interface `v_τ(ε) = sqrt(1 - ε/(2π))` and the ring-5 edge connection
`λ_ij = ln r_ij = φ(ε_j) - φ(ε_i)` with `φ = (1/2) ln(1 - ε/(2π))`
determine the linear coefficient of DM.5:

  κ_f(ε₀) = -φ'(ε₀) = 1 / (4π (1 - ε₀/(2π))).

At the zero-deficit anchor ε₀ = 0 this gives κ_f = 1/(4π), and the matrix-branch
linear scale becomes `c = v_τ² = 1 - ε₀/(2π)`, i.e. `c = 1` at the anchor.

Conditional on the FG interface (an assumption of the chain, gap E4).
No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.KappaF

/-- The logarithmic proper-time velocity φ(ε) = (1/2) ln(1 - ε/(2π)). -/
noncomputable def phi (e : ℝ) : ℝ := (1 / 2 : ℝ) * Real.log (1 - e / (2 * Real.pi))

/-- The squared FG velocity v_τ² = 1 - ε/(2π). -/
noncomputable def v2 (e : ℝ) : ℝ := 1 - e / (2 * Real.pi)

/-- Derivative of the logarithmic velocity. -/
theorem phi_deriv (e : ℝ) (hpos : 0 < v2 e) :
    deriv phi e = -1 / (4 * Real.pi * v2 e) := by
  have hinner : HasDerivAt (fun x : ℝ => 1 - x / (2 * Real.pi)) (-(1 / (2 * Real.pi))) e := by
    simpa using (hasDerivAt_const (x := e) (c := (1 : ℝ))).sub
      ((hasDerivAt_id e).div_const (2 * Real.pi))
  have hlog : HasDerivAt (fun x : ℝ => Real.log (1 - x / (2 * Real.pi)))
      ((1 / (1 - e / (2 * Real.pi))) * (-(1 / (2 * Real.pi)))) e := by
    simpa [v2] using (Real.hasDerivAt_log (ne_of_gt (by simpa [v2] using hpos))).comp e hinner
  have htot : HasDerivAt (fun x : ℝ => (1 / 2 : ℝ) * Real.log (1 - x / (2 * Real.pi))) _ e :=
    hlog.const_mul (1 / 2 : ℝ)
  unfold phi v2
  rw [htot.deriv]
  field_simp
  ring

/-- DM.5 coupling at a working point ε₀: the negative logarithmic response. -/
noncomputable def kappaF (e : ℝ) : ℝ := -deriv phi e

theorem kappaF_formula (e : ℝ) (hpos : 0 < v2 e) :
    kappaF e = 1 / (4 * Real.pi * v2 e) := by
  unfold kappaF
  rw [phi_deriv e hpos]
  ring

/-- At the zero-deficit anchor the coupling is 1/(4π). -/
theorem kappaF_at_zero : kappaF 0 = 1 / (4 * Real.pi) := by
  rw [kappaF_formula]
  · simp [v2]
  · simp [v2]

/-- Positivity on the physical branch. -/
theorem kappaF_pos (e : ℝ) (hpos : 0 < v2 e) : 0 < kappaF e := by
  rw [kappaF_formula e hpos]
  have hpi : 0 < 4 * Real.pi := by positivity
  exact one_div_pos.mpr (mul_pos hpi hpos)

/-- The matrix-branch linear scale c = κ_f / (-φ') = 4π v_τ² κ_f. -/
noncomputable def matrixScale (e : ℝ) (k : ℝ) : ℝ := k / (-deriv phi e)

theorem matrixScale_formula (e : ℝ) (k : ℝ) (hpos : 0 < v2 e) :
    matrixScale e k = 4 * Real.pi * v2 e * k := by
  unfold matrixScale
  rw [phi_deriv e hpos]
  field_simp [Real.pi_ne_zero, (ne_of_gt hpos)]

/-- With the geometric κ_f(ε) the matrix scale is identically one: the same
identification that fixes κ_f also fixes the normalization of `f`. -/
theorem matrixScale_eq_one {e : ℝ} (hpos : 0 < v2 e) :
    matrixScale e (kappaF e) = 1 := by
  rw [matrixScale_formula e (kappaF e) hpos, kappaF_formula e hpos]
  field_simp [Real.pi_ne_zero, (ne_of_gt hpos)]

/-- At the anchor the canonical normalization f(x) ≈ x is recovered. -/
theorem matrixScale_at_zero : matrixScale 0 (kappaF 0) = 1 := by
  have hpos : 0 < v2 0 := by simp [v2]
  exact matrixScale_eq_one hpos

end CQM.KappaF
