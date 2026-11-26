# Lean 验证：温度架构、相干热分裂、环 10 温度桥、环 15 尾占据、尺度反例、n(T) 领头阶、A12、矩阵分支、相位连接与正规性

**文件**：`ThermalArchitecture.lean`、`A12Counterexample.lean`、`A12Circulation.lean`、`A12Matrix.lean`、`PhaseConnection.lean`、`A12Normality.lean`、`CoherentThermalSplit.lean`、`TemperatureBridge.lean`、`TailOccupancy.lean`、`PairCellScale.lean`、`ModeCountTemperature.lean`、`PhaseStiffness.lean`、`UemuraScale.lean`、`ThreeTermBalance.lean`、`EffectiveStiffness.lean`、`SiteBondOccupancy.lean`、`IsotopeScaling.lean`、`Audit1NoGo.lean`、`PhaseTolerance.lean`、`BondGeometry.lean`、`LandauAnchor.lean`、`MemoryKernelWelding.lean`、`GeometricForcing.lean`、`M5Homogeneity.lean`、`KappaFDerivation.lean`、`TwoSectorOmegaLog.lean`、`NormalModeCompleteness.lean`、`DampingBridge.lean`、`GammaSource.lean`、`M8PhaseBoundary.lean`、`CycleSpaceHalf.lean`、`ClosureLedger.lean`、`GenusCorrection.lean`、`WeightQuantization.lean`、`A4RootCharge.lean`、`ThetaTerminal.lean`、`FieldSuppression.lean`、`AllPairsNormalization.lean`、`SelfAveraging.lean`、`FrozenCoboundary.lean`、`DeficitDrive.lean`、`PressureInvariance.lean`、`ZeroPointShift.lean`、`EffectiveCount.lean`、`MarginalAllocation.lean`、`CoexistenceWindow.lean`、`LemmaAPremise.lean`、`FrozenPremise.lean`、`ScaleCompatibility.lean`、`NodeClockCoord.lean`、`FourStageChain.lean`、`ZeroPointVariance.lean`、`CriterionSufficiency.lean`、`AllZeroUnreachable.lean`、`ShapeCompatibilityCheck.lean`、`FiniteModeReadout.lean`、`V1Limits.lean`、`AmplitudeGapEquation.lean`、`V2ElementDiagnostic.lean`、`BCSCoefficient.lean`、`EliashbergRenorm.lean`、`ZRenormWrite.lean`、`KarakozovPrefactor.lean`、`ForwardGapRatio.lean`、`MuStarShape.lean`、`IsotopeIntermediate.lean`、`FE01_EnergyScale.lean`（候选·未落地）、`FE02_NoGo.lean`（候选·未落地·否定性结果）、`FE03_CompleteTc.lean`（候选·未落地）、`FE04_PrefactorConfirm.lean`（候选·未落地）、`TwoBandGap.lean`（双带 gap 比加权，审查卡）、`Lin6FluxQuantum.lean`（临-6 磁通消歧，工作台卡）、`Lin5WeightNorm.lean`（临-5 权重归一，工作台卡）、`LoopHolonomySplit.lean`（环 5 比值传递分层，工作台卡）、`FlatTriangulationDeficit.lean`（环 3 平直三角化亏角，工作台卡）、`FLopeSlope.lean`（环 8 的 $f$ 斜率定标，工作台卡）、`TwoComponentDeficit.lean`（环 8 两分量与环流比，工作台卡）、`ZeroPointScaling.lean`（零点标度幂次，工作台卡）、`FE06_MultiBandTc.lean`（候选·未落地）、`BCCVFFElastic.lean`（环 8 BCC 弹性与 Keating 错配，工作台卡）、`BoundaryLayerDeficit.lean`（环 8 三环乘积边界分层，工作台卡）
**状态**：独立工作台文件，均已通过 `lake env lean`；未并入主库，故不改变 124 声明／60 定理计数。

## 一、承载什么

### 1.1 `ThermalArchitecture.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `totalVariance` | def | `Z + Θ T` | 只是分解接口，不证明 Debye 积分 |
| `totalVariance_mono` | theorem | Θ 单调增 ⇒ 总方差单调增 | 条件性；不证明 Θ 的谱来源 |
| `pairingCoupling` | def | 只用零点 `Z` | 不证明物理上 $\lambda$ 只取零点 |
| `pairingCoupling_T_independent` | theorem | 耦合式不含 `T` | 条件性：定义如此，故成立 |
| `dephasingRate` | def | $\gamma^2\sigma_v^2\tau_g$ | 只取环 26 的单节点支 |
| `coherence` | def | $\exp(-\Gamma t)$ | 不证明 $t$ 的物理来源 |
| `coherence_antitone` | theorem | $\Theta$ 单调增 ⇒ 相干单调减 | 需 $\tau_g,t\ge0$ 与 $\sigma_v^2$ 单调 |
| `thresholdProbability` | def | 旧 (15.1) 的阈值概率 | 只是旧读法的形式化 |
| `thresholdProbability_mono` | theorem | 方差单调增 ⇒ 阈值概率单调增 | 条件性 |
| `thresholdProbability_not_antitone_of_crossing` | theorem | 阈值跨越时不可能反单调 | 否定性判定 |

### 1.2 `A12Counterexample.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `Cex` | def | 对称 3×3 反例矩阵，对角 1、非对角一对 $-2$ | 只作逻辑反例，不声称是物理 $C$ |
| `Cex_symm` | theorem | 反例矩阵对称 | 具体计算 |
| `Cex_diag` | theorem | 对角元全为 1 | 具体计算 |
| `Cex_global_offdiag_zero` | theorem | 全局非对角零和 | 具体计算 |
| `Cex_row_zero` / `Cex_row_one` | theorem | 行和分别为 $0$、$3$ | 具体计算 |
| `Cex_not_row_sum_one` | theorem | 并非每行和为 1 | 具体计算 |
| `A12_global_not_enough` | theorem | 全局 A12 成立但 `C1=1` 不成立 | **否定性判定**：06 DM.3 不能推出 10 (8.2) |
| `per_row_A12_forces_zero_two` | theorem | 二节点逐行 A12 迫使两个非对角元为零 | 只证 $N=2$；$N=3$ 对称情形见下条 |
| `row_diag_forces_identity_two` | theorem | 二节点 `C_ii=1` 且行和全为 1 ⇒ 非对角元为零 | 只证 $N=2$；是 A12-C 在“二节点域合法”时的关键一步 |
| `symmetric_row_diag_forces_identity_three` | theorem | 三节点对称、`C_ii=1`、行和全为 1 ⇒ 三个非对角元为零 | 只证对称分支；不能当非对称分支的结论 |

### 1.3 `A12Circulation.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `Ccirc` | def | $C=I+A$，$A$ 反对称的三节点矩阵 | 只作矩阵层候选，不声称是物理 $C$ |
| `Ccirc_diag` | theorem | 对角元全为 1 | 具体计算 |
| `Ccirc_row_sum` | theorem | 每行和为 1 | 具体计算 |
| `Ccirc_global_offdiag_zero` | theorem | 全局非对角零和 | 具体计算 |
| `Ccirc_offdiag_nonzero` | theorem | $a\ne0$ 时非对角元非零 | 具体计算 |
| `Ccirc_not_symmetric` | theorem | $a\ne0$ 时 $C_{01}\ne C_{10}$ | 证明它是非对称循环，不是对称分支 |
| `Ccirc_normal` | theorem | $C C^{\top}=C^{\top}C$ | 正规性；给复特征基提供代数前提，不证明谱分解的方差式 |
| `sign_odd_row_zero_forces_all_equal` | theorem | $f$ 单射、奇、在 $x\ge0$ 上保号；$A_{ij}=f(\varepsilon_i-\varepsilon_j)$ 行和为零 ⇒ 所有 $\varepsilon$ 相等 | **任意 $N$**；是 A12-C 单函数 no-go 的一般形式 |
| `three_node_skew_row_zero_forces_zero` | theorem | $N=3$ 的同类 no-go：三个非对角值全为零 | 一般定理的具体推论 |
| `C3circ_not_from_injective_odd` | theorem | `C3circ` 不能由任何单射奇函数生成 | 是 `C3circ` 的专项否定；不证明 `C4circ` 的同类 |
| `A12_three_node_circulation_exists` | theorem | $N=3$ 存在非平凡 $C$：对角 1、行和 1、全局 A12、非对角非零 | **矩阵层存在性**；不证明它能由 $f$ 生成，也不证明物理闭环 |

### 1.4 `A12Matrix.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `Acirc3` / `Ccirc3` | def | 三节点有向环流边量与 $C=I+A$ | 只作矩阵层候选，不声称是物理 $C$ |
| `Acirc4` / `Ccirc4` | def | 四节点有向 plaquette 边量与 $C=I+A$ | 同上 |
| `Acirc3_diag` / `Acirc4_diag` | theorem | 边量对角为零 | 具体计算 |
| `Acirc3_antisymm` / `Acirc4_antisymm` | theorem | 边量反对称 | 具体计算 |
| `Acirc3_row_sum` / `Acirc4_row_sum` | theorem | 边量每行和为零（无散度） | 具体计算 |
| `Ccirc3_row_sum` / `Ccirc4_row_sum` | theorem | `C1=1` | 具体计算 |
| `Ccirc3_offdiag_global_zero` / `Ccirc4_offdiag_global_zero` | theorem | 全局 A12 | 具体计算 |
| `Acirc3_loop_sum` / `Acirc4_loop_sum` | theorem | 环路和乐为 $3a$／$4a$ | 具体计算；非梯度扇区的代数标志 |
| `Acirc3_not_gradient` / `Acirc4_not_gradient` | theorem | 不存在节点势 $\phi$ 使 $A_{ij}=\phi_j-\phi_i$ | 非梯度性；不证明材料中必有闭环 |
| `gradient_row_zero_forces_zero` | theorem | 梯度边量 $A_{ij}=\phi_j-\phi_i$ 且行和为零 ⇒ 所有差为零 | **关键结构定理**：梯度扇区被 `C1=1` 杀死 |
| `rowZero_decomp_gradient_zero` | theorem | 行零矩阵 $B=d\phi+\omega$、$\omega$ 无散度 ⇒ $d\phi=0$ | **环 9 断口**：逐样本 `C1=1` 会杀死 DM.5 的节点势差项；只支持 M／S 分支审计 |
| `A12_matrix_route_exists_three` | theorem | $N=3$：对角 1、`C1=1`、全局 A12、$A$ 无散度、非梯度 | 矩阵分支存在性 |
| `A12_matrix_route_exists_four` | theorem | $N=4$ 的同类存在性 | 矩阵分支存在性 |

**边界**：`A12Matrix.lean` 证明的是“边量矩阵分支的代数层非空且非梯度”，不证明物理闭环；H 非梯度化已否决，H 保持 \(\tau_i-\tau_j\)；它也不证明环 9 方差口径。`Ccirc3`／`Ccirc4` 仍不是 06 DM.2 的节点梯度解。

### 1.5 `PhaseConnection.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `properTimeH` | def | 固有时历史 $H_{ij}=\tau_i-\tau_j$（06 约定） | 只作代数定义，不证明 $\tau_i$ 的物理来源 |
| `properTimeH_cocycle` | theorem | $H_{ij}+H_{jk}=H_{ik}$ | 上闭链恒等式 |
| `properTimeH_loop_sum_zero3` | theorem | 三节点闭环和乐为零 | 梯度性的直接推论 |
| `phaseTheta3` | def | 三节点 \(U(1)\) 相位连接 $\theta=\alpha a$ | 只作矩阵层候选，不是物理相位 |
| `phaseTheta3_antisymm` | theorem | 相位连接反对称 | 具体计算 |
| `phaseTheta3_loop_sum` | theorem | 环路和乐为 $3\alpha a$ | 非零曲率的代数标志 |
| `phaseTheta3_not_gradient` | theorem | $\alpha a\ne0$ 时不能写成节点势差 | **关键区分**：相位连接不是固有时历史 |
| `properTime_gradient_and_phase_not_gradient` | theorem | H 是梯度、和乐为零；相位连接非梯度 | 两个 \(\mathcal H\) 的代数分离 |

**边界**：本文件只证明“固有时 H 与 \(U(1)\) 相位连接不是同一个对象”；$\theta=\alpha\lambda$ 的物理识别属 `G19`，未证。

### 1.6 `A12Normality.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `Normal` | def | $A A^{\top}=A^{\top}A$ | 实矩阵正规性定义 |
| `skew_normal` | theorem | 实反对称 $B$ 正规 | 标准线性代数 |
| `skew_add_one_normal` | theorem | $B$ 反对称 ⇒ $I+B$ 正规 | 单位阵与 $B$ 可交换 |
| `matrixBranch_normal` | theorem | 矩阵分支 $C=I+B$ 正规 | 条件性 |
| `odd_elementwise_skew` | theorem | 奇函数逐元作用于反对称边量仍反对称 | 需要 $\forall x,f(-x)=-f(x)$ |
| `matrixBranch_normal_of_odd` | theorem | 任意奇 \(f\)、任意反对称 $\lambda$，$C=I+B$ 正规 | **关键回改**：原先“一般 \(C\) 非正规”判断删除 |

**边界**：正规性只保证均值谱的酉本征基；不推出 DM.5 的 \(\rho_{ij}\)，也不证明 \(C\) 的物理来源；上一轮的 \(\rho^{spec}\) 路线已删除。

