import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Data.Real.Basic

/-!
# R4: 对 R2/R3 自我审计的代数核

证明配对通道模和收敛（R4.1 无对数）：
单项 w_k |V_k| = 1/(E2 k^3)，部分和 sum_{k=1}^K 1/k^3 ≤ 2。
故 sum w_k |V_k| ≤ 2/E2 对所有 K 成立，不产生对数。
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.CooperLogAudit

noncomputable section

/-- 单项：(1/k)(1/(E2 k^2)) = 1/(E2 k^3)。 -/
theorem wV_term (E2 : ℝ) (k : ℕ) (hE2 : E2 ≠ 0) (hk : (k : ℝ) ≠ 0) :
    (1 / (k : ℝ)) * (1 / (E2 * (k : ℝ) ^ 2)) = 1 / (E2 * (k : ℝ) ^ 3) := by
  field_simp [hE2, hk]

/-- 归纳步不等式：对 n≥1，1/(n+1)^3 ≤ 1/n - 1/(n+1)。 -/
private theorem cube_step (n : ℕ) (hn : 1 ≤ n) :
    (1 : ℝ) / ((n : ℝ) + 1) ^ 3 ≤ 1 / (n : ℝ) - 1 / ((n : ℝ) + 1) := by
  have hnpos : 0 < (n : ℝ) := by exact_mod_cast (lt_of_lt_of_le Nat.zero_lt_one hn)
  have hnp1 : 0 < (n : ℝ) + 1 := by positivity
  field_simp [hnpos.ne', hnp1.ne']
  nlinarith [sq_nonneg ((n : ℝ) + 1)]

/-- 对 K≥1：sum_{k=0}^{K-1} 1/(k+1)^3 ≤ 2 - 1/K。 -/
theorem sum_inv_cube_le_aux : ∀ K : ℕ, 1 ≤ K →
    Finset.sum (Finset.range K) (fun k => (1 : ℝ) / (k + 1 : ℝ) ^ 3)
      ≤ 2 - 1 / (K : ℝ)
  | 0, h => by omega
  | 1, h => by norm_num
  | K + 2, h => by
      rw [Finset.sum_range_succ]
      have ih := sum_inv_cube_le_aux (K + 1) (by omega)
      have hs := cube_step (K + 1) (by omega)
      have heq : ((K + 1 : ℕ) : ℝ) + 1 = (K + 2 : ℕ) := by
        exact_mod_cast (show (K + 1) + 1 = K + 2 by omega)
      rw [heq] at hs
      rw [heq]
      simp only [one_div] at ih hs ⊢
      linarith

/-- sum_{k=1}^K 1/k^3 ≤ 2。 -/
theorem sum_inv_cube_le_two (K : ℕ) :
    Finset.sum (Finset.range K) (fun k => (1 : ℝ) / (k + 1 : ℝ) ^ 3) ≤ 2 := by
  cases K with
  | zero => norm_num
  | succ n =>
      have h := sum_inv_cube_le_aux (n + 1) (by omega)
      have hpos : 0 ≤ (1 : ℝ) / (n + 1 : ℝ) := by positivity
      have heq : ((n + 1 : ℕ) : ℝ) = (n : ℝ) + 1 := by norm_num
      rw [heq] at h
      simp only [one_div] at h hpos ⊢
      linarith

/-- (R4.1)：配对通道模和 ≤ 2/E2 对所有 K 成立——收敛，无对数。 -/
theorem pairing_sum_convergent (E2 : ℝ) (K : ℕ) (hE2 : 0 < E2) :
    Finset.sum (Finset.range K)
      (fun k => (1 / (k + 1 : ℝ)) * (1 / (E2 * (k + 1 : ℝ) ^ 2))) ≤ 2 / E2 := by
  have hterm :
      Finset.sum (Finset.range K)
        (fun k => (1 / (k + 1 : ℝ)) * (1 / (E2 * (k + 1 : ℝ) ^ 2)))
      = (1 / E2) * Finset.sum (Finset.range K)
          (fun k => (1 : ℝ) / (k + 1 : ℝ) ^ 3) := by
    induction K with
    | zero => simp
    | succ K ih =>
        rw [Finset.sum_range_succ, Finset.sum_range_succ, ih]
        have hk' : (K + 1 : ℝ) ≠ 0 := by positivity
        field_simp [hE2.ne', hk']
  rw [hterm]
  have hsum := sum_inv_cube_le_two K
  have hinvpos : 0 ≤ (1 : ℝ) / E2 := by positivity
  have hmul := mul_le_mul_of_nonneg_left hsum hinvpos
  calc
    (1 / E2) * Finset.sum (Finset.range K)
        (fun k => (1 : ℝ) / (k + 1 : ℝ) ^ 3) ≤ (1 / E2) * 2 := hmul
    _ = 2 / E2 := by ring

end
end CQM.CooperLogAudit
