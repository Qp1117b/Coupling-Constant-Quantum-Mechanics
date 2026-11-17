# CQM 探索：约瑟夫森效应两阶段分支与磁通量子的配对/相位分解——R41

> **定位**：探索稿（非权威源），v0.1，2026-11-17，第二十三轮。承接第二十二轮 FGT 光学求和规则，正面处理超导第三个宏观量子现象——**约瑟夫森效应**（前两轮已完成迈斯纳/FGT 凝聚）。
>
> **靶点空白核查**：全库反复出现"相位通道 vs 配对通道"，但约瑟夫森这一"相位相干的旗舰探针"从未被系统审计。而第二十二轮 Homes 原文已埋下接缝：c 轴输运$=$Josephson 效应、dirty limit 与 Josephson 效应"功能上几乎等同"。核心问题：约瑟夫森同时含**能隙**（Ambegaokar–Baratoff $I_cR_N=\pi\Delta/2e$，配对量）与**相位刚度**（Josephson 等离子体 $\omega_{pl}^2\propto\rho_s$，相位量）两个源头——恰是两阶段解耦的天然试验台。
>
> **一句话结论**：约瑟夫森效应严格二分——$I_cR_N=\pi\Delta_*/2e$ 归**配对通道**（$\propto T^*$）、$\omega_{pl}^2=c^2/\epsilon_c\lambda_c^2\propto\rho_{sc}\propto T_c$ 归**相位通道**（Uemura，JPR 实测 $f^2\propto T_c$），BCS 中二者同源 $\propto T_c$、两阶段欠掺解耦（分离比 $1+x$）。磁通量子 $\Phi_0=h/2e$ 更可作**结构分解**：因子"$2$"（电荷 $2e$）属阶段一配对、在 $T^*$ 已由 Andreev/Nernst 可见；"$\oint\nabla\theta=d\,2\pi n$ 的量子化"属阶段二相位、只在 $T_c$ 以下成立——故"$2e$ 预成对"与"磁通量子化只在超导态"不再是矛盾，而是两阶段分离的直接推论。新增判据 R41。**绝对 $\Phi_0,K_J$ 数值外生 $e,h$（Z3，本轮只给拓扑结构分工）。**

---

## 第一部分：磁通量子的配对/相位结构分解（本轮核心，概念贡献）

SI 2019（$e,h$ 精确）第一性（脚本 §1）：

$$\Phi_0=\frac{h}{2e}=2.067833848\times10^{-15}\ {\rm Wb},\qquad K_J=\frac{2e}{h}=483.5978\ {\rm THz/V}\ (\rm 精确) \tag{J.1}$$

数值是外生常数（Z3：CQM 从第一性不给 $e,\hbar$ 数值，第十五轮 R31 已封）。但 $\Phi_0$ 的**结构**可分解进两阶段：

| 结构因子 | 物理来源 | 归属通道 | 出现温区 |
|:---|:---|:---|:---|
| 电荷 $2e$（分母的"2"） | 库珀配对 | **阶段一·配对**（$T^*$） | $T^*$ 以下（预成对，Nernst/Andreev 可见） |
| $\oint\nabla\theta\cdot d\ell=2\pi n$（量子化条件） | 全局相位相干 | **阶段二·相位**（$T_c$） | 仅 $T_c$ 以下 |

**判决**：常规超导把"$\Phi_0=h/2e$ 来自电荷 $2e$"当作一句话；两阶段框架要求**两件事同时到位**才有磁通量子化——配对给出 $2e$、相位相干给出量子化条件。这解释了一个长期被含糊处理的实验事实：**赝能隙区（$T_c<T<T^*$）有 $2e$ 配对信号（Nernst、Andreev 反射、STM 相干峰消失但能隙保留），却没有磁通量子化/零电阻**——因为相位量子化条件尚未满足。这不是悖论，是 (J.1) 两因子分属两支的必然。

---

## 第二部分：约瑟夫森两源头——Ambegaokar–Baratoff（配对）vs 等离子体（相位）

### 2.1 配对通道：$I_cR_N=\pi\Delta_*/2e$

T=0 s 波 SIS 隧穿（有限温乘 $\tanh(\Delta/2k_BT)$）：

$$I_cR_N=\frac{\pi\Delta_*}{2e}\quad\Rightarrow\quad \frac{2e\,I_cR_N}{\pi k_BT_c}=\frac{\Delta_*}{k_BT_c}=\tfrac12\,r_d(T^*/T_c)\propto\frac{T^*}{T_c}=1+x \tag{J.2}$$

脚本 §2 校验例（$\Delta=1.2$ meV, $R_N=10\,\Omega$）给 $I_c=188.50\,\mu$A，与文献 $\sim188\,\mu$A 一致。判读：(J.2) 把 AB 乘积归一化到 $T_c$，正好是第十八轮能隙比 $r_d(T^*/T_c)$ 的一半——**AB 临界电流乘积是配对通道可观测量，随 $1+x$ 增大**。

### 2.2 相位通道：$\omega_{pl}^2=c^2/\epsilon_c\lambda_c^2$

