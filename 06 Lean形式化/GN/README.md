# GN — $G_N$ 第一性推导形式化库

对应研究文档：`04 前沿研究/CQM_前沿研究_GN第一性推导_公理化证明稿.md`

本库形式化证明稿中**第一部分（数学事实层）**的可形式化子集，从
`SpectralGeometry.Basic` 复用相变量子 `spectralQuantum`（☯）的解析定义
与数值桥梁公理，不依赖当前编译失败的 `SpectralGeometry.RiemannXi` /
`SpectralGeometry.Mathieu`。

## 编译状态

✅ `lake build GN` 通过（Lean 4.29.1，零 `sorry`、零新增 `axiom`；CQM 代码零警告）。

## 模块

| 模块 | 内容 | 定理数 |
|:---|:---|:---:|
| `GN/Basic.lean` | 公共导入、缺口与文献标注 | 0 |
| `GN/TripleIdentity.lean` | §1 三重恒等的代数层 | 13 |
| `GN/SierraCQM.lean` | §5 Sierra-CQM 条件性渐近（Floquet 量子化 → 零点匹配 → 耦级误差） | 6 |
| `GN/SimplexSpectrum.lean` | §2 4-单纯形组合谱（10×10 边-面关联矩阵、特征多项式、本征空间直和分解） | 57 |
| `GN/AdeleJacobian.lean` | §6 Adele Jacobian 因子 2（条件定理，Tate 自对偶） | 11 |
| `GN/Constructions.lean` | §8–§11 可代数化构造（κ 组合-谱、G_N 乘积核正性与对数形式） | 14 |

**合计：101 定理/引理，零 `sorry`、零新增 `axiom`。**

## 核心定理（§1 三重恒等）

| 定理 | Lean 名 | 对应文档 | 证明方式 |
|:---|:---|:---|:---|
| ☯ 闭式等价变形 | `spectralQuantum_closedForm` | 定理 1.2 | log 乘法公式 + log 4 = 2 log 2 |
| λ₁ = ☯ | `liCoeffOne_eq_spectralQuantum` | 定理 1.3 | 定义展开 + `ring` |
| B = -☯ | `leclairConstant_eq_neg_spectralQuantum` | 定理 1.4 | 定理 1.2 + `ring` |
| 三重恒等（代数层） | `spectralQuantum_triple_identity` | 定理 1.5 | 上三者复合 |
| λ₁ > 0（Li 判据 n=1） | `liCoeffOne_pos` | 推论 | λ₁ = ☯ > 0 |
| B < 0 | `leclairConstant_neg` | 推论 | B = -☯ < 0 |
| λ₁ = -B | `liCoeffOne_eq_neg_leclairConstant` | 定理 1.5 推论 | 复合 |
| λ₁ 数值桥梁 | `liCoeffOne_numerical_bounds` | — | 继承 ☯ 区间公理 |
| B 紧凑形式 = 展开形式 | `leclairConstantCompact_eq` | 定义 1.5 | log(2√π) 展开 |

定义（按文献闭式，定义展开即证明）：

- `liCoeffOne`：第一 Li 系数 λ₁ = 1 − log(4π)/2 + γ_E/2（Voros 2016）
- `leclairConstant` / `leclairConstantCompact`：LeClair 常数 B = −γ_E/2 − 1 + log 2 + log π/2 = −γ_E/2 − 1 + log(2√π)（arXiv:2406.01828）

## 核心定理（§5 Sierra-CQM 条件性渐近）

对应文档定理 5.1；全部假设显式（sprinkling 区间 `L_n = 2πn/γ_n`、量子数 `m = n`、`|θ_n| < π`、`γ_n > 0`、`n > 0`），故为诚实的条件定理。

| 定理 | Lean 名 | 结论 | 证明方式 |
|:---|:---|:---|:---|
| 零点匹配 | `floquetMomentum_eq` | `k_n = γ_n(1 + θ_n/(2πn))` | 代入 `L_n` + `field_simp` |
| 偏差界 | `floquetMomentum_deviation_lt` | `|k_n − γ_n| < γ_n/(2n)` | `abs_div` + `div_lt_div_of_pos_right` |
| 耦级绝对误差 | `floquet_level_deviation_le` | `|k_n² − γ_n²| ≤ γ_n²(1/n + 1/(4n²))` | 平方差 + 三角不等式 + 乘性合并 |
| 耦级形式误差 | `couplingLevel_deviation_le` | `|c(k_n) − (γ_n²+1/4)| ≤ γ_n²(1/n + 1/(4n²))` | 复合上条 |
| 相对误差 | `floquet_relative_error_le` | `|k_n² − γ_n²|/γ_n² ≤ 1/n + 1/(4n²)` | `div_le_div_of_nonneg_right` |
| 相对误差（n≥1） | `floquet_relative_error_le_five_quarters` | `… ≤ 5/(4n)`（见证常数 5/4） | `1/n² ≤ 1/n` + `field_simp` |

