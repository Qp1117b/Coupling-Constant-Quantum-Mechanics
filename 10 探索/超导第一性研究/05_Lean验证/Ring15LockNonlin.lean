-- 环 15 / 审-6（第 181 轮）：锁条件的非线性映射 λ = ln√(1−ε/2π)
-- 只 import Spec（不 import 其他证明模块）；三条：一阶系数、严格单调减、指数反解。
import Ring15Spec

namespace CQM.Ring15.LockNonlin

open CQM.Ring15.Spec

/-- $1-\varepsilon/2\pi>0$ 由 $\varepsilon<2\pi$ 给出（$\pi>0$）。 -/
lemma one_sub_div_pos {e : ℝ} (he : e < 2 * Real.pi) : 0 < 1 - e / (2 * Real.pi) := by
  have hπ : (0 : ℝ) < 2 * Real.pi := by positivity
  have h : e / (2 * Real.pi) < 1 := (div_lt_one hπ).mpr he
  linarith

/-- 一阶系数：$\lambda'(e)=-\dfrac{1}{2(2\pi-e)}$。 -/
theorem lockLam_deriv (e : ℝ) (he : e < 2 * Real.pi) :
    HasDerivAt lockLam (-(1 / (2 * (2 * Real.pi - e)))) e := by
  have hπ : (0 : ℝ) < 2 * Real.pi := by positivity
  have hpos := one_sub_div_pos he
  have hne : (1 : ℝ) - e / (2 * Real.pi) ≠ 0 := ne_of_gt hpos
  have hinner :
      HasDerivAt (fun y : ℝ => 1 - y / (2 * Real.pi)) (-(1 / (2 * Real.pi))) e := by
    have h1 : HasDerivAt (fun y : ℝ => y / (2 * Real.pi)) (1 / (2 * Real.pi)) e :=
      (hasDerivAt_id e).div_const (2 * Real.pi)
    simpa using (hasDerivAt_const (x := e) (c := (1 : ℝ))).sub h1
  have hlog := HasDerivAt.log hinner hne
  have hmul := HasDerivAt.const_mul (1 / 2 : ℝ) hlog
  have hv :
      (1 / 2 : ℝ) * ((-(1 / (2 * Real.pi))) / (1 - e / (2 * Real.pi)))
        = -(1 / (2 * (2 * Real.pi - e))) := by
    have h2 : (2 * Real.pi - e) ≠ 0 := by
      have : (0 : ℝ) < 2 * Real.pi - e := by linarith
      exact ne_of_gt this
    field_simp
  simpa only [lockLam, hv] using hmul

/-- 严格单调减：$e_1<e_2<2\pi\Rightarrow\lambda(e_2)<\lambda(e_1)$。 -/
theorem lockLam_anti : StrictAntiOn lockLam (Set.Iio (2 * Real.pi)) := by
  intro a _ b hb hab
  have hπ : (0 : ℝ) < 2 * Real.pi := by positivity
  have hbpos : 0 < 1 - b / (2 * Real.pi) := one_sub_div_pos hb
  have hlt : 1 - b / (2 * Real.pi) < 1 - a / (2 * Real.pi) := by
    have : a / (2 * Real.pi) < b / (2 * Real.pi) := div_lt_div_of_pos_right hab hπ
    linarith
  have hlog := Real.log_lt_log hbpos hlt
  simp only [lockLam]
  linarith

/-- 指数反解：$\exp(2\lambda)=1-\varepsilon/2\pi$。 -/
theorem lockLam_exp (e : ℝ) (he : e < 2 * Real.pi) :
    Real.exp (2 * lockLam e) = 1 - e / (2 * Real.pi) := by
  have hpos := one_sub_div_pos he
  have h2 : 2 * lockLam e = Real.log (1 - e / (2 * Real.pi)) := by
    simp only [lockLam]
    ring
  rw [h2, Real.exp_log hpos]

/-- Spec 主定理一。 -/
theorem targetPropLockLamDeriv : TargetPropLockLamDeriv := fun e he => lockLam_deriv e he

/-- Spec 主定理二。 -/
theorem targetPropLockLamAnti : TargetPropLockLamAnti := lockLam_anti

/-- Spec 主定理三。 -/
theorem targetPropLockLamExp : TargetPropLockLamExp := fun e he => lockLam_exp e he

end CQM.Ring15.LockNonlin

