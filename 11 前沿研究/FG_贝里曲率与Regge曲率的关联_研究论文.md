# 贝里曲率与 Regge 曲率的关联：文献调研与研究论文

**作者**：ruster

> **文档定位**：文献调研记录 + 研究论文。调研贝里曲率（Berry curvature）的文献谱系，分析其与本框架 Regge 曲率（底空间角亏离散曲率）的关联，作为研究记录归档。
> **日期**：2026-09-08
> **调研方法**：网络文献检索（出版商官方页面、arXiv、NASA 天体物理数据系统），多来源交叉验证；所有列入参考文献的条目均经过作者、年份、期刊信息核实；未能核实的信息在正文中明确标注。
> **状态标注约定**（与项目"状态诚实标注"要求一致）：
> - 【文献确立】= 文献中已确立的结果（附参考文献编号）；
> - 【标准数学】= 教科书级数学定理（以定理名指认，不附网络来源）；
> - 【CQM 构造假设】= 本框架的构造性假设，无文献对应，诚实标注。

---

## 摘要

本文调研贝里曲率的文献谱系（奠基理论 → 能带物理 → 超导电性中的量子几何 → 第一性原理计算方法），并系统分析贝里曲率与本框架 Regge 曲率（三角剖分底空间中集中于共维 2 铰链的角亏曲率）的关联。核心结论：

1. **共同数学骨架【标准数学】**：贝里曲率与 Regge 曲率都是"联络—曲率—和乐"三位一体的具体实现——贝里曲率是厄米线丛（或向量丛）上贝里联络的曲率 2-形式，其和乐是贝里相位（Wilson 环）；Regge 曲率是分段平直几何中集中于铰链的曲率测度，其和乐是绕铰链回路的亏角旋转。两者都由 Ambrose–Singer 定理刻画的同一数学范畴（主丛联络的曲率与和乐）支配。
2. **拓扑层面平行【标准数学】**：贝里曲率在闭合二维流形（布里渊区环面）上的积分给出陈数（第一陈类）；二维三角剖分的角亏总和给出欧拉示性数（离散 Gauss–Bonnet 定理）。两者都是"曲率测度积分 = 拓扑不变量"的实例。
3. **物理交点【文献确立】**：锥形时空（宇宙弦亏角 δ = 8πGμ）是两类曲率在文献中确定交汇的物理对象——锥形时空和乐（绕弦一周 = 亏角旋转）与单铰链 Regge 几何同构，其形式与贝里相位同为闭合回路上指数化的角度。
4. **直接连接文献的缺失【诚实声明】**：文献检索未找到直接建立"贝里曲率 ↔ Regge 微积分"对应的工作；最接近的是锥形亏角与贝里相位相互作用的个别预印本（Binder 2002）。两者的关联是**结构性的**（共同的数学骨架），不是**文献性的**（无人建立过等式或映射）。
5. **与本框架的对接**：精细引力（FG）的伴丛和乐 $W_v^{(\ell)} = \exp(i\delta_v^{(\ell)}\hat{T}_\ell)$ 在数学范畴上与贝里和乐同型（均为 Wilson 环）；超导文档中"密度泛函理论贝里曲率是伴丛和乐的唯象近似"及"$\delta_{\text{intrinsic}}$ 需外部贝里曲率输入"的定位属【CQM 构造假设】。量子几何 × 平带超导文献（超流刚度由量子度规的布里渊区积分决定）为 $\delta_{\text{intrinsic}}$ 断链提供文献对照：几何信息控制超导转变温度有确立先例，但文献中使用的是动量空间量子度规，而非实空间角亏——映射本身仍需框架内构造。

---

## 1. 引言

### 1.1 研究动机

本框架（因果网络同步理论，CNST / 耦合常数量子力学，CQM）的精细引力（FG）采用"一个联络生成两种曲率"的结构：底空间曲率是 Regge 角亏 $\delta_v^{(\ell)} = 2\pi - \sum_{\Delta\ni v}\alpha_\Delta$，伴丛曲率是 $F_\ell = d\mathcal{A}_\ell + \mathcal{A}_\ell\wedge\mathcal{A}_\ell$，其和乐为 $W_v^{(\ell)} = \exp(i\delta_v^{(\ell)}\hat{T}_\ell) \in G_\ell$（`09 精细引力（FG）/FG_纤维丛理论.md` §3、§3.1）。

贝里曲率在数学上同为"联络的曲率"。项目内已有三处涉及贝里概念，但均未展开：

- **超导第一性链断链**：`08 超导/CQM_超导_FG层级同步算符体系.md` §1.2——"内禀角亏 $\delta_{\text{intrinsic}}$ 无内部来源——当前只能引入外部 DFT Berry 曲率"；
- **方法论定位**：同文档 §9.3——"DFT Berry 曲率是电子波函数在动量空间的几何相位——在 CQM 语言中它是伴丛和乐的某种唯象近似"；
- **谱理论线索**：`01 核心理论/CQM_核心_因果网络同步理论.md` §3.7——黎曼–西格尔相角 $\theta(t)$ 被读作"同步基态的 Berry 相位"。

本文回答三个问题：(1) 贝里曲率的文献谱系是什么；(2) 贝里曲率与 Regge 曲率有哪些严格成立的关联、哪些是文献空缺；(3) 这些文献对本框架（尤其是超导第一性链的 $\delta_{\text{intrinsic}}$ 断链）给出什么启示。

### 1.2 范围与限制

本文是文献调研与概念分析记录，不包含新证明。所有外部文献结论的可靠性以标注为准；框架内部的对接分析明确区分"数学范畴级同构"（严格）与"CQM 构造假设"（无文献对应）。

---

## 2. 贝里曲率文献综述

### 2.1 奠基文献：几何相位的发现与纤维丛表述

M. V. Berry（1984）证明：参数空间 $R$ 中的哈密顿量 $H(R)$ 沿闭合回路 $C$ 绝热演化一周后，系统本征态除动力学相位外获得一个几何相位【文献确立】[1]：

$$\gamma_n(C) = \oint_C i\langle n(R)|\nabla_R|n(R)\rangle\cdot dR$$

B. Simon（1983）指出该几何相位因子恰是厄米线丛上的和乐（holonomy）——绝热定理在量子态线丛上自然定义一个联络，几何相位是其和乐[2]。这一纤维丛表述是贝里曲率的数学基础【文献确立】。

Wilczek 与 Zee（1984）将构造推广到简并系统：简并能级的绝热输运生成**非阿贝尔**规范结构，曲率为 $F = d\mathcal{A} + \mathcal{A}\wedge\mathcal{A}$，和乐为路径编序的 Wilson 环[3]【文献确立】。这一非阿贝尔形式与本框架伴丛曲率 $F_\ell = d\mathcal{A}_\ell + \mathcal{A}_\ell\wedge\mathcal{A}_\ell$ 在公式层面完全同型（见 §4.1）。

