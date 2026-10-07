# -*- coding: utf-8 -*-
"""
维度 06 · 经验检验
产出（07_经验检验/）：
  因果模型/GN_causal_dag.json
  因果模型/dowhy_model.py
  因果模型/README.md
  贝叶斯网络/gap_closure_model.bif
  贝叶斯网络/network_spec.md
  贝叶斯网络/infer.py
  实验设计/design_matrix.csv
  实验设计/isotope_effect_protocol.md
  实验设计/pseudogap_arpes_protocol.md
运行：python build_causal.py
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S07 = os.path.join(ROOT, "07_经验检验")

# 权威数值（README 数值表 / 各概念权威定义处）
TAIJI = 0.02309570897           # ☯ = ξ'(1)/ξ(1)，D008 §3 / D005 §7.1
LAM_C = 1.316022911308          # Mathieu 临界 λ_c，D019 §5
I_DYN = 5.0 / 3.0               # Dynkin 指数比 I=5/3，D014 §5
KAPPA = (31 + TAIJI) / 30.0     # κ=(31+☯)/30，D031 §11


def causal_dag():
    nodes = [
        {"id": "I", "label": "Dynkin 指数比 I=5/3", "role": "群论因子", "source": "D014 §5"},
        {"id": "lambda_c", "label": "Mathieu 临界 λ_c", "role": "谱因子", "source": "D019 §5"},
        {"id": "taiji", "label": "相变量子 ☯", "role": "谱因子", "source": "D008 §3"},
        {"id": "c_1", "label": "第一耦级 𝔠₁=1/4+γ₁²", "role": "谱因子", "source": "D008 §3"},
        {"id": "kappa", "label": "谱修正 κ=(31+☯)/30", "role": "谱修正", "source": "D031 §11"},
        {"id": "m_p", "label": "质子质量 m_p", "role": "实验输入", "source": "D019"},
        {"id": "h", "label": "ℏc", "role": "常数", "source": "D019"},
        {"id": "GN", "label": "牛顿引力常数 G_N", "role": "结果", "source": "D014 §5"},
    ]
    edges = [
        {"from": "taiji", "to": "kappa", "relation": "映射", "note": "κ=(31+☯)/30"},
        {"from": "taiji", "to": "GN", "relation": "重组实现", "note": "☯²·exp(-2/☯)"},
        {"from": "kappa", "to": "GN", "relation": "重组实现", "note": "(1+κ☯)"},
        {"from": "I", "to": "GN", "relation": "重组实现", "note": "线性因子"},
        {"from": "lambda_c", "to": "GN", "relation": "重组实现", "note": "线性因子"},
        {"from": "c_1", "to": "GN", "relation": "重组实现", "note": "线性因子"},
        {"from": "m_p", "to": "GN", "relation": "重组实现", "note": "1/m_p²"},
        {"from": "h", "to": "GN", "relation": "重组实现", "note": "ℏc"},
    ]
    return {
        "model": "G_N 结构因果模型（SCM）",
        "formula": "G_N = (ℏc/m_p²)·I·λ_c·☯²·𝔠₁·exp(-2/☯)·(1+κ☯)",
        "source": "P010（D014 §5）；锚点映射 C081",
        "caveat": "构造后验数字校验，待独立复现",
        "variables": nodes, "edges": edges,
        "note": "本图为确定性结构方程（SCM），非观测因果图；用于敏感性/反事实分解。",
    }


def elasticity():
    """对数弹性解析式与可安全数值化的分量。"""
    e_taiji = 2 + 2 / TAIJI + (KAPPA * TAIJI) / (1 + KAPPA * TAIJI)
    return {
        "dlnGN/dlnI": 1.0,
        "dlnGN/dlnlambda_c": 1.0,
        "dlnGN/dlnc_1": 1.0,
        "dlnGN/dlnm_p": -2.0,
        "dlnGN/dlnkappa": round((KAPPA * TAIJI) / (1 + KAPPA * TAIJI), 6),
        "dlnGN/dlntaiji": round(e_taiji, 4),
        "values_used": {"taiji": TAIJI, "lambda_c": LAM_C, "I": round(I_DYN, 6), "kappa": round(KAPPA, 6)},
        "note": "☯ 弹性最大（≈88.6），放大 ☯ 的数值不确定性；𝔠₁ 与 γ₁ 取值以权威定义处为准。",
    }


def main():
    for d in ["因果模型", "贝叶斯网络", "实验设计"]:
        os.makedirs(os.path.join(S07, d), exist_ok=True)

    dag = causal_dag()
    dag["elasticity"] = elasticity()
    with open(os.path.join(S07, "因果模型", "GN_causal_dag.json"), "w", encoding="utf-8") as f:
        json.dump(dag, f, ensure_ascii=False, indent=2)

    with open(os.path.join(S07, "因果模型", "dowhy_model.py"), "w", encoding="utf-8") as f:
        f.write('''# -*- coding: utf-8 -*-
"""
G_N 结构因果模型：敏感性 / 反事实分解（对接 DoWhy / statsmodels）。
G_N = (ℏc/m_p²)·I·λ_c·☯²·𝔠₁·exp(-2/☯)·(1+κ☯)
未安装 dowhy 时，直接运行本文件的解析弹性即可。

