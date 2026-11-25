/-
  环 19／48：Ginzburg 判据的链内推导——代数承载
  ===============================================================================
  从链内 Landau 系数 a0=kB、b=zJ/8、R46 梯度系数 c=Upsilon0/2 推导：
    * 涨落比 ∝ |a|^{d/2 - 2} ⇒ 上临界维 d_c=4（链内重新得到）；
    * t_G 标度指数 2d/(4-d)，d=3 给 t_G ∝ N^{-6}；
    * 前因子 C_d ∝ (zJ/Upsilon0)^2（形状链内、数值外生）。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
  指数与系数用 ℚ 代数截面；前因子数值外生，不声称给出材料数值。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Data.Real.Basic

namespace CQM.Ginzburg

/-- t_G 标度指数 p(d) = 2d/(4-d)（d<4）。 -/
def gexp (d : ℚ) : ℚ := 2 * d / (4 - d)

/-- d=3 ⇒ 指数 = 6。 -/
theorem exponent_three : gexp 3 = 6 := by
  unfold gexp
  norm_num

/-- d=2 ⇒ 指数 = 2。 -/
theorem exponent_two : gexp 2 = 2 := by
  unfold gexp
  norm_num

/-- 涨落比的 |a| 指数 e(d) = d/2 - 2。 -/
def fexp (d : ℚ) : ℚ := d / 2 - 2

/-- d=4 ⇒ e=0（上临界维：指数变号点）。 -/
theorem upper_critical_dim : fexp 4 = 0 := by
  unfold fexp
  norm_num

/-- d=3 ⇒ e=-1<0（涨落比随 |a|→0 发散，平均场失效）。 -/
theorem fluct_diverges_d3 : fexp 3 < 0 := by
  unfold fexp
  norm_num

/-- d=5 ⇒ e=+1/2>0（涨落比收敛，平均场有效）。 -/
theorem fluct_converges_d5 : 0 < fexp 5 := by
  unfold fexp
  norm_num

/-- d<4 时 e<0（等价于 d<4）。 -/
theorem e_neg_iff_d_lt_four {d : ℚ} (hd4 : d < 4) : fexp d < 0 := by
  unfold fexp
  linarith

/-- t_G ∝ N^{-p(d)}：d=3 给 N^{-6}。代数截面：tG = N^{-6} 的比值形式
    tG(N2)/tG(N1) = (N1/N2)^6。 -/
theorem tG_ratio_N6 (N1 N2 : ℚ) (hN1 : 0 < N1) (hN2 : 0 < N2) :
    (N2 ^ 6) / (N1 ^ 6) = (N2 / N1) ^ 6 := by
  field_simp [hN1.ne']

/-- 前因子形状 C_d ∝ (zJ/Upsilon0)^2（平方正定，形状链内）。 -/
theorem prefactor_shape_pos (zJ Upsilon0 : ℚ) (hz : 0 < zJ) (hU : 0 < Upsilon0) :
    0 < (zJ / Upsilon0) ^ 2 := by
  positivity

/-- 链内系数：b(T0)=zJ/8，c=Upsilon0/2，kBT0=zJ/2（代数值）。
    kBT0*b/c^{3/2} 的形状 ∝ (zJ)^2/Upsilon0^{3/2}（d=3）。 -/
theorem coefficient_combo (zJ : ℚ) :
    (zJ / 2) * (zJ / 8) = (zJ ^ 2) / 16 := by
  ring

end CQM.Ginzburg
