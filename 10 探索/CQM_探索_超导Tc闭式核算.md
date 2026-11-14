# CQM 探索：超导 $T_c$ 闭式与超导判据核算

> **定位**：本文属 `10 探索/`（非权威源），只记录推演、核对与开放问题。**不改** `06 超导/` 的任何定义、数值与缺口状态——G18、G22 仍为原状态，本文不宣称任何缺口闭合。所有数值为构造后验数字校验，待独立复现。

---

## 1. 本轮问题

`06 超导/` 中现存四个 $T_c$ 表达式。本轮只回答三个可判定的问题：

| 编号 | 问题 | 判定方式 |
|:---|:---|:---|
| Q1 | 四个表达式是否等价？ | 逐项对照函数形式、依赖变量与极限 |
| Q2 | 哪一个可由「本征值交叉 + 玻色统计」严格导出？ | 从给定 ansatz 重推，检查是否引入新假设 |
| Q3 | 判据中的临界角亏 $\Delta\delta_c$ 是否与 $\delta_v$ 无关？ | 由判据式反解，并与文中三个数值对照 |

问题本身不引入新物理；判定只用到 `06` 已写出的式子。

---

## 2. 外部依据

### 2.1 取到的出处

| 出处 | 外部文献结论 | 与 CQM 的关系（仅作对照） |
|:---|:---|:---|
| Bardeen, Cooper, Schrieffer, *Phys. Rev.* **108**, 1175 (1957)；Tinkham, *Introduction to Superconductivity*, 2nd ed., Ch. 3（教科书常数） | $k_BT_c\simeq1.13\,\hbar\omega_D\exp[-1/N(0)V]$；弱耦合极限下 $T_c$ 与声子能量标度成**正比** | CQM 的 (T-a) 同为「$\theta_D\times$ 无量纲耦合函数」，结构同类；此处不把 BCS 结论当作 CQM 已证内容 |
| Maxwell, *Phys. Rev.* **78**, 477 (1950)；Reynolds, Serin, Wright, Nesbitt, *Phys. Rev.* **78**, 487 (1950) | Hg 同位素：$T_c\propto M^{-\alpha}$，$\alpha\simeq0.5$ | 用于检验第 8 节：CQM 公式隐含的声子通道指数 |
| Uemura et al., *Phys. Rev. Lett.* **62**, 2317 (1989) | 欠掺杂铜氧化物中 $T_c\propto n_s/m^*$，即 $T_c$ 与超流密度成**线性**关系（「Uemura 标度」） | 与幂律支「$T_c\propto\Delta\delta_0$」的线性族同类；CQM 未引入 $n_s$，仅作机制对照 |
| Emery, Kivelson, *Nature* **374**, 434 (1995) | 超流密度小时，相刚度和相位涨落而非声子能标决定 $T_c$ | 说明存在「非 $\theta_D$ 主导」的现实机制；CQM 若要保留幂律支，须说明其对应哪一类 |
| Regge, *Nuovo Cimento* **19**, 558 (1961)，doi:10.1007/BF02733251 | 离散曲率以顶点角亏 $\delta_v=2\pi-\sum_i\theta_i$ 表达 | 角亏定义的出处；CQM 的 $\delta_v$ 用法属自建构造 |

上表第二列为外部文献结论，第三列只是对照口径，不含任何 CQM 已证内容；CQM 自身的构造假设见 §3。

### 2.2 未取得

- `06` 引用的「$T_c$ 对 77 个超导体留一法交叉验证精度」无可复核产物；本轮**不**据此作任何判断，也不补造数字。
- $K_0=\mathrm{e}^{1/\beta}\alpha_{\text{fs}}^3\cdots\exp(A_G\gamma_n)$ 的前因子 $\mathrm{e}^{1/\beta}\alpha_{\text{fs}}^3\hbar^{-1/4}k_B^{1/8}m_e^{-1/4}a_0^{-1/2}$ 的量纲核对我未在本文完成（见 §9 未闭合项）。
- (T-b) 的 $(\ln2)^2$ 归一、(T-c)/(T-d) 的 $K_{\text{eff}}\propto G^{-0.77}\theta_D^{1.13}$ 均系 CQM 内部参数化，检索未见外部出处；本文只作内部自洽性判定，不为其寻找文献依据。

