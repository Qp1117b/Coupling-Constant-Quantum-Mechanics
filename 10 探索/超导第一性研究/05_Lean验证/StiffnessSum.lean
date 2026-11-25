/-
  第98轮补（成果登记 R-107）：临-20 刚度求和显式与 Uemura 常数族
  =================================================================
  承接 M6 键局域 J/J0=(1-rho)cos(s*ell)、Uemura Tc=(pi/2kB)Upsilon_bare Q。
  本文件纯代数承载：

    * Upsilon0 = 2 J0 (1-rho_nn)（方格子几何因子 2）；
    * 单调：Upsilon0 对 rho 单减、干净极限 rho=0 给 2J0、强关联 rho=1 给 0；
    * Uemura 上界 Tc <= (pi/kB) J0 (1-rho)；
    * FE10 eta ~ (1-rho) 与 Upsilon ~ (1-rho) 的竞争（同向系数、不同扇区）。

  外部依据（只作工具）：PRB99 104509 干净 XY rho_s^0=J；Benfatto 讲义；Uemura PRL62 2317。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

namespace CQM.StiffnessSum

noncomputable section

/-- 裸刚度 $\Upsilon_0=2J_0(1-\rho)$（方格子）。 -/
def upsilon0 (J0 rho : ℝ) : ℝ := 2 * J0 * (1 - rho)

/-- 干净极限 $\rho=0$ 给 $2J_0$。 -/
lemma clean_limit (J0 : ℝ) : upsilon0 J0 0 = 2 * J0 := by
  unfold upsilon0
  ring

/-- 强关联 $\rho=1$ 给刚度消失。 -/
lemma strong_corr_zero (J0 : ℝ) : upsilon0 J0 1 = 0 := by
  unfold upsilon0
  ring

/-- 单调：$J_0>0$ 时 $\Upsilon_0$ 对 $\rho$ 单减。 -/
lemma upsilon_antitone (J0 : ℝ) (hJ : 0 < J0) {r1 r2 : ℝ} (h12 : r1 ≤ r2) :
    upsilon0 J0 r2 ≤ upsilon0 J0 r1 := by
  unfold upsilon0
  nlinarith

/-- 正性：$0\le\rho<1$ 给 $\Upsilon_0>0$。 -/
lemma upsilon_pos (J0 rho : ℝ) (hJ : 0 < J0) (hr1 : rho < 1) :
    0 < upsilon0 J0 rho := by
  unfold upsilon0
  nlinarith

/-- Uemura 上界 $T_c\le(\pi/k_B)\Upsilon_0/2=(\pi/k_B)J_0(1-\rho)$。 -/
def uemuraBound (kB J0 rho : ℝ) : ℝ := Real.pi / kB * J0 * (1 - rho)

lemma uemura_bound_relation (kB J0 rho : ℝ) (hkB : kB ≠ 0) :
    uemuraBound kB J0 rho = Real.pi / (2 * kB) * upsilon0 J0 rho := by
  unfold uemuraBound upsilon0
  field_simp [hkB]

/-- 竞争判据：FE10 $\eta\propto(1-\rho)$ 与刚度 $\Upsilon\propto(1-\rho)$ 同向系数、
    但分属配对（振幅）与相位扇区——这里只承载"同向"的代数骨架。 -/
lemma eta_stiffness_same_sign (rho J0 cEta : ℝ) (hJ : 0 < J0) (hc : 0 < cEta)
    (hr : rho < 1) :
    0 < cEta * (1 - rho) ∧ 0 < upsilon0 J0 rho := by
  constructor
  · nlinarith
  · exact upsilon_pos J0 rho hJ hr

end
end CQM.StiffnessSum
