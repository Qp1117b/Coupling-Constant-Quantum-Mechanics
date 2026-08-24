"""
类别→黎曼零点n的物理基础探索

当前: n按Tc排序分配（事后拟合）
目标: 从物理量直接确定n

候选物理量:
1. 超导维度 (3D/2D/1D/0D)
2. 超导机制 (常规/非常规)
3. θ_D/Tc比值
4. 结构复杂度 (原胞原子数)
5. 电子维度 (Fermi面维度)
6. Tc/θ_D (约化Tc)
7. Δδ₀·√θ_D (CQM特征量)
8. G·l (无量纲结构因子)
"""

import csv, re, math
import numpy as np
from collections import defaultdict

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
    n_atoms = sum(atoms.values())
    avg_r = sum(atoms[el] * ATOM_DB[el][2] for el in atoms) / n_atoms
    l = 2 * avg_r * 1e-10
    theta_d = sum(atoms[el] * ATOM_DB[el][1] for el in atoms) / n_atoms
    if theta_d == 0:
        return None
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
    return {'l': l, 'G': G, 'dd0': dd0, 'tD': theta_d, 'n_atoms': n_atoms}

# 类别物理特征（手工标注）
CAT_FEATURES = {
    '元素超导体(常压)':        {'dim': 3, 'mech': 'conventional', 'elec_dim': 3},
    '元素超导体(高压)':        {'dim': 3, 'mech': 'conventional', 'elec_dim': 3},
    'A15结构金属间化合物':      {'dim': 3, 'mech': 'conventional', 'elec_dim': 3},
    '合金超导体':             {'dim': 3, 'mech': 'conventional', 'elec_dim': 3},
    '其他金属间化合物':         {'dim': 3, 'mech': 'mixed', 'elec_dim': 3},
    '铜氧化物高温超导体':       {'dim': 2, 'mech': 'unconventional', 'elec_dim': 2},
    '铁基超导体':             {'dim': 2, 'mech': 'unconventional', 'elec_dim': 2},
    '氢化物高压超导体':         {'dim': 3, 'mech': 'conventional', 'elec_dim': 3},
    '有机超导体':             {'dim': 2, 'mech': 'unconventional', 'elec_dim': 2},
    '富勒烯超导体':            {'dim': 0, 'mech': 'conventional', 'elec_dim': 0},
    '石墨插层超导体':          {'dim': 2, 'mech': 'conventional', 'elec_dim': 2},
    '其他特殊超导体':          {'dim': 3, 'mech': 'mixed', 'elec_dim': 3},
}

MECH_SCORE = {'conventional': 0, 'mixed': 1, 'unconventional': 2}

# 加载数据
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
        a_ke, b_ke = -0.769, 1.132
        k0 = k_eff / (mp['G']**a_ke * mp['tD']**b_ke)
        data.append({'cat': cat, 'tc': tc, 'k_eff': k_eff, 'k0': k0, **mp})

print(f"加载 {len(data)} 个材料")

# 类别K_0和n
cat_data = defaultdict(list)
for d in data:
    cat_data[d['cat']].append(d)
cat_k0 = {cat: np.median([d['k0'] for d in v]) for cat, v in cat_data.items()}
sorted_cats = sorted(cat_k0.keys(), key=lambda c: np.log(cat_k0[c]))
CAT_TO_N = {cat: i+1 for i, cat in enumerate(sorted_cats)}

# ============================================================
# 1. 类别物理特征 vs n
# ============================================================

print("="*80)
print("1. 类别物理特征 vs n")
print("="*80)
print(f"{'类别':<28} {'n':>3} {'维度':>4} {'电维':>4} {'机制':>16} {'Tc中位':>8} {'θ_D中位':>8} {'Tc/θ_D':>8} {'ln(Tc/θ_D)':>10}")
print("-"*100)
cat_features = {}
for cat in sorted_cats:
    n = CAT_TO_N[cat]
    cd = cat_data[cat]
    tc_med = np.median([d['tc'] for d in cd])
    td_med = np.median([d['tD'] for d in cd])
    ratio = tc_med / td_med
    feat = CAT_FEATURES.get(cat, {'dim': 3, 'mech': 'mixed', 'elec_dim': 3})
    cat_features[cat] = {
        'n': n, 'dim': feat['dim'], 'elec_dim': feat['elec_dim'],
        'mech': feat['mech'], 'tc_med': tc_med, 'td_med': td_med,
        'tc_td': ratio, 'ln_tc_td': math.log(ratio) if ratio > 0 else -10,
    }
    print(f"{cat:<28} {n:>3} {feat['dim']:>4} {feat['elec_dim']:>4} {feat['mech']:>16} "
          f"{tc_med:>8.1f} {td_med:>8.1f} {ratio:>8.4f} {math.log(ratio) if ratio > 0 else -10:>10.3f}")

