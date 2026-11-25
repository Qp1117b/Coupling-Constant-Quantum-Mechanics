# 环 19：Pearl–London 口径统一（约定因子、无约定不变量与简并度）

**前件**：第 151 轮 (19W.1)–(19W.10)（读出映射、BKT 无参数线、双边界、可辨识性）；L151j（Pearl 长度 $\Lambda=2\lambda_L^2/d$）；环 10 的 $\Upsilon(T)=\Upsilon_0w(T)$（R-08）。

**本轮任务**：消解 (19W.1) 的"把报告值读作 $\Lambda$ 还是 $\lambda_L$"歧义——给出 (i) 文献约定因子的完整记账；(ii) 不依赖约定的读法；(iii) $({\lambda_L},d)$ 的简并度与可辨识条件；(iv) 更正第 151 轮混用约定造成的因子 $2$。**不新增缺口编号，不改任何缺口状态**；`审-4`、`审-6` 状态栏不动。

**分层声明**：【外部标准】＝Pearl 长度定义、片动能电感与刚度关系、局域极限条件（逐条给 arXiv/DOI）；【链内识别】＝$\Upsilon=\Upsilon_0w$ 与 $\mathcal{B}$ 的定义。二者不互相提升。

---

## 结论先行

1. **文献中 Pearl 长度有两种约定，差一个因子 $2$**。$\Lambda=2\lambda_L^2/d$（Pearl 原始定义，L151j／L152b）与 $\Lambda=\lambda_L^2/d$（薄膜 SQUID 分析，L152c）并存。记
   $$\Lambda\equiv c_\Lambda\,\frac{\lambda_L^2}{d},\qquad c_\Lambda\in\{1,2\}. \tag{19PL.1}$$
   任何"Pearl 长度数值"必须声明 $c_\Lambda$，否则不可比。

2. **二维相位刚度只依赖组合 $\lambda_L^2/d$，与约定因子无关**：
   $$\Upsilon=\frac{\hbar^2}{4\mu_0e^2}\,d\,\lambda_L^{-2}=\frac{C_\Upsilon\,c_\Lambda}{\Lambda},\qquad C_\Upsilon\equiv\frac{\hbar^2}{4\mu_0e^2}=8.619\times10^{-26}\ \text{J}\cdot\text{m}. \tag{19PL.2}$$
   $c_\Lambda=2$ 时退化为 (19W.1) 的 $\frac{\hbar^2}{2\mu_0e^2}\Lambda^{-1}$。**约定因子只改常数，不改物理**。

3. **存在无约定读法：片动能电感 $L_{k\square}$**。薄膜每方动能电感 $L_{k\square}=\mu_0\lambda_L^2/d$（【外部标准】，L152d 的 $J_s$ 式同构），则
   $$\Upsilon=\frac{\hbar^2}{4e^2L_{k\square}}=\frac{\Phi_0^2}{4\pi^2L_{k\square}},\qquad L_{k\square}=\frac{\mu_0}{c_\Lambda}\Lambda. \tag{19PL.3}$$
   (19PL.3) **不含 $c_\Lambda$**，且 $L_{k\square}$ 由微波谐振直接测（L152e／L152g）。这是口径统一的可操作出口：**CQM 的读出变量应取 $L_{k\square}$（或 $\Upsilon$），而不是"穿透深度"**。

4. **第 151 轮的 $176.33$ 是 $c_\Lambda=1$ 的值，被写在了 $c_\Lambda=2$ 的式子下**。按其自身定义 (19W.1)，两读法之比应为
   $$\frac{\Upsilon_A}{\Upsilon_B}=\frac{c_\Lambda x}{d}\qquad(x=\text{报告值，当 }\lambda_L\text{ 读时}), \tag{19PL.4}$$
   $c_\Lambda=2$ 给 $352.67$／$160.0$／$60.0$（$d=3/5/10$ nm，$x=529/400/300$ nm）；$c_\Lambda=1$ 给第 151 轮所记 $176.33$／$80.0$／$30.0$。**两组都对，但必须标约定**；第 151 轮文字未标，已按标准 $c_\Lambda=2$ 更正并保留两组值。

5. **$({\lambda_L},d)$ 有精确一参数简并**：
   $$(\lambda_L,d)\mapsto(s\lambda_L,s^2d)\quad\Longrightarrow\quad \Upsilon\ \text{不变}\quad\forall s>0. \tag{19PL.5}$$
   故**只测刚度不能同时定 $\lambda_L$ 与 $d$**；凡文献同时给出二者，必另有独立的 $d$ 测量（如双线圈法扣除死层，L152f）。这不是模型缺陷，是映射的秩亏。

