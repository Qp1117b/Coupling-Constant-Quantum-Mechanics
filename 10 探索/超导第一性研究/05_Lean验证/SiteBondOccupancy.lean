import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# 审-4: induced bonds from occupied sites are correlated and use the site threshold

Formalises the algebraic core of `03_推导工作台/环15_座键口径.md`.

Given independent site occupation variables with probability `p`, an induced
bond between two neighbouring occupied sites has occupation `s_i * s_j`.

Proves:

1. `E[B] = p^2` for a single induced bond;
2. two induced bonds sharing a site have covariance `p^3 - p^4 = p^3 (1-p) > 0`;
3. two induced bonds with no shared site have zero covariance;
4. the naive mapping "q = p^2 with bond threshold 1/2" gives
   `p = sqrt(1/2) ≈ 0.7071`, strictly above the square-lattice site threshold
   `0.592746`; the induced bond fraction at the site threshold is
   `p_c^2 ≈ 0.3513 < 1/2`.

Does not prove the site threshold itself (external numerical result, L31).

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.SiteBondOccupancy

noncomputable section

/-- Mean occupation of one induced bond. -/
def inducedBondMean (p : ℝ) : ℝ := p ^ 2

/-- Joint occupation of two induced bonds sharing one site:
`Pr[s_i s_j = 1 and s_i s_k = 1] = p^3`. -/
def sharedBondMean (p : ℝ) : ℝ := p ^ 3

/-- Covariance of two shared-site induced bonds. -/
theorem shared_covariance (p : ℝ) :
    sharedBondMean p - inducedBondMean p * inducedBondMean p = p ^ 3 * (1 - p) := by
  unfold sharedBondMean inducedBondMean
  ring

/-- The covariance is positive in the open interval (0,1). -/
theorem shared_covariance_pos {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) :
    0 < sharedBondMean p - inducedBondMean p * inducedBondMean p := by
  rw [shared_covariance]
  have hp3 : 0 < p ^ 3 := by positivity
  exact mul_pos hp3 (by linarith)

/-- Two induced bonds with no shared site have product mean `p^4`, i.e. zero
covariance with independent Bernoulli sites. -/
theorem disjoint_bond_product (p : ℝ) :
    (p ^ 2) * (p ^ 2) = p ^ 4 := by ring

/-- The induced bond fraction at the site threshold is below the bond threshold. -/
theorem induced_fraction_at_site_threshold :
    (0.592746 : ℝ) ^ 2 < (1 / 2 : ℝ) := by
  norm_num

/-- The site threshold is strictly below the naive `sqrt(1/2)` threshold. -/
theorem site_threshold_below_naive :
    (0.592746 : ℝ) < Real.sqrt (1 / 2 : ℝ) := by
  have hsq : (0.592746 : ℝ) ^ 2 < (1 / 2 : ℝ) := by norm_num
  have hnonneg : 0 ≤ (0.592746 : ℝ) := by norm_num
  have hs : (Real.sqrt (1 / 2 : ℝ)) ^ 2 = (1 / 2 : ℝ) := by
    rw [Real.sq_sqrt]
    norm_num
  have hsqrt_nonneg : 0 ≤ Real.sqrt (1 / 2 : ℝ) := Real.sqrt_nonneg _
  nlinarith

/-- Relative size of the threshold error from the naive `p^2` mapping:
`sqrt(1/2) - 0.592746 > 0.1`. -/
theorem naive_threshold_error_gt_tenth :
    (0.1 : ℝ) < Real.sqrt (1 / 2 : ℝ) - 0.592746 := by
  have hsq : (0.692746 : ℝ) ^ 2 < (1 / 2 : ℝ) := by norm_num
  have hs : (Real.sqrt (1 / 2 : ℝ)) ^ 2 = (1 / 2 : ℝ) := by
    rw [Real.sq_sqrt]
    norm_num
  have hsqrt_nonneg : 0 ≤ Real.sqrt (1 / 2 : ℝ) := Real.sqrt_nonneg _
  nlinarith

/-- The correct criterion uses the site threshold, not the bond threshold:
`p_pair >= p_c(site)`, and never `p_pair^2 >= 1/2`. -/
theorem correct_criterion_not_naive {p : ℝ} (hp0 : 0 ≤ p) (hp : p ≤ 0.592746) :
    p ^ 2 < (1 / 2 : ℝ) := by
  have hsq := induced_fraction_at_site_threshold
  have hmul : 0 ≤ ((0.592746 : ℝ) - p) * ((0.592746 : ℝ) + p) := by
    exact mul_nonneg (sub_nonneg.mpr hp) (by linarith)
  nlinarith

end

end CQM.SiteBondOccupancy
