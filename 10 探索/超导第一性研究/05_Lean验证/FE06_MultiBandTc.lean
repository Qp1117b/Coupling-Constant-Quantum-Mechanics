import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# FE06 CANDIDATE (NOT LANDED): SMW two-band eigenvalue + CQM 12.A weight
Eigenvalue of 2x2 coupling matrix; enhancement lambda_eff >= max(lambda_ii);
12.A3 weight 2/n. No axiom/sorry/admit/native_decide/unsafe.
-/

namespace CQM.FE06

/-- SMW effective coupling (largest eigenvalue of 2x2 matrix). -/
noncomputable def lambdaEff (a b c : ℝ) : ℝ :=
  (a + b + Real.sqrt ((a - b)^2 + 4*c^2)) / 2

/-- lambda_eff >= a when c^2 >= 0. -/
theorem lambdaEff_ge_a (a b c : ℝ) : a ≤ lambdaEff a b c := by
  unfold lambdaEff
  have hsq : (a - b)^2 ≤ (a - b)^2 + 4*c^2 := by nlinarith [sq_nonneg c]
  have hsqrt : |a - b| ≤ Real.sqrt ((a - b)^2 + 4*c^2) := by
    rw [← Real.sqrt_sq_eq_abs (a - b)]
    exact Real.sqrt_le_sqrt hsq
  have hab : a - b ≤ |a - b| := le_abs_self (a - b)
  nlinarith

/-- lambda_eff >= b (symmetric). -/
theorem lambdaEff_ge_b (a b c : ℝ) : b ≤ lambdaEff a b c := by
  unfold lambdaEff
  have hsq : (a - b)^2 ≤ (a - b)^2 + 4*c^2 := by nlinarith [sq_nonneg c]
  have hsqrt : |a - b| ≤ Real.sqrt ((a - b)^2 + 4*c^2) := by
    rw [← Real.sqrt_sq_eq_abs (a - b)]
    exact Real.sqrt_le_sqrt hsq
  have hba : b - a ≤ |a - b| := by
    have := neg_le_abs (a - b)
    linarith
  nlinarith

/-- CQM 12.A3 weight Phi_n/Phi_2 = 2/n; n=4 -> Phi_4/Phi_2=2/4=1/2. -/
theorem mode_weight_n4 : (2 : ℝ) / 4 = 1 / 2 := by norm_num

/-- Tc monotone increasing in lambda_eff (exponent -1/lambda less negative). -/
theorem tc_mono_lambda (w L1 L2 : ℝ) (hw : 0 < w) (hL1 : 0 < L1) (hL2 : 0 < L2)
    (hlt : L1 < L2) :
    w * Real.exp (-(1 / L1)) < w * Real.exp (-(1 / L2)) := by
  have hfrac : -(1 / L1) < -(1 / L2) := by
    rw [neg_lt_neg_iff]
    field_simp [ne_of_gt hL1, ne_of_gt hL2]
    nlinarith
  exact mul_lt_mul_of_pos_left (Real.exp_lt_exp.mpr hfrac) hw

end CQM.FE06