6. **应用域**：由 $L_{k\square}$ 反推 $\lambda_L$ 需局域极限 $\xi\ll\lambda_L$（L152e 明确指出非局域区该关系失效）；而**由 $L_{k\square}$ 读 $\Upsilon$ 不需要该极限**——刚度是系数本身，$\lambda_L$ 是派生物。这进一步支持把 $\Upsilon$／$L_{k\square}$ 作基本读数。

7. **BKT 线也有无约定形式**。把 (19PL.3) 代入 $\Upsilon_R(T_c^-)=\frac{2}{\pi}k_BT_c$：
   $$L_{k\square}(T_c^-)=\frac{\pi\hbar^2}{8e^2k_BT_c}\ \ \Longleftrightarrow\ \ \Lambda(T_c^-)=\frac{C_\Lambda}{T_c},\quad C_\Lambda=\frac{\pi\hbar^2}{4\mu_0e^2k_B}, \tag{19PL.6}$$
   两式对所有 $c_\Lambda$ 同时成立（$L_{k\square}=\mu_0\Lambda/c_\Lambda$ 与 $C_\Lambda$ 中的 $\mu_0$ 相消）。故 $\mathcal{B}$ 可写成**无约定的动能电感比**
   $$\mathcal{B}=\frac{T_c\Lambda(0)}{C_\Lambda}=\frac{L_{k\square}(0)}{L_{k\square}^{\rm BKT}(T_c)}\in[0,1]. \tag{19PL.7}$$
   $\mathcal{B}$ 的分域判定（D2／D3）因此与约定无关。

> **与第 151 轮的关系**：(19W.2)–(19W.10) 在 $c_\Lambda=2$ 下全部有效；本轮只更正 (19W.1) 之后 §一／A3 的**文字比值**，不改 (19W.2) 的 $C_\Lambda$、不改 §七 $\mathcal{B}$ 的数值（§七原本就用 $c_\Lambda=2$，与 (19PL.1) 一致）。

---

## 一、定义链与约定因子

三个长度／电感量逐级定义（【外部标准】）：

$$\lambda_L^{-2}=\frac{\mu_0n_se^2}{m},\qquad \Lambda\equiv c_\Lambda\frac{\lambda_L^2}{d},\qquad L_{k\square}\equiv\frac{\mu_0\lambda_L^2}{d}. \tag{19PL.8}$$

$n_s$ 为电子密度、$m$ 为电子质量（配对因子已并入，见第 151 轮 §一）。三者的换算：

$$L_{k\square}=\frac{\mu_0}{c_\Lambda}\Lambda=\frac{\mu_0\lambda_L^2}{d}. \tag{19PL.9}$$

**约定因子的来源**：Pearl 原始推导给 $2\lambda_L^2/d$（L151j／L152b）；薄膜 SQUID 的线性响应分析把 $\Lambda$ 取为 $\lambda_L^2/d$（L152c）。两文用的是同一个物理长度，差的是"是否把 $2$ 吸收进符号"。因此**任何引用"Pearl 长度"的数值必须同时给 $c_\Lambda$**。

**第三个约定入口**：$d$ 本身可能是"有效厚度" $d_{\rm BKT}$（L151i 讨论过超导层数折算），死层扣除可带来约 $25\%$ 的 $\lambda$ 误差（L152f）。这属实验提取口径，不改 (19PL.1) 的结构；引用时须注明 $d$ 是几何厚度还是有效厚度。

## 二、无约定不变量与三个等价表述

直接把 $\lambda_L^{-2}=\mu_0n_se^2/m$ 代入二维刚度（与前轮同法）：

$$\Upsilon=\frac{\hbar^2}{4m}n_sd=\frac{\hbar^2d}{4\mu_0e^2\lambda_L^2}. \tag{19PL.10}$$

由 $L_{k\square}=\mu_0\lambda_L^2/d$ 得

$$\Upsilon=\frac{\hbar^2}{4\mu_0e^2}\cdot\frac{d}{\lambda_L^2}=\frac{\hbar^2}{4e^2L_{k\square}}.$$

再用 $\hbar/(2e)=\Phi_0/(2\pi)$ 得 $\Upsilon=\Phi_0^2/(4\pi^2L_{k\square})$。**三个等价表述**：

