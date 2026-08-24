"""
第一性Tc预测链条精确化
"""

import csv, re, math
import numpy as np
from collections import defaultdict
from scipy.optimize import minimize

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
BETA = 8 * math.pi + 1
C2 = 2.0 / 3.0
LN2 = math.log(2)
C = math.sqrt(C2)

RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832]

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
    pairs = re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f)
    atoms = {}
    for el, cnt in pairs:
        if el in ATOM_DB:
            atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    return atoms

def calc_params(formula):
    atoms = parse_formula(formula)
    if not atoms:
        return None
    total_m = sum(atoms[el] * ATOM_DB[el][0] for el in atoms)
    total_z = sum(atoms[el] * ATOM_DB[el][3] for el in atoms)
    n_atoms = sum(atoms.values())
    avg_r = sum(atoms[el] * ATOM_DB[el][2] for el in atoms) / n_atoms
    l = 2 * avg_r * 1e-10
    theta_d = sum(atoms[el] * ATOM_DB[el][1] for el in atoms) / n_atoms
    if theta_d == 0:
        return None
    V_cell = l**3
    f_corr = 1.0 - 0.3 * (1.0 - 1.0/n_atoms)
    edge_sum = 0
    els = list(atoms.keys())
    for i in range(len(els)):
        for j in range(i+1, len(els)):
            mi = atoms[els[i]] * ATOM_DB[els[i]][0] * AMU
            mj = atoms[els[j]] * ATOM_DB[els[j]][0] * AMU
            edge_sum += (1.0/mi + 1.0/mj)
    if not edge_sum:
        mi = total_m * AMU / n_atoms
        edge_sum = (n_atoms * (n_atoms-1) / 2) * 2.0 / mi
    G = (1.0/l) * math.sqrt((1.0 - f_corr) * edge_sum)
    omega_d = theta_d * KB / HBAR
    dd0_sq = (C2 / l**2) * (3*HBAR / (4*omega_d)) * (1 - f_corr) * edge_sum
    dd0 = math.sqrt(abs(dd0_sq))
    B_est = total_m * theta_d**2 * KB / V_cell * 1e-3
    return {'l': l, 'G': G, 'dd0': dd0, 'tD': theta_d,
            'M': total_m, 'Z': total_z, 'V': V_cell,
            'n_atoms': n_atoms, 'B': B_est}

