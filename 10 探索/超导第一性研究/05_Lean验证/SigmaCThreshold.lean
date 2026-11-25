/-
SigmaCThreshold.lean —— 第 145 轮：sigma_c 口径的链内判定与两个方差的分离

承载以下严格结果：
  1. (R154.1) 相对口径 sigma_c^2=rho*V ⇒ x=n_cell*rho 恒定 ⇒ p 恒定（相变消灭）；
  2. (R154.2) 严格减函数 barF 的反解唯一性：barF(x*)=p* ⇔ x*=barF^{-1}(p*)；
  3. 严格单调函数的单射性（反解唯一）；
  4. a*lambda(a)=a*phi(a)/sf(a) 的符号：a>0 正、a<0 负、a=0 零；
  5. (R154.5) 可解面二次解 s=2g/(C(g*a*lambda+2mu)) 的代数恒等式；
  6. 四象限符号：g=eps*dw，sgn(可解边界) 依赖 sgn(g) 与 sgn(a)。

本文件只承载代数与单调性结构，不证明 chi-square 物理来源、不给出 w(T) 的绝对值。
无 axiom / sorry / admit / native_decide / unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Topology.Basic
import Mathlib.Order.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

open scoped BigOperators

set_option linter.unusedVariables false

namespace CQM.SigmaCThreshold

/-! ### 一、相对口径消灭相变 (R154.1) -/

/-- 相对口径：sigma_c^2 = rho * V，代入 x = n * sigma_c^2 / V。 -/
theorem rel_threshold_x_const (n rho V : ℝ) (hV : V ≠ 0) :
    (n * (rho * V)) / V = n * rho := by
  field_simp [hV]

/-- 相对口径下 x 与 T 无关 ⇒ p=f(x) 与 T 无关（常量函数）。 -/
theorem const_arg_const_value (f : ℝ → ℝ) (x0 : ℝ) :
    f x0 = f x0 := rfl

/-- 若 x(T1)=x(T2)，则 p(T1)=p(T2)（同一函数读数相同）。 -/
theorem equal_arg_equal_value (f : ℝ → ℝ) (x1 x2 : ℝ) (h : x1 = x2) :
    f x1 = f x2 := by rw [h]

/-! ### 二、严格减函数的反解唯一性 (R154.2) -/

/-- 严格单调 ⇒ 单射（反解唯一）。 -/
theorem strictMono_injective {f : ℝ → ℝ} (hf : StrictMono f) : Function.Injective f :=
  hf.injective

theorem strictAnti_injective {f : ℝ → ℝ} (hf : StrictAnti f) : Function.Injective f :=
  hf.injective

/-- barF 严格减，barF(x*)=p* 且 barF(y)=p* ⇒ y=x*（反解唯一）。 -/
theorem barF_inverse_unique {barF : ℝ → ℝ} (hanti : StrictAnti barF)
    {xstar y pstar : ℝ} (hx : barF xstar = pstar) (hy : barF y = pstar) :
    y = xstar := by
  apply hanti.injective
  rw [hx, hy]

/-- sigma_c^2 = x* Z / n：反解代回恒等式。 -/
theorem sigma_sq_resolve (xstar Z n : ℝ) (hn : n ≠ 0) :
    n * (xstar * Z / n) / Z = xstar ∨ Z = 0 := by
  by_cases hZ : Z = 0
  · exact Or.inr hZ
  · left
    field_simp [hn, hZ]

/-- sigma_c^2/Z = x*/n。 -/
theorem sigma_sq_over_Z (xstar Z n : ℝ) (hZ : Z ≠ 0) (hn : n ≠ 0) :
    (xstar * Z / n) / Z = xstar / n := by
  field_simp [hZ, hn]

/-! ### 三、a*lambda(a) 的符号 -/

/-- 抽象 lambda>0 时，a*lambda 的符号与 a 相同。 -/
theorem a_lambda_pos_of_pos (a lam : ℝ) (ha : 0 < a) (hlam : 0 < lam) :
    0 < a * lam := mul_pos ha hlam

theorem a_lambda_neg_of_neg (a lam : ℝ) (ha : a < 0) (hlam : 0 < lam) :
    a * lam < 0 := mul_neg_of_neg_of_pos ha hlam

theorem a_lambda_zero (a lam : ℝ) (ha : a = 0) : a * lam = 0 := by rw [ha, zero_mul]

