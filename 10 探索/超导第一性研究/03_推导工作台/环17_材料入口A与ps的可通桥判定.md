# 环 17：材料入口 $A$ 与 $p_s$ 的可通桥判定（第 143 轮）

**状态**：工作台推导卡；主链 (17.1)–(17.2) 原文不改，06／08 台账不动，缺口状态栏不动。
**触发**：第 142 轮 R-151 给出 $g(2s-CK)=CA$，但 $A=2\operatorname{Cov}(\ell,\dot\ell)$ 与 $p_s=\partial p/\partial s$ 仍是自由入口（脚本里 $A=0.02$、$p_{\rm sync}=1-e^{-s/S_0}$ 都只是示意）。本轮判这两条桥哪条能接到物质状态。

---

## 一句话

$$\boxed{\ \varepsilon(\lambda\ell)=\varepsilon(\ell)\ \Rightarrow\ L\ell=0\ \Rightarrow\ \dot\ell=\mu\ell:\ A=2\mu s^2>0,\ \dot\varepsilon=0\ }\tag{R143.1}$$

$$\boxed{\ p=1-F_\nu\!\left(\frac{\nu\sigma_c^2}{s^2}\right)\ \Rightarrow\ p_s=\frac{\epsilon_\nu(x)}{s}\,p,\quad \epsilon_\nu(x)=2x\,\frac{f_\nu(x)}{\bar F_\nu(x)},\quad x=\frac{\nu\sigma_c^2}{s^2}\ }\tag{R143.2}$$

$$\boxed{\ \eta=\frac{2N-1}{2(N-1)}\,\epsilon_\nu(x)\,a\lambda(a),\qquad \eta<1\iff \epsilon_\nu(x)\,a\lambda(a)<1-\frac1{2N-1}\ }\tag{R143.3}$$

第一条是**否证**：$A$ 不可能由环 7 的 $\mathcal B^\pm$ 单独给出，必须拆成仿射／非仿射两路。第二条是**接通**：$p_s$ 可由环 15 的阈值尾直接算出，不必再用指数型读数。第三条把反馈型上限化为两个可追溯标量的乘积条件。

---

## 一、$A$ 的桥：尺度不变性给出的否证

### 1.1 亏角对边长是零次齐次

单形的面角由余弦定理给，$\cos\theta=(a^2+b^2-c^2)/(2ab)$。对任意 $\lambda>0$，

$$\frac{(\lambda a)^2+(\lambda b)^2-(\lambda c)^2}{2(\lambda a)(\lambda b)}=\frac{a^2+b^2-c^2}{2ab}\ \Rightarrow\ \theta(\lambda a,\lambda b,\lambda c)=\theta(a,b,c).\tag{R143.4}$$

对固定三角剖分，所有 $\theta_k$ 同时不变，故 $\varepsilon_v(\lambda\ell)=\varepsilon_v(\ell)$。记 $L_{ve}=\partial\varepsilon_v/\partial\ell_e$，沿 $\lambda$ 在 $\lambda=1$ 求导（Euler 齐次定理）：

$$\sum_e \ell_e\,\frac{\partial\varepsilon_v}{\partial\ell_e}=0,\qquad\text{即}\qquad L\ell=0.\tag{R143.5}$$

这是**恒等式**，不是近似；它也是"均匀伸缩不改亏角"（环 7／`临-1` 工作台）的精确形式。

### 1.2 仿射驱动生产 $A$，却不生产 $\varepsilon$

取 $\dot\ell=\mu\ell$。样本方差 $s^2=\frac1m\sum_e(\ell_e-\bar\ell)^2$ 的生产

$$A=\dot s^2=\frac{2\mu}{m}\sum_e(\ell_e-\bar\ell)\ell_e=2\mu s^2>0\quad(\mu>0,\ s>0),\tag{R143.6}$$

其中用了 $\sum_e(\ell_e-\bar\ell)=0$；同时 $\dot\varepsilon=L\dot\ell=\mu L\ell=0$，故 $\dot v_\tau=v_\tau'(\varepsilon)\dot\varepsilon=0$、环 7 的 $K(\varepsilon)$ 与环 8 的 $C_{ij}=f(\varepsilon_i-\varepsilon_j)$ 在该瞬间全部静止。

