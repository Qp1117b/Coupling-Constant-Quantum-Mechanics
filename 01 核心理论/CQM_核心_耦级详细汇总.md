# CQM 耦级详细汇总

**作者**：ruster

**框架**：耦合常数量子力学（CQM）

---

> **诚实声明**：本文档是耦级 $\mathfrak{c}_n = 1/4 + \gamma_n^2$ 的系统性汇总，整合定义、数学来源、性质、与 RH/GRH 的关系、误差结构、自伴性、物理测量等各方面。其中"耦级为实数 $\Longleftrightarrow$ RH"（§六/§九）是数学事实；"耦级是物理谱"（§十）指耦级是谱算符的本征值（无量纲数学纯数，非物理能量）；"经典化"（§十二）是路线图主张，非已完成的证明。$☯$ 的谱表示 $\textstyle ☯ = \sum_n 1/\mathfrak{c}_n$（§七）是 RH 成立时的推论，非 $☯$ 的定义。

> **与项目文档的关系**：本文档汇总的内容散见于以下项目文档：`01 核心理论/CQM_核心_集成理论.md` §8（Sierra-CQM 定理）、`03 引力与退相干/CQM_引力_GN可能公式.md` §3（耦谱）、`04 前沿研究/CQM_前沿研究_黎曼猜想证明思路.md`（RH 证明策略，含 §十四数学精确与物理截断、§十五自守形式–黎曼零点关联）、`02 量子引力/CQM_引力_量子引力集成.md` §13（耦级的双重身份与向外衍生）。本文档将这些散见内容系统化整理为单一参考文档。

---

## 目录

