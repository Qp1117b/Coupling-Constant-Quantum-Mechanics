import SuperconductivityChain.Basic
import SuperconductivityChain.Stage4
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-!
# 阶段 5：局域域、配对算符的节点实现与 DFT 分解（环 13 / 13.A）

次序：先有配对算符（`Stage4.PairOperatorData`），后以节点质数标签实现；
`PrimeRealization` 把“实现”写成结构，不把质数标签当前提。

形式化局域配对域、质数实现、Goldbach 条件下的配对供给、以 2 配对为基准的
密度剖面，以及 DFT 四项结构容器。相变等效三分不证；Goldbach 不证；
DFT 四项分解不是已证等式（`临-26`）。

缺口：`临-10`、`临-11`、`临-13`、`临-22`、`临-26`、`临-5`、`链外-D`、`G22`。
-/

namespace CQM.SuperconductivityChain

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- 环 13：节点 `i` 的局域配对域，取有限簇（有限性由 `Finset` 承担）。 -/
abbrev PairDomain (V : Type*) [DecidableEq V] := Finset V

/-- 环 13.A：质数实现；`operator` 先于 `label`，标签是算符的节点侧实现不是前提。 -/
structure PrimeRealization (V : Type*) where
  operator : PairOperatorData
  label : V → ℕ
  isPrime : ∀ i, Nat.Prime (label i)

/-- 兼容名：旧称“质数标签”，语义是 `PrimeRealization`，不是独立前提。 -/
abbrev PrimeLabeled (V : Type*) := PrimeRealization V

/-- 强 Goldbach 命题（偶数 ≥4 为两质数之和）；本文件不证明它。 -/
def Goldbach : Prop :=
  ∀ n : ℕ, 2 < n → Even n → ∃ p q : ℕ,
    Nat.Prime p ∧ Nat.Prime q ∧ p + q = n

/-- 环 13.A：一个偶数配对名额的质数供给；这是数据，不是命题证明。 -/
structure PairingSupply (n : ℕ) where
  left : ℕ
  right : ℕ
  prime_left : Nat.Prime left
  prime_right : Nat.Prime right
  sum_eq : left + right = n

/-- 环 13.A1：节点平均固有时流速；分母为零时 Lean 的除法取 0。 -/
noncomputable def meanValue (v : V → ℝ) : ℝ :=
  (∑ i, v i) / (Fintype.card V : ℝ)

/-- 环 13.A1：相对涨落 `(v_i - vbar)/vbar`。 -/
noncomputable def relativeFluctuation (v : V → ℝ) (i : V) : ℝ :=
  (v i - meanValue v) / meanValue v

/-- 环 13.A2 的谓词层：比值落在 `2 ln n` 的 `η` 邻域内。
这里不写 `spec`；有限比值集没有谱定理，`η` 是未定的分档半宽（`临-26`）。 -/
def LadderFit (v : V → ℝ) (η : ℝ) : Prop :=
  ∀ i, ∃ n : ℕ, n ≠ 0 ∧ Even n ∧
    |relativeFluctuation v i - 2 * Real.log n| ≤ η

/-- 精确落在阶梯上的点满足任意非负半宽的 `LadderFit`；不证明存在这样的点。 -/
theorem ladderFit_of_exact {v : V → ℝ} {η : ℝ} (hη : 0 ≤ η)
    (h : ∀ i, ∃ n : ℕ, n ≠ 0 ∧ Even n ∧
      relativeFluctuation v i = 2 * Real.log n) :
    LadderFit v η := by
  intro i
  rcases h i with ⟨n, hn, he, hEq⟩
  exact ⟨n, hn, he, by simpa [hEq] using hη⟩

/-- `LadderFit` 对半宽单调：已落在 `η` 邻域，就落在更大的 `η'` 邻域。 -/
theorem LadderFit.mono {v : V → ℝ} {η η' : ℝ} (h : LadderFit v η) (hη : η ≤ η') :
    LadderFit v η' := by
  intro i
  rcases h i with ⟨n, hn, he, hle⟩
  exact ⟨n, hn, he, le_trans hle hη⟩

/-- 环 13.A：Goldbach 条件下的配对供给；这是条件命题，不是 Goldbach 的证明。 -/
theorem goldbach_supply {n : ℕ} (h : Goldbach) (hn : 2 < n) (he : Even n) :
    Nonempty (PairingSupply n) := by
  rcases h n hn he with ⟨p, q, hp, hq, hsum⟩
  exact ⟨{ left := p, right := q, prime_left := hp, prime_right := hq, sum_eq := hsum }⟩

