import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp

/-!
# Ring 8 / `M5` x `审-19`／`审-20`: the Keating lattice mismatch and the BCC VFF

Workbench file (NOT closing any gap, NOT touching the main ledger).

## 1. The formula used in rounds 79/80 is the DIAMOND Keating formula

(8B.9): `c11 = (al + 3 be)/a`, `c12 = (al - be)/a`, `c44 = 4 al be/(a (al + be))`.

That is the unique form satisfying the Keating identity
`2 c44 (c11 + c12) = (c11 - c12) (c11 + 3 c12)`, and it reproduces Si's
`c44 = 79.2 GPa` against `79.6 GPa` experiment (0.5%).  It is a tetrahedral
(4-coordinated) formula: its bond-bending equilibrium condition is
`cos theta = -1/3`.  BCC has 8 nearest neighbours with equilibrium angles
`{70.5, 109.5, 180}` degrees, so the tetrahedral condition is violated.
Applying (8B.9) to BCC metals is a lattice mismatch.

## 2. Correct BCC two-parameter VFF

Bond stretching `al`, bond bending `be` (angle form; `sin^2 theta0 = 8/9`
for the 24 non-antipodal pairs, antipodal pairs do not bend).  Exact
enumeration over the 8 `<111>` neighbours gives

  `c11 = (16 al / 9 + 128 be / 3) / a^3`
  `c12 = (16 al / 9 -  64 be / 3) / a^3`
  `c44 = 16 (al + 4 be) / (9 a^3)`

hence the falsifiable identity `c44 = (4 c11 + 5 c12)/9`.

It fails for every BCC metal (2.2x to 6.4x), and the model's Cauchy pressure
`c12 - c44` is negative while experiment has `c12 - c44 > 0`.  So the
two-parameter VFF is NOT a valid effective elasticity model for BCC metals:
`beta_u` is a phenomenological coefficient, not a VFF bond-bending stiffness.

## 3. The mismatch inflates `beta/alpha` by at least 9

  `(beta/alpha)_diamond = (c11 - c12)/(c11 + 3 c12)`
  `(beta/alpha)_bcc     = (c11 - c12)/(12 (c11 + 2 c12))`

For `c11 >= c12 > 0` the diamond value is at least 9 times the BCC value,
so `r_circ ~ (beta/alpha)^{1/4}` is inflated by at least `9^{1/4} = sqrt 3`.

## 4. Why the numbers still cannot be quoted

The `1/4` power makes `r_circ` insensitive: `beta/alpha` in `[1/16, 1]` gives
`r_circ` in `[1/2, 1]`.  The exact value needs the dynamical matrix (`审-20`).

## 5. `f'(0)` and the two readings of DM.4

`C = delta + f(lambda)`, `lambda = -ell/(4 pi) + ...`

  node reading  `dC = kappa (d eps_i - d eps_j)`  =>  `f'(0) = -4 pi kappa / beta_u`
  bond reading  `dC = kappa d ell`                =>  `f'(0) = -4 pi kappa`

The node reading is incompatible with a non-zero bond component (proved below:
`alpha_u != 0` forces `alpha_u = 0`), so the two-component split forces the
bond reading.  Under it round 78's `f'(0) = -4 pi kappa_f = -1/v_tau^2` survives.

Proved here (no axiom/sorry/admit/native_decide/unsafe):
  * `bcc_c44_identity`        : `9 c44 = 4 c11 + 5 c12` from the BCC coefficients
  * `bcc_beta_over_alpha`     : the BCC ratio
  * `diamond_beta_over_alpha` : the diamond ratio
  * `diamond_ge_nine_bcc`     : `c11 >= c12 > 0` => `9 * bcc <= diamond`
  * `quarter_mono`, `quarter_sixteenth`, `quarter_bounds` : the 1/4-power band
  * `node_reading_forces_alpha_zero` : the node reading kills the bond component
  * `slope_node`, `slope_bond` : the two readings of `f'(0)`
-/

namespace CQM.BCCVFF

/-! ### 2. The BCC elastic-constant identity -/

/-- **The falsifiable BCC identity.**  With the exact BCC coefficients of a
two-parameter valence-force field, the three elastic constants satisfy
`9 c44 = 4 c11 + 5 c12`.  This is the test that the diamond Keating formula
fails: for Nb it predicts `c44 = 183.8` against `28.7` GPa. -/
theorem bcc_c44_identity (c11 c12 c44 al be a : ℝ) (ha : a ≠ 0)
    (h11 : c11 = (16 * al / 9 + 128 * be / 3) / a ^ 3)
    (h12 : c12 = (16 * al / 9 - 64 * be / 3) / a ^ 3)
    (h44 : c44 = 16 * (al + 4 * be) / (9 * a ^ 3)) :
    9 * c44 = 4 * c11 + 5 * c12 := by
  have ha3 : a ^ 3 ≠ 0 := pow_ne_zero 3 ha
  rw [h11, h12, h44]
  field_simp
  ring

/-! ### 3. The two `beta/alpha` ratios -/

