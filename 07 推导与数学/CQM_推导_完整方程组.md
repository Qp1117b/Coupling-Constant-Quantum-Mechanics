# CQM 完整方程组

> **方法论定位**：本文方程是两条独立路径的交汇点，路径无关。
>
> **经典路径（提供计算入口）**：以**作用量原理**为起点（`CQM_推导_经典路径.md`），建立一阶/二阶作用量 → 母方程 → 传输方程 → 谱结构的完整数学推导。该路径数学上严格，在推导各层提供了精确的计算入口（变分原理、Sturm-Liouville 理论、边界匹配等），但作用量是特设假设，没有第一性原理可以"推导出"作用量形式或维度提升。经典路径的方程形式在因果集路径中以不同本体论地位重新出现：不再是假设，而是从因果集结构导出的数学必然。经典路径因此贡献推导的**数学骨架与计算入口**，本体论地位由因果集路径承担。
>
> **因果集路径（唯一可行）**：以**因果集**为底层本体论（公理 I，`归档 CNT/06 论文/01-闭合核理论（CNT）` §3）——**量子引力属于因果叠加状态，因此适合因果集描述**。Sprinkling 过程严格涌现 $\mathbb{H}^2$ 几何，$\mathbb{H}^2$ 的 Laplacian 谱给出与经典路径全同的方程结构。该路径是唯一自洽的本体论路径——"从因果集到几何"的涌出替代了"假设作用量"，为方程提供了"从何而来"的终极回答。经典路径仅在该路径验证后才知其方程形式正确，但经典路径自身无法独立确立。
>
> **两路径关系**：经典路径提供方程形式与计算入口（数学上严格），因果集路径提供本体论根基（唯一自洽）。方程系统形式不变，是两路径的共同交汇点——但唯因果集路径能从第一性原理到达此交汇点。完整层递阅读路径见 `README.md`。
> >
>
> **符号约定**：$L^2$ 空间基于 Hilbert 测度 $d\mu = e^{-u}du\,d\theta$，**非**几何体积元 $d\text{vol}_g = e^{-2u}du\,d\theta$（详见 `CQM_推导_经典路径.md` §1）。仅一个实验输入：$m_p$。

---

## 〇、因果集：底层本体论

> 以下公理与方程来自因果集路径（`归档 CNT/06 论文/01-闭合核理论（CNT）` §3–§6），是 CQM 方程系统**唯一自洽的本体论源头**。经典路径的方程形式与此处的数学结构全同，但因果集路径为方程提供了"从何而来"的终极回答。

### 0.1 因果集公理

$$\boxed{\text{物理实在由因果集 } C = (X, \prec) \text{ 构成}} \tag{CS0}$$

$$x, y, z \in X, \qquad \prec \subseteq X \times X \tag{CS1}$$

$$\neg(x \prec x) \quad \text{(无自环)} \tag{CS2}$$

$$x \prec y \prec z \wedge x \neq z \implies x \prec z \quad \text{(传递性)} \tag{CS3}$$

$$x \prec y \wedge y \prec x \implies x = y \quad \text{(反对称)} \tag{CS4}$$

### 0.2 Sprinkling 测度

因果集通过泊松 Sprinkling 嵌入连续几何，密度 $\rho = l^{-d}$（$l$ 为基本长度，$d$ 为壳层维度）：

$$d\mu_{\text{spr}} = \rho\,dv, \qquad v = e^{-u} \tag{CS5}$$

$$d\mu_{\text{spr}} = \rho\,e^{-u}du \;\longrightarrow\; \boxed{d\mu = e^{-u}du} \tag{CS6}$$

吸收常数 $\rho$ 入定义后，$d\mu$ 即为下游所有内积与变分的 Hilbert 测度（定理 3.1, `归档 CNT/06 论文/01-闭合核理论（CNT）`）。

### 0.3 基本动力学

$$x \prec y \implies \text{激发从 } x \text{ 传播到 } y \tag{CS7}$$

