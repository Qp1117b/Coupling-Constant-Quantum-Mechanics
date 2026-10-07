import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import Mathlib.Topology.Basic
import Mathlib.Order.Filter.Basic
import Mathlib.Order.Filter.AtTopBot.Basic
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Order.Interval.Set.Basic
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Order.Monotone.Basic
import Mathlib.Topology.Order.MonotoneConvergence
import Mathlib.Topology.Algebra.GroupWithZero

/-! # Mathieu 连分数与 λ_c 的严格定义

本文件给出 CQM 中 Mathieu 临界值 λ_c 的解析定义。

Mathieu 方程 y'' + (a - 2q cos(2z))y = 0 的第一奇特征值 b₁(q) 满足
b₁(q) = 2q 当且仅当 q 满足以下连分数方程（McLachlan 1947, Ch. III;
NIST DLMF §28.6）：

  1 - 3q = q² / (9 - 2q - q² / (25 - 2q - q² / (49 - 2q - ...)))

λ_c := 4q_c，其中 q_c 是上述方程在 (0, 1/2) 内的唯一解。
-/

namespace CQM

open Filter Set Topology

section MathieuContinuedFraction

set_option maxHeartbeats 10000000

/-! ## 有限截断连分数 -/

/-- Mathieu 连分数尾部的有限截断。

`mathieuContFracTail q k N` 表示从第 `k` 层开始、深度为 `N` 的截断：
```
  q² / ((2k+1)² - 2q - q² / ((2(k+1)+1)² - 2q - ...
        ... - q² / ((2(k+N-1)+1)² - 2q)...))
```
当 `N = 0` 时返回 0。 -/
noncomputable def mathieuContFracTail (q : ℝ) (k : ℕ) : ℕ → ℝ
  | 0     => 0
  | N + 1 => q^2 / ((2 * k + 1) ^ 2 - 2 * q - mathieuContFracTail q (k + 1) N)

/-- 完整连分数的有限截断（深度 N），即从第 1 层开始的截断。 -/
noncomputable def mathieuContFracAux (q : ℝ) (N : ℕ) : ℝ :=
  mathieuContFracTail q 1 N

/-! ## 基本有界性（k ≥ 1）

当 k ≥ 1 且 q ∈ [0, 1/2] 时，所有有限截断都被一个与 k、N 无关的常数 1/7 控制。
这一简单上界足以保证分母恒正、序列单调收敛。 -/

/-- 辅助：k ≥ 1 时 (2k+1)² ≥ 9。 -/
private theorem two_k_one_sq_ge_nine {k : ℕ} (hk : k ≥ 1) : (2 * (k : ℝ) + 1) ^ 2 ≥ 9 := by
  have hk' : (k : ℝ) ≥ 1 := by exact_mod_cast hk
  calc
    (2 * (k : ℝ) + 1) ^ 2 ≥ (2 * (1 : ℝ) + 1) ^ 2 := by nlinarith
    _ = 9 := by norm_num

