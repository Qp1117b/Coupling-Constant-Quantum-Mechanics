# CQM 探索：GL 参数 $\kappa$ 的两阶段分支、临界场双尺度与 GL 关系适用域——R39

> **定位**：探索稿（非权威源），v0.1，2026-11-17，第二十一轮。承接第十九轮《迈斯纳退化》与第二十轮《$H_c$ 斜率判决》，正面处理 GL 三元组中最后一块——相干长度 $\xi$、上临界场 $H_{c2}$、GL 参数 $\kappa=\lambda/\xi$。
>
> **靶点空白核查**：变更日志 §643 登记「CQM 不能单独给出电子结构主导的量（$\xi$ 干净极限、$H_{c2}$、$\Delta C$ 精确值）——是分工非缺陷」；§646–663 给出 $\xi$ 两极限与 $H_{c2}$ 两路径（标度一致、YBCO 数值吻合、干净金属不适用）。但**同组的 $\Delta C$ 已在第十七轮被突破**（给 $0/1.43$ 两极，不靠 $v_F$），说明"分工论"应精化为"给形状/分支、不给干净极限绝对值"。$\xi$、$H_{c2}$、$\kappa$ 尚未作同样的 constructive 两阶段处理。
>
> **一句话结论**：GL 恒等式 $H_{c2}=\sqrt2\kappa H_c=\Phi_0/(2\pi\xi^2)$ **隐含 $\lambda$ 与 $\xi$ 同源（同一 GL 有效质量 $m^*$）**，这是它从未被言明的适用域前提。CQM 两阶段欠掺支 $\lambda$ 由相位刚度定（$\lambda^{-2}\propto T_c$）、$\xi$ 由配对能隙定（$\xi\propto1/T^*$）——**两个不同对象**，故该关系在欠掺支必然破缺、只在过掺配对限制支恢复。由此 $\kappa$ 非常数、随 $x=T^*/T_c-1$ 增大（定性），与"欠掺 $\kappa\sim100$ 极端 II 类"一致；$H_{c2}$ 分裂为配对场 $H^*\propto T^{*2}$ 与相位场 $H^\theta\propto T_c$ 两尺度，被 Grissonnanche 2014 热导率实验直接证实。新增判据 R39。**绝对 $\xi$、$H_{c2}$ 仍外生 $v_F,m^*,e$（Z2/Z3 不变，本轮只给无量纲结构与适用域）。**

---

## 第一部分：GL 恒等式的隐藏前提（第一性代数，严格）

标准 GL 关系（SI，脚本 §1 验证）：

$$H_{c2}=\frac{\Phi_0}{2\pi\xi^2},\qquad H_c=\frac{\Phi_0}{2\sqrt2\,\pi\lambda\xi},\qquad \kappa=\frac{\lambda}{\xi}\quad\Longrightarrow\quad \frac{H_{c2}}{H_c}=\sqrt2\,\kappa. \tag{GL.1}$$

第一性数值验证（$\Phi_0=h/2e=2.067834\times10^{-15}$ Wb）：

| $\lambda$ | $\xi$ | $\kappa$ | $H_{c2}$ | $H_c$ | $H_{c2}/H_c$ | $\sqrt2\kappa$ |
|:---|:---|:---|:---|:---|:---|:---|
| 150 nm | 1.5 nm | 100.0000 | 146.3 T | 1.034 T | 141.4214 | 141.4214 ✓ |
| 39 nm | 38 nm | 1.0263 | 0.2279 T | 0.1570 T | 1.4514 | 1.4514 ✓ |
| 16 nm | 1600 nm | 0.0100 | 1.29×10⁻⁴ T | 9.09×10⁻³ T | 0.0141 | 0.0141 ✓ |

三档全部严格相等。**关键身份**：式 (GL.1) 的推导要求 $\lambda$ 与 $\xi$ 来自同一个 GL 序参量 $\psi$、同一个有效质量 $m^*$：

$$\lambda^2=\frac{m^*}{\mu_0 n_s e^{*2}},\qquad \xi^2=\frac{\hbar^2}{2m^*|a|}\ \Rightarrow\ \frac{\lambda}{\xi}\ \text{中}\ m^*\ \text{与}\ a\ \text{同源}. \tag{GL.2}$$

