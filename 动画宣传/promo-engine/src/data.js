// 由 tools/extract_kernel.py 从 v2 片源逐字提取。勿手改：口径门禁以此为准。
// 内容内核与新引擎共用这一份数据，不存在第二份字幕/刻度/声场表。

export const C={bg:"#070A12",text:"#E8EEF9",dim:"#7A869C",faint:"#2A3448",
  cyan:"#35E0FF",gold:"#F5C542",amber:"#FFB020",purple:"#B98CFF",white:"#F2F5FA"};

export const MATH="Cambria Math, Times New Roman, serif";
export const MONO="Consolas, monospace";
export const ZH="Microsoft YaHei, Noto Sans SC, sans-serif";
export const SYM="Segoe UI Symbol";
export const TOTAL=180;

export const RAIL={x:60,y0:400,y1:880,n:24};

export const OPS=[5.0,9.5,12.5,15.0,21.0,28.0,32.0,36.0,40.0,44.0,48.0,51.0,
  63.0,70.0,74.0,82.0,85.0,96.0,105.0,112.0,116.0,124.0,138.0,163.0];

export const SEGS=[
  {a:0,b:26,label:"01  反演 · 什么才该被量子化"},
  {a:26,b:60,label:"02  相变量子 · ξ 的切线"},
  {a:60,b:96,label:"03  常数是坐标 · 七个位置的乘积"},
  {a:96,b:128,label:"04  一张谱定三种耦合"},
  {a:128,b:156,label:"05  时间与引力 · 角亏的钟"},
  {a:156,b:180,label:"06  下潜与边界"}
];

export const B={ring:C.gold,tri:C.cyan,broken:C.amber,square:C.white,purple:C.purple};

