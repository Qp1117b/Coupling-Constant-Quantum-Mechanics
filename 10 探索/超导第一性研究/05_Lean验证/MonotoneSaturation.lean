/-
  R30：(6G.8) 满足集随 T 收缩 ⇒ 满足率 q(T) 非增
  ============================================================
  链内前件（环06_G19容差标定 (6G.8)）：
    F(eps,T) = J0*A(eps)*w(T)*cos(s*Lambda(eps)) - (2/pi)*kB*T
  其中 w 严格减（10B.1）、kB>0、A(eps)>=0、cos 项在固定 eps 下为常数。
  本文件只承载单调性与集合包含；数值 q 需 eps 分布（外生）。

  不证明：q 的数值、G21 的定量谱函数闭合、谱线形的第一性来源。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

namespace CQM.MonotoneSaturation

noncomputable section

/-- (1) 对固定 $\\varepsilon$，$F(\\varepsilon,T)$ 随 $T$ 严格减。 -/
theorem F_strict_mono {B k : ℝ} (hB : 0 ≤ B) (hk : 0 < k) {w : ℝ → ℝ}
    (hw : ∀ {T₁ T₂}, T₁ < T₂ → w T₂ < w T₁) {T₁ T₂ : ℝ} (hT : T₁ < T₂) :
    B * w T₂ - k * T₂ < B * w T₁ - k * T₁ := by
  have hwlt : w T₂ < w T₁ := hw hT
  have hmul : B * w T₂ ≤ B * w T₁ := mul_le_mul_of_nonneg_left (le_of_lt hwlt) hB
  nlinarith

/-- (2) 若在 $T_2$ 满足，则在更低的 $T_1$ 也满足（即 $S(T_2)\\subseteq S(T_1)$）。 -/
theorem lower_T_satisfies {B k : ℝ} (hB : 0 ≤ B) (hk : 0 < k) {w : ℝ → ℝ}
    (hw : ∀ {a b}, a < b → w b < w a) {T₁ T₂ : ℝ} (hT : T₁ < T₂)
    (hsat : 0 ≤ B * w T₂ - k * T₂) : 0 ≤ B * w T₁ - k * T₁ := by
  have hmono : B * w T₂ - k * T₂ < B * w T₁ - k * T₁ := F_strict_mono hB hk hw hT
  linarith

/-- (3) 有限集上的满足率非增：$n_2\\le n_1\\le N$ ⇒ $n_2/N\\le n_1/N$。 -/
theorem rate_nonincreasing (N n₁ n₂ : ℕ) (hN : 0 < N) (h21 : n₂ ≤ n₁) :
    (n₂ : ℝ) / N ≤ (n₁ : ℝ) / N := by
  have hden : (0 : ℝ) < N := by exact_mod_cast hN
  exact div_le_div_of_nonneg_right (by exact_mod_cast h21) (le_of_lt hden)

/-- (4) 两分量谱权归一：$q+(1-q)=1$。 -/
theorem weight_partition (q : ℝ) : q + (1 - q) = 1 := by ring

end
end CQM.MonotoneSaturation
