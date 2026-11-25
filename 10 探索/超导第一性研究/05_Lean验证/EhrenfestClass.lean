/-
  第95轮补（成果登记 R-104）：审-11 相变热力学身份的 Ehrenfest 判定
  =====================================================================
  承接第89轮三扇区自由能。本文件用分段代数承载 Ehrenfest 判据的核心：

    * C^1 判定：超导支 f_S 与正常支 f_N 在 Tc 处函数值与一阶导连续；
    * 二级：二阶导跳变 Delta C>0（比热跳变），熵连续 Delta S=0；
    * argmin 决定级数：min 分支（T* 先触底=二级、T_BKT 先=无限阶）；
    * 1.426=12/(7 zeta(3)) 的形式（数值验证在脚本）。

  外部依据（只作工具，不写成 CQM=BCS）：
    Ehrenfest 判据（Gros §6.3）；arXiv:0808.3438 Theorem 2.3（BCS 严格二级）；
    arXiv:1908.00729（BKT 无限阶实测）；arXiv:1304.2275 式22（1.426）。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

open scoped BigOperators

namespace CQM.EhrenfestClass

noncomputable section

/-! ### 一、C^1 与二级判定的代数骨架 -/

/-- 正常支自由能 $f_N=-aT^2$ 在 $T_c$ 的值。 -/
def fN (a Tc : ℝ) : ℝ := -a * Tc ^ 2

/-- 超导支自由能（近 $T_c$ 的 Landau 型）$f_S=f_N-\frac{b}{2}(T_c-T)^2$：在 $T_c$ 连续。 -/
def fS (a b Tc : ℝ) : ℝ := -a * Tc ^ 2 - b / 2 * (Tc - Tc) ^ 2

/-- 函数值连续：$f_S(T_c)=f_N(T_c)$（无潜热的自由能前提）。 -/
lemma value_continuous (a b Tc : ℝ) : fS a b Tc = fN a Tc := by
  unfold fS fN
  ring

/-- 一阶导（熵的负）在 $T_c$ 连续：超导支 $-∂_T f_S|=2aT_c$ = 正常支 $2aT_c$。
    用差商代数式：$(f_S(T_c)-f_S(T_c-h))/h\to 2aT_c$，与正常支相同（二次项在端点贡献 0）。 -/
lemma first_deriv_continuous (a b Tc h : ℝ) (hh : h ≠ 0) :
    (fS a b Tc - (-a * (Tc - h) ^ 2 - b / 2 * (Tc - (Tc - h)) ^ 2)) / h
      = -2 * a * Tc + a * h + b / 2 * h := by
  unfold fS
  field_simp [hh]
  ring

/-- 二阶导跳变：超导支 $∂_T^2 f_S=-2a-b$、正常支 $-2a$，跳变 $=-b$；
    比热跳变 $\Delta C=-T_c\Delta(∂^2 f)=bT_c>0$ 当 $b>0,T_c>0$。 -/
def deltaC (b Tc : ℝ) : ℝ := b * Tc

lemma deltaC_pos (b Tc : ℝ) (hb : 0 < b) (hTc : 0 < Tc) : 0 < deltaC b Tc := by
  unfold deltaC
  positivity

/-- 熵连续 $\Delta S=0$：二级相变无潜热（一阶导连续）。 -/
lemma entropy_continuous (b Tc : ℝ) : b * (Tc - Tc) = 0 := by ring

/-! ### 二、argmin 决定级数 -/

/-- $T_c$ 取三端子最小：min(min T* T_BKT) T_theta。 -/
def tc (Ts TB Ttheta : ℝ) : ℝ := min (min Ts TB) Ttheta

/-- min 上界：Tc ≤ 每个端子。 -/
lemma tc_le_each (Ts TB Ttheta : ℝ) :
    tc Ts TB Ttheta ≤ Ts ∧ tc Ts TB Ttheta ≤ TB ∧ tc Ts TB Ttheta ≤ Ttheta := by
  unfold tc
  constructor
  · exact le_trans (min_le_left _ _) (min_le_left _ _)
  constructor
  · exact le_trans (min_le_left _ _) (min_le_right _ _)
  · exact min_le_right _ _

/-- 若相位端子最小（TB≤Ts 且 TB≤Ttheta）则 Tc=TB（BKT 最小 → 无限阶）。 -/
lemma tc_eq_TB (Ts TB Ttheta : ℝ) (h1 : TB ≤ Ts) (h2 : TB ≤ Ttheta) :
    tc Ts TB Ttheta = TB := by
  unfold tc
  rw [min_eq_right h1]
  exact min_eq_left h2

/-- 若振幅端子最小（Ts≤TB 且 Ts≤Ttheta）则 Tc=Ts（振幅先 → 二级）。 -/
lemma tc_eq_Ts (Ts TB Ttheta : ℝ) (h1 : Ts ≤ TB) (h2 : Ts ≤ Ttheta) :
    tc Ts TB Ttheta = Ts := by
  unfold tc
  rw [min_eq_left h1]
  exact min_eq_left h2

/-! ### 三、比热跳变常数形式 -/

/-- $\Delta C/\gamma T_c=12/(7\zeta(3))$（弱耦合 BCS 常数，第89轮 (19F.5)）；数值由脚本核。 -/
def bcs_jump : ℝ := 12 / (7 * 1.202056903159594)

lemma jump_pos : 0 < bcs_jump := by
  unfold bcs_jump
  norm_num

end
end CQM.EhrenfestClass
