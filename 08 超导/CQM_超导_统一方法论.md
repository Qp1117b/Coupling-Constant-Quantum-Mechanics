# CQM超导统一方法论：四层FG纤维丛与相对第一性计算链

> 本文档用统一纤维丛语言严格描述CQM超导预测的方法论：四层FG（元素/分子/晶胞/超导）各自是不同的纤维丛，剖分对象不同，但从Regge剖分到Tc的计算步骤完全统一且第一性。

## 1. 四层FG的纤维丛定义

### 1.1 纤维丛四元组

每层FG是一个主丛 $(M_\ell, P_\ell, \pi_\ell, G_\ell)$：

- $M_\ell$：底空间（剖分对象的空间分布）
- $P_\ell$：全空间（主丛）
- $\pi_\ell: P_\ell \to M_\ell$：投影映射
- $G_\ell$：结构群（对称群作用在纤维上）

配以联络 $\mathcal{A}_\ell$ 和曲率 $\mathcal{F}_\ell = d\mathcal{A}_\ell + \mathcal{A}_\ell \wedge \mathcal{A}_\ell$。

| 层级 | 底空间 $M_\ell$ | 结构群 $G_\ell$ | 联络 $\mathcal{A}_\ell$ | 剖分对象 |
|:---|:---|:---|:---|:---|
| 元素FG | 质子+中子分布 | 核子对称群（从壳层结构） | 核子间联络 | 质子和中子分布 |
| 分子FG | 原子分布 | 分子点群 | 原子间联络（化学键） | 原子分布 |
| 晶胞FG | 原子/分子在晶胞中分布 | 空间群 | 晶胞中原子/分子间联络 | 原子/分子分布 |
| 超导 | 晶胞分布的单位分布 | $U(1)/\mathbb{Z}_n$ | 超导同步联络 | 单位分布 |

### 1.2 层级嵌套

四层FG的纤维丛之间存在层级嵌套——每层的底空间是上层的纤维：

$$P_{\text{el}} \hookrightarrow P_{\text{mol}} \hookrightarrow P_{\text{cell}} \hookrightarrow P_{\text{super}}$$

- $M_{\text{mol}}$ 的每个点（原子）上附着 $P_{\text{el}}$（核子分布的主丛）
- $M_{\text{cell}}$ 的每个点（原子/分子位置）上附着 $P_{\text{mol}}$（原子分布的主丛）
- $M_{\text{super}}$ 的每个点（单位分布位置）上附着 $P_{\text{cell}}$（晶胞分布的主丛）

### 1.3 元素FG的纤维丛

**底空间** $M_{\text{el}}$：原子核内Z个质子和N个中子的空间分布。

**结构群** $G_{\text{el}}$：从核壳层结构（SU(5)重组实现→A4嘉当矩阵→壳层{2,6,10,14}）第一性导出的核子对称群。

**电子轨道是元素FG的谱体现**，不是剖分对象本身：
- 电子轨道主要是U(1)耦合常数涨落的体现
- 有SO(2)或SU(2)的影响
- 同位素（中子数N不同）也有影响
- 电子壳层反映核子分布几何（电子是关系产物），可间接确定对称性

从Z到纤维丛的路径：质子数=Z，中子数N从稳定同位素给出，核子分布对称性从壳层结构第一性导出。118个元素有限，可穷尽列举。

### 1.4 分子FG的纤维丛

**底空间** $M_{\text{mol}}$：分子中各原子的空间分布。

**结构群** $G_{\text{mol}}$：分子点群（从分子对称性给出）。

**联络** $\mathcal{A}_{\text{mol}}$：原子间联络，从化学键给出。

外部数据：键长、键角、分子点群（从实验或DFT）。

### 1.5 晶胞FG的纤维丛

**底空间** $M_{\text{cell}}$：晶胞中原子/分子的空间分布。

**结构群** $G_{\text{cell}}$：空间群。

**联络** $\mathcal{A}_{\text{cell}}$：晶胞中原子/分子间联络，从晶格结构给出。

外部数据：空间群、Wyckoff位置、晶格常数（从X射线衍射）。

### 1.6 超导的纤维丛

**底空间** $M_{\text{super}}$：晶胞分布的单位分布——能体现全局分布的局域单元。

**结构群** $G_{\text{super}} = U(1)/\mathbb{Z}_n$：超导结构群，$n$由资格条件筛选。

**联络** $\mathcal{A}_{\text{super}}$：超导同步联络，从晶胞FG联络诱导。

超导剖分不是对整个晶体剖分，而是取单位分布进行Regge剖分。N在Debye积分中消去（局域量），不需处理宏观材料。

## 2. Regge剖分与纤维丛的对应

### 2.1 Regge剖分作为底空间的三角剖分

