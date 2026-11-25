-- Ring15LockPhi.lean（第 189 轮）：Phi 是否进入 (15L.3) 的授权域
-- 只 import Spec（v16）；无 sorry／admit／自造 axiom。
import Ring15Spec

namespace CQM.Ring15.LockPhi

open CQM.Ring15.Spec

noncomputable section

theorem targetPropPhiMono : TargetPropPhiMono := by
  intro k Φ1 Φ2 hk h1 h12
  have hπ2 : (0 : ℝ) < Real.pi ^ 2 := pow_pos Real.pi_pos 2
  have hK : k * Φ1 ≤ k * Φ2 := mul_le_mul_of_nonneg_left h12 (le_of_lt hk)
  have hmul : Real.pi ^ 2 * (k * Φ1) ≤ Real.pi ^ 2 * (k * Φ2) :=
    mul_le_mul_of_nonneg_left hK (le_of_lt hπ2)
  have hE : -(Real.pi ^ 2 * (k * Φ2) / 2) ≤ -(Real.pi ^ 2 * (k * Φ1) / 2) := by
    have h3 : Real.pi ^ 2 * (k * Φ1) / 2 ≤ Real.pi ^ 2 * (k * Φ2) / 2 := by linarith [hmul]
    linarith [h3]
  exact mul_le_mul_of_nonneg_left (Real.exp_le_exp.mpr hE) (by positivity)

/-- 私有：BKT 钉住处 $K=\Upsilon/T$ 恰好等于 $2/\pi$。 -/
private lemma bkt_K (T U0 w : ℝ) (hT : 0 < T) (hU0 : 0 < U0) (hw : 0 < w) :
    U0 * w * phiBkt T U0 w / T = 2 / Real.pi := by
  unfold phiBkt
  field_simp

theorem targetPropPhiBktVal : TargetPropPhiBktVal := by
  intro T U0 w hT hU0 hw
  have hK := bkt_K T U0 w hT hU0 hw
  unfold fugOfK
  rw [hK]
  have hexp : -(Real.pi ^ 2 * (2 / Real.pi) / 2) = -Real.pi := by
    field_simp
  rw [hexp]

theorem targetPropPhiMinEq : TargetPropPhiMinEq := by
  intro T U0 w yc hT hU0 hw hyc hyc2
  have hπ : (0 : ℝ) < Real.pi := Real.pi_pos
  have hq : (0 : ℝ) < 2 * Real.pi / yc := div_pos (by positivity) hyc
  have hK : U0 * w * phiMin T U0 w yc / T = (2 / Real.pi ^ 2) * Real.log (2 * Real.pi / yc) := by
    unfold phiMin
    field_simp
  unfold fugOfK
  rw [hK]
  have hexp : -(Real.pi ^ 2 * ((2 / Real.pi ^ 2) * Real.log (2 * Real.pi / yc)) / 2)
      = -(Real.log (2 * Real.pi / yc)) := by
    field_simp
  rw [hexp]
  have hinv : Real.exp (-(Real.log (2 * Real.pi / yc))) = (2 * Real.pi / yc)⁻¹ := by
    rw [← Real.log_inv]
    exact Real.exp_log (inv_pos.mpr hq)
  rw [hinv]
  have hq2 : 2 * Real.pi * (2 * Real.pi / yc)⁻¹ = yc := by
    field_simp
  exact hq2

theorem targetPropPhiConflict : TargetPropPhiConflict := by
  intro b hb hbpi
  have hπ : (0 : ℝ) < Real.pi := Real.pi_pos
  have habs : 2 / Real.pi < 1 / b := by
    rw [div_lt_div_iff₀ hπ hb]
    linarith [hbpi]
  have hπ2 : (0 : ℝ) < Real.pi ^ 2 := pow_pos hπ 2
  have hmul : Real.pi ^ 2 * (2 / Real.pi) < Real.pi ^ 2 * (1 / b) :=
    mul_lt_mul_of_pos_left habs hπ2
  have hE : -(Real.pi ^ 2 * (1 / b) / 2) < -(Real.pi ^ 2 * (2 / Real.pi) / 2) := by
    have h1 : Real.pi ^ 2 * (2 / Real.pi) / 2 < Real.pi ^ 2 * (1 / b) / 2 := by linarith [hmul]
    linarith [h1]
  unfold fugOfK
  exact mul_lt_mul_of_pos_left (Real.exp_lt_exp.mpr hE) (by positivity)

end

end CQM.Ring15.LockPhi
