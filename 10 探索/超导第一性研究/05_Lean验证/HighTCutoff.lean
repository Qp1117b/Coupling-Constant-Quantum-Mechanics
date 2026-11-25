import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-!
# 环 19／目标区：$G(y)$ 高温截断的代数骨架（第 158 轮）

只承载代数与序；不证明卡方 CDF、`w(T)` 单调、$t_\Upsilon$ 普适性。
无 `axiom`／`sorry`／`admit`／`native_decide`／`unsafe`。
-/

namespace CQM.HighTCutoff

noncomputable section

/-- **截断恒等式**：$1-F(x_cw_c/y_*)=p_c$ 且 $F(F^{-1}(1-p_c))=1-p_c$ ⇒ $x_cw_c/y_*=F^{-1}(1-p_c)$。 -/
theorem cutoff_argument {F invF : ℝ → ℝ} {y xc wc pc : ℝ}
    (hinv : F (invF (1 - pc)) = 1 - pc) (hF : Function.Injective F)
    (h : 1 - F (xc * wc / y) = pc) :
    xc * wc / y = invF (1 - pc) := by
  have hval : F (xc * wc / y) = 1 - pc := by linarith
  exact hF (hval.trans hinv.symm)

/-- **截断取值**：$y_*=x_cw_c/F^{-1}(1-p_c)$。 -/
theorem y_star_formula {F invF : ℝ → ℝ} {y xc wc pc : ℝ}
    (hinv : F (invF (1 - pc)) = 1 - pc) (hF : Function.Injective F)
    (hy : y ≠ 0) (hden : invF (1 - pc) ≠ 0)
    (h : 1 - F (xc * wc / y) = pc) :
    y = xc * wc / invF (1 - pc) := by
  have harg := cutoff_argument hinv hF h
  field_simp [hy, hden] at harg ⊢
  linarith

/-- **严格两尺度**：$p$ 严格反单调、$p(T_c)=p_*>p_c=p(T_*)$ ⇒ $T_c<T_*$。 -/
theorem tc_lt_tstar {p : ℝ → ℝ} {Tc Ts ps pc : ℝ}
    (hp : StrictAnti p) (hps : pc < ps) (h1 : p Tc = ps) (h2 : p Ts = pc) :
    Tc < Ts := by
  by_contra hnot
  have hle : Ts ≤ Tc := le_of_not_gt hnot
  rcases lt_or_eq_of_le hle with hlt | heq
  · have hplt := hp hlt
    rw [h1, h2] at hplt
    linarith
  · rw [← heq] at h1
    rw [h2] at h1
    linarith

/-- **支撑外归零**：$\Phi=0$ ⇒ $G=0$。 -/
theorem G_zero_below_cutoff {y phiv phi0 : ℝ} (h : phiv = 0) :
    y * phiv / phi0 = 0 := by
  rw [h]
  simp

/-- **两通路一致**：$x_c^{\rm low}=x_c^{\rm high}$ 时截断与曲率给同一 $x_c$（代数骨架）。 -/
theorem two_route_agree {xcLow xcHigh ystar wc invv : ℝ}
    (hlow : xcLow = xcHigh)
    (hhigh : xcHigh = ystar * invv / wc) :
    xcLow = ystar * invv / wc := by
  rw [hlow, hhigh]

end
end CQM.HighTCutoff