给定纤维丛 $(M_\ell, P_\ell, \pi_\ell, G_\ell)$，对底空间 $M_\ell$ 进行Regge剖分 $T_\ell$：

- **顶点** = $M_\ell$ 中的离散点（剖分对象的位置）
- **边** = 联络 $\mathcal{A}_\ell$ 的离散化（连接顶点的路径，给出平移规则）
- **面** = 曲率 $\mathcal{F}_\ell$ 的离散化（绕回路的和乐）

### 2.2 角亏作为底空间曲率集中

顶点 $v$ 处的角亏 $\delta_v$ 是底空间曲率在该点的集中：

$$\delta_v = 2\pi - \sum_i \theta_i \quad \text{(2D, Gauss-Bonnet)}$$

等价于绕顶点 $v$ 的和乐：

$$W_v = \exp(i \delta_v \hat{T}) \in G_\ell$$

其中 $\hat{T}$ 是结构群 $G_\ell$ 的生成元。

### 2.3 联络离散化为动力学矩阵

联络 $\mathcal{A}_\ell$ 在Regge剖分上离散化为力常数矩阵：

$$K_{ij} = \frac{\partial^2 V}{\partial u_i \partial u_j}$$

其中 $V$ 是Regge作用量，$u_i$ 是顶点 $i$ 的位移。动力学矩阵：

$$D_{ij} = \frac{K_{ij}}{\sqrt{m_i m_j}}$$

### 2.4 曲率量子涨落为角亏涨落

底空间曲率的零温量子涨落给出角亏涨落：

$$\Delta\delta_0^2 = \sum_q \left|\frac{\partial \delta_v}{\partial u_q}\right|^2 \cdot \frac{\hbar}{2\omega_q}$$

其中 $\omega_q$ 是纤维上的量子谐振子本征频率（声子频率）。

## 3. 同步算符与Tc闭式

### 3.1 同步算符作为主丛谱算符

每层FG的同步算符 $\hat{\mathcal{S}}_\ell$ 是该层主丛 $P_\ell$ 上的谱算符：

$$\hat{\mathcal{S}}_\ell = V_0 + V_{\text{角亏激活}}(T)$$

其中 $V_0$ 是质数势（从QG基态紧化结构继承），$V_{\text{角亏激活}}(T)$ 是角亏激活势（从底空间曲率涨落给出）。

### 3.2 本征值与温度依赖

同步算符本征值：

$$\lambda_n(T) = \gamma_n - \frac{\beta^2 \Delta\delta_v(T)^2 (n^2-1)}{4n^2 (1-\beta\delta_v)}$$

其中：
- $\gamma_n$：第 $n$ 个黎曼零点虚部（零温极限，从S1谱方程给出）
- $\beta = \frac{1}{4\pi}\ln\frac{L}{a}$：系统尺寸严格确定（$L$系统尺寸，$a$晶格常数）
- $\delta_v$：底空间角亏（从Regge剖分计算）
- $\Delta\delta_v(T) = \Delta\delta_0 \sqrt{\tanh(\hbar\Omega_0 / 2k_B T)}$：温度依赖的角亏涨落

### 3.3 Tc从本征值交叉导出

超导相变发生在同步算符本征值交叉：

$$\lambda_2(T_c) = \lambda_1(T_c)$$

解出Tc闭式：

$$T_c = \frac{\theta_D}{2\,\text{arccoth}(x)}, \quad x = \frac{3\beta^2 \Delta\delta_0^2}{16(1-\beta\delta_v)(\gamma_2-\gamma_1)}$$

超导条件 $x > 1$ 等价于：

$$\beta\delta_v + \frac{3\beta^2}{16(\gamma_2-\gamma_1)} \Delta\delta_0^2 > 1$$

## 4. 统一计算步骤（纤维丛语言）

给定任意层FG的纤维丛 $(M_\ell, P_\ell, \pi_\ell, G_\ell)$，从剖分到Tc的步骤完全统一：

**步骤A：Regge剖分** — 对底空间 $M_\ell$ 进行三角剖分 $T_\ell$（顶点+边+面）

**步骤B：角亏** — 逐顶点计算底空间曲率集中：$\delta_v = 2\pi - \sum_i \theta_i$（Gauss-Bonnet定理）

**步骤C：动力学矩阵** — 联络 $\mathcal{A}_\ell$ 离散化为力常数矩阵 $K_{ij}$，动力学矩阵 $D_{ij} = K_{ij}/\sqrt{m_i m_j}$（Regge作用量变分）

**步骤D：声子谱** — 纤维上量子谐振子本征频率：$\omega_q = \sqrt{\text{eig}(D)}$，Debye频率 $\omega_D = \max(\omega_q)$（量子谐振子对角化）

