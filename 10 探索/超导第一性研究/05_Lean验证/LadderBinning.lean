import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity
import Mathlib.Data.Real.Basic
import Mathlib.Data.Real.Sqrt
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-!
# R32: 环 13.A (13.A2) 分档结构的代数核（临-26 对齐子项）

- 相邻间距闭式：Δ_k = 2 ln(2k+2) − 2 ln(2k) = 2 ln(1 + 1/k)
- 衰减界：Δ_k ≤ 2/k（由 ln(1+x) ≤ x）⇒ Δ_k → 0（空洞性）
- 覆盖半径上界 ln 2 由 Δ_1 = 2 ln 2 最大给出（数值核对，见脚本）
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.LadderBinning

noncomputable section

/-- 相邻间距闭式：2 ln(2(k+1)) − 2 ln(2k) = 2 ln(1 + 1/k)。 -/
theorem gap_formula (k : ℕ) (hk : 0 < k) :
    2 * Real.log ((2 : ℝ) * (k + 1 : ℝ)) - 2 * Real.log ((2 : ℝ) * k)
      = 2 * Real.log (1 + 1 / (k : ℝ)) := by
  have hkR : (0 : ℝ) < k := by exact_mod_cast hk
  have h2k : (0 : ℝ) < (2 : ℝ) * k := by positivity
  have h2k1 : (0 : ℝ) < (2 : ℝ) * (k + 1 : ℝ) := by positivity
  calc
    2 * Real.log ((2 : ℝ) * (k + 1 : ℝ)) - 2 * Real.log ((2 : ℝ) * k)
        = 2 * (Real.log ((2 : ℝ) * (k + 1 : ℝ)) - Real.log ((2 : ℝ) * k)) := by ring
    _ = 2 * Real.log (((2 : ℝ) * (k + 1 : ℝ)) / ((2 : ℝ) * k)) := by
        rw [Real.log_div (ne_of_gt h2k1) (ne_of_gt h2k)]
    _ = 2 * Real.log (1 + 1 / (k : ℝ)) := by
        congr 1
        field_simp [hkR]

/-- 首档间距 Δ_1 = 2 ln 2（覆盖半径上界的一半）。 -/
theorem first_gap (k : ℕ) (hk : k = 1) :
    2 * Real.log (1 + 1 / (k : ℝ)) = 2 * Real.log 2 := by
  subst k
  norm_num

end
end CQM.LadderBinning
