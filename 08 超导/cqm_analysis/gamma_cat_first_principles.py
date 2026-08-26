"""
从CQM几何直接确定γ_cat — 核心剩余问题 (修正版)

关键澄清: tc_precision_optimization.py的方法1是one-hot类别模型(每类别自由系数),
不是γ_cat线性约束模型。本脚本系统对比:
1. one-hot类别模型 (基线, 45%)
2. γ_cat线性约束模型 (用黎曼零点约束类别关系)
3. 从几何参数直接预测γ_cat → Tc (纯第一性)
4. 从几何参数直接预测Tc (端到端纯第一性)
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework'); from atom_db import ATOM_DB, atom_db

import csv, re, math
import numpy as np
from scipy.optimize import minimize
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import LeaveOneOut

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
BETA = 8 * math.pi + 1
C2 = 2.0 / 3.0
LN2 = math.log(2)
C = math.sqrt(C2)

RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832]


CAT_TO_N = {
    '石墨插层超导体': 1, '有机超导体': 3, 'A15结构金属间化合物': 7,
    '铁基超导体': 8, '铜氧化物高温超导体': 9, '氢化物高压超导体': 10,
    '元素超导体(常压)': 5, '元素超导体(高压)': 6, '其他金属间化合物': 4,
    '其他特殊超导体': 5, '合金超导体': 4, '富勒烯超导体': 3,
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
        n_cat = CAT_TO_N.get(cat, 5)
        gamma_cat = RIEMANN_ZEROS[n_cat - 1]
        data.append({'cat': cat, 'tc': tc, 'k_eff': k_eff,
                     'gamma_cat': gamma_cat, 'n_cat': n_cat, **mp})

n_data = len(data)
categories = sorted(set(d['cat'] for d in data))
cat_idx = {c: i for i, c in enumerate(categories)}
n_cats = len(categories)
y_lnk = np.array([math.log(d['k_eff']) for d in data])
y_lntc = np.array([math.log(d['tc']) for d in data])
print(f"加载 {n_data} 个材料, {n_cats} 个类别")

def get_feats(d):
    return np.array([
        math.log(d['G']), math.log(d['tD']), math.log(d['dd0']),
        math.log(d['M']), math.log(d['Z']) if d['Z'] > 0 else 0,
        math.log(d['V']), math.log(d['n_atoms']),
        math.log(d['B']) if d['B'] > 0 else 0,
        1.0/d['tD'], math.log(d['tD'])**2,
        math.log(d['tD']/d['dd0']) if d['dd0'] > 0 else 0,
    ])

X_geom = np.array([get_feats(d) for d in data])
y_gamma = np.array([d['gamma_cat'] for d in data])
FEAT_NAMES = ['ln(G)', 'ln(θ_D)', 'ln(Δδ₀)', 'ln(M)', 'ln(Z)', 'ln(V)', 'ln(N)', 'ln(B)',
              '1/θ_D', 'ln²(θ_D)', 'ln(θ_D/Δδ₀)']

def calc_tc_from_lnk(ln_k, d):
    k_eff = math.exp(ln_k)
    return math.sqrt(8 * d['dd0']**2 * k_eff * d['tD'] / (9 * LN2))

def loocv_err(predict_func):
    errs = []
    for i in range(n_data):
        tc_pred, d = predict_func(i)
        errs.append(abs(tc_pred - d['tc']) / d['tc'])
    return np.array(errs)

# ============================================================
# 方法1: one-hot类别模型 (基线, 复现45%)
# ============================================================
print("="*80)
print("方法1: one-hot类别模型 ln(K_eff) = Σβ_cat·I(cat) + p·ln(G) + q·ln(θ_D) + b")
print("="*80)

def build_onehot(data_subset, cats_subset, cidx_subset):
    n = len(data_subset)
    nct = len(cats_subset)
    X = np.zeros((n, nct + 3))
    for j, d in enumerate(data_subset):
        X[j, cidx_subset[d['cat']]] = 1.0
        X[j, nct] = math.log(d['G'])
        X[j, nct + 1] = math.log(d['tD'])
        X[j, nct + 2] = 1.0
    return X

err1 = []
for i in range(n_data):
    train = [data[j] for j in range(n_data) if j != i]
    cats_tr = sorted(set(dd['cat'] for dd in train))
    cidx_tr = {c: j for j, c in enumerate(cats_tr)}
    nct = len(cats_tr)
    if data[i]['cat'] not in cidx_tr:
        err1.append(0)
        continue
    X_tr = build_onehot(train, cats_tr, cidx_tr)
    y_tr = np.array([math.log(dd['k_eff']) for dd in train])
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    x_test = np.zeros(nct + 3)
    x_test[cidx_tr[data[i]['cat']]] = 1.0
    x_test[nct] = math.log(data[i]['G'])
    x_test[nct + 1] = math.log(data[i]['tD'])
    x_test[nct + 2] = 1.0
    tc_pred = calc_tc_from_lnk(x_test @ coef, data[i])
    err1.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
err1 = np.array(err1)
print(f"LOOCV: 中位{np.median(err1)*100:.0f}%, 2倍内{np.mean(err1<=1)*100:.0f}%, 5倍内{np.mean(err1<=4)*100:.0f}%")

# ============================================================
# 方法2: γ_cat线性约束模型 ln(K_eff) = a·γ_cat + p·ln(G) + q·ln(θ_D) + b
# ============================================================
print(f"\n{'='*80}")
print("方法2: γ_cat线性约束 ln(K_eff) = a·γ_cat + p·ln(G) + q·ln(θ_D) + b")
print("="*80)

def build_gamma(data_subset):
    X = np.zeros((len(data_subset), 4))
    for j, d in enumerate(data_subset):
        X[j, 0] = d['gamma_cat']
        X[j, 1] = math.log(d['G'])
        X[j, 2] = math.log(d['tD'])
        X[j, 3] = 1.0
    return X

X_gamma = build_gamma(data)
coef2, _, _, _ = np.linalg.lstsq(X_gamma, y_lnk, rcond=None)
r2_2 = 1 - np.sum((y_lnk - X_gamma @ coef2)**2) / np.sum((y_lnk - np.mean(y_lnk))**2)
print(f"全数据: a={coef2[0]:.4f}, p={coef2[1]:.4f}, q={coef2[2]:.4f}, b={coef2[3]:.4f}, R²={r2_2:.4f}")

err2 = []
for i in range(n_data):
    train = [data[j] for j in range(n_data) if j != i]
    X_tr = build_gamma(train)
    y_tr = np.array([math.log(dd['k_eff']) for dd in train])
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    x_test = np.array([data[i]['gamma_cat'], math.log(data[i]['G']), math.log(data[i]['tD']), 1.0])
    tc_pred = calc_tc_from_lnk(x_test @ coef, data[i])
    err2.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
err2 = np.array(err2)
print(f"LOOCV: 中位{np.median(err2)*100:.0f}%, 2倍内{np.mean(err2<=1)*100:.0f}%, 5倍内{np.mean(err2<=4)*100:.0f}%")

# ============================================================
# 方法3: 从几何参数线性回归γ_cat → 连续γ → Tc
# ============================================================
print(f"\n{'='*80}")
print("方法3: 线性回归 γ_cat = f(几何) → 连续γ → Tc (纯第一性)")
print("="*80)

coef_g, _, _, _ = np.linalg.lstsq(X_geom, y_gamma, rcond=None)
r2_g = 1 - np.sum((y_gamma - X_geom @ coef_g)**2) / np.sum((y_gamma - np.mean(y_gamma))**2)
print(f"γ_cat回归 R² = {r2_g:.4f}")

# 用方法2的a,p,q,b
a2, p2, q2, b2 = coef2
err3 = []
for i in range(n_data):
    train = [j for j in range(n_data) if j != i]
    X_tr = X_geom[train]
    y_tr = y_gamma[train]
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    gamma_pred = get_feats(data[i]) @ coef
    ln_k = a2 * gamma_pred + p2 * math.log(data[i]['G']) + q2 * math.log(data[i]['tD']) + b2
    tc_pred = calc_tc_from_lnk(ln_k, data[i])
    err3.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
err3 = np.array(err3)
print(f"LOOCV: 中位{np.median(err3)*100:.0f}%, 2倍内{np.mean(err3<=1)*100:.0f}%, 5倍内{np.mean(err3<=4)*100:.0f}%")

# ============================================================
# 方法4: GBR预测γ_cat → 连续γ → Tc
# ============================================================
print(f"\n{'='*80}")
print("方法4: GBR预测γ_cat → 连续γ → Tc (纯第一性)")
print("="*80)

loo = LeaveOneOut()
err4 = []
for train_idx, test_idx in loo.split(X_geom):
    gbr = GradientBoostingRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42)
    gbr.fit(X_geom[train_idx], y_gamma[train_idx])
    gamma_pred = gbr.predict(X_geom[test_idx])[0]
    d = data[test_idx[0]]
    ln_k = a2 * gamma_pred + p2 * math.log(d['G']) + q2 * math.log(d['tD']) + b2
    tc_pred = calc_tc_from_lnk(ln_k, d)
    err4.append(abs(tc_pred - d['tc']) / d['tc'])
err4 = np.array(err4)
print(f"LOOCV: 中位{np.median(err4)*100:.0f}%, 2倍内{np.mean(err4<=1)*100:.0f}%, 5倍内{np.mean(err4<=4)*100:.0f}%")

# ============================================================
# 方法5: GBR直接预测ln(K_eff) (纯第一性, 跳过γ_cat)
# ============================================================
print(f"\n{'='*80}")
print("方法5: GBR直接预测ln(K_eff) (纯第一性)")
print("="*80)

err5 = []
for train_idx, test_idx in loo.split(X_geom):
    gbr = GradientBoostingRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42)
    gbr.fit(X_geom[train_idx], y_lnk[train_idx])
    ln_k_pred = gbr.predict(X_geom[test_idx])[0]
    d = data[test_idx[0]]
    tc_pred = calc_tc_from_lnk(ln_k_pred, d)
    err5.append(abs(tc_pred - d['tc']) / d['tc'])
err5 = np.array(err5)
print(f"LOOCV: 中位{np.median(err5)*100:.0f}%, 2倍内{np.mean(err5<=1)*100:.0f}%, 5倍内{np.mean(err5<=4)*100:.0f}%")

# ============================================================
# 方法6: GBR端到端预测ln(Tc) (纯第一性)
# ============================================================
print(f"\n{'='*80}")
print("方法6: GBR端到端预测ln(Tc) (纯第一性)")
print("="*80)

err6 = []
for train_idx, test_idx in loo.split(X_geom):
    gbr = GradientBoostingRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42)
    gbr.fit(X_geom[train_idx], y_lntc[train_idx])
    ln_tc_pred = gbr.predict(X_geom[test_idx])[0]
    tc_pred = math.exp(ln_tc_pred)
    d = data[test_idx[0]]
    err6.append(abs(tc_pred - d['tc']) / d['tc'])
err6 = np.array(err6)
print(f"LOOCV: 中位{np.median(err6)*100:.0f}%, 2倍内{np.mean(err6<=1)*100:.0f}%, 5倍内{np.mean(err6<=4)*100:.0f}%")

# ============================================================
# 方法7: GBR端到端 + 类别特征 (半第一性)
# ============================================================
print(f"\n{'='*80}")
print("方法7: GBR端到端 + 类别one-hot (半第一性)")
print("="*80)

X_full = np.zeros((n_data, len(FEAT_NAMES) + n_cats))
for i, d in enumerate(data):
    X_full[i, :len(FEAT_NAMES)] = get_feats(d)
    X_full[i, len(FEAT_NAMES) + cat_idx[d['cat']]] = 1.0

err7 = []
for train_idx, test_idx in loo.split(X_full):
    gbr = GradientBoostingRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42)
    gbr.fit(X_full[train_idx], y_lntc[train_idx])
    ln_tc_pred = gbr.predict(X_full[test_idx])[0]
    tc_pred = math.exp(ln_tc_pred)
    d = data[test_idx[0]]
    err7.append(abs(tc_pred - d['tc']) / d['tc'])
err7 = np.array(err7)
print(f"LOOCV: 中位{np.median(err7)*100:.0f}%, 2倍内{np.mean(err7<=1)*100:.0f}%, 5倍内{np.mean(err7<=4)*100:.0f}%")

# ============================================================
# 总结
# ============================================================
print(f"\n{'='*80}")
print("全方法对比 — γ_cat第一性确定 vs 端到端")
print("="*80)
print(f"{'方法':<55} {'中位%':>6} {'2倍%':>6} {'5倍%':>6}")
print("-"*77)
methods = [
    ("1: one-hot类别模型 (基线)", err1),
    ("2: γ_cat线性约束模型", err2),
    ("3: 线性回归γ→连续γ→Tc [纯第一性]", err3),
    ("4: GBR回归γ→连续γ→Tc [纯第一性]", err4),
    ("5: GBR直接预测ln(K_eff) [纯第一性]", err5),
    ("6: GBR端到端预测ln(Tc) [纯第一性]", err6),
    ("7: GBR端到端+类别 [半第一性]", err7),
]
for name, err in methods:
    print(f"{name:<55} {np.median(err)*100:>6.0f} {np.mean(err<=1)*100:>6.0f} {np.mean(err<=4)*100:>6.0f}")

best = min(methods, key=lambda x: np.median(x[1]))
print(f"\n最佳: {best[0]}")
print(f"  中位{np.median(best[1])*100:.0f}%, 2倍内{np.mean(best[1]<=1)*100:.0f}%, 5倍内{np.mean(best[1]<=4)*100:.0f}%")

# 纯第一性最佳
pure = [(n, e) for n, e in methods if "纯第一性" in n]
best_pure = min(pure, key=lambda x: np.median(x[1]))
print(f"\n纯第一性最佳: {best_pure[0]}")
print(f"  中位{np.median(best_pure[1])*100:.0f}%, 2倍内{np.mean(best_pure[1]<=1)*100:.0f}%, 5倍内{np.mean(best_pure[1]<=4)*100:.0f}%")

# ============================================================
# γ_cat与几何参数的关系
# ============================================================
print(f"\n{'='*80}")
print("γ_cat与几何参数的相关性")
print("="*80)
for j, name in enumerate(FEAT_NAMES):
    corr = np.corrcoef(X_geom[:, j], y_gamma)[0, 1]
    print(f"  corr(γ_cat, {name:<15}) = {corr:+.3f}")

gbr_full = GradientBoostingRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42)
gbr_full.fit(X_geom, y_gamma)
r2_gbr = 1 - np.sum((y_gamma - gbr_full.predict(X_geom))**2) / np.sum((y_gamma - np.mean(y_gamma))**2)
print(f"\n多变量线性 R² = {r2_g:.4f}, GBR R² = {r2_gbr:.4f}")
print(f"\nGBR特征重要性:")
for name, imp in sorted(zip(FEAT_NAMES, gbr_full.feature_importances_), key=lambda x: -x[1]):
    print(f"  {name:<15}: {imp:.4f}")
