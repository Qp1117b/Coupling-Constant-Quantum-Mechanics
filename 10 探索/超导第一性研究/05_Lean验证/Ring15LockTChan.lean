-- Ring15LockTChan.lean（第 194 轮）：$t$ 的两条通道方向相反——$t$ 对 $p$ 严格增，复合为反号两项之和
-- 只 import Spec；无 sorry／admit／自造 axiom。
import Ring15Spec

namespace CQM.Ring15.LockTChan

open CQM.Ring15.Spec

noncomputable section

/-- 固定 $y$、变 $p$ 的差商：$t(p_1)-t(p_2)=m\ln(1-y)\cdot\dfrac{\ln p_2-\ln p_1}{\ln p_1\ln p_2}$。 -/
private lemma tEffM_diff_p (p1 p2 y : ℝ) (m : ℕ)
    (h1 : Real.log p1 ≠ 0) (h2 : Real.log p2 ≠ 0) :
    tEffM p1 y m - tEffM p2 y m
      = (m : ℝ) * (Real.log (1 - y) * (Real.log p2 - Real.log p1)
          / (Real.log p1 * Real.log p2)) := by
  unfold tEffM
  field_simp [h1, h2]
  ring

/-- $p$ 通道：$t$ 对 $p$ 严格增（$p$ 越小，$t$ 越小）。 -/
theorem targetPropTEffMPMono : TargetPropTEffMPMono := by
  intro p1 p2 y m hp2 hp21 hp1 hy0 hy1 hm
  have hp1pos : (0 : ℝ) < p1 := lt_trans hp2 hp21
  have hlogp2 : Real.log p2 < 0 := Real.log_neg hp2 (by linarith)
  have hlogp1 : Real.log p1 < 0 := Real.log_neg hp1pos hp1
  have hlog21 : Real.log p2 - Real.log p1 < 0 := by
    have h := Real.log_lt_log hp2 hp21
    linarith
  have hL : Real.log (1 - y) < 0 := Real.log_neg (by linarith) (by linarith)
  have hnum : 0 < Real.log (1 - y) * (Real.log p2 - Real.log p1) :=
    mul_pos_of_neg_of_neg hL hlog21
  have hden : 0 < Real.log p1 * Real.log p2 := mul_pos_of_neg_of_neg hlogp1 hlogp2
  have hquot : 0 < Real.log (1 - y) * (Real.log p2 - Real.log p1) / (Real.log p1 * Real.log p2) :=
    div_pos hnum hden
  have hm0 : 0 < m := lt_of_lt_of_le Nat.zero_lt_one hm
  have hmpos : (0 : ℝ) < (m : ℝ) := by exact_mod_cast hm0
  have hpos : 0 < tEffM p1 y m - tEffM p2 y m := by
    rw [tEffM_diff_p p1 p2 y m (ne_of_lt hlogp1) (ne_of_lt hlogp2)]
    exact mul_pos hmpos hquot
  linarith

/-- 两通道的反号分解（同一恒等式）：
$\Delta=(m/N)\,[\,(\ln(1-y_2)-\ln(1-y_1))\ln p_1+\ln(1-y_1)(\ln p_1-\ln p_2)\,]$，$N=\ln p_1\ln p_2>0$。 -/
private lemma tEffM_split (p1 p2 y1 y2 : ℝ) (m : ℕ)
    (h1 : Real.log p1 ≠ 0) (h2 : Real.log p2 ≠ 0) :
    tEffM p2 y2 m - tEffM p1 y1 m
      = (m : ℝ) * ((Real.log (1 - y2) - Real.log (1 - y1)) * Real.log p1
          + Real.log (1 - y1) * (Real.log p1 - Real.log p2)) / (Real.log p1 * Real.log p2) := by
  unfold tEffM
  field_simp [h1, h2]
  ring

theorem targetPropTChanSplit : TargetPropTChanSplit := by
  intro p1 p2 y1 y2 m hp2 hp21 hp1 hy1 hy12 hy2 hm
  have hp1pos : (0 : ℝ) < p1 := lt_trans hp2 hp21
  have hlogp2 : Real.log p2 < 0 := Real.log_neg hp2 (by linarith)
  have hlogp1 : Real.log p1 < 0 := Real.log_neg hp1pos hp1
  have hlogdiff : 0 < Real.log p1 - Real.log p2 := by
    have h := Real.log_lt_log hp2 hp21
    linarith
  have hLdiff : Real.log (1 - y2) - Real.log (1 - y1) < 0 := by
    have hpos2 : (0 : ℝ) < 1 - y2 := by linarith
    have hlt : 1 - y2 < 1 - y1 := by linarith
    have h := Real.log_lt_log hpos2 hlt
    linarith
  have hL1 : Real.log (1 - y1) < 0 := Real.log_neg (by linarith) (by linarith)
  refine ⟨tEffM_split p1 p2 y1 y2 m (ne_of_lt hlogp1) (ne_of_lt hlogp2), ?_, ?_⟩
  · exact mul_pos_of_neg_of_neg hLdiff hlogp1
  · exact mul_neg_of_neg_of_pos hL1 hlogdiff

end

end CQM.Ring15.LockTChan
