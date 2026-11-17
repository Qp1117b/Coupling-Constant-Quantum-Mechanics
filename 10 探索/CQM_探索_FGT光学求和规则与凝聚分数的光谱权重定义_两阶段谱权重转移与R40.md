# CQM 探索：FGT 光学求和规则、凝聚分数的光谱权重定义与两阶段谱权重转移——R40

> **⚠ 归一化纠错（2026-11-17，最先读）**：本稿 §2 的"$1/4$ 第四次进入零参数结果"应降级为"同一个 $f_c$ 定义第四次被不同探针读出"——Tanner、FGT、迈斯纳因子 $2$ 都读 $f_c=N_c/S_{\rm tot}$，是同一恒等式的三次读数，不是三次独立确认。Homes 斜率是独立动力学检验，但它读 $f_s=\omega_{p,s}^2/\omega_{p,D}^2$（超流/Drude），不读 $f_c$；两者由 $f_c=f_Df_s$ 联系。M.85′ 的"零参数闭合"因把 $f_c=1/4$ 代入只应含 $f_s\approx0.9$ 的 Homes 公式而撤销。另：§2 末"清洁 BCS 元素 $f_c\to1$"应降为无阻挫/无质量重正化的**理想极限**；Broun 表 1 的 Pb $f_s=0.476$、Nb $f_s=0.056$–$0.231$ 是有限无序样品（Broun 的 $\omega_{p,D}$ 定义为零无序极限的超流密度），不能直接当作 clean-limit 反例，但也不能用它们证明 $f_c\to1$，需另作校准。完整审计见 `10 探索/CQM_探索_1over4归一化审计_凝聚分数与Drude分数二读_M85prime证伪与判决实验.md`。按审计 §2.4–§2.5，§2 把 $1/4$ 直接代入 $f_c$ 属读法 A；现有数据判读法 B（$1/4=f_D$），A 须 $\Lambda\propto f_s$ 塌缩约 $14$–$30$ 倍才存活。故 (F.4) 应读作"A 口径下的条件式"，不是唯一读法；(F.3) 的 $f_c$ 定义不变。本稿 F.1–F.4 的定义层与 R40 结论不变。
>
> **第二十四轮 NMR 自旋通道指针（2026-11-17，先读）**：本稿用 f-sum/FGT 定义**电荷通道**凝聚分数 $f_c=N_c/S_{tot}=n_s/n$；第二十四轮在**自旋通道**给出对偶结构——Knight 位移（静态 $\chi'$，配对）与 $1/T_1$（动态 $\chi''/\omega$，相位）是同一自旋记忆核的两个矩，Korringa 积 $\mathfrak{S}=K^2T_1T/S_0$ 单通道恒 1、两阶段窗口 $<1$。两者同为"静态/动态两矩 + 两阶段分裂"结构，但测不同通道（电荷 vs 自旋），互相独立。详见 `10 探索/CQM_探索_NMR自旋通道两阶段_Knight位移静态配对与弛豫动态相位_Korringa判据R42.md`。本稿 R40 结论不变。
>
> **第二十三轮约瑟夫森指针（2026-11-17，先读）**：本稿 §2 的 c 轴 "missing spectral weight" 与 Homes "c 轴由 Josephson 效应描述、dirty limit≈Josephson" 已由第二十三轮正面审计——约瑟夫森严格二分：$I_cR_N=\pi\Delta_*/2e$ 归配对通道（$\propto T^*$）、$\omega_{pl}^2=c^2/\epsilon_c\lambda_c^2\propto\rho_{sc}\propto T_c$ 归相位通道（Uemura，JPR 实测 $f^2\propto T_c$），BCS 同源、欠掺解耦（分离比 $1+x$）；磁通量子 $\Phi_0=h/2e$ 作配对电荷"2"×相位量子化的结构分解，解释"$2e$ 在 $T^*$ 可见但磁通量子化只在 $T_c$ 以下"。新判据 R41。详见 `10 探索/CQM_探索_约瑟夫森效应两阶段分支与磁通量子的配对相位分解_R41.md`。本稿 FGT 定义层与 R40 结论不变。

