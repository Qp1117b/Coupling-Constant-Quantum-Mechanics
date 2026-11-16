import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# 超导交叉判别范式 (CrossingParadigm)

对应探索文档 `10 探索/CQM_探索_自能支Tc交叉判别计算.md`（§2、§3、§4、§9、§10）与
`06 超导/CQM_超导_非马尔可夫对接_方案.md`（§三、§四、§七）。

## 定位（如实标注：第一性演绎，非拟合）

本模块只形式化**范式层的代数演绎**——每条定理都从显式定义与显式假设出发，
经实数代数推出，不含任何数值凑配：

- **定义引入（不作断言）**：ansatz 权重 `weightAnsatz n = (n²−1)/n²`（对应
  `06` §11.10 的分支函数；其第一性推导属 06 方案 §四分支 A 路线，**未在此证明**）、
  自能谱线 `selfEnergySpectrum`（对应 06 方案 §三的单极形式，除法以逆元记号书写）；
  Λ（对应文档预因子 Λ²）、τ_g、γ_n 均为**显式参数**，不赋值、不引入数值。
- **演绎定理**：权重差闭式、P0 范式定理（解耦权重下交叉点核宽与材料参数无关）、
  特例 τ_g² = 3/(4Δγ)、交叉需求量闭式、自能谱的谱序不变性（SE-A 无交叉与
  §9.2 分支间零交叉的公共代数根源）、自能交叉方程显式根满足方程。

## 边界

- 本模块不含 `sorry`、`admit`、`native_decide`、`unsafe`、新增 `axiom`；
- 不含任何数值校验（数值层见探索文档 §5、§9.1、§9.3，定位为验证检验）；
- ansatz 权重与自能形式的「物理正确性」不是本模块的断言对象——本模块只演绎：
  **给定**谱方程与权重，**推出**交叉结构的全部代数后果。

## 定理清单

| 定理 | 内容 | 对应探索文档 |
|:---|:---|:---|
| `weightAnsatz_diff` | `w_m − w_n = (m²−n²)/(n²m²)`（n<m） | §9.1 |
| `weightAnsatz_adjacent_diff` | 相邻对差 `(2n+1)/(n²(n+1)²)` | §10.3 |
| `crossingWidth_P0` | 解耦权重范式定理 `τ_g² = (w_m−w_n)/Δγ` | §10.2 |
| `crossingWidth_P0_ansatz12` | 特例 `τ_g² = 3/(4Δγ)` | §2 |
| `crossingDemand_ansatz` | 需求量 `V₀ = n²m²(γ_m−γ_n)/(m²−n²)` | §9.1 |
| `selfEnergy_factor_lt` | 自能因子在 γ>0 严格递减 | §3 |
| `selfEnergySpectrum_lt_of_lt` | γ₁<γ₂ ⟹ λ₁<λ₂（SE-A 与 §9.2 公共根源） | §3、§9.2 |
| `selfEnergy_noCrossing` | 全分支同浴时 `λ₁ = λ₂` 无解 | §3 |
| `selfEnergy_crossing_root_add` | 自能交叉方程显式根满足方程 | §4 |
-/

namespace CQM
namespace CrossingParadigm

/-! ## 定义（引入，不作断言） -/

/-- ansatz 权重（`06` §11.10 的分支函数 `w_n = (n²−1)/n²`）。
    `n` 为分支序号（正实数），定义域 `1 ≤ n`。此定义只引入记号：
    该权重的第一性来源属 06 方案 §四分支 A 路线，未在此证明。 -/
noncomputable def weightAnsatz (n : ℝ) : ℝ :=
  (n ^ 2 - 1) / n ^ 2

/-- 自能谱线（06 方案 §三 单极形式，U2 口径）：`λ_n = γ_n − Λ·τ_g·(1+(γ_n·τ_g)²)⁻¹`，
    与文档记号 `Λ·τ_g/(1+(γ_n·τ_g)²)` 同一（除法以逆元记号书写）。
    `Λ` 对应文档预因子 Λ²（未赋值参数）；`t` 对应核宽 τ_g。定义只引入记号。 -/
noncomputable def selfEnergySpectrum (γ t Λ : ℝ) : ℝ :=
  γ - Λ * t * (1 + (γ * t) ^ 2)⁻¹

