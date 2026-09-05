import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic

/-!
# 不确定性关系 (Uncertainty Relation)

从耦合空间的正则对易关系 [û, p̂ᵤ] = i 推导
Robertson 不确定性关系。

## 核心定理
- **Robertson 不等式**：对于满足 CCR [A, B] = i·I 的自伴算子，
  ΔA · ΔB ≥ 1/2（ℏ=1 自然单位）

## 证明方法（Cauchy-Schwarz + 三角不等式）
1. 中心化算子 A₀ = A - ⟨A⟩, B₀ = B - ⟨B⟩
2. 令 z = ⟨A₀ψ, B₀ψ⟩，由 CCR 得 z - z̄ = i
3. 三角不等式：|z - z̄| ≤ 2|z| → |z| ≥ 1/2
4. Cauchy-Schwarz：|z| ≤ ‖A₀ψ‖·‖B₀ψ‖ = σ_A·σ_B
5. 因此 σ_A·σ_B ≥ 1/2

## 参考文献
- Robertson, H. P. (1929). "The Uncertainty Principle." Phys. Rev. 34, 163.
- ruster (2026). CNT 完整研究. Zenodo. DOI: 10.5281/zenodo.20804380.
-/

noncomputable section

open scoped InnerProductSpace

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-! ## 基本定义 -/

def expectation (ψ : H) (A : H →ₗ[ℂ] H) : ℂ := ⟪ψ, A ψ⟫_ℂ

def variance (ψ : H) (A : H →ₗ[ℂ] H) : ℝ :=
  ‖A ψ - (expectation ψ A) • ψ‖ ^ 2

noncomputable def stdDev (ψ : H) (A : H →ₗ[ℂ] H) : ℝ :=
  Real.sqrt (variance ψ A)

def commutatorOp (A B : H →ₗ[ℂ] H) : H →ₗ[ℂ] H := A ∘ₗ B - B ∘ₗ A

def IsHermitian (A : H →ₗ[ℂ] H) : Prop :=
  ∀ x y, ⟪A x, y⟫_ℂ = ⟪x, A y⟫_ℂ

def idOp : H →ₗ[ℂ] H := LinearMap.id

def centeredOp (ψ : H) (A : H →ₗ[ℂ] H) : H →ₗ[ℂ] H :=
  A - (expectation ψ A) • idOp

/-! ## 基本性质 -/

theorem variance_nonneg (ψ : H) (A : H →ₗ[ℂ] H) : variance ψ A ≥ 0 := by
  unfold variance; apply pow_two_nonneg

theorem stdDev_nonneg (ψ : H) (A : H →ₗ[ℂ] H) : stdDev ψ A ≥ 0 :=
  Real.sqrt_nonneg _

theorem stdDev_sq_eq_variance (ψ : H) (A : H →ₗ[ℂ] H) :
    (stdDev ψ A) ^ 2 = variance ψ A := by
  unfold stdDev; rw [Real.sq_sqrt (variance_nonneg ψ A)]

theorem centeredOp_apply (ψ : H) (A : H →ₗ[ℂ] H) :
    centeredOp ψ A ψ = A ψ - (expectation ψ A) • ψ := by
  unfold centeredOp idOp; simp

/-! ## 归一化态的内积 -/

/-- 辅助引理：归一化态的自内积 = 1（ℂ 值） -/
theorem inner_self_one_of_norm_one (ψ : H) (hψ : ‖ψ‖ = 1) :
    ⟪ψ, ψ⟫_ℂ = (1 : ℂ) := by
  calc
    ⟪ψ, ψ⟫_ℂ = ((‖ψ‖ : ℂ) ^ 2) := inner_self_eq_norm_sq_to_K ψ
    _ = ((1 : ℝ) : ℂ) ^ 2 := by rw [hψ]
    _ = (1 : ℂ) := by norm_num

/-! ## Hermitian 算子的期望值是实数 -/

theorem expectation_real_of_hermitian (ψ : H) (A : H →ₗ[ℂ] H) (hA : IsHermitian A) :
    star (expectation ψ A) = expectation ψ A := by
  unfold expectation
  calc
    star (⟪ψ, A ψ⟫_ℂ) = ⟪A ψ, ψ⟫_ℂ := by
      simp [inner_conj_symm (A ψ) ψ]
    _ = ⟪ψ, A ψ⟫_ℂ := by rw [hA ψ ψ]

/-! ## 中心化算子的基本性质 -/

