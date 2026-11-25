# 环 10 推进卡：$\lambda$ 的几何第一性形状（候选·未落地）

> 本卡**不修改**主链。只把主链已有的 (9.1)、(10.2)、(10.3) 与环 4 的零点方差代入，推出 $\lambda$ 的形状；$g$、$N(0)$ 仍按 `N-A` 为模型假设，绝对归一外生。

## 〇、动笔前十问（逐条回答）

| 序 | 回答 |
|:---|:---|
| 1 | 动**环 10**（配对强度）；前件在环 4（零点方差）与环 9（方差 (9.1)）。 |
| 2 | 只补**缺口**：`N-A`／`审-2` 的「$\lambda$ 绝对系数未定」。**状态不动**。 |
| 3 | 落在已登记编号 `N-A`（环 10）、`审-2`（$\kappa_f$）、`M6`（关联 $\rho$）。**不新建编号**。 |
| 4 | 前件全部已成立：(9.1)、(10.2)、(10.3)、环 4 的 $\sigma_0^2$、`审-2` 的 $\kappa_f$、$M6$ 的 $\rho_{3d}$；**不含相变后对象**（无 $A_\tau$、无 $\mathcal H=0$），非循环。 |
| 5 | 全是**物理量**（$\sigma_0^2$、$\rho$、$\lambda$）；无社会范畴。 |
| 6 | $\sigma_0^2$ 是亏角场的零点方差，$\kappa_f$ 是场响应；(10.2) 是键耦合，**没有"改造时间"**的操作。 |
| 7 | 未把 $c_{ij}=0$ 当材料性质。 |
| 8 | 未用相变等效原理（本环在相变前）；不涉及 (13.4)/(13.5)。 |
| 9 | **不引入新外参**；$N(0)$、$g$ 是 (10.3) 已有的模型假设（`N-A` 已登记），本轮不新增对象。 |
| 10 | 说的是**判据／形状**，不是相变；不碰 $T_c$（$\lambda\to T^\ast$ 一步属环节⑨，主链已明言未推）。 |

---

## 一、前件

1. 环 9 (9.1)：$\langle(\delta C_{ij})^2\rangle=2\kappa_f^2\sigma_0^2(1-\rho_{ij})$；
2. 环 10 (10.2)：$\lvert V_{ij}\rvert=\dfrac{4g^2\sigma_0^2(1-\rho_{ij})}{\hbar\omega_{ij}}$；
3. 环 10 (10.3)：$\lambda_i=N(0)\sum_j\lvert V_{ij}\rvert$；
4. 环 4（$d=3$，第 86 轮）：$\sigma_0^2=\dfrac{c_\varepsilon^2\hbar Q^4}{16\pi^2\rho_m c}$，$c_\varepsilon=\kappa\,\mathrm{RMS}(\varepsilon^{(0)})$；
5. `M6`：$\rho_{3d}(x)=\dfrac{2(1-\cos x)}{x^2}$，$x=Qd$；
6. `FE01`（候选区接口）：$\omega_D=cQ$，$k_D=(6\pi^2n)^{1/3}$，$\rho_m=Mn$。

**条件假设（明确标注）**：近邻壳层等价——同一壳层上 $\omega_{ij}=\omega_a=cQ$、$\rho_{ij}=\rho_a=\rho_{3d}(Qd)$，配位数 $z$。这不是新公设，是把 (10.3) 的求和按壳层归并。

## 二、式（推导）

**第一步：把环 4 零点方差代入 (10.2)**。

$$\lvert V_a\rvert=\frac{4g^2}{\hbar cQ}\cdot\frac{c_\varepsilon^2\hbar Q^4}{16\pi^2\rho_m c}\,(1-\rho_a)
=\frac{g^2c_\varepsilon^2(1-\rho_a)\,Q^3}{4\pi^2\rho_m c^2}.\tag{CQM-L1}$$

> $\hbar$ **完全约掉**——这与 $\lambda$ 为无量纲量一致，是命题 Z2 允许链内推出的那一类对象。

