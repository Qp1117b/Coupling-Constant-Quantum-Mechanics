import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-!
# CQM：Pearl–London 口径统一（第 152 轮，R-161）

承载 (19PL.1)–(19PL.12) 的代数部分：

* `pearl_convention_transfer`：约定 $\Lambda=c\lambda^2/d$ 与 $d/\lambda^2=c/\Lambda$ 等价；
* `readout_ratio`：两种读法之比为 $cx/d$（(19PL.4)(19PL.11)）；
* `kinetic_inductance_identity`：片动能电感表述与 London 表述恒等（(19PL.3)）；
* `scale_degeneracy`：$(\lambda,d)\mapsto(s\lambda,s^2d)$ 使刚度不变（(19PL.5)）；
* `bkt_kinetic_line`：BKT 线的无约定形式（(19PL.12)）。

全部为纯代数恒等式，无 axiom、无 sorry、无 native_decide。
-/

namespace CQM.PearlLondon

/-- (19PL.1)(19PL.9)：约定 $\Lambda=c\lambda^2/d$ 等价于 $d/\lambda^2=c/\Lambda$。 -/
theorem pearl_convention_transfer {d lam Lam c : ℝ} (hd : d ≠ 0) (hlam : lam ≠ 0)
    (hc : c ≠ 0) (hΛ : Lam = c * lam ^ 2 / d) : d / lam ^ 2 = c / Lam := by
  subst hΛ
  field_simp

/-- (19PL.4)(19PL.11)：读作 $\Lambda$ 与读作 $\lambda$ 的刚度比等于 $cx/d$。 -/
theorem readout_ratio {C x d c : ℝ} (hC : C ≠ 0) (hx : x ≠ 0) (hd : d ≠ 0)
    (hc : c ≠ 0) : (C * c / x) / (C * d / x ^ 2) = c * x / d := by
  field_simp

/-- (19PL.3)：$L=\mu_0\lambda^2/d$ ⇒ $\hbar^2d/(4\mu_0e^2\lambda^2)=\hbar^2/(4e^2L)$。 -/
theorem kinetic_inductance_identity {d lam L h2 mu0 e2 : ℝ} (hd : d ≠ 0)
    (hlam : lam ≠ 0) (hmu0 : mu0 ≠ 0) (he2 : e2 ≠ 0)
    (hL : L = mu0 * lam ^ 2 / d) :
    h2 * d / (4 * mu0 * e2 * lam ^ 2) = h2 / (4 * e2 * L) := by
  subst hL
  field_simp

/-- (19PL.5)：$(\lambda,d)\mapsto(s\lambda,s^2d)$ 保持 $d/\lambda^2$ 不变。 -/
theorem scale_degeneracy {d lam s : ℝ} (hd : d ≠ 0) (hlam : lam ≠ 0) (hs : s ≠ 0) :
    d / lam ^ 2 = s ^ 2 * d / (s * lam) ^ 2 := by
  field_simp

/-- (19PL.12)：$\Lambda=C/T$ 且 $C=\pi\hbar^2/(4\mu_0e^2k_B)$ ⇒
$L=\mu_0\Lambda/2=\pi\hbar^2/(8e^2k_BT)$。 -/
theorem bkt_kinetic_line {h2 e2 kB T mu0 C : ℝ} (hT : T ≠ 0) (hmu0 : mu0 ≠ 0)
    (he2 : e2 ≠ 0) (hkB : kB ≠ 0)
    (hC : C = Real.pi * h2 / (4 * mu0 * e2 * kB)) :
    mu0 * (C / T) / 2 = Real.pi * h2 / (8 * e2 * kB * T) := by
  subst hC
  field_simp
  ring

end CQM.PearlLondon
