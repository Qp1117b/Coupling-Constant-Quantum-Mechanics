# CQMFormal — CQM 的 Lean 4 形式化验证

本目录包含**耦合常数量子力学（CQM）**的 Lean 4 形式化验证项目。

## 编译状态

✅ **全部 9 个库编译通过**（3313 jobs） | Lean 4.29.1 | **零 CQM 警告**

> 注：构建过程中 8 条 Mathlib 内部 ProofWidgets 模块重复注册警告来自 Mathlib 4.29.1 上游，
> 非 CQM 代码问题，无法从本项目消除。`lake build` 完全成功。 -/

## 库结构

| 库 | 文件 | 关键类型/定理 |
|:---|:---|:---|
| **CausalSet** | `Basic.lean`, `Reproduction.lean`, `Sprinkling.lean`, `Axioms.lean` | `CausalSet`、`ReproductionOperator`、`asymm`、`sprinklingDensity` |
| **CouplingSpace** | `Basic.lean`, `Uncertainty.lean` | `couplingStrength`、`CanonicalCommutation`、`robertson_ccr_inequality` |
| **CartanAlgebra** | `Basic.lean` | `cartanA4`、本征值精确表达式、`dynkinIndex`、`simplexEulerChar` |
| **SpectralGeometry** | `Basic.lean`, `Mathieu.lean`, `RiemannXi.lean` | `spectralQuantum`、`mathieuParameter`、`goldenRatio`、`adeleCycle`、Sierra-CQM 耦谱、黎曼 ξ 函数 |
| **PrimeGeometry** | `Basic.lean`, `Compton.lean`, `Generation.lean`, `Particle.lean`, `Spin.lean`, `WindingDensity.lean` | 因果时几何：多边形/弧段/位置结构、粒子谱、自旋、康普顿、代际、绕数密度 |
| **Decoherence** | `Basic.lean` | `confinementScale`、`CausalLayer`、三层结构 |
| **PhysicalConstants** | `Basic.lean` | `GN_spectral_formula`、`alpha_inverse_SU5`、CODATA 偏差 |
| **Methodology** | `Basic.lean` | 涌现公式结构性表达、庸俗隐变量分解对比（公理为主） |
| **Superconductivity** | `Ontology.lean`, `Gravity.lean`, `Mechanism.lean`, `Integral.lean`, `TransitionTemperature.lean`, `StrongGravity.lean`, `Reduction.lean`, `CartanSuperconductivity.lean`, `FirstPrinciples.lean`, `SPAF.lean`, `SPAF_PT.lean`, `SPAF_PTH.lean`, `BCSIntegralAsymptotic.lean`, `BridgeTheorems.lean`, `ElementCartan.lean`, `MolecularGeometry.lean` | 强引力超导（16 模块）：有限本体论、τ_res/ω_causal、三方因果闭环、涌现积分、T_c、T_grav、**BCS 退化与还原（§11 温度依赖）**、**嘉当张量超导方程（§9 库珀对跃迁）**、**第一性推导链**、**SPAF 半唯像框架**、**BCS 渐近分析（G13 闭合）**、**桥接定理**、**元素嘉当矩阵**、**分子几何→晶胞嘉当矩阵（链B约束）→Regge晶胞/角亏（链A生成）→FG退相干场** |

## 形式化推导链

