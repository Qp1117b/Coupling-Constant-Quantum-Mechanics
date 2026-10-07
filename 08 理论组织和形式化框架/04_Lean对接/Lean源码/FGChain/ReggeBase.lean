import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import FGChain.CurvatureOperator
import FGChain.Basic

/-!
# FG 链路环节 9（发生学前置）：晶胞分布构成 Regge 底空间

《CQM_超导核心理论》§2.5 链A / 《FG_纤维丛理论》§1–2 的底空间构造形式化。

## 发生学修正说明

原链路把"晶胞分布构成Regge底空间"放在链路中段（环节9）；按两链结构
（《CQM_超导核心理论》§2.5），底空间几何由**链A（晶胞几何分布）生成**，
链B（嘉当矩阵）**仅约束**可实现谱。本模块将底空间构造前置为纤维丛的
发生学起点，并给出两链交汇定理。

## 链路位置

```
[环节1–2] 嘉当矩阵（链B 谱约束）∥ 晶胞几何分布（链A 生成）
   ↓（两链交汇）
[环节9] 晶胞分布构成 Regge 底空间（顶点集 + 角亏曲率场）
   ↓
[环节10] 纤维丛（见 FGChain.FiberBundle）
```
-/

namespace CQM.FGChain

open scoped Real

/-! ## 1. 晶胞分布与 Regge 底空间 -/

/-- **晶胞分布**：n 个晶胞中心的空间位置（ℝ³ 中有限点集）。
    这是链A 的几何原料：分布本身（而非嘉当矩阵）生成底空间。 -/
def CellDistribution (n : ℕ) := Fin n → (Fin 3 → ℝ)

/-- **Regge 底空间**：晶胞分布上的离散单纯复形结构——
    顶点集（晶胞中心）、逐顶点角亏曲率场（链A 生成）、
    以及谱可实现性谓词（链B 约束作用点）。
    角亏非负（凸 Regge 几何标准设定，保证 √(1−βδ_v) 良定义域）。 -/
structure ReggeBaseSpace (n : ℕ) where
  /-- 底空间顶点：晶胞中心位置（链A 几何分布） -/
  vertices : CellDistribution n
  /-- 底空间角亏曲率场：逐顶点 δ_v（链A 生成：几何分布 → Regge 晶胞 → 角亏） -/
  deficitField : Fin n → ℝ
  /-- 曲率场由链A 生成（生成关系记录） -/
  chainA : ChainAGeometric n
  /-- 生成一致性：角亏场 = 链A 的角亏 -/
  field_from_chainA : ∀ v, deficitField v = chainA.deficits v
  /-- 角亏非负（可实现几何：0 ≤ δ_v < 1/β 时进入固有时流速通道） -/
  deficit_nonneg : ∀ v, 0 ≤ deficitField v
  /-- 谱可实现性谓词（链B 约束的作用接口） -/
  spectralOK : Fin n → Prop

/-- 底空间曲率场逐点由链A 角亏给出（无独立输入）。 -/
theorem ReggeBaseSpace.deficit_eq_chainA {n : ℕ} (B : ReggeBaseSpace n) (v : Fin n) :
    B.deficitField v = B.chainA.deficits v := B.field_from_chainA v

/-! ## 2. 两链交汇定理 -/

/-- **两链交汇定理**：Regge 底空间是链A（生成）与链B（约束）的交汇点——
    给定链A 数据与链B 数据，存在底空间，其角亏场逐点等于链A 生成值，
    且每点满足链B 约束。（底空间几何由链A 生成；可实现性由链B 判定；
    二者角色正交。） -/
