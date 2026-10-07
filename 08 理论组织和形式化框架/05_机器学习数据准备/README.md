# 05 · 机器学习数据准备

> 维度 2。把超图与证明转成 ML 就绪格式，**只转格式、不训练模型**。

| 目录 | 文件 | 内容 |
|:---|:---|:---|
| `超图导出/` | `node_features.csv` | 82 节点 × (12 类型 one-hot + 3 度数) |
| | `hyperedge_index.csv` | 节点↔超边关联（47 次） |
| | `directed_edge_index.csv` | 有向边（51 条） |
| | `hypergraph_index.npz` | `x` / `hyperedge_index` / `edge_index` 张量 |
| | `heterodata.json` | 异构图 schema 与 id 映射 |
| | `build_pyg.py` | PyG/DGL 装配脚本（依赖 torch，未安装时以 npz 为准） |
| `证明数据集/` | `前提-结论对.jsonl` | 70 条论证（含概念 id 链） |
| | `命题-证明对.jsonl` | 63 条命题 + Lean 见证 |
| | `lean声明.jsonl` | 1388 条 Lean 声明 |
| `嵌入就绪/` | `节点特征矩阵.csv`、`README.md` | 特征矩阵、推荐方法（AllSet/HyperGCN/HGNN） |

**约定**：`⇒` 与 `→` 不得合并为同一张简单图（超边 vs 二元边）。构建：`_build/build_ml.py`。
