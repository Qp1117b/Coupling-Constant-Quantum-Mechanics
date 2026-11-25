import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Data.Real.Basic
import Mathlib.Data.Real.Sqrt

/-!
# R29: R1 λ 质量无关预言的代数核

- ρ_m c² = (M n)(a² κ_s/M) = n a² κ_s（质量精确抵消）
- λ 的 M-形式 = M-自由形式
- 同位素 ω_D ∝ M^{-1/2}
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.MassIndependence

noncomputable section

open Real

/-- ρ_m c² 的质量抵消：(M n)(a² κ_s / M) = n a² κ_s。 -/
theorem mass_cancels (M n a2 kappa : ℝ) (hM : M ≠ 0) :
    (M * n) * (a2 * kappa / M) = n * a2 * kappa := by
  field_simp [hM]

/-- λ 的 M-形式等于 M-自由形式（证明 M 被消去）。 -/
theorem lambda_no_mass (N0 z g2 ce2 oneMinusRho Q3 n a kappa M : ℝ)
    (hM : M ≠ 0) :
    N0 * z * g2 * ce2 * oneMinusRho * Q3 / ((M * n) * (a^2 * kappa / M))
      = N0 * z * g2 * ce2 * oneMinusRho * Q3 / (n * a^2 * kappa) := by
  rw [show (M * n) * (a^2 * kappa / M) = n * a^2 * kappa by field_simp [hM]]

/-- 同位素：ω_D = a √(κ_s/M) ∝ M^{-1/2}（固定 a,κ_s）。 -/
theorem isotope_omega (a kappa M : ℝ) (hkap : 0 ≤ kappa) :
    a * Real.sqrt (kappa / M) = (a * Real.sqrt kappa) / Real.sqrt M := by
  rw [Real.sqrt_div hkap]
  ring

end
end CQM.MassIndependence
