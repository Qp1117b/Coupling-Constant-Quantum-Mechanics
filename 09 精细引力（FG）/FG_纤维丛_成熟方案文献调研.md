# CQM 实现方案文献调研：Regge 底空间与纤维丛的成熟数学物理方案借用研究

> 调研性质：文献调研与实现方案分析（2026-09-01）。
> 调研范围：`FG_纤维丛理论.md`、`FG_核心理论.md`、`CQM_核心_集成理论.md`、`CQM_核心_朗兰兹分层共振与谱量子.md`、`CQM_核心_因果网络同步理论.md` 中"Regge 底空间 + 纤维丛"相关内容的全部需求，以及外部成熟框架文献（格点规范理论、Regge 计算、离散外微积分、因果动力三角剖分、转移矩阵方法、离散几何与自守形式桥接理论）。
> 核心结论先行：**"离散底空间 + 纤维丛"的物理实现与数学形式化均有成熟方案可借；"离散几何 → 自守形式 / L 函数"的通用通道在文献中不存在，该步仍是 CQM 必须自行构造的部分（与项目文档既有诚实标注一致）。**

---

## 1. 执行摘要

本报告针对"Regge 底空间 + 纤维丛需要自行探索、目前没有成熟方案"这一判断开展文献核查，得到四条核心结论：

1. **"纤维丛在离散底空间上"的标准物理实现早已存在，即格点规范理论（lattice gauge theory，Wilson 1974）**。格点规范理论本质上就是"以图/胞腔复形为底空间、以链接上的群元素为离散平行输运（离散联络）、以面（plaquette）乘积为离散曲率、以 Wilson 圈为和乐"的框架 [cite:1]。它与 `FG_纤维丛理论.md` §6 中"顶点 = 离散点、边 = 联络离散化、面 = 曲率离散化"的对应关系逐项吻合。将规范场放在**三角剖分对偶图**的链接上是动力三角剖分文献的标准做法，已有 U(1) 与 SU(2) 规范场在二维因果动力三角剖分上的完整构造与蒙特卡洛实现 [cite:10]。
2. **离散纤维丛的数学形式化在 2024 年达到可用程度**：Braune、Tong、Gay-Balmaz、Desbrun 的"丛值形式的离散外微积分"（Discrete Exterior Calculus of Bundle-valued Forms, arXiv:2406.05383）在组合流形上定义了带联络的向量丛值形式的离散外协变导数、离散曲率形式与离散 Bianchi 恒等式，并证明了网格细化下的数值收敛性 [cite:8]。这直接形式化 `FG_纤维丛理论.md` §3 的 $F_\ell=d\mathcal{A}_\ell+\mathcal{A}_\ell\wedge\mathcal{A}_\ell$ 与 $DF=0\iff$ Jacobi 恒等式。
3. **CQM 的和乐公式与 Regge 计算的标准定理一致**：`FG_纤维丛理论.md` §3.1 的 $W_v^{(\ell)}=\exp(i\delta_v^{(\ell)}\hat T_\ell)$ 恰好对应 Regge 计算中的标准结果——绕铰链（hinge）平行输运的和乐是绕固定轴、转角等于角亏（deficit angle）的旋转 [cite:13][cite:14]。即 CQM 的"一个联络生成两种曲率"中的底空间一侧，站在成熟定理之上。
4. **"Regge 复形 → 自守形式 / L 函数"没有通用成熟方案**：所有成熟的桥（theta 级数、Epstein zeta 函数、Eichler–Shimura 理论、Farey 三角剖分、Ihara zeta 函数）都要求底空间带算术结构（整格点、正定二次型、算术群作用等），一般单纯复形不具备 [cite:20][cite:22][cite:25][cite:28]。文献调研**确认不存在**"非算术流形的组合三角剖分 → 伽罗瓦表示/自守形式"的定理。此外存在一个对 CQM 有实质警示意义的成熟反例：Epstein zeta 函数的零点一般**不**全部位于临界线（Davenport–Heilbronn 型结果），即"格点型 zeta 函数自动满足黎曼猜想式结论"不成立 [cite:20]。

据此，第 12 节给出四阶段借用路线：阶段一（离散形式实现）、阶段二（谱实现）、阶段三（规范重组与超导计算链）基本可直接借用成熟框架；阶段四（算术通道）必须 CQM 自建，但可借用 theta 级数、Epstein zeta 函数、Farey 三角剖分等成熟构件。

---

## 2. CQM 对成熟方案的具体需求（源自项目文档）

### 2.1 需要实现的对象

依据 `FG_纤维丛理论.md` 与 `FG_核心理论.md`，需要落地的核心对象为纤维丛四元组

$$(M_\ell,\; P(M_\ell, G_\ell),\; \mathcal{A}_\ell,\; \hat{\mathcal{S}}_\ell)$$

及其配套结构：