### 1.7 `CoherentThermalSplit.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `totalVar` | def | \(Z(1+2n_B)\) | 单模总方差；不证明 Debye 积分 |
| `coherentVar` | def | \(Z/(1+2n_B)\) | 单模相干第二矩；物理识别未证 |
| `incoherentVar` | def | \(2Zn_B\) | 单模非相干热部分 |
| `total_eq_zero_add_incoherent` | theorem | \(V_{\rm tot}=Z+V_{\rm inc}\) | 代数恒等式 |
| `coherentVar_nonneg` / `incoherentVar_nonneg` | theorem | 非负性 | 需 \(Z,n_B\ge0\) |
| `coherentVar_antitone` | theorem | \(n_B\) 增 ⇒ 相干第二矩减 | 单模；不是多模定理 |
| `incoherentVar_mono` | theorem | \(n_B\) 增 ⇒ 非相干部分增 | 单模 |
| `coherent_mul_total` | theorem | \(V_{\rm coh}V_{\rm tot}=Z^2\) | **仅单模**；分母非零 |
| `coherent_eq_sq_div_total` | theorem | \(V_{\rm coh}=Z^2/V_{\rm tot}\) | **仅单模**；不能外推到 Debye 多模 |
| `nodeJosephsonWeight` | def | \(V_{\rm coh}/Z\) | 节点项归一；不是含 \(\sigma_\omega\) 的全式 |
| `nodeJosephsonWeight_zero` | theorem | \(V=Z\) 时权重为 1 | 条件 \(Z\ne0\) |
| `nodeJosephsonWeight_mono` | theorem | \(V\) 增 ⇒ 权重增 | 故 \(V\) 降 ⇒ \(J\) 降 |

**边界**：本文件只承载单模代数与方向，不证明 \(V_{\rm coh}\) 就是 DM.5 的物理对象，不证明 \(\sigma_{\omega,\rm coh}\) 的来源，也不证明 Debye 谱就是 CQM 的谱。

### 1.8 `TemperatureBridge.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `stiffnessFromBondSum` | def | \(\Upsilon=(1/(2A))\cdot\) 键和 | 键和抽象；不写显式格点和 |
| `stiffness_rescale` | theorem | 键和整体乘 \(w\) ⇒ \(\Upsilon\) 乘 \(w\) | 代数线性；不证明 \(w\) 的谱来源 |
| `bondTerm` / `bondTerm_rescale` | def / theorem | 单键 \(Jr^2\) 的线性重标 | 具体代数 |
| `normalizedCoherent` | def | \(V_{\rm coh}/Z\) | 归一化权重 |
| `normalizedCoherent_zero` | theorem | \(V_{\rm coh}=Z\) ⇒ 权重 1 | 条件 \(Z\ne0\) |
| `normalizedCoherent_antitone` | theorem | \(V_{\rm coh}\) 降 ⇒ 权重降 | 条件 \(Z>0\) |
| `stiffness_coherent` | theorem | \(\Upsilon\) 与 \(w\) 的桥 | 条件于键和因子化 |
| `pairReadout` | def | 任意单调读出 \(F(\sqrt{V})\) | 不代表具体概率分布 |
| `pairReadout_antitone` | theorem | \(V\) 反单调 ⇒ 读出反单调 | 只给方向 |
| `pSync_antitone` | theorem | \(t>0\) 时 \(p^t\) 同向 | \(t\) 未定 |

**边界**：本文件只承载“均匀重标 ⇒ 刚度同重标”与“单调读出保方向”；不证明 DM.9 的 \(J_{ij}\) 构造、不证明 \(p_{\rm pair}\) 的分布、不证明 Debye 积分或 \(w(T)\) 的 \(\pi^2/3\) 系数。

### 1.9 `TailOccupancy.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `tailOccupancy` | def | 上尾 \(1-F(u)\) | 任意 CDF 接口，不指定分布 |
| `tailOccupancy_antitone` | theorem | \(F\) 单调、\(u_1\le u_2\) 则上尾降 | 代数 |
| `pairOccupancy` | def | \(1-F(k/V)\) | 条件接口 |
| `pairOccupancy_antitone` | theorem | \(k\ge0\)、\(V_2\le V_1\) 则尾概率升 | 需 \(V_2>0\) |
| `normalizedPairArgument` | def | \(k/(Zw)\) | 环 10 形式 |
| `normalizedPairArgument_antitone` | theorem | \(w\) 降则归一自变量升 | 需 \(Z,k,w>0\) |

**边界**：本文件只承载“单调 CDF 下阈值概率的方向”，不证明局部方差是 chi-square，不证明 \(n_{\rm cell}\)、\(\sigma_c\)、\(t\) 的物理值，也不证明 \(p_{\rm sync}=p_c\) 与 \(T_c\) 等价。chi-square 身份与端点展开在 `03_推导工作台/环15_配对概率分布.md` 与 Python 数值中给出。

### 1.10 `PairCellScale.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `avgAbove` | def | 两读数均值超阈的指示 | 只是两读数接口，不声称是物理格胞 |
| `fracAbove` | def | 两读数中超阈的比例 | 同上 |
| `avgAbove_self` | theorem | 均匀格胞 \(x=y\) 时两者重合 | 只在两读数；不证明多读数 |
| `avgAbove_ne_fracAbove` | theorem | 存在非均匀格胞使两者不等 | **否定性判定**：阈值平均 ≠ 平均阈值 |
| `avg_above_not_all_above` | theorem | 均值超阈且一个读数不超阈时两者不等 | 条件性反例 |

**边界**：本文件只承载“粗粒化均值阈值不等于局域配对比例”的代数反例；不证明物理场一定非均匀，也不证明 \(p_{\rm sync}=p_c\)。它用于阻止把层 B 的 chi-square 尾直接当作 (15.1) 的层 A 局域概率。

### 1.11 `ModeCountTemperature.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `ratio_expansion` | theorem | \((1-bt)/(1-at)=1+(a-b)t+(a-b)at^2/(1-at)\) | 纯代数；\(1-at\ne0\) |
| `ratio_residual` | theorem | 减去线性项后的残差为 \(O(t^2)\)，系数 \((a-b)a/(1-at)\) | 纯代数；\(t\ne0\) |

**边界**：本文件只承载 \(n_{\rm cell}=N_{\rm eff}(T)\) 时归一自变量的领头代数；不证明 \(N_{\rm eff}\) 公式、\(b\) 的物理值，也不证明 chi-square 尾的端点展开。

### 1.12 `PhaseTolerance.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `theta_lin` | theorem | \(2\pi s(1-(1+\lambda)^2)=-4\pi s\lambda-2\pi s\lambda^2\) | 纯代数；给 `G19` 的线性系数与二阶余项 |
| `stiffness_scaling` | theorem | \(\sum_{ij}(\alpha x_i-\alpha x_j)^2=\alpha^2\sum_{ij}(x_i-x_j)^2\) | 纯代数；相位刚度按 \(\alpha^2\) 重标 |
| `tri_nonneg` / `tri_le_pi` | theorem | 折回相位读数落在 \([0,\pi]\) | 只证单周期三角读数 |
| `tri_eq_self` | theorem | \(x\le\pi\) 时三角读数 \(=x\) | 回收 06 §10.1 的小和乐线性式 |
| `fidelity_period` | theorem | \(\cos(W+2\pi)=\cos W\) | 相位窗口不能线性无界 |
| `onset_shifts_with_fidelity` | theorem | 同温下保真度更大 ⇒ 仍在闭合区内 | 条件性；不证明 \(T_*\) 存在唯一 |
| `dead_zone` | theorem | 保真度 \(\le0\) 时无正温解 | 条件性；对应完全阻挫 |

**边界**：本文件只承载 `G19` 的代数核心（线性化系数、\(\alpha^2\) 重标、单周期读数、死区）；不证明环长计数 (6G.5)、\(A(\varepsilon)\) 的方差来源或表示权 \(s\) 的 A4 值。

### 1.13 `BondGeometry.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `two_one_sub_cos_nonneg` | theorem | \(0\le2(1-\cos x)\) | 纯代数 |
| `two_one_sub_cos_le_sq` | theorem | \(2(1-\cos x)\le x^2\) | 由 `Real.one_sub_sq_div_two_le_cos`；给 3D 关联的界 |
| `rho3d_nonneg` / `rho3d_le_one` | theorem | \(x\ne0\) 时 \(0\le\rho_{3d}(x)\le1\) | 只证 3D；2D 无此界 |
| `one_minus_rho3d` | theorem | \(1-\rho_{3d}=(x^2-2+2\cos x)/x^2\) | 纯代数 |
| `Jshape_abs_le` | theorem | \(0\le\rho\le1\) 时 \(|(1-\rho)\cos\theta|\le1\) | 条件性 |
| `Jshape_pos` | theorem | \(\rho<1\)、\(\cos\theta>0\) 时 \(J>0\) | 条件性 |
| `saturates` | theorem | \(\rho(d)\to0\) ⇒ \((1-\rho(d))\to1\) | **饱和定理的代数核**；$\varepsilon$ 语言 |
| `saturates_to` | theorem | \(\rho(d)\to c\) ⇒ \((1-\rho(d))\to(1-c)\) | 加强版：不需衰减率、不需单调 |
| `saturation_pos` | theorem | \(c<1\) ⇒ \(0<1-c\) | 只有 \(\rho_\infty=1\)（零方差）才给 \(J=0\) |

**边界**：本文件只承载 `M6` 的代数核心（3D 关联的界、形状因子的界与号、饱和定理）；不证明 Debye 关联 (10M.9)–(10M.11)、Bessel 函数、全对求和发散（数值给），也不证明 \(J_0\) 的绝对值（Z2 外生）。

### 1.14 `LandauAnchor.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `aMF_zero_iff` | theorem | \(zJ\ne0\)、\(T\ne0\) 时 \(a(T)=0\iff T=T_0\) | 锚＝平均场临界点 |
| `aMF_neg` / `aMF_pos` | theorem | \(T<T_0\) 给 \(a<0\)；\(T>T_0\) 给 \(a>0\) | 有序／无序两侧 |
| `bMF_pos` | theorem | \(b(T)>0\) | 条件性 |
| `bMF_at_T0` | theorem | \(k_BT_0=zJ/2\) 时 \(b=zJ/8\) | 纯代数 |
| `mf_tc` | theorem | \(T_0=zJ/(2k_B)\) | 平均场相位温度 |
| `deltaC_MF` | theorem | \(\Delta C=T_0k_B^2/(2b)=2k_B\)（每座） | 平均场值 |
| `dim_selective` | theorem | \(2-d=0\iff d=2\) | 维度选择性算术核 |
| `bkt_ratio` | theorem | \(\Upsilon=\frac{2}{\pi}k_BT\Rightarrow\Upsilon/(k_BT)=\frac{2}{\pi}\) | 二维普适跳变 |
| `tc_scale` / `ratio_J_indep` | theorem | \(T_c=cJ/k_B\) 对 \(J\) 齐次；比值与 \(J\) 无关 | 能量标独立性 |
| `ginzburg_exp_pos` | theorem | \(0<d<4\Rightarrow2d/(4-d)>0\) | Ginzburg 指数 |
| `ginzburg_d3_lt_d2` | theorem | \(0<r<1\Rightarrow r^6<r^2\) | 三维临界区窄于二维 |

**边界**：本文件只承载 `审-11` 的代数核心；不证明 \(I_0\) 的级数展开与 \(\ln I_0\) 组合（数值给）、\(\Delta C\) 的求导、Ginzburg 判据的场论推导（外部标准）、三维 XY 常数（外部），也不证明绝对 \(T_c\)（瓶颈在振幅扇区）。

### 1.15 `MemoryKernelWelding.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `gamma_sq_ne_of_gamma_ne` | theorem | \(g\ne h\)、\(g\ne-h\) ⇒ \(g^2\ne h^2\) | 零点纵坐标互异 |
| `Gamma_ne_of_gamma_sq_ne` | theorem | \(\sigma_v^2\tau_g>0\) ⇒ \(\Gamma_n\ne\Gamma_m\) | 模相关阻尼 |
| `exp_rate_injective` | theorem | 指数率对所有 \(t\) 相等 ⇒ 率相等 | 用 \(t=1\) |
| `single_mode_rate` / `mode_no_go` | theorem | 单模对齐条件；两模不能同时对齐 | **No-go A 代数核** |
| `alpha_must_be_half` | theorem | 无涨落时仍须 \(\alpha=1/2\) | 规范归一 |
| `positive_type_zero_nonneg` / `zeta_kernel_zero_neg` | theorem | 正定型核 \(K(0)\ge0\)；链约定 \(K_\zeta(0)=-1\) | **No-go B**（条件性） |
| `gauge_coincidence` | theorem | 同一读数要求节点固有时相同 | **No-go C** |
| `W` / `W_eq_one` / `W_at_ideal` | 定义＋theorem | 逐模滤波器；\(W=1\iff\) 率对齐；理想极限 \(W=1\) | 规范截面 |
| `filter_ne_of_Gamma_ne` | theorem | \(\Gamma_n\ne\Gamma_m\) ⇒ 滤波器不同 | 物理核非 zeta 核的标量倍 |

**边界**：本文件只承载 `临-8` 的代数核心；不证明显式公式的收敛与共轭配对（外部）、正定型核的傅里叶刻画（外部）、$\psi(1)=0$（取链约定 \(K_\zeta(0)=-1\)）。

