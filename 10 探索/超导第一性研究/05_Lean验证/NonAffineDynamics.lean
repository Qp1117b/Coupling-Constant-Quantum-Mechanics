/-
  第 138 轮：非仿射扇区无链内动力学
  ==========================================================================
  承接 R145（im Ã ⊆ N_I = (im B)^⊥）与 R146（刚度谱 = sv(Ã)，上缘有界）。
  本轮判定 (4.1″) 的第一项能不能存在：

      ⟨(Δε)²⟩_T = Σ_{k∈N_I} |A v_k|² c_k⁰ [1 + 2n_B] + b n_d(T)

  **核心定理**：若 $\dot\ell = B\dot x$，则 $\dot\ell\in N_I$ 只能是零。
  证明：$\dot\ell \perp \operatorname{im}B \ni B\dot x$，故
  $|\dot\ell|^2 = \langle B\dot x,\dot\ell\rangle = 0$。

  于是顶点动能 $T=\frac12 m|\dot x|^2$ 在 $N_I$ 上恒为零，
  $M_\ell = (B^+)^\top B^+|_{N_I} = 0$，而 $c_k^0=\hbar/(2\sqrt{\sigma_kM_k})$
  在 $M_k=0$ 处发散 ⇒ 第一项不是有限物理量。

  其余：Arrhenius 支的对数斜率、对激活能的单调性、弗兰克角能的二次标度。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Algebra.Module.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Order.Basic

open scoped InnerProductSpace Real

namespace CQM.NonAffineDynamics

/-! ### 一、非仿射方向的速度恒为零 -/

variable {U V : Type*}
variable [AddCommGroup U] [Module ℝ U]
variable [NormedAddCommGroup V] [InnerProductSpace ℝ V]

/-- **主定理**：若 $\ell$ 与 $\operatorname{im}B$ 正交，且 $\ell$ 可由某个速度 $x$ 实现，
    则 $\ell=0$。即非仿射扇区里没有可实现的速度。 -/
theorem nonaffine_velocity_zero (B : U →ₗ[ℝ] V) (x : U) (l : V)
    (hl : ∀ y : U, ⟪B y, l⟫_ℝ = 0) (hx : B x = l) : l = 0 := by
  have h1 : ⟪B x, l⟫_ℝ = 0 := hl x
  rw [hx] at h1
  exact inner_self_eq_zero.mp h1

/-- 推论：$N_I$ 上唯一的可实现速度是零速度（对任何试探速度）。 -/
theorem nonaffine_no_motion (B : U →ₗ[ℝ] V) (l : V)
    (hl : ∀ y : U, ⟪B y, l⟫_ℝ = 0) :
    ¬ ∃ x : U, B x = l ∧ l ≠ 0 := by
  rintro ⟨x, hx, hne⟩
  exact hne (nonaffine_velocity_zero B x l hl hx)

/-! ### 二、零点幅度发散 -/

/-- 单个简谐模的零点方差 $\hbar/(2\sqrt{\sigma M})$（$\hbar=1$ 归一）。 -/
noncomputable def zeroPointVar (σ M : ℝ) : ℝ := 1 / (2 * Real.sqrt (σ * M))

/-- **发散**：固定 $\sigma>0$，$M\to0^+$ 时零点方差无界。 -/
theorem zero_point_diverges (σ : ℝ) (hσ : 0 < σ) :
    ∀ A : ℝ, ∃ M : ℝ, 0 < M ∧ A < zeroPointVar σ M := by
  intro A
  -- 取 M 足够小
  by_cases hA : A ≤ 0
  · refine ⟨1 / σ, ?_, ?_⟩
    · positivity
    · unfold zeroPointVar
      have hpos : 0 < 2 * Real.sqrt (σ * (1 / σ)) := by
        have : σ * (1 / σ) = 1 := by field_simp
        rw [this]; norm_num
      have : 0 < 1 / (2 * Real.sqrt (σ * (1 / σ))) := by positivity
      linarith
  · have hApos : 0 < A := not_le.mp hA
    -- A > 0：取 M = 1/(σ (4A)²)，则 √(σM)=1/(4A)，零点方差 = 2A > A
    refine ⟨1 / (σ * (4 * A) ^ 2), ?_, ?_⟩
    · have : 0 < σ * (4 * A) ^ 2 := by positivity
      positivity
    · unfold zeroPointVar
      have hσM : σ * (1 / (σ * (4 * A) ^ 2)) = 1 / (4 * A) ^ 2 := by
        field_simp
      rw [hσM]
      have hsq : Real.sqrt (1 / (4 * A) ^ 2) = 1 / (4 * A) := by
        rw [show (1 : ℝ) / (4 * A) ^ 2 = (1 / (4 * A)) ^ 2 by field_simp]
        exact Real.sqrt_sq (by positivity)
      rw [hsq]
      have h4A : 0 < 4 * A := by positivity
      have hfin : (1 : ℝ) / (2 * (1 / (4 * A))) = 2 * A := by
        field_simp
        norm_num
      rw [hfin]
      linarith

/-! ### 三、缺陷激活支 -/

/-- 向错对的激活密度 $n_d=e^{-E_c/T}$。 -/
noncomputable def defectDensity (Ec T : ℝ) : ℝ := Real.exp (-(Ec / T))

/-- Arrhenius 对数线性：$\ln n_d = -E_c\cdot(1/T)$。 -/
theorem defect_log_slope (Ec T : ℝ) (hT : 0 < T) :
    Real.log (defectDensity Ec T) = -Ec * (1 / T) := by
  unfold defectDensity
  rw [Real.log_exp]
  field_simp

/-- 激活能越大，同一温度下密度越小。 -/
theorem defect_density_antitone_Ec {Ec1 Ec2 T : ℝ}
    (hT : 0 < T) (h : Ec1 < Ec2) :
    defectDensity Ec2 T < defectDensity Ec1 T := by
  unfold defectDensity
  apply Real.exp_lt_exp.mpr
  have : Ec1 / T < Ec2 / T := by
    rw [div_lt_div_iff_of_pos_right hT]; exact h
  linarith

/-- 弗兰克角能的二次标度：$E_c\propto f^2$，$f\to2f$ 给 $E_c\to4E_c$。 -/
theorem frank_energy_quadratic (κ f : ℝ) :
    κ * (2 * f) ^ 2 = 4 * (κ * f ^ 2) := by ring

end CQM.NonAffineDynamics
