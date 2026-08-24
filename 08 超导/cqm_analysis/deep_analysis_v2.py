"""
深入分析v2: 重费米子n重映射 + 最优分类

发现: 重费米子Tc极低(0.05-0.5K), 但γ_n=32.94(n=5)预测高Tc
假设: 重费米子应该用低n值(γ_n小→低Tc), 而非高j值
策略: 按Tc层次重新映射n, 使γ_n与Tc正相关
"""

import csv, re, math
import numpy as np
from scipy.optimize import minimize

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
BETA = 8 * math.pi + 1
C2 = 2.0 / 3.0
LN2 = math.log(2)
C_GEO = math.sqrt(C2)

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

HEAVY_FERMION_ELEMENTS = {'Ce', 'Yb', 'U', 'Pr', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Lu', 'Nd', 'Np', 'Pu'}

GL1_CATS = {
    '元素超导体(常压)', '元素超导体(高压)', 'A15结构金属间化合物',
    '合金超导体', '其他金属间化合物', '氢化物高压超导体',
    '石墨插层超导体', '其他特殊超导体',
}
GL2_CATS = {
    '铜氧化物高温超导体', '铁基超导体', '有机超导体', '富勒烯超导体',
}

CAT_TO_N = {
    '石墨插层超导体': 1, '有机超导体': 3, 'A15结构金属间化合物': 7,
    '铁基超导体': 8, '铜氧化物高温超导体': 9, '氢化物高压超导体': 10,
    '元素超导体(常压)': 5, '元素超导体(高压)': 6, '其他金属间化合物': 4,
    '其他特殊超导体': 5, '合金超导体': 4, '富勒烯超导体': 3,
}
CAT_TO_J = {
    '铜氧化物高温超导体': 2, '铁基超导体': 1, '有机超导体': 1, '富勒烯超导体': 1,
}

def parse_formula(f):
    pairs = re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f)
    atoms = {}
    for el, cnt in pairs:
        if el in ATOM_DB:
            atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    return atoms

def calc_all_params(formula):
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
    has_f = any(el in HEAVY_FERMION_ELEMENTS for el in atoms)
    return {
        'formula': formula, 'M': total_m, 'Z': total_z, 'N': n_atoms,
        'l': l, 'theta_D': theta_d, 'V': V_cell,
        'G': G, 'dd0': dd0, 'B': B_est, 'has_f': has_f,
    }