```
Axioms
├── A0.1-3: 因果集 + 再生产算子
│   ├── 因果偏序非对称性 (asymm)
│   ├── Alexandrov 区间有限性 (interval_finite)
│   ├── 再生产幂等性 (muHat_idempotent)
│   └── Sprinkling → 耦合空间 (u, τ)
│       ├── Sprinkling 密度 ρ(u) = exp(u)
│       ├── 耦合速度 c = 1/ρ
│       └── 保序嵌入 (sprinkling_preserves_order)
│
├── A1.1: 正则对易关系 [û, p̂_u] = i
│   ├── 耦合强度 r = exp(u) > 0
│   ├── 耦合坐标 u = ln r
│   ├── 不确定性关系 Δr/⟨r⟩ · Δv_τ ≥ C/2 (Robertson 不等式)
│   └── 14 个辅助定理（中心化算子、方差、Hermitian 性等）
│
├── H3.3 + A2.1: 退相干稳态 = 正四单纯形 → A₄ 嘉当矩阵
│   ├── 对称性: A₄_{ij} = A₄_{ji}
│   ├── 迹 = 8, 行列式 = 5
│   ├── Aₙ 行列式 = n+1 (A₁:2, A₂:3, A₃:4, A₄:5)
│   ├── 本征值精确表达式:
│   │   λ₁ = (3-√5)/2, λ₂ = (5-√5)/2
│   │   λ₃ = (3+√5)/2, λ₄ = (5+√5)/2
│   ├── 本征值之和 = 8, 之积 = 5
│   ├── 逆嘉当矩阵 A₄⁻¹ 显式条目
│   ├── 正定性: 所有主子式 > 0
│   ├── 4-单纯形 f-向量回文性 (5,10,10,5)
│   ├── SU(5) Weyl 群 = S₅ = 4-单纯形对称群
│   └── Dynkin 指数 I = 5/3
│
├── A2.2: 谱量子 C = ξ'(1)/ξ(1)
│   ├── Mathieu 参数 q = φ/2（黄金比例一半，从 A₄ 本征值严格导出）
│   │   ├── φ = (1+√5)/2, φ² = φ + 1
│   │   ├── q = (λ₄-λ₁)/(λ₄+λ₁) = φ/2 ≈ 0.809
│   │   └── λ₄/λ₁ = 5+2√5 ≈ 9.472
│   ├── Mathieu 临界值 λ_c（系统在稳定区: q < λ_c）
│   ├── 第一耦级 𝔠₁ (Sierra-CQM: 𝔠_n = 1/4 + γ_n²)
│   ├── Adele 周期 N_cycle = 30
│   ├── 4-单纯形 f-向量和 = 30 = N_cycle
│   ├── 谱修正因子 κ = (31+C)/30
│   ├── G_N 因子 F(C) = C²·𝔠₁·exp(-2/C)·(1+κC)
│   ├── F(C) 严格为正
│   └── 谱常数网络: C·λ_c·𝔠₁ ∈ (6, 10)
│
├── 素数结构
│   ├── 活跃素数 {2, 3, 5}：Φ(k) > 0 的唯一素数
│   ├── 素数冻结定理：∀ k > 5, Φ(k) = 0 (axiom)
│   ├── N_cycle = 2·3·5 = 30 = 活跃素数积
│   └── 活跃素数个数 3 = rank(SU(5)) - 1
│
├── 退相干三层结构 L1/L2/L3
│   ├── 禁闭标度 L = 1
│   ├── 退相干条件 ρ(u) ≥ L
│   └── 退相干速率 Γ(u) = ρ(u)
│
└── m_p（实验输入）
    └── G_N = I·λ_c·C²·𝔠₁·exp(-2/C)·(1+κC) / m_p²
        ├── G_N > 0（严格正性）
        ├── G_N 因子分解
        ├── 层级因子 exp(-2/C) ≈ 10⁻³⁸
        ├── CODATA 偏差 < 10 ppm
        └── α⁻¹_SU(5) = 16384π/375 ≈ 137.27
            ├── 137 < α⁻¹_SU(5) < 138
            ├── 群论因子 = 2^14/(3×5^3) = 16384/375
            ├── α_SU(5) > 0
            └── 0.007 < α_SU(5) < 0.01
```

## 定理统计

| 库 | 已证明定理 | 公理/待证 |
|:---|:---:|:---:|
| CausalSet | 22 | 4 |
| CouplingSpace | 21 | 0 |
| CartanAlgebra | 30 | 0 |
| SpectralGeometry | 114 | 4 |
| PrimeGeometry | 79 | 4 |
| Decoherence | 15 | 2 |
| PhysicalConstants | 20 | 0 |
| Methodology | 6 | 11 |
| Superconductivity | 340 | 5 |
| **总计** | **647** | **30** |

## 已知缺口

| 缺口 | 描述 | 涉及库 | 状态 |
|:---|:---|:---|:---:|
| G5 | 退相干 = 禁闭的严格推导 | `CausalSet/Axioms` | `axiom` (H3.1) |
| G5 | 非交换 → 交换几何相变 | `CausalSet/Axioms` | `axiom` (H3.2) |
| A | 退相干稳态 = 正四单纯形 | `CausalSet/Axioms` | `axiom` (H3.3) |
| — | Sierra-CQM 耦谱定理严格证明 | `SpectralGeometry` | 数值验证 (偏差 < 1e-8) |
| — | Mathieu 第一特征值 b₁(q) | `SpectralGeometry` | `axiom` (待 Mathieu 函数理论) |
| — | 素数冻结定理严格证明 | `SpectralGeometry` | 数值验证 (100% 成功率) |
| — | Adele 约束 ∏_p ℤ_p = 1/30（有限乘积形式） | `SpectralGeometry` | 已证明 (`native_decide`) |
| — | 谱量子 C = ξ'(1)/ξ(1) 的闭式表达式 | `SpectralGeometry` | 已严格证明 |
| — | 因果分辨率 → 引力场有效描述的尺度依赖 | `ElementCartan` | `def` 占位（哲学立场） |
| — | 中子星/强引力例外（理想块对角失效、牛顿退化失效） | `ElementCartan` | `def` 占位（需核物理/量子引力） |

