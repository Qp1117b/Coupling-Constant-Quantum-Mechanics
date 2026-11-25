/-
  R33：临-5 高通道权重 1/k 的归一性——调和归一单调下降
  ============================================================
  链内 12.A1：模式集 2Z_{>=1} 无限；12.A3：权重比 2/n=1/k；
  L483/L492：第一档主导。`临-5`：权重归一未写出。
  外部（B 类）：H_K=sum 1/k ~ ln K + gamma 发散。

  本文件只承载代数部分：递归调和数、严格递增、归一权重 w1=1/H 严格递减、
  以及 K>2 时 w1(K)<2/3。发散本身由数值与 B 类外部标准承担。

  不证明：截断 K 的取值、临-5 闭合、任何外部标准的链内第一性。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

namespace CQM.WeightNormalization

noncomputable section

/-- 递归调和数 $H_K=\\sum_{k=1}^K1/k$。 -/
def H : ℕ → ℝ
  | 0 => 0
  | n + 1 => H n + 1 / (n + 1 : ℝ)

theorem H_one : H 1 = 1 := by norm_num [H]

theorem H_two : H 2 = 3 / 2 := by norm_num [H]

/-- $H_n>0$ 对 $n>0$。 -/
theorem H_pos {n : ℕ} (hn : 0 < n) : 0 < H n := by
  cases n with
  | zero => cases hn
  | succ n =>
      cases n with
      | zero => norm_num [H]
      | succ n =>
          rw [H]
          have hprev : 0 < H (Nat.succ n) := H_pos (Nat.succ_pos n)
          positivity

/-- $H$ 严格递增。 -/
theorem H_lt_succ (n : ℕ) : H n < H (n + 1) := by
  rw [H]
  have hpos : 0 < (1 : ℝ) / (n + 1 : ℝ) := by positivity
  linarith

/-- $H_a\\le H_{a+k}$。 -/
theorem H_le_add (a k : ℕ) : H a ≤ H (a + k) := by
  induction k with
  | zero => simp
  | succ k ih =>
      have hstep : H (a + k) < H (a + k + 1) := H_lt_succ (a + k)
      have hadd : a + Nat.succ k = a + k + 1 := by omega
      rw [hadd]
      linarith

/-- $k>0$ 时 $H_a<H_{a+k}$。 -/
theorem H_lt_add_of_pos (a k : ℕ) (hk : 0 < k) : H a < H (a + k) := by
  cases k with
  | zero => cases hk
  | succ k =>
      have hle : H a ≤ H (a + k) := H_le_add a k
      have hstep : H (a + k) < H (a + k + 1) := H_lt_succ (a + k)
      have hadd : a + Nat.succ k = a + k + 1 := by omega
      rw [hadd]
      linarith

/-- 归一权重 $w_1(K)=1/H_K$ 随 $K$ 严格下降。 -/
theorem w1_strict_decreasing (n : ℕ) (hn : 0 < n) :
    1 / H (n + 1) < 1 / H n := by
  exact one_div_lt_one_div_of_lt (H_pos hn) (H_lt_succ n)

/-- 基础档取值。 -/
theorem w1_one : 1 / H 1 = 1 := by rw [H_one]; norm_num

theorem w1_two : 1 / H 2 = 2 / 3 := by rw [H_two]; norm_num

/-- $K>2$ 时 $w_1(K)<2/3$：第一档权重被摊薄。 -/
theorem w1_lt_two_thirds {n : ℕ} (hn : 2 < n) : 1 / H n < 2 / 3 := by
  rcases Nat.exists_eq_add_of_le (Nat.succ_le_of_lt hn) with ⟨k, rfl⟩
  have hH : H 2 < H (3 + k) := by
    have hposk : 0 < 1 + k := by omega
    have hH' : H 2 < H (2 + (1 + k)) := H_lt_add_of_pos 2 (1 + k) hposk
    have heq : 2 + (1 + k) = 3 + k := by omega
    rw [heq] at hH'
    exact hH'
  have hpos : 0 < H 2 := by rw [H_two]; norm_num
  have hrecip : 1 / H (3 + k) < 1 / H 2 := one_div_lt_one_div_of_lt hpos hH
  rw [H_two] at hrecip
  norm_num at hrecip ⊢
  exact hrecip

end
end CQM.WeightNormalization
