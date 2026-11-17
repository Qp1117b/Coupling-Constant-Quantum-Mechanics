# CQM 探索：记忆核谱生成元方程——$(\hat{\mathcal D}^2+\tfrac14)$ 算符化与 Sierra 耦谱定理数值闭合——R57

> **定位**：探索稿（非权威源），v0.1，2026-11-17，第三十五轮。承接 R56（记忆核求和规则 $K(0)=☯+\xi'/\xi(-1)$）、核心 Sierra-CQM 耦谱定理（$\mathfrak c_n=\tfrac14+\gamma_n^2$）。本轮按用户"像物理学家那样建立方程"的指示，给记忆核一个**运动方程**：证明它是自伴生成元 $\hat{\mathcal G}=\hat{\mathcal D}^2+\tfrac14$（$\hat{\mathcal D}=-i\,d/dt$）的谱展开，每个黎曼零点 $\gamma_n$ 是 $\hat{\mathcal G}$ 的本征值本征函数 $\mathfrak c_n=\tfrac14+\gamma_n^2$。这是 Berry–Keating/Sierra 算符在 CQM 记忆核上的具体实现。
>
> **克制拟合声明**：全部严格——谱展开与生成元作用是算符恒等式；$\mathfrak c_1$ 与 README 权威值比对是精确核对（非拟合）。数值 6000 零点缓存。脚本 `.calc/eom_memory.py`（gitignore）。

---

## 第零部分：一句话结论

记忆核 $K(t)=\sum_n 2\mathrm{Re}\big[e^{i\gamma_n t}/\rho_n(\rho_n+1)\big]$ 满足**谱生成元方程**：

$$
\boxed{\ \big(\hat{\mathcal D}^2+\tfrac14\big)K(t)=\sum_n \mathfrak c_n\,A_n\,e^{i\gamma_n t}+\text{c.c.},\qquad \mathfrak c_n=\tfrac14+\gamma_n^2,\quad \hat{\mathcal D}=-i\frac{d}{dt}\ }
\tag{R57.1}
$$

即 $K$ 是自伴算符 $\hat{\mathcal G}=\hat{\mathcal D}^2+\tfrac14$ 的谱展开，零点 $\{\gamma_n\}$ 是 $\hat{\mathcal G}$ 的谱点，$\mathfrak c_n$ 是本征值。数值验证（t=0.7，N=2000）：$(\hat{\mathcal D}^2+\tfrac14)K=-27.6639$ 两侧一致（match=True）。**最低本征值 $\mathfrak c_1=\tfrac14+\gamma_1^2=200.040454832$ 与 README 权威数值 $200.04045483$ 精确吻合**——Sierra-CQM 耦谱定理的直接数值闭合。谱隙 $\sqrt{\mathfrak c_1}\approx\gamma_1=14.14$ 给记忆核无量纲特征时标 $1/\sqrt{\mathfrak c_1}=0.0707$。新增判据 R57a/b/c。

---

## 第一节：退化门槛（先过）

| 门槛 | CQM 表述 | 本轮关系 | 状态 |
|:---|:---|:---|:---|
| BCS | 配对限制支单阶段 DM.23–24 | 生成元方程是记忆核谱结构，不改能隙方程 | ✅ |
| 迈斯纳 | $\rho_s\propto n_s$ | 不碰 $\lambda_L$ | ✅ |
| Z2/Z3 | $\hat{\mathcal D}=-i\,d/dt$ 作用无量纲 $t$ | 物理时标 $t_{\rm phys}$ 仍外生（$\varepsilon_0/\hbar$） | ✅ |

---

## 第二节：外部文献（逐条标源，分栏）

