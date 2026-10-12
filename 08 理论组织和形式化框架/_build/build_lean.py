# -*- coding: utf-8 -*-
"""
维度 03 · 形式化验证（Lean 对接）
从 04_Lean对接/Lean源码/（Lean 4 项目）反向抽取声明与依赖，产出对接清单与蓝图。
产出（04_Lean对接/）：
  lean代码路径.yaml
  Lean结构提取/declarations.csv
  Lean结构提取/declarations.json
  Lean结构提取/模块清单.csv
  Lean结构提取/导入依赖.csv
  Lean结构提取/导入依赖.dot
  Lean↔概念映射.csv
  蓝图/蓝图.md
  蓝图/index.html
运行：python build_lean.py
"""
import csv
import json
import os
import re
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAN = os.path.join(ROOT, "04_Lean对接", "Lean源码")
S04 = os.path.join(ROOT, "04_Lean对接")
S01 = os.path.join(ROOT, "01_结构化数据")

DECL_KINDS = ["theorem", "lemma", "def", "abbrev", "axiom", "structure", "inductive",
              "class", "instance", "example", "opaque"]
DECL_RE = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)*(?:private\s+|protected\s+|noncomputable\s+|partial\s+|unsafe\s+|scoped\s+)*"
    r"(theorem|lemma|def|abbrev|axiom|structure|inductive|class|instance|example|opaque)\b\s*"
    r"([A-Za-z_][A-Za-z0-9_'.]*)", re.UNICODE)
IMPORT_RE = re.compile(r"^\s*import\s+([A-Za-z0-9_.]+)")
THEOREM_LIKE = {"theorem", "lemma", "example"}


def lean_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(LEAN):
        if ".lake" in dirpath.replace("\\", "/").split("/"):
            continue
        for fn in filenames:
            if fn.endswith(".lean"):
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


def module_of(path):
    rel = os.path.relpath(path, LEAN).replace("\\", "/")
    return rel[:-5].replace("/", ".")


def scan():
    decls, modules = [], []
    edges = []
    for path in lean_files():
        rel = os.path.relpath(path, LEAN).replace("\\", "/")
        mod = module_of(path)
        n_decl = collections.Counter()
        imports = []
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for ln, line in enumerate(f, 1):
                m = IMPORT_RE.match(line)
                if m:
                    imports.append(m.group(1))
                    continue
                if line.lstrip().startswith("--") or line.lstrip().startswith("/-"):
                    continue
                d = DECL_RE.match(line)
                if d:
                    kind, name = d.group(1), d.group(2)
                    decls.append({"module": mod, "file": rel, "line": ln, "kind": kind, "name": name})
                    n_decl[kind] += 1
        modules.append({
            "module": mod, "file": rel,
            "theorem_like": n_decl["theorem"] + n_decl["lemma"] + n_decl["example"],
            "def_like": n_decl["def"] + n_decl["abbrev"] + n_decl["opaque"],
            "axiom": n_decl["axiom"], "structure": n_decl["structure"] + n_decl["class"],
            "inductive": n_decl["inductive"], "instance": n_decl["instance"],
            "total_decl": sum(n_decl.values()),
        })
        for imp in imports:
            edges.append({"from": mod, "to": imp})
    return decls, modules, edges


