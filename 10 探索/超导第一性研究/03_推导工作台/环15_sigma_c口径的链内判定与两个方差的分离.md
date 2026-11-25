# 环 15/17：$\sigma_c$ 口径的链内判定与两个方差的分离

**状态**：A 类条件严格（口径判定与反解为链内结构），对象分离为否证（修正 R-152／R-153 的隐式混用）；$\sigma_c$ 的 $Z$、$n_{\rm cell}$、$t$ 仍外生，`审-4`／`审-6` 未闭合。
**边界**：本文只处理环 15 尾式中 $\sigma_c$ 的标度口径与环 17 反馈链里的方差对象归属，不处理渗流阈值的第一性推导、不给出 $w(T)$ 的绝对温标、不动 (15.1)／(15D.3)／(17.1) 原文。

---

## 一、问题：第 144 轮留下的口径分叉

R-153 登记：$\sigma_c$ 取绝对阈值时热膨胀使 $x=\nu\sigma_c^2/s^2$ 下降、$p$ 上升，与「升温破坏配对」方向紧张；取相对阈值 $\sigma_c\propto\bar\ell$ 时 $p$ 不变；链内未定口径。这个"未定"可以再推进一步——环 15 的结构本身已把口径选定，而且 R-152 把环 15 尾式套到环 17 的 $p_s$ 上是一次对象错配。两项都要判。

环 15 原文（(`环15_配对概率分布.md` §三)）：

$$
p_{\rm pair}(T)=1-F_{\chi^2_{n_{\rm cell}}}\!\left(\frac{n_{\rm cell}\sigma_c^2}{Z\,w(T)}\right),
\qquad
w(T)=\frac{2}{\omega_D^2}\int_0^{\omega_D}\omega\tanh\!\left(\frac{\omega}{2T}\right)d\omega .
\tag{15D.3}
$$

记 $V(T)=Zw(T)$、$x(T)=n_{\rm cell}\sigma_c^2/V(T)$。原文已钉死 $w'(T)<0$、$T\uparrow\Rightarrow x\uparrow\Rightarrow p\downarrow$。

---

## 二、$\sigma_c$ 口径：相对口径被相变存在性排除

设两种标度口径：

- **绝对口径**（A）：$\sigma_c=\sigma_0=\text{材料常数}$，与 $T$ 无关；
- **相对口径**（B）：$\sigma_c^2(T)=\rho\,V(T)$，$\rho>0$ 为常数（阈值随相干二阶矩同比缩放）。

**(R154.1) 相对口径消灭相变（否证 B）。** B 代入 $x$：

$$
x(T)=\frac{n_{\rm cell}\rho V(T)}{V(T)}=n_{\rm cell}\rho\equiv x_\rho,
\qquad
\frac{d x}{dT}=0
\quad\Longrightarrow\quad
\frac{d p_{\rm pair}}{dT}=0 .
\tag{R154.1}
$$

于是 (15D.3) 的读数不随温度变：渗流交点方程 $p_{\rm pair}(T_*)=p_c^{1/t}$ 要么无解（$1-F_\nu(x_\rho)\ne p_c^{1/t}$）、要么对整条 $T$ 轴恒成立（相等时），**都不存在唯一的 $T_*$**。环 15 §四的全部交点计算、R-149／R-150 的斜率分析、环 19 的 $p$ 通道都依赖 $x(T)$ 非常数。故链内若保留相变，只能取 A。这不是新增公设，是相变存在性对口径的必要条件。

**(R154.2) 反解（A 口径下 $\sigma_c$ 不再是自由现象学参数）。** 令 $p_*=p_c^{1/t}$，$F_\nu$ 严格增、$\bar F_\nu(x)=1-F_\nu(x)$ 严格减，故反解唯一：

$$
x_\ast=\bar F_\nu^{-1}(p_\ast)=F_\nu^{-1}(1-p_\ast),
\qquad
\sigma_c^2=\frac{x_\ast}{n_{\rm cell}}\,Z .
\tag{R154.2}
$$

$\sigma_c^2/Z$ 由 $(\nu,n_{\rm cell},t,p_c)$ 定；剩余外生的是 $Z$（零点方差标度）、$n_{\rm cell}$（自由度）、$t$（粗粒化指数）。这把环 15 状态栏"$\sigma_c$ 外部／现象学参数"收紧为"**阈值常数由渗流阈值反解，尺度因子 $Z$ 外生**"——$\sigma_c$ 的绝对数值仍不可第一性给出，但它的自由度从"独立参数"降为"$Z$ 的确定倍数"。

