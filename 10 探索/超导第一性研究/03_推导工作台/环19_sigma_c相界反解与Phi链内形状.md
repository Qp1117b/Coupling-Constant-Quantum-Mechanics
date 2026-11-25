# 环 19：$\sigma_c$ 的相界反解与 $\Phi(T)$ 的链内形状（第 154 轮，R-163）

**性质**：口径回改（A 类代数）＋形状推导（A 类条件严格）＋外部对照（B 类）。不闭合任何编号、不改状态栏、不动 06 原文。
**前件环**：环 10（$w(T)$）、环 15（$p_{\rm pair}$）、环 19（$\Phi$ 与相界 (19P.25)）。**动的是缺口**（`M8`／`审-4` 的 $\sigma_c$ 口径与 $\Phi$ 自变量），不是状态。

---

## 一、前件（均为已登记链内结论，逐条可溯）

1. **$T$ 唯一入口**：$w(T)=V_{\rm coh}/Z=\frac{2}{\omega_D^2}\int_0^{\omega_D}\omega\tanh(\omega/2k_BT)\,d\omega$，$w(0)=1$，低温 $1-w=\frac{\pi^2}{3}(T/\omega_D)^2+O(T^4)$；来源环 10 `(10B.1)(10B.5)`，工作台 `环10_温度桥与刚度.md`。
2. **配对尾**：$p_{\rm pair}(T)=1-F_\nu\!\left(x(T)\right)$，$x(T)=\dfrac{\nu\sigma_c^2}{Z\,w(T)}$，$\nu\equiv n_{\rm cell}$；来源环 15 `(15D.1)`，工作台 `环15_配对概率分布.md`。条件于 G1–G3（$F_\nu$ 取 $\chi^2_\nu$ CDF、密度 $f_\nu>0$）。
3. **渗流刚度因子**：$\Phi(p)=0\ (p\le p_c)$，$\Phi(p)=\left(\dfrac{p-p_c}{1-p_c}\right)^{t_\Upsilon}\ (p>p_c)$，$\Phi(1)=1$；来源 `(19P.19')`，$p_c=p_c^{\rm site}=0.592746$（座阈值，`环15_座键口径.md`）；$t_\Upsilon\approx1.3$ 为外部普适指数（L44）。
4. **因子化与相界**：$\Upsilon_{\rm eff}(T)=\Upsilon_{\rm bond}\,w(T)\,\Phi(p_{\rm pair}(T))$，BKT 判据 $\Upsilon_{\rm eff}(T_c)=\frac{2}{\pi}k_BT_c$；来源 `(19P.20)(19P.21)`。**`M8` 等价性已撤销**，正确相界是 (19P.25) $p_{\rm pair}(T_c)=p_*(T_c)>p_c$，且 (19P.24) $p_*(T_c)=p_c+(1-p_c)\kappa^{1/t_\Upsilon}$，其中
   $$\boxed{\kappa\equiv\frac{2k_BT_c}{\pi\Upsilon_{\rm bond}w_c}\in(0,1],\qquad w_c\equiv w(T_c).}\tag{154.0}$$
   $\kappa\le1$ 是 $p_*\le1$ 的可行性条件。
5. **现行 $\sigma_c$ 口径（R-154／R-147）**：$x_\ast=\bar F_\nu^{-1}(p_c^{1/t})$、$\sigma_c^2=x_\ast Zw_c/\nu$；$\nu=9$ 给 $x_\ast=7.427075$、$\sigma_c^2/Z=0.825231$（乘 $w_c$ 后 $0.626106$）。

---

## 二、断口定位：$\sigma_c$ 定标挂在已被降级的条件上

R-154 用 $p_{\rm pair}(T_c)=p_c^{1/t}$ 反解 $\sigma_c$。但主链已明确判定该条件只是 `M8` 的**必要**形式，正确相界是 (19P.25) 的 $p_{\rm pair}(T_c)=p_*(T_c)>p_c$。两者不相容：

