import GN.Basic

/-!
# §5 Sierra-CQM 条件性渐近引理 (SierraCQM)

公理化证明稿 §5 的形式化：Floquet 量子化 → 耦级渐近的**代数核心**。

对应文档：定理 5.1（Sierra-CQM），其结论为条件性陈述——
依赖两个构造性输入：

1. sprinkling 区间长度 `L_n = 2πn/γ_n`（物理来源未从第一性原理导出）
2. 第 n 个本征值取量子数 `m = n`（构造性选择）

本文件形式化步骤 3–5 的代数（零点匹配、偏差界、耦级误差），
全部以显式假设出现在定理陈述中，故为诚实的条件定理。

核心结论（显式定量形式）：

- `k_n = γ_n (1 + θ_n/(2πn))`（零点匹配）
- `|k_n − γ_n| < γ_n/(2n)`（k_n = γ_n + O(1/n)）
- `|k_n² − γ_n²| ≤ γ_n² (1/n + 1/(4n²))`（绝对误差 O(γ_n²/n)）
- `|k_n² − γ_n²| / γ_n² ≤ 5/(4n)`（相对误差 O(1/n)，n ≥ 1，见证常数 5/4）

## 未形式化部分（如实标注）

- 步骤 1（酉等价 U Ĥ U⁻¹ = -∂² + 1/4）：函数空间上的算子计算，
  需酉变换与形式伴随的分析学基础设施，待后续
- 步骤 2（平面波广义本征函数）：分布意义谱论，待后续
- L_n 与 m = n 的物理来源：构造性假设（文档已标注）

## 参考文献

- Sierra, G. (2008). A quantum mechanical model of the Riemann zeros.
  New J. Phys. 10, 033016.（LM 色散 + Floquet 导出 L_n 的文献背景）
- LeClair, A. & Mussardo, G. (2024). JHEP 04, 062. arXiv:2307.01254.
-/

open Real

namespace CQM
namespace GN

/-! ### 构造性输入（条件性定理的显式假设） -/

/-- sprinkling 区间长度（构造性假设）：L_n = 2πn/γ_n。

    物理来源（为何区间长度与第 n 个黎曼零点成反比）尚未从
    第一性原理导出；此定义即文档 §5 步骤 4 的构造性输入。 -/
noncomputable def sprinklingLength (n : ℕ) (γ : ℝ) : ℝ :=
  2 * Real.pi * (n : ℝ) / γ

/-- Floquet 量子化动量（量子数取 m = n 的构造性选择）：

    k_n = (θ_n + 2πn) / L_n

    其中 |θ_n| < π 为有界边界相位。 -/
noncomputable def floquetMomentum (n : ℕ) (θ L : ℝ) : ℝ :=
  (θ + 2 * Real.pi * (n : ℝ)) / L

/-- 耦级（谱算符 -∂² + 1/4 的本征值形式）：c = k² + 1/4。 -/
noncomputable def couplingLevel (k : ℝ) : ℝ :=
  k ^ 2 + 1 / 4

/-! ### 步骤 3–4：零点匹配 -/

/-- [步骤 4 代数] 零点匹配：给定 L_n = 2πn/γ_n（γ ≠ 0，n ≠ 0），

    k_n = γ_n · (1 + θ_n / (2πn))

    这是把 L_n 的构造直接代入 Floquet 量子化条件 k = (θ+2πn)/L 的结果。 -/
