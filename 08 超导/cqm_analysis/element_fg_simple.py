"""元素FG简化: 周期表位置 → 轨道类型 → A4基频
s-block → ω₁=13.8, p-block → ω₂=7.2, d-block → ω₃=5.3, f-block → ω₄=4.5
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework'); from atom_db import ATOM_DB, atom_db
import csv, re, math
import numpy as np

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
C2_geo = 2.0/3.0; LN2 = math.log(2)

ATOMIC_NUM = {el: i+1 for i, el in enumerate(ATOM_DB)}

HF_EL = {'Ce','Yb','U','Pr','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Lu','Nd','Np','Pu'}

omega_raw = np.array([1.0/np.sqrt(0.38196601), 1.0/np.sqrt(1.38196601), 1.0/np.sqrt(2.61803399), 1.0/np.sqrt(3.61803399)])
omega = omega_raw * 8.520890

# ============================================================
# 周期表位置 → 轨道类型 → A4基频
# ============================================================
def get_block(Z):
    """根据原子序数确定s/p/d/f块"""
    if Z <= 2: return 's'  # H, He
    if 3 <= Z <= 4: return 's'  # Li, Be
    if 5 <= Z <= 10: return 'p'  # B-Ne
    if 11 <= Z <= 12: return 's'  # Na, Mg
    if 13 <= Z <= 18: return 'p'  # Al-Ar
    if 19 <= Z <= 20: return 's'  # K, Ca
    if 21 <= Z <= 30: return 'd'  # Sc-Zn
    if 31 <= Z <= 36: return 'p'  # Ga-Kr
    if 37 <= Z <= 38: return 's'  # Rb, Sr
    if 39 <= Z <= 48: return 'd'  # Y-Cd
    if 49 <= Z <= 54: return 'p'  # In-Xe
    if 55 <= Z <= 56: return 's'  # Cs, Ba
    if 57 <= Z <= 71: return 'f'  # La-Lu (镧系)
    if 72 <= Z <= 80: return 'd'  # Hf-Hg
    if 81 <= Z <= 86: return 'p'  # Tl-Rn
    if Z >= 87: return 'f'  # Ac+
    return 's'

block_to_omega = {'s': omega[0], 'p': omega[1], 'd': omega[2], 'f': omega[3]}

# 构造元素FG表
el_gamma = {}
for el in ATOMIC_NUM:
    Z = ATOMIC_NUM[el]
    block = get_block(Z)
    el_gamma[el] = block_to_omega[block]

print("="*80)
print("元素FG: 周期表位置 → A4基频")
print("="*80)
print(f"ω₁={omega[0]:.1f}(s), ω₂={omega[1]:.1f}(p), ω₃={omega[2]:.1f}(d), ω₄={omega[3]:.1f}(f)")

print(f"\n元素Γ_el分布:")
for block, g in [('s',omega[0]),('p',omega[1]),('d',omega[2]),('f',omega[3])]:
    els_in_block = [el for el in ATOMIC_NUM if get_block(ATOMIC_NUM[el]) == block]
    print(f"  {block}区 ({len(els_in_block)}种): Γ={g:.1f}  例: {', '.join(els_in_block[:8])}")

# ============================================================
# 材料Γ预测: 1/mass加权平均
# ============================================================
def atom_db(el): return ATOM_DB.get(el, (100.0, 200, 1.5, 11))
def pf(f):
    pairs = re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f)
    a = {}
    for el, cnt in pairs:
        if el in ATOM_DB: a[el] = a.get(el,0)+(float(cnt) if cnt else 1.0)
    return a
def cp(formula):
    a = pf(formula)
    if not a: return None
    tm = sum(a[el]*atom_db(el)[0] for el in a)
    na = sum(a.values())
    ar = sum(a[el]*atom_db(el)[2] for el in a)/na
    l = 2*ar*1e-10
    td = sum(a[el]*atom_db(el)[1] for el in a)/na
    if td == 0: return None
    V = l**3
    ff = 1.0-0.3*(1.0-1.0/na)
    es = 0
    els = list(a.keys())
    for i in range(len(els)):
        for j in range(i+1,len(els)):
            es += 1.0/(a[els[i]]*atom_db(els[i])[0]*AMU) + 1.0/(a[els[j]]*atom_db(els[j])[0]*AMU)
    if not es:
        mi = tm*AMU/na
        es = (na*(na-1)/2)*2.0/mi
    G = (1.0/l)*math.sqrt((1.0-ff)*es)
    od = td*KB/HBAR
    dd = math.sqrt(abs((C2_geo/l**2)*(3*HBAR/(4*od))*(1-ff)*es))
    B = tm*td**2*KB/V*1e-3
    hf = any(el in HF_EL for el in a)
    return {'M':tm,'N':na,'l':l,'tD':td,'V':V,'G':G,'dd0':dd,'B':B,'hf':hf,'atoms':a}

data = []
with open("superconductors_deduplicated.csv",'r',encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc <= 0: continue
        mp = cp(row['材料(化学式)'])
        if mp is None or mp['dd0'] == 0: continue
        data.append({**mp,'formula':row['材料(化学式)'],'cat':row['类别'],'tc':tc})

non_hf = [d for d in data if not d['hf']]

# 全局系数
COEF = np.array([0.2616, -1.4924, -0.8620, 0.6354, 0.0813, -0.7463, 14.0305])
for it in range(20):
    for d in non_hf:
        ln_ke = math.log(d['tc']**2 * 9 * LN2 / (8 * d['dd0']**2 * d['tD']))
        geom = (COEF[1]*math.log(d['G']) + COEF[2]*math.log(d['tD']) +
                COEF[3]*math.log(d['B']) + COEF[4]*math.log(d['N']) + COEF[5]*math.log(d['V']) + COEF[6])
        d['Gamma'] = (ln_ke - geom) / COEF[0]
    X = np.column_stack([[d['Gamma'] for d in non_hf],
                         [math.log(d['G']) for d in non_hf],[math.log(d['tD']) for d in non_hf],
                         [math.log(d['B']) for d in non_hf],[math.log(d['N']) for d in non_hf],
                         [math.log(d['V']) for d in non_hf], np.ones(len(non_hf))])
    y = np.array([math.log(d['tc']**2 * 9 * LN2 / (8 * d['dd0']**2 * d['tD'])) for d in non_hf])
    cnew, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    if np.max(np.abs(cnew - COEF)) < 1e-8: break
    COEF = cnew

PAIR_ELS = {'铜氧化物高温超导体': {'Cu','O'},'铁基超导体': {'Fe','As','Se'},
            '氢化物高压超导体': {'H'},'A15结构金属间化合物': {'Nb','V','Mo'},
            '有机超导体': {'C','S','N'},'富勒烯超导体': {'C'}}

def material_gamma(d, use_pair=True):
    """元素FG → 材料Γ: 1/mass加权"""
    atoms = d['atoms']
    if use_pair and d['cat'] in PAIR_ELS:
        active = {el: cnt for el, cnt in atoms.items() if el in PAIR_ELS[d['cat']]}
        if not active: active = atoms
    else:
        active = atoms

    g_pred = 0; total_w = 0
    for el, cnt in active.items():
        if el in el_gamma:
            w = cnt / atom_db(el)[0]
            g_pred += w * el_gamma[el]
            total_w += w
    return g_pred / total_w if total_w > 0 else 30.0

# 配对元素预测
errs_pair = []
for d in non_hf:
    g_pred = material_gamma(d, use_pair=True)
    ln_ke = (COEF[0]*g_pred + COEF[1]*math.log(d['G']) + COEF[2]*math.log(d['tD']) +
             COEF[3]*math.log(d['B']) + COEF[4]*math.log(d['N']) + COEF[5]*math.log(d['V']) + COEF[6])
    tp = math.sqrt(8*d['dd0']**2*math.exp(ln_ke)*d['tD']/(9*LN2))
    errs_pair.append(abs(tp - d['tc'])/d['tc'])

errs_pair = np.array(errs_pair)

# 全部元素预测
errs_all = []
for d in non_hf:
    g_pred = material_gamma(d, use_pair=False)
    ln_ke = (COEF[0]*g_pred + COEF[1]*math.log(d['G']) + COEF[2]*math.log(d['tD']) +
             COEF[3]*math.log(d['B']) + COEF[4]*math.log(d['N']) + COEF[5]*math.log(d['V']) + COEF[6])
    tp = math.sqrt(8*d['dd0']**2*math.exp(ln_ke)*d['tD']/(9*LN2))
    errs_all.append(abs(tp - d['tc'])/d['tc'])

errs_all = np.array(errs_all)

print(f"\n{'='*80}")
print("元素FG → Γ → Tc 预测精度")
print(f"{'='*80}")
print(f"\n  配对元素预测({len(errs_pair)}): 中位={np.median(errs_pair)*100:.1f}%, {np.mean(errs_pair<=1)*100:.0f}%在2倍内, {np.mean(errs_pair<=4)*100:.0f}%在5倍内")
print(f"  全部元素预测({len(errs_all)}): 中位={np.median(errs_all)*100:.1f}%, {np.mean(errs_all<=1)*100:.0f}%在2倍内, {np.mean(errs_all<=4)*100:.0f}%在5倍内")

# 按类别
cats = {}
for d in non_hf:
    cats.setdefault(d['cat'], []).append(d)

print(f"\n--- 配对元素按类别 ---")
print(f"{'类别':<22} {'n':>4} {'Γ_pred均值':>9} {'中位%':>7} {'2倍内%':>7}")
for cat in sorted(cats.keys()):
    ds = cats[cat]
    g_vals = [material_gamma(d) for d in ds]
    errs = []
    for d in ds:
        g_pred = material_gamma(d)
        ln_ke = (COEF[0]*g_pred + COEF[1]*math.log(d['G']) + COEF[2]*math.log(d['tD']) +
                 COEF[3]*math.log(d['B']) + COEF[4]*math.log(d['N']) + COEF[5]*math.log(d['V']) + COEF[6])
        tp = math.sqrt(8*d['dd0']**2*math.exp(ln_ke)*d['tD']/(9*LN2))
        errs.append(abs(tp - d['tc'])/d['tc'])
    errs = np.array(errs)
    print(f"  {cat:<20} {len(ds):>4} {np.mean(g_vals):>9.2f} {np.median(errs)*100:>6.0f}% {np.mean(errs<=1)*100:>6.0f}%")

print(f"\n对比:")
print(f"  GBR(纯几何): 中位 47%, 79%在2倍内")
print(f"  one-hot类别: 中位 45%, 81%在2倍内")