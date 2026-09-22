import GN.Basic
import CartanAlgebra.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Charpoly.Basic
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.LinearAlgebra.Matrix.ToLinearEquiv
import Mathlib.LinearAlgebra.Eigenspace.Basic
import Mathlib.LinearAlgebra.LinearIndependent.Basic

/-!
# §2 4-单纯形组合谱 (SimplexSpectrum)

公理化证明稿 §2.1 的形式化：4-单纯形的边-面关联结构、曲率算符
（组合 Laplacian）`M = EᵀE` 的谱，以及非空面元计数。

对应文档定理：2.1（A₄ 谱定理）、推论 2.1（面元总数 31）、
推论 2.2（迹 30）；并为 §8 构造 κ = (N_faces + ☯)/N_cycle
提供组合输入 `N_faces` / `N_cycle = Tr(M)`。

## 结构

- 边 = 顶点 2-子集，共 C(5,2) = 10 条
- 三角面 = 顶点 3-子集，共 C(5,3) = 10 个
- 边-面关联矩阵 `E`：`E_{f,e} = 1` 当且仅当 `e ⊆ f`
- 曲率算符 `M = EᵀE`：`M_{e,e'}` = 同时含 `e,e'` 的三角面数
- 谱 `σ(M) = {9^{(1)}, 4^{(4)}, 1^{(5)}}`，`Tr(M) = 30`，`Tr(M²) = 150`
- 非空面元总数 `N_faces = 31 = 2⁵ − 1`

## 诚实边界

- 谱分解的表示论路线（`10 = 1 ⊕ 4 ⊕ 5`，Schur 引理）引用
  Fulton & Harris (1991)，此处以显式矩阵的特征多项式计算闭合；
  迹、二阶矩与全一向量本征方程为直接组合验证。
- 三角面选取定向为顶点 3-子集；每条边属于 3 个三角面
  （余下 3 顶点各补 1 个），对角元为 3。

## 参考文献

- Fulton, W. & Harris, J. (1991). *Representation Theory*. GTM 129.
- Horak, D. & Jost, J. (2013). Spectra of combinatorial Laplace operators.
  *Adv. Math.* 244, 303–336.
- Duval, A. & Reiner, V. (2002). Shifted simplicial complexes are
  Laplacian integral. *Trans. AMS* 354, 4313–4344.
- ruster (2026). CNT 完整研究. Zenodo. DOI: 10.5281/zenodo.20804380.
- 证明稿：`04 前沿研究/CQM_前沿研究_GN第一性推导_公理化证明稿.md`
-/

open Matrix Finset
open scoped Matrix

namespace CQM
namespace GN

/-! ### 边与三角面的枚举（顶点为 `Fin 5` 的 2- / 3-子集） -/

/-- 4-单纯形的顶点数。 -/
noncomputable def vertexCount : ℕ := 5

/-- 边：顶点的 2-子集，按字典序枚举（共 10 条）。 -/
def simplexEdgesList : List (Fin 5 × Fin 5) :=
  [(0, 1), (0, 2), (0, 3), (0, 4),
   (1, 2), (1, 3), (1, 4),
   (2, 3), (2, 4),
   (3, 4)]

/-- 三角面：顶点的 3-子集，按字典序枚举（共 10 个）。 -/
def simplexTrianglesList : List (Fin 5 × Fin 5 × Fin 5) :=
  [(0, 1, 2), (0, 1, 3), (0, 1, 4),
   (0, 2, 3), (0, 2, 4),
   (0, 3, 4),
   (1, 2, 3), (1, 2, 4),
   (1, 3, 4),
   (2, 3, 4)]

/-- 边数 = 10 = C(5,2)。 -/
theorem simplexEdgesList_length : simplexEdgesList.length = 10 := by rfl

/-- 三角面数 = 10 = C(5,3)。 -/
theorem simplexTrianglesList_length : simplexTrianglesList.length = 10 := by rfl

/-- 边数 = C(5,2)。 -/
theorem simplexEdges_eq_choose : simplexEdgesList.length = Nat.choose 5 2 := by
  decide

/-- 三角面数 = C(5,3)。 -/
theorem simplexTriangles_eq_choose : simplexTrianglesList.length = Nat.choose 5 3 := by
  decide

/-! ### 边-面关联与曲率算符 `M = EᵀE`

`M_{e,e'}` = 同时包含边 `e` 与 `e'` 的三角面个数：

- `e = e'`：每条边补余下 3 个顶点之一，得 3 个三角面，对角元 = 3
- `e ∩ e' ≠ ∅` 且 `e ≠ e'`：两条共端点边张成唯一 3-顶点集，恰含于 1 个三角面
- `e ∩ e' = ∅`：4 个顶点无法嵌入三角面，贡献 0

