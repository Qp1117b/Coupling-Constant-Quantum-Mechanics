import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-!
# R2: Cooper 对数的链内来源（代数核）

形式化工作台 `03_推导工作台/环节9_Cooper对数从12A.md` 的代数核：
- 谱阶梯 E_k = E2 k^2（审-15, p=2）；
- 荷分支权重 w_k = 1/k（12.A3）；
- 加权模密度 rho = w / (dE/dk) = 1/(2E) —— Cooper 对数核；
- 绕分支 w_k = k 给常数密度（无对数）；
- 自洽反解给非解析能标 E_lo = E_hi exp(-2/lambda)。

不引入新 axiom；不使用 sorry / admit / native_decide / unsafe。
自洽积分结构取自 BCS（外部工具），不写成 CQM 定理。
-/

namespace CQM.CooperLog

noncomputable section

open Real

/-- 模式 n=2k 的能量：ln E_n = 2 ln n + c ⇒ E_{2k} = E2 * k^2。 -/
def modeEnergy (E2 : ℝ) (k : ℕ) : ℝ := E2 * (k : ℝ) ^ 2

/-- 荷量子分支 (12.A3) 的权重 w_{2k} = 1/k。 -/
def chargeWeight (k : ℕ) : ℝ := 1 / (k : ℝ)

/-- 绕数分支 (临-6 另一支) 的权重 w_{2k} = k。 -/
def windingWeight (k : ℕ) : ℝ := (k : ℝ)

/-- 能量对档号的导数 dE/dk = 2 E2 k（把 k 连续化）。 -/
def dEdk (E2 : ℝ) (k : ℕ) : ℝ := 2 * E2 * (k : ℝ)

/-- 荷分支的加权模密度 rho = w / (dE/dk) = 1/(2E)。 -/
theorem charge_density_is_coopernucleus
    (E2 : ℝ) (k : ℕ) (hE2 : E2 ≠ 0) (hk : (k : ℝ) ≠ 0) :
    chargeWeight k / dEdk E2 k = 1 / (2 * modeEnergy E2 k) := by
  unfold chargeWeight dEdk modeEnergy
  field_simp [hE2, hk]

/-- 绕分支的加权模密度与 k 无关（常数，无对数核）。 -/
theorem winding_density_is_constant (E2 : ℝ) (k : ℕ) (hE2 : E2 ≠ 0) (hk : (k : ℝ) ≠ 0) :
    windingWeight k / dEdk E2 k = 1 / (2 * E2) := by
  unfold windingWeight dEdk
  field_simp [hE2, hk]

/-- 两分支密度之比 = k^2：荷分支随能量衰减，绕分支不衰减。 -/
theorem branch_density_ratio (E2 : ℝ) (k : ℕ) (hE2 : E2 ≠ 0) (hk : (k : ℝ) ≠ 0) :
    (chargeWeight k / dEdk E2 k) / (windingWeight k / dEdk E2 k) = 1 / (k : ℝ) ^ 2 := by
  unfold chargeWeight windingWeight dEdk
  field_simp [hE2, hk]

/-- 自洽方程 1 = (lambda/2) log(Ehi/Elo) 的非解析反解。 -/
theorem exponential_scale
    (lam Ehi Elo : ℝ) (hl : 0 < lam) (hh : 0 < Ehi) (he : 0 < Elo)
    (h : (lam / 2) * Real.log (Ehi / Elo) = 1) :
    Elo = Ehi * Real.exp (-(2 / lam)) := by
  have hratio : 0 < Ehi / Elo := div_pos hh he
  have hlog : Real.log (Ehi / Elo) = 2 / lam := by
    calc
      Real.log (Ehi / Elo) = (2 / lam) * ((lam / 2) * Real.log (Ehi / Elo)) := by
        field_simp [hl.ne']
      _ = (2 / lam) * 1 := by rw [h]
      _ = 2 / lam := by ring
  have hexp : Ehi / Elo = Real.exp (2 / lam) := by
    rw [← hlog]
    exact (Real.exp_log hratio).symm
  calc
    Elo = Ehi / (Ehi / Elo) := by field_simp [hh.ne', he.ne']
    _ = Ehi / Real.exp (2 / lam) := by rw [hexp]
    _ = Ehi * Real.exp (-(2 / lam)) := by
      rw [div_eq_mul_inv, ← Real.exp_neg]

/-- 非解析能标随 lambda 单调增（lambda 越大越不易指数压制）。 -/
theorem exp_scale_monotone (lam1 lam2 : ℝ) (h1 : 0 < lam1) (h12 : lam1 ≤ lam2) :
    Real.exp (-(2 / lam1)) ≤ Real.exp (-(2 / lam2)) := by
  apply Real.exp_le_exp.mpr
  have hinv : 1 / lam2 ≤ 1 / lam1 := one_div_le_one_div_of_le h1 h12
  have h1' : -(2 / lam1) = -2 * (1 / lam1) := by ring
  have h2' : -(2 / lam2) = -2 * (1 / lam2) := by ring
  rw [h1', h2']
  exact mul_le_mul_of_nonpos_left hinv (by norm_num : (-2 : ℝ) ≤ 0)

end
end CQM.CooperLog
