import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic

open scoped Matrix

namespace Test

noncomputable def neutronDefectCartan (delta : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![2, -1, 0, 0; -1, 2, -1, 0; 0, -1, 2, -delta; 0, 0, -delta, 2]

@[simp] theorem succAbove_two_zero : (2 : Fin 4).succAbove 0 = (0 : Fin 4) := by decide
@[simp] theorem succAbove_two_one : (2 : Fin 4).succAbove 1 = (1 : Fin 4) := by decide
@[simp] theorem succAbove_two_two : (2 : Fin 4).succAbove 2 = (3 : Fin 4) := by decide
@[simp] theorem succAbove_three_zero : (3 : Fin 4).succAbove 0 = (0 : Fin 4) := by decide
@[simp] theorem succAbove_three_one : (3 : Fin 4).succAbove 1 = (1 : Fin 4) := by decide
@[simp] theorem succAbove_three_two : (3 : Fin 4).succAbove 2 = (2 : Fin 4) := by decide

/-- D(δ) 的行列式 -/
theorem neutronDefectCartan_det (delta : ℝ) :
    (neutronDefectCartan delta).det = 8 - 3 * delta ^ 2 := by
  unfold neutronDefectCartan
  rw [Matrix.det_succ_column
    (!![2, -1, 0, 0; -1, 2, -1, 0; 0, -1, 2, -delta; 0, 0, -delta, 2]) (3 : Fin 4)]
  simp only [Fin.sum_univ_four]
  norm_num [Matrix.det_fin_three, Matrix.submatrix_apply, Matrix.cons_val_zero,
    Matrix.cons_val_one, Matrix.cons_val_two, Matrix.cons_val_three]
  ring

noncomputable def neutronCartan (eps : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  fun i j => (!![2, -1, 0, 0; -1, 2, -1, 0; 0, -1, 2, -1; 0, 0, -1, 2] : Matrix (Fin 4) (Fin 4) ℝ) i j - (if i = 0 ∧ j = 0 then eps else 0)

theorem neutronCartan_eq_explicit (eps : ℝ) :
    neutronCartan eps = !![(2 - eps), -1, 0, 0; -1, 2, -1, 0; 0, -1, 2, -1; 0, 0, -1, 2] := by
  ext i j <;> fin_cases i <;> fin_cases j <;> simp [neutronCartan]

/-- C_n(ε) 的行列式 -/
theorem neutronCartan_det (eps : ℝ) : (neutronCartan eps).det = 5 - 4 * eps := by
  rw [neutronCartan_eq_explicit]
  rw [Matrix.det_succ_column
    (!![(2 - eps), -1, 0, 0; -1, 2, -1, 0; 0, -1, 2, -1; 0, 0, -1, 2]) (3 : Fin 4)]
  simp only [Fin.sum_univ_four]
  norm_num [Matrix.det_fin_three, Matrix.submatrix_apply, Matrix.cons_val_zero,
    Matrix.cons_val_one, Matrix.cons_val_two, Matrix.cons_val_three]
  ring

end Test
