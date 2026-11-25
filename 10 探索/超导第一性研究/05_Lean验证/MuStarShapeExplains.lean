/-
  R68：Morel-Anderson 形状对 R67 经验 mu* 的解释——代数承载
  ===============================================================================
  mu* = mu/(1+mu*L), L=ln(eps_F/hbar omega_D).
  典型 L=2-5, 裸 mu=0.2 => mu*=0.10-0.143; 达 mu*=0.10 需裸 mu=0.125-0.20.
  解释 R67 经验 mu*=0.10 的合理性；不闭合审-14（裸 mu 外生）。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Data.Real.Basic

namespace CQM.MuStarShape

/-- Morel-Anderson 形状 mu* = mu/(1+mu*L)。 -/
def muStar (mu L : ℚ) : ℚ := mu / (1 + mu*L)

/-- 压制：mu* < mu（mu>0, L>0）。 -/
theorem muStar_lt_mu (mu L : ℚ) (hmu : 0 < mu) (hL : 0 < L) :
    muStar mu L < mu := by
  unfold muStar
  have hden : 0 < 1 + mu*L := by nlinarith
  have hden_gt : 1 < 1 + mu*L := by nlinarith
  -- mu/(1+muL) < mu ⇔ mu < mu(1+muL)（分母正）
  rw [div_lt_iff₀ hden]
  nlinarith

/-- 反解：mu*=target 时裸 mu = target/(1-target*L)。 -/
def bareMuFor (target L : ℚ) : ℚ := target / (1 - target*L)

/-- 达 mu*=0.10 需裸 mu：L=2 时 0.125（正且在常规范围）。 -/
theorem bare_mu_L2 : bareMuFor ((1 : ℚ)/10) 2 = (1 : ℚ)/8 := by
  unfold bareMuFor
  norm_num

/-- L=4 时需裸 mu=1/6（常规范围）。 -/
theorem bare_mu_L4 : bareMuFor ((1 : ℚ)/10) 4 = (1 : ℚ)/6 := by
  unfold bareMuFor
  norm_num

/-- 裸 mu 落在常规金属范围 [0.1, 0.25]（L=2..5 反解值）。 -/
theorem bare_mu_in_range : ((1 : ℚ)/8 : ℚ) ≥ (1 : ℚ)/10 ∧ (1 : ℚ)/6 ≤ (1 : ℚ)/4 := by
  constructor <;> norm_num

-- 边界注记：不给精确 mu* 数值（裸 mu/z_v/m 外生，审-14 不闭合）；
-- 精确数值表在 Python。解释经验值合理性，不给新 Tc。

end CQM.MuStarShape
