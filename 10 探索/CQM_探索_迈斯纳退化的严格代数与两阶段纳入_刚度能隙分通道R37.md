# CQM 探索：迈斯纳退化的严格代数、两阶段纳入与"刚度/能隙分通道"——R37

> **⚠ 归一化纠错（2026-11-17，最先读）**：本稿 §2.1 与 R37c 的 $\lambda_L/\lambda_p$ 未区分**总 f-sum** 与 **Drude** 口径。$\lambda_L=2\lambda_p/\sqrt{\Lambda}$ 的因子 $2$ 只在总 f-sum 口径成立：$\lambda_L/\lambda_{p,\rm tot}=1/\sqrt{f_c}=1/\sqrt{f_Df_s}=2.0$–$2.24$（最优掺杂铜氧）。若用 Drude 口径，$\lambda_L/\lambda_{p,D}=1/\sqrt{f_s}=1.03$–$1.12$，不是 $2$。故 R37c 应重述为："总 f-sum 口径测得 $\lambda_L/\lambda_{p,\rm tot}<2$ 才质疑 $f_c$；Drude 口径测得 $\lambda_L/\lambda_{p,D}\approx1$ 只说明 $f_s\approx1$，与 $f_c$ 无关。"本稿"$\lambda_L=2\lambda_p$ 受 Drude vs 全带 $4$–$5$ 倍口径限制"的表述方向反了：因子 $2$ 恰恰要求全带 f-sum。详见 `10 探索/CQM_探索_1over4归一化审计_凝聚分数与Drude分数二读_M85prime证伪与判决实验.md`。另按审计 §2.4–§2.5，$1/4$ 的身份现有数据判读法 B（$1/4=f_D$）；若采 B，本稿 $\lambda_L=2\lambda_p/\sqrt{\Lambda}$ 须读作 $\lambda_L=2\lambda_{p,\rm tot}/\sqrt{\Lambda f_s}$（$\Lambda\to\Lambda f_s$），欠掺杂曲线多一个 $1/\sqrt{f_s}$；因子 $2$ 的代数与总 f-sum 口径结论不变。本稿"刚度/能隙分通道"与 $\lambda_L(T)$ 曲线结论不变。
>
> **第二十一轮 κ/临界场指针（2026-11-17，见 `CQM_探索_GL参数kappa两阶段分支_临界场双尺度与GL关系适用域R39.md`）**：本稿把迈斯纳刚度归入相位通道（$\lambda$ 读刚度）；下轮处理 $\kappa=\lambda/\xi$——发现 GL 恒等式 $H_{c2}=\sqrt2\kappa H_c$ 隐含 $\lambda,\xi$ 同源（同一 $m^*$），故在过掺配对支成立、欠掺相位支破缺；$\kappa$ 非常数、随 $x=T^*/T_c-1$ 增大（欠掺 $\kappa\sim100$ 极端 II 类指纹），$H_{c2}$ 分裂为配对场 $H^*\propto T^{*2}$ 与相位场 $H^\theta\propto T_c$（Grissonnanche 2014 双场实验证实）。本稿的 $\lambda_L=2\lambda_p/\sqrt\Lambda$ 与"刚度/能隙反向"结论不变，新增 R39。
>
> **第二十轮 Hc 指针（2026-11-17，见 `CQM_探索_热力学临界场Hc的斜率判决_凝聚能分通道与Hc反演半循环出口.md`）**：本稿的 GL 关系 $H_c=\Phi_0/(2\sqrt2\pi\lambda_L\xi)$ 在下轮被用作迈斯纳边界；下轮由严格热力学 $\Delta C=T_c\mu_0(H_c')^2$ 把"比热无跳变"翻译成"$H_c$ 在 $T_c$ 零斜率"，并把凝聚能 $U=H_c^2/2\mu_0$ 归入相位通道（与能隙比对 $x=T^*/T_c-1$ 反向）——与本稿"刚度/能隙分通道"同构，新增判据 R38。本稿结论不变。
>
> **定位**：探索稿（非权威源），v0.1，2026-11-17，第十九轮。承接第十八轮《能隙比的 d 波分支修正》与第十轮《凝聚分数、普朗克耗散与 Homes 定律》，正面兑现用户每轮强调却十八轮未 constructive 完成的承诺——**"确保退化成迈斯纳效应"**。
>
> **一句话结论**：迈斯纳退化链 $\lambda_L=2\lambda_p/\sqrt{\Lambda}$ 经 SI 第一性验证**代数严格**，因子 $2$ 正是 M.83 凝聚分数 $1/4$ 的平方根倒数；外部三重证据（Fernandes/Oreg/Th-Gd 实验）确认迈斯纳由**相位刚度 $n_s$** 而非能隙 $\Delta$ 决定，与 CQM 两阶段逐字同构。据此把迈斯纳刚度正式纳入两阶段，得到一个 constructive 精确化与一条实质张力：**迈斯纳刚度 $\propto1/(1+x)$ 与能隙比 $\propto(1+x)$ 对同一 $x=T^*/T_c-1$ 方向相反**——第十八轮"三观测量统一"必须精确化为"同一控制量、分通道反向读出"，不可宣称同向塌缩。新增可证伪判据 R37。**绝对 $\lambda_L$ 仍外生 $m^*,e$（Z2/Z3 不变，本轮只给无量纲比）。**

---

## 第零部分：本轮要解决的问题

用户长期要求："建立模型…解释预言超导现象数据，并且**确保退化成 BCS 和迈斯纳效应**。"

十八轮盘点：BCS 侧做了同位素（M.93）、能隙比（DM.14′）、比热（M.96）、$\rho_s$（M.88/89）等多轮；**迈斯纳侧只有第十轮表格第 8 行一句条件预言** $\lambda_L=2\lambda_p/\sqrt{\Lambda}$（标【构造】，未列主判据），从未做代数严格性审计、从未与两阶段结构缝合。这是承诺缺口。本轮补三件事：

1. 迈斯纳退化链的**第一性代数审计**（$\mu_0\varepsilon_0c^2=1$ 单位链 + 凝聚分数来源）；
2. 迈斯纳刚度的**相位通道归属**（外部文献三重证据 + CQM 两阶段对齐）；
3. 把迈斯纳入 $x=T^*/T_c-1$ 统一图像，检验它与第十八轮能隙比/比热/$\rho_s$ 的方向一致性——**结果发现方向相反**，据此精确化第十八轮并立 R37。

---

## 第一部分：迈斯纳退化链的代数严格性（验证，非纠错）

### §1.1 SI 第一性单位链

London（SI）与 Drude 等离子体频率：

$$\lambda_L^{-2}=\mu_0\,\frac{n_s e^2}{m^*},\qquad \omega_p^2=\frac{n e^2}{\varepsilon_0 m^*},\qquad \lambda_p\equiv\frac{c}{\omega_p}.\tag{1}$$

两式相除，注意 $\mu_0\varepsilon_0c^2=1$（数值验证 $0.999999999456$，仅浮点舍入）：

$$\frac{\lambda_L^{-2}}{\lambda_p^{-2}}=\mu_0\varepsilon_0c^2\cdot\frac{n_s}{n}=\frac{n_s}{n}\quad\Longrightarrow\quad \lambda_L=\frac{\lambda_p}{\sqrt{n_s/n}}.\tag{2}$$

代入 M.83′（Homes 稿式 M.83′，L114/L333；$\Lambda(P)\le1$ 为 M.70 簇化压制因子）：

$$\frac{n_s}{n}=\frac{1}{4}\Lambda(P)\quad\Longrightarrow\quad \boxed{\lambda_L=\frac{2\lambda_p}{\sqrt{\Lambda}}.} \tag{3}$$

数值核验（脚本 `meissner_two_stage_audit.py` §1）：$\Lambda=1/0.8/0.5/0.1\Rightarrow n_s/n=0.25/0.20/0.125/0.025$，$\lambda_L/\lambda_p=2.000/2.236/2.828/6.325=2/\sqrt\Lambda$ 全 match。

**判定**：第十轮第 254 行 $\lambda_L=2\lambda_p/\sqrt{\Lambda}$ **代数正确**，因子 $2=1/\sqrt{1/4}$ 严格来自 M.83 凝聚分数——这是凝聚分数 $1/4$ 第二次（继 Homes 斜率 $8\pi$ 后）进入一个零参数结果。$\Lambda=1$ 的锐利形式 $\lambda_L=2\lambda_p$ 保持为条件预言（仍受 $\omega_p$ 取 Drude 权重 vs 全带 $f$-和差 4–5 倍的口径限制，LH7）。

> **勘误（本地登记）**：Homes 稿 L243 表格第 1 行写 "$n_s/n=\cos^2(\pi/3)/\Lambda$"（$\Lambda$ 在分母），与正文 L114/L250/L254/L333 一致使用的 $n_s/n=\tfrac14\Lambda$（$\Lambda$ 在分子、簇化压制）矛盾。正文四处为准，表格为笔误。已在《Homes 稿》加指针，未改原文。

### §1.2 退化到 BCS 的一致性

配对限制支（干净 BCS）$n_s/n\to1$，M.83 的 $1/4$ 不进 $T_c$（Homes 稿表格第 9 行已登记）。此时 $\lambda_L=\lambda_p/\sqrt1=\lambda_p$，即回到 Drude 等离子体波长——**与常规超导 London 极限一致**。注意 $\Lambda\to4$ 不是这条退化路径（$\Lambda\le1$ 是簇化压制因子，干净 BCS 无簇化，不走 M.83′）。BCS 退化守住。

---

## 第二部分：迈斯纳刚度的相位通道归属（外部三重证据）

### §2.1 Anderson–Higgs 链

相位刚度自由能（Fernandes 讲义式 117；Oreg 讲义式 21）经积分掉 Goldstone 相位得规范场有效作用量：

$$\mathcal F\propto\sum_{\mathbf q}\bigl(\lambda^{-2}+q^2\bigr)\mathbf A_\perp(\mathbf q)\mathbf A_\perp(-\mathbf q),\qquad \lambda^{-2}\propto n_s.\tag{4}$$

取 curl 得 $(\lambda^{-2}-\nabla^2)\mathbf B=0\Rightarrow \mathbf B(x)=B_0e^{-x/\lambda_L}$（London 第一方程 + 迈斯纳指数衰减）；光子获质量 $m_\gamma=\hbar/(\lambda_Lc)$。关键：**质量项 $\propto n_s$（rigidity），不是能隙 $\Delta$**。

### §2.2 三重外部证据（迈斯纳 ⟂ 能隙）

| 编号 | 出处 | 关键结论 | 对本轮的作用 |
|:---|:---|:---|:---|
| M1 | Fernandes, *Lectures on BCS*, 式(117)(118) | "rigidity $n_s$ … is the key property responsible for the Meissner effect, and **not** the gap function $\Delta$—gapless superconductors still display Meissner" | 直接判决：刚度而非能隙 |
| M2 | Oreg, *Concepts of CM Physics* §6.3, 式(21)(22) | $(\rho_0/m-\nabla^2)A_\perp=0$，$\lambda=\sqrt{mc^2/4\pi n_se^2}$；Anderson–Higgs 四步 | 标准推导链 |
| M3 | W. R. Decker & D. K. Finnemore, *Phys. Rev.* **172**, 430–436 (1968), DOI:10.1103/PhysRev.172.430 | Th 与 Th-Gd 磁性杂质合金，**gapless 后 "all show a Meissner effect"**，Abrikosov–Gor'kov 理论拟合到 0.5% | 硬实验证据：无能隙仍有迈斯纳 |

（M3′：另见 arXiv:2609.02263 反铁磁超导 anisotropic gapless → paramagnetic Meissner；IOP New J. Phys. 15 023023 gapless superfluid phase——均确认 gap 与 Meissner 可解耦。）

### §2.3 与 CQM 两阶段的逐字对齐

两阶段稿式 TP.24（相位限制支）：

$$k_BT_c\propto J_{\rm eff}\propto\frac{\hbar^2 n_s d}{m^*}\quad\Longleftrightarrow\quad \lambda_L^{-2}=\mu_0e^2\frac{n_s}{m^*}.\tag{5}$$

Uemura 关系 $T_c\propto n_s/m^*\propto\lambda_L^{-2}$（欠掺，L5 Uemura 1989；L4 Emery–Kivelson 1995）与迈斯纳刚度**同源**——都读阶段二相位通道。而配对通道（$T^*$、能隙 $\Delta$）在欠掺很高却被"刚度不足"卡住 $T_c$（Bohrium 讲义"stiffness-limited vs pairing-limited"）——这正是 DM.13 $T_c=\min(T^*,T_\theta)$ 的物理内容。

**判定**：迈斯纳刚度正式归属**相位通道**，与能隙比（配对通道）分属两支。这就是本轮最关键的 constructive 结构。

---

## 第三部分：迈斯纳纳入 $x$ 统一——精确化第十八轮 + 实质张力

### §3.1 两个通道对 $x=T^*/T_c-1$ 的相反依赖

第十八轮 DM.14′：能隙比 $=r_d(T^*/T_c)=r_d(1+x)$，$r_d=4.279$，**随 $x$ 单调增大**（欠掺 $T^*>T_c\Rightarrow x>0$）。

迈斯纳刚度（相位限制支）：$k_BT_c\propto\lambda_L^{-2}$（欠掺 Uemura）。设欠掺配对标度 $T^*$ 近似掺杂无关（赝能隙在欠掺区较平，LNW/Božović 图像），则

$$\lambda_L^{-2}(0)\propto T_c=\frac{T^*}{1+x}\ \propto\ \frac{1}{1+x},\tag{6}$$

**随 $x$ 单调减小**。数值（脚本 §3，$r_d=4.27937$）：

| $x$ | 0 | 0.25 | 0.5 | 1.0 | 2.0 | 3.0 |
|:---|:---|:---|:---|:---|:---|:---|
| 能隙比 $r_d(1+x)$ | 4.28 | 5.35 | 6.42 | 8.56 | 12.84 | 17.12 |
| 迈斯纳刚度 $\propto1/(1+x)$ | 1.000 | 0.800 | 0.667 | 0.500 | 0.333 | 0.250 |

**方向相反**：同一 $x$，能隙比涨、迈斯纳刚度跌。这与实验定性一致——欠掺区能隙比 $2\Delta/k_BT_c$ 暴涨（汞系 7.9/9.5/13，EG5/EG6），同时 Uemura 超流密度 $\lambda_L^{-2}$ 线性下降（Božović 2016 $T_c=\gamma\sqrt{\rho_s}$）。

### §3.2 对第十八轮"三观测量统一"的精确化（实质纠错）

第十八轮称能隙比、比热、$\rho_s$ 均由唯一 $x$ 控制、"一处结构的三投影"。本轮发现这句话**内部已含未察觉的张力**：

- $\rho_s(0)$ 与 $\lambda_L^{-2}(0)$ 是**同一物理量**（$\rho_s\propto\lambda_L^{-2}$）；
- $\rho_s$ 的"临界指数 $\nu=0.6717$"（第四轮，**温度形状**）与"$\rho_s(0)$ 掺杂值"（Uemura，**零温幅值**）是同一量的两个读出；
- 后者必须随 $x$ **减小**（式 6），而能隙比随 $x$ **增大**——若把两者都写成"随 $x$ 同向塌缩"就错了。

**精确化**：DM.13 $T_c=\min(T^*,T_\theta)$ 是**唯一控制结构**，但四个观测量分属两支、反向读出：

| 观测量 | 通道 | 对 $x$ 依赖 | 极限行为 |
|:---|:---|:---|:---|
| 能隙比 $2\Delta/k_BT_c$ | 配对支（$T^*$，分子） | $\propto(1+x)$ ↑ | 欠掺大、过掺 $\to r_d$ |
| 迈斯纳刚度 $\lambda_L^{-2}(0)$ / $\rho_s(0)$ | 相位支（$T_\theta$，Uemura） | $\propto1/(1+x)$ ↓ | 欠掺小、过掺饱和 |
| 比热跳变 $\Delta C/\gamma T_c$ | 两支重合度 | $1.43\to0$ | 过掺 1.43、欠掺 0 |
| $\rho_s(T)$ 临界指数 | 相位支（3D XY 形状） | 与 $x$ 无关（$\nu=0.6717$） | 普适 |

"同点"仍是 $x=0$（$T^*=T_\theta$，crossover），但**方向分通道**。这个精确化把第十八轮的"统一"从"一个函数三塌缩"升级为"一个控制量、四投影、两方向"——更强、更可证伪。

### §3.3 $\lambda_L(T)$ 温度曲线与一个 $\nu$ 的三读数（承接第四/十七轮）

由式 (2) 与 $\rho_s\propto\lambda_L^{-2}$，第四轮的零参数曲线直接给出：

$$\frac{\lambda_L^{-2}(T)}{\lambda_L^{-2}(0)}=\frac{\rho_s(T)}{\rho_s(0)}=f(t)=(1-t)^{\nu}\bigl[1+(\nu-a)t\bigr],\qquad t=\frac{T}{T_c}.\tag{7}$$

临界区 $f(t)\sim(1-t)^\nu$，$\nu=0.6717$（3D XY，**非平均场 $1/2$**）；hyperscaling 给比热指数 $\alpha=2-3\nu=-0.0151<0\Rightarrow\Delta C=0$（第十七轮 M.96a）。**一个 $\nu$、三读数**：$\rho_s$ 临界、$\lambda_L$ 临界、比热连续——同属 3D XY 普适类，非三次拟合。

---

## 第四部分：新判据 R37（可证伪）

> **R37a（分通道，与能隙比反号）**：同一欠掺材料序列，若以独立 $T^*$（ARPES/Andreev）固定分子，则 $\lambda_L^{-2}(0)$ 须随 $T^*/T_c-1$ **减小**（Uemura 相位支，$\propto T_c$），而 $2\Delta_0/k_BT_c$ 须**增大**（DM.14′）。若两者同向，则"迈斯纳刚度读相位通道 / 能隙比读配对通道"的分支被证伪，CQM 两阶段失效。
>
> **R37b（临界指数）**：$\lambda_L^{-2}(T)\sim(T_c-T)^{\nu}$，$\nu=0.6717$（3D XY），非平均场 $1/2$、非 $2\nu$。μSR 高分辨 $\lambda_L(T)$ 临界区拟合可直接判决；若给出 $\nu\approx1/2$，则第四轮 $\rho_s$ 指数的 3D XY 归属被否定。
>
> **R37c（退化链）**：$\lambda_L=2\lambda_p/\sqrt{\Lambda}$，$\Lambda\le1$；若用同一 Drude 权重口径测得 $\lambda_L/\lambda_p<2$，则 M.83 凝聚分数 $1/4$ 受质疑（口径差须先排除，LH7）。

与 R29（记忆核终值）、R30（振幅频率标度）、R31（量纲量子）、R32（三普适类）、R33–35（比热）、R36（能隙比）测不同对象，互相独立。

---

## 第五部分：退化守住与边界

| 退化/成果 | 本轮处理 | 状态 |
|:---|:---|:---|
| 迈斯纳 | $\lambda_L=2\lambda_p/\sqrt\Lambda$ 代数验证；London 形式不变、$n_s$ 按两阶段分支读 | ✓ 强化（从条件预言→严格代数+通道归属） |
| BCS | 配对限制支 $n_s/n\to1\Rightarrow\lambda_L=\lambda_p$；$\gamma\to0$ 同位素退化未碰 | ✓ |
| Z2/Z3 | 绝对 $\lambda_L$ 外生 $m^*,e$；本轮只给无量纲比 $\lambda_L/\lambda_p$、$\nu$、方向 | ✓ 未越界 |
| $\rho_s(T)$ 曲线 / 比热 | 式 (7) 承接第四轮；$\nu$ 三读数承接第十七轮 | ✓ 未改 |
| 能隙比 DM.14′ / 三统一 | 精确化为"一控制量、四投影、两方向" | ✓ 强化 |
| R27–R36、M.53、$\zeta$/质数形状侧 | 未触碰 | ✓ |

**诚实边界**：
1. 式 (6) 的 $\lambda_L^{-2}\propto1/(1+x)$ 依赖"$T^*$ 欠掺近似 doping 无关"这一实验图像（LNW/Božović），非严格定理；若 $T^*$ 随掺杂显著变化，方向判据 R37a 需改用实测 $T^*/(1+x)$ 而非 $1/(1+x)$。方向相反的**结构结论**（两支分通道）不依赖此近似。
2. $\lambda_L/\lambda_p=2/\sqrt\Lambda$ 的 $\Lambda=1$ 锐利形式受 $\omega_p$ 口径限制（Drude vs 全带 $f$-和差 4–5 倍），只作条件可检形式。
3. $\mu_0\varepsilon_0c^2$ 的数值 $0.999999999456$ 是 CODATA 常数有限精度所致，解析上严格等于 1。

---

## 第六部分：外部文献（逐条带出处）

| 编号 | 出处 | 结论 | 用途 |
|:---|:---|:---|:---|
| M1 | Fernandes, *Lecture Notes: BCS theory*, 式(106)(117)(118) | rigidity $n_s$ 决定 Meissner 而非 $\Delta$；gapless 仍 Meissner；Anderson–Higgs | §2.1/§2.2 主证据 |
| M2 | Oreg, *Concepts of Condensed Matter Physics* §6.3–6.4, 式(21)(22)(23) | Anderson–Higgs 四步；伦敦方程；$\lambda=\sqrt{mc^2/4\pi n_se^2}$ | §2.1 标准链 |
| M3 | Finnemore et al., *Phys. Rev.* **172**, 430 (1968) | Th-Gd gapless 合金 "all show a Meissner effect"，AG 理论拟合 0.5% | §2.2 硬实验 |
| M4 | Uemura et al., *Phys. Rev. Lett.* **62**, 2317 (1989)；Bohrium "Uemura 关系" | $T_c\propto n_s/m^*\propto\lambda_L^{-2}$（欠掺），过掺断裂 | §2.3/§3.1 Uemura |
| M5 | Emery & Kivelson, *Nature* **374**, 434 (1995), DOI:10.1038/374434a0 | 小超流密度下相位涨落决定 $T_c$ | §2.3 相位限制 |
| M6 | Lee–Nagaosa–Wen, cond-mat/0205497；Bohrium "超导穹顶" | stiffness-limited（欠掺）vs pairing-limited（过掺）crossover | §2.3/§3.1 |
| M7 | Božović et al., *Nature* **536**, 309 (2016) | 过掺 $T_c=T_0+\alpha\rho_{s0}$，深过掺 $T_c=\gamma\sqrt{\rho_{s0}}$ | §3.1 Uemura 断裂 |
| M8 | Wiedemann–Nikolić–Eschrig–Belzig, arXiv:2609.02263 | anisotropic gapless → paramagnetic Meissner；微波超流刚度探 gapless | §2.2 佐证 |
| M9 | Campostrini et al., *PRB* **74**, 144506 (2006)；第四/十七轮 | 3D XY $\nu=0.6717$、$\alpha=2-3\nu=-0.0151$ | §3.3 普适指数 |
| M10 | Villarreal–de Llano, arXiv:1001.0957 式(15–16)；第十八轮 EG3 | 自定义通道因子 $\Gamma^{(2)}=2e^{-1/2}=1.213$（本稿记作 $g_2$，非标准 $\Gamma(2)$），$r_d=4.279$ | §3.1 能隙比 |

---

## 第七部分：本轮小结

1. **兑现承诺**：迈斯纳退化从"一句条件预言"升级为 SI 第一性严格代数（$\lambda_L=2\lambda_p/\sqrt\Lambda$，因子 2 = M.83 的 $1/4$ 平方根倒数）+ 相位通道归属（外部三重证据）+ 两阶段温度曲线（式 7）。
2. **constructive 精确化**：第十八轮"三观测量统一"升级为"一个控制量 $x$、四投影、两通道反向读出"；迈斯纳刚度 $\propto1/(1+x)$（相位支）与能隙比 $\propto(1+x)$（配对支）方向相反——非矛盾，而是两阶段的本质。
3. **可证伪判据 R37a/b/c**：分通道反号、$\lambda_L$ 临界指数 $\nu=0.6717$、退化链比值。
4. **守住**：BCS/迈斯纳/Z2/Z3/R27–R36/$\zeta$ 形状侧全未破坏；零拟合参数。
5. **诚实纠错链**：本轮脚本初稿曾误判 $\Lambda$ 在分母，经原文核查（M.83′ 四处一致）抓回；Homes 稿 L243 表格 $\Lambda$ 位置笔误已就地加指针（保留原文）。

按用户要求：不做 Lean/网站/完整革命理论文档；未提交 git；未删除任何文档。
