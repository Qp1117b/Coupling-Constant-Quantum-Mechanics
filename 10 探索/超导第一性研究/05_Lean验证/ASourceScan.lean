/-
ASourceScan.lean —— 第 148 轮：R-157
A 源静态 no-go、扫描奇偶性与可解域统一判据

承载以下严格结果：
  1. (R157.1) 静态分量无率：常数的导数恒为零；
  2. (R157.5/6) 扫描奇偶：s 的自洽式在 (g,mu) → (-g,-mu) 下不变；
  3. (R157.9) 统一材料形式：g*r = -2mu 时
     2g/[C(2mu+g*aLam)] = 2/[C(aLam-r)]，升降温同式；
  4. (R157.10) 可解判据：s>0 ↔ r < aLam，升降温同判据；
  5. (R157.11) 降温 mu<0、升温 mu>0 的符号锁定，以及物理象限 (g>0,mu>0) 为空；
  6. (R157.13) 低温极限：mu=0 时 s=2/(C*aLam)；
  7. r ∝ T^2 的严格单调、T→0 趋零、边界下方可解、T_x 的平方形式；
  8. 降温 A=2mu*s^2<0（收缩），mu=0 时 A=0。

本文件只承载代数、符号与单调性结构；不证明 Debye 积分，不给 alpha_V、eps、a 的材料值。
无 axiom / sorry / admit / native_decide / unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Topology.Basic
import Mathlib.Topology.Order.Basic
import Mathlib.Order.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp

open scoped BigOperators

set_option linter.unusedVariables false

namespace CQM.ASourceScan

/-! ### 一、静态分量无率：A 是导数，不是方差 (R157.1) -/

