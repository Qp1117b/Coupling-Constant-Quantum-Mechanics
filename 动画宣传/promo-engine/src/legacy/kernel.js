// 内容内核：由 tools/extract_kernel.py 从 v2 片源逐字提取。
// 只负责「场景几何 + 演算逐步呈现」；镜头、流场、转场、字幕入场、
// 音画同步、渲染与验收一概不在这里，全部由 src/engine 承担。
// 请勿手改本文件；改动内容口径请回到上屏白名单并重新抽取。
export const SKELETON = "<svg id=\"stage\" viewBox=\"0 0 1920 1080\" xmlns=\"http://www.w3.org/2000/svg\">\n  <defs>\n    <radialGradient id=\"bg\" cx=\"46%\" cy=\"40%\" r=\"76%\">\n      <stop offset=\"0%\" stop-color=\"#0A0F1A\"/>\n      <stop offset=\"100%\" stop-color=\"#070A12\"/>\n    </radialGradient>\n    <radialGradient id=\"haloG\" cx=\"50%\" cy=\"50%\" r=\"50%\">\n      <stop offset=\"0%\" stop-color=\"#35E0FF\" stop-opacity=\"0.145\"/>\n      <stop offset=\"48%\" stop-color=\"#35E0FF\" stop-opacity=\"0.042\"/>\n      <stop offset=\"100%\" stop-color=\"#35E0FF\" stop-opacity=\"0\"/>\n    </radialGradient>\n    <linearGradient id=\"scanG\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"0\">\n      <stop offset=\"0%\" stop-color=\"#35E0FF\" stop-opacity=\"0\"/>\n      <stop offset=\"38%\" stop-color=\"#35E0FF\" stop-opacity=\"0.095\"/>\n      <stop offset=\"50%\" stop-color=\"#E8EEF9\" stop-opacity=\"0.175\"/>\n      <stop offset=\"62%\" stop-color=\"#35E0FF\" stop-opacity=\"0.095\"/>\n      <stop offset=\"100%\" stop-color=\"#35E0FF\" stop-opacity=\"0\"/>\n    </linearGradient>\n    <linearGradient id=\"swipeG\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"0\">\n      <stop offset=\"0%\" stop-color=\"#35E0FF\" stop-opacity=\"0\"/>\n      <stop offset=\"40%\" stop-color=\"#35E0FF\" stop-opacity=\"0.10\"/>\n      <stop offset=\"50%\" stop-color=\"#FFFFFF\" stop-opacity=\"0.21\"/>\n      <stop offset=\"60%\" stop-color=\"#F5C542\" stop-opacity=\"0.10\"/>\n      <stop offset=\"100%\" stop-color=\"#F5C542\" stop-opacity=\"0\"/>\n    </linearGradient>\n  </defs>\n  <rect width=\"1920\" height=\"1080\" fill=\"none\"/>\n  <g id=\"field\"></g>\n  <line x1=\"150\" y1=\"100\" x2=\"1770\" y2=\"100\" stroke=\"#1A2233\" stroke-width=\"1\"/>\n  <text id=\"segLabel\" x=\"150\" y=\"76\" font-family=\"Microsoft YaHei, Noto Sans SC, sans-serif\"\n        font-size=\"20\" fill=\"#7A869C\" letter-spacing=\"0.14em\"></text>\n\n  <g id=\"camera\">\n    <g id=\"s1\"></g><g id=\"s2\"></g><g id=\"s3\"></g>\n    <g id=\"s4\"></g><g id=\"s5\"></g><g id=\"s6\"></g>\n  </g>\n  <g id=\"carry\"></g>\n  <g id=\"rail\"></g>\n\n  <g id=\"overlay\"></g>\n  <line x1=\"150\" y1=\"930\" x2=\"1770\" y2=\"930\" stroke=\"#1A2233\" stroke-width=\"1\"/>\n  <text id=\"capMain\" x=\"150\" y=\"984\" font-family=\"Microsoft YaHei, Noto Sans SC, sans-serif\"\n        font-size=\"33\" fill=\"#E8EEF9\" letter-spacing=\"0.4\"></text>\n  <text id=\"capSub\" x=\"150\" y=\"1022\" font-family=\"Microsoft YaHei, Noto Sans SC, sans-serif\"\n        font-size=\"19\" fill=\"#FFB020\" letter-spacing=\"0.3\"></text>\n  <g id=\"badge\"></g>\n  <text id=\"railLabel\" x=\"60\" y=\"352\" font-family=\"Consolas, monospace\" font-size=\"15\"\n        fill=\"#4A5570\" letter-spacing=\"0.18em\">OPS 24</text>\n</svg>";