### 1.16 `GeometricForcing.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `loop_sum_ne_zero_of_product_ne_one` | theorem | $\exp\lambda_k=r_k$ 且 $r_1r_2r_3\ne1$ ⇒ $\sum\lambda\ne0$ | 几何强制的解析核 |
| `loop_sum_zero_of_product_one` | theorem | 乘积为 1 ⇒ 和乐为零 | 逆否方向 |
| `holonomy_gauge_invariant` | theorem | 规范位移不改三环和乐 | $\mathbb R_+$ 联络 |
| `odd_pair_cancel` / `three_cycle_row_zero` | theorem | 奇函数成对相消；三角环行和零 | 奇性代数 |
| `center_symmetric_row_sum` | theorem | 中心对称四邻居 ⇒ $\sum f(\lambda)=0$ | `C1=1` 自动成立 |
| `fLin` / `fCub` 及 `_odd` / `_row` | 定义＋theorem | $x$ 与 $x^3$ 都是奇函数且行和零 | 两个候选 $f$ |
| `f_not_determined_by_row_sum` | theorem | $f_{\rm lin}(2)\ne f_{\rm cub}(2)$ | $f$ 不由 `C1=1` 唯一确定 |

**边界**：本文件只承载 `审-1` 结构问题的代数核心；不证明 $v_\tau$ 单值性到 (1G.3) 的物理推导、外部线丛定理、BCC 壳层是否满足中心对称（需材料数据）；$f$ 显式与累积层 $f^{-1}$ 仍开放。

### 1.17 `M5Homogeneity.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `Solves` | 定义 | 齐次线性系统 $D\mathbf f=0$ | N×m 矩阵 |
| `zero_solves` | theorem | $\mathbf f=0$ 总是解 | $C=I$ 分支 |
| `scale_solves` / `sum_solves` | theorem | 数乘／加法保解 | 解集为子空间 |
| `odd_scale` / `odd_sum` | theorem | 数乘／加法保奇性 | 奇性不被破坏 |
| `not_unique_of_nonzero` | theorem | 非零解 ⇒ $f$ 与 $2f$ 是两个不同解 | 非唯一性 |
| `signedCount_zero_of_equal` | theorem | 中心对称 ⇒ 有符号计数为零 | $D=0$ 特例 |
| `zero_f_gives_zero_B` | theorem | $f\equiv0$ ⇒ $B=0$ | 平凡分支坍缩 |
| `kappa_absorbs_scale` | theorem | $(\kappa/c)(cf)=\kappa f$ | 尺度并入 $\kappa_f$ |
| `both_solve_centrosymmetric` / `fLin_ne_fCub` | theorem | $x$ 与 $x^3$ 都解但不同 | 形状不唯一 |

**边界**：本文件只承载 `M5` 的齐次线性代数核心；不计算 $\dim\ker D$（需 BCC 逐边亏角）、不证明秩—零化度（外部线性代数）、不给 $\kappa_f$ 来源（审-2）。

### 1.18 `KappaFDerivation.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `phi` / `v2` | 定义 | $\phi=\frac12\ln(1-\varepsilon/2\pi)$、$v_\tau^2=1-\varepsilon/2\pi$ | FG 接口 |
| `phi_deriv` | theorem | $\phi'=-1/(4\pi v_2)$ | 条件 $v_2>0$，用 `HasDerivAt` |
| `kappaF_formula` / `kappaF_at_zero` / `kappaF_pos` | theorem | $\kappa_f=1/(4\pi v_2)$；$\kappa_f(0)=1/(4\pi)$；正性 | 条件于 FG 与识别 |
| `matrixScale_formula` | theorem | $c=4\pi v_2\kappa_f$ | 代数 |
| `matrixScale_eq_one` / `matrixScale_at_zero` | theorem | 取几何 $\kappa_f$ 得 $c\equiv1$；锚点亦为 1 | 不是 $v_2$ |

**边界**：本文件只承载 `审-2` 的解析核心；不证明 $\delta C=\delta\lambda$ 的物理识别（构造步骤）、FG 接口本身（E4）、节点 ε 与边 ℓ 的代表值误差。

### 1.19 `TwoSectorOmegaLog.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `prefactor` / `omegaLogAmp` / `omegaLogPh` | 定义 | $e^{-1/d}$、两扇区对数矩 | 都 $\propto\omega_D$ |
| `two_moments_differ` | theorem | $e^{-1/3}\ne e^{-1/2}$ | 分裂的代数核 |
| `ratio_of_moments` | theorem | 比值 $e^{1/6}$，与能标无关 | 外部 Debye 矩 |
| `prefactor_three` / `prefactor_two` | theorem | 两个前因子的解析值 | 数值形式 |
| `isotope_scaling_same` | theorem | 两矩质量依赖相同 | 端点分类不变 |
| `sector_not_replace` | theorem | 单一公共矩不能等于两扇区矩 | 分裂而非替换 |

**边界**：本文件只承载 `审-10` 收口的代数核心；不证 Debye 积分的分析式（外部＋数值）、BCS 前因子 $1.13$（外来式）。

### 1.20 `NormalModeCompleteness.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `injective_implies_le` | theorem | 单射 $\mathbb R^n\to\mathbb R^m$ ⇒ $n\le m$ | 秩—零化度 |
| `euler_count` | theorem | $3F=2E,\ V-E+F=2$ ⇒ $E=3V-6$ | 闭球面三角化 |
| `deficit_not_complete` | theorem | $V\ge4$ ⇒ 亏角映射非单射 | `W-3′` 判否的代数核 |
| `kernel_nontrivial` | theorem | 存在 $\delta l\ne0$ 使 $\delta\varepsilon=0$ | 核模存在 |
| `kernel_bound` | theorem | $E-V=2V-6$ | 维数下界 |

**边界**：本文件只承载 `W-3′` 的计数核心；不证实际 Regge 映射矩阵元、离散共形形变定理（外部），只作物理识别。

### 1.21 `DampingBridge.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `tauG` / `Gamma` / `sigmaHighT` | 定义 | $c/\omega_D$、$\gamma_n^2\sigma_v^2\tau_g$、$\kappa T/\omega_D$ | 形状，$c$／$\kappa$ 未定 |
| `Gamma_linear_T` / `s_tau_highT` | theorem | $\Gamma_n\propto T$，$\sigma_v^2\tau_g\propto T/\omega_D^2$ | 高温分支 |
| `Gamma_modes_differ` | theorem | $\gamma_n^2\ne\gamma_m^2$ ⇒ $\Gamma_n\ne\Gamma_m$ | 模依赖 |
| `no_beta_unification` | theorem | 两模不能共享统一物理率 | `临-22` 判否 |
| `time_unit_gauge_only` | theorem | 公共重标不改模差（时间单位规范） | RH 仍外部 |

**边界**：本文件只承载 `临-22` 的代数核心；不证 Debye 浴关联时间（外部）、Planckian 系数（链内无对象）。

### 1.22 `GammaSource.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `Gamma` / `betaShape` / `tcFactor` | 定义 | 累积态数、热力学乘子形状、峰温因子 | 形状 |
| `spectral_exponent` | theorem | 累积 $x^d$ 的导数为 $d x^{d-1}$ | 谱维数 $n=d$ |
| `beta_n1_strictly_decreasing` | theorem | $n=1$ 无峰、无相变 | 单调性 |
| `peak_n2` | theorem | $n=2$ 峰条件正支 $x=1$ | 代数 |
| `tc_factor_n3` / `chi_rescales_only` | theorem | $2^{-2/3}$；外参只移峰位不改 $n$ | 与 (26.A3) 一致 |
| `prediction_vs_observation` | theorem | Al 观测比 $0.0028\ll0.63$ | 替代入口判否 |

**边界**：本文件只承载 `审-14` 的代数核心；不证 $\Gamma$ 的态计数物理解释（外部）、$\chi\leftrightarrow A12$ 精细对应、$\beta\neq\beta_n$ 的物理。

### 1.23 `M8PhaseBoundary.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `Rfun` / `pStar` | 定义 | $R=T/w$、$p_*=p_c+(1-p_c)R^{1/t}$ | 相界方程 |
| `R_log_deriv` | theorem | $R'/R=1/T-w'/w$ | 微积分 |
| `pStar_deriv` | theorem | $p_*'=(1-p_c)(1/t)R^{1/t-1}R'$ | 链则 |
| `implicit_slope` | theorem | $dT_c/d\delta=(dp_{\rm pair}/d\delta)/p_*'$ | 隐函数 |

**边界**：本文件只承载相界方程的微分核心；不证 $t_\Upsilon$ 数值、因子化、`审-4` 座→键映射。

### 1.24 `CycleSpaceHalf.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `cycle_half_fibre` | theorem | GF(2) 非零泛函两纤维等势 ⇒ 环空间每边占据 $1/2$ | 有限群 |
| `induced_bond_symm` / `induced_bond_mean` | theorem | 诱导键对称、均值 $p^2$ | 占据场，非联络 |
| `shared_covariance` | theorem | 共点协方差 $p^3(1-p)$ | 统计 |
| `site_threshold_bond_fraction` | theorem | $(0.592746)^2<1/2$ | 阈值换算 |
| `withdraw_tu6` / `loop_half_not_bond_fraction` | theorem | 推 6 混用对象，不成立 | 撤销判定 |

**边界**：本文件只承载 `审-4` 的代数核心；不证环空间维数的图论证明、材料对账。

### 1.25 `ClosureLedger.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `Status` | 归纳类型 | A/B/C/D 四态（都不是"已闭合"） | 分类判定人工 |
| `ledger_62_rows_35_unique` / `advanced_35_split` | theorem | 62 行、35 唯一编号、27 行重复；35 推进（A29/B6）、0 余 | 账面更新（第 48 轮） |
| `tc_homogeneous` | theorem | $T_c=\omega_D F(\Upsilon_0/\omega_D)$ 对两者共同缩放齐次 | 形状不定标度 |
| `injective_implies_le` / `euler_count` / `deficit_not_injective` | theorem | W-3′ 判否的代数核 | 计数 |
| `welding_no_go` / `unified_nogo` | theorem | 临-8 与临-22 的模依赖合取 | B 类汇总 |

**边界**：本文件只承载总账的代数核；四态分类是人工判定，不从主链自动抽取。

### 1.26 `GenusCorrection.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `euler_genus` / `codim_closed` | theorem | Euler 代入给面边界子空间余维 $2g$ | 闭曲面 |
| `codim_boundary` / `boundary_needed` | theorem | 带边界余维 $2g+b$，$b>0$ 必有缺失标签 | 带边界 |
| `planar_exact` / `noncontractible_needed` | theorem | 精确域 $g=0,b=0$；$g>0$ 必缺标签 | 适用域 |
| `bettiOne` / `betti_one_eq_two_g` | 定义＋theorem | $b_1=2g$ 账面等式 | 外部拓扑 |

**边界**：本文件只承载 2D 可定向曲面的代数核；3D 挠系数与材料拓扑未给。

### 1.27 `WeightQuantization.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `integer_weight_of_single_valued` | theorem | $\cos(2\pi s)=1\Rightarrow s\in\mathbb Z$ | 玻色表示 |
| `half_integer_weight_of_double_cover` | theorem | $\cos(2\pi s)=-1\Rightarrow 2s=2n-1$ | 旋量双覆盖 |
| `weight_quantized` | theorem | 两类合并 ⇒ $2s\in\mathbb Z$ | 群论 |
| `alpha_quantized` | theorem | $\alpha_{\rm lin}=-2\pi(2s)\in2\pi\mathbb Z$ | 代数 |

**边界**：本文件只承载转动子群的权量子化；A4 权选档（`临-26`）与非阿贝尔部分未处理。

### 1.28 `A4RootCharge.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `rootCharge` | 定义 | $q_{ij}=h_i-h_j$ | Fin 5 根 |
| `integral_cocharacter_charge` | theorem | 整余特征 ⇒ $q_{ij}\in\mathbb Z$ | 紧致约化 |
| `spin_cocharacter_charge` | theorem | 半整余特征 ⇒ $q_{ij}\in\frac12\mathbb Z$ | 自旋提升 |
| `omegaCoweight` / `fundamental_coweight_charge` | 定义＋theorem | 基础余特征电荷仅 $-1,0,1$ | 第一层 |
| `merge_with_G19` | theorem | 根电荷整性与 $s\in\frac12\mathbb Z$ 合并 | 选档约束 |

**边界**：本文件只承载根电荷格点；$A_4$ 完整根/权格定理与材料约化证明属外部。

### 1.29 `ThetaTerminal.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `thetaTemp` | 定义 | $T_{\theta,n}=C\gamma_n^2$，$C=\hbar\sigma_v^2\tau_g/k_B$ | 【构造】 |
| `gamma_sq_monotone` / `theta_monotone` | theorem | $\Gamma_n$ 与 $T_{\theta,n}$ 随 $\gamma_n$ 增 | 代数 |
| `min_selects_first` | theorem | 前三零点 min 为 $n=1$ | 数值示意 |
| `uniform_iff_same_theta` | theorem | 统一 $T_\theta$ ⇔ 统一阻尼 | 接 `临-22` |
| `theta_scaling` | theorem | 代入 $\tau_g=c/\omega_D$ | 代数 |

**边界**：本文件只承载端子的代数核；Planckian 换算的物理证明属外部标准。

