# 目标区口径核查：1.13 系数与 $\omega_{\log}$ 对数矩的搭配——BCS 截断 vs Eliashberg 对数矩

**状态**：工作台核查卡；不改权威式、不动缺口编号与状态栏、不动账面。

> **⚠ 后续更新（2026-11-23，防干扰注记）**：本卡发现 $e^{-1/3}$ 口径差后，主链 (目标.2) 已经两次修正——补 $Z=1+\lambda$（`环目标_Z重整化的授权修正.md`）与 Karakozov 前因子 $e^{-1/6}$（`环目标_Karakozov前因子修正.md`），最终 $T^*=1.13e^{-1/6}\hbar\omega_{\log}e^{-(1+\lambda)/\lambda}$，与 Eliashberg Eq37 精确重合、反解偏差 0。本卡所述 $e^{-1/3}$ 混搭的精确分解为对数矩 $e^{-1/3}$（保留）＋Karakozov $e^{-1/6}$（已补），二者已分别处理。本卡保留作历史记录。
**触发**：V2 首次真实数据对照后，回到物理本身核对 (目标.2) $T^*=1.13\hbar\omega_{\log}e^{-1/\lambda}$ 与 (目标.3) $\omega_{\log}^{\rm amp}=e^{-1/3}\theta_D$ 的搭配是否与标准 BCS 一致。
**文献依据**：Webb, Marsiglio & Hirsch, arXiv:1502.04724, **式(1)**（BCS：$T_c=1.13\theta_D e^{-1/[gV]}$）与 **式(2)**（McMillan：$T_c=\frac{\hbar\omega_{\ln}}{1.2k_B}\exp\frac{-1.04(1+\lambda)}{\lambda-\mu^\ast(1+0.62\lambda)}$），已在上轮 webfetch 全文核对。

## 一、核查结论：1.13 配 $\theta_D$，$\omega_{\log}$ 配 $1/1.2$——CQM 是混搭

标准两式（文献逐字）：
- **BCS**（Webb 式1）：$k_BT_c=1.13\,\hbar\omega_D\,e^{-1/\lambda}$，系数 $1.13=2e^\gamma/\pi$ 来自 $\int_0^{\hbar\omega_D}\frac{\tanh(\varepsilon/2k_BT)}{\varepsilon}d\varepsilon\approx\ln\frac{1.13\hbar\omega_D}{k_BT}$——**配 Debye 截断 $\hbar\omega_D$**；
- **McMillan**（Webb 式2）：$T_c=\frac{\hbar\omega_{\ln}}{1.2k_B}\exp(\cdots)$——**配对数矩 $\omega_{\ln}$，系数 $1/1.2$**。

对数矩与截断的关系（3D Debye 谱 $g\propto\omega^2$）：$\omega_{\log}=e^{-1/3}\omega_D=0.7165\,\omega_D$（这正是 (目标.3) 的振幅支）。

**核查发现**：CQM (目标.2) 用 BCS 系数 $1.13$ 乘 $\hbar\omega_{\log}=e^{-1/3}\hbar\omega_D$，得弱耦合极限

$$T^*=1.13\,e^{-1/3}\,\hbar\omega_D\,e^{-1/\lambda}=0.7165\times\bigl(1.13\hbar\omega_D e^{-1/\lambda}\bigr),\tag{C1}$$

即 **CQM 的弱耦合极限比标准 BCS (Webb 式1) 系统性低一个 $e^{-1/3}=0.7165$ 因子**。这是"BCS 系数＋Eliashberg 对数矩"的混搭——若要对齐 BCS 式1，前因子应取 $\hbar\omega_D$（不乘 $e^{-1/3}$）；若要取对数矩，系数不该是 1.13（McMillan 配 $1/1.2$）。

## 二、影响范围（关键：分"形状"与"刻度"）

| 结论 | 是否受 $e^{-1/3}$ 影响 | 理由 |
|:---|:---|:---|
| gap ratio $2\Delta/k_BT^*=2\pi/e^\gamma\approx3.528$ | **不受** | $\Delta(0)=\frac{\pi}{e^\gamma}k_BT^*$，比值与前因子频率无关（V1②/C5 的普适比） |
| $\lambda$ 的形状判据（凹性、扇区结构 $\Delta(1/\lambda)=1/3$） | **不受** | 纯代数，与前因子常数无关 |
| V2 P1/P2/P3（符号、量级、扇区结构） | **不受**（P3 是结构差，与常数无关） | 反解 $\lambda$ 整体平移，判据形式不变 |
| $T_c$ 绝对值 | **受影响** | $T^*\propto e^{-1/3}$ 直接缩小；但 $T_c$ 本就外生（`审-10`／Z2 定位），不闭合 |
| V2 P4（反解 $\lambda$ 数值 vs Eliashberg） | 小幅受影响 | 主因是缺 $\mu^\ast$（Webb 综述确认）；$e^{-1/3}$ 是次要因子 |

**总判定**：这是**刻度层面**的口径不一致，不是**形状层面**的错误。所有已推形状（gap ratio、凹性、扇区结构、标度）不受影响；受影响的 $T_c$ 绝对值本就外生、不闭合。与 `审-15` 的"同形已证、同刻度未证"完全同类。

## 三、为何不改权威式

1. 改 (目标.2) 为 $1.13\hbar\omega_D e^{-1/\lambda}$（对齐 BCS）会与 (目标.3) 的"振幅支进 (目标.2)"冲突，并波及 C5 注记、V1、V2 全部表述；
2. 由于 gap ratio 与前因子无关、$T_c$ 绝对值外生，改式对任何可证伪预测**无改变**，纯属刻度重标定——按"不虚构、不绕过"，不做无预测后果的权威式改动；
3. 正确处置是**加注记**明确：$T^*$ 前因子的 $e^{-1/3}$ 是 CQM 的构造选择（用对数矩替代截断），弱耦合对齐 BCS 时须注意此因子；它不影响普适比与形状。

## 四、回改与交付

- 主链 (目标.2)／(目标.3) 加注记（不动式本身）；
- Lean `05_Lean验证/BCSCoefficient.lean`：前因子结构、gap ratio 与前因子无关、$e^{-1/3}$ 因子代数；
- 数值 `04_计算验证/环目标_113系数口径.py`／`.png`／`.csv`：BCS vs CQM 前因子对比、gap ratio 恒定性、V2 反解两口径对比；
- 决策 `06_决策记录/2026-11-22_113系数口径核查.md`。

## 五、状态

口径核查完成：确认 $e^{-1/3}$ 是"BCS 系数＋Eliashberg 对数矩"混搭的刻度因子；形状层结论全部不受影响、$T_c$ 绝对值仍外生；加注记不改权威式、不动缺口与账面。
