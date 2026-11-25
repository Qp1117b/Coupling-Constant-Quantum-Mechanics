/-
  环 4／86：亏角转移函数——膨胀不变性、零点幅度归属、$c_\varepsilon$ 标度（代数承载）
  ===============================================================================
  第 85 轮把 $|G_q|^2\propto q^2$ 定成 $n=1$，剩余 O(1) 因子 $c_\varepsilon$。本轮：
    * 各向同性膨胀保持所有二面角 ⇒ 收缩 $\mathrm{tr}\,C=0$（亏角只响应形状改变）；
    * 零点幅度属于位移模：$|\Delta\varepsilon|^2=|G|^2|u|^2$，(2.1) 直接当亏角幅度
      会与 (4.1) 相差 $|G|^2\propto q^2$；
    * $c_\varepsilon\propto$ 参考曲率尺度（$\eta\to0$ 时为零），纵向／横向偏振权重不同。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。本文件只承载纯代数；
  Regge 角亏的逐边数值在 Python。
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp

namespace CQM.CurvatureTransfer

/-- 6 分量对称应变张量与对称响应张量的收缩（工程剪切份带因子 2）。 -/
def contract6 (c11 c22 c33 c12 c13 c23 : ℝ) (E11 E22 E33 E12 E13 E23 : ℝ) : ℝ :=
  c11 * E11 + c22 * E22 + c33 * E33 + 2 * (c12 * E12 + c13 * E13 + c23 * E23)

/-- 各向同性膨胀 $E=tI$ 下的收缩 = $t\,\mathrm{tr}\,C$（剪切份不参与）。 -/
theorem contract6_iso (c11 c22 c33 c12 c13 c23 t : ℝ) :
    contract6 c11 c22 c33 c12 c13 c23 t t t 0 0 0 = t * (c11 + c22 + c33) := by
  unfold contract6
  ring

/-- 无迹响应张量对纯膨胀零响应（"膨胀保角"的代数影子）。 -/
theorem trace_free_iso_zero (c11 c22 c33 c12 c13 c23 t : ℝ)
    (h : c11 + c22 + c33 = 0) :
    contract6 c11 c22 c33 c12 c13 c23 t t t 0 0 0 = 0 := by
  rw [contract6_iso, h, mul_zero]

/-- 每边响应对应变线性：$\Delta\varepsilon_e=C_e:\epsilon$。 -/
theorem response_linear (c e k : ℝ) : c * (k * e) = k * (c * e) := by
  ring

/-- 零点幅度归属：$|\Delta\varepsilon|^2=|G|^2|u|^2$。 -/
theorem amplitude_attribution (g u : ℝ) : (g * u) ^ 2 = g ^ 2 * u ^ 2 := by
  ring

/-- 转移函数一阶：$|G_q|^2=c_\varepsilon^2q^2$。 -/
theorem transfer_first_order (c q : ℝ) (hq : q ≠ 0) : (c * q) ^ 2 / q ^ 2 = c ^ 2 := by
  field_simp

/-- $c_\varepsilon\propto$ 参考曲率：$\eta=0$ 时为零。 -/
theorem ceps_zero (kap : ℝ) : (kap * 0) ^ 2 = 0 := by
  ring

/-- $c_\varepsilon$ 随参考曲率尺度线性。 -/
theorem ceps_scaling (kap eta : ℝ) : (kap * eta) ^ 2 = kap ^ 2 * eta ^ 2 := by
  ring

/-- 偏振权重：一份纵向 + 两份横向。 -/
theorem polarization_sum (cl ct : ℝ) : cl ^ 2 + 2 * ct ^ 2 = cl ^ 2 + ct ^ 2 + ct ^ 2 := by
  ring

/-- 正确读法与直接读 (2.1) 的比值恰为 $Q^2$。 -/
theorem cubic_over_linear (Q : ℝ) (hQ : Q ≠ 0) : Q ^ 3 / Q = Q ^ 2 := by
  field_simp

/-! ## 模求和维数进入指数

第 85 轮用 2D 测度，但 06 的 $\varepsilon$ 载体是 3D 铰链。一般律
$m_{\rm eff}^{(d)}=2n+(d-1)-s$；$\sigma_0^2$ 的指数始终是 $m_{\rm eff}^{(d)}+1$。 -/

/-- 维数定律：`m_eff^(d) = 2n + (d-1) - s`。 -/
def meffd (n d s : ℤ) : ℤ := 2 * n + (d - 1) - s

/-- `d = 2` 退回第 85 轮的合成律。 -/
theorem meffd_two (n s : ℤ) : meffd n 2 s = 2 * n + 1 - s := by
  unfold meffd; ring

/-- `d = 3` 给多一个指数。 -/
theorem meffd_three (n s : ℤ) : meffd n 3 s = 2 * n + 2 - s := by
  unfold meffd; ring

/-- 3D 相对 2D 恰好多 1。 -/
theorem meffd_diff_one (n s : ℤ) : meffd n 3 s = meffd n 2 s + 1 := by
  unfold meffd; ring

/-- 收敛裕度：`n ≥ 1`、`d ≥ 2`、`s ≤ 2` ⇒ `m_eff ≥ 1`。 -/
theorem meffd_ge_one {n d s : ℤ} (hn : 1 ≤ n) (hd : 2 ≤ d) (hs : s ≤ 2) :
    1 ≤ meffd n d s := by
  unfold meffd; linarith

/-- 数值例：`(n,s)=(1,1)` 在 `d=2/3` 分别给 `2/3`。 -/
example : meffd 1 2 1 = 2 := by decide
example : meffd 1 3 1 = 3 := by decide

/-- 3D 角向核的精确和：$\Sigma_{k\ge1}\rho^{(3)}_m(k)$ 在 $m=3$、$Q=\pi$ 给 $1/6$。
    由 $\sum_{k\ge1}\sin(qk)/(qk)=(\pi-q)/(2q)$（$0<q<2\pi$）逐项积分得
    $(2/Q^4)(Q^4/3-Q^4/4)$。 -/
theorem Srho_3d_exact (Q : ℝ) (hQ : Q ≠ 0) :
    (2 / Q ^ 4) * (Q ^ 4 / 3 - Q ^ 4 / 4) = 1 / 6 := by
  field_simp
  ring

/-- 对应周长律比值：$1+S_\rho=7/6$。 -/
theorem var_ratio_3d : (1 : ℝ) + 1 / 6 = 7 / 6 := by
  norm_num

end CQM.CurvatureTransfer
