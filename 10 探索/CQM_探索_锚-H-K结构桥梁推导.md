# CQM 锚—H_ij—K(t) 结构桥梁：从节点出发的完整推导


---

## 0. 结论先行

从节点定义可严格推出一条结构链：

$$\underbrace{A_\tau\ (\text{零亏角边约束})}_{\text{锚（相变体现）}}
\;\longrightarrow\;
\underbrace{\mathsf H=(\mathcal H_{ij}=\tau_i-\tau_j)\ \text{全对冻结为}\ c_{ij}}_{\text{T1 相位差（等高不等位）}}
\;\longrightarrow\;
\underbrace{K(\tau_i)-K(\tau_j)=-\sum_n\frac{e^{i\Phi_{n,j}}(e^{i\gamma_n\mathcal H_{ij}}-1)}{\rho_n}}_{\text{DM.25：逐对 }H\leftrightarrow K\ \text{桥梁}}$$

- **能严格推出**（第 1–4 节）：$\mathcal H_{ij}=\tau_i-\tau_j$ 与全对族 $\mathsf H$、T1 相位差、$K$ 谱侧、DM.25 代数桥梁、锚冻结全对相位差 ⇒ 各点 $K$ 差固定平移（**等高不等位**，不是同一平台）。
- **构造识别**（第 2 节，唯一跳跃）：$K$ 的自变量 $t$ ≡ 固有时 $\tau_i$（本框架固有时只有一个概念）。
- **未闭合**（第 6 节）：M9 数值同一、M10 定量映射、R30 谱系数读数待独立复现——只做结构层贯通，不写 $\mathcal I_K=\mathcal H_{ij}$。全局平台须全对 $c_{ij}=0$（`临-16`），不是锚的推论。

---

## 0.1 判定与适用范围

第 7 节那条"相变锚 ⇒ 共享"的链条须分三层读，且主语是**核** $A_\tau$：

| 层 | 命题 | 判定 |
|:---|:---|:---|
| 代数层 | 核内 $\dot{\mathcal H}_{ij}=0\Rightarrow K(\tau_i)=K(\tau_j+c_{ij})$ | **成立**（第 3–5 节已给，与改名无关） |
| 因果层 | "相变锚（$\mathfrak A(T)$）给出共享" | **不成立**：共享由零亏角几何（$\ell_e=0$）给出，相变锚是空间载体与读出 |
| 平台层 | "核内共享 ⇒ 同一平台" | **不成立**：需全对 $c_{ij}=0$（`临-16`）；数值同一属 M9 |

**适用范围**：$\dot{\mathcal H}=0$ 与 $T$ 无关，故"等高不等位"在**整核**成立（含未被 $\mathcal A(T)$ 占据的边），只能用 $A_\tau$ 表述。逐对共享**不需**全局单值条件（核内 $\prod_kr_k=1$ 由 $\ell^{(0)}=0$ 给）；"全样品单一平台"才需 $[r]=0$ 与 $c_{ij}=0$ 两件不同的事。$\dot{\mathcal H}=0$ 是冻结判据、平凡必要（条件于 T1／M1），不能当相变判据。

---

## 1. 权威定义（引述，不改写）

| 量 | 定义 | 来源 |
|:---|:---|:---|
| 固有时流速接口 | $v_\tau=\sqrt{1-\varepsilon/2\pi}$（假设） | FG_核心理论 §3.1；06 §0.4 |
| 节点固有时 | $\tau_i(t)=\int_0^t v_{\tau,i}\,dt'$ | 06 §0.4 |
| 历史总和（本体） | $\mathsf H(t)=(\mathcal H_{ij}(t))_{i,j\in V_t}$，分量 $\mathcal H_{ij}(t)=\int_0^t(v_{\tau,i}-v_{\tau,j})dt'=\tau_i-\tau_j$；投影 $\mathcal D=\frac{2}{N-1}\sum_i(\tau_i-\bar\tau)^2$（06 §0.3/§0.6） | 06 §0.4/§0.6 |
| 漂移定理 T1 | $\Phi_{n,i}=\gamma_n\tau_i$，$\Phi_{n,i}-\Phi_{n,j}=\gamma_n\mathcal H_{ij}$ | 06 §0.4 |
| 记忆核（超导态质数形式） | $K(t)=e^{-t/2}\bigl(\psi(e^t)-e^t\bigr)$，$\psi(x)=\sum_{p^m\le x}\ln p$；正常态 $K$ 为非质数涨落关联 | 06 §0.0/§0.6（【构造】） |
| 谱侧（显式公式） | $K(t)=-\sum_\rho e^{(\rho-1/2)t}/\rho+O(e^{-t/2})$ | 06 §0.6 DM.20（严格数论） |
| 相变锚核 | $A_\tau$＝零亏角边极大连通子图；判据"相位差冻结（等速）"；相变锚见 06 §7.3 | 06 §7.3/§0.3 |
| 记忆平台 | $K^{\rm SC}$（$T<T_c$ 稳定平台）；$A_\tau\to K^{\rm SC}$ 占据–读出 | 06 §0.7 |

