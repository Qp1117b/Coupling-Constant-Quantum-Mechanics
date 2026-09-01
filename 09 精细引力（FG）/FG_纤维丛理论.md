# FG纤维丛理论

## 1. FG的本体论定位

精细引力FG是量子引力QG与经典引力GR之间的关键中介：

| 引力 | 存在论地位 | 数学结构 |
|------|-----------|---------|
| **QG** | 最基础、最不可还原 | 黎曼零点谱 $\gamma_n$（前几何约束） |
| **GR** | 广度前提（平滑展开） | 伪黎曼流形 |
| **FG** | 深度前提（层级激发） | FG底空间上的主丛 $P(M,G)$ |

$$\boxed{\text{FG} \neq \text{GR}}$$

- GR是时空曲率，受 $G_N$ 约束，量级 $\sim 10^{-43}$
- FG是一个联络生成两种曲率——底空间Regge角亏 $\delta_v$ + 伴丛曲率 $F=d\mathcal{A}+\mathcal{A}\wedge\mathcal{A}$——**不受 $G_N$ 约束**，量级 $O(1)$
- FG是GR基态的非平庸激发态，直接由底空间Regge角亏给出

## 1.5 纤维丛双框架：运动学（容器）vs 动力学（约束）

同一套纤维丛数学，两种物理诠释。**CQM采用动力学（约束）框架**，运动学（容器）框架仅作为对比/批判对象——传统物理把丛当作先验舞台，CQM把丛当作物质自组织的涌现产物。

### 1.5.1 总纲

| | **纤维丛运动学**（容器框架，传统物理） | **FG纤维丛动力学**（重组框架，CQM） |
|---|---|---|
| **哲学** | 丛是**先验舞台**，物理在其上展开 | 丛是**涌现产物**，物理即约束过程 |
| **底空间** | 先验容器（给定背景） | 物质自组织的空间形态本身（§1） |
| **核心方程** | $D_\mu \psi = (\partial_\mu + A_\mu)\psi$ | $(p\cdot g,\, f) \sim (p,\, g\cdot f)$ |
| **主丛角色** | 固定背景（规范场 $A_\mu$ 的载体） | 自由相（重组实现前的高对称态） |
| **伴丛角色** | 物质取值空间（向量空间 $V$） | 约束结果（紧致李群 $R$） |
| **约束位置** | **外部**：微分方程强加于截面 | **内部**：等价关系定义空间本身 |

### 1.5.2 纤维丛运动学（容器框架，传统物理）

$$\begin{aligned}
&\text{主丛 } P(M,G) &&\text{—— 舞台骨架} \\
&\text{伴丛 } E = P \times_\rho V &&\text{—— 演员化妆间} \\
&\text{截面 } \psi \in \Gamma(E) &&\text{—— 演员（物质场）} \\
&\text{联络 } A \in \Omega^1(P,\mathfrak{g}) &&\text{—— 舞台灯光控制} \\
&\text{曲率 } F = dA + A\wedge A &&\text{—— 灯光效果}
\end{aligned}$$

动力学方程（外部强加）：
- **Dirac**：$(i\gamma^\mu D_\mu - m)\psi = 0$
- **Yang-Mills**：$D^\mu F_{\mu\nu} = J_\nu$
- **Bianchi**：$DF = 0$（舞台几何相容性）

特征：
- $G$ 固定不变，$H$ 不出现或作为外部破缺参数
- 物质场是**向量** $\psi: M \to V$
- 协变导数是**耦合装置**：$D_\mu = \partial_\mu + \rho(A_\mu)$

**CQM对容器框架的批判**：容器框架把底空间 $M$ 当作先验容器，与CQM核心主张"底空间是物质自组织的空间形态本身"矛盾。传统物理的规范场论、标准模型均采用容器框架——丛是给定的，物理在其上展开。CQM的发生学顺序（物质先在→自组织→底空间涌现→丛涌现）排除了先验容器。

### 1.5.3 纤维丛动力学（重组框架，CQM）

$$\begin{aligned}
&\text{主丛 } P(M,G) &&\text{—— 自由相（母群）} \\
&\text{约束群 } H \triangleleft G &&\text{—— 紧致李群，闭正规子群（约束触发）} \\
&\text{本征群 } R &&\text{—— 紧致李群（重组产物）} \\
&\text{约束伴丛 } E_{R} = P \times_G R &&\text{—— 涌现产物} \\
&\text{截面 } \langle\phi\rangle \in \Gamma(E_{R}) &&\text{—— 序参量/真空选择}
\end{aligned}$$

约束方程（内部定义）：

$$(p\cdot h,\, f) \sim (p,\, h\cdot f),\quad \forall h \in H$$

**$R$ 是重组产物**：给定母群 $G$ 和约束群 $H$（$H \triangleleft G$，$G$、$H$ 均为紧致李群），重组产物 $R$ 是紧致李群。物理实例：磁通量子化（$U(1)/Z_n \cong U(1)$）、整数自旋表示（$SU(2)/Z_2 \cong SO(3)$）、电荷量子化（$U(N) = (U(1)\times SU(N))/Z_N$）。

### 1.5.4 核心对比

| 对比项 | 运动学（容器，传统物理） | 动力学（约束，CQM） |
|--------|--------------|--------------|
| **主丛群 $G$** | 规范对称性（背景） | 母群（自由相，重组实现前） |
| **约束群 $H$** | 不出现或外部参数 | 内部子群，定义等价关系 |
| **纤维 $F$** | 向量空间 $V$（$\mathbb{C}, \mathbb{C}^n, \mathfrak{g}$） | 紧致李群 $R$（重组产物） |
| **伴丛** | $E = P \times_\rho V$ | $E_{R} = P \times_G R$ |
| **截面** | 物质场 $\psi$（向量值） | 序参量 $\langle\phi\rangle$（陪集值） |
| **联络作用** | 协变导数 $D_\mu$ 转动纤维 | 约束映射折叠纤维 |
| **曲率/场强** | 物理可观测量（能量、力） | 拓扑障碍（示性类、单极子） |
| **破缺** | 希格斯势外部强加 VEV | 自由能极小值自发选择 $H$ |
| **Goldstone 模** | 在 $G/H$ 上振动的场 | 约束伴丛截面的切向涨落 |
| **质量生成** | Higgs 机制（外部耦合） | 重组后 $R$ 方向的联络分量获得质量 |

### 1.5.5 转化关系：容器 ↔ 约束

两种框架是**同一纤维丛对象在不同能标/相下的两种视角**：

**容器 → 约束（追问起源）**：从线丛 $L_2$（容器）追溯到 $U(1)/Z_2$（约束）——库珀对是 $Z_2$ 约束的产物。

**约束 → 容器（低能有效理论）**：重组实现完成后，$R$ 的伴丛成为新能标下的固定背景——$SO(3)$ 规范场论把 $SO(3)$-向量丛当作容器，忘记它来自 $SU(2)/Z_2$。

$$\text{运动学} \xrightarrow{\text{追问 } H \text{ 的起源}} \text{动力学}$$

$$\text{动力学} \xrightarrow{\text{低能冻结 } \langle\phi\rangle} \text{运动学}$$

### 1.5.6 CQM的选择：重组框架

CQM选择动力学（约束）框架的原因：

1. **底空间是物质自组织的空间形态本身**（§1）——排除了先验容器
2. **丛是约束过程的涌现产物**——主丛群 $G$ 通过子群 $H$ 自我折叠为有效几何 $R$
3. **约束是内部的**——等价关系定义空间本身，非外部强加的微分方程
4. **发生学顺序**：物质先在→自组织→底空间涌现→丛涌现→约束→有效几何

容器框架仅在低能有效理论中出现——重组实现完成后，重组产物被"冻结"为新能标下的固定背景，此时可暂时采用容器框架描述，但需记住其重组起源。

### 1.5.7 重组框架的深层统一：伴丛截面 = 序参量 = 物质场

重组框架消除了"背景"与"物质"的形而上学分割——伴丛截面同时就是物质场。

**伴丛截面 = 序参量**：重组框架中，伴丛定义为 $E_{R} = P \times_G R \cong P/H$，其截面是映射 $\phi: M \to P/H$。在时空每一点 $x \in M$，$\phi(x)$ 是 $G/H$ 中的一个**陪集**，即一个**真空方向**——这正是序参量。

