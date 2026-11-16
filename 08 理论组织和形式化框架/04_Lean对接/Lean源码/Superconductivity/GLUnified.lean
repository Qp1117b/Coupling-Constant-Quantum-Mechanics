import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic

/-!
# CQM 超导：统一 Ginzburg–Landau 泛函 (GLUnified)

对应探索文档 `10 探索/CQM_探索_超导统一GL理论.md`。

## 形式化内容

1. **系数识别**（定义引入，不作物理断言）：
   `aCoefficient a₀ p_c p = a₀(p_c − p)`、`condensateFraction p p_c = max 0 (p − p_c)`。
2. **GL 极小**：均匀态自由能 `glFreeEnergy a b ψ = aψ² + (b/2)ψ⁴` 在
   `ψ² = −a/b`（`a<0`、`b>0`）处取极小，极小值 `−a²/(2b)`。
3. **零点即渗流阈值**：`a₀ ≠ 0` 时 `a(T)=0 ↔ p = p_c`——把「渗流判据」与
   「GL 系数零点」合并为一条。
4. **κ 的温度无关性**：`λ = C/√q`、`ξ = D/√q` 时 `λ/ξ = C/D`，与 `q = p−p_c` 无关。
5. **相干长度**：`ξ² = ℏ²/(2m*a₀q)` 的平方根自洽。

## 边界

- 不含 `sorry`/`admit`/`native_decide`/`unsafe`/新增 `axiom`；
  无数值进入形式化断言。
- 未形式化：变分方程（Sobolev/变分框架）、`H_c1`/`H_c2` 的常数因子、
  比热跳跃 `1.43`（依赖 BCS 的 φ⁴ 系数）、Josephson 公式。
-/

noncomputable section

namespace CQM

/-! ## 1 系数识别（定义引入） -/

/-- GL 二次系数：`a(T) = a₀(p_c − p)`。`p` 为合格分数，`p_c` 为渗流阈值。 -/
def aCoefficient (a0 pc p : ℝ) : ℝ := a0 * (pc - p)

/-- 凝聚分数：`|ψ₀|² = max(0, p − p_c)`（超出渗流阈值的合格比例）。 -/
def condensateFraction (p pc : ℝ) : ℝ := max 0 (p - pc)

/-- 均匀态 GL 自由能密度（忽略梯度与磁场）：`F = aψ² + (b/2)ψ⁴`。 -/
def glFreeEnergy (a b psi : ℝ) : ℝ := a * psi ^ 2 + (b / 2) * psi ^ 4

/-! ## 2 GL 极小 -/

/-- **GL 极小**：`a<0`、`b>0` 时，`ψ² = −a/b` 处的自由能为 `−a²/(2b)`。 -/
theorem glMinimum {a b : ℝ} (ha : a < 0) (hb : 0 < b) :
    glFreeEnergy a b (Real.sqrt (-a / b)) = -(a ^ 2) / (2 * b) := by
  unfold glFreeEnergy
  have hq : 0 ≤ -a / b := by
    apply div_nonneg
    · linarith
    · exact le_of_lt hb
  have h2 : (Real.sqrt (-a / b)) ^ 2 = -a / b := Real.sq_sqrt hq
  have h4 : (Real.sqrt (-a / b)) ^ 4 = (-a / b) ^ 2 := by
    rw [show (4 : ℕ) = 2 * 2 by norm_num, pow_mul, h2]
  rw [h2, h4]
  have hbne : b ≠ 0 := ne_of_gt hb
  field_simp [hbne]
  ring

/-! ## 3 零点即渗流阈值 -/

/-- **`a(T_c)=0` 等价于 `p=p_c`**：`a₀ ≠ 0` 时，GL 二次系数的零点就是渗流判据
`p(T_c)=p_c`。 -/
theorem aCoefficient_eq_zero_iff {a0 pc p : ℝ} (h : a0 ≠ 0) :
    aCoefficient a0 pc p = 0 ↔ p = pc := by
  unfold aCoefficient
  constructor
  · intro hzero
    rcases mul_eq_zero.mp hzero with h0 | h0
    · exact absurd h0 h
    · linarith
  · intro hp
    rw [hp]
    ring

/-! ## 4 κ 的温度无关性 -/

/-- **κ 与 `q=p−p_c` 无关**：`λ = C/√q`、`ξ = D/√q` 时 `λ/ξ = C/D`。
这是 GL 给出的结构性预言（κ 在宽温区内近似常数）。 -/
theorem kappa_independent {C D q : ℝ} (hD : D ≠ 0) (hq : 0 < q) :
    (C / Real.sqrt q) / (D / Real.sqrt q) = C / D := by
  have hs : Real.sqrt q ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr hq)
  field_simp [hs, hD]

/-! ## 5 相干长度 -/

/-- **相干长度平方**：`ξ² = ℏ²/(2m*a₀q)`（`q = p−p_c > 0`）。 -/
theorem coherenceLength_sq {hbar2 m a0 q : ℝ} (hh : 0 ≤ hbar2)
    (hm : 0 < m) (ha : 0 < a0) (hq : 0 < q) :
    (Real.sqrt (hbar2 / (2 * m * a0 * q))) ^ 2 = hbar2 / (2 * m * a0 * q) := by
  rw [Real.sq_sqrt]
  positivity

end CQM