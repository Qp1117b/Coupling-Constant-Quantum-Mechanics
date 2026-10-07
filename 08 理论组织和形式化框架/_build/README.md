# _build · 可复现构建脚本

> 本目录是 `08 理论组织和形式化框架/` 的可复现构建工具（不计入产品文件统计）。
> 全部脚本从 `01_结构化数据/*.csv`、`03_超图与理论图/`、`04_Lean对接/` 与外部 `08 理论组织和形式化框架/04_Lean对接/Lean源码/` 源码生成产物；**不改动外部理论文本**。

## 运行环境

- Python 3.14（`C:/Python314/python.exe`，已装 `numpy`、`networkx`、`matplotlib`、`owlready2`、`scipy`、`PIL`）。
- 无外部 Graphviz `dot` 二进制（静态图由 networkx+matplotlib 渲染）。

## 执行顺序

```bash
python check_consistency.py  # 组织层硬检查（23 项；必过，退出码 0）
python fix_csv.py          # 一次性：修复源 CSV 6 行未转义逗号（幂等，已修则跳过断言）
python build_base.py       # 超图数据.json（标准 CSV 解析）
python build_ontology.py   # 02：本体.owl / 概念关系图.png / 本体统计.json
python build_lean.py       # 03：Lean 结构提取 / 映射 / 蓝图
python build_ml.py         # ML 数据准备：特征 / 索引 / 证明数据集 / 嵌入就绪
python build_dynamics.py   # 动态机制：重写规则 / 状态模型 / 仿真
python build_causal.py     # 经验检验：因果模型 / 贝叶斯网络 / 实验设计
python build_bridge.py     # 桥接与翻译：符号表 / 等价映射 / 概念映射
python build_site.py       # 输出可视化展示：网站 / 交互超图 / 蓝图拷贝
python build_reader.py     # 输出可视化展示：离线阅读站（读 README + 01–07 + 附录 文本，不进入源 CSV 闭环）
python build_meta.py       # 元数据：manifest / 版本 / 变更日志 / 验证状态
```

## 说明

- 各脚本内部含**断言预检**（如 82/63/70 行数），不符即中止。
- `check_consistency.py` 是 `10/AGENTS.md` §八 完成判据的执行器，跨产物核对计数一致性、引用完整性、`⇒`/`→` 约定、维度覆盖、失效链接与禁用词；**未通过即视为研究未完成**。
- `fix_csv.py` 为一次性修复脚本，**幂等**：已修复行重写为同一正确值，重复运行不产生新的改动。