---

## 3. 现状清点：四个表达式

| 编号 | 出处 | 形式 | 阈值 | 显式含 $\delta_v$ |
|:---|:---|:---|:---|:---|
| (T-a) | §11.10（`CQM_超导核心理论.md`），并由 §11.11 判据承接 | $T_c=\dfrac{\theta_D}{2\,\mathrm{arccoth}(x)}$，$x=\dfrac{3\beta^2\Delta\delta_0^2}{16(1-\beta\delta_v)(\gamma_2-\gamma_1)}$ | 有（$x>1$） | 是 |
| (T-b) | §11.6 | $T_c=\dfrac{\hbar\Omega_0}{2k_B\,\mathrm{arccoth}\!\left[1+\dfrac{\dfrac{3\beta^2\Delta\delta_v^2}{16(1-\beta\delta_v)}-(\gamma_2-\gamma_1)}{(\ln2)^2}\right]}$ | 同上 | 是 |
| (T-c) | §11.14 自由能链 | $T_c^2=\dfrac{8\Delta\delta_0^2K_{\text{eff}}\theta_D}{9\ln2}$ | 无 | 否（原文称「不需要 $\delta_v$」） |
| (T-d) | §11.13 黎曼零点指数 | $T_c^2=\dfrac{8\Delta\delta_0^2Ce^{a\gamma_n}G^{-0.77}\theta_D^{2.13}}{9\ln2}$ | 无 | 否 |

(T-d) 在函数结构上是 (T-c) 的拟合填充（$K_{\text{eff}}\to Ce^{a\gamma_n}G^{-0.77}\theta_D^{1.13}$），故下文只对 (T-a)、(T-b)、(T-c) 作判定，(T-d) 随 (T-c)。

---

## 4. 判定一：(T-a) 在给定 ansatz 下是精确解

### 4.1 重推

取 §11.6/§11.10 已写出的两条：

$$
\lambda_n(T)=\gamma_n-\frac{\beta^2\Delta\delta_v(T)^2}{4(1-\beta\delta_v)}\cdot\frac{n^2-1}{n^2},\qquad
\Delta\delta_v(T)^2=\Delta\delta_0^2\tanh\frac{\theta_D}{2T}.
$$

并要求正常态无修正 $\lambda_1=\gamma_1$。令 $\lambda_2(T_c)=\lambda_1(T_c)$：

$$
\gamma_2-\gamma_1=\frac{3\beta^2\Delta\delta_v(T_c)^2}{16(1-\beta\delta_v)}.
$$

代入 $\Delta\delta_v(T_c)^2$ 并记

$$
A\equiv\frac{3\beta^2\Delta\delta_0^2}{16(1-\beta\delta_v)},\qquad x\equiv\frac{A}{\gamma_2-\gamma_1},
$$

得

$$
\tanh\frac{\theta_D}{2T_c}=\frac{1}{x}
\;\Longrightarrow\;
T_c=\frac{\theta_D}{2\,\mathrm{arccoth}(x)}=\frac{\theta_D}{\ln\dfrac{x+1}{x-1}}.
$$

这与 (T-a) 逐字相同。推导只用玻色恒等式 $\dfrac{1}{1+2n_B}=\tanh\dfrac{\theta_D}{2T}$（§11.1–§11.2 已给）与两式相减，**未引入新假设**。故 Q2 的答案是：只有 (T-a) 可导出；(T-b)、(T-c) 都不能。

### 4.2 等价形式：临界占据数

由 $2n_B(T_c)=x-1$ 立即得

$$
n_c\equiv n_B(T_c)=\frac{x-1}{2}.
$$