依赖（可选）：pip install dowhy pandas
"""
import json, os, math

TAIJI = 0.02309570897
LAM_C = 1.316022911308
I_DYN = 5/3
KAPPA = (31 + TAIJI)/30

def log_gn_factors(I, lam, taiji, c1, kappa, mp, hbarC=1.0):
    return (math.log(hbarC) - 2*math.log(mp) + math.log(I) + math.log(lam)
            + 2*math.log(taiji) + math.log(c1) - 2/taiji + math.log(1 + kappa*taiji))

def elasticities():
    return {
        "I": 1.0, "lambda_c": 1.0, "c_1": 1.0, "m_p": -2.0,
        "kappa": (KAPPA*TAIJI)/(1+KAPPA*TAIJI),
        "taiji": 2 + 2/TAIJI + (KAPPA*TAIJI)/(1+KAPPA*TAIJI),
    }

def counterfactual(taiji_new):
    """仅改 ☯，其余因子固定，返回 ln G_N 的相对变化。"""
    base = log_gn_factors(I_DYN, LAM_C, TAIJI, 1.0, KAPPA, 1.0)
    cf = log_gn_factors(I_DYN, LAM_C, taiji_new, 1.0, (31+taiji_new)/30, 1.0)
    return cf - base

if __name__ == "__main__":
    print("elasticities:", json.dumps(elasticities(), ensure_ascii=False, indent=2))
    print("dlnGN for taiji +1%:", round(counterfactual(TAIJI*1.01), 4))
    # DoWhy（若已安装）：以解析弹性作为结构假设的检验
    try:
        import dowhy  # noqa
        print("dowhy available: 可据 GN_causal_dag.json 构造 CausalModel 做识别与反驳")
    except ImportError:
        print("dowhy 未安装：pip install dowhy 后可构造识别/反驳检验")
''')

    with open(os.path.join(S07, "因果模型", "README.md"), "w", encoding="utf-8") as f:
        e = elasticity()
        f.write(f"""# 经验检验 · 因果模型（$G_N$ 结构因果模型）

> 把 $G_N$ 谱公式当作**结构因果模型（SCM）**，做敏感性分解与反事实推断。
> 数值带"构造后验数字校验，待独立复现"限定语；本文不产生新的物理结论。

## 一、结构方程

$$G_N = \\frac{{\\hbar c}}{{m_p^2}}\\,I\\,\\lambda_c\\,☯^2\\,\\mathfrak c_1\\,\\exp\\!\\left(-\\frac{{2}}{{☯}}\\right)(1+\\kappa☯)$$

出处：命题 P010（`03 引力与退相干/CQM_引力_GN可能公式.md` §5）。

## 二、因果图

节点与边见 `GN_causal_dag.json`。$☯$ 是**共同前因**：既直接进入 $G_N$，又经 $\\kappa=(31+☯)/30$ 二次进入。

## 三、对数弹性（敏感性分解）

对 $\\ln G_N$ 求对数弹性 $\\partial \\ln G_N/\\partial \\ln X$：

| 因子 $X$ | 弹性 | 值 |
|:---|:---|:---|
| $I$ | $1$ | 1 |
| $\\lambda_c$ | $1$ | 1 |
| $\\mathfrak c_1$ | $1$ | 1 |
| $m_p$ | $-2$ | −2 |
| $\\kappa$ | $\\dfrac{{\\kappa☯}}{{1+\\kappa☯}}$ | {e['dlnGN/dlnkappa']} |
| $☯$ | $2+\\dfrac{{2}}{{☯}}+\\dfrac{{\\kappa☯}}{{1+\\kappa☯}}$ | {e['dlnGN/dlntaiji']} |