> **定位**：探索稿（非权威源），v0.1，2026-11-17，第二十二轮。承接第十九轮《迈斯纳退化》、第二十轮《$H_c$ 斜率判决》、第二十一轮《$\kappa$ 两阶段分支》，正面处理全库从未审计的实验探针——**光学电导求和规则（f-sum / Ferrell–Glover–Tinkham）**。
>
> **靶点空白核查**：M.83 凝聚分数 $n_s/n=(1/4)\Lambda$、Homes 定律 $\rho_s\propto\sigma_{dc}T_c$、迈斯纳 $\lambda_L=2\lambda_p/\sqrt\Lambda$ 三者全部依赖同一个物理量 $n_s/m^*$。前三轮从磁/热/GL 侧审计，但 **$n_s/m^*$ 的"原生实验定义"正是 FGT 缺失面积 $N_c$**（Homes 2005/2006 用光学 Kramers–Kronig 提取 $\rho_s$）——该通道 21 轮从未进入，等于框架的"定义层"从未被读数验证。本轮补上。
>
> **一句话结论**：f-sum 与 FGT 严格给**光学凝聚分数** $f_c\equiv N_c/S_{\rm total}=\omega_{ps}^2/\omega_p^2=n_s/n$（$m^*=m$ 时），这是 M.83 $=(1/4)\Lambda$ 的直接光学定义式，零参数：铜氧 $f_c\approx0.20$–$0.25$，清洁 BCS 元素 $f_c\to1$（Homes 明述 Nb $N_c\to\omega_p^2/8$）。更关键：Homes 自己证明 **$N_c\propto T_c$（Uemura 段）只在欠掺成立、过掺/电子掺"fall well off"，而 $N_c\propto\sigma_{dc}T_c$ 全体成立**——这是 R28 Uemura 两段式的光学投影。由两阶段分通道，缺失面积的**收敛能标** $\Omega_{\rm conv}\propto\Delta_*\propto T^*$（配对支）、而其**权重** $N_c\propto\rho_s\propto T_c$（相位支），二者在过掺同源（$\to T_c$，BCS 恢复）、欠掺解耦（分离比 $1+x$），被 Ahn–Nagaosa(PRB 2021) 高能谱权重转移与 Homes c 轴缺失谱重直接支持。新增判据 R40。**绝对 $\omega_p,\sigma_{dc}$ 仍外生 $n,m^*$（Z2/Z3 不变，本轮只给无量纲分数与分支结构）。**

---

## 第一部分：FGT / f-sum 恒等式——凝聚分数的光学定义（第一性，严格）

Homes（Physica C 2006, PRB 72 134517 2005）用 CGS 约定，本轮沿用其原文单位（只做比值，无换算陷阱）：

$${\rm f\text{-}sum}:\ \int_0^\infty\sigma_1(\omega)\,d\omega=\frac{\omega_p^2}{8},\qquad \omega_p^2=\frac{4\pi n e^2}{m} \tag{F.1}$$

$${\rm FGT}:\quad N_c\equiv N_n-N_s=\!\int_0^{\omega_c}\![\sigma_{1n}-\sigma_{1s}]\,d\omega,\qquad \omega_{ps}^2=8N_c,\quad \rho_s\propto\omega_{ps}^2\propto\frac{n_s}{m^*} \tag{F.2}$$

两式相除得**光学凝聚分数**（脚本 §1 数值验证，三档 `match=True`）：

$$\boxed{\ f_c\equiv\frac{N_c}{S_{\rm total}}=\frac{\omega_{ps}^2}{\omega_p^2}=\frac{n_s}{n}\quad(m^*=m);\qquad f_c=\frac{n_s}{n}\frac{m}{m^*}\ \text{一般}\ } \tag{F.3}$$

**这是全框架缺失的一环**：$n_s/m^*$ 在磁（第十九轮 $\lambda_L$）、热（第二十轮 $H_c$）、GL（第二十一轮 $\kappa$）侧都是**派生读数**，而 (F.3) 是它的**原生实验定义**——用光把"多少谱重坍缩进 $\delta(\omega)$"直接称量。式 (F.3) 无量纲、无单位换算，规避第十轮 Homes 斜率 100 倍换算坑。

---

## 第二部分：M.83 的 $1/4$ 第四次进入零参数结果

