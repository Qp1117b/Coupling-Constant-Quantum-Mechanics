# PROGRESS：已确认成果 / 推进工作 / 每环四元组 / 复现命令



> 双账本之一。只登记**已落到工作台、Lean 或数值**的结论，不把工作假设升格为定理。

> 状态口径沿用 `00_当前有效口径表.md` 的 A/B/边界分区；本文件不替代该表。

> 目录边界：本文件及全部产出仅在 `10 探索/超导第一性研究/` 内。



## 〇、版本与依赖基线



- Lean 版本：4.29.1（`@Lean version`）；Mathlib 经 `08 理论组织和形式化框架/04_Lean对接/Lean源码/lakefile.toml` 提供。

- 编译命令（在 Lean源码 目录执行，文件用绝对路径）：

  `lake env lean "D:\WorkSpace\物理\CQMFormal\10 探索\超导第一性研究\05_Lean验证\<文件>.lean"`

- 组织层核查：`python "08 理论组织和形式化框架/_build/check_consistency.py"`（`41/41`）、`check_provenance.py`（`215/215`）。

- 环 15 Spec 基线：`05_Lean验证/Ring15Spec.lean` **v46**（第 223 轮，在 v45 之上新增 `wGapLowerSeptic`／`wGapUpperSeptic` 两 def 与 `TargetPropWGapLowerBound`（∀ T≥1/2, w_lb(T) ≤ w(T)）／`TargetPropWGapUpperBound`（∀ T≥1/2, w(T) ≤ w_ub(T)）；v45 段为 `TargetPropTanhSeptic`（∀ 0≤s≤1, tanh s ≤ S_3+62s⁹/2835）；v44 段为 `TargetPropTanhSepticLower`；v43 段为 `TargetPropDeficitLeThirdSubSq`；v42 起为 `TargetPropTanhQuintic`、v41 三阶界、v40 `deficitDerivAlt` 与三条 δ′ 命题、v39–v32 段全部保留）；模块 **四十六**（45→46 新增 `Ring15LockWGapSeptic`）；A 闸脚本 `05_Lean验证/a_gate.ps1` 覆盖**四十六**模块（`#print axioms` 109 条、`#check` 91 条）；第 219 轮实跑 PASS（43/43、103/103、88/88），第 221 轮 v44 PASS、第 222 轮 v45 PASS、**第 223 轮 v46 实跑 PASS（46/46 编译、109/109 公理白名单、91/91 `#check`、FAIL 0、token 276 文件 0 命中、exit 0）**（见 §五）。


## 一、骨架与当前缺口（第 0 步接续）



27 环发生学骨架见 `../CQM_探索_推导链.md`；本目录权威收束见 `00_当前有效口径表.md`。

当前活跃环与未闭合缺口（状态均「未闭合」，唯一编号 37、闭合数 0）：

- 环 4：`W-3′`／`审-3`（$\rho$ 形状、$\sigma_0$ 标度）；第 157 轮给 $\rho_{nn}$ 链内归一。

- 环 15：`审-4`（座→键映射）、`审-6`（锁定整数、$E_c$／$\gamma$、和乐映射）、`M8`（相界）。第 162 轮已把 `审-6` 的**键级口径**形式化（`Ring15Spec` v2 + `Ring15LockMult`，A 闸通过），第 163 轮把**锁定概率复合**形式化（$p_{\rm lock}=(1-y)^m$，A 闸通过），第 170 轮把**独立键前提的授权层**钉到条件层并算出偏差 $\rho=0.372154$，第 173 轮把该授权层**形式化落盘**（`Ring15Spec` v3 + `Ring15LockLayer`，A 闸通过）；第 185 轮回读 (161.1)–(161.5) 后**重开该段**：判最早失配在 `(161.4)` 第二等号（前件是已被第 138 轮撤销的 (4.1) 第一项，且把 $\Upsilon$ 冻成 $\Upsilon_0$），据此把 $y$ 的 $T$ 依赖归还刚度（(15L.3)＋(19W.8)）、把 $\sigma_\theta$ 降为恒等，`审-6` 残余改记为「$b\,n_d(T_c)$ 材料量／$s$／$\Phi$／$\Upsilon_0$ 下界／$T>T_{\rm break}$ 时 $p_{\rm lock}$ 写法」。第 186 轮把口径链首环（$t$ 的方向与下界）落 Lean（Spec v13、`Ring15LockT`、十三模块 A 闸 PASS），同时撞出并撤销前卡 (15M.5) 的同步区上界（$y(T_{\rm sync})=0.1847\gg y_{\rm crit}$），新增缺口 **G-186** 与"$t$ 在同步区无上界"；第 187 轮把口径链第二环（$t\to x_\ast$ 接口）落 Lean（Spec v14、`Ring15LockThr`、十四模块 A 闸 PASS），并给出 $y$ 的结构化天花板 $y_{\deg}=1-p_c^{1/m}$（$0.407254$／$0.230100$）；第 188 轮把第三环（$\epsilon_\nu\to r$）落 Lean（Spec v15、`Ring15LockR`、十五模块 A 闸 PASS），钉明 $r$ 的反比结构与 $s>0\iff a\lambda>r$，同时**判"$r(T)$ 整体单调上移"为假**（$m{=}1$ 在 $T=0.30575$ 有 $4.03\times10^{-4}$ 凹陷）并新增 **G-188**；第 189 轮把 $\Phi$ 的授权域判清（Spec v16、`Ring15LockPhi`、十六模块 A 闸 PASS）：判据 $\beta_{\rm KT}<\pi/2\iff y_{\rm crit}<y_R$ 使"$\Phi$ 进逸度＋BKT 钉住"必然违反 (15L.5)，据此**撤销 185 (ii) 的 $\Phi$ 窗口**（$y(T_c)$ 由窗口塌成点 $1.8862\times10^{-3}$、$T_{\rm sync}$ 收成点 $0.50665/0.47071$），并钉明 (15L.3) 的 $\Upsilon$ 是 bare、(19W.8) 的 $\Upsilon$ 是 effective（同名不同义）；新增 **G-189**；第 190 轮把 $w(T)$ 钉进 Spec（Spec v17、`Ring15LockW`、十七模块 A 闸 PASS）：$w=2\int_0^1 u\tanh(u/2T)du$ 的正性、单调不增、上界 1 三条定义式定理进链，186／187／188 三处对 $w$ 的消费从数值升为已证；新增 **G-190**（G-190a $w(0)=1$ 只作极限陈述、G-190b 严格单调未证、G-190c $|w'|$ 的导数表示未进 Lean）；第 191 轮把 $s$ 的同名判否（Spec v18、`Ring15LockS`、十八模块 A 闸 PASS）：$s_{\rm sol}=2/[C(a\lambda-r)]$ 是连续、可正可负的可解性因子（正向取遍 $(0,\infty)$，`TargetPropSolSurj`），$s_{\rm rep}\in\frac12\mathbb Z$ 是表示权，二者不同对象；据此 $s_{\rm sol}$ 归乙类、$s_{\rm rep}$ 的选档迁至环 26／`临-26`；第 192 轮把 $w$ 的"不增"升级为"严格减"（Spec v19、`Ring15LockWStr`、十九模块 A 闸 PASS）：`TargetPropWGapStrictAnti` 由 `integral_mono_on`＋`integral_pos`＋`integral_sub` 证出，G-190b 收口，186 的 $t$ 方向可用上严格性（G-186 转为"待复合"）；第 193 轮把这条严格性沿链传下去（Spec v20、`Ring15LockTStrict`、二十模块 A 闸 PASS）：`TargetPropKStrictAnti`（$K=\Upsilon_0w/T$ 严格减）、`TargetPropYStrictMono`（$y$ 作为 $T$ 的函数严格增）、`TargetPropTStrictMono`（$p$ 固定时 $t$ 严格增），G-186 的 **$w\to K\to y\to t$ 通道收口**，仅剩 $p_{\rm pair}(T)$ 通道单列 **G-186p**；第 194 轮把 $p_{\rm pair}$ 通道的**方向**判清并形式化（Spec v21、`Ring15LockTChan`、二十一模块 A 闸 PASS）：`TargetPropTEffMPMono`（$t$ 对 $p$ 严格增）＋`TargetPropTChanSplit`（$\Delta t$ 的 $y$ 项 $>0$、$p$ 项 $<0$ 的反号分解），据此**纠正** 193 的"等 $F_\nu$ 授权即可复合"——两通道反号，$t$ 的净方向须主导项比较，单列 **G-186c**（甲类），G-186p 的残余部分（$\chi^2$ 尾函数链内定义授权）归乙类；第 195 轮把 G-186c 写成**条件式**（Spec v22、`Ring15LockTDom`、二十二模块 A 闸 PASS）：`TargetPropTChanDominate`（$\delta_1+\delta_2>0\Rightarrow t$ 增，充分）与 `TargetPropTChanCriterion`（$\Delta t>0\iff\delta_1+\delta_2>0$，充要），把复合方向缩成一条标量不等式的符号；第 196 轮把 $w'$ 本身写进链（Spec v23、`Ring15LockWD`、二十三模块 A 闸 PASS）：`wGapDeriv T=-(1/T^2)\int_0^1u^2\mathrm{sech}^2\frac{u}{2T}du` 由参数积分求导引理逐点证出（`TargetPropWGapDeriv`），符号另立（`TargetPropWGapDerivNeg`，$|w'|=-w'$），**G-190c 收口**，188 的形状项 $w/|w'|$ 不再卡在数值层；第 197 轮把 $w$ 的分部积分恒等式写进链（Spec v24、`Ring15LockIbp`、二十四模块 A 闸 PASS）：$w=\tanh\frac{1}{2T}+\frac T2w'$ 及其三条推论（形状项＝端点商−半温、端点亏损＝$\frac T2|w'|$、端点严格高于平均），**G-188a 收口**，同时把 G-188 拆出 **G-188b**（$w''$ 与形状项极小编址）；第 198 轮把 **$w''$ 与形状项导数写进链**（Spec v25、`Ring15LockWD2`、二十五模块 A 闸 PASS）：$w''=-\frac{2}{T}w'-\frac{1}{T^4}\int_0^1u^3\mathrm{sech}^2\frac{u}{2T}\tanh\frac{u}{2T}du$ 与 $S'=\frac{w\,w''-(w')^2}{(w')^2}$ 均成定义式定理（`TargetPropWGapDeriv2`／`TargetPropShapeDeriv`），**只完成 G-188b 第一步**——$w''>0$ 与 $S'$ 的分段符号仍**未证**；第 199 轮把 $w''$ 换成**端点闭式** $w''=w'/T+\mathrm{sech}^2\frac{1}{2T}/T^3$（Spec v26、`Ring15LockWD3`、二十六模块 A 闸 PASS）：$u^3$ 积分被消掉，正性给出精确判据 $T^2|w'|<\mathrm{sech}^2\frac{1}{2T}$，$S'$ 的符号给出代数等价式 $S'<0\iff w\,w''<(w')^2$；同时**否证无条件凸性**（判据比仅在 $T\gtrsim0.256$ 小于 1，小 $T$ 处 $w''<0$），故 $w''>0$ 只能作条件式；第 200 轮把 199 的判据换元成**两个无量纲比值的比较**（Spec v27、`Ring15LockWD4`、二十七模块 A 闸 PASS）：$S'<0\iff\Phi(1+r)<2r$（$\Phi=w/\tanh\frac{1}{2T}$、$r=T^2|w'|/\mathrm{sech}^2\frac{1}{2T}$），并给出无条件段 $1\le r\Rightarrow S'<0$（即 $w''\le0$ 段形状项必降）；但 $r<1$ 段（$T\in[0.256,0.3438]$）与 $T>0.3438$ 的 $S'>0$ 仍只有判据、无定理；第 201 轮把 200 的二元判据**消成一元**（Spec v28、`Ring15LockUnary`、二十八模块 A 闸 PASS）：由端点亏损 $T|w'|=2h(1-\Phi)$ 与勾股恒等式 $\mathrm{sech}^2\frac{1}{2T}=1-h^2$ 得 $r$ 的闭式 $r=2Th(1-\Phi)/(1-h^2)$，代回 $\Phi(1+r)<2r$ 后 $r$ 被**整块消掉**，得 $S'<0\iff 0<G$（$G=2Th(1-\Phi)(2-\Phi)-\Phi(1-h^2)$）；据此**撤销"$r$ 的上下夹逼是必要入口"**，余下要证的是 $G$ 的符号，而它依赖 $\Phi$ 的单调性（现只有两端渐近 $\Phi\to1$／$\Phi\to2/3$，均未进 Lean）；第 202 轮把「$G$ 的符号」换成一对**可读标量**的比较（Spec v29、`Ring15LockDeficit`、二十九模块 A 闸 PASS）：$r$ 有**双侧夹逼** $1/3\le r\le1/(3\mathrm{sech}^2\frac{1}{2T})$（端点核单点界，两条定理）、端点尺度 $\lambda:=\mathrm{sech}^2\frac{1}{2T}/(2T\tanh\frac{1}{2T})=1/(T\sinh\frac1T)$ 有初等闭式、判据整块除以 $2Th(1-\Phi)$ 后成 $S'<0\iff\lambda(T)<\delta(1+\delta)/(1-\delta)$（$\delta:=1-\Phi$）；同时**否证「$\Phi$ 的单调性可判 $G$」**（$\Phi'<0$ 对应阈值 $2\delta/(1-\delta)$ 严格宽于判据阈值 $\delta(1+\delta)/(1-\delta)$），201 的「最该修＝$\Phi$ 单调性」改判为「判 $\delta$ 与 $\lambda$」；第 203 轮把判据两侧**各自单调化**（Spec v30、`Ring15LockLambda`、三十模块 A 闸 PASS）：$R(\delta)=\delta(1+\delta)/(1-\delta)$ 在 $(0,1)$ 严格单增（纯代数，差 $=\frac{(b-a)(1+a+b-ab)}{(1-a)(1-b)}$，不读 $\Phi'$）、$\lambda(T)=1/(T\sinh\frac1T)$ 在 $T>0$ 严格单增（$F(s)=s/\sinh s$ 严格减 $F'<0\iff\tanh s<s$ 由 $\tanh s=\int_0^s\mathrm{sech}^2$、$s-\tanh s=\int_0^s\tanh^2>0$ 证出，再与 $T\mapsto1/T$ 严格减复合）、且 $0<\lambda<1$（$s<\sinh s$）；三条均为定义式定理、无 sorry、公理白名单。同时判明**两侧同增不足以定交点**：$R(\delta(T))$ 的单增依赖 $\delta(T)=1-\Phi(T)$ 单增，而 $\Phi'$ 未进链，交点 $T_{\min}$ 须另立增速比较；第 204 轮把 $\delta$ 侧**从数值抬成定理**（Spec v31、`Ring15LockDeficitMono`、三十一模块 A 闸 PASS）：$\delta'$ 有闭式 $-\left(w'h+w\,\mathrm{sech}^2\frac1{2T}/(2T^2)\right)/h^2$（商法则＋$\tanh\frac1{2T}$ 的链式求导）、$\delta'>0$ 处处成立（等价核不等式 $\mathrm{sech}^2\frac1{2T}w<2T^2h\lvert w'\rvert$，逐点比较化为 $\sinh(2us)\le u\sinh(2s)$，由比值 $F(s)=\sinh s/s$ 严格增给出，$u=1$ 处恰取等）、$\delta$ 在 $(0,\infty)$ 严格单增、$R(\delta(T))$ 随 $T$ 严格单增；**长期阻塞的"$\Phi'$ 未进 Lean"就此消解**（$\Phi'=-\delta'$，不需独立模块），但交点编址仍在 `G-188b-2i`（两侧同增只保证"若相交则唯一"，定号须比 $\delta'$ 与 $\lambda'$）；`审-6` 仍「未闭合」，闭合数 0、唯一编号 37。- 环 15（第 205 轮新残余）：**G-188b-2k**——判据差 $D=R(\delta)-\lambda$ 的**导数闭式已进链**（v32：`lambdaDeriv`／`ratioFunDeriv`／`criterionGapDeriv`，三条定理 A 闸 PASS），但 $D'$ 的**符号结构未证**（$D$ 单峰 $\iff$ $D'$ 恰一零点；206 轮已否证更强的「$D'$ 严格单减」：$D'$ 为 U 形、$D''$ 在 $(0.03,1.5)$ 内变号两次）；207 轮纸面证得 $T\ge1\Rightarrow D<0$（$\delta<\frac13$／$R<\frac23$／$\lambda>\frac23$ 三界），零点域收窄至 $(0,1)$，但**未形式化**（Spec v32 不变），故仍按未闭记；208 轮已把其中 **$\lambda$ 一侧进链**（v33：`TargetPropSinhOneLt`／`TargetPropLambdaOne`／`TargetPropLambdaTailGt`，A 闸三十三模块 PASS）；209 轮把 **$R$ 一侧的代数上界与条件合成进链**（v34：`TargetPropRatioLeOfLeThird`（$0<x\le\frac13\Rightarrow R(x)\le\frac23$，纯代数）、`TargetPropGapNegOfDeficitLeThird`（$\delta\le\frac13$ 且 $T\ge1\Rightarrow D<0$，条件形态）；`Ring15LockTailRatio` 三定理）；210 轮把 **$\delta\le\frac13$ 与尾段的无条件版进链**（v35：`TargetPropTanhSecant`（$\tanh(au)\ge u\tanh a$，由 $g(u)=\tanh(au)/u$ 严格减、$g'$ 分子符号 $\iff2y<\sinh2y$）、`TargetPropDeficitLeThird`（积分比较 $w\ge\frac23h$）、`TargetPropGapNegTail`（$T\ge1\Rightarrow D<0$）），故 **$\{D=0\}\subseteq(0,1)$ 现在成立**；211 轮把 **近零端 $D>0$ 进链**（v36：`TargetPropDeficitGeSq`（$0<T\le\frac1{10}\Rightarrow\frac8{15}T^2\le\delta$，由 $|w'|=\frac1{T^2}\int_0^1u^2\mathrm{sech}^2\frac{u}{2T}du$、$\mathrm{sech}^2z\ge1-z^2$ 于 $z\le1$ 与 $\int_0^{2T}u^2(1-\frac{u^2}{4T^2})du=\frac{16}{15}T^3$）、`TargetPropLambdaLeSq`（$\lambda\le\frac{T^2}{3}$，由 $\sinh s\ge3s^3$ 于 $s\ge10$）、`TargetPropGapPosNearZero`（$D\ge\frac{T^2}{5}>0$，另用 $R(\delta)-\delta=\frac{2\delta^2}{1-\delta}\ge0$）；`Ring15LockNearZero` 3 定理＋6 私有引理），故零点集进一步收窄为 $\{D=0\}\subseteq[\frac1{10},1]$；212 轮把**零点存在性进链**（v37：`TargetPropGapZeroExists`（$\exists T,\ \frac1{10}<T<1\wedge D(T)=0$），由 205 的 `TargetPropCriterionGapDeriv` 逐点给 `ContinuousAt.continuousWithinAt`、211 于 $T=\frac1{10}$ 的正性与 210 于 $T=1$ 的负性、`intermediate_value_Icc'` 取介值，再以两端严格异号排除端点；`Ring15LockZeroExists` 1 定理），故 $\varnothing\neq\{D=0\}\subseteq(\frac1{10},1)$；仍缺**零点唯一（"至多一个"）**；213 轮把唯一性压成**条件句**（v38：`ratioOverLambda`＝$\lambda/R(\delta)$、`TargetPropGapZeroUniqueOfRatioMono`＝「$Q$ 在 $[\frac1{10},1]$ 严格单增 ⇒ $D$ 恰一零点」；`Ring15LockZeroUnique` 1 定理，A 闸三十八模块 PASS），并**否证**212 停点写的"$D'$ 左正右负分段"入口（$D'$ 先增后减、极大 $0.668$ 于 $0.110$、极小 $-0.7319$ 于 $0.353$、零点 $0.194$，而 $D$ 零点在 $0.3439$）；新增显式缺口 **G-188b-2k-u**＝$Q$ 严格单增（等价 $\lambda'R>\lambda R'\delta'$，数值余量最小 $0.0985$ 于 $T=1$），前件未证故唯一性仍未闭；$T_{\min}$ 的"交点存在"由 212 已升为定理（存在），"恰好一个"仍待 $Q$ 单调；数值上的「单峰＋恰一零点」只作反馈层；214 轮为 G-188b-2k-u 补**符号前件**：$R(\delta)>0$ 与 $Q>0$ 进链（v39：`TargetPropDeficitRatioPos`／`TargetPropRatioOverLambdaPos`；`Ring15LockRatioForm` 2 定理），使 $(Q)'/Q$ 的写法在链内合法（否则 $\ln Q$ 无定义）；同时**放弃**$Q$ 的乘法闭式（DISCARD 214-1：`field_simp` 后 $(2h-w)^{-1}$ 消不去，判证明路径限制而非命题为假）。$Q$ 严格单增仍未证，唯一性仍只到条件句；215 轮把 $Q$ 单调性的**右端**从积分形态降为有理形态：由 197 的分部积分 $w=h+\frac T2w'$ 消去 $|w'|$，得 $\delta'=\frac{2(h-w)}{Th}-\frac{w\,\mathrm{sech}^2}{2T^2h^2}$（v40 `TargetPropDeficitDerivAlt`），并给出 $\delta'<\frac{2\delta}{T}$ 与 $\delta'<\frac{2}{3T}$（`TargetPropDeficitDerivLtTwoDelta`／`LtTwoThird`，`Ring15LockDeficitUb` 3 定理）；但 $\frac{2}{3T}$ 是 $1/T$ 级，与 $(\ln\lambda)'\ge\frac{0.313}{T^2}$ 仍差一个量级，故新增子缺口 **G-188b-2k-u-1**＝$\delta'$ 的 $1/T^2$ 级上界（需 $w$ 的定量下界）。

- 环 19／目标区：`M8`、`临-25`（$g_{\rm ren}$ 动态源）、`审-11`、`链外-B`。

- 环 26：`临-8`、`临-22`、`临-26`（$s$／配对密度归一）。



**缺口三分类（第 191 轮起按此记账；只改记账口径，不改闭合数）**：



| 类 | 含义 | 本目录现有条目 | 算不算缺口 |

|:---|:---|:---|:---|

| **甲：链内可判** | 必须由链内定义／已证结论推出，且能给出判据或 Lean 陈述 | $s_{\rm rep}\in\frac12\mathbb Z$（已迁环 26／`临-26`）、$T>T_{\rm break}$ 时 $p_{\rm lock}$ 的写法、**G-186c**（$t$ 随 $T$ 严格增的复合净方向：充要判据已证（`TargetPropTChanCriterion`／`TargetPropTChanDominate`，195），余"$\rho:=|\delta_2|/\delta_1<1$ 在工作域成立"的域核对）、G-188b（形状项导数／极小编址与 $r$ 非单调：188a 的形状项分解已于 197 收口，**198 只完成第一步——$w''$ 与 $S'$ 的结构进链，$w''>0$ 与 $S'$ 分段符号仍未证；199 给出端点闭式与两条判据，并否证"$w''>0$ 无条件"（仅 $T\gtrsim0.256$ 成立），余 b-2：$S'$ 符号的分段判据与极小 $T_{\min}$ 编址；201 把 b-2 的判据消成一元 $S'<0\iff 0<G(T)$（**G-188b-2f**），余 $G$ 的符号；202 把 $G$ 的符号换成 $\lambda$ 与 $\delta$ 的显式比较（**G-188b-2g**），余 $\lambda(T)$ 单调、$R(\delta)$ 单增与 $T_{\min}$ 编址（**G-188b-2h**）；203 把 $\lambda$ 严格单增、$R(\delta)$ 严格单增、$0<\lambda<1$ 三条落成定理（2h 的 (i)(ii)＋值域闭合），并判明"两侧同增不足以定交点"，余交点编址 **G-188b-2i**）、G-189（判据依赖）、G-190a（$w(0)=1$ 仅作极限） | **算** |

| **乙：材料量／外部边界** | 按协议只能作边界条件，不得由链内导出 | $b\,n_d(T_c)$、$\Upsilon_0$（仅下界）、$\alpha_V$、$C$、$t_\Upsilon$、$\Phi_c$ 的数值、$\kappa$、**G-186p 的 $\chi^2$ 尾函数**（$F_{\chi^2_{n_{\rm cell}}}$ 的链内定义授权，方向已由 194 轮证完） | **不算**（记为边界，不再挂在缺口表） |

| **丙：已撤销／已判定** | 已被明确判否或已收口 | 185 (ii) 的 $\Phi$ 窗口、(161.4) 第二等号、$r(T)$ 单调上移、高温 $r\propto T$、$\Phi$ 进逸度、**G-190c（196 收口）**、**G-188a（197 收口：形状项分解）** | **不算**（留在 DISCARD 作痕） |



> 说明：这张分类是**记账纠正**，不是闭合。乙类条目此前与甲类混列，导致缺口表永远清不了零；把它们移到"边界"，缺口表才反映真实的链内待办。甲类要一条条打掉才算闭合，闭合数仍是 0、唯一编号仍是 37。



## 二、已确认关键成果（按轮次，A/B 分区）



| 轮 | 环 | 成果 | 类别 | Lean / 数值入口 |

|:---|:---|:---|:---|:---|

| 154 | 19 | $\sigma_c$ 由已降级的 $p_c^{1/t}$ 回改为相界反解；$\Upsilon/\Upsilon(0)=G(w)$ 单函数；低温系数 $\frac{\pi^2}{3}(1+B)$ 分离两通道 | A | `PercolationStiffnessShape`（9 条）／`环19_sigma_c相界反解与Phi形状.py` |

| 155 | 19/目标 | 回改裸交点→真实跳变 $\Phi_c=\kappa/g$；$g$ 在 (U.1) 抵消；低温曲率闭合反演 $g_{\rm ren}$ | A | `UemuraCurvatureInversion`（7 条）／`环19_Uemura曲率反演.py` |

| 156 | 15/19 | `审-4` 关联阈值接入相界；座/键近阈等价 $C_{sb}=0.681205$；反演偏差 $\Delta g/g\approx7.7\delta$ | A | `CorrelationSiteBond`（5 条）／`环15_审4关联阈值接入相界.py` |

| 157 | 4/15 | $\rho_{nn}(m)$ 链内归一；载体维数可由偏差符号判别（$m^\*=2.556$） | A | `RhoNormalization`（5 条）／`环04审4_rho归一与载体判别.py` |

| 158 | 19/目标 | $G(y)$ 有限支撑 $y_\*$、严格 $T_c<T_\*$、截断出口 $(T_\*-T)^{t_\Upsilon}$；两 $x_c$ 通路一致 | A | `HighTCutoff`（5 条）／`环19_G高温截断.py` |

| 159 | 15/目标 | $m_{\rm lock}=1$（声称）、$T_c\le T_{\rm sync}<T_\*$、$E_c=\pi^2U(0)/(2\Phi_0)$、$\gamma$ 反演 | A（主定理未形式化，见下） | `LockIntegerAndCore`（5 条）／`环15锁定整数与Ec反演.py` |

| 160 | 目标/数据 | 预注册 R12：$T^*$ 上界与同位素端点盲测，P1(A)/P2-P3(B) 通过 | A+B | `R12BlindTest`（5 条）／`R12_T星上界与同位素端点盲测.py` |

| 161 | 15 | 和乐高斯尾→锁相因子（**只匹配指数**）；$\sigma_\theta^2=k_BT/\Upsilon_0$；推 6 定量终结 | A+B | `HolonomyLockMap`（5 条）／`环15和乐动力学映射与推6终结.py` |

| 162 | 15/`审-6` | $m_{\rm lock}$ 定义授权修订（v1 定义式冒充命题 → v2 键级基数）；`TargetProp`＝充要刻画；A 闸逐条实测通过 | A（限键级计数口径） | `Ring15Spec`+`Ring15LockMult`（3 条）／`audit_log_环15_2026-11-25.txt` |

| 163 | 15/`审-6` | 锁定概率的键级复合 $p_{\rm lock}=(1-y)^m$；$m=1$ 给 $1-y$、$m=2$ 给 $(1-y)^2$；$t$ 关于 $m$ 严格单调；两分支数值核对与两界复核 | A（限独立键系综） | `Ring15LockProbability`（5 条）／`环15锁定概率复合_两分支核对.py` |

| 170 | 15/`审-6` | **独立键前提的授权层判定**：座独立 $\ne$ 键独立（跨层外推）；由 SB.3 协方差算得共点相关 $\rho=p/(1+p)=0.372154$、$p^3/p^4=1.687063$；授权应钉**条件层**（无条件层因子 $p^2=0.351$ 与登记 $p_{\rm sync}=0.8754138$ 不相容）；缺口未闭合，但形态由"含糊继承"变为"条件＋偏差量" | B（定义授权修订，未闭合） | `03_推导工作台/环15_审6_独立键前提的授权层与偏差.md` |

| 173 | 15/`审-6` | **授权层形式化落盘**：`Ring15Spec` v3 增 `pLockCond`／`pLockUncond`／`TargetPropLayer`；`Ring15LockLayer` 证 `targetPropLayer`（$0\le q,y\le1$ 时无条件层 ≤ 条件层、$q=1$ 时相等）与 `cond_eq_pLock`（定义同值 ⇒ 旧数值不变）；A 闸 `[propext, Classical.choice, Quot.sound]`，类型逐项对齐 | A（限授权层不等式） | `Ring15LockLayer.lean`／`olean_tmp`／`audit_log_环15_2026-11-25.txt` §六 |

| 174 | 流程 | **A 闸固化（环 15 级）**：`a_gate.ps1` 一键重放"出 olean → 仅 import Spec → axioms 白名单 → 类型强制标注 → token 卫生"，首次运行 PASS（四模块、7 条 axioms、3 条类型、233 文件 0 命中），非零退出码可挂提交前钩子；覆盖仅环 15 四模块 | 闸（流程，非物理） | `05_Lean验证/a_gate.ps1`；`audit_log` §七 |

| 175 | 15/`审-6` | **方向性定理**：`targetPropFugMono`（$T>0$、$E_{c1}\le E_{c2}\Rightarrow y(E_{c2})\le y(E_{c1})$）与 `targetPropSyncMono`（$0\le y_1\le y_2\le1\Rightarrow p_{\rm sync}(y_2)\le p_{\rm sync}(y_1)$），A 闸通过；**组合定理故意不写**（需 $y\le1$ 而该值域源自外部 $2\pi$）；给出线性化展宽 $\sigma_{T_{\rm sync}}/T_{\rm sync}\approx0.1725\,\sigma_\Upsilon/\Upsilon$（系数来自第 168 轮解析有限差分） | A（限单调方向）＋B（展宽估计） | `Ring15LockMono.lean`／`a_gate.ps1`（五模块）／`03_推导工作台/环15_审6_方向性定理与涨落展宽.md` |

| 179 | 15/`审-6` | **ρ 的载体核审计（自我纠偏）**：谱指数正确记账 $m_{\rm eff}=2n+(d-1)-s$（第 85 轮的 $2n+1-s$ 只是 $d=2$ 特例，与其"3D Regge 载体"自相矛盾）；$\rho_{nn}$ 的 $J_0$ 是 **2D 核**，3D 载体应配 $j_0=\sin z/z$。四支并列：$\rho_1=+0.0489/-0.0311/+0.3040/+0.2410$，$\rho_{XY}=-0.4249/-0.4778/-0.2271/-0.2745$，$T_{\rm sync}(m{=}2)=0.6107/0.6111/0.6096/0.6098$。**判定**：量级结论（$C_{\rm lock}-1\le2.5\times10^{-6}$、$T_{\rm sync}$ 跨度 $0.25\%$）对分支不敏感，但"$\rho_1=0.048930$ 是链内定值"是跨层＋跨核的过度确定，判**跑偏（限该句）**并已改口径 | B（定义式审计，判跑偏后改口径）＋A（无新引理，重跑九模块） | `04_计算验证/环15锁定概率_载体核分支.py|.json|.png`／卡 §十二 |

| 178 | 15/`审-6` | **θ_c 与聚集修正式接入**：$\theta_c=\pi$ 就在 (161.2)（"失锁即相位差越过主值支边界"）⇒ $a=\Phi^{-1}(1-y/2)$ 由 $y$ 自定（$T_c$ 处 $3.802960$），上一轮"$\theta_c$ 未取"是漏读；跨层同核由第 139 轮 $\delta\lambda=\kappa_f\delta\varepsilon$ 一阶＋`TargetPropAdjCorrScale`（$\rho_{XY}$ 与公共振幅无关）→ 一层成立；接进 $m=2$：$C_{\rm lock}-1$ 从 $T_c$ 的 $1.55\times10^{-6}$ 到 $T=0.72$ 的 $8.70\times10^{-3}$，$T_{\rm sync}^{(2)}$ 上移 $+0.001486$（$0.6092298\to0.6107161$），$m=1$ 不动 | A（九模块 PASS）＋B（定义式；一阶之外未算） | `Ring15LockScale.lean`／`a_gate.ps1`（九模块）／`04_计算验证/环15锁定概率_相位聚集修正.py`／卡 §十一 |

| 177 | 15/`审-6` | **把 $-1/2$ 落回链内真值**：由 (9.1) $2\kappa^2\sigma_0^2(1-\rho_{ij})$ 的差场形态＋$\delta C=\delta\lambda$（README 第 270 行）判定该 $\rho$ 是**顶点**相关（$\ne$ 第 170 轮占据层 $p/(1+p)$）；链内取值由第 84 轮 Bessel 核与第 85 轮 $m_{\rm eff}=2$ 给出 $\rho_1=0.048930$、$\rho_2(2a)=-0.093848$；重推 $\mathrm{Cov}=v(2\rho_1-1-\rho_2)$ ⇒ $\rho_{XY}=-0.424938$（v5 $-0.5$ → v6 $-0.474276$ → v7 $-0.424938$，两处漏相关逐次补上，各自留档）；工作点 $C_{\rm lock}-1=1.55\times10^{-6}$ ⇒ 数值结论不变、"顶点独立"作为链内前件被否证 | A（限算术核，八模块 PASS）＋B（定义式通过；跑偏风险在"$\rho$ 分层混用"） | `Ring15LockCorrGen.lean`／`Ring15LockCorrNear.lean`／`a_gate.ps1`（八模块）／`04_计算验证/环15共点键相位相关_链内Bessel分支.py`／卡 §十 |

| 176 | 15/`审-6` | **共点键相位相关 $\rho=-1/2$**：顶点相位独立等方差 $\Rightarrow$ 相邻相位差 $\mathrm{Var}=2v$、$\mathrm{Cov}=-v$、$\rho=-1/2$（与 $v$、$\theta_c$、$T$ 全无关的算术恒等式）；`TargetPropAdjCorr`＋`Ring15LockCorr` 证出，A 闸六模块 PASS（10 条 axioms／6 条类型／235 文件 0 命中）。**数值否证了自己的推测**：$\rho\ne0$ 使 $|X|,|Y|$ 正关联 ⇒ 都锁与都失锁均聚集（$C_{\rm lock}>1$ 恒成立，非反聚集），MC（$4\times10^6$）复核一致；工作点 $y=1.43\times10^{-4}\Rightarrow a=3.803\Rightarrow C_{\rm lock}-1=2.93\times10^{-6}$ ⇒ 独立假设在工作域数值可忽略但**未证**；$a\sim1$ 时偏差达 $7\%$／$32\%$ | A（限算术恒等式）＋B（定义式通过，跑偏风险在陈述被误读） | `Ring15LockCorr.lean`／`a_gate.ps1`／`04_计算验证/环15共点键相位相关_双变量高斯修正.py`／`03_推导工作台/环15_审6_共点键相位相关与条件层误差量级.md` |



## 三、每环四元组（最近一轮，环 15／`审-6` 重开段，第 205 轮）



**第 205 轮（判据差的导数结构：G-188b-2j 前件）**



- **本环输入**：204 的 `TargetPropDeficitDeriv`（$\delta'$ 闭式）、202 的 `TargetPropLambdaForm`（$T>0$ 时 $\lambda=1/(T\sinh\frac1T)$）与 `endpointLambda`、203 的 `TargetPropLambdaStrictMono`、204 的 `TargetPropDeficitRatioStrictMonoT`。

- **第一性依据**：商法则（$1/(T\sinh\frac1T)$ 与 $x(1+x)/(1-x)$ 各一次）；$\frac{d}{dT}\sinh\frac1T=-\cosh\frac1T/T^2$（`Real.hasDerivAt_sinh`＋`hasDerivAt_inv`＋链式）；$\delta(T)\ne1$ 由 $w>0$（`TargetPropWGapPos`）与 $h>0$（$\tanh\frac1{2T}>0$，本地自证）给出，不借数值。

- **待建模型/方程**：$\lambda'(T)=\dfrac{\cosh\frac1T/T-\sinh\frac1T}{(T\sinh\frac1T)^2}$；$R'(x)=\dfrac{1+2x-x^2}{(1-x)^2}$；$D(T)=R(\delta(T))-\lambda(T)$，$D'(T)=R'(\delta)\delta'-\lambda'$。

- **本环输出**：Spec v32（`lambdaDeriv`／`ratioFun`／`ratioFunDeriv`／`criterionGap`／`criterionGapDeriv`＋三条 Prop）＋`Ring15LockGapDeriv`（3 条定理、7 条私有引理，156 行）；A 闸三十二模块 PASS（72 axioms／67 `#check`／261 文件 0 命中／exit 0）；数值：$D'$ 闭式对差分 rel $2.0\times10^{-11}\sim1.7\times10^{-9}$、$D'$ 只变号一次于 $T\approx0.19415$、$D$ 极大 $7.5013\times10^{-2}$、零点唯一 $T_{\min}=0.343857872$。

- **下一环消费哪部分**：只消费 $D'$ 的**闭式**（用于问 $D'$ 是否严格单减／$D''<0$），**不消费** $D'$ 的具体符号，也不消费 $D$ 的单峰结论（未证）。



**第 204 轮（$\delta$ 的导数闭式与严格单增：G-188b-2i 前件）**



- **本环输入**：v24 的 `TargetPropShapeEnd`（$\frac T2\lvert w'\rvert=\tanh\frac1{2T}-w$）与 `TargetPropShapeEndGt`；v23 的 `TargetPropWGapDeriv`（$w'=-\frac1{T^2}\int_0^1u^2\mathrm{sech}^2\frac{u}{2T}$）；v29／v30 的 `deficitFrac`（$\delta=1-\Phi$）、`deficitRatio`（$R(\delta)$）、`TargetPropDeficitRatioMono`（$R$ 在 $(0,1)$ 严格单增）；v29 的 `endpointLambda`。

- **第一性依据**：链内四条——商法则（$h=\tanh\frac1{2T}$、$h'=-\mathrm{sech}^2\frac1{2T}/(2T^2)$ 自证）；端点亏损把 $\delta$ 写成 $\frac{T\lvert w'\rvert}{2h}$ 的显式形（只作核对）；$\sinh$ 过原点的凸性 ⇒ $\sinh(us)\le u\sinh s$（$0<u\le1$），严格性在 $u<1$、等号在 $u=1$；$\tanh s<s$ 由 $\int_0^s\tanh^2>0$（203 已证）。**本轮无新增外部锚**（沿用 R201 四条只作边界：$arXiv:2409.16930v2$、$arXiv:2410.22704v1$、$cond-mat/0612092v1$、`10.1103/PhysRevLett.39.1201`），不据外部数值改方程形式、不预埋可调项。

- **待建模型/方程**：$\delta'(T)=-\left(w'h+w\,\mathrm{sech}^2\frac1{2T}/(2T^2)\right)/h^2$；核不等式 $\mathrm{sech}^2\frac1{2T}\,w<2T^2h\lvert w'\rvert$；$\delta'>0$；$\delta$ 与 $R(\delta(\cdot))$ 在 $(0,\infty)$ 严格单增。