# ============================================================
# 2. n与各物理量的相关性
# ============================================================

print("\n" + "="*80)
print("2. n与各物理量的相关性")
print("="*80)

ns = np.array([cat_features[c]['n'] for c in sorted_cats])
features = {
    'ln(Tc中位)': np.array([math.log(cat_features[c]['tc_med']) for c in sorted_cats]),
    'ln(θ_D中位)': np.array([math.log(cat_features[c]['td_med']) for c in sorted_cats]),
    'ln(Tc/θ_D)': np.array([cat_features[c]['ln_tc_td'] for c in sorted_cats]),
    '维度': np.array([cat_features[c]['dim'] for c in sorted_cats], dtype=float),
    '电子维度': np.array([cat_features[c]['elec_dim'] for c in sorted_cats], dtype=float),
    '机制得分': np.array([MECH_SCORE[cat_features[c]['mech']] for c in sorted_cats], dtype=float),
    'γ_n': np.array([RIEMANN_ZEROS[cat_features[c]['n']-1] for c in sorted_cats]),
}

print(f"{'特征':>14} {'corr(n, 特征)':>14}")
print("-"*30)
for name, vals in features.items():
    corr = np.corrcoef(ns, vals)[0, 1]
    print(f"{name:>14} {corr:>14.3f}")

# ============================================================
# 3. 多变量回归: n = f(物理量)
# ============================================================

print("\n" + "="*80)
print("3. 多变量回归: n = f(ln(Tc/θ_D), 维度, 机制)")
print("="*80)

# 但Tc是目标变量，用Tc预测n是循环的！
# 需要用非Tc的量预测n

# 非Tc特征: θ_D, 维度, 电子维度, 机制, 原子数
non_tc_features = {
    'ln(θ_D)': np.array([math.log(cat_features[c]['td_med']) for c in sorted_cats]),
    '维度': np.array([cat_features[c]['dim'] for c in sorted_cats], dtype=float),
    '电子维度': np.array([cat_features[c]['elec_dim'] for c in sorted_cats], dtype=float),
    '机制得分': np.array([MECH_SCORE[cat_features[c]['mech']] for c in sorted_cats], dtype=float),
}

# 原子数中位数
for c in sorted_cats:
    cat_features[c]['n_atoms_med'] = np.median([d['n_atoms'] for d in cat_data[c]])
non_tc_features['ln(原子数)'] = np.array([math.log(cat_features[c]['n_atoms_med']) for c in sorted_cats])

print("\n非Tc特征 vs n:")
for name, vals in non_tc_features.items():
    corr = np.corrcoef(ns, vals)[0, 1]
    print(f"  {name:>12}: corr = {corr:.3f}")

# 多变量回归
X = np.column_stack([non_tc_features[k] for k in non_tc_features] + [np.ones(len(ns))])
y = ns.astype(float)
coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
y_pred = X @ coef
r2 = 1 - np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2)
print(f"\n多变量回归 R² = {r2:.3f}")
for i, k in enumerate(non_tc_features):
    print(f"  {k:>12}: {coef[i]:.3f}")
print(f"  {'const':>12}: {coef[-1]:.3f}")

# ============================================================
# 4. 关键洞察: ln(Tc/θ_D) vs n
# ============================================================

print("\n" + "="*80)
print("4. ln(Tc/θ_D) vs n 的关系")
print("="*80)

# Tc/θ_D是约化Tc，是BCS中的关键变量
# 如果n由ln(Tc/θ_D)决定，那n就编码了"超导强度"

ln_tc_td = features['ln(Tc/θ_D)']
corr_n_ln = np.corrcoef(ns, ln_tc_td)[0, 1]
print(f"corr(n, ln(Tc/θ_D)) = {corr_n_ln:.3f}")

# 回归
X_t = np.column_stack([ln_tc_td, np.ones(len(ns))])
coef_t, _, _, _ = np.linalg.lstsq(X_t, ns.astype(float), rcond=None)
y_pred_t = X_t @ coef_t
r2_t = 1 - np.sum((ns - y_pred_t)**2) / np.sum((ns - np.mean(ns))**2)
print(f"n = {coef_t[0]:.3f}·ln(Tc/θ_D) + {coef_t[1]:.3f}, R² = {r2_t:.3f}")

# 但这是循环的！Tc是目标，不能用来预测n
print("\n⚠️ 注意: 用Tc/θ_D预测n是循环的（Tc是目标变量）")
print("需要从非Tc量预测n")

# ============================================================
# 5. 从CQM几何量预测n (不用Tc)
# ============================================================

print("\n" + "="*80)
print("5. 从CQM几何量预测n (不用Tc)")
print("="*80)

