# -*- coding: utf-8 -*-
"""稳健性: 剔除撤稿/预测/离群后 rho(Tc,<1/M>) 是否稳定。"""
import csv, re, json, math
from collections import defaultdict

rows = list(csv.DictReader(open('superconductors_deduplicated.csv', encoding='utf-8-sig')))
elems = json.load(open('element_fg_table.json', encoding='utf-8'))
MASS = {e['symbol']: e['mass'] for e in elems}

def parse(f):
    s = re.split(r'[\s(（]', str(f).strip())[0]
    c = defaultdict(float)
    for el, n in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', s):
        if el in MASS:
            c[el] += float(n) if n else 1.0
    return dict(c)

def tc(s):
    m = re.search(r'[\d.]+', str(s))
    return float(m.group()) if m else None

def spearman(x, y):
    n = len(x)
    if n < 3: return None
    def rk(v):
        o = sorted(range(n), key=lambda i: v[i]); r = [0.0]*n; i = 0
        while i < n:
            j = i
            while j+1 < n and v[o[j+1]] == v[o[i]]: j += 1
            for k in range(i, j+1): r[o[k]] = (i+j)/2+1
            i = j+1
        return r
    a, b = rk(x), rk(y); ma, mb = sum(a)/n, sum(b)/n
    den = math.sqrt(sum((v-ma)**2 for v in a)*sum((v-mb)**2 for v in b))
    return sum((a[i]-ma)*(b[i]-mb) for i in range(n))/den if den>0 else None

D = []
for r in rows:
    c = parse(r['材料(化学式)']); t = tc(r['临界温度 Tc (K)'])
    if not c or t is None: continue
    tot = sum(c.values())
    im1 = sum((n/tot)/MASS[e] for e, n in c.items())
    D.append({'f': r['材料(化学式)'], 't': t, 'im': im1,
              'pred': '预测' in (str(r['条件'])+str(r['备注'])),
              'retracted': r['材料(化学式)'].strip().upper() == 'CSH'})

def show(sel, label):
    print('  %-28s n=%3d  rho=%+.3f' % (label, len(sel), spearman([d['t'] for d in sel],[d['im'] for d in sel])))

print('=== rho(Tc,<1/M>) 稳健性 ===')
show(D, '全样本(含CSH)')
show([d for d in D if not d['retracted']], '剔除CSH(撤稿)')
show([d for d in D if not d['pred']], '剔除全部预测')
show([d for d in D if not d['retracted'] and not d['pred']], '剔除CSH+全部预测')
show([d for d in D if not d['retracted'] and not d['pred'] and d['t']>=50], '  +仅Tc>=50K(实验)')
show([d for d in D if d['t']<50], '仅Tc<50K(常规区)')

print()
print('=== CSH 单点影响 ===')
for d in D:
    if d['retracted']:
        print('  %s: Tc=%.1f <1/M>=%.4f (全样本最低质量倒数之一, 却是第2高Tc -> 强离群)' % (d['f'], d['t'], d['im']))
rank = sorted(D, key=lambda d: -d['im'])
print('  <1/M> 最高的材料:', ', '.join('%s(%.1fK)'%(x['f'],x['t']) for x in rank[:6]))
