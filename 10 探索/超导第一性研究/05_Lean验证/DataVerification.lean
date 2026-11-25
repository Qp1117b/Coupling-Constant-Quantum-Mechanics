import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Data.Real.Basic
import Mathlib.Data.Real.Sqrt
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-!
# R6: 元素数据对照的代数核

只形式化判定用到的代数/单调结构，不把实验数据或数值常量写成定理：
- gap ratio 2π/e^γ 为正；
- 同位素端点 Tc=A/sqrt(M) 给 Tc(M2)/Tc(M1)^2 = M1/M2（alpha=1/2 的代数核）；
- 弱耦合代理 Tc/thetaD 的分区是判定用的分类（不写数值结论）。

无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.DataVerification

noncomputable section

open Real

/-- gap ratio 2π/e^γ 为正（γ 为外部欧拉常数，仅参数化）。 -/
theorem gap_ratio_pos (gamma : ℝ) : 0 < 2 * Real.pi / Real.exp gamma := by
  positivity

/-- 同位素端点代数核：Tc=A/sqrt(M) ⇒ (Tc(M2)/Tc(M1))^2 = M1/M2。 -/
theorem isotope_endpoint_squared
    (A M1 M2 : ℝ) (hA : 0 < A) (hM1 : 0 < M1) (hM2 : 0 < M2) :
    ((A / Real.sqrt M2) / (A / Real.sqrt M1)) ^ 2 = M1 / M2 := by
  have hcancel : (A / Real.sqrt M2) / (A / Real.sqrt M1) =
      Real.sqrt M1 / Real.sqrt M2 := by
    field_simp [hA.ne', (Real.sqrt_pos.2 hM1).ne', (Real.sqrt_pos.2 hM2).ne']
  rw [hcancel, div_pow, Real.sq_sqrt (le_of_lt hM1), Real.sq_sqrt (le_of_lt hM2)]

/-- 弱耦合代理阈值判据的单调性：Tc 升或 thetaD 降使 Tc/thetaD 增大。 -/
theorem weak_proxy_monotone (Tc1 Tc2 th1 th2 : ℝ)
    (hTc1 : 0 ≤ Tc1) (hth2 : 0 < th2)
    (hT : Tc1 ≤ Tc2) (hth : th2 ≤ th1) :
    Tc1 / th1 ≤ Tc2 / th2 := by
  have hratio : Tc1 / th1 ≤ Tc1 / th2 := by
    gcongr
  have hstep : Tc1 / th2 ≤ Tc2 / th2 := by
    gcongr
  exact le_trans hratio hstep

end
end CQM.DataVerification