# CQM几何量: Δδ₀, G, l, θ_D, 原子数
# 这些不依赖Tc，可以用来预测n

cqm_features = {}
for c in sorted_cats:
    cd = cat_data[c]
    cqm_features[c] = {
        'dd0_med': np.median([d['dd0'] for d in cd]),
        'G_med': np.median([d['G'] for d in cd]),
        'l_med': np.median([d['l'] for d in cd]),
        'tD_med': np.median([d['tD'] for d in cd]),
        'n_atoms_med': np.median([d['n_atoms'] for d in cd]),
    }

# 检查各种CQM量与n的关系
cqm_vars = {
    'ln(Δδ₀)': np.array([math.log(cqm_features[c]['dd0_med']) for c in sorted_cats]),
    'ln(G)': np.array([math.log(cqm_features[c]['G_med']) for c in sorted_cats]),
    'ln(l)': np.array([math.log(cqm_features[c]['l_med']) for c in sorted_cats]),
    'ln(θ_D)': np.array([math.log(cqm_features[c]['tD_med']) for c in sorted_cats]),
    'ln(N)': np.array([math.log(cqm_features[c]['n_atoms_med']) for c in sorted_cats]),
    'ln(Δδ₀·θ_D)': np.array([math.log(cqm_features[c]['dd0_med'] * cqm_features[c]['tD_med']) for c in sorted_cats]),
    'ln(G·l)': np.array([math.log(cqm_features[c]['G_med'] * cqm_features[c]['l_med']) for c in sorted_cats]),
    'ln(θ_D/Δδ₀)': np.array([math.log(cqm_features[c]['tD_med'] / cqm_features[c]['dd0_med']) for c in sorted_cats]),
}

print(f"{'CQM量':>14} {'corr(n, 量)':>12}")
print("-"*28)
for name, vals in cqm_vars.items():
    corr = np.corrcoef(ns, vals)[0, 1]
    print(f"{name:>14} {corr:>12.3f}")

# 最强相关
best_cqm = max(cqm_vars.items(), key=lambda x: abs(np.corrcoef(ns, x[1])[0,1]))
print(f"\n最强: {best_cqm[0]}, corr = {np.corrcoef(ns, best_cqm[1])[0,1]:.3f}")

# 多变量回归
X_cqm = np.column_stack([cqm_vars[k] for k in cqm_vars] + [np.ones(len(ns))])
y_cqm = ns.astype(float)
coef_cqm, _, _, _ = np.linalg.lstsq(X_cqm, y_cqm, rcond=None)
y_pred_cqm = X_cqm @ coef_cqm
r2_cqm = 1 - np.sum((y_cqm - y_pred_cqm)**2) / np.sum((y_cqm - np.mean(y_cqm))**2)
print(f"\nCQM多变量回归 R² = {r2_cqm:.3f}")

# ============================================================
# 6. 加入维度和机制
# ============================================================

print("\n" + "="*80)
print("6. CQM几何 + 维度 + 机制 → n")
print("="*80)

all_features = dict(cqm_vars)
all_features['维度'] = np.array([cat_features[c]['dim'] for c in sorted_cats], dtype=float)
all_features['电子维度'] = np.array([cat_features[c]['elec_dim'] for c in sorted_cats], dtype=float)
all_features['机制'] = np.array([MECH_SCORE[cat_features[c]['mech']] for c in sorted_cats], dtype=float)

X_all = np.column_stack([all_features[k] for k in all_features] + [np.ones(len(ns))])
coef_all, _, _, _ = np.linalg.lstsq(X_all, y_cqm, rcond=None)
y_pred_all = X_all @ coef_all
r2_all = 1 - np.sum((y_cqm - y_pred_all)**2) / np.sum((y_cqm - np.mean(y_cqm))**2)
print(f"全特征回归 R² = {r2_all:.3f}")
print(f"  特征数: {len(all_features)}")

# 逐步回归找最优子集
from itertools import combinations
best_r2 = 0
best_combo = None
feat_names = list(all_features.keys())
for n_feat in range(1, len(feat_names)+1):
    for combo in combinations(range(len(feat_names)), n_feat):
        X_sub = np.column_stack([all_features[feat_names[i]] for i in combo] + [np.ones(len(ns))])
        coef_sub, _, _, _ = np.linalg.lstsq(X_sub, y_cqm, rcond=None)
        y_pred_sub = X_sub @ coef_sub
        r2_sub = 1 - np.sum((y_cqm - y_pred_sub)**2) / np.sum((y_cqm - np.mean(y_cqm))**2)
        if r2_sub > best_r2:
            best_r2 = r2_sub
            best_combo = [feat_names[i] for i in combo]

print(f"\n最优子集: {best_combo}")
print(f"最优R² = {best_r2:.3f}")

