/-
MeasurableFailure.lean —— 第 146 轮：R154.5 可解域符号回修 + 约掉 Tdot 的可测失效判据

承载以下严格结果：
  1. (R155.1) 可解域符号：g<0、C>0、s=2g/[C(g*aLam+2mu)] ⇒ (0<s ↔ g*aLam+2mu<0)；
  2. 等价形式 g*aLam+2mu<0 ↔ 2mu/|g| < aLam（即 aLam>r）；
  3. (R155.3) Tdot 约掉：mu=alpha*Tdot/3、|g|=eps*|dl|*Tdot ⇒ r=2alpha/(3eps|dl|)；
  4. s=2/[C(aLam-r)] 在 g<0 下的等价与 s>0 ↔ aLam>r；
  5. s 在 aLam↓r+ 时发散（任意 M 的界）；
  6. (R155.5/6) w 两支展开 w=1-k*u^2、w=c/u 的代数骨架；
  7. r 的两支单调：绝缘体 r ∝ u^2（次线性、u→0 趋零）、金属 r 常数、高温 r ∝ u。

本文件只承载代数、符号与单调性结构，不证明 Debye 积分、不给出 alpha_V 的绝对值。
无 axiom / sorry / admit / native_decide / unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Topology.Basic
import Mathlib.Order.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

open scoped BigOperators

set_option linter.unusedVariables false

namespace CQM.MeasurableFailure

/-! ### 一、可解域符号回修 (R155.1) -/

/-- g<0、C>0 时 s=2g/[C(g*aLam+2mu)] 为正 ⟺ 分母括号为负。 -/
theorem solvable_iff_den_neg (g aLam mu C s : ℝ) (hg : g < 0) (hC : 0 < C)
    (hs : s = 2 * g / (C * (g * aLam + 2 * mu))) :
    0 < s ↔ g * aLam + 2 * mu < 0 := by
  rw [hs, div_pos_iff]
  constructor
  · intro h
    rcases h with h | h
    · linarith
    · by_contra hnot
      have hge : 0 ≤ g * aLam + 2 * mu := le_of_not_gt hnot
      have hmuge : 0 ≤ C * (g * aLam + 2 * mu) := mul_nonneg (le_of_lt hC) hge
      linarith
  · intro hden
    right
    constructor
    · linarith
    · exact mul_neg_of_pos_of_neg hC hden

/-- g<0 时分母括号为负 ⟺ aLam > 2mu/|g|（即 aLam>r）。 -/
theorem den_neg_iff_alam_gt_r (g aLam mu : ℝ) (hg : g < 0) :
    g * aLam + 2 * mu < 0 ↔ 2 * mu / |g| < aLam := by
  rw [abs_of_neg hg]
  rw [div_lt_iff₀ (neg_pos.mpr hg)]
  constructor <;> intro h <;> nlinarith

/-- 降温相 g>0 时恒可解（分母与分子同号）。 -/
theorem cooling_always_solvable (g aLam mu C s : ℝ) (hg : 0 < g) (hC : 0 < C)
    (hmu : 0 < mu) (haLam : 0 ≤ aLam)
    (hs : s = 2 * g / (C * (g * aLam + 2 * mu))) :
    0 < s := by
  rw [hs, div_pos_iff]
  left
  constructor
  · linarith
  · exact mul_pos hC (by nlinarith [mul_nonneg (le_of_lt hg) haLam])

/-! ### 二、Tdot 约掉 (R155.3) -/

/-- |eps*dl*Tdot| = eps*|dl|*Tdot（eps>0、Tdot>0）。 -/
theorem abs_rate (eps dl Tdot : ℝ) (heps : 0 < eps) (hTdot : 0 < Tdot) :
    |eps * dl * Tdot| = eps * |dl| * Tdot := by
  rw [abs_mul, abs_mul, abs_of_pos heps, abs_of_pos hTdot]

/-- mu=alpha*Tdot/3、|g|=eps*|dl|*Tdot ⇒ r=2mu/|g|=2alpha/(3eps|dl|)。 -/
theorem tdot_cancel (alpha Tdot eps dl : ℝ) (hTdot : 0 < Tdot) (heps : 0 < eps)
    (hdl : dl ≠ 0) :
    2 * ((alpha * Tdot) / 3) / |eps * dl * Tdot| = 2 * alpha / (3 * eps * |dl|) := by
  rw [abs_rate eps dl Tdot heps hTdot]
  field_simp [ne_of_gt hTdot, ne_of_gt heps, hdl]

/-- r 的无量纲性：两个不同 Tdot 给同一 r。 -/
theorem r_independent_of_rate (alpha eps dl T1 T2 : ℝ) (hT1 : 0 < T1) (hT2 : 0 < T2)
    (heps : 0 < eps) (hdl : dl ≠ 0) :
    2 * ((alpha * T1) / 3) / |eps * dl * T1|
      = 2 * ((alpha * T2) / 3) / |eps * dl * T2| := by
  rw [tdot_cancel alpha T1 eps dl hT1 heps hdl,
      tdot_cancel alpha T2 eps dl hT2 heps hdl]

/-! ### 三、s 的等价形式与发散 -/

/-- g<0 时 s=2g/[C(g*aLam+2mu)] 等于 2/[C(aLam-r)]，r=2mu/|g|。 -/
theorem s_equiv_form (g aLam mu C r : ℝ) (hg : g < 0)
    (hr : r = 2 * mu / |g|) :
    2 * g / (C * (g * aLam + 2 * mu)) = 2 / (C * (aLam - r)) := by
  rw [hr, abs_of_neg hg]
  field_simp [ne_of_lt hg]
  ring

