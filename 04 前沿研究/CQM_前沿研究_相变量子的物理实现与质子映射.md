# 相变量子的物理实现与质子映射

**作者**：ruster

**性质**：前沿研究记录（外部文献数学事实核查 + 模型核查 + $G_N$ 推导的物理实现基础）

**诚实声明**：本文档分三层内容，其成立性不同。（1）**数学事实层**：$\lambda_1 = ☯$、$B = -☯$ 两个等式均为已验证的数学事实（30 位精度确认），不依赖 CQM 框架任何假设。（2）**模型核查层**：§3 的排除清单基于对候选模型全文的实际核查，核查结论是确定性的"该文献是否出现该常数"。（3）**推导基础层**：建立本映射的核心目标是 $G_N$ 推导——LeClair 模型作为谱面孔的物理实现，为 $G_N$ 公式的普适因子（$☯^2$、$\exp(-2/☯)$）提供物理来源，并为质子特有参数（$\lambda_c$、$\mathfrak{c}_1$、$\kappa$）的推导提供模型基础。推导任务已定位（§6.6），其中 ☯︎ 的实现归属已论证，$\lambda_c$、$\mathfrak{c}_1$、$\kappa$ 的推导尚未完成；映射不提供 $m_p$ 数值（$m_p$ 仍是 $G_N$ 公式的量纲锚点输入），不改变推导路径的依赖方向（§6.6），且不进入 QG 框架（QG 框架不使用黎曼零点）。三层界限在正文中逐节标注。

---

## 1. 文献概览

| 编号 | 文件 | 文献 | 核心内容 |
|:---:|:---|:---|:---|
| [V] | `文献/voros.pdf` | Voros (2016), *Simplification of the Keiper/Li approach to RH* | Li 判据 RH⟺λ_n>0 的简化；ξ 对数导数生成函数 |
| [LM] | `文献/lm.pdf` | LeClair & Mussardo (2023), *Riemann zeros as quantized energies* | 散射模型 + Bethe Ansatz，量子化能级 = Riemann 零点虚部 |
| [L] | `文献/lmsf.pdf` | LeClair (2024), *Spectral Flow for the Riemann zeros* | 谱流 $\{E_n(\sigma)\}$ 当 $\sigma\to 1/2$，RH 判据 |
| [SH] | `文献/rev.pdf` | Schumayer & Hutchinson (2011), *Physics of the Riemann Hypothesis* | 综述：Hilbert–Pólya → Berry–Keating → Sierra → Connes |

§3 模型核查另行引用以下文献（全文核查，PDF 未入库，arXiv 编号见表）：

| 编号 | 文献 | 核查结论 |
|:---:|:---|:---|
| [BBM] | Bender, Brody & Müller (2017), arXiv:1608.03679 | 不涌现 ☯︎ |
| [S08] | Sierra (2008), New J. Phys. 10, 033016, arXiv:0712.0705 | 不涌现 ☯︎ |
| [S16] | Sierra (2016), arXiv:1601.01797 | 不涌现 ☯︎ |
| [LC06] | LeClair (2006/2008), arXiv:math-ph/0611043 | 不涌现 ☯︎ |
| [FL] | França & LeClair (2014/2024), arXiv:1407.4358 | 不涌现 ☯︎ |
| [Y] | Yakaboylu (2024–2026), arXiv:2408.15135 v17 | 组合形式，非 ☯︎ 本身 |

---

## 2. 核心发现：☯︎ 在外部文献中的两个独立锚点

### 2.1 发现一：$\lambda_1 = ☯$（Voros [V]）

**Li 系数的生成函数**（Keiper 1992, Li 1997）：

$$\sum_{n=1}^{\infty} \lambda_n\, z^{n-1} = \frac{d}{dz}\log\!\left[2\,\xi\!\left(\frac{1}{1-z}\right)\right]$$

**第一系数显式值** [V]：

$$\lambda_1 = 1 - \frac{\log 4\pi}{2} + \frac{\gamma_E}{2} \approx 0.0230957$$

**CQM 相变量子**：

$$☯ = \frac{d}{ds}\ln\xi(s)\bigg|_{s=1} = 1 + \frac{\gamma_E}{2} - \frac{\log\pi}{2} - \log 2 = 1 - \frac{\log 4\pi}{2} + \frac{\gamma_E}{2}$$

$$\boxed{\lambda_1 = ☯}$$

**验证**：30 位精度确认 $|\lambda_1 - ☯| < 10^{-30}$。

**Li 判据** [V]：RH $\Leftrightarrow$ $\lambda_n > 0$ for all $n$。$☯ = \lambda_1 > 0$ 满足 $n=1$ 条件。

