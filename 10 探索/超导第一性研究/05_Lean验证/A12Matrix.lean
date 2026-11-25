import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Finset.Max
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

open Matrix
open scoped BigOperators

/-!
# A12 matrix route: edge connection, circulation, and the non-gradient obstruction

The previous no-go theorem killed `C = I + f(ε_i - ε_j)` with `C1 = 1` and
`f` odd strictly monotone.  This file formalizes the algebraic alternative:
the generator is an oriented edge connection `a_ij`, not a node potential
difference.  The minimal nontrivial examples are the three- and four-node
directed circulations.  Both satisfy the global A12 condition and `C1 = 1`,
and both are divergence-free but **not** gradients.  The final theorem shows
why a gradient edge field with zero row sums must vanish.  This statement is
about the edge connection `B = C - I`, not about the proper-time history
`H_ij = τ_i - τ_j`; the proper-time history remains a pure gradient and is
not constrained by this theorem.
-/

/-- Oriented three-cycle edge connection `A = C - I`. -/
def Acirc3 (a : ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  Matrix.of fun i j =>
    if i = 0 then
      if j = 1 then a else if j = 2 then -a else 0
    else if i = 1 then
      if j = 2 then a else if j = 0 then -a else 0
    else
      if j = 0 then a else if j = 1 then -a else 0

/-- The three-node correlation matrix `C = I + A`. -/
abbrev Ccirc3 (a : ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  (1 : Matrix (Fin 3) (Fin 3) ℝ) + Acirc3 a

/-- Oriented four-cycle (plaquette) edge connection `A = C - I`. -/
def Acirc4 (a : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  Matrix.of fun i j =>
    if i = 0 then
      if j = 1 then a else if j = 3 then -a else 0
    else if i = 1 then
      if j = 2 then a else if j = 0 then -a else 0
    else if i = 2 then
      if j = 3 then a else if j = 1 then -a else 0
    else
      if j = 0 then a else if j = 2 then -a else 0

/-- The four-node correlation matrix `C = I + A`. -/
abbrev Ccirc4 (a : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  (1 : Matrix (Fin 4) (Fin 4) ℝ) + Acirc4 a

/-! ## Three-node circulation -/

lemma Acirc3_diag (a : ℝ) : ∀ i : Fin 3, Acirc3 a i i = 0 := by
  intro i
  fin_cases i <;> simp [Acirc3]

lemma Acirc3_antisymm (a : ℝ) :
    ∀ i j : Fin 3, Acirc3 a i j = - Acirc3 a j i := by
  intro i j
  fin_cases i <;> fin_cases j <;> simp [Acirc3]

lemma Acirc3_row_sum (a : ℝ) : ∀ i : Fin 3, ∑ j : Fin 3, Acirc3 a i j = 0 := by
  intro i
  fin_cases i <;> simp [Acirc3, Fin.sum_univ_three]

lemma Acirc3_global_zero (a : ℝ) :
    (∑ i : Fin 3, ∑ j : Fin 3, Acirc3 a i j) = 0 := by
  simp [Acirc3_row_sum a]

lemma Acirc3_loop_sum (a : ℝ) :
    Acirc3 a 0 1 + Acirc3 a 1 2 + Acirc3 a 2 0 = 3 * a := by
  simp [Acirc3]
  ring

lemma Ccirc3_diag (a : ℝ) : ∀ i : Fin 3, Ccirc3 a i i = 1 := by
  intro i
  simp [Ccirc3, Acirc3_diag a i]

lemma Ccirc3_row_sum (a : ℝ) : ∀ i : Fin 3, ∑ j : Fin 3, Ccirc3 a i j = 1 := by
  intro i
  fin_cases i <;> simp [Ccirc3, Acirc3, Fin.sum_univ_three]

lemma Ccirc3_offdiag_global_zero (a : ℝ) :
    (∑ i : Fin 3, ∑ j : Fin 3,
      if i = j then 0 else Ccirc3 a i j) = 0 := by
  have h : ∀ i j : Fin 3,
      (if i = j then 0 else Ccirc3 a i j) = Acirc3 a i j := by
    intro i j
    by_cases hij : i = j
    · subst j
      simp [Acirc3_diag a i]
    · simp [Ccirc3, hij]
  calc
    (∑ i : Fin 3, ∑ j : Fin 3,
      if i = j then 0 else Ccirc3 a i j)
        = ∑ i : Fin 3, ∑ j : Fin 3, Acirc3 a i j := by
          apply Finset.sum_congr rfl
          intro i _
          apply Finset.sum_congr rfl
          intro j _
          exact h i j
    _ = 0 := Acirc3_global_zero a

/-- A gradient loop has zero holonomy. -/
lemma gradient_loop_sum_zero3 (φ : Fin 3 → ℝ) :
    (φ 1 - φ 0) + (φ 2 - φ 1) + (φ 0 - φ 2) = 0 := by
  ring

lemma Acirc3_not_gradient (a : ℝ) (ha : a ≠ 0) :
    ¬ ∃ φ : Fin 3 → ℝ, ∀ i j : Fin 3, Acirc3 a i j = φ j - φ i := by
  rintro ⟨φ, hφ⟩
  have h01 := hφ 0 1
  have h12 := hφ 1 2
  have h20 := hφ 2 0
  simp [Acirc3] at h01 h12 h20
  have hloop : (φ 1 - φ 0) + (φ 2 - φ 1) + (φ 0 - φ 2) = 0 :=
    gradient_loop_sum_zero3 φ
  have ha0 : a = 0 := by linarith
  exact ha ha0

/-- A three-node matrix satisfying diagonal one, `C1 = 1`, global A12,
divergence-free `A`, and non-gradient circulation. -/
theorem A12_matrix_route_exists_three :
    (∀ i : Fin 3, Ccirc3 (1 : ℝ) i i = 1) ∧
    (∀ i : Fin 3, ∑ j : Fin 3, Ccirc3 (1 : ℝ) i j = 1) ∧
    ((∑ i : Fin 3, ∑ j : Fin 3,
      if i = j then 0 else Ccirc3 (1 : ℝ) i j) = 0) ∧
    (∀ i : Fin 3, ∑ j : Fin 3, Acirc3 (1 : ℝ) i j = 0) ∧
    (¬ ∃ φ : Fin 3 → ℝ,
      ∀ i j : Fin 3, Acirc3 (1 : ℝ) i j = φ j - φ i) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · exact Ccirc3_diag 1
  · exact Ccirc3_row_sum 1
  · exact Ccirc3_offdiag_global_zero 1
  · exact Acirc3_row_sum 1
  · exact Acirc3_not_gradient 1 one_ne_zero

/-! ## Four-node plaquette -/

lemma Acirc4_diag (a : ℝ) : ∀ i : Fin 4, Acirc4 a i i = 0 := by
  intro i
  fin_cases i <;> simp [Acirc4]

lemma Acirc4_antisymm (a : ℝ) :
    ∀ i j : Fin 4, Acirc4 a i j = - Acirc4 a j i := by
  intro i j
  fin_cases i <;> fin_cases j <;> simp [Acirc4]

lemma Acirc4_row_sum (a : ℝ) : ∀ i : Fin 4, ∑ j : Fin 4, Acirc4 a i j = 0 := by
  intro i
  fin_cases i <;> simp [Acirc4, Fin.sum_univ_four]

lemma Acirc4_global_zero (a : ℝ) :
    (∑ i : Fin 4, ∑ j : Fin 4, Acirc4 a i j) = 0 := by
  simp [Acirc4_row_sum a]

lemma Acirc4_loop_sum (a : ℝ) :
    Acirc4 a 0 1 + Acirc4 a 1 2 + Acirc4 a 2 3 + Acirc4 a 3 0 = 4 * a := by
  simp [Acirc4]
  ring

lemma Ccirc4_diag (a : ℝ) : ∀ i : Fin 4, Ccirc4 a i i = 1 := by
  intro i
  simp [Ccirc4, Acirc4_diag a i]

lemma Ccirc4_row_sum (a : ℝ) : ∀ i : Fin 4, ∑ j : Fin 4, Ccirc4 a i j = 1 := by
  intro i
  fin_cases i <;> simp [Ccirc4, Acirc4, Fin.sum_univ_four]

lemma Ccirc4_offdiag_global_zero (a : ℝ) :
    (∑ i : Fin 4, ∑ j : Fin 4,
      if i = j then 0 else Ccirc4 a i j) = 0 := by
  have h : ∀ i j : Fin 4,
      (if i = j then 0 else Ccirc4 a i j) = Acirc4 a i j := by
    intro i j
    by_cases hij : i = j
    · subst j
      simp [Acirc4_diag a i]
    · simp [Ccirc4, hij]
  calc
    (∑ i : Fin 4, ∑ j : Fin 4,
      if i = j then 0 else Ccirc4 a i j)
        = ∑ i : Fin 4, ∑ j : Fin 4, Acirc4 a i j := by
          apply Finset.sum_congr rfl
          intro i _
          apply Finset.sum_congr rfl
          intro j _
          exact h i j
    _ = 0 := Acirc4_global_zero a

lemma gradient_loop_sum_zero4 (φ : Fin 4 → ℝ) :
    (φ 1 - φ 0) + (φ 2 - φ 1) + (φ 3 - φ 2) + (φ 0 - φ 3) = 0 := by
  ring

lemma Acirc4_not_gradient (a : ℝ) (ha : a ≠ 0) :
    ¬ ∃ φ : Fin 4 → ℝ, ∀ i j : Fin 4, Acirc4 a i j = φ j - φ i := by
  rintro ⟨φ, hφ⟩
  have h01 := hφ 0 1
  have h12 := hφ 1 2
  have h23 := hφ 2 3
  have h30 := hφ 3 0
  simp [Acirc4] at h01 h12 h23 h30
  have hloop : (φ 1 - φ 0) + (φ 2 - φ 1) + (φ 3 - φ 2) + (φ 0 - φ 3) = 0 :=
    gradient_loop_sum_zero4 φ
  have ha0 : a = 0 := by linarith
  exact ha ha0

/-- A four-node plaquette satisfying diagonal one, `C1 = 1`, global A12,
divergence-free `A`, and non-gradient circulation. -/
theorem A12_matrix_route_exists_four :
    (∀ i : Fin 4, Ccirc4 (1 : ℝ) i i = 1) ∧
    (∀ i : Fin 4, ∑ j : Fin 4, Ccirc4 (1 : ℝ) i j = 1) ∧
    ((∑ i : Fin 4, ∑ j : Fin 4,
      if i = j then 0 else Ccirc4 (1 : ℝ) i j) = 0) ∧
    (∀ i : Fin 4, ∑ j : Fin 4, Acirc4 (1 : ℝ) i j = 0) ∧
    (¬ ∃ φ : Fin 4 → ℝ,
      ∀ i j : Fin 4, Acirc4 (1 : ℝ) i j = φ j - φ i) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · exact Ccirc4_diag 1
  · exact Ccirc4_row_sum 1
  · exact Ccirc4_offdiag_global_zero 1
  · exact Acirc4_row_sum 1
  · exact Acirc4_not_gradient 1 one_ne_zero

/-! ## The gradient obstruction -/

/-- If a gradient edge field has zero row sums, then every gradient difference
vanishes.  This is the matrix-route reason why `C1 = 1` cannot be carried by a
pure node potential for the edge connection `B`; it does not constrain the
proper-time history `H_ij = τ_i - τ_j`. -/
theorem gradient_row_zero_forces_zero
    {N : ℕ} [NeZero N] (φ : Fin N → ℝ)
    (hrow : ∀ i : Fin N, ∑ j : Fin N, (φ j - φ i) = 0) :
    ∀ i j : Fin N, φ j - φ i = 0 := by
  classical
  obtain ⟨i, _hi, hmax⟩ :=
    Finset.exists_max_image (Finset.univ : Finset (Fin N)) φ Finset.univ_nonempty
  have hnonpos : ∀ j : Fin N, φ j - φ i ≤ 0 := by
    intro j
    exact sub_nonpos.mpr (hmax j (Finset.mem_univ j))
  have hnonneg : ∀ j : Fin N, 0 ≤ -(φ j - φ i) := by
    intro j
    linarith [hnonpos j]
  have hsum_neg : (∑ j : Fin N, -(φ j - φ i)) = 0 := by
    rw [Finset.sum_neg_distrib]
    rw [hrow i]
    ring
  have hzero_neg : ∀ j : Fin N, -(φ j - φ i) = 0 := by
    have h' :=
      (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => hnonneg j)).mp hsum_neg
    intro j
    exact h' j (Finset.mem_univ j)
  intro i' j'
  have hij : φ j' - φ i = 0 := by
    linarith [hzero_neg j']
  have hii : φ i' - φ i = 0 := by
    linarith [hzero_neg i']
  linarith

/-- If a row-zero matrix is decomposed into a gradient plus a divergence-free
loop, then its gradient part must vanish.  Applied to fluctuations, this says:
if `δC` preserves `C1 = 1`, the node-potential (DM.5) part is killed and only
the loop variance can survive. -/
theorem rowZero_decomp_gradient_zero
    {N : ℕ} [NeZero N] (B : Matrix (Fin N) (Fin N) ℝ)
    (φ : Fin N → ℝ) (ω : Matrix (Fin N) (Fin N) ℝ)
    (hB : B = fun i j => (φ j - φ i) + ω i j)
    (hω : ∀ i : Fin N, ∑ j : Fin N, ω i j = 0)
    (hBrow : ∀ i : Fin N, ∑ j : Fin N, B i j = 0) :
    ∀ i j : Fin N, φ j - φ i = 0 := by
  have hgrad : ∀ i : Fin N, ∑ j : Fin N, (φ j - φ i) = 0 := by
    intro i
    have h := hBrow i
    rw [hB] at h
    simp [Finset.sum_add_distrib, hω i] at h
    simpa using h
  exact gradient_row_zero_forces_zero φ hgrad
