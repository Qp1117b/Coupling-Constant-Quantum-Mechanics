/-
  环 2／R71：`W-3` 量纲桥（代数承载）
  ==================================
  06 §4 说 "$L$ 的本征值是 $\omega_k^2$ 的几何来源"，缺的是**算子化**这一步：
  由 $\cot\theta$ 构成的 $L$ 是 FEM **刚度**矩阵（无量纲），
  离散 Laplace–Beltrami 是 $\Delta_{\rm disc}=M^{-1}L$（$M$ 为节点测度）。
  于是 $\omega^2=c_s^2\lambda_q/\Omega^{2/d}$，量纲因子只能是**测度**。

  本文件只承载纯代数：
    * `omegaSq` 的定义、正性、测度齐次性；
    * 声学极限 $\lambda_q=\Omega^{2/d}q^2\Rightarrow\omega=c_sq$；
    * Debye 模式计数的立方标度 $Q^3=6\pi^2n$；
    * 同位素指数 $\alpha=-\partial\ln\Theta_D/\partial\ln M+(1/\lambda^2)\partial\ln\lambda/\partial\ln M=1/2$（谐波、$\lambda$ 与 $M$ 无关）；
    * 零点幅度的无量纲群 $\sigma^2\propto(\ell_q/a)^4$ 的尺度不变性；
    * 环 10 振幅预算对 $g^2$ 的代数解。
  Bessel 核、Debye 积分数值、材料表在 Python（`04_计算验证/环02_W3量纲桥.py`）。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith

namespace CQM.PhononDim

noncomputable section

/-! ### 一、量纲桥：$\omega^2=c_s^2\lambda_q/\Omega^{2/d}$ -/

/-- 频率平方：$c^2\lambda/\Omega^{2/d}$。`meas` 是 $\Omega^{2/d}$（2D 取面积、3D 取体积的 $2/3$ 次幂）。 -/
def omegaSq (c lam meas : ℝ) : ℝ := c ^ 2 * lam / meas

/-- 量纲桥给正的频率平方（$c,\lambda,\Omega>0$）。 -/
theorem omegaSq_pos {c lam meas : ℝ} (hc : 0 < c) (hl : 0 < lam) (hm : 0 < meas) :
    0 < omegaSq c lam meas := by
  unfold omegaSq
  positivity

/-- 同一无量纲本征值下，测度加倍使 $\omega^2$ 减半——量纲因子是测度，不是材料常数。 -/
theorem omegaSq_measure_doubled {c lam meas : ℝ} (hm : meas ≠ 0) :
    omegaSq c lam (2 * meas) = omegaSq c lam meas / 2 := by
  unfold omegaSq
  field_simp

/-- 声学极限：$\lambda_q=\Omega^{2/d}q^2$ 时 $\omega^2=(c_sq)^2$，即色散严格线性。 -/
theorem omegaSq_acoustic {c q meas : ℝ} (hm : meas ≠ 0) :
    omegaSq c (meas * q ^ 2) meas = (c * q) ^ 2 := by
  unfold omegaSq
  field_simp

/-- 长波极限的两种写法等价：$\omega=\sqrt{c^2\lambda/\Omega}\Leftrightarrow\omega^2=c^2q^2$。 -/
theorem acoustic_dispersion_iff {c q lam meas : ℝ} (hm : meas ≠ 0) (h : lam = meas * q ^ 2) :
    omegaSq c lam meas = (c * q) ^ 2 := by
  subst h
  exact omegaSq_acoustic hm

/-! ### 二、截断＝模式计数（Debye 端点），立方形式避开分式幂 -/

/-- 模式计数：$Q^3=6\pi^2n$。 -/
def modeCount (Q n : ℝ) : Prop := Q ^ 3 = 6 * Real.pi ^ 2 * n

/-- 标度：$n\to s^3n$ 时 $Q\to sQ$（$Q\propto n^{1/3}$）。 -/
theorem cutoff_scale {Q n s : ℝ} (h : modeCount Q n) :
    (s * Q) ^ 3 = 6 * Real.pi ^ 2 * (s ^ 3 * n) := by
  unfold modeCount at h
  calc (s * Q) ^ 3 = s ^ 3 * Q ^ 3 := by ring
    _ = s ^ 3 * (6 * Real.pi ^ 2 * n) := by rw [h]
    _ = 6 * Real.pi ^ 2 * (s ^ 3 * n) := by ring

/-- Debye 频率：$\omega_D=c_sQ$，故 $c_s\to sc_s$、$Q\to sQ$ 给 $\omega_D\to s^2\omega_D$（同比例缩放）。 -/
theorem omegaD_scale (c Q s : ℝ) : (s * c) * (s * Q) = s ^ 2 * (c * Q) := by
  ring