function createKernel(container, DATA){
  const q = id => container.querySelector("#"+id);
  container.innerHTML = SKELETON;
  const NS="http://www.w3.org/2000/svg";
  const svg=q("stage");
  const G=[1,2,3,4,5,6].map(i=>q("s"+i));
  const carryG=q("carry"), railG=q("rail"), badgeG=q("badge");
  const capMain=q("capMain"), capSub=q("capSub"), segLabel=q("segLabel");
  const cameraG=q("camera"), fieldG=q("field"), overlayG=q("overlay");
  const {C,MATH,MONO,ZH,SYM,TOTAL,OPS,SEGS,B,CAPS}=DATA;

const clamp=(x,a,b)=>x<a?a:x>b?b:x;
const lerp=(a,b,t)=>a+(b-a)*t;
const easeOut=t=>1-Math.pow(1-clamp(t,0,1),3);
const easeIO=t=>{t=clamp(t,0,1);return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;};

function E(tag,attrs,parent){
  const e=document.createElementNS(NS,tag);
  if(attrs)for(const k in attrs)e.setAttribute(k,attrs[k]);
  if(parent)parent.appendChild(e);
  return e;
}
function T(parent,x,y,size,color,str,opts){
  opts=opts||{};
  const t=E("text",{x:x,y:y,"font-size":size,fill:color,
    "font-family":opts.font||ZH,"font-weight":opts.weight||"normal"},parent);
  if(opts.anchor)t.setAttribute("text-anchor",opts.anchor);
  if(opts.opacity!=null)t.setAttribute("opacity",opts.opacity);
  if(opts.spacing)t.setAttribute("letter-spacing",opts.spacing);
  t.textContent=str;
  return t;
}
// 公式行：parts = [{t, it, sup, sub, font, color}]
function FT(parent,x,y,size,color,parts){
  const t=E("text",{x:x,y:y,"font-size":size,fill:color,"font-family":MATH},parent);
  parts.forEach(p=>{
    const s=E("tspan",{},t);
    if(p.sup){s.setAttribute("baseline-shift","super");s.setAttribute("font-size",(size*0.62).toFixed(1));}
    if(p.sub){s.setAttribute("baseline-shift","sub");s.setAttribute("font-size",(size*0.62).toFixed(1));}
    if(p.it)s.setAttribute("font-style","italic");
    if(p.font)s.setAttribute("font-family",p.font);
    if(p.color)s.setAttribute("fill",p.color);
    s.textContent=p.t;
  });
  return t;
}
function vis(g,t,a,b,fin,out){
  fin=fin==null?0.25:fin; out=out==null?0.25:out;
  let o=0;
  if(t>=a&&t<=b){o=1;if(t<a+fin)o=easeOut((t-a)/fin);if(t>b-out)o=1-easeOut((t-(b-out))/out);}
  g.setAttribute("opacity",o.toFixed(3));
  return o;
}
function group(parent,x,y,w,h,opts){
  opts=opts||{};
  const g=E("g",{},parent);
  const r=E("rect",{x:x,y:y,width:w,height:h,rx:opts.rx==null?3:opts.rx,
    fill:opts.fill||"none","fill-opacity":opts.fillOp||"1",
    stroke:opts.stroke||C.faint,"stroke-width":opts.sw||1.2,
    "stroke-dasharray":opts.dash||"none"},g);
  g._rect=r;
  return g;
}
function smallLabel(parent,x,y,str,color){return T(parent,x,y,17,color||C.dim,str,{font:ZH,spacing:"0.1em"});}

const S1=(function(){
  const p=G[0];
  const grid=E("g",{},p),strike=E("g",{},p),axis=E("g",{},p);
  // 时空网格
  for(let i=0;i<=16;i++)E("line",{x1:270+i*84,y1:370,x2:270+i*84,y2:820,stroke:C.cyan,"stroke-opacity":".075","stroke-width":"1"},grid);
  for(let j=0;j<=8;j++)E("line",{x1:270,y1:370+j*56.25,x2:1614,y2:370+j*56.25,stroke:C.cyan,"stroke-opacity":".075","stroke-width":"1"},grid);
  E("line",{x1:270,y1:838,x2:1614,y2:838,stroke:C.cyan,"stroke-opacity":".26","stroke-width":"1"},grid);
  E("line",{x1:270,y1:838,x2:270,y2:370,stroke:C.cyan,"stroke-opacity":".26","stroke-width":"1"},grid);
  T(grid,1632,850,20,C.dim,"x",{font:MONO});T(grid,242,362,20,C.dim,"t",{font:MONO});
  T(grid,1050,560,22,C.dim,"事件",{font:ZH});
  E("circle",{cx:1030,cy:568,r:5,fill:C.white},grid);
  // 划掉
  const a=E("line",{x1:280,y1:380,x2:1600,y2:820,stroke:C.amber,"stroke-opacity":".72","stroke-width":"4.5"},strike);
  const b=E("line",{x1:280,y1:820,x2:1600,y2:380,stroke:C.white,"stroke-opacity":".34","stroke-width":"3.5"},strike);
  const la=a.getTotalLength(),lb=b.getTotalLength();
  a.setAttribute("stroke-dasharray",la);a.setAttribute("stroke-dashoffset",la);
  b.setAttribute("stroke-dasharray",lb);b.setAttribute("stroke-dashoffset",lb);
  // 耦合常数轴
  const AX={x0:300,x1:1620,y:690,u0:960,du:270};
  const ln=E("line",{x1:AX.x0,y1:AX.y,x2:AX.x1,y2:AX.y,stroke:C.gold,"stroke-opacity":".5","stroke-width":"1.6"},axis);
  const LL=ln.getTotalLength();ln.setAttribute("stroke-dasharray",LL);ln.setAttribute("stroke-dashoffset",LL);
  T(axis,310,646,25,C.gold,"u = ln r",{font:MONO});
  [-2,-1,0,1,2].forEach(u=>{const x=AX.u0+u*AX.du;
    E("line",{x1:x,y1:AX.y-10,x2:x,y2:AX.y+10,stroke:C.gold,"stroke-opacity":".42","stroke-width":"1"},axis);
    T(axis,x,732,19,C.dim,String(u),{font:MONO,anchor:"middle"});});
  const dot=E("circle",{cx:AX.u0,cy:AX.y,r:7,fill:C.gold},axis);
  T(axis,AX.u0+18,AX.y-16,19,C.gold,"常数",{font:ZH});
  const band=E("line",{x1:AX.u0,y1:AX.y,x2:AX.u0,y2:AX.y,stroke:C.cyan,"stroke-width":"2","stroke-dasharray":"6 7"},axis);
  T(axis,AX.u0,772,18,C.cyan,"Δu",{font:MONO,anchor:"middle"});
  // 公式
  const f1=E("g",{},p),f2=E("g",{},p),f3=E("g",{},p),f4=E("g",{},p);
  FT(f1,150,210,50,C.white,[{t:"["},{t:"x̂",it:1},{t:", "},{t:"p̂",it:1},{t:"x",sub:1},{t:"] = i"},{t:"ℏ",it:1}]);
  smallLabel(f1,150,158,"外部标准 · 标准量子力学",C.white);
  FT(f2,150,210,50,C.gold,[{t:"["},{t:"û",it:1},{t:", "},{t:"p̂",it:1},{t:"u",sub:1},{t:"] = i"}]);
  smallLabel(f2,150,158,"框架公理 · 耦合空间",C.gold);
  FT(f3,150,210,50,C.white,[{t:"Δ"},{t:"u"},{t:" · Δ"},{t:"p",it:1},{t:"u",sub:1},{t:" ≥ 1/2"}]);
  smallLabel(f3,150,158,"标准代数",C.white);
  const f4a=FT(f4,150,210,48,C.white,[{t:"Δ"},{t:"r"},{t:"/⟨"},{t:"r"},{t:"⟩ · Δ"},{t:"v",it:1},{t:"τ",sub:1},{t:" ≥ "}]);
  const w4=f4a.getComputedTextLength(),sx=150+w4+16;
  const slot=group(f4,sx,170,74,56,{stroke:C.amber,dash:"6 5",sw:1.8});
  const slotQ=T(f4,sx+37,209,30,C.amber,"?",{font:MATH,anchor:"middle"});
  FT(f4,sx+90,210,48,C.white,[{t:"/2"}]);
  smallLabel(f4,150,158,"代入  p̂u = v̂τ / ☯",C.cyan);
  // 右侧演算链：四步逐步点亮，避免钩子段只剩一行公式
  const chain=E("g",{},p),chainRows=[];
  smallLabel(chain,1060,370,"演算链 · 每一步都能在原文找到",C.dim);
  const chainDefs=[
    {p:[{t:"["},{t:"û",it:1},{t:", "},{t:"p̂",it:1},{t:"u",sub:1},{t:"] = i"}],c:C.gold,s:"框架公理"},
    {p:[{t:"Δ"},{t:"u"},{t:" · Δ"},{t:"p",it:1},{t:"u",sub:1},{t:" ≥ 1/2"}],c:C.white,s:"标准代数"},
    {p:[{t:"p̂",it:1},{t:"u",sub:1},{t:" = "},{t:"v̂",it:1},{t:"τ",sub:1},{t:" / "},{t:"☯",font:SYM}],c:C.cyan,s:"代入"},
    {p:[{t:"Δ"},{t:"r"},{t:"/⟨"},{t:"r"},{t:"⟩ · Δ"},{t:"v",it:1},{t:"τ",sub:1},{t:" ≥ "},{t:"☯",font:SYM},{t:"/2"}],c:C.cyan,s:"待求的数"}
  ];
  chainDefs.forEach((r,i)=>{
    const y=414+i*68;
    const g=group(chain,1060,y,680,54,{stroke:r.c,sw:1.1,fill:r.c,fillOp:".035"});
    T(g,1080,y+35,19,r.c,String(i+1).padStart(2,"0"),{font:MONO});
    FT(g,1130,y+36,25,C.text,r.p);
    T(g,1718,y+34,16,r.c,r.s,{font:ZH,anchor:"end"});
    g.setAttribute("opacity","0");chainRows.push(g);
  });
  chain.setAttribute("opacity","0");
  [f1,f2,f3,f4].forEach(g=>g.setAttribute("opacity","0"));
  grid.setAttribute("opacity","0");strike.setAttribute("opacity","0");axis.setAttribute("opacity","0");
  return {grid:grid,strike:strike,a:a,b:b,la:la,lb:lb,axis:axis,ln:ln,LL:LL,
    AX:AX,dot:dot,band:band,f1:f1,f2:f2,f3:f3,f4:f4,slot:slot._rect,slotQ:slotQ,
    chain:chain,chainRows:chainRows};
})();

/* ============================================================
   段 2 · 26–60 s  ☯ 是多少（ξ 五步 + 切线 hero）
   ============================================================ */
const S2=(function(){
  const p=G[1];
  // 真实数值：Γ（Lanczos）与 ζ（Euler–Maclaurin），用于画 ξ 与数值微分互验
  const GC=[0.99999999999980993,676.5203681218851,-1259.1392167224028,
    771.32342877765313,-176.61502916214059,12.507343278686905,
    -0.13857109526572012,9.9843695780195716e-6,1.5056327351493116e-7];
  function gamma(z){if(z<0.5)return Math.PI/(Math.sin(Math.PI*z)*gamma(1-z));
    z-=1;let x=GC[0];for(let i=1;i<9;i++)x+=GC[i]/(z+i);
    const t=z+7.5;return Math.sqrt(2*Math.PI)*Math.pow(t,z+0.5)*Math.exp(-t)*x;}
  function zeta(s){if(Math.abs(s-1)<1e-9)return NaN;
    const N=24;let sum=0;for(let n=1;n<N;n++)sum+=Math.pow(n,-s);
    sum+=Math.pow(N,1-s)/(s-1)+0.5*Math.pow(N,-s);
    sum+=(1/12)*s*Math.pow(N,-s-1);
    sum+=(-1/720)*s*(s+1)*(s+2)*Math.pow(N,-s-3);
    sum+=(1/30240)*s*(s+1)*(s+2)*(s+3)*(s+4)*Math.pow(N,-s-5);
    sum+=(-1/1209600)*s*(s+1)*(s+2)*(s+3)*(s+4)*(s+5)*(s+6)*Math.pow(N,-s-7);
    return sum;}
  function xi(s){if(Math.abs(s-1)<1e-7)return 0.5;
    return 0.5*s*(s-1)*Math.pow(Math.PI,-s/2)*gamma(s/2)*zeta(s);}
  const PSI=0.023095708966;
  const LN1=Math.log(xi(1));
  const NUM=(Math.log(xi(1+1e-4))-Math.log(xi(1-1e-4)))/(2e-4);
  const DIFF=Math.abs(NUM-PSI);
  window.__checks={xi_num:NUM,xi_analytic:PSI,xi_diff:DIFF};
  // 公式组
  const F={};
  ["a","b","c","d","e","f"].forEach(k=>{F[k]=E("g",{},p);F[k].setAttribute("opacity","0");});
  FT(F.a,150,210,44,C.white,[{t:"ξ("},{t:"s",it:1},{t:") = ½ "},{t:"s",it:1},{t:"("},{t:"s",it:1},{t:"−1) "},
    {t:"π",it:1},{t:"−s/2",sup:1},{t:" Γ("},{t:"s",it:1},{t:"/2) "},{t:"ζ",it:1},{t:"("},{t:"s",it:1},{t:")"}]);
  smallLabel(F.a,150,158,"定义式锚点 · ξ 函数",C.gold);
  FT(F.b,150,196,38,C.white,[{t:"ln ξ("},{t:"s",it:1},{t:") = ln ½ + ln "},{t:"s",it:1},{t:" + ln("},{t:"s",it:1},{t:"−1)"}]);
  FT(F.b,200,250,38,C.white,[{t:"− ("},{t:"s",it:1},{t:"/2) ln "},{t:"π",it:1},{t:" + ln Γ("},{t:"s",it:1},{t:"/2) + ln "},{t:"ζ",it:1},{t:"("},{t:"s",it:1},{t:")"}]);
  smallLabel(F.b,150,158,"取对数 · 六项拆开",C.cyan);
  FT(F.c,150,196,36,C.white,[{t:"ξ′("},{t:"s",it:1},{t:")/ξ("},{t:"s",it:1},{t:") = 1/"},{t:"s",it:1},{t:" + 1/("},{t:"s",it:1},{t:"−1) − ½ ln "},{t:"π",it:1}]);
  FT(F.c,200,248,36,C.white,[{t:"+ ½ ψ("},{t:"s",it:1},{t:"/2) + "},{t:"ζ",it:1},{t:"′("},{t:"s",it:1},{t:")/"},{t:"ζ",it:1},{t:"("},{t:"s",it:1},{t:")"}]);
  smallLabel(F.c,150,158,"逐项求导",C.cyan);
  FT(F.d,150,196,34,C.white,[{t:"ζ′/ζ("},{t:"s",it:1},{t:") = "},{t:"−1/(s−1)",color:C.amber},{t:" + "},{t:"γ",it:1,color:C.cyan},{t:" + O("},{t:"s",it:1},{t:"−1)"}]);
  const d2=FT(F.d,150,250,34,C.white,[{t:"1/(s−1)",color:C.amber},{t:" + ζ′/ζ("},{t:"s",it:1},{t:") = "},{t:"γ",it:1,color:C.cyan},{t:" + O("},{t:"s",it:1},{t:"−1)"}]);
  smallLabel(F.d,150,158,"s → 1 · 极点项相消",C.cyan);
  FT(F.e,150,210,42,C.white,[{t:"ψ(1/2) = −"},{t:"γ",it:1},{t:" − 2 ln 2"}]);
  smallLabel(F.e,150,158,"代入",C.cyan);
  const fa=FT(F.f,150,210,48,C.gold,[{t:"☯",font:SYM},{t:" = 1 + "},{t:"γ",it:1},{t:"/2 − ln(2√"},{t:"π",it:1},{t:") = "}]);
  const fw=fa.getComputedTextLength();
  const box=group(F.f,150+fw+4,166,360,60,{stroke:C.cyan,sw:1.4,fill:C.cyan,fillOp:".07"});
  T(F.f,150+fw+22,208,40,C.cyan,"0.023095708966",{font:MONO});
  smallLabel(F.f,150,158,"闭式落定",C.cyan);
  // ξ 曲线
  const plot=E("g",{},p);
  const PX0=360,PX1=1240,PY0=430,PY1=830,VMIN=-0.702,VMAX=-0.640;
  const sx=s=>PX0+(s-1)*(PX1-PX0);
  const vy=v=>PY1-(v-VMIN)/(VMAX-VMIN)*(PY1-PY0);
  E("line",{x1:PX0,y1:PY1,x2:PX1,y2:PY1,stroke:C.faint,"stroke-width":"1"},plot);
  E("line",{x1:PX0,y1:PY0,x2:PX0,y2:PY1,stroke:C.faint,"stroke-width":"1"},plot);
  for(let s=1;s<=2.001;s+=0.2){const x=sx(s);
    E("line",{x1:x,y1:PY1,x2:x,y2:PY1+8,stroke:C.faint,"stroke-width":"1"},plot);
    T(plot,x,PY1+30,17,C.dim,s.toFixed(1),{font:MONO,anchor:"middle"});}
  [-0.69,-0.67,-0.65].forEach(v=>{const y=vy(v);
    E("line",{x1:PX0-8,y1:y,x2:PX0,y2:y,stroke:C.faint,"stroke-width":"1"},plot);
    T(plot,PX0-14,y+6,16,C.dim,v.toFixed(2),{font:MONO,anchor:"end"});});
  T(plot,PX1+22,PY1+50,19,C.dim,"s",{font:MONO});
  T(plot,PX0-14,PY0-16,19,C.dim,"ln ξ(s)",{font:MONO,anchor:"end"});
  let d="";for(let i=0;i<=240;i++){const s=1+i/240,v=Math.log(xi(s));
    if(!isFinite(v))continue;d+=(i===0?"M ":" L ")+sx(s).toFixed(2)+" "+vy(v).toFixed(2);}
  const curve=E("path",{d:d,fill:"none",stroke:C.cyan,"stroke-width":"2.2","stroke-linecap":"round"},plot);
  const CL=curve.getTotalLength();curve.setAttribute("stroke-dasharray",CL);curve.setAttribute("stroke-dashoffset",CL);
  const pts=[];for(let i=0;i<=80;i++){const s=1+i/80;pts.push(sx(s).toFixed(1)+","+vy(LN1+PSI*(s-1)).toFixed(1));}
  const tan=E("polyline",{points:pts.join(" "),fill:"none",stroke:C.gold,"stroke-width":"2"},plot);
  const TL=tan.getTotalLength();tan.setAttribute("stroke-dasharray",TL);tan.setAttribute("stroke-dashoffset",TL);
  const tri=E("g",{},plot);
  const tx1=sx(1),tx2=sx(2),ty1=vy(LN1),ty2=vy(LN1+PSI);
  E("line",{x1:tx1,y1:ty1,x2:tx2,y2:ty1,stroke:C.gold,"stroke-opacity":".52","stroke-dasharray":"5 5","stroke-width":"1.4"},tri);
  E("line",{x1:tx2,y1:ty1,x2:tx2,y2:ty2,stroke:C.gold,"stroke-width":"1.6"},tri);
  T(tri,(tx1+tx2)/2,ty1+28,17,C.gold,"run = 1.0",{font:MONO,anchor:"middle"});
  T(tri,tx2+12,(ty1+ty2)/2+6,17,C.gold,"rise = 0.0231",{font:MONO});
  const chk=E("g",{},plot);
  T(chk,1320,470,18,C.dim,"数值微分",{font:MONO});
  T(chk,1320,500,19,C.text,NUM.toFixed(12),{font:MONO});
  T(chk,1320,548,18,C.dim,"解析值",{font:MONO});
  T(chk,1320,578,19,C.text,"0.023095708966",{font:MONO});
  T(chk,1320,626,19,C.cyan,"差 = "+DIFF.toExponential(1),{font:MONO});
  smallLabel(chk,1320,430,"切线斜率 = 相变量子",C.gold);
  plot.setAttribute("opacity","0");
  F.f._box=box._rect;
  return {F:F,d2:d2,plot:plot,curve:curve,CL:CL,tan:tan,TL:TL,tri:tri,chk:chk,NUM:NUM,DIFF:DIFF};
})();

/* ============================================================
   段 3 · 60–96 s  常数是坐标（七因子乘积 · 琥珀）
   ============================================================ */
const S3=(function(){
  const p=G[2];
  const vals=[
    {n:"☯",v:"0.02309570897",s:"ξ 对数导数"},
    {n:"𝔠₁",v:"200.04045483",s:"¼ + γ₁²"},
    {n:"λc",v:"1.316022911",s:"Mathieu 临界"},
    {n:"I",v:"5/3",s:"Dynkin 指数比"},
    {n:"κ",v:"1.034103190",s:"(31+☯)/30"},
    {n:"mp",v:"0.9382720882",s:"质子质量 · 实验输入"},
    {n:"ℏc",v:"换算因子",s:"恢复量纲"}
  ];
  const slots=E("g",{},p),cells=[];
  vals.forEach((v,i)=>{
    const x=160+i*226,w=206;
    const g=group(slots,x,410,w,116,{stroke:i===5?C.amber:C.faint,sw:i===5?1.8:1.1});
    T(g,x+14,448,22,i===5?C.amber:C.gold,v.n,{font:MATH});
    T(g,x+14,486,23,C.text,v.v,{font:MONO});
    T(g,x+14,514,15,C.dim,v.s,{font:ZH});
    if(i===5)T(g,x+14,388,15,C.amber,"唯一实验输入",{font:ZH});
    g.setAttribute("opacity","0");cells.push(g);
  });
  smallLabel(slots,160,370,"七个位置 · 六个组合-谱不变量 ＋ 一个实验输入",C.dim);
  // 乘积式三块
  const prod=E("g",{},p);
  const a=FT(prod,160,620,34,C.white,[{t:"I · λ"},{t:"c",sub:1},{t:" · ☯² · 𝔠₁ / "},{t:"m",it:1},{t:"p",sub:1},{t:"²"}]);
  const aw=a.getComputedTextLength();
  T(prod,160+aw+30,620,32,C.cyan,"= 2.658490028 × 10",{font:MONO});
  const aw2=prod.lastChild.getComputedTextLength();
  T(prod,160+aw+30+aw2-2,606,20,C.cyan,"−1",{font:MONO});
  const b=FT(prod,160,682,34,C.white,[{t:"exp(−2/☯) = exp(−86.596)"}]);
  T(prod,1020,682,32,C.cyan,"= 2.464677412 × 10",{font:MONO});
  T(prod,1020,666,20,C.cyan,"−38",{font:MONO});
  const c=FT(prod,160,744,34,C.white,[{t:"(1 + "},{t:"κ",it:1},{t:"☯) = 1.023883346"}]);
  // 量级塌缩
  const fall=E("g",{},p);
  E("line",{x1:1400,y1:390,x2:1400,y2:800,stroke:C.faint,"stroke-width":"1"},fall);
  T(fall,1420,406,18,C.dim,"10⁰",{font:MONO});
  const fallDot=E("circle",{cx:1400,cy:400,r:7,fill:C.cyan},fall);
  T(fall,1420,800,18,C.cyan,"10⁻³⁸",{font:MONO});
  smallLabel(fall,1300,352,"量级塌缩",C.cyan);
  // 结果框
  const res=group(p,160,762,900,84,{stroke:C.cyan,sw:1.6,fill:C.cyan,fillOp:".06"});
  FT(res,182,818,36,C.gold,[{t:"G",it:1},{t:"N",sub:1},{t:" = "}]);
  const rt=T(res,270,818,34,C.cyan,"6.708811657 × 10",{font:MONO});
  const rw=rt.getComputedTextLength();
  T(res,270+rw+2,802,21,C.cyan,"−39",{font:MONO});
  T(res,270+rw+44,818,27,C.dim,"GeV⁻²",{font:MONO});
  // 比对条
  const cmp=E("g",{},p);
  smallLabel(cmp,1120,410,"与实验值逐位比对",C.dim);
  T(cmp,1120,462,26,C.cyan,"6.708811657",{font:MONO});
  T(cmp,1120,504,26,C.white,"6.708832159",{font:MONO});
  T(cmp,1120,548,20,C.dim,"比值 0.9999969439",{font:MONO});
  const ppm=group(cmp,1120,580,360,70,{stroke:C.amber,dash:"6 5",sw:1.6});
  T(ppm,1140,626,28,C.amber,"偏差 −3 ppm",{font:MONO});
  T(cmp,1120,690,20,C.amber,"乘积结构为框架内构造",{font:ZH});
  // SI
  const si=E("g",{},p);
  smallLabel(si,1120,740,"乘以 ℏc 恢复 SI 单位",C.dim);
  T(si,1120,786,25,C.text,"6.6742810045 × 10⁻¹¹ m³kg⁻¹s⁻²",{font:MONO});
  // 空框（开场）
  const empty=group(p,160,762,900,84,{stroke:C.amber,dash:"8 6",sw:1.6});
  FT(empty,182,818,36,C.dim,[{t:"G",it:1},{t:"N",sub:1},{t:" = ?"}]);
  smallLabel(empty,160,744,"乘积结构：框架内构造，无统一变分原理",C.amber);
  return {cells:cells,slots:slots,prod:prod,fall:fall,fallDot:fallDot,
    res:res,cmp:cmp,si:si,empty:empty};
})();

/* ============================================================
   段 4 · 96–128 s  一张谱定三种耦合（矩阵长谱 hero）
   ============================================================ */
const S4=(function(){
  const p=G[3];
  const M=[
    [3,1,1,1,1,0,1,1,0,0],[1,3,1,1,0,1,1,0,1,0],[1,1,3,0,1,1,0,1,1,0],
    [1,1,0,3,1,1,1,0,0,1],[1,0,1,1,3,1,0,1,0,1],[0,1,1,1,1,3,0,0,1,1],
    [1,1,0,1,0,0,3,1,1,1],[1,0,1,0,1,0,1,3,1,1],[0,1,1,0,0,1,1,1,3,1],
    [0,0,0,1,1,1,1,1,1,3]];
  const mat=E("g",{},p),cells=[];
  const MX=170,MY=380,CS=34;
  for(let i=0;i<10;i++)for(let j=0;j<10;j++){
    const x=MX+j*CS,y=MY+i*CS;
    E("rect",{x:x,y:y,width:CS-2,height:CS-2,rx:1,fill:"#0E1522",stroke:C.faint,"stroke-width":".7"},mat);
    const t=T(mat,x+(CS-2)/2,y+CS-9,17,M[i][j]===3?C.gold:(M[i][j]===1?C.text:C.dim),
      String(M[i][j]),{font:MONO,anchor:"middle",opacity:"0"});
    cells.push(t);
  }
  smallLabel(mat,MX,352,"M = EᵀE  ·  10 × 10  ·  元素只取 0 / 1 / 3",C.cyan);
  const rowSum=E("g",{},mat);
  T(rowSum,MX+10*CS+26,MY+18,20,C.cyan,"行和 = 9",{font:MONO});
  // 单纯形骨架（右上角，作几何来源提示）
  const sk=E("g",{},p);
  const cxp=1480,cyp=560,R=128,verts=[];
  for(let i=0;i<5;i++){const a=-Math.PI/2+i*2*Math.PI/5;
    verts.push([cxp+R*Math.cos(a),cyp+R*Math.sin(a)]);}
  for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)
    E("line",{x1:verts[i][0],y1:verts[i][1],x2:verts[j][0],y2:verts[j][1],
      stroke:C.cyan,"stroke-opacity":".26","stroke-width":"1.2"},sk);
  verts.forEach(v=>E("circle",{cx:v[0],cy:v[1],r:4.5,fill:C.gold},sk));
  T(sk,cxp,720,17,C.dim,"5 顶点 · 10 边 · 10 三角形",{font:ZH,anchor:"middle"});
  // 陈述卡 / 迹条件 / 联立
  const schur=group(p,1100,380,660,62,{stroke:C.white,sw:1.2});
  T(schur,1120,422,26,C.white,"10 = 1 ⊕ 4 ⊕ 5",{font:MONO});
  T(schur,1120,462,17,C.dim,"Schur 引理 · 外部标准表示论",{font:ZH});
  const tr=E("g",{},p);
  FT(tr,1100,540,30,C.white,[{t:"Tr "},{t:"M",it:1},{t:" = 30"}]);
  FT(tr,1100,586,30,C.white,[{t:"Tr "},{t:"M",it:1},{t:"² = 150"}]);
  smallLabel(tr,1100,506,"计数 · 10 × 3 / 度数计数",C.cyan);
  const eqs=E("g",{},p);
  FT(eqs,1100,540,28,C.white,[{t:"9 + 4"},{t:"λ",it:1},{t:"₄ + 5"},{t:"λ",it:1},{t:"₅ = 30"}]);
  FT(eqs,1100,586,28,C.white,[{t:"81 + 4"},{t:"λ",it:1},{t:"₄² + 5"},{t:"λ",it:1},{t:"₅² = 150"}]);
  smallLabel(eqs,1100,506,"联立求根",C.cyan);
  // 谱轴（三条谱带，平行线数＝重数）
  const spec=E("g",{},p);
  E("line",{x1:170,y1:800,x2:840,y2:800,stroke:C.faint,"stroke-width":"1"},spec);
  E("line",{x1:170,y1:800,x2:170,y2:390,stroke:C.faint,"stroke-width":"1"},spec);
  T(spec,170,836,17,C.dim,"谱轴 σ(M)",{font:MONO});
  const bands=[{v:9,mult:1,x:300,c:C.gold,label:"9  → SU(3)"},
               {v:4,mult:4,x:490,c:C.cyan,label:"4  → SU(2)"},
               {v:1,mult:5,x:680,c:C.purple,label:"1  → U(1)"}];
  const bandEls=[];
  bands.forEach(bd=>{
    const g=E("g",{},spec);
    const h=bd.v/9*330;
    for(let k=0;k<bd.mult;k++){
      const ln=E("line",{x1:bd.x+k*9,y1:800,x2:bd.x+k*9,y2:800-h,
        stroke:bd.c,"stroke-width":"3","stroke-linecap":"round"},g);
      const L=ln.getTotalLength();ln.setAttribute("stroke-dasharray",L);ln.setAttribute("stroke-dashoffset",L);
      g._lines=g._lines||[];g._lines.push({el:ln,L:L});
    }
    T(g,bd.x-14,800-h-18,20,bd.c,String(bd.v),{font:MONO});
    T(g,bd.x-30,862,16,C.dim,bd.label,{font:MONO});
    g.setAttribute("opacity","0");bandEls.push(g);
  });
  const roots=E("g",{},p);
  const rb=group(roots,1090,640,660,76,{stroke:C.cyan,sw:1.6,fill:C.cyan,fillOp:".07"});
  FT(rb,1110,690,32,C.cyan,[{t:"σ("},{t:"M",it:1},{t:") = {9⁽¹⁾, 4⁽⁴⁾, 1⁽⁵⁾}"}]);
  smallLabel(roots,1090,620,"精确解 · 重数 1 + 4 + 5 = 10",C.cyan);
  // α 并排（待推，不得演成从谱导出）
  const alpha=group(p,1090,742,660,112,{stroke:C.amber,dash:"7 6",sw:1.6,fill:C.amber,fillOp:".05"});
  T(alpha,1110,780,22,C.amber,"待推 · 从谱到 π 因子的那一步没有推导",{font:ZH});
  T(alpha,1110,818,21,C.text,"16384π/375 = 137.2583",{font:MONO});
  T(alpha,1110,846,19,C.dim,"实验 137.035999 · 差 0.162%",{font:MONO});
  return {mat:mat,cells:cells,rowSum:rowSum,sk:sk,schur:schur,tr:tr,eqs:eqs,
    spec:spec,bandEls:bandEls,roots:roots,alpha:alpha};
})();

