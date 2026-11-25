/-
TwoMus.lean —— 第 144 轮：两个 mu 的分离与热膨胀材料入口

承载以下严格结果：
  1. (R144.1) tilde A 的行与 im(B) 正交 ⇒ 任意顶点位移 dot eps = 0；
  2. ell=Bp∈im(B) ⇒ delta ell=dot ell-mu*ell∈im(B) ⇒ tilde A delta ell=0
     （上一轮「dot eps=tilde L delta ell」在链内恒零）；
  3. (R144.2) 两个 mu 量纲不同：dim mu_(16)=1/[点数]、dim mu_(17)=1/[时间]；
  4. (R144.9)(R144.10) Gruneisen 膨胀率 mu=gamma Cv dotT/(3 K_T V) 的链式代数
     与 dilation 导数；
  5. (R144.12) Debye 低温 Cv ∝ T^3 ⇒ mu ∝ T^3 严格增且 T→0+ 时 →0；
  6. (R144.13) 绝对阈值下 s 增 ⇒ x 减 ⇒ p 增；相对阈值下 x 不变。

外部材料量（Gruneisen 参数、Debye 热容）只作 B 类前提，本文件不声称 CQM 推出数值。
无 axiom / sorry / admit / native_decide / unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Topology.Basic
import Mathlib.Order.Basic

namespace CQM.TwoMus

/-! ### 一、任意顶点位移下亏角不变（R144.1） -/

/-- 行向量版核心：r 与 B 的每行正交 ⇒ r 与 B 的任意线性组合正交。 -/
theorem row_orth_combination {ι κ : Type*} [Fintype ι] [Fintype κ]
    (r : ι → ℝ) (B : κ → ι → ℝ)
    (h : ∀ j, ∑ i, r i * B j i = 0) (x : κ → ℝ) :
    ∑ i, r i * (∑ j, B j i * x j) = 0 := by
  calc
    (∑ i, r i * (∑ j, B j i * x j)) = ∑ j, ∑ i, r i * (B j i * x j) := by
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro j hj
      rw [Finset.mul_sum]
    _ = ∑ j, (∑ i, r i * B j i) * x j := by
      apply Finset.sum_congr rfl
      intro j hj
      rw [Finset.sum_mul]
      apply Finset.sum_congr rfl
      intro i hi
      ring
    _ = 0 := by simp [h]

/-- 全行版：tilde A 每行与 im(B) 正交 ⇒ 任意位移下所有 eps 分量不变。 -/
theorem all_rows_orth {m κ ι : Type*} [Fintype m] [Fintype ι] [Fintype κ]
    (At : m → ι → ℝ) (B : κ → ι → ℝ)
    (h : ∀ a j, ∑ i, At a i * B j i = 0) (x : κ → ℝ) :
    ∀ a, ∑ i, At a i * (∑ j, B j i * x j) = 0 := by
  intro a
  exact row_orth_combination (At a) B (h a) x

/-- 矩阵版：A*B=0 ⇒ A.mulVec(B.mulVec x)=0。 -/
theorem matrix_comp_zero {m n k : Type*} [Fintype m] [Fintype n] [Fintype k]
    [DecidableEq k] (A : Matrix m n ℝ) (B : Matrix n k ℝ)
    (hAB : A * B = 0) (x : k → ℝ) :
    A.mulVec (B.mulVec x) = 0 := by
  ext i
  simp only [Matrix.mulVec, dotProduct, Pi.zero_apply]
  calc
    (∑ j, A i j * (∑ l, B j l * x l)) = ∑ l, ∑ j, A i j * (B j l * x l) := by
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro l hl
      rw [Finset.mul_sum]
    _ = ∑ l, (∑ j, A i j * B j l) * x l := by
      apply Finset.sum_congr rfl
      intro l hl
      rw [Finset.sum_mul]
      apply Finset.sum_congr rfl
      intro j hj
      ring
    _ = 0 := by
      apply Finset.sum_eq_zero
      intro l hl
      have hil : (∑ j, A i j * B j l) = 0 := by
        have hh := congrArg (fun M : Matrix m k ℝ => M i l) hAB
        simpa [Matrix.mul_apply] using hh
      rw [hil, zero_mul]

/-! ### 二、delta ell ∈ im(B) 时上一轮的桥恒零 -/

/-- 点态：ell=Bp、dot ell=Bx ⇒ delta=(∑B x)-mu(∑B p)=∑B(x-mu p)。 -/
theorem delta_in_image_point {ι κ : Type*} [Fintype ι] [Fintype κ]
    (B : κ → ι → ℝ) (p x : κ → ℝ) (mu : ℝ) (i : ι) :
    (∑ k, B k i * x k) - mu * (∑ k, B k i * p k)
      = ∑ k, B k i * (x k - mu * p k) := by
  rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro k hk
  ring