层状结电容 $C=\epsilon_0\epsilon_c A/d$、直流 Josephson $I_c=J_cA$ 给 $\omega_{pl}^2=2eI_c/\hbar C$，SI 第一性三式等价（脚本 §3 三式 `match=True`）：

$$\omega_{pl}^2=\frac{2eJ_cd}{\hbar\epsilon_0\epsilon_c}=\frac{2\pi J_cd}{\epsilon_0\epsilon_c\Phi_0}=\frac{c^2}{\epsilon_c\lambda_c^2},\qquad \lambda_c^2=\frac{\Phi_0}{2\pi\mu_0J_cd} \tag{J.3}$$

取 $J_c=10^7$ A/m², $d=1.2$ nm, $\epsilon_c=14$ 给 $\omega_{pl}/2\pi=0.086$ THz，落在文献 10–500 GHz 区。判读：$\omega_{pl}^2\propto J_c\propto\rho_{sc}$（c 轴超流密度，$=\lambda_c^{-2}$ 家族）——**等离子体频率是相位刚度可观测量**。

### 2.3 两源头对照表

| 约瑟夫森量 | 公式 | 主导通道 | 欠掺标度 | BCS 标度 |
|:---|:---|:---|:---|:---|
| $I_cR_N$（隧道临界乘积） | $\pi\Delta_*/2e$ (J.2) | 配对（能隙） | $\propto T^*$ ↑ | $\propto T_c$ |
| $\omega_{pl}^2$（等离子体） | $c^2/\epsilon_c\lambda_c^2$ (J.3) | 相位（刚度） | $\propto T_c$ ↓ | $\propto T_c$ |
| $\Phi_0$（磁通量子） | $h/2e$ (J.1) | 两通道$=$配对电荷×相位量子化 | 结构不变 | 同 |

---

## 第三部分：两阶段解耦与实验判决

### 3.1 解耦结构（脚本 §4）

$${\rm BCS}:\ \Delta\propto T_c\ \text{且}\ \rho_s\propto T_c\ \Rightarrow\ I_cR_N,\ \omega_{pl}^2\ \text{同源}\propto T_c\ (\text{无分离})$$

$${\rm 两阶段欠掺}:\ I_cR_N\propto\Delta_*\propto T^*\ (\text{配对}) ,\quad \omega_{pl}^2\propto\rho_{sc}\propto T_c\ (\text{相位})$$

$$\text{分离比}=\frac{[I_cR_N/T_c]}{[\omega_{pl}^2/\omega_{pl}^2(T_c)]}\propto\frac{T^*}{T_c}=1+x \tag{J.4}$$

$T^*/T_c=1.85/2.22/3.04$（第十八轮汞系零参数反解）给分离比 1.85/2.22/3.04，随欠掺深化增大；$x\to0$ 退化到 1（BCS）。

### 3.2 外部实验判决（全带出处）

| 编号 | 来源 | 关键结论 | 与 CQM 对接 |
|:---|:---|:---|:---|
| J1 | C.C. Homes, *Physica C* **445–448**, 8–13 (2006) | c 轴输运由 Josephson 效应描述；dirty limit 与 Josephson 效应"功能上几乎等同" | 第二十二轮接缝；c 轴归相位通道 |
| J2 | V. Ambegaokar & A. Baratoff, *PRL* **10**, 486 (1963); Tinkham《Introduction to Superconductivity》§6 | $I_cR_N=\pi\Delta/2e$（T=0 s 波），有限温 $\tanh$ | (J.2) 配对通道 |
| J3 | M.B. Gaifullin, Y. Matsuda et al., *Physica C* (2001), S0921453401003409 | JPR 测 c 轴超流密度；$\omega_p=c/(\sqrt{\epsilon_c}\lambda_c)=[8\pi^2cdJ_0/\epsilon_c\Phi_0]^{1/2}$ | (J.3) 相位通道 |
| J4 | A. Rullier-Albenque et al., *PRB* (2007), S0921453407002675 | 欠掺 Bi2212：$f_{JPR}$ 随辐照**正比于 $T_c$** 下降；温度依赖与**相位量子涨落模型**定量符合，与相干隧穿矛盾 | $\omega_{pl}^2\propto T_c$ 相位通道指纹；R41b 直接证据 |
| J5 | Gaifullin/Matsuda, *JPR underdoped Bi2212*, S0921453401012497 | 重欠掺 $T_c=69.4$K、$\omega_{pl}/2\pi\approx61$ GHz（远低于 gap≈1 THz）；$\omega_{pl}^2\propto J_c^{max}\langle\cos\varphi\rangle$ | 等离子体低频、相位敏感；$J_c$ 相位通道 |
| J6 | Bohrium/集智百科 Josephson 条目 | $E_J=\Phi_0I_c/2\pi$、$[\hat\varphi,\hat n]=i$；磁通量子 $\Phi_0=h/2e$ 源于电荷 $2e$ | (J.1) 结构；相位-电荷共轭 |
| J7 | Nernst/Andreev/STM 赝能隙综述（Bohrium 科普 Pseudogap；Deutscher 2005 Andreev） | $T_c$ 以上有 $2e$ 配对信号（大 Nernst、自旋隙、能隙保留但相干峰消失） | R41a：$2e$ 在 $T^*$ 可见、$\Phi_0$ 量子化只在 $T_c$ 以下 |
| J8 | F. Loder, A.P. Kampf, T. Kopp, arXiv:1212.2429 (2012) | 非常规超导环 $hc/4e$ 分数磁通周期（四重态/PDW 候选） | R41c 外来分支边界，本框架不预言 |

