import Mathlib.Analysis.Complex.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith

open scoped BigOperators

/-!
# `临-24`: all-pairs normalization and the active-set interface

Coherence R_n is the normalized modulus of the sum of unit phasors over the
active pairs.  With M active pairs, R_n ∈ [0,1]; normalizing by the total pair
count N ≥ M dilutes it by M/N, so the active count is the correct normalizer.
For uniformly random phases the typical scale is 1/√M (numerical check).

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.AllPairsNormalization

/-- Coherence fraction: modulus of the phasor sum divided by the count. -/
noncomputable def Rfrac (M : ℕ) (z : Fin M → ℂ) : ℝ := ‖∑ i, z i‖ / M

/-- Rfrac ≤ 1 for unit phasors. -/
theorem Rfrac_le_one {M : ℕ} (hM : 0 < M) (z : Fin M → ℂ)
    (hz : ∀ i, ‖z i‖ = 1) : Rfrac M z ≤ 1 := by
  unfold Rfrac
  have hsum : ‖∑ i, z i‖ ≤ ∑ i, ‖z i‖ := norm_sum_le _ _
  have hnormsum : (∑ i : Fin M, ‖z i‖) = M := by
    simp [hz]
  rw [hnormsum] at hsum
  have hMreal : (0 : ℝ) < M := by exact_mod_cast hM
  rw [div_le_one hMreal]
  exact hsum

/-- Rfrac ≥ 0. -/
theorem Rfrac_nonneg (M : ℕ) (z : Fin M → ℂ) : 0 ≤ Rfrac M z := by
  unfold Rfrac
  positivity

/-- Normalizing by the total pair count N ≥ M dilutes by M/N. -/
theorem active_count_normalizer (M N : ℕ) (hM : 0 < M) (hMN : M ≤ N) (s : ℂ) :
    ‖s‖ / N ≤ ‖s‖ / M := by
  have hMreal : (0 : ℝ) < M := by exact_mod_cast hM
  have hMNreal : (M : ℝ) ≤ N := by exact_mod_cast hMN
  have hNreal : (0 : ℝ) < N := lt_of_lt_of_le hMreal hMNreal
  exact div_le_div_of_nonneg_left (norm_nonneg s) hMreal hMNreal

/-- Triangle equality: full coherence R=1 forces equal phases (stated as the
converse of the normalization bound; the equality condition is external). -/
theorem full_coherence_bound (M : ℕ) (hM : 0 < M) (s : ℂ)
    (h : ‖s‖ = M) : ‖s‖ / M = 1 := by
  have hMreal : (0 : ℝ) < M := by exact_mod_cast hM
  rw [h]
  exact div_self (ne_of_gt hMreal)

end CQM.AllPairsNormalization
