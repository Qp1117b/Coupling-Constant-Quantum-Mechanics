"""
第一性Tc预测链条精确化
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework'); from atom_db import ATOM_DB, atom_db

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