### 已闭合缺口 (v0.5.8)

| 缺口 | 描述 | 闭合方式 |
|:---|:---|:---|
| G13 | BCS 积分方程 tanh→对数渐近 | `BCSIntegralAsymptotic.lean`：`bcsTcFromIntegral_solved` 严格证明 T_c = (2e^γ/π)·ω_D·exp(−1/λ) 是积分方程的唯一正解 |
| G20-ext | 两质子耦合精确阈值 | `MolecularGeometry.lean`：`twoProtonCoupling_exactThreshold` 用 SOS 分解 + 黄金比例恒等式证明 t < λ₁ 时正定 |
| — | `bcsConstant_gt_one`（2e^γ/π > 1） | 从 `axiom` 升级为 `theorem`：利用 Mathlib 的 γ>1/2、exp(1)>2.718、π<3.1416 严格证明 |
| — | 分子超嘉当矩阵谱间隙界 | `BridgeTheorems.lean`：`twoAtomSuperCartan_quadratic_lowerBound` 用 Cauchy-Schwarz + AM-GM 严格证明 |
| — | 元素嘉当矩阵 5 个 `True` 占位公理 | 转为诚实 `def ... : Prop := True` 声明，明确标注"不构成证明" |

## 编译命令

```bash
cd "06 Lean形式化"
lake build                    # 编译全部
lake build CausalSet          # 编译单个库
lake build CartanAlgebra      # 编译嘉当代数库
lake build SpectralGeometry   # 编译谱几何库（含 Mathieu）
lake build Superconductivity  # 编译强引力超导库（10 模块）
lake build Superconductivity.SPAF  # 编译 SPAF 半唯像框架模块
```

## 理论对应

| CQM 理论 | Lean 库 | 核心定理数 |
|:---|:---|:---:|
| 因果集本体论 | `CausalSet` | 22 |
| 耦合空间与不确定性 | `CouplingSpace` | 21 |
| SU(5) 嘉当矩阵 | `CartanAlgebra` | 30 |
| 谱几何与 Mathieu 方程 | `SpectralGeometry` | 114 |
| 因果时几何 | `PrimeGeometry` | 81 |
| 禁闭-退相干等价 | `Decoherence` | 15 |
| G_N 谱公式与 α⁻¹ | `PhysicalConstants` | 20 |
| 方法论基础 | `Methodology` | 6 |
| 强引力超导涌现 | `Superconductivity` | 340 |

## 本次更新亮点 (v0.6.0)

- **去除落后形式化**：删除 `MultiComponent.lean`（其引用的 §16 非平庸 GL 自由能理论与旧 §10.3 多分量凝聚已在文档中删除/改写，与最新研究文档不一致）；同步更新主入口 `Superconductivity.lean` 的章节映射（§13→§20、§7/§10 标注"对应文档章节已精简"）、§3.6 公式由落后的 `v_τ=c₀(1+βδ)` 改为与代码一致的 `v_τ=√(1-βδ)`、G13 标注已闭合、G17 标注已删除；清理 `Reduction.lean`/`CartanSuperconductivity.lean` 模块头对已删除文档名的引用（改为"方向锚定保留"中性表述）。模块数从 17 → 16
- **定理总数**：647（Superconductivity 库 340；`MultiComponent` 的 23 定理随模块删除而移除，其对应的 GL 物理内容已在文档层面弃用）

## 本次更新亮点 (v0.5.9)