- **本环输出**：Spec v31（`deficitDeriv`＋四条 Prop）＋`Ring15LockDeficitMono`（4 条定理、21 条私有引理，389 行）；A 闸三十一模块 PASS（69 axioms／64 `#check`／260 文件 0 命中／exit 0）；数值：$\delta'$ 闭式 vs 差分 rel $\le1.2\times10^{-9}$、$\delta'>0$ 301 点 0 违反、核比最大 $0.955319$、点位不等式 0 违反、$T_{\min}=0.343857873$ 不变。

- **下一环消费哪部分**：只消费 $\delta'$ 的**闭式与符号**（与 $\lambda'$ 的显式比较）与 $R(\delta(\cdot))$ 的严格单增（交点唯一性的外侧估计）；**不消费**"$\delta$ 严格单增"这句结论本身，也不消费 $\delta=\frac{T\lvert w'\rvert}{2h}$ 的显式形（那只是核对式）。



**第 203 轮（判据两侧的单调性：G-188b-2h 前件）**



- **本环输入**：v29 的 `TargetPropShapeSignDeficit`（$S'<0\iff\lambda(T)<R(\delta)$）、`deficitRatio`（$R(\delta)=\frac{\delta(1+\delta)}{1-\delta}$）、`TargetPropLambdaForm`（$\lambda=1/(T\sinh\frac1T)$）；v27／v28 的 `shapePhi`／`shapeH`（$\Phi=w/h$、$\delta=1-\Phi$）。

- **第一性依据**：链内三条——$R(\delta)$ 的形状由 202 判据整块除以 $2Th(1-\Phi)$ 后**唯一**剩下的 $\delta$ 依赖决定；$\lambda$ 的显式形式由 $S=2Th\lambda$ 与 $\sinh$ 二倍角给出；$\lambda$ 的值域由 $\sinh s>s$ 决定。本轮为**纯内部代数＋初等不等式**（$\tanh s=\int_0^s\mathrm{sech}^2$、$s-\tanh s=\int_0^s\tanh^2$、$0<s<\sinh s$），不引新量、不引可调前因子、不换核形式。外部锚沿用 R201 四条（E1 `arXiv:2409.16930v2`、E2 `arXiv:2410.22704v1`、E3 `cond-mat/0612092v1`、E4 `10.1103/PhysRevLett.39.1201`），**不新增外部锚**、不据外部数值改方程形式。

- **待建模型/方程**：`deficitRatio T := deficitFrac T*(1+deficitFrac T)/(1-deficitFrac T)`；`TargetPropDeficitRatioMono`（$0<a<b<1\Rightarrow R(a)<R(b)$）；`TargetPropLambdaStrictMono`（$0<T_1<T_2\Rightarrow\lambda(T_1)<\lambda(T_2)$）；`TargetPropLambdaBounds`（$0<T\Rightarrow0<\lambda<1$，新立的值域命题）。

- **本环输出**：三条定义式定理（Spec v30、`Ring15LockLambda`）；判据两侧从"两个待判的积分比"变成"两个**各自单调化**的显式量"，$\lambda$ 的单增**不经过 $\Phi$、不经过 $w$**；并判明"两侧同增仍不足以定交点"（交点由增速翻转决定），据此把 $T_{\min}$ 编址单列为 2i。A／B 闸实测见 §五。

- **下一环消费哪部分**：仅消费 $\lambda$ 严格单增、$R$ 严格单增、$0<\lambda<1$ 三条定理与"比较 $\frac{d\lambda}{dT}$ 与 $\frac{dR}{dT}$ 才能定交点"这一表述；不消费 $r$、$G$ 的数值，不消费 $w$、$|w'|$ 的具体积分值。



**第 202 轮（判据的 δ／λ 形式与判据比的双侧夹逼：G-188b-2g）**



- **本环输入**：v28 的 `TargetPropShapeSignUnary`／`shapeG`（$S'<0\iff 0<G$）；v27 的 `shapePhi`／`ratioR`；v23 的 `wGapDeriv`（$|w'|=\frac1{T^2}\int_0^1u^2\mathrm{sech}^2\frac{u}{2T}du$）与 `TargetPropWGapDerivNeg`；v24 的 `TargetPropShapeEndGt`（$\Phi<1$）。

- **第一性依据**：链内三条——窗口 $[0,1]$ 与核 $2u\tanh\frac{u}{2T}$ 是 $w$ 的定义本身；$w'$ 由 196 从该定义推出；端点亏损由 197 推出。本轮只用**初等不等式**（$\cosh$ 单增、$\mathrm{sech}^2\le1$、$\int_0^1u^2=\frac13$）与**恒等变形**（$S=2Th\lambda$、$\sinh$ 二倍角），不引新量、不引可调前因子、不换核形式。外部锚沿用 R201 四条（E1 `arXiv:2409.16930v2`、E2 `arXiv:2410.22704v1`、E3 `cond-mat/0612092v1`、E4 `10.1103/PhysRevLett.39.1201`），只作"刚度二阶量可分段变号、端点值有物理对应物"的边界；本轮为纯内部代数，不新增外部锚。

- **待建模型/方程**：`deficitFrac T := 1 - shapePhi T`；`endpointLambda T := sechSq(1/(2*T))/(2*T*shapeH T)`；`TargetPropRatioBracketLow`（$\frac13\le r$）；`TargetPropRatioBracketHigh`（$r\le1/(3S)$）；`TargetPropLambdaForm`（$\lambda=1/(T\sinh\frac1T)$）；`TargetPropShapeSignDeficit`（$S'<0\iff\lambda<\frac{\delta(1+\delta)}{1-\delta}$）。

- **本环输出**：四条定义式定理（Spec v29、`Ring15LockDeficit`）；$r$ 的夹逼不再依赖 $\Phi$，判据的比较对象换成 $\lambda(T)$（纯 $T$ 显式函数）与 $R(\delta)$（只读 $\delta$ 的显式阈值）；同时给出否决性代数结论（$\Phi$ 单调性严格弱于判据）。A／B 闸实测见 §五。

- **下一环消费哪部分**：仅消费 $\lambda(T)=1/(T\sinh\frac1T)$ 的单调性需求、$R(\delta)$ 在 $(0,1)$ 上的单调性需求与"两者相等点即 $T_{\min}$"这一表述；不消费 $r$、$G$ 的数值，不消费 $w$ 的具体积分值。



**第 201 轮（$r$ 的 $\Phi$ 闭式与判据一元化：G-188b-2f）**



- **本环输入**：v24 的 `TargetPropShapeEnd`（$\frac T2|w'|=\tanh\frac{1}{2T}-w$）与 `TargetPropShapeEndGt`（$w<\tanh\frac{1}{2T}$）；v27 的 `shapePhi`／`ratioR`／`TargetPropShapeSignRatio`（$S'<0\iff\Phi(1+r)<2r$）；v23 的 `TargetPropWGapDerivNeg`（$|w'|=-w'$）。

- **第一性依据**：链内换元——端点亏损把 $T|w'|$ 折算成 $2h(1-\Phi)$，勾股恒等式 $\cosh^2-\sinh^2=1$ 把 $\mathrm{sech}^2\frac{1}{2T}$ 折算成 $1-h^2$，二者相除即 $r$ 的闭式；故 $r$ **不是独立自由度**，200 的二元判据可整块消成一元。不引新假设、不引可调前项。外部锚只作边界：E1 `arXiv:2409.16930v2`（BKT 相界上 bare 刚度有局部极小）、E2 `arXiv:2410.22704v1`（NbN 多孔膜 $J_s$ 近线性降）说明二阶量分段变号是常态；E3 `cond-mat/0612092v1`、E4 `10.1103/PhysRevLett.39.1201`（Nelson–Kosterlitz 1977）说明端点值有物理对应物；四条**不给**方程形式。

- **待建模型/方程**：`shapeH T := tanh(1/(2*T))`；`TargetPropRatioPhiForm`（$r=\dfrac{2Th(1-\Phi)}{1-h^2}$）；`shapeG T := 2Th(1-\Phi)(2-\Phi)-\Phi(1-h^2)`；`TargetPropShapeSignUnary`（$S'<0\iff 0<G$）。

- **本环输出**：两条定义式定理＋两个新定义（Spec v28、`Ring15LockUnary`）；$r$ 从"两个积分之比"降为 $\Phi$ 与 $h$ 的显函数，$S'$ 的符号只剩一个一元不等式。A／B 闸实测结果见 §五。

- **下一环消费哪部分**：202 只消费 $0<G(T)$ 这一条判据与 $\Phi<1$、$h\in(0,1)$；不消费 $r$，也不消费 $w$、$|w'|$ 的数值。要证 $G$ 的符号，缺的新前件是 $\Phi$ 的单调性（现仅 $T\to0$ 的 $\Phi\to1$、$T\to\infty$ 的 $\Phi\to2/3$，均只在链外以渐近形式给出）。



**第 200 轮（形状比与判据比：G-188b-2 第二步）**



- **本环输入**：v26 的 `wGapDeriv2Alt`（$w''=w'/T+\mathrm{sech}^2\frac{1}{2T}/T^3$）与 `TargetPropShapeDerivSign`；v24 的 `TargetPropWGapIbp`、`TargetPropShapeEnd`、`TargetPropShapeEndGt`；v23 的 `TargetPropWGapDerivNeg`。

- **第一性依据**：链内换元——199 的"乘积比较"用 197 的端点亏损折算后，整块符号只由 $\Phi:=w/\tanh\frac{1}{2T}$ 与 $r:=T^2|w'|/\mathrm{sech}^2\frac{1}{2T}$ 的比较决定；不引新假设、不引可调前因子。外部锚只作边界（刚度二阶系数可过零变号、$d\rho_s/dT$ 近线性 ⇒ 符号分段是常态）。

- **待建模型/方程**：`shapePhi`／`ratioR`；`TargetPropShapeSignRatio`（$S'<0\iff\Phi(1+r)<2r$）；`TargetPropShapeNegOfRatioGeOne`（$1\le r\Rightarrow S'<0$）。

- **本环输出**：链内恒等式 $w\,w''-(w')^2=\tanh\frac{1}{2T}\mathrm{sech}^2\frac{1}{2T}[\Phi(1+r)-2r]/T^3$ ＋两条定理（Spec v27、`Ring15LockWD4`、二十七模块 A 闸 PASS）。

- **下一环消费哪部分**：201 只消费差量 $\Phi(1+r)-2r$ 的符号与 $\Phi<1$；不消费 $w''$ 的积分式，也不消费 $r$、$w$ 的具体数值。



**第 199 轮（$w''$ 的端点闭式与条件式符号判据：G-188b-2）**



- **本环输入**：v25 的 `wGapDeriv2`（$w''=-\frac{2}{T}w'-\frac{1}{T^4}\int u^3\mathrm{sech}^2\tanh$）与 `shapeDeriv`；v24 的 `TargetPropWGapIbp`（$w=\tanh\frac{1}{2T}+\frac T2w'$）；v23 的 `TargetPropWGapDeriv`／`TargetPropWGapDerivNeg`。

- **第一性依据**：链内依据只有一条——197 的恒等式是"平均—端点—导数"的闭合关系，对它逐项对 $T$ 求导即给 $w''$ 的第二闭式（$\tanh\frac{1}{2T}$ 的导数由 $\tanh'=\mathrm{sech}^2$ 与内层 $-\frac{1}{2T^2}$ 复合）。外部锚只作边界：刚度＝对相位扭曲的二阶导（`arXiv:2409.16930` 的 $J_{\mu\nu}=\partial^2f/\partial Q_\mu\partial Q_\nu$，其 Fig.1 显示 $J_{22}(Q_2)$ 可过零变号）、`arXiv:2410.22704` 与 twisted-trilayer 的 $d\rho_s/dT\approx0.2$–$0.3$ 近线性 ⇒ 曲率在温度上会变号，**恒正不是外部已立事实**。

- **待建模型/方程**：`wGapDeriv2Alt T = wGapDeriv T / T + sechSq(1/(2T))/T^3`；`TargetPropWGapDeriv2Alt`（两式同值）、`TargetPropWGapDeriv2Pos`（$T^2|w'|<\mathrm{sech}^2\frac{1}{2T}\Rightarrow w''>0$）、`TargetPropShapeDerivSign`（$S'<0\iff w\,w''<(w')^2$）。

- **本环输出**：三条定义式定理（Spec v26、`Ring15LockWD3`、二十六模块 A 闸 PASS，54 条 axioms／49 条 `#check`／256 文件 0 命中）；并**否证无条件凸性**（判据比仅 $T\gtrsim0.256$ 小于 1）。

- **下一环消费哪部分**：200 只消费端点闭式（$w\,w''=\frac{w}{T}w'+w\frac{\mathrm{sech}^2}{T^3}$，两项可分别与 $(w')^2$ 比较）与 `TargetPropShapeDerivSign` 的等价式；不消费积分式的具体值。



**第 198 轮（$w''$ 的链内表示与形状项导数：G-188b 第一步）**



- **本环输入**：197 的 `TargetPropShapeSplit`（$w/|w'|=\tanh\frac{1}{2T}/|w'|-\frac T2$）与 `TargetPropShapeEnd`（$\frac T2|w'|=\tanh\frac{1}{2T}-w$）；196 的 `TargetPropWGapDeriv`／`TargetPropWGapDerivNeg`（$w'=-T^{-2}\int_0^1u^2\mathrm{sech}^2\frac{u}{2T}du$、$w'<0$）；188 的形状项 $w/|w'|$ 与它此前从未进链的**导数**。

- **第一性依据**：链内依据是 $w'$ 由**单一被积核** $u^2\mathrm{sech}^2\frac{u}{2T}$ 生成，二阶导只能由该核对参数求导（核 $\partial_T\mathrm{sech}^2=-2\mathrm{sech}^2\tanh\cdot(-u/2T^2)$）＋商法则端点项 $\frac{d}{dT}(-T^{-2})=\frac{2}{T^3}$ 组成，两项不可省、不可只留其一。外部锚只作边界：刚度＝对相位扭曲的二阶导（`arXiv:2603.24766v1/v2`、`cond-mat/0612092v2`、Nelson–Kosterlitz 1977），不给方程形式。

- **待建模型/方程**：`wGapDeriv2 T := -(2/T)*wGapDeriv T - (1/T^4)*∫_0^1 u^3 sechSq(u/(2T)) tanh(u/(2T)) du`；`shapeDeriv T := (wGap T * wGapDeriv2 T - wGapDeriv T^2)/wGapDeriv T^2`；`TargetPropWGapDeriv2`（$\forall T>0$, `HasDerivAt wGapDeriv (wGapDeriv2 T) T`）、`TargetPropShapeDeriv`（$\forall T>0$, `HasDerivAt (fun T => wGap T/|wGapDeriv T|) (shapeDeriv T) T`）。

- **本环输出**：两条定义式定理（Spec v25、`Ring15LockWD2`、二十五模块 A 闸 PASS，51 条 axioms／46 条 `#check`／257 文件 0 命中）；G-188b **第一步**完成。

- **下一环消费哪部分**：G-188b 第二步只消费 $w''$ 的**两项结构**与 $S'$ 的**分子代数形** $w\,w''-(w')^2$，用来比较 $\frac{2}{T}|w'|^2$ 与 $\frac{|w'|}{T^4}\int u^3\mathrm{sech}^2\tanh$ 的大小（即 $w''>0$ 与 $S'$ 分段符号）；不消费本轮任何积分值。186／187 不消费本轮。



**第 197 轮（$w$ 的分部积分恒等式与形状项分解：G-188a 收口）**



- **本环输入**：190 的 `wGap`（$w=2\int_0^1u\tanh\frac{u}{2T}du$）、196 的 `TargetPropWGapDeriv`／`TargetPropWGapDerivNeg`；188 的形状项 $w/|w'|$（此前无链内分解）。

- **第一性依据**：核原函数 $\frac{u^2}{2}\tanh\frac{u}{2T}$ 由核本身给出，FTC 为分析学既有结论，不引新量、不引前因子。外部锚只作边界：二维超流刚度随 $T$ 降、BKT 处刚度跳变（Nelson–Kosterlitz 1977；`arXiv:2207.13748` §3.3），不给方程形式。

- **待建模型/方程**：`TargetPropWGapIbp`（$w=\tanh\frac{1}{2T}+\frac T2w'$）、`TargetPropShapeSplit`（$w/|w'|=\tanh\frac{1}{2T}/|w'|-\frac T2$）、`TargetPropShapeEnd`（$\frac T2|w'|=\tanh\frac{1}{2T}-w$）、`TargetPropShapeEndGt`（$w<\tanh\frac{1}{2T}$）。

- **本环输出**：四条定义式定理（Spec v24、`Ring15LockIbp`、二十四模块 A 闸 PASS）；**G-188a 收口**。

- **下一环消费哪部分**：188 的第二半（**G-188b**）消费 `TargetPropShapeSplit` 的代数形与 `TargetPropShapeEndGt` 的正性，并须先建 $w''$ 的链内表示；186／187 不消费本轮。



**第 196 轮（$w$ 的导数表示：G-190c 收口）**



- **本环输入**：190 的 `wGap`（正性／不增／上界 1）、192 的 `TargetPropWGapStrictAnti`（严格减）、188 的形状项 $w/|w'|$（其 $|w'|$ 从未进链）。

- **第一性依据**：(15L.3)／(19W.8) 的 $w$ 是核在动量窗内的积分、$T$ 只经辐角 $\tanh(u/2T)$ 进入 ⇒ 导数即"对参数求导"，不引新量、不引前因子。外部锚只作边界：$\tanh'=\mathrm{sech}^2$ 为经典恒等式，不给方程形式。

- **待建模型/方程**：`sechSq x := 1/cosh^2 x`、`wGapDeriv T := -(1/T^2)∫_0^1 u^2 sechSq(u/(2T)) du`；`TargetPropWGapDeriv`（$T>0$ 处 `HasDerivAt wGap (wGapDeriv T) T`）、`TargetPropWGapDerivNeg`（`wGapDeriv T < 0`）。

- **本环输出**：两条定义式定理（Spec v23、`Ring15LockWD`、二十三模块 A 闸 PASS）；**G-190c 收口**。

- **下一环消费哪部分**：188 消费**点态恒等**（把 $|w'|$ 化为可积表达式）与**符号**（$|w'|=-w'$）；`wGapDeriv` 的数值大小不被 188 消费（它要的是比值 $w/|w'|$，须另立命题）；186／187 不消费本轮。



**第 195 轮（G-186c 的条件式主导项闸与充要判据）**



- **本环输入**：194 的 `TargetPropTChanSplit`（$\Delta t=\frac{m}{N}(\delta_1+\delta_2)$，$\delta_1>0$、$\delta_2<0$、$N>0$）；`tEffM`；193 的 $y$ 对 $T$ 严格增。

- **第一性依据**：只有 (15L.4) 的 $t$ 定义与 194 的反号结构，不引新量。外部锚只作边界：χ² 尾单调（Goodman，L30）＋`README.md:120` 的低温展开 ⇒ "$\rho$ 的界不能由链内单调性给出"。

- **待建模型/方程**：`TargetPropTChanDominate`（充分）、`TargetPropTChanCriterion`（充要判据 $\Delta t>0\iff\delta_1+\delta_2>0$）。

- **本环输出**：两条定义式定理（Spec v22、`Ring15LockTDom`、二十二模块 A 闸 PASS）；G-186c 判据部分收口。

- **下一环消费哪部分**：186 消费 `TargetPropTChanDominate` 的充分性并逐点核 $\rho<1$；`TargetPropTChanCriterion` 的反向留作反查（观测 $t$ 减 ⇒ 定位 $S<0$）；188 不消费。

**第 194 轮（$p_{\rm pair}$ 通道的方向与两通道反号：G-186p 的形态判定）**



- **本环输入**：193 的 `TargetPropYStrictMono`（$y$ 对 $T$ 严格增）；`tEffM p y m := 1+m\ln(1-y)/\ln p`；$p_{\rm pair}(T)=1-F_{\chi^2_{n_{\rm cell}}}\!\big(n_{\rm cell}\sigma_c^2/(Zw(T))\big)$（`README.md:115`）。

- **第一性依据**：链内只有 (15L.4) 的 $t$ 定义与 $w(T)$ 的积分定义。外部锚只作边界：χ² 分布＝$n_{\rm cell}$ 个独立零均值高斯模的平方和（Goodman 散斑统计，L30），CDF 单调是外部已立的数学事实 ⇒ "$p_{\rm pair}$ 随 $T$ 降"只是 $w$ 严格增（192）＋CDF 单调的复合，不是 CQM 推的方程形式。

- **待建模型/方程**：`TargetPropTEffMPMono`（$t$ 对 $p$ 严格增）、`TargetPropTChanSplit`（$y$ 项／$p$ 项反号分解）。

- **本环输出**：两条定义式定理（Spec v21、`Ring15LockTChan`、二十一模块 A 闸 PASS）；对 193 口径的纠正（"等 $F_\nu$ 即可复合"作废）。

- **下一环消费哪部分**：195 只消费 `TargetPropTChanSplit` 的**符号结构**（$\delta_1>0$、$\delta_2<0$），在其上加显式侧条件 $\delta_1+\delta_2>0$ 立"主导项闸"，把 **G-186c** 从数值口径提为条件式命题；187／188 不消费本轮。



**第 193 轮（$w$ 的严格减沿 $T\to K\to y\to t$ 传下去：G-186 通道严格化）**



- **本环输入**：192 的 `TargetPropWGapStrictAnti`；$y$ 律 $K=\Upsilon_0w(T)/T$、$y=2\pi e^{-\pi^2K/2}$（`fugOfK`，(15L.3)＋(19W.3)）；$t=1+m\ln(1-y)/\ln p$（`tEffM`）；186 已证的 $t$ 对 $y$ 严格增。

- **第一性依据**：只用这三条已登记定义。外部锚为边界：Nelson–Kosterlitz 1977（PRL 39, 1201）给二维超流密度＝螺旋模量在 $T_c^-$ 的普适跳变 $K_R^{-1}\to2/\pi$、涡旋对软化刚度，故"刚度随 $T$ 降"外部已立；$w(T)$ 的具体形状与严格性仍由 CQM 的积分定义给出，文献不给方程形式。

- **待建模型/方程**：`yOfT ups0 T := fugOfK (ups0 * wGap T / T)`；`TargetPropKStrictAnti`、`TargetPropYStrictMono`、`TargetPropTStrictMono`。

- **本环输出**：三条定义式定理（Spec v20、`Ring15LockTStrict`、二十模块 A 闸 PASS）；G-186 的 $w\to K\to y\to t$ 通道收口。

- **下一环消费哪部分**：$p_{\rm pair}(T)$ 通道需要 $F_\nu$（χ² 尾）的定义授权，链内没有 ⇒ 单列 **G-186p**，本轮不消费。〔**194 轮已纠正**：这句话的后半段作废——$p_{\rm pair}$ 随 $T$ 降、$t$ 对 $p$ 增，两通道反号，$t$ 的净方向须主导项比较（G-186c），不是"$F_\nu$ 到位即可复合"。〕



**第 192 轮（$w$ 的严格单调：G-190b 收口）**



- **本环输入**：`wGap T := ∫ u in 0..1, 2*u*tanh(u/(2*T))`（v17 定义）＋`TargetPropWGapAnti`（不增，190 轮已证）＋`tanh_strictMono`（190 轮私有引理：$\tanh'=1/\cosh^2>0$）；186 的 $t$ 方向只需"$w$ 随 $T$ 减"。

- **第一性依据**：$w$ 的积分定义本身。对每个 $u>0$，辐角 $u/(2T)$ 关于 $T$ 严格减、$\tanh$ 严格增 ⇒ 被积函数关于 $T$ 严格减；被积函数连续、差值非负且在 $u=1$ 处为正 ⇒ 积分严格小。不引新假设，不用数值。

- **待建模型/方程**：`TargetPropWGapStrictAnti`：$\forall T_1T_2,\ 0<T_1\to T_1<T_2\to w(T_2)<w(T_1)$。

- **本环输出**：一条定义式定理（Spec v19、`Ring15LockWStr`、十九模块 A 闸 PASS）；G-190b 收口。

- **下一环消费哪部分**：186 只消费"严格"这一层（$y$ 严格减 ⇔ $p_{\rm pair}$ 严格增 ⇒ $t$ 严格增），故 G-186 由"仅数值"降为"待复合"（$y$／$p_{\rm pair}$ 两通道尚未各自进 Lean）；188 的形状项要的是 $w'$ 的积分表示（G-190c），**不消费**本轮。



**第 191 轮（$s$ 的同名判否：可解性因子 vs 表示权）**



- **本环输入**：环 6／G19 的 $s_{\rm rep}\in\frac12\mathbb Z$（$\theta=s\ell$、$\alpha=-4\pi s$；`临-26`：半整权需自旋提升，链内无；A4 整格再收成 $\mathbb Z$）；R155.1 的 $s_{\rm sol}=2g/[C(g\,a\lambda+2\mu)]=2/[C(a\lambda-r)]$；§16.3 用 $s_{\rm rep}$ 把 $\sigma_\varepsilon$ 预算筛到 $\lvert s\rvert=3/2$；188 的失效面 $a_*\lambda=r$ 用 $s_{\rm sol}$。

- **第一性依据**：$s_{\rm rep}$ 由相位单值性＋A4 根电荷整格定，值在离散格；$s_{\rm sol}$ 由 $C,A,K$ 的系数解出（$g=CA/(2s-CK)$），是"标准差可解"的实值条件。值域不同 ⇒ 不是同一对象。

- **待建模型/方程**：`TargetPropSolSurj`（$\forall y>0$，$C=1,r=0,a\lambda=2/y$ 给 $s_{\rm sol}=y$）、`TargetPropSolNeg`（$C=1,a\lambda=0,r=1$ 给 $-2$）。

- **本环输出**：两条定义式定理（Spec v18、`Ring15LockS`、十八模块 A 闸 PASS）＋同名判否；$s_{\rm sol}$ 归乙类，$s_{\rm rep}$ 选档迁环 26。

- **下一环消费哪部分**：环 15 失效面只消费 $s_{\rm sol}>0\iff r<a\lambda$（188 的 `TargetPropSFail`）；$\sigma_\varepsilon$ 桥只消费 $s_{\rm rep}$ 的格点值，两处不得互换。



**第 190 轮（$w(T)$ 的积分定义授权：正性、单调不增、上界 1）**



