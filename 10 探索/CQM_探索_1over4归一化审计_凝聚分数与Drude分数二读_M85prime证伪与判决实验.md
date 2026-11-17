# CQM 探索：$1/4$ 的归一化审计——凝聚分数与 Drude 分数二读、M.85′ 证伪与判决实验

> **定位**：探索稿（非权威源），v0.2，2026-11-17。承接《Homes 稿》（M.83–M.86）、《Homes 斜率纠错》（M.95/M.85′）、《FGT 光学求和规则》（F.3/F.4）与《迈斯纳退化》（R37）。本轮只做归一化审计：把"总谱重、Drude 权重、超流密度"三个密度分开，判定 M.85′ 的"零参数闭合"是否成立，并给出一个能判决 $1/4$ 身份的配对实验。v0.2 增补 Broun §VI 的"Tanner's law"因子 $4$ 原文与 Padilla 2005 的欠掺杂 $f_D\approx20\%$，把 Q1 从"待判"推进到"B 自然、A 需 $\Lambda$ 塌缩"。
>
> **边界**：不改 `01–07`、`归档/`、`08` 的任何定义、数值与缺口状态；不宣称缺口闭合；不更新 Lean/网站。外部文献只作对照，CQM 构造与外部事实分栏标注。全部数值为构造后验数字校验，待第三方复现。
>
> **一句话结论**：M.85′ 确定被证伪——它把 $f_c=1/4$ 代入了只应含 $f_s\approx0.9$ 的 Homes 公式；原 M.85 作为候选存活。$1/4$ 的身份已由现有文献推进到"读法 B 唯一无需 $\Lambda$ 塌缩"：Tanner 的 $20\%$ 是 $f_c$，Broun 的 $f_s\approx0.9$ 与"Tanner's law"的 Drude 权重因子 $4$ 给出 $f_D\approx1/4$，Padilla 2005 更在欠掺杂直接测得相干 Drude 分数 $\approx20\%$；读法 A 只有在 $\Lambda$ 随 $f_s$ 同步塌缩时才不被排除。R43 由现有数据部分满足，剩余是精度与 $\Lambda$ 的独立标定。

---

## 第零部分：判决清单（先看结论）

| # | 判决 | 性质 | 后果 |
|:--|:--|:--|:--|
| 1 | 光学有三个密度：总谱重 $n_{\rm tot}$、Drude 权重 $n_D$、超流密度 $n_s$；两个分数 $f_c=n_s/n_{\rm tot}$、$f_s=n_s/n_D$，恒等式 $f_c=f_Df_s$，$f_D=n_D/n_{\rm tot}$ | 【严格：定义 + 代数】 | 此前把 $f_c$ 与 $f_s$ 混用，是 M.85′ 错误的根源 |
| 2 | 最优掺杂铜氧：$f_s=0.80$–$0.95$（Broun 表 1），$f_c=0.20$–$0.25$（Tanner/FGT），故 $f_D=0.21$–$0.31$，中心 $0.25$ | 【外部数据 + 代数】 | $1/4$ 与 $f_D$ 数值吻合；但 $f_c$ 也在同一区间，两读退化 |
| 3 | **M.85′ 证伪**：它把 $f_c=1/4$ 当作 Homes 公式的系数；正确系数是 $f_s\approx0.89$。若坚持 $\alpha=11.415$，则 $\eta=423$，被实验排除；若取 $\eta=120$，则 $\alpha=3.24$，不是 $11.4$ | 【严格：M.95 + 外部 $f_s$】 | "$\eta_{\rm pred}=118.96$ vs $120$（$-0.9\%$）零参数闭合"撤销 |
| 4 | **原 M.85 存活**：$\alpha=2\pi/2.2017=2.854$，$\eta_{\rm pred}=41.673f_s\alpha=106$–$113$（$f_s=0.89$–$0.95$），对 $\eta=109$–$120$ 在 $-12\%$ 内；在 $\eta=109$、$f_s=0.92$ 处 $\alpha=2.843$，与 $2.854$ 差 $0.4\%$ | 【候选：单点识别 + 外部数据】 | M.85 不是"零参数"，但仍是与光学数据相容的候选 |
| 5 | **迈斯纳因子 $2$ 的口径**：$\lambda_L/\lambda_{p,\rm tot}=1/\sqrt{f_c}=2.00$–$2.24$；用 Drude 口径是 $\lambda_L/\lambda_{p,D}=1/\sqrt{f_s}=1.03$–$1.12$。因子 $2$ 只在**总 f-sum** 口径成立 | 【严格：代数】 | 《Homes 稿》第 258 行"要求 Drude 权重而非全带 f-sum"与 R37c 同句均反了 |
| 6 | **"四次独立确认"降级**：Tanner、FGT、迈斯纳因子 $2$ 是同一个 $f_c$ 恒等式的三次读数；Homes 斜率独立，但它读 $f_s\alpha$，不读 $f_c$ | 【审计】 | "一个定义 + 一次独立动力学检验"，不是四次独立 |
| 7 | **二读；B 是唯一无需 $\Lambda$ 塌缩的读法**：Tanner 的 $20\%$ 相对总谱重，是 $f_c$；Broun 的 $f_s\approx0.9$ 与"Tanner's law"的 Drude 权重因子 $4$ 给出 $f_D\approx1/4$；Padilla 2005 在欠掺杂 LSCO/YBCO 直接测得相干 Drude 分数 $\approx20\%$。读法 A（$f_c=1/4$）要求 $\Lambda\approx4f_Df_s\approx0.8f_s$，从最优掺杂的 $\sim0.9$ 塌到 LSCO 7 K 的 $\sim0.02$；读法 B 无需此塌缩 | 【现有数据判决：B 自然，A 需 $\Lambda$ 塌缩】 | R43 由 Padilla 数据部分满足；剩余为同一样品的 FGT+Drude 配对与 $\Lambda$ 独立标定 |
| 8 | 不变项：ζ 通道 no-go、两阶段 $T_c=\min(T^*,T_\theta)$、BCS 退化（理想极限）、3D XY $\nu=0.6717$、绝对 $T_c$ 外生（Z2/Z3） | 【既有】 | 本轮不触碰 |

