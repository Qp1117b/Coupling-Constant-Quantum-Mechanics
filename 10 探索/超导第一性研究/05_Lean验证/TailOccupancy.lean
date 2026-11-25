import Mathlib.Data.Real.Basic
import Mathlib.Order.Monotone.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp

/-!
# Tail occupancy from a monotone CDF

This file formalises the direction of the ring-15 readout

`p_pair(T) = 1 - F(k / V_coh(T))`,

where `F` is any monotone CDF and `k = n_cell * sigma_c^2`.
It does **not** prove that the physical local variance is chi-square; that
step is the Gaussian cell-variance assumption of
`03_推导工作台/环15_配对概率分布.md`, checked numerically.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.TailOccupancy

noncomputable section

/-- Upper tail of a monotone CDF: `1 - F u`. -/
def tailOccupancy (F : ℝ → ℝ) (u : ℝ) : ℝ :=
  1 - F u

/-- A larger threshold argument gives a smaller upper tail. -/
theorem tailOccupancy_antitone {F : ℝ → ℝ} (hF : Monotone F)
    {u₁ u₂ : ℝ} (hu : u₁ ≤ u₂) :
    tailOccupancy F u₂ ≤ tailOccupancy F u₁ := by
  unfold tailOccupancy
  linarith [hF hu]

/-- Pair occupancy with argument `k / V`. -/
def pairOccupancy (F : ℝ → ℝ) (k V : ℝ) : ℝ :=
  tailOccupancy F (k / V)

/-- If `V` decreases, `k/V` increases (for `k ≥ 0`, `V > 0`), so the upper
tail decreases.  This is the algebraic direction behind
`T ↓ => V_coh ↑ => p_pair ↑`. -/
theorem pairOccupancy_antitone {F : ℝ → ℝ} (hF : Monotone F)
    {k V₁ V₂ : ℝ} (hk : 0 ≤ k) (hV₂ : 0 < V₂)
    (hV : V₂ ≤ V₁) :
    pairOccupancy F k V₂ ≤ pairOccupancy F k V₁ := by
  unfold pairOccupancy
  apply tailOccupancy_antitone hF
  exact div_le_div_of_nonneg_left hk hV₂ hV

/-- A normalized threshold argument `k / (Z * w)`.  This is the form used
when `V_coh = Z * w(T)`. -/
def normalizedPairArgument (k Z w : ℝ) : ℝ :=
  k / (Z * w)

/-- If `w` decreases and `Z,k` are positive, the normalized argument
increases. -/
theorem normalizedPairArgument_antitone {k Z w₁ w₂ : ℝ}
    (hk : 0 ≤ k) (hZ : 0 < Z) (hw₁ : 0 < w₁) (hw₂ : 0 < w₂)
    (hw : w₂ ≤ w₁) :
    normalizedPairArgument k Z w₁ ≤ normalizedPairArgument k Z w₂ := by
  unfold normalizedPairArgument
  have hZV₁ : 0 < Z * w₁ := mul_pos hZ hw₁
  have hZV₂ : 0 < Z * w₂ := mul_pos hZ hw₂
  exact div_le_div_of_nonneg_left hk hZV₂ (mul_le_mul_of_nonneg_left hw hZ.le)

end

end CQM.TailOccupancy
