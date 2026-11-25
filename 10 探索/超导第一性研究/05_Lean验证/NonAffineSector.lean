/-
  第 136 轮：环 4 内禀扇区的自由度归属——非仿射子空间与谱正交性
  ==========================================================================
  承接 R73（ε 对位移恒零）、R96（载体定为 ker H 的正交补）、R97（把该载体的谱
  对接余切拉普拉斯＝顶点图算子）。本文件只承载纯代数骨架：

    * 维数计数：N_I = E - (3V-6)；若 E > 6V-6 则 N_I > 3V-6（无限体判据的算术核）。
    * 谱正交性：若 ε∘B = 0（B 为"顶点位移 → 边长变分"），则
        - 顶点扇区的任何位移给出的 ε 为零；
        - 顶点扇区的任何线性组合（＝任何声子本征模、任何顶点基算子的本征矢）的 ε 为零；
        - 因而用顶点谱求和得到的 σ_ε² 恒等于零（R97 的对接给零，不给 R96 的量）；
        - 若 ε(v) ≠ 0，则 v ∉ range B（非零 ε 必在非仿射扇区）。
    * 统计：缺陷激活支 e^{-E/T} 对 T 严格单增，且 ln 对 1/T 严格线性（Arrhenius）。

  外部依据（只作工具）：
    arXiv:1110.6866 §2（线性化 Regge 二阶作用量）；
    arXiv:0912.1817 §4 / arXiv:0810.3594（顶点位移＝Hessian 零模）；
    arXiv:0707.4513 式 27-28（Regge Hessian 非零 sector 由格点拉普拉斯支配，顶点基）。

  与 R97 的判定：R97 的"曲率模 ↔ 余切拉普拉斯非零模"把 E 维边长空间的对象
  对接到 3V 维顶点空间的本征矢上；由 `vertex_spectrum_sigma_zero`，这条路线
  给出的亏角方差**恒为零**，与 R96 要承载的非零零点项不相容。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Algebra.Module.Basic
import Mathlib.Algebra.Module.BigOperators
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Order.Basic

open scoped BigOperators

namespace CQM.NonAffineSector

/-! ### 一、自由度计数：非仿射子空间维数 -/

/-- 非仿射（内禀）子空间的维数 $N_I=E-(3V-6)$，在 $\mathbb Z$ 中取值以免截断减法。 -/
def nonAffineDim (V E : ℤ) : ℤ := E - (3 * V - 6)

/-- 可嵌入方向（顶点自由度）维数。 -/
def vertexDof (V : ℤ) : ℤ := 3 * V - 6

/-- 计数分解：$E=N_I+(3V-6)$。 -/
theorem dim_decomposition (V E : ℤ) :
    nonAffineDim V E + vertexDof V = E := by
  unfold nonAffineDim vertexDof; ring

/-- 无限体判据的算术核：若边数超过 $6V-6$，则非仿射维数超过整个顶点位移空间。 -/
theorem nonAffine_exceeds_vertex (V E : ℤ) (h : 6 * V - 6 < E) :
    vertexDof V < nonAffineDim V E := by
  unfold nonAffineDim vertexDof; linarith

/-- BCC 的边数密度代入：$E\approx 7.13V$ 时 $N_I\approx 4.13V>3V-6$。 -/
theorem bcc_limit_verdict (V : ℤ) (hV : 0 < V) :
    vertexDof V < nonAffineDim V (7 * V) := by
  unfold nonAffineDim vertexDof; linarith

/-! ### 二、谱正交性：顶点扇区不承载亏角 -/

variable {G E F : Type*}
variable [AddCommGroup G] [Module ℝ G]
variable [AddCommGroup E] [Module ℝ E]
variable [AddCommGroup F] [Module ℝ F]

/-- 几何事实的形式陈述：亏角映射 $\varepsilon$ 与"顶点位移 → 边长变分" $B$ 的复合为零。 -/
def Blind (eps : E →ₗ[ℝ] F) (B : G →ₗ[ℝ] E) : Prop := eps.comp B = 0

/-- 单个顶点位移给出的亏角为零（R73 位移盲性）。 -/
theorem vertex_displacement_blind (eps : E →ₗ[ℝ] F) (B : G →ₗ[ℝ] E)
    (h : Blind eps B) (x : G) : eps (B x) = 0 := by
  have hx : (eps.comp B) x = 0 := by rw [h]; rfl
  simpa using hx

/-- 顶点位移的**任何有限线性组合**（＝任何声子本征模、任何顶点基算子的本征矢）
    给出的亏角也为零。 -/
theorem vertex_combination_blind (eps : E →ₗ[ℝ] F) (B : G →ₗ[ℝ] E)
    (h : Blind eps B) {ι : Type*} (s : Finset ι) (c : ι → ℝ) (x : ι → G) :
    eps (∑ i ∈ s, c i • B (x i)) = 0 := by
  rw [map_sum]
  apply Finset.sum_eq_zero
  intro i _
  rw [map_smul, vertex_displacement_blind eps B h, smul_zero]

