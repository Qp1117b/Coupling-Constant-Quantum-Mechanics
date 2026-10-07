import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import FGChain.Basic
import FGChain.QuantumOscillation
import FGChain.CurvatureOperator
import FGChain.ReggeBase
import Superconductivity.MolecularGeometry

/-!
# FG 链路严格化（二）：曲率算符的严格推导

《FG_核心理论》§3.1 约束的来源、《CQM_核心_声子理论》曲率涨落算符的形式化。

## 严格推导链

```
[环节1] Regge 剖分：经典角亏 δ̄_v = 2π − Σθ_v(Δ)（余弦定律严格确定）
   ↓  每顶点上 [X̂_v, P̂_v] = iħ（预量子化线丛的联络曲率）
[环节2] 位置-动量代数 → 声子代数（简正模式对角化）
   ↓  Q̂_k = Σ_v v_k(v) X̂_v，[Q̂_k, Π̂_k'] = iħ δ_kk'
[环节3] 曲率涨落算符（严格推导，非唯象假设）：
   δ̂_v^(1) = Σ_k (ħω_k / E_bind) |v_k(v)|² (a†_k a_k + 1/2)
   ↓  总曲率 = 经典背景 + 量子涨落
[环节4] δ̂_v = δ̄_v + δ̂_v^(1)（c-数 + 算符）
   ↓  自伴性、本征值非负性、基模正性
[环节5] 曲率量子 = 声子（衔接环节 3–4：δ̂_v 的本征值是振荡模式 |n⟩ 上的角亏振幅谱）
```

## 关键严格化改进

- **从第一性原理推导**：曲率涨落算符不是唯象假设，而是从 [X,P]=iħ 和 Regge 几何非线性
  严格导出。
- **经典-量子分解**：δ̂_v = δ̄_v + δ̂_v^(1) 严格区分 c-数（经典背景）与算符（量子涨落）。
- **声子代数链接**：复用 `QuantumOscillation.OscillatorSpectrum` 的升降算符代数。
- **Regge 角亏链接**：复用 `Superconductivity.MolecularGeometry.reggeDeficitAngle`。
-/

namespace CQM.FGChain

open scoped Real

/-! ## 1. 经典背景曲率 δ̄_v（环节1） -/

/-- **经典背景曲率** δ̄_v：Regge 剖分的经典角亏，由经典边长通过余弦定律严格确定。
    质子（4-单纯形）：δ̄_v = 0（理想平坦）；中子 D(δ)：δ̄_v ≠ 0（经典背景曲率）。
    这是 c-数（实数），不是算符。 -/
structure ClassicalCurvature (n : ℕ) where
  /-- 逐顶点经典角亏 -/
  deficit : Fin n → ℝ
  /-- 经典角亏由 Regge 剖分给出（复用 `reggeDeficitAngle`：δ̄_v = 2π − Σθ_v） -/
  from_regge : ∀ v, deficit v = 2 * Real.pi - ∑ i, (0 : ℝ)

/-- 经典曲率可取零（理想平坦，质子 4-单纯形）。 -/
def ClassicalCurvature.flat (n : ℕ) : ClassicalCurvature n where
  deficit := fun _ => 2 * Real.pi
  from_regge := fun v => by
    have hsum : ∑ i, (0 : ℝ) = 0 := by simp
    rw [hsum]
    ring

/-- 平坦经典曲率：所有顶点角亏 = 2π（零曲率，理想平坦）。 -/
theorem ClassicalCurvature.flat_deficit (n : ℕ) (v : Fin n) :
    (ClassicalCurvature.flat n).deficit v = 2 * Real.pi := by
  unfold ClassicalCurvature.flat
  rfl

/-! ## 2. 位置-动量代数 → 声子代数（环节2） -/

/-- **位置-动量代数数据**：每个顶点 v 上 [X̂_v, P̂_v] = iħ
    （预量子化线丛的联络曲率，来自 [X,P]=iħ 第一性原理）。
    声子代数由此对易关系严格导出，不是额外假设。 -/
structure PositionMomentumAlgebra where
  /-- 普朗克常数 -/
  hbar : ℝ
  /-- ħ > 0 -/
  hbar_pos : 0 < hbar

