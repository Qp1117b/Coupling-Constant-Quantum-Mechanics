# CQM 稳定文档：平面二维晶格超导——从位置-动量到固有时流速差异的历史总和的拉通链条


---

## 〇、全链条总览

$$
[\hat X,\hat P]=i\hbar
\xrightarrow{\ \text{①}\ }\hat a_k\ (\text{声子})
\xrightarrow{\ \text{②}\ }\varepsilon_e,\ L\ (\text{亏角/图拉普拉斯})
\xrightarrow{\ \text{③}\ }\Delta\hat\varepsilon\ (\text{亏角涨落})
$$

$$
\xrightarrow{\ \text{④}\ }v_\tau,\ A_\tau\ (\text{固有时流速/相变锚核})
\xrightarrow{\ \text{⑤}\ }u_G\ (\text{全局耦合})
\xrightarrow{\ \text{⑥}\ }\sigma_v^2,\ \Gamma_n\ (\text{方差/去相干})
\xrightarrow{\ \text{⑦}\ }K(t)\ (\text{记忆核})
\xrightarrow{\ \text{⑧}\ }\mathcal I_K(t)=\int K\,dt\ (\text{全对历史测度的体现})
\quad(\text{止于⑧；相变方程与 }T_c\text{ 未推、暂时未定}).
$$

> **两条次序**：①–⑧ 是**推导次序**（$A_\tau$ 在环节④作为零亏角子复形定义）；相变的**层级**是「必要条件 L1–L3（不同刻度，不排箭头）→ 相变 → 锚（空间侧体现）→ 共享 $K$ → RH」。④ 的 $A_\tau$ 是几何候选集，相变锚的显现（占据集 $\mathcal A(T)$）以相变后局域刚度过阈为前提（`06 超导` §0.0）。

| 环节  | 输入 → 输出                     | 核心内容                                                   | 严格性         |
| :-: | :-------------------------- | :----------------------------------------------------- | :---------- |
|  ①  | 正则对易 → 声子                   | 简正变换、声子算符、位置涨落；稳定性判据                                   | 【严格】不依赖模式来源 |
|  ②  | 一般晶格 → 亏角、$L$               | Delaunay 二面角、铰链亏角、cot 拉普拉斯；尺度不变性                       | 【几何严格＋构造】   |
|  ③  | 声子 → 亏角涨落                   | 链规则 (E5)、二阶矩 (E6)、W-3′、温度 (E7)                         | 【条件严格】      |
|  ④  | 亏角 → 固有时流速                  | FG 接口、比值传递、闭环单值性、漂移定理 T1、锚 $A_\tau$                    | 【假设＋代数严格】   |
|  ⑤  | 流速 → 全局耦合                   | DNR 逐点不对易、子群跃迁、品质因数 T3                                 | 【构造假设＋代数严格】 |
|  ⑥  | 涨落 → 方差、去相干                 | $\sigma_v^2$、OU 扩散、$\Gamma_n$、两种退相干律、可读窗口              | 【文档显式＋构造】   |
|  ⑦  | 去相干 → 记忆核                   | $K(t)$ 计数定义、谱侧、两族零点、四阶段、占据–读出                          | 【文档显式＋构造】   |
|  ⑧  | 记忆核 → 记忆核积分（全对历史测度的体现） | $\mathcal I_K(t)=\int K\,dt$、Kramers–Kronig、DM.18 历史深度 | 【外部＋构造】     |
|  ⑨（未推、暂时未定，已从链条删除）  | 相变方程／$T_c$（候选目标）      | 两阶段、BKT/3D-XY、渗流乘子、软模等价（候选，未推）                | 【未推、暂时未定】   |

固有时流速差异的历史总和是全对族 $\mathsf H(t)=(\mathcal H_{ij}(t))_{i,j\in V_t}$，在环节④形成；环节⑧的 $\mathcal I_K(t)=\int_0^tKdt'$ 是它在**记忆侧的读数**（经节点对测度 $\mu_t$），不是它本身。两族零点分工贯穿下游：**平凡零点** $\zeta(-n)=0$（$n=2,4,6,\ldots$）管电子配对（$T^*$）与电荷密度结构；**非平凡零点** $\rho=\tfrac12+i\gamma$ 管相变（$T_\theta$）。外参量：**压强垂直作用于上下两个面**，经声子改涨落（配对支）；**静态电磁场从上方进入一个面**，经和乐相位改刚度（相变支）。

---

## 一、环节①：位置-动量 → 声子（严格段）

**输入**：顶点正则对易