/-! ## ansatz 权重的代数（§9.1） -/

/-- 一般分支对的权重差（§9.1）：`n < m` 时
    `w_m − w_n = (m²−n²)/(n²m²)`，权重差为正（权重随分支序号单调递增）。 -/
theorem weightAnsatz_diff {n m : ℝ} (hn : 1 ≤ n) (hm : n < m) :
    weightAnsatz m - weightAnsatz n = (m ^ 2 - n ^ 2) / (n ^ 2 * m ^ 2) := by
  have hn0 : n ≠ 0 := ne_of_gt (by linarith)
  have hm0 : m ≠ 0 := ne_of_gt (by linarith)
  unfold weightAnsatz
  field_simp
  ring

/-- 相邻分支对的权重差（§10.3）：`w_{n+1} − w_n = (2n+1)/(n²(n+1)²)`。
    这是交叉阶梯幂律截断公式 `n_max ≈ (2σ_p0²/Δγ)^{1/3}` 的代数起点。 -/
theorem weightAnsatz_adjacent_diff (n : ℝ) (hn : 1 ≤ n) :
    weightAnsatz (n + 1) - weightAnsatz n = (2 * n + 1) / (n ^ 2 * (n + 1) ^ 2) := by
  have hn0 : n ≠ 0 := ne_of_gt (by linarith)
  have hn1 : (n + 1) ≠ 0 := ne_of_gt (by linarith)
  unfold weightAnsatz
  field_simp
  ring

/-- 权重差为正：`n < m` 时 `w_m − w_n > 0`（供 P0 定理与需求量定理调用）。 -/
theorem weightAnsatz_diff_pos {n m : ℝ} (hn : 1 ≤ n) (hm : n < m) :
    0 < weightAnsatz m - weightAnsatz n := by
  rw [weightAnsatz_diff hn hm]
  have hnp : (0 : ℝ) < n := by linarith
  have hmp : (0 : ℝ) < m := by linarith
  have hsq : n ^ 2 < m ^ 2 := by
    have h2 : n * n < n * m := mul_lt_mul_of_pos_left hm hnp
    have h3 : n * m < m * m := mul_lt_mul_of_pos_right hm hmp
    rw [pow_two, pow_two]
    exact lt_trans h2 h3
  have hnpos : (0 : ℝ) < n ^ 2 := by
    rw [pow_two]
    exact mul_pos hnp hnp
  have hmpos : (0 : ℝ) < m ^ 2 := by
    rw [pow_two]
    exact mul_pos hmp hmp
  exact div_pos (by linarith) (mul_pos hnpos hmpos)

/-- **u 坐标权重恒等式（总装文档 §1.2）**：ansatz 权重可写为耦合空间坐标函数
    `w(n) = 1 − e^(−u_n)`，其中 `u_n = 2·ln n`（跃迁耦级量子化，`e^(u_n) = n²`）。
    这把 §11.10 的 n-表示与 §11.6 的 u-表示（`V_δ = (e^u−1)/e^u`）统一——
    类型 I 权重在耦合空间坐标下的显式形式。 -/
theorem weightAnsatz_eq_one_minus_exp_neg_two_log (n : ℝ) (hn : 1 ≤ n) :
    weightAnsatz n = 1 - Real.exp (-(2 * Real.log n)) := by
  have hnp : (0 : ℝ) < n := by linarith
  have hn0 : n ≠ 0 := ne_of_gt hnp
  have h2 : Real.exp (2 * Real.log n) = n ^ 2 := by
    rw [two_mul, Real.exp_add, Real.exp_log hnp]
    ring
  have hexp : Real.exp (-(2 * Real.log n)) = (n ^ 2)⁻¹ := by
    rw [Real.exp_neg, h2]
  unfold weightAnsatz
  rw [hexp]
  field_simp
  try ring

/-! ## P0 范式定理（§10.2）：解耦权重的交叉核宽普适 -/

/-- **P0 范式定理**（§10.2）：设谱方程 `λ_n = γ_n − V₀·w_n` 中权重与温度解耦
    （`V₀ = σ₀²·s`，`s = tanh(θ_D/2T)`，核宽 `τ_g = 1/(σ₀√s)`）。
    若分支对 `(n,m)` 在温度 `T_c` 处交叉（`V₀·(w_m−w_n) = γ_m−γ_n`），则交叉点核宽

    `τ_g² = (w_m−w_n)/Δγ_nm`

    **与全部材料参数（β、δ_v、Δδ₀）无关**，只由谱隙与权重差之比决定。
    证明只有三步代数：`τ_g² = 1/V₀`（谱方程定义）、交叉条件、除法。 -/
