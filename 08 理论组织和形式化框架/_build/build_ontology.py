# -*- coding: utf-8 -*-
"""
维度 02 · 概念本体构建（含公理层与推理校验）
从 `01_结构化数据/*.csv` 与证据/claim 层生成 OWL 本体、概念关系图与校验统计。

产出：
  02_概念本体/本体.owl          类层次 + 个体 + 对象属性（domain/range/逆属性）+ 限制公理 + 互斥类
  02_概念本体/概念关系图.png
  02_概念本体/本体统计.json     含公理计数与 HermiT 一致性/分类检查结果

公理层说明（不引入任何理论外内容，只是把既有关系的**类型约束**显式化）：
  · 每个对象属性声明 domain/range 与逆属性；
  · 12 个概念类型声明为互斥类（源数据每概念恰属一类，属组织层分类约定）；
  · Hyperedge ⊑ (hasPremise min 1 Concept) ⊓ (hasConclusion min 1 Concept)；
  · 缺口前置 gapPrecedes 由「缺口依赖闭包.md §二」与命题表 depends_on 给出。

运行：python build_ontology.py
"""
import csv
import json
import os
import re
import collections

from owlready2 import (get_ontology, Thing, ObjectProperty, AnnotationProperty, AllDisjoint,
                       sync_reasoner, Nothing)
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S00 = os.path.join(ROOT, "00_外部引用")
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
# 注意：论证表里的「依赖」是**概念→概念**，与命题表的「命题→概念 dependsOn」语义不同，
# 必须拆成两个属性，否则 RDFS 定义域推理会把概念判成命题（SHACL 已实测暴露该冲突）。
REL_AS_PROP = {"演化": "evolvesTo", "映射": "mapsTo", "等价": "equivalentTo",
               "依赖": "conceptDependsOn", "层级含于": "subsumedIn"}


