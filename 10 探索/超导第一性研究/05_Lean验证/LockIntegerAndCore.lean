import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# 环 15／目标区：锁定整数与涡旋核能反演的代数骨架（第 159 轮）

只承载代数与序；不证明 XY 核能、逸度指数、$p_{\rm sync}$ 充分性。
无 `axiom`／`sorry`／`admit`／`native_decide`／`unsafe`。
-/

namespace CQM.LockIntegerAndCore

noncomputable section

/-- **锁定分解**：$0\le y<1$ ⇒ $p_{\rm sync}=p_{\rm pair}(1-y)\le p_{\rm pair}$。 -/
theorem lock_le_pair {y psync ppair : ℝ} (hy0 : 0 ≤ y)
    (h : psync = ppair * (1 - y)) (hpp : 0 ≤ ppair) : psync ≤ ppair := by
  rw [h]
  have hfac : 1 - y ≤ 1 := by linarith
  exact mul_le_of_le_one_right hpp hfac

/-- **阈值抬升**：$p_{\rm pair}(1-y)>p_c$、$0\le y<1$ ⇒ $p_c/(1-y)<p_{\rm pair}$ 且 $p_c<p_c/(1-y)$。 -/
theorem threshold_uplift {y ppair pc : ℝ} (hypos : 0 < y) (hy1 : y < 1)
    (hp : pc < ppair * (1 - y)) (hpc : 0 < pc) :
    pc / (1 - y) < ppair ∧ pc < pc / (1 - y) := by
  have hden : 0 < 1 - y := by linarith
  constructor
  · rw [div_lt_iff₀ hden]
    exact hp
  · rw [lt_div_iff₀ hden]
    nlinarith

/-- **核能反演**：$E_c=\pi^2\Upsilon_0/2$、$\Upsilon_0=U(0)/\Phi_0$ ⇒ $E_c=\pi^2U(0)/(2\Phi_0)$。 -/
theorem core_from_inversion {Ec U0 Phi0 Upsilon0 : ℝ} (hPhi : Phi0 ≠ 0)
    (hEc : Ec = Real.pi ^ 2 / 2 * Upsilon0) (hU : Upsilon0 = U0 / Phi0) :
    Ec = Real.pi ^ 2 * U0 / (2 * Phi0) := by
  rw [hEc, hU]
  field_simp [hPhi]

/-- **重整化核能恒等式**：若误用 $\Upsilon=2T/\pi$，则 $\pi^2\Upsilon/2=\pi T$（给 $y=2\pi e^{-\pi}$，违反界的代数前置）。 -/
theorem renormalized_core_identity {U T : ℝ} (hU : U = 2 * T / Real.pi) :
    Real.pi ^ 2 / 2 * U = Real.pi * T := by
  rw [hU]
  field_simp [Real.pi_ne_zero]

/-- **$t\ge1$ 的代数核**：$\ln(1-y)\le0$、$\ln p<0$ ⇒ $1+\ln(1-y)/\ln p\ge1$。 -/
theorem t_ge_one {a b : ℝ} (ha : a ≤ 0) (hb : b < 0) : 1 ≤ 1 + a / b := by
  have hna : 0 ≤ -a := by linarith
  have hnb : 0 < -b := by linarith
  have hdiv : 0 ≤ (-a) / (-b) := div_nonneg hna (le_of_lt hnb)
  have hEq : (-a) / (-b) = a / b := by ring
  rw [← hEq]
  linarith

end
end CQM.LockIntegerAndCore
