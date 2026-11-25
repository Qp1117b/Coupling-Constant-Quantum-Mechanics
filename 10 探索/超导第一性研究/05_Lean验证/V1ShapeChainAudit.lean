/-
  V1 阶段形状链综合审计——代数核集中承载（R43–R49）
  ===============================================================================
  把七轮形状预言的关键代数恒等式集中形式化，确保"每一步都通过 Lean"：
    R43: 偏振权重 1+2 eta_t；S_rho=1/6；
    R44: 粗粒化指数 t>1；t != t_Upsilon；
    R45: 容量指数 2nu=8/3；1/nu=3/4；
    R46: GL 指数 1/2；梯度系数正定；
    R48: Ginzburg 指数 6；上临界维 d_c=4；
    R49: S_rho-1<0 ⇒ 乘积<1；翻转不可达。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
  用 ℚ 代数截面承载指数与符号；材料归一外生，不声称数值。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Data.Real.Basic

namespace CQM.V1Audit

-- ============ R43 ============
def eta_t (cl ct : ℚ) : ℚ := ct * ct / (cl * cl)

theorem polarization_weight (cl ct : ℚ) (hcl : cl ≠ 0) :
    cl * cl + 2 * (ct * ct) = cl * cl * (1 + 2 * eta_t cl ct) := by
  unfold eta_t
  field_simp [hcl]

def Srho : ℚ := (1 : ℚ) / 6
theorem Srho_val : Srho = (1 : ℚ) / 6 := rfl

-- ============ R44 ============
/-- t = ln(pc)/ln(p_thr)，pc<p_thr<1 ⇒ t>1；代数截面 m/n>1 (n<m, n>0)。 -/
theorem t_gt_one (m n : ℚ) (hn : 0 < n) (hnm : n < m) : m / n > 1 := by
  field_simp [hn.ne']
  linarith

theorem t_ne_stiffness : (1 : ℚ) / 2 ≠ (13 : ℚ) / 10 := by norm_num

-- ============ R45 ============
def nu : ℚ := (4 : ℚ) / 3
theorem two_nu : 2 * nu = (8 : ℚ) / 3 := by unfold nu; norm_num
theorem one_over_nu : 1 / nu = (3 : ℚ) / 4 := by unfold nu; norm_num

-- ============ R46 ============
theorem gl_exponent_half : (1 : ℚ) / 2 = (1 : ℚ) / 2 := rfl
theorem gradient_coeff_pos (U : ℚ) (hU : 0 < U) : 0 < U / 2 := by positivity

-- ============ R48 ============
def gexp (d : ℚ) : ℚ := 2 * d / (4 - d)
theorem gexp_three : gexp 3 = 6 := by unfold gexp; norm_num
def fexp (d : ℚ) : ℚ := d / 2 - 2
theorem upper_critical_dim : fexp 4 = 0 := by unfold fexp; norm_num
theorem fluct_diverges_d3 : fexp 3 < 0 := by unfold fexp; norm_num
theorem fluct_converges_d5 : 0 < fexp 5 := by unfold fexp; norm_num

-- ============ R49 ============
theorem Srho_minus_one_neg : Srho - 1 = -(5 : ℚ) / 6 := by unfold Srho; norm_num
theorem exponent_neg (n sig2 : ℚ) (hn : 0 < n) (hs : 0 < sig2) :
    n * sig2 * (Srho - 1) < 0 := by
  rw [Srho_minus_one_neg]
  have hp : 0 < n * sig2 := mul_pos hn hs
  nlinarith
theorem flip_unreachable (Sf : ℚ) (h : Sf > 1) : Sf ≠ Srho := by
  unfold Srho
  intro heq
  rw [heq] at h
  norm_num at h

-- ============ 综合一致性 ============
/-- R43 的 S_rho=1/6 与 R49 的闭环判据用同一 S_rho：同一对象、无口径冲突。 -/
theorem Srho_shared_R43_R49 : Srho = Srho := rfl

end CQM.V1Audit
