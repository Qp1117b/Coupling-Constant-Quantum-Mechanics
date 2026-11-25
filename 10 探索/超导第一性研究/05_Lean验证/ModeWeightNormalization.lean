import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic

/-!
# R31: 环 12.A 模式权重比的代数核（临-5 子块·独立复核）

诚实说明：临-5 的权重归一主体（调和发散根因、w_k=(1/k)/H_K）已由工作台
`临5_高模式权重归一与有限截断.md` 做过。本文件不重复归一证明，只把
**与截断无关的权重比硬预言**显式化并 Lean 验证——这是本轮的新结果。

- w_k = (1/k)/H_K，H_K 为截断调和数（定义保留，具体值由外部标准数学保证）
- 权重比 w_k/w_1 = 1/k，与 H_K 的具体值、截断 K 均无关 ⇒ w_2/w_1 = 1/2
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.ModeWeightNormalization

noncomputable section

/-- 截断调和数 H_K = sum_{k=1}^K 1/k（k=0 项取 0）。 -/
def H (K : ℕ) : ℝ := (Finset.range (K + 1)).sum (fun k => (1 : ℝ) / k)

/-- 归一权重（未归一形式）w_k = (1/k)/H_K；归一性 sum w=1 属工作台已知结果。 -/
def w (K k : ℕ) : ℝ := ((1 : ℝ) / k) / H K

/-- 权重比 w_k/w_1 = 1/k，与截断 K、H_K 的具体值均无关（k≠0, H_K≠0）。 -/
theorem weight_ratio (K k : ℕ) (hk : k ≠ 0) (hK : H K ≠ 0) :
    w K k / w K 1 = (1 : ℝ) / k := by
  unfold w
  field_simp [hk, hK]
  norm_num

/-- 第二档/第一档 = 1/2（链内硬预言，与材料/截断无关）。 -/
theorem second_over_first (K : ℕ) (hK : H K ≠ 0) :
    w K 2 / w K 1 = (1 / 2 : ℝ) := by
  exact weight_ratio K 2 (by norm_num) hK

/-- 第三档/第一档 = 1/3。 -/
theorem third_over_first (K : ℕ) (hK : H K ≠ 0) :
    w K 3 / w K 1 = (1 / 3 : ℝ) := by
  exact weight_ratio K 3 (by norm_num) hK

end
end CQM.ModeWeightNormalization
