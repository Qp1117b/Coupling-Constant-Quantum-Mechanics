# 决策：回查 Karakozov 前因子与对数矩定义——发现两矩分歧，诚实降级并回头重算

**日期**：2026-11-23  
**授权**：用户"发现不对劲再回过头有理有据的修正推导链、环节、理论、方程和模型"。  
**范围**：工作台审查；不改主链权威式、不动缺口编号与状态栏、不动账面。

## 一、发现（文献核对，已 webfetch 全文）

1. **Marsiglio arXiv:1807.04907v2 式(7) 明确 Einstein 谱假设**：$\alpha^2F=(\lambda\omega_E/2)\delta(\nu-\omega_E)$。Eq26/Eq37 的 $1.13/\sqrt e$ 是 **Einstein 谱**结果（$I_4\approx1/2$ 用 $\bar\omega_m=\omega_m/\omega_E$ 的 Lorentzian 核）。脚注29 确认 Karakozov 的 $1.134/e^{1/2}$ 同语境。
2. **Note added in proof**："for any shape of $\alpha^2F(\nu)$" 的弱耦合解在 Combescot, PRB 42, 7810 (1990)——**与 Eq37 是不同工作**。
3. **关键新发现——两个对数矩权重不同**：Webb 式(3) 的 $\omega_{\ln}=\exp[\frac{2}{\lambda}\int\ln\nu\,\frac{\alpha^2F}{\nu}d\nu]$ 权重是 **$\alpha^2F/\nu$**；对 Debye 谱 $\alpha^2F\propto\nu^2$ ⇒ 权重 $2y$ ⇒ $\omega_{\ln}=\nu_D e^{-1/2}$。而 CQM (目标.3) 用 **$3y^2$（电子态密度）** ⇒ $\omega_D e^{-1/3}$。**两矩差 $e^{1/6}$**——恰是第57轮 Karakozov 因子的数值。

## 二、决定

1. **降级第57轮结论**："与 Eq37 精确重合"→"与 Einstein 谱弱耦合式 Eq37 **形式上对齐**；跨谱合法性需 Combescot 任意谱解核对"。方向可能对（Combescot 或证普适），但当时仅凭同谱代数恒等式、未引用 Combescot、用的矩对象是 CQM 电子态密度矩——证据链不完整。既不断言相同也不断言不同，标"待核"。
2. **标注跨定义代入**：CQM $\omega_{\log}$（$3y^2$ 矩）与 Eliashberg $\omega_{\ln}$（$\alpha^2F/\nu$ 矩）**不是同一个量**；第57、58、60、61轮把它们代入 Eliashberg 标准式的结果（Eq37 重合、gap ratio、$\mu^\ast$ 双观测）须加边界："用的是 CQM 矩，非 Eliashberg 标准矩"。
3. **回头重算 gap ratio**（脚本 `审_Eliashberg矩重算gap比.py`）：用正确矩 $e^{-1/2}$ 替换 $e^{-1/3}$ 后，8 元素平均偏差 **2.7%→2.9%**（量级稳健），强耦合元素改善（Nb −1.1%→+0.7%、V −0.4%→+0.1%、Pb −2.1%→+1.8%）。第58轮 2.7% 的**精确值**依赖用错矩，核心量级结论不变——诚实标注，不删原卡（保可追溯）。
4. **Lean 引用现有**：`IsotopeScaling.lean` 已证 2D 矩 $e^{-1/2}$、3D 矩 $e^{-1/3}$、$e^{-1/2}<e^{-1/3}$、比值 $e^{-1/6}$——本轮恒等式已覆盖，无需新文件。
5. **登记两个临时缺口**（待与权威台账对齐）：`审-16`（Einstein 前因子跨谱合法性）、`审-17`（CQM $\omega_{\log}$ 与 Eliashberg $\omega_{\ln}$ 对应关系未建立）。按 §10 AGENTS.md"缺编号就登记新缺口，不借用旧编号"。
6. 保留所有编号与状态栏；账面不变（62 行/35 唯一/35 推进/0 余）。

## 三、否决的读法

1. 认为第57轮完全错：方向可能对，只降级证据链，不删改权威式。
2. 认为 CQM $\omega_{\log}$ 就是 Eliashberg $\omega_{\ln}$：权重不同（$3y^2$ vs $2y$），差 $e^{1/6}$。
3. 认为 gap ratio 2.7% 被推翻：重算 2.9%，量级稳健，强耦合反而改善；只改精确值标注。
4. 认为 Combescot 结论已知：原文付费墙未核对，方向待核，不断言。
5. 认为改了权威式/状态栏/账面：没有，只在工作台加审查卡与注记。

## 四、保留的可证伪分支

1. 若 Combescot 原文可获取，可直接判 Karakozov $e^{-1/2}$ 对任意谱是否普适——决定第57轮方向。
2. 若实验 $\omega_{\ln}$（隧穿反演）与 CQM $e^{-1/3}\theta_D$ 系统差 $e^{1/6}$，则 (目标.3) 的矩定义需重审——材料谱侧。
3. 若用正确矩后 gap ratio 系统偏离实验更大，则 Mitrović 式的矩输入需再核——外部式侧。

## 五、证据

- 审查卡：`03_推导工作台/审_Karakozov前因子的谱假设回查.md`、`03_推导工作台/审_Eliashberg对数矩与CQM对数矩的定义分歧.md`；
- 文献（标源，已 webfetch 全文）：Marsiglio arXiv:1807.04907v2 式(7)(26)(37)、脚注29、Note added；Webb 2015 式(3)(4)(6)；Combescot PRB 42 7810 (1990)（付费墙，未核对内容）；
- Lean：`IsotopeScaling.lean` 已有 `omegaLog2D`、`omegaLog3D`、`omegaLog2D_lt_3D`、`omegaLog_ratio`（退出码 0）；
- 数值：`审_Eliashberg矩重算gap比.py`／`.png`／`.csv`；两矩平均偏差 2.7% vs 2.9%。

## 六、状态

第57轮 Karakozov 前因子结论降级为"与 Einstein 谱 Eq37 形式对齐、跨谱待核"；发现 CQM $\omega_{\log}$ 与 Eliashberg $\omega_{\ln}$ 两矩分歧（差 $e^{1/6}$）；gap ratio 用正确矩重算 2.9%（量级稳健）；登记两个临时缺口；主链权威式、状态栏、缺口编号、账面（62 行/35 唯一/35 推进/0 余）、06 原文均未改；未提交任何内容。
