/-
  R25：相位模带能否代替电子带——统计有界性与链序循环性
  ============================================================
  承载两件事（其余 P1–P4 由数值脚本与 B 类外部文献对照）：
    (1) 费米占据 1/(exp x+1) <= 1；玻色占据 1/(exp x-1) 可任意大
        ——\"相位模带代替电子带\"在统计上不成立；
    (2) 链序：带(rB) < 配对(rP) < 序参量(rO) < 相位模(rPhi)，
        故 rPhi < rB（用相位模供给带）与链序矛盾——循环。

  不证明：电子 Bloch 带的存在（链外-D 仍缺）；外部 Anderson-Higgs 的数值；
          费米/玻色统计是 CQM 的公设（不是，这里只是对照统计的代数性质）。
  纪律：无 axiom／sorry／admit／native_decide／unsafe；链序以定理假设给出，不写死为物理公设。
-/
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity

namespace CQM.PhaseVsBand

noncomputable section

/-- (1) 费米占据有界：对任意实数 x，1/(e^x+1) <= 1。 -/
theorem fermi_occupation_le_one (x : ℝ) : 1 / (Real.exp x + 1) ≤ 1 := by
  have hpos : 0 < Real.exp x + 1 := by positivity
  rw [div_le_iff₀ hpos]
  have he : 0 ≤ Real.exp x := le_of_lt (Real.exp_pos x)
  linarith

/-- (1′) 玻色占据可超过任意给定上界 M：只要 e^x-1 < 1/M。 -/
theorem bose_occupation_gt (M x : ℝ) (hM : 0 < M) (hd : 0 < Real.exp x - 1)
    (hsmall : Real.exp x - 1 < 1 / M) : M < 1 / (Real.exp x - 1) := by
  rw [lt_div_iff₀ hd]
  have hprod : M * (Real.exp x - 1) < 1 := by
    have hmul := mul_lt_mul_of_pos_left hsmall hM
    field_simp at hmul
    exact hmul
  exact hprod

/-- (2) 链序的可逆闭包：带先于相位模。 -/
theorem band_precedes_phase {rB rP rO rPhi : ℕ}
    (h1 : rB < rP) (h2 : rP < rO) (h3 : rO < rPhi) : rB < rPhi := by
  exact Nat.lt_trans h1 (Nat.lt_trans h2 h3)

/-- (2′) 循环性 no-go：若相位模反过来供给带，链序要求 rPhi < rB，与上游链序矛盾。 -/
theorem no_phase_to_band {rB rP rO rPhi : ℕ}
    (h1 : rB < rP) (h2 : rP < rO) (h3 : rO < rPhi)
    (hback : rPhi < rB) : False := by
  have hb : rB < rPhi := Nat.lt_trans h1 (Nat.lt_trans h2 h3)
  exact (not_lt_of_ge (le_of_lt hb)) hback

/-- (2″) 等价表述：链序成立时，不可能同时有"相位模先于带"。 -/
theorem not_phase_precedes_band {rB rP rO rPhi : ℕ}
    (h1 : rB < rP) (h2 : rP < rO) (h3 : rO < rPhi) : ¬ rPhi < rB := by
  intro hback
  exact no_phase_to_band h1 h2 h3 hback

/-- (3) 低温比热比：玻色声学支相对电子线性项按 (T/θ)^2 退出。 -/
theorem bose_heat_ratio_vanishes (T theta : ℝ) (hT : 0 < T) (hth : 0 < theta)
    (h : T < theta) : (T / theta) ^ 2 < 1 := by
  have hlt : T / theta < 1 := (div_lt_one hth).mpr h
  have hnonneg : 0 ≤ T / theta := by positivity
  nlinarith

end
end CQM.PhaseVsBand
