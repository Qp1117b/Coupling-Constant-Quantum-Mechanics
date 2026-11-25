import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Data.Real.Basic
import Mathlib.Data.Real.Sqrt
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-!
# R1: 环 10 的 lambda 几何第一性形状（代数核）

只形式化工作台 `03_推导工作台/环10_lambda几何第一性.md` 的代数核：
hbar 抵消、声学形状、McMillan 型组合、正性、单调性、同位素质量无关性。
不引入新 axiom；不使用 sorry / admit / native_decide / unsafe。
物理识别不写成定理。
-/

namespace CQM.LambdaGeometry

noncomputable section

open Real

/-- 环 4 (d=3) 零点亏角方差 sigma_0^2 = c_eps^2 hbar Q^4 / (16 pi^2 rho_m c)。 -/
def sigma0Sq (hbar cE Q rhoM c : ℝ) : ℝ :=
  cE ^ 2 * hbar * Q ^ 4 / (16 * Real.pi ^ 2 * rhoM * c)

/-- 环 10 (10.2) 配对势 |V| = 4 g^2 sigma_0^2 (1-rho) / (hbar omega)。 -/
def pairingV (hbar g cE Q rhoM c rho omega : ℝ) : ℝ :=
  4 * g ^ 2 * sigma0Sq hbar cE Q rhoM c * (1 - rho) / (hbar * omega)

/-- (CQM-L1) 的 hbar 抵消。 -/
theorem pairingV_hbar_cancel
    (hbar g cE Q rhoM c rho omega : ℝ)
    (hhbar : hbar ≠ 0) (hQ : Q ≠ 0) (hrm : rhoM ≠ 0) (hc : c ≠ 0) :
    pairingV hbar g cE Q rhoM c rho omega =
      g ^ 2 * cE ^ 2 * (1 - rho) * Q ^ 4 / (4 * Real.pi ^ 2 * rhoM * c * omega) := by
  unfold pairingV sigma0Sq
  field_simp [hhbar, hQ, hrm, hc, ne_of_gt Real.pi_pos]
  ring_nf

/-- (CQM-L2) lambda 的声学形状。 -/
def lambdaAcoustic (N0 z g cE Q rhoM c rho : ℝ) : ℝ :=
  N0 * z * g ^ 2 * cE ^ 2 * (1 - rho) * Q ^ 3 / (4 * Real.pi ^ 2 * rhoM * c ^ 2)

/-- (10.3) 壳层归并 + omega = c Q ⇒ (CQM-L2)。 -/
theorem pairingV_to_lambda
    (N0 z hbar g cE Q rhoM c rho : ℝ)
    (hhbar : hbar ≠ 0) (hQ : Q ≠ 0) (hrm : rhoM ≠ 0) (hc : c ≠ 0) :
    N0 * z * pairingV hbar g cE Q rhoM c rho (c * Q) =
      lambdaAcoustic N0 z g cE Q rhoM c rho := by
  unfold pairingV sigma0Sq lambdaAcoustic
  field_simp [hhbar, hQ, hrm, hc, ne_of_gt Real.pi_pos]
  ring_nf

/-- (CQM-L3) McMillan 型无量纲组合 lambda = eta_CQM / (M omega_D^2)。 -/
def lambdaMcMillan (N0 z g cE rho Q M omegaD : ℝ) : ℝ :=
  (3 / 2 : ℝ) * N0 * z * g ^ 2 * cE ^ 2 * (1 - rho) * Q ^ 2 / (M * omegaD ^ 2)

/-- rho_m = M Q^3 / (6 pi^2)、c = omega_D / Q 代入 (CQM-L2) 得 (CQM-L3)。 -/
theorem lambda_acoustic_eq_mcmillan
    (N0 z g cE rho Q M omegaD : ℝ)
    (hQ : Q ≠ 0) (hM : M ≠ 0) (hw : omegaD ≠ 0) :
    lambdaAcoustic N0 z g cE Q (M * Q ^ 3 / (6 * Real.pi ^ 2)) (omegaD / Q) rho =
      lambdaMcMillan N0 z g cE rho Q M omegaD := by
  unfold lambdaAcoustic lambdaMcMillan
  field_simp [hQ, hM, hw, ne_of_gt Real.pi_pos]
  ring_nf

