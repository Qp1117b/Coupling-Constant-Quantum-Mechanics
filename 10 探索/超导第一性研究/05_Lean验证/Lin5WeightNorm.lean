import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# Lin-5: weight normalization for high modes (structural, NOT closing status)
CQM 12.A3: Phi_n/Phi_2 = 2/n = 1/k for n=2k (k=1,2,...).
If ALL modes filled, sum_k 1/k = harmonic series DIVERGES -> cannot normalize.
Physical resolution: finite participation ratio (Lin-21) -> finite cutoff K ->
normalized weight w_k = (1/k)/H_K with H_K = harmonic sum (positive, external).
Algebraic core proved here. No axiom/sorry/admit/native_decide/unsafe.
-/

namespace CQM.Lin5

/-- Raw weight from 12.A3: 1/k, decreasing. -/
theorem w_raw_decreasing (k : ℝ) (hk : 0 < k) :
    1 / (k + 1) < 1 / k := by
  exact one_div_lt_one_div_of_lt hk (by linarith)

/-- Normalized weight: w_k = (1/k)/H. Sum to one requires H = sum of 1/k (external). -/
theorem w_norm (k H : ℝ) (hk : k ≠ 0) (hH : H ≠ 0) :
    (1 / k) / H = 1 / (k * H) := by
  field_simp [hk, hH]

/-- First mode dominates: (1/1)/H > (1/k)/H for k>1, H>0. -/
theorem first_mode_dominates (k H : ℝ) (hk : 1 < k) (hH : 0 < H) :
    (1 / k) / H < (1 / (1 : ℝ)) / H := by
  have hkpos : 0 < k := by linarith
  rw [div_lt_div_iff_of_pos_right hH]
  exact one_div_lt_one_div_of_lt (by norm_num : (0 : ℝ) < 1) hk

/-- Divergence motivation: if weights were 1/k for all k with NO cutoff,
    normalization constant H_K grows like ln K (harmonic) -> unbounded.
    Algebraic core: sum of first K weights exceeds ln(K+1) style growth is external analysis;
    here we prove the reciprocal identity showing 2/n converts to 1/k exactly. -/
theorem mode_index (n k : ℝ) (hn : n = 2 * k) (hk : k ≠ 0) :
    2 / n = 1 / k := by
  rw [hn]
  field_simp [hk]

/-- Participation-ratio bound: n_eff >= 1 -> effective mode count >= 1,
    so at least first mode exists; finite n_eff -> finite K (external link). -/
theorem effective_modes_nonempty (neff : ℝ) (h : 1 ≤ neff) : 0 < neff := by
  linarith

end CQM.Lin5
