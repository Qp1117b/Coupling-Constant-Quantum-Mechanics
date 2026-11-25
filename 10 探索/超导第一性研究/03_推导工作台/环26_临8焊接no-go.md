# 环 26／`临-8`：物理 $K$ 与 $\zeta$ 形式不可焊接为恒等式——规范读出定理

**状态**：工作台推导卡；未写入主链正文、06、08 台账。
**触发**：研究纲领对 `临-8` 的产出要求是"物理 $K$ 与 $\zeta$ 显式公式的焊接；若不能焊接，给出'只能停在读法'的证明或强证据"。本轮给出**强 no-go**：三种独立理由都指向"不能焊接为恒等式"，并给出正面的替代结论——$\zeta$ 形式是规范截面上的**读出**，不是物理矩阵元。

**一句话**：物理核带**模相关阻尼** $\Gamma_n=\gamma_n^2\sigma_v^2\tau_g$ 与**外生时钟率** $\alpha=\langle v_\tau\rangle/2$，而 (26.2) 右端的衰减率是**模无关**的 $1/2$；只要 $\sigma_v^2\tau_g>0$，物理核与 (26.2) 右端对两个不同零点在代数上不可能相等。若把 $K$ 读作 GLE 摩擦核，则 (26.2) 右端在 $t=0$ 取 $-1<0$，违反正定型核必需的 $K(0)\ge0$。唯一能写 (26.2) 的情形是全对 $\mathcal H_{ij}=0$，那是同步规范的坐标选择（`临-16`），不是材料性质。故 `临-8` 判定为**不可焊接（当前链内）**，$\zeta$ 形式只能作规范读出。

---

## 一、前件

1. 环 26 (26.1b)：单节点时间涨落支给每模衰减
   $$\langle e^{i\Phi_{n,i}}\rangle=e^{i\gamma_n\langle\tau_i\rangle}e^{-\Gamma_nt},\qquad \Gamma_n=\gamma_n^2\sigma_v^2\tau_g. \tag{8W.1}$$
2. 环 26 (26.2)：全对相干（同步规范）给
   $$K_{\zeta}(t)=-\sum_n\frac{e^{i\gamma_n t}}{\rho_n}=e^{-t/2}\bigl(\psi(e^t)-e^t\bigr),\qquad \rho_n=\tfrac12+i\gamma_n. \tag{8W.2}$$
3. 环 26.A2：温度经声子把公共衰减率 $\tfrac12$ 换成 $\alpha=\tfrac{\langle v_\tau\rangle}{2}$，并给每模加 (8W.1) 的 $\Gamma_n$。
4. 链内判定（环 26 五区）：全对 $\mathcal H_{ij}=0$ 是**同步规范的坐标选择**，不是物理机制（`临-16`）；质数振荡在锚外，锚把振荡冻成等高平台。
5. 外部标准（只作工具，不作 CQM 结论）：
   - von Mangoldt 显式公式 $\psi(x)=x-\sum_\rho x^\rho/\rho-\log 2\pi-\frac12\log(1-x^{-2})$，零点和为**条件收敛**，须按共轭对对称求和（von Mangoldt 1895；Baez, *Explicit Formulas*；Kedlaya, *von Mangoldt's formula*, Theorem 10.1）；
   - 零点成对给 $x^\rho/\rho+x^{\bar\rho}/\bar\rho=2x^\beta\cos(\gamma\ln x-\arg\rho)/|\rho|$（同上）；
   - GLE 摩擦核若要有平稳解，延拓后必须是**正定型函数**，即 $\widehat\gamma(\omega)\succurlyeq0$，从而 $|K(t)|\le K(0)$、特别 $K(0)\ge0$（Kubo；arXiv:2507.17350, Remark 5 与 Theorem 3；Mori–Zwanzig 的第二 FDT 实为记忆核的隐式定义，arXiv:2503.20457）；
   - L14–L16：零点谱模型／统计类比不提供电子配对矩阵元（已登记于 `01_文献基线/文献基线.md` §3.4）。

---

## 二、No-go A：模相关阻尼 vs 模无关率（链内、纯代数）

由 (8W.1)，物理核第 $n$ 模的振幅衰减为

$$A_n^{\rm phys}(t)=e^{-(\alpha+\Gamma_n)t}=e^{-\left(\frac{\langle v_\tau\rangle}{2}+\gamma_n^2\sigma_v^2\tau_g\right)t}. \tag{8W.3}$$

而 (8W.2) 的每一模公共衰减为 $e^{-t/2}$，与 $n$ **无关**。两条直接结论：

**(A1) 率相同的必要条件**。若对某个模 $n$ 有 $A_n^{\rm phys}(t)=e^{-t/2}$ 对所有 $t$ 成立，则由 $t=1$ 处 $\exp$ 的单射性

$$\frac{\langle v_\tau\rangle}{2}+\gamma_n^2\sigma_v^2\tau_g=\frac12. \tag{8W.4}$$

**(A2) 两个模不能同时满足**。取 $n\ne m$，(8W.4) 两式相减：

