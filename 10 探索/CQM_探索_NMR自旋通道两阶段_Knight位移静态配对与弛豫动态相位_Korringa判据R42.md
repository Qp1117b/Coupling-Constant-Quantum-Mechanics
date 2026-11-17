# CQM 探索：NMR 自旋通道两阶段——Knight 位移（静态/配对）与弛豫（动态/相位）的 Korringa 判据——R42

> **定位**：探索稿（非权威源），v0.1，2026-11-17，第二十四轮。承接 R40 光学（电荷通道）、R41 约瑟夫森（相位/磁通），本轮首次系统审计 **NMR 自旋通道**——此前 23 轮全部是电荷/相位/热力学量，自旋通道从未触及。
>
> **靶点空白核查**：全库"自旋"字样仅见于 3D XY 自旋波（`超流密度温度曲线`、`曲率阻挫`）与一处质数自旋梯子脚注，**无一处 NMR/Knight/弛豫/相干峰**。而 NMR 恰是唯一同时给出"静态自旋磁化率（Knight 位移）"与"动态自旋谱（$1/T_1$）"的探针，是两阶段"静态配对 vs 动态相位"最干净的天然试验台。
>
> **一句话结论**：NMR 严格二分——静态位移 $K\propto\chi_s(q{=}0)$ 探**配对通道**（单重配对在 $T^*$ 先压制位移）、动态弛豫 $(T_1T)^{-1}\propto\sum_{\bf q}\chi''({\bf q},\omega_L)/\omega_L$ 探**相位通道**（在 $T_c$ 锐变）；两者之比 Korringa 积 $\mathfrak{S}=K^2T_1T/S_0$ 单通道恒为 1，两阶段窗口 $T_c<T<T^*$ 因"静态先行、动态未动"严格给出 $\mathfrak{S}<1$。Hebel–Slichter 相干峰的有/无由 d 波符号零 $\langle{\rm sgn}\Delta\rangle_{FS}=0$（对称 imposed，非拟合）决定，PRX 2024 的"四极有峰/磁无峰"是该符号零的通道投影。新增判据 R42。**绝对超精细常数 $A,B,\gamma_n$ 外生（Z3），本轮只给无量纲结构与时序。**

---

## 第一部分：Korringa 积——静态与动态的两个不同矩（本轮核心结构）

NMR 的两个可观测量来自**同一自旋谱 $\chi''({\bf q},\omega)$ 的两个不同矩**（Scholarpedia Eq.7/10；arXiv:1711.00033 Eq.12/13）：

$$
K \propto \chi'(q{=}0),\qquad
\frac{1}{T_1T}=\frac{2\gamma_n^2k_B}{g^2\mu_B^2}\sum_{\bf q}|A_0|^2\frac{\chi''({\bf q},\nu_L)}{\nu_L},\qquad
K^2T_1T \equiv S_0=\frac{\hbar}{4\pi k_B}\Big(\frac{\gamma_e}{\gamma_n}\Big)^2 \tag{N.1}
$$

三条结构判读：

1. **$K$ 是静态矩**（$\chi'(q{=}0)$，费米面处配对直接现行的量）；**$1/T_1T$ 是动态矩**（$\chi''/\omega$ 的 ${\bf q}$ 求和，含低能相位/节点涨落）。二者探测的是**同一记忆核的不同频率权重**——这正是 CQM 记忆核谱分解（R27–R29）的又一次外部实例。
2. **Korringa 积 $\mathfrak{S}=K^2T_1T/S_0$ 的恒定性是"单通道锁定"的判据**：无关联金属 $\chi''$ 平、$\mathfrak{S}=1$；铁磁涨落 $\chi''$ 集中于 $q{=}0$ 使 $\mathfrak{S}<1$，反铁磁涨落使 $\mathfrak{S}>1$（Moriya 因子，单通道、静态动态同源增强）。
3. **纠错**：Scholarpedia Eq.(10) 写作 $(\hbar/4\pi k_B)(g\mu_B/\gamma_n)^2$，若 $\gamma_n$ 用 rad·s⁻¹·T⁻¹，量纲为 $J^2s^3K$，缺一个 $\hbar^2$；正确标准式是 (N.1) 的比值式 $(\gamma_e/\gamma_n)^2$（脚本 §1 量纲自洽 PASS）。$S_0$ 只依赖核种：脚本算得 $^{63}{\rm Cu}=3.75\times10^{-6}$、$^{17}{\rm O}=1.43\times10^{-5}$、$^{27}{\rm Al}=3.87\times10^{-6}$、$^1{\rm H}=2.63\times10^{-7}$ s·K，量级与 NMR 手册一致。

**两阶段判决**（脚本 §4）：设单重配对在 $T^*$ 起把静态磁化率压制为 $K=g_K K_0$（$g_K<1$），而动态 $1/T_1$ 因相位通道未启动仍处正常态（$T_1T$ 不变）。则

$$
\boxed{\ \mathfrak{S}(T)=\frac{K^2T_1T}{S_0}=g_K(T)^2<1\quad (T_c<T<T^*)\ } \tag{N.2}
$$

