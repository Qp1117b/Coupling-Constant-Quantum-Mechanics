# Theta 对应与 Dirichlet GRH 新证明：CQM 外部对照研究

**作者**：ruster

**框架**：耦合常数量子力学（CQM）

> **前沿研究定位声明**：该文档属“04 前沿研究”，遵循**单向基础依赖原则**——
> 1. 以下提出的候选对接**允许与项目其它文档不一致**（前沿性），但凡引用框架既有基础表述（量纲定义、朗兰兹分层、自守形式定位、RH 路线图、相变量子 $☯$ 等），一律以既有文档原文为准，此处不修改基础；
> 2. 若前沿论点与基础已有表述**冲突**，以基础为准，前沿论点按诠释层处理并明确标注张力；
> 3. 全文采用五级状态标注：**【文献确立】**（外部文献直接确立）、**【标准数学】**（教科书级数学事实）、**【CQM 框架基础】**（框架既有基础表述）、**【CQM 构造假设】**（框架内新提出的猜想，未经证明）、**【哲学诠释】**（存在论/哲学层面的解读，不属数学或物理断言）；
> 4. 本文**不新开缺口编号、不升级既有缺口**（C、G2–G8、G9–G22、N1–N4 及链层编号状态不变）；末尾开放问题仅为外部对照待核查项；
> 5. 术语首次出现时给出全称并括注简称，后文统一用简称。

> **与核心文档的分工**：本专论只承担两类内容——**① 外部文献精读**（Theta 对应标准工具、322 页 Dirichlet GRH 证明骨架、Lean 验证状态）；**② 该文献与 CQM 的交叉分析**。量纲—群论—自守的权威口径见 `01 核心理论/CQM_核心_量纲与群论.md`，朗兰兹分层见 `01 核心理论/CQM_核心_朗兰兹分层共振与相变量子.md`，RH 路线图见 `04 前沿研究/CQM_前沿研究_黎曼猜想证明思路.md`；本专论以引用方式使用，不重复展开。

**调研记录**：外部文献检索与原文核对于 2026-11-27 完成（arXiv / GitHub 原始仓库 / Waterloo 核对页 / MIT 验证页交叉验证）。外部文献 PDF 存于 `归档/一体化研究/文献/`：

| 缩写 | 文件 | 出处 |
|:---|:---|:---|
| GRH-322 | `../归档/一体化研究/文献/GRH_Natural_Language_Proof_Yui_322p.pdf` | `yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis` 仓库内文件 proof-of-GRH.pdf；Alpöge 与 Claude 著，Kaiwen Jin 作 Lean→自然语言转写，322 页 |
| Theta-Gan | `../归档/一体化研究/文献/Theta_Correspondence_Gan_arXiv2303.14919.pdf` | Wee Teck Gan, *Explicit Constructions of Automorphic Forms: Theta Correspondence and Automorphic Descent*, arXiv:2303.14919 |
| RH-explained | `../归档/一体化研究/文献/Alpoge_Claude_RH_explained_Rubinstein_v2.pdf` | Michael Rubinstein, *The Alpöge–Claude proof of the Riemann hypothesis explained for the Riemann zeta function*, v2 工作稿（265 页，2026-11-22） |

---

## 1. 外部文献精读

### 1.1 Theta 对应（Theta correspondence / theta lift）的标准结构【文献确立】

Theta 对应是自守形式理论中把一个群上的自守表示转移到另一个群上表示的标准操作，其“翻译官”式的核积分结构见 Gan 讲义（arXiv:2303.14919）：

1. **约化对偶对**：取二次空间 $(V,q)$ 与辛空间 $(W,\langle-,-\rangle_W)$，得 $\mathrm O(V)\times\mathrm{Sp}(W)\longrightarrow\mathrm{Sp}(V\otimes W)$，两者在 $\mathrm{Sp}(V\otimes W)$ 中互为中心化子。约化对偶对由 Howe 分类，另有酉群、四元数酉群等对偶对。
2. **Weil 表示与 metaplectic 覆盖**：需要 $\mathrm{Sp}(\mathbb W)$ 的唯一非线性二重覆盖 $\mathrm{Mp}(\mathbb W)$ 及其 Weil 表示 $\omega_{\mathbb W,\psi}$；Schrödinger 模型实现于 Schwarz–Bruhat 函数空间 $\mathcal S(\mathbb Y)$，Weyl 元素 $w$ 的作用由 Fourier 变换给出。
3. **Theta 核与全局提升**：$\theta(\phi)(g)=\sum_{y\in\mathbb Y_k}(\omega_\psi(g)\phi)(y)$，全局提升为积分
   $$\theta(\phi,f)(h)=\int_{[\mathrm{Sp}(W)]}\theta(\phi)(gh)\,\overline{f(g)}\,dg.$$
   这正是“以 theta 级数为核，把 $[O(V)]$ 上的函数转到 $[\mathrm{Sp}(W)]$ 上”的积分变换。
