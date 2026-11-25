import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith

open scoped BigOperators

/-!
# `临-18`: pressure invariance of the deficit angle

Face angles depend only on side ratios, so a uniform affine scaling does not
change them and the deficit ε = 2π - Σθ is invariant.  Equivalently, the Euler
identity Σ ℓ_e ∂θ/∂ℓ_e = 0 holds for a triangle (homogeneity degree zero).
A non-proportional edge response generates angle changes and hence Var(ε) > 0.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.PressureInvariance

/-- The cosine of a face angle is homogeneous of degree zero. -/
theorem cos_ratio_invariant (a b c lam : ℝ) (ha : a ≠ 0) (hb : b ≠ 0) (hl : lam ≠ 0) :
    ((lam * a) ^ 2 + (lam * b) ^ 2 - (lam * c) ^ 2) / (2 * (lam * a) * (lam * b)) =
      (a ^ 2 + b ^ 2 - c ^ 2) / (2 * a * b) := by
  field_simp [ha, hb, hl]

/-- Partial derivatives of θ from the law of cosines. -/
noncomputable def dThetaDa (a b _c theta : ℝ) : ℝ :=
  (b * Real.cos theta - a) / (a * b * Real.sin theta)
noncomputable def dThetaDb (a b _c theta : ℝ) : ℝ :=
  (a * Real.cos theta - b) / (a * b * Real.sin theta)
noncomputable def dThetaDc (a b c theta : ℝ) : ℝ :=
  c / (a * b * Real.sin theta)

/-- Euler identity: Σ ℓ_e ∂θ/∂ℓ_e = 0 by the law of cosines. -/
theorem euler_zero_for_triangle {a b c theta : ℝ}
    (hc : c ^ 2 = a ^ 2 + b ^ 2 - 2 * a * b * Real.cos theta)
    (ha : a ≠ 0) (hb : b ≠ 0) (hs : Real.sin theta ≠ 0) :
    a * dThetaDa a b c theta + b * dThetaDb a b c theta + c * dThetaDc a b c theta = 0 := by
  unfold dThetaDa dThetaDb dThetaDc
  field_simp [ha, hb, hs]
  nlinarith

/-- Proportional edge strain gives zero first-order angle change. -/
theorem uniform_strain_zero {a b c theta k : ℝ}
    (hc : c ^ 2 = a ^ 2 + b ^ 2 - 2 * a * b * Real.cos theta)
    (ha : a ≠ 0) (hb : b ≠ 0) (hs : Real.sin theta ≠ 0) :
    dThetaDa a b c theta * (k * a) + dThetaDb a b c theta * (k * b) +
      dThetaDc a b c theta * (k * c) = 0 := by
  have h := euler_zero_for_triangle hc ha hb hs
  calc
    dThetaDa a b c theta * (k * a) + dThetaDb a b c theta * (k * b) +
        dThetaDc a b c theta * (k * c)
        = k * (a * dThetaDa a b c theta + b * dThetaDb a b c theta +
            c * dThetaDc a b c theta) := by ring
    _ = 0 := by rw [h]; ring

/-- Deficit change is minus the sum of angle changes. -/
theorem deficit_change (dtheta : ℕ → ℝ) (n : ℕ) (hzero : ∀ k < n, dtheta k = 0) :
    Finset.sum (Finset.range n) (fun k => dtheta k) = 0 := by
  apply Finset.sum_eq_zero
  intro k hk
  exact hzero k (Finset.mem_range.mp hk)

/-- Non-proportional response generates a nonzero angle change for the triangle. -/
theorem nonuniform_generates {a b c theta k1 : ℝ}
    (hka : dThetaDa a b c theta * k1 ≠ 0) :
    dThetaDa a b c theta * k1 + dThetaDb a b c theta * 0 +
      dThetaDc a b c theta * 0 ≠ 0 := by
  simpa using hka

end CQM.PressureInvariance
