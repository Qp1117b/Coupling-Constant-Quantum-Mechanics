# 环 19／目标区：Uemura 闭合与 $g_{\rm ren}$ 的热力学反演（第 155 轮，R-164）

**性质**：对第 154 轮的**回改**（裸交点 → 真实 BKT 跳变）＋ 拉通推导链（环 10／15／19／目标区）＋ A 类条件严格反演。
**不闭合任何编号，不改状态栏，不动 06 原文；社会范畴不进式。**

---

## 一、前件与十问

1. **动哪一环**：环 19（BKT 跳变与 $\Phi$ 定标）＋目标区（Uemura 恒等式 (U.1)–(U.7)）；不新增环号。
2. **缺口还是状态**：补缺口（目标区 `临-25` 的 $g_{\rm ren}$ 读出、`M8`／`审-4` 定标口径），状态不动。
3. **编号**：`临-25`（$g_{\rm ren}$ 动态来源未定）、`M8`／`审-4`（$\sigma_c$ 定标）；不升格。
4. **前件成立**：$w(T)$（环 10）、$p_{\rm pair}$（环 15）、$\Phi$ 与 (19P.24)（环 19）、(U.1)–(U.7)（目标区）均登记；不含相变后对象作前件。
5. **物理量**：$\Upsilon,\Phi,g_{\rm ren},\kappa$ 全是物理量；无【诠释】。
6. **场／积分**：不涉及 $v_\tau$ 改造。
7. **$c_{ij}=0$**：未触碰。
8. **等效原理**：只用相界判据层，未用读数等效 (13.5) 与配对等效原理。
9. **外参**：$T$ 仍经 (4.1) 唯一入口；$\kappa$ 是无量纲组合；$c_2$ 是读数。
10. **相变／判据**：只处理判据层的 BKT 跳变与读数反演，不宣称相变机制。

---

## 二、回改：第 154 轮用了裸交点

第 154 轮以 (19P.21) 的**裸** BKT 方程定标。但目标区 (U.4)–(U.7) 与 L47 明确：普适跳变作用在**重整化**刚度上，

$$\Upsilon_R(T_c^-)=g_{\rm ren}\,\Upsilon_0\,w_c\,\Phi_c=\frac{2}{\pi}k_BT_c,\qquad 0<g_{\rm ren}\le1.\tag{155.1}$$

(19P.21) 的裸式 $g_{\rm ren}=1$ 只是上界近似。定义

$$\kappa\equiv\frac{2k_BT_c}{\pi\Upsilon_0w_c}\quad\Longrightarrow\quad
\boxed{\Phi_c=\frac{\kappa}{g_{\rm ren}}.}\tag{155.2}$$

**可行性收紧**：$\Phi_c\le1$ ⇒ $\kappa\le g_{\rm ren}\le1$（旧轮只要求 $\kappa\le1$）。第 154 轮数值表只在 $g_{\rm ren}=1$ 极限有效；本轮把它推广。相界自变量相应改为

$$p_*=p_c+(1-p_c)\Bigl(\frac{\kappa}{g_{\rm ren}}\Bigr)^{1/t_\Upsilon}
=p_c+(1-p_c)\,\Phi_c^{\,1/t_\Upsilon},\qquad
x_c=\bar F_\nu^{-1}(p_*),\quad \sigma_c^2=\frac{x_cZw_c}{\nu}.\tag{155.3}$$

由 $\Phi(p)$ 的定义，$\Phi(p_c+(1-p_c)\Phi(p_*)^{1/t_\Upsilon})=\Phi(p_*)$，故 (155.3) 自洽（一致恒等式，Lean `phi_roundtrip`）。

---

## 三、拉通：Uemura 恒等式对 $g_{\rm ren}$ 无约束

记 $U(0)\equiv\Upsilon_{\rm bare}(0)=\Upsilon_0\Phi_0$、$\Phi_0=\Phi\bigl(1-F_\nu(x_cw_c)\bigr)$。由 (U.7)

$$r(T_c)=w_c\frac{\Phi_c}{\Phi_0}=w_c\frac{\kappa}{g_{\rm ren}\Phi_0}.\tag{155.4}$$

代入 (U.1)：

$$T_c=\frac{\pi}{2k_B}\,U(0)\,r(T_c)\,g_{\rm ren}
=\frac{\pi}{2k_B}\,\Upsilon_0\Phi_0\cdot\frac{w_c\kappa}{g_{\rm ren}\Phi_0}\cdot g_{\rm ren}
=\frac{\pi}{2k_B}\,\Upsilon_0w_c\kappa\equiv T_c.\tag{155.5}$$

**结论**：$g_{\rm ren}$ 在 (U.1) 中精确抵消；单测 $(T_c,U(0))$ **不能**定 $g_{\rm ren}$（这与目标区把 $g_{\rm ren}$ 当独立读出因子一致）。要定它必须再引入一个独立观测量——低温刚度曲率。这正是本轮要接的一环。

---

## 四、闭合反演：由低温曲率定 $g_{\rm ren}$

第 154 轮给（$a=\pi^2/3$，$\tau=T/\omega_D$）

$$\frac{\Upsilon_{\rm bare}(T)}{U(0)}=1-c_2\tau^2+O(\tau^4),\qquad
c_2=a\,(1+B),\qquad B=\frac{t_\Upsilon\,h_0 f_\nu(h_0)}{p_0-p_c},\tag{155.6}$$

