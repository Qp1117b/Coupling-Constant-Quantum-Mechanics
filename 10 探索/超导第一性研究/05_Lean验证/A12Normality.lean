import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic.NoncommRing

/-!
# A12 normality

Matrix branch: `C = 1 + B`, `Bᵀ = -B`.  Any real skew-symmetric `B` is normal,
and adding the identity preserves normality.  Therefore `C` is normal for every
odd elementwise `f`, not only for the `C3circ`/`C4circ` examples.

This corrects the earlier working assumption that a generic matrix-branch `C`
would be non-normal and would need a Schur decomposition.
-/

open Matrix

namespace CQM

variable {n : Type*} [Fintype n]

/-- A real matrix is normal when it commutes with its transpose. -/
def Normal (A : Matrix n n ℝ) : Prop :=
  A * Aᵀ = Aᵀ * A

/-- A real skew-symmetric matrix is normal. -/
theorem skew_normal (B : Matrix n n ℝ) (hB : Bᵀ = -B) : Normal B := by
  unfold Normal
  rw [hB]
  noncomm_ring

variable [DecidableEq n]

/-- Adding the identity to a real skew-symmetric matrix preserves normality. -/
theorem skew_add_one_normal (B : Matrix n n ℝ) (hB : Bᵀ = -B) :
    Normal (1 + B) := by
  unfold Normal
  rw [Matrix.transpose_add, Matrix.transpose_one, hB]
  noncomm_ring

/-- The matrix branch `C = 1 + B` is normal whenever `B` is skew-symmetric. -/
theorem matrixBranch_normal (B : Matrix n n ℝ) (hB : Bᵀ = -B) :
    Normal (1 + B) :=
  skew_add_one_normal B hB

omit [Fintype n] [DecidableEq n] in
/-- An odd elementwise function of an antisymmetric edge matrix is skew-symmetric. -/
theorem odd_elementwise_skew {f : ℝ → ℝ} (hf : ∀ x, f (-x) = -f x)
    (lam : Matrix n n ℝ) (hlam : lamᵀ = -lam) :
    (fun i j => f (lam i j))ᵀ = -(fun i j => f (lam i j)) := by
  ext i j
  have h : lam j i = -lam i j := by
    simpa [Matrix.transpose] using congrFun (congrFun hlam i) j
  simp [h, hf]

/-- The full matrix branch with `B = f(λ)` and odd `f` is normal. -/
theorem matrixBranch_normal_of_odd {f : ℝ → ℝ} (hf : ∀ x, f (-x) = -f x)
    (lam : Matrix n n ℝ) (hlam : lamᵀ = -lam) :
    Normal ((1 : Matrix n n ℝ) + Matrix.of (fun i j => f (lam i j))) := by
  let B : Matrix n n ℝ := Matrix.of (fun i j => f (lam i j))
  have hB : Bᵀ = -B := by
    simpa [B, Matrix.of] using odd_elementwise_skew hf lam hlam
  simpa [B] using matrixBranch_normal B hB

end CQM
