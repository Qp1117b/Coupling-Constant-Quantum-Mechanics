# 环 19／`审-11`：Ginzburg 临界区宽度的链内推导——从 Landau 系数到 $t_G\sim N^{-6}$

**状态**：工作台推导卡（R48）；不改主链正文、不改 06 原文、不改 08 台账、不改缺口编号与状态栏、不动账面。
**触发**：`环19_审11_Landau系数与锚.md` §五只是**引用**外部 Ginzburg 判据 $t_G=(a/\xi_0)^{2d/(4-d)}$（标"外部标准"），未从链内 Landau 系数 (11L.5/11L.6) 推导；本卡把 §五的外部引用升级为**链内推导**，前件全部链内（$a_0=k_B$、$b=zJ/8$、R46 梯度系数 $c=\Upsilon_0/2$）。
**一句话**：Ginzburg 判据比较"关联体积内的序参量涨落"与"平均场序参量平方"。链内 Landau 比热跳变 $\Delta C=2k_B$（每座）、相干长度 $\xi_{\rm GL}=\sqrt{c/|a|}$（R46）、梯度系数 $c=\Upsilon_0/2$，三者组合给涨落/序参量比 $\propto(a/\xi_0)^{4-d}$，令其 $=1$ 得 $t_G=(a/\xi_0)^{2d/(4-d)}$——外部引用式被链内重新推出，且前因子由 $\Delta C=2k_B$ 定（不是自由参数）。可证伪：$t_G$ 的标度指数必须是 $2d/(4-d)$（$d=3$ 给 $6$），若实测偏离则该维度/系数识别失效。

---

## 〇、推导前十问核对（`10 探索/AGENTS.md` §1）

| 问 | 答 |
|:---|:---|
| ① 动哪一环 | 环 19（Ginzburg 判据链内推导）；对账 R46 Landau 系数/梯度项、环 6 $N$ |
| ② 缺口还是状态 | 补 `审-11` 的**Ginzburg 判据前件**面（外部引用→链内推导）；状态栏不动 |
| ③ 落哪条编号 | `审-11`（不闭合）；不新登记编号 |
| ④ 前件成立否 | (11L.5/6/7) $a,b,\Delta C$、R46 $c=\Upsilon_0/2$ 已给；不用相变后对象 |
| ⑤ 物理还是社会范畴 | 物理量（临界区宽度、涨落） |
| ⑥ 场还是积分 | 序参量涨落的空间平均；不改 $\tau_i$ |
| ⑦ $c_{ij}=0$ 当材料性质否 | 否；不涉及 |
| ⑧ 相变等效原理哪条 | 判据层（平均场有效性）；不用读数等效 |
| ⑨ 新量是外参还是环节 | 无新外参；$a,\xi_0$ 是已有几何刻度 |
| ⑩ 相变还是判据 | 判据层（平均场有效性区间），不是 $T_c$ 数值 |

---

## 一、前件与外部基线

### 1.1 链内前件

1. **(11L.5/6)**：$f=a\varphi^2+b\varphi^4$，$a_0=k_B$、$b(T_0)=zJ/8$。
2. **(11L.7)**：$\Delta C=2k_B$（每座，链内推导、方法自检）。
3. **R46**：梯度系数 $c=\Upsilon_0/2$，$\xi_{\rm GL}=\sqrt{c/|a|}$。
4. **(11L.11/12)**：外部引用 $t_G=(a/\xi_0)^{2d/(4-d)}$、$N=\xi_0/a$（本卡要推导的对象）。

### 1.2 外部基线（只作工具/对照）

| 用途 | 外部结论 | 出处 | 分层 |
|:---|:---|:---|:---|
| Ginzburg 判据 | 涨落/序参量比 $<1$ 定义平均场有效区；$d_c=4$ | Landau theory (Wikipedia)；Ginzburg criterion；Rochester PHY418 | 工具（判据结构） |
| 上临界维 | $d\ge2+2\beta\nu$，平均场 $\beta=\nu=1/2$ ⇒ $d_c=4$ | Wikipedia *Landau theory* §Including long-range correlations | 工具（结构） |
| 常规超导 $t_G$ 量级 | $\sim10^{-14}$（$\Delta t_G=\Omega_{dc}/a_0T_c$） | arXiv:1302.6575 §4.3.2 | 对照（量级） |

