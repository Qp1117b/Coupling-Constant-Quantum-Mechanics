# -*- coding: utf-8 -*-
"""
维度 02 · 概念本体构建
从 01_结构化数据/{概念表,命题表,论证表}.csv 生成 OWL 本体（owlready2）与概念关系图（networkx+matplotlib）。
产出：
  02_概念本体/本体.owl
  02_概念本体/概念关系图.png
  02_概念本体/本体统计.json
运行：python build_ontology.py
"""
import csv
import json
import os
import collections

from owlready2 import get_ontology, Thing, ObjectProperty, AnnotationProperty
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S01 = os.path.join(ROOT, "01_结构化数据")
S02 = os.path.join(ROOT, "02_概念本体")

for fam in ["Microsoft YaHei", "SimHei", "SimSun"]:
    try:
        font_manager.findfont(fam, fallback_to_default=False)
        plt.rcParams["font.sans-serif"] = [fam]
        break
    except Exception:
        continue
plt.rcParams["axes.unicode_minus"] = False

# 概念类型 → 稳定英文类名
CTYPE_NAME = {
    "本体论": "OntologyConcept", "理论框架": "FrameworkConcept", "数学结构": "MathStructureConcept",
    "群论": "GroupTheoryConcept", "关系类型": "RelationTypeConcept", "引力层级": "GravityLevelConcept",
    "纤维丛": "FiberBundleConcept", "几何": "GeometryConcept", "量纲": "DimensionConcept",
    "数论": "NumberTheoryConcept", "物理": "PhysicsConcept", "共形场论": "CFTConcept",
}
PTYPE_NAME = {
    "定理": "Theorem", "命题": "Statement", "假设": "Hypothesis",
    "构造": "Construction", "缺口": "GapItem", "猜想": "Conjecture", "占位": "Placeholder",
}
# 关系类型 → 对象属性名（二元）
REL_AS_PROP = {"演化": "evolvesTo", "映射": "mapsTo", "等价": "equivalentTo",
               "依赖": "dependsOn", "层级含于": "subsumedIn"}


