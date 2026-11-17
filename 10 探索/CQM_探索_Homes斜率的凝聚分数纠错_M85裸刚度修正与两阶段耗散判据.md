# CQM 探索：Homes 斜率的凝聚分数纠错——M.85 裸刚度修正与两阶段耗散判据

> **⚠ 证伪指针（2026-11-17，最先读）**：本稿 §4 的 **M.85′（$\alpha=11.415$，$\eta_{\rm pred}=118.96$，$-0.9\%$ 零参数闭合）撤销**。M.95 的系数是 $f_s$（超流/Drude），不是 $f_c=1/4$（超流/总谱重）。用 Broun 表 1 的 $f_s\approx0.89$ 回代：若坚持 $\alpha=11.415$，$\eta=423$，被 $\eta=109$–$120$ 排除 $3.5$–$3.9$ 倍；若取 $\eta=120$，$\alpha=3.24$，不是 $11.4$。原 M.85（$\alpha=2.854$）存活：$\eta_{\rm pred}=41.673f_s\alpha=106$–$113$（$f_s=0.89$–$0.95$），在 $-12\%$ 内。故"$1/4$ 进 Homes 斜率"的读法 T 不成立；M.83 的 $1/4$ 只进静态归一化（按审计 §2.4–§2.5，现有数据判读法 B：$1/4=f_D$；读法 A 须 $\Lambda\propto f_s$ 同步塌缩约 $14$–$30$ 倍才存活），不进 Homes 的 $f_s\alpha$。本稿 §2 的 100 倍换算纠错、M.95、R25/R26 的两阶段结构不变；R17 阈值应回到 $2.85$–$3.2$，不是 $11.4$。完整审计见 `10 探索/CQM_探索_1over4归一化审计_凝聚分数与Drude分数二读_M85prime证伪与判决实验.md`。
>
> **定位**：探索稿（非权威源）。承接 `10 探索/CQM_探索_凝聚分数_普朗克耗散_Homes定律.md`（下称《Homes 稿》，M.83–M.86），本轮对其中 **M.84 的数值链**做硬纠错，并给出修正后的几何身份。
>
> **范式**：全部在"网格—和乐—刚度—凝聚分数"语言内推进。本轮不改核心文档任何定义、数值与缺口状态；只在探索层修正一篇探索稿的内部计算。
>
> **克制拟合声明**：本轮无被优化参数。全部输入只有三项：Homes 斜率实验值 $\eta$（外部实验）、$n_s/n=1/4$（M.83，框架内代数 + XY 数值检验）、$k_BT_c/J_{\rm eff}=2.2017$（外部普适类常数）。$8\pi=2\pi/(1/4)$ 是代数组合，不是拟合。

---

## 第零部分：本轮判决清单（先看结论）

