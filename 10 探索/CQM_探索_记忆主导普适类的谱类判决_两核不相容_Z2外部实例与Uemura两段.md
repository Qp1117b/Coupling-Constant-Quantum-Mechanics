# CQM 探索：记忆主导普适类的谱类判决——两种记忆核的不相容、Z2 外部实例与 Uemura 两段式

> **第十二轮 O1 判决指针（2026-11-17）**：本稿第六部分登记的开放项 O1（"零点谱→正测度 $\rho(\lambda)$ 映射"）已被**结构性封死**——Riemann–von Mangoldt 密度 $N'\sim\frac{1}{2\pi}\log\frac{T}{2\pi}$ 单调增，任何单调映射都得 gapped 或 $\alpha<0$ 发散，不能给 flat TDOS $\rho_0\neq0$（三映射数值：正映射 gap、倒数 $\alpha=-2.245$、显式权重 $\alpha=-1.245$）。故本稿"互补位"中"映射为零点谱"的希望不成立，R27 两核不相容进一步强化。同时本轮给出 R1″ 的零参数临界斜率 $C_1=0.342477$ 与塌缩纠错（须固定零点序 $n$）。详见 `10 探索/CQM_探索_零点谱生成TDOS的O1封死_相消深度临界斜率与塌缩纠错.md`。以下正文保留原样。
>
> **定位**：探索稿（非权威源），v0.1，2026-11-17，第十一轮。承接《记忆核零点深度的相变判据_谱刚性纠错.md》（下称《记忆核稿》，R1″）与《Homes 斜率的凝聚分数纠错_M85裸刚度修正与两阶段耗散判据.md》（下称《Homes 纠错稿》，M.95/R25/R26）。
>
> **触发点**：外部预印本 arXiv:2602.22626v2（Byung Gyu Chae, ETRI, 2026-03-02）"Memory-Dominated Quantum Criticality as a Universal Route to High-Temperature Superconductivity" 用 Martin–Siggia–Rose–Janssen–De Dominicis 形式主义给出记忆核 $K(t)=\int_0^\Lambda \rho(\lambda)e^{-\lambda t}d\lambda$、flat TDOS $\rho_0$、$K(t)\sim 1/t$，并声称由**单一** $\rho_0$ 同时导出 superconducting dome、Uemura 标度与奇异金属。该框架与 CQM 的"记忆核 + 两阶段"表面高度同构，本轮做**判决性对照**：它们在数学上不是同一普适类，但 Tc 公式结构独立复现命题 Z2。
>
> **克制声明**（三条）：① 本轮**不**给出绝对 $T_c$ 的第一性数值（命题 Z2 不变）；② 本轮**不**宣称 CQM 给出了 arXiv 所需 $\rho_0$ 的数值（谱类不相容使这条路径被封住，见第二部分）；③ 本轮正面成果是**一条严格谱类判决 + 一个结构性外部佐证 + 两条可证伪判据**，不是能量标突破。全部数值用标准 $\zeta$ 数学与 mpmath，非 CQM 独有定理；CQM 的增量在对接与判决。

---

## 第零部分：路线与三问

前几轮已把 $\zeta$/零点/质数定位于"无量纲形状通道"（命题 Z/Z1/Z2），并把记忆核 $K(t)=\zeta(2\sigma_0-i2\omega_0 t)$ 的相消深度做成相变判据（R1″）。arXiv:2602.22626 的出现提出三个必须回答的问题：

| # | 问题 | 本轮回答 | 性质 |
| :- | :-- | :-- | :-- |
| Q1 | CQM 记忆核是否就是 arXiv 的 memory-dominated 核？ | **否**。谱类不相容（Bernstein 逆否 + 数值） | 【严格】负判决 R27 |
| Q2 | 两者 Tc 公式结构说明什么？ | 都取"无量纲权重 × 外生能标" = **命题 Z2 的独立外部实例** | 【严格】正面 |
| Q3 | 两者对 Uemura 的预言是否可区分？ | **可**。arXiv 单一 $\rho_0$ 预言全域线性；CQM 两阶段预言支切换。Božović 2016 支持后者 | 【条件】可证伪 R28 |