| 对象 | 文档定义 | 出处 |
|---|---|---|
| Regge 底空间 $M_\ell$ | 层级 $\ell$ 物质分布几何的 Regge 剖分：顶点、边、面/4-单纯形；角亏 $\delta_v=2\pi-\sum_{\Delta\ni v}\theta_v^{(\Delta)}$ | `FG_纤维丛理论.md` §2、§6 |
| 主丛 $P(M_\ell,G_\ell)$ | 结构群按层级取值：元素FG 为 $U(1)\times SO(2)\times SU(4)$，分子FG 为分子点群，晶胞FG 为空间群 | `FG_核心理论.md` §6.1 |
| 联络 $\mathcal{A}_\ell$ | "由层级 Regge 晶胞分步生成"；同一条联络生成两种曲率：底空间角亏 $\delta_v^{(\ell)}$ 与伴丛曲率 $F_\ell=d\mathcal{A}_\ell+\mathcal{A}_\ell\wedge\mathcal{A}_\ell$ | `FG_纤维丛理论.md` §3 |
| 和乐 | $W_v^{(\ell)}=\exp(i\delta_v^{(\ell)}\hat T_\ell)\in G_\ell$ | `FG_纤维丛理论.md` §3.1 |
| 伴丛与运动方程 | $\mathrm{ad}(P)=P\times_{G_\ell}\mathfrak g_\ell\to M_\ell$，$D*F=*J_\Phi$，$DF=0\iff$ Jacobi | `FG_纤维丛理论.md` §3.3 |
| 同步算符 | $\hat{\mathcal{S}}_k^{\rm(full)}=\frac{L_u}{2\pi C}\sqrt{1-\beta\hat\delta_v^{(k)}}\,\hat{\mathbb I}_{G_k}+\hat C_2(G_k)$，要求 $\hat{\mathcal S}=\hat{\mathcal S}^\dagger$ | `FG_核心理论.md` §4.3 |
| 约束框架 | $R$（约束产物），本征群 $R_k$ 是约束产物 | `FG_纤维丛理论.md` §1.5 |
| QG 层 | $\hat{\mathcal{S}}_0:\mathcal H_{\rm auto}(GL_5)\to\mathcal H_{\rm phys}(SU(5))$，Regge 底空间几何约束自守形式（非唯一），自守形式确定 L 函数 | `CQM_核心_朗兰兹分层共振与谱量子.md` §0.5 |
| 超导计算链 | 候选群族 $\mathcal G=\{U(1)/\mathbb Z_n\}$、角亏资格条件、自由能交叉 $F_1(T_c)=F_2(T_c)$ | `CQM_核心_因果网络同步理论.md` §6.1 |

### 2.2 文档自我标注的缺口（与本次调研直接相关）

- "Regge 底空间几何约束（非唯一）"——底空间不能唯一确定自守形式（`CQM_核心_朗兰兹分层共振与谱量子.md` §0.5）；
- "从物质自组织到 GL(5) 基态自守形式的第一性原理推导尚未建立（朗兰兹对应一般 $n$ 情形未证明）"（`CQM_核心_因果网络同步理论.md` §7.2）；
- FG 因果约束为假设；$\beta$ 定值计算待完成；壳层结构由 SU(5) Dynkin图深度严格推导（`FG_核心理论.md` §3.1、§5.1.1）；
- 紧化约束方程 $\mathcal C_k(\lambda_{\rm phys},\gamma_n^{(k)})=0$ 的严格构造缺失（`CQM_核心_因果网络同步理论.md` §7.2）；
- GRH(GL(4))、GRH(GL(5)) 未证明（`FG_核心理论.md` §5.3）。

这些缺口决定了借用方案的边界：成熟框架能覆盖"离散底空间上的主丛/联络/曲率/和乐/谱算符/破缺/数值"全部物理实现层，但**不能**覆盖算术层（自守形式、L 函数零点、紧化约束）。

---

## 3. 成熟方案一：格点规范理论——离散纤维丛的标准物理实现

Wilson 1974 年提出的格点规范理论（"Confinement of Quarks", Physical Review D 10, 2445）是"规范理论 + 离散底空间"的标准框架 [cite:1]。其数学结构为：

- **底空间**：离散图/超立方格点（或更一般的胞腔复形）；
- **离散联络**：每条链接（link）上放群元素 $U_\ell\in G$，即离散平行输运算子；
- **离散曲率**：每个面（plaquette）上链接变量有序乘积 $U_p=\prod_{\ell\in\partial p}U_\ell$ 的和乐；
- **作用量**：Wilson 作用量 $S=\sum_p \mathrm{Re}\,\mathrm{Tr}\,U_p$；
- **规范不变观测**：Wilson 圈 $W[C]=\mathrm{Tr}\prod_{\ell\in C}U_\ell$（沿闭合回路 $C$ 的和乐）。

从数学观点看，这正是主 $G$ 丛及其联络在离散底空间上的离散化：链接变量是离散联络，面和乐是离散曲率，规范变换是顶点处的群作用。数学侧的严格化（Yang–Mills 测度、和乐映射的随机矩阵模型化）由 Sengupta、Driver、Lévy 等发展，近年仍有新进展（如格点 Yang–Mills 模型到曲面 Yang–Mills 测度的普适标度极限 [cite:19]）。

**成熟度**：五十年历史、格点量子色动力学（lattice quantum chromodynamics）已达到 FLAG 评述级的亚百分比精度 [cite:18]。这是本报告中成熟度最高的框架。

**与 CQM 的对应**：`FG_纤维丛理论.md` §6 的"边 = 联络 $\mathcal A_\ell$ 的离散化、面 = 曲率 $\mathcal F_\ell$ 的离散化"与格点规范理论的"链接变量/面和乐"逐项对应；CQM 的和乐 $W_v^{(\ell)}$ 对应 Wilson 圈类型的可观测量。

**缺口**：标准格点规范理论在规则格点上表述，底空间不是三角剖分（需第 4 节的对偶图构造适配）；不含任何算术/L 函数结构；"约束框架（$R$ 是约束产物）"是 CQM 自有概念，格点文献中无对应理论。

---

## 4. 成熟方案二：三角剖分上的规范场——Regge 计算与动力三角剖分

这是与"Regge 底空间 + 纤维丛"字面最贴合的方向，文献分布如下。

### 4.1 Regge 计算本体

