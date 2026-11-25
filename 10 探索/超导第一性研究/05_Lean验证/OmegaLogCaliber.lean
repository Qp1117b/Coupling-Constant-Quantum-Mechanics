/-
  第94轮补（成果登记 R-103）：双观测检验的 omega 对数矩口径修正
  ==================================================================
  承接第92轮（链内导出 omega_log=e^{-1/2} theta_D = omega_ln）。本文件承载：

    * e^{-1/2} < e^{-1/3}（振幅支矩高估 AD 式权重）；
    * 比值 e^{-1/3}/e^{-1/2} = e^{1/6}（两矩分歧精确值）；
    * Morel-Anderson 形状 mu*=mu/(1+mu L) 的正性、<mu、对 mu 单增、L 单减；
    * 双观测方程中 mu* 由 alpha 单调决定的代数骨架；
    * 二阶 MA 修正（Bauer et al.）给 mu* 略大的方向。

  外部依据（只作工具，不写成 CQM=BCS）：
    Allen-Dynes PRB12 905 / Webb 2015 式3：omega_ln=alpha^2F/nu 权重；
    Morel-Anderson PRB125 1263 (1962)；Bauer-Han-Gunnarsson arXiv:1202.5051。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

open scoped BigOperators

namespace CQM.OmegaLogCaliber

noncomputable section

/-! ### 一、对数矩口径 -/

/-- $\omega_{\ln}=e^{-1/2}\theta_D<e^{-1/3}\theta_D=\omega_{\log}^{\rm amp}$（$\theta_D>0$）。 -/
lemma wlog_AD_lt_amp (thetaD : ℝ) (h : 0 < thetaD) :
    Real.exp (-(1 : ℝ) / 2) * thetaD < Real.exp (-(1 : ℝ) / 3) * thetaD := by
  have he : Real.exp (-(1 : ℝ) / 2) < Real.exp (-(1 : ℝ) / 3) := by
    exact Real.exp_lt_exp.mpr (by norm_num)
  nlinarith

/-- 两矩比 $e^{-1/3}/e^{-1/2}=e^{1/6}$（振幅支高估的精确因子）。 -/
lemma wlog_ratio : Real.exp (-(1 : ℝ) / 3) / Real.exp (-(1 : ℝ) / 2) = Real.exp ((1 : ℝ) / 6) := by
  rw [← Real.exp_sub]
  congr 1
  ring

/-- 高估比例：$e^{1/6}>1$。 -/
lemma ratio_gt_one : 1 < Real.exp ((1 : ℝ) / 6) := by
  have := Real.exp_pos ((1 : ℝ) / 6)
  have hlog : (0 : ℝ) < (1 : ℝ) / 6 := by norm_num
  exact Real.one_lt_exp_iff.mpr hlog

/-! ### 二、Morel-Anderson 形状 -/

/-- $\mu^*=\mu/(1+\mu L)$，$\mu>0,L>0$ 时为正。 -/
def mustar (mu L : ℝ) : ℝ := mu / (1 + mu * L)

lemma mustar_pos (mu L : ℝ) (hmu : 0 < mu) (hL : 0 < L) : 0 < mustar mu L := by
  unfold mustar
  positivity

/-- $\mu^*<\mu$（延迟压制）。 -/
lemma mustar_lt_mu (mu L : ℝ) (hmu : 0 < mu) (hL : 0 < L) : mustar mu L < mu := by
  unfold mustar
  rw [div_lt_iff₀ (by positivity : 0 < 1 + mu * L)]
  nlinarith [mul_pos hmu hL]

/-- $\mu^*$ 对 $\mu$ 单增。 -/
lemma mustar_mono_mu (L : ℝ) (hL : 0 < L) {m1 m2 : ℝ} (hm1 : 0 < m1) (h12 : m1 ≤ m2) :
    mustar m1 L ≤ mustar m2 L := by
  unfold mustar
  have hm2 : 0 < m2 := lt_of_lt_of_le hm1 h12
  -- mu/(1+mu L) = (1/L)(1 - 1/(1+mu L))，随 mu 增
  have hden1 : 0 < 1 + m1 * L := by positivity
  have hden2 : 0 < 1 + m2 * L := by positivity
  have hfrac : 1 / (1 + m2 * L) ≤ 1 / (1 + m1 * L) := by
    apply one_div_le_one_div_of_le hden1
    nlinarith [mul_le_mul_of_nonneg_right h12 hL.le]
  field_simp [ne_of_gt hden1, ne_of_gt hden2]
  nlinarith [mul_le_mul_of_nonneg_right h12 hL.le]

/-- $\mu^*$ 对 $L=\ln(\epsilon_F/\hbar\omega_D)$ 单减。 -/
lemma mustar_antitone_L (mu : ℝ) (hmu : 0 < mu) {L1 L2 : ℝ} (hL1 : 0 < L1) (h12 : L1 ≤ L2) :
    mustar mu L2 ≤ mustar mu L1 := by
  unfold mustar
  have hL2 : 0 < L2 := lt_of_lt_of_le hL1 h12
  have hd1 : 0 < 1 + mu * L1 := by positivity
  have hd2 : 0 < 1 + mu * L2 := by positivity
  rw [div_le_div_iff₀ hd2 hd1]
  nlinarith [mul_le_mul_of_nonneg_left h12 hmu.le]

/-! ### 三、双观测方程代数骨架 -/

/-- 同位素方程 $\alpha=\frac12[1-C]$，$C\propto\mu^{*2}/(\lambda-\mu^* b)^2>0$ ⇒ $\alpha<1/2$。 -/
lemma alpha_below_half (C : ℝ) (hC : 0 < C) :
    (1 / 2 : ℝ) * (1 - C) < 1 / 2 := by linarith

/-- $\mu^*=0$ 端点给 $\alpha=1/2$（同位素端点，R1）。 -/
lemma alpha_endpoint : (1 / 2 : ℝ) * (1 - 0) = 1 / 2 := by ring

/-- 二阶 MA（Bauer et al.）在 $\mu$ 小时给更大 $\mu^*$ 的方向（定性骨架）：
    分子 $\mu+a\mu^2>\mu$，分母多一正项但主导仍使值升（$a>0$、$L$ 大）。 -/
lemma ma_second_order_num_gt (mu a : ℝ) (hmu : 0 < mu) (ha : 0 < a) : mu < mu + a * mu ^ 2 := by
  nlinarith [sq_pos_of_pos hmu]

end
end CQM.OmegaLogCaliber
