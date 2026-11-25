/-
  R40：审-7 三处"2"的对象辨析——不同类型与不同归一
  ============================================================
  2e（电荷）、ζ(-2) 的序号（整数）、N(0)（态密度）分属不同对象，
  用不同归一才能读成无量纲数；自然单位下 DOS 不等于 2。
  本文件只承载代数与不等式，不证明物理同一，不闭合缺口。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

namespace CQM.ThreeTwos

noncomputable section

/-- 配对荷（有电荷量纲），与零点序号、态密度分属不同类型。 -/
structure PairCharge where
  q : ℝ

/-- 平凡零点序号（无量纲整数）。 -/
structure ZeroIndex where
  n : ℕ

/-- 费米面态密度（有量纲），此处只存其数值。 -/
structure DosValue where
  rho : ℝ

/-- 用电荷单位 e 归一，2e 给 2。 -/
theorem pair_norm_two (e : ℝ) (he : e ≠ 0) :
    (⟨2 * e⟩ : PairCharge).q / e = 2 := by
  field_simp

/-- 零点序号天然就是整数 2，无需单位归一。 -/
theorem zero_index_two : (⟨2⟩ : ZeroIndex).n = 2 := rfl

/-- 条件式：若 $4\\pi^2\\ne1$，则 DOS 自然值不等于 2（本安装无 π 数值界定理，数值界由脚本承担）。 -/
theorem dos_natural_ne_two (hpi : 4 * Real.pi ^ 2 ≠ 1) :
    1 / (2 * Real.pi ^ 2) ≠ 2 := by
  intro heq
  have hden : 2 * Real.pi ^ 2 ≠ 0 := by positivity
  field_simp [hden] at heq
  apply hpi
  nlinarith

end
end CQM.ThreeTwos
