/-
  R36：参与比作截断候选——n_eff 的界
  ============================================================
  临-21：n_eff = 1/sum p_i^2，1<=n_eff<=|supp p|。
  本文件在 3 点域上证明归一化概率的 n_eff 界；w1 随 K 减复用 R33 的
  WeightNormalization 结论（此处不重复定义，仅在注释引用）。

  不证明：K=n_eff 的识别、临-5/临-21 闭合、p_i 的物理来源。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

namespace CQM.ParticipationCutoff

noncomputable section

/-- 三点域的参与比（要求 p1+p2+p3=1）。 -/
def neff3 (p1 p2 p3 : ℝ) : ℝ := 1 / (p1 ^ 2 + p2 ^ 2 + p3 ^ 2)

/-- 概率和平方和的基本界：1/3 <= sum p_i^2 <= 1。 -/
theorem sumsq_bounds (p1 p2 p3 : ℝ)
    (h1 : 0 ≤ p1) (h2 : 0 ≤ p2) (h3 : 0 ≤ p3)
    (hs : p1 + p2 + p3 = 1) :
    (1 / 3 : ℝ) ≤ p1 ^ 2 + p2 ^ 2 + p3 ^ 2 ∧ p1 ^ 2 + p2 ^ 2 + p3 ^ 2 ≤ 1 := by
  have h12 : 0 ≤ (p1 - p2) ^ 2 := sq_nonneg (p1 - p2)
  have h23 : 0 ≤ (p2 - p3) ^ 2 := sq_nonneg (p2 - p3)
  have h31 : 0 ≤ (p3 - p1) ^ 2 := sq_nonneg (p3 - p1)
  have hp1le : p1 ^ 2 ≤ p1 := by nlinarith [mul_nonneg h1 (sub_nonneg.mpr (by nlinarith : p1 ≤ 1))]
  have hp2le : p2 ^ 2 ≤ p2 := by nlinarith [mul_nonneg h2 (sub_nonneg.mpr (by nlinarith : p2 ≤ 1))]
  have hp3le : p3 ^ 2 ≤ p3 := by nlinarith [mul_nonneg h3 (sub_nonneg.mpr (by nlinarith : p3 ≤ 1))]
  constructor <;> nlinarith

/-- n_eff 在 [1,3]（三点域）；一般域为 [1,N]（IPR 标准，B 类）。 -/
theorem neff_bounds (p1 p2 p3 : ℝ)
    (h1 : 0 ≤ p1) (h2 : 0 ≤ p2) (h3 : 0 ≤ p3)
    (hs : p1 + p2 + p3 = 1) :
    1 ≤ neff3 p1 p2 p3 ∧ neff3 p1 p2 p3 ≤ 3 := by
  rcases sumsq_bounds p1 p2 p3 h1 h2 h3 hs with ⟨hlo, hhi⟩
  have hpos : 0 < p1 ^ 2 + p2 ^ 2 + p3 ^ 2 := by nlinarith
  unfold neff3
  constructor
  · rw [le_div_iff₀ hpos]
    nlinarith
  · rw [div_le_iff₀ hpos]
    nlinarith

end
end CQM.ParticipationCutoff
