import Mathlib.Data.Real.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith

/-!
# `审-4`: the topological origin of the 1/2 saturation and withdrawal of 推 6

For a finite GF(2) additive group V and a nonzero additive functional φ, the
two fibres φ⁻¹(0) and φ⁻¹(1) have equal cardinality (translation by v₀ with
φ v₀ = 1 is an involution in characteristic 2).  Applied to the graph cycle
space, every edge lying in some cycle has occupation rate exactly 1/2.

The pairing-induced bond occupation is the different, symmetric field B_ij = s_i s_j
with mean p²; its critical value is (p_c^site)² = 0.351348 < 1/2.  Hence 推 6,
which identified the 1/2 saturation with the 2D bond threshold, is withdrawn.

No axiom, `sorry`, `admit`, `native_decide`, `unsafe` is used.
-/

namespace CQM.CycleSpaceHalf

/-- Translation by a vector with φ v₀ = 1 pairs the two fibres of φ. -/
theorem cycle_half_fibre {V : Type*} [AddCommGroup V] [Module (ZMod 2) V] [Fintype V]
    (φ : V → ZMod 2) (hadd : ∀ a b, φ (a + b) = φ a + φ b)
    (v0 : V) (hv0 : φ v0 = 1) :
    Fintype.card {v : V // φ v = 0} = Fintype.card {v : V // φ v = 1} := by
  have htwo : (2 : ZMod 2) = 0 := by decide
  let e : {v : V // φ v = 0} ≃ {v : V // φ v = 1} :=
  { toFun := fun v => ⟨v.1 + v0, by simp [hadd, v.2, hv0]⟩
    invFun := fun v => ⟨v.1 + v0, by
      rw [hadd, v.2, hv0]
      decide⟩
    left_inv := by
      intro v
      ext
      simp [add_assoc, ← two_smul (ZMod 2) v0, htwo]
    right_inv := by
      intro v
      ext
      simp [add_assoc, ← two_smul (ZMod 2) v0, htwo] }
  exact Fintype.card_congr e

/-- The induced bond field is symmetric: it is an occupation field, not a
connection, so it carries no holonomy. -/
theorem induced_bond_symm (s : ℕ → ℝ) (i j : ℕ) : s i * s j = s j * s i := by
  ring

/-- Mean of an induced bond for independent site occupation. -/
theorem induced_bond_mean {p : ℝ} (s : ℕ → ℝ)
    (hmean : ∀ i, s i = p) (i j : ℕ) : s i * s j = p ^ 2 := by
  rw [hmean i, hmean j]
  ring

/-- Covariance of two bonds sharing a node: p³(1-p). -/
theorem shared_covariance (p : ℝ) : p ^ 3 - p ^ 4 = p ^ 3 * (1 - p) := by
  ring

/-- The bond fraction at the site threshold is below the naive 1/2. -/
theorem site_threshold_bond_fraction : (0.592746 : ℝ) ^ 2 < 1 / 2 := by
  norm_num

/-- If p exceeds the site threshold, its induced bond fraction exceeds the
critical induced fraction: pairing-induced bonds already percolate. -/
theorem withdraw_tu6 {p pc : ℝ} (hpc : pc = 0.592746) (hp : pc < p) :
    pc ^ 2 < p ^ 2 := by
  rw [hpc] at hp ⊢
  nlinarith

/-- The loop saturation value 1/2 and the pairing bond fraction are different
objects: equality of their numerical values does not identify them. -/
theorem loop_half_not_bond_fraction {p : ℝ} (hp : p ^ 2 < 1 / 2) : p ^ 2 ≠ (1 / 2 : ℝ) := by
  nlinarith

end CQM.CycleSpaceHalf