- **RQM 唯物化文档化**：将关系量子力学的唯物化操作正式纳入 SPAF 框架文档（§0）。三条原则：属性随附本体、因果自组织、观察者相对性的自然消解。推论：电子去特权化——取消电子的本体特权，使嘉当矩阵拼接理论得以统一处理超导问题，与 BCS 历史实践（晶格是关键）一致
- **六层探索架构**：SPAF 半唯像框架路径从四阶段扩展为六层架构——层级 I（质子/中子嘉当矩阵）→ 层级 II（元素嘉当矩阵，理想积木）→ 层级 III（单元素 BCS 退化）→ 层级 IV（分子超嘉当矩阵→Weyl 嵌入）→ 层级 V（宏观 Regge 亏角→FG 退相干场强度）→ 层级 VI（因果分辨率）
- **元素主次结构**：BCS 同位素效应揭示元素内部存在主次结构——质子扇区（纯 A4 块对角）为主、中子扇区（缺陷 A4 块对角）为次。主次结构直接指向 BCS 退化方向（往单元素材料退化），并揭示拼接规则（同种元素同位素之间 $\epsilon(N)$ 连续变化，跨元素种类需要 $t_{ij}$ 参数）
- **阶段 0：元素层级**：新增计算管线步骤 0a–0d（质子/中子分配→元素嘉当矩阵组装→主次结构识别→BCS 退化验证），使元素层级计算先于分子层级
- **新增缺口 11–15**：次结构谱间隙闭式、主次结构谱间隙差→同位素效应映射、因果分辨率形式化、~~牛顿引力退化定理~~（G17已删除：FG不走Regge→GR连续极限）、单元素拼接规则特殊性
- **文档总数**：SPAF 框架文档从 355 行扩展至约 500 行，新增 §0、§2.5、§5 阶段 0、§10.5 共四个章节
- **定理总数**：保持不变（624），本次更新为文档架构与概念框架的深化，非 Lean 代码层变更

## 本次更新亮点 (v0.5.8)

- **BCS 渐近分析（G13 闭合）**：新增 `BCSIntegralAsymptotic.lean`（9 定理），将 BCS 积分方程从第一性推导为对数方程。`bcsTcFromIntegral_solved` 严格证明 T_c = (2e^γ/π)·ω_D·exp(−1/λ) 是积分方程的唯一正解；`bcsTcFromIntegral_exists_unique` 证明存在唯一性。积分方程 ⟺ 对数方程 ⟺ 闭式 T_c 的完整推导链全部严格化
- **`bcsConstant_gt_one` 公理→定理**：`2e^γ/π > 1` 从 `axiom` 升级为 `theorem`。证明链：γ > 1/2（Mathlib `one_half_lt_eulerMascheroniConstant`）→ exp(γ) > exp(1/2) → 平方差因式分解证明 2·exp(1/2) > π（利用 π < 3.1416 和 exp(1) > 2.718）→ 2·exp(γ)/π > 1。BCS 理论中前因子 > 1 的"数值事实"首次从 Mathlib 已知数值界严格证明
- **桥接定理（跨模块因果链）**：新增 `BridgeTheorems.lean`（23 定理），将 CQM 各模块严格连接：`spectralGap_bcsTc_bound`（A₄ 谱间隙→BCS T_c 上限）、`gapChannelTc_exact`（谱间隙通道 T_c 闭式）、`spectralGap_to_ricciScalar_chain`（谱间隙→亏角密度→Ricci 标量）、`twoAtomSuperCartan_quadratic_lowerBound`（双原子耦合正定性）——用 Cauchy-Schwarz + AM-GM 严格证明 |t| < λ_min 时分子超嘉当矩阵正定
- **元素嘉当矩阵（质/中子层级）**：新增 `ElementCartan.lean`（39 定理），从质子/中子基本嘉当矩阵出发，按 Z/N 组装元素嘉当矩阵。包含：质子扇区（纯 A₄ 块对角）、中子扇区（缺陷 A₄，参数 ε(N)）、同位素效应（ε(N) = ε₀·(1+β·(N−N_ref)/N_ref)）、**单元素材料 CQM→BCS 退化**（§9：ε→0 时 T_c→bcsCriticalTemperature(ω_D, λ₁)，BCS 是 CQM 在单元素、无中子缺陷极限下的特例）、极端引力例外（中子星/强引力/黑洞视界，5 个 `True` 占位转为诚实 `def`）
- **分子几何→FG 退相干场管线**：新增 `MolecularGeometry.lean`（62 定理），完整形式化从分子构型到 FG 退相干场的管线：原子嘉当矩阵 → 分子超嘉当矩阵（块对角 + 跨原子耦合 t_ij）→ Weyl 嵌入（对角化提取谱间隙）→ Regge 亏角（δ_v = 2π − Σθ_tet）→ FG 退相干场强度（由角亏直接给出，不走 Regge→GR 连续极限）。`twoProtonCoupling_exactThreshold`（G20-ext 闭合）用 SOS 分解 + 黄金比例恒等式证明两质子耦合在 t < λ₁ 时正定
- **SPAF 压强-温度几何构型**：新增 `SPAF_PT.lean`（29 定理），将压强和温度转化为 A₄ 几何效应：几何压缩因子 χ(P) = (P/P_ref)^(1/3)、桥接定理（χ(P)→ω_D(P)、χ(P)→λ(P)）、再生产因子 R(T) = exp(−Γ_eff(T)·τ)、自洽 T_c 方程。新增 `SPAF_PTH.lean`（5 定理）涵盖磁场三相框架
- **消除所有 `True` 占位公理和 `sorry`**：`ElementCartan.lean` 中 5 个返回 `True` 的占位公理转为诚实 `def` 声明（`newtonianGravity_degeneracy`、`causalResolution_gravity_details`、`neutronStar_exception_idealCartan_fails`、`strongGravity_exception_newtonianDegeneracy_fails`、`extremeGravity_causalResolution_enhancement`），明确标注"不构成证明，仅标记命题声明位置"。全部 16 个 Superconductivity 模块零 `sorry`、零 `axiom`（除 `Ontology.lean` 中 5 条本体论公理，为框架出发点）
- **定理总数**：从 426 → 624（+198 个严格证明的定理），Superconductivity 库从 119 → 317（+198）

