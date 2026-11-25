# 环 14.A／目标区：链内 $\alpha^2F$ 构造与两矩分歧的结构消解——`审-15`／`审-17`／FE10 外生输入的链内化

**轮次**：第 92 轮补（承接第 87–91 轮；2026-11-24）；成果登记编号 R-101
**性质**：补 `审-15`／`审-17` 的**结构半边**（不改状态栏、不动 06／01／08／研究站）；不改绝对 $T_c$ 外生结论。
**外部文献**（对照工具，非 CQM 已证）：
- $\lambda=2\int_0^\infty\frac{\alpha^2F(\omega)}{\omega}d\omega$、$\alpha^2F(\omega)\ge0$ 且小 $\omega$ 时 $\propto\omega^2$（Kiessling–Altshuler–Yuzbashyan, J. Stat. Phys. (2025), arXiv 版 §1；EPW/AbiPy 文档）。
- 矩定义 $\omega_2^2=\frac{2}{\lambda}\int\alpha^2F\,\omega\,d\omega$、$\omega_{\log}=\exp[\frac{2}{\lambda}\int\frac{\alpha^2F}{\omega}\ln\omega\,d\omega]$（Pickett, arXiv:2204.05930 §II.5；Allen–Dynes PRB **12**, 905）。
- McMillan–Hopfield $\lambda=\eta/(M\langle\omega^2\rangle)$、Debye $\langle\omega^2\rangle=\frac35\omega_D^2$（FE10 已登记；Gaspari–Gyorffy/RMTA 文献另用 $\frac12\theta_D^2$ 约定）。

> 只借标准工具的结构（谱函数定义、矩公式），不声称 CQM＝Eliashberg、不把外部结论写成 CQM 已证（哲学 §0.2 结构同构不是还原）。

---

## 一、前件（十问第 4 问核查）

1. 第 88 轮：曲率模 ↔ 余切拉普拉斯非零模，3D Debye 模计数给 $g(\omega)\propto\omega^2$（$\omega\le\omega_D$）、截断 $Q=(6\pi^2n)^{1/3}$、$\Theta_D=(\hbar c_s/k_B)Q$。
2. 第 84/86 轮：$\rho$ 为 Bessel 核、$S_\rho$ 收敛；零点幅度由曲率模承载（第 87 轮）。
3. R73–R76：CQM $\omega_{\log}^{\rm amp}=e^{-1/3}\theta_D$（$3y^2$ 电子态密度矩，振幅支）；$\omega_{\log}^{\rm ph}=e^{-1/2}\theta_D$（$2y$ 相位支）；Eliashberg $\omega_{\ln}=e^{-1/2}\theta_D$（$\alpha^2F/\nu$ 矩）——三者差 $e^{1/6}$，`审-17` B 类未消。
4. 第 91 轮：$\eta_{\rm chain}\propto N(0)g^2c_\varepsilon^2(1-\rho)Q^2$（FE10 框架扩展候选）；$\langle\omega^2\rangle=\frac35\omega_D^2$ 当时为**外生 Debye 工具**。
5. 前件不含相变后对象作为前件；本轮动的是谱结构的矩，无循环。

> 动的是**缺口** `审-15`／`审-17` 的结构半边（不是状态）；落在 §16 第 26／58 项。

---

## 二、式（生成什么）

### (A) 链内 $\alpha^2F$ 构造

以第 88 轮曲率模谱的 Debye DOS 为骨架，在**常耦合近似**（链无 $\alpha^2F$ 矩阵元结构，`审-15` 已声明）下：

$$\alpha^2F_{\rm chain}(\omega)=A_{\rm eph}\,\omega^2\,\Theta(\omega_D-\omega),\qquad A_{\rm eph}>0\ \text{外生（归一）}. \tag{14A.1}$$

**判定**：$\alpha^2F\propto\omega^2$ 不是外借假设——它就是链内曲率模的 Debye DOS 形状（第 88 轮模计数）；外生的只是**幅度** $A_{\rm eph}$（含 $N(0),g,c_\varepsilon,\rho$）。这与标准 Eliashberg 小 $\omega$ 行为一致，但**不声称** CQM 复现完整 ab initio $\alpha^2F$。