| # | 判决 | 性质 | 后果 |
|:--|:--|:--|:--|
| 1 | 《Homes 稿》M.84 的换算因子内部差 **100 倍**：正文/附录表写 $8.988\times10^{11}$，但要得到文中 $\alpha=2.622$ 必须用 $8.988\times10^{9}$ | 【硬纠错：算术】 | "$\alpha=2.62$ 与 Shekhter $2.6$ 差 $0.8\%$"是**假相容**，必须撤销 |
| 2 | Shekhter 2025（arXiv:2504.02179）的 $\alpha\approx2.6$ 是在 **$n_s=n$**（凝聚分数取 1）下由 Homes 斜率反推的；她明确写"超流密度与电导率都正比于同一个 $n/m^*$" | 【外部文献，原文直引】 | 该 $\alpha$ 不能与 M.83 的 $n_s/n=1/4$ 同时代入同一条 Homes 公式 |
| 3 | 第一性（SI）$C=\eta=41.673\,(n_s/n)\,\alpha$，与 Shekhter 印刷的 "$\approx42\alpha$" 在 $n_s/n=1$ 处一致到 $0.8\%$ | 【严格：量纲+Drude+London】 | Homes 斜率**只约束乘积** $(n_s/n)\alpha$，不能单独定 $\alpha$ |
| 4 | 若坚持 M.83 的 $1/4$，则 $\eta=120$ 要求 $\alpha_{\rm Homes}=11.52$，而非 $2.62$ | 【条件严格】 | 与 Planckian $\alpha\!\approx\!1$（Legros 2019）差 11.5 倍，超出 Shekhter "因子 3" 容忍度——真实张力，不掩盖 |
| 5 | **M.85′（修正）**：$\hbar/\tau=2\pi J_0=8\pi J_{\rm eff}$（**裸刚度** $J_0$，非凝聚后 $J_{\rm eff}$）$\Rightarrow\alpha=8\pi/2.2017=11.415$，回代 $\eta_{\rm pred}=118.96$ vs $120$（$-0.9\%$） | 【候选：零参数，单点识别升级】 | M.83、M.85、Homes 三者首次自洽闭合；Shekhter 的 $2.6$ 被识别为 $J_{\rm eff}$ 版本的"表观系数" |
| 6 | 两阶段解释：$T\to0,\ p^*$ 处 $\alpha\approx1$（配对通道）；$T\to T_c$ 处 $\alpha\approx11.4$（相位通道，$2\pi J_0$）。可证伪预言 R25 | 【候选，可证伪】 | 与核心文档 DM.13 两阶段结构一致，给出"Shekhter 因子 3 偏离"的定量替代 |

---

## 第一部分：外部文献基准（LH10–LH16）

> 编号 LH10 起，独立于《Homes 稿》LH1–LH9 与《通道》LX 系列，互不混用。外部结论只作对照/标定，不替代 CQM 推导。

| 编号 | 出处 | 外部结论（原文要点） | 本轮用法 |
|:--|:--|:--|:--|
| LH10 | Shekhter, Chan, McDonald, Harrison, *Homes' Law and Universal Planckian Relaxation*, arXiv:2504.02179v2 (2025-06) | $\rho_{s0}=c^2\omega_{ps}^2=(1/2\pi\lambda_L)^2$，$\lambda_L^{-2}=4\pi e^2(n/m^*)/c^2$；$\sigma=e^2(n/m^*)\tau$；$\hbar/\tau=\alpha k_BT$；$C=\alpha(k_B/\hbar)/\pi c^2\approx\alpha\times42\ \Omega^{-1}{\rm cm}^{-1}{\rm K}^{-1}$；"**both** $\rho_s$ **and** $\sigma$ are proportional to the ratio $n/m^*$"；$\alpha\approx2.6$；Homes 只在对数精度成立，$T_c$ 附近电阻偏离 $T$-linear 约"不超过因子 3" | §2–§4 的主对照；**"同一个 $n/m^*$"是本轮判决关键** |
| LH11 | Zaanen, *Nature* **430**, 512 (2004), DOI:10.1038/430512a | 由 Homes+Drude+Tanner 反推 $\tau\sim\hbar/(2\pi k_BT)$，首提普朗克耗散 | 历史源头；本轮指出 Tanner 因子在后续文献中被丢弃 |
| LH12 | arXiv:1206.5305（全息实现 Homes 定律） | 明确用 $\rho_s\propto n_s$，$\sigma_{\rm DC}=n_n e^2\tau/m^*$，$\tau\simeq\hbar/k_BT_c$，**并显式引入 Tanner 定律 $n_s\approx n_n/4$**："To connect ... we employ Tanner's law" | §4：证明"Tanner+Planckian⇒Homes"是文献标准路线，但该文只证比例关系、未核对斜率数值 |
| LH13 | JHEP **10** (2016) 041 | "$\rho_s\sim n_S,\ \sigma_{\rm DC}\sim n_N\tau,\ \tau\approx\hbar/k_BT_c$ ... **if we use Tanner's law $n_S=n_N/4$, Homes' law is obtained**" | 同 LH12；独立复述 Tanner 因子不可省 |
| LH14 | Legros *et al.*, *Nat. Phys.* **15**, 142 (2019), DOI:10.1038/s41567-018-0334-2 | $1/\tau=\alpha h/(2\pi k_BT)=\alpha k_BT/\hbar$，$\alpha\approx1$（四种空穴掺杂 + 两种电子掺杂 + 有机导体，在 $p^*$ 的 $T\to0$ 极限） | §6：$\alpha\!\approx\!1$ 与 $\alpha_{\rm Homes}\!\approx\!11.4$ 属于**不同温区**，两阶段模型可容纳 |
| LH15 | Hooley/等综述性证据矩阵 qft.org "Evidence for Planckian Dissipation"（证据截止 2026-08，非同行评议，仅作方法论提醒） | "the dimensionless coefficient depends on **which lifetime is extracted**, on the transport model, and on material parameters"；Poniatowski 2021 是"对某输运界表述的反例，而非对所有普朗克时间的反例" | §6：支持"两个 $\alpha$ 不必相等"的审慎读法，**不作为物理依据** |
| LH16 | Fe(Te,Se) 闪烁超导 + Planckian, arXiv:2509.13969 (2025) | 涨落时间尺度在 $T_c$ 处转折并接近 $\tau_q=\hbar/(\alpha k_BT)$，实测 $\alpha=1.38\pm0.05$；样品遵守 Homes 而**不**遵守 Uemura | §6：又一个"$\alpha\!\sim\!1$ 与 Homes 共存"的实测点，作为张力背景 |