### 2.2 数学结构：贝里联络、贝里曲率与量子几何张量

对动量空间 $\mathbf{k}$ 中的布洛赫态 $|u_{n\mathbf{k}}\rangle$，贝里联络与贝里曲率定义为【文献确立】[7]：

$$\mathcal{A}_n(\mathbf{k}) = i\langle u_{n\mathbf{k}}|\nabla_{\mathbf{k}}|u_{n\mathbf{k}}\rangle, \qquad \Omega_n(\mathbf{k}) = \nabla_{\mathbf{k}}\times\mathcal{A}_n(\mathbf{k})$$

贝里相位等于曲率通量（Stokes 定理）：$\gamma_n(C) = \oint_C\mathcal{A}_n\cdot d\mathbf{k} = \iint_S\Omega_n\cdot dS$。

Provost 与 Vallee（1980，早于 Berry 1984）已在量子态流形上引入黎曼结构[4]：完整对象是**量子几何张量**（quantum geometric tensor）【文献确立】[4][7]：

$$Q_{\mu\nu} = \langle\partial_\mu n|\big(1-|n\rangle\langle n|\big)|\partial_\nu n\rangle = g_{\mu\nu} - \frac{i}{2}\Omega_{\mu\nu}$$

其实部 $g_{\mu\nu}$ 是**量子度规**（quantum metric），虚部是贝里曲率。量子度规与贝里曲率是同一张量的对称与反对称部分——这一点对 §5.4 的超导分析至关重要。

### 2.3 能带物理：陈数、反常霍尔效应与拓扑物态

- **整数量子霍尔效应**：Thouless–Kohmoto–Nightingale–den Nijs（1982）证明二维周期系统霍尔电导量子化为 $\sigma_{xy} = (e^2/h)\sum_n C_n$，其中陈数 $C_n = \frac{1}{2\pi}\int_{\text{BZ}}\Omega_n(\mathbf{k})\,d^2k \in \mathbb{Z}$ 是贝里曲率在布里渊区环面上的积分[5]【文献确立】。这是"贝里曲率积分 = 拓扑不变量"的范式确立。
- **反常霍尔效应**：Karplus 与 Luttinger（1954）的早期理论已包含内禀反常速度机制[6]；现代半经典动力学方程 $\dot{r} = \frac{1}{\hbar}\nabla_{\mathbf{k}}\varepsilon_n - \dot{k}\times\Omega_n$ 中的反常速度项由贝里曲率给出，Xiao–Chang–Niu（2010）的《现代物理评论》综述系统总结了贝里相位对电子性质的影响（半经典动力学、轨道磁化、输运）[7]；Nagaosa–Sinova–Onoda–MacDonald–Ong（2010）综述确立"金属铁磁体反常霍尔效应由内禀贝里曲率机制主导"[8]【文献确立】。
- **外尔半金属**：外尔点是动量空间中贝里曲率的单极子源（单极子荷 = 手性 = 绕外尔点小球面的陈数）[7][9]【文献确立】。这给出"贝里曲率 = 动量空间中的场强，其源是带隙简并点"的完整图像。

### 2.4 超导电性与量子几何

这是与本框架超导主线最相关的文献簇：

- Peotta 与 Törmä（2015）证明：**平带极限下超流刚度（superfluid weight）不来自能带色散，而来自量子度规在布里渊区的积分**；拓扑非平庸（陈数非零）的平带即使完全无色散也携带有限超流刚度，且受拓扑条件[10]【文献确立】。
- Julku 等（2016）在 Lieb 晶格平带证实超流权重的几何起源[11]；Liang 等（2017）在多带一般情形分离超流权重的能带几何与贝里曲率贡献[12]；Hu 等（2019）计算了魔角扭曲双层石墨烯中超流权重的几何贡献与常规贡献[13]【文献确立】。
- Törmä–Peotta–Bernevig（2022）《自然评论·物理》综述确立"超导电性、超流性与量子几何"作为研究领域的地位[14]；Tian 等（2023）在《自然》报道了量子几何使能的狄拉克平带超导实验证据[15]【文献确立】。

**要点**：该文献簇确立的结论是——控制超导转变温度 $T_c$（经由超流刚度 / Berezinskii–Kosterlitz–Thouless 转变温度）的几何量是**完整量子几何张量**（尤其量子度规 $g_{\mu\nu}$），不只是贝里曲率 $\Omega_{\mu\nu}$。

### 2.5 第一性原理计算中的贝里曲率

- King-Smith 与 Vanderbilt（1993）的现代极化理论将晶体极化确立为贝里相位（几何相位）对象[16]；Marzari 与 Vanderbilt（1997）建立最大局域化外尔函数方法[17]；Marzari 等（2012）的《现代物理评论》综述确立了"密度泛函理论波函数 → 最大局域化外尔函数 → 外尔插值 → 任意密集网格上的贝里曲率"的标准计算流程[18]【文献确立】。
- 反常霍尔电导的第一性原理计算先例：Yao 等（2004）对铁磁体 bcc Fe 的计算将反常霍尔效应与占据布洛赫态的动量空间贝里相位直接联系[19]；Wang 等（2006）实现外尔插值计算反常霍尔电导[20]【文献确立】。

**要点**：本框架超导文档中"引入外部 DFT Berry 曲率"在计算上是成熟、良定义的操作（外尔插值是标准流程），但文献中密度泛函理论贝里曲率测量的是**动量空间能带几何**（见 §5.3 的对接分析）。

---

## 3. Regge 曲率文献综述

### 3.1 Regge 微积分：曲率集中于铰链

Tullio Regge（1961）建立"无坐标广义相对论"：弯曲时空用分段平直单纯复形近似，曲率不在四维体积内分布，而是**集中于共维 2 的铰链（hinge）上**，以亏角（deficit angle）度量[21]【文献确立】：

$$\delta_h = 2\pi - \sum_{\sigma\supset h}\theta_{\sigma,h}$$

其中 $\theta_{\sigma,h}$ 是包含铰链 $h$ 的各单纯形在 $h$ 处的二面角。Einstein–Hilbert 作用离散化为：

$$S_R = \frac{1}{8\pi G}\sum_h A_h\,\delta_h$$

对边长变分给出 Einstein–Regge 方程【文献确立】[21][23][24]。

在二维情形（本框架底空间三角剖分的情形），铰链退化为顶点 $v$，亏角 $\delta_v = 2\pi - \sum_{\Delta\ni v}\theta_v^{(\Delta)}$ 正是顶点处的**离散高斯曲率测度**：$\delta_v = \iint_{A_v^*} K\,dA$（$A_v^*$ 为对偶胞面积），因此 $K_v = \delta_v/A_v^*$、有效里奇标量 $R_v = 2\delta_v/A_v^*$【标准数学】。这与本框架 Lean 形式化中的桥接公式 $R_{\text{eff}} = 2\delta_v/A_{\text{dual}}$（`06 Lean形式化/Superconductivity/BridgeTheorems.lean`）一致——该公式是标准二维 Regge 曲率密度关系的实现。

