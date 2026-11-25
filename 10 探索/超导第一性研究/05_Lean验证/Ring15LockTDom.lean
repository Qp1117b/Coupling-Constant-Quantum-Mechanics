-- Ring15LockTDom.lean（第 195 轮）：G-186c 的条件式主导项闸与充要判据
-- 只 import Spec；无 sorry／admit／自造 axiom。
import Ring15Spec

namespace CQM.Ring15.LockTDom

open CQM.Ring15.Spec

noncomputable section

/-- 反号分解的同一恒等式（194 轮的 `tEffM_split` 在本模块内自足重写，因模块只能 import Spec）：
$\Delta=(m/N)\,[\,(\ln(1-y_2)-\ln(1-y_1))\ln p_1+\ln(1-y_1)(\ln p_1-\ln p_2)\,]$，$N=\ln p_1\ln p_2$。 -/
private lemma tEffM_split (p1 p2 y1 y2 : ℝ) (m : ℕ)
    (h1 : Real.log p1 ≠ 0) (h2 : Real.log p2 ≠ 0) :
    tEffM p2 y2 m - tEffM p1 y1 m
      = (m : ℝ) * ((Real.log (1 - y2) - Real.log (1 - y1)) * Real.log p1
          + Real.log (1 - y1) * (Real.log p1 - Real.log p2)) / (Real.log p1 * Real.log p2) := by
  unfold tEffM
  field_simp [h1, h2]
  ring

private lemma one_le_nat_cast_pos (m : ℕ) (hm : 1 ≤ m) : (0 : ℝ) < (m : ℝ) := by
  have h0 : 0 < m := lt_of_lt_of_le Nat.zero_lt_one hm
  exact_mod_cast h0

/-- 主导项闸：$y$ 项压过 $p$ 项时，复合后的 $t$ 仍严格增。 -/
theorem targetPropTChanDominate : TargetPropTChanDominate := by
  intro p1 p2 y1 y2 m hp2 hp21 hp1 hy1 hy12 hy2 hm hS
  have hp1pos : (0 : ℝ) < p1 := lt_trans hp2 hp21
  have hlogp1 : Real.log p1 < 0 := Real.log_neg hp1pos hp1
  have hlogp2 : Real.log p2 < 0 := Real.log_neg hp2 (by linarith)
  have hN : 0 < Real.log p1 * Real.log p2 := mul_pos_of_neg_of_neg hlogp1 hlogp2
  have hmpos : (0 : ℝ) < (m : ℝ) := one_le_nat_cast_pos m hm
  have hpos : 0 < tEffM p2 y2 m - tEffM p1 y1 m := by
    rw [tEffM_split p1 p2 y1 y2 m (ne_of_lt hlogp1) (ne_of_lt hlogp2)]
    exact div_pos (mul_pos hmpos hS) hN
  linarith

/-- 充要判据：复合的符号完全由"两通道之和"的符号决定。 -/
theorem targetPropTChanCriterion : TargetPropTChanCriterion := by
  intro p1 p2 y1 y2 m hp2 hp21 hp1 hy1 hy12 hy2 hm
  have hp1pos : (0 : ℝ) < p1 := lt_trans hp2 hp21
  have hlogp1 : Real.log p1 < 0 := Real.log_neg hp1pos hp1
  have hlogp2 : Real.log p2 < 0 := Real.log_neg hp2 (by linarith)
  have hN : 0 < Real.log p1 * Real.log p2 := mul_pos_of_neg_of_neg hlogp1 hlogp2
  have hmpos : (0 : ℝ) < (m : ℝ) := one_le_nat_cast_pos m hm
  have hsplit := tEffM_split p1 p2 y1 y2 m (ne_of_lt hlogp1) (ne_of_lt hlogp2)
  constructor
  · intro hlt
    have hΔ : 0 < tEffM p2 y2 m - tEffM p1 y1 m := by linarith
    rw [hsplit] at hΔ
    rcases div_pos_iff.mp hΔ with ⟨hmS, _⟩ | ⟨_, hNneg⟩
    · exact pos_of_mul_pos_right hmS (le_of_lt hmpos)
    · exact absurd hNneg (not_lt.mpr (le_of_lt hN))
  · intro hS
    have hpos : 0 < tEffM p2 y2 m - tEffM p1 y1 m := by
      rw [hsplit]
      exact div_pos (mul_pos hmpos hS) hN
    linarith

end

end CQM.Ring15.LockTDom