**未取到的外部依据**：把 $\alpha$ 写成 $8\pi/(k_BT_c/J_{\rm eff})=2\pi/(n_s/n)/(k_BT_c/J_{\rm eff})$ 并归因为"正常态散射用裸刚度"——这是 CQM 构造，无外部出处，已标为【候选】。

---

## 第二部分：硬纠错——《Homes 稿》M.84 换算因子差 100 倍

### §2.1 算术事实

《Homes 稿》§3.1 给出 M.84：

$$\alpha=\frac{\hbar\,\eta}{4\pi\,(n_s/n)\,k_B}\quad\Longleftrightarrow\quad \eta=\frac{4\pi}{\hbar}\cdot\frac{n_s}{n}\cdot\alpha\,k_B.\tag{M.84}$$

该式中的 $\eta$ 必须是 **SI 单位**（${\rm s}^{-1}{\rm K}^{-1}$）。《Homes 稿》§3.2 表格与附录 A.7 均声明换算

$$1\ \Omega^{-1}{\rm cm}^{-1}=8.988\times10^{11}\ {\rm s}^{-1}.\tag{conv-A}$$

把 conv-A 代入 M.84，取 $\eta=120$、$n_s/n=1/4$：

$$\alpha=\frac{(1.0546\times10^{-34})(120)(8.988\times10^{11})}{4\pi(1/4)(1.3806\times10^{-23})}=262.2.$$

**不是文中写的 $2.622$。** 要得到 $2.622$，换算因子必须取 $8.988\times10^{9}$（附录 A.3 的反演系数 $2.185\times10^{-2}$ 隐含此值）：

$$\frac{8.988\times10^{11}}{8.988\times10^{9}}=100.01.$$

即：**同一篇文档的两处换算相差 100 倍**。§3.2 正文用 conv-A（$10^{11}$），附录 A.3 的"$\alpha=2.185\times10^{-2}\eta$"用 $10^{9}$。

### §2.2 后果

《Homes 稿》§3.2 的结论"三数闭合到 $0.8\%$"、附录 A.2 的 $\eta_{\rm pred}=130.7$、第六部分清洁数据表第 3/4 行的"带内 $0.4\sigma$"、以及 §4.2 围绕 $\alpha=2.62$ 的全部 $\pm9\%$ 讨论——**全部建立在错误的换算上，予以撤销**。

> **处置**：按项目惯例（撤销标注而非物理删除），在《Homes 稿》顶部加一条纠错指针（见本轮末），原文一字不动。本轮不把《Homes 稿》从库中删除——它仍是 M.83/M.86/R16/R17 的唯一出处，删之会丢失未受影响成果。