1. **口径数值隐含 $t=1$**：把 $x_\ast=7.427075$、$\nu=9$、$p_c=0.592746$ 代入，得 $1-F_9(x_\ast)=0.592746=p_c$，故 $p_c^{1/t}=p_c\Rightarrow t=1$。即现行数值口径以 $t=1$ 为该条件的实现。
2. **由此 $\Phi(T_c)=0$**：$t=1$ 给 $p_{\rm pair}(T_c)=p_c$，故 $\Phi(p_{\rm pair}(T_c))=\Phi(p_c)=0$，于是 $\Upsilon_{\rm eff}(T_c)=\Upsilon_{\rm bond}w_c\cdot0=0$。
3. **与 BKT 下界矛盾**：(19P.21) 要求 $\Upsilon_{\rm eff}(T_c)=\frac{2}{\pi}k_BT_c>0$（$T_c>0$）。$0=\frac{2}{\pi}k_BT_c$ 不可能。
4. **一般 $t$ 也不成立**：即使 $t>1$ 给 $p_c^{1/t}>p_c$，也不等于 $p_*(T_c)=p_c+(1-p_c)\kappa^{1/t_\Upsilon}$（后者还依赖 $\Upsilon_{\rm bond},T_c,w_c$）；把前者当定标条件即把已撤销的 `M8` 等价性偷运回来。

**结论**：$\sigma_c$ 的现行定标锚在已被降级的必要条件下，必须按 (19P.25) 重新反解。这是"发现不对劲→回改方程"的一步，不是新假设。

---

## 三、修正：$\sigma_c$ 由相界方程反解

把 (19P.24) 代入 $\Phi$ 并注意 $\Phi$ 的定义域包含 $p_*>p_c$：

$$\Phi\bigl(p_*(T_c)\bigr)=\left(\frac{p_*(T_c)-p_c}{1-p_c}\right)^{t_\Upsilon}
=\left(\kappa^{1/t_\Upsilon}\right)^{t_\Upsilon}=\kappa.\tag{154.1}$$

（$\kappa>0$，故 $(\kappa^{1/t_\Upsilon})^{t_\Upsilon}=\kappa$；Lean `phi_boundary`。）

于是相界判据 $\Phi(p_{\rm pair}(T_c))=\Phi(p_*(T_c))$ 给

$$\boxed{\Phi\bigl(p_{\rm pair}(T_c)\bigr)=\kappa=\frac{2k_BT_c}{\pi\Upsilon_{\rm bond}w_c},}\tag{154.2}$$

从而 $\Upsilon_{\rm eff}(T_c)=\Upsilon_{\rm bond}w_c\kappa=\frac{2}{\pi}k_BT_c$，**BKT 下界自动满足**——修正后的定标与相变判据自洽，不再需要额外否定。

反解 $\chi^2$ 尾：

$$\boxed{p_*(T_c)=p_c+(1-p_c)\kappa^{1/t_\Upsilon},\qquad
x_c=\bar F_\nu^{-1}\bigl(p_*(T_c)\bigr),\qquad
\sigma_c^2=\frac{x_c\,Z\,w_c}{\nu}.}\tag{154.3}$$

因 $p_*(T_c)>p_c=p_c^{1/t}|_{t=1}$ 且 $\bar F_\nu^{-1}$ 递减，故 $x_c<x_\ast$、$\sigma_c^2$ 小于 R-154 值。数值（$\nu=9$、$p_c=0.592746$、$t_\Upsilon=1.3$、$T_c/\omega_D=0.3$ 给 $w_c=0.758705$）：