---

## 第一部分：三个密度、两个分数

### §1.1 定义

光学电导的 f-sum（Broun 用角频率 $\omega$ 约定）：

$$\int_0^{\omega_c}\sigma_1(\omega)\,d\omega=\frac{\pi}{2}\epsilon_0\omega_p^2,\qquad \omega_p^2=\frac{n_{\rm tot}e^2}{\epsilon_0m_{\rm tot}}. \tag{1.1}$$

三个密度：

| 符号 | 名称 | 实验来源 | 物理含义 |
|:--|:--|:--|:--|
| $n_{\rm tot}$ | 总低能谱重 | 全谱 f-sum 到截断 $\omega_c$ | Tanner 的 $n$；包含 Drude + 中红外/非相干谱重 |
| $n_D$ | Drude 权重 | 正常态 Drude–Lorentz 拟合的零频峰 | Broun 的 $\omega_{p,D}^2$；相干载流子 |
| $n_s$ | 超流密度 | $\lambda_L^{-2}=\mu_0n_se^2/m^*$ 或 FGT 缺失面积 $N_c$ | 凝聚后无耗散响应 |

两个分数：

$$f_c\equiv\frac{n_s}{n_{\rm tot}}=\frac{\omega_{p,s}^2}{\omega_p^2},\qquad f_s\equiv\frac{n_s}{n_D}=\frac{\omega_{p,s}^2}{\omega_{p,D}^2},\qquad f_D\equiv\frac{n_D}{n_{\rm tot}}. \tag{1.2}$$

恒等式：

$$\boxed{f_c=f_D\,f_s.} \tag{1.3}$$

> **约定说明**：$\omega$ 与 $\nu$ 的 $2\pi$ 因子在比值中全部抵消；本文只比较无量纲分数，不比较绝对等离子体频率。严格地说，$f_c=\omega_{p,s}^2/\omega_p^2=(n_s/m_s)/(n_{\rm tot}/m_{\rm tot})$、$f_s=\omega_{p,s}^2/\omega_{p,D}^2=(n_s/m_s)/(n_D/m_D)$，质量重正化已包含在等离子体频率比中；只有在 $m_s=m_D=m_{\rm tot}$ 时才可把 $f_c,f_s$ 读作纯密度比。本文的数值比较不依赖这一简化。

### §1.2 三个探针各读什么

| 探针 | 读数 | 归一化 | 出处 |
|:--|:--|:--|:--|
| Tanner / FGT 缺失面积 | $N_c/S_{\rm tot}$ | 总 f-sum | Tanner et al., *Physica B* **244**, 1 (1998)；Homes 2004/2005；FGT 稿 F.3 |
| 迈斯纳 $\lambda_L$ | $\lambda_L^{-2}\propto n_s/m^*$ | 与 $\omega_p$ 比较时才需选口径 | R37 式 (2) |
| Homes 斜率 | $\rho_s/(\sigma_{dc}T_c)$ | $\sigma_{dc}$ 用**正常态 Drude 权重** | Homes 2004；Broun 2025 表 1 |

关键：Tanner 的 $n_s/n\approx0.20$ 是 $f_c$；Broun 的 $f_s=\omega_{p,s}^2/\omega_{p,D}^2$ 是 $f_s$。两者不是同一个量，差一个 $f_D$。

---

## 第二部分：外部数据

### §2.1 最优掺杂铜氧

Broun（Broun, Mishra, Dodge, *Beyond Homes scaling: disorder, the Planckian bound and a new universality*, arXiv:2502.13351）表 1 的 $f_s$ 与 Tanner/FGT 的 $f_c$ 并置。$f_c$ 取 $0.20$–$0.25$（Tanner 极限 $0.25$，簇化后 $0.20$–$0.22$），$f_D=f_c/f_s$：

| 材料 | $T_c$ (K) | $f_s$（Broun） | $f_c$（Tanner/FGT） | $f_D=f_c/f_s$ | $\lambda_L/\lambda_{p,\rm tot}$ | $\lambda_L/\lambda_{p,D}$ |
|:--|--:|--:|--:|--:|--:|--:|
| La$_{2}$CuO$_{4.12}$ | 40 | 0.80 | 0.20–0.25 | 0.250–0.312 | 2.00–2.24 | 1.12 |
| Tl$_{2}$Ba$_{2}$CaCu$_{2}$O$_{8+\delta}$ | 110 | 0.88 | 0.20–0.25 | 0.227–0.284 | 2.00–2.24 | 1.07 |
| Bi$_{2}$Sr$_{2}$CaCu$_{2}$O$_{8+\delta}$ (a) | 85 | 0.95 | 0.20–0.25 | 0.211–0.263 | 2.00–2.24 | 1.03 |
| Bi$_{2}$Sr$_{2}$CaCu$_{2}$O$_{8+\delta}$ (b) | 85 | 0.94 | 0.20–0.25 | 0.213–0.266 | 2.00–2.24 | 1.03 |
| Bi$_{2}$Sr$_{2}$CaCu$_{2}$O$_{8+\delta}$ (c) | 85 | 0.88 | 0.20–0.25 | 0.227–0.284 | 2.00–2.24 | 1.07 |
| YBa$_{2}$Cu$_{3}$O$_{7}$ | 91 | 0.92 | 0.20–0.25 | 0.217–0.272 | 2.00–2.24 | 1.04 |
| YBa$_{2}$Cu$_{3}$O$_{7-\delta}$ | 92 | 0.89 | 0.20–0.25 | 0.225–0.281 | 2.00–2.24 | 1.06 |

