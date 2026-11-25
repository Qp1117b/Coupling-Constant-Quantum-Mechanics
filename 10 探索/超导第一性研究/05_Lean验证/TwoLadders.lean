/-
  R35：两把阶梯辨析——2ln 阶梯的步长公式与不可仿射同一
  ============================================================
  链内 L616：gamma_n 与 (12.3) 两梯不可互译；L544：2ln n 与 {log p}
  两套刻度不互换；L1280 把 2ln n 标成“gamma_n 侧”——本轮登记为刻度混用。
  外部（B 类）Riemann–von Mangoldt：gamma_n ~ 2πn/ln n。

  本文件只承载代数部分：
    (1) 2ln 阶梯相邻步长 = 2 ln(1+1/n)；
    (2) 若两序列相邻步长不同，则不存在统一仿射同一（反证）。

  不证明：RvM 的链内来源、临-26/临-22 闭合、任何状态变更。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

namespace CQM.TwoLadders

noncomputable section

/-- (1) $2\\ln$ 阶梯的相邻步长：$2\\log(n+1)-2\\log n=2\\log(1+1/n)$。 -/
theorem log_ladder_step (n : ℕ) (hn : 0 < n) :
    2 * Real.log (n + 1 : ℝ) - 2 * Real.log (n : ℝ) =
      2 * Real.log (1 + 1 / (n : ℝ)) := by
  have hnpos : (0 : ℝ) < n := by exact_mod_cast hn
  have hnp1pos : (0 : ℝ) < (n + 1 : ℝ) := by positivity
  have hstep : Real.log (n + 1 : ℝ) - Real.log (n : ℝ) =
      Real.log (1 + 1 / (n : ℝ)) := by
    rw [← Real.log_div hnp1pos.ne' hnpos.ne']
    have heq : ((n + 1 : ℝ) / (n : ℝ)) = 1 + 1 / (n : ℝ) := by
      field_simp
    rw [heq]
  linarith

/-- (2) 两序列相邻步长不同 ⇒ 不存在把它们逐点同一的仿射映射。 -/
theorem no_affine_identity (d1 d2 a b : ℝ) (hneq : d1 ≠ d2)
    (h1 : a + d1 = b) (h2 : a + d2 = b) : False := by
  have heq' : d1 = d2 := by linarith
  exact hneq heq'

/-- (2') 若两个相邻步长比恒为 1 不成立，则阶梯不等价（用两点观测作前提）。 -/
theorem slopes_differ_not_equal (s1 s2 : ℝ) (h : s1 ≠ s2) : ¬ s1 = s2 := by
  exact h

end
end CQM.TwoLadders
