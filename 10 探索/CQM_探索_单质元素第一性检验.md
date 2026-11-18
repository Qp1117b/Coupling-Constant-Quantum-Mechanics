# CQM 探索：单质元素第一性检验（rev.2：判决 + 自洽修正 + 零模型对照）

> ## ⚠ 状态标注（2026-11-18 更新）：判据①排除已入权威层；其余判决仍待按稳定稿重估
>
> 本文 rev.1/rev.2 的"判决"对象是重构前的 `06 超导/CQM_超导核心理论.md`（判据 ①、DM.5/DM.6/DM.8、W-3′）。当前状态：
>
> 1. **判据①的排除已登记入权威层**：`06 超导` 已按九环节链重构（口径来源 `10 探索/稳定/CQM_二维晶格超导_全链路整合.md` 第十节），其 §0.2「判据①的排除登记」采纳本文对判据①的否证——排除状态就此为权威口径，本稿判据①部分（§三）不再需要重估；
> 2. **DM 定量链（DM.5/DM.6/DM.8、W-3′）的否证结论仍待重估**：重构后权威层保留 DM 公式为【文档显式】框架、定量计算链归 W-3 待推（`06 超导` §0.4、§13 G18）；本文对该定量链的否证保留为探索层判决记录；
> 3. 单质元素路线按用户指示**不再推进**；
> 4. 本文保留为历史记录与可复核脚本索引（脚本与图仍可复核），除判据①排除外不得作为 CQM 定论引用。
>
> 本文内部关于"同步锚"的提法亦须按稳定稿读作：**锚是相变前提，不是相变本身**；相变是稳定同步（稳定稿环节⑨）。

> **定位**：探索稿，非权威源。不改动 `06` 的任何定义、数值与缺口状态。
> **标注**：【文档显式】= 06 原文口径；【代数改写】= 纯代数变形；【本文推导】= 本文新增推理；【构造】= 本文新增假设；【外部】= 外部实验/理论，只作对照；【未证】= 缺口。
> **任务**：把"$T_c$ 第一性主线"放到 19 个单质元素的真实数据上做判决。
> **rev.1（§〇–§九）**：判据 ① 与声子支 $W$-3′+DM.6+DM.8 被否证。
> **rev.2（§3.3、§4.5–4.6、§5.1、§6.1 及 §七–§九修订）**：补上"静态亏角读法""裸 DOS 自洽""强耦合反演""零模型对照"四项修正。结论更严格：**链条即便加上全部可辩护的修正，仍比"令 $T_c$ 为常数"更差**；但同一几何变量 $L$ 配上指数 $-0.2$ 的幂律就把 $R^2$ 提到 0.58——错的是**指数**，不是变量。
> **脚本**：`10 探索/cqm_element_sc/`（`geom2.py`、`g_table.py`、`element_test.py`、`analyze.py`、`figures.py`、`dynamic_range.py`、`eps_req.py`、`final.py`、`final_figure.py`）
> **图**：`figs/element_sc_verdict.png`、`figs/element_lambda_range.png`、`figs/element_chain_vs_null.png`、`figs/element_criterion1_static_deficit.png`

---

## 〇、一页结论

| # | 内容 | 性质 |
|:---|:---|:---|
| 1 | **Regge 几何计算闭合**：$\sum_kA_{ek}=0$ 数值成立到 $10^{-9}$（尺度不变性的直接验证）；体相铰链 $\varepsilon_e\equiv0$。形变张量的无量纲强度 $G\equiv\sum_kA_{ek}^2(l_0/l_k)^2$ 在密堆结构上**近乎普适**：fcc 36.0（89% 铰链）、bcc 42.0（69%）、hcp 36.0（众数） | 正面结果 |
| 2 | **判据 ① 被排除（不是"需要微调"，而是"不可能"）**：① 要求所有材料落在 $\Delta\varepsilon_0\in(r_0,0.1540)$ 这个**宽 1.47 倍**的窗口内；而由几何算出的 $\Delta\varepsilon_0$ 在 19 个元素上跨 **3.09 倍**。$N\ge1$ 时 $T_c^{(1)}$ 对 $N$ 单调递增，故**没有任何 $N$ 能救** | 否证 |
| 3 | **几何输入否证 ① 的定量**：有解的 3 个元素被预言 $T_c=196$ K（Al，实测 1.175）、$1110$ K（Be，实测 0.026）；Hg1201 被预言 1245 K（实测 95）。16/19 个元素因 $\Delta\varepsilon_0<r_0$ 被**禁止超导** | 否证 |
| 4 | **W-3′ + DM.6 + DM.8 被否证**：条纹斜率应为 1，数据给 0.25（律 A）/0.22（律 B）；链条的 $\lambda$ 动态范围 44×/165×，数据只要求 **4.0×**（$\lambda_{\rm req}\in[0.090,0.357]$） | 否证 |
| 5 | **但质量结构是对的**：只有 律 B（$\lambda\propto N_0/(m\theta_D^2)$）给出正的、正确量级的同位素指数 $\alpha_{\rm iso}=1/2$；律 A 给 $\alpha<0$，被直接排除。**（rev.2 修正见 §5.1：加上裸 DOS 自洽后 A 也转正，但过大）** | 正面结果（筛选） |
| 6 | **诊断**：链条的 $\lambda$ 动态范围比数据大 10–40 倍。**任何线性屏蔽（$\mu^*$、$\cos\mathcal H$ 乘子）都修不了**（不改变 40× 的跨度）。所以错的不是缺一项，而是 $\lambda$ 的**函数形式**：真实的 $\lambda$ 必须是**压缩/饱和映射**，数据的有效幂次 $\lambda\propto[N_0/(m\theta_D^2)]^{0.23}$ | 【本文推导】 |
| 7 | **分支重新指派（用 06 自己的话）**：06 §11.12"$\delta_{\rm intrinsic}$：电子结构内禀亏角，来自 Fermi 面几何 frustration（**元素超导体主导**）"。W-3′ 用的是声子诱导的成变，只该管氢化物/光学模支。**rev.2 限定：这是静态亏角，管阈值（DM.32/DM.27），不管 $\lambda$**（§6.1） | 【文档显式】+【本文推导】 |
| 8 | **rev.2：判据 ① 在"静态亏角读法"下仍不成立**。反解所需 $\varepsilon_i=2\pi[1-(\Delta\varepsilon_0/r_0)^2\tanh(\theta_D/2T_c)]$：Al、V、Be 需 $\varepsilon<0$（**超出 $[0,2\pi)$ 定义域**）；其余 16 个需 $\varepsilon$ 落在 $0.22$–$0.82\times2\pi$，且对 $\Delta\varepsilon_0$ 的 1% 误差敏感到 $\varepsilon$ 变 160%——① 退化为每材料一个自由参数的恒等式 | 否证/去预测化 |
| 9 | **rev.2：4× 跨度要求不是反演假象**。Allen–Dynes 反演给 $\lambda\in[0.234,0.990]$（4.24×），BCS 反演给 $[0.090,0.357]$（3.95×），两者 Spearman=1.00。裸 DOS 自洽 $\gamma=\gamma_{\rm bare}(1+\lambda)$ 把链条跨度压成 A 17.6×/B 37.8×，**仍远宽于 4×** | 稳健性检验 |
| 10 | **rev.2：零模型对照（决定性）**。以 $\sqrt{\langle[\ln(T_c^{\rm pred}/T_c^{\rm obs})]^2\rangle}$ 为唯一误差度量（不给额外平移自由度）：常数 $T_c$ ×5.9、$T_c\propto\theta_D^p$ ×4.8、**链条 A ×22.3 / A+裸DOS ×15.5 / B ×163 / B+裸DOS ×105（全部 $R^2<0$）**；而同一变量 $L$ 配自由指数 $-0.20$ 给 ×3.2、$R^2=0.58$ | **否证 + 定位** |