$$x \nprec y \implies \text{传播被禁止} \tag{CS8}$$

### 0.4 涌现的测度与反射对称

Sprinkling 的均匀性在 $u$ 坐标中给出测度 $d\mu = e^{-u}du$，该测度天然支持反射对称性：

$$(R\Psi)(u) = e^{u}\Psi(-u), \qquad R^2 = I, \; R^\dagger = R \tag{CS9}$$

$$\hat{\mu} = \frac{I+R}{2}, \qquad \hat{\mu}^2 = \hat{\mu} \tag{CS10}$$

$\hat{\mu}\Psi = \Psi$ 定义物理子空间 $\mathcal{H}_\infty$，等价于物理振幅 $\phi = e^{-u/2}\Psi$ 满足 Neumann 条件 $\partial_u\phi(0)=0$（Robin = Neumann 引理）。

### 0.5 $\mathbb{H}^2$ 谱几何

Sprinkling 的连续极限涌现 Poincaré 半平面 $\mathbb{H}^2$：

$$ds^2 = \frac{du^2 + d\theta^2}{e^{2u}} \tag{CS11}$$

$\mathbb{H}^2$ 的 Laplace-Beltrami 算符 $\Delta_{\mathbb{H}^2} = -e^{2u}(\partial_u^2 + \partial_\theta^2)$ 在测度 $d\mu$ 下经 $\hat{\mu}$ 筛选后退化为：

$$\hat{H}_\infty = c^2\left(-\partial_u^2 + \partial_u\right) = c^2\left[\hat{D}^2 + \frac{1}{4}\right] \tag{CS12}$$

谱结构 $E_n = c^2(1/4 + \gamma_n^2)$ 直接从 $\mathbb{H}^2$ 的几何涌出（详见 §七）。

**状态**：CS0–CS4 公理；CS5–CS6 定理（`归档 CNT/06 论文/01-闭合核理论（CNT）` 定理 3.1）；CS7–CS8 公理；CS9–CS10 构造；CS11–CS12 严格极限

---

## 一、几何与 Hilbert 空间

### 1.1 底流形与测度

$$\mathcal{M} = \mathbb{R}_u \times S^1_\theta, \quad ds^2 = \frac{du^2 + d\theta^2}{e^{2u}}, \quad d\mu = e^{-u}du\,d\theta$$

### 1.2 反射算符与 $\mathcal{H}_\infty$

$$(R\Psi)(u,\theta) = e^{u}\Psi(-u,\theta), \qquad R^2 = I, \; R^\dagger = R$$

$$\hat{\mu} = \frac{I+R}{2}, \quad \hat{\mu}^2 = \hat{\mu}$$

$$\mathcal{H}_\infty = \{\Psi \in L^2(\mathcal{M},d\mu) : \hat{\mu}\Psi = \Psi\}$$

**引理**（Robin = Neumann）：$\hat{\mu}\Psi = \Psi \iff \phi(u)=e^{-u/2}\Psi(u)$ 为偶函数 $\iff \partial_u\phi(0)=0$。

### 1.3 $p$ 进扇区

$$\mathcal{H}_p = L^2(\mathbb{Q}_p, dx), \qquad \hat{H}_p = f_{\text{rep}}(D^{\alpha_p}+V_p)$$

**状态**：$\mathcal{H}_\infty$ 构造性（$R$ 酉对合，$\hat{\mu}$ 投影）；$\mathcal{H}_p$ 标准

---

## 二、作用量（独立构造，经典路径）

> **经典路径**：以下四个作用量泛函是经典路径的核心假设。数学推导严格，但"为何取此形式"需因果集路径回答。详见 `CQM_推导_经典路径.md`。

### 2.1 一阶实数扇区（Dirac 型，再生产子演化）

$$S_\infty^{(1)} = \int_{\mathbb{R}} d\tau \int_{\mathcal{M}} d\mu\; \Psi^\dagger\left(i\partial_\tau - \hat{\mathcal{D}}\right)\Psi$$