### 3.2 数学基础与收敛性

Cheeger–Müller–Schrader（1984）证明：给定光滑黎曼度量，存在一列加细的分段平直网格，其 Regge 曲率测度在测度意义下收敛到光滑曲率测度；Lipschitz–Killing 曲率有同样的收敛结果[22]【文献确立】。这确立了"集中于铰链的曲率测度"作为光滑曲率的合法离散化——Regge 曲率不是近似权宜，而是数学上严格的曲率测度观点。

### 3.3 和乐表述与离散量子引力

- **亏角 = 和乐旋转角**：分段平直几何中每个单纯形内部平直（联络平凡），绕包围铰链的闭合回路平行移动一周，结果是与该回路所围亏角相等的旋转（洛伦兹型号时含 boost 分量）【文献确立】[23][24]。曲率完全由和乐探测——这正是 Ambrose–Singer 定理的离散实现（见 §4.1）。
- **离散量子引力谱系**：Regge 与 Williams（2000）综述分段线性结构在量子引力中的地位[23]；Barrett–Oriti–Williams（2019）综述 Regge 微积分到自旋泡沫与群场论的发展——其中以 2 胞为中心的和乐型变量是现代离散引力的基本变量[24]；Hamber（2009）综述格点引力的路径积分方法[25]；Bahr 与 Dittrich（2009）发展常曲率单纯形的改进方案[26]【文献确立】。

---

## 4. 贝里曲率与 Regge 曲率的关联分析

### 4.1 共同数学骨架：联络—曲率—和乐【标准数学】

两类曲率由同一数学范畴支配，可逐条对应：

**(1) Ambrose–Singer 定理**：主丛的和乐群李代数由曲率生成——绕无穷小回路的和乐正比于"曲率 × 所围面积元"。贝里曲率：$\gamma \approx \Omega\cdot\Delta S$（小回路）；Regge 曲率：绕铰链小回路的和乐旋转角 = $\delta_h$。两者都以"闭合回路上平移的不可积性"定义曲率。

**(2) Stokes 定理 / 曲率通量**：贝里相位 = 回路所围曲面上贝里曲率通量；绕回路平移的净旋转 = 回路所围的总亏角。和乐都是"曲率 2-形式的环路积分 ↔ 曲面通量"的实例。

**(3) 曲率测度 → 拓扑不变量**：

| | 贝里曲率【文献确立】[5][7] | Regge 曲率【标准数学】 |
|:---|:---|:---|
| 积分定理 | $C = \frac{1}{2\pi}\int_{\text{BZ}}\Omega\,d^2k \in \mathbb{Z}$（陈数，TKNN） | $\sum_v \delta_v = 2\pi\chi(S)$（离散 Gauss–Bonnet，欧拉示性数） |
| 上同调根源 | 第一陈类（Chern–Weil 理论：示性类 = 曲率形式的德拉姆上同调类） | 同为 Gauss–Bonnet–Chern 定理的离散实现 |

两者都是"曲率积分给出拓扑不变量"的一般原理（Chern–Weil 理论）的实例。

**(4) 非阿贝尔推广**：Wilczek–Zee 非阿贝尔贝里曲率 $F = d\mathcal{A} + \mathcal{A}\wedge\mathcal{A}$【文献确立】[3] 与本框架伴丛曲率 $F_\ell = d\mathcal{A}_\ell + \mathcal{A}_\ell\wedge\mathcal{A}_\ell$（`09 精细引力（FG）/FG_纤维丛理论.md` §3）公式同型；Wilson 环 $W = \mathcal{P}\exp(i\oint\mathcal{A})$ 与本框架和乐 $W_v^{(\ell)} = \exp(i\delta_v^{(\ell)}\hat{T}_\ell)$（§3.1）同型。

### 4.2 逐维结构对照表

| 对照维度 | 贝里曲率 | Regge 曲率（含本框架实现） |
|:---|:---|:---|
| 基底流形 | 参数流形（动量空间布里渊区环面，或哈密顿量参数空间）——**非物理时空** | 物理时空 / 底空间本身（本框架：物质晶胞分布的三角剖分 $M_\ell$） |
| 丛结构 | 厄米线丛（非简并能带）；简并时厄米向量丛（非阿贝尔）[2][3] | 标架丛 / 切丛的离散联络；本框架：层级结构群主丛 $P(M_\ell, G_\ell)$ |
| 联络 | 贝里联络 $\mathcal{A}_n = i\langle u_n\|\nabla u_n\rangle$[1][7] | 分段平直联络（每单纯形内平凡）；本框架：层级联络 $\mathcal{A}_\ell$ |
| 曲率对象 | 光滑 2-形式 $\Omega = \nabla\times\mathcal{A}$（外尔点处为单极子奇异源）[7][9] | 集中于共维 2 铰链的曲率**测度**（亏角 $\delta_h$）[21] |
| 和乐 | 贝里相位 $\gamma = \oint\mathcal{A} = \iint\Omega$（Wilson 环）[1][2] | 绕铰链回路平移 = 亏角旋转[23][24]；本框架：$W_v = \exp(i\delta_v\hat{T}_\ell)$ |
| 曲率积分 → 拓扑 | 陈数（TKNN 电导量子化）[5] | 二维 Gauss–Bonnet（欧拉示性数）【标准数学】 |
| 极限 / 稳定性 | 陈数在能带形变下不变（拓扑稳定）[5] | Cheeger–Müller–Schrader：加细极限下曲率测度收敛到光滑曲率[22] |
| 作用量 | 无标准作用量；进入输运响应（反常霍尔电导、极化、轨道磁化）[7][8][16] | Regge 作用量 $S_R = \frac{1}{8\pi G}\sum_h A_h\delta_h$ → Einstein–Regge 方程[21] |
| 可观测（本框架语境） | （外部输入）密度泛函理论贝里曲率[18][20] | 固有时流速、不确定性关系、声子谱、转变温度 $T_c$ 链 |
| 曲率来源 | 量子态空间（投影希尔伯特空间）几何对参数空间的投影[1][2][4] | 物理空间自身几何 / 本框架：物质组织形态的内禀不均匀性（角亏 = 组织缺陷度量） |

### 4.3 已确立的物理交叉

#### 4.3.1 锥形时空与亏角和乐：确定的交点

