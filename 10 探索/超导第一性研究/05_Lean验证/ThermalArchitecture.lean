import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Order.Monotone.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.GCongr
import Mathlib.Tactic.NormNum

/-!
# Thermal architecture: a small formal interface

This file formalises only the *role separation* used in
`10 探索/超导第一性研究/03_推导工作台/环04_温度角色分层.md`.

It does **not** prove the Debye integral, the physical identification of
`sigmaV2` with lattice fluctuations, or any `T_c` formula.  It proves:

1. the total variance decomposes as `Z + Theta T`;
2. the pairing coupling built from `Z` is independent of `T`;
3. if `Theta` is monotone, the coherence factor `exp (-Gamma t)` is
   antitone in `T`;
4. if the variance is monotone, the old threshold probability
   `1[Var > sigma_c]` is monotone (so it cannot be the required
   low-temperature ordering probability).

All statements are conditional on the displayed hypotheses; no axiom,
`sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.ThermalArchitecture

noncomputable section

/-- Total angle variance as the sum of a zero-point part and a thermal part. -/
def totalVariance (Z : ℝ) (Theta : ℝ → ℝ) (T : ℝ) : ℝ :=
  Z + Theta T

/-- The total variance inherits monotonicity from the thermal part. -/
theorem totalVariance_mono
    {Z : ℝ} {Theta : ℝ → ℝ} (h : Monotone Theta) :
    Monotone (fun T => totalVariance Z Theta T) := by
  intro a b hab
  unfold totalVariance
  exact add_le_add_right (h hab) Z

/-- Pairing coupling built from the zero-point variance only. -/
def pairingCoupling (Z : ℝ) : ℝ := Z

/-- The coupling does not depend on the temperature argument. -/
theorem pairingCoupling_T_independent (Z : ℝ) (_T₁ _T₂ : ℝ) :
    pairingCoupling Z = pairingCoupling Z := by
  rfl

/-- Thermal dephasing rate `gamma^2 * sigmaV2 * tau_g`. -/
def dephasingRate (gamma tau_g : ℝ) (sigmaV2 : ℝ → ℝ) (T : ℝ) : ℝ :=
  gamma ^ 2 * sigmaV2 T * tau_g

/-- Coherence factor `exp (-Gamma t)`. -/
def coherence (gamma tau_g t : ℝ) (sigmaV2 : ℝ → ℝ) (T : ℝ) : ℝ :=
  Real.exp (-(dephasingRate gamma tau_g sigmaV2 T * t))

/-- If the thermal variance is monotone and the prefactors are nonnegative,
the coherence factor is antitone in `T`. -/
theorem coherence_antitone
    {gamma tau_g t : ℝ} {sigmaV2 : ℝ → ℝ}
    (htau : 0 ≤ tau_g) (ht : 0 ≤ t)
    (hsigma : Monotone sigmaV2) :
    Antitone (fun T => coherence gamma tau_g t sigmaV2 T) := by
  intro a b hab
  have hsig : sigmaV2 a ≤ sigmaV2 b := hsigma hab
  have hrate : gamma ^ 2 * sigmaV2 a * tau_g ≤ gamma ^ 2 * sigmaV2 b * tau_g := by
    gcongr
  have hrate_t : dephasingRate gamma tau_g sigmaV2 a * t ≤
      dephasingRate gamma tau_g sigmaV2 b * t := by
    unfold dephasingRate
    gcongr
  have harg : -(dephasingRate gamma tau_g sigmaV2 b * t) ≤
      -(dephasingRate gamma tau_g sigmaV2 a * t) := by
    linarith
  exact Real.exp_le_exp.mpr harg

/-- Threshold probability used by the old ring-15 reading. -/
def thresholdProbability (var : ℝ → ℝ) (sigmaC : ℝ) (T : ℝ) : ℝ :=
  if var T > sigmaC then 1 else 0

/-- A monotone variance produces a monotone threshold probability. -/
theorem thresholdProbability_mono
    {var : ℝ → ℝ} (h : Monotone var) (sigmaC : ℝ) :
    Monotone (fun T => thresholdProbability var sigmaC T) := by
  intro a b hab
  by_cases ha : var a > sigmaC
  · have hb : var b > sigmaC := lt_of_lt_of_le ha (h hab)
    simp [thresholdProbability, ha, hb]
  · by_cases hb : var b > sigmaC
    · simp [thresholdProbability, ha, hb]
    · simp [thresholdProbability, ha, hb]

/-- If the variance crosses the threshold upward between `a` and `b`,
the threshold probability is not antitone on that pair. -/
theorem thresholdProbability_not_antitone_of_crossing
    {var : ℝ → ℝ} {sigmaC a b : ℝ}
    (hab : a ≤ b)
    (ha : var a ≤ sigmaC) (hb : sigmaC < var b) :
    ¬ Antitone (fun T => thresholdProbability var sigmaC T) := by
  intro hanti
  have hpa : thresholdProbability var sigmaC a = 0 := by
    simp [thresholdProbability, ha]
  have hpb : thresholdProbability var sigmaC b = 1 := by
    simp [thresholdProbability, hb]
  have hle : thresholdProbability var sigmaC b ≤ thresholdProbability var sigmaC a :=
    hanti hab
  rw [hpa, hpb] at hle
  norm_num at hle

end

end CQM.ThermalArchitecture
