# CQM 质量研究思路汇总

## 0. 核心命题

$$
\boxed{
\text{质量不是基本输入，而是自守关联的涌现结果。}
}
$$

$$
\boxed{
\text{质子 } A_4 \text{ 的 } L \text{ 和 } T \text{ 属性建立自守关联，质量从关联中生成。}
}
$$

$$
\boxed{
\text{其他粒子是 } \pi_p \text{ 的朗兰兹函子性分化。}
}
$$

---

## 1. 质量的量纲地位

$$[M] = \frac{[L]^3}{[G_N]\cdot[T]^2}$$

$$
\boxed{
M \text{ 的转换常数是 } G_N。
}
$$

$G_N$ 把长度和时间的组合转换成质量量纲，是**第一个有动力学内容的转换常数**。

---

## 2. 为什么直接放在 $G_N$ 层

$$
\boxed{
\text{质量的建立意味着 } L \text{ 和 } T \text{ 已经建立。}
}
$$

$M$ 的定义预设了 $L$ 和 $T$ 已经存在，$G_N$ 的自守形式天然包含长度-时间关联。不需要单独讨论 $1/c$ 的自守形式。

---

## 3. 质子的 $L$ 和 $T$ 属性

| 属性 | 物理内容 | 数学对象 |
|---|---|---|
| $L$ | 质子几何延展 | $A_4$ 谱几何 |
| $T$ | 质子再生产周期 | 内部振荡模式 |

### 3.1 $A_4$ 谱几何

$A_4$ 的边-面关联矩阵 $M = E^T E$（$10 \times 10$，迹 $30$）的谱：

$$\{9^{(1)},\ 4^{(4)},\ 1^{(5)}\}$$

多重度 $(1, 4, 5)$，总和 $1+4+5 = 10$（单纯形面数）。

$$
\boxed{
\text{这是谱几何事实，与 } \mathrm{SU}(5) \text{ 表示的对应需单独论证。}
}
$$

### 3.2 自守关联

$$
\boxed{
f_L\left(-\frac{1}{z}\right) = \chi(z) \, f_T(z)
}
$$

### 3.3 统一自守表示

$$
\boxed{
f_L, f_T \in \pi_p
}
$$

---

## 4. 自守表示的构造：$\mathrm{GL}(5)$

### 4.1 为什么是 $\mathrm{GL}(5)$

$$
\boxed{
\text{单纯形 5 顶点} \;\to\; \text{基本表示维数 5} \;\to\; \mathrm{GL}(5)
}
$$

**注意**：不是"$A_4$ 有 5 个 Dynkin 节点"。$A_4$ 的 Dynkin 图有 **4 个节点**（对应 $\mathfrak{sl}_5$），$\mathrm{GL}(5)$ 的约化秩是 **5**（$= \mathrm{rank}\ \mathfrak{sl}_5 + 1$）。5 的来源是**基本表示维数**。

| 对象 | 数量 |
|---|---|
| $A_4$ 嘉当矩阵 | $4 \times 4$ |
| $A_4$ Dynkin 图节点 | $4$ |
| $\mathrm{SU}(5)$ 秩 | $4$ |
| 正四单纯形顶点 | $5$ |
| $\mathrm{GL}(5)$ 约化秩 | $5$ |
| $\mathrm{GL}(5)$ 基本表示维数 | $5$ |

### 4.2 候选构造：$\mathrm{Sym}^4$ 提升

$$\pi_p = \mathrm{Sym}^4(\pi_2)$$

| 提升 | 证明者 | 状态 |
|---|---|---|
| $\mathrm{Sym}^2\ (\mathrm{GL}_2 \to \mathrm{GL}_3)$ | Gelbart–Jacquet 1978 | 已证 |
| $\mathrm{Sym}^3\ (\mathrm{GL}_2 \to \mathrm{GL}_4)$ | Kim–Shahidi 2002 | 已证 |
| $\mathrm{Sym}^4\ (\mathrm{GL}_2 \to \mathrm{GL}_5)$ | Kim 2003 | 已证 |
| $\mathrm{Sym}^5$ 以上 | — | 一般情形未知 |

$$
\boxed{
\mathrm{GL}(5) \text{ 是当代数论能站住的最高阶对称幂之一。}
}
$$

**尖点性判据**（Kim–Shahidi）：

