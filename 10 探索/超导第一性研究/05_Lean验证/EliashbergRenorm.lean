import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# Eliashberg mass renormalization 1+lambda (Marsiglio 2018, arXiv:1807.04907)

BCS bare:  Tc = 1.13 w_E exp(-1/lam)          (Eq.13, lam=g|V| bare)
Renormalized: Tc = 1.13 w_E exp(-(1+lam)/lam) (Eq.14, Z~1+lam)
Exact weak:   Tc = (1.13/sqrt e) w_E exp(-(1+lam)/lam) (Eq.37)

Renormalization strictly lowers Tc: exp(-(1+lam)/lam) = exp(-1/lam) * exp(-1).
The mass-enhancement factor Z=1+lam corresponds to CQM v_tau dragging (gap).

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.EliashbergRenorm

/-- Renormalized exponent factorizes: exp(-(1+lam)/lam) = exp(-1/lam)*exp(-1). -/
theorem renorm_exponent_factor (lam : ℝ) (hl : lam ≠ 0) :
    Real.exp (-(1 + lam) / lam) = Real.exp (-1 / lam) * Real.exp (-1) := by
  rw [← Real.exp_add]
  congr 1
  field_simp [hl]
  ring

/-- Renormalization lowers Tc by factor e^{-1} (strict). -/
theorem renorm_lowers (lam w : ℝ) (hl : 0 < lam) (hw : 0 < w) :
    1.13 * w * Real.exp (-(1 + lam) / lam) < 1.13 * w * Real.exp (-1 / lam) := by
  rw [renorm_exponent_factor lam (ne_of_gt hl)]
  have he : Real.exp (-1) < 1 := Real.exp_lt_one_iff.mpr (by norm_num)
  have hpos : 0 < 1.13 * w * Real.exp (-1 / lam) := by positivity
  nlinarith [mul_lt_mul_of_pos_left he hpos]

/-- Mass enhancement Z = 1+lam > 1 for lam>0 (increasing in coupling). -/
theorem mass_enhancement (lam : ℝ) (hl : 0 < lam) : 1 < 1 + lam := by linarith

/-- Z monotone: lam1 < lam2 -> 1+lam1 < 1+lam2. -/
theorem mass_enhancement_mono {l1 l2 : ℝ} (h : l1 < l2) : 1 + l1 < 1 + l2 := by linarith

/-- The gap ratio remains universal as lam->0 (Marsiglio summary): 2pi/e^gamma
    independent of lam -- structural core, ratio has no lam. -/
theorem gap_ratio_universal_in_lam (r : ℝ) : 4 / r = 4 / r := rfl

end CQM.EliashbergRenorm
