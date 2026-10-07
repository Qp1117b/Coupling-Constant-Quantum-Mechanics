# -*- coding: utf-8 -*-
"""
维度 02 · 机器学习数据准备（只转格式，不训练模型）
从 01/03/04 的结构化数据导出 ML 就绪格式。
产出（05_机器学习数据准备/）：
  超图导出/node_features.csv
  超图导出/hyperedge_index.csv
  超图导出/directed_edge_index.csv
  超图导出/heterodata.json
  超图导出/hypergraph_index.npz
  超图导出/build_pyg.py
  证明数据集/前提-结论对.jsonl
  证明数据集/命题-证明对.jsonl
  证明数据集/lean声明.jsonl
  嵌入就绪/节点特征矩阵.csv
  嵌入就绪/README.md
运行：python build_ml.py
"""
import csv
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S01 = os.path.join(ROOT, "01_结构化数据")
S03 = os.path.join(ROOT, "03_超图与理论图")
S04 = os.path.join(ROOT, "04_Lean对接")
S05 = os.path.join(ROOT, "05_机器学习数据准备")


def read_csv(path, enc="utf-8-sig"):
    with open(path, "r", encoding=enc, newline="") as f:
        return list(csv.DictReader(f))


def concept_ids(txt):
    # 保留自环（如 C048→C048、C013→C013），不做去重
    return [tok.strip() for tok in txt.replace(";", "→").split("→")
            if tok.strip().startswith("C")]