**判决**：J4 是最硬证据——等离子体频率随掺杂/辐照**追随 $T_c$ 而非能隙**、且温度依赖吻合相位量子涨落，正是 (J.4) 相位通道标度；若只有一个能隙（BCS），$\omega_{pl}^2\propto\Delta\propto T_c$ 无从区分，欠掺 "$f_{JPR}\propto T_c$ 而 $\Delta_*\propto T^*$" 的分离才是两阶段的指纹。

---

## 第四部分：新判据 R41（可证伪，三条互补）

- **R41a（磁通量子的配对/相位分解）**：$T_c<T<T^*$ 的赝能隙区须测到 $2e$ 配对信号（Andreev 反射 $2e$、Nernst 涡旋、STM 能隙保留）但**无** $\Phi_0$ 磁通量子化/零电阻。若在 $T_c$ 以上稳健测到 $\Phi_0$ 整数量子化，则"量子化属相位通道（$T_c$）"被证伪，两阶段分解失效。
- **R41b（约瑟夫森双通道解耦）**：$\omega_{pl}^2\propto T_c$（相位，JPR），$I_cR_N\propto\Delta_*\propto T^*$（配对，AB 隧道）；分离比 (J.4) 随 $x=T^*/T_c-1$ 增大。若同一欠掺序列两支都 $\propto T_c$（无分离），两阶段约瑟夫森判决否定。
- **R41c（分数通量边界）**：$hc/4e$（四重态/PDW）为外来分支，本框架不预言；若稳健重复观测到 $hc/4e$ 周期，需扩展配对拓扑（登记为边界，不硬套、不拟合）。

与 R29–R40 测不同对象（本轮测约瑟夫森/磁通量子拓扑层），互相独立。

---

## 第五部分：边界、退化、范式自检

**退化守住**：
- **BCS**：s 波 AB $I_cR_N=\pi\Delta/2e$ + $\omega_{pl}^2\propto\rho_s\propto T_c$，两源同源 $\propto T_c$，$x\to0$ 自动恢复标准约瑟夫森；磁通量子 $\Phi_0=h/2e$ 本就是 BCS 结论，未改一字。
- **迈斯纳**（第十九/二十二轮）：$\omega_{pl}^2\propto\lambda_c^{-2}$ 与 $\lambda_{ab}^{-2}$ 同属 $\rho_s$ 家族（相位通道），$N_c\propto\rho_s$ 光学定义层互补不冲突。
- **GL $\kappa$**（第二十一轮 R39）：$\kappa=\lambda_{ab}/\xi$，$\lambda_{ab}$ 由 $\rho_s\propto T_c$（相位）、$\xi$ 由 $\Delta_*\propto T^*$（配对）——与第二轮同一 $\rho_s$-$\Delta_*$ 二分，三探针（约瑟夫森层间/迈斯纳面内/GL $\kappa$）互不冲突。
- **一个 $x$ 现统一七个投影**：$N_c,\rho_s,\lambda_L^{-2},\Delta C,U,\kappa$（前六，第二十二轮）+ $I_cR_N/\omega_{pl}^2$ 分离比（本轮第七），分属配对/相位两通道。
- **Z1/Z2/Z3、R27–R40、M.53、$\zeta$/质数形状侧**：全部未触碰。

**能标边界（诚实）**：$\Phi_0,K_J$ 绝对值外生 $e,h$（Z3/R31）；$J_c,\epsilon_c,\lambda_c$ 绝对值外生微观参数（Z2）——本轮只给**拓扑结构分解 + 无量纲分离比 $1+x$**，不承诺绝对数值。$hc/4e$ 外来分支明确不预言。

**克制拟合**：全轮无拟合参数。$1.2$ meV/$10\,\Omega$ 为文献校验例、$T^*/T_c=1.85/2.22/3.04$ 为第十八轮零参数反解、$J_c/\epsilon_c$ 为量级演示——均标注外部，不用于参数调节。

**范式**：关系性范式；不改 `01–08`、`归档/` 的定义与数值；只在 `10 探索/` 新增本文并给相关旧稿加指针（保留原文）。

---

## 附：脚本与数据

- 脚本：`10 探索/.calc/josephson_two_stage_audit.py`（已 gitignore）
- 第一性验证：(J.1) $\Phi_0=2.067833848\times10^{-15}$ Wb、$K_J=483.5978$ THz/V；(J.3) 三式 `match=True`、$\omega_{pl}/2\pi=0.086$ THz
- 全部外部文献 J1–J8 带 DOI/PRL卷页/arXiv/ScienceDirect 编号，作者已逐一核实