/-- 核心上界：tail_{k,N} ≤ 1/7（k ≥ 1，q ∈ [0,1/2]）。
使用 ∀ N, ∀ k 的归纳模式，使归纳假设对 k+1 可用。 -/
theorem mathieuContFracTail_le_one_seventh (q : ℝ) (hq : 0 ≤ q ∧ q ≤ 1 / 2)
    {k : ℕ} (hk : k ≥ 1) (N : ℕ) :
    mathieuContFracTail q k N ≤ 1 / 7 := by
  have h_all : ∀ N, ∀ (k : ℕ), k ≥ 1 → mathieuContFracTail q k N ≤ 1 / 7 := by
    intro N
    induction N with
    | zero =>
      intro k hk'; simp [mathieuContFracTail]
    | succ N ih =>
      intro k hk'
      simp [mathieuContFracTail]
      have hden : (2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTail q (k + 1) N ≥ 55 / 7 := by
        have h1 : (2 * (k : ℝ) + 1) ^ 2 ≥ 9 := two_k_one_sq_ge_nine hk'
        have h2 : (2 * q : ℝ) ≤ 1 := by nlinarith
        have h3 := ih (k + 1) (by omega)
        nlinarith
      apply (div_le_iff₀ (by nlinarith)).mpr
      nlinarith
  exact h_all N k hk

/-- 有限截断的分母恒正（k ≥ 1）。 -/
theorem mathieuContFracTail_denominator_pos (q : ℝ) (hq : 0 ≤ q ∧ q ≤ 1 / 2)
    {k : ℕ} (hk : k ≥ 1) (N : ℕ) :
    (2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTail q (k + 1) N > 0 := by
  have h1 : (2 * (k : ℝ) + 1) ^ 2 ≥ 9 := two_k_one_sq_ge_nine hk
  have h2 : (2 * q : ℝ) ≤ 1 := by nlinarith
  have h3 : mathieuContFracTail q (k + 1) N ≤ 1 / 7 :=
    mathieuContFracTail_le_one_seventh q hq (k := k + 1) (hk := by omega) (N := N)
  nlinarith

/-- 截断非负（k ≥ 1，q ∈ [0,1/2]）。 -/
theorem mathieuContFracTail_nonneg (q : ℝ) (hq : 0 ≤ q ∧ q ≤ 1 / 2)
    {k : ℕ} (hk : k ≥ 1) (N : ℕ) :
    mathieuContFracTail q k N ≥ 0 := by
  have h_all : ∀ N, ∀ (k : ℕ), k ≥ 1 → mathieuContFracTail q k N ≥ 0 := by
    intro N
    induction N with
    | zero =>
      intro k hk'; simp [mathieuContFracTail]
    | succ N ih =>
      intro k hk'
      simp [mathieuContFracTail]
      apply div_nonneg
      · nlinarith
      · have hpos := mathieuContFracTail_denominator_pos q hq hk' N
        linarith
  exact h_all N k hk

/-- 截断关于深度单调递增（k ≥ 1）。 -/
theorem mathieuContFracTail_mono (q : ℝ) (hq : 0 ≤ q ∧ q ≤ 1 / 2)
    {k : ℕ} (hk : k ≥ 1) (N : ℕ) :
    mathieuContFracTail q k N ≤ mathieuContFracTail q k (N + 1) := by
  have h_all : ∀ N, ∀ (k : ℕ), k ≥ 1 → mathieuContFracTail q k N ≤ mathieuContFracTail q k (N + 1) := by
    intro N
    induction N with
    | zero =>
      intro k hk'
      simp [mathieuContFracTail]
      apply div_nonneg
      · nlinarith
      · have hpos := mathieuContFracTail_denominator_pos q hq hk' 0
        have h0 : mathieuContFracTail q (k + 1) 0 = 0 := by simp [mathieuContFracTail]
        rw [h0] at hpos
        linarith
    | succ N ih =>
      intro k hk'
      have hpos1 : 0 < (2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTail q (k + 1) (N + 1) :=
        mathieuContFracTail_denominator_pos q hq hk' (N + 1)
      have hpos2 : 0 < (2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTail q (k + 1) N :=
        mathieuContFracTail_denominator_pos q hq hk' N
      have h_ih : mathieuContFracTail q (k + 1) N ≤ mathieuContFracTail q (k + 1) (N + 1) :=
        ih (k + 1) (by omega)
      have h_denom_le : (2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTail q (k + 1) (N + 1) ≤
                       (2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTail q (k + 1) N := by
        linarith
      have h_sq_nonneg : 0 ≤ q ^ 2 := sq_nonneg q
      have h_inv : 1 / ((2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTail q (k + 1) N) ≤
                  1 / ((2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTail q (k + 1) (N + 1)) :=
        (one_div_le_one_div hpos2 hpos1).mpr h_denom_le
      have hcalc : mathieuContFracTail q k (N + 1) ≤ mathieuContFracTail q k (N + 1 + 1) := by
        calc
          mathieuContFracTail q k (N + 1) = q ^ 2 / ((2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTail q (k + 1) N) := by
            simp [mathieuContFracTail]
          _ = q ^ 2 * (1 / ((2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTail q (k + 1) N)) := by ring
          _ ≤ q ^ 2 * (1 / ((2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTail q (k + 1) (N + 1))) :=
            mul_le_mul_of_nonneg_left h_inv h_sq_nonneg
          _ = q ^ 2 / ((2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTail q (k + 1) (N + 1)) := by ring
          _ = mathieuContFracTail q k (N + 1 + 1) := by simp [mathieuContFracTail]
      simpa [add_assoc] using hcalc
  exact h_all N k hk

/-- 截断序列单调递增（k ≥ 1）。使用 mathieuContFracTail_mono 逐步递推。 -/
theorem mathieuContFracTail_monotone (q : ℝ) (hq : 0 ≤ q ∧ q ≤ 1 / 2)
    {k : ℕ} (hk : k ≥ 1) (n m : ℕ) (hnm : n ≤ m) :
    mathieuContFracTail q k n ≤ mathieuContFracTail q k m := by
  have h_mono_succ : ∀ n, mathieuContFracTail q k n ≤ mathieuContFracTail q k (n + 1) :=
    λ n => mathieuContFracTail_mono q hq hk n
  exact monotone_nat_of_le_succ h_mono_succ hnm

/-- 截断序列有上界 1/7（k ≥ 1）。 -/
theorem mathieuContFracTail_bddAbove (q : ℝ) (hq : 0 ≤ q ∧ q ≤ 1 / 2)
    {k : ℕ} (hk : k ≥ 1) :
    BddAbove (Set.range (mathieuContFracTail q k)) := by
  use 1 / 7
  rintro _ ⟨N, rfl⟩
  exact mathieuContFracTail_le_one_seventh q hq hk N

/-! ## 无限连分数 -/

/-- 无限连分数尾部定义为其有限截断的上确界。 -/
noncomputable def mathieuContFracTailInf (q : ℝ) (_hq : 0 ≤ q ∧ q ≤ 1 / 2) (k : ℕ) : ℝ :=
  ⨆ N, mathieuContFracTail q k N

/-- 无限连分数尾部的收敛性质（k ≥ 1）。 -/
theorem mathieuContFracTailInf_spec (q : ℝ) (hq : 0 ≤ q ∧ q ≤ 1 / 2) {k : ℕ} (hk : k ≥ 1) :
    Tendsto (mathieuContFracTail q k) atTop (𝓝 (mathieuContFracTailInf q hq k)) := by
  unfold mathieuContFracTailInf
  apply tendsto_atTop_ciSup
  · intro n m hnm
    exact mathieuContFracTail_monotone q hq hk n m hnm
  · exact mathieuContFracTail_bddAbove q hq hk

/-- 无限连分数（第 1 层尾部）。 -/
noncomputable def mathieuContFrac (q : ℝ) (hq : 0 ≤ q ∧ q ≤ 1 / 2) : ℝ :=
  mathieuContFracTailInf q hq 1

/-- 极限保持非负性（k ≥ 1）。 -/
theorem mathieuContFracTailInf_nonneg (q : ℝ) (hq : 0 ≤ q ∧ q ≤ 1 / 2)
    {k : ℕ} (hk : k ≥ 1) :
    mathieuContFracTailInf q hq k ≥ 0 := by
  have h0 : mathieuContFracTail q k 0 = 0 := by simp [mathieuContFracTail]
  have hle : mathieuContFracTail q k 0 ≤ mathieuContFracTailInf q hq k := by
    rw [mathieuContFracTailInf]
    exact le_ciSup (mathieuContFracTail_bddAbove q hq hk) 0
  linarith

/-- 极限保持 1/7 上界（k ≥ 1）。 -/
theorem mathieuContFracTailInf_le_one_seventh (q : ℝ) (hq : 0 ≤ q ∧ q ≤ 1 / 2)
    {k : ℕ} (hk : k ≥ 1) :
    mathieuContFracTailInf q hq k ≤ 1 / 7 := by
  rw [mathieuContFracTailInf]
  apply ciSup_le
  intro N
  exact mathieuContFracTail_le_one_seventh q hq hk N

/-- 无限尾部分母恒正（k ≥ 1）。 -/
theorem mathieuContFracTailInf_denominator_pos (q : ℝ) (hq : 0 ≤ q ∧ q ≤ 1 / 2)
    {k : ℕ} (hk : k ≥ 1) :
    (2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTailInf q hq (k + 1) > 0 := by
  have h1 : (2 * (k : ℝ) + 1) ^ 2 ≥ 9 := two_k_one_sq_ge_nine hk
  have h2 : (2 * q : ℝ) ≤ 1 := by nlinarith
  have h3 := mathieuContFracTailInf_le_one_seventh q hq (k := k + 1) (hk := by omega)
  nlinarith

/-- 无限尾部满足函数方程（k ≥ 1）：
    tail_k = q² / ((2k+1)² - 2q - tail_{k+1})。 -/
theorem mathieuContFracTailInf_eq (q : ℝ) (hq : 0 ≤ q ∧ q ≤ 1 / 2)
    {k : ℕ} (hk : k ≥ 1) :
    mathieuContFracTailInf q hq k =
      q^2 / ((2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTailInf q hq (k + 1)) := by
  have h_tendsto_k : Tendsto (mathieuContFracTail q k) atTop (𝓝 (mathieuContFracTailInf q hq k)) :=
    mathieuContFracTailInf_spec q hq hk
  have h_tendsto_k1 : Tendsto (mathieuContFracTail q (k + 1)) atTop
      (𝓝 (mathieuContFracTailInf q hq (k + 1))) :=
    mathieuContFracTailInf_spec q hq (k := k + 1) (hk := by omega)
  let g := λ x : ℝ => q^2 / ((2 * (k : ℝ) + 1) ^ 2 - 2 * q - x)
  have hg_cont : ContinuousAt g (mathieuContFracTailInf q hq (k + 1)) := by
    have hne : (2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTailInf q hq (k + 1) ≠ 0 := by
      nlinarith [mathieuContFracTailInf_denominator_pos q hq hk]
    have h_denom_cont : ContinuousAt (λ x : ℝ => (2 * (k : ℝ) + 1) ^ 2 - 2 * q - x)
        (mathieuContFracTailInf q hq (k + 1)) := by
      refine (ContinuousAt.sub (ContinuousAt.sub ?_ ?_) continuousAt_id)
      · exact continuousAt_const
      · exact continuousAt_const
    have h_num_cont : ContinuousAt (λ _ : ℝ => q^2) (mathieuContFracTailInf q hq (k + 1)) :=
      continuousAt_const
    exact h_num_cont.div h_denom_cont hne
  have h_recurrence : ∀ N, mathieuContFracTail q k (N + 1) = g (mathieuContFracTail q (k + 1) N) := by
    intro N; simp [mathieuContFracTail, g]
  have h_g_comp : Tendsto (g ∘ mathieuContFracTail q (k + 1)) atTop
      (𝓝 (g (mathieuContFracTailInf q hq (k + 1)))) :=
    hg_cont.tendsto.comp h_tendsto_k1
  have h_shift_eq : (mathieuContFracTail q k ∘ Nat.succ) = (g ∘ mathieuContFracTail q (k + 1)) := by
    funext N; simp [h_recurrence, Function.comp]
  have h_shift : Tendsto (mathieuContFracTail q k ∘ Nat.succ) atTop
      (𝓝 (mathieuContFracTailInf q hq k)) := by
    simpa [Function.comp] using h_tendsto_k.comp (tendsto_add_atTop_nat 1)
  rw [h_shift_eq] at h_shift
  exact tendsto_nhds_unique h_shift h_g_comp

/-! ## q 的区间与有限截断的连续性 -/

/-- Mathieu 参数 q 所在的闭区间 [0, 1/2]。 -/
def mathieuParameterInterval : Set ℝ := Icc 0 (1 / 2)

/-- 有限截断关于 q 在 [0,1/2] 上连续（k ≥ 1 时）。 -/
theorem mathieuContFracTail_continuousOn {k : ℕ} (hk : k ≥ 1) (N : ℕ) :
    ContinuousOn (fun (q : ℝ) => mathieuContFracTail q k N) mathieuParameterInterval := by
  have h_all : ∀ N, ∀ (k : ℕ), k ≥ 1 →
      ContinuousOn (fun (q : ℝ) => mathieuContFracTail q k N) mathieuParameterInterval := by
    intro N
    induction N with
    | zero =>
      intro k hk'; simp [mathieuContFracTail]; exact continuousOn_const
    | succ N ih =>
      intro k hk'
      simp [mathieuContFracTail]
      apply ContinuousOn.div
      · apply ContinuousOn.pow; exact continuousOn_id
      · apply ContinuousOn.sub
        · apply ContinuousOn.sub
          · exact continuousOn_const
          · apply ContinuousOn.mul
            · exact continuousOn_const
            · exact continuousOn_id
        · exact ih (k + 1) (by omega)
      · intro q hq
        have hq' : 0 ≤ q ∧ q ≤ 1 / 2 := hq
        have hpos := mathieuContFracTail_denominator_pos q hq' (k := k) (hk := hk') (N := N)
        exact ne_of_gt hpos
  exact h_all N k hk

/-- 完整连分数截断关于 q 连续。 -/
theorem mathieuContFracAux_continuousOn (N : ℕ) :
    ContinuousOn (fun q => mathieuContFracAux q N) mathieuParameterInterval := by
  unfold mathieuContFracAux
  exact mathieuContFracTail_continuousOn (k := 1) (hk := by omega) (N := N)

/-! ## 一致收敛与极限连续性 -/

/-- 无限尾部与有限截断的逐点误差上界（k ≥ 1）。 -/
theorem mathieuContFracTailInf_sub_tail_le {k : ℕ} (hk : k ≥ 1)
    (q : ℝ) (hq : 0 ≤ q ∧ q ≤ 1/2) (N : ℕ) :
    mathieuContFracTailInf q hq k - mathieuContFracTail q k N ≤ (1 / 4) ^ (N + 1) := by
  have hge : mathieuContFracTailInf q hq k ≥ mathieuContFracTail q k N := by
    rw [mathieuContFracTailInf]
    exact le_ciSup (mathieuContFracTail_bddAbove q hq hk) N
  have h_all : ∀ N, ∀ (k : ℕ), k ≥ 1 →
      mathieuContFracTailInf q hq k - mathieuContFracTail q k N ≤ (1 / 4) ^ (N + 1) := by
    intro N
    induction N with
    | zero =>
      intro k hk'
      have h1 := mathieuContFracTailInf_le_one_seventh q hq hk'
      have h2 : mathieuContFracTail q k 0 = 0 := by simp [mathieuContFracTail]
      have h14 : (1 : ℝ) / 7 ≤ (1 / 4 : ℝ) ^ 1 := by norm_num
      rw [h2]
      linarith
    | succ N ih =>
      intro k hk'
      have h_eq := mathieuContFracTailInf_eq q hq hk'
      have h_finite : mathieuContFracTail q k (N + 1) =
          q^2 / ((2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTail q (k + 1) N) := by
        simp [mathieuContFracTail]
      rw [h_eq, h_finite]
      let D := (2 * (k : ℝ) + 1) ^ 2 - 2 * q
      let Tinf := mathieuContFracTailInf q hq (k + 1)
      let TN := mathieuContFracTail q (k + 1) N
      have hposTinf : D - Tinf > 0 :=
        mathieuContFracTailInf_denominator_pos q hq hk'
      have hposTN : D - TN > 0 :=
        mathieuContFracTail_denominator_pos q hq (k := k) (hk := hk') (N := N)
      have h3 : Tinf - TN ≤ (1 / 4) ^ (N + 1) := ih (k + 1) (by omega)
      have hq2 : q^2 ≤ 1 / 4 := by nlinarith
      have h_sq_nonneg : 0 ≤ q^2 := sq_nonneg q
      have h_diff_nonneg : 0 ≤ Tinf - TN := by
        have hle : TN ≤ Tinf := by
          dsimp [Tinf, mathieuContFracTailInf]
          exact le_ciSup (mathieuContFracTail_bddAbove q hq (k := k + 1) (hk := by omega)) N
        linarith
      have h_mul_nonneg : 0 ≤ q^2 * (Tinf - TN) := mul_nonneg h_sq_nonneg h_diff_nonneg
      have h_denom_ge_one : (D - Tinf) * (D - TN) ≥ 1 := by
        have hD_Tinf_ge_one : D - Tinf ≥ 1 := by
          dsimp [D, Tinf]
          have hsq : (2 * (k : ℝ) + 1) ^ 2 ≥ 9 := two_k_one_sq_ge_nine hk'
          have hqbound : (2 * q : ℝ) ≤ 1 := by nlinarith
          have htail : mathieuContFracTailInf q hq (k + 1) ≤ 1/7 :=
            mathieuContFracTailInf_le_one_seventh q hq (k := k + 1) (hk := by omega)
          calc
            (2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTailInf q hq (k + 1) ≥ 9 - 1 - (1/7 : ℝ) := by
              nlinarith
            _ ≥ 1 := by norm_num
        have hD_TN_ge_one : D - TN ≥ 1 := by
          dsimp [D, TN]
          have hsq : (2 * (k : ℝ) + 1) ^ 2 ≥ 9 := two_k_one_sq_ge_nine hk'
          have hqbound : (2 * q : ℝ) ≤ 1 := by nlinarith
          have htail : mathieuContFracTail q (k + 1) N ≤ 1/7 :=
            mathieuContFracTail_le_one_seventh q hq (k := k + 1) (hk := by omega) (N := N)
          calc
            (2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTail q (k + 1) N ≥ 9 - 1 - (1/7 : ℝ) := by
              nlinarith
            _ ≥ 1 := by norm_num
        nlinarith
      -- 核心代数恒等式：q²/(D-Tinf) - q²/(D-TN) = q²(Tinf-TN)/((D-Tinf)(D-TN))
      -- 由于分母 ≥ 1，有 ... ≤ q²(Tinf-TN)
      have h_main : q^2 / (D - Tinf) - q^2 / (D - TN) ≤ q^2 * (Tinf - TN) := by
        have hne1 : D - Tinf ≠ 0 := by linarith
        have hne2 : D - TN ≠ 0 := by linarith
        have h_sub_eq : 1 / (D - Tinf) - 1 / (D - TN) = (Tinf - TN) / ((D - Tinf) * (D - TN)) := by
          field_simp [hne1, hne2]
          ring
        calc
          q^2 / (D - Tinf) - q^2 / (D - TN) = q^2 * (1 / (D - Tinf) - 1 / (D - TN)) := by ring
          _ = q^2 * ((Tinf - TN) / ((D - Tinf) * (D - TN))) := by rw [h_sub_eq]
          _ = q^2 * (Tinf - TN) / ((D - Tinf) * (D - TN)) := by ring
          _ ≤ q^2 * (Tinf - TN) := div_le_self h_mul_nonneg h_denom_ge_one
      calc
        q^2 / (D - Tinf) - q^2 / (D - TN) ≤ q^2 * (Tinf - TN) := h_main
        _ ≤ (1 / 4) * (Tinf - TN) := by nlinarith
        _ ≤ (1 / 4) * (1 / 4) ^ (N + 1) := by nlinarith
        _ = (1 / 4) ^ (N + 2) := by ring
        _ = (1 / 4) ^ ((N + 1) + 1) := by ring
  exact h_all N k hk

/-- 无限尾部与有限截断的绝对值误差上界。 -/
theorem mathieuContFracTailInf_approx {k : ℕ} (hk : k ≥ 1)
    (q : ℝ) (hq : 0 ≤ q ∧ q ≤ 1/2) (N : ℕ) :
    |mathieuContFracTailInf q hq k - mathieuContFracTail q k N| ≤ (1 / 4) ^ (N + 1) := by
  have hge : mathieuContFracTailInf q hq k ≥ mathieuContFracTail q k N := by
    rw [mathieuContFracTailInf]
    exact le_ciSup (mathieuContFracTail_bddAbove q hq hk) N
  rw [abs_of_nonneg (sub_nonneg.mpr hge)]
  exact mathieuContFracTailInf_sub_tail_le hk q hq N

/-- 将无限连分数延拓到整个实数轴上的全函数（区间外用 0 填充）。 -/
noncomputable def mathieuContFracTotal (q : ℝ) : ℝ :=
  if h : 0 ≤ q ∧ q ≤ 1 / 2 then mathieuContFrac q h else 0

/-- 有限截断在 [0,1/2] 上一致收敛到无限连分数。 -/
theorem mathieuContFracAux_tendstoUniformlyOn :
    TendstoUniformlyOn (λ N q => mathieuContFracAux q N) mathieuContFracTotal atTop mathieuParameterInterval := by
  rw [Metric.tendstoUniformlyOn_iff]
  intro ε hε
  have h : ∀ᶠ N in atTop, (1 / 4 : ℝ) ^ (N + 1) < ε := by
    have h0 : Tendsto (λ N : ℕ => (1 / 4 : ℝ) ^ (N + 1)) atTop (𝓝 0) := by
      have h_pow : Tendsto (λ N : ℕ => (1 / 4 : ℝ) ^ N) atTop (𝓝 0) :=
        tendsto_pow_atTop_nhds_zero_of_lt_one (by norm_num : (0 : ℝ) ≤ 1 / 4) (by norm_num : (1 / 4 : ℝ) < 1)
      simpa [add_comm] using h_pow.comp (tendsto_add_atTop_nat 1)
    exact h0.eventually (gt_mem_nhds hε)
  filter_upwards [h] with N hN q hq
  have hq' : 0 ≤ q ∧ q ≤ 1/2 := hq
  have hbound := mathieuContFracTailInf_approx (k := 1) (hk := by omega) q hq' N
  simp only [mathieuContFracTotal, mathieuContFrac, mathieuContFracAux]
  rcases hq with ⟨hq0, hq1⟩
  rw [dif_pos ⟨hq0, hq1⟩]
  have hdist : dist (mathieuContFracTailInf q hq' 1) (mathieuContFracTail q 1 N) ≤ (1 / 4) ^ (N + 1) := by
    simpa using hbound
  linarith

/-- 无限连分数在 [0,1/2] 上连续。 -/
theorem mathieuContFracTotal_continuousOn : ContinuousOn mathieuContFracTotal mathieuParameterInterval := by
  have h_cont_event : ∃ᶠ n : ℕ in atTop, ContinuousOn (λ q => mathieuContFracAux q n) mathieuParameterInterval := by
    refine Filter.frequently_atTop.mpr ?_
    intro N
    refine ⟨N, le_refl N, ?_⟩
    exact mathieuContFracAux_continuousOn N
  exact TendstoUniformlyOn.continuousOn mathieuContFracAux_tendstoUniformlyOn h_cont_event

/-! ## 临界方程与 q_c 的存在唯一性 -/

/-- 临界方程 f(q) = 1 - 3q - cont_frac(q) 的全函数延拓。 -/
noncomputable def mathieuCriticalEquationTotal (q : ℝ) : ℝ :=
  1 - 3 * q - mathieuContFracTotal q

/-- 临界方程在 [0,1/2] 上连续。 -/
theorem mathieuCriticalEquationTotal_continuousOn :
    ContinuousOn mathieuCriticalEquationTotal mathieuParameterInterval := by
  apply ContinuousOn.sub
  · apply ContinuousOn.sub
    · exact continuousOn_const
    · apply ContinuousOn.mul
      · exact continuousOn_const
      · exact continuousOn_id
  · exact mathieuContFracTotal_continuousOn

/-- 临界方程在 [0,1/2] 上严格递减。 -/
theorem mathieuCriticalEquationTotal_strictAnti :
    StrictAntiOn mathieuCriticalEquationTotal mathieuParameterInterval := by
  intro q hq r hr hqr
  simp only [mathieuCriticalEquationTotal]
  have hmono : mathieuContFracTotal q ≤ mathieuContFracTotal r := by
    simp only [mathieuContFracTotal]
    rw [dif_pos ⟨hq.1, hq.2⟩, dif_pos ⟨hr.1, hr.2⟩]
    have hq' : 0 ≤ q ∧ q ≤ 1 / 2 := ⟨hq.1, hq.2⟩
    have hr' : 0 ≤ r ∧ r ≤ 1 / 2 := ⟨hr.1, hr.2⟩
    -- 证明 ∀ N, ∀ k ≥ 1, tail_{k,N}(q) ≤ tail_{k,N}(r) 当 q ≤ r
    have h_tail_mono : ∀ N, ∀ (k : ℕ), k ≥ 1 →
        mathieuContFracTail q k N ≤ mathieuContFracTail r k N := by
      intro N
      induction N with
      | zero =>
        intro k hk'; simp [mathieuContFracTail]
      | succ N ih =>
        intro k hk'
        simp [mathieuContFracTail]
        have hden_q := mathieuContFracTail_denominator_pos q hq' (k := k) (hk := hk') (N := N)
        have hden_r := mathieuContFracTail_denominator_pos r hr' (k := k) (hk := hk') (N := N)
        have h_tail_step : mathieuContFracTail q (k + 1) N ≤ mathieuContFracTail r (k + 1) N :=
          ih (k + 1) (by omega)
        have h_denom_le : (2 * (k : ℝ) + 1) ^ 2 - 2 * r - mathieuContFracTail r (k + 1) N ≤
                         (2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTail q (k + 1) N := by
          nlinarith
        have h_sq : q^2 ≤ r^2 := by nlinarith
        have h_nonneg_denom_r : 0 ≤ (2 * (k : ℝ) + 1) ^ 2 - 2 * r - mathieuContFracTail r (k + 1) N :=
          by linarith
        have h_sq_nonneg_r : 0 ≤ r^2 := sq_nonneg r
        have h_part1 : q^2 * ((2 * (k : ℝ) + 1) ^ 2 - 2 * r - mathieuContFracTail r (k + 1) N) ≤
                       r^2 * ((2 * (k : ℝ) + 1) ^ 2 - 2 * r - mathieuContFracTail r (k + 1) N) :=
          mul_le_mul_of_nonneg_right h_sq h_nonneg_denom_r
        have h_part2 : r^2 * ((2 * (k : ℝ) + 1) ^ 2 - 2 * r - mathieuContFracTail r (k + 1) N) ≤
                       r^2 * ((2 * (k : ℝ) + 1) ^ 2 - 2 * q - mathieuContFracTail q (k + 1) N) :=
          mul_le_mul_of_nonneg_left h_denom_le h_sq_nonneg_r
        exact (div_le_div_iff₀ hden_q hden_r).mpr (le_trans h_part1 h_part2)
    -- 使用 ciSup_mono 将逐点单调性提升到上确界
    have h_sup : (⨆ N, mathieuContFracTail q 1 N) ≤ (⨆ N, mathieuContFracTail r 1 N) := by
      apply ciSup_mono (mathieuContFracTail_bddAbove r hr' (k := 1) (hk := by omega))
      intro N
      exact h_tail_mono N 1 (by omega)
    dsimp [mathieuContFrac, mathieuContFracTailInf]
    exact h_sup
  nlinarith

/-- 临界方程在 q = 0 处取值为 1。 -/
theorem mathieuCriticalEquationTotal_zero : mathieuCriticalEquationTotal 0 = 1 := by
  simp only [mathieuCriticalEquationTotal, mathieuContFracTotal]
  rw [dif_pos ⟨by norm_num, by norm_num⟩]
  have h0 : mathieuContFrac 0 ⟨by norm_num, by norm_num⟩ = 0 := by
    have h0_seq : ∀ N, mathieuContFracTail 0 1 N = 0 := by
      intro N
      induction N with
      | zero => simp [mathieuContFracTail]
      | succ N ih => simp [mathieuContFracTail]
    have h_tendsto := mathieuContFracTailInf_spec 0 ⟨by norm_num, by norm_num⟩ (k := 1) (hk := by omega)
    have h_eq_seq : mathieuContFracTail 0 1 = λ _ : ℕ => 0 := by
      funext N; exact h0_seq N
    have h_seq_zero : Tendsto (λ _ : ℕ => (0 : ℝ)) atTop (𝓝 (0 : ℝ)) := tendsto_const_nhds
    rw [h_eq_seq] at h_tendsto
    have h_unique := tendsto_nhds_unique h_tendsto h_seq_zero
    rw [mathieuContFrac, mathieuContFracTailInf]
    exact h_unique
  nlinarith

/-- 临界方程在 q = 1/2 处为负。 -/
theorem mathieuCriticalEquationTotal_half_neg : mathieuCriticalEquationTotal (1 / 2) < 0 := by
  simp only [mathieuCriticalEquationTotal, mathieuContFracTotal]
  rw [dif_pos ⟨by norm_num, by norm_num⟩]
  have hpos : mathieuContFrac (1 / 2) ⟨by norm_num, by norm_num⟩ > 0 := by
    have h1 : mathieuContFracTail (1 / 2 : ℝ) 1 1 > 0 := by
      simp [mathieuContFracTail]; norm_num
    have h2 : mathieuContFrac (1 / 2) ⟨by norm_num, by norm_num⟩ ≥ mathieuContFracTail (1 / 2 : ℝ) 1 1 := by
      rw [mathieuContFrac, mathieuContFracTailInf]
      exact le_ciSup (mathieuContFracTail_bddAbove (1 / 2 : ℝ) ⟨by norm_num, by norm_num⟩ (k := 1) (hk := by omega)) 1
    linarith
  nlinarith

/-- 临界方程在 (0,1/2) 内存在解。使用 mathieuCriticalEquationTotal 避免
    在 ∃ 类型中嵌入 q 的证明项。 -/
theorem mathieuCriticalParameter_exists :
    ∃ q : ℝ, 0 < q ∧ q < 1 / 2 ∧ mathieuCriticalEquationTotal q = 0 := by
  let f := mathieuCriticalEquationTotal
  have hf_cont : ContinuousOn f mathieuParameterInterval := mathieuCriticalEquationTotal_continuousOn
  have hf0 : f 0 = 1 := mathieuCriticalEquationTotal_zero
  have hf1 : f (1 / 2) < 0 := mathieuCriticalEquationTotal_half_neg
  have h_ivt : ∃ x ∈ Icc (0 : ℝ) (1/2), f x = 0 := by
    have h_neg_cont : ContinuousOn (-f) (Icc (0 : ℝ) (1/2)) := hf_cont.neg
    have h_mem : (0 : ℝ) ∈ Icc ((-f) 0) ((-f) (1/2)) := by
      have h02 : (0 : ℝ) ≤ 1/2 := by norm_num
      have h0 : (-f) 0 = -1 := by
        calc
          (-f) 0 = -(f 0) := rfl
          _ = -1 := by rw [hf0]
      have h1 : 0 < (-f) (1/2) := by
        dsimp [f]
        linarith
      rw [h0]
      exact ⟨by norm_num, by linarith⟩
    have h_ivt' := intermediate_value_Icc (by norm_num : (0 : ℝ) ≤ 1/2) h_neg_cont
    rcases h_ivt' h_mem with ⟨x, hx, hx'⟩
    refine ⟨x, hx, ?_⟩
    dsimp at hx'
    linarith
  rcases h_ivt with ⟨q, hq, heq⟩
  rcases hq with ⟨hq0, hq1⟩
  have hq0' : q > 0 := by
    by_contra h
    have : q = 0 := by linarith
    rw [this] at heq
    rw [hf0] at heq
    linarith
  have hq1' : q < 1 / 2 := by
    by_contra h
    have : q = 1 / 2 := by linarith
    rw [this] at heq
    have : f (1 / 2) < 0 := hf1
    linarith
  refine ⟨q, hq0', hq1', heq⟩

/-- Mathieu 临界参数 q_c：连分数方程在 (0,1/2) 内的唯一解。 -/
noncomputable def mathieuCriticalParameter : ℝ :=
  Classical.choose mathieuCriticalParameter_exists

theorem mathieuCriticalParameter_pos : 0 < mathieuCriticalParameter :=
  (Classical.choose_spec mathieuCriticalParameter_exists).1

theorem mathieuCriticalParameter_lt_half : mathieuCriticalParameter < 1 / 2 :=
  (Classical.choose_spec mathieuCriticalParameter_exists).2.1

theorem mathieuCriticalParameter_eq_zero : mathieuCriticalEquationTotal mathieuCriticalParameter = 0 :=
  (Classical.choose_spec mathieuCriticalParameter_exists).2.2

theorem mathieuCriticalParameter_mem_interval :
    mathieuCriticalParameter ∈ mathieuParameterInterval :=
  mem_Icc.mpr ⟨mathieuCriticalParameter_pos.le, mathieuCriticalParameter_lt_half.le⟩

theorem mathieuCriticalParameter_eq :
    1 - 3 * mathieuCriticalParameter = mathieuContFrac mathieuCriticalParameter
      ⟨mathieuCriticalParameter_pos.le, mathieuCriticalParameter_lt_half.le⟩ := by
  have h := mathieuCriticalParameter_eq_zero
  have hpos' : 0 ≤ mathieuCriticalParameter := mathieuCriticalParameter_pos.le
  have hhalf' : mathieuCriticalParameter ≤ 1/2 := mathieuCriticalParameter_lt_half.le
  unfold mathieuCriticalEquationTotal mathieuContFracTotal at h
  rw [dif_pos ⟨hpos', hhalf'⟩] at h
  linarith

/-- 临界参数 q_c 的唯一性。 -/
theorem mathieuCriticalParameter_unique {q1 q2 : ℝ}
    (hq1 : 0 < q1 ∧ q1 < 1 / 2) (hq2 : 0 < q2 ∧ q2 < 1 / 2)
    (h1 : 1 - 3 * q1 = mathieuContFrac q1 ⟨hq1.1.le, hq1.2.le⟩)
    (h2 : 1 - 3 * q2 = mathieuContFrac q2 ⟨hq2.1.le, hq2.2.le⟩) :
    q1 = q2 := by
  by_contra hneq
  have hf1 : mathieuCriticalEquationTotal q1 = 0 := by
    simp only [mathieuCriticalEquationTotal, mathieuContFracTotal]
    rw [dif_pos ⟨hq1.1.le, hq1.2.le⟩]
    linarith
  have hf2 : mathieuCriticalEquationTotal q2 = 0 := by
    simp only [mathieuCriticalEquationTotal, mathieuContFracTotal]
    rw [dif_pos ⟨hq2.1.le, hq2.2.le⟩]
    linarith
  have hI1 : q1 ∈ mathieuParameterInterval := mem_Icc.mpr ⟨hq1.1.le, hq1.2.le⟩
  have hI2 : q2 ∈ mathieuParameterInterval := mem_Icc.mpr ⟨hq2.1.le, hq2.2.le⟩
  cases lt_or_gt_of_ne hneq with
  | inl hlt =>
    have hanti := mathieuCriticalEquationTotal_strictAnti hI1 hI2 hlt
    linarith
  | inr hgt =>
    have hanti := mathieuCriticalEquationTotal_strictAnti hI2 hI1 hgt
    linarith

/-! ## q_c 的数值上下界 -/

/-- 临界参数 q_c 的下界：q_c > 0.3275。 -/
theorem mathieuCriticalParameter_gt_3275 : mathieuCriticalParameter > 0.3275 := by
  have hanti : AntitoneOn mathieuCriticalEquationTotal mathieuParameterInterval :=
    mathieuCriticalEquationTotal_strictAnti.antitoneOn
  have hI : mathieuCriticalParameter ∈ mathieuParameterInterval :=
    mathieuCriticalParameter_mem_interval
  have hfp : mathieuCriticalEquationTotal mathieuCriticalParameter = 0 :=
    mathieuCriticalParameter_eq_zero
  have hI3275 : (0.3275 : ℝ) ∈ mathieuParameterInterval := by
    norm_num [mathieuParameterInterval]
  have hf3275 : mathieuCriticalEquationTotal 0.3275 > 0 := by
    have hq₀ : 0 ≤ (0.3275 : ℝ) ∧ (0.3275 : ℝ) ≤ 1/2 := ⟨by norm_num, by norm_num⟩
    -- 利用函数方程：tail₁ = q² / (9 - 2q - tail₂)，且 tail₂ ≤ 1/7
    have h_tail_bound : mathieuContFracTailInf (0.3275 : ℝ) hq₀ 1 ≤
        (0.3275 : ℝ)^2 / ((2*(1:ℝ)+1)^2 - 2*(0.3275 : ℝ) - (1/7 : ℝ)) := by
      have h_eq := mathieuContFracTailInf_eq (0.3275 : ℝ) hq₀ (k := 1) (hk := by omega)
      -- h_eq : tail₁ = q² / (9 - 2q - tail₂)
      have h_tail2_le : mathieuContFracTailInf (0.3275 : ℝ) hq₀ 2 ≤ 1/7 :=
        mathieuContFracTailInf_le_one_seventh (0.3275 : ℝ) hq₀ (k := 2) (hk := by omega)
      have hpos_denom1 : 0 < (2*(1:ℝ)+1)^2 - 2*(0.3275 : ℝ) - mathieuContFracTailInf (0.3275 : ℝ) hq₀ 2 := by
        have : mathieuContFracTailInf (0.3275 : ℝ) hq₀ ((1:ℕ)+1) = mathieuContFracTailInf (0.3275 : ℝ) hq₀ 2 := by simp
        have hpos := mathieuContFracTailInf_denominator_pos (0.3275 : ℝ) hq₀ (k := 1) (hk := by omega)
        simpa [this] using hpos
      have hpos_denom2 : 0 < (2*(1:ℝ)+1)^2 - 2*(0.3275 : ℝ) - (1/7 : ℝ) := by
        have : (2*(1:ℝ)+1)^2 = 9 := by norm_num
        nlinarith
      have h_denom_ineq : (2*(1:ℝ)+1)^2 - 2*(0.3275 : ℝ) - (1/7 : ℝ) ≤
                         (2*(1:ℝ)+1)^2 - 2*(0.3275 : ℝ) - mathieuContFracTailInf (0.3275 : ℝ) hq₀ 2 := by
        linarith
      have h_one_div : 1 / ((2*(1:ℝ)+1)^2 - 2*(0.3275 : ℝ) - mathieuContFracTailInf (0.3275 : ℝ) hq₀ 2) ≤
                      1 / ((2*(1:ℝ)+1)^2 - 2*(0.3275 : ℝ) - (1/7 : ℝ)) :=
        (one_div_le_one_div hpos_denom1 hpos_denom2).mpr h_denom_ineq
      have h_sq_nonneg : 0 ≤ (0.3275 : ℝ)^2 := sq_nonneg _
      calc
        mathieuContFracTailInf (0.3275 : ℝ) hq₀ 1
            = (0.3275 : ℝ)^2 / ((2*(1:ℝ)+1)^2 - 2*(0.3275 : ℝ) - mathieuContFracTailInf (0.3275 : ℝ) hq₀ 2) := by
          simpa using h_eq
        _ = (0.3275 : ℝ)^2 * (1 / ((2*(1:ℝ)+1)^2 - 2*(0.3275 : ℝ) - mathieuContFracTailInf (0.3275 : ℝ) hq₀ 2)) := by ring
        _ ≤ (0.3275 : ℝ)^2 * (1 / ((2*(1:ℝ)+1)^2 - 2*(0.3275 : ℝ) - (1/7 : ℝ))) :=
          mul_le_mul_of_nonneg_left h_one_div h_sq_nonneg
        _ = (0.3275 : ℝ)^2 / ((2*(1:ℝ)+1)^2 - 2*(0.3275 : ℝ) - (1/7 : ℝ)) := by ring
    have h_numerical : (0.3275 : ℝ)^2 / ((2*(1:ℝ)+1)^2 - 2*(0.3275 : ℝ) - (1/7 : ℝ)) < 0.0175 := by
      norm_num
    have h_tail_lt_00175 : mathieuContFracTailInf (0.3275 : ℝ) hq₀ 1 < 0.0175 :=
      lt_of_le_of_lt h_tail_bound h_numerical
    have h_one_minus : 1 - 3 * (0.3275 : ℝ) = 0.0175 := by norm_num
    simp only [mathieuCriticalEquationTotal, mathieuContFracTotal, mathieuContFrac]
    rw [dif_pos hq₀, h_one_minus]
    exact sub_pos.mpr h_tail_lt_00175
  by_contra h
  have hle_3275 : mathieuCriticalParameter ≤ (0.3275 : ℝ) := by linarith
  have hge := hanti hI hI3275 hle_3275
  rw [hfp] at hge
  linarith

/-- 临界参数 q_c 的上界：q_c < 0.33。 -/
theorem mathieuCriticalParameter_lt_33 : mathieuCriticalParameter < 0.33 := by
  have hanti : AntitoneOn mathieuCriticalEquationTotal mathieuParameterInterval :=
    mathieuCriticalEquationTotal_strictAnti.antitoneOn
  have hI : mathieuCriticalParameter ∈ mathieuParameterInterval :=
    mathieuCriticalParameter_mem_interval
  have hfp : mathieuCriticalEquationTotal mathieuCriticalParameter = 0 :=
    mathieuCriticalParameter_eq_zero
  have hI33 : (0.33 : ℝ) ∈ mathieuParameterInterval := by
    norm_num [mathieuParameterInterval]
  have hf33 : mathieuCriticalEquationTotal 0.33 < 0 := by
    have h033 : 0 ≤ (0.33 : ℝ) ∧ (0.33 : ℝ) ≤ 1/2 := ⟨by norm_num, by norm_num⟩
    have hge : mathieuContFracTail (0.33 : ℝ) 1 1 ≤ mathieuContFracTailInf (0.33 : ℝ) h033 1 := by
      rw [mathieuContFracTailInf]
      exact le_ciSup (mathieuContFracTail_bddAbove (0.33 : ℝ) h033 (k := 1) (hk := by omega)) 1
    have htail1 : mathieuContFracTail (0.33 : ℝ) 1 1 > 0.013 := by
      simp [mathieuContFracTail]; norm_num
    have h_tail_gt_001 : (0.01 : ℝ) < mathieuContFracTailInf (0.33 : ℝ) h033 1 := by
      linarith
    have h_one_minus : 1 - 3 * (0.33 : ℝ) = 0.01 := by norm_num
    simp only [mathieuCriticalEquationTotal, mathieuContFracTotal, mathieuContFrac]
    rw [dif_pos h033, h_one_minus]
    linarith
  by_contra h
  have hge_33 : mathieuCriticalParameter ≥ (0.33 : ℝ) := by linarith
  have hle_33 := hanti hI33 hI hge_33
  rw [hfp] at hle_33
  linarith

end MathieuContinuedFraction

end CQM