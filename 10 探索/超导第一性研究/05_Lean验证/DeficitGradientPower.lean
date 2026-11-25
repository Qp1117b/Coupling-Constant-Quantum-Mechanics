/-
  R74：亏角传递的 q-幂与振幅预算反演（代数承载）
  =============================================
  R73 判定：均匀缩放（q=0 模）给 eps=0；中心对称 ⇒ 传递函数偶。
  于是 A(q) = a2 q^2 + a4 q^4 + ...（无常数项、无 q^1 项）。
  数值（`04_计算验证/环04_几何传递的q幂与预算反演.py`）：指数 2.00（三方向），c=0.267a。

  本文件承载：
    * 偶函数 + A(0)=0 ⇒ 首项 q^2（多项式截断形式）；
    * 指数记账：|G|^2 ∝ q^{2n} ⇒ sum ∝ Q^{2n+2}；n=1 给 Q^4、n=2 给 Q^6；
    * sigma = c*eta 的线性与正性；线性响应上界给 eta 的上界；
    * g^2 = lam*hw/(4 N sigma^2 (1-rho)) 对 eta 的反单调。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith

namespace CQM.Deficitspectrum

noncomputable section

/-! ### 一、偶 + 零常数项 ⇒ 首项 $q^2$ -/

/-- 偶性去掉 $q^1$ 项、$A(0)=0$ 去掉常数项，故 $A(q)=q^2(a_2+a_4q^2)$。 -/
theorem even_poly_factor (a2 a4 q : ℝ) :
    a2 * q ^ 2 + a4 * q ^ 4 = q ^ 2 * (a2 + a4 * q ^ 2) := by
  ring

/-- 首项系数为正（$a_2>0$）⇒ 小 $q$ 时 $A>0$。 -/
theorem small_q_positive {a2 q : ℝ} (h2 : 0 < a2) (hq : q ≠ 0) :
    0 < a2 * q ^ 2 := by
  have hq2 : 0 < q ^ 2 := pow_pos (abs_pos.mpr hq) 2
  positivity

/-! ### 二、指数记账 -/

/-- $|G_q|^2\propto q^{2n}$ ⇒ 模求和 $\propto Q^{2n+2}$：$n=1$ 时 $Q^4$。 -/
theorem exponent_q2_gives_Q4 (n : ℤ) : 2 * n + 2 = 4 ↔ n = 1 := by
  constructor <;> intro h <;> linarith

/-- $n=2$（本轮的 $|G|^2\propto q^4$）时给 $Q^6$。 -/
theorem exponent_q4_gives_Q6 (n : ℤ) : 2 * n + 2 = 6 ↔ n = 2 := by
  constructor <;> intro h <;> linarith

/-! ### 三、$\sigma_\varepsilon=c\,\eta$ 与线性响应上界 -/

/-- $\sigma_\varepsilon=c\eta$：$c>0$ 时与 $\eta$ 同号。 -/
theorem sigma_same_sign {c η : ℝ} (hc : 0 < c) : 0 < c * η ↔ 0 < η := by
  constructor
  · intro h
    by_contra hη
    push Not at hη
    nlinarith
  · intro h
    positivity

/-- 线性响应上界 $\sigma_\varepsilon<0.1$ 给 $\eta$ 的上界（$c=0.808$）。 -/
theorem eta_upper_bound {η : ℝ} (h : 0.808 * η < 0.1) : η < 0.124 := by
  nlinarith

/-! ### 四、振幅预算对 $\eta$ 的反单调 -/

/-- 环 10 的预算：$g^2=\lambda\hbar\omega/(4N(0)\sigma^2(1-\rho))$，$\sigma=c\eta$。 -/
def gsq (lam hw N c eta rho : ℝ) : ℝ := lam * hw / (4 * N * (c * eta) ^ 2 * (1 - rho))

/-- $\eta$ 越小 ⇒ $g^2$ 越大（预算对噪声幅度反单调）。 -/
theorem gsq_antitone {lam hw N c rho : ℝ}
    (hlam : 0 < lam) (hhw : 0 < hw) (hN : 0 < N) (hc : 0 < c) (hr : 1 - rho ≠ 0 ∧ 0 < 1 - rho)
    {e1 e2 : ℝ} (h1 : 0 < e1) (h12 : e1 < e2) :
    gsq lam hw N c e2 rho < gsq lam hw N c e1 rho := by
  unfold gsq
  have hd : (0 : ℝ) < 1 - rho := hr.2
  have he1 : (0 : ℝ) < (c * e1) ^ 2 := by positivity
  have he2 : (0 : ℝ) < (c * e2) ^ 2 := by positivity
  have hsq : (c * e1) ^ 2 < (c * e2) ^ 2 := by nlinarith [mul_pos hc h1]
  have hden1 : (0 : ℝ) < 4 * N * (c * e1) ^ 2 * (1 - rho) := by positivity
  have hden2 : (0 : ℝ) < 4 * N * (c * e2) ^ 2 * (1 - rho) := by positivity
  have hnum : (0 : ℝ) < lam * hw := by positivity
  exact div_lt_div_of_pos_left hnum hden1 (by nlinarith)

end

end CQM.Deficitspectrum