因此 `M_{e,e'} ∈ {0,1,3}`，且对称。 -/
def edgeFaceMatrix : Matrix (Fin 10) (Fin 10) ℤ :=
  !![3, 1, 1, 1, 1, 1, 1, 0, 0, 0;
     1, 3, 1, 1, 1, 0, 0, 1, 1, 0;
     1, 1, 3, 1, 0, 1, 0, 1, 0, 1;
     1, 1, 1, 3, 0, 0, 1, 0, 1, 1;
     1, 1, 0, 0, 3, 1, 1, 1, 1, 0;
     1, 0, 1, 0, 1, 3, 1, 1, 0, 1;
     1, 0, 0, 1, 1, 1, 3, 0, 1, 1;
     0, 1, 1, 0, 1, 1, 0, 3, 1, 1;
     0, 1, 0, 1, 1, 0, 1, 1, 3, 1;
     0, 0, 1, 1, 0, 1, 1, 1, 1, 3]

/-- 曲率算符对称：`M = Mᵀ`。 -/
theorem edgeFaceMatrix_symm : edgeFaceMatrixᵀ = edgeFaceMatrix := by
  decide

/-- [推论 2.2 / 定理 2.1] 曲率算符的迹 = 30。

    对角元均为 3（每条边属于 3 个三角面），10 × 3 = 30。
    等价于边-面关联矩阵 `E` 中 1 的个数 = 10 个面 × 每面 3 边。 -/
theorem edgeFaceMatrix_trace_eq_30 : edgeFaceMatrix.trace = 30 := by
  native_decide

/-- [定理 2.1 的矩条件一] 迹 = 9·1 + 4·4 + 1·5（与谱重数一致）。 -/
theorem trace_matches_spectrum_moments :
    edgeFaceMatrix.trace = 9 + 4 * 4 + 1 * 5 := by
  rw [edgeFaceMatrix_trace_eq_30]
  norm_num

/-- [定理 2.1 的矩条件二] `Tr(M²) = 150 = 9² + 4²·4 + 1²·5`。 -/
theorem edgeFaceMatrix_trace_sq_eq_150 :
    (edgeFaceMatrix * edgeFaceMatrix).trace = 150 := by
  native_decide

/-- 二阶矩与谱重数一致：`81 + 64 + 5 = 150`。 -/
theorem trace_sq_matches_spectrum_moments :
    (edgeFaceMatrix * edgeFaceMatrix).trace = 9 ^ 2 + 4 ^ 2 * 4 + 1 ^ 2 * 5 := by
  rw [edgeFaceMatrix_trace_sq_eq_150]
  norm_num

/-! ### 全一向量本征方程 `M · 𝟙 = 9 · 𝟙`（平凡表示） -/

/-- 全 1 向量。 -/
def allOnesVec : Fin 10 → ℤ := fun _ => 1

/-- [定理 2.1(i)] 全一向量是本征值 9 的本征向量：

    每条边 `e` 有 `∑_{e' ∋ 共端点} M_{e,e'} = 3 + 6×1 = 9`，
    即（3 个共面邻接 + 3 个对角贡献的组合重写）行和恒为 9。
    由对称性，行和全为 9 等价于 `M · 𝟙 = 9 · 𝟙`。 -/
theorem edgeFaceMatrix_allOnes :
    ∀ i : Fin 10, ∑ j : Fin 10, edgeFaceMatrix i j * allOnesVec j = 9 := by
  intro i
  fin_cases i <;> native_decide

/-- 全一向量本征方程的矩阵形式：`M · 𝟙 = 9 · 𝟙`。 -/
theorem edgeFaceMatrix_mul_allOnes :
    edgeFaceMatrix.mulVec allOnesVec = fun _ => 9 := by
  funext i
  exact edgeFaceMatrix_allOnes i

/-- 平凡表示对应本征值 9（文档定理 2.1 步骤 (i)）。 -/
theorem eigenvalue_nine_exists : ∃ v : Fin 10 → ℤ,
    (∀ i, ∑ j, edgeFaceMatrix i j * v j = 9 * v i) ∧ v = allOnesVec := by
  refine ⟨allOnesVec, ?_, rfl⟩
  intro i
  have h := edgeFaceMatrix_allOnes i
  have hv : allOnesVec i = 1 := rfl
  rw [hv]
  rw [mul_comm]
  simpa [mul_one] using h

/-! ### 显式本征基与特征多项式

直接构造 10 个本征向量（λ = 9, 4, 1 各一组），证线性无关，
经 ℚ 上矩阵共轭把 `charpoly` 化为对角阵的特征多项式。
避免对 10×10 `Matrix.det` 做 `native_decide`（会栈溢出）。 -/

/-- 本征值 4 的本征向量 `gᵢ(S) = 5·[i ∈ S] − 2`（按边枚举；仅需 i = 0…3）。 -/
def gVec (i : Fin 4) : Fin 10 → ℤ := fun e =>
  match e.val, i.val with
  | 0, 0 | 0, 1 | 1, 0 | 1, 2 | 2, 0 | 2, 3 | 3, 0 => 3
  | 4, 1 | 4, 2 | 5, 1 | 5, 3 | 6, 1 => 3
  | 7, 2 | 7, 3 | 8, 2 | 9, 3 => 3
  | _, _ => -2

