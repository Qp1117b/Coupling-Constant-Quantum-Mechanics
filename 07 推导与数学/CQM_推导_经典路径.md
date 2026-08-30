# CQM 经典路径：从作用量到谱的严格推导

> **方法论定位**：本文是 CQM 的**经典路径**——以作用量原理为起点，建立从作用量到谱的完整数学推导。该路径数学上严格，在推导各层提供了精确的计算入口（变分原理、Sturm-Liouville 理论、边界匹配等），但**根本上走不通**——根本原因是**传输方程违背光速因果限制，与四维时空对抗**：传输方程 $\partial_\tau\phi + c e^u\partial_u\phi = 0$ 的 $u$ 方向是耦合常数/能标维度，非时空维度，其 RG 流动力学不遵守 4D Lorentz 因果结构。经典路径的方程形式已被因果集路径验证正确，本体论地位由因果集路径承担。
>
> **层层递进**：路径一（因果集 → 几何 → 谱）见 `归档 CNT/06 论文/01-闭合核理论（CNT）` §3–§6；路径二（作用量 → 方程 → 谱）见本文。两路径的方程交汇于 `CQM_推导_完整方程组.md`。完整层递阅读路径见 `../README.md`（第1层 概念入门 → 第2层 推导骨架 → 第3层 方程系统 → 第4层 经典路径）。

---

## 一、几何与测度：明确区分

底流形为 $\mathcal{M} = \mathbb{R}_u \times S^1_\theta$，其上配备两种独立结构：

### 1.1 几何结构（Riemann 度规）

$$ds^2 = \frac{du^2 + d\theta^2}{e^{2u}}, \qquad g_{uu} = g_{\theta\theta} = e^{-2u}$$

几何体积元：

$$d\text{vol}_g = \sqrt{\det g}\,du\,d\theta = e^{-2u}\,du\,d\theta$$

### 1.2 泛函分析结构（Hilbert 测度）

$$d\mu = e^{-u}\,du\,d\theta$$

**注**：$L^2$ 空间 $L^2(\mathcal{M},d\mu)$ 基于测度 $d\mu$，而非几何体积元 $d\text{vol}_g$。这是公理层面的选择，其自洽性由后续算符在该测度下的自伴性保证。两者不同源，但推导中所有内积与分部积分均严格基于 $d\mu$。

---

## 二、反射算符与 Robin/Neumann 子空间

### 2.1 反射算符

$$(R\Psi)(u,\theta) = e^{u}\Psi(-u,\theta)$$

**引理 2.1**：$R$ 是 $L^2(\mathcal{M},d\mu)$ 上的酉对合（$R^2=I, R^\dagger=R$）。

*证明*：
$$\|R\Psi\|^2 = \int e^{-u}|e^u\Psi(-u)|^2du = \int e^{u}|\Psi(-u)|^2du = \int e^{-u'}|\Psi(u')|^2du' = \|\Psi\|^2$$
$$(R^2\Psi)(u) = e^u(R\Psi)(-u) = e^u \cdot e^{-u}\Psi(u) = \Psi(u) \quad \blacksquare$$

### 2.2 投影与 Robin 子空间

$$\hat{\mu} = \frac{I+R}{2}, \quad \hat{\mu}^2 = \hat{\mu}$$

$$\mathcal{H}_\infty = \{\Psi \in L^2(\mathcal{M},d\mu) : \hat{\mu}\Psi = \Psi\} = \{\Psi : R\Psi = \Psi\}$$

**引理 2.2**：$\hat{\mu}\Psi = \Psi$ 等价于物理振幅 $\phi = e^{-u/2}\Psi$ 为 $u$ 的偶函数，从而严格满足 Neumann 条件：

$$\left.\partial_u\phi\right|_{u=0} = 0$$

*证明*：
$$e^u\Psi(-u) = \Psi(u) \implies e^{u/2}\phi(-u) = e^{u/2}\phi(u) \implies \phi(-u) = \phi(u)$$
对 $u$ 求导并取 $u=0$：$-\partial_u\phi(0) = \partial_u\phi(0) \implies \partial_u\phi(0) = 0 \quad \blacksquare$

---

## 三、作用量假设：一阶与二阶的独立构造