/-- 正性：全部前件为正且 rho < 1 ⇒ lambda > 0（与环 10「无负净耦合」一致）。 -/
theorem lambdaAcoustic_pos
    (N0 z g cE Q rhoM c rho : ℝ)
    (hN0 : 0 < N0) (hz : 0 < z) (hg : g ≠ 0) (hcE : cE ≠ 0)
    (hQ : 0 < Q) (hrm : 0 < rhoM) (hc : 0 < c) (hrho : rho < 1) :
    0 < lambdaAcoustic N0 z g cE Q rhoM c rho := by
  have hg2 : 0 < g ^ 2 := sq_pos_of_ne_zero hg
  have hcE2 : 0 < cE ^ 2 := sq_pos_of_ne_zero hcE
  have hrhopos : 0 < 1 - rho := by linarith
  have hnum : 0 < N0 * z * g ^ 2 * cE ^ 2 * (1 - rho) * Q ^ 3 := by positivity
  have hden : 0 < 4 * Real.pi ^ 2 * rhoM * c ^ 2 := by positivity
  unfold lambdaAcoustic
  exact div_pos hnum hden

/-- rho <= 1 给非负性（M6 关联函数的界）。 -/
theorem lambdaAcoustic_nonneg_of_rho_le_one
    (N0 z g cE Q rhoM c rho : ℝ)
    (hN0 : 0 < N0) (hz : 0 < z)
    (hQ : 0 < Q) (hrm : 0 < rhoM) (hc : 0 < c) (hrho : rho ≤ 1) :
    0 ≤ lambdaAcoustic N0 z g cE Q rhoM c rho := by
  have hrhononneg : 0 ≤ 1 - rho := by linarith
  have hnum : 0 ≤ N0 * z * g ^ 2 * cE ^ 2 * (1 - rho) * Q ^ 3 := by positivity
  have hden : 0 < 4 * Real.pi ^ 2 * rhoM * c ^ 2 := by positivity
  unfold lambdaAcoustic
  exact div_nonneg hnum (le_of_lt hden)

/-- 交易律的代数核：倒数平方单调。 -/
private theorem inverse_square_antitone {x y : ℝ} (hx : 0 < x) (hxy : x ≤ y) :
    (y ^ 2)⁻¹ ≤ (x ^ 2)⁻¹ := by
  have hx2 : 0 < x ^ 2 := sq_pos_of_pos hx
  have hxy2 : x ^ 2 ≤ y ^ 2 := by nlinarith
  simpa [one_div] using (one_div_le_one_div_of_le hx2 hxy2)

/-- 固定 eta_CQM >= 0 时，omega_D 增大 ⇒ lambda 减小。 -/
theorem lambda_antitone_in_omegaD
    (eta w1 w2 : ℝ) (heta : 0 ≤ eta) (hw1 : 0 < w1) (hw12 : w1 ≤ w2) :
    eta / w2 ^ 2 ≤ eta / w1 ^ 2 := by
  have h : (w2 ^ 2)⁻¹ ≤ (w1 ^ 2)⁻¹ := inverse_square_antitone hw1 hw12
  rw [div_eq_mul_inv, div_eq_mul_inv]
  exact mul_le_mul_of_nonneg_left h heta

/-- 同位素自洽：M (k / sqrt M)^2 = k^2，故分母 M omega_D^2 质量无关。 -/
theorem isotope_denominator (k M : ℝ) (hM : 0 < M) :
    M * (k / Real.sqrt M) ^ 2 = k ^ 2 := by
  rw [div_pow]
  rw [Real.sq_sqrt (le_of_lt hM)]
  field_simp [hM.ne']

end
end CQM.LambdaGeometry