- **本环输入**：环 19 的 $w(T)=2\int_0^1u\tanh\frac{u}{2T}du$（$w(T_c)=0.758705$）；186 的 $t(T)$ 方向依赖"$w$ 随 $T$ 减"；187 的 $y$ 天花板依赖 $w\le1$；188 的 $r=2\alpha_Vw/(3\epsilon_\nu|w'|)$ 依赖 $0<w$；(19W.1) 的 $T\to0$ 归一 $w\to1$。

- **第一性依据**：$\tanh(u/2T)$ 是 Fermi 占据差 $1-2n_F$ 的核，温度只出现在 $E/k_BT$ 的辐角里；外部约束：BCS-Bogoliubov 隙函数在 $[0,T_c]$ 单调递减已证（arXiv:1006.01160 摘要）——同一结构在 CQM 侧即 $w$ 的不增。

- **待建模型/方程**：`wGap T := ∫ u in 0..1, 2*u*tanh(u/(2*T))`；`TargetPropWGapPos`、`TargetPropWGapAnti`、`TargetPropWGapLeOne`。

- **本环输出**：三条定义式定理（$w>0$、$w$ 不增、$w\le1$）＋四个私有引理（$\tanh$ 连续、导数 $1/\cosh^2$、严格单调，及由其导出的正性/单调传递）。

- **下一环消费哪部分**：186 消费"不增"给 $t$ 方向；188 消费"$0<w$"给 $r$ 的分母；187／(19W.1) 消费"$w\le1$"给归一值 $1$ 的上确界地位；G-190c 留待把 $|w'|$ 的导数表示进链，188 的形状项才可能离开数值层。



**第 189 轮（$\Phi$ 的授权域：逸度窗口塌缩与 15／19 两层同名判定）**



- **本环输入**：185 (ii) 的 $\Phi$ 窗口（$y(T_c)\in[1.8862\times10^{-3},0.02501]$、$\Phi\in[0.68135,1]$、$T_{\rm sync}$ 窗口）；(15L.5) $y_{\rm crit}=2\pi e^{-\pi^2/(2\beta_{\rm KT})}=0.02501$；(154.1)/(154.2) 的 $\Phi(p_*(T_c))=\kappa$ 与 $\kappa=2k_BT_c/(\pi\Upsilon_{\rm bond}w_c)$；(19W.1) $\Upsilon_0=\Upsilon(0)$；(19W.8) $\Upsilon=\Upsilon_0w\Phi$。

- **第一性依据**：二维 XY 的涡旋逸度式 $g=2\pi e^{-\mu/(k_BT)}$ 与核能 $\mu_{XY}\simeq\frac{\pi^2}{2}J$（\texttt{arXiv:0712.0936} §II）——(15L.3) 就是这条式子的搬运，其 $J$ 是**单层 bare 刚度**；BKT 不动点 $K_R=2/\pi$、$\Upsilon_R=2T_{\rm BKT}/\pi$（\texttt{arXiv:2605.10226} 式 (11)(13)、\texttt{arXiv:0909.0479} 式 (10)）。纯代数：两个 $\Phi$ 之比只由两个指数定 ⇒ 判据与 $T_c,\Upsilon_0,w$ 无关。

- **待建模型/方程**：`phiBkt T U0 w := 2T/(π U0 w)`、`phiMin T U0 w yc := (2T/(π²U0w))·ln(2π/yc)`；四条命题 `TargetPropPhiMono`（$\Phi$ 增 ⇒ $y$ 减）、`TargetPropPhiBktVal`（$\Phi=\Phi_{\rm BKT}$ ⇒ $y=2\pi e^{-\pi}$）、`TargetPropPhiMinEq`（$\Phi=\Phi_{\min}$ ⇒ $y=y_{\rm crit}$，恒等而非反解）、`TargetPropPhiConflict`（$\beta<\pi/2$ ⇒ $y(1/\beta)<y(2/\pi)$）。

- **本环输出**：四条定义式定理（A 闸十六模块 PASS）；判据 $\beta_{\rm KT}<\pi/2\iff y_{\rm crit}<y_R$；$\Phi_{\rm BKT}/\Phi_{\min}=2\beta_{\rm KT}/\pi=0.5685$；185 (ii) 窗口撤销（塌成点）。

- **下一环消费哪部分**：下游只消费 $y$ 的**点值**（$\Phi=1$ 读数），不消费窗口；$\Phi$ 的自由度被彻底删掉后，$T_{\rm sync}$ 恢复为点值，环 15 侧不再有待定的 $\Phi$ 参数——残余只剩 $b\,n_d(T_c)$、$s$、$\Upsilon_0$ 下界与 $T>T_{\rm break}$ 的写法。



**第 188 轮（$\epsilon_\nu\to r$ 的 r/s 结构：反比结构与失效面判据）**



- **本环输入**：第 186 轮 v13 的 `tEffM` 与交接表（$\epsilon_8=2.4004$（$T_c$）、$1.5901$（同步点 $m{=}1$）、$1.4102$（$m{=}2$））；第 187 轮 v14 的 `pPairThr` 与 $x_\ast$ 唯一性；环 17 侧已登记（R-155 §二／R-157 §四）的 $r=2\alpha_Vw/(3\epsilon_\nu|w'|)$、$s=2/[C(a\lambda-r)]$、失效面 $a_\ast\lambda=r$。

- **第一性依据**：环 17 的扩大动力学（$g,\mu,A\propto\dot T$ ⇒ $\dot T$ 约掉、$r\ge0$）给 $s$ 的符号判据；环 19 的 $w(T)$ 积分式给 $w'$；$\epsilon_\nu=2x_\ast f_\nu/\bar F_\nu$ 的定义给反比通道。**纯代数事实**：$\epsilon_\nu$ 与 $r$ 共用同一个分母，故"$\epsilon$ 减 ⇒ $r$ 增"不需要新物理假设。文献侧（高压／非谐对 $T_c$ 的影响、MgB$_2$ 与 YB$_6$ 的 $\mathrm{d}\ln T_c/\mathrm{d}P$）**本轮不消费**——那是第 5 层的外部边界约束，理论未闭合前不进链。

- **待建模型/方程**：`rOfW alphaV w w' eps := 2*alphaV*w/(3*eps*|w'|)`、`sOfLock C aLam r := 2/(C*(aLam - r))`；两条结构命题 `TargetPropROfEps`（$\epsilon$ 通道反比）、`TargetPropSFail`（$s>0\iff r<a\lambda$，只要求 $C>0$）。

- **本环输出**：两条定义式定理（A 闸十五模块 PASS）；$r(T)/r(T_c)$ 的三因子分解与数值（反比项 $1.0120/1.528/1.723$，形状项极小 $0.98866$ @$T=0.3445$，合成后 $m{=}1$ 有 $4.03\times10^{-4}$ 凹陷）；$T\to T_{\rm break}$ 端 $1/\epsilon_\nu$ 发散主导。

- **下一环消费哪部分**：下游（$s$ 的符号域、锁定域与 $a\lambda$ 的比较）只消费"$r>0$、$r$ 对 $\epsilon_\nu$ 单调减"＋"$s>0\iff r<a\lambda$"；**不消费** $\alpha_V$、$C$ 的材料值，也**不消费** $r$ 在 $T$ 上的整体单调（21.3(3) 已判其为假）。



**第 187 轮（$t\to x_\ast$ 接口：两条写法等价、$y$ 的结构化天花板）**



- **本环输入**：第 186 轮 v13 的 `tEffM` 与两条定理；(15L.7) $p_{\rm pair}^{\rm thr}=p_c/(1-y)^m$；(15L.4) 的 $t$ 定义；R-158 ⑥ 的 $x_\ast=\bar F_\nu^{-1}(p_c^{1/t})$；§六交接表同时出现 $p_c^{1/t}$ 与阈值写法两种来源。

- **第一性依据**：对数代数（$\ln(ab)=\ln a+\ln b$、$\ln a^n=n\ln a$）；概率语义——阈值必须落在 $[0,1]$，故 $y\le1-p_c^{1/m}$。外部锚：方格座渗流 $p_c=0.59274602(4)$；损伤格点渗流阈 $f_c\approx0.407\approx1-p_c$。

- **待建模型/方程**：`pPairThr p y m := p/(1-y)^m`；两条 $t$ 写法；恒等 $p_c^{1/t}=p_{\rm pair}^{\rm thr}$（两条命题 `TargetPropThrLog`／`TargetPropThrRpow`）。

- **本环输出**：两条定义式定理（A 闸十四模块 PASS）；同步点两写法差 $3.3\times10^{-16}$、$T_c$ 处不同值（$0.597104$ vs $0.593866$）；天花板 $y_{\deg}=0.407254/0.230100$（$T=0.58607/0.52594$），同步点余量 $0.2225/0.1146$。

- **下一环消费哪部分**：只消费 $x_\ast$ 的**唯一性**与域约束 $y<y_{\deg}$；不消费 $\bar F_\nu$ 的形状（外部卡方尾），也不消费 $x_\ast$ 的具体数值（尚未进 Lean）。



**第 186 轮（$t$ 的方向与下界；撤销 $t$ 的同步区上界）**



- **本环输入**：第 185 轮 v12 的 `fugOfK`／`TargetPropFugStiff`／`TargetPropFugBound`／`TargetPropUpsLower`；R-158 ④ 的 $t$ 定义式 $t=1+m\ln(1-y)/\ln p_{\rm pair}$；前卡 (15M.5) 把 $t$ 上界扩到整个同步区的读法；185 轮数值（$y(T_c)=1.8862\times10^{-3}$、$t(T_c)=1.01420/1.02841$、$T_{\rm sync}=0.50665/0.47071$）。

- **第一性依据**：R-44「损失型粗粒化」——锁损失把每键有效联通概率压到 $(1-y)^m$，故配对阈值必须高于渗流阈值 $p_c$，$t>1$；$\ln$ 在 $(0,1)$ 严格增、$\ln(1-y)\le0$（$y\in[0,1)$）；(15L.5) 只给 $T_c$ 端点，不给全程。

- **待建模型/方程**：$t(T)=1+m\dfrac{\ln[1-y(T)]}{\ln p_{\rm pair}(T)}$，$y(T)=2\pi e^{-\pi^2K(T)/2}$、$K(T)=\Upsilon_0w(T)/T$，$p_{\rm pair}(T)=1-\bar F_\nu(4.5\,w(T_c)/w(T))$；两条命题 `TargetPropTEffMMono`（$y$ 通道单调）、`TargetPropTEffMGeOne`（$t\ge1$）。

- **本环输出**：两条定理均定义式通过（A 闸十三模块 PASS）；数值 $t(T)$ 在 $[T_c,T_{\rm break})$ 严格增、$t(T_{\rm sync})=1.64063/1.88466$、$T\to T_{\rm break}$ 发散；$x_\ast$／$\epsilon_\nu$／$r$ 交接表按 $T$ 分点（$\epsilon_8$：$2.4293$→$2.4004$（$T_c$，$m{=}1$）→$1.5901$（同步点，$m{=}1$））。**失配**：(15M.5) 撤销（其前提 $y(T_{\rm sync})=y_{\rm crit}$ 在 185 轮 y 律下不成立）。

- **下一环消费哪部分**：消费 $t$ 的**数值随 $T$ 的形状**（$x_\ast=\bar F_\nu^{-1}(p_c^{1/t})$ 逐点取 $t$），不消费"$t$ 上界"；$\epsilon_\nu$ 的 $T$ 分点表是本轮交给下一环的唯一输入，$r$ 只按 $\propto1/\epsilon_\nu$ 平移。



**第 185 轮（逸度的 $T$ 依赖归刚度；$\sigma_\theta$ 降为恒等）**



- **本环输入**：第 138 轮（R-147）"$N_I$ 扇区 $M_\ell=0$ ⇒ (4.1) 第一项撤销"；口径表 §一第 138 轮条（现行 (4.1″) 只剩 $\sigma_\varepsilon^2=b\,n_d$）；第 161 轮 (161.1)–(161.5) 原文；第 149 轮（15L.3）$y=2\pi e^{-E_c/(k_BT)}$、$E_c=\frac{\pi^2}{2}\Upsilon$ 与 (15L.5) $y(T_c)\le2\pi e^{-\pi^2/(2\beta_{\rm KT})}$；环 19 (19W.3)/(19W.8) $\Upsilon=\Upsilon_0w(T)\Phi(T)$、$0\le\Phi\le1$、$w$ 的积分式；第 163 轮常量与 $p_{\rm pair}$ 原式。

- **第一性依据**：能量均分／Bose 占据只在 $M_k>0$ 的模上成立（R-147 已证 $M_k=0$）；(15L.3) 的 $\Upsilon$ 是**同一 $T$ 的刚度**，故 $E_c$ 随 $T$ 变（环 19 的 $w$）；$\sigma_\theta=s\sqrt{2(1-\rho)}\,\sigma_\varepsilon$ 是 $\lambda\to\theta$ 线性映射的恒等式（第 139 轮＋G19 $\alpha=-4\pi s$），不含热学。外部仅 $2\pi$（XY）与 $\pi^2/2$（XY 核能标准）。

- **待建模型/方程**：$y(K)=2\pi e^{-\pi^2K/2}$、$K=\Upsilon/(k_BT)$；`TargetPropFugStiff`（$K$ 严格增 ⇒ $y$ 严格减）、`TargetPropFugBound`（$y(K)\le y(1/\beta)\iff K\ge1/\beta$）、`TargetPropUpsLower`（$1/\beta\le\Upsilon_0w/T\Rightarrow\Upsilon_0\ge T/(\beta w)$）。

- **本环输出**：(161.4) 第二等号与 (161.5) 撤销；(161.1) 第一等号保留为恒等。数值：$w(T_c)=0.758705$、$K(T_c)=1.64365\Rightarrow y(T_c)=1.8862\times10^{-3}\in[\,1.8862\times10^{-3},0.02501\,]$（$\Phi=0.68135$ 顶到上界）；$\Upsilon_0\ge0.442819$（**否证**第 163 轮 KAP 支 $\Upsilon_0=0.206875$，其 $y(T_c)=0.4752$ 越 (15L.5)）；$t(T_c)=1.01420$（$m=1$）／$1.02841$（$m=2$）；$T_{\rm sync}(m{=}1)\in[0.42603,0.50665]$、$T_{\rm sync}(m{=}2)\in[0.38821,0.47071]$、$T_*=0.651929$（与 $y$ 无关）；$y$ 小参数域在 $T_{\rm break}=0.73044$（$K=0.372432$）终止。

- **下一环消费哪部分**：下游 $p_{\rm lock}=1-y$ 只消费 $y(T)$ 的**形状与窗口**（不消费点值）；$m\ge2$ 的共点联合修正消费 $\sigma_\theta$ 的恒等式（其绝对尺度由 $\sigma_\varepsilon$ 外部给）；**不消费** $\sigma_\theta^2=k_BT/\Upsilon_0$ 与 (161.5) 的 $\Upsilon_0$ 反解式。



**第 184 轮（已作废，见 DISCARD 第 185 轮行）**：曾把冲突读成"热支/非热支二选一"；第 185 轮回读原文后判定该分岔由 (161.4) 第二等号这一处越权制造，两 Horn 框架不成立。



**第 179 轮（ρ 的载体核审计：$J_0$ 是 2D 核，载体却是 3D）**



- **本环输入**：第 177／178 轮的 $\rho_1=0.048930$（Bessel $J_0$、$m_{\rm eff}=2$）；第 85 轮 $m_{\rm eff}=2n+1-s\Rightarrow2$；第 157 轮 ρ_nn 表（2D⇒$m{=}2$、3D⇒$m{=}3$）；README 第 865 行（06 的 $\varepsilon$ 载体是 3D Regge，2D 晶格只承担 $p_c$／BKT）。

- **第一性依据**：$\sigma^2\propto\int d^dq\,|G_q|^2/\omega_q$ ⇒ $m_{\rm eff}=2n+(d-1)-s$（谱和定义展开）；$J_0$ 与 $j_0$ 是不同维数的核（定义）。

- **待建模型/方程**：$\rho_m(r)=(m+1)\int_0^1u^mK(\pi ur/a)du$，$K\in\{J_0,j_0\}$；$\rho_{XY}=(2\rho_1-1-\rho_2)/[2(1-\rho_1)]$。

- **本环输出**：四支表（$\rho_1$ 跨 $[-0.031,+0.304]$）；$C_{\rm lock}-1\le2.5\times10^{-6}$、$T_{\rm sync}(m{=}2)\in[0.60964,0.61114]$ ⇒ 量级结论分支无关；$\rho_1$ 定值撤回。

- **下一环消费哪部分**：下游只消费"$C_{\rm lock}\approx1$（量级）"；**不消费**任何一支的 $\rho_1$ 数值，直到载体层与核被钉死。



**第 178 轮（θ_c 取回、跨层同核、聚集修正接入 m=2）**



- **本环输入**：第 161 轮 (161.2)（$p_{\rm lock}=\Pr[|\theta|<\pi]$、$y=\operatorname{erfc}(\pi/\sqrt2\sigma_\theta)$）；第 177 轮 v7 的 $\rho_1=0.048930$、$\rho_2=-0.093848$（Bessel 核＋$m_{\rm eff}=2$）；第 139 轮 $\delta\lambda=\kappa_f\delta\varepsilon$ 一阶。

- **第一性依据**：相位以 $2\pi$ 为周期 ⇒ 失锁阈 $|\theta|=\pi$（链内判据）；公共线性因子 $\kappa_f$ 不改变相关系数（一阶）；$y$ 与 $a$ 由同一 $\operatorname{erfc}$ 关系互定，无需新参数。

- **待建模型/方程**：$a(T)=\Phi^{-1}(1-y(T)/2)$；$p_{\rm lock}^{(2)}=C_{\rm lock}(a(y))\,(1-y)^2$；`TargetPropAdjCorrScale`。

- **本环输出**：$a(T_c)=3.802960$；$C_{\rm lock}-1$ 从 $1.55\times10^{-6}$（$T_c$）到 $8.70\times10^{-3}$（$T=0.72$）；$T_{\rm sync}^{(2)}$ $0.6092298\to0.6107161$（$+0.24\%$），$m=1$ 不变；九模块 A 闸 PASS。

- **下一环消费哪部分**：$m=2$ 支消费 $C_{\rm lock}(a(y))$ 这个乘子；$m=1$ 支不消费（无联合项）；一阶之外的 $O(\sigma^2)$ 未算，下游不得当"精确"用。



**第 177 轮（ρ 的所指与完整协方差：v5→v7）**



- **本环输入**：第 176 轮 `TargetPropAdjCorr`（−1/2）与 B 闸指出的分支问题；权威式 (9.1) $\langle(\delta C_{ij})^2\rangle=2\kappa^2\sigma_0^2(1-\rho_{ij})$；README 第 270 行识别 $\delta C=\delta\lambda$、$\lambda_{ij}=\ln v_{\tau,j}-\ln v_{\tau,i}$；第 84 轮 Bessel 核 $\rho_m(r)$；第 85 轮 $m_{\rm eff}=2$。

- **第一性依据**：差场方差形态 $2v(1-\rho)$ ⇒ $\rho$ 是顶点相关（定义展开）；协方差由三条 Cov 展开（不假设任何一条为零）。

- **待建模型/方程**：$\mathrm{Cov}(X,Y)=v(2\rho_1-1-\rho_2)$、$\mathrm{Var}X=2v(1-\rho_1)$ ⇒ $\rho_{XY}=(2\rho_1-1-\rho_2)/[2(1-\rho_1)]$；`TargetPropAdjCorrGen`（v6，$\rho_2=0$ 情形）与 `TargetPropAdjCorrNear`（v7，完整）。

- **本环输出**：$\rho_1=0.048930$、$\rho_2=-0.093848$、$\rho_{XY}=-0.424938$；工作点 $C_{\rm lock}-1=1.55\times10^{-6}$；八模块 A 闸 PASS。

- **下一环消费哪部分**：只消费"$\rho_{XY}$ 是 (9.1)＋Bessel 核的可算量、工作域内修正 $\lesssim10^{-6}$"；"顶点独立"不再作为前件；$-0.424938$ 不进入下游方程（$\theta_c$ 未定，$C(a)$ 只作函数）。



**第 176 轮（共点键相位相关与条件层误差量级）**



- **本环输入**：第 173 轮 `pLockCond y m=(1-y)^m`（条件层）；第 161 轮顶点相位与 $\sigma_\theta^2=k_BT/\Upsilon_0$（E 类外部）；$y(T_c)=1.43\times10^{-4}$。

- **第一性依据**：方差加法、协方差对称性、相关系数定义（三条均为定义展开，不引新公设、不引文献数值）。

- **待建模型/方程**：$X=\theta_i-\theta_j$、$Y=\theta_j-\theta_k$ ⇒ $\rho=-v/\sqrt{2v\cdot2v}=-1/2$；修正比 $C_{\rm lock}(a)=P(|X|<a,|Y|<a)/P(|X|<a)^2$，$C_{\rm unlock}(a)$ 同构，$a=\theta_c/\sqrt{2v}$。

- **本环输出**：`TargetPropAdjCorr`＋`Ring15LockCorr`（A 闸 PASS）；$C_{\rm lock}(a)$／$C_{\rm unlock}(a)$ 曲线＋工作点 $C_{\rm lock}-1=2.93\times10^{-6}$。

- **下一环消费哪部分**：只消费"工作域内 $C_{\rm lock}$ 偏离 1 不超过 $\sim10^{-5}$"这条量化注记（给 `pLock` 标适用域）；$\rho=-1/2$ **不进方程、不充当"键独立已证"**。



- **本环输入**：第 173 轮的 `pLockCond`／`pLockUncond`；$y=2\pi e^{-E_c/T}$（第 155／161 轮）；$E_c=\pi^2\Upsilon_0/2$（第 159 轮）；第 168 轮弹性 0.1725。

- **第一性依据**：$E_c\uparrow\Rightarrow y\downarrow$（指数单调，$T>0$）；$y\downarrow\Rightarrow p_{\rm sync}\uparrow$（$(1-y)^m$ 单调不增，$0\le y\le1$）。两条初等单调性，不引新公设。

- **待建模型/方程**：`pSync=p_pair(1-y)^m`、`yFug=2\pi e^{-E_c/T}`；`TargetPropFugMono`、`TargetPropSyncMono`。

- **本环输出**：`Ring15LockMono`（2 条定理，A 闸 PASS）＋ 线性化 $\sigma_{T_{\rm sync}}/T_{\rm sync}\approx0.1725\,\sigma_\Upsilon/\Upsilon$。

- **下一环消费哪部分**：只消费方向与展宽系数；组合「$E_c\uparrow\Rightarrow p_{\rm sync}\uparrow$」因需 $y\le1$（外部 $2\pi$）**主动不写**。



**第 173 轮（授权层形式化，保留）**



- **本环输入**：第 170 轮判定（"独立键"是座级授权的跨层外推；应钉条件层）；$(1-y)^m$ 与 $p^{t}=p_{\rm pair}p_{\rm lock}$ 反解（第 163 轮）；SB.3 的 $q=p^2$（座独立、$q_c=0.351348$）。

- **第一性依据**：链内 $q=p^2$ 与 $\rho=p/(1+p)=0.372154$（由 (SB.3) 协方差 $p^3(1-p)$ 算得）；概率值域 $[0,1]$ 的显式侧条件；不引新公设、不引外部文献。

- **待建模型/方程**：两层锁定概率 `pLockCond y m = (1-y)^m` 与 `pLockUncond q y m = q^m (1-y)^m`；命题 `TargetPropLayer`：$0\le q\le1$、$0\le y\le1$ 时无条件层 ≤ 条件层，且 $q=1$ 时相等。

- **本环输出**：`Ring15Spec` v3（三个定义）＋`Ring15LockLayer`（`targetPropLayer : TargetPropLayer`、`cond_eq_pLock : pLockCond y m = pLock y m`）；A 闸 `[propext, Classical.choice, Quot.sound]`，类型逐项对齐 Spec。

- **下一环消费哪部分**：下游只消费**条件层**（`pLock`／`pLockCond` 及其数值），`pLockUncond` 仅作"若跨层会压低"的形式侧证据，不进入任何数值链；`cond_eq_pLock` 保证第 163 轮数值（$0.8754138$／$0.627385$／$0.609230$）不变。



**第 163 轮（第二段，保留）**



- **本环输入**：第 162 轮 `mLock_eq_one`（$m_{\rm lock}=1$ 已证）；R-158 的 $p_{\rm sync}=p_{\rm pair}p_{\rm lock}$ 与 $p^t$ 反解；SB.3 独立键系综（与 $p_{\rm pair}$ 同层）；逸度 $y=2\pi e^{-E_c/k_BT}$（$E_c$ 由第 155 轮反演，前因子为外部边界）。

- **第一性依据**：链内独立键（继承 SB.3 键渗流假设，不新立）＋$m_{\rm lock}=1$；外部（B 类）逸度 $e^{-E_c/T}$ 的 XY/BKT 标准。

- **待建模型/方程**：$p_{\rm lock}(y,m)=(1-y)^m$；$t_{\rm eff}=1+m\ln(1-y)/\ln p$；`TargetPropLock` 四条。

- **本环输出**：`Ring15LockProbability`（`targetPropLock : TargetPropLock` 等 7 条），A 闸通过；数值：$t(T_c)$ 由 $1.0010758$（$m{=}1$）到 $1.0021516$（$m{=}2$），$T_{\rm sync}$ 由 $0.6274$ 压到 $0.6092$。

- **下一环消费哪部分**：同步判据只消费 $m=1$ 一支；$t(2)>t(1)$ 仅作星级读法的定量对照，`M8` 不消费。



## 四、复现命令汇总



```bash

# Lean（在 Lean源码 目录，绝对路径指向本目录文件）

lake env lean "<本目录>/05_Lean验证/<文件>.lean"

# 本机无 git 时 lake env 会因 manifest 刷新失败：改用 lean 直驱（工作目录在 05_Lean验证）

lean -o .\olean_tmp\Ring15Spec.olean .\Ring15Spec.lean   # 出 Spec 的 olean（模块名 = 文件名）

lean .\Ring15LockMult.lean                                # LEAN_PATH 追加 .\olean_tmp 与各包 lib/lean

# 数值（在本目录 04_计算验证）

python "<文件>.py"

# 组织层

python "08 理论组织和形式化框架/_build/check_consistency.py"

python "08 理论组织和形式化框架/_build/check_provenance.py"

```



## 五、A/B 闸当前状态（诚实登记）



- **A 闸（机器）**：第 162 轮已对环 15 三个模块逐条跑 `#print axioms`，全部仅 `propext`／`Classical.choice`／`Quot.sound`，无 `sorryAx`、无自造 `axiom`；`Ring15Spec`(只含定义)→`Ring15LockMult`(仅 import Spec) 两路径比对成立，主定理类型即 `TargetProp`。第 163 轮新增 `Ring15LockProbability`（`targetPropLock : TargetPropLock`，`rpow_m2` 等）同样仅 `[propext, Classical.choice, Quot.sound]`。第 173 轮新增 `Ring15LockLayer`（`targetPropLayer : TargetPropLayer`、`cond_eq_pLock`），同样仅 `[propext, Classical.choice, Quot.sound]`；第 175 轮新增 `Ring15LockMono`（`targetPropFugMono`／`targetPropSyncMono`），仅 `[propext, Classical.choice, Quot.sound]`；`#check (… : CQM.Ring15.Spec.TargetPropLayer)` 等五条强制标注通过；`Ring15LockProbability` 在 v3/v4 上重编译 exit 0（数值不变）。第 174 轮已把该流程固化为 `a_gate.ps1`；第 185 轮随 Spec v12 把 `Ring15LockBridge` 撤出、由 `Ring15LockStiff` 接替，实跑**十二模块 PASS**（12/12 编译、20 条 axioms、15 条 `#check`、241 文件 0 命中、exit 0）；第 186 轮 Spec v13 增 `TargetPropTEffMMono`／`TargetPropTEffMGeOne`，`Ring15LockT` 接入后实跑**十三模块 PASS**（13/13 编译、22 条 axioms、17 条 `#check` 类型对齐、242 文件 0 命中、exit 0）；第 187 轮 Spec v14 增 `pPairThr`／`TargetPropThrLog`／`TargetPropThrRpow`，`Ring15LockThr` 接入后实跑**十四模块 PASS**（14/14 编译、24 条 axioms、19 条 `#check`、243 文件 0 命中、exit 0）；第 188 轮 Spec v15 增 `rOfW`／`sOfLock`／`TargetPropROfEps`／`TargetPropSFail`，`Ring15LockR` 接入后实跑**十五模块 PASS**（15/15 编译、26 条 axioms、21 条 `#check`、244 文件 0 命中、exit 0）。第 176 轮扩到**六模块**、第 177 轮扩到**八模块**（加 `Ring15LockCorrGen`／`Ring15LockCorrNear`）、第 178 轮扩到**九模块**（加 `Ring15LockScale`）并实测 PASS（13 条 axioms、9 条 `#check` 强制类型标注、238 个 `.lean` 去注释 0 命中，exit 0）。第 189 轮 Spec v16 增 `phiBkt`／`phiMin`／`TargetPropPhiMono`／`TargetPropPhiBktVal`／`TargetPropPhiMinEq`／`TargetPropPhiConflict`，`Ring15LockPhi` 接入后实跑**十六模块 PASS**（16/16 编译、30 条 axioms、25 条 `#check`、245 文件 0 命中、exit 0）；第 190 轮 Spec v17 增 `wGap`／`TargetPropWGapPos`／`TargetPropWGapAnti`／`TargetPropWGapLeOne`（＋两条基线 import：`IntervalIntegral.Basic`、`Complex.Trigonometric`），`Ring15LockW` 接入后实跑**十七模块 PASS**（17/17 编译、33 条 axioms、31 条 `#check`、246 文件 0 命中、exit 0）；第 191 轮 Spec v18 增 `TargetPropSolSurj`／`TargetPropSolNeg`（$s$ 同名判否），`Ring15LockS` 接入后实跑**十八模块 PASS**（18/18 编译、35 条 axioms、33 条 `#check`、247 文件 0 命中、exit 0）；第 192 轮 Spec v19 增 `TargetPropWGapStrictAnti`（$w$ 严格减，G-190b 收口），`Ring15LockWStr` 接入后实跑**十九模块 PASS**（19/19 编译、36 条 axioms、34 条 `#check`、248 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 十九模块 v19）`）；第 193 轮 Spec v20 增 `yOfT`／`TargetPropKStrictAnti`／`TargetPropYStrictMono`／`TargetPropTStrictMono`（G-186 通道严格化），`Ring15LockTStrict` 接入后实跑**二十模块 PASS**（20/20 编译、39 条 axioms、37 条 `#check`、249 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 二十模块 v20）`）；第 194 轮 Spec v21 增 `TargetPropTEffMPMono`／`TargetPropTChanSplit`（$ 通道方向＋两通道反号分解），`Ring15LockTChan` 接入后实跑**二十一模块 PASS**（21/21 编译、41 条 axioms、39 条 `#check`、250 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 二十一模块 v21）`）；第 195 轮 Spec v22 增 `TargetPropTChanDominate`／`TargetPropTChanCriterion`（主导项闸＋充要判据），`Ring15LockTDom` 接入后实跑**二十二模块 PASS**（22/22 编译、43 条 axioms、41 条 `#check`、251 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 二十二模块 v22）`）；第 196 轮 Spec v23 增 `sechSq`／`wGapDeriv`／`TargetPropWGapDeriv`／`TargetPropWGapDerivNeg`（$w$ 的导数表示，G-190c），`Ring15LockWD` 接入后实跑**二十三模块 PASS**（23/23 编译、45 条 axioms、43 条 `#check`、252 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 二十三模块 v23）`）；第 197 轮 Spec v24 增 `TargetPropWGapIbp`／`TargetPropShapeSplit`／`TargetPropShapeEnd`／`TargetPropShapeEndGt`（分部积分恒等式与形状项分解，G-188a），`Ring15LockIbp` 接入后实跑**二十四模块 PASS**（24/24 编译、49 条 axioms、47 条 `#check`、254 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 二十四模块 v24）`）；第 198 轮 Spec v25 增 `wGapDeriv2`／`shapeDeriv`／`TargetPropWGapDeriv2`／`TargetPropShapeDeriv`（$w''$ 与形状项导数，G-188b 第一步），`Ring15LockWD2` 接入后实跑**二十五模块 PASS**（25/25 编译、51 条 axioms、46 条 `#check`、257 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 二十五模块 v25）`）；第 199 轮 Spec v26 增 `wGapDeriv2Alt`／`TargetPropWGapDeriv2Alt`／`TargetPropWGapDeriv2Pos`／`TargetPropShapeDerivSign`（端点闭式与两条判据，G-188b-2），`Ring15LockWD3` 接入后实跑**二十六模块 PASS**（26/26 编译、54 条 axioms、49 条 `#check`、256 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 二十六模块 v26）`）；第 200 轮 Spec v27 增 `shapePhi`／`ratioR`／`TargetPropShapeSignRatio`／`TargetPropShapeNegOfRatioGeOne`（比值判据与 $r\ge1$ 段符号），`Ring15LockWD4` 接入后实跑**二十七模块 PASS**（27/27 编译、56 条 axioms、51 条 `#check`、256 文件 0 命中，末行 `A 闸 PASS（限环 15 二十七模块 v27）`）。token 卫生：本目录 `.lean`（去注释）与本次 A 闸实扫均 0 命中。**三类真实失败已记档**：①首版 `targetPropSyncMono` 单调方向写反，编译直接拒稿；②首版 `Ring15LockCorr` 在 `field_simp` 后仍写 `ring`，报 `No goals to be solved`；③首版 `Ring15LockCorrGen` 的 `Real.sqrt_sq` 期望 `(a)^2` 而给了 `a*a`，补 `ring` 重写 `a*a=a^2` 后通过。

  - **A 闸（第 209 轮，三十四模块）**：Spec v34 变更使全部下游 olean 失效，按依赖序重编 `LockW→LockWD→LockIbp→LockUnary→LockDeficit→LockLambda→LockTail` 后跑全闸，**PASS**：34/34 编译 ok、76 条 axioms 全 `{propext, Classical.choice, Quot.sound}`、72 条 `#check` 全 `[ ok ] type: … : Spec.…`、`[FAIL` 0、`token: {"files": 263, "hits": []}`、exit 0（约 30 分钟），末行 `A 闸 PASS（限环 15 三十四模块 v34）`。

- **A 闸（第 210 轮，三十五模块）**：Spec v35 变更使全部下游 olean 失效，按依赖序重编 `LockW→LockWD→LockIbp→LockUnary→LockDeficit→LockLambda→LockTail→LockTailRatio` 后跑全闸，**PASS**：35/35 编译 ok、79 条 axioms 全 `{propext, Classical.choice, Quot.sound}`、75 条 `#check` 全 `[ ok ] type: … : Spec.…`、`[FAIL` 0、`token: {"files": 264, "hits": []}`、exit 0，末行 `A 闸 PASS（限环 15 三十五模块 v35）`。

- **A 闸（第 211 轮，三十六模块）**：Spec v36 变更使全部下游 olean 失效，按依赖序重编 36 个模块后跑全闸，**PASS**：36/36 编译（含新模块 `Ring15LockNearZero`）、82 条 `#print axioms` 全为 `{propext, Classical.choice, Quot.sound}`、78 条 `#check` 全 `[ ok ] type: … : Spec.…`、`[FAIL` 0、token 扫描 265 个 `.lean` 0 命中、exit 0，末行 `A 闸 PASS（限环 15 三十六模块 v36）`（约 27 分钟）。

- **A 闸（第 212 轮，三十七模块）**：Spec v37 变更使全部下游 olean 失效，按依赖序重编 37 个模块后跑全闸，**PASS**：37/37 编译（含新模块 `Ring15LockZeroExists`）、83 条 `#print axioms`（80 条为 `{propext, Classical.choice, Quot.sound}`、3 条为 `{propext, Quot.sound}` 子集）、79 条 `#check` 全 `[ ok ] type: … : Spec.…`、`[FAIL` 0、token 扫描 266 个 `.lean` 0 命中、exit 0（约 28 分钟），末行 `A 闸 PASS（限环 15 三十七模块 v37：编译 + axioms 白名单 + 类型对齐 + token 卫生）`。

- **A 闸（第 213 轮，三十八模块）**：Spec v38 变更使全部下游 olean 失效，按依赖序重编 38 个模块后跑全闸，**PASS**：38/38 编译（含新模块 `Ring15LockZeroUnique`）、85 条 `#print axioms` 指令（日志中公理行 83 条：80 条 `{propext, Classical.choice, Quot.sound}`＋3 条 `{propext, Quot.sound}`）、80 条 `#check` 全 `[ ok ] type: … : Spec.…`（含新一条 `targetPropGapZeroUniqueOfRatioMono`）、`[FAIL` 0、token 扫描 267 个 `.lean` 0 命中、exit 0（约 28 分钟），末行 `A 闸 PASS（限环 15 三十八模块 v38：编译 + axioms 白名单 + 类型对齐 + token 卫生）`。

- **A 闸（第 214 轮，三十九模块）**：Spec v39 变更使全部下游 olean 失效，按依赖序重编 39 个模块后跑全闸，**PASS**：39/39 编译（含新模块 `Ring15LockRatioForm`）、87 条公理行全在白名单（82 条 `{propext, Classical.choice, Quot.sound}`＋5 条 `{propext, Quot.sound}` 子集；闸日志按 `[ ok ]` 前缀计得 85 行，属拼接换行未计入，另以 `_chk214.lean` 独立重放复核为 87/87）、82 条 `#check` 全 `[ ok ] type: … : Spec.…`（含新增两条 `targetPropDeficitRatioPos`／`targetPropRatioOverLambdaPos`）、`[FAIL` 0（日志中唯一命中 "FAIL" 的是定理名 `targetPropSFail`）、token 扫描 268 个 `.lean` 0 命中、exit 0，末行 `A 闸 PASS（限环 15 三十九模块 v39：编译 + axioms 白名单 + 类型对齐 + token 卫生）`。

**仍未完成**：本目录其余定理未逐条跑 axioms；且**已部分固化**——第 174 轮把环 15 四模块的整套流程落成一键脚本 `05_Lean验证/a_gate.ps1`（编译＋axioms 白名单＋类型标注＋token 卫生，非零退出码），首次运行 `A 闸 PASS（限环 15 四模块）`，但**全目录仍未纳入**，故 A 闸对全目录仍不能宣称"完全通过"。

- **A 闸（第 201 轮，v28）**：Spec v28 增 `shapeH`／`TargetPropRatioPhiForm`／`shapeG`／`TargetPropShapeSignUnary`，`Ring15LockUnary` 接入后实跑**二十八模块 PASS**（28/28 编译、58 条 axioms 全为 `{propext, Classical.choice, Quot.sound}`（其中若干条仅 `{propext, Quot.sound}`）、53 条 `#check` 全部 `[ ok ] type: … : Spec.…`、257 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 二十八模块 v28）`）；两条新主定理的类型与 Spec 逐项对齐（`targetPropRatioPhiForm : Spec.TargetPropRatioPhiForm`、`targetPropShapeSignUnary : Spec.TargetPropShapeSignUnary`），Spec 仍只 import 基线、不 import 任何证明模块。

- **A 闸（第 202 轮，v29）**：Spec v29 增 `deficitFrac`／`endpointLambda`／`TargetPropRatioBracketLow`／`TargetPropRatioBracketHigh`／`TargetPropLambdaForm`／`TargetPropShapeSignDeficit`，`Ring15LockDeficit` 接入后实跑**二十九模块 PASS**（29/29 编译、62 条 axioms 全为 `{propext, Classical.choice, Quot.sound}`（其中若干条仅 `{propext, Quot.sound}`）、57 条 `#check` 全部 `[ ok ] type: … : Spec.…`、258 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 二十九模块 v29）`）；四条新主定理类型与 Spec 逐项对齐（`targetPropRatioBracketLow : Spec.TargetPropRatioBracketLow` 等），Spec 仍只 import 基线、不 import 任何证明模块。闸前单独编译口径：Spec 65–85 s、单证明模块 35–50 s，一次实跑约 21 分钟。

- **A 闸（第 203 轮，v30）**：Spec v30 增 `deficitRatio`／`TargetPropDeficitRatioMono`／`TargetPropLambdaStrictMono`／`TargetPropLambdaBounds`，`Ring15LockLambda` 接入后实跑**三十模块 PASS**（30/30 编译、65 条 axioms 全为 `{propext, Classical.choice, Quot.sound}`（其中若干条仅 `{propext, Quot.sound}`）、60 条 `#check` 全部 `[ ok ] type: … : Spec.…`、259 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 三十模块 v30）`）；三条新主定理类型与 Spec 逐项对齐（`targetPropDeficitRatioMono : Spec.TargetPropDeficitRatioMono` 等），Spec 仍只 import 基线、不 import 任何证明模块。单独编译口径：Spec v30（624 行／38.7 KB）exit 0、`Ring15LockLambda` exit 0，A 闸实跑约 20–25 分钟。

- **B 闸（第 203 轮）**：判**定义式**；最可能跑偏行＝`tanh_lt_self` 里 $s-\tanh s=\int_0^s\tanh^2$ 的严格性交代（若只写 $\tanh s\le s$ 或漏 $s>0$，证出的是"$\lambda$ 不增"而非严格单增）。三条命题分开立、值域单独立条，$\lambda$ 单增的类型里不出现 $\Phi$／$w$，从类型层排除"借 $\Phi$ 单调带过"。

- **A 闸（第 204 轮，v31）**：Spec v31 增 `deficitDeriv`／`TargetPropDeficitDeriv`／`TargetPropDeficitDerivPos`／`TargetPropDeficitStrictMono`／`TargetPropDeficitRatioStrictMonoT`，`Ring15LockDeficitMono` 接入后实跑**三十一模块 PASS**（31/31 编译、68 条 `[ ok ] axioms`（第 69 条因三元组换行拆成三行未计入行数，单跑复核仍为 `[propext, Classical.choice, Quot.sound]`）、64 条 `#check` 全部 `[ ok ] type: … : Spec.…`、`[FAIL` 计数 0、`token: {"files": 260, "hits": []}`、exit 0，末行 `A 闸 PASS（限环 15 三十一模块 v31）`）；四条新主定理类型与 Spec 逐项对齐（`targetPropDeficitDeriv : Spec.TargetPropDeficitDeriv` 等），Spec 仍只 import 基线、不 import 任何证明模块。单独编译口径：Spec v31 exit 0、`Ring15LockDeficitMono`（约 300 行）exit 0 零告警；A 闸实跑约 25 分钟。

- **B 闸（第 204 轮）**：判**定义式**。逐问：下游（205）消费的是 $\delta'$ 的闭式与符号，不是"$\delta$ 单增"这句结论；靠定义展开（商法则＋`Tanh` 的链式求导）而非命名带过；语义上 $\Phi'=-\delta'$ 是同一条定理的两个面，非同名不同义；量词全程为 $\forall T>0$、$\forall T_1T_2$，无单点特例偷换；尺度·参数·索引只出现 $T$ 与窗口积分变量 $u$，均显式。**防抵消**：$R(\delta(\cdot))$ 的严格单增是"复合"而非"归一化吃掉符号"，且 $\delta'>0$ 另立一条，不靠 $R$ 侧结论反推。最可能跑偏行＝`hasDerivAt_deficit` 的 `hval`（值恒等 `0 + -(q) = deficitDeriv`，若漏 `shapeH T ^ 2 ≠ 0` 则 `field_simp` 仍能凑式而两侧差号）；次危险＝`point_ge_T`／`point_gt_T` 的 `unfold shapeH sechSq; rw [hv]`（$u$ 与 $T$ 的角色若对调，$\sinh(2us)\le u\sinh(2s)$ 会变成另一不等式）。两处均有数值锚（$\delta'$ 闭式 vs 差分 rel $\le1.2\times10^{-9}$、核比全程 $<1$）。

- **B 闸（接地）**：第 159 轮的 `m_lock=1` 在 v1 Spec 里"定义式冒充命题"（跑偏候选），已由第 162 轮修订为键级基数＋充要刻画，判**定义式通过（限键级计数口径）**。第 163 轮把 $p_{\rm lock}=(1-y)^m$ 形式化，判**定义式通过（限独立键系综）**；第 170 轮审计出该"独立"是**跨层外推**（座独立 $\ne$ 键独立，$\rho=0.372154$），已把授权钉到**条件层**并登记偏差，未闭合项改为"条件'给定键已存在'的链内来源"与逸度前因子 $2\pi$；`审-6` 仍未闭合。第 176 轮把这条**条件层独立假设的偏差算了出来**：共点两键的相位差满足 $\rho=-1/2$（顶点相位独立等方差的算术恒等式，`Ring15LockCorr` 已证，A 闸 PASS），由此 $|X|,|Y|$ 正关联 ⇒ 都锁/都失锁均聚集（$C_{\rm lock}>1$ 恒成立）；工作点 $y=1.43\times10^{-4}\Rightarrow a=3.803\Rightarrow C_{\rm lock}-1=2.93\times10^{-6}$，故独立假设在工作域内数值可忽略，但**顶点相位独立本身仍是第 161 轮 E 类输入，未由链内推出** ⇒ 判"假设已命名＋偏差已量化"，仍不闭合；$a\sim1$（锁定接近对半）时偏差 $7\%$／$32\%$，故同时给 `pLock` 划出适用域 $y\lesssim10^{-2}$。**B 闸另抓到分支问题（留作下一环最该修的一处）**：(9.1) 的 $\mathrm{Var}(\lambda_{ij})=2\kappa_f^2\sigma^2(T)(1-\rho)$ 的 $(1-\rho)$ 形态说明顶点相关不为 0，故 $\rho_{XY}=-1/2$ 只是 $\rho_v=0$ 一支，一般式 $\rho_{XY}=(2\rho_v-1)/(2(1-\rho_v))$；$\rho_v=0.372154$ 给 $-0.203626$。两支在工作点的偏差均 $\lesssim10^{-6}$（$1.0000029$ vs $1.0000002$），故"工作域可忽略"不受影响，但陈述须锁支；$\rho_v$ 所指须先从 (9.1) 权威定义处取出，**未取定前 $-1/2$ 不进入任何下游方程**。**第 177 轮已取定**：$\rho$ 是顶点相关（(9.1) 差场形态＋$\delta C=\delta\lambda$），链内取值由 Bessel 核与 $m_{\rm eff}=2$ 给出 $\rho_1=0.048930$、$\rho_2(2a)=-0.093848$，完整式 $\rho_{XY}=(2\rho_1-1-\rho_2)/[2(1-\rho_1)]=-0.424938$；三版（$-0.5$／$-0.474276$／$-0.424938$）在工作点的 $C_{\rm lock}-1$ 均在 $10^{-6}$，故数值结论不变，"顶点独立"作为链内前件**被否证**；`审-6` 仍不闭合（缺 $\rho$ 的 $m_{\rm eff}$ 定值、$2\pi$ 前因子、和乐层）。**第 178 轮补上两处并接入数值**：$\theta_c=\pi$ 见 (161.2) ⇒ $a=\Phi^{-1}(1-y/2)$ 由 $y$ 自定（$T_c$ 处 $3.802960$，上一轮"未取"是漏读）；跨层同核由第 139 轮一阶 $\delta\lambda=\kappa_f\delta\varepsilon$＋`TargetPropAdjCorrScale`（$\rho_{XY}$ 与公共振幅无关）支撑；$m=2$ 支改为 $p_{\rm lock}^{(2)}=C_{\rm lock}(a(y))\,(1-y)^2$，$C_{\rm lock}-1$ 从 $T_c$ 的 $1.55\times10^{-6}$ 到 $T=0.72$ 的 $8.7\times10^{-3}$，$T_{\rm sync}^{(2)}$ $0.6092298\to0.6107161$（$+0.24\%$），$m=1$ 不变。仍不闭合：$O(\sigma^2)$ 与非线性映射未算、$2\pi$、和乐层。

- **同名不同义风险**：$m_{\rm lock}$（键条数）≠ 外部文献的涡旋绕数 $n\in\mathbb Z$，下游若混用即语义漂移（见 `03_推导工作台/环15_审6_m_lock定义授权与双闸审计.md` §四）。

- **本环停点（第 201 轮）**：环 15／`审-6`；缺口 **G-188b-2f**（$S'$ 的一元判据 $0<G(T)$ 已进链，但 $G$ 的符号与极小 $T_{\min}$ 的链内编址未证）；**最该修的一处＝$\Phi$ 的单调性**（缺 $\Phi'$ 的链内表示与符号，现只有 $T\to0$ 的 $\Phi\to1$、$T\to\infty$ 的 $\Phi\to2/3$ 两端渐近，且均未进 Lean）；依据＝卡 §三十四 34.7、`Ring15LockUnary` 两条定理已锁（A 闸二十八模块 PASS）、`环15_判据一元化_数值核对.py`（$G$ 与 $S'$ 同号 0 处不符、变号括号 $[0.3430,0.3440]$）；**其中"最该修＝$\Phi$ 的单调性"已被第 202 轮代数否决**（见下一条）。

- **本环停点（第 203 轮）**：环 15／`审-6`；缺口 **G-188b-2i**（交点 $T_{\min}$ 的链内编址：两侧 $\lambda$ 与 $R(\delta(T))$ 已各自严格单增（三条定理），但同增只保证"若相交则唯一"，不定位交点）；**最该修的一处＝$\delta(T)=1-\Phi(T)$ 的链内单调性（即 $\Phi'$ 的链内表示）**——**该处已被第 204 轮修掉**（$\Phi'=-\delta'$，$\delta'$ 有闭式且处处正）；依据＝卡 §三十六 36.7、`Ring15LockLambda` 三条定理（A 闸三十模块 PASS）、`04_计算验证/环15_判据两侧单调性_数值核对.py`（变号点 $T\approx0.19415$、$T_{\min}=0.343857873$）。

- **本环停点（第 204 轮）**：环 15／`审-6`；缺口 **G-188b-2i**（交点 $T_{\min}$ 的链内编址：$\delta$ 侧已从数值升为四条定理——$\delta'$ 闭式、$\delta'>0$、$\delta$ 严格单增、$R(\delta(T))$ 严格单增，且"$\Phi'$ 未进 Lean"消解，但两侧同增不定位交点）；**最该修的一处＝$\delta'$ 与 $\lambda'$ 的显式比较**（$R'(\delta)\delta'(T)$ 与 $\lambda'(T)$ 的定号决定 $R-\lambda$ 的走向；两条闭式都已进链，缺的是比较不等式的链内证明或显式包络）；依据＝卡 §三十七 37.3 与 37.7、`Ring15LockDeficitMono` 四条定理已锁（A 闸三十一模块 PASS）、`04_计算验证/环15_δ导数与核不等式_数值核对.py`（$\delta'$ 闭式 rel $\le1.2\times10^{-9}$、核比最大 $0.955319$、$\delta'$ 最小 $0.012499$、$T_{\min}=0.343857873$ 不变）。

- **A 闸（第 205 轮，v32）**：Spec v32 增 `lambdaDeriv`／`ratioFun`／`ratioFunDeriv`／`criterionGap`／`criterionGapDeriv` 与三条 Prop，`Ring15LockGapDeriv` 接入后实跑**三十二模块 PASS**（32/32 编译、71 条 `[ ok ] axioms`（第 72 条因三元组换行未计入）、67 条 `#check`、`[FAIL` 0、261 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 三十二模块 v32）`）。

- **B 闸（第 205 轮）**：判**定义式**；最可能跑偏行＝`hasDerivAt_lambdaVal` 的 `hval`（值恒等 `-(g')/g² = (cosh/T - sinh)/(T sinh)²`）——若 $\sinh\frac1T\ne0$ 未显式给出就 `field_simp`，$\lambda'$ 的符号会翻转；次危险＝`hasDerivAt_deficitRatio` 的 `hfun`（`rfl`，是 `deficitRatio` 定义漂移的探测器）。$\lambda$ 的转置只在 $(0,\infty)$ 上宣称；$\delta(T)\ne1$ 由 $w>0$、$h>0$ 给出。防抵消：$\lambda'$ 与 $R'\delta'$ 的正性分开存在，$D'$ 的符号未被"两项都正"吸收。

- **本环停点（第 205 轮）**：环 15／`审-6`；缺口 **G-188b-2k**（$D'$ 的符号结构：$D=R(\delta)-\lambda$ 要"单峰且恰一零点"，须证 $D'$ 在 $(0,\infty)$ 上**恰有一个零点**（等价地 $D$ 单峰）；206 轮已否证其强条件"$D'$ 严格单减"（数值上 $D'$ 是 U 形，见 `DISCARD.md` 206-1），故意图命题改写为"零点唯一"；现只到 $D'$ 有闭式）；**最该修的一处＝$\delta''$ 与 $\lambda''$ 的闭式及其符号**（要拿 $\delta'$ 再求导并读出 $D''<0$）；**依据**：205 数值上 $D'$ 只在 $T\approx0.19415$ 变号一次、$D$ 只在 $T_{\min}=0.343857873$ 取零、极大 $7.5013\times10^{-2}$，两端异号——这是"单峰＋恰一零点"的数值显影，但二阶信息尚未进链；两条一阶闭式均已在链内（`deficitDeriv`、`lambdaDeriv`）。

- **本环停点（第 206 轮，第 0–1 步即停）**：环 15／`审-6`；缺口仍 **G-188b-2k**（$D$ 单峰／$D'$ 零点唯一）。本轮先做可行性核对，**否证了 205 停点写下的强意图**："$D'$ 在 $(0,\infty)$ 严格单减"不成立——数值上 $D'$ 是 U 形（$0.10$：$+0.6545$；$0.3529$：$-0.7319$ 极小；$1.50$：$-0.0470$），$D''$ 在 $(0.03,1.5)$ 内**变号两次**（$\approx0.1099$、$\approx0.3529$）；$D'$ 的零点仍**唯一**（$T^*=0.194153703$）。**最该修的一处＝意图命题的改写与判据的可判化**：把"$D'$ 单减"改为"$D'$ 恰一零点"，并证明 $R'(\delta)\delta'$ 与 $\lambda'$ 两条**单峰曲线**（$\lambda'$ 峰 $1.8598$ 于 $T=0.2951$）的交点唯一；**依据**：`04_计算验证/环15_判据差二阶_输出.txt` §[1][2][3][4]，`DISCARD.md` 206-1／206-2。**本轮不写 Spec**：意图命题尚不成立（强命题已否证、弱命题未证），按"锁定后不得随证明改动"的规矩，宁停不写未证 Prop。

- **本环停点（第 207 轮，第 2 步止于纸面）**：环 15／`审-6`；缺口 **G-188b-2k** 仍未闭。本轮不试二阶，改走**值域分离**：凹性引理（$\tanh(au)\ge u\tanh a$）$\Rightarrow w>\tfrac23h\Rightarrow\delta<\tfrac13$；$R$ 严格单增 $\Rightarrow R(\delta)<\tfrac23$；$\lambda$ 严格单增＋$\lambda(1)=\tfrac1{\sinh1}>\tfrac23$ $\Rightarrow T\ge1$ 时 $\lambda>\tfrac23$ —— 合得 **$T\ge1\Rightarrow D<0$**，即 $\{D=0\}\subseteq(0,1)$；副产物 $0<\delta<\tfrac13$、$0<R<\tfrac23$、$-1<D<\tfrac23$。但四条全是**纸面**（Spec 仍 v32、模块仍三十二、未跑闸），按未证记账。**最该修的一处＝把凹性链形式化**：Mathlib 缺 `tanh` 凹性、凹⇒割线、`sinh 1 < 3/2` 三件；208 先补第一件再升 Spec v33。另 **$D(0^+)>0$ 未证**（须比 $\delta\sim4T^2$ 与 $\lambda\sim2e^{-1/T}/T$，指数 vs 多项式），故"恰一零点"仍需近零端一段。**依据**：卡 §四十（四元组／四步纸面推导／判定）、`04_计算验证/环15_尾段界_输出.txt`。

- **本环停点（第 208 轮）**：环 15／`审-6`；缺口 **G-188b-2k** 未闭。本轮把尾段论证的 $\lambda$ 一侧**进链**：Spec v33 三条 `def`、`Ring15LockTail`（3 定理）、A 闸三十三模块 PASS（74 axioms 全白名单、70 `#check`、`[FAIL` 0、262 文件 0 命中）。但 $\delta<\frac13$ 与 $R(\delta)<\frac23$ 仍在纸面，故 $T\ge1\Rightarrow D<0$ **只有纸面版本**，未合成进链。**最该修的一处＝$\tanh$ 凹性**（$\delta<\frac13$ 的唯一入口；Mathlib 无凹性件，备用路径：$g(u)=\tanh(au)/u$ 单调 ⟺ $\sinh(2au)>2au$，而 `Real.sinh_sub_id_strictMono` 已给 $\sinh y>y$）。**依据**：卡 §四十一（四元组／v33 三条／证明要点／闸结果／B 闸逐问）、`05_Lean验证/Ring15LockTail.lean`、`a_gate.ps1`（v33）。

- **本环停点（第 209 轮）**：环 15／`审-6`；缺口 **G-188b-2k** 仍未闭。本轮把尾段的 **$R$ 侧代数上界与条件合成进链**：Spec v34 两条 `def`（`TargetPropRatioLeOfLeThird`、`TargetPropGapNegOfDeficitLeThird`）、`Ring15LockTailRatio`（2 定理＋2 私有引理）。**注意②是条件形态**——$\delta\le\frac13$ 被写成假设，故 $T\ge1\Rightarrow D<0$ 的**无条件版仍缺**，$\{D=0\}\subseteq(0,1)$ 与 $D(0^+)>0$ 亦缺。**最该修的一处＝$\tanh$ 凹性／割线**（$\delta<\frac13$ 的唯一入口）；现状核实：Mathlib 无 `hasDerivAt_tanh`、无 tanh 的 `ConcaveOn`，可用 `concaveOn_of_hasDerivWithinAt2_nonpos`（`Analysis/Convex/Deriv` L248）但须先自建一阶／二阶导数与 `sechSq` 复合链。**依据**：卡 §四十二（四元组／v34 两条／证明要点／B 闸逐问）、`05_Lean验证/Ring15LockTailRatio.lean`、`a_gate.ps1`（v34）。

- **本环停点（第 210 轮）**：环 15／`审-6`；缺口 **G-188b-2k** 的**尾段已闭、整体未闭**。本轮把 209 剩下的唯一前件 $\delta\le\frac13$ 落地：`TargetPropTanhSecant`（$g(u)=\tanh(au)/u$ 严格减 ⇒ $u\tanh a\le\tanh(au)$）、`TargetPropDeficitLeThird`（积分比较 ⇒ $w\ge\frac23h$）、`TargetPropGapNegTail`（②＋209 ⇒ $T\ge1\Rightarrow D<0$ 无条件），故 $\{D=0\}\subseteq(0,1)$ 成立。**最该修的一处＝近零端**：$D(0)=0$（$w=h=1$、$\delta=0$、$\lambda\to0$），故"近零端正"须先钉成 $\exists\varepsilon>0,\forall T\in(0,\varepsilon),D(T)>0$ 或给出 $D/T^k$ 首项；此后才是 $(0,1)$ 内零点唯一（$D'$ 恰一零点）。**依据**：卡 §四十三（四元组／证明路线／v35 三条／B 闸逐问／残余）、`05_Lean验证/Ring15LockSecant.lean`、`a_gate.ps1`（v35）。

- **本环停点（第 211 轮）**：环 15／`审-6`；缺口 **G-188b-2k** 的**尾段与近零端两段已闭、整体未闭**。本轮把近零端 $D>0$ 进链（v36 三条：`TargetPropDeficitGeSq`／`TargetPropLambdaLeSq`／`TargetPropGapPosNearZero`；`Ring15LockNearZero` 3 定理＋11 私有引理；A 闸三十六模块 PASS），与 210 的 `TargetPropGapNegTail` 合得 $\{D=0\}\subseteq[\frac1{10},1]$。**仍缺**：$(0,1)$ 内零点唯一（等价 $D'$ 恰一零点，含 $[\frac1{10},1]$ 内的交点存在性）；$T\downarrow0$ 的渐近常数（数值 $\delta/T^2\approx3.289868$，链内仅有 $\frac8{15}$ 与 $\frac13$ 两侧界）。下一环（212）入口＝$D'$ 在两段上的符号（或对 $D'$ 分段用 `strictMonoOn`／`strictAntiOn`）。

- **本环停点（第 212 轮）**：环 15／`审-6`；缺口 **G-188b-2k** 的**尾段＋近零端＋零点存在三段已闭、整体未闭**。本轮把"存在至少一个零点"进链（v37 一条 `def`：`TargetPropGapZeroExists`；`Ring15LockZeroExists` 1 定理；A 闸三十七模块 PASS）：由 205 可微性逐点给连续、211 于 $T=\frac1{10}$ 的正性与 210 于 $T=1$ 的负性、`intermediate_value_Icc'` 取介值，再以两端严格异号把零点挤进开区间，得 $\varnothing\neq\{D=0\}\subseteq(\frac1{10},1)$。**仍缺**：零点**唯一**（"至多一个"；$D'$ 恰一零点）；$T\downarrow0$ 的渐近常数。**最该修的一处＝$D'$ 在 $[\frac1{10},1]$ 上的符号分段**（若能给出左段 $D'>0$、右段 $D'<0$ 两条，与 212 的存在性合得唯一性；若分段符号不可证，则退回"$D'$ 在该区间恰一零点"的等值陈述）。依据＝卡 §四十五（四元组／路线／v37／B 闸逐问／残余）、`05_Lean验证/Ring15LockZeroExists.lean`、`a_gate.ps1`（v37）；数值旁证 `04_计算验证/环15_判据差二阶_输出.txt`（$T^*=0.194153703$、$D'$ 极小 $-0.731863$ 于 $0.3529$）。

- **本环停点（第 214 轮）**：环 15／`审-6`；缺口 **G-188b-2k-u**（$Q$ 严格单增／$\lambda'R>\lambda R'\delta'$）**仍未证**。本轮把它的"符号前件"进链：$R(\delta)>0$ 与 $Q>0$（v39 两条 Prop，`Ring15LockRatioForm` 2 定理，A 闸三十九模块 PASS），使 $(Q)'/Q$ 的对数导数写法在链内合法（否则 $\ln Q$ 无定义）；同时**放弃** $Q$ 的乘法闭式（DISCARD 214-1：`field_simp` 后 `(2tanh−w)⁻¹` 消不去，判**证明路径限制**而非命题为假，代数正确性已单独记明）。**最该修的一处＝$\delta'$ 的上界**（204 只有闭式与正性），配 $R'/R$ 的定量界，合成前件；数值余量最小 $0.0985$ 在 $T=1$，而 $\delta'$ 最大在 $T=0.172$，两处不同点 ⇒ 粗界须分段。依据＝卡 §四十七（四元组／为何先做正性／B 闸逐问／放弃分支）、`05_Lean验证/Ring15LockRatioForm.lean`、`a_gate.ps1`（v39）、`DISCARD.md` 214-1。

- **本环停点（第 213 轮）**：环 15／`审-6`；缺口 **G-188b-2k** 的**尾段＋近零端＋零点存在三段已闭，唯一性只到条件句**。本轮把 $D=0$ 改写为 $Q=\lambda/R(\delta)=1$，证出「$Q$ 在 $[\frac1{10},1]$ 严格单增 ⇒ $D$ 恰一零点」（v38 条件 `def`；`Ring15LockZeroUnique`；A 闸三十八模块 PASS），并**否证**"$D'$ 左正右负分段"这一 212 停点入口（$D'$ 在区间内先增后减、$D''$ 变号两次，$D'$ 零点 $0.194$ 与 $D$ 零点 $0.3439$ 不同位置）。**新缺口 G-188b-2k-u**＝$Q$ 严格单增（$\lambda'R>\lambda R'\delta'$）；数值余量最小 $0.098536$（$T=1$），粗界不足。**最该修的一处＝$\delta'$ 的上界**（204 只有闭式与正性、无上界），配 $R'/R\le C/\delta$ 型界即可合成前件。依据＝卡 §四十六（四元组／路线否证／v38／B 闸逐问／残余）、`05_Lean验证/Ring15LockZeroUnique.lean`、`a_gate.ps1`（v38）、`04_计算验证/环15_唯一性可行性_输出.txt`。

- **入场禁行**：理论链未闭合（`审-6` 未闭合、闭合数 0），故第 5 层（对照/定稿）**不启动**；本轮数值只作约束与反馈。



## 六、外部候选审查（不并入链）



| 轮 | 对象 | 结论 | 去向 |

|:---|:---|:---|:---|

| 164 | "欧几里得张量几何"（`openai/math` family 379，七篇，2026-11-24；$\omega\le9/4$ 等）＋"相变以 P=NP 为前提"＋"质数振荡下 P=NP" | **不采纳**：ETG 的"张量"是计算对象（秩／渐近秩），链内"张量"是曲率—应变几何量，同名不同义；P=NP 未证且同批方向为代数复杂度分离；"趋势—危机／共产主义"属社会范畴，按 §1 第 5 问只能进【诠释】 | `08_框架扩展候选/FE10_欧几里得张量几何的迁移审查.md`；`DISCARD.md` 第 164 轮三行；**未动任何环与状态** |

| 165 | "用 ETG 计价原子化／离散／质数化／相变" | **仍不采纳，但承认同构母题**（两边都是"最小生成元计数"：$m_{\rm lock}$／$q_c$／素数标记 ↔ 秩）。三条接口各自断：A 量纲不可比、B 无共同几何不变量、C 质数化是空间压缩且非域运算 | FE10 §八（含翻案的三个入口）；`DISCARD.md` 第 165 轮；**未动任何环与状态** |

| 166 | 用户指出"原子化—配对—质数化"含配对中间环节 | **形态上最接近的一次**：配对算符确为双线性映射，与 ETG 同型。但四个计数口径（节点 $n$／对数 $n^2$／素数 $n$／乘法条数）互不同构；且秩对整体缩放 $\lambda$ 不变，与 $T_c\propto e^{-1/\lambda}$ 直接冲突 | FE10 §九；`DISCARD.md` 第 166 轮；**未动任何环与状态** |

| 167 | 用户授权立 FE11 做 $\lambda$ 扫描检验 | **检验完毕，否证**：秩侧 7 乘法残差 $1.646\times10^{-15}$（$\lambda\in[0.05,4]$），物理侧比值跨 8.2 个数量级 ⇒ 以秩为判据等价于"$T_c$ 与耦合无关" | FE11 卡＋`04_计算验证/FE11_*`；`DISCARD.md` 第 167 轮；**未动任何环与状态** |

| 168 | 把耦合缩放写成 $E_c\to\lambda E_c$ 接入环 15 参数化（不改方程） | **判定分层**：$y$ 层跨 $4.64$ 量级、$\partial\ln y/\partial\lambda=-10.69=-E_c/T_c$（硬否证）；$T_{\rm sync}$ 层仅 $1.233$ 倍（弹性 $0.17$，近饱和 $T_*$）⇒ 秩在此层"数值像"但语义不同（跑偏形态）；$T_c$ 层为标定输入未扫，不宣称 | `04_计算验证/FE11b_*`；FE11 卡 §九；`DISCARD.md` 第 168 轮；**未动任何环与状态** |

| 169 | 用户在原始主张上补：原子化（关系切断）→ 配对算符化（歌猜）→ 质数化，并称"符合 CFT 尺度不变"；同时自我修正为"P=NP 不普遍成立" | **两处记对**：拆分顺序与 13.A 一致；撤"成立"的方向对。**五处纠正**：A 三阶段是描述层不是尺度层（无 flow 参数）；B 链内真标度在 BKT 固定线与 $t$；C $t-1=m\ln(1-y)/\ln p$ 是 log 定义式（实测超量比恰 2.000）；D 歌猜是加性 $p+q=2n$、链内是乘性 $p_ip_j$；E P/NP 与相变区分无涉（区分靠 $\Upsilon$、$p_{\rm sync}>p_c$） | FE10 §十；`DISCARD.md` 第 169 轮三行；**未动任何环与状态** |

| 171 | 用户再精化："尺度不变是表现，标度无关是本质，耦合涨落—关系重组" | **两件可落地**：(1) 质数化不是无标度而是**对数标度**（$p_n\sim n\ln n$ ⇒ $\Theta(n\log n)$ 位），13.A 待加一行精度注记（主链未动）；(2) **关系重组无链内对应物**（无重连动力学，只有占据随 $T$ 变），缺可测量而非措辞。链内真"标度无关"落点仍是 BKT 固定线与 $t$ | FE10 §十一；`DISCARD.md` 第 171 轮两行；**未动任何环与状态** |

| 172 | 用户指出"U(1)–$Z_n$，耦合常数涨落就是关系重组的表现" | **四轮里最扎实**：涡旋解绑确实含在 $y=2\pi e^{-E_c/T}$ 的流里（$\beta_K=0.89294$），不需新机制。两处改口径：A 涨落（$\sigma_\theta^2=k_BT/\Upsilon_0$，含 $T$）≠ 流动（$\beta_K$，无量纲）；B 12.A 的 $Z_n$ 是绕数**标记**（$\Phi_n=nh/2e$）不是规范场。要成机制仍缺 $\mathrm{Var}[\Upsilon(x)]$ 与 $\xi_\Upsilon$（可由 $\lambda_L(x)$ 反演） | FE10 §十二；`DISCARD.md` 第 172 轮两行；**未动任何环与状态** |

| 180 | 按权威源定支：`00_当前有效口径表.md` §一（第 86 轮）维数定律 `m_eff^(d)=2n+(d-1)-s` 明写"按 3D 载体 d=3：m_eff=3、σ₀²∝Q⁴、S_ρ=1/6（精确）"，同表符号表（R49/R45）明写"3D j₀ 核、载体同维※2D J₀ 核 −0.0226 降为对照" ⇒ ρ 取 **j₀ + m_eff=3**；第 179 轮四支收成一支。另给两个相关的**闭式**：ρ₁=4(π²−4)/π⁴=0.241029018、ρ₂=−1/π²=−0.101321184（分部积分，与数值积分一致到 1e−9），ρ_XY=−0.274464、C_lock−1=3.5e−7、T_sync(m=2)=0.609828。连带订正 `审-4`：c̄=0.036306、δ=+0.030626、Δg/g≈+0.236%（原登记 0.030%–0.177%），符号仍正、幅度超原最大值 33% | `03_推导工作台/环15_审6_共点键相位相关与条件层误差量级.md` §十三；`05_Lean验证/audit_log_环15_2026-11-25.txt` §十二 | 无新引理（闭式属实数积分，未进 Lean，列下一轮候选）；a_gate 九模块重跑确认未退 | 审-6 仍未闭合：O(σ²) 非线性、2π 前因子、和乐映射层；载体 d 的"材料实现"仍是可测选择 |

| 182 | 锁条件换到 $\varepsilon$ 空间（闭合 179 轮遗留项 ③ 的**判据**部分）：$|\Delta\lambda|>1/(4\lvert s\rvert)\iff(1-\varepsilon_1/2\pi)/(1-\varepsilon_2/2\pi)>e^{1/(2\lvert s\rvert)}$；参考 $\varepsilon_1=0$ 给单侧门槛 $\varepsilon_2>2\pi(1-e^{-1/\lvert s\rvert})$（$\lvert s\rvert{=}1/2$ ⇒ $3.972$ rad，上端 $36.8\%$）。**同时撞出硬矛盾**：$\sigma_\varepsilon=\sigma_\theta/\lvert s\rvert$ 在 $\lvert s\rvert{=}1/2$ 给 $1.168$ rad（对应 $y=6.7\times10^{-4}$），而环 4 (4.1″) 登记 $\sigma_\varepsilon=0.18$–$0.54$ rad；用后者算 $z=7.36$–$22.07$ ⇒ $y\lesssim10^{-13}$，与 $y(T_c)=1.43\times10^{-4}$ 差 9 个量级；$\lvert s\rvert{=}1$／$2$ 给 $y=2.3\times10^{-5}$／$1.9\times10^{-6}$（线性化 $1.43\times10^{-4}$ 与 $s$ 无关）。⇒ $\varepsilon$ 的方差被赋值两次（环 4 的 $b\,n_d$ vs 环 15 的 $k_BT/\Upsilon_0$），B 闸判"只借符号没借语义" | Spec **v10**（`TargetPropLockRatio`）；`05_Lean验证/Ring15LockRatio.lean`（`lock_ratio` 一条）；卡 §十五 | A 闸十一模块（`a_gate.ps1`） | **停在本环**：缺的是 $\sigma_\varepsilon^2$ 的归属（$b\,n_d$ 与 $k_BT/\Upsilon_0$ 之间无已证等式），不是 $2\pi$ 常数；`审-6` 未闭合，闭合数仍 0 |



| 183 | 方差桥写成**恒等式**并形式化：由 v9 一阶系数 + $\alpha=-4\pi s$ 得 $\sigma_\theta=\lvert s\rvert\sigma_\varepsilon$（$\varepsilon_0=0$），故 $k_BT/(s^2\Upsilon_0)=b\,n_d\iff\Upsilon_0=k_BT/(s^2b\,n_d)$。据此把 161 的"$2\pi$ 前因子＝外部熵因子"**改判**为有限 $s$ 修正：$\Upsilon_0=2E_c/\pi^2=0.649917$、$\sigma_\theta^2=0.461598$，精确 $y(s)$ 为 $3.47e{-3}$／$2.74e{-4}$／$8.41e{-5}$／$4.29e{-5}$（$s=\tfrac12$／1／$\tfrac32$／2），$s\to\infty$ 给 $3.76e{-6}$；反解 $y_{\rm exp}=1.43e{-4}$ 得 $\lvert s\rvert^\*=1.2358$。第二条把手（环 4 的 $\sigma_\varepsilon\le0.54$）给 $T_c$ 时 $\lvert s\rvert\ge1.258$，两线交于 $\approx1.25$ ⇒ $\tfrac12\mathbb Z$ 中最小可行值为 $\lvert s\rvert=3/2$（$\sigma_\varepsilon=0.453$、$y=8.4e{-5}$，低 1.7 倍） | Spec **v11**（`epsVarFromTheta`／`TargetPropVarBridge`）；`05_Lean验证/Ring15LockBridge.lean`（`var_bridge`）；卡 §十六 | A 闸十二模块（`a_gate.ps1`，$\leftrightarrow$ 两方向均证） | `审-6` 仍未闭合：$b\,n_d(T)$ 的 $T$ 依赖**形状**缺、$s$ 仍属 `临-26`；$y_{\rm exp}$ 非独立实验值 |

| 185 | 15/`审-6` | **重开环 15：逸度 $T$ 依赖归刚度**。回读 (161.1)–(161.5) 判最早失配在 `(161.4)` **第二等号**：其前件 $\sigma^2(T)=\sigma_0^2[1+2n_B]$ 属 (4.1) 第一项，已被第 138 轮（$M=0$）撤销；且把 $\Upsilon$ 冻成 $\Upsilon_0$ 与 (15L.3)（$E_c=\frac{\pi^2}{2}\Upsilon$）＋(19W.8)（$\Upsilon=\Upsilon_0w\Phi$）冲突。修：$y$ 由 (15L.3) 给、$T$ 依赖全经 $w(T)$；(161.1) 第一等号降为恒等 $\sigma_\theta=s\sqrt{2(1-\rho)}\sigma_\varepsilon$；(161.5) 撤销、$\Upsilon_0$ 回外部。**推论**：$\Upsilon_0\ge0.442819$（否证 163 轮 KAP 支 $0.206875$，其 $y(T_c)=0.4752$ 越 (15L.5)）；$y(T_c)\in[1.8862e{-3},0.02501]$（旧 $1.43e{-4}$ 需 $\Phi>1$，越界）；$t(T_c)=1.01420/1.02841$；$T_{\rm sync}$ 由点变窗口 $[0.42603,0.50665]$（$m{=}1$）／$[0.38821,0.47071]$（$m{=}2$），$T_*=0.651929$；$y$ 小参数域止于 $T_{\rm break}=0.73044$ | Spec **v12**（删 `epsVarFromTheta`／`TargetPropVarBridge`，增 `fugOfK`／`TargetPropFugStiff`／`TargetPropFugBound`／`TargetPropUpsLower`）；`05_Lean验证/Ring15LockStiff.lean`（3 条）；卡 §十八 | A 闸十二模块（`a_gate.ps1` Bridge→Stiff），12/12 编译、20 条 axioms 白名单、15 条 `#check`、241 文件 0 命中、exit 0；B 闸：新版定义式／旧版跑偏式 | `审-6` 仍未闭合：残余=$b\,n_d(T_c)$ 材料量、$s\in\frac12\mathbb Z$、$\Phi$、$\Upsilon_0$（仅下界）、$T>T_{\rm break}$ 的 $p_{\rm lock}$ 写法 |

| 184 | 桥接之后的**统计来源**审计：拆出同名 $E_c$（环 4 的向错弹性能 $E_c^{\varepsilon}\sim\mu f^2b^3\ln(R/r_c)/[16\pi(1-\nu)]$ vs 环 15 的涡旋逸度能 $E_c^{v}=\pi^2\Upsilon_0/2=3.207211$）；更硬的是统计分岔——环 15 的 $\sigma_\theta^2=k_BT/\Upsilon_0$ 是**热**的（能量均分），环 4 的 $\sigma_\varepsilon^2=b\,n_d$ 已被 R-147 判为**非热**（缺陷布居），而桥要求二者同方差。热支数值（$s=3/2$）：$T=0.30/0.40/0.50$ 给 $\sigma_\varepsilon=0.540/0.760/1.388$、$y=9.7e{-4}/1.9e{-2}/0.199$，$T\to0.551\,\omega_D$ 时 $w(T)\to0$、$y\to0.84$ ⇒ $T_{\rm sync}$ 被压到 $0.45$–$0.50$；非热支则 (161.1) 的 $k_BT/\Upsilon_0$ 识别作废、$y$ 与 $\Upsilon_0$ 脱钩 | 卡 §十七；口径表 §一第 138 轮（R-147）与第 161 轮条 | 无新引理；B 闸判**跑偏式**，指向 `(161.1)` 的第二个等号（**该判定已被 185 轮取代**：更准的失配在 `(161.4)` 第二等号） | ~~`审-6` 停在本环~~ → 185 轮已收口为"外部窗口＋三项外部量" |

| 186 | 15/`审-6` | **粗粒化指数 $t$ 的方向与下界（$y\to t\to x_\ast\to\epsilon_\nu\to r$ 口径链首环）**：`TargetPropTEffMMono`（$y$ 通道：$p$ 固定、$m\ge1$ 时 $y$ 增 $\Rightarrow t$ 增）、`TargetPropTEffMGeOne`（$t\ge1$，等号仅 $y=0$），两条均定义式（`unfold tEffM`＋`Real.log_lt_log`／`Real.log_neg`／`div_pos_iff`／`Real.log_nonpos`／`neg_div_neg_eq`）。数值：$t(T)$ 在 $[T_c,T_{\rm break})$ 严格增，$t(T_c)=1.01420/1.02841$、$t(T_{\rm sync})=1.64063/1.88466$、$T=0.730$ 处 $14.12/27.24$。**撞出失配并撤销前卡 (15M.5)**：其前提 $y(T_{\rm sync})=y_{\rm crit}=0.025007$ 在 185 轮 y 律下为 $0.1847$（$7.4$ 倍），$t$ 在 $T=0.34299$（$m{=}1$）／$0.34506$（$m{=}2$）即越 $1.0509$／$1.1072$；$y$ 越 $y_{\rm crit}$ 于 $T=0.38607$。(15L.6) 仍是 $T_c$ 端点界。**交接表**（$\nu=8$）：$t(T_c)$ 给 $x_\ast=6.4487/6.4103$、$\epsilon_\nu=2.4004/2.3722$；$t(T_{\rm sync})$ 给 $5.2821/4.9990$、$1.5901/1.4102$；$r$ 相应上移 $1.012$／$1.024$（$T_c$）与 $1.528$／$1.723$（同步点），$\epsilon_\nu$ 单一 $t$ 口径终止 | Spec **v13**（增 `TargetPropTEffMMono`／`TargetPropTEffMGeOne`）；`05_Lean验证/Ring15LockT.lean`（2 条＋私有差商引理）；卡 §十九；`04_计算验证/环15粗粒化指数t_方向与下界.py` | A 闸**十三模块 PASS**（13/13 编译、22 条 axioms 白名单、17 条 `#check`、242 文件 0 命中、exit 0）；B 闸判**定义式**（最可能跑偏行：`div_pos_iff` 的 `Or.inr ⟨hnum, hlogp⟩`，符号全赖 $\ln p<0$） | `审-6` 仍未闭合：新增 **G-186**（$t$ 在 $T$ 上的严格增只有数值证据，$p_{\rm pair}$ 下降通道未进 Lean）＋"$t$ 在同步区无上界"；残余仍为 $b\,n_d(T_c)$、$s$、$\Phi$、$\Upsilon_0$ 下界、$T>T_{\rm break}$ 的 $p_{\rm lock}$ 写法 |

| 187 | 15/`审-6` | **口径链第二环（$t\to x_\ast$ 接口）：两条写法等价 + $y$ 的结构化天花板**。`TargetPropThrLog`：$0<p_c<1$、$0\le y<1$、$m\ge1$、$p_c<(1-y)^m$ $\Rightarrow$ $t(p_{\rm pair}^{\rm thr},y,m)=\ln p_c/\ln p_{\rm pair}^{\rm thr}$；`TargetPropThrRpow`：同前件 $\Rightarrow$ $p_c^{1/t}=p_{\rm pair}^{\rm thr}$。故下游 $x_\ast$ 只有一个值（不会两值）。侧条件 $p_c<(1-y)^m$ 即 $y<y_{\deg}=1-p_c^{1/m}$（$m{=}1$：$0.407254$、$m{=}2$：$0.230100$，对应 $T=0.58607/0.52594$），**是"阈值不超过 1"的概率语义**：越此界 $p_{\rm pair}^{\rm thr}>1$、$t<0$，同步不可能。数值：同步点两写法差 $3.3\times10^{-16}$（$p_{\rm pair}=p_c^{1/t}=p_{\rm pair}^{\rm thr}=0.7270404$，回代 $p_{\rm sync}=0.5927460$）；$T_c$ 处两写法不同值（$p_{\rm pair}=0.875539$ vs 阈值写法 $0.593866/0.594988$、$p_c^{1/t}=0.597104/0.601371$）⇒ "处处相等"为假，只同步点相等。$m{=}1$ 天花板 $1-p_c=0.407254$ 与外部损伤格点阈 $f_c\approx0.407$ 同值 | Spec **v14**（增 `pPairThr`／`TargetPropThrLog`／`TargetPropThrRpow`）；`05_Lean验证/Ring15LockThr.lean`（2 条＋私有 `log_pPairThr`）；卡 §二十；`04_计算验证/环15配对阈值与t两写法.py` | A 闸**十四模块 PASS**（14/14 编译、24 条 axioms 白名单、19 条 `#check`、243 文件 0 命中、exit 0）；B 闸判**定义式**（最可能跑偏行 `Real.log_pow (1-y) m`——Lean 对负底数也成立，靠前件 $0\le y<1$ 才能剔病态域） | `审-6` 仍未闭合：$x_\ast$ 数值未进 Lean（卡方尾反演属外部标准）、G-186 仍在、新增域上限 $y_{\deg}$；残余 $b\,n_d(T_c)$／$s$／$\Phi$／$\Upsilon_0$ 下界／$T>T_{\rm break}$ 的 $p_{\rm lock}$ 写法 |

| 188 | 15/`审-6` | **口径链第三环（$\epsilon_\nu\to r$ 的 r/s 结构）：反比结构 + 失效面判据**。先把登记式两个写法面钉成同一：`rOfW`（(21.1b) 形）与 R-155 的 $2\alpha_V/(3\epsilon_\nu|d\ln w/dT|)$ 在 $w>0$、$w'\ne0$ 上逐字同值。`TargetPropROfEps`：$0<\alpha_V$、$0<w$、$w'\ne0$、$0<\epsilon_1<\epsilon_2$ $\Rightarrow$ $r(\epsilon_2)<r(\epsilon_1)$（路线 `rOfW_eq` 化 $k/\epsilon$ → `div_pos` → `div_lt_div_iff₀` → `mul_lt_mul_of_pos_left`）；`TargetPropSFail`：$0<C$ $\Rightarrow$ $s>0\iff r<a\lambda$（`div_pos_iff` 拆两支，第二支由 $0<2$ 排除）。**数值显影（非数据对照）**：$r(T)/r(T_c)=[w/w_c][|w'_c|/|w'|][\epsilon_c/\epsilon]$；反比项给 $1.0120$／$1.528$／$1.723$（$T_c$ / 同步点 $m{=}1$ / $m{=}2$，$\nu{=}8$，与 186 表逐位一致）；形状项在 $T\approx0.3445$ 有极小 $0.98866$（-$1.13\%$，因 $|w'|$ 在 $T_c$ 附近降得比 $w$ 快）；合成后 $m{=}2$ 严格增（$1.00\to16.406$），$m{=}1$ 在 $T=0.30575$ 有 $4.03\times10^{-4}$ 凹陷、其后到 $9.220$ ⇒ "r 随 T 单调上移"为假，只有 $\epsilon$ 通道单调 | Spec **v15**（增 `rOfW`／`sOfLock`／`TargetPropROfEps`／`TargetPropSFail`）；`05_Lean验证/Ring15LockR.lean`（2 条＋私有 `rOfW_eq`）；卡 §二十一；`04_计算验证/环15锁定失效面r的epsilon反比结构.py` | A 闸**十五模块 PASS**（15/15 编译、26 条 axioms 白名单、21 条 `#check`、244 文件 0 命中、exit 0）；B 闸判**定义式**（最可能跑偏行 `rOfW_eq` 的 `field_simp`：若漏 $w'\ne0$ 或 $0<\epsilon$，$1/0=0$ 会让等式照样"成立"而失效面语义归零；次风险 `div_lt_div_iff₀` 的两条正性缺一即翻号） | `审-6` 仍未闭合：新增 **G-188**（$r(T)$ 整体单调数值为假，$w/|w'|$ 形状项在 $T_c$ 邻域反向）；"高温 $r\propto T$"加边界（前提 $t$ 有界，$T\to T_{\rm break}$ 时 $1/\epsilon_\nu$ 发散主导，$r/r_c$ 到 $7.19$ 仍上冲）；残余 $b\,n_d(T_c)$／$s$／$\Phi$／$\Upsilon_0$ 下界／$T>T_{\rm break}$ 的 $p_{\rm lock}$ 写法／G-186 |

| 189 | 15/`审-6` | **$\Phi$ 的授权域：逸度窗口塌缩 + 15／19 两层同名判定**。185 让 $\Phi$ 进 (15L.3)，$y(T_c)$ 成窗口 $[1.8862\times10^{-3},0.02501]$、$\Phi\in[0.68135,1]$。本轮接上 19 层钉住：由 (154.1)/(154.2) 与 (19W.1)（$T\to0$ 时 $w=1$、$\Phi(1)=1$ ⇒ $\Upsilon_0=\Upsilon_{\rm bond}$）得 $\Phi_{\rm BKT}=2T_c/(\pi\Upsilon_0w_c)$；而 (15L.5) 反解给闭式 $\Phi_{\min}=\frac{2T}{\pi^2\Upsilon_0w}\ln\frac{2\pi}{y_{\rm crit}}$，且 $y(\Phi_{\min})=y_{\rm crit}$ 为**恒等**（`TargetPropPhiMinEq`）。二者之比 $\Phi_{\rm BKT}/\Phi_{\min}=\pi/\ln(2\pi/y_{\rm crit})=2\beta_{\rm KT}/\pi=K_{\rm BKT}=0.5684633$，**与 $T_c,\Upsilon_0,w$ 全无关** ⇒ 判据 $\beta_{\rm KT}<\pi/2\iff y_{\rm crit}<y_R=2\pi e^{-\pi}$（`TargetPropPhiConflict`）：只要 (15L.5) 比临界逸度更紧（紧 $10.86$ 倍），"$\Phi$ 进逸度＋BKT 钉住"必然违反 (15L.5)（`TargetPropPhiBktVal` 给 $\Phi=\Phi_{\rm BKT}$ 时 $y=2\pi e^{-\pi}$，与参数无关）。**判定**：$\Phi$ 不进 (15L.3)；(15L.3) 的 $\Upsilon$ 是 bare（149③/150② 的授权文本 $E_c^{\rm eff}=\frac{\pi^2}{2}\Upsilon_0w$ 无 $\Phi$），(19W.8) 的 $\Upsilon$ 是 effective（相界/BKT 用）——同名不同义。**撤销**：185 (ii) 的 $\Phi$ 窗口塌成点（$y(T_c)=1.8862\times10^{-3}$、$T_{\rm sync}=0.50665/0.47071$，正是窗口的 $\Phi=1$ 端点）；185 撤销 (161.4) 的**第二条理由**（"与 (19W.8) 冲突"）撤销，判决本身（$w$ 通道）保持。186–188 的数值全在 $\Phi=1$ 端点，**不受影响** | Spec **v16**（增 `phiBkt`／`phiMin`／`TargetPropPhiMono`／`TargetPropPhiBktVal`／`TargetPropPhiMinEq`／`TargetPropPhiConflict`）；`05_Lean验证/Ring15LockPhi.lean`（4 条＋私有 `bkt_K`）；卡 §二十二；`04_计算验证/环15锁定概率_Φ授权域与BKT钉住冲突.py` | A 闸**十六模块 PASS**（16/16 编译、30 条 axioms 白名单、25 条 `#check`、245 文件 0 命中、exit 0）；B 闸判**定义式**（最可能跑偏行 `Real.log_inv`＋`Real.exp_log`：$e^{-\log q}=1/q$ 需 $0<y_{\rm crit}$，漏则 Lean 取 $\log|q|$ 等式照样成立而概率语义归零） | `审-6` 仍未闭合：$\Phi_c$ 数值仍外生（$t_\Upsilon$／$\kappa$ 材料值）；新增 **G-189**（判据依赖 (15L.5) 与 (19P.24) 两条 A 类）；残余 $b\,n_d(T_c)$／$s$／$\Upsilon_0$ 下界／$T>T_{\rm break}$ 的写法／G-186／G-188 |

| 190 | 15/`审-6` | **$w(T)$ 的积分定义授权：正性、单调不增、上界 1**。把环 19 的 $w(T)=2\int_0^1u\tanh\frac{u}{2T}du$ 钉进 Spec：`wGap T := ∫ u in 0..1, 2*u*tanh(u/(2*T))`。三条定理：`TargetPropWGapPos`（$0<T\Rightarrow0<w$，`integral_pos` 取 $u=1$ 见证点）；`TargetPropWGapAnti`（$0<T_1\le T_2\Rightarrow w(T_2)\le w(T_1)$，逐点 $x/(2T_2)\le x/(2T_1)$ ⇒ `tanh_le_tanh` ⇒ `mul_le_mul_of_nonneg_left` ⇒ `integral_mono_on`）；`TargetPropWGapLeOne`（$0<T\Rightarrow w\le1$，integrand $\le2u$ ⇒ $\int_0^12u=1$）。底层私有：`continuous_tanh`、`hasDerivAt_tanh`（$\tanh'=1/\cosh^2$，商法则＋$\cosh^2-\sinh^2=1$）、`tanh_strictMono`（`strictMono_of_deriv_pos`）。**意义**：186（$t$ 方向）、187（$y$ 天花板）、188（$r$ 分母）三处对 $w$ 的消费从数值升为已证；温度只经辐角 $u/(2T)$ 进入，故"$w$ 随 $T$ 减"是占据差被抹平的逐点形式，不是拟合 | Spec **v17**（增 `wGap`／`TargetPropWGapPos`／`TargetPropWGapAnti`／`TargetPropWGapLeOne`＋两条基线 import）；`05_Lean验证/Ring15LockW.lean`（3 条＋4 个私有引理）；卡 §二十三；`04_计算验证/环15_w结构_单调与上界.py` | A 闸**十七模块 PASS**（17/17 编译、33 条 axioms 白名单、31 条 `#check`、246 文件 0 命中、exit 0）；B 闸判**定义式**（最可能跑偏行 `hasDerivAt_tanh` 的 `field_simp`＋`nlinarith [Real.cosh_sq x]`：$\cosh x\ne0$ 由 `Real.cosh_pos` 保证，漏之则在总除法下等式仍"成立"而导数符号翻） | `审-6` 仍未闭合：新增 **G-190a**（`wGap 0 = 0`，链内 $w(0)=1$ 只能作 $T\downarrow0$ 极限，数值给 $1-w\approx3.29T^2$）、**G-190b**（严格单调未证，数值最小降幅 $4.67\times10^{-4}$）、**G-190c**（$w'=-T^{-2}\int u^2\mathrm{sech}^2$ 未进 Lean，188 形状项仍只数值）；残余 $b\,n_d(T_c)$／$s$／$\Upsilon_0$ 下界／$T>T_{\rm break}$ 写法／G-186／G-188／G-189 |



| 191 | 15/`审-6` | **$s$ 的同名判否：可解性因子不是半整数格点**。`审-6` 残余里挂着的"$s\in\frac12\mathbb Z$、仅下界 $\ge3/2$"被拆开：环 6／G19 的 $s_{\rm rep}$ 是**表示权**（$\theta=s\ell$、$\alpha=-4\pi s$、$\sigma_\varepsilon=\sigma_\theta/|s|$，值落 $\frac12\mathbb Z$，A4 整格再收成 $\mathbb Z$）；R155.1 的 $s_{\rm sol}=2g/[C(g a\lambda+2\mu)]=2/[C(a\lambda-r)]$ 是**可解性因子**（连续实值、可正可负）。`TargetPropSolSurj`：$\forall y>0$，取 $C=1$、$r=0$、$a\lambda=2/y$ 即 $s_{\rm sol}=y$ ⇒ 值域是整条 $(0,\infty)$，任何格点都容不下它；`TargetPropSolNeg`：$C=1,a\lambda=0,r=1$ 给 $s_{\rm sol}=-2<0$。**判定**：同名不同义；§16.3 的"$|s|=3/2$ 是 $\frac12\mathbb Z$ 最小可行值"只对 $s_{\rm rep}$ 成立，不能当失效面因子的取值。**改挂**：$s_{\rm sol}$ 归乙类（$C$ 材料量，不入缺口表）；$s_{\rm rep}$ 的选档缺口迁至环 26／`临-26` | Spec **v18**（增 `TargetPropSolSurj`／`TargetPropSolNeg`）；`05_Lean验证/Ring15LockS.lean`（2 条，只 import Spec）；卡 §二十四 | A 闸**十八模块 PASS**（18/18 编译、35 条 axioms 白名单、33 条 `#check`、247 文件 0 命中、exit 0）；B 闸判**定义式**（最可能跑偏行 `targetPropSolSurj` 的 `field_simp`：漏 $y\ne0$ 时等式仍可成立，但值域论证退化） | `审-6` 仍未闭合；甲类残余收窄为 $T>T_{\rm break}$ 的 $p_{\rm lock}$ 写法、G-186、G-188、G-189、G-190b、G-190c；$b\,n_d(T_c)$、$\Upsilon_0$ 归乙类；$s_{\rm rep}$ 迁环 26 |



| 192 | 15/`审-6` | **$w$ 的严格单调（G-190b 收口）**。190 轮只到"不增"，严格性留在数值层（网格最小降幅 $4.67\times10^{-4}$）。本轮补上 `TargetPropWGapStrictAnti`（$0<T_1<T_2\Rightarrow w(T_2)<w(T_1)$）：路线是"先 $\le$ 再判差分为正"——`integral_mono_on` 由逐点 $g\le f$（`div_le_div_of_nonneg_left`＋`tanh_strictMono.monotone`＋`mul_le_mul_of_nonneg_left`）给 $\int g\le\int f$；`intervalIntegral.integral_pos` 判 $\int(f-g)>0$（连续性、$[0,1]$ 上非负、见证点取 $u=1$ 处 $1/(2T_2)<1/(2T_1)$ 经 `tanh_strictMono`＋`mul_lt_mul_of_pos_left`）；`integral_sub` 给 $\int(f-g)=\int f-\int g$，`linarith` 收口（`simp only [sub_eq_add_neg] at hpos hsub ⊢` 先把三处减法归一，否则原子对不齐）。**意义**：186 依赖的方向从此可读成严格方向，G-186 由"仅数值"降为"待复合"；不是新物理，是把 190 的定义授权补成严格形式 | Spec **v19**（增 `TargetPropWGapStrictAnti`）；`05_Lean验证/Ring15LockWStr.lean`（1 条＋复用 190 的 4 个私有引理，只 import Spec）；卡 §二十五 | A 闸**十九模块 PASS**（19/19 编译、36 条 axioms 白名单、34 条 `#check`、exit 0）；B 闸判**定义式**（最可能跑偏行：`integral_pos` 的见证点若取 $u=0$，$f(0)-g(0)=0$ 会让严格性退化成非严格） | `审-6` 仍未闭合；G-190b 收口，G-186 待复合；甲类残余＝$T>T_{\rm break}$ 的 $p_{\rm lock}$ 写法、G-186、G-188、G-189、G-190a、G-190c；$b\,n_d(T_c)$、$\Upsilon_0$ 仍乙类 |



| 193 | 15/`审-6` | **$w$ 的严格减沿 $T\to K\to y\to t$ 传下去（G-186 通道严格化）**。192 只补了链的第一环，本轮把后面三处接起来。①`TargetPropKStrictAnti`：$0<T_1<T_2$ 且 $0<w(T_1)$ ⇒ $\Upsilon_0w(T_2)/T_2<\Upsilon_0w(T_1)/T_1$（分子变小 `div_lt_div_of_pos_right`＋分母变大 `div_lt_div_of_pos_left`，两步严格传递后乘 $\Upsilon_0>0$；`calc` 用 `ring` 把 $(\Upsilon_0w)/T$ 与 $\Upsilon_0(w/T)$ 对齐）。②`TargetPropYStrictMono`：$y$ 作为 $T$ 的函数**严格增**（$K$ 严格减 ⇒ $e^{-\pi^2K/2}$ 严格减 `Real.exp_lt_exp`），新增显式定义 `yOfT ups0 T := fugOfK (ups0*wGap T/T)`（把 185 的 $y$ 律从文字升为定义）。③`TargetPropTStrictMono`：$p$ 固定、$y(T_1)<1$、$y(T_2)<1$ ⇒ $t(T_1)<t(T_2)$（与 186 同形的差商 `tEffM_sub`＋`Real.log_lt_log`＋`div_pos_iff`）。**方向注**：$y$ 随 $T$ 增不是笔误——$K$ 里 $w$ 降而 $T$ 升，两者同向压 $K$；与 185 数值一致（$y(T_c)=1.8862\times10^{-3}$、$T=0.38607$ 越过 $y_{\rm crit}$）。**写法坑**：`TargetPropKStrictAnti` 是 `def…:Prop`，套用须命名参数 `(ups0:=…) (T1:=…) (T2:=…)`，否则首参被当 `ups0:ℝ` | Spec **v20**（增 `yOfT`／`TargetPropKStrictAnti`／`TargetPropYStrictMono`／`TargetPropTStrictMono`）；`05_Lean验证/Ring15LockTStrict.lean`（3 条＋私有的 $w$ 严格性重证与 `fugOfK_strictAnti`／`fugOfK_pos`／`tEffM_sub`）；卡 §二十六；外部锚 Nelson–Kosterlitz 1977（PRL 39, 1201）只作边界；数值旁证 `04_计算验证/环15_w严格性沿链传递_旁证.py|.json`（网格三环方向全 true，$K(T_c)=1.643650$、$y(T_c)=1.886162\times10^{-3}$、$t(T_c)=1.014204$） | A 闸**二十模块 PASS**（20/20 编译、39 条 axioms 白名单、37 条 `#check`、249 文件 0 命中、exit 0）；B 闸判**定义式**（最可能跑偏行①的 `calc`＋`ring`：若把除法当乘法逆元而对 $T\ne0$ 无感，等式在总除法下仍成立但"分母变大"的链语义丢失） | `审-6` 仍未闭合；G-186 的 $w\to K\to y\to t$ 通道**收口**，新增 **G-186p**（$p_{\rm pair}(T)$ 通道，$F_\nu$ 链内无定义授权）；甲类残余＝$T>T_{\rm break}$ 的 $p_{\rm lock}$ 写法、G-186p、G-188、G-189、G-190a、G-190c |

| 194 | 15/`审-6` | **$p_{\rm pair}$ 通道的方向与两通道反号（G-186p 形态判定；纠正 193 口径）**。原文检索钉住 $p_{\rm pair}$ 权威式 $p_{\rm pair}(T)=1-F_{\chi^2_{n_{\rm cell}}}(n_{\rm cell}\sigma_c^2/(Zw(T)))$（`README.md:115`、`文献基线:156`）：$w$ 降 ⇒ 自变量升 ⇒ CDF 升 ⇒ $p_{\rm pair}$ **降**（与 `README.md:120` 的低温展开 $p_0-C(T/\omega_D)^2$ 同号）。①`TargetPropTEffMPMono`：$0<p_2<p_1<1$、$y\in(0,1)$、$m\ge1$ ⇒ $t(p_2,y,m)<t(p_1,y,m)$（差商 `tEffM_diff_p`；$\ln(1-y)<0$、$\ln p_2-\ln p_1<0$、分母 $>0$ ⇒ 差 $>0$）；②`TargetPropTChanSplit`：$\Delta t=\frac{m}{N}[(\ln(1-y_2)-\ln(1-y_1))\ln p_1+\ln(1-y_1)(\ln p_1-\ln p_2)]$ 且首项 $>0$（$y$ 通道抬 $t$）、次项 $<0$（$p$ 通道压 $t$）。**判定**：两通道**反号**，故 193 轮"等 $F_\nu$ 授权即可复合"**作废**，$t$ 随 $T$ 严格增的净方向须主导项比较 ⇒ 新增 **G-186c**（甲类）；G-186p 的方向已收口，余 $\chi^2$ 尾函数的链内定义授权归乙类。数值旁证（$m{=}1$，$T_c\to T_{\rm sync}=0.50665$）：$y$ 通道项全程 $>0$、$p$ 通道项全程 $<0$，$|p|/y$ 比值 $0.114$–$0.283$、均值 $0.201$ ⇒ $t$ 由 $1.014204$ 升到 $1.640631$，增量 $0.626427$；$p_c$ 口径（$p$ 常数）下该比值消失，方向会判错 | Spec **v21**（增 `TargetPropTEffMPMono`／`TargetPropTChanSplit`）；`05_Lean验证/Ring15LockTChan.lean`（2 条＋私有 `tEffM_diff_p`／`tEffM_split`）；卡 §二十七；`04_计算验证/环15_t两通道反号_旁证.py|.json|.png` | A 闸**二十一模块 PASS**（21/21 编译、41 条 axioms 白名单、39 条 `#check`、250 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 二十一模块 v21）`）；B 闸判**定义式**（最可能跑偏行：②的 `ring` 收口——恒等式对任何符号都成立，故把 $\delta_1>0$、$\delta_2<0$ 作为合取项写进 Spec 逼 Lean 分证，防抵消） | `审-6` 仍未闭合；G-186p 方向收口（余乙类）、新增 **G-186c**（主导项闸，195 立条件式）；甲类残余＝$T>T_{\rm break}$ 的 $p_{\rm lock}$ 写法、G-186c、G-188、G-189、G-190a、G-190c |

| 195 | 15/`审-6` | **G-186c 的条件式主导项闸与充要判据**。194 只把两通道拆成反号两项，"$t$ 随 $T$ 严格增"要什么条件没说清，本轮把它写成可消费的条件式。①`TargetPropTChanDominate`：$0<p_2<p_1<1$、$0<y_1<y_2<1$、$m\ge1$、$\delta_1+\delta_2>0$ ⇒ $t(p_1,y_1,m)<t(p_2,y_2,m)$（$\Delta t=m(\delta_1+\delta_2)/N$，$m>0$、$N>0$）。②`TargetPropTChanCriterion`：同一前件下 $\Delta t>0\iff\delta_1+\delta_2>0$（正向 `div_pos_iff` 拆两支、第二支 $N<0$ 与前件 $N>0$ 对撞；反向 `mul_pos`＋`div_pos`）。**判定**：复合符号只由一条标量不等式 $S:=\delta_1+\delta_2>0$ 决定，任一通道单独不定；不能无条件化的原因是 $p_{\rm pair}$ 形状来自外部 χ² 尾（乙类），链内只有"$w$ 严格减、$p$ 严格降"，给不出 $\rho:=|\delta_2|/\delta_1<1$ 的界。数值旁证（$[T_c,T_{\rm break})$ 401 点，$T_{\rm end}=0.729439$）：$\rho\in[0.018878,0.309125]$（最大在 $T=0.583430$），判据全程成立；$t$ 由 $1.014204$ 升到 $9.205335$（$m{=}1$）／$17.410670$（$m{=}2$），$\rho$ 与 $m$ 无关 | Spec **v22**（增 `TargetPropTChanDominate`／`TargetPropTChanCriterion`）；`05_Lean验证/Ring15LockTDom.lean`（2 条＋私有 `tEffM_split`／`one_le_nat_cast_pos`）；卡 §二十八；`04_计算验证/环15_t主导项闸_旁证.py|.json|.png` | A 闸**二十二模块 PASS**（22/22 编译、43 条 axioms 白名单、41 条 `#check`、251 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 二十二模块 v22）`）；B 闸判**定义式**（最可能跑偏行：`TargetPropTChanCriterion` 反向分支——`div_pos_iff` 的第二支若直接丢弃，就证出"$\Delta t>0\Rightarrow S>0$"的假版本；本轮用 `not_lt.mpr (le_of_lt hN)` 显式排掉） | `审-6` 仍未闭合；G-186c **判据部分收口**（余 $\rho<1$ 的域核属反馈层）；G-186p 方向收口（余乙类）；甲类残余＝$T>T_{\rm break}$ 的 $p_{\rm lock}$ 写法、G-186c 的域核、G-188、G-189、G-190a、G-190c |

| 196 | 15/`审-6` | **$w$ 的导数表示（G-190c 收口）**。190 只钉住 $w$ 的定义与三条单调性，$w'$ 本身从未进链，188 的 $w/\|w'\|$ 因此卡在数值层。①`TargetPropWGapDeriv`：$\forall T>0$，$\mathrm{HasDerivAt}\ wGap\ (wGapDeriv\,T)\ T$，其中 `wGapDeriv T = -(1/T^2)∫_0^1 u^2 sech^2(u/2T) du`——用 Mathlib 参数积分求导引理（`hasDerivAt_integral_of_dominated_loc_of_deriv_le`），邻域取 $s=(T/2,2T)$，控制函数 $\frac{4}{T^2}t^2$（$x>T/2\Rightarrow1/x^2<4/T^2$、$\mathrm{sech}^2\le1$），逐点导数由 $\tanh'=1/\cosh^2$（自证）＋`hasDerivAt_inv`＋复合得到，$-(1/T^2)$ 用 `integral_const_mul` 提出后 `simpa [wGap]` 收口（定义逐字对齐）。②`TargetPropWGapDerivNeg`：$w'<0$ 由 `integral_pos`（见证点 $u=\frac12$）单独证——不借范数论证，防"范数吃掉负号"。**判定**：G-190c 收口，$|w'|=-w'$ 可直接取用；但 `wGapDeriv` 的**数值大小**与 $r$ 的单调形状无关，188 仍须另立形状判据 | Spec **v23**（增 `sechSq`／`wGapDeriv`／`TargetPropWGapDeriv`／`TargetPropWGapDerivNeg`）；`05_Lean验证/Ring15LockWD.lean`（2 条＋私有 `continuous_tanh`／`hasDerivAt_tanh'`／`deriv_F`／`sechSq_pos`／`sechSq_le_one`）；卡 §二十九；`04_计算验证/环15_w导数表示_旁证.py\|.json\|.png` | A 闸**二十三模块 PASS**（23/23 编译、45 条 axioms 白名单、43 条 `#check`、252 文件 0 命中，exit 0，末行 `A 闸 PASS（限环 15 二十三模块 v23）`）；B 闸判**定义式**（最可能跑偏行：`show ‖-(t^2/x^2)*sechSq(t/(2x))‖ ≤ 4/T^2*t^2`——该不等式对 $\pm F'$ 同真，方向语义被范数吞掉，故符号另立命题） | `审-6` 仍未闭合；**G-190c 收口**（移入丙类）；甲类残余＝$T>T_{\rm break}$ 的 $p_{\rm lock}$ 写法、G-186c 的域核、G-188、G-189、G-190a；数值旁证 $w'$ 中心差分与积分式相对偏差 $\le2.6\times10^{-10}$ |

| 197 | 15/`审-6` | **$w$ 的分部积分恒等式与形状项分解（G-188a 收口）**。196 给了 $w'$，但形状项仍是"两数相处"，无分解、无判据。本轮用核的原函数 $\frac{u^2}{2}\tanh\frac{u}{2T}$＋FTC 得 ①`TargetPropWGapIbp`：$w(T)=\tanh\frac{1}{2T}+\frac T2w'(T)$（$\int_0^1u\tanh=\frac w2$、$\int_0^1u^2\mathrm{sech}^2=-T^2w'$ 代入整理）；②`TargetPropShapeSplit`：$\dfrac{w}{|w'|}=\dfrac{\tanh\frac{1}{2T}}{|w'|}-\dfrac T2$；③`TargetPropShapeEnd`：$\frac T2|w'|=\tanh\frac{1}{2T}-w$；④`TargetPropShapeEndGt`：$\tanh\frac{1}{2T}>w$。**判定**：形状项不是独立对象，其 $T$ 依赖只剩端点半温 $\tanh\frac{1}{2T}$ 与导数模 $|w'|$ 两条通道＋$\frac T2$ 平移；凹陷源于二者同向衰减的竞争，但**极小值位置仍属数值显影**。据此 G-188 拆为 **a（收口）** 与 **b（$w''$ 与极小编址）** | Spec **v24**（增四命题）；`05_Lean验证/Ring15LockIbp.lean`（4 条＋私有 `hasDerivAt_tanh'`／`cont_A`／`cont_B`）；卡 §三十；`04_计算验证/环15_w分部积分恒等式_旁证.py\|.json\|.png` | A 闸**二十四模块 PASS**（24/24 编译、49 条 axioms、47 条 `#check`、254 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 二十四模块 v24）`）；B 闸判**定义式**（最可能跑偏行 `rw [habs, hibp]`——`|w'|=-w'` 若反号，$\tanh-w=\frac T2w'<0$ 与端点正性矛盾而等式仍成立，故另立 `TargetPropShapeEndGt`） | `审-6` 仍未闭合；**G-188a 收口**（移入丙类）、**新拆 G-188b**；甲类残余＝$T>T_{\rm break}$ 的 $p_{\rm lock}$ 写法、G-186c 域核、G-188b、G-189、G-190a；数值旁证恒等式残差 $\le5.50\times10^{-10}$、端点亏损全程为正（最大 $0.200046$）、形状项极小 $0.652621$ 于 $T=0.343044$ |

| 198 | 15/`审-6` | **$w''$ 的链内表示与形状项导数（G-188b 第一步）**。197 把形状项化成"端点商减半温"，其导数仍无处落。本轮建二阶结构：①`TargetPropWGapDeriv2`：$\forall T>0$，`HasDerivAt wGapDeriv (wGapDeriv2 T) T`，`wGapDeriv2 T = -(2/T)·wGapDeriv T - (1/T^4)∫_0^1u^3\mathrm{sech}^2\frac{u}{2T}\tanh\frac{u}{2T}du`（对 $B(T)=\int u^2\mathrm{sech}^2$ 用参数积分求导引理得 $B'=T^{-2}\int u^3\mathrm{sech}^2\tanh$，再叠商法则端点项）；②`TargetPropShapeDeriv`：$\forall T>0$，`HasDerivAt (fun T => wGap T/|wGapDeriv T|) (shapeDeriv T) T`，`shapeDeriv T=(w\,w''-(w')^2)/(w')^2`（在 $(0,2T)$ 上 `abs_of_neg` 把 $|w'|$ 换 $-w'$，再 `HasDerivAt.div`）。**判定**：结构层闭合（形状项导数不再依赖外部输入），但 $w''>0$ 与 $S'$ 分段符号**未证**——两项符号相反（$-\frac2Tw'>0$、$-\frac{1}{T^4}\int u^3\mathrm{sech}^2\tanh<0$），和式符号不由单项决定，判据须比较 $w\,w''$ 与 $(w')^2$，粗界不可比，故留第二步 | Spec **v25**（增 `wGapDeriv2`／`shapeDeriv`／`TargetPropWGapDeriv2`／`TargetPropShapeDeriv`）；`05_Lean验证/Ring15LockWD2.lean`（2 条＋私有 `deriv_F`（$t^3/x^2$ 形）／`cont_F`／`cont_F'`／`tanh_pos_of_pos`）；卡 §三十一；`04_计算验证/环15_w二阶导与形状项导数_旁证.py\|.json\|.png` | A 闸**二十五模块 PASS**（25/25 编译、51 条 axioms 白名单、46 条 `#check`、257 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 二十五模块 v25）`）；B 闸判**定义式**（最可能跑偏行：`hval` 里 `unfold wGapDeriv2; field_simp`——若 `hBval` 的 $-T^2$ 因子记错，field_simp 仍能凑出"像样"的式子，故令 `hBval` 由定义 `field_simp` 自证、符号由定义强制） | `审-6` 仍未闭合；G-188b **第一步完成、未收口**；甲类残余＝$T>T_{\rm break}$ 的 $p_{\rm lock}$ 写法、G-186c 域核、G-188b 第二步（$w''>0$／$S'$ 符号）、G-189、G-190a；数值旁证 $w''$ 相对偏差 $\le4.02\times10^{-7}$、$S'$ $\le2.06\times10^{-5}$、$w''>0$ 61/61、$S'$ 单次变号于 $[0.343711,0.343927]$、极小 $T=0.343858$／$S=0.6526189$ |

| 199 | 15/`审-6` | **$w''$ 的端点闭式与条件式符号判据（G-188b-2）**。v25 的 $w''$ 依赖 $\int u^3\mathrm{sech}^2\tanh$，符号无法判。本轮对 197 的恒等式 $w=\tanh\frac{1}{2T}+\frac{T}{2}w'$ 逐项求导，得**第二闭式** ①`TargetPropWGapDeriv2Alt`：`wGapDeriv2 T = wGapDeriv2Alt T`，其中 `wGapDeriv2Alt T = wGapDeriv T/T + sechSq(1/(2T))/T^3`——$u^3$ 积分被整个消掉；②`TargetPropWGapDeriv2Pos`：$T^2|w'|<\mathrm{sech}^2\frac{1}{2T}\Rightarrow w''>0$（`lt_div_iff₀` 化为 $T^2w'+\mathrm{sech}^2>0$，再用 $w'=-|w'|$）；③`TargetPropShapeDerivSign`：$S'<0\iff w\,w''<(w')^2$（`div_lt_iff₀`，分母 $(w')^2>0$）。**判定**：判据层闭合；**无条件凸性不成立**——数值比 $r=T^2|w'|/\mathrm{sech}^2$ 仅在 $T\ge0.256$ 小于 1，$T=0.1/0.2/0.25$ 处 $w''=-6.38/-2.26/-0.18$，故 198 的"$w''>0$"只能是条件式，本轮据此改口径 | Spec **v26**（增 `wGapDeriv2Alt`／`TargetPropWGapDeriv2Alt`／`TargetPropWGapDeriv2Pos`／`TargetPropShapeDerivSign`）；`05_Lean验证/Ring15LockWD3.lean`（3 条＋私有 `hasDerivAt_tanh_inv`）；卡 §三十二；`04_计算验证/环15_w二阶导端点闭式_旁证.py|.json|.png` | A 闸**二十六模块 PASS**（26/26 编译、54 条 axioms、49 条 `#check`、256 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 二十六模块 v26）`）；B 闸判**定义式**（最可能跑偏行：`hwabs` 的 $|w'|=-w'$ 若在 $|\cdot|$ 内部重写会得 $|-|w'||$，改用 `congrArg` 避坑；导数同值由 v25 已锁命题经 `unique` 强制） | `审-6` 仍未闭合；G-188b 余 b-2（$S'$ 符号的分段判据与极小 $T_{\min}$ 编址）；甲类残余＝$T>T_{\rm break}$ 的 $p_{\rm lock}$ 写法、G-186c 域核、G-188b-2、G-189、G-190a；数值旁证端点闭式 vs 积分式 $\le2.18\times10^{-8}$、判据比 $T_c$ 0.7776／$T_{\rm break}$ 0.3973 |

| 200 | 15/`审-6` | **形状比与判据比——$S'$ 符号的比值判据（G-188b-2 第二步）**。199 的判据是"$w\,w''$ 与 $(w')^2$ 相乘比较"，两项各有符号，无法再分。本轮把整块化成一个无量纲差：①新增 `shapePhi T := wGap T/tanh(1/(2*T))`、`ratioR T := T²|wGapDeriv T|/sechSq(1/(2T))`；②`TargetPropShapeSignRatio`：$S'<0\iff\Phi(1+r)<2r$（由私有恒等式 $w\,w''-(w')^2=\tanh\frac{1}{2T}\mathrm{sech}^2\frac{1}{2T}[\Phi(1+r)-2r]/T^3$ 与 v26 的 `TargetPropShapeDerivSign` 合成）；③`TargetPropShapeNegOfRatioGeOne`：$1\le r\Rightarrow S'<0$——$r\ge1$ 恰是 $w''\le0$，故"$w''\le0$ 段形状项必降"为无条件命题。推导只消费 197 的端点亏损 $Ta=2\tanh(1-\Phi)$ 与 $r$ 的定义，不引新假设、不预埋可调项 | Spec **v27**（增 `shapePhi`／`ratioR`／`TargetPropShapeSignRatio`／`TargetPropShapeNegOfRatioGeOne`）；`05_Lean验证/Ring15LockWD4.lean`（2 条＋私有 `tanhPos`／`sechSqPos`／`wSub`）；卡 §三十三；`04_计算验证/环15_形状比与判据比_旁证.py|.json|.png` | A 闸**二十七模块 PASS**（27/27 编译、56 条 axioms、51 条 `#check`、256 文件 0 命中，末行 `A 闸 PASS（限环 15 二十七模块 v27）`）；B 闸判**定义式**（最可能跑偏行：`wSub` 里 `set a := |w'|` 后 `field_simp` 会展开 $a$、把头 `r` 定义式换成数值恒等式；本轮以 `div_mul_cancel₀` 显式给 $rS=T^2a$，并在 `rw [← ha]` 后补一次 `rw [haT]`，使 $a$ 不残留） | `审-6` 仍未闭合；G-188b-2 **判据层闭合、分段只解一半**（$r\ge1$ 段已证 $S'<0$；$r<1$ 段与 $T>0.3438$ 的 $S'>0$ 仍只有判据）；甲类残余＝$T>T_{\rm break}$ 的 $p_{\rm lock}$ 写法、G-186c 域核、G-188b-2（$r$ 的上下夹逼与 $\Phi$ 单调性）、G-189、G-190a；数值旁证恒等式残差 $\le5.12\times10^{-9}$、判据与 $S'$ 同号 0 处不符、$r$ 最小 $0.356680$、$r\ge1$ 段 43 点全负 |