**步骤E：角亏涨落** — 底空间曲率零温量子涨落：$\Delta\delta_0^2 = \sum_q |\partial\delta_v/\partial u_q|^2 \cdot \hbar/(2\omega_q)$

**步骤F：Tc闭式** — 主丛结构群上同步算符本征值交叉：$T_c = \theta_D / (2\,\text{arccoth}(x))$

每步都是CQM方程严格导出，无经验拟合参数。

## 5. 相对第一性的界定

### 5.1 完全第一性部分

- 元素FG纤维丛构造：从Z→核子分布→结构群→主丛，无外部输入
- 从剖分到Tc的步骤：步骤A-F全部从CQM方程严格导出
- 物理常数：$\beta=\frac{1}{4\pi}\ln\frac{L}{a}$, $C^2=2/3$, $\gamma_1$, $\gamma_2$ 等从CQM方程给出

### 5.2 需要外部数据的部分

- 分子FG纤维丛：需要分子键合几何（键长、键角）确定底空间 $M_{\text{mol}}$
- 晶胞FG纤维丛：需要晶体结构（空间群、Wyckoff位置）确定底空间 $M_{\text{cell}}$
- 超导纤维丛：需要晶体结构确定单位分布 $M_{\text{super}}$

### 5.3 相对第一性的含义

CQM超导预测是相对第一性：
- 不从CQM方程推导底空间分布（分布是组织原则/外部输入）
- 但从纤维丛到Tc的步骤完全第一性（无经验拟合）
- 元素FG底空间完全第一性（可穷尽列举）
- 分子FG/晶胞FG/超导底空间需要外部数据，但计算步骤统一

对比BCS：BCS需要电声耦合 $\lambda$ 和库仑赝势 $\mu^*$（经验参数），CQM不需要这些——CQM只需要晶体结构（实验输入确定底空间），从纤维丛到Tc的步骤完全第一性。

## 6. 元素FG穷尽列举方案

### 6.1 从Z到纤维丛

元素FG的纤维丛从Z第一性构造：

1. 质子数=Z，中子数N从稳定同位素给出
2. 底空间 $M_{\text{el}}$ = Z+N个核子的空间分布
3. 核壳层结构从SU(5)重组实现→A4嘉当矩阵→壳层{2,6,10,14}第一性导出
4. 结构群 $G_{\text{el}}$ 从核子分布对称性给出
5. 嘉当矩阵的Dynkin图给出Regge剖分的顶点和边

### 6.2 从Dynkin图到Regge剖分

嘉当矩阵的Dynkin图给出顶点和边：
- A1（s壳层）：1个顶点，无边
- A3（p壳层）：3个顶点链
- A4（d壳层）：4个顶点链

从1D Dynkin图构造2D Regge剖分（补面）：
- A3链→1个三角形
- A4链→2个三角形

### 6.3 预计算表

对118个元素预计算：
1. 质子数Z、中子数N
2. 核壳层结构与嘉当矩阵
3. Dynkin图（顶点+边）
4. 2D Regge剖分（补三角形面）
5. 顶点位置（从核子分布对称性）
6. 角亏 $\delta_v$（从剖分计算）

存储为元素FG纤维丛表，供分子FG和晶胞FG查用。

## 7. 分子FG构造方案

### 7.1 从元素FG纤维丛组合

分子FG纤维丛 = Σ元素FG纤维丛 + 跨原子联络

1. 查元素FG表获取各元素的主丛（核子级别）
2. 构造分子底空间 $M_{\text{mol}}$：顶点=原子位置，边=化学键
3. 跨原子联络 $\mathcal{A}_{\text{mol}}$ 从化学键给出
4. 补跨原子三角形面
5. 计算分子Regge剖分（原子级别）

### 7.2 外部数据需求

- 键长：从实验或DFT
- 键角：从实验或DFT
- 分子点群：从实验或DFT

## 8. 晶胞FG构造方案

### 8.1 从分子FG纤维丛周期化

晶胞FG纤维丛 = 分子FG纤维丛 + 空间群周期化

1. 构造分子FG纤维丛（原子级别）
2. 应用空间群操作生成周期结构
3. 取一个晶胞的底空间 $M_{\text{cell}}$
4. 晶胞联络 $\mathcal{A}_{\text{cell}}$ 从晶格结构给出
5. 计算晶胞Regge剖分和角亏 $\delta_v$

### 8.2 外部数据需求

- 空间群：从X射线衍射
- Wyckoff位置：从X射线衍射
- 晶格常数：从X射线衍射

## 9. 超导Tc计算：从单位分布到Tc

### 9.1 单位分布的选取