theorem expectation_centeredOp_eq_zero (ψ : H) (A : H →ₗ[ℂ] H) (hψ : ‖ψ‖ = 1) :
    expectation ψ (centeredOp ψ A) = 0 := by
  unfold expectation centeredOp idOp
  simp only [LinearMap.sub_apply, LinearMap.smul_apply, LinearMap.id_apply,
    inner_sub_right, inner_smul_right]
  -- Goal: ⟪ψ, A ψ⟫_ℂ - (expectation ψ A) * ⟪ψ, ψ⟫_ℂ = 0
  unfold expectation
  -- Goal: ⟪ψ, A ψ⟫_ℂ - ⟪ψ, A ψ⟫_ℂ * ⟪ψ, ψ⟫_ℂ = 0
  have h_inner : ⟪ψ, ψ⟫_ℂ = (1 : ℂ) := inner_self_one_of_norm_one ψ hψ
  rw [h_inner]
  simp

theorem variance_centeredOp_eq (ψ : H) (A : H →ₗ[ℂ] H) (hψ : ‖ψ‖ = 1) :
    variance ψ (centeredOp ψ A) = variance ψ A := by
  unfold variance centeredOp idOp expectation
  have h_inner : ⟪ψ, ψ⟫_ℂ = (1 : ℂ) := inner_self_one_of_norm_one ψ hψ
  simp only [LinearMap.sub_apply, LinearMap.smul_apply, LinearMap.id_apply,
    inner_sub_right, inner_smul_right]
  rw [h_inner]
  simp

theorem commutatorOp_centeredOp_eq (ψ : H) (A B : H →ₗ[ℂ] H) :
    commutatorOp (centeredOp ψ A) (centeredOp ψ B) = commutatorOp A B := by
  unfold commutatorOp centeredOp idOp
  ext x
  simp only [LinearMap.sub_apply, LinearMap.smul_apply, LinearMap.comp_apply,
    LinearMap.id_apply, LinearMap.map_sub, LinearMap.map_smul]
  -- Expand the expression and cancel terms algebraically
  -- LHS = (A(Bx) - eA·Bx - eB·Ax + eA·eB·x) - (B(Ax) - eB·Ax - eA·Bx + eB·eA·x)
  -- Since eA and eB are scalars (ℂ), they commute: eA·eB = eB·eA
  -- All terms cancel except A(Bx) - B(Ax)
  have h_smul_comm : (expectation ψ A : ℂ) • (expectation ψ B : ℂ) • x =
      (expectation ψ B : ℂ) • (expectation ψ A : ℂ) • x := by
    simp [smul_smul, mul_comm]
  -- Use abel for the additive commutative group structure of H
  abel_nf
  simp [h_smul_comm]

theorem IsHermitian_centeredOp (ψ : H) (A : H →ₗ[ℂ] H) (hA : IsHermitian A) :
    IsHermitian (centeredOp ψ A) := by
  unfold IsHermitian centeredOp idOp
  intro x y
  have h_real : star (expectation ψ A) = expectation ψ A :=
    expectation_real_of_hermitian ψ A hA
  simp only [LinearMap.sub_apply, LinearMap.smul_apply, LinearMap.id_apply,
    inner_sub_left, inner_smul_left, inner_sub_right, inner_smul_right]
  calc
    ⟪A x, y⟫_ℂ - (starRingEnd ℂ) (expectation ψ A) * ⟪x, y⟫_ℂ
        = ⟪A x, y⟫_ℂ - star (expectation ψ A) * ⟪x, y⟫_ℂ := by simp
    _ = ⟪A x, y⟫_ℂ - expectation ψ A * ⟪x, y⟫_ℂ := by rw [h_real]
    _ = ⟪x, A y⟫_ℂ - expectation ψ A * ⟪x, y⟫_ℂ := by rw [hA x y]

/-! ## Robertson 不确定性关系 — 核心定理 -/

/-- [THEOREM] Robertson 不确定性关系（CCR 特例）：
    对于满足正则对易关系 [A, B] = i·I 的 Hermitian 算子 A, B，
    和任意归一化态 ψ（‖ψ‖ = 1），有：
    ΔA · ΔB ≥ 1/2

    证明方法：Cauchy-Schwarz + 三角不等式。
    1. 构造中心化算子 A₀, B₀（其期望值为零，方差不变）
    2. 令 z = ⟨A₀ψ, B₀ψ⟩，由 CCR 得 z - z̄ = i
    3. 三角不等式：|z - z̄| ≤ 2|z| → |z| ≥ 1/2
    4. Cauchy-Schwarz：|z| ≤ ‖A₀ψ‖·‖B₀ψ‖ = σ_A·σ_B
    5. 因此 σ_A·σ_B ≥ 1/2 -/