4. **Howe 对偶与 tower**：大 theta 提升 $\Theta(\pi)$ 有限长；小 theta 提升 $\theta(\pi)$ 非零则不可约且唯一；Rallis tower 用 Witt tower 研究非零性；Rallis 内积公式与 Siegel–Weil 公式控制全局提升的范数。

**重要限定**：theta 提升不是任意两群之间的通用翻译机——须落在约化对偶对（并涉及 metaplectic 覆盖）；提升可能为零，且有大/小 theta 之分。权威参考为 Moeglin–Vignéras–Waldspurger 专著与 Kudla 讲义；Howe、Waldspurger、Rallis 的奠基工作见 Gan 讲义参考文献。

### 1.2 322 页 Dirichlet GRH 证明的骨架【文献确立：GRH-322】

GRH-322 的主定理：对每个 Dirichlet 特征 $\chi$，$L(s,\chi)$ 在 $0<\Re s<1$ 中的零点均满足 $\Re s=1/2$；且 $L(s,\chi)\ne0$ 于 $\Re s>1/2$（主特征在 $s=1$ 的极点除外）。证明链条（依 GRH-322 §Introduction）：

1. **核心比较**：对同一族“近张成”（nearly spanning）的 theta 提升，比较其**平方余体积（squared covolume）**的两个界；
2. **上界**：来自整 theta 提升链的可除性；算术项含两个光滑素数幂余项之差及较小尺度上的修正；
3. **下界**：在每一有限嵌入选取一个反循环 twist，使其前 $m$ 次幂同时满足 Selmer 长度估计与归一化 Hecke 值界；Selmer 估计控制原 Hecke 格上 Gram 行列式的有限分母，值界控制各提升体积的比较；经加权体积恒等式与短族可控完备，对同一向量用乘积公式，公共主项抵消，余项界获得因子 $m^{-1}$，其中 $m\asymp x^{1/2}$；
4. **零点判据**：固定模数的素数定理控制较小尺度余项，留下较大尺度的单边估计；二次 twist 分离 Mellin 变换中对数导数的极点；Landau 引理排除临界线右侧零点；函数方程给出临界带内结论。

**结构判读**：该证明的引擎是“theta 提升族余体积的算术—几何双边估计”，不属于 Hilbert–Pólya 自伴算符路线；其素数信息以素数幂余项 $R_q(y)$ 与固定模数素数定理进入，最终由 Landau 引理转成零点排除。

### 1.3 验证状态的两份自然语言稿【文献确立】

- **Lean 验证**（Rubinstein 核对页、MIT Sutherland 独立验证页）：原版 175,187 个模块全部编译；五个定理仅依赖 Lean 三条标准公理；内核重放接受全部模块；独立内核 nanoda 检查 1,484,729 条声明无类型错误。2026-11-25 的精简版（约 76,000 行，794 模块）于 11-26 通过全部检查，包括六个内核的 `lake comparator --paranoid`。
- **两份自然语言稿的状态不同**：GRH-322 的仓库说明称其为“complete, unconditional natural-language proof”；Rubinstein 的 265 页 v2 工作稿则明确说明：它把主不等式 $(M)$ 与 RH **归约为十三条以经典术语陈述的假设，其中没有一条被完全证明**，并列出尚待补写部分（§I.12）。两稿作者、目标与完成度不同；本文并列登记，**不裁决**其相互关系，也不把任一份当作 CQM 内部的证明。

---

## 2. 与 CQM 的关系分层

### 2.1 Theta 对应 ↔ CQM 自守形式／朗兰兹分层【CQM 构造假设（待核查）】

CQM 权威链条为“物质（先在） $\to$ 用质数自组织 $\to$ $GL(5)$ 潜能先在 $\to$ 自组织成 $SU(5)$ 基态 $\to$ $p$ 进大小耦合分化／重组实现 $\to$ $U(1)\times SU(2)\times SU(3)$”（`CQM_核心_朗兰兹分层共振与相变量子.md` §0.1）；自守形式被定位为“属性稳定性的数学体现”（`CQM_核心_量纲与群论.md:1030`）；已有的提升对象是 $\mathrm{Sym}^4$（$\mathrm{GL}(2)\to\mathrm{GL}(5)$，见 `CQM_前沿研究_质量的量纲地位与自守来源.md` §4.2）。

**判定**：Theta 对应是**另一类**自守转移（约化对偶对之间的核积分变换），全库未检索到 theta lift／θ 核积分变换的既有口径。把它作为量纲—自守链的候选工具，只能登记为【CQM 构造假设（待核查）】；在修改核心定义前，不得写成 CQM 既有结论。

### 2.2 GRH-322 ↔ CQM 的 RH 路线图【CQM 框架基础】

CQM 的 RH 路线图是“3 个已知（算符 $\hat H=\hat D^2+1/4$、相变量子 $☯$、带误差谱带 $\mathfrak c_n=\gamma_n^2+1/4+O_n$）＋ 2 个待推（素数边界条件、经典化）”；待推 1 的长度半已由 Riemann–von Mangoldt 反解，相位半 $S(T)$ 仍是实质缺口。$☯$ 的谱表示 $\sum_n1/(\gamma_n^2+1/4)$ 是 RH 的**单向推论**，不得反用为证明（见 `CQM_前沿研究_黎曼猜想证明思路.md` 状态说明与 §诊断）。