**Voros 渐近公式**（若 RH 成立）[V]：

$$\lambda_n \sim \frac{1}{2}\,n\log n + \frac{1}{2}\,n(\gamma_E - \log 2\pi - 1) + O(n^{1/2}\log n)$$

### 2.2 发现二：$B = -☯$（LeClair [L] 公式 42）

LeClair 对 ξ 函数方程取对数导数 [L, eq. (41)]：

$$-\Upsilon(s) = \frac{1}{s-1} - B - \log\sqrt{\pi} + \frac{1}{2}\frac{\Gamma'(s/2+1)}{\Gamma(s/2+1)} - \sum_\rho\left(\frac{1}{s-\rho} + \frac{1}{\rho}\right)$$

其中常数 [L, eq. (42)]：

$$B = -\frac{\gamma_E}{2} - 1 + \log(2\sqrt{\pi})$$

**与 ☯︎ 的关系**：

$$B = -\!\left(1 + \frac{\gamma_E}{2} - \log(2\sqrt{\pi})\right) = -\!\left(1 + \frac{\gamma_E}{2} - \frac{\log\pi}{2} - \log 2\right) = -☯$$

$$\boxed{B = -☯}$$

**验证**：30 位精度确认 $|B + ☯| < 10^{-30}$。

### 2.3 两个锚点的独立性

$\lambda_1$ 来自 Li 系数生成函数（Keiper–Li 框架），$B$ 来自 ξ 函数方程的对数导数（Hilbert–Pólya 谱流框架）。两者从不同数学结构出发，均给出 ☯︎，表明 ☯︎ 是 ξ 对数导数在 $s=1$ 的**自然不变量**，不依赖特定物理框架的选择。

---

## 3. 模型核查：哪些物理实现不涌现 ☯︎

围绕"是否存在 LeClair 模型之外、同样导出 ☯︎ 的物理实现"这一问题，对候选模型逐一进行全文核查（非摘要判断）。核查方法：提取全文，搜索 $\gamma_E/2 - \log(2\sqrt{\pi})$ 型常数组合及数值 $0.0230957$。

### 3.1 排除清单

| 模型 | 机制 | 核查结论 | 不涌现的结构原因 |
|:---|:---|:---:|:---|
| Berry–Keating 家族：Sierra [S08][S16]、Bender–Brody–Müller [BBM] | $xp$ 哈密顿量自伴扩张；Jost 函数经 Riemann–Siegel 公式调谐至 $\zeta$；或 Hurwitz zeta 边界条件 $\psi(0)=0$ 直接锁定零点 | 无 ☯︎ | 使用 $\vartheta(t)$ 相位与 $\zeta$ 的**线性表示**，不取对数导数 |
| LeClair 早期 [LC06] | 1d 费米气体 + 准周期势，$\mathrm{Li}_\nu$ 伪能量方程 $\delta=-\Re[T^{\nu-1}h_\nu\,\mathrm{Li}_\nu(-z_\delta)]$，$\zeta(\nu)=0 \Leftrightarrow$ 压强修正为零 | 无 ☯︎ | 多对数函数方程，不取对数导数 |
| França–LeClair [FL] | 第 $n$ 零点超越方程（Lambert $W$），平滑项 + $\arg\zeta$ | 无 ☯︎ | 不取对数导数在 $s=1$ 的取值 |
| Yakaboylu [Y] | $\Lambda(s)=\Gamma(s+1)(1-2^{1-s})\zeta(s)$ 的算符实现，Weil–Bombieri 正性判据 | 组合形式 | 若取 $\Lambda'/\Lambda(1)$ 得 $1-\gamma_E+\log 2+☯$，是组合而非 ☯︎ 本身 |

### 3.2 结构性结论

$$\boxed{
\text{LeClair–Mussardo 谱流模型是当前唯一让 } ☯ \text{ 以物理常数身份涌现的散射实现。}
}$$

原因在于 ☯︎ 的数学本质：$☯ = \xi'(1)/\xi(1)$ 是 **ξ 对数导数在 $s=1$ 的正则值**。文献中 ☯︎ 的三个独立来源全部经过对数导数结构：

1. **Keiper–Li 生成函数**：$\lambda_1 = \xi'(1)/\xi(1)$（数学侧）；
2. **LeClair 谱流 $\Upsilon(s)=\zeta'/\zeta$ 分解**：$B = -☯$（物理侧唯一）；
3. **CQM Hadamard 乘积**：$\xi'(1)/\xi(1) = \sum_{\gamma>0} 1/(\gamma^2+1/4)$。

Berry–Keating 家族（Sierra、Bender–Brody–Müller、Connes 谱实现）全部绕开对数导数，故均不涌现 ☯︎。这一核查同时强化了 LeClair 模型作为 CQM 相变量子外部锚点的地位。

---

## 4. 与 CQM 的结构对应

### 4.1 相变量子 ☯︎

| 来源 | 表达式 | 文献 |
|:---|:---|:---|
| CQM 定义 | $\xi'(1)/\xi(1) = \sum_{\gamma>0} 1/(\gamma^2+1/4)$ | Hadamard 乘积 |
| Li 第一系数 | $\lambda_1 = 1 - \log(4\pi)/2 + \gamma_E/2$ | [V] |
| LeClair 常数 | $-B = 1 + \gamma_E/2 - \log(2\sqrt{\pi})$ | [L] |

三者在数学上恒等，分属不同框架的自然产物。

### 4.2 黎曼零点谱诠释

**CQM Sierra-CQM 定理**：$\mathfrak{c}_n = 1/4 + \gamma_n^2$，黎曼零点作为耦谱。

**LeClair–Mussardo [LM]**：构造可积散射模型（单粒子在圆上与杂质散射），Bethe Ansatz 方程

$$p_n R + \sum_{j=1}^{N} \phi_j(p_n) = 2\pi\!\left(n - \frac{1}{2}\right)$$

给出的量子化能级 $E_n = E(p_n)$ 等于 Riemann 零点虚部 $\gamma_n$（在 $\Re(s)=1/2$ 轴上）。S-matrix 基于 Euler product，幺正构造 → Hamiltonian 厄米 → 本征值实。

**Schumayer–Hutchinson [SH]**：综述了 Hilbert–Pólya 程序（$R = \frac{1}{2}I + iH$，$H$ 自伴）、Berry–Keating $xp$ 模型、Sierra 自伴扩张、Connes 谱诠释。CQM 的 Sierra-CQM 定理处于此谱系中。

### 4.3 ζ/ξ 算术–谱二分法

**CQM**：$\zeta$ = 算术面孔（Euler 积、有极点、含平凡零点），$\xi$ = 谱面孔（整、无极点、零点集恰好 $\{\gamma_n\}$）。☯︎ 取自 $\xi$。

**LeClair–Mussardo [LM]**：S-matrix 基于 Euler product → 幺正 → 实谱。Euler product 的幺正性是谱实性的保证。

**LeClair [L]**：谱流 $E_n(\sigma)$ 当 $\sigma \to 1/2$ 时，Euler product 幺正性保证谱流实性 → RH 判据。

CQM 的 ζ/ξ 二分法与 LeClair 的 Euler product 幺正性–谱流实性是同一数学结构的两面。

### 4.4 谱流与 Adele Jacobian

**CQM**：Adele Jacobian $\exp(-2/☯)$ 来自 UV→IR 过渡（Tate 自对偶 + 双向平方），☯︎ 出现在指数中。

**LeClair [L]**：谱流 $\{E_n(\sigma)\}$ 当 $\sigma \to 1/2$，描述从临界带内部到临界线的过渡。$B = -☯$ 出现在对数导数 $\Upsilon(s)$ 中。

两者都是"从一面到另一面"的谱过渡：CQM 是 UV（非交换）→ IR（交换），LeClair 是 $\sigma > 1/2 \to \sigma = 1/2$。☯︎ 在两种过渡中均作为关键参数出现。

---

## 5. LeClair 模型的完整数学结构

本节系统梳理 LeClair–Mussardo [LM] 及 LeClair [L] 两篇文献的完整数学物理结构，不添加 CQM 诠释，仅忠实记录文献内容并标注公式编号。

### 5.1 物理设置

单粒子在周长 $R$ 的圆上运动，圆上分布 $N$ 个静止杂质，标记 $j = 1, 2, \ldots, N$（图见 [LM, Fig. 1]）。散射满足**纯透射条件**（无反射），因此多杂质 S-matrix 因子化：

$$S(p) = \prod_{j=1}^{N} S_j(p)$$

粒子绕圆一周后波函数单值性给出量子化条件 [LM, eq. (2)]：

$$e^{ipR} \prod_{j=1}^{N} S_j(p) = \pm 1$$

取费米子（$-1$），得 Bethe Ansatz 方程 [LM, eq. (3)]：

$$p_n R + \sum_{j=1}^{N} \varphi_j(p_n) = 2\pi\!\left(n - \frac{1}{2}\right)$$

其中 $\varphi_j(p)$ 为第 $j$ 个杂质的散射相移。

### 5.2 色散关系

自由粒子色散关系取 [LM, eq. (5)]：

$$p(E) = E \log\!\left(\frac{E}{2\pi e}\right)$$

逆函数用 Lambert $W$ 函数表示 [LM, eq. (6)]：

$$E(p) = \frac{p}{W(p/(2\pi e))}$$

大 $p$ 渐近 [LM, eq. (7)]：

$$E(p) \approx \frac{p}{\log p}$$

**群速度**：

$$\frac{dE}{dp} \approx \frac{1}{\log p} - \frac{1}{(\log p)^2} \xrightarrow{p \to \infty} \frac{1}{\log p} \to 0$$

群速度随动量递减，与 QFT 中渐近自由定性类似：高能（大 $p$）下粒子"减速"。

### 5.3 S-matrix 构造

每个杂质关联一个正实数 $q_j > 1$ 和常相位 $\varphi_j$。S-matrix 取 [LM, eq. (8)]：

$$S_j(E) = \frac{q_j^{\sigma} - e^{i(E \log q_j - \varphi_j)}}{q_j^{\sigma} - e^{-i(E \log q_j - \varphi_j)}}$$

其中 $\sigma > 0$ 为自由参数。散射相移 [LM, eq. (9)]：

$$\varphi_j(E) = -2\,\Im\log\!\left(1 - \frac{e^{-i(E \log q_j - \varphi_j)}}{q_j^{\sigma}}\right)$$

**幺正性**：$|S_j(E)| = 1$ 当且仅当 $q_j^{\sigma}$ 为实数（即 $\sigma$ 为实数），此时 $S_j = e^{i\varphi_j}$ 为纯相位。

**关键选择**：取 $q_j$ 为第 $j$ 个素数 $p_j$，即 $\{q_1, q_2, q_3, \ldots\} = \{2, 3, 5, \ldots\}$，并取 $\varphi_j = 0$。

### 5.4 Bethe Ansatz 方程与 ζ 函数涌现

取 $R = 1$、$q_j = p_j$（素数）、$\varphi_j = 0$，Bethe Ansatz 方程化为 [LM, eq. (10)]：

$$\frac{E_n}{2}\log\!\left(\frac{E_n}{2\pi e}\right) - \sum_{j=1}^{N} \Im\log\!\left(1 - \frac{e^{-i E_n \log p_j}}{p_j^{\sigma}}\right) = \left(n - \frac{3}{2}\right)\pi$$

当 $\sigma > 1$、$N \to \infty$ 时，散射相移求和收敛为 $\arg\zeta$ [LM, eq. (11)]：

$$\frac{E_n}{2}\log\!\left(\frac{E_n}{2\pi e}\right) + \arg\zeta(\sigma + iE_n) = \left(n - \frac{3}{2}\right)\pi$$

其中 $s = \sigma + iE$，$\zeta(s)$ 的 Euler 乘积 [LM, eq. (12)]：

$$\zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s} = \prod_{j=1}^{\infty} \frac{1}{1 - p_j^{-s}}, \quad \Re(s) > 1$$

