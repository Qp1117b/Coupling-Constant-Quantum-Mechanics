import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp

/-!
# Ring 8 / M5: the slope of `f` is fixed by DM.4's `kappa_f`

Workbench file (NOT closing any gap, NOT touching the main ledger).

Chain inputs:
  DM.4 : dC_ij = kappa_f (d eps_i - d eps_j) + O(d^2)      -- a FIRST-ORDER equality
  (5.2): lambda_ij = 1/2 ln(1 - ell_ij/(2 pi))  =>  dl/dell = -1/(4 pi) at ell = 0
  (8A.1): kappa_f = 1/(4 pi v_tau^2),  v_tau^2 = 1 - eps/(2 pi)

Writing `f(u) = c u + d u^3 + ...`, matching `dC = c dlambda` with `DM.4` gives
`c = -4 pi kappa_f = -1/v_tau^2`, i.e. `|f'(0)| = 1` in the flat background.

Proved here (algebra only, no axiom/sorry/admit/native_decide/unsafe):
  * `slope_from_first_order` : kappa*e = (-4 pi kappa) * (-(e/(4 pi)))
  * `kappa_identity`         : 4 pi v2 * (1/(4 pi v2)) = 1
  * `slope_unit_at_flat`     : -4 pi * (1/(4 pi)) = -1
  * `cubic_bound`            : |r| <= 10 and |u| <= 1/100  =>  |r| u^2 <= 1/1000

Not formalised: the identification `dell <-> (d eps_i - d eps_j)` (this is exactly
the index-layer question registered as `审-19`; the slope is the same under both
readings), the logarithmic expansion of `lambda(ell)`, and the physical size of `sigma_ell`.
-/

namespace CQM.FLope

/-- Two equivalent ways of writing the first-order relation: if `dC = kappa * e` and the
edge variable satisfies `lambda = -e/(4*pi)`, then `dC = (-4*pi*kappa) * lambda`.
This is the statement "the slope of `f` is `-4*pi*kappa`". -/
theorem slope_from_first_order (κ e : ℝ) :
    κ * e = (-4 * Real.pi * κ) * (-(e / (4 * Real.pi))) := by
  have h : (4 * Real.pi : ℝ) ≠ 0 := by positivity
  field_simp

/-- `4*pi*v2*kappa = 1` when `kappa = 1/(4*pi*v2)`: the identity behind "the matrix-branch
normalisation is `4*pi*v_tau^2*kappa_f = 1`" (`审-2`). -/
theorem kappa_identity (v2 : ℝ) (hv : v2 ≠ 0) :
    4 * Real.pi * v2 * (1 / (4 * Real.pi * v2)) = 1 := by
  have h : (4 * Real.pi * v2 : ℝ) ≠ 0 := by
    apply mul_ne_zero _ hv
    positivity
  field_simp

/-- In the flat background `kappa_f = 1/(4*pi)`, so the slope is exactly `-1`. -/
theorem slope_unit_at_flat :
    (-4 * Real.pi) * (1 / (4 * Real.pi)) = -1 := by
  have h : (4 * Real.pi : ℝ) ≠ 0 := by positivity
  field_simp

/-- The cubic coefficient is unobservable: for any ratio `r = d/c` bounded by 10 and any
`|u| <= 1/100`, the relative deviation `|r| u^2` is at most `1/1000`. -/
theorem cubic_bound (r u : ℝ) (hr : |r| ≤ 10) (hu : |u| ≤ 1 / 100) :
    |r| * u ^ 2 ≤ 1 / 1000 := by
  have hu2 : u ^ 2 ≤ 1 / 10000 := by
    have h := abs_le.mp hu
    nlinarith [h.1, h.2]
  calc
    |r| * u ^ 2 ≤ 10 * (1 / 10000) :=
      mul_le_mul hr hu2 (sq_nonneg u) (by norm_num)
    _ = 1 / 1000 := by norm_num

end CQM.FLope