Regge 计算（Regge calculus，1961 年提出）以单纯形格点逼近时空：边长为基本变量，曲率集中于余维 2 的铰链（hinge），铰链角亏 $\delta_h=2\pi-\sum\theta$ 为离散曲率，Regge 作用量 $\sum_h\delta_h A_h$ 模仿爱因斯坦–希尔伯特作用量 [cite:2][cite:15]。现代数值分析对 Regge 曲率定义与收敛性有系统研究 [cite:15]。量子化方向（量子 Regge 计算）以 Roček–Williams 1981 为早期代表 [cite:2]；Hamber–Williams 系统研究了单纯形引力的规范不变性（局域微分同胚不变性在格点上的实现）[cite:3]，以及在格点上计算牛顿势的 Wilson 线方法 [cite:4]。Barrett–Roček–Williams（1999）还建立了 Regge 计算与面积变量的联系 [cite:12]。

### 4.2 规范场放在三角剖分对偶图上（关键成熟构造）

Candido、Clemente、D'Elia、Rottoli（2020）给出了杨–米尔斯理论在动力三角剖分上的紧致（compact）离散化：**规范场生活在与三角剖分相关联的对偶图的链接上**，并完成了 U(1) 与 SU(2) 规范场与二维因果动力三角剖分耦合的马尔可夫链蒙特卡洛实现，发表于 Journal of High Energy Physics 04 (2021) 184 [cite:10]。该文还研究了和乐（torelon）观测、绕数与拓扑极化率等规范观测。

这一构造正是"Regge 型底空间 + 纤维丛"的现成结合方式：几何自由度在三角剖分上（边长/面积/角亏），规范自由度在对偶图链接上（群元素），两者通过最小耦合相互作用。

### 4.3 定理级事实：绕铰链和乐 = 角亏转角

这是本次调研中对 CQM 最有价值的成熟结果：

- "The spin connection of twisted geometry"（2013 年预印本）证明：若扭曲几何为 Regge 型，则绕链接 $l$ 的和乐 $U_l$ 是绕轴 $e^i(l)$、**转角等于 Regge 角亏**的旋转 [cite:13]；
- "Contracted Bianchi Identity and Angle Relation on n-dimensional Simplicial Complex of Regge Calculus"（arXiv:1807.11420）证明：四维欧氏 Regge 引力中，绕单个铰链的和乐全部是纯旋转，且二面角关系就是单纯复形上的收缩 Bianchi 恒等式 [cite:14]。

也就是说，`FG_纤维丛理论.md` §3.1 的 $W_v^{(\ell)}=\exp(i\delta_v^{(\ell)}\hat T_\ell)$ 在"结构群 = 自旋/旋转群"时是 Regge 计算的标准定理。CQM 的特殊之处是把和乐放进**物质结构群** $G_\ell$（如元素FG 的 $U(1)\times SO(2)\times SU(4)$），这相当于把格点规范理论的链接变量（第 3 节）与 Regge 铰链几何（本节）结合：两个成分各自成熟，其结合在动力三角剖分耦合规范场方向已有二维先例 [cite:10]，四维尚不成熟。

### 4.4 因果动力三角剖分

因果动力三角剖分（Causal Dynamical Triangulations，CDT）由 Ambjørn 与 Loll 提出（1998 年, Nuclear Physics B 536, 407），通过带因果叶状结构的三角剖分路径积分构造非微扰洛伦兹量子引力，能从离散量子几何中重现宏观四维时空 [cite:9]。CDT 与规范场的耦合即上述 4.2 的构造 [cite:10]；CDT 的谱分析（有限元方法）亦有专门研究。CDT 为 CQM "退相干 → 4-单纯形" 的动态几何一侧提供了成熟的路径积分机制。

**缺口**：规范场耦合目前仅二维成熟；SU(5) 型大统一规范理论在三角剖分上无现成处理；CDT 的底层几何是各向同性单纯形剖分而非"物质晶胞分布"的层级剖分——后者是 CQM 特有的输入。

---

## 5. 成熟方案三：离散外微积分与丛值形式——离散纤维丛的数学形式化

物理侧（格点规范理论）之外，数学侧的严格形式化由离散微分几何（discrete differential geometry）提供：

- **离散外微积分**（Discrete Exterior Calculus，DEC）：Hirani 2003 年博士论文奠定框架，将微分形式离散化为单纯复形上的上链（cochain），离散外微分由拓扑边界对偶定义，保证离散 Stokes 定理严格成立，配合 Whitney 形式与离散 Hodge 星实现插值与对偶 [cite:5]；Desbrun–Kanso–Tong 2006 年的系统论述覆盖离散曲率、联络、平行输运 [cite:6]。
- **有限元外微积分**（Finite Element Exterior Calculus，FEEC）：Arnold–Falk–Winther 将上述结构组织为离散 de Rham 复形，并证明与连续椭圆复形的相容性与数值稳定性定理 [cite:7]。
- **丛值形式的离散外微积分**（2024 年关键进展）：Braune、Tong、Gay-Balmaz、Desbrun 提出组合流形上带联络向量丛值形式的离散化，定义离散外协变导数，证明离散 Bianchi 恒等式在单纯形胞腔上成立，且在温和条件下网格细化时收敛到精确值（此前尝试做不到）[cite:8]。

第三项正是"离散底空间上的纤维丛"缺失的数学形式化：它给出的对象集合——离散向量丛/标架丛、离散联络一次形式、离散曲率二次形式、离散外协变导数、离散 Bianchi 恒等式——与 `FG_纤维丛理论.md` §3 的结构（$F_\ell=d\mathcal A_\ell+\mathcal A_\ell\wedge\mathcal A_\ell$、$DF=0$、$D*F=*J_\Phi$ 的离散化）一一对应。

