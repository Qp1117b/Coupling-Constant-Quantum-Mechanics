import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# `临-4`: (20.2) is necessary but not sufficient

Three-point counterexample: tau=(1,-1,0), v=(0,0,1) gives dDot D = 0
while v_1 != v_3.  Hence stationarity of the differentiation degree does NOT
imply all-pairs freezing -- sufficiency fails (not merely unproved).

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.CriterionSufficiency

/-- Three-point rate: dot D = 2 sum_{i<j} (tau_i-tau_j)(v_i-v_j). -/
def dDot3 (tau v : Fin 3 → ℝ) : ℝ :=
  2 * ((tau 0 - tau 1) * (v 0 - v 1) + (tau 0 - tau 2) * (v 0 - v 2) +
        (tau 1 - tau 2) * (v 1 - v 2))

/-- Counterexample: dDot D = 0 but v_1 != v_3. -/
theorem three_point_counterexample :
    let tau : Fin 3 → ℝ := fun i => if (i : ℕ) = 0 then 1 else if (i : ℕ) = 1 then -1 else 0
    let v : Fin 3 → ℝ := fun i => if (i : ℕ) = 2 then 1 else 0
    dDot3 tau v = 0 ∧ v 0 ≠ v 2 := by
  constructor
  · norm_num [dDot3]
  · norm_num

/-- Necessary direction: all-pairs freezing gives dDot D = 0. -/
theorem frozen_implies_stationary (tau v : Fin 3 → ℝ)
    (h : ∀ i j : Fin 3, v i = v j) : dDot3 tau v = 0 := by
  unfold dDot3
  have h01 : v 0 = v 1 := h 0 1
  have h12 : v 1 = v 2 := h 1 2
  rw [h01, ← h12]
  ring

/-- Necessary but NOT sufficient: stationarity does not force all-pairs freezing. -/
theorem necessary_not_sufficient :
    ¬ (∀ (tau v : Fin 3 → ℝ), dDot3 tau v = 0 → ∀ i j : Fin 3, v i = v j) := by
  intro h
  let tau : Fin 3 → ℝ := fun i => if (i : ℕ) = 0 then 1 else if (i : ℕ) = 1 then -1 else 0
  let v : Fin 3 → ℝ := fun i => if (i : ℕ) = 2 then 1 else 0
  have hd : dDot3 tau v = 0 := by
    dsimp [tau, v, dDot3]
    norm_num
  have hall := h tau v hd
  have hv02 : v 0 = v 2 := hall 0 2
  dsimp [v] at hv02
  norm_num at hv02

end CQM.CriterionSufficiency
