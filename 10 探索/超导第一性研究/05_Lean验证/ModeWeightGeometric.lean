import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Data.Real.Basic

/-!
# R35: 环 12 (12.2) 模式衰减权重的几何归一（临-21 接通·隔离区）

(12.2) 权重 e^{-(2k+1/2)t} = e^{-t/2} q^k，q=e^{-2t}∈(0,1)，几何级数。
归一权重 p_k=(1-q)q^{k-1}（几何分布）。
本文件核验代数核：
- 无限闭式 S1=q/(1-q), S2=q²/(1-q²)
- 参与比 n_eff=S1²/S2=(1+q)/(1-q)=coth t
- 第一档占比 p1=1-q
- 有限截断 S1(N)=q(1-q^N)/(1-q) 的 N=1 边界
有限截断的 n_eff→coth t 由数值脚本验证。
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.ModeWeightGeometric

noncomputable section

/-- 无限几何和 S1 = q/(1-q)。 -/
def S1inf (q : ℝ) : ℝ := q / (1 - q)

/-- 无限平方几何和 S2 = q²/(1-q²)。 -/
def S2inf (q : ℝ) : ℝ := q ^ 2 / (1 - q ^ 2)

/-- 参与比闭式：S1inf²/S2inf = (1+q)/(1-q)。 -/
theorem nEff_closed (q : ℝ) (hq1 : 1 - q ≠ 0) (hq0 : q ≠ 0) :
    (S1inf q) ^ 2 / S2inf q = (1 + q) / (1 - q) := by
  unfold S1inf S2inf
  field_simp [hq1, hq0]
  ring

/-- 第一档归一权重 p1 = 1-q（S1 中 k=1 项 / 总和）。 -/
theorem p1_limit (q : ℝ) (hq0 : q ≠ 0) : q / S1inf q = 1 - q := by
  unfold S1inf
  field_simp [hq0]

/-- 有限几何和 S1(N)=q(1-q^N)/(1-q)，N=1 边界 = q。 -/
def S1fin (q : ℝ) (N : ℕ) : ℝ := q * (1 - q ^ N) / (1 - q)

theorem S1fin_one (q : ℝ) (hq : 1 - q ≠ 0) : S1fin q 1 = q := by
  unfold S1fin
  field_simp [hq]

/-- 参与比随 q 单调增（(1+q)/(1-q) 对 0<q<1 增）——第一档主导在 q→0。 -/
theorem nEff_monotone_num (q1 q2 : ℝ) (hq12 : q1 < q2) (hq2 : q2 < 1) :
    (1 + q1) / (1 - q1) < (1 + q2) / (1 - q2) := by
  have hd1 : 0 < 1 - q1 := by linarith
  have hd2 : 0 < 1 - q2 := by linarith
  rw [div_lt_div_iff₀ hd1 hd2]
  ring_nf
  linarith

end
end CQM.ModeWeightGeometric