未形式化（如实标注）：步骤 1 酉等价（函数空间算子计算）、步骤 2 平面波广义本征函数（分布谱论）、`L_n` 与 `m = n` 的物理来源（构造性假设）。

## 已知缺口（如实标注）

| 缺口 | 描述 | 状态 |
|:---|:---|:---|
| 定理 1.1 | ☯ 的零点求和表示 ☯ = Σ 1/(γ_n²+1/4)，需 ξ 的 Hadamard 乘积 | 依赖 `SpectralGeometry.RiemannXi`（当前编译失败），待该模块修复 |
| 定理 1.3 解析侧 | 生成函数 λ_n 链路到 ξ'(1)/ξ(1) 的解析推导 | 同上；本库形式化其闭式代数层 |
| §5 步骤 1–2 | 酉等价 U Ĥ U⁻¹ = −∂² + 1/4 与平面波广义本征函数 | 分析学基础设施（酉变换、分布谱论），待后续 |
| §5 物理来源 | `L_n = 2πn/γ_n` 与 `m = n` 的第一性推导 | 构造性假设（文档已标注）；代数核心已在 `SierraCQM.lean` |
| ☯ = ξ'(1)/ξ(1) 本体 | A2.2 的解析推导 | 由 `SpectralGeometry.RiemannXi` 承接（修复前，定义与文档在 `SpectralGeometry.Basic`） |
| §6 Tate 自对偶 | `det(D_∞) · ∏_p det(D_p) = 1` 的严格证明 | 数学事实（Tate 1950）+ CQM 构造叠加；库内以 `tateSelfDual_placeholder` 标注，条件定理已证 |
| §6 构造 10.1 | `ln(∏ det D_p) = 1/☯` 的启发式对应 | 启发式；库内仅给出其条件推论 `𝒥 = exp(−2/☯)` |
| §9 构造 9.1 | `𝔠₁ = 1/4 + γ₁²` 的 n=1 精确等同 | 超出 Sierra-CQM 渐近定理范围；以 `firstCouplingExact : Prop` 记录，数值旁证 < 10⁻⁸ |
| §10 构造 10.1 | p-进谱行列式 `det(D_p)` 的存在性 | CQM 构造，非标准数学对象 |
| §11 开放问题 11.1 | `G_N` 乘积结构的变分原理 | 未解决；库内仅证各因子正性与对数形式 |

## 严格性边界

本库形式化的是**闭式层面的代数恒等**。三重恒等中的 ξ'(1)/ξ(1) 一侧由
`SpectralGeometry.Basic` 中 `spectralQuantum` 的定义（A2.2）承接；
生成函数 → 闭式的解析链路、Hadamard 乘积求和表示依赖
`SpectralGeometry.RiemannXi`，在该模块编译修复前不在此声明。

## 编译命令

```bash
cd "06 Lean形式化"
lake build GN # 编译整个 GN 库
lake build GN.TripleIdentity # 编译单模块
lake build GN.SierraCQM # 编译单模块
lake build GN.SimplexSpectrum # §2 组合谱
lake build GN.AdeleJacobian # §6 Adele Jacobian
lake build GN.Constructions # §8–§11 构造
```

## 参考文献

1. Titchmarsh, E. C. (1986). *The Theory of the Riemann Zeta-Function*, 2nd ed.
2. Voros, A. (2016). Simplifications of the Keiper/Li approach to the Riemann Hypothesis. arXiv:1602.03292.
3. LeClair, A. (2024). Spectral Flow for the Riemann zeros. arXiv:2406.01828.
4. LeClair, A. & Mussardo, G. (2024). Riemann zeros as quantized energies of scattering with impurities. *JHEP* 04, 062. arXiv:2307.01254.
5. Coffey, M. W. (2008). Relations and representations of the Euler constant. *Proc. R. Soc. A* 464, 2059–2074.
6. Sierra, G. (2008). A quantum mechanical model of the Riemann zeros. *New J. Phys.* 10, 033016. arXiv:0712.0705.
7. Sierra, G. (2014). The Riemann zeros as energy levels of a Dirac fermion in a potential built from the prime numbers in Rindler spacetime. *J. Phys. A* 47, 325204. arXiv:1404.4252.
8. Sierra, G. (2019). The Riemann Zeros as Spectrum and the Riemann Hypothesis. *Symmetry* 11(4), 494. arXiv:1601.01797.
9. Tate, J. T. (1950). Fourier analysis in number fields and Hecke's zeta-functions. In *Algebraic Number Theory* (Proc. Sympos.), 305–347; reprinted 1967.
10. Milne, J. S. The Work of John Tate. https://www.jmilne.org/math/xnotes/Tate.pdf
11. Brinkmann, P. & Ziegler, G. M. Small f-vectors of 3-spheres and of 4-polytopes. *Math. Comp.* (2017). arXiv:math/0208073（4-单纯形 f-向量 (5,10,10,5) 标准参考）。
12. OEIS A135278（n-单纯形 m-面数 = C(n+1,m+1)）。
