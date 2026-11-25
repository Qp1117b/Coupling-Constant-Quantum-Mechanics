import Mathlib.Tactic.Linarith
import Mathlib.Data.Real.Basic

/-!
# R39: R17 赝能隙判据实证核对的代数核（隔离区）

- 符号判据：ΔT_pg = T* - Tc ≥ 0（当 Tc ≤ T*）
- 正性：T_phi < T* 且 Tc ≤ T_phi ⇒ ΔT_pg > 0（R17.3）
- 定义区分：链 T* 是结构性配对上限（Tc≤T* 恒成立）；实验 Tν/Tρ 是现象学读数，
  二者不同谓词，不能等同（用不同类型标记，防止范畴混淆）。
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.PseudogapDataCheck

noncomputable section

/-- 赝能隙宽度 ΔT_pg = T* - Tc。 -/
def deltaT (Tstar Tc : ℝ) : ℝ := Tstar - Tc

/-- R17.2 符号闭合：Tc ≤ T* ⇒ ΔT_pg ≥ 0。 -/
theorem delta_nonneg (Tstar Tc : ℝ) (hle : Tc ≤ Tstar) : 0 ≤ deltaT Tstar Tc := by
  unfold deltaT
  linarith

/-- R17.3 正性：T_phi < T* 且 Tc ≤ T_phi ⇒ ΔT_pg > 0。 -/
theorem delta_pos (Tstar Tc Tphi : ℝ) (hphi_star : Tphi < Tstar) (hc_phi : Tc ≤ Tphi) :
    0 < deltaT Tstar Tc := by
  unfold deltaT
  linarith

/-- 等于 0 的可能（R17 结论 3：配对支最严时可能为零）。 -/
theorem delta_zero_possible : deltaT 50 50 = 0 := by
  unfold deltaT
  norm_num

-- 注：链 T* 是结构性配对上限（Tc≤T* 由构造），实验 Tν/Tρ 是现象学读数，
-- 二者是不同概念——此区分在推导卡文字中陈述，不靠伪形式化"证明"（R28 教训）。

end
end CQM.PseudogapDataCheck