theorem crossingWidth_P0 {σ₀ s V₀ wₙ wₘ Δγ : ℝ}
    (hσ : 0 < σ₀) (hs : 0 < s) (hV : 0 < V₀) (hΔ : 0 < Δγ)
    (hVeq : V₀ = σ₀ ^ 2 * s)
    (hwdiff : 0 < wₘ - wₙ)
    (hcross : V₀ * (wₘ - wₙ) = Δγ) :
    (1 / (σ₀ * Real.sqrt s)) ^ 2 = (wₘ - wₙ) / Δγ := by
  have hsqrtpos : 0 < Real.sqrt s := Real.sqrt_pos.mpr hs
  have hsq1 : (1 / (σ₀ * Real.sqrt s)) ^ 2 = 1 / ((σ₀ * Real.sqrt s) ^ 2) := by
    have h1 : (1 / (σ₀ * Real.sqrt s)) = (σ₀ * Real.sqrt s)⁻¹ := by simp
    rw [h1, inv_pow]
    simp
  have hsq2 : (σ₀ * Real.sqrt s) ^ 2 = σ₀ ^ 2 * s := by
    rw [mul_pow, Real.sq_sqrt hs.le]
  rw [hsq1, hsq2, ← hVeq]
  field_simp [hcross]
  exact hcross.symm

/-- **特例（§2 恒等式）**：ansatz 权重下 `(1,2)` 交叉点核宽
    `τ_g² = 3/(4Δγ)`——即探索文档 §2 的 `τ_g(T_c^ans) = √(3/(4Δγ))`。
    材料参数全部消去；数值验证（0.329994）属验证检验，不在此断言。 -/
theorem crossingWidth_P0_ansatz12 {σ₀ s V₀ Δγ : ℝ}
    (hσ : 0 < σ₀) (hs : 0 < s) (hV : 0 < V₀) (hΔ : 0 < Δγ)
    (hVeq : V₀ = σ₀ ^ 2 * s)
    (hcross : V₀ * (weightAnsatz 2 - weightAnsatz 1) = Δγ) :
    (1 / (σ₀ * Real.sqrt s)) ^ 2 = 3 / (4 * Δγ) := by
  have hwd : weightAnsatz 2 - weightAnsatz 1 = 3 / 4 := by
    unfold weightAnsatz
    norm_num
  have hpos : (0 : ℝ) < weightAnsatz 2 - weightAnsatz 1 := by
    rw [hwd]
    norm_num
  have h := crossingWidth_P0 hσ hs hV hΔ hVeq hpos hcross
  rw [hwd] at h
  rw [h]
  ring

/-! ## 交叉需求量（§9.1） -/

/-- **需求量闭式**（§9.1）：ansatz 分支对 `(n,m)`（`n < m`）的交叉条件
    `V₀·(w_m−w_n) = γ_m−γ_n` 等价于

    `V₀ = n²m²·(γ_m−γ_n)/(m²−n²)`。

    存在性判据 `V₀^need ≤ σ_p0²` 由此式与零温方差上限比较而得
    （数值层属验证检验；幂律截断 `n_max ≈ (2σ_p0²/Δγ)^{1/3}` 的粗粒化不在本模块）。 -/
