import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

open Matrix

/-!
# Proper-time history vs U(1) phase connection

This file separates two objects that the main text denotes by the same symbol
`H`:

* `properTimeH τ i j = τ i - τ j` is the proper-time history.  It is a pure
  gradient and satisfies the cocycle identity; every closed loop has zero sum.
* `phaseTheta3 α a` is a U(1) phase connection on a three-cycle.  It can have
  nonzero loop holonomy and is **not** a gradient when `α * a ≠ 0`.

The conclusion is formal: a nonzero phase connection cannot be identified with
the proper-time history.  The physical identification `θ = α λ` is a candidate
of the main text, not a theorem of this file.
-/

/-- Proper-time history `H_ij = τ i - τ j`, matching 06. -/
def properTimeH {N : Type*} (τ : N → ℝ) (i j : N) : ℝ := τ i - τ j

/-- The proper-time history satisfies the cocycle identity. -/
lemma properTimeH_cocycle {N : Type*} (τ : N → ℝ) (i j k : N) :
    properTimeH τ i j + properTimeH τ j k = properTimeH τ i k := by
  unfold properTimeH
  ring

/-- Every three-node closed loop of the proper-time history has zero holonomy. -/
lemma properTimeH_loop_sum_zero3 (τ : Fin 3 → ℝ) :
    properTimeH τ 0 1 + properTimeH τ 1 2 + properTimeH τ 2 0 = 0 := by
  unfold properTimeH
  ring

/-- A three-node U(1) phase connection with oriented edge amplitude `α * a`. -/
def phaseTheta3 (α a : ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  Matrix.of fun i j =>
    if i = 0 then
      if j = 1 then α * a else if j = 2 then -(α * a) else 0
    else if i = 1 then
      if j = 2 then α * a else if j = 0 then -(α * a) else 0
    else
      if j = 0 then α * a else if j = 1 then -(α * a) else 0

lemma phaseTheta3_antisymm (α a : ℝ) :
    ∀ i j : Fin 3, phaseTheta3 α a i j = - phaseTheta3 α a j i := by
  intro i j
  fin_cases i <;> fin_cases j <;> simp [phaseTheta3]

lemma phaseTheta3_loop_sum (α a : ℝ) :
    phaseTheta3 α a 0 1 + phaseTheta3 α a 1 2 + phaseTheta3 α a 2 0
      = 3 * (α * a) := by
  simp [phaseTheta3]
  ring

/-- A gradient loop has zero holonomy. -/
lemma gradient_loop_sum_zero3 (φ : Fin 3 → ℝ) :
    (φ 1 - φ 0) + (φ 2 - φ 1) + (φ 0 - φ 2) = 0 := by
  ring

/-- A nonzero phase connection is not a gradient. -/
lemma phaseTheta3_not_gradient (α a : ℝ) (hα : α ≠ 0) (ha : a ≠ 0) :
    ¬ ∃ φ : Fin 3 → ℝ,
      ∀ i j : Fin 3, phaseTheta3 α a i j = φ j - φ i := by
  rintro ⟨φ, hφ⟩
  have h01 := hφ 0 1
  have h12 := hφ 1 2
  have h20 := hφ 2 0
  have hloop : phaseTheta3 α a 0 1 + phaseTheta3 α a 1 2
      + phaseTheta3 α a 2 0 = 3 * (α * a) := phaseTheta3_loop_sum α a
  have hgrad : (φ 1 - φ 0) + (φ 2 - φ 1) + (φ 0 - φ 2) = 0 :=
    gradient_loop_sum_zero3 φ
  have hphase_zero :
      phaseTheta3 α a 0 1 + phaseTheta3 α a 1 2 + phaseTheta3 α a 2 0 = 0 := by
    rw [h01, h12, h20]
    exact hgrad
  have hzero : 3 * (α * a) = 0 := by linarith
  have hprod : α * a = 0 := by
    have h3 : (3 : ℝ) ≠ 0 := by norm_num
    exact (mul_eq_zero.mp hzero).resolve_left h3
  exact (mul_ne_zero hα ha) hprod

/-- The proper-time history is a gradient; the phase connection need not be. -/
theorem properTime_gradient_and_phase_not_gradient
    (τ : Fin 3 → ℝ) (α a : ℝ) (hα : α ≠ 0) (ha : a ≠ 0) :
    (∀ i j : Fin 3, properTimeH τ i j = τ i - τ j) ∧
    (properTimeH τ 0 1 + properTimeH τ 1 2 + properTimeH τ 2 0 = 0) ∧
    (¬ ∃ φ : Fin 3 → ℝ,
      ∀ i j : Fin 3, phaseTheta3 α a i j = φ j - φ i) := by
  refine ⟨?_, ?_, ?_⟩
  · intro i j
    rfl
  · exact properTimeH_loop_sum_zero3 τ
  · exact phaseTheta3_not_gradient α a hα ha
