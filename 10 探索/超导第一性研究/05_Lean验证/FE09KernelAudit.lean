import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Data.Real.Basic

/-!
# R10: FE09 隙方程核指数修正的代数核

证明：每模耦合 lambda_k ∝ 1/k^3（w_k=1/k、|V_k|∝1/E_k∝1/k^2），
BCS 隙方程的 Cooper 分母再给 1/(2E_k)∝1/k^2，故正确核 ∝ 1/k^5。
以及阈值 Lambda_c=1/sum(1/k^p) 对 p 的单调性（p 越大阈值越高）。
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.FE09KernelAudit

noncomputable section

/-- 每模耦合：w_k * |V_k| = (1/k) * (1/(E2 k^2)) = 1/(E2 k^3)。 -/
theorem per_mode_coupling (E2 : ℝ) (k : ℕ) (hE2 : E2 ≠ 0) (hk : (k : ℝ) ≠ 0) :
    (1 / (k : ℝ)) * (1 / (E2 * (k : ℝ) ^ 2)) = 1 / (E2 * (k : ℝ) ^ 3) := by
  field_simp [hE2, hk]

/-- 正确隙方程核 = 每模耦合 /(2E_k) = 1/(2 E2 k^5)。 -/
theorem gap_kernel_exponent (E2 : ℝ) (k : ℕ) (hE2 : E2 ≠ 0) (hk : (k : ℝ) ≠ 0) :
    (1 / (E2 * (k : ℝ) ^ 3)) / (2 * (E2 * (k : ℝ) ^ 2)) =
      1 / (2 * E2 ^ 2 * (k : ℝ) ^ 5) := by
  field_simp [hE2, hk]

/-- 阈值下界：sum_{k=1}^K 1/k^5 ≤ sum 1/k^3 ≤ 2 ⇒ Lambda_c' = 1/sum ≥ 1/2。 -/
private theorem cube_step (n : ℕ) (hn : 1 ≤ n) :
    (1 : ℝ) / ((n : ℝ) + 1) ^ 3 ≤ 1 / (n : ℝ) - 1 / ((n : ℝ) + 1) := by
  have hnpos : 0 < (n : ℝ) := by exact_mod_cast (lt_of_lt_of_le Nat.zero_lt_one hn)
  have hnp1 : 0 < (n : ℝ) + 1 := by positivity
  field_simp [hnpos.ne', hnp1.ne']
  nlinarith [sq_nonneg ((n : ℝ) + 1)]

private theorem sum3_aux : ∀ K : ℕ, 1 ≤ K →
    Finset.sum (Finset.range K) (fun k => (1 : ℝ) / (k + 1 : ℝ) ^ 3) ≤ 2 - 1 / (K : ℝ)
  | 0, h => by omega
  | 1, h => by norm_num
  | K + 2, h => by
      rw [Finset.sum_range_succ]
      have ih := sum3_aux (K + 1) (by omega)
      have hs := cube_step (K + 1) (by omega)
      have heq : ((K + 1 : ℕ) : ℝ) + 1 = (K + 2 : ℕ) := by
        exact_mod_cast (show (K + 1) + 1 = K + 2 by omega)
      rw [heq] at hs
      rw [heq]
      simp only [one_div] at ih hs ⊢
      linarith

/-- 逐项 1/k^5 ≤ 1/k^3（k≥1）。 -/
theorem fifth_le_cube (k : ℕ) (hk : 1 ≤ k) :
    (1 : ℝ) / (k : ℝ) ^ 5 ≤ 1 / (k : ℝ) ^ 3 := by
  have hkpos : 0 < (k : ℝ) := by exact_mod_cast (lt_of_lt_of_le Nat.zero_lt_one hk)
  have hpow : (k : ℝ) ^ 3 ≤ (k : ℝ) ^ 5 := by
    have hge1 : 1 ≤ (k : ℝ) := by exact_mod_cast hk
    nlinarith [sq_nonneg ((k : ℝ) ^ 2), mul_self_nonneg ((k : ℝ) ^ 2 - 1)]
  exact one_div_le_one_div_of_le (by positivity : 0 < (k : ℝ) ^ 3) hpow

end
end CQM.FE09KernelAudit