（与 §11.10 定位注一致。）这给出 (T-a) 的物理读法：**升温使角亏涨落幅度按 $\sqrt{\tanh}$ 衰减，把 $\lambda_2$ 从下方推到 $\lambda_1$；交叉条件是曲率涨落模的玻色占据数达到 $n_c$。** 该读法在阈值处良态（$n_c\to0$）。

### 4.3 存在唯一性

$f(T)\equiv A\tanh(\theta_D/2T)$ 在 $T\in(0,\infty)$ 上连续、严格递减，$f(0^+)=A$，$f(\infty)=0$。故 $f(T_c)=\gamma_2-\gamma_1$ 有唯一解当且仅当 $A>\gamma_2-\gamma_1$，即 $x>1$；$x\le1$ 时无解。这与 §11.10「应记为无解而非 $T_c=0$」一致，并可去掉该处的措辞余地：**无解是严格结论，不是约定**。

### 4.4 极限与数值

| $x$ | 1.001 | 1.01 | 1.1 | 1.35 | 2 | 3 | 5 | 10 | 25 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| $T_c/\theta_D$ | 0.1316 | 0.1886 | 0.3285 | 0.5251 | 0.9102 | 1.4427 | 2.4663 | 4.9833 | 12.4933 |
| $x/2$（强激活渐近） | 0.5005 | 0.5050 | 0.5500 | 0.6750 | 1.0000 | 1.5000 | 2.5000 | 5.0000 | 12.5000 |

两端渐近：

$$
x\to1^+:\quad T_c\simeq\frac{\theta_D}{\ln\dfrac{2}{x-1}}\quad(\text{对数趋零});\qquad
x\gg1:\quad T_c\simeq\frac{\theta_D\,x}{2}=\frac{3\beta^2\Delta\delta_0^2\,\theta_D}{32(1-\beta\delta_v)(\gamma_2-\gamma_1)}.
$$

弱端核对：$x=1.001$ 时精确值 $0.13155467$，渐近式 $0.13156332$（相对差 $7\times10^{-5}$）；$x=1.0001$ 时 $0.10097402$ 对 $0.10097453$。

### 4.5 两个结构性质（可作判据用）

- **P1（$\theta_D$ 线性）**：$T_c=\theta_D\cdot g(x)$，而 $x$ 不含 $\theta_D$，故 $\partial\ln T_c/\partial\ln\theta_D=1$ **精确成立**，与 $x$ 无关。
- **P2（硬阈值）**：$x\le1$ 时不存在 $T_c$。这是「Cu、Ag、Au 不超导」这类判据的唯一承载者。

P1、P2 是 (T-a) 的定性指纹，第 6、8 节据此排除其他支。

---

## 5. 判定二：(T-b) 不是其自身交叉方程的解

(T-b) 的交叉方程（把 §11.6 的 $\lambda_n(T)$ 两式相减）是隐式方程

$$
\coth\frac{\theta_D}{2T_c}-1=\frac{A\tanh\dfrac{\theta_D}{2T_c}-(\gamma_2-\gamma_1)}{(\ln2)^2},
$$

因为 $\Delta\delta_v(T)$ 本身含 $\tanh(\theta_D/2T_c)$。若在交叉方程中把 $\Delta\delta_v(T_c)^2$ 的 $\tanh$ 取为 $1$（即用 $\Delta\delta_0^2$ 代替），方程就化为 $x_b=1+\dfrac{A-(\gamma_2-\gamma_1)}{(\ln2)^2}$，这正是 (T-b) 写出的形式。两者不是同一个方程的解。

取同一材料点（以 $x_a=A/(\gamma_2-\gamma_1)$ 标记，$\theta_D$ 约去）：

| $x_a$ | (T-a) $T_c/\theta_D$ | (T-b) 写出式 | 比值 | (T-b) 隐式解 | 与 (T-a) 偏差 |
|:---|:---|:---|:---|:---|:---|
| 1.01 | 0.18856 | 0.36971 | 1.96 | 0.18618 | $-1.3\%$ |
| 1.35 | 0.52514 | 2.98073 | 5.68 | 0.50512 | $-3.8\%$ |
| 2 | 0.91024 | 7.65664 | 8.41 | 0.84560 | $-7.1\%$ |
| 5 | 2.46630 | 29.16723 | 11.83 | 2.01322 | $-18.4\%$ |
| 10 | 4.98329 | 65.00641 | 13.04 | 3.49455 | $-29.9\%$ |