$$(\gamma_n^2-\gamma_m^2)\,\sigma_v^2\tau_g=0. \tag{8W.5}$$

非平凡零点纵坐标互异（$\gamma_n^2\ne\gamma_m^2$），故只要 $\sigma_v^2\tau_g>0$ 就不成立。

**判定**：物理核**逐模**匹配 (8W.2) 需要无穷多个形如 (8W.4) 的等式同时成立，而它们对 $n$ 的依赖不同——$\sigma_v^2\tau_g>0$ 时最多只能满足一个模。这不是"还没算出权重"，而是**结构不相容**。$\zeta$ 形式的均匀衰减率 $1/2$ 与物理涨落支的模相关率 $\gamma_n^2\sigma_v^2\tau_g$ 不能共存。

> 注意：即使退到 $\sigma_v^2\tau_g=0$（无时间涨落），(8W.4) 仍要求 $\langle v_\tau\rangle=1$——一个无量纲归一化条件。$\langle v_\tau\rangle$ 是链内的时钟率，没有理由恒等于 $1$；它随外参与材料变（26.A3）。故"率对齐"本身也是额外规范条件。

---

## 三、No-go B：正定型（条件于 GLE 读法）

若把 $K$ 读成 GLE 摩擦核（唯一有标准物理矩阵元的读法），则由第二 FDT，延拓后的核必须正定型：

$$|K(t)|\le K(0)\quad\forall t,\qquad\text{特别}\quad K(0)\ge0. \tag{8W.6}$$

而按 (26.2) 的链内约定（常数项吸收，主项＋零点项）

$$K_\zeta(0)=\psi(1)-1=0-1=-1<0. \tag{8W.7}$$

**判定**：(8W.2) 右端**不是正定型核**，故即使只要求"物理上可作为摩擦核的最低条件"，焊接也失败。 fuller 显式公式还含 $-\log2\pi$ 与平凡零点项，它们在 $x\to1^+$ 发散，使问题更严重，不会更轻。

**边界**：链已明确" $K$ 不是 GLE 摩擦核"（`2026-11-22_三项平衡与临25判定.md`），故本条是**条件性**的：它排除的是"把 zeta 核当摩擦核"这一读法，不排除 CQM 自定义的"总效应"读法。No-go A 不依赖这个读法，是更强的主证。

---

## 四、No-go C：全对 $\mathcal H_{ij}=0$ 是规范，不是物理

(26.2) 只在"全对 $\mathcal H_{ij}=0$"时成立，而环 26 五区表明确写这是**同步规范的坐标选择**（(22.4)、`临-16`）。在此规范下各节点固有时被强行对齐：

$$\tau_i=t\quad\forall i \quad\Rightarrow\quad \langle e^{i\Phi_{n,i}}\rangle=e^{i\gamma_n t}e^{-\Gamma_nt}. \tag{8W.8}$$

但物理读数只依赖**相位差的历史** $\mathcal H_{ij}=\tau_i-\tau_j$；把全部 $\tau_i$ 平移到同一值是坐标规范，不改变任何可观测量。因此由规范选择得到的 (26.2) 形式**不能被赋予物理矩阵元的意义**。

**判定**：三条 no-go 覆盖五个区的全部物理情形——前夜·涨落由 A 排除，GLE 读法由 B 排除，全对相干由 C 排除，前夜·未冻结与锚核内因 $K$ 随时间漂／冻结而根本不是 (8W.2) 的时间依赖形式。

---

## 五、正结果：$\zeta$ 形式是规范截面上的读出（滤波器定理）

把 (8W.3) 与 (8W.2) 的模比率写成

$$W_n(t)\equiv\frac{A_n^{\rm phys}(t)}{e^{-t/2}}=\exp\!\left[-\left(\alpha+\Gamma_n-\tfrac12\right)t\right]. \tag{8W.9}$$

于是

$$K_{\rm phys}(t)=-\sum_n\frac{e^{i\gamma_n t}}{\rho_n}\,W_n(t). \tag{8W.10}$$

**滤波器定理**：

1. $W_n$ 不是标量而是**逐模**的；物理核是 $\zeta$ 核经逐模滤波得到，故两者一般不相等（由 A）；
2. 理想极限 $\sigma_v^2\tau_g\to0$ 且 $\alpha\to\tfrac12$ 给 $W_n\equiv1$，此时 (8W.10) 退化为 (8W.2)——这是一个**规范极限**，不是材料可达状态；
3. $\zeta$ 形式是 (8W.10) 在规范截面 $W_n\equiv1$ 上的**代表元**（读出器），而不是独立的物理核。

**这给了 `临-8` 一个明确答案**：焊接不是"还没做到"，而是"作为恒等式不可能；作为规范截面的读数已由 (8W.9)(8W.10) 给出"。

---

## 六、Lean 承载

`../05_Lean验证/MemoryKernelWelding.lean`：

