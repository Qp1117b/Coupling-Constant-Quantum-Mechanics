import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# Morel-Anderson mu* shape (M.1)

Webb 2015 Eq5 / Morel-Anderson 1962:
  mu* = mu / (1 + mu * L),  L = ln(epsilon_F / hbar omega_D) > 0.
Core algebra proved: 0 < mu* < mu; monotone increasing in mu;
limit form mu/(1+mu L) = 1/(1/mu + L) -> 1/L as mu -> infinity.

This is SHAPE only; epsilon_F and mu are external material values.
No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.MuStarShape

/-- M.1 positivity: mu* > 0 for mu>0, L>0. -/
theorem mustar_pos (mu L : ℝ) (hmu : 0 < mu) (hL : 0 < L) :
    0 < mu / (1 + mu * L) := by
  positivity

/-- M.1: mu* < mu (retardation weakens Coulomb). -/
theorem mustar_lt_mu (mu L : ℝ) (hmu : 0 < mu) (hL : 0 < L) :
    mu / (1 + mu * L) < mu := by
  have hden : 0 < 1 + mu * L := by positivity
  rw [div_lt_iff₀ hden]
  nlinarith [mul_pos hmu hL]

/-- M.1 monotonicity in mu: mu1 < mu2 => mu1* < mu2*. -/
theorem mustar_mono (mu1 mu2 L : ℝ) (h1 : 0 < mu1) (h12 : mu1 < mu2) (hL : 0 < L) :
    mu1 / (1 + mu1 * L) < mu2 / (1 + mu2 * L) := by
  have h2 : 0 < mu2 := by linarith
  have hd1 : 0 < 1 + mu1 * L := by positivity
  have hd2 : 0 < 1 + mu2 * L := by positivity
  rw [div_lt_div_iff₀ hd1 hd2]
  nlinarith [mul_pos hL (sub_pos.mpr h12)]

/-- M.1 limit form: mu/(1+mu L) = 1/(1/mu + L) (mu,L nonzero). -/
theorem mustar_limit_form (mu L : ℝ) (hmu : mu ≠ 0) (hden : 1 + mu * L ≠ 0) :
    mu / (1 + mu * L) = 1 / (1 / mu + L) := by
  field_simp [hmu, hden]

/-- Adiabatic limit: mu* < 1/L for finite mu>0,L>0 (approached from below). -/
theorem mustar_lt_limit (mu L : ℝ) (hmu : 0 < mu) (hL : 0 < L) :
    mu / (1 + mu * L) < 1 / L := by
  have hden : 0 < 1 + mu * L := by positivity
  rw [div_lt_div_iff₀ hden hL]
  nlinarith

end CQM.MuStarShape