$$\hat{\mathcal{D}} = -i\,c\,e^u\left(\partial_u - \frac{1}{2}\right)$$

在 $\mathcal{H}_\infty$ 上严格自伴（Sturm-Liouville + Neumann）。

### 2.2 二阶实数扇区（Klein-Gordon 型，谱结构）

$$S_\infty^{(2)} = \int_{\mathbb{R}} d\tau \int_{\mathcal{M}} d\mu\; \left[\frac{1}{2}|i\partial_\tau\Phi|^2 - \frac{1}{2}\Phi^\dagger \hat{H}_\infty \Phi\right]$$

$$\hat{H}_\infty = c^2\left(-\partial_u^2 + \partial_u\right) = c^2\left[\hat{D}^2 + \frac{1}{4}\right], \qquad \hat{D} = -i\left(\partial_u - \frac{1}{2}\right)$$

$\hat{H}_\infty$ 是 Sturm-Liouville 问题的唯一自伴正算符（Friedrichs 扩张 + Neumann）。

### 2.3 $p$ 进扇区

$$S_p = \int_{\mathbb{R}} d\tau \int_{\mathbb{Q}_p} dx\; \Psi_p^\dagger\left(i\partial_\tau - \hat{H}_p\right)\Psi_p$$

### 2.4 Adele 中介耦合

$$S_{\eta,p} = \int_{\mathbb{R}} d\tau\left[\eta_p^\dagger(i\partial_\tau - \omega_p)\eta_p + \lambda\left(\eta_p^\dagger \mathcal{C}_p + \mathcal{C}_p^\dagger \eta_p\right)\right]$$

$$\mathcal{C}_p = \int_{\mathbb{Z}_p}\Psi_p\,dx - \Psi_\infty(u_p,\theta_p)$$

一阶与二阶是**两个独立构造**，非数学平方关系。一阶平方给出变系数 $\hat{\mathcal{D}}^2 = c^2 e^{2u}(-\partial_u^2+1/4)$，不同于 $\hat{H}_\infty$。详见 `CQM_推导_经典路径.md` §3–§5。

---

## 三、母方程（严格变分）

### 3.1 一阶方程

$$\boxed{(i\partial_\tau - \hat{\mathcal{D}})\Psi = \sum_{p\in\{2,3,5\}} \lambda\eta_p\,\delta_p^{(e)}} \tag{M0}$$

### 3.2 二阶方程（独立）

$$\boxed{(i\partial_\tau)^2\Phi = \hat{H}_\infty\Phi + \sum_p \lambda\eta_p\,\delta_p^{(e)}} \tag{M}$$

### 3.3 $p$ 进方程

$$\boxed{(i\partial_\tau - \hat{H}_p)\Psi_p = -\lambda\eta_p^\dagger \mathbf{1}_{\mathbb{Z}_p}} \tag{M2}$$

### 3.4 中介场方程

$$\boxed{(i\partial_\tau - \omega_p)\eta_p = -\lambda\mathcal{C}_p} \tag{M3}$$

**状态**：M0 自伴 + 变分严格；M 独立变分严格；M2 变分严格；M3 变分严格

---

## 四、$\hat{\mathcal{D}}^2$ 修正

$$\hat{\mathcal{D}}^2 = c^2 e^{2u}\left(-\partial_u^2 + \frac{1}{4}\right) \neq \hat{H}_\infty$$

| | $\hat{\mathcal{D}}^2$（一阶平方） | $\hat{H}_\infty$（二阶独立） | |:---|:---|:---| | 形式 | $c^2 e^{2u}(-\partial_u^2+1/4)$ | $c^2(-\partial_u^2+\partial_u)$ | | 系数 | 变系数 | 常系数 | | 漂移项 | 无 | $+\partial_u$ |

**状态**：严格代数证明（`CQM_推导_经典路径.md` §5）