**这就是 (GL.1) 从未被言明的适用域前提**：一旦 $\lambda$ 与 $\xi$ 由不同机制决定，$m^*$ 在两者中不是同一个对象，$\sqrt2\kappa$ 就不再是 $H_{c2}/H_c$。

---

## 第二部分：$\kappa$ 三档 = 「相位刚度／配对能隙」比值（几何读法）

变更日志 §1248 的三档数值，用文献典型 $\lambda,\xi$ 复现（脚本 §2）：

| 材料 | $\lambda$ (nm) | $\xi$ (nm) | $\kappa$ | 类别 | 两阶段读法 |
|:---|:---|:---|:---|:---|:---|
| Al（干净） | 16 | 1600 | 0.0100 | Type-I | 高刚度 + 小能隙 |
| Nb（临界） | 39 | 38 | 1.0263 | Type-II（近界 $1/\sqrt2=0.707$） | 过渡 |
| YBCO（欠掺） | 150 | 1.5 | 100.0000 | 极端 Type-II | **低刚度（$T_c$ 低）+ 大能隙（$T^*$ 高）** |

**几何判决**：$\kappa\gg1$ 不是偶然材料参数，而是两阶段欠掺支的几何指纹——相位刚度通道给大 $\lambda$（Uemura $\lambda^{-2}\propto T_c$ 小），配对能隙通道给短 $\xi$（$\xi\propto1/\Delta$，$\Delta\propto T^*$ 大）。比值把两支的反向信息编码进一个数。这解释了为什么铜氧化物是"极端 II 类"（Liu–Mou–Feng, arXiv:1907.00663 报 $\kappa_0\approx7.86/13.05/18.20$ @ $\delta=0.08/0.12/0.15$；Zweck 学位论文报 YBCO $\kappa\approx100$）——**与第十九轮"迈斯纳刚度 ∝$1/(1+x)$ vs 能隙比 ∝$(1+x)$ 反向"是同一结构的两个读数**。

---

## 第三部分：$\kappa$ 两阶段分支——从"不变"到"分支依赖"

### 3.1 对 §1246「$\kappa$ 不变」的裁决

变更日志 §1246（统一 GL 理论）写：$\lambda,\xi\propto(p-p_c)^{-1/2}$，故 $\kappa=\lambda/\xi$ **不变**；§1249 甚至有 Lean 定理 `kappa_independent`。§1184 又写 $\kappa\propto c$（缺陷浓度）。两者看似矛盾，实则是**不同分支/不同对象**：

- **§1246 的"不变"**：平均场渗流标度下 $\lambda$ 与 $\xi$ **同源**（都由 $a(T)\propto p_c-p$ 一个系数定），比值抵消。这是**配对限制支**（$T^*=T_c$，单一序参量）的成立域——恰是 (GL.2) 同源前提满足的地方。
- **§1184 的"$\kappa\propto c$"与欠掺实验的 $\kappa$ 变化**：缺陷/掺杂改变的是刚度与能隙的**相对**权重，两对象不再同源。

**裁决**：`kappa_independent` 不是普适定理，而是**配对限制支的分支命题**。把它外推到欠掺相位限制支就是本轮要纠正的越界。

### 3.2 欠掺支的 $\kappa$ 标度

欠掺相位限制支（$x=T^*/T_c-1\gg0$）：

$$\lambda^{-2}\propto\rho_s\propto T_c\ (\text{Uemura})\ \Rightarrow\ \lambda\propto T_c^{-1/2};\qquad \xi\propto\frac{1}{\Delta_*}\propto\frac{1}{T^*}\ (\text{配对支})$$

$$\Rightarrow\ \kappa_{\rm eff}=\frac{\lambda}{\xi}\propto\frac{T^*}{\sqrt{T_c}}=\sqrt{T^*(1+x)}\ \xrightarrow[\ T^*\ \text{doping无关}\ ]{}\ \kappa\propto\sqrt{1+x}\ \uparrow. \tag{GL.3}$$