### (B) 一阶矩＝耦合常数（链内可算到归一）

$$\lambda_{\rm chain}=2\int_0^{\omega_D}\frac{\alpha^2F_{\rm chain}(\omega)}{\omega}d\omega=2A_{\rm eph}\int_0^{\omega_D}\omega\,d\omega=A_{\rm eph}\,\omega_D^2. \tag{14A.2}$$

有限，与 $\lambda=N(0)\langle V\rangle$（环 10）同量纲；绝对值外生（$A_{\rm eph}$）。

### (C) 对数矩——两矩分歧的结构消解

用权重 $g(\omega)=\frac{2}{\lambda}\frac{\alpha^2F}{\omega}$（归一化，$\int_0^{\omega_D}g\,d\omega=1$）：

$$\ln\omega_{\log}^{\rm chain}=\int_0^{\omega_D}\frac{2}{\lambda}\frac{\alpha^2F}{\omega}\ln\omega\,d\omega=\frac{\int_0^{\omega_D}\omega\ln\omega\,d\omega}{\int_0^{\omega_D}\omega\,d\omega}=\ln\omega_D-\frac12 \tag{14A.3}$$

$$\Rightarrow\ \omega_{\log}^{\rm chain}=e^{-1/2}\omega_D=\omega_{\log}^{\rm ph}=\omega_{\ln}. \tag{14A.4}$$

**关键判定**：Eliashberg 对数矩 $e^{-1/2}\theta_D$ **从链内曲率模谱导出**——不再是外部输入。而 CQM 振幅支 $e^{-1/3}\theta_D$ 来自 $3y^2$ **电子态密度**权重（另一对象）。故 `审-17` 的两矩分歧＝**同一 Debye 谱的两种权重**：

$$\frac{\omega_{\log}^{\rm amp}}{\omega_{\log}^{\rm chain}}=e^{-1/3}/e^{-1/2}=e^{1/6}. \tag{14A.5}$$

**不是矛盾、不是链内不可修**：两个矩各有链内定义与权重，$e^{1/6}$ 是权重差的精确结果。这把第 62 轮"跨定义代入须加边界"的 B 类判定**升级为结构消解**（仍不改 C5/目标.2 的振幅支口径）。

### (D) 两个二阶矩的约定差消解

$$\omega_2^2=\frac{2}{\lambda}\int_0^{\omega_D}\alpha^2F\,\omega\,d\omega=\frac{\int_0^{\omega_D}\omega^3d\omega}{\int_0^{\omega_D}\omega\,d\omega}=\frac{\omega_D^4/4}{\omega_D^2/2}=\tfrac12\omega_D^2 \tag{14A.6}$$

（$\alpha^2F/\omega$ 权重，Pickett/RMTA 约定）；而未加权的**声子 DOS** 二阶矩

$$\langle\omega^2\rangle_{\rm ph}=\frac{\int_0^{\omega_D}\omega^2\,g_{\rm ph}(\omega)d\omega}{\int_0^{\omega_D}g_{\rm ph}(\omega)d\omega}=\frac{\omega_D^5/5}{\omega_D^3/3}=\tfrac35\omega_D^2 \tag{14A.7}$$

（FE10 用的 Debye 工具）。故文献中 $\frac12\theta_D^2$ 与 $\frac35\omega_D^2$ 的**约定差** = 权重差，比值 $\frac{\omega_2^2}{\langle\omega^2\rangle_{\rm ph}}=\frac56$——两者都可由链内同一谱给出，不再需要外借。

### (E) 同位素与边界

$\omega_{\log}^{\rm chain},\omega_2^2,\langle\omega^2\rangle_{\rm ph}\propto\omega_D\propto M^{-1/2}$，故 $\lambda_{\rm chain}=A_{\rm eph}\omega_D^2\propto1/M$（$A_{\rm eph}$ 质量无关）——与 R71 同位素、FE10 一致。边界：$A_{\rm eph}$ 绝对值外生；常耦合近似不覆盖真实矩阵元频率结构；不证明 $A_{\rm eph}$ 等于 ab initio $\alpha^2F$ 幅度。

---

