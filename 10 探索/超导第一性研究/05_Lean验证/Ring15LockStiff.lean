-- Ring15LockStiff.lean（第 185 轮）：逸度归刚度——(15L.3) 的 Υ 是有效刚度
-- 只 import Spec（v12），逐条对齐三条意图命题；无 sorry／admit／自造 axiom。
import Ring15Spec

namespace CQM.Ring15.LockStiff

open CQM.Ring15.Spec

noncomputable section

private lemma pi_sq_pos : (0 : ℝ) < Real.pi ^ 2 := by
  nlinarith [Real.pi_pos]

/-- `fugOfK` 关于 `K` 严格减（`exp` 严格增 + 指数里 `−π²K/2` 严格减）。 -/
private lemma fug_strictAnti {K K' : ℝ} (h : K < K') : fugOfK K' < fugOfK K := by
  have hc : (0 : ℝ) < 2 * Real.pi := by positivity
  have harg : -(Real.pi ^ 2 * K' / 2) < -(Real.pi ^ 2 * K / 2) := by
    nlinarith [pi_sq_pos]
  unfold fugOfK
  exact mul_lt_mul_of_pos_left (Real.exp_lt_exp.mpr harg) hc

/-- 意图命题（一）：`Υ/T` 严格增 ⇒ `y` 严格减。即 $T$ 依赖全部经刚度。 -/
theorem targetPropFugStiff : TargetPropFugStiff := by
  intro ups ups' T T' _ _ _ _ hK
  exact fug_strictAnti hK

/-- 意图命题（二）：(15L.5) 的界是充要的。 -/
theorem targetPropFugBound : TargetPropFugBound := by
  intro beta K hbeta _
  have hc : (0 : ℝ) < 2 * Real.pi := by positivity
  have hpi : (0 : ℝ) < Real.pi ^ 2 := pi_sq_pos
  have hb : (0 : ℝ) < 1 / beta := one_div_pos.mpr hbeta
  constructor
  · intro h
    have h1 : Real.exp (-(Real.pi ^ 2 * K / 2)) ≤ Real.exp (-(Real.pi ^ 2 * (1 / beta) / 2)) := by
      unfold fugOfK at h
      exact le_of_mul_le_mul_left h hc
    have h2 : -(Real.pi ^ 2 * K / 2) ≤ -(Real.pi ^ 2 * (1 / beta) / 2) := Real.exp_le_exp.mp h1
    nlinarith
  · intro h
    have h2 : -(Real.pi ^ 2 * K / 2) ≤ -(Real.pi ^ 2 * (1 / beta) / 2) := by nlinarith
    have h1 : Real.exp (-(Real.pi ^ 2 * K / 2)) ≤ Real.exp (-(Real.pi ^ 2 * (1 / beta) / 2)) :=
      Real.exp_le_exp.mpr h2
    unfold fugOfK
    exact mul_le_mul_of_nonneg_left h1 (le_of_lt hc)

/-- 意图命题（三）：(15L.5) 反解出的 `Υ₀` 下界。 -/
theorem targetPropUpsLower : TargetPropUpsLower := by
  intro ups w T beta _ hw hT hbeta h
  have hb : (0 : ℝ) < beta := hbeta
  have hbw : (0 : ℝ) < beta * w := mul_pos hb hw
  have h1 : 1 / beta * T ≤ ups * w := (le_div_iff₀ hT).mp h
  have hmul : beta * (1 / beta * T) ≤ beta * (ups * w) :=
    mul_le_mul_of_nonneg_left h1 (le_of_lt hb)
  have hleft : beta * (1 / beta * T) = T := by
    rw [← mul_assoc, mul_one_div_cancel (ne_of_gt hb), one_mul]
  have h4 : T ≤ beta * (ups * w) := by
    rw [hleft] at hmul
    exact hmul
  rw [div_le_iff₀ hbw]
  nlinarith [h4]

end

end CQM.Ring15.LockStiff
