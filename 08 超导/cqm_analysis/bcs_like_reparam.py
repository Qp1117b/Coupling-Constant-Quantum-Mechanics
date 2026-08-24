"""
BCS-like重新参数化探索

BCS: Tc = 1.14·θ_D·exp(-1/(N(0)V - μ*))
  N(0)V ~ 0.3-0.5 (不接近0), μ* ~ 0.1-0.15
  指数敏感度适中

CQM当前: Tc = θ_D/(2·arccoth(x)), x = A/GAP ≈ 1 + 10⁻¹⁵
  等价于 Tc ≈ θ_D/ln(2/ε), ε ~ 10⁻¹⁵
  双指数敏感度

尝试BCS-like形式:
  Tc = θ_D · exp(-c/Δδ₀²)  [耦合~Δδ₀²]
  Tc = θ_D · exp(-c/(β²Δδ₀²))  [耦合~β²Δδ₀²]
  Tc = θ_D · Δδ₀^a  [幂律]
  Tc = θ_D · (β·Δδ₀)^a  [幂律]

关键：用从材料第一性计算的Δδ₀，不需要δ_v
"""

import csv, re, math
import numpy as np
from collections import defaultdict

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
BETA = 8 * math.pi + 1
GAP = 21.022040 - 14.134725
C2 = 2.0 / 3.0

ATOM_DB = {
    'H': (1.008, 0, 0.46, 0), 'He': (4.003, 0, 0.31, 0),
    'Li': (6.94, 344, 1.52, 11), 'Be': (9.01, 1440, 1.12, 130),
    'B': (10.81, 1480, 0.87, 185), 'C': (12.01, 2230, 0.77, 338),
    'N': (14.01, 0, 0.75, 0), 'O': (16.00, 0, 0.73, 0),
    'F': (19.00, 0, 0.72, 0), 'Ne': (20.18, 0, 0.71, 0),
    'Na': (22.99, 158, 1.86, 7), 'Mg': (24.31, 400, 1.60, 35),
    'Al': (26.98, 428, 1.43, 76), 'Si': (28.09, 645, 1.18, 100),
    'P': (30.97, 0, 1.10, 0), 'S': (32.06, 0, 1.05, 0),
    'Cl': (35.45, 0, 1.02, 0), 'K': (39.10, 91, 2.27, 3),
    'Ca': (40.08, 230, 1.97, 15), 'Sc': (44.96, 360, 1.62, 44),
    'Ti': (47.87, 420, 1.47, 110), 'V': (50.94, 383, 1.34, 162),
    'Cr': (52.00, 435, 1.28, 160), 'Mn': (54.94, 410, 1.27, 120),
    'Fe': (55.85, 470, 1.26, 170), 'Co': (58.93, 445, 1.25, 180),
    'Ni': (58.69, 450, 1.24, 180), 'Cu': (63.55, 343, 1.28, 140),
    'Zn': (65.38, 327, 1.34, 70), 'Ga': (69.72, 240, 1.35, 40),
    'Ge': (72.63, 374, 1.22, 75), 'As': (74.92, 0, 1.21, 0),
    'Se': (78.97, 0, 1.20, 0), 'Br': (79.90, 0, 1.20, 0),
    'Rb': (85.47, 56, 2.48, 2), 'Sr': (87.62, 147, 2.15, 12),
    'Y': (88.91, 280, 1.80, 37), 'Zr': (91.22, 291, 1.60, 95),
    'Nb': (92.91, 275, 1.46, 170), 'Mo': (95.96, 425, 1.39, 230),
    'Tc': (98.00, 0, 1.36, 0), 'Ru': (101.07, 0, 1.34, 220),
    'Rh': (102.91, 0, 1.34, 150), 'Pd': (106.42, 274, 1.37, 180),
    'Ag': (107.87, 215, 1.44, 100), 'Cd': (112.41, 209, 1.49, 42),
    'In': (114.82, 108, 1.62, 11), 'Sn': (118.71, 200, 1.58, 50),
    'Sb': (121.76, 0, 1.61, 0), 'Te': (127.60, 0, 1.60, 0),
    'I': (126.90, 0, 1.63, 0), 'Cs': (132.91, 38, 2.65, 2),
    'Ba': (137.33, 110, 2.22, 9), 'La': (138.91, 142, 1.87, 24),
    'Ce': (140.12, 0, 1.82, 22), 'Pr': (140.91, 0, 1.82, 21),
    'Nd': (144.24, 0, 1.82, 20), 'Sm': (150.36, 0, 1.81, 18),
    'Eu': (151.96, 0, 1.81, 8), 'Gd': (157.25, 0, 1.80, 25),
    'Tb': (158.93, 0, 1.79, 25), 'Dy': (162.50, 0, 1.79, 25),
    'Ho': (164.93, 0, 1.78, 26), 'Er': (167.26, 0, 1.78, 26),
    'Tm': (168.93, 0, 1.77, 28), 'Yb': (173.05, 0, 1.77, 10),
    'Lu': (174.97, 0, 1.77, 30), 'Hf': (178.49, 252, 1.59, 110),
    'Ta': (180.95, 240, 1.46, 200), 'W': (183.84, 400, 1.39, 310),
    'Re': (186.21, 430, 1.37, 370), 'Os': (190.23, 500, 1.35, 400),
    'Ir': (192.22, 420, 1.36, 355), 'Pt': (195.08, 240, 1.39, 230),
    'Au': (196.97, 170, 1.44, 180), 'Hg': (200.59, 0, 1.51, 25),
    'Tl': (204.38, 78, 1.70, 8), 'Pb': (207.20, 105, 1.75, 23),
    'Bi': (208.98, 0, 1.70, 0), 'Th': (232.04, 163, 1.80, 54),
    'Pa': (231.04, 0, 1.80, 0), 'U': (238.03, 207, 1.75, 100),
}