export const CAPS=[
  {a:0,b:4.5,m:"标准量子力学：量子化位置与动量。",s:"",g:["square",C.white,"外部标准"]},
  {a:4.5,b:7,m:"CQM 的判断：该被量子化的不是位置。",s:"",g:["ring",C.gold,"框架公理"]},
  {a:7,b:9.5,m:"舞台换成耦合常数空间 u = ln r。",s:"",g:["ring",C.gold,"框架公理"]},
  {a:9.5,b:12.5,m:"在这个空间里，常数是坐标，不是随时间的漂移。",s:"",g:["ring",C.gold,"框架公理"]},
  {a:12.5,b:15,m:"位置与动量不能同时测准。",s:"",g:["square",C.white,"外部标准"]},
  {a:15,b:21,m:"把动量换成固有时流速，量子浮现为一个待定的数。",s:"",g:["tri",C.cyan,"框架内推导"]},
  {a:21,b:26,m:"量子化的对象是耦合常数本身。",s:"",g:["ring",C.gold,"框架公理"]},
  {a:26,b:28,m:"这个数是多少？",s:"",g:["ring",C.gold,"定义"]},
  {a:28,b:32,m:"它就是 ξ 的对数导数在 s = 1 的值。",s:"",g:["ring",C.gold,"定义式锚点"]},
  {a:32,b:36,m:"取对数，把六项拆开。",s:"",g:["tri",C.cyan,"框架内推导"]},
  {a:36,b:40,m:"逐项求导。",s:"",g:["tri",C.cyan,"框架内推导"]},
  {a:40,b:44,m:"s → 1 的极点项相消，只剩 γ。",s:"",g:["tri",C.cyan,"框架内推导"]},
  {a:44,b:48,m:"代入 ψ(1/2) = −γ − 2ln2。",s:"",g:["tri",C.cyan,"框架内推导"]},
  {a:48,b:51,m:"得到一个纯数：0.023095708966。",s:"",g:["tri",C.cyan,"框架内推导"]},
  {a:51,b:55.5,m:"把切线画出来，斜率就是它。",s:"",g:["tri",C.cyan,"可复算"]},
  {a:55.5,b:60,m:"数值微分与解析值一致；充当量子的是这个数，不是 ℏ。",s:"",g:["tri",C.cyan,"可复算"]},
  {a:60,b:63,m:"七个位置：六个组合-谱不变量，一个实验输入。",s:"乘积结构为框架内构造，无推导",g:["broken",C.amber,"框架内构造"]},
  {a:63,b:70,m:"逐个给定值，槽位被真正填满。",s:"乘积结构为框架内构造，无推导",g:["broken",C.amber,"框架内构造"]},
  {a:70,b:74,m:"第一次相乘：无量纲预因子 2.658490028 × 10⁻¹。",s:"乘积结构为框架内构造，无推导",g:["broken",C.amber,"框架内构造"]},
  {a:74,b:79,m:"exp(−2/☯) 让量级塌到 10⁻³⁸。",s:"乘积结构为框架内构造，无推导",g:["broken",C.amber,"框架内构造"]},
  {a:79,b:82,m:"再乘修正项 1.023883346。",s:"乘积结构为框架内构造，无推导",g:["broken",C.amber,"框架内构造"]},
  {a:82,b:85,m:"七个数相乘，得到一个数。",s:"构造后验数字校验，待独立复现",g:["broken",C.amber,"框架内构造"]},
  {a:85,b:92,m:"与实验值逐位比对，偏差 −3 ppm。",s:"构造后验数字校验，待独立复现",g:["broken",C.amber,"框架内构造"]},
  {a:92,b:96,m:"Gₙ 像是乘积的结果，不是自由输入；乘积本身是框架内构造。",s:"构造后验数字校验，待独立复现 · 唯一实验输入是 mₚ",g:["broken",C.amber,"框架内构造"]},
  {a:96,b:100,m:"边—面关联矩阵 M = EᵀE，元素只有 0 / 1 / 3。",s:"",g:["tri",C.cyan,"框架内推导"]},
  {a:100,b:105,m:"逐行点亮；每一行的和都等于 9。",s:"",g:["tri",C.cyan,"框架内推导"]},
  {a:105,b:108,m:"Schur 引理给出表示论分解。",s:"",g:["square",C.white,"外部标准"]},
  {a:108,b:112,m:"两条计数：Tr M = 30，Tr M² = 150。",s:"",g:["tri",C.cyan,"框架内推导"]},
  {a:112,b:116,m:"联立两个方程，求三个特征值。",s:"",g:["tri",C.cyan,"框架内推导"]},
  {a:116,b:121,m:"谱是 {9¹, 4⁴, 1⁵}；重数用平行线数读出来。",s:"",g:["tri",C.cyan,"框架内推导"]},
  {a:121,b:124,m:"三条谱带，对应三种规范群。",s:"",g:["tri",C.cyan,"框架内推导"]},
  {a:124,b:128,m:"到 π 因子的那一步没有推导：137.2583 与实验并排，标待推。",s:"启发式近似，非从谱导出",g:["broken",C.amber,"待推"]},
  {a:128,b:131,m:"余弦定律：从边长反解顶点处的角。",s:"",g:["square",C.white,"外部标准"]},
  {a:131,b:134,m:"对六个三角形求和，定义角亏 δv。",s:"",g:["tri",C.cyan,"框架内推导"]},
  {a:134,b:138,m:"理想正 4-单纯形：6 × π/3 = 2π，δv = 0。",s:"",g:["tri",C.cyan,"框架内推导"]},
  {a:138,b:141,m:"拉开一个顶点，围不满的那一块就是角亏。",s:"示意值，不是理论预言",g:["tri",C.cyan,"框架内推导"]},
  {a:141,b:145,m:"dτ/dt = √(1−βδv) 是 FG 的因果假设，无推导。",s:"假设 · 不是推导；β 微观来源属待推",g:["broken",C.amber,"待推／假设"]},
  {a:145,b:150,m:"钟的间隔被拉长：1.000 s → 1.020 s。",s:"β 取示意值，微观来源属待推",g:["broken",C.amber,"待推／假设"]},
  {a:150,b:156,m:"时间不是坐标，是锁定的次数；引力不是力，是角亏。",s:"",g:["purple",C.purple,"哲学诠释"]},
  {a:156,b:159,m:"同一套链往下走一层：电子／元素／分子／晶胞。",s:"",g:["tri",C.cyan,"框架内推导"]},
  {a:159,b:163,m:"V 的形式在这里被设定，不是被推导出来。",s:"框架设定 · 无推导",g:["broken",C.amber,"设定"]},
  {a:163,b:167,m:"两条本征值曲线交叉，交点定义 Tc。",s:"机制形状，不是材料承诺",g:["tri",C.cyan,"框架内推导"]},
  {a:167,b:170,m:"解出 Tc = θD / (2 arccoth x)，x > 1 给出窗口。",s:"",g:["tri",C.cyan,"框架内推导"]},
  {a:170,b:174,m:"Lean 证到哪里，缺口还剩哪些。",s:"",g:["tri",C.cyan,"框架内推导"]},
  {a:174,b:177,m:"编译通过数 ≠ 缺口闭合数。",s:"",g:["broken",C.amber,"缺口"]},
  {a:177,b:180,m:"所有琥珀标记，都保留着未闭合的断口。",s:"",g:["broken",C.amber,"待推／缺口"]}
];

