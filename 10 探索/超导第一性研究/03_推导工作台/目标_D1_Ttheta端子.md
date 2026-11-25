# 目标区／`D1`：$T_\theta$ 端子从"空符号"到形状公式——最低零点模控制

**状态**：工作台推导卡；未写入主链正文、06、08 台账。
**触发**：`D1`——$T_\theta$ 是 (目标.1) 中空端子，只有符号无公式；主链 (27.2) 说"所有非平凡零点给同一 $T_\theta$ ⇔ RH"，但从未定义单个零点如何给温度。本轮用链内已有的阻尼率公式给出口径。

**一句话**：把单个零点的相位弛豫温度定义为

$$\boxed{\ T_{\theta,n}\equiv\frac{\hbar}{k_B}\Gamma_n
=\frac{\hbar}{k_B}\,\gamma_n^2\sigma_v^2\tau_g,\qquad
T_\theta=\min_n T_{\theta,n}=T_{\theta,1}\ } \tag{D1.1}$$

（$\Gamma_n$ 来自 (26.1b)，$\tau_g=c/\omega_D$ 来自上一轮阻尼桥）。因 $\Gamma_n\propto\gamma_n^2$ 随 $n$ 增，**最低零点 $n=1$ 的弛豫温度最低**，故 (目标.1) 的 $\min$ 端子由 $n=1$ 控制；而 (27.2) 的"所有零点给同一 $T_\theta$"恰对应 $\Gamma_n$ 与 $n$ 无关——即 `临-22` 已判定的阻尼统一，**链内不可由物理侧供给**。于是 $T_\theta$ 的形状已给、单一性依赖外部 RH 假设，绝对数值仍含 $\sigma_v^2$、$c$、$\omega_D$（外生）。

---

## 一、前件

1. (目标.1)：$T_c=\min\{T^*,T_{\rm BKT},T_\theta\}$；缺口记"$T_\theta$ 是空端子，只有符号无公式（`D1` 最高优先）"。
2. (27.2)：RH ⇔ 所有非平凡零点给同一 $T_\theta$ ⇔ 相变唯一；(27.3) $\rho_n=\beta_n+i\gamma_n$ 时阻尼率 $\propto\beta_n$，RH ⇔ $\beta_n\equiv1/2$。
3. (26.1b)：$\Gamma_n=\gamma_n^2\sigma_v^2\tau_g$（单节点 OU 时间涨落支）；上轮阻尼桥：$\tau_g=c/\omega_D$、高温 $\Gamma_n\propto T$ 形状。
4. 外部标准（只作工具，不作 CQM 结论）：Planckian 弛豫 $\tau_{\rm Pl}=\hbar/(k_BT)$ 与 $\hbar/\tau\sim k_BT$（arXiv:2506.19188；arXiv:2504.02179 *Homes’ Law and Universal Planckian Relaxation*；Legros et al. Nat. Phys. **15**, 142 (2019)）——给"速率↔温度"的 $\hbar/k_B$ 换算；零点纵坐标 $\gamma_1=14.1347,\gamma_2=21.0220,\gamma_3=25.0109$（数值示意）。

---

## 二、推导

### 2.1 单个零点的温度

由 (26.1b)，第 $n$ 个零点模的相位弛豫率 $\Gamma_n$ 有量纲 $1/\text{时间}$；用 Planckian 换算给温度

$$T_{\theta,n}=\frac{\hbar}{k_B}\Gamma_n=\frac{\hbar}{k_B}\gamma_n^2\sigma_v^2\tau_g.\tag{D1.2}$$

这是一个**定义（构造）**：把"模的相位记忆消失"读成一个温度端子。链内此前没有该定义，本轮补上；它不冒充已证物理关系。

### 2.2 min 由最低零点控制

$\gamma_n$ 随 $n$ 增（第一零点 $\gamma_1\approx14.13$ 最小），故 $\Gamma_n\propto\gamma_n^2$ 随 $n$ 增，$T_{\theta,n}$ 亦然。于是

$$T_\theta=\min_n T_{\theta,n}=T_{\theta,1}
=\frac{\hbar}{k_B}\gamma_1^2\sigma_v^2\tau_g. \tag{D1.3}$$

物理读法：**第一个（最低频）零点模最先失去相位相干**，它决定 $T_\theta$ 端子；更高频模在更低温度就已过阻尼。这是从已有 $\Gamma_n$ 公式直接读出的结构，不是新假设。

### 2.3 与 RH 的关系

