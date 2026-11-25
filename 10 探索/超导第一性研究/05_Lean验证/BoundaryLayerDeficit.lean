import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp

/-!
# 环 8 / `审-18`: 三环乘积 0.177/0.707/0.500 的边界分层口径

Workbench file. 不改主链、不改缺口状态、不动账面。

Chain inputs:
  Ring 5 (5.2):  r eps = sqrt(1 - eps/(2*pi))
  06 §0.3 环节④ / §944:  BCC 三角最小环 prod_C r = 0.177/0.707/0.500

数值事实（`04_计算验证/环08_三环乘积口径复现.py` 逐行复现 06 的
`cqm_analysis/ring_1d_flow.py`）：
  * 按"边中点是否落在凸包面上"分层后，**体内边** eps ≈ 0（最大 3.6e-13，
    且与 jitter 无关），**边界边** eps 取 O(1) 离散值；
  * 规则菱形四面体二面角为 90°，沿边共享 k 个角度时
        eps = 2*pi - k*(pi/2) = (4-k)*(pi/2),
        k=4（体）→ 0,  k=3（面）→ pi/2,  k=2（棱）→ pi,  k=1（角）→ 3*pi/2；
  * 于是 r 取 {1, sqrt3/2, 1/sqrt2, 1/2}，三值 0.177/0.707/0.500 恰由
    (棱)(角)(角) / (棱) / (角) 的边界边给出。

本文件只把这些**代数事实**形式化（纯实数代数，无 axiom/sorry/admit/
native_decide/unsafe）。三角化的组合记账与几何（哪条边在凸包面上）在
Python；"三值属读数层"的判定在推导卡与决策记录里，不作定理。
-/

namespace CQM.BoundaryLayer

open Finset

/-- 环 5 (5.2) 的键比值，作为实数函数。 -/
noncomputable def r (eps : ℝ) : ℝ := Real.sqrt (1 - eps / (2 * Real.pi))

/-- 零亏角给出单位比值（平直体内边）。 -/
theorem r_zero : r 0 = 1 := by
  unfold r
  rw [show (1 : ℝ) - 0 / (2 * Real.pi) = 1 by norm_num, Real.sqrt_one]

/-- 通式：沿边共享 `k` 个 90° 二面角时，亏角 `eps = (4-k)*(pi/2)`。 -/
theorem boundary_layer_deficit (k : ℝ) :
    2 * Real.pi - k * (Real.pi / 2) = (4 - k) * (Real.pi / 2) := by ring

/-- `k = 4`（体内，4 个 90°）给出零亏角。 -/
theorem k_four_flat : 2 * Real.pi - (4 : ℝ) * (Real.pi / 2) = 0 := by ring

/-- `k = 3`（凸包**面**上，3 个 90°）给出 `eps = pi/2`。 -/
theorem k_three_half_pi : 2 * Real.pi - (3 : ℝ) * (Real.pi / 2) = Real.pi / 2 := by ring

/-- `k = 2`（凸包**棱**上，2 个 90°）给出 `eps = pi`。 -/
theorem k_two_pi : 2 * Real.pi - (2 : ℝ) * (Real.pi / 2) = Real.pi := by ring

/-- `k = 1`（凸包**角**上，1 个 90°）给出 `eps = 3*pi/2`。 -/
theorem k_one_three_halves :
    2 * Real.pi - (1 : ℝ) * (Real.pi / 2) = 3 * Real.pi / 2 := by ring

/-- 棱边亏角 `pi` 给出 `r = 1/sqrt2`：等价地 `r*pi * r*pi = 1/2`。 -/
theorem r_pi_sq : r Real.pi * r Real.pi = 1 / 2 := by
  unfold r
  have h : 1 - Real.pi / (2 * Real.pi) = 1 / 2 := by
    field_simp
    norm_num
  rw [h, Real.mul_self_sqrt (by norm_num : (0 : ℝ) ≤ 1 / 2)]

/-- 角边亏角 `3*pi/2` 给出 `r = 1/2`。 -/
theorem r_three_halves : r (3 * Real.pi / 2) = 1 / 2 := by
  unfold r
  have h : 1 - (3 * Real.pi / 2) / (2 * Real.pi) = 1 / 4 := by
    field_simp
    ring_nf
  rw [h]
  rw [show (1 / 4 : ℝ) = (1 / 2) * (1 / 2) by norm_num]
  rw [Real.sqrt_mul_self (by norm_num : (0 : ℝ) ≤ 1 / 2)]

/-- 面边亏角 `pi/2` 给出 `r^2 = 3/4`（即 `r = sqrt3/2`）。 -/
theorem r_half_pi_sq : r (Real.pi / 2) * r (Real.pi / 2) = 3 / 4 := by
  unfold r
  have h : 1 - (Real.pi / 2) / (2 * Real.pi) = 3 / 4 := by
    field_simp
    ring_nf
  rw [h, Real.mul_self_sqrt (by norm_num : (0 : ℝ) ≤ 3 / 4)]

/-- 06 的 0.177 环：`(棱)(角)(角)` 三边乘积的平方 `= 1/32`，
即 `prod = 1/(4*sqrt2) = 0.176776…`。 -/
theorem triple_boundary_sq :
    (r Real.pi * r (3 * Real.pi / 2) * r (3 * Real.pi / 2)) ^ 2 = 1 / 32 := by
  rw [r_three_halves]
  have hp : r Real.pi * r Real.pi = 1 / 2 := r_pi_sq
  nlinarith [hp]

/-- 任意正亏角严格压低该边比值：`0 < eps ≤ 2*pi ⇒ r eps < 1`。
这条把"边界边非零亏角 ⇒ 环乘积偏离 1"钉成代数结论。 -/
theorem nonflat_edge_lowers (eps : ℝ) (h0 : 0 < eps) (h2 : eps ≤ 2 * Real.pi) :
    r eps < 1 := by
  unfold r
  have hπ : (0 : ℝ) < 2 * Real.pi := by positivity
  have hlt : 1 - eps / (2 * Real.pi) < 1 := by
    have : 0 < eps / (2 * Real.pi) := div_pos h0 hπ
    linarith
  have h1 : Real.sqrt (1 - eps / (2 * Real.pi)) < Real.sqrt 1 := by
    apply Real.sqrt_lt_sqrt
    · have : eps / (2 * Real.pi) ≤ 1 := by
        rw [div_le_one hπ]; linarith
      linarith
    · exact hlt
  simpa using h1

/-- 全平直闭环（每条边 eps = 0）的乘积为 1（任意边数）。 -/
theorem interior_loop_one (n : ℕ) :
    (range n).prod (fun _ => r 0) = 1 := by
  rw [show r 0 = (1 : ℝ) by exact r_zero]
  simp

end CQM.BoundaryLayer
