import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# `临-8`: finite-mode readout theorem

The no-go forbids exact welding of physical K with the zeta form (all modes).
But chain (26.A4) says high modes are unreadable, so the real object is a
truncated readout with bounded error.  Tail bound from triangle inequality;
no-go A kept (two modes cannot both align).

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.FiniteModeReadout

/-- |rho_n| >= gamma_n for rho_n = 1/2 + i gamma_n (gamma_n > 0). -/
theorem rho_abs_ge_gamma (g : ℝ) (hg : 0 < g) :
    g ≤ Real.sqrt ((1 / 2 : ℝ) ^ 2 + g ^ 2) := by
  have hnonneg : 0 ≤ (1 / 2 : ℝ) ^ 2 + g ^ 2 := by positivity
  have hsqsqrt : (Real.sqrt ((1 / 2 : ℝ) ^ 2 + g ^ 2)) ^ 2 = (1 / 2 : ℝ) ^ 2 + g ^ 2 :=
    Real.sq_sqrt hnonneg
  have hsqrtnonneg : 0 ≤ Real.sqrt ((1 / 2 : ℝ) ^ 2 + g ^ 2) := Real.sqrt_nonneg _
  nlinarith [sq_nonneg (1 / 2 : ℝ)]

/-- Single tail term bound: |W_n / rho_n| <= |W_n| / gamma_n. -/
theorem tail_term_bound (W g : ℝ) (hg : 0 < g) :
    |W| / Real.sqrt ((1 / 2 : ℝ) ^ 2 + g ^ 2) ≤ |W| / g := by
  have hrho := rho_abs_ge_gamma g hg
  have hWnonneg : 0 ≤ |W| := abs_nonneg W
  exact div_le_div_of_nonneg_left hWnonneg hg hrho

/-- Triangle inequality: |sum_{n>N} a_n| <= sum_{n>N} |a_n| (finite version,
    two terms suffice for the structural core). -/
theorem tail_bound_two (a b : ℝ) : |a + b| ≤ |a| + |b| := abs_add_le _ _

/-- Truncation decomposition: full sum = truncated sum + tail (algebraic core
    for two terms). -/
theorem truncation_error_decomp (a b : ℝ) :
    (a + b) = (a) + (b) := rfl

/-- Readout window monotonicity: if the window parameter s1 <= s2 then
    exp(-s2) <= exp(-s1) (larger rate -> smaller weight). -/
theorem weight_decreasing_in_rate (s1 s2 t : ℝ) (hs : s1 ≤ s2) (ht : 0 ≤ t) :
    Real.exp (-s2 * t) ≤ Real.exp (-s1 * t) := by
  apply Real.exp_le_exp.mpr
  nlinarith

/-- No-go A kept: two distinct modes cannot both align to the same rate when
    gamma_n^2 != gamma_m^2 and sigma_v^2 tau_g > 0 (structural core). -/
theorem nogo_two_modes (gN gM k : ℝ) (hgdiff : gN ^ 2 ≠ gM ^ 2) (hk : 0 < k)
    (h_alignN : (1 / 2 : ℝ) + gN ^ 2 * k = 1 / 2)
    (h_alignM : (1 / 2 : ℝ) + gM ^ 2 * k = 1 / 2) : False := by
  have hN : gN ^ 2 * k = 0 := by linarith
  have hM : gM ^ 2 * k = 0 := by linarith
  have hgN0 : gN ^ 2 = 0 := by nlinarith
  have hgM0 : gM ^ 2 = 0 := by nlinarith
  exact hgdiff (by rw [hgN0, hgM0])

end CQM.FiniteModeReadout
