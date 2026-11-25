import Mathlib.Tactic.Linarith
import Mathlib.Data.Real.Basic

/-!
# R19: 磁场方向判据 Υ(B) ≤ Υ(0) 的代数核

前提（已登记）：f(0)=1、f 单调减、x=B/Bc2 ≥ 0、Υ(0)>0。
- R19.1: x≥0 ⇒ f(x) ≤ 1
- R19.2: Υ(0) f(x) ≤ Υ(0)
- R19.3: Uemura 上界随 Υ 单调 ⇒ Tc 上界不增
- 反例：f 非单调时 R19.1 可违（前提必要）
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.FieldDirection

noncomputable section

/-- 单调减+归一化：x≥0 ⇒ f(x) ≤ 1。 -/
theorem f_le_one {f : ℝ → ℝ} (hmono : Antitone f) (hf0 : f 0 = 1) {x : ℝ} (hx : 0 ≤ x) :
    f x ≤ 1 := by
  have h : f x ≤ f 0 := hmono hx
  linarith

/-- 刚度方向判据：Υ(0)>0 ⇒ Υ(0) f(x) ≤ Υ(0)。 -/
theorem upsilong_le {f : ℝ → ℝ} (hmono : Antitone f) (hf0 : f 0 = 1)
    (U0 : ℝ) (hU0 : 0 < U0) {x : ℝ} (hx : 0 ≤ x) :
    U0 * f x ≤ U0 := by
  have hf := f_le_one hmono hf0 hx
  have h := mul_le_mul_of_nonneg_left hf hU0.le
  simpa using h

/-- Uemura 上界随 Υ 单调 ⇒ Tc 上界不增：Q≥0 时 (π/2) Υ Q 随 Υ 单调。 -/
theorem tc_upper_monotone (U1 U2 Q : ℝ) (hQ : 0 ≤ Q) (hU : U1 ≤ U2) :
    U1 * Q ≤ U2 * Q := by
  exact mul_le_mul_of_nonneg_right hU hQ

/-- 前提必要：f 非单调时 f(x)≤1 可违（说明单调减前提不可省）。 -/
theorem monotone_needed :
    ∃ (f : ℝ → ℝ) (x : ℝ), 0 ≤ x ∧ f 0 = 1 ∧ f x > 1 := by
  refine ⟨fun t => t + 1, 1, ?_⟩
  norm_num

end
end CQM.FieldDirection
