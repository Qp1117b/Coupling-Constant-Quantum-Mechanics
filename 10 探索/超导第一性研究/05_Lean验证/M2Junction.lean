import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Data.Real.Basic

/-!
# R26: M2 接续结构的代数核

- 接续比值：(9.1)/(10.2) 共享 σ²(1-ρ) 消去 ⇒ 比 = (ħω/2)(κ_f/g)²
- 比值与 σ² 无关（共享因子消去的恒等）
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.M2Junction

noncomputable section

open Real

/-- (9.1) 的方差读出：2 κ² s (1-r)，s=σ²。 -/
def varianceReadout (k s r : ℝ) : ℝ := 2 * k ^ 2 * s * (1 - r)

/-- (10.2) 的配对强度：4 g² s (1-r)/(ħω)。 -/
def pairingStrength (g s r hw : ℝ) : ℝ := 4 * g ^ 2 * s * (1 - r) / hw

/-- 接续比值：variance/pairing = (hw/2)(κ/g)²（共享因子 s(1-r) 消去）。 -/
theorem junction_ratio (k g s r hw : ℝ)
    (hs : s ≠ 0) (hr : 1 - r ≠ 0) (hg : g ≠ 0) (hkw : hw ≠ 0) :
    varianceReadout k s r / pairingStrength g s r hw = (hw / 2) * (k / g) ^ 2 := by
  unfold varianceReadout pairingStrength
  field_simp [hs, hr, hg, hkw]
  ring

/-- 比值与共享因子 s 无关（对两个不同 s，比相同）。 -/
theorem ratio_independent_of_shared (k g s1 s2 r hw : ℝ)
    (hs1 : s1 ≠ 0) (hs2 : s2 ≠ 0) (hr : 1 - r ≠ 0) (hg : g ≠ 0) (hkw : hw ≠ 0) :
    varianceReadout k s1 r / pairingStrength g s1 r hw =
      varianceReadout k s2 r / pairingStrength g s2 r hw := by
  unfold varianceReadout pairingStrength
  field_simp [hs1, hs2, hr, hg, hkw]

end
end CQM.M2Junction
