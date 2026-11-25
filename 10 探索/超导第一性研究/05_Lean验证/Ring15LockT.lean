-- Ring15LockT.lean（第 186 轮）：粗粒化指数 t 对逸度 y 的单调与下界
-- 只 import Spec（v13）；无 sorry／admit／自造 axiom。
import Ring15Spec

namespace CQM.Ring15.LockT

open CQM.Ring15.Spec

noncomputable section

/-- 差商写法：$t(y_2)-t(y_1)=m\cdot[\ln(1-y_2)-\ln(1-y_1)]/\ln p$。 -/
private lemma tEffM_sub (p y1 y2 : ℝ) (m : ℕ) :
    tEffM p y2 m - tEffM p y1 m
      = (m : ℝ) * ((Real.log (1 - y2) - Real.log (1 - y1)) / Real.log p) := by
  unfold tEffM
  field_simp
  ring

theorem targetPropTEffMMono : TargetPropTEffMMono := by
  intro p y1 y2 m hp0 hp1 hy1 h12 hy2 hm
  have hpos2 : (0 : ℝ) < 1 - y2 := by linarith
  have hlog : Real.log (1 - y2) < Real.log (1 - y1) :=
    Real.log_lt_log hpos2 (by linarith)
  have hlogp : Real.log p < 0 := Real.log_neg hp0 hp1
  have hnum : Real.log (1 - y2) - Real.log (1 - y1) < 0 := by linarith
  have hquot : 0 < (Real.log (1 - y2) - Real.log (1 - y1)) / Real.log p :=
    (div_pos_iff).mpr (Or.inr ⟨hnum, hlogp⟩)
  have hm0 : 0 < m := lt_of_lt_of_le Nat.zero_lt_one hm
  have hmpos : (0 : ℝ) < (m : ℝ) := by exact_mod_cast hm0
  have hdiff : tEffM p y2 m - tEffM p y1 m
      = (m : ℝ) * ((Real.log (1 - y2) - Real.log (1 - y1)) / Real.log p) :=
    tEffM_sub p y1 y2 m
  have hpos : 0 < tEffM p y2 m - tEffM p y1 m := by
    rw [hdiff]
    exact mul_pos hmpos hquot
  linarith

theorem targetPropTEffMGeOne : TargetPropTEffMGeOne := by
  intro p y m hp0 hp1 hy0 hy1 hm
  have hsub : tEffM p y m - tEffM p 0 m
      = (m : ℝ) * ((Real.log (1 - y) - Real.log (1 - 0)) / Real.log p) :=
    tEffM_sub p 0 y m
  have hzero : tEffM p 0 m = 1 := by
    unfold tEffM
    have : Real.log (1 - (0 : ℝ)) = 0 := by norm_num
    rw [this]
    ring
  have hlogp : Real.log p < 0 := Real.log_neg hp0 hp1
  have hpos1 : (0 : ℝ) < 1 - y := by linarith
  have hle : 1 - y ≤ 1 := by linarith
  have hlogle : Real.log (1 - y) ≤ 0 := Real.log_nonpos (by linarith) hle
  have hnum : Real.log (1 - y) - Real.log (1 - 0) ≤ 0 := by
    have : Real.log (1 - (0 : ℝ)) = 0 := by norm_num
    rw [this]
    linarith
  have hquot : 0 ≤ (Real.log (1 - y) - Real.log (1 - 0)) / Real.log p := by
    have hneg : (Real.log (1 - y) - Real.log (1 - 0)) / Real.log p
        = (-(Real.log (1 - y) - Real.log (1 - 0))) / (-(Real.log p)) := by
      rw [neg_div_neg_eq]
    rw [hneg]
    exact div_nonneg (by linarith) (by linarith)
  have hm0 : 0 < m := lt_of_lt_of_le Nat.zero_lt_one hm
  have hmpos : (0 : ℝ) < (m : ℝ) := by exact_mod_cast hm0
  have hdiff : 0 ≤ tEffM p y m - tEffM p 0 m := by
    rw [hsub]
    exact mul_nonneg (le_of_lt hmpos) hquot
  rw [hzero] at hdiff
  linarith

end

end CQM.Ring15.LockT