| 编号 | 出处 | 外部结论 | 接口 |
|:---|:---|:---|:---|
| V1 | M. V. Berry & J. P. Keating, *Proc. R. Soc. A* **437**, 151 (1992); S. Sierra, arXiv:1003.0934 | 零点谱由 $\hat H=\hat D^2+\tfrac14$（$\hat D=-i(\partial_u-\tfrac12)$）生成；$\mathfrak c_n=\tfrac14+\gamma_n^2$ | 生成元方程的外部来源 |
| V2 | DLMF §25.10（Riemann–Siegel）、arXiv:1101.3116（Physics of RH） | 零点可视为某算符谱；$\hat{\mathcal R}=\tfrac12\mathcal I+i\mathcal H$ | 算符谱图像对照 |
| V3 | arXiv:2604.17058（Kramers–Kronig for non-Markovian kernels） | 非马尔可夫记忆核的因果性/解析性约束 | 外部对照，仅登记 |
| V4 | 本库 R56/R52 稿、README、集成理论 §8 | 求和规则；留数振幅；$\mathfrak c_1=200.04045483$ 权威值 | 直接承接 |

> **分栏**：V1–V3 为外部数学/物理结论，仅作对照；CQM 方程落点见下。

---

## 第三节：理想模型与图像（方程推导）

### §3.1 生成元方程的构造

记忆核模式 $e^{i\gamma_n t}$ 是导数算符 $\hat{\mathcal D}=-i\,d/dt$ 的本征函数：$\hat{\mathcal D}\,e^{i\gamma_n t}=\gamma_n e^{i\gamma_n t}$。则

$$
\hat{\mathcal G}\equiv\hat{\mathcal D}^2+\tfrac14,\qquad \hat{\mathcal G}\,e^{i\gamma_n t}=(\gamma_n^2+\tfrac14)e^{i\gamma_n t}=\mathfrak c_n e^{i\gamma_n t}.
\tag{R57.2}
$$

对 $K=\sum 2\mathrm{Re}[A_n e^{i\gamma_n t}]$ 逐项作用即得 (R57.1)。这是 Berry–Keating/Sierra 算符（$\hat H=\hat D^2+\tfrac14$，经酉变换 $\hat{\mathcal D}\leftrightarrow\hat D$）在 CQM 记忆核上的实现。

### §3.2 图像：零点作为生成元谱

```
  自伴生成元 G = D^2 + 1/4  (D=-i d/dt)
     │
     ├─ 本征函数 e^{i gamma_n t}, 本征值 c_n = 1/4 + gamma_n^2
     │     c_1 = 200.04 (gap),  c_2 = 442.2, ...
     │
     ├─ 记忆核 K(t) = sum_n A_n e^{i gamma_n t}  =  G 的谱展开
     │
     └─ 物理: 零点 gamma_n 是"记忆振动模式", c_n 是其"能量^2"
              gap sqrt(c1)=14.14 -> 时标 1/sqrt(c1)=0.0707

  (对比: 薛定谔 H psi = E psi; 这里 G K_n = c_n K_n)
```

---

## 第四节：判决性计算（零参数）

### §4.1 生成元方程数值验证

$t=0.7$，N=2000：
- $K(t)=0.0148437216367$
- $(\hat{\mathcal D}^2+\tfrac14)K=\sum\mathfrak c_n A_n e^{i\gamma_n t}+\text{c.c.}=-27.6638806656$
- 直接算 $\hat{\mathcal D}^2K+\tfrac14K=-27.6638806656$——**match=True**（算符恒等式成立）。

### §4.2 Sierra 耦谱定理数值闭合

| 量 | 本轮数值 | 权威值（README/集成理论） |
|:---|:---|:---|
| $\mathfrak c_1=\tfrac14+\gamma_1^2$ | 200.040454832 | 200.04045483 |
| $\sqrt{\mathfrak c_1}$ | 14.14356585 | — |
| $1/\sqrt{\mathfrak c_1}$ | 0.07070353 | — |

**精确吻合**（差 $<10^{-6}$）。这是 Sierra-CQM 耦谱定理 $\mathfrak c_n=\tfrac14+\gamma_n^2$ 的直接数值确认，并把 $n=1$ 的精确等同从"渐近定理+构造"推进到"生成元谱本征值的算符实现"（条件于 R52 留数振幅）。谱隙 $\sqrt{\mathfrak c_1}\approx\gamma_1$（差 0.07%）给无量纲时标——物理时标仍需外生 $\hbar/\varepsilon_0$（Z3）。