**成熟度**：离散外微积分/有限元外微积分成熟（计算电磁学、几何处理领域广泛应用）；丛值形式方向为新兴（2024 年首次给出带收敛性的完整构造）。

**对 CQM 的特别价值**：该框架的对象是纯组合的（单纯复形 + 上链 + 群元素），无连续极限依赖，天然适合作为 Lean 形式化（`06 Lean形式化` 目录）的严格定义来源。

**缺口**：这是数学/数值形式化，不含物理动力学（无作用量路径积分）、不含谱算符、不含算术结构。

---

## 6. 成熟方案四：转移矩阵与 Osterwalder–Schrader 正性——谱算符的成熟桥梁

CQM 的同步算符 $\hat{\mathcal S}_\ell$ 是定义在截面空间上的自伴谱算符，且理论要求 $\hat{\mathcal S}=\hat{\mathcal S}^\dagger\iff\xi(s)=\xi(1-s)$（`CQM_核心_因果网络同步理论.md` §3.3）。格点理论中"从欧几里得路径积分到希尔伯特空间谱理论"的成熟桥梁是：

- **转移矩阵方法**：Lüscher（1977 年, Communications in Mathematical Physics 54, 283）对格点规范理论构造了自伴、严格正定的转移矩阵，从而建立欧几里得格点作用量与量子哈密顿量/谱理论之间的严格联系；
- **Osterwalder–Schrader 公理与正性**：欧氏格林函数在反射正性条件下重构闵氏时序场论（希尔伯特空间、哈密顿量、谱分解）[cite:11]。

这条通道与 CQM 需求的匹配点：格点上的"自伴正定谱生成算符"正是转移矩阵；"从配分函数/路径积分提取离散谱"有标准算法（关联函数谱分解、变分法）。CQM 若将其同步算符实现为某格点模型的转移矩阵类对象，即可借用整套成熟谱理论，包括自伴性证明的机制（反射正性结构）。

**缺口**：标准转移矩阵在规则时间切片上定义；Regge 动态几何上需推广（CDT 本身有时间叶状结构，是候选载体 [cite:9]）。同步算符的具体形式 $\frac{L_u}{2\pi C}\sqrt{1-\beta\hat\delta_v}$ 是 CQM 特有的，其自伴性必须另行证明，成熟框架只提供机制而非结论。

---

## 7. 成熟方案五：自旋网络与广义联络——图上联络空间的严格测度

圈量子引力（Loop Quantum Gravity）一侧，自旋网络（spin network，Penrose 提出；Rovelli–Smolin 1995 年系统化为量子引力态）给出"图 + 群表示 + 不变量张量（intertwiner）"的离散几何语言 [cite:12]；Ashtekar–Lewandowski 等构造了图上广义联络空间的严格测度（投影极限构造，Ashtekar–Lewandowski 测度），把"任意有限图上联络的集合"组织成可严格积分的构型空间 [cite:12]。这套结构与 Regge 计算的面积/角亏变量有部分对应（Barrett–Roček–Williams 面积变量 [cite:12]）。

**对 CQM 的价值**：若需要在"任意 Regge 剖分族"（而非固定剖分）上定义联络的测度与路径积分，Ashtekar–Lewandowski 式投影极限构造是现成的严格数学工具——它不依赖格点的规则性。

**缺口**：引力导向，结构群取自旋群而非物质结构群；无算术结构。

---

## 8. 成熟方案六：格点上的规范破缺与离散群——SU(5) 破缺与 U(1)/ℤₙ 的实现

CQM 需要在离散底空间上实现 SU(5) $\to$ U(1)×SU(2)×SU(3) 的约束/重组与超导候选群族 $U(1)/\mathbb Z_n$。成熟对应物：

- **格点规范-Higgs 模型**：规范场与固定长度 Higgs 标量耦合的格点理论是成熟研究对象。Fradkin–Shenker（1979 年, Physical Review D 19, 3682）证明了其相图结构：Higgs 场取基本表示时，"Higgs 相"与"禁闭相"解析连通（无相边界）；取其他表示（如伴随表示）时才可能出现真相边界 [cite:16]。Osterwalder–Seiler（1978 年）早期建立了格点规范场论的严格构造 [cite:17]。
- **离散/有限群格点规范理论**：$\mathbb Z_N$ 循环群等有限群的格点规范理论是标准对象（链接上放 $\mathbb Z_N$ 元素），广泛应用于禁闭-解禁闭转变与拓扑序研究——这是 $U(1)/\mathbb Z_n$ 超导群族的直接格点对应物。

**必须诚实记录的成熟约束**（对 CQM 的规范重组叙事有实质影响）：

1. **Elitzur 定理**（1975 年, Physical Review D 12, 3978）：格点上局域规范对称性不能自发破缺，能自发破缺的只是规范固定后的剩余整体对称性。格点实现 SU(5) 重组时，可讨论的严格对象是规范固定子群下的对称破缺或相结构差异，而非裸的局域对称破缺。
2. **Fradkin–Shenker 结果**：基本表示 Higgs 相与禁闭相可解析连通，说明"破缺相"与"禁闭相"的区分在格点上不是绝对的序参量区分 [cite:16]。

这两条不否定 CQM 的物理目标，但意味着"在格点上实现 SU(5) 重组"必须以规范固定/相结构/剩余对称的语言重新表述——这与 `FG_核心理论.md` §3.0 "物理主丛不能反向指定 GL(n)"的自我约束精神一致。