（隐式解由数值求根给出：$x_a=2$ 时 $y^*=\theta_D/2T_c=0.59129765$，$T_c/\theta_D=0.84559782$。）

**结论**：§11.6 的注「本节闭式与 §11.10 … 是同一物理机制的两种参数化」不成立。真实关系是：**（T-b）的隐式方程与（T-a）只是近似同解（阈值附近差 $1.3\%$，强激活端差 $30\%$），而（T-b）写出的显式式根本不是解，偏差从 2 倍到 13 倍。** 因而「数值计算以 §11.10 为准」是必要规定，但理由应写成「(T-b) 显式式非其方程之解」，而不是「两种参数化」。

---

## 6. 判定三：幂律支与 (T-a) 不可并存

### 6.1 指数对照

| 量 | (T-a) 强激活端 | (T-c) | 是否相容 |
|:---|:---|:---|:---|
| $\Delta\delta_0$ | $T_c\propto\Delta\delta_0^{2}$ | $T_c\propto\Delta\delta_0^{1}$ | 否（差一次幂） |
| $\theta_D$ | $T_c\propto\theta_D^{1}$（P1，精确） | $T_c\propto\theta_D^{1/2}$ | 否 |
| $\delta_v$ | $T_c\propto(1-\beta\delta_v)^{-1}$ | 原文称「不需要 $\delta_v$」 | 否 |
| 阈值 | $x>1$ 硬阈值 | 无阈值，$\Delta\delta_0\to0$ 时 $T_c\to0$ | 否 |

### 6.2 二者等价所需的 $K_{\text{eff}}$

若要求 (T-c) 在某一点复现 (T-a)，必须

$$
K_{\text{eff}}=\frac{9\ln2}{32}\,\frac{\theta_D}{\Delta\delta_0^2\,\mathrm{arccoth}^2(x)}
\;\xrightarrow[x\gg1]{}\;
\frac{9\ln2}{32}\,\frac{\theta_D\,x^2}{\Delta\delta_0^2}
=\frac{9\ln2}{32}\,\theta_D\left(\frac{3\beta^2}{16(\gamma_2-\gamma_1)}\right)^2\frac{\Delta\delta_0^2}{(1-\beta\delta_v)^2}.
$$

（第一式为恒等；第二式为 $x\gg1$ 渐近，$x=6.4$ 处偏高 $1.6\%$，$x=2.3$ 处偏高 $13\%$。）

即所需 $K_{\text{eff}}\propto\theta_D\,\Delta\delta_0^2\,(1-\beta\delta_v)^{-2}$。三点后果：

1. $K_{\text{eff}}$ **显含** $\Delta\delta_0$ 与 $\delta_v$，与 §11.14「不需要 $\delta_v$」直接冲突；
2. 若同时保留 §11.14 的能量 ansatz $E_2-E_1=\Delta\delta_0^2K_{\text{eff}}$，则 $E_2-E_1\propto\Delta\delta_0^4(1-\beta\delta_v)^{-2}$，即凝聚能对涨落幅度是**四次**而非二次——与 Regge 作用量 $K_v\delta_v^2A_v$ 的二次结构不符；
3. 数值示例（$\theta_D=300$ K，$\delta_v=0.0104$）：$\Delta\delta_0=0.2$ 需 $K_{\text{eff}}=281.7$ K，$\Delta\delta_0=0.3$ 需 $2988.5$ K，$\Delta\delta_0=0.5$ 需 $9373.8$ K——后两者相差 $33$ 倍（$1.5$ 个量级），与「$K_{\text{eff}}$ 是只依赖晶格几何的刚度」这一读法不符。

### 6.3 结论

