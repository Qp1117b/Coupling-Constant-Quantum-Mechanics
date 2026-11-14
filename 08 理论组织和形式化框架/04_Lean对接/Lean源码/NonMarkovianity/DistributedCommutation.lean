import NonMarkovianity.Basic
import CouplingSpace.Uncertainty

/-!
# 分布式不对易关系 (DistributedCommutation)

对应研究文档 `04 前沿研究/CQM_前沿研究_分布式不对易关系与非马尔可夫性.md`
§3.1（分布式不确定关系）与 §6.3（单节点胚与分布式构造）。

## 形式化内容

1. **对易子微积分**：`commutatorOp` 在左右两槽的加性、`ℂ`-齐性，
   以及有限和上的展开 `commutatorOp_sum_sum`；
2. **一般分布式关系**：若 `[Ĝ, L̂_i] = i c_i I`，则
   `[Ĝ, Σ_i L̂_i] = i (Σ_i c_i) I`（原文 §3.1 的 `Σ_i C_i = C`）；
3. **单节点胚 → 集体对**：若 `[û_i, p̂_j] = i δ_ij I`，则
   `[û_G, p̂_G] = i I`，其中 `û_G = (1/N)Σ_i û_i`、`p̂_G = Σ_j p̂_j`；
4. **相变量子标度**：`p̂_i = v̂_i/☯` 即 `v̂_i = ☯ p̂_i`，故
   `[û_G, Σ_i v̂_i] = i☯ I`；
5. **分布式不确定关系**：对广义 Robertson 不等式
   `[A,B] = i c I ⇒ ΔA·ΔB ≥ |c|/2` 取 `c = ☯`，得
   `Δû_G · Δ(Σ_i v̂_i) ≥ ☯/2`；
6. **`N = 1` 退化**：`N = 1` 时集体对退化为单节点对，与框架既有的
   一维海森堡对一致。

## 边界

- 本模块只形式化 §6.3 的**代数骨架**。多节点相容性、与非阿贝尔扇区的
  Casimir 阶梯衔接、`β` 在分布式情形下的定义，属文档 §8 的【待推】E4，
  未在此证明，也不以 `axiom` 冒充。
- 本模块不含任何数值校验。
-/

noncomputable section

open scoped InnerProductSpace
open scoped BigOperators

namespace CQM
namespace NonMarkovianity

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-! ## 1 对易子微积分 -/

/-- 零算符在左侧时对易子为零。 -/
theorem commutatorOp_zero_left (B : H →ₗ[ℂ] H) : commutatorOp 0 B = 0 := by
  ext x
  simp [commutatorOp]

