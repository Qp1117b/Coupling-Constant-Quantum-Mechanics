/-
  R37：参与比的一般权重恒等式
  ============================================================
  临-21 的参与比泛函：对未归一权重 w_i，
    n_eff = (sum w)^2 / sum w^2
  归一化 p_i=w_i/sum w 时退化为 1/sum p_i^2。
  本文件证明代数恒等式与整体标度不变性。

  不证明：w_i 的物理来源、临-21/临-5 闭合、任何状态变更。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

namespace CQM.ParticipationCoefficient

noncomputable section

/-- 三点未归一权重：$n_{eff}=(\\sum w)^2/\\sum w^2$。 -/
def neffW (w1 w2 w3 : ℝ) : ℝ :=
  (w1 + w2 + w3) ^ 2 / (w1 ^ 2 + w2 ^ 2 + w3 ^ 2)

/-- (1) 归一化权重形式：$p_i=w_i/S$ 时 $n_{eff}=1/\\sum p_i^2$。 -/
theorem neff_from_normalized (w1 w2 w3 : ℝ) (hS : w1 + w2 + w3 ≠ 0) :
    neffW w1 w2 w3 = 1 / ((w1 / (w1 + w2 + w3)) ^ 2 +
      (w2 / (w1 + w2 + w3)) ^ 2 + (w3 / (w1 + w2 + w3)) ^ 2) := by
  unfold neffW
  field_simp

/-- (2) 整体标度不变性：$w_i\\to c w_i$ 不改变 $n_{eff}$。 -/
theorem neff_scale_invariant (w1 w2 w3 c : ℝ) (hc : c ≠ 0) :
    neffW (c * w1) (c * w2) (c * w3) = neffW w1 w2 w3 := by
  unfold neffW
  field_simp

/-- (3) 等权饱和：$w_1=w_2=w_3\\ne0$ 时 $n_{eff}=3$。 -/
theorem neff_equal_three (w : ℝ) (hw : w ≠ 0) : neffW w w w = 3 := by
  unfold neffW
  field_simp
  norm_num

end
end CQM.ParticipationCoefficient
