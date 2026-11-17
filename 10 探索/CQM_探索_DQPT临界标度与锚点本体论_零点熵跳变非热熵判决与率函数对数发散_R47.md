# CQM 探索：DQPT 临界标度与锚点本体论——零点熵跳变"非热熵"判决、率函数对数发散与 R46 细化——R47

> **定位**：探索稿（非权威源），v0.1，2026-11-17，第二十五轮（DQPT 线第二稿）。承接上一稿 R46（对数谱热浴＝记忆核实现层候选），本轮处理 R46 留下的一处**表观张力**：Wei et al. 报零点处熵跳变（类一级），而 CQM 第十七轮已严格给出 $T_c$ 处 $\Delta C=0$（3D XY，R33）、熵在更高 $T^*$ 释放。本轮用 DQPT 临界标度理论与严格计算判定二者是否冲突，并据此**细化 R46**。
>
> **三条不宣称**：不宣称证 RH；不宣称从 CQM 公设推出 BCS；不宣称真实超导材料就是该工程热浴。本轮新增一条【定理级】微观推导（率函数对数发散的微观来源）、一条【构造】通道判决与判据 R47。
>
> **克制拟合声明**：全文零可调参数、无最小二乘。三处数值均为定理的直接检验（Taylor 线性消失、$\lvert\zeta'(\rho_n)\rvert$ 标度、零点间距渐近），脚本在 `.calc/dqpt_critical.py`（gitignore）。凡"相容/一致"均标明，不冒充验证。

---

## 第零部分：一句话结论

Wei et al. 零点处的熵跳变是**动力学熵**（由率函数 $F_1(\beta,t)$ 定义，探针相干的时间结构），不是平衡热熵——故与 CQM 的 $T_c$ 处 $\Delta C=0$（3D XY）**不冲突**：DQPT 须用动力学探针（探针相干/回响）检验，不能用平衡比热。严格地，累积相位因子在零点处**线性消失**（$\lvert\eta\rvert/\lvert\delta t\rvert\to\lvert\eta'(\rho_n)\rvert$），给出率函数 $-\ln\lvert t-\gamma_n\rvert$ 型对数发散（临界指数 0），这与 CQM"相变＝锚点出现"的事件性本体论同构，而与 Landau 连续对称破缺不同。据此**细化 R46**：零点 DQPT 绑定的是"锚点出现"这一事件本身，其动力学指纹（回响/率函数）独立于平衡热力学指纹（$\Delta C$）。新增 R47。

---

## 第一部分：外部文献（逐条标源，与 CQM 构造分栏）

| 编号 | 文献（含出处） | 外部结论 | 与 CQM 的接口 |
|:---|:---|:---|:---|
| **W1** | S. Wei et al., *Nat. Commun.* **17**, 8163 (2026), DOI:10.1038/s41467-026-74935-8, arXiv:2511.11199 | 零点处熵密度 $\mathscr S$ 反号跳变、$F_1$ 非解析；零点下方相干丢失/信息内流，上方信息倒流/再相干 | 本轮判定对象：该熵是否热熵 |
| **W7** | J. Li et al., "Critical exponent of dynamical quantum phase transitions…", *Phys. Rev. Lett.* (2025), DOI:10.1103/rwln-wbs1 | Loschmidt 回波呈 cusp 奇异性、率函数对数发散、临界指数为零 | 率函数对数发散的普适标度；与"锚点＝事件"同构 |
| **W8** | 同 W7 类；另 arXiv:2609.18208（双畴壁费米子 DQPT 对数奇异性）、arXiv:2504.00483（有限尺寸 Loschmidt 零点） | 对数奇异性在多类模型中重现；有限尺寸下回波零点可观测 | 普适性佐证，非 CQM 独有 |
| **W9** | M. B. Milinovich, "Upper bounds for the moments of $\zeta'(\rho)$", arXiv:0806.0786 (2008) | RH 下 $\lvert\zeta'(\rho)\rvert$ 的 $2k$ 阶矩上界；$\log\lvert\zeta'(\rho)\rvert$ 近似对数正态/缓慢增长 | 脉动峰幅度 $\lvert\eta'(\rho_n)\rvert$ 的标度依据 |
| **W3** | 同 R46 第一部分（Berry–Keating 1992；Sierra） | 零点谱迹公式与质数震荡 | 承接，不重复 |