无限长直宇宙弦的外部时空局部平直但整体锥形，亏角 $\delta = 8\pi G\mu$（$\mu$ 为弦线能量密度）【文献确立】[27][28]。绕弦一周的平行移动 = 亏角 $\delta$ 的旋转——**锥形时空和乐与单铰链 Regge 几何在数学上同构**：一个宇宙弦就是连续时空中的"一根铰链"。van de Meent（2013）证明无质量宇宙弦的几何由绕锥形奇点的回路和乐完全确定[28]【文献确立】。't Hooft（2008）的"局部有限引力模型"以直线弦源构造分段平直时空，结构上即 Regge 型几何[29]【文献确立】。

**关联要点**：锥形时空的和乐 $\exp(i\delta\times\text{旋转生成元})$ 与贝里相位 $\exp(i\gamma)$ 同为"闭合回路上的角度指数化"。这是贝里相位与亏角在物理对象上的确定交汇，无需任何构造假设。

#### 4.3.2 引力场中的贝里相位与引力 Aharonov–Bohm 效应

- Overstreet–Asenbaum–Curti–Kim–Kasevich（2022）在《科学》报道引力 Aharonov–Bohm 效应的观测：原子干涉仪两臂通过引力势不同但时空曲率为零的区域，测得非零且不可归约为偏折效应的相位差[30]【文献确立】。这确立了"引力几何信息以相位（而非力）形式进入量子力学"的实验事实。
- 中子自旋–转动耦合的贝里相位提案：地球自转频率涨落可经中子自旋的贝里拓扑相位探测[36]【文献确立，理论提案】。

#### 4.3.3 涌现时空纲领：贝里几何作为时空的候选来源

- Volovik（《氦滴中的宇宙》2003）系统论证：相对论不变性与规范结构可在量子液体中作为**涌现**现象出现，准粒子的贝里相位结构是涌现规范场的微观来源[31]；第二类外尔半金属中倾斜外尔锥可实现事件视界与霍金辐射的类比（Volovik 2016）[32]【文献确立】。
- Gao–Yang–Niu（2014）：贝里曲率修正后的布洛赫电子相空间具有非对易几何结构，半经典动力学可等效地用修改的相空间度规描述[33]【文献确立】。
- Copinger–Morales（2022）：从动量空间贝里相位出发构造与电磁场耦合的动力学规范场，得到"贝里启发的涌现时空"[34]【文献确立，属探索性文献】。

**性质判断**：涌现时空纲领是"把时空几何还原为量子态几何（贝里型结构）"的系统性研究纲领，方向上与本框架"物质自组织同步展开为时空"的存在论立场同向，但该纲领自身仍属探索阶段，未确立为物理。

#### 4.3.4 最接近的直接文献

Binder（2002，预印本）讨论锥形度规的 Aharonov–Bohm 亏角与贝里相位的相互作用（粒子在锥面上的量子力学中两者互相修正以恢复单值性）[35]【文献确立，预印本级】。这是检索到的唯一同时显式处理"亏角 ↔ 贝里相位"的工作，但未涉及 Regge 微积分或离散引力。

### 4.4 直接连接文献的缺失与关联的性质【诚实声明】

以"Berry phase Regge calculus"、"Berry curvature discrete gravity"、"geometric phase lattice gravity"等检索式系统检索后，**未找到直接建立贝里曲率与 Regge 微积分对应关系的文献**。因此：

- 贝里曲率与 Regge 曲率的关联是**结构性的**——共享 §4.1 的数学骨架（联络—曲率—和乐、曲率测度→拓扑不变量），这是范畴级严格事实；
- 不是**文献性的**——不存在任何文献建立过两者的等式、映射或换算；§4.3 的交点（锥形时空）是间接交汇，非直接对应；
- 任何把两者等同或换算的陈述（包括本框架内部的对接）都属构造性假设，必须如此标注。

---

## 5. 与 CQM 框架的对接

### 5.1 项目既有表述清单（原文定位）

| 表述 | 位置 | 性质 |
|:---|:---|:---|
| $W_v^{(\ell)} = \exp(i\delta_v^{(\ell)}\hat{T}_\ell)$，和乐平庸化 = 稳定构型 | `09 精细引力（FG）/FG_纤维丛理论.md` §3.1 | 框架结构（数学上为 Wilson 环） |
| 一个联络生成两种曲率：Regge 角亏 + 伴丛曲率 $F_\ell = d\mathcal{A}_\ell + \mathcal{A}_\ell\wedge\mathcal{A}_\ell$ | `09 精细引力（FG）/FG_纤维丛理论.md` §3 | 框架结构 |
| "内禀角亏 $\delta_{\text{intrinsic}}$ 无内部来源——当前只能引入外部 DFT Berry 曲率" | `08 超导/CQM_超导_FG层级同步算符体系.md` §1.2 | 【CQM 构造假设】（外部输入依赖） |
| "DFT Berry 曲率是电子波函数在动量空间的几何相位——在 CQM 语言中它是伴丛和乐的某种唯象近似" | 同上 §9.3 | 【CQM 构造假设】 |
| 黎曼–西格尔相角 $\theta(t)$ = "同步基态的 Berry 相位" | `01 核心理论/CQM_核心_因果网络同步理论.md` §3.7 | 【CQM 构造假设】 |
| 和乐 = 共形场论单值性（monodromy），$h = \delta_v\hat{T}/2\pi$ | `09 精细引力（FG）/FG_纤维丛理论.md` §9.4 | 【CQM 构造假设】（映射构造） |
| $R_{\text{eff}} = 2\delta_v/A_{\text{dual}}$（亏角 → 有效里奇标量） | `BridgeTheorems.lean` | 二维 Regge 曲率密度的标准关系【标准数学】 |
| Regge 底空间几何指定自守形式 | 项目全局共识（2026-08 修正） | 【CQM 构造假设】 |

### 5.2 严格数学同构层面【标准数学】

无需任何物理假设即可陈述的同构：

1. **Wilson 环同构**：$W_v^{(\ell)} = \exp(i\delta_v^{(\ell)}\hat{T}_\ell)$ 是主丛 $P(M_\ell, G_\ell)$ 上离散联络的和乐；贝里相位 / 非阿贝尔贝里和乐是厄米（向量）丛上贝里联络的和乐。两者是同一数学对象（Wilson 环）在不同底空间与结构群上的实例。若把层级联络 $\mathcal{A}_\ell$ 形式地视为某参数流形上的贝里联络，则 $F_\ell = d\mathcal{A}_\ell + \mathcal{A}_\ell\wedge\mathcal{A}_\ell$ 恰是 Wilczek–Zee 非阿贝尔贝里曲率[3]。
2. **曲率测度—拓扑同构**：二维底空间角亏满足 $\sum_v\delta_v = 2\pi\chi$（离散 Gauss–Bonnet）【标准数学】，与布里渊区陈数 $C = \frac{1}{2\pi}\int\Omega$[5] 同为 Chern–Weil 型"曲率积分 = 拓扑不变量"。
3. **锥形和乐同构**：单铰链 Regge 几何 ≅ 锥形时空（宇宙弦）[27][28]；锥形和乐与贝里相位同为闭合回路上的角度指数化（§4.3.1）。

