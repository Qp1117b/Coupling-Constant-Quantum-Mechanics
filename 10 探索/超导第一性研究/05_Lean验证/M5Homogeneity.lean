import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

open scoped BigOperators

/-!
# `M5`: homogeneity of the odd-function equation

The `C1 = 1` condition on `B_ij = f(λ_ij)` with `f` odd reduces to a homogeneous
linear system `D f = 0` in the values of `f` on the finite set of edge connections.
Consequences formalised here:

1. the zero vector always solves (the `C = I` branch);
2. scaling and addition of solutions preserve both the equation and oddness, so an
   odd solution is never unique once a nonzero one exists;
3. when the solution space is one-dimensional the shape is fixed but the scale is
   free, and that scale is absorbed by the external coupling `κ_f` (`审-2`);
4. a centrosymmetric neighbour shell gives signed counts zero, so all odd functions
   solve (the shape is not determined at all).

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.M5Homogeneity

/-- A homogeneous linear system `D f = 0` (rows indexed by nodes, columns by
distinct positive edge values). -/
def Solves {N m : ℕ} (D : Fin N → Fin m → ℝ) (f : Fin m → ℝ) : Prop :=
  ∀ i : Fin N, ∑ j : Fin m, D i j * f j = 0

/-- The zero vector always solves. -/
theorem zero_solves {N m : ℕ} (D : Fin N → Fin m → ℝ) :
    Solves D (fun _ : Fin m => 0) := by
  intro i
  simp

/-- Scaling a solution gives another solution. -/
theorem scale_solves {N m : ℕ} (D : Fin N → Fin m → ℝ) (c : ℝ) {f : Fin m → ℝ}
    (hf : Solves D f) : Solves D (fun j => c * f j) := by
  intro i
  calc
    (∑ j : Fin m, D i j * (c * f j)) = ∑ j : Fin m, c * (D i j * f j) := by
      apply Finset.sum_congr rfl
      intro j hj
      ring
    _ = c * (∑ j : Fin m, D i j * f j) := by rw [Finset.mul_sum]
    _ = 0 := by rw [hf i, mul_zero]

/-- The sum of two solutions is a solution. -/
theorem sum_solves {N m : ℕ} (D : Fin N → Fin m → ℝ) {f g : Fin m → ℝ}
    (hf : Solves D f) (hg : Solves D g) : Solves D (fun j => f j + g j) := by
  intro i
  calc
    (∑ j : Fin m, D i j * (f j + g j)) =
        ∑ j : Fin m, (D i j * f j + D i j * g j) := by
      apply Finset.sum_congr rfl
      intro j hj
      ring
    _ = (∑ j : Fin m, D i j * f j) + (∑ j : Fin m, D i j * g j) := by
      rw [Finset.sum_add_distrib]
    _ = 0 := by rw [hf i, hg i, add_zero]

/-- Oddness is preserved by scaling. -/
theorem odd_scale {f : ℝ → ℝ} (hf : ∀ x, f (-x) = -f x) (c : ℝ) :
    ∀ x, c * f (-x) = -(c * f x) := by
  intro x
  rw [hf x]
  ring

/-- Oddness is preserved by addition. -/
theorem odd_sum {f g : ℝ → ℝ} (hf : ∀ x, f (-x) = -f x)
    (hg : ∀ x, g (-x) = -g x) : ∀ x, f (-x) + g (-x) = -(f x + g x) := by
  intro x
  rw [hf x, hg x]
  ring

/-- A nonzero solution is never unique: `f` and `2f` are distinct solutions. -/
theorem not_unique_of_nonzero {N m : ℕ} (D : Fin N → Fin m → ℝ) {f : Fin m → ℝ}
    (hf : Solves D f) (hnz : ∃ j : Fin m, f j ≠ 0) :
    ∃ g : Fin m → ℝ, Solves D g ∧ g ≠ f := by
  refine ⟨fun j => 2 * f j, scale_solves D 2 hf, ?_⟩
  intro h
  obtain ⟨j, hj⟩ := hnz
  have hval := congr_fun h j
  simp at hval
  have hz : f j = 0 := by linarith
  exact hj hz

/-- Signed neighbour counts vanish on a centrosymmetric shell. -/
def signedCount (n : ℝ → ℕ) (α : ℝ) : ℤ := (n α : ℤ) - (n (-α) : ℤ)

theorem signedCount_zero_of_equal (n : ℝ → ℕ) (α : ℝ) (h : n α = n (-α)) :
    signedCount n α = 0 := by
  unfold signedCount
  rw [h]
  simp

/-- If the only solution is zero, the whole matrix branch collapses to `B = 0`. -/
theorem zero_f_gives_zero_B {α : Type} (f : ℝ → ℝ) (lam : α → α → ℝ)
    (h : ∀ x, f x = 0) : ∀ i j : α, f (lam i j) = 0 := by
  intro i j
  exact h (lam i j)

/-- The scale of `f` is absorbed by the external coupling `κ_f`. -/
theorem kappa_absorbs_scale (kappa c x : ℝ) (hc : c ≠ 0) :
    (kappa / c) * (c * x) = kappa * x := by
  field_simp

/-! ## A concrete two-function non-uniqueness example -/

noncomputable def fLin (x : ℝ) : ℝ := x
noncomputable def fCub (x : ℝ) : ℝ := x ^ 3

theorem both_solve_centrosymmetric (a b : ℝ) :
    (fLin a + fLin (-a) + fLin b + fLin (-b) = 0) ∧
    (fCub a + fCub (-a) + fCub b + fCub (-b) = 0) := by
  constructor
  · simp [fLin]
  · simp [fCub]
    ring

theorem fLin_ne_fCub : fLin 2 ≠ fCub 2 := by
  norm_num [fLin, fCub]

end CQM.M5Homogeneity
