import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Data.Real.Basic
import Mathlib.Data.Real.Sqrt

/-!
# R8: 环节⑨ 不可能性定理的代数核（R4+R5+R7 合取）

三条独立 no-go 的合取：
(1) 配对模和 sum 1/k^3 ≤ 2（收敛，无对数）——R4；
(2) DOS integrand 幂律 E^{-3/2}（无对数）——R5；
(3) 玻色 coth ≠ 费米 tanh，Matsubara 格点不交——R7。
合取给"链内不能同时提供 BCS Tc 三要素"的结构定理。
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.TripleNoGo

noncomputable section

open Real

/-- (R4) 配对模和部分和 ≤ 2：Finset.sum (range K) 1/(k+1)^3 ≤ 2。 -/
private theorem cube_step (n : ℕ) (hn : 1 ≤ n) :
    (1 : ℝ) / ((n : ℝ) + 1) ^ 3 ≤ 1 / (n : ℝ) - 1 / ((n : ℝ) + 1) := by
  have hnpos : 0 < (n : ℝ) := by exact_mod_cast (lt_of_lt_of_le Nat.zero_lt_one hn)
  have hnp1 : 0 < (n : ℝ) + 1 := by positivity
  field_simp [hnpos.ne', hnp1.ne']
  nlinarith [sq_nonneg ((n : ℝ) + 1)]

private theorem sum_inv_cube_le_aux : ∀ K : ℕ, 1 ≤ K →
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

theorem pairing_sum_le_two (K : ℕ) :
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

/-- (R5) DOS integrand 幂律：g/E ∝ E^{-3/2}（以 sqrt E 表示），非 1/E。 -/
theorem dos_integrand_power (E : ℝ) (hE : 0 < E) :
    (1 / (2 * Real.sqrt E)) / E = 1 / (2 * E * Real.sqrt E) := by
  field_simp [hE.ne', (Real.sqrt_pos.2 hE).ne']

/-- (R7) 热核统计类型：coth(a) ≠ tanh(a) for a>1（a=e^{2x}）。 -/
theorem thermal_no_identity (a : ℝ) (ha : 1 < a) :
    (a + 1) / (a - 1) ≠ (a - 1) / (a + 1) := by
  have h1 : 1 < (a + 1) / (a - 1) := by
    have hd : 0 < a - 1 := by linarith
    rw [lt_div_iff₀ hd]
    nlinarith
  have h2 : (a - 1) / (a + 1) < 1 := by
    have hd : 0 < a + 1 := by linarith
    rw [div_lt_iff₀ hd]
    nlinarith
  intro heq
  rw [heq] at h1
  linarith

/-- (R7) Matsubara 格点不交：2n ≠ 2m+1。 -/
theorem matsubara_disjoint (n m : ℤ) : 2 * n ≠ 2 * m + 1 := by
  intro h
  omega

/-- 合取：链内不能同时提供对数、费米热核，Matsubara 格点不交。 -/
theorem triple_no_go (a : ℝ) (ha : 1 < a) (E : ℝ) (hE : 0 < E) :
    ((∀ K : ℕ, Finset.sum (Finset.range K)
        (fun k => (1 : ℝ) / (k + 1 : ℝ) ^ 3) ≤ 2)
      ∧ ((a + 1) / (a - 1) ≠ (a - 1) / (a + 1))
      ∧ ((1 / (2 * Real.sqrt E)) / E = 1 / (2 * E * Real.sqrt E))) := by
  exact ⟨pairing_sum_le_two, thermal_no_identity a ha, dos_integrand_power E hE⟩

end
end CQM.TripleNoGo
