/-
InducedClusterIdentity.lean —— 第 154 轮：R-163

审-4：诱导键网络的簇恒等定理与阈值归属。

主结论（图论层，对任意相邻关系与任意占据集）：
  1. 座可达（路径顶点全在占据集 S 内）与诱导键可达（每条边两端都在 S 内）
     是同一个关系；
  2. 因此“存在跨越 A→B 的簇”在两个模型中同真同假；
  3. 诱导键网络的临界座占据率就是座渗流的临界值，诱导键占比在其临界点
     为 p_c^2，而不是独立键渗流的 1/2。

本文件只承载图论恒等与标量代数；不证明方格座阈值 0.592746 本身
（外部数值结果 L31），不做 Monte Carlo，不给出材料值。
无 axiom / sorry / admit / native_decide / unsafe。
-/
import Mathlib.Data.Set.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Analysis.SpecialFunctions.Pow.Real

set_option linter.unusedVariables false

namespace CQM.InducedCluster

variable {V : Type*}

/-- 诱导边关系：两端都在占据集 `S` 中且相邻。 -/
def InducedAdj (adj : V → V → Prop) (S : Set V) (x y : V) : Prop :=
  x ∈ S ∧ y ∈ S ∧ adj x y

/-- 座可达：存在一条路径，所有顶点都在 `S` 内、相邻步用 `adj`。 -/
inductive SiteReach (adj : V → V → Prop) (S : Set V) : V → V → Prop
  | refl (x : V) (hx : x ∈ S) : SiteReach adj S x x
  | step {x y z : V} (hxy : SiteReach adj S x y) (hyz : adj y z) (hz : z ∈ S) :
      SiteReach adj S x z

/-- 诱导键可达：每一步都走一条诱导边（两端都在 `S` 中）。 -/
inductive BondReach (adj : V → V → Prop) (S : Set V) : V → V → Prop
  | refl (x : V) (hx : x ∈ S) : BondReach adj S x x
  | step {x y z : V} (hxy : BondReach adj S x y) (hyz : InducedAdj adj S y z) :
      BondReach adj S x z

/-- 座可达的终点在 `S` 内。 -/
theorem siteReach_right_mem {adj : V → V → Prop} {S : Set V} {x y : V}
    (h : SiteReach adj S x y) : y ∈ S := by
  induction h with
  | refl hx => exact hx
  | step _ _ hz => exact hz

/-- 座可达的起点在 `S` 内。 -/
theorem siteReach_left_mem {adj : V → V → Prop} {S : Set V} {x y : V}
    (h : SiteReach adj S x y) : x ∈ S := by
  induction h with
  | refl hx => exact hx
  | step hxy _ _ ih => exact ih

/-- 诱导键可达的终点在 `S` 内。 -/
theorem bondReach_right_mem {adj : V → V → Prop} {S : Set V} {x y : V}
    (h : BondReach adj S x y) : y ∈ S := by
  induction h with
  | refl hx => exact hx
  | step _ hyz => exact hyz.2.1

/-- 诱导键可达的起点在 `S` 内。 -/
theorem bondReach_left_mem {adj : V → V → Prop} {S : Set V} {x y : V}
    (h : BondReach adj S x y) : x ∈ S := by
  induction h with
  | refl hx => exact hx
  | step hxy _ ih => exact ih

/-- 座可达 ⇒ 诱导键可达。 -/
theorem siteReach_to_bondReach {adj : V → V → Prop} {S : Set V} {x y : V}
    (h : SiteReach adj S x y) : BondReach adj S x y := by
  induction h with
  | refl hx => exact BondReach.refl _ hx
  | step hxy hyz hz ih =>
      exact BondReach.step ih ⟨siteReach_right_mem hxy, hz, hyz⟩

/-- 诱导键可达 ⇒ 座可达。 -/
theorem bondReach_to_siteReach {adj : V → V → Prop} {S : Set V} {x y : V}
    (h : BondReach adj S x y) : SiteReach adj S x y := by
  induction h with
  | refl hx => exact SiteReach.refl _ hx
  | step hxy hyz ih =>
      exact SiteReach.step ih hyz.2.2 hyz.2.1

/-- **簇恒等定理**：座可达与诱导键可达逐点等价。 -/
theorem siteReach_iff_bondReach {adj : V → V → Prop} {S : Set V} {x y : V} :
    SiteReach adj S x y ↔ BondReach adj S x y :=
  ⟨siteReach_to_bondReach, bondReach_to_siteReach⟩

/-- “存在跨越 `A → B` 的簇”这一事件。 -/
def Percolates (R : V → V → Prop) (A B : Set V) : Prop :=
  ∃ x ∈ A, ∃ y ∈ B, R x y

/-- 座模型与诱导键模型的跨越事件同真同假。 -/
theorem percolates_iff {adj : V → V → Prop} {S A B : Set V} :
    Percolates (SiteReach adj S) A B ↔ Percolates (BondReach adj S) A B := by
  constructor
  · rintro ⟨x, hx, y, hy, hxy⟩
    exact ⟨x, hx, y, hy, siteReach_to_bondReach hxy⟩
  · rintro ⟨x, hx, y, hy, hxy⟩
    exact ⟨x, hx, y, hy, bondReach_to_siteReach hxy⟩

/-! ### 标量层：两个阈值不可互换 -/

/-- 方格座阈值（外部值 L31）。 -/
def pcSite : ℝ := 0.592746

/-- 诱导键在座阈值处的占比。 -/
def qcInduced : ℝ := pcSite ^ 2

/-- 诱导键在座阈值处的占比严格小于独立键阈值 `1/2`。 -/
theorem qcInduced_lt_half : qcInduced < (1 / 2 : ℝ) := by
  unfold qcInduced pcSite
  norm_num

/-- 等价地，诱导键在座阈值处的占比不等于 `1/2`。 -/
theorem qcInduced_ne_half : qcInduced ≠ (1 / 2 : ℝ) := by
  unfold qcInduced pcSite
  norm_num

/-- 平方映射在非负半轴严格增：同一个诱导键占比不可能对应两个非负座比例。 -/
theorem sq_strictMonoOn_nonneg : StrictMonoOn (fun p : ℝ => p ^ 2) (Set.Ici 0) := by
  intro a ha b hb hab
  rw [Set.mem_Ici] at ha hb
  nlinarith [sq_nonneg (b - a), sq_nonneg (b + a)]

/-- 若 `p ≥ 0`、`q ≥ 0` 且 `p^2 = q`，则 `p` 是唯一的非负解。 -/
theorem eq_sqrt_of_sq_eq {p q : ℝ} (hp : 0 ≤ p) (hq : 0 ≤ q) (h : p ^ 2 = q) :
    p = Real.sqrt q := by
  rw [← h, Real.sqrt_sq hp]

/-- 独立键阈值 `1/2` 对应的是 `sqrt(1/2) ≈ 0.7071`，不是座阈值 `0.592746`。 -/
theorem half_threshold_is_not_site :
    Real.sqrt (1 / 2 : ℝ) ≠ pcSite := by
  unfold pcSite
  intro h
  have hsq : (Real.sqrt (1 / 2 : ℝ)) ^ 2 = (1 / 2 : ℝ) := by
    rw [Real.sq_sqrt]
    norm_num
  rw [h] at hsq
  norm_num at hsq

end CQM.InducedCluster
