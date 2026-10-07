# -*- coding: utf-8 -*-
"""
出口层 · 输出可视化展示
生成自包含（离线可用、无 CDN 依赖）的 HTML 网站与交互式超图，并汇总数据快照。
产出：
  10_输出可视化展示/网站/index.html
  10_输出可视化展示/网站/data.json
  10_输出可视化展示/交互式可视化/超图交互.html
  03_超图与理论图/超图可视化.html
  10_输出可视化展示/蓝图/index.html
运行：python build_site.py
"""
import csv
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S01 = os.path.join(ROOT, "01_结构化数据")
S03 = os.path.join(ROOT, "03_超图与理论图")
S04 = os.path.join(ROOT, "04_Lean对接")
S06 = os.path.join(ROOT, "06_动态机制")
S07 = os.path.join(ROOT, "07_经验检验")
S10 = os.path.join(ROOT, "10_输出可视化展示")


def rd(p, enc="utf-8-sig"):
    with open(p, "r", encoding=enc, newline="") as f:
        return list(csv.DictReader(f))


def build_data():
    concepts = rd(os.path.join(S01, "概念表.csv"))
    props = rd(os.path.join(S01, "命题表.csv"))
    args = rd(os.path.join(S01, "论证表.csv"))
    hg = json.load(open(os.path.join(S03, "超图数据.json"), encoding="utf-8"))
    lean_map = rd(os.path.join(S04, "Lean↔概念映射.csv"))
    modules = rd(os.path.join(S04, "Lean结构提取", "模块清单.csv"))
    dyn = json.load(open(os.path.join(S06, "仿真", "dynamic_hypergraph.json"), encoding="utf-8"))
    caus = json.load(open(os.path.join(S07, "因果模型", "GN_causal_dag.json"), encoding="utf-8"))
    onto = json.load(open(os.path.join(ROOT, "02_概念本体", "本体统计.json"), encoding="utf-8"))
    return {
        "concepts": concepts, "props": props, "args": args, "hypergraph": hg,
        "lean_map": lean_map, "lean_modules": modules, "dynamics": dyn["dynamics"],
        "elasticity": caus["elasticity"], "ontology": onto,
        "meta": {"nodes": len(concepts), "props": len(props), "args": len(args),
                 "hyperedges": len(hg["hyperedges"]), "edges": len(hg["directed_edges"]),
                 "modules": len(modules)},
    }


def write_site(data):
    d = os.path.join(S10, "网站")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    html = SITE_HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def write_hypergraph(data):
    html = HYPER_HTML.replace("__DATA__", json.dumps(data["hypergraph"], ensure_ascii=False))
    for path in [os.path.join(S10, "交互式可视化", "超图交互.html"),
                 os.path.join(S03, "超图可视化.html")]:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)


