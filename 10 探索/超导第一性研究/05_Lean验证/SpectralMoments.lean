/-
  第92轮补（成果登记 R-101）：链内 alpha^2F 与两矩分歧的结构消解
  ===================================================================
  承接第88轮（曲率模 Debye DOS g∝ω²）。本文件承载矩之间的**代数关系**；
  各矩的数值由标准微积分给出（并在数值脚本中高精度独立验证）：

    wNorm=1、logM=-1/2（∫₀¹2x ln x dx）、
    w2_A2F=1/2（∫₀¹2x·x²dx）、w2_DOS=3/5（∫₀¹3x⁴dx / ∫₀¹3x²dx）。

  Lean 证明的命题：
    * ω_log = ω_D·e^{logM} = e^{-1/2}ω_D（与链内相位支/ω_ln 一致）；
    * ω₂² = w2_A2F·ω_D² = ω_D²/2（α²F/ω 权重约定）；
    * ⟨ω²⟩_ph = w2_DOS·ω_D² = 3/5 ω_D²（FE10 约定）；
    * 两二阶矩比 (1/2)/(3/5)=5/6（外部两约定的差＝权重差）；
    * 两对数矩比 e^{-1/3}/e^{-1/2}=e^{1/6}（审-17 分歧的精确来源）；
    * λ_chain=A ω_D²、同位素 ω_D∝M^{-1/2} ⇒ λ∝1/M。

  外部依据（只作工具，不写成 CQM=Eliashberg）：
    Kiessling–Altshuler–Yuzbashyan 2025：λ=2∫α²F/ω、α²F∝ω²；
    Pickett arXiv:2204.05930 §II.5：ω₂、ω_log 矩；FE10：⟨ω²⟩=3/5ω_D²。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

open scoped BigOperators

namespace CQM.SpectralMoments

noncomputable section

/-- 标准 Debye 矩的无量纲值（微积分给、数值脚本验证）；仅作代数载体。 -/
def wNorm : ℝ := 1          -- ∫₀¹ 2x dx
def logM : ℝ := -(1 / 2)    -- ∫₀¹ 2x ln x dx
def w2A2F : ℝ := 1 / 2      -- ∫₀¹ 2x·x² dx（α²F/ω 权重）
def w2DOS : ℝ := 3 / 5      -- ∫₀¹ 3x⁴ dx / ∫₀¹ 3x² dx（声子 DOS 权重，FE10）

/-- $\omega_{\log}=\omega_D e^{\mathrm{logM}}=e^{-1/2}\omega_D$。 -/
lemma wlog_chain (w : ℝ) : w * Real.exp logM = w * Real.exp (-(1 : ℝ) / 2) := by
  unfold logM
  ring_nf

/-- $\omega_2^2=\mathrm{w2A2F}\cdot\omega_D^2=\omega_D^2/2$。 -/
lemma w2_chain (w : ℝ) : w2A2F * w ^ 2 = w ^ 2 / 2 := by
  unfold w2A2F
  ring

/-- $\langle\omega^2\rangle_{\rm ph}=\mathrm{w2DOS}\cdot\omega_D^2=\frac35\omega_D^2$（FE10）。 -/
lemma w2_ph (w : ℝ) : w2DOS * w ^ 2 = (3 / 5 : ℝ) * w ^ 2 := by
  unfold w2DOS
  ring

/-- 两二阶矩之比 $\frac{1/2}{3/5}=\frac56$：外部 $\frac12$ 与 $\frac35$ 约定的差＝权重差。 -/
lemma moment_ratio : w2A2F / w2DOS = 5 / 6 := by
  unfold w2A2F w2DOS
  norm_num

/-- 两对数矩之比 $e^{-1/3}/e^{-1/2}=e^{1/6}$（`审-17` 分歧的精确来源）。 -/
lemma moment_gap : Real.exp (-(1 : ℝ) / 3) / Real.exp (-(1 : ℝ) / 2) = Real.exp ((1 : ℝ) / 6) := by
  rw [← Real.exp_sub]
  congr 1
  ring

/-- $\lambda_{\rm chain}=A\omega_D^2$（$A=A_{\rm eph}$ 外生归一）。 -/
lemma lambda_chain (A w : ℝ) : 2 * A * (w ^ 2 / 2) = A * w ^ 2 := by
  ring

/-- 同位素：$\omega_D=k/\sqrt M$ ⇒ $\lambda=A k^2/M\propto1/M$。 -/
lemma isotope_lambda (A k M : ℝ) (hM : 0 < M) :
    A * (k / Real.sqrt M) ^ 2 = (A * k ^ 2) / M := by
  field_simp
  rw [Real.sq_sqrt (le_of_lt hM)]

/-- 常耦合 $\alpha^2F=A\omega^2$ 的形状单调（小 $\omega$ 行为，$\omega$ 非负）。 -/
lemma a2f_mono (A w1 w2 : ℝ) (hA : 0 ≤ A) (h1 : 0 ≤ w1) (h12 : w1 ≤ w2) :
    A * w1 ^ 2 ≤ A * w2 ^ 2 := by
  have hp : w1 ^ 2 ≤ w2 ^ 2 := sq_le_sq.mpr (by rw [abs_of_nonneg h1, abs_of_nonneg (le_trans h1 h12)]; exact h12)
  exact mul_le_mul_of_nonneg_left hp hA

end
end CQM.SpectralMoments
