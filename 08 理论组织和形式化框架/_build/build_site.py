# -*- coding: utf-8 -*-
"""
维度7（核心） · 展示可视化
生成自包含（离线可用、无 CDN 依赖）的 HTML 网站与交互式超图，并汇总数据快照。

产物：
  10_展示可视化/源_可视化/研究驾驶舱/index.html —— 研究驾驶舱（暗色；KPI + 8 类内联 SVG 图表 + 明细表）
  10_展示可视化/源_可视化/研究驾驶舱/data.json  —— 同一份数据快照（供下载/二次开发）
  10_展示可视化/交互式可视化/超图交互.html —— 交互式有向超图（Cytoscape.js：类型分簇等 6 布局、
                                           邻域聚焦、路径检索、派生级联回放、小地图、导出 PNG）
  03_超图与理论图/超图可视化.html          —— 同上（同步副本）
  04_Lean对接/蓝图/index.html               —— 由 build_lean.py 生成的蓝图（唯一一份）

交互式超图由 Cytoscape.js 渲染；库文件随包离线放置于 `_build/vendor/cytoscape.min.js`（MIT），
构建时复制到两个产物的 `assets/` 下，页面不引用任何 CDN。

呈现边界：本脚本只**呈现**既有数据（源 CSV / 超图 JSON / 派生仿真 / Lean 结构提取），
不新增理论内容、不改数值、不改缺口状态。派生级联回放的数据取自
`06_动态机制/仿真/derivation_order.csv`（49 条规则 / 4 轮），逐轮新增与累计可达在构建期复算并断言。

运行：python build_site.py
"""
import collections
import csv
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S01 = os.path.join(ROOT, "01_结构化数据")
S00 = os.path.join(ROOT, "00_外部引用")
S03 = os.path.join(ROOT, "03_超图与理论图")
S04 = os.path.join(ROOT, "04_Lean对接")
S05 = os.path.join(ROOT, "05_机器学习数据准备")
S06 = os.path.join(ROOT, "06_动态机制")
S07 = os.path.join(ROOT, "07_经验检验")
S10 = os.path.join(ROOT, "10_展示可视化")
VENDOR = os.path.join(ROOT, "_build", "vendor")


def rd(p, enc="utf-8-sig"):
    with open(p, "r", encoding=enc, newline="") as f:
        return list(csv.DictReader(f))


def jload(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def build_cascade(seeds, rows):
    """按派生轨迹复算逐轮新增/累计，返回级联快照（构建期断言与源仿真一致）。"""
    active = set(seeds)
    steps = []
    for s in sorted({int(r["step"]) for r in rows}):
        cur = [r for r in rows if int(r["step"]) == s]
        new = []
        for r in cur:
            cid = r["rhs"]
            if cid not in active:
                active.add(cid)
                new.append(cid)
        steps.append({
            "step": s,
            "rules": [{"order": int(r["order"]), "step": s, "rule": r["rule_id"], "rel": r["relation"],
                       "rhs": r["rhs"], "rhs_name": r["rhs_name"],
                       "lhs": [x for x in r["lhs"].split(";") if x]} for r in cur],
            "new": new,
            "cum": len(active),
        })
    return steps, sorted(active)


def build_data():
    concepts = rd(os.path.join(S01, "概念表.csv"))
    props = rd(os.path.join(S01, "命题表.csv"))
    args = rd(os.path.join(S01, "论证表.csv"))
    hg = jload(os.path.join(S03, "超图数据.json"))
    lean_map = rd(os.path.join(S04, "Lean↔概念映射.csv"))
    modules = rd(os.path.join(S04, "Lean结构提取", "模块清单.csv"))
    dyn = jload(os.path.join(S06, "仿真", "dynamic_hypergraph.json"))["dynamics"]
    caus = jload(os.path.join(S07, "因果模型", "GN_causal_dag.json"))
    onto = jload(os.path.join(ROOT, "02_概念本体", "本体统计.json"))

    # 派生级联（49 条规则 / 4 轮，逐轮复算）
    trace = rd(os.path.join(S06, "仿真", "derivation_order.csv"))
    cascade, reached = build_cascade(dyn["seed_concepts"], trace)
    assert cascade[-1]["cum"] == dyn["reachable_concepts"], "级联累计可达与 06 仿真不一致"

    # 证据层 / 主张图 / 质量报告
    ev = jload(os.path.join(S00, "证据映射.json"))["evidence"]
    EVK = ("struct_id", "kind", "name", "doc_id", "evidence_doc", "sec_title", "char_start", "char_end",
           "quote_clean", "match_method", "confidence", "score", "verified", "review_verdict", "reviewer",
           "doc_switch", "loc_status")
    ev_slim = [{k: r.get(k, "") for k in EVK} for r in ev]
    kg = jload(os.path.join(S03, "知识图谱.json"))
    evmap = {r["struct_id"]: r for r in ev_slim}
    kg_nodes_enriched = []
    for n in kg["nodes"]:
        if n["kind"] == "concept":
            continue
        e = evmap.get(n["id"], {})
        m = dict(n)
        m["ev"] = {k: e.get(k, "") for k in ("quote_clean", "match_method", "confidence",
                                             "evidence_doc", "char_start", "char_end", "sec_title")}
        kg_nodes_enriched.append(m)
    claim_ok = [e for e in kg["edges"]
                if e["kind"] == "claim" and e["src"] and e["dst"]
                and e["src"][0] in {x["id"] for x in kg["nodes"]}
                and e["dst"][0] in {x["id"] for x in kg["nodes"]}]
    qrep = jload(os.path.join(ROOT, "02_概念本体", "本体校验报告.json"))
    ext = jload(os.path.join(S05, "关系抽取", "抽取评测.json"))
    tstat = jload(os.path.join(S05, "术语候选", "术语候选统计.json"))
    gap_dep = rd(os.path.join(S01, "缺口依赖.csv"))
    claim_rows = rd(os.path.join(S01, "命题依赖.csv"))
    quality = {
        "shacl": qrep["shacl"], "rdf": qrep["rdf"],
        "extract": ext, "terms": tstat,
        "reasoner": onto.get("reasoner", {}),
        "ontology": {k: onto.get(k, 0) for k in ("owl_classes", "owl_individuals", "owl_object_properties",
                                                 "owl_annotation_properties", "owl_restrictions",
                                                 "owl_disjoint_type_classes")},
        "gap_dep_edges": len(gap_dep),
        "claim_hist": dict(collections.Counter(r["relation"] for r in claim_rows)),
        "alias_count": len(rd(os.path.join(S01, "概念别名表.csv"))),
        "align": {"args": len(rd(os.path.join(S01, "论证对齐.csv"))),
                  "count_ok": sum(1 for r in rd(os.path.join(S01, "论证对齐.csv")) if r["count_ok"] == "True")},
    }

    # Lean 声明构成（按 kind 聚合，避免内嵌 1388 条明细）
    decls = jload(os.path.join(S04, "Lean结构提取", "declarations.json"))
    kind_hist = collections.Counter(d["kind"] for d in decls)
    mod_kind = collections.Counter((d["module"], d["kind"]) for d in decls)
    by_mod = collections.defaultdict(dict)
    for (m, k), n in mod_kind.items():
        by_mod[m][k] = n
    top_mods = sorted(by_mod.items(), key=lambda kv: -sum(kv[1].values()))[:16]

    # 概念派生深度（取自级联复算：种子 0，其余按首次出现轮次）
    depth = {c: 0 for c in dyn["seed_concepts"]}
    for st in cascade:
        for cid in st["new"]:
            depth.setdefault(cid, st["step"])

    return {
        "concepts": concepts, "props": props, "args": args, "hypergraph": hg,
        "lean_map": lean_map, "lean_modules": modules, "dynamics": dyn,
        "elasticity": caus["elasticity"], "scm": caus, "ontology": onto,
        "cascade": cascade, "trace": trace,
        "evidence": ev_slim, "quality": quality,
        "kg_stats": kg["stats"],
        "kg_nodes": kg_nodes_enriched,
        "claim_edges": claim_ok,
        "lean_kinds": dict(kind_hist),
        "lean_top_modules": [{"module": m, "total": sum(k.values()), "kinds": k} for m, k in top_mods],
        "depth": depth,
        "meta": {"nodes": len(concepts), "props": len(props), "args": len(args),
                 "hyperedges": len(hg["hyperedges"]), "edges": len(hg["directed_edges"]),
                 "modules": len(modules), "decls": len(decls),
                 "reached": len(reached), "unreachable": dyn["unreachable_concepts"],
                 "rules_fired": len(trace), "steps": dyn["steps"],
                 "rel_hist": hg["metadata"]["relation_type_histogram"]},
    }


def write_site(data):
    d = os.path.join(S10, "源_可视化", "研究驾驶舱")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    html = SITE_HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def write_hypergraph(data):
    payload = {"hg": data["hypergraph"], "cascade": data["cascade"],
               "dynamics": data["dynamics"], "depth": data["depth"],
               "kg": {"nodes": data["kg_nodes"], "edges": data["claim_edges"]},
               "scm": {"elasticity": data["elasticity"], "caveat": data["scm"]["caveat"]}}
    html = HYPER_HTML.replace("__DATA__", json.dumps(payload, ensure_ascii=False))
    lib = os.path.join(VENDOR, "cytoscape.min.js")
    for path in [os.path.join(S10, "源_可视化", "超图交互.html")]:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        adir = os.path.join(os.path.dirname(path), "assets")
        os.makedirs(adir, exist_ok=True)
        shutil.copyfile(lib, os.path.join(adir, "cytoscape.min.js"))


def write_blueprint_copy():
    """蓝图唯一一份在 `04_Lean对接/蓝图/`（由 build_lean.py 生成），此处不再同步副本，
    仅保留官方工具链说明文件。"""
    d = os.path.join(S04, "蓝图")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "leanblueprint_source.md"), "w", encoding="utf-8") as f:
        f.write("""# leanblueprint 源文件说明

本目录的 `index.html` 为交互式蓝图（由 `_build/build_lean.py` 生成，离线自包含）。

若改用 leanblueprint 官方工具链，目录应含：

```text
10_展示可视化/蓝图/
├── content.tex      # 蓝图正文，节点用 \\lean{{...}} / \\uses{{...}} 标注
├── web.tex          # \\documentclass{{report}} + \\usepackage{{blueprint}} ...
├── plastex.cfg
└── blueprint/src/   # \\lean{{...}} 指向的 Lean 源码（软链或拷贝 08 理论组织和形式化框架/04_Lean对接/Lean源码/）
```

生成：`leanblueprint web`（需 `pip install leanblueprint` + `plasTeX`）。

> 与 `04_Lean对接/蓝图/蓝图.md` 的分工：后者是 Lean↔概念↔缺口的对照源，本目录是其面向读者的 HTML 呈现。
""")


def main():
    data = build_data()
    write_site(data)
    write_hypergraph(data)
    write_blueprint_copy()
    print("[OK] 源_可视化/研究驾驶舱/index.html(+data.json), 源_可视化/超图交互.html(+cytoscape)")
    print("     meta:", data["meta"])
    print("     cascade:", [(c["step"], len(c["rules"]), len(c["new"]), c["cum"]) for c in data["cascade"]])


