import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

open scoped BigOperators

/-!
# `临-1`: geometric kinematics of the deficit angle

The deficit at a vertex is ε = 2π - Σ θ_k, so ε̇ = -Σ θ̇_k.  The law of cosines
gives θ̇ as a linear combination of edge-length rates with geometric coefficients.
If edge rates are driven by an external field (ℓ̇_e = d_e Ė), then ε̇ = χ Ė with
χ = -Σ d_k · (∂θ/∂ℓ): geometric factor times material piezoelectric coefficient.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.DeficitDrive

/-- Angle rate from the differentiated law of cosines. -/
noncomputable def thetaRate (a b c adot bdot cdot theta : ℝ) : ℝ :=
  (2 * c * cdot - 2 * a * adot - 2 * b * bdot
    + 2 * (adot * b + a * bdot) * Real.cos theta) /
    (2 * a * b * Real.sin theta)

/-- The rate satisfies the differentiated law of cosines (algebraic check). -/
theorem law_of_cosines_rate (a b c adot bdot cdot theta : ℝ)
    (ha : a ≠ 0) (hb : b ≠ 0) (hs : Real.sin theta ≠ 0) :
    2 * c * cdot = 2 * a * adot + 2 * b * bdot
      - 2 * (adot * b + a * bdot) * Real.cos theta
      + 2 * a * b * Real.sin theta * thetaRate a b c adot bdot cdot theta := by
  unfold thetaRate
  field_simp [ha, hb, hs]
  ring

/-- Deficit from face angles. -/
noncomputable def deficitOf (n : ℕ) (theta : Fin n → ℝ) : ℝ :=
  2 * Real.pi - ∑ k : Fin n, theta k

/-- Deficit rate is minus the sum of angle rates. -/
theorem deficit_rate (n : ℕ) (th dth : Fin n → ℝ) :
    deficitOf n th - deficitOf n (fun k => th k + dth k) = ∑ k : Fin n, dth k := by
  unfold deficitOf
  rw [Finset.sum_add_distrib]
  ring

/-- If every face angle increases, the deficit decreases. -/
theorem all_angles_up {n : ℕ} (thdot : Fin n → ℝ) (h : ∀ k, 0 < thdot k)
    (hn : 0 < n) : 0 < ∑ k : Fin n, thdot k := by
  haveI : Nonempty (Fin n) := ⟨⟨0, hn⟩⟩
  exact Finset.sum_pos (fun k _ => h k) Finset.univ_nonempty

theorem deficit_decreases {n : ℕ} (th dth : Fin n → ℝ) (h : ∀ k, 0 < dth k)
    (hn : 0 < n) :
    deficitOf n (fun k => th k + dth k) < deficitOf n th := by
  have hs : 0 < ∑ k : Fin n, dth k := all_angles_up dth h hn
  have hd := deficit_rate n th dth
  linarith

/-- If angle rates are linear in the field rate, so is the deficit rate. -/
theorem linear_in_drive {n : ℕ} (d : Fin n → ℝ) (Edot : ℝ) :
    (∑ k : Fin n, d k * Edot) = (∑ k : Fin n, d k) * Edot := by
  rw [Finset.sum_mul]

end CQM.DeficitDrive
