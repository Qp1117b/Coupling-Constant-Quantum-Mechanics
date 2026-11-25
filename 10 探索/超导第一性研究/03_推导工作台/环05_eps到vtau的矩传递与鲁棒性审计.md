# 环 4→5→9 接口：$\varepsilon$ 的矩到 $v_\tau$ 的矩，及链路对载体细节的鲁棒性

**轮次**：第 139 轮（2026-11-25）；成果登记 R-148
**性质**：接口严格化＋鲁棒性审计（A 类代数）；不改任何缺口状态栏，不动 06／01／08／研究站。
**承接**：R147（$\varepsilon$ 的统计归 FG／材料）。既然链内不再产生 $\varepsilon$，就必须回答：链的下游到底需要 $\varepsilon$ 的什么信息？

---

## 一、前件

1. **(5.1)**：$v_\tau=\sqrt{1-\varepsilon/2\pi}$（FG 接口，【假设】）。
2. **(9.1)**：$\langle(\delta C_{ij})^2\rangle=2\kappa_f^2\sigma^2(1-\rho_{ij})$，$\sigma^2=\mathrm{Var}(\varepsilon)$。
3. **`审-2` 的 $\kappa_f$**：$\kappa_f=-\partial_\varepsilon\ln v_\tau$，其 FG 推导给 $\kappa_f(\varepsilon_0)=1/[4\pi(1-\varepsilon_0/2\pi)]$、$\kappa_f(0)=1/(4\pi)$。
4. **R147**：$\varepsilon$ 的统计是 FG／材料输入。

---

## 二、式

### （A）一阶传递是精确的，不是近似

有理化恒等式（Lean `sqrt_sub_sqrt`）：

$$\sqrt a-\sqrt b=\frac{a-b}{\sqrt a+\sqrt b}\qquad(a,b>0). \tag{4D.1}$$

代入 $a=1-\varepsilon_0'/2\pi$、$b=1-\varepsilon_0/2\pi$（$\varepsilon_0'=\varepsilon_0+\delta$）：

$$\boxed{\ v_\tau(\varepsilon_0+\delta)-v_\tau(\varepsilon_0)=-\frac{\delta/2\pi}{v_\tau(\varepsilon_0+\delta)+v_\tau(\varepsilon_0)}\ }\tag{4D.2}$$

这是**恒等式**：一阶系数 $v_\tau'(\varepsilon_0)=-1/(4\pi v_0)$ 不需要 Taylor 展开，右端分母的 $\delta$ 依赖给出全部高阶项。数值（$\varepsilon_0=0.30$、$v_0=0.975835$）：

| $\delta$ | 精确 $\Delta v_\tau$ | 一阶 $-1/(4\pi v_0)\delta$ | 相对偏差 |
|--:|--:|--:|--:|
| $10^{-3}$ | $-8.1552\times10^{-5}$ | $-8.1548\times10^{-5}$ | $4.2\times10^{-5}$ |
| $10^{-2}$ | $-8.1582\times10^{-4}$ | $-8.1548\times10^{-4}$ | $4.2\times10^{-4}$ |
| $10^{-1}$ | $-8.1892\times10^{-3}$ | $-8.1548\times10^{-3}$ | $4.2\times10^{-3}$ |

### （B）$\kappa_f$ 的独立一致性

由 (4D.2)，$v_\tau'=-1/(4\pi v_0)$，而