(T-c)/(T-d) 不能作为与 (T-a) 并列的独立闭式。可保留的地位只有两种，且须明写：

- **窗口再参数化**：在固定 $(\Delta\delta_0,\delta_v,\theta_D)$ 附近，把 (T-a) 的局部行为写成 $\theta_D$ 的幂律（此时指数应由 (T-a) 定出，而不是拟合得到）；
- **不同机制**：若坚持 (T-c) 是独立的物理机制（对照 Emery–Kivelson 的相刚度路线），则必须放弃硬阈值 P2，并撤回「非超导体 $\delta_v<1/\beta$」这条判据的承载者。

在未作此声明前，`06` 中「自由能第一性预测链条闭合」与「(T-a) 阈值判据」并存，属**同一量两套不相容的闭式**。

---

## 7. 判据核算：$\Delta\delta_c$ 依赖 $\delta_v$

### 7.1 精确式

由 $x>1$ 与一般 $n$（$\lambda_n$ 对 $\lambda_1$ 交叉）：

$$
\Delta\delta_c(n;\delta_v)=\sqrt{\frac{4n^2(1-\beta\delta_v)(\gamma_n-\gamma_1)}{\beta^2(n^2-1)}}.
$$

$n=2$ 即 §11.11 判据 $\beta\delta_v+\dfrac{3\beta^2}{16(\gamma_2-\gamma_1)}\Delta\delta_0^2>1$ 的边界；除以 $\beta$ 后在 $(\delta_v,\Delta\delta_0^2)$ 平面上是直线 $\delta_v+0.7114\,\Delta\delta_0^2>1/\beta$，斜率 $3\beta/[16(\gamma_2-\gamma_1)]=0.711437$，截距 $\delta_v^{\max}=1/\beta=0.0382662$。

### 7.2 数值（$\beta=8\pi+1=26.1327412$，$\gamma_{1,2,4,6}$ 取黎曼零点虚部）

| $\delta_v$ | $\Delta\delta_c(2)$ | $\Delta\delta_c(4)$ | $\Delta\delta_c(6)$ |
|:---|:---|:---|:---|
| 0 | 0.231921 | 0.319023 | 0.375878 |
| 0.005 | 0.216239 | 0.297451 | 0.350462 |
| 0.0104 | 0.197911 | 0.272241 | 0.320759 |
| 0.02 | 0.160234 | 0.220414 | 0.259695 |
| 0.03 | 0.107791 | 0.148275 | 0.174700 |

### 7.3 反解文中三个数值

`06` 给出 $\Delta\delta_c\approx0.20$、$0.27$、$0.32$（$n=2,4,6$）。把每个值代回上式反解 $1-\beta\delta_v$：

| $n$ | 文中值 | 反解 $1-\beta\delta_v$ | 反解 $\delta_v$ |
|:---|:---|:---|:---|
| 2 | 0.20 | 0.743672 | 0.009809 |
| 4 | 0.27 | 0.716281 | 0.010857 |
| 6 | 0.32 | 0.724779 | 0.010532 |

三个值互相自洽到约 $2\%$，共同指向

$$
\beta\delta_v\simeq0.27,\qquad \delta_v\simeq0.0104\ (0.0098\text{–}0.0109).
$$

**这是一项可复核的正向结果**：三个临界值不是三个独立数字，而是同一隐含参数 $\beta\delta_v\approx0.27$ 的三种表述；反过来，它们也验证了 (T-a) 与 $\lambda_n$ 谱隙的算术自洽。问题只在于：**这个 $\delta_v$ 在 `06` 中未被写出**，因此「$\Delta\delta_c\approx0.20$」作为可检验预言时缺一个参数。

### 7.4 建议措辞（不落地到 `06`）

