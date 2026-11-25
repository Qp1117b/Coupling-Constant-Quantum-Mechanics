import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# FE02 CANDIDATE (NOT LANDED): quantitative core of the "number-theoretic energy scale" no-go

Authority (already proved in main chain): lin-22 gives Gamma_n ~ gamma_n^2 T / w^2
(depends on external w = omega_D) => circular; lin-8 strong no-go: physical kernel
mode rate alpha + gamma_n^2 s v^2 tau_g is n-dependent, zeta rate 1/2 is not,
aligning two modes requires (gamma_n^2-gamma_m^2) s v^2 tau_g = 0, contradicting
s v^2 tau_g > 0 and gamma_n != gamma_m.

No axiom/sorry/admit/native_decide/unsafe.
-/

namespace CQM.FE02

/-- lin-8: two-mode alignment condition. If rate_n = rate_m and gamma_n != gamma_m,
    then sigma_v^2 tau_g = 0. -/
theorem l8_two_mode (g2n g2m s : ℝ) (hdiff : g2n ≠ g2m)
    (halign : g2n * s = g2m * s) : s = 0 := by
  have h : (g2n - g2m) * s = 0 := by nlinarith
  exact (mul_eq_zero.mp h).resolve_left (sub_ne_zero.mpr hdiff)

/-- lin-8 contradiction: with sigma_v^2 tau_g > 0, rates cannot align for distinct modes. -/
theorem l8_no_alignment (g2n g2m s : ℝ) (hdiff : g2n ≠ g2m) (hspos : 0 < s) :
    g2n * s ≠ g2m * s := by
  intro h
  have : s = 0 := l8_two_mode g2n g2m s hdiff h
  linarith

/-- lin-22 circularity: Gamma_1 = C * gamma1^2 * T / w^2.
    Show Gamma_1 depends on w (the very scale it would replace): monotone decreasing. -/
theorem gamma1_inverse_w_sq (C g2 T w1 w2 : ℝ)
    (hC : 0 < C) (hg2 : 0 < g2) (hT : 0 < T) (hw1 : 0 < w1) (hw2 : 0 < w2)
    (hlt : w1 < w2) :
    C * g2 * T / w2 ^ 2 < C * g2 * T / w1 ^ 2 := by
  have hnum : 0 < C * g2 * T := by positivity
  rw [div_lt_div_iff₀ (sq_pos_of_pos hw2) (sq_pos_of_pos hw1)]
  nlinarith [sq_pos_of_pos hw1, sq_pos_of_pos hw2,
             mul_pos (sub_pos.mpr hlt) (add_pos hw2 hw1)]

/-- Circularity statement: if one tries to set w^2 = k*Gamma_1 (self-consistency),
    substitute Gamma_1 = C g2 T / w^2 to get w^4 = k C g2 T: w is fixed by T and
    the external constants -- i.e. NOT by number theory alone (gamma alone cannot fix it). -/
theorem self_consistency_w4 (C g2 T k w : ℝ) (hw : 0 < w) (_hk : 0 < k) :
    w ^ 2 = k * (C * g2 * T / w ^ 2) ↔ w ^ 4 = k * C * g2 * T := by
  constructor
  · intro h
    have hw2ne : w ^ 2 ≠ 0 := pow_ne_zero 2 (ne_of_gt hw)
    field_simp [hw2ne] at h ⊢
    nlinarith
  · intro h
    have hw2ne : w ^ 2 ≠ 0 := pow_ne_zero 2 (ne_of_gt hw)
    field_simp [hw2ne] at h ⊢
    nlinarith

end CQM.FE02
