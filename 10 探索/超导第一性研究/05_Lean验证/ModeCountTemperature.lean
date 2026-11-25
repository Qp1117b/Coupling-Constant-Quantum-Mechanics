import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

/-!
# Ring 15: leading temperature correction when `n_cell = N_eff(T)`

At low temperature the Debye weight behaves as `w = 1 - a t` and the
readable-mode count as `n = n0 (1 - b t)`, with `t = (T/omega_D)^2`.
The normalized chi-square argument is

`x / x0 = (1 - b t) / (1 - a t)`.

This file records the exact decomposition

`(1 - b t)/(1 - a t) = 1 + (a - b) t + (a - b) a t^2/(1 - a t)`,

so the leading coefficient is `a - b`, not `a + b`.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.ModeCountTemperature

noncomputable section

/-- Exact decomposition of the normalized argument ratio. -/
theorem ratio_expansion (a b t : ℝ) (h : 1 - a * t ≠ 0) :
    (1 - b * t) / (1 - a * t) =
    1 + (a - b) * t + ((a - b) * a * t^2) / (1 - a * t) := by
  field_simp [h, mul_comm]
  ring

/-- The residual after subtracting the linear term is quadratic. -/
theorem ratio_residual (a b t : ℝ) (h : 1 - a * t ≠ 0) (ht : t ≠ 0) :
    ((1 - b * t) / (1 - a * t) - (1 + (a - b) * t)) / t^2 =
    ((a - b) * a) / (1 - a * t) := by
  field_simp [h, ht, mul_comm]
  ring

end

end CQM.ModeCountTemperature
