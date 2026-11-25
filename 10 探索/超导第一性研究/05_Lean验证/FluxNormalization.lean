/-
  R32：临-6 通量归一——两读法的对象辨析
  ============================================================
  链内 L469：绕数 n ⇒ 总通量 n*h/2e ⇒ Φ_n/Φ_2 = n/2（随 n 升）
  链内 L451/L481：荷量子归一 h/(ne) ⇒ Φ_n/Φ_2 = 2/n（随 n 降）
  外部标准：Φ_0(q)=h/q；绕数 n 给总通量 n*Φ_0。

  本文件承载：
    (1) 两比值互为倒数：(n/2)*(2/n)=1；
    (2) 若把两式当同一对象、同一归一化，则 n>2 时矛盾；
    (3) 换算因子 n^2/4 依赖未写的映射 n_zeta -> q(n)（临-6 保持开放）。

  不证明：q(n) 映射、任何缺口闭合、外部标准的链内第一性。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

namespace CQM.FluxNormalization

noncomputable section

/-- (1) 两读法比值互为倒数。 -/
theorem reciprocal_ratios (n : ℝ) (hn : n ≠ 0) : (n / 2) * (2 / n) = 1 := by
  field_simp

/-- (2) 同一对象读法：若 n>2 且两比值相等，则矛盾（n^2=4 只给 n=2）。 -/
theorem no_same_object (n : ℝ) (hn : 2 < n) : n / 2 ≠ 2 / n := by
  intro h
  have hn0 : n ≠ 0 := by linarith
  field_simp at h
  nlinarith

/-- (2') 正解只有 n=2：n/2=2/n ⇒ n^2=4 ⇒ n=2（取正根）。 -/
theorem same_object_only_base (n : ℝ) (hn : 0 < n) (h : n / 2 = 2 / n) : n = 2 := by
  field_simp at h
  nlinarith

/-- (3) 换算因子：两候选电荷映射给比值相差 n^2/4。 -/
theorem conversion_factor (n : ℝ) (hn : n ≠ 0) :
    (n / 2) / (2 / n) = n ^ 2 / 4 := by
  field_simp
  ring

/-- (3') 基础档 n=2 的换算因子为 1；n>2 时换算因子 >1。 -/
theorem conversion_grows (n : ℝ) (hn : 2 < n) : 1 < n ^ 2 / 4 := by
  nlinarith

end
end CQM.FluxNormalization