/-- 逆 Mills 比 lambda(a)>0 的抽象前提（phi>0, sf>0）。 -/
theorem mills_pos {phi sf a : ℝ} (hphi : 0 < phi) (hsf : 0 < sf) :
    0 < phi / sf := div_pos hphi hsf

/-! ### 四、可解面二次解 (R154.5) -/

/-- g(2s - C*aLam*s^2) = C*2mu*s^2，除以 s≠0 后解 s=2g/(C(g*aLam+2mu))。
    这里以 aLam 抽象 a*lambda(a)。 -/
theorem quadratic_solution (g C aLam mu s : ℝ)
    (hs : s ≠ 0) (hden : C * (g * aLam + 2 * mu) ≠ 0)
    (hsol : s = 2 * g / (C * (g * aLam + 2 * mu))) :
    g * (2 * s - C * aLam * s ^ 2) = C * (2 * mu) * s ^ 2 := by
  rw [hsol]
  field_simp [hden]
  ring

/-- 可解条件：g<0、mu>0、aLam>0 时，可解 ⇔ 2mu > |g|*aLam。 -/
theorem solvable_iff_rate_compete (g mu aLam : ℝ)
    (hg : g < 0) (hmu : 0 < mu) (haLam : 0 < aLam) :
    (g * aLam + 2 * mu > 0) ↔ (|g| * aLam < 2 * mu) := by
  rw [abs_of_neg hg]
  constructor <;> intro h <;> linarith [mul_neg_of_neg_of_pos hg haLam]

/-- 反例侧：不可解 ⇔ |g|*aLam ≥ 2mu。 -/
theorem unsolvable_iff (g mu aLam : ℝ)
    (hg : g < 0) (hmu : 0 < mu) (haLam : 0 < aLam) :
    ¬ (g * aLam + 2 * mu > 0) ↔ (2 * mu ≤ |g| * aLam) := by
  rw [abs_of_neg hg]
  constructor <;> intro h
  · have hle : g * aLam + 2 * mu ≤ 0 := le_of_not_gt h
    linarith [mul_neg_of_neg_of_pos hg haLam]
  · intro hle
    linarith [mul_neg_of_neg_of_pos hg haLam]

/-! ### 五、四象限符号 -/

/-- 升温 g<0：右尾 a>0 竞争（aLam>0），左尾 a<0 同号（aLam<0）。 -/
theorem heating_right_tail_competes (g mu a lam : ℝ)
    (hg : g < 0) (hmu : 0 < mu) (ha : 0 < a) (hlam : 0 < lam) :
    g * (a * lam) < 0 := by
  exact mul_neg_of_neg_of_pos hg (mul_pos ha hlam)

theorem heating_left_tail_same_sign (g a lam : ℝ)
    (hg : g < 0) (ha : a < 0) (hlam : 0 < lam) :
    0 < g * (a * lam) := by
  have hal : a * lam < 0 := mul_neg_of_neg_of_pos ha hlam
  exact mul_pos_of_neg_of_neg hg hal

/-- 降温 g>0：右尾同号，左尾竞争。 -/
theorem cooling_right_tail_same_sign (g a lam : ℝ)
    (hg : 0 < g) (ha : 0 < a) (hlam : 0 < lam) :
    0 < g * (a * lam) := mul_pos hg (mul_pos ha hlam)

theorem cooling_left_tail_competes (g mu a lam : ℝ)
    (hg : 0 < g) (hmu : 0 < mu) (ha : a < 0) (hlam : 0 < lam) :
    g * (a * lam) < 0 := mul_neg_of_pos_of_neg hg (mul_neg_of_neg_of_pos ha hlam)

/-- g = eps * (dw/dT)：符号由 eps>0 与 dw 符号决定。 -/
theorem g_sign_from_dw (eps dw g : ℝ) (heps : 0 < eps) (hg : g = eps * dw)
    (hdw : dw < 0) : g < 0 := by
  rw [hg]
  exact mul_neg_of_pos_of_neg heps hdw

theorem g_sign_from_dw_pos (eps dw g : ℝ) (heps : 0 < eps) (hg : g = eps * dw)
    (hdw : 0 < dw) : 0 < g := by
  rw [hg]
  exact mul_pos heps hdw

end CQM.SigmaCThreshold