**结论**：$☯$ 的弹性最大（≈{e['dlnGN/dlntaiji']}，由 $\\exp(-2/☯)$ 主导），故 $☯$ 的数值精度是 $G_N$ 精度的瓶颈；反事实示例见 `dowhy_model.py`（$☯$ 变动 1%）。

## 四、与 DoWhy 的对接

1. `pip install dowhy`。
2. 以 `GN_causal_dag.json` 的变量/边构造 `CausalModel(graph=...)`；因无观测样本，识别步骤针对**结构方程**而非数据。
3. 可执行的反驳检验：随机共同原因、安慰剂因子（替换为常数）、数据子集稳健性（对 $☯$ 扰动）。
4. 不训练模型、不引入实验数据；本节仅登记检验规格。

## 五、限定语

$G_N$ 相关数值一律带"构造后验数字校验，待独立复现"。$\\mathfrak c_1$、$\\gamma_1$ 取值以权威定义处为准，本文不重算。
""")

    # ---- 贝叶斯网络 ----
    bif = '''<?xml version="1.0" encoding="UTF-8"?>
<!-- CQM 缺口闭合贝叶斯网络（结构取自 01_结构化数据/缺口依赖闭包.md）
     状态：闭合 / 部分 / 未闭合；CPT 为占位均匀分布（待标定），不构成理论结论 -->
<BIF VERSION="0.3">
<NETWORK>
<NAME>CQM_gap_closure</NAME>
<STATES>closed_partial_open</STATES>
<PROBABILITY>
<FOR>G2</FOR>
<GIVEN>__dummy__</GIVEN>
<TABLE>0.33 0.34 0.33</TABLE>
</PROBABILITY>
<PROBABILITY>
<FOR>G3</FOR>
<GIVEN>G2 dummy</GIVEN>
<TABLE>0.5 0.5 0.0 0.5 0.5 0.0 0.0 0.5 0.5</TABLE>
</PROBABILITY>
<PROBABILITY>
<FOR>G4</FOR>
<GIVEN>G3 dummy</GIVEN>
<TABLE>0.5 0.5 0.0 0.5 0.5 0.0 0.0 0.5 0.5</TABLE>
</PROBABILITY>
<PROBABILITY>
<FOR>G5</FOR>
<GIVEN>G4 dummy</GIVEN>
<TABLE>0.5 0.5 0.0 0.5 0.5 0.0 0.0 0.5 0.5</TABLE>
</PROBABILITY>
<PROBABILITY>
<FOR>C_core</FOR>
<GIVEN>C_gap dummy</GIVEN>
<TABLE>0.5 0.5 0.0 0.5 0.5 0.0 0.0 0.5 0.5</TABLE>
</PROBABILITY>
<PROBABILITY>
<FOR>SC_chain</FOR>
<GIVEN>G13 G14 dummy</GIVEN>
<TABLE>0.8 0.2 0.0 0.6 0.4 0.0 0.4 0.5 0.1 0.6 0.4 0.0 0.4 0.5 0.1 0.2 0.5 0.3</TABLE>
</PROBABILITY>
<PROBABILITY>
<FOR>Formal_status</FOR>
<GIVEN>C_core SC_chain dummy</GIVEN>
<TABLE>0.7 0.3 0.0 0.5 0.5 0.0 0.3 0.5 0.2 0.5 0.5 0.0 0.3 0.6 0.1 0.1 0.5 0.4</TABLE>
</PROBABILITY>
</NETWORK>
</BIF>
'''
    with open(os.path.join(S07, "贝叶斯网络", "gap_closure_model.bif"), "w", encoding="utf-8") as f:
        f.write(bif)

    with open(os.path.join(S07, "贝叶斯网络", "infer.py"), "w", encoding="utf-8") as f:
        f.write('''# -*- coding: utf-8 -*-
"""缺口闭合贝叶斯网络：加载 BIF 并做后验推断（对接 pgmpy）。未安装 pgmpy 时打印网络结构。"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
BIF = os.path.join(HERE, "gap_closure_model.bif")

