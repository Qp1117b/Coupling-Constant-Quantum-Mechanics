# -*- coding: utf-8 -*-
"""
维度 2 · 抽取流水线（术语发现 / 关系抽取 / 评测 / 语义特征）

目标：把"人工策展"升级为**可复现、可评测**的抽取层，且不越红线——
  · 抽出的新术语只进「候选池」，**不得**写入概念表；
  · 关系抽取只在原文既有表述内定位，输出候选并**以 69 条人工论证表为金标准算 P/R/F1**；
  · 语义特征完全由本语料自训练（TF-IDF），不引入任何外部模型或理论外知识。

方法与主流一致：
  术语发现   n-gram（2–5）→ 频次 + 内部凝固度(PMI) + 左右邻接熵（无监督新词发现）
  术语打分   简化 C-value（Frantzi & Ananiadou）：嵌套惩罚 + log 长度加权
  关系抽取   概念名共现句 + 关系模式模板（⇒/→/对应/等价/依赖/包含/映射/演化…）
  评测       与论证表金标准比对，给出严格（关系类型一致）与宽松（两端一致）指标
  语义特征   概念文档（名称+定义+证据句）TF-IDF → 余弦近邻

产出（05_机器学习数据准备/）：
  术语候选/术语候选.csv       n-gram、频次、PMI、左右熵、C-value、是否已收录
  术语候选/术语候选统计.json
  关系抽取/候选关系.csv        src、dst、rel、句式、证据句、置信、是否命中金标准
  关系抽取/抽取评测.json       P/R/F1、混淆矩阵、样例
  嵌入就绪/语义特征.csv        概念 × 词项 TF-IDF（稀疏长表）
  嵌入就绪/语义近邻.csv        每个概念的 Top-8 语义近邻
运行：python build_extract.py
"""
import csv
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
except Exception:
    jieba = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S00 = os.path.join(ROOT, "00_外部引用")
S01 = os.path.join(ROOT, "01_结构化数据")
S05 = os.path.join(ROOT, "05_机器学习数据准备")
CJK = re.compile(r"[\u4e00-\u9fff]")
TERM_OK = re.compile(r"^[\u4e00-\u9fff]{2,8}$|^[A-Za-z][A-Za-z0-9_\-]{2,}$")
STOP = set("的了和与及或在是有为对从到把被将则不也都很上中下内外一二三四五六七八九十个之其所以因此如果那么这那对于以及并且或者一个我们他们它他她本文本理论可能必须应当由于通过关于基于并且不仅而且由此例如其中以上以下")

REL_PATTERNS = [
    ("重组实现", ["⇒", "重组实现", "多因一果", "共同给出", "共同构成", "综合得到", "联合给出"]),
    ("映射", ["映射为", "映射到", "对应", "给出", "定义为", "记作", "由…得到", "写成"]),
    ("等价", ["等价于", "等价", "等同于", "即", "就是", "同构于"]),
    ("依赖", ["依赖于", "取决于", "前提是", "条件是", "决定了", "由…决定"]),
    ("层级含于", ["包含于", "含于", "属于", "是…的子", "涵盖", "下辖"]),
    ("演化", ["演化为", "演变成", "退化为", "生长为", "发展为", "涌现为"]),
    ("未定", ["→", "->", "得出", "推出"]),   # 有向但类型需人工裁定
]


def rd(path, base):
    with io.open(os.path.join(base, path), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def wcsv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)


def load_sentences():
    out = []
    with io.open(os.path.join(S00, "句索引", "句索引.jsonl"), encoding="utf-8") as f:
        for line in f:
            if line.strip():
                out.append(json.loads(line))
    return out


