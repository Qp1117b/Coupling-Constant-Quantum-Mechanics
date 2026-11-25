# 框架扩展候选 FE06：多带 $T_c$ 的 Suhl–Matthias–Walker 方程 ↔ CQM 12.A 多模式结构对接

> **⚠【候选·未落地·不碰权威源】**。本卡把 CQM 12.A 多模式结构（$\{2,4,6,\ldots\}$、12.A3 权重 $\Phi_n/\Phi_2=2/n$）与外部标准的 Suhl–Matthias–Walker (SMW) 两带方程对接，给出定量多带 $T_c$ 候选式，目标是处理 FE05 中失效的多带系统（MgB₂/Pb/BP₃）。**不闭合 `临-5`/`临-6`**（高模式态—算子映射与第一性归一仍未写出），只把"载体未写出"推进到"结构有方程"。
> 文献：Suhl, Matthias, Walker, PRL **3**, 552 (1959)（Ruby PRL2015 ref 15）；Bussmann-Holder, Micnas, Bishop, EPJB (2004), arXiv:cond-mat/0211588（SMW 两带 $T_c$ 增强，摘要核对）；Kuzmichev et al.（两带 Moskalenko–Suhl 方程拟合实验，arXiv:1612.04303/1404.0517）。

---

## 一、SMW 两带方程（外部标准，弱耦合线性化）

两带（$i=1,2$）隙函数 $\Delta_i$，带内耦合 $\lambda_{ii}$、带间耦合 $\lambda_{ij}$。在 $T=T_c$ 处线性化的 SMW 方程（s 波、弱耦合、对数截断 $\omega_{\log}$）给耦合矩阵本征值条件：

$$\begin{pmatrix}\lambda_{11}&\lambda_{12}\dfrac{\omega_2}{\omega_1}\\[4pt]\lambda_{21}\dfrac{\omega_1}{\omega_2}&\lambda_{22}\end{pmatrix}\begin{pmatrix}\Delta_1\\\Delta_2\end{pmatrix}
=\lambda_{\rm eff}\begin{pmatrix}\Delta_1\\\Delta_2\end{pmatrix},\qquad
\lambda_{\rm eff}=\frac{\lambda_{11}+\lambda_{22}+\sqrt{(\lambda_{11}-\lambda_{22})^2+4\lambda_{12}\lambda_{21}}}{2}.\tag{FE6.1}$$

$T_c^{\rm 2band}\approx1.13\,\omega_{\log}\,e^{-1/\lambda_{\rm eff}}$（带间耦合 $\lambda_{12}\lambda_{21}>0$ 时 $\lambda_{\rm eff}>\max(\lambda_{11},\lambda_{22})$，即 $T_c$ 增强）。这是 SMW 的核心结果：带间对散射提升有效耦合。

## 二、与 CQM 12.A 对接（核心构造）

CQM 12.A：模式集 $n\in\{2,4,6,\ldots\}$，$\{2\}$ 第一档、$n=4$ 高模式；12.A2 填档由局域关系强度 $J_{ij}$（DM.9）决定；12.A3 权重 $\Phi_n/\Phi_2=2/n$。

**对接规则**（构造）：
- 模式 $n=2$（第一档）↔ 带 1，模式 $n=4$（高模式）↔ 带 2；
- 带内耦合 $\lambda_{11}=\lambda^{(2)}$、$\lambda_{22}=\lambda^{(4)}$（由各自模式的记忆核读数）；
- 带间耦合 $\lambda_{12},\lambda_{21}$ 由共享锚核（相变后全局共享，主链 25.A）给——CQM 的"全局共享 K"天然提供带间通道；
- 12.A3 权重进入参与比：带 2 的态密度权重 $w_4/w_2=2/4=0.5$（与第69轮 Pb 双带 $w_1=2/3$ 相容）。

代入 (FE6.1) 得 CQM 多带 $T_c$ 候选式：

$$T_c^{\rm CQM,multi}=1.13\,e^{-3/2}\,\omega_{\log}\,e^{-1/\lambda_{\rm eff}},\qquad
\lambda_{\rm eff}=\tfrac12\bigl[\lambda^{(2)}+\lambda^{(4)}+\sqrt{(\lambda^{(2)}-\lambda^{(4)})^2+4\lambda^{(2)}\lambda^{(4)}r_{\rm inter}^2}\bigr].\tag{FE6.2}$$

其中 $r_{\rm inter}$ 是带间/带内耦合比（CQM 全局共享 K 的强度，外生）。前因子 $e^{-3/2}$ 用 FE04 已确证的绝热区结果。

## 三、检验：MgB₂（FE05 失效系统）

MgB₂ 文献给平均 $\lambda=0.61$、各 Fermi 面 $\lambda(k,k')$ 从 0.1 到 2.5（强各向异性）。设两带 $\lambda^{(2)}=1.2$（强带 p-d）、$\lambda^{(4)}=0.3$（弱带 s-p），带间耦合比 $r_{\rm inter}\approx0.3$（Kuzmichev：层间耦合弱）：

$$\lambda_{\rm eff}=\tfrac12[1.2+0.3+\sqrt{(0.9)^2+4\cdot1.2\cdot0.3\cdot0.09}]\approx\tfrac12[1.5+\sqrt{0.81+0.130}]\approx\tfrac12[1.5+0.970]\approx1.235.$$

$T_c^{\rm multi}=1.13e^{-3/2}\cdot670\cdot e^{-1/1.235}=0.252\cdot670\cdot e^{-0.810}=0.252\cdot670\cdot0.445\approx75$K——过高（文献 39K）。说明两带参数假设需调（实际各向异性 Eliashberg 还有非谐性压制）。**这是候选式的首次试算，不调参贴合**——数值脚本扫描参数空间，看是否存在物理区间给 ~39K。

## 四、验证（Lean＋数值）

- **Lean** `FE06_MultiBandTc.lean`：SMW 有效耦合本征值、$\lambda_{\rm eff}\ge\max$（带间耦合增强）、12.A3 权重 $2/n$、$T_c$ 指数单调；
- **数值** `FE06_多带Tc扫描.py`／图：(a) $\lambda_{\rm eff}$ vs 带间耦合 $r_{\rm inter}$、(b) $T_c^{\rm multi}$ vs $\lambda^{(2)},\lambda^{(4)}$ 曲面、(c) MgB₂ 参数区间扫描（找给 39K 的物理区间）、(d) 与单带 $T_c$ 对照（增强效应）。

## 五、不能推出

1. 不能说闭合 `临-5`/`临-6`——高模式态—算子映射与第一性归一仍未写出，本卡只给结构方程；
2. 不能说 CQM 第一性推出 SMW 方程——SMW 是外部标准，CQM 12.A 提供相容的多模式结构读法；
3. 不能说 MgB₂ 已精确拟合——参数扫描是探索，不调参贴合；
4. 不能说所有多带系统已处理——只给候选框架，需各系统带结构数据；
5. 不改任何编号、状态栏、账面、06 原文。

## 六、状态与交付

**状态**：候选·未落地·不碰权威源；SMW 方程 ↔ 12.A 对接给出多带 $T_c$ 候选式，`临-5`/`临-6` 仍不闭合。
**交付**：本卡＋`FE06_MultiBandTc.lean`＋`FE06_多带Tc扫描.py`／图／csv＋决策记录；不动编号与状态栏、账面、06 原文；未提交。
