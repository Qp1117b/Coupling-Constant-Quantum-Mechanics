import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# A12: global zero-sum does not imply `C 1 = 1`

`06 超导/CQM_超导核心理论.md` (DM.3) states the global constraint

`sum_{i ≠ j} C i j = 0`.

`10 探索/CQM_探索_推导链.md` (8.2) uses it to conclude the vector identity
`C 1 = 1` (each row sums to one).  That implication is false.  This file
gives a symmetric 3×3 counterexample with diagonal one and global off-diagonal
sum zero, but row sums `0, 3, 0`.

It is a formal counterexample only; it does not assert that this `C` is the
physical correlation matrix.
-/

namespace CQM.A12

noncomputable section

/-- Symmetric 3×3 matrix: diagonal 1, one pair of off-diagonal entries -2,
all other off-diagonal entries 1. -/
def Cex (i j : Fin 3) : ℝ :=
  match i.val, j.val with
  | 0, 0 => 1
  | 0, 1 => 1
  | 0, 2 => -2
  | 1, 0 => 1
  | 1, 1 => 1
  | 1, 2 => 1
  | 2, 0 => -2
  | 2, 1 => 1
  | 2, 2 => 1
  | _, _ => 0

theorem Cex_symm (i j : Fin 3) : Cex i j = Cex j i := by
  fin_cases i <;> fin_cases j <;> simp [Cex]

theorem Cex_diag (i : Fin 3) : Cex i i = 1 := by
  fin_cases i <;> simp [Cex]

theorem Cex_global_offdiag_zero :
    (∑ i : Fin 3, ∑ j : Fin 3, if i ≠ j then Cex i j else 0) = 0 := by
  simp (config := { decide := true }) [Cex, Fin.sum_univ_three]
  norm_num

theorem Cex_row_zero : (∑ j : Fin 3, Cex 0 j) = 0 := by
  norm_num [Cex, Fin.sum_univ_three]

theorem Cex_row_one : (∑ j : Fin 3, Cex 1 j) = 3 := by
  norm_num [Cex, Fin.sum_univ_three]

theorem Cex_not_row_sum_one :
    ¬ (∀ i : Fin 3, ∑ j : Fin 3, Cex i j = 1) := by
  intro h
  have h1 := h 1
  rw [Cex_row_one] at h1
  norm_num at h1

/-- The global A12 constraint holds, but `C 1 = 1` fails. -/
theorem A12_global_not_enough :
    (∑ i : Fin 3, ∑ j : Fin 3, if i ≠ j then Cex i j else 0) = 0 ∧
    ¬ (∀ i : Fin 3, ∑ j : Fin 3, Cex i j = 1) :=
  ⟨Cex_global_offdiag_zero, Cex_not_row_sum_one⟩

/-- A symmetric three-node matrix with diagonal one and row sums one is the identity. -/
theorem symmetric_row_diag_forces_identity_three
    (C : Fin 3 → Fin 3 → ℝ)
    (hsymm : ∀ i j : Fin 3, C i j = C j i)
    (hdiag : ∀ i : Fin 3, C i i = 1)
    (hrow : ∀ i : Fin 3, ∑ j : Fin 3, C i j = 1) :
    C 0 1 = 0 ∧ C 0 2 = 0 ∧ C 1 2 = 0 := by
  have h01 : C 0 1 + C 0 2 = 0 := by
    have h := hrow 0
    have h00 : C 0 0 = 1 := hdiag 0
    simp [Fin.sum_univ_three, h00] at h
    linarith
  have h10 : C 1 0 + C 1 2 = 0 := by
    have h := hrow 1
    have h11 : C 1 1 = 1 := hdiag 1
    simp [Fin.sum_univ_three, h11] at h
    linarith
  have h20 : C 2 0 + C 2 1 = 0 := by
    have h := hrow 2
    have h22 : C 2 2 = 1 := hdiag 2
    simp [Fin.sum_univ_three, h22] at h
    linarith
  have s01 : C 1 0 = C 0 1 := hsymm 1 0
  have s02 : C 2 0 = C 0 2 := hsymm 2 0
  have s12 : C 2 1 = C 1 2 := hsymm 2 1
  constructor
  · linarith
  constructor
  · linarith
  · linarith

/-- Per-row A12 on two nodes forces both off-diagonal entries to zero. -/
theorem per_row_A12_forces_zero_two
    (C : Fin 2 → Fin 2 → ℝ)
    (hrow : ∀ i : Fin 2, ∑ j : Fin 2, (if (i ≠ j) then C i j else (0 : ℝ)) = 0) :
    C 0 1 = 0 ∧ C 1 0 = 0 := by
  constructor
  · have h := hrow 0
    simpa [Fin.sum_univ_two] using h
  · have h := hrow 1
    simpa [Fin.sum_univ_two] using h

/-- A two-node matrix with diagonal one and row sums one is the identity. -/
theorem row_diag_forces_identity_two
    (C : Fin 2 → Fin 2 → ℝ)
    (hdiag : ∀ i : Fin 2, C i i = 1)
    (hrow : ∀ i : Fin 2, ∑ j : Fin 2, C i j = 1) :
    C 0 1 = 0 ∧ C 1 0 = 0 := by
  constructor
  · have h := hrow 0
    have h00 : C 0 0 = 1 := hdiag 0
    simpa [Fin.sum_univ_two, h00] using h
  · have h := hrow 1
    have h11 : C 1 1 = 1 := hdiag 1
    simpa [Fin.sum_univ_two, h11] using h

end

end CQM.A12