> **分栏**：以上全部为外部结论，未经 CQM 证实，只作对照；CQM 构造结论见第二、三部分并明确分级。

---

## 第二部分：定理级推导——率函数对数发散的微观来源

### §2.1【严格·定理直接检验】回波幅度线性消失

由 R46 式 (R46.1)，$\mathcal L(\tfrac12,t)\propto\eta(\tfrac12+it)$。在零点 $\rho_n=\tfrac12+i\gamma_n$ 处 Taylor 展开：

$$
\eta(\tfrac12+i(\gamma_n+\delta))=\eta'(\rho_n)\,i\delta+O(\delta^2),\qquad
\frac{\lvert\eta\rvert}{\lvert\delta\rvert}\ \xrightarrow{\delta\to0}\ \lvert\eta'(\rho_n)\rvert.
\tag{R47.1}
$$

数值核验（脚本 A 段，30 位）：$\gamma_1=14.1347251417$，$\lvert\eta'(\rho_1)\rvert=1.882696711$；$\delta=10^{-2},10^{-3},10^{-4},10^{-5}$ 时比值 $1.88303,1.88273,1.88270,1.88270$——收敛到 $\lvert\eta'(\rho_1)\rvert$。**严格**：这是 Taylor 定理的直接数值检验，非拟合、非 CQM 独有定理。

### §2.2【严格·承接 W7】率函数对数发散

率函数（取标准 Loschmidt 归一化 $\lambda(t)=-\lim_N N^{-1}\ln\lvert\mathcal G\rvert^2$，注意 Wei 的 $F_1$ 用 $1/\ln N$ 归一化，奇异性同型但标度不同——诚实登记此差异）：由 (R47.1)，$\lvert\mathcal L\rvert\sim\lvert\eta'(\rho_n)\rvert\lvert t-\gamma_n\rvert$，故

$$
\lambda(t)\ \sim\ -2\ln\lvert t-\gamma_n\rvert+\text{const}\quad (t\to\gamma_n),
\tag{R47.2}
$$

即**对数发散的 cusp**，序参量（回波凹陷深度）临界指数为 0（幅度本身连续到零但导数不连续；W7 的"指数零"指此型 cusp）。这与 W7/W8 多模型中重现的对数奇异性同型。**严格**其数学来源（线性消失 → $-\ln$ 发散）；**外部**其普适类归类（W7）。

### §2.3【构造·本轮新判据素材】脉动峰幅度 $\lvert\eta'(\rho_n)\rvert$

由 $\eta'(\rho_n)=(1-2^{1/2-i\gamma_n})\zeta'(\rho_n)$，且 $\lvert1-2^{1/2-i\gamma_n}\rvert\in[0.414,\,2.414]$ 有界振荡，故幅度标度由 $\lvert\zeta'(\rho_n)\rvert$ 主导。数值（脚本 B 段，前 20 零点）：$\lvert\zeta'(\rho_n)\rvert$ 从 $0.793$（$n=1$）增长到 $1.46$–$2.96$（$n=11$–$20$），$\log\lvert\zeta'\rvert$ 在 $-0.23$ 到 $+1.09$ 间——缓慢（近对数、伴对数正态涨落）增长，与 W9 一致。

> **与 R30 的区分（重要，避免混同）**：R30 的深度斜率 $C_n=\lvert\zeta'(\rho_n)\rvert/\lvert\zeta(\tfrac12+i\tau_m)\rvert$ 与本轮的脉动峰幅度 $\lvert\eta'(\rho_n)\rvert$ 虽共享分子 $\lvert\zeta'(\rho_n)\rvert$，但**对象不同**——$C_n$ 是记忆核极小随 $q$ 变化的临界斜率（R1″），$\lvert\eta'(\rho_n)\rvert$ 是回波 cusp 的高度（DQPT）。两者不互相推导；本轮不翻 R30 的任何结论。

---

## 第三部分：表观张力的判决与 R46 细化

### §3.1 熵跳变"非热熵"判决