**缺口**：CQM 的约束框架（$R$ 是约束产物）在格点文献中没有对应理论；格点规范-Higgs 模型提供的是"规范场 + 序参量场耦合"的动力学模板，约束实现问题仍是 CQM 自有的数学问题。

---

## 9. 成熟方案七：数值机械

CQM 计算链（`08 超导` 目录的 $T_c$ 链、角亏涨落量子化、GUE 统计验证）需要的数值能力在格点社区全部成熟：

- **蒙特卡洛与混合蒙特卡洛**（Hybrid Monte Carlo, HMC）：规范场构型采样的标准算法，含动力费米子 [cite:18]；
- **自由能差与相变**：热力学积分/直方图方法计算自由能交叉 $F_1(T)=F_2(T)$ 是格点统计力学的标准技术（有限温度格点量子色动力学的退禁闭转变研究即此模式），直接对应 CQM 的 $T_c=\frac{E_2-E_1}{S_2-S_1}$；
- **谱提取**：关联函数变分谱分解（广义本征值问题）可提取转移矩阵/哈密顿量谱——同步算符谱 $n_k$ 的数值实现路径；
- **图谱统计**：量子图与图谱的迹公式（Kottos–Smilansky 方向；Kurasov 对一般自伴边界条件的推广）为 GUE 统计验证 $P(s)=1-(\sin\pi s/\pi s)^2$ 提供成熟的离散谱理论 [cite:27]；
- **CDT 有限元谱分析**：三角剖分几何上的谱方法有专门研究 [cite:10]。

---

## 10. "离散几何 → 自守形式 / L 函数"通道：成熟桥与算术性障碍

这是 CQM 发生学链条（质数 → 伽罗瓦表示 → L 函数 → 朗兰兹对应 → 自守表示 → 紧化投影）中唯一**没有**成熟整体方案的环节。文献核查结果如下。

### 10.1 存在的成熟桥（各自要求算术输入）

| 成熟理论 | 离散输入要求 | 输出 | 文献 |
|---|---|---|---|
| theta 级数（theta series） | 正定整格、偶格条件 | 模形式（GL(2) 层）、Siegel 模形式；Siegel–Weil 公式 | [cite:24] |
| Epstein zeta 函数 | 正定二次型/Gram 矩阵（$\mathbb Z^n$ 格） | 带 函数方程的 Dirichlet 级数，$n=2$ 时与 Eisenstein 级数相联系；度 = 格维数 $n$ | [cite:20][cite:21] |
| Eichler–Shimura 理论 / 模符号（modular symbols） | 模曲线、算术子群、局部系统 | 上同调 ↔ 自守形式 ↔ 伽罗瓦表示 ↔ L 函数 | [cite:25] |
| Kudla 纲领 / theta 对应 | Shimura 簇、算术格、特殊除子 | 算术 theta 提升、特殊 L 值关系 | [cite:24] |
| Ihara zeta 函数 / 图 L 函数 | 有限图（非回溯闭路径） | 行列式公式 $\zeta_X(u)^{-1}=(1-u^2)^{r-1}\det(I-Au+Qu^2)$、图素数定理、Ramanujan 谱隙 | [cite:22][cite:23] |
| Farey/模三角剖分 | $\mathrm{SL}_2(\mathbb Z)$ 作用的理想三角剖分 | 三角剖分本身即模曲线 $\mathrm{SL}_2(\mathbb Z)\backslash\mathbb H$ 的算术对象 | [cite:28] |
| Veech 表面 / Teichmüller 曲线 | 格点多边形平坦曲面、Veech 群为格 | Teichmüller 曲线 ↔ 希尔伯特模曲面、实乘 Jacobian | [cite:29] |
| 算术拓扑（arithmetic topology） | 3 维流形、纽结与素理想的类比词典 | 类比框架（研究纲领级） | [cite:26] |
| 量子图谱理论 | 度量图 + 自伴算子 | 迹公式、谱行列式、周期轨道求和 | [cite:27] |
| building 有限商 zeta 函数 | $p$-进群 building 的有限商（PGL(3)、PGSp(4)） | 封闭表达式、拓扑与谱信息 | [cite:30] |

### 10.2 核心障碍（调研确认）

**一般单纯复形不具备任何上述算术输入。**不存在"非算术流形的组合三角剖分 → 伽罗瓦表示/自守形式"的定理；成熟的唯一路线是"算术代数几何对象 → étale 上同调 → 伽罗瓦表示 → L 函数"，其入口要求模结构、周期结构、整格点或算术群作用 [cite:25]。这与项目文档"Regge 底空间几何约束（非唯一）"、"第一性原理推导尚未建立"的自我标注完全一致——文档的诚实标注是准确的。

**对 CQM 有实质警示的成熟反例**：Epstein zeta 函数的零点一般不全部位于临界线（Davenport–Heilbronn 型结果）[cite:20]。含义：即使 CQM 通过整格化构造打通"Regge 复形 → Epstein zeta 函数"通道，所得 zeta 函数**并不自动满足**"零点在临界线"的结论。CQM 的紧化约束 $\mathcal C_k(\lambda_{\rm phys},\gamma_n^{(k)})=0$（零点作为物理谱）必须由额外机制保证，不能指望格点型 zeta 函数自动提供。这是借用成熟方案时最重要的诚实性边界。

### 10.3 对 CQM 最有借用价值的三个构件