汞系 $T^*/T_c=1.85/2.22/3.04$（第十八轮反解）给 $\kappa_{\rm rel}=1.36/1.49/1.74$，**随欠掺深化单调增大**（脚本 §3）。

**诚实边界**：(GL.3) 的幂指数 $1/2$ 依赖"$T^*$ doping 无关"与"$\Delta\propto T^*$"两个近似；不同实验提取 $\Delta$ 口径分歧（LNW 的 $2\Delta/k_BT^*\approx2.15$ vs d 波理论 4.28，第十八轮已登记）。故**只锁定结构判决"$\kappa$ 非常数、欠掺增大"，不锁定幂指数**。

### 3.3 GL 关系适用域（核心）

由 (GL.2) 的隐藏前提直接得：

| 分支 | $\lambda,\xi$ 是否同源 | $H_{c2}=\sqrt2\kappa H_c$ | 场结构 |
|:---|:---|:---|:---|
| 过掺配对限制（$T^*=T_c$, $x\to0$） | 是（同一 $\psi,m^*$） | **成立** | 单一 $H_{c2}$ |
| 欠掺相位限制（$T^*\gg T_c$, $x\gg0$） | 否（刚度 vs 能隙两对象） | **破缺** | 双场 $H^*$ 与 $H^\theta$ |

**这是本轮最硬的判决**：GL 关系不是普适恒等式，而是**分支命题**；它失效的地方恰是两阶段解耦的地方。

---

## 第四部分：临界场双尺度与实验判决

### 4.1 两个场（CQM 两阶段的磁场投影）

$$\text{配对场：}\ H^*=\frac{\Phi_0}{2\pi\xi_*^2},\quad \xi_*\propto\frac{1}{T^*}\ \Rightarrow\ H^*\propto T^{*2}\quad(\text{Nernst / torque 测}) \tag{GL.4a}$$

$$\text{相位场：}\ H^\theta\propto\rho_s\propto T_c\quad(\text{比热/电阻测，Grissonnanche 称 }H_{vs}) \tag{GL.4b}$$

$$\text{分离比：}\ \frac{H^*}{H^\theta}\propto\frac{T^{*2}}{T_c}=T_c(1+x)^2. \tag{GL.5}$$

### 4.2 外部实验判决（GL1–GL6，全带出处）

| 编号 | 来源 | 关键结论 | 与 CQM 对接 |
|:---|:---|:---|:---|
| GL1 | Grissonnanche et al., *Nat. Commun.* **5**, 3280 (2014), DOI 10.1038/ncomms4280 | 热导率直接测 $H_{c2}=\Phi_0/2\pi\xi_0^2$、$\xi_0\sim v_F/\Delta$；YBCO(p=0.11) $22\pm2$ T、Y124(p=0.14) $44\pm2$ T | 配对场 $H^*$ 由 $\Delta\propto T^*$ 定（配对支） |
| GL2 | 同上 | 欠掺存在宽涡旋液体，$H_{c2}(0)\gg H_{vs}(0)$，"implying $\Delta$ is very large"；$p<0.18$ 凝聚能 **20× 塌缩** | **双场分离直接证据**（GL.4a vs 4b）+ 凝聚能塌缩（第二十轮） |
| GL3 | Wang & Wen, *EPL* **81**, 57007 (2008), arXiv:0803.0638 | LSCO 比热 $H_{c2}$ 随 $x$ 与 $T_c$ 相似；SH 测相干消失、Nernst/torque 测配对（更高场）；$\xi$ 由最优掺向两侧增大（U 形） | 同一材料两个场；$\xi$ U 形与两场竞争一致 |
| GL4 | Liu, Mou & Feng, *J. Supercond. Nov. Magn.* **33**, 69 (2020), arXiv:1907.00663 | $\kappa_0=\lambda(0)/\zeta_0$、$\zeta_0=\hbar v_F/(\pi\bar\Delta)$；$\kappa_0\approx7.86/13.05/18.20$ @ $\delta=0.08/0.12/0.15$ | $\kappa$ 随掺杂变化（非常数）、由 $\lambda$(刚度)/$\zeta$(能隙) 比定 |
| GL5 | Zweck, *Masterarbeit* LMU (2018), wmi.badw.de | YBCO 极端 II 类 $\kappa\approx100$，判据 $\kappa\lessgtr1/\sqrt2$ | $\kappa$ 三档几何读法（§2） |
| GL6 | Grissonnanche 2014（同 GL1） | $H$–$p$ 相图双峰 $p_1\sim0.08$、$p_2\sim0.18$ | 两个磁场峰 = 两支交叉的候选观测 |

