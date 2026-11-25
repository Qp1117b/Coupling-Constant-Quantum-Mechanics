import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# `临-2`: equal-marginal allocation and the two dome branches

Let m(n) = lam(n+1) - lam(n) be the discrete marginal.  Strict anti-monotonicity
(concave lam) gives a unique equal-marginal solution and a positive one-step
transfer gain, i.e. the interior equal split is the global maximum (water-filling
= descending branch).  Strict monotonicity (convex lam) reverses the gain, giving
a corner solution (winner-take-all = ascending branch).  The saturated candidate
(16.A1) has a geometric marginal, hence strictly anti-monotone.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.MarginalAllocation

/-- Discrete marginal m(n) = lam(n+1) - lam(n). -/
def marg (lam : ℕ → ℝ) (n : ℕ) : ℝ := lam (n + 1) - lam n

/-- Strictly decreasing marginal forces equal-marginal points to coincide. -/
theorem marg_eq_unique {m : ℕ → ℝ} (hm : StrictAnti m) {i j : ℕ}
    (h : m i = m j) : i = j := by
  by_contra hne
  rcases lt_or_gt_of_ne hne with hij | hji
  · have hlt : m j < m i := hm hij
    linarith
  · have hlt : m i < m j := hm hji
    linarith

/-- Concave case: moving one unit from a larger domain to a smaller one
    (with a gap) strictly increases the total lambda. -/
theorem transfer_gain {lam : ℕ → ℝ}
    (hm : StrictAnti (marg lam)) {i j : ℕ} (hij : i + 1 < j) :
    lam i + lam j < lam (i + 1) + lam (j - 1) := by
  have hij' : i < j - 1 := by omega
  have hlt := hm hij'
  unfold marg at hlt
  have hj : j - 1 + 1 = j := Nat.sub_add_cancel (by omega)
  rw [hj] at hlt
  linarith

/-- Convex case: the transfer gain reverses, so the equal split is a minimum
    and the maximum sits at a corner. -/
theorem convex_transfer_reverse {lam : ℕ → ℝ}
    (hm : StrictMono (marg lam)) {i j : ℕ} (hij : i + 1 < j) :
    lam (i + 1) + lam (j - 1) < lam i + lam j := by
  have hij' : i < j - 1 := by omega
  have hlt := hm hij'
  unfold marg at hlt
  have hj : j - 1 + 1 = j := Nat.sub_add_cancel (by omega)
  rw [hj] at hlt
  linarith

/-- Saturated candidate (16.A1): lambda(n) = linf * (1 - exp(-n/n0)). -/
noncomputable def lamSat (linf n0 : ℝ) (n : ℕ) : ℝ :=
  linf * (1 - Real.exp (-(n : ℝ) / n0))

/-- Closed form of the saturated marginal: geometric sequence. -/
theorem sat_marg_form (linf n0 : ℝ) (n : ℕ) :
    marg (lamSat linf n0) n =
      linf * (1 - Real.exp (-(1 : ℝ) / n0)) * Real.exp (-(n : ℝ) / n0) := by
  unfold marg lamSat
  rw [show (-(↑(n + 1) : ℝ) / n0) = (-(n : ℝ) / n0) + (-(1 : ℝ) / n0) by
    norm_num
    ring]
  rw [Real.exp_add]
  ring

/-- The saturated marginal is strictly decreasing when linf>0 and n0>0. -/
theorem sat_marg_strictAnti (linf n0 : ℝ) (hlinf : 0 < linf) (hn0 : 0 < n0) :
    StrictAnti (marg (lamSat linf n0)) := by
  intro i j hij
  rw [sat_marg_form linf n0, sat_marg_form linf n0]
  have hcoef : 0 < linf * (1 - Real.exp (-(1 : ℝ) / n0)) := by
    have hinv : 0 < (1 : ℝ) / n0 := one_div_pos.mpr hn0
    have hneg : -(1 : ℝ) / n0 < 0 := by
      rw [show -(1 : ℝ) / n0 = -(1 / n0) by ring]
      linarith
    have hexp : Real.exp (-(1 : ℝ) / n0) < 1 := Real.exp_lt_one_iff.mpr hneg
    nlinarith
  have harg : -(j : ℝ) / n0 < -(i : ℝ) / n0 := by
    have hijr : (i : ℝ) < j := by exact_mod_cast hij
    have hnegij : -(j : ℝ) < -(i : ℝ) := by linarith
    exact (div_lt_div_iff_of_pos_right hn0).mpr hnegij
  have hexplt : Real.exp (-(j : ℝ) / n0) < Real.exp (-(i : ℝ) / n0) :=
    Real.exp_lt_exp.mpr harg
  exact mul_lt_mul_of_pos_left hexplt hcoef

end CQM.MarginalAllocation