def parse_formula(f):
    f = re.sub(r'[\(（].*?[\)）]', '', f.strip())
    return {e: (float(c) if c else 1.0) for e,c in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f) if e in ATOM_DB}

def get_mass(c): return sum(ATOM_DB[e][0]*n for e,n in c.items())
def get_debye(c):
    ws = [(ATOM_DB[e][1], ATOM_DB[e][0]*n) for e,n in c.items() if ATOM_DB[e][1]>0]
    return sum(d*w for d,w in ws)/sum(w for _,w in ws) if ws else 300
def get_radius(c):
    rs = [ATOM_DB[e][2] for e in c if ATOM_DB[e][2]>0]
    return np.mean(rs) if rs else 1.5
def get_bulk(c):
    bs = [ATOM_DB[e][3] for e in c if ATOM_DB[e][3]>0]
    return np.mean(bs) if bs else 50

def ddv_inter(M, L, tD, z, f=0.5):
    L_m = L*1e-10; w = tD*KB/HBAR; s = z*2.0/(M*AMU)
    return math.sqrt(max((C2/L_m**2)*(3*HBAR/(4*w))*(1-f)*s, 0))

def ddv_intra(edges, l, tD, f=0.5):
    l_m = l*1e-10; w = tD*KB/HBAR
    s = sum((1.0/(mi*AMU)+1.0/(mj*AMU)) for mi,mj in edges)
    return math.sqrt(max((C2/l_m**2)*(3*HBAR/(4*w))*(1-f)*s, 0))

def estimate_params(formula, cat, condition):
    comp = parse_formula(formula)
    if not comp: return None
    n_atoms = sum(comp.values())
    M = get_mass(comp); r = get_radius(comp); tD = get_debye(comp); B = get_bulk(comp)
    P = 0
    if '高压' in condition or 'GPa' in condition:
        pm = re.search(r'~?(\d+)GPa', condition)
        P = int(pm.group(1)) if pm else 50
    L = 2*r; l_intra = 2*r; z = 6; edges = []; f = 0.5
    if '元素' in cat:
        tD = ATOM_DB.get(list(comp.keys())[0], (0,300,1.5,50))[1] or tD
        if tD < 50: tD = 300
        z = 12; f = 0.5
        if '高压' in cat: B = max(get_bulk(comp),50)*3; P = max(P,100)
    elif 'A15' in cat: tD = max(tD,400); z = 8; L = 2*r*0.9; f = 0.4
    elif '氢化物' in cat:
        tD = max(tD,1500); B = max(B,200); P = max(P,150); z = 8; L = 2.0; l_intra = 1.7
        n_h = comp.get('H',0); n_m = n_atoms - n_h
        if n_h > 0 and n_m > 0:
            m_m = (M - n_h*1.008)/n_m; edges = [(m_m,1.008)]*int(min(n_h,4))
        f = 0.5
    elif '铜氧' in cat:
        tD = max(tD,400); z = 6; L = 3.8; l_intra = 1.9
        if 'Cu' in comp and 'O' in comp: edges = [(63.55,16.0)]*2
        f = 0.4
    elif '铁基' in cat:
        tD = max(tD,350); z = 6; L = 3.5; l_intra = 2.0
        if 'Fe' in comp:
            if 'As' in comp: edges = [(55.85,74.92)]*2
            elif 'Se' in comp: edges = [(55.85,78.97)]*2
        f = 0.4
    elif '有机' in cat: tD = max(tD,100); z = 4; L = 5.0; f = 0.5
    elif '富勒烯' in cat: tD = 100; z = 4; L = 10.0; M = 720; f = 0.5
    elif '石墨' in cat: tD = 200; z = 3; L = 3.35; f = 0.5
    elif '合金' in cat: tD = max(tD,200); z = 12; f = 0.5
    else: tD = max(tD,200); z = 8; f = 0.5
    return tD, M, L, z, edges, l_intra, B, P, f

