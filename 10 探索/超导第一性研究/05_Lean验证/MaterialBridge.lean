/-
MaterialBridge.lean —— 第 143 轮：环 17 两个材料入口的可通桥判定

承载以下严格结果：
  1. 单形面角的余弦比值对边长伸缩不变（余弦定理的零次齐次性）；
  2. 样本方差在仿射驱动 dot ell = mu*ell 下的生产恒等式 A = 2*mu*s^2；
  3. 若线性形式 L 满足 L(ell)=0，则 L(mu*ell)=0（均匀伸缩在 ker L 内）；
  4. 尾概率 p(s)=S(theta/s^2) 的弹性链式：s*p'(s)/p = 2*x*S'(x)/p，x=theta/s^2；
  5. eta 的因子分解 eta = ((2N-1)/(2(N-1))) * eps * aLam，及可解界；
  6. 示意弹性 s/(S0*(exp(s/S0)-1)) < 1。

外部统计工具（卡方危险率、逆 Mills 比、仿射/非仿射分解）只作 B 类前提，
本文件不声称 CQM 推出它们。
无 axiom / sorry / admit / native_decide / unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Comp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Order.Basic

namespace CQM.MaterialBridge

/-! ### 一、余弦比值的尺度不变性 -/

/-- (R143.4)：余弦定理中的比值对共同伸缩不变。 -/
theorem cos_ratio_scale (a b c lam : ℝ) (ha : a ≠ 0) (hb : b ≠ 0) (hl : lam ≠ 0) :
    ((lam * a) ^ 2 + (lam * b) ^ 2 - (lam * c) ^ 2) / (2 * (lam * a) * (lam * b))
      = (a ^ 2 + b ^ 2 - c ^ 2) / (2 * a * b) := by
  field_simp [ha, hb, hl]

/-- 比值相等时 arccos 的输入相等（不调用 arccos 的求导，只用函数性）。 -/
theorem angle_scale_input (a b c lam : ℝ) (ha : a ≠ 0) (hb : b ≠ 0) (hl : lam ≠ 0) :
    (a ^ 2 + b ^ 2 - c ^ 2) / (2 * a * b)
      = ((lam * a) ^ 2 + (lam * b) ^ 2 - (lam * c) ^ 2) / (2 * (lam * a) * (lam * b)) := by
  exact (cos_ratio_scale a b c lam ha hb hl).symm

/-! ### 二、仿射驱动的方差生产 -/

/-- 逐点：中心化偏差与仿射速度的内积。 -/
theorem affine_pointwise (x xb mu : ℝ) :
    (x - xb) * (mu * x - mu * xb) = mu * (x - xb) ^ 2 := by
  ring

/-- 有限样本版：若均值随仿射率一起走，则方差生产累加为 mu 乘原方差。 -/
theorem affine_variance_rate {ι : Type*} [Fintype ι] (x : ι → ℝ) (mu xb : ℝ) :
    (∑ i, (x i - xb) * (mu * x i - mu * xb))
      = mu * (∑ i, (x i - xb) ^ 2) := by
  calc
    (∑ i, (x i - xb) * (mu * x i - mu * xb))
        = ∑ i, mu * (x i - xb) ^ 2 := by
            apply Finset.sum_congr rfl
            intro i hi
            exact affine_pointwise (x i) xb mu
    _ = mu * (∑ i, (x i - xb) ^ 2) := by
            rw [Finset.mul_sum]

/-- 仿射率的样本均值仍是 mu*xb。 -/
theorem affine_mean {ι : Type*} [Fintype ι] (x : ι → ℝ) (mu xb : ℝ) :
    (∑ i, (mu * x i - mu * xb)) = mu * (∑ i, (x i - xb)) := by
  symm
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i hi
  ring

/-! ### 三、齐次方向在 ker L 内 -/

