import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Data.Real.Basic

/-!
# R38: 端到端 Tc 贡献分解的代数核（隔离区）

Ad指数 E(λ,μ*) = -1.04(1+λ)/(λ-μ*(1+0.62λ))，1.04=26/25, 0.62=31/50。
压制因子 F = exp(E(λ,μ*) - E(λ,0)) = exp(E(λ,μ*) + 26/25·(1+λ)/λ)。
- μ*=0 ⇒ F=1
- μ*>0 ⇒ 指数<0 ⇒ F<1
这是外生 μ* 贡献的代数核；CQM 链不含 μ*。
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.EndToEndContribution

noncomputable section

/-- AD 指数的相反数（正值部分）：A(λ,μ*) = 1.04(1+λ)/(λ-μ*(1+0.62λ))。 -/
def Aexp (lam mu : ℝ) : ℝ := (26 / 25 : ℝ) * (1 + lam) / (lam - mu * (1 + (31 / 50 : ℝ) * lam))

/-- μ*=0 时 A(λ,0)=26/25·(1+λ)/λ。 -/
theorem A_zero (lam : ℝ) (hlam : lam ≠ 0) :
    Aexp lam 0 = (26 / 25 : ℝ) * (1 + lam) / lam := by
  unfold Aexp
  field_simp [hlam]
  ring

/-- μ*>0 使 A(λ,μ*)>A(λ,0)（分母变小），故 ln F=A(0)-A(μ)<0 ⇒ F<1（压制）。 -/
theorem suppression_A_increases (lam mu : ℝ) (hlam : 0 < lam) (hmu : 0 < mu)
    (hden : 0 < lam - mu * (1 + (31 / 50 : ℝ) * lam)) :
    (26 / 25 : ℝ) * (1 + lam) / lam < Aexp lam mu := by
  unfold Aexp
  -- 同分子 C=(26/25)(1+λ)>0，分母 d=λ-μ(1+0.62λ)<λ ⇒ C/λ < C/d
  have hC : 0 < (26 / 25 : ℝ) * (1 + lam) := by positivity
  rw [div_lt_div_iff₀ hlam hden]
  -- 目标 C·d < C·λ，即 C·(λ-μ(...))<C·λ
  have hsmall : lam - mu * (1 + (31 / 50 : ℝ) * lam) < lam := by
    have : 0 < mu * (1 + (31 / 50 : ℝ) * lam) := by positivity
    linarith
  exact mul_lt_mul_of_pos_left hsmall hC

end
end CQM.EndToEndContribution
