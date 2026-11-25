/-
SyncLockBridge.lean —— 第 149 轮：R-158
审-6 的锁定因子桥、t 的定义式与上界、n_cell 的二键界

承载以下严格结果：
  1. (R158.1) 同步 = 配对 × 锁定：0 ≤ y ≤ 1、0 ≤ p ⇒ 0 ≤ p(1-y) ≤ p；
  2. (R158.4) 指数恒等式：p^(1 + log(1-y)/log p) = p(1-y)；
  3. (R158.4) 零温极限：t_eff(p,0) = 1；
  4. (R158.4) t_eff > 1（0<p<1、0<y<1）；
  5. (R158.4) t_eff 随 y 单调不减；
  6. (R158.7) 阈值抬升：p_c ≤ p_c/(1-y)；
  7. (R158.7) 阈值恒等式：(p_c/(1-y))^(t_eff (p_c/(1-y)) y) = p_c；
  8. (R158.9) 二键格胞 n_cell = 2/(1+rho^2) ∈ [1,2]（|rho| ≤ 1）。

本文件只承载代数、符号与单调性结构；不证明涡旋逸度的第一性形式，
不给 E_c、p_c、y 的材料值。
无 axiom / sorry / admit / native_decide / unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp

set_option linter.unusedVariables false

namespace CQM.SyncLockBridge

noncomputable section

/-! ### 一、事件分解：同步 = 配对 × 锁定 (R158.1) -/

/-- 同步比例的边事件分解：$p_{\rm sync}=p_{\rm pair}(1-y)$，$y$ 为失锁（涡旋）概率。 -/
def pSync (p y : ℝ) : ℝ := p * (1 - y)

/-- 非负性。 -/
theorem sync_nonneg {p y : ℝ} (hp : 0 ≤ p) (hy : y ≤ 1) : 0 ≤ pSync p y := by
  unfold pSync
  exact mul_nonneg hp (by linarith)

/-- 二阶段上界：同步比例不超过配对比例。 -/
theorem sync_le_pair {p y : ℝ} (hp : 0 ≤ p) (hy : 0 ≤ y) : pSync p y ≤ p := by
  unfold pSync
  calc p * (1 - y) ≤ p * 1 := mul_le_mul_of_nonneg_left (by linarith) hp
    _ = p := by ring

/-- 概率上界：p ≤ 1 时同步比例仍 ≤ 1。 -/
theorem sync_le_one {p y : ℝ} (hp : 0 ≤ p) (hp1 : p ≤ 1) (hy : 0 ≤ y) : pSync p y ≤ 1 := by
  calc pSync p y ≤ p := sync_le_pair hp hy
    _ ≤ 1 := hp1

/-! ### 二、有效指数的定义式 (R158.4) -/

/-- (15L.4) 有效指数 $t=1+\ln(1-y)/\ln p$。 -/
def tEff (p y : ℝ) : ℝ := 1 + Real.log (1 - y) / Real.log p

/-- 指数恒等式：$p^{t_{\rm eff}}=p(1-y)$。 -/
theorem exponent_identity {p y : ℝ} (hp : 0 < p) (hp1 : p ≠ 1) (hy : 0 < 1 - y) :
    p ^ (1 + Real.log (1 - y) / Real.log p) = p * (1 - y) := by
  have hlog : Real.log p ≠ 0 := by
    intro h
    rcases (Real.log_eq_zero.mp h) with h0 | h1 | h1
    · linarith
    · exact hp1 h1
    · linarith
  rw [Real.rpow_add hp, Real.rpow_one]
  have h2 : p ^ (Real.log (1 - y) / Real.log p) = 1 - y := by
    rw [Real.rpow_def_of_pos hp]
    have hmul : Real.log p * (Real.log (1 - y) / Real.log p) = Real.log (1 - y) := by
      field_simp [hlog]
    rw [hmul, Real.exp_log hy]
  rw [h2]

/-- 零温极限：$y=0$ 时 $t_{\rm eff}=1$。 -/
theorem tEff_zero (p : ℝ) : tEff p 0 = 1 := by
  unfold tEff
  norm_num

