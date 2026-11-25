/-
  第97轮补（成果登记 R-106）：凝聚能普适比 Econd/(gamma Tc^2)=3/(4 e^{2 gamma_E})
  ================================================================================
  承接第89轮凝聚能 Econd=1/2 N(0) Delta_0^2=Bc^2/(2 mu0)、C5 Delta_0=pi/e^gamma kB Tc、
  Sommerfeld gamma=2pi^2/3 kB^2 N(0)。本文件用代数承载 N(0) 消去得纯数：

    Econd/(gamma Tc^2) = 3/(4 e^{2 gamma_E}) = 0.236427...
    Bc^2/(2 mu0) = 0.236 gamma Tc^2（临界场拉通）

  外部依据（只作工具）：SSRN 2026 Eq.(36)(40)(41)、Arovas 讲义 §1.2、WMI Table2。
  数值用 e^{gamma_E}=1.7810724179901979。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

namespace CQM.CondensationEnergyRatio

noncomputable section

/-- 欧拉常数指数 $e^{\gamma_E}$（数值）。 -/
def eGamma : ℝ := 1.7810724179901979

/-- 链内纯数 $\frac{3}{4e^{2\gamma_E}}$。 -/
def universalRatio : ℝ := 3 / (4 * eGamma ^ 2)

lemma ratio_bounds : 0.236 < universalRatio ∧ universalRatio < 0.237 := by
  unfold universalRatio eGamma
  norm_num

lemma ratio_pos : 0 < universalRatio := by
  unfold universalRatio eGamma
  positivity

/-- N(0) 消去：凝聚能/($\gamma T_c^2$) 的纯数化简。
    给定 $\Delta_0=\pi/e^\gamma k_BT_c$、$\gamma=\frac{2\pi^2}{3}k_B^2N(0)$，
    $\frac{\tfrac12 N\Delta_0^2}{\gamma T_c^2}=\frac{3}{4\pi^2}\frac{\Delta_0^2}{k_B^2T_c^2}=\frac{3}{4e^{2\gamma}}$。
    用 $E_{ratio}$ 记号承载消去后的 $\frac{3}{4\pi^2}r^2$（$r=\Delta_0/k_BT_c=\pi/e^\gamma$）。 -/
def eratio (r : ℝ) : ℝ := 3 / (4 * Real.pi ^ 2) * r ^ 2

lemma eratio_of_pi_over_eGamma : eratio (Real.pi / eGamma) = universalRatio := by
  unfold eratio universalRatio
  field_simp [ne_of_gt Real.pi_pos]

/-- 临界场拉通：$B_c^2/2\mu_0=\text{ratio}\cdot\gamma T_c^2$（代数结构）。 -/
def bcCond (ratio gamma Tc : ℝ) : ℝ := ratio * gamma * Tc ^ 2

lemma bcCond_pos (gamma Tc : ℝ) (hg : 0 < gamma) (hT : 0 < Tc) :
    0 < bcCond universalRatio gamma Tc := by
  unfold bcCond
  exact mul_pos (mul_pos ratio_pos hg) (sq_pos_of_pos hT)

/-- 强耦合偏差单调方向（定性骨架）：实测普适比随耦合偏离纯数。 -/
def coupling_dev (meas : ℝ) : ℝ := meas - universalRatio

lemma al_dev_small : |coupling_dev 0.2047| < 0.05 := by
  unfold coupling_dev universalRatio eGamma
  norm_num

end
end CQM.CondensationEnergyRatio