GRH-322 的机制（theta 提升族余体积双边估计、素数幂余项、固定模数 PNT、Landau 引理）与 CQM 的机制（自伴算符、耦合空间不确定性、退相干存在性）不同；它**不提供** $S(T)$ 的相位行为，也**不提供**从素数独立推出的边界条件。判定：外部独立路线，不闭合 CQM 的两个待推项，不升级缺口。

### 2.3 量纲论定位【CQM 构造假设 / 哲学诠释】

量纲定义 3 为 $\mathrm{Dim}:=[(G_{\max}(f),\rho)]$，即基本自守量纲＝极大关系群与其作用的配对同构类，且定义顺序为**先 $f$ 后群**（`CQM_核心_量纲与群论.md:664–666,985,1024`）；自守形式体现属性稳定性，本体论纲领为“属性先在，关系潜在-显现化它”，沿关系分化／实例化／具体化三环节展开。

将 Theta 对应读作“关系分化”或“潜在—显在”的数学实现，属【哲学诠释】＋【CQM 构造假设】，不是既有口径。两条与权威源**直接相反**的表述——「色荷可量纲化」（权威：色荷、弱荷“故没有量纲化”，`量纲与群论.md:1034,1553`）与「极大子群 $\leftrightarrow$ 一般量纲」（权威：极大关系群 $\ne$ 极大子群，`量纲与群论.md:1024`）——按“以原（第一）文档为准”**不写入本文**。

### 2.4 术语隔离【标准数学】

CQM 中的 $\theta(T)$（Riemann–Siegel theta）、Sierra 相位 $\vartheta_n$、自伴延拓相位 $\vartheta$ 与 $\mathrm{Sym}^4$ 提升，**均非** Theta 对应／theta lift；引用时须逐处指明对象，不得混用。

---

## 3. 外部对照待核查项（不编号、不升级既有缺口）

| 待核查项 | 对象 | 状态 |
|:---|:---|:---|
| Theta 提升的非零性与 Rallis tower 能否同 CQM 的 $GL(5)$ 固定层级建立条件性对应 | Theta-Gan §4.3、§7.3 | 【待核查】 |
| 25 个坐标自由度（$\dim M_5=5\times5=25$，非量纲数）与对偶对维数是否存在结构对应 | 量纲与群论 `:764–768` | 【待核查】 |
| 极大关系群 $G_{\max}(f)=\mathrm{Stab}_{G_0,\rho}(f)$ 与 theta 核的等变映射是否可对接 | 量纲与群论 `:664–666,1024`；Theta-Gan §2.5 | 【待核查】 |
| GRH-322 的素数幂余项方法能否转写为对 $S(T)$ 的外部约束 | GRH-322 §Introduction；CQM RH 路线图待推 1 | 【待核查】 |
| GRH-322 的 322 页稿与 RH-explained 的 265 页工作稿之间的关系 | 两稿并列登记 | 【待第三方复核】 |

---

## 4. 结论

1. **工具层**：Theta 对应是标准自守工具（约化对偶对＋Weil 表示＋theta 核积分变换），把 GRH-322 的引擎定位为 theta 提升族余体积比较，有充分外部依据。
2. **框架层**：CQM 未使用该工具；既有 $\theta(T)$、$\vartheta_n$、$\mathrm{Sym}^4$ 提升与之不同。把 Theta 对应纳入量纲—自守链只能作为【CQM 构造假设（待核查）】，不得冒充既有口径。
3. **证明层**：GRH-322 与 CQM 的 RH 路线图机制不同，不闭合待推 1／待推 2；验证状态须并列登记 Lean 机器验证与自然语言稿的完成度差异。
4. **候选路径**：第 5 章给出五个可迁移外部要素与量纲论真实缺口的对接，全部为【CQM 构造假设（待推）】；其中「补 $S$ 的物质根据」最直接对应时间量纲的承载群层缺口。
5. **证明结构**：第 6 章从完整源码（22,891 行）精读出四命题装配与主项抵消机制——上界来自整除性累积的 $-m\mathcal R$，下界来自高度乘积公式的 $2D(2\mathcal B_{\mathrm{cov}}-H)$，二者相减使 $H$ 消去，余项被 $1/m$ 压制；$m\asymp\sqrt x$ 是 $m$ 与 $x/m$ 两误差的平衡点。
6. **三项转移**：稳定性可量化为 Gram 正性（$\det C_\eta>0$）、关系分化可获得"度"（链长 $m$）、主项抵消可作为无量纲化的严格模型；三项均为【待推】，且论文的算术输入层（`fit-twists`／`crystalline-defect`／`galois-rows`）在 CQM 中无对应物。
7. **同名异义**：论文的"稳定性"是代数正性，CQM 的"稳定性"是退相干稳态；二者只在"自守形式＝稳定实现"层对齐，不可互相替代，缺口 C 状态不变。
8. **边界**：本文不修改 `01–07` 的定义、数值与缺口状态；按 AGENTS.md §四.5，若后续把候选对接升格为口径修正，须重跑组织层全链构建并通过三道核查。