## 本次更新亮点 (v0.5.7)

- **室温可行域量化判据（第三步）**：`roomTemperature_iff_debyeLowerBound`——T_c(ω_D, λ) ≥ T_room ⟺ ω_D ≥ (T_room/2e^γ/π)·e^{1/λ}，把「室温方向」从文字叙述落成严格不等式；`roomTemperatureDebyeLowerBound_antitone_in_coupling`——所需 ω_D 下界反单调于 λ（强耦合系统性降低所需 ω_D），与双单调骨架合读：两大室温杠杆（轻晶格/高压 → 高 ω_D；强耦合 → 高 λ）可沿等值下界互换/叠加
- **SPAF 半唯像应用框架（可严格证明部分）**：新增 `SPAF.lean`（17 定理 + 4 引理），严格化框架文档 §3–§5 的可证子集——因果耦合族 t_ij = t₀·e^{−d_ij/λ}·Θ(d_cut−d_ij)（截断内正性、截断外恒零、对距离单调衰减、全局非负：`causalCoupling_pos`/`_zero_of_cutoff`/`_antitone_in_distance`/`_nonneg`）；组装对称性（对称矩阵叠加保对称、A₄ 直接拼接保实对称：`superCartan_symmetric`/`identityBlock_symmetric`/`cartanA4Stack_symmetric`）；中子缺陷 C_n = A₄ − ε·diag(1,0,0,0)（对称、ε=0 退化 `cartanHamiltonian`、缺陷位对角元 2−ε、非缺陷位保持 2、ε<2 时缺陷位对角元为正：`neutronCartan_symmetric`/`_zero_eq_proton`/`_diag00`/`_diag_ne00`/`_diag00_pos`）；味概率流 Γ_rel ≥ 0 与 Regge 边长 l_e > 0（`flavorFlowRate_nonneg`/`reggeEdgeLength_pos`）。**中子缺陷谱判据正方向（SOS 版本）**：`neutronCartan_quadratic` 给出二次型分解 xᴴC_nx = (1−ε)x₀² + x₃² + (x₀−x₁)² + (x₁−x₂)² + (x₂−x₃)²，`neutronCartan_posDef_of_lt_one`/`_of_lt_spectralGap` 证明 ε < 1（更宽）与 ε < spectralGap（判据原文）⟹ C_n 正定；`neutronCartan_not_posDef_of_five_fourths_le` 给出反方向构造：ε ≥ 5/4 时非正定（见证向量 (4,3,2,1)，xᴴC_nx = 20 − 16ε ≤ 0）——同时修正文档原述「ε ≥ γ_min 即丧失正定」（0.699 ≤ ε < 5/4 仍正定）。唯一残留缺口：区间 [1, 5/4) 的正定保持（Sylvester 余子式族）与 γ_min 的阈值认证

## 本次更新亮点 (v0.5.6)