**读数**：$f_D$ 集中在 $0.21$–$0.31$，中心 $0.25$。这是 $1/4$ 与 $f_D$ 吻合的直接原因；但 $f_c$ 本身也在 $0.20$–$0.25$，所以同一张表也支持"$1/4=f_c$"。两读在最优掺杂退化，不能只靠这张表判决。

> **Tanner 的原话（外部，定义层）**：Tanner 等（*Physica C* **341–348**, 2193 (2000)）明确写：清洁金属超导体的超流密度"essentially equal to the conduction electron density"；铜氧化物则"only about 20% of the doping-induced spectral weight joins the superfluid. The rest remains in finite-frequency, midinfrared absorption." 这句话把 $20\%$ 的归一化钉在**总低能（掺杂诱导）谱重**上，即 $f_c$，不是 Drude 权重。结合 Broun 的 $f_s\approx0.9$，自然读出 $f_D=f_c/f_s\approx0.22$——这是读法 B 的直接外部支撑。

> **同一混用的第二处**：《Homes 稿》第 117 行（LH7 转述）把 Tanner 的"约 $4$–$5$ 倍"读成"凝聚部分占 **Drude 权重**的 $1/4$–$1/5$"。这也是把总谱重与 Drude 权重混用：Tanner 的 $20\%$ 是相对**总谱重**，不是相对 Drude 权重。若按后一读法取 $f_s\approx0.2$，Homes 斜率给出 $\eta\approx24$（取 $\alpha=2.854$），与 $120$ 差 $5$ 倍，立即被排除。故 LH7 的这句转述不能作为 $f_s\approx0.25$ 的证据；它和第 258 行是同一个口径错误的两处表现。

### §2.2 欠掺杂与过掺杂的 $f_s$ 塌缩

Broun 表 1 的 LSCO 与 YBCO$_{6.333}$ 序列显示 $f_s$ 随欠掺杂强烈塌缩：

| 材料 | $T_c$ (K) | $f_s$ |
|:--|--:|--:|
| La$_{2-x}$Sr$_x$CuO$_4$ | 27.5 | 0.423 |
| La$_{2-x}$Sr$_x$CuO$_4$ | 19.5 | 0.227 |
| La$_{2-x}$Sr$_x$CuO$_4$ | 17.5 | 0.206 |
| La$_{2-x}$Sr$_x$CuO$_4$ | 10.5 | 0.065 |
| La$_{2-x}$Sr$_x$CuO$_4$ | 7.0 | 0.031 |
| YBa$_{2}$Cu$_{3}$O$_{6.333}$ | 16.9 | 0.512 |
| YBa$_{2}$Cu$_{3}$O$_{6.333}$ | 12.1 | 0.319 |
| YBa$_{2}$Cu$_{3}$O$_{6.333}$ | 7.0 | 0.151 |
| YBa$_{2}$Cu$_{3}$O$_{6.333}$ | 4.2 | 0.079 |

**关键**：$f_s$ 不是普适常数，而是随掺杂塌缩的动力学量。任何把 $1/4$ 直接当作 $n_s/n_D$ 的公式，都会在欠掺杂给出错误量级——这正是 M.85′ 的结构性错误。

### §2.3 常规超导的 $f_s$（校准警告）

Broun 表 1 的常规超导条目：

| 材料 | $T_c$ (K) | $f_s$ | $\lambda_L/\lambda_{p,D}$ | 由 $f_s$ 反推的 $\lambda_L$ (nm) |
|:--|--:|--:|--:|--:|
| Nb | 8.3 | 0.056 | 4.23 | 90.4 |
| Nb | 9.3 | 0.231 | 2.08 | 44.4 |
| Pb | 7.2 | 0.476 | 1.45 | 38.8 |
| Nb-SrTiO$_3$ (0.1% Nb) | 0.168 | 0.278 | 1.90 | — |
| Sr$_2$RuO$_4$ | 1.5 | 0.941 | 1.03 | — |
| CeCoIn$_5$ | 2.25 | 0.879 | 1.07 | — |

> **警告**：即使 Pb 条目，$f_s$ 也只有 $0.48$；Nb 的 $f_s$ 强烈依赖样品（$0.056$–$0.231$）。因此《FGT 稿》§2 的"清洁 BCS 元素 $f_c\to1$"是**理想极限**，不是这批数据的直接读数。该句应降级为"无阻挫、无质量重正化的极限"。"常规超导的 $f_s<1$ 主要来自质量重正化/样品无序"只是一个**候选解释**，尚未逐项核对；列入开放项 Q2。

### §2.4 Broun 2025 的"Tanner's law"：Drude 权重因子 $4$

Broun 在 §VI 讨论 Planckian 区时写（外部，原文）：

> "...almost complete condensation of the available Drude weight into the superfluid condensate, recalling that inelastic scattering has already suppressed the Drude weight significantly relative to the noninteracting system. (As an aside, we note that in optimally doped cuprates this renormalization is approximately a factor of 4, a result that earlier has been dubbed 'Tanner's law'.)"

这句话把两个量分开：

1. "almost complete condensation of the available Drude weight" → $f_s=\omega_{p,s}^2/\omega_{p,D}^2\approx0.9$（表 1 的最优掺杂条目）；
2. "this renormalization is approximately a factor of 4" → $\omega_{p,D}^2/\omega_p^2\approx1/4$，即 $f_D\approx1/4$。