---

## 5. 关键要素提取：量纲论的候选突破路径

> **工作前提**：按研究要求，以「外部 GRH 证明正确」为工作前提；本提取**不**把 RH／GRH 当作 CQM 已证内容，**不**升级任何缺口。除明确标注【文献确立】或【CQM 框架基础】外，本节全部对接均为【CQM 构造假设（待推）】。

### 5.1 可迁移的五个外部要素【文献确立】

| 要素 | 外部原文要点 | 出处 |
|:---|:---|:---|
| $\Theta$1 链式 theta 提升替代重数 |  totally definite unitary groups 间 $U(X_0)\to U(X_1)\to\cdots\to U(X_m)$，“wins multiplicity $m$”，取 $m\asymp\sqrt X$；得到 $m$ 与 $x/m$ 两个竞争误差项 | alpo.ge/remark.pdf；Rubinstein 可读稿 §I.7／§I.9；GRH-322 §Introduction |
| $\Theta$2 theta 核即积分变换 | $\mathcal T_\varphi f(h)=\int_{[U(J)]}\Theta_\varphi(g,h)\,\overline{f(g)}\,dg$；Weil 表示的 Weyl 元素由 Fourier 变换实现 | Gan 讲义 §2.4–§2.5（arXiv:2303.14919）；Rubinstein 可读稿 §6.1 |
| $\Theta$3 余体积／Gram 比较 | 比较同一 theta 提升族平方余体积的上、下界；Selmer 估计控制 Hecke 格上 Gram 行列式的有限分母；乘积公式使主项抵消，余项获 $m^{-1}$ | GRH-322 §Introduction、§short-comparison |
| $\Theta$4 大／小 theta 与 Howe 对偶 | 大提升 $\Theta(\pi)$ 有限长；小提升 $\theta(\pi)$ 非零则不可约且唯一（cosocle），亦可为 $0$ | Gan 讲义 §3.1、§4.1 |
| $\Theta$5 Rallis tower／内积公式／doubling seesaw | 用 Witt tower 研究非零性二分；内积公式控制全局提升范数；seesaw 恒等式用于周期表达式 | Gan 讲义 §4.3、§7.4；GRH-322 §comparison-rallis、§seesaw |

### 5.2 对接量纲论的真实缺口（候选，非闭合）

| 量纲论缺口（权威原文） | 对应要素 | 构造提议 | 状态 |
|:---|:---|:---|:---|
| 时间 $[T]$ 为**待补锚点支**：$\mathbb Z$ 平移给出周期函数而非自守形式，须补 $S:z\mapsto-1/z$ 的物质根据；缺口在**承载群层**（`量纲与群论.md:1544–1551,1307–1309`） | $\Theta$2 | 把 $S$ 的物质根据候选为 Weil 表示 Weyl 元素 $w=\begin{pmatrix}0&1\\-1&0\end{pmatrix}$ 的 Fourier 作用：theta 核给出从 $\mathbb Z$ 平移到含 $S$ 的算术子群的提升 | 【CQM 构造假设（待推）】；须证承载群确含 $S$ 像且所得函数满足自守性 |
| 「自守形式作为数值来源」本身是**猜想**（`量纲与群论.md:46,1038,1136`） | $\Theta$4 | 把 $\Theta(\pi)$ 读作潜在实现空间、$\theta(\pi)$ 读作显在稳定实现（不可约或 $0$），cosocle 映射作为「关系显现化」的严格模型 | 【哲学诠释＋CQM 构造假设】；须与「先 $f$ 后群」一致 |
| 定义 3：$\mathrm{Dim}:=[(G_{\max}(f),\rho)]$，先 $f$ 后群；$G_{\max}(f)=\mathrm{Stab}_{G_0,\rho}(f)$（`量纲与群论.md:664–666,1024`） | $\Theta$1、$\Theta$4 | 检验 theta 提升链是否保持 $(G_{\max},\rho)$ 配对稳定性；若保持，则「属性在作用下实现为另一形式且保持一致性」获得严格模型 | 【待推】；若改变实现标识即违反权威定义 |
| $K_L$ 数值尚未定死（两条值链差 $3.3\%$，`量纲与群论.md` §6.3.1） | $\Theta$3 | 用余体积／Gram 比较给 $K_L$ 的第一性约束，而不是替换既有数值 | 【待推】；数值不改 |
| 缺口 C（退相干稳态为何是 $A_4$，`README.md:205`）、缺口 D（边-面矩阵 $E$） | $\Theta$3、$\Theta$5 | 以 $A_4$ 上自守数据的 Gram／余体积比较约束 $E$ 与 $M=E^{\mathsf T}E$ | 【待推】；**不声称闭合**缺口 C／D |

### 5.3 稳定性闭环与外部证明的覆盖边界【CQM 框架基础 + 文献确立】

