# -*- coding: utf-8 -*-
"""
维度 2 · LLM 结构化定型（OntoGPT/SPIRES 风格 · 就绪管线）

定位：`build_extract.py` 的 cooccur 层候选只有「两端同句共现、类型未定」；
本脚本用 **schema 约束的 LLM 提示** 给候选定关系类型与方向，属于 v1.7.0 计划的
"LLM 结构化提示，攻关系抽取类型上界"一环。

三条硬约束（与红线一致）：
  1. 输出 schema 固定 —— relation 只允许既有 6 类 + 未定；不引入理论外语义；
  2. **span 校验** —— 模型必须返回 `rationale_quote`（原文片段），程序要求其
     **逐字出现在候选句中**，否则该条丢弃（不采信无 span 的输出）；
  3. 结果只写 `LLM定型候选.csv` **候选文件**，不进入概念表/论证表，须人工确认。

运行环境（OpenAI 兼容 API）：
  set CQM_LLM_API_BASE=https://api.example.com/v1/chat/completions
  set CQM_LLM_API_KEY=sk-...
  set CQM_LLM_MODEL=...
  python llm_extract.py            # 可选 CQM_LLM_MAXN 限制条数（默认 60）

**未配置环境变量时：打印就绪说明并退出 0**（不谎报执行）。
"""
import csv
import io
import json
import os
import re
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S05 = os.path.join(ROOT, "05_机器学习数据准备")

RELATIONS = ["重组实现", "演化", "映射", "等价", "依赖", "层级含于", "未定"]
SCHEMA = """{"relation": "<%s>", "direction": "as_is|reversed|unsure", "rationale_quote": "<原文片段，逐字≤60字>"}""" % "|".join(RELATIONS)

PROMPT = """你是理论文本结构化助手。给定一条「句子」与其中出现的两个概念 A/B，判断它们的关系。
只允许取值：""" + "/".join(RELATIONS[:6]) + """ 或 未定（原文无显式关系时）。
direction 表示 A/B 方向：as_is（A→B 正确）/ reversed（应为 B→A）/ unsure。
rationale_quote 必须是**句子中逐字出现**的片段（≤60 字），用以支撑判断。
只输出一个 JSON 对象，不要任何解释、不要代码围栏。

句子：{sentence}
概念 A：{a}（{aid}）
概念 B：{b}（{bid}）
JSON："""


def rd(name):
    with io.open(os.path.join(S05, "关系抽取", name), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def wcsv(name, rows):
    if not rows:
        print("[WARN] 无输出行")
        return
    with io.open(os.path.join(S05, "关系抽取", name), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)


def call_llm(base, key, model, prompt):
    data = json.dumps({"model": model, "temperature": 0,
                       "messages": [{"role": "user", "content": prompt}]}).encode("utf-8")
    req = urllib.request.Request(base, data=data, headers={
        "Content-Type": "application/json", "Authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=90) as resp:
        out = json.loads(resp.read().decode("utf-8"))
    return out["choices"][0]["message"]["content"]


def parse_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def main():
    base = os.environ.get("CQM_LLM_API_BASE", "").strip()
    key = os.environ.get("CQM_LLM_API_KEY", "").strip()
    model = os.environ.get("CQM_LLM_MODEL", "unknown").strip()
    if not base or not key:
        print("[就绪] llm_extract.py 未配置 CQM_LLM_API_BASE / CQM_LLM_API_KEY，跳过执行（不谎报为已完成）。")
        print("       输入就绪：05_机器学习数据准备/关系抽取/候选关系.csv 中 cooccur 层类型未定的候选")
        print("       输出目标：05_机器学习数据准备/关系抽取/LLM定型候选.csv（候选，不入表）")
        print("       约束：schema 固定 6+1 类 · rationale_quote 须逐字命中候选句（span 校验，不采信无 span 输出）")
        return 0
    if not base.endswith("chat/completions"):
        base = base.rstrip("/") + "/v1/chat/completions" if "/v1/" not in base else base.rstrip("/")

    rows = rd("候选关系.csv")
    pending = [r for r in rows if "未定" in (r.get("rel_guess") or "")]
    if not pending:
        pending = rows
    maxn = int(os.environ.get("CQM_LLM_MAXN", "60"))
    pending = pending[:maxn]

    # 概念 id → 名称（从知识图谱）
    kg = json.load(io.open(os.path.join(ROOT, "03_超图与理论图", "知识图谱.json"), encoding="utf-8"))
    name_by_id = {n["id"]: n.get("label", n["id"]) for n in kg["nodes"]}

    out, ok_span, ok_rel = [], 0, 0
    for i, r in enumerate(pending, 1):
        a, b = name_by_id.get(r["src"], r["src"]), name_by_id.get(r["dst"], r["dst"])
        prompt = PROMPT.format(sentence=r["sentence"], a=a, aid=r["src"], b=b, bid=r["dst"])
        try:
            raw = call_llm(base, key, model, prompt)
        except Exception as e:
            out.append({**r, "llm_relation": "", "llm_quote": "", "span_ok": False,
                        "llm_status": "api_error:" + str(e)[:80]})
            continue
        j = parse_json(raw) or {}
        rel = (j.get("relation") or "").strip()
        quote = (j.get("rationale_quote") or "").strip()
        direction = (j.get("direction") or "unsure").strip()
        span_ok = bool(quote) and quote in r["sentence"]
        rel_ok = rel in RELATIONS
        ok_span += bool(span_ok)
        ok_rel += bool(rel_ok and rel != "未定")
        status = "accepted" if (span_ok and rel_ok and rel != "未定") else (
            "span_fail" if not span_ok else ("rel_fail" if not rel_ok else "未定"))
        src, dst = r["src"], r["dst"]
        if direction == "reversed":
            src, dst = dst, src
        out.append({**r, "llm_relation": rel, "llm_direction": direction,
                    "llm_quote": quote[:120], "span_ok": span_ok,
                    "final_src": src, "final_dst": dst, "llm_status": status})
        if i % 10 == 0:
            print(f"  … {i}/{len(pending)}")

    wcsv("LLM定型候选.csv", out)
    accepted = [r for r in out if r["llm_status"] == "accepted"]
    gold_pairs = {(r["src"], r["dst"]) for r in rows if r.get("in_gold_pair") == "True"}
    hits = sum(1 for r in accepted if (r["final_src"], r["final_dst"]) in gold_pairs)
    stat = {"requested": len(pending), "span_ok": ok_span, "typed_non_未定": ok_rel,
            "accepted": len(accepted),
            "accepted_hits_on_gold_pairs": hits,
            "note": "span_ok = rationale_quote 逐字命中候选句；accepted = span+schema 双通过且类型非未定。"
                    "输出仅为候选（LLM定型候选.csv），须人工确认后才可影响论证表；无密钥时本脚本跳过并登记为就绪。"}
    with io.open(os.path.join(S05, "关系抽取", "LLM定型统计.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(stat, f, ensure_ascii=False, indent=2)
    print(f"[OK] LLM 定型 {len(pending)} 条 → accepted {len(accepted)}（span 通过 {ok_span}，类型定出 {ok_rel}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
