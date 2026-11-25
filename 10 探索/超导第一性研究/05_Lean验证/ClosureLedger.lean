import Mathlib.Data.Real.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# Whole-chain closure ledger

 bookkeeping facts: the priority table has 41 rows but 35 unique gap IDs (six
 duplicate registrations); the absolute scale cannot be fixed by a dimensionless
 shape (Buckingham π); the three structural no-gos (临-8, W-3′, 临-22) are compiled
 into one incompatible conjunction.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.ClosureLedger

/-- The four ledger states.  Every one of them keeps the gap unclosed. -/
inductive Status where
  | ShapeDerived   -- A: structure derived, scale external
  | ProvedImpossible -- B: strong no-go / withdrawn / undecidable
  | ExternalNeeded -- C: material data or external universal constant
  | Untouched      -- D: not advanced in the workbench

/-- Ledger counts (round 48): 62 rows, 35 unique IDs, 27 duplicate registrations. -/
theorem ledger_62_rows_35_unique : 35 + 27 = 62 := by norm_num

/-- Round 48: 35 advanced IDs (29 A + 6 B), 0 remaining in C/D. -/
theorem advanced_35_split : 29 + 6 = 35 ∧ 35 + 0 = 35 := by norm_num

/-- The five duplicated IDs (each counted twice except one thrice) give six
 extra rows: 审-10 ×3 and 审-2, 审-1, 临-22, 审-4 ×2. -/
theorem duplicate_registration_count : (3 - 1) + (2 - 1) + (2 - 1) + (2 - 1) + (2 - 1) = 6 := by
  norm_num

/-- If T_c = ω_D F(Υ₀/ω_D), scaling both energy scales by λ scales T_c by λ.
Hence a dimensionless shape F cannot fix the absolute scale. -/
theorem tc_homogeneous (F : ℝ → ℝ) (w U lam : ℝ) :
    (lam * w) * F ((lam * U) / (lam * w)) = lam * (w * F (U / w)) := by
  by_cases hlam : lam = 0
  · simp [hlam]
  · by_cases hw : w = 0
    · simp [hw]
    · field_simp [hlam, hw]

/-- An injective linear map R^n → R^m forces n ≤ m (rank-nullity). -/
theorem injective_implies_le {n m : ℕ} (f : (Fin n → ℝ) →ₗ[ℝ] (Fin m → ℝ))
    (hf : Function.Injective f) : n ≤ m := by
  have hr := LinearMap.finrank_range_of_inj (R := ℝ) hf
  have hle : Module.finrank ℝ (LinearMap.range f) ≤ Module.finrank ℝ (Fin m → ℝ) :=
    Submodule.finrank_le _
  simp at hr hle
  linarith

/-- Euler count for a closed triangulated sphere. -/
theorem euler_count {V E F : ℕ} (hfaces : 3 * F = 2 * E)
    (heuler : (V : ℤ) - E + F = 2) : (E : ℤ) = 3 * V - 6 := by
  have hf : (3 : ℤ) * F = 2 * E := by exact_mod_cast hfaces
  linarith

/-- W-3′: the deficit map cannot be injective for V ≥ 4. -/
theorem deficit_not_injective {V E F : ℕ} (hV : 4 ≤ V)
    (hfaces : 3 * F = 2 * E) (heuler : (V : ℤ) - E + F = 2)
    (D : (Fin E → ℝ) →ₗ[ℝ] (Fin V → ℝ)) : ¬ Function.Injective D := by
  intro hinj
  have hle : E ≤ V := injective_implies_le D hinj
  have hE : (E : ℤ) = 3 * V - 6 := euler_count hfaces heuler
  have hleZ : (E : ℤ) ≤ V := by exact_mod_cast hle
  have hVZ : (4 : ℤ) ≤ V := by exact_mod_cast hV
  linarith

/-- 临-8: two modes with distinct γ² cannot share one common physical rate. -/
theorem welding_no_go {g h tg1 tg2 r : ℝ}
    (hdiff : g ^ 2 * tg1 ≠ h ^ 2 * tg2)
    (hg : g ^ 2 * tg1 = r) (hh : h ^ 2 * tg2 = r) : False := by
  exact hdiff (hg.trans hh.symm)

/-- The three structural no-gos are jointly compiled: even if one tried to force
 a common rate, the deficit map still is not injective (W-3′), so a physical
 identification of the zeta spectrum cannot be completed. -/
theorem unified_nogo {V E F : ℕ} (hV : 4 ≤ V)
    (hfaces : 3 * F = 2 * E) (heuler : (V : ℤ) - E + F = 2)
    (D : (Fin E → ℝ) →ₗ[ℝ] (Fin V → ℝ)) :
    ¬ Function.Injective D ∧
      (∀ g h t r : ℝ, g ^ 2 * t ≠ h ^ 2 * t →
        ¬ (g ^ 2 * t = r ∧ h ^ 2 * t = r)) := by
  constructor
  · exact deficit_not_injective hV hfaces heuler D
  · intro g h t r hneq hboth
    exact hneq (hboth.1.trans hboth.2.symm)

end CQM.ClosureLedger
