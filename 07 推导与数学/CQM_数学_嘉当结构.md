# 离散哈密顿量与嘉当结构：从哈密顿量到群与场

**定位**：研究笔记——追踪 CQM 中哈密顿量、离散哈密顿量、能动张量、嘉当矩阵、根系、群与场之间的结构关系。

**关联文档**：`03-方法论/07-完整方程组.md`（方程总表）、`07-论文/01` §4–§5（嘉当方程与 SU(5) 几何定理）

---

## 一、哈密顿量

### 1.1 连续谱哈密顿量

因果集涌出的 ℍ² 谱几何给出二阶谱哈密顿量：

$$\hat{H}_\infty = c^2\left(-\partial_u^2 + \partial_u\right) = c^2\left[\hat{D}^2 + \frac{1}{4}\right], \quad \hat{D} = -i\left(\partial_u - \frac{1}{2}\right)$$

Hilbert 空间：$\mathcal{H}_\infty = L^2(\mathbb{R}, e^{-u}du)$，内积 $\langle f,g\rangle = \int f^*(u)g(u)e^{-u}du$。

$\hat{H}_\infty$ 在 Neumann 边界条件 $\partial_u\phi(0)=0$ 下自伴（Friedrichs 扩张），谱：

$$E_n = c^2\left(\frac{1}{4} + \gamma_n^2\right), \quad E_0 = \frac{c^2}{4}$$

其中 $\gamma_n$ 为黎曼 $\zeta$ 函数第 $n$ 个非平凡零点的虚部。

### 1.2 一阶生成元

一阶算符 $\hat{\mathcal{D}} = -i\,c\,e^u(\partial_u - 1/2)$ 描述再生产子的单向演化：

$$i\partial_\tau\Psi = \hat{\mathcal{D}}\Psi$$

在体区域（源外）经测度补偿 $\Psi = e^{u/2}\phi$ 退化为传输方程：

$$\partial_\tau\phi + c\,e^u\partial_u\phi = 0$$

**关键**：$\hat{H}_\infty$ 与 $\hat{\mathcal{D}}$ 独立构造，非平方关系——$\hat{\mathcal{D}}^2 = c^2 e^{2u}(-\partial_u^2 + 1/4) \neq \hat{H}_\infty$。两者通过 $\hat{\mu}$ 在事件点衔接。

---

## 二、离散哈密顿量

### 2.1 嘉当方程（Cayley 离散化）

将连续哈密顿量离散化。SU(5) 嘉当矩阵 $A_4$ 作为离散 Laplacian：

$$(I + \frac{icA_4}{2a})\psi^{n+1} = (I - \frac{icA_4}{2a})\psi^n$$

- $A_4 = \text{Cartan}(\text{SU}(5))$：4×4 三对角矩阵
- $a = \hbar/(m_p c)$：格点间距（质子康普顿波长）
- $\psi^n \in \mathbb{C}^4$：第 $n$ 步态矢量
- $\Delta\tau = a/c$：因果步进

连续极限：

$$\frac{A_4}{a^2} \longrightarrow -\partial_u^2 + \partial_u = \hat{H}_\infty/c^2$$

### 2.2 谱结构

$A_4$ 本征值 $\lambda_k = 2 - 2\cos(k\pi/5),\; k=1,\dots,4$：

| $k$ | $\lambda_k$ | 物理扇区 |
|:---:|:---:|:---|
| 1 | $2-2\cos(\pi/5) \approx 0.382$ | 紫外起始 |
| 2 | $2-2\cos(2\pi/5) \approx 1.382$ | 中间 |
| 3 | $2-2\cos(3\pi/5) \approx 3.618$ | 中间 |
| 4 | $2-2\cos(4\pi/5) \approx 3.618$ | **谱间隙** |

谱间隙 $E_0 = c^2/4$ 由有效边界势 $V_{\text{eff}}(0) = c^2/(\Delta u)^2 \cdot 1/\text{Tr}(A^{-1})$ 严格给出。

---

## 三、能动张量

### 3.1 从谱结构到能量密度