theorem robertson_ccr_inequality (ψ : H) (hψ : ‖ψ‖ = 1) (A B : H →ₗ[ℂ] H)
    (hA : IsHermitian A) (hB : IsHermitian B)
    (hCCR : commutatorOp A B = (Complex.I : ℂ) • idOp) :
    stdDev ψ A * stdDev ψ B ≥ (1/2 : ℝ) := by
  -- 中心化算子
  let A₀ := centeredOp ψ A
  let B₀ := centeredOp ψ B
  have hA₀ : IsHermitian A₀ := IsHermitian_centeredOp ψ A hA
  have hB₀ : IsHermitian B₀ := IsHermitian_centeredOp ψ B hB
  have hCCR₀ : commutatorOp A₀ B₀ = (Complex.I : ℂ) • idOp := by
    rw [commutatorOp_centeredOp_eq ψ A B, hCCR]
  have h_inner_self : ⟪ψ, ψ⟫_ℂ = (1 : ℂ) := inner_self_one_of_norm_one ψ hψ

  -- 令 z = ⟨A₀ψ, B₀ψ⟩
  set z := ⟪A₀ ψ, B₀ ψ⟫_ℂ with hz

  -- 步骤 1：z - z̄ = i（从 CCR 导出）
  have h_conj_eq : star (⟪A₀ ψ, B₀ ψ⟫_ℂ) = ⟪B₀ ψ, A₀ ψ⟫_ℂ := by
    simp

  have h_z_sub_conj : z - star z = (Complex.I : ℂ) := by
    calc
      z - star z = ⟪A₀ ψ, B₀ ψ⟫_ℂ - star (⟪A₀ ψ, B₀ ψ⟫_ℂ) := rfl
      _ = ⟪A₀ ψ, B₀ ψ⟫_ℂ - ⟪B₀ ψ, A₀ ψ⟫_ℂ := by rw [h_conj_eq]
      _ = ⟪ψ, A₀ (B₀ ψ)⟫_ℂ - ⟪ψ, B₀ (A₀ ψ)⟫_ℂ := by rw [hA₀, hB₀]
      _ = ⟪ψ, (A₀ ∘ₗ B₀) ψ⟫_ℂ - ⟪ψ, (B₀ ∘ₗ A₀) ψ⟫_ℂ := by simp
      _ = ⟪ψ, ((A₀ ∘ₗ B₀) - (B₀ ∘ₗ A₀)) ψ⟫_ℂ := by
        rw [LinearMap.sub_apply, inner_sub_right]
      _ = ⟪ψ, (commutatorOp A₀ B₀) ψ⟫_ℂ := rfl
      _ = ⟪ψ, ((Complex.I : ℂ) • idOp) ψ⟫_ℂ := by rw [hCCR₀]
      _ = ⟪ψ, (Complex.I : ℂ) • ψ⟫_ℂ := by simp [idOp]
      _ = (Complex.I : ℂ) * ⟪ψ, ψ⟫_ℂ := by rw [inner_smul_right]
      _ = (Complex.I : ℂ) * (1 : ℂ) := by rw [h_inner_self]
      _ = (Complex.I : ℂ) := by simp

  -- 步骤 2：|z - z̄| = |i| = 1
  have h_norm_diff : ‖z - star z‖ = (1 : ℝ) := by
    rw [h_z_sub_conj]; simp

  -- 步骤 3：三角不等式 |z - z̄| ≤ |z| + |z̄| = 2|z|
  have h_norm_conj : ‖star z‖ = ‖z‖ := by simp
  have h_triangle : ‖z - star z‖ ≤ ‖z‖ + ‖star z‖ := norm_sub_le _ _
  rw [h_norm_conj, h_norm_diff] at h_triangle

  -- 步骤 4：|z| ≥ 1/2
  have h_abs_z_ge_half : (1/2 : ℝ) ≤ ‖z‖ := by linarith

  -- 步骤 5：Cauchy-Schwarz: |z| ≤ ‖A₀ψ‖·‖B₀ψ‖
  have h_cauchy : ‖z‖ ≤ ‖A₀ ψ‖ * ‖B₀ ψ‖ := by
    rw [hz]; exact norm_inner_le_norm (𝕜 := ℂ) (A₀ ψ) (B₀ ψ)

  -- 步骤 6：‖A₀ψ‖·‖B₀ψ‖ ≥ 1/2
  have h_norm_prod : ‖A₀ ψ‖ * ‖B₀ ψ‖ ≥ (1/2 : ℝ) := by linarith

  -- 步骤 7：联系方差和标准差
  have h_varA : variance ψ A = ‖A₀ ψ‖ ^ 2 := by
    dsimp [A₀, variance, centeredOp, idOp, expectation]
  have h_varB : variance ψ B = ‖B₀ ψ‖ ^ 2 := by
    dsimp [B₀, variance, centeredOp, idOp, expectation]
  have h_stdA : stdDev ψ A = ‖A₀ ψ‖ := by
    unfold stdDev; rw [h_varA, Real.sqrt_sq (norm_nonneg _)]
  have h_stdB : stdDev ψ B = ‖B₀ ψ‖ := by
    unfold stdDev; rw [h_varB, Real.sqrt_sq (norm_nonneg _)]
  rw [h_stdA, h_stdB]
  exact h_norm_prod

