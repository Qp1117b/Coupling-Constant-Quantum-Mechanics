# DISCARD：放弃内容 / 不成立的具体条件 / 文献或数据依据

> 双账本之二。**先记后删**：凡从工作台移除的读法，先在此登记"在何条件下不成立"与依据，再删净正文防干扰。
> 不凭审美丢弃；每条必须可回溯到文献、数据或链内定义矛盾。
> 目录边界：本文件仅在 `10 探索/超导第一性研究/` 内。

## 一、已放弃读法（按轮次登记）

| 轮 | 放弃内容 | 不成立的具体条件 | 依据 |
|:---|:---|:---|:---|
| 154 | 用 (19P.21) 裸 BKT 交点定 $\sigma_c$ | 普适跳变作用在**重整化**刚度上；真实判据含 $g_{\rm ren}\le1$；裸式给 $\Phi_c=0$、$\Upsilon(T_c)=0$，与 BKT 下界 $>0$ 矛盾 | U.4–U.7；L47 |
| 155 | "第 154 轮数值表普适" | 只在 $g_{\rm ren}=1$ 极限成立 | 第 155 轮指数匹配 |
| 156 | "座/键自变量在临界区给不同指数" | 近阈比收敛到常数 $C_{sb}=0.681205$，可吸收进外生 $\Upsilon_0$；只差归一、不改指数 | 第 156 轮数值／L44 |
| 157 | "$\rho$ 只能作连续外生参数" | 链内 Bessel 核在最近邻给 $\rho_{nn}(m)$，只剩离散载体选择；符号可由偏差判别 | (8G.3)；L49 |
| 158 | "连通温度 $T_\*$ 就是目标区振幅温度 $T^*$" | 二者属不同扇区（渗流连通 vs 振幅配对），链内不给数值顺序 | 第 158 轮边界 |
| 159 | 锁定整数"$m=2$ 全星分支" | 诱导键每对节点只有一条，星级条件是节点级、用于边级渗流属层级混用；$t(T_c)\le1.1072$ 分支排除 | SB.3；R-158 |
| 159 | "$E_c$ 可用重整化刚度 $\Upsilon(T_c)$" | 给 $y=2\pi e^{-\pi}=0.271521>0.025007$，违反 BKT 界；只能用裸 $\Upsilon_0$ | R-158；L51 |
| 160 | "(目标.2) 盲测是 A 类绝对 $T_c$ 验证" | $\omega_{\log}$ 跨定义差 $e^{1/6}$（R-62），P2/P3 只是 B 类上界对照 | 预注册 R12 |
| 161 | "推 6 单层不能渗流仍有残余可能" | 关联修正后三载体 $q_c<0.5$，达键阈值需 $\rho_{nn}\ge0.987$，远超 Bessel 核最大 $0.181$ | 第 157／161 轮 |
| 161 | "和乐尾匹配给出外部熵因子 $2\pi$" | 只匹配指数，前因子差登记为外部边界，CQM 不推出 $2\pi$ | L51/L53 |
| 162 | 环 15 的 `Ring15Spec.lean` v1：`lockMult := if ⟨(a,b),h⟩ ∈ edges then 1 else 0`，`TargetProp := InducedBond → lockMult = 1`，且无对应证明模块 | 把结论写进值域后，`TargetProp` 对任意键图恒真：`≤1`（SB.3 简单图）与"恰有一条"两半同时退化为定义展开，无法区分"多键不可能"与"锁定事件存在"，也不承载"星级读法被排除"这一层 | 术语锚点"定义式证明／语义漂移"；`03_推导工作台/环15锁定整数与E_c反演.md` §二（$m_{\rm lock}$ 是键级计数，非节点星级）；v1 文件第 22–31 行 |
| 164 | "相变是以 P=NP 为前提的过程" | P vs NP 未证；P/NP 属图灵机模型的均匀复杂度，链内无计算模型、无输入编码、无对应物；环 15／19 的判据只由 $K$、$p_c$、$y$、$\Upsilon$ 表述，加此前提即为外加未证公设 | `10 探索/AGENTS.md` §1 第 4 问；红线"不虚构" |
| 164 | "质数振荡（黎曼关联）下 P=NP 成立" | 13.A 的质数化是**配对算符的实现**（节点原子化），不是计算复杂度声明；同批 `openai/math` 手稿方向是代数复杂度**分离**（VP≠VNP、电路下界），既不能推出 P≠NP，更不能推出 P=NP | `openai/math` history.md 2026-11-24（family 379）；arXiv:2611.04175 |
| 164 | 把 ETG 的"张量／几何／曲率"直接接入本链 | ETG 张量＝三模计算对象（秩、边界秩、渐近秩）；链内张量＝曲率／亏角／应变（几何—物理量）；"几何"指退化分解诱导的度量与非正曲率，不是时空曲率 | `08_框架扩展候选/FE10_欧几里得张量几何的迁移审查.md` §二；术语锚点"语义漂移" |
| 165 | "用 ETG 的秩／乘法条数衡量原子化—离散化—质数化—相变过程" | 三接口各自断：①量纲不可比（无量纲乘法条数 vs 有量纲热力学代价，无 $1$ 次乘法$\leftrightarrow$焦耳的换算）；②无共同不变量（组合非正曲率 vs Regge 物理亏角；$\omega$ 与临界指数无已知函数关系）；③质数化是空间压缩且 $\mathbb Z$ 非域、位数成本超线性，rank 读不出其代价 | FE10 §八；`openai/math` family 379 清单；13.A；SB.3 |
| 166 | "原子化—配对—质数化三过程可统一由秩计价" | 配对阵型虽同型（双线性），但计数口径四个不同构（节点 $n$／对数 $n^2$／素数 $n$／乘法条数）；且质数化"写便宜读贵"，ETG 不计读回 | FE10 §九；13.A |
| 167 | "以张量秩／乘法条数为相变判据" | **数值否证**：$\mathrm{rank}(\lambda T)=\mathrm{rank}(T)$（$\lambda\ne0$，代数恒等；7 乘法复算残差 $1.646\times10^{-15}$，$\lambda\in[0.05,4]$），故该判据预测 $T_c$ 与耦合强度无关；而 $T_c/\omega_D=1.13e^{-1/\lambda}$ 在 $\lambda\in[0.05,0.90]$ 跨 $8.2$ 个数量级，与同位素效应／压力／掺杂下 $T_c$ 剧变冲突 | `04_计算验证/FE11_秩判据与Tc标度对照.py|.json|.png`；FE11 卡；BCS（B 类外部对照）；Winograd 1971 秩下界 |
| 168 | "以 $T_{\rm sync}$ 对 $\lambda$ 的弱变化支持'秩判据可用'" | $T_{\rm sync}$ 几乎不动源于**饱和**（$\lambda=1.6$ 时距 $T_*$ 仅 $2.3\%$），不是代数不变量；同一次缩放里 $y$ 跨 $4.64$ 个数量级、$\partial\ln y/\partial\lambda=-10.69$，秩恒 7 与它不可兼容。以 $T_{\rm sync}$ 的弱敏感当证据即"只借符号不借语义"（跑偏式） | `04_计算验证/FE11b_链内耦合缩放下的同步温度.json|.png`；FE11 §九；B 闸第 2 问 |
| 169 | "原子化—配对—质数化正好符合 CFT 的尺度不变性过程" | 三阶段共用同一 $T$、$m$、$(p_c,y)$，无 flow 参数；改的是**描述粒度**（节点 $n$／对 $n^2$／编码 $n$）而非尺度。链内真带 flow 参数的是 BKT 固定线与粗粒化指数 $t$，不在三阶段里 | FE10 §十 A–B；环 15 卡 §数值；B 闸第 3 问（层级/量词） |
| 169 | "配对算符化＝歌猜配对机制" | 歌猜是**加性**配对 $p+q=2n$；13.A 的标记是**乘性**配对 $p_ip_j$（唯一分解消碰撞）。链内无二者互换定理，也从未使用加性分解 | FE10 §十 D；13.A |
| 169 | "P=NP 不普遍成立 ⇒ 相变与常态可区分"（含方向正确的自我修正） | 方向对（撤回第 164 轮的"成立"），但范畴错：区分量是序参量／刚度 $\Upsilon$ 与 $p_{\rm sync}>p_c$，不含可判定性；正确表述是"P/NP 与相变区分无关"，而非"$P{=}NP$ 会抹掉相变" | FE10 §十 E；环 15 判据；红线"不虚构" |
| 170 | "由 (SB.1)–(SB.3) 的**座**独立可直接得**键**独立" | 共点两键共享座，故不独立：$\rho=p/(1+p)=0.372154$、$P(\text{共点两键同存})/P(\text{独立})=p^3/p^4=1.687063$（$p=0.592746$）。条件独立只在"给定座占据"层成立；无条件层乘 $p^{m+1}$ 会把 $p_{\rm sync}$ 压低（$m=1$ 因子 $0.351$），与第 163 轮登记 $0.8754138$ 冲突 | `03_推导工作台/环15_审6_独立键前提的授权层与偏差.md`；(SB.3) 协方差 $p^3(1-p)$；B 闸第 3 问（跨层） |
| 171 | "质数化是标度无关编码" | 素数定理 $p_n\sim n\ln n$：$n$ 个标记总位长 $\Theta(n\log n)$、单标记 $\Theta(\log n)$——**恰是一个对数标度**，而非无标度；该标度正是它比 $n^2$ 对表便宜的原因 | FE10 §十一；PNT |
| 171 | "耦合涨落—关系重组（作为链内机制）" | 涨落有对应物（$\sigma_\theta^2=k_BT/\Upsilon_0$、$y$ 的热涨落）；**重连／重组动力学链内没有**——环 15 只让占据随 $T$ 变、拓扑固定。缺的是可测量（重连率／键寿命 $\tau_{\rm bond}$），不是措辞 | FE10 §十一；环 15 拓扑固定 |
| 172 | "耦合常数涨落＝关系重组的表现" | 方向对（涡旋解绑确实含在 $y=2\pi e^{-E_c/T}$ 的流里），但**涨落与流动被并成一个词**：涨落是 $\sigma_\theta^2=k_BT/\Upsilon_0$（方差、含 $T$），流动是 $\beta_K=0.89294$（无量纲、不含 $T$）。合成后既不是方差也不是流 | FE10 §十二 A；$\beta_K$、$\sigma_\theta^2$ 登记处 |
| 172 | "U(1)–$Z_n$ 耦合"（把 $Z_n$ 当规范场） | 12.A 的 $Z_n$ 只是绕数扇区**标记**（$\Phi_n=nh/2e$），无规范场、无动力学；2+1 维 $Z_n$ 规范理论的任意子凝聚相变与 BKT 不同普适类。升格为规范场＝新增场，须走新机制流程 | FE10 §十二 B；12.A |
| 176 | "$\rho=-1/2$ ⇒ 共点两键的**锁定事件反聚集**（$C_{\rm lock}<1$）"（上一轮我的推测） | 数值与 MC 同时否证：$\rho\ne0$ 时 $|X|,|Y|$ **正关联**，都锁与都失锁均被抬高、混合态被压低，故 $C_{\rm lock}>1$ 恒成立（$a=0.5$ 处 $1.1259$，$a=1$ 处 $1.0685$）；"同型聚集"才是正确读法 | `04_计算验证/环15共点键相位相关_双变量高斯修正.py|.json`；MC $4\times10^6$ 复核（1.3169／3.923／22.79） |
| 177 | "顶点相位独立（$\rho_v=0$）可作链内前件" | (9.1) 的 $\mathrm{Var}=2\kappa_f^2\sigma_0^2(1-\rho_{ij})$ 是差场形态 ⇒ $\rho_{ij}\ne0$；第 84 轮 Bessel 核＋第 85 轮 $m_{\rm eff}=2$ 给 $\rho_1=0.048930$。"独立"只能是 $\rho_v\to0$ 的理想化极限，不是链内事实 | 卡 §十 10.1–10.2；README 第 270／837 行；(9.1) 权威式 |
| 177 | v6 式 $\rho_{XY}=(2\rho_1-1)/[2(1-\rho_1)]=-0.474276$（本轮首版 Spec） | 隐含**距离 2 顶点相关 $\rho_2=0$**；实际 $\rho_2=\rho_{m=2}(2a)=-0.093848$ ⇒ 完整式须含 $-1-\rho_2$（v7 给 $-0.424938$）。该式仅在 $\rho_2=0$ 时成立 | 卡 §十 10.3；`04_计算验证/环15共点键相位相关_链内Bessel分支.json` 的 `v7_full` |
| 178 | "$\theta_c$ 尚未从第 161 轮材料取出，$C(a)$ 只能给函数、不能给工作点单点值"（我上一轮的判断） | 漏读：(161.2) 明写"相位以 $2\pi$ 为周期；键失锁即相位差越过主值支边界 $|\theta|=\pi$" ⇒ $\theta_c=\pi$；且 $y=\operatorname{erfc}(\pi/\sqrt2\sigma_\theta)$ ⇒ $a=\Phi^{-1}(1-y/2)$ 由 $y$ 自定（$T_c$ 处 $3.802960$）。单点值一直可取 | 卡 §十一 11.1；`03_推导工作台/环15和乐动力学映射与推6终结.md` (161.2) |
| 179 | "$\rho_{nn}(m_{\rm eff}{=}2)=0.048930$ 就是 (9.1) 的链内定值"（第 177／178 轮我采用的写法） | 跨层＋跨核：$J_0$ 是 **2D 核**、且 $m_{\rm eff}=2n+1-s$ 只是 $d=2$ 特例；而 (9.1) 的 $\varepsilon$ 载体是 06 的 **3D Regge**（README 第 865 行）。3D 载体应给 $m_{\rm eff}=3$ 且核为 $j_0=\sin z/z$，$\rho_1$ 取 $+0.2410$（$m{=}3$）或 $+0.3040$（$m{=}2$）。该值只在"2D 核＋$d{=}2$ 测度"下成立 | 卡 §十二；`04_计算验证/环15锁定概率_载体核分支.json`；README 第 865 行；第 157 轮 ρ_nn 表 |
| 179 | 第 85 轮 "$m_{\rm eff}=2n+1-s\Rightarrow2$（3D Regge 载体）" | 记账自相矛盾：$2n+1-s$ 用的是 $d=2$ 测度，而载体声明为 3D。一般式 $m_{\rm eff}=2n+(d-1)-s$ 在 $d=3$ 给 $3$。第 157 轮"3D⇒3／2D⇒2"才自洽 | 卡 §十二 12.1；第 85 轮 README 第 864–865 行；第 157 轮卡 §16(2) |
|

