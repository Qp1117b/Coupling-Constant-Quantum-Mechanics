/-
  第93轮补（成果登记 R-102）：临-25 扩大项符号的热扫描判定
  ================================================================
  承接第87/88轮（曲率模方差 c^0[1+2n_B]、Debye 模计数 g∝ω²、热截断
  ω_T=k_B T/ħ）。本文件纯代数承载：

    * M_t∝ω_T³ ∝ T³、dot M_t/M_t = 3 dot T/T；
    * D(T)=3ħ²/(k_B T) ∝ 1/T（对 T 单减）；
    * D_new=ħ²/(k_B T)=D/3 ⇒ D_new-D = -(2/3)D < 0；
    * 扩大项 = -2 ħ² dot T/(k_B T²)，符号 = -sgn(dot T)：
      加热为负（平均化），冷却为正（差异化）；
    * 饱和区 ω_T 封顶于 ω_D（边界）。

  边界：这是准静态温度扫描关系，不是时间依赖动理学；临-25 仍不闭合。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

open scoped BigOperators

namespace CQM.ThreeTermSign

noncomputable section

/-- 热截断 $\omega_T=k_B T/\hbar$（$T\ll\Theta_D$ 时有效）。 -/
def omegaT (kB hbar T : ℝ) : ℝ := kB * T / hbar

/-- 活跃模数 $M_t=(C/3)\omega_T^3$（Debye 模计数）。 -/
def modesCount (C kB hbar T : ℝ) : ℝ := C / 3 * (omegaT kB hbar T) ^ 3

/-- $M_t\propto T^3$：比值 $M_t(T_2)/M_t(T_1)=(T_2/T_1)^3$。 -/
lemma modes_scaling (C kB hbar T1 T2 : ℝ)
    (hC : C ≠ 0) (hkB : kB ≠ 0) (hh : hbar ≠ 0) (hT1 : T1 ≠ 0) :
    modesCount C kB hbar T2 / modesCount C kB hbar T1 = (T2 / T1) ^ 3 := by
  unfold modesCount omegaT
  field_simp [hC, hkB, hh, hT1]

/-- 平均分化度 $\mathcal D(T)=3\hbar^2/(k_B T)\propto1/T$。 -/
def avgD (kB hbar T : ℝ) : ℝ := 3 * hbar ^ 2 / (kB * T)

/-- 新增分化度 $\mathcal D_{new}=\hbar^2/(k_B T)$。 -/
def newD (kB hbar T : ℝ) : ℝ := hbar ^ 2 / (kB * T)

/-- $\mathcal D_{new}/\mathcal D=1/3$（新模方差是平均的 1/3）。 -/
lemma newD_over_avgD (kB hbar T : ℝ) (hkB : kB ≠ 0) (hT : T ≠ 0) (hh : hbar ≠ 0) :
    newD kB hbar T / avgD kB hbar T = (1 / 3 : ℝ) := by
  unfold newD avgD
  field_simp [hkB, hT, hh]

/-- $\mathcal D_{new}-\mathcal D=-\frac23\mathcal D<0$（与扫描方向无关）。 -/
lemma newD_lt_avgD (kB hbar T : ℝ) (hkB : 0 < kB) (hh : 0 < hbar) (hT : 0 < T) :
    newD kB hbar T - avgD kB hbar T < 0 := by
  unfold newD avgD
  field_simp [ne_of_gt hkB, ne_of_gt hT]
  nlinarith [sq_pos_of_pos hh]

/-- $\mathcal D$ 对 $T$ 单减（升温平均化）。 -/
lemma avgD_antitone (kB hbar T1 T2 : ℝ) (hkB : 0 < kB) (hh : 0 < hbar)
    (h1 : 0 < T1) (h12 : T1 ≤ T2) : avgD kB hbar T2 ≤ avgD kB hbar T1 := by
  unfold avgD
  have hT2 : 0 < T2 := lt_of_lt_of_le h1 h12
  apply div_le_div_of_nonneg_left
  · positivity
  · exact mul_pos hkB h1
  · exact mul_le_mul_of_nonneg_left h12 hkB.le

/-- 扩大项 $=-2\hbar^2\dot T/(k_B T^2)$（由 $\dot M_t/M_t=3\dot T/T$ 与 $\mathcal D_{new}-\mathcal D=-\frac23\mathcal D$ 合成）。 -/
def expansionTerm (kB hbar T dT : ℝ) : ℝ := -2 * hbar ^ 2 * dT / (kB * T ^ 2)

/-- 加热（$\dot T>0$）扩大项为负：平均化。 -/
lemma expansion_heating_neg (kB hbar T dT : ℝ) (hkB : 0 < kB) (hh : 0 < hbar)
    (hT : 0 < T) (hdT : 0 < dT) : expansionTerm kB hbar T dT < 0 := by
  unfold expansionTerm
  have hnum : -2 * hbar ^ 2 * dT < 0 := by nlinarith [sq_pos_of_pos hh]
  exact div_neg_of_neg_of_pos hnum (mul_pos hkB (sq_pos_of_pos hT))

/-- 冷却（$\dot T<0$）扩大项为正：差异化。 -/
lemma expansion_cooling_pos (kB hbar T dT : ℝ) (hkB : 0 < kB) (hh : 0 < hbar)
    (hT : 0 < T) (hdT : dT < 0) : 0 < expansionTerm kB hbar T dT := by
  unfold expansionTerm
  have hnum : 0 < -2 * hbar ^ 2 * dT := by nlinarith [sq_pos_of_pos hh]
  exact div_pos hnum (mul_pos hkB (sq_pos_of_pos hT))

/-- 饱和边界：$\omega_T=\min(k_BT/\hbar,\omega_D)$，高温封顶。 -/
lemma cutoff_cap (kB hbar T wD : ℝ) (h : kB * T / hbar ≥ wD) :
    min (omegaT kB hbar T) wD = wD := by
  unfold omegaT
  exact min_eq_right h

end
end CQM.ThreeTermSign
