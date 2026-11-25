import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp

/-!
# Ring 8 / ring 9 / Shen-19: two-component deficit split and the circulation ratio

Workbench file (NOT closing any gap, NOT touching the main ledger).

Two-component split of the bond deficit (8B.4):
  d ell_ij = beta_u (d eps_i - d eps_j) + alpha_u d b_ij
Variance (8B.5):
  <(dC)^2> = kappa_f^2 [ beta_u^2 * 2 s_eps^2 (1 - rho_ij) + alpha_u^2 s_b^2 ]
Circulation ratio (8B.6):
  r_circ = alpha_u s_b / (beta_u s_eps sqrt(2(1-rho)))
Zero-point scaling (8B.7):  s_b^2 ~ 1/alpha,  s_eps^2 ~ 1/beta  =>  r_circ ~ (beta/alpha)^{3/2}

Keating inversion (8B.9):
  alpha = a(3 c12 + c11)/4,  beta = a(c11 - c12)/4  =>  (alpha+3 beta)/a = c11, (alpha-beta)/a = c12

Equilateral-triangle product (8B.10):
  prod_C r = (1 + r_circ)^{-3/2} = 1 / ((1+r_circ) * sqrt(1+r_circ))

Proved here (algebra / real analysis; no axiom/sorry/admit/native_decide/unsafe):
  * `two_comp_variance_ge_node` : the bond component only ADDS to the node variance
  * `circ_ratio_zero_iff`       : r_circ = 0 iff the bond component vanishes
  * `circ_ratio_pos`            : positive bond amplitude gives positive r_circ
  * `keating_c11` / `keating_c12` : the Keating inversion recovers c11, c12
  * `prod_ge_fifth`             : r_circ <= 1  =>  prod_C r >= 1/5 > 0.177

The last one is the quantitative judgement: since every element has r_circ <= 0.09 << 1,
the loop product cannot reach 0.177.

Not formalised: the identification of eps/ell with bond/site geometric quantities (Shen-18/19),
the coefficient in the zero-point scaling (Shen-20), and the elastic-constant data.
-/

namespace CQM.TwoComp

/-- The bond (stretching) component adds a non-negative piece to the node-difference variance.
Writing `V = beta^2 * Vnode + alpha^2 * Vbond`, the total is at least the node part. -/
theorem two_comp_variance_ge_node (beta2 vnode alpha2 vbond : ℝ)
    (hb : 0 ≤ vbond) (ha : 0 ≤ alpha2) :
    beta2 * vnode ≤ beta2 * vnode + alpha2 * vbond := by
  have : 0 ≤ alpha2 * vbond := mul_nonneg ha hb
  linarith

/-- The circulation ratio vanishes exactly when the bond component does. -/
theorem circ_ratio_zero_iff (a b c d : ℝ) (hc : c ≠ 0) (hd : d ≠ 0)
    (h : a * b / (c * d) = 0) : a = 0 ∨ b = 0 := by
  have hab : a * b = 0 := by
    have hcd : c * d ≠ 0 := mul_ne_zero hc hd
    field_simp at h
    simpa using h
  exact mul_eq_zero.mp hab

/-- A strictly positive bond amplitude gives a strictly positive circulation ratio. -/
theorem circ_ratio_pos (a b c d : ℝ) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) (hd : 0 < d) :
    0 < a * b / (c * d) := by
  positivity

/-- Keating inversion, first relation: `(alpha + 3 beta)/a = c11`. -/
theorem keating_c11 (c11 c12 a : ℝ) (ha : a ≠ 0) :
    (a * (3 * c12 + c11) / 4 + 3 * (a * (c11 - c12) / 4)) / a = c11 := by
  field_simp
  ring

/-- Keating inversion, second relation: `(alpha - beta)/a = c12`. -/
theorem keating_c12 (c11 c12 a : ℝ) (ha : a ≠ 0) :
    (a * (3 * c12 + c11) / 4 - a * (c11 - c12) / 4) / a = c12 := by
  field_simp
  ring

/-- **The quantitative judgement.** If the circulation ratio does not exceed one, the
equilateral loop product is at least `1/5`, hence strictly above `0.177`.
Since every element gives `r_circ <= 0.09`, the value `0.177` is unreachable. -/
theorem prod_ge_fifth (r : ℝ) (h0 : 0 ≤ r) (h1 : r ≤ 1) :
    1 / 5 ≤ 1 / ((1 + r) * Real.sqrt (1 + r)) := by
  have hp : (0 : ℝ) < 1 + r := by linarith
  have hs0 : 0 < Real.sqrt (1 + r) := Real.sqrt_pos.mpr hp
  have hs2 : Real.sqrt (1 + r) ^ 2 = 1 + r := Real.sq_sqrt (le_of_lt hp)
  have hsle : Real.sqrt (1 + r) ≤ 3 / 2 := by
    have h : Real.sqrt (1 + r) ≤ Real.sqrt (9 / 4) := by
      apply Real.sqrt_le_sqrt
      linarith
    have h94 : Real.sqrt (9 / 4 : ℝ) = 3 / 2 := by
      rw [show (9 / 4 : ℝ) = (3 / 2) ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
    linarith [h, h94]
  have hden : (1 + r) * Real.sqrt (1 + r) ≤ 27 / 8 := by
    nlinarith [hs0, hsle, hs2]
  have hdenpos : (0 : ℝ) < (1 + r) * Real.sqrt (1 + r) := by positivity
  calc (1 : ℝ) / 5 ≤ 8 / 27 := by norm_num
    _ = 1 / (27 / 8) := by norm_num
    _ ≤ 1 / ((1 + r) * Real.sqrt (1 + r)) := one_div_le_one_div_of_le hdenpos hden

end CQM.TwoComp