## 二、待删除正文（防干扰，先记后删）

- 无（既有废弃读法均已在对应推导卡内以注记形式收束，未留平行正文）。
- 若后续 B 闸判跑偏，按协议"回本环第 2 步修定义授权与 Spec，重跑整环"，旧版本正文先入本表再删。

## 三、账本纪律

- 任何删除必须同时满足：①本表有行；②依据可回溯（文献编号／方程编号／数据文件）；③不删除缺口编号或状态栏。
- 不把"不升格为 A 类"误写成"已解决"；未闭合处明写未闭合。
| 180 | 第 157 轮"沿用 J₀ 形状、把 m 换成 3 代表 3D 载体"的做法 | 与口径表符号表/第 86 轮维数定律冲突（3D 主值明写 j₀ 核）；J₀ 是 2D 角向积分的形状 | 口径表 §一第 86 轮条、§符号表 R49/R45 行 |
| 180 | `审-4` 把"Bessel 核最大 0.181192"当 ρ 的上界 | 该值只是 2D J₀ 核 m=1；3D j₀ m=3 给 ρ₁=0.241029 > 0.181192，"上界"不成立 | 本轮 §13.2 闭式；但"需 ρ_nn≥0.986862"结论不变 |
| 182 | 用线性化高斯给 $y=\operatorname{erfc}(a/\sqrt2)=1.43\times10^{-4}$ 作为"解锁率"，并以"$2\pi$ 前因子外部"结账 | 精确比值判据给 $y=6.7\times10^{-4}$／$2.3\times10^{-5}$／$1.9\times10^{-6}$（$s=\tfrac12$／$1$／$2$），与 $s$ 无关的线性化值 $1.43\times10^{-4}$ 在 $s{=}1/2$ 偏低 $4.7$ 倍、在 $s{=}2$ 偏高 $73$ 倍；用环 4 的 $\sigma_\varepsilon=0.18$–$0.54$ 则 $y\lesssim10^{-13}$。缺的是方差归属，不是常数 | 本轮 §15.1–15.3；环 4 (4.1″) 与 (161.1) 的方差赋值互不相容 |

