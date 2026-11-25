import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-!
# R14: 配对电荷/磁通量子数据核对的代数核

- Phi_0 = h/q；q=2e ⇒ Phi_0=h/(2e)；q=e ⇒ Phi_0=h/e = 2*(h/(2e))
- B_c2 = Phi_0/(2 pi xi^2)：q=e 给 q=2e 值的 2 倍
- 独立判别条件：xi 与 B_c2 独立测量时才成立
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.FluxQuantumCheck

noncomputable section

/-- q=e 的磁通量子是 q=2e 的两倍：h/e = 2*(h/(2e))。 -/
theorem flux_double (h e : ℝ) (he : e ≠ 0) :
    h / e = 2 * (h / (2 * e)) := by
  field_simp [he]

/-- B_c2 ∝ Phi_0：q=e 的 B_c2 是 q=2e 值的两倍。 -/
theorem bc2_double (Phi xi : ℝ) (hxi : xi ≠ 0) :
    (2 * Phi) / (2 * Real.pi * xi ^ 2) = 2 * (Phi / (2 * Real.pi * xi ^ 2)) := by
  field_simp [hxi, ne_of_gt (mul_pos (by norm_num : (0 : ℝ) < 2) Real.pi_pos)]

end
end CQM.FluxQuantumCheck
