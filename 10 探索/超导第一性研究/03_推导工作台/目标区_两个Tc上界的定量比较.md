# 目标区：两个 $T_c$ 上界的定量比较与维度判定——"取小者"的展开

**状态**：工作台推导卡（R57）；不改主链正文、不改 06 原文、不改 08 台账、不改缺口编号与状态栏、不动账面。
**触发**：`目标区_Uemura标度.md` 第 27 行："(U.3) $T_c\le\frac{\pi}{2k_B}\Upsilon_{\rm bare}(0)Q$ 与环 19 的 $T_c\le\min\{T_{\rm BKT}^{\rm pure},T_{\rm pair}(p_c)\}$ 是**两个独立上界，取小者**"——"取小者"只写了一句，从未定量比较谁更强、维度依赖如何。本轮展开。
**一句话**：两条独立上界——A（判据链）$T_c\le T_{\rm A}\equiv\min\{T^\ast,T_{\rm pair}(p_c)\}$，B（目标区/Uemura）$T_c\le T_{\rm B}\equiv\frac{\pi}{2k_B}\Upsilon_{\rm bare}(0)Q$。链内可判定谁更强：由 $\Upsilon_{\rm bare}(0)$ 与 $T^\ast/T_{\rm pair}$ 的相对大小定，且**维度依赖**——2D 相位刚度小（$\Upsilon_{\rm bare}(0)$ 小、BKT 主导），$T_{\rm B}$ 常更低、更紧；3D 刚度大（$\Upsilon\sim$ 费米能标），$T_{\rm B}$ 高、不紧，上界 A（配对支 $T^\ast$）主导。这与环19 (11L.13) 表（2D 由 $T_{\rm ph}$、3D 由 $T^\ast$ 控）**自洽**。可证伪：若 3D 材料实测 $T_c$ 逼近 $T_{\rm B}$（Uemura 上界）而非 $T^\ast$，则刚度主导假设失效。

---

## 〇、推导前十问核对（`10 探索/AGENTS.md` §1）

| 问 | 答 |
|:---|:---|
| ① 动哪一环 | 目标区（两上界比较）；对账环19 (11L.13)、Uemura (U.1)-(U.3)、R16 |
| ② 缺口还是状态 | 补"取小者"的定量展开（不闭合）；状态栏不动 |
| ③ 落哪条编号 | 无新编号（两上界都已有）；不新登记 |
| ④ 前件成立否 | 两上界式、(11L.13) 维度表已给；不用相变后对象 |
| ⑤ 物理还是社会范畴 | 物理量（温度上界） |
| ⑥ 场还是积分 | 刚度/判据温度；不改 $\tau_i$ |
| ⑦ $c_{ij}=0$ 当材料性质否 | 否；不涉及 |
| ⑧ 相变等效原理哪条 | 判据层；不用读数等效 |
| ⑨ 新量是外参还是环节 | 无新外参；$\Upsilon_0$、$T^\ast$ 已登记 |
| ⑩ 相变还是判据 | 判据层（上界比较），不是 $T_c$ 本身 |

---

## 一、前件（全部链内）

1. **上界 A**（环19 (11L.13)、R16 闭合）：$T_c\le\min\{T^\ast,T_{\rm BKT},T_\theta\}\equiv T_{\rm A}$；R16 已把三条件↔三支映射＋合取逻辑落地主链。
2. **上界 B**（Uemura U.1-U.3）：$T_c\le\frac{\pi}{2k_B}\Upsilon_{\rm bare}(0)Q\equiv T_{\rm B}$，$Q=r g_{\rm ren}\le1$。
3. **环19 (11L.13) 维度表**：2D 由 $T_{\rm ph}$（BKT，$\Upsilon$ 小）控；3D 由 $T^\ast$（$\Upsilon\sim$ 费米能标、$T_{\rm ph}\gg T_c$）控。
4. **外部对照**（Uemura 2002, arXiv:cond-mat/0212643, L36）：$T_c\propto n_s/m^\ast$ 普适关联、2D/3D 相变机制区分；只作工具。

> **分层声明**：Uemura 实验律是外部对照；CQM 的结论（两上界比较的维度判定）是链内前件的推论，不证明外部律。

---

## 二、推导

### 2.1 两上界的形式

$$
T_{\rm A}=\min\{T^\ast,\,T_{\rm pair}(p_c)\},\qquad
T_{\rm B}=\frac{\pi}{2k_B}\Upsilon_{\rm bare}(0)\,Q,\quad Q\le1. \tag{57.1}
$$
综合上界 $T_c\le\min\{T_{\rm A},T_{\rm B}\}$——这是"取小者"的精确写法。谁更紧由 $T_{\rm A}$ vs $T_{\rm B}$ 定。

### 2.2 维度判定（核心）

