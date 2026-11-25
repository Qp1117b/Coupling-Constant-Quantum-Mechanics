-- 环 15 / 审-6 第五段（第 176 轮）：共点两键相位差的相关系数 ρ = -1/2
-- 只 import Ring15Spec；算术核，无统计假设被藏进 tactic。
import Ring15Spec

namespace CQM.Ring15.LockCorr

open CQM.Ring15.Spec

theorem targetPropAdjCorr : TargetPropAdjCorr := by
  intro v hv
  have h2v : (0 : ℝ) < 2 * v := by linarith
  have hsq : (2 * v) * (2 * v) = (2 * v) ^ 2 := by ring
  have hsqrt : Real.sqrt ((2 * v) * (2 * v)) = 2 * v := by
    rw [hsq]
    exact Real.sqrt_sq h2v.le
  rw [hsqrt]
  -- 目标化为 (-v)/(2v) = -1/2；v>0 保证分母非零，field_simp 归一后即闭合
  field_simp

end CQM.Ring15.LockCorr