CQM 内部链条（逐字）：

- `量纲与群论.md:1030`：自守形式 $f$ 满足 $f(\gamma g)=j(\gamma,g)f(g)$，是「**属性稳定性的数学体现**：建立起自守形式，属性才算真正分化、获得稳定的物理身份」。
- `量纲与群论.md:987`：属性先在 $\to$ 关系分化（极大关系群）$\to$ 实例属性 $\to$ 实例化（自守形式＝稳定性的体现）$\to$ 具体化（量纲）。
- `因果网络同步理论.md:351`：零点猜想「**是**物质自组织稳定性的**组织性定理**（退相干是稳定性的表现）」；`:358` 表中 $GL(5)$ 行对应基态自守 $L(s,\Pi)$、广义黎曼猜想（实谱条件）、$SU(5)$ 基态。
- `朗兰兹分层共振与相变量子.md:392–393`：黎曼猜想为 GL(1) 电磁因子层特例、未证明；GRH 为 GL(5) 固定层级实谱条件、未证明，是超导完整理论的存在论前提。
- `集成理论.md:33`：基态 L 函数为 $L(s,\rho_5)=\prod_p\det(1-\rho_5(\mathrm{Fr}_p)p^{-s})^{-1}$。

**外部证明的覆盖边界**：GRH-322 的标题是 *The Dirichlet generalized Riemann hypothesis*；Rubinstein 核对页写明该证明针对 **Dirichlet $L$ 函数**，Lean 五个定理对应 RH 与 Dirichlet $L$ 函数 GRH。因此外部证明覆盖的是 GL(1)／Dirichlet 层，**未覆盖** CQM 所需的 $GL(5)$ 基态自守 $L(s,\Pi)$ 的 GRH（`朗兰兹分层共振与相变量子.md:393` 明标未证明）。

**判定**：「稳定性—RH／GRH—自守形式相关，突破在这篇论文里」在 CQM 链条内部成立；但论文给出的突破是**机制**——用 theta 提升链产生重数——而不是 GL(5) 的 GRH 结论。把它移入 CQM 还需一步【CQM 构造假设（待推）】：证明 theta 提升链在 $G_{\max}(f)$ 与 $GL(5)$ 基态自守 $L(s,\Pi)$ 上非零并保持实谱条件；该步成立之前，稳定性只能保持为框架内假说性等价（`集成理论.md:1213`），不得写成已证。

### 5.4 可证伪的下一步（不编号，全部【待推】）

1. 写出时间量纲候选承载群 $\Gamma$，证明 $\Gamma$ 含 Weyl 元素像，且 $\mathbb Z$ 平移不变函数经 theta 核后成为 $\Gamma$ 自守形式；否则该路径不成立。
2. 对给定 $f$，证明 theta 提升链保持 $G_{\max}(f)$ 与其作用 $\rho$ 的配对；若改变实现标识，按「先 $f$ 后群」判为不成立。
3. 给出余体积比较对 $K_L$ 的约束式，与 §6.3.1 两条值链对照；不得直接替换数值。
4. 明确外部证明**不提供** $S(T)$ 相位与经典化；CQM 待推 1／待推 2 仍开放。
5. 证明 theta 提升链在 $GL(5)$ 基态自守 $L(s,\Pi)$ 与 $G_{\max}(f)$ 上非零并保持实谱条件；这是把外部机制转为 CQM 稳定性闭环的必要一步。在此之前，外部 Dirichlet GRH 证明不得替代 CQM 的 GL(5) GRH。
6. 任何落地必须先改 `01` 权威源，再按 AGENTS.md §四.5 重跑全链并通过三道核查；在此之前本对照仅为候选工具登记。

---

## 6. 证明结构精读：四命题装配与 $m^{-1}$ 增益

> 本章基于完整源码（`sections/` 共 22,891 行 LaTeX，29 个文件）逐节精读。凡引外部机制标【文献确立】；凡对接 CQM 标【CQM 构造假设（待推）】。本章不修改任何 CQM 口径，不升级任何缺口。

### 6.1 装配骨架：四个命题如何拼成定理【文献确立】

全文只证一条定理（`opening.tex:4–9`，`thm:grh`）：对每个 Dirichlet 特征 $\chi$，$L(s,\chi)$ 在 $0<\Re s<1$ 内的零点都在 $\Re s=1/2$。证明被拆成四个联合命题（`opening.tex:323–382`）：

| 命题 | 内容 | 位置 |
|:---|:---|:---|
| `prop:data` 比较数据的存在 | 给定 $q_0,d,\varepsilon$，构造出尺度、秩、层、扭族，且 $\lvert H\rvert+m\lvert\mathcal R\rvert\le b^2x^{99}$ | `opening.tex:330` |
| `prop:short` 短提升族（上界） | 存在近张成独立元组：$n\ge(1-4/b^2)D$，指标 $\delta\le5D\log(1+b^2)\mathcal B$，且 $\mathcal V_\sigma(y)\le\exp\{n(H-m\mathcal R+\mathcal B_{\mathrm{cov}})\}$ | `opening.tex:348` |
| `prop:long` 余体积下界 | 若 $\mathcal V_\sigma(y)\le e^{V_{\mathrm{up}}}$，则 $D(H-3\mathcal B_{\mathrm{cov}})\le V_{\mathrm{up}}+2\delta$ | `opening.tex:363` |
| `prop:zeros` 单边零点判据 | 若素数幂余项 $R_{q_0}(x)\le x^{\beta-1}$，则 $\Re\rho>\beta$ 处无零点 | `opening.tex:374` |

