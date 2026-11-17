# -*- coding: utf-8 -*-
"""零点涨落幂次对比: <1/M> vs <1/sqrt(M)> vs 静态<delta_v>。不做选优拟合。"""
import csv, re, json, math
from collections import defaultdict

rows = list(csv.DictReader(open('superconductors_deduplicated.csv', encoding='utf-8-sig')))
elems = json.load(open('element_fg_table.json', encoding='utf-8'))
MASS = {e['symbol']: e['mass'] for e in elems}
DV = {e['symbol']: e['mean_delta_v'] for e in elems}

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
    if n < 3:
        return None
    def rk(v):
        o = sorted(range(n), key=lambda i: v[i])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[o[j+1]] == v[o[i]]:
                j += 1
            for k in range(i, j+1):
                r[o[k]] = (i+j)/2 + 1
            i = j+1
        return r
    a, b = rk(x), rk(y)
    ma, mb = sum(a)/n, sum(b)/n
    den = math.sqrt(sum((v-ma)**2 for v in a) * sum((v-mb)**2 for v in b))
    return sum((a[i]-ma)*(b[i]-mb) for i in range(n))/den if den > 0 else None

D = []
for r in rows:
    c = parse(r['材料(化学式)'])
    t = tc(r['临界温度 Tc (K)'])
    if not c or t is None:
        continue
    tot = sum(c.values())
    im1 = sum((n/tot)/MASS[e] for e, n in c.items())
    imh = sum((n/tot)/math.sqrt(MASS[e]) for e, n in c.items())
    dv = sum((n/tot)*DV[e] for e, n in c.items())
    pred = '预测' in (str(r['条件']) + str(r['备注']))
    D.append({'t': t, 'im1': im1, 'imh': imh, 'dv': dv, 'pred': pred})

def report(sel, label):
    print('=== %s (n=%d) ===' % (label, len(sel)))
    for name, key in [('<1/M>   [Omega固定]', 'im1'),
                      ('<1/sqrt M> [k固定]', 'imh'),
                      ('<delta_v> [静态角亏]', 'dv')]:
        r_all = spearman([d['t'] for d in sel], [d[key] for d in sel])
        print('  rho(Tc,%-18s) = %+.3f' % (name, r_all))
    print()

report(D, '全样本')
report([d for d in D if not d['pred']], '实验样本')
report([d for d in D if d['t'] >= 50], 'Tc>=50K')
report([d for d in D if not d['pred'] and d['t'] >= 50], '实验且Tc>=50K')

print('=== 代理量间相关性 (是否独立) ===')
print('  rho(<1/M>, <delta_v>)   = %+.3f' % spearman([d['im1'] for d in D], [d['dv'] for d in D]))
print('  rho(<1/sqrtM>,<delta_v>)= %+.3f' % spearman([d['imh'] for d in D], [d['dv'] for d in D]))
print('  rho(<1/M>, <1/sqrtM>)   = %+.3f' % spearman([d['im1'] for d in D], [d['imh'] for d in D]))
