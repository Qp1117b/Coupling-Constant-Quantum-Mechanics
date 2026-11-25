import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# `临-16`: all-pairs c_ij = 0 is unreachable (measure zero + gauge trivial)

c_ij = a_i - a_j with kernel = constant vector (dim 1).  All-pairs zero iff
a is constant.  Discrete uniform model: P(all equal) = M / M^N = 1/M^(N-1)
-> 0.  A kernel shift a_i -> a_i + c leaves every c_ij unchanged.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.AllZeroUnreachable

/-- A coboundary on n nodes: c_ij = a_i - a_j. -/
def cob (a : Fin n → ℝ) (i j : Fin n) : ℝ := a i - a j

/-- Kernel shift leaves every coboundary component unchanged (gauge trivial). -/
theorem kernel_shift_no_change (a : Fin n → ℝ) (cshift : ℝ) (i j : Fin n) :
    cob (fun k => a k + cshift) i j = cob a i j := by
  unfold cob
  ring

/-- All-pairs zero iff a is constant (kernel = constant vector). -/
theorem all_zero_iff_constant (a : Fin n → ℝ) (i0 : Fin n) :
    (∀ i j : Fin n, cob a i j = 0) ↔ (∀ i : Fin n, a i = a i0) := by
  constructor
  · intro h i
    have h0 : cob a i i0 = 0 := h i i0
    unfold cob at h0
    linarith
  · intro hc i j
    unfold cob
    rw [hc i, hc j]
    ring_nf

/-- Discrete uniform model: P(all equal) = M / M^N = 1 / M^(N-1). -/
theorem uniform_all_equal_probability (M N : ℕ) (hM : 0 < M) (hN : 0 < N) :
    (M : ℝ) / (M : ℝ) ^ N = 1 / (M : ℝ) ^ (N - 1) := by
  have hMr : (M : ℝ) ≠ 0 := by exact_mod_cast (ne_of_gt hM)
  have hpow : (M : ℝ) ^ N = (M : ℝ) ^ (N - 1) * M := by
    rw [← pow_succ]
    congr 1
    omega
  rw [hpow]
  field_simp [hMr]

/-- For M >= 2, 1/M^N <= 1/2^N (probability decays at least geometrically). -/
theorem prob_le_geometric (M N : ℕ) (hM : 2 ≤ M) :
    1 / (M : ℝ) ^ N ≤ (1 / 2 : ℝ) ^ N := by
  have hMr : (0 : ℝ) < M := by exact_mod_cast (lt_of_lt_of_le (by norm_num) hM)
  have hbase : (2 : ℝ) ≤ M := by exact_mod_cast hM
  have hpow : (2 : ℝ) ^ N ≤ (M : ℝ) ^ N := by
    gcongr
  have h2pos : (0 : ℝ) < (2 : ℝ) ^ N := pow_pos (by norm_num) _
  have h1 : 1 / (M : ℝ) ^ N ≤ 1 / (2 : ℝ) ^ N :=
    one_div_le_one_div_of_le h2pos hpow
  have h2 : (1 / 2 : ℝ) ^ N = 1 / (2 : ℝ) ^ N := by
    rw [one_div_pow]
  rw [h2]
  exact h1

end CQM.AllZeroUnreachable
