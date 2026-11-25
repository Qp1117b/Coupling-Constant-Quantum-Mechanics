import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# `临-14`: necessary and sufficient condition for pre-transition freezing

From tau_i = integral v_tau,i and H_ij = tau_i - tau_j we get the discrete rate
Delta H_ij = v_i - v_j.  Hence all-pairs freezing is equivalent to the velocity
field being constant (the converse of (22.3)), and the freezing relation is an
equivalence relation whose connected components give partial freezing.
Three states (fluctuating / frozen-misaligned / aligned) are mutually exclusive.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.FrozenPremise

/-- Discrete rate of the pair holonomy: H_ij(t+1)-H_ij(t) = v_i - v_j. -/
def hDiff (v : Fin n → ℝ) (i j : Fin n) : ℝ := v i - v j

/-- The rate is literally the speed difference. -/
theorem rate_eq_speed_diff (v : Fin n → ℝ) (i j : Fin n) :
    hDiff v i j = v i - v j := rfl

/-- Pairwise freezing iff the two speeds coincide. -/
theorem pair_frozen_iff_speed_eq (v : Fin n → ℝ) (i j : Fin n) :
    hDiff v i j = 0 ↔ v i = v j := by
  unfold hDiff
  constructor <;> intro h <;> linarith

/-- All-pairs freezing implies a constant field (transitivity), the converse of (22.3). -/
theorem all_pairs_frozen_imp_constant {n : ℕ} (v : Fin n → ℝ)
    (h : ∀ i j : Fin n, hDiff v i j = 0) :
    ∃ c : ℝ, ∀ i : Fin n, v i = c := by
  by_cases hn : n = 0
  · subst n
    exact ⟨0, fun i => Fin.elim0 i⟩
  · have hpos : 0 < n := Nat.pos_of_ne_zero hn
    let i0 : Fin n := ⟨0, hpos⟩
    refine ⟨v i0, ?_⟩
    intro i
    have hi : hDiff v i i0 = 0 := h i i0
    unfold hDiff at hi
    linarith

/-- A constant field implies all-pairs freezing (the (22.3) direction). -/
theorem constant_imp_all_pairs_frozen {n : ℕ} (v : Fin n → ℝ)
    (c : ℝ) (hc : ∀ i : Fin n, v i = c) :
    ∀ i j : Fin n, hDiff v i j = 0 := by
  intro i j
  unfold hDiff
  rw [hc i, hc j]
  ring

/-- The freezing relation is an equivalence relation. -/
theorem frozen_relation_equivalence (v : Fin n → ℝ) :
    Equivalence (fun i j : Fin n => v i = v j) where
  refl _ := rfl
  symm h := h.symm
  trans h1 h2 := h1.trans h2

/-- State 1 (unpublic field) excludes pairwise freezing for that pair. -/
theorem state1_excludes_freezing (v : Fin n → ℝ) (i j : Fin n)
    (hv : v i ≠ v j) : hDiff v i j ≠ 0 := by
  unfold hDiff
  intro hz
  apply hv
  linarith

/-- State 2 (misaligned origins) excludes state 3 (c_ij = 0). -/
theorem state2_excludes_state3 (ai aj : ℝ) (h : ai ≠ aj) : ai - aj ≠ 0 := by
  intro hz
  apply h
  linarith

end CQM.FrozenPremise