因此，Broun 的 $f_s$ 是**可用 Drude 权重的凝聚效率**，不是相对总谱重的凝聚分数；$1/4$ 在他的原文中对应**正常态 Drude 权重相对非相互作用系统的因子 $4$ 重整化**，即读法 B。定义层需要区分：§III 把 $\omega_{p,D}^2$ 操作性地定义为 Migdal–Eliashberg 模型内"零无序极限下的零温超流密度"；§IV.2 在实验层用正常态 Drude–Lorentz 拟合或 THz-TDS 的 $\lim_{\nu\to0}\nu\sigma_1^2/\sigma_2$ 提取 $\omega_{p,D}^2$。两者在 clean limit 下同一；对真实样品，$f_s$ 含无序/相位刚度抑制。

### §2.5 Padilla 2005：欠掺杂的 $f_D\approx20\%$

Padilla 等对欠掺杂 LSCO（$x=0.03$–$0.20$）与 YBCO（$y=6.2$–$7.0$）做了 Drude + 中红外双组分分解（*Phys. Rev. B* **72**, 060511(R) (2005), arXiv:cond-mat/0509307）。原文（外部，数据层）：

> "The coherent contribution amounts to approximately 20% of the total spectral weight below the CT excitation."

这里的 coherent contribution 是 Drude 拟合（或 $650\,\mathrm{cm}^{-1}$ 截断积分）给出的相干谱重，分母是电荷转移（CT）激发以下的总谱重；因此它就是本文的 $f_D=n_D/n_{\rm tot}$。在相应的欠掺杂区间（Broun 的 $f_s=0.03$–$0.5$），Padilla 读出 $f_D\approx0.20$，而不是 $0.25/f_s$。这与读法 B 一致；读法 A 若坚持 $\Lambda=1$，在同一区间要求 $f_D=0.25/f_s=0.5$–$8$，与 $0.20$ 差 $2.5$–$40$ 倍，且在 LSCO 7 K 给出 $f_D>1$。

> **边界**：$20\%$ 是欠掺杂区间的近似值，原文未给逐点误差；它也不是与 FGT $f_c$ 在同一样品上的配对测量。因此它足以把读法 A 逼到"$\Lambda$ 必须随 $f_s$ 塌缩"，但不足以把 $f_D=1/4$ 精确到百分位。R43 的剩余内容是同一样品的 FGT+Drude 配对与误差棒。

**读法 A 要容纳 Padilla 的 $f_D=0.20$ 需要多大的 $\Lambda$？** 由 $f_c=f_Df_s$ 与 $f_c=(1/4)\Lambda$：

$$\Lambda=4f_Df_s=0.8f_s\quad(f_D=0.20),\qquad \Lambda=f_s\quad(f_D=0.25). \tag{2.1}$$

数值见表 2.1。A 要求 $\Lambda$ 从 LSCO 27.5 K 的 $0.34$ 塌到 LSCO 7 K 的 $0.025$（约 $14$ 倍）；若从最优掺杂 $f_s\approx0.9$ 算起，则从 $0.72$–$0.90$ 塌到 $0.02$–$0.03$，约 $30$ 倍。B 则给出 $f_c=0.20f_s$，无需 $\Lambda$ 随掺杂塌缩（若坚持 $f_D=(1/4)\Lambda$，只需一个与掺杂无关的 $\Lambda\approx0.8$）。

| 材料 | $T_c$ (K) | $f_s$（Broun） | A：$f_D=0.25/f_s$（$\Lambda=1$） | Padilla $f_D$（区间近似） | A 所需 $\Lambda$（$f_D=0.20$） | B：$f_c=0.20f_s$ |
|:---|--:|--:|--:|--:|--:|--:|
| LSCO | 27.5 | 0.423 | 0.591 | 0.20 | 0.338 | 0.085 |
| LSCO | 17.5 | 0.206 | 1.214 | 0.20 | 0.165 | 0.041 |
| LSCO | 7.0 | 0.031 | 8.065 | 0.20 | 0.025 | 0.006 |
| YBCO$_{6.333}$ | 16.9 | 0.512 | 0.488 | 0.20 | 0.410 | 0.102 |
| YBCO$_{6.333}$ | 7.0 | 0.151 | 1.656 | 0.20 | 0.121 | 0.030 |
| YBCO$_{6.333}$ | 4.2 | 0.079 | 3.165 | 0.20 | 0.063 | 0.016 |

**读数**：Padilla 的 $f_D\approx0.20$ 与 B 的 $1/4$ 同量级；A 的 $\Lambda=1$ 列在 $f_s<0.8$ 时全部超过 $0.31$，并在 $f_s<0.25$ 时超过 $1$（物理上不可能）。A 要存活，$\Lambda$ 必须近似正比于 $f_s$，即几何分区因子必须与凝聚效率同步塌缩；这在 CQM 内没有独立依据。

---

## 第三部分：判决一——M.85′ 证伪

### §3.1 Homes 斜率的正确归一化

由 M.95（SI 第一性）：

$$\eta\equiv\frac{\rho_s}{T_c\sigma_{dc}}=41.673\,f_s\,\alpha,\qquad \alpha\equiv\frac{\hbar}{\tau k_BT}. \tag{3.1}$$

其中 $\sigma_{dc}$ 是正常态 Drude 电导，$\rho_s\propto n_s/m^*$。因此 Homes 斜率只约束乘积 $f_s\alpha$，**不含 $f_c$**。

### §3.2 M.85′ 错在哪里

M.85′ 写

$$\frac{\hbar}{\tau}=2\pi J_0=8\pi J_{\rm eff}\ \Longrightarrow\ \alpha=\frac{8\pi}{2.2017}=11.415, \tag{3.2}$$

然后回代 M.95 时取 $f_c=1/4$：

$$\eta_{\rm pred}=41.673\times\frac14\times11.415=118.93. \tag{3.3}$$

**这一步把 $f_c$ 当成了 $f_s$**。正确的回代是 $f_s\approx0.89$：

$$\eta_{\rm pred}=41.673\times0.89\times11.415=423.4, \tag{3.4}$$

被 $\eta=109$–$120$ 排除 $3.5$–$3.9$ 倍。反过来，若固定 $\eta=120$，则