1. **Epstein zeta 函数**：若 Regge 复形顶点可嵌入 $\mathbb Z^N$ 并配正定 Gram 矩阵，则 $N$ 维格给出度 $N$ 的 Epstein zeta 函数——**度 = 格维数**这一性质与 CQM 的 GL(n) 层级（$n=\dim V_{\rm fund}$）天然对齐，且自带函数方程 [cite:20][cite:21]。但受 10.2 节反例约束。
2. **Farey/模三角剖分**：文献中唯一"三角剖分本身就是算术对象"的成熟例子——上半平面被 $\mathrm{SL}_2(\mathbb Z)$ 轨道给出的理想三角剖分即模曲线的三角剖分，其后接 Eichler–Shimura 通道 [cite:25][cite:28]。若 CQM 在 GL(2) 层需要一个"自带算术的底空间"，这是现成模板；GL(5) 层无现成推广。
3. **Ihara zeta 函数**：Regge 复形 1-骨架（图）的 zeta 函数有行列式公式与"黎曼猜想"类比（Ramanujan 图谱条件）[cite:22][cite:23]。只编码图路径结构、不编码 4-单纯形几何，也不给出 GL(n) 自守 L 函数，但可作为底空间谱性质的辅助验证工具（谱隙、闭路径统计）。

---

## 11. CQM 对象与成熟方案映射总表

| CQM 对象（文档出处） | 成熟对应物 | 框架/文献 | 成熟度 | 借用后仍缺 |
|---|---|---|---|---|
| Regge 底空间 $M_\ell$、角亏 $\delta_v$ | Regge 计算铰链角亏 | [cite:2][cite:15] | 成熟（60 余年） | "物质晶胞分布 → 层级剖分"的剖分规则是 CQM 特有输入 |
| 主丛 $P(M_\ell,G_\ell)$ | 胞腔复形上的离散规范结构（链接群元素/离散标架丛） | [cite:1][cite:8] | 物理实现成熟；数学形式化新兴成熟 | — |
| 边 = 联络 $\mathcal A_\ell$ 离散化 | 链接变量 $U_\ell\in G_\ell$（规范场置于三角剖分对偶图链接） | [cite:1][cite:10] | 成熟 | "$\mathcal A_\ell$ 由层级晶胞分步生成"的生成规则需自建 |
| 面 = 曲率 $\mathcal F_\ell$ 离散化 | 面和乐/plaquette 乘积 | [cite:1][cite:10] | 成熟 | — |
| 和乐 $W_v=\exp(i\delta_v\hat T_\ell)$ | 绕铰链自旋联络和乐 = 角亏转角（定理级结果） | [cite:13][cite:14] | 定理级（引力结构群） | 和乐放物质结构群 $G_\ell$ 上需把链接变量与铰链几何绑定（二维有先例 [cite:10]，四维待建） |
| 伴丛曲率 $F=dA+A\wedge A$、$DF=0\iff$ Jacobi | 离散外协变导数、离散 Bianchi 恒等式 | [cite:8] | 新兴（2024，含收敛定理） | 物理作用量与动力学需自建 |
| 动态几何（退相干 → 4-单纯形） | 因果动力三角剖分路径积分 | [cite:9] | 成熟（引力侧） | 与物质层级剖分/规范场的四维耦合待建 |
| 谱算符 $\hat{\mathcal S}_\ell$（自伴） | 转移矩阵（Lüscher 自伴正定构造）+ Osterwalder–Schrader 正性 | [cite:11] | 成熟 | $\hat{\mathcal S}$ 特有形式的自伴性需自行证明 |
| SU(5) → U(1)×SU(2)×SU(3) 约束/重组 | 格点规范-Higgs 模型 | [cite:16][cite:17] | 成熟（受 Elitzur 定理与 Fradkin–Shenker 相图约束） | 需以规范固定/剩余对称语言重述；约束实现问题无现成理论 |
| 超导群族 $U(1)/\mathbb Z_n$ | 有限群 $\mathbb Z_N$ 格点规范理论 | 标准格点对象 | 成熟 | 与角亏资格条件的耦合是 CQM 特有 |
| $T_c$ 自由能交叉 $F_1(T_c)=F_2(T_c)$ | 热力学积分/直方图自由能差蒙特卡洛 | [cite:18] | 非常成熟 | — |
| GUE 统计验证 | 量子图/图谱迹公式 | [cite:27] | 成熟 | — |
| 底空间 → 自守形式 $f$ → L 函数 | theta 级数、Epstein zeta、Eichler–Shimura、Farey 三角剖分、Ihara zeta | [cite:20]–[cite:25][cite:28][cite:30] | 各自成熟，但全部要求算术输入 | "任意 Regge 复形 → 自守形式"不存在成熟通道（调研确认） |
| 零点在临界线（紧化约束） | 无成熟对应；存在 Epstein zeta 零点不全在临界线的反例 | [cite:20] | — | CQM 必须自建机制，不能想当然 |

---

## 12. 分阶段借用路线建议

### 阶段一：离散形式实现（可立即全面借用）

- 用组合流形上的丛值形式离散外微积分 [cite:8] 形式化 `FG_纤维丛理论.md` §2–§3 的全部对象：离散主丛、离散联络、离散曲率、离散 Bianchi 恒等式；
- 规范场按 Candido 等构造置于三角剖分对偶图链接 [cite:10]；
- 以"绕铰链和乐 = 角亏转角"定理 [cite:13][cite:14] 锚定 $W_v^{(\ell)}=\exp(i\delta_v^{(\ell)}\hat T_\ell)$ 的几何部分；
- 产出：一组纯组合的严格离散定义，可直接进入 `06 Lean形式化` 的形式化目标清单。

### 阶段二：谱实现（可大部借用）