/-- 本征值 1 的本征向量：各 4-圈上的交替符号（缺顶点 `om`）。 -/
def cycVec (om : Fin 5) : Fin 10 → ℤ := fun e =>
  match om.val, e.val with
  | 4, 0 => 1 | 4, 2 => -1 | 4, 4 => -1 | 4, 7 => 1
  | 3, 0 => 1 | 3, 3 => -1 | 3, 4 => -1 | 3, 8 => 1
  | 2, 0 => 1 | 2, 3 => -1 | 2, 5 => -1 | 2, 9 => 1
  | 1, 1 => 1 | 1, 3 => -1 | 1, 7 => -1 | 1, 9 => 1
  | 0, 4 => 1 | 0, 6 => -1 | 0, 7 => -1 | 0, 9 => 1
  | _, _ => 0

/-- 谱对角值按列序：`9, 4,4,4,4, 1,1,1,1,1`。 -/
def eigValCol : Fin 10 → ℤ
  | ⟨0, _⟩ => 9
  | ⟨1, _⟩ | ⟨2, _⟩ | ⟨3, _⟩ | ⟨4, _⟩ => 4
  | _ => 1

/-- 本征基按 `Fin 10` 列排列：全 1、g₀…g₃、五个 4-圈。 -/
def colVec : Fin 10 → Fin 10 → ℤ
  | ⟨0, _⟩ => fun _ => 1
  | ⟨1, _⟩ => gVec 0
  | ⟨2, _⟩ => gVec 1
  | ⟨3, _⟩ => gVec 2
  | ⟨4, _⟩ => gVec 3
  | ⟨5, _⟩ => cycVec 0
  | ⟨6, _⟩ => cycVec 1
  | ⟨7, _⟩ => cycVec 2
  | ⟨8, _⟩ => cycVec 3
  | ⟨9, _⟩ => cycVec 4

/-- 本征基矩阵：第 `j` 列 = `colVec j`。 -/
def eigBasisMat : Matrix (Fin 10) (Fin 10) ℤ := fun i j => colVec j i

/-- 对角本征值矩阵。 -/
def eigDiag : Matrix (Fin 10) (Fin 10) ℤ := Matrix.diagonal eigValCol

theorem colVec_zero : colVec 0 = allOnesVec := rfl

theorem colVec_g (k : Fin 4) : colVec ⟨k.val + 1, by omega⟩ = gVec k := by
  fin_cases k <;> rfl

theorem colVec_cyc (l : Fin 5) : colVec ⟨l.val + 5, by omega⟩ = cycVec l := by
  fin_cases l <;> rfl

theorem eigValCol_zero : eigValCol 0 = 9 := rfl

theorem eigValCol_g (k : Fin 4) : eigValCol ⟨k.val + 1, by omega⟩ = 4 := by
  fin_cases k <;> rfl

theorem eigValCol_cyc (l : Fin 5) : eigValCol ⟨l.val + 5, by omega⟩ = 1 := by
  fin_cases l <;> rfl

/-- 各本征向量非零。 -/
theorem colVec_ne_zero : ∀ j : Fin 10, colVec j ≠ 0 := by
  native_decide

theorem gVec_ne_zero : ∀ k : Fin 4, gVec k ≠ 0 := by
  native_decide

theorem cycVec_ne_zero : ∀ l : Fin 5, cycVec l ≠ 0 := by
  native_decide

/-- 本征方程 `M · colVec j = eigValCol j · colVec j`（逐列）。 -/
theorem edgeFaceMatrix_colVec_eigen :
    ∀ j i : Fin 10,
      ∑ k, edgeFaceMatrix i k * colVec j k = eigValCol j * colVec j i := by
  intro j i
  fin_cases j <;> fin_cases i <;> native_decide

