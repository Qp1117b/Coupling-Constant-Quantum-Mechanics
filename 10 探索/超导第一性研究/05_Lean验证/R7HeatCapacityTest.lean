/-
  预注册判定 R7：比热跳变普适常数盲测的代数骨架
  =================================================
  承载第95轮预言 ΔC/γTc=12/(7ζ(3))=1.426 与三项预注册判据的代数结构：
    P1 弱耦合相对偏差界；P2 分类均值单调；P3 同向（相关系数正）。
  数值在 04_计算验证/R7_比热跳变普适常数盲测.py 中独立核对。

  外部依据（只作工具）：IJPM 2026 表 + WMI 讲义 Table2 + Johnston arXiv:1304.2275。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

namespace CQM.R7HeatCapacity

noncomputable section

/-- CQM 第95轮弱耦合预言 $\Delta C/\gamma T^*=12/(7\zeta_3)$。 -/
def predictedJump : ℝ := 12 / (7 * 1.202056903159594)

lemma jump_bounds : 1.426 < predictedJump ∧ predictedJump < 1.427 := by
  unfold predictedJump
  norm_num

lemma jump_pos : 0 < predictedJump := by
  unfold predictedJump
  norm_num

/-- P1 判据：实测值与预言的相对偏差 ≤ 8% 等价 $|x-p| \le 0.08p$。 -/
def withinTol (x : ℝ) : Prop := |x - predictedJump| ≤ 0.08 * predictedJump

/-- Al 实测 1.45 在容差内。 -/
lemma al_pass : withinTol 1.45 := by
  unfold withinTol predictedJump
  norm_num

/-- Cd 实测 1.36 在容差内。 -/
lemma cd_pass : withinTol 1.36 := by
  unfold withinTol predictedJump
  norm_num

/-- P2 判据：三类均值严格单调 weak < inter < strong。 -/
def monotoneClasses (mw mi ms : ℝ) : Prop := mw < mi ∧ mi < ms

lemma p2_witness : monotoneClasses 1.405 1.64 2.34 := by
  unfold monotoneClasses
  constructor <;> norm_num

/-- 强耦合实测 (Pb) 应显著高于弱耦合上限（单调方向）。 -/
lemma strong_above_weak (pb al : ℝ) (hpb : 2.6 < pb) (hal : al < 1.5) : al < pb := by linarith

/-- P3 判据：比热跳变与 gap ratio 同向（协方差正）的代数骨架：
    两变量同增 ⇒ 乘积差正。 -/
def sameDirection (j1 j2 g1 g2 : ℝ) : Prop :=
  (j2 - j1) * (g2 - g1) > 0

lemma p3_witness : sameDirection 1.45 2.71 3.4 4.3 := by
  unfold sameDirection
  norm_num

end
end CQM.R7HeatCapacity
