/-
  预注册判定 R21：交流约瑟夫森计量闭环（A 类闭环＋B 类工具）
  ===========================================================
  链内 Phi0 = h/q = h/(2e)（R14/临19，q=2e 来自 12.A 模式集）。
  KJ = 2e/h = 1/Phi0（严格倒数闭环）；KJ*Phi0 = 1。
  q=e 分支给 Phi0'=2Phi0（链排除）。
  本文件承载代数骨架；SI 精确常数数值由 R21 脚本核对。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity

namespace CQM.ACJosephson

noncomputable section

/-- 用 ℚ 截面承载：取 h=1, e=1 ⇒ q=2, Phi0=1/2, KJ=2。 -/
def Phi0 (h e : ℚ) : ℚ := h / (2 * e)
def KJ (h e : ℚ) : ℚ := 2 * e / h

/-- 倒数闭环 KJ * Phi0 = 1（h,e ≠ 0）。 -/
lemma reciprocal_closure (h e : ℚ) (hh : h ≠ 0) (he : e ≠ 0) :
    KJ h e * Phi0 h e = 1 := by
  unfold KJ Phi0
  field_simp [hh, he]

/-- q=e 分支磁通量子是链选 q=2e 的两倍。 -/
lemma flux_double (h e : ℚ) (he : e ≠ 0) : h / e = 2 * Phi0 h e := by
  unfold Phi0
  field_simp [he]

end
end CQM.ACJosephson
