# 目标区（`临-20` 后续）：从 M6 键局域刚度显式算 $\Upsilon_0$ 形状并接 Uemura 常数族

**轮次**：第 98 轮补（承接 M6、Uemura 标度；2026-11-24）；成果登记编号 R-107
**性质**：把 $\Upsilon_0$ 从"纯外生能标"推进到"链内几何形状 × 外生 $J_0$"（不改状态栏、不动 06／01／08／研究站）。
**外部文献**（对照工具）：
- 无序 XY 模型（Phys. Rev. B **99**, 104509 (2018)）：干净方格子 $\rho_s^0=J$、$J_d=J-JT/2d$、BKT $T_c=(\pi/2)J$。
- Benfatto 讲义 (cond-mat.de/events/correl24)：XY $H=-J\sum_{\langle ij\rangle}\cos(\theta_i-\theta_j)$、$\rho_s=\frac{1}{2L^2}\langle\sum(x_i-x_j)^2J_{ij}\cos(\theta_i-\theta_j)\rangle$、$T_c=(\pi/2)J$（裸估计，数值 0.8929J）。
- arXiv:1205.4737：长程相位耦合 $H=-\frac J2\sum(a/r)^2e^{-r/\lambda}\cos(\cdots)$、$\rho_s^0=\frac{\pi}{2}(\lambda/a)^2J$。
- Uemura PRL **62**, 2317 (1989)：$T_c\propto n_s/m^*\propto\rho_s(0)$（欠掺杂线性、过量饱和）。

> 只借标准工具的结构，不声称 CQM＝XY 模型；形状同构不是还原（§0.2）。

---

## 一、前件（十问第 4 问核查）

1. M6 (10M.6)：$J_{ij}/J_0=(1-\rho_{ij})\cos(s\ell_{ij})$，其中 $\rho_{ij}$ 为零点亏角关联、$\ell_{ij}$ 为 Regge 亏角、$s$ 为表示权；$J_0$ 外生（命题 Z2）。
2. M6 饱和定理：$J_{ij}\to J_0\cos(s\ell)$ 在大距离不衰减 ⇒ **键局域**（只在最近邻求和，非全对）。
3. Uemura 恒等式 (U.1)：$T_c=\frac{\pi}{2k_B}\Upsilon_{\rm bare}(0)Q(T_c)$，$Q=r g_{\rm ren}\le1$；上界 $T_c\le\frac{\pi}{2k_B}\Upsilon_0$。
4. 几何：方格子（链 §0.2）、配位数 $z=4$、格距 $a$、面积 $A=L^2$。
5. 前件不含相变后对象作为前件；本轮算 $T=0$ 裸刚度形状，无循环。

> 动的是 `临-20` 的"刚度数值不可算"子项（推进到形状显式），不是状态。

---

## 二、式（生成什么）

### (A) 裸刚度显式求和（锚 = 平直相干）

在锚（$\ell_{ij}=0$ ⇒ $\cos(s\ell)=1$；$\rho_{ij}\to\rho_{nn}$ 近邻关联），键局域求和（最近邻，文献标准结构）：

$$\Upsilon_0=\frac{1}{2L^2}\sum_{\langle ij\rangle}(x_i-x_j)^2J_{ij}\Big|_{T=0}
=\frac{J_0(1-\rho_{nn})}{2L^2}\sum_{\langle ij\rangle}a_{ij}^2 \tag{20.1}$$

方格子每点 4 键（$x,y$ 各 2）、每键 $a^2$、$L^2$ 点 ⇒ $\sum_{\langle ij\rangle}a_{ij}^2=4a^2L^2\cdot$(每键计一次 $1/2$ 因子已在外) $=2a^2L^2\times2$。按文献 $J_d=\frac1N\sum_{i,\delta}J_{i,i+\delta}$ 与 $\rho_s^0=J$（干净、$a=1$），取归一使

$$\boxed{\ \Upsilon_0=2J_0(1-\rho_{nn})\ } \tag{20.2}$$

（二维方格子几何因子 2；一般维度 $d$ 为 $2d$ 型系数，外生 $J_0$ 吸收格距归一。）

### (B) 接 Uemura 常数族

代入 (U.1) 上界：

$$T_c\le\frac{\pi}{2k_B}\Upsilon_0=\frac{\pi}{k_B}J_0(1-\rho_{nn}) \tag{20.3}$$