- 固定 Regge 剖分（或以因果动力三角剖分采样动态几何 [cite:9]）+ Wilson 型作用量；
- 构造 Lüscher 型自伴正定转移矩阵，以反射正性机制承载 $\hat{\mathcal S}=\hat{\mathcal S}^\dagger$ 要求 [cite:11]；
- 以关联函数变分谱分解提取同步谱 $n_k$；
- 注意：$\hat{\mathcal S}$ 的 CQM 特有形式（$\frac{L_u}{2\pi C}\sqrt{1-\beta\hat\delta_v}$、Casimir 项）不在任何成熟框架内，其谱性质是新的数学对象。

### 阶段三：规范重组与超导计算链（可大部借用，有表述性约束）

- 以格点规范-Higgs 模型实现 SU(5) → 子群的破缺动力学 [cite:16][cite:17]，按 Elitzur 定理以规范固定/剩余对称语言重述"破缺"；
- 以 $\mathbb Z_n$ 有限群格点模型实现超导候选群族，角亏涨落 $\hat\delta_v^{(1)}$（声子量子化）在离散外微积分框架下实现；
- 以自由能差蒙特卡洛实现 $F_1(T_c)=F_2(T_c)$ 交叉 [cite:18]，替代/校验现有解析链条（`08 超导` 目录）。

### 阶段四：算术通道（必须 CQM 自建，可借成熟构件）

按可借用程度排序的三个候选方案：

- **方案 A（整格化 + Epstein zeta 函数）**：给 Regge 复形顶点附加 $\mathbb Z^N$ 嵌入与正定 Gram 矩阵，构造度 $N$ 的 Epstein zeta 函数（度与 GL(n) 层级对齐，自带函数方程）[cite:20][cite:21]。**警示**：Davenport–Heilbronn 型反例表明其零点不自动在临界线 [cite:20]——紧化约束方程 $\mathcal C_k=0$ 的机制必须另行构造。
- **方案 B（模对称三角剖分）**：在 GL(2) 层采用 Farey 型三角剖分使底空间自带 $\mathrm{SL}_2(\mathbb Z)$ 算术群作用，接 Eichler–Shimura 通道 [cite:25][cite:28]；GL(5) 层无现成推广，需另行构造（诚实标注：无文献支持）。
- **方案 C（1-骨架 Ihara zeta 函数）**：作为底空间谱性质（谱隙、闭路径统计）的辅助验证工具 [cite:22][cite:23]，不作为自守 L 函数通道。

无论哪个方案，"Regge 底空间几何约束自守形式"这一步都是构造性假设，成熟文献不提供定理支撑——这与项目文档既有标注一致，建议在文档中维持该诚实性分级。

---

## 13. 结论与诚实性声明

**可以直接站在成熟结果上的部分**（借用后即获得定理级支撑）：

1. 离散底空间上的主丛/联络/曲率/和乐的物理实现（格点规范理论，五十年历史 [cite:1][cite:18]）；
2. 规范场与三角剖分几何的结合方式（对偶图链接构造，二维已发表 [cite:10]）；
3. 离散纤维丛的数学形式化（丛值形式离散外微积分，2024 [cite:8]）；
4. 和乐 = 角亏转角（Regge 计算定理 [cite:13][cite:14]）；
5. 谱算符的机制框架（转移矩阵 + 反射正性 [cite:11]）；
6. 规范破缺的格点动力学模板与约束（Fradkin–Shenker [cite:16]、Osterwalder–Seiler [cite:17]、Elitzur 定理）；
7. 全套数值机械（蒙特卡洛、自由能差、谱提取、图谱统计 [cite:18][cite:27]）。

**成熟框架不能覆盖、仍是 CQM 自有构造的部分**：

1. 底空间算术化（"Regge 复形 → 自守形式"通道，文献确认无成熟方案）；
2. 约束框架（$R$ 是约束产物）的实现问题；
3. 同步算符特有形式的谱性质（含自伴性）；
4. 紧化约束方程 $\mathcal C_k=0$ 与"零点在临界线"的机制（存在 Epstein zeta 反例的警示 [cite:20]）；
5. GRH(GL(4))、GRH(GL(5))（未证明的数学前提）。

**总体判断**："Regge 底空间 + 纤维丛需要自行探索、没有成熟方案"的初始判断需要拆分为两半——**物理实现层（纤维丛在离散底空间上的构造与计算）有成熟方案可借，且比预期更成熟**（格点规范理论 + 对偶图构造 + 丛值离散外微积分 + 转移矩阵谱理论四件套覆盖了 `FG_纤维丛理论.md` §2–§4 的几乎全部对象）；**算术层（底空间 → 自守形式 → L 函数零点）确实没有成熟方案**，与文档既有诚实标注一致，本报告给出的方案 A/B/C 是可借用构件的最大集合，但每一条都以构造性假设为前提。

---

## Sources