| $\kappa$ | $p_*(T_c)$ | $x_c$ | $\sigma_c^2/Z$ | $\Phi_c=\kappa$ | $\Phi_0$ | $B$ | $\frac{\pi^2}{3}(1+B)$ |
|:---|:---|:---|:---|:---|:---|:---|:---|
| 0.10 | 0.662030 | 6.760582 | 0.569921 | 0.1000 | 0.476199 | 2.588806 | 11.8067 |
| 0.30 | 0.754052 | 5.857896 | 0.493824 | 0.3000 | 0.634665 | 1.533770 | 8.3358 |
| 0.50 | 0.831694 | 5.029898 | 0.424023 | 0.5000 | 0.761775 | 0.919107 | 6.3136 |
| 0.80 | 0.935766 | 3.599111 | 0.303407 | 0.8000 | 0.917886 | 0.303860 | 4.2895 |
| 0.95 | 0.984244 | 2.367205 | 0.199557 | 0.9500 | 0.981837 | 0.069873 | 3.5197 |

（$B$ 定义见 (154.8)。旧口径 $\sigma_c^2/Z=0.825231$／$0.626106$ 落在表外，且给 $\Phi_c=0$。）

---

## 四、$\Phi(T)$ 的链内形状与 $w\Phi$ 可分离判据

由 (154.3)，把 $T$ 的全部依赖集中到 $w$：

$$x(T)=\frac{\nu\sigma_c^2}{Zw(T)}=\frac{x_c\,w_c}{w(T)}.\tag{154.4}$$

记 $y\equiv w(T)\in[w_c,1]$、$h(y)\equiv x_c w_c/y$，则 $p(y)=1-F_\nu(h(y))$。因 $h$ 在 $y>0$ 严格反单调、$F_\nu$ 严格增，故

$$\frac{dp}{dy}=f_\nu(h)\,\frac{h}{y}>0.\tag{154.5}$$

（Lean `p_of_w_strictMono`。）**关键识别**：$\Phi$ 对 $T$ 的依赖**只经 $w(T)$**，没有独立的温度通道。于是

$$\boxed{\frac{\Upsilon(T)}{\Upsilon(0)}=y\cdot\frac{\Phi\bigl(p(y)\bigr)}{\Phi\bigl(p(1)\bigr)}\equiv G(y),\qquad y=w(T).}\tag{154.6}$$

$G$ 是单变量函数；给定 $\omega_D$（它定 $w(T)$）与 $(\kappa,\nu,t_\Upsilon,p_c)$，整条 $\Upsilon(T)/\Upsilon(0)$ 曲线**不含自由拟合参数**（只有整体归一 $\Upsilon(0)$）。这把第 151–153 轮反复登记的"$w\Phi$ 乘积不可分"化为**可分离**：

$$\boxed{\frac{\Phi\bigl(p_{\rm pair}(T)\bigr)}{\Phi\bigl(p_{\rm pair}(0)\bigr)}=\frac{\Upsilon(T)/\Upsilon(0)}{w(T)}.}\tag{154.7}$$

两边都由 $\omega_D$ 与上述参数决定；若实测 $\Upsilon(T)/\Upsilon(0)$ 不能写成 $G(w(T))$ 的形状，则 (19P.20) 的因子化或"$p_{\rm pair}$ 仅经 $w$ 依赖 $T$"被证伪。这是可证伪条件，不是拟合许可。

---

## 五、低温系数：$w$ 通道与渗流通道的定量分离

由 $y=1-a\tau^2+O(\tau^4)$（$\tau=T/\omega_D$，$a=\pi^2/3$）与 (154.6)，在 $y=1$ 处

$$G'(1)=1+\underbrace{t_\Upsilon\,\frac{h_0 f_\nu(h_0)}{p_0-p_c}}_{\displaystyle B},\qquad
h_0=x_c w_c,\quad p_0=1-F_\nu(h_0).\tag{154.8}$$

（Lean `G_deriv_one` 以链式法则承载：导数 $=\frac{d}{dy}[y\Phi/\Phi_0]\big|_{1}$。）$f_\nu>0$、$p_0>p_c$、$t_\Upsilon>0$ ⇒ $B>0$（Lean `B_pos`）。于是

