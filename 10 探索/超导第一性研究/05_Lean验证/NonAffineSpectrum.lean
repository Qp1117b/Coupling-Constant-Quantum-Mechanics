/-
  第 137 轮：非仿射刚度的谱与截断位置
  ==========================================================================
  承接 R145（im Ã ⊆ N_I，顶点谱贡献恒零）。本轮把非仿射刚度化简为

      H_{ee'} = -∂ω_e/∂ℓ_{e'} = ∂ε_e/∂ℓ_{e'} = Ã_{ee'}   （平直背景，ω_e ≡ ε_e）

  故非仿射刚度谱 = Ã 的奇异值谱。本文件只承载谱的纯代数骨架：

    * 非负序列的平方和 ≤ 和的平方（初等，供参与比下界用）；
    * 参与比 PR = (Σσ²)²/Σσ⁴ 满足 1 ≤ PR ≤ r（Cauchy–Schwarz），全等谱给 PR = r；
    * 方差可按"强模／弱模"分解（不重不漏）；
    * 上缘有界 ⇒ 截断存在；ω_cut = √(σ_max/M) 对 M 严格减。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Algebra.Module.Basic
import Mathlib.Algebra.Module.BigOperators
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Order.Basic

open scoped BigOperators

namespace CQM.NonAffineSpectrum

/-! ### 一、总权重 -/

/-- 谱的总权重 $\sum_k\sigma_k^2$（与 $\tilde A$ 的 Frobenius 范数平方对应）。 -/
noncomputable def totalSq {ι : Type*} (s : Finset ι) (σ : ι → ℝ) : ℝ :=
  ∑ k ∈ s, σ k ^ 2

/-- 总权重非负。 -/
lemma totalSq_nonneg {ι : Type*} (s : Finset ι) (σ : ι → ℝ) :
    0 ≤ totalSq s σ := by
  unfold totalSq
  exact Finset.sum_nonneg (fun k _ => sq_nonneg (σ k))

/-- 有非零模则总权重严格正。 -/
lemma totalSq_pos {ι : Type*} (s : Finset ι) (σ : ι → ℝ)
    (k0 : ι) (hk0 : k0 ∈ s) (hσ : σ k0 ≠ 0) :
    0 < totalSq s σ := by
  unfold totalSq
  have hterm : 0 < σ k0 ^ 2 := by positivity
  have hle : σ k0 ^ 2 ≤ ∑ k ∈ s, σ k ^ 2 :=
    Finset.single_le_sum (fun k _ => sq_nonneg (σ k)) hk0
  linarith

/-- 非负序列的平方和不超过和的平方：$\sum x^2\le(\sum x)^2$（$x\ge0$）。 -/
lemma sum_sq_le_sq_sum {ι : Type*} (s : Finset ι) (f : ι → ℝ)
    (h : ∀ k ∈ s, 0 ≤ f k) : ∑ k ∈ s, f k ^ 2 ≤ (∑ k ∈ s, f k) ^ 2 := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | insert a s ha ih =>
      rw [Finset.sum_insert ha, Finset.sum_insert ha]
      have ha0 : 0 ≤ f a := h a (Finset.mem_insert_self a s)
      have hs0 : 0 ≤ ∑ k ∈ s, f k :=
        Finset.sum_nonneg (fun k hk => h k (Finset.mem_insert_of_mem hk))
      have ih' : ∑ k ∈ s, f k ^ 2 ≤ (∑ k ∈ s, f k) ^ 2 :=
        ih (fun k hk => h k (Finset.mem_insert_of_mem hk))
      nlinarith [mul_nonneg ha0 hs0]

/-! ### 二、参与比（有效强模数） -/

/-- 参与比 $\mathrm{PR}=(\sum\sigma^2)^2/\sum\sigma^4$。 -/
noncomputable def participation {ι : Type*} (s : Finset ι) (σ : ι → ℝ) : ℝ :=
  (totalSq s σ) ^ 2 / (∑ k ∈ s, σ k ^ 4)

/-- **下界**：$\mathrm{PR}\ge1$（交叉项非负）。 -/
lemma participation_ge_one {ι : Type*} (s : Finset ι) (σ : ι → ℝ)
    (hpos : 0 < ∑ k ∈ s, σ k ^ 4) :
    1 ≤ participation s σ := by
  unfold participation
  rw [le_div_iff₀ hpos]
  unfold totalSq
  have h4 : ∑ k ∈ s, σ k ^ 4 = ∑ k ∈ s, (σ k ^ 2) ^ 2 :=
    Finset.sum_congr rfl (fun k _ => by ring)
  rw [h4]
  have h := sum_sq_le_sq_sum s (fun k => σ k ^ 2) (fun k _ => sq_nonneg (σ k))
  linarith

