import Mathlib.Data.Real.Basic
import Mathlib.Data.Nat.Basic
import Mathlib.Tactic
import PrimeGeometry.Basic
import PrimeGeometry.WindingDensity
import PrimeGeometry.Compton
import PrimeGeometry.Spin

/-!
# 粒子分类：费米子、玻色子与真空 (Particle Classification)

本模块形式化论文第 8.2 节提出的粒子分类体系：
- **费米子** = 质数（不可分解的再生产事件）
- **玻色子** = 合数（可分解的再生产事件，有内部子结构）
- **真空/希格斯** = 1（再生产的"零点"，对称性破缺的基点）
- **规范玻色子** = 角点处的密度跳跃（因果通道间的跃迁）

## 核心分类

| 数论 | CQM 粒子 | 物理性质 |
|:-----|:---------|:---------|
| 质数 p | 费米子 | 自旋半整数，Pauli 不相容 |
| 合数 n = ab | 玻色子 | 自旋整数，Bose-Einstein 凝聚 |
| 1 | 真空/希格斯 | 对称性破缺的基点 |
| 0 | — | 无再生产（无存在） |

## 定理

- 粒子分类的完备性（每个 n ≥ 1 恰好属于费米子/玻色子/真空之一）
- 粒子分类的互斥性（费米子 ≠ 玻色子，真空独立）
- 活跃素数 {2, 3, 5} 都是费米子
- 合数 4 = 2×2 是最小玻色子

## 参考文献

- ruster (2026). 质数几何密度-三代粒子模型：因果时弯曲与康普顿波长猜想.
- ruster (2026). CNT 完整研究. Zenodo. DOI: 10.5281/zenodo.20804380.
-/

namespace CQM

open scoped BigOperators

/-! ## 粒子分类定义 -/

/-- 费米子：不可分解的再生产事件（质数 p ≥ 2）。
    在 CQM 中，质数作为基本因果单元，满足 Pauli 不相容原理：
    同一因果时位置不能有两个相同的质数（质数唯一性）。
    每个质数标记一个独立的因果时闭合环，对应费米子的排斥统计。 -/
def isFermion (n : ℕ) : Prop := Nat.Prime n

/-- 玻色子：可分解的再生产事件（合数，有内部子结构）。
    合数可分解为质数乘积，对应可叠加的多粒子态。
    在 CQM 中，合数在因果时角点处产生密度跳跃，
    对应规范玻色子的交换（见 `gaugeBosonExchange`）。 -/
def isBoson (n : ℕ) : Prop := n ≥ 2 ∧ ¬ Nat.Prime n

/-- 真空/希格斯：单位元 1（既非质数也非合数）。
    在 CQM 中，1 是再生产的"零点"——因果时数轴的起点，
    对应对称性破缺前的真空态。希格斯机制从 1 的
    "非质数非合数"的特殊地位中涌现。 -/
def isVacuum (n : ℕ) : Prop := n = 1

/-- 粒子分类的完备性：每个 n ≥ 1 恰好属于费米子、玻色子、真空之一。 -/
theorem particle_classification_exhaustive (n : ℕ) (hn : n ≥ 1) :
    isFermion n ∨ isBoson n ∨ isVacuum n := by
  by_cases h : n = 1
  · right; right; exact h
  · have hn2 : n ≥ 2 := by omega
    by_cases hp : Nat.Prime n
    · left; exact hp
    · right; left; exact ⟨hn2, hp⟩

/-- 粒子分类的互斥性：费米子和玻色子不重叠。
    质数不可分解 = 费米子，合数可分解 = 玻色子。 -/
theorem fermion_not_boson (n : ℕ) : isFermion n → ¬ isBoson n := by
  intro hf hb
  rcases hb with ⟨_, hnp⟩
  exact hnp hf

