/-
  R69：链外-A 库仑赝势 mu* 的结构位置——代数承载（主链 §1439 限制(4)）
  ===============================================================================
  主链: 链里 V<0 恒成立 => lambda>0 恒成立 => 无"负净耦合"态 =>
        表达不了"为什么不超导" => mu* 属链外-A（不是审-14）。
  本文件载该结构的代数骨架：链内耦合只能为正（吸引），排斥态不存在。
  这不是对新物理的推导，是对主链限制(4)的形式化复述。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Data.Real.Basic

namespace CQM.ChainExternalA

/-- 链内有效耦合 lambda = -V（V<0 为吸引，故 lambda>0）。 -/
def coupling (V : ℚ) : ℚ := -V

/-- 链内前提：相互作用强度 V < 0（纯吸引，限制(4)）。 -/
theorem coupling_pos_of_attractive (V : ℚ) (hV : V < 0) : 0 < coupling V := by
  unfold coupling
  linarith

/-- 无"负净耦合"态：链内不存在使 lambda<=0 的 V<0。 -/
theorem no_nonpositive_coupling (V : ℚ) (hV : V < 0) : ¬ coupling V ≤ 0 := by
  unfold coupling
  linarith

/-- 排斥态不存在：若要求 V>0（Coulomb 排斥），与链内前提 V<0 矛盾。 -/
theorem no_repulsive_state (V : ℚ) (hV : V < 0) : ¬ 0 < V := by
  linarith

/-- 故 mu* 所需的"负净耦合/排斥"表达不了 ⇒ 链外-A。截面：
    吸引(-V>0) 与 排斥(V>0) 不能同时成立于同一 V。 -/
theorem attractive_excludes_repulsive (V : ℚ) :
    ¬ (V < 0 ∧ 0 < V) := by
  rintro ⟨h1, h2⟩
  linarith

-- 边界注记（写文档，不构造伪形式化）：
-- 本文件只复述主链限制(4)的代数骨架：链内 V<0 ⇒ 无排斥自由度。
-- 不引入 Thomas-Fermi / N(0)V_C 等 CQM 未涉及的新物理（红线不虚构）。
-- 不闭合任何缺口、不给新 Tc、不改状态。

end CQM.ChainExternalA
