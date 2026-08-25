"""元素FG从壳层构型第一性推导
CQM已推导周期表(§11.7): 每个壳层的E=n+l, 对应ζ零点γ_n
A4四基频 ω_j 对应4种轨道类型 s/p/d/f
Γ_el = (n_s)*ω₁ + (n_p)*ω₂ + (n_d)*ω₃ + (n_f)*ω₄
"""
import csv, re, math
import numpy as np
from itertools import product

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
C2_geo = 2.0/3.0; LN2 = math.log(2)

ATOM_DB = {'H':(1.008,0,0.46,0),'He':(4.003,0,0.31,0),'Li':(6.94,344,1.52,11),'Be':(9.01,1440,1.12,130),'B':(10.81,1480,0.87,185),'C':(12.01,2230,0.77,338),'N':(14.01,0,0.75,0),'O':(16.00,0,0.73,0),'F':(19.00,0,0.72,0),'Ne':(20.18,0,0.71,0),'Na':(22.99,158,1.86,7),'Mg':(24.31,400,1.60,35),'Al':(26.98,428,1.43,76),'Si':(28.09,645,1.18,100),'P':(30.97,0,1.10,0),'S':(32.06,0,1.05,0),'Cl':(35.45,0,1.02,0),'K':(39.10,91,2.27,3),'Ca':(40.08,230,1.97,15),'Sc':(44.96,360,1.62,44),'Ti':(47.87,420,1.47,110),'V':(50.94,383,1.34,162),'Cr':(52.00,435,1.28,160),'Mn':(54.94,410,1.27,120),'Fe':(55.85,470,1.26,170),'Co':(58.93,445,1.25,180),'Ni':(58.69,450,1.24,180),'Cu':(63.55,343,1.28,140),'Zn':(65.38,327,1.34,70),'Ga':(69.72,240,1.35,40),'Ge':(72.63,374,1.22,75),'As':(74.92,0,1.21,0),'Se':(78.97,0,1.20,0),'Br':(79.90,0,1.20,0),'Rb':(85.47,56,2.48,2),'Sr':(87.62,147,2.15,12),'Y':(88.91,280,1.80,37),'Zr':(91.22,291,1.60,95),'Nb':(92.91,275,1.46,170),'Mo':(95.96,425,1.39,230),'Tc':(98.00,0,1.36,0),'Ru':(101.07,0,1.34,220),'Rh':(102.91,0,1.34,150),'Pd':(106.42,274,1.37,180),'Ag':(107.87,215,1.44,100),'Cd':(112.41,209,1.49,42),'In':(114.82,108,1.62,11),'Sn':(118.71,200,1.58,50),'Sb':(121.76,0,1.61,0),'Te':(127.60,0,1.60,0),'I':(126.90,0,1.63,0),'Cs':(132.91,38,2.65,2),'Ba':(137.33,110,2.22,9),'La':(138.91,142,1.87,24),'Ce':(140.12,0,1.82,22),'Pr':(140.91,0,1.82,21),'Nd':(144.24,0,1.82,20),'Sm':(150.36,0,1.81,18),'Eu':(151.96,0,1.81,8),'Gd':(157.25,0,1.80,25),'Tb':(158.93,0,1.79,25),'Dy':(162.50,0,1.79,25),'Ho':(164.93,0,1.78,26),'Er':(167.26,0,1.78,26),'Tm':(168.93,0,1.77,28),'Yb':(173.05,0,1.77,10),'Lu':(174.97,0,1.77,30),'Hf':(178.49,252,1.59,110),'Ta':(180.95,240,1.46,200),'W':(183.84,400,1.39,310),'Re':(186.21,430,1.37,370),'Os':(190.23,500,1.35,400),'Ir':(192.22,420,1.36,355),'Pt':(195.08,240,1.39,230),'Au':(196.97,170,1.44,180),'Hg':(200.59,0,1.51,25),'Tl':(204.38,78,1.70,8),'Pb':(207.20,105,1.75,23),'Bi':(208.98,0,1.70,0),'Th':(232.04,163,1.80,54)}
HF_EL = {'Ce','Yb','U','Pr','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Lu','Nd','Np','Pu'}

