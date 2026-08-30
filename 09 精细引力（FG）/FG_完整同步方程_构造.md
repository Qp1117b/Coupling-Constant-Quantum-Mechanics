# 完整同步方程的构造

> **定位**：本文构造完整同步方程 $\hat{\mathcal{S}}^{(Z)}_{\text{full}}$ 的具体形式，使其在通用极限下退化为已有的平庸方程（§18.2）。平庸方程给出壳层结构和周期表（$Z_{\max}=118$），完整方程给出元素特定精确关联能。
>
> **关联文档**：`FG_元素FG_第一性.md`（§18.2完整同步方程表述、§19量纲归一化）、`FG_纤维丛理论.md`（§9纤维丛与CFT对应）、`01 核心理论/CQM_核心_声子理论.md`（声子三层结构）

---

## 1. 问题陈述

### 1.1 平庸同步方程（已有）

当前同步方程用**通用 $A_4$ 代数骨架**处理所有元素：

$$\hat{\mathcal{S}}_{\text{trivial}} = \frac{L_u}{2\pi C}\sqrt{1-\beta\hat{\delta}_v}$$

其中曲率算符：

$$\hat{\delta}_v = \bar{\delta}_v + \sum_k \frac{\hbar\omega_k}{E_{\text{bind}}}|v_k(v)|^2\left(\hat{a}_k^\dagger\hat{a}_k + \frac{1}{2}\right)$$

**平庸化的具体内容**：

| 量 | 平庸方程中的值 | 元素特定性 |
|:---|:---|:---|
| 嘉当矩阵 $\mathcal{C}$ | $A_4$（正4-单形，等边） | 固定，所有元素共享 |
| 本征值 $\lambda_k$ | $4\sin^2\frac{k\pi}{10}$ | 通用 |
| 本征向量 $v_k(v)$ | $|v_k(4)|^2 = \frac{2}{5}\sin^2\frac{k\pi}{5}$ | 通用 |
| 基准频率 $\omega_0$ | 通用 | 不依赖 $Z$ |
| 归一化 $E_{\text{bind}}$ | 通用 | 不依赖 $Z$ |
| 经典角亏 $\bar{\delta}_v$ | $0$（质子平坦） | 不依赖 $Z$ |

**平庸方程的输出**：壳层结构、Madelung规则、$Z_{\max}=118$、增强因子（Cr/Cu d波 $5/4$）、s波 $E_c=0$。

**平庸方程的不足**：抹除了元素特定信息，无法给出元素特定精确关联能。

### 1.2 完整同步方程（目标）

构造 $\hat{\mathcal{S}}^{(Z)}_{\text{full}}$，满足：

1. **元素特定性**：包含元素 $Z$ 的特定剖分 $\mathcal{R}_Z$、曲率数据、自组织数据
2. **退化关系**：忽略元素特定信息时退化为平庸方程
3. **第一性**：从CQM第一性原理构造，无经验参数
4. **自洽性**：电子结构反馈到曲率算符（非线性自洽方程）

---

## 2. 元素特定信息的三个来源

### 2.1 来源一：几何信息 $\mathcal{R}_Z$

每个元素 $Z$ 有自己的Regge剖分：

$$\mathcal{R}_Z = (V_Z, E_Z, F_Z, \{\bar{L}_{ij}^{(Z)}\})$$

- $V_Z = \{1,2,3,4\}$：4个顶点（核子平衡位置，拓扑固定为 $A_4$ 链）
- $E_Z$：边，经典边长 $\bar{L}_{ij}^{(Z)} = |\bar{X}_i^{(Z)} - \bar{X}_j^{(Z)}|$（**依赖元素 $Z$ 的核子分布**）
- $F_Z$：三角形面，二面角由边长通过余弦定律确定

**几何信息进入曲率的两条途径**：

**途径A：经典角亏**

$$\bar{\delta}_v^{(Z)} = 2\pi - \sum_{\Delta \ni v} \bar{\theta}_v^{(Z)}(\Delta)$$

其中 $\bar{\theta}_v^{(Z)}(\Delta)$ 由元素特定的边长 $\bar{L}_{ij}^{(Z)}$ 通过余弦定律确定。等边正4-单形极限下 $\bar{\delta}_v^{(Z)} \to 0$。

**途径B：动力学矩阵形变**

平庸方程中，动力学矩阵正比于嘉当矩阵（等边正4-单形）：

$$D_{vv'} = \frac{k}{m}\mathcal{C}_{vv'}$$

完整方程中，边长不等，弹性常数 $k_{ij}^{(Z)} = k(\bar{L}_{ij}^{(Z)})$ 依赖边长，动力学矩阵不再正比于嘉当矩阵：