### 5.3 CQM 构造假设层面【CQM 构造假设】

文献调研表明以下对接**无文献对应**，属框架构造，须诚实标注：

1. **"密度泛函理论贝里曲率 = 伴丛和乐的唯象近似"（§9.3）**：文献分析显示两者测的是**不同空间的几何数据**——密度泛函理论贝里曲率是动量空间（布里渊区）能带几何[7][18]；$\delta_{\text{intrinsic}}$ 是实空间分子几何偏离理想杂化几何的球面角亏（`08 超导/CQM_超导_FG层级同步算符体系.md` §1.2 诊断）。"动量空间带几何 ↔ 实空间组织几何"的等同性是构造假设，文献既未建立也未否定。该假设在数学范畴上自洽（同为曲率—和乐结构），但跨空间映射本身无先例。
2. **"黎曼–西格尔相角 = 同步基态贝里相位"（§3.7）**：$\theta(t)$ 是 $\zeta(1/2+it)$ 的辐角（$\zeta$ 的相位），将其读作贝里相位是框架构造。相容的历史谱系见 §5.5，但无文献直接支持该读法。
3. **"和乐 = 共形单值性"（§9.4）**：纤维丛和乐本征值与共形块 monodromy 本征值的映射是框架构造（该文档自身的定位即是"建立严格定量映射，消除缺口"的目标陈述）。

### 5.4 文献对 $\delta_{\text{intrinsic}}$ 断链的启示

超导第一性链的断点（§1.2）：

$$\text{材料结构} \xrightarrow{\text{Regge几何}} \delta_v \xrightarrow{\text{?}} \Delta\delta_0^{\text{eff}} \xrightarrow{\theta_D} T_c$$

文献给出三条对照：

1. **几何信息控制超导转变温度有确立先例**：平带超导文献簇（§2.4）证明超流刚度与转变温度由量子几何（量子度规的布里渊区积分）决定[10][11][12][14][15]——"能带色散之外的几何信息进入超导"这一纲领性立场与本框架"Regge 几何 → 角亏 → $T_c$"链条**方向一致**。
2. **但几何量的类型不同**：文献中控制超导的是量子几何张量的**对称部分（量子度规）**，而非贝里曲率（反对称部分）[10][14]。这提示：若 CQM 框架内"贝里曲率 ↔ 内禀角亏"的构造对应成立，则需检验所缺的内部信息是否更接近"度规型"而非"曲率型"——即分子层级同步算符应编码的可能是完整量子几何张量型的信息。这与 §1.2 自身的诊断（"中间的分子层级只有嘉当矩阵而没有同步算符"）相容：断链缺的是层级化的几何信息载体，不单是曲率数据。
3. **外部输入的可操作性与临时性**：外尔插值计算密度泛函理论贝里曲率是标准成熟流程[18][20]，"外部输入"在计算上无障碍；但按 §9.3 的框架定位，该输入最终应被分子 FG 同步算符谱的内部来源替代——文献现状（无动量空间 ↔ 实空间组织几何的映射先例）意味着替代机制必须在框架内构造，无法从文献移植。

### 5.5 历史注记：M. V. Berry 的双重线索

本框架中已有的贝里线索（Berry–Keating 对应 $\hat{H}_{BK} = \frac{1}{2}(x\hat{p}+\hat{p}x)$，GL(1) 层谱结构，`05 方法论与批判/CQM_方法论_HilbertPolya批判.md` §2.1 等）与本文调研的贝里曲率**同出于一人**：M. V. Berry 既是 1984 年几何相位论文的作者[1]，也是"黎曼 zeta 函数：量子混沌模型"（1986）[37]、黎曼零点数方差半经典公式（1988）[37]与 Berry–Keating 算符（1999）[38]的作者。两条线索在文献史中本就交汇于量子混沌与谱理论（黎曼零点的 GUE 统计 ↔ 量子混沌能级）[37]【文献确立】。因此框架同时使用贝里的两条工作线索不是巧合拼接，而是同一作者研究纲领的两翼；`01 核心理论/CQM_核心_因果网络同步理论.md` §3.7 把黎曼–西格尔相角读作贝里相位，与这一谱系相容（该读法本身仍属构造假设）。

### 5.6 曲率角色的分工与本源判定

针对"体系应使用哪种曲率"的问题，本节给出分析：**框架不需要在两类曲率之间选择——两者本就是同一联络上的分工结构，且关系是严格的**。

#### 5.6.1 分工结构：度量形式与响应形式

FG"一个联络生成两种曲率"（`09 精细引力（FG）/FG_纤维丛理论.md` §3）不是冗余设计，而是度量—响应分工（存在论层级分析见 §5.6.3）：

| | Regge 角亏 $\delta_v$ | 伴丛曲率 $F_\ell = d\mathcal{A}_\ell + \mathcal{A}_\ell\wedge\mathcal{A}_\ell$ |
|:---|:---|:---|
| 角色 | **底空间曲率（度量形式，发生学入口）**：物质组织内禀不均匀性的几何度量，联络由它生成 | **响应曲率（动力学）**：进入运动方程 $D*F = *J_\Phi$，按规范场规则独立演化 |
| 挂载的可观测 | 不确定性关系、固有时流速、声子谱、$T_c$ 链 | 同步场强、物质流耦合 |

#### 5.6.2 关联的严格性：和乐作为焊点

两类曲率由和乐焊接【标准数学】：

$$W_v^{(\ell)} = \exp(i\delta_v^{(\ell)}\hat{T}_\ell)$$

$\delta_v$ 提供角度（底空间几何数据），$\hat{T}_\ell$ 提供生成元（纤维上的表示数据），指数化即 Wilson 环。伴丛曲率 $F_\ell = d\mathcal{A}_\ell + \mathcal{A}_\ell\wedge\mathcal{A}_\ell$ 与 Wilczek–Zee 非阿贝尔贝里曲率[3]公式完全同型（§4.1、§5.2）。严格陈述：**框架的伴丛曲率本身就是非阿贝尔贝里型曲率的实例，Regge 角亏是同一联络在底空间上的和乐角度**。因此体系的正确使用方式是同时使用两者：Regge 角亏做发生学入口（联络由它生成），贝里型做响应（按规范场规则独立演化）——两者的存在论层级区分见 §5.6.3。

#### 5.6.3 三层本体结构：承担者、度量形式与响应形式【CQM 框架立场】

一个必要的精确化（修正"本源 vs 派生"的粗糙二分）：**Regge 曲率不是时空曲率**——时空曲率是 GR 的 $R^\rho_{\sigma\mu\nu}$，受 $G_N$ 重组、量级 $\sim 10^{-43}$；Regge 角亏度量的是**物质自组织空间形态**的内禀不均匀性，量级 $O(1)$、不受 $G_N$ 重组（`01 核心理论/CQM_核心_三种引力存在论前提.md` §3.2–§3.3）。

