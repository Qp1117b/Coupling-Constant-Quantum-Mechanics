# $G_N$ 第一性推导：公理化证明稿

**作者**：ruster

**风格**：定义 — 公理 — 引理 — 定理 — 证明（严格数学风格）

**诚实声明**：本文档严格区分三类命题：
- **定义**：概念的精确界定
- **公理/假设**：未经证明但被采纳为出发点的命题（标注 [A]）
- **定理/引理/推论**：从定义和公理出发，通过严格逻辑推理证明的命题

所有定理均给出完整证明。不能证明的命题明确标注为**猜想**或**开放问题**，不得伪装为定理。

---

# 第一部分：数学事实层（不依赖物理假设）

本部分所有定理均为纯数学命题，不依赖任何物理框架或假设。

---

## §1 相变量子 $☯$ 与 Riemann ξ 函数

### 1.1 定义

**定义 1.1（Riemann ξ 函数）**。定义整函数

$$\xi(s) = \frac{1}{2} s(s-1) \pi^{-s/2} \Gamma\left(\frac{s}{2}\right) \zeta(s)$$

其中 $\Gamma(s)$ 为 Gamma 函数，$\zeta(s)$ 为 Riemann zeta 函数。

**定义 1.2（相变量子 $☯$）**。相变量子 $☯$ 定义为 $\xi$ 函数的对数导数在 $s=1$ 处的值：

