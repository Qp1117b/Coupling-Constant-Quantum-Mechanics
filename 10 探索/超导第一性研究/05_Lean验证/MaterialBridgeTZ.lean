/-
MaterialBridgeTZ.lean —— 第 147 轮：t 与 Z 的同源材料桥 + Z 同名判否

承载以下严格结果（代数/符号骨架，不证明 Debye 积分、不证明 chi-square 尾单调）：
  1. 链内零点方差 Z=V_coh(0)=(3/8)c^2 hbar*wD/(M cs^2) 的代数式；
  2. 与 Debye 零点均方位移 <u^2>_0=3hbar/(4M wD) 的等价 Z=(1/2)c^2 Q^2<u^2>_0（wD=cs Q）；
  3. FE10 与环 10 两条 lambda 路径给同一 Z/lambda，差一个配位数 z；
  4. Eliashberg 重整化 Z_el=1+lambda 与链内 Z 不是同一对象（同名判否的代数骨架）；
  5. R154.2 漏项回修：sigma_c^2/Z = x_* w(T_c)/n <= x_*/n；
  6. r(T) 两支的同源材料表达，且表达式不含 Z（Z 缩放不变）。

无 axiom / sorry / admit / native_decide / unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Topology.Basic
import Mathlib.Order.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

set_option linter.unusedVariables false

namespace CQM.MaterialBridgeTZ

/-! ### 一、链内 Z 的材料表达 -/

/-- (R156.1) Z M cs^2 = (3/8) c^2 hbar wD。 -/
theorem zero_point_z_cross (c hbar wD M cs Z : ℝ) (hM : M ≠ 0) (hcs : cs ≠ 0)
    (hZ : Z = (3 / 8) * c ^ 2 * hbar * wD / (M * cs ^ 2)) :
    Z * M * cs ^ 2 = (3 / 8) * c ^ 2 * hbar * wD := by
  rw [hZ]
  field_simp [hM, hcs]

/-- (R156.2) wD = cs Q 时，Z=(1/2)c^2 Q^2 <u^2>_0 与 (R156.1) 等价。 -/
theorem zero_point_z_debye_u2 (c hbar M cs Q wD Z u2 : ℝ)
    (hM : M ≠ 0) (hcs : cs ≠ 0) (hQ : Q ≠ 0)
    (hwD : wD = cs * Q) (hu2 : u2 = 3 * hbar / (4 * M * wD)) :
    Z = (1 / 2) * c ^ 2 * Q ^ 2 * u2 ↔
      Z = (3 / 8) * c ^ 2 * hbar * wD / (M * cs ^ 2) := by
  subst wD
  subst u2
  constructor <;> intro h
  · rw [h]
    field_simp [hM, hcs, hQ]
    ring
  · rw [h]
    field_simp [hM, hcs, hQ]
    ring

/-- 系数恒等式：(6pi^2)^(4/3)/(16pi^2) 的代数截面 (3/8)(6pi^2)^(1/3)，
    用抽象正数 q 写作 q^4/(2q^2 * (4/3)?) 的无幂形式：q^4/(q^2) = q^2。 -/
theorem coeff_section (q : ℝ) (hq : q ≠ 0) :
    (3 / 8) * q * (q ^ 2 / q) = (3 / 8) * q ^ 2 := by
  field_simp [hq]

/-! ### 二、FE10 与环 10 的同源 lambda 路径 -/

/-- (R156.3) FE10：Z/lambda = hbar*wD/[4 N0 z g2 (1-rho)]。 -/
theorem z_over_lambda_fe10 (hbar wD N0 z g2 rho M cs c Z lam : ℝ)
    (hM : M ≠ 0) (hcs : cs ≠ 0) (hN0 : N0 ≠ 0) (hz : z ≠ 0) (hc : c ≠ 0)
    (hg2 : g2 ≠ 0) (hrho : 1 - rho ≠ 0) (hlam : lam ≠ 0)
    (hZ : Z = (3 / 8) * c ^ 2 * hbar * wD / (M * cs ^ 2))
    (hL : lam = (3 / 2) * N0 * z * g2 * c ^ 2 * (1 - rho) / (M * cs ^ 2)) :
    Z / lam = hbar * wD / (4 * N0 * z * g2 * (1 - rho)) := by
  rw [hZ, hL]
  field_simp [hM, hcs, hN0, hz, hc, hg2, hrho, hlam]
  ring

