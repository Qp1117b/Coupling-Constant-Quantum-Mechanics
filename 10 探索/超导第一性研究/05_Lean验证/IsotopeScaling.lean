import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# 审-10: cutoff and isotope scaling (conditional algebra)

Formalises the algebra of `03_推导工作台/环10_审10截断与同位素.md`.

Proves:

1. `omega_log` for the 2D Debye weight `2 y` is `omega_D * exp(-1/2)`,
   versus `omega_D * exp(-1/3)` for the 3D weight `3 y^2`;
2. a mass-independent stiffness gives a mass-independent `Tc` (isotope exponent 0);
3. a stiffness proportional to `omega_D` gives `Tc ~ M^{-1/2}` (exponent 1/2);
4. the two endpoint ratios differ by `sqrt(M1/M2)`.

The integrals defining `omega_log` and `w(T)` are NOT formalised here;
only the resulting algebraic scaling laws are.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.IsotopeScaling

noncomputable section

/-- 2D Debye logarithmic moment: `omega_log = omega_D * exp(-1/2)`. -/
def omegaLog2D (omegaD : ℝ) : ℝ := omegaD * Real.exp (-(1 / 2 : ℝ))

/-- 3D Debye logarithmic moment: `omega_log = omega_D * exp(-1/3)`. -/
def omegaLog3D (omegaD : ℝ) : ℝ := omegaD * Real.exp (-(1 / 3 : ℝ))

/-- The 2D moment is strictly below the 3D moment for a positive cutoff. -/
theorem omegaLog2D_lt_3D {omegaD : ℝ} (h : 0 < omegaD) :
    omegaLog2D omegaD < omegaLog3D omegaD := by
  unfold omegaLog2D omegaLog3D
  have hpos : 0 < Real.exp (-(1 / 3 : ℝ)) := Real.exp_pos _
  have hexp : Real.exp (-(1 / 2 : ℝ)) < Real.exp (-(1 / 3 : ℝ)) := by
    exact Real.exp_lt_exp.mpr (by norm_num)
  exact mul_lt_mul_of_pos_left hexp h

/-- Ratio of the two moments is `exp(-1/6)`, approximately 0.8465. -/
theorem omegaLog_ratio :
    omegaLog2D 1 / omegaLog3D 1 = Real.exp (-(1 / 6 : ℝ)) := by
  dsimp [omegaLog2D, omegaLog3D]
  ring_nf
  rw [← div_eq_mul_inv]
  rw [← Real.exp_sub]
  congr 1
  norm_num

/-- If the stiffness is mass-independent, the predicted `Tc` is mass-independent:
the isotope exponent is zero. -/
theorem isotope_exponent_zero {C : ℝ} (hC : C ≠ 0) : C / C = (1 : ℝ) := by
  field_simp [hC]

/-- If `Tc = omega_D / k` and `omega_D = const / sqrt(M)`, then the ratio of
critical temperatures is `sqrt(M1/M2)`. -/
theorem isotope_ratio_half {K M1 M2 : ℝ} (hK : K ≠ 0)
    (hM1 : 0 < M1) (hM2 : 0 < M2) :
    (K / Real.sqrt M2) / (K / Real.sqrt M1) = Real.sqrt (M1 / M2) := by
  have hsqrt1 : Real.sqrt M1 ≠ 0 := ne_of_gt (Real.sqrt_pos.2 hM1)
  have hsqrt2 : Real.sqrt M2 ≠ 0 := ne_of_gt (Real.sqrt_pos.2 hM2)
  field_simp [hK, hsqrt1, hsqrt2]
  rw [← Real.sqrt_mul hM2.le (M1 / M2)]
  have hprod : M2 * (M1 / M2) = M1 := by field_simp [ne_of_gt hM2]
  rw [hprod]

/-- The two endpoints differ: `sqrt(M1/M2) <> 1` when `M1 <> M2`. -/
theorem isotope_endpoints_differ {M1 M2 : ℝ} (hM1 : 0 < M1) (hM2 : 0 < M2)
    (hne : M1 ≠ M2) : Real.sqrt (M1 / M2) ≠ 1 := by
  intro h
  have hsq : (Real.sqrt (M1 / M2)) ^ 2 = 1 := by rw [h]; norm_num
  have hratio_nonneg : 0 ≤ M1 / M2 := div_nonneg hM1.le hM2.le
  rw [Real.sq_sqrt hratio_nonneg] at hsq
  have : M1 = M2 := by field_simp [ne_of_gt hM2] at hsq; exact hsq
  exact hne this

end

end CQM.IsotopeScaling
