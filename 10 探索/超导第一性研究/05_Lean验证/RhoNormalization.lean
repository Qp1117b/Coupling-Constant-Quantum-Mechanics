import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# 环 4／15：`rho` 归一与载体符号判别的代数骨架（第 157 轮）

只承载代数与序；不证明 Bessel 积分、二元正态展开、载体实现。
无 `axiom`／`sorry`／`admit`／`native_decide`／`unsafe`。
-/

namespace CQM.RhoNormalization

noncomputable section

/-- **位移合成**：$\bar c=\rho\phi^2$、$\delta=\bar c/(2p)$ ⇒ $\delta=\rho\phi^2/(2p)$。 -/
theorem delta_of_rho {rho phi2 p del cbar : ℝ}
    (hc : cbar = rho * phi2) (hd : del = cbar / (2 * p)) :
    del = rho * phi2 / (2 * p) := by
  rw [hc] at hd
  rw [hd]

/-- **正关联给正位移**。 -/
theorem delta_pos {rho phi2 p del : ℝ} (hrho : 0 < rho) (hphi : 0 < phi2)
    (hp : 0 < p) (h : del = rho * phi2 / (2 * p)) : 0 < del := by
  rw [h]
  positivity

/-- **负关联给负位移**。 -/
theorem delta_neg {rho phi2 p del : ℝ} (hrho : rho < 0) (hphi : 0 < phi2)
    (hp : 0 < p) (h : del = rho * phi2 / (2 * p)) : del < 0 := by
  rw [h]
  have hn : rho * phi2 < 0 := mul_neg_of_neg_of_pos hrho hphi
  exact div_neg_of_neg_of_pos hn (by positivity)

/-- **有效阈值**：$\delta>0$ ⇒ $p_c^{\rm eff}<p_c$；$\delta<0$ ⇒ $p_c^{\rm eff}>p_c$。 -/
theorem pceff_sign {p del pceff : ℝ} (h : pceff = p - del) :
    (0 < del → pceff < p) ∧ (del < 0 → p < pceff) := by
  constructor
  · intro hd
    rw [h]
    linarith
  · intro hd
    rw [h]
    linarith

/-- **偏差同号**：$\Delta g/g=k\delta$、$k>0$ ⇒ 偏差与 $\delta$ 同号。 -/
theorem bias_sign {k del bias : ℝ} (hk : 0 < k) (h : bias = k * del) :
    (0 < del → 0 < bias) ∧ (del < 0 → bias < 0) := by
  constructor
  · intro hd
    rw [h]
    positivity
  · intro hd
    rw [h]
    exact mul_neg_of_pos_of_neg hk hd

end
end CQM.RhoNormalization
