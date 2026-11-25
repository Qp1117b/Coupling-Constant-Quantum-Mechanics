import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-!
# 环 15／19：`审-4` 关联阈值接入相界的代数骨架（第 156 轮）

只承载代数与序；不证明关联渗流指数、`rho` 归一、外部阈值数值。
无 `axiom`／`sorry`／`admit`／`native_decide`／`unsafe`。
-/

namespace CQM.CorrelationSiteBond

noncomputable section

/-- **阈值位移**：$\bar c>0$ ⇒ $p_c^{\rm eff}=p_c-\bar c/(2p_c)<p_c$。 -/
theorem threshold_shift {pc cbar pceff : ℝ} (hpc : 0 < pc) (hcbar : 0 < cbar)
    (h : pceff = pc - cbar / (2 * pc)) : pceff < pc := by
  rw [h]
  have hden : 0 < 2 * pc := by positivity
  have : 0 < cbar / (2 * pc) := div_pos hcbar hden
  linarith

/-- **零关联退化**：$\bar c=0$ ⇒ $p_c^{\rm eff}=p_c$。 -/
theorem zero_cbar_no_shift {pc cbar pceff : ℝ} (hpc : pc ≠ 0)
    (h : pceff = pc - cbar / (2 * pc)) (hc : cbar = 0) : pceff = pc := by
  rw [hc] at h
  rw [h]
  field_simp [hpc]
  ring

/-- **相界随有效阈值单调**：若 $0\le s<1$，则 $p_*(p_c)=p_c+(1-p_c)s$ 在 $p_c$ 上严格增。 -/
theorem pstar_strictMono {pc1 pc2 s : ℝ} (h12 : pc1 < pc2) (hs1 : s < 1) :
    pc1 + (1 - pc1) * s < pc2 + (1 - pc2) * s := by
  have h : (pc2 + (1 - pc2) * s) - (pc1 + (1 - pc1) * s) = (pc2 - pc1) * (1 - s) := by ring
  have hpos : 0 < (pc2 - pc1) * (1 - s) := mul_pos (sub_pos.mpr h12) (sub_pos.mpr hs1)
  linarith

/-- **座—键近阈等价的底数**：$q=p^2$ 时 $q'(p_c)(1-p_c)/(1-q_c)=2p_c/(1+p_c)$。 -/
theorem site_bond_base {pc : ℝ} (hpc0 : 0 < pc) (hpc1 : pc < 1) :
    ((2 * pc) * (1 - pc)) / (1 - pc ^ 2) = (2 * pc) / (1 + pc) := by
  have h1 : 1 - pc ≠ 0 := ne_of_gt (sub_pos.mpr hpc1)
  have h2 : 1 + pc ≠ 0 := ne_of_gt (by linarith : 0 < 1 + pc)
  have h3 : 1 - pc ^ 2 = (1 - pc) * (1 + pc) := by ring
  rw [h3]
  field_simp [h1, h2]

/-- **反解单调**：$\bar F^{-1}$ 严格减 ⇒ $p_*$ 下移给 $x_c$ 上移。 -/
theorem xc_up_when_pstar_down {F : ℝ → ℝ} {x1 x2 p1 p2 : ℝ}
    (hF : StrictAnti F) (hp : p1 < p2) (h1 : F x1 = p1) (h2 : F x2 = p2) :
    x2 < x1 := by
  by_contra hnot
  have hx : x1 ≤ x2 := le_of_not_gt hnot
  rcases lt_or_eq_of_le hx with hlt | heq
  · have hltF := hF hlt
    rw [h1, h2] at hltF
    linarith
  · rw [heq] at h1
    rw [h2] at h1
    linarith

end
end CQM.CorrelationSiteBond