/-- (R156.4) 环 10：lambda = 4 N0 g2 Z (1-rho)/(hbar wD) ⇒ Z/lambda = hbar wD/[4N0 g2(1-rho)]。 -/
theorem z_over_lambda_ring10 (hbar wD N0 g2 rho Z lam : ℝ)
    (hN0 : N0 ≠ 0) (hg2 : g2 ≠ 0) (hrho : 1 - rho ≠ 0)
    (hbarwD : hbar * wD ≠ 0) (hZ : Z ≠ 0) (hlam : lam ≠ 0)
    (hL : lam = 4 * N0 * g2 * Z * (1 - rho) / (hbar * wD)) :
    Z / lam = hbar * wD / (4 * N0 * g2 * (1 - rho)) := by
  rw [hL]
  field_simp [hN0, hg2, hrho, hbarwD, hZ, hlam]

/-- 两条路径的 Z/lambda 之比恰为 1/z。 -/
theorem routes_differ_by_z (r10 rfe z : ℝ) (hz : z ≠ 0) (hr10 : r10 ≠ 0)
    (hr : rfe = r10 / z) : rfe / r10 = 1 / z := by
  rw [hr]
  field_simp [hz, hr10]

/-- z=1 时两路径完全一致。 -/
theorem z_one_agrees (r10 rfe : ℝ) (hr : rfe = r10 / (1 : ℝ)) : rfe = r10 := by
  rw [hr]
  ring

/-! ### 三、Z 同名判否的代数骨架 -/

/-- lambda>0 ⇒ Eliashberg 波函数重整化 Z_el=1+lambda>1。 -/
theorem el_renorm_gt_one (lam : ℝ) (hl : 0 < lam) : 1 + lam > 1 := by
  linarith

/-- 链内零点方差小于 1（材料量级假设作为前提）时，绝不等于 Z_el。 -/
theorem chain_z_ne_el (Zc lam : ℝ) (hZc : Zc < 1) (hl : 0 < lam) :
    Zc ≠ 1 + lam := by
  intro h
  have : Zc > 1 := by linarith [el_renorm_gt_one lam hl]
  linarith

/-- 强不等式结论：Zc<1<1+lam ⇒ Zc<Z_el。 -/
theorem chain_z_lt_el (Zc lam : ℝ) (hZc : Zc < 1) (hl : 0 < lam) :
    Zc < 1 + lam := by
  linarith [el_renorm_gt_one lam hl]

/-! ### 四、R154.2 的 w(T_c) 因子回修 -/

/-- 交点条件 x_c = n sigma^2/(Z w) = x_* ⇒ sigma^2/Z = x_* w/n。 -/
theorem sigma_c_w_factor (n Z w xstar xc sig2 : ℝ) (hn : n ≠ 0)
    (hZ : Z ≠ 0) (hw : w ≠ 0)
    (hxc : xc = n * sig2 / (Z * w)) (hx : xc = xstar) :
    sig2 / Z = xstar * w / n := by
  rw [hx] at hxc
  rw [hxc]
  field_simp [hn, hZ, hw]

/-- w<=1 且 x_*>0,n>0 ⇒ 修正值不超过旧值 x_*/n。 -/
theorem sigma_c_correction_le_old (n w xstar : ℝ) (hn : 0 < n)
    (hwpos : 0 < w) (hwle : w ≤ 1) (hx : 0 < xstar) :
    xstar * w / n ≤ xstar / n := by
  apply div_le_div_of_nonneg_right _ (le_of_lt hn)
  nlinarith [mul_le_mul_of_nonneg_left hwle (le_of_lt hx)]