def atom_db(el): return ATOM_DB.get(el, (100.0, 200, 1.5, 0))

# A4 基频
omega_raw = np.array([1.0/np.sqrt(0.38196601), 1.0/np.sqrt(1.38196601), 1.0/np.sqrt(2.61803399), 1.0/np.sqrt(3.61803399)])
omega = omega_raw * 8.520890

# ============================================================
# 电子构型解析: 从Z确定每个壳层的电子数
# ============================================================
def electron_config(Z):
    """Madelung规则填充: 按n+l顺序, 同n+l时按n小优先
    返回 {orbital_type: electron_count}
    """
    filling_order = [
        (1,'s',2),(2,'s',2),(2,'p',6),(3,'s',2),(3,'p',6),
        (4,'s',2),(3,'d',10),(4,'p',6),(5,'s',2),(4,'d',10),
        (5,'p',6),(6,'s',2),(4,'f',14),(5,'d',10),(6,'p',6),
        (7,'s',2),(5,'f',14),(6,'d',10),(7,'p',6)
    ]

    counts = {'s':0,'p':0,'d':0,'f':0}
    remaining = int(Z)
    for n, orb, cap in filling_order:
        filled = min(remaining, cap)
        counts[orb] += filled
        remaining -= filled
        if remaining <= 0: break
    return counts

# ============================================================
# 壳层→Γ 映射的核心假设:
# s轨道贡献 → ω₁ (最低频率)
# p轨道贡献 → ω₂
# d轨道贡献 → ω₃
# f轨道贡献 → ω₄
#
# 但Γ = n₁ω₁ + n₂ω₂ + n₃ω₃ + n₄ω₄ 只依赖于价电子
# 满壳层电子被"屏蔽"——只有价电子参与超导配对
# ============================================================

def valence_counts(Z):
    """只计数未满壳层的电子"""
    filling_order = [
        (1,'s',2),(2,'s',2),(2,'p',6),(3,'s',2),(3,'p',6),
        (4,'s',2),(3,'d',10),(4,'p',6),(5,'s',2),(4,'d',10),
        (5,'p',6),(6,'s',2),(4,'f',14),(5,'d',10),(6,'p',6),
        (7,'s',2),(5,'f',14),(6,'d',10),(7,'p',6)
    ]

    counts = {'s':0,'p':0,'d':0,'f':0}
    remaining = int(Z)

    # 跟踪当前部分填充的壳层
    for n, orb, cap in filling_order:
        filled = min(remaining, cap)
        if filled > 0 and filled < cap:
            # 部分填充 → 这是价壳层
            counts[orb] += filled
        elif filled == cap and remaining == filled:
            # 最后一个满壳层也算入价层
            counts[orb] += filled
        remaining -= filled
        if remaining <= 0: break
    return counts

def el_gamma_shell(el_name, Z):
    """从壳层构型计算元素的Γ_el（第一性）"""
    vc = valence_counts(Z)
    # 价电子加权平均Γ
    total_v = sum(vc.values())
    if total_v == 0:
        return 14.0  # 惰性气体近似

    # 每个价电子的轨道类型贡献
    gamma = 0.0
    orbital_to_omega = {'s': omega[0], 'p': omega[1], 'd': omega[2], 'f': omega[3]}
    for orb, count in vc.items():
        if count > 0:
            gamma += count * orbital_to_omega[orb]
    gamma /= total_v

    # 再加原子序数的对数修正(Z大→壳层多→有效配对数增加)
    if Z > 2:
        gamma += 0.5 * math.log(Z/10)

    return gamma

# ============================================================
# 计算所有元素的Γ_el并展示
# ============================================================
print("="*80)
print("元素FG: 从壳层构型第一性推导 Γ_el")
print("="*80)
print(f"\nA4基频 ω = {omega}")
print(f"\nω₁≈{omega[0]:.1f}(s轨道), ω₂≈{omega[1]:.1f}(p轨道), ω₃≈{omega[2]:.1f}(d轨道), ω₄≈{omega[3]:.1f}(f轨道)")

el_gamma_table = {}
print(f"\n{'元素':<6} {'Z':>5} {'价s':>4} {'价p':>4} {'价d':>4} {'价f':>4} {'Γ_el':>8} {'全s':>4} {'全p':>4} {'全d':>4} {'全f':>4}")
print("-"*75)

