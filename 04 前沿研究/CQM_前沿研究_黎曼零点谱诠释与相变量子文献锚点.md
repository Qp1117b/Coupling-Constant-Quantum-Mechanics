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

## 5. 文献引用信息

| 编号 | 完整引用 |
|:---:|:---|
| [V] | Voros, A. (2016). Simplification of the Keiper/Li approach to the Riemann Hypothesis. 8th DynQua Meeting, Grenoble. Based on preprint IPhT15/106 (June 2015), HAL cea-01166324. |
| [LM] | LeClair, A. & Mussardo, G. (2023). Riemann zeros as quantized energies of scattering with impurities. arXiv:2307.01254. |
| [L] | LeClair, A. (2024). Spectral Flow for the Riemann zeros. arXiv:2406.01828. |
| [SH] | Schumayer, D. & Hutchinson, D. A. W. (2011). Physics of the Riemann Hypothesis. arXiv:1101.3116 [math-ph]. |

PDF 文件存放于 `文献/` 目录。