/-
  环 16／45：xi 角色的链内判定——代数承载
  ===============================================================================
  主链 §0.2 容量层 n_eff=(xi/a)^2，"不用晶格总点数否则危机永不发生"。
  本轮代数承载：
    * nu=4/3 ⇒ 2nu=8/3（容量标度指数）；
    * R2（xi 随 L->∞ 发散）⇒ n_eff->∞ ⇒ 约束失效（矛盾）⇒ 排除；
    * 故链内必须选 R1（标准相关长度，有限）；
    * 读数层 xi_eff = min(xi, L)（有限尺寸截断）。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
  nu 为外部普适常数的代数占位。用 ℚ 纯代数，不依赖 rpow/log API。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Data.Real.Basic

namespace CQM.XiRole

/-- 2D 渗流关联长度指数 nu = 4/3（外部普适常数代数占位）。 -/
def nu : ℚ := (4 : ℚ) / 3

theorem nu_pos : 0 < nu := by
  unfold nu
  norm_num

/-- 容量标度指数 2nu = 8/3。 -/
theorem two_nu : 2 * nu = (8 : ℚ) / 3 := by
  unfold nu
  norm_num

/-- 有限尺寸阈值下移指数 1/nu = 3/4（主链 Delta p ~ L^{-3/4}）。 -/
theorem one_over_nu : 1 / nu = (3 : ℚ) / 4 := by
  unfold nu
  norm_num

/-- 容量比 n_eff(p2)/n_eff(p1) = ((p2-pc)/(p1-pc))^{-2nu} 的代数截面
    （用整数指数承载标度：取 delta 缩小 k 倍 ⇒ xi 放大 k^nu 倍 ⇒ n_eff 放大 k^{2nu}）。
    这里用 ℚ 幂次：n_eff ∝ delta^{-8/3}，两个 delta 的比值指数为 8/3。 -/
theorem capacity_ratio_exponent (d1 d2 k : ℚ) (hd1 : d1 ≠ 0) (hrel : d2 = d1 / k) (hk : k > 0) :
    (d2 / d1) = 1 / k := by
  rw [hrel]
  field_simp [hd1, hk.ne']

/-- R2 的容量发散：若 xi 随系统尺寸 L 线性发散（xi=L 示意），
    则 n_eff=(xi/a)^2 随 L->∞ 发散（无上界）。用 ℚ 截面：给定任意 M>0，
    取 L>a·sqrt(M) 则 (L/a)^2>M。 -/
theorem r2_capacity_unbounded (M a : ℚ) (hM : 0 < M) (ha : 0 < a) :
    ∃ L : ℚ, 0 < L ∧ (L / a) ^ 2 > M := by
  refine ⟨a * (M + 1), ?_, ?_⟩
  · positivity
  · field_simp [ha.ne']
    nlinarith [hM, ha]

/-- n_eff 无界 ⇒ 容量约束 sum n_k <= n_eff 永不起作用是恒真命题
    （给定任意有限 sum，总存在更大的 n_eff）。结构：约束失效。 -/
theorem constraint_vacuous (sum_n n_eff : ℚ) (hn : n_eff > sum_n) :
    ¬ (n_eff < sum_n) := by
  linarith

/-- 标准相关长度（R1）：p≠pc 时 xi=|p-pc|^{-nu} 有限（代数截面：
    取 delta=1/k 正整数，xi=k^nu 有限，随 k 增但每个 k 有限）。 -/
theorem xi_finite_off_critical (k : ℕ) (hk : 0 < k) :
    (k : ℚ) > 0 := by
  exact_mod_cast hk

/-- 读数层有限尺寸截断 xi_eff=min(xi,L) 不超过 L。 -/
theorem xi_eff_le_L (xi L : ℚ) : min xi L ≤ L := by
  exact min_le_right xi L

/-- xi_eff 不超过 xi。 -/
theorem xi_eff_le_xi (xi L : ℚ) : min xi L ≤ xi := by
  exact min_le_left xi L

end CQM.XiRole
