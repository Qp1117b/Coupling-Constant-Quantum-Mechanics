import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp

/-!
# R24: (目标.2) μ*=0 极限识别的代数核

- 比值恒等：(1+λ)/λ ÷ [1.04(1+λ)/λ] = 1/1.04（∀λ≠0, 1+λ≠0）
- 因果：指数小 ⇒ exp(-指数) 大 ⇒ Tc 高估
- μ*>0 时 AD 指数 > μ*=0 指数
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.MuZeroLimit

noncomputable section

open Real

/-- 比值恒等：(chain 指数)/(AD mu*=0 指数) = 1/1.04。 -/
theorem exponent_ratio (lam : ℝ) (hl : lam ≠ 0) (h1l : 1 + lam ≠ 0) :
    ((1 + lam) / lam) / ((1.04 : ℝ) * (1 + lam) / lam) = 1 / (1.04 : ℝ) := by
  field_simp [hl, h1l]

/-- 若 chain 指数 < AD 指数，则 chain 的 exp 因子更大（高估）。 -/
theorem smaller_exponent_larger_factor (a b : ℝ) (hab : a < b) :
    Real.exp (-a) > Real.exp (-b) := by
  exact Real.exp_lt_exp.mpr (by linarith)

/-- μ*>0 使 AD 分母变小 ⇒ 指数变大 ⇒ Tc 被压低。 -/
theorem mu_star_increases_exponent (lam mu : ℝ) (hl : 0 < lam) (hmu : 0 < mu)
    (hden : 0 < lam - mu * (1 + 0.62 * lam)) :
    1.04 * (1 + lam) / lam < 1.04 * (1 + lam) / (lam - mu * (1 + 0.62 * lam)) := by
  have hdenlt : lam - mu * (1 + 0.62 * lam) < lam := by nlinarith
  -- A/lam < A/d  (A>0, d<lam, both positive): A*d < A*lam
  have hA : 0 < (1.04 : ℝ) * (1 + lam) := by positivity
  rw [div_lt_div_iff₀ hl hden]
  nlinarith

end
end CQM.MuZeroLimit
