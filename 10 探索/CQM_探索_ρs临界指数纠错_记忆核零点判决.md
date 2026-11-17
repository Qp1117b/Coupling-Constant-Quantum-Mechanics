# CQM 探索：ρ_s 临界指数纠错、Regge 三角网格淬火、记忆核—黎曼零点判决

> **定位**：探索稿（非权威源），v0.1，2026-11-17。本轮做三件可判决的事，回应此前曲率阻挫退火判据（顶点角亏主题探索稿，已删）留下的两个硬问题，并对 `CQM_探索_跃迁谱配分函数_黎曼零点_质数震荡_记忆核_相变通道.md`（下称《通道》）的黎曼零点物理身份给出最终判决。
>
> **范式**：关系性范式；不引入电子自由度；不改 `01–08`、`归档/` 的任何定义与数值。两处**纠错**只针对 `10 探索/` 内的错误陈述。
>
> **克制拟合声明**：本文全部数值输入只有外部已发表常数（ν=0.6717、γ_n 前 8 项）与框架内代数（回路宇称、量纲分析）。没有可调参数，没有最小二乘。凡属"相容"处一律标注，不冒充验证。
>
> **【续篇 2026-11-17 · §1.4 真问题已处理】**：§1.4 登记的"整段 $\rho_s(T)$ 通道"见 `CQM_探索_超流密度温度曲线_相位涨落两机制.md`——结论：$\rho_s\npropto\Delta\varepsilon^p$（配对通道，低温给平台，已判决排除）；正确通道是 3D XY 相位涨落，给出零参数低温斜率 −0.367（=−2.2017/6），落在实验区间 [−0.55,−0.30]；连续标度函数零参数 RMSE=0.021；低温线性不需 d 波节点（Roddick–Stroud / Emery–Kivelson）。本文 §1 的指数纠错不受影响。

---

## 第一部分：$\rho_s$ 临界指数纠错——"34% 张力"是伪命题

### §1.1 错误陈述与其来源

上一轮文档第九部分 (ii) 写：

$$\Upsilon\propto(1-t)^{2\nu},\quad \nu=0.6717\ \Rightarrow\ \text{指数 }1.343,\quad\text{vs 实验近线性}\approx1,\ \text{差 }34\%.$$

**这是把磁化率指数 $\gamma=2\nu\approx1.34$ 误当成超流密度（helicity modulus）指数。**

### §1.2 权威基线（三源一致）

| 来源 | 陈述 |
|:---|:---|
| Shenoy, *Phys. Rev. B* **40**, 5056 (1989), DOI:10.1103/PhysRevB.40.5056 | "exponents for the helicity modulus $\rho_s\approx\|\epsilon\|^{\nu}$, … magnetic field response $\gamma=2\nu$"；给 $\nu=0.67$、$\gamma=1.34$、$\alpha=-0.015$ |
| Marchetti & Bighin, arXiv:1602.08936 §6 / arXiv:1607.03801（*J. Supercond. Nov. Magn.* **30**, 721 (2017), DOI:10.1007/s10948-016-3633-9） | "the superfluid density has … the critical exponent at $T_c$ is $2/3$, putting it in the 3D XY universality class, while a linear $T$-dependence at low temperature…" |
| Thermography of superfluid transition, *Science* (2022), DOI:10.1126/science.adg3430 | 3D XY：$\rho_S\propto(T_c-T)^{\nu}$、$\nu\approx0.672$（与 $^4$He 同普适类） |

### §1.3 正确对照

$$\boxed{\ \rho_s(T)\ \propto\ |1-T/T_c|^{\nu},\qquad \nu=0.6717\ (\approx 2/3).\ }$$

- **临界区**（$T\to T_c^-$）：指数 $\nu\approx0.67$——3D XY，实验（YBCO/LSCO/Hg-1201 归一化曲线）确认。
- **低温区**（$T\to0$）：$\rho_s(0)-\rho_s(T)\propto T$，指数 $\approx1$——d 波节点准粒子（BCS 侧），**不是同一温区**。
- $1.34=2\nu$ 是**磁化率** $\chi$ 的临界指数，与 $\rho_s$ 无关。

**判决**：三个数 $0.67$ / $1$ / $1.34$ 分属不同物理量或不同温区，本来就不该相等。"差 34% 超出拟合误差"是把 $2\nu$ 张冠李戴给 $\rho_s$ 后 manufactured 出来的伪张力，**撤销**。上一轮文档第九部分 (ii) 已就地更正（加【已纠正】标记并指向本文）。

### §1.4 真正可证伪的问题（替代）

伪张力撤销后，剩下的真问题是：**CQM 的退火图 $\rho_s(T)$ 在从 $T=0$ 到 $T_c$ 的整段，是否复现 3D XY 的普适标度函数？** 该函数已经同时含低温线性段与临界 $\nu$ 段（Marchetti–Bighin 用 $\Theta(T)\approx T$ 的线性映射把整段拉成单一 3D XY 曲线）。