实例（约束生成群 $R$，VEV 在 $V$ 中选方向）：
- **电弱**：约束 $(SU(2)\times U(1))/Z_2 \to U(1)\times SO(3)$，VEV $\langle\phi\rangle\in V=\mathbb{C}^2$ 选方向，约束至 $U(1)_{\text{em}}$，序参量 $\phi(x)\in (SU(2)\times U(1))/U(1)_{em} \sim S^3$
- **超导**：约束 $U(1)/Z_2 \to U(1)$，库珀对凝聚相位 $\phi(x) \in U(1)$
- **铁磁体**：约束 $SO(3)/\{e\} \to SO(3)$，VEV $\langle\psi\rangle\in V=\mathbb{R}^3$ 选方向，约束 $SO(3)\to SO(2)$，磁化方向 $\phi(x)\in SO(3)/SO(2) \sim S^2$

在重组框架中，"物质场"就是背景自身通过重组折叠后涌现的截面。

**与容器框架的精确平行**：两种框架共享同一幅"场=截面"的图像，区别仅在于纤维：

| | 容器框架 | 重组框架 |
|---|---|---|
| **伴丛** | $E = P \times_\rho V$ | $E_{R} = P \times_G R$ |
| **纤维** | 向量空间 $V$（线性） | 齐性空间 $G/H$（非线性） |
| **截面** | 物质场 $\psi: M \to V$ | 序参量 $\phi: M \to G/H$ |
| **变换法则** | $\psi \to \rho(g)\psi$（线性） | $\phi \to g\cdot\phi$（非线性） |
| **真空** | $\psi = 0$（平凡） | $\phi = \text{常值}$（约束方向） |

**关键统一**：在两种情况下，物理场都是**伴丛的截面**。容器框架是重组框架在"纤维可线性化"时的特例。

**背景与物质的同一**：当伴丛截面同时是物质场时，传统区分被消解：

| 传统区分 | 容器框架 | 重组框架 |
|---------|---------|---------|
| **背景 vs 物质** | 主丛是背景，伴丛是物质容器 | 主丛通过约束**成为**伴丛，背景即物质 |
| **真空 vs 激发** | 真空是 $\psi=0$，激发是 $\psi \neq 0$ | 真空是 $\phi = \langle\phi\rangle$（非零截面），激发是 $\phi(x)$ 在 $G/H$ 上的振动 |
| **对称性 vs 破缺** | 对称性是背景属性，破缺是物质属性 | 对称性折叠**定义了**物质场的取值空间 |

重组框架对通常说的自发对称性破缺的诠释：重组定义了新的伴丛，其非零截面就是物理真空。

**退化情形：重组框架回到容器**：如果 $G/H$ 允许忠实线性表示（如 $SO(3) \hookrightarrow GL(3,\mathbb{R})$），则 $G/H$ 的坐标可以嵌入向量空间 $V$，非线性序参量 $\phi: M \to G/H$ 退化为线性物质场 $\psi: M \to V$，重组框架的伴丛截面就是容器框架的物质场。其实质为约束伴丛与容器伴丛的同构：

$$\underbrace{P \times_G (G/\ker\rho)}_{\text{约束伴丛}} \;\cong\; \underbrace{P \times_\rho V}_{\text{容器伴丛}}$$

当表示存在时，两种框架的截面完全重合。

**总结**：重组框架下伴丛的截面同时就是物质场——严格的数学同一。容器框架中物质场是向量丛的截面；重组框架中物质场是齐性丛的截面。两者共享"场=伴丛截面"的本质，区别仅在于纤维是线性的 $V$ 还是非线性的 $G/H$。这彻底消除了背景与物质的二元对立：真空结构本身就是物质场的取值空间。

## 2. 纤维丛四元组

每层FG由纤维丛四元组完整刻画：

$$\boxed{(M_\ell,\; P(M_\ell, G_\ell),\; \mathcal{A}_\ell,\; \hat{\mathcal{S}}_\ell)}$$

| 要素 | 定义 | 物理意义 |
|:---|:---|:---|
| 底空间 $M_\ell$ | 层级 $\ell$ 的物质分布几何经Regge剖分 | 三角剖分的离散几何 |
| 主丛 $P(M_\ell, G_\ell)$ | 结构群 $G_\ell$ 上的主丛 | 规范结构 |
| 联络 $\mathcal{A}_\ell$ | 由层级Regge晶胞分步生成 | 平行移动规则 |
| 同步算符 $\hat{\mathcal{S}}_\ell$ | 紧化算符在层级截面空间的实现 | 谱算符，给出群谱 |

### 2.0 主丛结构关系：$F = G \leftrightarrow R = G \leftrightarrow \hat{H}$

**FG当前用于描述规范相变物理**。核心结构：CQM FG的主丛是从结构群到实现群（等价地到群算符）的重组实现，群算符是实现群在表示空间上的算符表示。箭头 $\leftrightarrow$ 表示**重组实现**（$G$ 经重组实现为 $R$，等价地重组为 $\hat{H}$）。

$$\boxed{F = G \leftrightarrow R = G \leftrightarrow \hat{H}}$$

其中：
- $G$：**主丛结构群**（母群，如 $SU(5)$）
- $R$：**实现群**（本征群，重组产物，公理1+2保证紧致性）
- $\hat{H}$：**群算符**（$R$ 在表示空间上的算符表示，故 $R$ 与 $\hat{H}$ 在谱的意义下等价）
- $F = G \leftrightarrow R = G \leftrightarrow \hat{H}$：**主丛**（结构群 $G$ 经重组实现为实现群 $R$，等价地重组为群算符 $\hat{H}$）

**子群重组**：在规范相变中，$G$ 本身不变，内部以子群重组——$R$ 和 $\hat{H}$ 的谱是 $G$ 内部子群的谱（$\text{Spec}(R), \text{Spec}(\hat{H}) \subseteq \text{Spec}(G)$），但 $G$ 本身不变为子群。规范相变是 $G$ 的内部结构通过子群重新组织，不是 $G$ 重组为别的群。

**类薛定谔方程**：同步方程 $\hat{\mathcal{S}}|\Psi\rangle = s|\Psi\rangle$ 类比薛定谔方程 $\hat{H}|\psi\rangle = E|\psi\rangle$：

| 薛定谔方程 | CQM同步方程 |
|:---|:---|
| $\hat{H}$（哈密顿算符） | $\hat{\mathcal{S}}$（同步算符） |
| $E$（能量本征值） | $s$（同步本征值） |
| $|\psi\rangle$（本征态） | $|\Psi\rangle$（同步本征态） |
| Hilbert空间 | 纤维丛截面空间 |

**四层结构**：

$$\underbrace{G,\; R}_{\text{1. 代数层}} \;\longrightarrow\; \underbrace{\hat{H}|\Psi\rangle = s|\Psi\rangle}_{\text{2. 算符层（类薛定谔）}} \;\longrightarrow\; \underbrace{F = G \leftrightarrow R = G \leftrightarrow \hat{H}}_{\text{3. 丛层（主丛）}} \;\hookrightarrow\; \underbrace{\text{运动学纤维丛}}_{\text{4. 运动学层}}$$

1. **代数层**：$G$（母群），$R$（实现群/本征群）
2. **算符层**：$\hat{H}$（群算符，$R$ 的算符表示）→ 类薛定谔方程 $\hat{H}|\Psi\rangle = s|\Psi\rangle$
3. **丛层**：$F = G \leftrightarrow R = G \leftrightarrow \hat{H}$（主丛，结构群 $G$ 经重组实现为实现群 $R$ 或群算符 $\hat{H}$）
4. **运动学层**：$F$ 作为主丛嵌入运动学纤维丛（§1.5.2容器框架），参与动力学

**物理意义**：
- $R = \hat{H}$：实现群 = 群算符（谱等价）——群论结构确定算符谱，算符谱反推群论结构
- $F = G \leftrightarrow R = G \leftrightarrow \hat{H}$：主丛是结构群到实现群（等价地到群算符）的重组实现，物理态空间 $= \text{Im}(G \leftrightarrow R)$
- $F \hookrightarrow$ 运动学纤维丛：重组框架（动力学）的产物嵌入容器框架（运动学），实现§1.5.5的转化关系