theorem crossingDemand_ansatz {V₀ γₙ γₘ n m : ℝ}
    (hn : 1 ≤ n) (hm : n < m)
    (hΔ : 0 < γₘ - γₙ)
    (hcross : V₀ * (weightAnsatz m - weightAnsatz n) = γₘ - γₙ) :
    V₀ = n ^ 2 * m ^ 2 * (γₘ - γₙ) / (m ^ 2 - n ^ 2) := by
  rw [weightAnsatz_diff hn hm] at hcross
  have hnp : (0 : ℝ) < n := by linarith
  have hmp : (0 : ℝ) < m := by linarith
  have hsq : n ^ 2 < m ^ 2 := by
    have h2 : n * n < n * m := mul_lt_mul_of_pos_left hm hnp
    have h3 : n * m < m * m := mul_lt_mul_of_pos_right hm hmp
    rw [pow_two, pow_two]
    exact lt_trans h2 h3
  have hmn : m ^ 2 - n ^ 2 ≠ 0 := ne_of_gt (by linarith)
  have hB : n ^ 2 * m ^ 2 ≠ 0 := by
    have h4 : (0 : ℝ) < n ^ 2 := by
      rw [pow_two]
      exact mul_pos hnp hnp
    have h5 : (0 : ℝ) < m ^ 2 := by
      rw [pow_two]
      exact mul_pos hmp hmp
    exact ne_of_gt (mul_pos h4 h5)
  rw [eq_div_iff hmn]
  have h2 : n ^ 2 * m ^ 2 * (γₘ - γₙ)
      = n ^ 2 * m ^ 2 * (V₀ * ((m ^ 2 - n ^ 2) / (n ^ 2 * m ^ 2))) := by
    rw [hcross]
  rw [h2]
  field_simp [hB]

/-! ## 自能谱的谱序不变性（§3、§9.2） -/

/-- 自能因子 `f(γ) = 1/(1+(γ·t)²)` 在 `γ > 0` 上随 γ 严格递减（`t > 0`）：
    `γ₁ < γ₂` 给出 `f(γ₂) < f(γ₁)`。 -/
theorem selfEnergy_factor_lt {t γ₁ γ₂ : ℝ} (ht : 0 < t) (h₁ : 0 < γ₁) (h₂ : 0 < γ₂)
    (hlt : γ₁ < γ₂) :
    1 / (1 + (γ₂ * t) ^ 2) < 1 / (1 + (γ₁ * t) ^ 2) := by
  have hp1 : 0 < 1 + (γ₁ * t) ^ 2 := by positivity
  have h1 : γ₁ * t < γ₂ * t := mul_lt_mul_of_pos_right hlt ht
  have hp1t : 0 < γ₁ * t := mul_pos h₁ ht
  have hsq : (γ₁ * t) ^ 2 < (γ₂ * t) ^ 2 := by
    have h2 : γ₁ * t * (γ₁ * t) < γ₁ * t * (γ₂ * t) := mul_lt_mul_of_pos_left h1 hp1t
    have h3 : γ₁ * t * (γ₂ * t) < γ₂ * t * (γ₂ * t) :=
      mul_lt_mul_of_pos_right h1 (mul_pos h₂ ht)
    rw [pow_two, pow_two]
    exact lt_trans h2 h3
  have hsum : 1 + (γ₁ * t) ^ 2 < 1 + (γ₂ * t) ^ 2 := by linarith
  exact one_div_lt_one_div_of_lt hp1 hsum

/-- **谱序不变性**（探索文档 §3 与 §9.2 的公共代数根源）：`0 < γ₁ < γ₂` 时
    `λ₁^SE < λ₂^SE`——自能移动量随 γ 递减，分支谱序永不重组。
    SE-A（全分支同浴，§3）与 SE-B（n≥2 分支间零交叉，§9.2）是同一引理的两个判读：
    前者给「`λ₁ = λ₂` 无解」，后者给「分支间零交叉」。 -/
theorem selfEnergySpectrum_lt_of_lt {t Λ γ₁ γ₂ : ℝ}
    (ht : 0 < t) (hΛ : 0 < Λ) (h₁ : 0 < γ₁) (h₂ : 0 < γ₂) (hlt : γ₁ < γ₂) :
    selfEnergySpectrum γ₁ t Λ < selfEnergySpectrum γ₂ t Λ := by
  unfold selfEnergySpectrum
  have hf : (1 + (γ₂ * t) ^ 2)⁻¹ < (1 + (γ₁ * t) ^ 2)⁻¹ := by
    simpa using selfEnergy_factor_lt ht h₁ h₂ hlt
  have hΛt : 0 < Λ * t := by positivity
  have hA : Λ * t * (1 + (γ₂ * t) ^ 2)⁻¹ < Λ * t * (1 + (γ₁ * t) ^ 2)⁻¹ :=
    mul_lt_mul_of_pos_left hf hΛt
  linarith