这是**零参数严格不等式**：BCS 中 $T^*=T_c$、无中间窗口，$g_K\equiv1$、$\mathfrak{S}=1$；两阶段欠掺中窗口存在，$\mathfrak{S}$ 必然从 $T^*$ 起向下偏离。关键可分性：Moriya-AF 也给 $\mathfrak{S}<1$，但那是**单通道、起始于高温且静态动态同源**；R42 的偏离**起始于 $T^*$、与位移下降同步、且 $T_c$ 处无拐折**（见第二部分 Haase 证据）。判据是时序 + 符号组合，非单看 $\mathfrak{S}$ 数值。

---

## 第二部分：Haase 位移分解的直接证据——"抑制位移但不抑制弛豫"

最新系统 NMR 现象学（Lee & Haase, arXiv:2604.19215，2026-04-21）只用平面 Cu 两个超精细耦合的**对称性**（各向异性 $A_\alpha$ 与各向同性 $B$，$A_\parallel/A_\perp=6$）即可把 Cu 位移分解为两个自旋分量 $\chi_A,\chi_B$，无需已知超精细常数绝对值：

$$
{}^{63}K_\parallel(T)-{}^{63}K_\parallel(0)=-K_{ANI}+K_{ISO},\qquad
{}^{63}K_\perp(T)-{}^{63}K_\perp(0)=\tfrac16 K_{ANI}+K_{ISO} \tag{N.3}
$$

脚本 §2 核验 (N.3) 可逆：$K_{ANI}=\frac67(\Delta K_\perp-\Delta K_\parallel)$、$K_{ISO}=\frac17\Delta K_\parallel+\frac67\Delta K_\perp$（三组随机输入精确回解，PASS）。论文摘要给出决定性陈述：

> "The pseudogap temperature is a measure of the coupling between A and B, **which suppresses the shifts but not nuclear relaxation**."

以及：欠掺有赝能隙的材料，两个自旋分量在 $T_c$ **以上**即随温变化，且折叠图 $\Delta_T\chi_A$ vs $\Delta_T\chi_B$ 的斜率 3（$B\chi_B$ 凝聚快一倍，$=\frac12$ 斜率）**自 $T^*$ 之上开始、穿过 $T_c$ 斜率不变**；而核弛豫在 $T_c$ 处是锐变。

**这几乎就是两阶段框架的 NMR 原文**：

| NMR 可观测量 | 论文实测 | 两阶段归属 | 时序 |
|:---|:---|:---|:---|
| 平面 Cu/O 位移 $K$（$A\chi_A,B\chi_B$） | 赝能隙材料 $T^*$ 以上即降、过 $T_c$ 无斜率拐折 | **配对通道**（静态单重配对先行） | $T^*$ |
| 核弛豫 $1/T_1$ | $T_c$ 处锐变，未被赝能隙"提前抑制" | **相位通道**（动态相干 onset） | $T_c$ |
| 斜率 3 之比 $=1/2$ | 有赝能隙材料普适（$B\chi_B$ 凝聚快一倍） | 无量纲形状数 | 脚本 §2：联合缩放下不变 |

**关于 $1/2$ 的克制判读**：脚本证明斜率比 $1/2$ 在超精细常数联合缩放下不变，属形状层无量纲数（与 Z2/Z3 一致，不依赖 $A,B$ 绝对值）。但**不**把它强行等同于 $1/4=\cos^2(\pi/3)$ 或能隙比——Haase 的 $1/2$ 是两分量凝聚速率比，与 M.83 凝聚分数是不同对象；此处只登记"两个独立自旋分量以 1:2 速率凝聚"这一结构事实，留待后续检验其是否可与 GL 双场/两阶段 $x$ 对接。

---

## 第三部分：Hebel–Slichter 相干峰——d 波符号零的通道投影

常规 s 波 BCS：$1/T_1$ 在 $T_c$ 下方因**态密度堆积 × 相干因子 $1+\Delta^2/E^2$** 出现 Hebel–Slichter 峰（ Scholarpedia；arXiv:1711.00033 §V）。铜氧化物中该峰**从未在磁弛豫观测到**——长期作为 d 波的关键反证。本轮给出对称解释（脚本 §3）：

$$
\langle{\rm sgn}\,\Delta\rangle_{FS}=
\begin{cases}
+1, & s\text{-波（全费米面同号）}\\
0,  & d\text{-波（}\cos2\phi\text{ 正负等权，对称 imposed 零）}
\end{cases} \tag{N.4}
$$