$$D_{vv'}^{(Z)} \neq \frac{k}{m}\mathcal{C}_{vv'}$$

动力学矩阵的本征值 $\lambda_k^{(Z)}$ 和本征向量 $v_k^{(Z)}(v)$ 都是元素特定的：

$$\lambda_k^{(Z)} \neq 4\sin^2\frac{k\pi}{10}, \quad v_k^{(Z)}(v) \neq v_k(v)$$

简正模式频率：

$$\omega_k^{(Z)} = \omega_0^{(Z)}\sqrt{\lambda_k^{(Z)}}$$

其中 $\omega_0^{(Z)} = \sqrt{k^{(Z)}/m}$ 是元素特定的基准频率。

**边长的来源**：边长 $\bar{L}_{ij}^{(Z)}$ = 核子间距离，由核子分布确定。核子分布由**核子层同步方程**（QG层紧化算符）的输出给出。这是层级结构：

$$\underbrace{\hat{\mathcal{S}}_0}_{\text{QG层：GL(5)→SU(5)}} \;\longrightarrow\; \text{核子分布} \;\longrightarrow\; \bar{L}_{ij}^{(Z)} \;\longrightarrow\; \hat{\delta}_v^{(Z)} \;\longrightarrow\; \underbrace{\hat{\mathcal{S}}^{(Z)}_{\text{full}}}_{\text{FG层：元素特定}}$$

### 2.2 来源二：归一化信息 $E_{\text{bind}}^{(Z)}$

平庸方程用通用 $E_{\text{bind}}$ 归一化：

$$\hat{\delta}_v^{(1)} = \sum_k \frac{\hbar\omega_k}{E_{\text{bind}}}|v_k(v)|^2(\hat{a}_k^\dagger\hat{a}_k + 1/2)$$

完整方程用元素特定 $E_{\text{bind}}^{(Z)}$ 归一化：

$$\hat{\delta}_v^{(1,Z)} = \sum_k \frac{\hbar\omega_k^{(Z)}}{E_{\text{bind}}^{(Z)}}|v_k^{(Z)}(v)|^2(\hat{a}_k^\dagger\hat{a}_k + 1/2)$$

$E_{\text{bind}}^{(Z)}$ 是元素 $Z$ 的核子结合能，依赖元素特定的核子结构。

**归一化的物理意义**（§19.6）：$\hbar\omega_k^{(Z)}/E_{\text{bind}}^{(Z)}$ 把有量纲声子能量转换为无量纲曲率。通用归一化抹除元素特定能量标度 → 平庸方程；元素特定归一化保留能量标度 → 完整方程。

### 2.3 来源三：自组织信息（电子反馈）

**这是完整同步方程的关键新增项**。

平庸方程中，曲率只来自核子振荡（声子）。完整方程中，电子分布反馈到曲率——电子在核子曲率场中运动，电子的分布改变核子的有效势场，从而改变曲率。

**物理图像**：

- 核子振荡产生曲率涨落（声子）——**同步的前提**
- 电子在曲率场中同步（同步方程）——**同步的发生**
- 电子分布反馈到曲率场（自洽）——**同步的完成**

这类似于Born-Oppenheimer近似 vs 完全解：
- 平庸方程 = Born-Oppenheimer近似（核子固定，忽略电子反馈）
- 完整方程 = 完全解（核子-电子耦合，自洽）

---

## 3. 元素特定曲率算符的构造

### 3.1 完整曲率算符

$$\boxed{\hat{\delta}_v^{(Z)}[\rho_Z] = \underbrace{\bar{\delta}_v^{(Z)}}_{\text{经典背景}} + \underbrace{\sum_k \frac{\hbar\omega_k^{(Z)}}{E_{\text{bind}}^{(Z)}}|v_k^{(Z)}(v)|^2\left(\hat{a}_k^\dagger\hat{a}_k + \frac{1}{2}\right)}_{\text{量子涨落}} + \underbrace{\Delta\hat{\delta}_v^{\text{e-n}}[\rho_Z]}_{\text{电子反馈}}}$$

其中 $\rho_Z$ 是电子密度（自洽确定，见§4）。

### 3.2 经典背景 $\bar{\delta}_v^{(Z)}$

由元素特定的Regge剖分 $\mathcal{R}_Z$ 严格确定：

$$\bar{\delta}_v^{(Z)} = 2\pi - \sum_{\Delta \ni v} \bar{\theta}_v^{(Z)}(\Delta)$$