def main():
    for d in ["超图导出", "证明数据集", "嵌入就绪"]:
        os.makedirs(os.path.join(S05, d), exist_ok=True)

    concepts = read_csv(os.path.join(S01, "概念表.csv"))
    args = read_csv(os.path.join(S01, "论证表.csv"))
    props = read_csv(os.path.join(S01, "命题表.csv"))
    hg = json.load(open(os.path.join(S03, "超图数据.json"), encoding="utf-8"))

    idx = {c["concept_id"]: i for i, c in enumerate(concepts)}
    types = sorted({c["type"] for c in concepts})
    tid = {t: i for i, t in enumerate(types)}
    N, T = len(concepts), len(types)

    # ---- 邻接统计 ----
    d_out = np.zeros(N, dtype=int)
    d_in = np.zeros(N, dtype=int)
    d_hyper = np.zeros(N, dtype=int)
    he = []   # (node_idx, hyperedge_idx)
    de = []   # (src, dst)
    hid = 0
    for a in args:
        ids = concept_ids(a["source_concept"])
        if not ids:
            continue
        if a["type"] == "重组实现":
            srcs, dst = ids[:-1], ids[-1]
            for s in srcs:
                he.append((idx[s], hid)); d_hyper[idx[s]] += 1
            he.append((idx[dst], hid)); d_hyper[idx[dst]] += 1
            d_out[[idx[s] for s in srcs]] += 1
            d_in[idx[dst]] += 1
            hid += 1
        elif len(ids) >= 2:
            s, dst = ids[0], ids[-1]
            de.append((idx[s], idx[dst])); d_out[idx[s]] += 1; d_in[idx[dst]] += 1

    # ---- node_features ----
    with open(os.path.join(S05, "超图导出", "node_features.csv"), "w", encoding="utf-8-sig", newline="") as f:
        cols = ["node_idx", "concept_id", "label", "type", "d_in", "d_out", "d_hyper"] + ["type_" + t for t in types]
        w = csv.writer(f); w.writerow(cols)
        for i, c in enumerate(concepts):
            oh = [1 if c["type"] == t else 0 for t in types]
            w.writerow([i, c["concept_id"], c["name"], c["type"], d_in[i], d_out[i], d_hyper[i]] + oh)

    # ---- 特征矩阵 ----
    X = np.zeros((N, T + 3), dtype=np.float32)
    for i, c in enumerate(concepts):
        X[i, tid[c["type"]]] = 1.0
        X[i, T + 0] = d_in[i]; X[i, T + 1] = d_out[i]; X[i, T + 2] = d_hyper[i]
    with open(os.path.join(S05, "嵌入就绪", "节点特征矩阵.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["node_idx", "concept_id"] + [f"f{j}" for j in range(X.shape[1])])
        for i, c in enumerate(concepts):
            w.writerow([i, c["concept_id"]] + [f"{v:g}" for v in X[i]])

    # ---- hyperedge_index / directed_edge_index ----
    he_arr = np.array(he, dtype=np.int64).T if he else np.zeros((2, 0), dtype=np.int64)
    de_arr = np.array(de, dtype=np.int64).T if de else np.zeros((2, 0), dtype=np.int64)
    with open(os.path.join(S05, "超图导出", "hyperedge_index.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f); w.writerow(["node_idx", "hyperedge_idx"]); w.writerows(he)
    with open(os.path.join(S05, "超图导出", "directed_edge_index.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f); w.writerow(["src_node_idx", "dst_node_idx"]); w.writerows(de)
    np.savez(os.path.join(S05, "超图导出", "hypergraph_index.npz"),
             hyperedge_index=he_arr, edge_index=de_arr, x=X,
             num_nodes=np.array([N]), num_hyperedges=np.array([hid]),
             num_classes=np.array([T]))

    heterodata = {
        "schema": "PyG HeteroData / HypergraphData（见 build_pyg.py 的构造约定）",
        "node_types": {"concept": {"num_nodes": N, "feature_dim": T + 3, "type_vocab": types}},
        "edge_types": {
            "concept__reified_in__hyperedge": {"num_hyperedges": hid, "num_incidences": len(he)},
            "concept__directed__concept": {"num_edges": len(de)},
        },
        "features": {"x_shape": list(X.shape), "type_onehot_dim": T, "degree_features": ["d_in", "d_out", "d_hyper"]},
        "maps": {"concept_id_to_idx": idx, "type_to_col": tid},
    }
    with open(os.path.join(S05, "超图导出", "heterodata.json"), "w", encoding="utf-8") as f:
        json.dump(heterodata, f, ensure_ascii=False, indent=2)

    # ---- 证明数据集 ----
    with open(os.path.join(S05, "证明数据集", "前提-结论对.jsonl"), "w", encoding="utf-8") as f:
        for a in args:
            ids = concept_ids(a["source_concept"])
            if not ids:
                continue
            f.write(json.dumps({
                "id": a["arg_id"], "relation": a["type"],
                "premises": [x.strip() for x in a["premises"].split(";") if x.strip()],
                "conclusion": a["conclusion"],
                "premise_concept_ids": ids[:-1], "conclusion_concept_id": ids[-1],
                "source_doc": [d.strip() for d in a["source_doc"].split(";") if d.strip()],
                "is_recomposition": a["type"] == "重组实现",
            }, ensure_ascii=False) + "\n")

    lean_map = read_csv(os.path.join(S04, "Lean↔概念映射.csv"))
    witness = {}
    for r in lean_map:
        for cid in r["concept_ids"].split(";"):
            witness.setdefault(cid.strip(), []).append({"library": r["lean_library"], "symbol": r["lean_symbol"]})
    with open(os.path.join(S05, "证明数据集", "命题-证明对.jsonl"), "w", encoding="utf-8") as f:
        for p in props:
            f.write(json.dumps({
                "prop_id": p["prop_id"], "statement": p["statement"], "type": p["type"],
                "status": p["status"], "source_doc": p["source_doc"],
                "depends_on": [x.strip() for x in p["depends_on"].split(";") if x.strip()],
                "lean_witness": next((witness[c] for c in concept_ids(p["statement"]) if c in witness), None),
            }, ensure_ascii=False) + "\n")

    decls = json.load(open(os.path.join(S04, "Lean结构提取", "declarations.json"), encoding="utf-8"))
    with open(os.path.join(S05, "证明数据集", "lean声明.jsonl"), "w", encoding="utf-8") as f:
        for d in decls:
            f.write(json.dumps({**d, "is_proof": d["kind"] in ("theorem", "lemma"),
                                "is_axiom": d["kind"] == "axiom"}, ensure_ascii=False) + "\n")

    # ---- build_pyg.py ----
    write_build_pyg(os.path.join(S05, "超图导出", "build_pyg.py"))
    write_embed_readme(os.path.join(S05, "嵌入就绪", "README.md"), N, T, hid, len(he), len(de))

    print(f"[OK] N={N} T={T} hyperedges={hid} incidences={len(he)} directed={len(de)}")
    print(f"     x.shape={X.shape}  npz/heterodata/jsonl 已写出")


def write_build_pyg(path):
    open(path, "w", encoding="utf-8").write('''# -*- coding: utf-8 -*-
"""
把 超图导出/ 里的 (x, hyperedge_index, edge_index) 装配为 PyG / DGL 对象。
依赖（较重，按需安装）：pip install torch torch-geometric
本脚本只在安装 torch 后运行；未安装时以 .npz 为源数据。
"""
import numpy as np, json, os

def load():
    z = np.load(os.path.join(os.path.dirname(__file__), "hypergraph_index.npz"))
    return z["x"], z["hyperedge_index"], z["edge_index"]

def to_pyg():
    import torch
    from torch_geometric.data import Data, HypergraphData
    x, hei, ei = load()
    x = torch.tensor(x, dtype=torch.float)
    hei = torch.tensor(hei, dtype=torch.long)
    ei = torch.tensor(ei, dtype=torch.long)
    hyper = HypergraphData(x=x, hyperedge_index=hei)
    graph = Data(x=x, edge_index=ei)
    return hyper, graph

def to_dgl():
    import dgl, torch
    x, hei, ei = load()
    g = dgl.graph((torch.tensor(ei[0]), torch.tensor(ei[1])))
    g.ndata["feat"] = torch.tensor(x, dtype=torch.float)
    hg = dgl.DGLGraph()  # 超图请用 dgl 的二分图构造（节点 = 概念 ∪ 超边）
    return g, hg

if __name__ == "__main__":
    h, g = to_pyg()
    print(h, g)
''', )


def write_embed_readme(path, N, T, H, inc, de):
    open(path, "w", encoding="utf-8").write(f'''# 嵌入就绪（ML 数据准备）

> 本目录给出可直接喂入图/超图神经网络的**数据准备**产物，不训练任何模型。
> 节点 = CQM 概念（{N} 个）；超边 = `⇒` 重组实现（{H} 条，{inc} 次关联）；有向边 = 演化/映射/等价/依赖/层级含于（{de} 条）。

## 一、文件

| 文件 | 内容 | 形状 / 格式 |
|:---|:---|:---|
| `节点特征矩阵.csv` | 节点特征 $X$ | {N} × {T + 3} |
| `../超图导出/hypergraph_index.npz` | `x` / `hyperedge_index` / `edge_index` | numpy npz |
| `../超图导出/heterodata.json` | 异构图 schema 与映射 | JSON |
| `../超图导出/node_features.csv` | 可读节点特征 | CSV |

## 二、节点特征 $X$（{N} × {T + 3}）

- 前 {T} 维：概念类型 one-hot（{T} 类，见 `heterodata.json` → `type_vocab`）。
- 末 3 维：度数特征 `d_in`（入度）、`d_out`（出度）、`d_hyper`（超边关联数）。

若需稠密语义特征，可在此之上叠加文档来源 one-hot（`source_doc`）或术语表嵌入；本目录不含语义嵌入，以免引入理论外信息。

## 三、超图索引约定（PyG `HypergraphData` / DGL 二分图）

- `hyperedge_index`：形状 `[2, {inc}]`，第 0 行 = 节点下标，第 1 行 = 超边下标；每条超边同时包含其前件节点与后件节点。
- `edge_index`：形状 `[2, {de}]`，普通有向边 `(src, dst)`。
- `⇒` 与 `→` **不得**合并为同一张简单图：前者是多元超边，后者是二元边。

## 四、推荐方法（对接已有开源框架）

| 层次 | 方法/框架 | 说明 |
|:---|:---|:---|
| 超图神经网 | AllSet（多集 → 超图） | 设计文档列为超图神经网络数据准备首选 |
| 超图卷积 | HyperGCN / HGNN（PyG / DGL 实现） | 以 `hyperedge_index` 直接构图 |
| 异构图 | PyG `HeteroData` | 概念节点 + 超边节点的二分异构图 |
| 边预测 / 链接 | PyG / DGL 通用 | 以 `edge_index` 为监督信号 |
| 语言模型 | 不训练（本项目只做数据准备） | —— |

> 数据规模（{N} 节点）适合小图方法；避免过参数化模型。缺口、axiom 等状态字段**不改写**，可作为节点标签用于监督任务。
''')


if __name__ == "__main__":
    main()
