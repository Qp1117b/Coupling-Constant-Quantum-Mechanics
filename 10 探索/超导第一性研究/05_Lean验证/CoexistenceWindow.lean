import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# `审-12`: coexistence window of local anchor and global percolation

Main-chain reading-layer scaling gives a downward shift Delta p ~ L^{-3/4}
(2D nu = 4/3); the participation ratio of `临-21` gives L_eff = sqrt(n_eff).
Hence the local pseudo-critical threshold is p_c^loc = p_c - C n_eff^{-3/8},
below the global p_c.  The nonempty window (p_c^loc, p_c) is the necessary
condition for "local anchor before global percolation" (inference 11).

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.CoexistenceWindow

/-- Local pseudo-critical threshold: p_c^loc = p_c - C * n_eff^{-3/8}. -/
noncomputable def pLoc (pc C neff : ℝ) : ℝ :=
  pc - C * neff ^ (-(3 : ℝ) / 8)

/-- The local threshold lies strictly below the global one. -/
theorem pLoc_lt_pc (pc C neff : ℝ) (hC : 0 < C) (hn : 0 < neff) :
    pLoc pc C neff < pc := by
  unfold pLoc
  have hp : 0 < neff ^ (-(3 : ℝ) / 8) := Real.rpow_pos_of_pos hn _
  nlinarith [mul_pos hC hp]

/-- Window width is C * n_eff^{-3/8}. -/
theorem window_width (pc C neff : ℝ) :
    pc - pLoc pc C neff = C * neff ^ (-(3 : ℝ) / 8) := by
  unfold pLoc
  ring

/-- The coexistence window (p_c^loc, p_c) is nonempty. -/
theorem window_nonempty (pc C neff : ℝ) (hC : 0 < C) (hn : 0 < neff) :
    ∃ p : ℝ, pLoc pc C neff < p ∧ p < pc := by
  refine ⟨(pLoc pc C neff + pc) / 2, ?_, ?_⟩
  · have h := pLoc_lt_pc pc C neff hC hn
    linarith
  · have h := pLoc_lt_pc pc C neff hC hn
    linarith

/-- Window width strictly decreases with n_eff (negative exponent). -/
theorem window_decreasing (C n1 n2 : ℝ) (hC : 0 < C)
    (hn1 : 0 < n1) (h12 : n1 < n2) :
    C * n2 ^ (-(3 : ℝ) / 8) < C * n1 ^ (-(3 : ℝ) / 8) := by
  have hpow : n2 ^ (-(3 : ℝ) / 8) < n1 ^ (-(3 : ℝ) / 8) :=
    Real.rpow_lt_rpow_of_neg hn1 h12 (by norm_num)
  exact mul_lt_mul_of_pos_left hpow hC

/-- Algebraic core of the capacity lower bound: q = n_eff^{-3/8} < p_c / C. -/
theorem capacity_lower_aux (pc C q : ℝ) (hC : 0 < C)
    (h : 0 < pc - C * q) : q < pc / C := by
  have hmul : q * C < pc := by nlinarith
  exact (lt_div_iff₀ hC).mpr hmul

/-- Equivalence of the two forms of the capacity bound:
    q = n_eff^{-3/8} gives q^{-8/3} = n_eff. -/
theorem q_pow_back (neff : ℝ) (hn : 0 < neff) :
    (neff ^ (-(3 : ℝ) / 8)) ^ (-(8 : ℝ) / 3) = neff := by
  rw [← Real.rpow_mul (le_of_lt hn)]
  norm_num

end CQM.CoexistenceWindow