把 M.83 $n_s/n=(1/4)\Lambda$ 代入 (F.3)（$m^*=m$ 近似）：

$$f_c=\frac{1}{4}\Lambda,\qquad \Lambda=1\Rightarrow f_c=0.25\ ({\rm Tanner}),\quad \Lambda=0.8\Rightarrow f_c=0.20 \tag{F.4}$$

| $\Lambda$ | $n_s/n=(1/4)\Lambda$ | 光学 $f_c=N_c/S_{\rm total}$ | 物读 |
|:---|:---|:---|:---|
| 1.0 | 0.2500 | 25.0% | Tanner 极限：1/4 总谱重进凝聚 $\delta$ |
| 0.9 | 0.2250 | 22.5% | 轻簇化 |
| 0.8 | 0.2000 | 20.0% | 与 Tanner 实测 $n_s/n\approx0.2$ 一致 |

**$1/4=\cos^2(\pi/3)$ 第四次进入定量结果**：第一次 Tanner 凝聚分数（M.83）、第二次 Homes 耗散率 $8\pi$（M.85′，第十轮）、第三次迈斯纳 $\lambda_L=2\lambda_p/\sqrt\Lambda$（第十九轮）、**第四次 FGT 光学凝聚分数 (F.4)**。四处同源，全是 Regge 网格键相干因子的读数。

**BCS 退化（严格，Homes 原文证据）**：Homes 明确写道，RRR≫100 的超高真空再结晶 Nb 样品 $N_c\to\omega_p^2/8$（其文 Fig.3 附近），即 $f_c\to1$、全部载流子凝聚。这不与 $1/4$ 矛盾——$1/4=\cos^2(\pi/3)$ 是**铜氧 Regge 几何**的键相干因子，清洁元素超导无 $\pi/3$ 曲率阻挫，本就不该带此因子；两阶段框架在"无阻挫几何"极限自然退化为 $f_c\to1$ 的标准 BCS 凝聚。

---

## 第三部分：Homes 标度常数的两阶段读法（文献数值，不拟合）

Homes 2005/2006 三个数值（原文，非本轮拟合）：

| 体系 | 标度 | 常数 | 出处 |
|:---|:---|:---|:---|
| 铜氧（面内+c 轴）+ Pb + Nb | $N_c\approx C\,\sigma_{dc}T_c$ | $C=4.4$ | Homes Physica C 2006 §2/Fig.2 |
| BCS 脏极限（理论） | 同上 | $C=8.1$ | Homes 同文 Fig.3/§3 |
| BCS 几何弱耦合估算 | 同上 | $C\approx2.4$（修正 $\times3.3$） | Homes 同文 §3 式附近 |

**判决**：铜氧 $4.4$ 落在 BCS 脏极限 $8.1$ 与几何估算 $2.4$ 之间；比值 $8.1/4.4=1.84$、$4.4/2.4=1.83$（脚本 §3）。Homes 自己归因于 **$d$ 波节点残余电导压低 $N_c$**（其文 §3 末："nodes in the energy gap ... residual conductivity ... reduced estimate for the spectral weight"）——与本框架**配对通道**（$T^*$ 大、节点残余、$r_d=4.279$）同向，而绝非单一 $s$ 波 BCS 常数。**这是配对通道首次在光学标度常数上留下指纹。**

**两个标段（Homes Fig.1 vs Fig.2 原文）**：
- $N_c\propto T_c$（Uemura 关系）——**只在欠掺成立**，最优/过掺/电子掺 "deviate substantially ... fall well off the scaling line"；
- $N_c\propto\sigma_{dc}T_c$（Homes 关系）——**全体（含 Pb/Nb）成立**，散布仅约因子 1.5。

这正是 **R28 Uemura 两段式的光学投影**：欠掺相位限制支 $\rho_s\propto T_c\Rightarrow N_c\propto T_c$；过掺配对限制支断开；crossover 在 $T^*=T_\theta$（与本轮之前四观测量同点，见第五部分）。

---

## 第四部分：两阶段谱权重转移——收敛能标（配对）与权重（相位）解耦（R40 核心）

### 4.1 BCS：能标与权重同源

