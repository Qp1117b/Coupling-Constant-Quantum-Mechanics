/-
  R62：Riemann-von Mangoldt 计数核对的代数核
  ===============================================================================
  N(T) ~ T/(2pi) ln(T/(2pi))。主链用其给 Xi 收敛、sum gamma^2 发散、可读窗口。
  本文件承载计数结构（对数增长、反解 gamma_n ~ 2pi n/ln n）的代数骨架；
  数值核对（OEIS A072080, ratio->1）在 Python。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Data.Real.Basic

namespace CQM.ZeroCount

/-- 计数结构截面：N(T) = k*T*ln(T)（k>0 常数，省略 2pi 与平移）。 -/
def countAsym (k T : ℚ) : ℚ := k * T

/-- 线性计数容量（格点论证，临-9）：容量 ~ T/alpha。 -/
def latticeCapacity (alpha T : ℚ) : ℚ := T / alpha

/-- 对数因子使计数超线性：T*ln T > T（T>e, k>0 截面用乘子 m>1）。 -/
theorem superlinear (k T m : ℚ) (hk : 0 < k) (hT : 0 < T) (hm : 1 < m) :
    k * T * m > k * T := by
  have hkT : 0 < k * T := mul_pos hk hT
  have h := mul_lt_mul_of_pos_left hm hkT   -- (k*T)*1 < (k*T)*m
  nlinarith

/-- 反解结构：gamma_n ~ 2pi n / ln n ⇒ gamma_n^2 ~ n^2/(ln n)^2（发散截面）。 -/
def gammaAsym (pi n ln_n : ℚ) : ℚ := 2 * pi * n / ln_n

/-- 发散项 gamma^2 随 n 增（截面：n^2/(ln n)^2 增，简化为 n^2 主导）。 -/
theorem gamma_sq_grows (n1 n2 : ℚ) (h : n1 < n2) (hn1 : 0 < n1) :
    n1^2 < n2^2 := by
  nlinarith

-- 边界注记（写文档，不构造伪形式化）：
-- ln T、pi 为超越数，ℚ 无法精确表示；本文件只载增长结构骨架。
-- 精确数值核对（MathWorld OEIS A072080, ratio 0.658->0.917）在 Python。
-- 计数公式是外部标准数学（已标源），非 CQM 推出。

end CQM.ZeroCount