- **金属氢能隙闭式（第二步计算框架）**：`hydrogenBcsGap` = ω_D^H/sinh(1/λ)，`hydrogen_bcs_gap_equation_solved` 证明该闭式**精确满足能隙积分方程** 1 = λ·arsinh(ω_D^H/Δ_H)——第一性解链在氢材料上的直接实例，无需经验参数：氢 = 单质子有限本体 → A₄ 谱间隙 → 晶格刚度 → 德拜频率 → 能隙闭式全部由第一性量决定
- **金属氢同位素方向**：`hydrogen_phonon_higher_than_deuterium`——氘（2·m_p）晶格的声子截止 ≤ 氢晶格（最轻有限本体给出最高 T_c 上限），对应 H3S/D3S 同位素位移 T_c(D) < T_c(H) 的家系
- **室温方向骨架（第三步）**：`bcsCriticalTemperature_mono_in_debye` / `bcsCriticalTemperature_mono_in_coupling`——T_c = 常·ω_D·e^{−1/λ} 对 ω_D 与 λ 均单调不减，室温路线的两大坐标：轻晶格 + 高压（高 ω_D）与强电子-声子耦合（高 λ）
- **第一性数值例链（主流输入标定）**：`stiffnessRefCalibrated` 由目标 ω_D 反解 A₄ 刚度 k₀ = ω_D²·M_p/λ₁；`hydrogenPhononFrequency_calibrated_eq` / `hydrogenBcsGap_calibrated_eq` / `hydrogenCriticalTemperature_calibrated_eq` 证明金属氢链（A₄ 标度 → 刚度 → 声子 → 能隙/T_c）精确还原主流输入 ω_D 与 BCS 闭式——H₃S/LaH10 数值例链的记号还原锚点（数值本身以文献 α²F(ω)/λ 为输入，见 08 超导 计算器）
- **A₄ 直接拼接（大量金属氢）**：`cartanA4Stack` = n 份 A₄ 块对角拼接（Fin 4 × Fin n）；`cartanA4Stack_zero_of_proton_ne`（跨质子零耦合）、`cartanA4Stack_block_eq`（块内仍为 A₄）、`cartanA4Stack_diag`（2-自环保持）、`cartanA4Stack_trace_eq`（Tr = 8n）、`cartanA4Stack_det_eq`（det = 5ⁿ）——禁闭几何尺度按质子数线性累加、不因拼接稀释，"大量金属氢 = 单质子 A₄ 直接拼接"已严格化

## 本次更新亮点 (v0.5.5)

- **第一性推导链**：新增 `FirstPrinciples.lean`（18 定理 + 1 引理），把超导推导起点从文献公式**下沉到物理第一原理**，全链一次铺开：质子 A₄ 循环相空间 → 晶格声子（ω_D = √(k/M)，k 由 A₄ 谱间隙 `spectralGap` 标定）→ 电子-声子耦合 λ = N(0)·V（N(0) 按主流研究结果采用，不重新推导）→ BCS 能隙积分方程 → 能隙闭式
- **严格积分恒等式（第一性严格步）**：`gapIntegral_pr` 用 `Real.hasDerivAt_arsinh`（d/dx arsinh x = 1/√(1+x²)）+ 链式法则 + 微积分基本定理（`intervalIntegral.integral_eq_sub_of_hasDerivAt`）**严格证明** ∫₀^{ω_D} dξ/√(ξ²+Δ²) = arsinh(ω_D/Δ)——把 BCS 能隙方程"积分 → arsinh"的台阶从文献输入升格为可证定理
- **积分能隙方程 ⟺ arsinh 方程、第一性解**：`bcsGapIntegralEquation_iff_arsinh` 直接把积分恒等式代入；`bcsGapIntegralEquation_solved` 证明积分方程的解 = ω_D/sinh(1/λ)（复用 Reduction 的 `bcs_gap_equation_unique` 唯一性）
- **A₄ 谱间隙标定晶格**：`latticeStiffnessFromA4_pos` / `phononFrequencyFromA4_pos` / `phononFrequencyFromA4_mono_in_stiffness`（A₄ 循环越强声子频率越高）
- **弱耦合消失**：`bcsCriticalTemperature_tendsto_zero` 证明 λ → 0⁺ 时 T_c → 0（`Tendsto`，e^{−1/λ} 严格闭式导致，非经验截断）
- **端到端正性链**：`firstPrinciples_chain_pos`——声子频率、耦合 λ、能隙闭式、张量超导序参量沿第一性链同为正
- **再生产维持（坍缩难题②的解答）**：`phaseLockingFactor_tendsto_zero`——锁定因子 e^{−Γ|τ|} 随再生产间隔趋于 0：涌现态的确定性不能一次获得、必须被反复耦合事件再生产维持（涌现公式再生产项的必要性定理）
- **金属氢实例（第二步计算起点）**：`hydrogenPhononFrequency_pos`——氢 = 单质子有限本体，禁闭几何直接是 A₄，德拜频率由谱间隙 λ₁ × 质子质量完全决定（A₄ 直接拼接，无需跨种类有限本体）
- **输入与非推导声明**：A₄ 本征向量显式构造、晶格刚度参考标度、配对强度 V、费米面态密度 N(0) 均为理想化/主流输入；G13（T_c 方程 tanh→对数渐近）如实列入缺口，不冒充定理

