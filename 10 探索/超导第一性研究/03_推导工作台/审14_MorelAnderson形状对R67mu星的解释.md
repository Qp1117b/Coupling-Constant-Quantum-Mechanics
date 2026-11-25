# `审-14`：Morel–Anderson 形状对 R67 经验 $\mu^\ast$ 的解释（R68）

**状态**：工作台核对卡（R68）；不改主链、不改 06、不动账面。

> **⚠ 口径更正注记（R69，2026-11-24）**：本卡标题含"审-14"及正文把 $\mu^\ast$ 归 `审-14` 是与主链权威源不一致的口径误用——主链 §1439 明确库仑赝势 $\mu^\ast$ 属**链外-A**（限制(4)：链内 $V<0$ 恒成立、无"负净耦合"态），`审-14` 是读出泛函 $\Gamma$ 的第一性来源（§1623）。本卡数值发现（Morel–Anderson 形状给普适小 $\mu^\ast$）不受影响，归属更正为链外-A，详见 `03_推导工作台/链外A_mu星归属更正与落地路径放弃.md`。
**触发**：R67 发现 CQM 自身 $T^\ast$ 式高估 2.65–6.33×，加 $\mu^\ast\approx0.10$ 后落到实验 0.92–1.03×——但 $\mu^\ast=0.10$ 当时是经验取值。本轮检验：链内已有的 Morel–Anderson 形状（`MuStarShape.lean`）+ R25 的 $\varepsilon_F/\hbar\omega_D$ 比值来源，能否解释"为什么 $\mu^\ast$ 是普适小而非常数"——即把经验 $\mu^\ast\approx0.10$ 从拟合参数提升为有链内形状来源的合理值。
**文献标源**：Webb–Marsiglio–Hirsch 综述（arXiv:1502.04724，webfetch 全文核对，L1）给 Morel–Anderson $\mu^\ast=\mu/[1+\mu\ln(\epsilon_F/\hbar\omega_{\log})]$；R25 已把 $\epsilon_F/\hbar\omega_D$ 化为链内声学量组合。只作工具，不声称 CQM 推出自由电子气。
**结论（诚实）**：对典型金属 $L=\ln(\epsilon_F/\hbar\omega_D)=2$–$5$，裸 $\mu=0.2$ 给 $\mu^\ast=0.10$–$0.143$；要 R67 的 $\mu^\ast\approx0.10$，只需裸 $\mu\approx0.125$–$0.20$——落在常规金属裸 Coulomb 范围。**Morel–Anderson 形状把"大的裸 $\mu$"压缩成"小的普适 $\mu^\ast$"，解释了 R67 经验值的合理性**。但仍不闭合 `审-14`（裸 $\mu$、$z_v$、$m$ 外生，不给精确数值）。

---

## 〇、推导前十问核对

非环、无闭合缺口（只定量解释已有经验值）、纯链内形状+标准工具、不改状态。

## 一、链内已有的 $\mu^\ast$ 形状

1. **Morel–Anderson**（MuStarShape.lean，外部标准）：$\mu^\ast=\frac{\mu}{1+\mu\ln(\epsilon_F/\hbar\omega_{\log})}$；
2. **R25**（链内比值来源）：$\frac{\epsilon_F}{\hbar\omega_D}=\frac{\hbar}{2ma}\sqrt{\frac{M}{\kappa_s}}\cdot\frac{(3\pi^2z_vn)^{2/3}}{(6\pi^2n)^{1/3}}$，标度 $\propto n^{1/3}z_v^{2/3}\sqrt{M/\kappa_s}$；
3. **R67**（端到端）：$\mu^\ast\approx0.10$ 对三材料同时给 0.92–1.03×。

## 二、定量解释

令 $L\equiv\ln(\epsilon_F/\hbar\omega_D)$。Morel–Anderson：$\mu^\ast=\frac{\mu}{1+\mu L}$。

| $L$ | $\mu=0.2$ 给 $\mu^\ast$ | 达 $\mu^\ast=0.10$ 需裸 $\mu$ |
|:---|:---|:---|
| 2 | 0.143 | 0.125 |
| 3 | 0.125 | 0.143 |
| 4 | 0.111 | 0.167 |
| 5 | 0.100 | 0.200 |

**关键**：对典型金属 $L=2$–$5$，裸 Coulomb $\mu\approx0.1$–$0.2$（常规范围）经 Morel–Anderson 压制自然给 $\mu^\ast\approx0.10$–$0.14$——R67 的经验 $\mu^\ast=0.10$ 不是一个任意拟合值，而是**落在链内形状 + 合理材料量给出的范围**。

## 三、对 `审-14` 的推进与非推进

- **推进**：解释了 $\mu^\ast$ 为什么是"普适小"（Morel–Anderson 对数压制的必然结果），且 R67 经验值有形状来源；
- **不推进（诚实）**：裸 $\mu$、$z_v$、$m$ 仍外生，不给任一材料的 $\mu^\ast$ 精确数值——`审-14` 整体**不闭合**；
- 这是"形状链内、归一外生"的命题 Z2 又一例。

## 四、历史唯物主义合规

几何/声学量（$\kappa_s,M,a,n$＝基础）决定能标比 $\epsilon_F/\hbar\omega_D$（读数），Morel–Anderson 对数压制把裸 Coulomb 化为有效 $\mu^\ast$（上层建筑式读数）——基础决定上层建筑的实现，不还原、不反向取证，未用社会范畴作物理证据。

## 五、交付

- 核对卡：`03_推导工作台/审14_MorelAnderson形状对R67mu星的解释.md`
- Lean：`05_Lean验证/MuStarShapeExplains.lean`（退出码 0、无禁用项）
- 计算：`04_计算验证/审14_MorelAnderson解释.py`／`.png`／`.csv`／`_摘要.txt`
- 决策记录 `06_决策记录/2026-11-24_R68_mu星形状解释.md`。

## 六、纪律自检

- 碰哪条缺口：`审-14`（定量解释经验值合理性，不闭合）。
- 状态是否变动：**未变动**。不给 $\mu^\ast$ 精确数值、不给 $T_c$。