---

## 三、两个方差的对象分离：R-152 的 $p_s$ 是一次对象错配

链内出现两个都记作"方差"、但**不是同一随机变量**的量：

| 对象 | 定义 | 来源 | 随升温 | 进入的方程 |
|:---|:---|:---|:---|:---|
| $V_{\rm coh}=Zw(T)$ | 亏角/相干涨落的**系综第二矩**（确定量） | 环 10 Debye tanh 积分 | **减小**（$w'<0$） | 配对概率 $p_{\rm pair}$ (15D.3) |
| $s^2=\operatorname{Var}(\ell_e)$ | 边长的**样本方差**（顶点位移的函数） | FG 几何；仿射支 $\mu=\frac13\alpha_V\dot T$ | **增大**（$\alpha_V>0$） | 方差生产 $A=2\mu s^2$、矩跃变 $K=a\lambda(a)s^2$ |

统计学根据（外部工具，不搬作 CQM 结论）：样本方差与系综第二矩是不同随机变量，正态样本下 $(n-1)s^2/\sigma^2\sim\chi^2_{n-1}$，二者由尺度参数联系而非同一；环 15 §一的对象分层表本身已把 $V_{\rm coh}$（系综矩、确定量）与 $\hat V_\ell$（样本方差、随机变量）分开。

R-152 写 $p_s=\partial p/\partial s=\epsilon_\nu p/s$，把 $p$（依赖 $V_{\rm coh}$）对 $s$（边长标准差）求导。链内 $V_{\rm coh}$ 与 $s$ 之间**没有映射**：亏角对边长零次齐次（R-143 的 $L\ell=0$）、R-145 的 $\tilde AB=0$ 又使任意顶点位移不改变 $\varepsilon$，故 $\partial V_{\rm coh}/\partial s=0$。因此

$$
\frac{\partial p}{\partial s}=\frac{\partial p}{\partial V_{\rm coh}}\cdot\frac{\partial V_{\rm coh}}{\partial s}=0 .
\tag{R154.3}
$$

R-152 的 $p_s=\epsilon_\nu p/s$ 在链内恒零；它是把 $p$ 对 $V_{\rm coh}$ 的弹性误挂到 $s$ 上。**这是 `审-6` 的第三层错配**：第 142 轮是"读数当自变量"，第 143 轮是"尾部机制错配"，本轮是"统计对象错配"。

---

## 四、$\eta$ 失效面的修正：从"自洽反馈"降为"外生竞争"

R-152 的失效面 $\eta=\frac{2N-1}{2(N-1)}\epsilon_\nu\,a\lambda(a)$，在 $\nu=9$、$p_c$ 处因 $\epsilon_\nu=2.5929$ 给出 $a_\ast=0.3686$，判 $a=0.5$ 已在失效侧。按 (R154.3) 修正后要重算。

严格式：$N=pN_{\rm eff}$ 中 $p$ 由 (15D.3) 给、随 $V_{\rm coh}(T)$ 变，不随 $s$ 变。故

$$
g=\frac{\dot N}{N}=\frac{\dot p}{p}=\epsilon_\nu\frac{\dot V_{\rm coh}}{V_{\rm coh}}
=\epsilon_\nu\frac{\dot w}{w}
\quad\text{（外生，由 }\dot T\text{ 定）},
\tag{R154.4}
$$

不含 $s$ 的自洽回路。把它代回 R-151 的自洽代数 $g(2s-CK)=CA$、$K=a\lambda(a)s^2$、$A=2\mu s^2$，并除以 $s\ne0$：

$$
s=\frac{2g}{C\left(g\,a\lambda(a)+2\mu\right)} ,
\qquad
\text{可解}\iff g\,a\lambda(a)+2\mu>0 .
\tag{R154.5}
$$

**失效面性质改变**：