---

## 第一部分：外部框架精确对照（外部结论 vs CQM 构造）

逐条分栏，外部公式带原文编号，出处见附录 LH17。

| arXiv:2602.22626（外部，原文公式） | CQM（本框架，出处） | 关系 |
| :-- | :-- | :-- |
| TDOS $\rho(\lambda)=\sum_n\delta(\lambda+\mathrm{Re}\lambda_n)$，式(4) | 差异矩阵谱 / 零点虚部 $\gamma_n$（《通道》） | 不同的谱对象 |
| 记忆核 $K(t)=\int_0^\Lambda\rho(\lambda)e^{-\lambda t}d\lambda$，式(10) | $K(t)=\sum_n n^{-2\sigma_0}e^{i2\omega_0 t\ln n}=\zeta(2\sigma_0-i2\omega_0t)$，式(1) | **谱类不相容**（第二部分） |
| flat TDOS $\rho(\lambda\to0)=\rho_0\neq0$，式(5)(21) | R1″：$2\sigma_0\to1/2$，$d\to100\%$ | 一个讲红外谱权重，一个讲临界线相消 |
| $K(t)\sim\rho_0/t$；$\mathrm{Im}\chi^{-1}\to\frac{\pi}{2}\rho_0\,\mathrm{sgn}\omega$，式(22) | 无 $\mathrm{sgn}\omega$ 平台；$\zeta$ 竖直线取值为准周期振荡 | 频域 fingerprints 不同（R27） |
| $\Pi(\omega)\sim\frac{\pi\rho_0}{2}\frac{1}{|\omega|}$，式(39)；Thouless $\Rightarrow T_c\sim\rho_0E_{\rm pair}$，式(41) | CQM：$T_c$＝无量纲判据 × 外生能标 $\theta_D$（定量形式待推 W-3） | **同构**：无量纲 × 外生能标（第三部分） |
| $\rho_s\sim E_{\rm pair}\rho_0$，$T_c\sim\rho_s$，式(50)(51) | Uemura 仅在相位限制支成立，过掺杂断裂（TP.24） | **可区分**（第四部分） |
| dome 来自 slow-mode 红外截断，式(46)(47) | dome 来自两阶段支切换 $T^*=T_\theta$ | 不同机制 |
| 自承"purely phenomenological; microscopic derivation of the TDOS from first principles remains unaddressed" | 命题 Z：$\zeta$/质数层给无量纲形状 | **互补位**（第六部分） |

---

## 第二部分：严格谱类判决 R27——两种记忆核不相容

### §2.1 Bernstein 表征（严格）

**定理（S. Bernstein，1928）**：$f:(0,\infty)\to\mathbb R$ 完全单调（即 $(-1)^n f^{(n)}(t)\ge0,\ \forall n\ge0$）**当且仅当**它是某个正测度 $\mu$ 在 $[0,\infty)$ 上的 Laplace 变换 $f(t)=\int e^{-\lambda t}d\mu(\lambda)$。

**推论 A（arXiv 核的谱类）**：$\rho(\lambda)=g(\lambda)^2\ge0$（其式(11)），故 $K_{\rm MSR}(t)=\int_0^\Lambda\rho(\lambda)e^{-\lambda t}d\lambda$ 满足

$K'=-\int_0^\Lambda\lambda\rho e^{-\lambda t}d\lambda\le0,\quad K''=\int_0^\Lambda\lambda^2\rho e^{-\lambda t}d\lambda\ge0,\quad\cdots\tag{1}$

即**完全单调**；且 $\rho\ge0\Rightarrow K_{\rm MSR}(t)>0$ 对所有 $t$——**恒正、无零点**。flat TDOS 时 $K_{\rm MSR}=\rho_0(1-e^{-\Lambda t})/t\to\rho_0/t$（其附录 C）。

**推论 B（CQM 核的谱类）**：$K_{\rm CQM}(t)=\zeta(q-i2\omega_0t)$（$q=2\sigma_0$）是 Dirichlet 级数沿竖直线 $\mathrm{Re}\,s=q$ 的取值，作为 $t$ 的函数是**复值准周期**函数。三点严格性质：