**CQM纤维丛理论描述的是规范相变物理**：$F = G \leftrightarrow R = G \leftrightarrow \hat{H}$ 的本质是规范相变。大统一群 $GL(5)$（约化李群，非紧致）本身是重组实现的，不是破缺的。**破缺的一定是非紧致李群，但实现重组实现的既可以是紧致李群也可以是非紧李群**。$GL(5,\mathbb{R})$ 的时空对称性若纳入规范群则必须破缺；紧致部分（如 $SU(5) \subset GL(5,\mathbb{C})$）的规范相变是重组实现，没有发生破缺。母群 $G$（高对称相/自由相）经重组实现为 $R$（低对称相/有序相），群算符 $\hat{H}$ 是重组后在表示空间中的算符残余。纤维丛刻画的是规范相变物理：主丛结构群 $G$ 是相变前的对称性，纤维 $R$ 是相变后的有序态空间，联络编码相变的局域触发机制，曲率表征相变的拓扑障碍（示性类、单极子）。§1.5.3的约束方程 $(p\cdot h, f) \sim (p, h\cdot f)$ 是规范相变的数学化——等价关系折叠高对称态空间为低对称相的轨道空间。

### 2.1 四层FG剖分

| 层级 | 底空间 $M_\ell$ | 结构群 $G_\ell$ | 联络 $\mathcal{A}_\ell$ |
|:---|:---|:---|:---|
| 元素FG | 质子+中子分布 | $U(1) \times SO(2) \times SU(4)$ | 核子间联络 |
| 分子FG | 原子分布 | 分子点群 | 原子间联络（化学键） |
| 晶胞FG | 原子/分子分布 | 空间群 | 晶胞中联络 |


### 2.2 层级嵌套

$$P_{\text{el}} \hookrightarrow P_{\text{mol}} \hookrightarrow P_{\text{cell}}$$

每层底空间是上层的纤维。

## 3. 联络：一个联络生成两种曲率

$$\mathcal{A}_\ell \longrightarrow \begin{cases} \text{底空间曲率：Regge角亏 } \delta_v^{(\ell)} = 2\pi - \sum_{\Delta \ni v} \alpha_\Delta \\ \text{伴丛曲率：} F_\ell = d\mathcal{A}_\ell + \mathcal{A}_\ell \wedge \mathcal{A}_\ell \end{cases}$$

- 底空间曲率进入不确定性关系与谱调制
- 伴丛曲率进入运动方程 $D * F = *J_\Phi$
- 同一联络，两种曲率，各自遵循不同的数学规则

### 3.1 和乐

$$W_v^{(\ell)} = \exp(i\delta_v^{(\ell)} \hat{T}_\ell) \in G_\ell$$

其中 $\hat{T}_\ell$ 是层级结构群 $G_\ell$ 的生成元。

和乐平庸化条件给出该层级的"稳定构型"：
- 元素FG：和乐平庸化 = 闭壳层稳定构型（稀有气体）
- 分子FG：和乐平庸化 = 稳定杂化几何（理想键角）
- 晶胞FG：和乐平庸化 = 稳定晶格构型

### 3.2 层级角亏传递

$$\delta_v^{(\ell+1)} = \delta_{v,\text{intrinsic}}^{(\ell)} + \Delta\delta_{\text{defect}}^{(\ell+1)}$$

上层内禀角亏是下层角亏的组成部分。

### 3.3 伴丛运动方程形式化

主丛 $P(M_\ell, G_\ell)$ 的**伴丛**（adjoint bundle）：

$$\boxed{\text{ad}(P) = P \times_{G_\ell} \mathfrak{g}_\ell \;\xrightarrow{\pi}\; M_\ell}$$

其中 $\mathfrak{g}_\ell = \text{Lie}(G_\ell)$，$G_\ell$ 通过伴随表示 $\text{Ad}: G_\ell \to \text{Aut}(\mathfrak{g}_\ell)$ 作用。**结构群 $G_\ell$ 必须是紧致李群**（§4.0.1），否则伴随表示非幺正、Killing形式非负定，伴丛上的几何失去正定性。

**伴丛上的几何量**：

| 量 | 数学定义 | 空间 | 物理意义 |
|:---|:---|:---|:---|
| 联络 $\mathcal{A}$ | $G_\ell$-联络 | $\Omega^1(M_\ell) \otimes \text{ad}(P)$ | Regge几何生成 |
| **伴丛曲率** $F$ | $d\mathcal{A} + \mathcal{A} \wedge \mathcal{A}$ | $\Omega^2(M_\ell) \otimes \text{ad}(P)$ | 同步场强 |
| 外协变导数 $D$ | $d + [\mathcal{A}, \cdot]$ | $\Omega^k \otimes \text{ad}(P) \to \Omega^{k+1} \otimes \text{ad}(P)$ | 规范协变 |
| 同步场 $\Phi$ | 伴丛截面 | $\Gamma(\text{ad}(P))$ | 物质分布 |
| 同步流 $J_\Phi$ | $J_\Phi = \frac{\delta S_{\text{matter}}}{\delta \mathcal{A}}$ | $\Omega^1(M_\ell) \otimes \text{ad}(P)$ | 物质源 |

**伴丛运动方程**（Yang-Mills型）：

$$\boxed{D * F = *J_\Phi}$$

物理意义：
- **左端 $D * F$**：伴丛曲率的协变散度，描述同步场强的规范协变变化
- **右端 $*J_\Phi$**：同步场 $\Phi$（物质分布）生成的流，是同步场强的源
- **方程整体**：物质分布（核子量子振荡）通过伴丛曲率决定同步场强，同步场强反过来约束物质分布——**自洽方程**

**Bianchi恒等式**（几何自洽性）：

$$D F = 0 \quad \iff \quad [\hat{L}_m, [\hat{L}_n, \hat{L}_p]] + \text{cyclic} = 0 \quad \text{（Jacobi恒等式）}$$

伴丛曲率的协变外导数为零，对应Kac-Moody代数的Jacobi恒等式（§9.3纤维丛与CFT严格对应）。这是同步方程相容性的几何保证。

**同步方程与伴丛运动方程的关系**：

| | 伴丛运动方程 | 同步方程 |
|:---|:---|:---|
| **方程** | $D * F = *J_\Phi$ | $\hat{\mathcal{S}}_k \Psi_k = s_k \Psi_k$ |
| **类型** | Yang-Mills型场方程 | 本征值方程 |
| **空间** | $\Omega^1(M_\ell) \otimes \text{ad}(P)$ | $\Gamma(\text{ad}(P))$ |
| **角色** | 曲率-物质自洽关系 | 谱分解（本征群分类） |
| **关系** | 运动方程的解给出允许的曲率配置 | 本征值方程对解空间做谱分解 |

同步方程是伴丛运动方程的**谱分解**：运动方程确定允许的曲率配置，同步算符 $\hat{\mathcal{S}}_k = \frac{L_u}{2\pi C}\sqrt{1 - \beta \hat{\delta}_v^{(k)}}$ 对这些配置做本征值分解，本征值 $s_k$ 分类本征群 $G_k$。

## 4. 同步算符：纤维丛的谱算符

### 4.0 核心问题：底空间+约束→同步方程→本征群→耦合常数

FG的核心问题之一是：**给定底空间（Regge剖分）+约束（核子量子振荡、曲率涨落、耦合常数涨落），求解同步方程的本征群（自守形式），本征群对应的耦合常数就是涨落耦合常数指定的。**

$$\boxed{\underbrace{M_\ell}_{\text{底空间}} + \underbrace{\hat{\mathcal{S}}_k}_{\text{作用量算符（同步算符）}} + \underbrace{G_k}_{\text{对称性}} \;\Rightarrow\; \underbrace{\Psi_k}_{\text{自守形式}} \;\longrightarrow\; \text{耦合常数（由涨落指定）}}$$

**底空间不可省略**：$\Psi_k \in \Gamma(\text{ad}(P))$ 是底空间 $M_\ell$ 上的伴丛截面（自守形式），作用量算符（同步算符）$\hat{\mathcal{S}}_k$ 作用在 $\Gamma(\text{ad}(P))$ 上，对称性 $G_k$ 在 $M_\ell$ 上作用。缺少底空间，作用量算符和对称性均无法定义。