装配的关键是一条**精确恒等式**而非估计（`lem:distribution`，`opening.tex:142–148`）：

$$\mathcal R=a\Big\{|B|\big(R_{q_0}(x)-R_{q_0}(x_1)\big)+|A|R_1(x_1)\Big\}.$$

它把纯代数的量 $\mathcal R$（由素数幂权重的分段线性函数定义）与解析的余项 $R_q$ 精确对应，不含误差。随后：

1. 取短族，令 $h=H-m\mathcal R+\mathcal B_{\mathrm{cov}}$，代入 `prop:long`；
2. 用 $n\le D$ 与 $\lvert H\rvert+m\lvert\mathcal R\rvert\le b^2x^{99}$ 补足缺失维度（`opening.tex:400–407`）；
3. 主项 $H$ 在两边抵消，得 $m\mathcal R\le4\mathcal B_{\mathrm{cov}}+4x^{99}+10\log(1+b^2)\mathcal B\le fa(\log b)^5$（`eq:star-reduction`，`opening.tex:415–418`）；
4. 回代恒等式并用固定模数 PNT 控制第二尺度，得 $R_{q_0}(x)\le\varphi(q_0)x^{-1/2+6\varepsilon}$（`opening.tex:479–485`）；
5. `prop:zeros` 用二次扭分离对数导数的极点，Landau 引理排除右侧零点（`opening.tex:650–694`）；
6. 函数方程把结论从半平面推到临界带（`opening.tex:515–532`）。

**结构要点**：第 3 步是整个证明的枢纽——**主项 $H$ 完全不进入最终不等式**，只有余项 $\mathcal R$ 留下，并被 $1/m$ 压制。

### 6.2 上界侧：近张成族与整除性【文献确立】

上界不来自解析估计，而来自**整性（integrality）**：

- 短族是近张成的：$n\ge(1-4/b^2)D$（`spanning.tex:403–478` 用稳定迹比较证明维数相等，$D$ 是目标空间维数）。
- 每个提升值落在局部 Weyl 格中，平方 Weyl 范数 $\le\exp(\mathcal B)$（`lem:small-columns`，`short-comparison.tex:25–86`）。证明用 Banaszczyk 传递不等式控制格的极小值，再取 $k$ 个格向量作 $E$-基。
- 类和在权 $1/a_c$ 下范数平方 $\le e^{x^{99}}M'$（`short-comparison.tex:123–159`）。
- 局部损失按素数累加后总和 $\le\mathcal B$（`lem:sum-local-loss`，`short-comparison.tex:195`）。

**为什么这给出 $m\mathcal R$**：链上每一步提升都把"算术内容"乘一次；短族的行列式因此带 $m$ 次余项累积，指数中出现 $-m\mathcal R$。这是"重数 $m$"进入不等式的唯一入口——它是**整除性沿链累积**的结果，不是解析输入。

### 6.3 下界侧：高度与乘积公式【文献确立】

下界是全文技术核心，形式是一个**局部-整体高度**（`volumes.tex:14–44`）：

$$\operatorname{ht}(F)\le C\iff\exists\,z\in\C^\times,\ A\in\R,\ E_\ell\in\R:\quad |\sigma z|\le e^A,\quad |\iota(zF_\iota)|_\ell\le e^{E_\ell},\quad A+\sum_{\ell<X}E_\ell\le C .$$

即：**阿基米德主项 $A$ 与全部有限位分母 $E_\ell$ 之和被同一个常数控制**。这正是乘积公式的"总次数为零"在带误差情形下的形态。三步：

1. **单提升**：$\operatorname{ht}\big(\lambda_j(1)/\lambda_j(\vartheta_\iota)\big)\le Dk(B_0\log b-\mathfrak U)$（`eq:single-volume-height`，`volumes.tex:177–180`），其中 $\lambda_j(\vartheta)=\det(u_{\vartheta^j,j}^*u_{\vartheta^j,j})$ 是平方体积（`volumes.tex:57–58`）。
2. **链的体积因子**（`eq:chain-volume-factor`，`volumes.tex:441–446`）：

$$\mathfrak z(\vartheta)=|c(\vartheta)|^D\prod_{j=1}^m\lambda_j(\vartheta),\qquad \operatorname{ht}\big(|c(\vartheta_\iota)/c(1)|^{-2}\big)\le2m^2t\,x^{999}.$$

3. **链的逆高度**（`eq:chain-inverse-height`，`volumes.tex:647–651`）：

