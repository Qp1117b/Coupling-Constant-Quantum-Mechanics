# 超导第一性研究

本目录是 `10 探索` 下的独立综合研究工作区。它只组织**文献、推导工作台、计算、Lean 索引、决策记录与数据接口**；权威推导链仍写回 `10 探索/CQM_探索_推导链.md`，不另立平行链，也不改动 `01–07` 与 `08` 的既有口径。

## 研究目标

在现有 27 环超导发生学骨架上，按物理学家式的工作流做第一性模型研究：

1. 先调研外部文献，区分“外部已证结论”“外部标准工具”“CQM 构造假设”；
2. 从骨架逐环重写方程与映射，发现符号、量纲、次序或适用域不对时，有依据地回改；
3. 每一环的改动先在 `03_推导工作台` 写清前件、方程、量纲、极限、可证伪条件，再进 Lean；
4. 全部环拉通后才进入数据对照与函数图像验证；图像用于检验极限、单调性、量级与符号，不用于拟合；
5. 确认的结论写入本目录与主链；被否证的草稿从工作台删除，只在 `06_决策记录` 留下结论、理由与替代路径。

## 目录

| 路径 | 用途 |
|:---|:---|
| `00_研究纲领.md` | 阶段门 S0–S6、每环最小交付、停止条件 |
| `01_文献基线` | 外部文献卡片、arXiv／DOI、可约束的链内环节 |
| `02_缺口重审` | 27 环缺口的分类、优先级、阻断范围与淘汰规则 |
| `03_推导工作台` | 逐环推导草稿；每篇必须有前件、方程、量纲、极限、证伪条件 |
| `04_计算验证` | 独立脚本、数值表、函数图像；不得把拟合曲线当作推导 |
| `05_Lean验证` | 每步对应的 Lean 文件、声明表、构建日志与主库映射 |
| `06_决策记录` | 接受／否决／回改的记录；`成果登记.md` 汇总已承载与未证项；被否决的草稿正文不留在工作台 |
| `07_数据与现象` | 目标数据、实验现象、误差口径与对照协议 |
| `08_框架扩展候选` | 绝对 $T_c$ 闭合的框架扩展候选（命题 Z2 带量纲公设），**非本表任何类别**，不碰权威源 |
| 原 `第一性突破研究/`（已并入各目录） | R1–R42 核心机制推进（$\lambda$ 几何第一性、$T_c\le\min$ 上界、赝能隙判据、FE10、R8 不可能性定理等）：文献已并入 `01_文献基线`、推导→`03_推导工作台`、计算→`04_计算验证`、Lean→`05_Lean验证`、决策→`06_决策记录`（含 `成果登记总表.md`、`README_原第一性突破研究.md`）、数据→`07_数据与现象`；其中 6 项已落地主链、其余候选未落地。原独立目录已删除，不再有平行研究 |

## 当前阶段

**阶段 0：文献基线与缺口重审（已完成）。** 34 张文献卡片、27 环缺口矩阵、P0–P3 顺序与淘汰规则已写入。首轮攻坚锁定环 4 的温度入口，因为它是全链唯一含 $T$ 的环节，且与环 10 的“$\lambda$ 与 $T$ 无关”、环 15 的“$T$ 降则 $p_{\rm sync}$ 升”直接冲突。

**首轮已定位的结构性缺陷（待回改，不是已闭合）**：

- (4.1) 的 $[1+2n_B]$ 使亏角方差随 $T$ **单调增**；
- (10.2) 的刚度却取 $\langle(\Delta\ell)^2\rangle_0$，即零点方差，故 $\lambda$ 与 $T$ 无关；
- (15.1) 又要求 $T$ 降时 $\sigma_\ell$ 升、$p_{\rm pair}$ 升。

三者不能同时成立。若把 (4.1) 的热方差送入 (15.1)，则 $p_{\rm sync}$ 随 $T$ **升**，与超导的低温有序方向相反；若把 (4.1) 只当零点项，则 $T$ 根本不进判据。`审-10` 的“截断位置”只是表层，真正的断口是**温度角色未分层**：$T^*$（局域配对／涨落）与 $T_c$（相位相干／配对不稳定性）被压进同一个入口。

首轮工作台给出这一矛盾的形式化版本，并用 Lean 证明其逻辑后果；修正方案须由链内量给出，未给出前不引入外部因子。

**首轮已交付**：

- 文献基线：29 张卡片，逐条标 arXiv／DOI 与约束环节；
- 缺口重审：27 环矩阵，P0–P3 顺序，5 条淘汰规则；
- 推导工作台：Debye 方差分解 (4.2)–(4.9)、零点／热方差分通道 (3.1)–(3.5)、旧 (15.1) 的否定性判定；
- 计算：`04_计算验证/温度架构.py`、`温度架构.png`、`温度架构.csv`；数值核 $\Theta$ 单调增、相干单调减；
- Lean：`05_Lean验证/ThermalArchitecture.lean`，`lake env lean` 退出码 0，无警告，无禁止项；主库 `lake build` 复核 2902 jobs 通过；
- 核查：`check_consistency` 41/41、`check_provenance` 10/10、`consistency_probe` 0 问题；
- 决策记录：接受“零点进 $\lambda$、热项进 $\Gamma_n$”为工作假设；拒绝“总方差进 $\lambda$／进 $p_{\rm pair}$”和“用 $\omega_{\log}$ 作方差截断”。

**第二轮已交付（S2 前置审计，含一次判定回改）**：

- 发现 06 DM.3 的**全局** A12 与 10 (8.2) 的**逐行** A12 不是同一条件；对称 3×3 反例满足全局零和但 `C1≠1`；
- 结论：`C1=1` 不能由 06 的 A12 推出；环 9 (9.1) 降为“A12 ＋ `C1=1` ＋ 谱分解”的条件式；
- 第一轮把 $C$ 默认成对称矩阵，得到 $N=2,3$ 塌缩；但 (7.3) 的 $f$ 奇性与 $C_{ii}=1$ 不能共用同一个 $f(0)$。正确分解是 $C=I+A$、$A$ 反对称；在此分支 $N=3$ 有满足 A12 的循环矩阵 `C3circ`。Lean `A12Circulation.lean` 已证其存在；
- 但进一步的**最大值 no-go** 证明：若 $C=I+A$、$A_{ij}=f(\varepsilon_i-\varepsilon_j)$、$f$ 奇且严格单调，且 $C\mathbf 1=\mathbf 1$，则取 $\varepsilon$ 最大节点，行和内每一项同号，和为零迫使所有差值 $f=0$，故所有 $\varepsilon$ 相等，$C=I$。这对**任意 $N$** 成立，Lean `sign_odd_row_zero_forces_all_equal` 承载；
- 因此 A12-C 的“单函数 $f$”版本在任意 $N$ 都不存在，$N_{\min}=3/4$ 不能救。`C3circ`／`C4circ` 只是矩阵族示例，不能由奇单调 $f$ 生成（`C3circ_not_from_injective_odd`）；它们满足 A12，但不能接 (7.3) 的 $f^{-1}$。唯一出路是放弃 `C1=1`，或放弃单函数 $f$ 并改写 (7.3)；
- 新增／更新 `03_推导工作台/环08_A12口径断口.md`、`05_Lean验证/A12Counterexample.lean`、`05_Lean验证/A12Circulation.lean`、`04_计算验证/A12_行和.py`／`.png`、`06_决策记录/2026-11-21_A12断口.md`。

**第三轮已交付（S2 矩阵化，方向已定）**：

- 选择“保留 `C1=1` 与全局 A12，放弃单个节点势差 $f(\varepsilon_i-\varepsilon_j)$ 生成”，走矩阵分支；
- 不另造边量，直接取环 5 的 $\lambda_{ij}=\ln r_{ij}$：$C_{ij}=\delta_{ij}+f(\lambda_{ij})$，$B_{ij}=C_{ij}-\delta_{ij}$；
- 前件：矩阵分支把 $\lambda$ 当独立边量，把 \(v_\tau\) 的全局单值性降为局部／零曲率扇区；若坚持全局单值 \(v_\tau\)，则 $\lambda$ 是节点势差、所有闭环和乐为零，矩阵分支不成立，只剩 A12-A。这是对环 5 的候选修正，不是已证；
- 全局 A12 自动成立（$B$ 反对称，成对抵消）；`C1=1` 等价于 $B$ 无散度；梯度—环流分解 $B=d\phi+\omega$；梯度扇区被最大值定理杀死，非平凡解是纯环流；
- 解空间维数（完全图 $K_N$）：$\dim\{B:\ d^*B=0\}=(N-1)(N-2)/2$；梯度子空间只有 $N-1$；一般图用 $E-V+1$。故 `C3circ`（$N=3$）与 `C4circ`（$N=4$）不是孤例；
- 结构后果：**H 非梯度化已否决**。环 5 的 $\lambda$ 属于 \(U(1)\) 和乐侧（相位阻挫），不是固有时历史 \(\mathcal H_{ij}=\tau_i-\tau_j\)；把 $\lambda$ 的环流灌进 H 会破坏 (6.2) 上闭链、T1 单值相位与 (6.5) 方差恒等式。H 保持纯梯度，环 6／T1／环 17 不改；环流改接相位连接 \(\theta=\alpha\lambda\)，$\alpha$ 属 `G19` 未定；
- 环 9 方差改为 $\langle(\delta C_{ij})^2\rangle=2\kappa_f^2\sigma_\varepsilon^2(1-\rho_{ij})+\sigma_\omega^2$（M 分支：`C1=1` 只约束均值）；旧 (9.1) 是 \(\omega=0\) 的梯度扇区；纯环流给常数方差；S 分支（逐样本 `C1=1`）由 Lean `rowZero_decomp_gradient_zero` 只剩 \(\sigma_\omega^2\)；第四轮进一步把 \(\sigma_\varepsilon^2\) 拆成相干 \(V_{\rm coh}\) 与非相干 \(\Theta\)；
- 新交付：`03_推导工作台/环08_A12矩阵化.md`、`05_Lean验证/A12Matrix.lean`（`gradient_row_zero_forces_zero`、`A12_matrix_route_exists_three`／`_four`、`Acirc3_not_gradient`、`Acirc4_not_gradient`；退出码 0、无警告）、`04_计算验证/A12_矩阵化.py`／`.png`／`.csv`／`_维度.csv`；
- 数值：`C3circ`／`C4circ` 梯度部分 0、环流部分 1；梯度对照相反；维数秩核对 $N=3,4,5,6$ 与公式一致；
- 核查：`check_consistency` 41/41、`check_provenance` 10/10、`consistency_probe` 0 问题；08 未改，主库计数仍 124 声明／60 定理。

**第三轮补（环 6 相位审计、环 9 方差分叉）：**

- 发现 06 有两套 \(\mathcal H\)：固有时历史 \(\mathcal H_{ij}=\tau_i-\tau_j\) 与 \(U(1)\) 和乐元素 \(e^{i\theta}\)；环 5 的 $\lambda$ 属后者，不是前者；
- 把 $\lambda$ 环流灌进 H 会破坏 (6.2) 上闭链、T1 单值相位与 (6.5) 方差恒等式，故 **H 非梯度化否决**；H 保持 $\tau_i-\tau_j$，环 6／T1／环 17 不改；
- 环流改接相位连接 \(\theta=\alpha\lambda\)，$\alpha$ 属 `G19` 未定；振幅—相位同源只是候选；
- 新交付：`03_推导工作台/环06_相位连接审计.md`、`05_Lean验证/PhaseConnection.lean`、`04_计算验证/相位连接审计.py`／`.png`／`.csv`、`06_决策记录/2026-11-21_相位连接.md`；文献基线增至 22 卡（L18–L22）；本轮补 L23–L24 至 24 卡；第四轮补 L25–L26 至 26 卡；
- 数值：`|H_loop|=2.7756e-17`（数值零）、`theta3_loop(a=1)=3`、`theta4_loop(a=1)=4`；PhaseConnection 退出码 0、无警告、无禁止项；
- 正规性回改：`A12Normality.lean` 证明任意奇 \(f\) 的 \(C=I+B\) 正规（`skew_normal`、`skew_add_one_normal`、`matrixBranch_normal`、`odd_elementwise_skew`、`matrixBranch_normal_of_odd`）；原先“一般 \(C\) 非正规、需 Schur”的判断删除；正规性只保证均值谱的酉本征基，不能替代 DM.5 的 \(\rho_{ij}\)；数值核 `04_计算验证/A12_正规性.py`／`.png`／`.csv`，五种奇 \(f\) 的正规残差 $\le1.665\times10^{-16}$、`max|Re λ-1|` $\le6.661\times10^{-16}$。
- 环 9 审计：新增 `03_推导工作台/环09_方差与DM5接口.md`；发现 `C1=1` 的均值／逐样本分叉，逐样本分支由 Lean `rowZero_decomp_gradient_zero` 把 DM.5 的节点势差项消掉；上一轮的 \(\rho^{spec}\) 谱投影路线删除。M 分支保留 DM.5 的 \(2\kappa_f^2\sigma_\varepsilon^2(1-\rho_{ij})\) 加环流项 \(\sigma_\omega^2\)。

**第四轮补（环 4／9／10 相干热分裂）：**

- 核对 06 §11.1 的 E7 后发现符号冲突：\(\Delta\varepsilon(T)=\Delta\varepsilon_0\sqrt{\tanh(\hbar\Omega_0/2k_BT)}\) 随 \(T\) 降，若当成总方差就与环 4 的 \(Z+\Theta(T)\) 方向相反；
- 判定：\(Z+\Theta\) 是**总方差**，06 的 E7 是**相干振幅**；单模下 \(V_{\rm coh}=Z^2/(Z+\Theta)=Z/(1+2n_B)\)，\(V_{\rm inc}=\Theta\)；多模 Debye 的 \(V_{\rm coh}\) 是 (9C.13) 的谱积分，不能套单模倒数；
- 接到链路：环 10 的 \(\lambda\) 只用零点 \(Z\)，\(J_{ij}(T)\) 用 \(V_{\rm coh}(T)\)，环 26 的 \(\Gamma_n\) 用 \(\Theta(T)\)；DM.5／DM.9 的振幅侧取相干，非相干进退相干预；
- 删除的读法：\(\sigma_\varepsilon^2=Z+\Theta\) 直接进 DM.5；多模 \(V_{\rm coh}=Z^2/(Z+\Theta)\)；E7 平方当总方差；
- 新交付：`03_推导工作台/环09_相干热分裂.md`、`05_Lean验证/CoherentThermalSplit.lean`、`04_计算验证/环09_相干热分裂.py`／`.png`／`.csv`、`06_决策记录/2026-11-21_相干热分裂.md`；
- Lean：`total_eq_zero_add_incoherent`、`coherentVar_antitone`、`incoherentVar_mono`、`coherent_mul_total`、`coherent_eq_sq_div_total`、`nodeJosephsonWeight_zero`、`nodeJosephsonWeight_mono`；退出码 0、无警告、无禁止项；
- 数值：`Vcoh(Tmin)=0.749753`、`Vcoh(Tmax)=0.0079053`、`Theta(Tmax)=94.121`、`min dVcoh=-6.7359e-3≤0`、`max dVinc=2.1059≥0`、单模 `max|Vcoh*Vtot-Z^2|=1.1102e-16`；
- 文献：补 L25（arXiv:2410.05216v1，零点／热／无序三源分层）与 L26（arXiv:cond-mat/0008100，量子／热相位涨落与刚度），基线至 26 卡；二者只确认“该分层是外部已有关心的问题”，不确认 CQM 的具体识别。

**第五轮补（环 10／15 温度桥）：**

- 核对 06 §0.5 的 \(J_{ij}(T)=J_{ij}^{(0)}\tau(T)\)、\(\Upsilon(T)=\Upsilon_0\tau(T)\)：\(\tau=\tanh(\theta_D/2T)\) 只在**单模**精确；Debye 多模的精确权重是 \(w(T)=V_{\rm coh}(T)/Z\)，不是 \(\tanh\)；
- 解析结果：\(w(T)=\frac{2}{\omega_D^2}\int_0^{\omega_D}\omega\tanh(\omega/2T)d\omega\)；低温 \(w=1-\frac{\pi^2}{3}(T/\omega_D)^2+O(T^4)\)，高温 \(w=\omega_D/(3T)+O(T^{-3})\)；单模低温是指数、高温是 \(1/(2T)\)，多模高温比单模低 \(1/3\)；
- 接到链路：\(J_{ij}(T)=J_{ij}^{(0)}w(T)\cos\theta_{ij}\)、\(\Upsilon(T)=\Upsilon_0w(T)\)；刚度判据为 \(w(T_c)=\Upsilon_c/\Upsilon_0\)，2D BKT 为 \(\Upsilon_0w(T_{\rm BKT})=2k_BT_{\rm BKT}/\pi\)，3D 为 \(k_BT_\theta=czJ_0w(T_\theta)\)；
- 环 15：\(\sigma_\ell^2(T)\equiv V_{\rm coh}(T)\)；\(T\) 降 → \(w\) 升 → \(\sigma_\ell\) 升 → \(p_{\rm pair}\) 升；`审-3` 的**方向**闭合，概率分布与 \(p_c\) 等价性仍未证；
- 否决的读法：06 的 \(\tanh\) 当 Debye 多模精确式；\(\sigma_\ell^2=Z+\Theta\) 直接进 \(p_{\rm pair}\)；低温 \(1-w=4x^2\) 的粗略展开（精确系数是 \(\pi^2/3\)）；
- 新交付：`03_推导工作台/环10_温度桥与刚度.md`、`05_Lean验证/TemperatureBridge.lean`、`04_计算验证/环10_温度桥.py`／`.png`／`.csv`、`06_决策记录/2026-11-21_环10温度桥.md`；
- Lean：`stiffness_rescale`、`bondTerm_rescale`、`normalizedCoherent_zero`、`normalizedCoherent_antitone`、`stiffness_coherent`、`pairReadout_antitone`、`pSync_antitone`；退出码 0、无警告、无禁止项；
- 数值：`w_debye(Tmin)=0.999996710236`、`w_debye(Tmax)=0.0333166785725`、`ratio_low_asym=0.999999683371`、`x*w_debye(x=10)=0.333166785725`、`x*w_single(x=10)=0.499583749579`、`x_BKT_debye=0.689680410682`、`x_BKT_single=0.839031178415`、`x_pair_sigma0.95=0.174479789355`；
- 文献：补 L27（arXiv:cond-mat/0612092v2，非普适超流跳变）、L28（arXiv:cond-mat/9710059，配对／相位相干分离）、L29（arXiv:2303.10639v3，无序 NbN 的锐 BKT），基线至 29 卡；三条只支持“刚度可测、两阶段可分离”，不证明 CQM 的 \(w(T)\) 系数或 \(p_{\rm pair}\) 分布。

**第六轮补（环 15 配对概率分布）：**

- 问题：06 (15.1) 只有 \(p_{\rm pair}=\Pr[\sigma_\ell>\sigma_c]\)，没有分布；\(\sigma_\ell^2=V_{\rm coh}\) 是系综第二矩，若确定化就没有概率。要保留概率，\(\sigma_\ell\) 必须读作有限格胞样本标准差；
- 工作假设 G1–G3：\(\delta C\) 第二矩层面为零均值 Gaussian 场；格胞含 \(n_{\rm cell}\) 个独立模；格胞内 \(V_{\rm coh}\) 近似均匀。则 \(n_{\rm cell}\hat V/V_{\rm coh}\sim\chi^2_{n_{\rm cell}}\)，给出

\[
p_{\rm pair}(T)=1-F_{\chi^2_{n_{\rm cell}}}\left(\frac{n_{\rm cell}\sigma_c^2}{Z\,w(T)}\right);
\]

- 符号三分：\(n_{\rm eff}=(\xi/a)^2\) 是容量／层 B 粗粒化刻度，\(N_{\rm eff}\simeq\gamma_*\ln\gamma_*/(2\pi)\) 是 06 §0.6 的可读模数，\(n_{\rm cell}\) 是局域方差估计的独立模数；候选对应是 \(n_{\rm cell}\simeq N_{\rm eff}\)，不是 \(n_{\rm cell}=n_{\rm eff}\)；\(N_{\rm eff}\) 只数可读模且随 \(T\) 变，当前固定 \(n_{\rm cell}\) 的端点展开只是条件结果；两者默认**不等**：\(n_{\rm eff}=(\xi/a)^2\) 是相干区座位数，相干区内独立自由度是 \(O(1)\)，把每个座位当独立模会与“相干”定义冲突；\(\xi\) 的角色也未定（标准相关长度 vs 全局相干域尺寸），两种读法下都不能直接同一；它按局域模读法取“同一局域读出内独立模数”，不是空间格胞点数；空间域读法属层 B，不能直接用 \(p_c=0.5927\)；
- 偶数 \(n_{\rm cell}=2m\) 的尾有精确有限和 \(p_{\rm pair}=e^{-x/2}\sum_{k=0}^{m-1}(x/2)^k/k!\)；
- 低温：\(w=1-a(T/\omega_D)^2\) 给 \(p_{\rm pair}=p_0-C(T/\omega_D)^2+O(T^4)\)，\(n_{\rm cell}\) 只进 \(p_0\) 与 \(C\)；**低温幂次固定为 \(T^2\)，不是 \(T^{n_{\rm cell}}\)**；若 \(n_{\rm cell}=N_{\rm eff}(T)\)，系数由 \(a\) 改为 \(a-b\)，幂次仍 \(T^2\)；方向保持要求 \(b<a=\pi^2/3\)；数值 \(p(0)-p(T)\) 斜率 `2.003703`、`2.005959`、`2.010482`（\(n=4,8,16\)）；
- 高温：\(w\simeq\omega_D/(3T)\) 给 \(p_{\rm pair}\propto T^{n_{\rm cell}/2-1}e^{-cT}\)，与单键高斯的 \(e^{-c/T}\) 不同；若 \(n_{\rm cell}(T)\sim T^{-1/2}\ln T\)，只加对数修正；
- \(p_{\rm sync}=p_{\rm pair}^t\) 与 \(p_c=0.59274602(4)\) 的接链写成 \(p_{\rm pair}=p_c^{1/t}\)，只是连通性必要条件，不是 \(T_c\)；
- 否决：低温 \(T^{n_{\rm cell}}\)、单键高斯尾 \(2\Phi(-\sigma_c/\sqrt{V})\)、确定性阈值、总方差 \(Z+\Theta\) 直接进 \(p_{\rm pair}\)；
- 新交付：`03_推导工作台/环15_配对概率分布.md`、`05_Lean验证/TailOccupancy.lean`、`05_Lean验证/PairCellScale.lean`、`05_Lean验证/ModeCountTemperature.lean`、`04_计算验证/环15_配对概率分布.py`／`.png`／`.csv`／`_交点.csv`、`04_计算验证/环15_nT方向.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_环15配对概率.md`；
- Lean：`tailOccupancy`、`tailOccupancy_antitone`、`pairOccupancy`、`pairOccupancy_antitone`、`normalizedPairArgument`、`normalizedPairArgument_antitone`；退出码 0、无警告、无禁止项；
- 数值：`w(Tmin)=0.999671023609`、`w(Tmax)=0.0333166796025`；`p_pair(Tmin,n=4)=0.93841276624`、`p_pair(Tmin,n=16)=0.999738993149`、`p_pair(Tmax,n=64)=3.33999397424e-47`；`Tstar(n=4)=1.12058122712`、`Tstar(n=16)=1.43212096877`、`Tstar(n=64)=1.54958381397`；
- 文献：补 L30（Goodman 散斑统计，chi-square 标准工具）、L31（Ziff，二维座渗流 \(p_c=0.59274602(4)\)）、L32（Khvalyuk–Feigel'man，强无序序参量非 Gaussian）、L33（Sulangi 等，纳米不均匀＋展宽 BKT）、L34（Jain–Sarma，有限模数 chi-square），基线至 34 卡；五条只给外部边界，不证明 CQM 的 \(\delta C\) 是 Gaussian 场或 \(n_{\rm cell}\) 的物理值。

**第七轮补（环 19 相位自由能与渗流刚度）：**

- `审-11` 的相位扇区候选：\(F_{\rm ph}[\theta]=-\sum J_{ij}\cos(\theta_i-\theta_j)\)；谐波展开给 \(\Upsilon=\frac{1}{2A}\sum J_{ij}r_{ij}^2\)，故“刚度定义”与“原始求和”在自旋波扇区相等，二维幂律 \(J\sim r^{-\alpha}\) 的收敛条件是 \(\alpha>4\)；这把 `临-20` 推进为条件判定，但物理 \(J\) 的衰减律仍属 `M6`；
- 二维支**放弃** \(\varphi=\langle e^{i\theta}\rangle\) 读法：Mermin–Wagner 使 \(\varphi\equiv0\)，只有准长程序 \(G(r)\sim r^{-\eta}\)；`审-11` 的正确落点是扭转刚度的 BKT 跳变，不是 \(f(T,0)\) 的幂律奇点；三维支 Landau 形式可用，但 \(a(T)\)、\(b\) 的第一性来源仍未给；
- 裸刚度只是**上界**：\(K_R\le K_0\) 与 \(K_R(T_{\rm BKT}^-)=2/\pi\) 给 \(T_{\rm BKT}\le T_{\rm bare}\)；(10B.13) 回改为裸交点方程，新增 (10B.13′)；
- 渗流刚度用**刚度指数**：\(\Upsilon_{\rm eff}\propto(p-p_c)^{t_\Upsilon}\)，2D \(t_\Upsilon\approx1.3\)，不是 \(P_\infty\propto(p-p_c)^{5/36}\)；旧候选 \(\Upsilon_{\rm eff}=\Upsilon_{\rm bond}P_\infty\) 在临界区否决，只作远离阈值的插值；
- `M8` **降级**：\(p_c\) 必要不充分；上界 \(T_c\le\min\{T_{\rm BKT}^{\rm pure},T_{\rm pair}(p_c)\}\)；正确相界是 \(p_{\rm pair}(T)=p_*(T)\)，\(p_*(0)=p_c\)、\(p_*(T_{\rm BKT}^{\rm pure})=1\)，交点至多一个；等价性不成立；
- 否决“\(w(T)\) 的 \(T^2\) 是外部 2D 超流刚度 \(T^2\) 的实验确认”：外部中性超流声子耗竭是 \(T^{d+1}\)（2D 为 \(T^3\)），带电超导体 Goldstone 模被 Anderson–Higgs gapped，低温由准粒子主导；\(w\) 的 \(T^2\) 只是 2D Debye 模占据权重；
- 新交付：`03_推导工作台/环19_相位自由能与渗流刚度.md`、`05_Lean验证/PhaseStiffness.lean`、`04_计算验证/环19_相位刚度.py`／`.png`／`.csv`／`_摘要.csv`、`06_决策记录/2026-11-22_相位自由能与渗流刚度.md`；
- Lean：`bondSpinWave_nonneg`、`bondSpinWave_eq_zero_iff`、`phaseStiffness_rescale`、`bkt_bare_crossing_ge`、`percolationStiffness_le_bare`、`bkt_upper_bound`、`pc_necessary`、`pc_not_sufficient`、`crossing_unique`、`percolationStiffness_antitone_in_T`；退出码 0、无输出、无禁止项；
- 数值：二维 XY 锚 \(T_{\rm BKT}=0.892940\)、跳变 \(0.568463\)；\(T_{\rm BKT}/T_{\rm bare}\) 在 \(c=2\) 为 \(0.744100\)–\(0.783130\)，\(c=5\) 为 \(0.952554\)–\(0.959370\)（始终 \(\le1\)）；\(\delta=10^{-3}\) 时 \(\Phi/P_\infty=3.285993\times10^{-4}\)；\(p_*(0)=0.500000\)、\(p_*(0.65)=0.960297\)、\(p_*(T_{\rm bare})=1.000000\)；
- 文献：Nelson（arXiv:cond-mat/9502114）、Loh 等（arXiv:1308.3033／J. Phys.: Condens. Matter **26**, 505702）、Bergman（Phys. Rev. E **65**, 026124）、Hasenbusch（arXiv:cond-mat/0502556）、Berger–Prokof'ev–Svistunov（arXiv:2506.22683／Phys. Rev. B **113**, 144512）；只给外部标准与数值锚，不证明 CQM 的相位扇区就是 XY 模型。

**第八轮补（目标区 Uemura 标度）：**

- 由环 19 的 BKT 普适跳变与因子化，写恒等式 \(T_c=\frac{\pi}{2k_B}\Upsilon_{\rm bare}(0)Q\)，\(Q=r g_{\rm ren}\le1\)；这是代数恒等式，不是拟合；
- Uemura 线性段的 CQM 成立条件是 \(w(T_c)\simeq1\) 与 \(\Phi(p_{\rm pair}(T_c))\simeq\Phi(p_{\rm pair}(0))\)；斜率 \(\pi g_{\rm ren}/(2k_B)\le\pi/2\)，**不预言普适斜率**；
- CQM 内部给出偏离机制：\(w\)、\(\Phi\) 比、\(g_{\rm ren}\) 三因子随掺杂下降 ⇒ \(T_c/\Upsilon_{\rm bare}(0)\) 单调降，与“Uemura 只在欠掺杂成立”一致；
- 数值：\(g_{\rm ren}=0.622281\)（\(c=2\) 分离点 \(K_c=1.023\)），低 \(\Upsilon_0\) 斜率 \(0.970533\) vs \(\pi g_{\rm ren}/2=0.977477\)，\(\Upsilon_0=4\) 降到 \(0.129378\)；全程 \(Q\le1\)、\(T_c\le\pi\Upsilon_{\rm bare}(0)/2\)、割线斜率单调降；
- 否决：Homes 律不可推（\(\sigma_{\rm dc}\) 属链外-F）；\(\rho_s\leftrightarrow\Upsilon\) 是外部 London 关系（链外-B 未闭合）；TDOS 预印本 arXiv:2602.22626 只作 `临-25` 对照候选；目标形式不成环；
- 新交付：`03_推导工作台/目标区_Uemura标度.md`、`05_Lean验证/UemuraScale.lean`、`04_计算验证/目标区_Uemura.py`／`.png`／`.csv`／`_摘要.csv`、`06_决策记录/2026-11-22_目标区Uemura标度.md`；文献基线补 L35–L39 至 39 卡；
- Lean：`uemura_identity`、`uemura_upper`、`uemura_Q_le_one`、`uemura_Q_eq_one_iff`、`uemura_linear_of_const_Q`、`uemura_strictMono_in_U0`、`uemura_breakdown_witness`、`uemura_bounds_combine`；退出码 0、无输出、无禁止项；
- 文献：Uemura（PRL **62**, 2317）、Homes（Nature **430**, 539）、Imry–Strongin–Homes（PRL **109**, 067003）、Nelson（arXiv:cond-mat/9502114）、Chae（arXiv:2602.22626v7 预印本）；只给外部标准与现象对应，不证明 CQM 的 \(\rho_s\) 识别。

**第九轮补（环 6 三项平衡与 `临-25` 判定）：**

- 生产—平均项的协方差读法 \(\mathcal B=\frac{4}{N-1}\sum x_iy_i\)，与 \(\mathcal D=\frac{2}{N-1}\sum x_i^2\)、\(W=\frac{2}{N-1}\sum y_i^2\) 同归一化；共线 \(y=\lambda x\) 时 \(\mathcal B=2\lambda\mathcal D\)；
- 尖锐不等式 \(\mathcal B^2\le4\mathcal DW\)；数值核对 2000 组、\(\max\mathcal B^2/(4\mathcal DW)=0.999999066973\)，协方差与无序对求和最大误差 \(3.553\times10^{-15}\)；
- 三点反例 \(\tau=(1,-1,0)\)、\(v=(0,0,1)\) 给 \(W=2/3>0\)、\(\mathcal B=0\) ⇒ 主链“差异只累积”过强，回改为“\(\dot{\mathcal D}\ge0\)（可持平）”；只改缺口行与分界段文字，**状态未变**；
- 扩大项可抵消正生产：\(\mathcal B_*=1/3\) 的显式例给 \(\mathcal B=0.2\) 时 \(\dot{\mathcal D}=-0.133<0\)；\(\dot M=0\) 是“不稀释”必要；
- `临-25` 判定为**不可判定（当前链内）**：\(\mathcal D_{\rm new}\)、\(\dot M_t\) 无独立动力学；外部 Boltzmann／Mori–Zwanzig／model A–B 的闭合均需额外假设；按停止条件登记，不自造编号、不升状态；
- 新交付：`03_推导工作台/环06_三项平衡与临25判定.md`、`05_Lean验证/ThreeTermBalance.lean`、`04_计算验证/环06_三项平衡.py`／`.png`／`.csv`／`_摘要.csv`、`06_决策记录/2026-11-22_三项平衡与临25判定.md`；文献基线补 L40–L42 至 42 卡；
- Lean：`B_sq_le_four_D_W`、`B_nonneg_of_aligned`、`B_nonpos_of_aligned_neg`、`three_point_cov_zero`、`three_point_W_pos`、`three_point_B_zero`、`V_pos_not_imp_B_pos`、`expansion_can_offset`、`crisis_reduction`、`crisis_nondecreasing`；退出码 0、无输出、无禁止项；
- 文献：Boltzmann 分子混沌／H 定理、Mori–Zwanzig／GLE（PNAS **106**, 2145）、Hohenberg–Halperin（Rev. Mod. Phys. **49**, 435）；只作“外部闭合需额外假设”的证据，不进 CQM 推导。

**第十轮补（环 10／`N-7` 刚度组装分类）：**

- 06 §7.3(c) 的“并联取和／串联取最小／几何平均”降为适用域分类：Wiener 界无条件、Dykhne 几何平均只在 2D 等比例统计等价时精确、Bruggeman 中远场近似、渗流幂律管近阈；
- Wiener 界 \((\frac{p}{a}+\frac{1-p}{b})^{-1}\le\Upsilon_{\rm eff}\le pa+(1-p)b\)；两键夹逼 \(0.166667\le0.447214\le0.600000\le1.200000\)；
- 超导＋绝缘相：Bruggeman 线性 \((2p-1)_+\) 与 CQM \((p-p_c)^{1.3}\) 冲突，比值随 \(\delta\to0\) 从 3.9905 发散到 31.6979，线性律近阈失效；
- 判定：`N-7` 的完成门槛改为“适用域分类”，本轮已给，**不闭合**为唯一公式（`审-4`、`临-24`、链外-B 未定）；登记事实：N-7 在 08 台账 62 条链层登记中未入账，本轮不改 08；
- 新交付：`03_推导工作台/环10_N7刚度组装.md`、`05_Lean验证/EffectiveStiffness.lean`、`04_计算验证/环10_N7刚度组装.py`／`.png`／`.csv`／`_摘要.csv`、`06_决策记录/2026-11-22_N7刚度组装分类.md`；同步回改 `环10_温度桥与刚度.md` 缺口行与主链 §2 键刚度行；
- Lean：`series_le_each`、`each_le_parallel`、`assembly_sandwich`、`harm_le_arith`、`geo_sq_between`、`geo_le_arith`、`linear_not_power_two`；退出码 0，无禁止项；
- 文献：Wiener 界、Keller–Dykhne 对偶（Dykhne, JETP **32**, 63；Bulgadaev, arXiv:cond-mat/0303622）、Bruggeman EMA；只作外部标准，不写成 CQM 已证。

**第十一轮补（环 15／`审-4` 座键口径与回改）：**

- 诱导键 \(B_{ij}=s_is_j\)：\(\mathbb E[B]=p^2\)；共点协方差 \(p^3(1-p)>0\)；不共点为 0；
- 正确阈值是座阈值 \(p_c^{\rm site}=0.592746\)，诱导键占比 \(q_c=0.351348<1/2\)；朴素 \(p^2\ge1/2\) 给 \(p=0.707107\)，相对误差 \(19.2934\%\)；
- Monte Carlo（Newman–Ziff，240 次／尺寸）\(L=16,24,32\) 给跨越占据率 \(0.58644,0.59280,0.59375\)，收敛到座阈值而非 0.707；
- **回改**：环 19 与目标区的 \(\Phi\) 阈值由 \(1/2\) 改为 \(0.592746\)，两脚本重跑；\(p_*(0)=0.592746\)、\(p_*(0.1)=0.642974\)、\(\Phi(p_{\rm pair}(0))=0.808142\)、低 \(\Upsilon_0\) 斜率首项 \(0.970533\)；旧数值作废，形状结论不变；
- 新交付：`03_推导工作台/环15_座键口径.md`、`05_Lean验证/SiteBondOccupancy.lean`、`04_计算验证/环15_座键口径.py`／`.png`／`.csv`／`_摘要.csv`、`06_决策记录/2026-11-22_审4座键口径.md`；同步回改 `环19_相位自由能与渗流刚度.md`、`目标区_Uemura标度.md` 与主链环 15 缺口行、§16 第 3 项；
- Lean：`shared_covariance_pos`、`induced_fraction_at_site_threshold`、`site_threshold_below_naive`、`naive_threshold_error_gt_tenth`、`correct_criterion_not_naive`；退出码 0，无禁止项；
- 文献：L31（Ziff 座阈值）、Kesten（键阈值 \(1/2\) 精确）、Jacobsen 2015（\(0.59274605079210\)）；只作外部标准，不写成 CQM 已证。

**第十二轮补（环 4／`审-10` 截断伪问题与同位素端点）：**

- `审-10` 原问“截断取 \(\theta_D\) 还是 \(\omega_{\log}\)”判为范畴错误：截断是方差测度支集 \(\omega_D\)，\(\omega_{\log}\) 是配对核的对数矩；降为 `W-3′` 子项；
- **维度回改**：\(w(T)\) 用 2D 权重 \(2y\)（低温 \(T^2\)、\(\pi^2/3\)），(目标.3) 用 3D 权重 \(3y^2\)（\(T^3\)）；2D 支应给 \(\omega_{\log}/\omega_D=e^{-1/2}=0.606531\)，旧值 \(e^{-1/3}=0.716531\) 属 3D 支；只在工作台与主链缺口行登记，未改目标区外来式原文；
- 同位素端点分类：\(\Upsilon_0\) 质量无关 ⇒ \(\alpha\to0\)（数值 0.210→0.005，与 06 §11 G15 的 0.0006 相容）；\(\Upsilon_0\propto\omega_D\) ⇒ \(\alpha=1/2\)（数值恒 0.5）；链内无 \(\mu^\ast\)，不能给中间值；
- 新交付：`03_推导工作台/环10_审10截断与同位素.md`、`05_Lean验证/IsotopeScaling.lean`、`04_计算验证/环10_审10截断与同位素.py`／`.png`／`.csv`／`_摘要.csv`、`06_决策记录/2026-11-22_审10截断与同位素.md`；同步主链环 4 缺口行、目标区缺口行、§16 第 1 项；
- Lean：`omegaLog2D_lt_3D`、`omegaLog_ratio`、`isotope_exponent_zero`、`isotope_ratio_half`、`isotope_endpoints_differ`；退出码 0，无禁止项；
- 文献：Allen–Dynes（Phys. Rev. B **12**, 905）、Bill–Kresin–Wolf 同位素综述、MgB\(_2\) \(\alpha\approx0.32\)；只作外部对照，不写成 CQM 已证。

**第十三轮补（环 7／`审-1` 局域映射强 no-go）：**

- 把 R-02 的“奇＋严格单调 ⇒ \(C=I\)”推广为**无正则性条件**的 no-go：逐行和恒为 1 对任意三点固有时成立，强制 \(f(u)+f(u+v)=f(-u)+f(v)\)，其唯一解为常数；
- 两种写法均无非平凡解：无对角量子时 \(f(0)=1\Rightarrow f\equiv1\Rightarrow C\mathbf1=N\mathbf1\ne\mathbf1\)；有对角量子时 \(g(0)=0\Rightarrow g\equiv0\Rightarrow C=I\)，差异方差归零；
- 判定：`审-1` 不是“还没算出 \(f\)”，而是**局域函数类内不可解**；非平凡 \(C\) 必须换自变量为边量 \(\lambda_{ij}\)（矩阵分支），而 \(\theta=\alpha\lambda\) 属 `G19`；
- 数值：常数族仅 \(c=1/3\) 行和残差为 0（但违反 \(C_{ii}=1\)），线性／tanh／有理族最小残差 1.922408／1.862110／1.974013；
- 新交付：`03_推导工作台/环07_审1映射no-go.md`、`05_Lean验证/Audit1NoGo.lean`、`04_计算验证/环07_审1no-go.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_审1局域映射no-go.md`；同步主链 §11 审-1 行与 §16 第 13 项；
- Lean：`constant_of_functional_eq`、`constant_solution`、`constant_implies_independent_of_H`、`row_sum_three`、`odd_zero_diag_collapse`；退出码 0，无禁止项；
- 外部：条件 Cauchy 方程（Forti–Paganosti 等）只作方程分类对照，不写成 CQM 结论。

**第十四轮补（环 6／`G19` 容差标定）：**

- 06 §10.1 的“有效窗口宽度 $=\varepsilon\xi_{\rm coher}-\Delta\phi_{\rm thermal}(T)$”拆为三处对象混淆：量纲（缺格距 \(a\)）、周期（相位属 \(U(1)\)，窗口不可能线性无界）、热项方向（须取非相干 \(\Theta(T)\)，不能取相干振幅）；
- 修复：\(\xi_{\rm coher}\to N=\xi/a\)；物理量改为相位保真度 \(\cos W\)（\(2\pi\) 周期，界 \([-1,1]\)）；“容差”不是独立对象，而是环 19 的 BKT 穿越 \(J_0A(\varepsilon)w(T)\cos(s\Lambda)=\frac{2}{\pi}k_BT\)；
- \(\alpha\) 判定：由 Regge 和乐（绕铰链转亏角 \(\ell\)）与表示权 \(s\) 得 \(\theta=s\ell\)，再由 \(\ell=2\pi(1-e^{2\lambda})\) 得 \(\alpha_{\rm lin}=-4\pi s\)；自由量只剩离散 \(s\)（须 A4 权／`临-26`）；
- 机制归属修正：06 把“向错芯先通过”归给相位窗口，方向错了；赝能隙不均匀应由振幅 \(A(\varepsilon)\) 承担，相位因子把它切成叶心在 \(\varepsilon\equiv0\pmod{2\pi/(sN)}\) 的周期叶，死区 \(\cos\le0\) 无解；
- 新交付：`03_推导工作台/环06_G19容差标定.md`、`05_Lean验证/PhaseTolerance.lean`、`04_计算验证/环06_G19容差.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_G19容差标定.md`；同步主链环 6 缺口行与 §16 第 30 项；
- 数值：线性化相对偏差 \(|\lambda|=0.01\) 时 \(1.0033\%\)、\(0.1\) 时 \(10.3331\%\)；\(w(1)=0.317771\)、\(w(10)=0.033317\)（高温渐近 \(1/(3\tau)=0.033333\) 吻合 \(5\times10^{-5}\)）；死区（\(s=N=1\)）\((1.570796,4.712389)\)；
- Lean：`theta_lin`、`stiffness_scaling`、`tri_nonneg`、`tri_le_pi`、`tri_eq_self`、`fidelity_period`、`onset_shifts_with_fidelity`、`dead_zone`；退出码 0，无禁止项；
- 外部：Regge 和乐转角＝亏角（arXiv:1904.01966 式 (5)；PRD **92**, 024013 式 (15)–(17)）、连续特征标 \(\chi(x)=e^{i\xi x}\)、Little–Parks 周期振荡，只作工具与形状对照。

**第十五轮补（环 10／`M6` 键几何与饱和定理）：**

- 把 `M6` 拆为**形状**与**能标**：形状 \(J/J_0=(1-\rho)\cos(s\ell)\) 可导（\(\rho\) 为零点差方差关联，\(s\ell\) 为 `G19` 相位），能标 \(J_0\) 按命题 Z2 外生；
- **饱和定理**：只要 \(\rho(d)\to0\)（任意衰减关联），差方差 \(2Z(1-\rho)\to2Z\)，故 \(J\) 不衰减；不需要 \(\rho\) 的具体形式；
- **键局域判定**：全对求和 \(\sim\int r^{d+1}J\,dr\) 在 3D（\(\int r^4\)）、2D（\(\int r^3\)）均发散，故全对外推是归谬；物理 \(J\) 在 DM.9 中定义于键，键局域求和有限；
- **`临-20` 子问题消解**："物理 \(J\) 衰减律"不是"还没算出"，而是"不存在需要衰减的律"；"\(\alpha>4\)"只是非法外推判据；
- 显式形状：3D \(\rho_{3d}=2(1-\cos x)/x^2\)、2D \(\rho_{2d}=2J_1(x)/x\)，\(x=k_Dd\)；近邻 \(1-\rho\approx0.59\)–\(0.77\)；
- 新交付：`03_推导工作台/环10_M6键几何.md`、`05_Lean验证/BondGeometry.lean`、`04_计算验证/环10_M6键几何.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_M6键几何饱和.md`；同步主链要素索引、环 19 缺口行与 §16 第 31 项；
- 数值：小 \(x\) 斜率 \(1/12\)、\(1/8\)；\(1-\rho_{3d}(50)=0.999972\)；\(S_3(20)=635426\) 对 \(X^5/5=640000\)、\(S_2(20)=40128\) 对 \(X^4/4=40000\)；
- Lean：`saturates`、`rho3d_le_one`、`Jshape_abs_le` 等八条；退出码 0，无禁止项；
- 外部：Debye 零点关联 \(\langle B(r)\rangle\propto(1-\cos\Lambda r)/(\Lambda r)^2\)（Tomaschitz 2020, Eq. 3.12）、3D 无质量等时 \(1/(4\pi^2r^2)\)、2D 对数，只作工具。

**第十六轮补（环 19／`审-11` 三维 Landau 系数与锚）：**

- 由 \(F_{\rm ph}[\theta]=-\sum J_{ij}\cos(\theta_i-\theta_j)\) 的变分平均场（单座配分 \(I_0\)）导出 Landau 系数：\(a(T)=\frac{zJ}{2}(1-T_0/T)\)、\(b(T)=\frac{(zJ)^4}{64(k_BT)^3}\)、\(k_BT_0=zJ/2\)；读出 \(a_0=k_B\)、\(b(T_0)=zJ/8\)、\(\Delta C=2k_B\)（每座）；
- **方法自检**：同一展开用于 Ising 给 \(a_0=k_B/2\)、\(b(T_0)=zJ/12\)、\(\Delta C=\frac32k_B\)，与 Bragg–Williams 值一致；
- **锚的身份**：\(\omega_0^2=0\iff a(T)=0\iff T=T_0\)，\(\varphi_0\propto(T_0-T)^{1/2}\)，故锚**是**相位扇区自由能的非解析点（平方根支点），但它是 \(T_c\) 的上界、不是 \(T_c\)；物理转变取 \(T_c=\min(T^*,T_{\rm ph})\)；
- **维度选择性**：\([\Upsilon_d]=[J]a^{2-d}\)，\(\Upsilon/(k_BT)\) 只在 \(d=2\) 无量纲，故“刚度＝纯数 \(\times\,k_BT\)”的普适跳变只在二维；三维须引入长度，落点是三维 XY 不动点；
- **Ginzburg 与环 6 的 \(N\)**：\(t_G=(a/\xi_0)^{2d/(4-d)}\)，\(\xi_0/a\) 正是 `G19` 的 \(N=\xi_{\rm coh}/a\)，\(d=3\) 时 \(t_G\sim N^{-6}\)；\(N=10^2\) 给 \(10^{-12}\)、\(N=10^3\) 给 \(10^{-18}\)，与常规三维超导体范围一致；故三维超导 \(N\gg1\) 时平均场渐近精确，不需要外部三维 XY 常数；
- 数值：\(a(0.8)/(zJ)=-0.125\)、\(a(1.25)/(zJ)=0.1\)；\(b(1)/(zJ)=0.125\)、\(b(2)/(zJ)=1/64\)；平均场／精确比 \(0.75192\)（Ising）、\(0.73397\)（XY）、\(0.72146\)（Heisenberg）；二维阶梯 \(2J\to1.571J\to0.893J\)；
- 新交付：`03_推导工作台/环19_审11_Landau系数与锚.md`、`05_Lean验证/LandauAnchor.lean`（十三条）、`04_计算验证/环19_审11_Landau.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_审11_Landau系数与锚.md`；同步主链环 19 缺口行与 §16 第 2 项、`成果登记.md`（R-33＋5 条否决读法）、`缺口重审.md`（环 19 行＋P1-2）；
- 外部：三维 XY 指数与 \(k_BT_c/J=2.2019\)（Campostrini et al. PRB **63**, 214503 (2001)；Lan–Hsieh–Kao arXiv:1211.0780）、Ising \(K_c=0.2216595\)（Ferrenberg–Landau PRB **44**, 5081 (1991)）、Heisenberg \(K_c=0.693035\)（Chen–Ferrenberg–Landau PRB **48**, 3249 (1993)）、Nelson–Kosterlitz PRL **39**, 1201 (1977)、Ginzburg 判据 \(t_G=(a/R)^{2d/(4-d)}\)（UCSD PHYS 210A 讲义；Tong §2.2.4），只作工具与对照。

**第十七轮补（环 26／`临-8` 不可焊接）：**

- **强 no-go**：物理核逐模率 \(\alpha+\Gamma_n\)（\(\Gamma_n=\gamma_n^2\sigma_v^2\tau_g\)）依 \(n\) 变，(26.2) 右端率 \(1/2\) 模无关；两模同时对齐要求 \((\gamma_n^2-\gamma_m^2)\sigma_v^2\tau_g=0\)，与 \(\sigma_v^2\tau_g>0\) 矛盾；即使无涨落仍须 \(\alpha=1/2\)（规范归一）；
- 辅证 B：正定型核必 \(K(0)\ge0\)，而链约定 \(K_\zeta(0)=\psi(1)-1=-1<0\)；该证条件于 GLE 读法，链已声明 \(K\) 不是 GLE 摩擦核，主证仍是 A；
- 辅证 C：唯一可写 (26.2) 的全对 \(\mathcal H_{ij}=0\) 是同步规范坐标选择（`临-16`），不是材料可达态；
- **正结果（滤波器定理）**：\(K_{\rm phys}(t)=-\sum_n\frac{e^{i\gamma_n t}}{\rho_n}W_n(t)\)、\(W_n=e^{-(\alpha+\Gamma_n-1/2)t}\)；理想极限 \(\sigma_v^2\tau_g\to0\)、\(\alpha\to1/2\) 给 \(W_n\equiv1\)，故 \(\zeta\) 形式是**规范截面上的读出**，不是物理矩阵元；
- `临-8` 判定为**不可焊接（当前链内）**，保留编号与未闭合状态；不引入"抹掉涨落"的新公设；
- 新交付：`03_推导工作台/环26_临8焊接no-go.md`、`05_Lean验证/MemoryKernelWelding.lean`（12 条定理）、`04_计算验证/环26_临8焊接no-go.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_临8焊接no-go.md`；同步主链环 26 缺口行／"不能推出"／§16 第 32 项、`成果登记.md`（R-34＋7 条否决读法）、`缺口重审.md`（环 26 行＋P2）、`00_研究纲领.md`（S4 产出）；
- 数值（示意）：前三零点 \(\Gamma_n=0.199790/0.441926/0.625543\)（\(\sigma_v^2\tau_g=10^{-3}\)），物理率 \(0.699790/0.941926/1.125543\) 全不同于 \(0.5\)；\(|\Delta\gamma^2|=242.1357/425.7525/183.6168\) 全落禁区；
- 外部：von Mangoldt 显式公式与条件收敛共轭配对（Baez；Kedlaya Thm 10.1）、GLE 正定型与第二 FDT（arXiv:2507.17350 Remark 5；arXiv:2503.20457）、零点纵坐标示意值，只作工具与对照。

**第十八轮补（环 7→8／`审-1` 矩阵分支几何强制）：**

- **几何强制**：06 BCC 三环 $\prod r=0.177/0.707/0.500\ne1$，而 $\lambda=\ln r$，故 $\sum_C\lambda=\ln\prod_Cr\ne0$，$\lambda$ 非梯度；由上一轮 no-go 的逆否（梯度＋`C1=1` ⇒ $B=0$），矩阵分支是链 inputs **强制**的逃生路径，`环08_A12矩阵化.md` §一 的前件冲突就此解决；
- **线丛读法**：$\ln v_\tau$ 不能全局单值，$\lambda$ 是图上联络，和乐属 $\mathbb R_+$；规范位移 $\lambda\to\lambda+\chi_j-\chi_i$ 不改三环和乐（数值偏差 $2.220\times10^{-16}$），与 `临-16` 一致；
- **中心对称消散度定理**：近邻壳层中心对称时任意奇 $f$ 自动给 $\sum_j f(\lambda_{ij})=0$、`C1=1` 无需显式 $f$；$x$ 与 $x^3$ 都满足 ⇒ $f$ 不由 `C1=1` 唯一确定，`M5` 与结构问题解耦；累积层 $f^{-1}$ 仍需严格单调假设；
- 新交付：`03_推导工作台/环07_审1矩阵分支几何强制.md`、`05_Lean验证/GeometricForcing.lean`（11 条）、`04_计算验证/环07_审1几何强制.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_审1矩阵分支几何强制.md`；同步主链环 7 缺口行／§16 第 33 项、`成果登记.md`（R-35＋7 条否决读法）、`缺口重审.md`（环 7／8 行）、`环08_A12矩阵化.md` §一；
- 数值：$\sum\lambda=-1.731606/-0.346725/-0.693147$；中心对称壳层四个奇函数残差全 $<10^{-15}$；非对称壳层残差 $1.700000/2.645000/1.145811/2.175736$；
- 外部：图离散 Hodge／Helmholtz 分解与环流维数 $E-V+1$（Strang；arXiv:2412.09434；CBS）、图上平坦线丛与和乐（arXiv:1207.2822；arXiv:1001.4028），只作工具与对照。

**第十九轮补（环 8／`M5` 齐次线性化）：**

- `C1=1` 齐次线性化：$D\mathbf f=0$、$D_{i\alpha}=n_{i,\alpha}-n_{i,-\alpha}$（有符号邻居计数，完全由几何决定）；
- 三条硬结论：$f\equiv0$ 总是解（$C=I$，无配对来源）；解集为线性子空间（数乘／加法保解保奇），故 $f$ 永不唯一；三档 $\dim\ker D=0/1/\ge2$（仅零解／形状唯一尺度自由／形状也不唯一）；
- **绝对 $f$ 不可由链推出**：最好情形只给形状 $f=c\,g$，尺度 $c$ 与 DM.5 的外生 $\kappa_f$ 不可分（审-2）。与 `M6` 的 $J_0$、`审-11` 的能标同构——CQM 定形状、不定绝对能标；
- BCC 逐边亏角未给（只有三角环乘积），故其 $\dim\ker D$ 当前不可算，挂账待材料数据；
- 新交付：`03_推导工作台/环08_M5齐次线性与形状能标.md`、`05_Lean验证/M5Homogeneity.lean`（11 条）、`04_计算验证/环08_M5齐次线性.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_M5齐次线性.md`；同步主链环 8 缺口行／§16 第 34 项、`成果登记.md`（R-36＋5 条否决读法）、`缺口重审.md`（环 8 行）；
- 数值：四例零化度 $4/2/1/0$；形状唯一例 $g=(0.577350,-0.577350,-0.577350)$、$|Dg|=1.110\times10^{-16}$；$D=0$ 例 $x$ 与 $x^3$ 行和均为 $0$；
- 外部：齐次线性方程组解集为子空间、秩—零化度；插值 unisolvence 需对偶基（arXiv:2606.22671 Thm 2.10）；正实奇函数插值的唯一性需额外 Lyapunov 条件（arXiv:2611.26240 Thm 2.14），只作工具与对照。

**第二十轮补（环 9／`审-2` 的 $\kappa_f$ 几何来源）：**

- 把 $\kappa_f$ 读作亏角—钟速对数响应 $\kappa_f=-\partial_\varepsilon\ln v_\tau$，由 FG 接口 $v_\tau=\sqrt{1-\varepsilon/2\pi}$ 得 $\kappa_f(\varepsilon_0)=1/[4\pi(1-\varepsilon_0/2\pi)]$、$\kappa_f(0)=1/(4\pi)=0.0795775$；
- 关键识别（构造步骤）：DM.2 连接与环 5 $\lambda_{ij}=\ln v_{\tau,j}-\ln v_{\tau,i}$ 同一，$\delta C=\delta\lambda$；不承认则 $\kappa_f$ 仍外生；
- 矩阵分支归一 $c=4\pi v_\tau^2\kappa_f\equiv1$（各工作点同）；**回改**：初稿写 $c=v_\tau^2$，数值核对发现那是"固定 $\kappa_f$ 于锚点值"的额外假设，已更正卡／Lean／脚本并留对照曲线；
- 新交付：`03_推导工作台/环09_审2_kappa_f第一性.md`、`05_Lean验证/KappaFDerivation.lean`（7 条＋4 定义）、`04_计算验证/环09_审2_kappa_f.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_审2_kappa_f几何来源.md`；同步主链环 9 缺口行／§16 第 35 项、`成果登记.md`（R-37＋5 条否决读法）、`缺口重审.md`（环 9 行）；
- 数值：$\kappa_f(0)=0.0795774715$；线性化相对误差 $7.98\times10^{-3}\to7.96\times10^{-6}$（$\Delta=0.1\to10^{-4}$）；四工作点 $4\pi v_\tau^2\kappa_f=1.000000000000$；
- 外部：Grüneisen 对数响应（Wikipedia；arXiv:2003.07686；arXiv:2607.27803 Eq.(8)）、Regge 亏角＝输运旋转角（arXiv:1904.01966），只作工具与对照。

**第二十一轮补（环 4／`审-10` 收口：$\omega_{\log}$ 按扇区分裂）：**

- $\omega_{\log}$ 必须按扇区分裂：振幅支（3D Debye $3y^2$）$\omega_{\log}^{\rm amp}=\omega_D e^{-1/3}$ 进 (目标.2) 的 $T^*$，相位支（2D $2y$）$\omega_{\log}^{\rm ph}=\omega_D e^{-1/2}$ 进 $w(T)$ 与 BKT；比值 $e^{1/6}=1.181360$；
- **回改上一轮的过度修正**：此前工作台写"2D 支应把 (目标.3) 整体替换成 $e^{-1/2}$"，那会破坏 (目标.2) 的 3D BCS 型 $T^*$。$e^{-1/3}$ 不是错值，只是属于振幅扇区；正确做法是分裂并加注记；
- 主链 (目标.3) 已按用户授权带注记修正（保留 $e^{-1/3}$ 并补 $e^{-1/2}$ 相位支），(目标.2) 式与 06 原文未动；两矩共用 $\omega_D$，同位素端点 $\alpha\in\{0,1/2\}$ 分类不变，绝对能标仍外生（Z2）；
- 新交付：`03_推导工作台/环04_审10_双扇区omega_log.md`、`05_Lean验证/TwoSectorOmegaLog.lean`（6 条＋3 定义）、`04_计算验证/环04_审10_双扇区omega.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_审10_双扇区omega.md`；同步主链 (目标.3)／目标区缺口行／§16 第 36 项、`成果登记.md`（R-38＋5 条否决读法）；
- 数值：$p_2=0.606531$、$p_3=0.716531$、比值 $1.181360$；$\int_0^1 d y^{d-1}\ln y=-1/d$（$d=2,3,4,5$ 数值吻合）；$w_2$ 低温 $T^2$、$w_3$ 低温 $T^3$；
- 外部：$d$ 维 Debye 态密度与几何平均 $e^{-1/d}$（Open Solid State Notes；TU Graz；Wikipedia）、BCS $1.13\hbar\omega_c e^{-1/\lambda}$（Illinois Lecture 15；arXiv:1910.04579），只作工具与对照。

**第二十二轮补（环 4／`W-3′` 判否）：**

- **计数定理**：闭球面三角化 $E=3V-6$；亏角映射 $D:\mathbb R^E\to\mathbb R^V$ 单射须 $E\le V\iff V\le3$，故 $V\ge4$ 时必非单射、$\dim\ker D\ge E-V=2V-6>0$。亏角**不是**简正模的完全坐标；
- **核模身份**：保角（离散共形）形变＋平坦区域顶点位移（锚核 $A_\tau$ 所在），改连接不改亏角 ⇒ 亏角模属振幅扇区、核模属相位扇区，给矩阵分支 $B=f(\lambda)$ 以结构根据（比 BCC 和乐更一般）；
- 新交付：`03_推导工作台/环04_W3prime简正模完全性.md`、`05_Lean验证/NormalModeCompleteness.lean`（5 条）、`04_计算验证/环04_W3prime简正模.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_W3prime简正模完全性.md`；同步主链环 4 缺口行／§16 第 37 项、`成果登记.md`（R-39＋4 条否决读法）、`缺口重审.md`（环 4 行）；
- 数值：$V=4\to12$ 核下界 $2\to18$；一般四面体 $4\times6$ Jacobian 秩 4、核维 2（与下界一致）、奇异值 $(4.380,3.194,1.828,0)$、核向量 $\|x\|=1$、$\|Jx\|=3.113\times10^{-10}$；
- 外部：Regge 亏角与和乐—平面角关系（arXiv:gr-qc/0408006；arXiv:1904.01966；arXiv:1709.08373）、线性化 Regge 平坦零模（arXiv:1411.5672；arXiv:1106.4266）、离散共形形变（arXiv:1702.04019），只作工具与对照。

**第二十三轮补（环 26／`临-22` 阻尼率物理桥）：**

- $\tau_g=c/\omega_D$（形状，$c$ 未定）填上"$\tau_g$ 无式子"的形状空位；高温 $\Gamma_n=(c\kappa_\Theta\gamma_n^2/\omega_D^2)T$ 给 **$T$ 线性阻尼形状**，与外部 Planckian 同形但斜率依材料，**不宣称已推普适系数**；
- `临-22` 判为**不可由物理侧桥接**：模依赖 $\Gamma_n-\Gamma_m=(\gamma_n^2-\gamma_m^2)c\sigma_v^2/\omega_D$ 与 $\beta_n\equiv1/2$ 统一性结构不相容；外参只能定时间单位（规范）；RH 仍外部假设，(27.3) 只能停在"位置"；
- 接口：$N_{\rm eff}\propto T^{-1/2}$ 高温可读窗口压缩，与 (26.A4) 同向；
- 新交付：`03_推导工作台/环26_临22阻尼率物理桥.md`、`05_Lean验证/DampingBridge.lean`（5 条）、`04_计算验证/环26_临22阻尼率桥.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_临22阻尼率桥.md`；同步主链环 26 缺口行／要素索引／§16 第 38 项、`成果登记.md`（R-40＋4 条否决读法）；
- 数值：$\Gamma_n$ 斜率 $1.997905/4.419262/6.255430$；$\Gamma_2/\Gamma_1=2.211948$ 在 $T=0.5/1/2$ 恒定；
- 外部：phonon 时间 $1/\omega_D$（Springer）、Debye DOS 等价 Ohmic bath（arXiv:2112.04001）、Planckian T 线性（Legros Nat. Phys. 2019；arXiv:2406.12133），只作工具与对照。

**第二十四轮补（目标补充／`审-14` 的 $\Gamma$ 来源）：**

- $\Gamma(E)=1+(E/E_0)^n$ 是累积态数 ⇒ $g\propto E^{n-1}$；Debye $g\propto\omega^{d-1}$ ⇒ **$n=d_{\rm spec}$、$E_0\sim\hbar\omega_D$**（唯一链内谱候选）；
- **替代 $T$ 入口判为非物理**：(补.3) 给 $T_c=0.629961\hbar\omega_D$，比 Al/Nb/Pb 观测 $T_c/\theta_D=0.002804/0.033636/0.068571$ 高 $9$–$225$ 倍；故支持环 4 唯一入口，两条路都不给绝对 $T_c$（另取 $E_0$ 即 Z2 换名）；
- $\chi$ 只经 $E_0(\chi)$ 移峰位、不改相变存在性（$n=1$ 无峰），与 (26.A3) 一致；(补.1b) 的 $\beta$ 与零点 $\beta_n$ **同名异物**，不碰 RH/`临-22`；
- 新交付：`03_推导工作台/目标_审14_Gamma第一性.md`、`05_Lean验证/GammaSource.lean`（6 条）、`04_计算验证/目标_审14_Gamma.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_审14_Gamma来源.md`；同步主链目标补充缺口行／互斥注记／§16 第 39 项、`成果登记.md`（R-41＋5 条否决读法）；
- 数值：峰位 $x_*=1.259921$（$n=3$）、$T_c/E_0$ 从 $1$（$n=2$）降到 $0.215$（$n=7$）；Debye 归一化积分 $\approx1$；
- 外部：Debye DOS $g\propto\omega^{d-1}$（arXiv:0909.3701；Open Solid State Notes）、Al $T_c=1.2$K／$\theta_D=428$K（NIST），只作工具与对照。

**第二十五轮补（环 19／`M8` 相界斜率律）：**

- 从相界方程 $p_{\rm pair}(T_c)=p_*(T_c)$ 推可微后果：$p_*'/(p_*-p_c)=\frac1{t_\Upsilon}(1/T-w'/w)$、$dT_c/d\delta=(dp_{\rm pair}/d\delta)/p_*'$；
- 近阈值幂律 **$T_c\propto(p_{\rm pair}-p_c)^{t_\Upsilon}$**，对数斜率 $=t_\Upsilon$；绝对斜率 $\propto(p_{\rm pair}-p_c)^{t_\Upsilon-1}\to0$（水平切线）——**回改**初稿"竖直切线"之误：发散的是对数斜率，不是绝对斜率；
- 与 Uemura 值律 $T_c\propto\rho_s$（L35）互补（高度 vs 陡度），且斜率律**不含** $\Upsilon_0$；
- 新交付：`03_推导工作台/环19_M8相界斜率.md`、`05_Lean验证/M8PhaseBoundary.lean`（3 条）、`04_计算验证/环19_M8相界斜率.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_M8相界斜率.md`；同步主链环 15 缺口行／§16 第 40 项、`成果登记.md`（R-42＋3 条否决读法）；
- 数值：(M8S.1) 相对误差 $2.9\times10^{-10}$–$1.3\times10^{-11}$；双对数斜率 $1.300000=t_\Upsilon$；交点 $T_c=0.457057$（归一化示意）；
- 外部：Uemura PRL **62**, 2317 (1989)（L35）、Imry–Strongin–Homes PRL **109**, 067003 (2012)（L37）、$t_\Upsilon\approx1.3$，只作工具与对照。

**第二十六轮补（环 15／`审-4` 环空间一半与推 6 撤销）：**

- $p_{\rm loop}$ 饱和 $1/2$ 来自 **GF(2) 环空间**的纤维等势：非零可加泛函的两个纤维等势（特征 2 平移对合），故均匀环向量每条在环中的边占据率恰 $1/2$；C4（$|Z|=2$）、K4（$|Z|=8$）枚举核对每边恰 $0.5$；
- 诱导键 $B_{ij}=s_is_j$ 是**对称占据场**（$\mathbb E=p^2$、共点协方差 $p^3(1-p)$），不是反对称联络 ⇒ "和乐动力学映射"问法按扇区分离解决（和乐属相位扇区的 $\lambda$）；
- **推 6 撤销**：它混用 $p_{\rm loop}=1/2$（拓扑环占据）与 $q_c=(p_c^{\rm site})^2=0.351348$（配对诱导键阈值）；$p_{\rm pair}>0.592746$ 时单层配对键已渗流。仅留条件性弱化版；
- 新交付：`03_推导工作台/环15_审4_和乐动力学与推6.md`、`05_Lean验证/CycleSpaceHalf.lean`（7 条）、`04_计算验证/环15_审4_环空间一半.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_审4环空间与推6撤销.md`；同步主链推 6（撤销注记）／§16 第 3 项／第 41 项、`成果登记.md`（R-43＋5 条否决读法）；
- 数值：C4/K4 每边 $0.5$；$q_c=0.351348<1/2$；$p=0.707107$ 时 $q=1/2$；
- 外部：图环空间 GF(2)（Wikipedia *Cycle space*；Mehlhorn–Michail）、Kesten CMP **74**, 41 (1980)，只作工具与对照。

**全链拉通核对（第 1–26 轮总账）：**

- 总账 `00_全链拉通核对.md`：四态（A 形状已推／B 已判否不可／C 外生外部／D 未动），全部保持未闭合；§16 账面 41 行、**35 个唯一编号**（重复：`审-10`×3，`审-2`／`审-1`／`临-22`／`审-4`×2）；A/B=7/7，其余 21 项在 C/D；
- 闭环读法：横向（频率阶梯、几何形状、判据结构）已推到底；纵向（绝对能标、零点纵坐标、材料归一）要么外生、要么链内不可；
- **绝对 $T_c$ 最小外生输入集（8 项）**：$\omega_D$、$\Upsilon_0/J_0$、$A(\varepsilon)/N/s$、$c/\kappa_\Theta$、$t_\Upsilon$、$\sigma_{\rm dc}\leftrightarrow\Upsilon$、RH/$\beta_n$、$p(r)$ 统计；由 $T_c=\omega_D F(\Upsilon_0/\omega_D)$ 与 Buckingham $\pi$，无量纲形状不能定绝对标度 ⇒ CQM 不可能从零算出绝对 $T_c$（理论定位，非待补技术缺口）；
- 新交付：`05_Lean验证/ClosureLedger.lean`（9 条）、`04_计算验证/全链_四态总账.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_全链拉通核对.md`；主链新增 §17 总账指针。

**第 27 轮补（环 23／`审-13` 亏格修正）：**

- 环空间维数 $E-V+1$、面边界子空间 $F-1$；Euler $\chi=2-2g-b$ ⇒ 余维 **$2g+b$**：最小环只在 $g=0,b=0$（闭球面）张成全部环路，带孔/有限样品缺 $2g+b$ 个绕数标签（缺失标签与和乐同源，属相位扇区）；
- **回改**初稿 $2g+b-1$ 的算术错误（Lean `ring_nf` 无法闭合后追查 Euler 代入）：正确结果 $2g+b$，平面片 $b=1$ 缺外边界圈；
- 新交付：`03_推导工作台/环23_审13_亏格修正.md`、`05_Lean验证/GenusCorrection.lean`（7 条）、`04_计算验证/环23_审13_亏格修正.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_审13亏格修正.md`；同步主链 §16 第 24／42 项、`成果登记.md`（R-44＋3 条否决读法）；
- 数值：$b=0$ 时 $g=0,1,2,3$ 的余维 $0,2,4,6$；$g=0$ 时 $b=1,2,3$ 为 $1,2,3$；
- 外部：环空间维数 $|E|-|V|+1$（Wikipedia *Cycle space*）、$\chi=2-2g$（ETH 讲义）、$b_1=2g$，只作工具与对照。

**第 28 轮补（环 6／`G19` 表示权量子化）：**

- 单值性 $\rho(R(2\pi))=e^{i2\pi s}$ 给 $s\in\mathbb Z$（玻色）或 $\mathbb Z+\frac12$（旋量双覆盖）⇒ **$2s\in\mathbb Z$**，穷尽原候选 $0,\frac12,1$、排除 $s=1/3$；$\alpha_{\rm lin}=-4\pi s=-2\pi(2s)\in2\pi\mathbb Z$；
- 选档仍须 A4 权（`临-26`）；绕铰链相位 $e^{is\varepsilon}$ 按 $\pi$ 跳变——可检验后果；
- 回改：初稿 Lean 清单多列未实现的 `excludes_third`，已删除；非半整数排除由数值给出；
- 新交付：`03_推导工作台/环06_G19表示权量子化.md`、`05_Lean验证/WeightQuantization.lean`（4 条）、`04_计算验证/环06_G19表示权量子化.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_G19表示权量子化.md`；同步主链 §16 第 30／43 项、`成果登记.md`（R-45＋4 条否决读法）；
- 数值：$\cos(2\pi s)$ 在 $s=0,1/2,1$ 给 $1,-1,1$、$s=1/3$ 给 $-0.5$；$\alpha$ 阶梯 $0,-2\pi,-4\pi,-6\pi,\ldots$；
- 外部：转动表示单值性与 $SU(2)\to SO(3)$ 双覆盖（DAMTP／Caltech 讲义），只作工具与对照。

**第 29 轮补（环 13.A／`临-26` 的 A4 权子项）：**

- $A_4$ 根 $\alpha_{ij}=e_i-e_j$（20 根/10 正根）；紧致 $U(1)\subset SU(5)$ 由整余特征生成 ⇒ 根电荷 $q_{ij}=h_i-h_j\in\mathbb Z$；与 G19 的 $s\in\frac12\mathbb Z$ 合并 ⇒ **$s\in\mathbb Z$**，半整分支须主丛自旋提升（链内无）；
- 基础余特征 $\omega_k^\vee$ 第一层只给 $0,\pm1$，最小非平凡 $s=1$ 与 (6G.14) 一致；选档仍待配对算符动力学；`临-26` 其余子项（实现次序、2 配对归一、DFT 四项）不动；
- 新交付：`03_推导工作台/环13A_临26_A4权电荷.md`、`05_Lean验证/A4RootCharge.lean`（5 条）、`04_计算验证/环13A_临26_A4权电荷.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_临26_A4权电荷.md`；同步主链 §16 第 29／44 项、`成果登记.md`（R-46＋4 条否决读法）；
- 数值：20 根/10 正根；五个基础余特征的电荷全为 $-1,0,1$；整格点为 G19 半整格点的子集；
- 外部：特征格/余特征格对偶（MIT *repweights*）、根格/权格（Stanford *rootcalc*），只作工具与对照。

**第 30 轮补（目标区／`D1` 的 $T_\theta$ 端子）：**

- 【构造】定义 $T_{\theta,n}=(\hbar/k_B)\Gamma_n=(\hbar/k_B)\gamma_n^2\sigma_v^2\tau_g$（Planckian 换算）；$\Gamma_n\propto\gamma_n^2$ 随 $n$ 增 ⇒ **$T_\theta=\min_n T_{\theta,n}=T_{\theta,1}$**（最低零点控制）；
- (27.2)"所有零点给同一 $T_\theta$"⇔阻尼统一，`临-22` 判链内不可供给、只能来自外部 RH；无 RH 时是梯度族，min 选 $n=1$ 是定义选择；
- 绝对归一含 $c$、$\sigma_v^2$、$\omega_D$（总账外生输入），不给绝对 $T_c$；
- 新交付：`03_推导工作台/目标_D1_Ttheta端子.md`、`05_Lean验证/ThetaTerminal.lean`（6 条）、`04_计算验证/目标_D1_Ttheta.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_D1_Ttheta端子.md`；同步主链 §16 第 15／45 项、`成果登记.md`（R-47＋4 条否决读法）；
- 数值：$T_{\theta,n}/C=199.7905,441.9262,625.5430,\ldots$；前 3/6/10 个零点的 min 均为 $199.7905$；
- 外部：Planckian $\tau_{\rm Pl}=\hbar/(k_BT)$（arXiv:2506.19188；arXiv:2504.02179；Legros 2019），只作工具与对照。

**第 31 轮补（目标区／`临-19` 场依赖）：**

- 链内配对模式集 $n\in2\mathbb Z$ 给 $q=2e$，相位单值性给 $\Phi_0=h/(2e)$；外部 GL 关系给 $B_{c2}=h/(4\pi e\xi^2)$（$\xi$ 外生，$\Delta$ 脏极限映射挂账）；
- $f(0)=1$、单调减、解析 ⇒ 低场 $f=1-a x+O(x^2)$、$a>0$；归一化初斜率 $d(T_c/T_{c0})/d(B/B_{c2})|_0=-a$（$a$ 外生，涡旋芯能／RG），与"磁场只能压低"一致；
- 新交付：`03_推导工作台/目标_临19_Bc2与场依赖.md`、`05_Lean验证/FieldSuppression.lean`（6 条）、`04_计算验证/目标_临19_Bc2与场依赖.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_临19_Bc2与场依赖.md`；同步主链 §16 第 19／46 项、`成果登记.md`（R-48＋4 条否决读法）；
- 数值：$\Phi_0=2.067834\times10^{-15}$ Wb；$\xi=10$ nm 给 $B_{c2}=3.2911$ T；低场斜率 $-a$；
- 外部：$B_{c2}=\Phi_0/(2\pi\xi^2)$、$\Phi_0=h/(2e)$（arXiv:2501.12889；TU Graz；Wikipedia），只作工具与对照。

**第 32 轮补（环 26／`临-24` 全对归一接口）：**

- $R_n=\frac1{M(t)}|\sum_{\mathcal P_t^{\rm act}}e^{i\Phi}|\in[0,1]$（三角不等式）；总键数归一只给 $M/N$ 稀释，把连通度下降误读为相干度下降 ⇒ **活跃键数是唯一自洽分母**，$\mu_t$ 支集＝活跃键集；
- 随机相位标度 $R\sim M^{-1/2}$（数值斜率 $-0.5101$），与 `临-11` 的 $|D_i|^{-1/2}$ 同量级但对象不同（不能合并）；
- 新交付：`03_推导工作台/环26_临24_全对归一接口.md`、`05_Lean验证/AllPairsNormalization.lean`（5 条）、`04_计算验证/环26_临24_全对归一.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_临24全对归一.md`；同步主链 §16 第 27／47 项、`成果登记.md`（R-49＋4 条否决读法）；
- 数值：$M/N$ 稀释因子核对（$M=50,N=400$ 时 $R$ 从 $0.1223$ 降到 $0.0153$）；$R\in[0.0016,0.2955]$；全相干 $R=1$；
- 外部：三角不等式与随机相位 $\mathbb E|\sum e^{i\theta}|^2=M$，只作工具与对照。

**第 33 轮补（环 13／`临-11` 自平均标度）：**

- $\operatorname{Var}(\hat\mu)=(n\sigma^2+C)/n^2$；独立 ⇒ 标准误 $\sigma/\sqrt{|D_i|}$——链内 $|D_i|^{-1/2}$ 标度的来源；
- 相关 $\bar c>0$ ⇒ 方差平台 $\to\bar c$、自平均失效；(13.6) 成立条件是 $\bar c=o(1/n)$（平均相关消失），不是单纯域大；`审-4` 的共点协方差 $p^3(1-p)>0$ 是相关源；
- 与 `临-24` 的相位相干 $M^{-1/2}$ 同指数但对象不同，不能合并；
- 新交付：`03_推导工作台/环13_临11自平均标度.md`、`05_Lean验证/SelfAveraging.lean`（5 条）、`04_计算验证/环13_临11自平均.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_临11自平均标度.md`；同步主链 §16 第 9／48 项、`成果登记.md`（R-50＋4 条否决读法）；
- 数值：标准误双对数斜率 $-0.5000$；$\bar c=0.1$ 时方差平台 $0.10009$（$n=10^4$）；
- 外部：自平均相对方差判据 $R_X\to0$（arXiv:2005.14188；KIT 讲义），只作工具与对照。

**第 34 轮补（环 22／`临-17` 冻结偏移接口）：**

- $c_{ij}=\tau_i-\tau_j=a_i-a_j$ 是 **1-余缘**（反对称＋三环闭合）；$N(N-1)/2$ 个偏移仅 $N-1$ 独立参数（数值映射秩 5，$N=6$）；归约为节点冻结固有时分布 $\sigma_a$；
- $R_n=|\langle e^{i\gamma_n a}\rangle|$；高斯给 $e^{-\gamma_n^2\sigma_a^2/2}$，可读窗口 $\gamma_*\sim1/\sigma_a$——给 (26.A4) 一个具体宽度；全对零余缘是规范选择，与 `临-16` 一致；
- 回改：初稿 reshape 算秩恒为 1，已改为映射矩阵，秩 $N-1$；
- 新交付：`03_推导工作台/环22_临17_冻结偏移的余边缘.md`、`05_Lean验证/FrozenCoboundary.lean`（7 条）、`04_计算验证/环22_临17_冻结偏移.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_临17余边缘.md`；同步主链 §16 第 6／49 项、`成果登记.md`（R-51＋4 条否决读法）；
- 数值：三环和乐残差 $2.220\times10^{-16}$；$\sigma_a=0.01/0.02/0.05$ 给 $R(\gamma_1)=0.990060/0.960830/0.779005$；
- 外部：1-余缘（Wikipedia *Cocycle*；nLab）、高斯特征函数，只作工具与对照。

**第 35 轮补（环 7／`临-1` 亏角驱动源）：**

- $\varepsilon_v=2\pi-\sum\theta_k$ 是 Regge 边长的导出量；余弦定理给 $\dot\theta$ 的边长率线性式，按边重组得 $\dot\varepsilon_v=\sum_e\chi^{(v)}_e\dot\ell_e$（几何因子）；电场驱动 $\dot\ell_e=d_e\dot E$ 时 $\chi_v=\sum_e\chi^{(v)}_e d_e$（几何×材料，$d_e$ 外生）；
- 均匀缩放不改亏角（数值 $\sim10^{-15}$）——须非均匀驱动；面角全增则亏角减（数值 $d\varepsilon/ds_0=-1.161898$）；
- 回改：Lean 初稿 `deficit_rate` 符号写反（$\theta-\dot\theta$），已更正为 $\theta+\dot\theta$；
- 新交付：`03_推导工作台/环07_临1_亏角驱动源.md`、`05_Lean验证/DeficitDrive.lean`（6 条）、`04_计算验证/环07_临1_亏角驱动源.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_临1亏角驱动源.md`；同步主链 §16 第 16／50 项、`成果登记.md`（R-52＋4 条否决读法）；
- 数值：偏导数解析 vs 有限差分 $1.154701$／$-0.577350$ 完全吻合；
- 外部：Regge 以边长为动力学变量（arXiv:0809.1815；arXiv:0804.0279）、余弦定理、压电系数，只作工具与对照。

**第 36 轮补（环 3／`临-18` 压强映射）：**

- 面角只依赖边长比 ⇒ 均匀仿射形变不改亏角（欧拉恒等式 $\sum_e\ell_e\partial_\ell\theta=0$）；**(3.4) 的"整体移位"修正为"不变"**（主链加注记，状态栏不动），$\mathcal H_{ij}$ 不变仍成立；
- $\partial\varepsilon/\partial P=\sum_e\chi^{(v)}_e\partial\ell_e/\partial P$：均匀弹性模量 $K$ 给零 ⇒ 目标区论断 1（静水压一阶无关）由几何推导；非均匀应变生 $\mathrm{Var}(\varepsilon)>0$（梯度 $0.1/0.2/0.31$ 给 $6.45\times10^{-3}/2.59\times10^{-2}/5.90\times10^{-2}$）；
- 褶皱是边界约束／非仿射形变的条件性后果，不是均匀压强必然后果；阈值需外部力学；
- 回改：初稿 `np.roll` 循环置换因对称性使方差恒零，已改为单半径扰动；
- 新交付：`03_推导工作台/环03_临18_压强映射与褶皱条件.md`、`05_Lean验证/PressureInvariance.lean`（5 条）、`04_计算验证/环03_临18_压强映射.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_临18压强映射.md`；同步主链 (3.4) 注记／§16 第 18／51 项、`成果登记.md`（R-53＋4 条否决读法）；
- 外部：薄板褶皱边界系综（arXiv:2103.07455）、二维材料弯曲刚度（Ares 2021），只作工具与对照。

**全链第二次核对（第 27–36 轮）：**

- §16 账面 41 行 → **51 行**，唯一编号仍 **35**（16 行重复登记）；实质推进 14 → **24**（A18／B6），余 11 项在 C/D；
- 新增 10 项：`审-13`（B）与 `G19`、`临-26`、`D1`、`临-19`、`临-24`、`临-11`、`临-17`、`临-1`、`临-18`（A）；
- 绝对 $T_c$ 结论**不变**：外生输入集仍非空（新增 $\sigma_a$、$d_e$、$\partial\ell_e/\partial P$、$a$、$\xi$、$\bar c$ 等材料量），B 类判否锁定；
- 累计三处带注记回改：(目标.3) $\omega_{\log}$ 扇区分裂、(3.4) 均匀压强不改亏角、推 6 撤销；均已写入主链，状态栏未动；
- 新交付：`04_计算验证/全链_第二次核对.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_全链第二次核对.md`；总账卡 `00_全链拉通核对.md` §九、`ClosureLedger.lean`（当时为 `ledger_51_rows_35_unique`、`advanced_24_split`，第 37 轮已更新为 `ledger_52_rows_35_unique`、`advanced_25_split`）、主链 §17 已更新。

**第 37 轮补（环 14／`临-12` 记忆核零点换元）：**

- $t_0\to t_0+\delta$ 给 $\tau_i'=\tau_i-\Delta_i$、$\Delta_i=\int_{t_0}^{t_0+\delta}v_{\tau,i}dt'$；(14.1) 与 (14.2) 均获**逐模相因子** $e^{-i\gamma_n\Delta}$（谱依赖畸变，非整体相移）⇒ 读数层非 $t_0$-不变；冻结时 $\mathcal H_{ij}$ 不变（判据层零点无关）；
- 零点无关三类：判据（场量）、幅度谱 $\{|1/\rho_n|\}$、时差相关量（零点相因子共轭相消，与外部 TTI 一致）；(13.2)"第一配对为零点"是必要规范固定（$\{\gamma_n\}$ 不可公度，仅 $\Delta=0$），给出定量理由；
- 回改：Lean 初稿 holonomy 平移式写成 $H-(D_i-D_j)$（数学错误），已改为 $(\tau_i-D_i)-(\tau_j-D_j)=(\tau_i-\tau_j)-(D_i-D_j)$；复数指数 coercion 与三角 API 按编译反馈修正；
- 新交付：`03_推导工作台/环14_临12_记忆核零点换元.md`、`05_Lean验证/ZeroPointShift.lean`（8 条）、`04_计算验证/环14_临12_记忆核零点换元.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_临12记忆核零点换元.md`；同步主链 (13.2) 注记／环 14 缺口行／§16 第 7／52 项、`成果登记.md`（R-55＋3 条否决读法）；
- 数值：相因子斜率 $-\gamma_n$ 偏差 $7.105\times10^{-15}$；冻结 $H'=0.300000$ 恒定、非冻结 $0.30\to0.42$；读数 $|D|=0.2749\to0.1469$；相关量零点相消偏差 $0$；
- 账面更新至 **52 行／35 唯一／25 项推进（A19／B6）**，余 10 项在 C/D；绝对 $T_c$ 结论不变；总账卡 `00_全链拉通核对.md` §十、`ClosureLedger.lean`（`ledger_52_rows_35_unique`、`advanced_25_split`）、主链 §17、`04_计算验证/全链_第三次核对.py`／`.png`／`.csv` 已同步；
- 外部：TTI⇒核只依赖时差（arXiv:2603.29481；arXiv:2401.15021）、aging 破缺 TTI（arXiv:2607.25374），只作工具与对照。

**第 38 轮补（环 16／`临-21` 有效点数的参与比）：**

- $n_{\rm eff}=1/\sum_i p_i^2$（归一化权重参与比）：泛函形式由"等权 $N$ 点给 $N$、集中一点给 $1$"唯一确定；`临-21` 归约为"权重选择未定"；
- 结构界（Lean 证）：$1\le n_{\rm eff}\le|\mathrm{supp}\,p|$，等权饱和；细分不减（$u^2+v^2\ge(u+v)^2/2$）、筛选可减（两点 $\le2$）——两种操作方向相反；
- 三候选（空间/能窗/费米壳层）是**不同筛选**、无一般序（数值交叉 2 次），权重选择与材料归一外生；$\pi(\xi/a)^2$ 仅二维空间等权截止读数；无限均匀等权给 $n_{\rm eff}\to\infty$ ⇒ 晶格总点数约束失效的严格版；
- 新交付：`03_推导工作台/环16_临21_有效点数的参与比.md`、`05_Lean验证/EffectiveCount.lean`（8 条）、`04_计算验证/环16_临21_有效点数参与比.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_临21有效点数参与比.md`；同步主链环 16 缺口行／§16 第 21／53 项／§17、`成果登记.md`（R-56＋3 条否决读法）；
- 数值：等权 $n_{\rm eff}=N$ 精确（$N=1/10/100/1000$）；指数权重 $\beta=0/0.05/0.2/0.5$ 给 $200/40.0/10.0/4.08$；细分 $36.87\to589.99$ 单调增；三候选次序交叉 2 次；
- 账面更新至 **53 行／35 唯一／26 项推进（A20／B6）**，余 9 项在 C/D；绝对 $T_c$ 结论不变；
- 外部：IPR/参与比（arXiv:1106.1131；arXiv:1007.5306）、有效通道数 $N_{\rm eff}$（arXiv:2205.02272），只作工具与对照。

**第 39 轮补（环 16／`临-2` 等边际凹性判据）：**

- 补 (16.1) 等边际的充分性与唯一性：$m(n)=\lambda(n+1)-\lambda(n)$；$m$ 严格反单调（凹）⇒ 等边际点唯一、转移增益 $m(i)-m(j-1)>0$、均等为唯一全局最大（water-filling，下降支/多域共存）；$m$ 严格递增（凸）⇒ 均等为最小、角点最大（上升支/单域主导）；
- **dome 两支由凹性判定，不由 (16.A1)/(16.A2) 选哪一族决定**；饱和型 $m^{(1)}=\lambda_\infty(1-e^{-1/n_0})e^{-n/n_0}$ 严格反单调（Lean 证）；顶点只是凹性切换的结构标志，$\mu$ 只给单调方向；
- 新交付：`03_推导工作台/环16_临2_等边际与dome两支的凹性判据.md`、`05_Lean验证/MarginalAllocation.lean`（6 条）、`04_计算验证/环16_临2_等边际凹性判据.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_临2等边际凹性判据.md`；同步主链环 16 注记／缺口行／§16 第 10／54 项／§17、`成果登记.md`（R-57＋3 条否决读法）；
- 数值：两候选边际严格递减；凹转移增益最小 $0.004675>0$、凸增益最大 $-0.265425<0$；凹均等 $6.0>$角点 $3.4641$、凸均等 $24.0<$角点 $41.5692$；$\mu$ 随 $n_{\rm eff}$ 降 $0.846\to0$；
- 账面更新至 **54 行／35 唯一／27 项推进（A21／B6）**，余 8 项在 C/D；绝对 $T_c$ 结论不变；
- 外部：KKT/water-filling（arXiv:1808.01707v4；arXiv:2510.11266）、dome 竞争趋势（arXiv:2110.06563v1），只作工具与对照。

**第 40 轮补（环 22／环 19／`审-12` 并存窗口）：**

- 尺度错位可算化：参与比 $L_{\rm eff}=\sqrt{n_{\rm eff}}$ ＋主链 §0.2 下移 $\Delta p\sim L^{-3/4}$（$\nu=4/3$）⇒ 局域伪临界阈值 $p_c^{\rm loc}=p_c-Cn_{\rm eff}^{-3/8}$（$C>0$，指数 $-3/8=-(1/2)(3/4)$ 纯代数合成）；
- 并存窗口 $(p_c^{\rm loc},p_c)$ 非空、宽度 $\Delta p=Cn_{\rm eff}^{-3/8}>0$ ⇒ 推 11"未扩完即相变"获**必要窗口**支持；随 $n_{\rm eff}$ 递减与"非均匀概率高、均匀概率低"同向；容量下限 $n_{\rm eff}>(C/p_c)^{8/3}$（该参数下 $n_{\min}\approx10^{-3}$，极弱）；
- 渗流只给连通、不保证 $\ell_e=0$（需环 20 流场公有化）⇒ 必要非充分；概率与 $C$ 外生；符号取主链下移口径，若有限尺寸定义改从上方趋近则推 11 被否证（可证伪分支）；
- 新交付：`03_推导工作台/环22_审12_局域锚与全局渗流的并存窗口.md`、`05_Lean验证/CoexistenceWindow.lean`（7 条）、`04_计算验证/环22_审12_并存窗口.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_审12并存窗口.md`；同步主链推 11 注记／`审-12` 行／§16 第 23／55 项／§17、`成果登记.md`（R-58＋3 条否决读法）；
- 数值：双对数斜率 $-0.375000=-3/8$ 精确；$L=4\to400$ 时 $p_c(L)$ 从 $0.5751\to0.5922$ 下移收敛；$n_{\rm eff}=1\to10^4$ 时 $p_c^{\rm loc}$ 从 $0.5427\to0.5912$ 上移；点/键渗流两口径对照；
- 账面更新至 **55 行／35 唯一／28 项推进（A22／B6）**，余 7 项在 C/D；绝对 $T_c$ 结论不变；
- 外部：二维 $\nu=4/3$ 与有限尺寸 shift（arXiv:1106.0354；arXiv:2412.06228；PRL 69, 2670），只作工具与对照。

**第 41 轮补（环 21／`临-9` 引理 A 前提弱化）：**

- **纠错**：引理 A 正文前提已是"一对无理比"，§16 第 17 项的"无穷理性"过强，已纠正；
- 三步弱化：一对无理比 ⇒ 既约分母 $\{q_n\}$ 无界 ⇒ 引理 A 结论 $\mathcal H=0$。核心整数论：若 $c\gamma_n\in\mathbb Z$、$c\gamma_1=k$、$\gamma_n/\gamma_1=p_n/q_n$ 既约，则 $q_n\mid k$；无界 ⇒ $k=0$（Lean 证）；
- 障碍精确定位：分母有界 ⇒ 虚部落在格点 $(\gamma_1/Q)\mathbb Z$，容量 $\sim T/\alpha$ 线性，与 Riemann–von Mangoldt $N(T)\sim T\ln T/(2\pi)$ 超线性矛盾（**条件于每格点零点数有界**）；LI 猜想与单个虚部无理性仍是外部未证；
- 新交付：`03_推导工作台/环21_临9_引理A前提的弱化.md`、`05_Lean验证/LemmaAPremise.lean`（4 条）、`04_计算验证/环21_临9_引理A前提弱化.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_临9引理A前提弱化.md`；同步主链引理 A 注记／`临-9` 缺口行／§16 第 17／56 项／§17、`成果登记.md`（R-59＋3 条否决读法）；
- 数值：格距 $\alpha=0.565388$（$Q=25$）、计数与格点容量交叉 $T\approx6.75\times10^4$；$c=0$ 同相满足率 1.0、$c>0$ 最大 0.167；数值逼近分母不证明无界性（已注明）；
- 账面更新至 **56 行／35 唯一／29 项推进（A23／B6）**，余 6 项在 C/D；绝对 $T_c$ 结论不变；
- 外部：LI 猜想（arXiv:2311.04860；arXiv:0807.2118）、单个虚部无理性未证（arXiv:1109.1788v2），只作工具与对照。

**第 42 轮补（环 14／`临-14` 前夜冻结三态）：**

- 由 (5.4) $\tau_i=\int v_{\tau,i}dt$ 与 $\mathcal H_{ij}=\tau_i-\tau_j$ 得 $\dot{\mathcal H}_{ij}=v_{\tau,i}-v_{\tau,j}$ ⇒ **全对冻结 ⇔ 流速场全域公有化**（补 (22.3) 反向，充要）；冻结关系是等价关系、连通分量给部分冻结；
- 三态：态1 场未公有化→$c_{ij}$ 漂移；态2 场公有化起点未齐→$c_{ij}=a_i-a_j$（1-余缘，`临-17`）；态3 全齐→$c_{ij}=0$（`临-16` 不可达）。对 §16 第 8 项的回答：前夜**可以**冻结（态2），只需场先公有化而起点未齐，不要求相变发生；
- 可证伪判据：测 $\dot c_{ij}$——非零⇒态1；零但某些 $c_{ij}\ne0$⇒态2；全零⇒态3（不可达）；
- 新交付：`03_推导工作台/环14_临14_前夜冻结的充要条件与三态.md`、`05_Lean验证/FrozenPremise.lean`（7 条）、`04_计算验证/环14_临14_前夜冻结三态.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_临14前夜冻结三态.md`；同步主链环 14 缺口行／§16 第 8／57 项／§17、`成果登记.md`（R-60＋3 条否决读法）；
- 数值：漂移率斜率 1.098；冻结图分量数 2→1；三态样本 117/3/0（态3 不可达）；
- 账面更新至 **57 行／35 唯一／30 项推进（A24／B6）**，余 5 项在 C/D；绝对 $T_c$ 结论不变；
- 外部：相位/频率锁定（arXiv:2610.24595；arXiv:1711.03711）、簇同步连通分量（PMC5381716），只作工具与对照。

**第 43 轮补（环 14.A／`审-15` 对数-幂律刻度）：**

- 幂律谱 $E_n=E_1n^p$ 的对数步长统一为 $\Delta\ln E_n=p\ln(1+1/n)=p/n+O(n^{-2})$；CQM (12.3) 是 $p=2$，2D 弯曲声子（$\omega=\alpha q^2$、等距 $q$）也是 $p=2$ ⇒ **同一对数坐标下步长相同**；3D 线性声子 $p=1$（差因子 2 属维度差异）；"对数 vs 幂律步长对不上"是坐标混用；
- 同形**限于对数步长层**：态密度层不同（CQM 计独立差异模式＝参与比，非波矢态）；粗化 $\mathcal H\to\tau$ 的结构＝参考节点规范 (14.0a)＋参与比 (`临-21`)＋熵 $S=\ln\Gamma$，动力学外生；不碰 $\gamma_n$（`临-8` no-go 不动）；
- 新交付：`03_推导工作台/环14A_审15_对数与幂律的刻度相容性.md`、`05_Lean验证/ScaleCompatibility.lean`（4 条）、`04_计算验证/环14A_审15_对数幂律刻度.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_审15对数幂律刻度.md`；同步主链 14.A 注记／缺口行／§16 第 26／58 项／§17、`成果登记.md`（R-61＋3 条否决读法）；
- 数值：同一谱 $\Delta\ln E_n$ 从 1.386 递减、$\Delta E_n$ 从 3 递增（坐标假象）；双对数斜率 $p=1/2$ 精确；$\ln N$ 对 $\ln E$ 斜率 2.000；
- 账面更新至 **58 行／35 唯一／31 项推进（A25／B6）**，余 4 项在 C/D；绝对 $T_c$ 结论不变；
- 外部：3D 声学 $g(\omega)\propto\omega^2$（ScienceDirect）、2D 弯曲 $\omega\propto q^2$，只作工具与对照。

**第 44 轮补（环 14／`临-15` 节点时钟坐标）：**

- 排除性依据：全局坐标 $K_i=K(t)$ ⇒ 读数恒等，与 (13.5) 及 `临-12` 逐模相因子 $e^{-i\gamma_n\Delta_i}$ 矛盾（除非全对 $c_{ij}=0$，`临-16` 不可达）⇒ **全局坐标 no-go**；
- 正面依据（条件性）：节点固有时 $\tau_i$ 逐点定义、保留标签；场公有化后 $\tau_i=\tau_{i_0}+\mathcal H_{i_0i}$ 可重构（`临-14`）；参与比 `临-21` 给"节点＝独立差异模式支撑"；信息保持 4 条 vs 全局压缩 1 条；
- **残余公设精确定位**："节点＝基本单元"若被拒认整环仍失效——no-go 不能排除此拒认，是有条件论证而非无条件推演；
- 新交付：`03_推导工作台/环14_临15_节点时钟坐标的排除性论证.md`、`05_Lean验证/NodeClockCoord.lean`（6 条）、`04_计算验证/环14_临15_节点时钟坐标.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_临15节点时钟坐标.md`；同步主链环 14 缺口行／§16 第 4／59 项／§17、`成果登记.md`（R-62＋3 条否决读法）；
- 数值：全局读数差恒 0、节点差 $c=0.02$ 时 0.007049；$c=10^{-6}$ 时差 $3.69\times10^{-7}$（趋零但 $c=0$ 不可达）；
- 账面更新至 **59 行／35 唯一／32 项推进（A26／B6）**，余 3 项在 C/D；绝对 $T_c$ 结论不变；
- 外部：关系性可观测量依赖时钟自由度（Rovelli 2002/2014；arXiv:1110.2429），只作工具与对照。

**第 45 轮补（四步链条口径修正，用户明确授权）：**

- 四步最终版：①**差异化**（差异产生）→②**扩大化**（差异扩张）→③**平均化**（差异被拉向同一平均）→④**危机化**（**平均量／平均线持续下降**）；
- 关键修正："变负"＝**增长率追不上平均化率**（净增长率为负），是③平均化的**驱动力**，经过③平均化与④平均量下降**两个阶段**，危机化是后一阶段——不是"平均量下降才推出变负"（原稿因果写反，据用户第二轮澄清回改）；不是独立第五步；反趋势因素**内化于④**为内在波动节奏；③→④不需额外机制；(19.2) 的 $\dot{\mathcal D}=\mathcal B\ge0$ 是同一过程的差异侧读数，与平均侧 $\bar v_\tau$ 下降并列；
- **用户授权范围**：修正推导链、缺口及所有文档——本轮据此同步 01 核心理论 §2.3／§4.1、06 命题⑦／对照表、主链环 19 注记与 §2.3 对应行／§17（唯一一次改及 01／06 原文，已登记）；
- 新交付：`03_推导工作台/全链_四步链条口径修正.md`、`05_Lean验证/FourStageChain.lean`（四构造器＋6 条）、`04_计算验证/全链_四步链条.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_四步链条口径修正.md`、`成果登记.md`（R-63＋3 条否决读法）；
- 数值：①方差 0→0.982、②节点 5→49.8、③方差 1→0.156（残余底）、④平均线 1.0→0.400、增长率恒 -0.600（变负）＋内化波动；
- 缺口编号与状态栏一律不动；危机 ≠ 相变、`临-25`、`审-12` 等既有判定全部保留；绝对 $T_c$ 结论不变。

**第 46 轮补（环 4/9/10／`审-3` 零方差钉死）：**

- `审-3` 把 $\sigma^2$ 钉死为 $\sigma_0^2$：(4.1) 的 $[1+2n_B]$ 给 $\sigma^2(T)=\sigma_0^2\coth(\hbar\omega/2k_BT)$，$\sigma_0^2=\sum_kG_{ek}^2\frac{\hbar}{2\rho_m\omega_k}$（$T=0$ 零点项）；
- (10.2) 的 $\kappa_{ij}$ 下标 $_0$ 明确零点方差 ⇒ (9.1)(10.2) 用 $\sigma_0^2$、**与 $T$ 无关**；温度只经 (4.1)→(15.1) 唯一入口进入；若塞热方差会重复计入 $T$、破坏唯一入口；符号对齐（$T\uparrow\Rightarrow\sigma^2(T)\uparrow$）由 $[1+2n_B]$ 保证；
- 新交付：`03_推导工作台/环09_审3_零方差钉死与温度唯一入口.md`、`05_Lean验证/ZeroPointVariance.lean`（6 条）、`04_计算验证/环09_审3_零方差与温度入口.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_审3零方差钉死.md`；同步主链环 9／环 10 缺口行／§16 第 12／60 项／§17、`成果登记.md`（R-64＋2 条否决读法）；
- 数值：coth 恒等式最大误差 $5.684\times10^{-14}$；$T=0.010\to16.144$ 时因子 $1.000\to32.299$；(9.1)(10.2) 恒为 $\sigma_0^2$（温度唯一入口）；
- 账面更新至 **60 行／35 唯一／33 项推进（A27／B6）**，余 2 项在 C/D；绝对 $T_c$ 结论不变；
- 外部：QHO 方差 $\coth$ 形式（Wikipedia QHO；TU Delft 讲义；Likharev FDT），只作工具与对照。

**第 47 轮补（环 20／`临-4` 判据充分性否证）：**

- 三点反例 $\tau=(1,-1,0)$、$v=(0,0,1)$ 给 $\dot{\mathcal D}=2[0-1+1]=0$ 而 $v_1\ne v_3$（Lean 证）⇒ **(20.2) 充分性严格不成立**（判否，非悬置的"未证"）；必要方向成立但平凡；
- 判据接口按 §9.A(五) 同口径：回溯必然／前瞻偶然，充分判据需偶然项（`审-11`／`临-16`／材料统计，外生）；"与 $T$ 无关"不构成对必要性的反驳（必要可不出现在 $T$ 式中，只说明该式不能当 $T_c$ 判据）；
- 新交付：`03_推导工作台/环20_临4_判据充分性的否证与接口.md`、`05_Lean验证/CriterionSufficiency.lean`（4 条）、`04_计算验证/环20_临4_判据充分性.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_临4判据充分性.md`；同步主链环 20 缺口行／§16 第 14／61 项／§17、`成果登记.md`（R-65＋3 条否决读法）；
- 数值：逐对贡献 $0,-1,+1$ 求和为零；$v_3=-2\to2$ 时 $\dot D$ 恒 0（偏差 0）而 $|v_3-v_1|$ 恒 2（无判别力）；
- 账面更新至 **61 行／35 唯一／34 项推进（A28／B6）**，余 1 项在 C/D；绝对 $T_c$ 结论不变；
- 外部：Kuramoto 必要/充分条件不等价（arXiv:2007.04343；arXiv:2503.19781），只作工具与对照。

**第 48 轮补（环 22／`临-16` 全对归零不可达）：**

- 把定性"不可达"升级为**测度零＋规范平凡**双重判据：$c_{ij}=a_i-a_j$ 核是常向量（`临-17`），"$c_{ij}$ 不能靠规范消掉"精确化为**相对值 $N-1$ 维不可消、整体平移 1 维可消但无效应**；连续分布下全对相等测度零（离散 $M/M^N=1/M^{N-1}\to0$，Lean 证指数衰减）；人为归零只是同步规范、无可观测效应；全对平台既非相变必要也非可实现目标——不可达是双重排除，非逻辑矛盾；
- 新交付：`03_推导工作台/环22_临16_全对归零的测度零与规范平凡.md`、`05_Lean验证/AllZeroUnreachable.lean`（4 条）、`04_计算验证/环22_临16_全对归零测度零.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_临16全对归零.md`；同步主链 (22.4) 注记／§16 第 5／62 项／§17、`成果登记.md`（R-66＋3 条否决读法）；
- 数值：$N=20$ 时概率 $10^{-6}$～$10^{-18}$；连续样本全对归零频率 0/2000、$\max|c_{ij}|$ 最小 1.0717；核内平移差 $4.4\times10^{-16}$；
- 账面更新至 **62 行／35 唯一／35 项推进（A29／B6）**，余 0 项在 C/D；绝对 $T_c$ 结论不变；
- 外部：连续随机变量相等测度零（Wikipedia *Almost surely*；Math SE），只作工具与对照。

**第 49 轮补（全链综合计算检验，C/D 清零后）：**

- 把已推形状串到共同 $T$/$p$ 轴：热方差升（(4.1)）→ $p_{\rm pair}$ 左尾升（前夜配对）→ 相位刚度降在 $T_{\rm BKT}$ 截断 → $T_c=\min\{T^*,T_{\rm BKT},T_\theta\}$ 自洽给 dome；**结构相容、无矛盾**；
- **非拟合**：外生参数只用主链已登记口径（$T_{\rm BKT}/T_{\rm bare}=0.7441$–$0.7831$、$p_c=0.592746$、$\sigma_a$ 示意），不调参贴合实验；外生输入清单 5 项明确（$\sigma_0^2$、$t_\Upsilon$、$J,c$、$\sigma_a$、三温度数值）——绝对 $T_c$ 仍需材料值，B 类判否不变；
- 新交付：`03_推导工作台/全链_形状相容性综合检验.md`、`05_Lean验证/ShapeCompatibilityCheck.lean`（6 条）、`04_计算验证/全链_形状相容性.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_形状相容性综合检验.md`、`成果登记.md`（R-67）；
- 数值：热因子 $T=0.01\to100$ 时 $1.000\to200.00$；$R_n=[0.961,0.915,0.882,0.831,0.754]$（高频衰减）；dome 形状峰位 $p\approx0.157$（示意，非实验值）；
- **账面不变**：62 行／35 唯一／35 推进／0 余；所有编号与"未闭合"状态原样保留。

**第 50 轮补（环 26／`临-8` 有限模读出，正面挑战最强 no-go）：**

- 找到 no-go A 的前提过强之处：它要求"无穷多模全部逐模对齐"，但 (26.A4) 链内已声明高频模不可读——真实对象是**低阶可读子集上的截断读出**，不是全模恒等式；
- 有限模读出定理：$K_{\rm phys}=-\sum_{n\le N_*}\frac{e^{i\gamma_n t}}{\rho_n}W_n+R_{N_*}$，误差 $|R_{N_*}|\le\sum_{n>N_*}|W_n|/|\rho_n|$ 有界（$|\rho_n|\ge\gamma_n$、$\Gamma_n\propto\gamma_n^2$ 使高阶指数衰减）——**不推翻恒等 no-go**（`nogo_two_modes` 保持），把正结果从定性代表元升级为定量截断读出＋误差界；
- 新交付：`03_推导工作台/环26_临8_有限模读出定理.md`、`05_Lean验证/FiniteModeReadout.lean`（5 条）、`04_计算验证/环26_临8_有限模读出.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_临8有限模读出.md`、`成果登记.md`（R-68＋2 条否决读法）；
- 数值：尾部误差 $N=1\to6$ 时 $10^{-2}\to10^{-7}$、窗口定 $N_*=2$（示意）、近似相对误差 $N=2\to10$ 时 $0.259\to6.8\times10^{-4}$、率 $0.90\to3.33$ 依 n 变（no-go 保持）；
- 账面不变（62 行/35 唯一/35 推进/0 余）；$\sigma_v^2\tau_g$／$N_*$ 外生。

**第 51 轮补（S6/V1 量纲与极限核对，数据对照第一步）：**

- 研究纲领 S6 数据对照此前从未执行；V1 是协议中"链闭合后先做、不需材料、不调参"的第一步，本轮补上；
- ①③④通过：量纲一致、高温无"升温配对增强"反向符号（`审-3` 已证 $\sigma^2\propto T$）、2D→BKT／3D→相位相干方向已判（`审-11`）；
- ②BCS 弱耦合退化：条件钉死为五条（C1–C5），**C5＝存在独立能隙方程硬阻断**（链无独立能隙方程，D01 明示）⇒只写条件清单、不声称证明、**不进 V2 盲测**；与"同形已证同刻度未证"一致；
- 新交付：`03_推导工作台/全链_V1量纲与极限核对.md`、`05_Lean验证/V1Limits.lean`（4 条）、`04_计算验证/全链_V1量纲与极限.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_V1量纲与极限核对.md`、`成果登记.md`（R-69＋2 条）；
- 数值：BCS 比 $2\pi/e^\gamma=3.5278$（外部口径）、高温 $\sigma^2=32.25\to200$ 线性、$d=2$ 维度选择；
- 账面不变（62 行/35 唯一/35 推进/0 余）；C5 是下一阶段入口，非新 CQM 编号。

**第 52 轮补（振幅扇区能隙方程，补 C5）：**

- 从已登记的 (目标.2) $T^*=1.13\hbar\omega_{\log}e^{-1/\lambda}$（$1.13=2e^\gamma/\pi$）反推 C5：BCS 中 $T_c$ 与 $\Delta(0)$ 出自同一隙方程两极限，CQM 既登记 $T^*$ 极限，同源必给 $\Delta(0)=\frac{\pi}{e^\gamma}k_BT^*$、$2\Delta/k_BT^*=2\pi/e^\gamma\approx3.528$；
- 输入全用 CQM 对象：$N(0)V\to\lambda$（记忆核对数矩）、参与比加权、$\omega_D$ 截断、$\omega_{\log}^{\rm amp}=e^{-1/3}\omega_D$——**不把 BCS 强加**，是从已登记 $T^*$ 反推同源极限；
- **C5 由阻断升为条件具备（弱耦合 s 波单带）**；V1② 在限定条件下通过、V1 四项全通过；仍不进 V2（无材料数据）；绝对值外生（$\lambda$、$\omega_D$）、强耦合 $\alpha^2F$ 缺（D01）；
- 新交付：`03_推导工作台/环目标_振幅扇区能隙方程.md`、`05_Lean验证/AmplitudeGapEquation.lean`（4 条）、`04_计算验证/环目标_振幅扇区能隙方程.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_振幅扇区能隙方程.md`、`成果登记.md`（R-70＋2 条）；
- 数值：普适比 3.5278 不随 $\lambda$ 变、$\Delta(0)=1.764\,k_BT^*$、$e^{-1/3}=0.7165$；账面不变。

**第 53 轮补（V2 第一步：元素超导量级与符号，首次真实数据对照）：**

- **首次真实文献数据对照**：14 元素实测 $(T_c,\theta_D)$（Webb, Marsiglio & Hirsch, arXiv:1502.04724, Table III）代入 CQM 已登记 $T^*=1.13e^{-1/3}\theta_D e^{-1/\lambda}$ 反解 $\lambda$；
- 预注册判据：P1 符号（$\lambda>0$）通过、P2 量级（$\lambda\in(0,2)$，实测 $[0.167,0.405]$）通过、P3 扇区结构（$\Delta(1/\lambda)=1/3$，偏差 $6\times10^{-16}$）通过；**P4 绝对精度不判定**（缺独立 $\lambda$ 实测表与 $\mu^*$，Webb 综述确认是链外缺口）——**不宣称通过 V2**；
- 反解 $\lambda\approx0.17$–$0.41$ 小于 Eliashberg $\lambda$（Al $\approx0.43$、Pb $\approx1.5$）的根因是简单指数公式缺 $\mu^*$ 与 $1.04(1+\lambda)$ 修正，属已知链外缺口（Webb 综述"superflexibility"），不是理论失败；
- 新交付：`03_推导工作台/全链_V2元素超导量级与符号.md`、`05_Lean验证/V2ElementDiagnostic.lean`（4 条）、`04_计算验证/全链_V2元素超导量级.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_V2元素超导量级.md`、`成果登记.md`（R-71＋3 条）；
- 数据标源：Webb 2015 arXiv:1502.04724 Table III（逐元素 $T_c$、$\theta_D$）；账面不变。

**第 54 轮补（1.13 系数口径核查，回到物理本身的核对）：**

- Webb 2015 式(1) $1.13=2e^\gamma/\pi$ 配 **Debye 截断 $\hbar\omega_D$**，式(2) McMillan 配对数矩 $\omega_{\ln}$ 且系数 $1/1.2$；CQM (目标.2) 用 $1.13\times\omega_{\log}=1.13e^{-1/3}\theta_D$——"BCS 系数＋Eliashberg 对数矩"混搭，弱耦合极限比标准 BCS 低 $e^{-1/3}=0.7165$（**刻度**差）；
- **形状层不受影响**：gap ratio $2\pi/e^\gamma$、凹性、扇区结构、V2 P1–P3 均与前因子频率无关（Lean `gap_ratio_independent_of_omega` 证）；受影响的 $T_c$ 绝对值本就外生（`审-10`／Z2）；与 `审-15` 同形/同刻度同类；
- 按"不虚构、不绕过"**不改权威式**，只加注记明确口径；V2 反解两口径差 $e^{-1/3}$ 平移，远小于缺 $\mu^*$ 造成的差距（再次确认 P4 根因）；
- 新交付：`03_推导工作台/环目标_113系数与omega对数矩口径核查.md`、`05_Lean验证/BCSCoefficient.lean`（4 条）、`04_计算验证/环目标_113系数口径.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_113系数口径核查.md`、`成果登记.md`（R-72＋2 条）；主链 (目标.2)/(目标.3) 加注记；账面不变。

**第 55 轮补（重大发现：P4 根因精确定位）：**

- Marsiglio 2018（arXiv:1807.04907，已 webfetch）给同一 bare $\lambda\equiv g_{\epsilon_F}|V|$（与 CQM (10.3) $N(0)\sum|V|$ 同类）的 BCS(13) $e^{-1/\lambda}$、含重整化(14) $e^{-(1+\lambda)/\lambda}$、弱耦合精确(37) $\frac{1.13}{\sqrt e}\omega_E e^{-(1+\lambda)/\lambda}$；
- **发现**：CQM (目标.2) 用裸指数 $e^{-1/\lambda}$，**缺 Eliashberg 质量增强 $e^{-(1+\lambda)/\lambda}$**（重整化严格压低 $T_c$ 一个 $e^{-1}$，Lean 证）；8 元素实测反解两口径比 $E/C=1.25$–$1.90$ **单调随耦合增**，正是 $Z=1+\lambda$ 的定性特征；
- P4 根因精确定位：缺 $1+\lambda$ 重整化（主）＋缺 $\mu^*$（次）＋对数矩口径 $e^{-1/3}$（次）——都属形状/刻度缺口，非实验否证；链内 $v_\tau$ 拖曳对应 $Z=1+\lambda$，但写入 (目标.2) 是新机制、波及 C5/V1/V2，**待用户授权**；
- 新交付：`03_推导工作台/环目标_Eliashberg重整化缺失与P4根因.md`、`05_Lean验证/EliashbergRenorm.lean`（4 条）、`04_计算验证/环目标_Eliashberg重整化.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_Eliashberg重整化P4根因.md`、`成果登记.md`（R-73＋2 条）；账面不变。

**第 56 轮补（授权修正：(目标.2) 写入 $Z=1+\lambda$）：**

- 执行用户持续授权"有理有据修正方程"＋上轮征询：(目标.2) 指数 $-1/\lambda\to-(1+\lambda)/\lambda$（带注记，06 DM.8 原文未动）；$Z$ 对应链内 $v_\tau$ 场被声子云拖曳 $v_\tau\to v_\tau/(1+\lambda)$（场是对象、改造落在场）；
- 三项严格依据：①上轮恒定比 $0.312$ 精确 $=e^{-7/6}=e^{-1}$（质量增强）$\times e^{-1/6}$（对数矩口径差，第54轮）——纯代数；②写入后反解 $\lambda$ 与 Eliashberg Eq37 平均偏差 $31.4\%\to6.4\%$；③**形状中性**——$Z$ 对 $T^*$ 与 $\Delta(0)$ 同乘 $e^{-1}$、gap ratio $3.528$ 不变，已推形状全部不变；
- **P4 仍不闭合**：剩余 $6.4\%$ 来自对数矩口径 $e^{-1/6}$ 与 $\mu^*$（`审-14`）；这是【构造修正】（文献＋代数＋定量），非 CQM 第一性证明；缺口编号、状态栏、账面不变；
- 新交付：`03_推导工作台/环目标_Z重整化的授权修正.md`、`05_Lean验证/ZRenormWrite.lean`（4 条）、`04_计算验证/环目标_Z重整化写入.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_Z重整化授权修正.md`、`成果登记.md`（R-74＋2 条）；主链 (目标.2)＋C5 注记同步。

**第 57 轮补（Karakozov 前因子修正，CQM 与 Eliashberg Eq37 精确重合）：**

- (目标.2) 二次修正：前因子 $1.13\hbar\omega_{\log}\to1.13e^{-1/6}\hbar\omega_{\log}=1.13e^{-1/2}\hbar\theta_D$（补 Karakozov 因子，Marsiglio arXiv:1807.04907 式26："$1.134/e^{1/2}$ instead of $2e^\gamma/\pi$"）；截断 $e^{-1/2}$ 经 CQM 对数矩 $\omega_{\log}=e^{-1/3}\theta_D$ 换算即 $e^{-1/6}$；
- 数值：修正后前因子 $0.68538$ 与 Eq37 **逐位相同**，8 元素反解 $\lambda$ 偏差 $6.4\%\to0$；形状中性（gap ratio 3.5278 不变）；
- **P4 刻度障碍清零**：前因子＋指数均与 Eq37 对齐，唯一剩余 $\mu^\ast$（`审-14` 链外材料输入，红线不凭空造）；构造修正，非第一性证明；第54轮口径差的精确分解＝对数矩 $e^{-1/3}$＋Karakozov $e^{-1/6}$，二者分别处理；
- 新交付：`03_推导工作台/环目标_Karakozov前因子修正.md`、`05_Lean验证/KarakozovPrefactor.lean`（4 条）、`04_计算验证/环目标_Karakozov前因子.py`／`.png`／`.csv`、`06_决策记录/2026-11-22_Karakozov前因子.md`、`成果登记.md`（R-75＋2 条）；主链 (目标.2) 二次修正注记同步。

**第 58 轮补（首次从头算到尾正算验证）：**

- **首次正算**（前 57 轮数据对照均为反解）：CQM 完整输出（$T^*$ 对齐 Eq37、$\omega_{\log}=e^{-1/3}\theta_D$）代入 Webb 式(6) Mitrović 公式（不含 $\mu^\ast$），正算 gap ratio 与实验对照；
- 8 元素（Webb Table III）平均偏差 **2.7%**（Al +2.7%、Pb −2.1%、V −0.4%、In +6.8%），强耦合偏离趋势正确，同位素端点 $\alpha\in\{0,1/2\}$ 覆盖实验 0.15–0.50；**无反解、无调参、无拟合**；
- gap ratio 分支不依赖 $\mu^\ast$（外部标准：Eliashberg 弱耦合比对数抵消）——不是绕过缺口，是该可观测量本就不需要它；**绝对 $T_c$ 仍卡 $\mu^\ast$**（`审-14`）；
- 新交付：`03_推导工作台/全链_正算gap比首次验证.md`、`05_Lean验证/ForwardGapRatio.lean`（4 条）、`04_计算验证/全链_正算gap比.py`／`.png`／`.csv`、`06_决策记录/2026-11-23_正算gap比首次验证.md`、`成果登记.md`（R-76＋2 条）；账面不变。

**第 59 轮补（当前有效口径表，防干扰整理）：**

- 建立 `00_当前有效口径表.md`：把 58 轮两次修正的 (目标.2) 最终式、gap ratio、B 类判否、外生输入收束成**单一权威表**——后续推演只引用此表；
- 5 张含旧式 $e^{-1/\lambda}$ 的历史卡（V2量级、双扇区、113口径、Z修正、能隙方程）加"口径已更新"防干扰注记（**不删除、保可追溯**）；权威顺序＝主链 > 口径表 > 历史卡；
- 确认主链 (目标.2) 第827行只有最终式、无旧式残留；gap ratio $2\pi/e^\gamma=3.528$ 与全部 B 类判否不受 $T^*$ 修正影响；
- 新交付：`00_当前有效口径表.md`、`06_决策记录/2026-11-23_当前有效口径表.md`、`成果登记.md`（R-77）；不改主链/编号/账面。

**第 60 轮补（$\mu^\ast$ 形状归口）：**

- $\mu^\ast$（`审-14`）从"完全外生"推进为"泛函形状已知（Webb 式5 / Morel-Anderson 1962：$\mu^\ast=\mu/(1+\mu\ln(\epsilon_F/\hbar\omega_D))$）＋材料量 $\mu,\epsilon_F$ 外生"；绝对 $T_c$ 缺口从笼统的"$\mu^\ast$ 外生"**精确到两个具体材料量** bare 库仑 $\mu$ 与 Fermi 能 $\epsilon_F$（链内无库仑通道、无费米面能标）；
- Lean `MuStarShape.lean`（5 条全证：$\mu^\ast>0$、$\mu^\ast<\mu$、对 $\mu$ 单调、极限形、$\mu^\ast<1/L$）；数值 `环目标_mu星与绝对Tc.py`／`.png`／`.csv`：M.1 形状＋绝热极限＋Allen-Dynes 敏感性（$\lambda=0.8$ 固定，$\mu^\ast:0\to0.3\Rightarrow T_c:16.1\to0.81$K，证实 $\mu^\ast$ 决定性）＋8 元素反解 $\lambda(\mu^\ast)$；
- **诚实边界**：AD 敏感性/反解是外部式＋CQM $\omega_{\log}$ 一个输入，**不是从头算到尾**；独立 $(\lambda,\mu^\ast)$ 实测对仍未接入（`07_数据与现象/数据/` 空）；
- 新交付：`03_推导工作台/环目标_mu星形状归口.md`、`05_Lean验证/MuStarShape.lean`、`04_计算验证/环目标_mu星与绝对Tc.py`／`.png`／`.csv`、`06_决策记录/2026-11-23_mu星形状归口.md`、`成果登记.md`（R-78）；不改主链/编号/账面。

**第 61 轮补（同位素中间值：接入链外成分、首次双观测量约束）：**

- 按第10轮卡 T10.3 指定的合法路径，接入第60轮归口的 $\mu^\ast$ 形状（**链外成分**），对 $T_c$ 求质量导数得 $\alpha=\frac12[1-\frac{1.04(1+\lambda)(1+0.62\lambda)\mu^{\ast2}}{(\lambda-\mu^\ast(1+0.62\lambda))^2}]$；
- **60轮来首次双观测量联立约束**：CQM $\omega_{\log}=e^{-1/3}\theta_D$＋实测 $T_c$＋实测 $\alpha$（Webb Table III）解 $(\lambda,\mu^\ast)$——13 元素全解出，8/13 $\mu^\ast\in[0.1,0.3]$ 常规区间，低 $T_c$→低 $\alpha$→高 $\mu^\ast$ 定性吻合 Webb §IV；无调参无拟合；
- Lean `IsotopeIntermediate.lean`（6 条全证）；数值 `环10_同位素中间值双观测.py`／`.png`／`.csv`；
- **边界**：$\mu^\ast$ 是链外成分（非纯链内），绝对 $T_c$ 仍未从头算到尾，`审-10` 不闭合；Zr/Ru $\alpha=0$ 属模型边界；
- 新交付：`03_推导工作台/环10_同位素中间值_链外成分接入.md`、`05_Lean验证/IsotopeIntermediate.lean`、`04_计算验证/环10_同位素中间值双观测.py`／`.png`／`.csv`、`06_决策记录/2026-11-23_同位素中间值链外接入.md`、`成果登记.md`（R-79）；不改主链/编号/账面。

**第 62 轮补（回查 Karakozov 前因子与对数矩定义，诚实降级）：**

- **发现一**：Marsiglio 原文式(7) 确认 Eq37 的 $1/\sqrt e$ 前因子是 **Einstein 谱**结果；任意谱的精确解在 Combescot PRB42 7810 (1990)（付费墙未核）——第57轮"与 Eq37 精确重合"是同谱代数自洽，降级为"形式对齐、跨谱待核"；
- **发现二（更深）**：CQM $\omega_{\log}$（$3y^2$ 电子态密度矩，$e^{-1/3}$）与 Eliashberg $\omega_{\ln}$（Webb 式3，$\alpha^2F/\nu$ 权重，Debye 给 $e^{-1/2}$）**是两个不同的矩，差 $e^{1/6}$**——第57/58/60/61轮跨定义代入须加边界注记；
- **回头重算**：用正确矩 $e^{-1/2}$ 重算 gap ratio，平均偏差 2.7%→**2.9%**（量级稳健，强耦合元素改善：Nb −1.1%→+0.7%、V −0.4%→+0.1%）；第58轮 2.7% 精确值依赖错矩，核心量级不变；
- 登记临时缺口 `审-16`（Einstein 前因子跨谱合法性）、`审-17`（两矩对应关系）；Lean 复用 `IsotopeScaling.lean`（已证 $e^{-1/2}<e^{-1/3}$、比值 $e^{-1/6}$）；
- 新交付：两张审查卡、`审_Eliashberg矩重算gap比.py`／`.png`／`.csv`、决策记录、`成果登记.md`（R-80）；主链权威式/编号/状态栏/账面均未动；未提交。

**第 63 轮补（方向纠偏审视——本轮核心产出）：**

- **诚实审视第55–62轮**：发现最近8轮全在目标区/唯象层用外部 Eliashberg 式做"对齐"，CQM 三处核心机制断口（$审-10$／$审-1$／$临-25$）与 $D1$、$审-11$ 一个都没碰——与主链第1559行"机制优先于判据、用外部标准式填补机制断口正是绕过"的警告相悖；
- **最权威依据 06 命题 Z2**（第192行）：CQM 被定义为**无量纲形状/普适类理论**，$J_0/\theta_D$ 必为外生能标，绝对 $T_c$ 原则上不可从链内推出——升级须新增带量纲公设（框架扩展，需授权）。最近8轮求绝对 $T_c$ 本质是试图绕过 Z2；
- **矩分歧链内不可修**：CQM 无 $\alpha^2F$ 原生对象（14.A1【外部·标准物理】、同形但刻度未证、`审-15` 不闭合），第62轮 $3y^2$ vs $\alpha^2F/\nu$ 的分歧在框架内无法修正；
- **三路线建议**（供决策）：A 回机制（需新增链内要素，框架已到边界）／B 接数据（材料 $\alpha^2F$／$\mu^\ast$）／C 诚实定位为"检验"而非"推进缺口"；
- 新交付：`06_决策记录/2026-11-23_第55至62轮方向纠偏审视.md`、`成果登记.md`（R-81）；不改主链/编号/账面。

**第 65 轮补（FE01 框架扩展候选——未落地）：**

- 按 06 命题 Z2 指明的唯一升级路径（新增带量纲公设），在综合文件夹 `08_框架扩展候选/` 给出**最小公设** $\omega_D=a\sqrt{\kappa_s/M}(6\pi^2n)^{1/3}$→$\theta_D$，把已推 $T^*$ 形状式闭合为绝对 $T_c$ 候选式（FE.3）；
- 同位素标度 $T_c\propto M^{-1/2}$（$\alpha=1/2$）自洽：Lean `FE01_EnergyScale.lean`（5 条，退出码 0）＋数值斜率 $-0.5000$；
- 数值四面板 `FE01_能标闭合.py`／`.png`／`.csv`（无拟合）：$T_c$–$\lambda$、同位素直线、德拜标度、Webb $\theta_D$ 反推 $\kappa/M$（量级合理，声速偏低 2–3 倍已标注）；
- **严格边界**：候选·未落地·不碰权威源；$\kappa_s,M,a,n,\lambda$ 仍材料输入，非纯链内；$\mu^\ast$ 未纳入（`审-14` 不动）；两矩分歧（B 类）仍待核；升级正式理论需明确授权；
- 新交付：`08_框架扩展候选/`（README＋FE01 卡）、`05_Lean验证/FE01_EnergyScale.lean`、`04_计算验证/FE01_能标闭合.py`／`.png`／`.csv`、`06_决策记录/2026-11-23_FE01框架扩展候选.md`、`成果登记.md`（FE01 候选）；不改主链/编号/账面。

**第 66 轮补（FE02 数论能标 no-go——否定性结果）：**

- 审查最深"革命"设想：不用外生能标、直接从 CQM 零点谱推能标——**否定**。`临-22` 证 $\Gamma_1\propto\gamma_1^2T/\omega_D^2$ 循环依赖被替代的 $\omega_D$；`临-8` 强 no-go 禁止物理核与 ζ 形式焊接；自洽 $w^4=kC\gamma_1^2T$ 仍需外生 $T,k,C$；
- **数论单独定不出能标**——这是命题 Z2 的深层原因（几何/数论层全无量纲）。FE02 印证 FE01 的外生声学公设是必要最小扩展；
- Lean `FE02_NoGo.lean`（4 条实质定理，退出码 0 无警告）；数值四面板 `FE02_数论能标循环.py`／`.png`／`.csv`（无拟合）；
- **明确标注为否定性结果**保留，防止后续再走此路（用户"放弃不对劲内容防干扰"）；候选·未落地·不碰权威源；不动任何编号与状态栏、账面；
- 新交付：`08_框架扩展候选/FE02_数论能标自洽性审查.md`、`05_Lean验证/FE02_NoGo.lean`、`04_计算验证/FE02_数论能标循环.py`／`.png`／`.csv`、`06_决策记录/2026-11-23_FE02数论能标no-go.md`、`成果登记.md`（FE02 候选）；不改主链/编号/账面。

**第 67 轮补（FE03 完整绝对 $T_c$ 候选式）：**

- **首次合并三要素**：FE01 外生能标＋第60轮 $\mu^\ast$ 形状＋第62轮矩分歧，成完整绝对 $T_c$ 候选式（Allen–Dynes）；
- **核心结果**：CQM 矩 $e^{-1/3}$ 系统高估绝对 $T_c$ **18.1%**（$e^{1/6}=1.1814$，与 $\lambda$ 无关），候选式对照实验必须用 Eliashberg 矩 $e^{-1/2}$（与 AD 定义一致）；$\mu^\ast:0\to0.2$ 压制 $T_c:8.09\to1.40$K；
- Lean `FE03_CompleteTc.lean`（5 条，退出码 0）；数值四面板 `FE03_完整Tc与矩选择.py`／`.png`／`.csv`（回代明确标为自洽核对，非独立验证）；
- **严格边界**：候选·未落地·不碰权威源；外部 AD 式＋FE01 公设，非纯链内；不动任何编号与状态栏、账面；
- 新交付：`08_框架扩展候选/FE03_完整Tc式与矩选择敏感性.md`、`05_Lean验证/FE03_CompleteTc.lean`、`04_计算验证/FE03_完整Tc与矩选择.py`／`.png`／`.csv`、`06_决策记录/2026-11-23_FE03完整Tc候选.md`、`成果登记.md`（FE03 候选）；不改主链/编号/账面。

**第 68 轮补（FE04 前因子文献坐实）：**

- **调研命中关键开放文献** arXiv:1910.04579（Phan & Chubukov, PRB 101, 024503 (2020)）：绝热区精确前因子 $T_c=1.13e^{-3/2}\omega_D e^{-1/\lambda}=0.252\omega_D e^{-1/\lambda}$（式III.29），Table2 分解 $e^{-1}$(自能)×$e^{-1/2}$(频率依赖)×$1$(KL)；
- **核心结果**：CQM 展开 $1.13e^{-1/6}(e^{-1/3}\theta_D)e^{-(1+\lambda)/\lambda}=1.13e^{-3/2}\theta_D e^{-1/\lambda}$——与 Chubukov 式III.29、Marsiglio Eq37 **逐因子一致**（数值差 $10^{-15}$，$1.13e^{-3/2}=0.25214\approx0.252$）；第56轮 Z＋第57轮 Karakozov 修正获独立确证；
- 第62轮"跨谱待核"**部分化解**：$e^{-1/2}$ 频率依赖因子在绝热区（$\omega_D$ 动态核）通用，从"完全待核"前进到"绝热区已确证、完全任意谱仍待核（Combescot 付费墙）"；
- Lean `FE04_PrefactorConfirm.lean`（4 条，退出码 0）；数值 `FE04_前因子核对.py`／`.png`／`.csv`；
- **边界**：候选·未落地·不碰权威源；是独立文献确证 CQM 构造式、非 CQM 第一性证明；不动任何编号与状态栏、账面；
- 新交付：`08_框架扩展候选/FE04_前因子e3/2文献坐实.md`、`05_Lean验证/FE04_PrefactorConfirm.lean`、`04_计算验证/FE04_前因子核对.py`／`.png`／`.csv`、`06_决策记录/2026-11-23_FE04前因子文献坐实.md`、`成果登记.md`（FE04 候选）；不改主链/编号/账面。

**第 69 轮补（Pb 双带实验 ↔ CQM 12.A 多模式结构）：**

- **调研命中关键实验** Ruby et al. PRL 114, 157001 (2015)（arXiv:1409.6638）：STS 直接证明 Pb 双带（两准粒子峰差 150 μeV ~10%，FS1 s-p / FS2 p-d 不同耦合），V/Ta 等亦有此行为；
- **12.A 首个独立实验佐证**：CQM 模式集 $\{2,4,6,\ldots\}$、$\{2\}$ 第一档、$n=4$ 高模式待填——Pb 双带 FS1↔$n=2$、FS2↔$n=4$；但 `临-5`/`临-6`（高模式载体与归一未写出）仍不闭合；
- **单带 gap ratio 偏差的材料侧解释**：双带叠加加 10% 能隙分裂，$w_1\approx0.8$ 把 Pb 偏差 −2.1%（4.198）→−0.2%（4.282）；CQM 12.A3 权重 $w_1=2/3$ 给 +1.1% 量级相容；第58轮 2.7% 需加边界（多带元素需修正）；非拟合（权重/分裂取实测范围）；
- Lean `TwoBandGap.lean`（5 条，退出码 0）；数值 `审_双带Pb与gap比偏差.py`／`.png`／`.csv`；
- 新交付：`03_推导工作台/审_双带实验与12A多模式对接.md`、`05_Lean验证/TwoBandGap.lean`、`04_计算验证/审_双带Pb与gap比偏差.py`／`.png`／`.csv`、`06_决策记录/2026-11-23_双带实验与12A对接.md`、`成果登记.md`（R-82）；不改主链/编号/账面。

**第 70 轮补（FE05 首次端到端独立参数 $T_c$ 判定）：**

- **首次用独立参数（非反解）做真正的预测检验**：arXiv API 命中三篇第一性 Eliashberg 论文，数据落地 `07_数据与现象/数据/独立参数集_第一性Eliashberg.csv`；
- **单带系统通过**：Mo₂NF₂ 两相反代 $T_c$ 与文献吻合 3%（strain 4.12 vs 4.0K）/8%（CDW 0.92 vs 1.0K）；
- **多带系统失效**：MgB₂ 单带 12.9 vs 39K（0.33×）——文献明证需双带（$\lambda(k,k')$ 0.1–2.5），与第69轮 Pb 双带结论互证；
- 意义：CQM 完整候选式对单带声子超导绝对 $T_c$ 定量有效（3–8%），多带需 12.A 定量推广（`临-5`/`临-6` 未闭合）；依赖 FE01 公设＋Allen-Dynes，非纯链内；$\mu^\ast$、$\omega_{\log}$ 假设已标；
- 新交付：`08_框架扩展候选/FE05_端到端独立参数Tc判定.md`、`07_数据/独立参数集_第一性Eliashberg.csv`、`04_计算验证/端到端_独立参数Tc判定.py`／`.png`／`.csv`、`06_决策记录/2026-11-23_FE05端到端判定.md`、`成果登记.md`（FE05）；不改主链/编号/账面。

**第 71 轮补（FE06 多带 $T_c$ ↔ CQM 12.A 对接）：**

- **调研命中 SMW 两带框架**（Suhl-Matthias-Walker PRL 3, 552 (1959)，正是 Ruby Pb 双带文献 ref 15；Bussmann-Holder arXiv:cond-mat/0211588）；
- **对接 CQM 12.A**：模式 n=2↔带1、n=4↔带2、带间耦合由全局共享 K（25.A）提供、12.A3 权重 $\Phi_4/\Phi_2=2/4=1/2$；给多带 $T_c$ 候选式；
- **解释 FE05 遗留的 MgB₂ 失效**：单带 AD 给 12.9K vs 39K；SMW 本征值结构给 39K 物理区间（$\lambda_{\rm eff}=0.682$，近 Choi 文献平均 $\lambda=0.61$）——失效根源是单带近似，非 CQM 错；带间增强 1.03–1.53×；与第69轮 Pb 双带结论互证；
- Lean `FE06_MultiBandTc.lean`（4 条，退出码 0：$\lambda_{\rm eff}\ge\max$、对称、12.A3 权重、$T_c$ 单调）；数值 `FE06_多带Tc扫描.py`／`.png`／`.csv`（探索性扫描，不调参贴合）；
- **边界**：不闭合 `临-5`/`临-6`（高模式载体与归一未写出，只把"载体未写出"推进到"结构有方程"）；SMW 外部标准＋CQM 12.A 结构读法；候选·未落地·不碰权威源；不动任何编号与状态栏、账面；
- 新交付：`08_框架扩展候选/FE06_多带Tc的SMW方程与12A对接.md`、`05_Lean验证/FE06_MultiBandTc.lean`、`04_计算验证/FE06_多带Tc扫描.py`／`.png`／`.csv`、`06_决策记录/2026-11-23_FE06多带Tc对接.md`、`成果登记.md`（FE06）；不改主链/编号/账面。

**第 72 轮补（FE07 统一验证判定——诚实总账）：**

- **建立四级验证判定**：L1 真正独立预测／L2 半独立／L3 自洽回代／L4 事后解释；把 71 轮所有结果统一分级；
- **决定性判定**：**L1=0**（71 轮来无一次参数完全独立的预测验证）、L2=2（Mo₂NF₂ 3–8%）、L3=1（gap 回代）、L4=3（MgB₂/Pb/同位素解释）——直面"尚未通过独立预测验证"的事实；
- **方法学自检**：抓取 Mo₂NF₂ 全文，反推隐含 $\mu^\ast=0.0964/0.1023$（标准值 0.10）——确证 L2 判定；论文式(3) $\alpha^2F/\omega$ 矩独立确证第62轮"Eliashberg 矩 ≠ CQM $3y^2$ 矩"；
- **达 L1 的精确条件**：需 $(\lambda,\mu^\ast,\omega_{\log})$ 全部独立给定的参数集——下一步检索目标（MgB₂ 全文若有 $\omega_{\log}$ 表即可凑 L1）；
- 新交付：`08_框架扩展候选/FE07_统一验证判定与诚实总账.md`、`04_计算验证/FE07_统一验证判定.py`／图／csv、`FE07_文献方法自检.py`／图／csv、`06_决策记录/2026-11-23_FE07统一验证判定.md`、`成果登记.md`（FE07）；候选·未落地·不碰权威源；不改主链/编号/账面。

**第 73 轮补（FE08 首个 L1 独立预测验证）：**

- **抓取 MgB₂ 全文**（arXiv:cond-mat/0111182 ar5iv）补齐 FE07 缺失的独立参数：$\lambda=0.61,\mu^\ast=0.12,\omega_{\ln}=63.5$meV=737K——**全部独立、非反解**；
- **首个 L1 验证**：CQM 各向同性候选式给 $T_c=14.2$K，与论文各向同性 Eliashberg 19K 偏差 −25.2%（AD 近似对完整 Eliashberg 的已知系统误差，论文 McMillan 低估 30%），量级/方向通过；非谐方向正确（谐振 22.6K→非谐 14.2K，论文 28→19K）；
- **精确限定**：不声称预测实验 39K——各向异性增强 2.05× 属 FE06 的 SMW↔12.A 推广（`临-5`/`临-6` 未闭合）；
- **FE07 总账更新**：L1 从 0→1；数据文件 $\omega_{\ln}$ 从假设 670K 修正为独立 737K；
- 新交付：`08_框架扩展候选/FE08_MgB2首个L1验证.md`、`04_计算验证/FE08_MgB2首个L1验证.py`／图／csv、数据文件更新、`06_决策记录/2026-11-23_FE08首个L1验证.md`、`成果登记.md`（FE08）；候选·未落地·不碰权威源；不改主链/编号/账面。

**第 74 轮补（`临-6` 磁通归一消歧 + charge-4e/6e 实验支撑）：**

- 74 轮来首次真正深入核心缺口 `临-6`：精确化矛盾（同一符号 $\Phi_n$ 两种读法反向——$h/(ne)$ 给 $2/n$ 递减、$nh/2e$ 给 $n/2$ 递增）；
- **语义消歧判定**：两个比值是两个不同对象（单量子单位 vs 总通量），互为倒数、符号重载非物理矛盾；权威 06 第482行定义 $\Phi_n=h/(ne)$、实验测 $h/ne$、12.A3 权重递减三者一致判单量子读法为物理；
- **关键实验**：Ge et al. PRX 14, 021025 (2024) 在 CsV₃Sb₅ 环观测 $h/4e$、$h/6e$ 磁通量子化（charge-4e/6e）——CQM 12.A 高模式 $n=4,6$ 的**直接实验实现**（此前仅 Pb 双带间接佐证）；
- **诚实边界**：只消歧"换算未定"子项，**不闭合 `临-6`**（物理同一需 M1/G22），状态栏不动；Lean `Lin6FluxQuantum.lean`（5 条，退出码 0）；数值 `临6_磁通归一消歧与4e实验.py`／图／csv；
- 新交付：`03_推导工作台/临6_磁通归一消歧与4e6e实验支撑.md`、`05_Lean验证/Lin6FluxQuantum.lean`、`04_计算验证/临6_磁通归一消歧与4e实验.py`／图／csv、`06_决策记录/2026-11-23_临6磁通消歧与4e实验.md`、`成果登记.md`（R-83）；不改主链/编号/账面。

**第 75 轮补（`临-5` 权重归一 + 有限截断）：**

- 75 轮来首次深入 `临-5`（$n\ge4$ 载体与权重归一）：识别 12.A3 相对权重 $1/k$ 的**调和发散根因**（$H_\infty=\infty$，无限档无法归一）；
- **有限截断方案** $w_k=(1/k)/H_K$（$\sum w_k=1$）对接参与比 $n_{\rm eff}$（临-21）；K=3(n=2,4,6) 给 $w=[0.545,0.273,0.182]$——2e 主导、4e/6e 递减，与 Ge PRX2024 charge-2e/4e/6e 实验权重序定性一致；
- **诚实边界**：只解决权重归一次项，未写 $n\ge4$ 态—算子映射、K 材料值外生（临-21），**不闭合 `临-5`**，状态栏不动；Lean `Lin5WeightNorm.lean`（5 条，退出码 0）；数值 `临5_权重归一与发散.py`／图／csv；
- 新交付：`03_推导工作台/临5_高模式权重归一与有限截断.md`、`05_Lean验证/Lin5WeightNorm.lean`、`04_计算验证/临5_权重归一与发散.py`／图／csv、`06_决策记录/2026-11-23_临5权重归一与有限截断.md`、`成果登记.md`（R-84）；不改主链/编号/账面。

**第 76 轮补（环 5／`审-1`：比值传递的望远镜恒等式与 $r_{ij}$ 的两层归属）：**

- **追查 `M5` 挂账的直接后果**：`M5` 写"BCC 逐边亏角未给故 $\dim\ker D$ 不可算"。追溯该数据来源时发现，环 5 同时写了三件不能共存的事——(P) $v_\tau$ 逐点单值且 $\mathcal H_{ij}=\tau_i-\tau_j$ 上闭链；(Q) $v_{\tau,j}=v_{\tau,i}r_{ij}$ 为**等式**；(R) BCC 三环 $\prod_Cr=0.177/0.707/0.500\ne1$；
- **望远镜恒等式（严格）**：若 $v_{\tau,i}$ 逐点定义，则 $r_{ij}=v_{\tau,j}/v_{\tau,i}$ 沿任意闭环的乘积**恒为 1**（只用求和望远镜与 $\exp(0)=1$，无附加假设）。故 P＋Q ⇒ ¬R；三者两两相容、三者不相容；
- **取舍**：放弃 **Q 的等式地位**。$r_{ij}$ 归**和乐侧**（有向边量、$U(1)$ 和乐的 $\mathbb R_+$ 对应物，$\prod\ne1$ 是曲率不是数值错误）；$v_{\tau,i}$ 归**固有时侧**（节点标量、单值）；二者只在 $O(\ell)$ 阶近似对应，非线性项即和乐；
- **最大收益**：$\mathcal H$ 的上闭链与 $|V_t|-1$ 独立自由度**原样保住**——不必为解释 (5.3) 的数值去承认"$v_\tau$ 多值"；`环06_相位连接审计` 判出的"两套 $\mathcal H$"由此获得理由（不是两套并列，而是 $r$ 本就不该进 $\mathcal H$）；
- **两处连带回改**：① `环07` 的"矩阵分支几何强制"**结论保留、理由改写**（$r$ 本来就是边量，不再需要 BCC 反例作前件）；② `C1=1` 的"自动性"**失效**——BCC 亏角量级下反对称残差 $\frac12\ln(1-x^2)$ 的相对破坏达 **18.8%–54.8%**，`C1=1` 回到实质约束；
- **`M5` 待办性质改变**：不是"缺一个数"，而是 3 个环乘积要定 9 个逐边 $\ell$，**欠定 6 维**（等边反解给 $\ell=4.302/1.297/2.325$ rad）；
- Lean `LoopHolonomySplit.lean`（7 条：望远镜、指数形式、双向平凡解、单边乘积 $<1$、反向亏角非线性、残差非正、残差零点唯一；**无警告、退出码 0**）；数值 `环05_比值传递望远镜.py`／图／csv（四面板，无拟合，结构断言全过）；
- **诚实边界**：不闭合 `审-1`／`M5`；不改 A12／DM.2／DM.3；06 原文、08 台账、账面（59 行／35 唯一／32 推进／3 余）均未动；主链仅在环 5 缺口行加注记；
- 新交付：`03_推导工作台/环05_审1_比值传递与和乐边量的分层.md`、`05_Lean验证/LoopHolonomySplit.lean`、`04_计算验证/环05_比值传递望远镜.py`／`.png`／`.csv`、`06_决策记录/2026-11-23_环05比值传递分层.md`、`成果登记.md`（R-85）；不改主链正文/编号/状态栏/账面。


**第 77 轮补（环 3／环 5：BCC 平直三角化的亏角恒为零——06 三环乘积的几何可实现性判定）：**

- **从上一轮的待办出发**：`M5` 剩"3 个环乘积定 9 个逐边亏角、欠定 6 维"。补这 6 维前必须先定 $\ell_{ij}$ 的口径；一定就发现口径本身是空的；
- **几何事实（可复算、精确值）**：BCC 的 Delaunay 三角化由点集唯一确定，四面体为菱形（4 条 $\sqrt3a/2$ + 2 条 $a$，体积 $1/12$，与 arXiv:1501.07505 §1.3 一致）。二面角是**精确** $\pi/2$（短边）与 $2\pi/3$（长边），绕边四面体数分别为 **4** 与 **3**，两者都闭合到 $2\pi$（$4\cdot\frac\pi2=3\cdot\frac{2\pi}3=2\pi$，$k=2\pi/\theta$ 恰为整数）；
- **定理**：由环 3 (3.1)，每条内部边 $\varepsilon_e=0$；由 (5.2)，$r_e=1$；故任意内部三角环 $\prod_Cr=1$；
- **判定**：06 的 $0.177/0.707/0.500$ 需常曲率 $\varepsilon_0=4.3024/1.2967/2.3250$ rad。三条来源全排除——(a) 正则三角化给 $\prod\equiv1$；(b) $\varepsilon_0=4.302$ 要求绕边角总和仅 $113.5^\circ$，与 BCC 的 $120^\circ\times3=360^\circ$ 冲突，**几何不可能**；(c) 环 4 涨落需 $3.45$ rad/边（$197.5^\circ$），远超涨落量级；
- **自我更正（本轮主要产出）**：上一轮"保留 R、放弃 Q"的理由**失效**——R 被查为几何不可实现，标为**待查**；但 P／Q／R 不相容（望远镜恒等式）**不变**，是纯逻辑；"$r$ 与 $v_\tau$ 分层"**精确化**为"两者差 $O(\ell^2)$，这个差就是和乐"，$\ell\to0$ 时 $\prod r\to1$ 与 $v_\tau$ 单值相容，**CQM 自洽**；06 的 0.177 要求 $O(\ell^2)$ 项达 82%，即 $\ell\sim4.3$ rad，不是小和乐；
- **新登记 `审-18`**：$r_{ij}$ 的几何赋值口径未定（哪个三角化／哪种曲率／是否为归一化后的其它量），挂在 `审-1` 的 R 分支下；`08` 缺口台账未改（入台账待授权）；
- Lean `FlatTriangulationDeficit.lean`（7 条：两条平直算术、亏角零 ⟺ 比值一、全零环乘积、比值严格反单调、反解式、反解正性；**无警告、退出码 0**）；数值 `环03_平直三角化亏角.py`／图／csv（26 行，含"$k$ 必须为整数"的结构断言）；
- **诚实边界**：不改 06 三个数（数值不改）；不闭合 `审-1`／`M5`；不改状态栏、账面、06 原文、08 台账；
- 新交付：`03_推导工作台/环03_平直三角化与三环乘积判定.md`、`05_Lean验证/FlatTriangulationDeficit.lean`、`04_计算验证/环03_平直三角化亏角.py`／`.png`／`.csv`、`06_决策记录/2026-11-23_环03平直三角化判定.md`、`成果登记.md`（R-86）。

**第 78 轮补（环 8／`M5`：$f$ 的斜率由 DM.4 的 $\kappa_f$ 定出——"用 `C1=1` 定 $f$"是问错了问题）：**

- **问题重定位**：`M5` 十几轮来把 `C1=1`（$\sum_jf(\lambda_{ij})=0$）当方程去解 $f$（$D\mathbf f=0$）。这是本末倒置——`C1=1` 是**约束**，且 `环07` 已证中心对称壳层下任意奇 $f$ 自动满足它，**约束力为零**；
- **正解**：06 DM.4 是**一阶等式**而非仅方差——$\delta C_{ij}=\kappa_f(\Delta\varepsilon_i-\Delta\varepsilon_j)+O(\Delta^2)$。与 (5.2) 的 $\lambda=\frac12\ln(1-\ell/2\pi)$ 联立（$\partial\lambda/\partial\ell=-1/4\pi$），逐项对照得
  $$f'(0)=-4\pi\kappa_f=-\frac{1}{v_\tau^2}\xrightarrow{\varepsilon\to0}-1,$$
  用到 `审-2` 的恒等式 $4\pi v_\tau^2\kappa_f\equiv1$；
- **两项稳健性**：① **与索引层无关**——节点差读法与键量读法给同一斜率（两边同时换定义，比例不变），故不必等 `审-18`／`审-19`；② **高阶可截断**——$f=-u+du^3$ 的相对偏差 $=\lvert d/c\rvert u^2$，取 $\sigma_\ell\le0.1$、$\lvert d/c\rvert\le10$ 时 $\le3.2\times10^{-4}$，在 CQM 当前精度（$T_c$ 3–8%、gap ratio 2.7%）下不可见；
- **`M5` 的缺口重写**：从"$f$ 完全未定、阻塞环 9"改为"**斜率固定、只剩高阶 $d$、不阻塞任何下游环节**"；编号与未闭合状态保留；
- **新登记 `审-19`**：DM.4／DM.5 的自变量层未定（节点差 vs 键量），挂在 `审-1` 的 R 分支下，与 `审-18` 并行；它决定 $\prod_Cr$ 是否为 1，但**不影响斜率**；`08` 台账未改；
- Lean `FLopeSlope.lean`（4 条：一阶对照、$\kappa_f$ 恒等式、平直斜率 $-1$、三次项界；**无警告、退出码 0**）；数值 `环08_f斜率定标.py`／图／csv（37 行，含 (8A.1) 恒等式与 $\partial\lambda/\partial\ell$ 的数值断言）；
- **诚实边界**：不闭合 `M5`（$d$ 与精确形式未给）；不改 DM.4／DM.5 原文；不改状态栏、账面、08 台账；
- 新交付：`03_推导工作台/环08_M5斜率由DM4定标.md`、`05_Lean验证/FLopeSlope.lean`、`04_计算验证/环08_f斜率定标.py`／`.png`／`.csv`、`06_决策记录/2026-11-23_环08f斜率定标.md`、`成果登记.md`（R-87）。

**第 79 轮补（环 8／环 9／`审-19`：DM.4 的两分量分解——键伸缩与键角弯曲，环流比 $\sim5\%$）：**

- **两难**：纯节点差读法给 $\prod_Cr\equiv1$（望远镜）且逐样本 `C1=1` 下由 `gradient_row_zero_forces_zero` 直接杀死 $B$；纯键量读法使 $\langle(\delta C_{ij})^2\rangle$ 与边无关，$J=J_0\cos\mathcal H$ **无 $(1-\rho)$ 调制**，摧毁 `M6` 形状／环 10 温度桥／环 15 概率尾。两者都不能单独用；
- **解**：经典价力场（Keating 1966）把立方晶格弹性能严格分成**键伸缩**（$\alpha$，键特定）与**键角弯曲**（$\beta$，节点局部）。搬到 CQM：
  $$\delta\ell_{ij}=\beta_u(\delta\varepsilon_i-\delta\varepsilon_j)+\alpha_u\,\delta b_{ij},$$
  这是最一般形式——Regge 亏角由四面体六条边长定，边长变化只有"整体缩放 + 畸变"两类；
- **环流比** $r_{\rm circ}=\alpha_u\sigma_b/(\beta_u\sigma_\varepsilon\sqrt{2(1-\rho)})$；谐振子零点标度给 $r_{\rm circ}\sim(\beta/\alpha)^{3/2}$；Keating 反解 $\alpha=a(3c_{12}+c_{11})/4$、$\beta=a(c_{11}-c_{12})/4$；
- **量级（5 元素标准弹性常数）**：$r_{\rm circ}=0.008$–$0.080$，$\prod_Cr=0.89$–$0.99$（偏离 1 的 $1\%$–$11\%$）；**06 的 0.177 需 $r_{\rm circ}=2.17$，差 27–263 倍**；
- **硬上界（不依赖标度系数）**：$c_{12}>0$ ⇒ $\beta/\alpha=(c_{11}-c_{12})/(c_{11}+3c_{12})<1$ ⇒ $r_{\rm circ}<1$ ⇒ $\prod_Cr>1/(2\sqrt2)=0.354$。**故 0.177 在任何 $c_{12}>0$ 的立方晶体中不可达**；
- **三项后果**：① 第 77 轮"几何不可能"获定量加强；② **矩阵分支的真实地位是微扰**（$r_{\rm circ}\sim5\%$），修正 `环08` 的表述；③ **`M6` 形状需 $r_{\rm circ}\ll1$** 才成立（$J/J_0|_{\rho=0}=\frac{(1-\rho)+r^2}{1+r^2}$），首次给出定量条件；
- **`审-19` 的工作台解答**：DM.4／DM.5 的右边为两分量；06 原文的节点差是 $\alpha_u\to0$ 端点，三环乘积是 $\alpha_u$ 主导端点，**两者是同一式的两个极限**；**新登记 `审-20`**（零点标度系数）；
- Lean `TwoComponentDeficit.lean`（6 条：两分量方差可加、环流比零点判据、正性、Keating 两式、`prod_ge_fifth`＝$r\le1\Rightarrow\prod_Cr\ge1/5>0.177$；**无警告、退出码 0**）；数值 `环08_两分量与环流比.py`／图／csv（9 行，含反解与 Keating 回代断言）；
- **诚实边界**：$r_{\rm circ}$ 是量级估计（幂次对、系数未定，`审-20`）；不改 DM.4／DM.5／DM.9 原文；不改状态栏、账面、08 台账；
- 新交付：`03_推导工作台/环08_两分量分解与环流比.md`、`05_Lean验证/TwoComponentDeficit.lean`、`04_计算验证/环08_两分量与环流比.py`／`.png`／`.csv`、`06_决策记录/2026-11-23_环08两分量分解.md`、`成果登记.md`（R-88）。

**第 80 轮补（环 8／环 9：零点标度幂次更正为 $1/4$——第 79 轮三项结论撤回）：**

- **自查发现错误**：第 79 轮 (8B.7) 写 $\sigma^2\propto1/k$。谐振子精确式为 $\langle x^2\rangle=\hbar/(2m\omega)$、$\omega=\sqrt{k/m}$，故 $\langle x^2\rangle=\hbar/(2\sqrt{km})$，即 $\sigma^2\propto k^{-1/2}$、$\sigma\propto k^{-1/4}$。**刚度加倍只让振幅降到 $1/\sqrt2=0.707$，不是 $1/2$**；
- **更正**：$r_{\rm circ}\sim(\beta/\alpha)^{1/4}$（原 $3/2$）。五元素重算：$r_{\rm circ}=0.4495$–$0.6570$（原 $0.008$–$0.080$，**低估 9 倍**），$\prod_Cr=0.4688$–$0.5730$（原 $0.89$–$0.99$），偏离 1 的 $42.7\%$–$53.1\%$（原 $1\%$–$11\%$）；
- **撤回第 79 轮五项**：(R79-1)(R79-2) 数值全错；(R79-3) **"矩阵分支是微扰"错**——更正后 $r_{\rm circ}\sim0.6$，键分量与节点分量**同量级**；(R79-4) **"0.177 差 27–263 倍"错**——实差 $2.7$–$3.3$ 倍；(R79-5) **"硬上界"只当 $\alpha_u\le\beta_u$ 成立**——该比值自由；
- **保留**（与幂次无关）：两难结构（纯节点差给 $\prod\equiv1$、纯键量摧毁 $(1-\rho)$ 形状）、两分量分解、Keating 反解、$c_{12}>0\Rightarrow\beta/\alpha<1$、`M6` 形状需 $r_{\rm circ}\ll1$ 的判据形式；
- **对 06 三值的重新判定**：第 77 轮两条证据（平直三角化、常曲率）**保留**，第 79 轮那条**撤回**。0.177 只需 $\alpha_u/\beta_u=3.37$（Nb）至 $4.83$（Pb）；而 $0.707$ 与 $0.500$ **恰好落在当前带宽附近**——三值可能是三组不同的 $\alpha_u/\beta_u$ 赋值，这给了 06 一个自洽解释，代价是它隐含了链内未写的耦合比；
- **`审-20` 范围扩大**：从"零点标度的系数未定"扩为"**形式（幂次与系数）未定**"——本轮定出幂次 $1/4$（单刚度谐振子），但真实晶格是耦合模式；
- Lean `ZeroPointScaling.lean`（4 条：$m\sqrt{k/m}=\sqrt{km}$、$\langle x^2\rangle$ 形式、$a^{1/4}<1$、$a<a^{1/4}$——最后一条正是"用错幂次会低估"的代数根据；**无警告、退出码 0**）；数值 `环08_幂次更正与耦合比.py`／图／csv（6 行，含三条结构断言）；
- **同步更正主链**：§16 第 34 项里第 79 轮注记的"矩阵分支是微扰"与"0.177 不可达"两句已改写为更正后的表述（这是本轮唯一动主链正文之处，且是改正错误）；
- 新交付：`03_推导工作台/环08_幂次更正与耦合比.md`、`05_Lean验证/ZeroPointScaling.lean`、`04_计算验证/环08_幂次更正与耦合比.py`／`.png`／`.csv`、`06_决策记录/2026-11-23_环08幂次更正.md`、`成果登记.md`（R-89）。

**第 81 轮（环 8／`M5`×`审-19`／`审-20`：Keating 映射是金刚石的，BCC 需另立——第 79／80 轮数值表作废）：**

- **自查发现映射错误**：第 79／80 轮的 (8B.3)／(8B.9) 是**金刚石／闪锌矿（4 配位）Keating 式**，键角平衡条件 $\cos\theta=-1/3$；BCC 是 8 配位，近邻夹角只有 $70.53^\circ$、$109.47^\circ$、$180^\circ$，每原子 28 对中 12 对为 $70.53^\circ$、平方残差 $4/9$ ⇒ **BCC 不在其极小流形上**，是晶格映射错误而非拟合误差。Si 自校验 $c_{44}^{\rm pred}=79.2$ vs $79.6$ GPa（$-0.5\%$）证明式子本身正确；
- **另立 BCC 两参数 VFF**（精确枚举）：$c_{11}=(16\alpha/9+128\beta/3)/a^3$、$c_{12}=(16\alpha/9-64\beta/3)/a^3$、$c_{44}=16(\alpha+4\beta)/(9a^3)$，故恒等式 $9c_{44}=4c_{11}+5c_{12}$；$\beta/\alpha=(c_{11}-c_{12})/(12(c_{11}+2c_{12}))$，比金刚石式小至少 $9$ 倍；
- **五金属证伪**：恒等式对 Nb／V／Ta／Mo／W 预测偏大 $6.40/3.93/2.32/2.72/2.16$ 倍，且模型 $c_{12}-c_{44}<0$ 而实验为强正 Cauchy 压（$+105.3/+76.4/+69.6/+57.0/+43.0$ GPa）⇒ **两参数 VFF 不是 BCC 金属有效弹性模型，$\beta_u$ 只能唯象**；
- **撤回**第 79／80 轮的 $\beta/\alpha$ 表与 $r_{\rm circ}=0.4495$–$0.6570$、$\prod_Cr=0.4688$–$0.5730$；**保留** $1/4$ 幂次；三口径并集 $r_{\rm circ}\in[0.35,0.88]$、$\prod_Cr\in[0.39,0.64]$ ⇒ "$r_{\rm circ}$ 是 $O(1)$、$\prod_Cr$ 明显偏离 1"稳健、具体数值不稳健；
- **06 三值**：$0.177$ 需 $g\gtrsim5.2$–$6.2$（BCC 口径）或 $g\sim0.7$–$2$（金刚石口径下 $0.500$ 恰 $g\approx1$）；$0.707$／$0.500$ 对应自然耦合比；**归属依赖口径，本轮不判定**，06 三个数不改；
- **$f'(0)$ 对账**：两分量下 $f'(0)=-4\pi\kappa_f/\beta_u$，$\beta_u=1$ 归一后恢复 $-1/v_\tau^2$；第 78 轮"与读法无关"改为"**与归一约定无关**"；
- Lean `BCCVFFElastic.lean`（9 条：BCC 恒等式、两反解比、金刚石 $\ge9\times$ BCC、$1/4$ 幂单调与界、节点差强迫 $\alpha_u=0$、两种斜率归一；**无警告、退出码 0**）；数值 `环08_Keating映射错配与BCC_VFF.py`／图／csv（24 行，含解析↔有限应变、Si 复现、恒等式、$\ge9$ 倍四条断言）；
- **同步更正主链** §16 第 34 项注记（第 81 轮）与 `00_当前有效口径表.md` 边界注记两条（标注第 79／80 轮数值作废）；
- 新交付：`03_推导工作台/环08_Keating映射错配与BCC_VFF.md`、`05_Lean验证/BCCVFFElastic.lean`、`04_计算验证/环08_Keating映射错配与BCC_VFF.py`／`.png`／`.csv`、`06_决策记录/2026-11-23_环08Keating映射错配.md`、`成果登记.md`（R-90）。

**第 82 轮（环 8／`审-18`：06 三环乘积 0.177/0.707/0.500 是有限样品的凸包边界读数——"矩阵分支由几何强制"依据失效）：**

- **复现优先**：直接运行 06 的原始脚本 `06 超导/cqm_analysis/ring_1d_flow.py`，三值精确重现（$0.1769/0.7070/0.5002$），排除"笔误／编造"；
- **判据换位**：共享四面体数 $k$ 不能判体内／边界（实测 $k=1$–$7$，$k=4$ 的边既有体内也有边界），改用**边的几何位置**（中点是否落在凸包面上）；
- **分层结果**：$n=1$（54 点）体内边 169 条、$\varepsilon\in[-3.6\times10^{-13},3.1\times10^{-13}]$（数值零，且 jitter $10^{-6}$–$10^{-3}$ 下不变），边界边 125 条、$\varepsilon$ 为 $O(1)$；$n$ 扫描边界占比 $42.5\%\to23.1\%\to16.6\%$、体内残差始终数值零（有限尺寸指纹）；
- **精确代数**：规则菱形四面体二面角 $90^\circ$ ⇒ $\varepsilon_k=(4-k)\pi/2$ ⇒ $r\in\{1,\sqrt3/2,1/\sqrt2,1/2\}$；$(棱)(角)(角)=1/(4\sqrt2)=0.176777$、$(棱)=0.70711$、$(角)=0.50000$，与 06 三值逐位一致；
- **环 8 后果**：三值属 §0.2 **读数层**，不是结构层输入 ⇒ 第 81 轮"矩阵分支由 06 三环 $\ne1$ **几何强制**"依据失效、矩阵分支退回候选；静态平直体内 $\ell=0\Rightarrow C_{ij}=\delta_{ij}$，不产生差异编码，差异只能来自环 4 零点涨落（`审-3`），环形流若存在须由**涨落环量**承担（未推）；
- **不变**：第 76 轮 $P$／$Q$／$R$ 望远镜恒等式逻辑不变（只是"保留 $R$"的理由改为"$R$ 是边界读数"）；第 77 轮体内 $\prod r=1$ 被数值复核确认；06 三值不改（仅加层级限定）；所有缺口编号与状态栏不变；
- Lean `BoundaryLayerDeficit.lean`（12 条：$\varepsilon=(4-k)\pi/2$、四个特殊 $r$、三环平方 $1/32$、非平直压低、全平直闭环 $=1$；**无警告、退出码 0**）；数值 `环08_三环乘积口径复现.py`／`.png`／`.csv`／`_摘要.txt`（内置三条结构断言）；
- 新交付：`03_推导工作台/环08_三环乘积边界分层口径.md`、`06_决策记录/2026-11-23_环08三环乘积边界分层.md`；同步主链环 8 缺口行、§16 第 13／33／34 项注记与 `00_当前有效口径表.md` 边界注记。

**第 83 轮（环 4→5→8／`审-18` 后续：零点涨落的闭环环量——矩阵分支是零均值涨落支撑，只在 RMS 意义）：**

- **结构事实（Hodge）**：边 1-形式分解 $\Delta\varepsilon=\mathrm da+\delta b+h$；可收缩闭环上梯度分量逐样本望远镜抵消（$\sum_C\mathrm da=0$），故 $\Phi_C=\sum_C\Delta\varepsilon_e$ 只由余确切分量（单连通片）与调和分量（$b_1=2g+b$，`审-13`）承担。这是第 76 轮望远镜恒等式的边场语言版；第 82 轮的"静态 $\prod r=1$"是 $\Delta\varepsilon\equiv0$ 的特例；
- **零均值与方差**：$\mathbb E[\Phi_C]=0$、$\mathrm{Var}(\Phi_C)=\sigma^2[n+2\sum_{i<j}\rho_{ij}]$，$\rho$ 即 (9.1) 的关联（由 $\delta C=\kappa_f\Delta\varepsilon$ 反解，无新参数）；界（非负关联）$n\sigma^2\le\mathrm{Var}\le n^2\sigma^2$，两端逐位取到（$\rho=0$／$1$）；
- **对数周长律**：$\sum_C\lambda=-\Phi_C/4\pi-\sum_C\Delta\varepsilon^2/16\pi^2+O(\sigma^3)$，一阶均值为零、**二阶恒负不抵消** ⇒ $\langle\ln\prod_Cr\rangle=-n\sigma^2/(16\pi^2)+O(\sigma^4)$；速率只由单边边际方差定、**与关联无关、无自由参数**（数值反演配对无偏估计，最大相对差 $0.92\%$）；
- **平均符号翻转**：$\langle\prod_Cr\rangle=\exp\{\sigma^2[2\sum\rho-n]/32\pi^2\}+O(\sigma^4)$；$\xi_c/a$ 从 $0.5$ 到 $10^4$ 给 $0.9988\to1.3501$，在 $\xi_c/a\approx0.7$ 穿过 $1$——短程关联压低、强正关联抬高，**可测**；
- **相干相位**：$|\langle e^{\mathrm is\Phi_C}\rangle|=e^{-s^2\mathrm{Var}/2}$，$n_*\simeq2/(s^2\sigma^2)$（$\sigma=0.05$、$s=1$ 给 $800$ 边）；长环退相干；
- **环 8 后果**：矩阵分支的**一阶环流**身份改判为**零均值、只在 RMS 意义**存在的涨落支撑（幅度 $\sigma\sqrt{n+2\sum\rho}$；完整 $\sum_C\lambda$ 另有确定二阶负偏移 $-n\sigma^2/16\pi^2$），既非静态几何常数、也非候选逃生路线；同一个 $\rho$ 同时控制 (9.1) 键对差方差与环量方差，给出内部一致性检验；
- **自查（一阶失效）**：只用一阶 $e^{\mathrm{Var}/32\pi^2}\ge1$ 会得"平均永远抬高"的错误结论；二阶项把它压回 $<1$。$n=128$、$\sigma=0.05$：一阶 $1.02045$、二阶 $1.01839$、精确 MC $1.01753$；
- Lean `LoopFluctuationCirculation.lean`（15 条：望远镜抵消、余确切、$V$ 递推／两端／单调／上下界、反演配对恒等式与非正、$e^{\pm}$ 平均 $\ge1$、相位 $\le1$；**无 `axiom`／`sorry`／`admit`／`native_decide`／`unsafe`，`lake env lean` 退出码 0、无输出**）；数值 `环08_涨落环量与闭环乘积.py`／`.png`／`.csv`／`_摘要.txt`（六面板、八项断言）；
- 外部工具（只作对照、不写成 CQM 结论）：Hodge Laplacians on Graphs（arXiv:1507.05379）、Wilson 环周长／面积律（arXiv:1007.4145 Eq.(17)、arXiv:2409.20085、arXiv:2101.05289）、等正关联对数正态矩（Carleton 技术报告式(21)、arXiv:1203.03288）、2D Mermin–Wagner（arXiv:0912.1490、arXiv:1510.05804、PNAS 10.1073/pnas.1612964114）、Regge 亏角（arXiv:1601.04821、arXiv:1208.1514）；
- 新交付：`03_推导工作台/环08_涨落环量与闭环乘积.md`、`06_决策记录/2026-11-23_环08涨落环量与闭环乘积.md`；同步主链环 8 缺口行、§16 第 13／33／34 项注记与 `00_当前有效口径表.md` 边界注记；不改编号／状态栏／账面／08 台账。

**第 84 轮（环 4：零点涨落关联定形为 Bessel 核——纯周长律，撤销第 83 轮的 $n\ln n$）：**

- **谱权重**：$\varepsilon$ 是铰链亏角（06 环节表②／符号表：曲率载体、与顶点角亏无关），对位移至少求一阶导，故 $|G_q|^2\propto q^{2n}$、$n\ge1$（$m=2n\ge2$）。$m=0$（位移载体）不是链内的 $\varepsilon$；
- **关联形状**：$\rho_m(r)=\int_0^Qq^mJ_0(qr)\,dq/(Q^{m+1}/(m+1))$；$\rho_m(0)=1$，大 $Qr$ 包络 $(m+1)J_1(Qr)/(Qr)$，格点 $k^{-3/2}$；
- **纯周长律**：$\sum_k\rho_k=S_\rho$ 收敛（$m=2/3/4$ 给 $-0.02255/-0.07561/-0.10214$），$\mathrm{Var}(\Phi_C)=n\sigma^2(1+S_\rho)+O(1)$；$n=512$ 时比值 $0.955/0.849/0.796$。**无 $\ln n$**；
- **撤销两处**：第 83 轮的 $n\ln n$ 括区（对应 $m=0$，非铰链亏角）与"强正关联把平均乘积抬过 $1$"（链内 $S_\rho<0$，平均恒 $<1$）；
- **$\sigma_0$ 标度**：$\sigma_0^2\propto Q^{m+1}=Q^{2n+1}$（应变／声学 $Q^3$，曲率／柔性 $Q^4$，曲率／声学 $Q^5$）；从"完全外生"降为"标度已定、只差 O(1) 角向因子与材料常数"。量级估计（$\rho_m=10^{-6}\,{\rm kg/m^2}$、$c=3\times10^3\,{\rm m/s}$、$a=3\times10^{-10}\,{\rm m}$）给 $\sigma_0\approx0.033\,{\rm rad}$、$n_*\approx1.9\times10^3$（仅量级）；
- **$n_*$ 领头不变**：$n_*\simeq2/(s^2\sigma_0^2)$，关联只给 $1+S_\rho$ 的常数修正；
- **已由第 85 轮解除**：$m$ 的分叉不是两个并列几何选择，而是 $m_{\rm eff}=2n+1-s$ 中 $n$ 与 $s$ 两件事；06 的 3D Regge 体给 $(n,s)=(1,1)$ ⇒ $m_{\rm eff}=2$、$\sigma_0^2\propto Q^3$（见下条）；
- Lean `DebyeMomentNormalization.lean`（6 条：谱矩归一化、标度律、周长律恒等式、正/负重整化；**无 `axiom`／`sorry`／`admit`／`native_decide`／`unsafe`，退出码 0、无输出**）；数值 `环04_零点涨落关联形状.py`／`.png`／`.csv`／`_摘要.txt`（六面板、七断言）；
- 外部工具（只作对照）：铰链亏角定义（IMA J. Numer. Anal. 2024、arXiv:1411.5672）、柔性色散（arXiv:2603.16717、arXiv:1304.6567、arXiv:1008.2523）、2D Mermin–Wagner（arXiv:0912.1490、arXiv:1510.05804、PNAS 10.1073/pnas.1612964114）、Bessel 渐近（Abramowitz–Stegun §9.2）；
- 新交付：`03_推导工作台/环04_零点涨落谱与关联形状.md`、`06_决策记录/2026-11-23_环04零点涨落谱与关联形状.md`；同步主链环 4 缺口行、§16 第 12 项、环 8 缺口行与 `00_当前有效口径表.md`；第 83 轮卡加修订注记；不改编号／状态栏／账面／08 台账。

**第 85 轮（环 4：亏角涨落的 $q$ 幂——参考亏角二分与谱指数合成律，$m$ 的分叉解除）：**

- **响应二分**：$\Delta\varepsilon_e=\sum_{e'}A_{ee'}\delta l_{e'}$，$A$ 不含导数。参考亏角为零 ⇒ 顶点全在 $\mathbb R^3$、四面体平铺其凸包 ⇒ $\varepsilon\equiv0$（Kuhn 补片 $M=6$、1296 四面体、闭合边 1206；数值 $2.7\times10^{-15}$，均匀应变 $\epsilon=10^{-3}\sim8\times10^{-3}$ 与平面波 $A=0.02\sim0.32$ 均不随幅度变）。故**平坦参考不能承载 $\varepsilon$**；
- **链必在弯曲参考**：06 的 $\varepsilon\in[0,2\pi)$ 与 FG 接口 $v_\tau=\sqrt{1-\varepsilon/2\pi}$ 非平凡要求参考亏角非零；此时 $\Delta\varepsilon=O(\text{应变})$（数值斜率 $1.002$）⇒ $|G_q|^2\propto q^2$（$n=1$）；
- **合成律**：$m_{\rm eff}=2n+1-s$（$|G_q|^2\propto q^{2n}$、$\omega_q\propto q^s$、2D 测度 $q$），$\sigma_0^2\propto Q^{m_{\rm eff}+1}$——形状与标度同指数；收敛 $m_{\rm eff}\ge1\iff s\le2n$；
- **分叉解除**：06 的 3D Regge 体（铰链＝边、共维 2、Delaunay **四面体**化）＋体声子 $s=1$ ⇒ $(n,s)=(1,1)$、$m_{\rm eff}=2$、$\sigma_0^2\propto Q^3$、$S_\rho=-0.0226$；主链 §0.2 的"二维平面晶格"承担 $p_c=1/2$ 与 BKT（$L2$），不改 $L1$ 的 $\varepsilon$ 载体；
- **第 84 轮三处订正**：$m=2n$ 补前提 $s=1$；"$m=3$"改为 $(n=2,s=2)$ 的对照；$\rho_0=J_1(Qr)$（非 $1/r$；$\sum_k\rho_0\propto\sqrt N$ 仍发散）；
- **可证伪**：$\mathrm{Var}(\Phi_C)-n\sigma^2=n\sigma^2S_\rho$ 的符号——体支 $m_{\rm eff}=2$ 给 $1+S_\rho=0.977<1$，柔性支 $m_{\rm eff}=1$ 给 $1.137>1$；两支平均闭环乘积都 $<1$（指数 $\propto S_\rho-1$），符号判据只用于方差；
- Lean `SpectralExponentComposition.lean`（1 定义＋13 条；**无 `axiom`／`sorry`／`admit`／`native_decide`／`unsafe`，退出码 0、无输出**）；数值 `环04_亏角q幂与谱指数合成.py`／`.png`／`.csv`／`_摘要.txt`（六面板、七断言）；
- 外部工具（只作对照）：亏角定义（arXiv:0907.4325 §II；arXiv:2303.07367）、亏角一阶变分（arXiv:1110.6866 §3.2）、柔性色散（arXiv:2603.16717、arXiv:1304.6567）、Bessel 渐近（Abramowitz–Stegun §9.2）；
- 新交付：`03_推导工作台/环04_亏角q幂与谱指数合成律.md`、`06_决策记录/2026-11-23_环04亏角q幂与谱指数合成.md`；同步主链环 4／环 8 缺口行、§16 第 12 项、`00_当前有效口径表.md` 与第 84 轮卡更正；不改编号／状态栏／账面／08 台账。

**第 86 轮（环 4：亏角转移函数——零点幅度归属、膨胀不变性、$c_\varepsilon\propto$ 曲率尺度、维数订正）：**

- **零点幅度归属**：$\Delta\varepsilon_q=G_qu_q$，故 $\langle|\Delta\varepsilon_q|^2\rangle=|G_q|^2\langle|u_q|^2\rangle$；$\hbar/(2\rho_m\omega_q)$ 属**位移模**。$(2.1)$ 直接当亏角零点幅度等于隐含 $|G_q|=1$（$n=0$ 位移读法，第 85 轮已撤销），与 $(4.1)$ 差 $Q^2$（数值 $Q$ 斜率 $3$ vs $1$）；
- **膨胀不变性**：各向同性膨胀使四面体等比缩放、二面角不变 ⇒ $\mathrm{tr}_\epsilon C=0$；数值相对残差 $1.9\times10^{-8}$；亏角只响应偏斜形变；
- **$c_\varepsilon$**：纵向 $0.2065$、横向 $0.3130$（$c^2$ 比 $2.30$，偏振权重 $5.59$）；$c_\varepsilon=\kappa\,\mathrm{RMS}(\varepsilon^{(0)})$，$\kappa\approx0.53$，$\eta$ 扫描 log-log 斜率 $1.043$（$\eta\to0$ 时为零，精确）；
- **维数定律**：$m_{\rm eff}^{(d)}=2n+(d-1)-s$，$\sigma_0^2\propto Q^{m_{\rm eff}+1}$。**订正第 85 轮**：其所用 2D 测度与 3D 载体不同维；按载体 $d=3$ 取 $m_{\rm eff}=3$、$\sigma_0^2=c_\varepsilon^2\hbar Q^4/(16\pi^2\rho_m c)$、$S_\rho=1/6$（**精确**，$\mathrm{Var}(\Phi_C)\to\frac76n\sigma^2$）；第 85 轮的 $m_{\rm eff}=2$／$Q^3$／$S_\rho=-0.0226$ 保留为 $d=2$ 对照；
- **否证**：相对亏损律 $\Delta\varepsilon_e\propto\varepsilon_e^{(0)}$（对角基 corr$\approx0$，剪切 $R^2=0.676$）；
- Lean `CurvatureTransferFunction.lean`（2 定义＋17 条；**无 `axiom`／`sorry`／`admit`／`native_decide`／`unsafe`，退出码 0、无输出**）；数值 `环04_亏角转移函数与膨胀不变性.py`／`.png`／`.csv`／`_摘要.txt`（六面板、七断言）；
- 外部工具（只作对照）：亏角定义（arXiv:0907.4325、arXiv:0810.3594）、角变分抵消（arXiv:gr-qc/0408079）、平坦背景（arXiv:1802.09551）、缺陷和乐（arXiv:1704.00998、cond-mat/0601077）、三维角向核 $j_0$（标准数学）；
- 新交付：`03_推导工作台/环04_亏角转移函数与膨胀不变性.md`、`06_决策记录/2026-11-23_环04亏角转移函数与维数订正.md`；同步主链环 4／环 8 缺口行、§16 第 12 项、`00_当前有效口径表.md`；**待定（不编号）**：模求和维数 $d$（2 vs 3）；不改编号／状态栏／账面／08 台账。

**未闭合**：`审-10`、`审-4`、`M8`、`M5`、`M6`、`审-1`、`审-11`、`审-13`、`N-7`、`临-20`、`G19`；`M6` 的**形状**已导（\(J/J_0=(1-\rho)\cos(s\ell)\)）并判定键局域，但绝对能标 \(J_0\) 按 Z2 外生、\(\rho\) 的真实谱形式未定，**不闭合**；`审-1` 已判定局域不可解，矩阵分支的"由 BCC 三环 $\prod r\ne1$ 几何强制"依据已失效（第 82 轮），第 83 轮改判为**零均值涨落支撑、只在 RMS 意义**；中心对称壳层下 `C1=1` 对任意奇 $f$ 自动成立，**仍不闭合**（$f$ 已齐次线性化为 $D\mathbf f=0$，形状至多定到尺度、尺度并入外生 $\kappa_f$；累积层 $f^{-1}$ 仍缺，须靠 `G19`）；`G19` 已拆为量纲／周期／热项三件事并定出 \(\alpha_{\rm lin}=-4\pi s\)，但 \(s\) 与 \(A(\varepsilon)\)、\(N\) 归一未给、06 原文未改，**不闭合**；`审-10` 截断伪问题已消、维度回改已登记、同位素端点已分类，但绝对 \(T_c\) 仍受命题 Z2 外生能标限制，**不闭合**；`审-4` 已给统计映射与阈值并回改，仍不闭合；`临-25` 已登记为不可判定（当前链内），非闭合；环 9 方差口径（M／S 分支）、\(V_{\rm coh}\) 的物理识别、\(\sigma_{\omega,\rm coh/inc}\) 的来源仍开放；矩阵分支 \(C\) 的正规性已由 `A12Normality.lean` 证明（任意奇 \(f\)），原先担心的“非正规 Schur”已删除。`审-3` 的**方向**已闭合；环 15 的概率分布已推进到条件 chi-square 尾；环 19 已把 `M8` 降为“必要＋上界＋相界方程”、把 `审-11` 推进为“3D 系数已导＋锚已定位但不是 \(T_c\) 通路”、把 `临-20` 推进为“键局域求和＋BKT”；目标区已由 BKT 跳变推出 Uemura 标度的形状与失效机制；环 6 已给三项平衡的精确刻画、`临-25` 的不可判定判定与 `G19` 的容差分解；环 10 已把 `N-7` 降为适用域分类、把 `M6` 推进为“形状已导＋能标外生”；环 26 已把 `临-8` 判定为“不可焊接（强 no-go）”，$\zeta$ 形式只是规范截面上的读出，保留编号与未闭合状态。以上均**未闭合**。链外-B（\(\Upsilon\leftrightarrow\rho_s\)）与链外-F（\(\sigma_{\rm dc}\)）阻断了绝对 \(T_c\) 与 Homes 律。06 §0.5 的 \(\tau\to w\) 是否正式修订未决。主链状态栏未改，08 台账未改；等待审计后再决定是否合并。

## 研究纪律

- 禁止 `axiom`、`sorry`、`admit`、`native_decide`、`unsafe`；Lean 验证以 `lake build` 或 `lake env lean` 的实际输出为准。
- 新方程必须写清：前件、定义域、量纲、极限、单调性、可证伪条件、Lean 状态。
- 外部标准结论只作对照，不写成 CQM 已证；CQM 构造假设不得冒充定理。
- 任何“修正”先进入 `06_决策记录`，注明被替代的旧式与理由；未确认前不改主链。
- 数据验证只在链拉通后进行；在此之前只做量纲、极限与函数形状检查。

## R43–R71 核心机制攻坚 + V1 检验 + FE01 落地（2026-11-23～24，承接第二十六轮之后）

> 本段编号 R43–R49 为独立攻坚轮次，与上方"第 N 轮补"体系并行记录。全部为**工作台候选／框架扩展候选**，未落地主链结论、未闭合缺口、未改状态栏与账面。逐条总账见 `06_决策记录/2026-11-23_R43至R49核心机制攻坚总账.md`。
>
> **编号说明（R70 审计）**：本独立编号序列中 **R55、R63 为未使用编号**——R55 属并行"第 N 轮"外层编号体系（见主链第 55 轮注记），未进入本 R 序列；R63 在 Kesten 键阈值核对执行中调整为 R64。全目录无 R55/R63 内容，不以虚构填补。R70 为总账收口审计（只读 + 本注记，不产出新推导）。

- **R43（环4／`W-3′``审-3`）**：三支偏振权重进 $\sigma_0^2$ 前因子 $1+2\eta_t=5.59$；$\rho$ 形状与 $S_\rho=1/6$ 不随偏振变；回改漏 $q$ 因子与求积法。
- **R44（环15／`M8`）**：粗粒化指数 $t=\ln p_c/\ln p_{\rm thr}>1$（压缩映射），$t\ne t_\Upsilon$（不同普适类）；回删被否证的插值式。
- **R45（环16／`临-21`）**：$\xi$ 角色判定为标准相关长度（非全局域尺寸），容量标度 $n_{\rm eff}\propto|p-p_c|^{-8/3}$；全局域尺寸归读数层。
- **R46（环19／`审-11`）**：GL 梯度系数 $c=\Upsilon_0/2$，$\xi_{\rm GL}\propto|T_0-T|^{-1/2}$（平均场）；回改错误指数 $-3/2$。
- **R47（目标区／`链外-B`，B 类）**：$\kappa(T)\propto|T_0-T|^{1/2}/\sqrt{w}$ 温度形状；回改"降温下降"读反之误。
- **R48（环19／`审-11`）**：Ginzburg 判据从外部引用升级为链内推导，$t_G\propto N^{-6}$、$d_c=4$。
- **R49（环8／`临-24`）**：闭环乘积用 3D 核统一，$\langle\prod_Cr\rangle<1$ 恒成立，翻转分支链外不可达。
- **V1 综合计算检验**：七轮形状预言整合成 4×2 函数总图，18/18 通过（极限/单调性/量级/符号，非拟合）；回改综合脚本 R47 温度索引方向之误。
- **R50（环25／`临-23`）**：总效应 $K$ 的 $L^2$ 范数由 Parseval 定理 = 相变量子 $☯$（$\langle|K|^2\rangle_\tau=\sum1/(\gamma_n^2+1/4)=☯$），给 `临-23` 一个整体守恒量与"幅度不散"的一句写法；条件于 RH，不闭合变分半边；数值 Parseval 差 0.01%。
- **R51（环25／`临-23`）**：补变分半边——$K$ 是二次泛函 $\mathcal F[\tilde K]=\|\tilde K\|^2-2\mathrm{Re}\langle\tilde K,K\rangle$ 的唯一极小元，极小值 $-\|K\|^2=-☯$（Hilbert 最小二乘投影）；守恒（R50）+ 变分由 $☯$ 统一。变分是结构刻画非物理定律；`临-23` 仍不闭合（无动力学来源）。
- **R52（环26／`临-22`）**：总效应矩 $M_{-2}=☯$ 收敛 vs 总退相干矩 $M_{+2}=\sum\gamma_n^2$ 发散的对偶——低频携带总效应/高频承担退相干，给"高频零点先被抹掉、可读窗口 $N_{\rm eff}$ 有限"定量基础（与 26.B 已登记 $N_{\rm eff}$ 公式相容）。避坑：不拉通 R50 的 $K$ 与环26 的 $R_n$（R30 已判谱侧振幅与实空间深度不同构）。`临-22` 仍不闭合。
- **R53（环22／26，`临-17`/`临-22`）**：空间退相干（高斯、静态、相变后）与时间退相干（指数、动态、相变前）**不可混用/不可相乘**；可读窗口 $\gamma_*=\min(\gamma_*^{(a)},\gamma_*^{(v)}(t))$，交叉 $t_\times=\sigma_a^2/(2\sigma_v^2\tau_g)$（回改初稿分母搞反的四量级错误），短时空间主导、长时时间主导（`临-17`/`临-22` 仍不闭合）。
- **R54（环19／`临-19`）**：GL 磁场最小耦合（$q=2e$ 链内、$c=\Upsilon_0/2$ 替代 $\hbar^2/2m^\ast$ 属构造），给 $H_{c2}=\hbar k_B(T_0-T)/(e\Upsilon_0)$ 线性温度律；与临-19 的 $B_{c2}=\Phi_0/(2\pi\xi^2)$ 两路径自洽（差 0），斜率由 $\Upsilon_0$ 定（外生归一）、与 WHH 弱耦合同形（`审-11`/`临-19` 仍不闭合）。
- **V1 扩展跨轮一致性检验**：把 R43–R54 十二轮成果做 5 组跨轮交叉核对（$☯$ 守恒/变分/对偶同值、R52/R53 时间截止同式、R46/R54 共用 $\Upsilon_0$、R44/R45/R52 共用 $\nu=4/3$、R43/R49 共用 $S_\rho=1/6$），**13/13 PASS**——验证十二轮真正自洽、无口径冲突（模型形状核对，非数据拟合）。
- **R56（环18／`审-5`/`临-3`）**：几何上限（2D $p_{\rm loop}=1/2$ 拓扑饱和）与资源上限（$\sum n_k\le n_{\rm eff}=N(0)\Delta\varepsilon$，全维度）维度判定——2D 几何可达、3D 靠资源，消除 `审-5` 混用；给 `临-3` 的 $n_{\rm eff}\propto N(0)$ 接口（`审-5`/`临-3` 仍不闭合）。
- **R57（目标区）**：两个 $T_c$ 上界的"取小者"定量展开——$\mathcal R=T_{\rm B}/T_{\rm A}$，2D 小 $\Upsilon$ ⇒ 刚度/Uemura 上界紧、3D 大 $\Upsilon$ ⇒ 判据/配对上界紧，与环19 (11L.13) 维度表自洽（模型判据比较，非数据拟合）。
- **R58（环25／`M10`）**：记忆积分 $\mathcal I_K$ 因 $K$ 准周期零均值振荡而**一致有界**（非 diffusion），界 $\le2\sum|r_n|/\gamma_n\le\sqrt{☯\sum1/\gamma_n^2}$——与 (25.2) $\chi(\omega\to0)$ 有限自洽、与 R50 的 $☯$ 通过 Cauchy–Schwarz 联系；回改初稿"$\sqrt t$ 增长"之误（`M10` 仍不闭合）。
- **R59（核心常数核对）**：README 权威值 $☯=\xi'(1)/\xi(1)=0.02309570897$ 的两种定义（导数 $s=1$、谱和）mpmath 40 位一致到 11 位；厘清符号细节（$\xi'(0)/\xi(0)=-0.0231$ 负、$\xi'(1)/\xi(1)=+0.0231$ 正，由函数方程）——确认 R50 数值基础正确，不改权威值。
- **R60（M1 判别子核对）**：主链第 634 行登记的零点相邻比 $1.4873/1.7695/2.1525$ 用标准零点虚部核对，3/3 吻合（4 位有效）——确认判别子数学正确（非 M1 物理证实）；承 R59 的主链数值基础核对。
- **R61（全链结构地图 v2）**：把 R43–R60 十八轮按四轴（DAG 串联+层级状态+共享量+可证伪清单）整合成 `03_推导工作台/全链结构地图_R1R60.md`——5 条新增串联链、共享量拉通表（$☯$/$S_\rho$/$\nu$/$\Upsilon_0$/$\gamma_*$）、绝对 $T_c$ 缺口精确位置；DAG 图 21 节点/16 边 is_dag=True（非拟合）。组织层整合，不改状态/权威源。
- **R62（零点计数核对）**：用 MathWorld OEIS A072080 核对 Riemann–von Mangoldt $N(T)\sim\frac{T}{2\pi}\ln\frac{T}{2\pi}$，比值 0.658→0.917 趋向 1、含次领头项后精确为 1——确认 R50 $☯$ 收敛/R52 对偶/可读窗口的计数基础（外部标准数学，非 CQM 推出）；主链数值基础核对系列第三个（承 R59、R60）。
- **R64（键阈值核对）**：并查集 Monte Carlo（L=16/24/32）核对 Kesten 2D 键渗流阈值 $p_c=1/2$，给 0.5017/0.4997/0.5006（误差<0.4%）——确认 R56 几何上限/推6撤销/环15座键口径的数值基础（外部标准数学，非 CQM 推出）；主链数值基础核对系列第四个。
- **R65（gap ratio 常数核对）**：mpmath 40 位核对 $2\pi/e^{\gamma_E}=3.52775398...$，C5 表 3.528（3位）、README 3.5278（4位）四舍五入正确、Al 精密实验 3.53 差 0.064%——核对系列第五个、唯一把理论纯数与超导实验读数两端都核对者（BCS 标准已标源、C5 同形非还原）。
- **R66（权威口径表同步）**：把 R43–R65 成果同步进 `00_当前有效口径表.md`（新增 8 行：3D $S_\rho=1/6$、$☯$ 守恒/变分、GL 梯度系数、Ginzburg、$H_{c2}$、收敛-发散对偶），消除旧注记 $S_\rho=-0.0226$（2D）与主值 $1/6$（3D）的内部矛盾——落实"修改必须同步全项目"，防干扰权威表与最新推导一致。
- **R67（端到端 CQM 自身 T* 检验·关键）**：首次用 CQM 自身 $T^\ast=1.13e^{-1/6}\hbar\omega_{\log}e^{-(1+\lambda)/\lambda}$（无 $\mu^\ast$）对三独立参数材料直接算 $T_c$——**系统性高估 2.65–6.33×**；加 $\mu^\ast$ 压制后落到实验 0.92–1.03×。定量证实 $\mu^\ast$ 是绝对 $T_c$ 的决定性归一输入（与 R38 的 $F_{\mu^\ast}=0.19$–$0.37$ 吻合）——形状链正确、绝对 $T_c$ 需能标+$\mu^\ast$ 两外生输入。诚实定位，非失败。**（R69 更正：$\mu^\ast$ 权威归属为链外-A，非 `审-14`）**
- **R68（$\mu^\ast$ 形状解释）**：用 Morel–Anderson 形状 $\mu^\ast=\mu/(1+\mu L)$（$L=\ln\varepsilon_F/\hbar\omega_D$）解释 R67 经验 $\mu^\ast\approx0.10$——典型 $L=2$–$5$ 下裸 $\mu=0.1$–$0.2$（常规金属范围）经对数压制自然给 $\mu^\ast=0.10$–$0.14$；裸 $\mu$ 越大压制越强 ⇒ 普适小。**（R69 更正：$\mu^\ast$ 权威归属为链外-A，非 `审-14`）**
- **R69（口径更正 + 落地路径放弃·决断）**：合规前置审查发现——①主链 §1439 明确库仑赝势 $\mu^\ast$ 属**链外-A**（限制(4)：链内 $V<0$ 恒成立、无"负净耦合"态），`审-14` 实为 Γ 第一性来源（§1623），R67/R68 归属误用已更正；②06 无 Coulomb 赝势口子。**放弃"裸 $\mu$ 第一性来源落地"路径**：链内无排斥自由度（落地=引入新物理，触"不虚构"红线）+ 外生输入无限回退（$\mu^\ast\to n,z_v,m$）。**决断：CQM 是形状理论，绝对 $T_c$ 两类归一（能标 $\omega_D$ + Coulomb $\mu^\ast$）结构性外生——命题 Z2/限制(4) 定位，非工作未完成，不可虚构突破。**
- **FE01 落地（命题 Z2，框架扩展）**：带量纲公设给 $\omega_D$ 公设级来源，得绝对 $T_c$ 能标结构 (FE.3)；承 v1.9.249 FE10 先例登记，标注框架扩展/非第一性/不闭合缺口；端到端独立参数判定单带 3–8% 有效、多带失效（见 `08_框架扩展候选/`）。
- **R70（总账收口审计）**：对 R43–R69 做全面交付物核对——决策记录覆盖 25 个 R 编号；全目录 150 个 Lean 剥注释后禁用项 **0 命中**、编译通过；计算产物 152 py/152 png/157 csv/31 摘要、无空文件；README 声明的 12 个关键文件 12/12 存在；三道核查全过。发现编号缺 R55/R63 已加说明注记。**只读审计，不产出新推导、不改结论与状态**。

> 每轮均通过 Lean（无禁用项）+ 数值断言 + 函数图像 + 决策记录；三道核查 `check_provenance` 10/10、`check_consistency` 41/41、`consistency_probe` 0 问题。

## R71：环 2 `W-3` 量纲桥 + 零点幅度预算（2026-11-24）

**性质**：补缺口（`W-3`），**不改状态栏**、不动 06／08／研究站。这是全链最靠前的未闭合缺口。

- **量纲桥**：$L_{ij}=-\tfrac12\sum_T\cot\theta^T$ 是 FEM **刚度**（无量纲），离散算子须除以质量矩阵；故 $\boxed{\omega_q^2=c_s^2\lambda_q/\Omega^{2/d}}$——量纲因子**只能是节点测度**，不能是材料常数。纯数 $K$ 由声学极限定：二维正三角网格（Voronoi 测度）**解析给 $K=1$**（$\lambda_q=A_vq^2$，$q\ell\le10^{-3}$ 时数值偏差 $<2\times10^{-3}$），三维各格型 $K$ 为 $O(1)$ 纯数、不进标度。
- **截断被钉成唯一值**：模式计数 ⇒ $Q=(6\pi^2n)^{1/3}$、$\Theta_D=(\hbar c_s/k_B)(6\pi^2n)^{1/3}$（Debye 恒等式，外部标准工具），与 `审-10`"截断＝谱支集"一致；$\Theta_D$ 由"独立外生输入"降为 $(c_s,n)$ 的合成。
- **角／位移量错位分离**：$(2.1)$ 的 $\Delta\varepsilon$ 与 $\sqrt{\hbar/2\rho_m\omega}$ 差一个 $G_q$（$[G]=1/L$，$|G_q|^2\propto q^2$ 用第 85 轮结论）。
- **小参数（链内首次可算）**：$\sigma_0^2=c_\varepsilon^2\cdot1.4617(\ell_q/a_n)^4$，$\ell_q=(\hbar/\rho_mc_s)^{1/4}$、$a_n=n^{-1/3}$（节点测度尺度，**不是晶格常数**）；$\sigma_\varepsilon=1.209\,c_\varepsilon(\ell_q/a_n)^2=(0.028$–$0.061)c_\varepsilon$（Al/Nb/V/Ta/Pb）⇒ 线性响应自洽（$\sigma_\varepsilon\lesssim0.03$ 当 $c_\varepsilon\lesssim0.5$）。
- **同位素**：$\alpha=1/2$ 由 $\Theta_D\propto M^{-1/2}$ 直接给出（不再只是端点分类）。
- **振幅预算（B 类，用观测 $\lambda$）**：反解形变势 $g=1.7$–$3.6$ eV（$g_{\rm pol}=1$、$1-\rho=0.9$）、$0.7$–$1.5$ eV（并入 R43 的 $5.59$）——**判定"边缘"而非"自洽"**：V／Nb 在偏振端点跌破 $1$ eV，须先定三个 $O(1)$ 因子（$|G_q|^2$ 角向系数、$g_{\rm pol}$、$1-\rho$）。`缺口 N-A` 由此被定量化：$g$ 必须是 $O(1$–$10)$ eV 量级。
- **交付**：`03_推导工作台/环02_W3量纲桥与振幅预算.md`、`01_文献基线/文献卡_L71a/b/c`、`04_计算验证/环02_W3量纲桥.py`（+4 png/csv，四断言全过）、`05_Lean验证/PhononDimensionalBridge.lean`（3 定义＋14 定理，退出码 0，无禁用项）、`06_决策记录/2026-11-24_R71_W3量纲桥与振幅预算.md`。
- **残量**：三个 $O(1)$ 因子（$|G_q|^2$ 角向系数、$g_{\rm pol}$ 与 R43 的 $5.59$、$1-\rho_{ij}$）——振幅预算定案的前提；三维格型纯数 $K$；$\mathrm{RMS}(\varepsilon^{(0)})$（FG 接口）。
- **本轮回改（自查）**：首算误把晶格常数当节点测度尺度，致 $\sigma_0^2$ 对 fcc 低估 $6.35$ 倍、bcc 低估 $2.52$ 倍，"自洽"结论随之降为"边缘"；已按 $a_n=n^{-1/3}$ 重算并同步四处口径。
- **主链同步**：环 2 缺口行、环 3 缺口行、§0.5 环 2 行、§15 环 2／环 3 行；`W-3` 登记为**量纲层闭合**，状态栏未动。

## R72：BCC 复形上 cot 拉普拉斯的实数——二面角订正、$L$ 四性质、三维纯数 $K$（2026-11-24）

**性质**：补缺口（`W-3` 的 3D 残量、环 3 的 `|cot|` 适用域）＋**订正第 77 轮的数值**；不改状态栏、不动 06／08／研究站。

- **订正**：BCC 长边（最近邻 $\sqrt3a/2$）的内二面角是 $\pi/3$（$60^\circ$）、绕边 **6** 个四面体，不是原记的 $2\pi/3$（$120^\circ$）、3 个。两条独立依据：菱形四面体直接算（脚本对正四面体自检 $70.529^\circ$）；绕最近邻键的 $C_3$ 对称要求 $k$ 为 3 的倍数，而 $3\times60^\circ\ne2\pi$。**结论不变**（$k\theta=2\pi$ ⇒ $\varepsilon_e=0$、$\prod_Cr=1$、三值几何不可实现），变的只是 $\cot$ 的符号。
- **$\cot$ 权**：$W_{\mathrm{NN}}=6\cot60^\circ=2\sqrt3>0$、$W_{\mathrm{NNN}}=4\cot90^\circ=0$；$L=\sqrt3(8I-A_{\mathrm{NN}})$。
- **$L$ 四性质首次实测成立**（16 原子周期超胞）：对称、零行和（$8.9\times10^{-16}$）、半正定（$\min\lambda=-10^{-16}$）、单零模。
- **三维纯数 $K$**：$\lambda_q=K\Omega^{2/3}q^2$，$K=2^{2/3}\sqrt3=2.749459$；$[100]/[110]/[111]$ 在 $q^2$ 阶各向同性（差 $<10^{-5}$），各向异性只在 $q^4$。校准：$\omega_q=\sqrt Kc_sq$，等价于把刚度除以 $K$ 后 $\omega_q=c_sq$。R71 的 $\sigma_0^2$ 与振幅预算**不受影响**（用的是校准后色散）。
- **`|cot|` 的适用域**：$k\le4$ ⇒ 必有某 $\theta\ge\pi/2$（Lean 两条），权 $\sum\cot\theta$ 的符号不受保证，此时才需要 $|\cot|$；$k=5$ 起保证失效（$5\times72^\circ=2\pi$）；BCC 的 $k=6/4$ 上权为正／零，$|\cot|$ **空转**。
- **边界**：仅最近邻耦合的 $\cot$ 模型只给一个弹性模量，不能复现 $c_{11},c_{12},c_{44}$——$L$ 是运动学模式生成器，$K$ 只能作标量校准；只算 BCC（FCC 需先定八面体对角线）。
- **交付**：`03_推导工作台/环02_环03_BCC的cot拉普拉斯与K.md`、`04_计算验证/环02_环03_BCC的cot拉普拉斯与K.py`（+png/csv，五组断言全过）、`05_Lean验证/BCCLatticeLaplacian.lean`（12 定理，退出码 0）、`06_决策记录/2026-11-24_R72_BCC的cot拉普拉斯与K.md`；订正 `环03_平直三角化与三环乘积判定.md`（加 §〇）、`2026-11-23_环03平直三角化判定.md`、主链环 3 注记、口径表第 77 轮条。
- **工具坑**：BCC 点集的 Delaunay 有大量零体积退化单纯形，必须按体积 $>10^{-9}$ 剔除，否则统计出 $k\in\{2,\ldots,6\}$ 的伪值（本轮第一次跑出的假信号）。

## R73：亏角的承载者——位移盲性、(4.1) 载体订正、`审-21`（2026-11-24）

**性质**：**方程订正**（(4.1) 的载体，不是数值）＋新登记 `审-21`；不改状态栏、不动 06／08／研究站。

- **判定的来历**：R71/R72 两轮都在追"$|G_q|^2$ 的 $O(1)$ 因子"。本轮先去算 $G$ 本身，一算就发现它**恒为零**。
- **平直盲性（定理级）**：固定组合的三角化嵌入 $\mathbb R^3$ 时，绕内部铰链的二面角之和恒为 $2\pi$（邻域被四面体铺满），故 $\varepsilon_e\equiv0$，**与顶点位置无关**。数值：BCC $4\times4\times4$、20 条内部铰链，随机位移到 $0.1a$、平面波 $q\le2$、均匀应变、六个应变模，全部 $\le1.8\times10^{-15}$。这把第 85 轮的"平坦参考不能承载 $\varepsilon$"从"几档数值"升级为定理。
- **两扇区分解**：$\delta\ell=\delta\ell^{\rm emb}\oplus\delta\ell^{\rm intr}$，$\varepsilon$ 只由内禀（不可嵌入）部分承载。单边边长 $\delta$ 给线性斜率 $-2.599$（$|\delta|\le2\%$ 残差 $3.9\times10^{-4}$）；整体均匀缩放给 $1.8\times10^{-15}$；随机内禀扰动 $10^{-4}$ 给 $1.4\times10^{-3}$；$A$（$20\times685$）$\max|A|=4.00$、$\|A\|_F=29.65$。
- **(4.1) 按字面恒等于零**：$G_{ek}=\partial\varepsilon_e/\partial q_k\equiv0$ ⇒ $\langle(\Delta\varepsilon_e)^2\rangle_T\equiv0$。这解释了历轮"$\sigma_0^2$ 归一不了"的根因：被归一的量本身为零。
- **载体订正**：$\langle(\Delta\varepsilon_e)^2\rangle_T=\sum_{e'}A_{ee'}^2\langle(\delta\ell^{\rm intr}_{e'})^2\rangle$；$A$ 可算，$\delta\ell^{\rm intr}$ 属 FG 扇区（链内无载体）。
- **两读法只能取一**：同物读法（$\varepsilon$ 既是亏角又是 (4.1) 的场）⇒ 必须改载体；异物读法（(2.1)/(4.1) 的 $\varepsilon$ 只是应变标量）⇒ (4.1) 自洽但环 5 的 $v_\tau$、环 8 的 $C_{ij}$ 失去前件。按链条实际用法取前者。
- **对 R71 的订正**：$\sigma_0^2$ 的**标度保留**（$Q^4$、$(\ell_q/a_n)^4$、$\hbar/\rho_mc_s$），**振幅来源撤销**（位移零点幅度）；$c_\varepsilon=\kappa\,\mathrm{RMS}(\varepsilon^{(0)})$ 属 FG 数据；振幅预算数值 $g=1.7$–$3.6$ eV 不变、可靠性下降。
- **新登记 `审-21`**：内禀扇区的统计与温度入口（是否热化、以何模谱热化，链内无载体）。
- **交付**：`03_推导工作台/环04_亏角的承载者与内禀扇区.md`、`04_计算验证/环04_亏角对位移不变性与内禀传递.py`（+png/csv，五组断言全过）、`05_Lean验证/DeficitIntrinsicSector.lean`（9 定理，退出码 0）、`06_决策记录/2026-11-24_R73_亏角载体与内禀扇区.md`；同步主链 §11（`审-21`）、环 4 缺口行、§15、§16 排序口径、口径表边界注记、缺口重审环 4 行；订正 R71 卡与决策记录。
- **工具坑**：四面体由 6 条边长重建时，若面的三角形接近退化会除零——须按最长边重排顶点；剪切应变张量的非对角元要取 $1/2$（否则 $I+\varepsilon$ 奇异，$\det=0$ 直接给 NaN）。

**第 87 轮补（环 4／`审-21` 后续：亏角涨落载体确立与温度入口 (4.1′) 重建；成果登记 R-96；2026-11-24）：**

- **触发**：R73 判亏角对位移恒为零、(4.1) 按字面恒等于零、新登记 `审-21`——全链唯一 $T$ 入口的前件危机，正卡在最前端。
- **文献调研**：arXiv:1110.6866 §2（平直背景边长扰动二阶展开 $S=S^{(0)}+\tfrac12H_{ee'}\lambda_e\lambda_{e'}$、$H_{ee'}=-\partial\omega_e/\partial l_{e'}$）；arXiv:0912.1817 §4／arXiv:0810.3594（顶点位移模 $Y_I^e$ 满足 $Y_I^e\partial\epsilon_\Delta/\partial l^e|_{\rm flat}=0$，是 Hessian 零模／离散微分同胚残余）；PRD **76**, 104020／**91**, 124034（非零本征方向是曲率激发）。只作标准工具对照，不声称 CQM＝量子引力。
- **载体判定**：位移模是 Regge Hessian 规范零模（$Y_I^eA_{ee'}|_{\rm flat}=0$、$Y_I^eH_{ee'}=0$），不承载亏角；载体＝$\ker H$ 正交补上的非规范曲率激发模 $v_k$（$Hv_k=k_kv_k,\ k_k>0$）。这把 R73 的"内禀扇区"精确化为链内结构可承载的子空间。
- **温度入口恢复**：二阶作用量给 $\langle\xi_k^2\rangle_T=c_k^0[1+2n_B(\omega_k)]$，故 (4.1′) $\langle(\Delta\varepsilon_e)^2\rangle_T=\sum_k|A\cdot v_k|_e^2c_k^0[1+2n_B(\omega_k)]$——结构等同 (4.1)、只换载体，**全链 $T$ 入口唯一性未破坏**。三点可检：零点有限正值（否证恒零）、对 $T$ 严格单增、高温上界 $\le\sum c+2T\sum(c/a)$。
- **历史唯物主义合规**：Hessian 本征结构（哪些模是规范零模）＝几何基础决定热读数的定义域；必然性（零模空间几何固定）＋偶然性（模谱／占据由材料与制备定）分层统一；未用社会范畴作物理证据；结构同构不是还原。
- **诚实边界**：$\{k_k,\omega_k,c_k^0\}$ 绝对值与热化判据外生（FG／`E4`）；`审-10` 截断位置未定；`审-21` **推进但不闭合**；状态栏、编号、账面、06／01／08、研究站均未动。
- **交付**：`03_推导工作台/环04_亏角涨落载体_Regge曲率模与温度入口重建.md`、`05_Lean验证/ReggeCurvatureModes.lean`（8 定理，`lake env lean` 退出码 0、无警告、无禁用项）、`04_计算验证/环04_Regge曲率模温度入口.py`／`.png`／`.csv`／`_摘要.csv`（四面板九断言，非拟合）、`06_决策记录/2026-11-24_第87轮_亏角载体与温度入口重建.md`；同步主链环 4 缺口行／§11 `审-21`／§15 环 4 缺口列／§16、`成果登记.md` R-96、`缺口重审.md` 环 4 行、`00_当前有效口径表.md` §一边界注记。
- **删除／防干扰**：删去"(4.1) 的 $G_{ek}$ 是位移简正模投影"与"内禀扇区统计链内完全无结构可说"两读法；未删任何编号、状态或推导卡。

**第 88 轮补（环 4／`审-10` 后续：曲率模谱与占据截断；成果登记 R-97；2026-11-24）：**

- **触发**：§16 第 1 位的 `审-10`——"被占据模谱的截断位置未定"。第 87 轮确立曲率模载体后，该问题可落在曲率模谱上并与 R71/R72 的余切拉普拉斯谱对接。
- **文献调研**：arXiv:0707.4513 (PRD **76**, 104020) 式27–28（Regge Hessian 非零 sector＝格点拉普拉斯、单零模）；arXiv:2408.04877（余切权 $c_{ij}=\tfrac12(\cot\alpha^k+\cot\alpha^l)$、节点质量决定非零本征值）；DOI 10.1007/s00211-011-0394-z（线性化 Regge 本征对按非一致 FEM 收敛）——均作标准工具对照，不声称 CQM＝量子引力。
- **谱对应**：曲率模 ↔ 余切拉普拉斯非零模，色散 $\omega_q^2=c_s^2\lambda_q/\Omega^{2/d}$（R71）；零模（顶点位移↔均匀平移）是规范模、不进 (4.1′)；$H$（边基）与 $L$（点基）模重数不同但共用色散。
- **截断判定**：先占据最低非零模（$n_B\to k_BT/\hbar\omega_q$、单模 $\propto1/\omega_q^2$）；Debye 模计数 $F(q)=(q/Q)^3$、$F(Q)=1$、$\Theta_D=(\hbar c_s/k_B)Q$ ⇒ **截断＝谱支集端点 $\Theta_D$，不是 $\omega_{\log}$**（后者是对数矩、差 $e^{1/6}$，`审-17` B 类不动）。2D 红外 $\ln(L/a)$ 与 §0.2 的 $T_{\rm BKT}(L)\sim1/\ln L$ 同标度族（只形状对应、不证明 BKT）。
- **历史唯物主义合规**：谱结构（基础）决定占据从哪端开始、截断在哪（热读数），读数不能反写谱结构；必然性（零模/非零模分野几何固定）＋偶然性（$c_s,n,\lambda_q$ 与具体占据材料决定）分层统一；结构同构不是还原；未用社会范畴作物理证据。
- **诚实边界**：$c_s,n,\omega_q$ 绝对值与绝对 $T_c$ 外生（R71／命题 Z2），热化判据属 `审-21` 残余 ⇒ `审-10` **推进但不闭合**；不证明 BKT、不碰 `临-8`／`临-22`／RH；状态栏、编号、账面、06／01／08、研究站均未动。
- **交付**：`03_推导工作台/环04_审10_曲率模谱与占据截断.md`、`05_Lean验证/CurvatureModeSpectrum.lean`（7 定理，`lake env lean` 退出码 0、无警告、无禁用项）、`04_计算验证/环04_审10_曲率模谱与占据截断.py`／`.png`／`.csv`／`_摘要.csv`（四面板九断言，非拟合）、`06_决策记录/2026-11-24_第88轮_曲率模谱与占据截断.md`；同步主链环 4 缺口行／§11 `审-10`／§15 环 4 缺口列／§16 第 1／36 项、`成果登记.md` R-97、`缺口重审.md` 环 4 行、`00_当前有效口径表.md` §一边界注记。
- **删除／防干扰**：删去"截断在 $\theta_D$ 与 $\omega_{\log}$ 之间待选"与"占据截断可凭唯象拟合定"两读法；未删任何编号、状态或推导卡。

**第 89 轮补（环 19／目标区／`审-11` 后续：自由能三扇区与比热跳变；成果登记 R-98；2026-11-24）：**

- **触发**：§16 第 2 位的 `审-11`——"完整 $f(T,P,B;\varphi)$ 仍未给，绝对 $T_c$ 的剩余缺口在振幅扇区"。第 88 轮已得曲率模谱与 Debye 截断，可据此从链内模谱直接写热自由能并与 C5/R-33 三扇区合成。
- **文献调研**：Debye 热自由能 $F=E_Z+k_BT\sum_q\ln(1-e^{-\hbar\omega_q/k_BT})$、低温 $-AT^4$、$C_V\propto T^3$（TU Graz / Caltech 127）；BCS 凝聚能 $F_N(0)-F_S(0)=\frac12N(0)\Delta_0^2$、近 $T_c$ 的 $\Delta^2=\frac{8\pi^2}{7\zeta(3)}(k_BT_c)^2(1-T/T_c)$ 与 $\Delta C/\gamma T_c=12/(7\zeta(3))=1.43$（Molinari BCS notes Eq.(25)(30)；arXiv:2312.11310 Lemma 2.2）——均作标准工具对照，不声称 CQM＝BCS。
- **曲率热扇区**（新）：同一批曲率模给 $F_{\rm curv}=\sum_q[\hbar\omega_q/2+k_BT\ln(1-e^{-\hbar\omega_q/k_BT})]$、$c_V\propto T^3$（3D Debye），与 (4.1′) 的 $[1+2n_B]$ 同源、温度入口唯一；有限 $T$ 解析 ⇒ **锚的非解析性不来自热占据**。
- **振幅凝聚扇区**（新）与关键订正：$T=0$ 精确 $F_N-F_S=\frac12N(0)\Delta_0^2$（由 C5 的 $\Delta(0)$）；**近 $T^*$ 必须用 GL 二次律 $F_S-F_N\propto-(T^*-T)^2$**（因 $\Delta^2\propto(1-T/T^*)$、$F=-\frac b2\Delta^4$），不能把 $T=0$ 的 $-\frac12N(0)\Delta^2(T)$ 外推（会给错误线性律）；比热跳变 $\Delta C/\gamma T^*=12/(7\zeta(3))=1.426$。
- **三扇区合成与非解析性清单**：$f=F_{\rm curv}+F_{\rm ph}+(F_S-F_N)_{\rm amp}$；曲率光滑／相位 2D BKT 跳变或 3D 平方根支点／振幅 $T^*$ 比热跳变。锚只给相位扇区非解析点、是 $T_c$ 上界，$T_c=\min(T^*,T_{\rm ph},T_\theta)$ 不动。
- **历史唯物主义合规**：模谱与 C5 隙方程（基础）决定三扇区自由能与跳变（热读数），读数不反写谱结构；必然性（非解析性位置几何/方程固定）＋偶然性（$c_s,n,N(0),\lambda$ 材料值）分层统一；结构同构不是还原；未用社会范畴作物理证据。
- **诚实边界**：$c_s,n,N(0),\lambda$ 绝对值与绝对 $T_c$ 外生；系数 $12/(7\zeta(3))$ 借外部标准工具（指数 $-2$ 由链内 C5 给）；强耦合/多带不适用；不证明 BKT、不碰 `临-8`／`临-22`／RH ⇒ `审-11` **推进但不闭合**；状态栏、编号、账面、06／01／08、研究站均未动。
- **交付**：`03_推导工作台/环19_审11_自由能三扇区与比热跳变.md`、`05_Lean验证/FreeEnergyThreeSectors.lean`（12 定理，用二阶差商替代导数 API，`lake env lean` 退出码 0、无警告、无禁用项）、`04_计算验证/环19_审11_自由能三扇区与比热跳变.py`／`.png`／`.csv`／`_摘要.csv`（四面板七断言，非拟合；面板 C 直观对照二次律与错误线性律）、`06_决策记录/2026-11-24_第89轮_自由能三扇区与比热跳变.md`；同步主链 §11 `审-11`／§15 环 19／§16 第 2 项、`成果登记.md` R-98、`缺口重审.md` 环 19 行、`00_当前有效口径表.md` §二已推形状表。
- **删除／防干扰**：删去"$T=0$ 的 $-\frac12N(0)\Delta^2(T)$ 外推全温区"与"锚的非解析性来自热占据"两读法；未删任何编号、状态或推导卡。

**第 90 轮补（环 15／`审-4` 后续：关联修正的座→键映射与渗流阈值位移；成果登记 R-99；2026-11-24）：**

- **触发**：§16 第 3 位的 `审-4`——"材料对账仍属外部"。核查发现 `环15_座键口径.md` 的 $\mathbb E[B]=p^2$ **建立在独立座假设上**，但 $p_{\rm pair}$ 来自带关联 $\rho$ 的高斯场（G1–G3；第 84 轮 Bessel 核）——这是还能推进的结构半边，且能把环 4 关联、审-4、临-11 三者拉通。
- **文献调研**：Plackett (1954) 恒等式 $\partial_\rho\Phi_2=\phi_2>0$、均值阈值精确 $P=\frac14+\frac{\arcsin\rho}{2\pi}$（Genz, *Computation of MVN and t Probabilities* §2.1）；关联渗流正关联降阈值（arXiv:1305.6941：0.5927→0.5546；arXiv:1708.02296 表）——均作标准工具对照，不声称 CQM 推出渗流阈值数值。
- **关联修正映射**：$\mathbb E[B_{ij}]=p^2+\bar c_{ij}$（旧 $p^2$ 是 $\rho\to0$ 极限）；$\bar c=\rho\phi(z)^2+O(\rho^2)$、均值阈值精确 $\arcsin\rho/(2\pi)$；$q=p^2+\bar c\ge p^2$。**不引入新参数**——$\rho$ 就是 (9.1) 同一个量。
- **阈值位移**：$p_*=\sqrt{p_c(0)^2-\bar c}=p_c(0)-\bar c/(2p_c(0))+O(\bar c^2)$，正关联**降阈值**（与外部关联渗流同向）；给"对账真实单层体系"的结构口径：单层不存在"因 2D 键阈值不能渗流"的问题（推 6 已撤销），真实关联只会更早渗流。
- **临-11 拉通**：同一 $\bar c$ 控制阈值位移与自平均失效 ⇒ **自平均成立 ⇔ 阈值位移可忽略**，是同一条件的两面——环 4 关联、审-4 映射、临-11 自平均三者拉通。
- **历史唯物主义合规**：关联结构（基础）决定连通性读数，读数不反写关联结构；必然性（正关联必降阈值）＋偶然性（$\rho$ 归一、$p_c(0)$ 实现外生）分层统一；结构同构不是还原；未用社会范畴作物理证据。
- **诚实边界**：$\rho$ 归一与 $p_c(0)$ 材料实现外生；系数 $\phi(z)^2$ 条件于 G1–G3 高斯假设；外部 6% 位移是特定模型值、**不是** CQM 数值预言；绝对 $T_c$ 受命题 Z2 限制 ⇒ `审-4` **推进但不闭合**；状态栏、编号、账面、06／01／08、研究站均未动。
- **交付**：`03_推导工作台/环15_审4_关联修正的座键映射与阈值位移.md`、`05_Lean验证/CorrelatedSiteBond.lean`（10 定理，`lake env lean` 退出码 0、无警告、无禁用项）、`04_计算验证/环15_审4_关联修正座键映射.py`／`.png`／`.csv`／`_摘要.csv`（四面板八断言，非拟合）、`06_决策记录/2026-11-24_第90轮_关联修正座键映射.md`；同步主链 §11 `审-4`／§15 环 15／§16 第 3 项、`成果登记.md` R-99、`缺口重审.md` 环 15 行、`00_当前有效口径表.md` §二已推形状表。
- **删除／防干扰**：删去"$\mathbb E[B]=p^2$ 普遍成立"与"座阈值 0.592746 与关联无关"两读法（旧卡保留作 $\rho\to0$ 极限记录）；未删任何编号、状态或推导卡。

**第 91 轮补（环 6→8／`审-1` 后续：矩阵分支的 Hessian 重证与 $f^{-1}$ 的锚邻域闭合；成果登记 R-100；2026-11-24）：**

- **触发**：§16 第 13／33 位的 `审-1`——"最靠前的断口，缺 $f$ 显式与累积层 $f^{-1}$"。第 87/88 轮已把位移模判为 Hessian 规范零模、曲率模（和乐边量 $\lambda$）承载亏角；第 78 轮给 $f'(0)=-1/v_\tau^2<0$——三者合起来可重证矩阵分支并在锚邻域求逆。
- **文献调研**：反函数定理与级数反演 $b_1=1/a_1$、$b_3=-a_3/a_1^4$（Dominici, arXiv:math/0501052 §1；mathlib `AnalyticAt.analyticAt_localInverse`）；和乐边量赋于界面穿越、$h_{ji}=h_{ij}^{-1}$、路径有序乘积（arXiv:2610.00593 §II.1；arXiv:1709.08373）——均作标准工具对照，不声称 CQM＝量子引力。
- **矩阵分支重证**：位移模＝Hessian 规范零模（节点标量 $v_\tau$ 侧），亏角只由曲率模承载、其边量表示即和乐侧 $\lambda_{ij}$（反对称、路径乘积）；故 $C=\delta+f(\lambda)$ 是曲率侧自然描述。依据从已撤回的三环边界读数改为 Hessian 规范/曲率二分（结构层，不随样品尺寸变）。
- **锚邻域求逆**：锚＝$\varepsilon=0$⇔$\lambda=0$⇔$u=C-I=0$，恰在 $f'(0)=-1/v_\tau^2<0$ 的可逆邻域 ⇒ 局部 $f^{-1}$ 对判据层足够、不需全局单调；逆级数 $b_1=-1/c$、$b_3=-d/c^4$ 给 $u$／$u^3$ 系数**精确抵消**、误差 $O(u^5)$（数值斜率 5.006），一阶 $\lambda=v_\tau^2(C-I)+O(u^3)$，相对修正 $|d|u^2/c^3$（$c=1$ 归一回到第 78 轮界，链精度下不可见）。
- **诚实边界**：$d$、可逆半径外生、全局可逆未给（$|\lambda|\ge\sqrt{c/3|d|}$ 可逆性可失效）；梯度扇区单函数 no-go **不推翻**（本轮是矩阵分支边量扇区）；$\theta=\alpha\lambda$ 仍属 `G19`；绝对 $T_c$ 受命题 Z2 限制 ⇒ `审-1` **推进但不闭合**；状态栏、编号、账面、06／01／08、研究站均未动。
- **历史唯物主义合规**：Hessian 二分（基础）决定可逆读数，读数不反写 Hessian；必然性（$f'(0)<0$ 由 DM.4＋FG 固定）＋偶然性（$d$、$v_\tau$ 材料外生）分层统一；结构同构不是还原；未用社会范畴作物理证据。
- **交付**：`03_推导工作台/环08_审1_矩阵分支的Hessian重证与f逆的锚邻域闭合.md`、`05_Lean验证/MatrixBranchInverse.lean`（10 定理，`lake env lean` 退出码 0、无警告、无禁用项）、`04_计算验证/环08_审1_矩阵分支求逆与锚邻域.py`／`.png`／`.csv`／`_摘要.csv`（四面板八断言，非拟合）、`06_决策记录/2026-11-24_第91轮_矩阵分支求逆与锚邻域.md`；同步主链 §11 `审-1`／环 8 缺口行／§15 环 7／§16 第 13 与 33 项、`成果登记.md` R-100、`缺口重审.md` 环 7／8 行、`00_当前有效口径表.md` §二已推形状表。
- **删除／防干扰**：删去"矩阵分支由 06 三环几何强制"（第 82 轮已撤回三环依据）与"累积层 $f^{-1}$ 完全缺失"两读法（后者锚邻域已闭合、不夸大全局）；未删任何编号、状态或推导卡。

**第 92 轮补（环 14.A／目标区／`审-15`／`审-17` 后续：链内 $\alpha^2F$ 构造与两矩分歧的结构消解；成果登记 R-101；2026-11-24）：**

- **触发**：`审-17`（第 62 轮）把 CQM $\omega_{\log}=e^{-1/3}\theta_D$ 与 Eliashberg $\omega_{\ln}=e^{-1/2}\theta_D$ 的分歧判为 B 类"链内不可修"。第 88 轮已给曲率模 Debye DOS $g\propto\omega^2$——可从链内构造 $\alpha^2F$ 并推导对数矩。
- **文献调研**：$\lambda=2\int\alpha^2F/\omega\,d\omega$、$\alpha^2F\propto\omega^2$（Kiessling–Altshuler–Yuzbashyan 2025）；矩定义 $\omega_2^2=\frac{2}{\lambda}\int\alpha^2F\,\omega\,d\omega$、$\omega_{\log}=\exp[\frac{2}{\lambda}\int\frac{\alpha^2F}{\omega}\ln\omega\,d\omega]$（Pickett arXiv:2204.05930；Allen–Dynes PRB **12**, 905）——均作标准工具对照。
- **链内 $\alpha^2F$**：常耦合近似下 $\alpha^2F_{\rm chain}=A_{\rm eph}\omega^2\Theta(\omega_D-\omega)$——$\propto\omega^2$ 是链内模计数（非外借），幅度 $A_{\rm eph}$ 外生；$\lambda=A_{\rm eph}\omega_D^2$；对数矩 $\int_0^1 2x\ln x=-\tfrac12$ ⇒ $\omega_{\log}^{\rm chain}=e^{-1/2}\omega_D=\omega_{\ln}$（**Eliashberg 对数矩链内导出**）。
- **两矩分歧结构消解**：振幅支 $e^{-1/3}$＝$3y^2$ 电子态密度权重、相位支 $e^{-1/2}$＝$\alpha^2F/\omega$ 权重，比 $e^{1/6}$ 是权重差的精确结果——不是矛盾、不是链内不可修。
- **FE10 约定差消解**：$\omega_2^2=\tfrac12\omega_D^2$（$\alpha^2F/\omega$ 权重，Pickett/RMTA）vs $\langle\omega^2\rangle_{\rm ph}=\tfrac35\omega_D^2$（DOS 权重，FE10），比 $\tfrac56$——文献两约定的差＝权重差，都从链内同一谱给。
- **历史唯物主义合规**：曲率模谱（基础）决定 $\alpha^2F$ 形状与矩（读数）、幅度外生；必然性（$e^{-1/2}$、$\tfrac12$、$\tfrac35$）＋偶然性（$A_{\rm eph},\omega_D$ 材料值）分层统一；结构同构不是还原；未用社会范畴作物理证据。
- **诚实边界**：$A_{\rm eph}$ 归一与真实矩阵元频率结构外生、常耦合近似不覆盖强耦合/多带 ⇒ `审-15`／`审-17` **推进但不闭合**；绝对 $T_c$ 仍受命题 Z2＋$\mu^\ast$ 限制；状态栏、编号、账面、06／01／08、研究站均未动。
- **交付**：`03_推导工作台/环14A_链内alpha2F构造与两矩分歧的结构消解.md`、`05_Lean验证/SpectralMoments.lean`（7 定理，矩值由标准微积分给、数值脚本独立验证，`lake env lean` 退出码 0、无警告、无禁用项）、`04_计算验证/环14A_链内alpha2F与两矩消解.py`／`.png`／`.csv`／`_摘要.csv`（四面板八断言，矩积分 12 位精度，非拟合）、`06_决策记录/2026-11-24_第92轮_链内alpha2F与两矩消解.md`；同步主链 §11 `审-15`／§16 第 26／36／58 项、`成果登记.md` R-101、`缺口重审.md` 环 14 行、`00_当前有效口径表.md` §二已推形状表。
- **删除／防干扰**：删去"两矩分歧链内不可修"与"$\tfrac12$ 与 $\tfrac35$ 是矛盾约定"两读法；未删任何编号、状态或推导卡。

**第 93 轮补（环 6／17／19／`临-25` 后续：扩大项符号的热扫描判定；成果登记 R-102；2026-11-24）：**

- **触发**：`临-25` 原判"$\mathcal D_{new}$、$\dot M_t$ 无独立动力学、符号不可算、不可判定"。第 87/88 轮已给曲率模方差与 Debye 模计数、主链 §0.3 允许温度作扫描路径——可在**准静态热扫描**下定符号，不需外部动理学方程。
- **判定**：活跃对＝热占据曲率模 ⇒ $M_t\propto T^3$、$\omega_T=k_BT/\hbar$；高温单模方差 $k_BT/\omega^2$ Debye 加权 ⇒ $\mathcal D=3\hbar^2/k_BT\propto1/T$、$\mathcal D_{new}=\hbar^2/k_BT=\mathcal D/3<\mathcal D$（精确 $n_B$ 比值 0.351，稳健 $<1$）；扩大项 $=-\operatorname{sgn}(\dot T)\cdot 2\hbar^2\dot T/k_BT^2$——**加热负（平均化）、冷却正（差异化）**，给第 45 轮"差异化—扩大化"链内读数。
- **历史唯物主义合规**：曲率模谱（基础）决定扩大项符号（动力学读数），读数不反写模谱；必然性（比值 1/3、符号 $-\operatorname{sgn}(\dot T)$）＋偶然性（扫描方向、$T$ 范围、$\Theta_D$ 外生）分层统一；不引入 Boltzmann／Mori–Zwanzig；未用社会范畴作物理证据。
- **诚实边界**：$\dot M_t(t)$、$\mathcal D_{new}(t)$ 时间依赖外生、饱和区（$T\gtrsim\Theta_D$）符号结构失效、不声称危机相变已证明、绝对 $T_c$ 受命题 Z2 限制 ⇒ `临-25` **推进但不闭合**；状态栏、编号、账面、06／01／08、研究站均未动。
- **交付**：`03_推导工作台/环06_临25_扩大项符号的热扫描判定.md`、`05_Lean验证/ThreeTermSign.lean`（7 定理，`lake env lean` 退出码 0、无警告、无禁用项）、`04_计算验证/环06_临25_扩大项符号热扫描.py`／`.png`／`.csv`／`_摘要.csv`（四面板七断言，非拟合）、`06_决策记录/2026-11-24_第93轮_临25扩大项符号热扫描.md`；同步主链 §11 `临-25`／环 6 缺口行／§15 环 6 与 17／§16 第 28 项、`成果登记.md` R-102、`缺口重审.md` 环 6／17 行、`00_当前有效口径表.md` §二已推形状表。
- **删除／防干扰**：删去"扩大项符号完全不可算"与"新增分化度大于平均"两读法；未删任何编号、状态或推导卡。

**第 94 轮补（环 10／目标区／`审-14` 后续：双观测检验的 $\omega$ 对数矩口径修正；成果登记 R-103；2026-11-24）：**

- **触发（"发现不对劲就回头修正"）**：核查发现第 61 轮脚本把 CQM **振幅支**矩 $e^{-1/3}\theta_D$（$3y^2$ 权重）喂进 **Allen–Dynes 式**——该式的 $\omega_{\ln}$ 按定义是 $\alpha^2F/\nu$ 权重 $=e^{-1/2}\theta_D$（第 92 轮链内导出）。这是第 62 轮登记 `审-17` 边界被忽略的实例，两矩比 $e^{1/6}=1.181$（旧值高估约 18%）。
- **文献调研**：Allen–Dynes PRB **12**, 905 / Webb 2015 式 (3)（$\omega_{\ln}$ 定义）；Morel–Anderson PRB **125**, 1263 (1962)（$\mu^*=\mu/[1+\mu\ln(D/\omega_D)]$）；Bauer–Han–Gunnarsson arXiv:1202.5051（一阶 MA 是 uncontrolled approximation、二阶给更大 $\mu^*$，$\alpha\approx0.1$）；SCDFT cond-mat/0408685/86/88（无参数 $\mu$、Al $\mu^*=0.091$、Hg 0.07）。
- **修正与结果（诚实）**：用 $e^{-1/2}\theta_D$ 重算 13 元素双观测 $(T_c^{exp},\alpha^{exp})\to(\lambda,\mu^*)$——新口径与旧口径**均 13/13 可解、常规区间 $\mu^*\in[0.1,0.3]$ 均 8/13**，即口径修正是对第 61 轮结论的**稳健性检验，不是改进**；Hg $\alpha=0.50$ 端点给 $\mu^*=0$（文献 0.07 来自 $\alpha$ 端点四舍五入，不判失败）。
- **历史唯物主义合规**：模谱（基础）决定 $\omega_{\ln}$ 权重（读数），误喂振幅支矩是读数错位、不改基础；必然性（$\omega_{\ln}=e^{-1/2}\theta_D$ 链内固定）＋偶然性（$\mu,N(0),\epsilon_F$ 材料外生）分层统一；不虚构 $\mu$ 的第一性来源（链外-A：链内 $V<0$ 恒成立）。
- **诚实边界**：$\mu$ 仍链外-A、`审-14` **不闭合**；不声称 SCDFT 无参数算法已链内实现；强耦合/多带不适用；状态栏、编号、账面、06／01／08、研究站均未动。
- **交付**：`03_推导工作台/环10_审14_双观测检验的omega对数矩口径修正.md`、`05_Lean验证/OmegaLogCaliber.lean`（8 定理，退出码 0、无警告、无禁用项）、`04_计算验证/环10_审14_双观测omega口径修正.py`／`.png`／`.csv`／`_摘要.csv`（四面板四断言，非拟合）、`06_决策记录/2026-11-24_第94轮_双观测omega口径修正.md`；同步主链 §16 第 36 项、`成果登记.md` R-103、`00_当前有效口径表.md` §一边界注记；旧脚本 `环10_同位素中间值双观测.py` 加"口径已修正"注记（保留可追溯）。
- **删除／防干扰**：删去"可把振幅支矩 $e^{-1/3}\theta_D$ 代入 Allen–Dynes 式"读法；旧脚本保留作历史、不删除；未删任何编号、状态或推导卡。

**第 95 轮补（环 19／目标区／`审-11` 后续：相变热力学身份的 Ehrenfest 判定；成果登记 R-104；2026-11-24）：**

- **触发**：`审-11` 第 89 轮已给三扇区自由能与非解析性清单，但未做 Ehrenfest 分类（未答"$T_c=\min$ 处整体几级"）。文献给出强判据与严格定理。
- **文献调研**：Ehrenfest 判据（Gros §6.3、Likharev §4.2：第 n 阶＝前 n-1 阶导连续、第 n 阶跳变）；**arXiv:0808.3438 Theorem 2.3** 严格证 BCS 相变二级（$\Omega$ 为 $C^1$、$\partial_T^2\Omega$ 仅在 $T_c$ 跳变、$\Delta C/\gamma T_c=12/(7\zeta_3)=1.426$，与第 89 轮链内值一致）；**arXiv:1908.00729** 超薄膜实测 BKT 无限阶（本质奇点、比热无有限跳变、BCS-BKT crossover）；arXiv:1304.2275 式 22。
- **判定**：三扇区阶＝曲率全纯（无）／相位 3D Landau 二级、2D BKT 无限阶／振幅 $T^*$ 二级；**整体级数由 $T_c=\min$ 的 argmin 扇区决定**——$T_{BKT}$ 最小（2D 弱刚度）⇒无限阶、$T^*$ 或 $T_\theta$ 最小（3D）⇒二级。故 CQM 的 $T_c$ **不是固定级数**。"锚是非解析点"**条件于**相位先触底，否则只是上界（R-33 上界判定的热力学精确化）。可检验：ΔS=0（无潜热）、3D $\Delta C/\gamma T_c=1.426$、2D 无有限跳变。
- **历史唯物主义合规**：扇区自由能结构（基础）决定相变级数（宏观热力学读数），读数不反写扇区；必然性（argmin→级数映射固定）＋偶然性（哪个扇区先触底由材料 $\Upsilon_0,c_s,n,\lambda$ 定）分层统一；**量变质变只作【诠释】不作物理证据**；未用社会范畴作物理证据。
- **诚实边界**：材料归一、强耦合/多带比热跳变偏离 1.426、不证明 BKT 微观机制、绝对 $T_c$ 外生 ⇒ `审-11` **推进但不闭合**；状态栏、编号、账面、06／01／08、研究站均未动。
- **交付**：`03_推导工作台/环19_审11_相变热力学身份的Ehrenfest判定.md`、`05_Lean验证/EhrenfestClass.lean`（8 定理，退出码 0、无警告、无禁用项）、`04_计算验证/环19_审11_Ehrenfest相变级数.py`／`.png`／`.csv`／`_摘要.csv`（四面板七断言，非拟合）、`06_决策记录/2026-11-24_第95轮_Ehrenfest相变级数判定.md`；同步主链 §11 `审-11`／§15 环 19／§16 第 2 项、`成果登记.md` R-104、`缺口重审.md` 环 19 行、`00_当前有效口径表.md` §二已推形状表。
- **删除／防干扰**：删去"CQM 的 $T_c$ 是固定二级相变"与"锚必然是实际 $T_c$ 的非解析点"两读法；未删任何编号、状态或推导卡。

**第 96 轮补（数据验证／预注册 R7：比热跳变普适常数盲测；成果登记 R-105；2026-11-24）：**

- **触发**：用户反复强调"从头算到尾严格精确验证超导数据"。第 95 轮给出可检验预言 $\Delta C/\gamma T_c=12/(7\zeta_3)=1.426$（弱耦合），文献给独立实测比热跳变数据——做预注册盲测。
- **文献调研**：Johnston arXiv:1304.2275（弱耦合 1.426、Pb 2.7、强耦合上限 3.7、表）；IJPM 2026 表（Al/Cd/Sn/In/Ta/Nb/Pb/Hg 实测 $\Delta C/\gamma T_c$ 与 gap ratio）；WMI 讲义 Table 2（Al 1.4、Nb 1.9、Pb 2.7 量热实测）；Carbotte 通用强耦合修正（偏离随耦合单调增）。
- **预注册 R7（跑数前写死）**：P1 弱耦合子集（Al/Cd 按文献标注固定）偏差 ≤8%；P2 分类均值 weak<inter<strong 单调；P3 比热跳变与 gap ratio 同向（Pearson>0）。禁止拟合、禁止挑子集。
- **结果（三项全过，无拟合）**：P1 最大偏差 **4.6%**（Al 1.45、Cd 1.36 vs 1.426）；P2 均值 **1.41<1.64<2.34**；P3 Pearson **r=0.928>0**。8 元素独立实测，无一从 CQM 反解。强耦合 Pb 2.71/Hg 2.37 偏离为预注册允许（弱耦合限定，Carbotte 修正同向）。
- **历史唯物主义合规**：几何基础（曲率模谱→比热纯数）决定宏观热读数（比热跳变实测），无拟合；必然性（1.426 纯数、单调趋势）＋偶然性（材料耦合强度外生）分层统一；未用社会范畴作物理证据。
- **诚实边界**：不声称 CQM＝BCS——1.426 是链内纯数与实验吻合，同形不是还原（§0.2）；绝对 $T_c$ 仍外生（命题 Z2＋`审-14`）；强耦合定量修正需外部 Carbotte 函数；`审-11` **状态不变**。
- **交付**：`07_数据与现象/预注册判定_R7.md`（跑数前写死）、`04_计算验证/R7_比热跳变普适常数盲测.py`／`.png`／`_摘要.csv`、`05_Lean验证/R7HeatCapacityTest.lean`（8 条，退出码 0、无警告、无禁用项）、`06_决策记录/2026-11-24_第96轮_比热跳变普适常数盲测.md`；同步 `成果登记.md` R-105、`数据对照协议.md` §六。
- **删除／防干扰**：无删除——新增独立数据验证，未动任何编号、状态或推导卡；预注册固定子集、不挑参、不拟合。

**第 97 轮补（目标区／凝聚能普适比 $0.236$ 的链内推导与盲测；成果登记 R-106；2026-11-24）：**

- **触发**：第 89 轮凝聚能式 $E_{cond}=\tfrac12N(0)\Delta_0^2=B_c^2/2\mu_0$ 从未独立验证；文献（SSRN 2026 Eq.(41)）给 GL-BCS 普适比 0.236——恰是链内式＋C5＋Sommerfeld 消元可推出的纯数。
- **文献调研**：SSRN 2026（GL-BCS $E_{cond}/\gamma_0=0.236T_c^2$、Boson-Fermion $0.252T_c^{1.997}$、Kim 实验拟合 $0.2T_c^{2.06}$）；Arovas–Wu 讲义 §1.2（凝聚能 $-H_c^2/8\pi$、$H_c(0)=\sqrt{2\pi g}\Delta_0$）；Tinkham Ch.3；WMI 讲义 Table2（Al/Nb/Pb 实测 $B_c,\gamma,T_c$）。
- **链内纯数**（19F.7）：$\frac{E_{cond}}{\gamma_0T_c^2}=\frac{\tfrac12N\Delta_0^2}{\tfrac{2\pi^2}{3}k_B^2N T_c^2}=\frac{3}{4\pi^2}\frac{\Delta_0^2}{k_B^2T_c^2}=\frac{3}{4e^{2\gamma_E}}=0.236427$——$N(0)$、$\Delta_0$ 材料依赖完全消去，与 gap ratio $2\pi/e^\gamma$、比热跳变 $12/(7\zeta_3)$ 并列的**第三个链内无参数纯数**，与 SSRN GL-BCS 0.236 精确一致。临界场拉通 $B_c^2/2\mu_0=0.236\gamma_0T_c^2$。
- **预注册 R8 盲测（跑数前写死）**：P1 弱耦合 Al 偏差≤20%；P2 三元素偏差<25%、强耦合系统性增大预注册允许。**结果（无拟合）**：P1 Al 偏差 **15.5%**（实测普适比 0.2047 vs 0.236）、P2 最大 **21.1%**（Al→Nb→Pb 单调、强耦合方向）、$B_c$ 预言三点贴近 y=x。
- **历史唯物主义合规**：$T=0$ 凝聚能（量子基态＝基础）决定宏观临界场/Sommerfeld 比（读数），读数不反写基态；必然性（纯数 $3/(4e^{2\gamma_E})$）＋偶然性（$T_c,\gamma_0$ 材料外生）分层统一；结构同构不是还原；未用社会范畴作物理证据。
- **诚实边界**：不声称 CQM＝BCS（同形不是还原、§0.2）；强耦合定量偏差属链外修正（C5 弱耦合限定）；绝对 $T_c$ 外生（命题 Z2＋`审-14`）；不碰 `临-8`／`临-22`／RH；状态栏、编号、账面、06／01／08 均未动。
- **交付**：`03_推导工作台/环目标_凝聚能普适比0.236的链内推导与验证.md`、`07_数据与现象/预注册判定_R8.md`、`04_计算验证/R8_凝聚能普适比盲测.py`／`.png`／`_摘要.csv`、`05_Lean验证/CondensationEnergyRatio.lean`（7 定理，退出码 0、无警告、无禁用项）、`06_决策记录/2026-11-24_第97轮_凝聚能普适比0.236.md`；同步 `成果登记.md` R-106、`数据对照协议.md` §七。
- **删除／防干扰**：无删除——新增纯数推导＋独立验证，未动任何编号、状态或推导卡；预注册固定、不挑参、不拟合。

**第 98 轮补（目标区／`临-20` 刚度求和显式与 Uemura 常数族；成果登记 R-107；2026-11-24）：**

- **触发**：`临-20` 原判"$\Upsilon$ 刚度数值不可算"。M6 已给键局域 $J/J_0=(1-\rho)\cos(s\ell)$ 与饱和定理（键局域、非全对求和），Uemura 已给恒等式 $T_c=\frac{\pi}{2k_B}\Upsilon_{\rm bare}Q$——可接起来显式算 $\Upsilon_0$ 形状。
- **文献调研**：无序 XY 模型 PRB **99**, 104509（干净方格子 $\rho_s^0=J$、$J_d=J-JT/2d$）；Benfatto 讲义（$\rho_s=\frac{1}{2L^2}\sum(x_i-x_j)^2J_{ij}\cos$、$T_c=(\pi/2)J$ 裸、数值 0.8929J）；arXiv:1205.4737（长程相位耦合 $\rho_s^0=\frac{\pi}{2}(\lambda/a)^2J$）；Uemura PRL **62**, 2317。只作工具，不声称 CQM＝XY 模型。
- **推导**：键局域求和 $\Upsilon_0=\frac{1}{2L^2}\sum_{\langle ij\rangle}(x_i-x_j)^2J_{ij}|_{0}=2J_0(1-\rho_{nn})$（方格子几何因子 2，$J_0$ 外生 Z2）；接 Uemura 上界 $T_c\le\frac{\pi}{k_B}J_0(1-\rho_{nn})$——关联越强刚度与 $T_c$ 越小。竞争判据：FE10 $\eta\propto(1-\rho)$ 与刚度同向系数但分属配对/相位两扇区，由 $T_c=\min$ 竞争。干净 XY 核对 $g_{ren}=0.568<1$（不取普适 $\pi/2$，与第18轮一致）。
- **历史唯物主义合规**：亏角关联结构（几何基础）决定刚度与 $T_c$ 上界（宏观读数），读数不反写关联；必然性（形状/单调）＋偶然性（$J_0,\rho_{nn}$ 材料外生）分层统一；结构同构不是还原；未用社会范畴作物理证据。
- **诚实边界（主动放弃不推）**：Type I/II 判据需 $v_F$ 等外生电子结构，链内不能给绝对值——不强行推（避免"绕过"）；$\rho_{nn}$ 需 FG 侧独立测 ⇒ `临-20` **推进但不闭合**；状态栏、编号、账面、06／01／08 均未动。
- **交付**：`03_推导工作台/目标区_临20_刚度求和显式与Uemura常数族.md`、`05_Lean验证/StiffnessSum.lean`（7 定理，退出码 0、无警告、无禁用项）、`04_计算验证/环目标_临20_刚度求和形状.py`／`.png`／`_摘要.csv`（四面板八断言，非拟合）、`06_决策记录/2026-11-24_第98轮_刚度求和显式.md`；同步 `成果登记.md` R-107、主链 §16 第20项、`00_当前有效口径表.md` §二。
- **删除／防干扰**：无删除——新增形状推导，未动任何编号、状态或推导卡；Type I/II 强行推导因需外生 $v_F$ 被主动放弃。

**第 99 轮补（数据验证／BCS 四纯数族统一：链内凝聚能式复现 $R_3=2\sqrt\pi$；成果登记 R-108；2026-11-24）：**

- **触发**：文献 cond-mat/9905081 明确 BCS 三纯数 $R_1=2\Delta/k_BT_c=3.52$、$R_2=\Delta C/\gamma T_c=1.43$、$R_3=H_c(0)/[\sqrt{N(0)}\Delta(0)]=2\sqrt\pi$。链内已推 $R_1,R_2$ 与凝聚能比 $3/(4e^{2\gamma})$，但 $R_3$ 未核对。
- **文献调研**：cond-mat/9905081（三纯数 $R_1,R_2,R_3$）；Johnston arXiv:1304.2275（$R_1=2\pi/e^\gamma$、$R_2=12/7\zeta_3$、四纯数同出隙方程）；Arovas 讲义（凝聚能 $-H_c^2/8\pi$）；SSRN 2026（凝聚能比）。
- **第四纯数**：链内第 89 轮凝聚能式（SI $B_c^2/2\mu_0=\tfrac12N\Delta_0^2$ / Gaussian $H_c^2/8\pi=\tfrac12N\Delta_0^2$）直接给 $H_c=2\sqrt\pi\sqrt{N(0)}\Delta_0$，即 **$R_3=2\sqrt\pi=3.5449$ 与文献精确一致**——凝聚能式的独立确认（与第 97 轮凝聚能比盲测不同对象）。
- **四纯数族统一**：$R_1=2\pi/e^\gamma=3.528$（C5）、$R_2=12/(7\zeta_3)=1.426$（第 95 轮）、$R_3=2\sqrt\pi=3.545$（第 89 轮，本轮核）、$R_4=3/(4e^{2\gamma})=0.236$（第 97 轮）——同出 $\alpha_{\rm BCS}=\pi/e^\gamma$ 与 $\zeta(3)$，消去全部材料参数；$R_1/R_4=8\pi e^\gamma/3$ 代数恒等式（Lean 承载）。预注册 R9 全过、无拟合。
- **历史唯物主义合规**：四纯数（必然性，结构固定的无参数纯数）与材料耦合强度（偶然性，外生）分层统一；同形不是还原（§0.2），不声称 CQM＝BCS；未用社会范畴作物理证据。
- **诚实边界**：四纯数只在弱耦合单带同源极限成立（强耦合 Pb/Hg 偏离为预注册允许）；绝对 $T_c$ 仍外生（命题 Z2＋`审-14`）；不碰 `临-8`／`临-22`／RH；状态栏、编号、账面、06／01／08 均未动。
- **交付**：`07_数据与现象/预注册判定_R9.md`、`04_计算验证/R9_三纯数族统一检验.py`／`.png`／`_摘要.csv`、`05_Lean验证/UniversalRatios.lean`（纯代数恒等式，退出码 0、无警告、无禁用项）、`06_决策记录/2026-11-24_第99轮_四纯数族统一.md`；同步 `成果登记.md` R-108、`数据对照协议.md` §八。
- **删除／防干扰**：无删除——新增统一检验，未动任何编号、状态或推导卡；本地 mathlib 缺数值 pi 界引理，按 Lean(代数)/脚本(数值)分工处理，不用 axiom 补。

**第 100 轮补（数据验证／链内 $R_1$ 强耦合截距对照，B 类诚实标注；成果登记 R-109；2026-11-24）：**

- **触发**：用户要求"从头算到尾严格精确验证超导数据"。四纯数族已统一（第 99 轮），但强耦合材料 gap ratio 系统性高于 3.528——文献 Mitrović 通用曲线以 $R_1$ 为弱耦合截距。本轮以链内 $R_1$ 代入，用独立实测核对并诚实标注 B 类。
- **文献调研**：Mitrović 1984 / Webb 2015 Eq.6（强耦合 gap ratio 通用式，系数 12.5 为 Eliashberg 拟合）；SCDFT suppl. PRL 125 057001（独立 $T_c,\omega_{\log}$）；Kittel 元素表（$2\Delta$）；Semenok-Altshuler-Yuzbashyan 2025 表 S1+S5（$\omega_{\log},\theta_D$）。
- **核心 P1 通过**：外部 Mitrović 式 + 链内唯一输入 $R_1=2\pi/e^\gamma=3.528$（不拟合 12.5）。6 元素偏差 Al 5.6%/In 4.6%/Sn 6.9%/Ta 0.5%/Pb 1.1%/Nb 0.7% 全 <8% ⇒ 链内 $R_1$ 是强耦合曲线正确弱耦合截距。
- **P2 严格单调未通过（如实报告，不改判据）**：Ta→In→Sn 局部下降（弱耦合段实验散布 ±3% 主导），Spearman $r=0.771$ 仅作补充；"不欺骗"——如实登记失败，不放宽判据、不挑子集。
- **口径边界（防误用）**：$\omega_{\log}/\theta_D$ 实测散布 0.53–1.19（Nb 0.588/Hg 1.194/Nb$_3$Sn 0.526）⇒ 第92轮 $\omega_{\log}=e^{-1/2}\theta_D$ 只适合理想 Debye＋常耦合，不可套实验 $\theta_D$；旧 $e^{-1/3}$ 同被否定。Al 低于值 3.344 属偶然性外生，不否定纯数。
- **历史唯物主义合规**：链内 $R_1$（必然性，隙方程结构纯数）与材料耦合强度/声子谱细节（偶然性，外生）分层统一；基础决定弱耦合极限读数、偶然性造成散布、读数不反写结构；Mitrović 式是外部工具、同形不是还原（§0.2），不声称 CQM＝BCS Eliashberg；未用社会范畴作物理证据。
- **诚实边界**：B 类不升格第一性；12.5 不拟合不调；P2 失败如实保留；绝对 $T_c$ 外生；不碰 `临-8`／`临-22`／RH；状态栏、编号、账面、06／01／08／主链均未动。
- **交付**：`07_数据与现象/预注册判定_R10.md`、`04_计算验证/R10_强耦合截距检验.py`／`.png`／`_摘要.csv`、`05_Lean验证/StrongCouplingCaliber.lean`（4 定理，退出码 0、无警告、无禁用项）、`06_决策记录/2026-11-24_第100轮_强耦合截距检验.md`；同步 `成果登记.md` R-109、`数据对照协议.md` §九、`00_当前有效口径表.md` §二。
- **删除／防干扰**：无删除——新增 B 类数据检验，P2 不利结果如实保留（不删不利结果），修正的是对判据适用范围的理解而非篡改判据/数据。

**第 101 轮补（数据验证／从 C5 隙方程推完整普适 gap 曲线；成果登记 R-110；2026-11-24）：**

- **触发**：用户要求"从头算到尾严格精确验证超导数据"。四纯数族都是 $T=0$ 或 $T=T_c$ 的极限点，还缺把两端连起来的完整温度曲线 $\Delta(T)/\Delta_0$。
- **文献调研**：Blackford & March (Can. J. Phys. 46, 141, 1968)——21 个 Al 结 $3.53\pm0.02$；Townsend & Sutton (Phys. Rev. 128, 591, 1962)——Sn/Ta/Nb 完整 $\Delta(T)$ 曲线（**图数据、无表、不伪造点**）；Langmann & Triola (PRB 108, 104503, 2023)——精确普适函数 $\sqrt{f_1}\approx3.0633$；Gross (1980) 插值式 $a=2/3$。
- **核心成果（A 类）**：C5 隙方程稳定分解数值解全程曲线——$f(0)=1.764014$ vs $\pi/e^\gamma=1.763877$（误差 0.008%）、单调、$f(1)=0$。**近-$T_c$ 斜率由链内比热跳变导出**：C5 的 $T\to T_c$ 展开给 $\Delta^2=\frac{8\pi^2}{7\zeta_3}(k_BT_c)^2(1-t)$ ⇒ $\sqrt{f_1}=\pi\sqrt{8/(7\zeta_3)}=3.06326$；由比热跳变 $12/(7\zeta_3)$ 得 $\frac{8}{7\zeta_3}=\frac23\frac{\Delta C}{\gamma T_c}$ ⇒ **$\sqrt{f_1}=\pi\sqrt{\frac23\frac{\Delta C}{\gamma T^*}}$——Gross $a=2/3$ 由链内两纯数推出、非拟合参数**。数值斜率 3.06349（差 0.008%），与 Langmann–Triola 独立一致。Al $3.53\pm0.02$ 覆盖 $2f(0)=3.528$。
- **预注册 R11 全过**：五判据（截距/斜率/$a=2/3$/单调/Al 覆盖）全过、无拟合。Lean `UniversalGapCurve.lean`（6 条代数恒等式，退出码 0）。
- **回头修正**：初版面板 A 把渐近线画全程（低温渐近在 $t\to1$ 给 0.67、近-$T_c$ 渐近在 $t=0$ 给 1.737，误导），已改为只在有效区间画（低温 $t\leq0.3$、近-$T_c$ $t\geq0.7$）。删除两份临时测试脚本防干扰。
- **历史唯物主义合规**：隙方程结构（基础）决定普适曲线形状与两纯数关系（读数），读数不反写结构；必然性（纯数/$a=2/3$）＋偶然性（$\lambda,\omega_D$ 外生消去）分层统一；同形不是还原（§0.2），不声称 CQM＝BCS；未用社会范畴作物理证据。
- **诚实边界**：C5 条件具备（弱耦合 s 波单带）；强耦合/多带偏离不在范围；绝对 $T_c$ 外生；低温激活渐近只定性不拟合；不伪造 Townsend–Sutton 图数据；状态栏/编号/账面/06/01/08/主链均未动。
- **交付**：`07_数据与现象/预注册判定_R11.md`、`04_计算验证/R11_普适gap温度曲线.py`／`.png`／`_摘要.csv`／`_数据.csv`、`05_Lean验证/UniversalGapCurve.lean`、`06_决策记录/2026-11-24_第101轮_普适gap温度曲线.md`；同步 `成果登记.md` R-110、`数据对照协议.md` §十、`00_当前有效口径表.md` §二。

**第 102 轮补（数据验证／热力学临界场斜率第五纯数；成果登记 R-111；2026-11-24）：**

- **触发**：用户要求"从头算到尾严格精确验证超导数据"。四纯数＋完整 gap 曲线已立，还缺一个能直接检验纯数关系的热力学量——热力学临界场 $H_c(T)$。
- **文献调研**：Molinari BCS 讲义（$H_c$ 展开＋比热跳变 12/7ζ₃ 同页、近-$T_c$ 斜率 $e^\gamma$）；Arovas 讲义（Rutgers Eq.1.12、两流体 $\Delta C=H_c(0)^2/\pi T_c$、BCS 1.43）；Johnston arXiv:1304.2275（α-model、$H_c(0)/\sqrt{\gamma T_c^2}=\sqrt{6\pi}e^{-\gamma}$）；Phys. Rev. 138, A1428 (1965)（Al 临界场精密测量）；Mapother 1962（临界场—比热热力学一致性）。
- **核心成果（A 类严格热力学）**：链内第五无参数纯数 $\kappa=\frac{T_c}{H_c(0)}|dH_c/dT|_{T_c}=\frac{2\sqrt2 e^\gamma}{\sqrt{7\zeta_3}}=1.73666$——由链内 gap ratio（$e^\gamma$）＋比热跳变（$12/7\zeta_3$）＋Rutgers 公式严格组合。**两流体抛物线给 $\kappa=2$，链内低 13.2%**；Al 精密临界场实验（$dH_c/dT=158\pm4$ Oe/K、$H_0=104.8\pm0.6$ Oe、$T_c=1.175$ K）算 $\kappa_{\rm Al}=1.771\pm0.046$，距链内 2.0%、距两流体 12.9%——**链内比两流体近似更接近实验**（非拟合）。Taylor $\beta=1.1317$、Molinari 低温系数 $e^{2\gamma}/3=1.057$、Johnston $H_c(0)/\sqrt{\gamma T_c^2}=2.438$ 同源。
- **预注册 R12 五判据全过**：$\kappa$ 恒等式、两流体被否、Al 对照、低温系数、Johnston 比——无拟合。Lean `CriticalFieldSlope.lean`（6 条：$\kappa^2=8e^{2\gamma}/(7\zeta_3)$、$\kappa^2<4$ 等，退出码 0）。
- **诚实注记**：四阶 Taylor 偏差函数 $D_{\min}=-0.0329@t=0.71$ vs BCS 精确约 $-0.037@t\approx0.5$（截断局限，负号量级对，不掩盖）。
- **历史唯物主义合规**：隙方程/凝聚能/比热结构（基础）决定 $H_c$ 斜率纯数（读数），读数不反写结构；必然性（$\kappa$ 由两纯数＋热力学固定）＋偶然性（材料 $H_0,T_c$ 外生）分层统一；同形不是还原（§0.2），不声称 CQM＝BCS；未用社会范畴。
- **诚实边界**：A 类但弱耦合单带条件具备；强耦合 Pb/Hg 比热跳变 2.7/2.37≫1.43、$\kappa$ 偏离预注册允许；绝对 $T_c$ 外生；不碰 `临-8`／`临-22`／RH；状态栏/编号/账面/06/01/08/主链均未动。
- **交付**：`07_数据与现象/预注册判定_R12.md`、`04_计算验证/R12_临界场斜率纯数.py`／`.png`／`_摘要.csv`、`05_Lean验证/CriticalFieldSlope.lean`、`06_决策记录/2026-11-24_第102轮_临界场斜率纯数.md`；同步 `成果登记.md` R-111、`数据对照协议.md` §十一、`00_当前有效口径表.md` §二。

**第 103 轮补（数据验证／比热全程曲线五纯数一致性网络；成果登记 R-112；2026-11-24）：**

- **触发**：用户要求"从头算到尾严格精确验证超导数据"。已确立五纯数（第 87–102 轮），本轮检验它们是否构成内部自洽网络，并从链内 gap 曲线推比热全程曲线做外部逐点盲测。
- **文献调研**：Johnston arXiv:1304.2275（Eq.20b 比热积分、Eq.24 低温渐近、Table IV 数值表）；Padamsee α-model；Zavaritskii JETP 34, 1116 (1958)（Al/Zn 比热指数）；Bryant Phys. Rev. 123, 491 (1961)（In/Sn 低温比热）。
- **核心成果 (A) 五纯数一致性网络**：$R_4\cdot2\kappa^2=R_2$，即 $\frac{3e^{-2\gamma}}{4}\cdot\frac{16e^{2\gamma}}{7\zeta_3}=\frac{12}{7\zeta_3}$，$e^{2\gamma}$ 精确消去（误差 $1.6\times10^{-16}$）。链内五纯数由**两生成元 $e^\gamma,\zeta_3$** 生成——2 生成元普适类，从未登记的内部结构。
- **核心成果 (B) 比热全程盲测**：链内 gap 曲线（R11）＋Johnston Eq.(20b) 积分算 $C_{es}(t)/\gamma T_c$，对独立 Table IV（BCS）$t=0.12$–$0.30$ 十点逐点盲测**最大误差 0.10%**（<2%）；低温激活指数（扣 $(\alpha/t)^{3/2}$ 幂律后）$-1.767$ vs $-\pi/e^\gamma=-1.764$（差 0.2%）。
- **预注册 R13 五判据全过**：五纯数恒等式、逐点盲测、跳变 2.426、激活指数、前因子——无拟合。Lean `FiveRatioNetwork.lean`（6 条：$R_4\cdot2\kappa^2=R_2$、$R_3^2=4\pi$ 等，退出码 0）。
- **回头修正**：初版低温拟合漏 $(\alpha/t)^{3/2}$ 幂律前因子得表观 -1.548（差 12%）、面板 C 箭头不渲染——均已诚实修正（修正后 -1.767，差 0.2%）。删临时测试脚本 `_test_specificheat.py`。
- **历史唯物主义合规**：隙方程/纯数结构（基础）决定比热曲线形状与五纯数关系（读数），读数不反写结构；必然性（网络/$e^{2\gamma}$ 消去/激活指数）＋偶然性（材料归一外生）分层统一；同形不是还原（§0.2），不声称 CQM＝BCS；未用社会范畴。
- **诚实边界**：B 类积分工具（不声称 CQM 推出 BCS 热力学）；强耦合 Pb/Hg 偏离；绝对 $T_c$ 外生；不碰 `临-8`／`临-22`／RH；状态栏/编号/账面/06/01/08/主链均未动。
- **交付**：`07_数据与现象/预注册判定_R13.md`、`04_计算验证/R13_比热曲线五纯数网络.py`／`.png`／`_摘要.csv`／`_盲测.csv`、`05_Lean验证/FiveRatioNetwork.lean`、`06_决策记录/2026-11-24_第103轮_比热曲线五纯数网络.md`；同步 `成果登记.md` R-112、`数据对照协议.md` §十二、`00_当前有效口径表.md` §二。

**第 104 轮补（数据验证／熵积分闭环；成果登记 R-113；2026-11-24）：**

- **触发**：用户要求"从头算到尾严格精确验证超导数据"。热力学链已通 gap 曲线→比热→临界场斜率，还缺最后一步：从 gap 经熵积分回到 T=0 凝聚能——Johnston Eq.(31)，若成立则整条链首尾闭合。
- **文献调研**：Johnston arXiv:1304.2275（Eq.20a 熵、Eq.30 $H_c(0)/\sqrt{\gamma T_c^2}=\sqrt{6\pi}e^{-\gamma}$、Eq.31 熵积分、Table III 熵表）；Chakravarty cond-mat/0211613（凝聚能 $=\int_0^{T_c}(S_n-S_s)dT$）；MIT/Aalto/UCSD 讲义（无潜热、熵差与临界场关系）。
- **核心成果（A 类结构闭合＋B 类工具）**：链内 gap 曲线＋Eq.(20a) 算熵，$\int_0^1[t-S_{es}/\gamma T_c]dt=0.236446$ vs 链内凝聚能纯数 $R_4=3/4e^{2\gamma}=0.236428$（差 **0.008%**）——整条热力学链 T=0 gap→比热/临界场→熵→凝聚能→回 T=0 **首尾闭合**。熵曲线对 Johnston Table III 全温区 21 点盲测最大误差 **0.13%**；$\Delta S(T_c)=0$（无潜热）、$S_{es}(0.02)=6.2\times10^{-38}$（低温指数）。
- **预注册 R14 五判据全过**：熵盲测、积分闭合、$H_c(0)$ 归一、$\Delta S(T_c)=0$、低温指数——无拟合。Lean `EntropyClosure.lean`（5 条：$R_4=H_c(0)^2/(8\pi\gamma T_c^2)$ 等，退出码 0）。
- **回头修正**：临时脚本 Table III 参考值手抄错误（webfetch 核对后全吻合）、numpy 2.x `trapz`→`trapezoid`——均诚实修正；删临时脚本。
- **历史唯物主义合规**：隙方程结构（基础）决定熵曲线与凝聚能闭合（读数），读数不反写结构；必然性（闭合/$R_4$/$\Delta S=0$）＋偶然性（材料外生）分层统一；同形不是还原（§0.2），不声称 CQM＝BCS；未用社会范畴。
- **诚实边界**：熵积分工具是 B 类外部 BCS 热力学，链内贡献是 gap 曲线＋$\alpha_{BCS}$＋凝聚能纯数（闭环是链内两独立路径一致性检验）；强耦合偏离、绝对 $T_c$ 外生；不碰 `临-8`／`临-22`／RH；状态栏/编号/账面/06/01/08/主链均未动。
- **交付**：`07_数据与现象/预注册判定_R14.md`、`04_计算验证/R14_熵积分闭环.py`／`.png`／`_摘要.csv`／`_盲测.csv`、`05_Lean验证/EntropyClosure.lean`、`06_决策记录/2026-11-24_第104轮_熵积分闭环.md`；同步 `成果登记.md` R-113、`数据对照协议.md` §十三、`00_当前有效口径表.md` §二。

**第 105 轮补（数据验证／超流密度与穿透深度全程，接 Uemura 标度；成果登记 R-114；2026-11-24）：**

- **触发**：用户要求"从头算到尾严格精确验证超导数据"。热力学链已闭合（R14），但独立可观测量——超流密度 $\rho_s(t)$ 与 London 穿透深度 $\lambda(t)$——未验。关键：Johnston Eq.(42a) 把它们唯一联系到 gap 温度导数，完全由链内 gap 曲线决定、无材料参数，把第 98 轮 Uemura T=0 刚度推广到全程。
- **文献调研**：Johnston arXiv:1304.2275（Eq.39/40/42/44、Table VI London 参数表）；Prozorov & Giannetta（μSR 超流密度 $\rho_s=[\lambda(0)/\lambda(T)]^2$）；Chandrasekhar-Einzell（半经典超流密度）；Rutgers 关系。
- **核心成果（A 类结构＋B 类工具）**：链内 gap 曲线经 Eq.(42a) 唯一决定全程形状——对 Table VI（BCS）全温区盲测 $I(t)$ 中温 **0.06%**/低温 **0.22%**、$\lambda$ **0.22%**。**两路径一致性闭环**：gap 导数 vs sech² 积分差 **0.018%**。**新纯数**近 $T_c$ 超流密度斜率 $\rho_s'(1)=-2$（数值 2.00043，与 $\kappa$ 同出 $d\tilde\Delta^2/dt|_1=-8e^{2\gamma}/7\zeta_3$）；低温激活指数 -1.7681 vs $-\pi/e^\gamma=-1.7639$。
- **预注册 R15 五判据全过**：I(t) 盲测、两路径一致、斜率 -2、低温激活、$\lambda$ 盲测——无拟合。Lean `SuperfluidDensity.lean`（6 条，退出码 0）。
- **历史唯物主义合规**：隙方程结构（基础）决定超流密度/穿透深度形状（读数），读数不反写结构；必然性（形状唯一/-2/两路径一致）＋偶然性（$\lambda(0)$、Uemura T=0 外生）分层统一；同形不是还原（§0.2），不声称 CQM＝BCS；未用社会范畴。
- **诚实边界**：电动力学工具（Eq.40/42/44）是 B 类外部 BCS 关系；洁净 London 极限假设，强耦合/各向异性/杂质偏离；**Al 是 Pippard 极限（London 曲线对 Al 只定性）**；绝对 $T_c$、$\lambda(0)$ 外生；不碰 `临-8`／`临-22`／RH；状态栏/编号/账面/06/01/08/主链均未动。
- **交付**：`07_数据与现象/预注册判定_R15.md`、`04_计算验证/R15_超流密度穿透深度全程.py`／`.png`／`_摘要.csv`／`_盲测.csv`、`05_Lean验证/SuperfluidDensity.lean`、`06_决策记录/2026-11-24_第105轮_超流密度穿透深度全程.md`；同步 `成果登记.md` R-114、`数据对照协议.md` §十四、`00_当前有效口径表.md` §二。删临时脚本 `_test_superfluid.py`。

**第 106 轮补（数据验证／临界场全程＋五表统一全景；成果登记 R-115；2026-11-24）：**

- **触发**：用户要求"从头算到尾严格精确验证超导数据"。R12 只做临界场斜率，全程未验；已验证的五观测量分散多轮。本轮补齐 $H_c(T)$ 全程盲测并整合成"五表统一全景"收官。
- **文献调研**：Johnston arXiv:1304.2275（Eq.20a/31、Table II–VI）；Saini IJPM 2026（偏差函数 BCS 最小值 -0.037）；Mühlschlegel Z. Phys. 155, 313 (1959)（原始 BCS 数值表）。
- **核心成果（A 类贯通＋B 类工具）**：链内 gap 经熵积分 Eq.(31) 算 $H_c(t)/H_c(0)$，对 Johnston Table V 全温区 **49 点盲测最大误差 0.014%**；分母 $=\int_0^1[t'-S_{es}]dt'=R_4=3/4e^{2\gamma}$（差 $7.8\times10^{-5}$）；近 $T_c$ 斜率 1.7363 vs $\kappa=1.73666$（差 0.02%）；偏差函数全程负、$D_{min}=-0.037@t=0.69$（修正 R12 四阶 Taylor 的 -0.0329 截断局限）。**五表统一全景（收官）**：Table II(gap)/III(熵)/IV(比热)/V(临界场)/VI(穿透深度) 全由单一链内 gap 曲线生成，各表盲测误差均 <0.23%——从头算到尾最强证据。
- **预注册 R16 五判据全过**：$H_c$ 盲测、分母=R4、斜率 κ、偏差负、五表统一——无拟合。Lean `CriticalFieldCurve.lean`（5 条，退出码 0）。
- **历史唯物主义合规**：隙方程结构（基础）决定全部热力学/电动力学曲线（读数），读数不反写结构；必然性（五表贯通/$H_c$全程/$\kappa$）＋偶然性（材料归一外生）分层统一；同形不是还原（§0.2），不声称 CQM＝BCS；未用社会范畴。
- **诚实边界**：热力学工具 B 类；Table II–VI 是理论数值表（非直接实验，实验对照见 R7/R10/R12）；强耦合/多带偏离；绝对 $T_c$ 外生；不碰 `临-8`／`临-22`／RH；状态栏/编号/账面/06/01/08/主链均未动。
- **交付**：`07_数据与现象/预注册判定_R16.md`、`04_计算验证/R16_临界场全程与五表全景.py`／`.png`／`_摘要.csv`／`_盲测.csv`、`05_Lean验证/CriticalFieldCurve.lean`、`06_决策记录/2026-11-24_第106轮_临界场全程与五表全景.md`；同步 `成果登记.md` R-115、`数据对照协议.md` §十五、`00_当前有效口径表.md` §二。删临时脚本 `_test_Hc.py`。

**第 107 轮补（数据验证／准粒子态密度与 Giaever 隧穿谱；成果登记 R-116；2026-11-24）：**

- **触发**：用户要求"从头算到尾严格精确验证超导数据"。前 16 轮为热力学/电动力学整体量，本轮补**能量分辨谱学**——历史上首次直接"看见"能隙的 Giaever 隧穿（1960）。
- **文献调研**：Giaever PRL 5, 64 (1960)/PR 126, 941 (1962)/Nobel 1973（态密度直接测量、Pb 声子 wiggles）；Bardeen Nobel 1972（$N_s/N_n=E/\sqrt{E^2-\Delta^2}$）；Caltech 联子谱学讲义（Giaever 公式）；Mattis-Bardeen PR 111, 412 (1958)。
- **核心成果（A 类结构＋B 类工具）**：Bogoliubov 粒子守恒给 $N_s/N_n=E/\sqrt{E^2-\Delta_0^2}$，代入链内 $\Delta_0=\pi e^{-\gamma}k_BT_c$（C5）。两个严格检验全过：**gap edge 平方根发散系数 $\sqrt{\Delta_0/2}$**（误差 <0.001%）；**态守恒 sum rule** $\int_0^X(N_s/N_n-1)dE=\sqrt{X^2-\Delta_0^2}-X$（差 $2\times10^{-12}$，$X\to\infty$ 趋 0——被隙驱逐态=相干峰吸收态）。Giaever $dI/dV\propto N_s(eV)$、gap edge $eV=\Delta_0$、$2\Delta/k_BT_c=3.527754$。
- **预注册 R17 五判据全过**：DOS 谱形、edge 系数、sum rule、有限和、隧穿 gap edge——无拟合。Lean `TunnelingDOS.lean`（5 条，退出码 0、无警告）。
- **历史唯物主义合规**：隙方程结构（基础）决定 gap 与态密度谱形（读数），读数不反写结构；必然性（edge 系数/sum rule/gap ratio）＋偶然性（材料 gap 外生）分层统一；同形不是还原（§0.2），不声称 CQM＝BCS；未用社会范畴。
- **诚实边界**：DOS/隧穿公式是 B 类外部谱学工具，链内贡献是 gap＋守恒律结构；**强耦合 Pb/Hg 声子 wiggles 偏离纯 BCS DOS**、实验展宽使 edge 不如理论尖锐；绝对 $T_c$ 外生；不碰 `临-8`／`临-22`／RH；状态栏/编号/账面/06/01/08/主链均未动。
- **交付**：`07_数据与现象/预注册判定_R17.md`、`04_计算验证/R17_准粒子态密度与隧穿谱.py`／`.png`／`_摘要.csv`、`05_Lean验证/TunnelingDOS.lean`、`06_决策记录/2026-11-24_第107轮_准粒子态密度与隧穿谱.md`；同步 `成果登记.md` R-116、`数据对照协议.md` §十六、`00_当前有效口径表.md` §二。

**第 108 轮补（数据验证／Mattis-Bardeen 光学电导与 FGT sum rule；成果登记 R-117；2026-11-24）：**

- **触发**：用户要求"从头算到尾严格精确验证超导数据"。前 17 轮贯通热力学/电动力学/隧穿谱学，本轮补第四个独立维度——光学/太赫兹响应（Mattis-Bardeen 1958），其光学阈值 $2\Delta_0$ 是链内 gap 的直接后果，FGT sum rule 把缺失谱重与已验证超流密度连接成闭环。
- **文献调研**：Mattis-Bardeen PR 111, 412 (1958)；FGT sum rule（PRB 108, 104501 2023 高精度验证）；arXiv cond-mat/0408054（MB Eq.61/63 闭式）；Al 准粒子响应（arXiv:0712.3391）；无序 NbN sub-gap 吸收文献。
- **核心成果（A 类结构＋B 类工具）**：MB $T=0$ 闭式解代入链内 $\Delta_0=\pi e^{-\gamma}k_BT_c$：光学阈值 $\hbar\omega_g=2\Delta_0$（$2\Delta/k_BT_c=3.5278$ 纯数）、$\omega<2\Delta_0$ 硬隙严格 0、高 $\omega$ 趋 1（0.99968）。**FGT 闭环**：光学缺失谱重＝超流密度（R15），累积趋平台 8.4646；光学 gap 尺度与隧穿（R17）一致；$\omega\sigma_{2s}\to\pi\Delta_0$（Tinkham 标准 3.141593）。
- **预注册 R18 五判据全过**：阈值、硬隙、曲线、FGT 守恒、$\sigma_2$ 极限——无拟合。Lean `OpticalConductivity.lean`（4 条，退出码 0、无警告）。
- **回头修正**：初版误把 $k'=\sqrt{1-k^2}$ 写为常数 1 得假象 $e^\gamma\Delta$，按 Eq.63 修正为 $\pi\Delta$——记入预注册防干扰。
- **历史唯物主义合规**：隙方程结构（基础）决定 gap 与光学阈值/谱形（读数），读数不反写结构；必然性（阈值/FGT/$\pi$ 系数）＋偶然性（$\lambda(0)$ 外生）分层统一；同形不是还原（§0.2），不声称 CQM＝BCS；未用社会范畴。
- **诚实边界**：MB/FGT 是 B 类外部电动力学工具，链内贡献是 gap＋超流密度＋α²F 构造；强耦合 Pb/Hg、无序 NbN sub-gap 吸收偏离纯 MB；绝对 $T_c$ 外生；不碰 `临-8`／`临-22`／RH；状态栏/编号/账面/06/01/08/主链均未动。
- **交付**：`07_数据与现象/预注册判定_R18.md`、`04_计算验证/R18_MattisBardeen光学电导.py`／`.png`／`_摘要.csv`、`05_Lean验证/OpticalConductivity.lean`、`06_决策记录/2026-11-24_第108轮_MattisBardeen光学电导.md`；同步 `成果登记.md` R-117、`数据对照协议.md` §十七、`00_当前有效口径表.md` §二。

**第 109 轮补（数据验证／同位素效应 $\alpha=1/2$ 上界；成果登记 R-118；2026-11-24）：**

- **触发**：用户继续授权但未指定方向。四个验证维度已贯通，本轮选最后一个经典 BCS 验证——同位素效应（电子-声子机制身份的核心证据），链内第88轮 $\Theta_D$ 构造与声速质量依赖有几何来源，可第一性推 $\alpha=1/2$。
- **文献调研**：Webb/Marsiglio/Hirsch Physica C 514, 17 (2015) Table 3（元素 α 表，本项目 R10 已用）；Illinois 讲义（McMillan 修正式、"α>1/2 未发现"、λ M-独立论证）；Fröhlich 1950；Garland 1963；Cd 同位素 PRB 2, 4442。
- **核心成果（A 类机制身份＋B 类工具）**：谐振子声速 $c_s=\sqrt{k/\rho}\propto M^{-1/2}$（几何）⇒ $\Theta_D\propto M^{-1/2}$；C5 $T_c=\frac{2e^\gamma}{\pi}\Theta_D e^{-1/\lambda}$（λ M-独立）⇒ $\alpha=-d\ln T_c/d\ln M=1/2$。**上界可证伪**：McMillan 修正 $\le1/2$（扫描全 ≤0.5）、Webb 实验元素全部 ≤0.5 无一违反；弱耦合非过渡金属平均 0.488、过渡金属 0.192（外生 $\mu^*$）。
- **预注册 R19 五判据全过**：链内 α、上界、弱耦合、过渡金属、McMillan 扫描——无拟合。Lean `IsotopeExponent.lean`（5 条，退出码 0、无警告）。
- **历史唯物主义合规**：几何声速结构（基础）决定 $\Theta_D$ 质量依赖与 $\alpha=1/2$ 上界（读数），读数不反写结构；必然性（上界）＋偶然性（$\mu^*$ 外生）分层统一；同形不是还原（§0.2），不声称 CQM＝BCS；未用社会范畴。
- **诚实边界**：McMillan 修正 B 类工具、$\mu^*$ 外生；**反常同位素（U -2、PdH -0.25）链外只登记不解释**（不虚构非声子机制）；绝对 $T_c$ 外生；不碰 `临-8`／`临-22`／RH；状态栏/编号/账面/06/01/08/主链均未动。
- **交付**：`07_数据与现象/预注册判定_R19.md`、`04_计算验证/R19_同位素效应上界.py`／`.png`／`_摘要.csv`、`05_Lean验证/IsotopeExponent.lean`、`06_决策记录/2026-11-24_第109轮_同位素效应上界.md`；同步 `成果登记.md` R-118、`数据对照协议.md` §十八、`00_当前有效口径表.md` §二。

**第 110 轮补（数据验证／约瑟夫森临界电流与 AB 纯数；成果登记 R-119；2026-11-24）：**

- **触发**：用户继续授权。超导三大现象（零电阻、迈斯纳、约瑟夫森）前两者已覆盖，约瑟夫森（宏观量子相位相干）未触及——链内有明确载体（环19 相位扇区、环13 U(1) 破缺、gap、Uemura 刚度）。
- **文献调研**：Ambegaokar-Baratoff PRL 10, 486 (1963)＋勘误 PRL 11, 104；Josephson PRL；arXiv:0908.1761（AB 微观推导 Eq.3.31/3.33）；Fiske RMP 36, 221。
- **核心成果（A 类结构＋B 类工具）**：AB $T=0$ 对称结 $I_cR_n=\pi\Delta_0/(2e)$，代入链内 $\Delta_0=\pi e^{-\gamma}k_BT_c$ 得**第 6 纯数** $eI_cR_n/k_BT_c=\pi^2/(2e^\gamma)=2.77069$；$E_J=\hbar I_c/2e=\Phi_0I_c/2\pi$ 与相位刚度同扇区。AB 温度曲线用链内 gap 全程单调 1→0、近 $T_c$ 斜率 2.65≈勘误 2.67（交叉确认）。
- **预注册 R20 五判据全过**：AB 纯数、$I_cR_n$、Josephson 能、温度曲线、近 $T_c$ 线性——无拟合。Lean `JosephsonAB.lean`（4 条，退出码 0、无警告）。
- **回头修正**：初版 $I_c$ 归一化误含多余 $\tanh(\Delta_0/2k_BT_c)$ 分母致 $>1$ 非物理值，已修正并记入决策记录。
- **历史唯物主义合规**：相位扇区结构（基础）决定约瑟夫森响应（读数），读数不反写结构；必然性（$\pi^2/2e^\gamma$）＋偶然性（$R_n$ 外生）分层统一；同形不是还原（§0.2），不声称 CQM＝BCS；未用社会范畴。
- **诚实边界**：AB/Josephson B 类工具、隧道极限；高透明 SNS/Andreev/二极管链外只登记；强耦合 Pb 偏离允许；绝对 $T_c$ 外生；不碰 `临-8`／`临-22`／RH；状态栏/编号/账面/06/01/08/主链均未动。
- **交付**：`07_数据与现象/预注册判定_R20.md`、`04_计算验证/R20_约瑟夫森AB纯数.py`／`.png`／`_摘要.csv`、`05_Lean验证/JosephsonAB.lean`、`06_决策记录/2026-11-24_第110轮_约瑟夫森AB纯数.md`；同步 `成果登记.md` R-119、`数据对照协议.md` §十九、`00_当前有效口径表.md` §二。

**第 111 轮补（数据验证／交流约瑟夫森计量闭环；成果登记 R-120；2026-11-24）：**

- **触发**：用户继续授权。R20 做了 DC 约瑟夫森，本轮补 AC 面（相位动力学 $d\phi/dt=2eV/\hbar$、Shapiro 台阶、$K_J=2e/h$）。关键闭环：$K_J=1/\Phi_0$——约瑟夫森常数恰是 R14/临19 链内磁通量子的倒数，$2e$ 同源（12.A）。
- **文献调研**：NIST 量子计量三角；CODATA 2018（$K_J$ 精确）；Poirier C. R. Physique 20, 92 (2019)（AC 约瑟夫森、Shapiro、$K_J^{-1}=\Phi_0$）；Deaver-Fairbank/Doll-Näbauer 1961；Nature Phys 2007（$h/e$ 争议，链外）。
- **核心成果（A 类闭环＋B 类工具）**：链内 $\Phi_0=h/2e$ ⇒ $K_J=2e/h=1/\Phi_0$，$K_J\cdot\Phi_0=1$（严格倒数闭环）。2019 SI 精确 $h,e$ ⇒ $K_J=483597.848417$ GHz/V 对 CODATA 差 $7.8\times10^{-16}$、$\Phi_0=2.067833848\times10^{-15}$ Wb 差 $2.2\times10^{-10}$；$f=K_JV$ 线性、Shapiro $V_1=20.678\ \mu$V（$f=10$ GHz）；$q=e$ 分支链排除。
- **预注册 R21 五判据全过**：倒数闭环、KJ/Φ0 对 CODATA、AC 线性、Shapiro、分支判别——无拟合。Lean `ACJosephson.lean`（2 条，退出码 0、无警告）。
- **历史唯物主义合规**：配对电荷结构（基础）决定 $\Phi_0$ 与 $K_J$ 倒数关系（读数），读数不反写结构；必然性（闭环/$q=2e$）＋偶然性（SI $h,e$ 定义外生）分层统一；同形不是还原（§0.2），不声称 CQM＝BCS；未用社会范畴。
- **诚实边界**：AC/Shapiro B 类工具、$h,e$ SI 定义外生；$h/e$ 周期争议链外只登记；绝对 $T_c$ 外生；不碰 `临-8`／`临-22`／RH；状态栏/编号/账面/06/01/08/主链均未动。
- **交付**：`07_数据与现象/预注册判定_R21.md`、`04_计算验证/R21_交流约瑟夫森计量闭环.py`／`.png`／`_摘要.csv`、`05_Lean验证/ACJosephson.lean`、`06_决策记录/2026-11-24_第111轮_交流约瑟夫森计量闭环.md`；同步 `成果登记.md` R-120、`数据对照协议.md` §二十、`00_当前有效口径表.md` §二。

**第 112 轮补（缺口重审／链外-B 载体辨析；成果登记 R-121；2026-11-24）：**

- **触发**：用户判断"不存在链外，按理来说理论内部就应该能解决"。本轮核实该判断，把六条链外逐条落到"载体／映射／物性"三层。
- **核查结论**："链外"是误名——§12 原判是"链无载体"，不是"原则上不可推"。六条链外无一属于"原则上链外"，全是**映射未建**。第一性理论的完整性 = 无拟合参数，不是无物质输入（arXiv:2407.14670）。
- **核心发现（A 类结构判定）**：相位扇区裸刚度 $\Upsilon(T)=\Upsilon_0w(T)$（(10B.5)，$w=1-\frac{\pi^2}{3}(T/\omega_D)^2$）是**纯相位涨落型 $T^2$**，取 $\omega_D=300$ K、$T_c=10$ K 得 $w(T_c)=0.9963$（几乎不降）；振幅扇区（C5 gap）准粒子耗竭给 $\rho_s\to0$ 于 $T_c$。故 $\Upsilon(T)\ne\rho_s(T)$ ⇒ **链外-B 的载体在振幅扇区 gap，不在相位扇区**；§12"链外-B 链无载体"在振幅扇区意义上不成立。
- **文献**：arXiv:2101.06697（$n_s$ 与 $\rho_s$ 同一量，$T_c$ 处准粒子耗竭归零）；arXiv:cond-mat/0008100（纯相位涨落给 $T^2$，但不可忽略准粒子）；PRB 109, 144501 (2023)（干净 BCS 的 $\rho_s$ 低温指数）。
- **预注册 R22 四判据全过**：$w(T_c)>0.99$、$\rho_s(T_c)<0.02$、$1-w$ 斜率 2、$\lambda_L$ 由 $\rho_s$ 决定——无拟合。Lean `LinkExternalB.lean`（5 条，退出码 0、无警告）。
- **历史唯物主义合规**：结构定读数（振幅／相位结构决定可观测 $\lambda_L$，读数不反写结构）；必然性（$T^2$/指数两机制）＋偶然性（$\omega_D,T_c$ 外生）分层统一；同形不是还原，不声称 CQM＝BCS；未用社会范畴。
- **诚实边界**：$\text{gap}\to\rho_s$ 两流体仍是 B 类；半接（载体链内／映射外部／绝对值物性）；Type I/II、$\xi$、$H_{c2}$ 仍缺；$w(T)$ 的 $T^2$ 不当实验 $\lambda(T)$ 直接对照；绝对 $T_c$ 外生；不碰 `临-8`／`临-22`／RH。
- **交付**：`02_缺口重审/链外重审_六个接口的链内接法.md`、`07_数据与现象/预注册判定_R22.md`、`04_计算验证/R22_链外B载体辨析.py`／`.png`／`_摘要.csv`、`05_Lean验证/LinkExternalB.lean`、`06_决策记录/2026-11-24_第112轮_链外重审与B载体辨析.md`；同步 `成果登记.md` R-121、`数据对照协议.md` §二十一、`00_当前有效口径表.md`。

**第 113 轮（链外-E 函数形式；成果登记 R-122；2026-11-24）：**

- **待检**：`§12` 说"（目标.1）只有差值，装不下真实赝能隙（$T_c$ 处 3–5 倍）"。本轮辨明：缺的不是温度形状，而是**温度端子→能量的换算**。
- **推导**：C5.1 的 $T=0$ 极限给 $\Delta_{\rm pg}(0)=\frac{\pi}{e^\gamma}k_BT^*$（$T^*$ 为配对端子），故 $\Delta_{\rm pg}(T)=\Delta_{\rm pg}(0)f(T/T^*)$；合并 (目标.1) 得
  $$\frac{2\Delta_{\rm pg}(0)}{k_BT_c}=\frac{2\pi}{e^\gamma}\cdot\frac{T^*}{T_c}=\frac{2\pi}{e^\gamma}\left(1+\frac{\Delta T_{\rm pg}}{T_c}\right).$$
  即**"3–5 倍"＝$T^*/T_c\in[3,5]$**。差值没有装不下，缺的是这一步换算。
- **预言**（非拟合）：赝能隙在 $T_c$ 几乎不降——$r\ge2.2$ 时 $f(1/r)>0.95$（$r{=}2.24$ 给 $0.974$、$r{=}5$ 给 $1.000$），对应文献"almost temperature independent"与"quasi-constant up to $T_c$"。
- **数值**：$f$ 由隙方程解出（$f(0.9)=0.5263$、$f(0.5)=0.9569$，与 BCS 表一致）；比值 $r\in\{2.24,3,3.4,4,5\}$ → $\{7.90,10.58,11.99,14.11,17.64\}$。
- **无参数对照**：Bi2212（67/150）$7.90$、Nd-LSCO $p{=}0.20$（15/75）$17.64$、Raman $p\approx0.12$ 报 $\sim12$ 反推 $r{=}3.40$——量级一致，无拟合。
- **文献**：arXiv:1806.03854（$2\Delta_p/k_BT_c$ 服从"把 $T_c$ 换成 $T^*$"的 BCS 关系；其常数 $d$ 波 4.28 vs 链 $s$ 波 3.53，归链外-C）；arXiv:0910.4295（几乎温度无关、比 BCS 3.5 大许多倍）；arXiv:0708.3732（Raman 反节点隙 quasi-constant up to $T_c$、$p\approx0.12$ 比值 $\sim12$）；arXiv:0908.4430（$\Delta_0$ 随平均场 $T_c^{mf}$ 而非观测 $T_c$ 标度）；PRB 57 R11093（$T^*$ 处 $\Delta\approx\Gamma_0$；**第 117 轮更正**：原文填平宽度 $\Gamma_0(T)=\frac{8}{\pi}(T-T_c)$ 为线性，旧笔记写的 $(T/T_c)^2$ 是误引，见 `01_文献基线/文献卡_R27_Gamma0线性.md`）。
- **拆分**：链外-E → **E1（函数形式／比值，本轮闭合）**＋**E2（连续谱权重与填平标度，仍缺）**；`G21` 未动。
- **预注册 R23 的 P1–P5 全过**；Lean `PseudogapFunction.lean`（8 条，退出码 0、无警告）。
- **历史唯物主义合规**：端子之比是结构（必然性）／$T^*,T_c$ 数值外生（偶然性）分层；结构定读数、读数不反写结构；同形不是还原（不声称 CQM＝BCS）；未用社会范畴。
- **诚实边界**：绝对 $T^*$ 外生（命题 Z2）；强耦合（D01 缺 $\alpha^2F$）不在链内；不把 (R23.2) 与 $d$ 波 4.28 混用；不声称链外-E 全闭合。
- **交付**：`07_数据与现象/预注册判定_R23.md`、`04_计算验证/R23_赝能隙函数形式.py`／`.png`／`_摘要.csv`、`05_Lean验证/PseudogapFunction.lean`、`06_决策记录/2026-11-24_第113轮_赝能隙函数形式.md`；同步 `成果登记.md` R-122、`数据对照协议.md` §二十二、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 114 轮（链外-D 氢原子断链定性；成果登记 R-123；2026-11-24）：**

- **待检**：06 §11.6.2 的氢原子断链（$a_n=n^2a_0$、"$n$ 即主量子数"）能否由链内对象补上？
- **四段定性**：A $\hat{\mathcal S}\to\gamma_n$（链内定义）；B $n=N(\gamma_n)$（**定义式**，零点计数函数恒等）；C $n\to a_n=n^2a_0$（**外部量子力学**：$SO(4)$ 不可约表示 $(j,j)$ 维数 $=(2j+1)^2=n^2$ ＋位力定理；链内无库仑势）；D $a_n\to E_n=-R/n^2$（链内严格代数）。
- **主结果**：B 代入 D 得 $E_n=-R/n^2$，**$\gamma_n$ 完全消失**——"从同步算符谱导出氢原子能级"在氢原子一侧是**空的**，不是"还没算"而是结构上空。
- **no-go 1**：字面读法 $E_n\propto1/\gamma_n^2$，由 Riemann–von Mangoldt $\gamma_n\sim2\pi n/\ln n$ 得 $\rho_n=(\gamma_n/n)^2$ 从 $n{=}1$ 的 $0.00501$ 到 $n{=}10^6$ 的 $2.7753$（$\max/\min=554.47$）；**无常数重标度**（Lean `no_uniform_rescale`）。
- **no-go 2**：$E_n=-R/n^2$ 是单指标确定性序列，展开后为 **picket fence**（间距标准差 $0$，与 GUE Wigner surmise 的 KS $0.532$）——06 L1419"间距标准差 $\approx0.61$、近 GUE"的预言不成立；零点 GUE 统计不能穿过确定性指标映射。
- **附带**：06 的 $n=N(\gamma_n)$ 是**零点序数**（正整数），链内 12.A 的 $n$ 是**绕数**（$2\mathbb Z_{\ge1}$），两者不是同一个。
- **$n^2$ 的真实来源（B 类对照）**：$SO(4)$ $(j,j)$ 维数 $=(2j+1)^2=n^2$（Fock 1935／Bargmann 1936；MDPI *Symmetry* **12**, 1323 (2020)；arXiv:2205.06151），与链内对象无关，不升格为链内第一性。
- **预注册 R24 的 P1–P5 全过**；Lean `HydrogenBreak.lean`（7 条，退出码 0、无警告）。
- **历史唯物主义合规**：$n^{-2}$ 是指标依赖的结构（必然性）／$R,a_0,\gamma_n$ 位置外生（偶然性）分层；结构定读数、读数不反写结构；同形不是还原（$SO(4)$ 的 $n^2$ 与同步算符谱的 $n$ 数值相同不算"导出"）；未用社会范畴。
- **诚实边界**：链外-D **未闭合**（电子 Bloch 带载体仍缺）；不声称 $SO(4)$ 是链内对象；不断言氢原子与 CQM 无关，只判该段推导不成立；06 原文不改，记"待与 06 对账"。
- **交付**：`07_数据与现象/预注册判定_R24.md`、`04_计算验证/R24_氢原子断链真相.py`／`.png`／`_摘要.csv`、`05_Lean验证/HydrogenBreak.lean`、`06_决策记录/2026-11-24_第114轮_氢原子断链定性.md`；同步 `成果登记.md` R-123、`数据对照协议.md` §二十三、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 115 轮（相位模带不能代替电子带；成果登记 R-124；2026-11-24）：**

- **待检**：链外-D 的电子带载体缺；"环 19 相位模带能否代替电子 Bloch 带，给 $N(E_F)$、$v_F$、能带色散？"
- **判定：不能。** 三条独立理由全过：
  - **统计**：相位模是 NGM 玻色型，$n_B=1/(e^{\omega/T}-1)$ 在 $\omega/T=10^{-7}$ 给 $1.0\times10^7$；电子是费米型，$n_F\le1$，有限 $N(E_F)$、$\gamma T$、$\chi_P=\mu_B^2N(E_F)$（$R_W=1$）。声学玻色支 $C_b/C_e=(T/\theta_D)^2$，$T/\theta_D\le0.1$ 时 $\le1\%$。配对核 $K_F$ 收敛到 BCS 对数（相对误差 $1.06\times10^{-8}$），$K_B$ 按 $1/\varepsilon$ 发散（$K_B(10^{-6})/K_B(10^{-2})=3862.6$）——换成玻色统计连有限 $T_c$ 都给不出。
  - **计数／耦合**：带电超导体相位模被 Anderson–Higgs 抬到等离子体频率：$\hbar\Omega_p=3.71$ eV、$\Delta\sim1$ meV、比值 $3713$；中性 Goldstone $\omega(0)=0$ 无费米面。
  - **循环性（链内，决定性）**：相位模预设序参量→序参量预设配对→配对预设 $N(0)$（`M3`）；用它供给 $N(0)$ 即下游当上游，按 `10 探索/AGENTS.md` 第 4 问为循环。Lean `no_phase_to_band` 严格推出矛盾。
- **对链外-D 的后果**：**未闭合**；电子 Bloch 带／$v_F$／vHs 载体仍缺。不声称"原则上不可推"——只否决"相位模带"这一个候选，链内仍需另找载体。环 19 相位扇区职责限定为 BKT／刚度；(目标.3) 的 $e^{-1/2}$ 不当电子带读数。
- **文献（外部 B 类）**：ETH 讲义 §1.2.1／§4.3；Geneva `fermi-gas.pdf` §3.2／§4.2；`cond-mat/9807366` (2.6)–(2.9)；J Res NIST **74A**, 569 (1970)；Annu Rev CMP **10**, 339 (2019), DOI `10.1146/annurev-conmatphys-031119-050644`；arXiv:2310.17148；arXiv:1406.2968；PRB **97**, 054510 (2018), DOI `10.1103/PhysRevB.97.054510`。
- **预注册 R25 的 P1–P4 全过**；Lean `PhaseVsBand.lean`（6 条，退出码 0、无警告）。
- **历史唯物主义合规**：统计—态密度—配对核对应是必然性，$\theta_D,\Omega_p,\Delta,n$ 数值是偶然性；结构定读数、读数不反写结构；同形不是还原（不声称 CQM＝BCS，不把电子统计说成 CQM 公设）；未用社会范畴。
- **诚实边界**：不给电子带／$v_F$／vHs；不动 06 原文与状态栏；不给绝对 $T_c$（命题 Z2）、不给 $\mu^\ast$（审-14）。
- **交付**：`07_数据与现象/预注册判定_R25.md`、`04_计算验证/R25_相位模不能代替电子带.py`／`.png`／`_摘要.csv`、`05_Lean验证/PhaseVsBand.lean`、`06_决策记录/2026-11-24_第115轮_相位模不能代替电子带.md`；同步 `成果登记.md` R-124、`数据对照协议.md` §二十四、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 116 轮（Spin(6) 旋量表示统计关闸；成果登记 R-125；2026-11-24）：**

- **待检**：06 L1695 高优先开放项——"电子费米统计的严格来源（$SU(4)\simeq Spin(6)$ 旋量表示？）"；L722 明写电子携带 $A_4$ 根指标、自旋编码于主丛拓扑。这是链内唯一成文的统计候选。
- **判定：不能。** 旋量表示 $\mathbf4$（$Spin(6)\simeq SU(4)$）的权重 $m=\pm\frac12$ 各二重、$\mathrm{tr}\,e^{2\pi iJ}=-4$——只给**半整数自旋**，不给**交换相位 $\theta=\pi$**。
- **自旋—统计定理前提不全**：定理要求 Lorentz＋定域＋正能＋正范数（Pauli 1940；Streater–Wightman §4-4；NIST SS–1）；06 与主链 Lorentz／boost／微因果文本审计均为 **0**；结构群 $U(1)\times SO(2)_{\rm space}\times SU(4)_{\rm internal}$ 为紧群。
- **二维辫群**：$B_N$ 一维表示给任意 $e^{i\theta}$，$\theta=0$（玻色）、$\pi$（费米）、$\pi/2$（任意子）均合法；$\eta^2=1$ 只在 $d>2$（Laidlaw–DeWitt 1971／Nayak 2008 §II.A.1）。
- **非相对论反例**：自旋 $0$ 的反对称 Slater 两体态与对称态残差均为 $0$——统计独立于单粒子表示（quant-ph/0304088）。
- **Lean 反模型**：`spinorBose`／`spinorFermi` 同旋量号 $-1$、同无 Lorentz，交换号可 $\pm1$；条件定理 `no_route_without_lorentz`。
- **预注册 R26 的 P1–P5 全过**；Lean `SpinorNotStatistics.lean`（7 条，退出码 0、无警告）。
- **历史唯物主义合规**：旋转号是表示权的必然性，交换相位需额外前提（链内缺失）；结构定读数、读数不反写结构；同形不是还原（相对论 QFT 有定理联系，但链内不能用）；未用社会范畴。
- **诚实边界**：06 L1695 **保持开放**，不声称统计不可推（须新增反对易公设或走 FE 通道，本轮不做）；链外-D 仍缺能带载体；`G19`／`临-26` 状态不动；不绝言旋量与费米统计无关。
- **交付**：`07_数据与现象/预注册判定_R26.md`、`04_计算验证/R26_旋量表示统计关闸.py`／`.png`／`_摘要.csv`、`05_Lean验证/SpinorNotStatistics.lean`、`06_决策记录/2026-11-24_第116轮_旋量表示统计关闸.md`；同步 `成果登记.md` R-125、`数据对照协议.md` §二十五、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 117 轮（E2 前提更正／G21 形状；成果登记 R-126；2026-11-24）：**

- **待检**：E2 的"填平标度 $\Gamma_0\propto(T/T_c)^2$"前提与链内 $1-w(T)\propto T^2$ 映射。
- **误引更正（本轮最重要）**：PRB **57**, R11093 (1998) 原文 "broadening proportional to $T-T_c$"、附录 $\Gamma_0(T)=\frac{8}{\pi}(T-T_c)$；Kanigel et al., *Nature Physics* **2**, 447–451 (2006), DOI `10.1038/nphys334` 亦写 "linearly with $T$"。**两篇都没有 $T^2$ 律**；项目旧笔记（README L1264、链外重审 §6.3／E2 行）的 $(T/T_c)^2$ 判为误引，已加更正注记并新建 `01_文献基线/文献卡_R27_Gamma0线性.md`。
- **映射否决**：$\Gamma_0(T_c)=0$（对寿命在超导态无穷大），而 $\omega_D[1-w(T_c)]=64.3\,k_B$K $>0$（$T_c=83,\omega_D=300$）；任意正常数重标度不可弥合零点位置（Lean `no_rescale_at_tc`／`pointwise_at_tc`）。数值上 $\Gamma_{\rm chain}/\Gamma_0$ 跨 $4.7$ 个量级；$T^*/\omega_D\approx0.5$ 处 $1-w$ 的低温 $T^2$ 展开偏离全域 (10B.1) 达 **88%**。
- **外部量级自洽（B 类）**：$\Delta_{\rm pg}(0)/\Gamma_0(T^*)=1.184\,(200/83)$、$1.252\,(150/67)$，支持"$T^*$ 是配对端子"读法，非链内证明。
- **`G21` 形状可写**：$A(\omega)=qA_{\rm coh}(\Delta)+(1-q)A_{\rm incoh}(\Gamma_0)$，$\int A=1$（残差 $<10^{-12}$）；$T\to T_c^+$ 尖锐、$T\to T^*$ 填平。但 $q$ 的空间分布依赖外生 $\varepsilon$ 分布、$\Gamma_0$ 依赖链内未证的对寿命（06 L1350）⇒ **E2 与 `G21` 均未闭合**。
- **预注册 R27 的 P1–P4 全过**；Lean `Gamma0VsPhaseWeight.lean`（5 条，退出码 0、无警告）。
- **历史唯物主义合规**：外部线性涨落与链内 Debye $T^2$ 属不同层次不可还原；$\omega_D,T_c,T^*$ 外生（偶然性）；结构定读数、读数不反写结构；未用社会范畴。
- **诚实边界**：不给 $\Gamma_0$ 的链内数值或第一性来源；不声称 CQM 推出 $\Gamma_0=8(T-T_c)/\pi$；不改 06 原文与状态栏。
- **交付**：`07_数据与现象/预注册判定_R27.md`、`01_文献基线/文献卡_R27_Gamma0线性.md`、`04_计算验证/R27_Gamma0线性核查.py`／`.png`／`_摘要.csv`、`05_Lean验证/Gamma0VsPhaseWeight.lean`、`06_决策记录/2026-11-24_第117轮_Gamma0线性前提更正.md`；同步 `成果登记.md` R-126、`数据对照协议.md` §二十六、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 118 轮（拍频交叉给 Γ0 线性形状；成果登记 R-127；2026-11-24）：**

- **待检**：06 L1350 的 $\tau_{\rm dec}\sim\hbar/|\lambda_m-\lambda_n|$ 与 L1332 的交叉 $\lambda_2(T_c)=\lambda_1(T_c)$ 能否给第 117 轮更正后的 $\Gamma_0=8(T-T_c)/\pi$。
- **判定：形状闭合（A 类）、系数不闭合（B 类）。**
- **线性形状**：两模在 $T_c$ 可微且斜率不同 ⇒ $|\lambda_2-\lambda_1|=|\Delta\lambda'|\,|T-T_c|+o$；代入 $\Gamma_0=\hbar|\lambda_2-\lambda_1|$ 得线性律且 $\Gamma_0(T_c)=0$。数值：劈裂(Tc)=0、斜率 0.350、$R^2=1.000000000$、归一化形状差 $4.44\times10^{-16}$。
- **真交叉必要**：同对称性避免交叉（von Neumann–Wigner 余维 2）在 $T_c$ 留间隙 $2W>0$ ⇒ $\Gamma_0(T_c)>0$，与外部零点矛盾（Lean `no_avoided_crossing`）；链内 $|U(1)//\mathbb Z_n\rangle$ 不同扇区给真交叉根据（arXiv:1405.6414 §2）。
- **$T<T_c$ 零宽度**：L1336 退相干到最低分量、无拍频 ⇒ $\Gamma_0=0$，与外部一致。
- **系数外生**：$|\Delta\lambda'|=8k_B/(\pi\hbar)$ 依赖未证的 $\hat V_{\rm 热}(T)$（L1691 开放）与 $\tau$ 关系（L1350 开放）⇒ **不得写"CQM 推出 $\Gamma_0=8(T-T_c)/\pi$"**。
- **预注册 R28 的 P1–P5 全过**；Lean `CrossingLinearGamma0.lean`（5 条，退出码 0、无警告）。
- **历史唯物主义合规**：可微交叉结构是必然性，斜率／系数外生是偶然性；结构定读数、读数不反写结构；同形不是还原；未用社会范畴。
- **诚实边界**：E2 仍未闭合（系数缺），`G21` 未动；06 L1350／L1691 保持开放（按前提使用，未证明）；不新增环号。
- **交付**：`07_数据与现象/预注册判定_R28.md`、`04_计算验证/R28_拍频交叉给线性Gamma0.py`／`.png`／`_摘要.csv`、`05_Lean验证/CrossingLinearGamma0.lean`、`06_决策记录/2026-11-24_第118轮_拍频交叉给线性Gamma0形状.md`；同步 `成果登记.md` R-127、`数据对照协议.md` §二十七、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 119 轮（τ 关系来源审计；成果登记 R-128；2026-11-24）：**

- **待检**：06 L1350 开放(1)"$\tau\sim\hbar/|\lambda_m-\lambda_n|$ 的严格证明"能否由链内前提给出。
- **no-go 1**：封闭两模叠加的相干幅度平方恒为 $w_1w_2$（数值偏差 $1.11\times10^{-16}$）——相位振荡但不衰减，**没有有限 $\tau$**；自由进动不是退相干（Steck §5.4.2；Zurek RMP **75**, 715 (2003)）。
- **替代结构 (R29.1)**：由 §10.2 空间不均匀对拍频做系综平均，$|C(t)|=1-\frac{\sigma_{\Delta\lambda}^2t^2}{2\hbar^2}+O(t^4)\approx\exp[-\frac12(\sigma t/\hbar)^2]$，$\tau_{1/e}=\sqrt2\hbar/\sigma_{\Delta\lambda}$（二阶系数相对误差 $7.66\times10^{-7}$）——这是**可逆 $T_2^*$ 型退相位**，不是不可逆退相干。
- **no-go 2**：$\tau\propto1/|\Delta\lambda|$ 需 $\sigma=\kappa|\Delta\lambda|$，$\kappa$ 外生（§10.2 只给不均匀、未给分布形式与相对涨落）。
- **no-go 3**：12.A3 高模权重 $\propto1/k$ 但**非零** ⇒ $T_c$ 处 $\sigma>0$、$\tau$ 有限（$w_4=0.1,L_4-L_1=20$ 给 $\sigma(T_c)=6.0$、$\tau=0.236$）；"拍频消失⇒发散"须高模严格为零。
- **后果**：06 L1350 **仍开放**；第 118 轮 $\Gamma_0$ 线性形状不受影响（只需 $\Gamma_0\propto|\Delta\lambda|$）；不声称退相干不可推（新增 $\kappa$／空间统计属 FE 通道）。
- **预注册 R29 的 P1–P4 全过**；Lean `DecoherenceSourceAudit.lean`（5 条，退出码 0、无警告）。
- **历史唯物主义合规**：幺正演化与展宽包络是结构必然性，$\kappa$／高模权重外生；结构定读数、读数不反写结构；同形不是还原（不把 $T_2^*$ 写成环境退相干）；未用社会范畴。
- **诚实边界**：不闭合 L1350；(R29.1) 的分布形式与展宽数值外生；静态展宽可逆；不动 06 原文与状态栏，不动 E2／`G21`。
- **交付**：`07_数据与现象/预注册判定_R29.md`、`04_计算验证/R29_拍频退相干来源审计.py`／`.png`／`_摘要.csv`、`05_Lean验证/DecoherenceSourceAudit.lean`、`06_决策记录/2026-11-24_第119轮_拍频退相干来源审计.md`；同步 `成果登记.md` R-128、`数据对照协议.md` §二十八、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 120 轮（G21 满足率链内定义；成果登记 R-129；2026-11-24）：**

- **待检**：`G21` 的满足率 $q$ 是否缺链内定义？能否证其单调性并给谱映射？
- **口径更正**：旧记"缺链内定义"不准确。工作台 `环06_G19容差标定.md` 的 (6G.8) 已给局域判据，故 $S(T)=\{\varepsilon:J_0A(\varepsilon)w(T)\cos(s\Lambda)\ge\frac{2}{\pi}k_BT\}$、$q(T)=|S(T)|/|\mathcal E|$——它就是 06 §10.2"通过/失败"的空间测度。
- **单调性（A 类）**：$F$ 随 $T$ 严格减（$w'<0$ 由 (10B.1)，$-\frac{2}{\pi}k_BT$ 同向）⇒ $S(T_2)\subseteq S(T_1)$ ⇒ $q$ 非增；数值子集包含全链成立；Lean `MonotoneSaturation.lean`（4 条，退出码 0、无警告）。
- **全域 w**：$w(T_c)=0.7858$，用 (10B.1) 全域；低温展开在 $T^*/\omega_D\approx0.67$ 失效，不用。
- **谱映射形状层（B 类）**：$A(\mathbf k,\omega)=q\mathcal A_{\rm coh}+(1-q)\mathcal A_{\rm incoh}$、${\rm LDOS}(\mathbf r,\omega)=\mathcal A(\varepsilon(\mathbf r),\omega)$ 是同一 $q$ 的 ARPES／STM 两读数，归一残差 $<10^{-12}$；示意 $q(T_c)=0.4058>q(T^*)=0.0675$。
- **外部方向对照（B 类）**：Kanigel et al., *PRL* **99**, 157001 (2007), DOI `10.1103/PhysRevLett.99.157001`；Wise et al., arXiv:0705.1731；arXiv:1305.2778（局域相干谱重与赝隙负相关）。只作方向对照，不声称 CQM 已复现。
- **预注册 R30 的 P1–P4 全过**。
- **历史唯物主义合规**：$w$ 单调与 (6G.8) 是结构必然性，$\varepsilon$ 分布／$J_0$／$N$ 外生（偶然性）；结构定读数、读数不反写结构；同形不是还原；未用社会范畴。
- **诚实边界**：`G21` **未闭合**——$q$ 数值需 $\varepsilon$ 分布外生、线形与 $\Gamma_0$ 系数外生；示意参数与 toy 场是 B 类；$q(T_c)=0.406<p_c$ 是示意标度结果，**不是** $q(T_c)=p_c$（M8 只给必要与上界）；不改 06 原文与状态栏。
- **交付**：`07_数据与现象/预注册判定_R30.md`、`04_计算验证/R30_G21满足率单调性.py`／`.png`／`_摘要.csv`、`05_Lean验证/MonotoneSaturation.lean`、`06_决策记录/2026-11-24_第120轮_G21满足率链内定义.md`；同步 `成果登记.md` R-129、`数据对照协议.md` §二十九、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 121 轮（FE09 候选·未落地；成果登记 R-130；2026-11-24）：**

- **待检**：剩余载体只能走框架扩展；评估最小候选 FE09——用链内 $n=2$ 通量量子做 Chern–Simons 统计附着。
- **判定**：候选自洽、未越界；作为**候选完成·未落地**登记，不改状态栏。
- **候选内容**：新增 Abelian CS 拓扑项 $\Delta\mathcal L=-(q/c)J^\mu a_\mu+\frac{\kappa}{2c}\epsilon^{\mu\nu\rho}a_\mu\partial_\nu a_\rho$，给曲率缺陷—通量复合体附着 $m$ 个 $h/e$；交换相位 $\theta=\pi m$，奇数 $m$ ⇒ 费米、偶数 ⇒ 玻色（Lean `FE09CSAttachment.lean`，4 条，退出码 0、无警告）。
- **链内输入**：12.A 绕数读 $\Phi_n=nh/2e$，第一档 $n=2$ 给 $\Phi_2=h/e$，故 $m=1$ 给费米符号；依赖 `临-6` 归一未闭合（风险已登记）。
- **外部机制（B 类）**：Wilczek *PRL* **49**, 957 (1982)；arXiv:2210.02530 式 (11)–(13)；PNAS **96**, 8821 (1999)——CS 项 $b=-(q/\kappa)\rho$，奇数层级转置。
- **只补统计**：不产生 Bloch 带／$v_F$／vHs／$\Gamma_0$ 系数／绝对 $T_c$／新纯数；不改变六纯数、E1 赝能隙比值、三扇区 min 判据、$q(T)$ 单调性。
- **预注册 R31 的 P1–P5 全过**。
- **历史唯物主义合规**：二维辫群任意交换相位是结构必然性，$\kappa$ 与通量归一外生；结构定读数、读数不反写结构；同形不是还原（不声称 CQM＝任意子超导）；未用社会范畴。
- **红线与边界**：候选落 `08_框架扩展候选/`，无授权不得并入主链／06／08，不改缺口状态栏，不声称 CQM 已含费米子；未解决第 116 轮自旋—统计问题。
- **交付**：`08_框架扩展候选/FE09_链内磁通的CS统计附着.md`（含 `08_框架扩展候选/README.md` 清单）、`07_数据与现象/预注册判定_R31.md`、`04_计算验证/R31_FE09_CS统计附着.py`／`.png`／`_摘要.csv`、`05_Lean验证/FE09CSAttachment.lean`、`06_决策记录/2026-11-24_第121轮_FE09候选.md`；同步 `成果登记.md` R-130、`数据对照协议.md` §三十、`00_当前有效口径表.md`。

**第 122 轮（`临-6` 通量归一对象辨析；成果登记 R-131；2026-11-24）：**

- **待检**：`临-6` 通量归一两种读法（$n/2$ 升 vs $2/n$ 降）是否真矛盾、缺的是什么（FE09 跨档风险）。
- **P1 原文**：L469 绕数读 $\Phi_n^{\rm total}=n\,h/2e$、L451/L481 荷量子归一 $h/(ne)$、L471"换算未定、两式不擅自改号"均逐字命中。
- **P2 外部标准（B 类）**：$\Phi_0(q)=h/q$，绕数 $n$ 给总通量 $n\Phi_0$（Thouless 讲义；Byers–Yang, *PRL* **7**, 46 (1961)；MIT 6.732 §2.7）。
- **P3 对象辨析（A 类）**：前者是 $n$ 个 $2e$ 对量子的**总通量**，后者是单个 $ne$ 团簇的**单位磁通量子**；比值互为倒数（数值乘积恒 1；Lean `reciprocal_ratios`），同一对象读法在 $n>2$ 矛盾（Lean `no_same_object`／`same_object_only_base`）。
- **P4 换算仍缺**：$\zeta$ 索引 $n\mapsto q(n)$ 映射未写；换算因子 $n^2/4$ 从 1（$n=2$）增到 100（$n=20$），不是链内常数——这正是 `临-6`"荷标号与索引对齐"的内容。
- **FE09 影响**：基础档 $n=2$ 换算因子为 1，不受号方向反转影响；跨档推广依赖该映射。
- **预注册 R32 的 P1–P4 全过**；Lean `FluxNormalization.lean`（5 条，退出码 0、无警告）。
- **历史唯物主义合规**：外部磁通标准是结构必然性，$q(n)$ 映射外生（偶然性）；结构定读数、读数不反写结构；同形不是还原；未用社会范畴。
- **诚实边界**：不闭合 `临-6`；不改 (12.3)／(12.A3) 号；不声称 CQM 推出 $h/2e$；`审-7` 未动；不动 06 原文与状态栏。
- **交付**：`07_数据与现象/预注册判定_R32.md`、`04_计算验证/R32_临6通量归一对象辨析.py`／`.png`／`_摘要.csv`、`05_Lean验证/FluxNormalization.lean`、`06_决策记录/2026-11-24_第122轮_临6通量归一对象辨析.md`；同步 `成果登记.md` R-131、`数据对照协议.md` §三十一、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 123 轮（`临-5` 权重归一 no-go；成果登记 R-132；2026-11-24）：**

- **待检**：12.A3 的 $1/k$ 权重能否在无限模式集 12.A1 上归一并维持“第一档主导”（`临-5`）。
- **P1 原文**：12.A1 模式集 $2\mathbb Z_{\ge1}$ **无限**、12.A2 局域填档（无截断函数）、12.A3 $\Phi_n/\Phi_2=2/n=1/k$、L483/L492“第一档主导”均逐字命中。
- **归一 no-go（P2–P4）**：若 $w_k=c/k$ 归一于 $K$，则 $w_1=1/H_K$；外部标准 $H_K=\ln K+\gamma+O(1/K)$ **发散**（Oresme；积分判别法；arXiv:0706.2513）⇒ $K\to\infty$ 时 $w_1\to0$，与“第一档主导”不相容。数值：$H_K$ 增、$w_1$ 严格减，$w_1(10^6)=0.0695$（渐近偏差 $1.68\times10^{-2}$）；$w_1\ge0.5$ 须 $K\le3$。
- **截断外生**：12.A2 的 $J_{\rm cr}$ 与涨落幅度分布未在链内写出 ⇒ 有限截断 $K$ 外生；`临-5` 的权重归一不能由 12.A3 单独闭合。
- **预注册 R33 的 P1–P4 全过**；Lean `WeightNormalization.lean`（10 条，退出码 0、无警告）：递归调和数严格增、$w_1(K)$ 严格减、$K>2$ 时 $w_1<2/3$。
- **历史唯物主义合规**：$1/k$ 阶梯与调和发散是结构必然性（数学层），截断 $K$ 由材料局域强度决定属偶然性；结构定读数、读数不反写结构；同形不是还原；未用社会范畴。
- **诚实边界**：不闭合 `临-5`、不给 $K_{\rm cut}$、不改 12.A3 形式；调和级数是 B 类工具；`临-6`／`临-26` 未动；不动 06 原文与状态栏。
- **交付**：`07_数据与现象/预注册判定_R33.md`、`04_计算验证/R33_临5权重归一性.py`／`.png`／`_摘要.csv`、`05_Lean验证/WeightNormalization.lean`、`06_决策记录/2026-11-24_第123轮_临5权重归一性.md`；同步 `成果登记.md` R-132、`数据对照协议.md` §三十二、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 124 轮（`临-26` 配对密度数学归一；成果登记 R-133；2026-11-24）：**

- **待检**：13.A6 的 $\rho^{(2)}(i)=p^{(2)}(i)/\sum_jp^{(2)}(j)$ 与 $\rho^{(n)}=\frac2n\rho^{(2)}$ 的总质量各是多少？能否当概率密度？缺的是什么（`临-26`）。
- **构造恒等式（P3、P5）**：$\sum_i\rho^{(2)}=1$（分母即总和，构造性归一，不需物理输入）；$\sum_i\rho^{(n)}=2/n$（$n=2$ 为 1，$n>2$ 为**次概率质量**，不是概率密度）。数值残差 $<10^{-12}$；Lean `PairDensityNormalization.lean`（4 条，退出码 0、无警告）。
- **同数不同物（P4）**：密度总质量 $2/n$ 与 12.3 单位磁通量子比 $2/n$ 数值恒等，但前者是密度质量、后者是通量比（第 122 轮 R32 已定性）——**不得说“密度就是通量”**，也不闭合 `临-6`。
- **外部测度标准（P2，B 类）**：概率密度总质量 $=1$；非负函数总质量 $<1$ 给有限测度／次概率（Radon–Nikodym 密度依赖参考测度）。不升格为链内第一性。
- **仍缺**：$p^{(2)}(i)$ 的物理形式、为何以 2 配对为基准、降权为何取 $2/n$——即 `临-26` 的**物理归一**；L570 明写 13.A6 是结构分解、不是已证等式。
- **预注册 R34 的 P1–P4 全过**。
- **历史唯物主义合规**：归一恒等式是结构必然性（数学层），$p^{(2)}$ 分布与基准选取外生（材料层）；结构定读数、读数不反写结构；同形不是还原；未用社会范畴。
- **诚实边界**：不闭合 `临-26`、不称 $\rho^{(n)}$ 为概率密度、不改 13.A6 形式；`临-5`／`临-6` 未动；不动 06 原文与状态栏。
- **交付**：`07_数据与现象/预注册判定_R34.md`、`04_计算验证/R34_配对密度归一.py`／`.png`／`_摘要.csv`、`05_Lean验证/PairDensityNormalization.lean`、`06_决策记录/2026-11-24_第124轮_配对密度归一.md`；同步 `成果登记.md` R-133、`数据对照协议.md` §三十三、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 125 轮（两把阶梯辨析；成果登记 R-134；2026-11-24）：**

- **待检**：L616“$\gamma_n$ 与 (12.3) 两梯不可互译”与 L1280“频率阶梯钉成 $2\ln n$（$\gamma_n$ 侧）”的张力，按数论标准如何判？
- **P1 原文**：L616／L1280／L544／L1429 四处均逐字命中。
- **外部数论（P2、P4，B 类）**：Riemann–von Mangoldt ⇒ $\gamma_n\sim2\pi n/\ln n$、相邻间距 $\sim2\pi/\ln n$；$2\ln n$ 步长 $2\ln(1+1/n)\sim2/n$（Lean `log_ladder_step` 严格证明）；$\{\log p\}$ 间距 $\sim1/p$。**三梯渐近间距两两不同**（MathWorld；arXiv:1307.5723；arXiv:1011.3997／DOI `10.4213/im5558`）。
- **P3 数值**：$\gamma_n/(2\ln n)=15.2\,(n{=}2)\to102.8\,(n{=}1000)$；$\Delta\gamma_n/[2\ln(1+1/n)]$ 跨 4.6 个量级；渐近间距（$n=10^6$）$4.55\times10^{-1}$／$2.0\times10^{-6}$／$7.24\times10^{-8}$；RvM 对上 $\gamma_n$、对不上 $2\ln n$。
- **判定（A 类）**：L1280 的“（$\gamma_n$ 侧）”按数论标准不能字面成立，登记为**刻度混用口径问题**；**不改 06／主链原文**。
- **后果**：`临-26` 的 $\delta v/\bar v$ 对齐不能用 $\gamma_n$ 数值替代验证；`临-22` 的阻尼率统一不能靠把 $\beta_n$ 读成 $2\ln n$ 消解。
- **预注册 R35 的 P1–P4 全过**；Lean `TwoLadders.lean`（3 条，退出码 0、无警告）。
- **历史唯物主义合规**：三梯渐近间距是外部数论结构（B 类工具），$\gamma_n$ 数值外生；结构定读数、读数不反写结构；同形不是还原（不把 RvM 当链内结论）；未用社会范畴。
- **诚实边界**：不闭合 `临-26`／`临-22`；不声称 CQM 推出 Riemann–von Mangoldt；不断言 L1280 “错”（只说不能字面读）；不动缺口状态栏。
- **交付**：`07_数据与现象/预注册判定_R35.md`、`04_计算验证/R35_两把阶梯辨析.py`／`.png`／`_摘要.csv`、`05_Lean验证/TwoLadders.lean`、`06_决策记录/2026-11-24_第125轮_两把阶梯辨析.md`；同步 `成果登记.md` R-134、`数据对照协议.md` §三十四、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 126 轮（参与比作截断候选；成果登记 R-135；2026-11-24）：**

- **待检**：R33 判 $1/k$ 权重归一需外生截断；评估链内 `临-21` 的参与比 $n_{\rm eff}=1/\sum p_i^2$ 能否当截断。
- **候选（构造假设，非推导）**：$K=\mathrm{round}(n_{\rm eff})$、$w_1=1/H_K$。链内 `临-21` 只给泛函与界，12.A2 只给局域填档条件，没有“通道数＝参与点数”的等式；$p_i$ 来源未定。
- **外部 IPR 标准（B 类）**：$n_{\rm eff}\in[1,N]$，等权给 $N$、完全局域给 1（Ujfalusi–Varga, *PRB* **86**, 125143 (2012), DOI `10.1103/PhysRevB.86.125143`；arXiv:0903.5172；arXiv:1108.3130）。
- **数值（$N=64$）**：均匀 $n_{\rm eff}=64\to w_1=0.2108$；局域 $\ell=8$ 给 $16\to0.2958$；随机 Dirichlet $28.8\to0.2524$。**预注册方向成立**：ℓ 增 ⇒ $n_{\rm eff}$ 增 ⇒ $w_1$ 减，与 L483“材料通常只显第一档”相容；若实测相反则候选被否。
- **预注册 R36 的 P1–P3 全过**；Lean `ParticipationCutoff.lean`（2 条，退出码 0、无警告）证 3 点域 $\frac13\le\sum p_i^2\le1$、$1\le n_{\rm eff}\le3$；$w_1$ 随 $K$ 减复用第 123 轮 `WeightNormalization`（10 条）。
- **历史唯物主义合规**：参与比泛函与界是结构（链内＋外部 IPR 标准），$p_i$ 分布由材料决定属偶然性；结构定读数、读数不反写结构；同形不是还原（不把 IPR 当链内公设、不把识别当已证）；未用社会范畴。
- **诚实边界**：候选一致但**未闭合** `临-5`／`临-21`；不给 $p_i$ 来源与识别证明；不声称 CQM 推出 IPR；不改 12.A2／12.A3 与状态栏。
- **交付**：`07_数据与现象/预注册判定_R36.md`、`04_计算验证/R36_参与比作截断.py`／`.png`／`_摘要.csv`、`05_Lean验证/ParticipationCutoff.lean`、`06_决策记录/2026-11-24_第126轮_参与比作截断.md`；同步 `成果登记.md` R-135、`数据对照协议.md` §三十五、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 127 轮（参与比系数轮廓依赖；成果登记 R-136；2026-11-24）：**

- **待检**：`临-21` 的“三候选无一般序、$\pi(\xi/a)^2$ 只是等权读数、权重外生”能否定量化？
- **P1 原文**：L736／L1608／L1640 三处均逐字命中。
- **二维参与比系数（P2、P3，B 类工具）**：$n_{\rm eff}=(\sum_iw_i)^2/\sum_iw_i^2$。均匀圆盘给 $C=\pi$、高斯给 $4\pi$、指数给 $8\pi$（标准二维积分）。数值（$L=501,\xi/a=48$）：$C=3.131/12.566/24.043$，对应理论 $\pi/4\pi/8\pi$，相对误差 $0.35\%/0.00\%/4.34\%$。
- **判定（A 类）**：**系数相差 8 倍** ⇒ $\xi$ 单独**不能**定 $n_{\rm eff}$；链内“无一般序、权重外生”被定量坐实；“$\pi(\xi/a)^2$”只是等权轮廓特例。
- **后果**：R36 的 $K=n_{\rm eff}$ 候选只能停在形状层、**不给数值**；`临-21`／`临-5` 不闭合。
- **预注册 R37 的 P1–P3 全过**；Lean `ParticipationCoefficient.lean`（3 条，退出码 0、无警告）证一般权重恒等式、整体标度不变性、等权饱和 $=3$。
- **历史唯物主义合规**：参与比泛函与二维积分系数是结构（外部 IPR 标准，B 类），具体轮廓与材料 $\xi$ 外生；结构定读数、读数不反写结构；同形不是还原；未用社会范畴。
- **诚实边界**：不闭合 `临-21`／`临-5`、不给 $p_i$ 来源与 $K$ 数值、不声称 CQM 推出 IPR 或二维积分；离散边缘修正（指数 4.34%）如实登记；不改原文与状态栏。
- **交付**：`07_数据与现象/预注册判定_R37.md`、`04_计算验证/R37_参与比系数轮廓依赖.py`／`.png`／`_摘要.csv`、`05_Lean验证/ParticipationCoefficient.lean`、`06_决策记录/2026-11-24_第127轮_参与比系数轮廓依赖.md`；同步 `成果登记.md` R-136、`数据对照协议.md` §三十六、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 128 轮（M2 谱形同形边界；成果登记 R-137；2026-11-24）：**

- **待检**：06 M2“节点间差异方差与声子配对模式的识别未证”；链内 R101 的 $\alpha^2F=A\omega^2\Theta(\omega_D-\omega)$ 与外部 Eliashberg 标准的同形边界。
- **P1 原文**：06 L176／L509／L1641 的 M2 登记与 R101 链内谱均命中。
- **同形与矩（P2、P3，B 类标准）**：外部 $\lambda=2\int\alpha^2F/\omega\,d\omega$、声学 $\alpha^2F\propto\omega^2$（ABINIT 文档；arXiv:1610.09441 式 (2)–(4)；Springer 2025）。对 $\alpha^2F=A\omega^s\Theta(\omega_D-\omega)$ 严格得
  $$\lambda_s=\frac{2A}{s}\omega_D^{s},\qquad \omega_{\log}=e^{-1/s}\omega_D. \tag{R38.1}$$
  数值（$A=1.7,\omega_D=32$）：$s=2$ 给 $\lambda=A\omega_D^2$、$\omega_{\log}=e^{-1/2}\omega_D$（**复现 R101**）；$s=3$ 给 $e^{-1/3}\omega_D$（振幅支）；两矩与 $A$ 无关。
- **识别缺口（P4）**：外部 $\alpha^2F=\frac1{N(0)}\sum|g|^2\delta(\omega-\omega_q)$ 依赖电子—声子矩阵元 $g$ 与费米面态 $N(0)$，链内均无载体（`链外-D`）⇒ 不能写“差异方差＝声子配对模式”，**M2 不闭合**。
- **预注册 R38 的 P1–P3 全过**；Lean `PairingModeShape.lean`（3 条，退出码 0、无警告）证被积函数恒等式、幅度无关性、线性标度。
- **历史唯物主义合规**：幂律依赖是结构必然性、$A/g/N(0)$ 外生（偶然性）；结构定读数、读数不反写结构；同形不是还原；未用社会范畴。
- **诚实边界**：不闭合 M2、不给 $g/N(0)$ 来源、不声称 CQM 推出 Eliashberg 标准、不动 06 原文与状态栏。
- **交付**：`07_数据与现象/预注册判定_R38.md`、`04_计算验证/R38_M2谱形同形边界.py`／`.png`／`_摘要.csv`、`05_Lean验证/PairingModeShape.lean`、`06_决策记录/2026-11-24_第128轮_M2谱形同形边界.md`；同步 `成果登记.md` R-137、`数据对照协议.md` §三十七、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 129 轮（六纯数代数闭环；成果登记 R-138；2026-11-24）：**

- **待检**：第 119 轮登记的第六纯数（Josephson 比）是否独立于已闭环五纯数网络？
- **主恒等式（P3）**：由 $R_1=2\pi/e^\gamma$、$R_3^2=4\pi$（Lean `FiveRatioNetwork`）与 $R_6=\pi^2/2e^\gamma$ 严格得
  $$\frac{R_6}{R_1}=\frac\pi4=\frac{R_3^2}{16},\qquad \boxed{R_6=\frac{R_1R_3^2}{16}}. \tag{R39.1}$$
  第六纯数由第一与第三纯数生成，**不独立**。数值 $R_1=3.527754$、$R_2=1.426127$、$R_3=3.544908$、$R_4=0.236428$、$\kappa=1.736661$、$R_6=2.770691$；四恒等式残差 $1.776\times10^{-15}$（双精度舍入）／$4.441\times10^{-16}$／$4.441\times10^{-16}$／$1.110\times10^{-16}$，按**相对残差**判阈值，图中如实标注。
- **外部 AB 标准（B 类）**：$I_cR_n=\pi\Delta_0/2e$（Ambegaokar–Baratoff, *PRL* **10**, 486 (1963)；erratum **11**, 104 (1963), DOI `10.1103/PhysRevLett.11.104`；Posazhennikova, arXiv:0908.1761 式 (3.31)/(3.33)）。
- **预注册 R39 的 P1–P4 全过**；Lean `SixRatioClosure.lean`（3 条，退出码 0、无警告）证 $R_3^2=4\pi$、$R_6=R_1R_3^2/16$、$R_6/R_1=\pi/4$。
- **历史唯物主义合规**：纯数间代数依赖是结构必然性、材料量外生；结构定读数、读数不反写结构；同形不是还原（不声称 CQM 推出 AB 隧道理论）；未用社会范畴。
- **诚实边界**：不闭合任何缺口、不重判“2 生成元”口径、高透明 SNS／Andreev 不在范围、不动 06 原文与状态栏。
- **交付**：`07_数据与现象/预注册判定_R39.md`、`04_计算验证/R39_六纯数闭环.py`／`.png`／`_摘要.csv`、`05_Lean验证/SixRatioClosure.lean`、`06_决策记录/2026-11-24_第129轮_六纯数闭环.md`；同步 `成果登记.md` R-138、`数据对照协议.md` §三十八、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 130 轮（`审-7` 三处“2”对象辨析；成果登记 R-139；2026-11-24）：**

- **待检**：`审-7` 的三处“2”（$2e$、$\zeta(-2)$、$N(0)$）是否同一对象？
- **P1 原文**：L1419／L435／L496／L1250 四处逐字命中。
- **对象与单位（P2、P3，B 类标准）**：$2e$ 是**配对荷**（电荷 [C]，归一 $2e/e=2$）；$\zeta(-2)$ 的 2 是**平凡零点序号**（无量纲整数）；$N(0)$ 的 2 是**态密度自旋简并**（$[\mathrm E^{-1}\mathrm V^{-1}]$，Kopnin §2.1 $N(0)=mp_F/2\pi^2\hbar^3$）。外部 $\Phi_0=h/2e$、$\zeta(-2n)=0$。自然单位单自旋 DOS $=1/(2\pi^2)=0.050661$，与 2 差 **39.5 倍**；读成 2 须外生 $N_{\rm ref}=0.025330$。
- **后果（P4）**：`审-7` 假连接判定成立；三处 2 不可互相供给；`审-7`／`临-7` 不闭合、26.B 乘法内容仍缺。
- **预注册 R40 的 P1–P3 全过**；Lean `ThreeTwos.lean`（3 条，退出码 0、无警告）用三个不同类型表达对象区分，证 $2e/e=2$、零点序号 2、条件式 DOS≠2。**本安装的 Mathlib 无 $\pi$ 数值界定理**（只有 `Real.pi_pos`），不等式以条件式给出、数值界由脚本承担——如实登记，不冒充严格证明。
- **历史唯物主义合规**：对象区分来自既有单位/结构（必然性），自然单位与参考尺度外生（偶然性）；结构定读数、读数不反写结构；同形不是还原（三个无量纲 2 数值相同不推出物理同一）；未用社会范畴。
- **诚实边界**：不闭合 `审-7`／`临-7`、不给 $N(0)$ 数值、不声称 CQM 推出外部磁通量子／DOS 标准、不动 06 原文与状态栏。
- **交付**：`07_数据与现象/预注册判定_R40.md`、`04_计算验证/R40_三处2的对象辨析.py`／`.png`／`_摘要.csv`、`05_Lean验证/ThreeTwos.lean`、`06_决策记录/2026-11-24_第130轮_三处2的对象辨析.md`；同步 `成果登记.md` R-139、`数据对照协议.md` §三十九、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 131 轮（`审-7` 乘法内容定位；成果登记 R-140；2026-11-24）：**

- **待检**：`审-7` 的“Hecke 乘法内容缺”是否等于“链内根本没有乘法”？
- **P1 原文**：L1250／L1260／L211／L267 四处逐字命中。
- **外部标准（P2，B 类）**：Hecke 特征形系数乘性 ⇒ $L(f,s)$ 有 Euler 积；Mellin 变换把 $q$ 展开（对 $n$ 的和）变为 Dirichlet 级数（Rolen, *Modular Forms Lecture 21*；Dospinescu, *Lecture 7*；arXiv:2404.01042）。
- **定位（P3、P4，A 类）**：链内**存在**乘法对象——和乐积 $\prod_Cr_e$ 及其统计（R83：$\langle\ln\prod_Cr\rangle=-n\sigma^2/16\pi^2+\cdots$）；而 $C_{ij}=f(\varepsilon_i-\varepsilon_j)$ 是加法差。数值：闭环加法和残差 $8.3\times10^{-17}$（望远镜恒 0），和乐积对数方差 $7.6\times10^{-4}$、均值 $3.3\times10^{-4}$（R83 预测 $-1.9\times10^{-4}$ 同量级）。$C\to r$ 靠 `审-1` 矩阵分支（未闭合），$r\leftrightarrow v_\tau$ 仅 $O(\ell)$（L267）。
- **判定**：`审-7` 应读作“乘法内容在和乐扇区、未桥接到 $C$ 扇区”，**不是**“链内无乘法”；`审-7`／`审-1`／`M1` 均不闭合。
- **预注册 R41 的 P1–P3 全过**；Lean `MultiplicativeContent.lean`（3 条，退出码 0、无警告）证三点闭环加法差望远镜恒 0、$e^ae^be^c=e^{a+b+c}$、和为 0 时积为 1。
- **历史唯物主义合规**：加法差望远镜与指数乘法化是结构（数学层），涨落与和乐赋值外生；结构定读数、读数不反写结构；同形不是还原（不把和乐积当 Euler 积）；未用社会范畴。
- **诚实边界**：不声称链内已有 Hecke 特征形或 Euler 积、不声称 CQM 推出 Hecke 标准（B 类）、不动 06 原文与状态栏。
- **交付**：`07_数据与现象/预注册判定_R41.md`、`04_计算验证/R41_乘法内容定位.py`／`.png`／`_摘要.csv`、`05_Lean验证/MultiplicativeContent.lean`、`06_决策记录/2026-11-24_第131轮_乘法内容定位.md`；同步 `成果登记.md` R-140、`数据对照协议.md` §四十、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 132 轮（`审-1` 局部逆全局边界；成果登记 R-141；2026-11-24）：**

- **待检**：`审-1` 的局部逆已证，全局可逆边界是否可定量化？
- **P1 原文**：工作台 R100 的 8A.2／8A.4／阈值边界／“不声称全局”四处均命中。
- **外部标准（P2，B 类）**：Hadamard 全局反函数定理要求导数处处非零且 proper／目标单连通（一维即区间内不变号；Wikipedia；arXiv:2306.17410；arXiv:1410.7902）。
- **阈值（P3、P4，A 类）**：对 $f=-c\lambda+d\lambda^3$、$f'=-c+3d\lambda^2$，可逆区间为 $|\lambda|<\lambda_*\equiv\sqrt{c/(3|d|)}$（R42.1）。取 $c=1,|d|=10$（R78 上界）得 $\lambda_*=0.182574$ rad；由 $\lambda=\ln\sqrt{1-\varepsilon/2\pi}$ 反解 $\varepsilon_*=1.9221$ rad（约 $2\pi$ 的 30.6%）；典型 $\sigma_\varepsilon=0.1$ 给 $|\lambda|\approx0.00796\ll\lambda_*$。**判据层锚邻域局部逆足够**，但大亏角域不能用全局逆；`审-1` 不闭合。
- **预注册 R42 的 P1–P3 全过**；Lean `InverseRadius.lean`（2 条，退出码 0、无警告）严格证 $f'=-c+3d\lambda^2<0\iff\lambda^2<c/(3d)$ 与阈值点导数为零。初稿曾留 `sorry`，已删除并给完整证明（禁用项自检通过）。
- **历史唯物主义合规**：阈值是数学结构（必然性），$|d|\le10$ 是 R78 归一化假设、$\sigma_\varepsilon$ 外生（偶然性）；结构定读数、读数不反写结构；同形不是还原；未用社会范畴。
- **诚实边界**：不闭合 `审-1`、不给 $d$ 第一性来源、不声称 CQM 推出 Hadamard 定理、不动 06 原文与状态栏。
- **交付**：`07_数据与现象/预注册判定_R42.md`、`04_计算验证/R42_局部逆全局边界.py`／`.png`／`_摘要.csv`、`05_Lean验证/InverseRadius.lean`、`06_决策记录/2026-11-24_第132轮_局部逆全局边界.md`；同步 `成果登记.md` R-141、`数据对照协议.md` §四十一、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 133 轮（Lean 产物可复现性审计；成果登记 R-142；2026-11-24）：**

- **性质**：纯本地可复现性核查，不改理论结论、不动缺口状态栏。
- **结果**：`05_Lean验证/` 共 **200** 个 `.lean`、**1177** 条 theorem/lemma；去注释正文扫描禁用项（`axiom`／`sorry`／`admit`／`native_decide`／`unsafe`）命中 **0**、空文件 0；第 128–132 轮五个文件（`InverseRadius`、`MultiplicativeContent`、`ThreeTwos`、`SixRatioClosure`、`PairingModeShape`）逐个 `lake env lean` 均 EXIT=0、无警告/错误；三道核查 PROV 0／CONS 0／PROBE 0。
- **如实登记**：审计脚本按 mtime 排序与轮次顺序不一致，A4 改用按轮次明确指定的 5 个文件编译；本轮**不等于 200 文件全部编译通过**，也不覆盖 08 主库 Lean。
- **交付**：`07_数据与现象/预注册判定_R43.md`、`04_计算验证/R43_Lean审计.py`／`R43_Lean审计_摘要.csv`、`06_决策记录/2026-11-24_第133轮_Lean审计.md`；同步 `成果登记.md` R-142、`数据对照协议.md` §四十二。

**第 134 轮（第七纯数 $S_J$；成果登记 R-143；2026-11-24）：**

- **待检**：第 119 轮登记的“AB 近 $T_c$ 斜率 2.65≈勘误 2.67”能否写成链内纯数？
- **推导（P3，A 类）**：链内 gap 近 $T_c$ 给 $\Delta^2\simeq\frac{8\pi^2}{7\zeta_3}(k_BT_c)^2(1-t)$；AB 有限温式（B 类）$\tanh x\simeq x$ 给 $I_cR_n\simeq\frac{2\pi^3}{7\zeta_3}\frac{k_BT_c}{e}(1-t)$，而 $I_c(0)R_n=\frac{\pi^2}{2e^\gamma}\frac{k_BT_c}{e}$。故
  $$\boxed{S_J\equiv\frac{T_c}{I_c(0)}\left|\frac{dI_c}{dT}\right|_{T_c}=\frac{4\pi e^\gamma}{7\zeta_3}=2.659919}. \tag{R44.1}$$
  由 $e^\gamma,\zeta_3,\pi$ 生成，**无新生成元**；与 AB 勘误 $2.67$ 差 **0.38%**，与第 119 轮数值 $2.65$ 一致；AB+BCS 插值数值斜率 $2.6638$。
- **预注册 R44 的 P1–P3 全过**；Lean `SeventhRatio.lean`（1 条，退出码 0、无警告）证两系数相除给 $4\pi E/(7Z)$。
- **历史唯物主义合规**：纯数是结构必然性、材料与绝对 $T_c$ 外生；结构定读数、读数不反写结构；同形不是还原（不声称 CQM 推出 AB 有限温式）；未用社会范畴。
- **诚实边界**：不闭合任何缺口、高透明 SNS／Andreev 不在范围、不动 06 原文与状态栏。
- **交付**：`07_数据与现象/预注册判定_R44.md`、`04_计算验证/R44_第七纯数.py`／`.png`／`_摘要.csv`、`05_Lean验证/SeventhRatio.lean`、`06_决策记录/2026-11-24_第134轮_第七纯数.md`；同步 `成果登记.md` R-143、`数据对照协议.md` §四十三、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 135 轮（七纯数生成元结构；成果登记 R-144；2026-11-24）：**

- **待检**：七纯数是否由同一生成元组给出、有无第八生成元？
- **指数矩阵（P2、P3）**：对 $(\pi,e^\gamma,\zeta_3)$，七纯数指数全为有理，矩阵秩 = **3**。$R_1=(1,-1,0)$、$R_2=(0,0,-1)$、$R_3=(1/2,0,0)$、$R_4=(0,-2,0)$、$\kappa=(0,1,-1/2)$、$R_6=(2,-1,0)$、$S_J=(1,1,-1)$。
- **派生关系（P4）**：$R_4=\frac{3R_1^2}{R_3^4}$、$\kappa=\frac{R_3^2\sqrt{R_2}}{R_1\sqrt6}$、$R_6=\frac{R_1R_3^2}{16}$、$S_J=\frac{R_2R_3^4}{24R_1}$，残差 $5.6\times10^{-17}$～$4.4\times10^{-16}$；$R_1,R_2,R_3$ 生成其余四个，**无第八生成元**。
- **预注册 R45 的 P1–P4 全过**；Lean `SevenRatioStructure.lean`（2 条，退出码 0、无警告）证 $R_4$、$S_J$ 组合式（$R_6$、$R_3^2$ 已由既有 Lean 证明）。
- **历史唯物主义合规**：代数依赖是结构必然性、材料数值外生；结构定读数、读数不反写结构；只登记代数依赖、不声称物理因果（同形不是还原）；未用社会范畴。
- **诚实边界**：不闭合任何缺口；**不重判“2 生成元”口径**（本轮只登记 $\pi$ 为第三指数）；不改 06 原文与状态栏。
- **交付**：`07_数据与现象/预注册判定_R45.md`、`04_计算验证/R45_七纯数生成元结构.py`／`_摘要.csv`、`05_Lean验证/SevenRatioStructure.lean`、`06_决策记录/2026-11-24_第135轮_七纯数生成元结构.md`；同步 `成果登记.md` R-144、`数据对照协议.md` §四十四、`00_当前有效口径表.md`、`02_缺口重审/链外重审_六个接口的链内接法.md`。

**第 136 轮（环 4／`审-21` 载体归属判定：顶点谱不承载亏角、载体改为非仿射子空间；成果登记 R-145；2026-11-25）：**

- **触发（"发现不对劲就回头修"）**：R96 把亏角载体定为「$\ker H$ 的正交补」，R97 把它的谱对接**余切拉普拉斯**（顶点图）并据此判「截断＝$\Theta_D$」。本轮不问系数，只问：顶点空间的谱能不能承载亏角？
- **判定：不能，且是零而非小量。** $\tilde A_{ee'}=\partial\varepsilon_e/\partial\ell_{e'}$、$B_{e,(i,a)}=\partial\ell_e/\partial x_{i,a}$，则 $\tilde AB=\partial\varepsilon_e/\partial x_{i,a}$。数值（BCC 内部铰链）：$\max|\tilde AB|/(\max|\tilde A|\max|B|)=3.3\times10^{-10}$（$n{=}2$）、$5.2\times10^{-10}$（$n{=}3$）；$\|\tilde A_{N_I}P_{N_I}\|/\|\tilde A_{N_I}\|=1.000000$ ⇒ $\operatorname{im}\tilde A\subseteq N_I:=(\operatorname{im}B)^\perp$。
- **决定性推论**：$L=B^\top WB$ 的全部本征矢在 $\operatorname{im}B$ 内 ⇒ **用顶点谱求和的 $\sigma_\varepsilon^2$ 恒等于零**（Lean `vertex_spectrum_sigma_zero`）。R97 的「曲率模 ↔ 余切拉普拉斯非零模」**谱同一性撤销**；保留「截断＝支集端点」的一般原则与 $\Theta_D$ 作为 (i) 支量程。
- **文献的适用域（L136b）**：arXiv:0707.4513 式 27–28「Regge Hessian 非零 sector 由格点拉普拉斯支配」是**顶点基**陈述，不能移到边基的非仿射扇区。
- **维数判据**：$\dim N_I=E-(3V-6)$，$n=2..5$ 给 $15/101/307/681$；$E/V=7.132-7.133/n$（极限配位数 $z=14.26$，与 BCC Delaunay 的 14 一致）⇒ $\dim N_I/(3V-6)\to1.377>1$。非仿射扇区在无限体比整个顶点位移空间还大，「顶点谱＋小修正」在维数上不够。
- **载体修正 (4.1″)**：$\langle(\Delta\varepsilon_e)^2\rangle_T=\sum_{k\in N_I}|Av_k|_e^2c_k^0[1+2n_B(\omega_k)]+b_e\,n_d(T)$，$n_d=\nu e^{-E_c/k_BT}$。(ii) 是向错对的热激活（弗兰克角＝亏角；KTHNY fugacity）；$b_e$ 由 $\varepsilon_e=-2.598\,\delta$ 定（独立复现 R73 的 $-2.599$，差 $0.03\%$）。
- **新登记 `审-22`**：第二温度入口，与 AGENTS §2「唯一 $T$ 入口」直接冲突，显式登记。它与 $[1+2n_B]$ **不是同一统计**——虚频模的解析延拓给 $\coth$，不是 $e^{-E/T}$；后者是势垒穿越速率（Kramers／Langer）。
- **"不对劲"的根源**：理想晶体以原子位置为基本变量，$N_I$ 方向被三角不等式约束消去 ⇒ $\varepsilon\equiv0$（R73）。承认 $\varepsilon\ne0$ 就必须承认缺陷。这解释了 R71–R73 一路「$\sigma_0^2$ 归一不了」：被归一的是物理上被约束掉的自由度，或为零的量。
- **历史唯物主义合规**：可嵌入性（几何基础）决定读数域，填充由材料力常数与缺陷结构定（偶然性）；差异源从「理想晶格的抽象涨落」落回「现实材料的缺陷结构」——物质第一性。未用社会范畴。
- **诚实边界**：不闭合 `审-21`／`审-10`；不给边基质量矩阵、$E_c$、$\nu$；不声称超导来自缺陷；不改 06 原文；唯一编号 36→37、闭合数仍 0。
- **交付**：`03_推导工作台/环04_内禀扇区的自由度归属与非仿射载体.md`、`04_计算验证/环04_内禀扇区自由度归属.py`／`.png`／`.csv`／`_摘要.csv`（五组断言，四面板非拟合）、`05_Lean验证/NonAffineSector.lean`（13 条，退出码 0、无禁用项）、`06_决策记录/2026-11-25_第136轮_内禀扇区自由度归属.md`；同步主链环 4 缺口行／§11（`审-21` 注记＋`审-22` 新行）／§15／§16、`00_当前有效口径表.md` §一边界注记、`02_缺口重审` 环 4 行、`01_文献基线` L136a–d、`成果登记.md` R-145。

**第 137 轮（环 4／`审-21`／`审-10` 后续：非仿射刚度谱、截断位置重定；成果登记 R-146；2026-11-25）：**

- **简化（严格）**：平直背景上 $\omega_e=2\pi-\sum_T\theta_e^T=\varepsilon_e$（R96 引文 (2.9) 的定义本身），故 $H_{ee'}=-\partial\omega_e/\partial\ell_{e'}=\partial\varepsilon_e/\partial\ell_{e'}=\tilde A_{ee'}$；又 $\operatorname{im}\tilde A\subseteq N_I$（R145），故 $H_{N_I}=P_N^\top HP_N=\tilde A$。**非仿射刚度谱＝$\tilde A$ 的奇异值谱**——纯几何、无需 Regge 三阶展开、无自由参数。
- **谱（BCC 内部铰链行）**：$\sigma_{\max}=14.262/18.928/20.565$（$n{=}2/3/4$），log–log 斜率 $0.151$（$\sqrt E$ 型应为 $0.5$）⇒ **上缘趋向有界**；$\sigma_{\min}/\sigma_{\max}=0.207\to0.039$；但 $\sigma>0.1\sigma_{\max}$ 占 $95.4\%$（$n{=}4$）⇒ 一个数量级内集中、**不是重尾**。
- **非单一幂律**：累积分布对数拟合指数 $2.05\to1.93$、残差 $\sim1$；$d_{\rm eff}=2\times$斜率 $=4.10/3.86$ 只是等效刻画，不能当 Debye 维数用。
- **有效模数**：$\mathrm{PR}/r=0.484\to0.450$ ⇒ 方差由约 $0.46r$ 个强模承担，前 $25\%$ 的模已贡献约 $2/3$。等权估计会高估 $\sigma_\varepsilon$ 约 2 倍。
- **对 `审-10` 的处置**：R97「截断＝谱支集端点」的**原则成立**（谱确有明确上缘），但**端点不是 $\Theta_D$**——$\Theta_D$ 属顶点位移（声子）扇区，该扇区对 $\varepsilon$ 的贡献由 R145 判为零。截断位置改为 $\omega_{\rm cut}=\sqrt{\sigma_{\max}/M_{\rm band}}$。Debye 模计数 $F(q)=(q/Q)^3$ 不能直接搬到非仿射扇区。
- **诚实边界**：$M_{\rm band}$（边基质量）与 $c_k^0$ 未给 ⇒ $\omega_{\rm cut}$、$\sigma_\varepsilon$ 的绝对值仍不可算；不判 $\omega_{\rm cut}$ 与 $\Theta_D$ 的大小（两者分属不同扇区）；$\mathrm{PR}/r$ 非材料无关常数（只算 BCC）；不闭合 `审-21`／`审-10`／`审-22`；不改 06；唯一编号仍 37、闭合数仍 0。
- **历史唯物主义**：组合复形与边长约束决定 $\tilde A$ 与其谱，谱上缘与有效模数是结构量、不随 $T$ 变；热占据只在既有模上分配权重，读数不反写谱。
- **交付**：`03_推导工作台/环04_非仿射刚度谱与截断位置.md`、`04_计算验证/环04_非仿射刚度谱.py`／`.png`／`.csv`／`_摘要.csv`（四组断言，四面板非拟合）、`05_Lean验证/NonAffineSpectrum.lean`（12 条，退出码 0、无警告、无禁用项）、`06_决策记录/2026-11-25_第137轮_非仿射刚度谱与截断.md`；同步主链环 4 缺口行／§11（`审-10`、`审-21` 注记）／§15／§16、口径表边界注记、缺口重审环 4、`成果登记.md` R-146。

**第 138 轮（环 4／`审-21` 结案：非仿射扇区无链内动力学；成果登记 R-147；2026-11-25）：**

- **判定（是定理，不是数值）**：顶点动能 $T_{\rm kin}=\tfrac12 m\sum_i|\dot x_i|^2$，边长速度 $\dot\ell=B\dot x\in\operatorname{im}B$。取 $\dot\ell\in N_I=(\operatorname{im}B)^\perp$，则 $|\dot\ell|^2=\langle B\dot x,\dot\ell\rangle=0$ ⇒ $\dot\ell=0$。**$N_I$ 中唯一可实现的速度是零**（$B^+|_{N_I}=0$、$M_\ell|_{N_I}=0$）。
- **数值**：$\|B^+v_{N_I}\|=8.5\times10^{-15}$（$n{=}3$）／$1.9\times10^{-14}$（$n{=}4$）；二次型 $1.2\times10^{-15}$／$2.7\times10^{-15}$；对照 $\operatorname{im}B$ 上 $8.95$／$14.72$。
- **后果**：$c_k^0=\hbar/(2\sqrt{\sigma_kM_k})$ 在 $M_k=0$ 处发散（$M=10^{-2}\to c^0=5$；$M=10^{-8}\to c^0=5000$）⇒ **(4.1″) 第一项不是有限物理量，撤销**。
- **(4.1″) 坍缩为缺陷一支**：$\langle(\Delta\varepsilon_e)^2\rangle_T=b\,n_d(T)$，$n_d=n_d^{(0)}+\nu e^{-E_c/k_BT}$。向错核心能 $E_c\sim\mu f^2b^3\ln(R/r_c)/[16\pi(1-\nu)]$：Al/Nb/Pb/V 在 $f=0.03$–$0.10$ 给 $E_c=0.7$–$16$ meV（$8$–$190$ K），室温 $n_d=0.53$–$0.97$、$\sigma_\varepsilon=0.18$–$0.54$ rad——**落在 06 的 $\varepsilon$ 带（$0.177/0.707/0.500$）内**。
- **但缺陷支不能单独承担 $T$ 依赖**：$T_c\sim1$–$20$ K 时 $n_d\sim e^{-5}$–$e^{-190}\approx0$（冻结），且「升温增缺陷」与链的「低温有序」（`审-4`）方向相反。故必须含**预存密度** $n_d^{(0)}$（冷加工、晶界、位错残留），它是材料输入。
- **`审-21` 判定（B 类）**：R73（位移盲）＋R145（顶点谱零贡献）＋本轮（无动能）三向合力 ⇒ **晶格几何不能产生 $\varepsilon$**。因果方向是「物质再生产 → $v_\tau$ → 几何表示 $\varepsilon$」；$\varepsilon$ 的统计是 FG／材料输入。工作台的行动项：**不再在链内寻找 $\varepsilon$ 的载体**。状态栏仍「未闭合」（按红线不升级）。
- **连锁登记**：R102（第 93 轮，环 17 的 $\mathcal D=3\hbar^2/k_BT$、$M_t\propto T^3$）用同一批非仿射模，也依赖 $M$，待 $M$ 定后复核；不改其状态。`审-22` 降级为「缺陷显式形式」。
- **历史唯物主义**：本轮判定的内容正是「几何不能产生 $\varepsilon$」——物质第一性、几何是表示。必然性（正交性与内积）／偶然性（$n_d^{(0)},E_c,\nu$）分层。未用社会范畴。
- **诚实边界**：不给 $\sigma_\varepsilon$ 绝对值；不解释 06 三值；不判超导机制；不闭合 `审-21`（判 B 类）；不改 06；唯一编号仍 37、闭合数仍 0。
- **交付**：`03_推导工作台/环04_非仿射无动力学与审21结案.md`、`04_计算验证/环04_非仿射无动力学与缺陷量级.py`／`.png`／`.csv`／`_摘要.csv`（断言全过，四面板非拟合）、`05_Lean验证/NonAffineDynamics.lean`（6 条，退出码 0、无警告、无禁用项）、`06_决策记录/2026-11-25_第138轮_非仿射无动力学与审21结案.md`；同步主链环 4 缺口行／§11（`审-21`、`审-22`）／§15／§16、口径表边界注记、缺口重审环 4、`成果登记.md` R-147。

**第 139 轮（环 5／`审-2` 后续：环 4→5→9 接口——$\varepsilon$ 的矩到 $v_\tau$ 的矩；成果登记 R-148；2026-11-25）：**

- **触发**：R147 判「链内不产生 $\varepsilon$」。那链的下游到底需要 $\varepsilon$ 的什么？只要 $(\bar\varepsilon,\sigma^2)$ 就够，还是需要分布形状？
- **一阶传递是恒等式，不是 Taylor 近似**：有理化 $\sqrt a-\sqrt b=(a-b)/(\sqrt a+\sqrt b)$ 给
  $$v_\tau(\varepsilon_0+\delta)-v_\tau(\varepsilon_0)=-\frac{\delta/2\pi}{v_\tau(\varepsilon_0+\delta)+v_\tau(\varepsilon_0)}.$$
  $\varepsilon_0=0.30$、$\delta=10^{-3}$ 时与线性式偏差 $4.2\times10^{-5}$。故 $v_\tau'=-1/(4\pi v_0)$ 精确成立。
- **$\kappa_f$ 的独立互检**：由上式 $\kappa_f=-v_\tau'/v_0=1/(4\pi v_0^2)=1/[4\pi(1-\varepsilon_0/2\pi)]$——**与 `审-2` 的 FG 推导逐字相同**。两条独立路线（对 (5.1) 求导 vs FG 几何）给同一个 $\kappa_f$。
- **矩传递**：$\mathrm{Var}(v_\tau)=\kappa_f^2v_0^2\sigma^2+O(\sigma^4)$、$\mathrm{Var}(\lambda_{ij})=2\kappa_f^2\sigma^2(1-\rho)$（即 (9.1)）；Jensen 给 $v_0-\langle v_\tau\rangle=\sigma^2/(32\pi^2v_0^3)+O(\mu_3)$（$\sigma\le0.05$ 时二阶偏差 $0.01\%$）。
- **鲁棒性判定**：三分布（截断高斯／均匀／Beta）同 $(\varepsilon_0,\sigma^2)$、`quad` 求积（区间限制＋重归一化，**无抽样噪声**）：$\mathrm{Var}(v_\tau)$ 的离散 0.02%／0.14%／1.83% ⇒ **二阶传递形状无关**。Jensen 三阶修正依赖 $\mu_3$（$\sigma\gtrsim0.03$ 三条误差曲线分道：$10^{-2}$／$10^{-12}$／$10^{-8}$）。环 15 的 $p_{\rm pair}$ **完全依赖分布族**（原隐含在 R90 的高斯假设里，现显式化）。
- **结论**：R147 **不伤害环 5 与环 9**（它们只用二阶矩）。受影响的只有 Jensen 三阶（$\sigma^4$ 量级，可忽略）与环 15 的尾概率。
- **诚实边界**：(5.1) 仍【假设】、未升格（本轮只证「给定 (5.1)，$v_\tau'$ 与 $\kappa_f$ 相容」）；$\sigma^2$ 与分布族仍材料／FG；Jensen 位移在 $\sigma\le0.05$ 时 $<10^{-5}$，不可直接观测；不改 06；不闭合任何编号。
- **历史唯物主义**：$\varepsilon$ 的统计（物质的实际缺陷／再生产结构，基础）决定 $v_\tau$ 的矩（读数），读数不反写统计；恒等式是必然性，$\sigma^2,\mu_3$ 与分布族是偶然性。
- **交付**：`03_推导工作台/环05_eps到vtau的矩传递与鲁棒性审计.md`、`04_计算验证/环04_eps到vtau的矩传递.py`／`.png`／`.csv`／`_摘要.csv`（四组断言，四面板非拟合）、`05_Lean验证/MomentTransfer.lean`（7 条，退出码 0、无警告、无禁用项）、`06_决策记录/2026-11-25_第139轮_eps到vtau的矩传递.md`；同步主链环 5 缺口行／§11（`审-2`）／§15／§16、口径表边界注记、缺口重审环 5、`成果登记.md` R-148。

**第 140 轮（环 15／`审-4` 后续：$p_{\rm pair}$ 的形状依赖与阈值敏感度——修正上一轮；成果登记 R-149；2026-11-25）：**

- **触发**：R148 判「环 15 的 $p_{\rm pair}$ 完全依赖分布族」。本轮一算，这句话在**阈值处**不成立。
- **Cantelli 界（分布无关）**：$E[z]=0$、$E[z^2]=v>0$ ⇒ $\Pr[z\ge k\sqrt v]\le1/(1+k^2)$（Lean `cantelli`，取 $\lambda=\sqrt v/k$ 用 $E[(z+\lambda)^2]=v+\lambda^2$）。界很松（因子 $10^4$），但证明形状**不能突破**它。
- **同 $(\mu,\sigma^2)$ 四分布**（$\mu=0.30,\sigma=0.05,n_{\rm cell}=10$，$2\times10^5$ 组）：

| 分布 | $\gamma_1$ | $p(r{=}1.5)$ | $p(r{=}2.0)$ | $p(r{=}3.0)$ |
|:--|--:|--:|--:|--:|
| 高斯 | 0.000 | 0.1417 | 0.0352 | $1.50\times10^{-3}$ |
| Gamma | 0.333 | 0.1457 | 0.0410 | $2.49\times10^{-3}$ |
| 对数正态 | 0.505 | 0.1498 | 0.0466 | $4.67\times10^{-3}$ |
| Beta | 0.316 | 0.1448 | 0.0387 | $2.29\times10^{-3}$ |

$r=2$ 处离散 **28.2%**。

- **阈值反解是关键的**：$p_c=0.592746$ 对应 $r\approx0.82$——**小于 1**，是样本方差的**左尾**。四分布要求的 $r$：高斯 0.8230／Gamma 0.8147／对数正态 0.7993／Beta 0.8160，$\sigma_c$ 最大只差 **1.5%**。
- **为什么差两个数量级**：右尾由重尾控制、对偏度极敏感；左尾被「方差固定」钉住，同方差分布在小值区形状相近。Edgeworth 核 $\partial p/\partial\gamma_1=-(z^2-1)\phi(z)/6$ 在 $z=0$ 最大 0.0665、$\pm1$ 过零。
- **判定（修正 R148）**：阈值判据对形状的敏感度 $\sim1.5\%$，与 $p_c$ 的 $1\%$ 精度同量级——**边缘，但不必引入分布族**。若链用低 $p$ 区（赝能隙 $p\sim0.03$），才必须给分布族（那里 28%）。`审-4` **不降级**，只加定量注记（不设新编号）。
- **历史唯物主义**：$\varepsilon$ 的分布（物质实际状态，基础）决定 $p_{\rm pair}$（连通读数）；Cantelli 是必然性，$1.5\%$／$28\%$ 是同方差族的结构事实，具体 $\gamma_1$ 是偶然性。**阈值判据对形状不敏感**说明宏观连通读数主要由二阶矩决定，不由分布细节决定。
- **诚实边界**：不给 $\sigma^2$、$\gamma_1$；$1\%$ 精度是参照不是链给的；Cantelli 界不作预测；不闭合 `审-4`／`M8`；不改 06；唯一编号仍 37、闭合数仍 0。
- **交付**：`03_推导工作台/环15_pair概率的形状依赖与阈值敏感度.md`、`04_计算验证/环15_pair概率的形状依赖.py`／`.png`／`.csv`／`_摘要.csv`（四段断言，四面板非拟合）、`05_Lean验证/PairProbabilityBound.lean`（2 条，退出码 0、无警告、无禁用项）、`06_决策记录/2026-11-25_第140轮_pair概率形状依赖.md`；同步主链环 15 缺口行／§11（`审-4`）／§15／§16、口径表边界注记、缺口重审环 15、`成果登记.md` R-149。

### 第 141 轮（2026-11-25）：相界斜率的链式法则修正与峰度通道

- **判定**：`环19_M8相界斜率.md` 沿相界求导漏 $\partial_Tp_{\rm pair}$（把 $p_{\rm pair}$ 写成只依赖掺杂）；严格式 $\frac{dT_c}{d\delta}=\frac{\partial_\delta p_{\rm pair}-\partial_\delta p_*}{\partial_Tp_*-\partial_Tp_{\rm pair}}$。偏读斜率/严格 $=1/r$，$r\in(0,1)$ ⇒ 系统性高估（正态基准 $9.47\%$，恒等式 $1/r-1$ 核到 $10^{-16}$）。
- **形状通道**：$DF_n=2n/[\kappa-(n-3)/(n-1)]$（O'Neill 2014）。固定交点下 $\partial_Tp_{\rm pair}$ 形状敏感 $60\%$–$70\%$、严格斜率离散 $48.7\%$ ⇒ **相界斜率需峰度输入**；R149 阈值位置判据不撤销。
- 入口：`03_推导工作台/环19_相界斜率链式法则修正与峰度通道.md`、`05_Lean验证/PhaseBoundarySlope.lean`（10 条，退出码 0）、`06_决策记录/2026-11-25_第141轮_相界斜率链式法则修正.md`、R-150。

### 第 142 轮（2026-11-25）：环 17 扩大动力学的三重链式漏项与自洽反馈

- **三重漏项**：(17.1) 的 $N_t-1$ 是组合数导数 $N_t-\tfrac12$ 的连续近似（相对误差 $1/(2N_t-1)$，$N_t\to1$ 时误给零）；$p$ 只列 $\sigma_\ell$ 一条路径（若沿用环 15 的 $p$ 须补 $p_T\dot T$）；(6.6) 的 $\mathcal D_{\rm new}-\mathcal D$ 是零均值对差特例，非零均值 $\ell$ 的通量须含 $K=(s_{\rm new}^2-s^2)+(\mu_{\rm new}-\mu)^2$。
- **自洽反馈**：$g(2s-CK)=CA$ ⇒ $g=CA/(2s-CK)$、$g_0/g=1-\eta$（$\eta=CK/(2s)$）；$0<\eta<1$ 时偏读低估（示意外放大 $3.441$ 倍），$\eta\to1$ 为隐函数失效面——**反馈型上限**，不同于环 18 的资源／几何上限。
- **审-6 深化**：截断正态下 $K/s^2=a\lambda(a)$；右尾（配对支）正反馈、左尾（骨干支）负反馈 ⇒ 同一个 $p$ 读数不能定 $\dot M_t$，变量错位实为机制错配。
- **边界**：不给材料值；截断矩为 B 类前提；(17.1) 原文／(17.2) 结构未改；不闭合编号，唯一编号仍 37、闭合数仍 0。
- 入口：`03_推导工作台/环17_扩大动力学的三重链式漏项与自洽反馈.md`、`04_计算验证/环17_扩大反馈自洽与矩通量.py`（+png/摘要）、`05_Lean验证/ExpansionFeedback.lean`（14 条，退出码 0）、`06_决策记录/2026-11-25_第142轮_环17扩大反馈自洽.md`、R-151。

- **第 143 轮（R-152）材料入口判定**：$A$ 的 $\mathcal B^\pm$ 桥**否证**——$\varepsilon(\lambda\ell)=\varepsilon(\ell)$ ⇒ $L\ell=0$，仿射驱动 $\dot\ell=\mu\ell$ 给 $A=2\mu s^2>0$ 而 $\dot\varepsilon=0$；合法形式为 $\dot\ell=\mu\ell+\delta\dot\ell$ 的仿射／非仿射两路。$p_s$ 桥**接通（条件于采用环 15 尾式）**：$p_s=\epsilon_\nu p/s$、$\epsilon_\nu=2xh_\nu(x)$，$\eta=\frac{2N-1}{2(N-1)}\epsilon_\nu a\lambda(a)$，$\nu=9$、$p_c$ 处 $a_\ast=0.3686$——反馈失效面可在阈值处即触发，第 142 轮读样式弹性 $\epsilon_{\rm ad}<1$ 掩盖了它。
- 入口：`03_推导工作台/环17_材料入口A与ps的可通桥判定.md`、`04_计算验证/环17_材料入口的可通桥.py`（+png/摘要）、`05_Lean验证/MaterialBridge.lean`（16 条，退出码 0）、`06_决策记录/2026-11-25_第143轮_环17材料入口的可通桥.md`、R-152。

- **第 144 轮（R-153）两个 $\mu$ 分离与热膨胀入口**：R-152 留的两个入口再判——$\tilde AB=0\Rightarrow\forall\dot x$ 下 $\dot\varepsilon=0$，且 $\delta\dot\ell\in\operatorname{im}B$ 使上一轮 $\dot\varepsilon=\tilde L\delta\dot\ell$ 恒零（非仿射支归 FG）；环 16 $\mu_{(16)}=\partial\lambda/\partial n$（$1/[\text{点数}]$）与环 17 $\mu_{(17)}=\dot\ell/\ell$（$1/[\text{时间}]$）量纲不同、符号撞车。$\mu_{(17)}=\bar\gamma C_V\dot T/(3K_TV)$（Grüneisen）给 $A_{\rm aff}$ 第一性材料式，纯谐 $\bar\gamma=0$ 对偶于亏角零次齐次，低温 $\mu\propto T^3\to0$；$\sigma_c$ 绝对／相对口径分叉（绝对下 $p\uparrow:0.593\to0.820$、相对下不变），链内未定。所有编号不闭合。
- 入口：`03_推导工作台/环17_两个mu的分离与热膨胀材料入口.md`、`04_计算验证/环17_两个mu与热膨胀入口.py`（+png/摘要）、`05_Lean验证/TwoMus.lean`（13 条，退出码 0）、`06_决策记录/2026-11-25_第144轮_两个mu的分离与热膨胀入口.md`、R-153。

- **第 145 轮（R-154）$\sigma_c$ 口径判定与两个方差分离**：接 R-153 的"口径未定"。相对口径 $\sigma_c^2=\rho V$ 给 $dp/dT=0$、无唯一 $T_*$，否证；链内只剩绝对口径，反解 $\sigma_c^2=x_\ast Z/n_{\rm cell}$（$\nu=9,p_c$ 给 $x_\ast=7.4271$、$\sigma_c^2/Z=0.8252$），$Z,n_{\rm cell},t$ 外生。$V_{\rm coh}=Zw(T)$（随升温减）与 $s^2=\operatorname{Var}(\ell)$（随升温增）为不同随机变量，$\partial p/\partial s=0$——R-152 的 $p_s=\epsilon_\nu p/s$ 为对象错配（`审-6` 第三层）。$g=\epsilon_\nu\dot w/w$ 外生、无 $s$ 自洽回路，可解 $ga\lambda+2\mu>0$，失效 $a_\ast\lambda=r=2\mu/|g|$（材料率比，R-152 普适 $a_\ast=0.3686$ 撤销），尾部符号依赖 $\operatorname{sgn}(\dot T)\operatorname{sgn}(a)$。所有编号不闭合。
- 入口：`03_推导工作台/环15_sigma_c口径的链内判定与两个方差的分离.md`、`04_计算验证/环15_sigma_c口径与两个方差.py`（+png/摘要）、`05_Lean验证/SigmaCThreshold.lean`（21 条，退出码 0）、`06_决策记录/2026-11-25_第145轮_sigma_c口径与两个方差.md`、R-154。

- **第 146 轮（R-155）符号回修与可测失效判据**：接 R-154 两外生率，先回修 R154.5——原「可解 $ga\lambda+2\mu>0$」与「失效 $|g|a\lambda>2\mu$」矛盾，物理可解 $s>0$ 在升温 $g<0$ 时要求 $a\lambda>r=2\mu/|g|$（$a\lambda\downarrow r^+$ 才发散、$a\lambda\le r$ 无物理解），降温恒可解。$\dot T$ 约掉给可测判据 $r(T)=2\alpha_V/(3\epsilon_\nu|d\ln w/dT|)$，与扫描速率无关；低温绝缘体 $r\propto T^2\to0$、金属常数、高温 $r\propto T$。超导温区 $r$ 极小（示意 $3.9e{-8}\ll a\lambda(0.5)=0.571$），反馈发散材料不可达、瓶颈为 $A\to0$ 无生产源（R-144）——两种失效源低温分离。所有编号不闭合。
- 入口：`03_推导工作台/环17_R154符号回修与可测失效判据.md`、`04_计算验证/环17_可测失效判据.py`（+png/摘要）、`05_Lean验证/MeasurableFailure.lean`（19 条，退出码 0）、`06_决策记录/2026-11-25_第146轮_可测失效判据与符号回修.md`、R-155。

### 第 147 轮（R-156）：$t$ 与 $Z$ 的同源材料桥、R154.2 漏项与 $Z$ 同名判否

- **回修**：R-145 (R154.2) 乘回 $w(T_c)$：$\sigma_c^2/Z=x_\ast w(T_c)/n_{\rm cell}$；$\epsilon_\nu=2.5929$ 不变。
- **$Z$ 接通**：$Z=\frac38c_\varepsilon^2\hbar\omega_D/(Mc_s^2)=\frac12c_\varepsilon^2Q^2\langle u^2\rangle_0$，与 $\omega_D$、$\lambda$ 同源；$Z/\lambda=\hbar\omega_D/[4N(0)zg^2(1-\rho)]$，FE10 与环 10 差 $1/z$。
- **判否**：$Z_{\rm chain}\sim10^{-4}$–$10^{-3}\ll Z_{\rm el}=1+\lambda=O(1)$——同名不同物，`审-6` 第四层错配；谱矩自洽只在 $\lambda\propto Z$ 层面。
- **$t$ 不可材料化**：渗流普适指数，只经 $\epsilon_\nu(t)$ 入 $r$；$r_{\rm low}\propto T^2$、$r_{\rm high}\propto T$ 的闭式不含 $Z$。
- 入口：`03_推导工作台/环17_t与Z的同源材料桥与Z同名判否.md`、`04_计算验证/环17_t与Z的同源材料桥.py`（+png/csv）、`05_Lean验证/MaterialBridgeTZ.lean`（19 条，退出码 0）、`06_决策记录/2026-11-25_第147轮_t与Z同源材料桥.md`、R-156。

### 第 148 轮（R-157）：$A$ 源的静态 no-go、扫描奇偶性与可解域统一判据

- **静态 no-go**：$A=2\operatorname{Cov}(\ell,\dot\ell)=d(\operatorname{Var}\ell)/dt$ 是**导数**；$Z$、冻结缺陷 $n_d^{(0)}$ 等静态分量率贡献恒零。R-147 的「缺陷／$Z$ 桥给非零 $A$」**判否**；激活支 $\propto(E_c/T^2)e^{-E_c/k_BT}\dot T$ 低温指数冻结且属 `审-22` 扇区。
- **扫描奇偶**：$g,\mu,A$ 全正比于 $\dot T$，反向使三方同时变号、方程不变 ⇒ $s(-\dot T)=s(\dot T)$，与扫描速率／方向均无关。
- **回改 R-155**：物理降温 $\mu<0$，「降温恒可解」撤销；统一材料率比 $r=2\alpha_Vw/(3\epsilon_\nu|w'|)$ 给 $s=2/[C(a\lambda-r)]$、**升降同判据** $s>0\iff a\lambda>r$。
- **低温**：绝缘体 $r\propto T^2\to0$ ⇒ $s\to2/(Ca\lambda)$ 有限，$A\to0$ 非瓶颈；$T_x$（$r=a\lambda$）是适用域边界，不是 $T_c$（$T_c$ 仍走刚度）。
- 入口：`03_推导工作台/环17_A源与扫描奇偶性.md`、`04_计算验证/环17_A源与扫描奇偶性.py`（+png/json，九段断言）、`05_Lean验证/ASourceScan.lean`（20 条，退出码 0）、`06_决策记录/2026-11-25_第148轮_A源与扫描奇偶性.md`、R-157。

### 第 149 轮（R-158）：`审-6` 的锁定因子桥与 `审-4` 三量的界

- **`审-6` 可接处唯一＝锁定因子**：$p_{\rm sync}=p_{\rm pair}\,p_{\rm lock}$（$0\le p_{\rm lock}\le1$）是边事件分解，不是对象同一；配对属振幅扇区、锁定属相位扇区，自由能可分离（环 9／环 19）⇒ R-151／152／154／156 四层同名错配不复现；二阶段 $T_{\rm sync}\le T_{\rm pair}$。
- **锁定因子＝涡旋逸度**：$1-p_{\rm lock}=y=2\pi e^{-E_c/(k_BT)}$、$E_c=\pi^2\Upsilon/2$（外部 XY 核能标准值），只用形状与极限，$E_c$ 外生。
- **$t$ 的定义式（回写 R-44／143／145／156）**：$t=1+\ln(1-y)/\ln p_{\rm pair}\ge1$；$t(0)=1$、有限温严格 $>1$；BKT 裸交点给 $y(T_c)\le0.02501$（与 $\Upsilon$ 无关）⇒ $t(T_c)\le1.0509$（$m=1$）／$1.1072$（$m=2$），$m$ 未定。
- **阈值与 $\epsilon_\nu$ 重算**：$p_{\rm pair}^{\rm thr}=p_c/(1-y)^m\ge p_c$；$\nu=8,t=1.0509$ 给 $\epsilon_\nu=2.3290$（$-10.2\%$）、$\nu=8,t=1$ 给 $2.4293$，R-145／R-156 的 $2.5929$（$\nu=9$）对 BCC 应替换。
- **`审-4` 三量**：$n_{\rm cell}=z^2/\sum\rho_{ee'}^2\in[1,z]$（BCC $z=8$ 容不下 $\nu=9$）；$Z$ 形式闭合、绝对值判 B 类；$T_c$ 仍走 $\Upsilon(T_c)=\Upsilon_c$。
- 入口：`03_推导工作台/环15_审6同步概率的锁定因子与审4三量的界.md`、`04_计算验证/环15_审6锁定因子与t的界.py`（+png/json，七段断言）、`05_Lean验证/SyncLockBridge.lean`（3 定义＋11 定理，退出码 0）、`06_决策记录/2026-11-25_第149轮_审6锁定因子与审4三量的界.md`、R-158。

### 第 150 轮（R-159）：逸度通道判定、R-158 §四笔误修正与 $t(T)$ 温度单调性

- **R-158 §四两处笔误已就地修正（数值不变）**：裸交点方向应为 $k_BT_c/\Upsilon_{\rm bare}(T_c)\le\beta_{\rm KT}$（非 $\beta_{\rm KT}^{-1}$）、$y_{\rm crit}$ 指数应为 $\pi^2/(2\beta_{\rm KT})$（非 $\pi^2\beta_{\rm KT}/2$，后者给 $0.076642$）；$0.02501$、$1.0509$／$1.1072$ 全不变——脚本／Lean／图本就用正确式，属文字对齐数值。
- **逸度通道**：$p_{\rm lock}$ 用热有效 $y=2\pi e^{-E_c^{\rm eff}/(k_BT)}$、$E_c^{\rm eff}=\frac{\pi^2}{2}\Upsilon_0w(T)$；涡旋固定点 $y_R=2\pi e^{-\pi}=0.2715$（$\Upsilon_R=\frac{2}{\pi}k_BT_c$）不用于 $p_{\rm lock}$（差 $10.86$ 倍）；R-158 取 $\Upsilon_{\rm bare}$ 正确，非遗漏重整化。
- **$t(T)$ 温度单调性（数值判定）**：精确 Debye $w(T)$＋卡方配对尾，$\gamma=\Upsilon_0/\omega_D\in\{1,1.5,2\}$ 下 $y\uparrow$、$p_{\rm pair}\downarrow$、$t\uparrow$，$t(0^+)=1$、$t(T_{\rm sync})=1.050888$（与 R-158 精确一致）⇒ $t(T)\le1.0509$ 覆盖整个同步区 $[0,T_{\rm sync}]$（判定非假设；$T>T_{\rm sync}$ 正常相不套用）。
- **log 导数判据** $d(t-1)/dT\gtrless0\iff\delta'L-\delta L'\gtrless0$，数值一致率 $1.0$，离散代数由 Lean `ratio_step_ge` 承载。
- 入口：`03_推导工作台/环15_逸度通道判定与t温度单调性.md`、`04_计算验证/环15_逸度通道与t温度单调性.py`（+png/json，六面板断言）、`05_Lean验证/TChannelMonotone.lean`（1 定义＋7 定理，退出码 0）、`06_决策记录/2026-11-25_第150轮_逸度通道判定与t温度单调性.md`、R-159。

### 第 151 轮（R-160）：$w(T)$ 与实验刚度的对应域判据

- **读出映射是两级的**：$\Upsilon=\frac{\hbar^2}{4\mu_0e^2}d\lambda_L^{-2}=\frac{\hbar^2}{2\mu_0e^2}\Lambda^{-1}$（Pearl 长度 $\Lambda=2\lambda_L^2/d$）。报告"$\lambda$"读作 $\Lambda$ 与读作 $\lambda_L$ 差 $2x/d=\Lambda/\lambda_L$（$c_\Lambda=2$：$352.67$／$160.0$／$60.0$，$d=3/5/10$ nm；原记 $176.33$／$80.0$／$30.0$ 属 $c_\Lambda=1$，第 152 轮统一）——这是对应域第一道界，纯代数。
- **BKT 无参数线**：$\Lambda(T_c^-)=C_\Lambda/T_c$，$C_\Lambda=19.612$ mm·K。被 $\epsilon_v>1$ 与无序展宽抹平，容差 $O(1)$–$2$，不得当可调参数。
- **形状判别**：$w$ 的低温耗竭是 $T^2$（斜率 $1.99994$，系数 $\pi^2/3$），与中性 2D 超流的 $T^3$、无序 2D 超导较高温段的 $T$ 线性都不同；莫尔近 $T^2$ 属几何刚度，机制不同，不互证。
- **双边界**：$\Upsilon_R\le\Upsilon_0w$ 与 $\Upsilon_R\ge\frac{2}{\pi}k_BT$ ⇒ $r(T)\equiv\Upsilon_R/\Upsilon_R(T_c^-)\ge T/T_c$（唯一无参数判据；上界含外生 $\Upsilon_0$）。最小 $\Upsilon_0$ 下带为 $\frac{T}{T_c}w(T_c)\le\Upsilon_R/\Upsilon_0\le w(T)$，凹性保非空。
- **$\omega_D$ 下界**：线性耗竭 $cT$ 要求 $T\le T^*=3c\omega_D^2/\pi^2$，即 $\omega_D\ge\pi\sqrt{T_{\rm lin}/(3c)}$；软模与延伸线性不相容（$c=0.1$ 时 $T^*/T_c=0.274/3.04/27.4$）。
- **可辨识性**：$w(0)=\Phi(0)=1$ 钉住 $\Upsilon_0=\Upsilon(0)$；$T>0$ 只给乘积 $w\Phi$，故 $w$ 通道的可证伪内容即 $\Upsilon(T)\le\Upsilon(0)w(T)$。
- **分域**：$\mathcal{B}=T_c\Lambda(0)/C_\Lambda\le1$，$\mathcal{B}\to1$ 为 BKT 主导、$\mathcal{B}\ll1$ 为振幅主导；NbN 样例两种读法均 $\ll1$，其 $T_c$ 不由 BKT 定。
- **边界**：全为必要条件，不闭合任何编号，`审-4`／`审-6` 与 $T_c$ 路径不动；唯一编号仍 37、闭合数仍 0。
- 入口：`03_推导工作台/环19_w温度与实验刚度的对应域判据.md`、`04_计算验证/环19_w与刚度对应域.py`（+png/json，六段断言）、`05_Lean验证/StiffnessReadout.lean`（6 定理，退出码 0）、`06_决策记录/2026-11-25_第151轮_w温度与实验刚度的对应域.md`、R-160。

### 第 152 轮（R-161）：Pearl–London 口径统一

- **两种约定并存**：$\Lambda=c_\Lambda\lambda_L^2/d$，$c_\Lambda\in\{1,2\}$——Pearl 原始定义用 $2$（L152b），薄膜 SQUID 线性响应用 $1$（L152c）。引用"Pearl 长度数值"必须声明 $c_\Lambda$，否则不可比。
- **刚度只依赖组合**：$\Upsilon=\frac{\hbar^2}{4\mu_0e^2}d\lambda_L^{-2}=\frac{C_\Upsilon c_\Lambda}{\Lambda}$，$C_\Upsilon=\hbar^2/(4\mu_0e^2)=8.619\times10^{-26}$ J·m；只测刚度不能分离 $\lambda_L$ 与 $d$。
- **无约定读法**：片动能电感 $L_{k\square}=\mu_0\lambda_L^2/d$，$\Upsilon=\frac{\hbar^2}{4e^2L_{k\square}}=\frac{\Phi_0^2}{4\pi^2L_{k\square}}$（L152d 同式；微波直测 L152e／L152g）。对应域判据一律写成此式。
- **更正第 151 轮因子 2**：两读法之比为 $c_\Lambda x/d$；$c_\Lambda=2$ 给 $352.67$／$160.0$／$60.0$（$d=3/5/10$ nm），第 151 轮原记 $176.33$／$80.0$／$30.0$ 属 $c_\Lambda=1$ 约定（已同步更正卡、决策记录、口径表与脚本）。
- **简并**：$(\lambda_L,d)\mapsto(s\lambda_L,s^2d)$ 使 $\Upsilon$ 不变；文献同报二者必另有独立 $d$（死层修正约 $25\%$，L152f）。
- **应用域**：$L_{k\square}\to\lambda_L$ 需局域极限 $\xi\ll\lambda_L$（L152e）；$L_{k\square}\to\Upsilon$ 无须该极限。
- **BKT 线无约定形式**：$L_{k\square}(T_c^-)=\pi\hbar^2/(8e^2k_BT_c)$（$10$ K 给 $1.233$ nH/方），$\mathcal{B}=L_{k\square}(0)/L_{k\square}^{\rm BKT}(T_c)$ 与 $c_\Lambda$ 无关。
- **边界**：只做口径统一，不产生新物理已证结论；不改 (19W.2)–(19W.10)、不闭合任何编号；唯一编号仍 37、闭合数仍 0，`审-4`／`审-6` 仍「未闭合」。
- 入口：`03_推导工作台/环19_Pearl与London口径统一.md`、`04_计算验证/环19_PearlLondon口径统一.py`（+png/json，六段断言）、`05_Lean验证/PearlLondon.lean`（5 定理，退出码 0）、`06_决策记录/2026-11-25_第152轮_Pearl与London口径统一.md`、R-161。

### 第 153 轮（R-162）：非局域区与 $q\to0$ 外推

- **刚度是 $q=0$ 量、片电感不是**：刚度取响应核 $K(\mathbf q)$ 的 $\mathbf q=0$ 分量；穿透深度由非局域 London 方程解定义；动能电感测的是依赖 $K(\mathbf q)$ 与边界条件的有效穿透深度（L153a）。故 (19PL.3) 只在 $q\to0$ 严格。
- **$q^2$ 修正**：Gaussian 层相位刚度与 $q$ 无关，积分掉 Gaussian 振幅涨落（L153b）后得 XY 作用量、刚度＝自由能对 $q$ 二阶导 ⇒ $\Upsilon(q)=\Upsilon(0)[1-A(q\xi)^2+O(q^4)]$，$A>0$（常规 s 波）。$A$ 外部核定，链内不预测。
- **方向单向**：$L_{k\square}(q)/L_{k\square}(0)=1/(1-A(q\xi)^2)\ge1$ ⇒ 有限 $q$ 高估片电感、低估刚度、低估 $T_{\rm BKT}$；三处同向，不是双向噪声。
- **单向界**：$\mathcal{B}\le L_{k\square}(q)/L_{k\square}^{\rm BKT}(T_c)$；NbN 两样例 $0.0667\to0.0741/0.0953$、$1.89\times10^{-4}\to2.10\times10^{-4}/2.70\times10^{-4}$（10%/30%），仍 $\ll1$ ⇒ D3 判定稳健；仅 $\mathcal{B}\to1$ 时有判别风险。
- **外推判据**：$A(q\xi)^2\le\epsilon\iff q\xi\le\sqrt{\epsilon/A}$；$A=0.5/1/2$ 时 $\epsilon=1\%$ 给 $0.141/0.100/0.0707$、$10\%$ 给 $0.447/0.316/0.224$、$30\%$ 给 $0.775/0.548/0.387$。
- **适用域三分**：I 局域 $q\xi\ll1$ 且 $d\ll\lambda_L$；II 准局域 $q\xi\lesssim1$（单向界＋修正）；III 非局域 $q\xi\gtrsim1$（须完整核）。$d\ll\lambda_L$ 属 Pearl 区（R-161），与 $q\xi\ll1$ 是两条独立条件。
- **边界**：只补读数适用域，不产生新物理已证结论；不改 (19PL.*)／(19W.*)、不闭合任何编号；唯一编号仍 37、闭合数仍 0，`审-4`／`审-6` 仍「未闭合」；$A<0$ 时不等号反向、本链不覆盖。
- 入口：`03_推导工作台/环19_非局域区与q0外推的刚度字典.md`、`04_计算验证/环19_非局域刚度字典适用域.py`（+png/json，六段断言）、`05_Lean验证/NonlocalStiffness.lean`（5 定理，退出码 0）、`06_决策记录/2026-11-25_第153轮_非局域区与q0外推.md`、R-162。

### 第 154 轮（R-163）：$\sigma_c$ 相界反解与 $\Phi(T)$ 链内形状

- **断口**：现行 $\sigma_c$ 定标用已被降级的 $p_{\rm pair}(T_c)=p_c^{1/t}$；$x_\ast=7.427075$、$\nu=9$ 隐含 $t=1$，给 $\Phi_c=0$、$\Upsilon_{\rm eff}(T_c)=0$，与 BKT 下界 $\frac{2}{\pi}k_BT_c>0$ 矛盾（$0$ vs $0.190986$）。
- **回改**：按 (19P.25) 反解——$\kappa=2k_BT_c/(\pi\Upsilon_{\rm bond}w_c)\in(0,1]$、$\Phi(p_*)=\Phi(p_{\rm pair}(T_c))=\kappa$、$x_c=\bar F_\nu^{-1}(p_*)$、$\sigma_c^2=x_cZw_c/\nu$；$\kappa=0.05$–$0.95$ 给 $\sigma_c^2/Z=0.183$–$0.626<0.626$ 旧值，BKT 下界自动满足。
- **$w\Phi$ 可分**：$\Phi$ 的 $T$ 依赖只经 $w(T)$，$\Upsilon(T)/\Upsilon(0)=G(w(T))$ 为单函数；$\Phi/\Phi_0=[\Upsilon/\Upsilon(0)]/w$。低温 $\Upsilon/\Upsilon(0)=1-\frac{\pi^2}{3}(1+B)(T/\omega_D)^2+O(T^4)$、$B>0$，首次把 Debye 通道（$1$）与渗流通道（$B$）显式分离；$\kappa\to1$ 时 $B\to0$、系数 $\to\pi^2/3$，$\kappa\to0$ 时放大。
- **边界**：不改 $T^2$ 幂次、不认作外部 $b\sim1.6$–$3$；$B$ 数值依赖分布族；不闭合任何编号、不改状态栏，唯一编号仍 37、闭合数仍 0。
- 入口：`03_推导工作台/环19_sigma_c相界反解与Phi链内形状.md`、`04_计算验证/环19_sigma_c相界反解与Phi形状.py`（+png/json，七段断言）、`05_Lean验证/PercolationStiffnessShape.lean`（9 定理，退出码 0）、`06_决策记录/2026-11-25_第154轮_sigma_c相界反解与Phi链内形状.md`、R-163；文献 L43–L45 只作外部对照。

### 第 155 轮（R-164）：Uemura 闭合与 $g_{\rm ren}$ 热力学反演

- **回改**：第 154 轮用裸 BKT 交点；真实跳变含涡旋重整化 $g_{\rm ren}$ ⇒ $\Phi_c=\kappa/g_{\rm ren}$、可行性收紧为 $\kappa\le g_{\rm ren}\le1$，$p_*=p_c+(1-p_c)(\kappa/g_{\rm ren})^{1/t_\Upsilon}$；第 154 轮数值表只对 $g_{\rm ren}=1$ 有效。
- **拉通**：$g_{\rm ren}$ 在 Uemura 恒等式 (U.1) 中精确抵消，单测 $(T_c,U(0))$ 定不出它；引入低温曲率 $c_2=a(1+B(x_c))$（$B$ 单调可逆）得闭合反演 $(T_c,U(0),\omega_D,c_2)\to x_c\to\Phi_0\to\Upsilon_0\to\kappa\to g_{\rm ren}$，外部输入仅 $(\nu,t_\Upsilon,p_c)$，无拟合自由度；恢复误差 $\le8.9\times10^{-16}$。
- **可证伪交叉检验**：热力学反演的 $g_{\rm ren}$ 与 RG 分离点 $g_{\rm ren}^{\rm RG}=(2/\pi)/K_c$ 是两条独立通路，不相等即否证因子化或某一读法。
- **边界**：不闭合任何编号、不改状态栏，唯一编号仍 37、闭合数仍 0；`临-25` 动态方程仍开放。
- 入口：`03_推导工作台/环19_Uemura闭合与g_ren热力学反演.md`、`04_计算验证/环19_Uemura曲率反演.py`（+png/json，七段断言）、`05_Lean验证/UemuraCurvatureInversion.lean`（7 定理，退出码 0）、`06_决策记录/2026-11-25_第155轮_Uemura闭合与g_ren反演.md`、R-164；文献 L46–L47 只作外部标准。

### 第 156 轮（R-165）：`审-4` 关联阈值接入相界与反演

- **座/键近阈等价**：$\Phi_b(q(p))/\Phi_s(p)\to C_{sb}=(2p_c/(1+p_c))^{t_\Upsilon}=0.681205$ 是常数，可吸收进外生 $\Upsilon_0$ ⇒ 临界区两写法同指数、同相界结构，只差归一；全局仍不可互换。
- **接入相界**：$p_c^{\rm eff}=p_c(0)-\bar c/(2p_c(0))$ ⇒ $p_*=p_c^{\rm eff}+(1-p_c^{\rm eff})(\kappa/g)^{1/t_\Upsilon}$、$x_c=\bar F_\nu^{-1}(p_*)$、$\Phi_c=\kappa/g$ 不变；$\delta>0\Rightarrow x_c\uparrow\Rightarrow\sigma_c^2\uparrow$。
- **可测偏差**：忽略关联的反演 $g$ 有正偏差 $\Delta g/g\approx7.7\delta$（$\delta=0.02$ 给 $+0.146\%$），用 $p_c^{\rm eff}$ 精确恢复；$8.03\times10^{-5}>4.13\times10^{-5}$（舍入残差）⇒ 关联效应可被两通路交叉检验分辨。
- **边界**：不闭合任何编号、不改状态栏，唯一编号仍 37、闭合数仍 0；$\rho$ 归一仍开放。
- 入口：`03_推导工作台/环15_审4_关联阈值接入相界与反演.md`、`04_计算验证/环15_审4关联阈值接入相界.py`（+png/json，七段断言）、`05_Lean验证/CorrelationSiteBond.lean`（5 定理，退出码 0）、`06_决策记录/2026-11-25_第156轮_审4关联阈值接入相界.md`、R-165；文献 L48 只作外部方向对照。

### 第 157 轮（R-166）：$\rho$ 链内归一与载体维数判别

- **归一**：诱导键共享节点 ⇒ $r=a$、$Qa=\pi$，$\rho_{nn}(m)=(m+1)\int_0^1u^mJ_0(\pi u)du$——$\rho$ 从连续外生数值降为链内 Bessel 形状＋离散载体 $m$＋链内几何。
- **接入**：$\bar c=\rho_{nn}\phi(z)^2$、$\delta=\bar c/(2p_c)$；$m=1/2/3/4$ 给 $\rho_{nn}=+0.181/+0.049/-0.031/-0.084$、$\delta=+0.0230/+0.0062/-0.0040/-0.0106$。
- **判别**：由第 156 轮 $\Delta g/g\approx7.7\delta$ 得符号对应；幅度全大于舍入残差，零穿越 $m^\*=2.556$ 在 2D（$m=2$）与 3D（$m=3$）之间 ⇒ 偏差符号可判别载体，第 86 轮维数待定化为可测离散选择。
- **边界**：不闭合任何编号、不改状态栏，唯一编号仍 37、闭合数仍 0；载体实现仍外生。
- 入口：`03_推导工作台/环04审4_rho归一与载体维数判别.md`、`04_计算验证/环04审4_rho归一与载体判别.py`（+png/json，七段断言）、`05_Lean验证/RhoNormalization.lean`（5 定理，退出码 0）、`06_决策记录/2026-11-25_第157轮_rho归一与载体判别.md`、R-166；文献 L49 只作标准工具。

### 第 158 轮（R-167）：$G(y)$ 高温截断与 $t_\Upsilon$ 出口

- **有限支撑**：$y_*=x_cw_c/\bar F_\nu^{-1}(p_c^{\rm eff})$，$G(y)=0\ (y\le y_*)$；$w(T_*)=y_*$ 定连通温度，$T_c<T_*$（(19P.22) 严格化）。工作点 $y_*=0.459693$、$T_*=0.651929\,\omega_D>T_c=0.3\,\omega_D$。
- **截断出口**：$\Upsilon(T)/\Upsilon(0)\propto(T_*-T)^{t_\Upsilon}$，数值指数 $1.29353/1.29948/1.29995\to1.3$；$G'\to0$、$G''$ 发散。
- **两通路判据**：低温曲率与高温截断各给一个 $x_c$，相等为一致性判据（工作点均 $4.500000$），与 $g_{\rm ren}$ 交叉检验独立。$T_c<T<T_*$ 对应赝能隙残余刚度窗口（L50，仅对照）。
- **边界**：不闭合任何编号、不改状态栏，唯一编号仍 37、闭合数仍 0；$T_*$（连通）与 $T^*$（振幅）是不同对象。
- 入口：`03_推导工作台/环19_G_y高温截断与载体出口.md`、`04_计算验证/环19_G高温截断.py`（+png/json，七段断言）、`05_Lean验证/HighTCutoff.lean`（5 定理，退出码 0）、`06_决策记录/2026-11-25_第158轮_G高温截断.md`、R-167；文献 L50 只作方向对照。

### 第 159 轮（R-168）：锁定整数与 $E_c$／$\gamma$ 反演

- **$m_{\rm lock}=1$**：诱导键每对节点只有一条 ⇒ 只需一条键无涡旋；R-158 的"全星" $m=2$ 属节点级条件用于边级渗流，排除 ⇒ $t(T_c)\le1.0509$ 为唯一分支。
- **两尺度细化**：$p_{\rm pair}>p_c/(1-y)>p_c$ ⇒ $T_c\le T_{\rm sync}<T_*$（工作点 $0.3<0.627385<0.651929$）。
- **$E_c$／$\gamma$**：L51 裸刚度 $E_c=\pi^2\Upsilon_0/2$ 接第 155 轮反演 ⇒ $E_c=\pi^2U(0)/(2\Phi_0)$、$\gamma=U(0)/(\Phi_0\omega_D)$（工作点 $3.207211$／$0.649917$）；误用重整化刚度给 $y=0.271521>0.025007$ 违反 BKT 界。
- **边界**：不闭合任何编号、不改状态栏，唯一编号仍 37、闭合数仍 0；推 6 与材料先验值仍开放。
- 入口：`03_推导工作台/环15锁定整数与E_c反演.md`、`04_计算验证/环15锁定整数与Ec反演.py`（+png/json，七段断言）、`05_Lean验证/LockIntegerAndCore.lean`（5 定理，退出码 0）、`06_决策记录/2026-11-25_第159轮_锁定整数与Ec反演.md`、R-168；文献 L51 只作外部标准。

### 第 160 轮（R-169）：$T^*$ 上界与同位素端点盲测（预注册 R12）

- **P1（A 类，通过）**：9 元素实测 $\alpha$ 全落 $[0,0.5]$，越界 0；链内同位素端点分类未被否证。
- **P2（B 类，通过）**：三独立参数系统 $T^*=0.95653\,\omega_{\log}e^{-(1+\lambda)/\lambda}$ 给 $6.3257/14.5060/50.3397$ K，全部 $\ge T_c^{\rm exp}$（$1/4/39$ K）。
- **P3（B 类，通过）**：余量随 $\lambda$ 严格减（Spearman $r=-1$）；P4 登记 MgB2 外部 $\alpha\approx0.3$ 属须 $\mu^\ast$ 链外成分。
- **边界**：$\omega_{\log}$ 跨定义差 $e^{1/6}$，P2/P3 为 B 类、不升格、不声称绝对 $T_c$；不闭合任何编号，唯一编号仍 37、闭合数仍 0。
- 入口：`07_数据与现象/预注册判定_R12.md`（判据跑数前写死）、`04_计算验证/R12_T星上界与同位素端点盲测.py`（+png/json）、`05_Lean验证/R12BlindTest.lean`（5 条，退出码 0）、`06_决策记录/2026-11-25_第160轮_T星上界与同位素端点盲测.md`、R-169；文献 L52 只作数据出处。

### 第 161 轮（R-170）：和乐动力学映射与推 6 终结

- **映射**：由高斯 $\lambda$ 与 $\theta=\alpha\lambda$ 得 $p_{\rm lock}=\operatorname{erf}(\pi/(\sqrt2\sigma_\theta))$、$y=\operatorname{erfc}(\cdot)$；只匹配指数到 $y=2\pi e^{-E_c/k_BT}$ ⇒ $\sigma_\theta^2=k_BT/\Upsilon_0$、$K=1/\sigma_\theta^2$，锁—失锁交叉与 BKT 同量级；前因子差（熵因子 $2\pi$）登记为外部边界。
- **$\Upsilon_0$ 结构式**：$\Upsilon_0=\hbar\omega/[4\alpha^2\kappa_f^2\sigma_0^2(1-\rho)]$，仍受 `审-21`／`临-26`／Z2 阻断，不闭合绝对能标。
- **推 6 终结**：三载体 $q_c=0.378641/0.358718/0.346664<0.5$，达键阈值需 $\rho_{nn}\ge0.986862>0.181192$。
- **边界**：不闭合任何编号、不改状态栏，唯一编号仍 37、闭合数仍 0。
- 入口：`03_推导工作台/环15和乐动力学映射与推6终结.md`、`04_计算验证/环15和乐动力学映射与推6终结.py`（+png/json，七段断言）、`05_Lean验证/HolonomyLockMap.lean`（5 定理，退出码 0）、`06_决策记录/2026-11-25_第161轮_和乐动力学映射与推6终结.md`、R-170；文献 L53 只作外部标准。

## 相关入口

- 主链：`../CQM_探索_推导链.md`
- 探索纪律：`../AGENTS.md`
- Lean 主库：`../../08 理论组织和形式化框架/04_Lean对接/Lean源码/`
- 缺口台账：`../../08 理论组织和形式化框架/附录/缺口台账.md`