| 183 | 161 的判定"$2\pi$ 前因子差＝外部熵因子，登记边界"，即以 $y=2\pi e^{-E_c/k_BT}$ 与 $y=\operatorname{erfc}(\pi/\sqrt2\sigma_\theta)$ 的常数差结账 | 一旦写出桥 $\sigma_\theta=\lvert s\rvert\sigma_\varepsilon$，前因子差不是常数：精确 $y(s)$ 从 $3.47e{-3}$（$s{=}\tfrac12$）单调降到 $3.76e{-6}$（$s\to\infty$），跨 $10^3$；登记值 $1.43e{-4}$ 只对应 $\lvert s\rvert\approx1.24$ | 本轮 §16.1–16.2；v9 一阶系数 + $\alpha=-4\pi s$ |
| 184 | "$\sigma_\theta^2=k_BT/\Upsilon_0$ 与 $\sigma_\varepsilon^2=b\,n_d$ 可各自赋值、桥只管数值" 这一读法 | 两者统计来源不同（热 vs 缺陷布居，R-147 已判 $\varepsilon$ 非热）；桥一旦写成恒等式即断言 $\varepsilon$ 布居由 $k_BT$ 供能，与 R-147 冲突 | 本轮 §17.2–17.3；口径表 §一 R-147 条 |
| 184 | 把两个 $E_c$ 当同一符号使用（弹性激活能 / 涡旋刚度能） | 数值不同、无语义等式；$E_c^{\varepsilon}$ 无链内值 | 本轮 §17.1 |
| 185 | (161.4) 的**第二等号** $\pi^2/(2\sigma_\theta^2)=E_c/(k_BT)\Rightarrow\sigma_\theta^2=k_BT/\Upsilon_0$，以及由它接出的 (161.5) $\Upsilon_0=\hbar\omega/[4\alpha^2\kappa_f^2\sigma_0^2(1-\rho)]$ | 不成立的条件：(4.1) 的**第一项**（Bose 占据曲率模）存在，即 $N_I$ 扇区的 $M_k>0$。第 138 轮已证 $B^+|_{N_I}=0$、$M_\ell|_{N_I}=0$ ⇒ $c_k^0$ 发散、该项整体撤销；而 (161.4) 的前件 $\sigma^2(T)=\sigma_0^2[1+2n_B]$ 正是该项。附带：它把 (15L.3) 的 $\Upsilon$ 冻成 $\Upsilon_0$，与 (19W.8) $\Upsilon=\Upsilon_0w(T)\Phi(T)$ 冲突 | 口径表 §一第 138 轮条（R-147）；卡 §十八 18.1–18.2；`环04_非仿射无动力学与审21结案.md` §(4C.6) |
| 185 | Spec **v11** 的 `epsVarFromTheta`／`TargetPropVarBridge` 与证明模块 `Ring15LockBridge.lean`（旧版 Spec＋模块整体退役，文件已删） | 不成立的条件：$\sigma_\theta^2=k_BT/\Upsilon_0$ 可作为**独立来源**与环 4 的 $b\,n_d$ 并列；它其实是 (161.4) 第二等号的推论，前件已撤。v12 改以 `fugOfK`（$y$ 只依赖 $K=\Upsilon/T$）＋`TargetPropFugStiff/FugBound/UpsLower` 接替 | 卡 §十八 18.2、18.6；`05_Lean验证/Ring15Spec.lean` v12 头注 |
| 185 | "第 184 轮的两 Horn（热支／非热支）二选一"这一分析框架 | 不成立的条件：热通道与 $\varepsilon$ 通道是两个并列的方差来源。实际只有一个热通道＝刚度（(15L.3) 的 $\Upsilon(T)$）；$\varepsilon$ 按 R-147 保持非热，二者不再被桥等式钉成同一方差 | 卡 §十八 18.1；PROGRESS 第 185 轮四元组 |
| 185 | 第 181 轮的等价项 "$\mathrm{Var}(\Delta\lambda)$ 的 $O(\sigma^2)$ 修正 $\iff E_c\to E_c/(1+c)$" | 不成立的条件：$E_c$ 由 $\sigma_\theta$ 的指数匹配定（即 $\sigma_\theta^2=k_BT/\Upsilon_0$）。$E_c$ 现由刚度给，与 $\lambda$ 映射的方差无关；$\mathrm{Var}(\Delta\lambda)$ 的公式本身保留（它只属映射层） | 卡 §十八 18.2；卡 §十四（旧版等价项在此留下） |
| 185 | 把 $\Upsilon_0=0.649917$ 当**链内导出值**（由 $E_c=\pi^2\Upsilon_0/2$ 与 $y$ 反演互定） | 不成立的条件：$y$ 与 $\Upsilon$ 之间有已证的指数识别。现 $\Upsilon_0$ 属外部可测（环 19 (19W.1)：$\Upsilon_0=\Upsilon(0)$ 由 $\Lambda(0)$ 定），链内只给下界 $0.442819$；该数值作为**可采外部值**保留，但"导出"资格撤销 | 卡 §十八 18.3(i)；`环19_w温度与实验刚度的对应域判据.md` (19W.1) |
| 185 | 第 163 轮"两分支核对"中的 KAP 支：$\Upsilon_0=0.206875$ | 被链内普适界否证：(15L.5) 要求 $K(T_c)=\Upsilon_0w(T_c)/T_c\ge1/\beta_{\rm KT}$，该支给 $K=0.52319<1.11990$、$y(T_c)=0.4752>0.02501$ | 卡 §十八 18.3(i)；`环15锁定概率_逸度归刚度的温度依赖.json`（`y_Tc_KAP=0.47523`、`K_Tc_KAP=0.52319`） |
| 186 | 前卡 (15M.5)："$t(T)\le t(T_{\rm sync})=1.0509$ 对整个同步区 $T\in[0,T_{\rm sync}]$ 成立" | 不成立的条件：$y(T_{\rm sync})=y_{\rm crit}=0.025007$（该判定把 $p_{\rm pair}$ 校准到阈值时隐含取定）。第 185 轮改 $y$ 律后 $y(T_{\rm sync})=0.1847$，为 $y_{\rm crit}$ 的 $7.4$ 倍；$t$ 在 $T=0.34299$（$m=1$）／$0.34506$（$m=2$）即越过 $1.0509$／$1.1072$ | 卡 §十九 19.3；`环15粗粒化指数t_方向与下界.json`；`环15_逸度通道判定与t温度单调性.md` §四警示框 |
| 186 | "$\epsilon_\nu$ 可用单一 $t$ 值（$t=1.0509$ 或 $1.1072$）贯穿同步区" 这一口径 | 不成立的条件：$t$ 随 $T$ 变化且无上界（$T\to T_{\rm break}$ 时 $t\to\infty$，$T=0.730$ 处 $14.12/27.24$）。同步点真值 $t=1.64063/1.88469$ 给 $\epsilon_8=1.5901/1.4102$、$r$ 上移 $1.53/1.72$ 倍，与单一值差 $50\%$–$72\%$ | 卡 §十九 19.3–19.4；同 json |
| 187 | "两条写法处处相等"（即把 $p_{\rm pair}^{\rm thr}=p_c/(1-y)^m$ 当作任意 $T$ 的 $p_{\rm pair}$ 值，或反之） | 不成立的条件：$T$ 不在同步点。$T_c$ 处 $p_{\rm pair}=0.875539$，阈值写法 $0.593866$（$m{=}1$）／$0.594988$（$m{=}2$），$p_c^{1/t}=0.597104$／$0.601371$；三者只在 $p_{\rm pair}(1-y)^m=p_c$ 处相等（差 $3.3\times10^{-16}$）。交接表须用 $p_c^{1/t}$ 或"同步点上的阈值" | 卡 §二十 20.3(2)；`环15配对阈值与t两写法.json`（`two_writings_diff_m1/m2`、`T_tc_mismatch_m1/m2`） |
| 188 | "失效面半径 $r(T)$ 随 $T$ 单调上移"（第 186 轮卡 §十九 末句「$r$ 同倍移动，失效面随之上移」的整段读法） | 不成立的条件：把 $w/|w'| 的形状项当常数。$r=2\alpha_Vw/(3\epsilon_\nu|w'|)$ 在 $T_c$ 邻域 $|w'|$ 降得比 $w$ 快（$w$: $0.75870\to0.70292$，$w'$: $-1.1494\to-1.0769$），形状项在 $T\approx0.3445$ 取极小 $0.98866$；合成后 $m=1$ 支在 $T=0.30575$ 有 $4.03\times10^{-4}$ 凹陷（$0.999597$）。只能说 $\epsilon$ 通道单调，不能说 $r$ 单调 | 卡 §二十一 21.3(3)；`环15锁定失效面r的epsilon反比结构.json`（`r_rel_min_m1`、`w_factor_min_m1`、`r_rel_strict_increasing_m1=false`） |
| 188 | "高温支 $r\propto T$ 可贯穿到 $T_{\rm break}$"（R-157 §五的渐近读法被当作全程结论） | 不成立的条件：$t$ 有界（$\epsilon_\nu$ 近常数）。$T\to T_{\rm break}$ 时 $p_c^{1/t}\to1$、$x_\ast\to0$、$\epsilon_\nu\to0$，$1/\epsilon_\nu$ 发散主导：$\epsilon_8=0.43764$（$T=0.7261$）、$r/r(T_c)=7.19$ 仍上冲。R-157 的 $r\propto T$ 只在 $|d\ln w/dT|\to2/T$ 且 $t$ 有界的高温段成立 | 卡 §二十一 21.3(4)；同 json（`near_break`）；`03_推导工作台/环17_A源与扫描奇偶性.md` §五 |
| 189 | 185 (ii) 的"$y(T_c)$ 是窗口 $[1.8862\times10^{-3},0.02501]$、$\Phi$ 可在 $[0.68135,1]$ 内自由取值、$T_{\rm sync}$ 是窗口" | 不成立的条件：$\Phi$ 进入 (15L.3)。环 19 在 $T_c$ 钉死 $\Phi_c=\kappa=2T_c/(\pi\Upsilon_0w_c)$（(154.2)＋(19W.1) 的 $\Upsilon_0=\Upsilon_{\rm bond}$），而 (15L.5) 要求 $\Phi\ge\Phi_{\min}=0.68135$；两者之比 $\Phi_{\rm BKT}/\Phi_{\min}=2\beta_{\rm KT}/\pi=0.5685<1$，**与 $T_c,\Upsilon_0,w$ 全无关** ⇒ $\Phi=\Phi_{\rm BKT}$ 时 $y=2\pi e^{-\pi}=0.2715>y_{\rm crit}$，(15L.5) 必被违反。故窗口塌成点：$y(T_c)=1.8862\times10^{-3}$、$T_{\rm sync}=0.50665/0.47071$ | 卡 §二十二 22.1–22.4；`环15锁定概率_Φ授权域与BKT钉住冲突.json`（`phi_min=0.68135`、`phi_bkt_kappa=0.38732`、`ratio=0.5685`、`no_go_holds=true`、`Tsync_Phi_1`）；Lean `TargetPropPhiConflict`／`TargetPropPhiBktVal` |
| 189 | 185 轮撤销 (161.4) 的**第二条理由**："把 $\Upsilon$ 冻成 $\Upsilon_0$ 与 (19W.8) 的 $\Upsilon=\Upsilon_0w\Phi$ 冲突" | 不成立的条件：$\Phi$ 有权进入 (15L.3)。(15L.3) 的 $\Upsilon$ 是 bare（授权文本 $E_c^{\rm eff}=\frac{\pi^2}{2}\Upsilon_0w$，无 $\Phi$），故"冻 $\Upsilon$"并不违反 (19W.8)；两条 $T$ 依赖通道里只有 $w(T)$ 一条属 (15L.3)。**判决本身保持**（(161.4) 第二等号仍撤销），只因第一条理由（$T$ 依赖须经 $w(T)$） | 卡 §二十二 22.3；口径表第 185／189 轮条；`DISCARD.md` 第 185 轮行（不改其结论，只改理由） |
| 190 | "$w(0)=1$ 是 $w$ 的**定义值**"（(19W.1) 原先把 $T\to0$ 的归一直接写成点值 $w(0)=1$，并据此 $T\to0\Rightarrow\Phi(1)=1\Rightarrow\Upsilon_0=\Upsilon_{\rm bond}$） | 不成立的条件：把 $w$ 当 Lean 里的总函数读。`wGap 0 = ∫ u in 0..1, 2*u*tanh(u/(2*0))`，总除法给 $u/(2\cdot0)=0$、`tanh 0 = 0`，故 `wGap 0 = 0`，与链内 $1$ 不同值。**正确读法**：$w(0)=1$ 只能作 $T\downarrow0$ 的**极限**陈述（数值 $1-w\approx3.29\,T^2$），(19W.1) 的 $T\to0$ 段须改写为极限句式，不得写成定义值。判决：**不收 (19W.1) 的物理内容**（$T\to0$ 时 $w\to1$ 成立），只撤"定义值"这一读法 | 卡 §二十三 23.5–23.6；`Ring15Spec.lean` v17 的 `wGap`；`环15_w结构_单调与上界.json`（`limit_small_T`：$1-w(0.01)=3.29\times10^{-4}$）；Lean `TargetPropWGapLeOne`（只给上界，不给点值） |

| 191 | "s∈½ℤ（仅下界 ≥3/2）是环 15／`审-6` 残余、且约束失效面因子" | 不成立的条件：把两个同名 s 当同一个。前者是环 6／G19 的**表示权**（θ=sℓ、α=-4πs、σ_ε=σ_θ/|s|，值落 ½ℤ）；后者是 R155.1 的**可解性因子** s_sol=2/[C(aλ−r)]（连续、可正可负、正向取遍 (0,∞)）。Lean 两条（`TargetPropSolSurj`／`TargetPropSolNeg`）证明后者值域不是任何格点。故整性约束不能加载到 s_sol；|s|=3/2 只筛表示权 | 卡 §二十四 24.2–24.4；`Ring15Spec.lean` v18；`Ring15LockS.lean`；A 闸十八模块 PASS |

| 192 | "G-190b：$w$ 严格单调只能作数值陈述（网格最小降幅 $4.67\times10^{-4}$ 即证据）" | 不成立的条件：把数值严格性当作证明。网格严格只是"没找到反例"，$w$ 的逐点严格减在链内可由 `tanh` 的导数为正＋积分对差分为正推出。判决：**撤销"仅数值"这一状态**，G-190b 收口；数值降级为旁证 | 卡 §二十五 25.2–25.5；`Ring15Spec.lean` v19；`Ring15LockWStr.lean`；A 闸十九模块 PASS |
| 192（工具坑） | 三个 Lean 写法陷阱（不计物理内容，只为复现不复踩）：①`intervalIntegral.integral_sub` 只传两条 `IntervalIntegrable` 时度量是隐式元变量（报 `∂?m` 与 `volume` 不匹配），须写 `(μ := volume)` 并同时给 `f`、`g` 命名参数；②其返回式右端是 `(∫f) - ∫g`，目标里是 `∫f - ∫g`，`linarith` 视作两个原子，须先 `simp only [sub_eq_add_neg] at hpos hsub ⊢`；③多行 `have h : (∫ u in (0:ℝ)..1,` 会被解析成绑定列表（`unexpected token ':='`），该等式必须单行 | 不成立的条件：以为这些写法可用（或以为有 `integral_lt_integral_of_le_of_lt` 现成机器——实测 Mathlib 无此名） | `Ring15LockWStr.lean` 编译记录；`probe192b–d`（已删） |

