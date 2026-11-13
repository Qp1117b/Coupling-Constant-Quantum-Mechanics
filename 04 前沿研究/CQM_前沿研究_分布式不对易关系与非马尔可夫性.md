# 分布式不对易关系：非马尔可夫性的结构起源（理论构造）

**作者**：ruster

> **定位**：本文属“04 前沿研究”，是“分布式不对易关系”（Distributed Noncommutative Relation, DNR）研究线的**理论构造卷**。任务是把 DNR 从工作概念推进为一组可陈述的定义、可推导的结构与可计算的判据，并展开它与 CQM 既有机制的关联。同研究线的审校性记录另见同目录文档，本文不重复其清单式结论。
>
> **标注约定**：
> - `【标准数学】` 外部数学事实，给出出处；`【文献】` 外部研究结论，附 arXiv／DOI；`【框架】` CQM 既有表述，附原文位置；`【构造假设】` 本文新构造、未证；`【待推】` 未完成项，编号 E1–E5。
> - 外部结论只作对照，不构成 CQM 的证明；框架内容一律引原文，本文不改动既有定义、数值与全局缺口状态，不新开全局缺口编号。
> - `☯` 为相变量子（耦合空间的作用量量子），作数学量使用。

---

## 摘要

本文把 DNR 构造为一条可推导的理论链，得到五个结构性结论。

**其一（代数层）**：约束代数 $[G,\sum_i L_i]=iC$ 的作用不是“产生记忆”，而是**禁止对角化压缩**。由罗伯逊–薛定谔不等式，$C\neq0$ 排除了 $G$ 与 $\sum_iL_i$ 的联合本征态，也排除了二者的完美相关（即 $G$ 为局部集体量之函数）。由此，“单点共时截面必损”由代数保证，而非由粗粒化选择。

**其二（动力学层）**：对双线性高斯模型，记忆核可分解为奇通道与偶通道。奇通道由对易子生成，是**与态无关的 $c$ 数**，由哈密顿量固定，承载响应（Kubo）；偶通道由反对易子生成，依赖浴的协方差矩阵（含跨节点元），承载噪声与退相干。DNR 的联合史只能进入偶通道。

**其三（载体分类）**：记忆有三个载体——谱分布 $J(\omega)$（含空间非均匀）、联合协方差 $\Sigma_B$、高阶累积量。原草稿的 $K_{\rm nc}$ 属于第三类（非线性／非高斯层）；在双线性高斯层，因奇部态无关，$K_{\rm nc}$ 恒为零。$K=K_{\rm cl}+C K_{\rm nc}$ 由此获得精确的定义域，而不是在所有层级通用。

**其四（阈值）**：纤维判据在模型中线性实现——两次制备若单点二阶矩相同、跨节点协方差不同，则未来响应之差正比于交叉项。阈值 $\ell_*$ 不是拟合参数，而是**联合协方差的关联长度**。公共浴情形另给出一条“不可还原”的动力学判据：核正比于 $(\sum_i c_i)^2$ 而非 $\sum_i c_i^2$，记忆权重随 $N^2$ 增长而不是 $N$。

**其五（判据的物理意义）**：非对易贡献比 $R_{\rm nc}$ 有闭式 $R_{\rm nc}=\tanh(\hbar\omega/2k_BT)$（单模；多模为加权平均），它度量的是涨落—耗散比，即量子性与温度，不度量联合史。DNR 的特异判据须换成“同切片、异协方差”的响应差 $R_{\rm DNR}$。

CQM 侧的关联给出一个可陈述的构造：全局集体量取节点对数耦合的几何平均 $\hat u_G=\frac1N\sum_i\hat u_i$，其共轭为总固有时流速 $\sum_i v_\tau^{(i)}$，二者对易子为 $\mathrm{i}☯$；$N=1$ 时退化为框架既有的单个一维海森堡对。经角亏—固有时流速接口，该不等式落成 $\Delta u_G\cdot\Delta\bigl(\sum_i\sqrt{1-\beta\delta_v^{(i)}}\bigr)\ge ☯/2$。此构造连同其定义域限制一并登记为【构造假设】。

**关键词**：分布式不对易关系；非马尔可夫性；记忆核；初态关联；涨落—耗散关系；约束代数；CQM 关联

---

## 1 非马尔可夫性的四种来源

非马尔可夫性——共时状态不足以使未来与过去条件独立——在文献中主要有三条既有来源，本文追加第四条候选。

| 来源 | 机制 | 数学位置 |
|:---|:---|:---|
| 环境记忆 | 浴的自由度被消去后留下核 | Nakajima–Zwanzig 核 $\mathcal K(t-s)$【标准数学】[1][2] |
| 无序与粗粒化 | 参数分布的系综平均或分辨率不足 | 平均核、有效生成元 |
| 非马尔可夫度量之下的强耦合 | 谱结构非平（能级近简并、结构化浴） | 核的振荡项 |
| **结构约束（本文）** | 全局约束与局部分布式差异不对易，截面读不出联合关联 | 约束代数＋非齐次项 |

【文献】前三条来源之外，近年的实验与理论把“历史依赖”推到了材料本体层面：

- UTe₂ 的电可控超导记忆：在 SC1／SC2 共存区，直流电流脉冲可把体系推入或推出一具有更高临界电流密度 $J_c$ 的亚稳态，记忆保持很长时间，缓扫电流可擦除；作者把它归于非平衡玻璃态涡旋的淬火／退火，并强调该功能“似为 UTe₂ 超导序本身的内禀属性”[4]。
- 超导量子比特噪声的核重构：通道分辨的后马尔可夫主方程可从噪声数据中重构振荡型记忆核【待推 E1，方法细节见 [7]】。
- 耗散挫败：一维相位模型经两个不对易算符与环境耦合（分流电阻与对地电阻），给出非单调的量子相变临界线[5]。
- 过程张量：非马尔可夫过程可由“过程”而非“状态”完备描述，边界关联不可因子化[6]。