/-! ## CQM 耦合空间不确定性关系 -/

/-- [THEOREM] CQM 耦合空间不确定性关系（从 Robertson 不等式导出）：

    设 û 和 p̂ᵤ 是耦合空间中的正则共轭算符对，满足 [û, p̂ᵤ] = i·I，
    且均为 Hermitian 算子。则对于任意归一化量子态 ψ：

    Δû · Δp̂ᵤ ≥ 1/2

    这是 Robertson 不等式的直接推论（见 `robertson_ccr_inequality`）。 -/
theorem cqm_uncertainty_from_robertson (ψ : H) (hψ : ‖ψ‖ = 1)
    (uHat pHat : H →ₗ[ℂ] H) (hu : IsHermitian uHat) (hp : IsHermitian pHat)
    (hCCR : commutatorOp uHat pHat = (Complex.I : ℂ) • idOp) :
    stdDev ψ uHat * stdDev ψ pHat ≥ (1/2 : ℝ) :=
  robertson_ccr_inequality ψ hψ uHat pHat hu hp hCCR

/-- 无量纲化不确定性关系：
    定义 ũ = û/C（C > 0 为谱量子），则 Δũ · Δp̂ᵤ ≥ 1/(2C)。

    证明：Δũ = Δû/C（因为 stdDev 是 1-齐次的），
    所以 Δũ · Δp̂ᵤ = (Δû/C) · Δp̂ᵤ ≥ (1/2)/C = 1/(2C)。 -/
theorem dimensionless_uncertainty (ψ : H) (hψ : ‖ψ‖ = 1)
    (uHat pHat : H →ₗ[ℂ] H) (hu : IsHermitian uHat) (hp : IsHermitian pHat)
    (hCCR : commutatorOp uHat pHat = (Complex.I : ℂ) • idOp)
    (C : ℝ) (hCpos : C > 0) :
    (stdDev ψ uHat / C) * stdDev ψ pHat ≥ 1 / (2 * C) := by
  have h_robertson : stdDev ψ uHat * stdDev ψ pHat ≥ (1/2 : ℝ) :=
    robertson_ccr_inequality ψ hψ uHat pHat hu hp hCCR
  -- Rewrite LHS: (σ_u / C) * σ_p = (σ_u * σ_p) / C
  have h_div : (stdDev ψ uHat / C) * stdDev ψ pHat = (stdDev ψ uHat * stdDev ψ pHat) / C := by ring
  rw [h_div]
  -- Goal: (σ_u * σ_p) / C ≥ 1 / (2 * C)
  -- Since C > 0, multiply both sides by C:
  -- equivalent to σ_u * σ_p ≥ 1/2, which is h_robertson
  -- Use field_simp to clear denominators
  have hCpos' : (0 : ℝ) < C := hCpos
  -- Apply the inequality: if a ≥ b and c > 0, then a/c ≥ b/c
  -- We use: (1/2)/C ≤ (σ_u*σ_p)/C, and (1/2)/C = 1/(2*C)
  have h_key : (1/2 : ℝ) / C ≤ (stdDev ψ uHat * stdDev ψ pHat) / C := by
    -- Use mul_le_mul_of_nonneg_right with 1/C
    have h_inv_pos : (0 : ℝ) ≤ 1 / C := div_nonneg (by norm_num) (by linarith)
    -- Actually, we can use: a ≥ b → a/c ≥ b/c when c > 0
    -- This is equivalent to a * (1/c) ≥ b * (1/c), which follows from mul_le_mul_of_nonneg_right
    have h' : (stdDev ψ uHat * stdDev ψ pHat) * (1 / C) ≥ (1/2 : ℝ) * (1 / C) :=
      mul_le_mul_of_nonneg_right h_robertson h_inv_pos
    simpa using h'
  have h_eq : (1/2 : ℝ) / C = 1 / (2 * C) := by ring
  rw [h_eq] at h_key
  exact h_key