s 波磁通道相干因子 $F_{mag}=+1$（有峰）、四极通道 $F_{quad}=-1$（无峰）；d 波 $F_{mag}=0$（磁峰被对称零压制）。**最硬外部证据**：Li, Mu, Li, Wu, Hu, Xiang, Jiang, Luo, *Phys. Rev. X* **14**, 041072 (2024) 用 $^{63/65}$Cu NQR 分解 YBa$_2$Cu$_4$O$_8$ 的磁弛豫 $1/T_{1M}$ 与四极弛豫 $1/T_{1Q}$——发现 **$1/T_{1Q}$ 在 $T_c$ 下有相干峰、$1/T_{1M}$ 无峰**，并归因于 d 波符号改变能隙使相干因子反转。这是"配对通道对称性指纹"的直接实验：相干峰**从自旋通道迁移到电荷通道**，而两阶段框架早把电荷/相位（R40/R41）与配对分开——此处 NMR 的通道反转与之自洽。

低能幂律同样守约（arXiv:1711.00033；Bohrium d 波条目）：d 波节点线性 DOS 给 $K\propto T$、$(T_1T)^{-1}\propto T^2$（即 $1/T_1\propto T^3$），s 波给指数衰减——R36 已处理 $d$ 波分支，本轮不重复拟合。

---

## 第四部分：R42 判据（与 R29–R41 测不同对象，互相独立）

- **R42a（静态/动态时序分裂）**：定义 $T_K$ = 位移 $K$ 开始下降温度、$T_{1}$ = 弛豫锐变温度。BCS/过掺 $T_K\simeq T_c$（单斜率 2、无 $T^*$ 前驱）；欠掺 $T_K\simeq T^*>T_c$、$K$ 过 $T_c$ 无拐折而 $1/T_1$ 锐变。分离比 $T_K/T_{1}\simeq 1+x$。
- **R42b（Korringa 偏离符号与起点）**：单通道 $\mathfrak{S}=1$ 或 Moriya-AF $\mathfrak{S}>1$；两阶段窗口 $\mathfrak{S}=g_K^2<1$，**起点在 $T^*$ 且随位移下降、$T_c$ 无拐折**。三者可由"符号 + 起点 + 拐折"三分，非单看数值。
- **R42c（相干峰通道反转）**：s 波磁 $1/T_1$ 有 HS 峰、四极无；d 波（符号零）磁无峰、四极可有峰（PRX 2024 已观测）。这是配对通道对称性的判据，与 $T_c$ 精确值无关。

---

## 第五部分：退化与边界（诚实交代）

**退化守住**：BCS（$x\to0$，$T^*=T_c$，$\mathfrak{S}=1$，磁 HS 峰归位、$K\propto\chi_s\to0$ 单重证实）、迈斯纳/GL$\kappa$/Hc/FGT/Josephson（本轮只加自旋通道，不动电荷/相位结论）、M.83（$1/4$ 未被 NMR 改写）、Z1/Z2/Z3（绝对 $A,B,\gamma_n,S_0$ 外生，只给比值/时序）。零拟合。

**边界**：（i）Haase 的两分量 $\chi_A/\chi_B$ 是唯象分解，**本框架不宣称微观推导出 $A_\parallel/A_\perp=6$ 或斜率 $1/2$**，只登记其为形状层输入；（ii）$\mathfrak{S}<1$ 与 Moriya-AF 简并，必须靠"起点 $T^*$"区分——若某材料 AF 涨落恰也在 $T^*$ 增强，R42b 单判据失效，需并测 $K(T)$ 与 $\chi''(q)$ 空间分布；（iii）PRX 四极峰目前仅 YBa$_2$Cu$_4$O$_8$ 一例，R42c 的普适性待跨材料重复；（iv）NMR 不直接给绝对 $T_c$、$\Delta$、$\lambda_L$，与 Z2/Z3 一致。以上均不强行套参数。

---

## 文献与出处

| 编号 | 出处 | 用途 |
|:---|:---|:---|
| N1 | Scholarpedia, "NMR studies of electronic properties of solids", DOI:10.4249/scholarpedia.32069 | (N.1) 静态/动态两矩、Korringa、HS 峰；并载有量纲待纠的 Eq.(10) |
| N2 | arXiv:1711.00033 (Chaboussant et al., NMR in High Magnetic Field) | FDT 式 (12)、Korringa 正确式 (13)、$\mathfrak{S}$ 的铁磁/反铁磁方向、d 波幂律 |
| N3 | Lee & Haase, arXiv:2604.19215 (2026-04-21), "Pseudogap and Condensation in Cuprate Superconductors from NMR Shifts" | (N.3) 分解、$A_\parallel/A_\perp=6$、斜率 1/2、"suppresses shifts but not relaxation" |
| N4 | Li, Mu, Li, Wu, Hu, Xiang, Jiang, Luo, Phys. Rev. X **14**, 041072 (2024), DOI:10.1103/PhysRevX.14.041072 | YBa$_2$Cu$_4$O$_8$ 四极峰/磁无峰、d 波符号反转 |
| N5 | arXiv:cond-mat/9307047, "What Does The Korringa Ratio Measure?" | $\mathfrak{S}$ 非简单 $\chi^2$、扩散修正；支撑"偏离需谨慎归因"边界 (ii) |

脚本：`.calc/nmr_spin_two_stage_audit.py`（§1–§5 全 PASS，零拟合；CODATA/SI 第一性常数 + 对称恒等式 + KK 数值积分）。
