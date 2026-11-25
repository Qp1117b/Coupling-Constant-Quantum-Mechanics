# 框架扩展候选 FE03：完整绝对 $T_c$ 式——FE01 能标＋$\mu^\ast$＋矩选择敏感性

> **⚠【候选·未落地·不碰权威源】**。FE01/FE02 的续作。把 FE01 的外生能标公设、第60轮归口的 Morel–Anderson $\mu^\ast$ 形状、第62轮发现的**矩定义分歧**（CQM $e^{-1/3}$ 矩 vs Eliashberg $e^{-1/2}$ 矩，差 $e^{1/6}$）三者首次合并成一个完整候选式，并量化矩选择对绝对 $T_c$ 的系统影响。**不是 CQM 现有结论，不写入主链/06/08 台账，不动编号与状态栏、账面。**

**日期**：2026-11-23
**标源**（均已 webfetch 全文核对）：
- Webb 2015 式(2) Allen–Dynes：$T_c=\frac{\hbar\omega_{\ln}}{1.2k_B}\exp\big[\frac{-1.04(1+\lambda)}{\lambda-\mu^\ast(1+0.62\lambda)}\big]$；式(3)(5) $\omega_{\ln}$、$\mu^\ast$ 定义；
- FE01（本区）：$\omega_D=a\sqrt{\kappa_s/M}(6\pi^2n)^{1/3}$；
- FE02（本区）：数论自生能标 no-go ⇒ 外生能标必要。

---

## 一、动机：此前从未把三者合并

- FE01 给绝对能标 $\omega_D$，但其闭合式用的是裸指数 $e^{-(1+\lambda)/\lambda}$，**未含 $\mu^\ast$**；
- 第60轮归口 $\mu^\ast=\mu/[1+\mu\ln(\epsilon_F/\hbar\omega_D)]$（形状已知、材料量外生）；
- 第62轮发现矩分歧：Allen–Dynes 的 $\omega_{\ln}$（$\alpha^2F/\nu$ 权重，Debye 谱给 $e^{-1/2}\theta_D$）≠ CQM 的 $\omega_{\log}$（$3y^2$ 电子态密度矩，$e^{-1/3}\theta_D$），差 $e^{1/6}$。

FE03 首次把这三者放进一个式子，并正面回答：**绝对 $T_c$ 候选式该用哪个矩？差多少？**

## 二、完整候选式

$$\boxed{\ T_c^{(m)}=\frac{\hbar\,\omega_D^{(m)}}{1.2\,k_B}\,
\exp\!\left[\frac{-1.04(1+\lambda)}{\lambda-\mu^\ast(1+0.62\lambda)}\right],\qquad
\mu^\ast=\frac{\mu}{1+\mu\ln(\epsilon_F/\hbar\omega_D)}\ }\tag{FE3.1}$$

其中 $\omega_D$ 由 FE01 公设给，两种矩选择：

$$\omega_D^{({\rm CQM})}=e^{-1/3}\omega_D\quad(3y^2\ \text{矩}),\qquad
\omega_D^{({\rm Eliash})}=e^{-1/2}\omega_D\quad(\alpha^2F/\nu\ \text{矩}).\tag{FE3.2}$$

**注意**：Allen–Dynes 式(2) 标准的 $\omega_{\ln}$ 是 $\alpha^2F/\nu$ 矩——故严格说应取 $\omega_D^{({\rm Eliash})}=e^{-1/2}\omega_D$。若误用 CQM 矩 $e^{-1/3}$，会使 $\omega_{\ln}$ 偏大 $e^{1/6}=1.181$ 倍，从而 $T_c$ 系统偏高同一因子。这正是第58轮 gap ratio 用错矩后 2.7%→2.9% 的同类问题在 $T_c$ 上的表现。

## 三、矩选择对绝对 $T_c$ 的影响（核心结果）

由于 $\omega_{\ln}$ 在 (FE3.1) 中是**线性前因子**（不在指数内），矩选择给

$$\frac{T_c^{({\rm CQM})}}{T_c^{({\rm Eliash})}}=\frac{e^{-1/3}}{e^{-1/2}}=e^{1/6}\approx1.181.\tag{FE3.3}$$

即：**用 CQM 矩会把绝对 $T_c$ 系统性高估 18.1%**。这是一个干净的、可检验的系统偏差——不是拟合误差，是定义差。

**判定**：框架扩展候选若要与实验绝对 $T_c$ 对照，**必须用 Eliashberg 矩 $e^{-1/2}$**（与 Allen–Dynes 式(2) 的定义一致）；用 CQM 矩 $e^{-1/3}$ 是自相矛盾的（把 CQM 的电子态密度矩塞进 $\alpha^2F/\nu$ 矩的位置）。这与第62轮"gap ratio 用正确矩改善强耦合元素"的结论方向一致。

## 四、$\mu^\ast$ 的作用（第60轮形状接入）

$\mu^\ast$ 出现在 (FE3.1) 指数的分母 $\lambda-\mu^\ast(1+0.62\lambda)$ 中，削弱有效吸引、降低 $T_c$。其形状 $\mu^\ast=\mu/[1+\mu L]$（$L=\ln(\epsilon_F/\hbar\omega_D)$）已知（第60轮 Lean 5 条），但 $\mu$、$\epsilon_F$ 外生——这是第61轮双观测反解要定的材料量。

## 五、验证计划（本轮执行）

- **Lean** `FE03_CompleteTc.lean`：矩比 $e^{1/6}$、`\mu^\ast$ 分母正性条件、$T_c$ 对 $\omega_{\ln}$ 线性、指数单调性；
- **数值** `FE03_完整Tc与矩选择.py`／图：(a) $T_c$–$\lambda$ 两矩对照（差 $e^{1/6}$）、(b) $\mu^\ast$ 对 $T_c$ 压制、(c) 矩比系统偏差 18.1%、(d) 用第61轮反解 $(\lambda,\mu^\ast)$ 代入的 $T_c$ vs 实测（自洽核对，明确非独立验证）。

## 六、不能推出

1. 不是纯 CQM 第一性——FE01 外生公设＋Allen–Dynes 外部式，$T_c$ 是候选构造；
2. 不是对元素 $T_c$ 的独立预测——(d) 面板用实测反解参数代入，必复现，是自洽核对非验证；
3. 不闭合 `审-10`／`审-14`／`审-16`／`审-17`——编号与状态栏不动；
4. 不改权威式——(目标.2)(目标.3) 不动；矩分歧仅在候选区量化；
5. 不碰权威源——主链、06、08 台账、账面、06 原文均不改。

## 七、状态与交付

**状态**：候选·未落地·不碰权威源；核心结果——绝对 $T_c$ 候选式必须用 Eliashberg 矩 $e^{-1/2}$，误用 CQM 矩 $e^{-1/3}$ 高估 18.1%。
**交付**：本卡＋`FE03_CompleteTc.lean`＋`FE03_完整Tc与矩选择.py`／图／csv＋决策记录；不动任何编号与状态栏、账面、06 原文；未提交。