| 201 | 15/`审-6` | **$r$ 的 $\Phi$ 闭式与判据一元化（G-188b-2f）**。200 判"下一步要 $r$ 的上下夹逼"，可 $r$ 的分子是积分、分母是端点核值，夹逼最难。本轮发现 $r$ **不是独立自由度**：端点亏损 $T|w'|=2h(1-\Phi)$（v24）与勾股恒等式 $\mathrm{sech}^2\frac{1}{2T}=1-h^2$ 给出 $r=\dfrac{2Th(1-\Phi)}{1-h^2}$；代回 $\Phi(1+r)<2r$ 后 $r$ 被整块消掉，得 $S'<0\iff 0<G$，$G=2Th(1-\Phi)(2-\Phi)-\Phi(1-h^2)$。判决：**撤销"$r$ 的上下夹逼是必要入口"**，$r$ 的界降为可选旁证 | Spec **v28**（增 `shapeH`／`TargetPropRatioPhiForm`／`shapeG`／`TargetPropShapeSignUnary`）；`05_Lean验证/Ring15LockUnary.lean`（2 条＋私有 `tanhPos`／`sechSq_eq_one_sub_tanh_sq`／`ratioCriterion`）；卡 §三十四；`04_计算验证/环15_判据一元化_数值核对.py`；`01_文献基线/文献卡_R201_超导刚度二阶曲率与判据一元化.md` | A 闸**二十八模块 PASS**（28/28 编译、58 条 axioms 全为白名单、53 条 `#check`、257 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 二十八模块 v28）`）；B 闸判**定义式**（最可能跑偏行：`targetPropRatioPhiForm` 里 `unfold ratioR` 后的 `rw [hT2, hS]`——分子或分母任一写错，`rw` 仍能对上形似式；本轮令分子由 `nlinarith [hp]` 从 $\frac T2|w'|=h(1-\Phi)$ 严格推出、分母由勾股恒等式逐步展开） | `审-6` 仍未闭合；G-188b-2f **判据一元化完成、$G$ 的符号未证**（$S'$ 分段与 $T_{\min}$ 编址依赖 $\Phi$ 单调性）；甲类残余＝$T>T_{\rm break}$ 的 $p_{\rm lock}$ 写法、G-186c 域核、G-188b-2f、G-189、G-190a；数值旁证 $r$ 闭式相对残差 $1.10\times10^{-8}$、$S'<0$ 与 $G>0$ 不一致 0 处、$S'$ 变号括号 $[0.3430,0.3440]$ |



| 202 | 15/`审-6` | **判据的 δ／λ 形式与判据比的双侧夹逼（G-188b-2g）**。201 把判据一元化后，`PROGRESS` 判"最该修＝$\Phi$ 的单调性"，本轮先做代数检验：$\Phi'<0\iff\Phi S<4Th\delta\iff\lambda<2\delta/(1-\delta)$，而 $G>0\iff\lambda<\delta(1+\delta)/(1-\delta)$，因 $1+\delta<2$，前者阈值严格更宽 ⇒ **$\Phi$ 单调性不足**；遂改判。三件构造：①$r$ 的**双侧夹逼**——$\mathrm{sech}^2\frac{u}{2T}\in[S,1]$（$u\in[0,1]$）逐点乘 $u^2\ge0$ 积分，$\int_0^1u^2=\frac13$ ⇒ $\frac S3\le T^2|w'|\le\frac13$ ⇒ $\frac13\le r\le\frac1{3S}$，两端只读端点核值与窗口长度、**不读 $\Phi$**；②$\lambda:=\frac{S}{2Th}$ 是 $h$ 的对数导数负值（$\lambda=-T\frac{d}{dT}\ln\tanh\frac1{2T}$），$\sinh$ 二倍角给 $\lambda=1/(T\sinh\frac1T)$——纯 $T$ 显式函数；③由 $S=2Th\lambda$ 得 $G=2Th[\delta(1+\delta)-(1-\delta)\lambda]$ ⇒ $S'<0\iff\lambda<R(\delta)$，$R(\delta)=\delta(1+\delta)/(1-\delta)$ | Spec **v29**（增 `deficitFrac`／`endpointLambda`／`TargetPropRatioBracketLow`／`TargetPropRatioBracketHigh`／`TargetPropLambdaForm`／`TargetPropShapeSignDeficit`）；`05_Lean验证/Ring15LockDeficit.lean`（4 条＋私有 `sechSq_anti`／`int_u_sq`／`abs_deriv`／`ratio_integral`／`criterionPhi` 等 10 条）；卡 §三十五；`04_计算验证/环15_判据δλ_数值核对.py|_输出.txt|环15_判据δλ形式_夹逼与近相切.png` | A 闸**二十九模块 PASS**（29/29 编译、62 条 axioms 全为 `{propext, Classical.choice, Quot.sound}`、57 条 `#check` 全 `[ ok ] type: … : Spec.…`、258 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 二十九模块 v29）`）；B 闸判**定义式**（最可能跑偏行：`sechSq_anti` 的 `Real.cosh_le_cosh.mpr harg` 与 `one_div_le_one_div_of_le` 的组合——若把 $|\cdot|$ 内的 $\frac{u}{2T}$ 直接当单调变量（略去 $u\ge0$ 的绝对值化），$u<0$ 段会给出反向不等式；本轮以 `abs_of_nonneg (div_nonneg hx.1 …)` 显式把 $u\in[0,1]$ 的符号交代） | `审-6` 仍未闭合；G-188b-2g **判据改写完成、$r$ 夹逼定理化**；余 **G-188b-2h**（$\lambda=1/(T\sinh\frac1T)$ 单调未证、$R(\delta)$ 单增未证、$T_{\min}\approx0.3439$ 编址依赖 $\delta(T)$ 单调）；数值旁证 $r$ 夹逼违反 0 点（$\min r=0.356719$）、$\lambda$ 闭式相对误差 $5.64\times10^{-16}$、$\mathrm{sign}(G>0)$ 与 $\lambda<R$ 不一致 0 点、变号括号 $(0.3430,0.3440)$、$R-\lambda$ 于 $T=0.3435$ 仅 $+2.61\times10^{-4}$（近相切） |