/-- 有限温严格大于 1。 -/
theorem tEff_gt_one {p y : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hy0 : 0 < y) (hy1 : y < 1) :
    1 < tEff p y := by
  unfold tEff
  have hlogp : Real.log p < 0 := Real.log_neg hp0 hp1
  have hlog1 : Real.log (1 - y) < 0 := Real.log_neg (by linarith) (by linarith)
  have hratio : 0 < Real.log (1 - y) / Real.log p := div_pos_of_neg_of_neg hlog1 hlogp
  linarith

/-- 单调性：$y$ 越大，$t_{\rm eff}$ 越大。 -/
theorem tEff_mono {p y1 y2 : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (h12 : y1 ≤ y2)
    (hpos : 0 < 1 - y2) : tEff p y1 ≤ tEff p y2 := by
  have hpos1 : 0 < 1 - y1 := by linarith
  have hle : Real.log (1 - y2) ≤ Real.log (1 - y1) :=
    Real.log_le_log hpos (by linarith)
  have hA : -Real.log (1 - y1) ≤ -Real.log (1 - y2) := by linarith
  have hB : 0 < -Real.log p := by
    have := Real.log_neg hp0 hp1
    linarith
  have hratio : (-Real.log (1 - y1)) / (-Real.log p) ≤ (-Real.log (1 - y2)) / (-Real.log p) :=
    (div_le_div_iff_of_pos_right hB).mpr hA
  have e1 : tEff p y1 = 1 + (-Real.log (1 - y1)) / (-Real.log p) := by
    unfold tEff
    rw [neg_div_neg_eq]
  have e2 : tEff p y2 = 1 + (-Real.log (1 - y2)) / (-Real.log p) := by
    unfold tEff
    rw [neg_div_neg_eq]
  rw [e1, e2]
  linarith

/-! ### 三、阈值关系 (R158.7) -/

/-- 配对比例必须先超过 $p_c$。 -/
theorem pair_threshold_ge {pc y : ℝ} (hpc : 0 < pc) (hy0 : 0 ≤ y) (hy1 : y < 1) :
    pc ≤ pc / (1 - y) := by
  have h1 : 0 < 1 - y := by linarith
  rw [le_div_iff₀ h1]
  nlinarith

/-- 阈值恒等式：$(p_c/(1-y))^{t}=p_c$，其中 $t$ 在阈值点取值。 -/
theorem threshold_identity {pc y : ℝ} (hpc : 0 < pc) (hpc1 : pc < 1)
    (hy0 : 0 < y) (hyc : y < 1 - pc) :
    (pc / (1 - y)) ^ tEff (pc / (1 - y)) y = pc := by
  have hy1 : y < 1 := by linarith
  have h1 : 0 < 1 - y := by linarith
  have hp : 0 < pc / (1 - y) := div_pos hpc h1
  have hp1 : pc / (1 - y) ≠ 1 := by
    intro h
    rw [div_eq_one_iff_eq (ne_of_gt h1)] at h
    linarith
  have h := exponent_identity (p := pc / (1 - y)) (y := y) hp hp1 h1
  have hval : pc / (1 - y) * (1 - y) = pc := by field_simp
  unfold tEff
  rw [h, hval]

/-! ### 四、$n_{\rm cell}$ 的二键界 (R158.9) -/

/-- 二键格胞的有效自由度 $n_{\rm cell}=2/(1+\rho^2)$。 -/
def neff2 (ρ : ℝ) : ℝ := 2 / (1 + ρ ^ 2)

/-- 下界：$|\rho|\le1$ ⇒ $n_{\rm cell}\ge1$。 -/
theorem neff2_ge_one (ρ : ℝ) (h : ρ ^ 2 ≤ 1) : 1 ≤ neff2 ρ := by
  unfold neff2
  have hpos : 0 < 1 + ρ ^ 2 := by positivity
  rw [le_div_iff₀ hpos]
  nlinarith

/-- 上界：$n_{\rm cell}\le z=2$。 -/
theorem neff2_le_two (ρ : ℝ) (h : ρ ^ 2 ≤ 1) : neff2 ρ ≤ 2 := by
  unfold neff2
  have hpos : 0 < 1 + ρ ^ 2 := by positivity
  rw [div_le_iff₀ hpos]
  nlinarith

end

end CQM.SyncLockBridge