---

## 第三部分：第一性 Homes 斜率——只约束乘积 $(n_s/n)\alpha$

### §3.1 SI 推导（干净链）

伦敦穿透深度（SI）：$\lambda_L^{-2}=\mu_0 n_s e^2/m^*$。约定 $\rho_s\equiv(1/2\pi\lambda_L)^2$，以 ${\rm cm}^{-2}$ 计：

$$\rho_s^{[\rm cm^{-2}]}=\frac{\mu_0 n_s e^2/m^*}{4\pi^2}\times10^{-4}.$$

Drude 电导率（SI）：$\sigma^{[\rm S/m]}=n e^2\tau/m^*$，以 $\Omega^{-1}{\rm cm}^{-1}$ 计需 $/100$。代入 $\tau=\hbar/(\alpha k_BT_c)$：

$$\boxed{\eta\equiv\frac{\rho_s}{T_c\sigma}=41.673\,\frac{n_s}{n}\,\alpha\quad[\Omega^{-1}{\rm cm}^{-1}{\rm K}^{-1}]}\tag{M.95}$$

【严格：量纲 + Drude + London + Planckian 定义】

**核对**：令 $n_s/n=1$，得 $41.673\alpha$，与 LH10 印刷的"$\approx42\alpha$"一致到 $0.8\%$——这条 42 的外部常数被本轮从第一性重建，且**不需要** Shekhter 印刷公式 $C=\alpha(k_B/\hbar)/\pi c^2$ 中互有歧义的 $c^2$ 与 $8.988\times10^{12}$ 写法（按字面代入该式得 $416.8$，与其自报 $42$ 差 10 倍，属其排版笔误，不影响其 $42\alpha$ 数值结论）。

### §3.2 判决：Homes 斜率不可分离 $n_s/n$ 与 $\alpha$

由 (M.95)，实验斜率 $\eta=120$ 只给

$$\frac{n_s}{n}\,\alpha=\frac{120}{41.673}=2.880.$$

两条读法给同一个乘积：

| 读法 | $n_s/n$ | $\alpha$ | 乘积 | 出处 |
|:--|:--|:--|:--|:--|
| S（Shekhter） | $1$ | $2.88$（其 $2.6$ 同量级） | $2.88$ | LH10 原文用同一个 $n/m^*$ |
| T（Tanner/M.83） | $1/4$ | $11.52$ | $2.88$ | LH12/LH13 显式用 $n_s=n_n/4$ |

**M.84 的深层错误**：它取了读法 T 的 $n_s/n=1/4$，却去匹配读法 S 的 $\alpha=2.6$（那是在 $n_s=n$ 下得到的数）。一旦统一到读法 T，$\alpha$ 必须是 $11.52$，而非 $2.62$。100 倍换算错误恰好把这个 $11.5$ 压成 $2.62$，制造了与 Shekhter $2.6$ 的假相容——**这是一次典型的"单位约定错误掩盖理论冲突"**。

---

## 第四部分：M.85′ 裸刚度修正——三数首次自洽闭合

### §4.1 把凝聚分数放进耗散率

《Homes 稿》M.85 的识别是 $\hbar/\tau(T_c)=2\pi J$，其中 $J$ 取凝聚后的有效刚度 $J_{\rm eff}$（因 $k_BT_c/J_{\rm eff}=2.2017$），给

$$\alpha=\frac{2\pi}{k_BT_c/J_{\rm eff}}=2.854.\tag{M.85}$$

但读法 T 要求 $\alpha=11.52$。两者之比

$$\frac{11.52}{2.854}=4.04\approx\frac{1}{n_s/n}=4.$$

这不是巧合。令耗散率由**裸刚度** $J_0=4J_{\rm eff}$ 设定：

