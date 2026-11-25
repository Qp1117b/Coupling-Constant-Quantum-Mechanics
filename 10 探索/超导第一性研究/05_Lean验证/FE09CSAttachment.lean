/-
  FE09（候选·未落地）：Chern–Simons 统计附着的奇偶律
  ============================================================
  外部标准（2+1D，Wilczek；CS 层级 kappa）：给复合体附着 m 个
  单位磁通量子 h/e，交换相位 theta=pi*m；(-1)^m 给交换符号。
    m 奇 ⇒ -1（费米）；m 偶 ⇒ +1（玻色）。

  本文件只承载奇偶律代数；不声称 CQM 已含费米子、不闭合任何缺口。
  链内 n=2 扇区的 Phi_2=h/e 只作为候选输入（临-6 归一未闭合）。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

namespace CQM.FE09CSAttachment

/-- (1) 偶数个磁通：$m=2k$ ⇒ $(-1)^m=+1$（玻色）。 -/
theorem even_flux_bose (k : ℕ) : (-1 : ℤ) ^ (2 * k) = 1 := by
  simp [pow_mul]

/-- (2) 奇数个磁通：$m=2k+1$ ⇒ $(-1)^m=-1$（费米）。 -/
theorem odd_flux_fermi (k : ℕ) : (-1 : ℤ) ^ (2 * k + 1) = -1 := by
  simp [pow_add, pow_mul]

/-- (3) 交换符号只由奇偶决定：相邻两次附着翻转符号。 -/
theorem flip_sign (m : ℕ) : (-1 : ℤ) ^ (m + 1) = -((-1 : ℤ) ^ m) := by
  rw [pow_succ]
  ring

/-- (4) 链内第一档 $n=2$ 给 $m=n/2=1$（一个单位磁通）⇒ 费米符号。 -/
theorem first_sector_is_fermionic : (-1 : ℤ) ^ (2 / 2) = -1 := by
  norm_num

end CQM.FE09CSAttachment