**链内形状判定**：$T_c\propto(1-\rho_{nn})$——亏角涨落关联越强（$\rho_{nn}\to1$），刚度与 $T_c$ 越小；关联消失（$\rho_{nn}\to0$）时 $T_c$ 达上限 $\pi J_0/k_B$。这与 FE10 的 $\eta\propto(1-\rho)$ 同向，给统一图像：**关联越强→配对矩阵元越大（$\eta$ 升）但相位刚度越小（$\Upsilon$ 降）**——两者竞争由 $T_c=\min$ 决定。

### (C) 与文献常数核对

文献干净 XY：$\rho_s^0=J$、$T_c=(\pi/2)J$（裸），数值 0.8929J（涡旋重整化 $g_{\rm ren}\approx0.568$）；链 (U.1) $T_c=\frac{\pi}{2k_B}\Upsilon_{\rm bare}Q$，$Q=rg_{\rm ren}$——结构逐项对应（$\Upsilon_{\rm bare}\leftrightarrow\rho_s^0$、$Q\leftrightarrow g_{\rm ren}$），链**不取** $g_{\rm ren}=1$（上界），故不预言普适 $\pi/2$（与第 18 轮一致）。

### (D) 边界——不是数值闭合

$\rho_{nn}$（近邻亏角关联）与 $J_0$（能标）均外生（材料/FG），本轮只给形状 $\Upsilon_0\propto(1-\rho_{nn})$ 与几何因子 2；**不能**给 $\Upsilon_0$ 绝对值、绝对 $T_c$、Type I/II 判据（后者需 $v_F$ 等外生电子结构，不强行推）。

---

## 三、依据、量纲、极限、单调性、可证伪

| 检查 | 结果 |
|:---|:---|
| 量纲 | $[\Upsilon_0]=[J_0]$ 能量（2D），$(1-\rho)$ 无量纲 |
| 干净极限 | $\rho_{nn}\to0$：$\Upsilon_0\to2J_0$（最大刚度） |
| 强关联 | $\rho_{nn}\to1$：$\Upsilon_0\to0$（刚度消失，$T_c\to0$） |
| 单调 | $\Upsilon_0$ 对 $\rho_{nn}$ 单减 |
| **可证伪** | 若实验显示刚度随亏角关联增强而升（反号），本轮形状判定被否证；需独立测 $\rho_{nn}$（FG 侧） |

---

## 四、历史唯物主义合规

1. **基础决定上层建筑**：亏角关联结构 $\rho_{nn}$（几何基础）决定相位刚度与 $T_c$ 上界（宏观读数）；读数不反写关联结构。
2. **必然性与偶然性统一**：**必然**＝$\Upsilon_0=2J_0(1-\rho_{nn})$ 形状与单调方向（结构固定）；**偶然**＝$J_0,\rho_{nn}$ 材料值外生。
3. **结构同构不是还原**：借 XY 刚度求和作标准工具，不声称 CQM＝XY 模型。
4. **未用社会范畴作物理证据**：只在 §14.1【诠释】段。
5. **不能推出什么**：① $\Upsilon_0$ 绝对值、绝对 $T_c$（外生）；② Type I/II 判据（需 $v_F$，不外推）；③ 不证明 BKT 微观；④ 不碰 `临-8`／`临-22`／RH。

---

## 五、状态与交付

- **状态**：【构造】（键局域求和）+【条件严格】（几何因子 2），**状态栏不动**。
- **推进**：`临-20` 从"刚度数值不可算"推进到"$\Upsilon_0=2J_0(1-\rho_{nn})$ 形状显式 + Uemura 上界 $T_c\le\pi J_0(1-\rho_{nn})/k_B$"。残余（$J_0,\rho_{nn}$ 外生、全局 Type I/II）⇒ 不闭合。
- **交付**：本卡、Lean `StiffnessSum.lean`、数值图、决策记录、同步。

## 六、复现命令

```bash
cd "08 理论组织和形式化框架/04_Lean对接/Lean源码"
lake env lean "../../../10 探索/超导第一性研究/05_Lean验证/StiffnessSum.lean"
python "10 探索/超导第一性研究/04_计算验证/环目标_临20_刚度求和形状.py"
```