$$\frac{\hbar}{\tau(T_c)}=2\pi J_0=8\pi J_{\rm eff}\quad\Longrightarrow\quad \alpha=\frac{8\pi}{k_BT_c/J_{\rm eff}}=\frac{8\pi}{2.2017}=11.415.\tag{M.85′}$$

回代 (M.95)：

$$\eta_{\rm pred}=41.673\times\frac14\times11.415=118.96,\qquad \frac{118.96-120}{120}=-0.87\%.$$

**零参数闭合**：$1/4$ 来自 M.83（键相干因子，XY 数值检验确认），$2.2017$ 来自 3D XY，$8\pi=2\pi/(1/4)$ 是代数组合，$41.673$ 是 SI 常数。无一处可调。

> **物理理由（构造，须标注）**：$T\to T_c$ 的正常态尚未凝聚，相位涨落的能量尺度应由裸耦合 $J_0$ 设定，而非凝聚后的 $J_{\rm eff}$；$J_{\rm eff}=J_0/4$ 只在 $T<T_c$ 的超流态才是有效刚度。Shekhter 的"同一个 $n/m^*$"等价于取 $J_0\to J_{\rm eff}$（凝聚分数 1），故其 $\alpha=2.6$ 是 $J_{\rm eff}$ 版本的**表观系数**。

### §4.2 与 M.84 错误值的定量关系

$$\underbrace{2.62}_{\text{M.84 错值}}\times\underbrace{4}_{1/(n_s/n)}\times\underbrace{1.10}_{\text{换算松量}}\approx11.5.$$

即 M.84 的错误可以精确分解为两步：换算差 100 倍（已撤销）+ 凝聚分数漏乘 4（本轮补上）。修正后不再是"与 $2.6$ 差 $0.8\%$"，而是"与 Shekhter 的 $2.6$ 差 $4.4$ 倍，且这 $4.4$ 倍由凝聚分数定量解释"。

### §4.3 分辨率与诚实边界

- Shekhter 的 $\alpha=2.6$ 与 $\eta=42\alpha=109$ 对应；《Homes 稿》LH1 引 $\eta=120\pm25$。两者本身差 $10\%$。用 $\eta=109$ 反解得 $\alpha=10.47$，与 $8\pi/2.2017=11.415$ 差 $8.3\%$——**在同篇约定的 $\pm10\%$ 分辨率内**。故本轮全部 $\alpha$ 比较仍沿用 ±10% 分辨率。
- $2\pi$ 的归一仍是【识别】不是【推导】（沿用《Homes 稿》§4.3 边界）；本轮升级的是 **$J_{\rm eff}\to J_0$** 这一步，它由凝聚分数 $1/4$ 强制，不是新拟合。
- 若改为 $\hbar/\tau=J_0$，则 $\alpha=1.82$，$\eta=19$，被实验排除 6 倍——$2\pi$ 仍是被数据选中的归一，已诚实标注。

---

## 第五部分：两阶段耗散判据（可证伪预言 R25）

### §5.1 两个 $\alpha$ 不矛盾，属于两阶段

核心文档 DM.13 的两阶段判据 $T_c=\min(T^*,T_\theta)$ 把系统分成两个区域，本轮给出各自的耗散系数：

| 区域 | 探针温区 | 刚度 | $\alpha$ | 出处 |
|:--|:--|:--|:--|:--|
| 配对通道（$T\to0,\ p^*$） | 低温极低温、临界掺杂 | 配对能标 $\hbar\omega$（非相位刚度） | $\alpha_{p^*}\approx1$（LH14） | 实验直接测 |
| 相位通道（$T\to T_c$） | $T_c$ 上方红外 | 裸相位刚度 $J_0$ | $\alpha_{T_c}\approx11.4$（M.85′） | 由 Homes 斜率 + Tanner 反推 |

Shekhter（LH10）已观察到"$T_c$ 附近电阻偏离 $T$-linear，通常不超过因子 3"，并以对数精度为由忽略。本轮把它定量化为 **$11.4/1\approx11$ 的偏离**，并给出机制（两阶段 + 裸刚度）。这是可判别的：