引入无量纲比
$$
\mathcal R\equiv\frac{T_{\rm B}}{T_{\rm A}}
=\frac{\pi\,\Upsilon_{\rm bare}(0)\,Q/(2k_B)}{\min\{T^\ast,T_{\rm pair}(p_c)\}}. \tag{57.2}
$$
- $\mathcal R<1$：上界 B 更紧（刚度/Uemura 主导）；
- $\mathcal R>1$：上界 A 更紧（判据/配对主导）。

**2D**：$\Upsilon_{\rm bare}(0)$ 小（二维刚度小、BKT 温度低），$T_{\rm B}\sim\frac{\pi}{2k_B}\Upsilon_{\rm bare}(0)Q$ 小；而 $T^\ast$（配对温度）可远大于 $T_{\rm B}$（赝能隙区 $T^\ast\gg T_c$）。故 $\mathcal R<1$，**上界 B（刚度）更紧**——与 (11L.13) 表"2D 由 $T_{\rm ph}$（BKT）控"自洽。

**3D**：$\Upsilon_{\rm bare}(0)\sim$ 费米能标（大），$T_{\rm B}$ 高；$T_{\rm pair}(p_c)$、$T^\ast$ 相对低。故 $\mathcal R>1$，**上界 A（配对判据）更紧**——与 (11L.13) 表"3D 由 $T^\ast$ 控"自洽。

### 2.3 自洽性核对

两上界的维度判定与环19 (11L.13) 表的判定**独立地来自同一物理**（2D 刚度小/3D 刚度大），故彼此自洽——这是两条判据链（判据链 vs 目标区/Uemura 链）的拉通核对，无需新假设。

### 2.4 可证伪预言

- 2D 材料：$T_c$ 应逼近上界 B（$\frac{\pi}{2k_B}\Upsilon_{\rm bare}Q$），而非 $T^\ast$——与欠掺杂 Uemura 线性段一致；
- 3D 材料：$T_c$ 应逼近上界 A（$T^\ast$ 或 $T_{\rm pair}(p_c)$），Uemura 上界 B 给不出紧界；
- 若 3D 材料实测 $T_c$ 逼近或超过 $T_{\rm B}$，则"3D 刚度大、B 不紧"假设失效，需回改。

### 2.5 不能推出什么（哲学 §0.2）

- 不给 $\Upsilon_{\rm bare}(0)$、$T^\ast$ 数值（材料外生）；不给 $\mathcal R$ 数值。
- 不闭合任何缺口（两上界都已有；本轮只做比较）。
- 不证明外部 Uemura 律（只作对照）。
- 不给 $T_c$ 精确值（上界不是值）。

---

## 三、数值核对（可复跑）

脚本 `../04_计算验证/目标区_两个Tc上界比较.py`，三面板：
1. $\mathcal R=T_{\rm B}/T_{\rm A}$ 随 $\Upsilon_{\rm bare}(0)$ 扫描：2D 区（小 $\Upsilon$）$\mathcal R<1$、3D 区（大 $\Upsilon$）$\mathcal R>1$，交叉点；
2. 2D/3D 的 $T_{\rm A}$、$T_{\rm B}$ 示意对照（B 紧 vs A 紧）；
3. 与 (11L.13) 维度表对照（2D 刚度控、3D 配对控）——自洽核对。

图像只检验**极限、单调性、量级、符号**，不作拟合。

---

## 四、Lean 承载

`../05_Lean验证/TwoTcBounds.lean`，命名空间 `CQM.TwoBounds`，无禁用项：
- `two_bounds`：$T_c\le\min\{T_A,T_B\}$（合取上界）；
- `ratio_def`：$\mathcal R=T_B/T_A$（代数截面）；
- `R_lt_one_2D`：2D 小 $\Upsilon$ ⇒ $\mathcal R<1$（截面）；
- `R_gt_one_3D`：3D 大 $\Upsilon$ ⇒ $\mathcal R>1$（截面）；
- `self_consistent_11L13`：维度判定与 (11L.13) 表一致（结构命题）。

---

## 五、决策

见 `../06_决策记录/2026-11-23_R57_两个Tc上界比较.md`。结论为**工作台候选（链内比较）**：
- 接受："取小者"展开为 $\mathcal R=T_{\rm B}/T_{\rm A}$ 判据——2D 小 $\Upsilon$ ⇒ $\mathcal R<1$（上界 B 刚度更紧）、3D 大 $\Upsilon$ ⇒ $\mathcal R>1$（上界 A 配对更紧），与环19 (11L.13) 表自洽；给可证伪预言。
- 不闭合：无新缺口；$\Upsilon_0$/$T^\ast$ 数值外生；不给 $T_c$、不证明 Uemura 律。
- 不改状态栏、不新登记编号。

## 六、纪律自检

- 动哪一环：目标区（两上界比较）。
- 碰哪条缺口：无新编号（两上界已有）。
- 状态是否变动：**未变动**。
