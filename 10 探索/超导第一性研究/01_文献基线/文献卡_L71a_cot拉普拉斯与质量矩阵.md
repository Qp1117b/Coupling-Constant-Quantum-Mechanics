# 文献卡 L71a：cot 拉普拉斯是刚度矩阵，算子须除以质量矩阵

**检索日期**：2026-11-24
**对应环节**：环 2 `W-3`（$L$ 本征值与 $\omega_k^2$ 之间的量纲因子）

## 一、外部结论（逐条带出处）

| # | 结论 | 出处 |
|:--|:---|:---|
| 1 | 三角网格上的 cot 公式 $L_{ij}=-\tfrac12(\cot\alpha_{ij}+\cot\beta_{ij})$，$L_{ii}=-\sum_{j\ne i}L_{ij}$，来自线性元（hat 基函数）的**刚度**内积 $L_{ij}=-\langle\nabla\phi_i,\nabla\phi_j\rangle$ | Pinkall & Polthier, *Experiment. Math.* **2**(1), 15–36 (1993). DOI 10.1080/10586458.1993.10504266 |
| 2 | 离散 Laplace–Beltrami 必须写成 $\Delta u\approx M^{-1}Lu$（$M$ 为质量矩阵：Voronoi 或重心面积）；只有 $\Delta$ 的最小二乘表述 $\int_M(\nabla u)^2\approx-u^\top Lu$ 才可直接用 $L$ | Wardetzky, Mathur, Kälberer, Grinspun, *Discrete Laplace operators: no free lunch*, SGP 2007, 33–37. DOI 10.2312/SGP/SGP07/033-037 |
| 3 | 网格加密（最大边长 $h\to0$）时 $\mathcal L_c=\mathcal M^{-1}\mathfrak L$ 收敛到 Laplace–Beltrami；$\mathfrak L=d_0^\top\star_1 d_0$ 是共形拉普拉斯（DEC 的刚度） | Crane, de Goes, Desbrun, Schröder, *Digital geometry processing with discrete exterior calculus*, SIGGRAPH '13 Courses. DOI 10.1145/2504435.2504450；Hildebrandt, Polthier, Wardetzky, *Geom. Dedicata* **123**, 89–112 (2006). DOI 10.1007/s10711-006-9109-5 |
| 4 | 一般网格上不存在同时满足连续算子的全部性质的离散化（正权、对称、局部性等）；钝角三角形的 cot 权可为负 | Wardetzky et al. 2007（同上） |
| 5 | 若无质量矩阵归一，cot 矩阵的谱不收敛到连续谱；点态收敛需特殊网格，$L_2$ 收敛也不普遍成立 | Belkin, Sun, Wang, *Discrete Laplace operator on meshed surfaces*, SoCG 2008, 278–287. DOI 10.1145/1377676.1377725 |

## 二、可约束的链内环节

- **环 2 `W-3`**：06 §4 把 $L$ 的"本征值"直接读作 $\omega_k^2$ 的几何来源。由 #1–#3，$L$ 是**无量纲刚度**，其本征值无量纲；算子化必须除以节点测度。
- **环 3 (3.1)**：$\cot\theta$ 的权重结构不变，只是被重新解读为刚度而非算子。
- **环 12／13**：谱阶梯 $\{2\ln n\}$ 与 $\{\gamma_n\}$ 只在"$\omega_k$ 已定义"之后才有意义，故本卡不触及。

## 三、不可越界（红线）

1. 上述结论是**外部标准工具**，不是 CQM 结论；本卡只用 #1–#3 的"刚度／测度"分解，不引入收敛性定理作物理假设。
2. #4 的"no free lunch"是**负面结论**：不得据此声称 CQM 的 $L$ 有唯一离散化；CQM 只用 06 已定的 cot 权重。
3. 不引入外部对 $\omega_D$、声速的数值，只引入结构关系（见 L71b）。

## 四、不能推出

不能由本卡推出 CQM 的 $K$（纯数）取值，也不能推出 $L$ 的谱在真实晶体上收敛——这两件都要在链内按格型单独算。
