import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# `临-21`: effective point count n_eff as a participation ratio

The capacity constraint sum_k n_k <= n_eff in (16.1) is given a structure:
n_eff is the participation ratio 1 / sum_i p_i^2 of a normalized weight p on a
finite support.  Elementary bounds 1 <= n_eff <= |supp p| are proved, with
equality at uniform weights.  Splitting a weight never decreases n_eff, while
filtering can decrease it, so the three candidate definitions (space / energy /
Fermi-shell) have no general order.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.EffectiveCount

/-- Participation ratio (effective number of points) of normalized weights p on s. -/
noncomputable def pr {α : Type*} [DecidableEq α] (s : Finset α) (p : α → ℝ) : ℝ :=
  1 / Finset.sum s (fun i => (p i) ^ 2)

/-- Weight hypothesis: nonnegative, normalized to one, nonempty support. -/
def IsWeight {α : Type*} (s : Finset α) (p : α → ℝ) : Prop :=
  (∀ i ∈ s, 0 ≤ p i) ∧ (Finset.sum s (fun i => p i) = 1) ∧ s.Nonempty

/-- Sum of squares is positive for a normalized nonnegative weight. -/
theorem sum_sq_pos {α : Type*} [DecidableEq α] {s : Finset α} {p : α → ℝ}
    (hsum : Finset.sum s (fun i => p i) = 1) :
    0 < Finset.sum s (fun i => (p i) ^ 2) := by
  by_contra h
  have hle : Finset.sum s (fun i => (p i) ^ 2) ≤ 0 := le_of_not_gt h
  have hnonneg : 0 ≤ Finset.sum s (fun i => (p i) ^ 2) :=
    Finset.sum_nonneg (fun i hi => sq_nonneg (p i))
  have hzero : Finset.sum s (fun i => (p i) ^ 2) = 0 := le_antisymm hle hnonneg
  have hp_zero : ∀ i ∈ s, p i = 0 := by
    intro i hi
    have ht : (p i) ^ 2 ≤ Finset.sum s (fun j => (p j) ^ 2) :=
      Finset.single_le_sum (fun j hj => sq_nonneg (p j)) hi
    nlinarith
  have hz : Finset.sum s (fun i => p i) = 0 := by
    apply Finset.sum_eq_zero
    intro i hi
    exact hp_zero i hi
  linarith

/-- Lower bound: n_eff >= 1. -/
theorem pr_lower {α : Type*} [DecidableEq α] {s : Finset α} {p : α → ℝ}
    (hw : IsWeight s p) : 1 ≤ pr s p := by
  rcases hw with ⟨hp0, hsum, hne⟩
  unfold pr
  have hpi_le_one : ∀ i ∈ s, p i ≤ 1 := by
    intro i hi
    have ht : p i ≤ Finset.sum s (fun j => p j) :=
      Finset.single_le_sum (fun j hj => hp0 j hj) hi
    simpa [hsum] using ht
  have hsq_le_one : Finset.sum s (fun i => (p i) ^ 2) ≤ 1 := by
    calc
      Finset.sum s (fun i => (p i) ^ 2) ≤ Finset.sum s (fun i => p i) := by
        apply Finset.sum_le_sum
        intro i hi
        have h0 := hp0 i hi
        have h1 := hpi_le_one i hi
        nlinarith [mul_nonneg h0 (sub_nonneg.mpr h1)]
      _ = 1 := hsum
  have hpos : 0 < Finset.sum s (fun i => (p i) ^ 2) := sum_sq_pos hsum
  exact (le_div_iff₀ hpos).mpr (by simpa using hsq_le_one)

/-- Upper bound: n_eff <= |supp p|, via (p_i - 1/N)^2 >= 0. -/
theorem pr_upper {α : Type*} [DecidableEq α] {s : Finset α} {p : α → ℝ}
    (hw : IsWeight s p) : pr s p ≤ (s.card : ℝ) := by
  rcases hw with ⟨hp0, hsum, hne⟩
  unfold pr
  have hcard_pos_nat : 0 < s.card := hne.card_pos
  have hcard_pos : (0 : ℝ) < s.card := by exact_mod_cast hcard_pos_nat
  let c : ℝ := s.card
  have hcpos : 0 < c := by simpa [c] using hcard_pos
  have hterm : ∀ i ∈ s, (2 : ℝ) * p i / c - 1 / c ^ 2 ≤ (p i) ^ 2 := by
    intro i hi
    have hsq := sq_nonneg (p i - 1 / c)
    field_simp [hcpos.ne'] at hsq ⊢
    nlinarith
  have hsum_term := Finset.sum_le_sum hterm
  have h1 : Finset.sum s (fun i => (2 : ℝ) * p i / c) = 2 / c := by
    simp_rw [div_eq_mul_inv]
    rw [← Finset.sum_mul]
    rw [← Finset.mul_sum]
    rw [hsum]
    ring
  have h2 : Finset.sum s (fun _ => (1 : ℝ) / c ^ 2) = (s.card : ℝ) * (1 / c ^ 2) := by
    rw [Finset.sum_const]
    norm_num
  have hleft : Finset.sum s (fun i => (2 : ℝ) * p i / c - 1 / c ^ 2) = 1 / c := by
    rw [Finset.sum_sub_distrib, h1, h2]
    simp only [c]
    field_simp [hcard_pos.ne']
    ring
  have hq_ge : 1 / c ≤ Finset.sum s (fun i => (p i) ^ 2) := by
    rwa [hleft] at hsum_term
  have hpos : 0 < Finset.sum s (fun i => (p i) ^ 2) := sum_sq_pos hsum
  rw [div_le_iff₀ hpos]
  have hmul := mul_le_mul_of_nonneg_left hq_ge (le_of_lt hcpos)
  field_simp [hcpos.ne'] at hmul
  nlinarith

/-- Uniform weights saturate the upper bound: n_eff = |s|. -/
theorem pr_uniform (n : ℕ) (hn : 0 < n) :
    pr (Finset.univ : Finset (Fin n)) (fun _ => (1 : ℝ) / (n : ℝ)) = (n : ℝ) := by
  unfold pr
  have hnpos : (0 : ℝ) < n := by exact_mod_cast hn
  simp [Finset.sum_const]
  field_simp [hnpos.ne']

/-- Splitting a weight never decreases n_eff: u^2+v^2 >= (u+v)^2/2. -/
theorem split_sq_ge (u v : ℝ) : (u + v) ^ 2 / 2 ≤ u ^ 2 + v ^ 2 := by
  nlinarith [sq_nonneg (u - v)]

/-- Filtering can decrease n_eff: two-point support gives 1/(p^2+(1-p)^2) <= 2. -/
theorem pr_two_le_two (p : ℝ) : 1 / (p ^ 2 + (1 - p) ^ 2) ≤ 2 := by
  have hpos : 0 < p ^ 2 + (1 - p) ^ 2 := by nlinarith [sq_nonneg p, sq_nonneg (1 - p)]
  rw [div_le_iff₀ hpos]
  nlinarith [sq_nonneg (p - 1 / 2)]

end CQM.EffectiveCount