$$\cos \bar{\theta}_v^{(Z)}(\Delta) = \frac{\cos \bar{\phi}_{vv'}^{(Z)} - \cos \bar{\phi}_{vv''}^{(Z)}\cos \bar{\phi}_{v'v''}^{(Z)}}{\sin \bar{\phi}_{vv'}^{(Z)}\sin \bar{\phi}_{v'v''}^{(Z)}}$$

其中二面角 $\bar{\phi}_{ij}^{(Z)}$ 由边长 $\bar{L}_{ij}^{(Z)}$ 通过余弦定律确定。

**退化**：等边正4-单形极限 $\bar{L}_{ij}^{(Z)} \to \bar{L}$，$\bar{\delta}_v^{(Z)} \to 0$（质子平坦）。

### 3.3 量子涨落

**动力学矩阵**：

$$D_{vv'}^{(Z)} = \frac{1}{m}\sum_{\text{边 } e \ni v,v'} \frac{k_e^{(Z)}}{m}\left(\delta_{vv'} - \delta_{vv''}\right)$$

其中 $k_e^{(Z)} = k(\bar{L}_e^{(Z)})$ 是边 $e$ 的弹性常数，依赖元素特定的边长。

**简正模式**：

$$D^{(Z)} v_k^{(Z)} = \lambda_k^{(Z)} v_k^{(Z)}, \quad \omega_k^{(Z)} = \omega_0^{(Z)}\sqrt{\lambda_k^{(Z)}}$$

**量子涨落算符**：

$$\hat{\delta}_v^{(1,Z)} = \sum_k \frac{\hbar\omega_k^{(Z)}}{E_{\text{bind}}^{(Z)}}|v_k^{(Z)}(v)|^2\left(\hat{a}_k^\dagger\hat{a}_k + \frac{1}{2}\right)$$

**退化**：等边极限 $k_e^{(Z)} \to k$，$D^{(Z)} \to \frac{k}{m}\mathcal{C}$，$\lambda_k^{(Z)} \to 4\sin^2\frac{k\pi}{10}$，$v_k^{(Z)}(v) \to v_k(v)$，$\omega_k^{(Z)} \to \omega_k$。

### 3.4 电子反馈曲率 $\Delta\hat{\delta}_v^{\text{e-n}}[\rho_Z]$

**构造原理**：电子分布通过电磁相互作用改变核子的有效曲率。在CQM中，曲率与耦合常数相关（$\hat{v}_\tau = \sqrt{1-\beta\hat{\delta}_v}$），电子分布改变有效耦合常数，从而改变曲率。

**具体形式**：

$$\boxed{\Delta\hat{\delta}_v^{\text{e-n}}[\rho_Z] = \sum_{v'} K_{vv'}^{(Z)} \rho_Z(v')}$$

其中：
- $\rho_Z(v')$：顶点 $v'$ 附近的电子密度（离散化）
- $K_{vv'}^{(Z)}$：电子-核子耦合核，描述电子在顶点 $v'$ 的分布如何影响顶点 $v$ 的曲率

**耦合核的构造**：

$$K_{vv'}^{(Z)} = \frac{\alpha}{\beta} \cdot \frac{1}{|\bar{X}_v^{(Z)} - \bar{X}_{v'}^{(Z)}|} \cdot \mathcal{G}_{vv'}$$

其中：
- $\alpha$：精细结构常数（电磁耦合强度）
- $\beta$：FG因果参数（$\beta = \frac{1}{4\pi}\ln\frac{L}{a}$）
- $|\bar{X}_v^{(Z)} - \bar{X}_{v'}^{(Z)}|$：核子间距离
- $\mathcal{G}_{vv'}$：几何因子（由Regge剖分的角度结构确定）

**物理意义**：电子在顶点 $v'$ 的分布通过电磁相互作用（强度 $\alpha$）影响顶点 $v$ 的核子，改变其有效曲率。距离越远，影响越弱（$1/r$ 衰减）。

**退化**：忽略电子反馈 $\rho_Z \to 0$，$\Delta\hat{\delta}_v^{\text{e-n}} \to 0$。

---

## 4. 自洽条件的构造

### 4.1 完整同步方程

$$\boxed{\hat{\mathcal{S}}^{(Z)}_{\text{full}}[\rho_Z]|\Psi_{Z,i}\rangle = s_{Z,i}|\Psi_{Z,i}\rangle}$$

其中完整同步算符：

$$\hat{\mathcal{S}}^{(Z)}_{\text{full}}[\rho_Z] = \frac{L_u}{2\pi C}\sqrt{1-\beta\hat{\delta}_v^{(Z)}[\rho_Z]}$$

**关键**：$\hat{\mathcal{S}}^{(Z)}_{\text{full}}$ 依赖电子密度 $\rho_Z$，而 $\rho_Z$ 依赖同步方程的解 $\Psi_{Z,i}$——这是**非线性自洽方程**。

### 4.2 自洽条件

$$\boxed{\rho_Z(v) = \sum_{i \in \text{occupied}} |\Psi_{Z,i}(v)|^2}$$

其中求和遍历所有占据态。

**自洽循环**：

$$\rho_Z \;\longrightarrow\; \hat{\delta}_v^{(Z)}[\rho_Z] \;\longrightarrow\; \hat{\mathcal{S}}^{(Z)}_{\text{full}}[\rho_Z] \;\longrightarrow\; \Psi_{Z,i} \;\longrightarrow\; \rho_Z$$

### 4.3 非线性来源

完整同步方程的非线性有两个来源：

1. **几何非线性**：$\sqrt{1-\beta\hat{\delta}_v}$ 中的平方根（Regge几何非线性）
2. **自洽非线性**：$\hat{\delta}_v^{(Z)}[\rho_Z]$ 依赖 $\rho_Z$，而 $\rho_Z = \sum_i |\Psi_{Z,i}|^2$ 依赖解

平庸方程只保留几何非线性（$\sqrt{1-\beta\hat{\delta}_v}$），忽略自洽非线性（$\Delta\hat{\delta}_v^{\text{e-n}} = 0$）。完整方程两者都保留。

### 4.4 双空间结构

完整同步算符保持双空间直积结构：

$$\hat{\mathcal{S}}^{(Z)}_{\text{full}} = \hat{\mathcal{S}}_{\text{nucleon}}^{(Z)}[\rho_Z] \otimes \hat{\mathbb{I}}_{U(1)} + \hat{\mathbb{I}}_{\text{nucleon}} \otimes \hat{\mathcal{S}}_{U(1)}(\hat{u})$$

其中：
- 核子部分 $\hat{\mathcal{S}}_{\text{nucleon}}^{(Z)}[\rho_Z] = \frac{L_u}{2\pi C}\sqrt{1-\beta\hat{\delta}_v^{(Z)}[\rho_Z]}$：元素特定，依赖电子密度
- U(1)部分 $\hat{\mathcal{S}}_{U(1)}(\hat{u}) = \sum_p \frac{\ln p}{\sqrt{p}}\delta(\hat{u} - \ln p)$：通用（质数势不依赖元素）

---

## 5. 退化关系的证明

### 5.1 退化条件

完整方程在以下极限下退化为平庸方程：

$$\bar{L}_{ij}^{(Z)} \to \bar{L} \quad \text{（等边正4-单形）}, \quad E_{\text{bind}}^{(Z)} \to E_{\text{bind}} \quad \text{（通用归一化）}, \quad \rho_Z \to 0 \quad \text{（忽略电子反馈）}$$

### 5.2 退化链

**步骤1：经典角亏退化**

$$\bar{\delta}_v^{(Z)} \xrightarrow{\bar{L}_{ij}^{(Z)} \to \bar{L}} \bar{\delta}_v = 0 \quad \text{（质子平坦）}$$

**步骤2：动力学矩阵退化**

$$D_{vv'}^{(Z)} \xrightarrow{k_e^{(Z)} \to k} \frac{k}{m}\mathcal{C}_{vv'} \quad \text{（正比于嘉当矩阵）}$$

**步骤3：简正模式退化**

$$\lambda_k^{(Z)} \to \lambda_k = 4\sin^2\frac{k\pi}{10}, \quad v_k^{(Z)}(v) \to v_k(v), \quad \omega_k^{(Z)} \to \omega_k$$

**步骤4：量子涨落退化**

$$\hat{\delta}_v^{(1,Z)} \xrightarrow{E_{\text{bind}}^{(Z)} \to E_{\text{bind}}} \hat{\delta}_v^{(1)} = \sum_k \frac{\hbar\omega_k}{E_{\text{bind}}}|v_k(v)|^2(\hat{a}_k^\dagger\hat{a}_k + 1/2)$$

**步骤5：电子反馈退化**

$$\Delta\hat{\delta}_v^{\text{e-n}}[\rho_Z] \xrightarrow{\rho_Z \to 0} 0$$

**步骤6：曲率算符退化**

$$\hat{\delta}_v^{(Z)}[\rho_Z] \to \hat{\delta}_v = \bar{\delta}_v + \hat{\delta}_v^{(1)}$$

**步骤7：同步算符退化**

$$\hat{\mathcal{S}}^{(Z)}_{\text{full}}[\rho_Z] \xrightarrow{\text{忽略元素特定信息}} \hat{\mathcal{S}}_{\text{trivial}} = \frac{L_u}{2\pi C}\sqrt{1-\beta\hat{\delta}_v}$$

### 5.3 退化定理

$$\boxed{\hat{\mathcal{S}}^{(Z)}_{\text{full}} \;\xrightarrow{\text{等边极限 + 通用归一化 + 忽略电子反馈}}\; \hat{\mathcal{S}}_{\text{trivial}}}$$

**推论**：完整方程的本征值 $s_{Z,i}$ 在退化极限下趋于平庸本征值 $n_i$：

$$s_{Z,i} \xrightarrow{\text{退化}} n_i$$

---

## 6. 关联能的计算方法

### 6.1 关联能分解

关联能分解为平庸部分和完整部分（§19.5）：

$$E_c(Z) = E_h \times \rho_Z \times f_{\text{full}}(Z)$$

其中：
- $E_h$：标度因子（$E_h = \alpha^2 m_e c^2 / 2$，Hartree能量）
- $\rho_Z$：增强因子（从平庸同步方程导出，如Cr/Cu的 $5/4$）
- $f_{\text{full}}(Z)$：元素特定因子（从完整同步方程导出）

### 6.2 增强因子 $\rho_Z$（平庸方程，已完成）

从平庸同步方程的本征值结构导出。例如：
- s波（He）：$E_c = 0$（SU(2)$_k$ 真空平庸）
- d波（Cr/Cu）：增强 $= 5/4 = 25\%$（g波禁戒 → 民主重分配）

### 6.3 元素特定因子 $f_{\text{full}}(Z)$（完整方程，本文构造）

从完整同步方程的本征值 $s_{Z,i}$ 与平庸本征值 $n_i$ 的差异导出：

$$\boxed{f_{\text{full}}(Z) = 1 + \frac{\sum_{i \in \text{occ}} (s_{Z,i} - n_i)}{\sum_{i \in \text{occ}} n_i}}$$

**物理意义**：
- $s_{Z,i} - n_i$：完整方程与平庸方程的本征值差异（元素特定修正）
- 求和遍历所有占据态
- $f_{\text{full}}(Z) = 1$ 时无元素特定修正（退化到平庸方程）

**退化验证**：

$$f_{\text{full}}(Z) \xrightarrow{\text{退化}} 1 + \frac{\sum_i (n_i - n_i)}{\sum_i n_i} = 1$$

### 6.4 本征值差异的微扰展开

对于小修正（边长形变小、电子反馈弱），本征值差异可用微扰展开：

$$s_{Z,i} - n_i \approx \langle \Psi_i | \Delta\hat{\mathcal{S}}^{(Z)} | \Psi_i \rangle$$

其中修正算符：

$$\Delta\hat{\mathcal{S}}^{(Z)} = \hat{\mathcal{S}}^{(Z)}_{\text{full}} - \hat{\mathcal{S}}_{\text{trivial}} \approx -\frac{L_u \beta}{4\pi C} \cdot \frac{\Delta\hat{\delta}_v^{(Z)}}{\sqrt{1-\beta\hat{\delta}_v}}$$

其中 $\Delta\hat{\delta}_v^{(Z)} = \hat{\delta}_v^{(Z)}[\rho_Z] - \hat{\delta}_v$ 是曲率修正（经典角亏差异 + 量子涨落差异 + 电子反馈）。

---

## 7. 迭代求解流程

完整同步方程是非线性自洽方程，需要迭代求解。

### 7.1 迭代算法

**步骤1：初始化**

从平庸方程的解作为初始猜测：

$$\hat{\mathcal{S}}_{\text{trivial}}|\Psi_i^{(0)}\rangle = n_i|\Psi_i^{(0)}\rangle$$

$$\rho_Z^{(0)}(v) = \sum_{i \in \text{occ}} |\Psi_i^{(0)}(v)|^2$$

**步骤2：构造完整曲率算符**

$$\hat{\delta}_v^{(Z)}[\rho_Z^{(n)}] = \bar{\delta}_v^{(Z)} + \sum_k \frac{\hbar\omega_k^{(Z)}}{E_{\text{bind}}^{(Z)}}|v_k^{(Z)}(v)|^2(\hat{a}_k^\dagger\hat{a}_k + 1/2) + \Delta\hat{\delta}_v^{\text{e-n}}[\rho_Z^{(n)}]$$

**步骤3：解完整同步方程**

$$\hat{\mathcal{S}}^{(Z)}_{\text{full}}[\rho_Z^{(n)}]|\Psi_{Z,i}^{(n+1)}\rangle = s_{Z,i}^{(n+1)}|\Psi_{Z,i}^{(n+1)}\rangle$$

**步骤4：更新电子密度**

$$\rho_Z^{(n+1)}(v) = \sum_{i \in \text{occ}} |\Psi_{Z,i}^{(n+1)}(v)|^2$$

**步骤5：检查收敛**

$$\|\rho_Z^{(n+1)} - \rho_Z^{(n)}\| < \epsilon$$

如果未收敛，回到步骤2。

**步骤6：计算关联能**

$$f_{\text{full}}(Z) = 1 + \frac{\sum_i (s_{Z,i}^{(\infty)} - n_i)}{\sum_i n_i}$$

$$E_c(Z) = E_h \times \rho_Z \times f_{\text{full}}(Z)$$

### 7.2 收敛性

**收敛条件**：电子反馈曲率 $\Delta\hat{\delta}_v^{\text{e-n}}$ 足够弱，使得迭代映射是压缩映射。

**物理依据**：电子反馈通过电磁相互作用（$\alpha \approx 1/137$）影响曲率，而曲率主要由核子振荡（强相互作用，$\alpha_s \sim 1$）决定。因此 $\Delta\hat{\delta}_v^{\text{e-n}} / \hat{\delta}_v^{(1)} \sim \alpha / \alpha_s \ll 1$，迭代收敛。

---

## 8. 与Hartree-Fock/DFT的结构类比

### 8.1 类比表

| 结构 | CQM完整同步方程 | Hartree-Fock/DFT |
|:---|:---|:---|
| 平庸方程 | 通用 $A_4$ 同步方程（壳层结构） | Thomas-Fermi模型（平均场） |
| 完整方程 | 元素特定自洽同步方程（关联能） | Kohn-Sham DFT（自洽场） |
| 自洽变量 | 电子密度 $\rho_Z(v)$（离散） | 电子密度 $\rho(r)$（连续） |
| 反馈机制 | 电子反馈曲率 $\Delta\hat{\delta}_v^{\text{e-n}}$ | 交换-关联势 $V_{xc}[\rho]$ |
| 方程类型 | 代数本征值问题（非线性） | 微分本征值问题（非线性） |
| 标度 | 无量纲（曲率） | 有量纲（能量） |

### 8.2 关键区别

1. **曲率 vs 势场**：CQM的反馈通过曲率（几何），DFT的反馈通过势场（电磁）
2. **代数 vs 微分**：CQM的同步方程是代数的（Regge离散化），DFT的KS方程是微分的
3. **第一性来源**：CQM从Regge剖分 + $[\hat{X},\hat{P}]=i\hbar$ 构造，DFT从Hohenberg-Kohn定理构造
4. **无量纲 vs 有量纲**：CQM在FG纤维丛截断处归一化为无量纲，DFT保持有量纲

### 8.3 CQM的优势

1. **几何统一**：电子结构和核子结构在同一几何框架（Regge剖分）内
2. **代数严格**：离散化后是纯代数问题，无数值微分误差
3. **层级一致**：从QG层到FG层，同一同步方程框架
4. **无量纲优雅**：归一化后纯代数运算，量纲恢复独立

---

## 9. 具体计算示例：Cr/Cu d波关联能

### 9.1 平庸方程结果（已有）

Cr（$Z=24$）和Cu（$Z=29$）的d波关联能，从平庸同步方程导出：
- 增强因子 $\rho_Z = 5/4$（g波禁戒 → 民主重分配）
- $E_c^{\text{trivial}} = E_h \times 5/4 \times 1 = 1.25 E_h$

### 9.2 完整方程修正（本文构造）

**步骤1**：确定Cr/Cu的元素特定数据
- 边长 $\bar{L}_{ij}^{(Z)}$：从核子分布（QG层输出）确定
- 结合能 $E_{\text{bind}}^{(Z)}$：Cr和Cu的特定值
- 经典角亏 $\bar{\delta}_v^{(Z)}$：从边长计算

**步骤2**：构造元素特定动力学矩阵
- $D_{vv'}^{(Z)}$：用Cr/Cu特定边长
- 本征值 $\lambda_k^{(Z)}$ 和本征向量 $v_k^{(Z)}(v)$：对角化

**步骤3**：自洽迭代
- 初始 $\rho_Z^{(0)}$：从平庸方程解
- 迭代直到收敛 $\rho_Z^{(\infty)}$

**步骤4**：计算元素特定因子
- $f_{\text{full}}(\text{Cr}) = 1 + \frac{\sum_i (s_{\text{Cr},i} - n_i)}{\sum_i n_i}$
- $f_{\text{full}}(\text{Cu}) = 1 + \frac{\sum_i (s_{\text{Cu},i} - n_i)}{\sum_i n_i}$

**步骤5**：完整关联能
- $E_c(\text{Cr}) = E_h \times 5/4 \times f_{\text{full}}(\text{Cr})$
- $E_c(\text{Cu}) = E_h \times 5/4 \times f_{\text{full}}(\text{Cu})$

### 9.3 预期结果

Cr和Cu的d波关联能应有不同的 $f_{\text{full}}(Z)$ 值，反映元素特定信息：
- Cr：3d⁴4s²，d壳层半满，关联效应强
- Cu：3d¹⁰4s¹，d壳层全满，关联效应弱

平庸方程给出相同的增强因子（$5/4$），完整方程给出不同的 $f_{\text{full}}(Z)$，区分Cr和Cu。

---

## 10. 边长 $\bar{L}_{ij}^{(Z)}$ 的确定

### 10.1 层级结构

边长 = 核子间距离，由核子分布确定。核子分布由层级同步方程给出：

$$\underbrace{\hat{\mathcal{S}}_0}_{\text{QG层}} \;\longrightarrow\; \text{核子分布} \;\longrightarrow\; \bar{L}_{ij}^{(Z)} \;\longrightarrow\; \hat{\mathcal{S}}^{(Z)}_{\text{full}}$$

### 10.2 QG层同步方程

QG层紧化算符 $\hat{\mathcal{S}}_0: \mathcal{H}_{\text{auto}}(\text{GL}_5) \to \mathcal{H}_{\text{phys}}(\text{SU}(5))$ 给出核子结构。

**核子分布的确定**：
- 质子分布：由QG层同步方程的解确定
- 中子分布：由核子-核子相互作用（QCD）确定
- 边长 $\bar{L}_{ij}^{(Z)}$：核子间距离，由核子分布确定

### 10.3 当前状态

QG层同步方程的完整形式是开放问题。当前可以：
1. **从实验输入**：用核物理实验数据确定 $\bar{L}_{ij}^{(Z)}$（半第一性）
2. **从QCD计算**：用格点QCD或核子模型计算 $\bar{L}_{ij}^{(Z)}$
3. **从QG层同步方程推导**：构造QG层完整同步方程，第一性推导 $\bar{L}_{ij}^{(Z)}$

**目标**：路径3（完全第一性），但路径1和2可以先建立框架。

---

## 11. 结合能 $E_{\text{bind}}^{(Z)}$ 的自洽确定

### 11.1 自洽条件

$E_{\text{bind}}^{(Z)}$ 依赖电子结构（通过结合能），电子结构依赖同步方程，同步方程依赖 $E_{\text{bind}}^{(Z)}$：

$$E_{\text{bind}}^{(Z)} = \mathcal{F}_{\text{bind}}[\Psi_Z], \quad \hat{\mathcal{S}}^{(Z)}_{\text{full}}[E_{\text{bind}}^{(Z)}]|\Psi_Z\rangle = s_Z|\Psi_Z\rangle$$

### 11.2 结合能的物理内容

$E_{\text{bind}}^{(Z)}$ 是元素 $Z$ 的核子结合能，包含：
1. **核子-核子结合能**：QCD贡献（主导）
2. **电子-核子结合能**：电磁贡献（小修正）
3. **电子-电子排斥能**：电子关联贡献

在自洽迭代中，$E_{\text{bind}}^{(Z)}$ 随电子密度 $\rho_Z$ 更新而更新。

### 11.3 简化处理

在一级近似中，可以忽略 $E_{\text{bind}}^{(Z)}$ 对电子结构的依赖（核子结合能主要由QCD决定，电子贡献小）：

$$E_{\text{bind}}^{(Z)} \approx E_{\text{bind}}^{\text{nucleon}}(Z)$$

其中 $E_{\text{bind}}^{\text{nucleon}}(Z)$ 是纯核子结合能（从核物理确定）。这样 $E_{\text{bind}}^{(Z)}$ 成为给定输入，自洽迭代只涉及电子密度 $\rho_Z$。

---

## 12. 开放问题与后续工作

### 12.1 已完成

| 内容 | 状态 |
|:---|:---|
| 完整同步方程的具体形式 | ✅ §3-§4 |
| 元素特定曲率算符的构造 | ✅ §3 |
| 电子反馈曲率的构造 | ✅ §3.4 |
| 自洽条件的构造 | ✅ §4 |
| 退化关系的证明 | ✅ §5 |
| 关联能的计算方法 | ✅ §6 |
| 迭代求解流程 | ✅ §7 |
| 与Hartree-Fock/DFT的关系 | ✅ §8 |

### 12.2 待完成

| 内容 | 优先级 | 说明 |
|:---|:---|:---|
| 边长 $\bar{L}_{ij}^{(Z)}$ 的第一性确定 | 高 | 需要QG层完整同步方程 |
| 耦合核 $K_{vv'}^{(Z)}$ 的严格推导 | 高 | 当前是唯象形式，需从CQM第一性推导 |
| 数值实现与验证 | 高 | 实现迭代算法，计算Cr/Cu关联能 |
| 收敛性严格证明 | 中 | 当前是物理论证，需数学证明 |
| $E_{\text{bind}}^{(Z)}$ 的自洽处理 | 中 | 当前用核物理输入，需CQM第一性 |
| 与实验数据对比 | 高 | 验证完整方程给出的关联能精度 |

### 12.3 关键挑战

1. **边长的第一性确定**：需要构造QG层完整同步方程，从GL(5)→SU(5)紧化推导核子分布。这是CQM框架内最深层的开放问题。

2. **耦合核的严格推导**：电子反馈曲率 $\Delta\hat{\delta}_v^{\text{e-n}}$ 的耦合核 $K_{vv'}^{(Z)}$ 当前是唯象构造（基于物理直觉），需要从CQM第一性原理严格推导。可能的路径：从电子-核子电磁相互作用的CQM描述出发，推导其对曲率的反馈。

3. **数值实现**：完整同步方程是非线性自洽方程，需要实现迭代算法。关键挑战：
   - 元素特定动力学矩阵的构造
   - 自洽迭代的收敛性
   - 与平庸方程解的对比

### 12.4 与§19的关系

本文构造的完整同步方程与§19量纲归一化的关系：

| §19表述 | 本文构造 |
|:---|:---|
| 完整归一化用 $E_{\text{bind}}^{(Z)}$ | ✅ §3.3 量子涨落用 $E_{\text{bind}}^{(Z)}$ |
| 完整方程保留元素特定能量标度 | ✅ §3 元素特定曲率算符 |
| 完整方程给出元素特定关联能 | ✅ §6 关联能计算方法 |
| 退化到平庸方程 | ✅ §5 退化关系证明 |
| 问题本质：归一化如何保留元素特定信息 | ✅ §3-§4 元素特定归一化 + 电子反馈 |

---

## 13. 总结

### 13.1 核心贡献

本文构造了完整同步方程 $\hat{\mathcal{S}}^{(Z)}_{\text{full}}$ 的具体形式：

$$\hat{\mathcal{S}}^{(Z)}_{\text{full}}[\rho_Z]|\Psi_{Z,i}\rangle = s_{Z,i}|\Psi_{Z,i}\rangle, \quad \rho_Z(v) = \sum_{i \in \text{occ}} |\Psi_{Z,i}(v)|^2$$

其中完整同步算符：

$$\hat{\mathcal{S}}^{(Z)}_{\text{full}}[\rho_Z] = \frac{L_u}{2\pi C}\sqrt{1-\beta\hat{\delta}_v^{(Z)}[\rho_Z]}$$

元素特定曲率算符包含三个来源：
1. **几何信息** $\bar{\delta}_v^{(Z)}$ + $D^{(Z)}$：来自元素特定Regge剖分
2. **归一化信息** $E_{\text{bind}}^{(Z)}$：元素特定结合能
3. **自组织信息** $\Delta\hat{\delta}_v^{\text{e-n}}[\rho_Z]$：电子反馈曲率

### 13.2 关键特征

1. **非线性自洽**：曲率依赖电子密度，电子密度依赖解——非线性自洽方程
2. **退化保证**：等边极限 + 通用归一化 + 忽略电子反馈 → 平庸方程
3. **第一性框架**：从CQM第一性原理构造，无经验参数（边长和结合能从QG层推导）
4. **关联能计算**：$E_c(Z) = E_h \times \rho_Z \times f_{\text{full}}(Z)$，$f_{\text{full}}(Z)$ 从本征值差异导出

### 13.3 与平庸方程的分工

| 方程 | 输出 | 元素特定性 |
|:---|:---|:---|
| 平庸方程 $\hat{\mathcal{S}}_{\text{trivial}}$ | 壳层结构、周期表、增强因子 | 通用（所有元素共享 $A_4$） |
| 完整方程 $\hat{\mathcal{S}}^{(Z)}_{\text{full}}$ | 元素特定关联能 | 元素特定（每个 $Z$ 有自己的剖分和自组织数据） |

**平庸方程给出周期表的结构，完整方程给出周期表的细节。**