$$\alpha=\frac{120}{41.673\times0.89}=3.235, \tag{3.5}$$

不是 $11.4$。若取 $\eta=109$，则 $\alpha=2.939$。

| $\eta$ | $f_s=0.80$ | $0.88$ | $0.89$ | $0.92$ | $0.95$ |
|--:|--:|--:|--:|--:|--:|
| 109 | 3.269 | 2.972 | 2.939 | 2.843 | 2.753 |
| 120 | 3.599 | 3.272 | 3.235 | 3.130 | 3.031 |

**判决**：M.85′ 的 $\alpha=11.415$ 与 Homes 斜率不相容；其"$\eta=118.96$ vs $120$（$-0.9\%$）"是拿 $f_c$ 冒充 $f_s$ 得到的假闭合。撤销。

### §3.3 原 M.85 为什么存活

原 M.85 的 $\alpha$ 来自

$$\alpha=\frac{2\pi}{k_BT_c/J_{\rm eff}}=\frac{2\pi}{2.2017}=2.854, \tag{3.6}$$

它不预设 $f_c=1/4$，只预设 $\hbar/\tau(T_c)=2\pi J_{\rm eff}$。回代 (3.1)：

| $f_s$ | 0.80 | 0.88 | 0.89 | 0.92 | 0.95 |
|--:|--:|--:|--:|--:|--:|
| $\eta_{\rm pred}$ | 95.1 | 104.7 | 105.8 | 109.4 | 113.0 |

对 $\eta=109$–$120$，$f_s=0.88$–$0.95$ 给出 $-12\%$ 到 $-5.8\%$ 的偏差；在 $\eta=109$、$f_s=0.92$ 处偏差仅 $0.4\%$。这是**一个候选识别**，不是零参数闭合：$2\pi$ 是识别，$2.2017$ 是外部 3D XY 常数，$f_s$ 是外部光学数据。三者的组合恰好落在 Homes 斜率的 $\pm10\%$ 分辨率内，但不构成"无参数预言"。

> **诚实边界**：若把 $2\pi$ 改成 $1$，$\alpha=0.454$，$\eta=17$–$18$，被排除 $6$ 倍；$2\pi$ 仍是被数据选中的归一。若把 $2.2017$ 改成平均场 $1.5$，$\alpha=4.19$，$\eta=155$–$166$，偏高 $30\%$。故 3D XY 标定与 $2\pi$ 两者都被数据偏好，但都不是第一性推导。

---

## 第四部分：判决二——迈斯纳因子 $2$ 的口径

由 R37 式 (2)，对总 f-sum 口径：

$$\frac{\lambda_L}{\lambda_{p,\rm tot}}=\frac{1}{\sqrt{f_c}}=\frac{1}{\sqrt{f_Df_s}}. \tag{4.1}$$

对 Drude 口径：

$$\frac{\lambda_L}{\lambda_{p,D}}=\frac{1}{\sqrt{f_s}}. \tag{4.2}$$

数值：

| $f_c$ | $\lambda_L/\lambda_{p,\rm tot}$ | $f_s$ | $\lambda_L/\lambda_{p,D}$ |
|--:|--:|--:|--:|
| 0.20 | 2.236 | 0.80 | 1.118 |
| 0.22 | 2.132 | 0.89 | 1.060 |
| 0.25 | 2.000 | 0.95 | 1.026 |

**判决**：所谓"$\lambda_L=2\lambda_p$"是 $\lambda_L=2\lambda_{p,\rm tot}$，因子 $2$ 来自 $1/\sqrt{f_c}$；若用 Drude 等离子体波长，因子是 $1.06$，不是 $2$。因此：

1. 《Homes 稿》第 258 行"它要求 $\omega_p$ 取 Drude 权重而非全带 f-sum"**反了**：因子 $2$ 恰恰要求全带 f-sum；用 Drude 权重会得到 $1.06$。
2. 《迈斯纳》§2.1 与 R37c 的"$\lambda_L/\lambda_p<2$ 则 $1/4$ 受质疑"必须重述为："若用**总 f-sum** 口径测得 $\lambda_L/\lambda_{p,\rm tot}<2$，则 $f_c>1/4$；若用 **Drude** 口径测得 $\lambda_L/\lambda_{p,D}\approx1$，则 $f_s\approx1$，与 $f_c$ 无关。"
3. 迈斯纳因子 $2$ 不是 $1/4$ 的独立证据：它与 Tanner/FGT 共用同一个 $f_c$，只是把 $f_c$ 开根号。

---

## 第五部分：判决三——三次读数不是三次独立确认

| 探针 | 读的量 | 是否独立 |
|:--|:--|:--|
| Tanner 凝聚分数 | $f_c=N_c/S_{\rm tot}$ | 定义 |
| FGT 缺失面积 | $f_c=N_c/S_{\rm tot}$ | 与 Tanner 同一恒等式，换样品/换拟合 |
| 迈斯纳 $\lambda_L=2\lambda_{p,\rm tot}$ | $f_c$ | 与 Tanner 同一恒等式，经开根 |
| Homes 斜率 | $f_s\alpha$ | **独立动力学组合**，但不读 $f_c$ |
| Uemura $T_c\propto n_s/m^*$ | $f_c$ 或 $f_s$（取决于归一化） | 相位支，与 Homes 两阶段分化 |

**结论**：

- "1/4 第四次进入零参数结果"（FGT 稿 §2）应改为"$1/4$ 的同一个定义（现判为 $f_D$）第四次被不同探针读出"。这是**定义的一致性**，不是四次独立确认。
- 真正的独立检验只有 Homes 斜率，而它读的是 $f_s\alpha$；它约束的是 $f_s$ 与 $\alpha$ 的乘积，不是 $1/4$ 本身。
- 因此台账应写成：**一个定义（现判为 $f_D$，见 §2.4–§2.5）+ 一次独立动力学检验（Homes $f_s\alpha$）**。此前"四次独立"的说法撤销。