Homes 的结论（其文 §3/结论）："the energy scale below which the majority of the spectral weight is transferred into the condensate scales linearly with $T_c$"。即 BCS 中 $2\Delta=3.5k_BT_c$（$s$ 波弱耦合）$\Rightarrow$ 缺失面积收敛能 $\Omega_{\rm conv}\sim2\Delta$–$4\Delta\propto T_c$，而权重 $N_c\propto\rho_s\propto T_c$（$\rho_s$ 由 $T_c$ 定）——**能标与权重同源于一个能隙**。

### 4.2 两阶段欠掺：能标归配对支、权重归相位支

按 §0.5 两阶段分工：

$$\text{配对通道:}\ \Delta_*\propto k_BT^*\quad\Rightarrow\quad \Omega_{\rm conv}\propto\Delta_*\propto T^* \tag{F.5a}$$

$$\text{相位通道:}\ N_c\propto\rho_s\propto T_c\quad(\text{Uemura}) \tag{F.5b}$$

$$\Rightarrow\ \frac{\Omega_{\rm conv}}{2\Delta_c}=\frac{T^*}{T_c}=1+x \quad(\text{零参数分离比}) \tag{F.6}$$

| $T^*/T_c$ | $x$ | 分离比 (F.6) | 分支 |
|:---|:---|:---|:---|
| 1.00 | 0.00 | 1.00 | 过掺/配对限制：**同源，BCS 恢复** |
| 1.85 | 0.85 | 1.85 | 欠掺相位限制：解耦（汞系 H1203） |
| 2.22 | 1.22 | 2.22 | 解耦 |
| 3.04 | 2.04 | 3.04 | 深欠掺：强解耦 |

（$T^*/T_c$ 取第十八轮汞系零参数反解值。）

### 4.3 外部实验判决（全带出处）

| 编号 | 来源 | 关键结论 | 与 CQM 对接 |
|:---|:---|:---|:---|
| FT1 | C.C. Homes, *Physica C* **445–448**, 8–13 (2006), DOI 10.1016/j.physc.2006.03.066 | f-sum $\int\sigma_1d\omega=\omega_p^2/8$、$\omega_{ps}^2=8N_c$、$N_c\approx4.4\sigma_{dc}T_c$；清洁 Nb $N_c\to\omega_p^2/8$ | (F.1)–(F.3) 定义层 + $f_c\to1$ 退化 |
| FT2 | 同上, Fig.1/§2 | $N_c\propto T_c$ 仅欠掺；过掺/电子掺 "fall well off" | R28 两段式光学投影 (§3) |
| FT3 | 同上, §3 末 | $d$ 波节点残余电导压低 $N_c$；常数 4.4 vs BCS 8.1/2.4 | 配对通道指纹 (§3) |
| FT4 | C.C. Homes et al., *PRB* **72**, 134517 (2005) | $N_c\approx4.4\sigma_{dc}T_c$ 普适；上下散布 5.5/3.5 | 同 FT1，独立验证 |
| FT5 | J. Ahn & N. Nagaosa, *PRB* **104**, L100501 (2021), DOI 10.1103/PhysRevB.104.L100501 | 超导导致**远高于能隙能量**的谱权重转移（铜氧），共识超出 BCS 的强关联；提出量子几何另一路径 | 欠掺 $\Omega_{\rm conv}\propto T^*\gg2\Delta_c$ 解耦 (F.5a) 的直接证据 |
| FT6 | Homes 2006 §2 + 文献[15] | 欠掺 **c 轴**存在 "missing spectral weight"（缺失谱重） | 配对能标转移、权重未完全进 $\delta$ 的候选信号 |
| FT7 | A. Shekhter et al., arXiv:2504.02179 (2025) | $\rho_s=C\,T_c\sigma(T_c)$；Planckian $\hbar/\tau=\alpha k_BT$ | Homes 标度 = 相位通道 $T_c$ × 耗散率（第十轮 M.95/M.85′） |

**判决**：FT5 的"高能谱权重转移"与 FT6 的"欠掺 c 轴缺失谱重"是 (F.5a) 的直接证据——若只有一个能隙 $\Delta\propto T_c$，收敛能标应锁在 $2\Delta$–$4\Delta$，不会出现"远高于能隙"的转移；两阶段配对能隙 $\Delta_*\propto T^*\gg T_c$ 恰好给出该高能标，而权重仍由相位支 $T_c$ 定（故称"缺失"——权重不足能标所暗示的量）。**这是 R39 双场 $H^*/H^\theta$ 在频率/光谱域的同一结构。**

