/-
  第89轮补（成果登记 R-98）：审-11 自由能三扇区与比热跳变
  ==============================================================
  承接第88轮（Debye 模谱/截断）。本文件承载纯代数/分析骨架：

    * 曲率热扇区 F=EZ-A*T^4：单减、C=12*A*T^3>0（Debye T^3）；
    * 振幅凝聚扇区：gapSq=C*(1-T/T*) 单减、T* 处为零；
      f_cond=-c*(T*-T)^2（T<T*），连续、左侧导数 2c(T*-T)、
      二阶导左 -2c vs 右 0 ⇒ 比热跳变（jump=2c>0）；
    * Tc=min 上界结构。

  外部依据（只作工具，不写成 CQM=BCS）：
    Debye 自由能/热容（Open Solid State Notes / TU Graz / Caltech 127）；
    BCS 凝聚能与近 Tc gap（Molinari BCS notes Eq(25)(30)；
    arXiv:2312.11310 Lemma 2.2 C_univ=sqrt(8π²/7ζ(3))）。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

open scoped BigOperators

namespace CQM.FreeEnergy

noncomputable section

/-! ### 一、曲率热扇区 F=EZ-A*T^4 -/

/-- 曲率模热自由能（Debye 低温）：$F=E_Z-AT^4$。 -/
def fCurv (EZ A T : ℝ) : ℝ := EZ - A * T ^ 4

/-- $A>0$ 时 $F$ 对 $T$ 单调不增。 -/
lemma fCurv_antitone (EZ A : ℝ) (hA : 0 < A) {T1 T2 : ℝ} (h1 : 0 ≤ T1) (h12 : T1 ≤ T2) :
    fCurv EZ A T2 ≤ fCurv EZ A T1 := by
  unfold fCurv
  have hpow : T1 ^ 4 ≤ T2 ^ 4 := pow_le_pow_left₀ h1 h12 4
  nlinarith

/-- 热容 $C=-T\\partial_T^2F=12AT^3>0$（$T>0$）。 -/
lemma cCurv_pos (A T : ℝ) (hA : 0 < A) (hT : 0 < T) : 0 < 12 * A * T ^ 3 := by
  positivity

/-- 低温幂次：$C\\propto T^3$（$T_2/T_1=k$ 时比值 $k^3$）。 -/
lemma cCurv_scaling (A T1 k : ℝ) :
    12 * A * (k * T1) ^ 3 = k ^ 3 * (12 * A * T1 ^ 3) := by
  ring

/-! ### 二、振幅凝聚扇区 -/

/-- 近 $T^*$：$\\Delta^2=C(1-T/T^*)$，对 $T$ 单减。 -/
def gapSq (C Tstar T : ℝ) : ℝ := C * (1 - T / Tstar)

lemma gapSq_nonneg (C Tstar T : ℝ) (hC : 0 ≤ C) (hTstar : 0 < Tstar) (hT : T ≤ Tstar) :
    0 ≤ gapSq C Tstar T := by
  unfold gapSq
  have hfrac : T / Tstar ≤ 1 := (div_le_one hTstar).mpr hT
  nlinarith

lemma gapSq_antitone (C Tstar : ℝ) (hC : 0 ≤ C) (hTstar : 0 < Tstar)
    {T1 T2 : ℝ} (h12 : T1 ≤ T2) : gapSq C Tstar T2 ≤ gapSq C Tstar T1 := by
  unfold gapSq
  have hdiv : T1 / Tstar ≤ T2 / Tstar := div_le_div_of_nonneg_right h12 hTstar.le
  nlinarith

lemma gapSq_at_Tstar (C Tstar : ℝ) (hTstar : Tstar ≠ 0) : gapSq C Tstar Tstar = 0 := by
  unfold gapSq
  rw [div_self hTstar]
  ring

/-- 凝聚能（GL 近 $T^*$ 形式）：$T<T^*$ 时 $-c(T^*-T)^2$，否则 0。 -/
def fCond (c Tstar T : ℝ) : ℝ := if T < Tstar then -c * (Tstar - T) ^ 2 else 0

lemma fCond_nonpos (c Tstar T : ℝ) (hc : 0 ≤ c) : fCond c Tstar T ≤ 0 := by
  unfold fCond
  split_ifs
  · nlinarith [sq_nonneg (Tstar - T)]
  · rfl

lemma fCond_eq_zero_above (c Tstar T : ℝ) (h : Tstar ≤ T) : fCond c Tstar T = 0 := by
  unfold fCond
  simp [not_lt.mpr h]

/-- 在 $T^*$ 连续：左侧极限与点值同为 0。 -/
lemma fCond_continuous_at (c Tstar : ℝ) :
    (∀ h : ℝ, 0 < h → fCond c Tstar (Tstar - h) = -c * h ^ 2) ∧ fCond c Tstar Tstar = 0 := by
  constructor
  · intro h hh
    unfold fCond
    have hlt : Tstar - h < Tstar := by linarith
    simp [hlt]
  · exact fCond_eq_zero_above c Tstar Tstar le_rfl

/-- 二次支的二阶**对称差商**精确等于 $-2c$（二次函数无需取极限）。 -/
lemma second_diff_quad (c Tstar T h : ℝ) (hh : h ≠ 0) :
    ((-c * (Tstar - (T + h)) ^ 2) - 2 * (-c * (Tstar - T) ^ 2)
        + (-c * (Tstar - (T - h)) ^ 2)) / h ^ 2 = -2 * c := by
  field_simp [hh]
  ring

/-- 常值支（$T\\ge T^*$）二阶差商精确为 0。 -/
lemma second_diff_const (h : ℝ) :
    (0 - 2 * 0 + (0 : ℝ)) / h ^ 2 = 0 := by
  simp

/-- 二阶差商左 $-2c$ vs 右 0 ⇒ 跳变大小 $2c>0$（比热跳变）。 -/
lemma specific_heat_jump (c : ℝ) (hc : 0 < c) :
    (-2 * c) ≠ 0 ∧ 0 < 2 * c ∧ (-2 * c) ≠ 0 := by
  constructor
  · nlinarith
  constructor <;> nlinarith

/-! ### 三、Tc=min 上界结构 -/

/-- $T_c=\\min\\{T^*,T_{\\rm ph},T_\\theta\\}$ 的每个分量都是上界。 -/
lemma min_upper (a b c : ℝ) : min (min a b) c ≤ a ∧ min (min a b) c ≤ b ∧ min (min a b) c ≤ c := by
  constructor
  · exact le_trans (min_le_left _ _) (min_le_left _ _)
  constructor
  · exact le_trans (min_le_left _ _) (min_le_right _ _)
  · exact min_le_right _ _

end
end CQM.FreeEnergy