---

## 五、全局幺正性

$$i\partial_\tau|\Psi\rangle = \hat{H}_{\text{tot}}|\Psi\rangle, \quad |\Psi\rangle = (\Psi, \Phi, \{\Psi_p\}, \{\eta_p\})^T$$

$$\hat{H}_{\text{tot}} = \begin{pmatrix}
\hat{\mathcal{D}} & 0 & 0 & \{\lambda\delta_p^{(e)}\} \\
0 & \hat{H}_\infty & 0 & \{\lambda\delta_p^{(e)}\} \\
0 & 0 & \{\hat{H}_p\} & \{-\lambda\mathbf{1}_{\mathbb{Z}_p}\} \\
\{\lambda\delta_p^\dagger\} & \{\lambda\delta_p^\dagger\} & \{-\lambda\mathbf{1}_{\mathbb{Z}_p}^\dagger\} & \{\omega_p\}
\end{pmatrix}$$

$$U(\tau) = \exp(-i\hat{H}_{\text{tot}}\tau), \qquad U^\dagger U = I$$

**自伴性验证**：
- 对角块：$\hat{\mathcal{D}}$（Neumann 自伴），$\hat{H}_\infty$（Sturm-Liouville 自伴），$\hat{H}_p$（Vladimirov + Kato-Rellich），$\omega_p\in\mathbb{R}$
- 非对角块互伴：$(\lambda\delta_p^{(e)}\eta_p,\Psi)_{d\mu} = \lambda\eta_p^\dagger \Psi(u_p,\theta_p) = (\eta_p,\lambda\delta_p^\dagger\Psi)_{\mathbb{C}}$

**状态**：Stone 定理 $\Rightarrow$ 强连续幺正群（`CQM_推导_经典路径.md` §6）

---

## 六、传输方程（一阶体区域退化）

体区域 $(u,\theta) \neq (u_p,\theta_p)$：

$$(i\partial_\tau - \hat{\mathcal{D}})\Psi = 0 \;\xrightarrow{\Psi = e^{u/2}\phi}\; \boxed{\partial_\tau\phi + c\,e^u\partial_u\phi = 0} \tag{T1}$$

特征线：$\displaystyle\frac{du}{d\tau} = c\,e^u \;\Rightarrow\; r(\tau) = \frac{1}{-c\tau + \text{const}} \tag{T2}$

**状态**：严格导出（测度补偿代数恒等，无近似）

---

## 七、二阶谱方程与谱间隙

### 7.1 Sturm-Liouville 构造

$$\hat{H}_\infty\Phi_n = E_n\Phi_n, \qquad E_n = c^2\left(\frac{1}{4} + \gamma_n^2\right) \tag{S1}$$

$$\hat{H}_\infty = c^2\left(\hat{D}^2 + \frac{1}{4}\right) \geq \frac{c^2}{4}, \qquad \boxed{E_0 = \frac{c^2}{4}} \tag{S2}$$

### 7.2 SU(5) 嘉当矩阵涌入

$$A_{ij} = \begin{pmatrix} 2 & -1 & 0 & 0 \\ -1 & 2 & -1 & 0 \\ 0 & -1 & 2 & -1 \\ 0 & 0 & -1 & 2 \end{pmatrix}$$

连续化 $\displaystyle\frac{1}{(\Delta u)^2}(A\psi)_i \to \left(-\partial_u^2 + \partial_u\right)\phi(u)$，谱待重新推导。

有效边界势：$\displaystyle V_{\text{eff}}(0) = \frac{c^2}{(\Delta u)^2}\cdot\frac{1}{\text{Tr}(A^{-1})} = \frac{c^2}{4}$，一致给出 $\boxed{E_0 = c^2/4}$。

Robin/Neumann 条件 $\partial_u\phi(0)=0$ 筛选 $s = 1/2 + i\gamma_n$ 满足 $\xi(s) = \xi(1-s)$。