---

## 2. 关键识别：固有时同一性（构造识别，全文唯一跳跃）

$K(t)$ 的自变量写为 $t$，节点固有时写为 $\tau_i$。**识别二者为同一坐标**：

$$t\;\equiv\;\tau_i .$$

**依据**（非虚构）：
1. 本框架固有时只有一个概念；$K$ 的定义"以参考点为基的计数减光滑主项"（06 §0.6 line 225）中的"参考点"即节点时钟。
2. 06 §0.6 line 233 早已把 $K$ 的指数接到 $\tau$：重标定 $\tau(t)=\int_0^t v_\tau dt'$ 把公共衰减率 $\tfrac12$ 换成 $\langle v_\tau\rangle/2$——即 $K$ 的时间变量与固有时族同源。

**边界**：这是构造识别，不是从更底层公设推导；若将来拒绝此识别，第 3–5 节的桥梁不成立。识别本身不新增概念或数值。

---

## 3. 从节点到 H_ij（严格）

**Step 1（定义恒等式）**：由 $\tau_i=\int_0^t v_{\tau,i}dt'$，

$$\tau_i-\tau_j=\int_0^t(v_{\tau,i}-v_{\tau,j})\,dt'=\mathcal H_{ij}(t),\qquad \mathsf H(t)=(\mathcal H_{ij}(t))_{i,j\in V_t}.$$

全对族满足 $\mathcal H_{ii}=0$、$\mathcal H_{ij}=-\mathcal H_{ji}$、$\mathcal H_{ij}+\mathcal H_{jk}=\mathcal H_{ik}$；$\binom{N}{2}$ 个分量只有 $N-1$ 个独立，故"所有节点对"不是把 $\mathcal H_{ij}$ 逐对相加，而是族及其对称投影（06 §0.6）。

**Step 2（T1，文档严格）**：$\Phi_{n,i}=\gamma_n\tau_i$，故

$$\Phi_{n,i}-\Phi_{n,j}=\gamma_n(\tau_i-\tau_j)=\gamma_n\mathcal H_{ij}.$$

$\mathcal H_{ij}$ 由流速差异累积而成，是**本体对象**；平均漂移率为零 $\Leftrightarrow\ell^{(0)}_{ij}=0$（06 §0.4）。

---

## 4. 从显式公式到 K 的谱侧（严格数论）

von Mangoldt 显式公式（1895；MathWorld "Explicit Formula"/"Mangoldt Summatory Function"）：

$$\psi(x)=x-\sum_\rho\frac{x^\rho}{\rho}-\ln2\pi-\tfrac12\ln(1-x^{-2}).$$

取 $x=e^t$ 并乘 $e^{-t/2}$（此为超导态 $K$ 的质数形式；正常态 $K$ 非质数形式）：

$$K(t)=e^{-t/2}(\psi(e^t)-e^t)=-\sum_\rho\frac{e^{(\rho-1/2)t}}{\rho}+O(e^{-t/2}).\tag{DM.20}$$

RH 下 $\rho=\tfrac12+i\gamma_n$，$e^{(\rho-1/2)t}=e^{i\gamma_n t}$，权重为留数 $1/\rho_n$，$|1/\rho_n|\sim\gamma_n^{-1}$（von Koch 1901：$K=O(t^2)$）。

---

## 5. DM.25 桥梁：H ↔ K（代数严格）

代入识别 $t=\tau_i$ 与 T1 的 $e^{i\gamma_n\tau_i}=e^{i\Phi_{n,i}}$：

$$K(\tau_i)=-\sum_n\frac{e^{i\Phi_{n,i}}}{\rho_n}+O(e^{-\tau_i/2}).$$

**即 $K$ 的第 $n$ 模是节点相位 $e^{i\Phi_{n,i}}$ 的留数 $1/\rho_n$ 加权和。** 对节点对 $(i,j)$ 作差，用 $\Phi_{n,i}-\Phi_{n,j}=\gamma_n\mathcal H_{ij}$：

$$\boxed{\;K(\tau_i)-K(\tau_j)=-\sum_n\frac{e^{i\Phi_{n,j}}\bigl(e^{i\gamma_n\mathcal H_{ij}}-1\bigr)}{\rho_n}+O(e^{-\tau/2}).\;}\tag{DM.25}$$