1. K. G. Wilson (1974), "Confinement of Quarks", *Physical Review D* 10, 2445–2459（格点规范理论开创文献；历史条目确认）. https://encyclopedia.pub/entry/history/show/82552
2. "Discrete Approaches to Quantum Gravity in Four Dimensions"（含量子 Regge 计算综述）. https://pmc.ncbi.nlm.nih.gov/articles/PMC5253799/
3. H. W. Hamber, R. M. Williams (1997), "Gauge Invariance in Simplicial Gravity", *Nuclear Physics B* 487, 345–408. https://aeneas.ps.uci.edu/hamber/gauge.pdf
4. H. W. Hamber, R. M. Williams (1993), "Newtonian Potential in Quantum Regge Gravity", *Physical Review D* 47, 5160–5172. https://cds.cern.ch/record/265293/files/9406163.pdf
5. A. Hirani (2003), "Discrete Exterior Calculus", PhD thesis. https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Hirani03.pdf
6. M. Desbrun, E. Kanso, Y. Tong (2006), "Discrete Differential Forms for Computational Modeling". https://www.cs.cmu.edu/~kmcrane/Projects/DDG/paper.pdf
7. D. N. Arnold, R. S. Falk, R. Winther (2010), "Finite Element Exterior Calculus: From Hodge Theory to Numerical Stability", *Bulletin of the AMS* 47(2), 281–354. https://sites.math.rutgers.edu/~falk/papers/bulletin-rev2.pdf
8. T. Braune, Y. Tong, F. Gay-Balmaz, M. Desbrun (2024), "A Discrete Exterior Calculus of Bundle-valued Forms", arXiv:2406.05383. https://arxiv.org/abs/2406.05383
9. "Causal Dynamical Triangulations: Gateway to Nonperturbative Quantum Gravity"（综述）. https://arxiv.org/pdf/arXiv:2401.09399v1
10. A. Candido, G. Clemente, M. D'Elia, F. Rottoli (2020), "Compact Gauge Fields on Causal Dynamical Triangulations: a 2D case study", arXiv:2010.15714；*JHEP* 04 (2021) 184. https://arxiv.org/abs/2010.15714
11. nLab, "Osterwalder–Schrader theorem"（含 Lüscher 转移矩阵与正性条件脉络）. https://ncatlab.org/nlab/show/Osterwalder-Schrader+theorem
12. J. Baez, "This Week's Finds in Mathematical Physics, Week 55"（评述 Ashtekar–Lewandowski 广义联络量子化与自旋网络文献；含 Barrett–Roček–Williams 面积变量线索）. https://math.ucr.edu/home/baez/week55.html
13. "The spin connection of twisted geometry"（2013 年预印本；命题：Regge 情形绕链接和乐为转角等于角亏的旋转）. https://faculty.bard.edu/~hhaggard/pubs/HaRoViWi2013/HaRoViWiTwistedSpinConnection.pdf
14. "Contracted Bianchi Identity and Angle Relation on n-dimensional Simplicial Complex of Regge Calculus", arXiv:1807.11420. https://arxiv.org/pdf/1807.11420.pdf
15. "On the definition of curvature in Regge calculus", *IMA Journal of Numerical Analysis*. https://academic.oup.com/imajna/advance-article/doi/10.1093/imanum/drad095/7502804
16. E. Fradkin, S. H. Shenker (1979), "Phase diagrams of lattice gauge theories with Higgs fields", *Physical Review D* 19, 3682. https://ui.adsabs.harvard.edu/abs/1979PhRvD..19.3682F （作者列表页：http://eduardo.physics.illinois.edu/homepage/recent.html）
17. "Phase diagram of the lattice SU(2) Higgs model", arXiv:0911.1721（引文含 Osterwalder–Seiler 1978 "Gauge Field Theories on a Lattice", *Annals of Physics* 110, 440）. https://arxiv.org/pdf/0911.1721
18. Flavour Lattice Averaging Group (FLAG) 2024, quark masses 评述（格点量子色动力学精度证据）. http://flag.itp.unibe.ch/2024/Media?action=AttachFile&do=get&target=FLAG_qmass.pdf
19. "The Yang–Mills measure on compact surfaces as a universal scaling limit of lattice gauge models", arXiv:2602.08591. https://arxiv.org/html/2602.08591v2
20. "Epstein zeta-function", *Encyclopedia of Mathematics*（含函数方程、Davenport–Heilbronn 零点结果、Selberg–Chowla）. https://encyclopediaofmath.org/wiki/Epstein_zeta-function
21. "Computation and Properties of the Epstein Zeta Function with Applications to Quantum Systems", arXiv:2412.16317. https://arxiv.org/html/2412.16317
22. A. Terras, *Graph Zeta Functions*（Ihara zeta、行列式公式、Ramanujan 图）. https://mathweb.ucsd.edu/~aterras/newbook.pdf
23. D. Lenz, F. Pogorzelski, M. Schmidt, "The Ihara Zeta Function for Infinite Graphs", arXiv:1408.3522. https://arxiv.org/pdf/1408.3522
24. Chao Li, "Geometric and Arithmetic Theta Correspondences"（theta 对应、Kudla 纲领讲义）. https://arxiv.org/pdf/2402.12159.pdf
25. "Modular Symbols"（Eichler–Shimura/模符号体系）. https://arxiv.org/html/math/9809058v1
26. nLab, "Arithmetic topology". https://ncatlab.org/nlab/show/arithmetic+topology
27. P. Kurasov, "The trace formula for quantum graphs with general self-adjoint boundary conditions", arXiv:0805.3111. https://arxiv.org/pdf/0805.3111v1
28. K. Stange, "Views on the Farey tesselation"（Farey/模三角剖分）. https://math.colorado.edu/~kstange/quarto-talks/FareyLegacy/Stange-FareyLegacy.html
29. C. McMullen, "Billiards and Teichmüller curves"（Veech 表面与 Teichmüller 曲线的算术联系）. http://math.harvard.edu/~ctm/home/text/papers/tsurv/tsurv.pdf
30. 华东师范大学学术报告摘要：PGL(3)、PGSp(4) building 有限商的 zeta 函数. https://math.ecnu.edu.cn/seminardetail.html?xqid=2046
31. Z. Rudnick 发表列表（Duke–Rudnick–Sarnak 对称空间格点计数方向）. https://www.math.tau.ac.il/~rudnick/pub.html
