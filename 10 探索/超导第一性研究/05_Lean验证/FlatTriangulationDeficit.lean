import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp

/-!
# Ring 3 / Ring 5: flat triangulation forces the loop product to one

Workbench file (NOT closing any gap, NOT touching the main ledger).

Chain inputs:
  Ring 3 (3.1):  eps_ij = 2*pi - sum_T theta^T_ij     (3D Regge deficit, per bond)
  Ring 5 (5.2):  r_ij = sqrt(1 - ell_ij/(2*pi))
  06 line 139/944: BCC triangle loops give prod_C r in {0.177, 0.707, 0.500}

Geometric fact verified numerically in `环03_平直三角化亏角.py`
(BCC Delaunay disphenoid: 4 edges sqrt3/2, 2 edges 1):
  short edges (|e| = 1)      : dihedral = pi/2, exactly 4 tetrahedra around -> 2*pi
  long  edges (|e| = sqrt3/2): dihedral = 2*pi/3, exactly 3 tetrahedra around -> 2*pi
so every INTERIOR edge has eps = 2*pi - 2*pi = 0 exactly.

Consequences proved here (pure algebra / real analysis, no axiom/sorry/admit):
  * `bcc_short_edge_flat`  : 4 * (pi/2) = 2*pi        (flatness of the short edge)
  * `bcc_long_edge_flat`   : 3 * (2*pi/3) = 2*pi      (flatness of the long edge)
  * `deficit_vanishes_iff_ratio_one` : sqrt(1 - eps/(2pi)) = 1 <-> eps = 0
  * `flat_loop_product_one`          : all-flat loop -> product = 1
  * `ratio_strict_anti`              : larger deficit strictly lowers the bond ratio
  * `inverted_deficit`               : prod = p  ->  eps = 2*pi*(1 - p^(2/3))
  * `inverted_deficit_pos`           : 0 < p < 1 -> eps > 0

Not formalised: the combinatorial bookkeeping of which edges form a loop; the
dihedral-angle computation itself (numerical, in Python); the claim that no
*other* triangulation of BCC can raise eps to 4.30 rad (that is a geometric
statement about admissible star triangulations, discussed in the push-card).
-/

namespace CQM.FlatTri3

open Finset

/-- Short BCC Delaunay edges (|e| = 1) carry dihedral angle `pi/2` and are shared by
exactly four tetrahedra: the angular sum closes to `2*pi`, i.e. zero deficit. -/
theorem bcc_short_edge_flat : (4 : ℝ) * (Real.pi / 2) = 2 * Real.pi := by ring

/-- Long BCC Delaunay edges (|e| = sqrt3/2) carry dihedral angle `2*pi/3` and are shared
by exactly three tetrahedra: again `2*pi`, i.e. zero deficit. -/
theorem bcc_long_edge_flat : (3 : ℝ) * (2 * Real.pi / 3) = 2 * Real.pi := by ring

/-- Zero deficit gives unit bond ratio (and conversely, on the admissible branch). -/
theorem deficit_vanishes_iff_ratio_one (eps : ℝ) (h2 : 0 < 2 * Real.pi) :
    Real.sqrt (1 - eps / (2 * Real.pi)) = 1 ↔ eps = 0 := by
  rw [Real.sqrt_eq_one]
  constructor
  · intro h
    have : eps / (2 * Real.pi) = 0 := by linarith
    exact (div_eq_zero_iff.mp this).resolve_right (ne_of_gt h2)
  · intro h
    rw [h]
    norm_num

/-- A fully flat loop (every edge deficit zero) has product exactly one. -/
theorem flat_loop_product_one (n : ℕ) :
    (range n).prod (fun _ => Real.sqrt (1 - (0 : ℝ) / (2 * Real.pi))) = 1 := by
  induction n with
  | zero => simp
  | succ m ih =>
      rw [prod_range_succ, ih]
      rw [show (1 : ℝ) - 0 / (2 * Real.pi) = 1 by norm_num, Real.sqrt_one, mul_one]

/-- A larger deficit strictly lowers the bond ratio (so the loop product is strictly
decreasing in the uniform deficit). -/
theorem ratio_strict_anti (a b : ℝ) (hab : a < b) (hb : b < 2 * Real.pi) :
    Real.sqrt (1 - b / (2 * Real.pi)) < Real.sqrt (1 - a / (2 * Real.pi)) := by
  have hp : (0 : ℝ) < 2 * Real.pi := by positivity
  apply Real.sqrt_lt_sqrt
  · -- 0 ≤ 1 - b/(2π)
    have : b / (2 * Real.pi) < 1 := by
      rw [div_lt_one hp]; linarith
    linarith
  · -- 1 - b/(2π) < 1 - a/(2π)
    have : a / (2 * Real.pi) < b / (2 * Real.pi) := by
      exact div_lt_div_of_pos_right hab hp
    linarith

/-- Inversion for an equilateral three-edge loop: `p = (1 - eps/(2π))^(3/2)` implies
`eps = 2π (1 - p^(2/3))`. Stated with `Real.rpow`. -/
theorem inverted_deficit (p eps : ℝ) (heps : eps < 2 * Real.pi)
    (h : p = (1 - eps / (2 * Real.pi)) ^ (3 / 2 : ℝ)) :
    eps = 2 * Real.pi * (1 - p ^ (2 / 3 : ℝ)) := by
  have hp2 : (0 : ℝ) < 2 * Real.pi := by positivity
  have hbase : 0 < 1 - eps / (2 * Real.pi) := by
    have : eps / (2 * Real.pi) < 1 := by rw [div_lt_one hp2]; linarith
    linarith
  -- p^(2/3) = ((1 - e/2π)^(3/2))^(2/3) = 1 - e/2π
  have key : p ^ (2 / 3 : ℝ) = 1 - eps / (2 * Real.pi) := by
    rw [h]
    rw [← Real.rpow_mul (le_of_lt hbase)]
    norm_num
  rw [key]
  field_simp
  ring

/-- The inverted deficit is strictly positive for any `0 < p < 1`: a loop product below one
requires a genuinely positive background deficit. -/
theorem inverted_deficit_pos (p eps : ℝ) (h1 : p < 1)
    (heps : eps < 2 * Real.pi)
    (h : p = (1 - eps / (2 * Real.pi)) ^ (3 / 2 : ℝ)) : 0 < eps := by
  have hp2 : (0 : ℝ) < 2 * Real.pi := by positivity
  have hbase : 0 < 1 - eps / (2 * Real.pi) := by
    have : eps / (2 * Real.pi) < 1 := by rw [div_lt_one hp2]; linarith
    linarith
  -- if the base were >= 1 the power would be >= 1, contradicting p < 1
  have hb1 : 1 - eps / (2 * Real.pi) < 1 := by
    by_contra hc
    push Not at hc
    have hge : (1 : ℝ) ≤ (1 - eps / (2 * Real.pi)) ^ (3 / 2 : ℝ) :=
      Real.one_le_rpow hc (by norm_num)
    rw [← h] at hge
    linarith
  have hpos : 0 < eps / (2 * Real.pi) := by linarith
  rcases (div_pos_iff.mp hpos) with ⟨he, _⟩ | ⟨he, hc⟩
  · exact he
  · exfalso; linarith

end CQM.FlatTri3