**判定**：存在 $A>0$ 而整个 $\varepsilon$ 扇区完全静止的合法驱动。环 6 的 $\mathcal B^\pm$ 按 $\mathcal H_{ij}\dot{\mathcal H}_{ij}$ 分流，其微观系数只经 $v_\tau(\varepsilon)$ 与 $K(\varepsilon)$ 依赖 $\varepsilon$；因此 $\mathcal B^\pm$ 不能决定 $A$，把 $A$ 读成 $\mathcal B$ 是跨对象代入（$\mathcal B$ 在节点固有时 $\tau_i$ 上，$A$ 在边长 $\ell_e$ 上）。反向也不能由 $A$ 决定 $\mathcal B$。上一轮留下的"从 $\mathcal B^\pm$ 接回 $A$"这条桥**不通**。

### 1.3 唯一合法的桥：仿射／非仿射分解

把边长率按齐次方向投影：

$$\dot\ell_e=\mu\,\ell_e+\delta\dot\ell_e,\qquad
A=2\mu s^2+2\operatorname{Cov}(\ell,\delta\dot\ell),\qquad
\dot\varepsilon=\tilde L\,\delta\dot\ell,\tag{R143.7}$$

其中 $\tilde L$ 是去掉均值漂移后的 $L$。第一项（膨胀，trace 部）**只**进 $A$，不进 $\varepsilon$；第二项（剪切／缺陷重排，deviatoric 部）同时进 $A$ 与 $\varepsilon$，才与环 7 的 $\mathcal B^\pm$ 同源。外部标准把这一步叫仿射／非仿射分解（Falk–Langer $D_{\min}^2$；迹／无迹分裂 $\epsilon_{ij}=\frac{\mathrm{Tr}\epsilon}{2}I+Q_{ij}$），这里只借其分解结构，不搬其动力学。

**结论**：$A$ 不是"一个待给的数值"，而是两条不同物质通道的和：$2\mu s^2$ 来自整体膨胀率，$\mathrm{Cov}(\ell,\delta\dot\ell)$ 来自非仿射重排。写进自洽方程时必须保留两路；只给一个 $A$ 会让反馈型上限 $\eta$ 掩盖掉它的物质来源。$\mu$ 与 $\delta\dot\ell$ 的第一性方程仍缺（`临-1` 的材料 $d_e$、$\dot\ell_e$ 方程），故 $A$ 的材料值仍不在链内。

---

## 二、$p_s$ 的桥：环 15 尾概率的弹性

### 2.1 精确微分

环 15 (15.1) 与 R90 的尾式在环 17 的读法下取 $V_{\rm coh}=s^2$（$s^2$ 是 $\ell$ 的总体方差，局部估计 $\hat V_\ell/s^2\sim\chi^2_\nu/\nu$）：

$$p(s)=\bar F_\nu(x),\qquad x=\frac{\nu\sigma_c^2}{s^2},\qquad \bar F_\nu=1-F_\nu.\tag{R143.8}$$

由 $d\bar F_\nu/dx=-f_\nu$ 与 $dx/ds=-2x/s$：

$$p_s=\frac{2x}{s}f_\nu(x)>0,\qquad
\epsilon_\nu(x):=\frac{s\,p_s}{p}=2x\,h_\nu(x),\qquad h_\nu=\frac{f_\nu}{\bar F_\nu}.\tag{R143.9}$$

$h_\nu$ 是 Gamma（形状 $\nu/2$、尺度 2）的危险率：形状 $>1$ 时从 0 单调升至 $1/2$（NIST；`临-1` 之外的 B 类工具）。于是

$$0<\epsilon_\nu(x)<x,\qquad \epsilon_\nu(x)\sim\frac{2x^{\nu/2}}{2^{\nu/2}\Gamma(\nu/2)}\ (x\to0^+),\qquad \epsilon_\nu(x)\sim x-\nu+2\ (x\to\infty).\tag{R143.10}$$

