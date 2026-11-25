-- 环 15 / 审-6 第七段（第 178 轮）：ρ_XY 的尺度不变性（与共同振幅 v 无关）
-- 只 import Ring15Spec；算术核，不引任何统计假设。
import Ring15Spec

namespace CQM.Ring15.LockScale

open CQM.Ring15.Spec

private theorem near_val (r1 r2 v : ℝ) (hv : 0 < v) (h1 : r1 < 1) :
    adjCorrNear r1 r2 v = (2 * r1 - 1 - r2) / (2 * (1 - r1)) := by
  have hpos1 : (0 : ℝ) < 1 - r1 := by linarith
  have hpos : (0 : ℝ) < 2 * v * (1 - r1) := by
    have : (0 : ℝ) < 2 * v := by linarith
    exact mul_pos this hpos1
  have hs : Real.sqrt ((2 * v * (1 - r1)) * (2 * v * (1 - r1))) = 2 * v * (1 - r1) := by
    rw [show (2 * v * (1 - r1)) * (2 * v * (1 - r1)) = (2 * v * (1 - r1)) ^ 2 by ring]
    exact Real.sqrt_sq hpos.le
  unfold adjCorrNear
  rw [hs]
  field_simp

theorem targetPropAdjCorrScale : TargetPropAdjCorrScale := by
  intro r1 r2 v hv h1
  rw [near_val r1 r2 v hv h1, near_val r1 r2 1 one_pos h1]

end CQM.Ring15.LockScale
