/-
  第87轮（成果登记 R-96）：亏角涨落的载体——Regge Hessian 的规范零模与曲率激发，温度入口 (4.1′)
  ==========================================================================
  承接 R73（位移盲性、(4.1) 改载体为内禀扇区）。本文件只承载纯代数/分析骨架：

    * 玻色占据 nB(u)=1/(exp u-1) 的正性；
    * 热因子 F(a,T)=1+2 nB(a/T) 的三条性质：
        - F>=1（零点项有限正值）
        - F<=1+2T/a（高温古典等分上界，用 exp x>=1+x）
        - F 对 T 严格单增（升温涨落增）——这是 (4.1′) 温度入口的链内要求
    * 曲率模求和 sigmaSq=Σ c_k F(a_k,T) 的正性、单调性、零点下界；
    * 规范零模（几何传递 transmission=0）不进读数。

  外部依据（只作工具，不写成 CQM=量子引力）：
    arXiv:1110.6866 §2 (2.5)-(2.9) 线性化 Regge 二阶作用量；
    arXiv:0912.1817 §4 (4.2)-(4.5) / arXiv:0810.3594：位移模 Y_I 是 Hessian 零模。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

open scoped BigOperators

namespace CQM.TemperatureEntry

noncomputable section

/-! ### 一、玻色占据数与热因子 -/

/-- 玻色占据数 $n_B(u)=1/(e^u-1)$（$u>0$）。 -/
def nB (u : ℝ) : ℝ := 1 / (Real.exp u - 1)

/-- $u>0\Rightarrow e^u-1>0$。 -/
lemma exp_minus_one_pos {u : ℝ} (hu : 0 < u) : 0 < Real.exp u - 1 := by
  have h : 1 < Real.exp u := Real.one_lt_exp_iff.mpr hu
  linarith

/-- 玻色占据数为正。 -/
lemma nB_pos {u : ℝ} (hu : 0 < u) : 0 < nB u := by
  unfold nB
  exact one_div_pos.mpr (exp_minus_one_pos hu)

/-- 热因子 $F(a,T)=1+2n_B(a/T)$（$a>0,T>0$）：即 $[1+2n_B]$ 结构。 -/
def thermalFactor (a T : ℝ) : ℝ := 1 + 2 * nB (a / T)

/-- 零点下界：$F\ge1$（有限正值，非 R73 前的恒零）。 -/
lemma thermalFactor_ge_one (a T : ℝ) (ha : 0 < a) (hT : 0 < T) :
    1 ≤ thermalFactor a T := by
  unfold thermalFactor
  have h := nB_pos (div_pos ha hT)
  linarith

/-- 严格正性：$F>0$。 -/
lemma thermalFactor_pos (a T : ℝ) (ha : 0 < a) (hT : 0 < T) :
    0 < thermalFactor a T := by
  have h := thermalFactor_ge_one a T ha hT
  linarith

/-- 高温古典等分上界：$F\le1+2T/a$（用 $e^x\ge1+x$）。 -/
lemma thermalFactor_le_linear (a T : ℝ) (ha : 0 < a) (hT : 0 < T) :
    thermalFactor a T ≤ 1 + 2 * (T / a) := by
  unfold thermalFactor nB
  have hu : 0 < a / T := div_pos ha hT
  have hden : 0 < Real.exp (a / T) - 1 := exp_minus_one_pos hu
  have hge : a / T ≤ Real.exp (a / T) - 1 := by
    have hx := Real.add_one_le_exp (a / T)
    linarith
  have hfrac : 1 / (Real.exp (a / T) - 1) ≤ 1 / (a / T) :=
    one_div_le_one_div_of_le hu hge
  have hrw : 1 / (a / T) = T / a := by
    field_simp [ha.ne', hT.ne']
  rw [hrw] at hfrac
  nlinarith

/-- 温度入口的核心：$T\mapsto F(a,T)$ 在 $(0,\infty)$ 上严格单增。 -/
lemma thermalFactor_strictMono (a : ℝ) (ha : 0 < a) :
    StrictMonoOn (thermalFactor a) (Set.Ioi 0) := by
  intro T1 hT1 T2 hT2 hT12
  unfold thermalFactor nB
  have hu2ltu1 : a / T2 < a / T1 := by
    rw [div_lt_div_iff₀ hT2 hT1]
    exact mul_lt_mul_of_pos_left hT12 ha
  have hexp : Real.exp (a / T2) < Real.exp (a / T1) := Real.exp_lt_exp.mpr hu2ltu1
  have hden2 : 0 < Real.exp (a / T2) - 1 := exp_minus_one_pos (div_pos ha hT2)
  have hdenlt : Real.exp (a / T2) - 1 < Real.exp (a / T1) - 1 := by linarith
  have hfrac : 1 / (Real.exp (a / T1) - 1) < 1 / (Real.exp (a / T2) - 1) :=
    one_div_lt_one_div_of_lt hden2 hdenlt
  linarith