其中 $h_0=x_cw_c$、$p_0=1-F_\nu(h_0)$。$B$ 只依赖 $x_c$（给定 $w_c,\nu,t_\Upsilon,p_c$），且在 $h_0<\nu-2$（卡方模态以下）时严格单调增：分子 $h_0f_\nu(h_0)$ 增、分母 $p_0-p_c$ 减。故 $B(x_c)$ 可逆。

**闭合反演链**（观测量 → 链内量，无拟合自由度）：

| 步 | 输入 | 输出 | 式 |
|:---|:---|:---|:---|
| 1 | $T_c/\omega_D$ | $w_c=w(T_c)$ | 环 10 Debye 积分 |
| 2 | 实测曲率 $c_2$ | $B=c_2/a-1$ | (155.6) |
| 3 | $B$,$\nu$,$w_c$,$t_\Upsilon$,$p_c$ | $x_c=B^{-1}(\cdot)$ | (155.6) 单调可逆 |
| 4 | $x_c,w_c$ | $\Phi_0=\Phi(1-F_\nu(x_cw_c))$、$\Upsilon_0=U(0)/\Phi_0$ | (U.7) |
| 5 | $T_c$,$U(0)$,$w_c$,$\Phi_0$ | $\kappa=2k_BT_c\Phi_0/(\pi U(0)w_c)$ | (155.2) 代 $\Upsilon_0=U(0)/\Phi_0$ |
| 6 | $x_c,\kappa$ | $\Phi_c=\Phi(1-F_\nu(x_c))$、$g_{\rm ren}=\kappa/\Phi_c$ | (155.2) |

外部输入只剩 $(\nu,t_\Upsilon,p_c)$（$\nu$ 统计自由度、$t_\Upsilon$ 外部普适指数、$p_c$ 座阈值）——都是已登记的外部普适数或口径，不是新拟合参数。

**可行性（可观测量不等式）**：$\kappa\le g_{\rm ren}\le1$ ⇒

$$U(0)\ \ge\ \frac{2k_BT_c\,\Phi_0}{\pi\,w_c},\qquad g_{\rm ren}\le1.\tag{155.7}$$

**交叉检验（两条独立通路）**：目标区 Uemura 卡由 RG 分离点 $K_c$ 给 $g_{\rm ren}^{\rm RG}=(2/\pi)/K_c$（依赖涡旋逸度形状参数 $c$）；本轮给 $g_{\rm ren}^{\rm thermo}$（依赖低温曲率）。两者若不相等，则因子化 (19P.20)、(U.7) 或 $g_{\rm ren}$ 的 RG 读法中至少一个有问题——这是**内部可证伪的一致性判据**，不是拟合优度。

---

## 五、量纲、极限、体积层

- $\kappa,g_{\rm ren},\Phi,B,c_2$ 无量纲；$U(0),\Upsilon_0$ 单位 J；$c_2$ 是 $(T/\omega_D)^2$ 的系数。
- $g_{\rm ren}\to1$ 极限：回到第 154 轮裸式，$\Phi_c=\kappa$、$x_c$ 取旧值；$g_{\rm ren}<1$ 时 $\Phi_c>\kappa$、$p_*$ 上移、$x_c$ 下移、$\sigma_c^2$ 更小。
- 体积三层：结构层 $p_c$ 无限体积；容量层 $\nu=n_{\rm cell}$；读数层 $c_2$ 由有限 $T$ 曲线提取、须扣有限尺寸展宽；本轮只写判据层。

## 六、外部对照（B 类）

- L46（Kreidel et al. PRR **6**, 043245 / arXiv:2407.09916）：$L_{k\square}$→$\Upsilon$ 的实验读出、精度 $10^{-6}$；只确认 $c_2$ 与 $U(0)$ 可测。
- L47（BKT 流方程；Benfatto 讲义；Nelson cond-mat/9502114）：$g_{\rm ren}$ 的 RG 来源与普适跳变；只作标准工具。
- L43/L44（前轮）：低温幂律与 $t_\Upsilon$；不重复引用为 CQM 已证。

## 七、不能推出

1. 不能推出绝对 $T_c$、$\omega_D$、$\Upsilon_0$ 的先验值（仍需 $U(0)$ 与曲率实测）；
2. 不能推出 $g_{\rm ren}$ 的动态方程（`临-25` 仍开放），本轮只给**读出反演**；
3. 不能推出 $\rho_s\leftrightarrow\Upsilon$ 的 CQM 证明（`链外-B`）；
4. 不能推出外部 Uemura/Homes 实验律；
5. 不闭合任何编号：`临-25`／`M8`／`审-4` 状态栏不动，唯一编号仍 37、闭合数仍 0。

## 八、验证与状态

- **Lean**：`05_Lean验证/UemuraCurvatureInversion.lean`（含 (155.5) 抵消恒等式、`phi_roundtrip`、`kappa_from_U0`、`g_from_curvature` 的代数骨架）。
- **数值**：`04_计算验证/环19_Uemura曲率反演.py`（7 段断言＋图像，无拟合）。
- **同步**：口径表、研究纲领、README、主链环 19／目标区注记、成果登记 R-164。