| 211 | 15/`审-6` | **近零端 $D>0$ 进链（G-188b-2k 近零端闭合）**。210 收盘余"近零端 $D>0$"与"$(0,1)$ 内零点唯一"两件，本轮做第一件。三步：①`TargetPropDeficitGeSq`（$0<T\le\frac1{10}\Rightarrow\frac8{15}T^2\le\delta(T)$）：$|w'|=-w'=\frac1{T^2}\int_0^1u^2\mathrm{sech}^2\frac{u}{2T}du$；$T\le\frac1{10}\Rightarrow2T\le1$，断区间 $[0,1]=[0,2T]\cup[2T,1]$、右段非负；左段 $\mathrm{sech}^2z=1-\tanh^2z\ge1-z^2$（$z=\frac{u}{2T}\le1$，由 $\tanh z\le z$ 自建 `tanh_le_self`，Mathlib 无 `Real.tanh_le_self`），$\int_0^{2T}u^2(1-\frac{u^2}{4T^2})du=\frac{16}{15}T^3$ ⇒ $-w'\ge\frac{16}{15}T$；配合 197 `TargetPropShapeEnd`（$h-w=\frac T2|w'|$）与 $h\le1$ ⇒ $\delta\ge h-w\ge\frac8{15}T^2$。②`TargetPropLambdaLeSq`（$\lambda\le\frac{T^2}{3}$）：$s=1/T\ge10$；$\varphi(s)=e^s/s^3$ 在 $[10,\infty)$ 单增（$\varphi'=\frac{e^s(s-3)}{s^4}\ge0$），$\varphi(10)=\frac{e^{10}}{1000}>12$（`Real.exp_one_gt_d9`：$e>2.7182818283$，$(2.7182818283)^{10}>12000$；`Real.exp_nat_mul` 把 $e^{10}=(e^1)^{10}$）⇒ $e^s\ge12s^3$；$2\le e^{2s}$（`Real.add_one_le_exp`）⇒ $e^{-s}\le e^s/2$ ⇒ $\sinh s=\frac{e^s-e^{-s}}2\ge\frac{e^s}{4}\ge3s^3$ ⇒ $\lambda=\frac1{T\sinh(1/T)}\le\frac{T^2}{3}$。③`TargetPropGapPosNearZero`（$0<T\le\frac1{10}\Rightarrow0<D$）：$R(\delta)-\delta=\frac{2\delta^2}{1-\delta}\ge0$（$1-\delta>0$ 由 $\delta\le\frac13$）⇒ $D\ge\delta-\frac{T^2}{3}\ge\frac{T^2}{5}>0$。 | Spec **v36**（+3 条 `def … : Prop`）；新模块 `Ring15LockNearZero.lean`（313 行、3 定理＋11 私有引理：`continuous_tanh`／`hasDerivAt_tanh`／`sechSq_le_one`／`tanh_le_self`／`tanh_nonneg`／`sechSq_ge_one_sub_sq`／`integral_u_sq_sechSq_ge`／`exp_ten_gt`／`exp_ge_twelve_cube`／`sinh_ge_three_cube`／`shapeH_pos`） | `04_计算验证/环15_近零端界_数值旁证.py`、`环15_近零端界_输出.txt`、`环15_近零端界_数值旁证.png`（126 445 B） | A 闸 **三十六模块 PASS**（36/36 编译、82 条 axioms 全白名单、78 条 `#check` 全对齐、`[FAIL` 0、265 文件 0 命中、exit 0，约 27 分钟） | G-188b-2k **尾段＋近零端两段已闭、整体未闭**：零点集收窄为 $\{D=0\}\subseteq[\frac1{10},1]$；余 $(0,1)$ 内零点唯一（$D'$ 恰一零点）；数值旁证 $\delta/T^2\approx3.289868$（$T\le0.1$）、$\lambda/T^2\le0.0908$、$D(0.005)=8.226\times10^{-5}>T^2/5$ |

