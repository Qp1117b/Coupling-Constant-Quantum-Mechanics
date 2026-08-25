"""Ŝ_5 混合谱: A4 四基频整数组合 → 完整谱表
检验: A4 基频能否直接复现 166 材料的 Γ 分布
"""
import csv, re, math
import numpy as np
from itertools import product

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
C2_geo = 2.0/3.0; LN2 = math.log(2)
RIEMANN_ZEROS = np.array([14.134725,21.022040,25.010858,30.424876,32.935062,37.586178,40.918720,43.311071,48.005150,49.773832])

ATOM_DB = {'H':(1.008,0,0.46,0),'He':(4.003,0,0.31,0),'Li':(6.94,344,1.52,11),'Be':(9.01,1440,1.12,130),'B':(10.81,1480,0.87,185),'C':(12.01,2230,0.77,338),'N':(14.01,0,0.75,0),'O':(16.00,0,0.73,0),'F':(19.00,0,0.72,0),'Ne':(20.18,0,0.71,0),'Na':(22.99,158,1.86,7),'Mg':(24.31,400,1.60,35),'Al':(26.98,428,1.43,76),'Si':(28.09,645,1.18,100),'P':(30.97,0,1.10,0),'S':(32.06,0,1.05,0),'Cl':(35.45,0,1.02,0),'K':(39.10,91,2.27,3),'Ca':(40.08,230,1.97,15),'Sc':(44.96,360,1.62,44),'Ti':(47.87,420,1.47,110),'V':(50.94,383,1.34,162),'Cr':(52.00,435,1.28,160),'Mn':(54.94,410,1.27,120),'Fe':(55.85,470,1.26,170),'Co':(58.93,445,1.25,180),'Ni':(58.69,450,1.24,180),'Cu':(63.55,343,1.28,140),'Zn':(65.38,327,1.34,70),'Ga':(69.72,240,1.35,40),'Ge':(72.63,374,1.22,75),'As':(74.92,0,1.21,0),'Se':(78.97,0,1.20,0),'Br':(79.90,0,1.20,0),'Rb':(85.47,56,2.48,2),'Sr':(87.62,147,2.15,12),'Y':(88.91,280,1.80,37),'Zr':(91.22,291,1.60,95),'Nb':(92.91,275,1.46,170),'Mo':(95.96,425,1.39,230),'Tc':(98.00,0,1.36,0),'Ru':(101.07,0,1.34,220),'Rh':(102.91,0,1.34,150),'Pd':(106.42,274,1.37,180),'Ag':(107.87,215,1.44,100),'Cd':(112.41,209,1.49,42),'In':(114.82,108,1.62,11),'Sn':(118.71,200,1.58,50),'Sb':(121.76,0,1.61,0),'Te':(127.60,0,1.60,0),'I':(126.90,0,1.63,0),'Cs':(132.91,38,2.65,2),'Ba':(137.33,110,2.22,9),'La':(138.91,142,1.87,24),'Ce':(140.12,0,1.82,22),'Pr':(140.91,0,1.82,21),'Nd':(144.24,0,1.82,20),'Sm':(150.36,0,1.81,18),'Eu':(151.96,0,1.81,8),'Gd':(157.25,0,1.80,25),'Tb':(158.93,0,1.79,25),'Dy':(162.50,0,1.79,25),'Ho':(164.93,0,1.78,26),'Er':(167.26,0,1.78,26),'Tm':(168.93,0,1.77,28),'Yb':(173.05,0,1.77,10),'Lu':(174.97,0,1.77,30),'Hf':(178.49,252,1.59,110),'Ta':(180.95,240,1.46,200),'W':(183.84,400,1.39,310),'Re':(186.21,430,1.37,370),'Os':(190.23,500,1.35,400),'Ir':(192.22,420,1.36,355),'Pt':(195.08,240,1.39,230),'Au':(196.97,170,1.44,180),'Hg':(200.59,0,1.51,25),'Tl':(204.38,78,1.70,8),'Pb':(207.20,105,1.75,23),'Bi':(208.98,0,1.70,0),'Th':(232.04,163,1.80,54)}
HF_EL = {'Ce','Yb','U','Pr','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Lu','Nd','Np','Pu'}
GL1_CATS = {'元素超导体(常压)','元素超导体(高压)','A15结构金属间化合物','合金超导体','其他金属间化合物','氢化物高压超导体','石墨插层超导体','其他特殊超导体'}
GL2_CATS = {'铜氧化物高温超导体','铁基超导体','有机超导体','富勒烯超导体'}