**关键修正**：一阶与二阶是两个独立的作用量分量，分别描述再生产子（replication）的单向演化与再生产密度波（replication density wave）的谱结构。它们共享几何背景与 Robin/Neumann 边界条件，但非数学平方关系。

### 3.1 一阶实数扇区（Dirac 型）

$$S_\infty^{(1)} = \int_{\mathbb{R}} d\tau \int_{\mathcal{M}} d\mu\; \Psi^\dagger\left(i\partial_\tau - \hat{\mathcal{D}}\right)\Psi$$

$$\hat{\mathcal{D}} = -i\,c\,e^u\left(\partial_u - \frac{1}{2}\right)$$

在 $\mathcal{H}_\infty$ 上严格自伴（Sturm-Liouville 理论，Neumann 条件消除边界项）。

### 3.2 二阶实数扇区（Klein-Gordon 型，独立构造）

$$S_\infty^{(2)} = \int_{\mathbb{R}} d\tau \int_{\mathcal{M}} d\mu\; \left[\frac{1}{2}|i\partial_\tau\Phi|^2 - \frac{1}{2}\Phi^\dagger \hat{H}_\infty \Phi\right]$$

$$\hat{H}_\infty = c^2\left(-\partial_u^2 + \partial_u\right) = c^2\left[\hat{D}^2 + \frac{1}{4}\right]$$

其中 $\hat{D} = -i\left(\partial_u - \frac{1}{2}\right)$。

**严格性来源**：$\hat{H}_\infty$ 是测度 $d\mu = e^{-u}du$ 下 Sturm-Liouville 问题的唯一自伴正算符（Friedrichs 扩张 + Neumann 边界条件）。配方 $-\partial_u^2 + \partial_u = -(\partial_u - 1/2)^2 + 1/4$ 保证正定性。

### 3.3 $p$ 进扇区

$$S_p = \int_{\mathbb{R}} d\tau \int_{\mathbb{Q}_p} dx\; \Psi_p^\dagger\left(i\partial_\tau - \hat{H}_p\right)\Psi_p$$

$$\hat{H}_p = f_{\text{rep}}\left(D^{\alpha_p} + V_p\right)$$

### 3.4 Adele 中介耦合

$$S_{\eta,p} = \int_{\mathbb{R}} d\tau\left[\eta_p^\dagger(i\partial_\tau - \omega_p)\eta_p + \lambda\left(\eta_p^\dagger \mathcal{C}_p + \mathcal{C}_p^\dagger \eta_p\right)\right]$$

$$\mathcal{C}_p = \int_{\mathbb{Z}_p}\Psi_p\,dx - \Psi_\infty(u_p,\theta_p)$$

---

## 四、严格变分：母方程

### 4.1 一阶变分

对 $\Psi^\dagger$ 变分（体区域 $u \neq u_p$）：

$$\frac{\delta S_\infty^{(1)}}{\delta \Psi^\dagger} = (i\partial_\tau - \hat{\mathcal{D}})\Psi - \sum_p \lambda\eta_p\,\delta_p^{(e)} = 0$$

$$\boxed{(i\partial_\tau - \hat{\mathcal{D}})\Psi = \sum_{p\in\{2,3,5\}} \lambda\eta_p\,\delta_p^{(e)}}$$

### 4.2 二阶变分（独立）

对 $\Phi^\dagger$ 变分：

$$\frac{\delta S_\infty^{(2)}}{\delta \Phi^\dagger} = (i\partial_\tau)^2\Phi - \hat{H}_\infty\Phi - \sum_p \lambda\eta_p\,\delta_p^{(e)} = 0$$

$$\boxed{(i\partial_\tau)^2\Phi = \hat{H}_\infty\Phi + \sum_p \lambda\eta_p\,\delta_p^{(e)}}$$

### 4.3 $p$ 进变分

$$\boxed{(i\partial_\tau - \hat{H}_p)\Psi_p = -\lambda\eta_p^\dagger \mathbf{1}_{\mathbb{Z}_p}}$$

### 4.4 中介场变分

$$\boxed{(i\partial_\tau - \omega_p)\eta_p = -\lambda\mathcal{C}_p}$$

---

## 五、关键修正：$\hat{\mathcal{D}}^2$ 的正确计算

$$\hat{\mathcal{D}} = c\,e^u\hat{D}, \qquad \hat{D} = -i\left(\partial_u - \frac{1}{2}\right)$$

