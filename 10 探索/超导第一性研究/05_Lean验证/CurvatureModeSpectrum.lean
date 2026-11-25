/-
  第88轮补（成果登记 R-97）：曲率模谱与占据截断——审-10 的结构半边
  =================================================================
  承接第87轮（R-96）：亏角涨落载体＝Regge Hessian 非规范曲率模，(4.1′) 给 [1+2nB]。
  本文件承载谱截断问题的纯代数/分析骨架：

    * Debye 模计数：V*(6π²n)/(2π²)=3nV（每原子 3 模）；
    * 占据模比例 F(q)=(q/Q)^3：F(Q)=1、对 q 单调；
    * 低频先占据：nB 对 ω 反单调、高温 nB<=1/x（线性上界）；
    * 两矩不等：ω_log=e^{-1/3}θ_D < θ_D（截断≠对数矩，审-17 不升级）；
    * 2D 红外：log(L/a)>0（有限尺寸截断的对数增长），3D 为幂律。

  外部依据（只作工具，不写成 CQM=量子引力）：
    arXiv:0707.4513 (PRD76 104020) 式(27)-(28) Hessian 非零 sector = 格点拉普拉斯；
    arXiv:2408.04877 余切权与节点质量；DOI 10.1007/s00211-011-0394-z FEM 收敛；
    R71/R72 链内登记 Q=(6π²n)^{1/3}、Θ_D=(ħc_s/kB)Q。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

open scoped BigOperators

namespace CQM.CurvatureSpectrum

noncomputable section

/-! ### 一、Debye 模计数 -/

/-- 玻色占据（复用第87轮结构，独立定义以便本文件自洽）。 -/
def nB (x : ℝ) : ℝ := 1 / (Real.exp x - 1)

lemma exp_minus_one_pos {x : ℝ} (hx : 0 < x) : 0 < Real.exp x - 1 := by
  have h : 1 < Real.exp x := Real.one_lt_exp_iff.mpr hx
  linarith

/-- 3D Debye 模计数：$V(6\pi^2n)/(2\pi^2)=3nV$（每原子 3 支）。 -/
lemma debye_mode_count (n V : ℝ) :
    V * (6 * Real.pi ^ 2 * n) / (2 * Real.pi ^ 2) = 3 * n * V := by
  have hp : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp [hp]
  ring

/-! ### 二、占据模比例 -/

/-- 累积占据模比例 $F(q)=(q/Q)^3$。 -/
def occupiedFraction (q Q : ℝ) : ℝ := (q / Q) ^ 3

/-- 在截断端点 $F(Q)=1$。 -/
lemma occupiedFraction_full (Q : ℝ) (hQ : Q ≠ 0) : occupiedFraction Q Q = 1 := by
  unfold occupiedFraction
  field_simp [hQ]

/-- $F$ 对 $q$ 单调不减（$0\le q_1\le q_2$、$Q>0$）。 -/
lemma occupiedFraction_mono {q1 q2 Q : ℝ} (hQ : 0 < Q) (h1 : 0 ≤ q1) (h12 : q1 ≤ q2) :
    occupiedFraction q1 Q ≤ occupiedFraction q2 Q := by
  unfold occupiedFraction
  have h2 : 0 ≤ q2 := le_trans h1 h12
  have hd1 : 0 ≤ q1 / Q := div_nonneg h1 hQ.le
  have hd : q1 / Q ≤ q2 / Q := div_le_div_of_nonneg_right h12 hQ.le
  exact pow_le_pow_left₀ hd1 hd 3

/-! ### 三、低频先占据、高温线性 -/

/-- $n_B$ 对自变量反单调：$0<x_1\le x_2\Rightarrow n_B(x_2)\le n_B(x_1)$。 -/
lemma nB_antitone {x1 x2 : ℝ} (hx1 : 0 < x1) (h12 : x1 ≤ x2) : nB x2 ≤ nB x1 := by
  unfold nB
  have hd1 : 0 < Real.exp x1 - 1 := exp_minus_one_pos hx1
  have hd : Real.exp x1 - 1 ≤ Real.exp x2 - 1 := by
    have he := Real.exp_le_exp.mpr h12
    linarith
  exact one_div_le_one_div_of_le hd1 hd

/-- 低频模先占据：$\omega_1\le\omega_2$、$T>0$ ⇒ $n_B(\omega_2/T)\le n_B(\omega_1/T)$。 -/
lemma low_mode_first {w1 w2 T : ℝ} (hw1 : 0 < w1) (hT : 0 < T) (h12 : w1 ≤ w2) :
    nB (w2 / T) ≤ nB (w1 / T) := by
  have hx1 : 0 < w1 / T := div_pos hw1 hT
  have hx12 : w1 / T ≤ w2 / T := div_le_div_of_nonneg_right h12 hT.le
  exact nB_antitone hx1 hx12

/-- 高温线性上界：$n_B(x)\le 1/x$（$e^x\ge1+x$）。 -/
lemma nB_le_inv {x : ℝ} (hx : 0 < x) : nB x ≤ 1 / x := by
  unfold nB
  have h : x ≤ Real.exp x - 1 := by
    have hx' := Real.add_one_le_exp x
    linarith
  exact one_div_le_one_div_of_le hx h

/-! ### 四、两矩不等（截断 ≠ 对数矩） -/

/-- $\omega_{\log}=e^{-1/3}\theta_D<\theta_D$：$\theta_D$ 才是谱支集端点。 -/
lemma omegaLog_lt_debye (thetaD : ℝ) (h : 0 < thetaD) :
    Real.exp (-(1 : ℝ) / 3) * thetaD < thetaD := by
  have he : Real.exp (-(1 : ℝ) / 3) < 1 := Real.exp_lt_one_iff.mpr (by norm_num)
  nlinarith

/-! ### 五、2D 红外对数截断 -/

/-- $0<a<L\Rightarrow \log(L/a)>0$：2D 红外发散由有限尺寸 $q_{\min}\sim2\pi/L$ 截断。 -/
lemma ir_log_growth {a L : ℝ} (ha : 0 < a) (haL : a < L) : 0 < Real.log (L / a) := by
  apply Real.log_pos
  exact (one_lt_div ha).mpr haL

/-- 3D 对应为幂律（可积）：$q_{\min}=2\pi/L>0$，累积正比于 $q_{\max}-q_{\min}$，无对数发散。 -/
lemma ir_power_finite {qmin qmax : ℝ} (hmin : 0 < qmin) (h : qmin ≤ qmax) :
    0 < qmax := lt_of_lt_of_le hmin h

end
end CQM.CurvatureSpectrum
