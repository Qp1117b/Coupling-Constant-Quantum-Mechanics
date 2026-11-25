/-
  R42：审-1 局部逆的全局边界——三次近似的导数变号阈值
  ============================================================
  工作台 R100：f(λ)=-cλ+dλ³，f'(λ)=-c+3dλ²；局部可逆在 λ=0，
  全局单射要求 f' 在区间内不变号。本文件严格证明变号阈值
  |λ| < sqrt(c/(3d)) 的代数，不证明 f 的物理来源，不闭合缺口。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

namespace CQM.InverseRadius

noncomputable section

/-- 导数：$f'(\\lambda)=-c+3d\\lambda^2$。 -/
def deriv (c d l : ℝ) : ℝ := -c + 3 * d * l ^ 2

/-- 导数为负当且仅当 $\\lambda^2<c/(3d)$。 -/
theorem deriv_neg_iff (c d l : ℝ) (hd : 0 < d) :
    deriv c d l < 0 ↔ l ^ 2 < c / (3 * d) := by
  unfold deriv
  have h3d : 0 < 3 * d := by positivity
  constructor
  · intro h
    have hmul : l ^ 2 * (3 * d) < c := by nlinarith
    exact (lt_div_iff₀ h3d).mpr hmul
  · intro h
    have hmul : l ^ 2 * (3 * d) < c := (lt_div_iff₀ h3d).mp h
    have hmul' : 3 * d * l ^ 2 < c := by nlinarith
    linarith

/-- 阈值点：$\\lambda^2=c/(3d)$ 时导数为零。 -/
theorem deriv_zero_at_threshold (c d : ℝ) (hc : 0 ≤ c) (hd : 0 < d) :
    deriv c d (Real.sqrt (c / (3 * d))) = 0 := by
  unfold deriv
  have hnonneg : 0 ≤ c / (3 * d) := by positivity
  rw [Real.sq_sqrt hnonneg]
  field_simp
  ring

end
end CQM.InverseRadius