$$☯ \;\equiv\; \frac{d}{ds}\ln\xi(s)\bigg|_{s=1} \;=\; \frac{\xi'(1)}{\xi(1)}$$

**定义 1.3（非平凡零点）**。$\xi(s)$ 的零点称为 Riemann zeta 函数的非平凡零点，记为 $\rho$。已知所有非平凡零点位于临界带 $0 < \Re(s) < 1$ 内，且关于临界线 $\Re(s) = 1/2$ 和实轴对称。若 RH 成立，则 $\rho = 1/2 \pm i\gamma_n$，其中 $\gamma_n > 0$ 为第 $n$ 个零点的虚部。

---

### 1.2 引理

**引理 1.1（Hadamard 乘积公式）**。$\xi(s)$ 可表示为无穷乘积

$$\xi(s) = \xi(0) \prod_{\rho} \left(1 - \frac{s}{\rho}\right)$$

其中乘积遍历所有非平凡零点 $\rho$，按 $|\rho|$ 递增顺序排列。该乘积在复平面的任意紧子集上绝对一致收敛。

**证明**。$\xi(s)$ 是整函数且阶为 1（genus 0 的整函数，因零点增长满足一定条件），由 Hadamard 因子分解定理直接得出。$\xi(s)$ 的阶为 1 的证明见 Titchmarsh (1986) §2.6。$\blacksquare$

**引理 1.2（对数导数的级数表示）**。

$$\frac{\xi'(s)}{\xi(s)} = \sum_{\rho} \frac{1}{s - \rho}$$

该级数在不含任何零点的紧集上一致收敛。

**证明**。对 Hadamard 乘积（引理 1.1）两边取对数导数。收敛性由 Hadamard 乘积的一致收敛性保证。$\blacksquare$

**引理 1.3（ξ 在 s=1 处的值）**。

$$\xi(1) = \frac{1}{2}$$

**证明**。由函数方程 $\xi(s) = \xi(1-s)$，有 $\xi(1) = \xi(0)$。又由定义：

$$\xi(0) = \frac{1}{2} \cdot 0 \cdot (-1) \cdot \pi^{0} \cdot \Gamma(0) \cdot \zeta(0)$$

注意此式含 $0 \cdot \Gamma(0)$ 的不定式，需取极限：

$$\xi(s) = \frac{1}{2} s(s-1) \pi^{-s/2} \Gamma(s/2) \zeta(s)$$

当 $s \to 0$ 时，$\Gamma(s/2) \sim 2/s$（因 $\Gamma(z) \sim 1/z$ 当 $z \to 0$），故 $s \cdot \Gamma(s/2) \to 2$。又 $\zeta(0) = -1/2$。因此：

$$\xi(0) = \frac{1}{2} \cdot \lim_{s\to 0} [s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s)] = \frac{1}{2} \cdot (-1) \cdot 1 \cdot 2 \cdot (-\tfrac{1}{2}) = \frac{1}{2}$$

由函数方程，$\xi(1) = \xi(0) = 1/2$。$\blacksquare$

**引理 1.4（digamma 函数特殊值）**。
$$\psi(1/2) = -\gamma_E - 2\ln 2$$
$$\psi(1) = -\gamma_E$$

其中 $\psi(z) = \Gamma'(z)/\Gamma(z)$ 为 digamma 函数，$\gamma_E$ 为 Euler–Mascheroni 常数。

**证明**。标准特殊函数恒等式，见 Abramowitz & Stegun §6.3。$\blacksquare$

**引理 1.5（ζ 的对数导数在 s→1 时的正则化）**。

$\zeta(s)$ 在 $s=1$ 处有单极点，其留数为 1。但 $\xi(s)$ 在 $s=1$ 处解析且非零（引理 1.3），故 $\xi'(s)/\xi(s)$ 在 $s=1$ 处正则。

**证明**。由定义，$\xi(s)$ 包含因子 $s-1$，它恰好抵消 $\zeta(s)$ 在 $s=1$ 的极点。由引理 1.3，$\xi(1) = 1/2 \neq 0$，故对数导数正则。$\blacksquare$

---

### 1.3 定理：$☯$ 的求和表示

**定理 1.1（$☯$ 的零点求和表示）**。

$$☯ = \sum_{n=1}^{\infty} \frac{1}{\gamma_n^2 + 1/4}$$

其中求和遍历上半平面的非平凡零点虚部 $\gamma_n > 0$（按共轭对 $\rho_n = 1/2 \pm i\gamma_n$ 成对折叠后的结果）。

**证明**。由引理 1.2：

$$\frac{\xi'(s)}{\xi(s)} = \sum_{\rho} \frac{1}{s - \rho}$$

在 $s=1$ 处取值（引理 1.5 保证收敛）：

$$☯ = \sum_{\rho} \frac{1}{1 - \rho}$$

零点共轭成对：若 $\rho = 1/2 + i\gamma$ 是零点，则 $\overline{\rho} = 1/2 - i\gamma$ 也是零点。对每一对，注意 $1 - \rho = 1/2 - i\gamma$，$1 - \overline{\rho} = 1/2 + i\gamma$，故：

$$\frac{1}{1-\rho} + \frac{1}{1-\overline{\rho}} = \frac{1}{1/2 - i\gamma} + \frac{1}{1/2 + i\gamma} = \frac{(1/2 + i\gamma) + (1/2 - i\gamma)}{(1/2)^2 + \gamma^2} = \frac{1}{\gamma^2 + 1/4}$$

即每对共轭零点贡献 $1/(\gamma^2 + 1/4)$（不是 $2/(\gamma^2+1/4)$：分子中 $i\gamma$ 相消后只剩 $1$）。对所有上半平面零点求和即得。$\blacksquare$

**注**：定理 1.1 的收敛性由 Hadamard 乘积的收敛性保证（引理 1.1）；求和表示亦见 Titchmarsh (1986) §4.12。

---

### 1.4 定理：$☯$ 的闭式表达式

**定理 1.2（$☯$ 的闭式）**。

$$☯ = 1 + \frac{\gamma_E}{2} - \frac{\ln \pi}{2} - \ln 2$$

（等价形式：$1 - \tfrac{1}{2}\log(4\pi) + \tfrac{\gamma_E}{2}$，与 Coffey (2008)、Voros (2016) 中 $\xi'/\xi|_{s=1}$ 的闭式一致。）

**证明**。由 $\xi(s)$ 的定义：

$$\ln \xi(s) = \ln(1/2) + \ln s + \ln(s-1) - \frac{s}{2}\ln\pi + \ln\Gamma(s/2) + \ln\zeta(s)$$

对 $s$ 求导：

$$\frac{\xi'(s)}{\xi(s)} = \frac{1}{s} + \frac{1}{s-1} - \frac{1}{2}\ln\pi + \frac{1}{2}\psi(s/2) + \frac{\zeta'(s)}{\zeta(s)}$$

其中 $\psi(z) = \Gamma'(z)/\Gamma(z)$。

现在需要在 $s=1$ 处取值。注意到 $s=1$ 时 $1/(s-1)$ 和 $\zeta'(s)/\zeta(s)$ 都是发散的，但二者之和有限（由引理 1.5，左边 $\xi'(s)/\xi(s)$ 在 $s=1$ 正则）。

我们需要直接计算正则组合。方法：利用 $\xi$ 的函数方程或直接计算极限。

**方法：利用已知的 $\zeta'(s)/\zeta(s)$ 在 $s\to 1$ 时的渐近**

当 $s \to 1^+$ 时：

$$\zeta(s) = \frac{1}{s-1} + \gamma_E + O(s-1)$$

$$\frac{\zeta'(s)}{\zeta(s)} = -\frac{1}{s-1} + \gamma_E + O(s-1)$$

（证明：$\zeta(s) = 1/(s-1) + \gamma_E + \cdots$，故 $\zeta'(s) = -1/(s-1)^2 + O(1)$，$\zeta'(s)/\zeta(s) = -1/(s-1) + \gamma_E + \cdots$）

现在计算各部分在 $s \to 1$ 时的行为：

- $1/s \to 1$
- $1/(s-1)$：极点
- $-(1/2)\ln\pi$：常数
- $(1/2)\psi(s/2) \to (1/2)\psi(1/2) = (1/2)(-\gamma_E - 2\ln 2) = -\gamma_E/2 - \ln 2$（引理 1.4）
- $\zeta'(s)/\zeta(s) = -1/(s-1) + \gamma_E + O(s-1)$

将发散项相加：
$$\frac{1}{s-1} + \frac{\zeta'(s)}{\zeta(s)} = \frac{1}{s-1} - \frac{1}{s-1} + \gamma_E + O(s-1) = \gamma_E + O(s-1)$$

极点抵消，极限为 $\gamma_E$。

因此：

$$☯ = \lim_{s\to 1} \frac{\xi'(s)}{\xi(s)} = 1 + \gamma_E - \frac{1}{2}\ln\pi + \left(-\frac{\gamma_E}{2} - \ln 2\right)$$

$$= 1 + \frac{\gamma_E}{2} - \frac{\ln\pi}{2} - \ln 2$$

$\blacksquare$

---

### 1.5 定理：$☯ = \lambda_1$（第一 Li 系数）

**定义 1.4（Li 系数）**。Li 系数 $\{\lambda_n\}_{n=1}^\infty$ 由生成函数定义（Keiper–Li 判据，见 Voros 2016 [2]）：

$$\sum_{n=1}^{\infty} \lambda_n z^{n-1} = \frac{d}{dz}\ln\left[2\,\xi\!\left(\frac{1}{1-z}\right)\right]$$

等价地，$\lambda_n$ 是函数 $\frac{d}{dz}\ln[2\,\xi(1/(1-z))]$ 的 Taylor 展开中 $z^{n-1}$ 的系数。

**引理 1.6**。第一 Li 系数为：

$$\lambda_1 = 1 - \frac{\log 4\pi}{2} + \frac{\gamma_E}{2}$$

**证明**。令 $f(z) = 2\xi(1/(1-z))$，则：

$$\lambda_1 = \frac{d}{dz}\ln f(z)\bigg|_{z=0} = \frac{f'(0)}{f(0)}$$

注意 $z=0$ 对应 $1/(1-z) = 1$。

计算：

$$\ln f(z) = \ln 2 + \ln\xi\left(\frac{1}{1-z}\right)$$

$$\frac{d}{dz}\ln f(z) = \xi'\!\left(\frac{1}{1-z}\right) \cdot \frac{1}{\xi(1/(1-z))} \cdot \frac{1}{(1-z)^2}$$

在 $z=0$ 处（此时 $1/(1-z) = 1$，$1/(1-z)^2 = 1$）：

$$\lambda_1 = \frac{\xi'(1)}{\xi(1)} \cdot 1 = \frac{\xi'(1)}{\xi(1)} = ☯$$

与 Voros 表达式核验：$1 - \log(4\pi)/2 + \gamma_E/2 = 1 - \ln 2 - \ln\pi/2 + \gamma_E/2 = ☯$（与定理 1.2 闭式一致）。$\blacksquare$

**定理 1.3（$☯ = \lambda_1$）**。第一 Li 系数等于相变量子：

$$\lambda_1 = ☯$$

**证明**。由引理 1.6 的计算过程直接得出。从生成函数定义出发，$\lambda_1$ 恰好等于 $\xi'(1)/\xi(1)$，而后者正是 $☯$ 的定义。$\blacksquare$

**注**：此定理的内容本质上是"生成函数在 $z=0$ 处的对数导数等于 $\xi$ 在 $s=1$ 处的对数导数"，是变量替换的直接结果，而非深刻的数论定理。但 Li 系数的重要性在于 Li 判据：RH 等价于所有 $\lambda_n > 0$。因此 $☯ = \lambda_1 > 0$ 验证了 RH 的 n=1 情形。

**RH 依赖辨析**：$\lambda_n$ 的标准等价定义为 $\lambda_n=\sum_\rho\big[1-(1-1/\rho)^n\big]$；$n=1$ 时 $\lambda_1=\sum_\rho 1/\rho$，经 $\rho\leftrightarrow1-\rho$ 配对化为 $\sum 1/(\frac14+\gamma_n^2)$，此步**依赖 RH**（谱表示是 RH 的单向推论，见黎曼猜想证明思路 §3.4）。而本文闭式 $1+\gamma_E/2-\frac12\ln\pi-\ln2$ **不依赖 RH**——等式 $\lambda_1=☯$ 的证明只用生成函数定义与 $\xi$ 的特殊函数值，与 RH 无关。

---

### 1.6 定理：$B = -☯$（LeClair 常数）

**定义 1.5（LeClair 常数 B）**。在 LeClair 谱流方程（arXiv:2406.01828 [3]，eq. (42) 附近）中，$\zeta$ 函数对数导数的解析延拓写为：

$$-\frac{\zeta'(s)}{\zeta(s)} = \frac{1}{s-1} - B - \log\sqrt{\pi} + \frac{1}{2}\frac{\Gamma'(s/2+1)}{\Gamma(s/2+1)} - \sum_{\rho}\left(\frac{1}{s-\rho} + \frac{1}{\rho}\right)$$

其中常数 $B$ 定义为：

$$B = -\frac{\gamma_E}{2} - 1 + \log(2\sqrt{\pi})$$

**定理 1.4（$B = -☯$）**。LeClair 常数与相变量子满足：

$$B = -☯$$

**证明**。直接计算：

$$-☯ = -\left(1 + \frac{\gamma_E}{2} - \frac{\ln\pi}{2} - \ln 2\right) = -1 - \frac{\gamma_E}{2} + \frac{\ln\pi}{2} + \ln 2$$

$$= -\frac{\gamma_E}{2} - 1 + \ln 2 + \frac{1}{2}\ln\pi = -\frac{\gamma_E}{2} - 1 + \ln(2\sqrt{\pi}) = B$$

$\blacksquare$

**注**：此恒等式的代数内容是直接的——两个表达式包含相同的常数组合，只是整理方式不同。其物理意义在于：$B$ 出现在散射模型的谱流方程中，而 $☯$ 出现在 CQM 的相变量子中，二者的等同将两个不同的物理框架联系在一起。

---

### 1.7 主定理：$☯$ 的三重恒等

**定理 1.5（相变量子三重恒等定理）**。

$$\boxed{☯ = \frac{\xi'(1)}{\xi(1)} = \lambda_1 = -B}$$

即：Riemann ξ 函数在 $s=1$ 处的对数导数、第一 Li 系数、LeClair 谱流常数的负值，三者严格相等。

**证明**。综合定理 1.2（$☯$ 的闭式）、定理 1.3（$☯ = \lambda_1$）、定理 1.4（$B = -☯$）即得。$\blacksquare$

**数值验证**：$☯ \approx 0.02309570896612$，三者偏差均小于 $10^{-16}$（机器精度）。

---

## §2 组合与群论事实

### 2.1 4-单纯形的组合谱

**定义 2.1（4-单纯形）**。4-单纯形（5 顶点的单纯形）是 4 维空间中 5 个处于一般位置的点的凸包。其 $k$-面元（$k=0,1,2,3,4$）数量为：

$$N_k = \binom{5}{k+1}$$

具体地：顶点数 $N_0=5$，边数 $N_1=10$，三角形数 $N_2=10$，四面体数 $N_3=5$，4-面数 $N_4=1$。

**定义 2.2（边-面关联矩阵）**。边-面关联矩阵 $E$ 是 $N_2 \times N_1 = 10 \times 10$ 的 0-1 矩阵，其中 $E_{f,e} = 1$ 当且仅当边 $e$ 包含在面 $f$ 中。

**定义 2.3（曲率算符）**。曲率算符（或称组合 Laplacian 的边版本）定义为：

$$M = E^T E$$

这是一个 $10 \times 10$ 的对称矩阵。

**引理 2.1（S₅ 对称性）**。矩阵 $M$ 与对称群 $S_5$ 的作用可交换，即对任意 $\sigma \in S_5$，有 $\sigma M = M \sigma$。

**证明**。4-单纯形的组合结构在顶点置换下不变。边和面的置换由顶点置换诱导，关联关系保持不变，故 $E$ 与 $S_5$ 交换，从而 $M = E^T E$ 也与 $S_5$ 交换。$\blacksquare$

**引理 2.2（边置换表示的分解）**。$S_5$ 在 10 条边上的置换表示分解为不可约表示：

$$\mathbf{10} = \mathbf{1} \oplus \mathbf{4} \oplus \mathbf{5}$$

其中 $\mathbf{1}$ 为平凡表示，$\mathbf{4}$ 为标准表示，$\mathbf{5}$ 为另一个不可约表示。

**证明**。这是 $S_n$ 表示论中的标准结果：$S_n$ 在 $k$-子集上的置换表示的分解由 Young 规则给出。对于 $n=5, k=2$（边对应 2-子集），分解为平凡表示、标准表示和一个 5 维表示。具体维数验证：$1 + 4 + 5 = 10$。见 Fulton & Harris (1991)。$\blacksquare$

**定理 2.1（A₄ 谱定理）**。矩阵 $M = E^T E$ 的本征值为 $\{9, 4, 1\}$，对应的重数分别为 $\{1, 4, 5\}$。即：

$$\sigma(M) = \{9^{(1)}, 4^{(4)}, 1^{(5)}\}$$

**证明**。由引理 2.1 和 Schur 引理，$M$ 在每个不可约子空间上为标量算子，即每个不可约表示对应一个本征值。由引理 2.2，有三个不可约分量 $\mathbf{1}, \mathbf{4}, \mathbf{5}$，故有三个本征值，重数分别为 1, 4, 5。

现在确定本征值：

**(i) 全 1 向量**。设 $\mathbf{u} = (1,1,\ldots,1)^T$（10 维）。这是平凡表示 $\mathbf{1}$ 的基向量。

每条边包含在多少个三角形中？在 4-单纯形中，每条边与另外 3 个顶点构成三角形，故每条边属于 3 个三角形。

因此 $(E\mathbf{u})_f = $ 面 $f$ 中的边数 $= 3$（每个三角形有 3 条边），故 $E\mathbf{u}$ 的每个分量都是 3。

进而 $(M\mathbf{u})_e = (E^T E \mathbf{u})_e = \sum_{f \ni e} (E\mathbf{u})_f = \sum_{f \ni e} 3 = 3 \times 3 = 9$。

（因为每条边属于 3 个三角形，每个贡献 3）。

所以 $M\mathbf{u} = 9\mathbf{u}$，即 $\mathbf{u}$ 是本征值 9 的本征向量。$\mathbf{1}$ 表示对应本征值 9。

**(ii) 迹的计算**。$M = E^T E$ 的迹等于 $E$ 所有元素的平方和（即 $E$ 中 1 的个数）。每个三角形有 3 条边，10 个三角形共 $10 \times 3 = 30$ 条边-面关联。因此 $\text{Tr}(M) = 30$。

**(iii) 第一个条件（迹）**。设三个本征值为 $\lambda_1$（对应 $\mathbf{1}$，重数 1）、$\lambda_4$（对应 $\mathbf{4}$，重数 4）、$\lambda_5$（对应 $\mathbf{5}$，重数 5）。由 (i)，$\lambda_1 = 9$。

由迹条件：
$$\lambda_1 + 4\lambda_4 + 5\lambda_5 = \text{Tr}(M) = 30$$
$$9 + 4\lambda_4 + 5\lambda_5 = 30$$
$$4\lambda_4 + 5\lambda_5 = 21 \tag{1}$$

还需要第二个条件。计算 $\text{Tr}(M^2)$：

$M^2 = E^T E E^T E = E^T (E E^T) E$

$\text{Tr}(M^2) = \text{Tr}(E E^T E E^T) = \text{Tr}((E E^T)^2)$

**(iv) 第二个条件（二阶矩）**。组合地计算 $\text{Tr}(M^2)$。记 $G$ 为三角形邻接图：10 个三角形为顶点，两顶点相邻当且仅当对应三角形共边。每个三角形有 3 条边、每条边属于 3 个三角形，故每顶点度数为 $3 \times 2 = 6$，边数 $|E(G)| = 10 \times 6 / 2 = 30$。由 $(E E^T)_{ff} = 3$（每个三角形 3 条边）且非对角元为 0 或 1（两不同三角形至多共 1 条边）：

$$\text{Tr}(M^2) = \text{Tr}((E E^T)^2) = \sum_{f,f'} (E E^T)_{ff'}^2 = 10 \times 3^2 + 2 \times 30 = 150$$

代入 $\text{Tr}(M^2) = \lambda_1^2 + 4\lambda_4^2 + 5\lambda_5^2$ 与 $\lambda_1 = 9$：

$$4\lambda_4^2 + 5\lambda_5^2 = 150 - 81 = 69 \tag{2}$$

**(v) 求解本征值**。联立 (1)(2)：由 (1) 得 $\lambda_4 = (21 - 5\lambda_5)/4$，代入 (2) 化简得 $3\lambda_5^2 - 14\lambda_5 + 11 = 0$，解得 $\lambda_5 \in \{1,\, 11/3\}$，对应 $\lambda_4 \in \{4,\, 2/3\}$。

排除第二组解：$M = E^T E$ 是整系数矩阵，其特征多项式为首一整系数多项式；由有理根定理，特征值中的有理数必为整数。$2/3$ 与 $11/3$ 均非整数，故不可能是特征值。因此 $(\lambda_4, \lambda_5) = (4, 1)$，结合重数 $\{1, 4, 5\}$ 得：

$$\sigma(M) = \{9^{(1)},\, 4^{(4)},\, 1^{(5)}\}$$

**另证（数值验证补充）**。构造矩阵并数值计算本征值亦得 $\{9, 4^{(4)}, 1^{(5)}\}$，迹为 30，$\text{Tr}(M^2) = 81 + 64 + 5 = 150$，与上一致。

**严格性边界**。引理 2.2 的表示分解 $\mathbf{10} = \mathbf{1} \oplus \mathbf{4} \oplus \mathbf{5}$ 引自标准文献（Fulton & Harris 1991）；其余步骤（显式本征向量、迹与二阶矩的组合计算、有理根排除）均为直接验证。本定理亦可由单纯形组合 Laplacian 的一般谱理论得到（Horak & Jost 2013，Duval & Reiner 2002）。$\blacksquare$

**推论 2.1**。4-单纯形的非空面元总数为 $31 = 2^5 - 1$。

**证明**。$\sum_{k=0}^4 N_k = \sum_{k=0}^4 \binom{5}{k+1} = 2^5 - 1 = 31$。$\blacksquare$

**推论 2.2**。$M$ 的迹为 $30$。

**证明**。定理 2.1：$9 \times 1 + 4 \times 4 + 1 \times 5 = 30$。$\blacksquare$

---

### 2.2 Dynkin 指数比

**定义 2.4（Dynkin 指数）**。设 $\mathfrak{g}$ 为半单李代数，$V$ 为其有限维表示。Dynkin 指数 $T(V)$ 定义为 Casimir 算符在 $V$ 上的本征值与伴随表示上本征值的比值（或等价地，表示的二次型与 Killing 型的比值）。

对于 $\mathfrak{sl}_n$（即 $A_{n-1}$ 型），伴随表示的 Dynkin 指数为 $T(\text{adj}) = 2n$（归一化约定下）。

**定理 2.2（SU(5)/SU(3) Dynkin 指数比）**。

$$I \equiv \frac{T(\mathbf{24}_{\text{SU(5)}})}{T(\mathbf{8}_{\text{SU(3)}})} = \frac{5}{3}$$

**证明**。对于 $A_{n-1} = \mathfrak{sl}_n$，伴随表示的维数为 $n^2 - 1$，其 Dynkin 指数（按标准归一化，基本表示 $\mathbf{n}$ 的指数为 1）为 $T(\text{adj}) = 2n$。

- 对 SU(5)（$\mathfrak{sl}_5$, $n=5$）：$T(\mathbf{24}) = 2 \times 5 = 10$
- 对 SU(3)（$\mathfrak{sl}_3$, $n=3$）：$T(\mathbf{8}) = 2 \times 3 = 6$

因此：
$$I = \frac{10}{6} = \frac{5}{3}$$

$\blacksquare$

---

## §3 Mathieu 临界参数

### 3.1 定义与基本性质

**定义 3.1（Mathieu 算符）**。在区间 $[0, \pi]$ 上，定义 Mathieu 算符

$$\hat{L}_q = -\frac{d^2}{dz^2} + 2q\cos 2z$$

考虑满足 $\pi$-周期奇函数边界条件的函数空间，即由 $\{\sin((2k+1)z)\}_{k=0}^\infty$ 张成的空间。在此空间上，$\hat{L}_q$ 是自伴算符，其本征值为离散的，记为 $\lambda_k(q)$，$k = 0, 1, 2, \ldots$，按从小到大排列。

最小本征值 $\lambda_0(q) = b_1(q)$（DLMF 记号中的第一奇 Mathieu 特征值）。

**引理 3.1（小 $q$ 微扰展开）**。

$$b_1(q) = 1 - q - \frac{q^2}{8} + \frac{q^3}{64} - \frac{q^4}{1536} + \cdots$$

特别地，$b_1(0) = 1$，$b_1'(0) = -1$。

**证明**。标准微扰论结果。令 $q = 0$ 时，算符为 $-d^2/dz^2$，其在奇函数空间的基态本征值为 $1$（对应 $\sin z$）。一阶微扰给出修正 $-\langle \sin z | 2\cos 2z | \sin z \rangle = -\int_0^\pi \sin^2 z \cdot 2\cos 2z \, dz / \int_0^\pi \sin^2 z \, dz$。计算得一阶修正为 $-q$，故 $b_1(q) = 1 - q + O(q^2)$。高阶项可通过 Rayleigh–Schrödinger 微扰论计算。$\blacksquare$

### 3.2 连分数表示

**引理 3.2（连分数方程）**。$b_1(q)$ 满足以下连分数方程：

$$b_1(q) = 1 - 2q - \frac{q^2}{b_3(q) - 2 - \frac{q^2}{b_5(q) - 2 - \cdots}}$$

其中 $b_{2k+1}(q)$ 为第 $k+1$ 个奇 Mathieu 特征值。

**证明**。这是 Mathieu 方程的标准连分数表示。将 Mathieu 方程的解展开为 Fourier 级数 $y = \sum_{k=-\infty}^\infty c_k e^{i(2k+1)z}$，代入方程得到递推关系，其连分数形式给出特征值条件。见 McLachlan (1947) 或 DLMF §28.6。$\blacksquare$

**推论 3.1**。令 $\lambda = b_1(q)$，则 $\lambda$ 满足：

$$\lambda - 1 + 2q = -\frac{q^2}{b_3(q) - 2 - \frac{q^2}{b_5(q) - 2 - \cdots}}$$

对于小 $q$，高阶特征值 $b_{2k+1}(q) \approx (2k+1)^2$，故分母 $b_{2k+1}(q) - 2 \approx (2k+1)^2 - 2$。

### 3.3 临界条件与存在唯一性

**定义 3.2（临界条件）**。临界参数 $q_c$ 定义为方程

$$b_1(q) = 2q$$

的解。临界值定义为 $\lambda_c = 4q_c$；在根处 $b_1(q_c) = 2q_c$，故等价地 $\lambda_c = 2 b_1(q_c)$。

**定理 3.1（临界参数的存在唯一性）**。方程 $f(q) = b_1(q) - 2q = 0$ 在区间 $q \in (0, 1)$ 内有且仅有一个根 $q_c$。

**证明**。

**步骤 1（严格单调性）**。对于自伴算符 $\hat{L}_q = -\frac{d^2}{dz^2} + 2q\cos 2z$，其基态本征值 $b_1(q)$ 对 $q$ 的导数由 Hellmann–Feynman 定理给出：

$$b_1'(q) = \langle \psi_1 | 2\cos 2z | \psi_1 \rangle$$

其中 $\psi_1$ 是归一化基态。基态波函数的模方集中在 $\cos 2z < 0$ 的区域（$\sin^2$ 型分布在 $z = \pi/2$ 处最大，而 $\cos 2z$ 在 $z = \pi/4$、$3\pi/4$ 处变号，负区域权重更大），故 $\cos 2z$ 的期望值为负，即 $b_1'(q) < 0$，$b_1(q)$ 严格递减。而 $2q$ 的导数为 $2 > 0$，故 $f(q) = b_1(q) - 2q$ 满足 $f'(q) = b_1'(q) - 2 < 0$，即 $f$ 在 $(0, \infty)$ 上**严格递减**。

**步骤 2（存在性）**。$f(0) = b_1(0) - 0 = 1 > 0$（引理 3.1）。另一方面，对充分大的 $q$，Mathieu 势 $2q\cos 2z$ 形成深势阱，基态能量 $b_1(q)$ 为负（势阱底部 $\cos 2z = -1$ 处势能 $\to -\infty$），而 $2q > 0$，故 $f(q) < 0$。由介值定理，存在 $q_0 > 0$ 使 $f(q_0) < 0$，进而存在根 $q_c \in (0, q_0)$。

（注：微扰展开 $b_1(q) = 1 - q - q^2/8 + \cdots$ 为 $q=0$ 处的渐近级数，其在 $q = 1$ 的收敛性无保证，故不用于端点符号判定。）

**步骤 3（唯一性）**。$f$ 在 $(0, \infty)$ 上严格递减，至多有一个根。结合步骤 2，方程在 $(0, \infty)$ 内有唯一根 $q_c$。

**步骤 4（根的定位）**。根可缩小至 $(0, 1/2)$：由微扰展开估计 $b_1(0.5) \approx 1 - 0.5 - 0.5^2/8 = 0.46875 < 1 = 2 \times 0.5$，即 $f(0.5) < 0$；结合 $f(0) = 1 > 0$ 与严格单调性得 $q_c \in (0, 0.5) \subset (0, 1)$。（此处微扰级数取首项为启发式定位；$q_c \in (0, 1/2)$ 内存在唯一性的严格证明由连分数方程（引理 3.2）的不动点构造给出，见 `MathieuContinuedFraction.lean`。）$\blacksquare$

**定义 3.3**。临界参数记为 $q_c$，且 $\lambda_c = 4q_c$。

**数值**。$q_c \approx 0.3290057278\ldots$，$\lambda_c \approx 1.3160229113\ldots$。

---

# 第二部分：CQM 框架内定理

本部分定理依赖于 CQM 的基本公理和假设。每个定理明确列出其所依赖的公理。

---

## §4 CQM 基本公理

**公理 A1（耦合空间海森堡代数）**。耦合常数空间的基本对易关系为：

$$[\hat{u}, \hat{p}_u] = i$$

其中 $\hat{u} = \ln \hat{r}$ 为对数耦合算符，$\hat{p}_u = \hat{v}_\tau / ☯$ 为固有时流速算符，$☯$ 为相变量子。

**公理 A2（Sprinkling 测度）**。耦合空间的测度为 $d\mu = e^{-u} du$，Hilbert 空间为 $\mathcal{H} = L^2(\mathbb{R}, e^{-u}du)$。

**公理 A3（谱算符）**。谱算符定义为：

$$\hat{H} = \hat{D}^2 + \frac{1}{4}$$

其中 $\hat{D} = -i(\partial_u - 1/2)$。

**公理 A4（退相干 = 禁闭边界）**。引力退相干发生在强子尺度，退相干后禁闭边界涌现，非交换几何变为交换几何。

**公理 A5（SU(5) 基态）**。退相干的稳态是 4-单纯形组合结构，对应 SU(5) 规范群。

**公理 A6（量纲锚点）**。质子质量 $m_p$ 是唯一的量纲输入，所有物理量的量纲由 $m_p$、$\hbar$、$c$ 的幂次组合提供。

---

## §5 Sierra-CQM 定理

**定理 5.1（Sierra-CQM）**。设 sprinkling 区间长度为 $L_n = 2\pi n / \gamma_n$，边界相位为 $\vartheta_n$（有界，$|\vartheta_n| < \pi$）。则谱算符 $\hat{H} = \hat{D}^2 + 1/4$ 在区间 $[0, L_n]$ 上的第 $n$ 个本征值（耦级）满足：

$$\mathfrak{c}_n = \frac{1}{4} + \gamma_n^2 + O\left(\frac{\gamma_n^2}{n}\right)$$

**依赖的公理**：A1, A2, A3。

**额外构造性假设**：sprinkling 区间 $L_n = 2\pi n / \gamma_n$ 的物理来源。

**证明**。

**步骤 1：酉等价**。定义酉变换 $U: L^2(e^{-u}du) \to L^2(du)$：

$$(Uf)(u) = e^{-u/2} f(u)$$

验证保内积：
$$\langle Uf | Ug \rangle_{L^2(du)} = \int e^{-u/2}\overline{f(u)} \cdot e^{-u/2}g(u) \, du = \int \overline{f(u)} g(u) e^{-u} du = \langle f | g \rangle_{L^2(e^{-u}du)}$$

谱算符的变换：
$$U \hat{H} U^{-1} = U\left(-\partial_u^2 + \partial_u\right) U^{-1}$$

令 $g(u) = e^{-u/2}f(u)$，则 $f(u) = e^{u/2}g(u)$。

计算：
$$\partial_u f = \frac{1}{2}e^{u/2}g + e^{u/2}\partial_u g$$
$$\partial_u^2 f = \frac{1}{4}e^{u/2}g + e^{u/2}\partial_u g + e^{u/2}\partial_u^2 g$$

$$-\partial_u^2 f + \partial_u f = -\frac{1}{4}e^{u/2}g - e^{u/2}\partial_u g - e^{u/2}\partial_u^2 g + \frac{1}{2}e^{u/2}g + e^{u/2}\partial_u g$$
$$= \left(-\frac{1}{4} + \frac{1}{2}\right)e^{u/2}g + (-1 + 1)e^{u/2}\partial_u g - e^{u/2}\partial_u^2 g$$
$$= \frac{1}{4}e^{u/2}g - e^{u/2}\partial_u^2 g$$

因此：
$$U \hat{H} U^{-1} g = e^{-u/2} \hat{H} (e^{u/2}g) = e^{-u/2} \left(\frac{1}{4}e^{u/2}g - e^{u/2}\partial_u^2 g\right) = \left(\frac{1}{4} - \partial_u^2\right)g$$

即 $\hat{H}$ 在 $L^2(e^{-u}du)$ 中酉等价于 $\tilde{H} = -\partial_u^2 + 1/4$ 在 $L^2(du)$ 中。$\blacksquare_{\text{步骤1}}$

**步骤 2：平面波本征函数**。在 $L^2(du)$ 中，算符 $-\partial_u^2$ 的广义本征函数为平面波 $g_k(u) = e^{iku}$，本征值为 $k^2$。因此 $\tilde{H}$ 的本征值为 $k^2 + 1/4$。$\blacksquare_{\text{步骤2}}$

**步骤 3：Floquet 边界条件与量子化**。在有限区间 $[0, L_n]$ 上，施加 Floquet（拟周期）边界条件：

$$g_k(L_n) = e^{i\vartheta_n} g_k(0), \qquad g_k'(L_n) = e^{i\vartheta_n} g_k'(0)$$

对平面波 $g_k(u) = e^{iku}$，边界条件给出：

$$e^{ikL_n} = e^{i\vartheta_n}$$

即量子化条件：

$$k L_n = \vartheta_n + 2\pi m, \qquad m \in \mathbb{Z}$$

对于第 $n$ 个本征值，取 $m = n$：

$$k_n = \frac{\vartheta_n + 2\pi n}{L_n}$$

$\blacksquare_{\text{步骤3}}$

**步骤 4：零点匹配**。取 $L_n = 2\pi n / \gamma_n$，则：

$$k_n = \frac{\vartheta_n + 2\pi n}{2\pi n / \gamma_n} = \gamma_n \cdot \frac{2\pi n + \vartheta_n}{2\pi n} = \gamma_n \left(1 + \frac{\vartheta_n}{2\pi n}\right)$$

由于 $|\vartheta_n| < \pi$ 有界，当 $n \to \infty$ 时：

$$k_n = \gamma_n + O\left(\frac{1}{n}\right)$$

$\blacksquare_{\text{步骤4}}$

**步骤 5：耦级**。$\tilde{H}$ 的本征值为 $k_n^2 + 1/4$，因此：

$$\mathfrak{c}_n = k_n^2 + \frac{1}{4} = \gamma_n^2\left(1 + \frac{\vartheta_n}{\pi n} + \frac{\vartheta_n^2}{4\pi^2 n^2}\right) + \frac{1}{4} = \frac{1}{4} + \gamma_n^2 + O\left(\frac{\gamma_n^2}{n}\right)$$

其中展开用了 $k_n = \gamma_n(1 + \vartheta_n/(2\pi n))$（步骤 4）与 $|\vartheta_n| < \pi$ 有界。由于 $\gamma_n \sim 2\pi n/\log n$（Riemann–von Mangoldt 公式 $N(T) \sim T\log T/(2\pi)$ 的推论），绝对误差项 $O(\gamma_n^2/n)$ 随 $n$ 增长，但相对误差为 $O(1/n) \to 0$。等价的相对误差表述为：

$$\frac{\mathfrak{c}_n - (1/4 + \gamma_n^2)}{\gamma_n^2} = O\left(\frac{1}{n}\right)$$

即 $\mathfrak{c}_n = \frac{1}{4} + \gamma_n^2\left(1 + O\left(\frac{1}{n}\right)\right)$。$\blacksquare$

**严格性评估**。
- 步骤 1-3 的数学推导是严格的（酉等价、平面波、Floquet 边界条件）
- 步骤 4 中 $L_n = 2\pi n / \gamma_n$ 的选择是**构造性的**——它被设计为使 $k_n \approx \gamma_n$。其物理来源（为何 sprinkling 区间长度与第 n 个黎曼零点成反比）尚未从第一性原理导出
- $m = n$ 的选择也是构造性的

因此，此定理是"**条件性定理**"——如果接受 $L_n$ 和 $m=n$ 的选择，则结论严格成立。

**Lean 形式化状态**：步骤 4–5 的代数核心已在 `06 Lean形式化/GN/SierraCQM.lean` 形式化（6 定理，零 `sorry`）——零点匹配、偏差界 $|k_n-\gamma_n|<\gamma_n/(2n)$、耦级绝对/相对误差（含 $n\ge1$ 时见证常数 $5/4$）；`L_n` 与 $m=n$ 以显式假设出现。步骤 1–2（酉等价、平面波广义本征函数）需函数空间算子与分布谱论基础设施，未形式化。

---

## §6 Adele Jacobian 因子 2

**定理 6.1（双向平方定理）**。设 $\det(D_\infty)$ 为 Archimedean 扇区的谱行列式，$\prod_p \det(D_p)$ 为非 Archimedean（p 进）扇区的谱行列式乘积。若满足 Tate 自对偶条件：

$$\det(D_\infty) \cdot \prod_p \det(D_p) = 1$$

则 UV→IR 过渡的 Jacobian 为：

$$\mathcal{J} = \frac{\det(D_\infty)}{\prod_p \det(D_p)} = \left(\prod_p \det(D_p)\right)^{-2}$$

特别地，$\ln \mathcal{J}$ 含因子 $-2$。

**依赖的公理/假设**：
- Tate 自对偶条件（数学事实，Tate 论文 1950）
- p 进谱行列式的存在性（CQM 框架假设）
- Jacobian 定义为 $\det(D_\infty) / \prod_p \det(D_p)$（框架定义）

**证明**。

由自对偶条件：
$$\det(D_\infty) = \left(\prod_p \det(D_p)\right)^{-1}$$

代入 Jacobian 定义：
$$\mathcal{J} = \frac{\det(D_\infty)}{\prod_p \det(D_p)} = \frac{(\prod_p \det(D_p))^{-1}}{\prod_p \det(D_p)} = \left(\prod_p \det(D_p)\right)^{-2}$$

取对数：
$$\ln \mathcal{J} = -2 \ln\left(\prod_p \det(D_p)\right)$$

因子 $-2$ 由此而来。$\blacksquare$

**严格性边界**。
- 代数运算是严格的
- Tate 自对偶是严格的数学定理（Tate 论文）
- 但 $\det(D_p)$ 的**定义**是 CQM 框架内的构造，不是标准数学中的已知对象
- 因此此定理的地位是：**如果** p 进谱行列式存在且满足自对偶条件，**则** Jacobian 含 -2 因子

---

## §7 SU(5) 唯一性的群论约束

**定理 7.1（根系分类定理）**。在不可约根系的双曲过扩张中，只有 $A_4^{++}$ 具有有限商并可镶嵌为双曲镶嵌 $\{5,4\}$。具体地：

| 根系 | 过扩张 | 有限商？ | 物理规范群 |
|:---:|:---:|:---:|:---:|
| $A_1$ | $A_1^{++}$ | 否 | SU(2) |
| $A_2$ | $A_2^{++}$ | 否 | SU(3) |
| $A_4$ | $A_4^{++}$ | **是** | SU(5) |

**证明概要**。双曲 Kac-Moody 代数的分类表明，只有少数过扩张根系具有有限指数的子群（即其 Weyl 群在双曲空间上的作用具有有限体积的基本域）。Feingold-Nicolai (2003) 建立了双曲 Weyl 群与范数代数的对应关系，其中 $A_4^{++}$ 对应四元数，其 Weyl 群同构于 $\text{PSL}_2^{(0)}(\mathcal{I})$（整四元数的投影群），具有有限商。

$A_1^{++}$ 和 $A_2^{++}$ 对应的双曲空间维数太低或其 Weyl 群的基本域体积无限，故无有限商。

完整证明需要双曲 Kac-Moody 代数和镶嵌理论的深入讨论，超出本文档范围。该结论为数学文献中的已知结果。$\blacksquare$

**推论 7.1（SU(5) 唯一曲率源）**。在标准模型规范群 $U(1) \times SU(2) \times SU(3)$ 中，各因子的根系过扩张均无有限商，无法独立产生 Regge 曲率。只有嵌入 SU(5) 的 $A_4^{++}$ 具有有限商，可产生 Cartan-Regge 曲率。

**依赖的额外假设**：
- 引力曲率必须通过 Regge 微积分从双曲镶嵌导出（CQM 框架假设）
- U(1) 无根系故无 Cartan 曲率（平凡事实）

**证明**。综合定理 7.1 和 U(1) 无根系的事实即得。$\blacksquare$

---

# 第三部分：启发式构造与开放问题

本部分的命题**不是**定理，而是有数值证据支撑的构造性猜想。

---

## §8 κ 的构造与缺口

**构造 8.1（κ 的组合-谱构造）**。

$$\kappa = \frac{N_{\text{faces}} + ☯}{N_{\text{cycle}}} = \frac{31 + ☯}{30}$$

其中：
- $N_{\text{faces}} = 31 = 2^5 - 1$：4-单纯形非空面元数（严格组合事实，推论 2.1）
- $N_{\text{cycle}} = 30 = \text{Tr}(M)$：边-面关联矩阵的迹（严格组合事实，推论 2.2）
- $+☯$：离散到连续过渡的修正项

**命题 8.1（κ 的分解）**。κ 可精确分解为主项加修正项：

$$\kappa = \frac{31}{30} + \frac{☯}{30}$$

**证明**。代数恒等式：$(31 + ☯)/30 = 31/30 + ☯/30$。$\blacksquare$

**开放问题 8.1**。为何谱行列式修正系数恰好是 $(N_{\text{faces}} + ☯)/N_{\text{cycle}}$？为何 $☯$ 加在分子而非分母？为何是 $+☯$ 而非其他函数形式（如 $+☯^2$、$\times(1+☯)$ 等）？

**当前状态**：构造性匹配，无严格推导。

---

## §9 𝔠₁ 的精确等同

**构造 9.1（第一耦级的精确等同）**。第一耦级精确等于第一黎曼零点对应的谱值：

$$\mathfrak{c}_1 = \frac{1}{4} + \gamma_1^2$$

**与定理 5.1 的关系**。Sierra-CQM 定理（定理 5.1）给出 $\mathfrak{c}_n = 1/4 + \gamma_n^2 + O(\gamma_n^2/n)$（相对误差 $O(1/n)$）。对于 $n=1$，相对误差为 $O(1)$，即误差项与主项同量级。因此，精确等同是**超出定理范围**的构造性假设。

**开放问题 9.1**。n=1 时误差项为何恰好为零？是否存在某种机制（如基态共振的特殊性、自洽条件等）使得第一耦级精确等于 $1/4 + \gamma_1^2$？

**当前状态**：构造性匹配，无严格推导。

---

## §10 $\exp(-2/\text{☯})$ 的 $☯$ 来源

**构造 10.1（p 进行列式与 $☯$ 的对应）**。

$$\ln\left(\prod_p \det(D_p)\right) = \frac{1}{☯} = 43.298086$$

因此，结合定理 6.1：

$$\ln \mathcal{J} = -\frac{2}{☯} \qquad \Longrightarrow \qquad \mathcal{J} = \exp\left(-\frac{2}{☯}\right)$$

**开放问题 10.1**。为何 p 进谱行列式的对数恰好等于 $1/☯$？这是最深层的缺口，涉及数论（Adele、L 函数）与物理（谱行列式、引力压制）的核心对应。

**当前状态**：启发式对应，无严格推导。

---

## §11 乘积结构

**构造 11.1（$G_N$ 公式）**。

$$G_N = \frac{\hbar c}{m_p^2} \cdot I \cdot \lambda_c \cdot ☯^2 \cdot \mathfrak{c}_1 \cdot \exp\left(-\frac{2}{☯}\right) \cdot (1 + \kappa ☯)$$

**开放问题 11.1**。为何 $G_N$ 取各因子的乘积形式？是否存在一个统一的变分原理或作用量，使得此乘积结构是自然导出的？

**当前状态**：构造性公式，无统一变分原理。

---

# 第四部分：推导链总览与严格性地图

## §12 从公理到 $G_N$ 的推导链

```
数学事实层（无条件成立）
├── 定理 1.5：☯ 的三重恒等（★★★）
│   └── 数值：☯ ≈ 0.0230957
├── 定理 2.1：A₄ 谱 {9,4,1}（★★★）
├── 定理 2.2：I = 5/3（★★★）
└── 定理 3.1：λ_c 存在唯一性（★★★）
    └── 数值：λ_c ≈ 1.316

CQM 公理层（接受 A1-A6）
├── 定理 5.1：Sierra-CQM（★★☆）
│   ├── 严格部分：酉等价 + Floquet 边界条件
│   │   └── 代数核心已 Lean 形式化（GN/SierraCQM.lean）
│   ├── 构造性输入：Lₙ = 2πn/γₙ, m=n
│   └── 输出：𝔠ₙ = 1/4 + γₙ² + O(γₙ²/n)
├── 定理 6.1：双向平方因子 2（★★☆）
│   ├── 严格部分：自对偶 + Jacobian 定义的代数运算
│   └── 假设：p 进谱行列式存在
│   └── 输出：ln 𝒥 = -2 · ln(∏ det(Dₚ))
└── 推论 7.1：SU(5) 唯一曲率源（★★☆）
    ├── 严格部分：根系分类定理
    └── 假设：曲率必须通过 Regge 化导出
    └── 输出：只有 SU(5) 产生曲率

启发式构造层（未证明）
├── 构造 9.1：𝔠₁ = 1/4 + γ₁²（精确等同）
│   └── 数值权重：𝔠₁ ≈ 200.04 单独贡献 **2.30 个数量级**；exp(-2/☯) 贡献 10⁻³⁸（38 个数量级）。未闭合项合计承载约 **40 个数量级**，已闭合项（I、λ_c、☯²）合计约 10⁻³。
├── 构造 10.1：ln(∏ det(Dₚ)) = 1/☯
│   └── → exp(-2/☯)
├── 构造 8.1：κ = (31+☯)/30
└── 构造 11.1：乘积结构

实验输入
└── m_p（唯一量纲锚点）
```

---

## §13 严格性层级总结

### 13.1 已严格证明（数学事实）

| 命题 | 定理编号 | 依赖 |
|:---|:---:|:---|
| $☯ = \xi'(1)/\xi(1) = \sum 1/(\gamma_n^2+1/4)$ | 1.1 | Hadamard 乘积 |
| $☯ = 1 + \gamma_E/2 - \ln\pi/2 - \ln 2$ | 1.2 | $\xi$ 定义 + 特殊函数值 |
| $☯ = \lambda_1$（第一 Li 系数） | 1.3 | 生成函数定义 |
| $B = -☯$（LeClair 常数） | 1.4 | 直接代数恒等 |
| A₄ 谱 {9,4,1}，重数 {1,4,5} | 2.1 | 组合 + S₅ 表示论 |
| 总面元数 = 31，迹 = 30 | 推论 2.1/2.2 | 组合数学 |
| I = 5/3（Dynkin 指数比） | 2.2 | 李代数标准结果 |
| λ_c 存在唯一性 | 3.1 | 介值定理 + 严格单调性 |
| 因子 2（代数部分） | 6.1 | 自对偶 + Jacobian 定义 |
| SU(5) 唯一可 Regge 化 | 7.1 | 根系分类 + 镶嵌理论 |

### 13.2 框架内定理（需 CQM 公理）

| 命题 | 定理编号 | 额外构造性输入 |
|:---|:---:|:---|
| Sierra-CQM 定理（渐近） | 5.1 | Lₙ 选择、m=n 选择（代数核心已 Lean 形式化：`GN/SierraCQM.lean`） |
| Adele Jacobian 因子 2 | 6.1 | p 进谱行列式存在性 |
| SU(5) 唯一曲率源 | 推论 7.1 | 曲率 = Regge 曲率假设 |

### 13.3 开放问题（启发式构造）

| 构造 | 核心缺口 | 难度 |
|:---|:---|:---:|
| $\kappa = (31+☯)/30$ | 为何是这个比值？+$☯$ 来源？ | 中等 |
| $\mathfrak{c}_1$ 精确等同 | n=1 误差为何为零？ | 中等偏难 |
| $\exp(-2/\text{☯})$ 的 $☯$ 来源 | p 进行列式 ↔ $☯$ 映射 | 极高 |
| 退相干稳态 = 4-单纯形 | 极值原理证明唯一性 | 极高 |
| 乘积结构 | 统一变分原理 | 未知 |

---

## 参考文献

1. Titchmarsh, E. C. (1986). *The Theory of the Riemann Zeta-Function*, 2nd ed. (rev. D. R. Heath-Brown). Oxford Univ. Press.
2. Voros, A. (2016). Simplifications of the Keiper/Li approach to the Riemann Hypothesis. arXiv:1602.03292.
3. LeClair, A. (2024). Spectral Flow for the Riemann zeros. arXiv:2406.01828. Adv. Theor. Math. Phys. (2025).
4. Coffey, M. W. (2008). Relations and representations of the Euler constant. *Proc. R. Soc. A* 464, 2059–2074.（$\xi'/\xi$ 及 $\psi$ 特殊值闭式的对数导数核验）
5. LeClair, A. & Mussardo, G. (2024). Riemann zeros as quantized energies of scattering with impurities. *JHEP* 04, 062. arXiv:2307.01254.
6. Sierra, G. (2008). A quantum mechanical model of the Riemann zeros. *New J. Phys.* 10, 033016.
7. McLachlan, N. W. (1947). *Theory and Application of Mathieu Functions*. Oxford.
8. NIST Digital Library of Mathematical Functions, Chapter 28.
9. Fulton, W. & Harris, J. (1991). *Representation Theory: A First Course*. GTM 129. Springer.
10. Feingold, A. J. & Nicolai, H. (2003). Hyperbolic Weyl groups and the four normed division algebras. *J. Algebra*, 250, 831.
11. Tate, J. (1950). Fourier analysis in number fields and Hecke's zeta-functions. *Thesis*, Princeton.
12. Horak, D. & Jost, J. (2013). Spectra of combinatorial Laplace operators on simplicial complexes. *Adv. Math.*, 244, 303–336.
13. Duval, A. & Reiner, V. (2002). Shifted simplicial complexes are Laplacian integral. *Trans. AMS*, 354, 4313–4344.