# 加载数据
with open("superconductors_deduplicated.csv", 'r', encoding='utf-8-sig') as fh:
    reader = csv.reader(fh); header = next(reader); rows = list(reader)

all_data = []
for row in rows:
    cat = row[0]; formula = row[1]; tc_str = row[3]
    condition = row[7] if len(row) > 7 else ''
    tc_match = re.match(r'~?(\d+\.?\d*)', tc_str.strip())
    if not tc_match: continue
    tc = float(tc_match.group(1))
    params = estimate_params(formula, cat, condition)
    if not params: continue
    tD, M, L, z, edges, l_intra, B, P, f = params
    di = ddv_inter(M, L, tD, z, f)
    dn = ddv_intra(edges, l_intra, tD, f) if edges else 0
    ddv0 = math.sqrt(di**2 + dn**2)
    lam = 3 * BETA**2 * ddv0**2 / (16 * GAP)
    all_data.append({'formula': formula, 'cat': cat, 'tc': tc, 'tD': tD,
                     'ddv0': ddv0, 'lam': lam})

print(f"加载 {len(all_data)} 个材料")

# ============================================================
# 尝试BCS-like形式
# ============================================================
print(f"\n{'='*90}")
print("BCS-like重新参数化")
print("=" * 90)

# 形式1: Tc = θ_D · exp(-c/Δδ₀²)  [BCS-like, 耦合~Δδ₀²]
print("\n形式1: Tc = θ_D · exp(-c/Δδ₀²)")
print("-" * 60)
# 反推c: c = -Δδ₀² · ln(Tc/θ_D)
cs = [-d['ddv0']**2 * np.log(d['tc']/d['tD']) for d in all_data]
cs = np.array(cs)
print(f"  c: 均值={np.mean(cs):.5f}, 中位数={np.median(cs):.5f}, CV={np.std(cs)/np.mean(cs)*100:.0f}%")

# 形式2: Tc = θ_D · exp(-c/(β²Δδ₀²))  [耦合~β²Δδ₀²]
print("\n形式2: Tc = θ_D · exp(-c/(β²Δδ₀²))")
cs2 = [-(BETA*d['ddv0'])**2 * np.log(d['tc']/d['tD']) for d in all_data]
cs2 = np.array(cs2)
print(f"  c: 均值={np.mean(cs2):.4f}, 中位数={np.median(cs2):.4f}, CV={np.std(cs2)/np.mean(cs2)*100:.0f}%")

# 形式3: Tc = θ_D · (β·Δδ₀)^a  [幂律]
print("\n形式3: Tc = θ_D · (β·Δδ₀)^a")
# ln(Tc/θ_D) = a·ln(β·Δδ₀) → a = ln(Tc/θ_D)/ln(β·Δδ₀)
as_ = [np.log(d['tc']/d['tD'])/np.log(BETA*d['ddv0']) for d in all_data if BETA*d['ddv0'] < 1]
as_ = np.array(as_)
print(f"  a: 均值={np.mean(as_):.3f}, 中位数={np.median(as_):.3f}, CV={np.std(as_)/abs(np.mean(as_))*100:.0f}%")

# 形式4: Tc = θ_D · Δδ₀^a  [幂律, 无β]
print("\n形式4: Tc = θ_D · Δδ₀^a")
as4 = [np.log(d['tc']/d['tD'])/np.log(d['ddv0']) for d in all_data if d['ddv0'] < 1]
as4 = np.array(as4)
print(f"  a: 均值={np.mean(as4):.3f}, 中位数={np.median(as4):.3f}, CV={np.std(as4)/abs(np.mean(as4))*100:.0f}%")

# 形式5: ln(Tc) = a·ln(θ_D) + b·ln(Δδ₀) + c  [多变量回归]
print("\n形式5: ln(Tc) = a·ln(θ_D) + b·ln(Δδ₀) + c")
from numpy.linalg import lstsq
X = np.array([[np.log(d['tD']), np.log(d['ddv0']), 1] for d in all_data])
y = np.array([np.log(d['tc']) for d in all_data])
coef, residuals, _, _ = lstsq(X, y, rcond=None)
a5, b5, c5 = coef
tc_pred5 = np.exp(X @ coef)
y_exp = np.array([d['tc'] for d in all_data])
errs5 = np.abs(tc_pred5 - y_exp) / y_exp
print(f"  a={a5:.3f}, b={b5:.3f}, c={c5:.3f}")
print(f"  中位误差={np.median(errs5)*100:.0f}%, 2倍内={np.sum(errs5<1)/len(errs5)*100:.0f}%")