/-- C>0 且 d>0 时 2/(C*d)>0。 -/
theorem two_div_pos (C d : ℝ) (hC : 0 < C) (hd : 0 < d) : 0 < 2 / (C * d) := by
  exact div_pos (by norm_num) (mul_pos hC hd)

/-- C>0 时 2/(C*d)>0 ⟺ d>0。 -/
theorem two_div_pos_iff (C d : ℝ) (hC : 0 < C) : 0 < 2 / (C * d) ↔ 0 < d := by
  rw [div_pos_iff]
  constructor
  · intro h
    rcases h with h | h
    · have hcases := (mul_pos_iff.mp h.2)
      rcases hcases with hpos | hneg
      · exact hpos.2
      · linarith
    · norm_num at h
  · intro hd
    exact Or.inl ⟨by norm_num, mul_pos hC hd⟩

/-- d↓0+ 时 2/(C*d) 超过任意 M：取 d<2/(C*M)。 -/
theorem s_blows_up (C d M : ℝ) (hC : 0 < C) (hd : 0 < d) (hM : 0 < M)
    (hsmall : d < 2 / (C * M)) : M < 2 / (C * d) := by
  have hCM : 0 < C * M := mul_pos hC hM
  have hCd : 0 < C * d := mul_pos hC hd
  rw [lt_div_iff₀ hCd]
  have hsmall' : d * (C * M) < 2 := (lt_div_iff₀ hCM).mp hsmall
  nlinarith

/-! ### 四、w 两支展开的代数骨架 -/

/-- 低温 w=1-k*u^2 且 0<k*u^2<1 ⇒ 0<w<1。 -/
theorem w_low_bounds (k u : ℝ) (hk : 0 < k) (hu : 0 < u) (hku : k * u ^ 2 < 1) :
    0 < 1 - k * u ^ 2 ∧ 1 - k * u ^ 2 < 1 := by
  constructor <;> nlinarith [sq_pos_of_pos hu, mul_pos hk (sq_pos_of_pos hu)]

/-- 高温 w=c/u、c>0、u>1 ⇒ 0<w<c。 -/
theorem w_high_bounds (c u : ℝ) (hc : 0 < c) (hu : 1 < u) :
    0 < c / u ∧ c / u < c := by
  have hu0 : 0 < u := lt_trans zero_lt_one hu
  constructor
  · exact div_pos hc hu0
  · rw [div_lt_iff₀ hu0]
    nlinarith [mul_lt_mul_of_pos_left hu hc]

/-! ### 五、r(T) 两支单调性 -/

/-- 低温导数骨架：|dlnw/dT|=k*u ⇒ r=2(alpha0*u^3)/(3eps*k*u)=K*u^2。 -/
theorem r_low_form (alpha0 k u eps K : ℝ) (hu : u ≠ 0) (hk : k ≠ 0) (heps : eps ≠ 0)
    (hK : K = 2 * alpha0 / (3 * eps * k)) :
    2 * (alpha0 * u ^ 3) / (3 * eps * (k * u)) = K * u ^ 2 := by
  rw [hK]
  field_simp [hu, hk, heps]

/-- 金属低温：|dlnw/dT|=k*u、alpha=alpha1*u ⇒ r 与 u 无关。 -/
theorem r_metal_const (alpha1 k u eps : ℝ) (hu : u ≠ 0) (hk : k ≠ 0) (heps : eps ≠ 0) :
    2 * (alpha1 * u) / (3 * eps * (k * u)) = 2 * alpha1 / (3 * eps * k) := by
  field_simp [hu, hk, heps]

/-- 高温导数骨架：|dlnw/dT|=1/u ⇒ r=2alpha0*u/(3eps)。 -/
theorem r_high_form (alpha0 u eps : ℝ) (hu : u ≠ 0) (heps : eps ≠ 0) :
    2 * alpha0 / (3 * eps * (1 / u)) = (2 * alpha0 / (3 * eps)) * u := by
  field_simp [hu, heps]

/-- K>0、0<u1<u2 ⇒ K*u1^2<K*u2^2（绝缘体支严格增）。 -/
theorem low_r_strict_mono (K u1 u2 : ℝ) (hK : 0 < K) (hu1 : 0 < u1) (hu12 : u1 < u2) :
    K * u1 ^ 2 < K * u2 ^ 2 := by
  exact mul_lt_mul_of_pos_left (pow_lt_pow_left₀ hu12 (le_of_lt hu1) (by norm_num : (2 : ℕ) ≠ 0)) hK

/-- K>0、0<u<1 ⇒ K*u^2<K*u（低温支次线性，故 u→0 时比线性更快趋零）。 -/
theorem low_r_sublinear (K u : ℝ) (hK : 0 < K) (hu0 : 0 < u) (hu1 : u < 1) :
    K * u ^ 2 < K * u := by
  have h : u ^ 2 < u := by nlinarith
  exact mul_lt_mul_of_pos_left h hK

/-- A>0、0<u1<u2 ⇒ A*u1<A*u2（高温支 r∝u 严格增）。 -/
theorem high_r_strict_mono (A u1 u2 : ℝ) (hA : 0 < A) (hu12 : u1 < u2) :
    A * u1 < A * u2 := by
  exact mul_lt_mul_of_pos_left hu12 hA

/-- 超导温区稳定性：aLam>r 给 s 有限正，与 aLam≈O(1) 时 r→0 相容。 -/
theorem superconducting_stable (C aLam r : ℝ) (hC : 0 < C) (hr0 : 0 ≤ r) (hrsmall : r < aLam) :
    0 < 2 / (C * (aLam - r)) := by
  exact two_div_pos C (aLam - r) hC (sub_pos.mpr hrsmall)

end CQM.MeasurableFailure