- 若 CQM 只给单一幂律（无论指数 0.67 还是 1），则与"整段普适曲线"不符 → 退火图需要温度依赖的有效刚度，而非常数 $J_{\rm eff}=J_0/4$。
- 这直接连到 M.86 的记忆核形状-标度分离 $K(t)=K(0)\Phi(t/\tau)$，$\tau=\alpha\hbar/k_BT$：**刚度随 $T$ 变**是框架内已有的机制，不是新假设。
- 【缺口】$\Phi$ 的具体形式未从 CQM 推出，故这一检验目前只能证伪"常数 $J_{\rm eff}$"的粗糙版本，不能证伪退火图本身。登记为开放项，不冒充闭合。

---

## 第二部分：Regge 三角网格的淬火基态——全阻挫，与方格 3/4 根本不同

### §2.1 模型与回路宇称定理（回顾）

DM.9 字面：$J_{ij}=\cos(\delta_i+\delta_j)$，$\delta_i=\pm\pi/3$。令 $t_i=\mathrm{sign}\,\delta_i\in\{\pm1\}$，则

$$J_{ij}=\tfrac14-\tfrac34\,t_it_j\ \in\ \Big\{+1\ (t_it_j=-1),\ -\tfrac12\ (t_it_j=+1)\Big\},\qquad \mathrm{sign}\,J_{ij}=-t_it_j.$$

绕 $L$ 边形回路的符号积：

$$\prod_{\rm loop}\mathrm{sign}\,J_{ij}=(-1)^L\prod_i t_i^2=(-1)^L.$$

- **偶数回路**（方格）：符号积 $+1$，无阻挫 → 淬火只损失幅度，$\Upsilon=3/4$（上一轮数值）。
- **奇数回路**（三角）：符号积 $-1$，每个面带 $\pi$ 通量 → **全阻挫**。CQM 的 Regge 网格是三角剖分（5/7 度顶点），故真实拓扑属后者。

### §2.2 三角网格数值（本轮新算）

实现：二维三角晶格（基矢 $a_1=(1,0)$、$a_2=(1/2,\sqrt3/2)$，三正键方向），$J_{ij}$ 如上；$T=0$ 阻尼梯度极小化 + Hessian 精确扭转刚度 $\Upsilon=d^2E_{\rm gs}/d\phi^2-H_{\phi\theta}H^+_{\theta\theta}H_{\theta\phi}$；手性序 $\chi=\frac{2}{3\sqrt3}\sum_\triangle\sin(\theta_j-\theta_i)$。脚本 `10 探索/.calc/xy_tri.py`（已 gitignore，参数见附录）。

标定：$\Upsilon_{\rm clean}=1.00000$，$\Upsilon_{\rm anneal}(J=1/4)=0.25000$（均到 5 位）。

| $L$ | 模式 | $\Upsilon$ | $E_{\rm gs}/{\rm bond}$ | $\langle\|\chi\|\rangle$ |
|:---:|:---|:---|:---|:---|
| 4 | 淬火 | $-0.68\pm0.36$（中位 $-0.74$） | $-0.372$ | 0.129 |
| 6 | 淬火 | $+0.20\pm0.06$ | $-0.403$ | 0.347 |
| 4 | 对照 $\pm1$ 随机符号 | $0.05\pm0.44$ | $-0.582$ | 0.306 |
| 4/6 | 退火 | $0.250$ | $-0.250$ | 0 |

**读法（克制）**：淬火在三角剖分上**没有干净的铁磁刚度**——$\Upsilon$ 在 0 附近漂移甚至为负，手性序随尺寸增大（0.13→0.35），是全阻挫手性玻璃的特征。这与方格的 $3/4$ 是**定性不同**的相。

**边界（重要，防止过度解读）**：
1. 均匀 FFXY（每 plaquette $\pi$ 磁通、$|J|$ 相等）在蜂窝晶格上 $T=0$ helicity modulus **有限**（$\approx J/2$），见 Kalz & Honecker, arXiv:1112.3723 —— 故"全阻挫⇒刚度必为零"**不成立**。本模型 $|J|\in\{1,1/2\}$ 非均匀，且梯度下降在高度简并的基态流形上未必收敛到全局极小（Hessian 零模存在，$\min$ 本征值 $\sim10^{-15}$ 是 Goldstone 模，未排除其他鞍点）。故本文只主张"淬火无**唯一、干净**的铁磁刚度值"，不主张"刚度严格为零"。
2. 因此 R18 的措辞收紧为：**在 Regge 三角网格上，"冻结曲率⇒$\eta$ 上移 3 倍"的方格推导不适用**；冻结曲率在某系综平均下 $\Upsilon$ 被强烈压制（趋向 0 或更小），方向仍是"上移"，但倍数不是普适的 3，依赖冻结的具体构型与有限尺寸。

