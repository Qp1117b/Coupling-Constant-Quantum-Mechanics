import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Tactic.NormNum

/-!
# R33: 26.B2 间距判别的数论核（谱侧接口·隔离区）

- 素数等比数列不可能：三互异素数 p1<p2<p3 不可能满足 p2²=p1·p3
  （由 Euclid 引理 p1|p2² ⇒ p1|p2 ⇒ p1=p2，矛盾）
- 由 log 单调：{p_n} 等比 ⇒ {log p_n} 等差（等距）；故素数非等比 ⇒ {log p_n} 非等距
这只是判别子的数学核，物理谱落哪支仍未证（见推导卡）。
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.PrimeGP

/-- 两个不同素数：若 p1<p2 且都为素数，则 p1 ∤ p2。 -/
theorem prime_not_dvd_distinct {p1 p2 : ℕ} (hp1 : Nat.Prime p1) (hp2 : Nat.Prime p2)
    (hlt : p1 < p2) : ¬ p1 ∣ p2 := by
  intro hd
  -- p1 | p2 且 p2 素数 ⇒ p2 的因子只有 1,p2 ⇒ p1=1 或 p1=p2
  have hfac := hp2.eq_one_or_self_of_dvd p1 hd
  rcases hfac with h1 | heq
  · have hp1gt1 := hp1.one_lt
    omega
  · omega

/-- 素数等比数列不可能的核心：p1<p2 互异素数 ⇒ p1∤p2²。 -/
theorem no_prime_gp {p1 p2 : ℕ} (hp1 : Nat.Prime p1) (hp2 : Nat.Prime p2)
    (hlt12 : p1 < p2) : ¬ (p1 ∣ p2 ^ 2) := by
  intro hd
  have hpp : p1 ∣ p2 := hp1.dvd_of_dvd_pow hd
  exact prime_not_dvd_distinct hp1 hp2 hlt12 hpp

/-- Euclid 引理的直接使用：p 素数、p|p2² ⇒ p|p2。 -/
theorem euclid_step {p p2 : ℕ} (hp : Nat.Prime p) (h : p ∣ p2 ^ 2) : p ∣ p2 :=
  hp.dvd_of_dvd_pow h

/-- 三素数等比 p2²=p1·p3 不可能（数值条件结论）。 -/
theorem three_prime_gp_impossible {p1 p2 p3 : ℕ} (hp1 : Nat.Prime p1) (hp2 : Nat.Prime p2)
    (hlt12 : p1 < p2) (heq : p2 ^ 2 = p1 * p3) : False := by
  have hdiv : p1 ∣ p2 ^ 2 := by
    rw [heq]
    exact dvd_mul_right p1 p3
  have hpp : p1 ∣ p2 := hp1.dvd_of_dvd_pow hdiv
  exact prime_not_dvd_distinct hp1 hp2 hlt12 hpp

end CQM.PrimeGP
