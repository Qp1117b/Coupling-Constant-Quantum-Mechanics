/-
  环 15：锁定因子逸度通道与 t(T) 的代数骨架（第 150 轮，R-159）
  仅承载纯实代数：t 的定义式、比值序引理、离散 log 导数判据、
  逸度对 x 的单调性、t≥1。跨界的 Debye/卡方单调性由数值脚本负责。
-/
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity

open Real

namespace CQM.TChannel

/-- t 的定义式（15L.4）：`t = 1 + ln(1-y)/ln p`。 -/
noncomputable def tEff (p y : ℝ) : ℝ := 1 + Real.log (1 - y) / Real.log p

/-- 比值序引理：`0<a1≤a2`、`0<b2≤b1` ⇒ `a1/b1≤a2/b2`。 -/
theorem ratio_le_ratio {a1 a2 b1 b2 : ℝ}
    (ha1 : 0 < a1) (ha : a1 ≤ a2) (hb2 : 0 < b2) (hb : b2 ≤ b1) :
    a1 / b1 ≤ a2 / b2 := by
  have hb1 : 0 < b1 := lt_of_lt_of_le hb2 hb
  have ha2 : 0 ≤ a2 := le_trans (le_of_lt ha1) ha
  rw [div_le_div_iff₀ hb1 hb2]
  calc a1 * b2 ≤ a2 * b2 := mul_le_mul_of_nonneg_right ha (le_of_lt hb2)
    _ ≤ a2 * b1 := mul_le_mul_of_nonneg_left hb ha2

/-- 离散 log 导数判据：`δ/L ≤ (δ+dδ)/(L+dL) ↔ dδ·L ≥ δ·dL`（`L,L+dL>0`）。 -/
theorem ratio_step_ge (δ dδ L dL : ℝ) (hL : 0 < L) (hL2 : 0 < L + dL) :
    δ / L ≤ (δ + dδ) / (L + dL) ↔ dδ * L ≥ δ * dL := by
  rw [div_le_div_iff₀ hL hL2]
  constructor
  · intro h; nlinarith [h]
  · intro h; nlinarith [h]

/-- 逸度 `y(x)=2π e^{-c/x}` 对 `x>0` 单调增（`c>0`）。 -/
theorem fugacity_mono {c x1 x2 : ℝ} (hc : 0 < c) (hx1 : 0 < x1) (hx12 : x1 ≤ x2) :
    2 * π * Real.exp (-(c / x1)) ≤ 2 * π * Real.exp (-(c / x2)) := by
  have hx2 : 0 < x2 := lt_of_lt_of_le hx1 hx12
  have hinv : 1 / x2 ≤ 1 / x1 := one_div_le_one_div_of_le hx1 hx12
  have hc_inv : c * (1 / x2) ≤ c * (1 / x1) :=
    mul_le_mul_of_nonneg_left hinv (le_of_lt hc)
  have hcx : c / x2 ≤ c / x1 := by
    simpa [div_eq_mul_inv] using hc_inv
  have hneg : -(c / x1) ≤ -(c / x2) := neg_le_neg hcx
  have hexp : Real.exp (-(c / x1)) ≤ Real.exp (-(c / x2)) := Real.exp_le_exp.mpr hneg
  exact mul_le_mul_of_nonneg_left hexp (mul_nonneg (by norm_num) (le_of_lt Real.pi_pos))

/-- `y ↦ -ln(1-y)` 在 `[0,1)` 上单调增。 -/
theorem negLog_one_sub_mono {y1 y2 : ℝ} (h12 : y1 ≤ y2) (h2 : y2 < 1) :
    -Real.log (1 - y1) ≤ -Real.log (1 - y2) := by
  have ha : 0 < 1 - y2 := by linarith
  have hab : 1 - y2 ≤ 1 - y1 := by linarith
  have hlog : Real.log (1 - y2) ≤ Real.log (1 - y1) := Real.log_le_log ha hab
  linarith

/-- `t ≥ 1`：`0<p<1`、`0≤y<1` 时 `1 ≤ tEff p y`。 -/
theorem tEff_ge_one {p y : ℝ} (hp : 0 < p) (hp1 : p < 1) (hy : 0 ≤ y) (hy1 : y < 1) :
    1 ≤ tEff p y := by
  unfold tEff
  have hlogp : Real.log p < 0 := Real.log_neg hp hp1
  have hlog1y : Real.log (1 - y) ≤ 0 := by
    apply Real.log_nonpos
    · linarith
    · linarith
  have hquot : 0 ≤ Real.log (1 - y) / Real.log p := by
    have heq : Real.log (1 - y) / Real.log p = (-Real.log (1 - y)) / (-Real.log p) := by
      field_simp
    rw [heq]
    exact div_nonneg (by linarith) (by linarith)
  linarith

/-- `y=0` 时 `t=1`（对任意 `p`，因 `ln 1 = 0` 且 `0/ln p = 0`）。 -/
theorem tEff_zero (p : ℝ) : tEff p 0 = 1 := by
  unfold tEff
  simp

/-- 热有效逸度在给定通道下界：`x = k_BT/Υ_bare`，`E_c/(kT) = (π²/2)/x`。 -/
theorem fugacity_at_crit (β : ℝ) (hβ : 0 < β) :
    2 * π * Real.exp (-((π^2 / 2) / β))
      = 2 * π * Real.exp (-(π^2 / (2 * β))) := by
  have hβ0 : β ≠ 0 := ne_of_gt hβ
  congr 1
  field_simp

end CQM.TChannel
