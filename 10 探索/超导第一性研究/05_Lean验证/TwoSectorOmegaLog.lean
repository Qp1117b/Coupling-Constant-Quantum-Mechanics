import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# `审-10`: the two sector-specific logarithmic Debye moments

The amplitude (pairing) sector uses the 3D Debye density of states `3y²`, giving
`ω_log^amp = ω_D · exp(-1/3)`.  The phase (coherence) sector uses the 2D weight `2y`,
giving `ω_log^ph = ω_D · exp(-1/2)`.  The earlier "replace e^{-1/3} by e^{-1/2}"
was an over-correction: the moments must be split by sector, not replaced.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.TwoSectorOmegaLog

/-- The dimensionless prefactor for a d-dimensional Debye density of states. -/
noncomputable def prefactor (d : ℝ) : ℝ := Real.exp (-1 / d)

/-- The two sector moments, both proportional to the same energy scale ω_D. -/
noncomputable def omegaLogAmp (omegaD : ℝ) : ℝ := omegaD * prefactor 3
noncomputable def omegaLogPh (omegaD : ℝ) : ℝ := omegaD * prefactor 2

/-- The two prefactors are distinct. -/
theorem two_moments_differ : prefactor 3 ≠ prefactor 2 := by
  unfold prefactor
  intro h
  have he : -1 / (3 : ℝ) = -1 / (2 : ℝ) := Real.exp_injective h
  norm_num at he

/-- Their ratio is exp(1/6), independent of the energy scale. -/
theorem ratio_of_moments {omegaD : ℝ} (hw : omegaD ≠ 0) :
    omegaLogAmp omegaD / omegaLogPh omegaD = Real.exp (1 / 6 : ℝ) := by
  unfold omegaLogAmp omegaLogPh prefactor
  rw [mul_div_mul_left _ _ hw]
  rw [← Real.exp_sub]
  norm_num

/-- Numerical values of the prefactors. -/
theorem prefactor_three : prefactor 3 = Real.exp (-(1 / 3 : ℝ)) := by
  unfold prefactor
  norm_num

theorem prefactor_two : prefactor 2 = Real.exp (-(1 / 2 : ℝ)) := by
  unfold prefactor
  norm_num

/-- Both moments scale the same way with the isotopic mass through ω_D ∝ M^{-1/2}. -/
theorem isotope_scaling_same {omegaD1 omegaD2 : ℝ} :
    omegaLogAmp omegaD2 / omegaLogAmp omegaD1 =
     omegaLogPh omegaD2 / omegaLogPh omegaD1 := by
  unfold omegaLogAmp omegaLogPh
  have hprefA : prefactor 3 ≠ 0 := by unfold prefactor; positivity
  have hprefP : prefactor 2 ≠ 0 := by unfold prefactor; positivity
  field_simp [hprefA, hprefP]

/-- A single common moment cannot equal both sector moments: replacing instead of
splitting is impossible. -/
theorem sector_not_replace (m : ℝ) {omegaD : ℝ} (hw : omegaD ≠ 0)
    (ha : m = omegaLogAmp omegaD) (hp : m = omegaLogPh omegaD) : False := by
  have h : omegaLogAmp omegaD = omegaLogPh omegaD := ha.symm.trans hp
  have hratio : omegaLogAmp omegaD / omegaLogPh omegaD = 1 := by
    rw [h]
    exact div_self (by unfold omegaLogPh prefactor; positivity)
  rw [ratio_of_moments hw] at hratio
  have : Real.exp (1 / 6 : ℝ) ≠ 1 := by
    intro he
    have hz : (1 / 6 : ℝ) = 0 := Real.exp_injective (by
      rw [Real.exp_zero]
      exact he)
    norm_num at hz
  exact this hratio

end CQM.TwoSectorOmegaLog