### 1.30 `FieldSuppression.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `fluxQuantum` / `flux_quantum_pair` | 定义＋theorem | $\Phi_0=h/q$，$q=2e$ ⇒ $h/(2e)$ | 链内电荷 |
| `pair_charge_excludes_e` | theorem | $q=e$ 会加倍 $\Phi_0$，链排除 | 模式集 |
| `bc2_formula` | theorem | $B_{c2}=h/(4\pi e\xi^2)$ | GL 外部 |
| `fLinear` / `f_linear_zero` / `low_field_slope` | 定义＋theorem | $f=1-a x$、$f(0)=1$、$a>0$ ⇒ 递减 | 低场 |
| `normalized_slope` | theorem | $dT_c/dB|_0=-a T_{c0}/B_{c2}$ | 代数 |

**边界**：本文件只承载场依赖的代数核；GL 关系、$a$ 的 RG 计算、$\xi$ 的第一性值属外部。

### 1.31 `AllPairsNormalization.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `Rfrac` | 定义 | $R=\|\sum z_i\|/M$ | 活跃键 |
| `Rfrac_le_one` / `Rfrac_nonneg` | theorem | 单位相量给 $R\in[0,1]$ | 三角不等式 |
| `active_count_normalizer` | theorem | 总数归一只给 $M/N$ 稀释 | 归一口径 |
| `full_coherence_bound` | theorem | 全相干 $R=1$ | 界 |

**边界**：本文件只承载归一的代数核；$\mu_t$ 谱形与随机相位标度属外部/数值。

### 1.32 `SelfAveraging.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `varMean` | 定义 | $(n\sigma^2+C)/n^2$ | 协方差和 $C$ |
| `independent_var` / `variance_ratio` | theorem | $C=0\Rightarrow\sigma^2/n$、比值 $m/n$ | $|D_i|^{-1/2}$ 来源 |
| `correlated_floor` | theorem | 正协方差给方差平台 $\bar c$ | 自平均失效 |
| `self_avg_condition` | theorem | $C\le kn\Rightarrow\operatorname{Var}\le(\sigma^2+k)/n$ | 成立条件 |

**边界**：本文件只承载方差代数；材料 $\bar c$ 与概率论公理属外部。

### 1.33 `FrozenCoboundary.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `cFromA` | 定义 | $c_{ij}=a_i-a_j$ | 冻结固有时 |
| `c_antisymm` / `c_cocycle` | theorem | 反对称与三环闭合（1-余缘） | 代数 |
| `c_kernel_constants` / `c_two_parameters` | theorem | 核为常向量；$N=3$ 时两参数定全部 | $N-1$ |
| `gaussCF` / `gaussCF_decreasing` | 定义＋theorem | 高斯特征函数；高频模衰减更快 | 外部标准 |

**边界**：本文件只承载余缘代数；材料 $\sigma_a$ 与概率论证明属外部。

### 1.34 `DeficitDrive.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `thetaRate` / `law_of_cosines_rate` | 定义＋theorem | 余弦定理微分形式的代数核对 | 几何 |
| `deficitOf` / `deficit_rate` | 定义＋theorem | $\varepsilon=2\pi-\sum\theta$、$\varepsilon$ 随 $\theta$ 的变化 | 线性 |
| `all_angles_up` / `deficit_decreases` | theorem | 面角全增 ⇒ 亏角减 | 符号 |
| `linear_in_drive` | theorem | $\dot\varepsilon=\chi\dot E$ 的线性性 | 代数 |

**边界**：本文件只承载运动学代数；材料 $d_e$ 与 $\arccos$ 求导属外部。

### 1.35 `PressureInvariance.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `cos_ratio_invariant` | theorem | 余弦比齐次不变 | 代数 |
| `euler_zero_for_triangle` | theorem | $\sum_e\ell_e\partial_\ell\theta=0$ | 余弦定理 |
| `uniform_strain_zero` | theorem | 比例应变给零角变 | 几何 |
| `deficit_change` / `nonuniform_generates` | theorem | 角变为零则亏角不变；非比例响应生非零 | 代数 |

**边界**：本文件只承载压强映射的几何核；弹性模量与褶皱阈值属外部。

### 1.36 `ZeroPointShift.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `phase_shift` / `mode_factor` | theorem | $\gamma(\tau-\Delta)=\gamma\tau-\gamma\Delta$；$e^{i\gamma(\tau-\Delta)}=e^{-i\gamma\Delta}e^{i\gamma\tau}$（辅助 `exp_I_add`） | 复数指数代数 |
| `h_shift` / `frozen_h_invariant` | theorem | $\mathcal H'=\mathcal H-(\Delta_i-\Delta_j)$；$\Delta_i=\Delta_j$ ⇒ $\mathcal H'=\mathcal H$ | 判据层零点无关 |
| `diff_shift_frozen` | theorem | 冻结下 (14.2) 差获逐模因子 $e^{-i\gamma\Delta}$ | 读数层零点相关 |
| `corr_zero_point_free` | theorem | 两点相关零点相消，只剩 $e^{i\gamma\Delta\tau}$ | 相关量零点无关 |
| `modulus_sq_one` | theorem | 模平方为一 ⇒ 幅度谱零点无关 | 外部三角恒等式 |

**边界**：本文件只承载零点换元的代数核；$\Delta_i$ 材料值与 $\{\gamma_n\}$ 不可公度属外部。

### 1.37 `EffectiveCount.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `pr` / `IsWeight` / `sum_sq_pos` | 定义＋theorem | 参与比泛函 $n_{\rm eff}=1/\sum p_i^2$；归一化权重平方和为正 | 初等代数 |
| `pr_lower` / `pr_upper` | theorem | $1\le n_{\rm eff}\le\|\mathrm{supp}\,p\|$（逐项平方，不依赖外部 Cauchy-Schwarz） | 不等式 |
| `pr_uniform` | theorem | 等权饱和 $n_{\rm eff}=N$ | 代数 |
| `split_sq_ge` / `pr_two_le_two` | theorem | 细分不减；筛选可减（两点 $\le2$） | 不等式 |

**边界**：本文件只承载参与比的代数核；三候选权重与 $\xi$／$\Delta\varepsilon$／$N(0)$ 属外部。

### 1.38 `MarginalAllocation.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `marg` | 定义 | 离散边际 $m(n)=\lambda(n+1)-\lambda(n)$ | 差分 |
| `marg_eq_unique` | theorem | 严格反单调 ⇒ 等边际点唯一 | 凹性 |
| `transfer_gain` / `convex_transfer_reverse` | theorem | 凹⇒转移增益正（内点最大）；凸⇒反向（角点最大） | 两支判据 |
| `sat_marg_form` / `sat_marg_strictAnti` | theorem | (16.A1) 边际几何闭式与严格反单调 | 指数代数 |

**边界**：本文件只承载分配结构的差分代数；$x^\beta$ 凹性、$\mu$ 绝对值与材料参数属外部。

### 1.39 `CoexistenceWindow.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `pLoc` / `pLoc_lt_pc` | 定义＋theorem | $p_c^{\rm loc}=p_c-Cn_{\rm eff}^{-3/8}$，严格低于全局 $p_c$ | rpow 代数 |
| `window_width` / `window_nonempty` | theorem | 窗口宽度 $\Delta p=Cn_{\rm eff}^{-3/8}$，并存区间非空 | 标度 |
| `window_decreasing` | theorem | 宽度随 $n_{\rm eff}$ 严格递减（负指数） | rpow 单调 |
| `capacity_lower_aux` / `q_pow_back` | theorem | 容量下限代数核 $q<p_c/C$ 与 $q^{-8/3}=n_{\rm eff}$ | 代数 |

**边界**：本文件只承载并存窗口的标度代数；$C$、材料微结构与锚的流场充分条件属外部。

### 1.40 `LemmaAPremise.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `pair_ratio_irrational_zero` | theorem | 原引理 A：一对无理比 ⇒ $c=0$ | 实数/有理 |
| `unbounded_dvd_only_zero_nat` | theorem | 无界整除因子 ⇒ 被整除数为零 | Nat 整除 |
| `denom_unbounded_zero` | theorem | 分母无界 ⇒ $c=0$（弱化前提版引理 A） | 整数论 |
| `bounded_denom_lattice` | theorem | 分母有界 ⇒ 格点结构 | 代数 |

**边界**：本文件只承载引理 A 前提弱化的整数论；LI 猜想、$N(T)$ 渐近与重数有界属外部。

### 1.41 `FrozenPremise.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `rate_eq_speed_diff` / `pair_frozen_iff_speed_eq` | 定义＋theorem | $\Delta\mathcal H_{ij}=v_i-v_j$，逐对冻结 ⇔ 流速相等 | 差分代数 |
| `all_pairs_frozen_imp_constant` / `constant_imp_all_pairs_frozen` | theorem | 冻结 ⇔ 场公有化（(22.3) 反向＋正向） | 传递性 |
| `frozen_relation_equivalence` | theorem | 冻结关系是对等关系（连通分量） | 等价关系 |
| `state1_excludes_freezing` / `state2_excludes_state3` | theorem | 三态互斥的代数表述 | 代数 |

**边界**：本文件只承载冻结的运动学代数；场公有化的材料动力学属外部。

### 1.42 `ScaleCompatibility.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `log_step_sq` / `log_step_linear` | theorem | $\Delta\ln E_n=p\ln(1+1/n)$ 的 $p=2$／$p=1$ 情形 | 对数代数 |
| `log_step_vanish` | theorem | 对数步长随 $n$ 严格递减 | 单调性 |
| `count_log_linear` | theorem | $\ln(N_0E^2)=\ln N_0+2\ln E$ | 计数坐标 |

**边界**：本文件只承载刻度相容性的对数代数；声子 DOS、$S=\ln\Gamma$ 的统计力学与 $v_\tau$ 动力学属外部。

### 1.43 `NodeClockCoord.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `global_coord_reading_equal` / `reading_diff_excludes_global` | theorem | 全局坐标⇒读数恒等；读数差非零⇒排除全局坐标 | no-go |
| `node_coord_depends_on_node` | theorem | $\tau_i'=\tau_i-\Delta_i$（节点索引） | 换元 |
| `node_coord_reconstructible` | theorem | $\tau_i=\tau_{i_0}+\mathcal H_{i_0i}$（可重构） | 代数 |
| `information_compression` / `two_readings_exclude_global` | theorem | 全局坐标压成一条；两读数不同排除全局 | 逻辑 |

**边界**：本文件只承载坐标选择的逻辑代数；残余公设（节点为基本单元）属诠释层。

### 1.44 `FourStageChain.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `Stage` / `four_stages_exhaustive` | 归纳＋theorem | 四步穷尽，无第五个"变负"构造器 | 结构 |
| `TurnedNegative` / `negative_drives_averaging` / `two_stages_to_crisis` | 定义＋theorem | 变负＝增长率追不上平均化率（驱动力）⇒ 平均化 ⇒ 平均量下降（危机化，第二阶段） | 代数 |
| `averaging_to_crisis` / `internal_oscillation_preserves_decrease` | theorem | ③→④延续；反趋势内化不推翻下降 | 代数 |
| `residual_oscillation` | theorem | 危机化含正残余波动（不等于相变） | 代数 |

**边界**：本文件只固化四步口径的逻辑代数；$\dot{\bar v}_\tau<0$ 的链内方程属外生，不冒充已推。

### 1.45 `ZeroPointVariance.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `nB_pos` / `factor_ge_one` / `sigma2_ge_zero` | theorem | $n_B>0$、$1+2n_B\ge1$、$\sigma^2(T)\ge\sigma_0^2$ | 不等式 |
| `coth_form` | theorem | $1+2/(e^x-1)=(e^x+1)/(e^x-1)$（QHO 恒等式） | 代数 |
| `high_temp_classical` | theorem | 高温 $n_B<1/x$ 的经典尺度界 | 指数不等式 |
| `zero_temp_factor` | theorem | 热因子为 1 ⇒ $\sigma^2=\sigma_0^2$（零点极限） | 代数 |

**边界**：本文件只承载零/热方差分解的代数；$\sigma_0^2$ 材料归一与 $p_{\rm pair}(T)$ 属外部。

### 1.46 `CriterionSufficiency.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `dDot3` | 定义 | 三点分化度变化率 $2\sum_{i<j}(\tau_i-\tau_j)(v_i-v_j)$ | 代数 |
| `three_point_counterexample` | theorem | $\tau=(1,-1,0)$、$v=(0,0,1)$：$\dot D=0$ 但 $v_1\ne v_3$ | 充分性否证 |
| `frozen_implies_stationary` | theorem | 全对冻结 ⇒ $\dot D=0$（必要方向） | 代数 |
| `necessary_not_sufficient` | theorem | 驻定不蕴含全对冻结（判否） | 逻辑 |

**边界**：本文件只承载判据充分性的代数反例；偶然项（`审-11`／`临-16`）属外部。

### 1.47 `AllZeroUnreachable.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `cob` / `kernel_shift_no_change` | 定义＋theorem | $c_{ij}=a_i-a_j$，核内平移不改变任何 $c_{ij}$ | 规范平凡 |
| `all_zero_iff_constant` | theorem | 全对归零 ⇔ $a$ 为常向量（核＝常向量） | 代数 |
| `uniform_all_equal_probability` / `prob_le_geometric` | theorem | $M/M^N=1/M^{N-1}$，$\le(1/2)^N$（指数衰减） | 离散概率 |

**边界**：本文件只承载归零不可达的代数与离散概率；连续分布测度论与 $a_i$ 材料分布属外部。

