import SuperconductivityChain.Basic

/-!
# 阶段 7：渗流、资源与扩大（环 15–18）

形式化数据结构：配对/同步概率、容量约束、扩大项、资源饱和终止。
阈值等价性、有限尺寸标度、独立动力学均不证。

缺口：`M8`、`审-4`、`审-5`、`审-6`、`审-12`、`临-2`、`临-3`、`临-21`、`临-24`、`临-25`。
-/

namespace CQM.SuperconductivityChain

open scoped BigOperators

/-- 环 15：配对概率与同步概率的容器；数值关系不在结构里冒充定理。 -/
structure PercolationData where
  pPair : ℝ
  pSync : ℝ
  pCrit : ℝ
  pPair_nonneg : 0 ≤ pPair
  pPair_le_one : pPair ≤ 1

/-- 环 15：配对概率落在 `[0,1]`；这只是字段的重述，不证明阈值等价。 -/
theorem pPair_mem_Icc (P : PercolationData) : P.pPair ∈ Set.Icc (0 : ℝ) 1 :=
  ⟨P.pPair_nonneg, P.pPair_le_one⟩

/-- 环 16：多域资源分配，`Σ n_k ≤ n_eff`。 -/
structure ResourceAllocation (ι : Type*) [Fintype ι] where
  nEff : ℕ
  n : ι → ℕ
  capacity : (∑ i, n i) ≤ nEff

/-- 环 16：容量约束的直接读出。 -/
theorem ResourceAllocation.sum_le_nEff {ι : Type*} [Fintype ι]
    (R : ResourceAllocation ι) : (∑ i, R.n i) ≤ R.nEff :=
  R.capacity

/-- 环 17：扩大项 `Ḋ = B + (Ṁ/M)(D_new − D)`。 -/
noncomputable def expansionRate (B Mdot M Dnew D : ℝ) : ℝ :=
  B + (Mdot / M) * (Dnew - D)

/-- 环 17：资源增长率为零时，扩大项只剩基础项 `B`。 -/
theorem expansionRate_zero_Mdot (B M Dnew D : ℝ) :
    expansionRate B 0 M Dnew D = B := by
  unfold expansionRate
  ring

/-- 环 18：资源上限被分完，即终止判据采用资源上限而非 2D 几何上限。 -/
def ResourceTermination {ι : Type*} [Fintype ι]
    (R : ResourceAllocation ι) : Prop :=
  (∑ i, R.n i) = R.nEff

/-- 环 18：终止等价于容量约束没有剩余空间。 -/
theorem resourceTermination_iff_noSlack {ι : Type*} [Fintype ι]
    (R : ResourceAllocation ι) :
    ResourceTermination R ↔ ¬ (∑ i, R.n i) < R.nEff := by
  unfold ResourceTermination
  constructor
  · intro h
    omega
  · intro h
    exact le_antisymm R.capacity (Nat.le_of_not_gt h)

/-- 环 18：资源容量用尽时给出终止；这是资源上限，不是 2D 几何饱和。 -/
theorem resourceTermination_of_sum_eq {ι : Type*} [Fintype ι]
    (R : ResourceAllocation ι) (h : (∑ i, R.n i) = R.nEff) :
    ResourceTermination R := h

end CQM.SuperconductivityChain