> **R25（可证伪）**：在**同一材料**上，分别测 (i) $T\to0$、高场抑制超导、$p^*$ 附近的 $\rho(T)$ 斜率得 $\alpha_{p^*}$；(ii) $T_c^+$ 附近的红外/太赫兹散射率得 $\alpha_{T_c}$。若两阶段图像成立，应有 $\alpha_{T_c}/\alpha_{p^*}\approx (2\pi J_0)/(\hbar\omega)\cdot(\hbar\omega/\text{...})$ 的量级 $O(10)$；若两者实测相等（都 $\approx1$ 或都 $\approx2.6$），则 M.85′ 的裸刚度识别被否定，需退回读法 S 并放弃 M.83 进 Homes。

**R26（辅助判据）**：Fe(Te,Se) 类样品（LH16，$\alpha=1.38$，守 Homes 不守 Uemura）应在 Uemura 支（欠掺杂铜氧化物）与 Homes 支之间分化：相位限制支守 Homes 且 $\alpha_{T_c}$ 大；配对限制支守 Uemura 且 $\alpha\approx1$。

### §5.2 R17 的更新

《Homes 稿》R17 原表述"$\alpha_{\rm res}$ 在 $T_c$ 附近是否升到 $2.85$"应改为 **"是否升到 $11.4$"**；若实测只升到 $\approx2.6$，则支持读法 S（Tanner 因子不进 Homes），M.83 与 Homes 的联系需重新审查。

---

## 第六部分：与黎曼零点、质数、记忆核、相变的关系（收束）

按命题 Z 的三分法，本轮**不新增**零点/质数侧的结论，只说明位置：

| 对象 | 在理论中的位置 | 本轮影响 |
|:--|:--|:--|
| $\zeta$ 零点 $\gamma_n$ | 记忆核形状载体 | 无。本轮全部是几何标度通道（$J_0,\eta$） |
| 质数分布/mod-6 | 整数权载体，给 $1/4$（M.83） | **间接强化**：$1/4$ 本轮第二次进入定量结果（耗散率 $8\pi$），仍走 mod-6 整数权，不经零点 |
| 黎曼猜想 | 形状侧 | 无 |
| 记忆核 | 相变序参量载体；M.86 $\Phi(t/\tau(T))$，$\tau=\alpha\hbar/k_BT$ | **受影响**：若 $\alpha$ 在 $T_c$ 附近为 $11.4$ 而非 $2.85$，则 M.86′ 的热标度 $\tau(T)$ 在相位通道要重标 4 倍；零点时刻 $t_n\propto1/T$ 的形式不变（R16′ 的形状-标度分离保持） |
| 相变 | 锚点出现；判据 DM.13 | 无。两阶段判据不变，本轮给其两个通道各配一个耗散系数 |

一句话：**零点管形状、质数管整数权、几何管标度**——本轮是"几何管标度"内部的修正（$J_0$ vs $J_{\rm eff}$），未触碰形状侧。

---

## 第七部分：退化检查

| 极限 | 要求 | 本轮是否保持 | 说明 |
|:--|:--|:--|:--|
| **BCS 退化** | 均匀极限 $\delta\to0$，$\langle\cos\mathcal H\rangle\to1$，$n_s/n\to1$ | ✓ | 此时 $J_{\rm eff}\to J_0$，$8\pi\to2\pi$，M.85′ 自动退回 M.85 的 $\alpha=2.854$；凝聚分数 $1$ → 读法 S 成立。退化是结构性的 |
| **迈斯纳效应** | $\lambda_L^2=m^*/(\mu_0n_se^2)$ | ✓ | 未改伦敦公式，只改 $n_s$ 在 Homes 斜率中的读法；$\lambda_L=2\lambda_p/\sqrt\Lambda$ 保持 |
| **Uemura** | 相位限制支 $T_c\propto n_s$ | ✓ | M.83 未动；R26 反而给出 Uemura/Homes 分化的判据 |
| **命题 Z2（能标外生）** | 绝对 $T_c$ 无第一性 | ✓ | 本轮定的是**无量纲乘积** $(n_s/n)\alpha$，仍需外部 $T_c$ 与 $J_{\rm eff}$ 换算；不构成对 Z2 的反例 |
| **命题 Z1（零点谱隙不可识别）** | — | ✓ | 本轮未触碰闭式 chain |