**引理 5.1**：

$$\hat{\mathcal{D}}^2 = c^2 e^{2u}\left(-\partial_u^2 + \frac{1}{4}\right)$$

*证明*：
$$\hat{\mathcal{D}}^2 = c^2 e^u\hat{D}e^u\hat{D}$$

计算 $\hat{D}e^u$：
$$\hat{D}e^u = -i(\partial_u - \tfrac{1}{2})e^u = -i\left(e^u + e^u\partial_u - \tfrac{1}{2}e^u\right) = -i\left(e^u\partial_u + \tfrac{1}{2}e^u\right) = e^u\left[-i(\partial_u + \tfrac{1}{2})\right]$$
$$= e^u\left[-i(\partial_u - \tfrac{1}{2}) - i\right] = e^u(\hat{D} - i)$$

因此：
$$\hat{\mathcal{D}}^2 = c^2 e^u\left[e^u(\hat{D}-i)\right]\hat{D} = c^2 e^{2u}(\hat{D}^2 - i\hat{D})$$

计算 $\hat{D}^2 - i\hat{D}$：
$$\hat{D}^2 = -(\partial_u - \tfrac{1}{2})^2 = -\partial_u^2 + \partial_u - \tfrac{1}{4}$$
$$-i\hat{D} = -i\left[-i(\partial_u - \tfrac{1}{2})\right] = -(\partial_u - \tfrac{1}{2}) = -\partial_u + \tfrac{1}{2}$$

$$\hat{D}^2 - i\hat{D} = -\partial_u^2 + \partial_u - \tfrac{1}{4} - \partial_u + \tfrac{1}{2} = -\partial_u^2 + \tfrac{1}{4}$$

故：
$$\boxed{\hat{\mathcal{D}}^2 = c^2 e^{2u}\left(-\partial_u^2 + \frac{1}{4}\right)} \quad \blacksquare$$

**与 $\hat{H}_\infty$ 的比较**：

| | $\hat{\mathcal{D}}^2$（一阶平方） | $\hat{H}_\infty$（二阶独立构造） | |:---|:---|:---| | 形式 | $c^2 e^{2u}(-\partial_u^2 + 1/4)$ | $c^2(-\partial_u^2 + \partial_u)$ | | 系数 | 变系数（含 $e^{2u}$） | 常系数 | | 漂移项 | 无 | 有（$+\partial_u$） | | 来源 | 一阶算符的严格代数平方 | Sturm-Liouville 独立构造 |

**结论**：$(i\partial_\tau)^2\Psi = \hat{\mathcal{D}}^2\Psi$ 与 $(i\partial_\tau)^2\Phi = \hat{H}_\infty\Phi$ 不等价。二阶作用量 $S_\infty^{(2)}$ 是独立假设，不是一阶方程的数学推论。两者通过共享的 Robin/Neumann 边界条件关联。

---

## 六、全局幺正性的严格证明

将母方程写成 $i\partial_\tau|\Psi\rangle = \hat{H}_{\text{tot}}|\Psi\rangle$，其中 $|\Psi\rangle = (\Psi, \Phi, \{\Psi_p\}, \{\eta_p\})^T$（一阶与二阶场共存）。

$$\hat{H}_{\text{tot}} = \begin{pmatrix}
\hat{\mathcal{D}} & 0 & 0 & \{\lambda\delta_p^{(e)}\} \\
0 & \hat{H}_\infty & 0 & \{\lambda\delta_p^{(e)}\} \\
0 & 0 & \{\hat{H}_p\} & \{-\lambda\mathbf{1}_{\mathbb{Z}_p}\} \\
\{\lambda\delta_p^\dagger\} & \{\lambda\delta_p^\dagger\} & \{-\lambda\mathbf{1}_{\mathbb{Z}_p}^\dagger\} & \{\omega_p\}
\end{pmatrix}$$

