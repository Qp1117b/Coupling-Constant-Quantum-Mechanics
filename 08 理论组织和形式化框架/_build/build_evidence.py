# -*- coding: utf-8 -*-
"""
维度1/7 · 证据层（Evidence Layer）—— 让每条结构化断言都能回溯到原文

背景：既有结构化条目（概念/命题/论证）只有 `source_doc` + 人工填的 `source_loc`，
没有字符偏移、没有原文引文，因此"是否忠实于原文"无法机器核验。
本脚本从 `00_外部引用/引用清单.yaml` 列出的 52 篇理论文本（**只读**）建立：

  00_外部引用/语料清单.csv     每篇文档的指纹、字符数、句数、引用层
  00_外部引用/章节索引.csv     标题树（层级、编号、标题、标题行/正文的字符区间、父节点）
  00_外部引用/句索引/句索引.jsonl  句子级索引（doc_id, sid, start, end, kind, text）
  00_外部引用/证据映射.csv     每个结构化条目 → 文档 / 章节 / 证据句 / 字符区间 / 引文 / 定位方法 / 置信分
  00_外部引用/证据映射.json    同上 + Top-3 候选句 + 章节区间（供前端证据面板使用）

定位策略（分级、**绝不虚构**）：
  1) exact    —— 断言文本（或其最长连续片段）在出处文档中逐字出现 → 记其精确区间；
  2) section  —— 依据 `source_loc`（§7.1 / §一 / 假设二 / 标题 …）解析到章节区间，
                 并在章节内按 IDF 加权词覆盖度回排句子；
  3) doc      —— 章节无法解析时退化为全篇回排；
  4) unresolved —— 既无逐字片段也无可用章节（如实登记，不猜）。

所有机器定位结果 `verified` 一律为 False（人工复核后才置 True）——这是本层的诚实边界。

运行：python build_evidence.py
"""
import csv
import gzip
import hashlib
import io
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

try:
    import jieba
    jieba.setLogLevel(60)
except Exception:  # pragma: no cover
    jieba = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # 08 理论组织和形式化框架
P = os.path.dirname(ROOT)                                            # 项目根
S00 = os.path.join(ROOT, "00_外部引用")
S01 = os.path.join(ROOT, "01_结构化数据")

HEAD = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$", re.M)
STOP = set("的了和与及或在是有为对从到把被将则不也都很上中下内外一二三四五六七八九十个之其所以因此如果那么这那对于以及并且或者一个我们他们它他她本文本理论".strip())

# ---------------------------------------------------------------- 语料装载

def load_manifest():
    txt = io.open(os.path.join(S00, "引用清单.yaml"), encoding="utf-8").read()
    docs = []
    for m in re.finditer(r"\{id:\s*(D\d+),\s*path:\s*([^,]+),\s*title:\s*([^,]+),\s*layer:\s*(\d+),\s*type:\s*([^}]+)\}", txt):
        docs.append({"doc_id": m.group(1), "path": m.group(2).strip(), "title": m.group(3).strip(),
                     "layer": int(m.group(4)), "type": m.group(5).strip()})
    return docs


def read_doc(path):
    full = os.path.join(P, path.replace("/", os.sep))
    if not os.path.exists(full):
        return None, None
    raw = io.open(full, encoding="utf-8", errors="replace").read()
    return full, raw


# ---------------------------------------------------------------- 结构解析

