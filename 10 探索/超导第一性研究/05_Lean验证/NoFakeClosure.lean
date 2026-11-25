import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Data.Real.Basic

/-!
# R27: 假闭合识别的代数核

R26 接续比代入 (9.1)(10.2) 后是恒等式 κ_f/g = κ_f/g —— 无独立信息，不能解 g。
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.NoFakeClosure

noncomputable section

/-- (9.1) 方差读出 与 (10.2) 配对强度 的比值定义。 -/
def varRead (k s r : ℝ) : ℝ := 2 * k^2 * s * (1 - r)
def pairStr (g s r hw : ℝ) : ℝ := 4 * g^2 * s * (1 - r) / hw

/-- R26 右端 sqrt(2 var/(hw pair)) 的平方 = (k/g)^2 —— 恒等，无新约束。 -/
theorem junction_is_identity (k g s r hw : ℝ)
    (hs : s ≠ 0) (hr : 1 - r ≠ 0) (hg : g ≠ 0) (hkw : hw ≠ 0) :
    2 * varRead k s r / (hw * pairStr g s r hw) = (k / g)^2 := by
  unfold varRead pairStr
  field_simp [hs, hr, hg, hkw]
  ring

/-- 恒等式不提供 g 的独立方程：给定 k0，任意非零比值都对应一个 g ⇒ g 自由。 -/
theorem g_not_determined (k0 : ℝ) (hk0 : k0 ≠ 0) (ratio : ℝ) (hratio : ratio ≠ 0) :
    let g := k0 / ratio
    g ≠ 0 ∧ k0 / g = ratio := by
  dsimp
  constructor
  · exact div_ne_zero hk0 hratio
  · field_simp [hk0, hratio]

end
end CQM.NoFakeClosure