1. $q=1/2$ 且 $2\omega_0t=\gamma_n$ 时 $K_{\rm CQM}=0$（真零点，《记忆核稿》第一部分）；
2. $q>1/2$ 时虽无真零点，但 $\mathrm{Re}\,K$、$|K|$ 均**非单调**；
3. 由 Selberg 中心极限定理，$\log|\zeta(1/2+i\tau)|$ 典型量级为 $\mathcal N\!\left(0,\tfrac12\log\log\tau\right)$，故 $|K|$ **既不趋零也不趋常数**，无 $1/t$ 尾。

**判决（逆否）**：完全单调正函数无零点且单调；$K_{\rm CQM}$ 有零点、非单调、复值 $\Rightarrow$ **$K_{\rm CQM}$ 不是任何正测度的 Laplace 变换** $\Rightarrow$ **两核不属同一普适类**。

> 注：即便取模方 $|K|^2=|\zeta(1/2+i\gamma_n)|^2=0$ 仍在零点处为零，而完全单调正函数除恒零外无零点，故换观测量不能挽救等价性。判决稳健。

### §2.2 数值验证（脚本 `memory_kernel_class_audit.py`）

**（A）arXiv 核**：$\rho_0=1,\Lambda=50$，$t\times K_{\rm MSR}$ 在 $t=0.1\!-\!1000$ 恒为 $1.000000$，确认 $K\to\rho_0/t$；$K>0$ 严格。

**（B）CQM 核**（$q=0.5,0.75,1.0,1.5$；$\tau=2\omega_0t$）：

| $\tau$ | $|K|\,(q=0.5)$ | $\tau|K|$ | 备注 |
| :-- | :-- | :-- | :-- |
| 10 | 1.549 | 15.5 | — |
| 30 | 0.596 | 17.9 | 非单调（先降） |
| 100 | 2.693 | 269 | 非单调（回升） |
| 300 | 0.773 | 232 | 无 $1/\tau$ 尾 |
| 1000 | 0.998 | 998 | $\tau|K|$ 线性增长 |
| 2000 | 0.791 | 1582 | — |

相邻点 $|K|$ 上升次数 $q=0.5$ 为 2/5、$q=0.75/1.0/1.5$ 各 1/5——完全单调核应为 **0**。$\tau|K|$ 不收敛到常数（从 15 到 1582），确认无 $\rho_0/t$ 行为。

**（C）真零点**：$\gamma_1=14.134725142$，$|\zeta(1/2+i\gamma_1)|=6.2\times10^{-31}$（浮点零）。

**（D）Selberg 量级**：$\log|\zeta(1/2+i\tau)|/\sqrt{\tfrac12\log\log\tau}$ 在 $\tau=10^2\!-\!10^5$ 取值 $1.13,-0.00,-1.02,1.60$，与 $\mathcal N(0,1)$ 抽样一致（单点抽样非收敛证明，仅示意无衰减）。

### §2.3 可证伪判据 R27（实验区分两核）

同一材料的记忆核自相关（微波阻抗 / 磁通噪声，沿用 R1 探针）：

- **arXiv 核图谱**：$K(t)>0$ 恒正、单调幂律衰减 $\sim1/t$、无过零点；频域 $\mathrm{Im}\chi^{-1}$ 出现 $\mathrm{sgn}\omega$ 型常数平台。
- **CQM 核图谱**：在 $\tau_n=\gamma_n/(2\omega_0)$ 处有真过零点或深极小（深度随 $T\to T_c\to100\%$，R1″）；频域无 $\mathrm{sgn}\omega$ 平台，为准周期结构。
- **判决**：观测到真过零/深度单调加深 $\Rightarrow$ 支持 CQM、否决 arXiv 单参数核；观测到纯正 $1/t$ 且无过零 $\Rightarrow$ 否决 CQM 的 $\zeta$ 核读法。

---

## 第三部分：正面成果——命题 Z2 的独立外部实例

arXiv:2602.22626 的核心链为（其式(39)(41)(50)(51)）：