(27.2) 的"所有零点给同一 $T_\theta$"要求 $T_{\theta,n}$ 与 $n$ 无关，即 $\Gamma_n$ 与 $n$ 无关。但 (26.1b) 的 $\Gamma_n\propto\gamma_n^2$ 依 $n$ 变；`临-22` 已判定物理侧**不可能**供给阻尼统一。故

- (27.2) 的"同一 $T_\theta$"只能来自外部 RH 假设（把 $\gamma_n^2$ 换成统一的 $\beta_n=1/2$ 结构）；
- 本轮定义的 $T_{\theta,n}$ 在不假设 RH 时是梯度族，(目标.1) 取 $\min$ 自动选 $n=1$——这**绕开**了 RH，但付出的代价是 $T_\theta$ 不再"唯一"（每模一个温度）。

**判定**：D1 从"空端子"推进为"形状公式已给（min 选 $n=1$），单一性需外部 RH"。

---

## 三、量纲与数值口径

- $\hbar\Gamma_n/k_B$ 有温度量纲 ✓；
- 代入 $\tau_g=c/\omega_D$：$T_\theta=\hbar c\,\gamma_1^2\sigma_v^2/(k_B\omega_D)$；高温 $\sigma_v^2=\kappa_\Theta T/\omega_D$ 时 $T_\theta\propto T/\omega_D^2$——**自洽方程**而非独立数值，因 $\sigma_v^2$ 本身随实际温度变；这不是缺陷，而是"记忆时间由声子谱定"的必然结果；
- 绝对数值含 $c$、$\kappa_\Theta$、$\omega_D$、$\sigma_v^2$（外生），与总账的最小外生输入集一致。

---

## 四、不能推出

1. **不能推出绝对 $T_c$**：$T_\theta$ 的绝对值含外生量。
2. **不能推出 RH**：(27.2) 的反向不成立，链已知。
3. **不能推出 $T_\theta$ 是唯一温度**：无 RH 时是梯度族，本轮用 min 选 $n=1$ 是**定义选择**。
4. **不能推出该定义就是 06 原意**：06 未给公式，本轮是【构造】。
5. **不能推出 $T_\theta$ 与 $T^*$／$T_{\rm BKT}$ 的数值大小关系**：三端子各自含不同外生量，超出只能由材料数据定。
6. **不能改 06 原文或主链状态栏**。

---

## 五、Lean 承载

`../05_Lean验证/ThetaTerminal.lean`：

- `thetaTemp`：定义 $T_{\theta,n}=(\hbar/k_B)\gamma_n^2\sigma_v^2\tau_g$（以正常数 $C$ 简记 $\hbar\sigma_v^2\tau_g/k_B$）；
- `gamma_sq_monotone`：若 $0<\gamma_1\le\gamma_2$ 则 $\Gamma_1\le\Gamma_2$；
- `min_selects_first`：零点纵坐标正且递增 ⇒ $\min_n T_{\theta,n}=T_{\theta,1}$（对前三个零点显式验证）；
- `uniform_iff_same_theta`：所有 $T_{\theta,n}$ 相等 ⇔ 所有 $\Gamma_n$ 相等（代数），接 `临-22` 的不可统一判定；
- `theta_scaling`：代入 $\tau_g=c/\omega_D$ 的代数式。

未形式化：$\hbar$、$k_B$ 的物理定义（外部）、Planckian 换算的物理证明（外部标准）。无 `axiom`、`sorry`、`admit`、`native_decide`、`unsafe`。

---

## 六、数值核对

`../04_计算验证/目标_D1_Ttheta.py`：

1. 前 6 个零点的 $T_{\theta,n}$ 阶梯（取 $C=1$ 示意），标出 $n=1$ 最小；
2. $\Gamma_n\propto\gamma_n^2$ 与 $T_{\theta,n}$ 的线性关系；
3. $\min$ 选择随零点数的稳定性（前 3／6／10 个零点都选 $n=1$）；
4. 统一阻尼假设下的退化：所有 $T_{\theta,n}$ 相等（虚线）与本轮梯度族（实线）对比。

无拟合；由 (D1.1)–(D1.3) 直接计算。

---

## 七、状态与缺口

**已确认（代数＋数值严格，条件于定义 D1.2）**：(D1.1)–(D1.3)；$T_\theta$ 由最低零点控制；单一性需 RH（外部）。

**判定**：`D1` 从"空端子"推进为"**形状公式已给、min 选 $n=1$、绝对归一外生**"；保留编号与未闭合状态。

**未闭合**：绝对 $\omega_D$、$c$、$\sigma_v^2$；`临-22`（阻尼统一不可供给）；RH 外部假设；`临-19`（$\Upsilon(B)$）。
