import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Algebra.Order.BigOperators.Ring.Finset

/-!
# G19: phase tolerance, phase weight, and the linearisation coefficient

Formalises the algebraic core of `03_推导工作台/环06_G19容差标定.md`.

Three groups of facts:

1. `theta_lin` : the exact phase `θ = 2π s (1 - (1+λ)^2)` has linear part
   `-4π s λ` and remainder `-2π s λ^2`.  Hence the "α" of `θ = α λ` is not a
   free parameter but `α_lin = -4π s`.
2. `stiffness_scaling` : the harmonic stiffness in the phase variable is `α^2`
   times the stiffness in the log-ratio variable.
3. `tri_nonneg`, `tri_le_pi`, `tri_eq_self`, `fidelity_period`,
   `onset_shifts_with_fidelity`, `dead_zone` : a phase window is bounded by `π`
   on one period, reduces to the linear form only for `0 ≤ x ≤ π`, is `2π`
   periodic, and has no positive-temperature solution when the fidelity is
   non-positive.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.PhaseTolerance

/-! ## 1. Linearisation coefficient -/

/-- Exact phase minus the linear term: the coefficient of `λ` is `-4π s` and the
remainder is exactly `-2π s λ²`. -/
theorem theta_lin (s lam : ℝ) :
    2 * Real.pi * s * (1 - (1 + lam) ^ 2)
      = -4 * Real.pi * s * lam - 2 * Real.pi * s * lam ^ 2 := by
  ring

/-! ## 2. Stiffness scaling -/

/-- The phase stiffness is `α²` times the log-ratio stiffness. -/
theorem stiffness_scaling {n : Type*} [Fintype n] (a : ℝ) (x : n → ℝ) :
    (∑ i, ∑ j, (a * x i - a * x j) ^ 2)
      = a ^ 2 * (∑ i, ∑ j, (x i - x j) ^ 2) := by
  have h : ∀ i j : n, (a * x i - a * x j) ^ 2 = a ^ 2 * (x i - x j) ^ 2 := by
    intro i j
    ring
  simp only [h]
  rw [Finset.mul_sum]
  simp only [Finset.mul_sum]

/-! ## 3. Phase window on one period -/

/-- Triangle reading of the reduced holonomy on one period `[0, 2π]`. -/
noncomputable def tri (x : ℝ) : ℝ := if x ≤ Real.pi then x else 2 * Real.pi - x

/-- A phase window is non-negative. -/
theorem tri_nonneg {x : ℝ} (h0 : 0 ≤ x) (h2 : x ≤ 2 * Real.pi) : 0 ≤ tri x := by
  unfold tri
  split_ifs with h
  · exact h0
  · linarith

/-- A phase window is bounded by half a period, for every real reduced holonomy. -/
theorem tri_le_pi (x : ℝ) : tri x ≤ Real.pi := by
  unfold tri
  split_ifs with h
  · exact h
  · linarith

/-- On the first half period the triangle reading is the linear form, which is
the small-holonomy limit used in 06 §10.1. -/
theorem tri_eq_self {x : ℝ} (h : x ≤ Real.pi) : tri x = x := by
  unfold tri
  rw [if_pos h]

/-- The fidelity `cos W` is `2π` periodic: the phase window cannot be unbounded. -/
theorem fidelity_period (W : ℝ) : Real.cos (W + 2 * Real.pi) = Real.cos W := by
  rw [Real.cos_add, Real.cos_two_pi, Real.sin_two_pi]
  ring

/-! ## 4. Onset and dead zone -/

/-- At fixed temperature, a larger fidelity means the temperature lies inside the
closed region, i.e. the onset temperature is higher. -/
theorem onset_shifts_with_fidelity (A k T c₁ c₂ : ℝ) (hA : 0 < A)
    (hc : c₁ < c₂) (h₁ : A * c₁ = k * T) : A * c₂ > k * T := by
  nlinarith

/-- No positive-temperature solution when the phase factor is non-positive: the
holonomy is maximally frustrated. -/
theorem dead_zone (A k T c : ℝ) (hA : 0 < A) (hk : 0 < k) (hT : 0 < T) (hc : c ≤ 0) :
    A * c ≠ k * T := by
  have hAc : A * c ≤ 0 := mul_nonpos_of_nonneg_of_nonpos (le_of_lt hA) hc
  intro h
  nlinarith

end CQM.PhaseTolerance
