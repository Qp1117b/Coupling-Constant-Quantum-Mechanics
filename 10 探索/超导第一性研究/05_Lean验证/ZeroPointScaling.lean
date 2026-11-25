import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp

/-!
# Ring 8 / ring 9: the zero-point scaling exponent is 1/4, not 1

Workbench file (NOT closing any gap, NOT touching the main ledger).

Round 79 used `sigma^2 ~ 1/k` and hence `r_circ ~ (beta/alpha)^{3/2}`.
That is wrong. The harmonic oscillator gives

    <x^2> = hbar/(2 m omega),   omega = sqrt(k/m)   =>   <x^2> = hbar/(2 sqrt(k m)),

so `sigma^2 ~ k^{-1/2}` and `sigma ~ k^{-1/4}`.

The factor `m sqrt(k/m) = sqrt(k m)` is the whole difference between `1/k` and `1/sqrt k`;
it is proved below as `harmonic_m_sqrt`.

Why the error mattered: for `0 < a < 1`, `a^{1/4} >> a` (proved as `quarter_gt_self`).
With `beta/alpha = 0.17`, using the exponent 1 gives 0.17 while the correct 1/4 gives 0.64 —
a factor 3.7, which propagates to a factor 9 in `r_circ` and turns prod_C r from 0.90 into 0.47.

Proved here (no axiom/sorry/admit/native_decide/unsafe):
  * `harmonic_m_sqrt`  : m * sqrt(k/m) = sqrt(k*m)          (the scaling identity)
  * `harmonic_x2`      : h/(2 m sqrt(k/m)) = h/(2 sqrt(k m)) (same statement for <x^2>)
  * `quarter_lt_one`   : 0 < a < 1 -> a^(1/4) < 1
  * `quarter_gt_self`  : 0 < a < 1 -> a < a^(1/4)            (why 1/4 >> 1 for a<1)

Not formalised: the identification of the stiffnesses with the Keating alpha/beta, the
mode-coupling diagonalisation (registered as Shen-20), and the coupling ratio alpha_u/beta_u.
-/

namespace CQM.ZeroPoint

/-- **The scaling identity.** The harmonic zero-point amplitude is `ℏ/(2mω)` with
`ω = sqrt(k/m)`; the mass factors combine to `sqrt(k m)`, giving the `k^{-1/2}` law for
the variance instead of `k^{-1}`. -/
theorem harmonic_m_sqrt (m k : ℝ) (hm : 0 < m) (hk : 0 < k) :
    m * Real.sqrt (k / m) = Real.sqrt (k * m) := by
  have hsq : (m * Real.sqrt (k / m)) ^ 2 = (Real.sqrt (k * m)) ^ 2 := by
    rw [mul_pow, Real.sq_sqrt (by positivity), Real.sq_sqrt (by positivity)]
    field_simp
  have h1 : 0 ≤ m * Real.sqrt (k / m) := by positivity
  have h2 : 0 ≤ Real.sqrt (k * m) := Real.sqrt_nonneg _
  nlinarith [hsq, h1, h2]

/-- Same statement written as the zero-point amplitude `ℏ/(2mω)`. -/
theorem harmonic_x2 (h m k : ℝ) (hm : 0 < m) (hk : 0 < k) :
    h / (2 * m * Real.sqrt (k / m)) = h / (2 * Real.sqrt (k * m)) := by
  rw [show (2 * m * Real.sqrt (k / m)) = 2 * (m * Real.sqrt (k / m)) by ring,
      harmonic_m_sqrt m k hm hk]

/-- For `0 < a < 1` the fourth root is still below one, so `beta/alpha < 1` bounds
`r_circ` from above at `g = alpha_u/beta_u = 1`. -/
theorem quarter_lt_one (a : ℝ) (h0 : 0 < a) (h1 : a < 1) :
    Real.sqrt (Real.sqrt a) < 1 := by
  have hs : Real.sqrt a < 1 := by
    rw [← Real.sqrt_one]
    exact Real.sqrt_lt_sqrt (le_of_lt h0) h1
  rw [← Real.sqrt_one]
  exact Real.sqrt_lt_sqrt (Real.sqrt_nonneg a) hs

/-- **Why the exponent error was a factor, not a detail.** For `0 < a < 1` the fourth
root exceeds `a` itself: using the exponent `1` instead of `1/4` underestimates the
bond amplitude. -/
theorem quarter_gt_self (a : ℝ) (h0 : 0 < a) (h1 : a < 1) :
    a < Real.sqrt (Real.sqrt a) := by
  have hs0 : 0 < Real.sqrt a := Real.sqrt_pos.mpr h0
  have hs2 : Real.sqrt a ^ 2 = a := Real.sq_sqrt (le_of_lt h0)
  have hs1 : Real.sqrt a < 1 := by
    rw [← Real.sqrt_one]
    exact Real.sqrt_lt_sqrt (le_of_lt h0) h1
  have h_a_lt_s : a < Real.sqrt a := by nlinarith [hs0, hs1, hs2]
  have h_s_lt_ss : Real.sqrt a < Real.sqrt (Real.sqrt a) :=
    Real.sqrt_lt_sqrt (le_of_lt h0) h_a_lt_s
  exact lt_trans h_a_lt_s h_s_lt_ss

end CQM.ZeroPoint
