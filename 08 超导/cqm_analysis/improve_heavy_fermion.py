"""改进重费米子精度分析"""
import csv, re, math
import numpy as np

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
BETA = 8 * math.pi + 1; C2 = 2.0/3.0; LN2 = math.log(2)
RIEMANN_ZEROS = [14.134725,21.022040,25.010858,30.424876,32.935062,37.586178,40.918720,43.311071,48.005150,49.773832]

ATOM_DB = {'H':(1.008,0,0.46,0),'He':(4.003,0,0.31,0),'Li':(6.94,344,1.52,11),'Be':(9.01,1440,1.12,130),'B':(10.81,1480,0.87,185),'C':(12.01,2230,0.77,338),'N':(14.01,0,0.75,0),'O':(16.00,0,0.73,0),'F':(19.00,0,0.72,0),'Ne':(20.18,0,0.71,0),'Na':(22.99,158,1.86,7),'Mg':(24.31,400,1.60,35),'Al':(26.98,428,1.43,76),'Si':(28.09,645,1.18,100),'P':(30.97,0,1.10,0),'S':(32.06,0,1.05,0),'Cl':(35.45,0,1.02,0),'K':(39.10,91,2.27,3),'Ca':(40.08,230,1.97,15),'Sc':(44.96,360,1.62,44),'Ti':(47.87,420,1.47,110),'V':(50.94,383,1.34,162),'Cr':(52.00,435,1.28,160),'Mn':(54.94,410,1.27,120),'Fe':(55.85,470,1.26,170),'Co':(58.93,445,1.25,180),'Ni':(58.69,450,1.24,180),'Cu':(63.55,343,1.28,140),'Zn':(65.38,327,1.34,70),'Ga':(69.72,240,1.35,40),'Ge':(72.63,374,1.22,75),'As':(74.92,0,1.21,0),'Se':(78.97,0,1.20,0),'Br':(79.90,0,1.20,0),'Rb':(85.47,56,2.48,2),'Sr':(87.62,147,2.15,12),'Y':(88.91,280,1.80,37),'Zr':(91.22,291,1.60,95),'Nb':(92.91,275,1.46,170),'Mo':(95.96,425,1.39,230),'Tc':(98.00,0,1.36,0),'Ru':(101.07,0,1.34,220),'Rh':(102.91,0,1.34,150),'Pd':(106.42,274,1.37,180),'Ag':(107.87,215,1.44,100),'Cd':(112.41,209,1.49,42),'In':(114.82,108,1.62,11),'Sn':(118.71,200,1.58,50),'Sb':(121.76,0,1.61,0),'Te':(127.60,0,1.60,0),'I':(126.90,0,1.63,0),'Cs':(132.91,38,2.65,2),'Ba':(137.33,110,2.22,9),'La':(138.91,142,1.87,24),'Ce':(140.12,0,1.82,22),'Pr':(140.91,0,1.82,21),'Nd':(144.24,0,1.82,20),'Sm':(150.36,0,1.81,18),'Eu':(151.96,0,1.81,8),'Gd':(157.25,0,1.80,25),'Tb':(158.93,0,1.79,25),'Dy':(162.50,0,1.79,25),'Ho':(164.93,0,1.78,26),'Er':(167.26,0,1.78,26),'Tm':(168.93,0,1.77,28),'Yb':(173.05,0,1.77,10),'Lu':(174.97,0,1.77,30),'Hf':(178.49,252,1.59,110),'Ta':(180.95,240,1.46,200),'W':(183.84,400,1.39,310),'Re':(186.21,430,1.37,370),'Os':(190.23,500,1.35,400),'Ir':(192.22,420,1.36,355),'Pt':(195.08,240,1.39,230),'Au':(196.97,170,1.44,180),'Hg':(200.59,0,1.51,25),'Tl':(204.38,78,1.70,8),'Pb':(207.20,105,1.75,23),'Bi':(208.98,0,1.70,0),'Th':(232.04,163,1.80,54),'Pa':(231.04,0,1.80,0),'U':(238.03,0,1.80,92)}

HF_EL = {'Ce','Yb','U','Pr','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Lu','Nd','Np','Pu'}

def pf(f):
    pairs = re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f)
    a = {}
    for el, cnt in pairs:
        if el in ATOM_DB: a[el] = a.get(el,0)+(float(cnt) if cnt else 1.0)
    return a