### 1.48 `ShapeCompatibilityCheck.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `min_three_le_*` / `min_three_mono_left` | theorem | $T_c=\min$ 的三上界与单调性 | 格结构 |
| `nB_strict_anti` / `thermal_factor_gt_one` | theorem | 热因子随 $T$ 升（$n_B$ 随 $x$ 降）、因子 $>1$ | 指数不等式 |
| `window_inverse_width` | theorem | 退相干窗口 $\gamma_*\sim1/\sigma$ 反比于宽度 | 代数 |
| `dome_min_at_crossing` / `min_bounded_by_crossing` | theorem | min 单峰的代数核心 | 格结构 |

**边界**：本文件只承载形状相容的格/代数核；材料归一与绝对 $T_c$ 属外部。

### 1.49 `FiniteModeReadout.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `rho_abs_ge_gamma` / `tail_term_bound` | theorem | $|\rho_n|\ge\gamma_n$、尾部单项界（截断误差） | 代数 |
| `tail_bound_two` / `truncation_error_decomp` | theorem | 三角不等式与截断分解的代数核 | 代数 |
| `weight_decreasing_in_rate` | theorem | 率越大权重越小（窗口单调） | 指数 |
| `nogo_two_modes` | theorem | 恒等焊接仍不可能（no-go 保持） | 代数 |

**边界**：本文件只承载有限模读出的代数；$\sigma_v^2\tau_g$／$N_*$ 与零点渐近属外部。

### 1.50 `V1Limits.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `bcs_ratio_check` | theorem | BCS 比在 (3,4) 的结构检查（比值外部给定，本环境无欧拉 γ 常量） | 外部口径 |
| `nB_upper_bound` / `thermal_factor_gt_one` | theorem | 高温 $n_B\le1/x$、热因子 $>1$（无反向符号） | 指数不等式 |
| `dimension_selection` | theorem | $d=2\iff d-2=0$（维度选择） | 代数 |

**边界**：本文件只承载 V1 的结构核；BCS 比值、材料归一属外部。

### 1.51 `AmplitudeGapEquation.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `weak_coupling_condition` | theorem | $\lambda>0\land\lambda<1$（弱耦合） | 条件 |
| `gap_from_tstar` | theorem | 由 (目标.2) $T^*$ 得 $\Delta=(2/r)k_BT^*$ | 代数 |
| `ratio_universal` | theorem | $2\Delta/k_BT^*=4/r$ 与材料无关 | 代数 |
| `amp_log_ratio` | theorem | $\omega_{\log}^{\rm amp}/\omega_D=e^{-1/3}>0$ | 指数 |

**边界**：本文件只承载 C5 的结构代数；欧拉 γ 值、$\lambda$／$\omega_D$ 材料值属外部。

### 1.52 `V2ElementDiagnostic.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `sector_gap_one_third` | theorem | $\log x-\log(xe^{-1/3})=1/3$（扇区结构） | 对数代数 |
| `lambda_pos_iff` / `lambda_lt_two` | theorem | 反解耦合的符号与量级判据 | 不等式 |
| `inverse_lambda` | theorem | $\lambda=1/\log(A\theta/T)$ 反解代数 | 代数 |

**边界**：本文件只承载 V2 诊断的代数；实测数据与 $\mu^*$ 属外部。

### 1.53 `BCSCoefficient.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `gap_ratio_independent_of_omega` | theorem | $2\Delta/k_BT^*$ 与前因子频率无关（形状） | 代数 |
| `prefactor_scale_factor` / `scale_factor_lt_one` | theorem | CQM/BCS 前因子差 $e^{-1/3}<1$（刻度） | 代数 |
| `sector_gap_prefactor_independent` | theorem | $\Delta(1/\lambda)=1/3$ 与常数前因子无关 | 对数代数 |

**边界**：本文件只承载口径核查的代数；BCS 系数文献值属外部。

### 1.54 `EliashbergRenorm.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `renorm_exponent_factor` | theorem | $e^{-(1+\lambda)/\lambda}=e^{-1/\lambda}e^{-1}$（重整化因子） | 指数代数 |
| `renorm_lowers` | theorem | 重整化严格压低 $T_c$ 一个 $e^{-1}$ | 不等式 |
| `mass_enhancement` / `_mono` | theorem | $Z=1+\lambda>1$ 且随耦合增 | 代数 |
| `gap_ratio_universal_in_lam` | theorem | 普适比与 $\lambda$ 无关（结构） | 代数 |

**边界**：本文件只承载质量增强的代数；$v_\tau$ 拖曳方程属待授权的接口。

### 1.55 `ZRenormWrite.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `ratio_e_decomp` | theorem | $e^{-7/6}=e^{-1}\cdot e^{-1/6}$（0.312 精确分解） | 指数代数 |
| `shape_neutral` | theorem | $Z$ 对 $T^\*$ 与 $\Delta$ 同因子 ⇒ gap ratio 不变 | 代数 |
| `tstar_renorm_factor` | theorem | 含重整化 $T^\*$ 是裸的 $e^{-1}$ 倍 | 指数代数 |
| `inverse_lambda_renorm` | theorem | 反解 $\log(P/T)=1/\lambda+1$ | 对数代数 |

**边界**：本文件只承载 Z 写入的代数核；材料定标与 $\mu^\ast$ 属外部。

### 1.56 `KarakozovPrefactor.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `cutoff_to_logmoment` | theorem | $e^{-1/2}=e^{-1/6}e^{-1/3}$（截断↔对数矩） | 指数代数 |
| `prefactor_eq` | theorem | $1.13e^{-1/2}\theta=1.13e^{-1/6}(e^{-1/3}\theta)$ | 代数 |
| `constant_prefactor_neutral` | theorem | 常数前因子不影响 gap ratio | 代数 |
| `inverse_lambda_shift` | theorem | 前因子重标定对反解的对数平移 | 对数代数 |

**边界**：本文件只承载 Karakozov 因子的代数换算；$\mu^\ast$ 材料值属外部。

### 1.57 `ForwardGapRatio.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `correction_nonneg` / `ratio_ge_bcs` | theorem | Mitrović 修正项非负、比值 ≥ BCS 3.53 | 对数不等式 |
| `x_from_theta` | theorem | $x=T_c/\omega_{\log}=e^{1/3}T_c/\theta_D$（(目标.3)） | 指数代数 |
| `log_argument` | theorem | $\ln$ 参数 $1/(2x)=\omega_{\ln}/(2T_c)$ | 代数 |

**边界**：本文件只承载正算验证的代数核；实验 gap ratio 与 $\mu^\ast$ 属外部。

### 1.58 `MuStarShape.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `mustar_pos` / `mustar_lt_mu` | theorem | $\mu^\ast>0$、$\mu^\ast<\mu$（推迟削弱库仑） | 有理不等式 |
| `mustar_mono` | theorem | $\mu^\ast$ 对 bare $\mu$ 单调增 | 交叉相乘 |
| `mustar_limit_form` | theorem | $\mu/(1+\mu L)=1/(1/\mu+L)$ | 代数 |
| `mustar_lt_limit` | theorem | $\mu^\ast<1/L$（绝热极限从下方趋近） | 不等价 |

**边界**：本文件只承载 Morel-Anderson $\mu^\ast$ 的形状核；$\mu,\epsilon_F$ 材料值属外部。

### 1.59 `IsotopeIntermediate.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `mustar_shift_exact` | theorem | M.1 精确差分 $\Delta\mu^\ast=-\mu^{\ast2}d/(1+\mu^\ast d)$ | 代数 |
| `mustar_decreases_with_mass` | theorem | 质量增 ⇒ $\mu^\ast$ 减 | 不等式 |
| `correction_pos` | theorem | Eliashberg 修正项 $C>0$ | 不等式 |
| `alpha_lt_half` / `alpha_in_range` | theorem | $\alpha<1/2$、$\alpha\in(0,1/2)$ | 线性 |
| `alpha_half_at_zero` | theorem | $\mu^\ast=0\Rightarrow\alpha=1/2$（CQM 端点） | 代数 |

**边界**：本文件只承载同位素中间值的代数核；$\mu^\ast$ 形状是链外成分（T10.3），材料值属外部。

### 1.60 `LoopHolonomySplit.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `cyclic_sum_sub_zero` | theorem | 周期序列 $\sum_{k<n}(f_{k+1}-f_k)=0$（望远镜核） | 只证差分和为零 |
| `telescoping_exp_prod` | theorem | 势差比值沿闭环乘积 $=1$ | 只证代数；不证明物理上是势 |
| `two_way_trivial` | theorem | $v(1-x^2)=v$ 且 $v\ne0$ 迫使 $x=0$ | 单边双向的平凡性 |
| `same_edge_product_lt_one` | theorem | $0<x<1$ 时 $(1-x)(1+x)<1$ | 代数 |
| `reverse_deficit_nonlinear` | theorem | $(1-x)(1-y)=1$ 的解是 $y=-x/(1-x)$，非线性 | 代数 |
| `asym_residual_nonpos` | theorem | $\tfrac12\ln(1-x^2)\le0$ | 代数 |
| `asym_residual_eq_zero_iff` | theorem | 残差为零当且仅当 $x=0$ | 代数 |

**边界**：本文件只承载"望远镜恒等式＋反对称残差"的代数核；不承载图论的闭环记账（哪些边组成 $C$）、BCC 数值输入本身、$\ell_{ij}$ 的物理识别，也不闭合 `审-1`／`M5`。

**导入**：精确导入 `Mathlib.Analysis.SpecialFunctions.Log.Basic`、`Mathlib.Analysis.SpecialFunctions.Exp`、`Mathlib.Algebra.BigOperators.Group.Finset.Basic`、`Mathlib.Tactic.Ring/Linarith/Positivity`；不 `import Mathlib`（理由见 §三）。

### 1.61 `FlatTriangulationDeficit.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `bcc_short_edge_flat` | theorem | $4\cdot\frac{\pi}{2}=2\pi$（短边角闭合） | 精确算术 |
| `bcc_long_edge_flat` | theorem | $3\cdot\frac{2\pi}{3}=2\pi$（长边角闭合） | 精确算术 |
| `deficit_vanishes_iff_ratio_one` | theorem | $\sqrt{1-\varepsilon/2\pi}=1\iff\varepsilon=0$ | 代数 |
| `flat_loop_product_one` | theorem | 全零亏角闭环乘积 $=1$（任意边数，归纳） | 代数 |
| `ratio_strict_anti` | theorem | $\varepsilon$ 增 ⇒ 键比值严格减 | 实分析 |
| `inverted_deficit` | theorem | $\prod=p\Rightarrow\varepsilon=2\pi(1-p^{2/3})$ | 实数幂 |
| `inverted_deficit_pos` | theorem | $p<1\Rightarrow\varepsilon>0$ | 反证 |

**边界**：本文件只承载"平直 ⇒ 零亏角 ⇒ 乘积一"与反解式的代数核；不承载三角化的组合记账、二面角的三角计算（在 Python），也不承载"任何其它 BCC 星形三角化都不能把 $\varepsilon$ 抬到 4.30 rad"这条几何陈述（在推导卡 §四 论证）。

### 1.62 `FLopeSlope.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `slope_from_first_order` | theorem | $\kappa\varepsilon=(-4\pi\kappa)\cdot(-\varepsilon/4\pi)$（一阶对照） | 代数 |
| `kappa_identity` | theorem | $4\pi v^2\cdot\frac{1}{4\pi v^2}=1$ | 代数 |
| `slope_unit_at_flat` | theorem | $(-4\pi)\cdot\frac{1}{4\pi}=-1$（平直斜率） | 代数 |
| `cubic_bound` | theorem | $\lvert r\rvert\le10,\ \lvert u\rvert\le\frac{1}{100}\Rightarrow\lvert r\rvert u^2\le\frac{1}{1000}$ | 不等式 |

**边界**：本文件只承载"一阶比例 ⇒ 斜率"的代数核；不承载 $\delta\ell\leftrightarrow(\Delta\varepsilon_i-\Delta\varepsilon_j)$ 的识别（那正是 `审-19`，且斜率在两读法下相同），不承载 $\lambda(\ell)$ 的对数展开，也不承载 $\sigma_\ell$ 的物理大小。

### 1.63 `TwoComponentDeficit.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `two_comp_variance_ge_node` | theorem | 键分量只**增加**节点部分的方差 | 代数 |
| `circ_ratio_zero_iff` | theorem | $r_{\rm circ}=0\iff$ 键分量消失 | 代数 |
| `circ_ratio_pos` | theorem | 正键幅 ⇒ 正 $r_{\rm circ}$ | 代数 |
| `keating_c11` / `keating_c12` | theorem | Keating 反解回代给 $c_{11}$、$c_{12}$ | 代数 |
| `prod_ge_fifth` | theorem | $0\le r\le1\Rightarrow\prod_Cr\ge\frac15>0.177$ | 实分析 |

**边界**：本文件只承载两分量方差的可加性、环流比判据与 Keating 反解的代数核；不证明 $\varepsilon$／$\ell$ 与键／节点几何量的识别（`审-18`／`审-19`），不证明零点标度的系数（`审-20`），也不证明弹性常数数据。

### 1.64 `ZeroPointScaling.lean`

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `harmonic_m_sqrt` | theorem | $m\sqrt{k/m}=\sqrt{km}$（标度恒等式） | 代数 |
| `harmonic_x2` | theorem | $\hbar/(2m\sqrt{k/m})=\hbar/(2\sqrt{km})$ | 代数 |
| `quarter_lt_one` | theorem | $0<a<1\Rightarrow a^{1/4}<1$ | 实分析 |
| `quarter_gt_self` | theorem | $0<a<1\Rightarrow a<a^{1/4}$（用错幂次会低估） | 实分析 |