| 表述 | 式子 | 是否含 $c_\Lambda$ | 直接可测性 |
|:---|:---|:---:|:---|
| London 长度 | $\Upsilon=\frac{\hbar^2}{4\mu_0e^2}d\lambda_L^{-2}$ | 否 | 需先由 $L_{k\square}$ 反推 $\lambda_L$（需局域极限） |
| Pearl 长度 | $\Upsilon=\frac{C_\Upsilon c_\Lambda}{\Lambda}$ | **是** | 需知道 $c_\Lambda$ |
| 片动能电感 | $\Upsilon=\frac{\hbar^2}{4e^2L_{k\square}}$ | 否 | 微波谐振直测（L152e／L152g） |

**判据**：CQM 的对应域判据一律写成第三种。这样"报告值读作 $\Lambda$ 还是 $\lambda_L$"不再进入判据——它只影响**报告者内部**的换算，不影响 $\Upsilon$。

## 三、简并度与可辨识性

(19PL.10) 的右端只含组合 $\lambda_L^2/d$。设 $(s\lambda_L,s^2d)$，则

$$\frac{s^2d}{(s\lambda_L)^2}=\frac{d}{\lambda_L^2}\quad\Longrightarrow\quad\Upsilon(s\lambda_L,s^2d)=\Upsilon(\lambda_L,d).$$

即 (19PL.5)。**后果**：

1. 单条 $\Upsilon(T)$ 曲线不能定 $\lambda_L$ 与 $d$ 两个量，只能定 $\lambda_L^2/d$（等价于定 $\Lambda$ 或 $L_{k\square}$）；
2. 文献若同时报 $\lambda_L$ 与 $d$，其 $d$ 必来自独立测量；引用时应追踪 $d$ 的出处，而非把它当 (19PL.10) 的解；
3. 第 151 轮"两读法之比"本质是**同一简并轨道上两个假设点**的 $\Upsilon$ 比，不是两种物理。

## 四、第 151 轮因子 $2$ 的更正

第 151 轮 §一写"两式之比为 $\Lambda/d$；$\Upsilon_A/\Upsilon_B=x/d$"，A3 记 $176.33$／$80.0$／$30.0$。按其自身定义 (19W.1)（$\Lambda=2\lambda_L^2/d$）复核：

$$\Upsilon_A=\frac{\hbar^2}{2\mu_0e^2x}=\frac{C_\Upsilon\cdot2}{x},\qquad \Upsilon_B=\frac{\hbar^2d}{4\mu_0e^2x^2}=\frac{C_\Upsilon d}{x^2},$$

$$\frac{\Upsilon_A}{\Upsilon_B}=\frac{2C_\Upsilon/x}{C_\Upsilon d/x^2}=\frac{2x}{d}=\frac{\Lambda}{\lambda_L}. \tag{19PL.11}$$

$d=3$ nm、$x=529$ nm 给 $352.67$，不是 $176.33$。**成因**：$176.33=x/d$ 恰是 $c_\Lambda=1$ 的比值（(19PL.4) 取 $c_\Lambda=1$），而 (19W.1) 用的是 $c_\Lambda=2$——**约定混用**，非算术粗心。

**更正口径**：

| 量 | 第 151 轮原记 | 按 $c_\Lambda=2$ 更正 | 按 $c_\Lambda=1$ 保留 |
|:---|:---|:---|:---|
| 比值公式 | $x/d$ | $2x/d=\Lambda/\lambda_L$ | $x/d$ |
| $d=3$ nm，$529$ nm | $176.33$ | $352.67$ | $176.33$ |
| $d=5$ nm，$400$ nm | $80.0$ | $160.0$ | $80.0$ |
| $d=10$ nm，$300$ nm | $30.0$ | $60.0$ | $30.0$ |

**同步更正**：第 151 轮卡结论 1、§一、A3；决策记录第 151 轮；`README.md` 第 151 轮段；`00_当前有效口径表.md` R-160；`成果登记.md` R-160；脚本 `环19_w与刚度对应域.py` 的 A3 与图 (e)；图中标签由 $\Lambda/d$ 改为 $2x/d$。**数值脚本的'London 读法'分支原用 $C_\Upsilon$（$=\hbar^2/(4\mu_0e^2)$ 的 $2$ 倍），一并改为 $C_\Upsilon$。**

**性质标注**：本轮更正是**约定对齐**，不是物理结论变更；(19W.2) 的 $C_\Lambda$、§七的 $\mathcal{B}$ 数值、全部不等式与 Lean 定理不受影响。

## 五、应用域与反推 $\lambda_L$ 的条件