- 现文：「临界角亏涨落 $\Delta\delta_c\approx0.20$（低于此不超导）」；
- 建议：「超导判据为 $\delta_v+0.7114\,\Delta\delta_0^2>1/\beta$；$\delta_v=0$ 时 $\Delta\delta_c(2)=0.2319$，$\delta_v\simeq0.0104$ 时 $\Delta\delta_c(2)\approx0.20$（构造后验数字校验，待独立复现）」。
- 同处「$T_c(4)/T_c(2)\approx0.13\text{–}0.27$」「$T_c(6)/T_c(2)\approx0.11\text{–}0.15$」也需要标注其对应的 $\delta_v$ 区间，否则无法复现。

---

## 8. 同位素指数：与 §11.9 的 $\alpha\approx0.0006$ 冲突

### 8.1 $\theta_D$ 通道是精确的 $1/2$

由 P1，$\partial\ln T_c/\partial\ln\theta_D=1$。同位素替换下 $\theta_D\propto M^{-1/2}$，故该通道贡献

$$
\alpha_\theta=\tfrac12\quad(\text{对一切 }x\text{ 精确}).
$$

### 8.2 $\Delta\delta_0$ 通道

§11.14 的 $\Delta\delta_0^2=\dfrac{C^2}{l^2}\dfrac{3\hbar}{4\omega_D}(1-f)\sum_{\text{edges}}\left(\dfrac{1}{m_i}+\dfrac{1}{m_j}\right)$ 显含 $1/m$，故 $\Delta\delta_0^2\propto M^{-1}$，附加

$$
\alpha_\Delta\equiv\frac{\partial\ln T_c}{\partial\ln\Delta\delta_0^2}=\frac{2xf}{x^2-1},\qquad f\equiv\frac{T_c}{\theta_D}=\frac{1}{2\,\mathrm{arccoth}(x)}.
$$

数值：

| $x$ | 1.01 | 1.1 | 1.35 | 2 | 3 | 5 | 10 | 25 | 100 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| $\alpha_\Delta$ | 18.95 | 3.441 | 1.724 | 1.214 | 1.082 | 1.028 | 1.007 | 1.001 | 1.000 |
| $\alpha_\theta+\alpha_\Delta$ | 19.45 | 3.941 | 2.224 | 1.714 | 1.582 | 1.528 | 1.507 | 1.501 | 1.500 |

### 8.3 三种口径

| 口径 | 对两个标量的假设 | $\alpha_{\text{total}}$ | 与 Hg 的 $\alpha\simeq0.5$ |
|:---|:---|:---|:---|
| R1 | $\theta_D\propto M^{-1/2}$，$\Delta\delta_0^2\propto M^{-1}$ | $1.5$ 至 $\infty$（随 $x$ 减小而增大） | 被排除 |
| R2 | 只有 $\theta_D\propto M^{-1/2}$，$\Delta\delta_0$ 视为化学固定 | $0.5$ | 相符 |
| R3 | 两者都对同位素不变 | $0$（只剩缺陷丰度通道） | 与元素超导体不符 |

`06` 现在的写法同时含有 R1 的两个输入（§11.9 的对照表写出 $\theta_D\propto M^{-1/2}$；§11.14 的 $\Delta\delta_0^2$ 含 $\sum 1/m$），却给出 §11.9/§18.4 的 $\alpha\approx0.0006$。这不是小数误差，是**三个量级**的差别，且落在「元素超导体」这一最干净的数据区。

### 8.4 最小修补（供选择，未落地）

- 若采用 R2：须在 §11.9 明写「$\Delta\delta_0$ 在同位素替换下不变（化学固定）」，并声明 §11.14 中 $\Delta\delta_0^2$ 的 $1/m$ 只用于绝对量级估计、不参与同位素替换；此时 $\alpha=0.5$，与 Hg/Pb 一致，但「非 BCS 质量效应」的论断退为「质量效应 + 缺陷丰度修正」。
- 若保留「非质量效应」论断（R3）：须明写 $\theta_D$ 与 $\Delta\delta_0$ 均为同位素不变量，并与 §11.9 对照表中 $\theta_D\propto M^{-1/2}$ 一行直接冲突，需删该行。
- 无论哪种，$\alpha\approx0.0006$ 只能作为**缺陷丰度通道** $\alpha_{\text{defect}}$ 的数值，总指数须写 $\alpha=\alpha_\theta+\alpha_\Delta+\alpha_{\text{defect}}$。