【文献】过程优先的框架与本议题共享语法：自旋泡沫以历史求和实现约束[14]，张量网络给出离散组合语法[17]。

【分析】这些现象都说明“历史依赖是真实对象”，但都不判决其来源是结构性的还是环境性的。DNR 若要有内容，必须给出**可算的载体与可判的判据**，而不是再命名一次现象。以下四节依次给出代数层、动力学层、阈值层与判据层。

---

## 2 定义

### 2.1 结构六要素

**定义 1（DNR 结构）** 一个物理系统满足 DNR，若存在：

| # | 要素 | 内容 | 本文的位置 |
|:---|:---|:---|:---|
| 1 | 全局集体变量 | $G$，可涨落，受约束 | §3.1 |
| 2 | 局部分布式变量 | $\{L_i\}_{i=1}^N$，定义在节点上 | §4.1 |
| 3 | 不对易关系 | $[G,\sum_iL_i]=iC$，或狄拉克括号非零 | §3 |
| 4 | 局部分布式差异 | 各节点 $L_i$ 不可统一为单点全局值 | §3.3、§5.2 |
| 5 | 层级不可还原 | $G$ 由 $\{L_i\}$ 构成／约束，但不是 $\sum_iL_i$ 的简单函数 | §3.2、§5.2 |
| 6 | 历史写入 | $G$ 涨落路径与 $\{L_i\}$ 分布的联合关联承载历史 | §4.3 |

要素 1–6 是**结构候选**，单独不构成定理。理论构造的任务，是给每一条找到它在哪个数学层上兑现。

### 2.2 描述类

单点共时属性取

$$\phi(v)=f\bigl(G|_{N_k(v)}\bigr),\qquad S_t=\{\phi(v)\}_{v\in V},$$

即每个站点只读半径 $k$ 内邻域。描述类 $\mathcal S_\ell$ 由四条约束同时确定：

| 约束 | 内容 | 排除的退化 |
|:---|:---|:---|
| 单一时刻截面 | 只取一个共时切片 | 非共时关系态 |
| 支撑半径有界 | 站点量只依赖半径 $\ell$ 内邻域 | $\ell$ 取到全系统使投影单射 |
| 站点规则位置无关 | $f$ 不随位置特设 | 把历史藏进位置编码 |
| 不显式携带历史标号 | 无任意历史堆栈 | 人为堆栈冒充载体 |

### 2.3 DNR 非马尔可夫性

**定义 2（DNR 非马尔可夫性）** DNR 系统相对于 $\mathcal S_\ell$ 是非马尔可夫的，若存在 $D\neq D'$ 使 $\pi(D)=\pi(D')$ 且

