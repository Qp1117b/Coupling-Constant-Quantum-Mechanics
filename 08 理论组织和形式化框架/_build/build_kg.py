# -*- coding: utf-8 -*-
"""
维度 02/03/07 · 知识图谱导出 · SHACL 校验 · SPARQL 能力问答

把 `02_概念本体/本体.owl`（owlready2 生成）与证据/别名/Lean 映射合并成一份可被主流工具链消费的 RDF 图，
并跑三样硬检查：

  1. 导出      03_超图与理论图/知识图谱.ttl   （Turtle；含 SKOS 词表、PROV 溯源、Lean 映射）
  2. SHACL     02_概念本体/shapes.shacl.ttl   + pyshacl 校验 → 02_概念本体/本体校验报告.json
  3. SPARQL    03_超图与理论图/SPARQL问答.json （能力问句的实际查询结果）

SHACL 形状是**数据契约**：例如"每个概念必须有 prefLabel、definition、出处与证据"，
"每条超边至少 1 前件 1 结论"，"缺口编号必须匹配 ^(C|G\\d+|N\\d+)$"。违约即如实报出，不隐藏。

运行：python build_kg.py
"""
import csv
import io
import json
import os

import rdflib
from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, XSD, URIRef
from rdflib.namespace import SKOS, PROV, SH
import pyshacl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S00, S01, S02, S03 = (os.path.join(ROOT, x) for x in
                      ("00_外部引用", "01_结构化数据", "02_概念本体", "03_超图与理论图"))
S04 = os.path.join(ROOT, "04_Lean对接")
CQM = Namespace("http://cqm.local/ontology#")