---

## 第六部分：二读判决与精度实验

### §6.1 两种读法

**读法 A（原读，保守）**：

$$f_c=\frac14\Lambda,\qquad f_D=\frac{f_c}{f_s}=\frac{\Lambda}{4f_s}. \tag{6.1}$$

$1/4$ 是凝聚分数；欠掺杂 $f_s$ 塌缩时，$f_D$ 必须上升，或 $\Lambda$ 必须塌缩，以保持 $f_c\le1/4$。Padilla 的 $f_D\approx0.20$ 排除了前者，故 A 只剩 $\Lambda$ 塌缩一条路。DM.11 的 $J_{\rm eff}=J_0\langle\cos H\rangle$ 保持原样（$\Lambda$ 吸收掺杂）。

**读法 B（新读，现有数据判决为唯一无需 $\Lambda$ 塌缩）**：

$$f_D=\frac14\Lambda,\qquad f_c=f_Df_s=\frac14\Lambda f_s. \tag{6.2}$$

$1/4$ 是正常态相干 Drude 分数；欠掺杂 $f_c$ 随 $f_s$ 塌缩，$f_D$ 保持 $\approx0.20$–$0.25$。若写入核心，DM.11 需细化为 $J_{\rm eff}=J_0(1/4)\Lambda f_s$，即刚度多一个凝聚效率因子——这属于核心层修改，须单独授权，本文只登记张力。

**为什么判 B**：(i) Tanner 2000 明确把 $20\%$ 归一在"doping-induced spectral weight"上，这是总低能谱重，不是 Drude 权重；(ii) Broun 的 $\omega_{p,D}$ 在实验层是正常态 Drude 权重（§IV.2），在模型层是"零无序极限下的零温超流密度"（§III）；两者在 clean limit 下同一，故 $f_s$ 是**可用 Drude 权重的凝聚效率**，最优掺杂 $f_s\approx0.9$ 已接近 clean limit；(iii) Broun §VI 明确把最优掺杂的 Drude 权重重整化称为"approximately a factor of 4... 'Tanner's law'"，即 $f_D\approx1/4$；(iv) Padilla 2005 在欠掺杂直接测得相干 Drude 分数 $\approx20\%$，与 B 的 $f_D\approx1/4$ 同量级，而 A 在 $\Lambda=1$ 下要求 $f_D=0.25/f_s$，在 $f_s<0.8$ 时超过 $0.31$，在 LSCO 7 K 达 $8.1$，与 Padilla 的 $0.20$ 冲突。A 只剩"$\Lambda$ 随 $f_s$ 塌缩"一条路；B 无需此塌缩，Occam 与数据都倾向 B。

### §6.2 两读的数值分歧

用 Broun 的 $f_s$ 与 $\Lambda=1$ 计算（本表取 $f_D=0.25$；若取 Padilla 的 $0.20$，B 列整体乘 $0.8$，见表 2.1）：

| 材料 | $T_c$ | $f_s$ | 读法 A：$f_c=0.25$，$f_D=0.25/f_s$ | 读法 B：$f_D=0.25$，$f_c=0.25f_s$ |
|:--|--:|--:|--:|--:|
| LSCO | 27.5 | 0.423 | $f_D=0.591$ | $f_c=0.106$ |
| LSCO | 17.5 | 0.206 | $f_D=1.214$（$>1$，须 $\Lambda\le0.824$） | $f_c=0.052$ |
| LSCO | 7.0 | 0.031 | $f_D=8.06$（$>1$，须 $\Lambda\le0.124$） | $f_c=0.0078$ |
| YBCO$_{6.333}$ | 16.9 | 0.512 | $f_D=0.488$ | $f_c=0.128$ |
| YBCO$_{6.333}$ | 7.0 | 0.151 | $f_D=1.656$（$>1$，须 $\Lambda\le0.604$） | $f_c=0.038$ |

**Padilla 的直接检验**：上表假设 $\Lambda=1$；Padilla 2005 在欠掺杂区间已测得 $f_D\approx0.20$。代入恒等式，A 要求 $\Lambda=4f_Df_s=0.8f_s$：从 LSCO 27.5 K 的 $0.34$ 塌到 LSCO 7 K 的 $0.025$（约 $14$ 倍）；若取 Broun 的 $f_D=0.25$，则 $\Lambda=f_s$，同样塌缩约 $14$ 倍。B 则给出 $f_c=0.20f_s$，从 $0.085$ 降到 $0.006$，无需 $\Lambda$ 随掺杂塌缩（最多一个常数 $\Lambda\approx0.8$ 的归一）。Padilla 的 $0.20$ 与 R43 的 $0.20$–$0.25$ 带相容；因此 R43 的判决条件已被现有数据近似满足，B 不再只是"倾向"。

**分歧是决定性的**：在 LSCO 7 K，读法 A 要求 $f_D=8.06$，物理上不可能（$f_D\le1$），除非 $\Lambda\le0.124$；读法 B 则自然给出 $f_c=0.0078$。两者对同一欠掺杂样品预言的 $f_c$ 在 $\Lambda=1$ 下差 $30$ 倍。**现有证据（Tanner 归一化 + Broun $f_s\approx0.9$ + Broun "Tanner's law" 因子 $4$ + Padilla 欠掺杂 $f_D\approx0.20$）使 B 成为唯一无需 $\Lambda$ 塌缩的读法；A 仍可借 $\Lambda\propto f_s$ 的塌缩容纳，但那是一个未获独立支持的额外假设。R43 的剩余任务是同一样品的 FGT+Drude 配对与误差棒，而不是从零判决。**

### §6.3 判决实验

