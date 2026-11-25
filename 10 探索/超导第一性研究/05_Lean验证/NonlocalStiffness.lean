import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-!
# CQM：非局域区与 $q\to0$ 外推（第 153 轮，R-162）

承载 (19NL.2)–(19NL.4) 的代数部分：

* `inductance_ratio`：$L_q=L_0/(1-a)\Rightarrow L_q/L_0=1/(1-a)$；
* `ratio_ge_one`：$0\le a<1\Rightarrow 1\le1/(1-a)$（单向高估）；
* `tolerance_threshold`：$Au^2\le\epsilon\leftrightarrow u^2\le\epsilon/A$；
* `b_upper_bound`：$L_0\le L_q\Rightarrow L_0/L_b\le L_q/L_b$（$\mathcal{B}$ 的上界）；
* `bkt_shift_ratio`：$T\propto\Upsilon\Rightarrow T_q/T_0=\Upsilon_q/\Upsilon_0$。

全部为纯代数，无 axiom、无 sorry、无 native_decide。
-/

namespace CQM.NonlocalStiffness

/-- (19NL.2)：$L_q=L_0/(1-a)$ ⇒ 比值 $=1/(1-a)$。 -/
theorem inductance_ratio {L0 Lq a : ℝ} (hL0 : L0 ≠ 0)
    (hLq : Lq = L0 / (1 - a)) : Lq / L0 = 1 / (1 - a) := by
  subst hLq
  field_simp

/-- 方向：$0\le a<1$ ⇒ $1\le1/(1-a)$，即有限 $q$ 高估片电感。 -/
theorem ratio_ge_one {a : ℝ} (h0 : 0 ≤ a) (h1 : a < 1) : 1 ≤ 1 / (1 - a) := by
  have hpos : (0 : ℝ) < 1 - a := by linarith
  rw [le_div_iff₀ hpos]
  linarith

/-- (19NL.4)：$A>0$ 时 $Au^2\le\epsilon\iff u^2\le\epsilon/A$。 -/
theorem tolerance_threshold {A u eps : ℝ} (hA : 0 < A) :
    A * u ^ 2 ≤ eps ↔ u ^ 2 ≤ eps / A := by
  constructor
  · intro h
    rw [le_div_iff₀ hA]
    nlinarith
  · intro h
    rw [le_div_iff₀ hA] at h
    nlinarith

/-- (19NL.3)：$\mathcal{B}$ 的单向上界。 -/
theorem b_upper_bound {L0 Lq Lb : ℝ} (hLb : 0 < Lb) (h : L0 ≤ Lq) :
    L0 / Lb ≤ Lq / Lb := by
  have hd : 0 ≤ (Lq - L0) / Lb := div_nonneg (by linarith) (le_of_lt hLb)
  rw [sub_div] at hd
  linarith

/-- 方向链：$T=c\Upsilon$ ⇒ 温度比等于刚度比。 -/
theorem bkt_shift_ratio {Tq T0 Uq U0 c : ℝ} (hTq : Tq = c * Uq) (hT0 : T0 = c * U0)
    (hU0 : U0 ≠ 0) (hc : c ≠ 0) : Tq / T0 = Uq / U0 := by
  subst hTq
  subst hT0
  field_simp

end CQM.NonlocalStiffness