### §2.3 对 M.87 的加强

上一轮结论"1/4 只能读作退火平均"在方格上靠"淬火给 3/4 ≠ 1/4"。本轮在 CQM 真实的三角剖分上得到更强结论：**淬火根本给不出稳定的 1/4（在 0 附近）**，故退火读法不是"两个候选值里选一个"，而是"唯一能给出 Tanner 观测值 $n_s/n=1/4$ 的读法"。曲率量子在相位动力学尺度内涨落（核心文档 §6 声子＝Regge 曲率量子）是硬要求。

---

## 第三部分：记忆核—黎曼零点判决——形状指纹，不产生能标

### §3.1 《通道》的 R1 判据回顾

《通道》主张：记忆核数论分量在 $t_n=\gamma_n/(2\omega_0)$ 有零点/极小序列，GUE 型间距；定标 $\omega_0=k_BT_c/(4\hbar)$（M.18，临界线）或 $k_B\theta_D/\hbar$（Debye）。另附 Sierra 的 Berry–Keating ↔ Russian doll BCS 先例。

### §3.2 量纲判决（严格）

$\gamma_n$ 是 $\zeta$ 非平凡零点的虚部，**无量纲纯数**（前 8 项 14.1347, …, 43.3271）。$t_n$ 的量纲**完全**来自 $\omega_0$：

$$t_n=\frac{\gamma_n}{2\omega_0}\ \Longrightarrow\ \frac{t_n}{t_1}=\frac{\gamma_n}{\gamma_1}\ \ (\text{与 }\omega_0\text{ 无关}),\qquad t_1=\frac{\gamma_1}{2\omega_0}\ \ (\text{全由 }\omega_0\text{ 定}).$$

- 零点提供的**只有无量纲比值** $\gamma_n/\gamma_1=\{1,\ 1.487,\ 1.770,\ 2.153,\ 2.330,\ 2.659,\ 2.895,\ 3.065\}$（GUE 排斥 fingerprint）。
- 时间**标度** $t_1$ 由 $\omega_0$ 决定，而 $\omega_0\propto T_c$（M.18）或 $\propto\theta_D$——两者都是**外部热学/声子标度**，不是从 $\zeta$ 内部产生的。

**这正是命题 Z**（$\zeta$ 通道标度无关）的直接实例：零点能给出"指纹形状"（比值、间距统计），不能给出"绝对时刻"。R1 的可观测量 $\Delta t_n=t_n-t_{n+1}$ 绝对值随材料按 $\omega_0^{-1}$ 缩放，跨材料**不普适**；只有 $t_n/t_1$ 普适。故《通道》§10.4 宣称"从飞秒推到可测窗口"的升级，本质是**借外部 $T_c$ 换标度**，不是零点自己给出时间。

**核对（无数值错误）**：Debye 定标 Al（$\theta_D$，$\omega_0=k_B\theta_D/\hbar$）给 $t_1\approx126$ fs 量级；临界线定标（$\omega_0=k_BT_c/4\hbar=3.85\times10^{10}$ rad/s）给 $t_1=0.184$ ns——两处公式不同、自洽，文档没有算错，只是把外部标度换了一次。

### §3.3 外部先例的判决

Sierra 的 Russian doll BCS 模型与 Berry–Keating $H=xp$ 的映射（arXiv:math-ph/0702034v2 自述）明确承认：
- "**Up to date, it is not known a Hamiltonian accomplishing the Hilbert–Pólya conjecture.**"
- 该映射只 reproduce 零点计数的**光滑部分**（$\frac{E}{2\pi}\log\frac{E}{2\pi e}$），"a point like spectrum associated to the Riemann zeros was completely absent in this quantization"。
- GUE 统计（Montgomery–Odlyzko）是**零点间距**的性质，属"形状/统计"通道；它不提供任何物理哈密顿量的本征能标。

**判决**：外部文献支持"零点↔谱统计/GUE 形状"的联系，但**没有任何先例**支持"零点虚部直接给出一个超导体的可观测激发频率或 $T_c$". CQM《通道》的黎曼零点成分据此**最终归类为形状通道**（与 $c_n$ 七带闭环、GUE 形状同级）：它是记忆核时间结构的指纹假设，$t_n$ 的绝对值寄生于外部 $\omega_0$。**不升级为 $T_c$ 机制，不宣称验证。**

### §3.4 可证伪判据（收紧后的 R1′）

原 R1 的"绝对时刻"不可证伪（因 $\omega_0$ 可调吸收）。收紧为**无量纲、跨材料普适**的形式：