| 193 | "G-186 只能整条挂着（'$t$ 严格增仅数值'），须等 $y$ 与 $p_{\rm pair}$ 两通道一起做完" | 不成立的条件：把 G-186 当不可分割的整体。它的 $w\to K\to y\to t$ 通道三条定义式定理已可即刻闭合（`TargetPropKStrictAnti`／`TargetPropYStrictMono`／`TargetPropTStrictMono`，$p$ 固定口径）；剩下的是 $p_{\rm pair}(T)$ 通道，缺 $F_\nu$（$v=8$ 的 χ² 尾）定义授权。判决：**G-186 拆分为"通道（收口）＋G-186p（新开）"**，不再整条挂 | 卡 §二十六 26.2–26.5；`Ring15Spec.lean` v20；`Ring15LockTStrict.lean`；A 闸二十模块 PASS |
| 193（工具坑） | `def … : Prop` 形式的 Spec 命题在套用其证明时必须写命名参数（`(ups0 := …) (T1 := …) (T2 := …)`）：否则 Lean 把第一个显式参数当 `ups0 : ℝ`，报 "`h0 : 0 < ups0` 但期望 `ℝ`" | 不成立的条件：以为 `theorem foo : TargetPropFoo` 可以直接 `foo h0 h1 …` 应用（`TargetPropFoo` 是 def，展开后首个绑定变量是实数，不是命题前件） | `Ring15LockTStrict.lean` 编译记录（首版两处报错，已改命名参数后通过） |
| 194 | "193 轮口径：$p_{\rm pair}(T)$ 通道只要把 $F_\nu$（χ² 尾）的定义授权补齐，就能与 $y$ 通道一起复合出'$t$ 随 $T$ 严格增'"（卡 §26.5、口径表第 193 条、PROGRESS §三 193 块的"下一环消费"） | 不成立的条件：两通道**同号**。$p_{\rm pair}=1-F_{\chi^2}(n_{\rm cell}\sigma_c^2/(Zw(T)))$ 随 $T$ **降**（`README.md:115`＋`README.md:120` 的低温展开 $p_0-C(T/\omega_D)^2$ 同号），而 `TargetPropTEffMPMono` 证得 $t$ 对 $p$ **严格增** ⇒ $p$ 通道**压低** $t$，与 $y$ 通道（抬 $t$）**反号**。故 $F_\nu$ 到位也只能给"$p$ 降"，净方向须主导项比较。判决：该口径**作废**；复合命题单列 **G-186c**（甲类），G-186p 只保留"方向已证、余 χ² 尾定义授权（乙类）" | 卡 §二十七 27.2–27.3；`Ring15Spec.lean` v21；`Ring15LockTChan.lean`（`TargetPropTChanSplit` 的两条符号合取项）；数值 `环15_t两通道反号_旁证.json`（`p_channel_negative_all=true`、`y_channel_positive_all=true`、$|p|/y=0.114$–$0.283$） |
| 194（工具坑） | 纯代数恒等式（$t(p_2,y_2)-t(p_1,y_1)=$ 两项和）若只以 `ring` 收口，在 Lean 里对任何符号都 PASS：$\delta_1$、$\delta_2$ 的正负会被"同一化"掉，跑偏也看不见 | 不成立的条件：以为"等式证完＝通道方向证完"。正确写法是把 $\delta_1>0$、$\delta_2<0$ 作为**合取项**写进 Spec 命题，逼 Lean 分别证两条符号不等式（这正是 B 闸"防抵消"要防的情形）；另：`field_simp` 清分母须显式给 $\ln p_1\ne0$、$\ln p_2\ne0$（由 $\ln p<0$ 用 `ne_of_lt` 供），否则 `ring` 在 `(log p)⁻¹` 原子前止步 | `Ring15LockTChan.lean` 编译记录（首版两处 `unsolved goals`：`field_simp` 后仍写 `ring`，改 `field_simp [h1,h2]`＋`ring` 并补非零假设后通过） |
| 195 | "G-186c 可以无条件化：$\delta_1+\delta_2>0$ 在链内可当定理证出，于是'$t$ 随 $T$ 严格增'无须任何侧条件" | 不成立的条件：能把 $p_{\rm pair}(T)$ 的形状全部由链内给出。$p_{\rm pair}=1-F_{\chi^2}(n_{\rm cell}\sigma_c^2/(Zw(T)))$ 的依赖来自外部 χ² 尾（乙类），链内只有"$w$ 严格减、$p$ 严格降"两条单调性，据此只能得 $\delta_1>0$、$\delta_2<0$，**给不出 $\rho=|\delta_2|/\delta_1<1$ 的界**。判决：G-186c 只能写成条件式（`TargetPropTChanCriterion` 充要判据＋`TargetPropTChanDominate` 充分闸），无条件净方向仍是逐点域核（数值），不冒充定理 | 卡 §二十八 28.3；`Ring15Spec.lean` v22；`Ring15LockTDom.lean`；`环15_t主导项闸_旁证.json`（$\rho\in[0.018878,0.309125]$ 仅作域核） |
| 195（工具坑） | `div_pos_iff` 的两支若只用第一支（`0<a ∧ 0<b`），会把"$\Delta t>0\Rightarrow S>0$"证成对 $N<0$ 也成立的假版本；另 `absurd hN hNneg` 会因 `hNneg : N<0` 与 `¬0<N` 类型不同而报 Application type mismatch | 不成立的条件：以为 `div_pos_iff` 的排除支不需要与前件的正性对撞。正确写法是显式取 `not_lt.mpr (le_of_lt hN)` 做矛盾（`exact absurd hNneg (not_lt.mpr (le_of_lt hN))`）；`m>0` 由 `1≤m` 经 `one_le_nat_cast_pos` 显式给出，不藏 tactic | `Ring15LockTDom.lean` 编译记录（首版第二支报类型不匹配，改 `not_lt.mpr` 后 exit 0） |

| 196 | "G-190c：$|w'|$ 只能停在数值层，$w'$ 没有链内表示" | 不成立的条件：以为"积分定义的函数不可微"或"求导要新物理"。$w(T)=2\int_0^1u\tanh\frac{u}{2T}du$ 的被积函数对参数 $T$ 光滑（$T>0$），参数积分求导引理（`hasDerivAt_integral_of_dominated_loc_of_deriv_le`）＋控制函数 $\frac{4}{T^2}t^2$ 即可逐点给出 $w'(T)=-\frac{1}{T^2}\int_0^1u^2\mathrm{sech}^2\frac{u}{2T}du$。判决：**撤销"仅数值"这一状态**，G-190c 收口（`TargetPropWGapDeriv`＋`TargetPropWGapDerivNeg`），188 的 $|w'|$ 可直接取用；`wGapDeriv` 的数值大小仍不参与 $r$ 的形状判定 | 卡 §二十九 29.2–29.5；`Ring15Spec.lean` v23；`Ring15LockWD.lean`；`环15_w导数表示_旁证.json`（差分 vs 积分式相对偏差 $\le2.6\times10^{-10}$） |
| 196 | "用范数不等式 $\|F'(x,t)\|\le\frac{4}{T^2}t^2$ 就足以证明 $w$ 在减" | 不成立的条件：把方向语义交给范数。该不等式对 $F'$ 与 $-F'$ **同时成立**（$\|\cdot\|$ 吃掉符号），故它只保证"可微"，对"$w'<0$"一无所证——错号也照样 PASS。判决：符号必须**另立命题**（`TargetPropWGapDerivNeg`，由被积函数 $u^2\mathrm{sech}^2>0$ 经 `integral_pos` 给出），不得由控制函数论证代替 | 卡 §二十九 29.4「防抵消」；`Ring15LockWD.lean` 中 `show ‖…‖ ≤ …` 一行 |
| 196（工具坑） | 四个写法陷阱：①`𝓝` 记法在 Spec 的 import 基线下**不可用**（`Unknown identifier 𝓝`），须写 `nhds T`；②`t ∈ Ι 0 1` 展开成 `min 0 1 < t ≤ max 0 1`，`ht.1` 拿不到 `0<t`，须先 `rw [Set.uIoc_of_le (by norm_num : (0:ℝ) ≤ 1)] at ht`；③有界性目标的表达式是 beta-未归约的 `(fun x t => …) x t`，`rw` 找不到模式，须先 `show ‖-(t^2/x^2)*sechSq(t/(2x))‖ ≤ …`；④`HasDerivAt.comp` 的结论是 `(f ∘ g)` 形，直接 `exact` 与 `fun y => tanh(t/(2y))` 不等形，须 `simpa [Function.comp] using …`；另 `field_simp` 常直接闭合目标，其后跟 `ring` 会报 `No goals to be solved` | 不成立的条件：以为这些写法在上述 import 基线下可用 | `Ring15LockWD.lean` 编译记录（首版 6 处报错，逐条改后 exit 0） |

| 197 | "G-188 整条只能挂着：形状项 $w/|w'|$ 只能是两个数的商，没有链内分解" | 不成立的条件：把形状项当独立对象。核的原函数在链内已有闭式（$\frac{u^2}{2}\tanh\frac{u}{2T}$），FTC 给出 $w=\tanh\frac{1}{2T}+\frac T2w'$，于是 $w/|w'|=\tanh\frac{1}{2T}/|w'|-\frac T2$、$\frac T2|w'|=\tanh\frac{1}{2T}-w$、$\tanh\frac{1}{2T}>w$ 三条全部可证。判决：**撤销"形状项无链内分解"这一读法**，G-188 拆为 **G-188a（收口）** 与 **G-188b（$w''$ 与极小编址）** | 卡 §三十 30.2–30.3；`Ring15Spec.lean` v24；`Ring15LockIbp.lean`；`环15_w分部积分恒等式_旁证.json`（残差 $\le5.50\times10^{-10}$） |
| 197（工具坑） | 六个写法陷阱：①`ne_of_lt hT`（$hT:0<T$）给的是 $0\ne T$，要 $T\ne0$ 须 `ne_of_gt hT`；②`intervalIntegral.integral_const_mul` 的常数参数名是 `r`（不是 `c`），且 `μ` 不能省（否则 `don't know how to synthesize implicit argument μ`）；③`intervalIntegral.integral_eq_sub_of_hasDerivAt` 在只 import Spec 时不可见，须显式 `import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus`；④`Continuous` 的括号若少一层，`exact` 会吞掉下一行并报 "Function expected … but this term has type Continuous"；⑤把 `2*u*tanh` 与 `2*(u*tanh)` 对齐时 `rw [hf]` 方向反了（目标里是前者、假设里是后者），须 `rw [← hf]`；⑥形状项 `field_simp` 不化简 `d * d⁻¹`，须显式给 `wGapDeriv T ≠ 0`（`ne_of_lt hneg`）再 `field_simp [hne]` | 不成立的条件：以为这些写法在 Spec 基线下可用 | `Ring15LockIbp.lean` 编译记录（三轮报错，逐条改后 exit 0） |