**GL(n) 由重组产物的基本表示严格确定（发生学顺序强制）**：$SU(5)$ 经重组实现 $\to U(1)\times SU(2)\times SU(3)$，各因子通过基本表示 $\rho_{\text{fund}}: R \to GL(V_{\text{fund}})$ 给出各自自守框架（$SU(5) \xrightarrow{\rho_{\text{fund}}} GL(\mathbb{C}^5)$、$SU(3) \xrightarrow{\rho_{\text{fund}}} GL(\mathbb{C}^3)$、$SU(2) \xrightarrow{\rho_{\text{fund}}} GL(\mathbb{C}^2)$、$U(1) \xrightarrow{\rho_{\text{fund}}} GL(\mathbb{C})$），$n = \dim V_{\text{fund}}$ 由表示严格确定。$SU(5)$ 由"含标准模型的最小单群"锚定（rank 4），$S_5=\mathrm{Weyl}(A_4)$ 只作交叉印证。物理主丛不能反向指定 $GL(n)$：主丛结构群（紧群）是紧化投影的输出，以输出指定输入构成循环论证。详见 `FG_核心理论.md` §3.0。

约束链：

$$\text{Regge剖分} + [\hat{X},\hat{P}]=i\hbar \xrightarrow{\text{离散协变导数}} \text{嘉当矩阵} \xrightarrow{\text{对角化}} \text{声子} \xrightarrow{\text{几何非线性}} \hat{\delta}_v \xrightarrow{\text{FG因果}} v_\tau \xrightarrow{\text{定义}} p_u \xrightarrow{[\hat{u},\hat{p}_u]=i} \text{紧化U(1)} \xrightarrow{\text{玻尔-索末菲}} n_k \xrightarrow{\text{同步方程}} G_k$$

