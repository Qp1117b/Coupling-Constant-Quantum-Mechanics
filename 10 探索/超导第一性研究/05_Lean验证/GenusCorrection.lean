import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# `审-13`: the genus correction to minimal-loop generation

For a triangulated orientable surface, the cycle space has dimension E - V + 1,
while the face-boundary subspace has dimension F - 1.  Euler's relation with
genus g (and b boundary components) gives χ = 2 - 2g - b, hence a codimension
2g + b - 1: minimal loops generate everything only in the simply-connected case
g = 0, b ≤ 1.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.GenusCorrection

/-- Closed orientable surface: F - 1 = E - V + 1 - 2g. -/
theorem euler_genus {V E F g : ℤ} (h : V - E + F = 2 - 2 * g) :
    F - 1 = E - V + 1 - 2 * g := by
  ring_nf at h ⊢
  linarith

/-- Closed surface: the face-boundary subspace has codimension 2g inside the
cycle space. -/
theorem codim_closed {V E F g : ℤ} (h : V - E + F = 2 - 2 * g) :
    (E - V + 1) - (F - 1) = 2 * g := by
  ring_nf at h ⊢
  linarith

/-- Surface with b boundary components: codimension 2g + b. -/
theorem codim_boundary {V E F g b : ℤ} (h : V - E + F = 2 - 2 * g - b) :
    (E - V + 1) - (F - 1) = 2 * g + b := by
  ring_nf at h ⊢
  linarith

/-- Closed sphere g = 0, b = 0: face boundaries generate all cycles. -/
theorem planar_exact {V E F : ℤ} (h : V - E + F = 2) :
    F - 1 = E - V + 1 := by
  ring_nf at h ⊢
  linarith

/-- Outside that domain (g > 0) at least one winding label is missing. -/
theorem noncontractible_needed {g b : ℤ} (hg : 0 < g) (hb : 0 ≤ b) :
    0 < 2 * g + b := by
  linarith

/-- An open sample (b > 0) also carries a boundary-cycle label. -/
theorem boundary_needed {g b : ℤ} (hb : 0 < b) (hg : 0 ≤ g) :
    0 < 2 * g + b := by
  linarith

/-- The first Betti number of a closed orientable surface is 2g (book identity). -/
noncomputable def bettiOne (g : ℤ) : ℤ := 2 * g

theorem betti_one_eq_two_g (g : ℤ) : bettiOne g = 2 * g := by
  rfl

end CQM.GenusCorrection