框架原文的定位支持进一步的层级区分（`01 核心理论/CQM_核心_三种引力存在论前提.md` §3.3、§7、§8）：

- "**底空间是物质自组织的空间形态本身**"（§3.3）；
- "**角亏是物质组织形态的缺陷度量**。源的位置是内禀的：**源即底空间自身的结构**"（§3.3）；
- "**物质晶胞是本体，Regge 晶胞是其几何映射，二者不可混同**"（§8）。

由此得到三层本体结构：

$$\underbrace{\text{物质自组织的因果结构}}_{\text{承担者（本体）}} \;\xrightarrow{\text{几何度量}}\; \underbrace{\delta_v}_{\text{度量形式}} \;\xrightarrow{\text{生成}}\; \underbrace{\mathcal{A}_{\text{FG}} \to F_\ell}_{\text{响应形式（贝里型）}} \;\rightarrow\; \underbrace{v_\tau,\ \Delta u\cdot\Delta\delta_v,\ \text{声子谱},\ T_c}_{\text{表现}}$$

- **承担者（本体）**：物质自组织的因果结构——"源即底空间自身的结构"。固有时流速的承担者正是它：`CouplingSpace.lean` 的原话是"因果限制越强（$\delta$ 越大）固有时被压扁越甚，$v_\tau\to 0$（**与黑洞冻结一致**）"——压缩固有时的承担者是因果条件结构本身，$\delta_v$ 只是其几何度量，$v_\tau=\sqrt{1-\beta\delta_v}$ 是从度量到表现的定律。黑洞冻结一致性恰好佐证承担者是因果结构而非其几何描述。
- **度量形式**：Regge 角亏 $\delta_v$——本体的几何映射（"物质晶胞是本体，Regge 晶胞是其几何映射"），同时是**发生学入口**：联络 $\mathcal{A}_{\text{FG}}$ 由 Regge 曲率生成（§3.3 双曲率结构）。Regge 曲率是"表现"（本体的几何表现）与"入口"（响应的生成源）的双重角色，而不是存在论终点。
- **响应形式（贝里型）**：$F_\ell = d\mathcal{A}_\ell + \mathcal{A}_\ell\wedge\mathcal{A}_\ell$——由度量形式生成、按规范场规则独立演化的动力学结构。

**本源判定的修正**：本源既非 Regge 曲率也非贝里型曲率，而是物质自组织的因果结构；两类曲率都是"形式"——对比不是"本源 vs 派生"，而是"度量形式 vs 响应形式"。这一修正使"一个联络生成两种曲率"的结构获得清晰解释：**联络正是度量形式与响应形式相遇的枢纽**。涌现时空纲领（Volovik 等[31][34]）取相反方向（把时空几何还原为量子态几何）——两条路线方向对冲；CQM 的取向是存在论选择，不是文献裁决，此处如实标注。

#### 5.6.4 Mead–Truhlar 构型空间机制：贝里相位反作用实空间几何的文献先例

分子物理中存在"贝里相位反作用于实空间几何"的确立机制【文献确立】：

- Herzberg 与 Longuet-Higgins（1963）发现：绕核构型空间中的锥形交叉（conical intersection）一周，绝热电子波函数累积 $\pi$ 相位[39]。
- Mead 与 Truhlar（1979）证明：为保持总波函数单值性，核运动薛定谔方程必须引入一个矢量势——几何相位以确定的矢量势形式反作用于实空间分子几何（分子 Aharonov–Bohm 效应）[40]。

**对框架的意义**：核构型空间正是 Regge 剖分三角化的对象（分子层级底空间 $M_{\text{mol}}$）——Mead–Truhlar 机制是"构型空间贝里相位 → 修正实空间几何"的文献先例，方向与 $\delta_{\text{intrinsic}}$ 的内部来源需求一致。但先例方向一致不等于映射已建立，此处对应关系属【CQM 构造假设】。

**关键区分**：Mead–Truhlar 机制处理的是**构型空间**贝里结构，不是当前外部输入的**动量空间**密度泛函理论贝里曲率[18]。后者与实空间组织几何的映射无文献先例（§5.3）；前者到实空间几何的反作用有确立机制。这提示 $\delta_{\text{intrinsic}}$ 的对口候选更可能是**分子构型空间上的贝里/和乐结构**，而非动量空间能带几何。

#### 5.6.5 三层结构下的解读：响应形式向度量形式的回流

§5.6.3 的三层结构（承担者 → 度量形式 → 响应形式 → 表现）使 Mead–Truhlar 先例的定位更精确：它是**响应形式反作用于度量形式**的文献实例——电子波函数的贝里相位（响应形式，量子态几何）经矢量势修正核运动方程，从而反作用到实空间分子几何（度量形式所在的构型空间）。文献中该回路的完成依赖量子态与核几何的 Born–Oppenheimer 耦合[40]；对 CQM 而言，对应的耦合枢纽正是"一个联络生成两种曲率"的联络 $\mathcal{A}_{\text{FG}}$。

**候选机制（构造性研究假设，非文献结论）**：$\delta_{\text{intrinsic}}$ 的内部来源可能不是度量形式内部的额外结构，而是**响应形式向度量形式的回流**——分子层级伴丛曲率 $F_{\text{mol}}$ 的和乐经联络反馈进底空间角亏，使 $\delta_{\text{intrinsic}}$ 成为框架内可从谱结构读出的量。该机制与 §1.2 的断链诊断相容（缺的是分子 FG 同步算符，即承载该回流的层级化谱载体）；其成立与否是开放问题 1 的检验对象，此处仅作为假设记录。

---

## 6. 结论

1. 贝里曲率与 Regge 曲率共享严格的数学骨架：联络—曲率—和乐三位一体（Ambrose–Singer 定理）、曲率通量 = 环路和乐（Stokes 定理）、曲率测度积分 = 拓扑不变量（陈数 / 离散 Gauss–Bonnet）【标准数学】。
2. 两者的确定物理交点是锥形时空（宇宙弦亏角和乐 ≅ 单铰链 Regge 几何）；引力 Aharonov–Bohm 效应（2022 实验观测）确立引力几何以相位形式进入量子力学【文献确立】。
3. **不存在直接连接两类曲率的文献**；涌现时空纲领（Volovik 等）是最接近的系统性纲领，但属探索阶段。两者的关联是结构性的，不是文献性的【诚实声明】。
4. 本框架的伴丛和乐 $W_v = \exp(i\delta_v\hat{T}_\ell)$ 与贝里和乐同属 Wilson 环范畴【标准数学】；"密度泛函理论贝里曲率 = 伴丛和乐唯象近似"与"$\delta_{\text{intrinsic}}$ 外部输入"是【CQM 构造假设】，其跨空间（动量空间 ↔ 实空间）映射无文献先例。存在论层级上（§5.6.3）：本源是物质自组织的因果结构，Regge 角亏是其度量形式（兼发生学入口），伴丛曲率是响应形式——"一个联络生成两种曲率"的联络正是两种形式相遇的枢纽。
5. 量子几何 × 平带超导文献（转变温度由量子度规决定）为 $\delta_{\text{intrinsic}}$ 断链给出方向一致的文献对照，并提示缺失的内部信息可能是量子几何张量完整结构（度规 + 曲率）而非单独贝里曲率——这是框架内可研究的问题。

