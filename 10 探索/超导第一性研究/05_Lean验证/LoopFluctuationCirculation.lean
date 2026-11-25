import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp

/-!
# 环 4 → 环 5 → 环 8: 零点涨落环量 Φ_C 与闭环乘积的代数核

Workbench file. 不改主链、不改缺口状态、不动账面。

Chain inputs:
  Ring 4 (4.1):  eps_e = eps_e^(0) + Δeps_e,  Δeps 零均值、方差 σ²
  Ring 5 (5.2):  r_e = sqrt(1 - eps_e/(2π)),  λ_e = ln r_e
  Ring 9 (9.1):  Cov(Δeps_i, Δeps_j) = σ² ρ_ij

本文件形式化四组**纯代数**事实（无 axiom/sorry/admit/native_decide/unsafe）：

  1. 望远镜：可收缩闭环上梯度分量的和恒为零 ⇒ 环量只由余确切分量承担；
  2. 等关联方差：V(n) = nσ² + n(n−1)ρσ²，含递推、两端极限与上下界；
  3. 反演配对：½[ln(1−x)+ln(1+x)] = ½ln(1−x²) ≤ 0
     ⇒ 逐边把几何平均向下压（对数周长律的符号与恒等式）；
  4. 两点对称的均值与相位：e^{±x/(4π)} 的平均 ≥ 1；相干因子 ≤ 1。

未形式化（数值/解析在 Python 与推导卡）：
  * ⟨ln∏r⟩ = −nσ²/(16π²) + O(σ⁴) 的**速率**（需高斯期望，超出纯代数）；
  * 关联函数 ρ_ij 的第一性形状（`W-3′` 未闭合）；
  * 逐边亏角的具体取值（`审-18`，读数层）。
-/

namespace CQM.LoopFluctuation

open Finset
open scoped BigOperators

/-! ## 一、望远镜与余确切分量 -/

/-- 望远镜恒等式：沿开链求和 `Σ_{i<n}(a_i − a_{i+1}) = a_0 − a_n`。 -/
theorem telescope (a : ℕ → ℝ) (n : ℕ) :
    (range n).sum (fun i => a i - a (i + 1)) = a 0 - a n := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [Finset.sum_range_succ, ih]
      ring_nf

/-- 可收缩闭环（`a_n = a_0`）上，梯度分量（确切 1-形式）的和恒为零。
这就是第 76 轮"望远镜恒等式"的代数内容：确切分量不产生环流。 -/
theorem loop_exact_zero (a : ℕ → ℝ) (n : ℕ) (h : a n = a 0) :
    (range n).sum (fun i => a i - a (i + 1)) = 0 := by
  rw [telescope, h]
  ring_nf

/-- 若边涨落分解为 `Δeps_e = (a_i − a_{i+1}) + h_e`（确切 + 余确切），
则闭环环量 `Σ_e Δeps_e` 只由 `h` 承担——梯度部分逐个样本抵消，不是统计抵消。 -/
theorem loop_coexact_only (a h : ℕ → ℝ) (n : ℕ) (hn : a n = a 0) :
    (range n).sum (fun i => ((a i - a (i + 1)) + h i)) = (range n).sum h := by
  rw [Finset.sum_add_distrib, loop_exact_zero a n hn, zero_add]

/-! ## 二、等关联方差 `V(n) = nσ² + n(n−1)ρσ²` -/

/-- 等关联涨落的闭环环量方差（矩阵求和 `Σ_{i,j}Cov` 的代数值）。 -/
noncomputable def V (n : ℕ) (rho s2 : ℝ) : ℝ :=
  (n : ℝ) * s2 + (n : ℝ) * ((n : ℝ) - 1) * rho * s2

/-- 零条边：方差为零。 -/
theorem V_zero (rho s2 : ℝ) : V 0 rho s2 = 0 := by
  unfold V
  norm_num

/-- 一条边：方差退回单边方差。 -/
theorem V_one (rho s2 : ℝ) : V 1 rho s2 = s2 := by
  unfold V
  norm_num

/-- 递推：加一条边，方差增加 `σ² + 2nρσ²`（自身方差 + 与已有 n 条边的两倍协方差）。 -/
theorem V_succ (n : ℕ) (rho s2 : ℝ) :
    V (n + 1) rho s2 = V n rho s2 + s2 + 2 * (n : ℝ) * rho * s2 := by
  unfold V
  push_cast
  ring_nf

/-- 不关联极限：`V(n) = nσ²`（周长律，√n 增长）。 -/
theorem V_no_corr (n : ℕ) (s2 : ℝ) : V n 0 s2 = (n : ℝ) * s2 := by
  unfold V
  ring_nf

/-- 全关联极限：`V(n) = n²σ²`（线性增长）。 -/
theorem V_full (n : ℕ) (s2 : ℝ) : V n 1 s2 = (n : ℝ) ^ 2 * s2 := by
  unfold V
  ring_nf