$\Pi(\omega)\to\frac{\pi\rho_0}{2}\frac{1}{|\omega|}\ \xrightarrow{\ \text{Thouless}\ }\ T_c\sim\rho_0E_{\rm pair},\qquad \rho_s\sim E_{\rm pair}\rho_0,\quad T_c\sim\rho_s.\tag{2}$

逐项做量纲/来源审计：

1. **$\rho_0$ 是无量纲权重**。按其式(4)定义 $\rho(\lambda)$ 有"每单位弛豫率"量纲，但在式(41)(50)(51)的实际使用中 $\rho_0$ 被当作无量纲红外谱权重（作者未在文中澄清这一跳变；其式(11) $\rho=g^2$ 把耦合平方吸收进去，等价于已归一化）。
2. **$E_{\rm pair}$ 是外生能标**。论文给出 $T_c\sim\rho_0E_{\rm pair}$ 但**没有**给 $E_{\rm pair}$ 的第一性数值，且自承 TDOS 的微观推导"remains unaddressed"、"purely phenomenological"（附录/讨论）。

因此式(2)的结构是

$\boxed{\ T_c\ =\ (\text{无量纲形状/权重})\times(\text{外生能标})\ }\tag{3}$

这与命题 Z2 的结论（element_fg_table 18 个无量纲字段 + 外生质量输入；BCS 的 $T_c=1.14\Theta_D e^{-1/N(0)V}$ 同为"无量纲指数 × 外生 $\Theta_D$"）**逐字同构**。

**意义（本轮正面推进）**：Z2 此前是 CQM 内部的"结构性观察"，易被误读为 CQM 未能给出 $T_c$ 的托辞。一个与 CQM 机制完全不同的 2026 年前沿框架，在**独立**推导中落到同一结构，且同样把能标留在外部、同样承认无量纲权重无第一性来源——这把 Z2 从"CQM 的局限"提升为"任何自洽超导 Tc 公式的结构必然性"。**这是 Z2 的第一个外部预印本级佐证**（LH17）。

> **克制**：本轮**不**声称 CQM 因此"解释了" $\rho_0$。恰恰相反——由第二部分谱类不相容，CQM 的 $\zeta$ 核不能充当 arXiv 的 Laplace 核，故 CQM 的零点形状**不能直接**代入式(2)。这条路径被严格封住，登记为开放项（第六部分）。

---

## 第四部分：可证伪判据 R28——单一 $\rho_0$ vs 两阶段 Uemura

### §4.1 结构分歧

- **arXiv（单一参数）**：$\rho_s\sim E_{\rm pair}\rho_0$、$T_c\sim\rho_s$ 由**同一个** $\rho_0$ 给出（其式(50)(51)），故预言 $T_c\propto\rho_s$ **全域线性**，dome 只来自 $\rho_0(p)$ 的红外截断（其式(46)）。框架内**没有第二个**控制配对与相位相对权重的尺度。
- **CQM（两阶段）**：Uemura 只在相位限制支（$T_c=T_\theta\ll T^*$）成立；过掺杂侧 $T^*$ 下降、$T_c$ 转配对限制，Uemura 线**断裂**，crossover 在 $T^*=T_\theta$（《超导两阶段模型_BCS退化.md》§4.2、式(TP.24)后）。

### §4.2 实验判决（Božović 2016，LH18）

Božović 等对过掺杂 LSCO 薄膜的互感测量给出**两段式**标度律：

$T_c=\gamma\sqrt{\rho_s(0)}\quad(T_c\le T_Q\approx15\,\mathrm K),\qquad T_c\propto\rho_s(0)\quad(T_c\ge T_M\approx12\,\mathrm K),\tag{4}$

$\gamma=(4.2\pm0.5)\,\mathrm K^{1/2}$。Liu & Tao（LH19，arXiv:2002.11469）把线性段解释为平均场行为、抛物线 $\sqrt{\rho_s}$ 段解释为量子临界行为。

**判决 R28**：