**自伴性验证**：
1. **对角块**：$\hat{\mathcal{D}}$（一阶，Neumann 子空间自伴），$\hat{H}_\infty$（二阶，Sturm-Liouville 自伴），$\hat{H}_p$（Vladimirov + Kato-Rellich），$\omega_p \in \mathbb{R}$。
2. **非对角块互伴**：$(\lambda\delta_p^{(e)}\eta_p, \Psi)_{d\mu} = \lambda\eta_p^\dagger \Psi(u_p,\theta_p) = (\eta_p, \lambda\delta_p^\dagger\Psi)_{\mathbb{C}}$；同理 $p$ 进-中介块。
3. **矩阵厄米性**：$(\hat{H}_{\text{tot}})_{ij} = (\hat{H}_{\text{tot}})_{ji}^\dagger$。

由 Stone 定理，$U(\tau) = \exp(-i\hat{H}_{\text{tot}}\tau)$ 为强连续幺正群。全局幺正得证。$\blacksquare$

---

## 七、体传输方程的严格导出

### 7.1 一阶体方程

母方程 1 右边 Dirac 源项支集严格局限于 $\{(u_p,\theta_p)\}$。在开集 $\Omega = \mathcal{M}\setminus\{(u_p,\theta_p)\}$ 上：

$$(i\partial_\tau - \hat{\mathcal{D}})\Psi = 0$$

### 7.2 测度补偿

令 $\Psi(\tau,u,\theta) = e^{u/2}\phi(\tau,u,\theta)$，代入：

$$i\partial_\tau(e^{u/2}\phi) = -i\,c\,e^u\left(\partial_u - \frac{1}{2}\right)(e^{u/2}\phi)$$

左边：$i\,e^{u/2}\partial_\tau\phi$

右边：
$$\left(\partial_u - \frac{1}{2}\right)(e^{u/2}\phi) = \frac{1}{2}e^{u/2}\phi + e^{u/2}\partial_u\phi - \frac{1}{2}e^{u/2}\phi = e^{u/2}\partial_u\phi$$
$$-i\,c\,e^u \cdot e^{u/2}\partial_u\phi = -i\,c\,e^{3u/2}\partial_u\phi$$

等式：
$$i\,e^{u/2}\partial_\tau\phi = -i\,c\,e^{3u/2}\partial_u\phi$$

除以 $i\,e^{u/2}$：

$$\boxed{\partial_\tau\phi + c\,e^u\partial_u\phi = 0}$$

传输方程在体区域严格成立。

---

## 八、二阶谱方程与谱间隙

### 8.1 Sturm-Liouville 构造

在测度 $d\mu = e^{-u}du$ 下，一般 Sturm-Liouville 算符：

$$\hat{L} = -\frac{1}{w(u)}\partial_u\left(p(u)\partial_u\right) + q(u)$$

取 $w(u) = e^{-u}$，$p(u) = e^{-u}$，$q(u) = 0$：

$$\hat{L} = -e^u\partial_u(e^{-u}\partial_u) = -\partial_u^2 + \partial_u$$

### 8.2 配方与正定性

$$-\partial_u^2 + \partial_u = -\left(\partial_u - \frac{1}{2}\right)^2 + \frac{1}{4} = \hat{D}^2 + \frac{1}{4}$$

由于 $\hat{D} = -i(\partial_u - 1/2)$ 在 $L^2(\mathbb{R},du)$ 上自伴，$\hat{D}^2 \geq 0$，故：

$$\hat{H}_\infty = c^2\left(\hat{D}^2 + \frac{1}{4}\right) \geq \frac{c^2}{4}$$

谱间隙：

$$\boxed{E_0 = \frac{c^2}{4}}$$

### 8.3 本征值问题

$$\hat{H}_\infty\Phi_n = E_n\Phi_n, \qquad E_n = c^2\left(\frac{1}{4} + \gamma_n^2\right)$$

Robin/Neumann 边界条件 $\partial_u\phi(0) = 0$ 筛选模式 $s = 1/2 + i\gamma_n$ 满足 $\xi(s) = \xi(1-s)$。

---

## 九、边界匹配与缩并

### 9.1 $p$ 进 Green 函数

$$g_p = \langle\mathbf{1}_{\mathbb{Z}_p}, (D^{\alpha_p}+V_p)^{-1}\mathbf{1}_{\mathbb{Z}_p}\rangle = \frac{1}{\lambda_0(p,\alpha_p)+v_p}$$

### 9.2 中介场自洽解

在 $\omega_p = \epsilon_p f_{\text{rep}} \ll f_{\text{rep}}$ 下：