def parse_sections(text):
    """返回标题树：level/title/number/heading_start/body_start/body_end/parent。"""
    marks = []
    for m in HEAD.finditer(text):
        line_start = text.rfind("\n", 0, m.start()) + 1
        marks.append({"level": len(m.group(1)), "title": m.group(2).strip(), "heading_start": line_start,
                      "body_start": m.end() + 1})
    secs = []
    for i, mk in enumerate(marks):
        end = len(text)
        for nxt in marks[i + 1:]:
            if nxt["level"] <= mk["level"]:
                end = nxt["heading_start"]
                break
        parent = None
        for j in range(i - 1, -1, -1):
            if marks[j]["level"] < mk["level"]:
                parent = j
                break
        num = ""
        mnum = re.match(r"^[§\s]*([0-9]+(?:\.[0-9]+)*)", mk["title"])
        if mnum:
            num = mnum.group(1)
        else:
            mcn = re.match(r"^([一二三四五六七八九十百]+)\s*[、.．]", mk["title"])
            if mcn:
                num = mcn.group(1)
        secs.append({"level": mk["level"], "title": mk["title"], "number": num,
                     "heading_start": mk["heading_start"], "body_start": mk["body_start"],
                     "body_end": end, "parent": parent})
    return secs


def split_sentences(text):
    """句级切分：保护行内公式 $...$、行内代码 `...`，跳过围栏代码块；表格/标题/列表单独标注 kind。"""
    out = []
    i, n = 0, len(text)
    in_fence = False
    while i < n:
        line_end = text.find("\n", i)
        if line_end < 0:
            line_end = n
        line = text[i:line_end]
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out.append((i, line_end, "code"))
            i = line_end + 1
            continue
        if in_fence:
            out.append((i, line_end, "code"))
            i = line_end + 1
            continue
        if not stripped:
            i = line_end + 1
            continue
        if stripped.startswith("#"):
            out.append((i, line_end, "heading"))
            i = line_end + 1
            continue
        if stripped.startswith("|"):
            out.append((i, line_end, "table"))
            i = line_end + 1
            continue
        kind = "quote" if stripped.startswith(">") else ("list" if re.match(r"^([-*+]|\d+[.)])\s", stripped) else "prose")
        # 行内切句
        j, seg_start, esc = i, i, False
        while j < line_end:
            ch = text[j]
            if ch in "$`":
                esc = not esc
            if not esc and ch in "。！？!?":
                out.append((seg_start, j + 1, kind))
                seg_start = j + 1
            elif not esc and ch == "；" and (j - seg_start) > 40:
                out.append((seg_start, j + 1, kind))
                seg_start = j + 1
            j += 1
        if seg_start < line_end:
            seg = text[seg_start:line_end]
            if seg.strip():
                out.append((seg_start, line_end, kind))
        i = line_end + 1
    return out


# ---------------------------------------------------------------- 词语与检索

PUNCT = re.compile(r"^[\s\W_]+$")