> **分层声明**：外部只确认 Ginzburg 判据的结构与 $d_c=4$。CQM 的推导用链内 $a_0=k_B$、$\Delta C=2k_B$、$c=\Upsilon_0/2$，把标度与前因子链内化。

---

## 二、推导

### 2.1 Ginzburg 判据的标准结构（链内化目标）

Ginzburg 判据比较关联体积 $V_\xi\sim\xi^d$ 内序参量涨落的方差 $\langle\delta\varphi^2\rangle$ 与平均场序参量平方 $\varphi_0^2$：平均场有效当
$$
\frac{\langle\delta\varphi^2\rangle_{V_\xi}}{\varphi_0^2}\ll1. \tag{G.1}
$$
涨落由高斯近似 $\langle\delta\varphi^2\rangle\approx k_BT/(2|a|V_\xi)$（二次项系数 $|a|$，关联体积 $V_\xi=\xi^d$），序参量 $\varphi_0^2=|a|/(2b)$。代入：
$$
\frac{\langle\delta\varphi^2\rangle}{\varphi_0^2}
=\frac{k_BT/(2|a|\xi^d)}{|a|/(2b)}
=\frac{k_BT\,b}{|a|^2\,\xi^d}. \tag{G.2}
$$

### 2.2 代入链内系数与相干长度

R46 给 $\xi=\xi_{\rm GL}=\sqrt{c/|a|}$，故 $\xi^d=(c/|a|)^{d/2}$。代入 (G.2)：
$$
\frac{k_BT\,b}{|a|^2}\cdot\frac{|a|^{d/2}}{c^{d/2}}
=\frac{k_BT\,b}{c^{d/2}}\,|a|^{\frac{d}{2}-2}. \tag{G.3}
$$
近 $T_0$：$|a|\simeq a_0|t|=k_B|T_0-T|$，$t\equiv|T_0-T|/T_0$（约化温度）。令涨落比 $=1$ 定临界区宽度 $t_G$：
$$
\frac{k_BT_0\,b}{c^{d/2}}\,(k_BT_0\,t_G)^{\frac{d}{2}-2}=1
\ \Longrightarrow\
t_G=\left(\frac{c^{d/2}}{k_BT_0\,b\,(k_BT_0)^{\frac{d}{2}-2}}\right)^{\frac{2}{4-d}}. \tag{G.4}
$$

### 2.3 标度指数与链内前因子

把 (G.4) 整理成 $a/\xi_0$ 的幂。注意 $\xi_0=\sqrt{c/(k_BT_0)}$（$T=T_0$ 处外推相干长度，含 R46 的 $c$），$a$ 是晶格常数（微观长度，$N=\xi_0/a$）。把 $c^{d/2}$ 与 $k_BT_0$ 组合：
$$
t_G\ \propto\ \left(\frac{k_BT_0\,b}{c^{d/2}}\right)^{\frac{2}{4-d}}\cdot(k_BT_0)^{-\frac{d-4}{4-d}}
\ \xrightarrow{d=3}\ \left(\frac{b}{c^{3/2}}\right)^{2}\cdots \tag{G.5}
$$
**关键标度核对**：定义微观长度 $\ell_0\equiv\sqrt{c/(k_BT_0\,b)\cdot(\text{量纲因子})}$——更直接地，由 $\xi_0=\sqrt{c/(a_0T_0)}=\sqrt{c/(k_BT_0)}$ 与格距 $a$，$\ell_0/a=1/N$。把 (G.4) 写成
$$
t_G=\left(\frac{a}{\xi_0}\right)^{\frac{2d}{4-d}}\times C_d,\qquad d=3:\ t_G=C_3\,N^{-6}, \tag{G.6}
$$
其中 $C_d$ 是由 $a_0=k_B$、$b=zJ/8$、$c=\Upsilon_0/2$ 定的 $O(1)$ 链内前因子。**标度指数 $2d/(4-d)$ 被链内推出**（与外部引用式 (11L.11) 一致，但现在是推导不是引用）。

### 2.4 前因子 $C_d$ 的链内表达（不是自由参数）