---

## 9. 未闭合项（本文不宣称闭合，G18/G22 状态不变）

1. **算子 ansatz 仍是猜测**。§4 的「严格」只相对于 $\lambda_n(T)$、$\lambda_1=\gamma_1$ 两条 ansatz；它们本身由六条物理条件唯象确定（§11.6 猜测状态说明已承认）。Q2 的结论应表述为：**给定 ansatz，(T-a) 是精确解；(T-b)(T-c) 不是。**
2. **$S_{U(1)//\mathbb{Z}_n}$ 仍缺**。本文未构造可计算作用量，因此「$F_1(T_c)=F_2(T_c)$ 是本征值交叉的热力学投影」仍未证明；§6 只证明它与 (T-a) 数值不相容。
3. **$K_{\text{eff}}$ 的独立性**。§11.13/§11.14 的 $K_{\text{eff}}=K_0G^{p}\theta_D^{q}$ 指数 $(-0.77,1.13)$ 是回归量；本文 §6.2 表明若要复现 (T-a)，它必须带 $\Delta\delta_0^2/(1-\beta\delta_v)^2$，二者不能同时成立。哪一个是拟合产物，需原始数据才能判，本轮无数据。
4. **同位素指数须重算**。§8 给出三种口径；选定口径后 $\alpha$ 是 $x$ 的函数，不再是一个常数，这本身是可检验结构（同一材料不同 $x$ 区间的 $\alpha$ 应不同）。
5. **$K_0$ 前因子的量纲**。$\mathrm{e}^{1/\beta}\alpha_{\text{fs}}^3\hbar^{-1/4}k_B^{1/8}m_e^{-1/4}a_0^{-1/2}$ 的量纲未核；本文未使用该式，故不影响 §4–§8。
6. **$\Delta\delta_c$ 的 $\delta_v$ 依赖是双刃**：判据线 $\delta_v+0.7114\,\Delta\delta_0^2>1/\beta$ 在 $\delta_v\to1/\beta$ 时让任意小涨落都满足，而该极限同时使 $v_\tau=\sqrt{1-\beta\delta_v}\to0$、框架退化。边界行为的物理解释未完成。

---

## 10. 状态

| 项 | 本轮结论 | 可复现性 |
|:---|:---|:---|
| (T-a) 的推导地位 | 在 ansatz 下精确；由玻色恒等式与两式相减得到，无新假设 | 可复算（本文 §4 给出全部代数步骤） |
| 解的存在唯一性 | $x>1$ 时唯一；$x\le1$ 严格无解 | 可复算 |
| (T-b) 的地位 | 写出的显式式**不是**其交叉方程的解（偏 2–13 倍）；隐式解与 (T-a) 差 $1.3\%$–$30\%$（阈值端到强激活端） | 数值可复算（本文表） |
| (T-c)/(T-d) 的地位 | 与 (T-a) 指数、阈值、$\delta_v$ 依赖三处不相容；不能作并列独立闭式 | 代数判定，可复算 |
| $\Delta\delta_c$ | 依赖 $\delta_v$；文中 0.20/0.27/0.32 对应 $\delta_v\simeq0.0104$ | 反解可复算（本文表） |
| 同位素指数 | $\theta_D$ 通道精确 $1/2$；R1 下总指数 $1.5$–$\infty$；与 $\alpha\approx0.0006$ 差三个量级 | 可复算（本文表） |

**一句话**：`06` 的 $T_c$ 不是「一个公式、三种写法」，而是「一个精确解（(T-a)）+ 一个误写的显式（(T-b)）+ 一条不相容的幂律链（(T-c)/(T-d)）」。判据 $\Delta\delta_c$ 则是一个隐含了 $\delta_v\simeq0.0104$ 的两参数关系。以上均不改变 G18、G22 的缺口状态，也未引入新物理假设。