/-- (R143.5) 的线性形式版：L(ell)=0 ⇒ L(mu*ell)=0。 -/
theorem homogeneous_kernel {ι : Type*} [Fintype ι] (c l : ι → ℝ) (mu : ℝ) :
    (∑ i, c i * (mu * l i)) = mu * (∑ i, c i * l i) := by
  symm
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i hi
  ring

/-- 同一件事的矩阵版：行向量点乘为零，则伸缩后仍为零。 -/
theorem matrix_homogeneous_kernel {n : Type*} [Fintype n]
    (L : Matrix n n ℝ) (ell : n → ℝ) (mu : ℝ)
    (h : L.mulVec ell = 0) :
    L.mulVec (fun i => mu * ell i) = 0 := by
  ext i
  simp only [Matrix.mulVec, dotProduct, Pi.zero_apply]
  have hi := congrFun h i
  simp only [Matrix.mulVec, dotProduct, Pi.zero_apply] at hi
  rw [show (∑ j, L i j * (mu * ell j)) = mu * (∑ j, L i j * ell j) by
    symm
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j hj
    ring]
  rw [hi, mul_zero]

/-! ### 四、尾概率弹性：链式法则 -/

lemma hasDerivAt_inv_sq (theta s : ℝ) (hs : s ≠ 0) :
    HasDerivAt (fun t : ℝ => theta / t ^ 2) (-2 * theta / s ^ 3) s := by
  have hpow : HasDerivAt (fun t : ℝ => t ^ 2) (2 * s) s := by
    simpa using (hasDerivAt_pow 2 s)
  have hdiv := (hasDerivAt_const (x := s) theta).div hpow (pow_ne_zero 2 hs)
  convert hdiv using 1
  field_simp [hs]
  ring_nf

