import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Block
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Tactic
import CartanAlgebra.Basic
import Superconductivity.CartanSuperconductivity

open scoped Matrix

/-!
# CQM 超导：元素嘉当矩阵与因果几何框架（可严格证明部分）

原则（与本库一贯的严格性铁律一致）：**只形式化能严格证明的内容**。
本节不做任何定义化推导或冒充：
- 因果耦合族 t_ij、Regge 边长等可证正性/单调性 → 定理；
- 中子缺陷谱判据**正方向**（ε < γ_min ⟹ 缺陷矩阵保持正定）以初等平方和
  （SOS）分解严格证明 → 定理；**反方向**已证 ε ≥ 5/4 时非正定
  （见证向量 (4,3,2,1)：xᴴC_nx = 20 − 16ε ≤ 0）。
  区间 [1, 5/4) 内正定保持未形式化（由 Sylvester 行列式判据成立），如实列为缺口。

内容：

1. **因果耦合族（§3.4）**：t_ij = t₀·e^{−d_ij/λ}·Θ(d_cut − d_ij) 的正性、
   截断恒零、对距离单调衰减、全局非负。
2. **组装对称性（§3.5）**：对称矩阵叠加保持对称（分子超嘉当矩阵 C_mol 的
   幺正约束的严格版本）；A₄ 直接拼接保持对称。
3. **中子缺陷（§3.2）**：缺陷矩阵 Δ = diag(−ε,0,0,0) 与缺陷嘉当矩阵
   C_n = A₄ − Δ 的对称性、ε = 0 退化、对角元、ε < 2 时缺陷位对角元为正，
   以及二次型分解与正定判据（SOS 版本）。
4. **Regge 边长（§5 步骤 15）**：l_e = κ/√λ_e 的正性。
-/

namespace CQM

/-! ## 1. 因果耦合族（§3.4） -/

/-- SPAF §3.4：原子对 (i,j) 的因果连接强度 t_ij = t₀·e^{−d_ij/λ}·Θ(d_cut − d_ij)。
    d_ij 为欧氏距离（脚手架假设，L0 赎回），Θ 为 Heaviside 截断。 -/
noncomputable def causalCoupling (t0 lam d dcut : ℝ) : ℝ :=
  if d ≤ dcut then t0 * Real.exp (-d / lam) else 0

/-- 截断之内因果耦合严格为正：t₀ > 0、λ > 0、d ≥ 0、d ≤ d_cut
    ⟹ t_ij > 0（因果连接在窗口内真实存在）。 -/
theorem causalCoupling_pos {t0 lam d dcut : ℝ} (ht0 : 0 < t0) (_hlam : 0 < lam)
    (_hd : 0 ≤ d) (hdcut : d ≤ dcut) : 0 < causalCoupling t0 lam d dcut := by
  unfold causalCoupling
  simp [hdcut]
  exact mul_pos ht0 (Real.exp_pos _)

/-- 截断之外恒为零：Θ 阶跃的严格形式（d > d_cut ⟹ t_ij = 0）。 -/
theorem causalCoupling_zero_of_cutoff (lam d dcut : ℝ) {t0 : ℝ} (h : ¬ d ≤ dcut) :
    causalCoupling t0 lam d dcut = 0 := by
  unfold causalCoupling
  simp [h]

/-- 因果耦合对距离单调衰减：d₁ ≤ d₂ ≤ d_cut ⟹ t(d₂) ≤ t(d₁)。
    体禀：e^{−d/λ} 随距离指数下降——越近的原子对因果连接越强。 -/
theorem causalCoupling_antitone_in_distance {t0 lam d1 d2 dcut : ℝ}
    (ht0 : 0 ≤ t0) (hlam : 0 < lam) (hd12 : d1 ≤ d2) (hd2c : d2 ≤ dcut) :
    causalCoupling t0 lam d2 dcut ≤ causalCoupling t0 lam d1 dcut := by
  have hd1c : d1 ≤ dcut := le_trans hd12 hd2c
  unfold causalCoupling
  simp [hd2c, hd1c]
  have hdiv : d1 / lam ≤ d2 / lam := div_le_div_of_nonneg_right hd12 (le_of_lt hlam)
  have hneg : -d2 / lam ≤ -d1 / lam := by
    rw [neg_div, neg_div]
    exact neg_le_neg hdiv
  have hexp : Real.exp (-d2 / lam) ≤ Real.exp (-d1 / lam) := Real.exp_monotone hneg
  exact mul_le_mul_of_nonneg_left hexp ht0

/-- 因果耦合全局非负（t₀ ≥ 0、λ > 0 ⟹ 连接强度永不取负）。 -/
theorem causalCoupling_nonneg {t0 lam : ℝ} (ht0 : 0 ≤ t0) (_hlam : 0 < lam) (d dcut : ℝ) :
    0 ≤ causalCoupling t0 lam d dcut := by
  by_cases h : d ≤ dcut
  · unfold causalCoupling
    simp [h]
    exact mul_nonneg ht0 (Real.exp_nonneg _)
  · unfold causalCoupling
    simp [h]

/-! ## 组装对称性（SPAF §3.5）：分子/宏观超嘉当矩阵的幺正约束 -/

/-- SPAF §3.5 严格版（叠加保对称）：对称矩阵之和仍对称。
    数学内容：全局幺正约束 Clmol† = Clmol 对"块对角拼接 + 耦合叠加"均保持。 -/
theorem superCartan_symmetric {n : Type*} (A B : Matrix n n ℝ)
    (hA : ∀ i j, A i j = A j i) (hB : ∀ i j, B i j = B j i) :
    ∀ i j, (A + B) i j = (A + B) j i := by
  intro i j
  simp [hA i j, hB i j]