data = []
with open("superconductors_deduplicated.csv", 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try:
            tc = float(row['临界温度 Tc (K)'])
        except:
            continue
        if tc <= 0:
            continue
        mp = calc_all_params(row['材料(化学式)'])
        if mp is None or mp['dd0'] == 0:
            continue
        cat = row['类别']
        gl = 1 if cat in GL1_CATS else (2 if cat in GL2_CATS else 1)
        j = CAT_TO_J.get(cat, 0)
        n_mode = CAT_TO_N.get(cat, 5)
        gamma_n = RIEMANN_ZEROS[n_mode - 1]
        casimir = j * (j + 1)
        k_eff = tc**2 * 9 * LN2 / (8 * mp['dd0']**2 * mp['theta_D'])
        data.append({**mp, 'cat': cat, 'tc': tc, 'k_eff': k_eff,
                     'gl': gl, 'j': j, 'casimir': casimir,
                     'gamma_n': gamma_n, 'n_mode': n_mode})

n_data = len(data)
y_lnk = np.array([math.log(d['k_eff']) for d in data])

# ============================================================
# 策略: 重费米子用n=1(γ_n=14.13), j=0; 其余不变
# ============================================================
print("="*80)
print("策略1: 重费米子n=1(γ_n=14.13), j=0")
print("="*80)

for d in data:
    if d['has_f'] and d['gl'] == 1:
        d['gamma_n_adj'] = RIEMANN_ZEROS[0]  # n=1
        d['j_adj'] = 0
        d['casimir_adj'] = 0
    else:
        d['gamma_n_adj'] = d['gamma_n']
        d['j_adj'] = d['j']
        d['casimir_adj'] = d['casimir']

def build_X1(lam):
    X = np.zeros((n_data, 7))
    for i, d in enumerate(data):
        gamma_eff = d['gamma_n_adj'] + lam * d['casimir_adj']
        X[i, 0] = gamma_eff
        X[i, 1] = math.log(d['G'])
        X[i, 2] = math.log(d['theta_D'])
        X[i, 3] = math.log(d['B'])
        X[i, 4] = math.log(d['N'])
        X[i, 5] = math.log(d['V'])
        X[i, 6] = 1.0
    return X

def obj1(lam):
    X = build_X1(lam[0])
    coef, _, _, _ = np.linalg.lstsq(X, y_lnk, rcond=None)
    return np.sum((y_lnk - X @ coef)**2)

res1 = minimize(obj1, x0=[0.234], method='Nelder-Mead', options={'maxiter': 10000})
lam1 = res1.x[0]
X1 = build_X1(lam1)
coef1, _, _, _ = np.linalg.lstsq(X1, y_lnk, rcond=None)
r2_1 = 1 - np.sum((y_lnk - X1 @ coef1)**2) / np.sum((y_lnk - np.mean(y_lnk))**2)
print(f"γ_eff = γ_n + {lam1:.4f}·j(j+1), R²={r2_1:.4f}")

err1 = []
for i in range(n_data):
    X_tr = np.delete(X1, i, axis=0)
    y_tr = np.delete(y_lnk, i)
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    ln_k = X1[i] @ coef
    tc_pred = math.sqrt(8 * data[i]['dd0']**2 * math.exp(ln_k) * data[i]['theta_D'] / (9 * LN2))
    err1.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
err1 = np.array(err1)

# 分层
is_hf = np.array([d['has_f'] and d['gl'] == 1 for d in data])
is_gl1 = np.array([not d['has_f'] and d['gl'] == 1 for d in data])
is_gl2 = np.array([d['gl'] == 2 for d in data])

print(f"全部: 中位{np.median(err1)*100:.0f}%, 2倍内{np.mean(err1<=1)*100:.0f}%, 5倍内{np.mean(err1<=4)*100:.0f}%")
print(f"GL(1)常规: 中位{np.median(err1[is_gl1])*100:.0f}%, 2倍内{np.mean(err1[is_gl1]<=1)*100:.0f}%, 5倍内{np.mean(err1[is_gl1]<=4)*100:.0f}%")
print(f"GL(2)非常规: 中位{np.median(err1[is_gl2])*100:.0f}%, 2倍内{np.mean(err1[is_gl2]<=1)*100:.0f}%, 5倍内{np.mean(err1[is_gl2]<=4)*100:.0f}%")
print(f"重费米子(n=1): 中位{np.median(err1[is_hf])*100:.0f}%, 2倍内{np.mean(err1[is_hf]<=1)*100:.0f}%, 5倍内{np.mean(err1[is_hf]<=4)*100:.0f}%")

# ============================================================
# 策略2: 从K_eff反推每个材料的最优γ_eff, 看分布
# ============================================================
print(f"\n{'='*80}")
print("策略2: 从K_eff反推最优γ_eff, 分析分布")
print("="*80)

# ln(K_0) = ln(K_eff) - p*ln(G) - q*ln(θ_D)
# γ_eff = (ln(K_0) - b) / a
# 用策略1的参数
a1 = coef1[0]
p1, q1 = coef1[1], coef1[2]
b1 = coef1[6]

for d in data:
    ln_k0 = math.log(d['k_eff']) - p1*math.log(d['G']) - q1*math.log(d['theta_D']) - coef1[3]*math.log(d['B']) - coef1[4]*math.log(d['N']) - coef1[5]*math.log(d['V'])
    d['gamma_eff_implicit'] = (ln_k0 - b1) / a1

print(f"各类别γ_eff_implicit分布:")
for cat in sorted(set(d['cat'] for d in data)):
    cat_data = [d for d in data if d['cat'] == cat]
    gammas = [d['gamma_eff_implicit'] for d in cat_data]
    j = cat_data[0]['j']
    print(f"  {cat:<30} j={j}, n={len(cat_data):>3}, γ_eff: 均值={np.mean(gammas):>7.2f}, 标准差={np.std(gammas):>6.2f}, 范围=[{min(gammas):>6.2f}, {max(gammas):>6.2f}]")

# 重费米子单独看
hf_data = [d for d in data if d['has_f'] and d['gl'] == 1]
if hf_data:
    gammas_hf = [d['gamma_eff_implicit'] for d in hf_data]
    print(f"\n  重费米子(含f电子): n={len(hf_data)}, γ_eff: 均值={np.mean(gammas_hf):.2f}, 标准差={np.std(gammas_hf):.2f}, 范围=[{min(gammas_hf):.2f}, {max(gammas_hf):.2f}]")
    print(f"    对应黎曼零点: γ={np.mean(gammas_hf):.2f} 介于γ_1=14.13和γ_2=21.02之间")

# ============================================================
# 策略3: 最优n映射 — 按γ_eff_implicit的中位数分配n
# ============================================================
print(f"\n{'='*80}")
print("策略3: 按γ_eff_implicit重新分配n")
print("="*80)

# 每个类别按γ_eff_implicit中位数排序，分配最近的黎曼零点
cat_gamma_med = {}
for cat in sorted(set(d['cat'] for d in data)):
    cat_data = [d for d in data if d['cat'] == cat]
    cat_gamma_med[cat] = np.median([d['gamma_eff_implicit'] for d in cat_data])

# 按γ_median排序
cats_sorted = sorted(cat_gamma_med.keys(), key=lambda c: cat_gamma_med[c])
print(f"类别按γ_eff中位数排序:")
for i, cat in enumerate(cats_sorted):
    n_best = min(range(1, 11), key=lambda n: abs(RIEMANN_ZEROS[n-1] - cat_gamma_med[cat]))
    print(f"  {i+1}. {cat:<30} γ_med={cat_gamma_med[cat]:>7.2f} → n={n_best} (γ_n={RIEMANN_ZEROS[n_best-1]:.2f})")

# 用新n映射
CAT_TO_N_NEW = {}
for cat in cats_sorted:
    n_best = min(range(1, 11), key=lambda n: abs(RIEMANN_ZEROS[n-1] - cat_gamma_med[cat]))
    CAT_TO_N_NEW[cat] = n_best

for d in data:
    n_new = CAT_TO_N_NEW.get(d['cat'], 5)
    d['gamma_n_new'] = RIEMANN_ZEROS[n_new - 1]
    d['n_new'] = n_new

def build_X3(lam):
    X = np.zeros((n_data, 7))
    for i, d in enumerate(data):
        gamma_eff = d['gamma_n_new'] + lam * d['casimir']
        X[i, 0] = gamma_eff
        X[i, 1] = math.log(d['G'])
        X[i, 2] = math.log(d['theta_D'])
        X[i, 3] = math.log(d['B'])
        X[i, 4] = math.log(d['N'])
        X[i, 5] = math.log(d['V'])
        X[i, 6] = 1.0
    return X

def obj3(lam):
    X = build_X3(lam[0])
    coef, _, _, _ = np.linalg.lstsq(X, y_lnk, rcond=None)
    return np.sum((y_lnk - X @ coef)**2)

res3 = minimize(obj3, x0=[0.234], method='Nelder-Mead', options={'maxiter': 10000})
lam3 = res3.x[0]
X3 = build_X3(lam3)
coef3, _, _, _ = np.linalg.lstsq(X3, y_lnk, rcond=None)
r2_3 = 1 - np.sum((y_lnk - X3 @ coef3)**2) / np.sum((y_lnk - np.mean(y_lnk))**2)
print(f"\nγ_eff = γ_n_new + {lam3:.4f}·j(j+1), R²={r2_3:.4f}")

err3 = []
for i in range(n_data):
    X_tr = np.delete(X3, i, axis=0)
    y_tr = np.delete(y_lnk, i)
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    ln_k = X3[i] @ coef
    tc_pred = math.sqrt(8 * data[i]['dd0']**2 * math.exp(ln_k) * data[i]['theta_D'] / (9 * LN2))
    err3.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
err3 = np.array(err3)

print(f"全部: 中位{np.median(err3)*100:.0f}%, 2倍内{np.mean(err3<=1)*100:.0f}%, 5倍内{np.mean(err3<=4)*100:.0f}%")
print(f"GL(1)常规: 中位{np.median(err3[is_gl1])*100:.0f}%, 2倍内{np.mean(err3[is_gl1]<=1)*100:.0f}%, 5倍内{np.mean(err3[is_gl1]<=4)*100:.0f}%")
print(f"GL(2)非常规: 中位{np.median(err3[is_gl2])*100:.0f}%, 2倍内{np.mean(err3[is_gl2]<=1)*100:.0f}%, 5倍内{np.mean(err3[is_gl2]<=4)*100:.0f}%")
print(f"重费米子: 中位{np.median(err3[is_hf])*100:.0f}%, 2倍内{np.mean(err3[is_hf]<=1)*100:.0f}%, 5倍内{np.mean(err3[is_hf]<=4)*100:.0f}%")

# ============================================================
# 策略4: 连续γ_eff — 不做离散化, 直接从几何参数回归
# ============================================================
print(f"\n{'='*80}")
print("策略4: 连续γ_eff从几何参数回归 (最优纯第一性)")
print("="*80)

# 用策略1的参数计算每个材料的γ_eff_implicit作为目标
y_gamma = np.array([d['gamma_eff_implicit'] for d in data])

# 几何特征
def get_feats(d):
    return np.array([
        math.log(d['G']), math.log(d['theta_D']), math.log(d['dd0']),
        math.log(d['M']), math.log(d['Z']) if d['Z'] > 0 else 0,
        math.log(d['V']), math.log(d['N']),
        math.log(d['B']) if d['B'] > 0 else 0,
    ])

X_geom = np.array([get_feats(d) for d in data])
FEAT_NAMES = ['ln(G)', 'ln(θ_D)', 'ln(Δδ₀)', 'ln(M)', 'ln(Z)', 'ln(V)', 'ln(N)', 'ln(B)']

# 线性回归
coef_g, _, _, _ = np.linalg.lstsq(X_geom, y_gamma, rcond=None)
r2_g = 1 - np.sum((y_gamma - X_geom @ coef_g)**2) / np.sum((y_gamma - np.mean(y_gamma))**2)
print(f"γ_eff线性回归 R² = {r2_g:.4f}")
for j, name in enumerate(FEAT_NAMES):
    print(f"  {name}: {coef_g[j]:.4f}")

# 用连续γ_eff预测Tc (LOOCV)
err4 = []
for i in range(n_data):
    # 回归γ_eff
    X_tr = np.delete(X_geom, i, axis=0)
    y_tr = np.delete(y_gamma, i)
    coef_g_l, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    gamma_pred = get_feats(data[i]) @ coef_g_l
    # 用γ_pred预测Tc
    X_tr2 = np.delete(X1, i, axis=0)
    y_tr2 = np.delete(y_lnk, i)
    coef_l, _, _, _ = np.linalg.lstsq(X_tr2, y_tr2, rcond=None)
    # 替换γ_eff
    x_test = X1[i].copy()
    x_test[0] = gamma_pred
    ln_k = x_test @ coef_l
    tc_pred = math.sqrt(8 * data[i]['dd0']**2 * math.exp(ln_k) * data[i]['theta_D'] / (9 * LN2))
    err4.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
err4 = np.array(err4)

print(f"\n连续γ_eff LOOCV: 中位{np.median(err4)*100:.0f}%, 2倍内{np.mean(err4<=1)*100:.0f}%, 5倍内{np.mean(err4<=4)*100:.0f}%")
print(f"GL(1)常规: 中位{np.median(err4[is_gl1])*100:.0f}%, 2倍内{np.mean(err4[is_gl1]<=1)*100:.0f}%, 5倍内{np.mean(err4[is_gl1]<=4)*100:.0f}%")
print(f"GL(2)非常规: 中位{np.median(err4[is_gl2])*100:.0f}%, 2倍内{np.mean(err4[is_gl2]<=1)*100:.0f}%, 5倍内{np.mean(err4[is_gl2]<=4)*100:.0f}%")
print(f"重费米子: 中位{np.median(err4[is_hf])*100:.0f}%, 2倍内{np.mean(err4[is_hf]<=1)*100:.0f}%, 5倍内{np.mean(err4[is_hf]<=4)*100:.0f}%")

# ============================================================
# 策略5: 最优 — 连续γ_eff + j(j+1)修正
# ============================================================
print(f"\n{'='*80}")
print("策略5: 连续γ_eff + j(j+1)修正 (最终最优)")
print("="*80)

# γ_eff_total = γ_geom(连续) + λ·j(j+1)
# 两阶段: 先回归γ_geom, 再优化λ

def obj5(lam):
    err = 0
    for i in range(n_data):
        X_tr = np.delete(X_geom, i, axis=0)
        y_tr = np.delete(y_gamma, i)
        coef_g_l, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
        gamma_geom = get_feats(data[i]) @ coef_g_l
        gamma_eff = gamma_geom + lam[0] * data[i]['casimir']
        # 用全数据K_eff公式参数
        ln_k = a1 * gamma_eff + p1*math.log(data[i]['G']) + q1*math.log(data[i]['theta_D']) + coef1[3]*math.log(data[i]['B']) + coef1[4]*math.log(data[i]['N']) + coef1[5]*math.log(data[i]['V']) + b1
        err += (ln_k - y_lnk[i])**2
    return err

res5 = minimize(obj5, x0=[0.234], method='Nelder-Mead', options={'maxiter': 5000})
lam5 = res5.x[0]
print(f"γ_eff = γ_geom + {lam5:.4f}·j(j+1)")

# LOOCV (两阶段)
err5 = []
for i in range(n_data):
    # 回归γ_geom
    X_tr = np.delete(X_geom, i, axis=0)
    y_tr = np.delete(y_gamma, i)
    coef_g_l, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    gamma_geom = get_feats(data[i]) @ coef_g_l
    gamma_eff = gamma_geom + lam5 * data[i]['casimir']

    # K_eff公式 (也用LOOCV)
    X_tr2 = np.delete(X1, i, axis=0)
    y_tr2 = np.delete(y_lnk, i)
    coef_l, _, _, _ = np.linalg.lstsq(X_tr2, y_tr2, rcond=None)
    x_test = X1[i].copy()
    x_test[0] = gamma_eff
    ln_k = x_test @ coef_l
    tc_pred = math.sqrt(8 * data[i]['dd0']**2 * math.exp(ln_k) * data[i]['theta_D'] / (9 * LN2))
    err5.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
err5 = np.array(err5)

print(f"LOOCV: 中位{np.median(err5)*100:.0f}%, 2倍内{np.mean(err5<=1)*100:.0f}%, 5倍内{np.mean(err5<=4)*100:.0f}%")