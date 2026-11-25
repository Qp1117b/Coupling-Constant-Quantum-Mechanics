import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# M6: bond geometry of the Josephson amplitude

Formalises the algebraic core of `03_推导工作台/环10_M6键几何.md`.

The physical content is the split

  J_ij / J_0 = (1 - ρ_ij) cos θ_ij,

where `ρ` is the normalised zero-point deficit-angle correlation and `θ = s ℓ` is
the Regge holonomy phase.  Three groups of facts are proved:

1. the 3D Debye correlation `ρ₃(x) = 2(1 - cos x)/x²` lies in `[0,1]`;
2. the shape factor `(1 - ρ) cos θ` is bounded by one and keeps the sign of `cos θ`;
3. the saturation theorem: if `ρ(d) → 0`, then `1 - ρ(d) → 1`, so the variance-built
   coupling does not decay at large distance.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.BondGeometry

open Real

/-! ## 1. The 3D Debye correlation is bounded -/

/-- `2 (1 - cos x)` is non-negative. -/
theorem two_one_sub_cos_nonneg (x : ℝ) : 0 ≤ 2 * (1 - Real.cos x) := by
  have h := Real.cos_le_one x
  linarith

/-- `2 (1 - cos x) ≤ x²`, equivalently `1 - cos x ≤ x²/2`. -/
theorem two_one_sub_cos_le_sq (x : ℝ) : 2 * (1 - Real.cos x) ≤ x ^ 2 := by
  have h := Real.one_sub_sq_div_two_le_cos (x := x)
  nlinarith

/-- The 3D Debye correlation `ρ₃(x) = 2(1 - cos x)/x²` is non-negative. -/
theorem rho3d_nonneg {x : ℝ} (hx : x ≠ 0) : 0 ≤ 2 * (1 - Real.cos x) / x ^ 2 := by
  have h2 : 0 < x ^ 2 := by positivity
  exact div_nonneg (two_one_sub_cos_nonneg x) (le_of_lt h2)

/-- The 3D Debye correlation is at most one. -/
theorem rho3d_le_one {x : ℝ} (hx : x ≠ 0) : 2 * (1 - Real.cos x) / x ^ 2 ≤ 1 := by
  have h2 : 0 < x ^ 2 := by positivity
  rw [div_le_one h2]
  exact two_one_sub_cos_le_sq x

/-- The complementary shape factor `1 - ρ₃` in a single fraction. -/
theorem one_minus_rho3d {x : ℝ} (hx : x ≠ 0) :
    1 - 2 * (1 - Real.cos x) / x ^ 2 = (x ^ 2 - 2 + 2 * Real.cos x) / x ^ 2 := by
  field_simp
  ring

/-! ## 2. The shape factor -/

/-- The dimensionless bond shape factor `(1 - ρ) cos θ`. -/
noncomputable def Jshape (rho theta : ℝ) : ℝ := (1 - rho) * Real.cos theta

/-- With `0 ≤ ρ ≤ 1`, the shape factor is bounded by one in absolute value. -/
theorem Jshape_abs_le {rho theta : ℝ} (h0 : 0 ≤ rho) (h1 : rho ≤ 1) :
    |Jshape rho theta| ≤ 1 := by
  unfold Jshape
  have hc : |Real.cos theta| ≤ 1 := Real.abs_cos_le_one theta
  have hr : |1 - rho| ≤ 1 := by
    rw [abs_le]
    constructor <;> linarith
  calc |(1 - rho) * Real.cos theta| = |1 - rho| * |Real.cos theta| := abs_mul _ _
    _ ≤ 1 * 1 := by
      exact mul_le_mul hr hc (abs_nonneg _) (by norm_num)
    _ = 1 := by ring

/-- Below the uniform limit `ρ < 1` and with `cos θ > 0`, the coupling is positive. -/
theorem Jshape_pos {rho theta : ℝ} (h : rho < 1) (hc : 0 < Real.cos theta) :
    0 < Jshape rho theta := by
  unfold Jshape
  exact mul_pos (by linarith) hc

/-! ## 3. Saturation of the difference variance -/

/-- If the normalised correlation tends to zero, then the complementary factor
`1 - ρ` tends to one.  This is the algebraic core of the saturation theorem: the
variance-built coupling does not decay at large distance. -/
theorem saturates (rho : ℝ → ℝ)
    (h : ∀ ε > 0, ∃ R, ∀ d, R < d → |rho d| < ε) :
    ∀ ε > 0, ∃ R, ∀ d, R < d → |(1 - rho d) - 1| < ε := by
  intro ε hε
  obtain ⟨R, hR⟩ := h ε hε
  refine ⟨R, ?_⟩
  intro d hd
  have h' : |rho d| < ε := hR d hd
  have e : (1 - rho d) - 1 = -rho d := by ring
  rw [e, abs_neg]
  exact h'

/-- Strengthened form: if `ρ` tends to any limit `c`, then `1 - ρ` tends to `1 - c`.
No decay rate or monotonicity is needed. -/
theorem saturates_to (rho : ℝ → ℝ) (c : ℝ)
    (h : ∀ ε > 0, ∃ R, ∀ d, R < d → |rho d - c| < ε) :
    ∀ ε > 0, ∃ R, ∀ d, R < d → |(1 - rho d) - (1 - c)| < ε := by
  intro ε hε
  obtain ⟨R, hR⟩ := h ε hε
  refine ⟨R, ?_⟩
  intro d hd
  have h' : |rho d - c| < ε := hR d hd
  have e : (1 - rho d) - (1 - c) = -(rho d - c) := by ring
  rw [e, abs_neg]
  exact h'

/-- Any limit `c < 1` leaves a strictly positive saturation value, so the coupling
does not decay to zero.  Only the fully uniform field (`c = 1`, zero variance) does. -/
theorem saturation_pos {c : ℝ} (hc : c < 1) : 0 < 1 - c := by
  linarith

end CQM.BondGeometry