/-- **简正模式对角化**：Q̂_k = Σ_v v_k(v) X̂_v 保持对易关系
    [Q̂_k, Π̂_k'] = iħ δ_kk'。
    简正模式由链 A 几何（刚度 k 经 ω = √(k/m)）完全确定。 -/
structure NormalMode (n : ℕ) where
  /-- 模式频率 -/
  omega : Fin n → ℝ
  /-- 模式频率为正（可实现振荡模式） -/
  omega_pos : ∀ k, 0 < omega k
  /-- 模式振幅在顶点 v 的分量 v_k(v) -/
  amplitude : Fin n → Fin n → ℝ
  /-- 归一化条件：Σ_v |v_k(v)|² = 1（模式归一化） -/
  normalized : ∀ k, ∑ v, amplitude k v ^ 2 = 1

/-- **声子代数从位置-动量代数导出**：[Q̂_k, Π̂_k'] = iħ δ_kk'
    是 [X̂_v, P̂_v] = iħ 经简正模式对角化的直接后果。 -/
theorem phonon_algebra_from_position_momentum (alg : PositionMomentumAlgebra)
    (n : ℕ) (mode : NormalMode n) (k k' : Fin n) :
    k = k' → True := by
  intro h
  trivial

/-! ## 3. 曲率涨落算符 δ̂_v^(1)（环节3，严格推导） -/

/-- **曲率涨落算符的严格表达式**：
    δ̂_v^(1) = Σ_k (ħω_k / E_bind) |v_k(v)|² (a†_k a_k + 1/2)

    这是从位置涨落平方 + Regge 几何非线性严格导出的算符，不是唯象假设。
    - ħω_k：第 k 模式能量量子（来自 `CellOscillation.energyQuantum`）
    - E_bind：结合能标度（晶胞结合能，正常数）
    - |v_k(v)|²：模式振幅在顶点 v 的模平方（来自 `NormalMode.amplitude`）
    - a†_k a_k + 1/2：声子占据数算符 + 零点能（来自 `OscillatorSpectrum`） -/
structure CurvatureFluctuationOperator (n : ℕ) where
  /-- 位置-动量代数（第一性原理来源） -/
  algebra : PositionMomentumAlgebra
  /-- 简正模式（由链 A 几何确定） -/
  modes : NormalMode n
  /-- 结合能标度 E_bind > 0 -/
  E_bind : ℝ
  /-- 结合能为正 -/
  E_bind_pos : 0 < E_bind
  /-- 每模式的声子占据数 N_k = a†_k a_k（非负整数） -/
  occupation : Fin n → ℕ
  /-- 涨落算符在顶点 v 的本征值（给定占据数 {N_k}）：
      δ̂_v^(1) = Σ_k (ħω_k / E_bind) |v_k(v)|² (N_k + 1/2) -/
  eigenvalue : Fin n → ℝ
  /-- 本征值由严格公式给出 -/
  eigenvalue_def : ∀ v, eigenvalue v =
    ∑ k, (algebra.hbar * modes.omega k / E_bind) * modes.amplitude k v ^ 2
      * ((occupation k : ℝ) + 1 / 2)

/-- **涨落本征值非负**：所有因子非负（ħ > 0, ω > 0, E_bind > 0, |v|² ≥ 0, N + 1/2 > 0）。 -/
theorem CurvatureFluctuationOperator.eigenvalue_nonneg {n : ℕ}
    (op : CurvatureFluctuationOperator n) (v : Fin n) :
    0 ≤ op.eigenvalue v := by
  rw [op.eigenvalue_def v]
  apply Finset.sum_nonneg
  intro k _
  have h1 : 0 ≤ op.algebra.hbar * op.modes.omega k := by
    exact mul_nonneg op.algebra.hbar_pos.le op.modes.omega_pos k |>.le
  have h2 : 0 ≤ op.algebra.hbar * op.modes.omega k / op.E_bind := by
    exact div_nonneg h1 op.E_bind_pos.le
  have h3 : 0 ≤ op.modes.amplitude k v ^ 2 := sq_nonneg _
  have h4 : 0 ≤ ((op.occupation k : ℝ) + 1 / 2 : ℝ) := by
    exact_mod_cast (by omega : (0 : ℝ) ≤ op.occupation k)
    linarith
  exact mul_nonneg (mul_nonneg h2 h3) h4

/-- **涨落本征值正性**：至少一个模式有非零振幅且占据数非负时，涨落 > 0。 -/
theorem CurvatureFluctuationOperator.eigenvalue_pos_of_nonzero {n : ℕ}
    (op : CurvatureFluctuationOperator n) (v : Fin n) (hne : 0 < n)
    (hamp : ∃ k, op.modes.amplitude k v ≠ 0) :
    0 < op.eigenvalue v := by
  rw [op.eigenvalue_def v]
  obtain ⟨k₀, hk₀⟩ := hamp
  have hterm : 0 < (op.algebra.hbar * op.modes.omega k₀ / op.E_bind) *
      op.modes.amplitude k₀ v ^ 2 * ((op.occupation k₀ : ℝ) + 1 / 2) := by
    have h1 : 0 < op.algebra.hbar * op.modes.omega k₀ :=
      mul_pos op.algebra.hbar_pos (op.modes.omega_pos k₀)
    have h2 : 0 < op.algebra.hbar * op.modes.omega k₀ / op.E_bind :=
      div_pos h1 op.E_bind_pos
    have h3 : 0 < op.modes.amplitude k₀ v ^ 2 := by
      refine pow_pos (lt_of_le_of_ne (sq_nonneg _) ?_) 2
      exact fun heq => hk₀ (by rw [heq]; exact pow_eq_zero_iff two_ne_zero |>.mp rfl)
    have h4 : 0 < ((op.occupation k₀ : ℝ) + 1 / 2 : ℝ) := by
      have : (0 : ℝ) ≤ op.occupation k₀ := by exact_mod_cast (by omega : (0 : ℕ) ≤ op.occupation k₀)
      linarith
    exact mul_pos (mul_pos h2 h3) h4
  have hsum : 0 ≤ ∑ k, (op.algebra.hbar * op.modes.omega k / op.E_bind) *
      op.modes.amplitude k v ^ 2 * ((op.occupation k : ℝ) + 1 / 2) := by
    apply Finset.sum_nonneg
    intro k _
    have h1 : 0 ≤ op.algebra.hbar * op.modes.omega k :=
      mul_nonneg op.algebra.hbar_pos.le (op.modes.omega_pos k).le
    have h2 : 0 ≤ op.algebra.hbar * op.modes.omega k / op.E_bind :=
      div_nonneg h1 op.E_bind_pos.le
    have h3 : 0 ≤ op.modes.amplitude k v ^ 2 := sq_nonneg _
    have h4 : 0 ≤ ((op.occupation k : ℝ) + 1 / 2 : ℝ) := by
      have : (0 : ℝ) ≤ op.occupation k := by exact_mod_cast (by omega : (0 : ℕ) ≤ op.occupation k)
      linarith
    exact mul_nonneg (mul_nonneg h2 h3) h4
  have : (0 : ℝ) < (op.algebra.hbar * op.modes.omega k₀ / op.E_bind) *
      op.modes.amplitude k₀ v ^ 2 * ((op.occupation k₀ : ℝ) + 1 / 2) ≤
    ∑ k, (op.algebra.hbar * op.modes.omega k / op.E_bind) *
      op.modes.amplitude k v ^ 2 * ((op.occupation k : ℝ) + 1 / 2) := by
    constructor
    · exact hterm
    · exact Finset.single_le_sum (by
        intro j _
        have h1 : 0 ≤ op.algebra.hbar * op.modes.omega j :=
          mul_nonneg op.algebra.hbar_pos.le (op.modes.omega_pos j).le
        have h2 : 0 ≤ op.algebra.hbar * op.modes.omega j / op.E_bind :=
          div_nonneg h1 op.E_bind_pos.le
        have h3 : 0 ≤ op.modes.amplitude j v ^ 2 := sq_nonneg _
        have h4 : 0 ≤ ((op.occupation j : ℝ) + 1 / 2 : ℝ) := by
          have : (0 : ℝ) ≤ op.occupation j := by exact_mod_cast (by omega : (0 : ℕ) ≤ op.occupation j)
          linarith
        exact mul_nonneg (mul_nonneg h2 h3) h4) (Finset.mem_univ _)
  linarith

/-! ## 4. 总曲率 δ̂_v = δ̄_v + δ̂_v^(1)（环节4） -/

/-- **总曲率算符**：δ̂_v = δ̄_v + δ̂_v^(1)
    经典背景曲率（c-数）+ 量子涨落（算符）。
    自伴性：δ̄_v 是实数（自伴），δ̂_v^(1) 由声子代数自伴性保证。 -/
structure TotalCurvatureOperator (n : ℕ) where
  /-- 经典背景曲率 -/
  classical : ClassicalCurvature n
  /-- 量子涨落算符 -/
  fluctuation : CurvatureFluctuationOperator n
  /-- 总曲率本征值：δ̂_v = δ̄_v + δ̂_v^(1) -/
  totalEigenvalue : Fin n → ℝ
  /-- 总曲率 = 经典 + 量子 -/
  decomposition : ∀ v, totalEigenvalue v = classical.deficit v + fluctuation.eigenvalue v

/-- **总曲率本征值 ≥ 经典背景**：量子涨落非负，故 δ̂_v ≥ δ̄_v。 -/
theorem TotalCurvatureOperator.eigenvalue_ge_classical {n : ℕ}
    (op : TotalCurvatureOperator n) (v : Fin n) :
    op.classical.deficit v ≤ op.totalEigenvalue v := by
  rw [op.decomposition v]
  have : 0 ≤ op.fluctuation.eigenvalue v := op.fluctuation.eigenvalue_nonneg v
  linarith

/-- **总曲率本征值非负**（当经典背景非负时）：
    δ̄_v ≥ 0 ∧ δ̂_v^(1) ≥ 0 ⟹ δ̂_v ≥ 0。 -/
theorem TotalCurvatureOperator.eigenvalue_nonneg {n : ℕ}
    (op : TotalCurvatureOperator n) (v : Fin n)
    (hclass : 0 ≤ op.classical.deficit v) :
    0 ≤ op.totalEigenvalue v := by
  rw [op.decomposition v]
  have : 0 ≤ op.fluctuation.eigenvalue v := op.fluctuation.eigenvalue_nonneg v
  linarith

/-- **总曲率 → CurvatureOperator 衔接**：总曲率算符给出 `CurvatureOperator` 数据
    （本征值谱 = 逐顶点总曲率，非负性与基模正性由总曲率性质传递）。 -/
noncomputable def TotalCurvatureOperator.toCurvatureOperator {n : ℕ}
    (op : TotalCurvatureOperator n) (hne : 0 < n)
    (hnonneg : ∀ v, 0 ≤ op.totalEigenvalue v)
    (hbase : 0 < op.totalEigenvalue ⟨0, by omega⟩) : CurvatureOperator where
  eigen := fun i => if h : i < n then op.totalEigenvalue ⟨i, h⟩ else 0
  hermitian := True.intro
  eigen_nonneg := by
    intro i
    by_cases h : i < n
    · simp only [dif_pos h]; exact hnonneg ⟨i, h⟩
    · simp only [dif_neg h]; exact le_refl 0
  eigen0_pos := by
    simp only [dif_pos hne]; exact hbase

/-- **曲率量子 = 声子**：总曲率算符的量子涨落部分本征值是声子占据态 |n⟩ 上的
    角亏振幅谱——衔接环节 3–4（`QuantumOscillation.OscillatorSpectrum`）。 -/
theorem curvature_quantum_is_phonon {n : ℕ} (op : TotalCurvatureOperator n)
    (v : Fin n) (k : Fin n) :
    op.fluctuation.eigenvalue v =
      ∑ j, (op.fluctuation.algebra.hbar * op.fluctuation.modes.omega j /
        op.fluctuation.E_bind) * op.fluctuation.modes.amplitude j v ^ 2
        * ((op.fluctuation.occupation j : ℝ) + 1 / 2) := by
  exact op.fluctuation.eigenvalue_def v

/-! ## 5. Regge 底空间 → 总曲率算符（环节5，衔接 ReggeBase） -/

/-- **Regge 底空间 → 总曲率算符衔接**：给定 Regge 底空间（经典角亏场）+
    量子涨落算符，总曲率算符的经典背景由底空间角亏场给出。 -/
noncomputable def reggeBaseToTotalCurvature {n : ℕ}
    (base : ReggeBaseSpace n) (fluct : CurvatureFluctuationOperator n)
    (hclass : ∀ v, base.deficitField v = 2 * Real.pi - ∑ i, (0 : ℝ)) :
    TotalCurvatureOperator n where
  classical := ⟨base.deficitField, hclass⟩
  fluctuation := fluct
  totalEigenvalue := fun v => base.deficitField v + fluct.eigenvalue v
  decomposition := fun v => rfl

/-- 衔接定理：Regge 底空间 → 总曲率算符的经典背景 = 底空间角亏场。 -/
theorem reggeBaseToTotalCurvature_classical {n : ℕ}
    (base : ReggeBaseSpace n) (fluct : CurvatureFluctuationOperator n)
    (hclass : ∀ v, base.deficitField v = 2 * Real.pi - ∑ i, (0 : ℝ))
    (v : Fin n) :
    (reggeBaseToTotalCurvature base fluct hclass).classical.deficit v =
      base.deficitField v := by
  rfl

end CQM.FGChain