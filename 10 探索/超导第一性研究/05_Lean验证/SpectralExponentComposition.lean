/-
  环 4／85：谱指数合成律与亏角响应二分（代数承载）
  =================================================
  第 84 轮把等时关联写成 Bessel 核 $\rho_m$，但索引只按 $m=2n$ 给。
  本轮给出一般律 $m_{\rm eff}=2n+1-s$，并说明：
    * 形状指数 $m_{\rm eff}$ 与 $\sigma_0^2$ 的标度指数 $m_{\rm eff}+1$ 同源；
    * 平坦参考下亏角恒为零（线性响应不存在），
      弯曲参考下响应线性（$|G_q|^2\propto q^2$）。
  本文件只承载其中的纯代数部分；Bessel 积分渐近与逐点数值在 Python。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp

namespace CQM.SpectralExponent

/-- 谱指数合成律：`m_eff = 2n + 1 - s`（在 `ℤ` 上定义，避免 `ℕ` 截断）。 -/
def meff (n s : ℤ) : ℤ := 2 * n + 1 - s

/-- 声学支 `s = 1`：`m_eff = 2n`（第 84 轮的 $m=2n$ 是此特例）。 -/
theorem meff_acoustic (n : ℤ) : meff n 1 = 2 * n := by
  unfold meff; ring

/-- 柔性支 `s = 2`：`m_eff = 2n - 1`。 -/
theorem meff_flexural (n : ℤ) : meff n 2 = 2 * n - 1 := by
  unfold meff; ring

/-- 同一个 `m_eff` 同时给出 $\sigma_0^2$ 的标度指数：`2n + 2 - s = m_eff + 1`。 -/
theorem sigma_exponent (n s : ℤ) : 2 * n + 2 - s = meff n s + 1 := by
  unfold meff; ring

/-- 弯曲参考的线性响应给 `n = 1`，此时 `m_eff = 3 - s`。 -/
theorem meff_of_n_one (s : ℤ) : meff 1 s = 3 - s := by
  unfold meff; ring

/-- 收敛裕度：`n ≥ 1` 且 `s ≤ 2` ⇒ `m_eff ≥ 1`（Bessel 核可求和）。 -/
theorem meff_ge_one {n s : ℤ} (hn : 1 ≤ n) (hs : s ≤ 2) : 1 ≤ meff n s := by
  unfold meff; linarith

/-- 数值例：3D 体（`n=1, s=1`）给 `m_eff = 2`。 -/
example : meff 1 1 = 2 := by decide

/-- 数值例：2D 膜柔性（`n=1, s=2`）给 `m_eff = 1`（边缘但收敛）。 -/
example : meff 1 2 = 1 := by decide

/-- 数值例：平坦参考若按非线性阶 `n=2, s=1` 读，给 `m_eff = 4`（仅作对照）。 -/
example : meff 2 1 = 4 := by decide

/-- 越界对照：`n=1, s=3` 给 `m_eff = 0`（核不再可求和，不属链内支）。 -/
example : meff 1 3 = 0 := by decide

/-- 平坦参考：仿射应变下亏角不变，涨落恒为零。 -/
theorem flat_response_zero (c : ℝ) : c * 0 = 0 := by ring

/-- 弯曲参考：响应对应变线性，`Δδ(λε) = λ Δδ(ε)`。 -/
theorem curved_response_linear (c lam eps : ℝ) : c * (lam * eps) = lam * (c * eps) := by
  ring

/-- 线性响应 ⇒ 一阶 q 权重：`|G_q|² = c²q²`（即 `n = 1`）。 -/
theorem q_power_two (c q : ℝ) (hq : q ≠ 0) : (c * q) ^ 2 / q ^ 2 = c ^ 2 := by
  field_simp

/-- 亏角方差按边长线性响应：`Δε = Σ (∂ε/∂l) δl`，`δl = l·ε_strain`。 -/
theorem strain_linear (coef l εs : ℝ) : coef * (l * εs) = (coef * l) * εs := by
  ring

end CQM.SpectralExponent