## 本次更新亮点 (v0.5.4)

- **嘉当张量超导方程**：新增 `CartanSuperconductivity.lean`（15 定理 + 1 引理），把 §6.8 张量涌现公式 𝒯_emergent = e^{−Γτ}·𝒫̂_𝒞(∫𝒟⊗𝒫 dμ) 理想化应用于超导序参量的 A₄ 本征谱分解——谱权重 [cartanEigenvalue]（因果潜能）× 谱系数（基础自由度）× 锁定因子 e^{−Γτ}，可观测序参量 = 对全部 4 通道的张量迹（Tr_𝒞 理想化）
- **A₄ 双重角色（哈密顿量 = 能动张量）**：`cartanHamiltonian`（A₄ 作为离散 Laplacian，07 嘉当结构 §2.1）与 `stressEnergyTrace`（A₄ 谱和 = 8）一致性定理 `cartanHamiltonian_trace_eq_stressEnergyTrace`——同一谱 {λ₁..λ₄} 同时充当哈密顿量迹与能动张量迹
- **张量序参量正性**：`superconductingOrderComponent_pos` / `superconductingOrderTensor_pos` / `superconductingOrderTensor_cartanWeights_pos`——A₄ 正定谱下超导序参量逐通道与全体严格为正
- **谱间隙退化到 BCS**：谱间隙 λ₁ = (3−√5)/2 的强大 >0/<1/最小定理；`bcsGapInGapChannel`/`bcsTcInGapChannel` 表现谱间隙同时缩放 Δ 与 T_c；`gapChannel_gapRatio_invariant` 说明普适能隙比不受谱间隙缩放影响
- **Tr(A₄⁻¹) 勘误**：`cartanInvTrace_eq_four` 证明 Tr(A⁻¹)=4；07 嘉当结构文档 §4.2 的 2 与直接计算不符，修正后 1/Tr(A⁻¹)=1/4 恰为谱间隙 E₀=c²/4 的自洽输入
- **公理性说明**：A₄ 本征结构的根 charpoly 验证沿用 CartanAlgebra 既有定位（本征向量显式构造为待办），模块以谱为输入，全部定理按理想化/退化约定严格证明

## 本次更新亮点 (v0.5.3)

- **BCS 退化与还原**：新增 `Reduction.lean`（22 定理 + 2 引理）；`cqm_reduces_to_bcs` / `cqm_debye_reduction` 为记号对应层定理；`criticalTemperature` 改用精确 BCS 常数 2e^γ/π（`bcsExactConstant`，文献 1.13 是其三位近似）
- **能隙方程的严格推导**：`bcs_gap_equation` / `bcs_gap_equation_unique` 从 T=0 能隙方程 1 = λ·arsinh(ω_D/Δ) 导出唯一闭式解 Δ = ω_D/sinh(1/λ)；`bcs_gap_weak_coupling_limit` 证明 λ→0⁺ 时闭式解渐近于 BCS 标准式 2ω_D·e^{−1/λ}（极限定理，非有限 λ 等式）
- **T_c 方程的严格推导**：`bcsTcEquation_solved`（T_c = (2e^γ/π)·ω_D·e^{−1/λ} 精确满足弱耦合 T_c 方程 1 = λ·ln((2e^γ/π)·ω_D/k_B T_c)）、`bcsTcEquation_unique`（该方程唯一正解）——T_c 公式是方程的**解**而非任意定义
- **普适能隙比（弱耦合极限定理）**：2Δ₀/k_BT_c → 2πe^{−γ} ≈ 3.5278（文献 3.53、旧公式 4/1.13 均为数值近似）——`bcs_universal_gap_ratio` 为 λ→0⁺ 极限定理（`Tendsto`）、`bcs_gap_ratio_closed_form` 为有限 λ 闭式恒等式、`bcs_gap_ratio_strong_coupling_excess` 证明有限 λ 下能隙比恒大于弱耦合极限（强耦合偏离 3.53）
- **同位素定律**：α = 1/2（`criticalTemperature_isotope_shift`）、氢/氘位移 T_c(D) = T_c(H)/√2（`hydrogen_deuterium_isotope_shift`）
- **朴素 CQM 异常（条件定理）**：`naive_cqm_isotope_anomaly` 只证明朴素替换下 T_c 随质量单调不减、与实验相反；它标示、而非证明退化的必要性
- **严格性整治**：消除 4/1.13 循环论证；能隙公式从凭空定义改为能隙方程推导；所有数值近似（1.13、3.53、0.707、1.2、1.04）在文档字符串中如实标注，不冒充定理结论
- **公理依赖审计（`#print axioms`）**：`criticalTemperature_pos`、`bcs_universal_gap_ratio`、`bcs_gap_equation(_unique)`、`bcs_gap_weak_coupling_limit`、同位素三定理、`emergenceIntegral_pos`、`strong_gravity_keeps_pairing_channels` 等全部只依赖 Lean 内核逻辑公理（`propext`、`Classical.choice`、`Quot.sound`），**不依赖任何 `physical_hypothesis` 本体论公理**——物理假设仅作公理存在、未冒充定理结论
- **金属氢机制验证**：H3S 203 K / LaH10 250 K / MgB2 39 K 验证数据已并入《CQM 超导核心理论》（08 超导），BCS/McMillan–Dynes/同位素计算对应 `TransitionTemperature.lean` 中的严格定理
- **室温方向**：三条路线 + 同位素指数 α(P) 判别性实验已并入《CQM 超导核心理论》（08 超导）§20-§21

