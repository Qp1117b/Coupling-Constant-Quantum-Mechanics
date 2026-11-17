# -*- coding: utf-8 -*-
"""
CQM 元素层量纲封闭定理的数值审查（第九轮）

命题 Z2（待证）：
  element_fg_table 的全部 18 字段中，唯一带物理量纲的是 mass（amu），
  且它是外部实验输入，不是 CQM 推导。其余字段（deform、角亏、Cartan 矩阵、
  positions、壳层计数、价态）都是无量纲的组合量/角量/计数。
  => CQM 几何层原则上不能给出 J0/theta_D 的绝对能标。
  => 这是命题 Z（zeta 无量纲不能给温度）的第二个实例。

本脚本只做：
  (1) 逐字段量纲分类审查（结构性，非统计）
  (2) 跨族同计量氢化物 Tc 差异能否由无量纲几何量（deform/角亏/价态/Cartan）解释
  (3) 全样本 Spearman（新几何量 vs Tc）
  不做多参数拟合。
"""
import csv, re, json, math
from collections import defaultdict

CSV = 'superconductors_deduplicated.csv'
EL = 'element_fg_table.json'
TCOL = '临界温度 Tc (K)'

elems = json.load(open(EL, encoding='utf-8'))
BY = {e['symbol']: e for e in elems}
MASS = {s: e['mass'] for s, e in BY.items()}

# ---------- (0) 量纲审查：字段 -> (是否无量纲, 依据) ----------
DIM = {
    'Z':            ('无量纲', '质子计数'),
    'symbol':       ('无量纲', '标签'),
    'protons':      ('无量纲', '计数'),
    'neutrons':     ('无量纲', '计数'),
    'mass':         ('有量纲 amu', '外部实验输入，非 CQM 推导'),
    'p_shells':     ('无量纲', '电子占据计数'),
    'n_shells':     ('无量纲', '核子占据计数'),
    'cartan_type':  ('无量纲', '离散标签 A1/A3/A4'),
    'deform':       ('无量纲', '由归一化 positions 算出的形变量'),
    'p_valence':    ('无量纲', '价电子/空位计数'),
    'n_valence':    ('无量纲', '价核子计数'),
    'cartan_matrix':('无量纲', '整数矩阵（Cartan 标准形）'),
    'positions':    ('无量纲', '归一化到单位圆的坐标'),
    'edges':        ('无量纲', '拓扑图边表'),
    'faces':        ('无量纲', '拓扑图面表'),
    'angle_deficits':('无量纲(弧度)', '角度量，弧度是无量纲'),
    'physical_delta_v':('无量纲(弧度)', '角亏'),
    'mean_delta_v': ('无量纲(弧度)', '角亏平均'),
    'max_delta_v':  ('无量纲(弧度)', '角亏最大'),
}

# ---------- 化学式解析（复用） ----------
def parse_formula(f):
    s = str(f).strip()
    s = re.split(r'[\s(（]', s)[0]
    for _ in range(3):
        m = re.search(r'\(([^()]+)\)(\d*\.?\d*)', s)
        if not m: break
        grp, num = m.group(1), m.group(2) or '1'
        try: nf = float(num)
        except ValueError: nf = 1.0
        exp = ''
        for el, cnt in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', grp):
            exp += el + (str(float(cnt) * nf) if cnt else str(nf))
        s = s[:m.start()] + exp + s[m.end():]
    comp = defaultdict(float)
    for el, cnt in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', s):
        if el in MASS:
            comp[el] += float(cnt) if cnt else 1.0
    return dict(comp)

def get_tc(s):
    m = re.search(r'[\d.]+', str(s))
    return float(m.group()) if m else None

def spearman(x, y):
    n = len(x)
    if n < 3: return None
    def rank(v):
        o = sorted(range(n), key=lambda i: v[i]); r = [0.0]*n; i = 0
        while i < n:
            j = i
            while j+1 < n and v[o[j+1]] == v[o[i]]: j += 1
            for k in range(i, j+1): r[o[k]] = (i+j)/2+1
            i = j+1
        return r
    rx, ry = rank(x), rank(y)
    mx, my = sum(rx)/n, sum(ry)/n
    num = sum((rx[i]-mx)*(ry[i]-my) for i in range(n))
    den = math.sqrt(sum((rx[i]-mx)**2 for i in range(n))*sum((ry[i]-my)**2 for i in range(n)))
    return num/den if den > 0 else None

# ---------- 材料级无量纲几何量聚合（原子分数加权） ----------
def agg(comp, field):
    tot = sum(comp.values())
    if tot <= 0: return None
    if field == 'deform':
        return sum((n/tot)*BY[el]['deform'] for el, n in comp.items())
    if field == 'dv':
        return sum((n/tot)*BY[el]['mean_delta_v'] for el, n in comp.items())
    if field == 'valence':
        # 取 p_valence 首项（最外层价电子数）加权
        return sum((n/tot)*BY[el]['p_valence'][0] for el, n in comp.items())
    if field == 'A4frac':
        # A4 型元素的原子分数
        return sum((n/tot)*(1 if BY[el]['cartan_type']=='A4' else 0) for el, n in comp.items())
    if field == 'im':
        return sum((n/tot)/MASS[el] for el, n in comp.items())
    return None

