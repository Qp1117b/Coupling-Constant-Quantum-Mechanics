import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-!
# 环 19／目标区：Uemura 闭合与 $g_{\rm ren}$ 反演的代数骨架（第 155 轮）

只承载代数、序与 rpow 恒等式；不证明 RG 流、Uemura 实验律、绝对能标。
无 `axiom`／`sorry`／`admit`／`native_decide`／`unsafe`。
-/

namespace CQM.UemuraCurvatureInversion

noncomputable section

/-- **真实 BKT 定标**：$g\Upsilon_0w\Phi_c=2k_BT_c/\pi$、$\kappa=2k_BT_c/(\pi\Upsilon_0w)$ ⇒ $\Phi_c=\kappa/g$。 -/
theorem true_bkt_calibration {g U0 w Phi kap Tc kB : ℝ}
    (hg : g ≠ 0) (hU0 : U0 ≠ 0) (hw : w ≠ 0)
    (hjump : g * U0 * w * Phi = 2 * kB * Tc / Real.pi)
    (hkap : kap = 2 * kB * Tc / (Real.pi * U0 * w)) :
    Phi = kap / g := by
  have hj := congrArg (fun x : ℝ => x * Real.pi) hjump
  field_simp [Real.pi_ne_zero] at hj
  ring_nf at hj
  have hprod : Phi * Real.pi * U0 * w * g = 2 * kB * Tc := by
    ring_nf
    nlinarith [hj]
  rw [hkap]
  field_simp [hg, hU0, hw, Real.pi_ne_zero]
  rw [← hprod]

/-- **相界往返**：$\Phi(p_c+(1-p_c)\Phi^{1/t})=\Phi(p_*)$。 -/
theorem phi_roundtrip {pc phi t : ℝ} (hpc : pc < 1) (hphi : 0 < phi) (ht : t ≠ 0) :
    ((pc + (1 - pc) * phi ^ (t⁻¹) - pc) / (1 - pc)) ^ t = phi := by
  have hden : 1 - pc ≠ 0 := ne_of_gt (sub_pos.mpr hpc)
  have hq : (pc + (1 - pc) * phi ^ (t⁻¹) - pc) / (1 - pc) = phi ^ (t⁻¹) := by
    field_simp [hden]
    ring
  rw [hq]
  exact Real.rpow_inv_rpow (le_of_lt hphi) ht

/-- **$g_{\rm ren}$ 抵消**：把 $U_0=\Upsilon_0\Phi_0$、$r=w\kappa/(g\Phi_0)$ 代入 (U.1) 恒等于 $T_c$。 -/
theorem uemura_g_cancels {U0 Ubond Phi0 w kap g r Tc kB : ℝ}
    (hU0 : U0 = Ubond * Phi0) (hr : r = w * kap / (g * Phi0))
    (hkap : kap = 2 * kB * Tc / (Real.pi * Ubond * w))
    (hg : g ≠ 0) (hPhi0 : Phi0 ≠ 0) (hw : w ≠ 0) (hUb : Ubond ≠ 0) (hkB : kB ≠ 0) :
    (Real.pi / (2 * kB)) * U0 * r * g = Tc := by
  rw [hU0, hr, hkap]
  field_simp [hg, hPhi0, hw, hUb, hkB, Real.pi_ne_zero]

/-- **$\kappa$ 改写**：$\Upsilon_0=U(0)/\Phi_0$ ⇒ $\kappa=2k_BT_c\Phi_0/(\pi U(0)w)$。 -/
theorem kappa_from_U0 {U0 Phi0 w kap Tc kB : ℝ}
    (hPhi0 : Phi0 ≠ 0) (hw : w ≠ 0)
    (hkap : kap = 2 * kB * Tc / (Real.pi * (U0 / Phi0) * w)) :
    kap = 2 * kB * Tc * Phi0 / (Real.pi * U0 * w) := by
  rw [hkap]
  field_simp [hPhi0, hw]

/-- **曲率反解 $g$**：$\Phi_c=\kappa/g$ ⇒ $g=\kappa/\Phi_c$。 -/
theorem g_from_curvature {g kap Phi : ℝ} (hkap : kap ≠ 0)
    (h : Phi = kap / g) : g = kap / Phi := by
  rw [h]
  field_simp [hkap]

/-- **曲率到放大系数**：$c_2=a(1+B)$、$a\ne0$ ⇒ $B=c_2/a-1$。 -/
theorem B_of_curvature {c2 a B : ℝ} (ha : a ≠ 0) (h : c2 = a * (1 + B)) :
    B = c2 / a - 1 := by
  rw [h]
  field_simp [ha]
  ring

/-- **可行性下界**：$\kappa\le g\le1$、$\kappa>0$ ⇒ $U0\ge 2k_BT_c\Phi_0/(\pi w)$。 -/
theorem feasibility_lower_bound {U0 w Phi0 Tc kB kap g : ℝ}
    (hwpos : 0 < w) (hTc : 0 < Tc) (hkB : 0 < kB) (hPhi0 : 0 < Phi0)
    (hkap : kap = 2 * kB * Tc * Phi0 / (Real.pi * U0 * w)) (hkap_pos : 0 < kap)
    (hkg : kap ≤ g) (hg1 : g ≤ 1) :
    2 * kB * Tc * Phi0 / (Real.pi * w) ≤ U0 := by
  have hnumpos : 0 < 2 * kB * Tc * Phi0 := by positivity
  have hkap_pos' : 0 < 2 * kB * Tc * Phi0 / (Real.pi * U0 * w) := by
    simpa [hkap] using hkap_pos
  have hdenpos : 0 < Real.pi * U0 * w := by
    rcases (div_pos_iff.mp hkap_pos') with h | h
    · exact h.2
    · linarith
  have hk1 : 2 * kB * Tc * Phi0 / (Real.pi * U0 * w) ≤ 1 := by
    rw [← hkap]
    exact le_trans hkg hg1
  rw [div_le_iff₀ hdenpos] at hk1
  have hwpipos : 0 < Real.pi * w := by positivity
  rw [div_le_iff₀ hwpipos]
  nlinarith [hk1]

end
end CQM.UemuraCurvatureInversion
