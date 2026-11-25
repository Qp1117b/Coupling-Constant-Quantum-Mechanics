/-
  第 140 轮：环 15 的 p_pair 对分布形状的依赖——无假设界与形状税
  ==========================================================================
  (15.1) p_pair = Pr[σ_ℓ > σ_c]，σ_ℓ² 是局域方差估计。本文件承载：
    * **Cantelli 不等式**（分布无关的单边上界）：E[z]=0、E[z²]=v>0 时
        Pr[z ≥ k√v] ≤ 1/(1+k²)。
      它是"形状税"的严格上限：不假设任何分布，尾概率也不超过 1/(1+k²)。
    * **形状税的代数结构**：若两个分布同 (μ,σ²) 而偏度差 Δγ₁，
      p 的一阶修正 ∝ Δγ₁（Edgeworth 的线性部分），故"p 的容差 ⇒ γ₁ 的容差"
      是一个线性换算。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Order.Basic

open scoped BigOperators

namespace CQM.PairProbability

/-- **Cantelli 不等式**（有限分布版）：若 $p_i\ge0$、$\sum p_i=1$、
    $\sum p_iz_i=0$、$\sum p_iz_i^2=v>0$，则对 $k>0$
    $$\sum_{z_i\ge k\sqrt v}p_i\ \le\ \frac{1}{1+k^2}.$$ -/
theorem cantelli {ι : Type*} (s : Finset ι) (p z : ι → ℝ)
    (hp : ∀ i ∈ s, 0 ≤ p i)
    (h1 : ∑ i ∈ s, p i = 1)
    (hm : ∑ i ∈ s, p i * z i = 0)
    (h2 : ∑ i ∈ s, p i * z i ^ 2 = v)
    (hv : 0 < v) (k : ℝ) (hk : 0 < k) :
    ∑ i ∈ s.filter (fun i => k * Real.sqrt v ≤ z i), p i ≤ 1 / (1 + k ^ 2) := by
  classical
  set lam : ℝ := Real.sqrt v / k with hlam
  have hsv : 0 < Real.sqrt v := Real.sqrt_pos.mpr hv
  have hlam_pos : 0 < lam := div_pos hsv hk
  set A := s.filter (fun i => k * Real.sqrt v ≤ z i) with hA
  -- 事件上的下界
  have hbound : ∀ i ∈ A, (k * Real.sqrt v + lam) ^ 2 ≤ (z i + lam) ^ 2 := by
    intro i hi
    have hzi : k * Real.sqrt v ≤ z i := (Finset.mem_filter.mp hi).2
    have hbase : k * Real.sqrt v + lam ≤ z i + lam := by linarith
    have hbase_nn : 0 ≤ k * Real.sqrt v + lam := by
      have hkv : 0 ≤ k * Real.sqrt v := mul_nonneg (le_of_lt hk) (le_of_lt hsv)
      linarith
    have hnn : 0 ≤ z i + lam := by linarith
    nlinarith [hbase, hbase_nn, hnn]
  -- 右侧总量
  have htotal : ∑ i ∈ A, p i * (z i + lam) ^ 2 ≤ v + lam ^ 2 := by
    have hsplit : ∑ i ∈ A, p i * (z i + lam) ^ 2 ≤ ∑ i ∈ s, p i * (z i + lam) ^ 2 := by
      apply Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _)
      intro i _ _
      exact mul_nonneg (hp i ‹i ∈ s›) (sq_nonneg _)
    have hexp : ∑ i ∈ s, p i * (z i + lam) ^ 2 = v + lam ^ 2 := by
      have : ∀ i ∈ s, p i * (z i + lam) ^ 2 =
          p i * z i ^ 2 + 2 * lam * (p i * z i) + lam ^ 2 * p i := by
        intro i _
        ring
      rw [Finset.sum_congr rfl this]
      rw [Finset.sum_add_distrib, Finset.sum_add_distrib]
      rw [← Finset.mul_sum, ← Finset.mul_sum, hm, h2, h1]
      ring
    linarith
  -- 左边 = (下界) × Σ_A p
  have hleft : (k * Real.sqrt v + lam) ^ 2 * (∑ i ∈ A, p i) ≤ v + lam ^ 2 := by
    have hsum_le : (k * Real.sqrt v + lam) ^ 2 * (∑ i ∈ A, p i)
        ≤ ∑ i ∈ A, p i * (z i + lam) ^ 2 := by
      rw [Finset.mul_sum]
      apply Finset.sum_le_sum
      intro i hi
      have hp' : 0 ≤ p i := hp i (Finset.mem_filter.mp hi).1
      calc (k * Real.sqrt v + lam) ^ 2 * p i
          ≤ (z i + lam) ^ 2 * p i := mul_le_mul_of_nonneg_right (hbound i hi) hp'
        _ = p i * (z i + lam) ^ 2 := by ring
    linarith
  -- 代数收尾：(k√v+√v/k)² = v(1+k²)²/k²，v+λ² = v(1+k²)/k²
  have hcoef : (k * Real.sqrt v + lam) ^ 2 = v * (1 + k ^ 2) ^ 2 / k ^ 2 := by
    have hsq : (Real.sqrt v) ^ 2 = v := Real.sq_sqrt (le_of_lt hv)
    rw [hlam]
    field_simp
    nlinarith [hsq]
  have hrhs : v + lam ^ 2 = v * (1 + k ^ 2) / k ^ 2 := by
    have hsq : (Real.sqrt v) ^ 2 = v := Real.sq_sqrt (le_of_lt hv)
    rw [hlam]
    field_simp
    nlinarith [hsq]
  have hden : 0 < v * (1 + k ^ 2) ^ 2 / k ^ 2 := by
    have : 0 < (1 + k ^ 2) ^ 2 := by positivity
    positivity
  -- 把 hleft 写成 D * ΣA ≤ (1/(1+k²)) * D，再除 D
  have hE : v * (1 + k ^ 2) / k ^ 2 = (1 / (1 + k ^ 2)) * (v * (1 + k ^ 2) ^ 2 / k ^ 2) := by
    field_simp
  rw [hcoef, hrhs, hE] at hleft
  rw [mul_comm (v * (1 + k ^ 2) ^ 2 / k ^ 2) (∑ i ∈ A, p i)] at hleft
  exact le_of_mul_le_mul_right hleft hden

/-- 形状税的线性换算：若 $p$ 的一阶修正为 $c\,\gamma_1$，则 $|p-p_0|\le\epsilon$
    等价于 $|\gamma_1|\le\epsilon/|c|$（$c\ne0$）。 -/
theorem shape_tolerance (c gamma eps : ℝ) (hc : c ≠ 0) :
    |c * gamma| ≤ eps ↔ |gamma| ≤ eps / |c| := by
  rw [abs_mul]
  have hcpos : 0 < |c| := abs_pos.mpr hc
  constructor
  · intro h
    rw [le_div_iff₀ hcpos]
    linarith
  · intro h
    have := (le_div_iff₀ hcpos).mp h
    linarith

end CQM.PairProbability
