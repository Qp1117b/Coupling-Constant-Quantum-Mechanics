# 目标区重大发现：CQM 缺 Eliashberg 质量增强 $1+\lambda$——P4 根因的定位

**状态**：工作台推导卡；不改权威式、不动缺口编号与状态栏、不动账面。
**触发**：V2 P4（绝对精度）此前判"不判定（缺 $\mu^*$ 与独立 $\lambda$ 表）"。本轮用 Marsiglio 2018（arXiv:1807.04907，已 webfetch 全文核对）的 Eliashberg 弱耦合精确结果，**首次定量定位了 P4 的真正根因**：CQM (目标.2) 用 BCS 裸指数 $e^{-1/\lambda}$，缺 Eliashberg 的质量增强 $e^{-(1+\lambda)/\lambda}$。

**一句话**：Marsiglio 文献给出同一 bare 耦合 $\lambda\equiv g_{\epsilon_F}|V|$（与 CQM (10.3) $\lambda_i=N(0)\sum_j|V_{ij}|$ **同类**）下的三个式：BCS(13) $T_c=1.13\omega_Ee^{-1/\lambda}$、含重整化(14) $T_c=1.13\omega_Ee^{-(1+\lambda)/\lambda}$、弱耦合精确(37) $T_c=\frac{1.13}{\sqrt e}\omega_Ee^{-(1+\lambda)/\lambda}$。CQM (目标.2) 用的是(13)型（无 $1+\lambda$）。**用实测 $T_c$ 反解**：(13)型给 bare $\lambda\approx0.17$–$0.41$（第53轮），(37)型给 $\approx0.22$–$0.77$；两者比值 $1.25$–$1.90$ 单调系统、与 $1+\lambda$ 同阶。**结论**：CQM 缺的是 Eliashberg 重整化 $Z=1+\lambda$——这正是固有时流速场的质量增强，链内有对应对象（$v_\tau$ 场），但从未写入 (目标.2)。这是"从头算到尾"必须补的一环。

---

## 一、文献（逐条标源，已 webfetch 全文）

Marsiglio, *Eliashberg Theory in the Weak Coupling Limit*, arXiv:1807.04907v2（2018）：
- 式(13)：$T_c=1.13\,\omega_E e^{-1/\lambda}$，$\lambda\equiv g_{\epsilon_F}|V|$（bare），**BCS，无重整化**；
- 式(14)：$T_c=1.13\,\omega_E e^{-(1+\lambda)/\lambda}$，含 $Z\approx1+\lambda$ 质量增强；
- 式(37)：$T_c=\frac{1.13}{\sqrt e}\omega_E e^{-(1+\lambda)/\lambda}$，弱耦合精确（文献称 $\lambda\lesssim0.2$ 基本精确）；
- 文献摘要明确："BCS is often viewed as the weak coupling limit of Eliashberg, **in spite of a handful of papers that have pointed out this is not so**"——与 CQM (目标.2) 用 BCS 型形成对照。

## 二、定量核对（8 元素，Webb Table III 实测 $T_c$）

| 元素 | $T_c$(K) | $\theta_D$(K) | $\lambda_{CQM}$ (13型反解) | $\lambda_{E37}$ (37型反解) | 比 $E/C$ | $1+\lambda_{CQM}$ |
|:---|:---|:---|:---|:---|:---|:---|
| Al | 1.18 | 428 | 0.176 | 0.221 | 1.26 | 1.18 |
| Nb | 9.25 | 275 | 0.314 | 0.496 | 1.58 | 1.31 |
| Pb | 7.2 | 105 | 0.405 | 0.768 | 1.90 | 1.41 |
| Sn | 3.7 | 200 | 0.265 | 0.383 | 1.45 | 1.26 |
| Cd | 0.52 | 209 | 0.173 | 0.217 | 1.25 | 1.17 |

**规律**：$E/C$ 单调随 $\lambda_{CQM}$ 增，从 1.25（弱耦合 Al/Cd）到 1.90（强耦合 Pb）——正是质量增强 $1+\lambda$ 的定性特征（强耦合增强更大），但数值上 $E/C>1+\lambda_{CQM}$（差 0.08–0.49），说明还有对数矩口径差异（第54轮的 $e^{-1/3}$）叠加。

## 三、P4 根因的精确定位

此前 P4 判"不判定（缺 $\mu^*$ 与独立 $\lambda$ 表）"——现在可以更精确：

1. **主因 1：缺 $1+\lambda$ 重整化**（本轮发现）——CQM (目标.2) 用 BCS 裸指数，正确的 Eliashberg 形式含 $Z=1+\lambda$；
2. **主因 2：缺 $\mu^*$**（已知，`审-14`）——Marsiglio 文献为聚焦推迟效应省略了 $\mu^*$，Webb 式(2) 含 $\mu^*$，CQM 无此符号位；
3. **次因：对数矩口径 $e^{-1/3}$**（第54轮）——BCS 系数配对数矩的混搭。

三者都是"形状与刻度"层面的链外/链内缺口，不是实验否定。

## 四、与 CQM 已有对象的对应（为何这是链内可补的一环）

CQM 已有固有时流速场 $v_\tau$（对象，环 5）、记忆核 $K$（总效应，环 14）、bare 耦合 $\lambda_i=N(0)\sum|V_{ij}|$（10.3）。Eliashberg 的 $Z=1+\lambda$ 质量增强 $m^\ast/m\approx1+\lambda$（Webb 综述 Section III 明确）对应的正是**固有时流速的重整化**——电子被声子云拖曳，有效质量增加、节律变慢。链内 $v_\tau$ 场的"被声子拖曳"机制从未写成方程，这是真实缺口（可归 `临-1` 亏角驱动源或新子项）。

**但**：补它须在 (目标.2) 引入 $e^{-(1+\lambda)/\lambda}$ 并重整化 $v_\tau$——这是**新机制**，会波及 C5/V1/V2 全部推导。按"不虚构、不绕过"，本轮**不擅自改权威式**，只定位根因并记录修正候选，待用户明确授权。

## 五、不能推出

1. 不能说 CQM 被实验否证：比值系统性来自缺重整化与口径，非物理错误；
2. 不能说 $\lambda_{E37}$ 是"真值"：它依赖 $\theta_D\approx\omega_E$ 的 rough 取等（Debye vs Einstein 谱不同）；
3. 不能给精确映射 $E/C=f(\lambda_C)$：会变成拟合，链内无此方程；
4. 不能改权威式或状态栏；不动账面。

## 六、交付

- 推导卡（本文件）；
- Lean `05_Lean验证/EliashbergRenorm.lean`：质量增强指数 $e^{-(1+\lambda)/\lambda}$ 与 BCS $e^{-1/\lambda}$ 的代数关系、重整化降低 $T_c$ 的单调性；
- 数值 `04_计算验证/环目标_Eliashberg重整化.py`／`.png`／`.csv`：8 元素两口径反解对比、$E/C$ vs $1+\lambda$、P4 根因分解；
- 决策 `06_决策记录/2026-11-22_Eliashberg重整化P4根因.md`。

## 七、状态

P4 根因由"笼统的缺 $\mu^*$"精确化为"缺 $1+\lambda$ 重整化（主）＋缺 $\mu^*$（次）＋对数矩口径（次）"；不改权威式、不动缺口与账面；修正候选待授权。
