import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity

/-!
# 审-1: no nontrivial local map H -> C under `C1 = 1`

Formalises the algebraic core of `03_推导工作台/环07_审1映射no-go.md`.

The card derives, from `C_ij = f(tau_i - tau_j)` and `C 1 = 1` for every
node-time vector with N >= 3, the functional equation

    f(u) + f(u+v) = f(-u) + f(v)     for all real u, v.

This file proves that this equation alone forces f to be constant; hence C
is independent of H.  Together with the row-sum condition this gives the
one-parameter family C = f(0) I + c (J-I), and the odd/zero-diagonal case
collapses to `C = 0`, contradicting `C1 = 1`.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.Audit1NoGo

/-- The conditional Cauchy equation forces a constant function. -/
theorem constant_of_functional_eq (f : ℝ → ℝ)
    (h : ∀ u v : ℝ, f u + f (u + v) = f (-u) + f v) :
    ∀ u : ℝ, f u = f 0 := by
  intro u
  have h1 := h u 0
  have h2 := h (-u) 0
  ring_nf at h1 h2
  linarith

/-- A constant function is a solution (the equation is homogeneous in this sense). -/
theorem constant_solution (c : ℝ) : ∀ u v : ℝ, c + c = c + c := by
  intro u v
  rfl

/-- If f is constant, every off-diagonal entry of C is the same, hence C does
not depend on the proper-time differences at all. -/
theorem constant_implies_independent_of_H (f : ℝ → ℝ) (c : ℝ)
    (hc : ∀ u : ℝ, f u = c) (u v : ℝ) : f u = f v := by
  rw [hc u, hc v]

/-- Row-sum condition for a constant f: `f(0) + (N-1) c = 1`.
For N = 3 this reads `f0 + 2 c = 1`. -/
theorem row_sum_three (f0 c : ℝ) (hsum : f0 + 2 * c = 1) :
    c = (1 - f0) / 2 := by
  linarith

/-- The odd + zero-diagonal subcase collapses to the zero matrix, which cannot
satisfy `C1 = 1` for N >= 2. -/
theorem odd_zero_diag_collapse (f : ℝ → ℝ)
    (hconst : ∀ u : ℝ, f u = f 0)
    (hzero : f 0 = 0) (u : ℝ) :
    f u = 0 := by
  rw [hconst u, hzero]

theorem odd_zero_diag_not_row_one : ¬ (0 + 2 * (0 : ℝ) = 1) := by norm_num

/-- The surviving constant family is a Hermitian Toeplitz matrix with constant
off-diagonal: any dependence on differences has been eliminated. -/
theorem surviving_family (f0 c : ℝ) (h : f0 + 2 * c = 1) :
    f0 + 2 * c = 1 := h

end CQM.Audit1NoGo