rows = list(csv.DictReader(open(CSV, encoding='utf-8-sig')))
data = []
for r in rows:
    comp = parse_formula(r['材料(化学式)'])
    if not comp: continue
    tc = get_tc(r[TCOL])
    if tc is None: continue
    d = {'f': r['材料(化学式)'], 'tc': tc, 'comp': comp,
         'pred': '预测' in str(r['条件'])+str(r['备注']),
         'highP': '高压' in str(r['条件']) or 'GPa' in str(r['条件'])}
    for k in ['deform','dv','valence','A4frac','im']:
        d[k] = agg(comp, k)
    data.append(d)

print('='*72)
print('[1] 量纲审查（结构性）')
print('='*72)
nd = sum(1 for v in DIM.values() if v[0].startswith('无量纲'))
print('  %d 字段中：无量纲 %d，有量纲 %d' % (len(DIM), nd, len(DIM)-nd))
for k,(dn,why) in DIM.items():
    if not dn.startswith('无量纲'):
        print('  ** 有量纲字段: %-18s %s' % (k, why))
print('  结论：唯一能标候选 mass 是外部实验输入，不是几何推导量。')

print()
print('='*72)
print('[2] 全样本 Spearman（新无量纲几何量 vs Tc）')
print('='*72)
exp = [d for d in data if not d['pred']]
for k,label in [('deform','<deform>'),('dv','<delta_v>'),('valence','<价电子>'),('A4frac','A4原子分数'),('im','<1/M>')]:
    print('  rho(Tc,%-12s) = %+.3f (全)  %+.3f (实验)' % (
        label, spearman([d[k] for d in data],[d['tc'] for d in data]),
        spearman([d[k] for d in exp],[d['tc'] for d in exp])))

# ---------- (3) 跨族同计量氢化物：第八轮失败处的正面检验 ----------
print()
print('='*72)
print('[3] 跨族同计量氢化物（LaH10/CeH10/ThH10 等）几何量 vs Tc')
print('='*72)
# 提取 XHn 型（单一金属 + H，固定 n）
xh_series = defaultdict(list)
for d in data:
    metals = [el for el in d['comp'] if el != 'H']
    if len(metals)==1 and 'H' in d['comp']:
        m = metals[0]
        nH = d['comp']['H']/d['comp'][m]
        ratio = round(nH, 1)
        xh_series[ratio].append((m, d))

for ratio in sorted(xh_series):
    lst = xh_series[ratio]
    if len(lst) < 3: continue
    # 只取实验、Tc>=50
    sel = [(m,d) for m,d in lst if not d['pred'] and d['tc']>=50]
    if len(sel) < 3: continue
    print('\n  --- XH%s 系列 n=%d ---' % (ratio, len(sel)))
    print('  %-4s %-14s %7s %9s %9s %9s %8s' % ('金属','化学式','Tc(K)','<1/M>','<deform>','<dv>','Cartan'))
    for m,d in sorted(sel, key=lambda x:-x[1]['tc']):
        print('  %-4s %-14s %7.1f %9.4f %9.4f %9.4f %8s' % (
            m, d['f'].split('(')[0][:14], d['tc'], d['im'], d['deform'], d['dv'], BY[m]['cartan_type']))
    # 各几何量与 Tc 的排序相关（跨族）
    xs = {k:[d[k] for m,d in sel] for k in ['im','deform','dv','valence']}
    ys = [d['tc'] for m,d in sel]
    print('  跨族 rho(Tc,·): ' + '  '.join('%s=%+.2f'%(k,spearman(xs[k],ys)) for k in xs))

# ---------- (4) 标度自由判据：去掉质量标度后几何量是否还有独立信号 ----------
print()
print('='*72)
print('[4] 标度自由检验：tau = Tc*sqrt(Mbar)（去掉 theta_D~M^-1/2 质量标度）')
print('='*72)
def mean_mass(comp):
    tot = sum(comp.values())
    return sum((n/tot)*MASS[el] for el,n in comp.items()) if tot > 0 else None
for d in data:
    mm = mean_mass(d['comp'])
    d['tau'] = d['tc']*math.sqrt(mm) if mm else None
exp2 = [d for d in data if not d['pred']]
print('  rho(tau, <1/M>)  = %+.3f (全)  %+.3f (实验)  <- 应接近0(质量标度已剥离)' % (
    spearman([d['tau'] for d in data],[d['im'] for d in data]),
    spearman([d['tau'] for d in exp2],[d['im'] for d in exp2])))
for k,label in [('deform','<deform>'),('dv','<delta_v>'),('valence','<价电子>'),('A4frac','A4原子分数')]:
    print('  rho(tau,%-12s) = %+.3f (全)  %+.3f (实验)  <- 几何量独立信号?' % (
        label, spearman([d[k] for d in data],[d['tau'] for d in data]),
        spearman([d[k] for d in exp2],[d['tau'] for d in exp2])))