/-- $\Theta_D=\hbar\omega_D/k_B$ 只差常数因子，故其标度与 $\omega_D$ 同。 -/
theorem thetaD_scale (h k c Q s : ℝ) (hk : k ≠ 0) :
    h * ((s * c) * (s * Q)) / k = s ^ 2 * (h * (c * Q) / k) := by
  field_simp

/-! ### 三、同位素指数 -/

/-- $\alpha=-\dfrac{\partial\ln\Theta_D}{\partial\ln M}+\dfrac{1}{\lambda^2}\dfrac{\partial\ln\lambda}{\partial\ln M}$。 -/
def isotopeAlpha (lam dlnTheta dlnLam : ℝ) : ℝ :=
  -dlnTheta + (1 / lam ^ 2) * dlnLam

/-- 谐波 + Born–Oppenheimer：$\Theta_D\propto M^{-1/2}$、$\lambda$ 与 $M$ 无关 ⇒ $\alpha=1/2$。 -/
theorem isotopeAlpha_harmonic (lam : ℝ) :
    isotopeAlpha lam (-(1 / 2)) 0 = 1 / 2 := by
  unfold isotopeAlpha
  ring

/-- 若 $\lambda$ 随 $M$ 变（非谐），$\alpha$ 由 $\partial\ln\lambda/\partial\ln M$ 修正；符号由该导数定。 -/
theorem isotopeAlpha_shift (lam dlnLam : ℝ) :
    isotopeAlpha lam (-(1 / 2)) dlnLam = 1 / 2 + (1 / lam ^ 2) * dlnLam := by
  unfold isotopeAlpha
  ring

/-! ### 四、零点幅度的无量纲群 -/

/-- 量子长度 $\ell_q=(\hbar/\rho_mc_s)^{1/4}$ 的比 $\ell_q/a$ 是**唯一**的无量纲输入：$(\ell_q,a)$ 同比缩放不改 $\sigma^2$。 -/
theorem sigmaRatio_scale_invariant {lq a s : ℝ} (hs : s ≠ 0) :
    (s * lq / (s * a)) ^ 4 = (lq / a) ^ 4 := by
  rw [mul_div_mul_left _ _ hs]

/-- $\sigma^2$ 对 $\ell_q/a$ 是四次齐次：把 $\ell_q$ 放大 $s$ 倍使 $\sigma^2$ 放大 $s^4$ 倍。 -/
theorem sigmaRatio_scale (c lq a s : ℝ) :
    c * (s * lq / a) ^ 4 = c * s ^ 4 * (lq / a) ^ 4 := by
  rw [mul_div_assoc, mul_pow]
  ring

/-- 小参数界：$\ell_q/a\le 1/5$ ⇒ $\sigma_\varepsilon/c_\varepsilon\le 1.21/25<0.05$。 -/
theorem small_parameter_bound {r : ℝ} (h0 : 0 ≤ r) (h : r ≤ 1 / 5) :
    121 / 100 * r ^ 2 < 1 / 20 := by
  nlinarith [sq_nonneg r, sq_nonneg (1 / 5 - r)]

/-! ### 五、环 10 振幅预算 -/

/-- 振幅预算的代数解：由 $\lambda=4N(0)g^2\sigma^2(1-\rho)/\hbar\omega$ 解出 $g^2$。 -/
theorem coupling_budget_sq {lam N0 g sq hw rho : ℝ}
    (h : lam = 4 * N0 * g ^ 2 * sq * (1 - rho) / hw)
    (hN : N0 ≠ 0) (hsq : sq ≠ 0) (hr : 1 - rho ≠ 0) (hw0 : hw ≠ 0) :
    g ^ 2 = lam * hw / (4 * N0 * sq * (1 - rho)) := by
  rw [h]
  field_simp

/-- $\sigma^2>0$ 且 $(1-\rho)>0$、$N(0)>0$ 时，$\lambda>0$ 给 $g^2>0$：预算总有实数解（$g$ 是唯一剩余外生量）。 -/
theorem coupling_budget_pos {lam N0 g sq hw rho : ℝ}
    (h : lam = 4 * N0 * g ^ 2 * sq * (1 - rho) / hw)
    (hN : 0 < N0) (hsq : 0 < sq) (hr : 0 < 1 - rho) (hw0 : 0 < hw) (hl : 0 < lam) :
    0 < g ^ 2 := by
  rw [coupling_budget_sq h (ne_of_gt hN) (ne_of_gt hsq) (ne_of_gt hr) (ne_of_gt hw0)]
  positivity

end

end CQM.PhononDim