### 2.2 反馈因子的完全分解

把 $p_s=\epsilon p/s$ 与 $N=pN_{\rm eff}$ 代入 R-151 的 $C$ 与 $\eta$：

$$C=\frac{2N-1}{N(N-1)}N_{\rm eff}p_s=\frac{2N-1}{(N-1)s}\,\epsilon_\nu(x),\tag{R143.11}$$

$$\eta=\frac{CK}{2s}=\frac{2N-1}{2(N-1)}\,\epsilon_\nu(x)\,a\lambda(a).\tag{R143.12}$$

$N_{\rm eff}$ 与 $p$ **分别消去**，只剩 $N$；材料输入缩成三样：峰度经 $DF_n(\kappa)$ 给的 $\nu$（R-150）、阈值比 $x=\nu\sigma_c^2/s^2$、尾部位置 $a$（R-151）。可解条件即 (R143.3)。

### 2.3 与示意 $p_{\rm sync}$ 的差别（为什么不能用读数代）

第 142 轮脚本用 $p_{\rm sync}=1-e^{-s/S_0}$，其弹性

$$\epsilon_{\rm ad}(s)=\frac{s}{S_0\bigl(e^{s/S_0}-1\bigr)}<1,\qquad \epsilon_{\rm ad}'<0.\tag{R143.13}$$

环 15 的 $\epsilon_\nu(x)$ 随 $x=\nu\sigma_c^2/s^2$ 增（即随 $s$ **减**）而增，且无上界。两者不仅数值不同，**单调方向相反**：示意式在 $s$ 变大时把反馈压小，环 15 式在 $s$ 变大时把反馈压小也是对的（$x$ 变小），但量级可差一个数量级，且示意式永不超过 1，会系统性掩盖 $\eta\to1$ 的失效面。用 $p(t)$ 的读数拟合一个指数型 $p_{\rm sync}$ 不能替代尾概率的链式微分——这是 `审-6` 在**弹性层**的表现，与 R-151 的机制错配并列。

### 2.4 失效面在渗流阈值处并不遥远

取 $\nu=9$（环 10 的 $n_{\rm cell}=10$ 正态基准）与 $p_c=0.592746$，阈值处 $x_{pc}=\chi^2_9$ 的上 $p_c$ 分位 $=7.4271$，弹性 $\epsilon_\nu(x_{pc})=2.5929$。由 (R143.3) 反解右尾临界位置 $a_\ast$：$\epsilon_\nu(x_{pc})\,a_\ast\lambda(a_\ast)=1$ 给 $a_\ast=0.3686$。即**尾部选择门槛只要超过约 $0.37s$，反馈型上限就在 $p_c$ 处已经触发**，扩大速度无解。对照：第 142 轮示意用的 $a=0.5$ 正在这一侧（其 $x_\ast=6.20<x_{pc}$）；若仍用 $\epsilon_{\rm ad}<1$ 的读样式，该失效面被完全掩盖。这给出 `临-25` 一个此前没有的定量通道：扩大项无解不是"无处可扩"，而是 $\epsilon_\nu a\lambda$ 越过 1。

---

## 三、数值核查

见 `04_计算验证/环17_材料入口的可通桥.py`（六段断言全过，四面板图，无拟合）。

| 段 | 内容 | 判据 |
|:--|:--|:--|
| A | 余弦比值 $\lambda$ 不变、随机三角剖分 $L\ell\approx0$ | 残差 $<10^{-12}$ |
| B | $\dot\ell=\mu\ell$ 给 $A=2\mu s^2>0$ 而 $\Delta\varepsilon\approx0$ | 反例成立 |
| C | 卡方弹性 $\epsilon_\nu(x)=2xh_\nu(x)$ vs 数值链式的 $sp_s/p$ | 逐点残差 $<10^{-9}$ |
| D | $\eta$ 分解恒等式（原始 $C$ 式 vs 因子式） | 残差 $<10^{-12}$ |
| E | 可解边界 $\epsilon\,a\lambda=1$ 反解 $x_\ast$ 与 $s_\ast$ | 单调、唯一 |
| F | 示意弹性 $\epsilon_{\rm ad}$ 与环 15 弹性对照 | $\epsilon_{\rm ad}<1$，环 15 弹性达 434 |
| G | 阈值 $p_c$ 处弹性与临界尾部 $a_\ast$ | $\epsilon=2.5929$，$a_\ast=0.3686$ |