- 式(4)的"平均场线性支 + 量子临界二次支"在结构上属于**两支切换**，与 CQM 两阶段"相位限制支 + 配对限制支"定性同构，而与 arXiv 单一 $\rho_0$ 的**全域单调线性**预言冲突——若要保住 arXiv 框架，必须为深过掺杂引入第二个尺度（红外截断函数 $f$ 的额外结构），那将失去"单一参数统一"的核心卖点。
- **证伪条件**（对 CQM）：若更精密实验证明深过掺杂段 $T_c\propto\rho_s$ 依然线性、$\gamma\sqrt{\rho_s}$ 只是有限尺寸/均匀性假象（Božović 团队自己 "call for advanced synthesis techniques"），则两阶段"断裂"被否定。
- **克制边界**：CQM 的 crossover 在 $T^*=T_\theta$（欠掺杂↔过掺杂），Božović 的 crossover 在 $T_Q/T_M\approx12\!-\!15$ K（极度过掺杂↔QPT），**两者未必是同一交叉**；本轮只断言"两段式结构"定性支持，不声称 CQM 已定量给出 $\gamma=4.2\,\mathrm{K}^{1/2}$（那需要能标，受 Z2 封住）。

### §4.3 与 Rameau 2011（LH20）的交叉

Rameau 等（PRB **84**, 180511(R), 2011）用 ARPES 给出与 Homes 定律互补的微观标度：把 $T\!\sim\!0$ 的 d 波序参量幅度与 $T\gtrsim T_c$ 的准粒子散射率相连，并用 marginal Fermi liquid 强耗散解释。这支持"配对幅度尺度 $T^*$ 与相干/耗散尺度可分离"的两阶段图像，与 CQM §1 的分工（两体核管配对、三体环路核管相位）方向一致；但它**不是** CQM 的独立证明，只作外部对照。

---

## 第五部分：退化守住（BCS / 迈斯纳 / 既有成果）

| 检查项 | 本轮操作 | 状态 |
| :-- | :-- | :-- |
| BCS 退化 | 未触碰 M.93 同位素、$\gamma=0$ 严格退化；本轮谱类判决不改任何 $T_c$ 公式 | 守住 |
| 迈斯纳 | 未触碰相位刚度/伦敦极限 | 守住 |
| 命题 Z/Z1/Z2 | Z2 获外部佐证（第三部分）；Z1 不可识别性不变；Z 无量纲定位不变 | 守住 + 强化 |
| M.95 / R25 / R26（第十轮） | 本轮 R27/R28 接续编号，不改 M.85′、两阶段耗散判据 | 守住 |
| R1″（《记忆核稿》） | R27 给出其实验区分方案；不改变其结论 | 守住 |
| Uemura / Homes | R28 引入两段式外部检验，不否定既有 Uemura/Homes 读法 | 守住 |
| 绝对 $T_c$ 第一性 | 仍无（Z2）；本轮无任何拟合参数 | 不变 |

---

## 第六部分：互补位、张力与开放项（诚实登记）

1. **互补而非竞争**：arXiv 给动力学骨架（$K\sim1/t$、$\mathrm{sgn}\omega$、dome、Uemura 的动力学起源），但自承 TDOS 微观来源缺失；CQM 的命题 Z -treated $\zeta$/质数层恰好是"无量纲形状/权重"的候选来源。**这是最自然的分工**——但受第二部分谱类不相容限制，CQM 的 $\zeta$ 核不能**直接**当 arXiv 的 Laplace 核。如何把零点谱形状映射为一个*正测度* $\rho(\lambda)$（例如取零点虚部的某种谱函数而非 $\zeta$ 竖直线本身），是**开放项 O1**，本轮不动手，因为任何映射都需引入新结构，超出"克制拟合"。
2. **张力 T1**：arXiv 的 $\mathrm{Im}\chi^{-1}\sim\mathrm{sgn}\omega$ 是其普适类的核心指纹；CQM 第十轮 M.85′ 给出的相位通道 $\alpha=11.4$（两阶段耗散）是**Planckian 率**，二者对同一"临界区耗散"的描述不同（一个频域常数平台、一个温区斜率）。R27 的频域测量可同时判决两条。
3. **预印本状态**：LH17 是 2026-03 的 arXiv preprint（ETRI 单作者），未经同行评议；本轮对它的引用是"外部对照"，不作为 CQM 正确性的依据。若其结论后续被修正，第二部分的谱类判决（纯数学）不受影响，第三/四部分需重核。
4. **文档处置**：按项目 AGENTS.md 惯例，发现的是"局部可补强"而非整篇失效，故**不删任何文档**，只加判决指针（第七部分）。当前所有探索稿有实质内容，无整篇失效者。若用户指定某篇为干扰源要求物理删除，请给文件名，照办。