/-- 常数的导数恒为零：冻结缺陷、零点方差 Z、预存密度 n_d^(0) 对 A=2Cov(l,l') 的贡献为零。 -/
theorem static_component_no_rate (c t : ℝ) :
    HasDerivAt (fun _ : ℝ => c) 0 t :=
  hasDerivAt_const t c

/-- 等价的 deriv 形式。 -/
theorem deriv_const_zero (c t : ℝ) :
    deriv (fun _ : ℝ => c) t = 0 :=
  deriv_const t c

/-! ### 二、扫描符号锁定与物理象限 (R157.5) -/

/-- 降温（Tdot<0）：g = eps*(w'*Tdot)/w > 0。 -/
theorem cooling_g_pos {eps w w' Tdot : ℝ}
    (heps : 0 < eps) (hw : 0 < w) (hw' : w' < 0) (hT : Tdot < 0) :
    0 < eps * (w' * Tdot) / w := by
  have hnum : 0 < w' * Tdot := mul_pos_of_neg_of_neg hw' hT
  exact div_pos (mul_pos heps hnum) hw

/-- 降温：mu = alpha*Tdot/3 < 0。 -/
theorem cooling_mu_neg {alpha Tdot : ℝ}
    (ha : 0 < alpha) (hT : Tdot < 0) :
    alpha * Tdot / 3 < 0 := by
  have : alpha * Tdot < 0 := mul_neg_of_pos_of_neg ha hT
  linarith

/-- 升温（Tdot>0）：g = eps*(w'*Tdot)/w < 0。 -/
theorem heating_g_neg {eps w w' Tdot : ℝ}
    (heps : 0 < eps) (hw : 0 < w) (hw' : w' < 0) (hT : 0 < Tdot) :
    eps * (w' * Tdot) / w < 0 := by
  have hnum : w' * Tdot < 0 := mul_neg_of_neg_of_pos hw' hT
  exact div_neg_of_neg_of_pos (mul_neg_of_pos_of_neg heps hnum) hw

/-- 升温：mu = alpha*Tdot/3 > 0。 -/
theorem heating_mu_pos {alpha Tdot : ℝ}
    (ha : 0 < alpha) (hT : 0 < Tdot) :
    0 < alpha * Tdot / 3 := by
  have : 0 < alpha * Tdot := mul_pos ha hT
  linarith

/-- 单一 Tdot 下 g 与 mu 异号：物理降温 (g>0,mu<0)、升温 (g<0,mu>0)。 -/
theorem g_mu_opposite {eps w w' alpha Tdot : ℝ}
    (heps : 0 < eps) (hw : 0 < w) (hw' : w' < 0) (ha : 0 < alpha)
    (hT : Tdot ≠ 0) :
    (eps * (w' * Tdot) / w) * (alpha * Tdot / 3) < 0 := by
  have hT2 : 0 < Tdot * Tdot := mul_self_pos.mpr hT
  have hcoef : eps * alpha * w' / (3 * w) < 0 := by
    have hnum : eps * alpha * w' < 0 :=
      mul_neg_of_pos_of_neg (mul_pos heps ha) hw'
    exact div_neg_of_neg_of_pos hnum (by positivity)
  have hEq : (eps * (w' * Tdot) / w) * (alpha * Tdot / 3)
      = (eps * alpha * w' / (3 * w)) * (Tdot * Tdot) := by
    field_simp
  rw [hEq]
  exact mul_neg_of_neg_of_pos hcoef hT2

/-- R-155 的 (g>0,mu>0) 象限在单一 Tdot 下为空，故「降温恒可解」不成立。 -/
theorem physical_quadrant_not_both_pos {eps w w' alpha Tdot : ℝ}
    (heps : 0 < eps) (hw : 0 < w) (hw' : w' < 0) (ha : 0 < alpha)
    (hT : Tdot ≠ 0) :
    ¬ (0 < eps * (w' * Tdot) / w ∧ 0 < alpha * Tdot / 3) := by
  rintro ⟨hg, hmu⟩
  have hneg := g_mu_opposite heps hw hw' ha hT
  nlinarith

/-! ### 三、扫描奇偶与统一材料形式 (R157.6–R157.9) -/

/-- 扫描反向 (g,mu) → (-g,-mu) 时自洽式不变。 -/
theorem s_scan_parity (g mu C aLam : ℝ) :
    2 * (-g) / (C * (2 * (-mu) + (-g) * aLam))
      = 2 * g / (C * (2 * mu + g * aLam)) := by
  have hden : C * (2 * (-mu) + (-g) * aLam) = -(C * (2 * mu + g * aLam)) := by ring
  have hnum : 2 * (-g) = -(2 * g) := by ring
  rw [hden, hnum, div_neg, neg_div, neg_neg]

/-- 统一材料形式：g*r = -2mu 时，s = 2/[C(aLam-r)]，升降温度同式。 -/
theorem s_material_form {g mu C aLam r : ℝ}
    (hg : g ≠ 0) (hr : g * r = -2 * mu)
    (hden : C * (aLam - r) ≠ 0) :
    2 * g / (C * (2 * mu + g * aLam)) = 2 / (C * (aLam - r)) := by
  have hC : C ≠ 0 := by
    intro hC0
    exact hden (by rw [hC0, zero_mul])
  have hden1 : C * (2 * mu + g * aLam) ≠ 0 := by
    intro h
    have h2 : 2 * mu + g * aLam = 0 := (mul_eq_zero.mp h).resolve_left hC
    have hgr : g * (aLam - r) = 0 := by nlinarith
    have hz : aLam - r = 0 := (mul_eq_zero.mp hgr).resolve_left hg
    exact hden (by rw [hz, mul_zero])
  rw [div_eq_div_iff hden1 hden]
  have hgr : g * (aLam - r) = 2 * mu + g * aLam := by nlinarith
  calc
    (2 * g) * (C * (aLam - r)) = 2 * C * (g * (aLam - r)) := by ring
    _ = 2 * C * (2 * mu + g * aLam) := by rw [hgr]
    _ = 2 * (C * (2 * mu + g * aLam)) := by ring

/-- 可解判据的统一形式：s>0 ↔ r < aLam，升降温同判据。 -/
theorem solvable_iff_of_material {g mu C aLam r : ℝ}
    (hg : g ≠ 0) (hC : 0 < C) (hr : g * r = -2 * mu)
    (hden : C * (aLam - r) ≠ 0) :
    0 < 2 * g / (C * (2 * mu + g * aLam)) ↔ r < aLam := by
  rw [s_material_form hg hr hden, div_pos_iff]
  constructor
  · rintro (⟨_, hb⟩ | ⟨hneg, _⟩)
    · have h2 : 0 < aLam - r := by
        rcases mul_pos_iff.mp hb with ⟨_, h⟩ | ⟨hnegC, _⟩
        · exact h
        · exact absurd hnegC (not_lt_of_gt hC)
      linarith
    · exact absurd hneg (by norm_num : ¬ (2 : ℝ) < 0)
  · intro h
    exact Or.inl ⟨by norm_num, mul_pos hC (by linarith)⟩

/-- 降温支（g>0, mu<0）：r = -2mu/g ⇒ s>0 ↔ r<aLam。 -/
theorem solvable_iff_cooling {g mu C aLam r : ℝ}
    (hg : 0 < g) (hmu : mu < 0) (hC : 0 < C) (hr : r = -2 * mu / g)
    (hden : C * (aLam - r) ≠ 0) :
    0 < 2 * g / (C * (2 * mu + g * aLam)) ↔ r < aLam := by
  have hgne : g ≠ 0 := ne_of_gt hg
  have hr' : g * r = -2 * mu := by
    rw [hr]; field_simp [hgne]
  exact solvable_iff_of_material hgne hC hr' hden

/-- 升温支（g<0, mu>0）：r = 2mu/(-g) ⇒ s>0 ↔ r<aLam，与降温同判据。 -/
theorem solvable_iff_heating {g mu C aLam r : ℝ}
    (hg : g < 0) (hmu : 0 < mu) (hC : 0 < C) (hr : r = 2 * mu / (-g))
    (hden : C * (aLam - r) ≠ 0) :
    0 < 2 * g / (C * (2 * mu + g * aLam)) ↔ r < aLam := by
  have hgne : g ≠ 0 := ne_of_lt hg
  have hr' : g * r = -2 * mu := by
    rw [hr]; field_simp [hgne]
  exact solvable_iff_of_material hgne hC hr' hden

/-! ### 四、低温极限 (R157.13) -/

/-- mu=0 时 s 的有限极限 2/(C*aLam)：A→0 不迫使 s→0 或发散。 -/
theorem lowT_limit {g C aLam : ℝ}
    (hg : g ≠ 0) (hC : C ≠ 0) (ha : aLam ≠ 0) :
    2 * g / (C * (0 + g * aLam)) = 2 / (C * aLam) := by
  field_simp [hg, hC, ha]
  ring

/-! ### 五、r ∝ T^2 的单调与边界 (R157.11–R157.12) -/

/-- r=cT^2 在 c>0、T≥0 上严格增。 -/
theorem r_low_power_mono {c T1 T2 : ℝ}
    (hc : 0 < c) (h1 : 0 ≤ T1) (h12 : T1 < T2) :
    c * T1 ^ 2 < c * T2 ^ 2 := by
  have hsq : T1 ^ 2 < T2 ^ 2 := pow_lt_pow_left₀ h12 h1 (by norm_num)
  exact mul_lt_mul_of_pos_left hsq hc

/-- r=cT^2 在 T→0 时趋零。 -/
theorem r_low_tendsto_zero (c : ℝ) :
    Filter.Tendsto (fun T : ℝ => c * T ^ 2) (nhds 0) (nhds 0) := by
  have hcont : Continuous fun T : ℝ => c * T ^ 2 :=
    continuous_const.mul (continuous_id.pow 2)
  simpa using hcont.tendsto 0

/-- 边界下方可解：T<T_x、c*T_x^2=aLam ⇒ c*T^2<aLam。 -/
theorem below_boundary_lt {c T Tx aLam : ℝ}
    (hc : 0 < c) (hT : 0 ≤ T) (hlt : T < Tx) (hTx : c * Tx ^ 2 = aLam) :
    c * T ^ 2 < aLam := by
  have hmono := r_low_power_mono hc hT hlt
  linarith

/-- T_x 的平方形式：c*(sqrt(aLam/c))^2 = aLam。 -/
theorem tx_sq {c aLam : ℝ} (hc : 0 < c) (ha : 0 < aLam) :
    c * (Real.sqrt (aLam / c)) ^ 2 = aLam := by
  rw [Real.sq_sqrt (le_of_lt (div_pos ha hc))]
  field_simp [ne_of_gt hc]

/-! ### 六、降温 A<0：收缩而非生产 -/

/-- 降温 mu<0、s^2>0 ⇒ A=2mu*s^2<0。 -/
theorem affine_A_neg_cooling {mu s2 : ℝ} (hmu : mu < 0) (hs : 0 < s2) :
    2 * mu * s2 < 0 := by
  have : 2 * mu * s2 = (2 * mu) * s2 := by ring
  rw [this]
  exact mul_neg_of_neg_of_pos (by linarith) hs

/-- mu=0（T→0 的仿射通道）⇒ A=0。 -/
theorem affine_A_zero (s2 : ℝ) : 2 * 0 * s2 = 0 := by ring

end CQM.ASourceScan