| 212 | 15/`审-6` | **零点存在性进链（G-188b-2k 存在性前段）**。210 收盘余"近零端"与"零点唯一"两件，211 已做近零端；本轮只做**存在性**、不碰唯一性。路线：不依赖单调性（$D$ 在 $(0,1)$ 内非单调，数值上 $D'$ 于 $0.194$ 变号、$0.3529$ 处负极小），只取"连续＋两端异号"。①连续：205 `TargetPropCriterionGapDeriv` 给 $\forall T>0$ `HasDerivAt criterionGap (criterionGapDeriv T) T`，逐点 `ContinuousAt.continuousWithinAt` 得 `ContinuousOn criterionGap (Icc (1/10) 1)`；②两端：211 于 $T=\frac1{10}$ 给 `0 < D`，210 于 $T=1$ 给 `D < 0`（前件在该端点均成立）；③介值：`intermediate_value_Icc'` 以 $0\in\mathrm{Icc}(D(1),D(\frac1{10}))$ 取 $x\in\mathrm{Icc}(\frac1{10},1)$ 与 $D(x)=0$；④端点排除：由两端严格异号，用 `rcases lt_or_eq_of_le` 分三支，等号支与 ②矛盾（第一支须 `rw [heq.symm] at hval`），得 $\frac1{10}<x<1$。Spec v37 一条 `def … : Prop`（`TargetPropGapZeroExists`），`Ring15LockZeroExists`（约 45 行、1 定理）；A 闸三十七模块 **PASS**（37/37 编译、83 条 `#print axioms`（80 条主白名单＋3 条 `{propext, Quot.sound}` 子集）、79 条 `#check` 全 `[ ok ] type: … : Spec.…`、`[FAIL` 0、266 文件 0 命中、exit 0，约 28 分钟）。B 闸判**定义式**：下游只消费"存在"这一句；两端符号是已证命题的显式实例化，连续性由 `HasDerivAt.continuousAt` 展开，介值一次应用，无"$D$ 连续显然"式带过；最可能跑偏行＝端点排除的 `rw [heq.symm] at hval`（方向写反则开区间退化为闭区间）。**与 211／210 合得** $\varnothing\neq\{D=0\}\subseteq(\frac1{10},1)$。文献边界（只作约束）：重入／多临界相变在铁磁超导与多带模型有先例，故"零点唯一"不得由物理常识假定，须链内证；本轮因此只证存在。**仍缺**：零点唯一（"至多一个"）、$D'$ 恰一零点、$T\downarrow0$ 的渐近常数。数值旁证（反馈层）：零点 $T^*=0.194153703$ 落在区间内，与存在性一致，但不得据此宣称"零点就是 $0.194$"。`审-6` 未闭合、闭合数 0、编号 37；第 5 层不启动。入口：`Ring15LockZeroExists.lean`／Spec v37／`a_gate.ps1`（v37）。 |

| 215 | 15/`审-6` | **$\delta'$ 去 $|w'|$ 的闭式与严格上界（G-188b-2k-u 右端形态降级）**。214 收盘余"$Q$ 严格单增"未证，其右端 $(\ln R)'=(R'/R)\delta'$ 需要 $\delta'$ 的**只含 T** 的界，而 204 的 $\delta'$ 里含积分 $|w'|=\frac1{T^2}\int_0^1u^2\mathrm{sech}^2\frac{u}{2T}du$。①四元组：输入＝v39 `deficitDeriv`、197 `TargetPropWGapIbp`、190 `w>0`、210 `δ≤1/3`；依据＝分部积分恒等式＋正性（无新参数、无拟合）；模型＝无（只做表示改写）；输出＝三条 Prop；下一环消费＝$\delta'$ 的 T-only 上界。②代数：由 $w=h+\frac T2w'$ 得 $w'=\frac{2(w-h)}{T}$（私有 `wderiv_eq`：`eq_div_iff`＋`nlinarith`），代入 204 闭式得 $\delta'=\frac{2(h-w)}{Th}-\frac{w\,s}{2T^2h^2}$（`ring_nf`），末项严格正 ⇒ $\delta'<\frac{2\delta}{T}$；再用 210 得 $\delta'<\frac{2}{3T}$。③`Ring15LockDeficitUb`（约 100 行、3 定理＋5 私有）：闭式对齐、两条上界；`tanh_norm_ne` 只为 `field_simp` 提供 $\tanh\frac1{2T}\ne0$ 的归一形态，不改变对象。④A 闸四十模块（90 axioms、85 `#check`）结果见 §五。B 闸判**定义式**：最可能跑偏行＝`wderiv_eq`（若把 $w'=\frac{2(w-h)}{T}$ 写成 $\frac{2(h-w)}{T}$，$\delta'$ 的减项变加项、上界方向反转；以 204 的 $\delta'>0$ 与数值 $\delta'(1)=0.0396$ 双向核对）。**新子缺口 G-188b-2k-u-1**＝$\delta'$ 的 $1/T^2$ 级上界（$T=1$ 处需 $C\le0.0596$）；$Q$ 严格单增仍未证；`审-6` 未闭合、闭合数 0、编号 37；第 5 层不启动。入口：`Ring15LockDeficitUb.lean`／Spec v40／`04_计算验证/环15_δ上界_数值旁证.py`。 |

| 216 | 15/`审-6` | **$\delta$ 的 $T\to\infty$ 渐近与 $Q$ 单调性入口改判（第 2 步止，Spec 未改）**。由 $h=\tanh\frac1{2T}$、$w=\int_0^12u\tanh\frac{u}{2T}du$ 的幂级数逐项积分得 $\delta=1-\frac wh=\frac13-\frac1{45T^2}+O(T^{-4})$、$\delta'=\frac2{45T^3}+O(T^{-5})$（纸面，未进 Lean）；数值核对 $(\frac13-\delta)/(\frac1{45T^2})$ 在 $T=5,10,20,50,100,200$ 取 $0.9976\to1.0000$。**关键反证**：$\sup_{T>0}T^2\delta'=0.059019$（$T=0.4250$），而 215 的可用条件是 $C\le0.0596$ ⇒ 窗口仅 **1%**；三阶 $\tanh$ 界给 $C\approx0.1$，任何解析粗界都落不进 ⇒ 判 215 的入口"$\delta'\le C/T^2$"不可用，`DISCARD.md` 216-1。**改判**：$Q$ 单调性改走 $G=\lambda'R-\lambda R'\delta'>0$ 的代数判号（三段均已有理闭式，数值余量 $(\ln Q)'\ge0.098536$，精度需求约 10%），记为新入口 **G-188b-2k-u-2**；G-188b-2k-u-1 降为备用。**本轮不改 Spec、不开模块、不跑 A 闸**（v40 的 40/40 PASS 仍为最新结论）。依据＝主卡 §四十九、`04_计算验证/环15_δ渐近系数_输出.txt`。闭合数 0、编号 37、第 5 层不启动。 |