> **R43（$1/4$ 身份判决）**：取同一欠掺杂样品（如 LSCO $T_c=7$–$20$ K 或 YBCO$_{6.333}$），在同一温度/同一表面同时测 (i) FGT 缺失面积 $N_c$ 与总 f-sum $S_{\rm tot}$ 得 $f_c$；(ii) 正常态 Drude–Lorentz 拟合得 $\omega_{p,D}^2$ 与 $\omega_p^2$ 得 $f_D$；(iii) $\lambda_L$ 独立校验 $f_s=f_c/f_D$。若 $f_D$ 在 $f_s=0.03$–$0.9$ 范围内保持 $0.20$–$0.25$（中心约 $0.22$，即 $1/4$ 的 $\pm20\%$ 带），读法 B 成立；若 $f_D$ 随 $1/f_s$ 上升（或 $\Lambda$ 必须塌缩到 $<0.2$ 才能避免 $f_D>1$），读法 A 成立。

> **R44（迈斯纳口径）**：最优掺杂铜氧若用 **Drude** 等离子体波长归一，应得 $\lambda_L/\lambda_{p,D}=1.03$–$1.12$；若实测为 $2$，则 $f_s\approx0.25$，与 Broun 的 $f_s\approx0.9$ 矛盾。若用**总 f-sum** 归一，应得 $2.00$–$2.24$。任何"$\lambda_L=2\lambda_p$"的报道必须注明 $\omega_p$ 口径，否则不可判决。

> **R45（Homes 指数）**：同一材料在 $T_c^+$ 附近测红外散射率，若两阶段图像成立，$\alpha_{T_c}$ 应在 $2.9$–$3.6$（本文）而不是 $11.4$（M.85′）。若实测 $\alpha_{T_c}\approx11$，M.85′ 复活，但需解释为何光学 $f_s\approx0.9$ 不进入 Homes 斜率。

---

## 第七部分：物理图像（构造，待独立检验）

若读法 B 成立，图像是"相干分区 + 凝聚效率"：

1. **曲率阻挫把 $3/4$ 的低能谱重推出相干 Drude 峰**。$\cos^2(\pi/3)=1/4$ 描述的是正常态中仍保持相位相干的 Drude 分数；其余 $3/4$ 进入中红外/非相干 reservoir。Broun §IV.2 的外部表述支持"存在 Drude/总谱重分区"这一**概念**："interactions shift part of the spectral weight to higher frequencies, leaving behind a reduced Drude weight near $\nu=0$." 但它不支持 $1/4$ 这个**数值**；数值仍是 CQM 的几何构造。
2. **凝聚发生在相干分区的内部**。$f_s$ 是这 $1/4$ 相干载流子的凝聚效率；最优掺杂 $f_s\approx0.9$，欠掺杂 $f_s$ 塌缩（相位刚度不足），于是 $f_c=f_Df_s$ 随掺杂下降。
3. **与两阶段一致**：$f_s$ 的塌缩属相位通道（$T_\theta$），$1/4$ 的相干分区属几何/正常态通道。两者相乘给出 Tanner 分数，而不是把 Tanner 分数全部归给几何。
4. **与 DM.11 的张力**：若 $J_0$ 是总密度刚度，则 $J_{\rm eff}=J_0f_c=J_0(1/4)\Lambda f_s$；核心 DM.11 的 $J_0\langle\cos H\rangle$ 是该式的 $\Lambda=1,f_s=1$ 极限。欠掺杂 $f_s<1$ 会进一步压低 $J_{\rm eff}$，定性上正是 Uemura 塌缩。是否把 $f_s$ 显式写入 DM.11，须核心层授权；本文只登记，不改。

**CQM 内部证据能判到哪一步**：M.87 的退火曲率数值检验（$T=0$ 扭转刚度，淬火 $0.71$–$0.72$、退火精确 $0.250$）直接计算的是 $J_{\rm eff}/J_0$，即**超流刚度**，不是正常态 Drude 权重。它在最优掺杂（$f_s\approx0.9$）只能固定乘积 $f_c=f_Df_s\approx1/4$，不能单独判 A/B；在欠掺杂它也没有给出 $f_s$ 的第一性值。故 A/B 的判决仍只能由欠掺杂的 $f_D$ 数据（Padilla）承担。B 的理论代价是：必须把 M.83 的 $1/4$ 从"凝聚刚度"重读为"相干正常权重"，并另设 $f_s$ 作为配对/相位效率——这正是 Q3 的构造缺口；A 的理论优势是 $1/4$ 直接等于 M.87 算出的 $J_{\rm eff}/J_0$，但须承担 $\Lambda\propto f_s$ 的塌缩。两者不是"数据全判 B"那么简单，本文的判决是**数据优先 B、理论成本 A 更低**。

> **反读法 B 的风险**：若 $f_D$ 并非 $1/4$，而是随掺杂强烈变化，则 $1/4$ 仍应回到 $f_c$（读法 A），本文的"相干分区"图像不成立。现有数据（Broun 因子 $4$ + Padilla 欠掺杂 $0.20$）已使 B 成为唯一无需 $\Lambda$ 塌缩的读法，但**核心层仍默认读法 A**，因为它保持 DM.11 不变且不需要授权修改；R43 的精度判决后再决定是否改核心。

---

## 第八部分：与 ζ 零点、质数、记忆核、相变的关系

| 对象 | 位置 | 本轮影响 |
|:--|:--|:--|
| ζ 零点 $\gamma_n$ | 记忆核形状载体 | 无。ζ 实轴 no-go 不变；$1/4$ 不来自零点 |
| 质数分布/mod-6 | 整数权载体，给 $1/4$ | 无。$1/4$ 仍是 $\cos^2(\pi/3)$ 的几何整数权；本轮只改它的归一化读法 |
| 黎曼猜想 | 形状侧 | 无 |
| 记忆核 | 相变序参量载体；M.86 $\Phi(t/\tau(T))$ | 无。Homes $\alpha$ 的修正只影响 $\tau(T)$ 的数值标定，不影响形状-标度分离 |
| 相变 | 锚点出现；判据 DM.13 | 无。两阶段 $T_c=\min(T^*,T_\theta)$ 不变；R43 只判 $1/4$ 的身份 |