解释：$\mathcal H_{ij}$ 作为相位差 $\gamma_n\mathcal H_{ij}$ 直接生成 $K$ 的模差 $(e^{i\gamma_n\mathcal H_{ij}}-1)$；当 $\mathcal H_{ij}=0$，模差为零，$K(\tau_i)=K(\tau_j)$。权重 $1/\rho_n$ 由 $K$ 的定义自带，**不是节点几何新造的自由参数**。这是 $\mathcal H_{ij}$ 与 $K$ 的严格结构对应（谱位置／代数层）。

### 5.1 全对版：从逐对差到测度与相干度

DM.25 是**一对节点的差**，不能把全局 $K$ 归给单对。记 $\mathcal P_t=\{(i,j):i<j,\ i,j\in V_t\}$、$M_t=\binom{|V_t|}{2}$，全对历史进模幅的接口是节点对测度的傅里叶变换：

$$\hat\mu_t(\gamma_n)=\frac{1}{|V_t|(|V_t|-1)}\sum_{i\ne j}e^{i\gamma_n\mathcal H_{ij}(t)}=\frac{1}{M_t}\sum_{(i,j)\in\mathcal P_t}\cos\bigl(\gamma_n\mathcal H_{ij}(t)\bigr)\in\mathbb R,\qquad$$
R_n^2(t)=\left|\frac1{|V_t|}\sum_{i\in V_t}e^{i\gamma_n\tau_i(t)}\right|^2=\frac1{|V_t|}+\frac{|V_t|-1}{|V_t|}\hat\mu_t(\gamma_n).$$

$N=2$ 时 $R_n^2=\cos^2(\gamma_n\mathcal H_{12}/2)$，即 DM.25 的单对写法正是两节点截断；一般 $N$ 下每对权重只有 $2/N^2$。若要全局标量，候选为节点平均 $K_{\rm glob}=\frac1N\sum_iK(\tau_i)=-\sum_n\frac{1}{\rho_n}\bigl(\frac1N\sum_ie^{i\gamma_n\tau_i}\bigr)+O(e^{-\tau/2})$，第 $n$ 模幅由 $R_n/|\rho_n|$ 读出（【构造】，不是已证）。$\mathcal D$ 的三项平衡与全对冻结判据见 06 §0.6、推导链环 6。

---

## 6. 涨落：去相干因子自然进入（不必消除 σ_v）

令 $\tau_i(t)=\langle\tau_i\rangle+\delta\tau_i$，$\delta v$ 为 OU 过程 $\langle\delta v(s)\delta v(s')\rangle=\sigma_v^2e^{-|s-s'|/\tau_g}$（06 §0.6 环节⑥）。积分 OU 的方差：

