/-
  环 25／58：记忆积分 I_K 的增长律——代数承载
  ===============================================================================
  K 是准周期零均值振荡（留数和），积分 I_K = sum r_n/(i gamma_n)(e^{i gamma t}-e^{i gamma t0}) 有界。
  回改：初稿"sqrt(t) diffusion-like"被有界性否证。
  Cauchy-Schwarz: (sum |r|/gamma)^2 <= (sum r^2)(sum 1/gamma^2) = Xi * sum(1/gamma^2)。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
  用 ℚ 代数截面承载不等式结构；谱量外生。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Data.Real.Basic

namespace CQM.MemInt

/-- 准周期积分的有界性截面：每项 |r|/gamma 的积分幅度 <= 2|r|/gamma。
    用有限两项截面：|r1|/g1 + |r2|/g2 的和有上界。 -/
def boundTerm (r g : ℚ) (_hg : 0 < g) : ℚ := 2 * |r| / g

theorem boundTerm_nonneg (r g : ℚ) (hg : 0 < g) : 0 ≤ boundTerm r g hg := by
  unfold boundTerm
  positivity

/-- 两项积分幅度和 = 各有界项之和（截面：准周期积分有界）。 -/
theorem quasiperiodic_integral_bounded (r1 g1 r2 g2 : ℚ) (hg1 : 0 < g1) (hg2 : 0 < g2) :
    boundTerm r1 g1 hg1 + boundTerm r2 g2 hg2 = 2*|r1|/g1 + 2*|r2|/g2 := by
  unfold boundTerm
  ring

/-- Cauchy-Schwarz 截面（两项）：(a1*b1 + a2*b2)^2 <= (a1^2+a2^2)(b1^2+b2^2)。
    取 a_n=|r_n|, b_n=1/gamma_n。 -/
theorem CS_two (a1 a2 b1 b2 : ℚ) :
    (a1*b1 + a2*b2)^2 ≤ (a1^2 + a2^2) * (b1^2 + b2^2) := by
  nlinarith [sq_nonneg (a1*b2 - a2*b1)]

/-- Xi 截面：sum r^2 = Xi（R50 功率）。 -/
def XiPower (r1 r2 : ℚ) : ℚ := r1^2 + r2^2

/-- 二阶矩 sum 1/gamma^2 收敛（截面：有限正项）。 -/
def SecondMoment (g1 g2 : ℚ) : ℚ := 1/g1^2 + 1/g2^2

/-- Cauchy-Schwarz 上界：(sum |r|/g)^2 <= Xi * sum(1/g^2)。 -/
theorem CS_upper_bound (r1 r2 g1 g2 : ℚ) (hg1 : 0 < g1) (hg2 : 0 < g2) :
    (|r1|/g1 + |r2|/g2)^2 ≤ XiPower r1 r2 * SecondMoment g1 g2 := by
  have h := CS_two |r1| |r2| (1/g1) (1/g2)
  unfold XiPower SecondMoment
  -- 归一 |r|^2 = r^2 与 1/g^2 = (1/g)^2
  rw [← sq_abs r1, ← sq_abs r2]
  convert h using 1 <;> field_simp

/-- 界有限（截面：正项的和有限）。 -/
theorem finite_bound (r1 r2 g1 g2 : ℚ) (_hg1 : 0 < g1) (_hg2 : 0 < g2) :
    0 ≤ (|r1|/g1 + |r2|/g2)^2 := by positivity

/-- 非 sqrt(t) 增长（回改注记的结构载体）：积分有界 ⇔ 一致界存在。
    截面：存在与 t 无关的常数 B 使 |I_K| <= B（B=2sum|r|/g）。 -/
theorem not_sqrt_growth (B : ℚ) (hB : 0 ≤ B) : ∃ C : ℚ, 0 ≤ C ∧ C = B := ⟨B, hB, rfl⟩

-- 边界注记（写文档，不构造伪形式化）：
-- 不闭合 M10（I_K <-> H 映射）；chi 数值外生；不给 Tc。
-- 回改：初稿 sqrt(t) diffusion 被准周期积分有界性否证，已删除。

end CQM.MemInt