for el, (mass, td, ar, Z) in sorted(ATOM_DB.items(), key=lambda x: x[1][3]):
    if Z == 0: continue
    vc = valence_counts(Z)
    fc = electron_config(Z)
    gamma = el_gamma_shell(el, Z)
    el_gamma_table[el] = gamma
    if Z <= 56 or el in {'La','Ce','Yb','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Pb','Bi','Th','U'}:
        print(f"  {el:<4} {Z:>5} {vc['s']:>4} {vc['p']:>4} {vc['d']:>4} {vc['f']:>4} {gamma:>8.2f} {fc['s']:>4} {fc['p']:>4} {fc['d']:>4} {fc['f']:>4}")

# ============================================================
# 用元素FG预测材料Γ和Tc
# ============================================================
print(f"\n{'='*80}")
print("元素FG → 化合物Γ → Tc 完整第一性预测")
print(f"{'='*80}")

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

# 联合优化1次取全局系数（用ground truth Γ）
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

# 用元素FG预测Γ
def material_gamma(atoms, pairing_el=None):
    """从元素FG计算材料Γ: 配对元素主导, 1/mass加权"""
    if pairing_el:
        active = {el: cnt for el, cnt in atoms.items() if el in pairing_el}
        if not active:
            active = atoms
    else:
        active = atoms

    g_pred = 0
    total_w = 0
    for el, cnt in active.items():
        if el in el_gamma_table:
            w = cnt / atom_db(el)[0]  # 1/mass 加权
            g_pred += w * el_gamma_table[el]
            total_w += w

    if total_w == 0:
        return None
    return g_pred / total_w

# 配对元素定义
PAIR_ELS = {
    '铜氧化物高温超导体': {'Cu','O'},
    '铁基超导体': {'Fe','As','Se'},
    '氢化物高压超导体': {'H'},
    'A15结构金属间化合物': {'Nb','V','Mo'},
    '有机超导体': {'C','S','N'},
    '富勒烯超导体': {'C'},
}

errs_el = []
for d in non_hf:
    pair_els = PAIR_ELS.get(d['cat'], None)
    g_pred = material_gamma(d['atoms'], pair_els)
    if g_pred is None: continue

    ln_ke = (COEF[0]*g_pred + COEF[1]*math.log(d['G']) + COEF[2]*math.log(d['tD']) +
             COEF[3]*math.log(d['B']) + COEF[4]*math.log(d['N']) + COEF[5]*math.log(d['V']) + COEF[6])
    tp = math.sqrt(8*d['dd0']**2*math.exp(ln_ke)*d['tD']/(9*LN2))
    errs_el.append(abs(tp - d['tc'])/d['tc'])

errs_el = np.array(errs_el)
print(f"\n元素FG→Γ→Tc ({len(errs_el)}材料): 中位={np.median(errs_el)*100:.1f}%, {np.mean(errs_el<=1)*100:.0f}%在2倍内, {np.mean(errs_el<=4)*100:.0f}%在5倍内")

# 纯元素FG（不指定配对元素）
errs_el_all = []
for d in non_hf:
    g_pred = material_gamma(d['atoms'])
    if g_pred is None: continue
    ln_ke = (COEF[0]*g_pred + COEF[1]*math.log(d['G']) + COEF[2]*math.log(d['tD']) +
             COEF[3]*math.log(d['B']) + COEF[4]*math.log(d['N']) + COEF[5]*math.log(d['V']) + COEF[6])
    tp = math.sqrt(8*d['dd0']**2*math.exp(ln_ke)*d['tD']/(9*LN2))
    errs_el_all.append(abs(tp - d['tc'])/d['tc'])

errs_el_all = np.array(errs_el_all)
print(f"元素FG(全元素) → Tc: 中位={np.median(errs_el_all)*100:.1f}%, {np.mean(errs_el_all<=1)*100:.0f}%在2倍内")

print(f"\n对比基准:")
print(f"  GBR(纯几何19特征): 中位 47%, 79%在2倍内")
print(f"  one-hot类别:        中位 45%, 81%在2倍内")