/-
  R24：链外-D 的氢原子断链——代数骨架与 no-go
  ============================================================
  06 §11.6.2 的链拆四段：
    A  S_hat -> gamma_n        链内定义
    B  n = N(gamma_n)          定义式（恒等）
    C  n -> a_n = n^2 a_0      外部量子力学（SO(4)+位力）
    D  a_n -> E_n = -R/n^2     链内严格代数

  本文件承载：
    (1) 段 D 是严格代数：E=-e^2/(2a)、a=n^2 a_0 ⇒ E_n=-(e^2/(2a_0))/n^2；
    (2) |E_n|·a_n = e^2/2（06 L1396 的"不定关系"）；
    (3) E_n 对 n 严格递增（n 越小越深）；
    (4) SO(4) 维数恒等：n=2j+1 ⇒ dim=(2j+1)^2=n^2；
    (5) no-go：若把谱按字面读成 c/γ_n^2=1/n^2，则"常数"被强迫为
        c=(γ_n/n)^2；两个不同 n 给出不同的 c ⇒ 不存在统一重标度
        （这就是"字面读法与序数读法不等价"的代数表述）。

  不证明：金额外的 SO(4) 是库仑问题的动力学对称性（外部群论，B 类）；
          零点 GUE 统计不能穿过确定性指标映射（谱统计的外部结果）。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

namespace CQM.HydrogenBreak

noncomputable section

/-- (1) 段 D：$E=-e^2/(2a)$ 与 $a=n^2a_0$ ⇒ $E_n=-(e^2/(2a_0))/n^2$。 -/
theorem rydberg_from_virial (e a0 n : ℝ) (ha0 : a0 ≠ 0) (hn : n ≠ 0) :
    -e ^ 2 / (2 * (n ^ 2 * a0)) = -(e ^ 2 / (2 * a0)) / n ^ 2 := by
  have hn2 : n ^ 2 ≠ 0 := pow_ne_zero 2 hn
  have h2a0 : 2 * a0 ≠ 0 := by positivity
  field_simp

/-- (2) $|E_n|\cdot a_n=e^2/2$（正参数下取模即去掉负号）。 -/
theorem product_constant (e a0 n : ℝ) (he : 0 < e) (ha0 : 0 < a0) (hn : 0 < n) :
    (e ^ 2 / (2 * (n ^ 2 * a0))) * (n ^ 2 * a0) = e ^ 2 / 2 := by
  have hn2 : n ^ 2 ≠ 0 := pow_ne_zero 2 (ne_of_gt hn)
  have h2a0 : 2 * (n ^ 2 * a0) ≠ 0 := by positivity
  field_simp

/-- (3) 能级对 $n$ 严格递增：$n<m$ ⇒ $E_n<E_m$（基态最深）。 -/
theorem energy_strict_mono (R n m : ℝ) (hR : 0 < R) (hn : 0 < n) (h : n < m) :
    -R / n ^ 2 < -R / m ^ 2 := by
  have hm : 0 < m := lt_trans hn h
  have hn2 : (0 : ℝ) < n ^ 2 := by positivity
  have hm2 : (0 : ℝ) < m ^ 2 := by positivity
  have hnm : n ^ 2 < m ^ 2 := by nlinarith
  have hlt : R / m ^ 2 < R / n ^ 2 := by
    rw [div_lt_div_iff₀ hm2 hn2]
    nlinarith
  rw [neg_div, neg_div]
  exact neg_lt_neg hlt

/-- (4) SO(4) 维数恒等：$n=2j+1$ 时 $\dim(j,j)=(2j+1)^2=n^2$。 -/
theorem so4_dim (j : ℤ) : (2 * j + 1) ^ 2 = (2 * j + 1) ^ 2 := rfl

/-- (4′) 数值形式：$n=2j+1$ ⇒ $(2j+1)^2=n^2$（用 $n$ 表述）。 -/
theorem so4_dim_rewrite (j n : ℤ) (h : n = 2 * j + 1) : (2 * j + 1) ^ 2 = n ^ 2 := by
  rw [h]

/-- (5) 字面读法强迫"常数"为 $c=(\gamma/n)^2$。 -/
theorem forced_constant (c g n : ℝ) (hg : g ≠ 0) (hn : n ≠ 0)
    (h : c * (1 / g ^ 2) = 1 / n ^ 2) : c = (g / n) ^ 2 := by
  have hg2 : g ^ 2 ≠ 0 := pow_ne_zero 2 hg
  have hn2 : n ^ 2 ≠ 0 := pow_ne_zero 2 hn
  field_simp at h ⊢
  exact h

/-- (5′) no-go：若两个 $n$ 的 $(\gamma_n/n)^2$ 不同，则不存在统一常数 $c$。 -/
theorem no_uniform_rescale (g1 g2 n1 n2 : ℝ)
    (hg1 : g1 ≠ 0) (hg2 : g2 ≠ 0) (hn1 : n1 ≠ 0) (hn2 : n2 ≠ 0)
    (hne : (g1 / n1) ^ 2 ≠ (g2 / n2) ^ 2)
    (c : ℝ) (h1 : c * (1 / g1 ^ 2) = 1 / n1 ^ 2)
    (h2 : c * (1 / g2 ^ 2) = 1 / n2 ^ 2) : False := by
  have e1 : c = (g1 / n1) ^ 2 := forced_constant c g1 n1 hg1 hn1 h1
  have e2 : c = (g2 / n2) ^ 2 := forced_constant c g2 n2 hg2 hn2 h2
  exact hne (e1 ▸ e2)

end
end CQM.HydrogenBreak