def discover_terms(text, min_freq=8, max_n=5, min_pmi=8.0, min_entropy=1.0, top_n=800):
    """无监督新词发现：频次 + 内部凝固度(PMI) + 左右邻接熵（阈值经语料实测收紧）。"""
    txt = "".join(ch if CJK.match(ch) else "\u0001" for ch in text)   # 非汉字作硬边界
    ngrams = {n: Counter() for n in range(2, max_n + 1)}
    for n in range(2, max_n + 1):
        for i in range(len(txt) - n + 1):
            g = txt[i:i + n]
            if "\u0001" not in g:
                ngrams[n][g] += 1
    total = {n: max(1, sum(ngrams[n].values())) for n in ngrams}
    uni = Counter()
    for n in ngrams:
        for g, c in ngrams[n].items():
            for ch in g:
                uni[ch] += c
    units = max(1, sum(uni.values()))
    BAD_CH = set("的了和与及或在是有为对从到把被将则不也都很上中下内外之其所以因此如果那么这那着一个我们他们它他她本文")
    cands = {}
    for n in ngrams:
        for g, c in ngrams[n].items():
            if c < min_freq or any(ch in BAD_CH for ch in g):
                continue
            pmi = min(
                math.log2((c / total[n]) / max(1e-12, (uni[g[:k]] / units) * (uni[g[k:]] / units)))
                for k in range(1, n)
            )
            if pmi < min_pmi:
                continue
            cands[g] = {"ngram": g, "n": n, "freq": c, "pmi": round(pmi, 3), "entropy": 0.0}
    left = defaultdict(Counter)
    right = defaultdict(Counter)
    keys = set(cands)
    for i in range(len(txt)):
        for n in range(2, max_n + 1):
            g = txt[i:i + n]
            if len(g) < n:
                break
            if g in keys:
                l = txt[i - 1] if i > 0 else "\u0002"
                r = txt[i + n] if i + n < len(txt) else "\u0002"
                left[g][l] += 1
                right[g][r] += 1
    kept = {}
    for g, c in cands.items():
        def ent(counter):
            tot = sum(counter.values()) or 1
            return -sum((v / tot) * math.log2(v / tot) for v in counter.values())
        e = min(ent(left[g]), ent(right[g]))
        if e < min_entropy:
            continue
        c["entropy"] = round(e, 3)
        kept[g] = c
    return kept, top_n


def c_value(cands, freq_of):
    """简化 C-value：c = log2(len) * (freq - Σ_{longer} freq(longer)/|longer|)"""
    by_len = defaultdict(list)
    for g, c in cands.items():
        by_len[len(g)].append(g)
    out = {}
    for g, c in cands.items():
        longer = [h for h in by_len.get(len(g) + 1, []) if g in h]
        nested = sum(freq_of.get(h, 0) for h in longer) / max(1, len(longer)) if longer else 0
        out[g] = round(math.log2(len(g)) * max(0.0, freq_of.get(g, 0) - nested), 3)
    return out


