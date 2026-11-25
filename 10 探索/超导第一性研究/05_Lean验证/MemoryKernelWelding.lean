import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# `临-8`: no-go on welding the physical memory kernel to the zeta form

Formalises the algebraic core of `03_推导工作台/环26_临8焊接no-go.md`.

The physical kernel carries a mode-dependent damping rate

  α + Γ_n,   Γ_n = γ_n² σ_v² τ_g,   α = <v_τ>/2,

while the zeta form (26.2) has one mode-independent rate 1/2.  Hence:

1. distinct zero ordinates give distinct dampings when σ_v² τ_g > 0, so at most one
   mode can be aligned; two modes cannot both match the uniform rate (No-go A);
2. even with σ_v² τ_g = 0, alignment forces α = 1/2, a gauge normalisation rather
   than a material fact;
3. a positive-type kernel needs K(0) ≥ 0, while the chain convention gives
   K_zeta(0) = -1 (No-go B, conditional on the GLE reading);
4. the quotient between the physical and zeta kernels is a mode-dependent filter W_n,
   equal to one only in the ideal gauge limit.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.MemoryKernelWelding

/-- Distinct zero ordinates (up to sign) have distinct squares. -/
theorem gamma_sq_ne_of_gamma_ne {g h : ℝ} (hgh : g ≠ h) (hgh' : g ≠ -h) :
    g ^ 2 ≠ h ^ 2 := by
  intro hs
  have hfac : (g - h) * (g + h) = 0 := by nlinarith
  rcases mul_eq_zero.mp hfac with hd | hs'
  · exact hgh (by linarith)
  · exact hgh' (by linarith)

/-- The damping increments Γ_n = γ_n²·σ_v²τ_g are distinct. -/
theorem Gamma_ne_of_gamma_sq_ne {g h svtg : ℝ} (hp : 0 < svtg)
    (hsq : g ^ 2 ≠ h ^ 2) : g ^ 2 * svtg ≠ h ^ 2 * svtg := by
  intro heq
  exact hsq (mul_right_cancel₀ (ne_of_gt hp) heq)

/-- Equality of exponential rates on all of ℝ forces the rates to coincide. -/
theorem exp_rate_injective {a b : ℝ}
    (h : ∀ t : ℝ, Real.exp (-a * t) = Real.exp (-b * t)) : a = b := by
  have h1 : Real.exp (-a) = Real.exp (-b) := by simpa using h 1
  have he : -a = -b := Real.exp_injective h1
  linarith

/-- A single mode is aligned with the uniform rate 1/2 iff its total rate equals 1/2. -/
theorem single_mode_rate {a g svtg t : ℝ} (ht : t ≠ 0)
    (h : Real.exp (-(a + g ^ 2 * svtg) * t) = Real.exp (-(1 / 2 : ℝ) * t)) :
    a + g ^ 2 * svtg = 1 / 2 := by
  have he : -(a + g ^ 2 * svtg) * t = -(1 / 2 : ℝ) * t := Real.exp_injective h
  have hpos : (a + g ^ 2 * svtg) * t = (1 / 2 : ℝ) * t := by nlinarith
  exact mul_right_cancel₀ ht hpos

/-- No-go A: two distinct zero ordinates cannot both be aligned when σ_v²τ_g > 0. -/
theorem mode_no_go {a g h svtg t : ℝ} (hp : 0 < svtg) (hgsq : g ^ 2 ≠ h ^ 2)
    (ht : t ≠ 0)
    (hg : Real.exp (-(a + g ^ 2 * svtg) * t) = Real.exp (-(1 / 2 : ℝ) * t))
    (hh : Real.exp (-(a + h ^ 2 * svtg) * t) = Real.exp (-(1 / 2 : ℝ) * t)) : False := by
  have hg' := single_mode_rate ht hg
  have hh' := single_mode_rate ht hh
  have hGamma : g ^ 2 * svtg = h ^ 2 * svtg := by nlinarith
  exact Gamma_ne_of_gamma_sq_ne hp hgsq hGamma

/-- Without time fluctuations, alignment still fixes the clock rate α = 1/2. -/
theorem alpha_must_be_half {a t : ℝ} (ht : t ≠ 0)
    (h : Real.exp (-a * t) = Real.exp (-(1 / 2 : ℝ) * t)) : a = 1 / 2 := by
  have he : -a * t = -(1 / 2 : ℝ) * t := Real.exp_injective h
  have hpos : a * t = (1 / 2 : ℝ) * t := by nlinarith
  exact mul_right_cancel₀ ht hpos

/-- No-go B: a positive-type kernel cannot have a negative value at zero. -/
theorem positive_type_zero_nonneg (K : ℝ → ℝ) (hpos : ∀ t, |K t| ≤ K 0) : 0 ≤ K 0 := by
  have h0 := hpos 0
  have habs : 0 ≤ |K 0| := abs_nonneg _
  linarith

/-- The chain convention (26.2) gives K_zeta(0) = ψ(1) - 1 = -1 < 0. -/
theorem zeta_kernel_zero_neg {K0 : ℝ} (h : K0 = -1) : K0 < 0 := by
  rw [h]
  norm_num

/-- No-go C: one common readout at a common instant forces the node proper times
to coincide, i.e. the fully coherent gauge choice, not a material property. -/
theorem gauge_coincidence {f : ℝ → ℝ} (hinj : Function.Injective f) {ti tj t : ℝ}
    (hi : f ti = f t) (hj : f tj = f t) : ti = tj := by
  exact hinj (hi.trans hj.symm)

/-! ## The filter between the physical and zeta kernels -/

/-- Mode-dependent filter: physical amplitude divided by the zeta amplitude. -/
noncomputable def W (a G t : ℝ) : ℝ := Real.exp (-((a + G - 1 / 2) * t))

/-- `W = 1` at a nonzero time iff the total rate is the uniform rate. -/
theorem W_eq_one {a G t : ℝ} (ht : t ≠ 0) (h : W a G t = 1) : a + G = 1 / 2 := by
  unfold W at h
  have h' : Real.exp (-((a + G - 1 / 2) * t)) = Real.exp 0 := by simpa using h
  have he : -((a + G - 1 / 2) * t) = 0 := Real.exp_injective h'
  have hmul : (a + G - 1 / 2) * t = 0 := by nlinarith
  have hzero : a + G - 1 / 2 = 0 := (mul_eq_zero.mp hmul).resolve_right ht
  linarith

/-- The ideal gauge limit `α = 1/2, Γ = 0` gives `W = 1`. -/
theorem W_at_ideal (t : ℝ) : W (1 / 2) 0 t = 1 := by
  unfold W
  norm_num

/-- Distinct Γ give distinct filters, so the physical kernel is not a scalar
multiple of the zeta kernel. -/
theorem filter_ne_of_Gamma_ne {G1 G2 t : ℝ} (hG : G1 ≠ G2) (ht : t ≠ 0) :
    Real.exp (-G1 * t) ≠ Real.exp (-G2 * t) := by
  intro he
  have hlin : -G1 * t = -G2 * t := Real.exp_injective he
  have hpos : G1 * t = G2 * t := by nlinarith
  exact hG (mul_right_cancel₀ ht hpos)

end CQM.MemoryKernelWelding
