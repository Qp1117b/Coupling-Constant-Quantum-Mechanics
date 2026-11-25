import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# `审-1` matrix branch: geometric forcing and central-symmetric divergence

Formalises the algebraic core of `03_推导工作台/环07_审1矩阵分支几何强制.md`.

The chain's own BCC data gives triangle products of edge ratios different from one.
Since `λ_ij = ln r_ij`, a nonzero loop sum of `λ` rules out a gradient connection:
the matrix branch is forced, not optional.  On a centrosymmetric neighbour shell,
oddness of `f` alone makes the row sums of `B = f(λ)` vanish, so `C1 = 1` holds
without any explicit choice of `f`.  Two different odd functions (`x` and `x³`)
satisfy this, so `f` is not determined by `C1 = 1`.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.GeometricForcing

/-- If the product of edge ratios on a triangle differs from one, the sum of the
logarithmic edge connections cannot vanish.  This is the analytic core of the
geometric forcing of the matrix branch. -/
theorem loop_sum_ne_zero_of_product_ne_one {l1 l2 l3 r1 r2 r3 : ℝ}
    (hr1 : Real.exp l1 = r1) (hr2 : Real.exp l2 = r2) (hr3 : Real.exp l3 = r3)
    (hp : r1 * r2 * r3 ≠ 1) : l1 + l2 + l3 ≠ 0 := by
  intro hs
  apply hp
  have he : Real.exp (l1 + l2 + l3) = Real.exp 0 := by rw [hs]
  rw [Real.exp_add, Real.exp_add, hr1, hr2, hr3] at he
  simpa using he

/-- Converse form: a unit product forces a zero loop sum. -/
theorem loop_sum_zero_of_product_one {l1 l2 l3 r1 r2 r3 : ℝ}
    (hr1 : Real.exp l1 = r1) (hr2 : Real.exp l2 = r2) (hr3 : Real.exp l3 = r3)
    (hp : r1 * r2 * r3 = 1) : l1 + l2 + l3 = 0 := by
  apply Real.exp_injective
  rw [Real.exp_add, Real.exp_add, hr1, hr2, hr3]
  simpa using hp

/-- The triangle holonomy is invariant under a gauge shift `λ_ij ↦ λ_ij + χ_j - χ_i`. -/
theorem holonomy_gauge_invariant (l01 l12 l20 c0 c1 c2 : ℝ) :
    (l01 + (c1 - c0)) + (l12 + (c2 - c1)) + (l20 + (c0 - c2)) =
      l01 + l12 + l20 := by
  ring

/-- Oddness makes a pair of opposite edges cancel. -/
theorem odd_pair_cancel {f : ℝ → ℝ} (hf : ∀ x, f (-x) = -f x) (x : ℝ) :
    f x + f (-x) = 0 := by
  rw [hf x]
  ring

/-- A centrosymmetric four-neighbour shell has zero `f`-divergence for any odd `f`. -/
theorem center_symmetric_row_sum {f : ℝ → ℝ} (hf : ∀ x, f (-x) = -f x)
    (a b : ℝ) : f a + f (-a) + f b + f (-b) = 0 := by
  rw [hf a, hf b]
  ring

/-- On a three-cycle the two neighbours of a node carry opposite edge values. -/
theorem three_cycle_row_zero {f : ℝ → ℝ} (hf : ∀ x, f (-x) = -f x) (a : ℝ) :
    f a + f (-a) = 0 := by
  exact odd_pair_cancel hf a

/-! ## Two distinct odd functions give the same `C1 = 1` -/

/-- The linear odd function. -/
noncomputable def fLin (x : ℝ) : ℝ := x

/-- The cubic odd function. -/
noncomputable def fCub (x : ℝ) : ℝ := x ^ 3

theorem fLin_odd : ∀ x : ℝ, fLin (-x) = -fLin x := by
  intro x
  simp [fLin]

theorem fCub_odd : ∀ x : ℝ, fCub (-x) = -fCub x := by
  intro x
  unfold fCub
  ring

theorem fLin_row (a b : ℝ) :
    fLin a + fLin (-a) + fLin b + fLin (-b) = 0 := by
  exact center_symmetric_row_sum fLin_odd a b

theorem fCub_row (a b : ℝ) :
    fCub a + fCub (-a) + fCub b + fCub (-b) = 0 := by
  exact center_symmetric_row_sum fCub_odd a b

/-- The two admissible odd functions are genuinely different, so `C1 = 1` cannot
determine `f`. -/
theorem f_not_determined_by_row_sum : fLin 2 ≠ fCub 2 := by
  norm_num [fLin, fCub]

end CQM.GeometricForcing
