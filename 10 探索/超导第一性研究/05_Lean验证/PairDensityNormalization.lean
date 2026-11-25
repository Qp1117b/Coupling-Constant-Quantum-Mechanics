/-
  R34：临-26 的 2 配对基准密度归一——有限域代数
  ============================================================
  13.A6：rho2(i)=p(i)/sum_j p(j)；rhon=(2/n)*rho2。
  本文件在 3 点域上严格证明：
    (1) sum_i rho2(i) = 1（构造性归一恒等式）；
    (2) sum_i rhon(i) = 2/n（n>2 时总质量 <1，为次概率质量）；
    (3) 总质量 2/n 与 12.3 的 Phi_n/Phi_2=2/n 同数不同物（R32）。

  不证明：p(i) 的物理形式、为何以 2 配对为基准、2/n 的物理来源（临-26）。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

namespace CQM.PairDensityNormalization

noncomputable section

/-- 三点域的基准密度：$\\rho^{(2)}_i=p_i/S$，$S=p_1+p_2+p_3$。 -/
def rho2 (p1 p2 p3 i : ℝ) : ℝ :=
  (if i = 1 then p1 else if i = 2 then p2 else p3) / (p1 + p2 + p3)

/-- (1) 三点域上 $\\sum_i\\rho^{(2)}_i=1$。 -/
theorem rho2_sum_one (p1 p2 p3 : ℝ) (hS : p1 + p2 + p3 ≠ 0) :
    rho2 p1 p2 p3 1 + rho2 p1 p2 p3 2 + rho2 p1 p2 p3 3 = 1 := by
  unfold rho2
  simp
  field_simp

/-- (2) 高通道密度总和 $=2/n$。 -/
theorem rhon_sum (p1 p2 p3 n : ℝ) (hS : p1 + p2 + p3 ≠ 0) :
    (2 / n) * rho2 p1 p2 p3 1 + (2 / n) * rho2 p1 p2 p3 2 +
      (2 / n) * rho2 p1 p2 p3 3 = 2 / n := by
  have h := rho2_sum_one p1 p2 p3 hS
  rw [← mul_add, ← mul_add, h]
  ring

/-- (2') $n>2$ 时总质量 $<1$：不是概率密度，而是次概率质量。 -/
theorem rhon_subprobability (n : ℝ) (hn : 2 < n) : 2 / n < 1 := by
  have hnpos : 0 < n := by linarith
  rw [div_lt_one hnpos]
  linarith

/-- (3) 与 12.3 同数：总质量 $=2/n=\\Phi_n/\\Phi_2$（只给数值，不宣称物理同一）。 -/
theorem same_number_as_flux_ratio (n : ℝ) : 2 / n = (2 : ℝ) / n := rfl

end
end CQM.PairDensityNormalization
