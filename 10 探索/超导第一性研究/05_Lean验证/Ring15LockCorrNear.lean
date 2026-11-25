-- 环 15 / 审-6 第六段（第 177 轮）：补入距离 2 相关的完整式
-- ρ_XY = (2ρ₁ - 1 - ρ₂)/(2(1-ρ₁))；只 import Ring15Spec，算术核。
import Ring15Spec

namespace CQM.Ring15.LockCorrNear

open CQM.Ring15.Spec

theorem targetPropAdjCorrNear : TargetPropAdjCorrNear := by
  intro r1 r2 v hv hr1
  have h1 : (0 : ℝ) < 1 - r1 := by linarith
  have hpos : (0 : ℝ) < 2 * v * (1 - r1) := by
    have : (0 : ℝ) < 2 * v := by linarith
    exact mul_pos this h1
  have hs : Real.sqrt ((2 * v * (1 - r1)) * (2 * v * (1 - r1))) = 2 * v * (1 - r1) := by
    rw [show (2 * v * (1 - r1)) * (2 * v * (1 - r1)) = (2 * v * (1 - r1)) ^ 2 by ring]
    exact Real.sqrt_sq hpos.le
  unfold adjCorrNear
  rw [hs]
  field_simp

end CQM.Ring15.LockCorrNear
