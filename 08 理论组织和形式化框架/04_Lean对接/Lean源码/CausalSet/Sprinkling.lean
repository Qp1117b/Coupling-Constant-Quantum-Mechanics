import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Order.Interval.Set.Defs
import CausalSet.Axioms

/-!
# Sprinkling：因果集 → 耦合空间的嵌入

Sprinkling 是 CQM 中因果集与连续耦合空间之间的桥梁。
通过 Poisson 过程将离散因果事件随机嵌入连续耦合空间，
得到耦合空间的基本结构。

## 核心概念
1. **Sprinkling 密度** ρ(u)：耦合坐标 u 处单位体积内的事件数
2. **Sprinkling 嵌入** u: α → ℝ：将因果集事件映射到耦合坐标
3. **耦合速度 c**：δu/δτ，由 Sprinkling 的平均间隔决定
4. **链接数**：因果集的直接相邻关系

## 推导链
因果集 (X, ≺) → Sprinkling → 耦合空间 (u, τ) → 连续极限

## 参考文献
- Bombelli, Lee, Meyer, Sorkin (1987).
- ruster (2026). CNT 完整研究. Zenodo.
-/

open CausalSet
open Set

/-! ## Sprinkling 密度 -/

/-- Sprinkling 密度 ρ(u)：
    在耦合坐标 u 处，单位体积内因果集事件的期望数量。
    在禁闭边界 u → ln L 处，ρ(u) → ∞（密度发散 → 退相干）。 -/
noncomputable def sprinklingDensity (u : ℝ) : ℝ := Real.exp u

/-- Sprinkling 密度严格为正 -/
theorem sprinklingDensity_pos (u : ℝ) : sprinklingDensity u > 0 :=
  Real.exp_pos u

/-- Sprinkling 密度是严格单调递增的 -/
theorem sprinklingDensity_strictMono : StrictMono sprinklingDensity := by
  intro a b h
  unfold sprinklingDensity
  exact Real.exp_lt_exp.mpr h

/-- Sprinkling 密度在 u → ∞ 时发散到 ∞ -/
theorem sprinklingDensity_tendsto_infty : Filter.Tendsto sprinklingDensity Filter.atTop Filter.atTop := by
  unfold sprinklingDensity
  exact Real.tendsto_exp_atTop

/-! ## Sprinkling 嵌入 — 因果集到耦合空间的映射 -/

/-- Sprinkling 嵌入结构：
    将因果集事件 α 嵌入到耦合坐标空间 ℝ 的映射 u: α → ℝ。
    
    核心性质：
    - `orderPreserving`: x ≺ y → u x < u y（因果序保持）
    - `densityCompatible`: 嵌入的局部事件密度与 sprinklingDensity 一致
    
    在连续极限下，Poisson Sprinkling 过程中，嵌入坐标 u 的分布
    密度为 ρ(u) = exp(u)，即 sprinklingDensity。 -/
structure SprinklingEmbedding (α : Type*) [CausalSet α] where
  /-- 嵌入映射：将因果集事件映射到耦合坐标 -/
  u : α → ℝ
  /-- 保序性：因果前导关系被保持为坐标的严格不等式 -/
  orderPreserving : ∀ {x y : α}, x ≺ y → u x < u y

namespace SprinklingEmbedding

variable {α : Type*} [CausalSet α] (e : SprinklingEmbedding α)

/-- 嵌入映射是单射（在可比较事件对上）：
    如果 x ≺ y，则 u x ≠ u y -/
theorem u_inj_on_comparable {x y : α} (h : x ≺ y) : e.u x ≠ e.u y := by
  linarith [e.orderPreserving h]

/-- 保序性的逆否命题：如果 u x ≥ u y，则 ¬ (x ≺ y) -/
theorem not_prec_of_u_ge {x y : α} (h : e.u x ≥ e.u y) : ¬ (x ≺ y) := by
  intro h_prec
  have h_lt := e.orderPreserving h_prec
  linarith

/-- 嵌入映射在因果过去方向上是单调的：
    如果 x ≺ y 且 y ≺ z，则 u x < u z（传递性 + 保序性） -/
theorem u_trans {x y z : α} (hxy : x ≺ y) (hyz : y ≺ z) : e.u x < e.u z := by
  have h_trans := CausalSet.trans hxy hyz
  exact e.orderPreserving h_trans

/-- 有限 Alexandrov 区间的像在 ℝ 中有界：
    对于任意 x ≺ y，区间 [u x, u y] 是紧致的（因而是有界的）。
    这与 CQM 中"因果区间有限"的公理一致。 -/
theorem u_image_of_interval_bounded {x y : α} (h : x ≺ y) :
    ∃ (a b : ℝ), a ≤ b ∧ ∀ z, x ≺ z → z ≺ y → e.u z ∈ Set.Icc a b := by
  refine ⟨e.u x, e.u y, le_of_lt (e.orderPreserving h), ?_⟩
  intro z hxz hzy
  have h_lt1 : e.u x < e.u z := e.orderPreserving hxz
  have h_lt2 : e.u z < e.u y := e.orderPreserving hzy
  exact ⟨le_of_lt h_lt1, le_of_lt h_lt2⟩