**边界**：本文件只承载谐振子零点振幅的代数核；不承载刚度与 Keating $\alpha,\beta$ 的识别，不承载模式耦合（需对角化动力学矩阵，`审-20`），也不承载耦合比 $\alpha_u/\beta_u$ 的物理值。

## 二、验证命令与结果

```powershell
Set-Location "D:\WorkSpace\物理\CQMFormal\08 理论组织和形式化框架\04_Lean对接\Lean源码"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\ThermalArchitecture.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\A12Counterexample.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\A12Circulation.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\A12Matrix.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\PhaseConnection.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\A12Normality.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\CoherentThermalSplit.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\TemperatureBridge.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\TailOccupancy.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\PairCellScale.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\ModeCountTemperature.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\PhaseTolerance.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\BondGeometry.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\LandauAnchor.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\MemoryKernelWelding.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\GeometricForcing.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\M5Homogeneity.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\KappaFDerivation.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\TwoSectorOmegaLog.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\NormalModeCompleteness.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\DampingBridge.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\GammaSource.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\M8PhaseBoundary.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\CycleSpaceHalf.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\ClosureLedger.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\GenusCorrection.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\WeightQuantization.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\A4RootCharge.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\ThetaTerminal.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\FieldSuppression.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\AllPairsNormalization.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\SelfAveraging.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\FrozenCoboundary.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\DeficitDrive.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\PressureInvariance.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\ZeroPointShift.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\EffectiveCount.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\MarginalAllocation.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\CoexistenceWindow.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\LemmaAPremise.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\FrozenPremise.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\ScaleCompatibility.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\NodeClockCoord.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\FourStageChain.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\ZeroPointVariance.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\CriterionSufficiency.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\AllZeroUnreachable.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\ShapeCompatibilityCheck.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\FiniteModeReadout.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\V1Limits.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\AmplitudeGapEquation.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\V2ElementDiagnostic.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\BCSCoefficient.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\EliashbergRenorm.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\ZRenormWrite.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\KarakozovPrefactor.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\ForwardGapRatio.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\MuStarShape.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\IsotopeIntermediate.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\LoopHolonomySplit.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\FlatTriangulationDeficit.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\FLopeSlope.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\TwoComponentDeficit.lean"
& "D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe" env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\ZeroPointScaling.lean"
```

结果：本清单中六十四个文件均退出码 0，无警告。文件内无 `axiom`、`sorry`、`admit`、`native_decide`、`unsafe`。

> **实测注记（第 76 轮）**：在 Git Bash 下直接 `lake env lean <工程外的绝对路径>` 会报 `unknown module prefix 'Mathlib'`——`lake env` 未把 `.lake/packages/*/.lake/build/lib/lean` 注入 `LEAN_PATH`（沙箱同时拦截 `lake env bash`）。可复跑做法：`cd` 到 Lean 源码目录，先导出
> `LEAN_PATH=".lake/build/lib/lean;` + 各依赖包 `.lake/packages/<pkg>/.lake/build/lib/lean`（mathlib、batteries、aesop、Qq、proofwidgets、importGraph、LeanSearchClient、plausible），再 `lean <文件名>`。本轮 `LoopHolonomySplit.lean` 以该方式验证：**无输出（无警告）、退出码 0**；验证后副本已从 Lean 源码目录删除。

## 三、为什么不用 `import Mathlib`

主工程 `.lake` 的 `Mathlib` 构建缺少 `Mathlib.CategoryTheory.Category.Init` 的 `.olean`，直接 `import Mathlib` 会在未使用的范畴模块上失败。本文件只导入实际需要的：

- `Mathlib.Analysis.SpecialFunctions.Exp`
- `Mathlib.Order.Monotone.Basic`
- `Mathlib.Tactic.Linarith`
- `Mathlib.Tactic.GCongr`
- `Mathlib.Tactic.NormNum`
- `Mathlib.Tactic.FieldSimp`（`CoherentThermalSplit.lean` 的分母消去）
- `Mathlib.Analysis.SpecialFunctions.Pow.Real`、`Mathlib.Analysis.SpecialFunctions.Sqrt`、`Mathlib.Tactic.Ring`（`TemperatureBridge.lean` 的权重、平方根与代数重标）

这不是主库构建失败；主库 `lake build` 仍走既有 2902 jobs 路径。`A12Circulation.lean` 另导入 `Mathlib.Data.Matrix.Basic`、`Mathlib.Tactic.Ring`，同样使用精确导入。`A12Normality.lean` 只导入 `Mathlib.Data.Real.Basic`、`Mathlib.Data.Matrix.Basic`、`Mathlib.Tactic.NoncommRing`；未使用 `Mathlib.Data.Matrix.Notation`（该 `.olean` 在当前 `.lake` 缺失）。`TailOccupancy.lean` 只导入 `Mathlib.Data.Real.Basic`、`Mathlib.Order.Monotone.Basic`、`Mathlib.Tactic.Linarith`、`Mathlib.Tactic.Ring`、`Mathlib.Tactic.FieldSimp`。`PairCellScale.lean` 只导入 `Mathlib.Data.Real.Basic`、`Mathlib.Tactic.Linarith`、`Mathlib.Tactic.NormNum`。`ModeCountTemperature.lean` 只导入 `Mathlib.Data.Real.Basic`、`Mathlib.Tactic.FieldSimp`、`Mathlib.Tactic.Ring`。

## 四、未承载

- Debye 积分恒等式 (4.4)–(4.7)：在 Python 数值核，不在 Lean；若要进 Lean，需另写测度与积分接口。
- $\sigma_v^2\propto\Theta$ 的线性化：在推导工作台 (3.3) 是条件严格，Lean 只把 `sigmaV2` 当抽象单调函数。
- $\lambda$ 的物理绝对值、$\Gamma_n$ 的数值、$T_c$ 的存在性：均未承载。
- A12 的物理 $\mathcal C$ 族、$f$ 显式、环 9 方差口径：均未承载；`A12Counterexample.lean` 只否定“全局零和 ⇒ 逐行零和”，`A12Circulation.lean` 给矩阵层存在性与“单函数 $f$ 下任意 $N$ 不存在”的一般 no-go；`A12Matrix.lean` 给边量矩阵分支的代数存在性、非梯度性、梯度扇区 no-go，以及 `rowZero_decomp_gradient_zero`（逐样本行零会杀死梯度方差）；`A12Normality.lean` 给任意奇 \(f\) 的 \(C=I+B\) 正规性。`C3circ`／`C4circ` 都不是节点差 $f$ 生成，但都是边量 $\lambda$ 生成的纯环流候选。
- H 非梯度化（已否决）不承载；相位连接的**代数分离**由 `PhaseConnection.lean` 承载；相位连接动力学、环 9 方差口径未承载。正规性已由 `A12Normality.lean` 承载；`rowZero_decomp_gradient_zero` 承载 M／S 分叉的 Lean 部分；原先“非正规 Schur”判断删除。
- `CoherentThermalSplit.lean` 只承载单模 `Vtot = Z + Vinc`、`Vcoh` 反单调、`Vinc` 单调与单模乘积恒等式；不承载 Debye 积分 (9C.13)，也不证明 \(V_{\rm coh}\) 就是 DM.5 的物理对象。
- `TemperatureBridge.lean` 只承载均匀重标与单调读出方向；不承载 Debye 积分 (10B.1)、低温 \(\pi^2/3\) 系数或 \(T_{\rm BKT}\) 的存在唯一性。
- `TailOccupancy.lean` 只承载单调 CDF 的尾方向；不承载 chi-square 分布、\(n_{\rm cell}\)、\(\sigma_c\)、\(t\) 的物理值，也不承载 \(p_{\rm sync}=p_c\) 与 \(T_c\) 的等价性。
- `PairCellScale.lean` 只承载“阈值平均 ≠ 平均阈值”的两读数代数反例；不证明物理场非均匀，也不证明空间域读法与局域模读法的取舍。
- `ModeCountTemperature.lean` 只承载 \((1-bt)/(1-at)\) 的领头系数 \(a-b\)；不证明 \(N_{\rm eff}(T)\)、\(b\) 的物理值，也不证明 chi-square 尾展开。
- `审-10`、`审-3`、`审-4`、`M8`：仍未完全闭合；`审-3` 只闭合方向，概率分布与 \(p_c\) 等价性仍开放。
- `ZeroPointScaling.lean` 只承载零点的 $k^{-1/4}$ 标度与 $a<a^{1/4}$ 的代数核；不证明该幂次在**耦合**晶格中仍成立（那是 `审-20` 的开放部分），也不证明两分量振幅之比。
- `TwoComponentDeficit.lean` 只承载两分量方差可加、环流比判据与 Keating 反解；不证明 $c_{12}>0$ ⇒ $r_{\rm circ}<1$（这是 Keating 的代数事实，在推导卡 §四 (8B.10a) 给出），也不证明 $r_{\rm circ}$ 的精确值。
- `FLopeSlope.lean` 只承载一阶比例与斜率的代数核；不证明 $f$ 的完整形式（高阶 $d$ 未给），不证明 $\kappa_f$ 的 FG 来源（`审-2` 的条件仍在）。
- `FlatTriangulationDeficit.lean` 只承载平直三角化的角闭合与反解代数核；不证明 BCC 的 Delaunay 三角化唯一（这是标准几何结论），不证明二面角数值（在 Python），也不证明 06 三个数必然错（只证明它们不能来自 (3.1) 的正则赋值）。
- `LoopHolonomySplit.lean` 只承载望远镜恒等式与反对称残差的代数核；不证明 $r_{ij}$ 与 $v_\tau$ 的物理分层是对的（这是**读法判定**，理由在推导卡 §三–§五），不证明 BCC 三环数值，也不证明 `C1=1` 在具体材料中可解。
- `BoundaryLayerDeficit.lean` 只承载边界分层的代数核：$\varepsilon_k=(4-k)\pi/2$、四个特殊比值 $1,\sqrt3/2,1/\sqrt2,1/2$、三环平方 $1/32$、非平直压低与全平直闭环 $=1$；不证明哪条边在凸包面上（组合记账在 Python），不证明二面角数值（Python），也不把"三值属读数层"这一**层级判定**形式化（它在推导卡 §五与决策记录里）。

### `SyncLockBridge.lean`（第 149 轮，R-158）

| 名称 | 类型 | 内容 | 边界 |
|:---|:---|:---|:---|
| `pSync` | def | $p_{\rm sync}=p_{\rm pair}(1-y)$ | 边事件分解接口，不声明两对象同一 |
| `tEff` | def | $t=1+\ln(1-y)/\ln p$ | 定义式，不含 $E_c$ |
| `neff2` | def | 二键格胞 $n_{\rm cell}=2/(1+\rho^2)$ | 只作 $z=2$ 代表 |
| `sync_nonneg` / `sync_le_pair` / `sync_le_one` | theorem | $0\le y\le1$、$0\le p\le1$ ⇒ $0\le p(1-y)\le p\le1$ | 二阶段序的代数核 |
| `exponent_identity` | theorem | $p^{1+\ln(1-y)/\ln p}=p(1-y)$ | 需 $0<p$、$p\ne1$、$0<1-y$ |
| `tEff_zero` | theorem | $t_{\rm eff}(p,0)=1$ | 零温极限 |
| `tEff_gt_one` | theorem | $0<p<1$、$0<y<1$ ⇒ $1<t_{\rm eff}$ | 有限温严格大于 1 |
| `tEff_mono` | theorem | $y_1\le y_2$ ⇒ $t_{\rm eff}(y_1)\le t_{\rm eff}(y_2)$ | 需 $0<1-y_2$ |
| `pair_threshold_ge` | theorem | $p_c\le p_c/(1-y)$ | 阈值抬升 |
| `threshold_identity` | theorem | $(p_c/(1-y))^{t_{\rm eff}(p_c/(1-y),y)}=p_c$ | 需 $0<y<1-p_c$ 排除 $p=1$ |
| `neff2_ge_one` / `neff2_le_two` | theorem | $\rho^2\le1$ ⇒ $1\le2/(1+\rho^2)\le2$ | $z=2$ 代表；一般 $z$ 在推导卡与 Python |

**边界**：不证明涡旋逸度的第一性形式（$E_c$ 为 XY 外部核能），不给 $p_c$、$y$、$\nu$、$m$ 的材料值；一般 $z$ 的 $n_{\rm cell}\in[1,z]$ 由 $\sum_{ee'}\rho_{ee'}^2\ge z$ 给出，Lean 只承载 $z=2$ 与全部标量代数。不闭合任何编号，`审-4`／`审-6` 状态不动。

## 五、后续并入主库的条件

1. 温度角色分层先在主链 `CQM_探索_推导链.md` 写成正式条目；
2. 取得链内对 $\Theta\to\sigma_v^2$ 的明确映射（不是线性化假设）；
3. 与 `Stage1`／`Stage9` 的现有 `boseOccupancy`、`dephasingRate` 命名不冲突；
4. 全量 `lake build`、`check_consistency`、`check_provenance`、`consistency_probe` 通过后，才并入主库计数。

---

## 第 185 轮（2026-11-25）：Spec v12 与 `Ring15LockStiff`