# 形式6: ln(Tc) = a·ln(θ_D) + b·ln(λ) + c  [λ=3β²Δδ₀²/(16GAP)]
print("\n形式6: ln(Tc) = a·ln(θ_D) + b·ln(λ) + c")
X6 = np.array([[np.log(d['tD']), np.log(d['lam']), 1] for d in all_data if d['lam'] > 0])
y6 = np.array([np.log(d['tc']) for d in all_data if d['lam'] > 0])
coef6, _, _, _ = lstsq(X6, y6, rcond=None)
tc_pred6 = np.exp(X6 @ coef6)
errs6 = np.abs(tc_pred6 - np.exp(y6)) / np.exp(y6)
print(f"  a={coef6[0]:.3f}, b={coef6[1]:.3f}, c={coef6[2]:.3f}")
print(f"  中位误差={np.median(errs6)*100:.0f}%, 2倍内={np.sum(errs6<1)/len(errs6)*100:.0f}%")

# ============================================================
# 类别校准的形式5
# ============================================================
print(f"\n{'='*90}")
print("类别校准: ln(Tc) = a·ln(θ_D) + b·ln(Δδ₀) + c_cat")
print("=" * 90)

cat_data = defaultdict(list)
for d in all_data: cat_data[d['cat']].append(d)

# 留一法交叉验证
print("\n留一法交叉验证:")
all_preds_loo = []
all_exps_loo = []
for i, d_test in enumerate(all_data):
    cat = d_test['cat']
    # 用同类别其他材料拟合a,b,c
    train = [d for j,d in enumerate(all_data) if j != i and d['cat'] == cat]
    if len(train) < 5:
        # 用全局
        train = [d for j,d in enumerate(all_data) if j != i]
    X_tr = np.array([[np.log(d['tD']), np.log(d['ddv0']), 1] for d in train])
    y_tr = np.array([np.log(d['tc']) for d in train])
    try:
        coef_tr, _, _, _ = lstsq(X_tr, y_tr, rcond=None)
        x_test = np.array([np.log(d_test['tD']), np.log(d_test['ddv0']), 1])
        tc_pred = np.exp(x_test @ coef_tr)
        all_preds_loo.append(tc_pred)
        all_exps_loo.append(d_test['tc'])
    except:
        pass

errs_loo = np.abs(np.array(all_preds_loo) - np.array(all_exps_loo)) / np.array(all_exps_loo)
print(f"  材料数: {len(errs_loo)}")
print(f"  中位误差: {np.median(errs_loo)*100:.0f}%")
print(f"  平均误差: {np.mean(errs_loo)*100:.0f}%")
print(f"  2倍内: {np.sum(errs_loo<1)/len(errs_loo)*100:.0f}%")
print(f"  5倍内: {np.sum(errs_loo<4)/len(errs_loo)*100:.0f}%")

# ============================================================
# 对比：当前arccoth反推法
# ============================================================
print(f"\n{'='*90}")
print("对比总结")
print("=" * 90)
print(f"""
方法                        | 中位误差 | 2倍内 | 需要δ_v?
----------------------------+----------+-------+--------
arccoth反推(当前)            |    0%    | 100%  | 是(15位精度)
半第一性(类别b_cat)          |   57%    |  53%  | 否
路径A(类别α)                |    1%    |  59%  | 是(反推)
BCS-like回归(全局3参数)      |   {np.median(errs5)*100:.0f}%    |  {np.sum(errs5<1)/len(errs5)*100:.0f}%  | 否
BCS-like回归(LOOCV类别)      |   {np.median(errs_loo)*100:.0f}%    |  {np.sum(errs_loo<1)/len(errs_loo)*100:.0f}%  | 否

关键：BCS-like回归不需要δ_v，纯从Δδ₀和θ_D预测Tc
  Δδ₀从晶格结构第一性计算 ✓
  θ_D从Debye温度查表 ✓
  回归系数a,b,c从训练集校准 (类似BCS的μ*)
""")

# 敏感度对比
print(f"\n敏感度对比 (Nb):")
nb = next(d for d in all_data if d['formula'] == 'Nb')
# BCS-like: Tc = θ_D · exp(-c/Δδ₀²)
c_nb = -nb['ddv0']**2 * np.log(nb['tc']/nb['tD'])
Tc0 = nb['tD'] * np.exp(-c_nb/nb['ddv0']**2)
ddv0_pert = nb['ddv0'] * 1.01
Tc_pert = nb['tD'] * np.exp(-c_nb/ddv0_pert**2)
sens_bcs = abs(Tc_pert - Tc0) / Tc0 / 0.01
print(f"  BCS-like: Tc={Tc0:.2f}K, Δδ₀变1%→Tc变{sens_bcs*100:.0f}%")
print(f"  arccoth:   Tc=9.20K, Δδ₀变1%→Tc变~46000%")
print(f"  敏感度降低: {46000/sens_bcs:.0f}倍")