(19PL.3) 的"读 $\Upsilon$ 不需要局域极限"与"读 $\lambda_L$ 需要"必须分开：

| 操作 | 条件 | 出处 |
|:---|:---|:---|
| $L_{k\square}\to\Upsilon$ | 无（线性响应定义） | (19PL.3) |
| $L_{k\square}\to\lambda_L$ | 局域极限 $\xi\ll\lambda_L$；否则非局域修正 | L152e |
| $d$ 的独立测量 | 双线圈法需扣死层（约 $25\%$ 误差） | L152f |
| 二维极限适用 | $d\ll\lambda_L$，且片电感随厚度标度 | L152g |

**推论**：第 151 轮"$\mathcal{B}$ 分域"在无约定形式 (19PL.7) 下只需 $L_{k\square}(0)$ 与 $T_c$，**不需要 $\lambda_L$ 或 $d$ 的单值**。这把 D2／D3 判定从"需要两组可能相差两个量级的读数"降为"一条可直接测的曲线"。

## 六、BKT 线的无约定形式

由 (19PL.3) 与 BKT 跳变 $\Upsilon_R(T_c^-)=\frac{2}{\pi}k_BT_c$：

$$L_{k\square}(T_c^-)=\frac{\hbar^2}{4e^2}\cdot\frac{\pi}{2k_BT_c}=\frac{\pi\hbar^2}{8e^2k_BT_c}. \tag{19PL.12}$$

与 (19W.2) 的等价性：$L_{k\square}=\mu_0\Lambda/c_\Lambda$，代入 $c_\Lambda\Lambda=2\lambda_L^2/d$ 并整理即得 $\Lambda=C_\Lambda/T_c$（Lean `bkt_kinetic_line`）。数值：$T_c=10$ K 给 $1.233$ nH／方，$T_c=1$ K 给 $12.33$ nH／方——落在微波薄膜电感的常见量级。

**$\mathcal{B}$ 的无约定读法**：

$$\mathcal{B}=\frac{L_{k\square}(0)}{L_{k\square}^{\rm BKT}(T_c)}=\frac{8e^2k_B}{\pi\hbar^2}T_cL_{k\square}(0)\in[0,1]. \tag{19PL.13}$$

第 151 轮 §七的 $1.89\times10^{-4}$（$529$ nm 作 $\Lambda$）与 $0.0667$（作 $\lambda_L$、$d=3$ nm）即由 (19PL.13) 复算，数值不变。

## 七、数值核对

脚本 `04_计算验证/环19_PearlLondon口径统一.py`（六面板图＋JSON，全断言通过）：

| 断言 | 内容 | 实测 |
|:---|:---|:---|
| B1 | 约定因子：同一 $\Lambda$ 下 $\Upsilon(c_\Lambda{=}2)/\Upsilon(c_\Lambda{=}1)$ | $2.000000$ |
| B2 | 读法比 $c_\Lambda x/d$（两组约定） | $352.67/160.0/60.0$（$c_\Lambda{=}2$）；$176.33/80.0/30.0$（$c_\Lambda{=}1$） |
| B3 | $L_{k\square}$ 恒等式：$\hbar^2/(4e^2L)$ vs $\hbar^2d/(4\mu_0e^2\lambda^2)$ | 相对误差 $<10^{-12}$（三组样例） |
| B4 | BKT 线：$\Lambda=2L_{k\square}/\mu_0$ vs $C_\Lambda/T_c$ | $T_c=1/7/10$ K 相对误差 $<10^{-12}$ |
| B5 | 简并：$\Upsilon(s\lambda,s^2d)/\Upsilon(\lambda,d)$ | $s=0.5/2/10$ 相对误差 $<10^{-14}$ |
| B6 | $\mathcal{B}$ 无约定：$L_{k\square}(0)/L_{k\square}^{\rm BKT}$ vs $T_c\Lambda/C_\Lambda$ | $1.89\times10^{-4}$／$0.0667$，一致到 $10^{-12}$ |

**复现**：`python "10 探索/超导第一性研究/04_计算验证/环19_PearlLondon口径统一.py"`。断言式的含义是"解析式的数值核对"，**不是数据拟合**。

## 八、Lean 承载

`05_Lean验证/PearlLondon.lean`（`lake env lean` 退出码 $0$，无警告）：