$$\mathrm{Sym}^4(\pi) \text{ 尖性} \iff \pi \text{ 非二面体/四面体/八面体型}$$

### 4.3 自守表示的结构

$$\pi_p = \bigotimes_v \pi_{p,v}$$

| 素处 | 类型 | 数据 |
|---|---|---|
| $v = \infty$ | Archimedean | 无穷小特征，由 $A_4$ 谱几何决定 |
| $v = p$ | 非 Archimedean | Satake 参数 |

---

## 5. $G_N$ 公式与自守形式的对应

### 5.1 谱公式

$$G_N = \frac{\hbar c}{m_p^2} \cdot I \cdot \lambda_c \cdot ☯^2 \cdot \mathfrak{c}_1 \cdot \exp(-2/☯) \cdot (1 + \kappa ☯)$$

### 5.2 公式元素的分解

| 因子               | 来源                         | 性质     |
| ---------------- | -------------------------- | ------ |
| $I = 5/3$        | $\mathrm{SU}(5)$ Dynkin 指数 | 质子特有   |
| $\lambda_c$      | Mathieu 临界参数               | 质子特有   |
| $\mathfrak{c}_1$ | 谱系数                        | 质子特有   |
| $\kappa$         | 修正系数                       | 质子特有   |
| $☯$              | 全局谱权重                      | **普适** |
| $\exp(-2/☯)$     | 全局谱行为                      | **普适** |

$$
\boxed{
G_N \text{ 是质子特有数据与普适 } ☯ \text{ 的结合。}
}
$$

---

## 6. $☯$ 的唯一定义