**方程结构**：左端第一项为平滑项（Riemann–von Mangoldt 平均密度），$\arg\zeta$ 为振荡项（来自 Euler 乘积的相位）。当 $\sigma \to 1/2^+$，解 $E_n$ 趋于 Riemann 零点虚部 $\gamma_n$。

### 5.5 谱流方程

LeClair [L] 研究 $E_n(\sigma)$ 对 $\sigma$ 的依赖。对 Bethe Ansatz 方程求 $\sigma$ 导数 [L, eq. (21)]：

$$\frac{dE_n(\sigma)}{d\sigma} = -\frac{\Im(\Upsilon(s))}{\Re(\Upsilon(s)) + \vartheta'(E_n(\sigma))}, \quad s = \sigma + iE_n(\sigma)$$

其中 [L, eq. (22)]：

$$\Upsilon(s) = \frac{\zeta'(s)}{\zeta(s)}$$

Euler 乘积形式 [L, eq. (27)]：

$$-\Upsilon(s) = \sum_{p} \frac{\log p}{p^s - 1}, \quad \Re(s) > 1$$

$\Upsilon(s)$ 的解析延拓 [L, eq. (41)]：

$$-\Upsilon(s) = \frac{1}{s-1} - B - \log\sqrt{\pi} + \frac{1}{2}\frac{\Gamma'(s/2+1)}{\Gamma(s/2+1)} - \sum_{\rho}\left(\frac{1}{s-\rho} + \frac{1}{\rho}\right)$$

常数 $B$ [L, eq. (42)]：

$$B = -\frac{\gamma_E}{2} - 1 + \log(2\sqrt{\pi}) = -0.0230957\ldots = -☯$$

### 5.6 RH 判据

**命题 2** [L, eq. (23)–(24)]：若存在 $\sigma_* > 1/2$ 和区域 $t_1 < t < t_2$ 使得

$$-\Re(\Upsilon(s)) < \vartheta'(t), \quad s = \sigma_* + it$$

则该区域中所有 $E_n(\sigma)$（$\sigma > \sigma_*$）为实数。大 $t$ 等价形式：

$$-\Re(\Upsilon(s)) \lesssim \frac{1}{2}\log\!\left(\frac{t}{2\pi}\right)$$

**命题 3** [L, eq. (26)]：临界线上（$\sigma = 1/2$），对任意非零点 $t$：

$$-\Re(\Upsilon(s)) \simeq \frac{1}{2}\log\!\left(\frac{t}{2\pi}\right), \quad s = \frac{1}{2} + it$$

此为**等式**而非不等式。命题 2 已被 Lagarias 证明等价于 RH [L, Sec. V]。

### 5.7 物理链条：素数 → RH

LeClair 模型的完整逻辑链条：

$$\text{素数} \xRightarrow{\text{标记杂质}} \text{Euler 乘积} \xRightarrow{\text{构造} S_j} |S_j| = 1 \xRightarrow{S = e^{-iH}} H = H^\dagger \xRightarrow{\text{厄米}} E_n \in \mathbb{R} \xRightarrow{\sigma \to 1/2} \text{RH}$$

每一步的必要性由反例佐证：Davenport–Heilbronn 函数 $D(s)$ 满足函数方程 $\chi(s) = \chi(1-s)$ 但**无 Euler 乘积** [L, Sec. IV]。因此无法构造幺正 S-matrix，$H$ 非厄米，存在复本征值，RH 不成立。这证明 Euler 乘积（即素数结构）是整个链条的不可替代基石。

### 5.8 ☯︎ 在谱流中的角色

在 $\Upsilon(s)$ 的解析延拓 [L, eq. (41)] 中，常数 $B = -☯$ 与 $1/(s-1)$（极点项）、$\log\sqrt{\pi}$（Gamma 因子项）、零点求和项并列出现。谱流方程 [L, eq. (21)] 的分子 $\Im(\Upsilon)$ 和分母 $\Re(\Upsilon) + \vartheta'$ 均含 $B$。

☯︎ 的数值微小（$\approx 0.023$）意味着 $B$ 接近零：谱流方程中常数项贡献小，$E_n(\sigma)$ 随 $\sigma$ 变化平缓。LeClair 的数值计算 [L, Fig. 3] 显示 $E_n(\sigma)$ 从 $\sigma > 1$ 到 $\sigma = 1/2$ 的变形"without a great deal of variation nor drama"——谱流近乎刚性。此近刚性的定量基础即 $|B| = ☯ \ll 1$。

**反例对比**：Davenport–Heilbronn 函数无 Euler 乘积，$\Upsilon(s)$ 无上述分解，谱流行为定性不同 [L, Fig. 10]，$E_n(\sigma)$ 出现复分支。

---

## 6. 质子映射：LeClair–Mussardo 模型在 CQM 体系中的定位

**本节性质：映射与推导定位**。§6.2–§6.4 的对应是结构类比（不是已完成的推导）；§6.6 给出该映射服务的 $G_N$ 推导任务分解。本节不为任何数值结果提供已完成的依据——$G_N$ 推导中各参数的数值推导状态见 §6.6 任务表。

### 6.1 量纲发生学定位：质量层与质子

按 `CQM_核心_量纲与单位制` 的量纲发生学层级：

| 层级 | 内容 | 转换常数 |
|:---|:---|:---|
| 时间层 | 第一个量纲 $T$（因果时、固有时） | 未知（可能没有）；固有时来自事件计数 |
| 时间–长度层 | $L = c\,T$ | $1/c$ |
| **质量层** | $M = L^3/(G_N\,T^2)$ | $G_N$ |
| 电荷层 | $[q] = M^{1/2}L^{3/2}T^{-1}$ | $K_Q$ |

质子在体系中的位置：

1. **质量层的稳定复合单元**：质子是质量层中绝对稳定的最低重子态（实验寿命下限 $> 10^{34}$ 年）；
2. **声子理论的振荡源**：声子源于中子/质子振荡（`CQM_核心_声子理论`），$m_e/m_p$ 推导链位于声子理论 §8.3；
3. **$G_N$ 公式的量纲锚点**：$G_N$ 可能公式以 $m_p$ 为唯一量纲锚点输入（见 §6.3）。

问题由此产生：$G_N$ 公式中出现的 $☯^2$ 与 $\exp(-2/☯)$ 来自谱面孔，而质子是质量层对象——**谱面孔的普适权重如何落实到质量层的复合单元上**？这正是建立 LeClair 模型映射的核心目标：为 $G_N$ 推导提供谱面孔侧的实现基础。§6.2–§6.4 建立映射，§6.6 给出推导任务分解。

### 6.2 质子的 $L/T$ 属性与 LeClair 模型要素的对应

`CQM_前沿研究_质量研究思路汇总` §3 给出质子的两个属性：$L$ 属性（质子几何延展，数学对象 $A_4$ 谱几何）与 $T$ 属性（质子再生产周期，数学对象为内部振荡模式）。LeClair 模型的核心要素与这两个属性存在逐项对应：

| 质子属性（质量研究思路汇总 §3） | LeClair 模型要素（本文 §5） | 对应内容 |
|:---|:---|:---|
| $L$ 属性：几何延展（$A_4$ 谱几何） | 圆（紧致空间，周长 $R$） | 紧致性给出有限空间延展；$A_4$ 谱几何与圆谱同属"几何对象的谱"这一数学类别 |
| $T$ 属性：再生产周期（内部振荡模式） | Bethe Ansatz 离散谱（圆上绕行量子化） | 离散谱是振荡模式的数学表达；绕行周期量子化给出离散能级 |

对应的共同数学基础：**紧致空间上的量子化给出离散谱**。$A_4$ 谱几何（边–面关联矩阵 $M = E^T E$，$10\times 10$，谱 $\{9^{(1)}, 4^{(4)}, 1^{(5)}\}$）与 LeClair 圆上的 Bethe Ansatz 都属于这一类别。这是类比的支点，也是类比的边界——二者的谱数据（$\{9,4,1\}$ vs $\{\gamma_n\}$）完全不同，对应只在机制层面成立。

### 6.3 $G_N$ 公式的普适/质子特有分解与实现归属

`CQM_前沿研究_质量研究思路汇总` §5、§6.4 给出 $G_N$ 可能公式及其分解：

$$G_N = \frac{\hbar c}{m_p^2} \cdot I \cdot \lambda_c \cdot ☯^2 \cdot \mathfrak{c}_1 \cdot \exp(-2/☯) \cdot (1 + \kappa ☯)$$

| 因子 | 来源 | 性质 | LeClair 模型中的归属 |
|:---|:---|:---|:---|
| $I = 5/3$ | $\mathrm{SU}(5)$ Dynkin 指数比 | 质子特有 | 无对应（模型不含 $\mathrm{SU}(5)$ 结构） |
| $\lambda_c$ | Mathieu 临界参数 | 质子特有 | 无对应 |
| $\mathfrak{c}_1$ | 谱系数 $1/4+\gamma_1^2$ | 质子特有 | 有谱学背景（第一 Riemann 零点），但模型不产生此值 |
| $\kappa$ | 修正系数 $(31+☯)/30$ | 质子特有 | 无对应 |
| $☯^2$ | 全局谱权重 | 普适常数 | **谱流刚度**（§5.8：$|B|=\☯\ll 1$，谱对 $\sigma$ 微扰的刚性响应） |
| $\exp(-2/☯)$ | 全局谱行为 | 普适常数 | **谱面孔全局压制行为**（模型中谱流近刚性对应的极端稳定性） |
| $m_p$ | 量纲锚点 | 实验输入 | 无对应（见 §6.5 失效点） |

分解解读：

$$\boxed{
\text{普适 } ☯ \text{（谱流实现候选：LeClair）} \;+\; \text{质子特有 } \pi_p \text{（} A_4 \text{ 谱几何）} \;\Longrightarrow\; G_N
}$$

LeClair 模型映射的是公式中**普适部分**的物理图像（谱权重与谱压制行为），不映射**质子特有部分**（$I, \lambda_c, \mathfrak{c}_1, \kappa$ 的来源仍是 $A_4$ 谱几何与 $\pi_p$ 构造，见质量研究思路汇总 §13 开放问题）。

### 6.4 映射的三层依据

在全部候选实现（§3 排除清单）中，LeClair–Mussardo 模型最能映射到质子，依据有三：

**（1）禁闭拓扑**（最强对应）。模型的核心量子化机制是"粒子困在圆上，波函数单值性 → Bethe Ansatz 离散谱"。质子的核心物理正是"夸克困在 $\sim 1$ fm 内 → 离散强子谱"。紧致空间 + 周期边界条件的禁闭–量子化同构，在所有候选实现中独此一家：Berry–Keating 家族（$xp$ 半直线自由运动）与 LeClair 早期准周期势均无此结构。

**（2）费米子与多散射中心**。模型粒子为费米子（量子化条件取 $-1$ 支），与质子自旋 $1/2$ 的统计性质一致；Bethe Ansatz 是"多散射中心自洽量子化"的最简可积实现，与质子作为三夸克多体束缚态的定性特征匹配。

**（3）谱流刚度与稳定性**。☯︎ 在模型中的物理角色是谱流刚度——谱对参数微扰的刚性响应（$|B| = ☯ \ll 1$）。质子作为绝对稳定重子（寿命下限 $> 10^{34}$ 年），其稳定性正是谱刚性的物理体现。这与 CQM 内 $\exp(-2/☯) \sim 10^{-38}$ 极端压制的角色同型（§4.4）。

### 6.5 映射的失效点（诚实标注）

- **素数与夸克不匹配**：质子只有 3 个价夸克，不是素数序列。素数在模型中是 Euler 乘积的生成元（算术面孔的给定结构），质子是质量层稳定单元——二者角色类似（"不可再分的基本单元"），但结构不同。映射只能到禁闭拓扑与统计性质层面，**不能映射到内部成分**。
- **不提供 $m_p$ 数值**：LeClair 模型不含任何能产出 $m_p$ 的结构。$m_e/m_p$ 的推导链在声子理论 §8.3（中子/质子振荡）。这不阻碍 $G_N$ 推导：$G_N$ 公式以 $m_p$ 为量纲锚点输入（§6.1），推导目标是其余因子的来源（§6.6）。
- **色散关系无质子对应**：模型色散关系 $E(p) \approx p/\log p$ 的对数修正来自素数分布，质子内部动力学（QCD 禁闭）无此结构。
- **$A_4$ 谱数据不同**：§6.2 的对应只在"紧致空间量子化"机制层面成立，$\{9^{(1)},4^{(4)},1^{(5)}\}$ 与 $\{\gamma_n\}$ 是两组不同的谱数据，不得混同。

### 6.6 推导定位：服务于 $G_N$ 推导

**建立本映射的核心目标是 $G_N$ 推导**。$G_N$ 可能公式（§6.3）中，质子特有参数 $\lambda_c$、$\mathfrak{c}_1$、$\kappa$ 的来源是质量研究思路汇总 §13 的开放问题；LeClair 模型映射到质子，正是为这些参数的推导提供模型物理结构。本映射在 CQM 体系中的定位：

| 层 | 内容 | 状态 |
|:---|:---|:---|
| 数学事实层 | $\lambda_1 = ☯$、$B = -☯$（§2） | 已验证（30 位精度） |
| 实现归属层 | $☯^2$、$\exp(-2/☯)$ 的物理来源 = 谱流刚度（§5.8、§6.3） | 已论证 |
| 推导任务层 | $\lambda_c$、$\mathfrak{c}_1$、$\kappa$ 从模型结构的推导 | **已定位，未完成** |

**推导任务分解**（从 $G_N$ 公式的待定参数出发）：

1. **$☯$ 因子（已完成归属论证）**：$☯^2$ 与 $\exp(-2/☯)$ 的物理来源是谱流刚度——模型谱对 $\sigma$ 微扰的刚性响应（$|B| = ☯ \ll 1$）。数学侧：$B = -☯$ 是 [L] 公式 (42) 的数学事实；物理侧：谱流刚度即谱面孔全局权重与压制行为的机制。
2. **$\mathfrak{c}_1 = 1/4 + \gamma_1^2$（待推导）**：第一 Riemann 零点的谱系数。模型中第一激发态对应的 Bethe Ansatz 结构是否给出此值的推导路径，是下一步任务。
3. **$\lambda_c$（待推导）**：Mathieu 临界参数 $q_c \approx 0.329$（DLMF $b_1(q) = 2q$ 的根）。模型圆谱与 Mathieu 谱的关联需建立。
4. **$\kappa = (31 + ☯)/30$（待推导）**：组合–谱对应（$30 = A_4$ 边–面关联矩阵迹）与 ☯︎ 的组合方式需从模型结构推出。

**依赖方向**：`CQM_前沿研究_质量研究思路汇总` §7 明确 $G_N$ 公式路径与自守路径互斥、不得互为前提。本映射在 $G_N$ 公式路径内部工作：为该公式的参数提供来源推导，不引入"由质量数据反推"的第二条路径。☯︎ 的提取来源仍是 $\mathrm{GL}(n)$ 平凡自守形式 $L$ 函数（质量研究思路汇总 §6.3），LeClair 模型是这一提取结果在物理侧的实现，二者是同一对象的两面而非两条独立路径。

**与 QG 框架的边界**：QG 框架不使用黎曼零点。本文档属前沿研究层，讨论黎曼零点谱诠释（§4.2 Sierra-CQM 定理）不改变 QG 框架的这一既定边界。

---

## 7. Li 系数与 GL(n) 层级

Voros [V] 给出 Li 系数的渐近行为（若 RH 成立）：

$$\lambda_n \sim \frac{1}{2}\,n\log n + \frac{1}{2}\,n(\gamma_E - \log 2\pi - 1) + O(n^{1/2}\log n)$$

CQM 中 GL(n) 平凡自守形式给出 $☯_n = n \cdot ☯$，层级因子 $\exp(-2/☯_n) = [\exp(-2/☯)]^{1/n}$。

Li 系数 $\lambda_n$ 与 $n \cdot ☯$ 的关系：$\lambda_1 = ☯$，$\lambda_n$ 的渐近增长 $\sim \frac{1}{2}n\log n$ 给出高阶 Li 系数的增长速率，为 GL(n) 层级因子的渐近行为提供文献参考。

---

## 8. 文献引用信息

| 编号 | 完整引用 |
|:---:|:---|
| [V] | Voros, A. (2016). Simplification of the Keiper/Li approach to the Riemann Hypothesis. 8th DynQua Meeting, Grenoble. Based on preprint IPhT15/106 (June 2015), HAL cea-01166324. |
| [LM] | LeClair, A. & Mussardo, G. (2023). Riemann zeros as quantized energies of scattering with impurities. arXiv:2307.01254. JHEP 2024, 62 (2024). |
| [L] | LeClair, A. (2024). Spectral Flow for the Riemann zeros. arXiv:2406.01828. Adv. Theor. Math. Phys. (2025). |
| [SH] | Schumayer, D. & Hutchinson, D. A. W. (2011). Physics of the Riemann Hypothesis. arXiv:1101.3116 [math-ph]. |
| [BBM] | Bender, C. M., Brody, D. C. & Müller, M. P. (2017). Hamiltonian for the zeros of the Riemann zeta function. Phys. Rev. Lett. 118, 130201. arXiv:1608.03679. |
| [S08] | Sierra, G. (2008). A quantum mechanical model of the Riemann zeros. New J. Phys. 10, 033016. arXiv:0712.0705. |
| [S16] | Sierra, G. (2016). The Riemann zeros as spectrum and the Riemann hypothesis. Symmetry 11(4), 494 (2019). arXiv:1601.01797. |
| [LC06] | LeClair, A. (2006/2008). Interacting Bose and Fermi gases in low dimensions and the Riemann hypothesis. Int. J. Mod. Phys. A 23, 1371 (2008). arXiv:math-ph/0611043. |
| [FL] | França, G. & LeClair, A. (2014/2024). A theory for the zeros of Riemann ζ and other L-functions (updated). arXiv:1407.4358. |
| [Y] | Yakaboylu, E. (2024–2026). Nontrivial Riemann Zeros as Spectrum. arXiv:2408.15135. |

PDF 文件存放于 `文献/` 目录；§3 核查文献未入库，以 arXiv 编号定位。

---

## 附：内部交叉引用

| 本文 | 引用对象 |
|:---|:---|
| §6.1 | `01 核心理论/CQM_核心_量纲与单位制.md` §6.0（量纲发生学层级表） |
| §6.2 | `04 前沿研究/CQM_前沿研究_质量研究思路汇总.md` §3（质子 $L/T$ 属性、$A_4$ 谱几何） |
| §6.3 | `04 前沿研究/CQM_前沿研究_质量研究思路汇总.md` §5、§6.3、§6.4（$G_N$ 可能公式、分解表、普适/质子特有分层） |
| §6.5 | `03 引力与退相干/CQM_引力_GN可能公式.md`（$\mathfrak{c}_1 = 1/4+\gamma_1^2$）；声子理论 §8.3（$m_e/m_p$ 推导链） |
| §6.6 | `04 前沿研究/CQM_前沿研究_质量研究思路汇总.md` §7（依赖方向）；QG 框架黎曼零点边界 |
