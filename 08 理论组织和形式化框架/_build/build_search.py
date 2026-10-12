# -*- coding: utf-8 -*-
"""
维度 7 · 检索台（Retrieval Console）

一份离线自包含的检索前端，背后是三套真实索引：
  1. 知识图谱检索：82 概念 + 39 命题 + 24 缺口，字段过滤（kind/type/status/doc/code）+ 别名命中
  2. 全文检索：17,519 句原文，**BM25 排序** + CJK 二元切分（Lucene CJKAnalyzer 同款思路）+
     引号短语 + +/- 必含排除 + doc: 字段限定；语料以 gzip+base64 内嵌，浏览器用 DecompressionStream 解压
  3. 证据检索：215 条证据映射 → 引文、章节、字符区间、定位方法与置信度，一键定位回原文

另附「能力问答」页：把 build_kg.py 跑出的 SPARQL 结果（CQ1–CQ9）直接呈现，证明图谱可被标准查询语言消费。

产出：10_展示可视化/源_可视化/检索台/index.html（自包含，无 CDN）
运行：python build_search.py
"""
import base64
import csv
import gzip
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S00, S01, S02, S03, S05, S10 = (os.path.join(ROOT, x) for x in
                                ("00_外部引用", "01_结构化数据", "02_概念本体", "03_超图与理论图",
                                 "05_机器学习数据准备", "10_展示可视化"))


def jload(p):
    with io.open(p, encoding="utf-8") as f:
        return json.load(f)