---

## 四、历史唯物主义合规

1. **物质第一性**：亏角的尺度不变性是几何本身，不随读数改；$p_s$ 来自局域方差尾概率（物质的实际涨落），不是从 $p(t)$ 读数反写的参数。
2. **必然／偶然分层**：(R143.4)–(R143.5)、(R143.9)、(R143.11)–(R143.12) 是必然性（恒等式／链式法则）；$\mu$、$\delta\dot\ell$、$\nu$、$\sigma_c$、$a$ 是偶然性（材料与制备）。
3. **结构同构不是还原**：危险率、仿射／非仿射分解只作外部工具；CQM 不声称推出 Gamma 分布或 Falk–Langer 测度。
4. **批判性**：否证了上一轮留下的"$A$ 从 $\mathcal B^\pm$ 接回"路线，保留其自洽方程形式而改正其入口解释。

---

## 五、不能推出什么（必填）

1. 不给 $\mu$、$\delta\dot\ell$ 的材料方程；$A$ 仍无链内数值，只给出它的两路分解。
2. 不把 $p_{\rm sync}$ 与 $p_{\rm pair}$ 等同（**`审-6` 保持**）；(R143.2) 是"环 17 若采用环 15 尾式"的条件结果，不声称链已选定该函数族。
3. 不给 $\nu$、$\sigma_c$、$a$ 的材料值；$x_\ast$／$s_\ast$ 只是结构边界。
4. 不闭合 `审-6`／`临-1`／`临-2`／`临-24`／`临-25`；唯一编号仍 37，闭合数仍 0。
5. 不改 (17.1)、(17.2) 原文，不改环 18 上限判据，不动 06。

---

## 六、Lean 承载

`05_Lean验证/MaterialBridge.lean`（16 条 theorem，退出码 0，无警告、无禁用项）：

| 定理 | 内容 |
|:--|:--|
| `cos_ratio_scale` / `angle_scale_input` | 余弦比值的 $\lambda$ 不变性 (R143.4) |
| `affine_pointwise` / `affine_variance_rate` / `affine_mean` | 仿射驱动的方差生产逐点式与有限样本式 |
| `two_point_affine_positive` | 两点样本上 $A>0$ 的非平凡实例 |
| `homogeneous_kernel` / `matrix_homogeneous_kernel` | $L\ell=0\Rightarrow L(\mu\ell)=0$ (R143.5) |
| `hasDerivAt_inv_sq` | $\dfrac{d}{dt}\theta/t^2=-2\theta/s^3$ |
| `elasticity_chain` | $p=1-S(\theta/s^2)$ 的导数与弹性 $\epsilon=2xS'/p$ |
| `elasticity_from_hazard` | $\epsilon p=2xf$ 的代数式 |
| `eta_factor` | $N_{\rm eff}$、$p$ 消去，$\eta$ 因子分解 (R143.12) |
| `finite_N_factor_gt_one` | 有限 $N$ 因子 $>1$ |
| `eta_lt_one_bound` / `eta_eq_one_critical` | 可解界与临界边界 |
| `lt_exp_sub_one` / `ad_hoc_elasticity_lt_one` | 示意弹性严格小于 1 (R143.13) |

---

## 七、复现

```bash
python "10 探索/超导第一性研究/04_计算验证/环17_材料入口的可通桥.py"
cd "08 理论组织和形式化框架/04_Lean对接/Lean源码"
export LEAN_PATH="$(ls -d .lake/packages/*/.lake/build/lib/lean | tr '\n' ':')"
/d/DevTools/.elan/toolchains/leanprover--lean4---v4.29.1/bin/lean \
  "../../../10 探索/超导第一性研究/05_Lean验证/MaterialBridge.lean"
```
