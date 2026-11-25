/-
  目标区／57：两个 Tc 上界的定量比较——代数承载
  ===============================================================================
  T_A = min{T*, T_pair(pc)}（判据链，R16 闭合）
  T_B = (pi/2kB) Upsilon_bare(0) Q（Uemura，U.3）
  R = T_B / T_A；2D 小 Upsilon => R<1（B 紧）；3D 大 Upsilon => R>1（A 紧）。
  与环19 (11L.13) 维度表自洽。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
  用 ℚ 代数截面承载比值与不等式；材料量外生。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Data.Real.Basic

namespace CQM.TwoBounds

/-- 上界 A = min{T*, T_pair}，截面取 min 函数。 -/
def boundA (Tstar Tpair : ℚ) : ℚ := min Tstar Tpair

theorem boundA_le_both (Tstar Tpair : ℚ) :
    boundA Tstar Tpair ≤ Tstar ∧ boundA Tstar Tpair ≤ Tpair := by
  unfold boundA
  constructor <;> simp

/-- 上界 B = (pi/2) Upsilon Q，截面取系数 k>0。 -/
def boundB (k Upsilon Q : ℚ) : ℚ := k * Upsilon * Q

/-- 综合上界：Tc <= min{TA,TB}（合取）。截面：min <= 各自。 -/
theorem two_bounds (TA TB : ℚ) : min TA TB ≤ TA ∧ min TA TB ≤ TB := by
  constructor <;> simp

/-- 比值 R = TB/TA。 -/
def ratio (TB TA : ℚ) : ℚ := TB / TA

/-- 2D：Upsilon 小 ⇒ TB 小 ⇒ R<1（设 TA 固定正、TB<TA）。 -/
theorem R_lt_one_2D (TB TA : ℚ) (hTA : 0 < TA) (h : TB < TA) :
    ratio TB TA < 1 := by
  unfold ratio
  rw [div_lt_one hTA]
  exact h

/-- 3D：Upsilon 大 ⇒ TB 大 ⇒ R>1（设 TB>TA）。 -/
theorem R_gt_one_3D (TB TA : ℚ) (hTA : 0 < TA) (h : TA < TB) :
    ratio TB TA > 1 := by
  unfold ratio
  show 1 < TB / TA
  rw [one_lt_div hTA]
  exact h

/-- TB 随 Upsilon 单调增（k>0, Q>0）：维度判定的结构基础。 -/
theorem boundB_mono_Upsilon (k Q U1 U2 : ℚ) (hk : 0 < k) (hQ : 0 < Q) (h : U1 < U2) :
    boundB k U1 Q < boundB k U2 Q := by
  unfold boundB
  have hkQ : 0 < k * Q := mul_pos hk hQ
  nlinarith

/-- 自洽性截面：2D（小 Upsilon => TB 小）与 3D（大 Upsilon => TB 大）覆盖两种主导。
    结构命题：R<1 或 R>1（或 =1 边界），穷尽。 -/
theorem dichotomy (TB TA : ℚ) : ratio TB TA < 1 ∨ ratio TB TA = 1 ∨ ratio TB TA > 1 := by
  by_cases h1 : ratio TB TA < 1
  · exact Or.inl h1
  · by_cases h2 : ratio TB TA = 1
    · exact Or.inr (Or.inl h2)
    · exact Or.inr (Or.inr (lt_of_le_of_ne (le_of_not_gt h1) (Ne.symm h2)))

-- 边界注记（写文档，不构造伪形式化）：不给 Upsilon0/T* 数值；
-- 不证明外部 Uemura 律；维度判定与环19 (11L.13) 表自洽（写推导卡 §2.3）。

end CQM.TwoBounds
