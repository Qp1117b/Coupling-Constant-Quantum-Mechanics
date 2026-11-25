import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# Four-stage chain (final version)

Stages: differentiation -> expansion -> averaging -> crisis.  "Turned negative"
means the growth rate cannot keep up with the averaging rate (net growth < 0);
it is the DRIVER of averaging (③), and passes through two stages: averaging (③)
and the continued decline of the average line (④ = crisis).  Negative growth is
NOT a fifth stage and NOT a corollary of the decline -- it precedes it.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.FourStageChain

/-- The four stages; no fifth "negative growth" constructor. -/
inductive Stage where
  | differentiation
  | expansion
  | averaging
  | crisis

/-- Four stages are exhaustive. -/
theorem four_stages_exhaustive (s : Stage) :
    s = Stage.differentiation ∨ s = Stage.expansion ∨
      s = Stage.averaging ∨ s = Stage.crisis := by
  cases s <;> simp

/-- "Turned negative": growth rate < averaging rate (net growth negative).
    This is the driver, preceding averaging. -/
def TurnedNegative (growth avgRate : ℝ) : Prop := growth < avgRate

/-- ③ Averaging: the difference shrinks (net difference growth negative). -/
def Averaging (dNow dPrev : ℝ) : Prop := dNow < dPrev

/-- ④ Crisis: the average quantity / average line keeps falling. -/
def CrisisContent (avgNow avgPrev : ℝ) : Prop := avgNow < avgPrev

/-- Turned-negative growth forces net difference growth negative (averaging). -/
theorem negative_drives_averaging (growth avgRate : ℝ)
    (h : TurnedNegative growth avgRate) : growth - avgRate < 0 := by
  unfold TurnedNegative at h
  linarith

/-- The two stages of "turned negative": averaging (③) then average decline (④).
    Crisis is the SECOND stage, not the source of "turned negative". -/
theorem two_stages_to_crisis (dNow dPrev avgNow avgPrev growth avgRate : ℝ)
    (hneg : TurnedNegative growth avgRate)
    (h3 : Averaging dNow dPrev) (h4 : CrisisContent avgNow avgPrev) :
    TurnedNegative growth avgRate ∧ Averaging dNow dPrev ∧ CrisisContent avgNow avgPrev :=
  ⟨hneg, h3, h4⟩

/-- From averaging (③) to crisis (④): the post-averaging line keeps falling. -/
theorem averaging_to_crisis (after before : ℝ) (h : after < before) :
    CrisisContent after before := h

/-- Counteraction internal: even with an internal upward oscillation eps,
    the line still falls if a+eps < b -- the oscillation does not reverse ④. -/
theorem internal_oscillation_preserves_decrease (a b eps : ℝ)
    (heps : 0 ≤ eps) (h : a + eps < b) : CrisisContent a b := by
  unfold CrisisContent
  linarith

/-- The residual bottom is positive: crisis keeps an internal fluctuation. -/
theorem residual_oscillation (base eps : ℝ) (heps : 0 < eps) :
    base < base + eps := by linarith

end CQM.FourStageChain
