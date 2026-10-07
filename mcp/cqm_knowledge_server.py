# -*- coding: utf-8 -*-
"""
CQM 只读知识 MCP server

把 `08 理论组织和形式化框架/01_结构化数据/*.csv` 及其派生结构化产物（超图、本体统计、
Lean 映射、文档引用清单、术语表、缺口台账）暴露为 MCP tools / resources，使 agent 与
AI IDE 会话可直接检索、导航、追溯，而不必只读原始 Markdown 文本。

严格只读：不写入、不修改任何源数据；返回值均为源文件内容的原样投影，不做推断或补全。

运行（stdio）：
    uv run --no-project --with "mcp>=2,<3" python mcp/cqm_knowledge_server.py
自检（不启动传输层）：
    uv run --no-project --with "mcp>=2,<3" python mcp/cqm_knowledge_server.py --selftest
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
from collections import deque

from mcp.server.mcpserver import MCPServer


# --------------------------------------------------------------------------
# 路径定位与读取
# --------------------------------------------------------------------------
def _find_root() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    cur = here
    for _ in range(8):
        if os.path.isdir(os.path.join(cur, "08 理论组织和形式化框架")) and os.path.isfile(
            os.path.join(cur, "README.md")
        ):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return os.path.dirname(here)


ROOT = _find_root()
S08 = os.path.join(ROOT, "08 理论组织和形式化框架")
S01 = os.path.join(S08, "01_结构化数据")
S02 = os.path.join(S08, "02_概念本体")
S03 = os.path.join(S08, "03_超图与理论图")
S04 = os.path.join(S08, "04_Lean对接")
S11 = os.path.join(S08, "11_元数据")
REF = os.path.join(S08, "00_外部引用")
APPENDIX = os.path.join(ROOT, "一体化研究", "附录")


def _read_csv(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return [dict(row) for row in csv.DictReader(f)]


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _read_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


_DOC_RE = re.compile(
    r"-\s*\{id:\s*(D\d+),\s*path:\s*([^,]+),\s*title:\s*([^,]+),\s*layer:\s*(\d+),\s*type:\s*([^}]+)\}"
)


def _load_documents() -> dict[str, dict]:
    docs: dict[str, dict] = {}
    for m in _DOC_RE.finditer(_read_text(os.path.join(REF, "引用清单.yaml"))):
        docs[m.group(1)] = {
            "id": m.group(1),
            "path": m.group(2).strip(),
            "title": m.group(3).strip(),
            "layer": int(m.group(4)),
            "type": m.group(5).strip(),
        }
    return docs


# --------------------------------------------------------------------------
# 数据装载（惰性、单例）
# --------------------------------------------------------------------------
_CACHE: dict[str, object] = {}


def _concepts() -> list[dict]:
    if "concepts" not in _CACHE:
        _CACHE["concepts"] = _read_csv(os.path.join(S01, "概念表.csv"))
    return _CACHE["concepts"]  # type: ignore[return-value]


def _propositions() -> list[dict]:
    if "props" not in _CACHE:
        _CACHE["props"] = _read_csv(os.path.join(S01, "命题表.csv"))
    return _CACHE["props"]  # type: ignore[return-value]


def _arguments() -> list[dict]:
    if "args" not in _CACHE:
        _CACHE["args"] = _read_csv(os.path.join(S01, "论证表.csv"))
    return _CACHE["args"]  # type: ignore[return-value]


def _hypergraph() -> dict:
    if "hg" not in _CACHE:
        _CACHE["hg"] = _read_json(os.path.join(S03, "超图数据.json"))
    return _CACHE["hg"]  # type: ignore[return-value]


def _lean_map() -> list[dict]:
    if "lean" not in _CACHE:
        _CACHE["lean"] = _read_csv(os.path.join(S04, "Lean↔概念映射.csv"))
    return _CACHE["lean"]  # type: ignore[return-value]


def _ontology_stats() -> dict:
    if "onto" not in _CACHE:
        _CACHE["onto"] = _read_json(os.path.join(S02, "本体统计.json"))
    return _CACHE["onto"]  # type: ignore[return-value]


def _documents() -> dict[str, dict]:
    if "docs" not in _CACHE:
        _CACHE["docs"] = _load_documents()
    return _CACHE["docs"]  # type: ignore[return-value]


def _concept_index() -> dict[str, dict]:
    if "cidx" not in _CACHE:
        _CACHE["cidx"] = {c["concept_id"]: c for c in _concepts()}
    return _CACHE["cidx"]  # type: ignore[return-value]


def _prop_index() -> dict[str, dict]:
    if "pidx" not in _CACHE:
        _CACHE["pidx"] = {p["prop_id"]: p for p in _propositions()}
    return _CACHE["pidx"]  # type: ignore[return-value]


# --------------------------------------------------------------------------
# 辅助
# --------------------------------------------------------------------------
def _dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def _doc_path(doc_id: str) -> str:
    d = _documents().get(doc_id)
    return d["path"] if d else ""


def _with_doc(record: dict, field: str = "source_doc") -> dict:
    """给记录补上来源文档路径（原样附加，不改动原字段）。"""
    out = dict(record)
    raw = record.get(field, "") or ""
    ids = [x for x in raw.split(";") if x]
    out["source_doc_path"] = [_doc_path(i) for i in ids]
    return out


def _norm(s: str) -> str:
    return (s or "").strip().lower()


def _graph_edges() -> list[tuple[str, str, str, str]]:
    """返回 (source, target, relation_type, edge_id)，含超边 premise→conclusion 展开。"""
    if "edges" in _CACHE:
        return _CACHE["edges"]  # type: ignore[return-value]
    edges: list[tuple[str, str, str, str]] = []
    hg = _hypergraph()
    for e in hg.get("directed_edges", []):
        edges.append((e["source"], e["target"], e.get("type", ""), e.get("id", "")))
    for h in hg.get("hyperedges", []):
        for p in h.get("premises", []):
            for c in h.get("conclusion", []):
                edges.append((p, c, h.get("type", ""), h.get("id", "")))
    _CACHE["edges"] = edges
    return edges


def _adjacency() -> dict[str, list[tuple[str, str, str]]]:
    if "adj" in _CACHE:
        return _CACHE["adj"]  # type: ignore[return-value]
    adj: dict[str, list[tuple[str, str, str]]] = {}
    for s, t, rt, eid in _graph_edges():
        adj.setdefault(s, []).append((t, rt, eid))
    _CACHE["adj"] = adj
    return adj


# --------------------------------------------------------------------------
# MCP server
# --------------------------------------------------------------------------
mcp = MCPServer(
    name="cqm-knowledge",
    title="CQM 只读知识库",
    instructions=(
        "CQMFormal 理论的结构化知识入口（只读）。数据源为 08 理论组织和形式化框架/"
        "01_结构化数据/*.csv 及其派生结构化产物。用于按概念/命题/论证/缺口检索、"
        "沿超图与依赖边导航、追溯来源文档与 Lean 映射。返回值为源数据原样投影。"
    ),
    version="1.0.0",
)


@mcp.tool()
def project_overview() -> str:
    """返回项目结构化知识总览：概念/命题/论证/超图计数、缺口计数、文档清单规模、本体统计。"""
    props = _propositions()
    gaps = [p for p in props if p.get("type") == "缺口"]
    hg = _hypergraph()
    onto = _ontology_stats()
    docs = _documents()
    return _dump(
        {
            "counts": {
                "concepts": len(_concepts()),
                "propositions": len(props),
                "gaps": len(gaps),
                "arguments": len(_arguments()),
                "hyperedges": len(hg.get("hyperedges", [])),
                "directed_edges": len(hg.get("directed_edges", [])),
                "documents": len(docs),
                "lean_mappings": len(_lean_map()),
            },
            "ontology": onto,
            "data_source": "08 理论组织和形式化框架/01_结构化数据/*.csv（唯一源）",
            "read_only": True,
        }
    )


@mcp.tool()
def search_concepts(query: str, concept_type: str = "", limit: int = 20) -> str:
    """按关键词检索概念（匹配名称、定义、同义词，大小写不敏感）。concept_type 可选，按类型过滤。"""
    q = _norm(query)
    out = []
    for c in _concepts():
        if concept_type and c.get("type") != concept_type:
            continue
        hay = _norm(c.get("name", "")) + " " + _norm(c.get("definition", "")) + " " + _norm(c.get("synonyms", ""))
        if q in hay:
            out.append(_with_doc(c))
        if len(out) >= limit:
            break
    return _dump({"query": query, "count": len(out), "concepts": out})


@mcp.tool()
def get_concept(concept_id: str) -> str:
    """按 concept_id（如 C048）取概念全记录，并附其入/出关系边、超边参与情况、相关论证与 Lean 映射。"""
    c = _concept_index().get(concept_id)
    if not c:
        return _dump({"error": f"未找到概念 {concept_id}", "available_prefix": "C001–C082"})
    hg = _hypergraph()
    out_edges = [e for e in hg.get("directed_edges", []) if e.get("source") == concept_id]
    in_edges = [e for e in hg.get("directed_edges", []) if e.get("target") == concept_id]
    hyper = [
        h
        for h in hg.get("hyperedges", [])
        if concept_id in h.get("premises", []) or concept_id in h.get("conclusion", [])
    ]
    args = [
        a
        for a in _arguments()
        if concept_id in a.get("source_concept", "") or concept_id in a.get("premises", "") + a.get("conclusion", "")
    ]
    lean = [
        m
        for m in _lean_map()
        if concept_id in m.get("concept_ids", "")
    ]
    return _dump(
        {
            "concept": _with_doc(c),
            "outgoing_edges": out_edges,
            "incoming_edges": in_edges,
            "hyperedges": hyper,
            "arguments": args,
            "lean_mappings": lean,
        }
    )


@mcp.tool()
def search_propositions(query: str = "", prop_type: str = "", status: str = "", limit: int = 30) -> str:
    """检索命题/缺口。query 匹配陈述文本；prop_type 可为 定理/命题/假设/构造/猜想/缺口；status 按状态过滤。"""
    q = _norm(query)
    out = []
    for p in _propositions():
        if prop_type and p.get("type") != prop_type:
            continue
        if status and p.get("status") != status:
            continue
        if q and q not in _norm(p.get("statement", "")):
            continue
        out.append(_with_doc(p))
        if len(out) >= limit:
            break
    return _dump({"count": len(out), "propositions": out})


@mcp.tool()
def get_proposition(prop_id: str) -> str:
    """按 prop_id（如 P010、G002）取命题全记录，并解析其 depends_on 指向的记录。"""
    p = _prop_index().get(prop_id)
    if not p:
        return _dump({"error": f"未找到命题 {prop_id}"})
    dep_ids = [x for x in (p.get("depends_on", "") or "").split(";") if x]
    deps = []
    for d in dep_ids:
        r = _prop_index().get(d) or _concept_index().get(d)
        if r:
            deps.append({"id": d, "kind": "proposition" if d in _prop_index() else "concept", "record": r})
        else:
            deps.append({"id": d, "kind": "unknown"})
    return _dump({"proposition": _with_doc(p), "depends_on_resolved": deps})


@mcp.tool()
def list_gaps(status: str = "") -> str:
    """列出全部缺口（命题表 type=缺口），可按状态过滤；状态为源数据原样值，不得升级为"已证"。"""
    gaps = [_with_doc(p) for p in _propositions() if p.get("type") == "缺口"]
    if status:
        gaps = [g for g in gaps if g.get("status") == status]
    return _dump({"count": len(gaps), "gaps": gaps, "note": "缺口状态为源数据原样值，禁止升级为已证/已闭合。"})


@mcp.tool()
def neighbors(concept_id: str, direction: str = "both", relation_type: str = "") -> str:
    """取某概念在超图/依赖图中的邻接关系。direction ∈ {out, in, both}；relation_type 可选过滤。"""
    if concept_id not in _concept_index():
        return _dump({"error": f"未找到概念 {concept_id}"})
    hg = _hypergraph()
    res: dict[str, list] = {"out": [], "in": []}
    if direction in ("out", "both"):
        for e in hg.get("directed_edges", []):
            if e.get("source") == concept_id and (not relation_type or e.get("type") == relation_type):
                res["out"].append(e)
    if direction in ("in", "both"):
        for e in hg.get("directed_edges", []):
            if e.get("target") == concept_id and (not relation_type or e.get("type") == relation_type):
                res["in"].append(e)
    hyper = [
        h
        for h in hg.get("hyperedges", [])
        if (concept_id in h.get("premises", []) or concept_id in h.get("conclusion", []))
        and (not relation_type or h.get("type") == relation_type)
    ]
    return _dump({"concept_id": concept_id, "directed": res, "hyperedges": hyper})


@mcp.tool()
def find_path(source_id: str, target_id: str, max_depth: int = 4) -> str:
    """在超图/依赖图上做 BFS 最短路（沿边方向），返回概念 id 与途径边；找不到则给出可达性说明。"""
    adj = _adjacency()
    if source_id == target_id:
        return _dump({"path": [source_id], "steps": []})
    prev: dict[str, tuple[str, str, str]] = {}
    seen = {source_id}
    q = deque([(source_id, 0)])
    while q:
        node, depth = q.popleft()
        if depth >= max_depth:
            continue
        for nxt, rt, eid in adj.get(node, []):
            if nxt in seen:
                continue
            seen.add(nxt)
            prev[nxt] = (node, rt, eid)
            if nxt == target_id:
                chain = [nxt]
                steps = []
                cur = nxt
                while cur in prev:
                    p, r, e = prev[cur]
                    steps.append({"from": p, "to": cur, "relation": r, "edge": e})
                    chain.append(p)
                    cur = p
                chain.reverse()
                steps.reverse()
                return _dump(
                    {
                        "path": chain,
                        "path_labels": [_concept_index().get(x, {}).get("name", x) for x in chain],
                        "steps": steps,
                        "depth": len(steps),
                    }
                )
            q.append((nxt, depth + 1))
    return _dump({"path": None, "reachable_within_depth": False, "max_depth": max_depth})


@mcp.tool()
def list_arguments(concept_id: str = "", relation_type: str = "", limit: int = 40) -> str:
    """列出论证（超边）。concept_id 过滤涉及该概念的论证；relation_type 过滤关系类型（如 重组实现/映射/等价）。"""
    out = []
    for a in _arguments():
        if relation_type and a.get("type") != relation_type:
            continue
        if concept_id:
            blob = a.get("source_concept", "") + a.get("premises", "") + a.get("conclusion", "")
            if concept_id not in blob:
                continue
        out.append(_with_doc(a))
        if len(out) >= limit:
            break
    return _dump({"count": len(out), "arguments": out})


@mcp.tool()
def lean_mapping(concept_id: str = "", library: str = "") -> str:
    """取 Lean 形式化映射（Lean↔概念映射.csv）。可按 concept_id 或 lean_library 过滤。"""
    out = []
    for m in _lean_map():
        if concept_id and concept_id not in m.get("concept_ids", ""):
            continue
        if library and library.lower() not in m.get("lean_library", "").lower():
            continue
        out.append(m)
    return _dump({"count": len(out), "lean_mappings": out})


@mcp.tool()
def resolve_document(doc_id: str = "", query: str = "") -> str:
    """把文档 ID（D005）解析为相对路径/标题/层级，或按关键词在标题与路径中检索文档。"""
    docs = _documents()
    if doc_id:
        d = docs.get(doc_id)
        if not d:
            return _dump({"error": f"未找到文档 {doc_id}"})
        return _dump(d)
    q = _norm(query)
    hits = [d for d in docs.values() if q in _norm(d["title"]) or q in _norm(d["path"])] if q else list(docs.values())
    return _dump({"count": len(hits), "documents": hits})


# --------------------------------------------------------------------------
# Resources
# --------------------------------------------------------------------------
@mcp.resource("cqm://glossary", name="术语表", mime_type="text/markdown")
def res_glossary() -> str:
    """一体化研究/附录/术语表.md 原文。"""
    return _read_text(os.path.join(APPENDIX, "术语表.md"))


@mcp.resource("cqm://gaps", name="缺口台账", mime_type="text/markdown")
def res_gaps() -> str:
    """一体化研究/附录/缺口台账.md 原文（缺口状态禁止升级）。"""
    return _read_text(os.path.join(APPENDIX, "缺口台账.md"))


@mcp.resource("cqm://gap-closure", name="缺口依赖闭包", mime_type="text/markdown")
def res_gap_closure() -> str:
    """08 理论组织和形式化框架/01_结构化数据/缺口依赖闭包.md 原文。"""
    return _read_text(os.path.join(S01, "缺口依赖闭包.md"))


@mcp.resource("cqm://concepts", name="概念表", mime_type="application/json")
def res_concepts() -> str:
    """概念表（82 概念）结构化 JSON。"""
    return _dump(_concepts())


@mcp.resource("cqm://propositions", name="命题表", mime_type="application/json")
def res_propositions() -> str:
    """命题表（命题 + 缺口）结构化 JSON。"""
    return _dump(_propositions())


@mcp.resource("cqm://arguments", name="论证表", mime_type="application/json")
def res_arguments() -> str:
    """论证表（超边）结构化 JSON。"""
    return _dump(_arguments())


@mcp.resource("cqm://hypergraph", name="超图数据", mime_type="application/json")
def res_hypergraph() -> str:
    """超图数据（节点/超边/有向边）JSON。"""
    return _dump(_hypergraph())


@mcp.resource("cqm://documents", name="文档引用清单", mime_type="application/json")
def res_documents() -> str:
    """文档引用清单（D001–D052 → 路径/标题/层级）。"""
    return _dump(list(_documents().values()))


@mcp.resource("cqm://ontology-stats", name="本体统计", mime_type="application/json")
def res_ontology() -> str:
    """概念本体统计 JSON。"""
    return _dump(_ontology_stats())


@mcp.resource("cqm://term-symbol-consistency", name="术语符号一致清单", mime_type="text/markdown")
def res_term_symbol() -> str:
    """08 理论组织和形式化框架/02_概念本体/术语符号一致清单.md 原文。"""
    return _read_text(os.path.join(S02, "术语符号一致清单.md"))


# --------------------------------------------------------------------------
# 自检
# --------------------------------------------------------------------------
def _selftest() -> int:
    ok = True
    checks = []

    def check(name: str, cond: bool, detail: str = ""):
        nonlocal ok
        ok = ok and cond
        checks.append(("PASS" if cond else "FAIL", name, detail))

    check("定位仓库根", os.path.isdir(S08), ROOT)
    check("概念表可读", len(_concepts()) == 82, f"{len(_concepts())} 条")
    check("命题表可读", len(_propositions()) == 63, f"{len(_propositions())} 条")
    check("论证表可读", len(_arguments()) == 70, f"{len(_arguments())} 条")
    check("超图可读", len(_hypergraph().get("hyperedges", [])) == 19, "19 超边")
    check("文档清单可读", len(_documents()) == 52, f"{len(_documents())} 篇")
    check("Lean 映射可读", len(_lean_map()) > 0, f"{len(_lean_map())} 行")

    c = json.loads(get_concept("C048"))
    check("get_concept(C048)", c.get("concept", {}).get("name") == "相变量子", str(c.get("concept", {}).get("name")))
    check("来源文档解析", bool(c.get("concept", {}).get("source_doc_path")), _doc_path("D008"))

    g = json.loads(list_gaps())
    check("缺口计数", g["count"] >= 24, f"{g['count']} 缺口")

    p = json.loads(find_path("C001", "C017"))
    check("find_path(C001→C017)", p.get("path") is not None, str(p.get("path")))

    n = json.loads(neighbors("C012", "both"))
    check("neighbors(C012)", len(n["directed"]["out"]) + len(n["directed"]["in"]) > 0, "有邻接")

    check("术语表资源", len(res_glossary()) > 0, f"{len(res_glossary())} 字符")
    check("缺口台账资源", "缺口" in res_gaps(), "含缺口")

    for status, name, detail in checks:
        print(f"[{status}] {name} {detail}")
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(_selftest())
    mcp.run()