export const SCORE=[
  {t:0.0,op:"bed"},{t:0.0,op:"expand",a:520,b:1180,d:1.1},
  {t:2.0,op:"pluck",f:520},{t:4.8,op:"cancel"},{t:5.1,op:"thud",f:72},
  {t:7.0,op:"expand",a:600,b:1000,d:0.7},{t:7.6,op:"sub",f:118},
  {t:9.5,op:"sub",f:110},{t:12.5,op:"sub",f:104},{t:15.0,op:"sub",f:120},
  {t:18.0,op:"glass",f:1320},{t:21.0,op:"bell",f:660},
  {t:23.0,op:"sub",f:96},{t:25.2,op:"silence"},
  {t:26.4,op:"tone",f:98,d:0.5},{t:28.0,op:"expand",a:640,b:1280,d:0.9},
  {t:32.0,op:"count",n:5},
  {t:36.0,op:"count",n:5},{t:40.0,op:"cancel"},{t:41.2,op:"thud",f:64},
  {t:44.0,op:"sub",f:112},{t:48.0,op:"bell",f:880},{t:48.0,op:"thud",f:58},
  {t:51.0,op:"expand",a:260,b:760,d:0.9},{t:53.0,op:"pluck",f:1320},
  {t:55.5,op:"glass",f:1200},{t:55.9,op:"glass",f:1210},
  {t:58.6,op:"silence"},
  {t:60.0,op:"expand",a:420,b:900,d:0.8},
  {t:62.4,op:"slot",i:0},{t:63.45,op:"slot",i:1},{t:64.5,op:"slot",i:2},
  {t:65.55,op:"slot",i:3},{t:66.6,op:"slot",i:4},{t:67.65,op:"slot",i:5},{t:68.7,op:"slot",i:6},
  {t:70.0,op:"compare",n:4},{t:74.0,op:"deficit"},{t:74.2,op:"expand",a:900,b:180,d:2.0},
  {t:79.0,op:"sub",f:132},{t:82.0,op:"bell",f:740},{t:82.0,op:"thud",f:56},
  {t:85.0,op:"compare",n:8},{t:89.0,op:"gap"},{t:91.0,op:"sub",f:100},{t:94.6,op:"silence"},
  {t:96.0,op:"expand",a:500,b:1100,d:0.9},
  {t:99.0,op:"gran",n:10},{t:103.0,op:"glass",f:1180},
  {t:105.0,op:"pluck",f:620},{t:108.0,op:"count",n:2},
  {t:112.0,op:"count",n:2},{t:116.0,op:"solve",n:3},
  {t:121.0,op:"count",n:10},{t:124.0,op:"gap"},{t:126.8,op:"silence"},
  {t:128.0,op:"expand",a:480,b:960,d:0.8},{t:131.0,op:"pluck",f:700},
  {t:134.0,op:"count",n:6},{t:138.0,op:"deficit"},{t:138.4,op:"lock"},
  {t:141.0,op:"gap"},{t:145.0,op:"clock",n:5},{t:150.0,op:"glass",f:880},{t:154.8,op:"silence"},
  {t:156.0,op:"expand",a:440,b:820,d:0.9},{t:156.3,op:"layer",i:0},{t:157.1,op:"layer",i:1},
  {t:157.9,op:"layer",i:2},{t:158.7,op:"layer",i:3},
  {t:159.0,op:"set"},{t:163.0,op:"cross"},{t:167.0,op:"bell",f:660},
  {t:170.0,op:"count",n:4},{t:174.0,op:"gap"},{t:177.0,op:"gap"},
  {t:178.6,op:"silence"}
];

export const FPS = 60;
export const DURATION_IN_FRAMES = TOTAL * FPS;