一句话：**零点管形状，质数管整数权，几何管标度**——本轮是"几何管标度"内部的归一化纠错，未触碰形状侧。

---

## 第九部分：开放项

| # | 问题 | 性质 | 建议路径 |
|:--|:--|:--|:--|
| Q1 | $1/4$ 是 $f_c$ 还是 $f_D$ | 现有数据判决为 B；A 需 $\Lambda\propto f_s$ 塌缩 | Padilla 2005 已给欠掺杂 $f_D\approx0.20$；剩余为同一样品 FGT+Drude 配对、误差棒与 $\Lambda$ 独立标定。R43 不再是"从零判决"，而是"精度判决" |
| Q2 | 常规超导 $f_s<1$ 的来源 | 外部校准 | Pb $f_s=0.476$、Nb $f_s=0.056$–$0.231$；区分质量重正化、样品无序、绝对 $\lambda_L$ 标定。"清洁 BCS $f_c\to1$"须降为理想极限 |
| Q3 | 若读法 B，$f_s$ 能否从两阶段相位刚度导出 | 构造 | 从 DM.11 的 $J_{\rm eff}(T)$ 与 3D XY 刚度曲线算 $f_s(T)$，而不是外部代入 |
| Q4 | $J_{\rm eff}=J_0f_c$ 是否应写入核心 | 核心层修改 | 需明确授权；先做 R43，避免在数据未判前改 DM.11 |
| Q5 | $\eta$ 的单位标签 | 约定 | 本文只比较数值（与 Shekhter 的 $42\alpha$ 对齐）；单位标签不影响比值物理 |
| Q6 | FGT 稿"清洁 BCS $N_c\to\omega_p^2/8$" | 外部表述 | 需回查 Homes 2005/2006 原文的 $\omega_p$ 口径；暂不当作 $f_c\to1$ 的证据 |

---

## 第十部分：确认/否定台账

**本轮确认**：

1. 三密度恒等式 $f_c=f_Df_s$，以及 Tanner/FGT 读 $f_c$、Homes 读 $f_s$ 的分工。
2. 最优掺杂铜氧 $f_D=0.21$–$0.31$（中心 $0.25$），$f_s=0.80$–$0.95$。
3. M.85′ 的 $\alpha=11.415$ 与 Homes 斜率不相容；其"$0.9\%$ 零参数闭合"是 $f_c/f_s$ 混用。
4. 原 M.85 的 $\alpha=2.854$ 与 $\eta=109$–$120$ 在 $-12\%$ 内相容；但它不是零参数。
5. $\lambda_L=2\lambda_p$ 的因子 $2$ 只在总 f-sum 口径成立；Drude 口径是 $1.06$。
6. Tanner/FGT/迈斯纳不是三次独立确认，而是同一个 $f_c$ 定义的三次读数。
7. Broun §VI 的"Tanner's law"原文：最优掺杂的 Drude 权重相对非相互作用系统重整化约因子 $4$，即 $f_D\approx1/4$。
8. Padilla 2005 在欠掺杂 LSCO/YBCO 测得相干 Drude 分数 $\approx20\%$；这是 R43 所需的 $f_D$ 读数。现有数据已把 $1/4$ 的身份判为 B（A 仅靠 $\Lambda\propto f_s$ 的塌缩存活）。

**本轮否定/降级**：

1. M.85′ 零参数闭合——否定。
2. "1/4 四次独立进入定量结果"——降级为"一个定义 + 一次独立动力学检验"。
3. "$\lambda_L=2\lambda_{p,D}$"——否定；正确是 $2\lambda_{p,\rm tot}$。
4. "清洁 BCS $f_c\to1$"——降为理想极限，待 Q2/Q6 校准。
5. "$1/4$ 确定是凝聚分数"——否定（除非 $\Lambda$ 随 $f_s$ 同步塌缩）；"$1/4$ 确定是 Drude 分数"——现有数据判决为 B（Tanner 总谱重归一 + Broun $f_s\approx0.9$ + Broun "Tanner's law" 因子 $4$ + Padilla 欠掺杂 $f_D\approx0.20$）。核心层仍默认读法 A（不改 DM.11），这是**未授权的保守选择**，不是数据判决；读法 B 的 DM.11 细化 $J_{\rm eff}=J_0(1/4)\Lambda f_s$ 待授权。

**本轮未做**：未改核心文档、未改 Lean、未更新网站、未提交 git、未删除任何文档。

---

**版本**：v0.2（2026-11-17，探索稿；非权威源）。v0.2 增补 Broun §VI 的"Tanner's law"因子 $4$ 与 Padilla 2005 的欠掺杂 $f_D\approx20\%$；Q1 从"待判"推进到"B 自然、A 需 $\Lambda$ 塌缩"。脚本 `10 探索/.calc/stiffness_fraction_audit.py`（`.calc/` 已 gitignore）。外部对照：Broun, arXiv:2502.13351（§VI、表 1）；Padilla et al., *Phys. Rev. B* **72**, 060511(R) (2005), arXiv:cond-mat/0509307；Homes, *Nature* **430**, 539 (2004)；Tanner et al., *Physica B* **244**, 1 (1998)；Tanner et al., *Physica C* **341–348**, 2193 (2000)；Quijada et al., *Phys. Rev. B* **52**, 15485 (1995)；Quijada et al., *Phys. Rev. B* **60**, 14917 (1999)；Shekhter et al., arXiv:2504.02179。全部数值为构造后验数字校验，待第三方复现。