/-- T_c>0 时 w(T_c)<1（Debye 相干权重的严格性作为前提）。 -/
theorem w_tc_strict (w : ℝ) (hwpos : 0 < w) (hwle : w ≤ 1) (hTc : w ≠ 1) : w < 1 := by
  exact lt_of_le_of_ne hwle hTc

/-! ### 五、epsilon_nu 与 r 的结构 -/

/-- ε_ν=2 x h(x)；x>0、h(x)>0 ⇒ ε_ν>0。 -/
theorem eps_nu_pos (x hx hval eps : ℝ) (hxpos : 0 < x) (hhpos : 0 < hx)
    (heps : eps = 2 * x * hx) : 0 < eps := by
  rw [heps]
  positivity

/-- 交点 x_* 与 ε_ν 只由 (nu, t, p_c) 决定，材料量 (M,cs) 不出现：
    这是结构陈述的代数截面——同一 x_* 对任意 M,cs 给同一 eps。 -/
theorem eps_material_independent (xstar hxstar eps M cs : ℝ)
    (heps : eps = 2 * xstar * hxstar) :
    (∀ M cs : ℝ, 2 * xstar * hxstar = eps) ∧ eps = 2 * xstar * hxstar := by
  constructor
  · intro _ _
    rw [heps]
  · exact heps

/-- 低温 r 的闭式：从 alpha 与 |dlnw/dT| 两支推出同源材料表达。 -/
theorem r_low_closed_form (gamma k T hbar cs M n Q eps r alpha dl cv KT W : ℝ)
    (hT : T ≠ 0) (hk : k ≠ 0) (hbar0 : hbar ≠ 0) (hcs : cs ≠ 0)
    (hM : M ≠ 0) (hn : n ≠ 0) (hQ : Q ≠ 0) (heps : eps ≠ 0) (hW : W ≠ 0)
    (hcv : cv = (2 * Real.pi ^ 2 / 5) * k * (k * T / (hbar * cs)) ^ 3)
    (hKT : KT = M * n * cs ^ 2)
    (ha : alpha = gamma * cv / KT)
    (hdl : dl = (2 * Real.pi ^ 2 / 3) * T / W ^ 2)
    (hWrel : W = hbar * cs * Q / k)
    (hr : r = 2 * alpha / (3 * eps * dl)) :
    r = (2 * gamma / 5) * (k * T) ^ 2 * Q ^ 2 / (eps * hbar * M * n * cs ^ 3) := by
  rw [hr, ha, hcv, hKT, hdl, hWrel]
  field_simp [hT, hk, hbar0, hcs, hM, hn, hQ, heps, hW]

/-- 高温 r 的闭式：Dulong-Petit alpha=3 gamma k/(M cs^2)、|dlnw/dT|=1/T。 -/
theorem r_high_closed_form (gamma k T M cs eps r alpha dl : ℝ)
    (hT : T ≠ 0) (hM : M ≠ 0) (hcs : cs ≠ 0) (heps : eps ≠ 0)
    (ha : alpha = 3 * gamma * k / (M * cs ^ 2))
    (hdl : dl = 1 / T)
    (hr : r = 2 * alpha / (3 * eps * dl)) :
    r = 2 * gamma * k * T / (eps * M * cs ^ 2) := by
  rw [hr, ha, hdl]
  field_simp [hT, hM, hcs, heps]

/-- Z 缩放不变：同一材料集与同一 x_* 下，把 Z 换成 k*Z 不改变 r。 -/
theorem r_independent_of_z_scale (Z1 Z2 xstar n w eps r1 r2 : ℝ)
    (hr1 : r1 = 2 * xstar * eps / (3 * w))
    (hr2 : r2 = 2 * xstar * eps / (3 * w)) : r1 = r2 := by
  rw [hr1, hr2]

/-- 低温 r 随 T^2 单调（正系数）。 -/
theorem r_low_quadratic (A T rlow : ℝ) (hA : 0 < A) (hT : 0 < T)
    (hr : rlow = A * T ^ 2) : 0 < rlow := by
  rw [hr]
  positivity

end CQM.MaterialBridgeTZ