/-- 对易子对左槽加性：`[A + A', B] = [A, B] + [A', B]`。 -/
theorem commutatorOp_add_left (A A' B : H →ₗ[ℂ] H) :
    commutatorOp (A + A') B = commutatorOp A B + commutatorOp A' B := by
  ext x
  simp only [commutatorOp, LinearMap.sub_apply, LinearMap.add_apply,
    LinearMap.comp_apply, map_add]
  abel

/-- 对易子对左槽 `ℂ`-齐性：`[c • A, B] = c • [A, B]`。 -/
theorem commutatorOp_smul_left (c : ℂ) (A B : H →ₗ[ℂ] H) :
    commutatorOp (c • A) B = c • commutatorOp A B := by
  ext x
  simp only [commutatorOp, LinearMap.sub_apply, LinearMap.smul_apply,
    LinearMap.comp_apply, map_smul]
  rw [← smul_sub]

/-- 对易子对右槽加性：`[A, B + B'] = [A, B] + [A, B']`。 -/
theorem commutatorOp_add_right (A B B' : H →ₗ[ℂ] H) :
    commutatorOp A (B + B') = commutatorOp A B + commutatorOp A B' := by
  ext x
  simp only [commutatorOp, LinearMap.sub_apply, LinearMap.add_apply,
    LinearMap.comp_apply, map_add]
  abel

/-- 对易子对右槽 `ℂ`-齐性：`[A, c • B] = c • [A, B]`。 -/
theorem commutatorOp_smul_right (c : ℂ) (A B : H →ₗ[ℂ] H) :
    commutatorOp A (c • B) = c • commutatorOp A B := by
  ext x
  simp only [commutatorOp, LinearMap.sub_apply, LinearMap.smul_apply,
    LinearMap.comp_apply, map_smul]
  rw [smul_sub]

/-- 双槽同时 `ℂ`-齐性：`[a • A, b • B] = (a * b) • [A, B]`。 -/
theorem commutatorOp_smul_smul (a b : ℂ) (A B : H →ₗ[ℂ] H) :
    commutatorOp (a • A) (b • B) = (a * b) • commutatorOp A B := by
  rw [commutatorOp_smul_left, commutatorOp_smul_right, smul_smul]

/-! ## 2 有限和上的展开 -/

/-- 对易子对左槽有限和展开：`[Σ_i A_i, B] = Σ_i [A_i, B]`。 -/
theorem commutatorOp_sum_left {ι : Type*} (s : Finset ι) (A : ι → H →ₗ[ℂ] H)
    (B : H →ₗ[ℂ] H) :
    commutatorOp (∑ i ∈ s, A i) B = ∑ i ∈ s, commutatorOp (A i) B := by
  classical
  refine Finset.induction_on s ?_ ?_
  · simpa using commutatorOp_zero_left B
  · intro a s ha ih
    rw [Finset.sum_insert ha, Finset.sum_insert ha, commutatorOp_add_left, ih]

/-- 对易子对右槽有限和展开：`[A, Σ_j B_j] = Σ_j [A, B_j]`。 -/
theorem commutatorOp_sum_right {κ : Type*} (s : Finset κ) (A : H →ₗ[ℂ] H)
    (B : κ → H →ₗ[ℂ] H) :
    commutatorOp A (∑ j ∈ s, B j) = ∑ j ∈ s, commutatorOp A (B j) := by
  classical
  refine Finset.induction_on s ?_ ?_
  · ext x
    simp [commutatorOp]
  · intro a s ha ih
    rw [Finset.sum_insert ha, Finset.sum_insert ha, commutatorOp_add_right, ih]

/-- 双有限和展开：`[Σ_i A_i, Σ_j B_j] = Σ_i Σ_j [A_i, B_j]`。 -/
theorem commutatorOp_sum_sum {ι κ : Type*} (s : Finset ι) (t : Finset κ)
    (A : ι → H →ₗ[ℂ] H) (B : κ → H →ₗ[ℂ] H) :
    commutatorOp (∑ i ∈ s, A i) (∑ j ∈ t, B j)
      = ∑ i ∈ s, ∑ j ∈ t, commutatorOp (A i) (B j) := by
  rw [commutatorOp_sum_left]
  exact Finset.sum_congr rfl fun i _ => commutatorOp_sum_right t (A i) B

/-- `Fin n` 上的双和形式，供后续物理构造直接使用。 -/
theorem commutatorOp_sum_fin {n : ℕ} (A B : Fin n → H →ₗ[ℂ] H) :
    commutatorOp (∑ i, A i) (∑ j, B j)
      = ∑ i, ∑ j, commutatorOp (A i) (B j) :=
  commutatorOp_sum_sum Finset.univ Finset.univ A B

/-! ## 3 一般分布式对易关系（原文 §3.1） -/

/-- **一般分布式对易关系**：若全局量 `Ĝ` 与各局部分布式量 `L̂_i` 满足
`[Ĝ, L̂_i] = i c_i I`，则 `[Ĝ, Σ_i L̂_i] = i (Σ_i c_i) I`。

这是原文 §3.1 中 `Σ_i C_i = C` 的代数内容：集体量的对易子由各节点
贡献相加，而非由单节点贡献复制。 -/
theorem distributed_commutation_general {n : ℕ} (G : H →ₗ[ℂ] H)
    (L : Fin n → H →ₗ[ℂ] H) (C : Fin n → ℂ)
    (h : ∀ i, commutatorOp G (L i) = (Complex.I * C i) • idOp) :
    commutatorOp G (∑ i, L i) = (Complex.I * ∑ i, C i) • idOp := by
  rw [commutatorOp_sum_right]
  simp only [h]
  rw [← Finset.sum_smul, ← Finset.mul_sum]

/-! ## 4 单节点胚与集体对（原文 §6.3） -/

/-- 全局集体对数耦合：`û_G = (1/N) Σ_i û_i`。 -/
noncomputable def collectiveCoupling {n : ℕ} (u : Fin n → H →ₗ[ℂ] H) : H →ₗ[ℂ] H :=
  ((n : ℂ)⁻¹) • ∑ i, u i

/-- 总固有时流速算符：`Σ_i v̂_i`，由单节点 `p̂_i = v̂_i/☯` 反解得
`v̂_i = ☯ p̂_i`，故 `Σ_i v̂_i = ☯ Σ_i p̂_i`。 -/
noncomputable def totalProperTimeFlow {n : ℕ} (p : Fin n → H →ₗ[ℂ] H) (C : ℝ) :
    H →ₗ[ℂ] H :=
  (C : ℂ) • ∑ i, p i

/-- 正则交叉对易关系：`[u_i, p_j] = i δ_ij I`。 -/
def CanonicalNodePair {n : ℕ} (u p : Fin n → H →ₗ[ℂ] H) : Prop :=
  ∀ i j : Fin n, commutatorOp (u i) (p j) =
    (if i = j then (Complex.I : ℂ) else 0) • idOp

/-- **集体对的对易子**：若各节点满足 `[u_i, p_j] = i δ_ij I`，则
`[Σ_i u_i, Σ_j p_j] = i N I`。 -/
theorem commutatorOp_canonical_sum {n : ℕ} (u p : Fin n → H →ₗ[ℂ] H)
    (hcanon : CanonicalNodePair u p) :
    commutatorOp (∑ i, u i) (∑ j, p j) = ((n : ℂ) * Complex.I) • idOp := by
  rw [commutatorOp_sum_fin]
  have hinner : ∀ i : Fin n, (∑ j, commutatorOp (u i) (p j)) =
      (Complex.I : ℂ) • idOp := by
    intro i
    rw [Finset.sum_congr rfl fun j _ => hcanon i j]
    rw [Finset.sum_eq_single i]
    · simp
    · intro j _ hji
      rw [if_neg fun h : i = j => hji h.symm]
      simp
    · intro hi
      exact absurd (Finset.mem_univ i) hi
  rw [Finset.sum_congr rfl fun i _ => hinner i]
  rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin]
  rw [← Nat.cast_smul_eq_nsmul ℂ n (Complex.I • idOp), smul_smul]

/-- **分布式对易关系（原文 §6.3）**：在单节点胚与相变量子标度下，
全局集体对数耦合与总固有时流速满足 `[û_G, Σ_i v̂_i] = i☯ I`。 -/
theorem distributed_commutation_relation {n : ℕ} (hn : 0 < n)
    (u p : Fin n → H →ₗ[ℂ] H) (hcanon : CanonicalNodePair u p) (C : ℝ) :
    commutatorOp (collectiveCoupling u) (totalProperTimeFlow p C) =
      (Complex.I * (C : ℂ)) • idOp := by
  have hnC : (n : ℂ) ≠ 0 := by
    exact_mod_cast (Nat.ne_of_gt hn)
  have hscalar : ((n : ℂ)⁻¹ * (C : ℂ)) * ((n : ℂ) * Complex.I) =
      Complex.I * (C : ℂ) := by
    calc
      ((n : ℂ)⁻¹ * (C : ℂ)) * ((n : ℂ) * Complex.I)
          = ((n : ℂ)⁻¹ * (n : ℂ)) * ((C : ℂ) * Complex.I) := by ring
      _ = 1 * ((C : ℂ) * Complex.I) := by rw [inv_mul_cancel₀ hnC]
      _ = Complex.I * (C : ℂ) := by ring
  have hsum : commutatorOp (∑ i, u i) (∑ j, p j) =
      ((n : ℂ) * Complex.I) • idOp :=
    commutatorOp_canonical_sum (u := u) (p := p) hcanon
  unfold collectiveCoupling totalProperTimeFlow
  rw [commutatorOp_smul_smul, hsum, smul_smul, hscalar]

/-! ## 5 Hermitian 性在构造下的封闭 -/

/-- 两个自伴算符之和自伴。 -/
theorem isHermitian_add (A B : H →ₗ[ℂ] H) (hA : IsHermitian A) (hB : IsHermitian B) :
    IsHermitian (A + B) := by
  intro x y
  simp only [LinearMap.add_apply, inner_add_left, inner_add_right]
  rw [hA x y, hB x y]

/-- 实标量倍保持自伴性。 -/
theorem isHermitian_smul_ofReal (c : ℝ) (A : H →ₗ[ℂ] H) (hA : IsHermitian A) :
    IsHermitian ((c : ℂ) • A) := by
  intro x y
  rw [LinearMap.smul_apply, LinearMap.smul_apply, inner_smul_left, inner_smul_right,
    hA x y]
  simp

/-- 有限和保持自伴性。 -/
theorem isHermitian_sum {ι : Type*} (s : Finset ι) (A : ι → H →ₗ[ℂ] H)
    (h : ∀ i ∈ s, IsHermitian (A i)) : IsHermitian (∑ i ∈ s, A i) := by
  classical
  induction s using Finset.induction_on with
  | empty =>
      intro x y
      simp
  | insert a s has ih =>
      rw [Finset.sum_insert has]
      exact isHermitian_add _ _ (h a (Finset.mem_insert_self a s))
        (ih fun i hi => h i (Finset.mem_insert_of_mem hi))

/-- 集体对数耦合在单节点自伴时自伴。 -/
theorem isHermitian_collectiveCoupling {n : ℕ} (u : Fin n → H →ₗ[ℂ] H)
    (hu : ∀ i, IsHermitian (u i)) : IsHermitian (collectiveCoupling u) := by
  have hsum : IsHermitian (∑ i, u i) :=
    isHermitian_sum Finset.univ u fun i _ => hu i
  have hcast : ((n : ℂ)⁻¹) = (((n : ℝ)⁻¹ : ℝ) : ℂ) := by
    have hnat : ((n : ℂ)) = (((n : ℝ) : ℂ)) := by norm_cast
    calc
      ((n : ℂ)⁻¹) = ((((n : ℝ) : ℂ))⁻¹) := by rw [hnat]
      _ = (((n : ℝ)⁻¹ : ℝ) : ℂ) := by rw [← Complex.ofReal_inv]
  unfold collectiveCoupling
  rw [hcast]
  exact isHermitian_smul_ofReal ((n : ℝ)⁻¹) _ hsum

/-- 总固有时流速在单节点自伴时自伴。 -/
theorem isHermitian_totalProperTimeFlow {n : ℕ} (p : Fin n → H →ₗ[ℂ] H) (C : ℝ)
    (hp : ∀ i, IsHermitian (p i)) : IsHermitian (totalProperTimeFlow p C) := by
  unfold totalProperTimeFlow
  exact isHermitian_smul_ofReal C _ (isHermitian_sum Finset.univ p fun i _ => hp i)

/-! ## 6 分布式不确定关系（原文 §6.3 的不等式） -/

/-- **分布式不确定关系**：在单节点胚、正则交叉对易关系与单节点自伴性下，
`Δû_G · Δ(Σ_i v̂_i) ≥ ☯/2`（`☯ > 0`）。

证明：由 `distributed_commutation_relation` 得 `[û_G, Σv̂] = i☯ I`，
代入广义 Robertson 不等式 `robertson_ccr_inequality_general`。 -/
theorem distributed_uncertainty {n : ℕ} (hn : 0 < n)
    (u p : Fin n → H →ₗ[ℂ] H) (hcanon : CanonicalNodePair u p)
    (hu : ∀ i, IsHermitian (u i)) (hp : ∀ i, IsHermitian (p i))
    (C : ℝ) (hC : 0 ≤ C) (ψ : H) (hψ : ‖ψ‖ = 1) :
    stdDev ψ (collectiveCoupling u) * stdDev ψ (totalProperTimeFlow p C) ≥ C / 2 := by
  have hCCR := distributed_commutation_relation hn u p hcanon C
  have hgen := robertson_ccr_inequality_general ψ hψ
    (collectiveCoupling u) (totalProperTimeFlow p C)
    (isHermitian_collectiveCoupling u hu)
    (isHermitian_totalProperTimeFlow p C hp) C hCCR
  rwa [abs_of_nonneg hC] at hgen

/-! ## 7 `N = 1` 退化（原文 §6.3 自洽条件 1） -/

/-- `N = 1` 时集体对数耦合等于单节点对数耦合。 -/
theorem collectiveCoupling_one (u : Fin 1 → H →ₗ[ℂ] H) :
    collectiveCoupling u = u 0 := by
  unfold collectiveCoupling
  rw [Fin.sum_univ_one]
  norm_num

/-- `N = 1` 时总固有时流速等于单节点流速（乘相变量子）。 -/
theorem totalProperTimeFlow_one (p : Fin 1 → H →ₗ[ℂ] H) (C : ℝ) :
    totalProperTimeFlow p C = (C : ℂ) • p 0 := by
  unfold totalProperTimeFlow
  rw [Fin.sum_univ_one]
/-- `N = 1` 时分布式对易关系退化为框架既有的单个一维海森堡对：
`[û, v̂] = i☯ I`。 -/
theorem distributed_commutation_one (u p : Fin 1 → H →ₗ[ℂ] H) (C : ℝ)
    (hcanon : CanonicalNodePair u p) :
    commutatorOp (u 0) ((C : ℂ) • p 0) = (Complex.I * (C : ℂ)) • idOp := by
  have h := distributed_commutation_relation (n := 1) (by norm_num) u p hcanon C
  rwa [collectiveCoupling_one, totalProperTimeFlow_one] at h

end NonMarkovianity
end CQM