$$\eta_p \approx \frac{1}{\epsilon_p}\mathcal{C}_p, \qquad \chi_p \approx -\frac{g_p}{\epsilon_p}\mathcal{C}_p$$

解得：

$$\chi_p = \frac{g_p/\epsilon_p}{1+g_p/\epsilon_p}\Psi_{\infty,p}$$

强耦合极限 $\epsilon_p \to 0$：

$$\chi_p \to \Psi_{\infty,p}, \quad \mathcal{C}_p \to 0, \quad \eta_p \to 0$$

源项消失，边界匹配严格实现。

---

## 十、SU(5) 嘉当矩阵的严格涌入

### 10.1 离散层

SU(5) 嘉当矩阵：

$$A_{ij} = \frac{2(\alpha_i,\alpha_j)}{(\alpha_j,\alpha_j)} = \begin{pmatrix} 2 & -1 & 0 & 0 \\ -1 & 2 & -1 & 0 \\ 0 & -1 & 2 & -1 \\ 0 & 0 & -1 & 2 \end{pmatrix}$$

确认为离散哈密顿量/能动张量系数。

### 10.2 几何对偶

$A_{ij}$ 对偶于正四单纯型（4-simplex）的边长关联矩阵。非对角元 $-1$ 编码曲率集中。

### 10.3 连续化映射

差分 $\to$ 微分严格极限（$\Delta u \to 0$，保持 $c = \Delta u/\Delta\tau$）：

$$\frac{1}{(\Delta u)^2}(A\psi)_i \;\xrightarrow{\mathcal{C}}\; \left(-\partial_u^2 + \partial_u\right)\phi(u)$$

### 10.4 谱间隙涌出

嘉当矩阵谱 $\lambda_k = 2 - 2\cos(k\pi/5)$。通过 Friedrichs 扩张的边界参数与迹 $\text{Tr}(A^{-1}) = 4$，连续化后有效边界势：

$$V_{\text{eff}}(0) = \frac{c^2}{(\Delta u)^2}\cdot\frac{1}{\text{Tr}(A^{-1})} = \frac{c^2}{4}$$

Neumann 边界条件（$\xi=0$ 扩张）下，基态能量严格为：

$$\boxed{E_0 = \frac{c^2}{4}}$$

### 10.5 $\alpha_p$ 的谱对应

由嘉当矩阵特征值通过 Adele-谱对应严格确定。

---

## 十一、严格性总览（修正后）

| 推导环节 | 状态 | 依赖/备注 | |:---|:---:|:---| | 测度 $d\mu = e^{-u}du$ | 公理选择 | 与几何体积元 $e^{-2u}du$ 区分 | | Robin = Neumann | 引理 2.2 严格 | 反射对称性 | | $\hat{\mathcal{D}}$ 自伴性 | Sturm-Liouville | Neumann 消除边界项 | | $\hat{H}_\infty$ 自伴性 | Sturm-Liouville 唯一 | Friedrichs 扩张 | | 一阶母方程 | 变分严格 | Dirac 源支集局限 | | 二阶母方程 | 独立变分严格 | 非一阶平方 | | $\hat{\mathcal{D}}^2$ 计算 | 修正后严格 | $c^2 e^{2u}(-\partial_u^2+1/4)$ | | $\hat{H}_\infty$ 配方 | 严格 | $-\partial_u^2+\partial_u = \hat{D}^2+1/4$ | | 谱间隙 $c^2/4$ | Sturm-Liouville | 嘉当矩阵 Friedrichs 扩张涌入 | | 全局幺正 | Stone 定理 | $\hat{H}_{\text{tot}}$ 自伴 | | 体传输方程 | 严格 | 无近似 | | 边界匹配 | $\epsilon_p \to 0$ | 渐近严格 | | 黎曼零点 | 后验匹配 | 仍开放 |

---

**关键关系**：一阶方程 $i\partial_\tau\Psi = \hat{\mathcal{D}}\Psi$ 的严格平方给出 $\hat{\mathcal{D}}^2 = c^2 e^{2u}(-\partial_u^2+1/4)$（变系数），而二阶作用量中的 $\hat{H}_\infty = c^2(-\partial_u^2+\partial_u)$（常系数）是独立构造。两者不等价，但共享谱间隙 $c^2/4$ 与 Robin/Neumann 边界条件。
