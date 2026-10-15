# -*- coding: utf-8 -*-
"""
维度1 · Claim Graph（主张图）—— 把"陈述清单"变成"可推理的主张网络"

既有源表只有三种关系入口：概念超图（19 ⇒ + 51 →）、命题的文档级 depends_on、论证表的概念链。
命题之间没有一条边，缺口依赖写在 .md 的表格与散文中，论证表的文本词表与概念表不对齐。
本脚本把这些补成可计算结构（**只搬运原文既有表述，不新增任何理论判断**）：

  01_结构化数据/缺口编号对照.csv  G001…G024 ↔ 权威缺口编号（C / G2–G22 / N1–N4）
  01_结构化数据/缺口依赖.csv      缺口→缺口前置边（来源：命题表 depends_on、缺口依赖闭包.md 表格）
  01_结构化数据/命题依赖.csv      命题→概念 / 命题→缺口 / 命题→命题 / 命题→文档 的 claim 级边
  01_结构化数据/概念别名表.csv    同义词、符号、论证表里的变体写法 → 规范概念名
  01_结构化数据/论证对齐.csv      论证表文本词元 ↔ 概念 ID 的对齐结果（暴露词表不一致）
  03_超图与理论图/知识图谱.json   统一多层图（概念 / 命题 / 缺口 + 关系 / 超边 / claim 边）

每条机器产生的边都带 `method` 与 `verified`：只有源表与权威 .md 表格直接给出的边为 True，
文本线索推出的边一律 False（候选待核）。运行：python build_claims.py
"""
import csv
import io
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.dirname(ROOT)
S00, S01, S03 = (os.path.join(ROOT, x) for x in ("00_外部引用", "01_结构化数据", "03_超图与理论图"))
PUNCT = re.compile(r"[\s\W_]+")
CUE = re.compile(r"因此|所以|故(?![乡事])|由此|从而|导致|推出|给出了|源于|来自于|依赖|前提|等价|对应|即(?=[^是])|由此可知")
GAPCODE = re.compile(r"缺口\s*([CGN]\d*|C)\b")
GAPTOK = re.compile(r"(?<![A-Za-z])([CGN]\d+)(?![A-Za-z0-9])")
STATUS_KEY = re.compile(r"未闭合|部分闭合|闭合|待证明|待严格化|占位|axiom|猜想|数值验证|公式推导完成")


def canon_gap(x):
    """把 G002 之类的 prop-id 或 G2 之类的权威编号统一成权威编号。"""
    x = (x or "").strip()
    m = re.match(r"^([CGN])0*(\d+)$", x)
    if m:
        return m.group(1) + str(int(m.group(2)))
    return x


def status_key(s):
    m = STATUS_KEY.search(s or "")
    return m.group(0) if m else (s or "").strip()


def rd(name):
    with io.open(os.path.join(S01, name), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def rdp(path):
    with io.open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def wcsv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)


def norm(s):
    return PUNCT.sub("", (s or "")).lower()


def tokens(s):
    return [t for t in re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z][A-Za-z0-9_\-]{1,}", s or "")]