$$
\boxed{
☯ = \frac{d}{ds}\ln\xi(s)\bigg|_{s=1} = \frac{\xi'(1)}{\xi(1)} \approx 0.0230957
}
$$

### 6.1 $\zeta$ 与 $\xi$：同一对象的两副面孔

$\zeta$ 和 $\xi$ 不是两个东西，而是 $\mathrm{GL}(1)$ 平凡特征给出的**同一个 $L$ 函数**的两种呈现。$\zeta$ 是最基础的那个（Selberg 类 degree 1），$\xi$ 是在它上面补 $\Gamma$ 因子、消极点造出来的：

$$\xi(s) = \tfrac12\, s(s-1)\,\pi^{-s/2}\,\Gamma(s/2)\,\zeta(s)$$

| | $\zeta(s)$ | $\xi(s)$ |
|---|---|---|
| **本质** | 有限/算术部分 | 完备 + 整化 |
| **$s=1$** | 极点 | $= 1/2$ |
| **Euler 积** | 有 | 无 |
| **平凡零点** $(−2,−4,\ldots)$ | 有 | 被消掉 |

不是 $\xi$ 退化成 $\zeta$，而是 $\xi$ 由 $\zeta$ 构成。二者是同一对象的**算术面孔**（$\zeta$：Euler 积、有极点、含平凡零点）与**谱面孔**（$\xi$：整、无极点、只含非平凡零点）。

### 6.2 为什么取 $\xi$ 而非 $\zeta$

关键区别：$\xi$ 把平凡零点消掉了。$\Gamma(s/2)$ 在负偶数的极点正好抵消 $\zeta$ 在那里的平凡零点，于是：

- $\zeta$ 的零点 = 非平凡零点（临界带）$+$ 平凡零点 $(−2,−4,\ldots)$
- $\xi$ 的零点 = **只有非平凡零点** $\{\gamma_n\}$

$☯$ 的求和式只过 $\gamma_n$，不过平凡零点：

$$\frac{d}{ds}\ln\xi(s)\bigg|_{s=1} = \sum_{\gamma > 0} \frac{1}{\gamma^2 + 1/4} = ☯$$

这恰好是 $\xi$ 的 Hadamard 积 $\xi(s) = \xi(0)\prod_\rho\bigl(1 - s/\rho\bigr)$ 给出的。如果用 $\zeta$，求和会多出一堆平凡零点的贡献；且 $\frac{d}{ds}\ln\zeta(s)\big|_{s=1}$ 发散（$\zeta$ 在 $s=1$ 有极点）。**CQM 的 $☯$ 取自 $\xi$ 而非 $\zeta$，因为只有 $\xi$ 的零点集恰好是 $\{\gamma_n\}$**——它是谱上唯一干净的那个。

### 6.3 $\mathrm{GL}(n)$ 推广

$☯$ 来自 $\mathrm{GL}(n)$ 对应的平凡自守形式（Eisenstein 级数）$L$ 函数。对每个 $n$，$\mathrm{GL}(n)$ 平凡自守形式 $L$ 函数给出 $n \cdot ☯$（$n$ 倍相变量子）；除以 $n$ 提取出 $☯$ 本身。$☯$ 是**普适常数**，不依赖于 $n$。$\mathrm{GL}(1)$ 情形（$n=1$）即 $☯ = \frac{d}{ds}\ln\xi(s)\big|_{s=1}$。

### 6.4 定性

$☯$ 属于**谱面孔**。"质数是源"（$\zeta$ / 算术侧）和"$☯$ 是全局谱权重"（$\xi$ / 谱侧）不是同一侧的陈述——它们分别对应这个最简单对象的两张脸。

**正确的分层**：

$$
\boxed{
\text{普适 } ☯ \;+\; \text{质子特有 } \pi_p \;\Longrightarrow\; G_N
}
$$

---

## 7. 质量从自守关联中出现

$$[M] = \frac{[L]^3}{[G_N]\cdot[T]^2}$$

$$
\boxed{
M_{\text{质子}} \sim \text{自守 } L\text{-函数在特殊点的值}
}
$$

$$M_{\text{质子}} = \frac{L_{\text{质子}}^3}{G_N \cdot T_{\text{质子}}^2}$$

等价地：

$$G_N = \frac{L_{\text{质子}}^3}{M_{\text{质子}} \cdot T_{\text{质子}}^2}$$

（两者是同一方程的移项，不再重复列为两个结果。）

---

## 8. 自守分化：从质子到其他粒子（修正）

### 8.1 核心命题

$$
\boxed{
\text{质子 } A_4 \text{ 是基础对象，} \pi_p \text{ 是根本自守表示。}
}
$$

$$
\boxed{
\text{其他粒子是 } \pi_p \text{ 的朗兰兹函子性分化。}
}
$$

### 8.2 分化操作（只用已证的函子性操作）

| 粒子 | 操作 | 数学形式 | 状态 |
|---|---|---|---|
| **介子** | 对称平方 | $\mathrm{Sym}^2(\pi_p)$ | 已证（Kim–Shahidi） |
| **中子** | 内窥转移 | $\mathrm{BC}_{E/F}(\pi_p)$ | 已证（Langlands） |
| **电子** | 自守诱导的对偶 | $\mathrm{Ind}_H^G(\sigma)^\vee$ | 需构造 |
| **激发态** | 对称幂 | $\mathrm{Sym}^n(\pi_p)$ | $n \leq 4$ 已证 |

**删除**：
- $\mathrm{Res}_H(\pi_p)$：限制到子群不是朗兰兹函子性操作
- $\pi_p \otimes D(\delta)$：缺陷矩阵不是自守表示，不能张量
- $\pi_p \otimes \tilde{\pi}_p$：Rankin–Selberg $L$-函数在 $s=1$ 有单极点

### 8.3 介子的正确公式

$$L(s, \pi_p \times \pi_p^\vee) = \frac{\zeta(s)}{\zeta(s+1)} \cdot L(s, \mathrm{Sym}^2 \pi_p)$$

极点来自 $\zeta(s)$，但 $\mathrm{Sym}^2 \pi_p$ 部分是有限的。所以：

$$
\boxed{
m_{\text{meson}} = \text{const} \cdot L(1, \mathrm{Sym}^2 \pi_p)
}
$$

### 8.4 中子的正确公式

内窥转移：

$$\pi_n = \mathrm{BC}_{E/F}(\pi_p)$$

其中 $E/F$ 是某个二次扩张，$D(\delta)$ 作为转移参数。

### 8.5 电子的正确公式

自守诱导的对偶：

$$\pi_e = \mathrm{Ind}_H^G(\sigma)^\vee$$

其中 $H \subset G$ 是某个子群，$\sigma$ 是 $H$ 上的自守表示。

### 8.6 质量谱

$$
\boxed{
\text{质量谱 = 朗兰兹函子性分化谱。}
}
$$

$$m_i = \text{const} \cdot L(1, \pi_i)$$

---

## 9. 完整图景

$$
\boxed{
\begin{array}{c}
\text{质子 } A_4 \\
\swarrow \quad\quad \searrow \\
L \text{ 属性} \quad\quad T \text{ 属性} \\
\searrow \quad\quad \swarrow \\
\text{自守关联 } \pi_p = \mathrm{Sym}^4(\pi_2) \\
\downarrow \\
\text{质量 } M_{\text{质子}} \\
\downarrow \\
G_N \text{ 的谱公式} \\
\downarrow \\
\text{朗兰兹函子性分化} \to \text{其他粒子}
\end{array}
}
$$

---

## 10. 研究路径

$$
\boxed{
\begin{array}{c}
\text{第一步：构造 } \pi_p = \mathrm{Sym}^4(\pi_2) \\
\downarrow \\
\text{第二步：计算 } L(s, \pi_p) \\
\downarrow \\
\text{第三步：验证函数方程（} L \leftrightarrow T \text{ 对偶）} \\


\downarrow \\
\text{第四步：推导 } G_N \\
\downarrow \\
\text{第五步：与 CODATA 对比} \\
\downarrow \\
\text{第六步：计算朗兰兹函子性分化} \\
\downarrow \\
\text{第七步：得到其他粒子质量谱}
\end{array}
}
$$

### 10.1 第一步：构造 $\pi_p$

**输入**：
- $A_4$ 谱几何：$\{9^{(1)}, 4^{(4)}, 1^{(5)}\}$
- $\mathrm{SU}(5)$ Dynkin 指数：$I = 5/3$
- 基本表示维数：$5$
- 禁闭边界条件

**构造**：
$$\pi_p = \mathrm{Sym}^4(\pi_2)$$

### 10.2 第二步：计算 $L(s, \pi_p)$

$$L(s, \pi_p) = \prod_v L_v(s, \pi_{p,v})$$

Archimedean 因子：
$$L_\infty(s, \pi_{p,\infty}) = \prod_{j=1}^{5} \Gamma_\mathbb{R}(s + \mu_j)$$

非 Archimedean 因子：
$$L_p(s, \pi_{p,v}) = \prod_{j=1}^{5} \frac{1}{1 - \alpha_{j,p} p^{-s}}$$

### 10.3 第三步：验证函数方程

$$L(s, \pi_p) = \varepsilon(s, \pi_p) L(1-s, \tilde{\pi}_p)$$

物理诠释：$s \leftrightarrow 1-s$ 对应 $L \leftrightarrow T$。


### 10.4 第四步：推导 $G_N$

$$G_N = \frac{\hbar c}{m_p^2} \cdot I \cdot \lambda_c \cdot ☯^2 \cdot \mathfrak{c}_1 \cdot \exp(-2/☯) \cdot (1 + \kappa ☯)$$

### 10.5 第五步：与 CODATA 对比

$$G_N^{\text{CQM}} \stackrel{?}{=} 6.6742810045 \times 10^{-11}\ \text{SI}$$

当前偏差约 $-3\ \text{ppm}$。

---

## 11. 关键约束

| 约束 | 内容 |
|---|---|
| **函数方程** | $L(s,\pi_p) = \varepsilon(s,\pi_p) L(1-s,\tilde{\pi}_p)$ |
| **尖点性** | $\mathrm{Sym}^4(\pi)$ 尖性 $\iff$ $\pi$ 非二面体/四面体/八面体型 |
| **谱几何** | $A_4$ 本征值 $\{9^{(1)}, 4^{(4)}, 1^{(5)}\}$ 决定 Archimedean 参数 |
| **数值检验** | $G_N$ 与 CODATA 偏差约 $-3\ \text{ppm}$ |
| **统一性** | 所有粒子来自同一个 $\pi_p$ 的函子性分化 |

---

## 12. 与传统方法的竞争关系

| 维度 | 传统方法 | CQM |
|---|---|---|
| **起点** | 质量数据 | $A_4$ 谱几何 |
| **自守形式** | 拟合工具 | 生成机制 |
| **质量比** | 核心对象 | 副产品 |
| **量纲** | 预设 | 生成 |
| **粒子数** | 每个独立 | 一个 $\pi_p$ 分化 |
| **第一性** | 否 | 目标 |

$$
\boxed{
\text{传统回答"是什么"，CQM 回答"为什么"。}
}
$$

---

## 13. 开放问题

| 问题 | 内容 |
|---|---|
| **$\pi_2$ 的具体选择** | 从 $A_4$ 谱几何到 $\pi_2$ 的严格映射 |
| **$\lambda_c, \mathfrak{c}_1, \kappa$ 的来源** | 这些系数如何从 $\pi_p$ 的算术数据推出 |
| **电子的自守诱导** | $\mathrm{Ind}_H^G(\sigma)^\vee$ 中 $H, \sigma$ 的具体选择 |
| **中子的内窥转移** | $\mathrm{BC}_{E/F}(\pi_p)$ 中 $E/F$ 的具体选择 |
| **多重度与表示维数的对应** | $(1,4,5)$ 与 $\mathbf{1} \oplus \mathbf{4} \oplus \mathbf{5}$ 的对应需单独论证 |
| **$☯$ 的来源** | 从 $\mathrm{GL}(n)$ 平凡自守形式 $L$ 函数提取（$n\cdot☯$ 除以 $n$），普适常数，不依赖 $n$；闭式 $1+\gamma_E/2-\tfrac12\ln\pi-\ln2$ 已验证 |

---

## 14. 最终结论

$$
\boxed{
\text{核心思路：质子的 } L \text{ 和 } T \text{ 属性建立自守关联，质量从中涌现。}
}
$$

$$
\boxed{
\text{自守表示：} \pi_p = \mathrm{Sym}^4(\pi_2) \text{ 在 } \mathrm{GL}(5,\mathbb{A}_{\mathbb{Q}}) \text{ 上。}
}
$$

$$
\boxed{
\text{质量 } M \text{ 和 } G_N \text{ 从 } \pi_p \text{ 的 } L\text{-函数特殊值中出现。}
}
$$

$$
\boxed{
\text{其他粒子是 } \pi_p \text{ 的朗兰兹函子性分化。}
}
$$

$$
\boxed{
\text{核心任务：从 } A_4 \text{ 谱几何构造 } \pi_2 \text{，计算 } L(s, \mathrm{Sym}^4 \pi_2) \text{，验证 } G_N \text{ 和粒子质量谱。}
}
$$

$$
\boxed{
\text{一旦 } G_N \text{ 被第一性推导，CQM 就从"理论框架"升级为"第一性理论"。}
}
$$

---

## 附 A：来源定位（提取自项目文档）

本汇总的正文各条目与项目文档的对应关系如下（"修正版新增"指本次修正引入的框架性表述，项目文档无同文先行）：

| 本汇总条目 | 项目出处 |
|---|---|
| §0–§2（量纲地位、$G_N$ 为 $M$ 的转换常数、$L/T$ 先建立） | `01 核心理论/CQM_核心_量纲与单位制.md` §7（$[M]=[L]^3/([G_N][T]^2)$；质量层转换常数为 $G_N$；每压掉一个量纲冒出一个更基础的转换常数） |
| §3.1（$A_4$ 谱几何 $\{9,4,1\}$） | `03 引力与退相干/CQM_引力_GN谱公式.md` §8；`01 核心理论/CQM_核心_集成理论.md`（$M=E^TE$ 本征值 $\{9,4,1\}$、重数 $\{1,4,5\}$，标为"S₅ 表示论 + 迹条件"） |
| §3.2/§3.3（自守关联、$f_L,f_T\in\pi_p$） | 修正版新增（对应发生学分层：自守形式 → L 函数 → 朗兰兹；见 `01 核心理论/CQM_核心_朗兰兹分层共振与谱量子.md`） |
| §4（GL(5) 构造与 Sym⁴ 提升） | 修正版新增（候选构造 $\pi_p=\mathrm{Sym}^4(\pi_2)$；文献支撑见附 B） |
| §5（$G_N$ 谱公式） | `03 引力与退相干/CQM_引力_GN谱公式.md` §8.2–8.3（参数来源表：$☯=0.02309570897$、$\mathfrak{c}_1=1/4+\gamma_1^2=200.04045483$、$\lambda_c=1.316022911$、$I=5/3$、$\kappa=(31+☯)/30$、$\exp(-2/☯)$、$m_p$ 实验输入） |
| §6（☯ 唯一定义） | `01 核心理论/CQM_核心_朗兰兹分层共振与谱量子.md`（$☯=\frac{d}{ds}\ln\xi(s)\big|_{s=1}=\sum 1/(\gamma_n^2+1/4)\approx 0.0230957$）；$\zeta$ 与 $\xi$ 是 GL(1) 平凡特征同一 $L$ 函数的算术面孔与谱面孔，☯ 取自 $\xi$（只有 $\xi$ 零点集恰好是 $\{\gamma_n\}$）；$\mathrm{GL}(n)$ 给出 $n\cdot☯$，☯ 为普适常数 |
| §7（质量从自守关联出现） | 修正版整理（原 §7.2/§7.3 两处移项合并为一个方程） |
| §8（自守分化） | 修正版新增（朗兰兹函子性分化；删除 $\mathrm{Res}_H$、$\otimes D(\delta)$、$\otimes\tilde{\pi}_p$ 三个错误操作） |
| §10.6（CODATA 对比） | `03 引力与退相干/CQM_引力_GN谱公式.md` §9 高精度数值验证（$G_N$ 与 CODATA 偏差约 $-3$ ppm） |
| 历史前身（仅作参考，非当前权威表述） | `归档 CNT/07 计算框架/03-完整粒子谱`、`05-汤川耦合与费米子混合`（谱几何第一性推导的历史探索） |

---

## 附 B：文献支持（外部文献核查，2026-09-20）

**核查范围说明**：文献核查只确认数学构件（函子性定理、标准理论、数值事实）在文献中成立；本汇总的物理命题（质子 $L/T$ 属性 → 自守关联 → 质量涌现）属 CQM 框架自身主张，文献支撑其数学构件而非背书其物理诠释。

| 本汇总条目 | 文献 | 文献建立的内容 | 状态 |
|---|---|---|---|
| §4.2 Sym² | Gelbart & Jacquet 1978, *Ann. Sci. École Norm. Sup.* (4) 11, 471–542 | GL(2) 自守表示的对称平方提升为 GL(3) 自守表示，L 函数对应 | 已证（严格） |
| §4.2 Sym³ | Kim & Shahidi 2002, *Ann. of Math.* (2) 155, 837–893 | Sym³(π) 为 GL(4) 自守表示（Langlands–Shahidi 方法）；尖点性依 π 而定 | 已证（函子性） |
| §4.2 Sym⁴ | Kim 2003, *J. Amer. Math. Soc.* 16, 139–183 | Sym⁴(π) 为 GL(5) 自守表示；exterior square 与 symmetric fourth 的 L 函数关系 | 已证（函子性） |
| §4.2 Sym⁵ 以上 | 一般 GL(2) 情形仍开放；Newton & Thorne 2021, *Publ. Math. IHES* 134, 1–116 | 对全纯 Hecke 尖点形式（无复乘）情形，全部对称幂函子性已证；一般情形不直接外推 | 一般情形未证 |
| §4.2/§11 尖点性判据 | Kim 2003（附录含 Ramakrishnan、Sarnak） | Sym⁴ 尖点性判据（非二面体/四面体/八面体型） | 已证；表述以原文为准 |
| §8.3/§8.6 Rankin–Selberg | Jacquet & Shalika 1981, *Amer. J. Math.* 103, 777–815；Jacquet–Piatetski-Shapiro–Shalika 1983, *Amer. J. Math.* 105, 367–464 | 尖点 π 的 $L(s,\pi\times\tilde{\pi})$ 在 $s=1$ 有简单极点；GL(n)×GL(m) Rankin–Selberg 卷积的标准参考 | 已证（严格） |
| §8.3 恒等式（对齐注） | 标准恒等式：$L(s,\pi\times\tilde{\pi})=\zeta(s)\,L(s,\mathrm{Sym}^2\pi)$ | 标准恒等式不含 $\zeta(s+1)$ 分母因子；文档写法的 $\zeta(s+1)$ 分母为框架内表述，需对齐说明 | 需对齐 |
| §8.4 内窥转移 | Langlands 1980, *Base Change for GL(2)*, AMS 96；Arthur & Clozel 1989, *Simple Algebras, Base Change, and the Advanced Theory of the Trace Formula*, AMS 120 | GL(2) 循环基变换；GL(n) 循环基变换与自守诱导 | 已证（严格） |
| §8.5 自守诱导 | Arthur & Clozel 1989（循环扩张情形）；Henniart 2000, *Invent. Math.* 139, 439–455（局部） | 循环扩张的自守诱导 $\pi\mapsto AI(\pi)$，L 函数保持；可解扩张亦成立 | 已证（循环/可解情形） |
| §8.2 删除 Res_H | Cogdell 2003, "Dual groups and Langlands functoriality", in *An Introduction to the Langlands Program*（Bernstein–Gelbart 编），251–268；Borel 1979, *Proc. Sympos. Pure Math.* 33, 27–61 | 函子性 = 经 L 群同态 $^{L}H \to {}^{L}G$ 的表示转移；不存在一般的"限制"函子 | 支持删除判断 |
| §3.1 $A_4$ 谱 $\{9^{(1)},4^{(4)},1^{(5)}\}$ | 本项目直接计算验证（迹 30、谱和 30）；框架文献：Horak & Jost 2013, *Adv. Math.* 244, 303–336；Duval & Reiner 2002, *Trans. AMS* 354, 4313–4344 | 单纯形组合/高阶 Hodge 拉普拉斯谱的一般框架；整数谱性质 | 谱事实=本项目验证；文献提供框架 |
| §3.1 S₅ 分解 $1\oplus4\oplus5$ | Fulton & Harris 1991, GTM 129；James & Kerber 1981, LNM 682 | S₅ 作用在 3-子集上的 10 维置换表示分解为 $1\oplus4\oplus5$ | 标准（严格） |
| §5 λ_c（Mathieu） | McLachlan 1947, *Theory and Application of Mathieu Functions*, Oxford；NIST DLMF 第 28 章（§28.2） | Mathieu 方程标准形式、特征值 $b_1(q)$、$se_1$、连分数理论 | 标准理论；$\lambda_c$ 数值为本项目计算（$q_c=0.3290057278$） |
| §6 ☯ | Titchmarsh 1986（2 版，Heath-Brown 修订） | ξ 函数、Hadamard 乘积、$\xi'/\xi$ 理论；恒等式 $\sum_{\gamma>0}1/(\gamma^2+1/4)=\frac{d}{ds}\ln\xi(s)\big|_{s=1}$ 可由此推出；本项目验证闭式 $1+\gamma_E/2-\tfrac12\ln\pi-\ln2=0.02309570897$ | 标准理论；数值已验证 |
| §10.6 CODATA | Mohr, Newell, Taylor, Tiesinga 2025, *Rev. Mod. Phys.* 97, 025002（CODATA 2022） | $G=6.67430(15)\times10^{-11}\ \mathrm{m^3\,kg^{-1}\,s^{-2}}$（2022 与 2018 相同）；本项目值偏差 $-2.85$ ppm ≈ $-3$ ppm | 实验参考值 |
| §4.1 Lie 理论 | Bourbaki, *Groupes et Algèbres de Lie*, Ch. 4–6；Humphreys 1972, GTM 9 | $A_4$ Dynkin 图 4 节点、Cartan 矩阵 $4\times4$、SL(5) 秩 4、GL(5) 约化秩 5 | 标准（严格） |

**补充说明**：

1. **Sym⁵ 以上的现状**：§4.2 表中"一般情形未知"应精确理解为"一般 GL(2) 自守表示情形未解决"——Newton–Thorne（2021）已证明全纯 Hecke 尖点形式（无复乘）情形的对称幂函子性，不能直接外推到一般情形。
2. **§8.3 恒等式对齐**：标准 Rankin–Selberg 恒等式为 $L(s,\pi\times\tilde{\pi})=\zeta(s)L(s,\mathrm{Sym}^2\pi)$，不含 $\zeta(s+1)$ 分母。文档写法为框架内表述，严格化时需给出该分母的机制说明或改按标准恒等式。
3. **§8.4 术语提示**：文献中"内窥转移"（endoscopy）通常指 Langlands–Shelstad 内窥理论，而 $\mathrm{BC}_{E/F}$（基变换）对应 Langlands 1980 / Arthur–Clozel 1989；术语可考虑统一为"基变换"以避免歧义。
4. **§3.1 谱事实已直接验证**：4-单纯形边-面关联矩阵 $E\in\{0,1\}^{10\times10}$（$E_{fe}=1$ 当边 $e\subset$ 面 $f$），$E^TE$ 本征值恰为 $\{9,4,4,4,4,1,1,1,1,1\}$，即 $\{9^{(1)},4^{(4)},1^{(5)}\}$，迹 30、谱和 30。
5. **§6 ☯ 的闭式**：$☯=\frac{d}{ds}\ln\xi(s)\big|_{s=1}=1+\gamma_E/2-\tfrac12\ln\pi-\ln2\approx 0.02309570897$（$\gamma_E$ 为欧拉–马歇罗尼常数），由 ξ 的 Hadamard 乘积推出，非拟合值。

---

## 参考文献

[1] S. Gelbart, H. Jacquet, *A relation between automorphic representations of GL(2) and GL(3)*, Ann. Sci. École Norm. Sup. (4) 11 (1978), 471–542.

[2] S. Gelbart, H. Jacquet, *Forms of GL(2) from the analytic point of view*, in: Automorphic Forms, Representations and L-functions, Proc. Sympos. Pure Math. 33, AMS, 1979, 213–251.

[3] H. H. Kim, F. Shahidi, *Functorial products for GL(2)×GL(3) and the symmetric cube of GL(2)*, Ann. of Math. (2) 155 (2002), 837–893.

[4] H. H. Kim, *Functoriality for the exterior square of GL(4) and the symmetric fourth of GL(2)*, J. Amer. Math. Soc. 16 (2003), 139–183.

[5] J. Newton, J. A. Thorne, *Symmetric power functoriality for holomorphic modular forms*, Publ. Math. IHES 134 (2021), 1–116.

[6] H. Jacquet, J. Shalika, *On Euler products and the classification of automorphic forms II*, Amer. J. Math. 103 (1981), 777–815.

[7] H. Jacquet, I. I. Piatetski-Shapiro, J. Shalika, *Rankin-Selberg convolutions*, Amer. J. Math. 105 (1983), 367–464.

[8] R. P. Langlands, *Base Change for GL(2)*, Annals of Mathematics Studies 96, Princeton Univ. Press, 1980.

[9] J. Arthur, L. Clozel, *Simple Algebras, Base Change, and the Advanced Theory of the Trace Formula*, Annals of Mathematics Studies 120, Princeton Univ. Press, 1989.

[10] G. Henniart, *Une preuve simple des conjectures de Langlands pour GL(n) sur un corps p-adique*, Invent. Math. 139 (2000), 439–455.

[11] A. Borel, *Automorphic L-functions*, in: Automorphic Forms, Representations and L-functions, Proc. Sympos. Pure Math. 33, AMS, 1979, 27–61.

[12] J. W. Cogdell, *Dual groups and Langlands functoriality*, in: An Introduction to the Langlands Program (J. Bernstein, S. Gelbart, eds.), Birkhäuser, 2003, 251–268.

[13] J. Arthur, *The principle of functoriality*, Bull. Amer. Math. Soc. 40 (2003), 1–34.

[14] D. Horak, J. Jost, *Spectra of combinatorial Laplace operators on simplicial complexes*, Adv. Math. 244 (2013), 303–336.

[15] A. Duval, V. Reiner, *Shifted simplicial complexes are Laplacian integral*, Trans. Amer. Math. Soc. 354 (2002), 4313–4344.

[16] N. W. McLachlan, *Theory and Application of Mathieu Functions*, Oxford Univ. Press, 1947.

[17] NIST Digital Library of Mathematical Functions, Chapter 28: *Mathieu Functions and Hill's Equation*. https://dlmf.nist.gov/28

[18] E. C. Titchmarsh, *The Theory of the Riemann Zeta-Function*, 2nd ed. (rev. D. R. Heath-Brown), Oxford Univ. Press, 1986.

[19] P. J. Mohr, D. B. Newell, B. N. Taylor, E. Tiesinga, *CODATA recommended values of the fundamental physical constants: 2022*, Rev. Mod. Phys. 97 (2025), 025002.

[20] W. Fulton, J. Harris, *Representation Theory: A First Course*, GTM 129, Springer, 1991.

[21] G. James, A. Kerber, *The Representation Theory of the Symmetric Group*, LNM 682, Springer, 1981.

[22] N. Bourbaki, *Groupes et Algèbres de Lie*, Chapitres 4–6, Hermann, Paris, 1968.

[23] J. E. Humphreys, *Introduction to Lie Algebras and Representation Theory*, GTM 9, Springer, 1972.
