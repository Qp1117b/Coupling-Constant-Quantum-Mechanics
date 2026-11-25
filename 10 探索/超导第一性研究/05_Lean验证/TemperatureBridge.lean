import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Order.Monotone.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith

/-!
# Temperature bridge: coherent variance -> bond stiffness -> phase stiffness

This file formalises the algebraic bridge of
`03_推导工作台/环10_温度桥与刚度.md`.

It does **not** prove the Debye integral or the physical identification of
`V_coh` with the DM.5 amplitude.  It proves only:

1. a uniform rescaling of the aggregate bond sum rescales the phase stiffness
   by the same factor;
2. the normalized coherent weight `V_coh / Z` is one at `V_coh = Z` and is
   antitone when `V_coh` is antitone;
3. any monotone readout of the coherent amplitude preserves the temperature
   direction;
4. for positive exponent `t`, the percolation readout `p^t` preserves the
   same direction.

The aggregate bond sum is kept abstract on purpose: the current Mathlib build
does not contain the `Finset` big-operator module, and the bridge theorem only
needs linearity, not an explicit summation.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.TemperatureBridge

noncomputable section

/-- Phase stiffness read from an aggregate bond sum:
`(1/(2A)) * bondSum`, where `bondSum = sum_i J_i r_i^2`.
The geometry `r_i` is held fixed; only the bond stiffness carries the
temperature dependence. -/
def stiffnessFromBondSum (A bondSum : ℝ) : ℝ :=
  (1 / (2 * A)) * bondSum

/-- If the aggregate bond sum is multiplied by `w`, the phase stiffness is
multiplied by `w`.  This is the algebraic content of
`Upsilon(T) = Upsilon_0 * w(T)` under the factorization readout of DM.9. -/
theorem stiffness_rescale (A w bondSum : ℝ) :
    stiffnessFromBondSum A (w * bondSum) =
      w * stiffnessFromBondSum A bondSum := by
  unfold stiffnessFromBondSum
  ring

/-- A single bond term `J * r^2` rescales linearly. -/
def bondTerm (J r : ℝ) : ℝ :=
  J * r ^ 2

/-- A single bond term rescales by the same factor as `J`. -/
theorem bondTerm_rescale (J r w : ℝ) :
    bondTerm (J * w) r = w * bondTerm J r := by
  unfold bondTerm
  ring

/-- The normalized coherent weight `V_coh / Z`.  It is the object that
replaces the single-mode `tanh(theta_D / 2T)` in the multi-mode Debye readout. -/
def normalizedCoherent (Z V : ℝ) : ℝ :=
  V / Z

/-- At `V_coh = Z` the normalized coherent weight is one. -/
theorem normalizedCoherent_zero {Z : ℝ} (hZ : Z ≠ 0) :
    normalizedCoherent Z Z = 1 := by
  unfold normalizedCoherent
  field_simp [hZ]

/-- If the coherent second moment decreases, the normalized weight decreases. -/
theorem normalizedCoherent_antitone {Z V₁ V₂ : ℝ} (hZ : 0 < Z)
    (h : V₂ ≤ V₁) :
    normalizedCoherent Z V₂ ≤ normalizedCoherent Z V₁ := by
  unfold normalizedCoherent
  exact div_le_div_of_nonneg_right h hZ.le

/-- The phase stiffness under the coherent rescaling of the aggregate bond
sum. -/
theorem stiffness_coherent (A Z V bondSum : ℝ) :
    stiffnessFromBondSum A (normalizedCoherent Z V * bondSum) =
      normalizedCoherent Z V * stiffnessFromBondSum A bondSum := by
  exact stiffness_rescale A (normalizedCoherent Z V) bondSum

/-- A generic monotone readout of the coherent amplitude.  `F` can be any
CDF-like function; the theorem only uses monotonicity, not a distribution. -/
def pairReadout (F : ℝ → ℝ) (V : ℝ) : ℝ :=
  F (Real.sqrt V)

/-- If `V_coh` is antitone in temperature and nonnegative, any monotone
readout of its square root is antitone.  This fixes the direction of
`p_pair(T)` without assuming a particular disorder distribution. -/
theorem pairReadout_antitone {F : ℝ → ℝ} (hF : Monotone F)
    {V : ℝ → ℝ} (hV : Antitone V) :
    Antitone (fun T => pairReadout F (V T)) := by
  intro T₁ T₂ hT
  unfold pairReadout
  apply hF
  exact Real.sqrt_le_sqrt (hV hT)

/-- The percolation readout `p_sync = p_pair^t` preserves the direction for
positive `t`.  The exponent `t` itself remains an open parameter. -/
theorem pSync_antitone {p : ℝ → ℝ} (hp : Antitone p)
    (hpnonneg : ∀ T, 0 ≤ p T) {t : ℝ} (ht : 0 < t) :
    Antitone (fun T => (p T) ^ t) := by
  intro T₁ T₂ hT
  exact Real.rpow_le_rpow (hpnonneg T₂) (hp hT) ht.le

end

end CQM.TemperatureBridge