谱结构 $E_n$ 确定系统能级。QCD 能动张量主导引力源（~99% 质子质量来自 QCD 迹反常）：

$$\langle T_{\mu\nu}\rangle = \langle\psi|\hat{\mathcal{P}}_{\text{self}}^{(2)}\hat{T}_{\mu\nu}^{\text{QCD}}\hat{\mathcal{P}}_{\text{self}}^{(2)}|\psi\rangle$$

$\hat{\mathcal{P}}_{\text{self}}^{(2)}$ 为再生产筛选后的自耦投影。

### 3.2 GR 涌现

Einstein 方程从统计收敛 $N\to\infty$ 经 Jacobson 热力学 + Lovelock 唯一性涌出：

$$G_{\mu\nu} = 8\pi G_N\langle T_{\mu\nu}\rangle$$

$G_N$ 的谱公式：

$$G_N = \frac{I\cdot\lambda_c\cdot C^2\cdot E_1}{m_p^2}\cdot\exp\left(-\frac{2}{C}\right)\cdot(1+\kappa C),\quad \kappa = \frac{31+C}{30}$$

全部因子来自谱几何与群论，无一自由参数。

---

## 四、嘉当矩阵

### 4.1 $A_4$ 定义

SU(5) 的嘉当矩阵 $A_4$：

$$A_{ij} = \frac{2\langle\alpha_i,\alpha_j\rangle}{\langle\alpha_j,\alpha_j\rangle} = \begin{pmatrix}
2 & -1 & 0 & 0 \\
-1 & 2 & -1 & 0 \\
0 & -1 & 2 & -1 \\
0 & 0 & -1 & 2
\end{pmatrix}$$

其中 $\alpha_i$ 为 SU(5) 的 4 个单根。

### 4.2 本征结构

$A_4$ 本征值 $\lambda_k$ 对应 4-单纯形的离散 Laplacian 谱。$A_4$ 的逆矩阵 $A_4^{-1}$ 的迹：

$$\text{Tr}(A_4^{-1}) = 4$$

该值直接出现在谱间隙 $E_0 = c^2/4$ 的 Friedrichs 扩张推导中（$1/\text{Tr}(A_4^{-1}) = 1/4$）。
（与 Lean 定理 `cartanInvTrace_eq_four` 直接计算
$\text{Tr}(A_4^{-1}) = (4+6+6+4)/5 = 4$ 一致。）

### 4.3 与连续极限的对应

| 离散量 | 连续极限 |
|:---|:---|
| $\frac{1}{(\Delta u)^2}A_4$ | $-\partial_u^2 + \partial_u$ |
| $A_4$ 本征值 $\lambda_k$ | Sturm-Liouville 本征值 $E_n/c^2$ |
| 谱间隙 $\lambda_0$ | $E_0/c^2 = 1/4$ |
| 边界条件 $\psi_3 = e^{2a}\psi_0$ | $\partial_u\phi(0)=0$（Neumann） |

---

## 五、根系集合

### 5.1 SU(5) 根系

SU(5)（$A_4$ 型）的根系 $\Phi$：

- 秩：$r = 4$
- 单根：$\{\alpha_1,\alpha_2,\alpha_3,\alpha_4\}$，Dynkin 图为 $A_4$ 链
- 正根数：$|\Phi^+| = 10$
- 总根数：$|\Phi| = 20$
- $\text{dim}(\text{SU}(5)) = 24 = r + |\Phi|$

### 5.2 权空间分解

$A_4$ 的 Weyl 群 $W(A_4) \cong S_5$（5 阶置换群）作用在权空间上。基本支配权 $\{\omega_1,\omega_2,\omega_3,\omega_4\}$ 对应 SU(5) 的基本表示。

### 5.3 $A_4^{++}$ 与双曲几何

$A_4$ 嵌入 overextended Kac-Moody 代数 $A_4^{++}$。偶 Weyl 群 $W^+(A_4^{++}) \cong \text{PSL}_2^{(0)}(\mathcal{I})$ 作用在 Poincaré 半平面 $\mathbb{H}^2$ 上，基本域为镶嵌 $\{5,4\}$：