| 198 | "$w''$ 只由核的导数项构成：把 $w'=-T^{-2}B(T)$ 对 $T$ 求导就是 $-T^{-2}B'(T)$，端点前因子 $T^{-2}$ 不必再求导" | 不成立的条件：$w'$ 的前因子与 $T$ 无关。$T^{-2}$ 随 $T$ 变，商法则必给端点项 $-\frac{2}{T}w'=+\frac{2}{T^3}B$；漏掉它，$w''$ 会系统性偏负（只剩 $-\frac{1}{T^4}\int u^3\mathrm{sech}^2\tanh<0$ 一项），符号与数值全错而等式仍"看起来像"。判决：**撤销"末端点项"读法**，$w''$ 必须是"端点项＋核导数项"两项结构 | 卡 §三十一 31.2–31.3；`Ring15Spec.lean` v25；`Ring15LockWD2.lean` 的 `hinvder`（$\frac{d}{dT}(-T^{-2})=\frac{2}{T^3}$）与 `hBval` | 
| 198 | "$S'$ 可由端点商的导数 $\left(\tanh\frac{1}{2T}/|w'|\right)'$ 与 $-\frac12$ 直接读出符号，不必引入 $w''$" | 不成立的条件：端点商求导后能避开二阶量。$\left(\tanh\frac{1}{2T}/|w'|\right)'$ 的分母含 $|w'|^2$、分子含 $\tanh\cdot|w'|'$ 与 $\tanh'\cdot|w'|$，归并后**恒等于** $\frac{w\,w''-(w')^2}{(w')^2}$（用 197 的 $\tanh=w-\frac T2w'$ 与 $|w'|=-w'$ 代换）；二阶量 $w''$ 无法被消掉。判决：**撤销"形状项导数可绕开 $w''$"读法**，$S'$ 的判据只能比较 $w\,w''$ 与 $(w')^2$ | 卡 §三十一 31.2；`Ring15LockWD2.lean` 的 `targetPropShapeDeriv`（`HasDerivAt.div` 后 `field_simp` 对齐 `shapeDeriv`） | 
| 198 | "本轮顺带把 $w''>0$（$w$ 凸）与 $S'$ 的分段符号一起证掉；数值 61/61 为正已够" | 不成立的条件：粗界可比。两项反号（$-\frac2Tw'>0$、$-\frac{1}{T^4}\int u^3\mathrm{sech}^2\tanh<0$），要定号和须证 $\frac{2}{T}|w'|^2>\frac{|w'|}{T^4}\int u^3\mathrm{sech}^2\tanh$，而 $\int u^3\mathrm{sech}^2\tanh\le\int_0^1u^3du=\frac14$ 这类粗界与 $2T^3|w'|$ 不可比；数值全正不构成链内证明。判决：**本轮只交结构与导数闭式**，符号判据留 G-188b 第二步，不以数值冒充已证 | 卡 §三十一 31.7；`环15_w二阶导与形状项导数_旁证.json`（`wpp_positive_all=true` 仅记为显影，不入链） | 
| 198（工具坑） | 五个写法陷阱：①$\cosh$ 的链式导数必须乘内层导数 $-\frac{t}{2x^2}$，只写 $\sinh\frac{t}{2x}$ 会差因子 $-2x^2$；②`cont_F'` 少一层括号会让 `exact` 吞掉后续行并报 Type mismatch；③`field_simp` 常直接闭合目标，其后 `ring` 报 `No goals to be solved`（本轮五处），`rw [integral_const_mul]` 后 `rfl` 亦多余；④`HasDerivAt (-fun x => (x^2)⁻¹)` 与目标 `fun x => -(1/x^2)` 差一层 `one_div`，须 `simpa [one_div]`；⑤`filter_upwards [Ioo_mem_nhds …]` 的端点无法推断（成元变量、`linarith failed`），须显式 `show Set.Ioo (0:ℝ) (2*T) ∈ nhds T from Ioo_mem_nhds …` | 不成立的条件：以为这些写法在 Spec v25 基线下可用 | `Ring15LockWD2.lean` 编译记录（三轮报错，逐条改后 exit 0） |

| 199 | "$w$ 在全温区凸：$w''(T)>0$ 对所有 $T>0$ 成立，可直接作为定理"（198 轮的"待证命题"口径） | 不成立的条件：$T$ 足够小。$w''$ 的端点闭式 $w''=w'/T+\mathrm{sech}^2\frac{1}{2T}/T^3$ 给出精确判据 $T^2|w'|<\mathrm{sech}^2\frac{1}{2T}$；数值比 $r=T^2|w'|/\mathrm{sech}^2$ 在 $T=0.255525$ 处穿过 1，仅 $T\gtrsim0.256$ 满足，而 $T=0.1/0.2/0.25$ 处 $w''=-6.376/-2.264/-0.180$。物理上：小 $T$ 时 $w\to1$ 已饱和，$w$ 从"下垂"转为"上凹"。判决：**撤销"无条件凸性"**，只保留条件式 `TargetPropWGapDeriv2Pos`（充分条件）与精确判据；$w''>0$ 只作为窗口内事实，不作定理 | 卡 §三十二 32.2、32.6；`Ring15Spec.lean` v26；`Ring15LockWD3.lean`；`环15_w二阶导端点闭式_旁证.json`（`ratio_one_crossings=[0.255525]`、`criterion_holds_ranges=[[0.2562,1.20]]`、`wpp_sign_at_0p1=-6.376`） | 
| 199 | "v25 的 $u^3$ 积分式是 $w''$ 的必需要素：要判符号就必须估 $\int u^3\mathrm{sech}^2\tanh$" | 不成立的条件：$w''$ 只有积分式这一种写法。197 的恒等式 $w=\tanh\frac{1}{2T}+\frac{T}{2}w'$ 对 $T$ 求导即给 $w''=\frac{w'}{T}+\frac{\mathrm{sech}^2\frac{1}{2T}}{T^3}$，$u^3$ 积分被整个消掉（两式同值，`TargetPropWGapDeriv2Alt` 已证）。判决：**积分式降为等价写法/校验用**，符号判据一律走端点闭式；数值旁证两式相对偏差 $\le2.18\times10^{-8}$ 作交叉核对 | 卡 §三十二 32.2–32.3；`Ring15LockWD3.lean` 的 `targetPropWGapDeriv2Alt`（`unique` 强制同值）；`环15_w二阶导端点闭式_旁证.json` | 
| 199（工具坑） | 五处写法陷阱：①`TargetPropWGapIbp` 是 `def … : Prop`，不能当函数套用，须 import `Ring15LockIbp` 取定理 `LockIbp.targetPropWGapIbp`；②`HasDerivAt.congr_of_eventuallyEq` 要 `wGap =ᶠ F`，与手头 `F =ᶠ wGap` 反向，须 `.symm`；③`field_simp` 已闭合目标时后接 `ring` 报 `No goals`；④`congrArg` 后是 beta-项，`rw` 找不到模式，须先 `simp only [] at h`；⑤在 `|w'|` 内部 `rw [hwabs]` 会重写成 $|-|w'||$，须用 `congrArg (fun x => T^2*x)`；`pow_pos (abs_pos …) 2` 与 $w'^2$ 差一层 `sq_abs` | 不成立的条件：以为这些写法在 Spec v26 基线下可用 | `Ring15LockWD3.lean` 编译记录（三轮报错，逐条改后 exit 0） |

| 200 | "199 的判据 $S'<0\iff w\,w''<(w')^2$ 已到终点，下一步只能靠数值核" | 不成立的条件：只当 $w$、$|w'|$ 的具体大小可估时才需要逐点数值。本轮把它换元——用 197 端点亏损 $Ta=2\tanh\frac{1}{2T}(1-\Phi)$ 与 $r$ 的定义，整块 $w\,w''-(w')^2=\tanh\cdot\mathrm{sech}^2[\Phi(1+r)-2r]/T^3$，符号只由两个无量纲数比较。判决：199 的乘积判据**降为中间步**，现行口径取比值判据 `TargetPropShapeSignRatio`（Spec v27）；数值从"判符号"退为"核恒等式与核对同号"（不一致 0 处） | 卡 §三十三 33.2；`Ring15Spec.lean` v27；`Ring15LockWD4.lean`；`环15_形状比与判据比_旁证.json`（`identity_rel_err_max=5.12e-9`、`sign_mismatch_count=0`） |
| 200（工具坑） | 四处写法陷阱：① `Real.tanh_pos`／`Real.sinh_pos_of_pos` 在此依赖基线不存在（只有 `Real.sinh_pos_iff`），须经 `tanh_eq_sinh_div_cosh` 用 `div_pos`；② `set a := |w'|` 后 `field_simp` 会把 $a$ 展开成绝对值、并残留 `|w'|*S/S=|w'|`，须改用 `div_mul_cancel₀` 直接给 $rS=T^2a$；③ 先 `rw [haT]` 再 `unfold ratioR`＋`rw [← ha]` 时新出现的 $a$ 不会被前面的重写覆盖，须再补一次 `rw [haT]`；④ `push_neg` 已弃用，改 `push Not`，且其结果形为 $2r\le\Phi(1+r)$，要 `linarith` 转成 $0\le\Phi(1+r)-2r$ 才能喂 `mul_nonneg` | 不成立的条件：以为这些写法在 Spec v27 基线下可用 | `Ring15LockWD4.lean` 编译记录（四轮报错，逐条改后 exit 0） |

| 201 | "第 200 轮判'下一步需要 $r$ 的上下夹逼 与 $\Phi$ 单调性'，故 $r$ 的界是 $r<1$ 段符号判定的**必要入口**" | 不成立的条件：判据必须停在 $(\Phi,r)$ 二元。端点亏损 $T\,|w'|=2h(1-\Phi)$（v24）与勾股恒等式 $\mathrm{sech}^2\frac{1}{2T}=1-h^2$ 给出 $r=\dfrac{2Th(1-\Phi)}{1-h^2}$；代回 $\Phi(1+r)<2r$ 后 $r$ 被**整块消掉**，得 $S'<0\iff 0<G(T)$，$G=2Th(1-\Phi)(2-\Phi)-\Phi(1-h^2)$。判决：**撤销"$r$ 的上下夹逼是必要入口"**；$r$ 的界降为可选旁证，后续只需 $\Phi$ 的界与单调性 | 卡 §三十四 34.2–34.4；`Ring15Spec.lean` v28；`Ring15LockUnary.lean`；`环15_判据一元化_数值核对.py`（$r$ 闭式相对残差 $1.10\times10^{-8}$、同号不一致 0 处） |
| 201（工具坑） | 五处：① `field_simp` 已直接闭合 `h₁`，其后 `ring` 报 `No goals to be solved`（198／199 的老坑仍在）；② PowerShell 管道 `lean … 2>&1 \| Select-Object -Last 5` 会**挂死**（CPU 停在约 19 s 不动、10 min 无输出、exit −1），须改为 `> 文件 2>&1` 再读文件；③ `Set-Content -Encoding UTF8` 写的临时 `.lean` 带 BOM，Lean 报 `expected token`（1:0），须用无 BOM 写法；④ 改 Spec 会使**全部下游 olean 失效**，必须按依赖序（Spec → WD → Ibp → WD2 → WD3 → WD4 → Unary）重编，单模块约 35 s、32 KB Spec 约 85 s；⑤ 新增 `shapeH T := tanh(1/(2*T))` 与 `shapePhi` 的分母是同一表达式，二者从此成为**耦合点**——改任一处必须同步另一处，否则 $r$ 的闭式与 $S'$ 判据会各说各话 | 不成立的条件：以为这些写法／流程在 Spec v28 基线下可用 | `Ring15LockUnary.lean` 编译记录（首版 1 处 `No goals`）；`a_gate.ps1` 重定向改写；A 闸二十八模块 PASS（58 条 axioms／53 条 `#check`／257 文件 0 命中／exit 0） |