def main():
    os.makedirs(os.path.join(S04, "Lean结构提取"), exist_ok=True)
    os.makedirs(os.path.join(S04, "蓝图"), exist_ok=True)
    decls, modules, edges = scan()

    # 只保留库内（CQM 自有）模块
    libs = sorted({m["module"].split(".")[0] for m in modules
                   if m["module"].split(".")[0] not in ("",)})
    internal = {m["module"] for m in modules}
    edges_int = [e for e in edges if e["to"] in internal or any(e["to"].startswith(l + ".") for l in libs)]

    with open(os.path.join(S04, "Lean结构提取", "declarations.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["module", "file", "line", "kind", "name"])
        w.writeheader()
        w.writerows(decls)
    with open(os.path.join(S04, "Lean结构提取", "declarations.json"), "w", encoding="utf-8") as f:
        json.dump(decls, f, ensure_ascii=False, indent=1)
    with open(os.path.join(S04, "Lean结构提取", "模块清单.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(modules[0].keys()))
        w.writeheader()
        w.writerows(modules)
    with open(os.path.join(S04, "Lean结构提取", "导入依赖.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["from", "to"])
        w.writeheader()
        w.writerows(edges)

    # 依赖 dot（仅库内边）
    with open(os.path.join(S04, "Lean结构提取", "导入依赖.dot"), "w", encoding="utf-8") as f:
        f.write('digraph LeanImports {\n  rankdir=LR; node [shape=box, style=rounded, fontname="Consolas", fontsize=9];\n')
        for e in edges_int:
            f.write(f'  "{e["from"]}" -> "{e["to"]}";\n')
        f.write("}\n")

    # ---- lean代码路径.yaml ----
    toolchain = open(os.path.join(LEAN, "lean-toolchain"), encoding="utf-8").read().strip()
    lf = open(os.path.join(LEAN, "lakefile.toml"), encoding="utf-8").read()
    ver = re.search(r'version\s*=\s*"([^"]+)"', lf)
    targets = re.search(r'defaultTargets\s*=\s*\[([^\]]+)\]', lf)
    kinds_total = collections.Counter(d["kind"] for d in decls)
    yaml = []
    yaml.append("# CQM Lean 4 形式化项目路径与结构记录")
    yaml.append("# 由 _build/build_lean.py 自动生成；权威状态见 08 理论组织和形式化框架/04_Lean对接/Lean源码/README.md")
    yaml.append("project:")
    yaml.append("  name: CQMFormal")
    yaml.append(f'  root: "08 理论组织和形式化框架/04_Lean对接/Lean源码"')
    yaml.append(f'  version: "{ver.group(1) if ver else ""}"')
    yaml.append(f'  toolchain: "{toolchain}"')
    yaml.append("  build_command: lake build")
    tg = targets.group(1) if targets else ""
    libs_list = [t.strip().strip('"') for t in tg.split(",")] if tg else libs
    yaml.append("  libraries:")
    for l in libs_list:
        yaml.append(f"    - name: {l}")
    yaml.append("  modules:")
    for m in modules:
        yaml.append(f'    - {{module: "{m["module"]}", file: "{m["file"]}", '
                    f'theorem_like: {m["theorem_like"]}, def_like: {m["def_like"]}, '
                    f'axiom: {m["axiom"]}, total_decl: {m["total_decl"]}}}')
    yaml.append("  declaration_histogram:")
    for k in DECL_KINDS:
        if kinds_total.get(k):
            yaml.append(f"    {k}: {kinds_total[k]}")
    yaml.append("  totals:")
    yaml.append(f"    modules: {len(modules)}")
    yaml.append(f"    declarations: {len(decls)}")
    yaml.append(f"    theorem_like: {kinds_total['theorem'] + kinds_total['lemma'] + kinds_total['example']}")
    yaml.append(f"    axioms: {kinds_total['axiom']}")
    yaml.append("  authoritative_status:")
    yaml.append('    note: "编译状态与定理计数以 08 理论组织和形式化框架/04_Lean对接/Lean源码/README.md 为权威：8 库通过、3 库部分通过；748 已证明定理 / 30 公理待证。"')
    with open(os.path.join(S04, "lean代码路径.yaml"), "w", encoding="utf-8") as f:
        f.write("\n".join(yaml) + "\n")

    # ---- Lean↔概念映射（人工审定） ----
    MAPPING = [
        # lean_module, lean_symbol, concept_ids, prop_ids, gap_ids, note
        ("CausalSet", "CausalSet/Axioms", "C004;C002;C003", "P002", "H3.1;H3.2;C", "因果集公理；缺口 C 以 Lean 公理 H3.3 承载"),
        ("CouplingSpace", "Basis", "C060;C061;C062", "P005", "", "耦合空间 u=ln r 与正则对易关系"),
        ("CartanAlgebra", "cartanA4", "C053;C054;C055;C056", "P001;P017", "", "A₄ 嘉当矩阵、本征值精确表达式、Dynkin 指数比"),
        ("SpectralGeometry", "spectralQuantum", "C048;C047;C043;C044;C045;C046;C049", "P004;P015", "G002;G003;G004", "相变量子 ☯、Sierra-CQM 耦谱、黎曼 ξ、谱算符"),
        ("SpectralGeometry", "MathieuContinuedFraction", "C057", "P010", "G005", "Mathieu 临界 λ_c（连分数唯一根）"),
        ("PrimeGeometry", "Basic", "C010", "P004", "", "质数前网络与因果时几何（多边形/弧段/位置）"),
        ("Decoherence", "Basic;DeepCoupling", "C008;C005;C006;C019", "P009;P011;P012", "", "退相干三层结构、跨层级深耦合与唯一性"),
        ("PhysicalConstants", "gn_spectral_formula", "C081", "P010;P032", "", "G_N 谱公式与 α⁻¹_SU(5)（构造后验数字校验，待独立复现）"),
        ("Methodology", "Basic", "C007", "P009;P022;P023", "", "涌现逻辑结构、庸俗隐变量分解对比（公理为主）"),
        ("Superconductivity", "TransitionTemperatureCQM", "C070;C069;C067", "P026;P027", "G22", "CQM 临界温度严格推导"),
        ("Superconductivity", "BCSIntegralAsymptotic", "C070", "P027", "G13", "BCS 积分 tanh→对数渐近（G13 闭合）"),
        ("Superconductivity", "MolecularGeometry", "C028;C026;C029", "P028", "G20-ext;N2;N3", "分子几何→晶胞嘉当矩阵→Regge 角亏"),
        ("Superconductivity", "ElementCartan", "C030;C026", "P028;P029", "G16", "元素嘉当矩阵；因果分辨率形式化为 def 占位"),
        ("Superconductivity", "TestDet", "C029", "P027", "G14", "中子缺陷谱判据 det D=8-3δ²（G14 闭合）"),
        ("Superconductivity", "SPAF", "C029;C026", "P011", "N1;N2", "SPAF 半唯像框架（neutronDefect）"),
        ("FGChain", "FiberBundle", "C020;C021;C022;C023;C024", "P024", "", "离散主丛（重组实现 F=G⇒R=G⇒Ĥ、和乐平庸化）"),
        ("FGChain", "SyncOperator", "C012;C046", "P024", "G002;G003;G004", "同步算符→零点谱→耦级 𝔠_n"),
        ("FGChain", "CurvatureOperator", "C060;C061;C062", "P007", "", "曲率算符（海森堡对 [û,p̂_u]=i）"),
        ("FGChain", "Observable", "C063;C070", "P007;P026", "", "实验可观测：壳层容量、跃迁耦级谱 Δu_n=2ln n、BCS T_c"),
        ("FGChain", "Hierarchy", "C073;C012", "P028", "H3.1;H3.2;H3.3", "FG 层级化与紧化算符"),
        ("GN", "TripleIdentity", "C048;C047", "P015", "", "三重恒等 ☯=λ_1=-B、闭式表达式"),
        ("GN", "SierraCQM", "C057;C046", "P010", "", "Sierra-CQM 条件性渐近、零点匹配、偏差界"),
        ("GN", "SimplexSpectrum", "C055;C053", "P001", "", "4-单纯形边-面矩阵谱 {9¹4⁴1⁵} 严格化（57 定理）"),
        ("GN", "AdeleJacobian", "C058", "P010", "", "Adele Jacobian 因子 2、exp(-2/☯)"),
        ("GN", "Constructions", "C058;C081", "P010", "", "κ=(31+☯)/30 组合-谱连接、全因子正性"),
    ]
    with open(os.path.join(S04, "Lean↔概念映射.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["lean_library", "lean_symbol", "concept_ids", "prop_ids", "gap_ids", "remark"])
        w.writerows(MAPPING)

    # ---- 蓝图 ----
    build_mapping_cp = {r[0] for r in MAPPING}
    bp_md = ["# CQM 形式化蓝图（Lean ↔ 概念 ↔ 缺口）", "",
             "> 由 `_build/build_lean.py` 从 Lean 源码抽取与人工审定的映射生成。",
             "> 节点 = CoreQM 概念 / 命题 / 缺口；链接 = Lean 库/符号。状态以 `08 理论组织和形式化框架/04_Lean对接/Lean源码/README.md` 为权威。", "",
             "## 一、库—概念—缺口对照", "",
             "| Lean 库 | 关键符号 | 概念 | 命题 | 缺口 | 说明 |",
             "|:---|:---|:---|:---|:---|:---|"]
    for lib, sym, cs, ps, gs, note in MAPPING:
        bp_md.append(f"| `{lib}` | `{sym}` | {cs} | {ps} | {gs or '—'} | {note} |")
    bp_md += ["", "## 二、缺口 ↔ Lean 状态", "",
              "| 缺口 | Lean 对应 | 状态 |", "|:---|:---|:---|",
              "| C | `CausalSet/Axioms`（公理 H3.3） | 公理承载 |",
              "| G2–G4 | `FGChain/SyncOperator`、`GN` | 部分（算子/谱结构） |",
              "| G13 | `Superconductivity/BCSIntegralAsymptotic` | 闭合（`bcsTcFromIntegral_solved`） |",
              "| G14 | `Superconductivity/TestDet` | 闭合 |",
              "| G20-ext | `Superconductivity/MolecularGeometry` | 闭合（不属缺口表） |",
              "| N1–N3 | `Superconductivity/SPAF`、`MolecularGeometry` | 待证明 |",
              "| N4 | `FGChain/` | 待证明（多数模块不通过） |",
              "| H3.1–H3.3 | `CausalSet/Axioms`、`FGChain/Hierarchy` | `axiom` |", "",
              "## 三、声明统计（自动抽取）", "",
              f"- 模块数：{len(modules)}；声明总数：{len(decls)}",
              f"- theorem/lemma/example：{kinds_total['theorem'] + kinds_total['lemma'] + kinds_total['example']}",
              f"- axiom：{kinds_total['axiom']}；def/abbrev：{kinds_total['def'] + kinds_total['abbrev']}"]
    with open(os.path.join(S04, "蓝图", "蓝图.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(bp_md) + "\n")

    build_blueprint_html(MAPPING, modules, decls, os.path.join(S04, "蓝图", "index.html"))

    print(f"[OK] modules={len(modules)} decls={len(decls)} mapping={len(MAPPING)}")
    print("     kinds:", dict(kinds_total))


def build_blueprint_html(MAPPING, modules, decls, out):
    kind_hist = {}
    for d in decls:
        kind_hist[d["kind"]] = kind_hist.get(d["kind"], 0) + 1
    axiom_decls = [{"module": d["module"], "file": d["file"], "line": d["line"], "name": d["name"]}
                   for d in decls if d["kind"] == "axiom"]
    mapped_concepts = sorted({c.strip() for m in MAPPING
                              for c in (m[2] or "").split(";") if re.match(r"^C\d{3}$", c.strip())})
    payload = {"mapping": MAPPING, "modules": modules, "n_decl": len(decls),
               "kind_hist": kind_hist, "axiom_decls": axiom_decls,
               "mapped_concepts": mapped_concepts}
    html = BP_HTML_TMPL.replace("__DATA__", json.dumps(payload, ensure_ascii=False))
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)


BP_HTML_TMPL = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CQM 形式化蓝图 · Lean ↔ 概念 ↔ 缺口</title>
<style>
:root{--bg:#f6f8fc;--card:#fff;--ink:#1c2530;--mut:#5d6b7a;--line:#d8e0ea;--acc:#2f6fb5;--hy:#b0552b;
--ok:#2f7d4f;--warn:#b8860b;--gap:#b03434;
--k-theorem:#2f6fb5;--k-lemma:#6aa9f0;--k-def:#7c6cf0;--k-structure:#ec4899;--k-axiom:#d97706;
--k-inductive:#10b981;--k-class:#eab308;--k-abbrev:#94a3b8}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.65 "Microsoft YaHei",system-ui,sans-serif}
header{background:linear-gradient(120deg,#22456b,#2f6fb5);color:#fff;padding:20px 26px}
h1{margin:0 0 4px;font-size:19px}.sub{opacity:.9;font-size:12.5px}
.wrap{max-width:1220px;margin:0 auto;padding:20px 24px 70px}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden;font-size:13px}
th,td{padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left}
th{background:#eef3fb;color:#274766;font-weight:600;position:sticky;top:0}
tr:hover td{background:#fbfdff}
code{background:#eef1f5;color:var(--ink);padding:1px 5px;border-radius:4px;font-family:Consolas,monospace;font-size:12.5px}
.tag{display:inline-block;padding:1px 7px;border-radius:10px;font-size:11.5px;margin:1px}
.t-ok{background:#e3f3ea;color:var(--ok)}.t-gap{background:#fdeaea;color:var(--gap)}.t-ax{background:#fdf3e0;color:var(--warn)}
.stats{display:flex;gap:12px;flex-wrap:wrap;margin:16px 0 18px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 16px;min-width:126px;
box-shadow:0 4px 14px rgba(34,69,107,.06)}
.stat b{display:block;font-size:23px;color:var(--acc);font-variant-numeric:tabular-nums}
.stat span{color:var(--mut);font-size:12px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px;margin-bottom:6px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;box-shadow:0 4px 14px rgba(34,69,107,.06)}
.card h3{margin:0 0 10px;font-size:13.5px;color:#274766}
h2{font-size:16px;margin:26px 0 10px;color:#274766}
.hint{color:var(--mut);font-size:12px;margin-top:8px}
.kbar{display:flex;height:26px;border-radius:7px;overflow:hidden;border:1px solid var(--line)}
.kbar i{display:block;height:100%}
.kleg{display:flex;flex-wrap:wrap;gap:5px 14px;margin-top:9px;font-size:12px;color:var(--mut)}
.kleg i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px;vertical-align:-1px}
.band{display:flex;align-items:center;gap:8px;margin-bottom:5px;font-size:12px}
.band .bn{width:230px;flex:0 0 230px;text-align:right;color:#3b4a5c;font-family:Consolas,monospace;font-size:11.5px;
white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.band .bt{flex:1;display:flex;height:14px;border-radius:4px;overflow:hidden;background:#eef2f7}
.band .bt i{display:block;height:100%}
.band .bv{width:38px;text-align:right;color:var(--mut);font-variant-numeric:tabular-nums}
.axlist{max-height:184px;overflow:auto;font-size:12.5px;border:1px solid var(--line);border-radius:8px}
.axlist div{padding:4px 9px;border-bottom:1px solid #eef2f7}
.axlist code{background:#fdf3e0}
.toolbar{display:flex;gap:8px;margin-bottom:9px}
.toolbar input{padding:7px 11px;border:1px solid var(--line);border-radius:8px;font:inherit;min-width:250px}
svg text.num{font-variant-numeric:tabular-nums}
@media print{.toolbar{display:none}body{background:#fff}}
</style></head><body>
<header><h1>CQM 形式化蓝图</h1>
<div class="sub">Lean 4 形式化项目 ↔ 概念表 ↔ 缺口台账 · 状态以 <code>08 理论组织和形式化框架/04_Lean对接/Lean源码/README.md</code> 为权威</div></header>
<div class="wrap">
<div class="stats" id="stats"></div>
<div class="grid">
  <div class="card"><h3>形式化映射覆盖（Lean↔概念映射）</h3><div id="ring"></div></div>
  <div class="card"><h3>声明构成（自动抽取 8 类）</h3><div id="kbar" class="kbar"></div><div class="kleg" id="kleg"></div>
    <div class="hint" id="knote"></div></div>
  <div class="card"><h3 id="axt">公理（axiom）声明 · 待证焦点</h3><div class="axlist" id="axl"></div>
    <div class="hint" id="axnote"></div></div>
</div>
<h2>一、模块声明色带（按声明总数排序）</h2>
<div id="bands"></div>
<h2>二、库—概念—缺口对照</h2>
<div class="toolbar"><input id="q1" placeholder="搜索库 / 符号 / 概念 / 缺口…"></div>
<table id="t1"><thead><tr><th>Lean 库</th><th>关键符号</th><th>概念</th><th>命题</th><th>缺口</th><th>说明</th></tr></thead><tbody></tbody></table>
<h2>三、模块声明统计（自动抽取）</h2>
<div class="toolbar"><input id="q2" placeholder="搜索模块 / 文件…"></div>
<table id="t2"><thead><tr><th>模块</th><th>文件</th><th>theorem/lemma</th><th>def</th><th>axiom</th><th>structure</th><th>合计</th></tr></thead><tbody></tbody></table>
</div>
<script>
const D=__DATA__;
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const gapSplit=s=>s?s.split(';').filter(Boolean):[];
const KC={theorem:'var(--k-theorem)',lemma:'var(--k-lemma)',def:'var(--k-def)',structure:'var(--k-structure)',
 axiom:'var(--k-axiom)',inductive:'var(--k-inductive)',class:'var(--k-class)',abbrev:'var(--k-abbrev)',
 theorem_like:'var(--k-theorem)',def_like:'var(--k-def)',instance:'var(--k-abbrev)'};
const totalOf=D.n_decl;
const thLike=(D.kind_hist.theorem||0)+(D.kind_hist.lemma||0);
const mappedN=D.mapped_concepts.length,gapsN=new Set(D.mapping.flatMap(m=>gapSplit(m[4]))).size;
document.getElementById('stats').innerHTML=[
 ['模块数',D.modules.length],['声明总数',totalOf],
 ['theorem/lemma',thLike],['axiom（抽取）',D.kind_hist.axiom||0],
 ['映射概念',mappedN+'/82'],['缺口映射',gapsN+'/24']
].map(([k,v])=>'<div class="stat"><b>'+v+'</b><span>'+k+'</span></div>').join('');
/* 覆盖率环 */
(function(){
 const pct=mappedN/82,r=54,cx=74,cy=74,C=2*Math.PI*r,off=C*(1-mappedN/82);
 document.getElementById('ring').innerHTML=
 '<svg width="148" height="148" viewBox="0 0 148 148">'+
 '<defs><linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2f6fb5"/>'+
 '<stop offset="1" stop-color="#7c6cf0"/></linearGradient></defs>'+
 '<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="none" stroke="#e8eef6" stroke-width="16"/>'+
 '<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="none" stroke="url(#g1)" stroke-width="16" stroke-linecap="round"'+
 ' stroke-dasharray="'+C+'" stroke-dashoffset="'+off+'" transform="rotate(-90 '+cx+' '+cy+')">'+
 '<title>映射概念 '+mappedN+'/82</title></circle>'+
 '<text x="'+cx+'" y="'+(cy+2)+'" text-anchor="middle" font-size="24" font-weight="600" fill="#2f6fb5" class="num">'+mappedN+'/82</text>'+
 '<text x="'+cx+'" y="'+(cy+22)+'" text-anchor="middle" font-size="11.5" fill="#5d6b7a">概念已映射 · '+(pct*100).toFixed(1)+'%</text></svg>'+
 '<div class="hint">映射源：<code>04_Lean对接/Lean↔概念映射.csv</code>（25 条）；<b>'+(mappedN===41?'计算值 41/82 与组织层 README 权威口径 41/82（50.0%）一致':'计算值 '+mappedN+'/82 与权威口径 41/82 不一致——以权威源为准')+'</b>。</div>';
})();
/* 声明构成条 */
(function(){
 const ks=Object.entries(D.kind_hist).sort((a,b)=>b[1]-a[1]);
 document.getElementById('kbar').innerHTML=ks.map(([k,n])=>
  '<i style="width:'+(n/totalOf*100)+'%;background:'+(KC[k]||'#94a3b8')+'"><title>'+esc(k)+'：'+n+'</title></i>').join('');
 document.getElementById('kleg').innerHTML=ks.map(([k,n])=>
  '<span><i style="background:'+(KC[k]||'#94a3b8')+'"></i>'+esc(k)+' '+n+'</span>').join('');
 document.getElementById('knote').textContent='合计 '+totalOf+' 条声明（'+D.modules.length+' 模块，源码自动扫描）。';
})();
/* axiom 焦点 */
(function(){
 const ax=D.axiom_decls||[];
 document.getElementById('axt').textContent='公理（axiom）声明 · 待证焦点（'+ax.length+' 条）';
 document.getElementById('axl').innerHTML=ax.length?ax.map(a=>
  '<div><code>'+esc(a.name)+'</code> <span style="color:#5d6b7a">'+esc(a.file)+':'+a.line+'</span></div>').join('')
  :'<div>无</div>';
 document.getElementById('axnote').innerHTML='抽取自源码的 <code>axiom</code> 声明共 '+ax.length+
  ' 条；权威 <code>Lean源码/README.md</code> 记「30 公理待证」（转引自建设报告）——两口径并列登记，不擅自统一。';
})();
/* 模块色带 top18 */
(function(){
 const rows=D.modules.filter(m=>+m.total_decl>0).slice().sort((a,b)=>(+b.total_decl)-(+a.total_decl)).slice(0,18);
 const max=Math.max(...rows.map(r=>+r.total_decl),1);
 document.getElementById('bands').innerHTML=rows.map(m=>{
  const parts=[['theorem_like',m.theorem_like],['def_like',m.def_like],['structure',m.structure],
   ['inductive',m.inductive],['axiom',m.axiom],['instance',m.instance]];
  const seg=parts.filter(p=>+p[1]>0).map(p=>
   '<i style="width:'+(+p[1]/max*100)+'%;background:'+(KC[p[0]]||'#94a3b8')+'" title="'+esc(p[0])+'：'+p[1]+'"></i>').join('');
  return '<div class="band"><span class="bn" title="'+esc(m.module)+'">'+esc(m.module)+'</span>'+
   '<span class="bt">'+seg+'</span><span class="bv">'+m.total_decl+'</span></div>';}).join('')
   ||'<div class="hint">无</div>';
})();
/* 对照表（可筛） */
function renderT1(){
 const q=(document.getElementById('q1').value||'').toLowerCase();
 const rows=D.mapping.filter(m=>!q||m.join(' ').toLowerCase().includes(q));
 document.querySelector('#t1 tbody').innerHTML=rows.map(m=>{
  const gs=gapSplit(m[4]).map(g=>'<span class="tag t-gap">'+esc(g)+'</span>').join('')||'—';
  const cs=(m[2]||'').split(';').filter(Boolean).map(c=>'<span class="tag">'+esc(c)+'</span>').join('');
  return '<tr><td><code>'+esc(m[0])+'</code></td><td><code>'+esc(m[1])+'</code></td><td>'+cs+'</td>'+
   '<td>'+esc(m[3]||'—')+'</td><td>'+gs+'</td><td>'+esc(m[5])+'</td></tr>';}).join('')
  ||'<tr><td colspan="6">无匹配</td></tr>';
}
document.getElementById('q1').oninput=renderT1;renderT1();
/* 模块统计（按合计降序 + 可筛） */
function renderT2(){
 const q=(document.getElementById('q2').value||'').toLowerCase();
 const rows=D.modules.filter(m=>+m.total_decl>0&&(!q||(m.module+' '+m.file).toLowerCase().includes(q)))
  .slice().sort((a,b)=>(+b.total_decl)-(+a.total_decl));
 document.querySelector('#t2 tbody').innerHTML=rows.map(m=>{
  const w=Math.round((+m.total_decl)/Math.max(...D.modules.map(x=>+x.total_decl),1)*100);
  return '<tr><td><code>'+esc(m.module)+'</code></td><td>'+esc(m.file)+'</td><td>'+m.theorem_like+'</td>'+
   '<td>'+m.def_like+'</td><td>'+(+m.axiom?'<span class="tag t-ax">'+m.axiom+'</span>':m.axiom)+'</td>'+
   '<td>'+m.structure+'</td><td>'+m.total_decl+
   ' <span style="display:inline-block;width:70px;height:7px;background:#eef2f7;border-radius:4px;vertical-align:middle">'+
   '<span style="display:block;height:7px;width:'+w+'%;background:#2f6fb5;border-radius:4px"></span></span></td></tr>';}).join('')
  ||'<tr><td colspan="7">无匹配</td></tr>';
}
document.getElementById('q2').oninput=renderT2;renderT2();
</script></body></html>"""


if __name__ == "__main__":
    main()