def main():
    concepts = rd("概念表.csv", S01)
    args = rd("论证表.csv", S01)
    name2id = {c["name"]: c["concept_id"] for c in concepts}
    names = sorted(name2id, key=len, reverse=True)
    sents = load_sentences()
    corpus = "\n".join(s["text"] for s in sents)
    print(f"     语料 {len(sents):,} 句 / {len(corpus):,} 字符")

    # ---------- 1) 术语发现 ----------
    cands, top_n = discover_terms(corpus)
    cv = c_value(cands, {g: c["freq"] for g, c in cands.items()})
    covered = set(names)
    rows = []
    for g, c in sorted(cands.items(), key=lambda kv: -cv.get(kv[0], 0)):
        rows.append({"term": g, "n": c["n"], "freq": c["freq"], "pmi": c["pmi"],
                     "boundary_entropy": c["entropy"], "c_value": cv.get(g, 0),
                     "in_concept_table": g in covered,
                     "candidate_id": f"T{len(rows)+1:04d}",
                     "status": "已收录" if g in covered else "候选待核"})
    rows.sort(key=lambda r: (r["in_concept_table"], -r["c_value"]))
    n_all = len(rows)
    rows = rows[:top_n]
    wcsv(os.path.join(S05, "术语候选", "术语候选.csv"), rows)
    new_rows = [r for r in rows if not r["in_concept_table"]]
    term_stat = {"candidates_after_threshold": n_all, "kept_top_n": len(rows),
                 "already_in_concept_table": len(rows) - len(new_rows),
                 "new_candidates_kept": len(new_rows),
                 "concept_coverage": f"{len(rows)-len(new_rows)}/{len(concepts)}",
                 "thresholds": {"min_freq": 8, "min_pmi": 8.0, "min_boundary_entropy": 1.0, "n_gram": "2-5"},
                 "top_new": [r["term"] for r in new_rows[:40]]}
    with io.open(os.path.join(S05, "术语候选", "术语候选统计.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(term_stat, f, ensure_ascii=False, indent=2)

    # ---------- 2) 关系抽取：分层候选 ----------
    #   pattern 层：两端之间存在关系线索词 → 关系类型由线索词推断
    #   cooccur 层：仅同句共现（方向按文本出现顺序）→ 类型标「未定」，交由人工/LLM 定型
    # 金标准 = 人工论证表；配对召回以「同句共现」为物理上界，逐层逼近该上界。
    gold = set()
    gold_pairs = set()
    for a in args:
        left, right = (a["source_concept"].split("→", 1) + [""])[:2]
        srcs = [x.strip() for x in left.split(";") if x.strip()]
        dsts = [x.strip() for x in right.split(";") if x.strip()]
        for s in srcs:
            for d in dsts:
                gold.add((s, d, a["type"]))
                gold_pairs.add((s, d))
    gold_unord = {tuple(sorted(x)) for x in gold_pairs}
    # 供线索词反查关系类型（平铺：cue → rel）
    cue2rel = []
    for rel, pats in REL_PATTERNS:
        for p in sorted(pats, key=len, reverse=True):
            cue2rel.append((p, rel))

    cand_rows = []
    for s in sents:
        t = s["text"]
        occ = []
        for nm in names:                       # names 已按长度降序，优先长名
            st = t.find(nm)
            while st >= 0:
                if not any(st < e and st2 < st + len(nm) for st2, e, _ in occ):
                    occ.append((st, st + len(nm), nm))
                st = t.find(nm, st + 1)
        occ.sort()
        for i in range(len(occ)):
            for j in range(i + 1, len(occ)):
                c1, c2 = name2id[occ[i][2]], name2id[occ[j][2]]
                if c1 == c2:
                    continue
                gap = occ[j][0] - occ[i][1]
                between = t[occ[i][1]:occ[j][0]] if gap >= 0 else ""
                cue, rel = "", "未定"
                if 0 <= gap <= 60:
                    for p, r in cue2rel:
                        if p in between:
                            cue, rel = p, r
                            break
                layer = "pattern" if cue else "cooccur"
                window = t[occ[i][0]:occ[j][1]]
                cand_rows.append({"src": c1, "dst": c2, "rel_guess": rel, "pattern": cue,
                                  "layer": layer, "doc_id": s["doc_id"], "sid": s["sid"],
                                  "sentence": window[:200],
                                  "in_gold_pair": (c1, c2) in gold_pairs,
                                  "in_gold_unord": tuple(sorted((c1, c2))) in gold_unord,
                                  "gold_rel": next((r for (x, y, r) in gold if (x, y) == (c1, c2)), ""),
                                  "type_hit": (c1, c2, rel) in gold})
    # 去重（同 src/dst：pattern 层优先；其余线索并入 rel_guess 备选）
    seen, dedup = {}, []
    for r in sorted(cand_rows, key=lambda x: 0 if x["layer"] == "pattern" else 1):
        k = (r["src"], r["dst"])
        if k in seen:
            if r["rel_guess"] not in seen[k]["rel_guess"]:
                seen[k]["rel_guess"] += "|" + r["rel_guess"]
            continue
        seen[k] = r
        dedup.append(r)
    dedup.sort(key=lambda r: (r["layer"] != "pattern", r["doc_id"], r["sid"]))
    wcsv(os.path.join(S05, "关系抽取", "候选关系.csv"), dedup)

    pattern_rows = [r for r in dedup if r["layer"] == "pattern"]
    tp_pair = sum(1 for r in dedup if r["in_gold_pair"])
    tp_pat = sum(1 for r in pattern_rows if r["in_gold_pair"])
    tp_unord = sum(1 for r in dedup if r["in_gold_unord"])
    precision = tp_pair / max(1, len(dedup))
    precision_pat = tp_pat / max(1, len(pattern_rows))
    recall = len({(r["src"], r["dst"]) for r in dedup if r["in_gold_pair"]}) / max(1, len(gold_pairs))
    recall_unord = len({tuple(sorted((r["src"], r["dst"]))) for r in dedup if r["in_gold_unord"]}) / max(1, len(gold_pairs))
    recall_pat = len({(r["src"], r["dst"]) for r in pattern_rows if r["in_gold_pair"]}) / max(1, len(gold_pairs))
    typed = [r for r in pattern_rows if r["in_gold_pair"]]
    type_hit = sum(1 for r in typed if r["type_hit"])
    # ---- 召回上界：金标准两端是否在同一句中逐字共现（物理上界）----
    id2name_all = {c["concept_id"]: c["name"] for c in concepts}
    ceiling_hit = 0
    for (a, b) in gold_pairs:
        na, nb = id2name_all.get(a, ""), id2name_all.get(b, "")
        if not na or not nb:
            continue
        if any((na in s["text"] and nb in s["text"]) for s in sents):
            ceiling_hit += 1
    ceiling = ceiling_hit / max(1, len(gold_pairs))
    evalj = {
        "gold_edges": len(gold), "gold_pairs": len(gold_pairs),
        "candidates": len(dedup),
        "pattern_candidates": len(pattern_rows),
        "cooccur_only_candidates": len(dedup) - len(pattern_rows),
        "pair_hits": tp_pair, "pattern_pair_hits": tp_pat,
        "precision_pair": round(precision, 3),
        "precision_pattern": round(precision_pat, 3),
        "recall_pair": round(recall, 3),
        "recall_pair_unordered": round(recall_unord, 3),
        "recall_pattern": round(recall_pat, 3),
        "f1_pair": round(2 * precision * recall / max(1e-9, precision + recall), 3),
        "relation_type_accuracy": round(type_hit / max(1, len(typed)), 3),
        "typed_candidates_on_gold_pairs": len(typed),
        "recall_ceiling_sentence_cooccurrence": round(ceiling, 3),
        "recall_vs_ceiling": round(recall_unord / max(1e-9, ceiling), 3),
        "note": "金标准 = 人工论证表（69 条，含多前件超边展开）。**分层候选**：pattern 层（两端间有关系线索词，"
                "类型可推断）与 cooccur 层（仅同句共现，类型标『未定』，交人工/LLM 定型）。"
                "配对召回的物理上界 = 金标准两端在原文同句共现的比例；"
                f"cooccur 层按无向配对计的召回 / 上界 = {recall_unord/max(1e-9,ceiling):.0%}。"
                "『未定』类型的候选不得直接入库——类型定型须经人工或 LLM（span 校验后）。",
        "by_rel": {rel: {"candidates": sum(1 for r in pattern_rows if r["rel_guess"].startswith(rel)),
                         "pair_hits": sum(1 for r in pattern_rows if r["rel_guess"].startswith(rel) and r["in_gold_pair"])}
                   for rel, _ in REL_PATTERNS if rel != "未定"},
    }
    with io.open(os.path.join(S05, "关系抽取", "抽取评测.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(evalj, f, ensure_ascii=False, indent=2)

    # ---------- 2b) 零覆盖语料的结构化候选（只进候选池，不写概念表） ----------
    item_docs = {r["source_doc"].split(";")[0].strip() for r in
                 rd("概念表.csv", S01) + rd("命题表.csv", S01) + rd("论证表.csv", S01)}
    corpus_docs = rd("语料清单.csv", S00)
    zero_docs = [d for d in corpus_docs if d["doc_id"] not in item_docs]
    cov_rows = []
    for d in zero_docs:
        sents_d = [x for x in sents if x["doc_id"] == d["doc_id"]]
        if not sents_d:
            continue
        text = "\n".join(x["text"] for x in sents_d)
        cands_d, _ = discover_terms(text, min_freq=3, min_pmi=6.0, min_entropy=0.8, top_n=40)
        cv_d = c_value(cands_d, {g: c["freq"] for g, c in cands_d.items()})
        for g, c in sorted(cands_d.items(), key=lambda kv: -cv_d.get(kv[0], 0))[:40]:
            ex = next((x["text"] for x in sents_d if g in x["text"]), "")
            cov_rows.append({"doc_id": d["doc_id"], "doc_title": d["title"], "term": g,
                             "freq": c["freq"], "pmi": c["pmi"], "boundary_entropy": c["entropy"],
                             "c_value": cv_d.get(g, 0), "example_sentence": ex[:150],
                             "status": "候选待核（未覆盖语料）"})
    if cov_rows:
        wcsv(os.path.join(S05, "术语候选", "零覆盖语料候选.csv"), cov_rows)
    term_stat["zero_cover_docs"] = len(zero_docs)
    term_stat["zero_cover_candidates"] = len(cov_rows)
    with io.open(os.path.join(S05, "术语候选", "术语候选统计.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(term_stat, f, ensure_ascii=False, indent=2)

    # ---------- 3) 语义特征（语料自训练 TF-IDF） ----------
    ev = {}
    for r in rd("证据映射.csv", S00):
        ev[r["struct_id"]] = r
    docs = {}
    for c in concepts:
        r = ev.get(c["concept_id"], {})
        docs[c["concept_id"]] = f'{c["name"]} {c["definition"]} {r.get("quote_clean", "")}'
    tok = {k: [t for t in (jieba.lcut(v) if jieba else v.split())
               if TERM_OK.match(t) and t not in STOP] for k, v in docs.items()}
    df = Counter()
    for k, ts in tok.items():
        for t in set(ts):
            df[t] += 1
    N = len(tok)
    vec = {}
    for k, ts in tok.items():
        tf = Counter(ts)
        v = {}
        for t, c in tf.items():
            if df[t] < 2:
                continue
            w = (1 + math.log(c)) * math.log(1 + N / df[t])
            v[t] = round(w, 4)
        nrm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vec[k] = {t: round(x / nrm, 5) for t, x in v.items()}
    long_rows = [{"concept_id": k, "term": t, "weight": w}
                 for k, v in sorted(vec.items()) for t, w in sorted(v.items(), key=lambda x: -x[1])[:40]]
    wcsv(os.path.join(S05, "嵌入就绪", "语义特征.csv"), long_rows)
    near = []
    ids = sorted(vec)
    for a in ids:
        sims = sorted(((sum(x * vec[b].get(t, 0.0) for t, x in vec[a].items()), b) for b in ids if b != a),
                      reverse=True)[:8]
        near.append({"concept_id": a, "name": next(c["name"] for c in concepts if c["concept_id"] == a),
                     "neighbors": ";".join(f"{b}:{s:.2f}" for s, b in sims)})
    wcsv(os.path.join(S05, "嵌入就绪", "语义近邻.csv"), near)

    print(f"[OK] 术语候选 {len(rows)}/{n_all}（新候选 {len(new_rows)}）| 零覆盖语料 {len(zero_docs)} 篇 → 候选 {len(cov_rows)}")
    print(f"     关系候选 {len(dedup)}（pattern {len(pattern_rows)} / cooccur {len(dedup)-len(pattern_rows)}）"
          f" | 配对 P={precision:.2f} R={recall:.2f} / 无向R={recall_unord:.2f}"
          f" | 上界={ceiling:.2f} 达上界={evalj['recall_vs_ceiling']:.0%}"
          f" | 类型命中率={evalj['relation_type_accuracy']:.2f}")
    print("     术语样例（新）:", "、".join(term_stat["top_new"][:12]))
    print("     语义特征词项:", len(long_rows), "| 近邻表:", len(near))
    print("     语义近邻样例:", near[0]["name"], "→", near[0]["neighbors"][:60])


if __name__ == "__main__":
    main()
