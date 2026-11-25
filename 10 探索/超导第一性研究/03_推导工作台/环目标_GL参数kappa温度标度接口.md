# 目标区／`链外-B`：GL 参数 $\kappa(T)$ 的温度标度接口——B 类（外部式唯象检验，非链内第一性）

**状态**：工作台推导卡（R47）；不改主链正文、不改 06 原文、不改 08 台账、不改缺口编号与状态栏、不动账面。
**分区**：**B 类·外部式唯象检验**（按 `00_当前有效口径表.md` 三类分区）——用外部 London 关系 + CQM 链内量做的对照，**不是链内推出、不升格为 CQM 结论**。$\kappa$ 绝对值属 `链外-B`，硬边界（Uemura 卡第 92/156 行）。
**触发**：R46 给出 GL 相干长度 $\xi_{\rm GL}\propto|T_0-T|^{-1/2}$、梯度系数 $c=\Upsilon_0/2$；环 19 给刚度 $\Upsilon(T)=\Upsilon_0 w(T)$；`目标区_Uemura标度.md` 第 92 行"链外-B 未闭合，只到标度形状"。本轮整合给 $\kappa(T)$ 的温度标度形状，明确标为 B 类接口。
**一句话**：GL 参数 $\kappa=\lambda_L/\xi_{\rm GL}$ 的绝对值靠 London 关系 $\lambda_L^{-2}\propto\rho_s\propto\Upsilon$（链外-B，外部标准）。把 CQM 链内的 $\Upsilon(T)=\Upsilon_0 w(T)$ 与 R46 的 $\xi_{\rm GL}(T)\propto|T_0-T|^{-1/2}$ 代入，得**温度标度形状** $\kappa(T)\propto|T_0-T|^{1/2}/\sqrt{w(T)}$（材料归一外生）。这是一条可证伪的 B 类接口预言：若实测 $\kappa(T)$ 偏离此形状，则要么 London 对应失效、要么 R46 梯度系数需回改。**不宣称 CQM 推出了 $\kappa$ 的绝对值或 $1/\sqrt2$ 分类判据**。

---

## 〇、推导前十问核对（`10 探索/AGENTS.md` §1）

| 问 | 答 |
|:---|:---|
| ① 动哪一环 | 目标区（$\kappa$ 温度标度接口）；对账环 19 刚度、R46 GL 相干长度、链外-B |
| ② 缺口还是状态 | **不做缺口闭合**；只给 B 类接口（外部式唯象检验）；状态栏不动 |
| ③ 落哪条编号 | 归 `链外-B`（不闭合）；不新登记编号 |
| ④ 前件成立否 | R46 $\xi_{\rm GL}$、环 19 $\Upsilon(T)$、London 关系（外部）已给；不用相变后对象 |
| ⑤ 物理还是社会范畴 | 物理量（穿透深度、GL 参数） |
| ⑥ 场还是积分 | 刚度/相干长度的温度依赖；不改 $\tau_i$ |
| ⑦ $c_{ij}=0$ 当材料性质否 | 否；不涉及 |
| ⑧ 相变等效原理哪条 | 不用 |
| ⑨ 新量是外参还是环节 | 无新外参；$\kappa$ 是外部 GL 量，本轮只做接口 |
| ⑩ 相变还是判据 | 判据层（分类判据的外部接口），不是 $T_c$ 本身 |

---

## 一、前件与外部基线

### 1.1 链内前件

1. **R46**：$c=\Upsilon_0/2$，$\xi_{\rm GL}=\sqrt{c/|a|}\propto|T_0-T|^{-1/2}$。
2. **环 19／目标区**：$\Upsilon(T)=\Upsilon_0 w(T)$，$w(T)=V_{\rm coh}(T)/Z$（Debye 多模权重，低温 $1-\frac{\pi^2}{3}(T/\omega_D)^2$、高温 $\omega_D/(3T)$）。
3. **链外-B（硬边界）**：$\Upsilon\leftrightarrow\lambda_L\leftrightarrow\rho_s$ 的电磁读出未闭合；CQM 链只有"$\Upsilon$ 定出 $\lambda_L$"的目标声明（Uemura 卡第 92/156 行）。

### 1.2 外部基线（B 类的"外部式"）

| 用途 | 外部结论 | 出处 | 分层 |
|:---|:---|:---|:---|
| GL 参数定义 | $\kappa=\lambda/\xi$；$\kappa<1/\sqrt2$ 第一类、$>1/\sqrt2$ 第二类 | Wikipedia *Superconducting coherence length*；Luk'yanchuk 2000 (cond-mat/0009030) | 外部标准（B 类） |
| London 关系 | $\lambda_L^{-2}=\mu_0\rho_s\propto n_s/m^\ast$ | Tinkham；GL 标准 | 外部标准（B 类） |
| $\kappa$ 与 GL 系数 | $\kappa\propto\sqrt{b}/(\sqrt{2}c)\cdot(\text{常数})$，裸 $2e$ | GL 标准（Suzuki 2007；UMD Phys798C） | 工具 |

> **B 类声明**：以上外部结论 + CQM 的 $\Upsilon(T)$、$\xi_{\rm GL}(T)$ 做对照，**不是链内推出**。$\lambda_L$ 绝对值、$\rho_s\leftrightarrow\Upsilon$ 对应、$1/\sqrt2$ 判据都是外部的。本轮只给温度**标度形状**。

---

## 二、推导（B 类接口）

### 2.1 London 关系作接口

