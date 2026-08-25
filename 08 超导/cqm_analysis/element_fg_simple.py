"""元素FG简化: 周期表位置 → 轨道类型 → A4基频
s-block → ω₁=13.8, p-block → ω₂=7.2, d-block → ω₃=5.3, f-block → ω₄=4.5
"""
import csv, re, math
import numpy as np

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
C2_geo = 2.0/3.0; LN2 = math.log(2)

ATOMIC_NUM = {'H':1,'He':2,'Li':3,'Be':4,'B':5,'C':6,'N':7,'O':8,'F':9,'Ne':10,'Na':11,'Mg':12,'Al':13,'Si':14,'P':15,'S':16,'Cl':17,'K':19,'Ca':20,'Sc':21,'Ti':22,'V':23,'Cr':24,'Mn':25,'Fe':26,'Co':27,'Ni':28,'Cu':29,'Zn':30,'Ga':31,'Ge':32,'As':33,'Se':34,'Br':35,'Rb':37,'Sr':38,'Y':39,'Zr':40,'Nb':41,'Mo':42,'Tc':43,'Ru':44,'Rh':45,'Pd':46,'Ag':47,'Cd':48,'In':49,'Sn':50,'Sb':51,'Te':52,'I':53,'Cs':55,'Ba':56,'La':57,'Ce':58,'Pr':59,'Nd':60,'Sm':62,'Eu':63,'Gd':64,'Tb':65,'Dy':66,'Ho':67,'Er':68,'Tm':69,'Yb':70,'Lu':71,'Hf':72,'Ta':73,'W':74,'Re':75,'Os':76,'Ir':77,'Pt':78,'Au':79,'Hg':80,'Tl':81,'Pb':82,'Bi':83,'Th':90}

ATOM_DB = {'H':(1.008,0,0.46,11),'He':(4.003,0,0.31,11),'Li':(6.94,344,1.52,11),'Be':(9.01,1440,1.12,130),'B':(10.81,1480,0.87,185),'C':(12.01,2230,0.77,338),'N':(14.01,0,0.75,11),'O':(16.00,0,0.73,11),'F':(19.00,0,0.72,11),'Ne':(20.18,0,0.71,11),'Na':(22.99,158,1.86,7),'Mg':(24.31,400,1.60,35),'Al':(26.98,428,1.43,76),'Si':(28.09,645,1.18,100),'P':(30.97,0,1.10,11),'S':(32.06,0,1.05,11),'Cl':(35.45,0,1.02,11),'K':(39.10,91,2.27,3),'Ca':(40.08,230,1.97,15),'Sc':(44.96,360,1.62,44),'Ti':(47.87,420,1.47,110),'V':(50.94,383,1.34,162),'Cr':(52.00,435,1.28,160),'Mn':(54.94,410,1.27,120),'Fe':(55.85,470,1.26,170),'Co':(58.93,445,1.25,180),'Ni':(58.69,450,1.24,180),'Cu':(63.55,343,1.28,140),'Zn':(65.38,327,1.34,70),'Ga':(69.72,240,1.35,40),'Ge':(72.63,374,1.22,75),'As':(74.92,0,1.21,11),'Se':(78.97,0,1.20,11),'Br':(79.90,0,1.20,11),'Rb':(85.47,56,2.48,2),'Sr':(87.62,147,2.15,12),'Y':(88.91,280,1.80,37),'Zr':(91.22,291,1.60,95),'Nb':(92.91,275,1.46,170),'Mo':(95.96,425,1.39,230),'Tc':(98.00,0,1.36,11),'Ru':(101.07,0,1.34,220),'Rh':(102.91,0,1.34,150),'Pd':(106.42,274,1.37,180),'Ag':(107.87,215,1.44,100),'Cd':(112.41,209,1.49,42),'In':(114.82,108,1.62,11),'Sn':(118.71,200,1.58,50),'Sb':(121.76,0,1.61,11),'Te':(127.60,0,1.60,11),'I':(126.90,0,1.63,11),'Cs':(132.91,38,2.65,2),'Ba':(137.33,110,2.22,9),'La':(138.91,142,1.87,24),'Ce':(140.12,0,1.82,22),'Pr':(140.91,0,1.82,21),'Nd':(144.24,0,1.82,20),'Sm':(150.36,0,1.81,18),'Eu':(151.96,0,1.81,8),'Gd':(157.25,0,1.80,25),'Tb':(158.93,0,1.79,25),'Dy':(162.50,0,1.79,25),'Ho':(164.93,0,1.78,26),'Er':(167.26,0,1.78,26),'Tm':(168.93,0,1.77,28),'Yb':(173.05,0,1.77,10),'Lu':(174.97,0,1.77,30),'Hf':(178.49,252,1.59,110),'Ta':(180.95,240,1.46,200),'W':(183.84,400,1.39,310),'Re':(186.21,430,1.37,370),'Os':(190.23,500,1.35,400),'Ir':(192.22,420,1.36,355),'Pt':(195.08,240,1.39,230),'Au':(196.97,170,1.44,180),'Hg':(200.59,0,1.51,25),'Tl':(204.38,78,1.70,8),'Pb':(207.20,105,1.75,23),'Bi':(208.98,0,1.70,11),'Th':(232.04,163,1.80,54)}
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
COEF = np.array([0.2358, -1.5477, -1.3720, 0.7953, -0.1227, -0.9642, 2.5884])
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