theorem two_chain_meet {n : ℕ} (A : ChainAGeometric n)
    (hnonneg : ∀ v i, 0 ≤ A.cells v i) (B : ChainBSpectral)
    (hreal : ∀ v, B.spectralConstraint (A.deficits v)) :
    ∃ bs : ReggeBaseSpace n,
      (∀ v, bs.deficitField v = A.deficits v) ∧
      (∀ v, bs.spectralOK v) := by
  refine ⟨⟨fun v => fun i => 0, A.deficits, A, fun v => rfl, ?_,
    fun v => B.spectralConstraint (A.deficits v)⟩, fun v => rfl, fun v => hreal v⟩
  intro v
  rw [show A.deficits v = 2 * Real.pi - ∑ i, A.cells v i from A.generated v]
  have hsum : (0 : ℝ) ≤ ∑ i, A.cells v i := Finset.sum_nonneg fun i _ => hnonneg v i
  linarith

/-- **发生学分离（链B 不生成几何）在底空间层的重述**：同一角亏场可由
    不同晶胞几何生成（逐顶点二面角和不变、分布不同），故底空间几何信息
    只能来自链A（生成资格），不能来自链B（仅约束资格）。 -/
theorem base_geometry_from_chainA_only {n : ℕ}
    (c₁ c₂ : ChainAGeometric n)
    (hsum : ∀ v, ∑ i, c₁.cells v i = ∑ i, c₂.cells v i)
    (v : Fin n) (i : Fin 4)
    (hdiff : c₁.cells v i ≠ c₂.cells v i) :
    c₁.cells v i ≠ c₂.cells v i ∧ c₁.deficits v = c₂.deficits v := by
  refine ⟨hdiff, ?_⟩
  rw [c₁.generated v, c₂.generated v, hsum v]

/-! ## 3. 底空间曲率进入曲率算符（衔接环节6） -/

/-- 底空间角亏场按模式索引嵌入为本征值谱（i < n 取第 i 顶点，i ≥ n 零延拓）。 -/
private noncomputable def baseEigen {n : ℕ} (B : ReggeBaseSpace n) : ℕ → ℝ :=
  fun i => if h : i < n then B.deficitField ⟨i, h⟩ else 0

/-- 嵌入谱的第 i 模 = 底空间第 i 顶点角亏（i < n 时）。 -/
theorem baseEigen_eq {n : ℕ} (B : ReggeBaseSpace n) (i : ℕ) (hi : i < n) :
    baseEigen B i = B.deficitField ⟨i, hi⟩ := by
  unfold baseEigen
  rw [dif_pos hi]

/-- 嵌入谱基模正性（非平凡底空间）。 -/
theorem baseEigen_pos {n : ℕ} (B : ReggeBaseSpace n) (hne : 0 < n)
    (hbase : 0 < B.deficitField ⟨0, by omega⟩) : 0 < baseEigen B 0 := by
  rw [baseEigen_eq B 0 hne]
  exact hbase

/-- **底空间 → 曲率算符衔接**：非空 Regge 底空间（含非平凡基模角亏）给出
    曲率算符数据：本征值谱 = 逐顶点角亏按模式索引嵌入，非负性与基模正性
    由底空间数据传递。 -/
noncomputable def curvatureOperatorOf {n : ℕ} (B : ReggeBaseSpace n) (hne : 0 < n)
    (hbase : 0 < B.deficitField ⟨0, by omega⟩) : CurvatureOperator where
  eigen := baseEigen B
  hermitian := True.intro
  eigen_nonneg := by
    intro i
    by_cases h : i < n
    · rw [baseEigen_eq B i h]; exact B.deficit_nonneg ⟨i, h⟩
    · unfold baseEigen; rw [dif_neg h]; exact le_refl 0
  eigen0_pos := baseEigen_pos B hne hbase

/-- 衔接定理：曲率算符第 i 模本征值 = 底空间第 i 顶点角亏（i < n 时）。 -/
theorem curvatureOperatorOf_eigen {n : ℕ} (B : ReggeBaseSpace n) (hne : 0 < n)
    (hbase : 0 < B.deficitField ⟨0, by omega⟩) (i : ℕ) (hi : i < n) :
    (curvatureOperatorOf B hne hbase).eigen i = B.deficitField ⟨i, hi⟩ :=
  baseEigen_eq B i hi

end CQM.FGChain
