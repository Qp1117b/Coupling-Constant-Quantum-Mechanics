# _build · 可复现构建脚本

> 本目录是 `08 理论组织和形式化框架/` 的可复现构建工具（不计入产品文件统计）。
> 全部脚本从 `01_结构化数据/*.csv`、`03_超图与理论图/`、`04_Lean对接/` 与外部 `08 理论组织和形式化框架/04_Lean对接/Lean源码/` 源码生成产物；**不改动外部理论文本**。

## 运行环境

- Python 3.14（`C:/Python314/python.exe`，已装 `numpy`、`networkx`、`matplotlib`、`owlready2`、`scipy`、`PIL`）。
- 无外部 Graphviz `dot` 二进制（静态图由 networkx+matplotlib 渲染）。

## 执行顺序

```bash
python check_consistency.py  # 组织层硬检查（41 项；必过，退出码 0）
python check_provenance.py   # 证据层硬检查（无复核文件 10 项 / 有复核结果 13 项；引文必须逐字等于原文区间）
python fix_csv.py          # 一次性：修复源 CSV 6 行未转义逗号（幂等，已修则跳过断言）
python build_base.py       # 超图数据.json（标准 CSV 解析）
python build_evidence.py   # 00：语料指纹 / 章节索引 / 句索引 / 证据映射（只读理论文本）
python build_claims.py     # 01：缺口编号对照 / 缺口依赖 / 命题依赖 / 别名 / 论证对齐 + 03/知识图谱.json
python build_ontology.py   # 02：本体.owl（含 domain/range/逆属性/互斥/限制公理）+ 概念关系图.png + HermiT 一致性
python build_kg.py         # 02/03：知识图谱.ttl（SKOS+PROV）/ shapes.shacl.ttl / pyshacl 校验 / SPARQL CQ1–CQ9
python build_lean.py       # 04：Lean 结构提取 / 映射 / 蓝图
python build_ml.py         # 05：特征 / 索引 / 证明数据集 / 嵌入就绪
python build_extract.py    # 05：术语候选（新词发现+C-value）/ 分层关系抽取与评测 / 语义特征与近邻 / 零覆盖语料候选
python llm_extract.py      # 05：LLM 关系定型（就绪管线；无 CQM_LLM_* 环境变量时打印就绪说明并退出 0，不谎报执行）
python build_dynamics.py   # 06：重写规则 / 状态模型 / 仿真
python build_causal.py     # 07：因果模型 / 贝叶斯网络 / 实验设计
python build_bridge.py     # 09：符号表 / 等价映射 / 概念映射
python build_site.py       # 10：研究驾驶舱 / 可推演多层超图 / 蓝图拷贝（含级联复算断言）
python build_search.py     # 10：检索台（图谱 + BM25 全文 + 证据 + 质量 + SPARQL）
python build_reader_site.py # 10：离线阅读站（Material for MkDocs：jieba 分词搜索 + offline/privacy，只读 01–07 文本）
python build_meta.py       # 11：manifest / 版本 / 变更日志 / 验证状态
```

> `build_reader.py`（v1.7 自研单页阅读站）自 **v1.8.0 起由 `build_reader_site.py` 接替**，保留存档不再执行。

## 说明

- 各脚本内部含**断言预检**（如 82/63/70 行数、级联累计可达 = 06 仿真值），不符即中止。
- `check_consistency.py` 是 `10/AGENTS.md` §八 完成判据的执行器，跨产物核对计数一致性、引用完整性、`⇒`/`→` 约定、维度覆盖、失效链接与禁用词，并覆盖 v1.7.0 新增的证据层/主张层/RDF/SHACL/HermiT/抽取；**未通过即视为研究未完成**。
- `check_provenance.py` 是**证据层执行器**：断言覆盖、引文逐字一致、字符区间边界、方法枚举、跨文档标记，
  以及**人工复核闭环**（存在 `00_外部引用/复核结果.csv` 时：`verified ⟺ approved 且有复核人`；不存在时：`verified` 全为 `False`）；**未通过即视为证据层未完成**。
- 依赖：`rdflib`、`pyshacl`（RDF 导出与 SHACL 校验）、`jieba`（中文分词）、`owlready2` + **Java**（HermiT 推理）、`mkdocs-material`（阅读站，pip 安装）。缺失时对应脚本会如实报错，不静默降级。
- `llm_extract.py` 依赖可选的 OpenAI 兼容 API（`CQM_LLM_API_BASE/KEY/MODEL`）；其输出（`LLM定型候选.csv`）经 **span 校验**后仍只是候选，须人工确认。
- `fix_csv.py` 为一次性修复脚本，**幂等**：已修复行重写为同一正确值，重复运行不产生新的改动。