def rd(path, base):
    with io.open(os.path.join(base, path), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_base():
    g = Graph()
    g.parse(os.path.join(S02, "本体.owl"), format="xml")
    g.bind("cqm", CQM)
    g.bind("skos", SKOS)
    g.bind("prov", PROV)
    return g


def add_wordnet_annotations(g):
    """SKOS 词表标注 + PROV 溯源指针（标准词表，便于与外部工具互通）。"""
    n_alt = 0
    for r in rd("概念别名表.csv", S01):
        s = CQM[r["concept_id"]]
        g.add((s, SKOS.altLabel, Literal(r["alias"], lang="zh")))
        n_alt += 1
    n_pref = 0
    for r in rd("概念表.csv", S01):
        s = CQM[r["concept_id"]]
        g.add((s, SKOS.prefLabel, Literal(r["name"], lang="zh")))
        if r["definition"]:
            g.add((s, SKOS.definition, Literal(r["definition"], lang="zh")))
        n_pref += 1
    n_prov = 0
    for r in rd("证据映射.csv", S00):
        if not r["quote"]:
            continue
        ev = CQM["EV_" + r["struct_id"]]
        g.add((ev, RDF.type, PROV.Entity))
        if r["quote_clean"]:
            g.add((ev, PROV.value, Literal(r["quote_clean"][:300], lang="zh")))
        if r["char_start"] and r["char_end"]:
            g.add((ev, PROV.atLocation, Literal(f'{r["char_start"]}-{r["char_end"]}')))
        if r["evidence_doc"]:
            g.add((ev, CQM.sourceDoc, Literal(r["evidence_doc"])))
        if r["match_method"]:
            g.add((ev, CQM.evidenceMethod, Literal(f'{r["match_method"]}/{r["confidence"]}')))
        for sid in (r["struct_id"],):
            if (CQM[sid], None, None) in g:
                g.add((CQM[sid], PROV.wasDerivedFrom, ev))
                n_prov += 1
    return {"alt_labels": n_alt, "pref_labels": n_pref, "prov_links": n_prov}


def add_lean_mapping(g):
    n = 0
    for r in rd("Lean↔概念映射.csv", S04):
        lib = URIRef(f'http://cqm.local/lean#{r["lean_library"]}')
        g.add((lib, RDF.type, CQM.LeanLibrary))
        g.add((lib, RDFS.label, Literal(r["lean_library"])))
        if r.get("lean_symbol"):
            g.add((lib, CQM.leanSymbol, Literal(r["lean_symbol"])))
        for cid in (r.get("concept_ids") or "").split(";"):
            cid = cid.strip()
            if cid.startswith("C"):
                g.add((CQM[cid], CQM.formalizedIn, lib))
                n += 1
    return {"lean_links": n}


SHAPES = """@prefix sh:   <http://www.w3.org/ns/shacl#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix cqm:  <http://cqm.local/ontology#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

cqm:ConceptShape a sh:NodeShape ;
  sh:targetClass cqm:Concept ;
  sh:property [ sh:path skos:prefLabel ; sh:minCount 1 ; sh:nodeKind sh:Literal ;
                sh:message "概念缺少规范名（skos:prefLabel）" ] ;
  sh:property [ sh:path skos:definition ; sh:minCount 1 ; sh:nodeKind sh:Literal ;
                sh:message "概念缺少定义（skos:definition）" ] ;
  sh:property [ sh:path cqm:sourceDoc ; sh:minCount 1 ; sh:pattern "^D[0-9]{3}$" ;
                sh:message "概念缺少可解析的出处文档（sourceDoc 需形如 D008）" ] ;
  sh:property [ sh:path prov:wasDerivedFrom ; sh:minCount 1 ; sh:class prov:Entity ;
                sh:message "概念没有任何证据单元（证据层未覆盖）" ] .

cqm:PropositionShape a sh:NodeShape ;
  sh:targetClass cqm:Proposition ;
  sh:property [ sh:path rdfs:label ; sh:minCount 1 ;
                sh:message "命题缺少陈述（rdfs:label）" ] ;
  sh:property [ sh:path cqm:status ; sh:minCount 1 ; sh:datatype xsd:string ;
                sh:message "命题缺少状态" ] .

cqm:GapShape a sh:NodeShape ;
  sh:targetClass cqm:Gap ;
  sh:property [ sh:path cqm:gapCode ; sh:minCount 1 ; sh:pattern "^(C|G[0-9]+|N[0-9]+)$" ;
                sh:message "缺口编号必须为 C / G n / N n 之一" ] ;
  sh:property [ sh:path prov:wasDerivedFrom ; sh:minCount 1 ;
                sh:message "缺口没有证据单元" ] .

cqm:HyperedgeShape a sh:NodeShape ;
  sh:targetClass cqm:Hyperedge ;
  sh:property [ sh:path cqm:hasPremise ; sh:minCount 1 ; sh:class cqm:Concept ;
                sh:message "超边缺少前件概念" ] ;
  sh:property [ sh:path cqm:hasConclusion ; sh:minCount 1 ; sh:class cqm:Concept ;
                sh:message "超边缺少结论概念" ] ;
  sh:property [ sh:path cqm:sourceDoc ; sh:minCount 1 ;
                sh:message "超边缺少出处" ] .

cqm:ArgumentShape a sh:NodeShape ;
  sh:targetClass cqm:Argument ;
  sh:property [ sh:path cqm:relationType ; sh:minCount 1 ;
                sh:in ( "演化"^^xsd:string "映射"^^xsd:string "等价"^^xsd:string
                        "依赖"^^xsd:string "层级含于"^^xsd:string ) ;
                sh:message "有向论证的关系类型必须在既有 5 类之内" ] ;
  sh:property [ sh:path prov:wasDerivedFrom ; sh:minCount 1 ;
                sh:message "论证没有证据单元" ] .

cqm:EvidenceShape a sh:NodeShape ;
  sh:targetClass prov:Entity ;
  sh:property [ sh:path prov:value ; sh:minCount 1 ;
                sh:message "证据单元缺少引文" ] ;
  sh:property [ sh:path prov:atLocation ; sh:pattern "^[0-9]+-[0-9]+$" ;
                sh:message "证据单元缺少字符区间" ] ;
  sh:property [ sh:path cqm:evidenceMethod ; sh:minCount 1 ;
                sh:message "证据单元缺少定位方法" ] .
"""

CQS = [
    ("CQ1 未闭合缺口及其前置",
     """SELECT ?code ?status (GROUP_CONCAT(DISTINCT ?p2; separator=",") AS ?precededBy)
        WHERE { ?g a ?gc . ?gc rdfs:subClassOf* cqm:Gap .
                ?g cqm:gapCode ?code ; cqm:status ?status .
                OPTIONAL { ?p cqm:gapPrecedes ?g . ?p cqm:gapCode ?pre }
                BIND(COALESCE(?pre, "") AS ?p2) }
        GROUP BY ?code ?status ORDER BY ?code"""),
    ("CQ2 缺证据的断言（应为空）",
     """SELECT ?s WHERE {
          { ?s a ?c1 . ?c1 rdfs:subClassOf* cqm:Concept }
          UNION { ?s a ?c2 . ?c2 rdfs:subClassOf* cqm:Proposition }
          UNION { ?s a cqm:Hyperedge } UNION { ?s a cqm:Argument }
          FILTER NOT EXISTS { ?s prov:wasDerivedFrom ?e } }"""),
    ("CQ3 超边的前件闭包（一跳）",
     """SELECT ?h (GROUP_CONCAT(DISTINCT ?pre; separator=",") AS ?premises)
        WHERE { ?h a cqm:Hyperedge ; cqm:hasPremise ?p . ?p skos:prefLabel ?pre }
        GROUP BY ?h ORDER BY ?h LIMIT 25"""),
    ("CQ4 缺口依赖链（传递闭包）",
     """SELECT ?src ?dst WHERE { ?a cqm:gapCode ?src ; cqm:gapPrecedes+ ?b . ?b cqm:gapCode ?dst }"""),
    ("CQ5 被最多断言提及的概念",
     """SELECT ?name (COUNT(?s) AS ?n) WHERE { ?s cqm:mentionedIn ?c . ?c skos:prefLabel ?name }
        GROUP BY ?name ORDER BY DESC(?n) LIMIT 8"""),
    ("CQ6 形式化覆盖（有 Lean 映射的概念）",
     """SELECT (COUNT(DISTINCT ?c) AS ?formalized) WHERE { ?c cqm:formalizedIn ?lib }"""),
    ("CQ7 别名 → 规范名",
     """SELECT ?alias ?name WHERE { ?c skos:altLabel ?alias ; skos:prefLabel ?name } ORDER BY ?alias LIMIT 40"""),
    ("CQ8 出处文档分布",
     """SELECT ?doc (COUNT(DISTINCT ?s) AS ?n) WHERE { ?s cqm:sourceDoc ?doc } GROUP BY ?doc
        ORDER BY DESC(?n) LIMIT 10"""),
    ("CQ9 未闭合缺口的证据句",
     """SELECT ?code ?q WHERE { ?g cqm:gapCode ?code ; cqm:status "未闭合" ; prov:wasDerivedFrom ?e .
                ?e prov:value ?q } ORDER BY ?code"""),
]


def main():
    g = load_base()
    n0 = len(g)
    stats = {}
    stats.update(add_wordnet_annotations(g))
    stats.update(add_lean_mapping(g))

    ttl_path = os.path.join(S03, "知识图谱.ttl")
    g.serialize(destination=ttl_path, format="turtle")
    shapes_path = os.path.join(S02, "shapes.shacl.ttl")
    with io.open(shapes_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(SHAPES)

    sg = Graph().parse(shapes_path, format="turtle")
    conforms, rgraph, rtext = pyshacl.validate(g, shacl_graph=sg, inference="rdfs",
                                               abort_on_first=False, allow_infos=True, allow_warnings=True,
                                               advanced=True)
    viol_rows = []
    for res in rgraph.subjects(RDF.type, SH.ValidationResult):
        path = rgraph.value(res, SH.resultPath)
        msg = rgraph.value(res, SH.resultMessage)
        fn = rgraph.value(res, SH.focusNode)
        viol_rows.append({"focus": str(fn).split("#")[-1],
                          "path": str(path).split("#")[-1] if path is not None else "",
                          "message": str(msg)})
    viol = {}
    for r in viol_rows:
        viol[r["message"]] = viol.get(r["message"], 0) + 1
    focus = sorted({r["focus"] for r in viol_rows})

    cq_out = []
    for title, q in CQS:
        try:
            res = g.query(q)
            rows = [[str(x) for x in row] for row in res]
        except Exception as e:  # pragma: no cover
            rows = [["ERROR", str(e)[:120]]]
        cq_out.append({"question": title, "sparql": " ".join(q.split()), "rows": rows[:60],
                       "row_count": len(rows)})

    report = {
        "generated_by": "_build/build_kg.py",
        "rdf": {"triples_in_owl": n0, "triples_exported": len(g), "added": stats,
                "turtle": os.path.relpath(ttl_path, ROOT).replace("\\", "/")},
        "shacl": {"conforms": bool(conforms), "shapes_file": "02_概念本体/shapes.shacl.ttl",
                  "violations": sum(viol.values()), "by_message": viol, "focus_nodes": focus[:40],
                  "details": viol_rows[:200]},
        "sparql": {"questions": len(cq_out), "results": cq_out},
    }
    with io.open(os.path.join(S02, "本体校验报告.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    with io.open(os.path.join(S03, "SPARQL问答.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"questions": cq_out}, f, ensure_ascii=False)

    print(f"[OK] 知识图谱.ttl（{len(g):,} 三元组，本体 {n0:,} → 导出 {len(g):,}）")
    print(f"     SHACL: conforms={conforms} 违约 {sum(viol.values())} 条")
    for k, v in sorted(viol.items(), key=lambda x: -x[1]):
        print(f"       - {v:>3} × {k}")
    print(f"     SPARQL 能力问句 {len(cq_out)} 条：", {c['question'].split()[0]: c['row_count'] for c in cq_out})


if __name__ == "__main__":
    main()