/-- 块间耦合项 T_ij = t_ij · I₄ 对称：标量倍单位矩阵（实对称）。 -/
theorem identityBlock_symmetric (t : ℝ) :
    ∀ i j : Fin 4, (t • (1 : Matrix (Fin 4) (Fin 4) ℝ)) i j =
      (t • (1 : Matrix (Fin 4) (Fin 4) ℝ)) j i := by
  intro i j
  by_cases h : i = j
  · subst h
    simp
  · have h' : j ≠ i := by exact fun hji => h hji.symm
    simp [h, h']

/-- A₄ 直接拼接保持对称：⨁ₖ A₄ 仍满足实对称（§3.5 的 ⊕ 分量）。
   结合 superCartan_symmetric 与 identityBlock_symmetric，分子超嘉当矩阵
   C_mol = ⊕C_i + Σ T_ij 的各对称性分量全部被严格化。 -/
theorem cartanA4Stack_symmetric {n : ℕ} : ∀ a b : Fin 4 × Fin n,
    cartanA4Stack n a b = cartanA4Stack n b a := by
  intro ⟨i, k⟩ ⟨j, k'⟩
  unfold cartanA4Stack
  by_cases h : k = k'
  · subst h
    simp
    exact cartanA4_symmetric i j
  · have hk : ¬ k' = k := fun hkk => h hkk.symm
    simp [Matrix.blockDiagonal_apply', h, hk]

/-! ## 中子缺陷（SPAF §3.2）：缺陷嘉当矩阵 C_n = A₄ − ε·diag(1,0,0,0) -/

/-- SPAF §3.2：中子缺陷矩阵 Δ 的矩阵形式 diag(−ε, 0, 0, 0)。
   （epsilon 以能量无量纲化；ε = ℏ/(τ_n·Λ_cas)·f_bind(Z,A) 的微观赎回
   依赖本库未建的内在场 Λ_cas。） -/
noncomputable def neutronDefect (eps : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  Matrix.of fun i j => if i = 0 ∧ j = 0 then eps else 0

/-- SPAF §3.2：缺陷嘉当矩阵 C_n = A₄ − Δ = A₄ − ε·diag(1,0,0,0)
   （逐点定义：A₄ 逐元提升为实序再减缺陷；ε = 0 时退化为 cartanHamiltonian。） -/
noncomputable def neutronCartan (eps : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  fun i j => (cartanA4 i j : ℝ) - (if i = 0 ∧ j = 0 then eps else 0)

/-- 中子缺陷嘉当矩阵对称（§3.5）：C_n 与 C_p 同样满足实对称自伴约束。 -/
theorem neutronCartan_symmetric (eps : ℝ) : ∀ i j : Fin 4,
    neutronCartan eps i j = neutronCartan eps j i := by
  intro i j
  unfold neutronCartan
  have hA : (cartanA4 i j : ℝ) = (cartanA4 j i : ℝ) := by
    exact_mod_cast cartanA4_symmetric i j
  by_cases h : i = 0 ∧ j = 0
  · simp [h]
  · have h' : ¬ (j = 0 ∧ i = 0) := by
      rintro ⟨hj, hi⟩
      exact h ⟨hi, hj⟩
    simp [hA, h, h']

/-- ε = 0 时中子缺陷退化为质子：C_n(0) = C_p（A₄ 的 ℝ 提升 cartanHamiltonian）。 -/
theorem neutronCartan_zero_eq_proton :
    neutronCartan 0 = cartanHamiltonian := by
  unfold neutronCartan cartanHamiltonian
  ext i j
  simp

/-- 缺陷位对角元：C_n[0,0] = 2 − ε。 -/
theorem neutronCartan_diag00 (eps : ℝ) : neutronCartan eps 0 0 = 2 - eps := by
  unfold neutronCartan
  have hA : (cartanA4 0 0 : ℝ) = 2 := by
    rw [cartanA4_diag]
    norm_num
  simp [hA]

/-- 非缺陷位对角元保持：C_n[i,i] = 2（i ≠ 0）——缺陷仅作用于单个顶点。 -/
theorem neutronCartan_diag_ne00 (eps : ℝ) {i : Fin 4} (hi : i ≠ 0) :
    neutronCartan eps i i = 2 := by
  unfold neutronCartan
  have hA : (cartanA4 i i : ℝ) = 2 := by
    rw [cartanA4_diag]
    norm_num
  simp [hA, hi]

/-- 缺陷位对角元在 ε < 2 时保持为正（缺陷未吞掉该自环；谱判据的平凡必要条件）。 -/
theorem neutronCartan_diag00_pos {eps : ℝ} (heps : eps < 2) : 0 < neutronCartan eps 0 0 := by
  rw [neutronCartan_diag00]
  linarith

/-! ### 中子缺陷正定判据（SPAF §3.2 谱判据的初等版本） -/

/-- C_n 的显式矩阵形式：A₄ − ε·diag(1,0,0,0) 逐点展开为三对角形式。 -/
lemma neutronCartan_eq_explicit (eps : ℝ) :
    neutronCartan eps = !![(2 - eps), -1, 0, 0; -1, 2, -1, 0; 0, -1, 2, -1; 0, 0, -1, 2] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [neutronCartan, cartanA4]

/-- 二次型分解：xᴴC_nx = (1−ε)x₀² + x₃² + (x₀−x₁)² + (x₁−x₂)² + (x₂−x₃)²。
    正定判据的全部信息都藏在这个平方和（SOS）里。 -/
lemma neutronCartan_quadratic (eps : ℝ) (x : Fin 4 → ℝ) :
    star x ⬝ᵥ (neutronCartan eps *ᵥ x) =
      (1 - eps) * x 0 ^ 2 + x 3 ^ 2 + (x 0 - x 1) ^ 2 + (x 1 - x 2) ^ 2 + (x 2 - x 3) ^ 2 := by
  rw [neutronCartan_eq_explicit]
  simp [dotProduct]
  simp [Fin.sum_univ_four]
  ring

/-- 中子缺陷嘉当矩阵自伴：C_nᴴ = C_n（矩阵正定的共轭对称前提）。 -/
lemma neutronCartan_isHermitian (eps : ℝ) : (neutronCartan eps).IsHermitian := by
  ext i j
  simp [Matrix.conjTranspose_apply, neutronCartan_symmetric eps j i]

/-- SOS 的严格正性：ε < 1 时，上述平方和取零当且仅当 x = 0（逐项消零＋连锁相等）。 -/
lemma neutronCartan_quadForm_pos {eps : ℝ} (heps : eps < 1) {x : Fin 4 → ℝ} (hx : x ≠ 0) :
    0 < (1 - eps) * x 0 ^ 2 + x 3 ^ 2 + (x 0 - x 1) ^ 2 + (x 1 - x 2) ^ 2 + (x 2 - x 3) ^ 2 := by
  by_contra hnneg
  have hle : (1 - eps) * x 0 ^ 2 + x 3 ^ 2 + (x 0 - x 1) ^ 2 + (x 1 - x 2) ^ 2 + (x 2 - x 3) ^ 2 ≤ 0 :=
    le_of_not_gt hnneg
  have hn1 : 0 ≤ (1 - eps) * x 0 ^ 2 := mul_nonneg (le_of_lt (sub_pos.mpr heps)) (sq_nonneg (x 0))
  have hn2 : 0 ≤ x 3 ^ 2 := sq_nonneg (x 3)
  have hn3 : 0 ≤ (x 0 - x 1) ^ 2 := sq_nonneg (x 0 - x 1)
  have hn4 : 0 ≤ (x 1 - x 2) ^ 2 := sq_nonneg (x 1 - x 2)
  have hn5 : 0 ≤ (x 2 - x 3) ^ 2 := sq_nonneg (x 2 - x 3)
  have hz1 : (1 - eps) * x 0 ^ 2 = 0 := by linarith
  have hz2 : x 3 ^ 2 = 0 := by linarith
  have hz3 : (x 0 - x 1) ^ 2 = 0 := by linarith
  have hz4 : (x 1 - x 2) ^ 2 = 0 := by linarith
  have hz5 : (x 2 - x 3) ^ 2 = 0 := by linarith
  have hx0 : x 0 = 0 := by
    have hne : (1 : ℝ) - eps ≠ 0 := by
      rw [sub_ne_zero]
      exact (ne_of_lt heps).symm
    have hsq : x 0 ^ 2 = 0 := (mul_eq_zero.mp hz1).resolve_left hne
    exact sq_eq_zero_iff.mp hsq
  have hx1 : x 1 = 0 := by
    have hd : x 0 - x 1 = 0 := sq_eq_zero_iff.mp hz3
    linarith [hx0, hd]
  have hx2 : x 2 = 0 := by
    have hd : x 1 - x 2 = 0 := sq_eq_zero_iff.mp hz4
    linarith [hx1, hd]
  have hx3 : x 3 = 0 := by
    have hd : x 2 - x 3 = 0 := sq_eq_zero_iff.mp hz5
    linarith [hx2, hd]
  have hzero : x = 0 := by
    funext i
    fin_cases i <;> simp [hx0, hx1, hx2, hx3]
  exact hx hzero

/-- 谱判据正方向（SOS 版）：ε < 1 ⟹ C_n 正定。比判据原文 ε < γ_min ≈ 0.382 更宽。 -/
theorem neutronCartan_posDef_of_lt_one {eps : ℝ} (heps : eps < 1) :
    (neutronCartan eps).PosDef := by
  rw [Matrix.posDef_iff_dotProduct_mulVec]
  constructor
  · exact neutronCartan_isHermitian eps
  · intro x hx
    rw [neutronCartan_quadratic]
    exact neutronCartan_quadForm_pos heps hx

/-- 谱判据正方向（文档 §3.2 判据 1 的严格形式）：ε < γ_min ⟹ C_n 保持正定。 -/
theorem neutronCartan_posDef_of_lt_spectralGap {eps : ℝ} (heps : eps < spectralGap) :
    (neutronCartan eps).PosDef :=
  neutronCartan_posDef_of_lt_one (by linarith [spectralGap_lt_one])

/-- 谱判据反方向（直接构造）：ε ≥ 5/4 ⟹ C_n 非正定。
    见证向量 (4,3,2,1)：xᴴC_nx = 20 − 16ε ≤ 0，其中 det C_n = 5 − 4ε 恰在 ε = 5/4
    跨零点。故文档原述「ε ≥ γ_min 时正定性丧失」不成立（0.699 ≤ ε < 1 时正定保持）。 -/
theorem neutronCartan_not_posDef_of_five_fourths_le {eps : ℝ} (heps : 5 / 4 ≤ eps) :
    ¬ (neutronCartan eps).PosDef := by
  intro hpd
  let x : Fin 4 → ℝ := ![4, 3, 2, 1]
  have hx0 : x ≠ 0 := by
    intro hx
    have : (x 0 : ℝ) = 0 := congrArg (fun f : Fin 4 → ℝ => f 0) hx
    norm_num [x, Matrix.cons_val_zero] at this
  have hq : 0 < star x ⬝ᵥ (neutronCartan eps *ᵥ x) :=
    (Matrix.posDef_iff_dotProduct_mulVec.mp hpd).2 hx0
  have hq' : star x ⬝ᵥ (neutronCartan eps *ᵥ x) = 20 - 16 * eps := by
    rw [neutronCartan_quadratic]
    norm_num [x, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two,
      Matrix.cons_val_three]
    ring
  have hnonpos : 20 - 16 * eps ≤ 0 := by nlinarith
  rw [hq'] at hq
  exact (not_lt_of_ge hnonpos) hq

/-! ## Regge 边长（SPAF §5 步骤 15） -/

/-- SPAF §5 步骤 15：Regge 边长 l_e = κ / √λ_e（λ_e 为边 e 对应的耦合本征值）。 -/
noncomputable def reggeEdgeLength (kappa lam_e : ℝ) : ℝ := kappa / Real.sqrt lam_e

/-- 边长正性：κ > 0、λ_e > 0 ⟹ l_e > 0（正边长 = Regge 微积分良定义的必要条件）。 -/
theorem reggeEdgeLength_pos {kappa lam_e : ℝ} (hk : 0 < kappa) (hl : 0 < lam_e) :
    0 < reggeEdgeLength kappa lam_e := by
  unfold reggeEdgeLength
  exact div_pos hk (Real.sqrt_pos_of_pos hl)

/-! ## 中子缺陷正定区间闭合（Sylvester 判据，SPAF §3.2 补完） -/

/-- C_n(ε) 的第一个主子式：Δ₁(ε) = 2 − ε。 -/
noncomputable def neutronCartanMinor1 (eps : ℝ) : ℝ := 2 - eps

/-- C_n(ε) 的第二个主子式：Δ₂(ε) = det([[2-ε, -1], [-1, 2]]) = 3 − 2ε。 -/
noncomputable def neutronCartanMinor2 (eps : ℝ) : ℝ := 3 - 2 * eps

/-- C_n(ε) 的第三个主子式：Δ₃(ε) = det([[2-ε,-1,0],[-1,2,-1],[0,-1,2]]) = 4 − 3ε。 -/
noncomputable def neutronCartanMinor3 (eps : ℝ) : ℝ := 4 - 3 * eps

/-- C_n(ε) 的第四个主子式（行列式）：Δ₄(ε) = det(C_n) = 5 − 4ε。 -/
noncomputable def neutronCartanMinor4 (eps : ℝ) : ℝ := 5 - 4 * eps

/-- [Sylvester 判据闭合] ε < 5/4 时全部四个主子式严格为正。 -/
theorem neutronCartan_allMinors_pos_of_lt_five_fourths {eps : ℝ} (heps : eps < 5/4) :
    neutronCartanMinor1 eps > 0 ∧ neutronCartanMinor2 eps > 0 ∧
    neutronCartanMinor3 eps > 0 ∧ neutronCartanMinor4 eps > 0 := by
  unfold neutronCartanMinor1 neutronCartanMinor2 neutronCartanMinor3 neutronCartanMinor4
  constructor <;> (try constructor) <;> (try constructor) <;> nlinarith

/-- [Sylvester 判据闭合] ε < 5/4 ⟹ C_n 正定。
    结合已有定理 neutronCartan_posDef_of_lt_one（SOS 版，ε < 1）和
    neutronCartan_not_posDef_of_five_fourths_le（ε ≥ 5/4 非正定），
    **正定区间完全闭合**：C_n 正定 ⟺ ε < 5/4。
    这是 Sylvester 判据在 4 阶三对角扰动矩阵上的完整应用。 -/
theorem neutronCartan_posDef_of_lt_five_fourths {eps : ℝ} (heps : eps < 5/4) :
    (neutronCartan eps).PosDef := by
  -- 当 ε < 1 时，已有 SOS 证明
  by_cases h : eps < 1
  · exact neutronCartan_posDef_of_lt_one h
  · -- 当 1 ≤ ε < 5/4 时，使用 Cauchy-Schwarz 下界完成
    have hpos : 1 ≤ eps := by linarith
    rw [Matrix.posDef_iff_dotProduct_mulVec]
    constructor
    · exact neutronCartan_isHermitian eps
    · intro x hx
      rw [neutronCartan_quadratic]
      -- 二次型 Q(x) = (1-ε)x₀² + x₃² + (x₀-x₁)² + (x₁-x₂)² + (x₂-x₃)²
      -- 关键不等式（Cauchy-Schwarz）：由 x₀ = (x₀-x₁)+(x₁-x₂)+(x₂-x₃)+x₃ 得
      --   x₀² ≤ 4·((x₀-x₁)² + (x₁-x₂)² + (x₂-x₃)² + x₃²)
      -- 因此 Q(x) ≥ (1-ε)x₀² + x₀²/4 = (5/4-ε)x₀²
      by_cases hx0 : x 0 = 0
      · -- x₀ = 0：Q(x) = x₁² + x₃² + (x₁-x₂)² + (x₂-x₃)² > 0
        have hpos' : 0 < x 1 ^ 2 + x 3 ^ 2 + (x 1 - x 2) ^ 2 + (x 2 - x 3) ^ 2 := by
          by_contra! hle
          have hsum : x 1 ^ 2 + x 3 ^ 2 + (x 1 - x 2) ^ 2 + (x 2 - x 3) ^ 2 = 0 := by nlinarith
          have hx1 : x 1 = 0 := by
            have : x 1 ^ 2 = 0 := by nlinarith
            exact eq_zero_of_pow_eq_zero this
          have hx3 : x 3 = 0 := by
            have : x 3 ^ 2 = 0 := by nlinarith
            exact eq_zero_of_pow_eq_zero this
          have hx12 : x 1 - x 2 = 0 := by
            have : (x 1 - x 2) ^ 2 = 0 := by nlinarith
            exact eq_zero_of_pow_eq_zero this
          have hx23 : x 2 - x 3 = 0 := by
            have : (x 2 - x 3) ^ 2 = 0 := by nlinarith
            exact eq_zero_of_pow_eq_zero this
          have hx2 : x 2 = 0 := by
            rw [hx3] at hx23
            exact sub_eq_zero.mp hx23
          have hzero : x = 0 := by
            funext i
            fin_cases i <;> simp [hx0, hx1, hx2, hx3]
          exact hx hzero
        have : (1 - eps) * x 0 ^ 2 + x 3 ^ 2 + (x 0 - x 1) ^ 2 + (x 1 - x 2) ^ 2 + (x 2 - x 3) ^ 2 =
            x 1 ^ 2 + x 3 ^ 2 + (x 1 - x 2) ^ 2 + (x 2 - x 3) ^ 2 := by
          simp [hx0]; ring
        rw [this]
        exact hpos'
      · -- x₀ ≠ 0：使用 Cauchy-Schwarz 下界
        have hcs : x 0 ^ 2 ≤ 4 * ((x 0 - x 1) ^ 2 + (x 1 - x 2) ^ 2 + (x 2 - x 3) ^ 2 + x 3 ^ 2) := by
          -- Cauchy-Schwarz: (a+b+c+d)² ≤ 4(a²+b²+c²+d²)
          have hsum : x 0 = (x 0 - x 1) + (x 1 - x 2) + (x 2 - x 3) + x 3 := by ring
          rw [hsum]
          nlinarith [sq_nonneg ((x 0 - x 1) - (x 1 - x 2)),
            sq_nonneg ((x 0 - x 1) - (x 2 - x 3)),
            sq_nonneg ((x 0 - x 1) - x 3),
            sq_nonneg ((x 1 - x 2) - (x 2 - x 3)),
            sq_nonneg ((x 1 - x 2) - x 3),
            sq_nonneg ((x 2 - x 3) - x 3)]
        have hx0sq_pos : 0 < x 0 ^ 2 := sq_pos_iff.mpr hx0
        have hlower : (1 - eps) * x 0 ^ 2 + x 3 ^ 2 + (x 0 - x 1) ^ 2 + (x 1 - x 2) ^ 2 + (x 2 - x 3) ^ 2 ≥
            (5/4 - eps) * x 0 ^ 2 := by
          nlinarith
        have hcoeff_pos : 0 < 5/4 - eps := by linarith
        nlinarith

/-- [Sylvester 判据闭合] 正定区间的完整刻画：C_n 正定 ⟺ ε < 5/4。
    正向：ε < 5/4 ⟹ 正定（neutronCartan_posDef_of_lt_five_fourths）；
    反向：ε ≥ 5/4 ⟹ 非正定（neutronCartan_not_posDef_of_five_fourths_le）。
    因此 5/4 是 C_n 正定性的精确阈值。 -/
theorem neutronCartan_posDef_iff_lt_five_fourths {eps : ℝ} :
    (neutronCartan eps).PosDef ↔ eps < 5/4 := by
  constructor
  · intro hpd
    by_contra! hge
    exact neutronCartan_not_posDef_of_five_fourths_le hge hpd
  · exact neutronCartan_posDef_of_lt_five_fourths

/-! ## 分子超嘉当矩阵组装（SPAF §3.5 完整体） -/

/-- SPAF §3.5：原子类型标签（质子 / 中子）。 -/
inductive AtomType
  | proton
  | neutron
  deriving DecidableEq

/-- 单个原子的嘉当矩阵：质子 → A₄（cartanHamiltonian），中子 → C_n(ε)。 -/
noncomputable def atomCartan (a : AtomType) (eps : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  match a with
  | AtomType.proton => cartanHamiltonian
  | AtomType.neutron => neutronCartan eps

/-- 任意原子的嘉当矩阵保持对称（§3.5 幺正约束）。 -/
theorem atomCartan_symmetric (a : AtomType) (eps : ℝ) :
    ∀ i j : Fin 4, atomCartan a eps i j = atomCartan a eps j i := by
  cases a
  · -- 质子：A₄ 对称
    simp [atomCartan, cartanHamiltonian, cartanA4_symmetric]
  · -- 中子：C_n 对称
    unfold atomCartan
    exact neutronCartan_symmetric eps

/-- 分子超嘉当矩阵：C_mol = ⊕_k C_atom(k) + Σ_{i<j} T_ij。
    n 个原子，每个原子带一个 4×4 嘉当块；
    块间耦合项 T_ij = t_ij · I₄（标量倍单位矩阵）。
    索引 = (块内顶点, 原子号) = Fin 4 × Fin n。 -/
noncomputable def molecularCartan (n : ℕ) (atoms : Fin n → AtomType)
    (eps : ℝ) (tMatrix : Fin n → Fin n → ℝ) : Matrix (Fin 4 × Fin n) (Fin 4 × Fin n) ℝ :=
  -- 块对角部分：⊕_k C_atom(k)
  Matrix.blockDiagonal (fun k : Fin n => atomCartan (atoms k) eps) +
  -- 块间耦合：Σ_{i≠j} t_ij · I₄
  Matrix.of (fun ⟨i, k⟩ ⟨j, k'⟩ =>
    if k = k' then 0 else tMatrix k k' * (if i = j then 1 else 0))

/-- 分子超嘉当矩阵的块对角部分（不含块间耦合）。 -/
noncomputable def molecularCartanBlockDiag (n : ℕ) (atoms : Fin n → AtomType)
    (eps : ℝ) : Matrix (Fin 4 × Fin n) (Fin 4 × Fin n) ℝ :=
  Matrix.blockDiagonal (fun k : Fin n => atomCartan (atoms k) eps)

/-- 块对角部分保对称。 -/
theorem molecularCartanBlockDiag_symmetric (n : ℕ) (atoms : Fin n → AtomType) (eps : ℝ) :
    ∀ a b : Fin 4 × Fin n, molecularCartanBlockDiag n atoms eps a b =
      molecularCartanBlockDiag n atoms eps b a := by
  intro ⟨i, k⟩ ⟨j, k'⟩
  unfold molecularCartanBlockDiag
  by_cases h : k = k'
  · subst h
    simp
    exact atomCartan_symmetric (atoms k) eps i j
  · have hk : ¬ k' = k := fun hkk => h hkk.symm
    simp [Matrix.blockDiagonal_apply', h, hk]

/-- 分子超嘉当矩阵保对称（块对角 + 块间耦合均保对称）。 -/
theorem molecularCartan_symmetric (n : ℕ) (atoms : Fin n → AtomType)
    (eps : ℝ) (tMatrix : Fin n → Fin n → ℝ) (hT : ∀ i j, tMatrix i j = tMatrix j i) :
    ∀ a b : Fin 4 × Fin n, molecularCartan n atoms eps tMatrix a b =
      molecularCartan n atoms eps tMatrix b a := by
  intro ⟨i, k⟩ ⟨j, k'⟩
  unfold molecularCartan
  rw [Matrix.add_apply, Matrix.add_apply]
  -- 块对角部分对称
  have h_block : Matrix.blockDiagonal (fun k => atomCartan (atoms k) eps) (i, k) (j, k') =
      Matrix.blockDiagonal (fun k => atomCartan (atoms k) eps) (j, k') (i, k) := by
    by_cases hkk : k = k'
    · subst hkk; simp; exact atomCartan_symmetric (atoms k) eps i j
    · have hkk' : k' ≠ k := Ne.symm hkk
      simp [Matrix.blockDiagonal_apply', hkk, hkk']
  rw [h_block]
  -- 块间耦合部分对称
  simp only [Matrix.of_apply]
  by_cases hkk : k = k'
  · subst hkk; simp
  · have hkk' : k' ≠ k := Ne.symm hkk
    by_cases hij : i = j
    · subst hij; simp [hkk, hkk', hT k k']
    · have hji : j ≠ i := Ne.symm hij
      simp [hij, hji, hkk, hkk']

/-- 纯质子分子（所有原子均为质子）：块对角部分 = A₄ 直接拼接（提升到 ℝ）。 -/
theorem molecularCartan_allProtons (n : ℕ) :
    molecularCartanBlockDiag n (fun _ => AtomType.proton) 0 =
    (fun i j => ((cartanA4Stack n) i j : ℝ)) := by
  unfold molecularCartanBlockDiag atomCartan cartanHamiltonian cartanA4Stack
  ext i j
  simp [Matrix.blockDiagonal_apply]

/-- 中子缺陷嘉当矩阵的迹：Tr(C_n) = 8 - ε。
    C_n 的对角元：2-ε, 2, 2, 2，迹 = 8 - ε。 -/
theorem neutronCartan_trace (eps : ℝ) : Matrix.trace (neutronCartan eps) = 8 - eps := by
  have h0 : neutronCartan eps 0 0 = 2 - eps := neutronCartan_diag00 eps
  have h1 : neutronCartan eps 1 1 = 2 := neutronCartan_diag_ne00 eps (by decide)
  have h2 : neutronCartan eps 2 2 = 2 := neutronCartan_diag_ne00 eps (by decide)
  have h3 : neutronCartan eps 3 3 = 2 := neutronCartan_diag_ne00 eps (by decide)
  simp [Matrix.trace, Fin.sum_univ_four, h0, h1, h2, h3]
  ring

/-- 分子超嘉当矩阵的迹：Tr(C_mol) = Σ_k Tr(C_atom(k)) = 8·n_p + (8-ε)·n_n。
    其中 n_p 为质子数，n_n 为中子数。 -/
theorem molecularCartan_trace (n : ℕ) (atoms : Fin n → AtomType) (eps : ℝ)
    (tMatrix : Fin n → Fin n → ℝ) :
    Matrix.trace (molecularCartan n atoms eps tMatrix) =
      (∑ k : Fin n, match atoms k with
        | AtomType.proton => 8
        | AtomType.neutron => 8 - eps) := by
  unfold molecularCartan
  -- 块间耦合项对角元全部为零，不贡献迹
  have h_coupling_trace_zero : Matrix.trace (Matrix.of (fun (x : Fin 4 × Fin n) (y : Fin 4 × Fin n) =>
      match x, y with
      | (i, k), (j, k') => if k = k' then 0 else tMatrix k k' * (if i = j then 1 else 0))) = 0 := by
    simp [Matrix.trace, Matrix.of_apply]
  rw [Matrix.trace_add, h_coupling_trace_zero, add_zero]
  -- molecularCartanBlockDiag already simplified to blockDiagonal
  rw [Matrix.trace_blockDiagonal]
  simp_rw [atomCartan]
  apply Finset.sum_congr rfl
  intro k _
  cases atoms k
  · -- 质子：迹 = 8
    have h_trace : Matrix.trace cartanHamiltonian = (8 : ℝ) := by
      rw [Matrix.trace]
      simp [cartanHamiltonian]
      exact_mod_cast cartanA4_trace
    exact h_trace
  · -- 中子：迹 = 8 - ε
    rw [neutronCartan_trace eps]

/-! ## 体投影与低能谱分析（SPAF §4 计算管线步骤 7-9） -/

/-- SPAF §4 步骤 7-8：体嘉当矩阵 C_bulk 为大量分子超嘉当矩阵的组装。
    对 N 个分子，C_bulk = ⊕_m C_mol(m) + Σ_{m<m'} T_mm'。
    此定义以简化形式给出：N 个分子 × n 个原子每分子。
    索引 = (块内顶点, 分子内原子号, 分子号) = Fin 4 × Fin n × Fin N。 -/
noncomputable def bulkCartan (n N : ℕ) (atoms : Fin (n * N) → AtomType)
    (eps : ℝ) (tMatrix : Fin (n * N) → Fin (n * N) → ℝ) :
    Matrix (Fin 4 × Fin (n * N)) (Fin 4 × Fin (n * N)) ℝ :=
  -- 简化：使用分子超嘉当矩阵 + 跨分子耦合
  -- 实际组装 = 块对角（每分子 C_mol）+ 跨分子 T_ij
  -- 此处以块对角形式定义，跨分子耦合由 tMatrix 承载
  molecularCartan (n * N) atoms eps tMatrix

/-- 体投影：对体嘉当矩阵 C_bulk 进行谱投影，保留能量低于截断 E_cut 的子空间。
    P_low = Σ_{λ_k ≤ E_cut} |v_k⟩⟨v_k|。
    此定义以谱投影算子形式给出，用于后续超导序参量计算。 -/
noncomputable def bulkLowEnergyProjection (n N : ℕ) (atoms : Fin (n * N) → AtomType)
    (eps E_cut : ℝ) (tMatrix : Fin (n * N) → Fin (n * N) → ℝ) :
    Matrix (Fin 4 × Fin (n * N)) (Fin 4 × Fin (n * N)) ℝ :=
  -- 简化：对角元取 Θ(E_cut - C_bulk[i,i]) 的阶梯投影
  -- 精确投影需对角化，此处以对角近似形式声明
  Matrix.of (fun a b =>
    if a = b then
      let val := bulkCartan n N atoms eps tMatrix a a
      if val ≤ E_cut then 1 else 0
    else 0)

/-- 低能投影的幂等性（形式声明）：P² = P（投影算子基本性质）。 -/
theorem bulkLowEnergyProjection_idempotent (n N : ℕ) (atoms : Fin (n * N) → AtomType)
    (eps E_cut : ℝ) (tMatrix : Fin (n * N) → Fin (n * N) → ℝ) :
    bulkLowEnergyProjection n N atoms eps E_cut tMatrix *
    bulkLowEnergyProjection n N atoms eps E_cut tMatrix =
    bulkLowEnergyProjection n N atoms eps E_cut tMatrix := by
  ext i j
  simp [bulkLowEnergyProjection, Matrix.mul_apply, Matrix.of_apply]
  by_cases h : i = j
  · subst h
    simp
  · simp [h]

/-! ## 分子超嘉当矩阵正定性（SPAF §3.5 补完） -/

/-- A₄ 嘉当矩阵的 ℝ 提升 cartanHamiltonian 是正定的。
    二次型分解：xᴴA₄x = x₀² + x₃² + (x₀−x₁)² + (x₁−x₂)² + (x₂−x₃)² > 0。
    由 neutronCartan_quadratic 在 ε = 0 处直接给出（neutronCartan_zero_eq_proton）。 -/
lemma cartanHamiltonian_posDef : (cartanHamiltonian : Matrix (Fin 4) (Fin 4) ℝ).PosDef := by
  have h : cartanHamiltonian = neutronCartan 0 := by
    rw [neutronCartan_zero_eq_proton]
  rw [h]
  exact neutronCartan_posDef_of_lt_one (by norm_num : (0 : ℝ) < 1)

/-- 纯质子分子（无块间耦合）的正定性：C_mol = ⊕_{k=1}^n A₄ 严格正定。
    每个质子块 = A₄ → 正定（cartanHamiltonian_posDef），
    块对角保持正定（二次型按块分解为各块二次型之和，均正）。 -/
theorem molecularCartanBlockDiag_posDef_of_allProtons (n : ℕ) (eps : ℝ) :
    (molecularCartanBlockDiag n (fun _ => AtomType.proton) eps).PosDef := by
  unfold molecularCartanBlockDiag
  simp [atomCartan]
  -- Goal: (Matrix.blockDiagonal (fun (_ : Fin n) => cartanHamiltonian)).PosDef
  have h_posDef : cartanHamiltonian.PosDef := cartanHamiltonian_posDef
  rw [Matrix.posDef_iff_dotProduct_mulVec]
  refine ⟨?_, ?_⟩
  · -- IsHermitian: Aᴴ = A
    rw [Matrix.IsHermitian]
    ext i j
    simp only [Matrix.conjTranspose_apply]
    rw [Matrix.blockDiagonal_apply, Matrix.blockDiagonal_apply]
    by_cases h : i.2 = j.2
    · have h_symm : cartanHamiltonian i.1 j.1 = cartanHamiltonian j.1 i.1 := by
        unfold cartanHamiltonian
        exact_mod_cast cartanA4_symmetric i.1 j.1
      have h_eq : j.2 = i.2 := h.symm
      rw [if_pos h, if_pos h_eq, h_symm]
      simp
    · have h_ne : ¬ j.2 = i.2 := by
        intro hji; apply h; exact hji.symm
      rw [if_neg h, if_neg h_ne]
      simp
  · -- quadratic form positivity: ∀ x ≠ 0, 0 < star x ⬝ᵥ (blockDiagonal M) *ᵥ x
    intro x hx
    -- 分解二次型：star x ⬝ᵥ (blockDiag M) *ᵥ x = Σ_k star x_k ⬝ᵥ M *ᵥ x_k
    -- Step 1: 展开 (blockDiag M) *ᵥ x
    have h_mulVec : ∀ (p : Fin 4 × Fin n),
        (Matrix.blockDiagonal (fun (_ : Fin n) => cartanHamiltonian) *ᵥ x) p =
          ∑ j : Fin 4, cartanHamiltonian p.1 j * x (j, p.2) := by
      intro ⟨i, k⟩
      simp only [Matrix.mulVec, Matrix.blockDiagonal_apply, dotProduct]
      rw [Fintype.sum_prod_type]
      simp
    -- Step 2: 展开点积并重排求和
    have h_quad : star x ⬝ᵥ (Matrix.blockDiagonal (fun (_ : Fin n) => cartanHamiltonian) *ᵥ x) =
        ∑ k : Fin n, star (fun (i : Fin 4) => x (i, k)) ⬝ᵥ
          (cartanHamiltonian *ᵥ (fun (i : Fin 4) => x (i, k))) := by
      simp only [dotProduct, h_mulVec]
      rw [Fintype.sum_prod_type_right]
      simp only [dotProduct, Matrix.mulVec]
      simp
    rw [h_quad]
    -- Step 3: 每项非负，且至少一项严格正
    have h_pos := (Matrix.posDef_iff_dotProduct_mulVec.mp h_posDef).2
    -- 存在 k 使 x_k ≠ 0
    have h_nonzero : ∃ k : Fin n, (fun (i : Fin 4) => x (i, k)) ≠ 0 := by
      by_contra! h_all
      apply hx
      ext ⟨i, k⟩
      have hx_ik : x (i, k) = 0 := by
        simpa using congrArg (fun (f : Fin 4 → ℝ) => f i) (h_all k)
      simpa using hx_ik
    rcases h_nonzero with ⟨k, hk⟩
    have h_pos_k : 0 < star (fun (i : Fin 4) => x (i, k)) ⬝ᵥ
        (cartanHamiltonian *ᵥ (fun (i : Fin 4) => x (i, k))) :=
      @h_pos (fun (i : Fin 4) => x (i, k)) hk
    have h_nonneg : ∀ k' : Fin n, 0 ≤ star (fun (i : Fin 4) => x (i, k')) ⬝ᵥ
        (cartanHamiltonian *ᵥ (fun (i : Fin 4) => x (i, k'))) := by
      intro k'
      by_cases hzero : (fun (i : Fin 4) => x (i, k')) = 0
      · rw [hzero]
        simp [dotProduct, Matrix.mulVec]
      · exact le_of_lt (@h_pos (fun (i : Fin 4) => x (i, k')) hzero)
    exact Finset.sum_pos' (fun k' _ => h_nonneg k') ⟨k, Finset.mem_univ k, h_pos_k⟩

/-- 纯质子分子（无块间耦合）的正定性（推论）。
    所有原子均为质子、且无块间耦合时，C_mol = ⊕ A₄ 严格正定。 -/
theorem molecularCartan_posDef_of_allProtons_zeroCoupling (n : ℕ) (eps : ℝ) :
    (molecularCartan n (fun _ => AtomType.proton) eps (fun _ _ => 0)).PosDef := by
  have h_eq : molecularCartan n (fun _ => AtomType.proton) eps (fun _ _ => 0) =
      molecularCartanBlockDiag n (fun _ => AtomType.proton) eps := by
    unfold molecularCartan molecularCartanBlockDiag
    ext i j
    simp
  rw [h_eq]
  exact molecularCartanBlockDiag_posDef_of_allProtons n eps

/-! ## 体嘉当矩阵迹与尺度分析 -/

/-- 体嘉当矩阵的迹：Tr(C_bulk) = 8·n·N - ε·n_n。
    n·N 为总原子数，n_n 为中子数。
    迹 = 禁闭几何的总能量尺度，随原子数线性增长。 -/
theorem bulkCartan_trace (n N : ℕ) (atoms : Fin (n * N) → AtomType) (eps : ℝ)
    (tMatrix : Fin (n * N) → Fin (n * N) → ℝ) :
    Matrix.trace (bulkCartan n N atoms eps tMatrix) =
      (∑ k : Fin (n * N), match atoms k with
        | AtomType.proton => 8
        | AtomType.neutron => 8 - eps) := by
  unfold bulkCartan
  exact molecularCartan_trace (n * N) atoms eps tMatrix

/-- 体低能投影的维度估计：Tr(P_low) = 能量低于 E_cut 的对角元数目。
    对纯质子体系，C_bulk 对角元 ≈ 2，故 Tr(P_low) ≈ min(4·n·N, 4·n·N)。 -/
theorem bulkLowEnergyProjection_trace (n N : ℕ) (atoms : Fin (n * N) → AtomType)
    (eps E_cut : ℝ) (tMatrix : Fin (n * N) → Fin (n * N) → ℝ) :
    Matrix.trace (bulkLowEnergyProjection n N atoms eps E_cut tMatrix) =
      (∑ a : Fin 4 × Fin (n * N),
        let val := bulkCartan n N atoms eps tMatrix a a
        if val ≤ E_cut then 1 else 0) := by
  unfold bulkLowEnergyProjection
  simp [Matrix.trace, Matrix.of_apply]

end CQM