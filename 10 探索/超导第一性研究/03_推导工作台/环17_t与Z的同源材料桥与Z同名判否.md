# 环 15/17/14.A：粗粒化指数 $t$ 与零点方差 $Z$ 的同源材料桥，以及 $Z=1+\lambda$ 的同名判否

**状态**：A 类严格（代数恒等式与回修）＋ B 类材料桥（Debye 零点位移、Hopfield 谱矩；外部只作工具）。
**边界**：只处理第 146 轮末留下的"把 $\epsilon_\nu$ 的 $t$ 与 $\sigma_c^2/Z$ 的 $Z$ 用同一组材料量表示"这一问；不动 (15D.1)(15D.3)(10B.1)(FE10.1) 原式，不改 06，`审-4`／`审-6`／`M8` 状态栏不动。

---

## 一、先回修 R-145 的 (R154.2)：漏掉交点处的 $w(T_\ast)$

环 15 原文 (15D.3) 的归一自变量是

$$
x(T)=\frac{n_{\rm cell}\sigma_c^2}{Z\,w(T)},\qquad
p_{\rm pair}(T)=1-F_\nu(x(T)).
\tag{R156.1}
$$

渗流交点在有限温度 $T_\ast=T_c$ 处，故 $x(T_c)=x_\ast=\bar F_\nu^{-1}(p_c^{1/t})$。由此

$$
\boxed{\ \frac{\sigma_c^2}{Z}=\frac{x_\ast\,w(T_c)}{n_{\rm cell}}\ }
\tag{R156.2}
$$

R-145 写成 $\sigma_c^2=x_\ast Z/n_{\rm cell}$，等价于把 $T_\ast$ 钉在 $0$（$w(0)=1$）——**漏项，予以回修**；$\epsilon_\nu=2x_\ast h_\nu(x_\ast)$ 用的是交点处的 $x_\ast$，**不受影响**（R-145 的数值 $2.5929$ 保留）。量级：$T_c/\omega_D=0.01$ 时修正因子 $w=0.99967$（可忽略）；$0.3$ 时 $w=0.7587$（不可忽略）。修正值恒不超过旧值，且随 $T_c$ 单调减。

---

## 二、$Z$ 的链内材料表达（A 类代数）

$R71$／环 02 (W3.6) 给零点相干二阶矩

$$
Z=V_{\rm coh}(0)=\sigma_0^2
=c_\varepsilon^2\,\frac{(6\pi^2)^{4/3}}{16\pi^2}\Bigl(\frac{\ell_q}{a_n}\Bigr)^4,
\qquad \ell_q=\Bigl(\frac{\hbar}{\rho_m c_s}\Bigr)^{1/4},\quad a_n=n^{-1/3}.
$$

代入 $\rho_m=Mn$、$Q=(6\pi^2n)^{1/3}$、$\omega_D=c_sQ$，并用恒等式
$\frac{(6\pi^2)^{4/3}}{16\pi^2}=\frac38(6\pi^2)^{1/3}$，得

$$
\boxed{\ Z=\frac38\,c_\varepsilon^2\,\frac{\hbar\,Q}{M c_s}
=\frac38\,c_\varepsilon^2\,\frac{\hbar\,\omega_D}{M c_s^2}\ }.
\tag{R156.3}
$$

**Debye 零点核对（B 类外部工具）**：Debye 谱 $g(\omega)=3\omega^2/\omega_D^3$ 给
$\langle u^2\rangle_0=\int_0^{\omega_D}\frac{\hbar}{2M\omega}g(\omega)d\omega
=\frac{3\hbar}{4M\omega_D}$（NCrystal 文献卡 L147a 的 $f(0)=1/4$ 同式）。于是

$$
Z=\tfrac12\,c_\varepsilon^2\,Q^2\,\langle u^2\rangle_0 .
\tag{R156.4}
$$

两条路与 (W3.6) 数值逐点相同（Al 材料截面：$9.185827\times10^{-4}$ 三式一致）。**物理读法**：链内 $Z$ 不是新参数，它就是"几何曲率耦合 $c_\varepsilon^2$ 乘 Debye 零点位移、再乘节点测度尺度 $Q^2$"；$Z$ 与 $\omega_D$、$\lambda$ 现在由**同一组材料量** $\{c_\varepsilon,\hbar,n,M,c_s\}$ 表示。

---

## 三、$\lambda$ 与 $Z/\lambda$：FE10 与环 10 两条同源路径

FE10（框架扩展候选，已落地注记）＋链内 Debye 二阶矩 $\langle\omega^2\rangle_{\rm ph}=\tfrac35\omega_D^2$：