# ============================ 主站 HTML（研究驾驶舱） ============================
SITE_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CQM 组织层 · 研究驾驶舱</title>
<style>
:root{--bg:#070b12;--bg2:#0b1220;--panel:rgba(255,255,255,.035);--line:rgba(255,255,255,.09);
--ink:#e6eef8;--mut:#8ea0b8;--acc:#38bdf8;--acc2:#a78bfa;--ok:#34d399;--warn:#fbbf24;--gap:#f87171;--hy:#f59e0b}
*{box-sizing:border-box}
html,body{margin:0;height:100%}
body{color:var(--ink);font:13.5px/1.7 "Microsoft YaHei",system-ui,-apple-system,sans-serif;
background:radial-gradient(1200px 620px at 10% -12%,rgba(56,189,248,.12),transparent 62%),
radial-gradient(900px 520px at 100% 0%,rgba(167,139,250,.12),transparent 58%),var(--bg);}
.app{display:flex;min-height:100vh}
aside{width:212px;flex:0 0 212px;border-right:1px solid var(--line);padding:18px 14px;
background:linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.01));position:sticky;top:0;height:100vh;overflow:auto}
.brand{font-size:14.5px;font-weight:700;letter-spacing:.3px}
.brand span{display:block;font-weight:400;color:var(--mut);font-size:11.5px;letter-spacing:0;margin-top:3px}
nav{display:flex;flex-direction:column;gap:3px;margin-top:18px}
nav button{border:0;background:none;text-align:left;padding:8px 11px;border-radius:9px;font:inherit;color:var(--mut);cursor:pointer;
display:flex;justify-content:space-between;gap:8px;transition:.15s}
nav button:hover{background:rgba(255,255,255,.05);color:var(--ink)}
nav button.on{background:linear-gradient(90deg,rgba(56,189,248,.20),rgba(167,139,250,.12));color:#fff;box-shadow:inset 0 0 0 1px rgba(56,189,248,.35)}
nav button em{font-style:normal;color:var(--mut);font-size:11.5px}
.sidefoot{margin-top:20px;color:var(--mut);font-size:11px;line-height:1.6;border-top:1px solid var(--line);padding-top:12px}
.main{flex:1;min-width:0;display:flex;flex-direction:column}
.top{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:14px;padding:12px 22px;
background:rgba(7,11,18,.82);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.crumb{font-size:15px;font-weight:600}
.crumb small{display:block;font-weight:400;color:var(--mut);font-size:11.5px}
.gsearch{margin-left:auto;position:relative;width:min(420px,46vw)}
.gsearch input{width:100%;padding:8px 12px;border-radius:9px;border:1px solid var(--line);
background:rgba(255,255,255,.05);color:var(--ink);font:inherit;outline:none}
.gsearch input:focus{border-color:rgba(56,189,248,.6);box-shadow:0 0 0 3px rgba(56,189,248,.12)}
.gres{position:absolute;top:41px;left:0;right:0;max-height:52vh;overflow:auto;background:#0d1421;border:1px solid var(--line);
border-radius:11px;box-shadow:0 18px 40px rgba(0,0,0,.55);display:none}
.gres.on{display:block}
.gres a{display:block;padding:8px 12px;border-bottom:1px solid rgba(255,255,255,.05);color:var(--ink);text-decoration:none}
.gres a:hover{background:rgba(56,189,248,.10)}
.gres a i{font-style:normal;color:var(--acc);font-family:Consolas,monospace;font-size:11.5px;margin-right:7px}
.gres a u{text-decoration:none;color:var(--mut);font-size:11.5px;margin-left:6px}
.gres .empty{padding:10px 12px;color:var(--mut)}
main{padding:20px 22px 80px;max-width:1320px;width:100%}
section{display:none}section.on{display:block}
h2{font-size:14px;color:#cfe2f6;margin:22px 0 10px;font-weight:600;display:flex;align-items:center;gap:8px}
h2:first-child{margin-top:4px}
h2::before{content:"";width:3px;height:13px;border-radius:2px;background:linear-gradient(180deg,var(--acc),var(--acc2))}
.grid{display:grid;gap:14px;align-items:start}
.g2{grid-template-columns:repeat(auto-fit,minmax(330px,1fr))}
.g3{grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px}
.kpi{background:linear-gradient(180deg,rgba(255,255,255,.058),rgba(255,255,255,.018));border:1px solid var(--line);
border-radius:14px;padding:12px 14px;box-shadow:0 10px 26px rgba(0,0,0,.28)}
.kpi b{display:block;font-size:25px;line-height:1.15;font-variant-numeric:tabular-nums;color:#8ed0ff;
text-shadow:0 0 16px rgba(56,189,248,.35)}
.kpi span{color:var(--mut);font-size:11.5px}
.card{background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.015));border:1px solid var(--line);
border-radius:14px;padding:13px 15px;box-shadow:0 10px 26px rgba(0,0,0,.26)}
.card h3{margin:0 0 10px;font-size:12.5px;color:#bcd3ea;font-weight:600;display:flex;justify-content:space-between;align-items:baseline}
.card h3 em{font-style:normal;color:var(--mut);font-size:11px}
.legend{display:flex;flex-wrap:wrap;gap:5px 12px;margin-top:9px;font-size:11.5px;color:var(--mut)}
.legend i{display:inline-block;width:9px;height:9px;border-radius:3px;margin-right:5px;vertical-align:middle}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th,td{padding:6px 9px;border-bottom:1px solid rgba(255,255,255,.06);text-align:left;vertical-align:top}
th{background:rgba(255,255,255,.05);color:#b9cde3;position:sticky;top:0;font-weight:600;z-index:1;backdrop-filter:blur(6px);white-space:nowrap}
tbody tr:hover td{background:rgba(56,189,248,.06)}
code{background:rgba(255,255,255,.08);padding:1px 5px;border-radius:4px;font-family:Consolas,monospace;font-size:11.5px}
.tag{display:inline-block;padding:1px 7px;border-radius:9px;font-size:11px;margin:1px;white-space:nowrap;
background:rgba(255,255,255,.07);color:var(--mut)}
.t-ok{background:rgba(52,211,153,.16);color:#6ee7b7}
.t-gap{background:rgba(248,113,113,.16);color:#fca5a5}
.t-ax{background:rgba(251,191,36,.16);color:#fcd34d}
.t-hy{background:rgba(245,158,11,.18);color:#fbd38d}
.t-d0{background:rgba(56,189,248,.18);color:#7dd3fc}
.t-d1{background:rgba(167,139,250,.16);color:#c4b5fd}
.t-d2{background:rgba(244,114,182,.16);color:#f9a8d4}
.t-d3{background:rgba(52,211,153,.16);color:#6ee7b7}
.t-d4{background:rgba(251,191,36,.16);color:#fcd34d}
.tbx{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;align-items:center}
.tbx input,.tbx select{padding:6px 10px;border-radius:8px;border:1px solid var(--line);background:rgba(255,255,255,.05);
color:var(--ink);font:inherit;outline:none}
.tbx input:focus,.tbx select:focus{border-color:rgba(56,189,248,.55)}
.tbx .count{color:var(--mut);font-size:11.5px;margin-left:auto}
.scroll{max-height:64vh;overflow:auto;border:1px solid var(--line);border-radius:12px;background:rgba(255,255,255,.015)}
.hint{color:var(--mut);font-size:11.5px;margin:6px 0 12px}
a{color:var(--acc)}
svg{display:block;width:100%;height:auto;overflow:visible}
svg.w-sm{max-width:238px;margin:0 auto}
svg.w-md{max-width:330px;margin:0 auto}
.cl{fill:#9fb3c8;font-size:11px}
.cv{fill:#dbe7f3;font-size:11px;font-variant-numeric:tabular-nums}
.dt{fill:#eaf3ff;font-size:20px;font-weight:600;font-variant-numeric:tabular-nums}
.dl{fill:#8ea0b8;font-size:10.5px}
.cascade .csq{fill:rgba(56,189,248,.28);stroke:rgba(125,211,252,.55)}
.cascade text{font-size:10.5px;fill:#9fb3c8}
.cascade .cg{font-size:11px;fill:#dbe7f3;font-weight:600}
.rib{fill:rgba(167,139,250,.13)}
.chips{display:flex;flex-wrap:wrap;gap:5px}
.chip{background:rgba(248,113,113,.13);color:#fca5a5;border:1px solid rgba(248,113,113,.25);
border-radius:8px;padding:2px 8px;font-size:11.5px}
.chip.ax{background:rgba(251,191,36,.13);color:#fcd34d;border-color:rgba(251,191,36,.25)}
.note{border-left:3px solid var(--warn);background:rgba(251,191,36,.07);padding:7px 11px;border-radius:0 8px 8px 0;
color:#f3d99a;font-size:11.5px;margin-top:10px}
.links{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.links a{background:rgba(56,189,248,.10);border:1px solid rgba(56,189,248,.28);border-radius:9px;padding:6px 11px;
text-decoration:none;font-size:12px}
.links a:hover{background:rgba(56,189,248,.2)}
</style></head>
<body>
<div class="app">
<aside>
  <div class="brand">CQM 组织层<span>理论组织与形式化框架 · 08</span></div>
  <nav id="nav"></nav>
  <div class="sidefoot">
    离线自包含 · 无 CDN<br>
    数据快照 <span id="snap">—</span><br>
    源 CSV 为唯一源，本页为派生呈现
  </div>
</aside>
<div class="main">
  <div class="top">
    <div class="crumb" id="crumb">总览<small id="crumbsub"></small></div>
    <div class="gsearch">
      <input id="gq" placeholder="全局检索：概念 / 命题 / 论证（Ctrl+K）" autocomplete="off">
      <div class="gres" id="gres"></div>
    </div>
  </div>
  <main id="views"></main>
</div>
</div>
<script>
const D=__DATA__;
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const el=id=>document.getElementById(id);
const TYPE_COLOR={'本体论':'#f0916a','理论框架':'#c39bf5','数学结构':'#6aa9f0','群论':'#4fd1a5','关系类型':'#9aa6b2',
 '引力层级':'#e3c05a','纤维丛':'#a08cf0','几何':'#4fc4d6','量纲':'#e0845f','数论':'#4fd07a','物理':'#5b95e8','共形场论':'#e070b0'};
const REL_COLOR={'重组实现':'#f59e0b','映射':'#38bdf8','演化':'#a78bfa','等价':'#34d399','依赖':'#f472b6','层级含于':'#facc15'};
const KIND_COLOR={theorem:'#38bdf8',lemma:'#7dd3fc',def:'#a78bfa',structure:'#f472b6',axiom:'#f87171',
 inductive:'#34d399',class:'#fbbf24',abbrev:'#94a3b8'};
const STATUS_GROUP=s=>/未闭合|待证明|待.*复现/.test(s)?'未闭合/待证':(/闭合|已证明/.test(s)?'闭合':(/axiom/.test(s)?'axiom':(/占位|部分/.test(s)?'部分/占位':'已陈述')));
const ST_COLOR={'已陈述':'#38bdf8','未闭合/待证':'#f87171','闭合':'#34d399','axiom':'#fbbf24','部分/占位':'#a78bfa'};
/* ---------- 内联 SVG 图表工具（无外部依赖） ---------- */
function svg(w,h,inner,cls){return '<svg class="'+(cls||'')+'" viewBox="0 0 '+w+' '+h+'" preserveAspectRatio="xMidYMid meet">'+inner+'</svg>';}
function donut(items,opt){opt=opt||{};const S=opt.size||196,R=S/2-8,r=R*.615,cx=S/2,cy=S/2;
  const tot=items.reduce((a,b)=>a+b.value,0)||1;let a=-Math.PI/2,s='';
  const P=(rad,ang)=>[cx+rad*Math.cos(ang),cy+rad*Math.sin(ang)];
  items.forEach(it=>{const a2=a+it.value/tot*Math.PI*2,lg=(a2-a)>Math.PI?1:0;
    const[x1,y1]=P(R,a),[x2,y2]=P(R,a2),[x3,y3]=P(r,a2),[x4,y4]=P(r,a);
    s+='<path d="M'+x1+' '+y1+'A'+R+' '+R+' 0 '+lg+' 1 '+x2+' '+y2+'L'+x3+' '+y3+'A'+r+' '+r+' 0 '+lg+' 0 '+x4+' '+y4+'Z" fill="'+it.color+'" fill-opacity=".92" stroke="#0b1220" stroke-width="1.5"><title>'+esc(it.label)+'：'+it.value+'</title></path>';
    a=a2;});
  s+='<text x="'+cx+'" y="'+(cy+2)+'" text-anchor="middle" class="dt">'+tot+'</text>';
  s+='<text x="'+cx+'" y="'+(cy+20)+'" text-anchor="middle" class="dl">'+esc(opt.label||'')+'</text>';
  return svg(S,S,s,opt.cls);}
function hbars(items,opt){opt=opt||{};const W=opt.w||470,LH=opt.lh||22,LW=opt.lw||104,G=6;
  const max=Math.max(1,...items.map(d=>d.value)),H=items.length*(LH+G)+6;let s='';
  items.forEach((d,i)=>{const y=i*(LH+G)+3,bw=Math.max(2,(W-LW-52)*d.value/max);
    s+='<text x="'+(LW-8)+'" y="'+(y+LH*.72)+'" text-anchor="end" class="cl">'+esc(d.label)+'</text>';
    s+='<rect x="'+LW+'" y="'+(y+3)+'" width="'+(W-LW-52)+'" height="'+(LH-7)+'" rx="3" fill="rgba(255,255,255,.05)"/>';
    s+='<rect x="'+LW+'" y="'+(y+3)+'" width="'+bw+'" height="'+(LH-7)+'" rx="3" fill="'+(d.color||opt.color||'#38bdf8')+'" fill-opacity=".9"><title>'+esc(d.label)+'：'+d.value+'</title></rect>';
    s+='<text x="'+(W-4)+'" y="'+(y+LH*.72)+'" text-anchor="end" class="cv">'+d.value+'</text>';});
  return svg(W,H,s);}
function stackbar(rows,opt){opt=opt||{};const W=opt.w||470,LH=26,G=9,H=rows.length*(LH+G)+24,LW=opt.lw||92;
  const max=Math.max(1,...rows.map(r=>r.parts.reduce((a,b)=>a+b.value,0)));let s='';
  const keys=opt.noKeys?[]:(opt.keys||[]);keys.forEach((k,i)=>{s+='<rect x="'+(LW+i*Math.min(96,(W-LW)/keys.length))+'" y="0" width="9" height="9" rx="2" fill="'+opt.colors[k]+'"/><text x="'+(LW+i*Math.min(96,(W-LW)/keys.length)+13)+'" y="9" class="cl">'+esc(k)+'</text>';});
  rows.forEach((r,i)=>{const y=i*(LH+G)+24,tot=r.parts.reduce((a,b)=>a+b.value,0)||1;let x=LW;
    s+='<text x="'+(LW-8)+'" y="'+(y+LH*.7)+'" text-anchor="end" class="cl">'+esc(r.label)+'</text>';
    const scale=(W-LW-58)/max;
    r.parts.forEach(p=>{const w=p.value*scale;if(w<=0)return;
      s+='<rect x="'+x+'" y="'+y+'" width="'+Math.max(w,1.5)+'" height="'+(LH-8)+'" rx="3" fill="'+opt.colors[p.label]+'" fill-opacity=".9"><title>'+esc(r.label)+' · '+esc(p.label)+'：'+p.value+'</title></rect>';x+=w;});
    s+='<text x="'+(W-4)+'" y="'+(y+LH*.7)+'" text-anchor="end" class="cv">'+tot+'</text>';});
  return svg(W,H,s);}
function cascade(seeds,steps,opt){opt=opt||{};const W=opt.w||470,H=opt.h||196,top=26,bot=26;
  const cols=[{t:'种子',n:seeds,rules:0,cum:seeds,color:'#22d3ee'}].concat(steps.map(s=>({t:'第'+s.step+'轮',n:s.new.length,rules:s.rules.length,cum:s.cum,color:'#a78bfa'})));
  const maxC=Math.max(...cols.map(c=>c.cum)),colW=42,avail=W-70,gap=avail/(cols.length-1),cx=i=>35+i*gap;let s='';
  const hOf=c=>Math.max(10,(H-top-bot)*c/maxC);
  cols.forEach((c,i)=>{const hh=hOf(c.cum),y0=top+(H-top-bot-hh)/2;
    s+='<rect x="'+(cx(i)-colW/2)+'" y="'+y0+'" width="'+colW+'" height="'+hh+'" rx="7" fill="'+c.color+'" fill-opacity=".18" stroke="'+c.color+'" stroke-opacity=".55"/>';
    s+='<text x="'+cx(i)+'" y="'+(y0+15)+'" text-anchor="middle" class="cg">'+c.cum+'</text>';
    s+='<text x="'+cx(i)+'" y="'+(H-8)+'" text-anchor="middle">'+c.t+'</text>';
    if(i) s+='<text x="'+cx(i)+'" y="'+(y0-8)+'" text-anchor="middle" class="cl">+'+(c.n)+'</text>';});
  for(let i=0;i<cols.length-1;i++){const h1=hOf(cols[i].cum),h2=hOf(cols[i+1].cum);
    const y1t=top+(H-top-bot-h1)/2,y1b=y1t+h1,y2t=top+(H-top-bot-h2)/2,y2b=y2t+h2,mid=(cx(i)+cx(i+1))/2;
    s+='<path class="rib" d="M'+cx(i)+' '+y1t+'C'+mid+' '+y1t+' '+mid+' '+y2t+' '+cx(i+1)+' '+y2t+'L'+cx(i+1)+' '+y2b+'C'+mid+' '+y2b+' '+mid+' '+y1b+' '+cx(i)+' '+y1b+'Z"/>';}
  return svg(W,H,s,'cascade');}
function logbars(items,opt){opt=opt||{};const W=opt.w||470,LH=24,G=7,LW=opt.lw||118,H=items.length*(LH+G)+6;
  const logs=items.map(d=>Math.log10(Math.max(Math.abs(d.value),1e-3)));
  const lo=Math.min(...logs),hi=Math.max(...logs,0);let s='';
  items.forEach((d,i)=>{const y=i*(LH+G)+3,L=(logs[i]-lo)/Math.max(hi-lo,1e-6),bw=Math.max(3,L*(W-LW-70));
    s+='<text x="'+(LW-8)+'" y="'+(y+LH*.72)+'" text-anchor="end" class="cl">'+esc(d.label)+'</text>';
    s+='<rect x="'+LW+'" y="'+(y+3)+'" width="'+(W-LW-70)+'" height="'+(LH-7)+'" rx="3" fill="rgba(255,255,255,.05)"/>';
    s+='<rect x="'+LW+'" y="'+(y+3)+'" width="'+bw+'" height="'+(LH-7)+'" rx="3" fill="'+(d.hot?'#f87171':'#38bdf8')+'" fill-opacity=".9"><title>'+esc(d.label)+'：'+d.value+'</title></rect>';
    s+='<text x="'+(W-4)+'" y="'+(y+LH*.72)+'" text-anchor="end" class="cv">'+(d.hot?'★ ':'')+d.value+'</text>';});
  return svg(W,H,s);}
/* ---------- 数据派生 ---------- */
const CN={};D.concepts.forEach(c=>CN[c.concept_id]=c);
const depth=D.depth||{};
const relHist=D.meta.rel_hist;
const typeCount=Object.entries(D.concepts.reduce((a,c)=>(a[c.type]=(a[c.type]||0)+1,a),{})).sort((a,b)=>b[1]-a[1]);
const VIEWS=[
 ['ov','总览','系统规模与七维度'],
 ['con','概念','82 个概念 · 类型 / 派生深度'],
 ['prop','命题与缺口','63 条命题 · 24 个缺口'],
 ['rel','关系与超边','19 超边 ⇒ · 51 有向边 →'],
 ['lean','Lean 对接','68 模块 · 1388 声明'],
 ['dyn','动态机制','49 条规则 · 4 轮派生'],
 ['ev','证据','215 条断言 → 原文定位'],
 ['qual','质量看板','SHACL · 本体推理 · 抽取评测'],
 ['meta','元数据','本体 / 快照 / 下载']];
/* ---------- 骨架 ---------- */
el('nav').innerHTML=VIEWS.map((v,i)=>'<button data-t="'+v[0]+'"'+(i?'':' class="on"')+'>'+v[1]+'<em>'+({'ov':D.meta.nodes,'con':D.meta.nodes,'prop':D.meta.props,'rel':D.meta.args,'lean':D.meta.decls,'dyn':D.meta.rules_fired,'ev':D.evidence.length,'qual':'✓','meta':''})[v[0]]+'</em></button>').join('');
function gov(){const v=el('views');v.innerHTML=VIEWS.map((x,i)=>'<section id="'+x[0]+'"'+(i?'':' class="on"')+'><div id="v_'+x[0]+'"></div></section>').join('');}
gov();
function activate(t,push){
  const btn=document.querySelector('#nav button[data-t="'+t+'"]');if(!btn)return;
  document.querySelectorAll('#nav button').forEach(x=>x.classList.remove('on'));btn.classList.add('on');
  document.querySelectorAll('section').forEach(x=>x.classList.remove('on'));el(t).classList.add('on');
  const v=VIEWS.find(x=>x[0]===t);el('crumb').innerHTML=v[1]+'<small>'+v[2]+'</small>';
  if(push!==false){try{history.replaceState(null,'','#'+t);}catch(e){}}
  window.scrollTo(0,0);
}
document.querySelectorAll('#nav button').forEach(b=>b.onclick=()=>activate(b.dataset.t));
const _init=(location.hash||'').replace('#','');
if(VIEWS.some(v=>v[0]===_init))activate(_init,false);
const V=id=>el('v_'+id);
/* ---------- 总览 ---------- */
{const m=D.meta,cs=D.cascade;
 V('ov').innerHTML=
 '<h2>系统规模</h2><div class="kpis">'+[['概念',m.nodes],['命题 / 缺口',m.props],['论证 / 关系',m.args],
  ['超边 ⇒',m.hyperedges],['有向边 →',m.edges],['Lean 声明',m.decls]].map(([k,v])=>'<div class="kpi"><b>'+v+'</b><span>'+k+'</span></div>').join('')+'</div>'
 +'<h2>分布与派生</h2><div class="grid g2">'
 +'<div class="card"><h3>概念类型分布<em>12 类 / '+m.nodes+'</em></h3>'+donut(typeCount.map(([t,n])=>({label:t,value:n,color:TYPE_COLOR[t]||'#888'})),{label:'概念'})
 +'<div class="legend">'+typeCount.map(([t,n])=>'<span><i style="background:'+(TYPE_COLOR[t]||'#888')+'"></i>'+esc(t)+' '+n+'</span>').join('')+'</div></div>'
 +'<div class="card"><h3>关系类型分布<em>19 + 51 = 70</em></h3>'+hbars(Object.entries(relHist).sort((a,b)=>b[1]-a[1]).map(([t,n])=>({label:t,value:n,color:REL_COLOR[t]||'#38bdf8'})),{lw:76})
 +'<div class="hint">⇒ 仅表重组实现（超边，多因一果）；其余为普通有向边 →。</div></div>'
 +'<div class="card"><h3>重写系统前向派生<em>'+m.rules_fired+' 规则 / '+m.steps+' 轮 · 可达 '+m.reached+'/'+m.nodes+'</em></h3>'+cascade(D.dynamics.seed_concepts.length,cs)
 +'<div class="hint">种子 '+D.dynamics.seed_concepts.length+' → 累计可达 <b>'+m.reached+'/'+m.nodes+'</b>；不可达 <code>'+m.unreachable.join('、')+'</code>（依赖自环或须理论外输入）。</div></div>'
 +'<div class="card"><h3>命题构成<em>6 类</em></h3>'+stackbar(
   Object.keys(D.props.reduce((a,p)=>(a[p.type]=1,a),{})).sort().map(t=>({label:t,parts:['已陈述','未闭合/待证','闭合','axiom','部分/占位'].map(g=>({label:g,value:D.props.filter(p=>p.type===t&&STATUS_GROUP(p.status)===g).length}))})),
   {keys:['已陈述','未闭合/待证','闭合','axiom','部分/占位'],colors:ST_COLOR,lw:64})
 +'<div class="hint">其中缺口 '+D.props.filter(p=>p.type==='缺口').length+' 条，编号与状态照录权威源（详见「命题与缺口」）。</div></div>'
 +'</div>'
 +'<h2>七维度</h2><div class="scroll"><table><thead><tr><th>#</th><th>维度</th><th>核心问题</th><th>目录</th><th>产物</th></tr></thead><tbody>'
 +[['1','结构化','理论由什么组成？','00–03','概念/命题/论证表、本体、超图'],
   ['2','ML 数据准备','机器如何读？','05','PyG/DGL 就绪、证明数据集 JSONL、嵌入就绪'],
   ['3','形式化验证','推理是否可靠？','04','Lean 结构提取、概念映射、蓝图'],
   ['4','动态机制','理论如何演化？','06','重写系统、状态模型、派生仿真'],
   ['5','经验检验','理论如何被检验？','07','因果模型、贝叶斯网络、实验设计'],
   ['6','元理论反思','本体论/认识论根基？','08','范畴论模型、类型论基础、哲学假设'],
   ['—','展示可视化','人如何看懂？','10','研究驾驶舱、交互超图、阅读站、讲解']]
   .map(r=>'<tr><td>'+r[0]+'</td><td><b>'+r[1]+'</b></td><td>'+r[2]+'</td><td><code>'+r[3]+'</code></td><td>'+r[4]+'</td></tr>').join('')
 +'</tbody></table></div>';}
/* ---------- 概念 ---------- */
{const types=['全部'].concat([...new Set(D.concepts.map(c=>c.type))].sort());
 const depths=['全部','0','1','2','3','4','未参与派生'];
 V('con').innerHTML='<h2>概念表</h2>'
 +'<div class="tbx"><input id="cq" placeholder="搜索名称 / 定义 / 编号…" style="min-width:230px">'
 +'<select id="ct">'+types.map(t=>'<option>'+esc(t)+'</option>').join('')+'</select>'
 +'<select id="cd">'+depths.map(t=>'<option>'+esc(t)+'</option>').join('')+'</select>'
 +'<span class="count" id="ccount"></span></div>'
 +'<div class="grid g2"><div class="scroll"><table><thead><tr><th>ID</th><th>名称</th><th>类型</th><th>派生深度</th><th>定义</th><th>出处</th></tr></thead><tbody id="ctb"></tbody></table></div>'
 +'<div><div class="card"><h3>类型分布</h3><div id="cdonut"></div></div>'
 +'<div class="card" style="margin-top:14px"><h3>派生深度分布<em>种子 + 4 轮</em></h3><div id="cdepth"></div>'
 +'<div class="hint">深度由 <code>06_动态机制/仿真/derivation_order.csv</code> 复算：种子 44，第 1–4 轮依次新增 28 / 6 / 2 / 1，累计 81/82。</div></div></div></div>';
 const depthHist=[0,1,2,3,4].map(d=>({label:'深度 '+d,value:D.concepts.filter(c=>depth[c.concept_id]===d).length,color:['#38bdf8','#a78bfa','#f472b6','#34d399','#fbbf24'][d]}));
 depthHist.push({label:'未参与派生',value:D.concepts.filter(c=>depth[c.concept_id]===undefined).length,color:'#64748b'});
 el('cdonut').innerHTML=donut(typeCount.map(([t,n])=>({label:t,value:n,color:TYPE_COLOR[t]||'#888'})),{size:180,label:'概念',cls:'w-sm'});
 el('cdepth').innerHTML=hbars(depthHist,{w:300,lw:82,lh:20,cls:'w-md'});
 function render(){
   const q=(el('cq').value||'').trim().toLowerCase(),t=el('ct').value,d=el('cd').value;
   const rows=D.concepts.filter(c=>{
     if(t!=='全部'&&c.type!==t)return false;
     if(d!=='全部'){const dd=depth[c.concept_id];if(d==='未参与派生'?dd!==undefined:String(dd)!==d)return false;}
     if(q&&!((c.name+' '+c.definition+' '+c.concept_id).toLowerCase().includes(q)))return false;
     return true;});
   el('ctb').innerHTML=rows.map(c=>{const dd=depth[c.concept_id];
     return '<tr><td><code>'+esc(c.concept_id)+'</code></td><td>'+esc(c.name)+'</td>'
     +'<td><span class="tag" style="background:'+(TYPE_COLOR[c.type]||'#888')+'26;color:'+(TYPE_COLOR[c.type]||'#888')+'">'+esc(c.type)+'</span></td>'
     +'<td>'+(dd===undefined?'<span class="tag">—</span>':'<span class="tag t-d'+dd+'">'+dd+'</span>')+'</td>'
     +'<td>'+esc(c.definition)+'</td><td>'+esc(c.source_doc)+' '+esc(c.source_loc)+'</td></tr>';}).join('');
   el('ccount').textContent='显示 '+rows.length+' / '+D.concepts.length;}
 ['cq','ct','cd'].forEach(i=>{el(i).oninput=render;el(i).onchange=render;});render();}
/* ---------- 命题与缺口 ---------- */
{const pt=['全部'].concat([...new Set(D.props.map(p=>p.type))].sort());
 V('prop').innerHTML='<h2>命题 / 定理 / 假设 / 构造 / 缺口</h2>'
 +'<div class="grid g2"><div class="card"><h3>类型 × 状态<em>63 条</em></h3><div id="pstack"></div></div>'
 +'<div class="card"><h3>缺口 24 条<em>状态原样保留</em></h3><div id="pgaps" class="chips"></div>'
 +'<div class="note">缺口编号与状态照录权威源（C / G2–G8 / G9–G22 / N1–N4 / H3.1–H3.3），不作升级。</div></div></div>'
 +'<div class="card" style="margin-top:14px"><h3>缺口依赖链 · 状态分组<em>数据化自命题表.depends_on 与 缺口依赖闭包.md §二</em></h3>'
 +'<div id="gchain"></div>'
 +'<div class="hint">已核对入图的前置边仅 <code>G2→G3→G4→G5</code>；其余依赖在闭包 .md 以表格/散文登记，未数据化者不推断、不补边。</div></div>'
 +'<h2>明细</h2><div class="tbx"><input id="pq" placeholder="搜索陈述 / 编号…" style="min-width:230px">'
 +'<select id="pt">'+pt.map(t=>'<option>'+esc(t)+'</option>').join('')+'</select>'
 +'<span class="count" id="pcount"></span></div>'
 +'<div class="scroll"><table><thead><tr><th>ID</th><th>陈述</th><th>类型</th><th>状态</th><th>出处</th><th>依赖</th></tr></thead><tbody id="ptb"></tbody></table></div>';
 const groups=['已陈述','未闭合/待证','闭合','axiom','部分/占位'];
 el('pstack').innerHTML=stackbar(pt.filter(t=>t!=='全部').map(t=>({label:t,parts:groups.map(g=>({label:g,value:D.props.filter(p=>p.type===t&&STATUS_GROUP(p.status)===g).length}))})),
   {keys:groups,colors:ST_COLOR,lw:64});
 el('pgaps').innerHTML=D.props.filter(p=>p.type==='缺口').map(p=>'<span class="chip'+(/axiom/.test(p.status)?' ax':'')+'" title="'+esc(p.statement)+'">'+esc(p.prop_id)+' · '+esc(p.status)+'</span>').join('');
  /* 缺口依赖链 SVG + 按编号系分组的状态色带 */
  {const N=D.kg_nodes.filter(n=>n.kind==='gap'),by={};N.forEach(n=>by[n.id]=n);
   const E=D.claim_edges.filter(e=>e.rel==='缺口前置'&&by[e.src[0]]&&by[e.dst[0]]);
   const stOf=n=>n.status||'';
   const hex=s=>s==='闭合'?'#34d399':(/占位/.test(s)?'#64748b':(/部分/.test(s)?'#fbbf24':(/未闭合|待证明/.test(s)?'#f87171':'#fbbf24')));
   let html='';
   if(E.length){
     const indeg={},lay={};
     N.forEach(n=>indeg[n.id]=0);E.forEach(e=>indeg[e.dst[0]]++);
     N.forEach(n=>{if(indeg[n.id]===0&&E.some(e=>e.src[0]===n.id))lay[n.id]=0;});
     let changed=true;
     while(changed){changed=false;E.forEach(e=>{const a=e.src[0],b=e.dst[0];
       if(lay[a]!==undefined&&(lay[b]===undefined||lay[b]<lay[a]+1)){lay[b]=lay[a]+1;changed=true;}});}
     const ord=N.filter(n=>lay[n.id]!==undefined).sort((a,b)=>lay[a.id]-lay[b.id]||(a.code<b.code?-1:1));
     const BW=118,BH=48,GAPx=58,H=BH+26,W=Math.max(1,ord.length)*(BW+GAPx)+16;
     let s='<svg viewBox="0 0 '+W+' '+H+'" style="max-width:'+W+'px">';
     const px={},py={};ord.forEach((n,i)=>{px[n.id]=16+i*(BW+GAPx);py[n.id]=13;});
     E.forEach(e=>{const a=e.src[0],b=e.dst[0];if(px[a]===undefined||px[b]===undefined||px[b]<=px[a])return;
       const x1=px[a]+BW,y1=py[a]+BH/2,x2=px[b],y2=py[b]+BH/2,mx=(x1+x2)/2;
       s+='<path d="M'+x1+' '+y1+'C'+mx+' '+y1+' '+mx+' '+y2+' '+x2+' '+y2+'" fill="none" stroke="#fbbf24" stroke-width="2.4"/>';
       s+='<path d="M'+x2+' '+y2+'l-9 -5.5v11z" fill="#fbbf24"/>';
       s+='<text x="'+mx+'" y="'+((y1+y2)/2-7)+'" text-anchor="middle" font-size="10.5" fill="#fcd34d">前置</text>';});
     ord.forEach(n=>{const c=hex(stOf(n));
       s+='<g><rect x="'+px[n.id]+'" y="'+py[n.id]+'" width="'+BW+'" height="'+BH+'" rx="9" fill="rgba(255,255,255,.05)" stroke="'+c+'" stroke-width="1.8"/>';
       s+='<text x="'+(px[n.id]+BW/2)+'" y="'+(py[n.id]+21)+'" text-anchor="middle" font-size="15" font-weight="600" fill="'+c+'">'+esc(n.code||n.id)+'</text>';
       s+='<text x="'+(px[n.id]+BW/2)+'" y="'+(py[n.id]+38)+'" text-anchor="middle" font-size="10.5" fill="#8ea0b8">'+esc(stOf(n))+'</text>';
       s+='<title>'+esc(n.label)+'</title></g>';});
     s+='</svg>';
     html+=s;
   }
   const GDEF=[{t:'核心 C',f:c=>c==='C'},{t:'G2–G8',f:c=>/^G[2-8]$/.test(c)},
     {t:'G9–G22',f:c=>{const m=/^G(\d+)$/.exec(c);return m&&+m[1]>=9&&+m[1]<=22;}},
     {t:'N1–N4',f:c=>/^N[1-4]$/.test(c)}];
   html+=GDEF.map(g=>{const list=N.filter(n=>g.f(n.code||''));
     if(!list.length)return '';
     return '<div style="margin-top:9px"><span style="color:var(--mut);font-size:11.5px;margin-right:8px">'+g.t+'</span>'
       +list.sort((a,b)=>(a.code||'').localeCompare(b.code||'',undefined,{numeric:true}))
       .map(n=>'<span class="tag" style="background:'+(hex(stOf(n)))+'22;color:'+hex(stOf(n))+'" title="'+esc(n.label)+'">'+esc(n.code)+' · '+esc(stOf(n))+'</span>').join('')+'</div>';}).join('');
   el('gchain').innerHTML=html;}
 function render(){
   const q=(el('pq').value||'').trim().toLowerCase(),t=el('pt').value;
   const rows=D.props.filter(p=>(t==='全部'||p.type===t)&&(!q||(p.statement+p.prop_id).toLowerCase().includes(q)));
   el('ptb').innerHTML=rows.map(p=>{const g=STATUS_GROUP(p.status),cls={'闭合':'t-ok','未闭合/待证':'t-gap','axiom':'t-ax'}[g]||'';
     return '<tr><td><code>'+esc(p.prop_id)+'</code></td><td>'+esc(p.statement)+'</td><td>'+esc(p.type)+'</td>'
     +'<td><span class="tag '+cls+'">'+esc(p.status)+'</span></td><td>'+esc(p.source_doc)+'</td><td><code>'+esc(p.depends_on)+'</code></td></tr>';}).join('');
   el('pcount').textContent='显示 '+rows.length+' / '+D.props.length;}
 ['pq','pt'].forEach(i=>{el(i).oninput=render;el(i).onchange=render;});render();}
/* ---------- 关系与超边 ---------- */
{const rt=['全部'].concat([...new Set(D.args.map(a=>a.type))].sort());
 V('rel').innerHTML='<h2>论证 / 关系</h2><div class="grid g2">'
 +'<div class="card"><h3>关系类型<em>70 条</em></h3>'+hbars(Object.entries(relHist).sort((a,b)=>b[1]-a[1]).map(([t,n])=>({label:t,value:n,color:REL_COLOR[t]||'#38bdf8'})),{lw:76})+'</div>'
 +'<div class="card"><h3>超边 ⇒ 明细<em>多因一果</em></h3><div class="scroll" style="max-height:260px"><table><thead><tr><th>ID</th><th>前件</th><th>后件</th></tr></thead><tbody>'
 +D.hypergraph.hyperedges.map(h=>'<tr><td><code>'+esc(h.id)+'</code></td><td>'+h.premises.map(p=>esc((CN[p]||{}).name||p)).join('、')+'</td><td>'+h.conclusion.map(c=>esc((CN[c]||{}).name||c)).join('、')+'</td></tr>').join('')
 +'</tbody></table></div></div></div>'
 +'<h2>全部论证</h2><div class="tbx"><input id="rq" placeholder="搜索前件 / 后件 / 编号…" style="min-width:230px">'
 +'<select id="rt">'+rt.map(t=>'<option>'+esc(t)+'</option>').join('')+'</select><span class="count" id="rcount"></span></div>'
 +'<div class="scroll"><table><thead><tr><th>ID</th><th>类型</th><th>前件</th><th>后件</th><th>概念链</th><th>出处</th></tr></thead><tbody id="rtb"></tbody></table></div>';
 function render(){
   const q=(el('rq').value||'').trim().toLowerCase(),t=el('rt').value;
   const rows=D.args.filter(a=>(t==='全部'||a.type===t)&&(!q||(a.premises+a.conclusion+a.arg_id+a.source_concept).toLowerCase().includes(q)));
   el('rtb').innerHTML=rows.map(a=>'<tr><td><code>'+esc(a.arg_id)+'</code></td><td><span class="tag '+((/^H/.test(a.arg_id))?'t-hy':'')+'">'+esc(a.type)+'</span></td>'
     +'<td>'+esc(a.premises)+'</td><td>'+esc(a.conclusion)+'</td><td><code>'+esc(a.source_concept)+'</code></td><td>'+esc(a.source_doc)+'</td></tr>').join('');
   el('rcount').textContent='显示 '+rows.length+' / '+D.args.length;}
 ['rq','rt'].forEach(i=>{el(i).oninput=render;el(i).onchange=render;});render();}
/* ---------- Lean ---------- */
{const kinds=Object.entries(D.lean_kinds).sort((a,b)=>b[1]-a[1]);
 V('lean').innerHTML='<h2>Lean 结构对接</h2><div class="grid g2">'
 +'<div class="card"><h3>声明构成<em>'+D.meta.decls+' 条 / '+D.meta.modules+' 模块</em></h3>'
 +stackbar([{label:'全部',parts:kinds.map(([k,n])=>({label:k,value:n}))}],{keys:kinds.map(k=>k[0]),colors:KIND_COLOR,lw:52,w:470,noKeys:true})
 +'<div class="legend">'+kinds.map(([k,n])=>'<span><i style="background:'+(KIND_COLOR[k]||'#888')+'"></i>'+esc(k)+' '+n+'</span>').join('')+'</div></div>'
 +'<div class="card"><h3>声明最多的模块<em>Top 16</em></h3>'
 +hbars(D.lean_top_modules.map(m=>({label:m.module,value:m.total,color:'#a78bfa'})),{lw:150,lh:19,w:470})+'</div></div>'
 +'<h2>Lean ↔ 概念 ↔ 缺口（25 条）</h2><div class="scroll" style="max-height:44vh"><table><thead><tr><th>Lean 库</th><th>关键符号</th><th>概念</th><th>命题</th><th>缺口</th><th>说明</th></tr></thead><tbody>'
 +D.lean_map.map(r=>{const gs=(r.gap_ids||'').split(';').filter(Boolean).map(g=>'<span class="tag t-gap">'+esc(g)+'</span>').join('')||'—';
   return '<tr><td><code>'+esc(r.lean_library)+'</code></td><td><code>'+esc(r.lean_symbol)+'</code></td><td>'+esc(r.concept_ids)+'</td><td>'+esc(r.prop_ids)+'</td><td>'+gs+'</td><td>'+esc(r.remark)+'</td></tr>';}).join('')
 +'</tbody></table></div>'
 +'<h2>模块声明统计（自动抽取）</h2><div class="scroll" style="max-height:44vh"><table><thead><tr><th>模块</th><th>文件</th><th>theorem/lemma</th><th>def</th><th>axiom</th><th>合计</th></tr></thead><tbody>'
 +D.lean_modules.filter(m=>+m.total_decl>0).map(m=>'<tr><td><code>'+esc(m.module)+'</code></td><td>'+esc(m.file)+'</td><td>'+esc(m.theorem_like)+'</td><td>'+esc(m.def_like)+'</td><td>'+esc(m.axiom)+'</td><td>'+esc(m.total_decl)+'</td></tr>').join('')
 +'</tbody></table></div>';}
/* ---------- 动态机制 ---------- */
{const E=D.elasticity;
 V('dyn').innerHTML='<h2>重写系统前向派生</h2><div class="grid g2">'
 +'<div class="card"><h3>派生级联<em>'+D.meta.rules_fired+' 条规则 / '+D.meta.steps+' 轮 · 可达 '+D.meta.reached+'/'+D.meta.nodes+'</em></h3>'+cascade(D.dynamics.seed_concepts.length,D.cascade,{h:236})
 +'<div class="hint">种子 '+D.dynamics.seed_concepts.length+' · 逐轮新增 '+D.cascade.map(c=>c.new.length).join(' / ')+' · 累计 <b>'+D.meta.reached+'/'+D.meta.nodes+'</b></div></div>'
 +'<div class="card"><h3>G<sub>N</sub> 结构因果模型 · 对数弹性<em>对数刻度</em></h3>'
 +logbars([['I','dlnGN/dlnI'],['λ_c','dlnGN/dlnlambda_c'],['𝔠₁','dlnGN/dlnc_1'],['m_p','dlnGN/dlnm_p'],['κ','dlnGN/dlnkappa'],['☯','dlnGN/dlntaiji']]
   .map(([lab,k])=>({label:lab,value:E[k],hot:k==='dlnGN/dlntaiji'})),{lw:56,w:470})
 +'<div class="note">☯ 弹性最大（≈88.6），是 G<sub>N</sub> 数值不确定性的瓶颈。构造后验数字校验，待独立复现。</div></div></div>'
 +'<h2>派生轨迹（49 条）</h2><div class="tbx"><select id="ds"><option value="">全部轮次</option>'
 +D.cascade.map(c=>'<option value="'+c.step+'">第 '+c.step+' 轮（'+c.rules.length+' 条）</option>').join('')+'</select><span class="count" id="dcount"></span></div>'
 +'<div class="scroll"><table><thead><tr><th>序</th><th>轮</th><th>规则</th><th>关系</th><th>前件</th><th>后件</th><th>深度</th></tr></thead><tbody id="dtb"></tbody></table></div>';
 const all=D.cascade.flatMap(c=>c.rules);
 function render(){const s=el('ds').value;const rows=s?all.filter(r=>String(r.step)===s):all;
   el('dtb').innerHTML=rows.map(r=>'<tr><td>'+r.order+'</td><td>'+r.step+'</td><td><code>'+esc(r.rule)+'</code></td>'
     +'<td><span class="tag '+(r.rel==='重组实现'?'t-hy':'')+'">'+esc(r.rel)+'</span></td>'
     +'<td>'+r.lhs.map(x=>esc((CN[x]||{}).name||x)).join('、')+'</td><td>'+esc(r.rhs_name)+' <code>'+esc(r.rhs)+'</code></td><td>'+(depth[r.rhs]!==undefined?depth[r.rhs]:'—')+'</td></tr>').join('');
   el('dcount').textContent='显示 '+rows.length+' / '+all.length;}
 el('ds').onchange=render;render();}
/* ---------- 证据层 ---------- */
{const E=D.evidence;
 const un=E.filter(r=>r.match_method==='unresolved').length;
 V('ev').innerHTML='<h2>证据层：断言 → 原文</h2><div class="kpis">'
  +[['断言',E.length],['有证据',E.length-un],['高置信',E.filter(r=>r.confidence==='high').length],
    ['含引文',E.filter(r=>r.quote_clean).length],['跨文档定位',E.filter(r=>String(r.doc_switch)==='True').length],
    ['人工已核验',E.filter(r=>String(r.verified)==='True').length]]
   .map(([k,v])=>'<div class="kpi"><b>'+v+'</b><span>'+k+'</span></div>').join('')+'</div>'
  +'<div class="note">机器定位结果一律 <code>verified=False</code>，人工复核后才置 True；'
  +'<code>check_provenance.py</code> 硬校验「引文必须逐字等于原文区间」，并统计覆盖率与跨文档定位。</div>'
  +'<h2>定位明细</h2><div class="tbx"><input id="eq" placeholder="搜索条目 / 引文 / 章节…" style="min-width:240px">'
  +'<select id="em"><option value="">全部方法</option>'+[...new Set(E.map(r=>r.match_method))].map(m=>'<option>'+m+'</option>').join('')+'</select>'
  +'<select id="ec"><option value="">全部置信</option><option>high</option><option>medium</option><option>low</option></select>'
  +'<select id="ek"><option value="">全部类别</option>'+[...new Set(E.map(r=>r.kind))].map(m=>'<option>'+m+'</option>').join('')+'</select>'
  +'<span class="count" id="ecount"></span></div>'
  +'<div class="scroll"><table><thead><tr><th>条目</th><th>名称</th><th>方法</th><th>置信</th><th>复核</th><th>出处 / 章节</th><th>字符区间</th><th>引文</th></tr></thead><tbody id="etb"></tbody></table></div>';
 function renderEv(){
   const q=(el('eq').value||'').trim().toLowerCase(),m=el('em').value,c=el('ec').value,k=el('ek').value;
   const rows=E.filter(r=>(!m||r.match_method===m)&&(!c||r.confidence===c)&&(!k||r.kind===k)
     &&(!q||(r.struct_id+' '+r.name+' '+r.quote_clean+' '+r.sec_title+' '+r.evidence_doc).toLowerCase().includes(q)));
   el('etb').innerHTML=rows.slice(0,300).map(r=>{
     const cls=r.confidence==='high'?'t-ok':(r.confidence==='unresolved'?'t-gap':(r.confidence==='low'?'t-ax':''));
     return '<tr><td><code>'+esc(r.struct_id)+'</code></td><td>'+esc(r.name).slice(0,26)+'</td><td>'+esc(r.match_method)+'</td>'
      +'<td><span class="tag '+cls+'">'+esc(r.confidence)+'</span></td>'
      +'<td>'+(r.review_verdict?'<span class="tag '+(r.review_verdict==='approved'?'t-ok':(r.review_verdict==='rejected'?'t-gap':'t-ax'))+'">'
        +esc(r.review_verdict)+(r.reviewer?' · '+esc(r.reviewer):'')+'</span>':'<span class="tag t-neu">未复核</span>')+'</td>'
      +'<td>'+esc(r.evidence_doc||r.doc_id)+(r.sec_title?' · '+esc(r.sec_title).slice(0,18):'')+'</td>'
      +'<td>'+esc(r.char_start)+'-'+esc(r.char_end)+'</td>'
      +'<td>'+esc(r.quote_clean).slice(0,90)+'</td></tr>';}).join('');
   el('ecount').textContent='显示 '+Math.min(rows.length,300)+' / '+rows.length;}
 ['eq','em','ec','ek'].forEach(i=>{el(i).oninput=renderEv;el(i).onchange=renderEv;});renderEv();}
/* ---------- 质量看板 ---------- */
{const Q=D.quality,S=Q.shacl,e=Q.extract,t=Q.terms,K=D.kg_stats,O=Q.ontology;
 const ch=Q.claim_hist,chItems=Object.entries(ch).sort((a,b)=>b[1]-a[1]);
 const chTotal=chItems.reduce((a,b)=>a+b[1],0);
 V('qual').innerHTML='<h2>质量看板</h2><div class="kpis">'
  +[['SHACL 合规',S.conforms?'通过':'违约 '+S.violations],['RDF 三元组',Q.rdf.triples_exported],
    ['图谱实体',K.concepts+K.props+K.gaps],['关系 / claim 边',K.relations+' / '+K.claim_edges],
    ['缺口依赖边',Q.gap_dep_edges],['关系抽取 F1',e.f1_pair]]
   .map(([k,v])=>'<div class="kpi"><b>'+v+'</b><span>'+k+'</span></div>').join('')+'</div>'
  +'<div class="grid g2"><div class="card"><h3>数据契约（SHACL）<em>'+esc(S.shapes_file)+'</em></h3>'
  +(S.violations?Object.entries(S.by_message).map(([m,n])=>'<div class="hint">· '+n+' × '+esc(m)+'</div>').join('')
    :'<div class="hint">全部通过：概念 / 命题 / 缺口 / 超边 / 论证均具备规范名、定义、出处与证据；缺口编号匹配 <code>^(C|G\\d+|N\\d+)$</code>；有向论证的关系类型限于既有 5 类。</div>')
  +'</div><div class="card"><h3>本体推理<em>HermiT</em></h3><table><tbody>'
  +[['一致性',Q.reasoner.consistent?'一致（无不可满足类）':'不一致'],
    ['OWL 类 / 个体',O.owl_classes+' / '+O.owl_individuals],
    ['对象属性 / 互斥类型类',O.owl_object_properties+' / '+O.owl_disjoint_type_classes],
    ['限制公理 / 注解属性',O.owl_restrictions+' / '+O.owl_annotation_properties],
    ['概念别名',Q.alias_count+' 条（同义词 / 符号 / 论证表变体）'],
    ['论证词表对齐',Q.align.count_ok+'/'+Q.align.args+' 前件数与 ID 数一致']]
   .map(([a,b])=>'<tr><td>'+a+'</td><td>'+b+'</td></tr>').join('')+'</tbody></table></div>'
  +'<div class="card"><h3>关系抽取评测<em>金标准 = 人工论证表</em></h3><table><tbody>'
  +[['候选 / 金标准配对',e.candidates+' / '+e.gold_pairs],['配对精确率 P',e.precision_pair],
    ['配对召回率 R',e.recall_pair],['配对 F1',e.f1_pair],
    ['召回上界（原文共现）',e.recall_ceiling_sentence_cooccurrence+'（当前达上界 '+e.recall_vs_ceiling+'）'],
    ['关系类型命中率',e.relation_type_accuracy]]
   .map(([a,b])=>'<tr><td>'+a+'</td><td>'+b+'</td></tr>').join('')+'</tbody></table>'
  +'<div class="hint">上界即"金标准两端在原文同一句出现"的比例：说明论证表的关系多为组织层归纳，'
  +'原文缺少显式句式——这是模式抽取的诚实边界，也是需要语义模型 + 人工复核的环节。</div></div>'
  +'<div class="card"><h3>主张图构成<em>'+chTotal+' 条 claim 边</em></h3>'
  +hbars(chItems.map(([k,v])=>({label:k,value:v,color:'#a78bfa'})),{w:430,lw:118,lh:20})+'</div>'
  +'<div class="card"><h3>术语候选池<em>'+t.new_candidates_kept+' 条新候选</em></h3>'
  +'<div class="hint">无监督新词发现（n-gram 2–5 · 内部凝固度 ≥ '+t.thresholds.min_pmi+' · 左右邻接熵 ≥ '+t.thresholds.min_boundary_entropy+' · 频次 ≥ '+t.thresholds.min_freq+'）。'
  +'<b>候选不进入概念表</b>——只有人工确认且与权威定义处一致的术语才可入库。</div>'
  +'<div>'+t.top_new.slice(0,28).map(x=>'<span class="tag t-neu">'+esc(x)+'</span>').join('')+'</div></div></div>';}
{const O=D.ontology,m=D.meta;
 V('meta').innerHTML='<h2>本体与快照</h2><div class="grid g2">'
 +'<div class="card"><h3>本体统计</h3><table><tbody>'
 +Object.entries({'概念数':O.concept_count,'命题数':O.proposition_count,'论证数':O.argument_count,'OWL 类':O.owl_classes,
   'OWL 个体':O.owl_individuals,'OWL 对象属性':O.owl_object_properties,'跨类型边':O.cross_type_edges})
   .map(([k,v])=>'<tr><td>'+k+'</td><td><b>'+v+'</b></td></tr>').join('')
 +'</tbody></table></div>'
 +'<div class="card"><h3>数据下载与入口</h3><div class="links">'
 +'<a href="data.json">data.json（本页数据快照）</a>'
 +'<a href="../交互式可视化/超图交互.html">交互式超图</a>'
 +'<a href="../index.html">研究站首页</a>'
 +'<a href="../蓝图/index.html">形式化蓝图</a>'
 +'<a href="../检索台/index.html">检索台（BM25 / SPARQL）</a></div>'
 +'<div class="hint">源 CSV / JSON / OWL 见各维度目录；本页为派生呈现，源为唯一事实。</div></div></div>'
 +'<h2>快照</h2><div class="kpis">'+[['概念',m.nodes],['命题',m.props],['论证',m.args],['Lean 模块',m.modules],['Lean 声明',m.decls],['可达概念',m.reached+'/'+m.nodes]]
   .map(([k,v])=>'<div class="kpi"><b>'+v+'</b><span>'+k+'</span></div>').join('')+'</div>'
 +'<div class="note">形式化覆盖 F 仅 41/82（50.0%）；未覆盖概念不得视为已形式化。缺口状态未改动；贝叶斯 CPT 为占位。</div>';}
/* ---------- 全局检索 ---------- */
{const box=el('gres'),inp=el('gq');
 function search(){
   const q=(inp.value||'').trim().toLowerCase();
   if(!q){box.classList.remove('on');box.innerHTML='';return;}
   const hits=[];
   D.concepts.forEach(c=>{if((c.name+c.definition+c.concept_id).toLowerCase().includes(q))hits.push(['概念',c.concept_id,c.name,c.definition,'con']);});
   D.props.forEach(p=>{if((p.statement+p.prop_id).toLowerCase().includes(q))hits.push(['命题',p.prop_id,p.statement,'',  'prop']);});
   D.args.forEach(a=>{if((a.premises+a.conclusion+a.arg_id).toLowerCase().includes(q))hits.push(['论证',a.arg_id,a.premises+' → '+a.conclusion,'','rel']);});
   box.innerHTML=hits.slice(0,40).map(h=>'<a data-go="'+h[4]+'"><i>'+esc(h[1])+'</i>'+esc(h[2]).slice(0,88)+'<u>'+h[0]+'</u></a>').join('')||'<div class="empty">无匹配</div>';
   box.classList.add('on');}
 inp.oninput=search;
 inp.onfocus=search;
 box.addEventListener('click',e=>{const a=e.target.closest('a[data-go]');if(!a)return;
   const t=a.dataset.go;const btn=document.querySelector('#nav button[data-t="'+t+'"]');if(btn)btn.click();
   const q=inp.value.trim();const map={con:'cq',prop:'pq',rel:'rq'};
   setTimeout(()=>{const i=el(map[t]);if(i){i.value=q;i.dispatchEvent(new Event('input'));}},30);
   box.classList.remove('on');inp.blur();});
 document.addEventListener('click',e=>{if(!e.target.closest('.gsearch'))box.classList.remove('on');});
 document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();inp.focus();inp.select();}
   if(e.key==='Escape')box.classList.remove('on');});}
el('snap').textContent=new Date().toLocaleString('zh-CN',{hour12:false}).replace(/\//g,'-');
</script>
</body></html>"""


# ============================ 交互式超图 ============================
HYPER_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CQM 概念关系超图 · 可推演</title>
<style>
:root{--bg:#070b12;--line:rgba(255,255,255,.09);--ink:#e6eef8;--mut:#8ea0b8;--acc:#38bdf8;--hy:#f59e0b}
*{box-sizing:border-box}html,body{margin:0;height:100%}
body{font:13px/1.6 "Microsoft YaHei",system-ui,sans-serif;background:var(--bg);color:var(--ink);display:flex;flex-direction:column;overflow:hidden}
header{background:linear-gradient(120deg,rgba(34,69,107,.95),rgba(12,22,38,.95));border-bottom:1px solid var(--line);padding:8px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
header h1{font-size:14px;margin:0;letter-spacing:.3px}
header .sub{opacity:.8;font-size:11.5px;color:#bcd3ea}
.ctrl{display:flex;gap:9px;align-items:center;margin-left:auto;flex-wrap:wrap}
.ctrl select,.ctrl label{font-size:12px;color:#cfdcec}
.ctrl select{padding:4px 8px;border:1px solid rgba(255,255,255,.16);border-radius:7px;background:rgba(255,255,255,.07);color:#fff;font:inherit;outline:none}
.ctrl input[type=search]{padding:5px 10px;border:1px solid rgba(255,255,255,.16);border-radius:8px;background:rgba(255,255,255,.07);color:#fff;font:inherit;outline:none;width:170px}
.ctrl input[type=search]:focus{border-color:rgba(56,189,248,.7);box-shadow:0 0 0 3px rgba(56,189,248,.14)}
.bar2{display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:7px 16px;background:rgba(255,255,255,.03);border-bottom:1px solid var(--line);font-size:12px}
.bar2 .sep{width:1px;height:18px;background:var(--line);margin-left:auto}
button.cls{border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.06);border-radius:8px;padding:4px 11px;font:inherit;color:#dce7f5;cursor:pointer;transition:.15s}
button.cls:hover{background:rgba(56,189,248,.18);border-color:rgba(56,189,248,.5)}
button.cls.pri{background:linear-gradient(90deg,rgba(56,189,248,.30),rgba(167,139,250,.24));border-color:rgba(56,189,248,.55);color:#fff}
button.cls:disabled{opacity:.4;cursor:default}
#wrap{flex:1;position:relative;overflow:hidden;display:flex;background:
 radial-gradient(900px 500px at 20% 0%,rgba(56,189,248,.10),transparent 60%),
 radial-gradient(700px 460px at 90% 100%,rgba(167,139,250,.10),transparent 60%),#070b12}
#cy{flex:1}
#tip{position:absolute;pointer-events:none;background:rgba(10,16,26,.96);border:1px solid rgba(56,189,248,.35);color:#e6eef8;padding:8px 11px;border-radius:9px;font-size:12px;max-width:330px;display:none;z-index:9;line-height:1.55;box-shadow:0 12px 30px rgba(0,0,0,.5)}
#side{position:absolute;right:0;top:0;bottom:0;width:344px;background:rgba(11,18,32,.97);border-left:1px solid var(--line);padding:14px 16px;overflow:auto;transform:translateX(100%);transition:.28s cubic-bezier(.22,.7,.3,1);z-index:8;box-shadow:-10px 0 30px rgba(0,0,0,.45)}
#side.on{transform:none}
#side h3{margin:0 0 4px;font-size:14.5px;color:#eaf3ff}
#side .k{color:var(--mut);font-size:11.5px}
#side .def{color:#c6d6e8;font-size:12.5px;margin:8px 0;padding:8px 10px;background:rgba(255,255,255,.04);border-radius:8px;border-left:2px solid var(--acc)}
#side table{width:100%;border-collapse:collapse;font-size:12px;margin-top:6px}
#side td{padding:4px 5px;border-bottom:1px solid rgba(255,255,255,.06);vertical-align:top}
#side a{color:var(--acc);cursor:pointer;text-decoration:none}
#side a:hover{text-decoration:underline}
.sidebtns{display:flex;gap:6px;flex-wrap:wrap;margin-top:9px}
.legend{display:flex;gap:6px 12px;flex-wrap:wrap;font-size:11.5px;padding:6px 16px;background:rgba(255,255,255,.03);border-top:1px solid var(--line);color:var(--mut)}
.legend span{cursor:pointer;user-select:none;transition:.15s}
.legend span.off{opacity:.32;text-decoration:line-through}
.legend i{display:inline-block;width:9px;height:9px;border-radius:3px;margin-right:5px;vertical-align:middle}
#narr{color:#cfe2f6;font-size:12px}
#narr b{color:#7dd3fc}
#mini{position:absolute;right:12px;bottom:12px;width:176px;height:124px;background:rgba(8,13,22,.88);border:1px solid var(--line);border-radius:10px;z-index:7;cursor:crosshair}
#mini canvas{width:100%;height:100%;border-radius:10px}
.badge{display:inline-block;padding:1px 7px;border-radius:9px;font-size:11px;background:rgba(56,189,248,.16);color:#7dd3fc;margin-left:6px}
.badge.hy{background:rgba(245,158,11,.18);color:#fbd38d}
.badge.gap{background:rgba(248,113,113,.16);color:#fca5a5}
#prog{position:relative;height:5px;flex:0 0 190px;background:rgba(255,255,255,.09);border-radius:3px;overflow:hidden}
#prog i{position:absolute;left:0;top:0;bottom:0;width:0;background:linear-gradient(90deg,#38bdf8,#a78bfa);transition:width .3s}
</style></head>
<body>
<header>
  <h1>CQM 概念关系超图</h1><span class="sub" id="stat"></span>
  <div class="ctrl">
    <input type="search" id="q" placeholder="搜索概念…">
    <label>关系 <select id="flt"><option value="">全部</option><option>重组实现</option><option>演化</option><option>映射</option><option>等价</option><option>依赖</option><option>层级含于</option></select></label>
    <label>布局 <select id="lay"><option value="clusters">类型分簇</option><option value="cose">力导向</option><option value="concentric">同心</option><option value="circle">环形</option><option value="grid">网格</option><option value="breadthfirst">层级</option></select></label>
    <label><input type="checkbox" id="lbl" checked> 标签</label>
    <label><input type="checkbox" id="hy" checked> 超边</label>
    <label><input type="checkbox" id="kg"> 命题/缺口层</label>
    <button class="cls" id="reset">重置布局</button>
    <button class="cls" id="png">导出 PNG</button>
    <button class="cls" id="fs">全屏</button>
  </div>
</header>
<div class="bar2">
  <button class="cls pri" id="play">▶ 派生回放</button>
  <button class="cls" id="next">下一轮 ⏭</button>
  <button class="cls" id="prst">↺ 复位</button>
  <label>速度 <select id="spd"><option value="1400">慢</option><option value="900" selected>中</option><option value="450">快</option></select></label>
  <div id="prog"><i></i></div>
  <span id="narr">—</span>
  <div class="sep"></div>
  <label>路径 <input list="cl" id="pa" placeholder="起点" style="width:92px;padding:3px 8px;border:1px solid rgba(255,255,255,.16);border-radius:7px;background:rgba(255,255,255,.07);color:#fff;font:inherit"></label>
  <label>→ <input list="cl" id="pb" placeholder="终点" style="width:92px;padding:3px 8px;border:1px solid rgba(255,255,255,.16);border-radius:7px;background:rgba(255,255,255,.07);color:#fff;font:inherit"></label>
  <button class="cls" id="find">找路径</button>
  <button class="cls" id="clr">清除</button>
  <datalist id="cl"></datalist>
</div>
<div id="wrap">
  <div id="cy"></div>
  <div id="tip"></div>
  <div id="side"><div style="display:flex;justify-content:space-between;align-items:center"><b style="font-size:13px">节点详情</b><button class="cls" onclick="closeSide()">关闭</button></div><div id="sidebody"></div></div>
  <div id="mini"><canvas id="mc" width="352" height="248"></canvas></div>
</div>
<div class="legend" id="lg"></div>
<script src="assets/cytoscape.min.js"></script>
<script>
const PAY=__DATA__;
const HG=PAY.hg,CASC=PAY.cascade,DYN=PAY.dynamics,DEPTH=PAY.depth||{},SCM=PAY.scm||{};
const KG=PAY.kg||{nodes:[],edges:[]};
const TYPE_COLOR={'本体论':'#f0916a','理论框架':'#c39bf5','数学结构':'#6aa9f0','群论':'#4fd1a5','关系类型':'#9aa6b2',
 '引力层级':'#e3c05a','纤维丛':'#a08cf0','几何':'#4fc4d6','量纲':'#e0845f','数论':'#4fd07a','物理':'#5b95e8','共形场论':'#e070b0'};
const REL_COLOR={'重组实现':'#f59e0b','映射':'#38bdf8','演化':'#a78bfa','等价':'#34d399','依赖':'#f472b6','层级含于':'#facc15'};
const HYPER_COLOR='#f59e0b';
const NODES=HG.nodes,HY=HG.hyperedges,ED=HG.directed_edges;
const KG_NODES=KG.nodes||[];
const ALLID=new Set(NODES.map(n=>n.id).concat(KG_NODES.map(n=>n.id)));
const KG_EDGES=(KG.edges||[]).filter(e=>e.src&&e.dst&&e.src[0]&&e.dst[0]&&ALLID.has(e.src[0])&&ALLID.has(e.dst[0]));
const labelById={};NODES.forEach(n=>labelById[n.id]=n.label);
const idByLabel={};NODES.forEach(n=>{if(!(n.label in idByLabel))idByLabel[n.label]=n.id;});
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const ruleEl=id=>(/^H/.test(id)?'#HY_'+id:'#E_'+id);
const SEEDS=new Set(DYN.seed_concepts);
const STEPS=CASC.map(c=>c.step);
let play={on:false,step:0,active:new Set(),timer:null};
document.getElementById('stat').innerHTML=NODES.length+' 概念 · '+HY.length+' 超边 ⇒ · '+ED.length+' 有向边 →'
  +'<span class="badge">派生 '+DYN.steps+' 轮</span><span class="badge">可达 '+DYN.reachable_concepts+'/'+NODES.length+'</span>'
  +'<span class="badge hy">命题 '+KG_NODES.filter(n=>n.kind!=='gap').length+' · 缺口 '+KG_NODES.filter(n=>n.kind==='gap').length+' · claim 边 '+KG_EDGES.length+'</span>';
document.getElementById('cl').innerHTML=NODES.map(n=>'<option value="'+esc(n.label)+'">'+n.id+'</option>').join('');
/* ---- 度数 ---- */
const deg={};NODES.forEach(n=>deg[n.id]=0);
ED.forEach(e=>{if(deg[e.source]!=null)deg[e.source]++;if(deg[e.target]!=null)deg[e.target]++;});
HY.forEach(h=>{h.premises.forEach(p=>{if(deg[p]!=null)deg[p]++;});h.conclusion.forEach(c=>{if(deg[c]!=null)deg[c]++;});});
/* ---- 类型扇区（类型分簇布局的扇区标签） ---- */
function sectorAngles(){
  const types=[...new Set(NODES.map(n=>n.type))].sort();
  const by={};NODES.forEach(n=>(by[n.type]=by[n.type]||[]).push(n));
  let a0=-Math.PI/2,out=[];
  types.forEach(t=>{const span=Math.PI*2*by[t].length/NODES.length;
    out.push({type:t,list:by[t],a0:a0,span:span,mid:a0+span/2});a0+=span;});
  return out;
}
const SECTORS=sectorAngles();
/* ---- 图元素 ---- */
const els=[];
NODES.forEach(n=>els.push({data:{id:n.id,label:n.label,type:n.type,color:TYPE_COLOR[n.type]||'#8899aa',
  def:n.definition,doc:n.source_doc+(n.source_loc?(' '+n.source_loc):''),deg:deg[n.id]||0,depth:(n.id in DEPTH?DEPTH[n.id]:-1),kind:'concept'}}));
HY.forEach(h=>{const hub='HY_'+h.id;
  els.push({data:{id:hub,label:h.id,kind:'hyper',rule:h.id}});
  h.premises.forEach((p,i)=>els.push({data:{id:h.id+'_p'+i,source:p,target:hub,kind:'hmem',rule:h.id}}));
  h.conclusion.forEach((c,i)=>els.push({data:{id:h.id+'_c'+i,source:hub,target:c,kind:'hcon',rule:h.id}}));});
ED.forEach(e=>els.push({data:{id:'E_'+e.id,source:e.source,target:e.target,kind:'dir',rel:e.type,rule:e.id,color:REL_COLOR[e.type]||'#54637a'}}));
SECTORS.forEach((s,i)=>els.push({data:{id:'SEC_'+i,label:s.type+' '+s.list.length,kind:'sector',color:TYPE_COLOR[s.type]||'#8899aa'}}));
/* 命题 / 缺口层与 claim 边（多层图谱：概念 ⊂ 主张 ⊂ 缺口） */
KG_NODES.forEach(n=>els.push({data:{id:n.id,label:(n.kind==='gap'?(n.code||n.id):n.id),full:(n.label||''),
  kind:(n.kind==='gap'?'gap':'prop'),ptype:n.type||'',status:n.status||'',code:n.code||'',doc:n.doc||'',
  ev:(n.ev&&n.ev.quote_clean)||'',evMethod:(n.ev&&n.ev.match_method)||'',evConf:(n.ev&&n.ev.confidence)||'',
  evSpan:(n.ev&&n.ev.char_start?n.ev.char_start+'-'+n.ev.char_end:''),evSec:(n.ev&&n.ev.sec_title)||''}}));
KG_EDGES.forEach((e,i)=>els.push({data:{id:'CL_'+i,source:e.src[0],target:e.dst[0],kind:'claim',
  rel:e.rel||'',verified:String(!!e.verified),method:e.method||''}}));
const cy=cytoscape({
  container:document.getElementById('cy'),elements:els,wheelSensitivity:.22,minZoom:.08,maxZoom:5,
  style:[
    {selector:'node',style:{'label':'data(label)','font-size':'10px','color':'#dbe7f3','text-valign':'bottom','text-halign':'center',
      'text-margin-y':4,'text-outline-width':2.6,'text-outline-color':'#070b12','border-width':1.2,'border-color':'rgba(255,255,255,.32)',
      'transition-property':'opacity,background-color,border-color,shadow-opacity','transition-duration':'260ms'}},
    {selector:'node[kind="concept"]',style:{'background-color':'data(color)','width':'mapData(deg,0,24,17,40)','height':'mapData(deg,0,24,17,40)',
      'shadow-blur':14,'shadow-color':'data(color)','shadow-opacity':.5,'shadow-offset-x':0,'shadow-offset-y':0}},
    {selector:'node[kind="hyper"]',style:{'shape':'round-diamond','background-color':HYPER_COLOR,'width':14,'height':14,'font-size':8,
      'color':HYPER_COLOR,'text-valign':'center','text-outline-width':0,'shadow-blur':12,'shadow-color':HYPER_COLOR,'shadow-opacity':.45}},
    {selector:'node[kind="sector"]',style:{'background-opacity':0,'border-width':0,'width':1,'height':1,'font-size':21,
      'color':'rgba(255,255,255,.20)','text-valign':'center','text-halign':'center','text-outline-width':0,'events':'no','z-index':-1}},
    {selector:'node[kind="prop"]',style:{'shape':'round-rectangle','background-color':'#7c6cf0','background-opacity':.9,
      'width':'mapData(deg,0,24,11,20)','height':'mapData(deg,0,24,8,14)','font-size':8.5,'color':'#cfc4ff',
      'text-outline-width':2,'text-outline-color':'#070b12','border-width':1,'border-color':'rgba(196,181,253,.5)',
      'shadow-blur':10,'shadow-color':'#7c6cf0','shadow-opacity':.4}},
    {selector:'node[kind="gap"]',style:{'shape':'diamond','background-color':'#f87171','background-opacity':.92,
      'width':15,'height':15,'font-size':8.5,'color':'#fca5a5','text-outline-width':2,'text-outline-color':'#070b12',
      'shadow-blur':12,'shadow-color':'#f87171','shadow-opacity':.5}},
    {selector:'node[kind="gap"][status="闭合"]',style:{'background-color':'#34d399','color':'#6ee7b7','shadow-color':'#34d399'}},
    {selector:'edge[kind="claim"]',style:{'line-color':'rgba(167,139,250,.55)','line-style':'dotted','width':1.1,
      'target-arrow-shape':'vee','target-arrow-color':'rgba(167,139,250,.7)','arrow-scale':.7,'curve-style':'bezier'}},
    {selector:'edge',style:{'curve-style':'bezier','width':1,'transition-property':'opacity,line-color,width','transition-duration':'260ms'}},
    {selector:'edge[kind="dir"]',style:{'line-color':'data(color)','line-opacity':.5,'target-arrow-shape':'triangle','target-arrow-color':'data(color)','arrow-scale':.85,'width':1.1}},
    {selector:'edge[kind="hmem"]',style:{'line-color':'rgba(245,158,11,.42)','line-style':'dashed','width':1.2}},
    {selector:'edge[kind="hcon"]',style:{'line-color':HYPER_COLOR,'line-opacity':.85,'width':1.8,'target-arrow-shape':'triangle','target-arrow-color':HYPER_COLOR,'arrow-scale':1}},
    {selector:'node.hit',style:{'border-width':3,'border-color':'#e0a020','shadow-opacity':.95,'shadow-blur':26}},
    {selector:'node:selected',style:{'border-width':3,'border-color':'#38bdf8','shadow-opacity':1,'shadow-blur':28}},
    {selector:'node.pathn',style:{'border-width':3,'border-color':'#22d3ee','shadow-color':'#22d3ee','shadow-opacity':1,'shadow-blur':26}},
    {selector:'edge.path',style:{'line-color':'#22d3ee','line-opacity':1,'width':3.4,'z-index':99}},
    {selector:'.faded',style:{'opacity':.055}},
    {selector:'node.pending',style:{'opacity':.13,'shadow-opacity':0,'border-color':'rgba(255,255,255,.10)'}},
    {selector:'node.fresh',style:{'border-width':3,'border-color':'#7dd3fc','shadow-color':'#38bdf8','shadow-opacity':1,'shadow-blur':30}},
    {selector:'edge.armed',style:{'line-opacity':1,'width':2.6,'line-color':'#fbbf24'}},
    {selector:'node.orphan',style:{'border-width':2.5,'border-style':'dashed','border-color':'#f87171','opacity':.85,'shadow-color':'#f87171','shadow-opacity':.5}}
  ]
});
/* ---- 布局 ---- */
const R_CLUSTER=520;
function clusterPositions(){
  const pos={};
  SECTORS.forEach(s=>{s.list.forEach((n,i)=>{
    const a=s.a0+s.span*((i+.5)/s.list.length),r=R_CLUSTER*(.62+.38*((i%3)/2));
    pos[n.id]={x:Math.cos(a)*r,y:Math.sin(a)*r};});});
  HY.forEach(h=>{const ps=h.premises.map(p=>pos[p]).filter(Boolean);
    pos['HY_'+h.id]=ps.length?{x:ps.reduce((a,b)=>a+b.x,0)/ps.length,y:ps.reduce((a,b)=>a+b.y,0)/ps.length}:{x:0,y:0};});
  SECTORS.forEach((s,i)=>pos['SEC_'+i]={x:Math.cos(s.mid)*R_CLUSTER*1.30,y:Math.sin(s.mid)*R_CLUSTER*1.30});
  // 命题/缺口节点放在其关联概念的质心（无关联者置于外环）
  const touch={};
  KG_EDGES.forEach(e=>{const a=e.src[0],b=e.dst[0];
    (touch[a]=touch[a]||[]).push(b);(touch[b]=touch[b]||[]).push(a);});
  KG_NODES.forEach((n,i)=>{
    const ps=(touch[n.id]||[]).map(x=>pos[x]).filter(Boolean);
    if(ps.length){pos[n.id]={x:ps.reduce((a,b)=>a+b.x,0)/ps.length*1.02,y:ps.reduce((a,b)=>a+b.y,0)/ps.length*1.02};}
    else{const a=Math.PI*2*i/Math.max(1,KG_NODES.length);pos[n.id]={x:Math.cos(a)*R_CLUSTER*1.45,y:Math.sin(a)*R_CLUSTER*1.45};}
  });
  return pos;
}
const LAYOUTS={
  cose:{name:'cose',animate:false,nodeRepulsion:30000,idealEdgeLength:105,edgeElasticity:130,nestingFactor:1.15,gravity:.28,numIter:1800,randomize:true},
  concentric:{name:'concentric',animate:false,minNodeSpacing:30,equator:1},
  circle:{name:'circle',animate:false},
  grid:{name:'grid',animate:false},
  breadthfirst:{name:'breadthfirst',animate:false,directed:true,spacingFactor:1.1}
};
let curLayout='clusters';
function runLayout(name){
  curLayout=name;
  cy.nodes('[kind="sector"]').style('display',name==='clusters'?'element':'none');
  const fitEles=cy.elements(':visible').not(cy.nodes('[kind="sector"]'));
  if(name==='clusters')cy.layout({name:'preset',positions:clusterPositions(),fit:false}).run();
  else cy.layout(Object.assign({},LAYOUTS[name]||LAYOUTS.cose,{eles:fitEles})).run();
  applyVisibility();
  cy.fit(cy.elements(':visible'),46);drawMini();
}
/* ---- 可见性 / 图例 ---- */
const hidden=new Set();
function applyVisibility(){
  const f=document.getElementById('flt').value,on=document.getElementById('hy').checked;
  const kgOn=document.getElementById('kg').checked&&!play.on;
  cy.batch(()=>{
    cy.nodes('[kind="hyper"]').style('display',on?'element':'none');
    cy.nodes('[kind="sector"]').style('display',curLayout==='clusters'?'element':'none');
    cy.nodes('[kind="prop"],[kind="gap"]').style('display',kgOn?'element':'none');
    cy.edges('[kind="claim"]').style('display',kgOn?'element':'none');
    cy.nodes('[kind="concept"]').forEach(n=>n.style('display',hidden.has(n.data('type'))?'none':'element'));
    cy.edges().forEach(e=>{const k=e.data('kind');let show=true;
      if(k==='hmem'||k==='hcon')show=on&&(!f||f==='重组实现');
      else if(k==='dir')show=(!f||e.data('rel')===f);
      e.style('display',show?'element':'none');});
  });
}
document.getElementById('lg').innerHTML=Object.entries(TYPE_COLOR).map(([k,c])=>'<span data-type="'+esc(k)+'"><i style="background:'+c+'"></i>'+esc(k)+'</span>').join('')
  +'<span style="cursor:default"><i style="background:'+HYPER_COLOR+'"></i>超边 ⇒ 哑节点</span>'
  +'<span style="cursor:default"><i style="background:#7c6cf0"></i>命题</span>'
  +'<span style="cursor:default"><i style="background:#f87171"></i>缺口（闭合转绿）</span>'
  +'<span style="cursor:default"><i style="background:rgba(167,139,250,.75)"></i>claim 边</span>';
document.querySelectorAll('#lg span[data-type]').forEach(sp=>sp.onclick=()=>{
  const t=sp.dataset.type;if(hidden.has(t))hidden.delete(t);else hidden.add(t);
  sp.classList.toggle('off',hidden.has(t));applyVisibility();});
/* ---- 搜索 ---- */
function applySearch(){
  const q=(document.getElementById('q').value||'').trim();
  cy.batch(()=>{
    if(!q){cy.nodes().removeClass('hit');return;}
    cy.nodes('[kind="concept"]').forEach(n=>{
      const hit=(n.data('label')||'').includes(q)||(n.data('def')||'').includes(q)||n.id().includes(q);
      n.toggleClass('hit',hit);});});
}
/* ---- 侧栏 ---- */
const side=document.getElementById('side'),sidebody=document.getElementById('sidebody'),tip=document.getElementById('tip');
let focused=null;
function neighborIds(n,r){
  const keep=new Set([n.id()]);
  for(let i=0;i<r;i++){
    [...keep].forEach(id=>{const el=cy.$id(id);if(!el.length)return;
      el.connectedEdges().forEach(e=>{const o=e.source().id()===id?e.target():e.source();keep.add(o.id());});});}
  return keep;
}
function focusNeighborhood(n,on){
  if(!on){cy.elements().removeClass('faded');focused=null;return;}
  const keep=neighborIds(n,1);
  cy.batch(()=>{cy.elements().removeClass('faded');
    cy.nodes().forEach(x=>{if(!keep.has(x.id()))x.addClass('faded');});
    cy.edges().forEach(e=>{if(!keep.has(e.source().id())||!keep.has(e.target().id()))e.addClass('faded');});});
  focused=n.id();
}
function openSide(n){
  side.classList.add('on');
  if(n.data('kind')==='concept'){
    const out=[],inn=[],hys=new Set();
    cy.edges('[kind="dir"]').forEach(e=>{if(e.source().id()===n.id())out.push(e);else if(e.target().id()===n.id())inn.push(e);});
    cy.edges('[kind="hmem"],[kind="hcon"]').forEach(e=>{if(e.source().id()===n.id()||e.target().id()===n.id())hys.add(e.data('rule'));});
    const rows=out.concat(inn).slice(0,40).map(e=>{const o=e.source().id()===n.id()?e.target():e.source();
      return '<tr><td><a data-go="'+o.id()+'">'+esc(o.data('label'))+'</a></td><td class="k">'+esc(e.data('rel')||'⇒')+'</td></tr>';}).join('');
    const d=n.data('depth');
    sidebody.innerHTML='<h3>'+esc(n.data('label'))+'<span class="badge">'+n.id()+'</span></h3>'
      +'<div class="k"><span class="badge" style="background:'+(n.data('color'))+'33;color:'+n.data('color')+'">'+esc(n.data('type'))+'</span>'
      +'<span class="badge">'+(d>=0?'派生深度 '+d:'未参与派生')+'</span></div>'
      +'<div class="def">'+esc(n.data('def'))+'</div>'
      +'<div class="k">出处：'+esc(n.data('doc'))+'</div>'
      +'<div class="k" style="margin-top:6px">出边 '+out.length+' · 入边 '+inn.length+' · 参与超边 '+hys.size+' · 度数 '+n.data('deg')+'</div>'
      +'<div class="sidebtns"><button class="cls" id="focbtn">聚焦邻域</button>'
      +'<button class="cls" id="pa_set">设为起点</button><button class="cls" id="pb_set">设为终点</button></div>'
      +'<table>'+rows+'</table>';
    document.getElementById('focbtn').onclick=()=>{if(focused===n.id()){focusNeighborhood(n,false);cy.fit(cy.elements(),46);}else focusNeighborhood(n,true);};
    document.getElementById('pa_set').onclick=()=>{document.getElementById('pa').value=n.data('label');};
    document.getElementById('pb_set').onclick=()=>{document.getElementById('pb').value=n.data('label');};
  }else if(n.data('kind')==='prop'||n.data('kind')==='gap'){
    const d=n.data();
    const nb=cy.edges('[kind="claim"]').filter(e=>e.source().id()===n.id()||e.target().id()===n.id());
    sidebody.innerHTML='<h3>'+esc((d.kind==='gap'?'缺口 ':'命题 ')+(d.code||n.id()))+'<span class="badge '+(d.kind==='gap'?'gap':'')+'">'+esc(d.status||'')+'</span></h3>'
      +'<div class="def">'+esc(d.full)+'</div>'
      +'<div class="k">'+esc(d.ptype||'')+' · 出处 '+esc(d.doc||'—')+' · 关联 '+nb.length+' 条</div>'
      +(d.ev?'<div class="k" style="margin-top:6px">证据（'+esc(d.evMethod)+'/'+esc(d.evConf)+' · 字符 '+esc(d.evSpan)+'）</div>'
        +'<div class="def">「'+esc(d.ev)+'」</div>':'<div class="k">（无证据）</div>')
      +'<table>'+nb.slice(0,24).map(e=>{const o=e.source().id()===n.id()?e.target():e.source();
        return '<tr><td><a data-go="'+o.id()+'">'+esc(o.data('label')||o.id())+'</a></td><td class="k">'+esc(e.data('rel'))+'</td></tr>';}).join('')+'</table>';
  }else{
    const h=HY.find(x=>x.id===n.data('rule'));
    sidebody.innerHTML='<h3>超边 '+esc(h.id)+'<span class="badge hy">⇒ 重组实现</span></h3>'
      +'<div class="k">多因一果：前件全部满足时后件被派生。</div><table>'
      +'<tr><td class="k">前件</td><td>'+h.premises.map(p=>'<a data-go="'+p+'">'+esc(labelById[p]||p)+'</a>').join('、')+'</td></tr>'
      +'<tr><td class="k">后件</td><td>'+h.conclusion.map(c=>'<a data-go="'+c+'">'+esc(labelById[c]||c)+'</a>').join('、')+'</td></tr>'
      +'<tr><td class="k">出处</td><td>'+[].concat(h.source_doc).map(esc).join('、')+'</td></tr></table>';
  }
}
function closeSide(){side.classList.remove('on');}
function focusNode(id){const n=cy.$id(id);if(!n.length)return;
  cy.elements().unselect();n.select();cy.animate({center:{eles:n},zoom:Math.max(cy.zoom(),1.15)},{duration:280});openSide(n);}
sidebody.addEventListener('click',ev=>{const a=ev.target.closest('a[data-go]');if(a)focusNode(a.dataset.go);});
cy.on('tap','node',ev=>openSide(ev.target));
cy.on('tap',ev=>{if(ev.target===cy)closeSide();});
cy.on('mouseover','node',ev=>{const p=ev.target.renderedPosition();
  tip.style.display='block';tip.style.left=(p.x+16)+'px';tip.style.top=(p.y+16)+'px';
  const d=ev.target.data();
  tip.innerHTML=d.kind==='concept'
    ?'<b>'+esc(d.label)+'</b> <span style="opacity:.6">'+ev.target.id()+'</span><br>'+esc(d.type)+' · 度数 '+d.deg+' · '+(d.depth>=0?'深度 '+d.depth:'未参与派生')
    :'<b>超边 '+ev.target.id().replace('HY_','')+'</b>（⇒ 重组实现）';});
cy.on('mouseout','node',()=>{tip.style.display='none';});
cy.on('select unselect',()=>drawMini());
/* ---- 派生回放 ---- */
const prog=document.querySelector('#prog i'),narr=document.getElementById('narr');
function paint(){
  cy.batch(()=>{
    if(!play.on&&play.step===0){cy.nodes().removeClass('pending').removeClass('fresh').removeClass('orphan');cy.edges().removeClass('armed');return;}
    cy.nodes('[kind="concept"]').forEach(n=>{const on=play.active.has(n.id());
      n.toggleClass('pending',!on);n.removeClass('fresh');});
    cy.nodes('[kind="hyper"]').removeClass('pending');
    cy.edges().forEach(e=>e.removeClass('armed'));
    const un=DYN.unreachable_concepts;
    cy.nodes('[kind="concept"]').forEach(n=>n.toggleClass('orphan',play.step>=DYN.steps&&un.indexOf(n.id())>=0));
  });
  applyVisibility();
}
function narrate(){
  if(!play.on){narr.innerHTML='点「派生回放」：44 个种子概念出发，按 <b>'+CASC.length+'</b> 轮重写逐轮点亮（数据取自 06 动态机制派生仿真）。';prog.style.width='0%';return;}
  if(play.step===0){narr.innerHTML='第 0 轮 · 种子 <b>'+play.active.size+'</b> 个概念（未点亮者表示尚未被派生）';prog.style.width='0%';return;}
  const c=CASC[play.step-1];
  narr.innerHTML='第 <b>'+c.step+'/'+CASC.length+'</b> 轮 · 触发 <b>'+c.rules.length+'</b> 条规则 · 新增 <b>'+c.new.length+'</b> 概念 · 累计可达 <b>'+c.cum+'/'+NODES.length+'</b>';
  prog.style.width=(play.step/CASC.length*100)+'%';
}
function doStep(){
  if(play.step>=CASC.length){stopPlay();return false;}
  const c=CASC[play.step];play.step++;
  cy.batch(()=>{
    cy.nodes().removeClass('fresh');
    c.rules.forEach(r=>{
      const re=cy.$(ruleEl(r.rule));
      if(re.length)re.addClass('armed');
      if(r.lhs.every(x=>play.active.has(x))&&!play.active.has(r.rhs))play.active.add(r.rhs);
      r.lhs.concat([r.rhs]).forEach(x=>cy.$id(x).removeClass('pending'));
      cy.$id(r.rhs).addClass('fresh');
      if(cy.$id(r.rhs).length)cy.$id(r.rhs).removeClass('pending');
    });
  });
  if(play.step>=CASC.length){
    cy.nodes('[kind="concept"]').forEach(n=>{if(DYN.unreachable_concepts.indexOf(n.id())>=0)n.addClass('orphan');});
    narrate();stopPlay();
    narr.innerHTML+=' · <span style="color:#fca5a5">不可达 '+DYN.unreachable_concepts.join('、')+'</span>（依赖自环或须理论外输入）';
    return false;
  }
  narrate();return true;
}
function tick(){if(play.on){if(!doStep())stopPlay();}}
function startPlay(){
  if(!play.on){play.on=true;play.step=0;play.active=new Set(SEEDS);paint();narrate();
    document.getElementById('play').innerHTML='⏸ 暂停';play.timer=setInterval(tick,+document.getElementById('spd').value);}
  else stopPlay();
}
function stopPlay(){play.on=false;clearInterval(play.timer);play.timer=null;document.getElementById('play').innerHTML='▶ 派生回放';paint();}document.getElementById('play').onclick=startPlay;
document.getElementById('next').onclick=()=>{if(!play.on&&play.step===0){play.on=true;play.active=new Set(SEEDS);paint();}
  if(!doStep()){if(play.step>=CASC.length)stopPlay();}};
document.getElementById('prst').onclick=()=>{stopPlay();play.step=0;play.active=new Set();cy.nodes().removeClass('pending').removeClass('fresh').removeClass('orphan');cy.edges().removeClass('armed');narrate();};
document.getElementById('spd').onchange=()=>{if(play.on){clearInterval(play.timer);play.timer=setInterval(tick,+document.getElementById('spd').value);}};
/* ---- 路径（有向：前件 → 超边 → 后件） ---- */
function adjacency(){const adj={};els.forEach(e=>{if(!e.data.source)return;
  (adj[e.data.source]=adj[e.data.source]||[]).push(e.data.target);});
  return adj;}
const ADJ=adjacency();
function bfs(a,b){const prev={},q=[a],seen=new Set([a]);
  while(q.length){const cur=q.shift();if(cur===b)break;
    (ADJ[cur]||[]).forEach(nx=>{if(!seen.has(nx)){seen.add(nx);prev[nx]=cur;q.push(nx);}});}
  if(!seen.has(b))return null;const path=[b];let c=b;
  while(c!==a){c=prev[c];path.unshift(c);}return path;}
document.getElementById('find').onclick=()=>{
  const a=idByLabel[document.getElementById('pa').value.trim()],b=idByLabel[document.getElementById('pb').value.trim()];
  cy.elements().removeClass('path').removeClass('pathn').removeClass('faded');
  if(!a||!b){narr.innerHTML='<span style="color:#fca5a5">起点/终点需为概念名称</span>';return;}
  const p=bfs(a,b);
  if(!p){narr.innerHTML='<span style="color:#fca5a5">'+labelById[a]+' → '+labelById[b]+'：无有向路径</span>';return;}
  const shown=[];
  for(let i=0;i<p.length;i++){const id=p[i];
    if(id.indexOf('HY_')===0){shown.push('⟦'+id.slice(3)+'⟧');continue;}
    if(id.indexOf('E_')===0){shown.push('—');continue;}
    shown.push(labelById[id]||id);
    const nx=p[i+1];
    if(nx&&nx.indexOf('HY_')!==0&&nx.indexOf('E_')!==0){
      const de=cy.edges('[source="'+id+'"][target="'+nx+'"]');
      if(de.length)shown.push('—'+(de.data('rel')||'→')+'→');
    }}
  cy.batch(()=>{p.forEach(id=>{const n=cy.$id(id);if(n.length&&n.isNode())n.addClass('pathn');});
    for(let i=0;i<p.length-1;i++){const e=cy.edges('[source="'+p[i]+'"][target="'+p[i+1]+'"]');if(e.length)e.addClass('path');}
    cy.elements().not(cy.$('.pathn,.path')).addClass('faded');});
  narr.innerHTML='有向链（'+p.length+' 步）：'+esc(shown.join(' '));
};
document.getElementById('clr').onclick=()=>{cy.elements().removeClass('path').removeClass('pathn').removeClass('faded');narrate();};
/* ---- 小地图 ---- */
const mc=document.getElementById('mc').getContext('2d');
function drawMini(){
  const W=352,H=248;mc.clearRect(0,0,W,H);
  if(!cy||!cy.nodes().length)return;
  const bb=cy.elements(':visible').boundingBox();
  if(!bb.w||!bb.h)return;
  const s=Math.min((W-16)/bb.w,(H-16)/bb.h),ox=(W-bb.w*s)/2-bb.x1*s,oy=(H-bb.h*s)/2-bb.y1*s;
  mc.fillStyle='rgba(255,255,255,.05)';mc.fillRect(0,0,W,H);
  cy.nodes(':visible').forEach(n=>{if(n.data('kind')==='sector')return;const p=n.position();
    mc.fillStyle=n.data('kind')==='hyper'?'#f59e0b':(n.data('color')||'#7dd3fc');
    mc.globalAlpha=(play.on&&n.hasClass('pending'))?.18:.9;
    mc.fillRect(p.x*s+ox-1.7,p.y*s+oy-1.7,3.4,3.4);});
  mc.globalAlpha=1;
  const e=cy.extent();
  mc.strokeStyle='#38bdf8';mc.lineWidth=1.4;
  mc.strokeRect(e.x1*s+ox,e.y1*s+oy,(e.x2-e.x1)*s,(e.y2-e.y1)*s);}
document.getElementById('mini').onclick=ev=>{
  const r=ev.currentTarget.getBoundingClientRect(),bb=cy.elements(':visible').boundingBox();
  const s=Math.min((352-16)/bb.w,(248-16)/bb.h),ox=(352-bb.w*s)/2-bb.x1*s,oy=(248-bb.h*s)/2-bb.y1*s;
  const x=((ev.clientX-r.left)*(352/r.width)-ox)/s,y=((ev.clientY-r.top)*(248/r.height)-oy)/s;
  cy.animate({center:{x:x,y:y}},{duration:200});};
/* ---- 导出 / 全屏 / 其余控件 ---- */
document.getElementById('png').onclick=()=>{const a=document.createElement('a');
  a.href=cy.png({full:true,scale:2,bg:'#070b12'});a.download='CQM_概念关系超图.png';a.click();};
document.getElementById('fs').onclick=()=>{const w=document.getElementById('wrap');
  if(document.fullscreenElement)document.exitFullscreen();else w.requestFullscreen&&w.requestFullscreen();};
document.getElementById('flt').onchange=applyVisibility;
document.getElementById('hy').onchange=applyVisibility;
document.getElementById('kg').onchange=()=>{applyVisibility();runLayout(document.getElementById('lay').value);};
document.getElementById('lbl').onchange=ev=>{cy.nodes().style('label',ev.target.checked?'data(label)':'');};
document.getElementById('q').oninput=applySearch;
document.getElementById('lay').onchange=ev=>runLayout(ev.target.value);
document.getElementById('reset').onclick=()=>runLayout(document.getElementById('lay').value);
window.addEventListener('resize',()=>{cy.resize();drawMini();});
cy.on('viewport',()=>drawMini());
cy.on('layoutstop',()=>drawMini());
narrate();
requestAnimationFrame(()=>{cy.resize();runLayout('clusters');narrate();drawMini();});
</script>
</body></html>"""


if __name__ == "__main__":
    main()