| 定理 | 内容 |
|:---|:---|
| `pearl_convention_transfer` | $\Lambda=c\lambda^2/d\Rightarrow d/\lambda^2=c/\Lambda$（(19PL.1)(19PL.9)） |
| `readout_ratio` | $\dfrac{C c/x}{Cd/x^2}=\dfrac{cx}{d}$（(19PL.4)(19PL.11)） |
| `kinetic_inductance_identity` | $L=\mu_0\lambda^2/d\Rightarrow\dfrac{\hbar^2d}{4\mu_0e^2\lambda^2}=\dfrac{\hbar^2}{4e^2L}$（(19PL.3)） |
| `scale_degeneracy` | $s\ne0\Rightarrow d/\lambda^2=(s^2d)/(s\lambda)^2$（(19PL.5)） |
| `bkt_kinetic_line` | $C=\pi\hbar^2/(4\mu_0e^2k_B)\Rightarrow \mu_0(C/T)/2=\pi\hbar^2/(8e^2k_BT)$（(19PL.12)） |

## 九、状态、缺口与"不能推出"

**状态**：环 19 §六／§九 的"与实验 $\rho_s(T)$ 对照"项**仍不闭合**；`审-4`、`审-6` 状态栏**不变**；缺口编号仍 $37$ 个、闭合数 $0$。本轮只做**口径统一**，不产生新的物理已证结论。

**不能推出**：
1. 不能推出某材料的 $\lambda_L$ 或 $d$——简并 (19PL.5) 禁止由 $\Upsilon$ 同时定二者。
2. 不能把 $c_\Lambda$ 当自由参数拟合——它只是文献记账，二选一且必须声明。
3. 不能把 $L_{k\square}\to\lambda_L$ 的换算用于 $\xi\gtrsim\lambda_L$ 的非局域样品（L152e）。
4. 不能把 $d_{\rm BKT}$、死层扣除等实验口径当作链内结果——它们只定 (19PL.12) 的容差。
5. 不能把 (19PL.13) 的 $\mathcal{B}\ll1$ 读成 CQM 失败——它判定该材料属 D3（$T_c$ 由振幅定），$\mathcal{B}$ 分域只是适用域筛选。

**遗留（不编号）**：$\Phi$ 形状独立来源、三条残余 $E_c$／$\gamma$／$m$ 不变；本轮不处理。

## 十、文献（外部）

- **L152a** J. Pearl, *Current distribution in superconducting films carrying quantized fluxoids*, Appl. Phys. Lett. **5**, 65 (1964), DOI 10.1063/1.1754056. Pearl 长度原始定义（$\Lambda=2\lambda_L^2/d$）。
- **L152b** *Realistic Pearl vortices in thin film superconductors*, arXiv:2604.09440v1. 明确采用 $\Lambda=2\lambda^2/d$，并说明薄膜中磁屏蔽尺度由 $\Lambda$ 而非 $\lambda$ 决定。
- **L152c** *Response of thin-film SQUIDs to applied fields and vortex fields: Linear SQUIDs*, arXiv:cond-mat/0507524v2. 采用 $\Lambda=\lambda^2/d$（不含 $2$）；是本轮"约定因子 $c_\Lambda\in\{1,2\}$"的直接证据。
- **L152d** *Sharpness of the Berezinskii–Kosterlitz–Thouless transition in ultrathin NbN films*, arXiv:2303.10639v1. 给出 $J_s=\dfrac{\hbar^2d}{4e^2k_B\mu_0\lambda^2}=\dfrac{\hbar^2}{4e^2k_BL_\square}$，与 (19PL.3) 同构。
- **L152e** *Measuring kinetic inductance and superfluid stiffness of two-dimensional superconductors using high-quality transmission-line resonators*, arXiv:2407.09916. 给出 $1/\lambda_L^2=(4\mu_0e^2/\hbar^2)\mathscr{D}_s$，并指出该局域关系在 $\xi>\lambda_L$ 的非局域区失效。
- **L152f** R. Zhang, Z. Zhao, M. Qin, J. Xu, W. Cheng, Y. Li, Q. Chen, J. Yuan, K. Jin, *Determining the thickness of the dead layer in superconducting film using a two-coil mutual-inductance technique*, Phys. Rev. Applied **17**, 054034 (2022), DOI 10.1103/PhysRevApplied.17.054034. 双线圈法测 $\lambda$ 须扣死层，未扣可致约 $25\%$ 误差；支撑"$d$ 需独立测量"。
- **L152g** *Kinetic inductance of few-layer NbSe$_2$ in the two-dimensional limit*, arXiv:2511.08466v2. 微波测得片动能电感 $L_{k,\rm sq}$ 随厚度标度，二维极限下 $L_{k,\rm sq}$ 为直接读出量。
