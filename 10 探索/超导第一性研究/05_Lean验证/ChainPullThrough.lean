import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Data.Real.Basic
import Mathlib.Data.Real.Sqrt
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-!
# R3: 环 4→10→12→14→环节⑨ 的形状拉通（代数核）

形式化 `03_推导工作台/全链R1R2拉通_Tc形状.md` 的代数核：
指数替换 (R3.1)、归一映射 (R3.3)、同位素质量无关、
对 c_eps^2 与 (1-rho) 的单调方向。
不自洽方程整体、前因子 p、物理同一均不写成定理。
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.ChainPullThrough

noncomputable section

open Real

/-- R1 的 lambda 几何式（CQM-L3）。 -/
def lambdaGeom (N0 z g cE rho Q M omegaD : ℝ) : ℝ :=
  (3 / 2 : ℝ) * N0 * z * g ^ 2 * cE ^ 2 * (1 - rho) * Q ^ 2 / (M * omegaD ^ 2)

/-- (R3.1)：omegaD = c Q 时 2/lambda_geom = 4 M c^2 / (3 N0 z g^2 cE^2 (1-rho))。 -/
theorem exponent_substitution
    (N0 z g cE rho Q M c : ℝ)
    (hN0 : N0 ≠ 0) (hz : z ≠ 0) (hg : g ≠ 0) (hcE : cE ≠ 0)
    (hrho : 1 - rho ≠ 0) (hQ : Q ≠ 0) (hM : M ≠ 0) (hc : c ≠ 0) :
    2 / lambdaGeom N0 z g cE rho Q M (c * Q) =
      4 * M * c ^ 2 / (3 * N0 * z * g ^ 2 * cE ^ 2 * (1 - rho)) := by
  unfold lambdaGeom
  field_simp [hN0, hz, hg, hcE, hrho, hQ, hM, hc]
  ring_nf

/-- (R3.3) 归一映射：lambda_geom = 2 lamChain ⇒ 2/lambda_geom = 1/lamChain。 -/
theorem normalization_map (lamChain : ℝ) (hl : lamChain ≠ 0) :
    2 / (2 * lamChain) = 1 / lamChain := by
  field_simp [hl]

/-- 同位素：M (k/sqrt M)^2 = k^2，指数中 M c^2 与 c^2 ~ 1/M 抵消。 -/
theorem isotope_exponent_mass_free (k M : ℝ) (hM : 0 < M) :
    M * (k / Real.sqrt M) ^ 2 = k ^ 2 := by
  rw [div_pow]
  rw [Real.sq_sqrt (le_of_lt hM)]
  field_simp [hM.ne']

/-- exp(-C/x) 在 x>0、C>0 时随 x 严格增（T* 对 c_eps^2 的指数灵敏度方向）。 -/
theorem exp_neg_c_div_x_strictMono (C x1 x2 : ℝ) (hC : 0 < C) (hx1 : 0 < x1) (h12 : x1 < x2) :
    Real.exp (-C / x1) < Real.exp (-C / x2) := by
  have hx2 : 0 < x2 := lt_trans hx1 h12
  have hinv : 1 / x2 < 1 / x1 := one_div_lt_one_div_of_lt hx1 h12
  have hneg : -C * (1 / x1) < -C * (1 / x2) :=
    mul_lt_mul_of_neg_left hinv (by linarith : -C < 0)
  rw [show -C / x1 = -C * (1 / x1) by ring,
      show -C / x2 = -C * (1 / x2) by ring]
  exact Real.exp_lt_exp.mpr hneg

/-- T* 对关联 rho 单调减：rho 增（1-rho 减）使指数更负。 -/
theorem tc_antitone_in_rho (C r1 r2 : ℝ) (hC : 0 < C)
    (hr2 : 0 < 1 - r2) (hr12 : r1 ≤ r2) :
    Real.exp (-C / (1 - r2)) ≤ Real.exp (-C / (1 - r1)) := by
  have hden : 1 - r2 ≤ 1 - r1 := by linarith
  have hinv : 1 / (1 - r1) ≤ 1 / (1 - r2) := one_div_le_one_div_of_le hr2 hden
  have hneg : -C * (1 / (1 - r2)) ≤ -C * (1 / (1 - r1)) :=
    mul_le_mul_of_nonpos_left hinv (by linarith : -C ≤ 0)
  rw [show -C / (1 - r2) = -C * (1 / (1 - r2)) by ring,
      show -C / (1 - r1) = -C * (1 / (1 - r1)) by ring]
  exact Real.exp_le_exp.mpr hneg

end
end CQM.ChainPullThrough