/-- (R143.9)：p(s)=1-S(theta/s^2) ⇒ s*p'(s)/p = 2*x*S'(x)/p。 -/
theorem elasticity_chain (S : ℝ → ℝ) (S' theta s p : ℝ) (hs : s ≠ 0)
    (hS : HasDerivAt S S' (theta / s ^ 2))
    (hp_eq : p = 1 - S (theta / s ^ 2)) :
    HasDerivAt (fun t : ℝ => 1 - S (theta / t ^ 2)) (2 * theta * S' / s ^ 3) s
      ∧ s * (2 * theta * S' / s ^ 3) / p = 2 * (theta / s ^ 2) * S' / p := by
  have hx := hasDerivAt_inv_sq theta s hs
  have hcomp := hS.comp s hx
  have hder : HasDerivAt (fun t : ℝ => 1 - S (theta / t ^ 2))
      (2 * theta * S' / s ^ 3) s := by
    convert hcomp.const_sub 1 using 1
    field_simp [hs]
  constructor
  · exact hder
  · rw [hp_eq]
    field_simp [hs]

/-- 危险率形式：2*x*f = epsilon*p（当 p=S 且 S'=-f 时）。 -/
theorem elasticity_from_hazard (x p f eps : ℝ) (hp : p ≠ 0)
    (heps : eps = 2 * x * f / p) :
    eps * p = 2 * x * f := by
  rw [heps]
  field_simp [hp]

/-! ### 五、eta 的因子分解与可解界 -/

/-- (R143.11)–(R143.12)：N_eff 与 p 分别消去，eta 只剩 eps*aLam×有限 N 因子。 -/
theorem eta_factor (N eps aLam s p Neff ps : ℝ)
    (hN1 : N - 1 ≠ 0) (hs : s ≠ 0) (hp : p ≠ 0) (hNeff : Neff ≠ 0)
    (hN : N = p * Neff) (hps : ps = eps * p / s) :
    ((2 * N - 1) / (N * (N - 1)) * Neff * ps) * (s ^ 2 * aLam) / (2 * s)
      = ((2 * N - 1) / (2 * (N - 1))) * eps * aLam := by
  subst N
  rw [hps]
  field_simp [hN1, hs, hp, hNeff]

/-- 有限 N 因子大于 1。 -/
theorem finite_N_factor_gt_one (N : ℝ) (hN : 1 < N) :
    1 < (2 * N - 1) / (2 * (N - 1)) := by
  have hp : 0 < 2 * (N - 1) := by linarith
  rw [lt_div_iff₀ hp]
  linarith

/-- eta<1 等价于 eps*aLam 低于临界值 2(N-1)/(2N-1)。 -/
theorem eta_lt_one_bound (N z : ℝ) (hN : 1 < N) :
    ((2 * N - 1) / (2 * (N - 1))) * z < 1 ↔ z < 2 * (N - 1) / (2 * N - 1) := by
  have hden : 0 < 2 * (N - 1) := by linarith
  have hnum : 0 < 2 * N - 1 := by linarith
  constructor
  · intro h
    rw [div_mul_eq_mul_div] at h
    rw [div_lt_iff₀ hden] at h
    rw [lt_div_iff₀ hnum]
    nlinarith
  · intro h
    rw [lt_div_iff₀ hnum] at h
    rw [div_mul_eq_mul_div]
    rw [div_lt_iff₀ hden]
    nlinarith

/-- eta=1 恰好是临界边界（没有解的分界点）。 -/
theorem eta_eq_one_critical (N z : ℝ) (hN : 1 < N) :
    ((2 * N - 1) / (2 * (N - 1))) * z = 1 ↔ z = 2 * (N - 1) / (2 * N - 1) := by
  have hden : 0 < 2 * (N - 1) := by linarith
  have hnum : 0 < 2 * N - 1 := by linarith
  constructor
  · intro h
    rw [div_mul_eq_mul_div] at h
    rw [div_eq_iff (ne_of_gt hden)] at h
    rw [eq_div_iff (ne_of_gt hnum)]
    nlinarith
  · intro h
    rw [eq_div_iff (ne_of_gt hnum)] at h
    rw [div_mul_eq_mul_div]
    rw [div_eq_iff (ne_of_gt hden)]
    nlinarith

/-! ### 六、示意弹性严格小于 1 -/

/-- x>0 ⇒ x < exp x - 1（用 exp 的严格凸性下游引理）。 -/
theorem lt_exp_sub_one (x : ℝ) (hx : 0 < x) : x < Real.exp x - 1 := by
  have h := Real.add_one_lt_exp (ne_of_gt hx)
  linarith

/-- 指数型读数的弹性 eps_ad = s/(S0*(exp(s/S0)-1)) < 1。 -/
theorem ad_hoc_elasticity_lt_one (s S0 : ℝ) (hs : 0 < s) (hS0 : 0 < S0) :
    s / (S0 * (Real.exp (s / S0) - 1)) < 1 := by
  have hx : 0 < s / S0 := div_pos hs hS0
  have hlt : s / S0 < Real.exp (s / S0) - 1 := lt_exp_sub_one (s / S0) hx
  have hpos : 0 < Real.exp (s / S0) - 1 := by linarith
  have hmul : s < S0 * (Real.exp (s / S0) - 1) := by
    have hm := mul_lt_mul_of_pos_left hlt hS0
    have hcancel : S0 * (s / S0) = s := by field_simp [ne_of_gt hS0]
    nlinarith
  exact (div_lt_one (mul_pos hS0 hpos)).2 hmul

/-! ### 七、仿射生产为正的非平凡实例 -/

/-- 两点样本、x=(0,1)、mu>0：方差生产严格为正。 -/
theorem two_point_affine_positive (mu : ℝ) (hmu : 0 < mu) :
    let xb : ℝ := (0 + 1) / 2
    let rate : ℝ := 2 * (((0 - xb) * (mu * 0 - mu * xb) + (1 - xb) * (mu * 1 - mu * xb)) / 2)
    let s2 : ℝ := ((0 - xb) ^ 2 + (1 - xb) ^ 2) / 2
    rate = 2 * mu * s2 ∧ 0 < rate := by
  dsimp
  constructor
  · ring
  · nlinarith

end CQM.MaterialBridge