$$\boxed{\frac{\Upsilon(T)}{\Upsilon(0)}=1-a(1+B)\Bigl(\frac{T}{\omega_D}\Bigr)^2+O(T^4).}\tag{154.9}$$

**分离**：系数 $a=1+B$ 中的 $1$ 是纯 Debye 通道，$B$ 是渗流通道；二者首次在低温 $T^2$ 系数里被显式分开。极限行为：

- $\kappa\to1$（$p_*(T_c)\to1$，$\Phi_c\to1$，BKT／洁净极限）：$x_c\downarrow$、$p_0\uparrow$、$B\to0$，系数 $\to a=\pi^2/3$；
- $\kappa\to0$（$p_*(T_c)\downarrow p_c$，趋近渗流阈值／SIT）：$p_0\downarrow p_c$、$B\to+\infty$，系数放大（同时 $\Phi_0\to0$，低温展开适用域收缩）。

**边界**：$B$ 的数值依赖分布族（R-141 已判相界斜率需峰度为显式输入）；$B>0$ 与其随 $\kappa$ 的单调方向只依赖 $f_\nu>0$，不依赖具体分布族。本轮**不改幂次**（仍是 $T^2$），不把放大后的有限窗口有效指数认作外部 $b\sim1.6$–$3$（L43）。

---

## 六、量纲、极限与体积层

- $x,\nu,\sigma_c^2/Z,\kappa,B$ 均无量纲；$w$ 无量纲；$\Upsilon$ 单位 J。
- 低温极限 $\tau\to0$ 如上；高温 $y\simeq\omega_D/(3T)$ 时 $G(y)$ 由 $w$ 主导，$\Phi$ 饱和到 $\Phi(p)$ 的高 $p$ 值；本轮只展开低温系数。
- 体积三层：结构层 $p_c$ 取无限体积值；容量层 $\nu=n_{\rm cell}$；读数层有限尺寸 $\Delta p\sim L^{-3/4}$ 不改本轮代数（$\kappa$ 是判据层量）。

## 七、外部对照（B 类，不进推导）

- L43（Khvalyuk–Feigel'man PRB **109**, 144501）：强无序中 $\delta\Theta\propto T^b$、$b\sim1.6$–$3$，机制为序参量宽分布；只作"放大系数随无序增大"的方向对照，**不声称 CQM 推出 $b$**。
- L44（Stauffer；Grassberger cond-mat/9808095；Bergman PRE）：$t_\Upsilon\approx1.3$ 是外部普适数、node–link 结构；CQM 只用它做代数。
- L45（Emery–Kivelson Nature **374**, 434；Lee-Hone PRB **96**, 024501）：$\rho_s^{\rm macro}=f\rho_s^{\rm micro}$、$f:1\to0$ 于阈值；与 (19P.20) 同形，不互证。

## 八、不能推出

1. 不能推出绝对 $T_c$、$\omega_D$、$\Upsilon_{\rm bond}$、$t_\Upsilon$、$\nu$ 的数值（仍外生，`审-10`／Z2）；
2. 不能推出外部实验指数 $b$，本轮只给 $T^2$ 系数的放大；
3. 不能推出 $B$ 的普适数值（依赖分布族，R-141）；
4. 不能推出 $\Phi$ 的幂律来源（外部普适数，L44）；
5. 不能推出任何缺口已闭合：`M8`、`审-4` 仍「未闭合」，编号仍 $37$，闭合数仍 $0$。

## 九、验证与状态

- **Lean**：`05_Lean验证/PercolationStiffnessShape.lean`，`lake env lean` 退出码 $0$、无警告、无 axiom／sorry／admit／native_decide／unsafe。
- **数值**：`04_计算验证/环19_sigma_c相界反解与Phi形状.py`，断言＋多面板图＋JSON，无拟合。
- **状态**：`M8`／`审-4` 缺口行加注记，**状态栏未变动**；主链环 15／环 19 注记同步；口径表 R-154 条加"定标条件已回改"注记，不删原条目。