- `Ring15Spec.lean` → **v12**：删 `epsVarFromTheta`／`TargetPropVarBridge`；增 `fugOfK`、`TargetPropFugStiff`、`TargetPropFugBound`、`TargetPropUpsLower`。
- `Ring15LockStiff.lean`：三条定理（`targetPropFugStiff`／`targetPropFugBound`／`targetPropUpsLower`），只 `import Ring15Spec`，逐条 `unfold fugOfK`。
- `Ring15LockBridge.lean` 已删除（随 v11 退役，见 `DISCARD.md` 第 185 轮）。
- `a_gate.ps1`：`$mods` 十二项（…`Ring15LockRatio`, `Ring15LockStiff`），20 条 `#print axioms`、15 条 `#check`；末次实跑 PASS（241 文件 0 命中，exit 0）。

## 第 186 轮（2026-11-25）：Spec v13 与 `Ring15LockT`

- `Ring15Spec.lean` → **v13**：增 `TargetPropTEffMMono`、`TargetPropTEffMGeOne`（不改既有定义）。
- `Ring15LockT.lean`：两条定理（`targetPropTEffMMono`／`targetPropTEffMGeOne`）＋私有差商引理 `tEffM_sub`，只 `import Ring15Spec`，逐条 `unfold tEffM`。
- `a_gate.ps1`：`$mods` 十三项（…`Ring15LockRatio`, `Ring15LockStiff`, `Ring15LockT`），22 条 `#print axioms`、17 条 `#check`；末次实跑 PASS（242 文件 0 命中，exit 0）。

## 第 187 轮（2026-11-25）：Spec v14 与 `Ring15LockThr`

- `Ring15Spec.lean` → **v14**：增 `pPairThr`、`TargetPropThrLog`、`TargetPropThrRpow`。
- `Ring15LockThr.lean`：两条定理（`targetPropThrLog`／`targetPropThrRpow`）＋私有 `log_pPairThr`，只 `import Ring15Spec`。
- `a_gate.ps1`：`$mods` 十四项，24 条 `#print axioms`、19 条 `#check`；末次实跑 PASS（243 文件 0 命中，exit 0）。

## 第 188 轮（2026-11-25）：Spec v15 与 `Ring15LockR`

- `Ring15Spec.lean` → **v15**：增 `rOfW alphaV w w' eps := 2*alphaV*w/(3*eps*|w'|)`、`sOfLock C1 aLam r := 2/(C1*(aLam-r))`、`TargetPropROfEps`、`TargetPropSFail`。命名注：`aλ` 不能作标识符（`λ` 是 lambda 关键字），故用 `aLam`。
- `Ring15LockR.lean`：两条定理（`targetPropROfEps`／`targetPropSFail`）＋私有 `rOfW_eq`（化 $k/\epsilon$ 形），只 `import Ring15Spec`。
- `a_gate.ps1`：`$mods` 十五项，26 条 `#print axioms`、21 条 `#check`；末次实跑 `A 闸 PASS（限环 15 十五模块 v15）`（244 文件 0 命中，exit 0）。
- 过程坑：`div_lt_div_iff` 在 Mathlib 不存在（只有 Rat 版弃用别名），用 `div_lt_div_iff₀`；`le_of_not_lt` 不存在，`not_lt.mp` 已给 `≤`。

### 第 189 轮（$\\Phi$ 的授权域）

- `Ring15Spec.lean` → **v16**：增 `phiBkt T U0 w := 2*T/(π*U0*w)`、`phiMin T U0 w yc := (2*T/(π^2*U0*w))*log(2π/yc)`、`TargetPropPhiMono`、`TargetPropPhiBktVal`、`TargetPropPhiMinEq`、`TargetPropPhiConflict`；不改既有定义。
- `Ring15LockPhi.lean`：四条定理（`targetPropPhiMono`／`targetPropPhiBktVal`／`targetPropPhiMinEq`／`targetPropPhiConflict`）＋私有 `bkt_K`，只 `import Ring15Spec`。
- `a_gate.ps1`：`$mods` 十六项，30 条 `#print axioms`、25 条 `#check`；末次实跑 `A 闸 PASS（限环 15 十六模块 v16）`（245 文件 0 命中，exit 0）。
- 过程坑：`div_le_div_of_nonneg_left`／`div_lt_div_of_pos_left` 参数形状与本形不合（改 `mul_le_mul_of_nonneg_left` 等＋`linarith`）；`field_simp` 常已闭合，后面再跟 `ring` 报 "No goals to be solved"（189 轮四处踩到）。

### 第 190 轮（$w(T)$ 的积分定义授权）

- `Ring15Spec.lean` → **v17**：新增基线 import `Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic`、`Mathlib.Analysis.Complex.Trigonometric`，`open MeasureTheory`／`open scoped Interval`；增 `wGap T := ∫ u in 0..1, 2*u*Real.tanh (u/(2*T))`、`TargetPropWGapPos`／`TargetPropWGapAnti`／`TargetPropWGapLeOne`。
- `Ring15LockW.lean`：三条定理（`targetPropWGapPos`／`targetPropWGapAnti`／`targetPropWGapLeOne`）＋私有引理（`continuous_tanh`、`hasDerivAt_tanh`、`tanh_strictMono`、`tanh_pos_of_pos`、`tanh_nonneg_of_nonneg`、`tanh_le_tanh`、`cont_integrand`），只 `import Ring15Spec`。
- `a_gate.ps1`：`$mods` 十七项，33 条 `#print axioms`、31 条 `#check`；末次实跑 `A 闸 PASS（限环 15 十七模块 v17）`（246 文件 0 命中，exit 0）。
- 过程坑：`integral_eq_sub_of_hasDerivAt` 只有 `(hderiv) (hint)` 两参（别多传 `ContinuousOn`）；`2*x ≤ 2*x*1` 形状要用 `simpa` 收尾；交互式命令里 `$PSScriptRoot` 为空，LEAN_PATH 须写绝对路径。
- Mathlib 名字：`Real.tanh_eq_sinh_div_cosh`、`Real.hasDerivAt_sinh`／`Real.hasDerivAt_cosh`、`HasDerivAt.div`、`strictMono_of_deriv_pos`、`intervalIntegral.integral_mono_on`／`integral_pos`／`integral_eq_sub_of_hasDerivAt`、`Real.tanh_lt_one`／`tanh_zero`；`Real.tanh` 在 `Mathlib.Analysis.Complex.Trigonometric`。


### 第 191 轮（$s$ 的同名判否）

- `Ring15Spec.lean` → **v18**：增 `TargetPropSolSurj`（$s_{\rm sol}$ 正向取遍 $(0,\infty)$）、`TargetPropSolNeg`（另一分支取负）；无新 import。
- `Ring15LockS.lean`：两条定理（`targetPropSolSurj`／`targetPropSolNeg`），只 `import Ring15Spec`。
- `a_gate.ps1`：`$mods` 十八项，35 条 `#print axioms`、33 条 `#check`；末次实跑 `A 闸 PASS（限环 15 十八模块 v18）`（247 文件 0 命中，exit 0）。
- 判否内容：$s_{\rm rep}$（表示权，$\frac12\mathbb Z$，$\theta=s\ell$、$\alpha=-4\pi s$）与 $s_{\rm sol}$（可解性因子，$2/[C(a\lambda-r)]$，连续可正可负）不是同一对象；整性只能加载到前者。


### 第 192 轮（$w$ 的严格单调）

- `Ring15Spec.lean` → **v19**：增 `TargetPropWGapStrictAnti`（$0<T_1<T_2\Rightarrow w(T_2)<w(T_1)$）；无新 import。
- `Ring15LockWStr.lean`：一条定理 `targetPropWGapStrictAnti`（复用 190 轮的四个私有引理），只 `import Ring15Spec`。
- `a_gate.ps1`：`$mods` 十九项，36 条 `#print axioms`、34 条 `#check`；末次实跑 `A 闸 PASS（限环 15 十九模块 v19）`（exit 0）。
- 路线：`integral_mono_on`（逐点 $\le$）→ `integral_pos`（差值在 $u=1$ 处 $>0$）→ `integral_sub`（差积分＝积分差）→ `simp only [sub_eq_add_neg]` ＋ `linarith`。
- 过程坑（三条，均已修正）：`integral_sub` 须显式 `(μ := volume)` 并命名 `f`、`g`；返回式右端 `(∫f) - ∫g` 与目标 `∫f - ∫g` 是两个原子，须先 `sub_eq_add_neg` 归一；多行 `have h : (∫ u in (0:ℝ)..1,` 会被当绑定列表，必须单行。Mathlib **无** `integral_lt_integral_of_le_of_lt` 一类严格性机器。
- 判定：G-190b 收口；186 的 $t$ 方向可用上严格性，G-186 降为"待复合"；G-190a／G-190c 不变。


### 第 193 轮（$w$ 的严格减沿 $T\to K\to y\to t$）

- `Ring15Spec.lean` → **v20**：增 `yOfT`（$y$ 律显式定义）与 `TargetPropKStrictAnti`／`TargetPropYStrictMono`／`TargetPropTStrictMono`；无新 import。
- `Ring15LockTStrict.lean`：三条定理（+ 私有的 $w$ 严格性重证、`fugOfK_strictAnti`／`fugOfK_pos`／`tEffM_sub`），只 `import Ring15Spec`。
- `a_gate.ps1`：`$mods` 二十项，39 条 `#print axioms`、37 条 `#check`；末次实跑 `A 闸 PASS（限环 15 二十模块 v20）`（exit 0）。
- 写法坑：`TargetProp*` 是 `def : Prop`，套用其证明须命名参数 `(ups0 := …) (T1 := …) (T2 := …)`，否则首参被当 `ups0 : ℝ`。
- 判定：$K$ 严格减、$y$ 严格增、$t$ 严格增（$p$ 固定）；G-186 通道收口，新增 G-186p（$p_{\rm pair}(T)$ 通道缺 $F_\nu$ 定义授权）。

### 第 194 轮（$t$ 的两通道方向）

- `Ring15Spec.lean` → **v21**：增 `TargetPropTEffMPMono`（$t$ 对 $p$ 严格增）与 `TargetPropTChanSplit`（$\Delta t$ 的 $y$ 项 $>0$、$p$ 项 $<0$ 的反号分解，两条符号不等式作为合取项）；无新 import。
- `Ring15LockTChan.lean`：两条定理（+ 私有 `tEffM_diff_p`／`tEffM_split`），只 `import Ring15Spec`。
- `a_gate.ps1`：`$mods` 二十一项，41 条 `#print axioms`、39 条 `#check`；末次实跑 `A 闸 PASS（限环 15 二十一模块 v21）`——21/21 编译 ok、axioms 全为 `{propext, Classical.choice, Quot.sound}`、token 扫描 250 文件 0 命中、exit 0。
- 写法坑（两条）：`field_simp` 清分母须显式给 $\ln p_1\ne0$、$\ln p_2\ne0$（`ne_of_lt` 由 $\ln p<0$ 供），否则 `ring` 在 `(Real.log p)⁻¹` 原子前止步；`have := Real.log_lt_log …` 的匿名 `this` 在 `linarith` 里不稳，改命名或写成 `linarith [Real.log_lt_log …]`。
- 判定：$p_{\rm pair}$ 随 $T$ 降、$t$ 对 $p$ 增 ⇒ $p$ 通道压 $t$，与 $y$ 通道反号；193 的"等 $F_\nu$ 即可复合"作废，新增 **G-186c**（$t$ 复合的净方向须主导项闸），G-186p 方向收口、余 χ² 尾定义授权归乙类。

### 第 195 轮（G-186c 条件式主导项闸）

- `Ring15Spec.lean` → **v22**：增 `TargetPropTChanDominate`（充分：$\delta_1+\delta_2>0\Rightarrow t$ 增）与 `TargetPropTChanCriterion`（充要：$\Delta t>0\iff\delta_1+\delta_2>0$）；无新 import。
- `Ring15LockTDom.lean`：两条定理（+ 私有 `tEffM_split`／`one_le_nat_cast_pos`），只 `import Ring15Spec`。
- `a_gate.ps1`：`$mods` 二十二项，43 条 `#print axioms`、41 条 `#check`；实跑 `A 闸 PASS（限环 15 二十二模块 v22）`——22/22 编译 ok、axioms 白名单、251 文件 token 0 命中、exit 0。
- 写法坑：`div_pos_iff` 的第二支不能直接丢弃（会证出对 $N<0$ 也成立的假判据）；`absurd hN hNneg` 类型不匹配，须 `exact absurd hNneg (not_lt.mpr (le_of_lt hN))`。
- 判定：$\Delta t$ 符号只由 $\delta_1+\delta_2$ 决定；G-186c 判据部分收口，无条件净方向留作域核（$\rho<1$，非证明）。

### 第 196 轮（$w$ 的导数表示 G-190c）

- `Ring15Spec.lean` → **v23**：增 `sechSq`（$1/\cosh^2$）、`wGapDeriv`（$-\frac{1}{T^2}\int_0^1u^2\mathrm{sech}^2\frac{u}{2T}du$）、`TargetPropWGapDeriv`（$\forall T>0$，`HasDerivAt wGap (wGapDeriv T) T`）、`TargetPropWGapDerivNeg`（$w'<0$）；无新 import（`HasDerivAt`／`nhds` 已在基线内）。
- `Ring15LockWD.lean`：两条定理（+ 私有 `continuous_tanh`／`hasDerivAt_tanh'`／`cont_F`／`cont_F'`／`cont_sechSq`／`sechSq_pos`／`sechSq_le_one`／`deriv_F`），`import Ring15Spec` ＋ `ParametricIntervalIntegral`／`Deriv.Inv`／`Trigonometric.DerivHyp` 三条基线模块。
- `a_gate.ps1`：`$mods` 二十三项，45 条 `#print axioms`、43 条 `#check`；实跑 `A 闸 PASS（限环 15 二十三模块 v23）`——23/23 编译 ok、axioms 白名单、252 文件 token 0 命中、exit 0。
- 写法坑（四条）：`𝓝` 在该 import 基线下不可用（写 `nhds`）；`t ∈ Ι 0 1` 是 `min/max` 形，须先 `rw [Set.uIoc_of_le (by norm_num)]`；有界性目标是 beta-未归约形，须 `show` 后才可 `rw`；`HasDerivAt.comp` 给 `∘` 形，须 `simpa [Function.comp]`。
- 判定：**G-190c 收口**（恒等式＋符号均进链，$|w'|=-w'$ 可用）；但符号**不能**由控制函数范数不等式代替（它对 $\pm F'$ 同真），故单立 `TargetPropWGapDerivNeg`。188 的形状判据仍缺。