def cp(formula):
    a = pf(formula)
    if not a: return None
    tm = sum(a[el]*ATOM_DB[el][0] for el in a)
    na = sum(a.values())
    ar = sum(a[el]*ATOM_DB[el][2] for el in a)/na
    l = 2*ar*1e-10
    td = sum(a[el]*ATOM_DB[el][1] for el in a)/na
    if td == 0: return None
    V = l**3
    f = 1.0-0.3*(1.0-1.0/na)
    es = 0
    els = list(a.keys())
    for i in range(len(els)):
        for j in range(i+1,len(els)):
            es += 1.0/(a[els[i]]*ATOM_DB[els[i]][0]*AMU) + 1.0/(a[els[j]]*ATOM_DB[els[j]][0]*AMU)
    if not es:
        mi = tm*AMU/na
        es = (na*(na-1)/2)*2.0/mi
    G = (1.0/l)*math.sqrt((1.0-f)*es)
    od = td*KB/HBAR
    dd = math.sqrt(abs((C2/l**2)*(3*HBAR/(4*od))*(1-f)*es))
    B = tm*td**2*KB/V*1e-3
    hf = any(el in HF_EL for el in a)
    return {'M':tm,'N':na,'l':l,'tD':td,'V':V,'G':G,'dd0':dd,'B':B,'atoms':a,'hf':hf}

# 收集重费米子材料（排除石墨插层和氢化物中的HF）
hf_materials = []
with open("superconductors_deduplicated.csv",'r',encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc <= 0: continue
        mp = cp(row['材料(化学式)'])
        if mp is None: continue
        cat = row['类别']
        # 只取真正的重费米子超导体（其他金属间化合物中的HF）
        if cat != '其他金属间化合物': continue
        if not mp['hf']: continue
        hf_materials.append({**mp,'formula':row['材料(化学式)'],'tc':tc,'cat':cat})

print(f"重费米子超导体（其他金属间化合物中的f电子材料）: {len(hf_materials)}个\n")

# 计算每个重费米子的γ_eff_implicit（从Tc反推）
COEF = [0.2358, -1.5477, -1.3720, 0.7953, -0.1227, -0.9642, 2.5884]
LAM = 0.3898

print(f"{'材料':<15} {'Tc_exp':>7} {'γ_eff_implicit':>15} {'n当前':>5} {'γ_n当前':>8} {'误差当前':>10}")
print("-"*70)

results = []
for m in hf_materials:
    # 从Tc反推γ_eff
    ke = m['tc']**2*9*LN2/(8*m['dd0']**2*m['tD'])
    ln_ke = math.log(ke)
    # ln_ke = COEF[0]*ge + COEF[1]*lnG + COEF[2]*lnθD + COEF[3]*lnB + COEF[4]*lnN + COEF[5]*lnV + COEF[6]
    other = (COEF[1]*math.log(m['G']) + COEF[2]*math.log(m['tD']) +
             COEF[3]*math.log(m['B']) + COEF[4]*math.log(m['N']) + COEF[5]*math.log(m['V']) + COEF[6])
    ge_implicit = (ln_ke - other) / COEF[0]

    # 当前n=1, j=0
    gn_current = RIEMANN_ZEROS[0]  # n=1
    ge_current = gn_current
    lk_current = COEF[0]*ge_current + other
    tp_current = math.sqrt(8*m['dd0']**2*math.exp(lk_current)*m['tD']/(9*LN2))
    err_current = abs(tp_current - m['tc'])/m['tc']

    # 找最近的黎曼零点
    n_nearest = 1
    min_dist = abs(ge_implicit - RIEMANN_ZEROS[0])
    for n in range(1, 11):
        d = abs(ge_implicit - RIEMANN_ZEROS[n-1])
        if d < min_dist:
            min_dist = d
            n_nearest = n

    results.append({**m,'ge_implicit':ge_implicit,'n_nearest':n_nearest,'err_current':err_current})
    print(f"{m['formula']:<15} {m['tc']:>7.2f} {ge_implicit:>15.2f} {1:>5} {gn_current:>8.2f} {err_current*100:>9.1f}%")

print(f"\n{'='*70}")
print("γ_eff_implicit统计")
print(f"{'='*70}")
ge_arr = np.array([r['ge_implicit'] for r in results])
print(f"均值: {np.mean(ge_arr):.2f}")
print(f"中位: {np.median(ge_arr):.2f}")
print(f"标准差: {np.std(ge_arr):.2f}")
print(f"范围: [{np.min(ge_arr):.2f}, {np.max(ge_arr):.2f}]")
print(f"γ_1 = 14.13, γ_2 = 21.02, γ_3 = 25.01")

# 按f电子元素分组
print(f"\n{'='*70}")
print("按f电子元素分组")
print(f"{'='*70}")
hf_groups = {}
for r in results:
    for el in r['atoms']:
        if el in HF_EL:
            hf_groups.setdefault(el, []).append(r)
            break

for el, rs in sorted(hf_groups.items()):
    ge_vals = [r['ge_implicit'] for r in rs]
    tc_vals = [r['tc'] for r in rs]
    print(f"\n{el}基重费米子 ({len(rs)}个):")
    print(f"  Tc范围: {min(tc_vals):.2f}-{max(tc_vals):.2f}K")
    print(f"  γ_eff范围: {min(ge_vals):.2f}-{max(ge_vals):.2f}")
    print(f"  γ_eff中位: {np.median(ge_vals):.2f}")

# 尝试：按f电子元素分别优化n
print(f"\n{'='*70}")
print("尝试：按f电子元素分别确定n")
print(f"{'='*70}")

# 对每个f电子元素，找使LOOCV中位误差最小的n
for el, rs in sorted(hf_groups.items()):
    if len(rs) < 2: continue
    best_n = 1
    best_err = float('inf')
    for n in range(1, 11):
        gn = RIEMANN_ZEROS[n-1]
        errs = []
        for r in rs:
            ge = gn  # j=0 for HF
            other = (COEF[1]*math.log(r['G']) + COEF[2]*math.log(r['tD']) +
                     COEF[3]*math.log(r['B']) + COEF[4]*math.log(r['N']) + COEF[5]*math.log(r['V']) + COEF[6])
            lk = COEF[0]*ge + other
            tp = math.sqrt(8*r['dd0']**2*math.exp(lk)*r['tD']/(9*LN2))
            errs.append(abs(tp - r['tc'])/r['tc'])
        med_err = np.median(errs)
        if med_err < best_err:
            best_err = med_err
            best_n = n
    print(f"{el}基: 最佳n={best_n} (γ_n={RIEMANN_ZEROS[best_n-1]:.2f}), 中位误差={best_err*100:.1f}%")

# 尝试：连续γ_eff = a + b*ln(Tc_Kondo)？
# 由于没有Kondo温度数据，尝试用材料参数预测γ_eff
print(f"\n{'='*70}")
print("尝试：用材料参数预测γ_eff（重费米子专用）")
print(f"{'='*70}")

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import LeaveOneOut

# 特征：ln(G), ln(θD), ln(B), ln(N), ln(V), ln(M), Z
X = np.array([[math.log(r['G']), math.log(r['tD']), math.log(r['B']),
               math.log(r['N']), math.log(r['V']), math.log(r['M']),
               sum(r['atoms'][el]*ATOM_DB[el][3] for el in r['atoms'])] for r in results])
y = np.array([r['ge_implicit'] for r in results])

# GBR
gbr = GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=42)
loo = LeaveOneOut()
preds_ge = np.zeros(len(results))
for train_idx, test_idx in loo.split(X):
    gbr.fit(X[train_idx], y[train_idx])
    preds_ge[test_idx] = gbr.predict(X[test_idx])