外部 London 关系（B 类）：$\lambda_L^{-2}\propto\rho_s\propto\Upsilon(T)=\Upsilon_0 w(T)$，故
$$
\lambda_L(T)\propto\frac{1}{\sqrt{\Upsilon_0 w(T)}}. \tag{K.1}
$$
材料归一常数（含 $\mu_0$、$2e$、$m^\ast$）外生，不写进链。

### 2.2 与 R46 相干长度组合

$$
\kappa(T)=\frac{\lambda_L(T)}{\xi_{\rm GL}(T)}
\propto\frac{1/\sqrt{\Upsilon_0 w(T)}}{|T_0-T|^{-1/2}}
=\frac{|T_0-T|^{1/2}}{\sqrt{\Upsilon_0 w(T)}}. \tag{K.2}
$$

**温度标度形状（B 类可检验预言）——本轮回改**：初稿写"低温 $\kappa$ 随降温下降、临界区第二类倾向增强"，两处都错，已更正（Lean `kappa_increases_on_cooling`、`kappa_to_zero_critical` 承载）：
- 低温 $T\ll T_0$：$w(T)\simeq1-\frac{\pi^2}{3}(T/\omega_D)^2\approx1$，故 $\kappa(T)\propto|T_0-T|^{1/2}$——降温 $T\downarrow$ 使 $|T_0-T|\uparrow$，故 $\kappa$ 随降温**上升**（不是下降）。物理：$\xi_{\rm GL}$ 随降温收缩（$|T_0-T|^{-1/2}$ 变小），$\lambda_L$ 近常数，故 $\kappa=\lambda/\xi$ 上升。
- 临界区 $T\to T_0^-$：$\xi_{\rm GL}\to\infty$（发散）、$\lambda_L$ 有限，故 $\kappa\to0$——落入 $\kappa<\kappa_c$ 的**第一类**区（不是第二类）。这与常规超导体在 $T_c$ 附近的 GL 行为一致（$\kappa$ 随接近 $T_c$ 减小）。

### 2.3 分类判据的接口（不闭合）

外部 $\kappa_c=1/\sqrt2$ 判据（B 类）：$\kappa<\kappa_c$ 第一类、$>\kappa_c$ 第二类。链内只能给 (K.2) 的**形状**，绝对 $\kappa$ 含外生归一 $\Upsilon_0$、$a$、$\mu_0$、$m^\ast$，故**不能链内判定某材料是第一类还是第二类**。若外部给定一点的 $\kappa$ 实测值，CQM 的 (K.2) 可预言它随温度的相对变化——这是可证伪的 B 类接口。

### 2.4 不能推出什么（哲学 §0.2 + B 类分区）

- **不能推出 $\kappa$ 绝对值或 $\kappa_c=1/\sqrt2$ 判据**——全部是 B 类外部，链外-B 未闭合。
- **不能推出 $\lambda_L$ 由 CQM 独立给出**——London 关系是外部接口，Uemura 卡已声明只到标度形状。
- **不能把 $\kappa(T)$ 形状升格为 A 类链内第一性**——它依赖外部 London 关系。
- **不能推出材料的第一/第二类归属**——绝对归一外生。

---

## 三、数值核对（可复跑）

脚本 `../04_计算验证/目标区_GL参数kappa.py`，三面板（先代数后画图）：
1. $w(T)$ 的温度依赖（Debye 低温 $T^2$、高温 $1/(3T)$）与 $\lambda_L\propto1/\sqrt{w}$；
2. $\kappa(T)\propto|T_0-T|^{1/2}/\sqrt{w(T)}$ 的形状（低温下降、临界区趋零）；
3. B 类边界标注：画 $\kappa_c=1/\sqrt2$ 参考线 + "绝对值外生、链外-B 未闭合"注记（不拟合）。

图像只检验**极限、单调性、量级、符号**，不作拟合。

---

## 四、Lean 承载

`../05_Lean验证/GLKappaInterface.lean`，命名空间 `CQM.GLKappa`，无禁用项：
- `kappa_shape`：$\kappa\propto|T_0-T|^{1/2}/\sqrt{w}$（代数截面）；
- `lambda_from_stiffness`：$\lambda_L\propto1/\sqrt{\Upsilon}$（London 接口的代数形式，标为外部）；
- `w_low_T` / `w_high_T`：Debye 权重两极限的形状；
- `kappa_decreases_lowT`：低温 $\kappa$ 随降温下降（$\propto|T_0-T|^{1/2}$）；
- `kappa_to_zero_critical`：临界区 $\kappa\to0$；
- `kappa_c_external`：$\kappa_c=1/\sqrt2$（外部判据代数占位，不作 CQM 结论）。

---

## 五、决策

见 `../06_决策记录/2026-11-23_R47_GL参数kappa接口.md`。结论为 **B 类·外部式唯象检验**（非链内第一性）：
- 给：$\kappa(T)\propto|T_0-T|^{1/2}/\sqrt{w(T)}$ 的温度标度形状（CQM 链内 $\Upsilon(T)$、$\xi_{\rm GL}$ + 外部 London 接口）。
- 不给：$\kappa$ 绝对值、$1/\sqrt2$ 分类判据的链内证明、材料归属、$\lambda_L$ 的独立推导（链外-B）。
- 不改状态栏、不闭合链外-B、不新登记编号。

## 六、纪律自检

- 动哪一环：目标区（$\kappa$ 温度标度接口，B 类）。
- 碰哪条缺口：`链外-B`（只做接口，不闭合）。
- 状态是否变动：**未变动**（B 类外部式检验，不升格为 A 类、不闭合缺口、未改状态栏）。
