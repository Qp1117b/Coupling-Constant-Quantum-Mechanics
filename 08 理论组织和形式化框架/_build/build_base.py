# -*- coding: utf-8 -*-
"""
CQM 理论组织与形式化框架 · 基座重建脚本
从 01_结构化数据/*.csv 用标准 CSV 解析重建 03_超图与理论图/超图数据.json。
修复旧 JSON 因 naive 逗号切分导致的字段错位（含逗号字段被拆坏）。
运行：python build_base.py
"""
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S01 = os.path.join(ROOT, "01_结构化数据")
S03 = os.path.join(ROOT, "03_超图与理论图")


def read_csv(name):
    path = os.path.join(S01, name)
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    concepts = read_csv("概念表.csv")
    props = read_csv("命题表.csv")
    args = read_csv("论证表.csv")

    # ---- 断言预检 ----
    assert len(concepts) == 82, f"概念表应为 82 行，实为 {len(concepts)}"
    assert len(props) == 63, f"命题表应为 63 行，实为 {len(props)}"
    assert len(args) == 70, f"论证表应为 70 行，实为 {len(args)}"
    # 概念 id 连续无重
    cids = [c["concept_id"] for c in concepts]
    assert len(set(cids)) == len(cids), "概念 id 有重复"
    # 论证表引用的 concept 必须存在
    for a in args:
        for tok in a["source_concept"].replace("→", ";").split(";"):
            tok = tok.strip()
            if tok.startswith("C") and tok not in cids:
                raise AssertionError(f"论证 {a['arg_id']} 引用了不存在的概念 {tok}")

    # 关系类型分类：⇒ 仅表重组实现；premises/conclusion 用概念 ID（从 source_concept 解析）
    REL_HYPER = "重组实现"
    hyper, directed = [], []
    for a in args:
        sc = a["source_concept"]
        if "→" in sc:
            left, right = sc.split("→", 1)
            src_ids = [c.strip() for c in left.split(";") if c.strip()]
            tgt_ids = [c.strip() for c in right.split(";") if c.strip()]
        else:
            src_ids = [c.strip() for c in sc.split(";") if c.strip()]
            tgt_ids = []
        prem_labels = [p.strip() for p in a["premises"].split(";") if p.strip()]
        concl_label = a["conclusion"].strip()
        src_docs = [d.strip() for d in a["source_doc"].split(";") if d.strip()]
        if a["type"] == REL_HYPER:
            hyper.append({"id": a["arg_id"], "premises": src_ids, "conclusion": tgt_ids,
                           "premises_label": prem_labels, "conclusion_label": concl_label,
                           "type": a["type"], "source_doc": src_docs, "source_concept": sc})
        else:
            directed.append({"id": a["arg_id"], "source": src_ids[0] if src_ids else "",
                               "target": tgt_ids[0] if tgt_ids else "",
                               "source_label": prem_labels[0] if prem_labels else "",
                               "target_label": concl_label, "type": a["type"],
                               "source_doc": src_docs[0] if src_docs else "",
                               "source_concept": sc})

    nodes = []
    for c in concepts:
        nodes.append({
            "id": c["concept_id"],
            "label": c["name"],
            "type": c["type"],
            "definition": c["definition"],
            "source_doc": c["source_doc"],
            "source_loc": c["source_loc"],
            "synonyms": [s.strip() for s in c.get("synonyms", "").split(",") if s.strip()],
        })

    doc = {
        "metadata": {
            "project": "CQMFormal",
            "format": "XGI-compatible",
            "note": "由 _build/build_base.py 从 01_结构化数据/*.csv 标准 CSV 解析重建；⇒ 仅表重组实现（有向超边），其余为普通有向边。",
            "node_count": len(nodes),
            "hyperedge_count": len(hyper),
            "directed_edge_count": len(directed),
            "relation_type_histogram": {},
        },
        "nodes": nodes,
        "hyperedges": hyper,
        "directed_edges": directed,
    }
    hist = {}
    for h in hyper:
        hist[REL_HYPER] = hist.get(REL_HYPER, 0) + 1
    for d in directed:
        hist[d["type"]] = hist.get(d["type"], 0) + 1
    doc["metadata"]["relation_type_histogram"] = hist

    out = os.path.join(S03, "超图数据.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)

    print(f"[OK] nodes={len(nodes)} hyperedges={len(hyper)} directed={len(directed)}")
    print("     关系类型直方图:", hist)
    print("     写出:", out)


if __name__ == "__main__":
    main()