从晶胞FG底空间 $M_{\text{cell}}$ 中选取单位分布——能体现全局分布的局域单元：
- 单位分布是最小结构单元，其角亏能代表全局角亏
- 超导底空间 $M_{\text{super}}$ = 单位分布
- 超导联络 $\mathcal{A}_{\text{super}}$ 从晶胞FG联络诱导
- N在Debye积分中消去（局域量），不需处理宏观材料

### 9.2 从单位分布到Tc

对超导纤维丛 $(M_{\text{super}}, P_{\text{super}}, \pi_{\text{super}}, G_{\text{super}})$ 执行统一步骤A-F（§4），得到Tc闭式。

## 10. 实现路线

Phase 1: 元素FG穷尽列举（完全第一性）
- cqm_element_fg.py
- 118个元素→核子分布→纤维丛→嘉当矩阵→Dynkin图→Regge剖分
- 预计算元素FG纤维丛表（顶点位置+边+面+角亏）

Phase 2: 统一从纤维丛到Tc的步骤（完全第一性）
- cqm_regge_to_tc.py
- 输入：Regge剖分（顶点位置+边+面）+原子质量
- 步骤A-F：剖分→角亏→动力学矩阵→声子频率→角亏涨落→Tc闭式

Phase 3: 分子FG构造（需化学数据）
- cqm_cell_fg_hybrid.py（分子FG无独立脚本，取"元素FG拓扑+晶胞FG晶格参数修正"杂交流水线）
- 输入：化学式+分子结构（键长/键角）
- 从元素FG表组合+跨原子联络→分子纤维丛→Regge剖分
- 调用Phase 2计算Tc

Phase 4: 晶胞FG构造（需晶体数据）
- cqm_cell_fg_to_tc.py
- 输入：晶胞结构（空间群/Wyckoff位置/晶格常数）
- 从分子FG+空间群周期化→晶胞纤维丛→Regge剖分
- 选取单位分布
- 调用Phase 2计算Tc

## 11. 与之前方法的对比

| | 之前（闭式公式跳步） | 现在（纤维丛严格推导） |
|--|--|--|
| 数学框架 | 无统一框架 | 四层FG纤维丛 $(M_\ell, P_\ell, \pi_\ell, G_\ell)$ |
| 剖分对象 | 不区分层级 | 元素=核子分布，分子=原子分布，晶胞=原子/分子分布，超导=单位分布 |
| 角亏 $\delta_v$ | 经验近似0.01 | 底空间曲率集中（Gauss-Bonnet） |
| 动力学矩阵 | 不构造 | 联络 $\mathcal{A}_\ell$ 离散化 |
| 声子频率 | 从数据库取 | 纤维上量子谐振子本征频率 |
| 角亏涨落 | 闭式公式跳步 | 底空间曲率量子涨落 |
| Tc | 自由能公式 | 同步算符本征值交叉（主丛谱算符） |
| 严格性 | 含数值拟合 | 从纤维丛到Tc完全第一性 |

## 12. 核心方程（从CQM方程严格导出）

**Tc闭式**（同步算符本征值交叉 $\lambda_2(T_c) = \lambda_1(T_c)$）：

$$T_c = \frac{\theta_D}{2\,\text{arccoth}(x)}, \quad x = \frac{3\beta^2 \Delta\delta_0^2}{16(1-\beta\delta_v)(\gamma_2-\gamma_1)}$$

**角亏**（底空间曲率集中，Gauss-Bonnet）：

$$\delta_v = 2\pi - \sum_{i} \theta_i$$

**和乐**（绕顶点 $v$ 的结构群元素）：

$$W_v = \exp(i \delta_v \hat{T}) \in G_\ell$$

**动力学矩阵**（联络离散化）：

$$D_{ij} = \frac{K_{ij}}{\sqrt{m_i m_j}}, \quad K_{ij} = \frac{\partial^2 V_{\text{Regge}}}{\partial u_i \partial u_j}$$

**声子频率**（纤维上量子谐振子本征值）：

$$\omega_q^2 = \text{eig}(D)$$

**角亏涨落**（底空间曲率零温量子涨落）：

$$\Delta\delta_0^2 = \sum_q \left|\frac{\partial \delta_v}{\partial u_q}\right|^2 \cdot \frac{\hbar}{2\omega_q}$$

**同步算符**（主丛谱算符）：

$$\hat{\mathcal{S}}_\ell = V_0 + V_{\text{角亏激活}}(T), \quad \lambda_n(T) = \gamma_n - \frac{\beta^2 \Delta\delta_v(T)^2 (n^2-1)}{4n^2 (1-\beta\delta_v)}$$

**超导条件**：

$$x > 1 \iff \beta\delta_v + \frac{3\beta^2}{16(\gamma_2-\gamma_1)} \Delta\delta_0^2 > 1$$