- **Regge剖分约束**：$\mathcal{R}=(V,E,F,\{\bar{L}_{ij}\})$，经典角亏 $\bar{\delta}_v = 2\pi - \sum_{\Delta\ni v}\bar{\theta}_v(\Delta)$ 由经典边长通过余弦定律严格确定。质子 $A_4$：$\bar{\delta}_v=0$（理想平坦）；中子 $D(\delta)$：$\bar{\delta}_v\neq 0$（经典背景曲率）
- **位置-动量代数**：每个顶点 $v$ 上 $[\hat{X}_v,\hat{P}_v]=i\hbar$（预量子化线丛的联络曲率）
- **嘉当矩阵 = 图拉普拉斯**：离散协变导数的矩阵形式，是Regge剖分的必然结果
- **声子代数**：简正模式对角化保持对易子 $[\hat{Q}_k,\hat{\Pi}_{k'}]=i\hbar\delta_{kk'}$，声子来自 $[\hat{X},\hat{P}]=i\hbar$，**不是额外假设**。声子的三层结构（QG前几何/GR时空度规/FG核子曲率）与统一角色详见 `01 核心理论/CQM_核心_声子理论.md`
- **曲率涨落算符（严格推导）**：位置涨落平方 + Regge几何非线性 → $\hat{\delta}_v^{(1)} = \sum_k \frac{\hbar\omega_k}{E_{\text{bind}}}|v_k(v)|^2(\hat{a}_k^\dagger\hat{a}_k + \frac{1}{2})$，**不是唯象假设**。其中 $1/E_{\text{bind}}$ 是**量纲归一化因子**——FG纤维丛截断在此处把有量纲的声子能量 $\hbar\omega_k$（$[\text{能量}]$）除以核子结合能 $E_{\text{bind}}$（$[\text{能量}]$），得到无量纲曲率算符。这是CQM所有后续方程（同步方程、CFT/OPE）无量纲性的**根本来源**。
- **总曲率 = 经典背景 + 量子涨落**：$\hat{\delta}_v = \bar{\delta}_v + \hat{\delta}_v^{(1)}$，$\bar{\delta}_v$ 是c-数（经典背景曲率），$\hat{\delta}_v^{(1)}$ 是算符（量子涨落）
- **FG因果约束（假设）**：固有时流速 $v_\tau^{(k)} = \sqrt{1-\beta\delta_v^{(k)}}$ → 耦合动量 $p_u^{(k)} = v_\tau^{(k)}/C$。这是FG核心机制，标注为**假设**
- **同步方程**：$\hat{\mathcal{S}}_k \Psi_k = n_k \Psi_k$，同步算符 $\hat{\mathcal{S}}_k = \frac{L_u}{2\pi C}\sqrt{1-\beta\hat{\delta}_v^{(k)}}$ 由约束严格确定
- **本征群**：$R_k$ 是重组产物，壳层标签 $l_k = k-1$ 由 SU(5) 简单根的 Dynkin 图深度严格推导
- **耦级（定义）**：$n_k \equiv C_k = l_k(l_k+1) + 3/4$（同步成本=对称性强度）
- **约束方程**：$\frac{L_u}{2\pi C}\sqrt{1-\beta\delta_v^{(k)}} = C_k$（锁定声子占据数 $N_k$）
- **CFT OPE**：同步本征态 $\otimes$ 耦合本征态 $\to$ 群本征态（共形固定点，Dirac约束=共形自举方程的CQM具体化）
- **耦合常数**：$g_k = \alpha\exp(-(n_k-n_1)/n_1)$——是同步方程的**输出**，不是输入参数

### 4.0.1 SU(5)重组实现→A_4→4紧致本征群→4耦合常数

SU(5)李代数$\mathfrak{su}_5$的根系为$A_4$型，重组实现产生两个独立效应：

**规范重组**（不属于本征群效应，三个空间群直积，全紧致，**时间内禀没有群**）：

$$\text{SU}(5) \;\xrightarrow{\text{规范重组}}\; U(1) \times SU(2) \times SU(3) \;\xrightarrow{g_{U(1)}}\; \alpha$$

**本征群效应**（同步方程本征群，全紧致）：

$$\boxed{\{R_k\}_{k=1}^{4} \;\xrightarrow{\text{4耦合常数}}\; \{g_k\}_{k=1}^{4}}$$

本征群 $R_k$ 是重组产物，壳层标签 $l_k = k-1$ 由 SU(5) 简单根的 Dynkin 图深度严格推导。四个本征群 $R_k \cong SU(2) \cong S^3$（三维球面，**紧致连通李群**），对应s/p/d/f四个亚壳层。Kac-Moody代数 $\widehat{\mathfrak{su}(2)}_k$ 由紧致李代数 $\mathfrak{su}(2)$ 中心扩展构造，CFT框架（Verlinde公式、OPE系数）的数学前提满足。

**精细结构常数 $\alpha$ 来自SU(5)规范重组后$U(1)$电磁群的耦合常数**。精细结构常数是GL(5)整体的反映，不是GL(1)层的产物。

### 4.1 耦合常数算符 $\hat{u}$

$$\boxed{\hat{u} = \ln \hat{g}, \quad [\hat{u}, \hat{p}_u] = i}$$

- $\hat{u}$：耦合常数对数算符，本征值 $u \in [0, L_u)$
- $\hat{g} = e^{\hat{u}}$：耦合常数算符，本征值 $g = e^u$
- $\Delta u \cdot \Delta p_u \geq \frac{1}{2}$

### 4.2 双空间同步算符

同步算符**同时**作用于核子空间和耦合常数空间：

$$\boxed{\hat{\mathcal{S}} = \hat{\mathcal{S}}_{\text{nucleon}} \otimes \hat{\mathbb{I}}_{U(1)} + \hat{\mathbb{I}}_{\text{nucleon}} \otimes \hat{\mathcal{S}}_{U(1)}(\hat{u})}$$

**核子部分**（由FG因果严格确定）：

$$\hat{\mathcal{S}}_{\text{nucleon}} = \frac{L_u}{2\pi C}\sqrt{1-\beta\hat{\delta}_v}$$

其中曲率算符 $\hat{\delta}_v = \bar{\delta}_v + \hat{\delta}_v^{(1)}$ 严格来自 **Regge剖分约束** + **$[\hat{X},\hat{P}]=i\hbar$**：经典背景曲率 + 位置涨落平方的量子期望 + Regge几何非线性，不是唯象假设。

**耦合常数部分**（GL(1)探针层）：

$$\hat{\mathcal{S}}_{U(1)}(\hat{u}) = \sum_p \frac{\ln p}{\sqrt{p}}\delta(\hat{u} - \ln p)$$

质数势是**投影算符的叠加**，在耦合常数空间选择 $u = \ln p$ 的离散点。

- 本征态 $\Psi_k(u) = \frac{1}{\sqrt{L_u}}e^{i\frac{2\pi n_k}{L_u}u}$（紧化U(1)基矢）
- 本征值 = 耦级 $n_k \equiv C_k = l_k(l_k+1) + 3/4$（定义），约束方程 $\frac{L_u}{2\pi C}\sqrt{1-\beta\delta_v^{(k)}} = C_k$ 锁定 $N_k$
- $C = \xi'(1)/\xi(1) \approx 0.0230957$（Riemann xi函数）
- 紧化 = $\hat{u}$ 的**谱边界条件** $\psi(u+L_u) = \psi(u)$，与核子声子态联立

### 4.3 同步算符的完整形式（含 Casimir）

$$\boxed{\hat{\mathcal{S}}_k^{\text{(full)}} = \frac{L_u}{2\pi C}\sqrt{1-\beta\hat{\delta}_v^{(k)}} \cdot \hat{\mathbb{I}}_{G_k} + \hat{C}_2(G_k)}$$

- 耦级项：U(1)紧化的同步成本（径向）
- Casimir项：$G_k$ 内部对称的同步成本（角向）
- 同步成本 $s_k = n_k + l$

## 5. 群谱与朗兰兹纲领

### 5.1 FG的完整数学对象

FG的完整数学对象是**朗兰兹纲领GL(n)各层+广义黎曼猜想（GRH）**。黎曼猜想（GL(1)）只是特例。

**正确结构**：不是GL(1)+GL(4)+GL(5)直和，而是**单个GL(5)自守表示**。GL(1)和GL(4)是其**子结构**（中心特征和$K$-type），分别贡献主量子数 $n$ 和轨道角动量 $l$。GL(4)来自 $SO(5)\subset SU(5)$ 的旋量表示 $\mathbb{C}^4$（$\dim V = 4$），非 $SU(4)$ 重组因子。

同步算符由物理约束严格确定，本征群 $R$ 是重组产物：

$$\boxed{\hat{\mathcal{S}}_{\text{atom}} = \bigoplus_{k=1}^{4} \hat{\mathcal{S}}_k^{\text{(full)}}}$$

物质自组织基态同步是SU(5)（GL(5)自守谱），重组实现后各因子层GL(n)谱是残留：

| 朗兰兹层 | L函数 | 猜想 | FG中的角色 |
|:---|:---|:---|:---|
| GL(1) | $\zeta(s)$ | RH | 电磁因子层（GL(5)中心特征） |
| GL(2) | $L(s, \pi)$ | GRH(GL2) | 模对称层 |
| GL(3) | $L(s, \pi)$ | GRH(GL3) | 色因子层 |
| GL(4) | $L(s, \pi)$ | GRH(GL4) | $SO(5)$ 旋量表示（GL(5)的$K$-type） |
| GL(5) | $L(s, \pi)$ | GRH(GL5) | 基态同步（单层自守表示） |

### 5.2 群谱的前提

$$\boxed{\text{完整同步谱} \iff \text{RH} \land \text{GRH(GL(4))} \land \text{GRH(GL(5))}}$$

- 黎曼猜想成立 → GL(1)层本征值在临界线上 → 电磁因子层谱唯一（GL(5)中心特征）
- 广义黎曼猜想成立 → 各层本征值在临界线上 → FG完整谱唯一
- **FG完整理论需要各层GRH同时成立**（数学前提，未证明）

### 5.3 GUE统计

各GL(n)层L函数零点间距 = GUE sine-kernel（Montgomery-Odlyzko推广）

$$P(s) = 1 - \left(\frac{\sin(\pi s)}{\pi s}\right)^2$$

各层零点 = 量子混沌能级（Berry图景：周期轨道 = 素数）。

### 5.4 文献锚定

| 文献 | 贡献 |
|---|---|
| Hilbert-Pólya (1914+) | 自伴算符H，本征值=黎曼零点虚部 |
| Berry-Keating (1999) [arXiv:0712.0705] | H=xp算符，semiclassical实现 |
| Connes (2019) [arXiv:1910.14368] | 缩放哈密顿量，谱实现，紧化算符 |
| Montgomery (1973) + Odlyzko | GUE统计验证 |
| Bost-Connes (1995) [arXiv:1012.4665] | Z(β)=ζ(β)量子统计系统 |
| Srednicki (2011) [arXiv:1104.1850] | Berry-Keating+局部RH谱证明 |
| Ng (2006) [arXiv:math/0603275] | Virasoro c=1/2谱实现 |
| Benjamin-Chang (2022) [arXiv:2208.02259] | CFT模共形自举包含黎曼零点 |

## 6. Regge剖分与纤维丛的对应

给定纤维丛 $(M_\ell, P_\ell, \pi_\ell, G_\ell)$，对底空间 $M_\ell$ 进行Regge剖分 $T_\ell$：

- **顶点** = $M_\ell$ 中的离散点（剖分对象的位置）
- **边** = 联络 $\mathcal{A}_\ell$ 的离散化（连接顶点的路径，给出平移规则）
- **面** = 曲率 $\mathcal{F}_\ell$ 的离散化（绕回路的和乐）

### 6.1 角亏作为底空间曲率集中

$$\delta_v = 2\pi - \sum_i \theta_i \quad \text{(Gauss-Bonnet)}$$

### 6.2 曲率量子涨落

$$\Delta\delta_0^2 = \sum_q \left|\frac{\partial \delta_v}{\partial u_q}\right|^2 \cdot \frac{\hbar}{2\omega_q}$$

其中 $\omega_q$ 是纤维上的量子谐振子本征频率（声子频率）。

## 7. 统一计算步骤

给定任意层FG的纤维丛 $(M_\ell, P_\ell, \pi_\ell, G_\ell)$，从剖分到谱的步骤完全统一：

| 步骤 | 内容 | 公式 |
|:---|:---|:---|
| A. Regge剖分 | 对底空间三角剖分 | 顶点+边+面 |
| B. 角亏 | 逐顶点曲率集中 | $\delta_v = 2\pi - \sum_i \theta_i$ |
| C. 动力学矩阵 | 联络离散化 | $D_{ij} = K_{ij}/\sqrt{m_i m_j}$ |
| D. 声子谱 | 纤维上量子谐振子 | $\omega_q = \sqrt{\text{eig}(D)}$ |
| E. 角亏涨落 | 曲率零温量子涨落 | $\Delta\delta_0^2 = \sum_q \|\partial\delta_v/\partial u_q\|^2 \cdot \hbar/(2\omega_q)$ |


每步都是CQM方程严格导出，无经验拟合参数。

## 8. 物理常数

| 常数 | 值 | 来源 |
|:---|:---|:---|
| $\beta$ | $\frac{1}{4\pi}\ln\frac{L}{a}$ | 系统尺寸严格确定 |
| $C$ | $\xi'(1)/\xi(1) \approx 0.0230957$ | Riemann xi函数 |
| $L_u$ | $\ln\Lambda$ | 耦合常数空间紧化U(1)周长 |

## 9. 纤维丛与CFT的严格对应：联络→曲率→同步→共形

**目标**：建立纤维丛结构（联络、曲率、和乐、截面）与CFT结构（Virasoro代数、共形块、OPE、primary operator）之间的严格定量映射，消除"Dirac约束=共形自举方程"仅一行陈述的缺口。

CFT一般理论见 `01 核心理论/CQM_核心_共形场论与OPE.md`。

### 9.1 截面 = primary operator

**纤维丛截面**：截面 $\psi \in \Gamma(P(M,G))$ 是底空间 $M$ 上的物理场，满足联络的协变作用 $D\psi = 0$。

**CFT primary operator**：primary operator $\phi(z)$ 是复平面上的共形场，满足Virasoro最高权条件 $\hat{L}_{n>0}\phi = 0$。

**严格对应**：

$$\boxed{\psi(x) \in \Gamma(P(M,G)) \;\longleftrightarrow\; \phi_l(z) \in \mathcal{H}_{\text{CFT}}}$$

| 纤维丛 | CFT | 对应机制 |
|:---|:---|:---|
| 底空间 $M$（Regge剖分） | 复平面 $\mathbb{C}$ | 指数映射 $z = e^{-\kappa r}$（§6.4 of CFT文档） |
| 截面 $\psi$（物理场） | primary operator $\phi_l$（壳层） | 态-算符对应 |
| 截面空间 $\Gamma$ | Hilbert空间 $\mathcal{H}$ | 所有物理态的集合 |
| 协变作用 $D\psi = 0$ | 最高权条件 $\hat{L}_{n>0}\phi = 0$ | §9.5严格证明 |
| 联络作用 $\nabla_\mu\psi$ | descendant $\hat{L}_{-1}^k\phi$ | §9.2严格对应 |

**截面的显式构造**：在A₄框架下，截面（=电子轨道态）对应于descendant态：

$$\psi_{n,l,m}(x) \;\longleftrightarrow\; \sum_{k=0}^{n-l-1} c_k^{(n,l)}\,\hat{L}_{-1}^k\,\phi_{l,m}(z)$$

其中 $c_k^{(n,l)}$ 是Shapovalov内积确定的descendant系数。

### 9.2 联络 = Virasoro生成元

**纤维丛联络**：$\mathcal{A}_\ell$ 作用于截面给出协变导数 $\nabla_\mu\psi = \partial_\mu\psi + \mathcal{A}_\mu\psi$。在A₄ Regge剖分下，联络离散化形式由 SU(5) 简单根的 SU(2) 子代数结构确定。

**Virasoro生成元**：$\hat{L}_n$ 作用于primary operator给出descendant。$\hat{L}_{-1}$ 生成descendant tower，$\hat{L}_0$ 给出共形维度。

**严格对应**：

$$\boxed{\mathcal{A}_\ell \;\longleftrightarrow\; \{\hat{L}_n\}_{n \in \mathbb{Z}}}$$

| 纤维丛联络 | Virasoro代数 | 对应机制 |
|:---|:---|:---|
| 联络 $\mathcal{A}$ | $\{\hat{L}_n\}$ | 模展开 $\mathcal{A}(z) = \sum_n \mathcal{A}_n z^{-n-1}$ |
| 离散联络 = 嘉当矩阵 | $\hat{L}_{-1}$ descendant生成 | 声子频率 → descendant level |
| 协变导数 $\nabla_\mu\psi$ | descendant $\hat{L}_{-1}^k\phi$ | 联络作用 = descendant生成 |
| 曲率 $F = d\mathcal{A} + \mathcal{A}\wedge\mathcal{A}$ | 对易子 $[\hat{L}_m, \hat{L}_n]$ | §9.3严格对应 |
| Bianchi恒等式 $dF + [\mathcal{A},F] = 0$ | Jacobi恒等式 | 代数自洽性 |

**联络的模展开**：在CFT的复坐标下，联络的模展开为：

$$\mathcal{A}(z) = \sum_{n=-\infty}^{\infty} \mathcal{A}_n\,z^{-n-1}$$

其中 $\mathcal{A}_n$ 对应Virasoro生成元 $\hat{L}_n$。联络的Kac-Moody扩展（中心项）对应Virasoro中央荷：

$$[\mathcal{A}_m, \mathcal{A}_n] = (m-n)\mathcal{A}_{m+n} + k\,m\,\delta_{m+n,0} \;\longleftrightarrow\; [\hat{L}_m, \hat{L}_n] = (m-n)\hat{L}_{m+n} + \frac{c}{12}m(m^2-1)\delta_{m+n,0}$$

左式是Kac-Moody代数（联络的仿射扩展），右式是Virasoro代数（Sugawara构造）。中央荷 $c = k\dim\mathfrak{g}/(k+h^\vee)$ 从Kac-Moody水平 $k$ 严格确定（Sugawara构造）。

### 9.3 曲率 = 对易子：Bianchi → Jacobi

**纤维丛曲率**：$F = d\mathcal{A} + \mathcal{A}\wedge\mathcal{A}$，满足Bianchi恒等式 $dF + \mathcal{A}\wedge F - F\wedge\mathcal{A} = 0$。

**Virasoro对易子**：$[\hat{L}_m, \hat{L}_n] = (m-n)\hat{L}_{m+n} + \frac{c}{12}m(m^2-1)\delta_{m+n,0}$，满足Jacobi恒等式。

**严格对应**：

$$\boxed{F = d\mathcal{A} + \mathcal{A}\wedge\mathcal{A} \;\longleftrightarrow\; [\hat{L}_m, \hat{L}_n] = (m-n)\hat{L}_{m+n} + \frac{c}{12}m(m^2-1)\delta_{m+n,0}}$$

**Bianchi → Jacobi**：

Bianchi恒等式 $dF + [\mathcal{A}, F] = 0$ 是曲率的**可积条件**——联络的二次协变导数可交换当且仅当曲率满足Bianchi。

Jacobi恒等式 $[\hat{L}_m, [\hat{L}_n, \hat{L}_p]] + \text{cyclic} = 0$ 是Virasoro代数的**自洽条件**——对易子的二次嵌套可交换。

二者在代数层面严格对应：Bianchi保证联络定义的曲率自洽，Jacobi保证Virasoro代数的对易子自洽。

**曲率本征值 → 共形维度**：

壳层标签 $l_k = k-1$ 由 SU(5) 简单根的 Dynkin 图深度严格推导。primary共形维度 $h_l = l_k$（壳层角动量），descendant共形维度 $h = n + l$（Madelung规则）。

### 9.4 和乐 = OPE monodromy：曲率 → 共形维度的定量映射

**纤维丛和乐**：绕回路 $\gamma$ 的平行移动：

$$W(\gamma) = \mathcal{P}\exp\oint_\gamma \mathcal{A} = \exp(i\delta_v\,\hat{T})$$

其中 $\delta_v$ 是回路包围的角亏（底空间曲率集中），$\hat{T}$ 是结构群生成元。

**CFT monodromy**：共形块绕 $z = 0$ 的monodromy：

$$\mathcal{F}(z\,e^{2\pi i}) = e^{2\pi i h}\,\mathcal{F}(z)$$

其中 $h$ 是共形维度。monodromy描述共形块在解析延拓下的变换行为，由BPZ方程严格确定。

**严格对应**：

$$\boxed{W(\gamma) = e^{i\delta_v\,\hat{T}} \;\longleftrightarrow\; \text{monodromy} = e^{2\pi i h}}$$

**定量映射**：和乐本征值 = monodromy本征值给出：

$$i\,\delta_v\,\hat{T} = 2\pi i\,h \quad \Longrightarrow \quad \boxed{h = \frac{\delta_v\,\hat{T}}{2\pi}}$$

**A₄系统的显式计算**：

对A₄嘉当矩阵的第 $k$ 个本征模式：
- 曲率涨落 $\delta_v^{(k)} = \frac{\hbar\omega_k}{E_{\text{bind}}}|v_k(v)|^2(N_k + \frac{1}{2})$（来自§4.0约束链，$N_k$ 为声子占据数）

- 共形维度 $h_k = \frac{\delta_v^{(k)}\,\lambda_k}{2\pi}$（$\lambda_k$ 为结构群生成元 $\hat{T}$ 的本征值）

primary共形维度 $h_l = l_k$（壳层角动量，$l_k = k-1$ 由 SU(5) Dynkin图深度严格推导），descendant共形维度 $h = n + l$（Madelung规则）。

**和乐平庸化 = 闭壳层稳定**：

和乐平庸化 $W(\gamma) = 1$（$\delta_v = 0$）对应：
- 纤维丛：平坦联络，无曲率集中
- CFT：monodromy平凡，共形块单值
- 物理：闭壳层稳定构型（稀有气体）

和乐非平庸化 $W(\gamma) \neq 1$（$\delta_v \neq 0$）对应：
- 纤维丛：曲率集中，非平坦联络
- CFT：monodromy非平凡，共形块多值
- 物理：开壳层，化学活性

### 9.5 同步算符 = CFT mode算符：同步方程 = 最高权条件

**同步算符**（§4.2-§4.3）：

$$\hat{\mathcal{S}}_k^{\text{(full)}} = \underbrace{\frac{L_u}{2\pi C}\sqrt{1-\beta\hat{\delta}_v^{(k)}}}_{\text{核子部分（径向）}} \cdot \hat{\mathbb{I}}_{G_k} + \underbrace{\hat{C}_2(G_k)}_{\text{Casimir部分（角向）}}$$

**CFT mode算符**：

$$\hat{L}_0 + \hat{C}_2(G_k) = \underbrace{\hat{L}_0}_{\text{descendant level（径向）}} + \underbrace{\hat{C}_2(G_k)}_{\text{角动量Casimir（角向）}}$$

**严格对应**：

$$\boxed{\hat{\mathcal{S}}_k^{\text{(full)}} \;\longleftrightarrow\; \hat{L}_0 + \hat{C}_2(G_k)}$$

| 同步算符 | CFT mode算符 | 对应机制 |
|:---|:---|:---|
| 核子部分 $\frac{L_u}{2\pi C}\sqrt{1-\beta\hat{\delta}_v^{(k)}}$ | $\hat{L}_0$（descendant level） | 径向量子数 $n$ |
| Casimir部分 $\hat{C}_2(G_k)$ | $\hat{C}_2(G_k)$（角动量Casimir） | 壳层角动量 $l$ |
| 本征值 = 耦级 $n_k = C_k$ | 本征值 = 共形维度 $h = n + l$ | §9.5.1严格推导 |
| 同步方程 $\hat{\mathcal{S}}\Psi = n\Psi$ | 最高权条件 $\hat{L}_0\phi = h\phi$ | §9.5.2严格对应 |

#### 9.5.1 耦级 → 共形维度的严格推导

同步算符本征值（耦级）：

$$n_k = C_k = l_k(l_k+1) + \frac{3}{4}$$

CFT mode算符本征值（共形维度）：

$$h = h_{\text{primary}} + n_{\text{desc}} = l_k + n$$

其中 $n$ 是descendant level（主量子数），$l_k$ 是primary共形维度（角动量）。

**二者的关系**：

同步算符的Casimir部分给出primary共形维度 $h_l = l_k$（壳层结构），核子部分给出descendant level $n$（径向量子数）。完整同步算符的本征值对应于总共形维度：

$$\hat{\mathcal{S}}_k^{\text{(full)}}\,\Psi_{n,l} = \underbrace{(n + l_k)}_{\text{共形维度 } h}\,\Psi_{n,l} + \underbrace{\frac{3}{4}}_{\text{自旋部分}}\,\Psi_{n,l}$$

自旋部分 $s(s+1) = 3/4$（$s = 1/2$）分离后，轨道共形维度 $h = n + l$ 严格对应Madelung规则。

#### 9.5.2 同步方程 = 最高权条件

**同步方程**：

$$\hat{\mathcal{S}}_k\,\Psi_k = n_k\,\Psi_k$$

物理意义：约束（核子量子振荡 + 曲率涨落 + 耦合常数涨落）联立求解，选出离散的同步本征态。

**CFT最高权条件**：

$$\hat{L}_0\,\phi = h\,\phi, \quad \hat{L}_{n>0}\,\phi = 0$$

物理意义：primary operator是Virasoro代数的最高权表示，descendant由 $\hat{L}_{-n}$ 生成。

**严格对应**：

$$\boxed{\hat{\mathcal{S}}_k\,\Psi_k = n_k\,\Psi_k \;\longleftrightarrow\; \hat{L}_0\,\phi = h\,\phi}$$

- 同步方程选出离散本征态 $\Psi_k$（耦级 $n_k$） → 最高权条件选出primary $\phi$（共形维度 $h$）
- 紧化U(1)边界条件 $\psi(u + L_u) = \psi(u)$ → Kac-Moody代数的可积表示条件（水平 $k$ 为正整数）
- 约束方程锁定声子占据数 $N_k$ → fusion rules锁定允许的descendant level $n \geq l + 1$

### 9.6 Dirac约束 = 共形自举方程：严格证明

**纤维丛Dirac约束**：

$$D\psi = 0 \quad \text{（协变作用为零）}$$

其中 $D = \gamma^\mu \nabla_\mu$ 是Dirac算符，$\nabla_\mu = \partial_\mu + \mathcal{A}_\mu$ 是协变导数。

物理意义：截面在联络作用下"无加速"——物理场满足规范约束。

**CFT共形自举方程**：

$$\sum_p C_{ij}^p\,C_{pk}^m = \sum_p C_{jk}^p\,C_{ip}^m \quad \text{（OPE结合律）}$$

物理意义：OPE的配对顺序不影响结果——共形场论的代数自洽性。

**严格对应**：

$$\boxed{D\psi = 0 \;\longleftrightarrow\; \text{OPE结合律（共形自举方程）}}$$

**证明链条**：

1. **Dirac约束 → 截面的协变作用为零**：$D\psi = 0$ 意味着截面 $\psi$ 在联络 $\mathcal{A}$ 的作用下"无源"——物理场是联络的**零模**。

2. **零模 → primary operator**：在CFT对应下，联络的零模对应于Virasoro代数的最高权态（primary operator）——$\hat{L}_{n>0}\phi = 0$ 是"无源"条件的CFT表述。

3. **primary的OPE → 结合律**：primary operator的OPE $\phi_i \times \phi_j = \sum_p C_{ij}^p \phi_p$ 必须满足结合律（配对顺序不影响结果），否则OPE不自洽。

4. **结合律 → 共形自举方程**：OPE结合律就是共形自举方程——代数自洽性条件。

5. **可积条件 → Bianchi = Jacobi**：Dirac约束的可积条件 $[D, D] = F$（曲率）对应OPE结合律的相容条件——Bianchi恒等式 = Jacobi恒等式（§9.3）。

$$\boxed{D\psi = 0 \;\xrightarrow{\text{零模}}\; \hat{L}_{n>0}\phi = 0 \;\xrightarrow{\text{OPE}}\; \text{结合律} \;\xrightarrow{\text{自洽}}\; \text{共形自举方程}}$$

**A₄具体化**：$A_4$结合律方程的解恰好锁定s,p,d,f四种模式，禁戒g。这是Dirac约束=共形自举方程在CQM中的具体实例——壳层标签 $l_k = k-1$ 由 SU(5) Dynkin图深度严格推导，第5个（g）的约束方程无解。

### 9.7 同步算符 = 紧化算符：三层关系统一

同步算符=紧化算符在三个层次有不同表述，此处统一说明：

| 层次 | 文档 | 定义 | 物理意义 |
|:---|:---|:---|:---|
| **QG层**（基态定义） | CNST §4 | $\hat{\mathcal{S}}_0: \mathcal{H}_{\text{auto}}(\text{GL}_5) \to \mathcal{H}_{\text{phys}}(\text{SU}(5))$ | 紧化投影：GL(5)自守形式 → SU(5)物理表示 |
| **FG纤维丛层**（截面实现） | 本文 §4 | $\hat{\mathcal{S}}_\ell$ = 紧化算符在层级截面空间 $\Gamma(P_\ell)$ 的实现 | 谱算符：给出群谱 $G_k$ |
| **FG核心层**（因子再现） | FG核心 §4.4 | $\hat{\mathcal{S}}_{\text{FG}}$ = QG紧化结构在电磁因子层GL(1)的再现 | 物理可观测的耦合常数 $g_k$ |

**层次关系**：

$$\underbrace{\hat{\mathcal{S}}_0}_{\text{QG层：GL(5)\to SU(5)}} \;\xrightarrow{\text{SU(5)重组实现}}\; \underbrace{\hat{\mathcal{S}}_\ell}_{\text{FG纤维丛层：截面空间}} \;\xrightarrow{\text{取GL(1)因子}}\; \underbrace{\hat{\mathcal{S}}_{\text{FG}}}_{\text{FG核心层：电磁因子}}$$

- **QG层**：紧化投影 $\hat{\mathcal{S}}_0$ 将非紧GL(5)自守形式投影到紧SU(5)表示。自伴性 $\Leftrightarrow$ 紧化约束可解 $\Leftrightarrow$ 各层L函数零点在临界线上（GRH）。
- **FG纤维丛层**：SU(5)经重组实现，$A_4$ 根系 $\to U(1)\times SU(2)\times SU(3)$，紧化算符下放到每层纤维丛的截面空间 $\Gamma(P_\ell)$，实现为 $\hat{\mathcal{S}}_\ell = \frac{L_u}{2\pi C}\sqrt{1-\beta\hat{\delta}_v^{(\ell)}}$。
- **FG核心层**：取GL(1)电磁因子层，紧化算符再现为 $\hat{u}$ 的谱边界条件 $\psi(u+L_u) = \psi(u)$（紧化U(1)玻尔-索末菲量子化），给出物理可观测的耦合常数 $g_k$。

**与CFT的对应**（§9.5）：三层同步算符均对应CFT的mode算符 $\hat{L}_0 + \hat{C}_2$，但所处层级不同——QG层对应GL(5) Kac-Moody代数，FG纤维丛层对应SU(2) Kac-Moody代数（重组实现后），FG核心层对应U(1)自由玻色子（GL(1)因子）。

### 9.8 完整对应表

| 纤维丛结构 | CFT结构 | 对应机制 | 严格性 |
|:---|:---|:---|:---|
| 截面 $\psi$ | primary operator $\phi$ | 态-算符对应 | §9.1 |
| 联络 $\mathcal{A}$ | Virasoro $\{\hat{L}_n\}$ | 模展开 | §9.2 |
| 曲率 $F$ | 对易子 $[\hat{L}_m, \hat{L}_n]$ | $F=d\mathcal{A}+\mathcal{A}\wedge\mathcal{A}$ | §9.3 |
| Bianchi恒等式 | Jacobi恒等式 | 代数自洽性 | §9.3 |
| 和乐 $W(\gamma)$ | monodromy $e^{2\pi ih}$ | $h = \delta_v\hat{T}/(2\pi)$ | §9.4 |
| 同步算符 $\hat{\mathcal{S}}$ | mode算符 $\hat{L}_0 + \hat{C}_2$ | 本征值=共形维度 | §9.5 |
| 同步方程 $\hat{\mathcal{S}}\Psi = n\Psi$ | 最高权条件 $\hat{L}_0\phi = h\phi$ | 约束→离散谱 | §9.5 |
| Dirac约束 $D\psi = 0$ | 共形自举方程（OPE结合律） | 零模→primary→结合律 | §9.6 |
| 紧化算符 | CFT mode算符 | 三层统一 | §9.7 |
| 和乐平庸化 | 闭壳层稳定 | $\delta_v = 0 \Leftrightarrow$ 稀有气体 | §9.4 |

### 9.9 局域分析足够性原理

**问题**：底空间 $M_\ell$ 上有大量Regge顶点 $\{v\}$，每个顶点有不同的曲率涨落态 $\hat{\delta}_v|0\rangle$。为什么只需要取**一个**能体现底空间分布性质的代表性局域来分析，即可得到整个纤维丛的同步谱？

**回答**：CFT算符插入生成局域态，但同步算符是整体定义的——其本征值谱由代数结构固定，不依赖于插入点。因此局域分析足够。

#### 9.10.1 数学表述

**CFT算符插入生成态**（态-算符对应，§9.1）：

$$\mathcal{O}(z)|0\rangle = |\mathcal{O}(z)\rangle$$

在CQM中，局域算符是曲率算符 $\hat{\delta}_v$，插入到Regge顶点 $v$ 生成局域态：

$$\hat{\delta}_v |0\rangle = |\delta_v\rangle$$

**同步算符的普适性**（§9.5, §9.7）：

$$\hat{\mathcal{S}}_k = \frac{L_u}{2\pi C}\sqrt{1-\beta\hat{\delta}_v^{(k)}}$$

同步算符 $\hat{\mathcal{S}}_k$ 的本征值谱 $\{n_k\}$ 由 SU(5) 简单根的 Dynkin 图深度严格推导（$l_k = k-1$）：

- 本征群 $\{R_k\}$、角动量 $\{l_k = k-1\}$、容量 $\{N_k^{\max} = 2(2l_k+1)\}$ 均由 SU(5) 简单根的 Dynkin 图深度严格推导

**关键点**：本征值谱 $\{n_k\}$ **不依赖于具体的插入顶点 $v$**，只依赖于代数结构。

#### 9.10.2 物理图像

| 层面 | 局域 | 整体 |
|:---|:---|:---|
| **态** | 每个顶点 $v$ 有不同的曲率涨落态 $\|\delta_v\rangle$（离散态多） | 所有态遵守同一套同步方程 $\hat{\mathcal{S}}\Psi = n\Psi$ |
| **算符** | 曲率算符 $\hat{\delta}_v$ 是局域的（定义在单个顶点） | 同步算符 $\hat{\mathcal{S}}$ 是整体的（定义在整个截面空间 $\Gamma(P_\ell)$） |
| **谱** | 局域态携带顶点的曲率信息 | 同步本征值 $\{n_k\}$ 由 SU(5) Dynkin图深度严格推导（$l_k = k-1$），与顶点无关 |
| **CFT对应** | 算符插入 $\mathcal{O}(z)\|0\rangle$ 生成局域态 | OPE系数 $C_{ij}^k$ 由共形对称性固定，不依赖插入点 $z$ |

#### 9.10.3 严格论证

**命题**：取一个能体现底空间分布性质的代表性局域 $v^*$（如质子A₄的平坦顶点 $\bar{\delta}_{v^*}=0$，或中子的背景曲率顶点 $\bar{\delta}_{v^*}\neq 0$），分析其同步谱 $\hat{\mathcal{S}}\Psi_{v^*} = n\Psi_{v^*}$，结果普适于整个纤维丛。

**证明**：

1. **所有顶点共享同一代数结构**：Regge剖分的每个4-单纯形共享同一个 $A_4$ 嘉当矩阵（§6, §18.1）。嘉当矩阵是联络的离散化，由4-单纯形的组合几何确定，与顶点位置无关。

2. **同步算符的本征值由代数结构决定**：$\hat{\mathcal{S}}_k$ 的本征值 $n_k = C_k = l_k(l_k+1) + 3/4$，其中 $l_k = k-1$ 由 SU(5) 简单根的 Dynkin 图深度严格推导（§9.5.1）。本征值不依赖于具体的顶点 $v$。

3. **CFT OPE系数的普适性**：OPE $\mathcal{O}_i(z)\mathcal{O}_j(0) \sim \sum_k C_{ij}^k z^{h_k-h_i-h_j}\mathcal{O}_k(0)$ 中，系数 $C_{ij}^k$ 由共形对称性（Kac-Moody代数 + Virasoro代数）固定，不依赖于插入点 $z$（§9.5, CFT核心文档§3）。

4. **局域态→整体谱**：在代表性顶点 $v^*$ 插入算符 $\hat{\delta}_{v^*}$ 生成局域态 $|\delta_{v^*}\rangle$，用同步算符 $\hat{\mathcal{S}}$ 分析得到本征值谱 $\{n_k\}$。由于步骤1-3，任何其他顶点 $v'$ 的分析给出相同的本征值谱。$\square$

#### 9.10.4 与CFT自举的关系

CFT共形自举（OPE结合律 = 共形自洽，§9.6）的普适性是局域分析足够性的代数基础：

- **共形自举方程** $\sum_p C_{ij}^p C_{pk}^q = \sum_p C_{jk}^p C_{ip}^q$（结合律）不依赖插入点
- **解空间**由代数结构（$A_4$ 嘉当矩阵 + Kac-Moody代数）固定
- 因此，在一个点解自举方程，解普适于整个共形场

**总结**：

$$\boxed{\text{局域算符插入} + \text{整体同步规则（同一代数结构）} = \text{局域分析足够}}$$

底空间上离散态虽多，但都遵守同一套同步算符 $\hat{\mathcal{S}}$ 和同步方程 $\hat{\mathcal{S}}\Psi = n\Psi$。取一个体现底空间分布性质的代表性局域，分析其同步谱，结果由 $A_4$ 代数结构统一给出，普适于整个纤维丛。

### 9.10 相关文档

- `FG_核心理论.md`：FG物理机制层（同步算符比丛作用量更根本的论证、SU(5)重组实现→A₄→4耦合常数→α）
- `01 核心理论/CQM_核心_共形场论与OPE.md`：CFT一般理论（OPE、共形自举、Kac-Moody代数、共形块、指数映射与合流极限）
- `01 核心理论/CQM_核心_因果网络同步理论.md`：因果网络同步理论（QG层紧化算符定义、黎曼结构→CNST七条提取、三种引力同步诠释）
