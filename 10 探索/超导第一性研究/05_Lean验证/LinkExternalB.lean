/-
  R22：链外-B 载体辨析——相位刚度与超流密度的温度律不同（代数骨架）
  ==================================================================
  链内相位扇区 (10B.5)/(10B.10)：
    w(T) = 1 - c*T^2  (c = pi^2/(3 wD^2) > 0, 低温展开)
    Upsilon(T) = Upsilon_0 * w(T)
  振幅扇区（C5 gap）超流密度 rho_s(T)：Tc 归零，准粒子型。
  London 关系：lambda^{-2} = k * rho_s (k>0)。

  本文件只承载代数结构：
    (1) w(T) 在 T>=0 上严格递减；
    (2) Upsilon(T) 随 w 递减（Upsilon_0>0）；
    (3) 若 c*Tc^2<1 则 w(Tc)>0（相位刚度在 Tc 不为零）；
    (4) lambda^{-2} 随 rho_s 递增（即 lambda 随 rho_s 递减）。
  不证明：两流体/BCS 映射、rho_s(Tc)=0 的具体形式、绝对数值。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

namespace CQM.LinkExternalB

noncomputable section

/-- 相位扇区低温权重截面：w(T)=1-c*T^2（(10B.5)，c=pi^2/(3 wD^2)>0）。 -/
def wPhase (c T : ℝ) : ℝ := 1 - c * T ^ 2

/-- 相位刚度：Upsilon(T)=Upsilon_0*w(T)。 -/
def upsilon (U0 c T : ℝ) : ℝ := U0 * wPhase c T

/-- London 关系截面：lambda^{-2}=k*rho_s（k>0）。 -/
def lambdaInvSq (k rho : ℝ) : ℝ := k * rho

/-- (1) w(T) 在 T>=0 上严格递减：0<=T1<T2 ⇒ w(T2)<w(T1)。 -/
theorem wPhase_lt (c T1 T2 : ℝ) (hc : 0 < c) (h0 : 0 ≤ T1) (hlt : T1 < T2) :
    wPhase c T2 < wPhase c T1 := by
  unfold wPhase
  have hsq : T1 ^ 2 < T2 ^ 2 := by nlinarith
  have hc' : c * T1 ^ 2 < c * T2 ^ 2 := by nlinarith
  linarith

/-- (2) Upsilon(T) 随 w 递减（Upsilon_0>0）。 -/
theorem upsilon_lt (U0 c T1 T2 : ℝ) (hU : 0 < U0) (hc : 0 < c)
    (h0 : 0 ≤ T1) (hlt : T1 < T2) :
    upsilon U0 c T2 < upsilon U0 c T1 := by
  unfold upsilon
  have h := wPhase_lt c T1 T2 hc h0 hlt
  nlinarith

/-- (3) 若 c*Tc^2<1，则相位刚度在 Tc 不为零：w(Tc)>0。 -/
theorem wPhase_pos_at_Tc (c Tc : ℝ) (h : c * Tc ^ 2 < 1) :
    0 < wPhase c Tc := by
  unfold wPhase
  linarith

/-- (4) lambda^{-2} 随 rho_s 递增：rho1<rho2 ⇒ lambdaInvSq rho1 < lambdaInvSq rho2。 -/
theorem lambdaInvSq_lt (k rho1 rho2 : ℝ) (hk : 0 < k) (hlt : rho1 < rho2) :
    lambdaInvSq k rho1 < lambdaInvSq k rho2 := by
  unfold lambdaInvSq
  nlinarith

/-- (5) 结构判定：若 w(Tc)>0 而 rho_s(Tc)=0，则两者不是同一温度函数。 -/
theorem not_same_function (wTc : ℝ) (hw : 0 < wTc) : wTc ≠ (0 : ℝ) := by
  linarith

end
end CQM.LinkExternalB