$$
\lambda=\frac{\eta_{\rm chain}}{M\langle\omega^2\rangle_{\rm ph}}
=\frac{\frac9{10}N(0)z g^2c_\varepsilon^2(1-\rho)Q^2}{M\cdot\frac35 c_s^2Q^2}
=\frac32\,\frac{N(0)z g^2c_\varepsilon^2(1-\rho)}{M c_s^2}.
\tag{R156.5}
$$

与 (R156.3) 相除，$c_\varepsilon^2,M,c_s^2$ **全部约掉**：

$$
\boxed{\ \frac{Z}{\lambda}=\frac{\hbar\omega_D}{4N(0)z g^2(1-\rho)}\ }.
\tag{R156.6}
$$

环 10 (W3.9) 的路径 $\lambda=4N(0)g^2Z(1-\rho)/(\hbar\omega_D)$ 给
$Z/\lambda=\hbar\omega_D/[4N(0)g^2(1-\rho)]$。两者之比恰为 $1/z$：

- **$z=1$ 时两条已落地路径完全一致**；FE10 的配位数 $z>1$ 时存在 $O(z)$ 的未消因子。这不是新公设，是两处已登记公式的**口径差**，登记为残余 $O(1)$ 因子，不私自吸收到 $g$ 或 $c_\varepsilon$ 里。
- 外部对照：McMillan–Hopfield $\lambda=\eta/(M\langle\omega^2\rangle)$ 与 $\langle\omega^2\rangle\simeq\frac12\theta_D^2$（Gaspari–Gyorffy／RMTA 约定，L147b）与链内 $\frac35$ 的差是**权重约定差**，R-101 已记为 $\frac56$，本轮不改。

---

## 四、$Z=1+\lambda$ 的同名判否（A 类判定＋B 类量级）

Eliashberg 侧 $Z_{\rm el}=1+\lambda$ 是**准粒子波函数重整化／质量增强**：$\lambda=2\int\alpha^2F/\omega$，低能 $m^\ast=m(1+\lambda)$（L147c；不同文献对 $Z$ 与 $Z^{-1}$ 的记号约定不统一，但重整化是 $O(1)$ 量级这一点稳健）。链内 $Z$ 是**亏角相干涨落的零点二阶矩**，(R156.3) 的量级由 $(\ell_q/a_n)^4\sim10^{-3}$ 定。

取 R-145 量级 $c_\varepsilon=0.5$，用其材料表的 $\ell_q/a_n$ 与观测 $\lambda$：

| 材料 | $Z_{\rm chain}$ | $Z_{\rm el}=1+\lambda_{\rm obs}$ | 比值 |
|:--|--:|--:|--:|
| Al | $9.3652\times10^{-4}$ | 1.43 | $6.55\times10^{-4}$ |
| Nb | $4.5648\times10^{-4}$ | 1.95 | $2.34\times10^{-4}$ |
| V  | $6.3286\times10^{-4}$ | 1.80 | $3.52\times10^{-4}$ |
| Ta | $1.9506\times10^{-4}$ | 1.65 | $1.18\times10^{-4}$ |
| Pb | $2.8422\times10^{-4}$ | 2.55 | $1.11\times10^{-4}$ |

$$
\boxed{\ Z_{\rm chain}\sim10^{-4}\text{--}10^{-3}\ \ll\ Z_{\rm el}=O(1)\quad\Rightarrow\quad Z_{\rm chain}\ne Z_{\rm el}\ }
\tag{R156.7}
$$

**判否**：把 Eliashberg 的 $1+\lambda$ 代入 (15D.3) 的 $Z$ 是把同名不同物混同，禁止。这是 `审-6` 的**第四层错配：同名对象错配**（前三层为读数当自变量、尾部机制错配、统计对象错配）。反过来，链内 $Z$ 仍可通过 $\lambda\propto Z$ 与谱矩**同源**（(R156.6)），这才是"与 $\alpha^2F$ 谱矩自洽"的正确含义。

---

## 五、$t$ 不是材料量：$\epsilon_\nu$ 的普适性与 $r(T)$ 的同源材料表达

**$t$ 的归属**：R-145 已判 $t=\ln p_c/\ln p_{\rm pair}^{\rm thr}$ 属渗流占据普适类、与材料无关，$t\ne t_\Upsilon$（不同普适类）。外部渗流理论确认 $p_c$ 依赖晶格局部结构而临界指数普适（L147d）。因此"把 $t$ 用材料量表示"在链内**不成立**：强行让 $t$ 随材料漂移会破坏 R-145 的压缩映射判定与渗流类归属。我们能给出的是它的**唯一入口**：

$$
x_\ast(t)=\bar F_\nu^{-1}\!\bigl(p_c^{1/t}\bigr),\qquad
\epsilon_\nu(t)=2x_\ast(t)h_\nu(x_\ast(t)),
\tag{R156.8}
$$

