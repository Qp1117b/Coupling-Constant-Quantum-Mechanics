import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# `临-22`: the physical damping bridge

The OU memory time is tied to the Debye spectrum, `τ_g = c/ω_D`.  With the
high-temperature incoherent variance `σ_v² = κ T/ω_D` this gives a T-linear
damping shape `Γ_n ∝ γ_n² T/ω_D²`.  Because the rate is mode dependent, it cannot
supply the uniform zeta rate `β_n ≡ 1/2` (RH); only a time-unit normalization
can be fixed by external parameters.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.DampingBridge

/-- The Debye-set OU memory time. -/
noncomputable def tauG (c omegaD : ℝ) : ℝ := c / omegaD

/-- The physical mode damping rate from (26.1b). -/
noncomputable def Gamma (g sigma2 c omegaD : ℝ) : ℝ :=
  g ^ 2 * sigma2 * tauG c omegaD

/-- High-temperature form: σ_v² = κ T / ω_D. -/
noncomputable def sigmaHighT (kap T omegaD : ℝ) : ℝ := kap * T / omegaD

/-- The T-linear shape: Γ_n = (c κ γ_n² / ω_D²) T. -/
theorem Gamma_linear_T (g kap T c omegaD : ℝ) (ho : omegaD ≠ 0) :
    Gamma g (sigmaHighT kap T omegaD) c omegaD =
      (c * kap * g ^ 2 / omegaD ^ 2) * T := by
  unfold Gamma sigmaHighT tauG
  field_simp [ho]

/-- The product σ_v² τ_g in the high-T branch. -/
theorem s_tau_highT (kap T c omegaD : ℝ) (ho : omegaD ≠ 0) :
    sigmaHighT kap T omegaD * tauG c omegaD = kap * c * T / omegaD ^ 2 := by
  unfold sigmaHighT tauG
  field_simp [ho]

/-- Distinct zero ordinates give distinct damping rates. -/
theorem Gamma_modes_differ {g h sigma2 c omegaD : ℝ}
    (hs : 0 < sigma2) (hc : 0 < c) (hw : 0 < omegaD)
    (hgsq : g ^ 2 ≠ h ^ 2) : Gamma g sigma2 c omegaD ≠ Gamma h sigma2 c omegaD := by
  unfold Gamma tauG
  intro heq
  have hsne : sigma2 ≠ 0 := ne_of_gt hs
  have hcne : c ≠ 0 := ne_of_gt hc
  have hwne : omegaD ≠ 0 := ne_of_gt hw
  field_simp [hsne, hcne, hwne] at heq
  exact hgsq (by nlinarith)

/-- Two distinct modes cannot share one uniform physical rate: the physical side
cannot supply β_n ≡ 1/2. -/
theorem no_beta_unification {g h b sigma2 c omegaD : ℝ}
    (hs : 0 < sigma2) (hc : 0 < c) (hw : 0 < omegaD)
    (hgsq : g ^ 2 ≠ h ^ 2)
    (hg : Gamma g sigma2 c omegaD = b) (hh : Gamma h sigma2 c omegaD = b) : False := by
  have hdiff := Gamma_modes_differ (g := g) (h := h) (sigma2 := sigma2)
    (c := c) (omegaD := omegaD) hs hc hw hgsq
  exact hdiff (hg.trans hh.symm)

/-- A common rescaling of all rates is a time-unit choice: it preserves the
mode-to-mode difference, so it cannot create uniformity. -/
theorem time_unit_gauge_only {g h sigma2 c omegaD lam : ℝ}
    (hs : 0 < sigma2) (hc : 0 < c) (hw : 0 < omegaD) (hl : lam ≠ 0)
    (hgsq : g ^ 2 ≠ h ^ 2) :
    lam * Gamma g sigma2 c omegaD ≠ lam * Gamma h sigma2 c omegaD := by
  have hdiff := Gamma_modes_differ (g := g) (h := h) (sigma2 := sigma2)
    (c := c) (omegaD := omegaD) hs hc hw hgsq
  intro heq
  have : Gamma g sigma2 c omegaD = Gamma h sigma2 c omegaD := by
    apply mul_left_cancel₀ hl
    exact heq
  exact hdiff this

end CQM.DampingBridge