**状态**：S1 定理（自伴已证）；S2 猜想（Hilbert-Pólya）；谱间隙 双路径（Sturm-Liouville + 嘉当矩阵 Friedrichs）

---

## 八、边界匹配与缩并

### 8.1 $p$ 进 Green 函数

$$g_p = \langle\mathbf{1}_{\mathbb{Z}_p}, (D^{\alpha_p}+V_p)^{-1}\mathbf{1}_{\mathbb{Z}_p}\rangle = \frac{1}{\lambda_0(p,\alpha_p)+v_p}$$

### 8.2 中介场自洽解

$\omega_p = \epsilon_p f_{\text{rep}} \ll f_{\text{rep}}$ 下：

$$\eta_p \approx \frac{1}{\epsilon_p}\mathcal{C}_p, \quad \chi_p \approx -\frac{g_p}{\epsilon_p}\mathcal{C}_p, \quad \chi_p = \frac{g_p/\epsilon_p}{1+g_p/\epsilon_p}\Psi_{\infty,p}$$

强耦合极限 $\epsilon_p \to 0$：$\chi_p \to \Psi_{\infty,p}$，$\mathcal{C}_p \to 0$，$\eta_p \to 0$，源项消失。

**状态**：$\epsilon_p \to 0$ 渐近严格

---

## 九、$p$ 进扇区（离散动力学）

### 9.1 Vladimirov 算符

$$D^{\alpha_p}f(x) = \frac{1}{\Gamma_p(-\alpha_p)}\int_{\mathbb{Q}_p}\frac{f(x)-f(y)}{|x-y|_p^{1+\alpha_p}}d\mu(y) \tag{P1}$$

$$D^{\alpha_p}\psi_{k;j,a} = p^{\alpha_p j}\psi_{k;j,a} \tag{P2}$$

### 9.2 Adele 约束

$$\prod_{p\in\{2,3,5\}}\mathbb{Z}_p = \frac{1}{30} \tag{A2}$$

**状态**：P1 严格定义；P2 Kozyrev 基严格对角化；A2 假设（"仅 2,3,5" 证明开放）

---

## 十、物理常数（从谱结构涌出）

### 10.1 SU(5) 精细结构常数

$$\boxed{\alpha^{-1} = 2^{14} \cdot 3^{-1} \cdot 5^{-3} \cdot \pi = \frac{16384\pi}{375} = 137.2583} \tag{Q1}$$

> **此粗略表达式是GL(5)整体的反映**，不是GL(1)层的产物。源于SU(5)破缺→$A_4$嘉当矩阵→4紧致本征群$\{SU(2)_k\}_{k=1}^{4}$（全紧致）的整体结构，$\alpha$来自$U(1)$电磁群耦合常数。

### 10.2 引力常数

$$\boxed{G_N^{(0)} = \frac{I\cdot\lambda_c\cdot C^2\cdot E_1}{m_p^2}\cdot\exp\left(-\frac{2}{C}\right)} \tag{Q2}$$

$$\boxed{G_N = G_N^{(0)}\cdot(1+\kappa C)}, \quad \kappa = \frac{31 + C}{30} \tag{Q3}$$

### 10.3 中子质量差

$$\boxed{\Delta m = 2\theta_4\cdot C^2\cdot m_p\cdot\left[1-\alpha_5(C)C\right]} \tag{Q4}$$

### 10.4 中子寿命

$$\boxed{\tau = \frac{e^{-u_0}(1-1/e)\hbar}{C\varepsilon m_p}, \quad u_0 = -\sqrt{\frac{E_1^{\text{eff}}}{\pi C}}} \tag{Q5}$$

| 方程 | 状态 | 备注 | |:---|:---:|:---| | Q1 ($\alpha^{-1}$) | 定理 | 禁闭精细结构常数（SU(5)） | | Q2 ($G_N^{(0)}$) | 数值自洽 | 大头公式 | | Q3 ($\kappa$) | 定理 | $\kappa=(31+C)/30$，约 −3 ppm | | Q4 ($\Delta m$) | 数值自洽 | −0.09 ppm | | Q5 ($\tau$) | 数值自洽 | +4 ppm |