def atom_db(el): return ATOM_DB.get(el, (100.0, 200, 1.5, 0))
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
    tz = sum(a[el]*atom_db(el)[3] for el in a)
    return {'M':tm,'N':na,'l':l,'tD':td,'V':V,'G':G,'dd0':dd,'B':B,'hf':hf,'Z':tz}

data = []
with open("superconductors_deduplicated.csv",'r',encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc <= 0: continue
        mp = cp(row['材料(化学式)'])
        if mp is None or mp['dd0'] == 0: continue
        cat = row['类别']
        gl = 1 if cat in GL1_CATS else 2
        data.append({**mp,'formula':row['材料(化学式)'],'cat':cat,'tc':tc,'gl':gl})

# 反推 Γ
COEF = np.array([0.2358, -1.5477, -1.3720, 0.7953, -0.1227, -0.9642, 2.5884])
non_hf = [d for d in data if not (d['hf'] and d['gl'] == 1)]
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

for d in data:
    ln_ke = math.log(d['tc']**2 * 9 * LN2 / (8 * d['dd0']**2 * d['tD']))
    geom = (COEF[1]*math.log(d['G']) + COEF[2]*math.log(d['tD']) +
            COEF[3]*math.log(d['B']) + COEF[4]*math.log(d['N']) + COEF[5]*math.log(d['V']) + COEF[6])
    d['Gamma'] = (ln_ke - geom) / COEF[0]

# A4 基频 (√来自嘉当矩阵特征值)
omega_raw = np.array([1.0/np.sqrt(0.38196601), 1.0/np.sqrt(1.38196601), 1.0/np.sqrt(2.61803399), 1.0/np.sqrt(3.61803399)])

# ζ零点作为校准点: γ_2 - γ_1 = ω_2 + ω_1 - ω_1 = ω_2
# 但我们需要精确匹配所有 γ_n

# 标度：使得 ω_1 ≈ γ_1
scale = RIEMANN_ZEROS[0] / omega_raw[0]
omega = omega_raw * scale

CAT_J = {'铜氧化物高温超导体':2,'铁基超导体':1,'有机超导体':1,'富勒烯超导体':1}
CAT_D = {'铜氧化物高温超导体':2.0,'铁基超导体':2.0,'有机超导体':1.5,'富勒烯超导体':2.0}

# 计算各类别 Γ 中位
cats = {}
for d in data:
    cats.setdefault(d['cat'], []).append(d['Gamma'])

cat_targets = {}
for cat, gs in cats.items():
    cat_targets[cat] = np.median(gs)

# ============================================================
# 全面搜索 A4 四基频整数组合，匹配 Γ
# ============================================================
print("="*80)
print("Ŝ_5 混合谱: A4 四基频整数组合 → 匹配材料 Γ")
print("="*80)

print(f"\nA4 基频(标度后): ω = [{omega[0]:.4f}, {omega[1]:.4f}, {omega[2]:.4f}, {omega[3]:.4f}]")
print(f"ζ(s) 零点(前10): {RIEMANN_ZEROS[:10]}")

# 搜索所有 |n| ≤ N_max 的整数组合
N_max = 4
best_matches = {}  # cat -> (best_Gamma, best_n, error)

print(f"\n搜索 N ≤ {N_max} 的所有整数组合 (共 {(2*N_max+1)**4} 种)...")

for n1, n2, n3, n4 in product(range(0, N_max+1), repeat=4):
    Gamma_pred = n1*omega[0] + n2*omega[1] + n3*omega[2] + n4*omega[3]

    # 对所有类别计算误差
    for cat, Gamma_target in cat_targets.items():
        err = abs(Gamma_pred - Gamma_target)
        if cat not in best_matches or err < best_matches[cat][2]:
            best_matches[cat] = (Gamma_pred, (n1,n2,n3,n4), err)

print(f"\n{'类别':<22} {'j':>2} {'Γ中位':>8} {'Γ_A4':>8} {'Δ':>8} {'(n₁,n₂,n₃,n₄)':>15}")
print("-"*75)
for cat in sorted(cat_targets.keys()):
    j = CAT_J.get(cat, 0)
    Gamma_target = cat_targets[cat]
    Gamma_pred, ns, err = best_matches[cat]
    ns_str = f"({ns[0]},{ns[1]},{ns[2]},{ns[3]})"
    print(f"  {cat:<20} {j:>2} {Gamma_target:>8.2f} {Gamma_pred:>8.2f} {err:>8.2f} {ns_str:>15}")

# 全局统计: A4 基频匹配 ζ 零点
print(f"\n{'='*80}")
print("A4 基频组合匹配 ζ(s) 零点")
print(f"{'='*80}")

best_zeta = {}
for k in range(10):
    zeta = RIEMANN_ZEROS[k]
    if zeta not in best_zeta:
        for n1, n2, n3, n4 in product(range(0, N_max+1), repeat=4):
            Gamma_pred = n1*omega[0] + n2*omega[1] + n3*omega[2] + n4*omega[3]
            err = abs(Gamma_pred - zeta)
            if k not in best_zeta or err < best_zeta[k][1]:
                best_zeta[k] = (Gamma_pred, err, (n1,n2,n3,n4))

print(f"\n{'k':>2} {'γ_k':>8} {'Γ_A4':>8} {'Δ':>8} {'(n₁,n₂,n₃,n₄)':>15}")
print("-"*55)
for k in range(10):
    Gamma_pred, err, ns = best_zeta[k]
    ns_str = f"({ns[0]},{ns[1]},{ns[2]},{ns[3]})"
    print(f"  {k+1:>2} {RIEMANN_ZEROS[k]:>8.2f} {Gamma_pred:>8.2f} {err:>8.2f} {ns_str:>15}")

# ============================================================
# 优化标度因子
# ============================================================
print(f"\n{'='*80}")
print("优化 A4 基频标度（最小化 ζ 零点匹配误差）")
print(f"{'='*80}")

from scipy.optimize import minimize

def zeta_error(scale_factor):
    omega_scaled = omega_raw * scale_factor
    total_err = 0
    for k in range(10):
        zeta = RIEMANN_ZEROS[k]
        best_err = float('inf')
        for n1, n2, n3, n4 in product(range(0, 5), repeat=4):
            Gamma_pred = n1*omega_scaled[0] + n2*omega_scaled[1] + n3*omega_scaled[2] + n4*omega_scaled[3]
            err = abs(Gamma_pred - zeta)
            if err < best_err:
                best_err = err
        total_err += best_err**2
    return total_err

r = minimize(zeta_error, x0=[scale], method='Nelder-Mead')
scale_opt = r.x[0]
omega_opt = omega_raw * scale_opt
print(f"最佳标度: {scale_opt:.4f} (原始: {scale:.4f})")
print(f"基频: {omega_opt}")

# 用优化后的基频重新匹配
best_zeta_opt = {}
for k in range(10):
    zeta = RIEMANN_ZEROS[k]
    for n1, n2, n3, n4 in product(range(0, 5), repeat=4):
        Gamma_pred = n1*omega_opt[0] + n2*omega_opt[1] + n3*omega_opt[2] + n4*omega_opt[3]
        err = abs(Gamma_pred - zeta)
        if k not in best_zeta_opt or err < best_zeta_opt[k][1]:
            best_zeta_opt[k] = (Gamma_pred, err, (n1,n2,n3,n4))

print(f"\n优化后 A4 → ζ 零点匹配:")
print(f"{'k':>2} {'γ_k':>8} {'Γ_A4':>8} {'Δ':>8} {'(n₁,n₂,n₃,n₄)':>15}")
print("-"*55)
for k in range(10):
    Gamma_pred, err, ns = best_zeta_opt[k]
    print(f"  {k+1:>2} {RIEMANN_ZEROS[k]:>8.2f} {Gamma_pred:>8.2f} {err:>8.2f} ({ns[0]},{ns[1]},{ns[2]},{ns[3]})")

# 全局材料匹配
print(f"\n用优化基频匹配材料 Γ:")
best_materials_opt = {}
for cat in sorted(cat_targets.keys()):
    Gamma_target = cat_targets[cat]
    for n1, n2, n3, n4 in product(range(0, N_max+1), repeat=4):
        Gamma_pred = n1*omega_opt[0] + n2*omega_opt[1] + n3*omega_opt[2] + n4*omega_opt[3]
        err = abs(Gamma_pred - Gamma_target)
        if cat not in best_materials_opt or err < best_materials_opt[cat][2]:
            best_materials_opt[cat] = (Gamma_pred, (n1,n2,n3,n4), err)

print(f"\n{'类别':<22} {'j':>2} {'Γ中位':>8} {'Γ_A4':>8} {'Δ':>8} {'(n₁,n₂,n₃,n₄)':>15}")
print("-"*75)
for cat in sorted(cat_targets.keys()):
    j = CAT_J.get(cat, 0)
    Gamma_pred, ns, err = best_materials_opt[cat]
    print(f"  {cat:<20} {j:>2} {cat_targets[cat]:>8.2f} {Gamma_pred:>8.2f} {err:>8.2f} ({ns[0]},{ns[1]},{ns[2]},{ns[3]})")

# 统计总误差
total = sum(best_materials_opt[cat][2] for cat in best_materials_opt)
print(f"\n总匹配误差(各类别Γ中位): {total:.2f}")
print(f"平均每类别: {total/len(best_materials_opt):.2f}")