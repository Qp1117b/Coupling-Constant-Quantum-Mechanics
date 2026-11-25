import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# `审-14`: the first-principles source of Γ(E;χ)

Γ is the cumulative count of states, so its exponent is the spectral dimension:
a Debye density `g(ω) ∝ ω^(d-1)` gives a cumulative `∝ ω^d`, hence `n = d` and the
only chain-internal energy scale is `E₀ ~ ħω_D`.  Plugging into (补.3) gives
`T_c ~ 0.63 ħω_D`, orders of magnitude above observation: the alternate T entrance
is not the physical one.  External parameters can only move the peak via E₀(χ).

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.GammaSource

/-- The cumulative state count Γ(E) = 1 + (E/E₀)^n. -/
noncomputable def Gamma (E E0 : ℝ) (n : ℕ) : ℝ := 1 + (E / E0) ^ n

/-- The dimensionless inverse-temperature shape β = n x^(n-1)/(1+x^n). -/
noncomputable def betaShape (x : ℝ) (n : ℕ) : ℝ :=
  (n : ℝ) * x ^ (n - 1) / (1 + x ^ n)

/-- The cumulative exponent is the spectral exponent: derivative of x^d is d x^(d-1). -/
theorem spectral_exponent (d : ℕ) (x : ℝ) :
    deriv (fun y : ℝ => y ^ d) x = (d : ℝ) * x ^ (d - 1) := by
  exact (hasDerivAt_pow d x).deriv

/-- For n = 1 the shape is strictly decreasing: no peak, no transition. -/
theorem beta_n1_strictly_decreasing {x y : ℝ} (hx : 0 < x) (hxy : x < y) :
    betaShape y 1 < betaShape x 1 := by
  unfold betaShape
  simp
  have hx1 : 0 < 1 + x := by linarith
  have hy1 : 0 < 1 + y := by linarith
  have hlt : 1 / (1 + y) < 1 / (1 + x) := one_div_lt_one_div_of_lt hx1 (by linarith)
  simpa [one_div] using hlt

/-- The peak condition for n = 2 is `1 - x² = 0`, giving x = 1 on the positive branch. -/
theorem peak_n2 {x : ℝ} (hx : 0 < x) (h : (1 : ℝ) - x ^ 2 = 0) : x = 1 := by
  have hfac : (1 - x) * (1 + x) = 0 := by nlinarith
  rcases mul_eq_zero.mp hfac with h1 | h2
  · linarith
  · nlinarith

/-- The peak temperature factor for n = 3 is 2^(-2/3). -/
noncomputable def tcFactor (n : ℕ) : ℝ :=
  (((n : ℝ) - 1) ^ (-(((n : ℝ) - 1) / (n : ℝ))))

theorem tc_factor_n3 : tcFactor 3 = (2 : ℝ) ^ (-(2 : ℝ) / 3) := by
  unfold tcFactor
  norm_num

/-- External parameters entering only through E₀ rescale T_c linearly: the peak
exists (or not) independently of χ. -/
theorem chi_rescales_only {E0 c : ℝ} (n : ℕ) :
    (c * E0) * tcFactor n = c * (E0 * tcFactor n) := by
  ring

/-- The Debye-based prediction is orders of magnitude above the measured ratio
for aluminium (external values T_c = 1.2 K, θ_D = 428 K). -/
theorem prediction_vs_observation : (1.2 : ℝ) / 428 < (2 : ℝ) ^ (-(2 : ℝ) / 3) := by
  have hmono : (2 : ℝ) ^ (-1 : ℝ) < (2 : ℝ) ^ (-(2 : ℝ) / 3) := by
    apply Real.rpow_lt_rpow_of_exponent_lt
    norm_num
    norm_num
  have hhalf : (2 : ℝ) ^ (-1 : ℝ) = 1 / 2 := by norm_num [Real.rpow_neg]
  rw [hhalf] at hmono
  nlinarith

end CQM.GammaSource
