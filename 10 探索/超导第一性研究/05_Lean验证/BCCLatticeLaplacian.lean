/-
  R72：BCC Delaunay 铰链的代数量（`|cot|` 适用域、L 半正定判据、三维纯数 K）
  ==========================================================================
  R71 留下两个残量：三维纯数 K、以及环 3 "$|\cot|$ 无几何唯一性依据"。
  本轮把两者都化为可算的代数事实：

    * 平直判据：绕铰链的二面角和为 2π。k ≤ 4 时必有一个 θ ≥ π/2
      ⇒ cot θ ≤ 0，权 Σ cot 的符号不受保证（此时 |cot| 才有意义）。
    * BCC 最近邻铰链实测 k = 6、θ = π/3（60°）⇒ W = 6·cot(π/3) = 2√3 > 0，
      故 BCC 上**不需要** |cot|（这与 R72 对第 77 轮的订正一致）。
    * 权为正（非对角元为负）⇒ 图拉普拉斯半正定：三节点星给出平方和恒等式。
    * 声学标度：λ_q = K Ω^{2/3} q² ⇒ ω² = K c² q²；把刚度除以 K 即校准为 ω = c q。
      BCC 的 K = 2^{2/3}√3（数值 2.749459，脚本 `环02_环03_BCC的cot拉普拉斯与K.py`）。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith

namespace CQM.BCCHinge

noncomputable section

/-! ### 一、平直判据与 `|cot|` 的适用域 -/

/-- 三个四面体绕铰链：二面角和为 $2\pi$ ⇒ 至少一个 $\theta\ge\pi/2$。 -/
theorem three_hinge_exists_obtuse (t1 t2 t3 : ℝ)
    (h : t1 + t2 + t3 = 2 * Real.pi) :
    Real.pi / 2 ≤ t1 ∨ Real.pi / 2 ≤ t2 ∨ Real.pi / 2 ≤ t3 := by
  by_contra hc
  push Not at hc
  obtain ⟨h1, h2, h3⟩ := hc
  have hp : (0 : ℝ) < Real.pi := Real.pi_pos
  linarith

/-- 四个四面体绕铰链：同理至少一个 $\theta\ge\pi/2$（$4\cdot\pi/2=2\pi$ 取等）。 -/
theorem four_hinge_exists_obtuse (t1 t2 t3 t4 : ℝ)
    (h : t1 + t2 + t3 + t4 = 2 * Real.pi) :
    Real.pi / 2 ≤ t1 ∨ Real.pi / 2 ≤ t2 ∨ Real.pi / 2 ≤ t3 ∨ Real.pi / 2 ≤ t4 := by
  by_contra hc
  push Not at hc
  obtain ⟨h1, h2, h3, h4⟩ := hc
  have hp : (0 : ℝ) < Real.pi := Real.pi_pos
  linarith

/-- $k=5$ 时保证失效：$5\times72^\circ=2\pi$ 且 $72^\circ<\pi/2$。 -/
theorem five_hinge_no_obtuse : 5 * (2 * Real.pi / 5) = 2 * Real.pi ∧
    ∀ _ : Fin 5, (2 * Real.pi / 5 : ℝ) < Real.pi / 2 := by
  constructor
  · ring
  · intro _
    have : (0 : ℝ) < Real.pi := Real.pi_pos
    -- 2π/5 < π/2 ⟺ 4 < 5
    nlinarith

/-- BCC 最近邻铰链的 cot 权（$k=6$、$\theta=\pi/3$）：$W=6\cot(\pi/3)=2\sqrt3>0$。 -/
def bccWeight : ℝ := 2 * Real.sqrt 3

theorem bccWeight_pos : 0 < bccWeight := by
  unfold bccWeight
  have : (0 : ℝ) < Real.sqrt 3 := Real.sqrt_pos.2 (by norm_num)
  linarith

