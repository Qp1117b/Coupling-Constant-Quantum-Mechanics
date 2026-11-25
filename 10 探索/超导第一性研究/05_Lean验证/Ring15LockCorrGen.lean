-- 环 15 / 审-6 第六段（第 177 轮）：带顶点相关的一般式 ρ_XY = (2ρ_v-1)/(2(1-ρ_v))
-- 只 import Ring15Spec；算术核。ρ_v 的链内取值（Bessel 核）由卡接，不进 Lean 陈述。
import Ring15Spec

namespace CQM.Ring15.LockCorrGen

open CQM.Ring15.Spec

theorem targetPropAdjCorrGen : TargetPropAdjCorrGen := by
  intro rv v hv hrv
  have h1 : (0 : ℝ) < 1 - rv := by linarith
  have hpos : (0 : ℝ) < 2 * v * (1 - rv) := by
    have : (0 : ℝ) < 2 * v := by linarith
    exact mul_pos this h1
  have hs : Real.sqrt ((2 * v * (1 - rv)) * (2 * v * (1 - rv))) = 2 * v * (1 - rv) := by
    rw [show (2 * v * (1 - rv)) * (2 * v * (1 - rv)) = (2 * v * (1 - rv)) ^ 2 by ring]
    exact Real.sqrt_sq hpos.le
  unfold adjCorrGen
  rw [hs]
  field_simp

end CQM.Ring15.LockCorrGen
