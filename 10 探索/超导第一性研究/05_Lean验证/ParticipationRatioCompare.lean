import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Data.Real.Basic

/-!
# R36: 跨块参与比标度核对的代数核（R31/R35·隔离区）

几何权重 R35: n_eff = (1+q)/(1-q) = coth t。
给定 n_eff = n，反解 q = (n-1)/(n+1)（n>1）。
调和权重 R31: n_eff = H_K²/H_{K,2} ~ (ln K)²/ζ(2)，其渐近由数值验证本 Lean 只做几何支的严格代数核。
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.ParticipationRatioCompare

noncomputable section

/-- 参与比函数（几何权重 q 形式）：(1+q)/(1-q)。 -/
def nEff (q : ℝ) : ℝ := (1 + q) / (1 - q)

/-- 几何支反解：q=(n-1)/(n+1) ⇒ nEff(q)=n（n≠-1）。 -/
theorem geom_inverse (n : ℝ) (hn1 : n + 1 ≠ 0) :
    nEff ((n - 1) / (n + 1)) = n := by
  unfold nEff
  field_simp [hn1]
  ring

/-- q 落在 (0,1)：n>1 ⇒ 0<(n-1)/(n+1)<1。 -/
theorem geom_q_range (n : ℝ) (hn : 1 < n) : 0 < (n - 1) / (n + 1) ∧ (n - 1) / (n + 1) < 1 := by
  have hnum : 0 < n - 1 := by linarith
  have hden : 0 < n + 1 := by linarith
  constructor
  · exact div_pos hnum hden
  · rw [div_lt_one hden]
    linarith

/-- 第一档占比 p1=1-q=2/(n+1)。 -/
theorem first_fraction (n : ℝ) (hn1 : n + 1 ≠ 0) :
    1 - (n - 1) / (n + 1) = 2 / (n + 1) := by
  field_simp [hn1]
  ring

/-- 单调性：n 增 ⇒ 反解 q 增（支撑增长）。 -/
theorem geom_inverse_monotone (n1 n2 : ℝ) (hn1 : 1 < n1) (h12 : n1 < n2) :
    (n1 - 1) / (n1 + 1) < (n2 - 1) / (n2 + 1) := by
  have hd1 : 0 < n1 + 1 := by linarith
  have hd2 : 0 < n2 + 1 := by linarith
  rw [div_lt_div_iff₀ hd1 hd2]
  ring_nf
  linarith

end
end CQM.ParticipationRatioCompare