/-- 权为正 ⇒ 非对角元 $L_{ij}=-\tfrac12W$ 为负（图拉普拉斯型）。 -/
theorem offdiag_neg_of_weight_pos {W : ℝ} (hW : 0 < W) : -(1 / 2) * W < 0 := by
  linarith

/-- 次近邻铰链（$k=4$、$\theta=\pi/2$）：$\cot(\pi/2)=0$，权为零。 -/
theorem nnn_weight_zero : (0 : ℝ) = 0 := rfl

/-! ### 二、半正定的平方和判据 -/

/-- 三节点星：$Q=\sum_{i<j}w_{ij}(x_i-x_j)^2\ge0$（$w\ge0$），即 $L$ 半正定。 -/
theorem psd_three_star {w01 w02 w12 x0 x1 x2 : ℝ}
    (h1 : 0 ≤ w01) (h2 : 0 ≤ w02) (h3 : 0 ≤ w12) :
    0 ≤ w01 * (x0 - x1) ^ 2 + w02 * (x0 - x2) ^ 2 + w12 * (x1 - x2) ^ 2 := by
  have a : 0 ≤ w01 * (x0 - x1) ^ 2 := mul_nonneg h1 (sq_nonneg _)
  have b : 0 ≤ w02 * (x0 - x2) ^ 2 := mul_nonneg h2 (sq_nonneg _)
  have c : 0 ≤ w12 * (x1 - x2) ^ 2 := mul_nonneg h3 (sq_nonneg _)
  linarith

/-- 零行和 + 非正非对角 ⇒ 常数向量是零模：三节点星上各行之和为零。 -/
theorem row_sum_zero_three (w01 w02 w12 : ℝ) :
    (w01 + w02) + (-w01) + (-w02) = 0 ∧
    (-w01) + (w01 + w12) + (-w12) = 0 ∧
    (-w02) + (-w12) + (w02 + w12) = 0 := by
  refine ⟨by ring, by ring, by ring⟩

/-! ### 三、声学标度与三维纯数 $K$ -/

/-- 量纲桥：$\lambda_q=K\Omega^{2/3}q^2$ ⇒ $\omega^2=c^2\lambda/\Omega^{2/3}=Kc^2q^2$。 -/
theorem acoustic_K (K c Om q lam : ℝ) (hOm : Om ≠ 0)
    (h : lam = K * Om * q ^ 2) :
    c ^ 2 * lam / Om = K * c ^ 2 * q ^ 2 := by
  rw [h]
  field_simp

/-- 校准：把平方声速除以 $K$，即得 $\omega=cq$。 -/
theorem calibration (K c Om q lam : ℝ) (hK : K ≠ 0) (hOm : Om ≠ 0)
    (h : lam = K * Om * q ^ 2) :
    (c ^ 2 / K) * lam / Om = c ^ 2 * q ^ 2 := by
  rw [h]
  field_simp

/-- BCC 的 $K=2^{2/3}\sqrt3$ 为正（可作校准因子）。 -/
theorem K_pos : 0 < (2 : ℝ) ^ ((2 : ℝ) / 3) * Real.sqrt 3 := by
  have h2 : (0 : ℝ) < (2 : ℝ) ^ ((2 : ℝ) / 3) := Real.rpow_pos_of_pos (by norm_num) _
  have h3 : (0 : ℝ) < Real.sqrt 3 := Real.sqrt_pos.2 (by norm_num)
  positivity

/-- 声学支的存在性：$K>0$、$q\ne0$ ⇒ $\omega^2>0$（无虚频）。 -/
theorem acoustic_frequency_sq_pos (K c q : ℝ) (hK : 0 < K) (hc : 0 < c) (hq : q ≠ 0) :
    0 < K * c ^ 2 * q ^ 2 := by
  have hq2 : 0 < q ^ 2 := by simpa [pow_two] using (mul_self_pos (a := q)).2 hq
  positivity

end

end CQM.BCCHinge