## 本次更新亮点 (v0.5.2)

- **新增强引力超导库**：`Superconductivity`（6 模块，38 定理 / 5 公理），对应 [08 超导](../08%20超导/) 两卷文档
- **分层映射**：Ontology（第 1–2 层有限本体论）→ Gravity（第 3 层引力因果限制场）→ Mechanism（第 4–5 层超导机制）→ Integral（第 6–7 层涌现积分）→ TransitionTemperature（第 8 层 T_c）→ StrongGravity（第 9 层强引力修正）
- **核心定理**：`fourSimplex_euler_char_zero`、`causalCutoff_eq_two_pi_over_resolution`（ω_causal=2π/τ_res）、`strong_gravity_does_not_lower_causal_cutoff`、`superconductivity_requires_relation_network`、`tripleLoopStrength_locked_pos`、`emergenceIntegral_pos`、`criticalTemperature_pos`、`neutronStar_cutoff_blueshift`
- **新公理**：5 条 `physical_hypothesis`（有限本体/缺陷体/禁闭几何/内部量子引力/电子封装），沿用 CausalSet.Axioms 不透明公理模式

## 本次更新亮点 (v0.5.0)

- **消除所有 CQM 警告**：零 CQM 代码警告，构建完全清洁 ✅
- **修复 Mathieu.lean 矛盾公理**：`b1` 从占位符 `def ... := 0` 改为不透明 `axiom`，消除与 `mathieu_stable_region` 的逻辑矛盾
- **移除 4 个未使用的裸 `Prop` 公理**：`sierra_cqm_coupling_spectrum`、`prime_freezing_theorem`、`adele_constraint`、`coupling_formula_pi_factor` 替换为文档注释
- **修复文档错误**：`firstCoupling_sierraCQM_matches` → `firstCoupling_sierraCQM_deviation`、`spectralProduct_lt_one` → `spectralProduct_lt_ten`
- **定理总数**：从 96 → 160（+64 个严格证明的定理，得益于完整计数）
- **公理数**：从 14 → 7（减少 50%，消除所有未使用的声明）
- **Robertson 不等式**：从 CCR 严格推导（14 个辅助定理，无 `sorry`）✅
- **α⁻¹_SU(5) = 16384π/375**：从 A₄ 群论不变量严格证明 137 < α⁻¹ < 138 ✅
- **G_N 谱公式**：严格正性 + CODATA 偏差 < 10 ppm ✅

## 本次更新亮点 (v0.5.1)

- **Adele 约束严格化**：将 `adeleConstraint` 从公理改为由 `native_decide` 直接证明的定理，消除一个不必要的公理
- **删除未使用公理**：移除 `mathieu_critical_condition`（对占位函数 `b1` 的任意约束，且无任何定理引用）
- **清理测试残留**：删除未加入 `lakefile.toml` 且含 `sorry` 的 `TestNum.lean`
- **更新定理/公理统计**：按实际代码重新计数，当前 180 个定理 / 8 个公理（含物理假设与数值桥梁）
- **消除虚假精确等式**：谱量子 `C` 严格定义为 `1 + γ/2 - (1/2)ln(4π)`，数值近似以区间公理显式标注

## 版本

- **项目版本**: 0.6.0
- **Lean 版本**: 4.29.1
- **依赖**: mathlib, physlib
- **最后更新**: 2026-08-20