/-- **SE-A 推论**（§3）：全分支同浴时 `λ₁ = λ₂` 无解（γ₁ ≠ γ₂ 严格保序）——
    交叉判据 `λ₁ = λ₂` 在自能侧不产生 `T_c`；这是结构性排除，不是数值差。 -/
theorem selfEnergy_noCrossing {t Λ γ₁ γ₂ : ℝ}
    (ht : 0 < t) (hΛ : 0 < Λ) (h₁ : 0 < γ₁) (h₂ : 0 < γ₂) (hne : γ₁ ≠ γ₂) :
    selfEnergySpectrum γ₁ t Λ ≠ selfEnergySpectrum γ₂ t Λ := by
  rcases lt_or_gt_of_ne hne with h | h
  · exact ne_of_lt (selfEnergySpectrum_lt_of_lt ht hΛ h₁ h₂ h)
  · exact ne_of_gt (selfEnergySpectrum_lt_of_lt ht hΛ h₂ h₁ h)

/-- **类型 II 谱方程的谱序不变性（核形状鲁棒性，探索文档 §12.1）**：谱线
    `λ_n = γ_n − A·φ(γ_n)`，`φ` 在 `(0,∞)` 上严格递减（点态形式）、`A > 0`，则
    `0 < γ₁ < γ₂ ⟹ λ₁ < λ₂`。单极核（`φ = 1/(1+u²)`）与精确高斯核
    （`φ = √(π/2)·e^(−u²/2)`）同为特例——谱序定理对核形状鲁棒。 -/
theorem spectralOrder_robust {A : ℝ} (hA : 0 < A) (φ : ℝ → ℝ)
    (hφ : ∀ x y : ℝ, 0 < x → 0 < y → x < y → φ y < φ x) {γ₁ γ₂ : ℝ}
    (h₁ : 0 < γ₁) (h₂ : 0 < γ₂) (hlt : γ₁ < γ₂) :
    γ₁ - A * φ γ₁ < γ₂ - A * φ γ₂ := by
  have hφlt : φ γ₂ < φ γ₁ := hφ γ₁ γ₂ h₁ h₂ hlt
  have h2 : A * φ γ₁ > A * φ γ₂ := mul_lt_mul_of_pos_left hφlt hA
  linarith

/-! ## 自能交叉方程的根结构（§4） -/

/-- **交叉方程根的代数验证**（§4）：二次方程 `a·τ² − L·τ + d = 0`
    （`a = Δγ·γ₂²`、`L = Λ²`、`d = Δγ`）在判别式 `L² − 4ad` 非负时，
    显式高温根 `τ⁺ = (L + √(L²−4ad))/(2a)` 满足方程——纯代入验证。
    低温根 `τ⁻ = (L − √(L²−4ad))/(2a)` 同理（证明同构，此处不重复登记）。
    探索文档 §4 的三层结构（数学存在性 / 物理可达性 / 无双根）中，
    本定理只覆盖第一层的代数部分；可达性涉及 `τ_g(T)` 值域与 tanh 反演，
    属接口层，未在此形式化。 -/
theorem selfEnergy_crossing_root_add {a L d c : ℝ}
    (ha : 0 < a) (hd : 0 < d) (hL : 0 < L)
    (hdisc : 0 ≤ L ^ 2 - 4 * a * d)
    (hc : c = Real.sqrt (L ^ 2 - 4 * a * d)) :
    a * ((L + c) / (2 * a)) ^ 2 - L * ((L + c) / (2 * a)) + d = 0 := by
  have h2a : (2 : ℝ) * a ≠ 0 := ne_of_gt (by linarith)
  have hsq : c ^ 2 = L ^ 2 - 4 * a * d := by
    rw [hc, Real.sq_sqrt hdisc]
  have hzero : a * (L + c) ^ 2 - L * (L + c) * (2 * a) + d * (2 * a) ^ 2 = 0 := by
    have expand : (L + c) ^ 2 = L ^ 2 + 2 * L * c + c ^ 2 := by ring
    rw [expand, hsq]
    ring
  have hrew : a * ((L + c) / (2 * a)) ^ 2 - L * ((L + c) / (2 * a)) + d
      = (a * (L + c) ^ 2 - L * (L + c) * (2 * a) + d * (2 * a) ^ 2) / (2 * a) ^ 2 := by
    field_simp [h2a]
  rw [hrew, hzero]
  simp

end CrossingParadigm
end CQM