import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# `临-11`: the |D_i|^(-1/2) self-averaging scale

Variance of a sample mean over n elements:
  Var = (n σ² + C)/n²,  C = Σ_{k≠l} Cov.
Independent case C=0 gives Var = σ²/n (standard error ∝ n^{-1/2}).
A positive average covariance gives a nonzero variance floor, so self-averaging
fails unless the covariance sum grows sub-quadratically.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.SelfAveraging

/-- Variance of a mean, with C the sum of off-diagonal covariances. -/
noncomputable def varMean (n : ℝ) (s2 C : ℝ) : ℝ := (n * s2 + C) / n ^ 2

/-- Independent case. -/
theorem independent_var (n : ℝ) (hn : n ≠ 0) (s2 : ℝ) :
    varMean n s2 0 = s2 / n := by
  unfold varMean
  field_simp [hn]
  ring

/-- Independent variance scales as 1/n: Var(n)/Var(m) = m/n. -/
theorem variance_ratio (n m : ℝ) (hn : n ≠ 0) (hm : m ≠ 0) (s2 : ℝ) (hs2 : s2 ≠ 0) :
    varMean n s2 0 / varMean m s2 0 = m / n := by
  rw [independent_var n hn s2, independent_var m hm s2]
  field_simp [hn, hm, hs2]

/-- With constant mean off-diagonal covariance c, C = n(n-1)c and the variance
has the lower bound (n-1)c/n, tending to c. -/
theorem correlated_floor (n c s2 : ℝ) (hn : 0 < n) (hs2 : 0 ≤ s2) :
    varMean n s2 (n * (n - 1) * c) ≥ (n - 1) * c / n := by
  unfold varMean
  have hnne : n ≠ 0 := ne_of_gt hn
  field_simp [hnne]
  nlinarith

/-- Relative variance with a covariance sum growing at most linearly:
R ≤ (s2 + k)/(n μ²), hence it tends to zero (self-averaging). -/
theorem self_avg_condition (n s2 C k : ℝ) (hn : 0 < n) (hC : C ≤ k * n) :
    varMean n s2 C ≤ (s2 + k) / n := by
  unfold varMean
  have hnne : n ≠ 0 := ne_of_gt hn
  field_simp [hnne]
  nlinarith

end CQM.SelfAveraging
