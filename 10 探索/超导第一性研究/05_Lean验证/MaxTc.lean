import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-!
# R15: 最大 Tc 的代数核（条件结果）

核心不等式 ln u <= u-1 ⇒ u exp(-u) <= exp(-1)（等号 u=1）。
推出 kappa exp(-2 A kappa) <= 1/(2 A e)，即 sqrt(kappa)exp(-A kappa) 的上界。
不把数值 Tc 或外生参数写成定理。无 axiom/sorry/admit/native_decide/unsafe。
-/

namespace CQM.MaxTc

noncomputable section

open Real

/-- 核心不等式：u>0 ⇒ u exp(-u) <= exp(-1)（来自 ln u <= u-1）。 -/
theorem u_exp_neg_u_le (u : ℝ) (hu : 0 < u) : u * Real.exp (-u) ≤ Real.exp (-1 : ℝ) := by
  have hlog : Real.log u ≤ u - 1 := Real.log_le_sub_one_of_pos hu
  have h1 : u ≤ Real.exp (u - 1) := by
    calc
      u = Real.exp (Real.log u) := (Real.exp_log hu).symm
      _ ≤ Real.exp (u - 1) := Real.exp_le_exp.mpr hlog
  calc
    u * Real.exp (-u) ≤ Real.exp (u - 1) * Real.exp (-u) :=
      mul_le_mul_of_nonneg_right h1 (Real.exp_pos (-u)).le
    _ = Real.exp (-1 : ℝ) := by
      rw [← Real.exp_add]
      congr 1
      ring

/-- 等号点：u=1 时 u exp(-u) = exp(-1)（最大值可达）。 -/
theorem equality_at_one : (1 : ℝ) * Real.exp (-1) = Real.exp (-1 : ℝ) := by ring

/-- 平方界：A>0, kappa>0 ⇒ kappa exp(-2 A kappa) <= 1/(2 A e)。 -/
theorem kappa_exp_bound (A kappa : ℝ) (hA : 0 < A) (hk : 0 < kappa) :
    kappa * Real.exp (-2 * A * kappa) ≤ 1 / (2 * A * Real.exp 1) := by
  let u := 2 * A * kappa
  have hu : 0 < u := by dsimp [u]; positivity
  have hcore := u_exp_neg_u_le u hu
  dsimp [u] at hcore
  have hrew : (2 * A * kappa) * Real.exp (-(2 * A * kappa)) =
      2 * A * (kappa * Real.exp (-2 * A * kappa)) := by ring
  rw [hrew] at hcore
  have hpos : 0 < 2 * A := by positivity
  -- 从 2A*(kappa exp...) <= exp(-1) 得 kappa exp... <= exp(-1)/(2A) = 1/(2A exp1)
  have hfinal : kappa * Real.exp (-2 * A * kappa) ≤ Real.exp (-1 : ℝ) / (2 * A) := by
    exact (le_div_iff₀ hpos).2 (by simpa [mul_comm] using hcore)
  calc
    kappa * Real.exp (-2 * A * kappa) ≤ Real.exp (-1 : ℝ) / (2 * A) := hfinal
    _ = 1 / (2 * A * Real.exp 1) := by
      field_simp [hA.ne', (Real.exp_pos 1).ne']
      rw [← Real.exp_add]
      norm_num

end
end CQM.MaxTc