theorem floquetMomentum_eq (n : ℕ) (θ γ : ℝ) (hγ : γ ≠ 0) (hn : (n : ℝ) ≠ 0) :
    floquetMomentum n θ (sprinklingLength n γ)
      = γ * (1 + θ / (2 * Real.pi * (n : ℝ))) := by
  unfold floquetMomentum sprinklingLength
  have hpn : 2 * Real.pi * (n : ℝ) ≠ 0 :=
    mul_ne_zero (mul_ne_zero (by norm_num) Real.pi_pos.ne') hn
  field_simp [hγ, hpn]
  ring

/-- [步骤 4 偏差界] |k_n − γ_n| < γ_n / (2n)。

    由 k_n = γ_n(1 + θ_n/(2πn)) 得 k_n − γ_n = γ_n·θ_n/(2πn)，
    且 |θ_n| < π、γ_n > 0、n > 0，故

    |k_n − γ_n| = γ_n·|θ_n|/(2πn) < γ_n·π/(2πn) = γ_n/(2n)。

    这是 k_n = γ_n + O(1/n) 的显式定量形式。 -/
theorem floquetMomentum_deviation_lt (n : ℕ) (θ γ : ℝ)
    (hθ : |θ| < Real.pi) (hγ : 0 < γ) (hn : 0 < (n : ℝ)) :
    |γ * (1 + θ / (2 * Real.pi * (n : ℝ))) - γ| < γ / (2 * (n : ℝ)) := by
  have h1 : γ * (1 + θ / (2 * Real.pi * (n : ℝ))) - γ
      = γ * θ / (2 * Real.pi * (n : ℝ)) := by ring
  rw [h1]
  have hpos : 0 < 2 * Real.pi * (n : ℝ) :=
    mul_pos (mul_pos (by norm_num) Real.pi_pos) hn
  calc
    |γ * θ / (2 * Real.pi * (n : ℝ))|
        = γ * |θ| / (2 * Real.pi * (n : ℝ)) := by
          rw [abs_div, abs_mul, abs_of_pos hγ, abs_of_pos hpos]
    _ < γ * Real.pi / (2 * Real.pi * (n : ℝ)) :=
          div_lt_div_of_pos_right (mul_lt_mul_of_pos_left hθ hγ) hpos
    _ = γ / (2 * (n : ℝ)) := by
          field_simp [Real.pi_pos.ne', ne_of_gt hn]

/-! ### 步骤 5：耦级误差 -/

/-- [步骤 5] 耦级的绝对误差界（O(γ_n²/n) 的显式形式）：

    |k_n² − γ_n²| ≤ γ_n² · (1/n + 1/(4n²))

    其中 k_n = γ_n(1 + θ_n/(2πn))，|θ_n| < π，γ_n > 0，n > 0。

    证明：|k² − γ²| = |k−γ|·|k+γ|，第一步用
    `floquetMomentum_deviation_lt`，第二步用三角不等式与 |θ| 界。 -/
theorem floquet_level_deviation_le (n : ℕ) (θ γ : ℝ)
    (hθ : |θ| < Real.pi) (hγ : 0 < γ) (hn : 0 < (n : ℝ)) :
    |(γ * (1 + θ / (2 * Real.pi * (n : ℝ)))) ^ 2 - γ ^ 2|
      ≤ γ ^ 2 * (1 / (n : ℝ) + 1 / (4 * (n : ℝ) ^ 2)) := by
  set k := γ * (1 + θ / (2 * Real.pi * (n : ℝ))) with hk
  have hfactor : k ^ 2 - γ ^ 2 = (k - γ) * (k + γ) := by ring
  rw [hfactor, abs_mul]
  -- 第一步：|k - γ| < γ/(2n)
  have hdev : |k - γ| < γ / (2 * (n : ℝ)) := by
    rw [hk]
    exact floquetMomentum_deviation_lt n θ γ hθ hγ hn
  -- 第二步：|k + γ| ≤ γ·(2 + 1/(2n))
  have hθle : |θ| / (2 * Real.pi * (n : ℝ)) ≤ 1 / (2 * (n : ℝ)) := by
    have hnum : |θ| ≤ Real.pi := le_of_lt hθ
    have hden_pos : 0 < 2 * Real.pi * (n : ℝ) :=
      mul_pos (mul_pos (by norm_num) Real.pi_pos) hn
    calc
          |θ| / (2 * Real.pi * (n : ℝ))
          ≤ Real.pi / (2 * Real.pi * (n : ℝ)) :=
            div_le_div_of_nonneg_right hnum (le_of_lt hden_pos)
      _ = 1 / (2 * (n : ℝ)) := by
            field_simp [Real.pi_pos.ne', ne_of_gt hn]
  have hkabs : |k| ≤ γ * (1 + 1 / (2 * (n : ℝ))) := by
    rw [hk, abs_mul, abs_of_pos hγ]
    have hmul : |1 + θ / (2 * Real.pi * (n : ℝ))| ≤ 1 + 1 / (2 * (n : ℝ)) := by
      calc
        |1 + θ / (2 * Real.pi * (n : ℝ))|
            ≤ |1| + |θ / (2 * Real.pi * (n : ℝ))| := abs_add_le ..
        _ = 1 + |θ| / (2 * Real.pi * (n : ℝ)) := by
              rw [abs_one, abs_div]
              rw [abs_of_pos (mul_pos (mul_pos (by norm_num) Real.pi_pos) hn)]
        _ ≤ 1 + 1 / (2 * (n : ℝ)) := add_le_add le_rfl hθle
    exact mul_le_mul_of_nonneg_left hmul (le_of_lt hγ)
  have hsum : |k + γ| ≤ γ * (2 + 1 / (2 * (n : ℝ))) := by
    calc
      |k + γ| ≤ |k| + |γ| := abs_add_le ..
      _ ≤ γ * (1 + 1 / (2 * (n : ℝ))) + γ := by
            rw [abs_of_pos hγ]
            exact add_le_add hkabs le_rfl
      _ = γ * (2 + 1 / (2 * (n : ℝ))) := by ring
  -- 合并：|k−γ|·|k+γ| < γ/(2n) · γ·(2+1/(2n)) = γ²(1/n + 1/(4n²))
  have hpos2 : 0 < γ * (2 + 1 / (2 * (n : ℝ))) := by
    have h2 : 0 < 1 / (2 * (n : ℝ)) := one_div_pos.mpr (mul_pos (by norm_num) hn)
    refine mul_pos hγ ?_
    linarith
  have hfinal : γ / (2 * (n : ℝ)) * (γ * (2 + 1 / (2 * (n : ℝ))))
      = γ ^ 2 * (1 / (n : ℝ) + 1 / (4 * (n : ℝ) ^ 2)) := by
    ring
  have hlt : |k - γ| * |k + γ|
      < γ ^ 2 * (1 / (n : ℝ) + 1 / (4 * (n : ℝ) ^ 2)) := by
    calc
      |k - γ| * |k + γ|
          ≤ |k - γ| * (γ * (2 + 1 / (2 * (n : ℝ)))) :=
            mul_le_mul_of_nonneg_left hsum (abs_nonneg (k - γ))
      _ < γ / (2 * (n : ℝ)) * (γ * (2 + 1 / (2 * (n : ℝ)))) :=
            mul_lt_mul_of_pos_right hdev hpos2
      _ = γ ^ 2 * (1 / (n : ℝ) + 1 / (4 * (n : ℝ) ^ 2)) := hfinal
  exact le_of_lt hlt

/-- [步骤 5] 耦级形式的绝对误差（带 1/4 平移）：

    |c(k_n) − (γ_n² + 1/4)| ≤ γ_n² · (1/n + 1/(4n²))，
    其中 c(k) = k² + 1/4。 -/
theorem couplingLevel_deviation_le (n : ℕ) (θ γ : ℝ)
    (hθ : |θ| < Real.pi) (hγ : 0 < γ) (hn : 0 < (n : ℝ)) :
    |couplingLevel (γ * (1 + θ / (2 * Real.pi * (n : ℝ)))) - (γ ^ 2 + 1 / 4)|
      ≤ γ ^ 2 * (1 / (n : ℝ) + 1 / (4 * (n : ℝ) ^ 2)) := by
  unfold couplingLevel
  have hsh :
      (γ * (1 + θ / (2 * Real.pi * (n : ℝ)))) ^ 2 + 1 / 4 - (γ ^ 2 + 1 / 4)
        = (γ * (1 + θ / (2 * Real.pi * (n : ℝ)))) ^ 2 - γ ^ 2 := by ring
  rw [hsh]
  exact floquet_level_deviation_le n θ γ hθ hγ hn

/-- [步骤 5 相对误差] 二阶矩的相对误差 O(1/n) 的显式形式：

    |k_n² − γ_n²| / γ_n² ≤ 1/n + 1/(4n²)

    即文档定理 5.1 的相对误差表述
    |c_n − (1/4 + γ_n²)| / γ_n² = O(1/n) 的定量版本。 -/
theorem floquet_relative_error_le (n : ℕ) (θ γ : ℝ)
    (hθ : |θ| < Real.pi) (hγ : 0 < γ) (hn : 0 < (n : ℝ)) :
    |(γ * (1 + θ / (2 * Real.pi * (n : ℝ)))) ^ 2 - γ ^ 2| / γ ^ 2
      ≤ 1 / (n : ℝ) + 1 / (4 * (n : ℝ) ^ 2) := by
  have h := floquet_level_deviation_le n θ γ hθ hγ hn
  have hγ2 : 0 < γ ^ 2 := pow_pos hγ 2
  have hdiv :
      |(γ * (1 + θ / (2 * Real.pi * (n : ℝ)))) ^ 2 - γ ^ 2| / γ ^ 2
        ≤ (γ ^ 2 * (1 / (n : ℝ) + 1 / (4 * (n : ℝ) ^ 2))) / γ ^ 2 :=
    div_le_div_of_nonneg_right h (le_of_lt hγ2)
  rw [mul_div_cancel_left₀ _ hγ2.ne'] at hdiv
  exact hdiv

/-- [步骤 5 相对误差，n ≥ 1] 更整齐的 O(1/n) 常数形式：

    |k_n² − γ_n²| / γ_n² ≤ 5/(4n)   （n ≥ 1）

    由 1/n² ≤ 1/n（n ≥ 1）与 1 + 1/4 = 5/4。这给出文档中
    相对误差 O(1/n) 的显式见证常数 C = 5/4。 -/
theorem floquet_relative_error_le_five_quarters (n : ℕ) (θ γ : ℝ)
    (hθ : |θ| < Real.pi) (hγ : 0 < γ) (hn : 1 ≤ n) :
    |(γ * (1 + θ / (2 * Real.pi * (n : ℝ)))) ^ 2 - γ ^ 2| / γ ^ 2
      ≤ 5 / (4 * (n : ℝ)) := by
  have h11 : (1 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  have hn0 : 0 < (n : ℝ) := by linarith
  have h := floquet_relative_error_le n θ γ hθ hγ hn0
  have hmain : 1 / (n : ℝ) + 1 / (4 * (n : ℝ) ^ 2) ≤ 5 / (4 * (n : ℝ)) := by
    have hc : (0 : ℝ) < 4 * (n : ℝ) ^ 2 :=
      mul_pos (by norm_num) (pow_pos hn0 2)
    have key : (1 / (n : ℝ) + 1 / (4 * (n : ℝ) ^ 2)) * (4 * (n : ℝ) ^ 2)
        = 4 * (n : ℝ) + 1 := by
      field_simp [hn0.ne']
    have key2 : (5 / (4 * (n : ℝ))) * (4 * (n : ℝ) ^ 2) = 5 * (n : ℝ) := by
      field_simp [hn0.ne']
    have hprod : (1 / (n : ℝ) + 1 / (4 * (n : ℝ) ^ 2)) * (4 * (n : ℝ) ^ 2)
        ≤ (5 / (4 * (n : ℝ))) * (4 * (n : ℝ) ^ 2) := by
      rw [key, key2]
      linarith
    exact le_of_mul_le_mul_right hprod hc
  exact le_trans h hmain

end GN
end CQM