1. [耦级的定义](#一耦级的定义)
2. [耦级的数学来源](#二耦级的数学来源)
3. [第一耦级](#三第一耦级)
4. [耦级的层级结构](#四耦级的层级结构)
5. [耦级的性质](#五耦级的性质)
6. [耦级与零点实部的关系](#六耦级与零点实部的关系)
7. [耦级与相变量子 $☯$](#七耦级与相变量子-)
8. [耦级的误差结构](#八耦级的误差结构)
9. [耦级与自伴性](#九耦级与自伴性)
10. [耦级与物理测量](#十耦级与物理测量)
11. [耦级与 GRH](#十一耦级与-grh)
12. [耦级与经典化](#十二耦级与经典化)
13. [耦级的完整逻辑链](#十三耦级的完整逻辑链)
14. [总结表](#十四总结表)
15. [一句话总结](#十五一句话总结)

---

## 一、耦级的定义

### 1.1 基本定义

耦级是 CQM 核心算符的本征值：

$$\boxed{\hat{H} = \hat{D}^2 + \frac14, \qquad \hat{D} = -i(\partial_u - 1/2)}$$

定义在耦合空间 $u = \ln r$ 上，Hilbert 空间为 $L^2(\mathbb{R}, e^{-u}du)$。

耦级记为：

$$\boxed{\mathfrak{c}_n = \frac14 + \gamma_n^2}$$

其中 $\gamma_n$ 是黎曼零点的虚部。

### 1.2 名称来源

"耦级"来自"耦合空间"+"能级"：

- **耦**：耦合空间 $u = \ln r$，其中 $r$ 是总耦合强度；
- **级**：能级，即算符的本征值。

### 1.3 与标准量子力学的类比

| 标准量子力学 | CQM |
|---|---|
| 位置空间 $x$ | 耦合空间 $u = \ln r$ |
| 动量 $\hat{p} = -i\hbar\partial_x$ | $\hat{p}_u = -i\partial_u$ |
| 哈密顿量 $\hat{H} = \hat{p}^2/2m + V$ | $\hat{H} = \hat{D}^2 + 1/4$ |
| 能级 $E_n$ | 耦级 $\mathfrak{c}_n = 1/4+\gamma_n^2$ |

---

## 二、耦级的数学来源

### 2.1 从黎曼零点出发

非平凡零点：

$$\rho_n = \frac12 + i\gamma_n$$

### 2.2 函数方程配对

函数方程 $\xi(s) = \xi(1-s)$ 给出配对：

$$\rho_n \;\longleftrightarrow\; 1-\rho_n$$

$$1-\rho_n = \frac12 - i\gamma_n$$

### 2.3 配对不变量

$$\rho_n(1-\rho_n) = \left(\frac12+i\gamma_n\right)\left(\frac12-i\gamma_n\right) = \frac14 + \gamma_n^2$$

$$\boxed{\mathfrak{c}_n = \rho_n(1-\rho_n) = \frac14 + \gamma_n^2}$$

**耦级是复值零点的模方/配对不变量。**

### 2.4 与 $|\rho_n|^2$ 的关系

在临界线上：

$$1-\rho_n = \overline{\rho_n}$$

所以：

$$\rho_n(1-\rho_n) = \rho_n\overline{\rho_n} = |\rho_n|^2$$

$$\boxed{\mathfrak{c}_n = |\rho_n|^2 = \frac14 + \gamma_n^2}$$

---

## 三、第一耦级

### 3.1 第一个黎曼零点

$$\rho_1 = \frac12 + i\gamma_1$$

$$\gamma_1 = 14.134725141734693790\ldots$$

### 3.2 第一耦级的计算

$$\gamma_1^2 = 199.790454832\ldots$$

$$\mathfrak{c}_1 = \frac14 + \gamma_1^2 = 0.25 + 199.790454832\ldots$$

$$\boxed{\mathfrak{c}_1 = 200.040454832\ldots}$$

### 3.3 反向验证

$$\gamma_1 = \sqrt{\mathfrak{c}_1 - \frac14} = \sqrt{200.040454832 - 0.25} = \sqrt{199.790454832} = 14.134725141\ldots$$

---

## 四、耦级的层级结构

| 耦级 | 零点 | 耦级值 |
|---|---|---|
| $\mathfrak{c}_1$ | $\rho_1 = 1/2 + i \times 14.1347\ldots$ | $200.040454832\ldots$ |
| $\mathfrak{c}_2$ | $\rho_2 = 1/2 + i \times 21.0220\ldots$ | $442.176\ldots$ |
| $\mathfrak{c}_3$ | $\rho_3 = 1/2 + i \times 25.0108\ldots$ | $625.793\ldots$ |
| $\vdots$ | $\vdots$ | $\vdots$ |
| $\mathfrak{c}_n$ | $\rho_n = 1/2 + i\gamma_n$ | $1/4 + \gamma_n^2$ |

---

## 五、耦级的性质

### 5.1 实性

$$\mathfrak{c}_n \in \mathbb{R}, \qquad \mathfrak{c}_n > \frac14$$

因为 $\gamma_n \in \mathbb{R}$。

### 5.2 正定性

$$\mathfrak{c}_n - \frac14 = \gamma_n^2 > 0$$

### 5.3 离散性

耦级是离散序列，对应自伴算符的离散谱。

### 5.4 与零点的对应

$$\boxed{
\mathfrak{c}_n = \frac14 + \gamma_n^2
\;\Longleftrightarrow\;
\gamma_n = \sqrt{\mathfrak{c}_n - \frac14}
\;\Longleftrightarrow\;
\rho_n = \frac12 + i\sqrt{\mathfrak{c}_n - \frac14}
}$$

### 5.5 开方的根据

开方的根据在于算符的**平方结构**：

$$\hat{H} = \hat{D}^2 + \frac14$$

$\hat{D}^2$ 的本征值非负，所以：

$$\mathfrak{c}_n - \frac14 = \gamma_n^2 \geq 0$$

$$\gamma_n = \sqrt{\mathfrak{c}_n - \frac14} \in \mathbb{R}$$

$$\boxed{\text{开方的合法性来自 } \hat{H} = \hat{D}^2+1/4 \text{ 的二次型结构，不来自零点。}}$$

---

## 六、耦级与零点实部的关系

### 6.1 RH 成立时

若 $\rho_n = 1/2 + i\gamma_n$：

$$\mathfrak{c}_n = \frac14 + \gamma_n^2 \in \mathbb{R}$$

### 6.2 RH 不成立时

若 $\rho_n = \beta_n + i\gamma_n$，$\beta_n \neq 1/2$：

$$\rho_n(1-\rho_n) = \beta_n(1-\beta_n) + \gamma_n^2 + i\gamma_n(1-2\beta_n)$$

出现虚部：

$$\boxed{\operatorname{Im}[\rho_n(1-\rho_n)] = \gamma_n(1-2\beta_n)}$$

| 条件 | 耦级性质 |
|---|---|
| $\beta_n = 1/2$ | 耦级为实数 |
| $\beta_n \neq 1/2$ | 耦级为复数 |

$$\boxed{\text{耦级为实数} \;\Longleftrightarrow\; \beta_n = 1/2 \;\Longleftrightarrow\; \text{RH}}$$

---

## 七、耦级与相变量子 $☯$

### 7.1 $☯$ 的定义

$$☯ = \frac{\xi'(1)}{\xi(1)} = 1 + \frac{\gamma}{2} - \frac{1}{2}\ln\pi - \ln 2 \approx 0.0230957$$

### 7.2 $☯$ 的谱表示（RH 成立时的推论）

$$☯ = \sum_n \frac{1}{\gamma_n^2 + 1/4} = \sum_n \frac{1}{\mathfrak{c}_n}$$

$$\boxed{☯ = \sum_n \frac{1}{\mathfrak{c}_n} = \operatorname{Tr}(\hat{H}^{-1})}$$

### 7.3 逻辑方向

$$\text{RH} \;\Longrightarrow\; ☯ = \sum_n \frac{1}{\mathfrak{c}_n}$$

**方向是单向的**：RH 推出这个等式，但这个等式不推出 RH。

**注意**：$☯ = \sum 1/\mathfrak{c}_n$ 是 RH 成立时的**推论**，不是 $☯$ 的定义。$☯$ 的定义是 $\xi'(1)/\xi(1)$，不依赖零点。

---

## 八、耦级的误差结构

### 8.1 带误差的耦级

从谱推导：

$$\mathfrak{c}_n = \gamma_n^2 + \frac14 + O_n$$

误差：

$$O_n = O\!\left(\frac{\gamma_n^2}{n}\right)$$

### 8.2 误差的结构分解

$$O_n = \underbrace{\frac{\gamma_n^2 \vartheta_n^R}{\pi n}}_{O_n^R \text{（实）}} + i\underbrace{\frac{\gamma_n^2 \vartheta_n^I}{\pi n}}_{O_n^I \text{（虚）}} + \cdots$$

| 分量 | 来源 | 作用 |
|---|---|---|
| $O_n^R$ | $\vartheta_n^R$ | 谱的实部平移，可被重标度吸收 |
| $O_n^I$ | $\vartheta_n^I$ | 谱的虚部，**不可被任何平移消除** |

### 8.3 误差虚部与零点偏移

$$O_n^I = 2\gamma_n \delta_n, \qquad \delta_n = \beta_n - \frac12$$

### 8.4 等价链

$$\boxed{
\text{耦级为实数}
\;\Longleftrightarrow\;
O_n^I = 0
\;\Longleftrightarrow\;
\vartheta_n^I = 0
\;\Longleftrightarrow\;
\delta_n = 0
\;\Longleftrightarrow\;
\beta_n = \frac12
\;\Longleftrightarrow\;
\text{RH}
}$$

---

## 九、耦级与自伴性

### 9.1 自伴算符的谱

$$\hat{H} = \hat{D}^2 + \frac14$$

若 $\hat{H}$ 自伴，则：

$$\operatorname{Spec}(\hat{H}) \subset \mathbb{R}$$

### 9.2 耦级的实性

$$\boxed{\text{耦级为实数} \;\Longleftrightarrow\; \hat{H} \text{ 自伴} \;\Longleftrightarrow\; \text{RH}}$$

### 9.3 自伴延拓的相位参数

$\hat{H}$ 作为对称算符，亏指数为 $(1,1)$，有无穷多个自伴延拓，由相位参数 $\vartheta \in \mathbb{R}$ 标记：

$$U = e^{i\vartheta}$$

### 9.4 相位参数与耦级

$$\mathfrak{c}_n = \gamma_n^2 + \frac14 + O_n(\vartheta_n)$$

- 若 $\vartheta_n \in \mathbb{R}$：耦级为实数；
- 若 $\vartheta_n \in \mathbb{C}$：耦级为复数。

$$\boxed{\text{耦级为实数} \;\Longleftrightarrow\; \vartheta_n \in \mathbb{R}}$$

---

## 十、耦级与物理测量

### 10.1 物理测量只能得到实值

$$\boxed{\text{物理测量} \;\longrightarrow\; \text{实值输出}}$$

### 10.2 复值零点不是可观测量

$$\rho_n = \frac12 + i\gamma_n \quad \text{是复值，不是物理可观测量}$$

### 10.3 耦级是物理谱

$$\boxed{\mathfrak{c}_n = \frac14 + \gamma_n^2 \quad \text{是实值，是谱算符的本征值}}$$

> **量纲说明**：耦级 $\mathfrak{c}_n$ 是无量纲数学纯数（$u$ 是对数耦合坐标，无量纲；$\hat{D}$ 无量纲；$\hat{H}$ 无量纲），不是物理能量。物理量纲由 $m_p$ 在下游公式中分配（见 `03 引力与退相干/CQM_引力_GN可能公式.md` §2.2）。

### 10.4 为什么至今未被发现

$$\boxed{
\begin{array}{c}
\text{物理实验只能测量实值} \\
\text{黎曼零点是复值，不是可观测量} \\
\text{耦级是零点的模方，是实值} \\
\text{耦级定义在耦合空间上} \\
\text{耦合空间尚未被实验探索}
\end{array}
}$$

---

## 十一、耦级与 GRH

### 11.1 自守形式的耦级

对自守表示 $\pi$：

$$\mathfrak{c}_{n,\pi} = \frac14 + \gamma_{n,\pi}^2$$

### 11.2 条件传导

$$\boxed{
\begin{array}{c}
\text{自守表示 } \pi \\
\Downarrow \\
\text{条件 } \mathcal{C}_\pi \\
\Downarrow \\
\text{自伴算子 } \hat{H}_\pi \\
\Downarrow \\
\operatorname{Spec}(\hat{H}_\pi) = \{\mathfrak{c}_{n,\pi}\} \\
\Downarrow \\
\text{所有零点在 } 1/2 \text{ 上}
\end{array}
}$$

### 11.3 RH 作为特例

$$\boxed{
\begin{array}{c}
\text{GRH} = \text{对所有自守表示 } \pi \text{，耦级 } \mathfrak{c}_{n,\pi} \text{ 为实数} \\
\Downarrow \\
\text{RH} = \text{GRH在 } \pi = \text{GL}(1) \text{ 平凡表示 时的特例}
\end{array}
}$$

### 11.4 层级结构

| 层级 | 自守表示 | 耦级 | 临界线 |
|---|---|---|---|
| GL(1) 平凡 | 平凡表示 | $\mathfrak{c}_n = 1/4+\gamma_n^2$ | $1/2$ |
| GL(1) 非平凡 | 狄利克雷特征 | $\mathfrak{c}_{n,\chi} = 1/4+\gamma_{n,\chi}^2$ | $1/2$ |
| GL(2) | 模形式/Maass形式 | $\mathfrak{c}_{n,f} = 1/4+\gamma_{n,f}^2$ | $1/2$ |
| GL(n) | 一般自守表示 | $\mathfrak{c}_{n,\pi} = 1/4+\gamma_{n,\pi}^2$ | $1/2$ |

**所有层级共享同一个 $1/2$，但条件、谱、耦级各不相同。**

---

## 十二、耦级与经典化

> **诚实声明**：本节是证明策略层面的分析，非已完成的证明。"经典化消除误差"是路线图主张。

### 12.1 物理系统有误差

$$\mathfrak{c}_n = \gamma_n^2 + \frac14 + O_n$$

### 12.2 经典化的目标

$$\mathcal{C}(O_n) = 0 \quad \text{对所有 } n$$

### 12.3 经典化的等价表述

$$\boxed{
\mathcal{C}(\vartheta_n^I) = 0
\;\Longleftrightarrow\;
\mathcal{C}(O_n^I) = 0
\;\Longleftrightarrow\;
\text{耦级精确为实数}
\;\Longleftrightarrow\;
\text{RH}
}$$

### 12.4 物理截断与数学精确

$$\boxed{
\begin{array}{c}
\text{物理系统：有限，截断，有误差} \\
\text{算术结构：离散，代数，精确} \\
\text{数学证明不需要物理无穷} \\
\text{精确性来自自守形式的代数结构}
\end{array}
}$$

> **参见**：`04 前沿研究/CQM_前沿研究_黎曼猜想证明思路.md` §十四（数学精确与物理截断的互补）对这一区分有更详细的分析。

---

## 十三、耦级的完整逻辑链

$$\boxed{
\begin{array}{c}
\text{黎曼零点 } \rho_n = \frac12 + i\gamma_n \\
\Downarrow \\
\text{函数方程配对 } \rho_n \leftrightarrow 1-\rho_n \\
\Downarrow \\
\text{配对不变量 } \mathfrak{c}_n = \rho_n(1-\rho_n) = \frac14+\gamma_n^2 \\
\Downarrow \\
\text{算符本征值 } \hat{H} = \hat{D}^2 + \frac14 \\
\Downarrow \\
\text{自伴性} \;\Longleftrightarrow\; \mathfrak{c}_n \in \mathbb{R} \\
\Downarrow \\
\text{开方 } \gamma_n = \sqrt{\mathfrak{c}_n - \frac14} \in \mathbb{R} \\
\Downarrow \\
\rho_n = \frac12 + i\gamma_n \\
\Downarrow \\
\text{RH}
\end{array}
}$$

---

## 十四、总结表

| 层面 | 内容 | 数学表达 |
|---|---|---|
| 定义 | 耦级是算符本征值 | $\mathfrak{c}_n = 1/4+\gamma_n^2$ |
| 来源 | 配对不变量 | $\mathfrak{c}_n = \rho_n(1-\rho_n)$ |
| 模方 | 临界线上 | $\mathfrak{c}_n = |\rho_n|^2$ |
| 第一耦级 | 第一个零点对应 | $\mathfrak{c}_1 = 200.040454832\ldots$ |
| 开方 | 算符二次型结构 | $\gamma_n = \sqrt{\mathfrak{c}_n-1/4}$ |
| 实性 | RH 成立时 | $\mathfrak{c}_n \in \mathbb{R}$ |
| 复性 | RH 不成立时 | $\operatorname{Im}(\mathfrak{c}_n) \neq 0$ |
| 与 $☯$ | RH 成立时 | $☯ = \sum 1/\mathfrak{c}_n$ |
| 与自伴性 | 等价 | $\mathfrak{c}_n \in \mathbb{R} \iff \hat{H}$ 自伴 |
| 与 GRH | 推广 | $\mathfrak{c}_{n,\pi} = 1/4+\gamma_{n,\pi}^2$ |
| 物理测量 | 只能测实值 | 耦级是实值，可测量 |
| 经典化 | 消除误差 | $\mathcal{C}(O_n)=0 \iff \mathfrak{c}_n \in \mathbb{R}$ |

---

## 十五、一句话总结

$$\boxed{\text{耦级是复值黎曼零点的模方/配对不变量，是自伴算符的实本征值。}}$$

- **定义**：$\mathfrak{c}_n = 1/4+\gamma_n^2$；
- **来源**：$\mathfrak{c}_n = \rho_n(1-\rho_n) = |\rho_n|^2$；
- **第一耦级**：$\mathfrak{c}_1 = 200.040454832\ldots$；
- **开方根据**：算符的二次型结构 $\hat{H} = \hat{D}^2+1/4$；
- **实性等价于 RH**：$\mathfrak{c}_n \in \mathbb{R} \iff \beta_n = 1/2$；
- **推广给出 GRH**：对每个自守表示 $\pi$，$\mathfrak{c}_{n,\pi} = 1/4+\gamma_{n,\pi}^2$；
- **物理上**：对应耦合空间的谱，尚未被实验发现；
- **经典化**：消除误差 $O_n$，使耦级精确为实数。

---

## 参考文献

1. Riemann, B. (1859). Über die Anzahl der Primzahlen unter einer gegebenen Größe. *Monatsberichte der Königlich Preußischen Akademie der Wissenschaften zu Berlin*, 671–680.
2. Sierra, G. (2008). A quantum mechanical model of the Riemann zeros. *New Journal of Physics*, 10, 033016.
3. Berry, M. V., & Keating, J. P. (1999). The Riemann zeros and eigenvalue asymptotics. *SIAM Review*, 41(2), 236–266.
4. ruster. (2026). *CNT 完整研究*. Zenodo. DOI: 10.5281/zenodo.20804380.

**项目内交叉引用**：

- `01 核心理论/CQM_核心_集成理论.md` §8（Sierra-CQM 定理，耦级的谱推导）
- `03 引力与退相干/CQM_引力_GN可能公式.md` §3（Sierra-CQM 定理，第一耦级数值）
- `04 前沿研究/CQM_前沿研究_黎曼猜想证明思路.md`（RH 证明策略，§十四数学精确与物理截断、§十五自守形式–黎曼零点关联）
- `02 量子引力/CQM_引力_量子引力集成.md` §13（耦级的双重身份与向外衍生）
- `01 核心理论/CQM_核心_朗兰兹分层共振与相变量子.md`（相变量子 $☯$ 的定义与来源）