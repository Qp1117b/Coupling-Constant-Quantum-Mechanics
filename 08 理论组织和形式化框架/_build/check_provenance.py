# -*- coding: utf-8 -*-
"""
组织层证据完整性硬检查（证据层执行器）

校验 `00_外部引用/证据映射.csv` 与句索引/章节索引/原文的一致性：
  1. 覆盖：每条结构化断言（82 概念 + 63 命题 + 70 论证）恰有一条证据记录；
  2. 完整性：quote 必须**逐字等于**原文 [char_start, char_end) 区间；
  3. 边界：区间落在文档字符数之内，且 start < end；
  4. 枚举：match_method / confidence / loc_status 取值合法；
  5. 诚实：verified 默认全 False（人工复核后才可置 True），如实统计；
  6. 追溯：evidence_doc 必须是引用清单内文档，doc_switch 需显式标记。

退出码 0 = 通过；非 0 = 证据层存在硬失败（研究视为未完成）。
运行：python check_provenance.py
"""
import csv
import io
import json
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.dirname(ROOT)
S00, S01 = os.path.join(ROOT, "00_外部引用"), os.path.join(ROOT, "01_结构化数据")
METHODS = {"exact", "name", "section", "doc", "unresolved"}
CONFS = {"high", "medium", "low", "unresolved"}
LOCS = {"section", "fail", "empty", "no_doc"}
results = []


def rec(lv, name, detail=""):
    results.append((lv, name, detail))


def check(name, cond, detail=""):
    rec("PASS" if cond else "FAIL", name, detail)


def rd(p, base):
    with io.open(os.path.join(base, p), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    concepts = rd("概念表.csv", S01)
    props = rd("命题表.csv", S01)
    args = rd("论证表.csv", S01)
    ev = rd("证据映射.csv", S00)
    corpus = {r["doc_id"]: r for r in rd("语料清单.csv", S00)}
    manifest = set()
    txt = io.open(os.path.join(S00, "引用清单.yaml"), encoding="utf-8").read()
    import re
    for m in re.finditer(r"\{id:\s*(D\d+),", txt):
        manifest.add(m.group(1))

    want = {c["concept_id"] for c in concepts} | {p["prop_id"] for p in props} | {a["arg_id"] for a in args}
    got = [r["struct_id"] for r in ev]
    check("证据条数 = 结构化断言数", len(ev) == len(want), f"{len(ev)} vs {len(want)}")
    check("每个断言恰有一条证据", set(got) == want and len(got) == len(set(got)),
          f"缺 {sorted(want - set(got))[:5]} 多 {sorted(set(got) - want)[:5]}")

    docs, bad_quote, bad_range = {}, 0, 0
    for r in ev:
        did = r.get("evidence_doc") or r.get("doc_id")
        if did not in docs:
            path = None
            for d in corpus.values():
                if d["doc_id"] == did:
                    path = os.path.join(P, d["path"])
            docs[did] = io.open(path, encoding="utf-8", errors="replace").read() if path and os.path.exists(path) else None
        raw = docs.get(did)
        if raw is None:
            rec("WARN", f"文档不可读 {did}", "")
            continue
        try:
            st, en = int(r["char_start"]), int(r["char_end"])
        except Exception:
            if r["match_method"] != "unresolved":
                bad_range += 1
            continue
        if not (0 <= st < en <= len(raw)):
            bad_range += 1
            continue
        if r["quote"] and raw[st:en] != r["quote"]:
            bad_quote += 1
    check("quote 与字符区间逐字一致", bad_quote == 0, f"{bad_quote} 条不一致")
    check("字符区间落在文档范围内", bad_range == 0, f"{bad_range} 条越界/缺失")

    check("match_method 取值合法", all(r["match_method"] in METHODS for r in ev),
          str({r["match_method"] for r in ev} - METHODS))
    check("confidence 取值合法", all(r["confidence"] in CONFS for r in ev),
          str({r["confidence"] for r in ev} - CONFS))
    check("loc_status 取值合法", all(r["loc_status"] in LOCS for r in ev),
          str({r["loc_status"] for r in ev} - LOCS))
    check("证据文档都在引用清单内", all((r.get("evidence_doc") or r.get("doc_id")) in manifest for r in ev),
          str([r["struct_id"] for r in ev if (r.get("evidence_doc") or r.get("doc_id")) not in manifest][:5]))
    switch = [r for r in ev if str(r.get("doc_switch")) == "True"]
    check("跨文档证据显式标记 doc_switch", all(r["match_method"] == "name" for r in switch),
          f"{len(switch)} 条")

    verified = sum(1 for r in ev if str(r["verified"]) == "True")
    covered = sum(1 for r in ev if r["match_method"] != "unresolved")

    # ---- 人工复核闭环：verified ⟺ (approved 且有复核人) ----
    rev_path = os.path.join(S00, "复核结果.csv")
    n_reviews = 0
    if os.path.exists(rev_path):
        with io.open(rev_path, encoding="utf-8-sig", newline="") as f:
            reviews = list(csv.DictReader(f))
        n_reviews = len(reviews)
        check("复核结果结构合法",
              all((r.get("struct_id") or "").strip() and
                  r.get("verdict") in ("approved", "rejected", "unsure") for r in reviews),
              f"{n_reviews} 条记录")
        known_ids = {r["struct_id"] for r in ev}
        bad_ids = sorted({(r.get("struct_id") or "").strip() for r in reviews} - known_ids)
        check("复核 struct_id 全部存在于证据映射", not bad_ids, str(bad_ids[:5]))
        check("approved 均带复核人",
              all((r.get("reviewer") or "").strip() for r in reviews if r.get("verdict") == "approved"))
        rmap = {r["struct_id"]: r for r in reviews if (r.get("struct_id") or "").strip()}
        mismatch = []
        for x in ev:
            rv = rmap.get(x["struct_id"])
            should = bool(rv and rv["verdict"] == "approved" and (rv.get("reviewer") or "").strip())
            if (str(x["verified"]) == "True") != should:
                mismatch.append(x["struct_id"])
        check("verified ⟺ (approved 且有复核人)", not mismatch, str(mismatch[:6]))
    else:
        check("无复核文件时 verified 全为 False", verified == 0, str(verified))

    with_quote = sum(1 for r in ev if r["quote"])
    nf = sum(1 for lv, _, _ in results if lv == "FAIL")
    nw = sum(1 for lv, _, _ in results if lv == "WARN")
    print("=" * 70)
    for lv, name, detail in results:
        mark = {"PASS": "  OK ", "FAIL": "FAIL ", "WARN": "WARN "}[lv]
        print(f"[{mark}] {name}" + (f"   ({detail})" if detail and lv != "PASS" else ""))
    print("-" * 70)
    print(f"证据覆盖 {covered}/{len(ev)} = {covered/len(ev):.1%} | 含引文 {with_quote} | "
          f"人工复核记录 {n_reviews} | verified=True {verified}")
    print("方法分布:", dict(Counter(r["match_method"] for r in ev)))
    print("置信分布:", dict(Counter(r["confidence"] for r in ev)))
    print(f"检查项 {len(results)}：通过 {len(results)-nf-nw} · 失败 {nf} · 警告 {nw}")
    print("结果：" + ("全部通过" if nf == 0 else "存在硬失败——证据层未完成"))
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main())
