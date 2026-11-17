# -*- coding: utf-8 -*-
"""
曲率零点涨落理想模型的数据检验（CQM 第八轮）

物理命题（框架内，非拟合）：
  谐振子零点位移 x_zp = sqrt(hbar/(2 M Omega))
  => 角亏涨落幅度 Delta delta_0 ∝ x_zp ∝ 1/sqrt(M)
  => 材料级 <Delta delta_0^2> ∝ <1/M> = sum_i c_i / M_i  (c_i 原子分数)
  第五轮闭环: Tc = theta_D/(2 arccoth x), x = 3 beta^2 Delta delta_0^2/[16(1-beta delta_v) Delta gamma]
  => Tc 随 <1/M> 单调增 (其他量固定时)

本脚本只做: 解析化学式 -> <1/M> -> Spearman 相关 + 同族对照。不做多参数拟合。
"""
import csv, re, json, math
from collections import defaultdict

CSV = 'superconductors_deduplicated.csv'
EL = 'element_fg_table.json'
TCOL = '临界温度 Tc (K)'

elems = json.load(open(EL, encoding='utf-8'))
MASS = {e['symbol']: e['mass'] for e in elems}
DV = {e['symbol']: e['mean_delta_v'] for e in elems}

# 稳健化学式解析器: 元素+数字, 括号组, 点号水合物/复合, 忽略掺杂 x/y 的非化学计量部分
def parse_formula(f):
    s = str(f).strip()
    # 去掉常见后缀注释
    s = re.split(r'[\s(（]', s)[0]
    # 展开括号 (AB)3 形式
    for _ in range(3):
        m = re.search(r'\(([^()]+)\)(\d*\.?\d*)', s)
        if not m:
            break
        grp, num = m.group(1), m.group(2) or '1'
        try:
            nf = float(num)
        except ValueError:
            nf = 1.0
        expanded = ''
        for el, cnt in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', grp):
            expanded += el + (str(float(cnt) * nf) if cnt else str(nf))
        s = s[:m.start()] + expanded + s[m.end():]
    comp = defaultdict(float)
    for el, cnt in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', s):
        if el not in MASS:
            continue
        comp[el] += float(cnt) if cnt else 1.0
    return dict(comp)

def inv_mass(comp):
    """<1/M> = sum_i c_i / M_i, c_i = n_i / sum n_j (原子分数)"""
    tot = sum(comp.values())
    if tot <= 0:
        return None
    return sum((n / tot) / MASS[el] for el, n in comp.items())

def h_fraction(comp):
    tot = sum(comp.values())
    if tot <= 0:
        return None
    return comp.get('H', 0.0) / tot

def mean_dv(comp):
    tot = sum(comp.values())
    if tot <= 0:
        return None
    return sum((n / tot) * DV[el] for el, n in comp.items())

def get_tc(s):
    m = re.search(r'[\d.]+', str(s))
    return float(m.group()) if m else None

def spearman(x, y):
    n = len(x)
    if n < 3:
        return None
    def rank(v):
        order = sorted(range(n), key=lambda i: v[i])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(x), rank(y)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    den = math.sqrt(sum((rx[i] - mx) ** 2 for i in range(n)) * sum((ry[i] - my) ** 2 for i in range(n)))
    return num / den if den > 0 else None

rows = list(csv.DictReader(open(CSV, encoding='utf-8-sig')))
data = []
for r in rows:
    comp = parse_formula(r['材料(化学式)'])
    if not comp:
        continue
    tc = get_tc(r[TCOL])
    if tc is None:
        continue
    im = inv_mass(comp)
    if im is None:
        continue
    cond = str(r['条件'])
    note = str(r['备注'])
    data.append({
        'formula': r['材料(化学式)'], 'tc': tc, 'im': im,
        'xh': h_fraction(comp), 'dv': mean_dv(comp),
        'highP': '高压' in cond or 'GPa' in cond,
        'pred': '预测' in cond or '预测' in note,
        'cat': r['类别'], 'comp': comp, 'cond': cond,
    })

print('=== 样本 %d 种 ===' % len(data))

# 1) 全样本
print('\n[1] 全样本 Spearman:')
print('  rho(Tc, <1/M>) = %+.3f' % spearman([d['im'] for d in data], [d['tc'] for d in data]))
print('  rho(Tc, <dv>)  = %+.3f' % spearman([d['dv'] for d in data], [d['tc'] for d in data]))

# 2) 实验 vs 预测, 常压 vs 高压
for label, sel in [
    ('实验(non-pred)', [d for d in data if not d['pred']]),
    ('预测(pred)', [d for d in data if d['pred']]),
    ('常压', [d for d in data if not d['highP']]),
    ('高压', [d for d in data if d['highP']]),
]:
    if len(sel) >= 5:
        r_im = spearman([d['im'] for d in sel], [d['tc'] for d in sel])
        print('  %-16s n=%3d  rho(Tc,<1/M>)=%+.3f' % (label, len(sel), r_im))

# 3) 氢化物子样本
hyd = [d for d in data if d['xh'] and d['xh'] > 0.3 and d['tc'] >= 50]
print('\n[2] 富氢化物子样本 (x_H>0.3, Tc>=50K): n=%d' % len(hyd))
print('  rho(Tc, <1/M>) = %+.3f' % spearman([d['im'] for d in hyd], [d['tc'] for d in hyd]))
print('  rho(Tc, x_H)   = %+.3f' % spearman([d['xh'] for d in hyd], [d['tc'] for d in hyd]))
# 实验氢化物
he = [d for d in hyd if not d['pred']]
print('  实验氢化物 n=%d: rho(Tc,<1/M>)=%+.3f  rho(Tc,x_H)=%+.3f' % (
    len(he), spearman([d['im'] for d in he], [d['tc'] for d in he]),
    spearman([d['xh'] for d in he], [d['tc'] for d in he])))

# 4) 同族对照: 同一重元素, 不同 H 含量 (排除元素/压力混淆的定性证据)
print('\n[3] 同族对照 (同重元素, 不同 H 含量):')
by_el = defaultdict(list)
for d in hyd:
    metals = [el for el in d['comp'] if el != 'H']
    if len(metals) == 1:
        by_el[metals[0]].append(d)
for el, lst in sorted(by_el.items()):
    if len(lst) >= 2:
        lst.sort(key=lambda d: d['xh'])
        s = '  %-3s: ' % el + '  '.join('%s(xH=%.2f,Tc=%.0f,im=%.3f%s)' % (
            d['formula'].split('(')[0], d['xh'], d['tc'], d['im'], '*' if d['pred'] else '') for d in lst)
        print(s)

# 5) 关键检验: <1/M> 排序 vs Tc 排序 单调一致性(富氢实验)
print('\n[4] 富氢实验样本 <1/M> vs Tc 明细:')
for d in sorted(he, key=lambda d: -d['im']):
    print('  %-14s <1/M>=%.4f xH=%.2f Tc=%6.1f %s' % (
        d['formula'].split('(')[0], d['im'], d['xh'], d['tc'], d['cond'][:16]))
