import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# `审-3`: zero-point variance pinned down; temperature has one entrance

From (4.1), sigma^2(T) = sigma_0^2 [1 + 2 n_B], n_B = 1/(exp x - 1), x>0.
(9.1)(10.2) use sigma_0^2 (the subscript 0 is zero-point), so they carry no
temperature.  QHO identity 1+2/(e^x-1) = (e^x+1)/(e^x-1) = coth(x/2).

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.ZeroPointVariance

/-- Bose occupation n_B = 1/(exp x - 1) is positive for x>0. -/
theorem nB_pos (x : ℝ) (hx : 0 < x) : 0 < 1 / (Real.exp x - 1) := by
  have h1 : 1 < Real.exp x := by
    simpa using (Real.exp_lt_exp.mpr hx)
  have hden : 0 < Real.exp x - 1 := by linarith
  exact one_div_pos.mpr hden

/-- The thermal factor 1+2n_B is at least 1. -/
theorem factor_ge_one (x : ℝ) (hx : 0 < x) : 1 ≤ 1 + 2 / (Real.exp x - 1) := by
  have hden : 0 < Real.exp x - 1 := by
    have h1 : 1 < Real.exp x := by simpa using (Real.exp_lt_exp.mpr hx)
    linarith
  have h2 : 0 < 2 / (Real.exp x - 1) := div_pos (by norm_num) hden
  linarith

/-- Finite zero-point variance gives sigma^2(T) >= sigma_0^2. -/
theorem sigma2_ge_zero (s0 x : ℝ) (hs0 : 0 < s0) (hx : 0 < x) :
    s0 ≤ s0 * (1 + 2 / (Real.exp x - 1)) := by
  have h := factor_ge_one x hx
  nlinarith [mul_le_mul_of_nonneg_left h (le_of_lt hs0)]

/-- QHO identity: 1+2/(e^x-1) = (e^x+1)/(e^x-1) = coth(x/2). -/
theorem coth_form (x : ℝ) (hx : 0 < x) :
    1 + 2 / (Real.exp x - 1) = (Real.exp x + 1) / (Real.exp x - 1) := by
  have hden : Real.exp x - 1 ≠ 0 := by
    have h1 : 1 < Real.exp x := by simpa using (Real.exp_lt_exp.mpr hx)
    linarith
  field_simp [hden]
  ring

/-- High-temperature bound: n_B < 1/x from 1+x < e^x (classical limit scale). -/
theorem high_temp_classical (x : ℝ) (hx : 0 < x) :
    1 / (Real.exp x - 1) < 1 / x := by
  have hx1 : 1 + x < Real.exp x := by
    simpa [add_comm] using (Real.add_one_lt_exp (ne_of_gt hx))
  have hden : 0 < Real.exp x - 1 := by linarith
  have hxpos : 0 < x := hx
  have hlt : x < Real.exp x - 1 := by linarith
  exact one_div_lt_one_div_of_lt hxpos hlt

/-- Zero-temperature point: n_B -> 0 as x -> infinity; at x with exp x - 1
    denominator, the zero-point part is the x-independent s0.  Formal core:
    if the thermal factor equals 1, then sigma^2 equals sigma_0^2. -/
theorem zero_temp_factor (s0 x : ℝ) (h : 1 + 2 / (Real.exp x - 1) = 1) :
    s0 * (1 + 2 / (Real.exp x - 1)) = s0 := by
  rw [h]
  ring

end CQM.ZeroPointVariance
