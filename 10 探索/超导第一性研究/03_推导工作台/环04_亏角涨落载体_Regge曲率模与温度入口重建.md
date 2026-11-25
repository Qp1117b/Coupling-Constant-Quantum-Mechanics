# 环 4（`审-21` 后续）：亏角涨落的载体确立——Regge Hessian 的规范零模与曲率激发，温度入口 (4.1′) 重建

**轮次**：第 87 轮补（承接 R73；2026-11-24）；成果登记编号 R-96（与既有 R-87「f 斜率」不同编号序列，勿混）
**性质**：补缺口 `审-21` 的**载体与温度结构**（不改状态栏、不动 06／01／08／研究站）；改的是**方程载体**，不是数值。
**外部文献**（对照工具，非 CQM 已证）：
- Dittrich–Steinhaus, *Path integral measure and triangulation independence in discrete gravity*, arXiv:1110.6866，§2 (2.5)–(2.9)：平直背景上边长扰动 $l_e=l_e^{(0)}+\lambda_e$ 的二阶展开 $S=S^{(0)}+\tfrac12 H_{ee'}\lambda_e\lambda_{e'}$，$H_{ee'}=-\partial\omega_e/\partial l_{e'}$（3D，Schläfli 恒等式）。
- Dittrich, *Diffeomorphism symmetry in quantum gravity models*, arXiv:0810.3594，§4 式 (4.2)–(4.5)：平直背景上顶点位移诱导的边长变分 $Y_I^e=\vec B_I\!\cdot\!\vec E^e/|\vec E^e|$ 满足 $Y_I^e\,\partial\epsilon_\Delta/\partial l^e|_{\rm flat}=0$，故 Hessian 退化、$Y_I$ 是零模（离散微分同胚残余）。
- Bahr–Dittrich, *From covariant to canonical formulations of discrete gravity*, arXiv:0912.1817，§4：同上命题，$Y_I^eH_{ee'}=0$。
- Baez–Catalan–Dittrich–Walsh, PRD **76**, 104020 (2007) 与 PRD **91**, 124034 (2014)：非零本征方向是传播的曲率激发（lattice graviton）。

> 以上只提供**标准工具的结构**（哪些模承载曲率、二阶作用量给热统计），不写成 CQM＝量子引力，不构成还原（哲学 §0.2 结构同构不是还原）。

---

## 一、前件（这一步必须已成立的东西）

1. **R73 的定理级判定**：固定组合的三角化嵌入 $\mathbb R^3$ 时，绕内部铰链的二面角和恒为 $2\pi$，故 $\varepsilon_e\equiv0$，与顶点位移无关；$\delta\ell=\delta\ell^{\rm emb}\oplus\delta\ell^{\rm intr}$，$\varepsilon$ 只由 $\delta\ell^{\rm intr}$ 承载（数值 $\max|A|=4.0$、$\|A\|_F=29.65$）。
2. **链内温度唯一入口的既定约束**：全链只有 (4.1) 的 $[1+2n_B(\omega_k)]$ 含 $T$（AGENTS §2）；任何温度依赖必须来自这一结构。
3. **`审-21` 原状**：R73 登记"内禀扇区的统计与温度入口链内无载体"——本轮补的正是这个载体，**不改编号与状态**。

> 前件核查（十问第 4 问）：本环前件只含环 3 的亏角定义、R73 的两扇区分解与 (4.1) 的热结构，**不含相变后对象**（$A_\tau$、$\mathcal H_{ij}=c_{ij}$），无循环。

---

## 二、式（这一步生成什么）

**(A) 位移模是 Hessian 零模——载体判据**

记 $A_{ee'}=\partial\varepsilon_e/\partial l_{e'}$（R73 的几何传递）。平直背景上顶点位移诱导的边长变分 $Y_I^e$ 满足（arXiv:0912.1817 式 (4.3)，外部标准工具）

$$Y_I^e\,A_{e e'}\big|_{\rm flat}=0,\qquad H_{e e'}=-\sum_\Delta\frac{\partial A_\Delta}{\partial l^{e'}}\frac{\partial\varepsilon_\Delta}{\partial l^e}\Big|_{\rm flat}\ \Longrightarrow\ Y_I^e H_{e e'}=0. \tag{4.1a}$$

即 $\delta\ell^{\rm emb}\in\ker H$ 是**规范零模**：亏角对其盲（R73 位移盲性的 Hessian 表述）。

**(B) 曲率激发模与二阶作用量**

在 $\ker H$ 的正交补上取本征基 $H v_k=k_k v_k,\ k_k>0$；令 $\xi_k=v_k\cdot\delta\ell^{\rm intr}$。线性化 Regge 作用量给（arXiv:1110.6866 式 (2.6)，外部标准工具）

$$S^{(2)}=\tfrac12\sum_k k_k\,\xi_k^2,\qquad \omega_k=\sqrt{k_k/m_{\rm eff}}>0. \tag{4.1b}$$

**(C) 每个曲率模的热方差——$[1+2n_B]$ 的恢复**

对玻色二次模，$n_B(\omega_k)=\bigl(e^{\hbar\omega_k/k_BT}-1\bigr)^{-1}$，零点振幅 $c_k^0=\hbar/(2\sqrt{k_k m_{\rm eff}})\ge0$：

$$\langle\xi_k^2\rangle_T=c_k^0\Bigl[1+2n_B(\omega_k)\Bigr]=c_k^0\coth\frac{\hbar\omega_k}{2k_BT}. \tag{4.1c}$$

**(D) 亏角热方差（(4.1) 的载体订正）**

$$\boxed{\ \langle(\Delta\varepsilon_e)^2\rangle_T=\sum_k\bigl|A\cdot v_k\bigr|_e^2\,c_k^0\Bigl[1+2n_B(\omega_k)\Bigr]\ }\tag{4.1′}$$

与 R73 的 $\sum_{e'}A_{ee'}^2\langle(\delta\ell^{\rm intr}_{e'})^2\rangle$ 逐项对应：$|A\cdot v_k|_e^2$ 是几何传递权重，方括号是热占据。**结构完全等同 (4.1)，只把载体从位移模换成非规范曲率模。**

**(E) 温度入口的三条可检性质**

$$1\le \frac{\langle(\Delta\varepsilon_e)^2\rangle_T}{\sum_k|A\cdot v_k|_e^2c_k^0}\le 1+\frac{2k_BT}{\hbar}\sum_k\frac{|A\cdot v_k|_e^2c_k^0}{\sum_j|A\cdot v_j|_e^2c_j^0}\,\frac{1}{\omega_k}\ \ (T\to\infty\ \text{线性}) \tag{4.1d}$$

$$\frac{\partial}{\partial T}\langle(\Delta\varepsilon_e)^2\rangle_T>0,\qquad T\to0:\ \langle(\Delta\varepsilon_e)^2\rangle_0=\sum_k|A\cdot v_k|_e^2c_k^0>0. \tag{4.1e}$$

(4.1d) 上界用 $e^x\ge1+x$（$x=\hbar\omega_k/k_BT>0$）；零点项有限正值，解决 R73 前"(4.1) 恒为零"的危机。

---

## 三、依据（为什么这样改）

1. **R73 给了危机的根因**（被归一的量本身为零），本轮不给它"补一个归一系数"，而是换载体——符合 AGENTS §3"不绕过"：断口在载体，不在系数。
2. **位移盲性与 Hessian 零模是同一件事**：R73 的数值定理（位移不改亏角）↔ 外部文献的规范零模（$Y_I^eA_{ee'}=0$）。两者逐字对应，故 R73 的"内禀扇区"可精确定义为 $\ker H$ 的正交补（曲率激发子空间）——这是**链内结构可承载**的，不是凭空新自由度。
3. **$[1+2n_B]$ 不是外借**：它是 (4.1) 原有的热结构。玻色二次模的方差本就取该形式（与环 4 原有的零点项 $\hbar/2\rho\omega$ 同源），故温度入口的**唯一性未被破坏**——没有第二处 $T$ 进入。
4. **量纲核对**：$[A]=1/L$（R71），$[c_k^0]=L\cdot(\text{弧度})^2$（弧度无量纲），故 $[\langle(\Delta\varepsilon)^2\rangle]=(\text{弧度})^2$，与 (4.1) 一致；$\hbar\omega_k/k_BT$ 无量纲。

---

## 四、极限、单调性、可证伪条件

| 检查 | 结果 | 判据 |
|:---|:---|:---|
| 零点极限 $T\to0$ | $\sum_k|A\cdot v_k|^2c_k^0>0$（有限） | 否证 R73 前"恒为零" |
| 高温极限 $T\to\infty$ | $\langle(\Delta\varepsilon)^2\rangle_T\propto T$（古典等分） | 与 (4.1) 同向；升温涨落增 |
| 单调性 | $\partial\langle(\Delta\varepsilon)^2\rangle_T/\partial T>0$（$c_k^0>0$） | 升温利于配对前夜（与 `审-3` 方向一致） |
| **可证伪** | 若实验测到亏角相关涨落随 $T$ **下降**或与 $T$ 无关，则载体判定被否证 | 需独立测内禀亏角涨落（FG 侧），当前链内无此读数 |
| 零模排除 | 位移模权重 $|A\cdot Y_I|^2=0$，不进 (4.1′) | 数值已在 R73 验证（$\le1.8\times10^{-15}$） |

---

## 五、历史唯物主义合规（用户明确要求"必须复合历史唯物主义"）

1. **基础决定上层建筑**：Regge Hessian 的本征结构（哪些模是规范零模、哪些是曲率激发）属**几何基础／存在层**；热占据 $[1+2n_B]$ 是施加于其上的**温度读数／上层建筑式量**。基础决定读数的定义域（零模不进读数），读数反作用只改数值不改结构——不是互相还原。
2. **必然性与偶然性的统一**：**必然性**＝Hessian 零模空间由几何固定（位移必为规范模，曲率激发必为非零本征模，回溯必然）；**偶然性**＝具体 $\{k_k,\omega_k,c_k^0\}$ 取值与哪些模被热占据由材料与制备决定（前瞻偶然）。二者分层统一。
3. **结构同构不是还原**：借用线性化 Regge 的 Hessian 作为标准工具表达载体，**不声称** CQM＝量子引力、不声称两系统互相推导（哲学 §0.2）。
4. **未用社会范畴作物理证据**：先锋队／公有制等只进 §14.1【诠释】，本卡不引用。
5. **不能推出什么**（必填栏）：① $\omega_k,k_k,c_k^0$ 的绝对值（材料／FG 外生，`E4`）；② 内禀扇区是否真的热化、以何时间尺度热化（FG 动力学，链内无载体）；③ 哪个模先被占据（`审-10` 截断位置，仍未定）；④ 绝对 $T_c$（命题 Z2 外生能标）；⑤ 不证明 RH、不碰 `临-8`／`临-22`。

---

## 六、状态与缺口

- **状态**：本卡是【构造】载体识别＋【标准数学】（零模定理）＋【条件严格】（热方差形式），**状态栏不动**。
- **`审-21` 推进**：从"载体未知、(4.1) 恒为零"推进为"载体＝非规范曲率激发模（$\ker H$ 正交补），(4.1′) 温度入口以 $[1+2n_B]$ 结构恢复，规范零模被排除"。**残余**：模谱与材料归一外生 ⇒ `审-21` **仍不闭合**（不升状态、不改编号）。
- **不动**：`审-10`、`审-3`、`W-3′`、`E4`、命题 Z2 状态原样；06 §4 的 $G_{ek}$"几何投影"表述**仍待与 06 对账**（只登记不改）。

---

## 七、Lean 状态

`05_Lean验证/ReggeCurvatureModes.lean`：
- `nB_pos`、`thermalFactor_ge_one`、`thermalFactor_le_linear`（古典等分上界）、`thermalFactor_strictMono`（升温涨落增）、`sigmaSq_pos`、`sigmaSq_mono`、`gauge_mode_zero_weight`（规范零模不进读数）、`sigmaSq_zero_point`（零点有限正值）——共 8 条定理。
- 无 `axiom`／`sorry`／`admit`／`native_decide`／`unsafe`；`lake env lean` 退出码 0（见决策记录）。

## 八、复现命令

```bash
cd "08 理论组织和形式化框架/04_Lean对接/Lean源码"
lake env lean "../../../10 探索/超导第一性研究/05_Lean验证/ReggeCurvatureModes.lean"
python "10 探索/超导第一性研究/04_计算验证/环04_Regge曲率模温度入口.py"
```