- `gamma_sq_ne_of_gamma_ne`：非零异号纵坐标的平方不等（作为代数引理）；
- `Gamma_ne_of_gamma_sq_ne`：$\sigma_v^2\tau_g>0$ 且 $\gamma_n^2\ne\gamma_m^2$ ⇒ $\Gamma_n\ne\Gamma_m$；
- `exp_rate_injective`：$\forall t,\ \exp(-at)=\exp(-bt)\Rightarrow a=b$（用 $t=1$ 与 `Real.exp_injective`）；
- `single_mode_rate`：单模对齐 (8W.4) 的充要条件；
- `mode_no_go`：两个不同模不能同时对齐（No-go A 的代数核）；
- `alpha_must_be_half`：$\sigma_v^2\tau_g=0$ 时对齐仍要求 $\alpha=1/2$；
- `positive_type_zero_nonneg`：正定型核必满足 $K(0)\ge0$（No-go B 的代数核）；
- `zeta_kernel_zero_neg`：链内约定下 $K_\zeta(0)=-1<0$；
- `gauge_coincidence`：读数同一要求节点固有时相同（No-go C 的代数核）；
- `W`（定义）与 `W_eq_one`：滤波器定义及 $W=1\iff$ 总率为 $1/2$（$t\ne0$）；
- `W_at_ideal`：理想极限 $\alpha=1/2$、$\Gamma=0$ 给 $W=1$；
- `filter_ne_of_Gamma_ne`：$\Gamma_n\ne\Gamma_m$ ⇒ 两滤波器在 $t\ne0$ 处不等（滤波器逐模性）。

未形式化：显式公式的收敛与共轭配对（外部标准）、正定型核的傅里叶刻画（外部标准）、$\psi(1)=0$ 的数论定义（由外部事实直接取 $K_\zeta(0)=-1$）。无 `axiom`、`sorry`、`admit`、`native_decide`、`unsafe`。

---

## 七、数值核对

`../04_计算验证/环26_临8焊接no-go.py`：

1. 滤波器 $W_n(t)=\exp[-\Gamma_nt]$（前三零点 $\gamma_1=14.134725141$、$\gamma_2=21.022039639$、$\gamma_3=25.010857580$，取 $\sigma_v^2\tau_g=10^{-3}$）：三条不同斜率 vs $\zeta$ 参考线 $W=1$；
2. 逐模衰减率 $\alpha+\Gamma_n$ vs 统一率 $1/2$ 的水平线；
3. 截断实核 $K_N(t)=-\sum_{n=1}^{3}\frac{\cos\gamma_nt+2\gamma_n\sin\gamma_nt}{1/4+\gamma_n^2}$ 随 $t$ 的振荡，显示变号与非正定型形状；
4. no-go 区域图：$(\sigma_v^2\tau_g,|\gamma_n^2-\gamma_m^2|)$ 平面中只有两轴可对齐，内部全禁。

外部零点数值只作示意，不参与定理；定理只用 $\gamma_n^2\ne\gamma_m^2$。

---

## 八、不能推出

1. **不能推出物理 $K$ 等于 (26.2) 右端**：三条 no-go 明确否定恒等式。
2. **不能推出 $\zeta$ 零点给出配对矩阵元**：这只把数论谱当读出器，与 L14–L16 一致。
3. **不能由 no-go B 否定 CQM 的 $K$**：它只在 GLE 读法下成立，链已声明 $K$ 不是 GLE 摩擦核；主证是 A。
4. **不能推出 RH**：No-go A 只用 $\gamma_n^2\ne\gamma_m^2$，不涉及零点是否共线；$K(t)=O(e^{\varepsilon t})\iff$ RH（26.A2）仍属 S1 层，与本条无关。
5. **不能推出外参能抹掉质数形式**：26.A3 已判结构判据不变，本条只说读出形式不能被当成物理核。
6. **不能改主链 (26.2) 的数学身份**：零点和＝von Mangoldt 右端是标准数学，本条只否定"物理 $K$＝该右端"。
7. **不能推出材料可达规范极限**：$\alpha=1/2$、$\sigma_v=0$ 是规范条件，不是可制备态。

---

## 九、状态与缺口

**已确认（代数严格）**：

- (8W.5)：两个不同模不能同时满足率对齐，只要 $\sigma_v^2\tau_g>0$；
- (8W.6)(8W.7)：链内约定下 zeta 核不是正定型核；
- (8W.9)(8W.10)：物理核＝逐模滤波的 zeta 核，zeta 形式是规范截面代表元。

**判定**：

- `临-8` 判定为**不可焊接（当前链内）**：作为恒等式不可能；作为规范截面读出已给出显式滤波器；
- 保留编号与"未闭合"状态，不升状态、不自造新编号；不删主链 (26.2) 的数学内容。

**未闭合／挂账**：

- 若要正面焊接，必须新增一条把 $\sigma_v^2\tau_g$ 与 $\alpha-1/2$ 强制归零的物理公设——链内无此公设，且它等价于把涨落抹掉，属新假设，不引入；
- `G22`（表示论证明）、`临-17`（$\{c_{ij}\}$ 分布）、`临-24`（归一接口）均不动；
- 06 原文、主链状态栏、08 台账未改。