即 $t$ 只经 $\epsilon_\nu(t)$ 进入 $r(T)$。数值：$t=1\Rightarrow\epsilon_\nu=2.592946$（R-145 的 $2.5929$）、$t=5\Rightarrow0.643190$，单调减。

**$r(T)$ 两支改成同源材料量**（沿用 $\alpha_V=\bar\gamma C_V/(K_TV)$、$K_T=\rho_mc_s^2=Mn c_s^2$、$w$ 的 Debye 两支）：

低温绝缘体（$C_V/V=\frac{2\pi^2}{5}k_B(k_BT/\hbar c_s)^3$、$|d\ln w/dT|\to\frac{2\pi^2}{3}T/\omega_D^2$）：

$$
\boxed{\ r_{\rm low}(T)=\frac{2\bar\gamma}{5}\,
\frac{(k_BT)^2Q^2}{\epsilon_\nu(t)\,\hbar\,M\,n\,c_s^3}\ }\propto T^2 .
\tag{R156.9}
$$

高温（Dulong–Petit $\alpha_V\to3\bar\gamma k_B/(Mc_s^2)$、$|d\ln w/dT|\to1/T$）：

$$
\boxed{\ r_{\rm high}(T)=\frac{2\bar\gamma k_BT}{\epsilon_\nu(t)\,M c_s^2}\ }\propto T .
\tag{R156.10}
$$

两式的输入是同一组 $\{\bar\gamma,M,n,c_s,\hbar,k_B,\epsilon_\nu(t)\}$；**$Z$ 完全不出现**。数值核对：Al 截面（$\bar\gamma=2$、$\omega_D=428$K、$Q=1.527\times10^{10}$/m、$c_s=3668$m/s）直接式与闭式逐点残差 $<10^{-12}$、低温双对数斜率 $2.000000$、$r(10\,{\rm K})=9.77\times10^{-5}$。把 $Z$ 人为放大 $10^6$ 倍，交点条件给 $\sigma_c^2$ 同比放大、$x_\ast$ 与 $\epsilon_\nu$ 不变，故 $r$ 不变——**$r$ 对 $Z$ 的绝对标度不敏感**。

**边界**：$K_T=Mn c_s^2$ 沿用链内纵波模量口径（R29 的 $\rho_mc^2=na^2\kappa_s$）；若改用体模量需乘泊松比相关的 $O(1)$ 因子，仍外生。$\bar\gamma$、$n$、$M$、$c_s$ 的具体值不由此给出。

---

## 六、数值与 Lean

- 脚本 `../04_计算验证/环17_t与Z的同源材料桥.py`（六面板函数图 + 摘要 CSV）：A 段 $w(T_c)$ 修正、B 段三条 $Z$ 路径恒等、C 段两路径比 $1/z$、D 段同名量级、E 段 $\epsilon_\nu(t)$ 与 $r$ 两支闭式、F 段解析导数两支（低温系数 $6.579758$ vs $2\pi^2/3=6.579735$、高温 $0.999$）。全部断言通过，无拟合。
- Lean `../05_Lean验证/MaterialBridgeTZ.lean`（**19 条定理**，退出码 0、零警告）：(R156.1)–(R156.6) 代数恒等、(R156.7) 的 $Z_{\rm chain}<1<1+\lambda\Rightarrow Z_{\rm chain}\ne Z_{\rm el}$、(R156.2) 的 $w$ 因子与 $\le x_\ast/n$、(R156.9)(R156.10) 两支闭式、$Z$ 缩放不变与低温二次型。无 `axiom`／`sorry`／`admit`／`native_decide`／`unsafe`。

## 七、结论与边界

1. **回修**：R-145 (R154.2) 乘回 $w(T_c)$；$\epsilon_\nu=2.5929$ 不变。
2. **接通**：$Z$ 已由同一组材料量 $\{c_\varepsilon,\hbar,n,M,c_s\}$ 表示，并与 Debye 零点位移严格等价；$\lambda$ 与 $Z$ 同源，$Z/\lambda$ 中 $c_\varepsilon^2,M,c_s^2$ 全约掉。
3. **判否**：$Z_{\rm chain}\ne Z_{\rm el}=1+\lambda$（同名不同物，第四层错配）；FE10 与环 10 的 $Z/\lambda$ 差 $1/z$，$z=1$ 才一致。
4. **不可做的那半**：$t$ 是普适指数，不能由材料量表示；只经 $\epsilon_\nu(t)$ 入 $r$。$r$ 两支的闭式不含 $Z$，与谱矩的自洽性体现在 $\lambda\propto Z$ 而非 $Z=1+\lambda$。
5. **不动**：所有原式与 06；`审-4`／`审-6`（只加注记层第四层）／`M8` 状态栏；不闭合任何编号，唯一编号仍 37、闭合数仍 0。