$$\operatorname{ht}\!\left(\frac{\mathfrak z(1)^2}{\mathfrak z(\vartheta_\iota)^2}\right)\le2D(2\mathcal B_{\mathrm{cov}}-H).$$

**结构要点**：第 3 式把"体积比的高度"上界写成 $2D(2\mathcal B_{\mathrm{cov}}-H)$——**主项 $H$ 以负号出现在高度上界里**。这与上界的 $-m\mathcal R$ 正好配成一对，使 $H$ 在相减时消去。有限位侧由 Selmer 长度估计（`eq:fit-strict-selmer`，`fit-twists.tex:284–287`）与 Hecke 值界（`prop:fit-twists`，`fit-twists.tex:239–259`）控制，最终压缩为原格上 Gram 行列式的分母界（`prop:original-level-denominator`，`denominators.tex:28–43`；`cor:original-level-gram`，`denominators.tex:377–392`）：

$$\big|\iota\det(h\operatorname{pr}_ZBB^*|_Z)\big|_\ell\le\exp(d_ZrB_\ell\log\ell).$$

### 6.4 主项抵消与两个竞争误差项【文献确立】

把 §6.2 与 §6.3 并置：

$$\underbrace{D(H-3\mathcal B_{\mathrm{cov}})}_{\text{下界}}\ \le\ \underbrace{V_{\mathrm{up}}}_{\text{上界}}\ \approx\ D(H-m\mathcal R+\mathcal B_{\mathrm{cov}}),$$

故 $m\mathcal R\le4\mathcal B_{\mathrm{cov}}$。

$H$ 消去，剩下的是**纯算术偏差 $\mathcal R$ 被链长 $m$ 压制**。两个竞争误差项是：

| 项 | 标度 | 来源 |
|:---|:---|:---|
| $m$ | $\sqrt x\le m\le2\sqrt x$（`eq:scales`，`opening.tex:96–99`） | 链长；越大越压制 $\mathcal R$，但链的标量误差按 $m^2t\,x^{999}$ 增长 |
| $x/m$ | 第二尺度 $x_1$，$\log x_1=x^{\varepsilon/6}$ | 需要 PNT 控制的 $R_{q_0}(x_1)$ 与 $R_1(x_1)$ |

取 $m\asymp\sqrt x$ 即 $m\asymp x/m$，是两误差的平衡点，最终给出 $R_{q_0}(x)\le\varphi(q_0)x^{-1/2+6\varepsilon}$——恰好是"半"的指数。

### 6.5 可迁移与不可迁移的分界【文献确立 + 判定】

论文 29 个文件可分为两层，**这一分界决定 CQM 能取走什么**：

| 层 | 文件 | 性质 | 对 CQM |
|:---|:---|:---|:---|
| 结构引擎 | `seesaw`、`theta-products`、`volumes`、`comparison-*`、`spanning`、`short-comparison`、`denominators` | 自守形式转移、余体积比较、高度乘积公式、Gram 正性 | **可迁移**：与具体 $L$ 函数无关 |
| 算术输入 | `fit-twists`、`crystalline-defect`、`first-order-return`、`galois-rows`、`sieve`、`real-cell`、`finite-cell` | $\ell$-进 Galois 表示的行/列系统、晶体上同调缺陷界、局部周期估计 | **不可迁移**：绑定 GL(1)／Dirichlet 特征与 $\Q$ 上的具体算术 |

结论：论文给 CQM 的是**"稳定性如何被量化并沿链放大"的模板**，不是可直接套用的实例。CQM 的 $GL(5)$ 若要复制，须自建对应的算术输入层；而该层在 CQM 中**尚无对应物**，这本身是一个新登记的缺口候选（不编号，不并入既有缺口体系）。

### 6.6 对量纲论的三项结构性转移（候选，全部【待推】）

以下三项是本章的实质结论。它们把"突破"从口号落到可检验的命题上，但**没有一项已成立**。

**（一）"稳定性"获得可计算的正性量。**

CQM 现有口径是定性的：`量纲与群论.md:1030` 说自守形式是「属性稳定性的数学体现：建立起自守形式，属性才算真正分化、获得稳定的物理身份」。论文把"稳定"实现为两个可计算的正量：

- Gram 行列式正性：$C_\eta=h\operatorname{pr}_{Z_\eta}B_\eta B_\eta^*|_{Z_\eta}$，$c_\eta=\det C_\eta>0$（`volumes.tex:80–82`）；
- 平方余体积：$\mathfrak z(\vartheta)=\det(\Theta_\vartheta^*\Theta_\vartheta)>0$（`volumes.tex:57–58`）。

**转移提议**：把定义 3 的配对 $(G_{\max}(f),\rho)$ 附上一个"稳定度"量——提升族 Gram 行列式的正性与高度有界。状态【CQM 构造假设（待推）】。可证伪点：若某 $f$ 的 $G_{\max}(f)$ 上不存在非零提升族（Howe 对偶意义下 $\theta(\pi)=0$），则"稳定性"无法量化，该转移不成立。

**（二）"关系分化"获得"度"的量。**