/* ============================================================
   段 5 · 128–156 s  时间与引力（角亏的钟 hero）
   ============================================================ */
const S5=(function(){
  const p=G[4];
  const f={};
  ["a","b","c","d"].forEach(k=>{f[k]=E("g",{},p);f[k].setAttribute("opacity","0");});
  FT(f.a,150,210,38,C.white,[{t:"L",it:1},{t:"ab",sub:1},{t:"² = "},{t:"L",it:1},{t:"va",sub:1},{t:"² + "},{t:"L",it:1},{t:"vb",sub:1},
    {t:"² − 2"},{t:"L",it:1},{t:"va",sub:1},{t:"L",it:1},{t:"vb",sub:1},{t:" cos "},{t:"θ",it:1},{t:"v",sub:1}]);
  smallLabel(f.a,150,158,"余弦定律 · 外部标准",C.white);
  FT(f.b,150,210,38,C.white,[{t:"θ",it:1},{t:"v",sub:1},{t:" = arccos("},{t:")"}]);
  T(f.b,410,210,26,C.dim,"(Lva² + Lvb² − Lab²) / 2LvaLvb",{font:MONO});
  smallLabel(f.b,150,158,"反解",C.cyan);
  FT(f.c,150,210,44,C.white,[{t:"δ",it:1},{t:"v",sub:1},{t:" = 2"},{t:"π",it:1},{t:" − Σ "},{t:"θ",it:1},{t:"v",sub:1},{t:"(Δ)"}]);
  smallLabel(f.c,150,158,"对 6 个三角形求和",C.cyan);
  // 顶点与六个三角形
  const geo=E("g",{},p);
  const vx=620,vy=600,R=180;
  const wedges=E("g",{},geo),wedgeLabels=[];
  for(let i=0;i<6;i++){
    const a0=-Math.PI/2+i*Math.PI/3, a1=a0+Math.PI/3;
    const g=E("path",{d:`M ${vx} ${vy} L ${vx+R*Math.cos(a0)} ${vy+R*Math.sin(a0)} A ${R} ${R} 0 0 1 ${vx+R*Math.cos(a1)} ${vy+R*Math.sin(a1)} Z`,
      fill:C.cyan,"fill-opacity":".045",stroke:C.cyan,"stroke-opacity":".32","stroke-width":"1.2"},wedges);
    const lt=T(wedges,vx+125*Math.cos(a0+Math.PI/6),vy+125*Math.sin(a0+Math.PI/6),16,C.dim,"π/3",
      {font:MATH,anchor:"middle",opacity:"0"});
    wedgeLabels.push(lt);
  }
  E("circle",{cx:vx,cy:vy,r:6,fill:C.gold},geo);
  T(geo,vx,380,18,C.dim,"理想正 4-单纯形：6 × π/3 = 2π  ⇒  δv = 0",{font:MATH,anchor:"middle"});
  const gapArc=E("path",{d:`M ${vx} ${vy} L ${vx+R*Math.cos(-Math.PI/2)} ${vy+R*Math.sin(-Math.PI/2)} A ${R} ${R} 0 0 1 ${vx+R*Math.cos(-Math.PI/2+0.02*Math.PI)} ${vy+R*Math.sin(-Math.PI/2+0.02*Math.PI)} Z`,
    fill:C.amber,"fill-opacity":".5",stroke:C.amber,"stroke-width":"1.5"},geo);
  gapArc.setAttribute("opacity","0");
  T(geo,vx+40,460,19,C.amber,"δv > 0",{font:MATH,opacity:"0"}).setAttribute("id","gapLabel");
  const gapLabel=geo.lastChild;
  smallLabel(geo,150,860,"示意形变：Σθv = 1.98π ⇒ δv = 0.02π（示意值，不是理论预言）",C.amber);
  // 琥珀虚框：FG 因果假设
  const hyp=group(p,1080,150,700,140,{stroke:C.amber,dash:"7 6",sw:1.8,fill:C.amber,fillOp:".06"});
  FT(hyp,1100,210,38,C.white,[{t:"d"},{t:"τ",it:1},{t:"/"},{t:"dt",it:1},{t:" = √(1 − "},{t:"β",it:1},{t:"δ",it:1},{t:"v",sub:1},{t:")"}]);
  T(hyp,1100,246,19,C.amber,"FG 的因果假设 · 无推导 · β 的微观来源属待推",{font:ZH});
  T(hyp,1100,276,17,C.dim,"GR 弱场对照：dτ/dt ≈ 1 + Φ/c²（外部标准）",{font:ZH});
  // 钟
  const clk=E("g",{},p);
  const cx=1420,cy=690,cr=132;
  E("circle",{cx:cx,cy:cy,r:cr,fill:"none",stroke:C.faint,"stroke-width":"1.5"},clk);
  for(let i=0;i<12;i++){const a=-Math.PI/2+i*Math.PI/6;
    E("line",{x1:cx+(cr-14)*Math.cos(a),y1:cy+(cr-14)*Math.sin(a),
      x2:cx+cr*Math.cos(a),y2:cy+cr*Math.sin(a),stroke:C.dim,"stroke-width":"1.4"},clk);}
  const hand=E("line",{x1:cx,y1:cy,x2:cx,y2:cy-cr+34,stroke:C.gold,"stroke-width":"2.6","stroke-linecap":"round"},clk);
  const t1=E("line",{x1:cx-16,y1:cy-30,x2:cx+16,y2:cy-30,stroke:C.cyan,"stroke-width":"1.6"},clk);
  T(clk,cx,cy+cr+40,19,C.dim,"间隔 1.000 s → 1.020 s（β 取示意值）",{font:MONO,anchor:"middle"});
  smallLabel(clk,1080,560,"同一枚钟 · 锁定次数变少",C.gold);
  return {f:f,geo:geo,wedges:wedges,wedgeLabels:wedgeLabels,gapArc:gapArc,gapLabel:gapLabel,
    hyp:hyp,clk:clk,hand:hand,cx:cx,cy:cy,cr:cr};
})();

