# 第 108 轮决策记录：Mattis-Bardeen 光学电导与 FGT sum rule——链内 gap 的太赫兹谱学闭环

**范围**：`10 探索/超导第一性研究`；新增预注册 R18；不改状态栏、不动 06／01／08／研究站／主链环号。
**日期**：2026-11-24
**成果登记编号**：R-117（成果表独立序列；README 用"第 108 轮补"）
**触发**：用户要求"从头算到尾严格精确验证超导数据"。前 17 轮贯通热力学/电动力学/隧穿谱学，本轮补第四个独立维度——光学/太赫兹响应（Mattis-Bardeen 1958），其光学阈值 $2\Delta_0$ 是链内 gap 的直接后果，FGT sum rule 把缺失谱重与已验证超流密度连接成闭环。

## 一、决定

1. **Mattis-Bardeen 光学电导（A 类结构＋B 类工具）**：$T=0$ 干净极限闭式解 $\frac{\sigma_{1s}}{\sigma_{1n}}=[(1+2\Delta/\omega)E(k)-\frac{4\Delta}{\omega}K(k)]\Theta(\omega-2\Delta)$，$k=(\omega-2\Delta)/(\omega+2\Delta)$，代入链内 $\Delta_0=\pi e^{-\gamma}k_BT_c$。光学阈值 $\hbar\omega_g=2\Delta_0$，$2\Delta_0/k_BT_c=3.5278$（纯数）；$\omega<2\Delta_0$ 硬隙严格为 0；高 $\omega$ 趋 1（$\sigma_1(200\Delta)=0.99968$）。
2. **FGT sum rule（闭环）**：$\rho_s=\frac{c^2}{8\lambda_L^2}=\frac{2}{\pi}\int_{0^+}^\infty[\sigma_{1n}-\sigma_{1s}]d\omega$——光学缺失谱重＝超流密度（R15 已验证 $\rho_s(t)$ 全程）。数值累积谱重趋平台 8.4646（有限、守恒），光学 gap 尺度 $2\Delta_0$ 与隧穿 gap（R17）一致。
3. **$\sigma_2$ 低频极限**：$\omega\sigma_{2s}/\sigma_{1n}\to\pi\Delta_0$（Tinkham 标准，数值 3.141593）。**回头修正**：初版误把 $k'=\sqrt{1-k^2}$ 写为常数 1，得假象 $e^\gamma\Delta$；按 Eq.63 正确取 $k'$ 后恢复标准 $\pi\Delta$——修正已落地并记入预注册，防干扰。
4. **文献调研**：Mattis & Bardeen PR 111, 412 (1958)；Ferrell-Glover-Tinkham sum rule（PRB 108, 104501 2023 高精度验证、Dressel 2013 综述）；arXiv cond-mat/0408054（MB Eq.61/63 闭式）；Boris PRB 108 104501；Quasiparticle response of Al（arXiv:0712.3391）；无序 NbN sub-gap 吸收文献。
5. **历史唯物主义合规**：隙方程结构（基础）决定 gap 与光学阈值/谱形（读数），读数不反写结构；必然性（阈值 $2\Delta_0$、FGT 守恒、$\pi\Delta$ 系数）＋偶然性（$\lambda(0)$、材料归一外生）分层统一；同形不是还原（§0.2），不声称 CQM＝BCS；未用社会范畴。
6. **Lean**：`OpticalConductivity.lean`（4 条：光学阈值 $2\pi/e^\gamma$、$\omega\sigma_2$ 系数、阈值正性，退出码 0、无警告）。
7. **诚实边界**：MB/FGT 是 B 类外部电动力学工具，链内贡献是 gap $\Delta_0$＋超流密度（R15）＋$\alpha^2F$ 构造（第92轮）；**强耦合 Pb/Hg、无序 NbN 的 sub-gap 吸收偏离纯 MB**（文献明确），本轮只验弱耦合干净极限；绝对 $T_c$ 外生。

## 二、对既有口径的处理

| 项 | 判定 |
|:---|:---|
| C5 gap ratio（$2\pi/e^\gamma$）、gap 曲线（R11）、超流密度（R15）、隧穿（R17）、α²F（第92轮） | **补上光学维度**：阈值 $2\Delta_0$＋FGT 守恒，与四维度互相印证、不升状态 |
| MB/FGT 电动力学工具 | **B 类外部工具**，不升格链内第一性 |
| 初版 $\sigma_2$ 假象 $e^\gamma\Delta$ | **已修正为 $\pi\Delta$**（Tinkham 标准），记入预注册防干扰 |
| 第 100 轮强耦合偏离 | 状态原样 |
| `审-11`、`临-20` 等 | 状态原样 |
| 06 原文 | **仍待与 06 对账**（只登记不改） |

## 三、边界与"不能推出什么"
1. 电动力学工具 B 类，光学阈值/谱形的链内决定是 A 类结构；2. 不声称 CQM＝BCS（同形不是还原）；3. 强耦合/无序 sub-gap 偏离（本轮只验弱耦合干净极限）；4. 绝对 $T_c$、$\lambda(0)$ 外生；5. 不碰 `临-8`／`临-22`／RH；6. 量变质变只作诠释、未用社会范畴。

## 四、交付物
- 预注册 `07_数据与现象/预注册判定_R18.md`
- Lean `05_Lean验证/OpticalConductivity.lean`（4 条，退出码 0、无警告、无禁用项）
- 数值图 `04_计算验证/R18_MattisBardeen光学电导.py`／`.png`／`_摘要.csv`（四面板、五断言）
- 决策记录（本文件）、同步 `成果登记.md` R-117、`数据对照协议.md` §十七、`00_当前有效口径表.md` §二、README

## 五、删除／防干扰
无删除——新增光学维度验证，未动任何编号、状态或推导卡。初版 $\sigma_2$ 公式错误（$k'$ 写反得假象 $e^\gamma$）已回头修正为 $\pi\Delta$，记入预注册。

## 六、下一步
1. 用真实 THz/红外 $\sigma_1(\omega)$ 数据（Al/NbN，Pracht/Office et al.）做 MB 谱形＋FGT 谱重盲测（本轮是理论闭式＋守恒）。
2. Mattis-Bardeen 相干峰（finite-T $\sigma_1(T)$ near $T_c$）的链内描述（须授权，不虚构）。
3. 强耦合光学谱（Eliashberg 声子结构）的链内路径（须授权，不虚构）。

## 七、纪律自检（AGENTS §5 必答）
- 动了哪一环：**无环号改动**（光学维度验证）；新增预注册 R18。
- 碰了哪条缺口：**光学阈值与 FGT 守恒（A 类结构）；接超流密度与 α²F**，状态不动。
- 状态是否变动：**未变动**（状态栏、编号、账面均不动）。不改 06／01／08，不动研究站、Lean 主库、主链环号。