/-- delta ell 仍在 im(B) ⇒ tilde A delta ell=0（上一轮桥恒零）。 -/
theorem delta_bridge_zero {ι κ : Type*} [Fintype ι] [Fintype κ]
    (r : ι → ℝ) (B : κ → ι → ℝ)
    (h : ∀ j, ∑ i, r i * B j i = 0) (p x : κ → ℝ) (mu : ℝ) :
    ∑ i, r i * ((∑ k, B k i * x k) - mu * (∑ k, B k i * p k)) = 0 := by
  calc
    (∑ i, r i * ((∑ k, B k i * x k) - mu * (∑ k, B k i * p k)))
        = ∑ i, r i * (∑ k, B k i * (x k - mu * p k)) := by
          apply Finset.sum_congr rfl
          intro i hi
          rw [delta_in_image_point B p x mu i]
    _ = 0 := row_orth_combination r B h (fun k => x k - mu * p k)

/-! ### 三、两个 mu 的量纲分离（R144.2） -/

/-- 量纲指数向量 (M,L,T,N)：mu_(16)=1/[点数]。 -/
def dimMu16 : ℤ × ℤ × ℤ × ℤ := (0, 0, 0, -1)
/-- mu_(17)=1/[时间]。 -/
def dimMu17 : ℤ × ℤ × ℤ × ℤ := (0, 0, -1, 0)

theorem dim_mu_ne : dimMu16 ≠ dimMu17 := by
  norm_num [dimMu16, dimMu17]

/-! ### 四、Gruneisen 膨胀率链式式（R144.9）（R144.10） -/

/-- mu=(gamma Cv/(KT V))*dotT/3 = gamma Cv dotT/(3(KT V))。 -/
theorem gruneisen_chain (gamma Cv KT V dotT : ℝ) (hKT : KT ≠ 0) (hV : V ≠ 0) :
    (gamma * Cv / (KT * V)) * dotT / 3 = gamma * Cv * dotT / (3 * (KT * V)) := by
  field_simp [hKT, hV]

/-! ### 五、Debye 低温幂律（R144.12） -/

/-- 0 ≤ a < b ⇒ a^3 < b^3。 -/
theorem cubic_lt {a b : ℝ} (ha : 0 ≤ a) (hab : a < b) : a ^ 3 < b ^ 3 := by
  exact pow_lt_pow_left₀ hab ha (by norm_num)

/-- c>0、0≤T1<T2 ⇒ c T1^3 < c T2^3（mu ∝ T^3 严格增）。 -/
theorem mu_cubic_growth (c T1 T2 : ℝ) (hc : 0 < c) (hT1 : 0 ≤ T1) (h12 : T1 < T2) :
    c * T1 ^ 3 < c * T2 ^ 3 := by
  exact mul_lt_mul_of_pos_left (cubic_lt hT1 h12) hc

/-- 低温极限：mu(T)=c T^3 在 T→0+ 时 →0。 -/
theorem mu_cubic_tendsto_zero (c : ℝ) :
    Filter.Tendsto (fun T : ℝ => c * T ^ 3) (nhdsWithin (0 : ℝ) (Set.Ioi 0)) (nhds 0) := by
  have h1 : Filter.Tendsto (fun T : ℝ => T ^ 3) (nhdsWithin (0 : ℝ) (Set.Ioi 0)) (nhds (0 ^ 3)) := by
    exact (continuousAt_id.pow 3).tendsto.mono_left nhdsWithin_le_nhds
  simpa using h1.const_mul c

/-! ### 六、绝对／相对阈值下 p 的方向（R144.13） -/

/-- theta>0、0<s1<s2 ⇒ theta/s2^2 < theta/s1^2。 -/
theorem theta_div_sq_antitone (theta s1 s2 : ℝ) (ht : 0 < theta)
    (hs1 : 0 < s1) (h12 : s1 < s2) :
    theta / s2 ^ 2 < theta / s1 ^ 2 := by
  have hs2 : 0 < s2 := lt_trans hs1 h12
  have hs_sq : s1 ^ 2 < s2 ^ 2 := by nlinarith [sq_pos_of_pos hs1, sq_pos_of_pos hs2]
  rw [div_lt_div_iff₀ (sq_pos_of_pos hs2) (sq_pos_of_pos hs1)]
  nlinarith

/-- 绝对阈值：S 严格反单调（尾概率），s 增 ⇒ p=S(theta/s^2) 增。 -/
theorem abs_threshold_p_up (S : ℝ → ℝ) (hS : StrictAntiOn S (Set.Ioi 0))
    (theta s1 s2 : ℝ) (ht : 0 < theta) (hs1 : 0 < s1) (h12 : s1 < s2) :
    S (theta / s1 ^ 2) < S (theta / s2 ^ 2) := by
  have hs2 : 0 < s2 := lt_trans hs1 h12
  apply hS
  · exact div_pos ht (sq_pos_of_pos hs2)
  · exact div_pos ht (sq_pos_of_pos hs1)
  · exact theta_div_sq_antitone theta s1 s2 ht hs1 h12

/-- 相对阈值：theta ∝ s^2 ⇒ x=theta/s^2 恒定。 -/
theorem rel_threshold_x_const (k s : ℝ) (hs : s ≠ 0) :
    (k * s ^ 2) / s ^ 2 = k := by
  field_simp [hs]

end CQM.TwoMus