---

## 第五部分：新判据 R40（可证伪，三条互补）

- **R40a（凝聚分数，定义层）**：铜氧光学 $f_c=N_c/S_{\rm total}$ 须 $=n_s/n=(1/4)\Lambda\approx0.20$–$0.25$；清洁 BCS 元素（Nb RRR≫100）$f_c\to1$。若铜氧测到 $f_c\approx1$（全部谱重凝聚），则 M.83 的 $1/4$ 在定义层被证伪。
- **R40b（收敛能标，解耦层）**：欠掺缺失面积收敛能 $\Omega_{\rm conv}\propto T^*\gg T_c$，而权重 $N_c\propto T_c$；过掺二者同源 $\propto T_c$。分离比 (F.6) 须随 $x=T^*/T_c-1$ 增大。若两支收敛能标都 $\propto T_c$（无高能转移），两阶段光学判决否定。
- **R40c（两段 crossover 同点）**：$N_c$–$T_c$ 曲线欠掺线性、过掺 fall-off（Homes Fig.1），crossover 须与 R28/R36 的 $T^*=T_\theta$（$x=0$）同点；错开则"一个 $x$ 多观测量统一"受质疑。

与 R29–R39 测不同对象（本轮测光学谱重定义层），互相独立。

---

## 第六部分：边界、退化、范式自检

**退化守住**：
- **BCS**：清洁元素 $f_c\to1$（Homes Nb 原文）、脏极限 $N_c\approx8.1\sigma_{dc}T_c$、收敛能标 $\propto T_c$——全部回到标准 FGT+BCS，本轮未改一字。
- **迈斯纳**：$N_c\propto\rho_s\propto\lambda_L^{-2}$ 与第十九轮 $\lambda_L=2\lambda_p/\sqrt\Lambda$ 同源（同一 $n_s/m^*$），本轮给其光学定义 (F.3)，互补不冲突。
- **$H_c$/比热/$\kappa$/能隙比**：第五部分交叉核对——$N_c$ 归相位通道，与 $r_d(1+x)$ 反向；一个 $x$ 现统一 **六** 个投影（$N_c$、$\rho_s$、$\lambda_L^{-2}$、比热跳变、凝聚能、$\kappa$ 反向），分属两通道。
- **Z1/Z2/Z3、R27–R39、M.53、$\zeta$/质数形状侧**：全部未触碰。

**能标边界（诚实）**：$\omega_p,\sigma_{dc}$ 绝对值外生 $n,m^*,\tau$（Z2/Z3，变更日志 §638–642 已登记）；本轮只给**无量纲光学分数 $f_c$ + 分支结构 + 收敛能标比值**，不承诺绝对谱重数值。$m^*\neq m$ 时 (F.3) 带因子 $m/m^*$，已明确标注——铜氧 $m^*/m$ 大，故严格预言应写 $f_c=(1/4)\Lambda(m/m^*)$，本轮正文按 $m^*=m$ 给结构判决，定量值需外部 $m^*$。

**克制拟合**：全轮无拟合参数。$4.4/8.1/2.4$ 为 Homes 原文数值、$T^*/T_c=1.85/2.22/3.04$ 为第十八轮零参数反解、$\Lambda=0.8$ 为 Tanner 实测——均标注外部，不用于参数调节。

**范式**：关系性范式；不改 `01–08`、`归档/` 的定义与数值；只在 `10 探索/` 新增本文并给相关旧稿加指针（保留原文）。

---

## 附：脚本与数据

- 脚本：`10 探索/.calc/fgt_optical_two_stage_audit.py`（已 gitignore）
- 文献底稿：`10 探索/.calc/homes_06.txt`（Homes Physica C 2006 pdftotext 提取，已 gitignore）
- 第一性验证：(F.3) $f_c=n_s/n$ 三档 `match=True`；分离比 (F.6) 汞系三档
- 全部外部文献 FT1–FT7 带 DOI/arXiv，作者/数值已逐一核对原文
