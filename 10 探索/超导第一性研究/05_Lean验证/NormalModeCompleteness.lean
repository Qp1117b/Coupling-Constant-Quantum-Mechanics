import Mathlib.Data.Real.Basic
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# `W-3′`: the deficit angle is not a complete coordinate of normal modes

For a closed triangulated sphere with V vertices, E = 3V - 6 edges, and the
linearised deficit map goes from R^E (edge-length perturbations) to R^V
(vertex deficits).  An injective linear map requires E ≤ V, which with
E = 3V - 6 forces V ≤ 3.  Hence for every V ≥ 4 the deficit map has a nontrivial
kernel of dimension at least E - V = 2V - 6.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.NormalModeCompleteness

/-- An injective linear map from R^n to R^m forces n ≤ m (rank-nullity). -/
theorem injective_implies_le {n m : ℕ} (f : (Fin n → ℝ) →ₗ[ℝ] (Fin m → ℝ))
    (hf : Function.Injective f) : n ≤ m := by
  have hr := LinearMap.finrank_range_of_inj (R := ℝ) hf
  have hle : Module.finrank ℝ (LinearMap.range f) ≤ Module.finrank ℝ (Fin m → ℝ) :=
    Submodule.finrank_le _
  simp at hr hle
  linarith

/-- Euler count for a closed triangulated sphere: 3F = 2E and V - E + F = 2
imply E = 3V - 6. -/
theorem euler_count {V E F : ℕ} (hfaces : 3 * F = 2 * E)
    (heuler : (V : ℤ) - E + F = 2) : (E : ℤ) = 3 * V - 6 := by
  have hf : (3 : ℤ) * F = 2 * E := by exact_mod_cast hfaces
  linarith

/-- The deficit map cannot be injective for V ≥ 4. -/
theorem deficit_not_complete {V E F : ℕ} (hV : 4 ≤ V)
    (hfaces : 3 * F = 2 * E) (heuler : (V : ℤ) - E + F = 2)
    (D : (Fin E → ℝ) →ₗ[ℝ] (Fin V → ℝ)) : ¬ Function.Injective D := by
  intro hinj
  have hle : E ≤ V := injective_implies_le D hinj
  have hE : (E : ℤ) = 3 * V - 6 := euler_count hfaces heuler
  have hleZ : (E : ℤ) ≤ V := by exact_mod_cast hle
  have hVZ : (4 : ℤ) ≤ V := by exact_mod_cast hV
  linarith

/-- Consequently a nonzero edge perturbation with zero deficit variation exists. -/
theorem kernel_nontrivial {V E F : ℕ} (hV : 4 ≤ V)
    (hfaces : 3 * F = 2 * E) (heuler : (V : ℤ) - E + F = 2)
    (D : (Fin E → ℝ) →ₗ[ℝ] (Fin V → ℝ)) :
    ∃ x : Fin E → ℝ, x ≠ 0 ∧ D x = 0 := by
  have hninj : ¬ Function.Injective D := deficit_not_complete hV hfaces heuler D
  have hker : D.ker ≠ ⊥ := by
    intro hbot
    exact hninj ((LinearMap.ker_eq_bot).mp hbot)
  rw [Submodule.ne_bot_iff] at hker
  obtain ⟨x, hxker, hxne⟩ := hker
  exact ⟨x, hxne, hxker⟩

/-- The dimension bound: E - V = 2V - 6 for a spherical triangulation. -/
theorem kernel_bound {V E : ℕ} (hE : (E : ℤ) = 3 * V - 6) :
    (E : ℤ) - V = 2 * V - 6 := by
  linarith

end CQM.NormalModeCompleteness
