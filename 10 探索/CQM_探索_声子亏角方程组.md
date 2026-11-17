# CQM 探索：声子 ↔ 亏角方程组的建立

> **定位**：探索稿（非权威源）。本轮回答"如何建立声子和亏角的方程"——把前几轮成果（严格段、一般晶格剖分、稳定性判据）收束为一套**分层方程组 (E1)–(E7)**，用 cot 拉普拉斯 $L$ 的本征模把声子简正模与亏角涨落统一到同一组基底上。全程 CQM 内生；外部文献仅对照，不引入作 CQM 已证内容。
>
> **外部检索（承 AGENTS §〇，仅对照）**：亏角量子化（isolated horizon, gr-qc/0005126：亏角在 prequantization 下量子化、Gauss–Bonnet 量子类似）；Regge 二阶变分 $\delta^2S=\delta_iM_{ij}\delta_j$、零模对应规范涨落（gr-qc/0012035 §C）；线性化亏角 $\delta\tilde\epsilon_t=\varepsilon(\partial\tilde\epsilon_t/\partial l^e_k\,y^e_k+\cdots)$（arXiv:1411.5672 式 8.3）——后者与本轮 (E5) 结构同构，仅作对照。

**日期**：2026-11-17

---

## 0. 建立方程组的思路

骨架里声子（§1–§2）与亏角涨落（§3）本是两条表述，靠"A4 本征向量 $v_k(v)$"和"系数来源未导出的 $\hat\varepsilon^{(1)}$"松散连接。本轮用**一般晶格的 cot 拉普拉斯 $L$** 作统一桥梁：

- $L$ 的本征向量＝简正模式 $U_{kv}$（声子的模式来源，晶格 ≠ A4）
- $L$ 的本征值＝$\omega_k^2$ 的几何来源（比例系数待推 W-3）
- 亏角 $\varepsilon_e$ 与 $L$ 由同一组二面角 $\theta_e$ 定义 → 声子与亏角共用同一组本征模

这样方程组不再是两套脱节的构造，而是一组自洽的几何-量子方程。

## 1. 方程组 (E1)–(E7)

### 第一层：声子（严格段，承 `CQM_探索_位置动量到声子_严格段.md`）

**起点**（正则对易，权威源声子理论 §1.2 记作"顶点正则对易"）：