| 202 | "第 201 轮判'最该修的一处＝$\Phi$ 的单调性'：只要 $\Phi$ 严格单调减（或再补 $\Phi'<0$ 的链内表示），$G(T)$ 的符号与 $T_{\min}$ 编址即可判出" | 不成立的条件：只当判据阈值与 $\Phi'<0$ 的等价阈值一致时才成立。逐项展开给 $\Phi'<0\iff\Phi S<4Th\delta\iff\Phi<2r\iff\lambda<\dfrac{2\delta}{1-\delta}$，而 $G>0\iff\lambda<\dfrac{\delta(1+\delta)}{1-\delta}$；因 $1+\delta<2$，判据阈值**严格更小**，故"$\Phi$ 单调"能保证的区间比判据所需更宽，无法反推 $G$ 的符号。判决：**撤销"$\Phi$ 的单调性可判 $G$"**，改判为"判 $\delta$ 与 $\lambda$ 的比较"（$\lambda=1/(T\sinh\frac1T)$ 为纯 $T$ 显式函数，$R(\delta)=\delta(1+\delta)/(1-\delta)$ 只读 $\delta$） | 卡 §三十五 35.3 末段、35.7；`Ring15Spec.lean` v29（`deficitFrac`／`endpointLambda`／`TargetPropShapeSignDeficit`）；`Ring15LockDeficit.lean`（`targetPropShapeSignDeficit`）；`环15_判据δλ_数值核对_输出.txt`（$R-\lambda$ 在 $T=0.3435$ 仅 $+2.61\times10^{-4}$，近相切） |
| 202（工具坑） | 五处：① `refine intervalIntegral.integral_mono_on (a:=…) (b:=1) … hcont.intervalIntegrable 0 1 ?_ ?_` 里未加括号的 `.intervalIntegrable 0 1` 被 refine 拆成**三个独立参数**，报"numerals are data…"——须写成 `(hcont.intervalIntegrable 0 1)`；② `pow_le_pow_left` 在 v4.29.1 基线不存在，平方保序用 `nlinarith [hc, hx, hy]`；③ 分式不等式的引理名是 `div_le_div_iff₀`／`div_lt_div_iff₀`（旧名 `div_*_div_iff` 已删，报 unknown identifier）；④ `field_simp` 常已闭合目标，其后 `ring` 报 `No goals to be solved`（`ratio_integral`／`targetPropLambdaForm` 各一处）；⑤ `shapePhi` 与 `shapeH` 的分母是同一表达式但**不能 `unfold shapePhi` 后直接与 `shapeH T` 对齐**（目标里出现的是 `Real.tanh (1/(2*T))` 而定理要 `shapeH T`），须先 `have hΦeq : shapePhi T = wGap T / shapeH T := rfl` 再 `rw [hΦeq, div_lt_one hh0]` | 不成立的条件：以为这些写法在 Spec v29 基线下可用 | `Ring15LockDeficit.lean` 编译记录（四轮报错，逐条改后 exit 0）；`a_gate.ps1` 二十九模块 PASS（62 条 axioms／57 条 `#check`／258 文件 0 命中／exit 0） |
| 203 | 「两侧各自严格单增（$\lambda$ 单增、$R(\delta(T))$ 单增）即可给出交点 $T_{\min}$ 的位置」——202 收尾时打算靠这两条单调性直接编址 $T_{\min}$ | 不成立的条件：只当两函数的**增速关系**已知时才成立。两侧同向单增只能保证"若相交则交点唯一"，不能定位交点：$d\lambda/dT$ 与 $dR/dT=R'(\delta)\delta'(T)$ 谁大才决定 $R-\lambda$ 的走向。数值上 $\frac{d\lambda}{dT}-\frac{dR}{dT}$ 在 $T\approx0.19415$ 变号一次（$T=0.15$ 差 $-0.4629$：$R$ 增得快；$T=0.3439$ 差 $+0.7305$：$\lambda$ 增得快），而 $R(\delta(T))$ 的单增本身还依赖 $\delta(T)=1-\Phi(T)$ 单增，$\Phi'$ 至今未进 Lean。判决：**撤销"两侧单调性可直接编址 $T_{\min}$"**；两条单调性按本轮定理保留（它们仍是远区定号的前件），交点记 **G-188b-2i**，须另立增速比较或 $\delta(T)$ 的链内单调＋显式包络 | 卡 §三十六 36.3 末段、36.7；`Ring15Spec.lean` v30（`TargetPropLambdaStrictMono`／`TargetPropDeficitRatioMono`／`TargetPropLambdaBounds`）；`Ring15LockLambda.lean`；`环15_判据两侧单调性_数值核对_输出.txt`（变号点 $T\approx0.19415$、$T_{\min}=0.343857873$） |
| 203（工具坑） | 七处：① `intervalIntegral.integral_pos` 首参要求 **`0 < b`**（不是 `0 ≤ b`），传 `hx.le` 报 "expected 0 < x"；② 用 `Real.abs_tanh_lt_one`＋`sq_abs` 去证 $\mathrm{sech}^2\frac{x}{2}<1$ 失败（`linarith` 无矛盾），改用 `div_lt_one (pow_pos (Real.cosh_pos _) 2)`＋`Real.cosh_sq`＋`nlinarith`；③ `strictAntiOn_of_hasDerivWithinAt_neg` 的隐式 `f'` 无法合成（报 "don't know how to synthesize implicit argument f'"），须显式传 `(D := …) (f := …) (f' := …)`；④ `StrictAntiOn` 的参数序是 $(x\in s)(y\in s)(x<y)\Rightarrow f\,y<f\,x$，故要证 $\lambda(T_1)<\lambda(T_2)$ 必须传 $x=1/T_2$、$y=1/T_1$（写成 `F_strictAnti hu1 hu2 hlt` 会报 $1/T_2<1/T_1$ 与 $1/T_1<1/T_2$ 不符）；⑤ `positivity` 证 `show (0:ℝ) < 1/T₁` 失败（把 `1` 当字面量），改 `one_div_pos.mpr h1`；⑥ `div_lt_one` 必须在**未化简的分式**形态上重写——先 `field_simp` 会把 $1/(T\sinh)$ 化成别形，导致 `rw` 找不到模式；⑦ `Set.interior (Set.Ioi 0)` 的成员类型是 `x ∈ interior` 而非 `0 < x`，须 `have hx' : (0:ℝ) < x := by simpa using hx` 才能喂给已证引理 | 不成立的条件：以为这些写法在 Spec v30 基线下可用 | `Ring15LockLambda.lean` 编译记录（三轮报错、逐条改后 exit 0）；`a_gate.ps1` 三十模块 PASS（65 条 axioms／60 条 `#check`／259 文件 0 命中／exit 0） |
| 204 | 「$\delta$ 的单调性必须先把 $\Phi'$ 单独搬进 Lean 才能判——$\Phi'$ 是独立缺口」——197–203 一直把"$\Phi'$ 未进 Lean"当作 $T_{\min}$ 编址的阻塞点 | 不成立的条件：只当 $\delta$ 与 $\Phi$ 不是同一函数的平移时才需要 $\Phi'$ 独立形式。$\Phi=1-\delta$ 给 $\Phi'=-\delta'$，故 $\Phi'$ 的符号与 $\delta'$ 的符号**同一条定理**即可给出；而 $\delta'$ 本身有纯商法则闭式 $\delta'=-\left(w'h+w\,\mathrm{sech}^2\frac1{2T}/(2T^2)\right)/h^2$，不需要新的积分估计。判决：**撤销"$\Phi'$ 需独立入 Lean"**；`Ring15LockDeficitMono` 的 `targetPropDeficitDeriv`＋`targetPropDeficitDerivPos` 一并给出 $\delta'$ 闭式与符号，$\Phi'$ 降为 $\delta'$ 的推论（口径表 204 条） | 卡 §三十七 37.3–37.4；`Ring15Spec.lean` v31（`deficitDeriv`／`TargetPropDeficitDeriv`／`…DerivPos`／`…StrictMono`／`…RatioStrictMonoT`）；`Ring15LockDeficitMono.lean`；`环15_δ导数与核不等式_输出.txt`（$\delta'$ 闭式 vs 差分 rel $3.1\times10^{-11}\sim1.2\times10^{-9}$、负值点 0） |
| 204 | 「点位不等式 $\sinh(us)\le u\sinh s$ 需要 Mathlib 的 $\sinh$ 凸性引理（`ConvexOn ℝ (Ici 0) Real.sinh` 之类）」——写证明前先查基线库有无此引理 | 不成立的条件：$s>0$、$u\in[0,1]$ 的比较只有凸性一条路。判法改用**比值函数** $F(s)=\sinh s/s$：$\sinh(us)\le u\sinh s\iff F(us)\le F(s)$，而 $F$ 在 $(0,\infty)$ 严格增由 $F'=\frac{s\cosh s-\sinh s}{s^2}>0$，后者等价于 203 已证的 $\tanh s<s$。判决：**撤销"必须找 sinh 凸性引理"**（基线库 `ConvexOn`＋`Real.sinh` 组合查无），比值路线全链在 `Ring15LockDeficitMono` 内自足（`sinh_ratio_strictMono`／`sinh_smul_lt`／`sinh_smul_le`）；数值 $s\in\{0.5,1,2,3.3333,10\}$ 各 2001 点 0 违反 | `Ring15LockDeficitMono.lean`；`环15_δ导数与核不等式_输出.txt`（点位不等式最大超出 0） |
| 204（工具坑） | 六处写法陷阱：① `intervalIntegral.integral_pos` 裸名不可见（本环境无 Mathlib 伞模块），须全名 `intervalIntegral.integral_pos`，且其论域是 `Ioc a b`、第四参是 `∃ c ∈ Icc a b`——故第三参（非负）必须能覆盖 $u=1$，只能用非严格版点位不等式；② `convert` 不可用（不在内核），函数/值两处不等都要靠 `have hfun`／`have hval`＋`rw … at h`；③ `HasDerivAt.const_mul` 的首个显式参数是**常数**，方法式 `hinv.const_mul (1/2)` 会把 `hinv` 塞进常数位，须写 `HasDerivAt.const_mul (1/2) hinv`；④ `StrictMonoOn` 的 $a,b$ 是隐式绑定，普通应用时成员证明先于 $b$ 定值会造出元变量（报 `0 < ?m`），须 `@hmono a ha b hb hlt`；⑤ 成员证明不能拿 $T_1<T_2$ 顶 $0<T_2$（`simpa using h2` 必失败），须 `lt_trans h1 h2`；⑥ `field_simp` 已闭合目标时后接 `ring`／`try ring` 报 `No goals to be solved`（沿用 198–203 老坑），本轮统一改为 `field_simp` 后 `try ring` | 不成立的条件：以为这些写法在 Spec v31 基线下可用 | `Ring15LockDeficitMono.lean` 编译记录（五轮报错，逐条改后 exit 0、零告警）；`a_gate.ps1` 三十一模块 PASS（69 条 axioms／64 条 `#check`／exit 0） |
## 第 205 轮（G-188b-2j 前件：判据差的导数结构）

### 205-1　"两侧单增即可推 $D$ 单峰"——不成立
- **内容**：曾把 $\lambda$ 严格单增（203）＋$R(\delta(\cdot))$ 严格单增（204）当作"交点唯一"的充分依据，并预期由此读 $T_{\min}$ 的位置。
- **不成立的条件**：两函数各自单增只给"若相交则唯一"，对**差函数** $D=R-\lambda$ 无形状信息。$D$ 的形状由 $D'=R'\delta'-\lambda'$ 的符号决定，而 $D'$ 并非恒正：205 数值上 $D'$ 在 $T\approx0.19415$ 变号（左侧 $+0.4629$、右侧 $-0.7305$），$D$ 因此单峰而非单调。故"单增 ⇒ 单峰/定位"在 $T\lesssim0.2$ 段即失效。
- **依据**：204 卡 §37.7 已撤销"两侧同增可编址"；205 数值 `环15_判据差导数_输出.txt` §[3][4]；$D'$ 闭式见 Spec v32 `criterionGapDeriv`。
- **处置**：交点编址转 **G-188b-2k**（须 $D'$ 单减／$D''<0$），$T_{\min}$ 数值只留反馈层。

### 205-2　"$\Phi$ 或 $D$ 的形状可由既有单调性定理直接读出"——撤销
- **内容**：一度设想用 203 的 `TargetPropLambdaStrictMono` 与 204 的 `TargetPropDeficitRatioStrictMonoT` 直接合成 "$D$ 有唯一零点"的命题。
- **不成立的条件**：两条定理只给一阶信息（各自递增），合成不出二阶信息（$D''$ 的符号）。在 $D'$ 变号的两侧都满足"两侧递增"，故该合成在任何区间上都成立，**无法区分** $D'$ 的正负——这是典型的语义不足（借了符号没借语义）。
- **处置**：205 不再尝试该合成；改走"先把 $D'$ 的闭式进链"（本轮完成），二阶留给 206。