/-- [AXIOMATIC IDENTIFICATION] 耦合空间中的物理量对应关系：

    (ID1) Δu = Δr/⟨r⟩：耦合坐标不确定性 = 耦合强度相对不确定性
           （对小涨落在 u = ln r 附近成立，du = dr/r）

    (ID2) Δv_τ = C · Δp̂ᵤ：耦合速度不确定性 = C × 耦合动量不确定性
           （来自无量纲化 v_τ = du/dτ ↔ p̂ᵤ 的正则关系）

    这些对应关系目前在 CQM 中以公理形式引入，待从耦合空间
    的基本几何结构和动力学严格推导。 -/
structure CouplingIdentification where
  /-- Δu = Δr/⟨r⟩：耦合坐标涨落 = 耦合强度相对涨落 -/
  deltaU_eq_deltaR_div_r : Prop
  /-- Δv_τ = C · Δp̂ᵤ：耦合速度涨落 = C × 耦合动量涨落 -/
  deltaV_eq_C_times_deltaP : Prop

/-- [THEOREM — 条件性] 若接受耦合空间物理量对应关系，
    则 CQM 不确定性关系 (Δr/⟨r⟩)·Δv_τ ≥ C/2 成立。

    此定理将物理对应关系作为显式假设，使推导链透明化。
    当这些对应关系从耦合空间基本定义严格证明后，
    可将假设替换为对应关系的证明。 -/
theorem cqm_uncertainty_conditional
    (Δu Δp Δr_div_r Δvτ C : ℝ)
    (hCpos : C > 0)
    (h_robertson : Δu * Δp ≥ 1/2)
    (h_id1 : Δr_div_r = Δu)
    (h_id2 : Δvτ = C * Δp) :
    Δr_div_r * Δvτ ≥ C / 2 := by
  rw [h_id1, h_id2]
  -- Goal: Δu * (C * Δp) ≥ C / 2
  have h : Δu * (C * Δp) = C * (Δu * Δp) := by ring
  rw [h]
  -- Goal: C * (Δu * Δp) ≥ C / 2
  have h_mul : C * (Δu * Δp) ≥ C * (1/2 : ℝ) :=
    mul_le_mul_of_nonneg_left h_robertson (by linarith)
  -- Now C * (1/2) = C/2, so rewrite the RHS of h_mul
  have h_bound : C * (1/2 : ℝ) = C / 2 := by ring
  -- Rewrite h_bound in h_mul to match the goal
  rw [h_bound] at h_mul
  exact h_mul

/-!
## 已严格证明的定理（14 个）
- `variance_nonneg`：方差非负 ✅
- `stdDev_nonneg`：标准差非负 ✅
- `stdDev_sq_eq_variance`：标准差与方差的关系 ✅
- `centeredOp_apply`：中心化算子的作用 ✅
- `inner_self_one_of_norm_one`：归一化态的内积自等于 1 ✅
- `expectation_real_of_hermitian`：Hermitian 算子的期望值为实数 ✅
- `expectation_centeredOp_eq_zero`：中心化算子的期望值为零 ✅
- `variance_centeredOp_eq`：中心化不改变方差 ✅
- `commutatorOp_centeredOp_eq`：中心化不改变对易子 ✅
- `IsHermitian_centeredOp`：中心化保持 Hermitian 性 ✅
- **`robertson_ccr_inequality`**：Robertson 不等式 ΔA·ΔB ≥ 1/2 ✅
- **`cqm_uncertainty_from_robertson`**：CQM 不确定性关系（Robertson 直接推论）✅
- **`dimensionless_uncertainty`**：无量纲化不确定性关系 ✅
- **`cqm_uncertainty_conditional`**：条件性 CQM 不确定性关系（显式假设）✅

## 缺口状态
- 缺口 U1（不确定性关系证明）：✅ 完全解决，无 `sorry` 招留
- 缺口 U2：✅ 严格定理
-/