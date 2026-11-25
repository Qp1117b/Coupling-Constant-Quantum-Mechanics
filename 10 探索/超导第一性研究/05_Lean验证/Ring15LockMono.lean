-- 环 15 / 审-6 第四段（第 175 轮）：方向性——刚度↑ ⇒ 逸度↓ ⇒ 同步概率↑
-- 只 import Ring15Spec；不引新公设，不用 nlinarith 跳步。
-- 注意：第三条（组合）**故意不写**——它需要 $y\le1$ 的值域，而该值域来自外部前因子归一（DISCARD 161），
-- 链内不可得。用两条带显式侧条件的定理替代，避免把外部条件藏进假设。
import Ring15Spec

namespace CQM.Ring15.LockMono

open CQM.Ring15.Spec

/-- 逸度关于核心能单调不增（$T>0$）。 -/
theorem targetPropFugMono : TargetPropFugMono := by
  intro Ec1 Ec2 T hT hle
  have hneg : -Ec2 ≤ -Ec1 := neg_le_neg hle
  have hdiv : -Ec2 / T ≤ -Ec1 / T := div_le_div_of_nonneg_right hneg hT.le
  have hexp : Real.exp (-Ec2 / T) ≤ Real.exp (-Ec1 / T) := Real.exp_le_exp.mpr hdiv
  have hpos : (0 : ℝ) ≤ 2 * Real.pi := by positivity
  exact mul_le_mul_of_nonneg_left hexp hpos

/-- 同步概率关于逸度单调不增（$m$ 条键同时锁定，$0\le y\le 1$）。 -/
theorem targetPropSyncMono : TargetPropSyncMono := by
  intro ppair y1 y2 m hpp hy1 h12 hy2
  have h2 : 0 ≤ 1 - y2 := by linarith
  have hle : 1 - y2 ≤ 1 - y1 := by linarith
  have hp : (1 - y2) ^ m ≤ (1 - y1) ^ m := pow_le_pow_left₀ h2 hle m
  exact mul_le_mul_of_nonneg_left hp hpp

end CQM.Ring15.LockMono