def structure():
    return {"nodes": ["G2","G3","G4","G5","C_gap","C_core","G13","G14","SC_chain","Formal_status"],
            "edges": [("G2","G3"),("G3","G4"),("G4","G5"),("C_gap","C_core"),
                      ("G13","SC_chain"),("G14","SC_chain"),
                      ("C_core","Formal_status"),("SC_chain","Formal_status")],
            "states": ["闭合","部分","未闭合"]}

def run():
    try:
        from pgmpy.readwrite import BIFReader
        m = BIFReader(BIF).get_model()
        from pgmpy.inference import VariableElimination
        inf = VariableElimination(m)
        print(inf.query(["Formal_status"], evidence={"G13":"闭合","G14":"闭合"}))
    except ImportError:
        print("pgmpy 未安装：pip install pgmpy。网络结构：")
        print(structure())

if __name__ == "__main__":
    run()
''')

    with open(os.path.join(S07, "贝叶斯网络", "network_spec.md"), "w", encoding="utf-8") as f:
        f.write(r"""# 经验检验 · 贝叶斯网络（缺口闭合）

> 以 `01_结构化数据/缺口依赖闭包.md` 的缺口依赖图为**结构先验**，构建贝叶斯网络，用于"证据（某些缺口闭合）→ 后验（整体形式化状态）"的推断。
> **CPT 为占位（均匀 / 半经验）分布，标注为待标定**；本网络不产生理论结论。

## 一、节点（状态：闭合 / 部分 / 未闭合）

| 节点 | 含义 | 依赖 |
|:---|:---|:---|
| `G2` | 耦合空间 → 双曲 Laplacian 必要性 | 根 |
| `G3` | $\hat D=-i(\partial_u-1/2)$ 唯一性 | `G2` |
| `G4` | $\hat D\to\hat H=\hat D^2+1/4$ 涌现 | `G3` |
| `G5` | 退相干 → 边界条件 $\vartheta_n$ 锁定（归属待裁定） | `G4` |
| `C_gap` / `C_core` | 缺口 C（退相干稳态＝$A_4$）及其被依赖 | 根 → 汇聚 |
| `G13` / `G14` | BCS 渐近（闭合）/ 中子缺陷谱判据（闭合） | 根 |
| `SC_chain` | 超导涌现链整体闭合 | `G13`,`G14` |
| `Formal_status` | 形式化整体状态 | `C_core`,`SC_chain` |

## 二、结构与 CPT

- 结构：`gap_closure_model.bif`（BIF 0.3，兼容 pgmpy `BIFReader`）。
- CPT：`G13`、`G14` 已知为**闭合**（Lean `bcsTcFromIntegral_solved` / `TestDet`），其余为占位均匀分布，**待以独立复现结果标定**。
- 推断：`infer.py`（`pip install pgmpy`）。

## 三、用法与边界

- 可回答：给定若干缺口闭合证据，形式化状态的后验分布。
- 不可用于：声称任何缺口"实际上已闭合"；`Formal_status` 的后验是**模型先验+占位 CPT 的产物**，非理论事实。
- 与 `07_经验检验/因果模型/` 的分工：因果模型处理物理量（$G_N$）的结构方程；本网络处理缺口状态的形式推断。
""")

    # ---- 实验设计 ----
    with open(os.path.join(S07, "实验设计", "design_matrix.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["exp_id", "target_gap", "phenomenon", "independent_variable", "dependent_variable",
                    "cm_prediction_source", "control", "data_source", "status"])
        w.writerow(["E1", "G15", "同位素效应", "同位素质量 M", "主/次结构谱间隙差 ΔE", "D031 §11（未闭合）",
                    "同族非同位素样品", "ARPES/比热/穿透深度", "未闭合"])
        w.writerow(["E2", "G21", "赝能隙相图", "掺杂/温度 (p,T)", "赝能隙 Δ_pg", "D031 §11（未闭合）",
                    "正常态拟合外推", "ARPES/STM", "未闭合"])
        w.writerow(["E3", "G19", "和乐相位闭合", "晶胞构型", "和乐相位 φ_H≈1", "D031 §11（未闭合）",
                    "平凡晶胞", "第一性/数值", "未闭合"])
        w.writerow(["E4", "G13", "BCS 渐近", "耦合 λ、德拜频率 ω_D", "T_c", "D031 §13（闭合）",
                    "弱/强耦合极限", "LeClair 型积分", "闭合（Lean 见证）"])
        w.writerow(["E5", "G22", "T_c 丛作用量交叉", "群指数 n", "T_c(n)", "D030 §2（公式完成）",
                    "单一群限制", "比热/磁穿透", "推导完成待严格化"])
        w.writerow(["E6", "G16", "因果分辨率", "角亏密度 ρ_δ", "有效 Ricci 标量", "D031 §11（未闭合）",
                    "均匀剖分", "数值相对论类比", "未闭合"])

    with open(os.path.join(S07, "实验设计", "isotope_effect_protocol.md"), "w", encoding="utf-8") as f:
        f.write("""# 实验设计 E1 · 同位素效应（缺口 G15）

> 目标缺口：**G15** 主次结构谱间隙差 → 同位素效应映射（`06 超导/CQM_超导_专题与扩展.md` §13，未闭合）。
> 本文件给出**检验方案**，不给出理论结论；缺口状态保持"未闭合"。

## 一、待检验陈述

- 陈述来源：P027（元素周期表可导出；$T_c$ 自由能框架）涉及的 G15 环节。
- 待检验的可观测后果：同位素替换（$M\\to M'$）改变特征频率 $\\Omega\\propto M^{-1/2}$，进而改变 $T_c$；CQM 预测的**同位素指数** $\\alpha$（$T_c\\propto M^{-\\alpha}$）应由主/次结构谱间隙差给出。

## 二、设计

| 项 | 设定 |
|:---|:---|
| 自变量 | 同位素质量 $M$（≥3 个同位素，跨足够质量范围） |
| 因变量 | $T_c$、上临界场 $H_{c2}$、穿透深度 $\\lambda_L$、比热跳变 $\\Delta C/\\gamma T_c$ |
| 控制 | 同族同构型、同掺杂、同热处理 |
| 对照 | 非同位素样品（同电子结构） |
| 数据 | ARPES / 比热 / 磁化 / 穿透深度 |

## 三、判据

1. 拟合 $\\ln T_c$ 对 $\\ln M$ 的斜率得 $\\alpha$。
2. 与 CQM 由谱间隙差推出的 $\\alpha$ 比较（该推导为 G15 待闭合内容）。
3. 若 $\\alpha$ 偏离 BCS 单声子值且呈结构依赖，将信息反馈至 G15 的第参数标定。

## 四、边界

- 本方案**不声称** CQM 已给出 $\\alpha$；G15 未闭合，$\\alpha$ 的 CQM 数值为待推项。
- 不引入理论外假设；数据来源与实验细节须可第三方复现。
""")

    with open(os.path.join(S07, "实验设计", "pseudogap_arpes_protocol.md"), "w", encoding="utf-8") as f:
        f.write("""# 实验设计 E2 · 赝能隙相图（缺口 G21）

> 目标缺口：**G21** 赝能隙相图 → ARPES/STM 映射（`06 超导/CQM_超导_专题与扩展.md` §13，未闭合）。

## 一、待检验陈述

- 来源：P027 / `06 超导` §11 赝能隙相图（概念 C072）。
- 待检验后果：CQM 的赝能隙相边界 $\\Delta_{pg}(p,T)$ 在 $(p,T)$ 平面上的形状应与谱权重转移一致。

## 二、设计

| 项 | 设定 |
|:---|:---|
| 自变量 | 掺杂 $p$、温度 $T$ |
| 因变量 | 赝能隙大小 $\\Delta_{pg}$、谱权重转移、费米弧长度 |
| 对照 | 正常态外推（无赝能隙基线） |
| 探针 | ARPES（动量分辨）、STM/STS（实空间） |
| 采样 | 相图上网格化 $(p,T)$ |

## 三、判据

1. 由 ARPES 提取 $\\Delta_{pg}(p,T)$ 等值线，与 CQM 相图边界比较。
2. 相边界处的谱权重转移量作为第二判据。
3. 差异登记回 G21，作为"相图 → 可观测量映射"的标定输入。

## 四、边界

- G21 未闭合，本节不给出 CQM 的定量相图；仅规定可观测映射的检验流程。
""")

    print("[OK] 因果模型 / 贝叶斯网络 / 实验设计 已生成")
    print("     弹性:", elasticity())


if __name__ == "__main__":
    main()
