import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Order.Monotone.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.GCongr
import Mathlib.Tactic.FieldSimp

/-!
# Coherent / incoherent split of the curvature variance

This file formalises the algebraic core of
`03_推导工作台/环09_相干热分裂.md`.

The physical identification is **not** proved here.  We only prove:

1. `totalVar Z n = Z + incoherentVar Z n`;
2. `coherentVar Z n * totalVar Z n = Z^2` (for nonzero denominator);
3. `coherentVar` is antitone in the Bose occupation `n`;
4. `incoherentVar` is monotone in `n`.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.CoherentThermalSplit

noncomputable section

/-- Total mean-square curvature fluctuation:
`Z (1 + 2 n_B)`.  This is the object that grows with temperature. -/
def totalVar (Z n : ℝ) : ℝ :=
  Z * (1 + 2 * n)

/-- Coherent second moment: `Z / (1 + 2 n_B)`.
This is the object that decreases with temperature and is the candidate
for the coherent part entering DM.5 / DM.9. -/
def coherentVar (Z n : ℝ) : ℝ :=
  Z / (1 + 2 * n)

/-- Incoherent thermal part: `2 Z n_B`.
This is the part that grows with temperature and is the candidate
for the dephasing channel. -/
def incoherentVar (Z n : ℝ) : ℝ :=
  Z * (2 * n)

/-- The total variance is the zero-point part plus the incoherent part. -/
theorem total_eq_zero_add_incoherent (Z n : ℝ) :
    totalVar Z n = Z + incoherentVar Z n := by
  unfold totalVar incoherentVar
  ring

/-- The coherent second moment is positive when `Z` is nonnegative and
the denominator is positive. -/
theorem coherentVar_nonneg {Z n : ℝ} (hZ : 0 ≤ Z) (hn : 0 ≤ n) :
    0 ≤ coherentVar Z n := by
  unfold coherentVar
  positivity

/-- The incoherent part is nonnegative under the same hypotheses. -/
theorem incoherentVar_nonneg {Z n : ℝ} (hZ : 0 ≤ Z) (hn : 0 ≤ n) :
    0 ≤ incoherentVar Z n := by
  unfold incoherentVar
  positivity

/-- The coherent second moment is antitone in the Bose occupation. -/
theorem coherentVar_antitone {Z n₁ n₂ : ℝ}
    (hZ : 0 ≤ Z) (hn₁ : 0 ≤ n₁) (hn : n₁ ≤ n₂) :
    coherentVar Z n₂ ≤ coherentVar Z n₁ := by
  unfold coherentVar
  have hden₁ : 0 < 1 + 2 * n₁ := by linarith
  have hden₂ : 0 < 1 + 2 * n₂ := by linarith
  gcongr

/-- The incoherent part is monotone in the Bose occupation. -/
theorem incoherentVar_mono {Z n₁ n₂ : ℝ}
    (hZ : 0 ≤ Z) (hn : n₁ ≤ n₂) :
    incoherentVar Z n₁ ≤ incoherentVar Z n₂ := by
  unfold incoherentVar
  nlinarith

/-- The product of the coherent and total variances is `Z^2`. -/
theorem coherent_mul_total {Z n : ℝ} (hden : 1 + 2 * n ≠ 0) :
    coherentVar Z n * totalVar Z n = Z ^ 2 := by
  unfold coherentVar totalVar
  field_simp [hden]

/-- Equivalent form: the coherent second moment is `Z^2 / totalVar`. -/
theorem coherent_eq_sq_div_total {Z n : ℝ}
    (hZ : Z ≠ 0) (hden : 1 + 2 * n ≠ 0) :
    coherentVar Z n = Z ^ 2 / totalVar Z n := by
  unfold coherentVar totalVar
  field_simp [hZ, hden]

/-- The node-only Josephson weight `V_coh / Z`.  It is normalized to `1`
at `T = 0` and is antitone as the coherent part decreases. -/
def nodeJosephsonWeight (Z V : ℝ) : ℝ :=
  V / Z

/-- At `V = Z`, the node-only Josephson weight is `1`. -/
theorem nodeJosephsonWeight_zero {Z : ℝ} (hZ : Z ≠ 0) :
    nodeJosephsonWeight Z Z = 1 := by
  unfold nodeJosephsonWeight
  field_simp [hZ]

/-- If the coherent part decreases, the node-only Josephson weight decreases. -/
theorem nodeJosephsonWeight_mono {Z V₁ V₂ : ℝ}
    (hZ : 0 < Z) (h : V₁ ≤ V₂) :
    nodeJosephsonWeight Z V₁ ≤ nodeJosephsonWeight Z V₂ := by
  unfold nodeJosephsonWeight
  exact div_le_div_of_nonneg_right h hZ.le

end

end CQM.CoherentThermalSplit