$$[\hat X_v,\hat P_{v'}]=i\hbar\,\delta_{vv'}.\tag{E1}$$

> **术语边界**：本方程组的基本单元是**节点（node）**（关系网络的位点）。**亏角都是节点之间（铰链）的量**，不存在"节点自身亏角"；固有时流速与耦合常数定义在节点上，由相邻节点间的边亏角经比值关系定。E1 沿权威源 §1.2 记为"顶点"对易，此处 $v$ 是 Regge 复形位点（几何角点）；"顶点角亏"专属于该角点、与固有时流速无关（FG_核心理论 §3.1），不与节点间亏角 $\varepsilon$ 混同。

**简正模式**（$U$ 取 $L$ 的本征向量，$UU^{\mathsf T}=I$）：

$$\hat Q_k=\sum_v U_{kv}\hat X_v,\quad \hat\Pi_k=\sum_v U_{kv}\hat P_v\ \Longrightarrow\ [\hat Q_k,\hat\Pi_{k'}]=i\hbar\delta_{kk'}.\tag{E1'}$$

**声子算符**（玻色对易严格）：

$$\hat a_k=\sqrt{\frac{m\omega_k}{2\hbar}}\hat Q_k+i\sqrt{\frac{1}{2m\hbar\omega_k}}\hat\Pi_k,\qquad [\hat a_k,\hat a_{k'}^\dagger]=\delta_{kk'}.\tag{E2}$$

**位置涨落**（§2.2，声子的线性叠加）：

$$\Delta\hat X_v=\sum_k U_{kv}\sqrt{\frac{\hbar}{2m\omega_k}}(\hat a_k+\hat a_k^\dagger).\tag{E3}$$

### 第二层：亏角（几何，承 `CQM_探索_一般晶格几何剖分建模.md`）

**几何亏角**（铰链 $e$，由二面角/余弦定律严格确定）：

$$\varepsilon_e=2\pi-\sum_{T\supset e}\theta_e^{T},\qquad L_{ij}\big|_{i\ne j}=-\tfrac12\sum_{T\supset e_{ij}}\cot\theta_{e_{ij}}^{T}.\tag{E4}$$

**亏角涨落算符**（位置涨落经边长投影进入亏角，链规则）：

$$\Delta\hat\varepsilon_e=\sum_{e'}\frac{\partial\varepsilon_e}{\partial l_{e'}}\,\Delta\hat l_{e'},\qquad \Delta\hat l_e=(\Delta\hat X_{v_i}-\Delta\hat X_{v_j})\cdot\hat t_e.\tag{E5}$$

**二阶矩（真空涨落幅度）**（把 (E3) 代入 (E5)，$n_k=\langle\hat a_k^\dagger\hat a_k\rangle$）：

$$\langle(\Delta\varepsilon_e)^2\rangle=\sum_k\Bigl(\frac{\partial\varepsilon_e}{\partial l}\Bigr)^2 U_{kv}^2\,\frac{\hbar}{m\omega_k}\Bigl(n_k+\tfrac12\Bigr)\ \xrightarrow{n_k=0}\ \Delta\varepsilon_0^2.\tag{E6}$$

### 第三层：温度（骨架 §9.2、超导核心）

$$\Delta\varepsilon(T)=\Delta\varepsilon_0\sqrt{\tanh\frac{\hbar\Omega_0}{2k_BT}},\qquad \omega_k^2=c_0\,\lambda_k(L).\tag{E7}$$

$\lambda_k(L)$ 是 $L$ 本征值，$c_0$ 为频率标度系数（待推 W-3）。

## 2. 方程组的结构意义

| 连接 | 此前状态 | 本轮方程组 |
|:---|:---|:---|
| 声子模式来源 | 骨架 §1.2 "由 $A_4$ 本征向量确定"（与晶格脱节）| $L$ 本征向量（一般晶格，晶格 ≠ A4）|
| $\omega_k$ 来源 | §1.2 "频率待推" | $L$ 本征值 × 系数 $c_0$（几何来源明确，系数待推）|
| 亏角涨落系数 | §3.1 "框架设定，来源未导出" | (E5) 链规则 $\partial\varepsilon/\partial l$，(E6) 二阶矩 |
| 声子-亏角一致性 | 两套脱节构造 | 同一组 $L$ 本征模统一 |

**关键**：(E6) 是声子与亏角的定量接口——它把上一轮定位的"位置涨落平方 $\propto1/\omega_k$ 与骨架公式 $\propto\omega_k$ 依赖相反"的矛盾，落实为明确的二阶矩表达式，缺口集中到 $c_0$ 与 $\partial\varepsilon/\partial l$ 两个待推系数上，不再模糊。

## 3. 数值闭合检验（承 `cqm_analysis/lattice_regge_model.py`）

BCC-Nb 晶格（54 原子，213 四面体）：

| 检验 | 结果 | 判定 |
|:---|:---|:---|
| $U$ 正交归一性 $\max\lvert U^{\mathsf T}U-I\rvert$ | $2.0\times10^{-15}$ | (E1') 严格成立 |
| $L$ 本征模 | 1 零模 + 53 正模 | 稳定声子基底（承稳定性判据）|
| 零点方差 $\sum_k 1/(2\omega_k)$ | 2.41（有限）| (E6) 可定义 $\Delta\varepsilon_0^2$ |
| 低频模主导 | $\omega_k$ 范围 $[2.8,483]$，低频方差大 | 声学模主导，与 §11.14 "元素超导体 $f\approx0.5$ 声学模主导"一致 |
| (E7) 温度极限 | $T\to0$: ratio→1；$T=300$K: 0.36 | 极限正确 |

## 4. 边界（不得升级）

| 环节 | 状态 |
|:---|:---|
| (E1)–(E3) 声子层 | 【严格】不依赖 $U$/$\omega_k$ 来源（承上轮严格段）|
| (E4) 几何亏角 + cot $L$ | 【几何严格＋构造】$|\cot|$ 稳健化是构造选择 |
| (E5) 链规则 | 【条件严格】给定 $\partial\varepsilon/\partial l$ |
| (E6) 二阶矩 | 【结构严格】形式严格，$\partial\varepsilon/\partial l$、$c_0$ 待推 |
| (E7) 温度 | 【条件严格】骨架 §9.2 既有 |
| $c_0$、边长→亏角转换系数 | 【待推 W-3】不闭合绝对值 |
| $\Delta\varepsilon_0^2$ 双尺度分解（式 1602）| 【待推 W-3】需 inter/intra 几何输入，本轮未闭合绝对值 |

## 5. 成果登记与迭代定位

| 成果 | 内容 | 状态 |
|:---|:---|:---|
| **T1** | 建立声子 ↔ 亏角分层方程组 (E1)–(E7)，用 $L$ 本征模统一声子简正模与亏角涨落 | 【方程组建立】CQM 内生 |
| **T2** | 声子模式来源从脱节的"A4 本征向量"改为一般晶格 $L$ 本征向量（晶格 ≠ A4）| 【脱节消除】|
| **T3** | 声子-亏角定量接口落实为二阶矩 (E6)，缺口集中到 $c_0$、$\partial\varepsilon/\partial l$ 两系数 | 【接口明确化】|
| **T4** | 数值检验 (E1')/(E6)/(E7) 自洽；低频模主导与"声学模主导"一致 | 【数值检验】|

**迭代结论**：本轮完成"如何建立声子和亏角方程"——一套分层、自洽、边界清晰的方程组。它把前几轮的严格段、晶格剖分、稳定性判据收束为可用形式，并把缺口精确集中到两个待推系数（W-3），不再绕过。下一步可沿两条路线：
1. 从 Regge 二阶变分结构尝试导出 $\partial\varepsilon/\partial l$ 与 $c_0$（闭合 W-3 的第一步，接 W-3 缺口）；
2. 把 (E6) 的 $\Delta\varepsilon_0^2$ 接到节点间差异方差 $\langle(\delta C_{ij})^2\rangle$（超导核心 DM.5–DM.6），贯通"声子→亏角→配对"通道。

未动 01–07 权威源；所有构造选择、待推系数如实登记。待续。