/-! ### 二、曲率模求和 (4.1′) -/

/-- $\sigma^2(T)=\sum_k c_k F(a_k,T)$：$c_k=|A\cdot v_k|^2c_k^0\ge0$，$a_k=\hbar\omega_k/k_B$。 -/
def sigmaSq (c a : ℕ → ℝ) (N : ℕ) (T : ℝ) : ℝ :=
  Finset.sum (Finset.range N) (fun k => c k * thermalFactor (a k) T)

/-- 零点项 $\sum_k c_k$。 -/
def zeroPoint (c : ℕ → ℝ) (N : ℕ) : ℝ :=
  Finset.sum (Finset.range N) c

/-- 有非零权重则 $\sigma^2(T)>0$（否证"恒为零"）。 -/
lemma sigmaSq_pos {c a : ℕ → ℝ} {N : ℕ}
    (hc : ∀ k, 0 ≤ c k) (ha : ∀ k, 0 < a k) (hT : 0 < T)
    (hpos : ∃ k < N, 0 < c k) : 0 < sigmaSq c a N T := by
  unfold sigmaSq
  rcases hpos with ⟨k, hk, hck⟩
  have hmem : k ∈ Finset.range N := Finset.mem_range.mpr hk
  have hterm : 0 < c k * thermalFactor (a k) T := by
    exact mul_pos hck (thermalFactor_pos (a k) T (ha k) hT)
  have hle : c k * thermalFactor (a k) T ≤ sigmaSq c a N T := by
    unfold sigmaSq
    exact Finset.single_le_sum
      (fun i hi => mul_nonneg (hc i) (le_of_lt (thermalFactor_pos (a i) T (ha i) hT))) hmem
  exact lt_of_lt_of_le hterm hle

/-- 零点下界：$\sigma^2(T)\ge\sum_kc_k$（$F\ge1$）。 -/
lemma sigmaSq_ge_zeroPoint {c a : ℕ → ℝ} {N : ℕ}
    (hc : ∀ k, 0 ≤ c k) (ha : ∀ k, 0 < a k) (hT : 0 < T) :
    zeroPoint c N ≤ sigmaSq c a N T := by
  unfold sigmaSq zeroPoint
  apply Finset.sum_le_sum
  intro k hk
  have hf := thermalFactor_ge_one (a k) T (ha k) hT
  nlinarith [hc k]

/-- $\sigma^2$ 对 $T$ 单调不减（升温涨落增，方向同 `审-3`）。 -/
lemma sigmaSq_mono {c a : ℕ → ℝ} {N : ℕ}
    (hc : ∀ k, 0 ≤ c k) (ha : ∀ k, 0 < a k)
    {T1 T2 : ℝ} (hT1 : 0 < T1) (hT2 : 0 < T2) (hT12 : T1 ≤ T2) :
    sigmaSq c a N T1 ≤ sigmaSq c a N T2 := by
  unfold sigmaSq
  apply Finset.sum_le_sum
  intro k hk
  have hmono : MonotoneOn (thermalFactor (a k)) (Set.Ioi 0) :=
    (thermalFactor_strictMono (a k) (ha k)).monotoneOn
  exact mul_le_mul_of_nonneg_left (hmono hT1 hT2 hT12) (hc k)

/-! ### 三、规范零模不进读数 -/

/-- 位移（规范）模的几何传递 $|A\cdot Y_I|^2=0$ ⇒ 对 (4.1′) 贡献为零。 -/
lemma gauge_mode_zero_weight (transmission c0 a T : ℝ) (h : transmission = 0) :
    transmission ^ 2 * c0 * thermalFactor a T = 0 := by
  rw [h]
  ring

/-- 曲率（非规范）模权重正：传递非零且 $c_0>0$ ⇒ 贡献正。 -/
lemma curvature_mode_pos (transmission c0 a T : ℝ)
    (ht : transmission ≠ 0) (hc0 : 0 < c0) (ha : 0 < a) (hT : 0 < T) :
    0 < transmission ^ 2 * c0 * thermalFactor a T := by
  have ht2 : 0 < transmission ^ 2 := sq_pos_of_ne_zero ht
  exact mul_pos (mul_pos ht2 hc0) (thermalFactor_pos a T ha hT)

end
end CQM.TemperatureEntry