def read_csv(name, base=None):
    with open(os.path.join(base or S01, name), "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def build_owl(concepts, props, args, gap_edges, claim_rows, ev_rows):
    onto = get_ontology("http://cqm.local/ontology")
    with onto:
        class Concept(Thing):
            """概念实体"""
        class Proposition(Thing):
            """命题 / 定理 / 假设 / 构造 / 猜想"""
        class Gap(Proposition):
            """缺口（C/G2–G8、G9–G22、N1–N4、H3.1–H3.3）"""
        class Argument(Thing):
            """论证单元（前提集合 → 结论 的文本化表示）"""
        class Hyperedge(Thing):
            """有向超边（⇒ 重组实现，多因一果）"""
        class RelationType(Thing):
            """关系类型元类"""
        class Evidence(Thing):
            """证据单元（原文文档 + 字符区间 + 引文 + 定位方法）"""

        # ---- 对象属性：定义域 / 值域 / 逆属性 ----
        class evolvesTo(ObjectProperty):
            domain = [Concept]
            range = [Concept]
        class evolvedFrom(ObjectProperty):
            inverse_property = evolvesTo
        class mapsTo(ObjectProperty):
            domain = [Concept]
            range = [Concept]
        class mappedFrom(ObjectProperty):
            inverse_property = mapsTo
        class equivalentTo(ObjectProperty):
            domain = [Concept]
            range = [Concept]
        class dependsOn(ObjectProperty):
            domain = [Proposition]
            range = [Concept]
        class dependedOnBy(ObjectProperty):
            inverse_property = dependsOn
        class conceptDependsOn(ObjectProperty):
            """概念依赖概念（论证表『依赖』）"""
            domain = [Concept]
            range = [Concept]
        class conceptDependedOnBy(ObjectProperty):
            inverse_property = conceptDependsOn
        class subsumedIn(ObjectProperty):
            domain = [Concept]
            range = [Concept]
        class subsumes(ObjectProperty):
            inverse_property = subsumedIn
        class hasPremise(ObjectProperty):
            domain = [Hyperedge]
            range = [Concept]
        class hasConclusion(ObjectProperty):
            domain = [Hyperedge]
            range = [Concept]
        class gapPrecedes(ObjectProperty):
            """缺口前置：src 未闭合时 dst 无法闭合（缺口依赖闭包 §二）"""
            domain = [Gap]
            range = [Gap]
        class mentionedIn(ObjectProperty):
            """命题提及概念（claim 级边）"""
            domain = [Proposition]
            range = [Concept]
        class derivedFrom(ObjectProperty):
            """断言 → 证据单元"""
            range = [Evidence]

        ctype_cls = {t: type(CTYPE_NAME[t], (Concept,), {}) for t in sorted({c["type"] for c in concepts})}
        ptype_cls = {}
        for t in sorted({p["type"] for p in props}):
            base = Gap if t == "缺口" else Proposition
            ptype_cls[t] = type(PTYPE_NAME[t], (base,), {})

        # 12 个概念类型互斥（组织层分类约定：源数据每概念恰属一类）
        AllDisjoint(list(ctype_cls.values()))

        # 限制公理：超边至少 1 个前件、1 个结论
        Hyperedge.is_a.append(hasPremise.min(1, Concept))
        Hyperedge.is_a.append(hasConclusion.min(1, Concept))
        # 缺口必须有编号
        Gap.is_a.append(Proposition)

        sourceDoc = type("sourceDoc", (AnnotationProperty,), {})
        sourceLoc = type("sourceLoc", (AnnotationProperty,), {})
        definition = type("definition", (AnnotationProperty,), {})
        synonyms = type("synonyms", (AnnotationProperty,), {})
        status = type("status", (AnnotationProperty,), {})
        premisesText = type("premisesText", (AnnotationProperty,), {})
        conclusionText = type("conclusionText", (AnnotationProperty,), {})
        relationType = type("relationType", (AnnotationProperty,), {})
        gapCode = type("gapCode", (AnnotationProperty,), {})
        evidenceKind = type("evidenceKind", (AnnotationProperty,), {})
        evidenceSpan = type("evidenceSpan", (AnnotationProperty,), {})
        evidenceQuote = type("evidenceQuote", (AnnotationProperty,), {})
        evidenceMethod = type("evidenceMethod", (AnnotationProperty,), {})
        evidenceConfidence = type("evidenceConfidence", (AnnotationProperty,), {})
        humanVerified = type("humanVerified", (AnnotationProperty,), {})

        # ---- 概念个体 ----
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

        # ---- 命题个体 ----
        pind = {}
        for p in props:
            ind = ptype_cls.get(p["type"], Proposition)(p["prop_id"], namespace=onto)
            ind.label = [p["statement"]]
            status[ind] = [p["status"]]
            if p["source_doc"]:
                sourceDoc[ind] = [p["source_doc"]]
            if p["depends_on"]:
                for dep in [x.strip() for x in p["depends_on"].split(";") if x.strip()]:
                    if dep in cind:
                        ind.dependsOn = list(set(list(ind.dependsOn) + [cind[dep]]))
            pind[p["prop_id"]] = ind

        # ---- 论证个体 ----
        aind = {}
        for a in args:
            if a["type"] == "重组实现":
                h = Hyperedge(a["arg_id"], namespace=onto)
                h.label = [a["premises"] + " ⇒ " + a["conclusion"]]
                premisesText[h] = [a["premises"]]
                conclusionText[h] = [a["conclusion"]]
                sourceDoc[h] = a["source_doc"]
                left, right = (a["source_concept"].split("→", 1) + [""])[:2]
                h.hasPremise = [cind[x] for x in left.split(";") if x.strip() in cind]
                h.hasConclusion = [cind[x] for x in right.split(";") if x.strip() in cind]
                aind[a["arg_id"]] = h
            else:
                rel = Argument(a["arg_id"], namespace=onto)
                rel.label = [a["premises"] + " → " + a["conclusion"]]
                premisesText[rel] = [a["premises"]]
                conclusionText[rel] = [a["conclusion"]]
                relationType[rel] = [a["type"]]
                sourceDoc[rel] = a["source_doc"]
                ids = [x for x in a["source_concept"].replace(";", "→").split("→") if x.strip().startswith("C")]
                ids = [x for x in ids if x in cind]
                if len(ids) >= 2 and a["type"] in REL_AS_PROP:
                    setattr(cind[ids[0]], REL_AS_PROP[a["type"]], [cind[ids[-1]]])
                aind[a["arg_id"]] = rel

        # ---- 缺口编号与缺口前置边 ----
        code2prop = {}
        for p in props:
            if p["type"] == "缺口":
                m = re.search(r"缺口\s*([CGN]\d*|C)", p["statement"])
                if m:
                    code2prop[m.group(1)] = p["prop_id"]
                    gapCode[pind[p["prop_id"]]] = [m.group(1)]
        n_gap_edges = 0
        for e in gap_edges:
            s, d = code2prop.get(e["src"]), code2prop.get(e["dst"])
            if s and d and s != d:
                cur = list(pind[s].gapPrecedes)
                if pind[d] not in cur:
                    pind[s].gapPrecedes = cur + [pind[d]]
                    n_gap_edges += 1

        # ---- claim 级边：命题 → 概念 ----
        n_mention = 0
        for r in claim_rows:
            if r["relation"] in ("提及概念", "证据句提及概念") and r["src_id"] in pind and r["dst_id"] in cind:
                cur = list(pind[r["src_id"]].mentionedIn)
                if cind[r["dst_id"]] not in cur:
                    pind[r["src_id"]].mentionedIn = cur + [cind[r["dst_id"]]]
                    n_mention += 1

        # ---- 证据个体 + derivedFrom ----
        n_ev = 0
        for r in ev_rows:
            if not r.get("quote"):
                continue
            ev = Evidence("EV_" + r["struct_id"], namespace=onto)
            ev.label = [r["struct_id"]]
            evidenceKind[ev] = [r["kind"]]
            sourceDoc[ev] = [r.get("evidence_doc") or r.get("doc_id") or ""]
            evidenceSpan[ev] = [f"{r.get('char_start','')}-{r.get('char_end','')}"]
            evidenceQuote[ev] = [(r.get("quote_clean") or "")[:300]]
            evidenceMethod[ev] = [f"{r.get('match_method','')}/{r.get('confidence','')}"]
            evidenceConfidence[ev] = [str(r.get("score", ""))]
            humanVerified[ev] = [str(r.get("verified", False))]
            tgt = cind.get(r["struct_id"]) or pind.get(r["struct_id"]) or aind.get(r["struct_id"])
            if tgt is not None:
                tgt.derivedFrom = list(set(list(tgt.derivedFrom) + [ev]))
                n_ev += 1
    return onto, {"gap_precedes_edges": n_gap_edges, "mentioned_in_edges": n_mention, "evidence_individuals": n_ev}


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
    assert len(concepts) == 82 and len(props) == 63 and len(args) == 70

    gap_edges = read_csv("缺口依赖.csv") if os.path.exists(os.path.join(S01, "缺口依赖.csv")) else []
    claim_rows = read_csv("命题依赖.csv") if os.path.exists(os.path.join(S01, "命题依赖.csv")) else []
    ev_rows = read_csv("证据映射.csv", S00) if os.path.exists(os.path.join(S00, "证据映射.csv")) else []

    onto, extra = build_owl(concepts, props, args, gap_edges, claim_rows, ev_rows)
    out = os.path.join(S02, "本体.owl")
    onto.save(file=out, format="rdfxml")

    # ---- HermiT 推理检查（内存中运行；推理结果记入统计，不改写本体文件）----
    reason = {"ok": False, "unsatisfiable": [], "inferred_subclasses": 0, "error": ""}
    try:
        with onto:
            sync_reasoner(debug=0)
        unsat = sorted({c.name for c in onto.classes() if Nothing in c.ancestors()})
        reason["ok"] = not unsat
        reason["unsatisfiable"] = unsat
        reason["inferred_subclasses"] = sum(1 for c in onto.classes() for _ in c.is_a)
    except Exception as e:  # pragma: no cover
        reason["error"] = str(e)[:200]

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
        "owl_annotation_properties": len(list(onto.annotation_properties())),
        "owl_disjoint_type_classes": len(ctype_cls_names(onto)),
        "owl_restrictions": sum(1 for c in onto.classes() for a in c.is_a
                                if getattr(a, "is_a", None) and type(a).__name__ == "Restriction"),
        "cross_type_edges": sum(cnt.values()),
        "axiom_layer": extra,
        "reasoner": {"engine": "HermiT (owlready2 sync_reasoner, 内存推理)",
                     "consistent": reason["ok"], "unsatisfiable_classes": reason["unsatisfiable"],
                     "error": reason["error"]},
    }
    with open(os.path.join(S02, "本体统计.json"), "w", encoding="utf-8") as f:
        json.dump(stat, f, ensure_ascii=False, indent=2)
    print("[OK] 本体.owl / 概念关系图.png / 本体统计.json")
    print("  类=%d 个体=%d 对象属性=%d 注解属性=%d" % (
        stat["owl_classes"], stat["owl_individuals"], stat["owl_object_properties"],
        stat["owl_annotation_properties"]))
    print("  公理层:", extra, "| 跨类型边:", stat["cross_type_edges"])
    print("  HermiT 一致:", reason["ok"], reason["unsatisfiable"] or "", reason["error"])


def ctype_cls_names(onto):
    return [c for c in onto.classes() if c.name in CTYPE_NAME.values()]


if __name__ == "__main__":
    main()