---

## 7. 开放问题（记录备查）

1. $\delta_{\text{intrinsic}}$ 的内部来源是否可由**分子构型空间**的贝里/和乐结构给出：绕锥形交叉类简并点的 Mead–Truhlar 型和乐[39][40]能否在分子 FG 层级谱中表现为内禀角亏的谱贡献？具体候选机制是**响应形式向度量形式的回流**（§5.6.5）：分子层级伴丛和乐经联络 $\mathcal{A}_{\text{FG}}$ 反馈进底空间角亏——文献先例确立的是反作用方向[40]，回流机制的构造与检验属框架内研究。
2. 若问题 1 成立，动量空间外部输入（密度泛函理论贝里曲率[18]）是应被构型空间内部来源**替代**，还是与后者**互补**？——即 §9.3"伴丛和乐唯象近似"定位（`08 超导/CQM_超导_FG层级同步算符体系.md`）的两种可能结局，何者成立？
3. 锥形时空和乐 ↔ Regge 铰链 ↔ 贝里相位的三角对应能否在本框架层级结构（元素 / 分子 / 晶胞 FG）中严格化？
4. 黎曼–西格尔相角 $\theta(t)$ 作为贝里相位的构造读法，能否通过与 Berry 量子混沌谱系[37]的显式对接（零点数方差、周期轨道展开）获得更严格的表述？
5. 二维 Gauss–Bonnet（角亏总和 = 欧拉示性数）与陈数（贝里曲率积分）的平行，是否可在"Regge 底空间几何指定自守形式"的构造链中用作拓扑条件的一致性检验？

---

## 参考文献

**贝里曲率基础与能带物理**

[1] M. V. Berry, "Quantal phase factors accompanying adiabatic changes", *Proc. R. Soc. Lond. A* **392**, 45–57 (1984). https://royalsocietypublishing.org/doi/10.1098/rspa.1984.0023
[2] B. Simon, "Holonomy, the quantum adiabatic theorem, and Berry's phase", *Phys. Rev. Lett.* **51**, 2167–2170 (1983). https://doi.org/10.1103/PhysRevLett.51.2167
[3] F. Wilczek, A. Zee, "Appearance of Gauge Structure in Simple Dynamical Systems", *Phys. Rev. Lett.* **52**, 2111–2114 (1984). https://doi.org/10.1103/PhysRevLett.52.2111
[4] J.-P. Provost, G. Vallee, "Riemannian structure on manifolds of quantum states", *Commun. Math. Phys.* **76**, 289 (1980).
[5] D. J. Thouless, M. Kohmoto, M. P. Nightingale, M. den Nijs, "Quantized Hall conductance in a two-dimensional periodic potential", *Phys. Rev. Lett.* **49**, 405–408 (1982). https://ui.adsabs.harvard.edu/abs/1982PhRvL..49..405T/abstract
[6] R. Karplus, J. M. Luttinger, "Hall Effect in Ferromagnetics", *Phys. Rev.* **95**, 1154 (1954).
[7] D. Xiao, M.-C. Chang, Q. Niu, "Berry phase effects on electronic properties", *Rev. Mod. Phys.* **82**, 1959 (2010). https://ui.adsabs.harvard.edu/abs/2010RvMP...82.1959X/abstract
[8] N. Nagaosa, J. Sinova, S. Onoda, A. H. MacDonald, N. P. Ong, "Anomalous Hall effect", *Rev. Mod. Phys.* **82**, 1539 (2010). https://ui.adsabs.harvard.edu/abs/2010RvMP...82.1539N/abstract （arXiv:0904.4154）
[9] X. Wan, A. M. Turner, A. Vishwanath, S. Y. Savrasov, "Topological semimetal and Fermi-arc surface states in the electronic structure of pyrochlore iridates", *Phys. Rev. B* **83**, 205101 (2011).

**量子几何与超导电性**

[10] S. Peotta, P. Törmä, "Superfluidity in topologically nontrivial flat bands", *Nat. Commun.* **6**, 8944 (2015). https://arxiv.org/abs/1506.02815
[11] A. Julku, S. Peotta, T. I. Vanhala, D.-H. Kim, P. Törmä, "Geometric origin of superfluidity in the Lieb lattice flat band", *Phys. Rev. Lett.* **117**, 045303 (2016). https://arxiv.org/abs/1603.03237
[12] L. Liang et al., "Band geometry, Berry curvature and superfluid weight", *Phys. Rev. B* **95**, 024515 (2017). https://doi.org/10.1103/PhysRevB.95.024515
[13] X. Hu, T. Hyart, D. I. Pikulin, E. Rossi, "Geometric and conventional contribution to the superfluid weight in twisted bilayer graphene", *Phys. Rev. Lett.* **123**, 237002 (2019). https://doi.org/10.1103/PhysRevLett.123.237002
[14] P. Törmä, S. Peotta, B. A. Bernevig, "Superconductivity, superfluidity and quantum geometry in twisted multilayer systems", *Nat. Rev. Phys.* **4**, 528–542 (2022). https://doi.org/10.1038/s42254-022-00466-y
[15] H. Tian et al., "Evidence for Dirac flat band superconductivity enabled by quantum geometry", *Nature* **614**, 440–444 (2023). https://doi.org/10.1038/s41586-022-05576-2

**第一性原理计算方法**

[16] R. D. King-Smith, D. Vanderbilt, "Theory of polarization of crystalline solids", *Phys. Rev. B* **47**, 1651 (1993). https://doi.org/10.1103/PhysRevB.47.1651
[17] N. Marzari, D. Vanderbilt, "Maximally localized generalized Wannier functions for composite energy bands", *Phys. Rev. B* **56**, 12847 (1997). https://doi.org/10.1103/PhysRevB.56.12847
[18] N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, D. Vanderbilt, "Maximally localized Wannier functions: Theory and applications", *Rev. Mod. Phys.* **84**, 1419 (2012). https://doi.org/10.1103/RevModPhys.84.1419
[19] Y. Yao et al., "First principles calculation of anomalous Hall conductivity in ferromagnetic bcc Fe", *Phys. Rev. Lett.* **92**, 037204 (2004). https://doi.org/10.1103/PhysRevLett.92.037204
[20] X. Wang, J. R. Yates, I. Souza, D. Vanderbilt, "Ab initio calculation of the anomalous Hall conductivity by Wannier interpolation", *Phys. Rev. B* **74**, 195118 (2006). https://arxiv.org/abs/cond-mat/0608257