$$P(\text{未来}\mid D)\neq P(\text{未来}\mid D').$$

即纤维混合。配合 §5 的阈值，该定义可写成尺度命题：

$$\exists\,\ell_*:\quad \ell<\ell_* \text{ 时 }\mathcal S_\ell\text{ 充分};\qquad \ell\ge\ell_*\text{ 时存在反例}.$$

这样“必然非马尔可夫”不是定义真理，而是一个可判伪的建模断言，且 $\ell_*$ 有物理意义（§5.1）。

---

## 3 代数层：约束代数给出什么

### 3.1 分布式不确定关系

设 $[\hat G,\hat L_i]=iC_i$，$\sum_iC_i=C$（$C$ 为 $c$ 数）。对 $A=\hat G$、$B=\sum_i\hat L_i$ 用罗伯逊–薛定谔不等式【标准数学】：

$$\Delta G^2\,\Delta\Bigl(\sum_iL_i\Bigr)^2\ \ge\ \tfrac14\bigl|\langle\{\Delta G,\Delta\bigl(\textstyle\sum_iL_i\bigr)\}\rangle\bigr|^2+\frac{C^2}{4}.$$

记 $\mathrm{Cov}\equiv\tfrac12\langle\{\Delta G,\Delta\sum_iL_i\}\rangle$，则

$$\Delta G^2\,\Delta\Bigl(\sum_iL_i\Bigr)^2-\mathrm{Cov}^2\ \ge\ \frac{C^2}{4}.$$

若各节点 $\Delta L_i=\Delta L$ 且协方差可忽略，$\Delta(\sum_iL_i)^2=N\Delta L^2$，得

$$\Delta G\cdot\Delta L\ \ge\ \frac{|C|}{2\sqrt N}.$$

集体量的下界 $|C|/2$ 不随 $N$ 衰减，逐节点下界按 $1/\sqrt N$ 减弱。这是标准不确定关系对集体对的实例，本身不产生记忆；但它的两个推论直接兑现要素 4 与要素 5。

### 3.2 定理 1（不可还原的代数判据）

**定理 1**【标准数学】设 $[G,\sum_iL_i]=iC$，$C\neq0$。则：

1. **无联合本征态**：不存在 $|g,l\rangle$ 同时满足 $\hat G|g,l\rangle=g|g,l\rangle$ 与 $\sum_i\hat L_i|g,l\rangle=l|g,l\rangle$。
2. **无完美相关**：任何态满足 $|\mathrm{Cov}|\le\sqrt{\Delta G^2\Delta(\sum_iL_i)^2-C^2/4}<\Delta G\,\Delta(\sum_iL_i)$。故 $G$ 与 $\sum_iL_i$ 不可能是完全相关的两个经典变量。
3. **无函数关系**：若 $G=f(\sum_iL_i)$ 对某函数 $f$ 成立，则二者可同时对角化，与 1 矛盾。因此“全局不可还原为局部加总”在 $C\neq0$ 时**不是建模选择，而是代数事实**。

**推论 3.1（截面必损）** 任何把 $\{L_i\}$ 赋以确定值、并据此赋 $G$ 以确定值的描述，必与 $C\neq0$ 冲突。于是“单点共时截面丢失信息”不是粗粒化的后果，而是约束代数的直接禁止。要素 5 由此获得代数形式。

**推论 3.2（差异的不可消除下界）** 由 1 与 2，$\Delta(\sum_iL_i)\ge|C|/(2\Delta G)$。全局量越确定，集体量越不定；而集体量的展宽只能由个体展宽与跨节点协方差两者提供。故“把所有节点的差异同时抹平”被禁止：或个体展宽不为零，或跨节点关联不为零。

**推论 3.3（约束代数作用于态空间，而非核振幅）** $C$ 不进入任何传播子的振幅相加，而是把可行协方差集限制为

$$\Bigl\{\Sigma:\ \Sigma+\tfrac{\mathrm i}{2}\Omega\ge0\Bigr\}\ \cap\ \Bigl\{|\mathrm{Cov}|\le\sqrt{\Delta G^2\Delta(\textstyle\sum L)^2-C^2/4}\Bigr\}.$$

这是本文与“$K_{\rm nc}\propto C$ 的加性修正”这一图像的分野：**$C$ 是态空间的约束，不是核的加性项**。记忆的量子部分不是“多加了一项”，而是“可行域被收紧后，偶通道只能取到某些值”。§4.5 与 §7.3 依赖这条推论。

---

## 4 动力学层：记忆的三个载体

### 4.1 双线性模型与 NZ 结构

取

$$H=H_G(P,G)+\sum_i\Bigl[\frac{p_i^2}{2m_i}+\tfrac12m_i\omega_i^2x_i^2\Bigr]-G\sum_ic_ix_i,\qquad \rho(0)=\rho_G(0)\otimes\rho_B+\delta,$$

$\mathrm{Tr}_B\delta=0$。以 $\mathcal P=\mathrm{Tr}_B[\rho_B\otimes\cdot]$ 作 Nakajima–Zwanzig 投影【标准数学】[1][2]：

$$\partial_t\rho_G(t)=-\mathrm i[H_G,\rho_G(t)]+\int_0^t\mathrm ds\,\mathcal K(t-s)\rho_G(s)+\mathcal I(t).$$

核 $\mathcal K$ 是超算符，由浴的双点函数生成：

$$C_B(\tau)=\sum_{ij}c_ic_j\,\langle x_i(\tau)x_j(0)\rangle_B.$$

非齐次项携带初态关联：

$$\mathcal I(t)=-\mathrm i\,\mathrm{Tr}_B\bigl[H_I(t),\,\mathrm e^{-\mathrm iQLt}Q\rho(0)\bigr].$$

这套结构是标准的；本文的构造在于**把 $C_B$ 的两支分开，并认定 DNR 的联合史落在哪一支**。

### 4.2 通道分解：奇通道态无关，偶通道载史

**定理 2（双线性模型的通道分解）**【标准数学】令 $X=\sum_ic_ix_i$。$C_B$ 可唯一分解为

$$C_B(\tau)=\underbrace{\tfrac12\langle\{X(\tau),X(0)\}\rangle}_{\text{偶通道}}+\underbrace{\tfrac12\langle[X(\tau),X(0)]\rangle}_{\text{奇通道}}.$$

1. **奇通道**对线性动力学是 $c$ 数，且**与态无关**：

$$\chi(\tau)\equiv\frac{\mathrm i}{\hbar}\langle[X(\tau),X(0)]\rangle=\sum_i\frac{c_i^2}{m_i\omega_i}\sin\omega_i\tau .$$

它只由哈密顿量与耦合常数决定，不含任何 $\rho_B$ 的信息，承载响应（Kubo 公式【标准数学】[12]）。

2. **偶通道**依赖浴的二阶协方差，含跨节点元：

$$\tfrac12\langle\{X(\tau),X(0)\}\rangle=\sum_{ij}c_ic_j\,\tfrac12\langle\{x_i(\tau),x_j(0)\}\rangle .$$

单模热态给出 $\tfrac12\langle\{x_i(\tau),x_i(0)\}\rangle=\frac{\hbar}{2m_i\omega_i}\coth\frac{\hbar\omega_i}{2k_BT}\cos\omega_i\tau$，与奇通道由涨落—耗散关系绑定【标准数学】[9][10]：

$$S(\omega)=\hbar\coth\frac{\hbar\omega}{2k_BT}\,\mathrm{Im}\,\hat\chi(\omega).$$

**结论**：DNR 的“$G$ 涨落与 $\{L_i\}$ 分布的联合关联”只能进入偶通道；若把非对易修正指认为奇通道（对易子部分），它在高斯线性层是**态无关的 $c$ 数**，不可能承载历史。这不是归一化问题，而是通道归属问题。

### 4.3 初始项：联合史的两个入口

$\mathcal I(t)$ 线性于 $\delta$，故“历史写入联合关联”有两个入口，代价不同：

| 入口 | $\delta$ 的类型 | 进入阶次 | 未来响应之差 |
|:---|:---|:---|:---|
| 系统—浴关联 | $\delta\propto Gx_i+x_iG$ | **一阶**，$\mathcal I\propto\sum_ic_i\mu_i\,[G_I(t),\langle\{x_i(t),G\}\rangle]$ | $\propto c\,\mu$ |
| 浴—浴交叉关联 | $\delta\propto\sum_{ij}\lambda_{ij}(x_ix_j-\langle x_ix_j\rangle)$ | 一阶抵消（居中高斯态三点函数为零），**二阶**进入 | $\propto c^2\lambda$ |

【标准数学】居中高斯态下 $\mathrm{Tr}_B[x_i^I(t)x_jx_k\rho_B]=0$，故纯浴—浴交叉关联的一阶项为零；其效应自二阶起显现。这一事实决定了实验设计：想用一阶效应看联合史，必须制备系统—浴关联；想用纯浴侧关联，须有足够统计精度取二阶。

### 4.4 三载体分类

**定理 3（记忆的载体）** 在本文模型中，记忆有三个互不替代的载体：

| 载体 | 数学位置 | 依赖 $C$ | 依赖初态联合结构 | 实例 |
|:---|:---|:---|:---|:---|
| ① 谱分布 $J(\omega)$（含空间非均匀） | $\mathcal K$ 的形状（奇＋偶） | 否 | 否 | 角亏分布 → 频率分布 → 系综平均（§6.5） |
| ② 联合协方差 $\Sigma_B$（跨节点） | 偶通道权重、$\mathcal I$ | 受下界约束（推论 3.2） | 是 | DNR 的“分布式联合史” |
| ③ 高阶累积量／非线性 | $\mathcal K$ 的态依赖修正 | 受可行域约束 | 是 | 原草稿的 $K_{\rm nc}$ |

三者不可互相解释：①是“浴长什么样”，②是“各节点怎么关联”，③是“关联偏离高斯有多远”。

### 4.5 核的正确形式与 $K_{\rm nc}$ 的位置

由定理 2–3，核应写成

$$\boxed{\mathcal K=\mathcal K_{\rm odd}[H]+\mathcal K_{\rm even}[\Sigma_B]+\mathcal K_{\rm cum}[\kappa_3,\kappa_4,\dots]}$$

其中第一项由哈密顿量固定，第二项是联合协方差的泛函，第三项是高阶累积量的泛函。原草稿的

$$K=K_{\rm cl}+C\,K_{\rm nc}$$

在**第三层**（非线性或非高斯）才有非零的 $K_{\rm nc}$：此时 $K_{\rm nc}$ 是联合累积量的展开项，且其可取幅度受约束代数收紧（推论 3.3）。在双线性高斯层，$K_{\rm nc}\equiv0$——不是因为“非对易修正很小”，而是因为该层奇通道态无关、偶通道已被 $K_{\rm cl}$ 完全吸收。

这条定位把草稿的公式从“处处成立的分解”改为“分层成立的展开”，同时保留其可检验内容：$K_{\rm nc}$ 的谱权重应与高阶累积量（而非与 $C$）成比例。

---

## 5 阈值定理

### 5.1 $\ell_*$ 是关联长度

【构造假设】取 $\delta=\sum_{i<j}\lambda_{ij}(x_ix_j+x_jx_i)/2$ 为纯浴侧交叉关联，其余条件相同。则

$$\Delta P(\text{未来})\ \propto\ c^2\sum_{i<j}\lambda_{ij}\,\Phi_{ij}(t),$$

$\Phi_{ij}$ 由两节点的频率与耦合给出。**两次制备若单点二阶矩相同**（对角 $\Sigma_B$ 相同），而 $\lambda_{ij}$ 不同，则未来统计不同——这正是定义 2 的纤维判据，并且是**线性实现**，不是隐喻。

于是阈值不是拟合参数：

$$\ell_*=\text{联合协方差的关联长度}=\max\{|i-j|:\lambda_{ij}\neq0\}.$$

$\ell<\ell_*$ 时，$\mathcal S_\ell$ 的切片读不到 $\lambda$，过程在该类中非马尔可夫；$\ell\ge\ell_*$ 时切片足以重建 $\lambda$，马尔可夫化成功。这给出一个可数值化的判据：$\ell_*$ 可由关联矩阵的谱或张量网络方法直接估计【待推 E3】。

### 5.2 公共浴：不可还原的动力学判据

若所有节点耦合到同一浴算符 $X$（而非各自独立的 $x_i$），则

$$C_B(\tau)=\Bigl(\sum_ic_i\Bigr)^2\langle X(\tau)X(0)\rangle .$$

核正比于**集体耦合的平方**，而不是各节点贡献之和 $\sum_ic_i^2$。这正是要素 5（层级不可还原）在动力学层的判据：记忆不能分解为“各节点记忆之和”。

可观测后果是标度：公共浴下记忆权重 $\propto N^2$，独立浴下 $\propto N$。这条标度比 $R_{\rm nc}$ 更能区分结构（§7.5）。

### 5.3 与代数层的衔接

代数层（定理 1）保证“截面必损”；动力学层（定理 2、§5.1）保证“损失的部分影响未来”。两者合起来，才得到定义 2 的非马尔可夫性。单独任一层都不够：只有代数，得到的是静态禁止；只有动力学，得到的是普通开放系统。

---

## 6 与 CQM 的关联

本章不是对框架的改写，而是把 DNR 的五个数学位置逐一接到框架的既有表述上，并在接口处给出可陈述的构造。

### 6.1 全局编码／局部不可接入 ↔ 偶通道的跨节点权重

【框架】退相干时“其余潜在方式……其信息仍被全局幺正性所编码，只是对局部层级不再显现为可接入的因果节点”（`05 方法论与批判/CQM_方法论_资本主义-旧物理-层级还原论批判.md` §6.5）。

这句话在本文中有精确对应：

| 框架表述 | 本文结构 | 可计算对象 |
|:---|:---|:---|
| 信息仍被全局编码 | 偶通道保留全部跨节点协方差 | $\Sigma_B$ |
| 局部不可接入 | $\mathcal S_\ell$ 的切片读不到 $\lambda_{ij}$（$|i-j|>\ell$） | $\ell_*$ |
| 后续展开依赖它 | $\mathcal I(t)$ 与偶通道权重进入 $G$ 的有效方程 | $\Delta P(\text{未来})$ |

于是“非马尔可夫记忆 ＝ 全局编码中对该层级不可接入的那部分”这句框架内定义，获得一个解析形式：**记忆 ＝ 偶通道中跨节点的那部分 ＋ 非齐次项中的初态关联**。这是本文对框架的主要贡献：把“不可接入”从信息描述推进到可算的通道权重。

### 6.2 同步事件性与截面分辨率

【框架】“同步方程是条件本征值问题，不是动力学方程。同步是退相干事件……不是时间演化过程”（`01 核心理论/CQM_核心_引力存在论前提.md` §3.7）；“时间不是先验参数，是组织过程的持续节拍”（`01 核心理论/CQM_核心_因果网络同步理论.md` §2.3）。

【构造假设】由此，$\mathcal S_\ell$ 的 $\ell$ 不是外加的截断，而是**层级分辨率**：在无优先共时切片的框架里，“取一个截面”本身就是层级操作，其分辨率与因果截断不等式

$$\Delta\tau\ \ge\ \tau_{\text{res}}=\frac{\hbar}{Mc^2}$$

（`03 引力与退相干/CQM_退相干_引力因果场.md` §2.0）同源。$\ell$ 越小，可接入的联合范围越窄，$\mathcal I$ 与偶通道的可读部分越少。两者是同构的分辨率限制，而不是同一个量；把 $\ell$ 与 $\tau_{\rm res}$ 的换算写成显式关系属【待推 E4 的伴生问题】。

### 6.3 耦合常数—固有时：单节点胚与分布式构造

【框架】权威口径是**无量纲**的一维海森堡对（`01 核心理论/CQM_核心_集成理论.md` §3.3；`07 精细引力（FG）/FG_核心理论.md` §4.1；`README.md` 核心公式节）：

$$[\hat u,\hat p_u]=\mathrm i,\qquad \hat u=\ln\hat g,\qquad \hat p_u=\frac{v_\tau}{☯},\qquad \Delta u\cdot\Delta v_\tau\ \ge\ \frac{☯}{2}.$$

合法定义域限于一维阿贝尔群（$U(1)$ 电磁扇区）；$SU(2)$、$SU(3)$ 因子的耦合不能直接量子化，只能经 Casimir 阶梯从 $U(1)$ 锚导出。

DNR 需要 $N$ 个局部变量，而框架给的是单个一维对。构造如下。

【构造假设】**单节点胚**：每个节点携带一维耦合空间 $(\hat u_i,\hat p_{u,i})$，$[\hat u_i,\hat p_{u,j}]=\mathrm i\delta_{ij}$，$\hat p_{u,i}=v_\tau^{(i)}/☯$。**全局集体量**取对数耦合的几何平均：

$$\hat u_G=\frac1N\sum_{i=1}^N\hat u_i,\qquad \hat p_{u,G}=\sum_{i=1}^N\hat p_{u,i},\qquad [\hat u_G,\hat p_{u,G}]=\mathrm i,$$

即

$$\Bigl[\hat u_G,\ \sum_i v_\tau^{(i)}\Bigr]=\mathrm i\,☯,\qquad \Delta u_G\cdot\Delta\Bigl(\sum_iv_\tau^{(i)}\Bigr)\ \ge\ \frac{☯}{2}.$$

三条自洽条件：

1. **$N=1$ 极限**退化为框架既有的单个一维对，故该构造不修改既有口径，只作延伸；
2. **定义域**：每节点耦合空间仍为一维阿贝尔，非阿贝尔扇区一律经 Casimir 阶梯；
3. **集体下界不随 $N$ 衰减**：$\Delta u_G\cdot\Delta(\sum_iv_\tau)\ge ☯/2$ 与 $N$ 无关，逐节点版本按 $1/\sqrt N$ 减弱——与 §3.1 的结构一致。

【构造假设】经角亏—固有时流速接口 $v_\tau=\sqrt{1-\beta\delta_v}$（$\beta$ 为 FG 几何耦合参数，$\delta_v$ 为局域角亏；`01 核心理论/CQM_核心_引力存在论前提.md` §3.4），上式落成

$$\Delta u_G\cdot\Delta\Bigl(\sum_{i=1}^N\sqrt{1-\beta\,\delta_v^{(i)}}\Bigr)\ \ge\ \frac{☯}{2}.$$

这是本文给出的、CQM 侧最具体的一条 DNR 不等式：全局集体量是平均对数耦合，局部分布式量是各节点固有时流速，二者共轭；角亏分布是“不可统一的差异”的几何来源。要素 4 在此获得框架内的落点。

**边界**：该构造的多节点相容性、与本框架“耦合空间一维”命题的严格关系、以及 $\beta$ 在分布式情形下的定义，均属【待推 E4】。在 E4 完成前，此式只作构造登记，不作框架结论。

### 6.4 引力：无全局马尔可夫生成元

【框架】“引力因果限制场并不改变因果结构，而是对因果结构施加时空限定，导致不同物理子系统之间存在因果链上的凹凸不平，从而导致即使子系统之间也不能被一套微分方程组贯穿”（同文 §6.3）。

“不能被一套微分方程组贯穿”即**不存在单一的全局马尔可夫生成元**。这与本文的 $\mathcal I(t)$ 结构对应：非齐次项与偶通道的跨节点权重不能由任何有限维生成元吸收。差别只在语言：框架说“不能贯穿”，本文说“不能因子化”。要素 3 的引力候选由此获得一个判据形式，而不是类比喻。

**边界**：限定而非改写；不得把引力读成凝聚态记忆的致因。

### 6.5 五步链：谱分布型记忆与联合型记忆的互补

【框架】CQM 侧的超导接口是五步链

$$\text{LQG}\ \rightarrow\ \text{Regge}\ \rightarrow\ \delta_v\text{ 涨落}\ \rightarrow\ \text{声子谱}\ \rightarrow\ \text{配对场记忆核}\ \rightarrow\ T_c/\text{赝能隙},$$

第一环的局部映射已写出（`07 精细引力（FG）/FG_LQG-Regge显式映射.md`）：自旋网络边 $e$ 的自旋 $j_e$ 给出面积 $A_e=\lambda_\ell\,8\pi\gamma\ell_P^2\sqrt{j_e(j_e+1)}$，交织子给角数据，解出 4-单纯形边长，按 $\delta_v=2\pi-\sum_{\Delta\ni v}\theta_v(\Delta)$ 得顶点角亏。

记忆核在第 4 至第 5 环之间显现，机制是局域频率分布的系综平均：

$$K(t)=\bigl\langle \mathrm e^{-\mathrm i\omega(v)t}\bigr\rangle_{P(\delta_v)}.$$

按本文分类（§4.4），这是**载体 ①（谱分布）**：记忆来自 $\delta_v$ 的空间分布，而非来自跨节点协方差。其非马尔可夫性是形状性的：若 $P(\delta_v)$ 近似高斯，则 $K(t)\propto \mathrm e^{-t^2/2\tau_g^2}$；而【标准数学】平稳高斯过程的协方差满足马尔可夫性质，当且仅当 $R(a+b)R(0)=R(a)R(b)$，其连续解为指数型 $R(\tau)=R(0)\mathrm e^{-\alpha|\tau|}$（Ornstein–Uhlenbeck 型）[13]。高斯核不满足该条件，故在形状上已非马尔可夫；马尔可夫极限是指数型或 $\delta(t)$，不是高斯型。

**映射的条件性**：该映射只局部落成，不构成全球粘合——10 个面积最多对应 64 组边长，须由交织子或临界点选支；CQM 的顶点角亏不是 4 维 Regge 的三角形骨亏；LQG 面积单位与 FG 晶胞尺度之间需层级重标 $\lambda_\ell$；全球粘合与自旋泡沫动力学仍未闭合。记忆核在这条链的**第 4 环到第 5 环之间**显现，而不是从 LQG 顶点直接给出：每个区域由 $\delta_v(v)$ 给出 $v_\tau$ 与 $\tau_{\rm relax}$，从而给出局域频率 $\omega(v)$；对 $P(\delta_v)$ 平均得到配对场的记忆因子。若 $P(\delta_v)$ 在相关变量上近似高斯，核宽 $\tau_g$ 由 $\delta_v$ 的方差与 $\tau_{\rm relax}$ 共同决定。$\tau_{\rm relax}$ 是核的特征宽度，不是核本身；完整核仍需声子谱与配对场耦合。

**与 DNR 的关系**：五步链给核的**几何来源**（载体 ①），DNR 给核的**跨节点权重**（载体 ②）。两者相加不重复计数：前者决定核的时间形状，后者决定核在阵列上的分配。这一分工是本文对“框架已有记忆机制”与“DNR 新增机制”的划界，也是避免把两者混为“同一件事的两种说法”的关键。

### 6.6 角亏—固有时流速—弛豫时标与涨落—记忆乘积

【框架】固有时流速由局域角亏调制：

$$\frac{\mathrm d\tau}{\mathrm dt}=\sqrt{1-\beta\,\delta_v},$$

其中 $\beta$ 为 FG 几何耦合参数（不同于网络刚度 $\beta_{\text{sync}}$），$\delta_v$ 为局域角亏；$\delta_v>0$ 使固有时流速减慢（`01 核心理论/CQM_核心_引力存在论前提.md` §3.4；形式化见 `CouplingSpace.properTimeFlow`）。

【构造假设】**局部命题 N1**：记忆核的空间不均匀性可写为局域弛豫时标

$$\tau_{\rm relax}(v)\ \propto\ \bigl(1-\beta\,\delta_v\bigr)^{-1/2}.$$

**依据与边界**：框架既有的是因果截断不等式 $\Delta\tau\ge\tau_{\text{res}}=\hbar/(Mc^2)$（`03 引力与退相干/CQM_退相干_引力因果场.md` §2.0），它给出**分辨率下限**而非弛豫时标；两者的衔接是本文推演，未在框架内证明。可判伪方式：角亏分布由质量—能量分布给出，弛豫时标由弛豫测量给出，二者应同向变化，比例系数可测。

【构造假设】在超导核心理论的资格边界上，把资格条件

$$\Delta\delta_0\ \ge\ \frac{☯\sqrt{1-\beta\delta_v}}{2\beta\ln n}$$

与 N1 的归一化 $\tau_{\rm relax}=(1-\beta\delta_v)^{-1/2}$ 相乘，得**涨落—记忆乘积关系**

$$\Delta\delta_0\,\tau_{\rm relax}\ \ge\ \frac{☯}{2\beta\ln n},$$

$n=2$ 时为 $☯/(2\beta\ln 2)$。其含义是：要在局域驱动 $\Delta u_n=2\ln n$ 的耦合跃迁，几何涨落必须同时具备足够幅度与足够持续时间，二者不能同时任意小。该式是既有公式的代数推论，不是新机制；若 N1 的比例系数 $\kappa_{\rm relax}\neq1$，右端应乘以 $\kappa_{\rm relax}$。可检验形式：对满足局域资格的区域，测 $\Delta\delta_0$（结构／谱学不均匀性）与 $\tau_{\rm relax}$（噪声／弛豫），其乘积应在给定 $n$ 下聚在一条与材料无关的下界附近。该检验与 $R_{\rm DNR}$（§7.2）互补：后者测核的联合权重，前者测几何涨落与记忆时长的乘积下界。

【待推】更远的两个推论：赝能隙起始 $T^*$ 可定为物理记忆时间 $\tau_{\rm relax}(T)\cdot 2\pi/\Omega_0$ 与热时间 $\hbar/(k_BT)$ 相交的温度；当 $\delta_v\to1/\beta$ 时 $\tau_{\rm relax}\sim(1-\beta\delta_v)^{-1/2}$，若到转变点的距离线性于 $1-\beta\delta_v$，则临界动力学指数 $z\nu=1/2$。两者都依赖尚未证明的映射，不作预言引用。

---

## 7 可检验结构

### 7.1 $R_{\rm nc}$ 的闭式：它是涨落—耗散比

取单模，奇通道幅值 $\hbar/(2m\omega)$，偶通道幅值 $(\hbar/2m\omega)\coth(\hbar\omega/2k_BT)$，且 $\int|\sin|=\int|\cos|$ 在同一窗口内相等。故

$$\boxed{R_{\rm nc}=\frac{\int|K_{\rm odd}|\,\mathrm dt}{\int|K_{\rm even}|\,\mathrm dt}=\tanh\frac{\hbar\omega}{2k_BT}}$$

多模为加权平均

$$R_{\rm nc}=\frac{\sum_iw_i\tanh(\hbar\omega_i/2k_BT)}{\sum_iw_i},\qquad w_i\propto\frac{c_i^2}{m_i\omega_i}.$$

于是 $R_{\rm nc}\in[0,1]$：$T\to0$ 时 $\to1$，$T\to\infty$ 时 $\to0$。它是 FDT 的比值，度量量子性与温度。**它不是 DNR 判据**：对同一频率与同一温度，任何量子开放系统的 $R_{\rm nc}$ 都取同一值，与其是否具有分布式联合结构无关。

这条闭式的价值是正面的：它把原判据的物理意义锁定，从而腾出位置给真正的 DNR 判据。

### 7.2 $R_{\rm DNR}$：同切片、异协方差的响应差

**定义 3（DNR 判据）** 取两次制备 $\rho^{(a)},\rho^{(b)}$，其 $\mathcal S_\ell$ 切片相同（单点数据与半径 $\ell$ 内关联一致），而跨节点协方差不同。定义

$$R_{\rm DNR}=\frac{\bigl\|\Delta P^{(a)}-\Delta P^{(b)}\bigr\|}{\bigl\|\lambda^{(a)}-\lambda^{(b)}\bigr\|},$$

$\|\cdot\|$ 取未来可观测量上的总变差或迹距离。$R_{\rm DNR}\neq0$ 即纤维判据成立。

可操作方案：以通道分辨的核重构取得 $\mathcal K$ 与 $\mathcal I$ 的时间结构【文献】[7][8]，在两次制备上分别重构，比较偶通道权重与 $\mathcal I$ 的差异。这条判据的关键是**只改变跨节点关联**，不改单点数据——否则测到的是普通的环境效应。

### 7.3 约束下限检验

由推论 3.2，$\Delta(\sum_iL_i)\ge|C|/(2\Delta G)$：全局越确定，集体展宽越大。可设计的检验：用压缩或反馈把 $\Delta G$ 压到接近饱和值 $|C|/(2\Delta(\sum L))$，此时集体展宽达下界；若此时偶通道的跨节点权重仍可自由压到零，则“$C$ 限制可行域”不成立，$C$ 不是同一对变量的对易子。这条检验把静态代数与动态核绑定，且不依赖模型细节。

### 7.4 $\ell_*$ 与节点分辨调制

两条可算预言：

1. **$\ell_*$ 的数值**：在给定关联矩阵 $\lambda$ 的模型上，$\ell_*$ 由谱或张量网络方法估计；随温度升高，热噪声加宽 $\lambda$ 的支撑，$\ell_*$ 上升【待推 E3】。
2. **节点分辨调制**：对单节点耦合 $c_i$ 作局域调制，偶通道中对应频率分量的权重应按 $c_ic_j\lambda_{ij}$ 响应；若整体重排而无节点分辨，则不满足 DNR 结构。

### 7.5 判决力分级

| 级别 | 判据 | 现状 |
|:---|:---|:---|
| 强 | $R_{\rm DNR}$：同切片异协方差的响应差 | 方法已具备（核重构 [7][8]） |
| 强 | 公共浴 $N^2$ 标度 vs 独立浴 $N$ 标度 | 可直接测 |
| 中 | 约束下限检验（§7.3） | 依赖 $C$ 的独立测量 |
| 中 | $\ell_*$ 的数值与温度依赖 | 待算（E3） |
| 弱 | 引力侧结构类比 | 无定量预言，不作检验 |

---

## 8 开放问题

| 编号 | 事项 | 完成判据 |
|:---|:---|:---|
| E1 | 偶通道权重的闭式（非均匀 $J$、多模交叉谱） | 给出 $\mathcal K_{\rm even}$ 的解析或半解析表达，并与 $R_{\rm DNR}$ 对照 |
| E2 | 第三层 $K_{\rm nc}$ 的累积量展开 | 给出 $K_{\rm nc}$ 与 $\kappa_3,\kappa_4$ 的关系式及收敛条件；检验其谱权重是否与 $C$ 无关 |
| E3 | $\ell_*$ 的数值与标度 | 在自旋链／张量网络模型上算出 $\ell_*$，给出温度依赖 |
| E4 | 分布式耦合空间构造的相容性 | 证明 §6.3 的构造与本框架一维性限定相容，或指出必须修改的部分；含 $N=1$ 极限与 Casimir 阶梯 |
| E5 | 转变点的锁定形式 | 给出 $K$ 在 $T_c$ 附近定性改变的可判伪形式，或撤回该猜想 |

---

## 9 结论

1. **代数层的收获**：约束代数 $[G,\sum_iL_i]=iC\neq0$ 禁止联合本征态、禁止完美相关、禁止函数关系。故“全局不可还原”“截面必损”是代数事实，不是建模选择；$C$ 作用于态空间（可行协方差集），不作用于核振幅。
2. **动力学层的收获**：双线性模型下记忆核分奇偶两通道。奇通道态无关（由 $H$ 固定，承载响应），偶通道依赖联合协方差（承载噪声与退相干）。DNR 的联合史只能进偶通道；把非对易修正放在奇通道，等于把它放在唯一不载史的一支上。
3. **载体分类的收获**：谱分布、联合协方差、高阶累积量三分。原草稿的 $K_{\rm cl}+C K_{\rm nc}$ 属于第三层；在双线性高斯层 $K_{\rm nc}\equiv0$，这不是小量问题，而是通道归属问题。$K_{\rm nc}$ 的谱权重应与高阶累积量成比例，而非与 $C$ 成比例。
4. **阈值层的收获**：$\ell_*$ 等于联合协方差的关联长度，纤维判据在模型中线性实现（未来响应差 $\propto c^2\lambda$）；公共浴给出 $N^2$ 标度，是“不可还原”的动力学判据。
5. **判据层的收获**：$R_{\rm nc}=\tanh(\hbar\omega/2k_BT)$ 是 FDT 比，度量量子性与温度，不是 DNR 判据；DNR 判据应为 $R_{\rm DNR}$——同一切片、异协方差的响应差。
6. **CQM 关联的收获**：$\hat u_G=\frac1N\sum_i\hat u_i$ 与 $\sum_iv_\tau^{(i)}$ 构成 $\mathrm i☯$ 的一维对，$N=1$ 时退化为框架既有口径；经角亏接口落成 $\Delta u_G\cdot\Delta(\sum_i\sqrt{1-\beta\delta_v^{(i)}})\ge ☯/2$。此构造待 E4 检验。
7. **与框架既有记忆机制的分工**：五步链给核的几何形状（载体 ①），DNR 给核的阵列分配（载体 ②）。两者互补，不互为解释。

**一句话**：DNR 的结构起源论可以写成一句可算的话——不对易性禁止把全局量压进局部截面，分布式联合协方差因此只能从偶通道与非齐次项进入未来；记忆不在“多了一项修正”，而在“可行域被收紧后，某些联合关联再也读不出来”。

---

## 参考文献

[1] Nakajima S. On quantum theory of transport phenomena: steady diffusion. *Prog. Theor. Phys.* **20**, 948–959 (1958). DOI: 10.1143/PTP.20.948；Zwanzig R. Ensemble method in the theory of irreversibility. *J. Chem. Phys.* **33**, 1338–1341 (1960). DOI: 10.1063/1.1731409.

[2] Breuer H.-P., Petruccione F. *The Theory of Open Quantum Systems*. Oxford University Press (2002).

[3] Rivas Á., Huelga S. F., Plenio M. B. Quantum non-Markovianity: characterization, quantification and detection. *Rep. Prog. Phys.* **77**, 094001 (2014). DOI: 10.1088/0034-4885/77/9/094001. arXiv:1405.0303.

[4] Wu Z., Chen H., Eaton A. G., et al. Electrically controllable superconducting memory effect in UTe₂. *Nature* (2026). arXiv:2603.02450.（SC1／SC2 共存区的电流脉冲写入高／低 $J_c$ 亚稳态；玻璃态涡旋淬火／退火机制；作者强调该功能为超导序的内禀属性。）

[5] Maile D., Andergassen S., Belzig W., Rastelli G. Quantum phase transition with dissipative frustration. *Phys. Rev. B* **97**, 155427 (2018). DOI: 10.1103/PhysRevB.97.155427. arXiv:1711.11346.（两个不对易算符耦合环境；约瑟夫森结链实现；非单调临界线。）

[6] Pollock F. A., Rodríguez-Rosario C., Frauenheim T., Paternostro M., Modi K. Non-Markovian quantum processes: complete framework and efficient characterisation. *Phys. Rev. Lett.* **120**, 040401 (2018). arXiv:1512.00589.

[7] Learning Volterra Memory Kernels for Non-Markovian Qubit Dynamics. arXiv:2601.09075.（以非近似 Nakajima–Zwanzig 方程为对象，用 Volterra 核学习重构非马尔可夫量子比特动力学。）

[8] Causality from Projection and Hardy-Space Analyticity of Non-Markovian Memory Kernels. arXiv:2604.17058.（记忆核的解析性与因果结构；投影对核的约束。）

[9] Hänggi P., Ingold G.-L. Fundamental aspects of quantum Brownian motion. arXiv:quant-ph/0412052.（量子布朗运动综述；涨落—耗散关系与核的通道结构。）

[10] Kinetic Energy of a Free Quantum Brownian Particle. *Entropy* **20**(2), 123 (2018). DOI: 10.3390/e20020123.（给出 $C(\omega)=\frac{\hbar\omega}{2}\coth\frac{\hbar\omega}{2k_BT}\,\gamma(\omega)$ 形式的涨落—耗散关系。）

[11] Caldeira A. O., Leggett A. J. Path integral approach to quantum Brownian motion. *Physica A* **121**, 587–616 (1983). DOI: 10.1016/0378-4371(83)90013-4.

[12] Kubo R. Statistical-mechanical theory of irreversible processes I. *J. Phys. Soc. Jpn.* **12**, 570–586 (1957). DOI: 10.1143/JPSJ.12.570.

[13] Doob J. L. *Stochastic Processes*. Wiley (1953).（平稳高斯过程的马尔可夫性质与指数型协方差；亦见 Ornstein–Uhlenbeck 过程的标准表述。）

[14] Perez A. The spin foam approach to quantum gravity. *Living Reviews in Relativity* **16**, 3 (2013). arXiv:1205.2019.

[15] A Master equation approach to line shape in dissipative systems. arXiv:0905.2261.（把初态系统—浴关联作为主方程的“非齐次项”处理，给出含初态关联的非马尔可夫动力学的紧凑二阶累积量公式。）

[16] Quantum Frames of Reference and the Noncommutative Values of Observables. arXiv:2112.04028.（量子参考系与非对易观测值：约束—参考系—观测值三者的关系，可作 §3 代数层的对照。）

[17] Swingle B. Entanglement renormalization and holography. *Phys. Rev. D* **86**, 065007 (2012). arXiv:0905.1317.

> **引注说明**：以上条目均给出可核验的 arXiv 编号或 DOI。凡本次检索未直接取到完整著录者（[9] 的期刊卷期），只引 arXiv 编号，不补未核实的卷期。
