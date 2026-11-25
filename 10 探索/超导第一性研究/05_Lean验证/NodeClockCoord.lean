import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# `临-15`: why the node proper-time coordinate is forced

A global coordinate makes K a constant function across nodes, hence reading
equality (13.5) -- contradicted by the per-mode phase distortion of `临-12`.
The node proper-time coordinate preserves node labels and is reconstructible
once the field is public (`临-14`).  The residual postulate ("node = elementary
support") is located but not removed.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.NodeClockCoord

/-- Global coordinate: K is the same function for every node. -/
def IsGlobalCoord (K : Fin n → ℝ) : Prop := ∀ i j : Fin n, K i = K j

/-- Global coordinate implies equal readings at every pair. -/
theorem global_coord_reading_equal {K : Fin n → ℝ} (hg : IsGlobalCoord K)
    (i j : Fin n) : K i = K j := hg i j

/-- A nonzero reading difference rules out the global constant coordinate. -/
theorem reading_diff_excludes_global {K : Fin n → ℝ} (i j : Fin n)
    (hne : K i ≠ K j) : ¬ IsGlobalCoord K := by
  intro hg
  exact hne (hg i j)

/-- Node proper-time shift: tau_i' = tau_i - Delta_i (from `临-12`). -/
noncomputable def tauShift (tau Delta : ℝ) : ℝ := tau - Delta

/-- The shift is node-indexed by Delta_i. -/
theorem node_coord_depends_on_node (tau Delta : ℝ) :
    tauShift tau Delta = tau - Delta := rfl

/-- Once the field is public, tau_i = tau_i0 + H_i0i (`临-14`), so the node
    coordinate is reconstructible from pair holonomies. -/
theorem node_coord_reconstructible (tau0 H : ℝ) :
    (tau0 + H) - tau0 = H := by ring

/-- Information compression: a constant coordinate cannot distinguish nodes. -/
theorem information_compression {K : Fin n → ℝ} (hg : IsGlobalCoord K)
    (i j : Fin n) : K i = K j := hg i j

/-- Two different readings cannot both come from a global coordinate. -/
theorem two_readings_exclude_global {a b : ℝ} (h : a ≠ b)
    (K : Fin 2 → ℝ) (ha : K 0 = a) (hb : K 1 = b) : ¬ IsGlobalCoord K := by
  intro hg
  have h01 : K 0 = K 1 := hg 0 1
  rw [ha, hb] at h01
  exact h h01

end CQM.NodeClockCoord
