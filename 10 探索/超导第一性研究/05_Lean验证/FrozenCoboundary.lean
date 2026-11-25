import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Positivity

/-!
# `临-17`: frozen offsets are a 1-coboundary

At freezing, c_ij = τ_i - τ_j = a_i - a_j.  Hence c_ji = -c_ij and
c_ij + c_jk = c_ik; for N nodes only N-1 parameters are independent.
The coherent fraction is the characteristic function R_n = |⟨e^{iγ_n a}⟩|,
which for Gaussian a is exp(-γ_n²σ_a²/2).

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.FrozenCoboundary

/-- Frozen offset from node freeze-times. -/
noncomputable def cFromA (a : Fin 3 → ℝ) (i j : Fin 3) : ℝ := a i - a j

/-- Antisymmetry. -/
theorem c_antisymm (a : Fin 3 → ℝ) : ∀ i j : Fin 3, cFromA a j i = -cFromA a i j := by
  intro i j
  unfold cFromA
  ring

/-- Three-cycle cocycle closedness. -/
theorem c_cocycle (a : Fin 3 → ℝ) : ∀ i j k : Fin 3,
    cFromA a i j + cFromA a j k = cFromA a i k := by
  intro i j k
  unfold cFromA
  ring

/-- The kernel of a ↦ c is the constant vectors (N=3 explicit). -/
theorem c_kernel_constants (a : Fin 3 → ℝ) (h : ∀ i j : Fin 3, cFromA a i j = 0) :
    a 0 = a 1 ∧ a 1 = a 2 := by
  constructor
  · have h01 := h 0 1
    unfold cFromA at h01
    linarith
  · have h12 := h 1 2
    unfold cFromA at h12
    linarith

/-- For N = 3 the six offsets are determined by two parameters. -/
theorem c_two_parameters (a : Fin 3 → ℝ) :
    cFromA a 0 2 = cFromA a 0 1 + cFromA a 1 2 ∧
    cFromA a 1 0 = -cFromA a 0 1 ∧
    cFromA a 2 1 = -cFromA a 1 2 := by
  constructor
  · exact (c_cocycle a 0 1 2).symm
  constructor
  · exact c_antisymm a 0 1
  · exact c_antisymm a 1 2

/-- Gaussian characteristic function (external standard, algebraic form). -/
noncomputable def gaussCF (gamma sigma : ℝ) : ℝ := Real.exp (-((gamma * sigma) ^ 2) / 2)

/-- Higher zeta modes decohere faster: R_n decreases with gamma. -/
theorem gaussCF_decreasing {sigma g1 g2 : ℝ} (hs : 0 < sigma)
    (hg1 : 0 ≤ g1) (h : g1 < g2) : gaussCF g2 sigma < gaussCF g1 sigma := by
  unfold gaussCF
  apply Real.exp_lt_exp.mpr
  have hg2 : 0 < g2 := lt_of_le_of_lt hg1 h
  have hmul : g1 * sigma < g2 * sigma := mul_lt_mul_of_pos_right h hs
  have hn1 : 0 ≤ g1 * sigma := mul_nonneg hg1 (le_of_lt hs)
  have hn2 : 0 ≤ g2 * sigma := mul_nonneg (le_of_lt hg2) (le_of_lt hs)
  have hsquares : (g1 * sigma) ^ 2 < (g2 * sigma) ^ 2 := by
    rw [sq_lt_sq]
    rw [abs_of_nonneg hn1, abs_of_nonneg hn2]
    exact hmul
  nlinarith

end CQM.FrozenCoboundary
