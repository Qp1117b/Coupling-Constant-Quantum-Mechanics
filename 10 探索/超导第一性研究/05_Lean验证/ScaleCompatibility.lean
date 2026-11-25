import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity

/-!
# `审-15`: compatibility of logarithmic and power-law scales

For a power-law spectrum E_n = E_1 n^p, the logarithmic step is
Delta log E_n = p log(1+1/n) ~ p/n.  CQM (12.3) has p=2; 2D flexural phonons
(omega ~ q^2 with equally spaced q) also have p=2, so the two agree in the same
logarithmic coordinate.  The apparent "log vs power" conflict is a coordinate
mix-up (CQM uses Delta log E, phonons use Delta omega).

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.ScaleCompatibility

/-- Logarithmic step of a quadratic spectrum: Delta log E = 2 log((n+1)/n). -/
theorem log_step_sq (E1 : ℝ) (hE1 : 0 < E1) (n : ℕ) (hn : 0 < n) :
    Real.log (E1 * ((n + 1 : ℕ) : ℝ) ^ 2) - Real.log (E1 * (n : ℝ) ^ 2) =
      2 * (Real.log ((n + 1 : ℕ) : ℝ) - Real.log (n : ℝ)) := by
  have hn0 : (n : ℝ) ≠ 0 := by exact_mod_cast (ne_of_gt hn)
  have hn1 : ((n + 1 : ℕ) : ℝ) ≠ 0 := by positivity
  rw [Real.log_mul (ne_of_gt hE1) (pow_ne_zero 2 hn0),
      Real.log_mul (ne_of_gt hE1) (pow_ne_zero 2 hn1)]
  rw [Real.log_pow, Real.log_pow]
  ring

/-- Logarithmic step of a linear spectrum: Delta log omega = log((n+1)/n). -/
theorem log_step_linear (E1 : ℝ) (hE1 : 0 < E1) (n : ℕ) (hn : 0 < n) :
    Real.log (E1 * ((n + 1 : ℕ) : ℝ)) - Real.log (E1 * (n : ℝ)) =
      Real.log ((n + 1 : ℕ) : ℝ) - Real.log (n : ℝ) := by
  have hn0 : (n : ℝ) ≠ 0 := by exact_mod_cast (ne_of_gt hn)
  have hn1 : ((n + 1 : ℕ) : ℝ) ≠ 0 := by positivity
  rw [Real.log_mul (ne_of_gt hE1) hn1, Real.log_mul (ne_of_gt hE1) hn0]
  ring

/-- The logarithmic step decreases with n (p/n behaviour). -/
theorem log_step_vanish {n m : ℕ} (hn : 0 < n) (hnm : n < m) :
    Real.log ((m : ℝ) + 1) - Real.log (m : ℝ) <
      Real.log ((n : ℝ) + 1) - Real.log (n : ℝ) := by
  have hnpos : (0 : ℝ) < n := by exact_mod_cast hn
  have hmpos : (0 : ℝ) < m := by exact_mod_cast (lt_trans hn hnm)
  have hn0 : (n : ℝ) ≠ 0 := ne_of_gt hnpos
  have hm0 : (m : ℝ) ≠ 0 := ne_of_gt hmpos
  have hn1 : (n : ℝ) + 1 ≠ 0 := by positivity
  have hm1 : (m : ℝ) + 1 ≠ 0 := by positivity
  rw [← Real.log_div hm1 hm0, ← Real.log_div hn1 hn0]
  apply Real.log_lt_log
  · positivity
  · have hnr : (n : ℝ) < m := by exact_mod_cast hnm
    field_simp [hn0, hm0]
    nlinarith

/-- Counting coordinate: log of a power-law count is linear in log E. -/
theorem count_log_linear (N0 E : ℝ) (hN0 : 0 < N0) (hE : 0 < E) :
    Real.log (N0 * E ^ 2) = Real.log N0 + 2 * Real.log E := by
  rw [Real.log_mul (ne_of_gt hN0) (pow_ne_zero 2 (ne_of_gt hE))]
  rw [Real.log_pow]
  ring

end CQM.ScaleCompatibility