| 量 | Wei et al. 的 $\mathscr S$ | CQM 的 $T_c$ 比热（R33） |
|:---|:---|:---|
| 定义 | $\mathscr S=-\partial_T(\beta^{-1}F_1)$，$F_1$ 由探针相干 $\mathcal L$ 定义 | 平衡自由能二阶导 $\Delta C$ |
| Plane | $(\beta,t)$ 动力学平面（固定演化时 $t$，扫 $\beta$） | 热平衡温度轴（扫 $T$） |
| 物理 | 信息倒流/相干换向（动力学量） | 熵对温度的响应（平衡热力学量） |
| 跳变 | 零点处反号跳变 | $\Delta C=0$（$\alpha=-0.0151<0$，连续 cusp） |

**判决**：二者是**不同平面的不同量**，$\mathscr S$ 不是平衡热熵，故零点熵跳变与 $\Delta C=0$ **不矛盾**。把 $\mathscr S$ 误读为热熵会得出"DQPT＝一级相变"的错误结论——这是本轮要防的误读。

### §3.2 R46 细化（本轮核心推进）

R46 原文把"零点＝锚点出现"对接到两阶段相位通道（$T_c$），未区分指纹类型。本轮细化为：

$$
\boxed{\ \text{零点 DQPT}=\text{锚点出现（事件性本体论）};\quad
\text{其指纹}=\text{动力学的（}\mathcal L\text{ 回响/率函数 cusp）};\quad
\text{平衡}\Delta C=0\text{ 与它测不同对象}.\ }
\tag{R47.3}
$$

- **锚点本体论同构**：CQM 把相变定义为"锚点出现"（$K^{\rm SC}$ 在 $T_c$ 从零变非零，§0.7），是事件性、非 Landau 连续对称破缺；DQPT 的"指数零、对数 cusp、回波凹陷"正是事件性（临界时刻才出现、之前无 precursors 的序参量增长）。两者结构同构（【构造】）。
- **指纹分离**：动力学指纹（R47a/b）与平衡热力学指纹（R33 $\Delta C=0$）测不同对象，互不推导、互不冲突。一个 $x=T^*/T_c-1$ 仍统一平衡侧诸投影（R36/R40/R42），本轮不改。

### §3.3 理想模型与图像：cusp 森林

```
  |L| (回波幅度)
  1 ┤╲    ╲    ╲    ╲
    │ ╲    ╲    ╲    ╲
  0 ┤  ●    ●    ●    ●        ← 零点 γ_1,γ_2,γ_3,γ_4：|L|=0（线性消失）
    ─┴───┬────┬────┬────┬──→ t
        γ_1  γ_2  γ_3  γ_4
  λ(t)  -ln|t-γ_n| 型 cusp 森林（每个零点一根向下无穷的对数尖峰）
  cusp 高度 ∝ |eta'(rho_n)| ∝ |zeta'(rho_n)| （缓慢对数增长）
```
**图像读法**：回波幅度在每个零点**触底**（线性），率函数因此在每个零点生出一根对数尖峰——"cusp 森林"。锚点出现＝尖峰出现，是事件；两阶段配对/相位是平衡侧的温区划分，二者不在同一图。

---

## 第四部分：可证伪判据 R47（与 R1″/R32/R42 测不同对象）

- **R47a（线性消失/率函数对数 cusp）**：在对数谱热浴探测中，$\mathcal L$ 在 $t=\gamma_n$ 处的凹陷须线性（$\lvert\mathcal L\rvert/\lvert\delta t\rvert\to$ 常数 $\lvert\eta'(\rho_n)\rvert$），率函数呈 $-\ln\lvert t-\gamma_n\rvert$ cusp。若凹陷为二次（$\lvert\mathcal L\rvert\sim\delta t^2$）或无 cusp，则"锚点＝DQPT 事件"结构在该装置被证伪。
- **R47b（cusp 高度标度）**：第 $n$ 根 cusp 高度须 $\propto\lvert\eta'(\rho_n)\rvert\propto\lvert\zeta'(\rho_n)\rvert$（缓慢对数增长、对数正态涨落，W9）。若高度随 $n$ 按幂律 $\gamma^{\pm p}$ 系统漂移，则本轮的峰幅度识别失败（与 R30 深度斜率不同）。
- **R47c（动力学/平衡指纹分离）**：同一材料在 $T_c$ 附近应同时满足——动力学探针见零点关联回响（R47a/b），平衡比热 $\Delta C=0$（R33）。若平衡比热出现尖锐一级跳变（$\Delta C>0$ 有限），则 3D XY 相位支图像（R33）被否，本轮"指纹分离"随之失效；若动力学探针无回响但平衡正常，则 DQPT 实现层候选对该材料不适用（不动摇两阶段本身）。