$$[\hat X_v,\hat P_{v'}]=i\hbar\,\delta_{vv'}\qquad(\text{声子理论 §1.2}),$$

$v$ 标记 Regge 复形顶点或晶格位点；式本身不依赖几何来源。

**推导**（三步，仅用对易子线性性，与模式来源无关）。

**第一步：简正变换保持对易子。** 取实正交归一简正变换 $U$（$M\times N$，$UU^{\mathsf T}=I$）：

$$\hat Q_k=\sum_vU_{kv}\hat X_v,\qquad \hat\Pi_k=\sum_vU_{kv}\hat P_v .$$

则

$$[\hat Q_k,\hat\Pi_{k'}]=\sum_{v,v'}U_{kv}U_{k'v'}[\hat X_v,\hat P_{v'}]=i\hbar\sum_vU_{kv}U_{k'v}=i\hbar(UU^{\mathsf T})_{kk'}=i\hbar\delta_{kk'}.$$

**第二步：声子算符保持玻色对易。**

$$\hat a_k=\sqrt{\frac{m\omega_k}{2\hbar}}\hat Q_k+i\sqrt{\frac{1}{2m\hbar\omega_k}}\hat\Pi_k
\ \Rightarrow\ [\hat a_k,\hat a_{k'}^\dagger]=\delta_{kk'},\quad [\hat a_k,\hat a_{k'}]=0 .$$

**第三步：逆变换重建位置涨落。**

$$\hat Q_k=\sqrt{\frac{\hbar}{2m\omega_k}}\bigl(\hat a_k+\hat a_k^\dagger\bigr)
\ \Longrightarrow\ \Delta\hat X_v=\sum_kU_{kv}\sqrt{\frac{\hbar}{2m\omega_k}}\bigl(\hat a_k+\hat a_k^\dagger\bigr).$$

**输出**：声子算符与玻色对易关系。【严格】——三步不依赖 $U$、$\omega_k$ 的来源。

**数值检验**（一般正交 $U$，非 $A_4$；$6\times4$ 正交部分，QR 分解，Fock 截断）：

| 检验项 | 结果 | 判定 |
|:---|:---|:---|
| $UU^{\mathsf T}$ 偏离 $I_4$ | $4.4\times10^{-16}$ | 机器精度成立 |
| 单点 $[\hat X,\hat P]=i\hbar$ 对角 | $i$（截断层内） | 严格成立 |
| $[\hat a_1,\hat a_1^\dagger]$ 对角 | $1$ | 严格成立 |
| $[\hat a_1,\hat a_2^\dagger]$ 最大元 | $0$ | 严格成立 |

**稳定性判据**：$\omega_k^2>0$ 给有界震荡 $e^{\pm i\omega_k t}$（稳定）；$\omega_k^2<0$ 给指数发散（结构失稳）。由 $\omega_k^2\propto L$ 的本征值（环节②），

$$\text{声子}=\text{稳定震荡}\iff L\ \text{半正定}\iff\omega_k^2\ge0 .$$

$L$ 的零模（1 个）是平移/规范模；正模是稳定声子；负模属结构相变/重构，不属稳定声子。三晶格数值（BCC-Nb、FCC-Al、HCP-Tc）的 $L$ 谱均为「0 负模 / 1 零模 / 其余正模」，都是稳定声子基底。

**关键区分**：「必震荡」（位置-动量不确定给出零点振幅）与「稳定」（亏角曲率的 $L$ 谱符号）是两个独立条件；骨架此前只给了前者。

**层级**：晶格 ≠ $A_4$。晶格声子的 $U$ 来自一般晶格动力学矩阵（力常数矩阵），$A_4=\mathrm{Cartan}(\mathrm{SU}(5))$ 是核子层/禁闭边界的代数结构；二者同享「正则对易 → 简正模式 → 量子化」的代数骨架，但物理载体与来源不同。严格段 (E1)–(E3) 对此中性；$U$ 来源归材料依赖（缺口 B），频率谱归 W-3。

> 来源：稳定稿环节①；声子理论 §1–§2；原位置-动量→声子严格段稿、声子稳定性判据稿（已并入本节）。

---

## 二、环节②：一般晶格几何剖分 → 亏角与 cot 拉普拉斯

**输入**：真实 3D 晶格（BCC/FCC/HCP），非 $A_4$ 二维结构。

**推导**：

1. **底空间**：$\mathcal R=(V,E,T,\{\bar L_{ij}\})$，$V$ 为原子位置，$T$ 为 Delaunay 四面体化给出的 3D 单形集合，$E$ 为铰链（边）。
2. **二面角**：四面体沿铰链 $e$ 的二面角 $\theta_e^T$ 由面法向夹角给出（等价于余弦定律）。
3. **铰链亏角**（曲率载体，共维 2，挂在**节点之间**的边上）：

$$\varepsilon_e=2\pi-\sum_{T\supset e}\theta_e^{T}.$$

4. **cot 权重拉普拉斯**（Regge 二阶变分矩阵的几何实现）：

$$L_{ij}\big|_{i\ne j}=-\frac12\sum_{T\supset e_{ij}}\cot\theta_{e_{ij}}^{T},\qquad
L_{ii}=+\sum_{j\ne i}w_{ij},$$

其中 $w_{ij}=-L_{ij}\big|_{i\ne j}$。由

$$f^{\mathsf T}Lf=\frac12\sum_{i,j}w_{ij}\bigl(f_i-f_j\bigr)^2\ge0$$

（$w_{ij}\ge0$ 时）得 $L$ 的图拉普拉斯四性质：对称、零行和、半正定、单一零模（连通分量数为 1）。

**数值检验**：

| 晶格 | 原子数 | 四面体数 | $L$ 对称偏差 | 零行和 | 最小特征值 | 零模数 | 第一激发 $\lambda_1$ | 非零亏角铰链 |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| BCC-Nb | 54 | 213 | 0 | $2.9\times10^{-11}$ | $-8.6\times10^{-12}$ | 1 | 8.04 | 84 |
| FCC-Al | 108 | 506 | 0 | $1.0\times10^{-10}$ | $-8.1\times10^{-12}$ | 1 | 7.68 | 102 |
| HCP-Tc | 54 | 224 | 0 | $3.7\times10^{-11}$ | $6.3\times10^{-12}$ | 1 | 11.50 | 78 |

**输出**：$L$ 满足图拉普拉斯四性质；$L$ 的本征向量＝简正模式 $U$，本征值＝$\omega_k^2$ 的几何来源（比例系数属 W-3）。一般晶格剖分确实产生非空曲率载体 $\varepsilon_e$。

**尺度不变性**（Euler 齐次定理）：二面角由边长之**比**决定，是零次齐次函数，故

$$\varepsilon_e(\{\lambda l_k\})=\varepsilon_e(\{l_k\})\quad\forall\lambda>0 .$$

对 $\lambda$ 求导并在 $\lambda=1$ 取值：

$$\sum_k\frac{\partial\varepsilon_e}{\partial\ln l_k}=0,\qquad A_{ek}\equiv\frac{\partial\varepsilon_e}{\partial\ln l_k}.$$

三条推论：

- **C1**：各向同性呼吸（热膨胀、静水压）**严格不产生**亏角涨落；
- **C2**：只有形变（剪切成变、光学模）耦合；
- **C3**：旧「顶点角亏」公式的 $C^2/L^2$ 结构不可移植到铰链亏角（后者只含形状，不含整体尺度）。

**严格性**：亏角【几何严格】；$|\cot|$ 稳健化【构造选择】（钝角二面角不保证全为锐角）；「$L$ 本征值＝$\omega_k^2$」比例系数属 W-3。

> 来源：稳定稿环节②；`geom2.py` 数值自检（$\sum_kA_{ek}=0$ 到 $10^{-9}$）；原一般晶格几何剖分稿、主线稿 §二尺度不变性（已并入本节）。

---

## 三、环节③：声子 → 亏角涨落（E5–E7）

**输入**：环节①的声子算符与环节②的 $L$。

**推导**：

**第一步：位置涨落进入边长。** 边 $e=(v_i,v_j)$ 的切向单位向量 $\hat t_e$，

$$\Delta\hat l_e=\bigl(\Delta\hat X_{v_i}-\Delta\hat X_{v_j}\bigr)\cdot\hat t_e .$$

**第二步：链规则给亏角涨落。**

$$\Delta\hat\varepsilon_e=\sum_{e'}\frac{\partial\varepsilon_e}{\partial l_{e'}}\,\Delta\hat l_{e'} .$$

**第三步：代入声子展开得二阶矩。** 把 (E3) 代入 (E5)，边分辨时 $U_{kv}$ 取两端点之差 $(U_{kv_i}-U_{kv_j})$（含极化时取沿边切向的投影），得

$$\langle(\Delta\varepsilon_e)^2\rangle=\sum_k\Bigl(\frac{\partial\varepsilon_e}{\partial l}\Bigr)^2U_{kv}^2\,\frac{\hbar}{m\omega_k}\Bigl(n_k+\frac12\Bigr)
\ \xrightarrow{n_k=0}\ \Delta\varepsilon_{0,e}^2 .$$

这是声子与亏角的定量接口：真空涨落幅度 $\Delta\varepsilon_0$，温度经 $n_k$ 进入。

**形变张量形式（W-3′）**：取 06 的键长涨落 $\langle\delta l_k^2\rangle=\frac{3\hbar}{4\omega_D}\bigl(\frac1{m_i}+\frac1{m_j}\bigr)(1-f)$，并设不同键的涨落不相关：

$$\Delta\varepsilon_{0,e}^2=\frac{3\hbar(1-f)}{4\omega_D}\sum_{k\in T(e)}\frac{A_{ek}^2}{l_k^2}\Bigl(\frac1{m_i}+\frac1{m_j}\Bigr).$$

与旧式相比：长度尺度统一为键长 $l_k$；系数由单一数 $C^2$ 变为张量缩并 $\sum_kA_{ek}^2$，且 $\sum_kA_{ek}=0$；各向同性呼吸贡献严格为零（C1）。

**与 01/FG 曲率算符式的口径核对（P4）**：01 声子理论 §3.1 的曲率涨落算符式与 FG §4.0 的同一式，标注互斥（前者【构造】、后者【严格推导】）。从环节①的严格段核对：位置涨落平方的单模式期望 $\propto1/\omega_k$，而该式 $\propto\omega_k$，依赖相反，不能直接相等。两者对接需 Regge 二阶映射系数 $c/L^2$ 与标度关系

$$\omega_k^2=\frac{c\,E_{\rm bind}}{mL^2}\tag{★}$$

这两个环节均未导出；取核子质量、$E_{\rm bind}\sim{\rm MeV}$、$L\sim1\,{\rm fm}$、$c\sim1$ 时量级自洽。故 01 §3.1 的【构造】标注更准确，FG §4.0 的【严格推导】缺乏导出支撑；本文的 E5–E7 链不依赖该式，缺口仍归 W-3。

**温度（E7）**：

$$\Delta\varepsilon(T)=\Delta\varepsilon_0\sqrt{\tanh\frac{\hbar\Omega_0}{2k_BT}},\qquad \omega_k^2=c_0\,\lambda_k(L).$$

$\lambda_k(L)$ 是 $L$ 的本征值，$c_0$ 为频率标度系数（待推 W-3）。$\omega_D$ 为 Debye 频率；E7 的 $\Omega_0$ 与 $\omega_D$ 的识别属 M4（未证）。

**输出**：带温度依赖的亏角涨落 $\Delta\varepsilon(T)$ 与真空幅度 $\Delta\varepsilon_0$。

**严格性**：(E5)【条件严格，给定 $\partial\varepsilon/\partial l$】；(E6)【结构严格，$c_0$ 与 $\partial\varepsilon/\partial l$ 待推 W-3】；(E7)【条件严格，06 既有】；W-3′【本文推导＋构造：键间不相关】。

> 来源：稳定稿环节③；原声子-亏角方程组稿 (E1)–(E7)、W-3′ 与主线稿 §二形式结果（已并入本节）。

---

## 四、环节④：亏角 → 固有时流速（FG 接口、乘积传递、闭环、漂移定理）

**输入**：环节③的边亏角 $\ell_{ij}\equiv\varepsilon_{ij}$（06 §7.3 记号）。

**推导**：

**第一步：FG 接口**（【假设】，FG_核心理论 §3.1）：

$$\frac{d\tau}{dt}=v_\tau=\sqrt{1-\frac{\varepsilon}{2\pi}} .$$

**第二步：比值传递。** 亏角挂在节点之间的铰链上，两两节点之间唯一一条边＝一个亏角。沿相邻节点按比值传递：

$$v_{\tau,j}=v_{\tau,i}\,r_{ij},\qquad r_{ij}=\sqrt{1-\frac{\ell_{ij}}{2\pi}} .$$

沿路径累乘给两点流速之比：$v_{\tau,j}/v_{\tau,i}=\prod_{\text{路径}}r$——乘积关系，不是加和。参考节点流速 $v_o$ 是**变量**（固定为 c-数会与 $[\hat u_G,v_\tau^{(j)}]=i☯/N$ 矛盾，环节⑤）。

**第三步：一阶展开。** 在 $\ell\ll2\pi$ 下

$$r_{ij}\simeq1-\frac{\ell_{ij}}{4\pi},\qquad
v_{\tau,j}-v_{\tau,i}=v_{\tau,i}\bigl(r_{ij}-1\bigr)\simeq-\frac{\ell_{ij}}{4\pi}\quad(v_{\tau,i}\simeq1).$$

故 $\Delta v_\tau\equiv v_{\tau,j}-v_{\tau,i}\simeq-\ell_{ij}/(4\pi)$。

**第四步：闭环单值性。** 一维闭环首尾同一节点，同一节点流速唯一：

$$\prod_{k=1}^{N}r_k=1 .$$

这是「闭环拓扑＋比值传递」的自然结果，非预设。Delaunay 亏角非负，故 $r_k\le1$，一般 $\prod_kr_k<1$（绕环衰减）；严格满足需鞍形铰链（$\varepsilon<0$）正负抵消。BCC 三角最小环的数值核查给 $\prod_kr_k=0.177/0.707/0.500$，三例无一自动满足。逐跳传递在环上一般不一致：三晶格数值核查中，60 条非树亏角边里 54 条的传递比偏离 1 超过 0.05（中位 0.23）。这不是数值误差，而是绕环和乐 $\mathcal H$（06 §10.1 的相位阻挫）在流速侧的几何对应——沿不同路径传递流速的差异即和乐；和乐相位与流速实数乘积不是同一对象，二者定量关系仍属 G19。涨落一阶只给 $\sum_k\Delta\varepsilon_k=0$（绕环和为零），不给出「彼此相等」，是必要而非充分条件。

**第五步：漂移定理 T1。** 模式 $n$ 在节点 $i$ 的时钟相位

$$\Phi_{n,i}(t)=\gamma_n\tau_i(t),\qquad \tau_i=\int_0^t v_{\tau,i}\,dt' .$$

相对相位

$$\Phi_{n,i}-\Phi_{n,j}=\gamma_n\int_0^t\bigl(v_{\tau,i}-v_{\tau,j}\bigr)dt' .$$

记**全对固有时流速差异的历史总和**

$$\mathsf H(t)=\bigl(\mathcal H_{ij}(t)\bigr)_{i,j\in V_t},\qquad
\mathcal H_{ij}(t)\equiv\int_0^t\bigl(v_{\tau,i}(t')-v_{\tau,j}(t')\bigr)dt'=\tau_i-\tau_j,$$

则 $\Phi_{n,i}-\Phi_{n,j}=\gamma_n\mathcal H_{ij}$，且 $\mathcal H_{ii}=0$、$\mathcal H_{ij}=-\mathcal H_{ji}$、$\mathcal H_{ij}+\mathcal H_{jk}=\mathcal H_{ik}$。这个**全对族**是链条上的**本体对象**：由流速差异本身累积而成，不经过记忆核；$\binom{N}{2}$ 个分量只有 $N-1$ 个独立，故"所有节点对"不是逐对相加，而是族及其投影 $\mathcal D=\frac{2}{N-1}\sum_i(\tau_i-\bar\tau)^2$（推导链环 6）。

按边定向 $i\to j$ 记 $\ell_{ij}\ge0$，一阶展开给 $v_{\tau,i}-v_{\tau,j}\simeq+\ell_{ij}/(4\pi)$。对时间求导，并写成与定向无关的漂移率：

$$\frac{d}{dt}\bigl(\Phi_{n,i}-\Phi_{n,j}\bigr)=\frac{\gamma_n}{4\pi}\ell_{ij}+O(\ell^2),
\qquad
\Gamma^{\rm drift}_{ij}\equiv\Bigl|\overline{\frac{d}{dt}\bigl(\Phi_{n,i}-\Phi_{n,j}\bigr)}\Bigr|=\frac{\gamma_n}{4\pi}\bigl|\ell^{(0)}_{ij}\bigr|.$$

符号随边的定向；判据只用到零性，故与定向无关。因 $\gamma_n>0$，

在确定性（平均）意义上

$$\overline{\frac{d}{dt}\bigl(\Phi_{n,i}-\Phi_{n,j}\bigr)}=0\iff\ell^{(0)}_{ij}=0 .$$

完整相位差还叠加环节⑥的扩散：锚固定的是均值，涨落仍在。

**相变锚核 $A_\tau$**：零亏角边的极大连通子图（同步即零漂移；核与温度无关，相变锚的定义见 `06 超导` §7.3）：

$$A_\tau:\quad \ell_e=0\ (\forall e\subset A_\tau),\quad \text{极大连通},\quad |A_\tau|\ge2,\quad d=\dim A_\tau\in\{1,2\}.$$

同步是节点之间的关系，单点不能与自己同步，故**无 0 维锚**。锚的读数是「相位差冻结」（等速），不是「相位相同」；这是冻结判据，真而平凡（`临-4`）、不判超导（推导链环 20.2）。锚固定均值，涨落仍在（锚内并非「无差异」）。

**环上三种结局**：整环 $\ell=0$ 给整环锚（$d=1$）；含零边给 1 维弧锚；全非零则无锚。一维开链有节点间边亏角但无闭环反馈、无边界约束，故无锚（§4.1），流速差无法锁定。

**同步是几率事件**：因 $v=\sqrt{1-\varepsilon/2\pi}$ 对自变量单调，

$$\text{所有 }v_\tau^{(i)}\text{ 相等}\iff\text{所有 }\Delta\varepsilon_i\text{ 相等}.$$

温度降低时，和乐相位关联长度增大（§10.1），提高同步几率。06 §7.3「$\Delta\varepsilon\to0$（低温）」与 §11.2 的低温极限冲突，本文按 §11.2 读取（低温 $\Delta\varepsilon$ 最大）；因此低温提高同步几率只经关联长度，不读成「涨落趋零」。2D 中「相位精确相等」在任意 $T>0$ 都不成立（Mermin–Wagner），故锚只能读成「零漂移」，不能读成「零涨落」。

**锚是相变的体现**：相变发生→相位差冻结→零亏角边极大连通子图 $A_\tau$ 显现，故锚是相变在空间侧的读出、不是相变的前提。渗流只给全局连通域与刚度乘子（L2，不独立触发相变）；相变由刚度判据（$\Upsilon(T_c)=\Upsilon_c$）界定，锚作为体现随后显现；时序为相变前无真锚、相变中可多局域锚、理论研究取单锚。

**输出**：固有时流速场 $v_\tau$、漂移定理 T1、相变锚核 $A_\tau$。

**严格性**：FG 接口【假设】；乘积递推【模型实现】；单值性/单调性【严格】；T1【代数改写】；同步几率依赖涨落模型【构造】。

> 来源：稳定稿环节④、⑥；06 §7.3；相变锚判据稿 T1、§四；记忆核计数稿 §10–§12；原声子亏角固有时流速全局耦合链稿（U4 和乐，已并入本节）。

---

## 五、环节⑤：固有时流速 → 全局耦合（DNR、群跃迁、品质因数）

**输入**：环节④的逐节点固有时流速 $v_\tau^{(i)}$。

**推导**：

**第一步：单节点胚**（【构造假设，待 E4】；04 前沿 §6.3）：

$$[\hat u_i,\hat p_{u,j}]=i\delta_{ij},\qquad p_{u,i}=\frac{v_\tau^{(i)}}{☯},\qquad \hat u_G=\frac1N\sum_i\hat u_i .$$

**第二步：逐点不对易（定义）。** 仅用对易子线性性：

$$[\hat u_G,v_\tau^{(j)}]=\frac{☯}{N}\sum_i[\hat u_i,\hat p_{u,j}]=\frac{i\,☯}{N}\neq0\qquad(\forall j).$$

每个节点都「感知」全局耦合涨落。$N=1$ 退化为 $i☯$；逐点下界 $\Delta u_G\Delta v_\tau^{(j)}\ge☯/(2N)$ 随 $N$ 减弱。

**第三步：总和形式（附加假设）。** 若集体动量取算术和 $\hat p_{u,G}=\sum_i\hat p_{u,i}$ 且节点间对易子严格对角，则

$$\Bigl[\hat u_G,\sum_i v_\tau^{(i)}\Bigr]=i☯,\qquad
\Delta u_G\cdot\Delta\Bigl(\sum_i v_\tau^{(i)}\Bigr)\ge\frac{☯}{2}.$$

A12（$\sum_{i\ne j}C_{ij}=0$）与总和形式在附加假设下是同一代数事实；逐点关系是定义，总和形式不作定义使用。

**第三步附：A12 的代数推导（D1–D4）**：记 $M_{ij}=[\hat u_i,\hat p_{u,j}]/i$，则 $M_{ii}=1$、$M_{ij}=C_{ij}$（$i\ne j$）。DNR 左边为

$$\Bigl[\hat u_G,\sum_jv_\tau^{(j)}\Bigr]=\frac{i☯}{N}\sum_{i,j}M_{ij}=\frac{i☯}{N}\Bigl(N+\sum_{i\ne j}C_{ij}\Bigr).$$

令其等于 $i☯$ 得

$$\sum_{i\ne j}C_{ij}=0\qquad(\text{A12}).$$

反向代入即得总和形式。故 A12 与 DNR 在附加假设下是同一代数事实的两种表述，A12 不是独立假设。$C_{ij}$ 的厄米性由对易子厄米共轭反号推出（$[\hat u_i,\hat p_{u,j}]^\dagger=-[\hat u_i,\hat p_{u,j}]$）；反对称性 $C_{ij}=-C_{ji}$ 需 $f$ 奇，属【构造】。

**第四步：子群跃迁（群论）。** $\hat u_G$ 是全局 $U(1)$ 耦合涨落的约束，$U(1)//\mathbb Z_n$ 子群跃迁（$n=2,4,6,\ldots$）：

$$\Delta u_n=2\ln n\quad\Longleftrightarrow\quad \alpha\to n^2\alpha .$$

$n=2$ 库珀对（$\alpha\to4\alpha$）、$n=4$ 四电子凝聚、$n=6$ 六电子凝聚。谱的形式闭合：$u_{G,n}=\ln\alpha^{-1}+2\ln n$。

**第五步：品质因数定理 T3。** 由 DM.5 与 DM.9：

$$\bigl\langle(\delta C_{ij})^2\bigr\rangle=\kappa_f^2\bigl\langle(\Delta\varepsilon_i-\Delta\varepsilon_j)^2\bigr\rangle=2\kappa_f^2\sigma_\ell^2(1-f),$$

$$J_{ij}=J_0\,\frac{\langle(\delta C_{ij})^2\rangle}{\langle(\delta C)^2\rangle_{\rm ref}}\cos\mathcal H_{ij}
=J_0\,\frac{2\kappa_f^2\sigma_\ell^2(1-f)}{\langle(\delta C)^2\rangle_{\rm ref}}\cos\mathcal H_{ij}.$$

由环节⑥的相对相位扩散率

$$\Gamma^{\rm link}_{ij}=\frac{\gamma_n^2\tau_g}{8\pi^2}\sigma_\ell^2(1-f)=2(1-f)\Gamma_n,$$

两式相除，$\sigma_\ell^2(1-f)$ 完全抵消：

$$\Gamma^{\rm link}_{ij}=\mathcal R_n\,J_{ij},\qquad
\mathcal R_n=\frac{\gamma_n^2\tau_g\,\bigl\langle(\delta C)^2\bigr\rangle_{\rm ref}}{16\pi^2\kappa_f^2J_0\cos\mathcal H_{ij}}.$$

$\mathcal R_n$ 与 $T$、$\sigma_\ell$、$f$ 都无关；在本材料内它只经 $\cos\mathcal H_{ij}$ 依赖边指标。

**推论 K1（不能「用几何换相干」）**：降低 $J$ 必然同步降低 $\Gamma^{\rm link}$，不存在「做弱耦合获长相干」的自由度；键的相干品质因数 $Q_n=1/\mathcal R_n$ 是材料与模式的常数。

**推论 K2（排除「锚在 $T_c$ 变稳」）**：任何形如 $\Gamma^{\rm link}(T)<\Gamma_c$ 或 $\Gamma^{\rm link}(T)<J(T)$ 的率型判据，代入 T3 后与 $T$ 无关，不能定义 $T_c$。温度驱动的相变只能来自「能量型量 vs $k_BT$」（相位支）或「计数跨越阈值」（渗流支），不能来自「率型量 vs 率型量」。

**锚不进刚度（关键分工）**：由 06 §4，静态亏角 $\varepsilon^{(0)}$ 只进时钟，涨落部分 $\Delta\varepsilon$ 只进差异方差（DM.5）。因此：

| 物理量 | 由什么决定 | $A_\tau$ 是否影响 |
|:---|:---|:---:|
| 相对相位漂移率 $\gamma_n\ell^{(0)}/(4\pi)$ | 静态亏角 $\ell^{(0)}$ | **是**（唯一入口） |
| 相位刚度 $\Upsilon\propto J\propto\sigma_\ell^2(1-f)$ | 涨落部分 $\Delta\varepsilon$ | 否 |
| 关联指数 $\eta=k_BT/(2\pi\Upsilon)$ | 同上＋$T$ | 否 |
| 配对强度 $\langle(\delta C_{ij})^2\rangle$ | 涨落部分 $\Delta\varepsilon$ | 否 |

在现有形式化下，$A_\tau$ 只进「时钟漂移」，不进 $J$、$\Upsilon$、$\eta$、配对。它不是配对与相干的载体，只是「频差为零」的条件。

**边界**：$u=\ln g$ 与 $p_u=v_\tau/☯$ 正则共轭——**不从 $v_\tau$ 臆造 $\alpha$**；DNR 构造性待 E4。

**输出**：全局耦合约束、子群跃迁谱、品质因数 T3、锚-刚度分工表。

**严格性**：代数严格（条件于胚）；DNR 构造性待 E4；$u_i$ 量子化绝对值属 W-3（谱已形式闭合）。

> 来源：04 前沿 §6.3；稳定稿环节⑤；相变锚判据稿 T3、§3.4、§四；06 §8–§9；原逐节点不对易稿、差异代数内生推导稿（A12 证明，已并入本节）。

---

## 六、环节⑥：涨落 → 方差 → 去相干（σ_v、Γ_n）

**输入**：环节④的流速涨落与环节③的 $\Delta\varepsilon$。

**推导**：

**第一步：方差的文档定义。** 06 §0.6 环节⑥显式：

$$\sigma_v^2=\mathrm{Var}\bigl[\Delta v_\tau\bigr],$$

$\tau_g$ 为 $\Delta v_\tau$ 的相关时间（与 $\delta\ell$ 的关联时间是同一符号）。

**第二步：与亏角方差的换算。** 由 $\Delta v_\tau\simeq-\Delta\varepsilon/(4\pi)$：

$$\sigma_v^2\simeq\frac{\sigma_\ell^2}{16\pi^2},\qquad \sigma_\ell^2(T)=\Delta\varepsilon(T)^2 .$$

这一步是线性化代数；把 $\sigma_v^2$ 与空间 $\sigma_\ell^2/(16\pi^2)$ 等同需要各态历经假设（06 未写，标【构造】）。

**第三步：OU 扩散给 $\Gamma_n$。** 模式相位差 $\Delta\Phi_n=\gamma_n\int\delta v\,dt'$，设 $\delta v$ 为 Ornstein–Uhlenbeck 过程：

$$\langle\delta v(t)\delta v(0)\rangle=\sigma_v^2e^{-|t|/\tau_g},$$

则

$$\mathrm{Var}\bigl[\Delta\Phi_n(t)\bigr]
=\gamma_n^2\int_0^t\!\!\int_0^t\langle\delta v(t_1)\delta v(t_2)\rangle\,dt_1dt_2
\xrightarrow{\ t\gg\tau_g\ }2\gamma_n^2\sigma_v^2\tau_g\,t\equiv2\Gamma_n t .$$

故

$$\Gamma_n=\gamma_n^2\sigma_v^2\tau_g .$$

这是 06 §0.6 环节⑥的单节点-单模式去相干率；相对相位的 $\Gamma^{\rm link}_{ij}=2(1-f)\Gamma_n$ 见环节⑤。

**第四步：可读窗口。** 06 §0.6 环节⑥：

$$\gamma_n\sigma_v\sqrt{\tau_g}\ll\sqrt{\frac{\langle v_\tau\rangle}{2}} .$$

窗口内低阶零点可读，高阶零点先被抹掉。首次穿过 $|\Delta\Phi|=\pi$ 的时间 $t_*\simeq\pi^2/(2\Gamma^{\rm link})$。

**第五步：两种退相干律（形状可判据）。** 记忆核计数稿 §12.4：

| 机制 | 相干因子 $C_n(t)$ | 形状 |
|:---|:---|:---|
| 静态不均匀（冻结的 $\varepsilon^{(0)}$ 使 $v$ 有空间散布 $\sigma_v$） | $e^{-\gamma_n^2\sigma_v^2t^2/2}$ | 高斯（非均匀展宽） |
| 动态涨落（声子，OU，相关时间 $\tau_g$） | $e^{-\gamma_n^2\sigma_v^2\tau_g t}$ | 指数（均匀展宽，即 $\Gamma_n$） |

交接时间 $\sim\tau_g$：短时由静态无序主导（高斯），长时被运动窄化（指数）。两者 $\gamma^2$ 标度相同。数值对照（$\gamma_1=14.13$、$\sigma_v=0.01$、$\tau_g=1$）：

| $t$ | 0.5 | 1 | 2 | 5 | 10 | 20 | 30 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 静态（高斯） | 0.998 | 0.990 | 0.961 | 0.779 | 0.368 | 0.018 | $1\times10^{-4}$ |
| 动态（指数） | 0.990 | 0.980 | 0.961 | 0.905 | 0.819 | 0.671 | 0.549 |

两曲线在 $t=2\tau_g$ 相交。长时间端静态无序比声子狠三个量级——估计「可读窗口」必须用静态支，只用声子支会高估范围。

**第六步：谱丰富度。** 由窗口定义 $\gamma_*=\sqrt{\langle v_\tau\rangle/(2\sigma_v^2\tau_g)}$：

$$N_{\rm eff}\simeq\frac{\gamma_*\ln\gamma_*}{2\pi}.$$

数值：$\sigma_v=0.005,0.010,0.020,0.050,0.100$ 对应 $N_{\rm eff}=90,39,16,4.7,1.7$。这给出「谱在什么噪声范围内可读」的定量刻度。

**温度方向注**：06 §7.3「$\Delta\varepsilon\to0$（低温）」与 §11.1–§11.2 的低温极限 $\Delta\varepsilon\to\Delta\varepsilon_0$（最大）记号冲突；本文一律按 §11.2 读取（低温 $\Delta\varepsilon$ 最大），该冲突属记号问题，不修改原文。

**输出**：涨落强度 $\sigma_v$ 与每模去相干率 $\Gamma_n$。

**严格性**：$\sigma_v^2$ 定义【文档显式】；线性化/各态历经【构造】；$\Gamma_n$【文档显式】；两种退相干律【代数改写＋构造】；$N_{\rm eff}$【构造】。

> 来源：06 §0.6 环节⑥；相变锚判据稿 T2、§3.4；记忆核计数稿 §四–§五、§12.4。

---

## 七、环节⑦：去相干 → 记忆核 K(t)

**输入**：环节⑥的 $\Gamma_n$ 与零点谱 $\{\gamma_n\}$。

**推导**：

**第一步：超导态计数定义**（06 §0.0/§0.6，【构造：记忆＝以参考点为基的计数减光滑主项】；正常态 $K$ 非质数形式）：

$$K(t)=e^{-t/2}\bigl(\psi(e^t)-e^t\bigr),\qquad \psi(x)=\sum_{p^m\le x}\ln p .$$

**第二步：谱侧。** 由显式公式：

$$K(t)=-\sum_\rho\frac{e^{(\rho-\frac12)t}}{\rho}+O(e^{-t/2}).$$

每个零点 $\rho=\sigma+i\gamma$ 给一个模式：$\sigma=\frac12$ 纯振荡 $e^{i\gamma t}$；$\sigma>\frac12$ 以 $e^{(\sigma-\frac12)t}$ 抬起。RH 下每模是纯振荡，节奏 $\pi/\gamma_1$。

**第三步：稳定性判据（不是 $T_c$ 判据）。**

$$\sigma\equiv\frac12\ \bigl(\text{零点全共线}\bigr)\iff\forall\varepsilon>0:\ K(t)=O(e^{\varepsilon t}),$$

RH 下更强的 von Koch 界 $K(t)=O(t^2)$。「各模式等速率衰减、记忆不散」$\iff$ RH。这只是稳定性判据；相变方程与 $T_c$ 未推、暂时未定（环节⑨已从链条删除）。

**第四步：两族零点分工。** 平凡零点 $s=-2m$（$m=1,2,\ldots$）在实轴、无虚部，贡献纯衰减 $e^{(-2m-\frac12)t}$，给不出 $e^{i\gamma t}$ 节奏——**只能进配对支，不能进相变支**。非平凡零点 $\rho=\frac12+i\gamma$ 给节奏与本征值交叉——**只能进相变支**。记忆核的谱侧只对非平凡零点求和。

**第五步：有限温度。** 06 §0.6 环节⑥：重标定 $\tau(t)=\int_0^tv_\tau dt'$ 把公共衰减率由 $\frac12$ 换成 $\langle v_\tau\rangle/2$，并给每个模式加去相干率 $\Gamma_n$。RH 下：

$$K_T(t)\approx e^{-\langle v_\tau\rangle t/2}\sum_n\frac{e^{-\Gamma_n t}}{\rho_n}e^{i\gamma_n t}.$$

这是链条上的「截面」形式：每个零点模式被乘上 $e^{-\Gamma_n t}$；高阶模式先被抹掉，可读窗口由环节⑥给。

**第六步：四阶段（06 §0.6，【构造】）。**

| 阶段 | 温度 | 记忆核行为 | 锚点 |
|:---|:---|:---|:---|
| 自由变化 | $T\gg T^*$ | 振荡/衰减/拍频（无全局趋势） | 无 |
| 赝能隙 | $T^*>T>T_c$ | 弛豫到中间平台 $K^{\rm mid}$ | 预形成 |
| 相变 | $T=T_c$ | 临界值 $K^{\rm crit}$ | 出现 |
| 偏离 | $T<T_c$ | 稳定平台 $K^{\rm SC}$ + 慢偏离 | 锁定 |

正常态不是「衰退」，是「自由变化」；超导态不是「衰退」，是「偏离」（围绕锚点的涨落）；赝能隙是「锚点的预形成」。四阶段边界未精确。

**第七步：空间锚与记忆侧平台的关系（占据–读出）。** 空间锚 $A_\tau$ 由静态几何定，与 $T$ 无关；记忆侧平台 $K^{\rm SC}$ 随 $T$ 变——两者是**两个对象**，不能读成「同一事件的不同读法」。可计算的关系是占据–读出：

$$A_\tau\ \xrightarrow{\ \text{占据}\ }\ \mathcal A(t)\subseteq A_\tau\ \xrightarrow{\ \text{读出}\ }\ K^{\rm SC}.$$

相变锚判据稿 §10.4 已给出因果链：横向 Hessian 正定 ⇔ 锚稳定；若锚落在鞍点，涨落沿降向逃逸，记忆核平台 $K^{\rm SC}$ 缓慢漂移。$A_\tau$ 与 $K^{\rm SC}$ 的同一性属 M9，未证；占据/渗流提案亦未证。

**第八步：FDT 统一（外部标准物理）。** 阻尼谐振子 $m(\ddot x+\omega_0^2x)+\eta\dot x=f(t)$ 的不动点 $x_0$（势阱极小＝边界）与关联函数 $C_{xx}(t)\propto e^{-\Gamma t}\cos\omega_0t$（震荡＝截面）由 FDT 统一（Rutgers L14 式 9.5；Ingold §4.4 式 4.74）：

$$S(\omega)=2\hbar\bigl[1+n_B(\omega)\bigr]\chi''(\omega)\quad\Longleftrightarrow\quad \text{涨落关联＝响应/耗散}.$$

映射：环节④的 $x=\Delta v_\tau$ 的不动点 $x_0$ ↔ 动力学边界；关联 $C(t)$ ↔ 记忆核 $K(t)$。这里的「边界」是动力学不动点，**不自动等于空间锚 $A_\tau$**；二者之间的识别仍属 M9 的占据–读出映射。FDT 统一的是「震荡–边界」这一随机动力学对象的两面，不是把 $A_\tau$ 与 $K^{\rm SC}$ 读成同一物。

**输出**：记忆核截面 $K(t)$（含有限温度去相干）。

**严格性**：$K(t)$ 定义【构造】；谱侧【文档显式】；RH 判据【文档显式＋外部标准】；四阶段【构造】；占据–读出【文档显式＋本文推导】；FDT【外部】。

> 来源：06 §0.6–§0.7；记忆核计数稿 §11–§12；锚与记忆核关联稿；相变锚判据稿 §10.4–§10.5；稳定稿环节⑦。

---

## 八、环节⑧：记忆核积分——固有时流速差异历史总和的体现

**输入**：环节④的固有时流速差异 $v_{\tau,i}-v_{\tau,j}$（固有时流速差异历史总和的本体）；环节⑦的 $K(t)$（记忆核）。

**推导**：

**第一步：定义全对固有时流速差异的历史总和（回顾环节④）。** 当前同步域 $V_t$ 上，节点 $i,j$ 的固有时流速差异在时间上的累积构成全对族

$$\mathsf H(t)=\bigl(\mathcal H_{ij}(t)\bigr)_{i,j\in V_t},\qquad \mathcal H_{ij}(t)\equiv\int_0^t\bigl(v_{\tau,i}(t')-v_{\tau,j}(t')\bigr)dt'=\tau_i-\tau_j .$$

环节④ T1 已给出 $\Phi_{n,i}-\Phi_{n,j}=\gamma_n\mathcal H_{ij}$。这个**全对族**由流速差异本身累积而成，是**本体对象**，不经过记忆核；其投影为 $\mathcal D=\frac{2}{N-1}\sum_i(\tau_i-\bar\tau)^2$，三项平衡 $\dot{\mathcal D}=\mathcal B+\frac{\dot M_t}{M_t}(\mathcal D_{\rm new}-\mathcal D)$ 分开生产／平均／扩大（推导链 (6.4)–(6.7)）。

**第二步：记忆核积分是体现，不是本体。** 定义记忆核的时间积分

$$\mathcal I_K(t)\equiv\int_0^tK(t')\,dt' .$$

$\mathcal I_K(t)$ 是全对历史 $\mathsf H$ 经节点对测度 $\mu_t$ 在**记忆侧的体现/读数**：它把这一历史映射为记忆核的累积截面，**不是**历史总和本身。二者之间是体现/识别关系，不是数值相等；具体映射未证（属识别层，不作同一性宣称）。因此不能写 $\mathcal I_K=\mathcal H_{ij}$，也不能把 $\mathcal I_K$ 直接称为历史总和。

**第三步：与静态响应的关系（Kramers–Kronig，【外部·标准物理】）。** 若 $K(t)$ 是线性响应的记忆核（【外部】识别，不是 CQM 已证的同一性），则响应函数

$$\chi(\omega)=\int_0^\infty K(t)e^{i\omega t}dt,\qquad
\lim_{t\to\infty}\mathcal I_K(t)=\int_0^\infty K(t')\,dt'=\chi(\omega\to0).$$

这是 $\mathcal I_K$ 在响应侧的另一种体现；与第二步的记忆侧体现不是同一性。故 $\mathcal I_K$ 的长时间极限体现为静态响应率 $\chi(0)$，但不能说 $\mathcal I_K$ 直接就是 $\chi(0)$，也不能说它直接就是某个 $\mathcal H_{ij}$ 或全对族 $\mathsf H$。

**第四步：与 06 历史深度 DM.18 的关系。**

$$D=\underbrace{\frac{1}{t_0}\int_0^{t_0}K(t)\,dt}_{\text{时间深度}}+\underbrace{\frac{\mathcal C_\delta}{\mathcal C_0}}_{\text{结构深度}}.\tag{DM.18}$$

【构造】。$t_0,\mathcal C_0$ 是参考时间与参考复杂度，未定；式只补齐量纲，不改变「双重来源」的读法。时间深度项是记忆核积分的归一化截断；结构深度项是额外的几何/复杂度贡献。本文用 $\mathsf H=(\mathcal H_{ij})_{i,j\in V_t}$ 记全对固有时流速差异的历史总和，用 $\mathcal I_K$ 记记忆核的时间积分，用 $D$ 记 DM.18 的历史深度，三者不混同。

**第五步：术语边界（防止与 DNR 的「历史总和」混用）。** 04 前沿 §6.3 的「节点间的历史总和」指分布式不对易的总和形式 $[\hat u_G,\sum_i v_\tau^{(i)}]=i☯$（节点间不可被单点共时变量吸收）；本文的**全对固有时流速差异的历史总和**是 $\mathsf H=(\mathcal H_{ij})_{i,j\in V_t}$，$\mathcal H_{ij}=\int(v_{\tau,i}-v_{\tau,j})dt'$，其记忆侧体现是 $\mathcal I_K$。两者不是同一对象，不能互相替代。

**第六步：$K$ 贯穿两态，与相变的分工。** $K$ 在两态都存在：正常态自由变化、超导态因锚内全对冻结取等高不等位平台 $K^{\rm SC}$（单一平台需全对 $c_{ij}=0$）；$\mathcal I_K$ 与 $K^{\rm SC}$ 平台是记忆侧读数；$T_c$ 是刚度/软模事件。$D_c$ 在本框架内未定义——记忆核积分不是独立的 $T_c$ 判据；它只是全对历史总和的体现，不是全对历史总和本身，也不是相变本身。

**输出**：全对固有时流速差异的历史总和 $\mathsf H(t)=(\mathcal H_{ij}(t))_{i,j\in V_t}$ 及投影 $\mathcal D$、$\hat\mu_t$、$R_n$；其记忆侧体现 $\mathcal I_K(t)$；其响应侧体现 $\chi(0)$；DM.18 的历史深度 $D$。

**严格性**：$\mathcal H_{ij}$ 与 $\mathsf H$ 定义【代数】；$\mathcal D$、$\hat\mu_t$、$R_n$ 的恒等式【代数】；$\mathcal I_K$ 定义【代数】；$\mathcal I_K$ 与 $\mathsf H$ 的体现/识别关系【未证，不作同一性】；Kramers–Kronig 与 $\chi(0)$ 的识别【外部·标准物理】；DM.18【构造】；$D_c$ 未定【缺口】。

> 来源：06 §0.6（DM.18）；稳定稿环节⑧；04 前沿 §6.3（术语边界）；环节④ T1（$\mathcal H_{ij}$ 的定义）。

---

## 九、环节⑨（未推、暂时未定，已从链条删除）：相变方程与 T_c 的候选目标（两阶段、刚度、软模）

**输入**：记忆核积分 $\mathcal I_K(t)$（固有时流速差异历史总和的记忆侧体现）、相位刚度 $\Upsilon(T)$、配对幅度。

$\mathcal I_K(t)$ 是固有时流速差异历史总和的记忆侧体现，**不直接给 $T_c$**，也不能直接当作序参量或相变判据；$T_c$ 由相位刚度条件（或等价的软模条件）给出。$K$ 贯穿正常态与超导态、给记忆侧的可观测读数，为相变提供记忆侧伴随量；它不是固有时流速差异的历史总和本身，也不是相变方程本身。

**推导**：

**第一步：两个事件，先分开。**

| 事件 | 方程 | 变的量 | 记号 |
|:---|:---|:---|:---|
| 配对 | DM.6–DM.8 自洽 $k_BT=1.13\hbar\omega e^{-1/\lambda(T)}$ | 幅度 $\Delta$ 从零变非零 | $T^*$ |
| 相干 | DM.9–DM.13，$\Upsilon(T_c)=\Upsilon_c$ | 刚度从零变正 | $T_c$ |

平凡零点管配对支（选择定则 $n=2,4,6,\ldots$、电荷量子 $\Phi_n=h/(ne)$）；非平凡零点管相变支（节奏 $\pi/\gamma_1$、本征值交叉 $\lambda_2(T_c)=\lambda_1(T_c)$）。两族零点**不交汇**：$T_c=\min$ 是取小，不是同一。

**第二步：刚度粗粒化。** 由 DM.1 的 XY 能，对 $\varphi_i-\varphi_j\ll1$ 展开：

$$\mathcal E_\varphi=\sum_{\langle ij\rangle}J_{ij}\bigl[1-\tfrac12(\varphi_i-\varphi_j)^2\bigr]
\to\frac12\sum_{\langle ij\rangle}J_{ij}\bigl(\mathbf r_{ij}\cdot\nabla\varphi\bigr)^2 .$$

各向同性格子上与连续式 $\frac12\int d^2x\,\Upsilon|\nabla\varphi|^2$ 比对：

$$\Upsilon=\frac{1}{2A}\sum_{\langle ij\rangle}J_{ij}\,r_{ij}^2 .$$

方格校验：$\mathcal N_b=2N$、$r=a$、$A=Na^2$，得 $\Upsilon=J$，与标准结果一致。一般格子 $\Upsilon=\frac{z}{4}J_0\langle w\rangle\cos\mathcal H\,\tau(T)$（$z$ 为配位数）。

**第三步：图样冻结（T4）。** 由 $\Delta\varepsilon(T)=\Delta\varepsilon_0\sqrt{\tau(T)}$、$\tau(T)=\tanh(\theta_D/2T)$，代入 DM.5 与 DM.9：

$$\bigl\langle(\delta C_{ij})^2\bigr\rangle(T)=\bigl\langle(\delta C_{ij})^2\bigr\rangle^{(0)}\tau(T),\qquad
J_{ij}(T)=J_{ij}^{(0)}\tau(T).$$

空间图样 $J_{ij}^{(0)}$ 与温度无关，温度只做整体重标度。故 $\Upsilon(T)=\Upsilon_0\tau(T)$；任何形如 $J_{ij}(T)\gtrless k_BT$ 的占据判据自动单调。

**第四步：BKT/3D-XY 判据。**

单层 2D（BKT，Nelson–Kosterlitz）：

$$\Upsilon(T_{\rm BKT})=\frac{2k_BT_{\rm BKT}}{\pi}.$$

3D 堆叠（DM.10）：

$$k_BT_\theta=2.2017\,J_{\rm eff}.$$

**单调性与唯一性**：$T$ 降低 → $\tau$ 增大 → $\Upsilon$ 增大；同时 $2k_BT/\pi$ 线性下降。一个升、一个降，唯一交点。3D 支同理（$\tau$ 严格单调减、$\tau(\infty)=0$）。

**合成**：

$$T_c=\min\{T^*,\ T_{\rm BKT},\ T_\theta\},\qquad \Delta T_{\rm pg}=T^*-T_c .$$

- 配对限制（$T^*<T_{\rm BKT},T_\theta$）：$T_c=T^*$，$\Delta T_{\rm pg}=0$，BCS 型；
- 相位限制（$T_{\rm BKT}$ 或 $T_\theta<T^*$）：$T_c=T_{\rm BKT}$ 或 $T_\theta$，$\Delta T_{\rm pg}>0$，相位限制型；
- 渗流不独立定义 $T_c$（见第五步）。

**第五步：渗流的正确角色（定义域/乘子，不是独立 $T_c$）。**

DM.12 的对象是配对格点比例 $p_{\rm pair}$（座渗流），跨阈只给连通域、不作独立 $T_c$（M8）。闭环判据另用激活边比例 $p_{\rm loop}$（键渗流）：

$$p_{\rm loop}(T)=\Pr\bigl[S_C<4\pi\epsilon\bigr]\approx\Phi\Bigl(\frac{4\pi\epsilon-m_C}{\sigma_\ell(T)\sqrt{|C|}}\Bigr).$$

$m_C>0$ 使条件成为**左尾**事件：$T$ 降低 → $\sigma_\ell$ 增大 → 左尾变肥 → $p_{\rm loop}$ 单调升，饱和于 $1/2$。饱和值与键渗流阈值比较：2D 方格 $p_c=1/2$（恰好临界，单层不能渗流）；3D 简立方 $p_c\approx0.249$（可以渗流）。这给「单层必须靠层间耦合进入 3D」的结构性理由。

渗流**先建立全局连通域、不在刚度上**：锚在该域中判定同步一致性；若 $[r]=0$ 且 $A_\tau$ 连通，则存在全局单值 $v_\tau$，各处锚共用同一参考系；否则跨越环产生参考系错配。DM.11 的 $p(T)^t$ 只作刚度乘子，移动 $T_{\rm BKT}$，不作独立 $T_c$。

**第六步：软模等价（【外部·标准物理】）。** 连续相变的序参量势曲率在 $T_c$ 软化到零（Schwabl–Täuber, cond-mat/9607028；Jussieu 相变讲义）：

$$\omega_0^2(T_c)=\frac{V''(A_\tau,T_c)}{m}=0 .$$

$\omega_0^2\to0$ 时关联时间 $\tau$ 发散（临界慢化），$\xi\simeq\tau^{1/z}$。这与刚度判据 $\Upsilon(T_c)=\Upsilon_c$ 描述**同一临界点**的两种标准读法：一个读势曲率，一个读相位刚度。CQM 内可算的是刚度条件；势 $V$ 的微观定义仍属缺口。软模方程给出的是同一事件的等价格式，不是独立于两阶段框架的第三个 $T_c$。

**第七步：记忆核积分在何处进入。** $\mathcal I_K(t)$ 与 $K^{\rm SC}$ 平台是记忆侧的伴随**体现**：$T>T_c$ 无平台、$T<T_c$ 有稳定平台；平台值随 $\sigma_v$（温度）变化。$T_c$ 的位置由刚度/软模条件定，不由 $\mathcal I_K$ 的某个临界值 $D_c$ 定（$D_c$ 未定义）。因此链条的终点关系是：

$$\text{记忆侧体现}\ \mathcal I_K(t),K^{\rm SC}\ \longleftrightarrow\ \text{刚度条件}\ \Upsilon(T_c)=\Upsilon_c\ \longleftrightarrow\ T_c ,$$

而不是把 $\mathcal I_K$ 的某个阈值直接当作相变。

**输出**：$T_c=\min\{T^*,T_{\rm BKT},T_\theta\}$；记忆侧伴随读数。

**严格性**：两阶段/零点分工【文档显式】；BKT/3D-XY/软模【外部标准物理】；T4/粗粒化【代数改写＋构造】；渗流乘子【提案，M8 未证】；$D_c$、$V$ 微观定义【缺口】。

> 来源：06 §0.5、DM.9–DM.13、§11.6；相变锚判据稿 §5.1、§5.4、§9.3、§11.1–§11.2；记忆核计数稿 §四；稳定稿结论；外部 BKT/3D-XY/软模标准物理；T4 与 $\Upsilon$ 粗粒化（原主线稿 §三–§四形式结果，已并入本节）。

---

## 十、严格性总表与缺口清单

| 环节 | 核心结论 | 严格性 | 主要缺口 |
|:---:|:---|:---|:---|
| ① | 声子严格段、稳定判据 | 【严格】 | $U$/$\omega_k$ 来源（B、W-3） |
| ② | 一般晶格 $L$＝图拉普拉斯 | 【几何严格＋构造】 | $\lvert\cot\rvert$ 稳健化、频率比例系数 |
| ③ | E1–E7、W-3′ | 【严格＋条件严格】 | $c_0$、$\partial\varepsilon/\partial l$（W-3） |
| ④ | FG 接口、乘积递推、闭环、T1、$A_\tau$ | 【假设＋代数严格】 | FG 假设、$v_o$ 一维不定 |
| ⑤ | DNR 逐节点不对易、T3 | 【代数严格】条件于胚 | E4、$u_i$ 量子化 W-3 |
| ⑥ | $\sigma_v^2$、$\Gamma_n$、两种退相干律 | 【文档显式＋构造】 | 各态历经假设、静态支标定 |
| ⑦ | $K(t)$、谱侧、四阶段、占据–读出 | 【文档显式＋构造】 | 空间锚—记忆侧映射（M9）、$K^{\rm SC}$ 微观定义 |
| ⑧ | 记忆核积分 $\mathcal I_K$（固有时流速差异历史总和的体现）、$\chi(0)$、DM.18 | 【外部＋构造】 | $\mathcal I_K$ 与 $\mathcal H_{ij}$ 的映射未证、$K$ 作为响应核的识别、$t_0,\mathcal C_0$ |
| ⑨ | 两阶段、BKT/3D-XY、渗流乘子、软模 | 【外部＋文档显式】 | $D_c$、$V$ 微观定义、M1、M7/G19、M8 |

**未闭合缺口清单**（按原文，不得升级）：

- **W-3**：定量 $T_c$、$\Delta\varepsilon_0$ 计算链、$c_0$、$\partial\varepsilon/\partial l$、$u_i$ 量子化；
- **G10/G19**：闭环条件函数动力学形式、和乐相位容差标定；
- **E4**：DNR 构造相容性；
- **M1**：时钟相位＝超导相位（识别未证）；
- **M2/M3/M4**：配对通道/态密度/频率三步识别；
- **M8**：渗流等价性（本文按「定义域/乘子」读，不独立定 $T_c$）；
- **M9／空间锚—记忆侧映射**：$A_\tau$ 与 $K^{\rm SC}$ 的同一性未证；占据/渗流提案未证；
- **固有时流速差异的历史总和—记忆核积分**：$\mathcal I_K$ 是 $\mathcal H_{ij}$ 的记忆侧体现，具体映射未证；不得写成 $\mathcal I_K=\mathcal H_{ij}$；
- **M7**：和乐与非高斯识别；
- **Z2**：CQM 属无量纲普适类理论，绝对 $T_c$ 能标外生（$J_0/\theta_D$），给结构关系不给绝对数值；
- **命题 Z（数论）**：$\zeta$ 零点无量纲；平凡零点管配对选择定则、非平凡零点管相变——分工是结构对应，不是物理同一；**R30**：振幅-深度不同构，不能推广为振幅物理同一；
- **判据 ①（已排除）**：曾被单质元素第一性检验排除（检验记录），不进入本链；本链的 $T_c$ 终点为两阶段＋刚度/软模。

---

## 十一、两族零点的分工（下游贯穿）

| | 平凡零点 $\zeta(-n)=0$（$n=2,4,6,\ldots$） | 非平凡零点 $\rho=\tfrac12+i\gamma$ |
|:---|:---|:---|
| 物理事件 | **电子配对**（$T^*$，幅度层） | **相变**（$T_\theta$，相位层） |
| 进入方程 | DM.6–DM.8（$\lambda,N_i(0),\Phi_n,T^*$） | DM.9–DM.13（$J,\Upsilon,\lambda_2=\lambda_1,T_\theta$） |
| 数学特征 | 实轴、无虚部、纯衰减 | 临界线、有 $\gamma$、有节奏 |
| 给什么 | 允许 $n=2,4,6,\ldots$、电荷量子 $\Phi_n=h/(ne)$ | 节奏 $\pi/\gamma_1$、交叉温度 |
| 不能给 | 相变节奏/温度 | 配对强度/态密度 |

**索引对齐**（【严格】）：$\zeta(-n)=0\iff n=2,4,6,\ldots$（由 $\zeta(1-m)=-B_m/m$、$B_{\text{奇}}=0$），与配对支的群量子精确对齐；$\Phi_n/\Phi_2=2/n$（脚本检验）。

**平凡零点不能进相变支**（数学硬约束）：平凡零点无虚部，$e^{(\rho-\frac12)t}=e^{(-n-\frac12)t}$ 是纯衰减，给不出 $e^{i\gamma t}$ 节奏。

**记忆核谱只对非平凡零点求和**：

$$K(t)=-\sum_\rho\frac{e^{(\rho-\frac12)t}}{\rho}+O(e^{-t/2}).$$

> 来源：06 §0.6、§0.8、§9；记忆核计数稿 §12；原两族零点分工稿（已并入本节）。

---

## 十二、五要素机制整合

| 要素 | 角色 | 做什么 | 不做什么 |
|:---|:---|:---|:---|
| 相变锚核 $A_\tau$ | 静态前提 | 给零漂移基线（可同步性） | 不提供配对、不提供刚度 |
| 记忆核 $K$（超导态平台 $K^{\rm SC}$） | 贯穿两态、因共享生平台、读出相变 | 正常态自由变化 → 超导态 $K^{\rm mid}\to K^{\rm crit}\to K^{\rm SC}$；谱侧编码 RH | 不直接给 $T_c$ 数值（06 §0.6） |
| 配对 $\lambda_i$ | 局域、可不同 | 给 $T_i^*$；各畴强度可不相同 | 不决定全局连通 |
| 渗流（在先） | 建立全局连通域 | 无限簇形成后锚（相变体现）显现 → 全局相干 | 不作用在刚度上；不独立定 $T_c$ |
| 相变 $T_c$ | 全局事件 | $\min(T^*,T_{\rm BKT},T_\theta)$，非平凡零点节奏+交叉 | $\mathfrak A(T)$ 不是 $T_c$ 判据 |

**记忆核贯穿两态的四阶段**（06 §0.6，【构造】）：$T\gg T^*$ 自由变化（无锚）→ $T^*>T>T_c$ 中间平台 $K^{\rm mid}$（相变锚尚未显现，核 $A_\tau$ 在位）→ $T=T_c$ 临界值 $K^{\rm crit}$（锚作为相变体现显立）→ $T<T_c$ 稳定平台 $K^{\rm SC}$（锚内共享、锁定）。$K^{\rm SC}$ 在 $T_c$ 从零变非零，「像序参量一样经历相变」。

**相变锚核与记忆核的关系**：相变锚核 $A_\tau$ 静态、记忆侧平台 $K^{\rm SC}$ 随 $T$ 变，是两个对象；二者经「占据」关系 $A_\tau\to\mathcal A(t)\subseteq A_\tau$（相变锚判据稿 §6.2）相连，或「反馈闭环环集渗流」（提案，未证）。FDT 层面统一的是动力学变量 $x=\Delta v_\tau$ 的关联与不动点，不把相变锚核 $A_\tau$ 与 $K^{\rm SC}$ 读成同一物。

> 来源：06 §0.6–§0.7；相变锚判据稿 §6；记忆核计数稿 §10；锚-记忆核关联稿。

---

## 十三、外参量汇总

### 13.1 压强：垂直作用于平面上下两个面（配对支，严格）

**几何设定**：压强施加在单层晶格的**上表面与下表面**（两个面），方向垂直于平面（$\sigma_{zz}$，法向 $\pm\hat z$）。静力平衡要求 $\nabla\cdot\boldsymbol\sigma=0$、上下面 traction $\mathbf t=\boldsymbol\sigma\mathbf n$ 大小相等方向相反——单面压强给净力、非静态。所以「压强＝两个面」，与电磁场的「一个面」不同（见 13.2）。

垂直压强只改面外几何（层间/厚度方向的键），不改面内键的一阶长度；对**静态**亏角：平衡 Delaunay 剖分下体相铰链亏角恒零（$\sum_T\theta_e^T=2\pi$ 恒等），垂直压强不改它。

压强经声子链进入**涨落**通道：$\to$ 晶格常数 $l$、声子频率 $\omega_D$；$A_{ek}$ 与 $G$ 尺度不变（C1）。经声子链：

$$\Delta\varepsilon_0^2\propto\frac{1}{\omega_D l^2},\qquad
\frac{\partial\ln\Delta\varepsilon_0^2}{\partial P}=\kappa_T\Bigl(\frac23-\gamma\Bigr)\ne0\quad(\textbf{严格}).$$

典型 $\gamma>2/3$ 时压强使涨落减小 → $\Upsilon\propto\Delta\varepsilon_0^2$ 减小。**各向同性静水压对静态亏角严格无效**（体相 Delaunay 恒零，数值 $10^{-15}$ rad）。压强不改锚（锚由静态 $\ell^{(0)}$ 定），只改涨落/刚度。

> 来源：`geom2.py` 数值自检；原压强严格推导稿（已并入本节）。**未闭合**：与实验 $dT_c/dP>0$ 的符号张力暴露 M4/Grüneisen 识别缺口。

### 13.2 静态电磁场：从上方垂直进入上表面（一个面，相变支，严格到边界）

**几何设定**：电磁场从上方垂直进入，**只作用一个面**（上表面，法向 $\hat z$）；与压强的「上下两个面」不同。静态场不谈「入射面」——场弥漫空间，源在一侧只是边界条件选择。

- **电场** $E\hat z$：无环量、对中性声子无耦合，故 $\partial\ln\Delta\varepsilon_0^2/\partial E=0$，**严格无入口**；
- **磁场** $B\hat z$：唯一规范不变标量 $\Phi_C=BA_{\rm loop}$（严格）；不改涨落（$\partial\ln\Delta\varepsilon_0^2/\partial B=0$，严格）；接到和乐相位 $\varphi_B=2\pi\Phi_C/\Phi_n$ 是【构造】（G10/G19 未闭合），$J_{ij}(B)=J_{ij}^{(0)}\cos\varphi_B$ 为条件结论；
- 三者都不改锚。

> 来源：06 §11.5；原静态电磁场严格分析稿（已并入本节）。

### 13.3 外参量分工总表

| 外参 | $\Delta\varepsilon_0$ | 锚 $A_\tau$ | 和乐相位 | 分支 |
|:---|:---|:---:|:---|:---|
| 压强 $\sigma_{zz}$（上下两面，垂直） | 变：$\kappa_T(2/3-\gamma)$【严格】 | 不改 | 不变 | 配对支 |
| 静态 $E\hat z$（上面一个面） | 不变【严格】 | 不改 | 无环量 | 无 |
| 静态 $B\hat z$（上面一个面） | 不变【严格】 | 不改 | $\Phi_C=BA_{\rm loop}$【构造接入】 | 相变支 |
| 温度 $T$ | E7 $\sqrt{\tanh}$【严格】 | 不改 | — | 两支 |

---

## 十四、结论

本链条从位置-动量对易 $[\hat X,\hat P]=i\hbar$ 出发，经声子（环节①）、一般晶格剖分与亏角/图拉普拉斯（环节②）、亏角涨落（环节③）、固有时流速（环节④）、全局耦合与品质因数（环节⑤）、方差与去相干（环节⑥）、记忆核（环节⑦）、记忆核积分（环节⑧，固有时流速差异历史总和的记忆侧体现），止于记忆核积分（环节⑧）；环节⑨（相变方程／$T_c$）未推、暂时未定，已从链条删除。八个环节的输入、推导、输出、严格性与来源已逐环给出，严格段、构造段、外部段分栏保留。

**链条的主干关系**：位置-动量不确定给出「必震荡」与声子算符（严格）；亏角曲率给出「稳定」判据（$L$ 半正定）；亏角涨落经 FG 接口进入固有时流速；流速差异经 DNR 进入全局耦合；涨落方差经 OU 扩散给去相干率；去相干把记忆核谱侧截断；记忆核的时间积分 $\mathcal I_K$ 是**固有时流速差异历史总和的体现**；固有时流速差异的历史总和本身是 $\mathcal H_{ij}=\int(v_i-v_j)dt$。$\mathcal I_K$ 与 $K^{\rm SC}$ 平台是记忆侧的**体现**，$T_c$ 由刚度/软模条件给出，两者不能互相替代。

**五要素分工**：渗流给连通域与刚度乘子（L2，不独立触发相变），锚是相变的空间体现（稳定性边界），记忆核 $K$ 贯穿两态、因共享生平台并编码 RH，配对可局域不同，相变取小。两族零点分工：平凡零点管配对与电荷结构，非平凡零点管相变节奏。

**外参通道**：压强垂直作用于上下两个面（静力平衡要求双面，经声子改涨落、配对支）；静态电磁场从上方进入一个面（电场无入口、磁场经构造的和乐相位、相变支）；两者都不改锚。

**严格边界**：空间锚与记忆核由「占据–读出」相连（FDT 统一的是动力学变量层面），不是同一对象；$A_\tau$ 与 $K^{\rm SC}$ 的同一性属 M9，未证。记忆核积分 $\mathcal I_K$ 的长时间极限在响应侧**体现为**静态响应 $\chi(0)$（外部 Kramers–Kronig 识别），但 $D_c$ 未定义；$\mathcal I_K$ 不是独立的 $T_c$ 判据，只是固有时流速差异历史总和的体现，不是固有时流速差异的历史总和本身，也不是相变本身。软模方程 $\omega_0^2(T_c)=0$ 与刚度判据 $\Upsilon(T_c)=\Upsilon_c$ 是同一临界点的两种标准读法，$V$ 的微观定义仍是缺口。

严格段与构造段已分栏，缺口如实保留，未绕过 W-3、G10/G19、E4、M1、M2–M4、M7–M9、Z2、R30。本文**未修改** 01–07、Lean、网站；元素路线不在本文范围。

> 可复核产物：`06 超导/cqm_analysis/`（lattice_regge_model.py、ring_1d_flow.py、vtau_coupling_chain.py、global_coupling_constraint.py）；`10 探索/cqm_element_sc/geom2.py`（尺度不变性自检）；`10 探索/cqm_trivial_zeros/`（索引对齐检验）。