import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Data.Real.Basic
import Mathlib.Data.Real.Sqrt
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-!
# R5: 由参与比计数导出 CQM 态密度形状（代数核）

- 计数函数 N(E) = n_eff sqrt(E/E2)（E=E2 k^2 的反解）
- DOS g(E) = dN/dE = n_eff/(2 sqrt(E2 E)) ∝ E^{-1/2}
- 对数矩 omega_log = omega_D exp(-2)（积分已在解析层给出，这里证代数核）
- Cooper integrand g/E ∝ E^{-3/2} 收敛（R4 no-go 从 DOS 侧确认）

无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.ModeDOS

noncomputable section

open Real

/-- 反解：E = E2 k^2 ⇒ k = sqrt(E/E2)。 -/
theorem count_inverse (E2 : ℝ) (k : ℕ) (hE2 : 0 < E2) (hk : 0 < (k : ℝ)) :
    Real.sqrt ((E2 * (k : ℝ) ^ 2) / E2) = (k : ℝ) := by
  have hdiv : (E2 * (k : ℝ) ^ 2) / E2 = (k : ℝ) ^ 2 := by
    field_simp [hE2.ne']
  rw [hdiv, Real.sqrt_sq_eq_abs, abs_of_pos hk]

/-- DOS 分母恒等：2 E2 k = 2 sqrt(E2 · E)，其中 E = E2 k^2。 -/
theorem dos_denominator (E2 : ℝ) (k : ℕ) (hE2 : 0 < E2) (hk : 0 < (k : ℝ)) :
    2 * E2 * (k : ℝ) = 2 * Real.sqrt (E2 * (E2 * (k : ℝ) ^ 2)) := by
  rw [show E2 * (E2 * (k : ℝ) ^ 2) = (E2 * (k : ℝ)) ^ 2 by ring]
  rw [Real.sqrt_sq_eq_abs, abs_of_pos (mul_pos hE2 hk)]
  ring

/-- DOS 形状：dN/dE = n_eff/(2 E2 k) = n_eff/(2 sqrt(E2 E)) ∝ E^{-1/2}。 -/
theorem dos_shape (neff E2 : ℝ) (k : ℕ) (hE2 : 0 < E2) (hk : 0 < (k : ℝ)) :
    neff / (2 * E2 * (k : ℝ)) =
      neff / (2 * Real.sqrt (E2 * (E2 * (k : ℝ) ^ 2))) := by
  rw [dos_denominator E2 k hE2 hk]

/-- 离散 DOS 单项：w_k/E_k = 1/(E2 k^3) —— Cooper integrand 的 k^-3 衰减（R4 同构）。 -/
theorem cooper_integrand_term (E2 : ℝ) (k : ℕ) (hE2 : E2 ≠ 0) (hk : (k : ℝ) ≠ 0) :
    (1 / (k : ℝ)) / (E2 * (k : ℝ) ^ 2) = 1 / (E2 * (k : ℝ) ^ 3) := by
  field_simp [hE2, hk]

/-- 对数矩的代数核：积分比 = ln W - 2 ⇒ exp = W e^{-2}。 -/
theorem log_moment_algebra (W : ℝ) (hW : 0 < W) :
    Real.exp (Real.log W - 2) = W * Real.exp (-2 : ℝ) := by
  calc
    Real.exp (Real.log W - 2) = Real.exp (Real.log W) / Real.exp (2 : ℝ) := by
      rw [Real.exp_sub]
    _ = W / Real.exp (2 : ℝ) := by rw [Real.exp_log hW]
    _ = W * Real.exp (-(2 : ℝ)) := by
      rw [div_eq_mul_inv, ← Real.exp_neg]

/-- 两矩刻度比：e^{-5/3} 与 e^{-3/2} 均为正且小于 1（态密度层不同的定量差）。 -/
theorem moment_ratio_lt_one (a : ℝ) (ha : 0 < a) : Real.exp (-a) < 1 := by
  rw [← Real.exp_zero]
  exact Real.exp_lt_exp.mpr (by linarith : -a < 0)

end
end CQM.ModeDOS