$$ds^2 = du^2 + e^{-2u}d\theta^2$$

这是因果集路径中 $\mathbb{H}^2$ 几何的直接代数来源——**嘉当矩阵 $A_4$ 通过 $A_4^{++}$ 嵌入直接涌出壳层度规**。

---

## 六、群嘉当结构

### 6.1 4-单纯形曲率算子

4-单纯形（5 顶点、10 边、10 三角面）的边-面关联矩阵 $E \in \{0,1\}^{10\times 10}$：

$$M = E^T E \in \mathbb{R}^{10 \times 10}, \quad \text{本征值 } \{9, 4, 1\}$$

重数 $\{1, 4, 5\}$，对应 $S_5$ 表示分解 $\mathbf{10} = \mathbf{1} \oplus \mathbf{4} \oplus \mathbf{5}$。

### 6.2 物理扇区对应

| 本征值 | 重数 | $S_5$ 表示 | 规范群 | p 进扇区 |
|:---:|:---:|:---:|:---:|:---:|
| 9 | 1 | $\mathbf{1}$ | SU(3) 色 | $p=2$ |
| 4 | 4 | $\mathbf{4}$ | SU(2) 弱 | $p=3$ |
| 1 | 5 | $\mathbf{5}$ | U(1) 电磁 | $p=5$ |

本征值比例 $9:4:1$ 直接决定三种规范耦合的相对强度——源自 4-单纯形的组合几何，非经验拟合。

### 6.3 SU(5) → SU(3)×SU(2)×U(1) 分解

SU(5) 嘉当矩阵 $A_4$ 的 Weyl 群 $S_5$ 同时是 4-单纯形的置换对称群。$S_5$ 表示论给出规范群分解的群论根源——SU(5) 不再是假设，而是 4-单纯形几何的定理。

---

## 七、从群到场

### 7.1 p 进扇区与规范场

每个规范群对应一个质数扇区：

| 质数 $p$ | 规范群 | 场内容 | Vladimirov 指数 |
|:---:|:---:|:---|:---:|
| 2 | SU(3) | 胶子（8） | $\alpha_2 = 1.545$ |
| 3 | SU(2) | $W^\pm, Z$（3） | $\alpha_3 = 0.443$ |
| 5 | U(1) | 光子（1） | $\alpha_5 = 0.826$ |

嘉当矩阵本征值 $9:4:1$ 映射到耦合强度 $\gamma_p = 1/p$——圈图展开的递归折损因子：强力 ($p=2$) 折损 50% 最强，电磁力 ($p=5$) 折损 20% 最弱。

### 7.2 场从群结构涌现

群结构确定场的代数性质：

- **SU(3) / $p=2$**：非 Abel，$f^{abc} \neq 0$ → 胶子自相互作用 → 色禁闭（壳层完全退相干）
- **SU(2) / $p=3$**：非 Abel，对称性破缺 → $W/Z$ 质量生成（壳层部分退相干）
- **U(1) / $p=5$**：Abel，$f^{abc} = 0$ → 光子长程传播（壳层最小退相干）

场的动力学内容（拉格朗日量、传播子、顶点）由 p 进结构在实数扇区的投影确定，非外加假设。

### 7.3 从哈密顿量到场：收束

完整收束链：

```
哈密顿量 Ĥ_∞（谱结构）
 → 离散化：嘉当方程（A₄ Cayley）
 → 嘉当矩阵 A₄ 本征结构 → 4-单纯形曲率算子 → S₅ 表示
 → SU(5) → SU(3)×SU(2)×U(1) 分解
 → p 进扇区 p=2,3,5 编码 → 规范场内容
 → 能动张量 T_μν → GR 涌现
```

该链与因果集路径（`07-论文/01` §3–§6）完全一致，且仅因果集路径能为每一步提供"从何而来"的本体论回答。经典路径（`08-经典路径.md`）提供数学骨架，但无法独立确立。
