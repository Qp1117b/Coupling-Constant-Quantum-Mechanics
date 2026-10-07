# 07 · 经验检验

> 维度 6。把理论预测与数据接口对接：结构因果模型、贝叶斯网络、实验设计。**不产生新物理结论**。

| 目录 | 文件 | 内容 |
|:---|:---|:---|
| `因果模型/` | `GN_causal_dag.json` | $G_N$ 结构因果模型（变量/边/弹性） |
| | `dowhy_model.py` | 敏感性与反事实（对接 DoWhy） |
| | `README.md` | $G_N$ 公式、因果图、对数弹性表 |
| `贝叶斯网络/` | `gap_closure_model.bif` | 缺口闭合网络（BIF，结构取自缺口依赖图） |
| | `infer.py` | 后验推断（对接 pgmpy） |
| | `network_spec.md` | 节点、结构、CPT 说明 |
| `实验设计/` | `design_matrix.csv` | 6 项实验（E1–E6） |
| | `isotope_effect_protocol.md` | 同位素效应（缺口 G15） |
| | `pseudogap_arpes_protocol.md` | 赝能隙相图（缺口 G21） |

**边界**：$G_N$ 数值带"构造后验数字校验，待独立复现"；贝叶斯 CPT 为占位（待标定），其输出非理论结论。构建：`_build/build_causal.py`。
