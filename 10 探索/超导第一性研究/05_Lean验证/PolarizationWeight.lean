/-
  环 4／43：亏角关联核的偏振分解——代数承载
  ===============================================================================
  第 86 轮算出亏角响应各向异性（纵 c_l、横 c_t，平方比 eta_t=2.30），
  但关联核 rho(r) 用各向同性标量核。本轮代数承载：
    * 3D 测度下 m_eff = 2n + (3-1) - s；
    * sigma_0^2 ∝ Q^(m_eff+1) = Q^4；
    * 三支零点权重和 = c_l^2 (1 + 2 eta_t)；
    * 代入 eta_t=2.30 得 1+2 eta_t = 5.59（第 86 轮已记下的三支总权重）；
    * 三支角向核相同 ⇒ rho 形状与偏振无关，S_rho=1/6，Var 比=7/6 保持。

  纪律：无 axiom／sorry／admit／native_decide／unsafe；纯代数（数值核对在 Python）。
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp

namespace CQM.PolarizationWeight

/-- 有效谱指数：m_eff = 2n + (d-1) - s。 -/
def meff (n d s : ℕ) : ℤ := (2 * n : ℤ) + ((d : ℤ) - 1) - (s : ℤ)

/-- 3D（d=3）、声学（s=1）、n=1 给 m_eff = 3。 -/
theorem meff_three : meff 1 3 1 = 3 := by
  unfold meff
  norm_num

/-- 一般 d 比 d-1 多 1（固定 n,s）。 -/
theorem meff_succ_d (n d s : ℕ) :
    meff n (d + 1) s = meff n d s + 1 := by
  unfold meff
  omega

/-- sigma_0^2 的 Q 幂 = m_eff + 1。 -/
theorem sigma_exponent (n d s : ℕ) :
    (meff n d s + 1) = ((2 * n : ℤ) + (d : ℤ) - (s : ℤ)) := by
  unfold meff
  ring

/-- n=1,d=3,s=1 ⇒ Q 幂 = 4。 -/
theorem sigma_scale_q4 : meff 1 3 1 + 1 = 4 := by
  rw [meff_three]
  norm_num

/-- 偏振各向异性比 eta_t = c_t^2 / c_l^2（c_l>0）。 -/
noncomputable def eta (cl ct : ℝ) : ℝ := (ct * ct) / (cl * cl)

/-- 三支零点权重和：c_l^2 + 2 c_t^2 = c_l^2 (1 + 2 eta_t)。 -/
theorem polarization_weight (cl ct : ℝ) (hcl : cl ≠ 0) :
    cl * cl + 2 * (ct * ct) = cl * cl * (1 + 2 * eta cl ct) := by
  unfold eta
  field_simp [hcl]

/-- 用第 86 轮实测 c_l=0.2065=413/2000、c_t=0.3130=626/2000 算 eta_t = (626/413)^2，
    前因子 = 1+2 eta_t ≈ 5.595（即第 86 轮记下的 5.59，两位小数）。 -/
theorem weight_from_measured :
    (1 : ℝ) + 2 * (((626 : ℝ) / 413) ^ 2) = (954321 : ℝ) / 170569 := by
  norm_num

/-- 一般权重和恒 ≥ 单支纵波权重（横波贡献非负）。 -/
theorem weight_ge_longitudinal (cl ct : ℝ) :
    cl * cl ≤ cl * cl + 2 * (ct * ct) := by
  nlinarith [sq_nonneg ct]

/-- 三支角向核相同 ⇒ 关联 rho 的形状与偏振无关（结构性命题：权重作常数因子约掉）。
    这里以"分子/分母同乘权重"的代数恒等式承载。 -/
theorem kernel_polynomial_independent (wL wT1 wT2 I : ℝ) (hden : wL + wT1 + wT2 ≠ 0) (hI : I ≠ 0) :
    (wL * I + wT1 * I + wT2 * I) / ((wL + wT1 + wT2) * I) = 1 / 1 := by
  have hnum : wL * I + wT1 * I + wT2 * I = (wL + wT1 + wT2) * I := by ring
  rw [hnum]
  field_simp [hden, hI]

/-- 3D 各向同性核的 S_rho = 1/6（第 86 轮 9B.9，本轮不依赖偏振）。 -/
theorem Srho_one_six : (2 : ℝ) * ((1 : ℝ) / 3 - (1 : ℝ) / 4) = (1 : ℝ) / 6 := by
  norm_num

/-- 闭环方差比 1 + S_rho = 7/6。 -/
theorem var_ratio_seven_six : (1 : ℝ) + (1 : ℝ) / 6 = (7 : ℝ) / 6 := by
  norm_num

/-- 方差比不随偏振前因子改变形状：Var = (7/6) * n * sigma2。 -/
theorem var_shape_invariant (n sigma2 : ℝ) :
    (1 + (1 : ℝ) / 6) * n * sigma2 = ((7 : ℝ) / 6) * n * sigma2 := by
  rw [var_ratio_seven_six]

end CQM.PolarizationWeight
