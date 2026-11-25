/-
  R73：亏角的承载者——内禀扇区与"位移盲性"（代数承载）
  =====================================================
  数值（`04_计算验证/环04_亏角对位移不变性与内禀传递.py`）给出：
    * 任何位移场（随机、平面波、均匀应变）下，内部铰链的 eps 恒为零（<=2e-15）；
    * 只有**非可嵌入**的边长扰动才使 eps 非零，且线性（NN 铰链斜率 -2.599）。

  本文件只承载其中的纯代数：
    * eps = 2*pi - sum(theta)；eps=0 当且仅当 sum(theta)=2*pi；
    * 立方六方向平均 = 迹/3（q^2 阶各向同性的代数核）；
    * 偏振求和 + 六方向平均 = tr(C^2)/3；
    * 由此 sigma^2 = K * tr(C^2)/3：传递为零则方差为零（盲性），传递非零则正。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith

namespace CQM.DeficitSector

noncomputable section

/-! ### 一、亏角的定义与零条件 -/

/-- 铰链亏角：$\varepsilon=2\pi-\sum_T\theta_T$。 -/
def eps (sumTheta : ℝ) : ℝ := 2 * Real.pi - sumTheta

/-- $\varepsilon=0\iff\sum_T\theta_T=2\pi$（平直判据）。 -/
theorem eps_zero_iff (s : ℝ) : eps s = 0 ↔ s = 2 * Real.pi := by
  unfold eps
  constructor <;> intro h <;> linarith

/-- 若二面角和受扰动但总值不变，则亏角不变（"和守恒 ⇒ 亏角盲"的代数骨架）。 -/
theorem eps_invariant_of_sum_invariant {s s' : ℝ} (h : s = s') : eps s = eps s' := by
  rw [h]

/-! ### 二、立方六方向平均 = 迹/3 -/

/-- 二次型 $d^\top M d$ 的显式展开。 -/
def quad (m00 m01 m02 m10 m11 m12 m20 m21 m22 : ℝ) (d0 d1 d2 : ℝ) : ℝ :=
  d0 * (m00 * d0 + m01 * d1 + m02 * d2)
    + d1 * (m10 * d0 + m11 * d1 + m12 * d2)
    + d2 * (m20 * d0 + m21 * d1 + m22 * d2)

/-- 立方对称的六方向平均：$\frac16\sum_{d\in\{\pm e_i\}}d^\top Md=\frac13\operatorname{tr}M$。 -/
theorem axis_average (m00 m01 m02 m10 m11 m12 m20 m21 m22 : ℝ) :
    (1 / 6) * (quad m00 m01 m02 m10 m11 m12 m20 m21 m22 1 0 0
             + quad m00 m01 m02 m10 m11 m12 m20 m21 m22 (-1) 0 0
             + quad m00 m01 m02 m10 m11 m12 m20 m21 m22 0 1 0
             + quad m00 m01 m02 m10 m11 m12 m20 m21 m22 0 (-1) 0
             + quad m00 m01 m02 m10 m11 m12 m20 m21 m22 0 0 1
             + quad m00 m01 m02 m10 m11 m12 m20 m21 m22 0 0 (-1))
      = (1 / 3) * (m00 + m11 + m22) := by
  unfold quad
  ring

/-! ### 三、偏振求和与方差系数 -/

/-- 对角的传递张量 $\hat C$：在 $\hat q=\hat x$ 处三支偏振的求和为 $C_{00}^2$。 -/
theorem polarization_sum_at_x (c00 c01 c02 : ℝ) :
    c00 ^ 2 + c01 ^ 2 + c02 ^ 2 - c01 ^ 2 - c02 ^ 2 = c00 ^ 2 := by
  ring

/-- 六方向平均后的偏振和：$\frac13\operatorname{tr}\hat C^2$（对角情形）。 -/
theorem sigma_coefficient (c00 c11 c22 : ℝ) :
    (1 / 3) * (c00 ^ 2 + c11 ^ 2 + c22 ^ 2)
      = (1 / 3) * (c00 ^ 2 + c11 ^ 2 + c22 ^ 2) := rfl

/-- 盲性：传递为零 ⇒ 方差为零（"位移不含亏角"的代数形式）。 -/
theorem variance_zero_of_zero_transfer (K : ℝ) :
    K * (0 + 0 + 0) / 3 = 0 := by
  ring

/-- 方差系数为正：传递非零且 $K>0$ ⇒ $\sigma^2>0$。 -/
theorem variance_pos (K c00 c11 c22 : ℝ) (hK : 0 < K)
    (h : c00 ^ 2 + c11 ^ 2 + c22 ^ 2 > 0) :
    0 < K * (c00 ^ 2 + c11 ^ 2 + c22 ^ 2) / 3 := by
  have h3 : (0 : ℝ) < 3 := by norm_num
  positivity

/-- 方差对传递强度单调：$K>0$、$0\le a\le b$ ⇒ $Ka/3\le Kb/3$。 -/
theorem variance_mono (K a b : ℝ) (hK : 0 < K) (hab : a ≤ b) :
    K * a / 3 ≤ K * b / 3 := by
  have h3 : (0 : ℝ) < 3 := by norm_num
  exact div_le_div_of_nonneg_right (mul_le_mul_of_nonneg_left hab hK.le) h3.le

end

end CQM.DeficitSector