def rd(name, base):
    with io.open(os.path.join(base, name), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def build_payload():
    kg = jload(os.path.join(S03, "知识图谱.json"))
    ev = jload(os.path.join(S00, "证据映射.json"))
    docs = rd("语料清单.csv", S00)
    sents = []
    with io.open(os.path.join(S00, "句索引", "句索引.jsonl"), encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                sents.append([r["doc_id"], r["sid"], r["kind"], r["text"]])
    aliases = {}
    for r in rd("概念别名表.csv", S01):
        aliases.setdefault(r["concept_id"], []).append(r["alias"])
    lean = {}
    for r in rd("Lean↔概念映射.csv", os.path.join(ROOT, "04_Lean对接")):
        for cid in (r.get("concept_ids") or "").split(";"):
            cid = cid.strip()
            if cid.startswith("C"):
                lean.setdefault(cid, []).append(r["lean_library"])
    terms = rd("术语候选.csv", os.path.join(S05, "术语候选"))[:300]
    quality = {
        "shacl": jload(os.path.join(S02, "本体校验报告.json"))["shacl"],
        "rdf": jload(os.path.join(S02, "本体校验报告.json"))["rdf"],
        "ontology": jload(os.path.join(S02, "本体统计.json")),
        "extract": jload(os.path.join(S05, "关系抽取", "抽取评测.json")),
        "termpool": jload(os.path.join(S05, "术语候选", "术语候选统计.json")),
    }
    cq = jload(os.path.join(S03, "SPARQL问答.json"))["questions"]
    ev_by_id = {r["struct_id"]: r for r in ev["evidence"]}

    payload = {
        "nodes": kg["nodes"], "edges": kg["edges"], "docs": docs,
        "evidence": ev_by_id, "aliases": aliases, "lean": lean, "terms": terms,
        "quality": quality, "cq": cq,
        "stats": kg["stats"],
    }
    return payload, sents


HTML = r"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CQM 检索台 · 图谱 / 全文 / 证据</title>
<style>
:root{--bg:#070b12;--panel:rgba(255,255,255,.04);--line:rgba(255,255,255,.10);--ink:#e6eef8;
--mut:#8ea0b8;--acc:#38bdf8;--acc2:#a78bfa;--ok:#34d399;--warn:#fbbf24;--gap:#f87171;--hy:#f59e0b}
*{box-sizing:border-box}html,body{margin:0;height:100%}
body{color:var(--ink);font:13.5px/1.7 "Microsoft YaHei",system-ui,sans-serif;
background:radial-gradient(1100px 600px at 8% -10%,rgba(56,189,248,.12),transparent 60%),
radial-gradient(900px 520px at 100% 0%,rgba(167,139,250,.12),transparent 58%),var(--bg)}
header{padding:12px 20px;border-bottom:1px solid var(--line);display:flex;gap:14px;align-items:center;flex-wrap:wrap;
background:rgba(7,11,18,.85);position:sticky;top:0;z-index:20;backdrop-filter:blur(10px)}
h1{font-size:15px;margin:0}
h1 small{display:block;font-weight:400;color:var(--mut);font-size:11.5px}
.mode{display:flex;gap:4px;margin-left:auto}
.mode button{border:1px solid var(--line);background:rgba(255,255,255,.05);color:var(--mut);border-radius:9px;
padding:6px 13px;font:inherit;cursor:pointer}
.mode button.on{background:linear-gradient(90deg,rgba(56,189,248,.25),rgba(167,139,250,.18));color:#fff;border-color:rgba(56,189,248,.5)}
main{display:grid;grid-template-columns:230px 1fr;gap:0;height:calc(100vh - 66px)}
aside{border-right:1px solid var(--line);padding:14px;overflow:auto;background:rgba(255,255,255,.02)}
aside h3{font-size:12px;color:#bcd3ea;margin:14px 0 7px}
aside h3:first-child{margin-top:0}
.facet{display:block;padding:3px 7px;border-radius:7px;color:var(--mut);cursor:pointer;font-size:12.5px;
display:flex;justify-content:space-between;gap:6px}
.facet:hover{background:rgba(255,255,255,.06);color:var(--ink)}
.facet.on{background:rgba(56,189,248,.18);color:#fff}
.facet em{font-style:normal;opacity:.7;font-size:11.5px}
section{padding:16px 20px 60px;overflow:auto}
.qbar{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap}
.qbar input{flex:1;min-width:280px;padding:10px 13px;border-radius:10px;border:1px solid var(--line);
background:rgba(255,255,255,.06);color:var(--ink);font:inherit;outline:none}
.qbar input:focus{border-color:rgba(56,189,248,.6);box-shadow:0 0 0 3px rgba(56,189,248,.12)}
.qbar button{padding:9px 16px;border-radius:10px;border:1px solid rgba(56,189,248,.5);
background:linear-gradient(90deg,rgba(56,189,248,.28),rgba(167,139,250,.22));color:#fff;font:inherit;cursor:pointer}
.hint{color:var(--mut);font-size:11.5px;margin:-4px 0 12px}
.hint code{background:rgba(255,255,255,.08);padding:1px 5px;border-radius:4px}
.card{background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.015));border:1px solid var(--line);
border-radius:12px;padding:11px 14px;margin-bottom:10px}
.card h4{margin:0 0 5px;font-size:13.5px}
.card .k{color:var(--mut);font-size:11.5px}
.card .quote{margin:7px 0 0;padding:8px 11px;border-left:2px solid var(--hy);background:rgba(245,158,11,.07);
border-radius:0 8px 8px 0;color:#f0e0c8;font-size:12.5px}
mark{background:rgba(56,189,248,.28);color:#eaf6ff;border-radius:3px;padding:0 2px}
.tag{display:inline-block;padding:1px 7px;border-radius:9px;font-size:11px;margin-right:5px;background:rgba(255,255,255,.08);color:var(--mut)}
.t-ok{background:rgba(52,211,153,.16);color:#6ee7b7}.t-gap{background:rgba(248,113,113,.16);color:#fca5a5}
.t-ax{background:rgba(251,191,36,.16);color:#fcd34d}.t-hy{background:rgba(245,158,11,.18);color:#fbd38d}
.t-con{background:rgba(56,189,248,.16);color:#7dd3fc}.t-prop{background:rgba(167,139,250,.16);color:#c4b5fd}
.res{display:flex;justify-content:space-between;gap:10px;align-items:baseline}
.score{color:var(--mut);font-size:11.5px;font-variant-numeric:tabular-nums}
.bar{height:4px;border-radius:2px;background:linear-gradient(90deg,#38bdf8,#a78bfa);margin-top:6px}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th,td{padding:6px 8px;border-bottom:1px solid rgba(255,255,255,.06);text-align:left;vertical-align:top}
th{background:rgba(255,255,255,.05);color:#b9cde3;position:sticky;top:0}
code{background:rgba(255,255,255,.08);padding:1px 5px;border-radius:4px;font-family:Consolas,monospace;font-size:11.5px}
a{color:var(--acc)}
.pill{display:inline-block;background:rgba(255,255,255,.07);border-radius:8px;padding:2px 8px;margin:2px 4px 2px 0;font-size:11.5px;color:var(--mut)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;margin-bottom:14px}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:10px 12px}
.kpi b{display:block;font-size:20px;color:#8ed0ff;text-shadow:0 0 14px rgba(56,189,248,.35)}
.kpi span{color:var(--mut);font-size:11.5px}
.empty{color:var(--mut);padding:20px;text-align:center}
#prog{color:var(--warn);font-size:12px}
pre{white-space:pre-wrap;word-break:break-all;background:rgba(255,255,255,.04);border:1px solid var(--line);
border-radius:9px;padding:9px 11px;font-size:11.5px;color:#cfe2f6;margin:6px 0}
</style></head>
<body>
<header>
  <h1>CQM 检索台<small>知识图谱 · 全文 BM25 · 证据溯源 · SPARQL 能力问答</small></h1>
  <div class="mode" id="mode">
    <button data-m="graph" class="on">图谱检索</button>
    <button data-m="full">全文检索</button>
    <button data-m="ev">证据检索</button>
    <button data-m="review">证据复核</button>
    <button data-m="quality">质量看板</button>
    <button data-m="cq">能力问答</button>
  </div>
</header>
<main>
  <aside id="side"></aside>
  <section id="view"></section>
</main>
<script>const PAY=__PAYLOAD__;const CORPUS_GZ="__CORPUS__";</script>
<script>
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const el=id=>document.getElementById(id);
const NODES=PAY.nodes, EDGES=PAY.edges, EV=PAY.evidence, DOCS=PAY.docs, ALIAS=PAY.aliases, LEAN=PAY.lean;
const byId={}; NODES.forEach(n=>byId[n.id]=n);
const KIND_NAME={concept:'概念',prop:'命题',gap:'缺口'};
const nodeKind=n=>KIND_NAME[n.kind]||n.kind;
/* ---------- 分面 ---------- */
let FACETS={kind:null,type:null,status:null,doc:null};
const cnt=(f)=>NODES.filter(n=>{
  if(FACETS.kind&&n.kind!==FACETS.kind)return false;
  if(FACETS.type&&(n.type!==FACETS.type))return false;
  if(FACETS.status&&(n.status!==FACETS.status))return false;
  if(FACETS.doc&&(n.doc!==FACETS.doc))return false;
  return true;});
function facetBlock(title,key,values){
  const cur=FACETS[key];
  return '<h3>'+esc(title)+(cur?' <a href="#" data-clear="'+key+'" style="float:right;font-size:11px">清除</a>':'')+'</h3>'
   +values.slice(0,26).map(([v,n])=>'<span class="facet'+(cur===v?' on':'')+'" data-f="'+key+'" data-v="'+esc(v)+'">'
     +esc(v)+'<em>'+n+'</em></span>').join('');
}
function renderSide(){
  const dist=(key,pool)=>Object.entries(pool.reduce((a,n)=>{const v=n[key]||'—';a[v]=(a[v]||0)+1;return a;},{}))
      .sort((a,b)=>b[1]-a[1]);
  const pool=NODES.filter(n=>(!FACETS.kind||n.kind===FACETS.kind));
  el('side').innerHTML=
    facetBlock('实体类型','kind',dist('kind',NODES))
   +facetBlock('概念/命题类型','type',dist('type',pool))
   +facetBlock('状态','status',dist('status',NODES.filter(n=>n.status)))
   +facetBlock('出处文档','doc',dist('doc',pool));
  el('side').querySelectorAll('.facet').forEach(s=>s.onclick=()=>{
    FACETS[s.dataset.f]=(FACETS[s.dataset.f]===s.dataset.v)?null:s.dataset.v;renderSide();run();});
  el('side').querySelectorAll('[data-clear]').forEach(s=>s.onclick=e=>{e.preventDefault();FACETS[s.dataset.clear]=null;renderSide();run();});
}
/* ---------- 语料解压 + BM25 ---------- */
let SENTS=null,IDX=null,DF=null,AVGDL=0,corpusNote='';
async function loadCorpus(){
  if(SENTS)return true;
  if(typeof DecompressionStream==='undefined'){corpusNote='当前浏览器不支持 DecompressionStream，无法解压全文语料（请用 Chrome/Edge 103+）。';return false;}
  el('prog')&&(el('prog').textContent='解压语料中…');
  const bin=Uint8Array.from(atob(CORPUS_GZ),c=>c.charCodeAt(0));
  const ds=new DecompressionStream('gzip');
  const buf=await new Response(new Blob([bin]).stream().pipeThrough(ds)).arrayBuffer();
  SENTS=JSON.parse(new TextDecoder('utf-8').decode(buf));
  corpusNote='';return true;
}
const isCJK=c=>/[\u4e00-\u9fff]/.test(c);
function tokenize(s){                       // CJK 一元 + 二元（Lucene CJKAnalyzer 思路）
  const out=[];let i=0;
  while(i<s.length){
    const ch=s[i];
    if(isCJK(ch)){out.push(ch);if(i+1<s.length&&isCJK(s[i+1]))out.push(s.slice(i,i+2));i++;}
    else if(/[A-Za-z0-9_\-]/.test(ch)){let j=i;while(j<s.length&&/[A-Za-z0-9_\-]/.test(s[j]))j++;
      out.push(s.slice(i,j).toLowerCase());i=j;}
    else i++;
  }
  return out;
}
function buildIndex(){
  IDX=new Map();DF=new Map();
  SENTS.forEach((s,di)=>{
    const toks=tokenize(s[3]);
    const tf=new Map();
    toks.forEach(t=>tf.set(t,(tf.get(t)||0)+1));
    tf.forEach((v,t)=>{
      if(!IDX.has(t))IDX.set(t,[]);
      IDX.get(t).push([di,v]);
      DF.set(t,(DF.get(t)||0)+1);
    });
  });
  AVGDL=SENTS.reduce((a,s)=>a+s[3].length,0)/Math.max(1,SENTS.length);
}
const K1=1.2,B=0.75;
function bm25(terms,N){
  const scores=new Map();
  terms.forEach(t=>{
    const posting=IDX.get(t);if(!posting)return;
    const df=DF.get(t),idf=Math.log(1+(SENTS.length-df+0.5)/(df+0.5));
    posting.forEach(([di,tf])=>{
      const dl=SENTS[di][3].length;
      const s=idf*(tf*(K1+1))/(tf+K1*(1-B+B*dl/AVGDL));
      scores.set(di,(scores.get(di)||0)+s);
    });
  });
  return [...scores.entries()].sort((a,b)=>b[1]-a[1]).slice(0,N);
}
function parseQuery(q){
  const must=[],not=[],terms=[];let phrase=null;
  const m=q.match(/"([^"]+)"/); if(m)phrase=m[1];
  q.replace(/"([^"]+)"/g,' ').split(/\s+/).filter(Boolean).forEach(w=>{
    if(w.startsWith('+')&&w.length>1)must.push(w.slice(1).toLowerCase());
    else if(w.startsWith('-')&&w.length>1)not.push(w.slice(1).toLowerCase());
    else if(w.startsWith('doc:'))FACETS.doc=w.slice(4).toUpperCase();
    else terms.push(w.toLowerCase());
  });
  return {terms,must,not,phrase};
}
function highlight(text,terms){
  let out=esc(text);
  terms.concat(phraseTerms).filter(Boolean).sort((a,b)=>b.length-a.length).slice(0,12).forEach(t=>{
    if(t.length<1)return;
    try{out=out.replace(new RegExp(t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),'gi'),m=>'<mark>'+m+'</mark>');}catch(e){}
  });
  return out;
}
let phraseTerms=[];
/* ---------- 五个视图：外壳一次渲染，结果区局部更新 ---------- */
let MODE='graph',LASTQ='';
const qbarHTML=ph=>'<div class="qbar"><input id="q" placeholder="'+ph+'" value="'+esc(LASTQ)+'"><button id="go">检索</button></div>';
const kpiHTML=rows=>'<div class="kpis">'+rows.map(([k,v])=>'<div class="kpi"><b>'+v+'</b><span>'+k+'</span></div>').join('')+'</div>';
function bindQ(){
  const inp=el('q'),go=el('go');
  if(!inp)return;
  const act=()=>{LASTQ=inp.value;dispatch();};
  go.onclick=act;
  inp.onkeydown=e=>{if(e.key==='Enter')act();};
  inp.focus();
}
function dispatch(){
  if(MODE==='graph')doGraph();else if(MODE==='full')doFull();else if(MODE==='ev')doEv();
  else if(MODE==='review')renderReview();
}
function run(){
  if(MODE==='graph'){
    el('view').innerHTML=kpiHTML([['实体',PAY.stats.concepts+PAY.stats.props+PAY.stats.gaps],['关系',PAY.stats.relations],
      ['claim 边',PAY.stats.claim_edges],['已核验边',PAY.stats.verified_edges],['证据',Object.keys(EV).length]])
      +qbarHTML('检索实体：名称 / 定义 / ID / 别名 / 缺口编号…')
      +'<div class="hint">左侧分面可叠加过滤；结果显示证据引文、上下游邻接与 Lean 映射。</div><div id="out"></div>';
    bindQ();doGraph();
  }else if(MODE==='full'){
    el('view').innerHTML=qbarHTML('全文检索：词 / "短语" / +必含 / -排除 / doc:D008')
      +'<div class="hint">BM25 排序 · CJK 一元+二元切分 · 语料 17,519 句（gzip 内嵌，浏览器本地解压）。</div>'
      +'<div id="prog"></div><div id="out"></div>';
    bindQ();doFull();
  }else if(MODE==='ev'){
    el('view').innerHTML=qbarHTML('检索证据：条目 ID / 引文 / 章节…')
      +'<div class="hint">每行 = 一条断言的原文定位（章节 + 字符区间 + 引文 + 方法 + 置信）。'
      +'置真 <b>verified</b> 请走「证据复核」模式。</div>'
      +'<div id="out"></div>';
    bindQ();doEv();
  }else if(MODE==='review'){renderReview();}
  else if(MODE==='quality'){runQuality();}
  else{runCq();}
}
function doGraph(){
  const q=(el('q').value||'').trim().toLowerCase();
  const rows=cnt().filter(n=>{
    if(!q)return true;
    return (n.id+' '+n.label+' '+(n.type||'')+' '+(n.status||'')+' '+(n.code||'')+' '+((ALIAS[n.id]||[]).join(' '))).toLowerCase().includes(q);
  }).slice(0,200);
  el('out').innerHTML=rows.map(n=>{
    const cls=n.kind==='concept'?'t-con':(n.kind==='gap'?'t-gap':'t-prop');
    const ev=EV[n.id]||{};
    const nb=EDGES.filter(e=>e.src.includes(n.id)||e.dst.includes(n.id));
    const outn=[],inn=[];
    nb.forEach(e=>{if(e.dst.includes(n.id))e.src.forEach(s=>outn.push(s));
                   if(e.src.includes(n.id))e.dst.forEach(d=>inn.push(d));});
    return '<div class="card"><div class="res"><h4>'+esc(n.label)
      +' <span class="tag '+cls+'">'+esc(nodeKind(n))+'</span>'
      +(n.type?'<span class="tag">'+esc(n.type)+'</span>':'')
      +(n.status?'<span class="tag '+(/未闭合|待证明/.test(n.status)?'t-gap':(/闭合|已证明/.test(n.status)?'t-ok':'t-ax'))+'">'+esc(n.status)+'</span>':'')
      +'</h4><span class="score">'+esc(n.id)+(n.code?' · '+esc(n.code):'')+'</span></div>'
      +(n.def?'<div class="k">'+esc(n.def)+'</div>':'')
      +'<div class="k">出处 '+esc(n.doc||'—')+' · 上游 '+outn.length+' · 下游 '+inn.length
      +(LEAN[n.id]?' · Lean: '+esc(LEAN[n.id].join('、')):'')
      +(ev.match_method?' · 证据 '+esc(ev.match_method)+'/'+esc(ev.confidence):'')+'</div>'
      +(ev.quote_clean?'<div class="quote">「'+esc(ev.quote_clean)+'」<div class="k" style="margin-top:4px">'
        +esc(ev.evidence_doc)+' · 字符 '+esc(ev.char_start)+'-'+esc(ev.char_end)+' · '+esc(ev.sec_title||'')+'</div></div>':'')
      +'<div>'+(outn.length?'<span class="k">上游：</span>'+outn.slice(0,8).map(x=>'<span class="pill">'+esc((byId[x]||{}).label||x)+'</span>').join(''):'')
      +(inn.length?'<span class="k">下游：</span>'+inn.slice(0,8).map(x=>'<span class="pill">'+esc((byId[x]||{}).label||x)+'</span>').join(''):'')+'</div></div>';
  }).join('')||'<div class="empty">无匹配实体</div>';
}
async function doFull(){
  const out=el('out'),prog=el('prog');
  const ok=await loadCorpus();
  if(!ok){out.innerHTML='<div class="empty">'+esc(corpusNote)+'</div>';return;}
  if(!IDX){prog.textContent='构建倒排索引…';await new Promise(r=>setTimeout(r,30));buildIndex();}
  prog.textContent='';
  const p=parseQuery(LASTQ);
  phraseTerms=p.terms.concat(p.phrase?[p.phrase]:[]).filter(t=>t.length>1);
  let hits=bm25(tokenize(LASTQ.replace(/["+]/g,' ').replace(/-\S+/g,'')).slice(0,40),400);
  if(p.phrase)hits=hits.filter(([di])=>SENTS[di][3].includes(p.phrase));
  if(p.must.length)hits=hits.filter(([di])=>p.must.every(t=>SENTS[di][3].toLowerCase().includes(t)));
  if(p.not.length)hits=hits.filter(([di])=>!p.not.some(t=>SENTS[di][3].toLowerCase().includes(t)));
  if(FACETS.doc)hits=hits.filter(([di])=>SENTS[di][0]===FACETS.doc);
  const top=hits.slice(0,60);
  out.innerHTML=(top.length?top.map(([di,s])=>{
    const row=SENTS[di];
    return '<div class="card"><div class="res"><span class="tag">'+esc(row[0])+'</span><span class="tag">'+esc(row[2])+'</span>'
      +'<span class="k">#'+row[1]+'</span><span class="score">BM25 '+s.toFixed(2)+'</span></div>'
      +'<div style="margin-top:4px">'+highlight(row[3],phraseTerms)+'</div>'
      +'<div class="bar" style="width:'+Math.min(100,s*8)+'%"></div></div>';}).join('')
    :'<div class="empty">无命中</div>');
}
function doEv(){
  const q=(el('q').value||'').trim().toLowerCase();
  const rows=Object.values(EV).filter(r=>!q||((r.struct_id+' '+(r.quote_clean||'')+' '+(r.sec_title||'')+' '+(r.name||'')).toLowerCase().includes(q)));
  const bad=rows.filter(r=>r.confidence==='unresolved'||!r.quote).length;
  const head=kpiHTML([['证据条数',Object.keys(EV).length],['当前结果',rows.length],
    ['高置信',rows.filter(r=>r.confidence==='high').length],['无证据',bad],
    ['已人工核验',rows.filter(r=>String(r.verified)==='True').length]]);
  el('view').insertAdjacentHTML('afterbegin',head);
  el('out').innerHTML=rows.slice(0,120).map(r=>'<div class="card"><div class="res"><h4><code>'+esc(r.struct_id)+'</code> '
    +esc(r.name||'')+'<span class="tag '+(r.confidence==='high'?'t-ok':(r.confidence==='unresolved'?'t-gap':'t-ax'))+'">'+esc(r.confidence)+'</span>'
    +(r.review_verdict?'<span class="tag '+(r.review_verdict==='approved'?'t-ok':(r.review_verdict==='rejected'?'t-gap':'t-ax'))+'">'
      +esc(r.review_verdict)+(r.reviewer?' · '+esc(r.reviewer):'')+'</span>':'<span class="tag">未复核</span>')+'</h4>'
    +'<span class="score">'+esc(r.match_method)+' · '+esc(r.score)+'</span></div>'
    +'<div class="k">'+esc(r.evidence_doc||r.doc_id)+' · 章节 '+esc(r.sec_title||'—')+' · 字符 '+esc(r.char_start)+'-'+esc(r.char_end)
    +(String(r.doc_switch)==='True'?' · <span style="color:#fbbf24">证据位于非指定出处文档</span>':'')+'</div>'
    +(r.quote_clean?'<div class="quote">「'+esc(r.quote_clean)+'」</div>':'<div class="k">（无引文）</div>')+'</div>').join('')
    ||'<div class="empty">无匹配证据</div>';
}
function runQuality(){
  const q=PAY.quality,s=q.shacl,e=q.extract,t=q.termpool,o=q.ontology;
  const vt=Object.entries(s.by_message||{});
  el('view').innerHTML=kpiHTML([['SHACL 合规',s.conforms?'通过':'违约 '+s.violations],['RDF 三元组',q.rdf.triples_exported],
      ['OWL 类/个体',o.owl_classes+' / '+o.owl_individuals],['HermiT',o.reasoner.consistent?'一致':'不一致'],
      ['关系抽取 F1',e.f1_pair],['术语候选',t.new_candidates_kept]])
   +'<div class="card"><h4>SHACL 数据契约</h4><div class="k">形状文件 <code>'+esc(s.shapes_file)+'</code> · 违约 '+s.violations+' 条</div>'
   +(vt.length?vt.map(([m,n])=>'<div class="k">· '+n+' × '+esc(m)+'</div>').join('')
     :'<div class="k">全部通过：概念/命题/缺口/超边/论证均有规范名、定义、出处与证据；缺口编号符合 ^(C|G\\d+|N\\d+)$。</div>')+'</div>'
   +'<div class="card"><h4>关系抽取评测（金标准 = 人工论证表）</h4><table><tbody>'
   +Object.entries(e).filter(([k,v])=>typeof v!=='object').map(([k,v])=>'<tr><td>'+esc(k)+'</td><td>'+esc(v)+'</td></tr>').join('')
   +'</tbody></table><div class="hint">分层口径：cooccur 层（同句共现，类型未定）无向召回已逼近'
   +'「原文同句共现」物理上界；pattern 层（两端间有线索词）带类型但精确率有限。'
   +'类型定型交由人工复核或 LLM（<code>llm_extract.py</code> 就绪，须过 span 校验）。</div></div>'
   +'<div class="card"><h4>RDF 导出构成</h4>'+Object.entries(q.rdf.added||{}).map(([k,v])=>'<span class="pill">'+esc(k)+' '+v+'</span>').join('')+'</div>';
}
function runCq(){
  el('view').innerHTML='<div class="hint">下列问句由 <code>build_kg.py</code> 用 SPARQL 1.1 在本体+证据图上实际执行（rdflib），结果内嵌本页。</div>'
    +PAY.cq.map(c=>'<div class="card"><h4>'+esc(c.question)+'<span class="tag">'+c.row_count+' 行</span></h4>'
      +'<pre>'+esc(c.sparql)+'</pre><table><tbody>'
      +c.rows.slice(0,12).map(r=>'<tr>'+r.map(x=>'<td>'+esc(x)+'</td>').join('')+'</tr>').join('')
      +'</tbody></table>'+(c.rows.length>12?'<div class="k">…共 '+c.rows.length+' 行</div>':'')+'</div>').join('');
}
/* ---------- 证据复核：verified 置真的唯一合法来源 ---------- */
const RVKEY='cqm_review_v1',RKY='cqm_reviewer_v1';
let RV={};try{RV=JSON.parse(localStorage.getItem(RVKEY)||'{}')}catch(e){RV={}}
let RVIDX=0,RVFILTER='all';
const rvAll=()=>Object.keys(EV);
function rvSave(){try{localStorage.setItem(RVKEY,JSON.stringify(RV))}catch(e){}}
function rvList(){const ids=rvAll();
  if(RVFILTER==='todo')return ids.filter(i=>!RV[i]);
  if(RVFILTER==='approved'||RVFILTER==='rejected'||RVFILTER==='unsure')
    return ids.filter(i=>RV[i]&&RV[i].verdict===RVFILTER);
  return ids;}
function csvEsc(s){s=String(s==null?'':s);return /[",\n]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s}
function rvExport(){
  const rows=rvAll().filter(i=>RV[i]).map(i=>[i,RV[i].verdict,RV[i].reviewer||'',RV[i].note||'',RV[i].at||'']);
  if(!rows.length){alert('尚无复核记录，先逐条判定。');return}
  const csv='\uFEFF'+[['struct_id','verdict','reviewer','note','reviewed_at']].concat(rows)
    .map(r=>r.map(csvEsc).join(',')).join('\r\n');
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));
  a.download='复核结果.csv';document.body.appendChild(a);a.click();a.remove();
}
function rvImport(inp){
  const f=inp.files&&inp.files[0];if(!f)return;
  const rd=new FileReader();
  rd.onload=()=>{const txt=String(rd.result||'').replace(/^\uFEFF/,'');
    const lines=txt.split(/\r?\n/).filter(Boolean);let n=0;
    lines.slice(1).forEach(l=>{
      const cells=l.split(/,(?=(?=(?:[^"]*){2}[^"])*$)/).map(c=>{c=c.trim();
        if(c.charAt(0)==='"'&&c.charAt(c.length-1)==='"')c=c.slice(1,-1).replace(/""/g,'"');return c;});
      const id=cells[0],v=cells[1];
      if(id&&EV[id]&&['approved','rejected','unsure'].indexOf(v)>=0){
        RV[id]={verdict:v,reviewer:cells[2]||'',note:cells[3]||'',at:cells[4]||''};n++;}});
    rvSave();RVIDX=0;renderReview();alert('导入 '+n+' 条复核记录');};
  rd.readAsText(f,'utf-8');
}
function rvSet(v){
  const ids=rvList();if(!ids.length)return;
  const id=ids[Math.min(RVIDX,ids.length-1)];
  const rev=(localStorage.getItem(RKY)||'').trim();
  if(v==='approved'&&!rev){alert('「通过」必须填写复核人（上方输入框）。');return}
  const nt=document.getElementById('rvnote');
  RV[id]={verdict:v,reviewer:rev,note:nt?nt.value:'',
    at:new Date().toISOString().slice(0,19).replace('T',' ')};
  rvSave();renderReview();
}
function rvRenderCard(){
  const list=rvList();
  if(RVIDX>=list.length)RVIDX=0;
  const cur=list[RVIDX];
  if(!cur)return '<div class="empty">当前筛选下无条目</div>';
  const r=EV[cur],rv=RV[cur];
  return '<div class="card"><div class="res"><h4><code>'+esc(cur)+'</code> '+esc(r.name||'')
   +'<span class="tag">'+esc(r.kind||'')+'</span>'
   +'<span class="tag '+(r.confidence==='high'?'t-ok':(r.confidence==='unresolved'?'t-gap':'t-ax'))+'">'+esc(r.confidence||'')+'</span>'
   +(rv?'<span class="tag '+(rv.verdict==='approved'?'t-ok':(rv.verdict==='rejected'?'t-gap':'t-ax'))+'">'
      +esc(rv.verdict)+(rv.reviewer?' · '+esc(rv.reviewer):'')+'</span>':'<span class="tag t-ax">未复核</span>')
   +'</h4><span class="score">'+(RVIDX+1)+' / '+list.length+'</span></div>'
   +'<div class="k">定位 '+esc(r.match_method)+' · 文档 '+esc(r.evidence_doc||r.doc_id)
     +' · 字符 '+esc(r.char_start)+'-'+esc(r.char_end)+' · 章节 '+esc(r.sec_title||'—')
   +(String(r.doc_switch)==='True'?' · <b style="color:#fbbf24">跨文档</b>':'')+'</div>'
   +'<div class="k">条目（'+esc(r.kind||'')+'）：'+esc(r.name||'')+'</div>'
   +(r.quote_clean?'<div class="quote">「'+esc(r.quote_clean)+'」</div>':'<div class="k">（机器未给出引文）</div>')
   +'<div class="qbar" style="margin-top:10px">'
     +'<button id="rvok">✔ 通过（置 verified）</button><button id="rvno">✘ 驳回</button><button id="rvus">? 存疑</button>'
     +'<button id="rvprev">← 上一条</button><button id="rvnext">下一条 →</button></div>'
   +'<textarea id="rvnote" rows="2" style="width:100%;margin-top:8px;background:rgba(255,255,255,.05);'
     +'border:1px solid var(--line);border-radius:8px;color:var(--ink);padding:7px 9px;font:inherit" '
     +'placeholder="复核备注（可选，随 CSV 导出）">'+esc(rv&&rv.note||'')+'</textarea></div>';
}
function renderReview(){
  const ids=rvAll(),list=rvList();
  const done=ids.filter(i=>RV[i]).length;
  const cnt=v=>ids.filter(i=>RV[i]&&RV[i].verdict===v).length;
  el('view').innerHTML=kpiHTML([['进度',done+'/'+ids.length],['已通过',cnt('approved')],
      ['驳回',cnt('rejected')],['存疑',cnt('unsure')],['待复核',ids.length-done]])
   +'<div class="qbar">'
   +'<input id="rvrev" placeholder="复核人（「通过」必填；存 localStorage）" style="flex:0 0 260px" value="'+esc(localStorage.getItem(RKY)||'')+'">'
   +'<select id="rvf"><option value="all">全部</option><option value="todo">仅未复核</option>'
     +'<option value="approved">仅通过</option><option value="rejected">仅驳回</option><option value="unsure">仅存疑</option></select>'
   +'<button id="rvexp">导出 复核结果.csv</button>'
   +'<input id="rvfile" type="file" accept=".csv,.txt" style="flex:0 0 auto;font-size:12px">'
   +'</div>'
   +'<div class="hint">流程：逐条判定 → <b>导出 复核结果.csv</b> → 放入 <code>00_外部引用/</code> → '
   +'重跑 <code>build_evidence.py</code> 合入 verified → <code>check_provenance.py</code> 硬校验「verified ⟺ approved 且有复核人」。'
   +'草稿存浏览器 localStorage；快捷键 1/2/3 = 通过/驳回/存疑，←/→ 翻页（输入框内不触发）。</div>'
   +rvRenderCard();
  const revI=el('rvrev');
  revI.oninput=()=>{try{localStorage.setItem(RKY,revI.value.trim())}catch(e){}};
  el('rvf').value=RVFILTER;
  el('rvf').onchange=e=>{RVFILTER=e.target.value;RVIDX=0;renderReview();};
  el('rvexp').onclick=rvExport;
  el('rvfile').onchange=function(){rvImport(this);this.value='';};
  const go=el('rvok');if(go){go.onclick=()=>rvSet('approved');
    el('rvno').onclick=()=>rvSet('rejected');
    el('rvus').onclick=()=>rvSet('unsure');
    el('rvprev').onclick=()=>{RVIDX=Math.max(0,RVIDX-1);renderReview();};
    el('rvnext').onclick=()=>{RVIDX=Math.min(rvList().length-1,RVIDX+1);renderReview();};
    const nt=el('rvnote');
    nt.oninput=()=>{const id=rvList()[RVIDX];if(RV[id]){RV[id].note=nt.value;RV[id].at=new Date().toISOString().slice(0,19).replace('T',' ');rvSave();}};
  }
}
document.addEventListener('keydown',e=>{
  if(MODE!=='review')return;
  const t=e.target&&e.target.tagName;
  if(t==='INPUT'||t==='TEXTAREA'||t==='SELECT')return;
  if(e.key==='1')rvSet('approved');else if(e.key==='2')rvSet('rejected');else if(e.key==='3')rvSet('unsure');
  else if(e.key==='ArrowLeft'){RVIDX=Math.max(0,RVIDX-1);renderReview();}
  else if(e.key==='ArrowRight'){RVIDX=Math.min(rvList().length-1,RVIDX+1);renderReview();}
});
el('mode').querySelectorAll('button').forEach(b=>b.onclick=()=>{
  el('mode').querySelectorAll('button').forEach(x=>x.classList.remove('on'));
  b.classList.add('on');MODE=b.dataset.m;run();
});
renderSide();run();
</script>
</body></html>"""


def main():
    payload, sents = build_payload()
    raw = json.dumps(sents, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    gz = base64.b64encode(gzip.compress(raw, 9)).decode("ascii")
    html = (HTML.replace("__PAYLOAD__", json.dumps(payload, ensure_ascii=False))
                .replace("__CORPUS__", gz))
    out_dir = os.path.join(S10, "源_可视化", "检索台")
    os.makedirs(out_dir, exist_ok=True)
    with io.open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print(f"[OK] 检索台/index.html  {len(html):,} 字符（语料 {len(sents):,} 句 → gzip {len(gz):,} 字符）")
    print(f"     实体 {len(payload['nodes'])} · 边 {len(payload['edges'])} · 证据 {len(payload['evidence'])}"
          f" · 术语候选 {len(payload['terms'])} · SPARQL 问句 {len(payload['cq'])}")


if __name__ == "__main__":
    main()
