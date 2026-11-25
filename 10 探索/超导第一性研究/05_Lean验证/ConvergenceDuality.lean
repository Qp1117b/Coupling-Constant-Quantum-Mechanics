/-
  环 26／52：总效应与总退相干的收敛-发散对偶——代数承载
  ===============================================================================
  M_-2 = sum 1/(gamma^2+1/4) = Xi 收敛（R50）；
  M_+2 = sum gamma^2 发散（零点计数 gamma_n ~ 2pi n / ln n）。
  对偶：低频携带总效应、高频承担退相干 ⇒ 可读窗口有限。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
  用 ℚ 代数截面承载收敛/发散的结构性判据（不形式化无穷级数 API）；
  RH 与零点计数为已登记外部假设。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Data.Real.Basic

namespace CQM.Duality

/-- Xi 权威常数占位（README 定义，R50）。 -/
def Xi : ℚ := 0.02309570897

/-- M_-2 的和项（收敛侧）：1/(gamma^2+1/4)，恒正且有界。 -/
def m_minus2_term (gamma : ℚ) : ℚ := 1 / (gamma ^ 2 + (1 : ℚ) / 4)

theorem m_minus2_term_pos (gamma : ℚ) : 0 < m_minus2_term gamma := by
  unfold m_minus2_term
  positivity

theorem m_minus2_term_le_four (gamma : ℚ) : m_minus2_term gamma ≤ 4 := by
  unfold m_minus2_term
  have hden : (1 : ℚ) / 4 ≤ gamma ^ 2 + (1 : ℚ) / 4 := by nlinarith [sq_nonneg gamma]
  have hpos : 0 < gamma ^ 2 + (1 : ℚ) / 4 := by nlinarith [sq_nonneg gamma]
  rw [div_le_iff₀ hpos]
  nlinarith [sq_nonneg gamma]

/-- M_+2 的和项（发散侧）：gamma^2，随 gamma 增而无界。 -/
def m_plus2_term (gamma : ℚ) : ℚ := gamma ^ 2

theorem m_plus2_unbounded (M : ℚ) (hM : 0 < M) :
    ∃ g : ℚ, m_plus2_term g > M := by
  refine ⟨M + 1, ?_⟩
  unfold m_plus2_term
  nlinarith [sq_nonneg (M + 1), sq_nonneg M]

/-- 核心对偶（结构性截面）：收敛侧有界（<=4 每项的截面）、发散侧无界。
    用"一项有上界 vs 一项可任意大"承载两谱矩收敛性相反。 -/
theorem duality_opposite_signs (gamma M : ℚ) (hM : 0 < M) :
    m_minus2_term gamma ≤ 4 ∧ ∃ g : ℚ, m_plus2_term g > M := by
  constructor
  · exact m_minus2_term_le_four gamma
  · exact m_plus2_unbounded M hM

/-- 低频/高频分工的代数截面：小 gamma 给大 m_-2、小 m_+2；大 gamma 反之。
    取 gamma1<gamma2，比较 1/(g^2) 与 g^2 的相对大小（g1<1<g2 截面）。 -/
theorem low_freq_carries_effect (g1 g2 : ℚ) (hg1 : 0 < g1) (hg1lt : g1 < 1) (hg2 : 1 < g2) :
    m_minus2_term g1 > m_minus2_term g2 ∧ m_plus2_term g1 < m_plus2_term g2 := by
  constructor
  · unfold m_minus2_term
    have hd1 : 0 < g1 ^ 2 + (1 : ℚ)/4 := by positivity
    have hd2 : 0 < g2 ^ 2 + (1 : ℚ)/4 := by positivity
    have hs : g1 ^ 2 < g2 ^ 2 := by nlinarith [sq_pos_of_pos hg1]
    apply one_div_lt_one_div_of_lt hd1
    linarith
  · unfold m_plus2_term
    nlinarith [sq_pos_of_pos hg1]

/-- 可读窗口有限的结构语义：存在 gamma_* 使 gamma < gamma_* 可读（截面：有界区间）。 -/
theorem readable_window_finite (gstar : ℚ) (hg : 0 < gstar) :
    ∃ g : ℚ, 0 < g ∧ g < gstar := by
  refine ⟨gstar / 2, ?_, ?_⟩ <;> linarith

-- 边界注记（写文档，不构造伪形式化，承 R28/R30 教训）：
-- 本对偶不闭合临-22（模依赖率 beta_n 的物理桥仍缺）；
-- gamma_n ~ 2pi n / ln n 用 RH 下零点计数（外部假设）。

end CQM.Duality