### 205-3　Lean 写法坑（第 205 轮新增，先记后删）
- `1 / T` 与 `T⁻¹` 在 Lean 里不是 defeq（`one_div` 只是等式）：`HasDerivAt.comp` 会按外层函数的取值点把内函数猜成 `fun x => 1/x`，与 `fun x => x⁻¹` 冲突而报 "Application type mismatch"。处置：全程统一 `T⁻¹` 写法，最后用 `one_div` 一次性换回 `1/T`。
- `HasDerivAt.add`／`.sub`／`hasDerivAt_const` 给的是**函数和**形态 `((fun _ => c) + id)` 与值 `0 + 1`／`0 - 1`：直接 `exact` 会报 type mismatch。处置：`funext`＋`norm_num` 显式换成 `fun y => 1 + y` 与 `1`。
- `HasDerivAt.mul` 的值里 `id x` 不自动归约为 `x`：须 `simp only [id_eq]` 后再 `ring`。
- `HasDerivAt.comp` 的复合值把 `((fun s => sinh s) ∘ Inv.inv) T` 原样保留：值恒等须按该形态写（`simp only [Function.comp_apply, id_eq, one_mul]`），不能按 `sinh (T⁻¹)` 写。
- 跨模块 `private` 引理不可见（`shapeH_pos`、`deficit_lt_one`、`deficit_eq` 都在 `Ring15LockDeficitMono` 内私有）：须在本模块以 `'` 后缀本地重证，不得改原模块的 private 状态。
- `congr_of_eventuallyEq` 的方向是"新函数 =ᶠ 旧函数"：`TargetPropLambdaForm` 给的是 `endpointLambda = 1/(T sinh(1/T))`，直接用（勿 `.symm`，否则 type mismatch）。
## 第 206 轮

### 206-1　"$D'$ 在 $(0,\infty)$ 严格单减（$D''<0$）"——不成立，撤销

**内容**：205 停点把 $G$-$188b$-2k 的强意图写成"须证 $D'$ 在 $(0,\infty)$ 严格单减，或给出分段判据"。本轮实算否证前者。

**不成立的具体条件**：在 $T\in[0.03,1.50]$（3001 点，$\Delta T\approx4.9\times10^{-4}$）上：
- $D'$ 在 $T<0.3529$ 段递减、在 $T>0.3529$ 段**递增**，极小 $D'(0.3529)=-0.731863$；故 $D'$ 是 U 形，不单调。
- $D''$ **变号两次**：$\approx0.1099$（$+9.9\times10^{-4}\to-1.37\times10^{-1}$）、$\approx0.3529$（$-3.08\times10^{-3}\to+1.19\times10^{-2}$）。
- 端点值 $D'(0.10)=+0.654548$、$D'(0.20)=-0.060387$、$D'(1.20)=-0.086352$、$D'(1.50)=-0.047045$。

**依据**：`04_计算验证/环15_判据差二阶_数值核对.py` 与同名 `_输出.txt` §[1][2]；`04_计算验证/环15_判据差二阶_数值核对.png` 面板 (b)(c)。

**替代**：意图命题改写为"$D'$ 在 $(0,\infty)$ 上**恰有一个零点**"（等价于 $D$ 单峰且极大唯一）。该弱命题在数值上成立（$T^*=0.194153703$，零点数 1），但尚未证明。

### 206-2　"由 $\lambda''$ 的符号给 $D''$ 定号"——不可行，撤销

**内容**：205 停点把"最该修"定为"$\delta''$ 与 $\lambda''$ 的闭式及其符号"，隐含"$\lambda''<0$ 可助 $D''<0$"。

**不成立的具体条件**：$\lambda'(T)$ 是**钟形**（两端趋于 0）：$\lambda'(0.05)=3.1\times10^{-5}$、$\lambda'(0.29509)=1.859783$（极大）、$\lambda'(1.50)=0.089202$；故 $\lambda''$ 在峰两侧**必然变号**，不能为 $D''$ 提供定号。同一事实也排除"$\delta'$ 单减"：$\delta'(T)$ 在 $[0.03,1.5]$ 上出现 290 段上升，$\delta''$ 同样变号（$\delta'(0.15)=0.838648$、$\delta'(1.20)=0.023719$）。

**依据**：同上脚本 §[4][5]；图面板 (a)。

**替代**：二阶路线不能作为判据主体。$D'$ 的零点唯一性须回到**两条一阶单峰曲线的比较**（$P(T):=R'(\delta(T))\delta'(T)$ 与 $\lambda'(T)$，后者的峰在 $T=0.2951$，前者峰位待定），而不是对 $D$ 直接求二阶。
### 209-1　"$\tanh$ 凹性可直接从 Mathlib 现成 API 取用"——不成立，撤销该路线

**内容**：207／208 把 $\delta<\frac13$ 的入口写成"$\tanh$ 凹性／割线"，并倾向"先引一条 Mathlib 的凹性引理再拼"。

**不成立的具体条件**：本轮逐项检索 Mathlib（Lean 4.29.1／本工程 `.lake/packages/mathlib`）确认：`hasDerivAt_tanh` **全库 0 命中**（tanh 的导数在链内是 190／196 轮自建的，不在 Mathlib）；tanh 的 `ConcaveOn`／`StrictConcaveOn` **0 命中**；可用的只有通用判据 `concaveOn_of_hasDerivWithinAt2_nonpos`（`Mathlib/Analysis/Convex/Deriv.lean` L248）与 `concaveOn_of_deriv2_nonpos`（L223），两者都要求先给出 $f'$、$f''$ 的 `HasDerivWithinAt`。因此"引一条现成凹性引理"这条路**在 $\tanh$ 上不成立**。

**依据**：`Mathlib` 内 `Grep` 结果（0 命中）；`Analysis/Convex/Deriv` L223／L248 的签名；`Ring15LockW.lean`／`Ring15LockWD.lean` 中已自建的 `hasDerivAt_tanh`／`hasDerivAt_tanh'`（仅一阶）。

**替代**：凹性路径改记为**四件工程**：①自建 $\tanh'=\mathrm{sech}^2$（链内已有，可复用）；②对 $\mathrm{sechSq}(a u)$ 复合求二阶导；③用 `concaveOn_of_hasDerivWithinAt2_nonpos` 得凹性；④由凹性＋端点为零得割线不等式 $\tanh(au)\ge u\tanh a$。在此之前，$\delta\le\frac13$ 不得以"显然"或数值替代。
### 210-1　"先建 tanh 的 `ConcaveOn`、再由凹性取割线"——不作为本轮路线，改走一阶判据

**内容**：209 的替代方案把 $\delta\le\frac13$ 写成"四件工程"，第三件是用 `concaveOn_of_hasDerivWithinAt2_nonpos` 建凹性，第四件由凹性转割线。

**在何条件下不划算**：Mathlib **没有**"`ConcaveOn` ⇒ 割线"的一键引理；要自己写 $f(ux+(1-u)y)\ge uf(x)+(1-u)f(y)$ 的实例化，且 `concaveOn_of_hasDerivWithinAt2_nonpos` 还要求 $f'$、$f''$ 两条 `HasDerivWithinAt`（二阶导链比一阶长一倍）。也就是说，该路线的真实成本是"二阶导＋凹性＋割线转换"三层，而实际只需要 $[0,1]$ 段的**一条**割线。

**依据**：（本轮检索）`Mathlib/Analysis/Convex/Deriv.lean` L223／L248 的签名；`ConcaveOn` 相关引理清单中无"凹性 ⇒ 割线"直接可用的名字；`Ring15LockSecant.lean` 的 `tanh_secant_core` 用一阶判据把全部工作压到 `strictAntiOn_of_hasDerivWithinAt_neg` 一行。

**替代（已落地）**：$g(u)=\tanh(au)/u$ 严格减。$g'$ 分子 $=y\mathrm{sech}^2y-\tanh y\iff y<\sinh y\cosh y\iff2y<\sinh(2y)$，后者由 `Real.sinh_two_mul`＋`Real.sinh_sub_id_strictMono` 给出；$u<1$ 时 $g(1)<g(u)$，乘 $u>0$ 即得割线。若后续确需**严格**凹性（例如用于 $u>1$ 段或 Jensen），再回到 `ConcaveOn` 路线——本条只否决其**作为当前入口**，不否决其数学正确性。
### 211-1　"$D'/D$ 首项展开定近零端符号"（未采用作当前入口）

- **内容**：想用 $T\downarrow0$ 的渐近式（$w'\sim-\frac1{3T^2}$、$\lambda\to0$、$\delta\sim$ 某常数 $\cdot T^2$）直接读 $D$ 的首项符号。
- **在何条件下不成立**：该路线要求 **$w'$ 与 $\delta$ 的 $T\downarrow0$ 渐近常数已进链**；现状（211 前）只有 $w$ 的单调性与 $|w'|$ 的积分表示，没有任何渐近常数定理。缺此前件时，"首项"只能由数值拟出，等于用曲线反推方程——与第 5 层禁令冲突。
- **改用**：只用可证的一侧界（$\mathrm{sech}^2z\ge1-z^2$ 于 $z\le1$、$\sinh s\ge3s^3$ 于 $s\ge10$）得 $\delta\ge\frac8{15}T^2$、$\lambda\le\frac{T^2}{3}$，合得 $D\ge\frac{T^2}{5}>0$；不引入任何拟合常数。
- **保留条件**：若后续把 $w'$、$\delta$ 的 $T\downarrow0$ 渐近常数作为**独立定理**证出，可重启该路线，用于给出 $D$ 的**渐近常数**（而不是符号）。
### 212-1　"用 $D$ 的单调性／单峰性直接给出零点存在"（未采用作存在性入口）

- **内容**：若已知 $D$ 在 $(0,1)$ 上先增后减（单峰），可由 $D(0^+)=0$、$D(\frac1{10})>0$、$D(1)<0$ 立刻读出"存在零点"。
- **在何条件下不成立**：该路线要求 **$D$ 的单峰性（或 $D'$ 恰一零点）已在链内**；现状只有 205 的 $D'$ 闭式，无任何符号分段定理。数值反而给出更强的反证：$D'$ 是 U 形（$+0.6545$ 于 $0.10$；$-0.7319$ 于 $0.3529$；$-0.0470$ 于 $1.50$），$D''$ 在 $(0.03,1.5)$ 内变号两次，故"$D$ 单增／单减"连数值都不成立；把单峰当默认前提即"用曲线反推原理"，与第 5 层禁令冲突。
- **改用**：只用"连续＋两端异号"（205 可微性 ⇒ 连续；211 于 $T=\frac1{10}$ 正；210 于 $T=1$ 负）经 `intermediate_value_Icc'` 给存在，再以严格不等号排除端点。存在性**不**消费任何单调性信息。
- **保留条件**：若后续把 $D'$ 在 $[\frac1{10},1]$ 上的符号分段（或恰一零点）作为**独立定理**证出，可把它与 212 的存在性合成**唯一性**；届时不是"用单峰证存在"，而是"用符号分段把已证的存在升为唯一"。
### 213-1　"用 $D'$ 在 $[\frac1{10},1]$ 上的左正右负分段给出零点唯一"（未采用）

- **内容**：212 停点设想：若 $D'$ 在 $(\frac1{10},T^*)$ 为正、在 $(T^*\!,1)$ 为负，则 $D$ 先增后减，配合两端符号可读"恰一零点"。
- **在何条件下不成立**：该分段要求 **$D'$ 在该区间至多一次变号**。本轮数值核对直接否证：$D'$ 在 $[\frac1{10},1]$ 上**先增后减**（极大 $0.668035$ 于 $T=0.110$、极小 $-0.731863$ 于 $T=0.353$），$D''$ 变号两次（$\approx0.10987$、$\approx0.35301$）。且 $D'$ 的唯一零点在 $T=0.194154$，而 $D$ 的零点在 $T=0.343858$：**"$D'$ 恰一零点"与"$D$ 恰一零点"不是同一命题**，前者不能直接换成后者。
- **改用**：把 $D=0$ 改写为 $Q:=\lambda/R(\delta)=1$，把唯一性归约为"$Q$ 严格单增 $\Rightarrow$ 至多一解"；先落成**条件句**（v38 `TargetPropGapZeroUniqueOfRatioMono`，A 闸通过），再单独立"$Q$ 严格单增"为缺口 **G-188b-2k-u**。
- **保留条件**：若后续**独立**证出 $D'$ 在 $[\frac1{10},1]$ 上恰一零点，并另证 $D$ 在该零点右侧的符号，可把该路线作为唯一性的**第二条独立路径**（交叉校验），但不得用它替代 $Q$ 单调性命题，也不得把两者混为一谈。
### 214-1　"$Q$ 的乘法闭式 $Q=\mathrm{sech}^2\frac1{2T}\,w/\big(2T(h-w)(2h-w)\big)$ 作为本轮锁定命题"（未入 Spec）