---

## 十一、涌现几何（宏观极限）

### 11.1 爱因斯坦方程

$$\boxed{G_{\mu\nu} = 8\pi G_N\langle T_{\mu\nu}\rangle} \tag{E1}$$

### 11.2 能动张量来源

$$\boxed{\langle T_{\mu\nu}\rangle = \langle\psi|\hat{\mathcal{P}}_{\text{self}}^{(2)}\hat{T}_{\mu\nu}^{\text{QCD}}\hat{\mathcal{P}}_{\text{self}}^{(2)}|\psi\rangle} \tag{E2}$$

QCD 能动张量主导（~99% 质子质量），禁闭后残余为引力源。

### 11.3 有效作用量

$$\boxed{S_{\text{eff}}[g, \psi, A] = \frac{1}{16\pi G_N} \int d^4x \sqrt{-g} \, R + \int d^4x \sqrt{-g} \, \mathcal{L}_{\text{QCD}}[\hat{\mu}\psi, A]} \tag{E3}$$

**推导链**：一阶/二阶耦合系统 $\to$ 统计收敛 $N\to\infty$ $\to$ Jacobson 热力学 $\to$ Lovelock 唯一性 $\to$ E3。

**状态**：E1 启发式（Jacobson）；E2 物理图像清晰；E3 形式写定

---

## 严格性总览

| # | 环节 | 方程 | 状态 | 缺口 | |:---|:---|:---|:---:|:---| | 0 | 本体论公理 | A0–A1 | 预设 | — | | 1 | 几何与 Hilbert 空间 | $R,\hat{\mu},\mathcal{H}_\infty,\mathcal{H}_p$ | 构造性 | — | | 2 | 作用量 | $S_\infty^{(1)}, S_\infty^{(2)}, S_p, S_{\eta,p}$ | 形式写定 | — | | 3 | 母方程 | M0–M3 | 变分严格 | — | | 4 | $\hat{\mathcal{D}}^2$ 修正 | $\hat{\mathcal{D}}^2 = c^2 e^{2u}(-\partial_u^2+1/4)$ | 严格代数 | — | | 5 | 全局幺正 | $\hat{H}_{\text{tot}}$ 自伴 | Stone 定理 | — | | 6 | 传输方程 | T1–T2 | 测度补偿 | — | | 7 | 二阶谱与间隙 | S1–S2, $E_0=c^2/4$ | 猜想 | Hilbert-Pólya | | 8 | 边界匹配 | $\epsilon_p\to0$ | 渐近严格 | — | | 9 | $p$ 进扇区 | P1–P2, A2 | 严格+假设 | "仅 2,3,5" | | 10 | 物理常数 | Q1–Q5 | 数值自洽 | 缺口 1,6,7,N-2 | | 11 | 涌现几何 | E1–E3 | 启发式/形式写定 | — |

---

## 核心方程（极简版）

一阶：$\displaystyle i\partial_\tau\Psi = \hat{\mathcal{D}}\Psi + \sum_p \lambda\eta_p\,\delta_p^{(e)}$

二阶：$\displaystyle (i\partial_\tau)^2\Phi = \left[-\partial_u^2 + \partial_u + \bigoplus_{p\in\{2,3,5\}}\left(D^{\alpha_p}+V_p\right)\right]\Phi$

$$\boxed{\hat{\mu}^2=\hat{\mu}, \quad \hat{\mu}=\frac{I+R}{2}}$$

$$\boxed{E_0 = \frac{c^2}{4}, \qquad G_N=\frac{I\lambda_c C^2 E_1}{m_p^2}e^{-2/C}\bigl(1+\kappa C\bigr)}$$

**完整严格推导链**：`CQM_推导_经典路径.md`