/* ============================================================
   段 6 · 156–180 s  下潜与边界
   ============================================================ */
const S6=(function(){
  const p=G[5];
  // 四层叠片
  const layers=E("g",{},p),layerEls=[];
  ["电子 FG","元素 FG","分子 FG","晶胞 FG"].forEach((s,i)=>{
    const y=380+i*66;
    const g=E("g",{},layers);
    E("path",{d:`M 170 ${y} L 600 ${y} L 640 ${y+34} L 210 ${y+34} Z`,
      fill:C.cyan,"fill-opacity":".045",stroke:C.cyan,"stroke-opacity":".4","stroke-width":"1.2"},g);
    T(g,190,y+25,19,C.text,s,{font:ZH});
    g.setAttribute("opacity","0");layerEls.push(g);
  });
  smallLabel(layers,170,352,"同一套链往下走一层",C.cyan);
  // 设定虚框
  const setg=group(p,170,660,660,96,{stroke:C.amber,dash:"7 6",sw:1.8,fill:C.amber,fillOp:".06"});
  FT(setg,190,706,30,C.white,[{t:"λ",it:1},{t:"n",sub:1},{t:"(T) = "},{t:"γ",it:1},{t:"n",sub:1},{t:" − "},{t:"V",it:1},{t:"(n, T)"}]);
  T(setg,190,740,18,C.amber,"V 的形式：框架设定 · 无推导",{font:ZH});
  T(setg,600,690,16,C.amber,"设定",{font:ZH});
  // 交叉曲线
  const cross=E("g",{},p);
  const X0=940,X1=1700,Y0=410,Y1=780,u=x=>X0+x*(X1-X0),v=y=>Y1-y*(Y1-Y0);
  E("line",{x1:X0,y1:Y1,x2:X1,y2:Y1,stroke:C.faint,"stroke-width":"1"},cross);
  E("line",{x1:X0,y1:Y0,x2:X0,y2:Y1,stroke:C.faint,"stroke-width":"1"},cross);
  T(cross,X1+10,Y1+30,17,C.dim,"T",{font:MATH});
  T(cross,X0-30,Y0-12,17,C.dim,"λn",{font:MATH});
  const tc=0.70/1.02, yc=0.86-0.62*tc;
  const l1=E("line",{x1:u(0),y1:v(0.86),x2:u(1),y2:v(0.86-0.62),stroke:C.cyan,"stroke-width":"2.4"},cross);
  const l2=E("line",{x1:u(0),y1:v(0.16),x2:u(1),y2:v(0.16+0.40),stroke:C.gold,"stroke-width":"2.4"},cross);
  [l1,l2].forEach(l=>{const L=l.getTotalLength();l.setAttribute("stroke-dasharray",L);l.setAttribute("stroke-dashoffset",L);});
  const vl=E("line",{x1:u(tc),y1:Y1,x2:u(tc),y2:v(yc),stroke:C.white,"stroke-dasharray":"5 5","stroke-width":"1.3"},cross);
  const dot=E("circle",{cx:u(tc),cy:v(yc),r:7,fill:C.white},cross);
  T(cross,u(tc),Y1+30,18,C.white,"Tc",{font:MATH,anchor:"middle"});
  smallLabel(cross,X0,370,"本征值交叉 · 机制形状，不是材料承诺",C.cyan);
  const tcF=group(p,940,806,760,62,{stroke:C.cyan,sw:1.3});
  FT(tcF,960,848,29,C.cyan,[{t:"T",it:1},{t:"c",sub:1},{t:" = "},{t:"θ",it:1},{t:"D",sub:1},{t:" / (2 arccoth "},{t:"x",it:1},{t:") · "},{t:"x",it:1},{t:" > 1"}]);
  // 边界计数
  const bound=E("g",{},p);
  smallLabel(bound,170,352,"边界 · 能算到这里，不等于已经证完",C.amber);
  const nums=[["74","模块"],["1439","声明"],["857","theorem"],["15","axiom"]];
  nums.forEach((n,i)=>{
    const x=170+i*180;
    const g=group(bound,x,410,158,96,{stroke:C.faint,sw:1.1});
    T(g,x+79,462,30,C.cyan,n[0],{font:MONO,anchor:"middle"});
    T(g,x+79,492,17,C.dim,n[1],{font:ZH,anchor:"middle"});
  });
  T(bound,170,556,19,C.dim,"缺口编号：C · G2–G8 · G9–G22 · N1–N4 · H3.1–H3.3",{font:MONO});
  const neq=group(bound,170,586,700,64,{stroke:C.amber,dash:"7 6",sw:1.7,fill:C.amber,fillOp:".05"});
  T(neq,192,630,25,C.amber,"编译通过数  ≠  缺口闭合数",{font:ZH});
  const finalG=E("g",{},p);
  T(finalG,960,700,52,C.text,"能算到这里，不等于已经证完。",{font:ZH,anchor:"middle"});
  T(finalG,960,752,20,C.dim,"框架内构造 · 待推 · 构造后验数字校验，待独立复现",{font:ZH,anchor:"middle"});
  // 断边 4-单纯形轮廓（保留断口）
  const brk=E("g",{},p);
  const bv=[[1300,430],[1560,430],[1640,600],[1440,710],[1240,600]];
  for(let i=0;i<5;i++){
    if(i===2)continue;
    const a=bv[i],b=bv[(i+1)%5];
    if(i===1||i===3)continue;
    E("line",{x1:a[0],y1:a[1],x2:b[0],y2:b[1],stroke:C.amber,"stroke-opacity":".55","stroke-width":"1.6"},brk);
  }
  E("line",{x1:bv[1][0],y1:bv[1][1],x2:bv[2][0]-26,y2:bv[2][1]-18,stroke:C.amber,"stroke-opacity":".55","stroke-width":"1.6"},brk);
  E("line",{x1:bv[3][0],y1:bv[3][1],x2:bv[2][0]-26,y2:bv[2][1]+18,stroke:C.amber,"stroke-opacity":".55","stroke-width":"1.6"},brk);
  T(brk,1440,760,17,C.amber,"断口保留",{font:ZH,anchor:"middle"});
  return {layers:layers,layerEls:layerEls,setg:setg,cross:cross,l1:l1,l2:l2,vl:vl,dot:dot,
    tcF:tcF,bound:bound,finalG:finalG,brk:brk,u:u,tc:tc};
})();

