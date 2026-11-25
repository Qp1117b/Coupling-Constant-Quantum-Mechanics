import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith

/-!
# Lin-6: flux-quantum normalization disambiguation (structural, NOT closing status)
Authority 06 §0.8 (line 482/485), §9 (1020), §0.6 (1197-1201):
  Phi_n = h/(n e)  (single-quantum flux unit, experimentally measured h/ne)
  Phi_n/Phi_2 = 2/n  (charge-quantum normalization)
Winding reading: total flux of n quanta = n*h/(2e), ratio n/2 -- OPPOSITE direction.
Resolution: two DIFFERENT objects sharing symbol Phi_n:
  Phi_n^unit  = h/(ne)      -> ratio 2/n  (single quantum, measured)
  Phi_n^total = n*h/(2e)    -> ratio n/2  (total flux of n quanta)
No axiom/sorry/admit/native_decide/unsafe.
-/

namespace CQM.Lin6

/-- Single-quantum flux unit ratio: (h/ne)/(h/2e) = 2/n. -/
theorem unit_ratio (h e n : ℝ) (hh : h ≠ 0) (he : e ≠ 0) (hn : n ≠ 0) :
    (h / (n * e)) / (h / (2 * e)) = 2 / n := by
  field_simp [hh, he, hn]

/-- Total flux of n quanta ratio to n=2: n/2. -/
theorem total_ratio (h e n : ℝ) (hh : h ≠ 0) (he : e ≠ 0) :
    (n * h / (2 * e)) / (2 * h / (2 * e)) = n / 2 := by
  field_simp [hh, he]

/-- The two ratios are reciprocal: (2/n)*(n/2)=1. -/
theorem reciprocal (n : ℝ) (hn : n ≠ 0) : (2 / n) * (n / 2) = 1 := by
  field_simp [hn]

/-- total / unit = n^2/2. -/
theorem total_over_unit (h e n : ℝ) (hh : h ≠ 0) (he : e ≠ 0) (hn : n ≠ 0) :
    (n * h / (2 * e)) / (h / (n * e)) = n ^ 2 / 2 := by
  field_simp [hh, he, hn]

/-- Unit weight 2/n decreases in n (first-band dominance, 12.A3);
    total weight n/2 increases. -/
theorem unit_weight_decreasing (n1 n2 : ℝ) (h1 : 0 < n1) (hlt : n1 < n2) :
    2 / n2 < 2 / n1 := by
  have h2 : 0 < n2 := by linarith
  rw [div_lt_div_iff₀ h2 h1]
  nlinarith

end CQM.Lin6