def write_blueprint_copy():
    src = os.path.join(S04, "蓝图", "index.html")
    d = os.path.join(S10, "蓝图")
    os.makedirs(d, exist_ok=True)
    if os.path.exists(src):
        shutil.copyfile(src, os.path.join(d, "index.html"))
    # leanblueprint 源（content 骨架）
    with open(os.path.join(d, "leanblueprint_source.md"), "w", encoding="utf-8") as f:
        f.write("""# leanblueprint 源文件说明

本目录的 `index.html` 为交互式蓝图（由 `_build/build_lean.py` 生成，离线自包含）。

若改用 leanblueprint 官方工具链，目录应含：

```text
10_输出可视化展示/蓝图/
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
    print("[OK] 网站/index.html, 交互式可视化/超图交互.html, 03/超图可视化.html, 蓝图/index.html")
    print("     meta:", data["meta"])
    print("     dynamics:", {k: v for k, v in data["dynamics"].items() if not isinstance(v, list)})


# ============================ 主站 HTML ============================
SITE_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CQM 理论组织与形式化框架 · 总览</title>
<style>
:root{--bg:#f6f8fb;--card:#fff;--ink:#1b2430;--mut:#5c6b7a;--line:#dae2ec;--acc:#2f6fb5;--hy:#b0552b;--ok:#2f7d4f;--gap:#b03434;--warn:#b8860b;}
*{box-sizing:border-box}html,body{margin:0}
body{background:var(--bg);color:var(--ink);font:14px/1.7 "Microsoft YaHei",system-ui,sans-serif}
header{background:linear-gradient(120deg,#22456b,#2f6fb5);color:#fff;padding:22px 26px}
header h1{margin:0 0 4px;font-size:20px}header .sub{opacity:.9;font-size:12.5px}
nav{display:flex;gap:2px;background:#fff;border-bottom:1px solid var(--line);padding:0 16px;position:sticky;top:0;z-index:9;flex-wrap:wrap}
nav button{border:0;background:none;padding:12px 15px;font:inherit;color:var(--mut);cursor:pointer;border-bottom:2px solid transparent}
nav button.on{color:var(--acc);border-bottom-color:var(--acc);font-weight:600}
main{max-width:1200px;margin:0 auto;padding:20px 22px 70px}
section{display:none}section.on{display:block}
h2{font-size:16px;color:#274766;margin:8px 0 12px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;margin-bottom:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.card b{display:block;font-size:24px;color:var(--acc);line-height:1.2}
.card span{color:var(--mut);font-size:12.5px}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:8px;overflow:hidden;font-size:13px}
th,td{padding:7px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{background:#eef3fb;color:#274766;position:sticky;top:0}
tr:hover td{background:#fbfdff}
code{background:#eef1f5;padding:1px 5px;border-radius:4px;font-family:Consolas,monospace;font-size:12.5px}
.tag{display:inline-block;padding:1px 7px;border-radius:10px;font-size:11.5px;margin:1px}
.t-ok{background:#e3f3ea;color:var(--ok)}.t-gap{background:#fdeaea;color:var(--gap)}.t-ax{background:#fdf3e0;color:var(--warn)}.t-neu{background:#eef1f5;color:var(--mut)}
.toolbar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px}
.toolbar input,.toolbar select{padding:6px 9px;border:1px solid var(--line);border-radius:7px;font:inherit;background:#fff}
.scroll{max-height:70vh;overflow:auto;border:1px solid var(--line);border-radius:8px}
.hint{color:var(--mut);font-size:12.5px;margin:6px 0 14px}
a{color:var(--acc)}
</style></head>
<body>
<header>
  <h1>CQM 理论组织与形式化框架</h1>
  <div class="sub">将 CQM 自然语言理论重构为可计算、可推理、可验证的结构化形式系统 · 外部理论文本不动 · 六维度</div>
</header>
<nav>
  <button class="on" data-t="ov">总览</button>
  <button data-t="con">概念（82）</button>
  <button data-t="prop">命题与缺口（63）</button>
  <button data-t="rel">关系与超边（70）</button>
  <button data-t="lean">Lean 对接</button>
  <button data-t="dyn">动态机制</button>
  <button data-t="meta">元数据</button>
</nav>
<main>
  <section id="ov" class="on">
    <h2>系统规模</h2>
    <div class="cards" id="ovcards"></div>
    <h2>六维度</h2>
    <table><thead><tr><th>#</th><th>维度</th><th>核心问题</th><th>目录</th><th>产物</th></tr></thead><tbody id="ovdim"></tbody></table>
    <h2>数据关系</h2>
    <p class="hint">概念以 <code>⇒</code>（重组实现，多因一果）构成有向超边；以 <code>→</code>（演化/映射/等价/依赖/层级含于）构成普通有向边。交互式超图见 <a href="../交互式可视化/超图交互.html">交互式可视化/超图交互.html</a>。</p>
  </section>

  <section id="con">
    <h2>概念表（82）</h2>
    <div class="toolbar"><input id="cq" placeholder="搜索名称/定义…">
      <select id="ct"></select></div>
    <div class="scroll"><table><thead><tr><th>ID</th><th>名称</th><th>类型</th><th>定义</th><th>出处</th><th>派生深度</th></tr></thead><tbody id="contb"></tbody></table></div>
  </section>

  <section id="prop">
    <h2>命题 / 定理 / 假设 / 构造 / 缺口</h2>
    <div class="toolbar"><input id="pq" placeholder="搜索陈述…"><select id="pt"></select></div>
    <div class="scroll"><table><thead><tr><th>ID</th><th>陈述</th><th>类型</th><th>状态</th><th>出处</th></tr></thead><tbody id="proptb"></tbody></table></div>
  </section>

  <section id="rel">
    <h2>论证 / 超边（70）</h2>
    <div class="toolbar"><select id="rt"></select></div>
    <div class="scroll"><table><thead><tr><th>ID</th><th>类型</th><th>前件</th><th>后件</th><th>概念链</th><th>出处</th></tr></thead><tbody id="reltb"></tbody></table></div>
  </section>

  <section id="lean">
    <h2>Lean ↔ 概念 ↔ 缺口</h2>
    <div class="scroll"><table><thead><tr><th>Lean 库</th><th>关键符号</th><th>概念</th><th>命题</th><th>缺口</th><th>说明</th></tr></thead><tbody id="leantb"></tbody></table></div>
    <h2>模块声明统计（自动抽取）</h2>
    <div class="scroll"><table><thead><tr><th>模块</th><th>文件</th><th>theorem/lemma</th><th>def</th><th>axiom</th><th>合计</th></tr></thead><tbody id="modtb"></tbody></table></div>
  </section>

  <section id="dyn">
    <h2>重写系统前向派生</h2>
    <div class="cards" id="dyncards"></div>
    <h2>$G_N$ 结构因果模型 · 对数弹性</h2>
    <table><thead><tr><th>因子</th><th>弹性</th></tr></thead><tbody id="eltb"></tbody></table>
  </section>

  <section id="meta">
    <h2>本体统计</h2>
    <table><thead><tr><th>项</th><th>值</th></tr></thead><tbody id="onttb"></tbody></table>
    <h2>数据下载</h2>
    <p class="hint">原始数据：<a href="data.json">data.json</a>（本页数据快照）。源 CSV/JSON/OWL 见各维度目录。</p>
  </section>
</main>
<script>
const D=__DATA__;
function el(id){return document.getElementById(id)}
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('nav button').forEach(x=>x.classList.remove('on'));
  document.querySelectorAll('section').forEach(x=>x.classList.remove('on'));
  b.classList.add('on'); el(b.dataset.t).classList.add('on');});
// 总览
const mv=D.meta;
el('ovcards').innerHTML=[['概念',mv.nodes],['命题/缺口',mv.props],['论证/超边',mv.args],
 ['超边 ⇒',mv.hyperedges],['有向边 →',mv.edges],['Lean 模块',mv.modules]].map(([k,v])=>`<div class="card"><b>${v}</b><span>${k}</span></div>`).join('');
const DIMS=[['1','结构化','理论由什么组成？','00–03','概念/命题/论证表、本体、超图'],
['2','ML 数据准备','机器如何读？','05','PyG/DGL 就绪、证明数据集 JSONL、嵌入就绪'],
['3','形式化验证','推理是否可靠？','04','Lean 结构提取、概念映射、蓝图'],
['4','动态机制','理论如何演化？','06','重写系统、状态模型、派生仿真'],
['5','经验检验','理论如何被检验？','07','因果模型、贝叶斯网络、实验设计'],
['6','元理论反思','本体论/认识论根基？','08','范畴论模型、类型论基础、哲学假设'],
['—','输出可视化展示','人如何看懂？','10','HTML 网站、交互超图、讲解']];
el('ovdim').innerHTML=DIMS.map(r=>`<tr><td>${r[0]}</td><td><b>${r[1]}</b></td><td>${r[2]}</td><td><code>${r[3]}</code></td><td>${r[4]}</td></tr>`).join('');
// 概念
const depthById={}; (D.dynamics.seed_concepts||[]).forEach(c=>depthById[c]=0);
const ctypes=[...new Set(D.concepts.map(c=>c.type))].sort();
el('ct').innerHTML='<option value="">全部类型</option>'+ctypes.map(t=>`<option>${t}</option>`).join('');
function renderCon(){
  const q=(el('cq').value||'').trim(), t=el('ct').value;
  el('contb').innerHTML=D.concepts.filter(c=>!t||c.type===t)
    .filter(c=>!q||c.name.includes(q)||c.definition.includes(q)||c.concept_id.includes(q))
    .map(c=>`<tr><td><code>${c.concept_id}</code></td><td>${c.name}</td><td><span class="tag t-neu">${c.type}</span></td><td>${c.definition}</td><td>${c.source_doc} ${c.source_loc}</td><td>${depthById[c.concept_id]??'—'}</td></tr>`).join('');
}
el('cq').oninput=renderCon; el('ct').onchange=renderCon; renderCon();
// 命题
const ptypes=[...new Set(D.props.map(p=>p.type))].sort();
el('pt').innerHTML='<option value="">全部类型</option>'+ptypes.map(t=>`<option>${t}</option>`).join('');
function renderProp(){
  const q=(el('pq').value||'').trim(), t=el('pt').value;
  el('proptb').innerHTML=D.props.filter(p=>!t||p.type===t).filter(p=>!q||p.statement.includes(q)||p.prop_id.includes(q))
   .map(p=>{let cls=p.status==='闭合'||p.status==='已证明'?'t-ok':(p.type==='缺口'?'t-gap':(p.status==='axiom'?'t-ax':'t-neu'));
    return `<tr><td><code>${p.prop_id}</code></td><td>${p.statement}</td><td>${p.type}</td><td><span class="tag ${cls}">${p.status}</span></td><td>${p.source_doc}</td></tr>`}).join('');
}
el('pq').oninput=renderProp; el('pt').onchange=renderProp; renderProp();
// 关系
const rtypes=[...new Set(D.args.map(a=>a.type))].sort();
el('rt').innerHTML='<option value="">全部关系</option>'+rtypes.map(t=>`<option>${t}</option>`).join('');
function renderRel(){
  const t=el('rt').value;
  el('reltb').innerHTML=D.args.filter(a=>!t||a.type===t)
   .map(a=>`<tr><td><code>${a.arg_id}</code></td><td><span class="tag ${a.type==='重组实现'?'t-hy t-neu':''}">${a.type}</span></td><td>${a.premises}</td><td>${a.conclusion}</td><td><code>${a.source_concept}</code></td><td>${a.source_doc}</td></tr>`).join('');
}
el('rt').onchange=renderRel; renderRel();
// Lean
el('leantb').innerHTML=D.lean_map.map(r=>{
  const gs=(r.gap_ids||'').split(';').filter(Boolean).map(g=>`<span class="tag t-gap">${g}</span>`).join('')||'—';
  return `<tr><td><code>${r.lean_library}</code></td><td><code>${r.lean_symbol}</code></td><td>${r.concept_ids}</td><td>${r.prop_ids}</td><td>${gs}</td><td>${r.remark}</td></tr>`}).join('');
el('modtb').innerHTML=D.lean_modules.filter(m=>m.total_decl>0).map(m=>
  `<tr><td><code>${m.module}</code></td><td>${m.file}</td><td>${m.theorem_like}</td><td>${m.def_like}</td><td>${m.axiom}</td><td>${m.total_decl}</td></tr>`).join('');
// 动态
const dy=D.dynamics;
el('dyncards').innerHTML=[['种子概念',dy.seed_concepts.length],['派生轮数',dy.steps],['触发规则',dy.fired_rules],
 ['可达概念',dy.reachable_concepts+'/82'],['最大深度',dy.max_depth],['不可达',dy.unreachable_concepts.length]]
 .map(([k,v])=>`<div class="card"><b>${v}</b><span>${k}</span></div>`).join('')
 +`<div class="card" style="grid-column:1/-1"><b style="font-size:14px">不可达概念</b><span>${dy.unreachable_concepts.join('、')}（依赖自环或须理论外输入）</span></div>`;
const E=D.elasticity;
el('eltb').innerHTML=['dlnGN/dlnI','dlnGN/dlnlambda_c','dlnGN/dlnc_1','dlnGN/dlnm_p','dlnGN/dlnkappa','dlnGN/dlntaiji']
 .map(k=>`<tr><td><code>${k.replace('dlnGN/dln','')}</code></td><td>${E[k]}</td></tr>`).join('');
// 元数据
const O=D.ontology;
el('onttb').innerHTML=Object.entries({'概念数':O.concept_count,'命题数':O.proposition_count,'论证数':O.argument_count,
 'OWL 类':O.owl_classes,'OWL 个体':O.owl_individuals,'OWL 对象属性':O.owl_object_properties,'跨类型边':O.cross_type_edges})
 .map(([k,v])=>`<tr><td>${k}</td><td>${v}</td></tr>`).join('');
</script>
</body></html>"""


# ============================ 交互式超图 ============================
HYPER_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CQM 概念关系超图 · 交互式</title>
<style>
*{box-sizing:border-box}html,body{margin:0;height:100%}
body{font:13px/1.6 "Microsoft YaHei",system-ui,sans-serif;background:#f6f8fb;color:#1b2430;display:flex;flex-direction:column}
header{background:#22456b;color:#fff;padding:12px 18px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
header h1{font-size:15px;margin:0}
header .sub{opacity:.85;font-size:12px}
.ctrl{display:flex;gap:8px;align-items:center;margin-left:auto;flex-wrap:wrap}
.ctrl select,.ctrl label{font-size:12.5px}
#wrap{flex:1;position:relative;overflow:hidden;background:#fff}
canvas{display:block;cursor:grab}
#tip{position:absolute;pointer-events:none;background:rgba(20,30,42,.94);color:#fff;padding:8px 11px;border-radius:8px;font-size:12.5px;max-width:320px;display:none;z-index:5;line-height:1.5}
#side{position:absolute;right:0;top:0;bottom:0;width:300px;background:#fff;border-left:1px solid #dae2ec;padding:14px 16px;overflow:auto;transform:translateX(100%);transition:.25s;z-index:6}
#side.on{transform:none}
#side h3{margin:0 0 6px;font-size:14px;color:#274766}
#side .k{color:#5c6b7a;font-size:12px}
#side table{width:100%;border-collapse:collapse;font-size:12.5px;margin-top:8px}
#side td{padding:4px 6px;border-bottom:1px solid #eef1f5;vertical-align:top}
.legend{display:flex;gap:10px;flex-wrap:wrap;font-size:12px;padding:8px 18px;background:#fff;border-top:1px solid #dae2ec}
.legend i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:4px;vertical-align:middle}
button.cls{border:0;background:#eef1f5;border-radius:6px;padding:4px 10px;font:inherit;cursor:pointer}
</style></head>
<body>
<header>
  <h1>CQM 概念关系超图</h1><span class="sub" id="stat"></span>
  <div class="ctrl">
    <label>关系 <select id="flt"><option value="">全部</option><option>重组实现</option><option>演化</option><option>映射</option><option>等价</option><option>依赖</option><option>层级含于</option></select></label>
    <label><input type="checkbox" id="lbl" checked> 标签</label>
    <label><input type="checkbox" id="hy" checked> 超边哑节点</label>
    <button class="cls" id="reset">重置布局</button>
  </div>
</header>
<div id="wrap">
  <canvas id="cv"></canvas>
  <div id="tip"></div>
  <div id="side"><button class="cls" onclick="closeSide()">关闭</button><div id="sidebody"></div></div>
</div>
<div class="legend" id="lg"></div>
<script>
const HG=__DATA__;
const TYPE_COLOR={本体论:'#c96a4b',理论框架:'#9b6ac9',数学结构:'#4f8fd0',群论:'#3f9d7a',关系类型:'#8a8f98',
 引力层级:'#c2a13a',纤维丛:'#7a6ad0',几何:'#39a0b0',量纲:'#b0603f',数论:'#2f9d5f',物理:'#3a72c0',共形场论:'#b35498'};
const NODES=HG.nodes, HY=HG.hyperedges, ED=HG.directed_edges;
document.getElementById('stat').textContent=`${NODES.length} 概念 · ${HY.length} 超边 ⇒ · ${ED.length} 有向边 →`;
document.getElementById('lg').innerHTML=Object.entries(TYPE_COLOR).map(([k,c])=>`<span><i style="background:${c}"></i>${k}</span>`).join('');
const cv=document.getElementById('cv'),ctx=cv.getContext('2d'),tip=document.getElementById('tip');
let W=0,H=0,DPR=window.devicePixelRatio||1;
function resize(){const w=cv.parentElement;W=w.clientWidth;H=w.clientHeight;cv.width=W*DPR;cv.height=H*DPR;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0)}
window.addEventListener('resize',()=>{resize();draw()});
// ---- 图模型 ----
const nodes=NODES.map((n,i)=>({...n,idx:i,x:Math.cos(i*2.399)*220+W/2,y:Math.sin(i*2.399)*220+H/2,vx:0,vy:0,deg:0}));
const id2i={};nodes.forEach(n=>id2i[n.id]=n.idx);
const hex=[]; // hyperedge hubs
HY.forEach((h,k)=>{const hy={id:h.id,x:0,y:0,vx:0,vy:0,members:[],deg:0};hex.push(hy)});
// 有向边
const dedges=[];
ED.forEach(e=>{const toks=[...new Set((e.source_concept||'').replace(/;/g,'→').split('→').map(s=>s.trim()).filter(s=>s.startsWith('C')))];if(toks.length>=2){const s=id2i[toks[0]],t=id2i[toks[toks.length-1]];if(s!=null&&t!=null){dedges.push({s,t,type:e.type,id:e.id,label:e.conclusion});nodes[s].deg++;nodes[t].deg++;}}});
// 超边成员
HY.forEach((h,k)=>{const toks=(h.source_concept||'').replace(/;/g,'→').split('→').map(s=>s.trim()).filter(s=>s.startsWith('C'));toks.forEach(t=>{if(id2i[t]!=null){hex[k].members.push(id2i[t]);nodes[id2i[t]].deg++;}});});
// 力导向（简化 velocity-Verlet）
let alpha=1;
function step(){
  const cx=W/2,cy=H/2;
  for(let iter=0;iter<2;iter++){
    for(const n of nodes){n.vx+=(cx-n.x)*0.0012*alpha;n.vy+=(cy-n.y)*0.0012*alpha;}
    // 斥力
    for(let i=0;i<nodes.length;i++)for(let j=i+1;j<nodes.length;j++){
      const a=nodes[i],b=nodes[j];let dx=b.x-a.x,dy=b.y-a.y;let d2=dx*dx+dy*dy+0.01;
      if(d2<62500){const f=900*alpha/d2;const d=Math.sqrt(d2);const ux=dx/d,uy=dy/d;a.vx-=ux*f;a.vy-=uy*f;b.vx+=ux*f;b.vy+=uy*f;}
    }
    // 弹簧（有向边）
    for(const e of dedges){const a=nodes[e.s],b=nodes[e.t];let dx=b.x-a.x,dy=b.y-a.y;let d=Math.hypot(dx,dy)||1;const f=(d-120)*0.02*alpha;a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;}
    // 超边：成员拉向中心 + 中心拉向成员质心
    for(const h of hex){if(!h.members.length)continue;let mx=0,my=0;for(const m of h.members){mx+=nodes[m].x;my+=nodes[m].y;}mx/=h.members.length;my/=h.members.length;
      h.vx+=(mx-h.x)*0.06*alpha;h.vy+=(my-h.y)*0.06*alpha;
      for(const m of h.members){const a=nodes[m];a.vx+=(h.x-a.x)*0.012*alpha;a.vy+=(h.y-a.y)*0.012*alpha;}}
  }
  for(const n of nodes){n.vx*=0.82;n.vy*=0.82;n.x+=n.vx;n.y+=n.vy;n.x=Math.max(30,Math.min(W-30,n.x));n.y=Math.max(30,Math.min(H-30,n.y));}
  for(const h of hex){h.vx*=0.82;h.vy*=0.82;h.x+=h.vx;h.y+=h.vy;}
  alpha*=0.995;if(alpha<0.02)alpha=0.02;
}
function visible(type){const f=document.getElementById('flt').value;return !f||type===f;}
function draw(){
  ctx.clearRect(0,0,W,H);
  const showHy=document.getElementById('hy').checked, showLbl=document.getElementById('lbl').checked;
  // 有向边
  for(const e of dedges){if(!visible(e.type))continue;const a=nodes[e.s],b=nodes[e.t];ctx.strokeStyle='#b9c4d0';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();arrow(a,b,'#9aa7b6');}
  // 超边
  if(showHy)for(const h of hex){for(const m of h.members){const a=nodes[m];ctx.strokeStyle='rgba(176,85,43,.35)';ctx.lineWidth=1.3;ctx.setLineDash([4,3]);ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(h.x,h.y);ctx.stroke();ctx.setLineDash([]);}
    ctx.fillStyle='#b0552b';ctx.beginPath();ctx.arc(h.x,h.y,3,0,7);ctx.fill();}
  // 节点
  for(const n of nodes){const r=4+Math.min(9,n.deg);ctx.beginPath();ctx.arc(n.x,n.y,r,0,7);ctx.fillStyle=TYPE_COLOR[n.type]||'#888';ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=1;ctx.stroke();
    if(showLbl){ctx.fillStyle='#35424f';ctx.font='11px "Microsoft YaHei"';ctx.fillText(n.label,n.x+r+2,n.y+3);}}
}
function arrow(a,b,c){const ang=Math.atan2(b.y-a.y,b.x-a.x);const L=9;ctx.fillStyle=c;const x=b.x-Math.cos(ang)*9,y=b.y-Math.sin(ang)*9;ctx.beginPath();ctx.moveTo(b.x-Math.cos(ang)*6,b.y-Math.sin(ang)*6);ctx.lineTo(x-Math.sin(ang)*4.5,y+Math.cos(ang)*4.5);ctx.lineTo(x+Math.sin(ang)*4.5,y-Math.cos(ang)*4.5);ctx.closePath();ctx.fill();}
// ---- 交互 ----
let drag=null,dragging=false;
function pick(x,y){for(const n of nodes){if((n.x-x)**2+(n.y-y)**2<(12+Math.min(9,n.deg))**2)return {t:'node',o:n};}
  for(const h of hex){if((h.x-x)**2+(h.y-y)**2<49)return {t:'hy',o:h};}return null;}
cv.addEventListener('mousedown',ev=>{drag=pick(ev.offsetX,ev.offsetY);dragging=!!drag;});
cv.addEventListener('mousemove',ev=>{const p=pick(ev.offsetX,ev.offsetY);cv.style.cursor=p?'pointer':'grab';
  if(drag){drag.o.x=ev.offsetX;drag.o.y=ev.offsetY;drag.o.vx=drag.o.vy=0;}
  if(p){tip.style.display='block';tip.style.left=(ev.offsetX+14)+'px';tip.style.top=(ev.offsetY+14)+'px';
    if(p.t==='node'){const n=p.o;tip.innerHTML=`<b>${n.label}</b> <span style="opacity:.7">${n.id}</span><br>类型：${n.type}<br>${n.definition}<br>度数：${n.deg}`;}
    else{const h=p.o;tip.innerHTML=`<b>超边 ${h.id}</b>（⇒ 重组实现）<br>成员 ${h.members.length} 个概念`;}}
  else tip.style.display='none';});
window.addEventListener('mouseup',()=>{if(drag&&!moved){openSide(drag.o);}drag=null;moved=false;});
let moved=false;cv.addEventListener('mousemove',()=>{if(drag)moved=true;});
cv.addEventListener('click',ev=>{const p=pick(ev.offsetX,ev.offsetY);if(p&&!moved)openSide(p.o);});
cv.addEventListener('wheel',ev=>{ev.preventDefault();alpha=Math.min(1,alpha+0.15);}, {passive:false});
function openSide(o){const s=document.getElementById('side'),b=document.getElementById('sidebody');s.classList.add('on');
  if(o.label!=null){const ins=dedges.filter(e=>e.s===o.idx||e.t===o.idx);
    b.innerHTML=`<h3>${o.label}</h3><div class="k">${o.id} · ${o.type}</div><div class="k" style="margin:6px 0">${o.definition}</div>
     <div class="k">出处：${o.source_doc} ${o.source_loc||''}</div>
     <table><tr><td class="k">出/入边</td><td>${ins.length}</td></tr></table>`;
  }else{b.innerHTML=`<h3>超边 ${o.id}</h3><div class="k">⇒ 重组实现 · 成员 ${o.members.length}</div><table>${o.members.map(m=>`<tr><td>${nodes[m].label}</td><td class="k">${nodes[m].id}</td></tr>`).join('')}</table>`;}}
function closeSide(){document.getElementById('side').classList.remove('on');}
document.getElementById('reset').onclick=()=>{alpha=1;nodes.forEach((n,i)=>{n.x=Math.cos(i*2.399)*240+W/2;n.y=Math.sin(i*2.399)*240+H/2;n.vx=n.vy=0;});};
document.getElementById('flt').onchange=draw;document.getElementById('lbl').onchange=draw;document.getElementById('hy').onchange=draw;
resize();
(function loop(){step();draw();requestAnimationFrame(loop)})();
</script>
</body></html>"""


if __name__ == "__main__":
    main()