| 217 | 15/`审-6` | **$\tanh$ 工具引理公开化与三阶下界（Spec v41，工具环）**。216 判明 $Q$ 单调性须走 $G=\lambda'R-\lambda R'\delta'>0$ 的代数判号，但 `hasDerivAt_tanh`／`tanh_lt_self` 原为 `LockW`／`LockDeficitMono` 的**私有**引理，跨模块取不到 ⇒ 本轮建工具层。Spec v41 加 `TargetPropTanhCubic`（$\forall x\ge0,\ x-\frac{x^3}{3}\le\tanh x$）；新模块 `Ring15LockTanhTools` 证出该命题＋8 条公开定理（`continuous_tanh`／`cont_sechSq`／`sechSq_pos`／`sechSq_le_one`／`tanhHasDerivAt`／`sechSq_eq_one_sub_tanh_sq`／`tanh_pos_of_pos`／`tanhLtSelf`）。**路线（定义式，不走级数）**：$\tanh x=x-\int_0^x\tanh^2$（FTC）＋$\tanh^2t\le t^2$＋$\int_0^xt^2=\frac{x^3}{3}$ ⇒ 三阶界；不用 Bernoulli 系数。**关键定量结论**：三阶逐点代入只给 $\delta\le\frac13+\frac{1}{30T^2}$（方向错，$T\to\infty$ 时松于 $\frac13$），要得 $\delta\le\frac13-\frac{c}{T^2}$ 必须补 $h$ 的**五阶上界**（218 靶）。A 闸四十一模块 **PASS**（41/41 编译、99/99 公理白名单、86/86 `#check`、`[FAIL` 0、token 270 文件 0 命中、exit 0）。依据＝主卡 §五十、`04_计算验证/环15_tanh三阶界_输出.txt`。本轮 9 条定理**不计入闭合数**；闭合数 0、编号 37、第 5 层不启动。 |
| 218 | 15/`审-6` | **$\tanh$ 的五阶上界（Spec v42，工具环续）**。217 判"三阶界只给 $\delta\le\frac13+\frac{1}{30T^2}$（方向错）"，缺项来自 $\frac{s-h}{s}\approx\frac1{12T^2}$ ⇒ 必须给 $h$ 的上界。本轮不靠级数余项（216 预警的最难点），改用**三阶界平方后积分**：$\tanh s=s-\int_0^s\tanh^2$、$\tanh^2t\ge(t-\frac{t^3}{3})^2\ge t^2-\frac{2t^4}{3}$（$0\le t\le1$，$t^6/9$ 整体丢弃、方向安全）⇒ $\tanh s\le s-\frac{s^3}{3}+\frac{2s^5}{15}$。Spec v42 加 `TargetPropTanhQuintic`；新模块 `Ring15LockTanhQuintic`（`tanhQuintic`＋对齐主定理 `targetPropTanhQuintic`）。**侧条件 $s\le1$ 不可省**：平方要求两个底数非负，$t-\frac{t^3}{3}\ge0$ 只在 $t^2\le1$ 成立（B 闸最可能跑偏行）。合成预告：三阶给 $w\ge\frac{1}{3T}-\frac{1}{60T^3}$，与五阶 ${h_{\rm ub}}$ 合成 $\delta\le\frac13-\frac{c}{T^2}$，数值 $c(T)$ 由 0.018018（$T=1$）升至 0.022221（$T=50$）、极限 $\frac1{45}$ ⇒ 219 取 $c=0.018$。A 闸四十二模块 **PASS**（42/42 编译、101/101 公理白名单、87/87 `#check`、FAIL 0、token 271 文件 0 命中、exit 0）。依据＝主卡 §五十一、`04_计算验证/环15_tanh五阶界_输出.txt`。本轮 2 条定理**不计入闭合数**；闭合数 0、编号 37、第 5 层不启动。 |
| 219 | 15/`审-6` | **$\delta$ 的减平方界（Spec v43）**。218 只给 $h$ 的上界，本环把 $w$ 的下界（217 三阶界逐点积分：$w\ge\frac1{3T}-\frac1{60T^3}$）与 $h$ 的上界（$h\le\frac1{2T}-\frac1{24T^3}+\frac1{240T^5}$）合成 $\delta$ 的上界：$\frac wh\ge\frac{w_{\rm lb}}{h_{\rm ub}}=\frac{4T^2(20T^2-1)}{120T^4-10T^2+1}$，交叉相乘后 $\frac{w_{\rm lb}}{h_{\rm ub}}\ge\frac23+\frac{9}{500T^2}\iff1.52T^4-1.46T^2-0.054\ge0$（$T=1$ 余量 $0.006$、单增）⇒ $\delta\le\frac13-\frac{9}{500T^2}$（$T\ge1$）。Spec v43 加 `TargetPropDeficitLeThirdSubSq`；新模块 `Ring15LockDeficitSq`（5 辅助＋1 主＋对齐）。**侧条件 $T\ge1$ 不可去**（五阶界要 $s=\frac1{2T}\le1$；余量在 $T=0.9$ 已转负 $-0.24$）；**常数 $\frac{9}{500}$ 不可再大**（$T=1$ 处余量恰被吃光，真界 $0.018018$）。A 闸四十三模块 **PASS**（43/43 编译、103/103 公理白名单、88/88 `#check`、FAIL 0、token 272 文件 0 命中、exit 0）。依据＝主卡 §五十二、`04_计算验证/环15_δ减平方界_输出.txt`。本轮 1 主＋4 辅助定理**不计入闭合数**；闭合数 0、编号 37、第 5 层不启动。 |
| 220 | 15/`审-6` | **判据的 $h$-闭式（纸面环，Spec 不动）**。$G$ 判号的两个奇异量（$\lambda$ 含 $1/h$、$R$ 含 $1/(1-\delta)$）无法直接比较，本轮把 $\lambda'$ 化成只含 $h$：$\lambda=\frac{1-h^2}{2Th}$、$\lambda'=\frac{(1-h^2)(1+h^2-2Th)}{4T^3h^2}$，故 $(\ln Q)'=\frac{1+h^2-2Th}{2T^2h}-\delta'W$，$W=\frac1\delta+\frac1{1+\delta}+\frac1{1-\delta}$。**副产品**：$2Th\le1\Rightarrow$ 分子 $\ge h^2>0$，$\lambda$ 严格增成为 $h\le\frac1{2T}$ 的推论（与 v29 互为互检）；判号只剩"分子 vs $\delta'$"。**精度定量**：判号允许 $\delta'$ 上界为 $1.43$–$1.46$ 倍真值（$T\ge0.1$）；若用 $h^2$ 替分子，允许域压到 $1.07$ 倍，五阶界（$T=1$ 给 $\delta'\le0.63$）差一个量级 ⇒ 221 必须七阶 $\tanh$ 双界。数值核对：$\lambda'$ 闭式 $\le4.3\times10^{-9}$、$(\ln Q)'$ 闭式 $\le4.6\times10^{-7}$。本轮不产定理、不跑闸、**不计入闭合数**；闭合数 0、编号 37、第 5 层不启动。 |
|||| 221 | 15/`审-6` | **七阶 $\tanh$ 下界进 Spec（v44），判据定义域被劈成两段**。220 登记"七阶双界"未动手；本轮先做**下界**：$\tanh s=s-\int_0^s\tanh^2$（217 FTC）＋v42 五阶上界 $S(t)=t-\frac{t^3}{3}+\frac{2t^5}{15}$ ⇒ $\tanh^2\le S^2$，而 $S^2=\bigl(t^2-\frac{2t^4}{3}+\frac{17t^6}{45}\bigr)+\frac{4t^8}{45}\bigl(\frac{t^2}{5}-1\bigr)\le t^2-\frac{2t^4}{3}+\frac{17t^6}{45}$（$t\le1$，末项非正），积分得 $s-\frac{s^3}{3}+\frac{2s^5}{15}-\frac{17s^7}{315}$ ⇒ $\tanh s\ge$ 该式。Spec v44 加 `TargetPropTanhSepticLower`；新模块 `Ring15LockTanhSeptic`（`tanhEqSubIntegral`／`integralTrunc`／`tanhSepticLower`／对齐主定理）。**同时纠正 220 的一处记账错误**：七阶**上界**是 $S_3+\frac{62s^9}{2835}$、下界才是 $S_3$（$s=0.5$：$S_3=0.462078373<\tanh=0.462117157<S_4=0.462121087$），220 写反了奇偶归属（DISCARD 221-1）。**判据域定量**：$T\ge\frac12$ 时七阶双界的 $\delta'$ 上界只占 220 允许域的 $68\%$–$70\%$（余量 1.44 倍，$T=1$ 处 $1.457$）⇒ 222 可闭；但 $T\in[\frac1{10},\frac12)$ 时 $s=\frac1{2T}>1$、$\tanh$ 幂级数在 $s>\pi/2$ 外发散，多项式界整体失效，且粗界 $\frac{2\delta}{T}$ 在 $T=0.30/0.40/0.45$ 已越允许域 ⇒ **新立缺口 G-188b-2k-u-2a**（低端第三条估计）。A 闸四十四模块 **PASS**（44/44 编译、105/105 公理白名单、89/89 `#check`、FAIL 0、token 273 文件 0 命中、exit 0）。依据＝主卡 §五十四、`04_计算验证/环15_七阶双界_数值核对.py`／`_输出.txt`。本轮 4 条定理**不计入闭合数**；闭合数 0、编号 37、第 5 层不启动。 |
|||| 222 | 15/`审-6` | **七阶 $\tanh$ 上界进 Spec（v45），七阶双界闭环**。221 只落下界；本环用"下界平方后积分"造上界：$\tanh^2\ge P^2$（$P$＝v44 七阶下界），且 $P=S_2-C$（$C=\frac{17t^7}{315}$）、$S_2\le t$ ⇒ $P^2=S_2^2-2S_2C+C^2\ge S_2^2-\frac{34t^8}{315}$（丢正项 $C^2$、放大交叉项 $2S_2C\le2tC$）。积分：$\int S_2^2=\frac{s^3}{3}-\frac{2s^5}{15}+\frac{17s^7}{315}-\frac{4s^9}{405}+\frac{4s^{11}}{2475}$、$\int\frac{34t^8}{315}=\frac{34s^9}{2835}$，s⁹ 合成 $-\frac{4}{405}-\frac{34}{2835}=-\frac{62}{2835}$ 与级数第 5 项 $62/2835$ 严格对齐 ⇒ $\tanh s\le S_4:=s-\frac{s^3}{3}+\frac{2s^5}{15}-\frac{17s^7}{315}+\frac{62s^9}{2835}$。Spec v45 加 `TargetPropTanhSeptic`；新模块 `Ring15LockTanhSepticUb`（`integralFive`／`tanhSepticUpper`／对齐版）。**七阶双界现已完整进链**：$S_3\le\tanh s\le S_4$（$0\le s\le1$，两条独立定理）。**首版把 $\int\frac{34t^8}{315}$ 写成 $\frac{34s^9}{315}$（漏乘 $\frac19$），`ring` 报 9 倍差暴露，已记 DISCARD 222-1**。数值：双界余量浮点零、$S_4$ 最大松度 $0.83\%$（$s=1$）、双侧 $w,h$ 误差 $T=1$ 约 $10^{-4}$／$T=5$ 约 $10^{-11}$（$O(T^{-7})$ 兑现）。A 闸四十五模块 **PASS**（45/45 编译、107/107 公理白名单、90/90 `#check`、FAIL 0、token 275 文件 0 命中、exit 0）。依据＝主卡 §五十五、`04_计算验证/环15_七阶上界_数值核对.py`／`_输出.txt`。本轮 3 条定理**不计入闭合数**；闭合数 0、编号 37、第 5 层不启动。 |
|||| 223 | 15/`审-6` | **$w$ 的七阶双侧界进 Spec（v46），判号域定量复核**。222 备齐 $S_3\le\tanh\le S_4$（$0\le s\le1$）；本环把双界沿权积分传到 $w$：$u\in[0,1]$、$T\ge\frac12$ ⇒ $\frac{u}{2T}\in[0,1]$，逐点 $2uS_3(\frac{u}{2T})\le2u\tanh(\frac{u}{2T})\le2uS_4(\frac{u}{2T})$，`integral_mono_on` 后两支积分闭式逐项 `integral_pow` 收成 $w_{\rm lb}(T)=\frac{1}{3T}-\frac{1}{60T^3}+\frac{1}{840T^5}-\frac{17}{181440T^7}$、$w_{\rm ub}=w_{\rm lb}+\frac{31}{3991680T^9}$ ⇒ $\forall T\ge\frac12$：$w_{\rm lb}\le w\le w_{\rm ub}$。Spec v46 加两 def＋`TargetPropWGapLowerBound`／`TargetPropWGapUpperBound`；新模块 `Ring15LockWGapSeptic`（`integralS3`／`integralS4`／`wGapLowerBound`／`wGapUpperBound`／两条对齐版，6 定理）。**判号域定量（约束/反馈层）**：正确复合上界 $\delta'_{\rm ub}=\frac{2(h_{\rm ub}-w_{\rm lb})}{T h_{\rm lb}}-\frac{w_{\rm lb}(1-h_{\rm ub}^2)}{2T^2h_{\rm ub}^2}$ 给 $\sup_{[0.5,1]}\delta'_{\rm ub}/\delta'=1.46338$（$T=0.5$）、$[1,5]$ 上 $1.00319$，与 220 允许域 $1.43$–$1.46$ 贴边；充分条件 $A_{\rm lb}:=\frac{1+h_{\rm ub}^2-2Th_{\rm ub}}{2T^2h_{\rm ub}}\ge\delta'_{\rm ub}W(\delta_{\rm ub})$ 在 $T\ge\frac12$ **全域成立**，最小比值 $1.08009$（$T=0.5$），渐近 $\frac{10}{7}=1.42857$ ⇒ $(G>0)$ 于 $T\ge\frac12$ 已"数值可判"，但**未成定理**。A 闸四十六模块 **PASS**（46/46 编译、109/109 公理白名单、91/91 `#check`、FAIL 0、token 276 文件 0 命中、exit 0）。依据＝主卡 §五十六、`04_计算验证/环15_w七阶双侧界_数值核对.py`／`_输出.txt`。本轮 6 条定理**不计入闭合数**；闭合数 0、编号 37、第 5 层不启动。 |
| 214 | 15/`审-6` | **$Q$ 与 $R(\delta)$ 的正性（G-188b-2k-u 的结构前件）**。213 收盘余"$Q$ 严格单增"未证；本轮先补其**符号前件**：$R(\delta)>0$ 与 $Q>0$ 由 $\delta\in(0,1)$ 与 $\lambda>0$ 给出，使 $(Q)'/Q$ 的写法在链内合法（否则对数导数无定义）。①四元组：输入＝202 `endpointLambda` 与 203 `deficitRatio` 定义、190 `targetPropWGapPos`（$w>0$）、197 `targetPropShapeEndGt`（$w<h$）；第一性依据＝纯代数（$R=\delta(1+\delta)/(1-\delta)$、$\delta=1-\Phi$、$\Phi=w/h$）＋保序性；待建模型＝无；输出＝`TargetPropDeficitRatioPos`／`TargetPropRatioOverLambdaPos`；下一环消费＝对数导数的分母非零与分子正。②**放弃分支（DISCARD 214-1）**：$Q$ 的乘法闭式 $Q=\mathrm{sech}^2\frac1{2T}\cdot w/\big(2T(h-w)(2h-w)\big)$ 虽代数正确，但 `unfold … ／field_simp` 后目标停在 `sechSq*tanh*w*(2tanh−w)⁻¹*2 − sechSq*w²*(2tanh−w)⁻¹ = sechSq*w`，试 `ring`／`ring_nf`／`← sub_div + div_eq_iff`／`mul_right_cancel₀`（并 `field_simp`）均不闭合，故**不入 Spec**（不成立条件：仅以逆元消去＋多项式归一的路径；非命题为假）。③`Ring15LockRatioForm`（约 55 行、2 定理＋1 私有 `tanh_pos_of_pos`）：正性走 `Real.tanh_eq_sinh_div_cosh`＋`Real.sinh_pos_iff`＋`Real.cosh_pos`＋`div_pos`（`Real.tanh_pos` 在本环境 Mathlib 不存在）；$\delta>0$ 由 `div_lt_one`＋`linarith`；$1-\delta>0$ 由 `simp only [deficitFrac]`＋`linarith`；$Q>0$ 由 `div_pos` 合 202 界。④A 闸三十九模块（87 axioms、82 `#check`）实跑结果见 §五。B 闸判**定义式**：最可能跑偏行＝`hltT : wGap T < Real.tanh (1/(2*T)) := hlt`（`shapeH` 与 `tanh` 的 defeq 转写；若误把 `shapeH` 当成与 `tanh` 不同的对象，$\delta$ 的口径会在 `deficitFrac`／`shapePhi` 之间漂移，而 $Q>0$ 仍可照过）。**G-188b-2k-u 仍未证**（本轮只补正性与分母结构，未触及单调性）；`审-6` 未闭合、闭合数 0、编号 37；第 5 层不启动。入口：`Ring15LockRatioForm.lean`／Spec v39／`a_gate.ps1`（v39）。 |

| 213 | 15/`审-6` | **零点唯一性压成条件句（G-188b-2k 唯一性前段）**。212 收盘余"唯一"；本轮不硬攻 $D'$，而把 $D=0$ 改写成 $Q:=\lambda/R(\delta)=1$，并把唯一性归约为"$Q$ 严格单增 ⇒ 至多一解"。①数值可行性核对（反馈层）：$Q(0.10)=0.025932246$ 单调升至 $Q(1)=1.427389136$，901 格点无回退，$(\ln Q)'$ 最小 $0.098536$（$T=1$）仍正；同时**否证**"$D'$ 左正右负分段"入口——$D'$ 先增后减（极大 $0.668035$ 于 $0.110$、极小 $-0.731863$ 于 $0.353$，$D''$ 变号两次 $0.10987$／$0.35301$），唯一零点 $0.194154$，而 $D$ 零点 $0.343858$，"$D'$ 恰一零点"$\ne$"$D$ 恰一零点"。②Spec v38：`ratioOverLambda T := endpointLambda T / deficitRatio T`（`deficitRatio` 内含 `deficitFrac`，故即 $\lambda/R(\delta)$）、`TargetPropGapZeroUniqueOfRatioMono`（条件 `def … : Prop`）。③`Ring15LockZeroUnique`（约 50 行、1 定理＋1 私有）：`D=0` 经 `unfold criterionGap` 与 `linarith` 给 $\lambda=R$，`targetPropLambdaBounds` 给 $\lambda>0$ 故 $R\ne0$，`div_self` 得 $Q=1$；唯一性用 `lt_trichotomy` 三支，两支由 `hmono` 的严格不等与 $Q\equiv1$ 冲突（`linarith`）。前件限制在 $[\frac1{10},1]$，未放大到 $(0,\infty)$。A 闸三十八模块 **PASS**（38/38 编译、公理行 83 条（80 主＋3 子集）、80 条 `#check` 全 `[ ok ] type: … : Spec.…`、`[FAIL` 0、267 文件 0 命中、exit 0，约 28 分钟）。B 闸判**定义式（条件形态）**：最可能跑偏行＝私有引理的 `rw [heq]`（若把 `deficitRatio T` 误读成不含 $\delta$ 的另一支，$Q$ 的定义就会漂移），已用 `unfold ratioOverLambda` 钉住。**新增显式缺口 G-188b-2k-u**＝$Q$ 严格单增（$\lambda'R>\lambda R'\delta'$），前件未证 ⇒ 唯一性仍未闭；`审-6` 未闭合、闭合数 0、编号 37；第 5 层不启动。入口：`Ring15LockZeroUnique.lean`／Spec v38／`a_gate.ps1`（v38）／`04_计算验证/环15_唯一性可行性_数值核对.py`。 |

| 210 | 15/`审-6` | **$\delta\le\frac13$ 落地与尾段的最终排除（G-188b-2k 尾段闭合）**。209 把尾段削到只剩 $\delta\le\frac13$，本轮把它落地：①`TargetPropTanhSecant`：$a>0$、$u\in[0,1]$ ⇒ $u\tanh a\le\tanh(au)$——路线不是"引 tanh 凹性 API"（209 已确认 Mathlib 无），而是 $g(u)=\tanh(au)/u$ 的**一阶判据**：$g'$ 分子 $=y\mathrm{sech}^2y-\tanh y$（$y=au$），其符号 $\iff y<\sinh y\cosh y\iff2y<\sinh(2y)$，由 `Real.sinh_two_mul`＋`Real.sinh_sub_id_strictMono`；`strictAntiOn_of_hasDerivWithinAt_neg` 给 $g$ 严格减，$g(1)<g(u)$ 乘 $u>0$ 收口；②`TargetPropDeficitLeThird`：逐点 $2u\cdot uh\le2u\tanh\frac{u}{2T}$ 后 `integral_mono_on`＋`integral_pow` 给 $w\ge\frac23h$，`le_div_iff₀` 得 $\delta\le\frac13$；③`TargetPropGapNegTail`：②＋209 条件合成 ⇒ **$T\ge1\Rightarrow D<0$ 无条件版**，$\{D=0\}\subseteq(0,1)$ 成立。**不闭合近零端与区间内零点唯一** | Spec **v35**（+3 条 `def … : Prop`）；`05_Lean验证/Ring15LockSecant.lean`（3 条目标定理＋4 条私有：`continuous_tanh`／`hasDerivAt_tanh`／`shapeH_pos`／`tanh_secant_core`）；卡 §四十三 | `_agate210.log`（跑完即删） | 编译：Spec exit 0；依赖序重建八模块后新模块 exit 0 零告警；A 闸**三十五模块实跑 PASS**（35/35 编译、79 条 axioms 全白名单、75 条 `#check`、`[FAIL` 0、264 文件 0 命中、exit 0） | G-188b-2k **尾段闭合、整体未闭**（闭合数 0）；余近零端 $D>0$ 的链内判据、$(0,1)$ 内零点唯一（$D'$ 恰一零点）；第三件 $\delta\to\frac13$ 速率只作趋势；211 入口＝近零端判据（先把"$D(0^+)$"的严格陈述钉清） |

| 209 | 15/`审-6` | **尾段的代数合成进链（G-188b-2k 前件-4/5）**。207 的三界里 $\lambda>\frac23$ 已于 208 进链、$\delta<\frac13$ 需 $\tanh$ 凹性（Mathlib 无 `hasDerivAt_tanh`／无 tanh 的 `ConcaveOn`，成本是自建一阶导＋sechSq 复合二阶导＋凹性判定＋割线四件），故本轮先做**不依赖凹性**的部分：①`TargetPropRatioLeOfLeThird`：$0<x\le\frac13\Rightarrow R(x)\le\frac23$，由 `div_le_iff₀` 化为 $3x^2+5x-2\le0$，再以 $3x^2\le x$ ⇒ $3x^2+5x-2\le6x-2\le0$，`nlinarith`；②`TargetPropGapNegOfDeficitLeThird`：**把 $\delta\le\frac13$ 明写为假设**，则 $R(\delta)\le\frac23<\lambda$ ⇒ $D<0$。$\delta>0$ 由 `TargetPropShapeEndGt`＋`div_lt_iff₀` 显式给出。**不闭合尾段、不改 Spec 已锁条目** | Spec **v34**（+2 条 `def … : Prop`）；`05_Lean验证/Ring15LockTailRatio.lean`（2 条目标定理＋私有 `shapeH_pos`／`deficit_pos`）；卡 §四十二 | `_agate209.log`（跑完即删） | 编译：Spec 39.7 s exit 0，依赖序重建七模块后新模块 exit 0 零告警；A 闸**三十四模块实跑 PASS**（34/34 编译、76 条 axioms 全白名单、72 条 `#check`、`[FAIL` 0、263 文件 0 命中、exit 0，约 30 分钟） | G-188b-2k 仍未闭（闭合数 0）；余 $R$ 侧已过闸、$\delta\le\frac13$ 未证、$D(0^+)>0$ 未证、$(0,1)$ 零点唯一未证；210 入口＝$\tanh$ 凹性／割线 |

| 208 | 15/`审-6` | **尾段下界的 $\lambda$ 一侧形式化（G-188b-2k 前件）**。207 纸面尾段需 $\lambda(1)=1/\sinh1$ 与 $\sinh1<3/2$，链内皆无。本轮升 Spec v33 加三条 `def … : Prop`（`TargetPropSinhOneLt`／`TargetPropLambdaOne`／`TargetPropLambdaTailGt`），新建 `Ring15LockTail`（50 行、3 定理、无私有引理）：$\sinh1<3/2$ 由 `Real.sinh_eq`＋`Real.exp_one_lt_three`＋`Real.exp_pos`；$\lambda(1)$ 由 `TargetPropLambdaForm` 在 $T=1$ 取值（部分需要边界）；$\forall T\ge1,\ 2/3<\lambda(T)$ 由 `div_lt_div_iff₀` 交叉相乘＋`TargetPropLambdaStrictMono`＋端点分支。**只闭合 $\lambda$ 一侧**，不含 $R(\delta)<2/3$，故 $T\ge1\Rightarrow D<0$ **未合成**。 | Spec **v33**（+3 条 def）；模块 33 个（+`Ring15LockTail`） | `_agate208.log`（已删） | `Ring15LockTail.lean` 50 行 | A 闸 **三十三模块 PASS**（33/33 编译、74 条 axioms 全白名单、70 条 `#check`、`[FAIL` 0、262 文件 0 命中、exit 0，约 27 分钟） | G-188b-2k 仍未闭（闭合数 0）；余 $\tanh$ 凹性／$R<2/3$／合成／近零端；209 入口＝凹性（首选 $1-\frac{2}{e^{2x}+1}$ 复合，备用 $\sinh y>y$） |

| 207 | 15/`审-6` | **尾段排除与零点域收窄（G-188b-2k 第 2 步，纸面＋数值）**。206 把目标改写为"$D'$ 恰一零点"，本轮不再试二阶，改走值域分离：凹性引理（$\tanh(au)\ge u\tanh a$，由 $\varphi'=-2a^2\tanh(au)\mathrm{sech}^2(au)\le0$＋端点为零）$\Rightarrow w>\tfrac23h\Rightarrow\delta<\tfrac13$；$R$ 严格单增 $\Rightarrow R(\delta)<R(\tfrac13)=\tfrac23$；$\lambda$ 严格单增且 $\lambda(1)=\tfrac1{\sinh1}>\tfrac23$（$\sinh1<\tfrac32$ 由 $e<3$）$\Rightarrow T\ge1$ 时 $\lambda>\tfrac23$。合得 $T\ge1\Rightarrow D<0$，故 $\{D=0\}\subseteq(0,1)$；副产物 $0<\delta<\tfrac13$、$0<R<\tfrac23$、$-1<D<\tfrac23$。 | 无（Spec 保持 **v32**、三十二模块不变，未升级） | `环15_尾段界_输出.txt` | `环15_尾段界_数值旁证.png` | **未跑闸**（结论全是纸面，未进 Spec；不得记为已过闸） | G-188b-2k 仍未闭（闭合数 0）；纸面给出尾部严格排除，形式化待 208（缺 `tanh` 凹性／割线／`sinh1<3/2` 三件） |

| 206 | 15/`审-6` | **判据差二阶可行性核对与意图改写（G-188b-2k，第 0–1 步即停）**。205 停点原定"求 $\delta''$、$\lambda''$ 闭式并读符号以证 $D''<0$"，本轮实算否证：$D'$ 为 U 形（极小 $-0.731863$ 于 $T=0.3529$，$1.50$ 处仍 $-0.047045$）、$D''$ 变号两次（$\approx0.1099$、$\approx0.3529$）、$\lambda'$ 钟形（峰 $1.859783$ 于 $0.29509$）、$\delta'$ 非单调（升段 290）；$D'$ 零点仍唯一（$T^*=0.194153703$）。故意图命题改写为"$D'$ 恰一零点"，等价于两单峰曲线 $P=R'\delta'$ 与 $\lambda'$ 只交一次。 | 无（Spec 保持 **v32**、三十二模块不变，未升级） | `环15_判据差二阶_输出.txt` | `环15_判据差二阶_数值核对.png` | **未跑闸**（无新 Spec／新模块；不得记为已过闸） | `审-6` 仍未闭合；余 **G-188b-2k**（零点唯一未证）；207 入口＝$P$ 峰位估计与 $0.2951$ 的次序比较 |

| 205 | 15/`审-6` | **判据差的导数结构（G-188b-2j 前件）**。204 收盘时最该修的是"$\delta'$ 与 $\lambda'$ 的显式比较"，本轮把两条闭式都推进链内：①`lambdaDeriv`：$\lambda'(T)=\dfrac{\cosh\frac1T/T-\sinh\frac1T}{(T\sinh\frac1T)^2}$——由 202 的 `TargetPropLambdaForm` 把 `endpointLambda` 转成 $1/(T\sinh\frac1T)$（只在 $(0,\infty)$ 上宣称，经 `Ioi_mem_nhds` 的最终相等交给 `congr_of_eventuallyEq`），再用商法则：$g=T\sinh\frac1T$、$g'=\sinh\frac1T-\cosh\frac1T/T$ ⇒ $\lambda'=-g'/g^2$；②`ratioFunDeriv`：$R'(x)=\dfrac{1+2x-x^2}{(1-x)^2}$（$n=x+x^2$、$n'=1+2x$、$m=1-x$、$m'=-1$）；③`criterionGapDeriv`：$D=R(\delta)-\lambda$ ⇒ $D'=R'(\delta)\delta'-\lambda'$（`HasDerivAt.sub`＋`comp`，$\delta(T)\ne1$ 由 $w>0$、$h>0$ 给出而非数值）。**未证**：$D'$ 的符号结构（$D$ 单峰须 $D'$ 单减／$D''<0$） | Spec **v32**（增 `lambdaDeriv`／`ratioFun`／`ratioFunDeriv`／`criterionGap`／`criterionGapDeriv`／`TargetPropLambdaDeriv`／`TargetPropRatioFunDeriv`／`TargetPropCriterionGapDeriv`）；`05_Lean验证/Ring15LockGapDeriv.lean`（3 条＋私有 `shapeH_pos'`／`deficit_eq'`／`hasDerivAt_lambdaVal`／`hasDerivAt_endpointLambda`／`hasDerivAt_ratioFun`／`hasDerivAt_deficitRatio`／`hasDerivAt_criterionGap`，156 行）；卡 §三十八；`04_计算验证/环15_判据差导数_数值核对.py|_输出.txt|环15_判据差导数_数值核对.png` | A 闸**三十二模块 PASS**（32/32 编译、72 条 axioms 全为 `{propext, Classical.choice, Quot.sound}`、67 条 `#check` 全 `[ ok ] type: … : Spec.…`、261 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 三十二模块 v32）`）；B 闸判**定义式**（最可能跑偏行：`hasDerivAt_lambdaVal` 的 `hval`——$-g'/g^2$ 化成 $\frac{\cosh/T-\sinh}{(T\sinh)^2}$ 时若 $\sinh\frac1T\ne0$ 未给足，$\lambda'$ 的正负会静默翻转而 A 闸照过；本轮显式给 `hsinhne`，并以闭式对差分的符号一致作外部锚） | `审-6` 仍未闭合；G-188b-2j 的**导数结构收口**为三条定理；余 **G-188b-2k**（$D'$ 的符号结构／$D$ 单峰）；数值旁证 $D'$ 闭式对差分 rel $2.0\times10^{-11}\sim1.7\times10^{-9}$、$D'$ 只变号一次于 $(0.19415,0.19464)$、$D$ 极大 $7.501333\times10^{-2}$ 于 $T=0.19415$、$D$ 零点唯一 $T_{\min}=0.343857872$、$D(0.03)=+2.978\times10^{-3}$、$D(1.50)=-2.960\times10^{-1}$ |

| 204 | 15/`审-6` | **$\delta$ 的导数闭式、严格单增与判据右端随 $T$ 的单增（G-188b-2i 前件）**。203 判"两侧同增不足以定交点"，卡点是 $\delta(T)=1-\Phi(T)$ 的链内单调性（$\Phi'$ 未进 Lean）。本轮证明 $\Phi'$ 根本不需要独立进入链：$\Phi=1-\delta$ ⇒ $\Phi'=-\delta'$，而 $\delta'$ 有纯商法则闭式 ①`TargetPropDeficitDeriv`：$\forall T>0$，$\mathrm{HasDerivAt}\,\delta\,(\delta'(T))\,T$，$\delta'=-\left(w'h+w\mathrm{sech}^2\frac1{2T}/(2T^2)\right)/h^2$（$h'=-\mathrm{sech}^2\frac1{2T}/(2T^2)$ 自证）；②`TargetPropDeficitDerivPos`：$\delta'>0$——等价核不等式 $S\,w<2T^2h\lvert w'\rvert$，两端写成积分后在 $u\in(0,1)$ 上逐点比较等价于 $\sinh(2uV)\le u\sinh(2V)$，即 $\sinh(us)\le u\sinh s$，由 $F(s)=\sinh s/s$ 严格增（$F'=\frac{s\cosh s-\sinh s}{s^2}>0\iff\tanh s<s$，203 已证）给出；$u=1$ 处恰取等，故非负覆盖 $u=1$、严格点取 $u=1/2$（`integral_pos` 的 `Ioc` 论域正好匹配）；③`TargetPropDeficitStrictMono`：$0<T_1<T_2\Rightarrow\delta(T_1)<\delta(T_2)$（`strictMonoOn_of_deriv_pos`）；④`TargetPropDeficitRatioStrictMonoT`：$0<T_1<T_2\Rightarrow R(\delta(T_1))<R(\delta(T_2))$（由 ②③ 把 $(0,\infty)$ 映入 $(0,1)$ 后复合 203 的 $R$ 单增）。**判定**：$\Phi'$ 降为 $\delta'$ 的推论；$\delta$ 侧单调性从数值升为无条件定理 | Spec **v31**（增 `deficitDeriv`／`TargetPropDeficitDeriv`／`TargetPropDeficitDerivPos`／`TargetPropDeficitStrictMono`／`TargetPropDeficitRatioStrictMonoT`）；`05_Lean验证/Ring15LockDeficitMono.lean`（4 条＋私有 `continuous_tanh`／`cont_sechSq`／`sechSq_pos`／`sechSq_le_one`／`hasDerivAt_tanh`／`tanh_lt_self`／`sinh_ratio_deriv`／`sinh_ratio_strictMono`／`sinh_smul_lt`／`sinh_smul_le`／`point_gt_core`／`point_ge_core`／`point_gt_T`／`point_ge_T`／`key_integral`／`shapeH_pos`／`deficit_eq`／`deficit_pos`／`deficit_lt_one`／`hasDerivAt_shapeH`／`hasDerivAt_deficit`）；卡 §三十七；`04_计算验证/环15_δ导数与核不等式_数值核对.py|_输出.txt|环15_δ导数与核不等式_数值核对.png` | A 闸**三十一模块 PASS**（31/31 编译、69 条 axioms 全为 `{propext, Classical.choice, Quot.sound}`、64 条 `#check` 全 `[ ok ] type: … : Spec.…`、260 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 三十一模块 v31）`）；B 闸判**定义式**（最可能跑偏行：`hasDerivAt_deficit` 的 `hval`——`0 + -(q) = deficitDeriv` 若丢了 `shapeH T ^ 2 ≠ 0` 的侧条件，`field_simp` 仍能凑出"像样"等式而两侧差一个符号；本轮显式给 `hhne`／`hh2`，并以 $\delta'$ 闭式与中心差分一致到 $10^{-11}$ 作外部锚） | `审-6` 仍未闭合；G-188b-2i 的 **$\delta$ 侧（闭式＋正性＋两处严格单增）收口**，"$\Phi'$ 未进 Lean"消解；余 **G-188b-2i 的交点编址**（$\delta'$ 与 $\lambda'$ 的显式比较：$\frac{d}{dT}(R-\lambda)$ 只在 $T\approx0.19415$ 变号一次，未成定理）；数值旁证 $\delta'$ 闭式 vs 差分 rel $3.1\times10^{-11}\sim1.2\times10^{-9}$、$\delta'$ 最小 $0.012499$、负值点 0、核比最大 $0.955319$（余量 $2.90\times10^{-2}$）、点位不等式 0 违反、$T_{\min}=0.343857873$ 不变 |



| 203 | 15/`审-6` | **判据两侧的单调性（G-188b-2h 前件）**。202 把判据换成 $\lambda(T)$ 与 $R(\delta)$ 的比较后，缺的是两侧各自可读。三件构造：①$R(\delta)$ 在 $(0,1)$ **严格单增**——$R(b)-R(a)=\frac{(b-a)(1+a+b-ab)}{(1-a)(1-b)}$，分子三因子皆正，**纯代数、不读 $\Phi'$**（202 撤销"$\Phi$ 单调性可判 $G$"后右端单增仍可独立拿到）；②$\lambda$ **严格单增**——令 $s=1/T$、$F(s)=s/\sinh s$，$F'(s)=\frac{\cosh s(\tanh s-s)}{\sinh^2s}<0$ 由 $\tanh s=\int_0^s\mathrm{sech}^2=1-\int_0^s\tanh^2$ 即 $s-\tanh s=\int_0^s\tanh^2>0$ 给出，$T\mapsto1/T$ 严格减 ⇒ 复合单增，**全程不经过 $\Phi$、不经过 $w$**；③$0<\lambda<1$——$0<s<\sinh s$ ⇒ $s/\sinh s\in(0,1)$，给远区一条硬界：$R(\delta)$ 随 $\delta\to1^-$ 发散可越 1，$\lambda$ 永不可越 1。同时判明**两侧同增不足以定交点**（须比较 $\frac{d\lambda}{dT}$ 与 $\frac{dR}{dT}=R'(\delta)\delta'(T)$，而 $\Phi'$ 未进链） | Spec **v30**（增 `deficitRatio`／`TargetPropDeficitRatioMono`／`TargetPropLambdaStrictMono`／`TargetPropLambdaBounds`）；`05_Lean验证/Ring15LockLambda.lean`（3 条＋私有 `cont_sechSq`／`sechSq_pos`／`sechSq_le_one`／`hasDerivAt_tanh`／`tanh_lt_self`／`self_lt_sinh`／`shapeF`／`F_deriv`／`F_strictAnti`）；卡 §三十六；`04_计算验证/环15_判据两侧单调性_数值核对.py|_输出.txt|环15_判据两侧单调性_交点与增速.png` | A 闸**三十模块 PASS**（30/30 编译、65 条 axioms 全为 `{propext, Classical.choice, Quot.sound}`、60 条 `#check` 全 `[ ok ] type: … : Spec.…`、259 文件 0 命中、exit 0，末行 `A 闸 PASS（限环 15 三十模块 v30）`）；B 闸判**定义式**（最可能跑偏行：`tanh_lt_self` 里 $s-\tanh s=\int_0^s\tanh^2$ 的**符号与严格性交代**——若只写 $\tanh s\le s$ 或漏 $s>0$，得到的是"$\lambda$ 不增"这一近似命题；本轮以 $s>0$ 与 $\int_0^s\tanh^2>0$ 显式给严格） | `审-6` 仍未闭合；G-188b-2h 的 (i)(ii)＋值域**闭合成三条定理**；余 **G-188b-2i**（交点 $T_{\min}$ 编址：需增速比较或 $\delta(T)$ 链内单调＋显式包络，$\Phi'$ 未进 Lean 是阻塞处）；数值旁证 $R$ 闭式差相对误差 0、$\lambda$ 单增 3001 点全正、闭式 rel err $6.50\times10^{-16}$、$0<\lambda<1$ 违反 0 点、$d\lambda/dT-dR/dT$ 在 $(0.03,1.5)$ 只变号一次（$T\approx0.19415$）、$\lambda-R$ 变号区间 $(0.3436,0.34409)$、二分得 $T_{\min}=0.343857873$ |



- **入库状态（第 201 轮）**：本地提交（十三文件：Spec v28＋`LockUnary`＋两 README＋审计＋账本＋口径表＋主卡＋决策记录＋文献卡＋数值核对）；**推送未完成**——当前网络下 GitHub 传输 <1 KB/s（`git push` 报 `GnuTLS recv error (-110)` 与 `Operation too slow`；WSL 侧无可用代理、Windows 未开系统代理），待网络恢复后重试；本地工作区与该提交一致，不影响续跑。

- **入库状态（第 203 轮）**：按用户"不用推送，先研究"的明确指令，本轮**零 git 操作**（本地 `c21ba9d` 仍领先 `origin/main` 一个提交、待网络恢复后补推）。

- **入库状态（第 204 轮）**：按用户"不用推送，先研究"的明确指令，本轮**零 git 操作**（本地 `c21ba9d` 仍领先 `origin/main` 一个提交、待网络恢复后补推）。本轮改动：`Ring15Spec.lean`（v31）、新模块 `Ring15LockDeficitMono.lean`、`a_gate.ps1`（三十一模块 v31）、卡 §三十七、本文件、`DISCARD.md`、`00_当前有效口径表.md`、审计日志 §三十六、两 README 的 204 节、决策记录`第204轮`、数值脚本＋输出＋图各一。

