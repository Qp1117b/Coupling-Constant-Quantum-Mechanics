import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-!
# 环 19：$w(T)$ 与实验刚度对应域的代数骨架（第 151 轮）

本文件只承载解析式中的纯代数部分，不引入新的物理假设：
1. `pearl_identity`：Pearl 长度 $\Lambda=2\lambda^2/d$ 与 $d/\lambda^2=2/\Lambda$ 等价；
2. `bkt_floor_ratio`：$K_R\ge2/\pi$ 给出归一化刚度的普适下界 $T/T_c$；
3. `ceiling_le`：$\Phi\le1$ 给出 $w\Phi\le w$；
4. `linear_quadratic_window`：线性耗竭与二次下限的比较窗口 $T^*=3c\omega_D^2/\pi^2$；
5. `band_of_concavity`：$w$ 的凹性使容许带非空；
6. `bktRelevance_le_one`：$\mathcal B=T_c\Lambda(0)/C\le1$。
-/

namespace CQM.StiffnessReadout

noncomputable section

/-- **Pearl 恒等式**。$\Lambda=2\lambda^{2}/d$ 时 $d/\lambda^{2}=2/\Lambda$。

即 (19W.1) 的两种写法 $\Upsilon=\dfrac{\hbar^{2}}{4\mu_{0}e^{2}}d\lambda^{-2}
=\dfrac{\hbar^{2}}{2\mu_{0}e^{2}}\Lambda^{-1}$ 等价。 -/
theorem pearl_identity {d lam Lam : ℝ} (hd : d ≠ 0) (hlam : lam ≠ 0)
    (hLam : Lam = 2 * lam ^ 2 / d) : d / lam ^ 2 = 2 / Lam := by
  subst hLam
  field_simp

/-- **BKT 普适下界**。若 $\Upsilon_R(T)\ge\frac{2}{\pi}k_BT$ 且
$\Upsilon_R(T_c)=\frac{2}{\pi}k_BT_c$，则 $\dfrac{T}{T_c}\le\dfrac{\Upsilon_R(T)}{\Upsilon_R(T_c)}$。

这里把 $k_B$ 吸收进 $\Upsilon$ 的单位，只保留 $\frac{2}{\pi}$ 因子。 -/
theorem bkt_floor_ratio {U Uc T Tc : ℝ} (hTc : 0 < Tc)
    (hUc : Uc = (2 / Real.pi) * Tc) (hU : (2 / Real.pi) * T ≤ U) :
    T / Tc ≤ U / Uc := by
  rw [hUc]
  have hden : (0 : ℝ) < (2 / Real.pi) * Tc := by positivity
  rw [le_div_iff₀ hden]
  have hEq : T / Tc * ((2 / Real.pi) * Tc) = (2 / Real.pi) * T := by
    field_simp
  rw [hEq]
  exact hU

/-- **上界收缩**。$0\le w$、$\Phi\le1$ ⇒ $w\Phi\le w$（再乘 $0\le\Upsilon_0$）。 -/
theorem ceiling_le {U0 w Φ : ℝ} (hU0 : 0 ≤ U0) (hw : 0 ≤ w) (hΦ : Φ ≤ 1) :
    U0 * (w * Φ) ≤ U0 * w := by
  have h : w * Φ ≤ w * 1 := mul_le_mul_of_nonneg_left hΦ hw
  simpa using mul_le_mul_of_nonneg_left h hU0

/-- **线性—二次窗口**。$3c\omega^{2}\le\pi^{2}T$ ⇔ $\omega^{2}\le\pi^{2}T/(3c)$。

配合 $1-w=\frac{\pi^{2}}{3}(T/\omega_D)^{2}$，把"线性耗竭不低于二次下限"
化成 $T\le T^{*}=3c\omega_D^{2}/\pi^{2}$。 -/
theorem linear_quadratic_window {c T w2 : ℝ} (hc : 0 < c) :
    (3 * c * w2 ≤ Real.pi ^ 2 * T) ↔ (w2 ≤ Real.pi ^ 2 * T / (3 * c)) := by
  rw [le_div_iff₀ (by positivity)]
  constructor <;> intro h <;> nlinarith [h]

/-- **容许带非空**。若 $w$ 在 $[0,T_c]$ 上位于弦上方
$w\ge1-\frac{T}{T_c}(1-w_c)$（凹性推论），则 $w\ge\frac{T}{T_c}w_c$。

即 (19W.5) 的上界在 $T\le T_c$ 时不弱于下界。 -/
theorem band_of_concavity {w wc T Tc : ℝ} (hTc : 0 < Tc)
    (hT : T ≤ Tc) (hconc : w ≥ 1 - (T / Tc) * (1 - wc)) :
    w ≥ (T / Tc) * wc := by
  have h1 : T / Tc ≤ 1 := by
    rw [div_le_one hTc]
    exact hT
  nlinarith [hconc, h1]

/-- **BKT 相关度不超过 1**。若 $T_c\Lambda(0)\le C$
（$C=\pi\hbar^{2}/(4\mu_{0}e^{2}k_B)$，BKT 下限），则 $\mathcal B=T_c\Lambda(0)/C\le1$。 -/
theorem bktRelevance_le_one {Tc Lam C : ℝ} (hC : 0 < C) (hLam : Tc * Lam ≤ C) :
    Tc * Lam / C ≤ 1 := by
  exact (div_le_one hC).mpr hLam

end

end CQM.StiffnessReadout