def _clean_md(s):
    """去 markdown 标记（链接、强调符、行内标记符、表格行的分列竖线）。
    只在**数学区间之外**调用。"""
    # 行内代码 `…`：内容原样保留——其中的 `_` 是标识符的一部分
    # （实测 ``bcsTcFromIntegral_solved``、``CQM_核心_因果网络同步理论.md`` 曾被削成
    #  ``bcsTcFromIntegralsolved``、``CQM核心…``）
    code = []

    def _keep(m):
        code.append(m.group(1))
        return "\x00C%d\x00" % (len(code) - 1)

    s = re.sub(r"`([^`]*)`", _keep, s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[*#]+", "", s)
    s = s.replace(">", "")
    # 下划线：`\pi_p` / `x_5` / `K_{…}` 这类 LaTeX 下标、标识符 a_b 原样保留；
    # 只有 markdown 斜体 `_…_` 的 _ 才去掉（判据：前后都成记号字形时视为下标）。
    s = re.sub(r"(?<![A-Za-z0-9_}\\])_|_(?![A-Za-z0-9_{\\])", "", s)
    s = re.sub(r"\x00C(\d+)\x00", lambda m: code[int(m.group(1))], s)
    return s


_QUOTE_MATH_RE = re.compile(r"\$\$[\s\S]*?\$\$|\$[^$\n]+?\$")


def clean_quote(s):
    """去掉 markdown 标记，得到可读引文（原始区间仍保留在 char_start/char_end）。

    数学区间内的 `_` `*` ` 是 LaTeX 记号（下标、上标、模板），不是 markdown 强调。
    旧实现对整个串做 `re.sub(r"[*`_>#]+", "")`，把 `$\\bar{\\delta}_v$` 清成
    `$\\bar{\\delta}v$`、`$[\\hat{X}_v,\\hat{P}_v]$` 清成 `$[\\hat{X}v,\\hat{P}v]$`
    —— 实测 213 条引文中 69 条下标整段丢失，卡片与检索台显示错误公式。
    故先把数学区间整段取出（占位符保护），只清洗区间之外的文本——区间外另见
    _clean_md 的下标感知与行内代码保护；表格行的分列竖线也只在区间外改全角，
    否则会把 `\\big|_{s=1}` 这类区间内竖线一并切开。
    """
    segs, math, last = [], [], 0
    for m in _QUOTE_MATH_RE.finditer(s):
        segs.append(_clean_md(s[last:m.start()]))
        math.append(m.group(0))
        segs.append("\x01M%d\x01" % (len(math) - 1))
        last = m.end()
    segs.append(_clean_md(s[last:]))
    t = "".join(segs)
    t = re.sub(r"^\s*([-+*]|\d+[.)])\s+", "", t)     # 行首项目符号（整串一次）
    t = re.sub(r"\s+", " ", t).strip()
    # 整条引文就是一行表格（首尾为竖线）→ 把分列竖线改全角，避免引文里露出
    # ASCII 断行竖线（检索台按「…」原样显示，会看着像表格没解析）。
    if t.count("|") >= 2 and t.startswith("|") and t.endswith("|"):
        cells = [c.strip() for c in t.strip("|").split("|")]
        while cells and not cells[0]:
            cells.pop(0)
        while cells and not cells[-1]:
            cells.pop()
        if len(cells) >= 2:
            t = " ｜ ".join(cells)
    return re.sub(r"\x01M(\d+)\x01", lambda m: math[int(m.group(1))], t)


def _balance_end(text, st, en, limit=48):
    """把引文右界推进到 LaTeX 组体闭合处（不改逐字事实，quote 仍是 text[st:en]）。

    句切分在 `\\text{…}` 组体内的「。」上断开时，区间终点会停在收尾「}」之前
    （实测 3 条：C080/P016 的 `\\text{…分化。`、H013 的 `$$\\boxed{\\text{…`）。
    这样的引文在前端补 `$…$` 后 MathJax 无法配对，LaTeX 原文裸露在检索台上。
    只在**同一行、邻近**范围内补齐；跨行或过远则不动（宁缺勿错）。
    """
    d = text[st:en].count("{") - text[st:en].count("}")
    if d <= 0:
        return en
    k = en
    while k < len(text) and (k - en) < limit and d > 0:
        ch = text[k]
        if ch == "\n":
            break
        if ch == "{":
            d += 1
        elif ch == "}":
            d -= 1
        k += 1
    return k


def is_weak(seg):
    """目录行 / 纯链接行 / 短标题行——不宜作为证据。"""
    if "](#" in seg or seg.count("](") >= 2:
        return True
    if len(re.sub(r"[\s\W]", "", seg)) < 8:
        return True
    return False


def name_anchored(name, cited_doc, sec, sent_of_doc, doc_text, doc_layer):
    """概念名锚定：先在本篇找含该名的句子，找不到再按引用层序在全库找（只认逐字出现，不猜）。
    返回按『本节优先 → prose 优先 → 位置靠前』排序的候选列表。"""
    if not name:
        return []
    order = [cited_doc] + [d for d in sorted(doc_text, key=lambda x: (doc_layer.get(x, 9), x)) if d != cited_doc]
    sect = (sec["body_start"], sec["body_end"]) if sec else (-1, -1)
    for d in order:
        raw = doc_text.get(d, "")
        hits = [(d, st, en, kind, sid) for (st, en, kind, sid) in sent_of_doc.get(d, [])
                if kind != "code" and name in raw[st:en]]
        if hits:
            hits.sort(key=lambda t: (0 if sect[0] <= t[1] < sect[1] else 1,
                                     0 if t[3] == "prose" else (1 if t[3] == "list" else 2), t[1]))
            return hits[:6]
    return []


def tokenize(s):
    s = s.strip()
    if not s:
        return []
    if jieba is None:
        return [t for t in re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z][A-Za-z0-9_]{2,}", s)]
    toks = []
    for t in jieba.lcut(s):
        t = t.strip()
        if not t or PUNCT.match(t):
            continue
        if re.match(r"^[\u4e00-\u9fff]+$", t):
            if len(t) >= 2 and t not in STOP:
                toks.append(t)
        elif re.match(r"^[A-Za-z][A-Za-z0-9_\-]{1,}$", t):
            toks.append(t.lower())
    return toks


def longest_common_run(a, b, minimum=8):
    """a 中在 b 里逐字出现的最长连续片段 → (长度, a 中起点, b 中起点)。"""
    if not a or not b:
        return 0, 0, 0
    for L in range(len(a), minimum - 1, -1):
        for i in range(0, len(a) - L + 1):
            j = b.find(a[i:i + L])
            if j >= 0:
                return L, i, j
    return 0, 0, 0


def resolve_section(secs, loc, doc_text):
    """把人工填的 source_loc 解析到章节。返回 (sec_dict|None, status)。"""
    loc = (loc or "").strip()
    if not loc:
        return None, "empty"
    toks = re.findall(r"§\s*([0-9]+(?:\.[0-9]+)*)", loc)
    if toks:
        for t in toks:
            cand = [s for s in secs if s["number"] == t]
            if not cand:
                cand = [s for s in secs if s["number"].startswith(t + ".")]
            if not cand:
                cand = [s for s in secs if t in s["title"]]
            if cand:
                return min(cand, key=lambda s: s["level"]), "section"
    cn = re.findall(r"§\s*([一二三四五六七八九十百]+)", loc)
    if cn:
        for t in cn:
            cand = [s for s in secs if s["number"] == t or re.match(r"^" + t + r"\s*[、.．]", s["title"])]
            if cand:
                return min(cand, key=lambda s: s["level"]), "section"
    kw = re.sub(r"^(§|第)?", "", loc)
    kw = re.sub(r"[\d\.;；,，\s]+$", "", kw)
    if kw and len(kw) >= 2:
        cand = [s for s in secs if kw in s["title"]]
        if cand:
            return max(cand, key=lambda s: len(s["title"])), "section"
    return None, "fail"


# ---------------------------------------------------------------- 主流程

def main():
    docs = load_manifest()
    corpus_rows, sec_rows, sent_rows = [], [], []
    doc_text, doc_secs = {}, {}
    sent_of_doc = defaultdict(list)

    for d in docs:
        full, raw = read_doc(d["path"])
        if raw is None:
            print(f"[WARN] 缺文件：{d['doc_id']} {d['path']}")
            continue
        doc_text[d["doc_id"]] = raw
        secs = parse_sections(raw)
        doc_secs[d["doc_id"]] = secs
        for k, s in enumerate(secs):
            sec_rows.append({"doc_id": d["doc_id"], "sec_idx": k, "level": s["level"], "number": s["number"],
                             "title": s["title"], "heading_start": s["heading_start"],
                             "body_start": s["body_start"], "body_end": s["body_end"],
                             "parent": "" if s["parent"] is None else s["parent"]})
        sents = split_sentences(raw)
        for k, (st, en, kind) in enumerate(sents):
            sent_rows.append({"doc_id": d["doc_id"], "sid": k, "start": st, "end": en, "kind": kind,
                              "text": raw[st:en]})
            sent_of_doc[d["doc_id"]].append((st, en, kind, k))
        corpus_rows.append({
            "doc_id": d["doc_id"], "path": d["path"], "title": d["title"], "layer": d["layer"], "type": d["type"],
            "chars": len(raw), "sentences": len(sents), "sections": len(secs),
            "sha256_16": hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16],
        })

    # ---- 逆文档频率（供句子回排）----
    df = Counter()
    for r in sent_rows:
        for t in set(tokenize(r["text"])):
            df[t] += 1
    N = max(1, len(sent_rows))
    idf = {t: math.log(1 + N / (1 + c)) for t, c in df.items()}

    # ---- 待定位的结构化条目 ----
    def rd(name):
        with io.open(os.path.join(S01, name), encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))

    concepts, props, args = rd("概念表.csv"), rd("命题表.csv"), rd("论证表.csv")
    items = []
    for c in concepts:
        items.append({"struct_id": c["concept_id"], "kind": "概念", "name": c["name"],
                      "text": c["definition"], "query": c["name"] + " " + c["definition"],
                      "doc": c["source_doc"], "loc": c["source_loc"]})
    for p in props:
        items.append({"struct_id": p["prop_id"], "kind": "缺口" if p["type"] == "缺口" else "命题",
                      "name": p["statement"][:24], "text": p["statement"], "query": p["statement"],
                      "doc": p["source_doc"], "loc": ""})
    for a in args:
        items.append({"struct_id": a["arg_id"], "kind": "论证", "name": a["conclusion"],
                      "text": a["premises"] + " ⇒ " + a["conclusion"],
                      "query": a["premises"] + " " + a["conclusion"] + " " + a["type"],
                      "doc": a["source_doc"].split(";")[0].strip(), "loc": ""})

    # ---- 逐条定位 ----
    doc_layer = {r["doc_id"]: r["layer"] for r in corpus_rows}
    ev_rows, ev_json = [], []
    for it in items:
        did = it["doc"].split(";")[0].strip()
        raw = doc_text.get(did)
        rec = {"struct_id": it["struct_id"], "kind": it["kind"], "name": it["name"], "doc_id": did,
               "loc_raw": it["loc"], "loc_status": "no_doc", "sec_title": "", "sec_start": "", "sec_end": "",
               "sid": "", "char_start": "", "char_end": "", "quote": "", "quote_clean": "",
               "match_method": "unresolved", "verbatim_run": 0, "name_hit": False, "doc_switch": False,
               "evidence_doc": did, "score": 0.0, "confidence": "unresolved", "verified": False}
        cands = []
        if raw:
            secs = doc_secs.get(did, [])
            sec, loc_status = resolve_section(secs, it["loc"], raw)
            # 1) 逐字片段
            plain = re.sub(r"\s+", "", it["text"])
            L, ai, bj = longest_common_run(plain, raw, minimum=8)
            rec["verbatim_run"] = L
            anchored = name_anchored(it["name"], did, sec, sent_of_doc, doc_text, doc_layer) if it["kind"] == "概念" else []
            if L >= max(8, int(len(plain) * 0.6)):
                ce = _balance_end(raw, bj, bj + L)
                rec.update(match_method="exact", char_start=bj, char_end=ce,
                           quote=raw[bj:ce], quote_clean=clean_quote(raw[bj:ce]), loc_status=loc_status,
                           sec_title=sec["title"] if sec else "", sec_start=sec["body_start"] if sec else "",
                           sec_end=sec["body_end"] if sec else "", score=round(L / max(1, len(plain)), 3),
                           name_hit=bool(it["name"][:6] and it["name"][:6] in raw[bj:bj + L]),
                           confidence="high" if L >= 10 else "medium")
            elif anchored:
                ed, st, en, kind, sid = anchored[0]
                eraw = doc_text[ed]
                en = _balance_end(eraw, st, en)
                toks = set(tokenize(eraw[st:en]))
                qt = set(tokenize(it["query"])) | set(tokenize(it["name"]))
                sc = round(sum(idf.get(t, 1.0) for t in qt & toks) / math.sqrt(max(4, len(toks))) + 3.0, 3)
                rec.update(match_method="name", loc_status=loc_status, score=sc,
                           confidence="high" if sc >= 5 else "medium", sid=sid,
                           char_start=st, char_end=en, quote=eraw[st:en], quote_clean=clean_quote(eraw[st:en]),
                           name_hit=True, evidence_doc=ed, doc_switch=(ed != did),
                           sec_title=sec["title"] if sec else "", sec_start=sec["body_start"] if sec else "",
                           sec_end=sec["body_end"] if sec else "")
                for (d2, s2, e2, k2, i2) in anchored[1:4]:
                    cands.append({"score": sc, "sid": i2, "doc_id": d2, "char_start": s2, "char_end": e2,
                                  "quote": clean_quote(doc_text[d2][s2:e2]), "kind": k2})
            else:
                lo, hi = (sec["body_start"], sec["body_end"]) if sec else (0, len(raw))
                qt = set(tokenize(it["query"]))
                for t in tokenize(it["name"]):
                    qt.add(t)
                name_probe = it["name"][:6]
                scored = []
                for (st, en, kind, sid) in sent_of_doc.get(did, []):
                    if st < lo or en > hi or kind in ("heading", "code"):
                        continue
                    body = raw[st:en]
                    if is_weak(body):
                        continue
                    toks = set(tokenize(body))
                    hit = sum(idf.get(t, 1.0) for t in qt & toks)
                    if not hit:
                        continue
                    bonus = 0.0
                    if name_probe and name_probe in body:
                        bonus += 4.0
                    elif it["name"][:3] and it["name"][:3] in body:
                        bonus += 1.5
                    if kind == "prose":
                        bonus += 0.6
                    elif kind == "table":
                        bonus += 0.2
                    scored.append((hit / math.sqrt(max(4, len(toks))) + bonus, st, en, kind, sid))
                scored.sort(reverse=True)
                for sc, st, en, kind, sid in scored[:3]:
                    ce = _balance_end(raw, st, en)
                    cands.append({"score": round(sc, 3), "sid": sid, "char_start": st, "char_end": ce,
                                  "quote": clean_quote(raw[st:ce]), "kind": kind})
                if scored:
                    sc, st, en, kind, sid = scored[0]
                    en = _balance_end(raw, st, en)
                    conf = ("high" if ((sec and sc >= 6.0) or ((not sec) and sc >= 9.0))
                            else ("medium" if sc >= 3.5 else "low"))
                    rec.update(match_method=("section" if sec else "doc"),
                               loc_status=loc_status, score=round(sc, 3), sid=sid, confidence=conf,
                               name_hit=bool(name_probe and name_probe in raw[st:en]),
                               char_start=st, char_end=en, quote=raw[st:en], quote_clean=clean_quote(raw[st:en]),
                               sec_title=sec["title"] if sec else "",
                               sec_start=sec["body_start"] if sec else "", sec_end=sec["body_end"] if sec else "")
                elif sec:
                    be = _balance_end(raw, sec["body_start"], min(sec["body_end"], sec["body_start"] + 400))
                    rec.update(match_method="section", loc_status=loc_status, sec_title=sec["title"],
                               sec_start=sec["body_start"], sec_end=sec["body_end"], confidence="medium",
                               char_start=sec["body_start"], char_end=be,
                               quote=raw[sec["body_start"]:be],
                               quote_clean=clean_quote(raw[sec["body_start"]:be]), score=0.5)
                else:
                    rec.update(loc_status=loc_status, confidence="unresolved")
        ev_rows.append(rec)
        ev_json.append(dict(rec, candidates=cands))
        if it["loc"] == "" and rec["match_method"] in ("section", "doc"):
            ev_rows[-1]["loc_raw"] = f"（未给 source_loc，机器回排 {rec['match_method']}）"

    # ---- 人工复核合入（00_外部引用/复核结果.csv）----
    # 复核 CSV 由「检索台 · 证据复核」模式导出后放置于此：
    #   列 = struct_id, verdict(approved|rejected|unsure), reviewer, note, reviewed_at
    # 仅 verdict=approved **且 reviewer 非空** 才置 verified=True ——
    # 机器定位不是人工核验；无复核文件时全部保持 False。
    review_path = os.path.join(S00, "复核结果.csv")
    reviews = {}
    if os.path.exists(review_path):
        with io.open(review_path, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                sid = (r.get("struct_id") or "").strip()
                v = (r.get("verdict") or "").strip()
                if sid and v in ("approved", "rejected", "unsure"):
                    reviews[sid] = r
    for rec in ev_rows + ev_json:
        rv = reviews.get(rec["struct_id"])
        rec["review_verdict"] = (rv.get("verdict", "") if rv else "")
        rec["reviewer"] = (rv.get("reviewer", "") if rv else "")
        rec["review_note"] = ((rv.get("note", "") if rv else "")[:200])
        rec["reviewed_at"] = (rv.get("reviewed_at", "") if rv else "")
        rec["verified"] = bool(rv and rv["verdict"] == "approved"
                               and (rv.get("reviewer") or "").strip())
    known = {r["struct_id"] for r in ev_rows}
    unknown = sorted(set(reviews) - known)
    if unknown:
        print(f"[WARN] 复核结果含未知条目（忽略）: {unknown[:6]}")
    n_ver = sum(1 for r in ev_rows if r["verified"])
    n_rev = len(reviews)
    print(f"     复核合入: {review_path if os.path.exists(review_path) else '（无复核文件）'}"
          f" → 记录 {n_rev} 条 / verified=True {n_ver} 条")

    # ---- 写出 ----
    def wcsv(name, rows, cols=None):
        os.makedirs(S00, exist_ok=True)
        cols = cols or list(rows[0].keys())
        with io.open(os.path.join(S00, name), "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in rows:
                w.writerow(r)

    wcsv("语料清单.csv", corpus_rows)
    wcsv("章节索引.csv", sec_rows)
    wcsv("证据映射.csv", ev_rows)
    os.makedirs(os.path.join(S00, "句索引"), exist_ok=True)
    with io.open(os.path.join(S00, "句索引", "句索引.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        for r in sent_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with io.open(os.path.join(S00, "证据映射.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"docs": corpus_rows, "evidence": ev_json}, f, ensure_ascii=False)

    # ---- 报告 ----
    meth = Counter(r["match_method"] for r in ev_rows)
    loc = Counter(r["loc_status"] for r in ev_rows)
    print(f"[OK] 语料 {len(corpus_rows)} 篇 / {sum(r['chars'] for r in corpus_rows):,} 字符 / {len(sent_rows):,} 句")
    print(f"     章节 {len(sec_rows)} 个；证据映射 {len(ev_rows)} 条")
    print("     定位方法:", dict(meth))
    print("     source_loc 解析:", dict(loc))
    cov = sum(1 for r in ev_rows if r["match_method"] != "unresolved")
    print(f"     有证据（章节或句）: {cov}/{len(ev_rows)} = {cov/len(ev_rows):.1%}")
    print("     置信分布:", dict(Counter(r["confidence"] for r in ev_rows)))
    runs = sorted(r["verbatim_run"] for r in ev_rows)
    print(f"     最长逐字重合：中位 {runs[len(runs)//2]} 字 / ≥8 字 {sum(1 for r in runs if r >= 8)}/{len(runs)}"
          f" / ≥15 字 {sum(1 for r in runs if r >= 15)}")
    print(f"     证据句含概念名: {sum(1 for r in ev_rows if r['name_hit'])}/{len(ev_rows)}")
    print("     ---- 抽样（struct_id / 方法 / 置信 / 分 / 引文前 46 字）----")
    for r in ev_rows[:4] + ev_rows[82:86] + ev_rows[145:149] + ev_rows[-3:]:
        print(f"     {r['struct_id']:<5} {r['match_method']:<9} {r['confidence']:<9} {r['score']:<7} "
              f"{r['quote_clean'][:46]}")
    print(f"     证据映射.json 大小: {os.path.getsize(os.path.join(S00, '证据映射.json')):,} B")


if __name__ == "__main__":
    main()
