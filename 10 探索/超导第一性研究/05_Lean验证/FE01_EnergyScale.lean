import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# FE01 framework-extension CANDIDATE (NOT LANDED): dimensional postulate -> Tc scale
Algebraic core only. No axiom/sorry/admit/native_decide/unsafe.
-/

namespace CQM.FE01

/-- Ratio of Debye frequencies: sqrt(kappa/M2)/sqrt(kappa/M1) = sqrt(M1/M2).
    Proof: squares equal, both sides nonnegative so negative branch is excluded. -/
theorem omegaD_mass_scaling (kappa M1 M2 : ℝ) (hκ : 0 < kappa) (hM1 : 0 < M1) (hM2 : 0 < M2) :
    Real.sqrt (kappa / M2) / Real.sqrt (kappa / M1) = Real.sqrt (M1 / M2) := by
  have hs : (Real.sqrt (kappa / M2) / Real.sqrt (kappa / M1)) ^ 2
      = (Real.sqrt (M1 / M2)) ^ 2 := by
    rw [div_pow, Real.sq_sqrt (div_nonneg (le_of_lt hκ) (le_of_lt hM2)),
        Real.sq_sqrt (div_nonneg (le_of_lt hκ) (le_of_lt hM1)),
        Real.sq_sqrt (div_nonneg (le_of_lt hM1) (le_of_lt hM2))]
    field_simp [ne_of_gt hκ, ne_of_gt hM1, ne_of_gt hM2]
  rw [sq_eq_sq_iff_eq_or_eq_neg] at hs
  rcases hs with h | h
  · exact h
  · have hL : 0 ≤ Real.sqrt (kappa / M2) / Real.sqrt (kappa / M1) := by positivity
    have hR : 0 < Real.sqrt (M1 / M2) := Real.sqrt_pos.2 (div_pos hM1 hM2)
    nlinarith

/-- Tc mass ratio under the candidate: common factor C cancels. -/
theorem tc_mass_ratio (kappa M1 M2 C : ℝ) (hκ : 0 < kappa) (hM1 : 0 < M1) (hM2 : 0 < M2)
    (hC : C ≠ 0) :
    (C * Real.sqrt (kappa / M2)) / (C * Real.sqrt (kappa / M1)) = Real.sqrt (M1 / M2) := by
  rw [mul_div_mul_left _ _ hC]
  exact omegaD_mass_scaling kappa M1 M2 hκ hM1 hM2

/-- Isotope exponent: for Tc ~ M^{-1/2}, alpha = -dlnTc/dlnM = 1/2. -/
theorem isotope_alpha_half (M1 M2 : ℝ) (hM1 : 0 < M1) (hM2 : 0 < M2) (hne : M2 ≠ M1) :
    - Real.log (Real.sqrt (M1 / M2)) / Real.log (M2 / M1) = (1 / 2 : ℝ) := by
  rw [Real.log_sqrt (le_of_lt (div_pos hM1 hM2))]
  have hlog : Real.log (M1 / M2) = - Real.log (M2 / M1) := by
    rw [Real.log_div (ne_of_gt hM1) (ne_of_gt hM2),
        Real.log_div (ne_of_gt hM2) (ne_of_gt hM1)]
    ring
  rw [hlog]
  field_simp [Real.log_ne_zero_of_pos_of_ne_one (div_pos hM2 hM1)
              (by intro h; apply hne; field_simp [ne_of_gt hM1] at h; nlinarith)]

/-- Positivity of the candidate scale. -/
theorem tc_scale_pos (kappa M n C : ℝ) (hκ : 0 < kappa) (hM : 0 < M)
    (hn : 0 < n) (hC : 0 < C) :
    0 < C * Real.sqrt (kappa / M) * (6 * Real.pi ^ 2 * n) ^ (1 / 3 : ℝ) := by
  positivity

end CQM.FE01