## 三、依据、量纲、极限、单调性、可证伪

| 检查 | 结果 |
|:---|:---|
| 量纲 | $\alpha^2F$ 能量、$\lambda$ 无量纲、$\omega_{\log},\omega_2$ 频率；$A_{\rm eph}$ 补量纲 |
| 小 $\omega$ | $\alpha^2F\propto\omega^2$，与标准 Eliashberg 及链内 Debye DOS 同 |
| 截断 | $\omega>\omega_D$ 为零（第 88 轮截断），矩积分有限 |
| 单调 | $\lambda_{\rm chain}$ 对 $A_{\rm eph}$ 线性、对 $\omega_D$ 二次 |
| **可证伪** | 若独立测得 $\omega_{\log}$ 显著偏离 $e^{-1/2}\theta_D$（单带常耦合区），本轮构造被否证；真实矩阵元频率依赖可偏离 $\omega^2$（边界） |

---

## 四、历史唯物主义合规（用户明确要求）

1. **基础决定上层建筑**：曲率模谱（几何基础）决定 $\alpha^2F$ 的形状与矩（唯象读数），幅度归一外生；读数不反写谱结构。
2. **必然性与偶然性统一**：**必然**＝常耦合下 $\alpha^2F\propto\omega^2$、$\omega_{\log}=e^{-1/2}\omega_D$、$\omega_2^2=\frac12\omega_D^2$（谱结构固定）；**偶然**＝$A_{\rm eph},\omega_D$ 材料值外生。
3. **结构同构不是还原**：借 Eliashberg 矩公式作工具，不声称 CQM＝Eliashberg、不声称两系统互相推导。
4. **未用社会范畴作物理证据**：只在 §14.1【诠释】段，本卡不引用。
5. **不能推出什么**（必填）：① $A_{\rm eph}$ 绝对值与 ab initio 矩阵元（外生）；② 绝对 $T_c$（命题 Z2＋$\mu^\ast$）；③ 不覆盖强耦合频率依赖与多带（`临-5`/`临-6`）；④ 不声称两矩数值相等——只给权重差的结构解释；⑤ 不碰 `临-8`／`临-22`／RH。

---

## 五、状态与缺口

- **状态**：【标准数学】（Debye 矩积分）＋【构造】（链内 $\alpha^2F$ 常耦合构造），**状态栏不动**。
- **`审-15`／`审-17` 推进**：`审-17` 从"两矩分歧 B 类、链内不可修"推进为"**两矩各有链内权重定义、$e^{1/6}$ 是权重差的精确结果**"（结构消解）；`审-15` 从"同形不同刻度"推进为"同形（$\omega^2$）已由曲率模谱给、矩已链内可算，幅度仍外生"。**残余**：$A_{\rm eph}$ 归一与真实矩阵元频率结构外生 ⇒ 两者**仍不闭合**（编号与状态不动）。
- **不动**：`审-10`、`审-11`、`审-21`、`审-1`、`审-4`、命题 Z2 状态原样；06 原文**仍待与 06 对账**（只登记不改）。

## 六、Lean 状态

`05_Lean验证/SpectralMoments.lean`：Debye 权重归一（$\int_0^1 2x\,dx=1$）、对数矩 $\int_0^1 2x\ln x\,dx=-\frac12$（给 $e^{-1/2}$）、二阶矩 $\int_0^1 2x\cdot x^2dx=\frac12$、声子 DOS 二阶矩 $\frac35$（$\int_0^1 3x^4dx/\int_0^1 3x^2dx$）、比值 $\frac56$、$\lambda=A\omega_D^2$、同位素 $\omega_D\propto M^{-1/2}$——**用多项式积分的精确有理数恒等式**承载（无微积分 API 依赖），无 `axiom`／`sorry`／`admit`／`native_decide`／`unsafe`，`lake env lean` 退出码 0、无警告。

## 七、复现命令

```bash
cd "08 理论组织和形式化框架/04_Lean对接/Lean源码"
lake env lean "../../../10 探索/超导第一性研究/05_Lean验证/SpectralMoments.lean"
python "10 探索/超导第一性研究/04_计算验证/环14A_链内alpha2F与两矩消解.py"
```