/-- Diamond (tetrahedral) Keating inversion gives `beta/alpha = (c11-c12)/(c11+3c12)`. -/
theorem diamond_beta_over_alpha (c11 c12 : ℝ) (h : c11 + 3 * c12 ≠ 0) :
    ((c11 - c12) / 4) / ((3 * c12 + c11) / 4) = (c11 - c12) / (c11 + 3 * c12) := by
  have h' : 3 * c12 + c11 ≠ 0 := by
    rw [add_comm]
    exact h
  field_simp
  ring

/-- BCC inversion gives `beta/alpha = (c11-c12)/(12 (c11+2c12))`. -/
theorem bcc_beta_over_alpha (c11 c12 : ℝ) (h : c11 + 2 * c12 ≠ 0) :
    ((c11 - c12) / 64) / (3 * (c11 + 2 * c12) / 16) =
      (c11 - c12) / (12 * (c11 + 2 * c12)) := by
  have h1 : (3 : ℝ) * (c11 + 2 * c12) / 16 ≠ 0 := by
    apply div_ne_zero
    · exact mul_ne_zero (by norm_num) h
    · norm_num
  field_simp
  ring

/-- **The lattice mismatch inflates `beta/alpha` by at least 9.**  For any
`c11 >= c12 > 0` the diamond ratio is at least nine times the BCC ratio, hence
`r_circ ~ (beta/alpha)^{1/4}` is inflated by at least `sqrt 3`. -/
theorem diamond_ge_nine_bcc (c11 c12 : ℝ) (h1 : 0 < c12) (h2 : c12 ≤ c11) :
    9 * ((c11 - c12) / (12 * (c11 + 2 * c12))) ≤ (c11 - c12) / (c11 + 3 * c12) := by
  have hA : 0 < c11 + 2 * c12 := by linarith
  have hB : 0 < c11 + 3 * c12 := by linarith
  rw [le_div_iff₀ hB]
  have h9 : 9 * ((c11 - c12) / (12 * (c11 + 2 * c12))) * (c11 + 3 * c12)
      = 9 * (c11 - c12) * (c11 + 3 * c12) / (12 * (c11 + 2 * c12)) := by ring
  have hA12 : 0 < 12 * (c11 + 2 * c12) := by linarith
  rw [h9, div_le_iff₀ hA12]
  nlinarith [h1, h2]

/-! ### 4. The `1/4` power band -/

/-- `t^(1/4)`, realised as `sqrt (sqrt t)` (equal for `t >= 0`). -/
noncomputable def quarter (t : ℝ) : ℝ := Real.sqrt (Real.sqrt t)

theorem quarter_nonneg (t : ℝ) : 0 ≤ quarter t := Real.sqrt_nonneg _

theorem quarter_mono {x y : ℝ} (h : x ≤ y) : quarter x ≤ quarter y := by
  unfold quarter
  exact Real.sqrt_le_sqrt (Real.sqrt_le_sqrt h)

theorem quarter_sixteenth : quarter (1 / 16) = 1 / 2 := by
  unfold quarter
  rw [show (1 / 16 : ℝ) = (1 / 4) ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  rw [show (1 / 4 : ℝ) = (1 / 2) ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]

theorem quarter_one : quarter 1 = 1 := by
  unfold quarter
  rw [Real.sqrt_one, Real.sqrt_one]

/-- **The 1/4-power insensitivity.**  A factor-16 spread in `beta/alpha`
gives only a factor-2 spread in `r_circ`. -/
theorem quarter_bounds {t : ℝ} (h1 : 1 / 16 ≤ t) (h2 : t ≤ 1) :
    1 / 2 ≤ quarter t ∧ quarter t ≤ 1 := by
  constructor
  · have h := quarter_mono h1
    rwa [quarter_sixteenth] at h
  · have h := quarter_mono h2
    rwa [quarter_one] at h

/-! ### 5. The two readings of DM.4 -/

/-- **The node reading kills the bond component.**  If `c (beta g + alpha b) = kappa g`
for every `g` and every `b`, and `c != 0`, then `alpha = 0`.  Hence a non-zero
`alpha_u` is incompatible with DM.4's node-difference form. -/
theorem node_reading_forces_alpha_zero (c kappa beta alpha : ℝ) (hc : c ≠ 0)
    (h : ∀ g b : ℝ, c * (beta * g + alpha * b) = kappa * g) : alpha = 0 := by
  have h1 : c * alpha = 0 := by
    have := h 0 1
    simpa using this
  exact (mul_eq_zero.mp h1).resolve_left hc

/-- Node reading: `f'(0) = -4 pi kappa / beta_u`, i.e. `f'(0) beta_u = -4 pi kappa`. -/
theorem slope_node (kappa beta c : ℝ) (hb : beta ≠ 0)
    (h : c = -(4 * Real.pi * kappa) / beta) :
    c * beta = -(4 * Real.pi * kappa) := by
  rw [h]
  field_simp

/-- Bond reading: `f'(0) = -4 pi kappa`, independent of `beta_u`. -/
theorem slope_bond (kappa c : ℝ) (h : c = -(4 * Real.pi * kappa)) :
    c = -(4 * Real.pi * kappa) := h

end CQM.BCCVFF
