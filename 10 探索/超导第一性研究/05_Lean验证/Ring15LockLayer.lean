-- 环 15 / 审-6 第三段（第 173 轮）：授权层的形式侧
-- 只 import Ring15Spec（Spec 只含定义、不 import 证明模块），两路径仍分离。
import Ring15Spec

namespace CQM.Ring15.LockLayer

open CQM.Ring15.Spec

/-- 无条件层 ≤ 条件层；`q = 1` 时相等。
证明不做任何命名跳跃：只用 `pow_nonneg`、`mul_le_mul`、`mul_le_mul_of_nonneg_right`，
并在 `q^m ≤ 1` 上做对 `m` 的归纳（不用任何"显然"）。 -/
theorem targetPropLayer : TargetPropLayer := by
  intro q y m hq0 hq1 hy0 hy1
  have hbase : 0 ≤ 1 - y := by linarith
  have hqpow : q ^ m ≤ 1 := by
    induction m with
    | zero => simp
    | succ k ih =>
        calc
          q ^ (k + 1) = q ^ k * q := by rw [pow_succ]
          _ ≤ 1 * 1 := mul_le_mul ih hq1 hq0 zero_le_one
          _ = 1 := by norm_num
  have hcond : 0 ≤ (1 - y) ^ m := pow_nonneg hbase m
  constructor
  · calc
      pLockUncond q y m = q ^ m * (1 - y) ^ m := rfl
      _ ≤ 1 * (1 - y) ^ m := mul_le_mul_of_nonneg_right hqpow hcond
      _ = pLockCond y m := by simp [pLockCond]
  · intro hq
    simp [pLockUncond, pLockCond, hq]

/-- 条件层与 v2 的 `pLock` 逐项同值（授权层的迁移不改动既有数值）。 -/
theorem cond_eq_pLock (y : ℝ) (m : ℕ) : pLockCond y m = pLock y m := rfl

end CQM.Ring15.LockLayer