> 与 R1″（深度随温度→100%）、R32（普适类三通道）、R42（NMR 自旋）各自独立：R47 测回波的**时间域 cusp 结构与峰幅度标度**。

---

## 第五部分：退化守住（逐项核对）

| 对象 | 本轮处理 |
|:---|:---|
| BCS（DM.23–24） | 不变：本轮只给动力学 cusp 结构，未碰能隙方程与 $2\Delta/k_BT_c$ |
| 迈斯纳（R37） | 不变：平衡刚度未触碰 |
| 比热 R33/$\Delta C=0$、R34/R35 | 不变；本轮判决 $\mathscr S$ 非热熵，恰**保护** R33 不被误读 |
| Z2/Z3 | 不变：$\gamma_n,\eta',\zeta'$ 全无量纲；$t$ 的绝对定标仍外生 $\varepsilon_0/\hbar$ |
| R30/R32/R42、R46、M1–M9、缺口 C/G/N/H | 全部不变；R46 被细化（指纹类型分离），非推翻 |
| 质数层 Poisson / 零点层 GUE | 不变 |

---

## 第六部分：边界与开放问题

1. **归一化差异**（诚实登记）：Wei 的 $F_1$ 用 $1/\ln N$、标准 Loschmidt 率函数用 $1/N$，对数奇异性同型但前因子与有限尺寸标度不同；不把两者数值混用。
2. **$\mathscr S$ 非热熵的判决范围**：本轮判定仅针对 W1 定义的 $\mathscr S$（由 $F_1$ 经 $\partial_T$ 得到）；若 W1 后续把 $\mathscr S$ 明确等同平衡熵，需重新审计。
3. **$\lvert\zeta'(\rho_n)\rvert$ 严格上界**：W9 给 RH 下矩上界；本轮数值为具体零点取值，非上界证明。
4. **M1 仍未闭合**：本轮细化 R46 的指纹类型，未证真实材料通道、未证两条 $\gamma_n$ 通道同一。
5. **RH 未证**：W7/W9 均为条件（RH/GUE）结果；本轮不宣称证明 RH。
6. **文档处理**：本轮未发现需删除的"不对劲"文档；R46 以"细化指针"方式处理（非删除、非推翻），符合项目纠错惯例。物理删除须作者确认，本轮不删任何文档。
7. **未做**：lean、网站、完整理论文档、任何参数拟合。

---

## 参考文献（外部，逐条核实出处；CQM 构造见正文分栏）

- [W1] S. Wei et al., *Nat. Commun.* **17**, 8163 (2026), DOI:10.1038/s41467-026-74935-8; arXiv:2511.11199.
- [W7] J. Li et al., "Critical exponent of dynamical quantum phase transitions…", DOI:10.1103/rwln-wbs1 (2025).
- [W8] arXiv:2609.18208; arXiv:2504.00483（DQPT 对数奇异性/有限尺寸回波零点）。
- [W9] M. B. Milinovich, arXiv:0806.0786 (2008).
- [W3] M. V. Berry & J. P. Keating, *Proc. R. Soc. A* **437**, 151 (1992); S. Sierra, arXiv:1003.0934.
- CQM 侧：DM.17、DM.19、§0.6–§0.7 见 `06 超导/CQM_超导核心理论.md`；R33–R35 见 `CQM_探索_比热跳变的两阶段判决_3DXY无跳变与赝能隙提前释放熵.md`；R1″ 见 `CQM_探索_记忆核零点深度的相变判据_谱刚性纠错.md`；R30/R32/R42 见对应探索稿；R46 见上一稿。
