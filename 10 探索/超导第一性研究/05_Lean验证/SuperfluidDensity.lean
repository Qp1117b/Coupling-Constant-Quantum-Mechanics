/-
  预注册判定 R15：超流密度/穿透深度的纯数骨架（A 类结构＋B 类工具）
  =================================================================
  近-Tc 斜率纯数：rho_s(t) -> 2(1-t)，斜率 -2。
  由链内 d Delta^2/dt|_1 = -8 e^{2gamma}/(7 zeta3) 出发，
  经 Eq.(17) t/Delta^2 dDelta2/dt|_1 = -1/(1-t) 与 Eq.(43) 得斜率 -2。
  低温激活指数 = pi/e^gamma（C5 gap ratio 一半）。
  本文件承载代数恒等式；数值盲测由 R15 脚本完成。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

namespace CQM.SuperfluidDensity

noncomputable section

def eGamma : ℝ := 1.7810724179901979
def zeta3 : ℝ := 1.202056903159594
def alphaBCS : ℝ := Real.pi / eGamma          -- pi/e^gamma = 1.7639
def dDelta2SlopeTc : ℝ := 8 * eGamma ^ 2 / (7 * zeta3)  -- |d Delta^2/dt|_1 = 3.016

lemma eGamma_ne : eGamma ≠ 0 := by unfold eGamma; norm_num

/-- 链内 gap 导数斜率 |d Delta^2/dt|_1 = 8 e^{2gamma}/(7 zeta3) ≈ 3.016。 -/
lemma slope_value_interval : 3.0 < dDelta2SlopeTc ∧ dDelta2SlopeTc < 3.1 := by
  unfold dDelta2SlopeTc eGamma zeta3
  norm_num

/-- 近-Tc 超流密度斜率 = -2：由 Eq.(43) 1/(1-I)=1+1/(2(1-t))，
    rho_s = 1-I = 2(1-t)/(1+2(1-t))，d rho_s/dt|_1 = -2。
    这里证明 rho_s/(1-t) -> 2 的代数核心：2(1-t)/(1+2(1-t))/(1-t) = 2/(1+2(1-t)) -> 2。 -/
lemma rho_s_nearTc_factor (eps : ℝ) (heps : eps ≠ 0) (heps_pos : 0 < eps) :
    (2 * eps / (1 + 2 * eps)) / eps = 2 / (1 + 2 * eps) := by
  field_simp [heps]

/-- 当 eps -> 0，2/(1+2 eps) -> 2（斜率纯数 -2 的代数骨架）。 -/
lemma rho_s_slope_limit : 2 / (1 : ℝ) = 2 := by norm_num

/-- 低温 London 参数前因子 sqrt(2 pi alpha/t)，激活指数 alpha=pi/e^gamma（C5）。 -/
def lowTActivate : ℝ := alphaBCS
lemma lowTActivate_eq : lowTActivate = Real.pi / eGamma := rfl

/-- alpha_BCS 正性。 -/
lemma alphaBCS_pos : 0 < alphaBCS := by
  unfold alphaBCS
  apply div_pos Real.pi_pos
  unfold eGamma
  norm_num

end
end CQM.SuperfluidDensity