- **内容**：把 $Q=\lambda/R(\delta)$ 的除法改写成乘法形态（把除 $R$ 换成除 $(h-w)(2h-w)$），作为下一步单调性逐因子估界的形式准备。
- **在何条件下不成立（形式化侧，非数学侧）**：代数上该式**正确**（$R=(h-w)(2h-w)/(hw)$ 由 $\delta=(h-w)/h$、$1-\delta=w/h$、$1+\delta=(2h-w)/h$ 直接给出）；但本轮只走"`unfold` 定义 → `field_simp` → `ring`"的路径，收尾残式恒为
  `sechSq*tanh*w*(2tanh−w)⁻¹*2 − sechSq*w²*(2tanh−w)⁻¹ = sechSq*w`，
  `ring`／`ring_nf`（不识别逆元）、`← sub_div`＋`div_eq_iff`（形态是单个除法而非两除法相减）、`apply mul_right_cancel₀ h2`（再 `field_simp` 又回到同一逆元形态）均不闭合。即：**"逆元消去＋多项式归一"这一路在 $(2h-w)^{-1}$ 因子处不成立**，不是命题为假。
- **改用**：本轮只锁**正性**两条（`TargetPropDeficitRatioPos`、`TargetPropRatioOverLambdaPos`），Spec v39 不含乘法闭式；闭式的形式化留待"分因子恒等式（分子恒等于 `sechSq*w*(2h−w)`）＋分母非零消去"两步写法，或改用 `div_eq_iff` 直接对原始分式。
- **依据**：`05_Lean验证/Ring15LockRatioForm.lean` 的失败残式与 tactic 报错（`ring` 提示改 `ring_nf` 后仍不过；`mul_right_cancel₀` 后 `field_simp` 复原）；`Ring15LockZeroUnique.lean` 的 `unfold criterionGap` 写法可作对照。
- **保留条件**：一旦两步写法（分子恒等 `have key : … := by ring` ＋ `rw [key, mul_assoc, mul_inv_cancel₀ h2, mul_one]`）在独立测试文件中闭合，可把闭式作为**独立定理**补进 v40，并在口径表登记；但它**不**替代 $Q$ 严格单增（G-188b-2k-u）。
## 216-1　"以 $\delta'\le C/T^2$ 作为 $Q$ 单调性的入口"（第 216 轮）

- **放弃内容**：把 215 记下的子缺口 G-188b-2k-u-1（$\delta'\le C/T^2$，$C\le0.0596$）当作证 $Q$ 严格单增的必需入口。
- **在何条件下不成立**：$C$ 的可行窗口由数值定为 $[\sup T^2\delta',\;0.0596]=[0.059019,\;0.0596]$，宽 **1%**（$\sup T^2\delta'=0.059019$ 于 $T=0.4250$）。任何解析粗界——例如由 $\tanh s\ge s-\frac{s^3}{3}$ 得到的 $C\approx0.1$——都落不进窗口；故在这条入口上"再算细"等于要求一条几乎锐利的上界，与"由原理推不等式"的工作方式不符。
- **依据**：`04_计算验证/环15_δ渐近系数_输出.txt` §[2][3]；纸面展开 $\delta=\frac13-\frac{1}{45T^2}+O(T^{-4})$（系数 1/45 数值四位有效）。
- **保留条件**：若日后出现误差 <1% 的 $\delta'$ 锐利上界（例如由 $(T,h)$ 的有理式直接给出），此入口可复活；否则不作必需环节。
- **替代入口**：$G(T):=\lambda'R(\delta)-\lambda R'(\delta)\delta'>0$ 的代数判号（记为 G-188b-2k-u-2；三段闭式均已在链内，数值余量 $(\ln Q)'\ge0.098536$，精度需求约 10%）。
---

## 221-1　七阶双界的"上下归属"写法（220 停点版）——作废

- **被作废的内容**：220 停点与 §五十三 把七阶双界登记为
  "$\tanh s\le s-\frac{s^3}{3}+\frac{2s^5}{15}-\frac{17s^7}{315}$、$\tanh s\ge$ 该式 $+\frac{62s^9}{2835}$"。
- **不成立的具体条件**：$0\le s\le1$（$\tanh$ 幂级数在此收敛、且项绝对值单调递减）时的**交错级数部分和奇偶归属**。
  $s=0.5$ 数值：$S_3=0.462078373$、$\tanh 0.5=0.462117157$、$S_4=0.462121087$ ⇒ $S_3<\tanh<S_4$，
  与"$S_3$ 是上界"矛盾。末项为负的部分和位于真值**下方**、末项为正的位于**上方**。
- **依据**：`04_计算验证/环15_七阶双界_数值核对.py`（`tanh-L` 最小 $-8.674\mathrm{e}{-19}$、`U-tanh` 最小 $-6.939\mathrm{e}{-18}$，均在浮点误差量级）。
- **替代**：$S_3\le\tanh s\le S_4$（$S_4=S_3+\frac{62s^9}{2835}$）；$S_3$ 已于第 221 轮落成定理 `tanhSepticLower`（Spec v44），$S_4$ 留第 222 轮。
- **删除原因**：错误方向若被 222 当作"上界"使用，会把 $w$ 的下界当上界、$h$ 的上界当下界，得到"看似更紧"的假进展且类型检查照过（跑偏式）。先在账本记录再改，防污染。
---

## 222-1　$\int_0^s\frac{34t^8}{315}$ 的常数（首次写法）——作废

- **被作废的写法**：第 222 轮首版把 $\int_0^s\frac{34t^8}{315}$ 写成 $\frac{34s^9}{315}$。
- **不成立的具体条件**：任何 $s\ne0$（$\int_0^s t^8\,dt=\frac{s^9}{9}$ 是 `integral_pow` 的直接结果，$\frac{34}{315}\cdot\frac19=\frac{34}{2835}$）。
- **依据**：`Ring15LockTanhSepticUb.lean` 的 `hsplit` 首次编译在
  `rw [hm, hInt8]` 后留下目标 `34 * (s ^ 9 / 9) / 315 = 34 * s ^ 9 / 315`，`ring` 报失败（两侧相差 9 倍）；改右端为 $\frac{34s^9}{2835}$ 后 `ring` 立即闭合。
- **替代**：$\frac{34s^9}{2835}$；由此 $s^9$ 合成 $-4/405-34/2835=-62/2835$ 与幂级数系数 $\frac{62}{2835}$ 对齐。
- **删除原因**：该错误若留到下游（例如把 $-\frac{62}{2835}$ 写成 $-\frac{4}{405}-\frac{34}{315}$），结论数值会偏大约 $\frac{34}{315}(1-\frac19)\approx0.0977$ 的 $s^9$ 量级，而类型检查照过——正是"跑偏式"的典型入口。---

## 223-1　$\delta'_{\rm ub}$ 的"复合式重复扣减"（数值脚本首版）——作废

- **被作废的写法**：`04_计算验证/环15_w七阶双侧界_数值核对.py` 首版把闭式
  $\delta'=\frac{2(h-w)}{Th}-\frac{w(1-h^2)}{2T^2h^2}$ 记成 `dl = 2*(hu - w_lb)/(T*hu) - K_lb`，
  然后**又**写 `return 2*deficit_ub(T)/T - dl`，相当于把 $\frac{2h}{Th}=\frac2T$ 与 $\frac{2w}{Th}$ 拆开各扣一次。
- **不成立的具体条件**：任何 $T>0$。$T=1$ 时该式给 $\delta'_{\rm ub}=0.585100$，而闭式真值 $0.039592$（相差 14.8 倍）；
  判号表随之在全域 FAIL（$A_{\rm lb}=0.3130$ vs 积 $3.17$），与 220 的精度定量（允许域 $1.43$–$1.46$ 倍）自相矛盾。
- **依据**：`环15_w七阶双侧界_输出.txt` 首版（表 2 的 `ratio` 列 $3.36\ldots374.8$、表 3 全 FAIL、表 4 最小余量 $-3.24$）；
  改用正确复合上界 $\delta'_{\rm ub}=\frac{2(h_{\rm ub}-w_{\rm lb})}{T\,h_{\rm lb}}-\frac{w_{\rm lb}(1-h_{\rm ub}^2)}{2T^2h_{\rm ub}^2}$ 后，
  比值落回 $1.0000$–$1.4634$、判号全域 PASS。
- **替代**：上式（分母对第一项用 $h_{\rm lb}$、对减项用 $h_{\rm ub}$，方向各自为"放大"）；同时 $T=0.5$ 处 $\frac{\delta'_{\rm ub}}{\delta'}=1.4634$ 略超 220 的 $1.46$ 上端，属预期边界效应，不再收紧。
- **删除原因**：该错式会让"判号可行"被误判为"全域不可行"，从而误弃七阶路线、退回五阶界重做——是**方向相反**的跑偏，比数值偏大更危险；且错误来自把"已含减项的闭式"当成"待减的正项"，同类错误在下游合成时极易复发。
---

## 223-2　`a_gate.ps1` 的 `type` 判定分支被覆盖（扩闸时的编辑事故）——作废

- **被作废的写法**：本轮把闸脚本由四十五模块扩到四十六模块时，用"整行替换＋按行拼接"改动 `$check` 数组，
  误把 `elseif ($s -match "^\S+ : ") { Write-Output "[ ok ] type: $s" }` 这一行覆盖掉（同时把数组尾部一个元素挪出了引号区）。
  首次实跑输出 `[ ok ] axioms` 109 条、`compile` 46 条，但 `[ ok ] type` **0 条**，末行仍打印 PASS。
- **不成立的具体条件**：任何一次闸运行——`type` 分支缺失时，#check 结果既不计入通过数、也不产生 FAIL，
  等于"类型对齐"这一维被静默跳过（而 `_a_gate_out.txt` 中 91 条 `#check` 结果当时齐全且无 error，所以那一次**不是假 PASS，是报告漏计**）。
- **依据**：`_agate223.log`（首跑）`type` 计数 0、`FAIL` 0、`compile` 46、`axioms` 109；`_a_gate_out.txt` 含
  `CQM.Ring15.LockWGapSeptic.targetPropWGapUpperBound : CQM.Ring15.Spec.TargetPropWGapUpperBound` 且无 error 行。
- **替代**：恢复 `elseif` 分支（置于 axioms 分支之后、`sorryAx` 分支之前）并用
  `[System.Management.Automation.Language.Parser]::ParseFile` 校验脚本零语法错误后重跑，得 compile 46/46、axioms 109/109、type 91/91、FAIL 0。
- **删除原因**：闸脚本是 A 闸唯一执行体，其"报告维度"缺失会让后续轮次误以为类型对齐已被覆盖；且此次事故出在"按行号拼接"这一编辑手法上，必须记账以免再用。