---

## 第八部分：开放项

| # | 问题 | 性质 | 建议路径 |
|:--|:--|:--|:--|
| Q1 | $\eta_{\rm Homes}$ 取值 $109$（LH10）vs $120$（LH1），带 $\pm25$ | 外部实验离散 | 以 $\pm10\%$ 为分辨率；若能取到 Homes 2004 原始数据表，重新拟合斜率 |
| Q2 | $\hbar/\tau=2\pi J_0$ 的 $2\pi$ 归一 | 单点识别 | 从 DM.1 相位动力学直接算滑移率前因子（承《Homes 稿》Q2） |
| Q3 | $\alpha_{T_c}$ 是否真为 $11.4$ | R25，可证伪 | 同一材料双温区测 $\rho(T)$ 斜率 |
| Q4 | Shekhter 印刷公式 $C=\alpha(k_B/\hbar)/\pi c^2$ 的字面 10 倍歧义 | 外部排版 | 已用 SI 第一性重建 (M.95) 绕过，不必追其笔误 |
| Q5 | M.83 的 $1/4$ 是否应进 Homes 斜率 | 读法 S vs T | R25 判决；若支持 S，需解释为何 Tanner 因子在 Homes 中被吸收 |

---

**本轮确认并记录的关键推进**（作者指令：确认成果必须记录）：

1. **硬纠错**：《Homes 稿》M.84 换算因子内部差 100 倍（$8.988\times10^{11}$ vs $8.988\times10^{9}$），"$\alpha=2.62$ 与 $2.6$ 差 $0.8\%$"为假相容，已撤销。
2. **第一性关系 M.95**：$\eta=41.673(n_s/n)\alpha$，从 SI 重建 Shekhter 的 $42\alpha$（$0.8\%$ 一致），并证明 Homes 斜率只约束乘积 $(n_s/n)\alpha=2.88$。
3. **判决**：Shekhter 2025 的 $\alpha\approx2.6$ 隐含 $n_s=n$，与 M.83 的 $1/4$ 不相容；坚持 $1/4$ 则 $\alpha_{\rm Homes}=11.52$，与 Planckian $\alpha\approx1$ 差 11.5 倍——真实张力，已诚实登记。
4. **M.85′（零参数闭合）**：$\hbar/\tau=2\pi J_0=8\pi J_{\rm eff}$，$\alpha=11.415$，$\eta_{\rm pred}=118.96$ vs $120$（$-0.9\%$）。M.83 + M.85 + Homes 首次自洽。Shekhter 的 $2.6$ 被识别为 $J_{\rm eff}$ 版表观系数。
5. **R25/R26（可证伪）**：两阶段各配一个耗散系数（$p^*$ 处 $\alpha\approx1$，$T_c$ 处 $\alpha\approx11.4$），双温区同材料测量可判决；R17 的阈值由 $2.85$ 更新为 $11.4$。
6. **边界守住**：绝对 $T_c$ 仍无第一性（Z2），BCS/迈斯纳/Uemura 退化全部保持，零点/质数形状侧未触碰。

---

**版本**：v0.1（2026-11-17，探索稿；非权威源）。承接《Homes 稿》v0.1；硬纠错 1 项、新增 M.95/M.85′、R25/R26。外部对照 LH10–LH16。全部数值由 Python 现场计算（构造后验数字校验，待独立复现），脚本在 `10 探索/.calc/homes_unit_audit.py`、`m84_internal_audit.py`、`conv_check.py`（`.calc/` 已 gitignore）。本轮未删任何文档、未提交 git、未做 Lean/网站/完整理论文档。
