-- 环 15 / 审-6（第 182 轮）：锁条件的 ε 空间比值判据
-- 只 import Spec：|Δλ| > 1/(4|s|) ⇔ 周长比之比 > exp(1/(2|s|))
import Ring15Spec

namespace CQM.Ring15.LockRatio

open CQM.Ring15.Spec

lemma one_sub_div_pos' {e : ℝ} (he : e < 2 * Real.pi) : 0 < 1 - e / (2 * Real.pi) := by
  have hπ : (0 : ℝ) < 2 * Real.pi := by positivity
  have h : e / (2 * Real.pi) < 1 := (div_lt_one hπ).mpr he
  linarith

/-- 比值判据。 -/
theorem lock_ratio (s e1 e2 : ℝ) (hs : s ≠ 0) (h1 : e1 < 2 * Real.pi)
    (h2 : e2 < 2 * Real.pi) (h12 : e1 < e2) :
    (lockLam e1 - lockLam e2 > 1 / (4 * |s|)) ↔
      ((1 - e1 / (2 * Real.pi)) / (1 - e2 / (2 * Real.pi)) > Real.exp (1 / (2 * |s|))) := by
  have hA : 0 < 1 - e1 / (2 * Real.pi) := one_sub_div_pos' h1
  have hB : 0 < 1 - e2 / (2 * Real.pi) := one_sub_div_pos' h2
  have hs2 : (0 : ℝ) < |s| := abs_pos.mpr hs
  set R : ℝ := (1 - e1 / (2 * Real.pi)) / (1 - e2 / (2 * Real.pi)) with hRdef
  have hR : 0 < R := by rw [hRdef]; exact div_pos hA hB
  have hkey : lockLam e1 - lockLam e2 = (1 / 2) * Real.log R := by
    simp only [lockLam]
    rw [hRdef, Real.log_div (ne_of_gt hA) (ne_of_gt hB), mul_sub]
  rw [hkey]
  have h2c : 2 * (1 / (4 * |s|)) = 1 / (2 * |s|) := by
    have hsne : |s| ≠ 0 := ne_of_gt hs2
    field_simp
    ring
  have hthr : ((1 / 2) * Real.log R > 1 / (4 * |s|)) ↔ Real.log R > 1 / (2 * |s|) := by
    constructor
    · intro hh
      nlinarith [hh, h2c, hs2]
    · intro hh
      nlinarith [hh, h2c, hs2]
  rw [hthr]
  rw [show (Real.log R > 1 / (2 * |s|)) ↔ (Real.exp (1 / (2 * |s|)) < R) from
    Real.lt_log_iff_exp_lt (y := R) hR]

/-- Spec 主定理。 -/
theorem targetPropLockRatio : TargetPropLockRatio := fun s e1 e2 hs h1 h2 h12 =>
  lock_ratio s e1 e2 hs h1 h2 h12

end CQM.Ring15.LockRatio
