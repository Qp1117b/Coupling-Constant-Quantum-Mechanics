import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp

/-!
# FE04 CANDIDATE (NOT LANDED): prefactor e^{-3/2} literature confirmation
Identities only. No axiom/sorry/admit/native_decide/unsafe.
-/

namespace CQM.FE04

/-- e^{-1/6} * e^{-1/3} = e^{-1/2}: CQM log-moment conversion. -/
theorem logmoment_conv :
    Real.exp (-(1 / 6 : ℝ)) * Real.exp (-(1 / 3 : ℝ)) = Real.exp (-(1 / 2 : ℝ)) := by
  rw [← Real.exp_add]
  congr 1
  norm_num

/-- e^{-1/2} * e^{-1} = e^{-3/2}: frequency-dependence x self-energy. -/
theorem prefactor_total :
    Real.exp (-(1 / 2 : ℝ)) * Real.exp (-1 : ℝ) = Real.exp (-(3 / 2 : ℝ)) := by
  rw [← Real.exp_add]
  congr 1
  norm_num

/-- exponent split: e^{-(1+lam)/lam} = e^{-1} e^{-1/lam} (lam != 0). -/
theorem exponent_split (lam : ℝ) (hlam : lam ≠ 0) :
    Real.exp (-((1 + lam) / lam)) = Real.exp (-1 : ℝ) * Real.exp (-(1 / lam)) := by
  rw [← Real.exp_add]
  congr 1
  field_simp [hlam]
  ring

/-- CQM展开 = literature绝热区前因子 (lam != 0). -/
theorem cqm_equals_literature (theta lam : ℝ) (hlam : lam ≠ 0) :
    1.13 * Real.exp (-(1 / 6 : ℝ)) * (Real.exp (-(1 / 3 : ℝ)) * theta)
        * Real.exp (-((1 + lam) / lam))
      = 1.13 * Real.exp (-(3 / 2 : ℝ)) * theta * Real.exp (-(1 / lam)) := by
  rw [exponent_split lam hlam]
  have h1 := logmoment_conv
  have h2 := prefactor_total
  calc
    1.13 * Real.exp (-(1 / 6 : ℝ)) * (Real.exp (-(1 / 3 : ℝ)) * theta)
        * (Real.exp (-1 : ℝ) * Real.exp (-(1 / lam)))
        = (1.13 * theta * Real.exp (-(1 / lam)))
            * (Real.exp (-(1 / 6 : ℝ)) * Real.exp (-(1 / 3 : ℝ))) * Real.exp (-1 : ℝ) := by ring
    _ = (1.13 * theta * Real.exp (-(1 / lam)))
            * Real.exp (-(1 / 2 : ℝ)) * Real.exp (-1 : ℝ) := by rw [h1]
    _ = (1.13 * theta * Real.exp (-(1 / lam)))
            * (Real.exp (-(1 / 2 : ℝ)) * Real.exp (-1 : ℝ)) := by ring
    _ = 1.13 * Real.exp (-(3 / 2 : ℝ)) * theta * Real.exp (-(1 / lam)) := by rw [h2]; ring

end CQM.FE04