**一句话**：rev.1 关掉了"几何$\to\Delta\varepsilon_0\to$判据①"；rev.2 进一步证明"几何$\to N_0/(m\theta_D^a)\to$DM.8"这条支线也没超过零模型，但**变量 $L$ 是对的、指数错了约 5 倍**——下一轮的靶子是 $\lambda\propto L^{1/5}$ 的第一性来源，而不是再补一个线性项。

---

## 一、数据与流程

### 1.1 输入（全部外部实验值，逐条标源）

| 量 | 来源 | 备注 |
|:---|:---|:---|
| $T_c$ | `06 超导/cqm_analysis/superconductors_deduplicated.csv`（项目自带，40 条单质） | 只取常压、结构确定的 19 个 |
| $\theta_D$（0 K 值） | KnowledgeDoor *Elements Handbook*, "Debye Temperature"（其引用 Kittel, *ISSP* 8th ed.; Stewart, *RSI* **54**, 1 (1983)） | 例：Al 433、Pb 105、Nb 276、Be 1481、W 383 |
| 电子比热系数 $\gamma$ | 同上，"Electronic Heat Capacity Coefficient" | $N_0[{\rm states/eV/atom}]=\gamma[{\rm mJ/mol\,K^2}]/2.3574$（$\gamma=\frac{\pi^2}{3}k_B^2N_0$） |
| 晶格常数 $a$、$c/a$ | CRC 标准值 | fcc/bcc/hcp 三类，共 19 个 |
| 原子质量 $m$ | 标准原子量 | |

**未使用的数据**：Ca 29 K、Li 20 K、S 17 K、P 16 K、Si 8.5 K 等高压相全部剔除（结构与 $\theta_D$ 都变了，不可比）。

### 1.2 链条（全部来自 06）