- **入库状态（第 205 轮）**：按用户"不用推送，先研究"的明确指令，本轮**零 git 操作**（本地 `c21ba9d` 仍领先 `origin/main` 一个提交、待网络恢复后补推）。本轮改动：`Ring15Spec.lean`（v32）、新模块 `Ring15LockGapDeriv.lean`、`a_gate.ps1`（三十二模块 v32）、卡 §三十八、本文件、`DISCARD.md`、`00_当前有效口径表.md`、审计日志 §三十七、两 README 的 205 节、决策记录`第205轮`、数值脚本＋输出＋图各一。- **入库状态（第 209 轮）**：按用户"不用推送，先研究"的明确指令，本轮**零 git 操作**（本地 `c21ba9d` 仍领先 `origin/main` 一个提交、待网络恢复后补推）。本轮改动：`Ring15Spec.lean`（v34，+2 条 `def … : Prop`）、新模块 `Ring15LockTailRatio.lean`（2 定理＋2 私有引理）、`a_gate.ps1`（三十四模块 v34、76 axioms、72 `#check`）、卡 §四十二、本文件、`00_当前有效口径表.md`、审计日志 §四十一、两 README 的 209 节、决策记录`第209轮`。无新数值脚本、无新图（本轮为纯代数合成，不产生曲线）。- **入库状态（第 210 轮）**：按用户"不用推送，先研究"的明确指令，本轮**零 git 操作**（本地 `c21ba9d` 仍领先 `origin/main` 一个提交、待网络恢复后补推）。本轮改动：`Ring15Spec.lean`（v35，+3 条 `def … : Prop`）、新模块 `Ring15LockSecant.lean`（3 定理＋4 私有引理）、`a_gate.ps1`（三十五模块 v35、79 axioms、75 `#check`）、卡 §四十三、本文件、`DISCARD.md`（210-1）、`00_当前有效口径表.md`、审计日志 §四十二、两 README 的 210 节、决策记录`第210轮`。无新数值脚本、无新图。



- **入库状态（第 211 轮）**：按用户"不用推送，先研究"的明确指令，本轮**零 git 操作**（本地 `c21ba9d` 仍领先 `origin/main` 一个提交、待网络恢复后补推）。本轮改动：`Ring15Spec.lean`（v36，+3 条 `def … : Prop`）、新模块 `Ring15LockNearZero.lean`（3 定理＋11 私有引理）、`a_gate.ps1`（三十六模块 v36、82 axioms、78 `#check`）、卡 §四十四、本文件、`00_当前有效口径表.md`、审计日志 §四十三、两 README 的 211 节、决策记录`第211轮`、数值脚本＋输出＋图各一（`环15_近零端界_*`）；`DISCARD.md` 新增 211-1（"$D'/D$ 首项展开"未采用，附条件与依据）。

- **入库状态（第 212 轮）**：按用户"不用推送，先研究"的明确指令，本轮**零 git 操作**（本地 `c21ba9d` 仍领先 `origin/main` 一个提交、待网络恢复后补推）。本轮改动：`Ring15Spec.lean`（v37，+1 条 `def … : Prop`）、新模块 `Ring15LockZeroExists.lean`（约 45 行、1 定理）、`a_gate.ps1`（三十七模块 v37）、主卡 §四十五、本账本（§〇 基线／§一 G-188b-2k／§二 212 行／§五 A 闸＋停点＋本条）、`00_当前有效口径表.md` §212、`audit_log_环15_2026-11-25.txt` §四十四、两 README 212 节、决策记录 `06_决策记录/2026-11-26_第212轮_零点存在性.md`。

- **入库状态（第 213 轮）**：按用户"不用推送，先研究"的明确指令，本轮**零 git 操作**（本地 `c21ba9d` 仍领先 `origin/main` 一个提交、待网络恢复后补推）。本轮改动：`Ring15Spec.lean`（v38，+1 `def` ＋1 条件 `def … : Prop`）、新模块 `Ring15LockZeroUnique.lean`（约 50 行、1 定理＋1 私有）、`a_gate.ps1`（三十八模块 v38）、主卡 §四十六、本账本（§〇 基线／§一 G-188b-2k／§二 213 行／§五 A 闸＋停点＋本条）、`00_当前有效口径表.md` §213、`audit_log_环15_2026-11-25.txt` §四十五、两 README 213 节、决策记录 `06_决策记录/2026-11-26_第213轮_零点唯一性条件句.md`、数值脚本＋输出＋图（`环15_唯一性可行性_*`）；`DISCARD.md` 新增 213-1（"$D'$ 左正右负分段"未采用，附条件与依据）。

- **入库状态（第 214 轮）**：按用户"不用推送，先研究"的明确指令，本轮**零 git 操作**（本地 `c21ba9d` 仍领先 `origin/main` 一个提交、待网络恢复后补推）。本轮改动：`Ring15Spec.lean`（v39，+2 条 `def … : Prop`）、新模块 `Ring15LockRatioForm.lean`（约 55 行、2 定理＋1 私有）、`a_gate.ps1`（三十九模块 v39，`$mods`／imports／axioms 87／`#check` 82／头注／末行同步）、主卡 §四十七、本账本（§〇 基线 v39＋PASS／§一 G-188b-2k 补 214 句／§二 214 行／§五 A 闸＋停点＋本条）、`00_当前有效口径表.md` §214、`audit_log_环15_2026-11-25.txt` §四十六、两 README 214 节、决策记录 `06_决策记录/2026-11-27_第214轮_Q与R正性.md`；`DISCARD.md` 新增 214-1（$Q$ 乘法闭式未入 Spec：证明路径限制＋保留条件）。无新数值脚本、无新图（正性为纯符号结论，不画曲线）。

- **临时件清理（第 214 轮）**：`_agate214.log`／`_agate214.err`／`_a_gate_out.txt`／`_a_gate_scan.txt`／`_chk214.lean`／`_chk214.out` 已删净（`olean_tmp` 内 39 个 olean 保留）。



- **A 闸（第 215 轮，四十模块）**：Spec v40 变更使全部下游 olean 失效，按依赖序重编 40 个模块后跑全闸，**PASS**：40/40 编译 ok（含新模块 `Ring15LockDeficitUb`）、90 条 `#print axioms` 全部落在白名单（87 条 `{propext, Classical.choice, Quot.sound}`＋3 条 `{propext, Quot.sound}` 子集）、85 条 `#check` 全 `[ ok ] type: … : Spec.…`（含新增三条 `targetPropDeficitDerivAlt`／`…LtTwoDelta`／`…LtTwoThird`）、`[FAIL` 0、`token: {"files": 269, "hits": []}`、exit 0，末行 `A 闸 PASS（限环 15 四十模块 v40：编译 + axioms 白名单 + 类型对齐 + token 卫生）`。**闸内缺陷与修复（215 记）**：Lean 的 `#print axioms` 在 80 列处折行，原逐行解析把两条折行条目（`LockDeficitMono.targetPropDeficitRatioStrictMonoT`、`LockZeroUnique.targetPropGapZeroUniqueOfRatioMono`）整条丢弃，日志只记 88 条 `[ ok ] axioms`；已修 `a_gate.ps1`（拼接续行＋允许空公理集），并用修复后的解析在同一份 `_a_gate_out.txt` 上重放复核为 **90/90 白名单、85/85 类型对齐**（216 起由脚本原生覆盖）。

- **本环停点（第 215 轮）**：环 15／`审-6`；缺口 **G-188b-2k-u**（$Q$ 严格单增／$\lambda'R>\lambda R'\delta'$）**仍未证**。本轮把它的右端 $\delta'$ 从"含积分 $|w'|$"降为有理闭式并给出两条严格上界：$\delta'=\frac{2(h-w)}{Th}-\frac{w\,\mathrm{sech}^2(1/(2T))}{2T^2h^2}$（v40 `deficitDerivAlt`）、$\delta'<\frac{2\delta}{T}$、$\delta'<\frac{2}{3T}$（用 210 的无条件 $\delta\le\frac13$）；`Ring15LockDeficitUb` 3 定理进链，A 闸四十模块 PASS。**但 $1/T$ 级界不足**：$(\ln\lambda)'\sim0.313/T^2$，须 $\delta'$ 为 $1/T^2$ 级才可能压过 $R'/R$ 项 ⇒ 新增**子缺口 G-188b-2k-u-1**（$\delta'\le C/T^2$，$T=1$ 处需 $C\le0.0596$）。**最该修的一处＝$w$ 在 $T\ge1$ 段的定量下界**（减项 $\frac{\Phi\,\mathrm{sech}^2}{2T^2h}$ 的定量下界；链内现只有 $0<w<h$ 与 $w\ge\frac23h$，在 $T=1$ 给 $w\le0.4621$ vs 真值 $0.3167$，精度不足）。依据＝卡 §四十八（四元组／三行代数／B 闸逐问）、`05_Lean验证/Ring15LockDeficitUb.lean`、`a_gate.ps1`（v40）、`04_计算验证/环15_δ上界_输出.txt`（新闭式 vs 中心差分最大相对差 $3.5\times10^{-5}$、$\delta'/(2/3T)$ 最大 $0.271276$）。闭合数 0、编号 37、第 5 层不启动。

- **入库状态（第 215 轮）**：按用户"不用推送，先研究"的明确指令，本轮**零 git 操作**（本地 `c21ba9d` 仍领先 `origin/main` 一个提交、待网络恢复后补推）。本轮改动：`Ring15Spec.lean`（v40，+1 `noncomputable def` ＋3 条 `def … : Prop`）、新模块 `Ring15LockDeficitUb.lean`（约 100 行、3 定理＋5 私有）、`a_gate.ps1`（四十模块 v40，`$mods`／imports／axioms 90／`#check` 85／头注／末行同步；另修折行解析缺陷）、主卡 §四十八、本账本（§〇 基线 v40＋PASS／§一 补 215 句／§二 215 行／§五 A 闸＋停点＋本条）、`00_当前有效口径表.md` §215、`audit_log_环15_2026-11-25.txt` §四十七、两 README 215 节、决策记录 `06_决策记录/2026-11-27_第215轮_δ闭式与上界.md`、数值脚本＋输出＋图 `04_计算验证/环15_δ上界_数值旁证.py`／`_输出.txt`／`_数值旁证.png`。`DISCARD.md` 本轮无新增（Spec 内部形态调整发生在锁定前、无下游消费，只记决策记录）。

- **临时件清理（第 215 轮）**：`_agate215.log`／`_agate215.err`／`_a_gate_out.txt`／`_a_gate_scan.txt`／`_gate_compile.out` 已删净（`olean_tmp` 内 40 个 olean 保留）。



- **本环停点（第 216 轮，第 2 步止）**：环 15／`审-6`；缺口 **G-188b-2k-u**（$Q$ 严格单增）仍未证，且**入口改判**：215 记的"$\delta'\le C/T^2$"被定量否证（$\sup T^2\delta'=0.059019$ vs 可用 $C\le0.0596$，窗口 1%；三阶 $\tanh$ 界给 $C\approx0.1$），入 `DISCARD.md` 216-1。**新入口 G-188b-2k-u-2**＝$G(T)=\lambda'R-\lambda R'\delta'>0$ 的代数判号（精度需求约 10%，与 1% 相比可行）。**最该修的一处＝三件工具引理落 Spec v41**：①`hasDerivAt_tanh`／`tanh_lt_self` 现为 `Ring15LockW`／`Ring15LockDeficitMono` 的私有引理，跨模块不可引用，须提升为 Spec 级公开（Spec 只 import 基线）；②$\tanh$ 的五阶上下界（需 sinh／cosh 级数界，Mathlib 侧未见现成件）；③`sechSq = 1 - tanh^2` 把 $G$ 化成纯 $(T, h)$ 有理式。本轮为纸面＋数值环，未改 Spec、未开模块、未跑闸；A 闸最新结论仍是 v40 四十模块 PASS。依据＝主卡 §四十九（四元组／渐近展开／窗口定量／B 闸预警）、`04_计算验证/环15_δ渐近系数_数值核对.py`／`_输出.txt`。闭合数 0、编号 37、第 5 层不启动。

- **入库状态（第 216 轮）**：按用户"不用推送，先研究"的明确指令，本轮**零 git 操作**（本地 `c21ba9d` 仍领先 `origin/main` 一个提交、待网络恢复后补推）。本轮改动：`04_计算验证/环15_δ渐近系数_数值核对.py`／`_输出.txt`（新）、主卡 §四十九、本账本（§二 216 行／§五 停点＋本条）、`00_当前有效口径表.md` §216、`audit_log_环15_2026-11-25.txt` §四十八、`04_计算验证/README.md` 216 节、`DISCARD.md` 216-1、决策记录 `06_决策记录/2026-11-27_第216轮_δ渐近系数与入口改判.md`。**无 Spec 变更、无新模块、未跑 A 闸**（v40 结论继续有效）；无临时件。


- **A 闸（第 217 轮，四十一模块 v41）**：Spec v41 变更使全部下游 olean 失效，按依赖序重编 41 个模块后跑全闸，**PASS**：41/41 编译 ok（含新模块 `Ring15LockTanhTools`）、99 条 `#print axioms` 全在白名单（含新 9 条 `LockTanhTools` 定理，均为 `{propext, Classical.choice, Quot.sound}`）、86 条 `#check` 全 `[ ok ] type: … : Spec.…`（新增 `targetPropTanhCubic : Spec.TargetPropTanhCubic`）、`[FAIL` 0、`token: {"files": 270, "hits": []}`、exit 0，末行 `A 闸 PASS（限环 15 四十一模块 v41：编译 + axioms 白名单 + 类型对齐 + token 卫生）`。折行解析修复（215 记）本轮原生覆盖，日志 99 条 axioms 无遗漏（修复前同场景会丢 2 条）。
- **本环停点（第 217 轮）**：环 15／`审-6`；缺口 **G-188b-2k-u**（$Q$ 严格单增）仍未证。本轮把它的**工具层**落地：Spec v41 `TargetPropTanhCubic` ＋ `Ring15LockTanhTools`（9 条定理，原私有件公开化），A 闸四十一模块 PASS。**三阶界不够用（本轮最硬结论）**：逐点代入后 $\frac wh\ge\frac ws=\frac23-\frac{1}{30T^2}$ ⇒ $\delta\le\frac13+\frac{1}{30T^2}$（方向错，$T\to\infty$ 松于 $\frac13$，数值上 $T=1$ 给 $0.3667$ vs 真值 $0.3124$）；差的正号来自 $\frac{s-h}{s}\approx\frac1{12T^2}$。**最该修的一处＝$h$ 的五阶上界** $\tanh s\le s-\frac{s^3}{3}+\frac{2s^5}{15}$（须自建 sinh／cosh 级数余项的符号控制），与 $w$ 的五阶下界合用才能得 $\delta\le\frac13-\frac{c}{T^2}$（218 靶）。依据＝主卡 §五十（四元组／三阶推导／为何不够／B 闸）、`05_Lean验证/Ring15LockTanhTools.lean`、`04_计算验证/环15_tanh三阶界_输出.txt`。闭合数 0、编号 37、第 5 层不启动。
- **入库状态（第 217 轮）**：按用户"不用推送，先研究"的明确指令，本轮**零 git 操作**（本地 `c21ba9d` 仍领先 `origin/main` 一个提交、待网络恢复后补推）。本轮改动：`Ring15Spec.lean`（v41，+1 `def`）、新模块 `Ring15LockTanhTools.lean`（约 150 行、9 定理）、`a_gate.ps1`（四十一模块 v41：`$mods`／imports／axioms 99／`#check` 86／头注／末行）、主卡 §五十、本账本（§〇 基线 v41＋PASS／§二 217 行／§五 A 闸＋停点＋本条）、`00_当前有效口径表.md` §217、`audit_log_环15_2026-11-25.txt` §四十九、两 README 217 节、决策记录 `06_决策记录/2026-11-27_第217轮_纯工具环_三阶下界.md`、数值脚本＋输出 `04_计算验证/环15_tanh三阶界_数值核对.py`／`_输出.txt`。`DISCARD.md` 本轮无新增。
- **临时件清理（第 217 轮）**：`_agate217.log`／`_agate217.err`／`_a_gate_out.txt`／`_a_gate_scan.txt`／`_gate_compile.out`／`_chk217.lean` 已删净（`olean_tmp` 内 41 个 olean 保留）。

- **A 闸（第 218 轮，四十二模块 v42）**：Spec 加 `TargetPropTanhQuintic` 后全链失效，按依赖序重编 42 模块并跑全闸，**PASS**：42/42 编译 ok（含新模块 `Ring15LockTanhQuintic`）、101 条 `#print axioms` 全在白名单（新增 `LockTanhQuintic.tanhQuintic`、`…targetPropTanhQuintic` 均 `{propext, Classical.choice, Quot.sound}`）、87 条 `#check` 全 `[ ok ] type: … : Spec.…`（新增 `targetPropTanhQuintic : Spec.TargetPropTanhQuintic`）、FAIL 0、`token: {"files": 271, "hits": []}`、exit 0，末行 `A 闸 PASS（限环 15 四十二模块 v42：编译 + axioms 白名单 + 类型对齐 + token 卫生）`。
- **本环停点（第 218 轮）**：环 15／`审-6`；缺口 **G-188b-2k-u**（$Q$ 严格单增）仍未证。本轮把 217 缺的 "h 的上界" 落地：Spec v42 `TargetPropTanhQuintic` ＋ `Ring15LockTanhQuintic`（2 条定理），A 闸四十二模块 PASS。**关键手法**：不用 Taylor 余项符号，用 "三阶界平方后积分"，把 $t^6/9$ 单向丢掉。**最该修的一处＝219 的合成**：$w\ge\frac{1}{3T}-\frac{1}{60T^3}$（三阶）与 $h\le s-\frac{s^3}{3}+\frac{2s^5}{15}$（五阶，$s=\frac1{2T}$）合成 $\delta\le\frac13-\frac{c}{T^2}$，常数取 $c=0.018$（数值 $c(T)$ 在 $T\ge1$ 上由 0.018018 升至 0.022221，$T\to\infty$ 趋 $\frac1{45}$）。依据＝主卡 §五十一（四元组／推导／B 闸）、`05_Lean验证/Ring15LockTanhQuintic.lean`、`04_计算验证/环15_tanh五阶界_输出.txt`。闭合数 0、编号 37、第 5 层不启动。
- **入库状态（第 218 轮）**：按用户 "不用推送，先研究" 的明确指令，本轮**零 git 操作**（本地 `c21ba9d` 仍领先 `origin/main` 一个提交、待网络恢复后补推）。本轮改动：`Ring15Spec.lean`（v42，+1 `def`）、新模块 `Ring15LockTanhQuintic.lean`（`tanhQuintic`＋对齐定理）、`a_gate.ps1`（四十二模块 v42：`$mods`／imports／axioms 101／`#check` 87／头注／末行）、主卡 §五十一、本账本（§〇 基线 v42＋PASS／§二 218 行／§五 四条）、`00_当前有效口径表.md` §218、`audit_log_环15_2026-11-25.txt` §五十、两 README 218 节、决策记录 `06_决策记录/2026-11-27_第218轮_tanh五阶上界.md`、数值脚本＋输出 `04_计算验证/环15_tanh五阶界_数值核对.py`／`环15_tanh五阶界_输出.txt`。`DISCARD.md` 本轮无新增。
- **临时件清理（第 218 轮）**：`_agate218.log`／`_agate218.err`／`_a_gate_out.txt`／`_a_gate_scan.txt`／`_gate_compile.out`／`_chk218.lean` 待删（`olean_tmp` 内 42 个 olean 保留）。
- **A 闸（第 219 轮，四十三模块 v43）**：Spec 加 `TargetPropDeficitLeThirdSubSq` 后按依赖序重编 43 模块并跑全闸，**PASS**：43/43 编译 ok（含新模块 `Ring15LockDeficitSq`）、103 条 `#print axioms` 全在白名单（新增 `LockDeficitSq.deficitLeThirdSubSq`、`…targetPropDeficitLeThirdSubSq` 均 `{propext, Classical.choice, Quot.sound}`）、88 条 `#check` 全 `[ ok ] type: … : Spec.…`、FAIL 0、`token: {"files": 272, "hits": []}`、exit 0，末行 `A 闸 PASS（限环 15 四十三模块 v43：编译 + axioms 白名单 + 类型对齐 + token 卫生）`。
- **本环停点（第 219 轮）**：环 15／`审-6`；缺口 **G-188b-2k-u**（$Q$ 严格单增）仍未证。本轮把 $\delta$ 的上界从 $\frac13$ 收紧为 $\frac13-\frac{9}{500T^2}$（$T\ge1$），A 闸四十三模块 PASS。**最该修的一处＝220 的 $G$ 判号**：现已有 $\delta\le\frac13-\frac{c}{T^2}$（$c=0.018$）、$\delta'<\frac{2}{3T}$、$\lambda<\frac{T^2}{3}$（$T\le\frac1{10}$ 段）与 $\lambda=1/(T\sinh\frac1T)$；$G=\lambda'R-\lambda R'\delta'>0$ 需把三项在同一 $T$ 段上化成显式比较（$R'(\delta)\le\frac{1+2/3-1/9}{(1-\delta)^2}$ 与 $(1-\delta)\ge\frac23+\frac{c}{T^2}$ 两条并用），精度需求约 $10\%$（$(\ln Q)'$ 最小 $0.098536$ 于 $T=1$）。依据＝主卡 §五十二、`05_Lean验证/Ring15LockDeficitSq.lean`、`04_计算验证/环15_δ减平方界_输出.txt`。闭合数 0、编号 37、第 5 层不启动。
- **入库状态（第 219 轮）**：按用户"不用推送，先研究"的指令，本轮**零 git 操作**（本地 `c21ba9d` 仍领先 `origin/main` 一个提交）。改动：`Ring15Spec.lean`（v43，+1 `def`）、新模块 `Ring15LockDeficitSq.lean`、`a_gate.ps1`（43 模块 v43）、主卡 §五十二、本账本（§〇 基线 v43＋PASS／§二 219 行／§五 四条）、口径表 §219、审计日志 §五十一、两 README 219 节、决策记录 `06_决策记录/2026-11-27_第219轮_δ减平方界.md`、数值脚本＋输出 `04_计算验证/环15_δ减平方界_数值核对.py`／`_输出.txt`。`DISCARD.md` 本轮无新增。
- **临时件清理（第 219 轮）**：`_agate219.log`／`_agate219.err`／`_a_gate_out.txt`／`_a_gate_scan.txt`／`_gate_compile.out` 待删（`olean_tmp` 内 43 个 olean 保留）。
- **A 闸（第 220 轮）**：纸面环，**无新增条目**——不改 Spec、不建模块、不跑闸；Spec 仍 v43、模块仍四十三、闸内仍 103 axioms／88 `#check`（第 219 轮 PASS 记录有效）。
- **本环停点（第 220 轮）**：环 15／`审-6`；缺口 **G-188b-2k-u**（$Q$ 严格单增）未证。本轮产出判据的 $h$-闭式：$(\ln Q)'=\frac{1+h^2-2Th}{2T^2h}-\delta'W$，并定量化判号允许域（$\delta'$ 上界 $\le1.43$–$1.46$ 倍真值，$T\ge0.1$）。**最该修的一处＝221 的七阶 $\tanh$ 双界**：$s-\frac{s^3}{3}+\frac{2s^5}{15}-\frac{17s^7}{315}\le\tanh s\le s-\frac{s^3}{3}+\frac{2s^5}{15}-\frac{17s^7}{315}+\frac{62s^9}{2835}$（$0\le s\le1$），把 $w,h$ 压到 $O(T^{-7})$，$\delta'$ 的界才进 $1.4$ 倍。依据＝主卡 §五十三、`04_计算验证/环15_判据h闭式_输出.txt`。闭合数 0、编号 37、第 5 层不启动。
- **入库状态（第 220 轮）**：零 git 操作（"不用推送，先研究"）。改动：主卡 §五十三、本账本（§二 220 行／§五 三条）、口径表 §220、审计日志 §五十二、两 README 220 节、决策记录 `06_决策记录/2026-11-27_第220轮_判据h闭式.md`、数值脚本＋输出 `04_计算验证/环15_判据h闭式_数值核对.py`／`_输出.txt`。`DISCARD.md` 无新增。
- **临时件清理（第 220 轮）**：`04_计算验证/__pycache__` 已清；`05_Lean验证` 无本轮临时件。

- **A 闸（第 221 轮，四十四模块 v44）**：Spec 加 `TargetPropTanhSepticLower` 后按依赖序重编 44 模块并跑全闸，**PASS**：44/44 编译 ok（含新模块 `Ring15LockTanhSeptic`）、105 条 `#print axioms` 全在白名单（新增 `LockTanhSeptic.tanhSepticLower`、`…targetPropTanhSepticLower` 均 `{propext, Classical.choice, Quot.sound}`）、89 条 `#check` 全 `[ ok ] type: … : Spec.…`、FAIL 0、`token: {"files": 274, "hits": []}`、exit 0，末行 `A 闸 PASS（限环 15 四十四模块 v44：编译 + axioms 白名单 + 类型对齐 + token 卫生）`（实跑约 45 分钟）。
- **本环停点（第 221 轮）**：环 15／`审-6`；缺口 **G-188b-2k-u**（$Q$ 严格单增）未证。本轮把七阶 $\tanh$ **下界**落地：Spec v44 `TargetPropTanhSepticLower` ＋ `Ring15LockTanhSeptic`（4 条定理），A 闸四十四模块 PASS。**关键手法**：$\tanh s=s-\int_0^s\tanh^2$、$\tanh^2\le S^2$（$S$＝v42 五阶上界），$S^2$ 只丢一个非正项即得 $s^3/3-2s^5/15+17s^7/315$，故 $\tanh s\ge s-\frac{s^3}{3}+\frac{2s^5}{15}-\frac{17s^7}{315}$。**最该修的一处（222 的入口）＝七阶上界 $S_4=S_3+\frac{62s^9}{2835}$**：须由其后再平方积分（$\tanh^2\ge P^2$）合成 $w$ 的上界与 $h$ 的上界，才能与 219 的 $\delta$ 上界接成 $O(T^{-7})$ 的双侧界；数值已核七阶双界的 $\delta'$ 上界占 220 允许域 $68\%$–$70\%$（余量 1.44），够用。**同时登记新缺口 G-188b-2k-u-2a**：$T<\frac12$ 时 $s>1$、多项式界失效，且粗界 $\frac{2\delta}{T}$ 在 $T=0.30/0.40/0.45$ 越允许域，须另立第三条估计。依据＝主卡 §五十四（含两张精度表与 B 闸逐问）、`05_Lean验证/Ring15LockTanhSeptic.lean`、`04_计算验证/环15_七阶双界_输出.txt`。闭合数 0、编号 37、第 5 层不启动。
- **入库状态（第 221 轮）**：按用户"不用推送，先研究"的指令，本轮**零 git 操作**（本地 `c21ba9d` 仍领先 `origin/main` 一个提交）。改动：`Ring15Spec.lean`（v44，+1 `def`）、新模块 `Ring15LockTanhSeptic.lean`、`a_gate.ps1`（44 模块 v44：105 axioms／89 `#check`）、主卡 §五十四、本账本（§〇 基线 v44＋PASS／§二 221 行／§五 四条）、口径表 §221（并修正 §220 的方向写法）、审计日志 §五十三、两 README 221 节、决策记录 `06_决策记录/2026-11-27_第221轮_七阶tanh下界.md`、数值脚本＋输出 `04_计算验证/环15_七阶双界_数值核对.py`／`_输出.txt`。`DISCARD.md` 新增 **221-1**（220 双界方向写反，先记后改）。
- **临时件清理（第 221 轮）**：`_agate221.log`／`_agate221.err`／`_a_gate_out.txt`／`_a_gate_scan.txt`／`_chk221.lean` 已删；`04_计算验证/__pycache__` 已清（`olean_tmp` 内 44 个 olean 保留）。
- **A 闸（第 222 轮，四十五模块 v45）**：Spec 加 `TargetPropTanhSeptic` 后按依赖序重编 45 模块并跑全闸，**PASS**：45/45 编译 ok（含新模块 `Ring15LockTanhSepticUb`）、107 条 `#print axioms` 全在白名单（新增 `LockTanhSepticUb.tanhSepticUpper`、`…targetPropTanhSeptic` 均 `{propext, Classical.choice, Quot.sound}`）、90 条 `#check` 全 `[ ok ] type: … : Spec.…`、FAIL 0、`token: {"files": 275, "hits": []}`、exit 0，末行 `A 闸 PASS（限环 15 四十五模块 v45：编译 + axioms 白名单 + 类型对齐 + token 卫生）`。
- **本环停点（第 222 轮）**：环 15／`审-6`；缺口 **G-188b-2k-u**（$Q$ 严格单增）未证。本轮把七阶 $\tanh$ **上界**落地：Spec v45 `TargetPropTanhSeptic` ＋ `Ring15LockTanhSepticUb`（3 条定理），A 闸四十五模块 PASS。**七阶双界已完整进链**（$S_3\le\tanh s\le S_4$，$0\le s\le1$，两条独立定理、两个模块），$w,h$ 的双向误差数值为 $O(T^{-7})$（$T=1$ 约 $10^{-4}$、$T=5$ 约 $10^{-11}$）。**最该修的一处（223 的入口）＝把双侧界合成 $\delta'$ 上界并与 $(\ln Q)'$ 的分子比较**：即证 $\frac{1+h_{\rm lb}^2-2Th_{\rm ub}}{2T^2h_{\rm ub}}\ge\delta'_{\rm ub}W_{\rm ub}$（$T\in[\frac12,1]$），其中 $\delta'_{\rm ub}=\frac{2\delta_{\rm ub}}{T}-\frac{w_{\rm lb}(1-h_{\rm ub}^2)}{2T^2h_{\rm ub}^2}$、$\delta_{\rm ub}=1-\frac{w_{\rm lb}}{h_{\rm ub}}$；数值上 $\delta'$ 上界只占允许域 $68\%$–$70\%$（余量 $\approx1.44$）。依据＝主卡 §五十五（含 B 闸逐问）、`05_Lean验证/Ring15LockTanhSepticUb.lean`、`04_计算验证/环15_七阶上界_输出.txt`。闭合数 0、编号 37、第 5 层不启动。
- **入库状态（第 222 轮）**：按用户"不用推送，先研究"的指令，本轮**零 git 操作**（本地 `c21ba9d` 仍领先 `origin/main` 一个提交）。改动：`Ring15Spec.lean`（v45，+1 `def`）、新模块 `Ring15LockTanhSepticUb.lean`、`a_gate.ps1`（45 模块 v45：107 axioms／90 `#check`）、主卡 §五十五、本账本（§〇 基线 v45＋PASS／§二 222 行／§五 四条）、口径表 §222、审计日志 §五十四、两 README 222 节、决策记录 `06_决策记录/2026-11-27_第222轮_七阶tanh上界.md`、数值脚本＋输出 `04_计算验证/环15_七阶上界_数值核对.py`／`_输出.txt`。`DISCARD.md` 新增 **222-1**（$\int\frac{34t^8}{315}$ 首版常数漏乘 $\frac19$）。
- **临时件清理（第 222 轮）**：`_agate222.log`／`_agate222.err`／`_a_gate_out.txt`／`_a_gate_scan.txt`／`_chk222.lean`／`_gate_compile.out` 与 `04_计算验证/__pycache__` 已删（`olean_tmp` 内 45 个 olean 保留）。
- **A 闸（第 223 轮，四十六模块 v46）**：Spec 加 `wGapLowerSeptic`／`wGapUpperSeptic` 与两条 Prop 后按依赖序重编 46 模块并跑全闸，**PASS**：46/46 编译 ok（含新模块 `Ring15LockWGapSeptic`）、109 条 `#print axioms` 全在白名单（新增 `LockWGapSeptic.wGapLowerBound`、`…targetPropWGapUpperBound` 均 `{propext, Classical.choice, Quot.sound}`）、91 条 `#check` 全 `[ ok ] type: … : Spec.…`（新增 `targetPropWGapUpperBound : Spec.TargetPropWGapUpperBound`）、FAIL 0、`token: {"files": 276, "hits": []}`、exit 0，末行 `A 闸 PASS（限环 15 四十六模块 v46：编译 + axioms 白名单 + 类型对齐 + token 卫生）`。
- **本环停点（第 223 轮）**：环 15／`审-6`；缺口 **G-188b-2k-u**（$Q$ 严格单增）未证。本轮把 $w$ 的**七阶双侧界**落地：Spec v46 两 def＋两 Prop ＋ `Ring15LockWGapSeptic`（6 条定理），A 闸四十六模块 PASS。**关键手法**：双界沿权 $2u\ge0$ 传到积分（`integral_mono_on`），两支闭式逐项 `integral_pow`；侧条件 $T\ge\frac12$ 由 $\frac{u}{2T}\le\frac{1}{2T}\le1$ 显式给出，不可去。**本环最硬结论（判号域）**：正确复合上界 $\delta'_{\rm ub}=\frac{2(h_{\rm ub}-w_{\rm lb})}{T h_{\rm lb}}-\frac{w_{\rm lb}(1-h_{\rm ub}^2)}{2T^2h_{\rm ub}^2}$ 在 $[0.5,1]$ 上 $\sup\delta'_{\rm ub}/\delta'=1.46338$、$[1,5]$ 上 $1.00319$；判号充分条件 $A_{\rm lb}\ge\delta'_{\rm ub}W_{\rm ub}$ 于 $T\ge\frac12$ **全域成立**，最小比值 $1.08009$（$T=0.5$），渐近 $\frac{10}{7}$。**最该修的一处（224 的入口）＝把该不等式化成单项正系数有理不等式并在 Lean 证**（$T\ge\frac12$，可用变量 $x=1/T$）；$T\in[\frac1{10},\frac12)$ 段仍空（G-188b-2k-u-2a）。依据＝主卡 §五十六、`05_Lean验证/Ring15LockWGapSeptic.lean`、`04_计算验证/环15_w七阶双侧界_输出.txt`。闭合数 0、编号 37、第 5 层不启动。
- **入库状态（第 223 轮）**：按用户"不用推送，先研究"的指令，本轮**零 git 操作**（本地 `c21ba9d` 仍领先 `origin/main` 一个提交）。改动：`Ring15Spec.lean`（v46，+2 def＋2 Prop）、新模块 `Ring15LockWGapSeptic.lean`（6 定理）、`a_gate.ps1`（46 模块 v46：109 axioms／91 `#check`，并修复 `type` 判定分支的编辑事故）、主卡 §五十六、本账本（§〇 基线 v46＋PASS／§二 223 行／§五 四条）、口径表 §223、审计日志 §五十五、两 README 223 节、决策记录 `06_决策记录/2026-11-27_第223轮_w七阶双侧界.md`、数值脚本＋输出 `04_计算验证/环15_w七阶双侧界_数值核对.py`／`_输出.txt`。`DISCARD.md` 新增 **223-1**（$\delta'_{\rm ub}$ 复合式重复扣减）、**223-2**（闸脚本 `type` 分支被覆盖）。
- **临时件清理（第 223 轮）**：`_agate223.log`／`_agate223.err`／`_agate223b.log`／`_agate223b.err`／`_a_gate_out.txt`／`_a_gate_scan.txt`／`_chk223.lean`／`_gate_compile.out` 与 `04_计算验证/__pycache__` 已删（`olean_tmp` 内 46 个 olean 保留）。