/* ============ 跨段共享元素：☯ 常驻小标记 ============ */

const carryBox=group(carryG,1480,44,290,42,{stroke:C.gold,sw:1.1,fill:C.gold,fillOp:".05"});
T(carryG,1498,72,20,C.gold,"☯ = 0.023095708966",{font:MONO});
carryG.setAttribute("opacity","0");

/* ============ 演算刻度尺 ============ */
const RAIL={x:60,y0:400,y1:880,n:24};
const ticks=[];
for(let i=0;i<RAIL.n;i++){
  const y=RAIL.y0+i*(RAIL.y1-RAIL.y0)/(RAIL.n-1);
  ticks.push(E("rect",{x:RAIL.x,y:y,width:5,height:9,fill:C.faint},railG));
}

let badgeKey="";
function setBadge(shape,color,label){
  const key=shape+"|"+color+"|"+label;
  if(key===badgeKey)return;badgeKey=key;badgeG.innerHTML="";
  const x=1782,y=980;
  if(shape==="ring")E("circle",{cx:x,cy:y,r:10,fill:"none",stroke:color,"stroke-width":"1.6"},badgeG);
  if(shape==="tri")E("path",{d:`M ${x} ${y-11} L ${x+10} ${y+8} L ${x-10} ${y+8} Z`,fill:"none",stroke:color,"stroke-width":"1.6"},badgeG);
  if(shape==="square")E("rect",{x:x-9,y:y-9,width:18,height:18,rx:2,fill:"none",stroke:color,"stroke-width":"1.6"},badgeG);
  if(shape==="purple")E("circle",{cx:x,cy:y,r:10,fill:"none",stroke:color,"stroke-width":"1.6","stroke-dasharray":"4 3"},badgeG);
  if(shape==="broken"){
    E("path",{d:`M ${x+10} ${y} A 10 10 0 1 1 ${x+2} ${y-9.8}`,fill:"none",stroke:color,"stroke-width":"1.7"},badgeG);
  }
  T(badgeG,x-20,y+6,19,color,label,{font:ZH,anchor:"end"});
}

