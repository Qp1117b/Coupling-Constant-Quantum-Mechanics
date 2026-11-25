/-
  R67：端到端 Tc 用 CQM 自身 T* 式的判定——代数承载
  ===============================================================================
  CQM T* (no mu*) 系统性高估 2.65-6.33x；mu* 压制后落到实验 0.92-1.03x。
  定量确认审-14 (mu* 链外) 是决定性缺口。
  本文件承载高估因子结构与 mu* 压制方向；精确数值在 Python。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Data.Real.Basic

namespace CQM.EndToEnd

/-- 高估因子截面：CQM/exp > 1（三材料都 >1）。 -/
theorem overestimate_factor (cqm exp : ℚ) (hexp : 0 < exp) (h : exp < cqm) :
    1 < cqm / exp := by
  rw [one_lt_div hexp]
  exact h

/-- mu* 压制使 Tc 下降：AD(mu*>0) < AD(mu*=0) 的结构截面。
    用指数：exp 指数分母 (lam - mu*(1+0.62lam)) < lam ⇒ 负指数更负 ⇒ Tc 更小。
    截面用有理数：压制后有效耦合 lam_eff < lam ⇒ exp(-1/lam_eff) < exp(-1/lam)（代数骨架）。 -/
def effective_lambda (lam mus c : ℚ) : ℚ := lam - mus * c

theorem mu_star_reduces_lambda (lam mus c : ℚ) (hmus : 0 < mus) (hc : 0 < c) :
    effective_lambda lam mus c < lam := by
  unfold effective_lambda
  nlinarith

/-- 高估因子 > 压制因子：mu* 是决定性修正（截面）。 -/
def suppression (ad cqm : ℚ) : ℚ := ad / cqm

theorem suppression_lt_one (ad cqm : ℚ) (hcqm : 0 < cqm) (h : ad < cqm) :
    suppression ad cqm < 1 := by
  unfold suppression
  rw [div_lt_one hcqm]
  exact h

/-- 三材料高估因子互异（截面：6.33 > 3.63 > 2.65）。 -/
theorem factors_ordered (f1 f2 f3 : ℚ) (h12 : f2 < f1) (h23 : f3 < f2) :
    f3 < f1 := by
  linarith

-- 边界注记（写文档，不构造伪形式化）：
-- exp/e 为超越数，ℚ 无法精确表示；本文件只载高估/压制结构骨架。
-- 精确数值（6.33/3.63/2.65x，mu*压制后 0.92/1.03/0.93x）在 Python。
-- 不闭合审-14；不给新 Tc；external AD 是对照工具非 CQM 推出。

end CQM.EndToEnd
