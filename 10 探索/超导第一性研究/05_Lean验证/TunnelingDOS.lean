/-
  预注册判定 R17：准粒子态密度与 Giaever 隧穿的纯数骨架（A 类结构＋B 类工具）
  =================================================================
  链内 gap Δ0/kB Tc = pi/e^gamma（C5）。
  BCS DOS Ns/Nn = E/sqrt(E^2-Delta^2)，gap edge 平方根发散系数 sqrt(Delta/2)。
  态守恒 sum rule: ∫_0^X (Ns/Nn-1)dE = sqrt(X^2-Delta^2)-X -> 0。
  本文件承载代数骨架；数值积分由 R17 脚本完成。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

namespace CQM.TunnelingDOS

noncomputable section

def eGamma : ℝ := 1.7810724179901979
def Delta0 : ℝ := Real.pi / eGamma       -- Δ0/kB Tc = pi/e^gamma

lemma eGamma_pos : 0 < eGamma := by unfold eGamma; norm_num
lemma Delta0_pos : 0 < Delta0 := by
  unfold Delta0
  apply div_pos Real.pi_pos eGamma_pos

/-- gap ratio 2Δ0/kB Tc = 2pi/e^gamma（C5）。 -/
lemma gap_ratio : 2 * Delta0 = 2 * Real.pi / eGamma := by
  unfold Delta0
  ring

/-- edge 发散系数平方 = Delta0/2。 -/
def edgeCoeffSq : ℝ := Delta0 / 2
lemma edge_coeff_sq_pos : 0 < edgeCoeffSq := by
  unfold edgeCoeffSq
  exact div_pos Delta0_pos (by norm_num)

/-- sum rule 解析式 sqrt(X^2-Delta^2)-X < 0（对 X>Delta），
    且随 X 增大趋于 0（被隙驱逐态=相干峰吸收态）。 -/
lemma sum_rule_negative (X : ℝ) (hXpos : 0 < X) :
    Real.sqrt (X^2 - Delta0^2) - X < 0 := by
  have hslt : Real.sqrt (X^2 - Delta0^2) < X := by
    rw [Real.sqrt_lt' hXpos]
    nlinarith [Delta0_pos]
  linarith

end
end CQM.TunnelingDOS