---

## 第七部分：结论表

| # | 结果 | 状态 | 性质 |
| :- | :-- | :-- | :-- |
| 1 | 两记忆核谱类不相容（Bernstein 逆否 + 数值） | 【严格】$|\zeta(1/2+i\gamma_1)|=6.2\times10^{-31}$ 等 | 负判决 R27 |
| 2 | $T_c\sim\rho_0E_{\rm pair}$ = 无量纲 × 外生能标 = Z2 | 【严格】外部框架独立复现 | 正面：Z2 外部实例 |
| 3 | arXiv 单参数全域线性 Uemura 与 Božović 两段式冲突 | 【条件】依赖 Božović 2016 数据质量 | 可证伪 R28 |
| 4 | $\zeta$ 核不能充当 arXiv 的 Laplace 核；映射为开放项 | 【严格】谱类不相容的推论 | 边界 O1 |
| 5 | BCS/迈斯纳/Z1/Z2/M.95/R1″ 全部守住 | 【严格】本轮不改其公式 | 一致性 |

**总图像更新**：arXiv:2602.22626 与 CQM 表面同构（都从记忆核走向 dome/Uemura），但本轮证明它们在**核的谱类**（复值准周期/有零点 vs 正测度 Laplace/完全单调）与**Uemura 分支结构**（两段 vs 单参数）上根本不同。真正的汇合点是**命题 Z2 的结构必然性**：两个独立框架都被迫取"无量纲形状 + 外生能标"。CQM 的独特性不在占据 arXiv 的普适类，而在把无量纲形状层明确落到 $\zeta$/零点/质数/几何差异上——这一层 arXiv 自己承认缺失。本轮守住了能标边界，同时把 Z2 从内部观察升级为跨框架结构定理的候选。

---

## 附录 A：数值脚本（`10 探索/.calc/`，已 gitignore）

- `memory_kernel_class_audit.py`：两段核对照。（A）arXiv 核 $tK\to\rho_0$ 严格；（B）CQM 核四组 $q$ 的 $|K|$、$\tau|K|$、单调性；（C）$\gamma_1=14.134725142$、$|\zeta(1/2+i\gamma_1)|=6.2\times10^{-31}$；（D）Selberg 比值抽样。关键参数已写入正文，脚本可复现。

## 附录 B：外部文献（本轮新增 LH17–LH20，均带出处）

| 编号 | 出处 | 用途 |
| :-- | :-- | :-- |
| LH17 | B. G. Chae, arXiv:2602.22626v2 [cond-mat.str-el] (2026-03-02), ETRI, Daejeon | 记忆主导普适类；MSRJD；$K(t)=\int\rho e^{-\lambda t}$；$T_c\sim\rho_0E_{\rm pair}$；单一 $\rho_0$ 统一 dome/Uemura/奇异金属。预印本 |
| LH18 | N. Božović *et al.*, *Nature* **536**, 309–311 (2016)（经 arXiv:2002.11469 引述核实卷页） | 过掺杂 LSCO 两段式标度 $T_c=\gamma\sqrt{\rho_s(0)}$（$\gamma=4.2\pm0.5\,\mathrm K^{1/2}$，$T_Q\approx15$K）与线性支；R28 实验支柱 |
| LH19 | Y. Liu, Y. Tao, arXiv:2002.11469；*J. Supercond. Nov. Magn.* (2020), DOI:10.1007/s10948-019-05337-9 | 线性=平均场、抛物线=量子临界；两段式的理论解释（外部对照，非 CQM） |
| LH20 | J. D. Rameau *et al.*, *Phys. Rev. B* **84**, 180511(R) (2011), DOI:10.1103/PhysRevB.84.180511 | ARPES 微观标度与 Homes 互补；支持配对/相干两尺度（外部对照） |