/-- 方差关于关联系数单调不减。 -/
theorem V_mono_rho (n : ℕ) (hn : 1 ≤ n) {rho1 rho2 s2 : ℝ}
    (hr : rho1 ≤ rho2) (hs : 0 ≤ s2) :
    V n rho1 s2 ≤ V n rho2 s2 := by
  unfold V
  have hn0 : (0 : ℝ) ≤ (n : ℝ) := Nat.cast_nonneg n
  have hn1 : (0 : ℝ) ≤ (n : ℝ) - 1 := by
    have h : (1 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
    linarith
  have hcoef : (0 : ℝ) ≤ (n : ℝ) * ((n : ℝ) - 1) * s2 :=
    mul_nonneg (mul_nonneg hn0 hn1) hs
  nlinarith [mul_nonneg hcoef (sub_nonneg.mpr hr)]

/-- 上下界：`nσ² ≤ Var(Φ_C) ≤ n²σ²`（`0 ≤ ρ ≤ 1`）。
下界把"涨落永不小于独立情形"钉成代数结论。 -/
theorem V_bounds (n : ℕ) {rho s2 : ℝ} (hr0 : 0 ≤ rho) (hr1 : rho ≤ 1)
    (hs : 0 ≤ s2) :
    (n : ℝ) * s2 ≤ V n rho s2 ∧ V n rho s2 ≤ (n : ℝ) ^ 2 * s2 := by
  rcases Nat.eq_zero_or_pos n with hn | hn
  · subst hn
    constructor <;> simp [V]
  · have hn1 : 1 ≤ n := hn
    constructor
    · rw [← V_no_corr n s2]
      exact V_mono_rho n hn1 hr0 hs
    · rw [← V_full n s2]
      exact V_mono_rho n hn1 hr1 hs

/-! ## 三、反演配对：几何平均被逐边压低 -/

/-- 配对恒等式：`½[ln(1−x)+ln(1+x)] = ½ln(1−x²)`（`|x|<1`）。
左边是 `Δeps` 与 `−Δeps` 两个对称实现的 `ln∏r` 平均。 -/
theorem antithetic_pair (x : ℝ) (hx : x ^ 2 < 1) :
    (Real.log (1 - x) + Real.log (1 + x)) / 2 = Real.log (1 - x ^ 2) / 2 := by
  have hx1 : x < 1 := by nlinarith [sq_nonneg x]
  have hx2 : -1 < x := by nlinarith [sq_nonneg x]
  have h1 : (1 : ℝ) - x ≠ 0 := by intro h; linarith
  have h2 : (1 : ℝ) + x ≠ 0 := by intro h; linarith
  rw [← Real.log_mul h1 h2]
  congr 1
  ring_nf

/-- 配对平均非正：`ln(1−x²) ≤ 0`（`|x|<1`）。
故二阶项 `−ΣΔeps²/(16π²)` 不抵消——涨落总把典型闭环乘积向下压。 -/
theorem antithetic_nonpos (x : ℝ) (hx : x ^ 2 < 1) :
    Real.log (1 - x ^ 2) ≤ 0 := by
  have hpos : (0 : ℝ) < 1 - x ^ 2 := by nlinarith [sq_nonneg x]
  have hle : 1 - x ^ 2 ≤ 1 := by nlinarith [sq_nonneg x]
  have hlog := Real.log_le_log hpos hle
  simpa using hlog

/-! ## 四、两点对称的均值与相位 -/

/-- 对称两点涨落 `±x` 下，闭环乘积 `e^{−Φ/(4π)}` 的平均 `= cosh(x/4π) ≥ 1`。
这里不引入 `cosh`，直接用 `e^t ≥ 1+t` 的两侧相加给出下界。 -/
theorem mean_product_ge_one (x : ℝ) :
    1 ≤ (Real.exp (-(x / (4 * Real.pi))) + Real.exp (x / (4 * Real.pi))) / 2 := by
  have h1 := Real.add_one_le_exp (x / (4 * Real.pi))
  have h2 := Real.add_one_le_exp (-(x / (4 * Real.pi)))
  linarith

/-- 相干因子：两点对称平均的实部 `cos(sx) ≤ 1`。 -/
theorem phase_le_one (x s : ℝ) : Real.cos (s * x) ≤ 1 :=
  Real.cos_le_one (s * x)

/-- 相干相位随方差指数衰减且始终 `≤ 1`：`e^{−s²Var/2} ≤ 1`。 -/
theorem phase_decay_le_one {s2 v : ℝ} (hs : 0 ≤ s2) (hv : 0 ≤ v) :
    Real.exp (-(s2 * v)) ≤ 1 := by
  calc Real.exp (-(s2 * v)) ≤ Real.exp 0 := by
        apply Real.exp_le_exp.mpr
        nlinarith
    _ = 1 := Real.exp_zero

end CQM.LoopFluctuation
