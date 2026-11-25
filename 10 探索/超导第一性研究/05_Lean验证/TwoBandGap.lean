import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# Review: two-band gap-ratio superposition (algebraic core)
w*r1 + (1-w)*r2 with r2=r1*(1+d); CQM 12.A3 weight Phi_n/Phi_2=2/n.
Material-side explanation of single-band gap-ratio deviation.
No axiom/sorry/admit/native_decide/unsafe.
-/

namespace CQM.TwoBand

/-- Two-band weighted average: w*r1+(1-w)*r2, r2=r1(1+d).
    Equals r1*(1+(1-w)*d): deviation from single-band is (1-w)*d. -/
theorem two_band_decomp (w r1 d : ℝ) :
    w * r1 + (1 - w) * (r1 * (1 + d)) = r1 * (1 + (1 - w) * d) := by
  ring

/-- Deviation fraction from single band is (1-w)*d (positive when d>0, w<1). -/
theorem dev_fraction (w r1 d : ℝ) (hr1 : r1 ≠ 0) :
    (w * r1 + (1 - w) * (r1 * (1 + d)) - r1) / r1 = (1 - w) * d := by
  rw [two_band_decomp]
  field_simp [hr1]
  ring

/-- CQM 12.A3 weight: Phi_4/Phi_2 = 2/4 = 1/2; normalized w1 = 1/(1+1/2) = 2/3. -/
theorem mode_weight_n4 :
    (2 : ℝ) / 4 = 1 / 2 := by norm_num

theorem mode_weight_normalized :
    1 / (1 + (2 : ℝ) / 4) = 2 / 3 := by norm_num

/-- With w=2/3 and d=0.10, deviation = (1/3)*0.1 = 1/30 ~ 3.3% of single band. -/
theorem dev_at_cqm_weight :
    (1 - (2 : ℝ) / 3) * (1 / 10 : ℝ) = 1 / 30 := by norm_num

end CQM.TwoBand
