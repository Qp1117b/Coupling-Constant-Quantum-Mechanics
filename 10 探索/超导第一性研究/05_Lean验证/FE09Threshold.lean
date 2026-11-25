import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Data.Real.Basic
import Mathlib.Data.Real.Sqrt

/-!
# FE09: 阈值超导候选的代数核（框架扩展，非链内已证）

- sum 1/k^3 ≤ 2 ⇒ Lambda_c = 1/zeta(3) ≥ 1/2（严格下界）
- Lambda*S < 1 ⇒ 无解（阈值条件）
- gap 因子 E/sqrt(E^2+D^2) ≤ 1（右端有界）
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.FE09

noncomputable section

/-- sum_{k=1}^K 1/k^3 ≤ 2。 -/
private theorem cube_step (n : ℕ) (hn : 1 ≤ n) :
    (1 : ℝ) / ((n : ℝ) + 1) ^ 3 ≤ 1 / (n : ℝ) - 1 / ((n : ℝ) + 1) := by
  have hnpos : 0 < (n : ℝ) := by exact_mod_cast (lt_of_lt_of_le Nat.zero_lt_one hn)
  have hnp1 : 0 < (n : ℝ) + 1 := by positivity
  field_simp [hnpos.ne', hnp1.ne']
  nlinarith [sq_nonneg ((n : ℝ) + 1)]

private theorem sum_aux : ∀ K : ℕ, 1 ≤ K →
    Finset.sum (Finset.range K) (fun k => (1 : ℝ) / (k + 1 : ℝ) ^ 3) ≤ 2 - 1 / (K : ℝ)
  | 0, h => by omega
  | 1, h => by norm_num
  | K + 2, h => by
      rw [Finset.sum_range_succ]
      have ih := sum_aux (K + 1) (by omega)
      have hs := cube_step (K + 1) (by omega)
      have heq : ((K + 1 : ℕ) : ℝ) + 1 = (K + 2 : ℕ) := by
        exact_mod_cast (show (K + 1) + 1 = K + 2 by omega)
      rw [heq] at hs
      rw [heq]
      simp only [one_div] at ih hs ⊢
      linarith

theorem sum_inv_cube_le_two (K : ℕ) :
    Finset.sum (Finset.range K) (fun k => (1 : ℝ) / (k + 1 : ℝ) ^ 3) ≤ 2 := by
  cases K with
  | zero => norm_num
  | succ n =>
      have h := sum_aux (n + 1) (by omega)
      have hpos : 0 ≤ (1 : ℝ) / (n + 1 : ℝ) := by positivity
      have heq : ((n + 1 : ℕ) : ℝ) = (n : ℝ) + 1 := by norm_num
      rw [heq] at h
      simp only [one_div] at h hpos ⊢
      linarith

/-- 阈值严格下界：S ≤ 2 且 S>0 ⇒ Lambda_c = 1/S ≥ 1/2。 -/
theorem threshold_lower_bound (S : ℝ) (hSpos : 0 < S) (hSle : S ≤ 2) :
    1 / 2 ≤ 1 / S := by
  exact one_div_le_one_div_of_le hSpos hSle

/-- Lambda*S < 1 ⇒ Lambda < 1/S（低于阈值无解）。 -/
theorem no_solution_below_threshold (Lam S : ℝ) (hS : 0 < S) (hprod : Lam * S < 1) :
    Lam < 1 / S := by
  exact (lt_div_iff₀ hS).2 (by simpa [mul_comm] using hprod)

/-- gap 因子有界：E/sqrt(E^2+D^2) ≤ 1。 -/
theorem gap_factor_le_one (E D : ℝ) (hE : 0 < E) :
    E / Real.sqrt (E ^ 2 + D ^ 2) ≤ 1 := by
  have hsqrtpos : 0 < Real.sqrt (E ^ 2 + D ^ 2) :=
    Real.sqrt_pos.2 (by nlinarith [sq_pos_of_pos hE])
  rw [div_le_iff₀ hsqrtpos]
  have hle : E ≤ Real.sqrt (E ^ 2 + D ^ 2) := by
    rw [Real.le_sqrt (le_of_lt hE) (by nlinarith [sq_nonneg E, sq_nonneg D])]
    nlinarith [sq_nonneg D]
  simpa using hle

end
end CQM.FE09