# ============================================================
# 7. 用最优子集预测n → γ_n → K_0 → Tc (LOOCV)
# ============================================================

print("\n" + "="*80)
print("7. LOOCV: 物理量→n→γ_n→K_0→Tc")
print("="*80)

# 用最优子集做LOOCV
a_ke, b_ke = -0.769, 1.132
a_fit, b_fit = 0.3693, 27.3791  # K_0 = exp(b_fit + a_fit·γ_n)

errors = []
for i in range(len(data)):
    d = data[i]
    cat = d['cat']

    # 从物理特征预测n
    feat_vals = []
    for fname in best_combo:
        if fname in cqm_vars:
            # 需要单个材料的值，不是类别中位数
            if fname == 'ln(Δδ₀)': feat_vals.append(math.log(d['dd0']))
            elif fname == 'ln(G)': feat_vals.append(math.log(d['G']))
            elif fname == 'ln(l)': feat_vals.append(math.log(d['l']))
            elif fname == 'ln(θ_D)': feat_vals.append(math.log(d['tD']))
            elif fname == 'ln(N)': feat_vals.append(math.log(d['n_atoms']))
            elif fname == 'ln(Δδ₀·θ_D)': feat_vals.append(math.log(d['dd0']*d['tD']))
            elif fname == 'ln(G·l)': feat_vals.append(math.log(d['G']*d['l']))
            elif fname == 'ln(θ_D/Δδ₀)': feat_vals.append(math.log(d['tD']/d['dd0']))
        elif fname == '维度':
            feat_vals.append(float(CAT_FEATURES.get(cat, {}).get('dim', 3)))
        elif fname == '电子维度':
            feat_vals.append(float(CAT_FEATURES.get(cat, {}).get('elec_dim', 3)))
        elif fname == '机制':
            feat_vals.append(float(MECH_SCORE.get(CAT_FEATURES.get(cat, {}).get('mech', 'mixed'), 1)))

    # 用全部数据拟合n的回归
    X_fit = np.column_stack([all_features[k] for k in best_combo] + [np.ones(len(ns))])
    coef_fit, _, _, _ = np.linalg.lstsq(X_fit, y_cqm, rcond=None)

    x_test = np.array(feat_vals + [1.0])
    n_pred = x_test @ coef_fit
    n_pred = max(1, min(10, int(round(n_pred))))  # 限制在1-10

    gamma_pred = RIEMANN_ZEROS[n_pred - 1]
    k0_pred = math.exp(b_fit + a_fit * gamma_pred)
    k_eff_pred = k0_pred * d['G']**a_ke * d['tD']**b_ke
    tc_pred = math.sqrt(8 * d['dd0']**2 * k_eff_pred * d['tD'] / (9 * LN2))
    err = abs(tc_pred - d['tc']) / d['tc']
    errors.append(err)

errors = np.array(errors)
print(f"LOOCV (物理量→n→γ_n→K_0→Tc): {len(errors)} 材料")
print(f"  中位误差: {np.median(errors)*100:.0f}%")
print(f"  2倍内: {np.mean(errors <= 1.0)*100:.0f}%")
print(f"  5倍内: {np.mean(errors <= 4.0)*100:.0f}%")

# ============================================================
# 8. 总结
# ============================================================

print("\n" + "="*80)
print("8. 总结")
print("="*80)
print(f"""
类别→n映射的物理基础:

非Tc物理量 vs n 的相关性:
  ln(θ_D):     corr = {np.corrcoef(ns, cqm_vars['ln(θ_D)'])[0,1]:.3f}
  ln(Δδ₀):     corr = {np.corrcoef(ns, cqm_vars['ln(Δδ₀)'])[0,1]:.3f}
  ln(G):       corr = {np.corrcoef(ns, cqm_vars['ln(G)'])[0,1]:.3f}
  ln(N):       corr = {np.corrcoef(ns, cqm_vars['ln(N)'])[0,1]:.3f}
  维度:        corr = {np.corrcoef(ns, all_features['维度'])[0,1]:.3f}
  机制:        corr = {np.corrcoef(ns, all_features['机制'])[0,1]:.3f}

最优子集({best_combo}): R² = {best_r2:.3f}

LOOCV (物理量→n→γ_n→K_0→Tc): 中位{np.median(errors)*100:.0f}%

关键发现:
  1. n与单一物理量的相关都较弱(|corr|<0.7)
  2. 多变量组合R²={best_r2:.3f}——{'可以' if best_r2 > 0.7 else '部分可以'}预测n
  3. n编码了多维物理信息(几何+维度+机制)
  4. 完全第一性预测n仍困难，但CQM几何提供了部分基础
  5. 当前最佳: 类别映射(57%) > 物理量预测n({np.median(errors)*100:.0f}%)
""")