**Regge 微积分与离散引力**

[21] T. Regge, "General relativity without coordinates", *Nuovo Cim.* **19**, 558 (1961). https://www.osti.gov/biblio/4028412
[22] J. Cheeger, W. Müller, R. Schrader, "On the curvature of piecewise flat spaces", *Commun. Math. Phys.* **92**, 405–454 (1984).
[23] T. Regge, R. M. Williams, "Discrete structures in gravity", *J. Math. Phys.* **41**, 3964 (2000). https://arxiv.org/abs/gr-qc/0012035
[24] J. W. Barrett, D. Oriti, R. M. Williams, "Tullio Regge's legacy: Regge calculus and discrete (quantum) gravity", arXiv:1812.06193 (2019). https://arxiv.org/abs/1812.06193
[25] H. W. Hamber, *Quantum Gravitation — The Feynman Path Integral Approach* (Springer, 2009)；"Quantum gravity on the lattice", *Gen. Relativ. Gravit.* **41**, 1959 (2009). https://arxiv.org/abs/0901.0964
[26] B. Bahr, B. Dittrich, "Regge calculus from a new angle", arXiv:0907.4325 (2009). https://arxiv.org/abs/0907.4325

**引力场中的贝里相位、锥形时空与涌现时空**

[27] A. Vilenkin, "Gravitational field of vacuum domain walls and strings", *Phys. Rev. D* **23**, 852 (1981).
[28] M. van de Meent, "The Geometry of massless cosmic strings", arXiv:1211.4365 (2013). https://arxiv.org/abs/1211.4365
[29] G. 't Hooft, "A locally finite model for gravity", *Found. Phys.* **38**, 733 (2008). https://arxiv.org/abs/0804.0328
[30] C. Overstreet, P. Asenbaum, J. Curti, M. Kim, M. A. Kasevich, "Observation of a gravitational Aharonov-Bohm effect", *Science* **375**, 226–229 (2022). https://www.science.org/doi/10.1126/science.abl7152
[31] G. E. Volovik, *The Universe in a Helium Droplet* (Oxford University Press, 2003). https://global.oup.com/academic/product/the-universe-in-a-helium-droplet-9780198507826
[32] G. E. Volovik, "Black hole and Hawking radiation by type-II Weyl fermions", *JETP Lett.* **104**, 645 (2016). arXiv:1610.00521
[33] Y. Gao, S. A. Yang, Q. Niu, "Field induced positional shift of Bloch electrons and its dynamical implications", *Phys. Rev. Lett.* **112**, 166601 (2014).
[34] P. Copinger, P. Morales, "Emergent spacetime from a Berry-inspired dynamical gauge field coupled to electromagnetism", arXiv:2211.14165 (2022). https://arxiv.org/abs/2211.14165
[35] B. Binder, "Iterative Interplay between Aharonov-Bohm Deficit Angle and Berry Phase", preprint (philsci-archive, 2002). https://philsci-archive.pitt.edu/810/
[36] "Neutron-gravity interferometry experiment: testing Earth's rotating frequency fluctuations via neutron Berry's phases due to spin-rotation couplings", arXiv:physics/0305108 (2003). https://arxiv.org/abs/physics/0305108

**量子混沌与黎曼零点（历史谱系）**

[37] M. V. Berry, "Riemann's Zeta function: A model for quantum chaos?", in *Quantum Chaos and Statistical Nuclear Physics*, Lecture Notes in Physics vol. 263 (Springer, 1986)；M. V. Berry, "Semiclassical formula for the number variance of the Riemann zeros", *Nonlinearity* **1**, 399 (1988). 综述来源：http://var.scholarpedia.org/article/Riemann_zeros_and_quantum_chaos
[38] M. V. Berry, J. P. Keating, "The Riemann zeros and eigenvalue asymptotics", *SIAM Rev.* **41**, 236 (1999).

**分子几何相位（构型空间桥梁）**

[39] G. Herzberg, H. C. Longuet-Higgins, "Intersection of potential energy surfaces in polyatomic molecules", *Discuss. Faraday Soc.* **35**, 77 (1963).
[40] C. A. Mead, D. G. Truhlar, "On the determination of Born-Oppenheimer nuclear motion wave functions including complications due to conical intersections and identical nuclei", *J. Chem. Phys.* **70**, 2284 (1979).

**框架内部文档（对接分析引用源）**

- `09 精细引力（FG）/FG_纤维丛理论.md` §3（一个联络生成两种曲率）、§3.1（和乐）、§9.4（和乐 = 共形单值性）
- `08 超导/CQM_超导_FG层级同步算符体系.md` §1.2（$\delta_{\text{intrinsic}}$ 断链诊断）、§9.3（与贝里曲率的方法论定位）
- `01 核心理论/CQM_核心_因果网络同步理论.md` §3.7（黎曼–西格尔公式 → 几何相位）
- `01 核心理论/CQM_核心_三种引力存在论前提.md` §3.3–§3.4（Regge 角亏进入不确定性关系）
- `06 Lean形式化/Superconductivity/BridgeTheorems.lean`（$R_{\text{eff}} = 2\delta_v/A_{\text{dual}}$ 桥接定理）
- `06 Lean形式化/Superconductivity/MolecularGeometry.lean`（reggeDeficitAngle 定义）
- `05 方法论与批判/CQM_方法论_HilbertPolya批判.md` §2.1（Berry–Keating 对应）

> **调研记录说明**：文献检索与核实于 2026-09-08 完成，采用多来源交叉验证（出版商官方页面 / arXiv / NASA 天体物理数据系统 / 引用数据库）。反常霍尔效应综述 [8] 的作者列表经直接核实为五作者（Nagaosa–Sinova–Onoda–MacDonald–Ong）。个别经典文献（[4][6][9][22][27][33][39][40]）未附直接网络链接，其书目信息经多个二级来源交叉确认。§5.6 与开放问题 1–2 的增补（含 [39][40] 的核实：Herzberg–Longuet-Higgins π 相位发现与 Mead–Truhlar 矢量势机制的归属，经分子动力学几何相位综述与明尼苏达大学出版物页面确认）于同日完成。§5.6.3 三层本体结构修订（承担者/度量形式/响应形式，依据 `01 核心理论/CQM_核心_三种引力存在论前提.md` §3.3、§7、§8 原文定位与 `CouplingSpace.lean` 黑洞冻结一致性注释）与 §5.6.5 回流候选机制亦于同日完成。