$$\mathrm{Var}\Big[\!\int_0^t\!\delta v\,ds'\Big]=2\sigma_v^2\Big[\tau_g t-\tau_g^2(1-e^{-t/\tau_g})\Big]\xrightarrow[t\gg\tau_g]{}2\sigma_v^2\tau_g t .$$

高斯过程特征函数 $\mathbb E[e^{iX}]=e^{-\sigma_X^2/2+i\mu_X}$（标准 Gaussian process 性质）给出

$$\langle e^{i\Phi_{n,i}}\rangle=e^{i\gamma_n\langle\tau_i\rangle}\exp\!\Big(-\tfrac12\gamma_n^2\cdot2\sigma_v^2\tau_g t\Big)=e^{i\gamma_n\langle\tau_i\rangle}e^{-\Gamma_n t},\qquad \Gamma_n=\gamma_n^2\sigma_v^2\tau_g,$$

与 06 §0.6 环节⑥ 的 $\Gamma_n$ 逐字一致。结论：涨落扩散是 $K$ 的**固有退相干因子**，不需要把 $\sigma_v$ 置零——此前"$\Gamma_n\to0$ 与涨落必须存在矛盾"的障碍消解。

---

## 7. 锚如何进入（M9 结构桥梁）

锚核内边 $\ell_e=0\Rightarrow v_{\tau,i}=v_{\tau,j}\Rightarrow\mathcal H_{ij}=\tau_i-\tau_j=c_{ij}$（**全对冻结，常数不必为零**）。于是

$$e^{i\gamma_n c_{ij}}\ne1\ \ (\text{一般}),\qquad
K(\tau_i)-K(\tau_j)=-\sum_n\frac{e^{i\Phi_{n,j}}\bigl(e^{i\gamma_nc_{ij}}-1\bigr)}{\rho_n},$$

即 $K(\tau_i)=K(\tau_j+c_{ij})$：锚核内节点共享**同一谱阶梯与同一斜率**，但各自带固定相位偏移——**等高不等位**，不是同一 $K(\tau)$。只有全对 $c_{ij}=0$ 才给 $K(\tau_i)=K(\tau_j)$，而 $c_{ij}=0$ 不能由 $\ell_e=0$ 推出（起点 $t_{0,i}$ 是物理事件，`临-16`）。

这正是 06 §0.7 占据–读出 $A_\tau\xrightarrow{\text{占据}}\mathcal A(t)\subseteq A_\tau\xrightarrow{\text{读出}}K^{\rm SC}$ 的代数实现：锚之所以能约束记忆侧平台，在于它把生成 $K$ 模差的相位差 $\gamma_n\mathcal H_{ij}$ 冻成常数偏移。全对相干由 §5.1 的 $\hat\mu_t(\gamma_n)$、$R_n$ 读；$K^{\rm SC}$ 的"等高"由冻结保证，"同位"另需全对 $c_{ij}=0$（`临-17`）。

**边界**：这里只给结构层，不证明 $A_\tau$ 与 $K^{\rm SC}$ 的数值同一（M9）；不写 $\mathcal I_K=\mathcal H_{ij}$（M10）。锚外 $\mathcal H_{ij}\ne\text{const}$，模差按 DM.25 持续生成。

---

## 8. 外部对照（只作对照，不进 CQM 证明）

| 外部结果 | 支持什么 | 不支持什么 |
|:---|:---|:---|
| Mori–Zwanzig／GLE：$m\gamma(t)=\beta\langle R(0)R(t)\rangle$（Kubo 1966 *Rep. Prog. Phys.* 讲义 §7–8；arXiv:2604.20453） | "涨落关联 ↔ 记忆核"的对应（第 6 节） | 不提供留数权重 $1/\rho_n$ 的节点来源 |
| 显式公式与 von Koch 界（von Mangoldt 1895；MathWorld） | $K$ 谱侧与留数权重（第 4 节） | 不涉及节点／亏角／锚 |
| Gaussian 特征函数、integrated OU 方差（MathOverflow 254927；MathStackexchange 653240） | 退相干因子 $\Gamma_n$（第 6 节） | 不涉及相位差与 $K$ 的桥梁 |

外部只支持**结构对应**，不替代 CQM 内部的识别与推导。

---

## 9. 严格性总表与边界

| 步骤 | 内容 | 等级 |
|:---:|:---|:---|
| 1 | $\mathcal H_{ij}=\tau_i-\tau_j$ 与全对族 $\mathsf H$ | 定义恒等式（严格） |
| 2 | $\Phi_{n,i}-\Phi_{n,j}=\gamma_n\mathcal H_{ij}$ | 文档 T1（严格） |
| 3 | $K$ 谱侧、留数 $1/\rho_n$ | 数论严格（显式公式） |
| 4 | **识别 $t\equiv\tau_i$** | **构造识别（唯一跳跃）** |
| 5 | DM.25 模差桥梁（逐对）与 §5.1 全对测度、$R_n$ | 代数严格（给定识别） |
| 6 | $\Gamma_n$ 退相干 | 严格（给定 OU） |
| 7 | 锚核内各点 $K$ 等高不等位；全对相干由 $\hat\mu_t$、$R_n$ 读 | 代数严格（给定 DM.25） |
| 8 | 共享的适用范围：核内逐对（$\ell_e=0$ 自动）／单一平台需 $[r]=0$ 且 $c_{ij}=0$ | 判定（条件式，见 §0.1） |

**边界（缺口不升级）**：
- **M9**：DM.25 给出"共享"的结构层，$A_\tau$ 与 $K^{\rm SC}$ 的**数值同一**待独立复现（编号不变）。
- **M10**：DM.25 建立结构桥梁，但不写 $\mathcal I_K=\mathcal H_{ij}$、不宣称振幅物理同一；精确数值映射待独立复现（编号不变）。
- **R30**：DM.25 把节点相位振幅权重定为留数 $1/\rho_n$（谱系数读数），原判决的 $C_n\sim\gamma_n^{+0.45}$ 是导数斜率读数，二者是同一 $K$ 的不同函数；谱系数读数待独立复现（判据保留为历史）。
- **M1**：零点虚部与节点模式频率的物理同一仍是识别，本文不宣称 M1 已证。

---

## 10. 结论

从节点定义出发，**锚—全对 $\mathcal H_{ij}$—$K$** 的结构桥梁可在一条链上贯通：亏角→固有时→T1 相位差→显式公式谱侧→DM.25 逐对模差→全对测度 $\hat\mu_t$、$R_n$→锚核内等高不等位（各点共享谱阶梯与斜率）。全链只用 CQM 已有定义与一个构造识别（固有时同一性），未新增概念、数值、缺口编号；涨落以固有退相干因子自然进入，无需消除。全对平台单一需 $c_{ij}=0\ \forall i<j$（`临-16`、`临-17`），不是锚的推论。未闭合的是数值层（M9/M10/R30 待独立复现），不是结构层——本文不把结构对应写成数值相等，符合"不绕过"红线。