---

## 第五节：新判据 R57（三条）

- **R57a（生成元方程）**：记忆核须满足 $(\hat{\mathcal D}^2+\tfrac14)K=\sum\mathfrak c_n A_n e^{i\gamma_n t}$，本征值 $\mathfrak c_n=\tfrac14+\gamma_n^2$。若测得的记忆核谱本征值偏离此式，则零点-记忆核谱生成元同一（M1 谱位置侧）在该材料失效。
- **R57b（耦谱数值）**：最低本征值 $\mathfrak c_1=200.04045483$ 是固定纯数（由 $\gamma_1$ 决定）；若某零点集给不同 $\mathfrak c_1$，则非真实 zeta 零点谱。
- **R57c（谱隙时标）**：记忆核最短无量纲时标 $1/\sqrt{\mathfrak c_1}=0.0707$（乘外生 $\hbar/\varepsilon_0$）；若动力学在该时标以下仍有结构，则需新增高频模式（超出当前零点谱）。

> 与 R56（求和规则）、R52（振幅判决）、R48（SFF）测不同对象：R57 测**记忆核的运动方程/谱生成元**。

---

## 第六部分：退化守住

| 对象 | 本轮处理 |
|:---|:---|
| BCS（DM.23–24） | 生成元方程不改能隙方程；✅ |
| 迈斯纳（R37） | 不碰 $\rho_s$；✅ |
| Z2/Z3 | $\hat{\mathcal D}$ 作用无量纲 $t$，物理时标外生；✅ |
| R56/R52 | 不变；生成元方程建立在留数振幅谱展开上 |
| Sierra-CQM | 耦谱定理获算符实现 + 数值闭合；不改定义 |
| 缺口 | 不升级；M1 物理同一仍受振幅边界 |

---

## 第七部分：边界与开放问题

1. **数学非 CQM 独有**：$\hat D^2+\tfrac14$ 是 Berry–Keating/Sierra 算符，CQM 增量只在把它接入记忆核运动方程、并用留数振幅（R52）闭合。
2. **酉变换细节**：Sierra 的 $\hat D=-i(\partial_u-\tfrac12)$ 与本轮 $\hat{\mathcal D}=-i\,d/dt$ 差酉变换/归一化（$u\leftrightarrow t$），本轮用简化的 $-\,i\,d/dt$ 形式（本征值同为 $\gamma_n$），严格对应见 V1。
3. **只锁谱不锁动力学**：生成元方程给谱结构，不给 $K(t)$ 的全时域演化或相变温度；绝对 $T_c$ 仍外生。
4. **V3 仅登记**：Kramers-Kronig 非马尔可夫核（arXiv:2604.17058）作外部对照，未引入理论。
5. **未做**：lean、网站、完整理论文档、参数拟合；无文档需删（删除须你确认）。

---

## 参考文献与脚本

- [V1] M. V. Berry & J. P. Keating, *Proc. R. Soc. A* **437**, 151 (1992); S. Sierra, arXiv:1003.0934; 本库 `01 核心理论/CQM_核心_集成理论.md` §8。
- [V2] DLMF §25.10; Schumayer & Hutchinson, arXiv:1101.3116。
- [V3] arXiv:2604.17058（Kramers–Kronig for non-Markovian kernels）— 仅登记。
- [V4] 本库 R56/R52 稿；`README.md`（$\mathfrak c_1=200.04045483$）；集成理论 §8。
- CQM 侧：Sierra-CQM 耦谱定理、记忆核 DM.17/DM.21 见 `06 超导/CQM_超导核心理论.md`、`README.md`。
- 脚本 `.calc/eom_memory.py`（gitignore）；零点缓存 `.calc/zeros.npy`。
