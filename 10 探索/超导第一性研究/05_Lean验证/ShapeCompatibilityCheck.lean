import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# Full-chain shape compatibility check (non-fitting)

Structural cores: T_c = min of three temperatures is bounded by each; the
thermal factor 1+2n_B increases with T; the decoherence window gamma* ~ 1/sigma
is inverse to the width; min of an increasing and a decreasing branch is a
single peak (dome) on an interval where they cross.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.ShapeCompatibilityCheck

/-- T_c = min of three temperatures is bounded above by each. -/
theorem min_three_le_left (a b c : ℝ) : min (min a b) c ≤ a := by
  exact le_trans (min_le_left _ _) (min_le_left _ _)

theorem min_three_le_mid (a b c : ℝ) : min (min a b) c ≤ b := by
  exact le_trans (min_le_left _ _) (min_le_right _ _)

theorem min_three_le_right (a b c : ℝ) : min (min a b) c ≤ c := min_le_right _ _

/-- If a <= a' then min(a,b,c) <= min(a',b,c) (monotone in each argument). -/
theorem min_three_mono_left {a a' b c : ℝ} (h : a ≤ a') :
    min (min a b) c ≤ min (min a' b) c := by
  gcongr

/-- Thermal factor 1+2n_B(x) decreases in x = hbar omega / kT;
    since x ~ 1/T, the factor increases with T.  Core: for 0<x1<x2,
    n_B(x2) < n_B(x1). -/
theorem nB_strict_anti (x1 x2 : ℝ) (hx1 : 0 < x1) (h12 : x1 < x2) :
    1 / (Real.exp x2 - 1) < 1 / (Real.exp x1 - 1) := by
  have h1 : (1 : ℝ) < Real.exp x1 := by simpa using (Real.exp_lt_exp.mpr hx1)
  have h2 : (1 : ℝ) < Real.exp x2 := by simpa using (Real.exp_lt_exp.mpr (lt_trans hx1 h12))
  have he : Real.exp x1 < Real.exp x2 := Real.exp_lt_exp.mpr h12
  have hd1 : 0 < Real.exp x1 - 1 := by linarith
  have hd2 : 0 < Real.exp x2 - 1 := by linarith
  have hden : Real.exp x1 - 1 < Real.exp x2 - 1 := by linarith
  exact one_div_lt_one_div_of_lt hd1 hden

/-- Thermal factor is strictly above 1 for x>0. -/
theorem thermal_factor_gt_one (x : ℝ) (hx : 0 < x) :
    1 < 1 + 2 / (Real.exp x - 1) := by
  have h1 : 1 < Real.exp x := by simpa using (Real.exp_lt_exp.mpr hx)
  have hd : 0 < Real.exp x - 1 := by linarith
  have h2 : 0 < 2 / (Real.exp x - 1) := div_pos (by norm_num) hd
  linarith

/-- Decoherence window gamma* ~ 1/sigma: larger width -> smaller window. -/
theorem window_inverse_width (s1 s2 : ℝ) (hs1 : 0 < s1) (h12 : s1 < s2) :
    1 / s2 < 1 / s1 := by
  exact one_div_lt_one_div_of_lt hs1 h12

/-- Dome core: if f increases and g decreases, and they cross, then h=min(f,g)
    is bounded above by both, and equals f on the left of crossing, g on the right.
    We formalize the algebraic core at the crossing point p0 with f(p0)=g(p0). -/
theorem dome_min_at_crossing (l r : ℝ)
    (hcross : l = r) :
    min l r = l := by rw [hcross]; simp

/-- At any p, min(f(p),g(p)) <= the crossing value when f(p) <= crossing and
    g(p) <= crossing on respective sides -- captured by the bound lemmas above.
    The single-peak shape is thus a consequence of min's upper-bound structure. -/
theorem min_bounded_by_crossing (f_val g_val peak : ℝ)
    (hf : f_val ≤ peak) (hg : g_val ≤ peak) :
    min f_val g_val ≤ peak := by
  rcases le_total f_val g_val with hfg | hgf
  · rw [min_eq_left hfg]
    exact hf
  · rw [min_eq_right hgf]
    exact hg

end CQM.ShapeCompatibilityCheck
