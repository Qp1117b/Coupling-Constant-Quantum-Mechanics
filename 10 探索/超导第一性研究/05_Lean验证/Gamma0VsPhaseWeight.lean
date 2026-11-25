/-
  R27：Gamma_0 线性 vs 相位权重——零点不相容
  ============================================================
  外部原文（PRB 57 R11093 (1998)；Nature Physics 2, 447 (2006)）：
    Gamma_0(T) = a*(T-Tc)（a>0），Gamma_0(Tc)=0，T* 由 Delta≈Gamma_0(T*) 定。
  链内 (10B.1)/(10B.5)：w(T)=V_coh/Z，1-w(T)>0 对任意 T>0；
    低温展开 1-w≈(pi^2/3)(T/omega_D)^2 只在 T<<omega_D 有效。

  本文件承载：
    (1) 线性宽度在 Tc 处为零、且对 T 严格增；
    (2) 对任意正常数 C、omega_D，C*omega_D*(1-w(Tc)) > 0；
    (3) no-go：常数重标度 C*omega_D*(1-w(T)) = a*(T-Tc) 在 T=Tc 处矛盾；
    (4) 单点数值接近（脚本 P3）不等于函数相等。

  不证明：Gamma_0 的链内第一性来源（缺对寿命，06 L1350 未闭合）；
          G21 的定量谱映射（缺 q 的空间分布与对寿命）。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

namespace CQM.Gamma0VsPhaseWeight

noncomputable section

/-- (1) 线性对寿命宽度在 $T_c$ 处严格为零。 -/
theorem gamma_zero_at_tc (a Tc : ℝ) : a * (Tc - Tc) = 0 := by ring

/-- (1′) $a>0$ 时 $\\Gamma_0(T)=a(T-T_c)$ 对 $T$ 严格递增。 -/
theorem gamma_strict_mono (a T1 T2 Tc : ℝ) (ha : 0 < a) (h : T1 < T2) :
    a * (T1 - Tc) < a * (T2 - Tc) := by
  nlinarith

/-- (2) 链内相位权重在 $T_c$ 处为正 ⇒ 任意正重标度仍为正。 -/
theorem phase_weight_scaled_pos (C wD pwTc : ℝ) (hC : 0 < C) (hwD : 0 < wD)
    (hpw : 0 < pwTc) : 0 < C * wD * pwTc := by positivity

/-- (3) no-go：若候选在 $T_c$ 处等于 $\\Gamma_0(T_c)=0$，与相位权重为正矛盾。 -/
theorem no_rescale_at_tc (a C wD pwTc Tc : ℝ) (hC : 0 < C)
    (hwD : 0 < wD) (hpw : 0 < pwTc)
    (h : C * wD * pwTc = a * (Tc - Tc)) : False := by
  have hzero : a * (Tc - Tc) = 0 := by ring
  rw [hzero] at h
  have hpos : 0 < C * wD * pwTc := phase_weight_scaled_pos C wD pwTc hC hwD hpw
  linarith

/-- (4) 单点相等不推出函数相等：若所有 $T$ 相等，则在 $T_c$ 必相等（供反证使用）。 -/
theorem pointwise_at_tc {pw : ℝ → ℝ} (hAll : ∀ T, C0 * wD0 * pw T = a0 * (T - Tc0))
    (hposTc : 0 < pw Tc0) (hC : 0 < C0) (hwD : 0 < wD0) : False := by
  have hTc := hAll Tc0
  exact no_rescale_at_tc a0 C0 wD0 (pw Tc0) Tc0 hC hwD hposTc hTc

end
end CQM.Gamma0VsPhaseWeight
