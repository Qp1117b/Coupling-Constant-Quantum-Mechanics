import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# Karakozov prefactor e^{-1/6} (log-moment form)

Marsiglio arXiv:1807.04907 Eq26: prefactor 1.13 e^{-1/2} (cutoff omega).
CQM uses log-moment omega_log = theta e^{-1/3}.  Conversion:
1.13 e^{-1/2} theta = 1.13 e^{-1/6} (theta e^{-1/3}) = 1.13 e^{-1/6} omega_log.
Thus CQM prefactor must carry e^{-1/6} in log-moment form to match Eq37.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.KarakozovPrefactor

/-- Cutoff-to-log-moment conversion: e^{-1/2} = e^{-1/6} * e^{-1/3}. -/
theorem cutoff_to_logmoment :
    Real.exp (-(1 / 2 : ℝ)) = Real.exp (-(1 / 6 : ℝ)) * Real.exp (-(1 / 3 : ℝ)) := by
  rw [← Real.exp_add]
  congr 1
  norm_num

/-- Prefactor equality: 1.13 e^{-1/2} theta = 1.13 e^{-1/6} (theta e^{-1/3}). -/
theorem prefactor_eq (th : ℝ) :
    1.13 * Real.exp (-(1 / 2 : ℝ)) * th =
      1.13 * Real.exp (-(1 / 6 : ℝ)) * (th * Real.exp (-(1 / 3 : ℝ))) := by
  rw [cutoff_to_logmoment]
  ring

/-- Shape neutrality: constant prefactor c cancels in gap ratio 2(zD)/(zT). -/
theorem constant_prefactor_neutral (c d t : ℝ) (hc : c ≠ 0) (ht : t ≠ 0) :
    2 * (c * d) / (c * t) = 2 * d / t := by
  field_simp [hc, ht]

/-- Inverse-lambda algebra unchanged by prefactor rescale p1 -> p2:
    log(p2/T)-1 = log(p1/T)-1 + log(p2/p1) (shift), structural core. -/
theorem inverse_lambda_shift (p1 p2 T : ℝ) (hp1 : 0 < p1) (hp2 : 0 < p2) (hT : 0 < T) :
    Real.log (p2 / T) - Real.log (p1 / T) = Real.log (p2 / p1) := by
  rw [Real.log_div (ne_of_gt hp2) (ne_of_gt hT),
      Real.log_div (ne_of_gt hp1) (ne_of_gt hT),
      Real.log_div (ne_of_gt hp2) (ne_of_gt hp1)]
  ring

end CQM.KarakozovPrefactor