/* ============ 确定性渲染 ============ */
function segOp(i,t){
  const s=SEGS[i];
  if(t<s.a||t>s.b)return 0;
  let o=1;
  if(i>0&&t<s.a+0.55)o=easeOut((t-s.a)/0.55);
  if(t>s.b-0.35)o=Math.min(o,1-easeOut((t-(s.b-0.35))/0.35));
  return o;
}

  function segIndex(t){let k=0;for(let i=0;i<6;i++)if(t>=SEGS[i].a)k=i;return k;}

function renderAt(t){
  t=clamp(t,0,TOTAL);
  const seg=segIndex(t);
  for(let i=0;i<6;i++)G[i].setAttribute("opacity",segOp(i,t).toFixed(3));

  /* --- 段 1 --- */
  {
    const s=S1;
    const gi=easeOut(clamp(t/1.1,0,1));
    let g=gi;
    if(t>4.5)g=Math.max(0.08,0.92*(1-easeOut(clamp((t-4.5)/1.4,0,1))));
    if(t>7)g=Math.max(0,0.08*(1-easeOut(clamp((t-7)/1.0,0,1))));
    s.grid.setAttribute("opacity",g.toFixed(3));
    const sp=clamp((t-4.8)/0.3,0,1);
    s.strike.setAttribute("opacity",sp>0?String(0.95*(1-clamp((t-6.6)/1.2,0,1))):"0");
    s.a.setAttribute("stroke-dashoffset",(s.la*(1-easeOut(sp))).toFixed(1));
    s.b.setAttribute("stroke-dashoffset",(s.lb*(1-easeOut(clamp((t-4.94)/0.3,0,1)))).toFixed(1));
    const ai=clamp((t-7)/0.9,0,1);
    s.axis.setAttribute("opacity",ai.toFixed(3));
    s.ln.setAttribute("stroke-dashoffset",(s.LL*(1-easeOut(ai))).toFixed(1));
    const dp=clamp((t-7.6)/1.1,0,1);
    s.dot.setAttribute("cy",lerp(300,s.AX.y,easeOut(dp)).toFixed(2));
    s.dot.setAttribute("opacity",dp.toFixed(2));
    const bw=58*easeOut(clamp((t-12.6)/0.7,0,1));
    s.band.setAttribute("x1",(s.AX.u0-bw).toFixed(1));s.band.setAttribute("x2",(s.AX.u0+bw).toFixed(1));
    vis(s.f1,t,1.2,4.5);vis(s.f2,t,9.2,12.5);vis(s.f3,t,12.5,15.0);vis(s.f4,t,15.0,26.0);
    s.chain.setAttribute("opacity",easeOut(clamp((t-9.2)/0.5,0,1)).toFixed(2));
    [9.5,12.5,15.0,21.0].forEach((a,i)=>s.chainRows[i].setAttribute("opacity",
      easeOut(clamp((t-a)/0.5,0,1)).toFixed(2)));
    const qp=t>15.2&&t<16.0?Math.sin((t-15.2)/0.8*Math.PI):0;
    s.slot.setAttribute("stroke-opacity",(0.55+0.45*qp).toFixed(2));
    if(t>=21){s.slotQ.textContent="☯";s.slotQ.setAttribute("font-family",SYM);
      s.slotQ.setAttribute("font-size","26");s.slotQ.setAttribute("fill",C.cyan);}
    else{s.slotQ.textContent="?";s.slotQ.setAttribute("font-family",MATH);
      s.slotQ.setAttribute("font-size","30");s.slotQ.setAttribute("fill",C.amber);}
  }
  /* --- 段 2 --- */
  {
    const s=S2,F=s.F;
    vis(F.a,t,28.0,32.0);vis(F.b,t,32.0,36.0);vis(F.c,t,36.0,40.0);
    vis(F.d,t,40.0,44.0);vis(F.e,t,44.0,48.0);vis(F.f,t,48.0,60.0);
    s.d2.setAttribute("opacity",clamp((t-41.2)/0.4,0,1).toFixed(2));
    const pi=easeOut(clamp((t-50.6)/0.6,0,1));
    s.plot.setAttribute("opacity",pi.toFixed(3));
    const cd=clamp((t-51.0)/3.0,0,1);
    s.curve.setAttribute("stroke-dashoffset",(s.CL*(1-easeOut(cd))).toFixed(1));
    const td=clamp((t-52.2)/1.2,0,1);
    s.tan.setAttribute("opacity",td.toFixed(2));
    s.tan.setAttribute("stroke-dashoffset",(s.TL*(1-easeOut(td))).toFixed(1));
    s.tri.setAttribute("opacity",clamp((t-53.0)/0.9,0,1).toFixed(2));
    s.chk.setAttribute("opacity",clamp((t-55.4)/0.7,0,1).toFixed(2));
  }
  /* --- carry ☯ --- */
  carryG.setAttribute("opacity",(easeOut(clamp((t-48.0)/0.6,0,1))*(1-easeOut(clamp((t-95.0)/1.0,0,1)))).toFixed(3));
  /* --- 段 3 --- */
  {
    const s=S3;
    s.cells.forEach((c,i)=>{
      const a=62.4+i*1.05;
      c.setAttribute("opacity",easeOut(clamp((t-a)/0.45,0,1)).toFixed(3));
    });
    vis(s.slots,t,60.6,82.0,0.3,0.7);
    vis(s.empty,t,60.2,68.0,0.4,0.4);
    vis(s.prod,t,69.5,82.0,0.35,0.35);
    vis(s.fall,t,73.5,80.0,0.3,0.35);
    const fp=clamp((t-74.2)/2.2,0,1);
    s.fallDot.setAttribute("cy",lerp(400,800,easeIO(fp)).toFixed(1));
    vis(s.res,t,81.6,96.0,0.35,0.35);
    vis(s.cmp,t,84.4,96.0,0.3,0.35);
    vis(s.si,t,91.0,96.0,0.3,0.35);
  }
  /* --- 段 4 --- */
  {
    const s=S4;
    const matOut=1-easeOut(clamp((t-115.0)/1.0,0,1));
    s.mat.setAttribute("opacity",(easeOut(clamp((t-96.2)/0.6,0,1))*matOut).toFixed(3));
    s.cells.forEach((c,i)=>{
      const row=Math.floor(i/10),a=99.0+row*0.52;
      c.setAttribute("opacity",(easeOut(clamp((t-a)/0.22,0,1))*0.92*matOut).toFixed(2));
    });
    s.rowSum.setAttribute("opacity",(clamp((t-103.0)/0.5,0,1)*matOut).toFixed(2));
    const skOut=1-easeOut(clamp((t-118.4)/1.0,0,1));
    s.sk.setAttribute("opacity",(0.75*easeOut(clamp((t-96.4)/0.8,0,1))*skOut).toFixed(2));
    vis(s.schur,t,104.6,108.4,0.3,0.3);
    vis(s.tr,t,108.4,112.2,0.3,0.3);
    vis(s.eqs,t,112.2,116.2,0.3,0.3);
    vis(s.spec,t,115.4,128.0,0.35,0.35);
    s.bandEls.forEach((g,i)=>{
      const a=116.0+i*1.5;
      g.setAttribute("opacity",easeOut(clamp((t-a)/0.4,0,1)).toFixed(2));
      const pr=clamp((t-a)/1.0,0,1);
      g._lines.forEach((ln,k)=>{
        const p=clamp((pr-k*0.08)/0.55,0,1);
        ln.el.setAttribute("stroke-dashoffset",(ln.L*(1-easeOut(p))).toFixed(1));
      });
    });
    vis(s.roots,t,116.8,124.0,0.3,0.3);
    vis(s.alpha,t,123.6,128.0,0.3,0.35);
  }
  /* --- 段 5 --- */
  {
    const s=S5;
    vis(s.f.a,t,128.2,131.2,0.3,0.3);
    vis(s.f.b,t,131.2,134.2,0.3,0.3);
    vis(s.f.c,t,134.2,141.0,0.3,0.3);
    vis(s.geo,t,133.8,156.0,0.35,0.35);
    s.wedgeLabels.forEach((lt,i)=>lt.setAttribute("opacity",
      easeOut(clamp((t-(133.9+i*0.32))/0.3,0,1)).toFixed(2)));
    const gp=clamp((t-138.0)/0.8,0,1);
    s.gapArc.setAttribute("opacity",gp.toFixed(2));
    s.gapLabel.setAttribute("opacity",gp.toFixed(2));
    wedgesShift(s.wedges,t);
    vis(s.hyp,t,140.8,156.0,0.3,0.35);
    vis(s.clk,t,144.4,156.0,0.35,0.35);
    // 钟：间隔由 dτ/dt 决定（示意），两段时间刻度不同
    const slowed=t>=147.0;
    const rate=slowed?1/1.020:1/1.000;
    const ang=(t-144.4)*rate*2*Math.PI/4-Math.PI/2;
    s.hand.setAttribute("x2",(s.cx+(s.cr-34)*Math.cos(ang)).toFixed(2));
    s.hand.setAttribute("y2",(s.cy+(s.cr-34)*Math.sin(ang)).toFixed(2));
  }
  /* --- 段 6 --- */
  {
    const s=S6;
    vis(s.layers,t,156.2,169.4,0.3,0.35);
    s.layerEls.forEach((g,i)=>g.setAttribute("opacity",
      easeOut(clamp((t-(156.3+i*0.8))/0.5,0,1)).toFixed(2)));
    vis(s.setg,t,158.6,169.4,0.3,0.35);
    vis(s.cross,t,162.4,169.4,0.35,0.35);
    const cd=clamp((t-162.6)/2.4,0,1);
    [s.l1,s.l2].forEach(l=>{const L=l.getTotalLength();
      l.setAttribute("stroke-dashoffset",(L*(1-easeOut(cd))).toFixed(1));});
    const dp=clamp((t-165.0)/0.5,0,1);
    s.vl.setAttribute("opacity",dp.toFixed(2));s.dot.setAttribute("opacity",dp.toFixed(2));
    vis(s.tcF,t,166.6,169.4,0.3,0.35);
    vis(s.bound,t,169.6,177.0,0.3,0.35);
    vis(s.brk,t,169.8,177.0,0.4,0.35);
    vis(s.finalG,t,176.6,180.0,0.45,0.2);
  }
  /* --- 刻度尺 / 字幕 / 徽章 --- */
  let lit=0;OPS.forEach(o=>{if(t>=o)lit++;});
  ticks.forEach((r,i)=>{r.setAttribute("fill",i<lit?C.cyan:C.faint);
    r.setAttribute("opacity",i<lit?"1":".55");});
  segLabel.textContent=SEGS[seg].label;
  let c=CAPS[CAPS.length-1];
  for(let i=0;i<CAPS.length;i++)if(t>=CAPS[i].a&&t<CAPS[i].b){c=CAPS[i];break;}
  capMain.textContent=c.m;
  capSub.textContent=c.s;
  capSub.setAttribute("opacity",c.s?"1":"0");
  setBadge(c.g[0],c.g[1],c.g[2]);

  // 进度 UI

}
// 顶点拉开：六个三角形整体做一个可见的位移（示意形变）
function wedgesShift(g,t){
  const p=clamp((t-138.0)/0.8,0,1);
  g.setAttribute("transform",`translate(${(p*16).toFixed(2)} ${(-p*10).toFixed(2)})`);
}

  return {render:renderAt, svg, G, cameraG, fieldG, overlayG,
    capMain, capSub, badgeG, segLabel, carryG, railG,
    CAPS, SEGS, OPS, B, C, TOTAL, S1, S2, S3, S4, S5, S6};
}

export {createKernel};