$$\mathbf{R1'}:\quad \text{记忆核自相关的极小时刻比值 } \frac{t_n}{t_1}\stackrel{?}{=}\frac{\gamma_n}{\gamma_1}=\{1.487,\,1.770,\,2.153,\,2.330,\,2.659,\,2.895,\,3.065\},\quad \text{且小间距比例}\sim8\%\ (\mathrm{GUE}).$$

- 若观测到等间距声子拍频（比值呈小整数）→ 数论分量否定。
- 若比值普适但间距统计为 Cramér 型（小间距比例 $\sim34\%$）→ 走质数模式通道而非零点通道（《通道》§12 判据）。
- 两判据都只用无量纲量，不含可吸收的标度参数——这是与旧 R1 的关键差别。
- 【状态】构造判据，待实验；本文不提供数据拟合。

---

## 第四部分：本轮结论清单

| # | 结论 | 状态 |
|:--|:---|:---|
| 1 | $\rho_s$ 临界指数是 $\nu\approx0.67$，不是 $2\nu=1.34$；"34% 张力"撤销 | **纠错，确定**【严格：三源文献一致】 |
| 2 | 真问题是"整段 $\rho_s(T)$ 是否复现 3D XY 普适标度函数"，常数 $J_{\rm eff}$ 粗糙版本可证伪 | 开放判据 |
| 3 | 回路宇称：$\prod\mathrm{sign}J=(-1)^L$；方格无阻挫、三角全阻挫 | **严格代数** |
| 4 | 三角网格淬火无干净铁磁刚度、手性序随尺寸增；退火精确 1/4 | 数值【边界：基态简并，定性判据】 |
| 5 | M.87 加强：退火是给出 $n_s/n=1/4$ 的唯一读法 | 条件严格（依赖 4） |
| 6 | 零点 $\gamma_n$ 无量纲，$t_n$ 标度全由外部 $\omega_0$ 定→零点只给形状指纹 | **判决，严格量纲分析** |
| 7 | 外部 Hilbert–Pólya 未解，无零点→$T_c$/可观测能标的先例 | 外部对照 |
| 8 | 黎曼零点成分最终归为形状通道；R1 收紧为无量纲 R1′ | 判决 |
| 9 | 迈斯纳/BCS 退化不受本轮影响（$1/4$ 退火读法、$J_{\rm eff}=J_0/4$ 保持） | 未改动 |

---

## 附录：数值与外部文献记录

- 指数：$\nu=0.6717$、$\gamma=2\nu=1.3434$；错误的旧陈述指数 1.343 实为 $\gamma$。
- 三角网格脚本 `10 探索/.calc/xy_tri.py`：三键方向 $\{(1,0),(0,1),(-1,1)\}$；$J_{ij}=0.25-0.75\,t_it_j$；阻尼梯度下降 steps=4000、restarts=8；Hessian 用 `pinv(rcond=1e-8)` 去 Goldstone 零模；手性 $\chi=\frac{2}{3\sqrt3}\sum_\triangle\sin(\theta_j-\theta_i)$。构造后验数字校验，待独立复现。
- 零点前 8 项虚部与 $\gamma_n/\gamma_1$ 比值见 §3.2；t 标度：临界线定标 $\omega_0=k_BT_c/(4\hbar)=3.27\times10^{10}T_c$ rad/s；Al 1.175 K → $3.85\times10^{10}$ rad/s（6.1 GHz）、$t_1=0.184$ ns；Debye 定标 $\omega_0=k_B\theta_D/\hbar$ → Al $t_1\sim126$ fs。
- 外部文献：
  - LH-EX1 Shenoy, PRB **40**, 5056 (1989), DOI:10.1103/PhysRevB.40.5056（3D XY 涡环标度，$\rho_s\sim|\epsilon|^\nu$）
  - LH-EX2 Marchetti & Bighin, arXiv:1602.08936 / 1607.03801, DOI:10.1007/s10948-016-3633-9（铜氧化物 $\rho_s$：临界 2/3 + 低温线性；Uemura）
  - LH-EX3 *Science* (2022), DOI:10.1126/science.adg3430（unitary Fermi gas 3D XY，$\rho_S\sim(T_c-T)^\nu$）
  - LH-EX4 Kalz & Honecker, arXiv:1112.3723（蜂窝 FFXY 基态与有限 $\Gamma(0)\approx J/2$，三个相变）
  - LH-EX5 Sierra, arXiv:math-ph/0702034v2 + 报告 pg.infn.it/StatPhys23pgsatellite/talks/sierra.pdf（Berry–Keating↔Russian doll BCS；明言 Hilbert–Pólya 未解、只给光滑计数）
  - LH-EX6 超对称 QM 谱嵌入猜想（ScienceDirect S3050475925008978）：零点为稀疏嵌入子谱，非完整谱——进一步说明零点"谱"无普适物理能标。