/-- 矩阵形式 `M · P = P · D`。 -/
theorem edgeFaceMatrix_mul_eigBasis :
    edgeFaceMatrix * eigBasisMat = eigBasisMat * eigDiag := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.diagonal_apply, eigBasisMat, eigDiag]
  calc ∑ x, edgeFaceMatrix i x * colVec j x
      = eigValCol j * colVec j i := edgeFaceMatrix_colVec_eigen j i
    _ = ∑ x, colVec x i * (if x = j then eigValCol x else 0) := by
        simp_rw [mul_ite, mul_zero]
        rw [Finset.sum_ite_eq' Finset.univ j]
        simp [mul_comm]

/-- λ=4 组：在边 0,1,2,4 上取值构成的 4×4 求值矩阵，行列式非零。 -/
def gEvalMat : Matrix (Fin 4) (Fin 4) ℤ := fun k i =>
  gVec i ((![0, 1, 2, 4] : Fin 4 → Fin 10) k)

theorem gEvalMat_det_ne_zero : gEvalMat.det ≠ 0 := by
  native_decide

/-- λ=1 组：在边 0,1,2,5,6 上取值构成的 5×5 求值矩阵，行列式非零。 -/
def cycEvalMat : Matrix (Fin 5) (Fin 5) ℤ := fun k i =>
  cycVec i ((![0, 1, 2, 5, 6] : Fin 5 → Fin 10) k)

theorem cycEvalMat_det_ne_zero : cycEvalMat.det ≠ 0 := by
  native_decide

/-- g₀…g₃ 线性无关。 -/
theorem gVec_linearIndependent : LinearIndependent ℤ (fun i : Fin 4 => gVec i) := by
  rw [linearIndependent_iff']
  intro s g hg j hj
  let ĝ : Fin 4 → ℤ := fun i => if i ∈ s then g i else 0
  have hs : ∀ i ∈ s, ĝ i = g i := fun i hi => if_pos hi
  have hsum : ∑ i ∈ Finset.univ, ĝ i • gVec i = 0 := by
    have h1 : ∑ i ∈ Finset.univ, ĝ i • gVec i = ∑ i ∈ s, ĝ i • gVec i :=
      (Finset.sum_subset (Finset.subset_univ s) fun i _ hi => by
        show (if i ∈ s then g i else 0) • gVec i = 0
        rw [if_neg hi, zero_smul]).symm
    have h2 : ∑ i ∈ s, ĝ i • gVec i = ∑ i ∈ s, g i • gVec i :=
      Finset.sum_congr rfl fun i hi => by rw [hs i hi]
    rw [h1, h2, hg]
  have hmul : gEvalMat *ᵥ (fun i => ĝ i) = 0 := by
    funext k
    have hcoord := congr_arg (fun v : Fin 10 → ℤ =>
      v ((![0, 1, 2, 4] : Fin 4 → Fin 10) k)) hsum
    simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Pi.zero_apply] at hcoord
    calc ∑ i : Fin 4, gEvalMat k i * ĝ i
        = ∑ i : Fin 4, ĝ i * gVec i ((![0, 1, 2, 4] : Fin 4 → Fin 10) k) := by
            refine Finset.sum_congr rfl fun i _ => ?_
            simp only [gEvalMat]
            ring
      _ = ∑ i : Fin 4, ĝ i • gVec i ((![0, 1, 2, 4] : Fin 4 → Fin 10) k) := by
            simp only [smul_eq_mul]
      _ = _ := hcoord
  have h0 : (fun i : Fin 4 => ĝ i) = 0 :=
    Matrix.eq_zero_of_mulVec_eq_zero gEvalMat_det_ne_zero hmul
  have h0j : ĝ j = 0 := congr_fun h0 j
  exact (hs j hj) ▸ h0j

/-- 4-圈向量线性无关。 -/
theorem cycVec_linearIndependent : LinearIndependent ℤ (fun i : Fin 5 => cycVec i) := by
  rw [linearIndependent_iff']
  intro s g hg j hj
  let ĝ : Fin 5 → ℤ := fun i => if i ∈ s then g i else 0
  have hs : ∀ i ∈ s, ĝ i = g i := fun i hi => if_pos hi
  have hsum : ∑ i ∈ Finset.univ, ĝ i • cycVec i = 0 := by
    have h1 : ∑ i ∈ Finset.univ, ĝ i • cycVec i = ∑ i ∈ s, ĝ i • cycVec i :=
      (Finset.sum_subset (Finset.subset_univ s) fun i _ hi => by
        show (if i ∈ s then g i else 0) • cycVec i = 0
        rw [if_neg hi, zero_smul]).symm
    have h2 : ∑ i ∈ s, ĝ i • cycVec i = ∑ i ∈ s, g i • cycVec i :=
      Finset.sum_congr rfl fun i hi => by rw [hs i hi]
    rw [h1, h2, hg]
  have hmul : cycEvalMat *ᵥ (fun i => ĝ i) = 0 := by
    funext k
    have hcoord := congr_arg (fun v : Fin 10 → ℤ =>
      v ((![0, 1, 2, 5, 6] : Fin 5 → Fin 10) k)) hsum
    simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Pi.zero_apply] at hcoord
    calc ∑ i : Fin 5, cycEvalMat k i * ĝ i
        = ∑ i : Fin 5, ĝ i * cycVec i ((![0, 1, 2, 5, 6] : Fin 5 → Fin 10) k) := by
            refine Finset.sum_congr rfl fun i _ => ?_
            simp only [cycEvalMat]
            ring
      _ = ∑ i : Fin 5, ĝ i • cycVec i ((![0, 1, 2, 5, 6] : Fin 5 → Fin 10) k) := by
            simp only [smul_eq_mul]
      _ = _ := hcoord
  have h0 : (fun i : Fin 5 => ĝ i) = 0 :=
    Matrix.eq_zero_of_mulVec_eq_zero cycEvalMat_det_ne_zero hmul
  have h0j : ĝ j = 0 := congr_fun h0 j
  exact (hs j hj) ▸ h0j

/-- `mulVecLin` 形式的本征向量（由逐列本征方程）。 -/
theorem mem_eigenspace_colVec (j : Fin 10) :
    colVec j ∈ Module.End.eigenspace edgeFaceMatrix.mulVecLin (eigValCol j) := by
  rw [Module.End.mem_eigenspace_iff]
  funext i
  simp only [Matrix.mulVecLin_apply, Matrix.mulVec, Pi.smul_apply, smul_eq_mul]
  exact edgeFaceMatrix_colVec_eigen j i

theorem hasEigenvector_colVec (j : Fin 10) :
    Module.End.HasEigenvector edgeFaceMatrix.mulVecLin (eigValCol j) (colVec j) :=
  ⟨mem_eigenspace_colVec j, colVec_ne_zero j⟩

/-- 三组本征空间两两不交（`disjoint_genEigenspace`）。 -/
theorem disjoint_eig_9_4 :
    Disjoint (Module.End.eigenspace edgeFaceMatrix.mulVecLin (9 : ℤ))
      (Module.End.eigenspace edgeFaceMatrix.mulVecLin (4 : ℤ)) :=
  Module.End.disjoint_genEigenspace edgeFaceMatrix.mulVecLin (by norm_num : (9:ℤ) ≠ 4) 1 1

theorem disjoint_eig_9_1 :
    Disjoint (Module.End.eigenspace edgeFaceMatrix.mulVecLin (9 : ℤ))
      (Module.End.eigenspace edgeFaceMatrix.mulVecLin (1 : ℤ)) :=
  Module.End.disjoint_genEigenspace edgeFaceMatrix.mulVecLin (by norm_num : (9:ℤ) ≠ 1) 1 1

theorem disjoint_eig_4_1 :
    Disjoint (Module.End.eigenspace edgeFaceMatrix.mulVecLin (4 : ℤ))
      (Module.End.eigenspace edgeFaceMatrix.mulVecLin (1 : ℤ)) :=
  Module.End.disjoint_genEigenspace edgeFaceMatrix.mulVecLin (by norm_num : (4:ℤ) ≠ 1) 1 1

theorem ones_in_eigenspace :
    allOnesVec ∈ Module.End.eigenspace edgeFaceMatrix.mulVecLin (9 : ℤ) := by
  have h := mem_eigenspace_colVec 0
  rwa [colVec_zero, eigValCol_zero] at h

theorem g_in_eigenspace (k : Fin 4) :
    gVec k ∈ Module.End.eigenspace edgeFaceMatrix.mulVecLin (4 : ℤ) := by
  have h := mem_eigenspace_colVec ⟨k.val + 1, by omega⟩
  rwa [colVec_g, eigValCol_g] at h

theorem cyc_in_eigenspace (l : Fin 5) :
    cycVec l ∈ Module.End.eigenspace edgeFaceMatrix.mulVecLin (1 : ℤ) := by
  have h := mem_eigenspace_colVec ⟨l.val + 5, by omega⟩
  rw [colVec_cyc, eigValCol_cyc] at h
  exact h

/-- Reindexing helper: `Fin 10` split as ones | g₀…g₃ | cyc₀…cyc₄. -/
def splitIdxAux : (n : ℕ) → n < 10 → Fin 1 ⊕ (Fin 4 ⊕ Fin 5)
  | 0, _ => Sum.inl 0
  | n + 1, h =>
    if hn : n < 4 then Sum.inr (Sum.inl ⟨n, hn⟩)
    else Sum.inr (Sum.inr ⟨n - 4, by omega⟩)

/-- `Fin 10` 的分组重标号（与 `colVec` 列序一致）。 -/
def splitIdx (j : Fin 10) : Fin 1 ⊕ (Fin 4 ⊕ Fin 5) :=
  splitIdxAux j.val j.isLt

/-- 按 ones | g's | cycles 分组的向量族。 -/
def colGrouped : Fin 1 ⊕ (Fin 4 ⊕ Fin 5) → (Fin 10 → ℤ) :=
  Sum.elim (fun _ => allOnesVec) (Sum.elim gVec cycVec)

theorem allOnesVec_ne_zero : allOnesVec ≠ 0 := by
  intro h
  have h1 := congr_fun h 0
  simp [allOnesVec] at h1

theorem splitIdx_injective : Function.Injective splitIdx := by
  intro a b hab
  fin_cases a <;> fin_cases b <;> simp [splitIdx, splitIdxAux] at hab ⊢

theorem colVec_eq_grouped : colVec = colGrouped ∘ splitIdx := by
  funext j i
  fin_cases j <;> fin_cases i <;> native_decide

theorem colGrouped_linearIndependent : LinearIndependent ℤ colGrouped := by
  delta colGrouped
  refine LinearIndependent.sum_type ?_ ?_ ?_
  · rw [linearIndependent_unique_iff]
    simpa using allOnesVec_ne_zero
  · refine LinearIndependent.sum_type gVec_linearIndependent cycVec_linearIndependent ?_
    exact Disjoint.mono
      (Submodule.span_le.2 (Set.range_subset_iff.2 fun i => g_in_eigenspace i))
      (Submodule.span_le.2 (Set.range_subset_iff.2 fun l => cyc_in_eigenspace l))
      disjoint_eig_4_1
  · have h1 : Submodule.span ℤ
        (Set.range (Sum.elim (fun _ : Fin 1 => allOnesVec) (Sum.elim gVec cycVec) ∘ Sum.inl)) ≤
        Module.End.eigenspace edgeFaceMatrix.mulVecLin (9 : ℤ) := by
      apply Submodule.span_le.2
      rintro a ⟨x, rfl⟩
      simp only [Function.comp_apply, Sum.elim_inl]
      exact ones_in_eigenspace
    have h2 : Submodule.span ℤ
        (Set.range (Sum.elim (fun _ : Fin 1 => allOnesVec) (Sum.elim gVec cycVec) ∘ Sum.inr)) ≤
        Module.End.eigenspace edgeFaceMatrix.mulVecLin (4 : ℤ) ⊔
        Module.End.eigenspace edgeFaceMatrix.mulVecLin (1 : ℤ) := by
      apply Submodule.span_le.2
      rintro a ⟨x, rfl⟩
      simp only [Function.comp_apply, Sum.elim_inr]
      cases x with
      | inl i => exact Submodule.mem_sup_left (g_in_eigenspace i)
      | inr l => exact Submodule.mem_sup_right (cyc_in_eigenspace l)
    have hd : Disjoint (Module.End.eigenspace edgeFaceMatrix.mulVecLin (9 : ℤ))
        (Module.End.eigenspace edgeFaceMatrix.mulVecLin (4 : ℤ) ⊔
         Module.End.eigenspace edgeFaceMatrix.mulVecLin (1 : ℤ)) := by
      refine Submodule.disjoint_def.mpr fun x hx hx' => ?_
      rw [Submodule.mem_sup] at hx'
      obtain ⟨y, hy4, z, hz1, rfl⟩ := hx'
      have e9 := Module.End.mem_eigenspace_iff.mp hx
      have e4 := Module.End.mem_eigenspace_iff.mp hy4
      have e1 := Module.End.mem_eigenspace_iff.mp hz1
      have h9 : (9 : ℤ) • (y + z) = (4 : ℤ) • y + (1 : ℤ) • z := by
        rw [← e9, map_add, e4, e1]
      have h58 : (5 : ℤ) • y + (8 : ℤ) • z = 0 := by
        rw [smul_add] at h9
        calc (5 : ℤ) • y + (8 : ℤ) • z
            = (9 : ℤ) • y + (9 : ℤ) • z - ((4 : ℤ) • y + (1 : ℤ) • z) := by abel
          _ = 0 := by rw [← h9]; abel
      have h20 : (20 : ℤ) • y + (8 : ℤ) • z = 0 := by
        have h2 := congr_arg edgeFaceMatrix.mulVecLin h58
        simp only [map_zero, map_add] at h2
        rw [map_smul, map_smul, e4, e1] at h2
        simp only [smul_smul, one_smul] at h2
        -- h2 : (5 * 4) • y + (8 * 1) • z = 0
        simpa using h2
      have h15y : (15 : ℤ) • y = 0 := by
        calc (15 : ℤ) • y
            = (20 : ℤ) • y + (8 : ℤ) • z - ((5 : ℤ) • y + (8 : ℤ) • z) := by abel
          _ = 0 - 0 := by rw [h20, h58]
          _ = 0 := by abel
      have hy0 : y = 0 := by
        funext i
        have hi := congr_fun h15y i
        simp only [Pi.smul_apply, smul_eq_mul, Pi.zero_apply] at hi
        exact (mul_eq_zero.mp hi).resolve_left (by norm_num)
      have hz0 : z = 0 := by
        have := h58
        rw [hy0, smul_zero, zero_add, smul_eq_zero] at this
        exact this.resolve_left (by norm_num)
      rw [hy0, hz0, add_zero]
    exact Disjoint.mono h1 h2 hd

/-- 三组向量合起来线性无关。 -/
theorem colVec_linearIndependent : LinearIndependent ℤ colVec := by
  rw [colVec_eq_grouped]
  exact LinearIndependent.comp colGrouped_linearIndependent _ splitIdx_injective

/-- 本征基矩阵可逆：`det P ≠ 0`（由列线性无关，避免 10×10 行列式求值）。 -/
theorem eigBasisMat_det_ne_zero : eigBasisMat.det ≠ 0 := by
  intro h
  obtain ⟨v, hvne, hv⟩ := exists_mulVec_eq_zero_iff.mpr h
  have hsum : ∑ j : Fin 10, v j • colVec j = 0 := by
    funext i
    have hi := congr_fun hv i
    simp only [Matrix.mulVec, dotProduct, eigBasisMat] at hi
    calc ∑ j, v j • colVec j i = ∑ j, colVec j i * v j := by
          refine Finset.sum_congr rfl fun j _ => by rw [smul_eq_mul, mul_comm]
      _ = 0 := hi
  have hcoeff := linearIndependent_iff'.mp colVec_linearIndependent Finset.univ v hsum
  have : v = 0 := funext fun j => hcoeff j (Finset.mem_univ j)
  exact hvne this

/-! ### ℚ 上对角化与特征多项式 -/

/-- ℤ → ℚ 逐项提升。 -/
def castQ (A : Matrix (Fin 10) (Fin 10) ℤ) : Matrix (Fin 10) (Fin 10) ℚ :=
  A.map (Int.castRingHom ℚ)

theorem castQ_det_ne_zero : (castQ eigBasisMat).det ≠ 0 := by
  intro h
  have h2 : (Int.castRingHom ℚ) eigBasisMat.det = 0 := by
    rw [RingHom.map_det]
    exact h
  have h3 : ((eigBasisMat.det : ℤ) : ℚ) = ((0 : ℤ) : ℚ) := by simpa using h2
  exact eigBasisMat_det_ne_zero (Int.cast_injective h3)

theorem castQ_isUnit : IsUnit (castQ eigBasisMat).det :=
  isUnit_iff_ne_zero.mpr castQ_det_ne_zero

theorem castQ_eigDiag : castQ eigDiag = Matrix.diagonal fun i => (eigValCol i : ℚ) := by
  simp only [castQ, eigDiag]
  exact diagonal_map (map_zero _)

theorem castQ_conj :
    castQ edgeFaceMatrix =
      castQ eigBasisMat * castQ eigDiag * (castQ eigBasisMat)⁻¹ := by
  have hmul : castQ edgeFaceMatrix * castQ eigBasisMat =
      castQ eigBasisMat * castQ eigDiag := by
    simp only [castQ]
    rw [← Matrix.map_mul, ← Matrix.map_mul, edgeFaceMatrix_mul_eigBasis]
  have hright : (castQ eigBasisMat) * (castQ eigBasisMat)⁻¹ = 1 :=
    Matrix.mul_nonsing_inv _ castQ_isUnit
  calc castQ edgeFaceMatrix
      = castQ edgeFaceMatrix * castQ eigBasisMat * (castQ eigBasisMat)⁻¹ := by
          rw [mul_assoc, hright, mul_one]
    _ = castQ eigBasisMat * castQ eigDiag * (castQ eigBasisMat)⁻¹ := by
          rw [hmul]

theorem castQ_charpoly_eq :
    (castQ edgeFaceMatrix).charpoly = (castQ eigDiag).charpoly := by
  rw [castQ_conj]
  calc (castQ eigBasisMat * castQ eigDiag * (castQ eigBasisMat)⁻¹).charpoly
      = (castQ eigBasisMat * (castQ eigDiag * (castQ eigBasisMat)⁻¹)).charpoly := by
          rw [mul_assoc]
    _ = ((castQ eigDiag * (castQ eigBasisMat)⁻¹) * castQ eigBasisMat).charpoly :=
          charpoly_mul_comm _ _
    _ = (castQ eigDiag * ((castQ eigBasisMat)⁻¹ * castQ eigBasisMat)).charpoly := by
          rw [← mul_assoc]
    _ = (castQ eigDiag * 1).charpoly := by
          rw [Matrix.nonsing_inv_mul _ castQ_isUnit]
    _ = (castQ eigDiag).charpoly := by rw [mul_one]

theorem castQ_eigDiag_charpoly :
    (castQ eigDiag).charpoly =
      ∏ i : Fin 10, (Polynomial.X - Polynomial.C ((eigValCol i : ℚ))) := by
  rw [castQ_eigDiag, charpoly_diagonal]

theorem eigVal_product_Q :
    ∏ i : Fin 10, (Polynomial.X - Polynomial.C ((eigValCol i : ℚ))) =
      (Polynomial.X - (9 : Polynomial ℚ)) * (Polynomial.X - (4 : Polynomial ℚ)) ^ 4 *
      (Polynomial.X - (1 : Polynomial ℚ)) ^ 5 := by
  let s9 : Finset (Fin 10) := {0}
  let s4 : Finset (Fin 10) := {1, 2, 3, 4}
  let s1 : Finset (Fin 10) := {5, 6, 7, 8, 9}
  have hdisj1 : Disjoint s9 (s4 ∪ s1) := by decide
  have hdisj2 : Disjoint s4 s1 := by decide
  have hunion : s9 ∪ (s4 ∪ s1) = Finset.univ := by decide
  rw [← hunion, Finset.prod_union hdisj1, Finset.prod_union hdisj2]
  have hp9 : ∏ i ∈ s9, (Polynomial.X - Polynomial.C ((eigValCol i : ℚ)))
      = (Polynomial.X - (9 : Polynomial ℚ)) := by
    simp only [s9, Finset.prod_singleton]
    simp [eigValCol]
    exact Polynomial.C_eq_natCast 9
  have hp4 : ∏ i ∈ s4, (Polynomial.X - Polynomial.C ((eigValCol i : ℚ)))
      = (Polynomial.X - (4 : Polynomial ℚ)) ^ 4 := by
    simp only [s4]
    have key : ∀ i ∈ ({1, 2, 3, 4} : Finset (Fin 10)),
        (Polynomial.X - Polynomial.C ((eigValCol i : ℚ)))
          = (Polynomial.X - (4 : Polynomial ℚ)) := by
      intro i hi
      simp only [Finset.mem_insert, Finset.mem_singleton] at hi
      rcases hi with rfl | rfl | rfl | rfl <;> simp [eigValCol]
      all_goals exact Polynomial.C_eq_natCast _
    rw [Finset.prod_congr rfl key]
    simp
  have hp1 : ∏ i ∈ s1, (Polynomial.X - Polynomial.C ((eigValCol i : ℚ)))
      = (Polynomial.X - (1 : Polynomial ℚ)) ^ 5 := by
    simp only [s1]
    have key : ∀ i ∈ ({5, 6, 7, 8, 9} : Finset (Fin 10)),
        (Polynomial.X - Polynomial.C ((eigValCol i : ℚ)))
          = (Polynomial.X - (1 : Polynomial ℚ)) := by
      intro i hi
      simp only [Finset.mem_insert, Finset.mem_singleton] at hi
      rcases hi with rfl | rfl | rfl | rfl | rfl <;> simp [eigValCol]
    rw [Finset.prod_congr rfl key]
    simp
  rw [hp9, hp4, hp1]
  ring

/-- [定理 2.1] 4-单纯形曲率算符的特征多项式
    `(X − 9)(X − 4)⁴(X − 1)⁵`。 -/
theorem edgeFaceMatrix_charpoly :
    edgeFaceMatrix.charpoly =
      (Polynomial.X - (9 : Polynomial ℤ)) * (Polynomial.X - (4 : Polynomial ℤ)) ^ 4 *
      (Polynomial.X - (1 : Polynomial ℤ)) ^ 5 := by
  refine Polynomial.map_injective (Int.castRingHom ℚ) Int.cast_injective ?_
  rw [← charpoly_map]
  show (castQ edgeFaceMatrix).charpoly = _
  rw [castQ_charpoly_eq, castQ_eigDiag_charpoly, eigVal_product_Q]
  simp only [Polynomial.map_mul, Polynomial.map_pow, Polynomial.map_sub,
    Polynomial.map_X, Polynomial.map_ofNat, Polynomial.map_one]


/-! ### 非空面元计数 `N_faces = 31 = 2⁵ − 1` -/

/-- 非空面元（各维面）计数分解：

    | 维 k | 面数 N_k = C(5, k+1) |
    |---|---|
    | 0（顶点） | C(5,1) = 5 |
    | 1（边）   | C(5,2) = 10 |
    | 2（三角） | C(5,3) = 10 |
    | 3（四面体）| C(5,4) = 5 |
    | 4（体）   | C(5,5) = 1 |
-/
theorem simplex_face_counts :
    Nat.choose 5 1 = 5 ∧
    Nat.choose 5 2 = 10 ∧
    Nat.choose 5 3 = 10 ∧
    Nat.choose 5 4 = 5 ∧
    Nat.choose 5 5 = 1 := by
  decide

/-- 非空面元总数 `N_faces = Σ_{k=1}^{5} C(5,k) = 31`。 -/
noncomputable def simplexNonemptyFaces : ℕ :=
  ∑ k ∈ Ico 1 6, Nat.choose 5 k

/-- [推论 2.1] 非空面元总数 = 31 = 2⁵ − 1。 -/
theorem simplexNonemptyFaces_eq_31 : simplexNonemptyFaces = 31 := by
  unfold simplexNonemptyFaces
  decide

/-- 二项式恒等：`Σ_{k=1}^{n} C(n,k) = 2ⁿ − 1`（`n = 5` 实例）。 -/
theorem simplexNonemptyFaces_eq_two_pow_sub_one :
    simplexNonemptyFaces = 2 ^ 5 - 1 := by
  rw [simplexNonemptyFaces_eq_31]
  norm_num

/-- 含空集的全部子集数 = `2⁵ = 32`（与非空面元 31 互补）。 -/
theorem simplex_all_subsets : ∑ k ∈ Finset.range 6, Nat.choose 5 k = 2 ^ 5 := by
  decide

/-! ### 与 CartanAlgebra 中 f-向量的衔接 -/

/-- 文档 f-向量 `(f₀,f₁,f₂,f₃) = (5,10,10,5)` 与本文件各维计数一致
    （4-单纯形的体 `f₄ = 1` 单独由 `simplex_face_counts` 给出）。 -/
theorem simplex_fVector_matches :
    (simplexVertices, simplexEdges, simplexFaces, simplexCells)
      = (5, 10, 10, 5) := by
  unfold simplexVertices simplexEdges simplexFaces simplexCells
  rfl

/-- `N_faces` 分解为 f-向量和加上 4-维体：`31 = 30 + 1`。 -/
theorem nonemptyFaces_eq_fVector_sum_add_one :
    simplexNonemptyFaces = simplexFVectorSum + 1 := by
  rw [simplexNonemptyFaces_eq_31, simplexFVectorSum_eq_30]

/-! ### κ 的组合构造（§8 衔接） -/

/-- [构造 8.1 的组合输入] κ 的分子中离散面元数 = `N_faces = 31`。 -/
theorem kappa_numerator_faces : simplexNonemptyFaces = 31 :=
  simplexNonemptyFaces_eq_31

/-- [构造 8.1 的组合输入] κ 的分母 = `N_cycle = Tr(M) = 30`
    （与 `SpectralGeometry.adeleCycle` 的数值对应由该库
    `simplexFVectorSum_eq_adeleCycle` 给出）。 -/
theorem kappa_denominator_trace : Int.toNat edgeFaceMatrix.trace = 30 := by
  rw [edgeFaceMatrix_trace_eq_30]
  rfl

end GN
end CQM
