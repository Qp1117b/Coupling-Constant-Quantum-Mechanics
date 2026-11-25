# 目标区：`\mu^\ast` 的形状归口——从"完全外生"推进为"泛函形状已知、材料值外生"

**状态**：工作台推导卡；不改主链权威式、不动缺口编号与状态栏、不动账面。
**触发**：59 轮后绝对 $T_c$ 的唯一链外理论输入是 $\mu^\ast$（`审-14`）。但此前把它当"完全外生"是不精确的——Webb 2015 综述式(5) 给了它的泛函形状。本轮按用户"一环不能缺"要求，把 $\mu^\ast$ 像 $\kappa_f$、$\omega_{\log}$ 一样推进为"形状已推、数值外生"。
**文献依据**：Webb, Marsiglio & Hirsch, arXiv:1502.04724 式(5)：$\mu^\ast=\frac{\mu}{1+\mu\ln(\epsilon_F/\hbar\omega_D)}$，极限 $\mu^\ast\to1/\ln(\epsilon_F/\hbar\omega_D)$；正文明确"typically $\epsilon_F\gg\hbar\omega_D$ so $\mu^\ast\ll\mu$"、Al 需 $\mu^\ast\approx0.1$–$0.2$。（已 webfetch 全文核对）

**一句话**：$\mu^\ast$ 不是无结构的自由参数——它有明确的**对数重整化形状**（Morel-Anderson 方程），由 bare 库仑 $\mu$、Fermi 能 $\epsilon_F$、Debye 能 $\hbar\omega_D$ 三者决定。链内已有 (目标.2) 的 $\omega_D$、区间 [0,1/2] 端点分类（`审-10`），但无 $\epsilon_F$、$\mu$ 的对应对象。故 $\mu^\ast$ 应归为：**泛函形状已知（外部标准）＋端点/极限链内可判（$\mu^\ast\to0$ 当 $\epsilon_F/\omega_D\to\infty$）＋材料值（$\mu,\epsilon_F$）外生**。这样绝对 $T_c$ 的"还差什么"从笼统的"$\mu^\ast$ 外生"精确为两个具体材料量。

---

## 一、$\mu^\ast$ 的形状（外部标准，逐条标源）

$$\mu^\ast=\frac{\mu}{1+\mu\ln(\epsilon_F/\hbar\omega_D)},\qquad \mu=g(\epsilon_F)U\ (\text{bare Coulomb}),\qquad \mu^\ast\xrightarrow[\epsilon_F\gg\hbar\omega_D]{}\frac{1}{\ln(\epsilon_F/\hbar\omega_D)}.\tag{M.1}$$

（Webb 式(5)；Morel & Anderson 1962，Phys. Rev. 125 1263。）

**三个定性结论**（链内可核对）：
1. $\mu^\ast<\mu$ 恒成立（分母 >1）——推迟效应削弱库仑排斥；
2. $\epsilon_F/\hbar\omega_D\to\infty$ ⇒ $\mu^\ast\to0$（绝热极限无赝势效应）；
3. $\mu>0$ ⇒ $\mu^\ast>0$，且 $\mu^\ast$ 单调随 $\mu$ 增。

## 二、与 CQM 框架的对应（哪些链内可判）

| $\mu^\ast$ 的决定因素 | CQM 链内对应 | 状态 |
|:---|:---|:---|
| $\hbar\omega_D$（Debye 能） | `审-10` 已钉：谱支集 $\omega_D$，外生能标 | 外生（已知位置） |
| $\epsilon_F$（Fermi 能） | 链无对应对象（无费米面能标） | **链外新输入** |
| $\mu=g(\epsilon_F)U$（bare 库仑） | 链无库仑排斥通道（`链外-A` 只记 $V<0$ 恒成立） | **链外新输入** |
| 对数重整化形状 M.1 | 外部标准（Morel-Anderson） | 形状已知 |

**判定**：$\mu^\ast$ 的形状已知、$\omega_D$ 位置已知，但 $\epsilon_F$、$\mu$ 两个材料量链内无对象——这是绝对 $T_c$ 的**精确缺口清单**（比"笼统 $\mu^\ast$ 外生"更具体）。

## 三、用实测 $\mu^\ast$ 做终局代入判定（数值，非拟合）

McMillan/Allen-Dynes 文献给元素实测 $\mu^\ast$（Al $\approx0.1$–$0.2$、Nb $\approx0.13$、Pb $\approx0.15$、Sn $\approx0.14$，取标准值区间）。把 CQM 最终 $T^*$ 式（$1.13e^{-1/6}\hbar\omega_{\log}e^{-(1+\lambda)/\lambda}$）用 **Allen-Dynes 形式**（含 $\mu^\ast$）做绝对 $T_c$ 正算：

$$T_c=\frac{\hbar\omega_{\log}}{1.2k_B}\exp\!\left[\frac{-1.04(1+\lambda)}{\lambda-\mu^\ast(1+0.62\lambda)}\right].\tag{M.2}$$

CQM 已对齐 bare $\lambda$（第56–57轮）与 $\omega_{\log}=e^{-1/3}\theta_D$（(目标.3)）；只剩 $\mu^\ast$ 取实测。这是**首次绝对 $T_c$ 正算**——但必须诚实：M.2 是 Eliashberg 标准式（外部），CQM 贡献的是 $\lambda$、$\omega_{\log}$ 两个输入；用实测 $\mu^\ast$ 代入检验 **CQM 输入是否让标准式复现实验 $T_c$**。

## 四、不能推出

1. **不能说 $\mu^\ast$ 链内推出**：形状外部标准，$\epsilon_F$、$\mu$ 材料外生；
2. **不能说绝对 $T_c$ 纯链内算出**：M.2 是外部 Eliashberg 式，$\mu^\ast$ 实测；
3. 不能把实测 $\mu^\ast$ 调参贴合 $T_c$（协议禁止）——$\mu^\ast$ 取文献标准值，不反推；
4. 不能改权威式、状态栏、账面。

## 五、交付

- 推导卡（本文件）；决策 `06_决策记录/2026-11-23_mu星形状归口.md`；
- Lean `05_Lean验证/MuStarShape.lean`：M.1 形状不等式（$\mu^\ast<\mu$、单调、极限）；
- 数值 `04_计算验证/环目标_mu星与绝对Tc.py`／`.png`／`.csv`：M.1 形状曲线＋M.2 绝对 $T_c$ 正算（实测 $\mu^\ast$）；
- `成果登记.md`、README。

## 六、状态

$\mu^\ast$ 从"完全外生"推进为"泛函形状已知（M.1）＋$\epsilon_F$、$\mu$ 材料外生"；绝对 $T_c$ 缺口精确到两个材料量；用实测 $\mu^\ast$ 做首次绝对 $T_c$ 正算（标注外部式来源）。不改编号、状态栏、账面。
