import Mathlib.Tactic.Linarith
import Mathlib.Data.Real.Basic

/-!
# R17: 赝能隙存在判据的代数核（从已闭合 ≤min 推出）

记 Tphi = min{T_BKT,T_theta}，Tc ≤ min{T*,Tphi}（R16 已闭合）。
- 符号闭合：Tc ≤ T* ⇒ ΔTpg = T* - Tc ≥ 0
- 存在充分判据：Tphi < T* ⇒ Tc < T* ⇒ ΔTpg > 0
- 反向不推出：T* ≤ Tphi 时 ΔTpg 可为 0（反例）
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.PseudogapCriterion

noncomputable section

/-- 符号闭合：Tc ≤ T* ⇒ T* - Tc ≥ 0。 -/
theorem pseudogap_nonneg (Tc Tstar : ℝ) (h : Tc ≤ Tstar) : 0 ≤ Tstar - Tc := by
  linarith

/-- 存在充分判据：Tc ≤ min{T*,Tphi} 且 Tphi < T* ⇒ Tc < T* ⇒ T* - Tc > 0。 -/
theorem pseudogap_exists_of_phase_tighter (Tc Tstar Tphi : ℝ)
    (hTc : Tc ≤ min Tstar Tphi) (hphase : Tphi < Tstar) :
    0 < Tstar - Tc := by
  have hle : Tc ≤ Tphi := le_trans hTc (min_le_right _ _)
  have hlt : Tc < Tstar := lt_of_le_of_lt hle hphase
  linarith

/-- 反向不推出：T* ≤ Tphi 且 Tc = T* 满足 Tc ≤ min，但 ΔTpg = 0（赝能隙可不存在）。 -/
theorem reverse_not_forced :
    ∃ (Tc Tstar Tphi : ℝ), Tc ≤ min Tstar Tphi ∧ Tstar ≤ Tphi ∧ Tstar - Tc = 0 := by
  refine ⟨5, 5, 8, ?_⟩
  constructor
  · norm_num
  constructor <;> norm_num

end
end CQM.PseudogapCriterion
