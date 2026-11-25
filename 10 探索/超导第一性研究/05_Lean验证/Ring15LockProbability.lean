-- 环 15 / 审-6 第二段：锁定概率的键级复合与指数单调（第 163 轮）
-- 独立路径：import Ring15Spec（只含定义），主定理类型即 Spec 的 TargetPropLock。
import Ring15Spec
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity

set_option autoImplicit false

open CQM.Ring15.Spec

namespace CQM.Ring15.LockProbability

/-- $m=1$：锁定概率 $=1-y$（消费上一段 `m_lock=1`）。 -/
theorem pLock_one (y : ℝ) : pLock y 1 = 1 - y := by
  simp [pLock]

/-- $m=2$：锁定概率 $=(1-y)^2$（星级读法）。 -/
theorem pLock_two (y : ℝ) : pLock y 2 = (1 - y) ^ 2 := by
  simp [pLock]

/-- $0\le y\le 1$ 时 $(1-y)^2\le 1-y$：两条键同时无涡旋不比一条容易。 -/
theorem pLock_two_le_one {y : ℝ} (hy0 : 0 ≤ y) (hy1 : y ≤ 1) :
    pLock y 2 ≤ pLock y 1 := by
  rw [pLock_two, pLock_one]
  have hnn : 0 ≤ 1 - y := by linarith
  have hle : 1 - y ≤ 1 := by linarith
  calc (1 - y) ^ 2 = (1 - y) * (1 - y) := by ring
    _ ≤ (1 - y) * 1 := mul_le_mul_of_nonneg_left hle hnn
    _ = 1 - y := by ring

/-- $0<p<1$、$0<y<1$ 时 $p^L=1-y$，$L=\ln(1-y)/\ln p$。 -/
theorem rpow_log_div {p y : ℝ} (hp : 0 < p) (hp1 : p ≠ 1) (hy : 0 < 1 - y) :
    p ^ (Real.log (1 - y) / Real.log p) = 1 - y := by
  have hlog : Real.log p ≠ 0 := by
    intro h
    rcases Real.log_eq_zero.mp h with h0 | h1 | h1
    · linarith
    · exact hp1 h1
    · linarith
  rw [Real.rpow_def_of_pos hp]
  have hmul : Real.log p * (Real.log (1 - y) / Real.log p) = Real.log (1 - y) := by
    field_simp [hlog]
  rw [hmul, Real.exp_log hy]

/-- 指数恒等式（$m=1$）：$p^{t(1)}=p(1-y)$。 -/
theorem rpow_m1 {p y : ℝ} (hp : 0 < p) (hp1 : p ≠ 1) (hy : 0 < 1 - y) :
    p ^ tEffM p y 1 = p * (1 - y) := by
  unfold tEffM
  norm_num
  rw [Real.rpow_add hp, Real.rpow_one]
  rw [rpow_log_div hp hp1 hy]

/-- 指数恒等式（$m=2$）：$p^{t(2)}=p(1-y)^2$。 -/
theorem rpow_m2 {p y : ℝ} (hp : 0 < p) (hp1 : p ≠ 1) (hy : 0 < 1 - y) :
    p ^ tEffM p y 2 = p * (1 - y) ^ 2 := by
  unfold tEffM
  norm_num
  have hL : p ^ (Real.log (1 - y) / Real.log p) = 1 - y := rpow_log_div hp hp1 hy
  have h2 : p ^ (2 * Real.log (1 - y) / Real.log p) = (1 - y) ^ 2 := by
    rw [show 2 * Real.log (1 - y) / Real.log p
        = (Real.log (1 - y) / Real.log p) * 2 by ring]
    rw [Real.rpow_mul hp.le (Real.log (1 - y) / Real.log p) 2, hL]
    norm_num
  rw [Real.rpow_add hp, Real.rpow_one, h2]

/-- $t$ 关于 $m$ 单调：星级读法给更大的粗粒化指数。 -/
theorem tEffM_mono {p y : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hy0 : 0 < y) (hy1 : y < 1) :
    tEffM p y 1 ≤ tEffM p y 2 := by
  have hl1 : Real.log (1 - y) < 0 := Real.log_neg (by linarith) (by linarith)
  have hl2 : Real.log p < 0 := Real.log_neg hp0 hp1
  have hdiff : tEffM p y 2 - tEffM p y 1 = Real.log (1 - y) / Real.log p := by
    unfold tEffM
    push_cast
    field_simp
    ring
  have hpos : 0 < Real.log (1 - y) / Real.log p := div_pos_of_neg_of_neg hl1 hl2
  linarith

/-- 本环第二段主定理：与 Spec 的 `TargetPropLock` 同一命题。 -/
theorem targetPropLock : TargetPropLock := by
  intro p y hp hp1 hy0 hy1
  have hpos : 0 < 1 - y := by linarith
  have hne : p ≠ 1 := ne_of_lt hp1
  have h1 := rpow_m1 hp hne hpos
  have h2 := rpow_m2 hp hne hpos
  have hle : p * (1 - y) ^ 2 ≤ p * (1 - y) := by
    have := pLock_two_le_one (le_of_lt hy0) (le_of_lt hy1)
    rw [pLock_two, pLock_one] at this
    exact mul_le_mul_of_nonneg_left this hp.le
  have ht := tEffM_mono hp hp1 hy0 hy1
  exact ⟨h1, h2, hle, ht⟩

end CQM.Ring15.LockProbability

#print axioms CQM.Ring15.LockProbability.targetPropLock
#print axioms CQM.Ring15.LockProbability.rpow_m2
#check @CQM.Ring15.LockProbability.targetPropLock
