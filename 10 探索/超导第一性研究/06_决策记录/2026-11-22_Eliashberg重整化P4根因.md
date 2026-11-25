# 决策：Eliashberg 质量增强 $1+\lambda$ 缺失——P4 根因的精确定位（重大发现）

**日期**：2026-11-22  
**范围**：目标区 (目标.2) 与 V2 P4；不改权威式、不动缺口编号与状态栏、不动账面。  
**文献**：Marsiglio, arXiv:1807.04907v2（已 webfetch 全文核对）+ Webb 2015 Table III 实测数据。

## 一、决定（本轮是首次定量 P4 检验的重大发现）

1. **文献关键**：Marsiglio 给出同一 bare $\lambda\equiv g_{\epsilon_F}|V|$（与 CQM (10.3) $\lambda_i=N(0)\sum|V_{ij}|$ **同类**）的 BCS(13) $T_c=1.13\omega_Ee^{-1/\lambda}$、含重整化(14) $e^{-(1+\lambda)/\lambda}$、弱耦合精确(37) $\frac{1.13}{\sqrt e}\omega_Ee^{-(1+\lambda)/\lambda}$。文献明确"BCS 常被视为 Eliashberg 弱耦合极限，但有论文指出并非如此"。
2. **定量发现**：用实测 $T_c$ 反解，BCS 型(13)给 bare $\lambda\approx0.17$–$0.41$（第53轮 CQM 反解），Eliashberg(37)型给 $\approx0.22$–$0.77$；两口径比值 $E/C=1.25$–$1.90$ **单调随耦合增**，正是质量增强 $Z=1+\lambda$ 的定性特征——**CQM (目标.2) 用 BCS 裸指数 $e^{-1/\lambda}$，缺 Eliashberg 质量增强 $e^{-(1+\lambda)/\lambda}$**（Lean `renorm_exponent_factor`、`renorm_lowers` 证重整化严格压低 $T_c$ 一个 $e^{-1}$ 因子）。
3. **P4 根因精确定位**：从笼统"缺 $\mu^*$"精确为三因素——①缺 $1+\lambda$ 重整化（主）；②缺 $\mu^*$（次，`审-14`）；③对数矩口径 $e^{-1/3}$（次，第54轮）。三者都属"形状与刻度"缺口，非实验否证。
4. **链内对应**：$Z=1+\lambda$ 质量增强 $m^\ast/m\approx1+\lambda$（Webb 综述）对应 CQM 固有时流速场 $v_\tau$ 的"被声子拖曳"——链内有对象但从未写成方程（可归 `临-1` 或新子项）。**这是"从头算到尾"必须补的一环**。
5. **不擅自改权威式**：补它须在 (目标.2) 引入 $e^{-(1+\lambda)/\lambda}$ 并重整化 $v_\tau$——新机制、波及 C5/V1/V2 全部推导。按"不虚构、不绕过"，本轮只定位根因、记录修正候选，**待用户明确授权**才改式。
6. **回改**：Lean 初稿未用参数警告、数值脚本 `tab:yellow` 无效颜色，已按反馈修正；无数学结论错误残留。
7. 保留所有编号与状态栏；账面不变（62 行/35 唯一/35 推进/0 余）。

## 二、否决的读法

1. 认为 CQM 被实验否证：比值系统性来自缺重整化与口径，非物理错误。
2. 认为 $\lambda_{E37}$ 是真值：依赖 $\theta_D\approx\omega_E$ 取等（Debye vs Einstein 谱不同）。
3. 认为可给精确映射 $E/C=f(\lambda_C)$：会变成拟合，链内无此方程。
4. 认为已改权威式：没有，只定位根因与修正候选，待授权。
5. 认为重整化是外部强加：$Z=1+\lambda$ 对应链内 $v_\tau$ 场拖曳，是链内可补的一环，只是尚未写入。
6. 认为本轮改了状态栏或账面：没有。

## 三、保留的可证伪分支

1. 若授权补入 $e^{-(1+\lambda)/\lambda}$ 重整化，须重跑 C5/V1/V2 全部——gap ratio 仍普适（Marsiglio 文献明确比值在 $\lambda\to0$ 保持普适）。
2. 若实验 $\lambda$（隧穿 $\alpha^2F$）给出，可直接核对两口径哪个对。
3. 若 $E/C$ 偏离 $1+\lambda$ 单调趋势，则对数矩口径需重审。

## 四、证据

- 工作台：`03_推导工作台/环目标_Eliashberg重整化缺失与P4根因.md`；
- Lean：`05_Lean验证/EliashbergRenorm.lean`，退出码 0、无警告（`renorm_exponent_factor`、`renorm_lowers`、`mass_enhancement`、`mass_enhancement_mono`）；
- 数值：`04_计算验证/环目标_Eliashberg重整化.py`／`.png`／`.csv`；8 元素两口径反解 $E/C=1.25$–$1.90$ 单调随 $\lambda_C$ 增；
- 外部（标源）：Marsiglio arXiv:1807.04907 Eq.13/14/37；Webb 2015 Table III。

## 五、状态

P4 根因由"笼统缺 $\mu^*$"精确定位为"缺 $1+\lambda$ 重整化（主）＋缺 $\mu^*$（次）＋对数矩口径（次）"；这是"从头算到尾"的关键剩余环节，链内有对应对象（$v_\tau$ 拖曳）但需授权才能写入 (目标.2)。不动缺口编号与状态栏、账面不变。

**下一步（需用户定夺）**：是否授权把 Eliashberg 质量增强 $Z=1+\lambda$ 作为新环节写入 (目标.2)？授权则需重跑 C5/V1/V2 全链并同步；不授权则本发现作为 P4 根因登记、保持现状。
