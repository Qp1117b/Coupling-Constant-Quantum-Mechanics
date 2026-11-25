import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Data.Real.Basic

/-!
# R42: 有效质量链内化的自我否证代数核（隔离区）

- 模式谱 E_mode(k) = E2·k²（k=模式序号）
- 电子能带 E_band(q) = ħ²q²/(2m*)（q=电子波矢）
- 两者曲率代数形式相同（d²/dk²=2E2 vs ħ²/m*），但对象不同（模式序号 vs 电子波矢）
- 猜想 m*=ħ²/(2E2) 把两者混同——范畴错误
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.EffectiveMassNoGo

noncomputable section

/-- 链内模式谱 E_mode(k) = E2·k²（k=模式序号）。 -/
def E_mode (E2 k : ℝ) : ℝ := E2 * k ^ 2

/-- 电子能带（抛物线）E_band(q) = ħ²q²/(2m*)（q=电子波矢，链外-D）。 -/
def E_band (hbar2 mstar q : ℝ) : ℝ := hbar2 * q ^ 2 / (2 * mstar)

/-- 模式谱的二阶差分（离散曲率）= 2E2。 -/
theorem mode_curvature (E2 : ℝ) : E_mode E2 2 - 2 * E_mode E2 1 + E_mode E2 0 = 2 * E2 := by
  unfold E_mode
  ring

/-- 抛物线能带的二阶差分（连续曲率 ħ²/m*；离散二阶差分 Q=1 给 ħ²/m*）。 -/
theorem band_curvature (hbar2 mstar : ℝ) (hm : mstar ≠ 0) :
    E_band hbar2 mstar 2 - 2 * E_band hbar2 mstar 1 + E_band hbar2 mstar 0 = hbar2 / mstar := by
  unfold E_band
  field_simp [hm]
  ring

/-- 两种曲率都 ∝"系数"，故数值上可令 hbar2/mstar = 2E2 ⇒ mstar = hbar2/(2E2)。
    但这只在把模式谱当能带时成立——是本卡否证的范畴错误。 -/
theorem formal_mass_guess (hbar2 E2 mstar : ℝ) (hm : mstar ≠ 0) (hE2 : E2 ≠ 0)
    (hcurv : hbar2 / mstar = 2 * E2) : mstar = hbar2 / (2 * E2) := by
  field_simp [hm, hE2] at hcurv ⊢
  linarith

-- 注：formal_mass_guess 的代数成立，但前提 hcurv（把模式曲率当能带曲率）无物理依据——
-- 模式序号 k ∈ ℤ≥1 ≠ 电子波矢 q ∈ BZ（链外-D）。此区分在推导卡文字中陈述。

end
end CQM.EffectiveMassNoGo