CQM 的关系分化止于极大关系群 $G_{\max}(f)$，没有"分化到什么程度"的度量。论文的链长 $m$ 正是这个度量：$U(X_0)\to U(X_1)\to\cdots\to U(X_m)$，每步增秩 $t$，偏差被 $1/m$ 抑制。

**转移提议**：把 $m$ 登记为"关系链长度"，$1/m$ 登记为"算术偏差抑制率"。状态【CQM 构造假设（待推）】。可证伪点：若 $G_{\max}(f)$ 的秩不允许长链（链在有限步后提升为零），则"分化度"退化，该转移不成立。

**（三）主项抵消是无量纲化的严格模型。**

量纲论的核心动作是"无量纲 → 量纲"的具体化。论文的高度机制恰好给出其严格形态：所有位的对数绝对值之和（乘积公式）使主项 $H$ 在上下界中抵消，留下的 $\mathcal R$ 是纯偏差，而 $1/m$ 是其压制率。**"主项抵消后剩下的不变量"**正是量纲论所谓"具体化"的数学对应物。

**转移提议**：把"量纲＝主项抵消后的不变量"登记为【哲学诠释＋CQM 构造假设】。**约束**：不得与定义 3 的"先 $f$ 后群"冲突——不变量必须先由 $f$ 确定，再由 $G_{\max}(f)$ 实现；论文的主项 $H$ 是先于群给定的标量，不可反过来充当 $f$。

| 论文机制 | CQM 概念 | 状态 | 可证伪检验 |
|:---|:---|:---|:---|
| $\det C_\eta>0$、$\mathfrak z(\vartheta)>0$ | 自守形式＝稳定性（`量纲与群论.md:1030`） | 【待推】 | 存在 $f$ 使 $G_{\max}(f)$ 上无非零提升 |
| 链长 $m$、抑制率 $1/m$ | 关系分化的"度"（定义 3 之外） | 【待推】 | 链在有限步后为零 |
| 主项 $H$ 抵消、留 $\mathcal R$ | 无量纲化的具体化 | 【哲学诠释＋待推】 | 与"先 $f$ 后群"冲突即不成立 |
| 高度 $A+\sum_\ell E_\ell\le C$ | 局部-整体配对分解 | 【待推】 | 有限位分母不受 Selmer 型界控制 |

### 6.7 两种"稳定性"不可等同（边界声明）

必须写明一处**同名异义**，否则会越过红线：

| | 论文的稳定性 | CQM 的稳定性 |
|:---|:---|:---|
| 对象 | 提升族 Gram 行列式正定、余体积非零 | 退相干稳态（动力学不动点） |
| 判据 | $\det G>0$（代数正性） | 稳态唯一、$A_4$ 涌现（缺口 C 未闭合） |
| 依赖 | 无动力学 | Lindblad 演化、非交换粗粒化极限 |

二者只在"自守形式＝稳定实现"这一层对齐（`量纲与群论.md:987,1030`），**不能**把论文的代数正性当作缺口 C 的解答，也不能把缺口 C 的动力学稳定性当作论文已证内容。缺口 C 状态不变（`README.md:205`）。

### 6.8 增补的可证伪检验（承接 §5.4 编号）

7. 对给定 $f$，构造 $G_{\max}(f)$ 上的提升族，计算 $\det C_\eta$ 与 $\mathfrak z(\vartheta)$；若恒为零则（一）不成立。
8. 确定 $G_{\max}(f)$ 所允许的最长非零提升链，给出实际抑制率；若 $m$ 有上界 $m_0$ 而 $m_0^{-1}$ 不足以压制偏差，则（二）不成立。
9. 检验"主项抵消"是否与定义 3 的"先 $f$ 后群"相容；不相容则（三）降为纯诠释，不得写入 `01`。
10. 明确 CQM 的 $GL(5)$ 算术输入层缺失：论文的 `fit-twists`／`crystalline-defect`／`galois-rows` 在 CQM 中无对应物，须先建立或声明该路径不通。
11. 任何落地仍须先改 `01` 权威源，再按 AGENTS.md §四.5 重跑全链并通过三道核查。

---

## 附：核对记录

- 外部链接：arXiv:2303.14919；`https://github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis`；`https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/`；`https://mrubinst.github.io/grh-lean-verification/`；`https://mrubinst.github.io/grh-lean-compact-check/`；`https://math.mit.edu/~drew/shortgrh/`。
- Lean 转写基准：`lsernau/grh-lean` 的 `grh-compact`，固定提交 `72fead102f663d5c7a407964a13dc0cf9d977207`。
- 本次写入仅新增本文件与三份外部 PDF；未改动 `01–07`、未改动 `08` 派生文件、未升级任何缺口。
- 第 6 章依据完整源码：`codeload.github.com/yuiyuiui/Natural-Language-Proof-Generalized-Riemann-Hypothesis/zip/refs/heads/main`（`sections/` 共 22,891 行、29 个 `.tex`，与 322 页 PDF 同源）。引用的行号均为该源码内行号。