def read_csv(name):
    with open(os.path.join(S01, name), "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def build_owl(concepts, props, args):
    onto = get_ontology("http://cqm.local/ontology")
    with onto:
        class Concept(Thing):
            """概念实体"""
        class Proposition(Thing):
            """命题 / 定理 / 假设 / 构造 / 猜想"""
        class Gap(Proposition):
            """缺口（C/G2–G8、G9–G22、N1–N4、H3.1–H3.3）"""
        class Argument(Thing):
            """论证单元（前提集合 → 结论 的二元或文本化表示）"""
        class Hyperedge(Thing):
            """有向超边（⇒ 重组实现，多因一果）"""
        class RelationType(Thing):
            """关系类型元类"""

        ctype_cls = {t: type(CTYPE_NAME[t], (Concept,), {}) for t in sorted({c["type"] for c in concepts})}
        ptype_cls = {}
        for t in sorted({p["type"] for p in props}):
            base = Gap if t == "缺口" else Proposition
            ptype_cls[t] = type(PTYPE_NAME[t], (base,), {})

        obj_props = {rt: type(pn, (ObjectProperty,), {}) for rt, pn in REL_AS_PROP.items()}
        has_premise = type("hasPremise", (ObjectProperty,), {})
        has_conclusion = type("hasConclusion", (ObjectProperty,), {})
        sourceDoc = type("sourceDoc", (AnnotationProperty,), {})
        sourceLoc = type("sourceLoc", (AnnotationProperty,), {})
        definition = type("definition", (AnnotationProperty,), {})
        synonyms = type("synonyms", (AnnotationProperty,), {})
        status = type("status", (AnnotationProperty,), {})
        premisesText = type("premisesText", (AnnotationProperty,), {})
        conclusionText = type("conclusionText", (AnnotationProperty,), {})
        relationType = type("relationType", (AnnotationProperty,), {})

        # 概念个体
        cind = {}
        for c in concepts:
            ind = ctype_cls[c["type"]](c["concept_id"], namespace=onto)
            ind.label = [c["name"]]
            if c["definition"]:
                definition[ind] = [c["definition"]]
            if c["source_doc"]:
                sourceDoc[ind] = [c["source_doc"]]
            if c["source_loc"]:
                sourceLoc[ind] = [c["source_loc"]]
            if c.get("synonyms"):
                synonyms[ind] = [c["synonyms"]]
            cind[c["concept_id"]] = ind
        # 命题个体
        for p in props:
            ind = ptype_cls.get(p["type"], Proposition)(p["prop_id"], namespace=onto)
            ind.label = [p["statement"]]
            status[ind] = [p["status"]]
            if p["source_doc"]:
                sourceDoc[ind] = [p["source_doc"]]
            if p["depends_on"]:
                for dep in [x.strip() for x in p["depends_on"].split(";") if x.strip()]:
                    if dep in cind:
                        ind.dependsOn = [cind[dep]]
        # 论证个体
        ctype_of = {c["concept_id"]: c["type"] for c in concepts}
        for a in args:
            pts = [x.strip() for x in a["premises"].split(";") if x.strip()]
            if a["type"] == "重组实现":
                h = Hyperedge(a["arg_id"], namespace=onto)
                h.label = [a["premises"] + " ⇒ " + a["conclusion"]]
                premisesText[h] = [a["premises"]]
                conclusionText[h] = [a["conclusion"]]
                sourceDoc[h] = a["source_doc"]
            else:
                rel = Argument(a["arg_id"], namespace=onto)
                rel.label = [a["premises"] + " → " + a["conclusion"]]
                premisesText[rel] = [a["premises"]]
                conclusionText[rel] = [a["conclusion"]]
                relationType[rel] = [a["type"]]
                sourceDoc[rel] = a["source_doc"]
                # 若 source_concept 两端可解析为概念 id，则连二元对象属性
                ids = [x for x in a["source_concept"].replace(";", "→").split("→") if x.strip().startswith("C")]
                ids = [x for x in ids if x in cind]
                if len(ids) >= 2 and a["type"] in REL_AS_PROP:
                    pname = REL_AS_PROP[a["type"]]
                    setattr(cind[ids[0]], pname, [cind[ids[-1]]])
    return onto


def build_type_graph(concepts, args):
    ctype_of = {c["concept_id"]: c["type"] for c in concepts}
    G = nx.DiGraph()
    for c in concepts:
        G.add_node(c["type"], n=sum(1 for x in concepts if x["type"] == c["type"]))
    cnt = collections.Counter()
    for a in args:
        ids = [x for x in a["source_concept"].replace(";", "→").split("→") if x.strip().startswith("C")]
        if len(ids) >= 2:
            s, t = ctype_of.get(ids[0]), ctype_of.get(ids[-1])
            if s and t:
                cnt[(s, t)] += 1
    for (s, t), w in cnt.items():
        G.add_edge(s, t, w=G[s][t]["w"] + w if G.has_edge(s, t) else w)
    return G, cnt


def main():
    concepts = read_csv("概念表.csv")
    props = read_csv("命题表.csv")
    args = read_csv("论证表.csv")
    assert len(concepts) == 82 and len(props) == 63 and len(args) >= 41

    onto = build_owl(concepts, props, args)
    out = os.path.join(S02, "本体.owl")
    onto.save(file=out, format="rdfxml")

    G, cnt = build_type_graph(concepts, args)
    fig, ax = plt.subplots(figsize=(13, 9.5), dpi=150)
    pos = nx.spring_layout(G, seed=7, k=1.1)
    sizes = [500 + 130 * G.nodes[n]["n"] for n in G.nodes]
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=sizes, node_color="#cfe0f5",
                           edgecolors="#4a6d99", linewidths=1.2)
    nx.draw_networkx_labels(G, pos, ax=ax,
                            labels={n: f"{n}\n({G.nodes[n]['n']})" for n in G.nodes}, font_size=10)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#8a8a8a", arrows=True, arrowsize=12,
                           width=[0.8 + 0.45 * G[s][t]["w"] for s, t in G.edges],
                           connectionstyle="arc3,rad=0.08")
    ax.set_title("CQM 概念类型关系图（节点=概念类型及概念数；边=论证表跨类型关系计数，共 %d 条）" % sum(cnt.values()),
                 fontsize=13)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(os.path.join(S02, "概念关系图.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)

    ctypes = sorted({c["type"] for c in concepts})
    ptypes = sorted({p["type"] for p in props})
    rtypes = sorted({a["type"] for a in args})
    stat = {
        "concept_count": len(concepts), "proposition_count": len(props), "argument_count": len(args),
        "concept_types": ctypes, "proposition_types": ptypes, "relation_types": rtypes,
        "type_hist": {t: sum(1 for c in concepts if c["type"] == t) for t in ctypes},
        "prop_type_hist": {t: sum(1 for p in props if p["type"] == t) for t in ptypes},
        "rel_type_hist": {t: sum(1 for a in args if a["type"] == t) for t in rtypes},
        "owl_classes": len(list(onto.classes())),
        "owl_individuals": len(list(onto.individuals())),
        "owl_object_properties": len(list(onto.object_properties())),
        "cross_type_edges": sum(cnt.values()),
    }
    with open(os.path.join(S02, "本体统计.json"), "w", encoding="utf-8") as f:
        json.dump(stat, f, ensure_ascii=False, indent=2)
    print("[OK] 本体.owl / 概念关系图.png / 本体统计.json")
    print("  类=%d 个体=%d 对象属性=%d 跨类型边=%d" % (
        stat["owl_classes"], stat["owl_individuals"], stat["owl_object_properties"], stat["cross_type_edges"]))


if __name__ == "__main__":
    main()
