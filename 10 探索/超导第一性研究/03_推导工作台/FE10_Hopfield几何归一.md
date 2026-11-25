# 框架扩展候选 FE10：Hopfield 参数的链内几何归一（候选·未落地）

> **⚠ 框架扩展候选**：新增匹配公设（外部 $\lambda=\eta/(M\langle\omega^2\rangle)$ 接入链），不是链内已证。本卡在隔离工作区，不落地主链/06/08。落地需授权。

## 〇、动笔前十问

| 序 | 回答 |
|:---|:---|
| 1 | 框架扩展候选，连接环 10（λ 几何）与外部 McMillan 关系，不新编环号。 |
| 2 | 做**候选研究**；状态不动。 |
| 3 | 关联 `N-A`（λ 归一）、`M3`（DOS）。 |
| 4 | 前件：R1 λ 几何（链内 A 类）+ 外部 McMillan/Debye 矩（工具）；匹配关系标为公设。 |
| 5 | 物理量；无社会范畴。 |
| 6 | 动的是**归一匹配**，不是场改造。 |
| 7 | 未把 $c_{ij}=0$ 当材料性质。 |
| 8 | 未用相变等效原理。 |
| 9 | 新增匹配公设，明确标注；不伪装链内已证。 |
| 10 | 说的是**归一形状**，不给 $T_c$ 数值。 |

---

## 一、前件与新公设

1. 链内 R1：$\lambda_{\rm geom}=\frac{\frac32 N(0)z g^2 c_\varepsilon^2(1-\rho)Q^2}{M\omega_D^2}$；
2. 外部工具：McMillan $\lambda=\eta/(M\langle\omega^2\rangle)$、Debye $\langle\omega^2\rangle=\frac35\omega_D^2$；
3. **新公设 FE10**：外部 McMillan 关系作为匹配桥接入链（框架扩展，非链内推导，R8 定理已证隙方程结构外生）。

## 二、式

**匹配**（FE10.1）：

$$\frac{\eta}{M\cdot\frac35\omega_D^2}=\lambda_{\rm geom}\ \Rightarrow\ \eta_{\rm chain}=\frac{9}{10}N(0)z g^2 c_\varepsilon^2(1-\rho)Q^2.\tag{FE10.1}$$

**链给出的形状**：

$$\eta_{\rm chain}\propto N(0)\,g^2\,c_\varepsilon^2\,(1-\rho)\,Q^2.\tag{FE10.2}$$

对比标准理论：$\eta=N(0)\langle I^2\rangle$，其中 $\langle I^2\rangle$ 是经验矩阵元（"atomic property"）——链把它细化为 $g^2 c_\varepsilon^2(1-\rho)Q^2$（几何×关联×倒格子尺度）。

**一致性检验**：同位素——$\eta_{\rm chain}$ 不含 $M$（$Q$ 由数密度定），故 $\lambda\propto1/M$，与标准 $\eta$ 质量无关、$\omega_D\propto M^{-1/2}$ 一致；R1 已证 $\lambda$ 质量无关，FE10 兼容。

## 三、可证伪预言 P-FE10

对同元素、$N(0)$ 近似不变的样品系列（如不同退火/无序度）：
- $\eta\propto c_\varepsilon^2=\kappa^2\mathrm{RMS}(\varepsilon^{(0)})^2$ ⇒ 结构无序（亏角涨落）越大，$\eta$ 越大；
- $\eta\propto(1-\rho)$ ⇒ 亏角关联越强（$\rho\to1$），$\eta$ 越小。

$\eta$ 可由隧穿 $\alpha^2F$ 反演的 $\lambda$ 与 $\langle\omega^2\rangle$ 独立测定（$\eta=\lambda\langle\omega^2\rangle M$）。若实测 $\eta$ 与无序度无此相关，FE10 被证伪。

## 四、状态与诚实边界

- **框架扩展候选**（新增匹配公设），未落地；落地需授权；
- 只给 $\eta$ 形状，$N(0),g,c_\varepsilon,\rho$ 外生；
- 不宣称解释具体 $\eta$ 数值；与 R8 定理相容（公设是外生结构的显式化）；
- 不改权威源。

## 五、验证

- Lean `HopfieldGeometry.lean`：匹配代数（FE10.1）、形状比例、同位素质量无关、单调方向；
- 数值/图像：$\eta$ 随 $c_\varepsilon^2$、$(1-\rho)$、$Q^2$ 的形状；无拟合。

## 六、不能推出什么

1. 不是链内第一性——新增匹配公设；
2. 不能给 $\eta$ 绝对值——外生归一；
3. 不能说已验证——需隧穿 $\alpha^2F$ 独立测 $\eta$ 的判别实验；
4. 不能改权威源。

## 七、状态与交付

框架扩展候选（未落地、不碰权威源）；交付本卡＋Lean＋数值图像＋决策记录。