/-- **上界**：$\mathrm{PR}\le r$（Cauchy–Schwarz）。 -/
lemma participation_le_card {ι : Type*} (s : Finset ι) (σ : ι → ℝ)
    (hpos : 0 < ∑ k ∈ s, σ k ^ 4) :
    participation s σ ≤ (s.card : ℝ) := by
  unfold participation
  rw [div_le_iff₀ hpos]
  unfold totalSq
  have hcs : (∑ k ∈ s, σ k ^ 2 * 1) ^ 2 ≤
      (∑ k ∈ s, (σ k ^ 2) ^ 2) * (∑ _k ∈ s, (1 : ℝ) ^ 2) :=
    Finset.sum_mul_sq_le_sq_mul_sq s (fun k => σ k ^ 2) (fun _ => (1 : ℝ))
  simp only [mul_one, one_pow, Finset.sum_const, nsmul_eq_mul] at hcs
  have h4 : ∑ k ∈ s, (σ k ^ 2) ^ 2 = ∑ k ∈ s, σ k ^ 4 :=
    Finset.sum_congr rfl (fun k _ => by ring)
  rw [h4] at hcs
  calc (∑ k ∈ s, σ k ^ 2) ^ 2
      ≤ (∑ k ∈ s, σ k ^ 4) * (s.card : ℝ) := hcs
    _ = (s.card : ℝ) * (∑ k ∈ s, σ k ^ 4) := by ring

/-- 全等谱（$\sigma_k\equiv a$）：$\mathrm{PR}=r$。 -/
lemma participation_of_uniform {ι : Type*} (s : Finset ι) (a : ℝ) (ha : a ≠ 0)
    (hne : s.Nonempty) :
    participation s (fun _ => a) = (s.card : ℝ) := by
  unfold participation totalSq
  have h2 : ∑ _k ∈ s, a ^ 2 = (s.card : ℝ) * a ^ 2 := by
    rw [Finset.sum_const, nsmul_eq_mul]
  have h4 : ∑ _k ∈ s, a ^ 4 = (s.card : ℝ) * a ^ 4 := by
    rw [Finset.sum_const, nsmul_eq_mul]
  rw [h2, h4]
  have hc : (s.card : ℝ) ≠ 0 := by
    exact_mod_cast Finset.card_ne_zero.mpr hne
  have ha2 : a ^ 2 ≠ 0 := pow_ne_zero 2 ha
  field_simp

/-! ### 三、方差按强模／弱模分解 -/

/-- 强模集合与弱模集合的权重之和等于总权重（不重不漏）。 -/
theorem variance_split {ι : Type*} [DecidableEq ι] (s t : Finset ι) (σ : ι → ℝ)
    (ht : t ⊆ s) :
    totalSq t σ + totalSq (s \ t) σ = totalSq s σ := by
  unfold totalSq
  have h := Finset.sum_sdiff (f := fun k => σ k ^ 2) ht
  linarith

/-- 强模权重不超过总权重。 -/
lemma band_le_total {ι : Type*} [DecidableEq ι] (s t : Finset ι) (σ : ι → ℝ)
    (ht : t ⊆ s) : totalSq t σ ≤ totalSq s σ := by
  unfold totalSq
  exact Finset.sum_le_sum_of_subset_of_nonneg ht (fun k _ _ => sq_nonneg (σ k))

/-! ### 四、截断 -/

/-- 上缘有界 ⇒ 存在截断：所有模的刚度都不超过某个 $C'$。 -/
theorem cutoff_exists {ι : Type*} (s : Finset ι) (σ : ι → ℝ) (C : ℝ)
    (h : ∀ k ∈ s, σ k ≤ C) : ∃ C', ∀ k ∈ s, σ k ≤ C' :=
  ⟨C, h⟩

/-- 截断频率 $\omega_{\rm cut}=\sqrt{\sigma_{\max}/M}$ 对质量 $M$ 严格减。 -/
theorem omega_cut_strictAntiOn (σmax : ℝ) (hσ : 0 < σmax) :
    StrictAntiOn (fun M => Real.sqrt (σmax / M)) (Set.Ioi 0) := by
  intro M1 hM1 M2 hM2 hlt
  have hdiv : σmax / M2 < σmax / M1 := by
    rw [div_lt_div_iff₀ hM2 hM1]
    exact mul_lt_mul_of_pos_left hlt hσ
  have h2 : 0 < σmax / M2 := div_pos hσ hM2
  exact Real.sqrt_lt_sqrt (le_of_lt h2) hdiv

/-- 上缘有界且质量正 ⇒ 截断频率有限正。 -/
theorem omega_cut_pos (σmax M : ℝ) (hσ : 0 < σmax) (hM : 0 < M) :
    0 < Real.sqrt (σmax / M) :=
  Real.sqrt_pos.mpr (div_pos hσ hM)

/-- 上缘有界 ⇒ 截断频率有界（对固定的 $M$）。 -/
theorem omega_cut_bounded (σmax C M : ℝ) (hM : 0 < M) (hC : σmax ≤ C) :
    Real.sqrt (σmax / M) ≤ Real.sqrt (C / M) := by
  apply Real.sqrt_le_sqrt
  exact div_le_div_of_nonneg_right hC (le_of_lt hM)

end CQM.NonAffineSpectrum
