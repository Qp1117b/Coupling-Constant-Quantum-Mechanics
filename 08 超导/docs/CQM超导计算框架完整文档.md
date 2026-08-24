# CQM超导：计算框架与推导完整文档

**本文档将理论推导与计算实现严格对齐。每个公式标注对应代码位置，每个代码函数标注理论来源。**

**代码目录**：`08 超导/cqm_analysis/`

---

## 目录

1. [理论基础：SU(5)发生学与β推导](#1-理论基础)
2. [同步算符与Tc闭式](#2-同步算符与tc闭式)
3. [双尺度涨落公式](#3-双尺度涨落公式)
4. [超导判据与反推法](#4-超导判据与反推法)
5. [计算实现：代码结构与公式对应](#5-计算实现)
6. [大规模测试结果](#6-大规模测试结果)
7. [已知缺口](#7-已知缺口)

---

## 1. 理论基础

### 1.1 SU(5)发生学

**物理图像**：QG前几何退相干 → SU(5)形成 → 破缺 → U(1)×SU(2)×SU(3) + 电子/核子

**A4型嘉当矩阵**（SU(5)的根系结构）：

$$A_4 = \begin{pmatrix} 2 & -1 & 0 & 0 \\ -1 & 2 & -1 & 0 \\ 0 & -1 & 2 & -1 \\ 0 & 0 & -1 & 2 \end{pmatrix}$$

**代码**：`wolfram_verify.wl` line 7
```wolfram
A4 = {{2,-1,0,0},{-1,2,-1,0},{0,-1,2,-1},{0,0,-1,2}};
```

**特征值**：$\lambda_k = 2 - 2\cos(k\pi/5)$, $k=1,2,3,4$

**Coxeter数** $h = 5$ → 轨道角动量限制 $l = 0, 1, 2, 3$

**壳层饱和数**：$2(2l+1) = 2, 6, 10, 14$（SU(2)自旋×2来自SU(5)破缺）

**周期长度**：$2, 8, 18, 32$

### 1.2 β的第一性推导

**定理**：$\beta = 8\pi + 1 \approx 26.13$

**推导**（A4群论）：

1. $V_4 = \{e, (12)(34), (13)(24), (14)(23)\} \trianglelefteq A_4$（Klein四元群），$|V_4| = 4$
2. 每个V₄元素贡献$2\pi$和乐（绕位错闭合回路）
3. $\beta = 2|V_4|\pi + 1 = 8\pi + 1$

**等价推导**（格林函数迹）：

$$\beta = 2\pi \cdot \mathrm{tr}(C_{A_4}^{-1}) + 1, \quad \mathrm{tr}(C_{A_4}^{-1}) = \frac{n(n+2)}{6} = 4$$

**代码**：
- `cqm_core.py` line 40: `DEFAULT_BETA = 8.0 * math.pi + 1.0`
- `csv_database_test.py` line 17: `BETA = 8 * math.pi + 1`
- `V_element_to_super_sync.py` line 30: `beta = 8 * math.pi + 1`
- `beta_first_principles.py`: 完整A4群论验证

**数值**：$\beta = 26.1327...$, $1/\beta = 0.03826...$

**代码**：`csv_database_test.py` line 22: `DELTA_C = 1.0 / BETA`

### 1.3 黎曼零点与同步算符

**定义**：同步算符是黎曼式的，本征值 = $\gamma_n$（黎曼零点虚部）

**前几个零点**：

| $n$ | $\gamma_n$ | 代码位置 |
|-----|-----------|----------|
| 1 | 14.134725 | `csv_database_test.py` line 18: `GAMMA_1 = 14.134725` |
| 2 | 21.022040 | `csv_database_test.py` line 19: `GAMMA_2 = 21.022040` |

**谱间隙**：$\Delta\gamma = \gamma_2 - \gamma_1 = 6.887315$

**代码**：`csv_database_test.py` line 20: `GAP = GAMMA_2 - GAMMA_1`

---

## 2. 同步算符与Tc闭式

### 2.1 V_element构造

**元素FG上的同步算符**：

$$\hat{V}_{\text{element}} = V_0 + L_{\text{orbital}}$$

- $V_0 = \sum_p \frac{\ln p}{\sqrt{p}} \delta(u - \ln p)$（质数势，给出n能级）
- $L_{\text{orbital}} = \sum_l l \cdot \Pi_l$（轨道角动量算符，给出l分裂）

**本征值**：$E(n, l) = N(\gamma_n) + l = n + l$（Madelung规则）

**代码**：`V_element_explicit_construction.py`（显式构造），`element_genesis.py`（推导链）

### 2.2 V_element → S_super映射

**映射 $\Phi$**：

$$\Phi(V_0 + L_{\text{orbital}}) = V_0 + V_{\text{角亏激活}}$$

| 映射规则 | 物理意义 |
|----------|----------|
| $\Phi(V_0) = V_0$ | 质数势不变（QG前几何普适） |
| $\Phi(L_{\text{orbital}}) = V_{\text{角亏激活}}$ | 轨道角动量 → 角亏激活 |
| $\Phi(N(\gamma_n)) = \gamma_n$ | 计数函数 → 零点本身 |

**代码**：`V_element_to_super_sync.py` line 80-96

### 2.3 超导同步算符本征值

$$\lambda_n(T) = \gamma_n - V_{\text{角亏激活}}(n, T)$$

**角亏激活能**：

$$V_{\text{角亏激活}}(n, T) = \frac{\beta^2 \Delta\delta_v(T)^2 (n^2 - 1)}{4n^2 (1 - \beta\delta_v)}$$

**温度依赖**：

$$\Delta\delta_v(T) = \Delta\delta_0 \cdot \sqrt{\tanh\frac{\theta_D}{2T}}$$

**代码**：`V_element_to_super_sync.py` line 105-116
```python
def V_angle_activation(n, delta_delta_0, delta_v, beta, T, Omega_0, theta_D):
    if n == 1:
        return 0.0  # n²-1=0
    tanh_arg = theta_D / (2 * T) if T > 0 else float('inf')
    delta_delta_T = delta_delta_0 * math.sqrt(math.tanh(tanh_arg))
    return beta**2 * delta_delta_T**2 * (n**2 - 1) / (4 * n**2 * (1 - beta * delta_v))
```

**关键性质**：
- $n=1$（正常态）：$V_{\text{角亏激活}} = 0$，$\lambda_1 = \gamma_1$（无角亏激活）
- $n=2$（超导态）：$V_{\text{角亏激活}} = \frac{3\beta^2 \Delta\delta^2}{16(1-\beta\delta_v)}$

### 2.4 Tc闭式推导

**本征值交叉条件**：$\lambda_1(T_c) = \lambda_2(T_c)$

$$\gamma_1 = \gamma_2 - \frac{3\beta^2 \Delta\delta_v(T_c)^2}{16(1 - \beta\delta_v)}$$

代入温度依赖：

$$\tanh\frac{\theta_D}{2T_c} = \frac{16(1-\beta\delta_v)(\gamma_2 - \gamma_1)}{3\beta^2 \Delta\delta_0^2} = \frac{1}{x}$$

其中：

$$\boxed{x = \frac{3\beta^2 \Delta\delta_0^2}{16(1 - \beta\delta_v)(\gamma_2 - \gamma_1)}}$$

**Tc闭式**：

$$\boxed{T_c = \frac{\theta_D}{2 \cdot \text{arccoth}(x)}}$$

利用 $\text{arccoth}(x) = \frac{1}{2}\ln\frac{x+1}{x-1}$：

$$T_c = \frac{\theta_D}{\ln\frac{x+1}{x-1}}$$

**超导条件**：$x > 1$

**代码**：`csv_database_test.py` line 139-146
```python
def calc_Tc(ddv0, dv, theta_D):
    if BETA * dv >= 1:
        return 0, 0
    x = 3 * BETA**2 * ddv0**2 / (16 * (1 - BETA*dv) * GAP)
    if x > 1:
        return x, theta_D / (2 * 0.5 * math.log((x+1)/(x-1)))
    return x, 0
```

**代码**：`V_element_to_super_sync.py` line 143-165（完整推导过程）

---

## 3. 双尺度涨落公式

### 3.1 Regge剖分与晶胞

**关键概念**：Regge剖分顶点 = **晶胞**（原子/分子/复合物），不是单个原子

**晶胞不是刚体**——晶胞内原子相对运动贡献角亏涨落。总涨落为晶胞间（声学模）与晶胞内（光学模）的平方和：

$$\boxed{\Delta\delta_0^2 = \Delta\delta_{\text{inter}}^2 + \Delta\delta_{\text{intra}}^2}$$

### 3.2 晶胞间涨落（声学模）

$$\Delta\delta_{\text{inter}}^2 = \frac{C^2}{L^2} \cdot \frac{3\hbar}{4\omega_D} \cdot (1-f) \cdot \frac{2z}{M_{\text{cell}}}$$

| 符号 | 含义 | 代码变量 |
|------|------|----------|
| $C^2$ | Regge几何因子 = 2/3（**已严格导出**：$4/3 \times 1/2$） | `C2 = 2.0/3.0` |
| $L$ | 晶胞间距离 (m) | `L_ang * 1e-10` |
| $\omega_D$ | Debye频率 = $\theta_D k_B / \hbar$ | `theta_D * KB / HBAR` |
| $f$ | 关联因子 (0<f<1) | `f` |
| $z$ | 晶胞配位数 | `z` |
| $M_{\text{cell}}$ | 晶胞总质量 (kg) | `M_amu * AMU` |

**代码**：`csv_database_test.py` line 114-118
```python
def ddv_inter(M_amu, L_ang, theta_D, z, f=0.5):
    L = L_ang * 1e-10
    w = theta_D * KB / HBAR
    s = z * 2.0 / (M_amu * AMU)
    return math.sqrt(max((C2/L**2) * (3*HBAR/(4*w)) * (1-f) * s, 0))
```

### 3.3 晶胞内涨落（光学模）

$$\Delta\delta_{\text{intra}}^2 = \frac{C^2}{l^2} \cdot \frac{3\hbar}{4\omega_D} \cdot (1-f) \cdot \sum_{\text{edges}} \left(\frac{1}{m_i} + \frac{1}{m_j}\right)$$

| 符号 | 含义 | 代码变量 |
|------|------|----------|
| $l$ | 晶胞内原子间距 (m) | `l_ang * 1e-10` |
| $\sum$ | 遍历晶胞内原子对 | `edges`列表 |
| $m_i, m_j$ | 边两端原子质量 (amu) | `mi, mj` |

**代码**：`csv_database_test.py` line 120-124
```python
def ddv_intra(edges, l_ang, theta_D, f=0.5):
    l = l_ang * 1e-10
    w = theta_D * KB / HBAR
    s = sum((1.0/(mi*AMU) + 1.0/(mj*AMU)) for mi, mj in edges)
    return math.sqrt(max((C2/l**2) * (3*HBAR/(4*w)) * (1-f) * s, 0))
```

### 3.4 最小分布单元与N消去

**关键修正**：每个顶点的角亏涨落是**局域量**，不依赖系统总原子数N。

Debye积分中，DOS $g(\omega) = \frac{9N\omega^2}{\omega_D^3}$ 的N在归一化时被消去：

$$\langle u_i^2 \rangle = \frac{1}{3N} \int_0^{\omega_D} g(\omega) \frac{\hbar}{2m_i \omega} d\omega = \frac{3\hbar}{4m_i \omega_D}$$

**结果**：代码中`ddv_inter`和`ddv_intra`均不含N，纯局域量。

### 3.5 关联因子f的物理意义

| f值 | 物理意义 | 适用场景 |
|-----|----------|----------|
| 0 | 最近邻原子位移完全独立 | 理论下限 |
| →1 | 最近邻原子同相运动（声学模） | 边长不变，涨落小 |
| <0 | 最近邻原子反相运动（光学模） | 边长变化大 |
| 0.3-0.6 | 实际材料（声学+光学混合） | 氢化物 |
| 0.4-0.5 | 中等关联 | 铜氧/铁基 |
| 0.5 | 默认值 | 元素/合金 |

### 3.6 完整角亏

$$\delta_v = \delta_{\text{intrinsic}} + \delta_{\text{pressure}}$$

- $\delta_{\text{intrinsic}}$：电子结构内禀角亏（Fermi面几何frustration）
- $\delta_{\text{pressure}} = P/(3B)$：压力诱导角亏

**注**：在计算实现中，高压材料的压力效应已体现在结构参数变化（$\theta_D$增大、晶格压缩）中，反推得到的是总角亏$\delta_v$。

---

## 4. 超导判据与反推法

### 4.1 超导临界条件

从 $x > 1$ 导出：

$$\boxed{\beta\delta_v + \frac{3\beta^2}{16(\gamma_2 - \gamma_1)} \Delta\delta_0^2 > 1}$$

即 $\delta_v + 0.711 \cdot \Delta\delta_0^2 > \frac{1}{\beta} \approx 0.038$

**物理意义**：静态角亏 $\delta_v$（Fermi面拓扑/压力诱导）与动态角亏涨落 $\Delta\delta_0$（声子零点运动）共同决定超导。

### 4.2 反推法

从实验$T_c$反推$\delta_v$（使超导判据等号成立的临界角亏）：

**步骤1**：从$T_c$计算$x$

$$x = \coth\frac{\theta_D}{2T_c} = \frac{1}{\tanh(\theta_D / 2T_c)}$$

**步骤2**：从$x$计算$\omega$

$$\omega = \frac{3\beta^2 \Delta\delta_0^2}{16 \cdot x \cdot (\gamma_2 - \gamma_1)}$$

**步骤3**：反推$\delta_v$

$$\delta_v = \frac{1 - \omega}{\beta}$$

**代码**：`csv_database_test.py` line 126-137
```python
def rev_delta(ddv0, theta_D, tc, dp=0):
    if tc <= 0 or theta_D <= 0:
        return None
    arg = theta_D / (2*tc)
    if arg < 1:
        return None
    x = 1.0 / math.tanh(arg)
    om = 3 * BETA**2 * ddv0**2 / (16 * x * GAP)
    if om <= 0 or om > 1:
        return None
    return (1 - om) / BETA - dp
```

**判定标准**：反推$\delta_v \approx 1/\beta \approx 0.038$ → 超导候选

### 4.3 数学-物理双重性

当 $T_c \ll \theta_D$ 时，$x = \coth(\theta_D / 2T_c) \approx 1$，公式结构迫使 $\delta_v \approx 1/\beta$（数学必然）。

**物理内容**：非超导体的 $\delta_v < 1/\beta$（Fermi面无足够frustration），超导体的 $\delta_v$ 达到临界值。

---

## 5. 计算实现

### 5.1 代码文件结构

```
cqm_analysis/
├── cqm_core.py                      ← 核心计算模块（β, ℏ, k_B等）
├── csv_database_test.py             ← 226材料CSV测试（主测试脚本）
├── large_scale_test.py              ← 187材料测试（含非超导体对照）
├── cell_subdivision.py              ← 晶胞剖分双尺度涨落验证
├── universal_criterion.py           ← 非超导体对照+普适判据
├── beta_first_principles.py         ← β=8π+1第一性推导验证
├── V_element_to_super_sync.py       ← V_element→S_super映射+Tc闭式
├── material_Tc_prediction.py        ← 材料Tc数值预测
├── element_genesis.py               ← 元素发生学：A4→周期表
├── complete_shell_derivation.py     ← 壳层推导：SU(5)→2,6,10,14
├── spin_origin_and_emergence.py     ← SU(2)自旋来源
├── V_element_explicit_construction.py ← V_element显式构造
├── delta_spectral_constraint.py     ← δ(Z,N)谱约束
├── hund_rules_quantitative.py       ← 洪特规则定量推导
├── wolfram_verify.wl                ← Wolfram验证（19项）
└── superconductors_deduplicated.csv ← 超导数据库（226条）
```

### 5.2 核心常数定义

| 常数 | 值 | 代码位置 |
|------|-----|----------|
| $\hbar$ | 1.0546e-34 J·s | `csv_database_test.py` line 14 |
| $k_B$ | 1.381e-23 J/K | `csv_database_test.py` line 15 |
| $m_u$ | 1.66e-27 kg | `csv_database_test.py` line 16 |
| $\beta$ | 8π+1 ≈ 26.13 | `csv_database_test.py` line 17 |
| $\gamma_1$ | 14.134725 | `csv_database_test.py` line 18 |
| $\gamma_2$ | 21.022040 | `csv_database_test.py` line 19 |
| $C^2$ | 2/3 | `csv_database_test.py` line 21 |
| $1/\beta$ | 0.03827 | `csv_database_test.py` line 22 |

### 5.3 计算流程（csv_database_test.py）

```
对每个材料:
  1. 解析化学式 → 原子组成 {元素: 数量}
  2. 估算参数 → (θ_D, M_cell, L, z, edges, l, B, P, f)
  3. 计算δ_pressure = P/(3B)
  4. 计算Δδ_inter = ddv_inter(M_cell, L, θ_D, z, f)
  5. 计算Δδ_intra = ddv_intra(edges, l, θ_D, f)
  6. 合成Δδ₀ = √(Δδ_inter² + Δδ_intra²)
  7. 反推δ_v = rev_delta(Δδ₀, θ_D, Tc_exp)
  8. 判定: δ_v ≈ 1/β → ✓ (超导)
```

### 5.4 参数估算策略

| 类别 | θ_D | L (Å) | z | l_intra (Å) | edges_intra | f |
|------|-----|--------|---|-------------|-------------|---|
| 元素(常压) | 查表 | 2r_avg | 12 | — | — | 0.5 |
| 元素(高压) | 查表 | 2r_avg | 12 | — | — | 0.5 |
| A15 | ≥400 | 1.8r_avg | 8 | — | — | 0.4 |
| 氢化物 | ≥1500 | 2.0 | 8 | 1.7 | [(m_metal, 1.008)]×min(n_H,4) | 0.5 |
| 铜氧化物 | ≥400 | 3.8 | 6 | 1.9 | [(63.55, 16.0)]×2 | 0.4 |
| 铁基 | ≥350 | 3.5 | 6 | 2.0 | [(55.85, m_X)]×2 | 0.4 |
| 有机 | ≥100 | 5.0 | 4 | — | — | 0.5 |
| 富勒烯 | 100 | 10.0 | 4 | — | — | 0.5 |

**代码**：`csv_database_test.py` line 151-261 (`estimate_params`函数)

### 5.5 原子参数库

每个原子存储4个参数：`(质量amu, Debye温度K, 金属半径Å, 体积模量GPa)`

**代码**：`csv_database_test.py` line 27-71 (`ATOM_DB`字典)

**化合物参数估算**：
- Debye温度：质量加权平均
- 金属半径：简单平均
- 体积模量：简单平均

---

## 6. 大规模测试结果

### 6.1 CSV数据库测试（226个材料）

**数据来源**：`superconductors_deduplicated.csv`（226条记录，12个类别）

**结果**：反推法226/226"成功"，**但这是数学恒等式，不是物理预言**

> **重要警告**：以下"100%成功率"使用的是**反推法**——从实验$T_c$反推$\delta_v$，再检查$\delta_v$是否在合理范围。给定任何$T_c>0$都能反推$\delta_v\approx 1/\beta$，这是公式结构而非独立预言。代码中`tc_calc = tc_exp`直接赋值。**前向计算**（从材料参数独立计算$T_c$）目前失败：$\delta_{\text{intrinsic}}=0$时大部分材料$T_c=0$，$\delta_{\text{intrinsic}}=0.99/\beta$时Nb算出322K vs 实验9.2K。详见`honest_forward_check.py`。

| 类别 | 测试数 | 反推"成功率" |
|------|--------|--------|
| A15结构金属间化合物 | 14 | 100% |
| 元素超导体(常压) | 27 | 100% |
| 元素超导体(高压) | 15 | 100% |
| 其他特殊超导体 | 32 | 100% |
| 其他金属间化合物 | 25 | 100% |
| 合金超导体 | 8 | 100% |
| 富勒烯超导体 | 9 | 100% |
| 有机超导体 | 19 | 100% |
| 氢化物高压超导体 | 22 | 100% |
| 石墨插层超导体 | 7 | 100% |
| 铁基超导体 | 26 | 100% |
| 铜氧化物高温超导体 | 22 | 100% |

**反推$\delta_v$统计**（注意：CV=11%，非窄分布）：
- 样本数：168
- 均值：0.03683
- 标准差：0.00403
- $1/\beta$ = 0.03827
- 均值$/（1/\beta）$ = 0.962
- 中位数：0.03785
- $T_c$范围：0.01 K（W）到 475 K（La₂MgH₁₅）

### 6.2 非超导体对照

| 材料 | $\delta_v$ | $\beta\delta_v$ | 超导？ |
|------|-----------|-----------------|--------|
| Cu | < 1/β | < 1 | ✗ |
| Ag | < 1/β | < 1 | ✗ |
| Au | < 1/β | < 1 | ✗ |
| Si | < 1/β | < 1 | ✗ |
| Ge | < 1/β | < 1 | ✗ |
| Fe | > 1/β | > 1（铁磁竞争） | ✗ |

**代码**：`universal_criterion.py`

### 6.3 Wolfram验证（19项全部通过）

| 编号 | 验证内容 |
|------|----------|
| 1-4 | A4特征值、D(δ)谱、壳层鲁棒性、SU(4)分解 |
| 5-8 | 壳层{2,6,10,14}、λ_l单调性、Madelung填充、δ(Z,N)约束 |
| 9-14 | 交换算符恒等式、洪特规则、p²/d²基态、洪特第三规则、V_element构造、SU(5)破缺 |
| 15-19 | 交换算符详细验证、洪特阈值、p²/d²/d³基态(ls/lo=12)、完整p壳、完整d壳 |

**代码**：`wolfram_verify.wl`

---

## 7. 已知缺口

| 缺口 | 状态 | 说明 |
|------|------|------|
| $C^2 = 2/3$ 严格推导 | **已闭合** | $C^2 = \frac{4}{3} \times \frac{1}{2} = \frac{2}{3}$。几何因子 $4/3$：2D正三角形剖分，每条边被2个三角形共享，$|\partial\delta/\partial l| = 2/(L\sqrt{3})$。边共享因子 $1/2$：每条边属于2个顶点，单顶点分一半。3D→2D投影因子$\sin\phi$在链式法则中消去。验证：`derive_C_squared.py` |
| 关联因子 $f$ 严格计算 | **半推导** | Debye模型下严格公式：$f = \mathrm{sinc}^2(k_D R/2)$，$k_D=(6\pi^2 n)^{1/3}$。数值验证通过。BCC: $f\approx0.16$, FCC: $f\approx0.14$。与唯象值0.5有差异（Debye各向同性近似），精确值需DFT声子谱。氢化物：$f=(f_{ac}+w \cdot f_{op})/(1+w)$，$w=(M/m_H)(\omega_{ac}/\omega_{op})^2$。验证：`derive_f_correlation.py` |
| $\delta_{\text{intrinsic}}$ 严格推导 | **半推导** | 公式已写出：$\delta_{\text{intrinsic}} = \frac{1}{2\pi}\int_{\text{FS}}|\Omega(\mathbf{k})|dS/A_{\text{FS}}$（Berry曲率积分）。球形Fermi面→$\delta=0$（Cu/Ag/Au不超导✓），van Hove→$\delta$最大（铜氧化物✓）。$\delta_v\approx 1/\beta$是$T_c\ll\theta_D$时的数学必然，物理内容在于非超导体$\delta_v<1/\beta$。数值需DFT。验证：`derive_delta_intrinsic.py` |
| 原子参数精度 | 估算 | Debye温度、体积模量等从原子组成估算，应从DFT计算获取 |
| **前向计算** | **失败** | 反推法是数学恒等式（任何$T_c$→$\delta_v\approx 1/\beta$）。前向计算（$\delta_{\text{intrinsic}}=0$）大部分$T_c=0$；$\delta_{\text{intrinsic}}=0.99/\beta$时Nb→322K vs 9.2K。$T_c$对$\delta_{\text{intrinsic}}$极度敏感。$\Delta\delta_0$不能区分超导/非超导。**当前是拟合框架，非预言框架**。详见`honest_forward_check.py` |

---

## 附录：完整公式速查表

| 公式 | 表达式 | 代码位置 |
|------|--------|----------|
| β | $8\pi + 1 \approx 26.13$ | `BETA = 8*math.pi + 1` |
| $1/\beta$ | $\approx 0.0383$ | `DELTA_C = 1.0/BETA` |
| 谱间隙 | $\gamma_2 - \gamma_1 \approx 6.887$ | `GAP = GAMMA_2 - GAMMA_1` |
| Debye频率 | $\omega_D = \theta_D k_B / \hbar$ | `w = theta_D * KB / HBAR` |
| 晶胞间涨落 | $\sqrt{\frac{C^2}{L^2} \cdot \frac{3\hbar}{4\omega_D} \cdot (1-f) \cdot \frac{2z}{M}}$ | `ddv_inter()` |
| 晶胞内涨落 | $\sqrt{\frac{C^2}{l^2} \cdot \frac{3\hbar}{4\omega_D} \cdot (1-f) \cdot \sum(\frac{1}{m_i}+\frac{1}{m_j})}$ | `ddv_intra()` |
| 总涨落 | $\sqrt{\Delta\delta_{\text{inter}}^2 + \Delta\delta_{\text{intra}}^2}$ | `sqrt(di**2 + dn**2)` |
| x参数 | $\frac{3\beta^2 \Delta\delta_0^2}{16(1-\beta\delta_v)(\gamma_2-\gamma_1)}$ | `calc_Tc()` |
| Tc | $\frac{\theta_D}{\ln\frac{x+1}{x-1}}$ | `theta_D / (2*0.5*log((x+1)/(x-1)))` |
| 超导条件 | $x > 1$ | `if x > 1:` |
| 反推δ_v | $\frac{1}{\beta}(1 - \frac{3\beta^2\Delta\delta_0^2}{16x(\gamma_2-\gamma_1)})$ | `rev_delta()` |
| 超导判据 | $\beta\delta_v + \frac{3\beta^2}{16(\gamma_2-\gamma_1)}\Delta\delta_0^2 > 1$ | $x > 1$ 等价 |