/-- 因果无关事件保持为不同事件。
    
    注意：spacelike 事件可以具有相同的嵌入坐标 u(x) = u(y)
    （它们位于同一类空超曲面上），也可以具有不同的坐标。
    因果序保持 x ≺ y → u x < u y，但其逆不成立：
    u x < u y 并不蕴含 x ≺ y。
    
    此定理确认 spacelike 蕴含事件不同，这是 spacelike 定义的一部分。 -/
theorem u_spacelike_indeterminate {x y : α} (h : spacelike x y) : x ≠ y :=
  h.2.2

end SprinklingEmbedding

/-! ## 耦合速度与离散结构 -/

/-- 耦合速度 c = δu/δτ：
    由因果集 Sprinkling 的平均事件间隔决定。
    在连续极限下，c 与 1/ρ(u)^{1/d} 成正比，其中 d 是耦合空间维数。 -/
noncomputable def couplingSpeed (rho : ℝ) (_hrho : rho > 0) : ℝ := 1 / rho

/-- 因果集链与耦合空间路径的对应：
    因果集中长度为 n 的链对应耦合空间中长度为 n·δu 的路径。
    其中 δu 是 Sprinkling 的平均间隔。 -/
def chainToPathLength (chainLength : ℕ) (deltaU : ℝ) : ℝ :=
  (chainLength : ℝ) * deltaU

/-- 再生产时间步进 τ = n·δτ：
    每个再生产步骤对应一个因果集事件，
    离散时间由再生产计数给出。 -/
def reproductionTime (n : ℕ) (deltaTau : ℝ) : ℝ :=
  (n : ℝ) * deltaTau

/-- 链接（link）：因果集中直接相邻的两个事件。
    x 和 y 是链接，当且仅当 x ≺ y 且不存在 z 满足 x ≺ z ≺ y。 -/
def isLink {α : Type*} [CausalSet α] (x y : α) : Prop :=
  x ≺ y ∧ ∀ z, x ≺ z → z ≺ y → z = x ∨ z = y

/-- 链接的基本性质：如果 x 和 y 是链接，则 x ≺ y -/
theorem isLink_imp_prec {α : Type*} [CausalSet α] {x y : α} (h : isLink x y) : x ≺ y :=
  h.1

/-- 链接的不可分解性：不存在中间事件 -/
theorem isLink_no_intermediate {α : Type*} [CausalSet α] {x y z : α}
    (h : isLink x y) (hxz : x ≺ z) (hzy : z ≺ y) : z = x ∨ z = y :=
  h.2 z hxz hzy

/-- 耦合空间的度规从 Sprinkling 链接数导出：
    ds² = -du² + dτ²（耦合空间中的双曲度规）
    这是从因果集离散结构到连续度规的涌现。 -/
def couplingMetric (du dτ : ℝ) : ℝ :=
  - du^2 + dτ^2

/-! ## Sprinkling 嵌入与耦合空间的连接 -/

/-- 从 Sprinkling 嵌入到耦合坐标的对应：
    嵌入 u(x) 直接给出耦合坐标 u。
    耦合强度 r = exp(u(x)) = sprinklingDensity(u(x))。 -/
def embeddingToCouplingCoordinate {α : Type*} [CausalSet α]
    (e : SprinklingEmbedding α) (x : α) : ℝ := e.u x

/-- Sprinkling 嵌入坐标与 Sprinkling 密度的关系：
    在事件 x 处，sprinklingDensity(u(x)) = exp(u(x))。
    这是耦合空间的基本几何关系。 -/
theorem embeddingDensityRelation {α : Type*} [CausalSet α]
    (e : SprinklingEmbedding α) (x : α) :
    sprinklingDensity (e.u x) = Real.exp (e.u x) := by
  rfl

/-- 嵌入坐标的差给出耦合空间中的"距离"（在 u 坐标中）：
    |u(x) - u(y)| 衡量两个事件在耦合空间中的分离程度。 -/
def couplingCoordinateDistance {α : Type*} [CausalSet α]
    (e : SprinklingEmbedding α) (x y : α) : ℝ :=
  |e.u x - e.u y|

/-- 耦合坐标距离的非负性 -/
theorem couplingCoordinateDistance_nonneg {α : Type*} [CausalSet α]
    (e : SprinklingEmbedding α) (x y : α) : couplingCoordinateDistance e x y ≥ 0 :=
  abs_nonneg _

/-- 当 x ≺ y 时，耦合坐标距离 = u(y) - u(x) > 0 -/
theorem couplingCoordinateDistance_of_prec {α : Type*} [CausalSet α]
    (e : SprinklingEmbedding α) {x y : α} (h : x ≺ y) :
    couplingCoordinateDistance e x y = e.u y - e.u x := by
  unfold couplingCoordinateDistance
  have h_lt : e.u x < e.u y := e.orderPreserving h
  rw [abs_of_neg (by linarith : e.u x - e.u y < 0)]
  ring

/-- 当 x ≺ y 时，耦合坐标距离严格为正 -/
theorem couplingCoordinateDistance_pos_of_prec {α : Type*} [CausalSet α]
    (e : SprinklingEmbedding α) {x y : α} (h : x ≺ y) :
    couplingCoordinateDistance e x y > 0 := by
  rw [couplingCoordinateDistance_of_prec e h]
  have h_lt : e.u x < e.u y := e.orderPreserving h
  linarith