$$\underbrace{\{\varepsilon_e\}}_{\rm Regge}\xrightarrow[\ A_{ek}\ ]{\rm W\text{-}3'}\Delta\varepsilon_0\xrightarrow[\ \Delta\varepsilon(T)\ ]{\rm DM.8}T_c(\text{DM.6+DM.8})$$

---

## 二、几何：Regge 计算的结果

### 2.1 做法

`geom2.py`：$n^3$ 超胞（$n=4$）→ Delaunay → 只保留顶点全在内部的四面体 → 剔除最小二面角 $<15^\circ$ 的 sliver → 每条铰链检查覆盖度 $\sum_T\theta_e^T/(2\pi)=1$（合法铰链判据）→ 数值差分 $\partial\theta_e^T/\partial\ln l_k$ 汇总到全局边。

### 2.2 三项验证

| 检查 | 结果 |
|:---|:---|
| $\varepsilon_e=2\pi-\sum_T\theta_e^T$ | 合法铰链上 $<10^{-6}$ 度（完美晶体平直） |
| 尺度不变性 $\sum_kA_{ek}=0$ | fcc $4.0\times10^{-9}$、bcc $8.7\times10^{-10}$、sc $2.0\times10^{-8}$、hcp $2.4\times10^{-7}$ |
| sliver 必须剔除 | 不剔除时 $\sum_kA_{ek}$ 可到 $5\times10^2$，$S$ 到 $10^5$；$A_{ek}\propto1/\sin\theta$ 在近退化四面体上发散 |

第三条是一条**方法性警告**：任何直接对理想高对称格子做 Delaunay 再算 $A_{ek}$ 的做法，若不剔除 sliver，会得到纯噪声。本轮全部结果都在剔除后。

### 2.3 $G$ 近乎普适

$$G\equiv\sum_kA_{ek}^2\left(\frac{l_0}{l_k}\right)^2,\qquad \Delta\varepsilon_0^2=\frac{3\hbar(1-f)}{2m\omega_D\,l_0^2}\,G .$$

| 结构 | $G$ 众数（占比） | 少数派 | 样本铰链 |
|:---|:---|:---|:---:|
| fcc | **36.0**（89%） | 80.0（11%） | 130 |
| bcc | **42.0**（69%） | 30.375（31%） | 26 |
| hcp | **36.0**（29%） | 80 / 35.6 / 38.2 | 68 |

**读法**：密堆金属的亏角对形变的敏感度是一个**结构普适数**，$G=36$–$42$。这是一个正面结果：CQM 的几何层在密堆金属里**不提供材料区分度**。所有材料区分只能来自 $m,\theta_D,N_0$。

**代价（也是本轮最重要的一条）**：$G$ 普适 ⟹ $\Delta\varepsilon_0\propto\sqrt{G/(m\theta_D)}$ 只在 $(m\theta_D)^{-1/2}$ 上变。19 个元素上 $\Delta\varepsilon_0\in[0.0444,0.1370]$，跨度 **3.09 倍**。这个数在后面直接杀死判据 ①。

**三角剖分规范的不确定性**：同一结构里 11%（fcc）到 31%（bcc）的铰链因八面体劈分方式不同而给出另一组 $G$（80 或 30.4）。所以 $W$-3′ 的绝对系数有 $\pm\sqrt2$ 的规范不确定性，这是 $W$-3′ 的**固有**缺陷（$A_{ek}$ 依赖辅助剖分），登记为 N-15。

---

## 三、判据 ① 的判决

$$T_c^{(1)}=\frac{\theta_D}{2\,{\rm artanh}\,\Theta},\qquad \Theta=\left(\frac{r_0}{N\Delta\varepsilon_0}\right)^2,\quad r_0=0.1046781 .$$

### 3.1 三条硬事实

**(i) 窗口宽 1.47 倍，材料跨 3.09 倍。**

$$r_0<\Delta\varepsilon_0<r_0/\sqrt{\tanh(1/2)}=0.15399\ \Longrightarrow\ \frac{0.15399}{0.10468}=1.471 .$$

只有落在这条 1.47 倍宽的带子里，① 才有解且 $T_c<\theta_D$。而几何给出的 19 个元素跨 3.09 倍。**带宽比材料跨度窄一半**——① 在结构上就装不下一整类材料。

**(ii) 16/19 个元素被禁止超导。**

$\Delta\varepsilon_0<r_0$（即 $\Theta>1$、${\rm artanh}$ 无定义）的元素：

> Pb, Ir, Nb, Ta, Mo, W, Tc, Ru, Os, Re, Zn, Cd, Tl, Ti, Zr, Hf（16 个）

其中包括 $T_c$ 最高的 Nb（9.25 K）和全部 4d/5d 过渡金属。**若 ① 是必要条件，这些材料不该超导。**

**(iii) 没有 $N$ 能救。**

$N\ge1$（计数）时 $\Theta\propto N^{-2}$ 单调降 ⟹ $T_c^{(1)}$ 对 $N$ **单调递增**。$N=1$ 已经给出了下表这么高的值：

| 材料 | $\Delta\varepsilon_0$ | $T_c^{(1)}$ | $T_c^{\rm obs}$ | 偏差 |
|:---|:---:|:---:|:---:|:---:|
| Al | 0.1169 | 196 K | 1.175 K | $1.7\times10^{2}$ |
| V | 0.1047 | 45.9 K（在 $\Theta=1$ 刀刃上） | 5.4 K | $8.5$ |
| Be | 0.1370 | 1110 K | 0.026 K | $4.3\times10^{4}$ |
| Hg1201（CuO$_2$，$l=1.93$ Å，$\theta_D=350$ K，$m_{\rm red}=12.8$） | 0.280 | 1245 K | 95 K | $13$ |

$N>1$ 只会把这些数字推得更高、并把 (ii) 里的 16 个"解禁"后同样推到 $10^3$–$10^5$ K。**故 ① 作为 $T_c$ 定律被排除，与 $N$ 取值无关。**

### 3.2 这条否证的性质

前稿把 ① 从"主线"降为"必要条件"，理由是"低 $T_c$ 需要 $\Delta\varepsilon_0$ 与 $r_0$ 相符到 $10^{-158}$"。本轮把理由升级为**定量的不可能性**：

> ① 需要 $\Delta\varepsilon_0$ 落在宽 1.47 倍的带内；几何给出 3.09 倍的跨度，且 $G$ 普适意味着没有任何几何自由度能压缩这个跨度（$(m\theta_D)^{-1/2}$ 已经被质量与声子定死）。**不是精度问题，是量程问题。**

![判决图](figs/element_sc_verdict.png)

**图 (a)**：横轴实测、纵轴 ① 预言，虚线为完美线、点线为 $\pm10^2,\pm10^4$。三个点全部落在 $10^2$–$10^4$ 上方。**图 (b)**：$\Delta\varepsilon_0$ 与 $T_c$ 的散点，绿带是 ① 的窗口——$T_c$ 在 $r_0$ 处**没有任何门槛结构**（$T_c$ 从 $1.8\times10^{-5}$ 连续铺到 $6.9\times10^{-2}$，跨过窗口边界毫无变化）。

### 3.3 rev.2：把 $\delta_{\rm intrinsic}$ 当成静态亏角时，① 会怎样（§九 悬案的判决）

§九 留下的问题："若 $\Delta\varepsilon$ 的主控量换成 $\delta_{\rm intrinsic}$，① 需重算。"本节给出结果。

06 §4 明确分家：**静态**部分 $\varepsilon^{(0)}$ 进 DM.27 与资格条件（DM.32），**涨落**部分 $\Delta\varepsilon$ 才进 DM.5。§11.12 的 $\delta_{\rm intrinsic}$ 属于前者。于是 ① 的完整式是

$$\Delta\varepsilon_0\ \ge\ r_0\sqrt{1-\frac{\varepsilon}{2\pi}},\qquad r_0=\frac{\pi ☯}{\ln2}=0.1046781,$$

$$T_c^{(1)}=\frac{\theta_D}{2\,{\rm artanh}\,\Theta},\qquad \Theta=\left(\frac{r_0\sqrt{1-\varepsilon/2\pi}}{\Delta\varepsilon_0}\right)^2 .$$

**反解（【代数改写】）**：给定 $T_c$ 与 $\Delta\varepsilon_0$，① 唯一决定静态亏角

$$\Theta_{\rm req}=\tanh\frac{\theta_D}{2T_c},\qquad
\boxed{\ \varepsilon_{\rm req}=2\pi\left[1-\left(\frac{\Delta\varepsilon_0}{r_0}\right)^2\Theta_{\rm req}\right]\ }$$

| 结果 | 数值 |
|:---|:---|
| $\varepsilon_{\rm req}<0$（**超出 $[0,2\pi)$，被 ① 禁止**） | Al $-1.56$、V $-0.002$、Be $-4.49$ rad（3/19） |
| 其余 16 个的 $\varepsilon_{\rm req}$ | $1.37$–$5.15$ rad $=0.22$–$0.82\times2\pi$ |
| 灵敏度 | $\partial\varepsilon/\partial\Delta\varepsilon_0=-4\pi\Delta\varepsilon_0/r_0^2$，中位数绝对值 $80$；$\Delta\varepsilon_0$ 变 1% ⟹ $\varepsilon_{\rm req}$ 变约 160% |

![静态亏角](figs/element_criterion1_static_deficit.png)

**判决（两层）**：

1. **硬否定**：Al、V、Be 要求 $\varepsilon<0$，而 06 全文把亏角定义为 $[0,2\pi)$（第 43 行、第 419 行 $\varepsilon/(2\pi)<1$）。若该定义域不可放宽，① 在静态亏角读法下仍被这 3 个元素排除——包括 $T_c$ 最高的 V（5.4 K）附近那个"刀刃"点。
2. **去预测化**：对其余 16 个，① 对任何 $T_c$ 都能给出一个 $\varepsilon_{\rm req}\in[0,2\pi)$，因而**不可证伪**；而且所需的 $\varepsilon$ 必须与声子支算出的 $\Delta\varepsilon_0^2$ 精确到 1% 地反向配平（$\varepsilon_{\rm req}$ 几乎就是 $\Delta\varepsilon_0^2$ 的仿射函数）。这不是一个 $T_c$ 定律，而是把 $T_c$ 的信息搬进了 $\delta_{\rm intrinsic}$ 的定义。若要恢复预测力，必须**独立**算出 $\delta_{\rm intrinsic}$（N-16），再检验它是否等于上表的值。

> 与 rev.1 的关系不冲突：rev.1 排除的是"$\varepsilon=0$、$\Delta\varepsilon$ 全由声子涨落给"的读法；本小节排除的是"$\varepsilon$ 可调"的读法。**两种读法下 ① 都不能承担 $T_c$。**

---

## 四、$W$-3′ + DM.6 + DM.8 的判决

$$\lambda=\frac{N_0\,g^2\,z\,\langle w\rangle}{\hbar\omega_D},\qquad \langle w\rangle=\frac{\Delta\varepsilon_0^2}{\Delta\varepsilon_{\rm ref}^2},\qquad \frac{T_c}{\theta_D}=1.13\,e^{-1/\lambda}$$

（$\omega_D=k_B\theta_D/\hbar$；$g$ 是 06 未定义的耦合，只能取两种量纲自洽的假设，见下）

### 4.1 两条候选律

| 律 | $g$ 的假设 | $\lambda$ | 与"标准"对照 |
|:---|:---|:---|:---|
| **A** | $g=\hbar\omega_D$ | $\propto N_0G/(m\theta_D)$ | — |
| **B** | $g=$ 常数能量 | $\propto N_0G/(m\theta_D^2)$ | 与 McMillan $\lambda=N_0\langle I^2\rangle/(M\langle\omega^2\rangle)$ **同构** |

### 4.2 判决

以 $L\equiv\ln(1.13\theta_D/T_c)=1/\lambda$ 为纵轴、$\ln X$ 为横轴（$X=m\theta_D^{a}/(N_0G)$），**理论要求斜率 1**：

| 律 | 拟合斜率 | 要求 | $R^2$ |
|:---|:---:|:---:|:---:|
| A | **0.253** | 1 | 0.55 |
| B | **0.223** | 1 | 0.48 |

动态范围（图 `element_lambda_range.png` 面板 c）：

| 量 | 范围 | 跨度 |
|:---|:---|:---:|
| 数据要求 $\lambda_{\rm req}=1/L$ | $0.090$–$0.357$ | **4.0×** |
| 律 A 的 $\lambda$（均值对齐） | $0.033$–$1.455$ | **44×** |
| 律 B 的 $\lambda$ | $7.5\times10^{-3}$–$1.23$ | **165×** |

![动态范围](figs/element_lambda_range.png)

### 4.3 为什么这不是"再加一项就能修"

设真实耦合为 $\lambda_{\rm net}=F(\lambda_{\rm chain})$。

**先排除最简单的一类**：若 $F$ 是**线性**的（加性 $\lambda-\mu^*$ 或乘性 $c\lambda$、$\cos\mathcal H\cdot\lambda$），则

$$\frac{\lambda_{\rm net}^{\max}}{\lambda_{\rm net}^{\min}}=\frac{\lambda_{\rm chain}^{\max}-\mu^*}{\lambda_{\rm chain}^{\min}-\mu^*}\ \ge\ \frac{1.455}{0.0328}=44\quad(\text{律 A},\ \mu^*\in[0,\lambda^{\min}_{\rm chain}))$$

（$\mu^*\to0$ 取到 44，$\mu^*\to\lambda^{\min}_{\rm chain}$ 时发散。）律 B 同构，43 倍以上。**所以"缺一个 $\mu^*$"这条最省事的路被排除。**

**剩下唯一可能**：$F$ 必须是**压缩（饱和）映射**，把 44 倍压成 4 倍。数据的有效幂次是

$$\lambda\propto X^{0.23\pm0.03},\qquad X\equiv\frac{N_0}{m\theta_D^2},$$

即"耦合是朴素耦合的 $\sim1/4$ 次幂"。$1/4$ 指数不是任何线性屏蔽能给出来的（登记 N-19，机制未证）。

> **注意**：本小节排除的是**线性**修正（$\mu^*$、$\cos\mathcal H$ 乘子），不是"任何修正"。$F$ 非线性是允许的，而这正是数据要求的。


### 4.4 对下一轮模型的硬约束

$$\boxed{\ \lambda\ \text{必须是一个在密堆金属间只起伏 4 倍、取值}\approx0.2\ \text{的饱和函数}\ }$$

这是本轮 rev.1 给出的、可被直接检验的模型约束。**rev.2 的检验结果见 §4.5–§4.6：约束本身没错，但链条改不到那个形式。**

### 4.5 rev.2：两项可辩护的修正（都不是拟合）

**(a) 裸 DOS 自洽（必须做）。** DM.6 的 $N(0)$ 是能带 DOS；而输入表里的 $\gamma$ 是**实验**电子比热系数，已含电声质量重整 $\gamma=\gamma_{\rm bare}(1+\lambda)$（【外部】标准关系：W. L. McMillan, *Phys. Rev.* **167**, 331 (1968), doi:10.1103/PhysRev.167.331）。故

$$N_0^{\rm bare}=\frac{N_0^{\rm exp}}{1+\lambda}\ \Longrightarrow\
\lambda=\frac{C\,N_0^{\rm exp}}{(1+\lambda)\,m\theta_D^{a}}\ \Longleftrightarrow\
\boxed{\ \lambda(1+\lambda)=C\,\frac{N_0^{\rm exp}}{m\theta_D^{a}}\ }$$

大 $\lambda$ 端自动给出 $\lambda\propto L^{1/2}$ 的压缩。链条跨度：A $44\to17.6$、B $165\to37.8$。**方向对，但还差 4–9 倍。**

**(b) 强耦合反演（稳健性检验，不参与定标）。** DM.8 是弱耦合式。用 Allen–Dynes（【外部】$T_c=\omega_{\log}/1.2\exp[-1.04(1+\lambda)/(\lambda-\mu^*(1+0.62\lambda))]$，P. B. Allen & B. I. Dynes, *Phys. Rev. B* **12**, 905 (1975), doi:10.1103/PhysRevB.12.905；取 $\omega_{\log}\to\theta_D$、$\mu^*=0.1$，沿用 M4 的单入口）反演同一批 $T_c$：

| 反演 | 范围 | 跨度 | 与 BCS 反演的 Spearman |
|:---|:---|:---:|:---:|
| BCS：$1/\lambda=\ln(1.13\theta_D/T_c)$ | $[0.090,0.357]$ | 3.95× | 1.00 |
| Allen–Dynes（$\mu^*=0.1$） | $[0.234,0.990]$ | 4.24× | — |

**结论：§4.2 的"数据只要 4×"不是 BCS 反演的假象**，换强耦合公式后跨度几乎不变（3.95→4.24）。作为旁证，AD 反演给 Al 0.372、Zn 0.369、Cd 0.367、Be 0.234、Pb 0.990，与文献 $\lambda_{ep}$（Al≈0.43、Zn≈0.38、Cd≈0.38、Be≈0.24、Pb≈1.5）同量级；差异主要来自把 $\omega_{\log}$ 等同于 $\theta_D$（Pb 尤甚），属 M4 未闭合项。

### 4.6 rev.2：零模型对照——链条连常数 $T_c$ 都打不过

**误差度量必须统一**：取 $r_i=\ln(T_{c,i}^{\rm pred}/T_{c,i}^{\rm obs})$，报 $\exp\sqrt{\langle r^2\rangle}$ 与 $R^2=1-\langle r^2\rangle/{\rm Var}(\ln T_c)$。**不扣均值**——平移就是误差，不能当第二个免费参数（这是 rev.1 的 §4 诊断里容易误算的地方）。每个模型的参数列在表末。

| 模型 | 参数数 | RMS | 最大偏差 | $R^2$ |
|:---|:---:|:---:|:---:|:---:|
| 常数 $T_c$ | 1 | **×5.9** | ×51 | 0 |
| $T_c=a\theta_D$ | 1 | ×8.4 | ×134 | −0.43 |
| $T_c=B\theta_D^{\,p}$（$p=-1.39$） | 2 | ×4.8 | ×43 | 0.22 |
| 链条 A：$1/\lambda=C L$ | 1 | ×22.3 | ×380 | −2.05 |
| 链条 B：$1/\lambda=C L$ | 1 | ×163 | ×1033 | −7.20 |
| 链条 A + 裸 DOS 自洽 | 1 | **×15.5** | ×229 | −1.37 |
| 链条 B + 裸 DOS 自洽 | 1 | ×105 | ×611 | −5.84 |
| 同一 $L$，自由幂律 A：$1/\lambda\propto L^{-0.30}$ | 2 | ×4.0 | ×13 | 0.39 |
| 同一 $L$，自由幂律 B：$1/\lambda\propto L^{-0.20}$ | 2 | **×3.2** | ×8.5 | **0.58** |

![零模型对照](figs/element_chain_vs_null.png)

**读法（这是本轮最硬的一条）**：

1. 四种链条变体的 $R^2$ **全部为负**——比"所有材料都取同一个 $T_c$"还差。外加裸 DOS 自洽把 A 从 ×22 改到 ×15.5，是**改善**，但仍未越过零模型（×5.9）这条线。
2. 然而**变量本身不是垃圾**：把指数从链条的 $+1$ 改成 $-0.20$（等价地 $\lambda\propto L^{0.20}$），同样的 $L$、同样的单常数结构，$R^2$ 跳到 0.58。_rank_ 上链条 A 与数据要求的 $\lambda$ 的 Spearman 也有 0.62（律 B 0.72）。
3. 所以判决要改写：不是"几何变量与该材料无关"，而是 **$\lambda$ 对几何变量的幂次错约 5 倍**（$1$ vs $0.2$）。§4.3 的"线性屏蔽修不了"由此得到最终确认：线性变换不改变幂次。

**新增硬约束（替代 §4.4 的定性说法）**：

$$\boxed{\ \lambda\ \propto\ \left[\frac{N_0}{m\theta_D^2}\right]^{0.20\pm0.03}\quad\text{且需在 }L\text{ 的整个 165× 跨度上成立}\ }$$

这是可被下一轮模型直接检验的定量靶子。指数 $1/5$ 的第一性来源未证（N-19 升级）。

---

## 五、正面收获：同位素指数把两条律筛掉一条

$\theta_D\propto m^{-1/2}$（同一材料改变同位素时晶格常数与力常数基本不动，$\omega_D\propto M^{-1/2}$）。记 $\alpha_{\rm iso}\equiv-d\ln T_c/d\ln m$：

$$\ln T_c=\ln\theta_D-\frac1\lambda\ \Longrightarrow\ \alpha_{\rm iso}=\frac12-\frac1\lambda\frac{d\ln\lambda}{d\ln m}$$

| 律 | $d\ln\lambda/d\ln m$ | $\alpha_{\rm iso}$ | 判定 |
|:---|:---:|:---:|:---|
| A | $-1/2$ | $-\tfrac12-\tfrac{1}{2\lambda}$（$\approx-3.5$ 于 $\lambda=0.17$） | **负值，直接排除**（同位素效应必为正：轻同位素 $T_c$ 高） |
| B | $0$ | $+1/2$ | **正确量级**（BCS 亦为 $1/2$；实测元素 $0.2$–$0.5$，Ru 近 0） |

**结论**：$W$-3′ 与 DM.6 的**质量结构**（$1/(m\theta_D^2)$）是对的，错的是**强度与随材料的起伏**。这排除了"把 $W$-3′ 整个丢掉"这条偷懒路线，也把下一轮的靶子收窄到"$\lambda$ 的饱和机制"。

> 注意：这是【外部】事实（$\theta_D\propto m^{-1/2}$、$\alpha_{\rm iso}>0$）与【代数改写】的合用，不是新假设。

### 5.1 rev.2：裸 DOS 自洽把律 A 的同位素指数也转正了

加上 $\lambda(1+\lambda)=C N_0/(m\theta_D^a)$ 后，沿同位素变化 $\theta_D\propto m^{-1/2}$ 使 $m\theta_D^a\propto m^{1-a/2}$：

$$\frac{d\ln\lambda}{d\ln m}\bigg|_{\rm iso}=-\frac{1-a/2}{1+2\lambda},\qquad
\alpha_{\rm iso}=\frac12+\frac{1-a/2}{\lambda(1+2\lambda)} .$$

| 律 | $a$ | 裸 DOS 修正后的 $\alpha_{\rm iso}$ | 判定 |
|:---|:---:|:---|:---|
| A | 1 | $\tfrac12+\tfrac{1}{2\lambda(1+2\lambda)}\approx1.19$（$\lambda=0.4$） | 由负转正，但**过大**（实测多为 $0.2$–$0.5$） |
| B | 2 | $1/2$（精确） | **仍最贴近实测** |

**结论不变**：律 B 的质量结构仍是最优选择；律 A 只是从"符号错"降格为"数值错"。注意 $\S4.6$ 的 $R^2$ 表说明**最优质量结构与最优 $T_c$ 拟合并不落在同一支上**（B 的秩相关 0.72 高于 A 的 0.62，但 B 的 $R^2$ 更负）——这本身就是一个信号：链条缺的不是"选 A 还是选 B"，而是共同的幂次。

---

## 六、分支重新指派：元素支不是声子支

06 §11.12：

> $\delta_{\rm intrinsic}$：电子结构内禀亏角，来自 Fermi 面几何 frustration（**元素超导体主导**）

这句话与本轮数值判决**互相印证**：

1. $W$-3′ 的输入是**声子诱导的键长涨落** $\langle\delta l^2\rangle$，它给出的是"零点的、长波的、化学盲的"涨落——这正是 $G$ 普适的成因；
2. 元素超导体的 $\lambda$ 却明显带有**化学**特征：按 $\lambda_{\rm req}$ 排，V/Nb/Ta（多片复杂 Fermi 面）与 Pb/Tl 偏高，Be/Os/Re/W/Zn（近自由电子或强共价）偏低；
3. 所以对元素而言，配对通道的**主导项是 $\delta_{\rm intrinsic}$（电子）**，声子项只是修正。$W$-3′ 是氢化物/光学模支（06 §11.12 的 intra/inter $\approx6$–$12$ 倍）的正确工具，不是元素支的。

**这不是为失败找台阶，而是判决本身指向 06 已有的分支。** 登记为：元素支的主控量是 $\delta_{\rm intrinsic}$，$W$-3′ 降为元素支的次级修正。

### 6.1 rev.2 重要限定：$\delta_{\rm intrinsic}$ 管的是阈值，不是 $\lambda$

上面的第 3 句写得过强，必须按 06 §4 收窄：

- $\delta_{\rm intrinsic}$ 是**静态**亏角 $\varepsilon^{(0)}$，入口是 DM.27（$d\tau/dt=\sqrt{1-\varepsilon/2\pi}$）与资格条件 DM.32（$\Delta\varepsilon_0\ge\pi ☯\sqrt{1-\varepsilon/2\pi}/\ln n$）；
- $\lambda$ 的入口是**涨落** $\Delta\varepsilon_0$ 经 DM.6/DM.8（§4）。两者不是同一个量，也不能互相替代。

所以 rev.1 说"元素支主控量是 $\delta_{\rm intrinsic}$"应读作：**元素支的阈值/资格由 $\delta_{\rm intrinsic}$ 主控**；$\lambda$ 仍由 DM.6 的涨落结构承担，而 §4.6 证明这条支线目前不成立。§3.3 的反解正是把这两条入口接起来后得到的结论：① 要求 $\delta_{\rm intrinsic}$ 与 $\Delta\varepsilon_0$ 反向配平到 1%，故**把 $\lambda$ 的失败归咎于"没算 $\delta_{\rm intrinsic}$"是错误的推理**。

---

## 七、下一轮的具体推导目标（rev.2 重排）

> **重排理由**：rev.1 把"$\delta_{\rm intrinsic}$ 的 Fermi 面角亏定义"列为首要目标。rev.2 证明它是**静态阈值量**（§6.1），而 ① 即便在静态读法下也不能承担 $T_c$（§3.3）。因此降为次要；首要目标改为**§4.6 定量定位的幂次缺口**。

### 7.1【首要】$\lambda\propto L^{1/5}$ 的第一性来源（N-19 升级）

目标不是再拟合指数，而是从 CQM 已有结构推出它。已经排除的路：

- 线性屏蔽（$\mu^*$ 加性、$\cos\mathcal H$ 乘性）不改变幂次（§4.3）；
- 裸 DOS 自洽 $\lambda(1+\lambda)=CL$ 只给 $L^{1/2}$ 的渐近压缩，跨度仍 17.6×/37.8×（§4.5），且 $R^2$ 仍为负（§4.6）。

**待查的候选方向（均为【提案】，未证，不得当作结论）**：

1. 多重自洽链：若 DOS 重整与耦合重整各贡献一个 $(1+\lambda)$ 因子，$\lambda(1+\lambda)^3=CL$ 的大 $\lambda$ 端会给 $L^{1/4}$；需说明两个重整因子在 CQM 中确实不同源，否则是数字游戏。
2. 差异方差 $\langle(\delta C_{ij})^2\rangle$ 的空间关联：DM.5 的方差在强关联极限会因近邻抵消而饱和，可能给出分数幂；需从 Regge 图的谱性质推出指数。
3. $J$ 的几何平均（② 的 $J$ 与 DM.1 同源）若进入 $\lambda$，会引入另一个无量纲比值的幂次。

**最低验收标准**：在 §4.6 的同一张表上，$R^2>0.22$（超过两参数纯 $\theta_D$ 幂律）且 RMS < ×4.8，否则不算推进。

### 7.2【次要】$\delta_{\rm intrinsic}$ 的几何定义（N-16 降级但保留）

候选（需推导+数值，不是结论）：把 Fermi 面当闭合分片曲面 $\Sigma_F$，角亏测度满足 Gauss–Bonnet $\int\mu_F=4\pi$，分布由形状定：

$$\varepsilon^{\rm intr}_i=2\pi-\sum_{f\ni i}\theta_i^f,\qquad \sum_i\varepsilon_i^{\rm intr}=4\pi .$$

**用途已改变**：它不再用来解释 $\lambda$，而是用来检验 §3.3 反解的 $\varepsilon_i^{\rm req}$ 是否可由几何独立给出。若算出的 $\varepsilon_i$ 与 $\varepsilon_i^{\rm req}$ 相差大于约 1%，① 即被最终排除。计算入口：`06 超导/cqm_analysis/data_raw/3DSC_MP.csv` 的 `dos_2`/`band_structure_2` 列（内容未核查），或外部 Fermi 面数据。

### 7.3【并行·唯一未否证】单层 CuO₂ 的 ② 支

单层 CuO₂ 走 ②（2D BKT，$k_BT_{\rm BKT}=0.89290J$）不受 ① 与 §4.6 否证的影响，只需 $J$ 的第一性来源。本轮之后优先级升至与 7.1 并列。

---

## 八、缺口台账更新

| 编号 | 内容 | 状态变化 |
|:---|:---|:---|
| ① | $\Delta u_G<\ln4$ 作为 $T_c$ 判据 | **两种读法均不能承担 $T_c$**：$\varepsilon=0$ 读法量程 1.47× vs 材料 3.09×、$N$ 单调性、16/19 禁止（rev.1）；静态亏角读法下 Al/V/Be 需 $\varepsilon<0$，其余 16 个退化为 1% 配平的恒等式（rev.2，§3.3）。降为"资格条件"，不承担定量 |
| W-3′ | 声子诱导亏角涨落 | **形式保留、元素支降为次级**；$G$ 已算出（36–42），$\sum A_{ek}=0$ 已验证 |
| DM.6+DM.8 | 几何 $\to\lambda\to T_c$ 支 | **rev.2 否证**：四种变体 $R^2<0$，全部劣于常数 $T_c$（§4.6）；变量 $L$ 有效但指数错约 5× |
| M3 | $N_i(0)$ 映射 | 仍开；rev.1 证明它补不了 40× 跨度；rev.2 证明裸 DOS 自洽也补不了 |
| M4 | $\omega_i=\Omega_0$ | 保留（$\theta_D$ 单入口）；Allen–Dynes 对照中 $\omega_{\log}\to\theta_D$ 是主要系统差（Pb 尤甚） |
| N-15 | $A_{ek}$ 的三角剖分规范依赖 | 11%–31% 铰链给另一组 $G$，$\pm\sqrt2$ |
| N-16 | $\delta_{\rm intrinsic}$ 的 Fermi 面角亏定义与数值 | **降级为次要**：只用于检验 §3.3 反解的 $\varepsilon_i^{\rm req}$，不解释 $\lambda$ |
| N-17 | 角亏测度上界 $2\pi$ 给出的 $\lambda$ 饱和 | **撤销**：上界不能解释幂次 $1/5$，也不能把 $R^2$ 抬到 0 以上 |
| N-18 | 判据 ① 的替代：谁能承担 $T_c$ 的绝对值 | 仍开：只剩 DM.8 支（$J_0$ 外生，Z2）与 ② 支；§4.6 表明 DM.8 支当前不成立 |
| N-19 | $\lambda\propto L^{1/5}$ 的幂次来源 | **升级为首要**（未证）：需给出 $1/5$ 的第一性推导，验收线 $R^2>0.22$、RMS<×4.8（§7.1） |
| N-20 | 轨道特征/矩阵元的缺失自由度 | **新增**：残差按 d 带填充组织（图 b），而 $G,m,\theta_D,N_0$ 全无 $l$ 波信息；CQM 内部尚无对应量 |
| N-21 | 裸 DOS 自洽 $\gamma=\gamma_{\rm bare}(1+\lambda)$ | **新增·已采纳**：把 $\lambda(1+\lambda)=CL$ 作为链条的必要修正；仍不足（§4.5） |

---

## 九、边界与未证

- $\theta_D$ 用 0 K Debye 温度，DM.8 的 $\omega_i$ 是否就是它，属 M4 的单一识别，未证。
- $\gamma\to N_0$ 的换算用 $\gamma=\frac{\pi^2}{3}k_B^2N_0$（自由电子形式）。实验 $\gamma$ 已含电声增强；rev.2 已按 $\gamma=\gamma_{\rm bare}(1+\lambda)$ 做自洽修正（§4.5(a)），但 $\lambda$ 本身也是待定量，故修正只闭合到二次方程层次。
- 19 个元素里 La（fcc/dhcp 两相）、Sn/In（四方）、Hg/Bi（菱方）因结构非简单 Bravais 未入表，$G$ 只在 fcc/bcc/hcp 上算过。
- $f=1/2$ 是取定值；$f$ 只整体重标 $\Delta\varepsilon_0$，被 $\lambda$ 的归一化吸收，不影响 §三、§四 的**跨度**结论。
- 判据 ① 的两种读法在 rev.1（$\varepsilon=0$）与 rev.2 §3.3（$\varepsilon$ 可调）下均已判决；后者仍有"$\varepsilon$ 是否允许为负"这一定义域问题（06 全文取 $[0,2\pi)$，故按禁止处理）。
- $\mu^*=0.1$ 只是 Allen–Dynes 对照的一个代表值；§4.6 的主判决完全不依赖它。$\omega_{\log}\to\theta_D$ 的识别属 M4，未证。
- 误差度量采用 $\sqrt{\langle r^2\rangle}$ 且**不扣残差均值**；若允许一个自由平移，链条 A+裸DOS 可"改善"到 ×9.5，但仍劣于常数模型 ×5.9，故主判决不变。
- 两轮均**没有**修改 `06`、`08`、Lean 与网站。

---

## 附录 A：19 个单质元素输入与中间量

$T_c$ 取自 `superconductors_deduplicated.csv`；$\theta_D$（0 K）与 $\gamma$ 取自 KnowledgeDoor Elements Handbook（引 Kittel *ISSP* 8th ed.、Stewart *RSI* 54, 1 (1983)）；$N_0=\gamma/2.3574$；$G$ 由 `g_table.py` 的 Regge 计算给出；$\Delta\varepsilon_0$ 由 $W$-3′（$f=1/2$）；$L=1/\lambda_{\rm req}=\ln(1.13\theta_D/T_c)$。

| 元素 | 结构 | $T_c$ (K) | $\theta_D$ (K) | $m$ (amu) | $N_0$ | $G$ | $\Delta\varepsilon_0$ | $L$ | $\lambda_{\rm req}$ |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Al | fcc | 1.175 | 433 | 26.98 | 0.573 | 36 | 0.1169 | 6.03 | 0.166 |
| Pb | fcc | 7.196 | 105 | 207.2 | 1.268 | 36 | 0.0701 | 2.80 | 0.357 |
| Ir | fcc | 0.112 | 420 | 192.2 | 1.332 | 36 | 0.0469 | 8.35 | 0.120 |
| Nb | bcc | 9.25 | 276 | 92.91 | 3.309 | 42 | 0.0854 | 3.52 | 0.284 |
| V | bcc | 5.40 | 399 | 50.94 | 4.200 | 42 | 0.1047 | 4.42 | 0.226 |
| Ta | bcc | 4.47 | 246 | 180.9 | 2.490 | 42 | 0.0647 | 4.13 | 0.242 |
| Mo | bcc | 0.915 | 423 | 95.95 | 0.776 | 42 | 0.0712 | 6.26 | 0.160 |
| W | bcc | 0.0154 | 383 | 183.8 | 0.428 | 42 | 0.0537 | 10.24 | 0.098 |
| Tc | hcp | 7.80 | 454 | 98.0 | 1.824 | 36 | 0.0627 | 4.19 | 0.239 |
| Ru | hcp | 0.49 | 555 | 101.1 | 1.315 | 36 | 0.0565 | 7.15 | 0.140 |
| Os | hcp | 0.66 | 467 | 190.2 | 0.870 | 36 | 0.0444 | 6.68 | 0.150 |
| Re | hcp | 1.70 | 416 | 186.2 | 0.971 | 36 | 0.0471 | 5.62 | 0.178 |
| Zn | hcp | 0.85 | 329 | 65.38 | 0.271 | 36 | 0.0926 | 6.08 | 0.164 |
| Cd | hcp | 0.52 | 210 | 112.4 | 0.291 | 36 | 0.0791 | 6.12 | 0.163 |
| Tl | hcp | 2.38 | 78.5 | 204.4 | 0.624 | 36 | 0.0827 | 3.62 | 0.276 |
| Ti | hcp | 0.40 | 420 | 47.87 | 1.425 | 36 | 0.0865 | 7.08 | 0.141 |
| Zr | hcp | 0.61 | 290 | 91.22 | 1.175 | 36 | 0.0689 | 6.29 | 0.159 |
| Hf | hcp | 0.128 | 252 | 178.5 | 0.912 | 36 | 0.0534 | 7.71 | 0.130 |
| Be | hcp | 0.026 | 1481 | 9.012 | 0.073 | 36 | 0.1370 | 11.07 | 0.090 |

**极值**：$\Delta\varepsilon_0\in[0.0444,\,0.1370]$（3.09×）；$\lambda_{\rm req}\in[0.090,\,0.357]$（4.0×）；$T_c/\theta_D\in[1.76\times10^{-5},\,6.85\times10^{-2}]$（$3.9\times10^3$）。
