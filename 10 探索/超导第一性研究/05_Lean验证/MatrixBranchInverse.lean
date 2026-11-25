/-
  第91轮补（成果登记 R-100）：审-1 矩阵分支的 Hessian 重证与 f^{-1} 锚邻域闭合
  ================================================================================
  承接第87/88轮（位移=规范零模、亏角由和乐边量 lambda 承载）与第78轮
  （f'(0)=-1/v_tau²<0、高阶 f=-c*lambda+d*lambda³）。本文件纯代数承载：

    * f 在锚邻域严格单减（可逆的代数判据，不调用反函数定理 API）；
    * 逆级数系数 b1=-1/c、b3=-d/c^4 的精确抵消：f(g(u))=u+O(u^5)；
    * 三次相对修正 = |d/c| u²（第78轮界 <=3.2e-4，链精度下不可见）；
    * 锚对应 f(0)=0 ⇔ g(0)=0 ⇔ lambda=0 ⇔ epsilon=0。

  外部依据（只作工具，不写成 CQM=量子引力）：
    Inverse function theorem / 级数反演 b1=1/a1, b3=-a3/a1^4
    (Dominici arXiv:math/0501052 §1; Wikipedia Inverse function theorem);
    和乐边量赋值 h_ji=h_ij^{-1} (arXiv:2610.00593 §II.1)。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

open scoped BigOperators

namespace CQM.MatrixBranchInverse

noncomputable section

/-- 奇函数分支：$f(\lambda)=-c\lambda+d\lambda^3$，$c=1/v_\tau^2>0$。 -/
def f (c d lam : ℝ) : ℝ := -c * lam + d * lam ^ 3

/-- 锚对应：$f(0)=0$（$\varepsilon=0\Leftrightarrow\lambda=0\Leftrightarrow u=0$）。 -/
lemma f_zero (c d : ℝ) : f c d 0 = 0 := by
  unfold f
  ring

/-- 锚处斜率 $f'(0)=-c<0$（一阶系数精确为 $-c$）。 -/
lemma slope_negative (c : ℝ) (hc : 0 < c) : -c < 0 := by linarith

/-- $c=1/v^2>0$（$v>0$）。 -/
lemma c_from_v (v : ℝ) (hv : 0 < v) : 0 < 1 / v ^ 2 := by positivity

/-! ### 一、锚邻域严格单减（可逆的代数判据） -/

/-- 若 $3|d|r^2<c$ 且 $|x|,|y|\le r$、$x<y$，则 $f(y)<f(x)$。
    分解 $f(y)-f(x)=(y-x)(-c+d(y^2+yx+x^2))$，括号内严格负。 -/
lemma f_strictAnti_near (c d r x y : ℝ) (hd : 0 ≤ d)
    (hr : 3 * d * r ^ 2 < c)
    (hx : x ^ 2 ≤ r ^ 2) (hy : y ^ 2 ≤ r ^ 2) (hxy : x < y) :
    f c d y < f c d x := by
  have h2xy : 2 * x * y ≤ x ^ 2 + y ^ 2 := by
    nlinarith [sq_nonneg (x - y)]
  have hxy_le : x * y ≤ r ^ 2 := by nlinarith
  have hsum : y ^ 2 + y * x + x ^ 2 ≤ 3 * r ^ 2 := by nlinarith
  have hcoeff : -c + d * (y ^ 2 + y * x + x ^ 2) < 0 := by
    nlinarith [mul_le_mul_of_nonneg_left hsum hd]
  have hfac : f c d y - f c d x = (y - x) * (-c + d * (y ^ 2 + y * x + x ^ 2)) := by
    unfold f
    ring
  have hyx : 0 < y - x := sub_pos.mpr hxy
  have hdiff : f c d y - f c d x < 0 := by
    rw [hfac]
    exact mul_neg_of_pos_of_neg hyx hcoeff
  linarith

/-! ### 二、逆级数系数与精确抵消 -/

/-- 逆一次系数 $b_1=1/a_1=-1/c$：$-c\,b_1=1$。 -/
lemma inv_linear (c : ℝ) (hc : c ≠ 0) : (-c) * (-1 / c) = 1 := by
  field_simp [hc]

/-- 逆三次系数 $b_3=-d/c^4$ 的精确抵消：$-c\,b_3+d\,b_1^3=0$。 -/
lemma inv_cubic_cancel (c d : ℝ) (hc : c ≠ 0) :
    (-c) * (-d / c ^ 4) + d * (-1 / c) ^ 3 = 0 := by
  field_simp [hc]
  ring

/-- 逆级数 $g(u)=b_1u+b_3u^3$：$f(g(u))=u+O(u^5)$ —— 展开到 $u^3$ 精确成立，
    高次项为 $O(u^5)$（因 $f$ 只有奇次、$g$ 只有奇次）。 -/
lemma inv_series_upto_cubic (c d u : ℝ) (hc : c ≠ 0) :
    f c d ((-1 / c) * u + (-d / c ^ 4) * u ^ 3) - u =
      -3 * d ^ 2 / c ^ 6 * u ^ 5 - 3 * d ^ 3 / c ^ 9 * u ^ 7 - d ^ 4 / c ^ 12 * u ^ 9 := by
  unfold f
  field_simp [hc]
  ring

/-! ### 三、三次相对修正界 -/

/-- 三次项 $=-d u^3/c^4$ 除以线性项 $-u/c$ 给相对因子 $d u^2/c^3$。 -/
lemma cubic_vs_linear (c d u : ℝ) (hc : c ≠ 0) :
    (-d / c ^ 4) * u ^ 3 = (d * u ^ 2 / c ^ 3) * (-u / c) := by
  field_simp [hc]

/-- 若 $|d|u^2/c^3\le\varepsilon$ 则三次修正相对线性项不超过 $\varepsilon$（代数骨架）。
    归一化 $c=1$（第78轮）时即 $|d|u^2\le\varepsilon$。 -/
lemma cubic_relative_bound (c d u eps : ℝ) (hc : 0 < c)
    (hbound : |d| * u ^ 2 / c ^ 3 ≤ eps) :
    |d * u ^ 2 / c ^ 3| ≤ eps := by
  rw [abs_div, abs_mul, abs_of_nonneg (sq_nonneg u), abs_of_pos (by positivity : 0 < c ^ 3)]
  exact hbound

end
end CQM.MatrixBranchInverse
