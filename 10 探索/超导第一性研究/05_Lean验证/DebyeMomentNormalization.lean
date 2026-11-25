import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp

/-!
# 环 4: 零点涨落关联的谱矩与周长律（代数核）

Workbench file. 不改主链、不改缺口状态、不动账面。

链内输入：
  Ring 2 (2.1):  Δeps 是简正模线性叠加，等时零点幅度 ħ/(2ρ_m ω_q)
  Ring 3 (3.1):  ε_e 是铰链亏角；线性化为 |G_q|² ∝ q^{2n}
  Ring 4 (4.1):  σ² = Σ_q |G_q|² ħ/(2ρ_m ω_q) = C ∫_0^Q q^m dq，m = 2n

本文件形式化（无 axiom/sorry/admit/native_decide/unsafe）：

  1. 谱矩 `moment m Q = Q^{m+1}/(m+1)`（∫_0^Q x^m dx 的代数值）；
  2. 标度律：`moment m (c·Q) = c^{m+1}·moment m Q` ⇒ σ0²∝Q^{2n+1}；
  3. 周长律恒等式：若 Σ_{i<j}ρ_ij = nS/2，则 Var = nσ²(1+S)；
  4. 负/正重整化：S<0 ⇒ Var<nσ²；S>0 ⇒ Var>nσ²（完整符号谱）。

未形式化（在 Python 与推导卡）：
  * 有限 BZ 的 Bessel 积分 ∫_0^Q q^m J0(qr)dq 与 k^{-3/2} 渐近；
  * ρ_k 的逐点数值与 S_ρ 的收敛值；
  * m=0 慢发散（∝ln）的严格估计。
-/

namespace CQM.DebyeMoment

/-- 谱矩：`∫_0^Q x^m dx = Q^{m+1}/(m+1)` 的代数值。 -/
noncomputable def moment (m : ℕ) (Q : ℝ) : ℝ := Q ^ (m + 1) / ((m : ℝ) + 1)

/-- `m=0` 退回线性标度。 -/
theorem moment_zero (Q : ℝ) : moment 0 Q = Q := by
  unfold moment
  norm_num

/-- 归一化：`moment m Q / Q^{m+1} = 1/(m+1)` 与 `Q` 无关。 -/
theorem moment_ratio (m : ℕ) (Q : ℝ) (hQ : Q ≠ 0) :
    moment m Q / Q ^ (m + 1) = 1 / ((m : ℝ) + 1) := by
  unfold moment
  have hden : ((m : ℝ) + 1) ≠ 0 := by positivity
  have hQp : Q ^ (m + 1) ≠ 0 := pow_ne_zero _ hQ
  field_simp

/-- 标度律（本轮的 `σ0²∝Q^{m+1}`）：`moment m (c·Q) = c^{m+1}·moment m Q`。
故 `|G_q|²∝q^{2n}`（m=2n）⇒ 谱矩按 `Q^{2n+1}` 标度。 -/
theorem moment_scaling (m : ℕ) (c Q : ℝ) :
    moment m (c * Q) = c ^ (m + 1) * moment m Q := by
  unfold moment
  rw [mul_pow]
  ring

/-- 周长律恒等式：`Σ_{i<j}ρ_ij = nS/2` 时 `Var(Φ_C) = nσ²(1+S)`。
这是 `Var = nσ² + 2Σ_{i<j}Cov` 的代数形式。 -/
theorem perimeter_identity (n : ℕ) (S s2 : ℝ) :
    (n : ℝ) * s2 + 2 * ((n : ℝ) * S / 2) * s2 = (n : ℝ) * s2 * (1 + S) := by
  ring

/-- 负重整化：`S<0`（关联求和非正）⇒ `Var < nσ²`。
本轮数值给 `S_ρ≈−0.02`（m=2）、`−0.08`（m=3）、`−0.10`（m=4），都在此形式内。 -/
theorem below_independent (n : ℕ) (hn : 1 ≤ n) {S s2 : ℝ}
    (hS : S < 0) (hs : 0 < s2) :
    (n : ℝ) * s2 * (1 + S) < (n : ℝ) * s2 := by
  have hn' : (0 : ℝ) < (n : ℝ) := by exact_mod_cast hn
  have hpos : (0 : ℝ) < (n : ℝ) * s2 := mul_pos hn' hs
  have hneg : (n : ℝ) * s2 * S < 0 := mul_neg_of_pos_of_neg hpos hS
  have hsplit : (n : ℝ) * s2 * (1 + S) = (n : ℝ) * s2 + (n : ℝ) * s2 * S := by ring
  linarith

/-- 正重整化：`S>0` ⇒ `Var > nσ²`（与 `below_independent` 配对，完整符号谱）。 -/
theorem above_independent (n : ℕ) (hn : 1 ≤ n) {S s2 : ℝ}
    (hS : 0 < S) (hs : 0 < s2) :
    (n : ℝ) * s2 < (n : ℝ) * s2 * (1 + S) := by
  have hn' : (0 : ℝ) < (n : ℝ) := by exact_mod_cast hn
  have hpos : (0 : ℝ) < (n : ℝ) * s2 := mul_pos hn' hs
  have hpos2 : (0 : ℝ) < (n : ℝ) * s2 * S := mul_pos hpos hS
  have hsplit : (n : ℝ) * s2 * (1 + S) = (n : ℝ) * s2 + (n : ℝ) * s2 * S := by ring
  linarith

end CQM.DebyeMoment
