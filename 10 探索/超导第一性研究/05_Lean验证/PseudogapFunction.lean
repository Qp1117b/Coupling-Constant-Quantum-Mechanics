/-
  R23：链外-E 的赝能隙函数形式——代数骨架
  ============================================================
  前件（链内已登记）：
    C5.1：振幅扇区隙方程的两个极限，T=0 给
          Δ(0) = (π/e^γ) k_B T^*，T^* 是配对端子。
    (目标.1)：T_c = min{T^*, T_φ}，ΔT_pg = T^* - T_c。

  本文件承载（非新物理，是 (R23.1)/(R23.2) 的代数）：
    (1) 赝能隙幅值 Δ_pg(0) = ratio·k_B·T^*（ratio = π/e^γ > 0）；
    (2) 比值式 2Δ_pg(0)/(k_B T_c) = (2 ratio)·(T^*/T_c)；
    (3) T^*/T_c = 1 + ΔT_pg/T_c（差值与比值同一信息）；
    (4) 3 ≤ T^*/T_c ≤ 5 ⇒ 比值落在 [3·R4, 5·R4]（"3–5 倍"）；
    (5) T^* > T_c ⇒ 比值严格大于 BCS 值（赝能隙放大）；
    (6) r = 1（T^*=T_c）⇒ 比值退回 BCS——退化自洽；
    (7) 形状 f 严格减 ⇒ r 越大，Δ_pg(T_c)/Δ_pg(0)=f(1/r) 越接近 1
        （赝能隙在 T_c "几乎不降"）。

  不证明：f 的具体解析式（C5.1 数值解）、绝对 T^* 数值（命题 Z2 外生）、
          连续谱权重与填平标度（E2，仍缺）。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

namespace CQM.PseudogapFunction

noncomputable section

/-- 赝能隙幅值：Δ_pg(0) = ratio · k_B · T^*（C5.1，ratio = π/e^γ）。 -/
def pgGap (ratio kB Tstar : ℝ) : ℝ := ratio * kB * Tstar

/-- (3) 差值与比值同一信息：T^*/T_c = 1 + (T^* - T_c)/T_c。 -/
theorem ratio_eq_one_plus_delta (Tstar Tc : ℝ) (hTc : Tc ≠ 0) :
    Tstar / Tc = 1 + (Tstar - Tc) / Tc := by
  field_simp
  ring

/-- (2)(R23.2)：2Δ_pg(0)/(k_B T_c) = R4 · (T^*/T_c)，R4 = 2 ratio。 -/
theorem ratio_form (ratio kB Tstar Tc : ℝ) (hkB : kB ≠ 0) (hTc : Tc ≠ 0) :
    2 * pgGap ratio kB Tstar / (kB * Tc) = (2 * ratio) * (Tstar / Tc) := by
  unfold pgGap
  field_simp

/-- (6) 退化自洽：T^* = T_c 时比值退回 BCS 值 2 ratio。 -/
theorem ratio_eq_bcs_at_one (ratio kB T : ℝ) (hkB : kB ≠ 0) (hT : T ≠ 0) :
    2 * pgGap ratio kB T / (kB * T) = 2 * ratio := by
  unfold pgGap
  field_simp

/-- (5) 赝能隙放大：T^* > T_c > 0 ⇒ 比值 > BCS 值。 -/
theorem ratio_gt_bcs (ratio kB Tstar Tc : ℝ)
    (hR : 0 < 2 * ratio) (hkB : 0 < kB) (hTc : 0 < Tc) (h : Tc < Tstar) :
    2 * ratio < 2 * pgGap ratio kB Tstar / (kB * Tc) := by
  unfold pgGap
  have hpos : 0 < kB * Tc := mul_pos hkB hTc
  rw [lt_div_iff₀ hpos]
  have h1 : Tc < Tstar := h
  nlinarith [mul_pos hR hpos]

/-- (4) "3–5 倍"：3 ≤ r ≤ 5 ⇒ R4·r ∈ [3 R4, 5 R4]。 -/
theorem three_to_five (R4 r : ℝ) (hR4 : 0 < R4) (h3 : 3 ≤ r) (h5 : r ≤ 5) :
    3 * R4 ≤ R4 * r ∧ R4 * r ≤ 5 * R4 := by
  constructor
  · nlinarith
  · nlinarith

/-- (1)(7) 赝能隙温度函数：Δ_pg(T) = Δ_pg(0) · f(T/T^*)。 -/
def pgT (D0 : ℝ) (f : ℝ → ℝ) (T Tstar : ℝ) : ℝ := D0 * f (T / Tstar)

/-- (1) 在 T = T^* 归零（f(1)=0 且 T^* ≠ 0）。 -/
theorem pgT_zero_at_tstar (D0 Tstar : ℝ) (f : ℝ → ℝ)
    (hf : f 1 = 0) (hT : Tstar ≠ 0) :
    pgT D0 f Tstar Tstar = 0 := by
  unfold pgT
  rw [div_self hT, hf, mul_zero]

/-- 在 T = T_c 处的值只依赖 r 与形状：Δ_pg(T_c) = Δ_pg(0)·f(T_c/T^*)。 -/
theorem pgT_at_tc (D0 Tc Tstar : ℝ) (f : ℝ → ℝ) :
    pgT D0 f Tc Tstar = D0 * f (Tc / Tstar) := rfl

/-- (7) 形状严格减 ⇒ r 越大，赝能隙在 T_c 越接近其 T=0 值。 -/
theorem pg_at_tc_closer (f : ℝ → ℝ) (r1 r2 : ℝ)
    (hr1 : 1 < r1) (hr2 : r1 < r2)
    (hmono : ∀ a b : ℝ, 0 ≤ a → a < b → b ≤ 1 → f b < f a) :
    f (1 / r1) < f (1 / r2) := by
  have hr1pos : 0 < r1 := by linarith
  have hr2pos : 0 < r2 := by linarith
  have ha : 0 ≤ 1 / r2 := by positivity
  have hlt : 1 / r2 < 1 / r1 := by
    rw [div_lt_div_iff_of_pos_left (by norm_num : (0:ℝ) < 1) hr2pos hr1pos]
    exact hr2
  have hle : 1 / r1 ≤ 1 := by
    rw [div_le_one hr1pos]
    exact le_of_lt hr1
  exact hmono (1 / r2) (1 / r1) ha hlt hle

end
end CQM.PseudogapFunction