### 第 197 轮（$w$ 的分部积分恒等式与形状项分解 G-188a）

- `Ring15Spec.lean` → **v24**：增 `TargetPropWGapIbp`（$w=\tanh\frac{1}{2T}+\frac T2w'$）、`TargetPropShapeSplit`（形状项＝端点商−半温）、`TargetPropShapeEnd`（$\frac T2|w'|=\tanh\frac{1}{2T}-w$）、`TargetPropShapeEndGt`（端点严格高于平均）；无新 import。
- `Ring15LockIbp.lean`：四条定理（+ 私有 `continuous_tanh`／`hasDerivAt_tanh'`／`cont_sechSq`／`cont_A`／`cont_B`），`import Ring15Spec`＋`Ring15LockWD`＋`Trigonometric.DerivHyp`＋`IntervalIntegral.FundThmCalculus`。
- `a_gate.ps1`：`$mods` 二十四项，49 条 `#print axioms`、47 条 `#check`；实跑 `A 闸 PASS（限环 15 二十四模块 v24）`——24/24 编译 ok、axioms 白名单、254 文件 token 0 命中、exit 0。
- 写法坑（六条）：`ne_of_lt hT` 给的是 $0\ne T$（要 `ne_of_gt`）；`integral_const_mul` 常数参数名是 `r` 且 `μ` 须显式；FTC 引理须显式 import `FundThmCalculus`；`Continuous` 括号少一层会让 `exact` 吞掉下一行；`2*u*tanh` 与 `2*(u*tanh)` 对齐须 `rw [← hf]`；形状项 `field_simp` 须显式给 `wGapDeriv T ≠ 0`。
- 判定：**G-188a 收口**（形状项分解、端点亏损、端点正性进链）；G-188 拆出 **G-188b**（$w''$ 的链内表示与形状项极小编址）。最易跑偏处是 `|w'|` 的符号翻转（`abs_of_neg`），故正性单列一命题。

### 第 198 轮（$w''$ 的链内表示与形状项导数 G-188b 第一步）

- `Ring15Spec.lean` → **v25**：增 `wGapDeriv2 T := -(2/T)*wGapDeriv T - (1/T^4)*∫_0^1u^3*sechSq(u/(2T))*tanh(u/(2T))`、`shapeDeriv T := (wGap T*wGapDeriv2 T - wGapDeriv T^2)/wGapDeriv T^2`、`TargetPropWGapDeriv2`（$\forall T>0$, `HasDerivAt wGapDeriv (wGapDeriv2 T) T`）、`TargetPropShapeDeriv`（$\forall T>0$, `HasDerivAt (fun T => wGap T/|wGapDeriv T|) (shapeDeriv T) T`）；无新 import。
- `Ring15LockWD2.lean`：两条定理（+ 私有 `continuous_tanh`／`cont_sechSq`／`sechSq_pos`／`sechSq_le_one`／`tanh_pos_of_pos`／`cont_F`／`cont_F'`／`deriv_F`），`import Ring15Spec`＋`Ring15LockWD`＋`ParametricIntervalIntegral`＋`Trigonometric.DerivHyp`。
- `a_gate.ps1`：`$mods` 二十五项，51 条 `#print axioms`、46 条 `#check`；实跑 `A 闸 PASS（限环 15 二十五模块 v25）`——25/25 编译 ok、axioms 白名单、257 文件 token 0 命中、exit 0。
- 写法坑（五条）：$\cosh$ 链式导数须乘内层 $-\frac{t}{2x^2}$（漏则差 $-2x^2$）；`cont_F'` 少一层括号会吞行；`field_simp` 常直接闭合目标（后接 `ring` 报 `No goals`，本轮五处）；`HasDerivAt (-fun x => (x^2)⁻¹)` 与 `fun x => -(1/x^2)` 差 `one_div`（`simpa [one_div]`）；`filter_upwards [Ioo_mem_nhds …]` 端点成元变量（显式 `show Set.Ioo (0:ℝ) (2*T) ∈ nhds T from …`）。
- 判定：**G-188b 第一步完成、未收口**——$w''$ 与 $S'$ 的结构进链；$w''>0$、$S'$ 分段符号、极小 $T_{\min}$ 编址**未证**。最易跑偏处：`hBval` 的 $-T^2$ 因子（由定义 `field_simp` 自证、符号由定义给出），故判定义式。

### 第 199 轮（$w''$ 的端点闭式与条件式符号判据 G-188b-2）

- `Ring15Spec.lean` → **v26**：增 `wGapDeriv2Alt T := wGapDeriv T/T + sechSq(1/(2*T))/T^3`、`TargetPropWGapDeriv2Alt`（$\forall T>0$, `wGapDeriv2 T = wGapDeriv2Alt T`）、`TargetPropWGapDeriv2Pos`（$\forall T>0$, `T^2*|wGapDeriv T| < sechSq (1/(2*T)) → 0 < wGapDeriv2 T`）、`TargetPropShapeDerivSign`（$\forall T>0$, `shapeDeriv T < 0 ↔ wGap T*wGapDeriv2 T < (wGapDeriv T)^2`）；无新 import。
- `Ring15LockWD3.lean`：三条定理（+ 私有 `continuous_tanh`／`cont_sechSq`／`hasDerivAt_tanh'`／`hasDerivAt_tanh_inv`），`import Ring15Spec`＋`Ring15LockWD`＋`Ring15LockWD2`＋`Ring15LockIbp`＋`Deriv.Inv`＋`Trigonometric.DerivHyp`。
- 证法要点：`hAlt` 由 197 恒等式 $w=\tanh\frac{1}{2T}+\frac T2w'$ 逐项求导，与 v25 的 `HasDerivAt wGapDeriv` 经 `HasDerivAt.unique` 得同值；`hPos` 由 `lt_div_iff₀` 与 $w'=-|w'|$ 化为 $T^2w'+\mathrm{sech}^2>0$；`hSign` 由 `div_lt_iff₀` 化为 $w\,w''<(w')^2$。
- `a_gate.ps1`：`$mods` 二十六项，54 条 `#print axioms`、49 条 `#check`；实跑 `A 闸 PASS（限环 15 二十六模块 v26）`——26/26 编译 ok、axioms 白名单、256 文件 token 0 命中、exit 0。
- 写法坑（五条）：`Spec.TargetPropWGapIbp` 是 `def … : Prop`，须 import `Ring15LockIbp` 取定理（不能当函数套用）；`HasDerivAt.congr_of_eventuallyEq` 方向反须 `.symm`；`field_simp` 已闭合后多写 `ring` 报 `No goals`；`congrArg` 后 beta-项须先 `simp only [] at h`；在 `|w'|` 内部 `rw` 会得 $|-|w'||$，须 `congrArg (fun x => T^2*x)`，`pow_pos` 与 $w'^2$ 差 `sq_abs`。
- 判定：**G-188b 第二步只完成判据层**；**无条件凸性不成立**（判据比仅在 $T\gtrsim0.2555$ 小于 1），故 `TargetPropWGapDeriv2Pos` 写成带前提的条件式；$S'$ 分段符号与极小 $T_{\min}$ 编址**未证**。最易跑偏处：`hwabs` 在绝对值内部改动（句法仍对、被改的宿主换掉），本轮用 `congrArg` 限定位置。

### 第 200 轮（形状比与判据比：$S'$ 符号的比值判据 G-188b-2 第二步）

- `Ring15Spec.lean` → **v27**：增 `shapePhi T := wGap T/Real.tanh(1/(2*T))`、`ratioR T := T^2*|wGapDeriv T|/sechSq(1/(2*T))`、`TargetPropShapeSignRatio`（$\forall T>0$, `shapeDeriv T < 0 ↔ shapePhi T*(1+ratioR T) < 2*ratioR T`）、`TargetPropShapeNegOfRatioGeOne`（$\forall T>0$, `1 ≤ ratioR T → shapeDeriv T < 0`）；无新 import。
- `Ring15LockWD4.lean`：两条定理（+ 私有 `tanhPos`／`sechSqPos`／`wSub` 恒等式），`import Ring15Spec`＋`Ring15LockWD`＋`Ring15LockWD2`＋`Ring15LockWD3`＋`Ring15LockIbp`。
- 证法要点：`wSub` 用 197 的端点亏损 $Ta=2\tanh\frac{1}{2T}(1-\Phi)$、v26 端点闭式、v23 的 $w'<0$，把 $w\,w''-(w')^2$ 整块换成 $\tanh\cdot\mathrm{sech}^2[\Phi(1+r)-2r]/T^3$；比值判据由该恒等式＋`TargetPropShapeDerivSign` 合成；$r\ge1$ 段由 $\Phi<1$（`div_lt_one`＋`TargetPropShapeEndGt`）与 $1+r\le2r$ 给出。
- `a_gate.ps1`：`$mods` 二十七项，56 条 `#print axioms`、51 条 `#check`；实跑 `A 闸 PASS（限环 15 二十七模块 v27）`——27/27 编译 ok、axioms 白名单、256 文件 token 0 命中、错误流为空。
- 写法坑（四条）：此基线无 `Real.tanh_pos`／`Real.sinh_pos_of_pos`（用 `Real.sinh_pos_iff`＋`div_pos`）；`set` 的 $a$ 会被 `field_simp` 展开（改用 `div_mul_cancel₀` 给 $rS=T^2a$）；`rw [haT]` 后 `unfold ratioR`＋`rw [← ha]` 会漏掉新引入的 $a$（补一次 `rw [haT]`）；`push_neg` 弃用，`push Not` 后须 `linarith` 转形。
- 判定：**G-188b-2 判据层闭合（换元完成）**，$r\ge1$ 段 $S'<0$ 无条件；$r<1$ 段与 $T>0.3438$ 的 $S'>0$ **未证**。最易跑偏处：`wSub` 的 `field_simp` 把 $r$ 的定义式化掉（恒等式仍成立但不含 $r$ 语义），故显式保留 $rS=T^2a$。

### 第 201 轮（$r$ 的 $\Phi$ 闭式与判据一元化 G-188b-2f）

- `Ring15Spec.lean` → **v28**：增 `shapeH T := Real.tanh (1/(2*T))`、`TargetPropRatioPhiForm`（$\forall T>0$，`ratioR T = 2*T*shapeH T*(1-shapePhi T)/(1-shapeH T^2)`）、`shapeG T := 2*T*shapeH T*(1-shapePhi T)*(2-shapePhi T) - shapePhi T*(1-shapeH T^2)`、`TargetPropShapeSignUnary`（$\forall T>0$，`shapeDeriv T < 0 ↔ 0 < shapeG T`）；无新 import。
- `Ring15LockUnary.lean`：两条定理（＋私有 `tanhPos`／`sechSq_eq_one_sub_tanh_sq`／`ratioCriterion`），`import Ring15Spec`＋`Ring15LockWD`＋`Ring15LockWD2`＋`Ring15LockWD3`＋`Ring15LockWD4`＋`Ring15LockIbp`。
- 证法要点：闭式的分子由 197 端点亏损 $T|w'|=2h(1-\Phi)$ 经 `nlinarith` 推到 $T^2|w'|=2Th(1-\Phi)$，分母由勾股恒等式 $\mathrm{sech}^2\frac{1}{2T}=1-h^2$ 单独展开（来源不混）；一元化只做"整块乘正分母 $D=1-h^2>0$"的代数换元（`ratioCriterion`），$r$ 被消掉，$G$ 只含 $\Phi$ 与 $h$。
- `a_gate.ps1`：`$mods` 二十八项，58 条 `#print axioms`、53 条 `#check`；实跑 `A 闸 PASS（限环 15 二十八模块 v28）`——28/28 编译 ok、axioms 全白名单、257 文件 token 0 命中、exit 0。
- 写法坑（五条）：`field_simp` 已闭合后多写 `ring` 报 `No goals`；pwsh 里 `lean … 2>&1 | Select-Object -Last` 会挂死，须重定向到文件再读；`Set-Content -Encoding UTF8` 的临时 `.lean` 带 BOM（Lean 报 `expected token` 于 1:0）；改 Spec 使全部下游 olean 失效，须按依赖序重编（Spec≈85 s、模块≈35 s）；`shapeH` 与 `shapePhi` 的分母同式，是耦合点，改一处必须同步。
- 判定：**G-188b-2f 判据一元化完成**；$G$ 的符号**未证**（缺 $\Phi$ 的单调性）。最易跑偏处：`rw [hT2, hS]`——分子分母任一写错，`rw` 仍能对上"形似式"，故分子只走 `nlinarith [hp]`、分母只走勾股恒等式。
- 口径：200 的"$r$ 的上下夹逼是必要入口"**撤销**（记入 `DISCARD.md` 第 201 轮），$r$ 的界降为可选旁证。
