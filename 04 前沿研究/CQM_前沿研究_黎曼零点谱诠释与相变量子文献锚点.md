# 黎曼零点谱诠释与相变量子的文献锚点

**作者**：ruster

**性质**：前沿研究记录（外部文献数学事实核查 + CQM 构件对应）

**诚实声明**：本文档记录的数学等式（λ₁ = ☯︎、B = −☯︎）均为已验证的数学事实（30 位精度确认），不依赖 CQM 框架任何假设。这些等式在外部文献中独立出现，CQM 的相变量子 ☯︎ 在其中自然涌现。文献与 CQM 的结构对应（§3）属框架诠释，不改变数学事实本身的成立性。

---

## 1. 文献概览

| 编号 | 文件 | 文献 | 核心内容 |
|:---:|:---|:---|:---|
| [V] | `文献/voros.pdf` | Voros (2016), *Simplification of the Keiper/Li approach to RH* | Li 判据 RH⟺λ_n>0 的简化；ξ 对数导数生成函数 |
| [LM] | `文献/lm.pdf` | LeClair & Mussardo (2023), *Riemann zeros as quantized energies* | 散射模型 + Bethe Ansatz，量子化能级 = Riemann 零点虚部 |
| [L] | `文献/lmsf.pdf` | LeClair (2024), *Spectral Flow for the Riemann zeros* | 谱流 $\{E_n(\sigma)\}$ 当 $\sigma\to 1/2$，RH 判据 |
| [SH] | `文献/rev.pdf` | Schumayer & Hutchinson (2011), *Physics of the Riemann Hypothesis* | 综述：Hilbert–Pólya → Berry–Keating → Sierra → Connes |

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

## 3. 与 CQM 的结构对应

### 3.1 相变量子 ☯︎

| 来源 | 表达式 | 文献 |
|:---|:---|:---|
| CQM 定义 | $\xi'(1)/\xi(1) = \sum_{\gamma>0} 1/(\gamma^2+1/4)$ | Hadamard 乘积 |
| Li 第一系数 | $\lambda_1 = 1 - \log(4\pi)/2 + \gamma_E/2$ | [V] |
| LeClair 常数 | $-B = 1 + \gamma_E/2 - \log(2\sqrt{\pi})$ | [L] |

三者在数学上恒等，分属不同框架的自然产物。

### 3.2 黎曼零点谱诠释

**CQM Sierra-CQM 定理**：$\mathfrak{c}_n = 1/4 + \gamma_n^2$，黎曼零点作为耦谱。

**LeClair–Mussardo [LM]**：构造可积散射模型（单粒子在圆上与杂质散射），Bethe Ansatz 方程

$$p_n R + \sum_{j=1}^{N} \phi_j(p_n) = 2\pi\!\left(n - \frac{1}{2}\right)$$

给出的量子化能级 $E_n = E(p_n)$ 等于 Riemann 零点虚部 $\gamma_n$（在 $\Re(s)=1/2$ 轴上）。S-matrix 基于 Euler product，幺正构造 → Hamiltonian 厄米 → 本征值实。

**Schumayer–Hutchinson [SH]**：综述了 Hilbert–Pólya 程序（$R = \frac{1}{2}I + iH$，$H$ 自伴）、Berry–Keating $xp$ 模型、Sierra 自伴扩张、Connes 谱诠释。CQM 的 Sierra-CQM 定理处于此谱系中。

### 3.3 ζ/ξ 算术–谱二分法

**CQM**：$\zeta$ = 算术面孔（Euler 积、有极点、含平凡零点），$\xi$ = 谱面孔（整、无极点、零点集恰好 $\{\gamma_n\}$）。☯︎ 取自 $\xi$。

**LeClair–Mussardo [LM]**：S-matrix 基于 Euler product → 幺正 → 实谱。Euler product 的幺正性是谱实性的保证。

**LeClair [L]**：谱流 $E_n(\sigma)$ 当 $\sigma \to 1/2$ 时，Euler product 幺正性保证谱流实性 → RH 判据。

CQM 的 ζ/ξ 二分法与 LeClair 的 Euler product 幺正性–谱流实性是同一数学结构的两面。

### 3.4 谱流与 Adele Jacobian

**CQM**：Adele Jacobian $\exp(-2/☯)$ 来自 UV→IR 过渡（Tate 自对偶 + 双向平方），☯︎ 出现在指数中。

**LeClair [L]**：谱流 $\{E_n(\sigma)\}$ 当 $\sigma \to 1/2$，描述从临界带内部到临界线的过渡。$B = -☯$ 出现在对数导数 $\Upsilon(s)$ 中。

两者都是"从一面到另一面"的谱过渡：CQM 是 UV（非交换）→ IR（交换），LeClair 是 $\sigma > 1/2 \to \sigma = 1/2$。☯︎ 在两种过渡中均作为关键参数出现。

---

## 4. Li 系数与 GL(n) 层级

Voros [V] 给出 Li 系数的渐近行为（若 RH 成立）：

$$\lambda_n \sim \frac{1}{2}\,n\log n + \frac{1}{2}\,n(\gamma_E - \log 2\pi - 1) + O(n^{1/2}\log n)$$

CQM 中 GL(n) 平凡自守形式给出 $☯_n = n \cdot ☯$，层级因子 $\exp(-2/☯_n) = [\exp(-2/☯)]^{1/n}$。

Li 系数 $\lambda_n$ 与 $n \cdot ☯$ 的关系：$\lambda_1 = ☯$，$\lambda_n$ 的渐近增长 $\sim \frac{1}{2}n\log n$ 给出高阶 Li 系数的增长速率，为 GL(n) 层级因子的渐近行为提供文献参考。

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

## 6. 文献引用信息

| 编号 | 完整引用 |
|:---:|:---|
| [V] | Voros, A. (2016). Simplification of the Keiper/Li approach to the Riemann Hypothesis. 8th DynQua Meeting, Grenoble. Based on preprint IPhT15/106 (June 2015), HAL cea-01166324. |
| [LM] | LeClair, A. & Mussardo, G. (2023). Riemann zeros as quantized energies of scattering with impurities. arXiv:2307.01254. |
| [L] | LeClair, A. (2024). Spectral Flow for the Riemann zeros. arXiv:2406.01828. |
| [SH] | Schumayer, D. & Hutchinson, D. A. W. (2011). Physics of the Riemann Hypothesis. arXiv:1101.3116 [math-ph]. |

PDF 文件存放于 `文献/` 目录。