**第二步：代入 (10.3) 得 $\lambda$ 的声学形状**。

$$\boxed{\ \lambda=\frac{N(0)\,z\,g^2\,c_\varepsilon^2\,(1-\rho_a)\,Q^3}{4\pi^2\rho_m c^2}\ }\tag{CQM-L2}$$

**第三步：换成 McMillan 型无量纲组合**。由 $c=\omega_D/Q$、$\rho_m=Mn=M Q^3/(6\pi^2)$：

$$\rho_m c^2=\frac{MQ^3}{6\pi^2}\cdot\frac{\omega_D^2}{Q^2}=\frac{MQ\omega_D^2}{6\pi^2},$$

$$\boxed{\ \lambda=\frac{\frac32 N(0)z g^2 c_\varepsilon^2(1-\rho_a)Q^2}{M\omega_D^2}\equiv\frac{\eta_{\rm CQM}}{M\omega_D^2}\ }\tag{CQM-L3}$$

其中 $\eta_{\rm CQM}=\frac32 N(0)z g^2 c_\varepsilon^2(1-\rho_a)Q^2$ 是 **CQM 给出的 Hopfield 参数几何因子**。

## 三、依据

- (CQM-L1) 是纯代入：$\hbar$、数值因子 $4/16=1/4$ 由 (10.2) 与环 4 式联立；
- (CQM-L2) 是 (10.3) 的壳层归并；
- (CQM-L3) 是 $c=\omega_D/Q$ 与 $\rho_m=MQ^3/(6\pi^2)$ 的代数替换，无新物理假设。

**三个即时自洽检验**（数值见 `04_计算验证/`）：

1. **同位素**：$\eta_{\rm CQM}$ 不含 $M$，而 $\omega_D\propto M^{-1/2}$（`FE01`）⇒ $M\omega_D^2$ 与 $M$ 无关 ⇒ $\lambda$ **质量无关**；$T_c\propto M^{-1/2}$。与 `推9` 端点 $\alpha=1/2$ 一致。
2. **交易律**：固定 $\eta_{\rm CQM}$ 时 $\lambda\propto1/\omega_D^2$，与 McMillan $\lambda=\eta/(M\langle\omega^2\rangle)$ 同形（外部标准工具，B 类对照）。
3. **符号**：$N(0),z,g^2,c_\varepsilon^2,Q,\rho_m,c>0$ 且 $\rho_a<1$（$M6$ 关联函数 $\rho_{3d}<1$，$x>0$）⇒ $\lambda>0$，与环 10「链里没有负净耦合」一致。

## 四、状态

**【条件严格】**：条件于 (i) 近邻壳层等价；(ii) 环 4 的 $d=3$ 零点方差；(iii) `FE01` 的 $\omega_D=cQ$ 接口；(iv) `N-A` 已登记的 $g,N(0)$ 模型假设。**不闭合任何缺口**。

**缺口行（不动状态栏）**：`N-A` — $\lambda$ 的**形状**已由链内量给出，绝对归一仍待 $g,N(0),c_\varepsilon$ 的材料归一；本卡只推进形状，编号原样保留。`审-2` — $\kappa_f$ 条件于 FG，未变。`M6` — $\rho_{3d}$ 的形状未变。

## 五、不能推出什么（哲学 §0.2 判据）

1. **不能推出 $\lambda$ 的绝对值**：$g$、$N(0)$、`RMS(ε^(0))`、`κ` 外生（`N-A`／环 4 剩余 O(1) 因子）。
2. **不能推出 $T_c$**：(目标.2) 是外来式，$\lambda\to T^\ast$ 的 Cooper 不稳定性与对数求和属环节⑨、未推；不得以「与 BCS 形式相同」充当该步完成。
3. **不能推出外部 2025 相关性由 CQM 造成**：只做到 $\lambda\propto1/\omega_D^2$ 的**形状同形**；因果归属未证。
4. **不能推出自由能非解析性或相变**：本环在相变前，无 $\varphi$、无 $A_\tau$。
5. **不能改 06 原文、主链、08 台账、状态栏、账面**。