# 用预测的γ_eff计算Tc
errs_gbr = []
for i, r in enumerate(results):
    ge = preds_ge[i]
    other = (COEF[1]*math.log(r['G']) + COEF[2]*math.log(r['tD']) +
             COEF[3]*math.log(r['B']) + COEF[4]*math.log(r['N']) + COEF[5]*math.log(r['V']) + COEF[6])
    lk = COEF[0]*ge + other
    tp = math.sqrt(8*r['dd0']**2*math.exp(lk)*r['tD']/(9*LN2))
    errs_gbr.append(abs(tp - r['tc'])/r['tc'])

errs_gbr = np.array(errs_gbr)
print(f"GBR预测γ_eff → Tc: 中位{np.median(errs_gbr)*100:.1f}%, {np.mean(errs_gbr<=1)*100:.0f}%在2倍内, {np.mean(errs_gbr<=4)*100:.0f}%在5倍内")

# 对比：当前n=1
errs_current = np.array([r['err_current'] for r in results])
print(f"当前n=1:        中位{np.median(errs_current)*100:.1f}%, {np.mean(errs_current<=1)*100:.0f}%在2倍内, {np.mean(errs_current<=4)*100:.0f}%在5倍内")

# 线性回归
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
preds_lr = np.zeros(len(results))
for train_idx, test_idx in loo.split(X):
    lr.fit(X[train_idx], y[train_idx])
    preds_lr[test_idx] = lr.predict(X[test_idx])

errs_lr = []
for i, r in enumerate(results):
    ge = preds_lr[i]
    other = (COEF[1]*math.log(r['G']) + COEF[2]*math.log(r['tD']) +
             COEF[3]*math.log(r['B']) + COEF[4]*math.log(r['N']) + COEF[5]*math.log(r['V']) + COEF[6])
    lk = COEF[0]*ge + other
    tp = math.sqrt(8*r['dd0']**2*math.exp(lk)*r['tD']/(9*LN2))
    errs_lr.append(abs(tp - r['tc'])/r['tc'])

errs_lr = np.array(errs_lr)
print(f"线性回归γ_eff:   中位{np.median(errs_lr)*100:.1f}%, {np.mean(errs_lr<=1)*100:.0f}%在2倍内, {np.mean(errs_lr<=4)*100:.0f}%在5倍内")