data = []
with open("superconductors_deduplicated.csv", 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try:
            tc = float(row['临界温度 Tc (K)'])
        except:
            continue
        if tc <= 0:
            continue
        mp = calc_params(row['材料(化学式)'])
        if mp is None or mp['dd0'] == 0:
            continue
        cat = row['类别']
        k_eff = tc**2 * 9 * LN2 / (8 * mp['dd0']**2 * mp['tD'])
        data.append({'cat': cat, 'tc': tc, 'k_eff': k_eff, **mp})

print(f"加载 {len(data)} 个材料")
n_data = len(data)
categories = sorted(set(d['cat'] for d in data))
cat_idx = {c: i for i, c in enumerate(categories)}
n_cats = len(categories)
y = np.array([math.log(d['k_eff']) for d in data])

# ============================================================
# 方法1: γ_cat + G + θ_D (类别γ + 幂律分解)
# ============================================================
print("="*80)
print("方法1: ln(K_eff) = a·γ_cat + p·ln(G) + q·ln(θ_D) + b")
print("="*80)

def build_X(a_val):
    X = np.zeros((n_data, n_cats + 3))
    for i, d in enumerate(data):
        X[i, cat_idx[d['cat']]] = a_val
        X[i, n_cats] = math.log(d['G'])
        X[i, n_cats + 1] = math.log(d['tD'])
        X[i, n_cats + 2] = 1.0
    return X

# 优化a
def objective(a_val):
    X = build_X(a_val[0])
    coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    return np.sum((y - X @ coef)**2)

result = minimize(objective, x0=[0.369], method='Nelder-Mead')
a_opt = result.x[0]
X1 = build_X(a_opt)
coef1, _, _, _ = np.linalg.lstsq(X1, y, rcond=None)
r2_1 = 1 - np.sum((y - X1 @ coef1)**2) / np.sum((y - np.mean(y))**2)
print(f"a={a_opt:.4f}, p={coef1[n_cats]:.4f}, q={coef1[n_cats+1]:.4f}, b={coef1[n_cats+2]:.4f}")
print(f"R² = {r2_1:.4f}")

# LOOCV
def loocv_method1(a_val):
    errors = []
    for i in range(n_data):
        train = [data[j] for j in range(n_data) if j != i]
        cats_tr = sorted(set(dd['cat'] for dd in train))
        cidx_tr = {c: j for j, c in enumerate(cats_tr)}
        nct = len(cats_tr)
        X_tr = np.zeros((len(train), nct + 3))
        y_tr = np.zeros(len(train))
        for j, dd in enumerate(train):
            X_tr[j, cidx_tr[dd['cat']]] = a_val
            X_tr[j, nct] = math.log(dd['G'])
            X_tr[j, nct + 1] = math.log(dd['tD'])
            X_tr[j, nct + 2] = 1.0
            y_tr[j] = math.log(dd['k_eff'])
        coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
        if data[i]['cat'] not in cidx_tr:
            continue
        x_test = np.zeros(nct + 3)
        x_test[cidx_tr[data[i]['cat']]] = a_val
        x_test[nct] = math.log(data[i]['G'])
        x_test[nct + 1] = math.log(data[i]['tD'])
        x_test[nct + 2] = 1.0
        k_eff_pred = math.exp(x_test @ coef)
        tc_pred = math.sqrt(8 * data[i]['dd0']**2 * k_eff_pred * data[i]['tD'] / (9 * LN2))
        errors.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
    return np.array(errors)

err1 = loocv_method1(a_opt)
print(f"LOOCV: 中位{np.median(err1)*100:.0f}%, 2倍内{np.mean(err1<=1)*100:.0f}%, 5倍内{np.mean(err1<=4)*100:.0f}%")

# ============================================================
# 方法2: γ_cat + G + θ_D + 材料参数
# ============================================================
print(f"\n{'='*80}")
print("方法2: γ_cat + G + θ_D + M + Z + V + N + B")
print("="*80)

MAT_VARS = ['M', 'Z', 'V', 'n_atoms', 'B']

def build_X2(a_val):
    n_feat = n_cats + 2 + len(MAT_VARS) + 1
    X = np.zeros((n_data, n_feat))
    for i, d in enumerate(data):
        X[i, cat_idx[d['cat']]] = a_val
        X[i, n_cats] = math.log(d['G'])
        X[i, n_cats + 1] = math.log(d['tD'])
        for j, v in enumerate(MAT_VARS):
            X[i, n_cats + 2 + j] = math.log(d[v]) if d[v] > 0 else 0
        X[i, -1] = 1.0
    return X

X2 = build_X2(a_opt)
coef2, _, _, _ = np.linalg.lstsq(X2, y, rcond=None)
r2_2 = 1 - np.sum((y - X2 @ coef2)**2) / np.sum((y - np.mean(y))**2)
print(f"R² = {r2_2:.4f}")

# LOOCV
err2 = []
for i in range(n_data):
    train = [data[j] for j in range(n_data) if j != i]
    cats_tr = sorted(set(dd['cat'] for dd in train))
    cidx_tr = {c: j for j, c in enumerate(cats_tr)}
    nct = len(cats_tr)
    n_feat = nct + 2 + len(MAT_VARS) + 1
    X_tr = np.zeros((len(train), n_feat))
    y_tr = np.zeros(len(train))
    for j, dd in enumerate(train):
        X_tr[j, cidx_tr[dd['cat']]] = a_opt
        X_tr[j, nct] = math.log(dd['G'])
        X_tr[j, nct + 1] = math.log(dd['tD'])
        for k, v in enumerate(MAT_VARS):
            X_tr[j, nct + 2 + k] = math.log(dd[v]) if dd[v] > 0 else 0
        X_tr[j, -1] = 1.0
        y_tr[j] = math.log(dd['k_eff'])
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    if data[i]['cat'] not in cidx_tr:
        continue
    x_test = np.zeros(n_feat)
    x_test[cidx_tr[data[i]['cat']]] = a_opt
    x_test[nct] = math.log(data[i]['G'])
    x_test[nct + 1] = math.log(data[i]['tD'])
    for k, v in enumerate(MAT_VARS):
        x_test[nct + 2 + k] = math.log(data[i][v]) if data[i][v] > 0 else 0
    x_test[-1] = 1.0
    k_eff_pred = math.exp(x_test @ coef)
    tc_pred = math.sqrt(8 * data[i]['dd0']**2 * k_eff_pred * data[i]['tD'] / (9 * LN2))
    err2.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
err2 = np.array(err2)
print(f"LOOCV: 中位{np.median(err2)*100:.0f}%, 2倍内{np.mean(err2<=1)*100:.0f}%, 5倍内{np.mean(err2<=4)*100:.0f}%")

# ============================================================
# 方法3: 非线性特征 (1/θ_D, ln²θ_D等)
# ============================================================
print(f"\n{'='*80}")
print("方法3: γ_cat + G + θ_D + 1/θ_D + ln²(θ_D) + 材料参数")
print("="*80)

def build_X3(a_val):
    n_feat = n_cats + 2 + 2 + len(MAT_VARS) + 1  # γ, G, θ_D, 1/θ_D, ln²θ_D, mat, const
    X = np.zeros((n_data, n_feat))
    for i, d in enumerate(data):
        X[i, cat_idx[d['cat']]] = a_val
        X[i, n_cats] = math.log(d['G'])
        X[i, n_cats + 1] = math.log(d['tD'])
        X[i, n_cats + 2] = 1.0 / d['tD']
        X[i, n_cats + 3] = math.log(d['tD'])**2
        for j, v in enumerate(MAT_VARS):
            X[i, n_cats + 4 + j] = math.log(d[v]) if d[v] > 0 else 0
        X[i, -1] = 1.0
    return X

X3 = build_X3(a_opt)
coef3, _, _, _ = np.linalg.lstsq(X3, y, rcond=None)
r2_3 = 1 - np.sum((y - X3 @ coef3)**2) / np.sum((y - np.mean(y))**2)
print(f"R² = {r2_3:.4f}")

# LOOCV
err3 = []
for i in range(n_data):
    train = [data[j] for j in range(n_data) if j != i]
    cats_tr = sorted(set(dd['cat'] for dd in train))
    cidx_tr = {c: j for j, c in enumerate(cats_tr)}
    nct = len(cats_tr)
    n_feat = nct + 2 + 2 + len(MAT_VARS) + 1
    X_tr = np.zeros((len(train), n_feat))
    y_tr = np.zeros(len(train))
    for j, dd in enumerate(train):
        X_tr[j, cidx_tr[dd['cat']]] = a_opt
        X_tr[j, nct] = math.log(dd['G'])
        X_tr[j, nct + 1] = math.log(dd['tD'])
        X_tr[j, nct + 2] = 1.0 / dd['tD']
        X_tr[j, nct + 3] = math.log(dd['tD'])**2
        for k, v in enumerate(MAT_VARS):
            X_tr[j, nct + 4 + k] = math.log(dd[v]) if dd[v] > 0 else 0
        X_tr[j, -1] = 1.0
        y_tr[j] = math.log(dd['k_eff'])
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    if data[i]['cat'] not in cidx_tr:
        continue
    x_test = np.zeros(n_feat)
    x_test[cidx_tr[data[i]['cat']]] = a_opt
    x_test[nct] = math.log(data[i]['G'])
    x_test[nct + 1] = math.log(data[i]['tD'])
    x_test[nct + 2] = 1.0 / data[i]['tD']
    x_test[nct + 3] = math.log(data[i]['tD'])**2
    for k, v in enumerate(MAT_VARS):
        x_test[nct + 4 + k] = math.log(data[i][v]) if data[i][v] > 0 else 0
    x_test[-1] = 1.0
    k_eff_pred = math.exp(x_test @ coef)
    tc_pred = math.sqrt(8 * data[i]['dd0']**2 * k_eff_pred * data[i]['tD'] / (9 * LN2))
    err3.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
err3 = np.array(err3)
print(f"LOOCV: 中位{np.median(err3)*100:.0f}%, 2倍内{np.mean(err3<=1)*100:.0f}%, 5倍内{np.mean(err3<=4)*100:.0f}%")

# ============================================================
# 方法4: 纯第一性 (不用类别, 非线性材料参数)
# ============================================================
print(f"\n{'='*80}")
print("方法4: 纯第一性 (不用类别, 非线性特征)")
print("="*80)

def build_X4():
    vars_log = ['G', 'tD', 'M', 'Z', 'V', 'n_atoms', 'B']
    n_feat = len(vars_log) + 3 + 1  # log vars + 1/θ_D + ln²θ_D + θ_D² + const
    X = np.zeros((n_data, n_feat))
    for i, d in enumerate(data):
        for j, v in enumerate(vars_log):
            X[i, j] = math.log(d[v]) if d[v] > 0 else 0
        X[i, len(vars_log)] = 1.0 / d['tD']
        X[i, len(vars_log) + 1] = math.log(d['tD'])**2
        X[i, len(vars_log) + 2] = d['tD']**2
        X[i, -1] = 1.0
    return X

X4 = build_X4()
coef4, _, _, _ = np.linalg.lstsq(X4, y, rcond=None)
r2_4 = 1 - np.sum((y - X4 @ coef4)**2) / np.sum((y - np.mean(y))**2)
print(f"R² = {r2_4:.4f}")

# LOOCV
err4 = []
for i in range(n_data):
    train = [data[j] for j in range(n_data) if j != i]
    X_tr = build_X4()[:n_data-1]  # 不对，需要重新构建
    # 手动构建
    vars_log = ['G', 'tD', 'M', 'Z', 'V', 'n_atoms', 'B']
    n_feat = len(vars_log) + 3 + 1
    X_tr = np.zeros((len(train), n_feat))
    y_tr = np.zeros(len(train))
    for j, dd in enumerate(train):
        for k, v in enumerate(vars_log):
            X_tr[j, k] = math.log(dd[v]) if dd[v] > 0 else 0
        X_tr[j, len(vars_log)] = 1.0 / dd['tD']
        X_tr[j, len(vars_log) + 1] = math.log(dd['tD'])**2
        X_tr[j, len(vars_log) + 2] = dd['tD']**2
        X_tr[j, -1] = 1.0
        y_tr[j] = math.log(dd['k_eff'])
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    x_test = np.zeros(n_feat)
    for k, v in enumerate(vars_log):
        x_test[k] = math.log(data[i][v]) if data[i][v] > 0 else 0
    x_test[len(vars_log)] = 1.0 / data[i]['tD']
    x_test[len(vars_log) + 1] = math.log(data[i]['tD'])**2
    x_test[len(vars_log) + 2] = data[i]['tD']**2
    x_test[-1] = 1.0
    k_eff_pred = math.exp(x_test @ coef)
    tc_pred = math.sqrt(8 * data[i]['dd0']**2 * k_eff_pred * data[i]['tD'] / (9 * LN2))
    err4.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
err4 = np.array(err4)
print(f"LOOCV: 中位{np.median(err4)*100:.0f}%, 2倍内{np.mean(err4<=1)*100:.0f}%, 5倍内{np.mean(err4<=4)*100:.0f}%")

# ============================================================
# 总结
# ============================================================
print(f"\n{'='*80}")
print("全方法对比")
print("="*80)
print(f"{'方法':<45} {'R²':>6} {'中位%':>6} {'2倍%':>6} {'5倍%':>6}")
print("-"*70)
methods = [
    ("γ_cat + G + θ_D (优化a)", r2_1, err1),
    ("γ_cat + G + θ_D + 材料参数", r2_2, err2),
    ("γ_cat + 非线性(G,θ_D,...)", r2_3, err3),
    ("纯第一性(非线性, 无类别)", r2_4, err4),
]
for name, r2, err in methods:
    print(f"{name:<45} {r2:>6.3f} {np.median(err)*100:>6.0f} {np.mean(err<=1)*100:>6.0f} {np.mean(err<=4)*100:>6.0f}")

best = min(methods, key=lambda x: np.median(x[2]))
print(f"\n最佳: {best[0]}")
print(f"  R²={best[1]:.3f}, 中位{np.median(best[2])*100:.0f}%, 2倍内{np.mean(best[2]<=1)*100:.0f}%, 5倍内{np.mean(best[2]<=4)*100:.0f}%")