/-- **决定性推论**：用顶点谱（任何顶点基算子的本征分解）求和得到的亏角方差恒为零。
    即 R97 的"曲率模 ↔ 余切拉普拉斯"路线不能承载 R96 的非零零点项。 -/
theorem vertex_spectrum_sigma_zero (eps : E →ₗ[ℝ] F) (B : G →ₗ[ℝ] E)
    (h : Blind eps B) {ι : Type*} (s : Finset ι) (c : ι → ℝ) (x : ι → G)
    (f : F →ₗ[ℝ] ℝ) :
    f (eps (∑ i ∈ s, c i • B (x i))) = 0 := by
  rw [vertex_combination_blind eps B h s c x, map_zero]

/-- 非零亏角方向必落在顶点扇区之外（即非仿射扇区）。 -/
theorem nonzero_eps_outside_vertex_sector (eps : E →ₗ[ℝ] F) (B : G →ₗ[ℝ] E)
    (h : Blind eps B) (v : E) (hv : eps v ≠ 0) :
    v ∉ LinearMap.range B := by
  intro hmem
  obtain ⟨x, rfl⟩ := hmem
  exact hv (vertex_displacement_blind eps B h x)

/-- 权重形式：若顶点模的传递为零，则它在 (4.1′) 中的权重平方为零。 -/
theorem vertex_mode_weight_zero (transmission c0 : ℝ) (h : transmission = 0)
    (rest : ℝ) : transmission ^ 2 * c0 * rest = 0 := by
  rw [h]; ring

/-- 非仿射模的权重正（传递非零、$c_0>0$、热因子 $>1$）。 -/
theorem nonaffine_mode_weight_pos (transmission c0 a T : ℝ)
    (ht : transmission ≠ 0) (hc0 : 0 < c0) (hT : 0 < T) (ha : 0 < a) :
    0 < transmission ^ 2 * c0 * (1 + 2 / (Real.exp (a / T) - 1)) := by
  have ht2 : 0 < transmission ^ 2 := by positivity
  have hu : 0 < a / T := div_pos ha hT
  have hden : 0 < Real.exp (a / T) - 1 := by
    have : 1 < Real.exp (a / T) := Real.one_lt_exp_iff.mpr hu
    linarith
  have hfac : 0 < 1 + 2 / (Real.exp (a / T) - 1) := by positivity
  exact mul_pos (mul_pos ht2 hc0) hfac

/-! ### 三、缺陷激活支的统计 -/

/-- 缺陷（向错对）激活因子 $y(T)=e^{-E_c/T}$，$E_c>0$。 -/
noncomputable def defectFugacity (Ec T : ℝ) : ℝ := Real.exp (-(Ec / T))

/-- 严格正。 -/
theorem defectFugacity_pos (Ec T : ℝ) : 0 < defectFugacity Ec T := Real.exp_pos _

/-- 对温度严格单增（升温更多缺陷被激活）。 -/
theorem defectFugacity_strictMonoOn (Ec : ℝ) (hEc : 0 < Ec) :
    StrictMonoOn (defectFugacity Ec) (Set.Ioi 0) := by
  intro T1 hT1 T2 hT2 hlt
  unfold defectFugacity
  apply Real.exp_lt_exp.mpr
  have h1 : 0 < T1 := hT1
  have h2 : 0 < T2 := hT2
  have hdiv : Ec / T2 < Ec / T1 := by
    rw [div_lt_div_iff₀ h2 h1]
    exact mul_lt_mul_of_pos_left hlt hEc
  linarith

/-- Arrhenius 对数线性：$\ln y=-E_c\cdot(1/T)$，在 $1/T$ 坐标下是斜率为 $-E_c$ 的直线。 -/
theorem defectFugacity_log_linear (Ec T : ℝ) (hT : 0 < T) :
    Real.log (defectFugacity Ec T) = -Ec * (1 / T) := by
  unfold defectFugacity
  rw [Real.log_exp]
  field_simp

/-- 两支在对数坐标下的渐近行为不同：缺陷支在 $1/T$ 中线性，简谐支饱和于 $2T/a$。 -/
theorem harmonic_saturates_linear (a T : ℝ) (ha : 0 < a) (hT : 0 < T) :
    1 + 2 / (Real.exp (a / T) - 1) ≤ 1 + 2 * (T / a) := by
  have hu : 0 < a / T := div_pos ha hT
  have hden : 0 < Real.exp (a / T) - 1 := by
    have : 1 < Real.exp (a / T) := Real.one_lt_exp_iff.mpr hu
    linarith
  have hge : a / T ≤ Real.exp (a / T) - 1 := by
    have hx := Real.add_one_le_exp (a / T)
    linarith
  have hfrac : 1 / (Real.exp (a / T) - 1) ≤ 1 / (a / T) :=
    one_div_le_one_div_of_le hu hge
  have hrw : 1 / (a / T) = T / a := by field_simp
  rw [hrw] at hfrac
  have h2 : 2 / (Real.exp (a / T) - 1) ≤ 2 * (T / a) := by
    simpa [div_eq_mul_inv] using
      mul_le_mul_of_nonneg_left hfrac (by norm_num : (0 : ℝ) ≤ 2)
  linarith

end CQM.NonAffineSector