$$\kappa_f=-\frac{v_\tau'}{v_0}=\frac{1}{4\pi v_0^{2}}=\frac{1}{4\pi(1-\varepsilon_0/2\pi)} .\tag{4D.3}$$

**与 `审-2` 的 FG 推导逐字相同**（Lean `slope_consistency`）。这是 (5.1) 与 $\kappa_f$ 式子相容的独立检验：两条路线（对 (5.1) 求导 vs FG 几何）给同一个 $\kappa_f$。

### （C）矩传递

$$\mathrm{Var}(v_\tau)=\kappa_f^2v_0^2\,\sigma^2+O(\sigma^4),\qquad
\mathrm{Var}(\lambda_{ij})=\mathrm{Var}(\ln v_{\tau,j}-\ln v_{\tau,i})=2\kappa_f^2\sigma^2(1-\rho). \tag{4D.4}$$

第二式就是环 9 的 (9.1)（$\lambda_{ij}=\ln r_{ij}$，独立时 $\rho=0$）。

### （D）Jensen：涨落使平均钟速变慢

$v_\tau(\varepsilon)=\sqrt{1-\varepsilon/2\pi}$ 在定义域上**凹**（Lean `sqrt_concave_two`、`slowdown_nonneg`），故

$$\langle v_\tau\rangle\le v_0,\qquad v_0-\langle v_\tau\rangle=\frac{\sigma^2}{32\pi^2v_0^3}+O(\mu_3). \tag{4D.5}$$

数值（$\varepsilon_0=0.3$）：

| $\sigma$ | $\langle v_\tau\rangle$ | $v_0$ | 减慢量 | $\sigma^2/(32\pi^2v_0^3)$ |
|--:|--:|--:|--:|--:|
| 0.005 | 0.9758347 | 0.9758348 | $8.52\times10^{-8}$ | $8.52\times10^{-8}$ |
| 0.010 | 0.9758344 | 0.9758348 | $3.41\times10^{-7}$ | $3.41\times10^{-7}$ |
| 0.050 | 0.9758263 | 0.9758348 | $8.52\times10^{-6}$ | $8.52\times10^{-6}$ |

$\sigma\le0.05$ 时二阶公式的最大相对偏差 $0.01\%$。

---

## 三、鲁棒性审计（本轮的实际判定）

用三种分布（截断高斯、均匀、Beta）在同一 $(\varepsilon_0,\sigma^2)$ 下求积（`scipy.integrate.quad`，重归一化，无抽样噪声）：

| 分布 | $\sigma$ | $\langle v_\tau\rangle$ | 二阶预测 | $\mathrm{Var}(v_\tau)$ | $\kappa_f^2v_0^2\sigma^2$ | 偏差 |
|:--|--:|--:|--:|--:|--:|--:|
| 截断高斯 | 0.02 | 0.9758334 | 0.9758334 | $2.660\times10^{-6}$ | $2.660\times10^{-6}$ | $10^{-5}$ |
| 截断高斯 | 0.10 | 0.9757649 | 0.9758007 | $6.565\times10^{-5}$ | $6.650\times10^{-5}$ | $1.3\times10^{-2}$ |
| 均匀 | 0.10 | 0.9758007 | 0.9758007 | $6.651\times10^{-5}$ | $6.650\times10^{-5}$ | $1.4\times10^{-4}$ |
| Beta | 0.10 | 0.9758005 | 0.9758007 | $6.687\times10^{-5}$ | $6.650\times10^{-5}$ | $5.6\times10^{-3}$ |

同 $\sigma$ 下三种分布的 $\mathrm{Var}(v_\tau)$ 相对离散：$0.02\%$（$\sigma{=}0.02$）、$0.14\%$（$0.05$）、$1.83\%$（$0.10$）。

**判定分三层**：

| 下游量 | 依赖什么 | 鲁棒性 |
|:--|:--|:--|
| $\mathrm{Var}(v_\tau)$、$\mathrm{Var}(\lambda_{ij})$（环 5／9） | 仅 $(\varepsilon_0,\sigma^2,\rho)$ | **形状无关**（$\le1.8\%$） |
| Jensen 位移的一阶项（4D.5） | 仅 $\sigma^2$ | 形状无关 |
| Jensen 位移的三阶修正 | 三阶矩 $\mu_3$ | **依赖形状**（图 B 三条曲线在 $\sigma\gtrsim0.03$ 分道：$10^{-2}$／$10^{-12}$／$10^{-8}$） |
| 环 15 的尾概率 $p_{\rm pair}$ | 完整分布族 | **完全依赖形状**（chi-square 尾的前提） |

**结论**：R147 的判定（$\varepsilon$ 归 FG）**不伤害环 5 与环 9**——这两环只用二阶矩，而二阶传递是形状无关的（$\le1.8\%$）。受影响的只有：Jensen 的三阶修正（量级 $\sigma^4$，可忽略）与环 15 的尾概率（必须额外输入分布族）。

---

## 四、状态

- **环 5 的 (5.1) 获独立支持**：$v_\tau'$ 与 $\kappa_f$ 的一致性（4D.3）是纯代数恒等式，不需 FG 推导作前提；反过来，它验证了 `审-2` 的 $\kappa_f$ 式子与 (5.1) 不矛盾。**状态栏不动**（(5.1) 仍【假设】——它是 FG 接口，不是由 (1.2) 推出）。
- **环 9 的 (9.1)**：$\sigma^2$ 的来源现确定为 FG／材料输入（R147），但 (9.1) 的**形式**不受影响。
- **`审-21`／`审-22`／`审-10`**：状态原样。
- **新增的接口登记（不设新编号）**：环 15 的 $p_{\rm pair}$ 需要 $\varepsilon$ 的**分布族**作为额外输入，不只是 $(\bar\varepsilon,\sigma^2)$。这原在 R90 的高斯假设里隐含，本轮把它显式化。
- **全链唯一编号仍 37、闭合数仍 0**。

---

## 五、不能推出什么（必填）

1. **不能推出 $\sigma^2$ 的数值**：它仍是 FG／材料输入（R147）。
2. **不能推出 $\varepsilon$ 的分布族**：本轮只说明哪些下游量不需要它，不给它。
3. **不能推出 $T_c$**：接口只保证传递链自洽，不提供能标。
4. **不能把 (5.1) 升格**：它仍是 FG 接口【假设】；本轮的恒等式只说明"给定 (5.1)，$v_\tau'$ 与 $\kappa_f$ 相容"，不说明 (5.1) 本身被推出。
5. **不能推出 Jensen 位移可观测**：$\sigma\le0.05$ 时减慢量 $<10^{-5}$，远低于任何直接测量；它只是结构事实。
6. **不能改 06**：(5.1)、(9.1)、`审-2` 的 $\kappa_f$ 原文均未动。

---

## 六、历史唯物主义合规

1. **基础决定读数**：$\varepsilon$ 的统计（物质的实际缺陷/再生产结构，基础）决定 $v_\tau$ 的矩（读数）；读数不能反写统计。
2. **必然性／偶然性分层**：(4D.1)–(4D.4) 是必然性（纯代数恒等式，与分布无关）；$\sigma^2$、$\mu_3$、分布族是偶然性（材料与制备）。
3. **物质第一性**：Jensen 位移说明"涨落使平均钟速变慢"——这是从 $v_\tau$ 的凹性直接读出的物质效应，不是拟合参数。
4. **未用社会范畴作物理证据**。
5. **结构同构不是还原**：借误差传播与 Jensen 不等式作标准工具。

---

## 七、Lean 承载

`05_Lean验证/MomentTransfer.lean`（7 条 theorem/lemma，`lake env lean` 退出码 0，无警告、无禁用项）：

| 定理 | 内容 |
|:--|:--|
| `sqrt_sub_sqrt` | $\sqrt a-\sqrt b=(a-b)/(\sqrt a+\sqrt b)$，$a,b>0$ |
| `abs_sqrt_sub_sqrt` | 绝对值版本 |
| `vtau_diff` | (4D.2) 的有理化差分形式 |
| `slope_consistency` | $-\kappa_fv_0=-1/(4\pi v_0)$，$\kappa_f=1/(4\pi v_0^2)$ |
| `sqrt_concave_two` | $\dfrac{\sqrt a+\sqrt b}{2}\le\sqrt{\dfrac{a+b}{2}}$ |
| `jensen_slowdown` / `slowdown_nonneg` | 两态 Jensen 与减慢量非负 |

---

## 八、复现

```bash
python "10 探索/超导第一性研究/04_计算验证/环04_eps到vtau的矩传递.py"

cd "08 理论组织和形式化框架/04_Lean对接/Lean源码"
export LEAN_PATH="$(ls -d .lake/packages/*/.lake/build/lib/lean | tr '\n' ':')"
/d/DevTools/.elan/toolchains/leanprover--lean4---v4.29.1/bin/lean \
  "../../../10 探索/超导第一性研究/05_Lean验证/MomentTransfer.lean"
```

数值脚本四组断言全过（一阶精确性、三分布二阶一致性、Jensen 单调、$\sigma\le0.05$ 时二阶误差 $<2\%$）；图四面板，无拟合。