- 升温相：$\dot w<0\Rightarrow g<0$；配对支 $a>0\Rightarrow a\lambda>0$，故 $g\,a\lambda<0$，与 $2\mu>0$（Grüneisen 膨胀）**反向竞争**。失效条件 $|g|\,a\lambda>2\mu$，是"配对消失速度×尾部选择"与"膨胀速度"两个**外生率**的比较，不再是体系自身矩读数的正反馈。
- 降温相：$\dot w>0\Rightarrow g>0$、$a>0$，两项同号，无失效面。
- 骨干支 $a<0$：$a\lambda<0$，升温时 $g\,a\lambda>0$ 与 $2\mu$ 同号，降温时反向——左右尾的反馈符号**互换**（R-151 的尾部符号结论需按温度相重标）。

数值后果：$a=0.5$ 时 $a\lambda(a)=0.571$；若 $\epsilon_\nu=2.593$ 误乘则 $1.48>1$（R-152 判失效），但正确的 (R154.5) 只比较 $g$ 与 $\mu$ 两个率，无固定 $\eta>1$ 判据。R-152 的 $a_\ast=0.3686$ 不成立，撤销；R-151 的尾部符号改为依赖 $\operatorname{sgn}(\dot T)$ 与 $\operatorname{sgn}(a)$ 的乘积。

---

## 五、数值核查与图像（段 A–E）

脚本：`04_计算验证/环15_sigma_c口径与两个方差.py`，四面板无拟合函数图，摘要 CSV 同目录。

| 段 | 核查 | 判据 |
|:---|:---|:---|
| A | 相对口径 (R154.1)：$x_\rho$ 与 $p$ 对 $T$ 恒定 | 数值方差 $<10^{-14}$ |
| B | 绝对口径反解 (R154.2)：$\bar F_\nu(x_\ast)=p_c^{1/t}$ 二分闭合 | 残差 $<10^{-12}$ |
| C | $w(T)$ 严格减、$s^2$ 随 $\mu>0$ 严格增（方向相反） | $\max\Delta w<0$、$\min\Delta s^2>0$ |
| D | 对象错配 (R154.3)：$p$ 对 $V_{\rm coh}$ 有弹性、对 $s$ 恒零 | $\epsilon_\nu>0$、$\partial_s p=0$ 逐点 |
| E | (R154.5) 可解面：$g\,a\lambda+2\mu=0$ 与二次解一致、升降温/左右尾四象限 | 代数残差 $<10^{-10}$ |

---

## 六、Lean 形式化

`05_Lean验证/SigmaCThreshold.lean`（21 条定理，退出码 0、零警告）：相对口径下 $x$ 与 $p$ 恒定、严格单调 CDF 的反解唯一性恒等式、$\bar F_\nu$ 严格减、$a\lambda$ 的符号、可解面二次解的代数恒等式与四象限符号判定。无 `axiom`／`sorry`／`admit`／`native_decide`／`unsafe`。

**数值补充**（段 E）：失效阈 $a_\ast\lambda(a_\ast)=r\equiv2\mu/|g|$ 随材料率比移动——$r=0.05,0.15,0.40,1.0,2.0$ 分别给 $a_\ast=0.060,0.166,0.379,0.752,1.191$。R-152 的 $a_\ast=0.3686$ 是"$\epsilon_\nu a\lambda=1$ 的普适常数"，本轮判据里阈值是**外生率比 $r$**，不再是普适数。当前示意 $\mu=0.01$ 给 $r=0.0054$、$a_\ast\approx0.0054$，仅示数量级，不对应任何材料。

---

## 七、边界与登记

- **判否**：相对口径（R154.1）、R-152 的 $p_s=\epsilon_\nu p/s$（R154.3）、R-152 的 $a_\ast=0.3686$ 与固定 $\eta>1$ 判据（R154.5）。
- **收紧**：$\sigma_c$ 从自由现象学参数降为 $\sigma_c^2=x_\ast Z/n_{\rm cell}$（R154.2），但 $Z$、$n_{\rm cell}$、$t$ 外生。
- **不改**：(15.1)／(15D.3)／(17.1) 原文不动；06 不动；`审-4`、`审-6`、`临-24`、`临-25` 不闭合；唯一编号仍 37、闭合数仍 0。
- **下一步**：(R154.5) 里的 $g=\epsilon_\nu\dot w/w$ 与 $\mu=\bar\gamma C_V\dot T/(3K_TV)$ 都是外生率，下一轮应查二者能否由同一个温度扫描 $\dot T$ 约掉材料常数，给出可测的失效判据；在此之前 $t$ 仍不闭合。