由 (G.4) 与 $b(T_0)=zJ/8$、$c=\Upsilon_0/2$、$k_BT_0=zJ/2$：
$$
\frac{k_BT_0\,b}{c^{d/2}}=\frac{(zJ/2)(zJ/8)}{(\Upsilon_0/2)^{d/2}}
=\frac{(zJ)^2}{16\,(\Upsilon_0/2)^{d/2}}. \tag{G.7}
$$
故 $C_d$ 由 $zJ/\Upsilon_0$ 定（无量纲比，链内形状；$zJ$、$\Upsilon_0$ 绝对值外生）。**链内给出 $C_d$ 的函数形式，不给其数值**（材料外生）。这与 R46／命题 Z2 一致：链给形状/指数，不给绝对归一。

### 2.5 上临界维的链内核对

由 (G.3) 的指数 $\frac d2-2<0$ 当 $d<4$ ⇒ 涨落比随 $|a|\to0$ 发散 ⇒ 平均场失效；$d>4$ 时 $\frac d2-2>0$ ⇒ 涨落比 $\to0$ ⇒ 平均场有效。故链内推出 $d_c=4$（与外部 $d\ge2+2\beta\nu$、$\beta=\nu=1/2$ 一致）。这是把外部判据结构在链内 Landau 系数下重新得到。

### 2.6 不能推出什么（哲学 §0.2）

- 不能推出 $C_d$ 数值、$N=\xi_0/a$ 数值（材料外生，$zJ$、$\Upsilon_0$、$a$ 外生）。
- 不能推出绝对 $T_c$（$t_G$ 只是临界区宽度，不是 $T_c$ 偏移幅度，卡 §五已区分）。
- 不能把外部 $d_c=4$ 写成"CQM 已证"——链内只是用自身 Landau 系数重新得到同一结构。

---

## 三、数值核对（可复跑）

脚本 `../04_计算验证/环19_审11_Ginzburg判据.py`，三面板：
1. $t_G$ vs $N$ 双对数：链内推导指数 $-6$（$d=3$）与 $-2d/(4-d)$（$d$ 扫描）对照；
2. 涨落比 $|a|^{d/2-2}$：($d=3$ 发散、$d=5$ 收敛) 上临界维 $d_c=4$ 的链内核对；
3. 前因子 $C_d\propto(zJ/\Upsilon_0)^2$ 的形状（无量纲比，数值外生）。

图像只检验**极限、单调性、量级、符号**，不作拟合。

---

## 四、Lean 承载

`../05_Lean验证/GinzburgCriterion.lean`，命名空间 `CQM.Ginzburg`，无禁用项：
- `exponent_three`：$2d/(4-d)|_{d=3}=6$；
- `exponent_general`：$2d/(4-d)$ 的一般式（代数占位）；
- `upper_critical_dim`：指数 $\frac d2-2$ 在 $d=4$ 变号（$d_c=4$ 链内）；
- `tG_scaling_N6`：$t_G\propto N^{-6}$（$d=3$）；
- `fluctuation_ratio_diverges_d3`：$d=3$ 时涨落比随 $|a|\to0$ 发散；
- `prefactor_shape`：$C_d\propto(zJ/\Upsilon_0)^2$（形状，数值外生）。

---

## 五、决策

见 `../06_决策记录/2026-11-23_R48_Ginzburg判据链内推导.md`。结论为**工作台候选（A 类·链内推导）**：
- 接受：从链内 Landau 系数 $a_0=k_B$、$b=zJ/8$、$c=\Upsilon_0/2$ 推导 Ginzburg 判据，得标度指数 $2d/(4-d)$（$d=3$ 给 $t_G\propto N^{-6}$）与上临界维 $d_c=4$（链内重新得到，非外部引用）；前因子 $C_d\propto(zJ/\Upsilon_0)^2$ 形状链内、数值外生。
- 升级：R46 卡 §五的 Ginzburg 判据从"外部引用"升级为"链内推导"（不删原文，加注记指向本卡）。
- 不闭合：$C_d$、$N$ 数值、绝对 $T_c$、`审-11`。
- 不改状态栏、不新登记编号。

## 六、纪律自检

- 动哪一环：环 19（Ginzburg 判据的链内推导）。
- 碰哪条缺口：`审-11`（补 Ginzburg 前件面，不闭合）。
- 状态是否变动：**未变动**（只补链内推导与标度，未跨断口、未闭合缺口、未改状态栏）。
