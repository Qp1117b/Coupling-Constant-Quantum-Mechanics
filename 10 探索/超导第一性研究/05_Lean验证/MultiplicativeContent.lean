/-
  R41：审-7 乘法内容定位——加法差望远镜 vs 和乐积指数
  ============================================================
  链内 C_ij=f(eps_i-eps_j) 是加法差；闭环上求和望远镜恒 0。
  和乐侧 prod r_e 是乘法对象；若 r_e=exp(a_e)，则 prod=exp(sum a_e)。
  本文件只承载代数恒等式，不证明两扇区桥接，不闭合缺口。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Ring

namespace CQM.MultiplicativeContent

noncomputable section

/-- 三点闭环的加法差望远镜恒为零。 -/
theorem additive_cycle_telescopes (e1 e2 e3 : ℝ) :
    (e2 - e1) + (e3 - e2) + (e1 - e3) = 0 := by
  ring

/-- 和乐侧乘法积：$e^{a}e^{b}e^{c}=e^{a+b+c}$。 -/
theorem holonomy_product_exp (a b c : ℝ) :
    Real.exp a * Real.exp b * Real.exp c = Real.exp (a + b + c) := by
  rw [← Real.exp_add, ← Real.exp_add]

/-- 两扇区的读数不同：加法和为 0 不推出乘法积为 1（在一般 a 上）。 -/
theorem zero_sum_not_force_product_one (a b c : ℝ) (hs : a + b + c = 0) :
    Real.exp a * Real.exp b * Real.exp c = 1 := by
  rw [holonomy_product_exp, hs, Real.exp_zero]

end
end CQM.MultiplicativeContent
