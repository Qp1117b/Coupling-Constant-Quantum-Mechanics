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
    html = BP_HTML_TMPL.replace("__DATA__", json.dumps(
        {"mapping": MAPPING, "modules": modules, "n_decl": len(decls)}, ensure_ascii=False))
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)


BP_HTML_TMPL = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CQM 形式化蓝图 · Lean ↔ 概念 ↔ 缺口</title>
<style>
:root{--bg:#f7f9fc;--card:#fff;--ink:#1c2530;--mut:#5d6b7a;--line:#d8e0ea;--acc:#2f6fb5;--hy:#b0552b;--ok:#2f7d4f;--warn:#b8860b;}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.65 "Microsoft YaHei",system-ui,sans-serif}
header{background:#fff;border-bottom:1px solid var(--line);padding:18px 24px}
h1{margin:0 0 4px;font-size:19px}.sub{color:var(--mut);font-size:12.5px}
.wrap{max-width:1180px;margin:0 auto;padding:20px 24px 60px}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden;font-size:13px}
th,td{padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left}
th{background:#eef3fb;color:#274766;font-weight:600;position:sticky;top:0}
tr:hover td{background:#fbfdff}
code{background:#eef1f5;padding:1px 5px;border-radius:4px;font-family:Consolas,monospace;font-size:12.5px}
.tag{display:inline-block;padding:1px 7px;border-radius:10px;font-size:11.5px;margin:1px}
.t-ok{background:#e3f3ea;color:var(--ok)}.t-gap{background:#fdeaea;color:#b03434}.t-ax{background:#fdf3e0;color:var(--warn)}
.stats{display:flex;gap:14px;flex-wrap:wrap;margin:14px 0 22px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 18px;min-width:120px}
.stat b{display:block;font-size:22px;color:var(--acc)}
h2{font-size:16px;margin:26px 0 10px;color:#274766}
</style></head><body>
<header><h1>CQM 形式化蓝图</h1>
<div class="sub">Lean 4 形式化项目 ↔ 概念表 ↔ 缺口台账 · 状态以 <code>08 理论组织和形式化框架/04_Lean对接/Lean源码/README.md</code> 为权威</div></header>
<div class="wrap">
<div class="stats" id="stats"></div>
<h2>一、库—概念—缺口对照</h2>
<table id="t1"><thead><tr><th>Lean 库</th><th>关键符号</th><th>概念</th><th>命题</th><th>缺口</th><th>说明</th></tr></thead><tbody></tbody></table>
<h2>二、模块声明统计（自动抽取）</h2>
<table id="t2"><thead><tr><th>模块</th><th>文件</th><th>theorem/lemma</th><th>def</th><th>axiom</th><th>structure</th><th>合计</th></tr></thead><tbody></tbody></table>
</div>
<script>
const D=__DATA__;
const gapSplit=s=>s?s.split(';').filter(Boolean):[];
document.getElementById('stats').innerHTML=[
 ['模块数',D.modules.length],['声明总数',D.n_decl],
 ['映射条目',D.mapping.length],
 ['缺口映射',new Set(D.mapping.flatMap(m=>gapSplit(m[4]))).size]
].map(([k,v])=>`<div class="stat"><b>${v}</b>${k}</div>`).join('');
document.querySelector('#t1 tbody').innerHTML=D.mapping.map(m=>{
 const gs=gapSplit(m[4]).map(g=>`<span class="tag t-gap">${g}</span>`).join('')||'—';
 return `<tr><td><code>${m[0]}</code></td><td><code>${m[1]}</code></td><td>${m[2]}</td><td>${m[3]}</td><td>${gs}</td><td>${m[5]}</td></tr>`;}).join('');
document.querySelector('#t2 tbody').innerHTML=D.modules.map(m=>
 `<tr><td><code>${m.module}</code></td><td>${m.file}</td><td>${m.theorem_like}</td><td>${m.def_like}</td><td>${m.axiom}</td><td>${m.structure}</td><td>${m.total_decl}</td></tr>`).join('');
</script></body></html>"""


if __name__ == "__main__":
    main()