/-- 环 13.A：把 Goldbach 作为显式外部假设，一次给出所有偶数名额的配对供给。 -/
theorem goldbach_supply_all (h : Goldbach) :
    ∀ n : ℕ, 2 < n → Even n → Nonempty (PairingSupply n) := by
  intro n hn he
  exact goldbach_supply h hn he

/-- 环 13.A：以 2 配对为基准的局域配对密度剖面；`total_eq_one` 把基准读成概率分布。 -/
structure PairDensityProfile (V : Type*) [Fintype V] where
  base : V → ℝ
  base_nonneg : ∀ i, 0 ≤ base i
  total_eq_one : (∑ i, base i) = 1

/-- 基准概率剖面的单点质量不超过 1；这是归一化的直接推论，不声称物理密度。 -/
theorem PairDensityProfile.base_le_one (ρ : PairDensityProfile V) (i : V) :
    ρ.base i ≤ 1 := by
  have h : ρ.base i ≤ ∑ j, ρ.base j :=
    Finset.single_le_sum (fun j _ => ρ.base_nonneg j) (Finset.mem_univ i)
  simpa [ρ.total_eq_one] using h

/-- 兼容名：局域配对密度剖面。 -/
abbrev LocalPairDensity (V : Type*) [Fintype V] := PairDensityProfile V

/-- 环 13.A：高模式密度 `ρ^(n) = (2/n) ρ^(2)`。 -/
noncomputable def higherDensity (ρ : PairDensityProfile V) (n : ℕ) : V → ℝ :=
  fun i => pairModeWeight n * ρ.base i

/-- 高模式密度非负；`n>0` 时权重非负。 -/
theorem higherDensity_nonneg (ρ : PairDensityProfile V) (n : ℕ) :
    ∀ i, 0 ≤ higherDensity ρ n i := by
  intro i
  unfold higherDensity
  exact mul_nonneg (pairModeWeight_nonneg n) (ρ.base_nonneg i)

/-- 高模式的总质量是 `2/n`；它不是概率分布，只有 `n=2` 时总质量为 1。 -/
theorem higherDensity_total (ρ : PairDensityProfile V) (n : ℕ) :
    (∑ i, higherDensity ρ n i) = pairModeWeight n := by
  unfold higherDensity
  rw [← Finset.mul_sum, ρ.total_eq_one, mul_one]

/-- 高模式的数学重标度 `(n/2) ρ^(n)`；物理权重仍是 `2/n`，态—算子映射未证（`临-5`）。 -/
noncomputable def normalizedHigherDensity (ρ : PairDensityProfile V) (n : ℕ) : V → ℝ :=
  fun i => ((n : ℝ) / 2) * higherDensity ρ n i

/-- 重标度后高模式总质量为 1；这不证明物理权重归一。 -/
theorem normalizedHigherDensity_total (ρ : PairDensityProfile V) {n : ℕ} (hn : n ≠ 0) :
    (∑ i, normalizedHigherDensity ρ n i) = 1 := by
  unfold normalizedHigherDensity
  rw [← Finset.mul_sum, higherDensity_total]
  simp [pairModeWeight, hn]

/-- 重标度后高模式非负。 -/
theorem normalizedHigherDensity_nonneg (ρ : PairDensityProfile V) {n : ℕ} (_hn : 0 < n) :
    ∀ i, 0 ≤ normalizedHigherDensity ρ n i := by
  intro i
  unfold normalizedHigherDensity
  have hnR : (0 : ℝ) ≤ (n : ℝ) := by exact_mod_cast Nat.zero_le n
  exact mul_nonneg (div_nonneg hnR (by norm_num)) (higherDensity_nonneg ρ n i)

/-- 单点域上的基准概率剖面；用来证明该结构不空。 -/
def unitDensity : PairDensityProfile Unit where
  base := fun _ => 1
  base_nonneg := by intro i; norm_num
  total_eq_one := by simp

/-- 环 13.A：DFT 的四项结构容器；不声明四项相加等于已证等式。
`reference` 是参考节点，`baseDensity` 已带概率归一。 -/
structure DFTDecomposition (V : Type*) [Fintype V] where
  formalPairing : Set ℕ
  formalPairing_eq : formalPairing = pairModeSet
  reference : V
  crisisOperator : V → V → ℝ
  baseDensity : PairDensityProfile V
  expansion : V → ℝ
  distance : V → V → ℝ

end CQM.SuperconductivityChain