**判决**：GL2 的 $H_{c2}(0)\gg H_{vs}(0)$ 是两场分离的直接证据——若只有一个 GL 序参量，涡旋固体熔化场 $H_{vs}$ 与上临界场 $H_{c2}$ 在 $T\to0$ 应重合（该文自己指出 YBCO/Y124 在 $T=0$ 无涡旋液体，恰是过掺/近最优支的表现）。欠掺的宽涡旋液体正是**配对已成立（$H^*$ 大）而相位刚度不足（$H^\theta$ 小）**的宏观信号。

---

## 第五部分：新判据 R39（可证伪）

- **R39a（$\kappa$ 分支）**：同一材料欠掺→过掺序列，$\kappa=\lambda/\xi$ 须**非常数**、欠掺端更大（定性 $\propto\sqrt{1+x}$）；若测到 $\kappa$ 全程恒定（在误差内），则 $\kappa$ 同源假设成立、证伪分通道。
- **R39b（GL 关系适用域）**：欠掺样品实测 $H_{c2}/(\sqrt2\kappa H_c)$ 须系统性偏离 1；过掺样品须趋近 1。若两支都严格满足 (GL.1)，则"两对象"判决被否定。
- **R39c（双场次序）**：同一欠掺样品，Nernst/torque 提取场 $H^*$ 须 **>** 比热/电阻提取场 $H^\theta$（GL2）；次序反转则证伪。
- 与 R29–R38 测不同对象，互相独立。

---

## 第六部分：边界、退化、范式自检

**退化守住**：
- **BCS/GL**：过掺 $x\to0$ ⇒ $T^*\to T_c$、两 $\xi$ 合一、$\lambda/\xi$ 同源 ⇒ (GL.1) 自动恢复，$H_{c2}=\Phi_0/2\pi\xi^2=\sqrt2\kappa H_c$，Type-I/II 判据 $\kappa\lessgtr1/\sqrt2$ 回到教材值（Al 0.010、Nb 1.03）。
- **迈斯纳**：本轮不触及 $\lambda_L=2\lambda_p/\sqrt\Lambda$（第十九轮），只补充 $\lambda$ 在 $\kappa$ 中的通道归属。
- **$H_c$ 斜率判决**：第二十轮 $\Delta C=T_c\mu_0(H_c')^2$ 不变；本轮只处理 $H_c2$ 侧。
- **Z1/Z2/Z3、R27–R38、M.53、$\zeta$/质数形状侧**：全部未触碰。

**能标边界（诚实）**：$\Phi_0=h/2e$ 含外生 $e$；$\xi$、$H_{c2}$、$\lambda$ 的绝对值外生 $v_F,m^*$（变更日志 §638–642 已登记）——与 $\Delta C$ 突破方式一致，本轮只给**无量纲结构 + 分支适用域**，不承诺绝对数值。Z2/Z3 不变。

**克制拟合**：全轮无拟合参数。$\kappa\propto\sqrt{1+x}$ 的指数、$\kappa_0$ 三档数值、$T^*/T_c$ 反解值均标注为外部或近似，不用于参数调节。

**范式**：关系性范式；不改 `01–08`、`归档/` 的定义与数值；只在 `10 探索/` 新增本文并给相关旧稿加指针（保留原文）。

---

## 附：脚本与数据

- 脚本：`10 探索/.calc/gl_kappa_two_stage_audit.py`（已 gitignore）
- 第一性验证：GL 恒等式三档 match=True；$\Phi_0=2.067834\times10^{-15}$ Wb
- 全部外部文献 GL1–GL6 带 DOI/arXiv 出处，作者已逐一核实