def load_jsonl(path):
    with io.open(path, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def parse_gap_tables(md):
    """解析 缺口依赖闭包.md 的缺口表：返回 [{code, desc, status, deps, dependents, lean, section}]"""
    rows, sec = [], ""
    for line in md.splitlines():
        if line.startswith("#"):
            sec = line.strip("# ").strip()
            continue
        if not line.startswith("|") or re.match(r"^\|[\s:|\-]+\|$", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or cells[0] in ("编号",):
            continue
        head = cells[0]
        if re.match(r"^([CGN]\d*|C|G20-ext|G17|H3\.\d|黎曼|Mathieu|素数冻结|Tate 自对偶|\$G_N\$ 变分|B3|E2|H1–H5|U1–U8|闭环相容子空间一维性猜想)$", head):
            r = {"code": head, "desc": cells[1] if len(cells) > 1 else "", "status": "", "deps": "", "dependents": "",
                 "lean": "", "section": sec}
            if len(cells) >= 3:
                r["status"] = cells[2]
            # 列位置随表不同：§二(6列) 依赖=3 被依赖=4 Lean=5；§四(5列) 依赖=3 Lean=4
            if "核心理论缺口" in sec:
                r["deps"], r["dependents"], r["lean"] = (cells[3], cells[4], cells[5]) if len(cells) > 5 else ("", "", "")
            elif "中子缺陷矩阵" in sec:
                r["deps"], r["lean"] = (cells[3], cells[4]) if len(cells) > 4 else ("", "")
            elif "层级假设" in sec:
                r["lean"] = cells[3] if len(cells) > 3 else ""
            rows.append(r)
    return rows


def main():
    concepts = rd("概念表.csv")
    props = rd("命题表.csv")
    args = rd("论证表.csv")
    symbols = rdp(os.path.join(ROOT, "09_桥接与翻译", "符号对照表.csv"))
    closure = io.open(os.path.join(S01, "缺口依赖闭包.md"), encoding="utf-8").read()
    ev_rows = rdp(os.path.join(S00, "证据映射.csv"))
    ev = {r["struct_id"]: r for r in ev_rows}
    sents = load_jsonl(os.path.join(S00, "句索引", "句索引.jsonl"))
    docs = {r["doc_id"]: r for r in rdp(os.path.join(S00, "语料清单.csv"))}

    name2id = {c["name"]: c["concept_id"] for c in concepts}
    id2name = {c["concept_id"]: c["name"] for c in concepts}
    id2con = {c["concept_id"]: c for c in concepts}

    # ---------------- 1) 缺口编号对照 + 缺口依赖 ----------------
    gap_rows, code_by_prop = [], {}
    for p in props:
        if p["type"] != "缺口":
            continue
        m = GAPCODE.search(p["statement"])
        code = m.group(1) if m else ""
        code_by_prop[p["prop_id"]] = code
        gap_rows.append({"prop_id": p["prop_id"], "gap_code": code, "status_prop": p["status"],
                         "statement": p["statement"], "depends_on": p["depends_on"]})
    # id 前缀重载检查：G 前缀既用于缺口（G001–G024）又用于其他命题（G025–G032）
    for r in props:
        if r["prop_id"].startswith("G") and r["type"] != "缺口":
            gap_rows.append({"prop_id": r["prop_id"], "gap_code": "", "status_prop": r["status"],
                             "statement": r["statement"], "depends_on": r["depends_on"],
                             "id_prefix_conflict": "G 前缀被非缺口命题占用"})
    for g in gap_rows:
        g.setdefault("id_prefix_conflict", "")
    table = parse_gap_tables(closure)
    by_code = {}
    for r in table:
        by_code.setdefault(r["code"], r)
    for g in gap_rows:
        t = by_code.get(g["gap_code"], {})
        g["status_closure"] = t.get("status", "")
        g["lean"] = t.get("lean", "")
        g["desc_closure"] = t.get("desc", "")
        g["status_consistent"] = (status_key(g["status_prop"]) == status_key(g["status_closure"])
                                  or not t.get("status"))
        g["section"] = t.get("section", "")
    wcsv(os.path.join(S01, "缺口编号对照.csv"), gap_rows)

    # 缺口依赖边：命题表 depends_on 的 G 引用（权威） + 闭包表 §二 的 依赖/被依赖
    gap_edges, seen = [], set()

    def add_gap_edge(a, b, method, verified, note=""):
        if not a or not b or a == b:
            return
        k = (a, b)
        if k in seen:
            return
        seen.add(k)
        gap_edges.append({"src": a, "dst": b, "relation": "前置（dst 依赖 src）", "method": method,
                          "verified": verified, "note": note})

    for p in props:
        if p["type"] != "缺口":
            continue
        src = code_by_prop.get(p["prop_id"], "")
        for t in p["depends_on"].split(";"):
            t = t.strip()
            if re.match(r"^G\d+$", t):
                add_gap_edge(canon_gap(t), src, "命题表.depends_on", True, f"{p['prop_id']}")
    for r in table:
        if "核心理论缺口" not in r["section"]:
            continue
        for t in GAPTOK.findall(r["deps"]):
            add_gap_edge(canon_gap(t), canon_gap(r["code"]), "缺口依赖闭包.md §二「依赖」", True)
        for t in GAPTOK.findall(r["dependents"]):
            add_gap_edge(canon_gap(r["code"]), canon_gap(t), "缺口依赖闭包.md §二「被依赖」", True)
    wcsv(os.path.join(S01, "缺口依赖.csv"),
         sorted(gap_edges, key=lambda e: (e["src"], e["dst"])))

    # ---------------- 2) 概念别名表 ----------------
    alias_rows, aseen = [], set()

    def add_alias(cid, alias, atype, source, verified):
        if not alias or norm(alias) == norm(id2name.get(cid, "")):
            return
        k = (cid, norm(alias))
        if k in aseen:
            return
        aseen.add(k)
        alias_rows.append({"concept_id": cid, "canonical": id2name.get(cid, ""), "alias": alias,
                           "alias_type": atype, "source": source, "verified": verified})

    for c in concepts:
        for s in (c.get("synonyms") or "").split(","):
            s = s.strip()
            if s:
                add_alias(c["concept_id"], s, "同义词", "概念表.synonyms", True)
    for s in symbols:
        cid = name2id.get(s["name"].strip())
        if cid:
            sym_raw = s["symbol"].strip()
            latex_field = (s.get("latex") or "").strip()
            sym_latex = ""
            if latex_field:
                depth = 0
                for i, ch in enumerate(latex_field):
                    if ch == "{": depth += 1
                    elif ch == "}": depth -= 1
                    elif ch == "=" and depth == 0:
                        sym_latex = latex_field[:i].strip(); break
                else:
                    sym_latex = latex_field
            if sym_latex:
                add_alias(cid, "$" + sym_latex + "$", "符号", "09_桥接与翻译/符号对照表.csv", True)
            else:
                add_alias(cid, sym_raw, "符号", "09_桥接与翻译/符号对照表.csv", True)
    for a in args:
        for raw in [x.strip() for x in a["premises"].split(";") if x.strip()] + [a["conclusion"].strip()]:
            if raw in name2id:
                continue
            na = norm(raw)
            for nm, cid in name2id.items():
                nn = norm(nm)
                if na and nn and (na == nn or (len(nn) >= 2 and na.startswith(nn))):
                    add_alias(cid, raw, "论证表变体写法", f"论证表.{a['arg_id']}", False)
                    break
    wcsv(os.path.join(S01, "概念别名表.csv"),
         sorted(alias_rows, key=lambda r: (r["concept_id"], r["alias"])))

    # ---------------- 3) 论证对齐 ----------------
    align_rows = []
    for a in args:
        sc = a["source_concept"]
        left, right = (sc.split("→", 1) + [""])[:2] if "→" in sc else (sc, "")
        pids = [x.strip() for x in left.split(";") if x.strip()]
        cids = [x.strip() for x in right.split(";") if x.strip()]
        praw = [x.strip() for x in a["premises"].split(";") if x.strip()]
        craw = a["conclusion"].strip()

        def align(raw, cid):
            if not cid:
                return "无 ID"
            nm = id2name.get(cid, "")
            if raw == nm:
                return "精确"
            if norm(raw) == norm(nm):
                return "规范化后一致"
            if norm(nm) and norm(nm) in norm(raw):
                return "含规范名"
            return "不对齐"
        align_rows.append({
            "arg_id": a["arg_id"], "rel_type": a["type"],
            "premises_raw": a["premises"], "premise_ids": ";".join(pids),
            "premise_count": len(praw), "premise_id_count": len(pids),
            "premise_align": " / ".join(align(x, cids0) for x, cids0 in
                                        zip(praw, pids + [""] * max(0, len(praw) - len(pids)))),
            "conclusion_raw": craw, "conclusion_id": cids[0] if cids else "",
            "conclusion_align": align(craw, cids[0] if cids else ""),
            "count_ok": len(praw) == len(pids),
            "evidence": ev.get(a["arg_id"], {}).get("evidence_doc", ""),
            "confidence": ev.get(a["arg_id"], {}).get("confidence", ""),
        })
    wcsv(os.path.join(S01, "论证对齐.csv"), align_rows)

    # ---------------- 4) claim 级命题依赖 ----------------
    claim_edges, cseen = [], set()

    def add_claim(src, dst, rel, method, verified, conf, note=""):
        k = (src, dst, rel)
        if k in cseen:
            return
        cseen.add(k)
        claim_edges.append({"src_id": src, "dst_id": dst, "relation": rel, "method": method,
                            "verified": verified, "confidence": conf, "note": note})

    sent_by_doc = defaultdict(dict)
    for s in sents:
        sent_by_doc[s["doc_id"]][s["sid"]] = s
    # idf（句子级）
    df = Counter()
    for s in sents:
        for t in set(tokens(s["text"])):
            df[t] += 1
    N = max(1, len(sents))
    idf = {t: math.log(1 + N / (1 + c)) for t, c in df.items()}

    for p in props:
        pid = p["prop_id"]
        st = p["statement"]
        for nm, cid in name2id.items():
            if not nm:
                continue
            if nm in st or ("$" in nm and nm.replace("$", "") in st):
                add_claim(pid, cid, "提及概念", "命题表.statement 含概念名", True, "high")
        for code in set(re.findall(r"(?<![A-Za-z])([CGN]\d{1,2})(?![A-Za-z0-9])", st)):
            tgt = [g["prop_id"] for g in gap_rows if g["gap_code"] == code]
            if tgt and tgt[0] != pid:
                add_claim(pid, tgt[0], "提及缺口", "命题表.statement 含缺口编号", False, "medium")
        for t in p["depends_on"].split(";"):
            t = t.strip()
            if t.startswith("D") and t in docs:
                add_claim(pid, t, "依据文档", "命题表.depends_on", True, "high")
        r = ev.get(pid, {})
        if r.get("evidence_doc") and r["confidence"] in ("high", "medium"):
            add_claim(pid, r["evidence_doc"], "证据文档", f"证据层({r['match_method']})", False, r["confidence"])
            srec = sent_by_doc.get(r["evidence_doc"], {}).get(int(r["sid"]) if str(r["sid"]).isdigit() else -1)
            if srec:
                txt = srec["text"]
                for nm, cid in name2id.items():
                    if nm and len(nm) >= 2 and (nm in txt or ("$" in nm and nm.replace("$", "") in txt)):
                        add_claim(pid, cid, "证据句提及概念", f"证据句 {r['evidence_doc']}#{r['sid']}", False, "medium")
                if CUE.search(txt):
                    add_claim(pid, "DISC:" + f"{r['evidence_doc']}#{r['sid']}", "话语线索", "证据句含推理连接词", False, "low",
                              txt[:80])
    # 命题↔命题：同证据句 / 术语重叠 + 话语线索（候选）
    ev_by_sent = defaultdict(list)
    for p in props:
        r = ev.get(p["prop_id"], {})
        if r.get("sid") and str(r["sid"]).isdigit() and r.get("evidence_doc"):
            ev_by_sent[(r["evidence_doc"], int(r["sid"]))].append(p["prop_id"])
    for (d, sid), plist in ev_by_sent.items():
        for i in range(len(plist)):
            for j in range(i + 1, len(plist)):
                add_claim(plist[i], plist[j], "同证据句", f"{d}#{sid}", False, "medium")
    # 命题↔命题：TF-IDF 余弦近邻（陈述 + 证据句），仅取每节点前 3 且标为候选
    def vec(text):
        tf = Counter(tokens(text))
        v = {t: (1 + math.log(c)) * idf.get(t, 1.0) for t, c in tf.items()}
        nrm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {t: x / nrm for t, x in v.items()}
    pv = {}
    for p in props:
        r = ev.get(p["prop_id"], {})
        pv[p["prop_id"]] = vec(p["statement"] + " " + (r.get("quote_clean", "") or ""))
    for a1 in [p["prop_id"] for p in props]:
        sims = []
        for a2 in [p["prop_id"] for p in props]:
            if a1 == a2:
                continue
            dot = sum(x * pv[a2].get(t, 0.0) for t, x in pv[a1].items())
            if dot >= 0.22:
                sims.append((dot, a2))
        for s, a2 in sorted(sims, reverse=True)[:3]:
            add_claim(a1, a2, "语义近邻（候选）", f"TF-IDF 余弦 {s:.2f}", False, "low")
    wcsv(os.path.join(S01, "命题依赖.csv"),
         sorted(claim_edges, key=lambda e: (e["src_id"], e["relation"], e["dst_id"])))

    # ---------------- 5) 统一知识图谱 ----------------
    hg = json.load(io.open(os.path.join(S03, "超图数据.json"), encoding="utf-8"))
    nodes = []
    depth = {c["concept_id"]: "" for c in concepts}
    for n in hg["nodes"]:
        nodes.append({"id": n["id"], "kind": "concept", "label": n["label"], "type": n["type"],
                      "def": n["definition"], "doc": n["source_doc"], "loc": n["source_loc"]})
    for p in props:
        k = "gap" if p["type"] == "缺口" else "prop"
        nodes.append({"id": p["prop_id"], "kind": k, "label": p["statement"], "type": p["type"],
                      "status": p["status"], "code": code_by_prop.get(p["prop_id"], ""),
                      "doc": p["source_doc"]})
    edges = []
    for h in hg["hyperedges"]:
        edges.append({"id": h["id"], "kind": "hyper", "src": h["premises"], "dst": h["conclusion"],
                      "rel": "重组实现", "doc": ";".join(h["source_doc"]), "verified": True, "method": "论证表"})
    for d in hg["directed_edges"]:
        edges.append({"id": d["id"], "kind": "dir", "src": [d["source"]], "dst": [d["target"]],
                      "rel": d["type"], "doc": d["source_doc"], "verified": True, "method": "论证表"})
    for e in claim_edges:
        if e["dst_id"].startswith("DISC:"):
            continue
        s = e["src_id"]
        kind = ("claim" if not s.startswith("D") else "doc")
        edges.append({"id": f"{s}~{e['dst_id']}~{e['relation']}", "kind": kind, "src": [s], "dst": [e["dst_id"]],
                      "rel": e["relation"], "doc": "", "verified": e["verified"], "method": e["method"],
                      "confidence": e["confidence"]})
    for e in gap_edges:
        gp = {g["gap_code"]: g["prop_id"] for g in gap_rows}
        if e["src"] in gp and e["dst"] in gp:
            edges.append({"id": f"GAP~{e['src']}~{e['dst']}", "kind": "claim", "src": [gp[e["src"]]],
                          "dst": [gp[e["dst"]]], "rel": "缺口前置", "doc": "", "verified": e["verified"],
                          "method": e["method"], "confidence": "high" if e["verified"] else "low"})
    kg = {"nodes": nodes, "edges": edges,
          "stats": {"concepts": sum(1 for n in nodes if n["kind"] == "concept"),
                    "props": sum(1 for n in nodes if n["kind"] == "prop"),
                    "gaps": sum(1 for n in nodes if n["kind"] == "gap"),
                    "relations": sum(1 for e in edges if e["kind"] in ("hyper", "dir")),
                    "claim_edges": sum(1 for e in edges if e["kind"] in ("claim", "doc")),
                    "verified_edges": sum(1 for e in edges if e.get("verified"))}}
    with io.open(os.path.join(S03, "知识图谱.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(kg, f, ensure_ascii=False)
    gp = sum(1 for e in claim_edges if e["relation"] == "术语重叠（候选）")
    print(f"[OK] 缺口对照 {len(gap_rows)}；缺口依赖边 {len(gap_edges)}；claim 边 {len(claim_edges)}"
          f"（其中候选 {gp}）；别名 {len(alias_rows)}；论证对齐 {len(align_rows)}")
    print("     状态一致性：", dict(Counter(g["status_consistent"] for g in gap_rows)))
    print("     论证前件 ID 数与前件数一致：",
          f'{sum(1 for r in align_rows if r["count_ok"])}/{len(align_rows)}')
    print("     claim 边类型：", dict(Counter(e["relation"] for e in claim_edges)))
    print("     知识图谱：", kg["stats"])
    print("     图谱大小:", f"{os.path.getsize(os.path.join(S03, '知识图谱.json')):,} B")


if __name__ == "__main__":
    main()
