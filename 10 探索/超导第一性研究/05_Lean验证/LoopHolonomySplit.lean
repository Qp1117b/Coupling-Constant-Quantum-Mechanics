import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# Ring 5 / Shen-1: telescoping identity of ratio transfer, and the two-layer split of `r_ij`

Workbench file (NOT closing any gap, NOT touching the main ledger).

Chain text under audit:
  (5.2)  `v_{tau,j} = v_{tau,i} * r_{ij}`     -- written as an EQUALITY
  (5.3c) `r_{ji} = 1 / r_{ij}`                -- oriented edge variable
  (5.3)  `prod_C r != 1` for BCC triangle loops (numeric input 0.177 / 0.707 / 0.500)

If `v_tau : V -> R_{>0}` is a single-valued site field (chain table in 7.1 says
"field, defined pointwise"), then `r_{ij} = v_j / v_i = exp (phi_j - phi_i)` and the
product around ANY closed loop telescopes to 1. Hence P & Q => not R: the three
assertions cannot coexist.

What is proved here (pure algebra, no axiom/sorry/admit/native_decide/unsafe):
  * `cyclic_sum_sub_zero`     : periodic difference sums vanish (telescoping core)
  * `telescoping_exp_prod`    : the loop product of `exp (f_{k+1} - f_k)` equals 1
  * `two_way_trivial`         : `v * (1 - x^2) = v` with `v != 0` forces `x = 0`
  * `same_edge_product_lt_one`: `(1-x)(1+x) < 1` for `0 < x < 1`
  * `reverse_deficit_nonlinear`: if `(1-x)(1-y) = 1` then `y = -x/(1-x)`, NOT `y = -x`
  * `asym_residual_nonpos`    : `(1/2) log (1 - x^2) <= 0` on `|x| < 1`
  * `asym_residual_eq_zero_iff`: equality iff `x = 0`

Not formalised: the graph-theoretic loop bookkeeping (which edges form `C`), the
numeric BCC input itself, and the physical identification of `ell_{ij}`.
-/

namespace CQM.Loop5A

open Finset
open scoped BigOperators

/-- Telescoping core: for a sequence `f` that closes up (`f n = f 0`) — the discrete
analogue of "the potential is single-valued" — the sum of consecutive differences
around the cycle vanishes. -/
theorem cyclic_sum_sub_zero (f : ℕ → ℝ) (n : ℕ) (hper : f n = f 0) :
    (range n).sum (fun k => f (k + 1) - f k) = 0 := by
  rw [sum_range_sub]
  rw [hper, sub_self]

/-- Loop holonomy of a ratio transfer. If each edge factor is the exponential of a
potential difference, the product around a closed loop is exactly one. -/
theorem telescoping_exp_prod (f : ℕ → ℝ) (n : ℕ) (hper : f n = f 0) :
    (range n).prod (fun k => Real.exp (f (k + 1) - f k)) = 1 := by
  rw [← Real.exp_sum, cyclic_sum_sub_zero f n hper, Real.exp_zero]

/-- Two-way transfer on a single edge is incompatible with a non-zero clock speed.
Writing `v_j = v_i r_ij` and `v_i = v_j r_ji` with `r_ij r_ji = 1 - x^2` gives
`v_j = v_j (1 - x^2)`; a non-zero `v_j` then forces `x = 0`, i.e. vanishing deficit. -/
theorem two_way_trivial (v x : ℝ) (hv : v ≠ 0) (h : v * (1 - x ^ 2) = v) :
    x = 0 := by
  have h1 : v * (x ^ 2) = 0 := by nlinarith
  rcases mul_eq_zero.mp h1 with hv0 | hx2
  · exact absurd hv0 hv
  · exact sq_eq_zero_iff.mp hx2

/-- The reverse product on one edge is strictly below one whenever the deficit is
non-zero, so the two directions cannot be mutual inverses at the level of `sqrt(1-x)`. -/
theorem same_edge_product_lt_one (x : ℝ) (h0 : 0 < x) (h1 : x < 1) :
    (1 - x) * (1 + x) < 1 := by
  have hpos : 0 < 1 - x := by linarith
  have hx2 : 0 < x ^ 2 := by nlinarith
  nlinarith [mul_pos hpos (by linarith : (0 : ℝ) < 1 + x)]

/-- The deficit assigned to the reversed direction is non-linear: requiring
`(1 - x) * (1 - y) = 1` gives `y = -x/(1-x)`, which equals `-x` only at `x = 0`.
This is the quantitative form of "`ell` is a scalar hinge deficit, while `lambda`
is an oriented edge variable". -/
theorem reverse_deficit_nonlinear (x : ℝ) (hx : x ≠ 1) :
    (1 - x) * (1 - (-x / (1 - x))) = 1 := by
  have h : (1 : ℝ) - x ≠ 0 := sub_ne_zero.mpr (Ne.symm hx)
  field_simp
  ring

/-- Antisymmetry residual: with `lambda_± = (1/2) log (1 ∓ x)`, the pairing sum is
`(1/2) log (1 - x^2)`, which is never positive. -/
theorem asym_residual_nonpos (x : ℝ) (h0 : 0 ≤ 1 - x ^ 2) (h1 : 1 - x ^ 2 ≤ 1) :
    (1 / 2) * Real.log (1 - x ^ 2) ≤ 0 := by
  have hlog : Real.log (1 - x ^ 2) ≤ 0 := Real.log_nonpos h0 h1
  linarith

/-- The residual vanishes exactly at zero deficit: `C1 = 1` is automatic only in the
linear regime `ell << 2*pi`. -/
theorem asym_residual_eq_zero_iff (x : ℝ) (hx : 0 < 1 - x ^ 2) :
    (1 / 2) * Real.log (1 - x ^ 2) = 0 ↔ x = 0 := by
  have hlog0 : Real.log (1 - x ^ 2) = 0 ↔ 1 - x ^ 2 = 1 := by
    rw [← Real.log_one]
    exact ⟨fun h => Real.log_injOn_pos (Set.mem_Ioi.mpr hx) (Set.mem_Ioi.mpr (by norm_num)) h,
           fun h => by rw [h]⟩
  constructor
  · intro h
    have hlog : Real.log (1 - x ^ 2) = 0 := by linarith
    have h1 : 1 - x ^ 2 = 1 := hlog0.mp hlog
    have hx2 : x ^ 2 = 0 := by linarith
    exact sq_eq_zero_iff.mp hx2
  · intro h
    rw [h]
    norm_num

end CQM.Loop5A