/-- 真空既非费米子也非玻色子：1 既不是质数也不是合数。 -/
theorem vacuum_not_fermion_not_boson (n : ℕ) : isVacuum n → ¬ isFermion n ∧ ¬ isBoson n := by
  intro hv
  have hn1 : n = 1 := hv
  subst hn1
  constructor
  · intro h; exact Nat.not_prime_one h
  · intro h; rcases h with ⟨h2, _⟩; linarith

/-- 费米子的最小例子：2（第一个质数，对应第一代费米子）。 -/
theorem two_is_fermion : isFermion 2 := Nat.prime_two

/-- 玻色子的最小例子：4 = 2 × 2（第一个合数，对应第一个玻色子）。 -/
theorem four_is_boson : isBoson 4 := by
  unfold isBoson
  constructor
  · omega
  · native_decide

/-- 真空的唯一性：只有 n = 1 是真空。 -/
theorem vacuum_unique (n : ℕ) : isVacuum n ↔ n = 1 := by
  unfold isVacuum; rfl

/-! ## 活跃素数作为费米子 -/

/-- 活跃素数 {2, 3, 5} 都是费米子。
    这三个素数对应 CQM 中 Φ(k) > 0 的再生产通道，
    也是因果时三角形三边上的密度来源。 -/
theorem activePrimes_are_fermions : ∀ p ∈ activePrimeSet, isFermion p :=
  activePrimeSet_all_prime

/-- 活跃费米子恰好有 3 个（对应三代）。
    ≤ 5 的素数：2, 3, 5 → 恰好 3 个。 -/
theorem activeFermions_count_three :
    ((Finset.range 6).filter (λ n => decide (Nat.Prime n))).card = 3 := by
  native_decide

/-- 冻结素数（k > 5）不是活跃费米子，但仍是费米子。
    在 CQM 中，冻结素数的再生产潜力 Φ(k) = 0，
    因此在因果时三角形中不产生密度贡献。
    但它们仍标记了"潜在"的费米子态——对应更重的
    未发现粒子，在极早期宇宙中可能短暂存在。 -/
theorem frozenPrimes_are_fermions_but_inactive (p : ℕ) (hp : Nat.Prime p) (hp_gt_5 : p > 5) :
    isFermion p ∧ p ∉ activePrimeSet := by
  constructor
  · exact hp
  · exact frozenPrime_density_zero p hp hp_gt_5

/-! ## 玻色子与规范玻色子 -/

/-- 合数 6 = 2 × 3：活跃素数乘积，对应"双费米子"复合态。
    在 CQM 中，6 可能是第一个规范玻色子（色 SU(3) 的胶子）的
    数论对应。活跃素数乘积的特殊地位使其成为因果通道间
    跃迁的载体。 -/
theorem six_is_boson : isBoson 6 := by
  unfold isBoson
  constructor
  · omega
  · native_decide

/-- 角点密度跳跃对应规范玻色子交换。

    在因果时三角形的顶点处，缠绕密度 ρ(s) 发生跳跃 Δρ。
    该跳跃在物理上对应规范玻色子的交换——
    从一个因果通道到另一个因果通道的跃迁。

    角点处的三向分叉（每条边分叉到两个相邻边）
    推广到连续极限给出 SU(3) 三重性（色荷）。
    边内部的"质数/合数"二态对应 SU(2) 二重态（弱同位旋）。

    完整定义需密度跳跃 Δρ 的 Dirichlet L-函数解析计算。 -/
def gaugeBosonExchange (_p : CausalPolygon) (_vertex : ℕ) : ℝ := 0
  -- 占位：完整定义需密度跳跃 Δρ 的解析计算

/-! ## 费米子-玻色子统计与自旋的关系

    在 CQM 中，自旋-统计关系不是公理，而是因果时定向的直接推论：
    - 费米子（质数）→ 因果时闭合环的定向 → Z_2 定向 → 自旋半整数
    - 玻色子（合数）→ 可分解为多个闭合环 → 定向抵消 → 自旋整数

    这与标准模型完全一致，但推导路径完全不同：
    不是从 Lorentz 群的表示论出发，而是从因果时几何的
    定向结构出发。 -/

end CQM