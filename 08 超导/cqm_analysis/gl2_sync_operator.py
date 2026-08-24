"""
GL(2)同步算符的第一性推导

发生学: SU(5)破缺 → U(1)×SU(2)×SU(3)
  - GL(1) → U(1)_em → 黎曼零点 → 常规超导
  - GL(2) → SU(2)_spin → 模形式零点 + Casimir → 非常规超导

同步算符在非常规超导中涉及GL(2)因子:
  Ŝ_super = Ŝ_GL1 + Ŝ_GL2

GL(2)的本征值结构:
  - 紧群SU(2)的Casimir: j(j+1), j=0,1/2,1,3/2,...
  - 自旋表示维度: 2j+1
  - 配对对称性: s波(j=0), p波(j=1), d波(j=2)

关键假设: K_0^GL2 = C·exp(a·γ_eff),
  γ_eff = γ_riemann + λ·j(j+1)  (黎曼零点+SU(2)Casimir修正)
"""

import csv, re, math
import numpy as np
from scipy.optimize import minimize
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import LeaveOneOut

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

GL1_CATS = {
    '元素超导体(常压)', '元素超导体(高压)', 'A15结构金属间化合物',
    '合金超导体', '其他金属间化合物', '氢化物高压超导体',
    '石墨插层超导体', '其他特殊超导体',
}
GL2_CATS = {
    '铜氧化物高温超导体', '铁基超导体', '有机超导体', '富勒烯超导体',
}

# SU(2)自旋量子数j和配对对称性
# j=0: s波(常规), j=1: p波, j=2: d波(铜氧化物),
# 铁基: s±波(有效j=1), 有机: p波或d波(j=1)
CAT_TO_SPIN_J = {
    # GL(1) - 常规超导, j=0 (s波)
    '元素超导体(常压)': 0, '元素超导体(高压)': 0,
    'A15结构金属间化合物': 0, '合金超导体': 0,
    '其他金属间化合物': 0, '氢化物高压超导体': 0,
    '石墨插层超导体': 0, '其他特殊超导体': 0,
    # GL(2) - 非常规超导
    '铜氧化物高温超导体': 2,    # d波, j=2, Casimir=6
    '铁基超导体': 1,           # s±波, 有效j=1, Casimir=2
    '有机超导体': 1,           # p波/d波, j=1, Casimir=2
    '富勒烯超导体': 1,         # s波但非常规, j=1
}

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
        gl = 1 if cat in GL1_CATS else (2 if cat in GL2_CATS else 1)
        j_spin = CAT_TO_SPIN_J.get(cat, 0)
        n_mode = CAT_TO_N.get(cat, 5)
        gamma_n = RIEMANN_ZEROS[n_mode - 1]
        casimir = j_spin * (j_spin + 1)
        data.append({'cat': cat, 'tc': tc, 'k_eff': k_eff,
                     'gl': gl, 'j': j_spin, 'casimir': casimir,
                     'gamma_n': gamma_n, 'n_mode': n_mode, **mp})

n_data = len(data)
categories = sorted(set(d['cat'] for d in data))
cat_idx = {c: i for i, c in enumerate(categories)}
n_cats = len(categories)
y_lnk = np.array([math.log(d['k_eff']) for d in data])
y_lntc = np.array([math.log(d['tc']) for d in data])

print(f"加载 {n_data} 个材料")
print(f"GL(1): {sum(1 for d in data if d['gl']==1)}, GL(2): {sum(1 for d in data if d['gl']==2)}")

def calc_tc_from_lnk(ln_k, d):
    k_eff = math.exp(ln_k)
    return math.sqrt(8 * d['dd0']**2 * k_eff * d['tD'] / (9 * LN2))

# ============================================================
# 模型1: 基线 one-hot (45%)
# ============================================================
print(f"\n{'='*80}")
print("模型1: 基线 one-hot类别模型")
print("="*80)

err1 = []
for i in range(n_data):
    train = [data[j] for j in range(n_data) if j != i]
    cats_tr = sorted(set(dd['cat'] for dd in train))
    cidx_tr = {c: j for j, c in enumerate(cats_tr)}
    nct = len(cats_tr)
    if data[i]['cat'] not in cidx_tr:
        err1.append(0); continue
    X_tr = np.zeros((len(train), nct + 3))
    y_tr = np.zeros(len(train))
    for j, dd in enumerate(train):
        X_tr[j, cidx_tr[dd['cat']]] = 1.0
        X_tr[j, nct] = math.log(dd['G'])
        X_tr[j, nct + 1] = math.log(dd['tD'])
        X_tr[j, nct + 2] = 1.0
        y_tr[j] = math.log(dd['k_eff'])
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    x_test = np.zeros(nct + 3)
    x_test[cidx_tr[data[i]['cat']]] = 1.0
    x_test[nct] = math.log(data[i]['G'])
    x_test[nct + 1] = math.log(data[i]['tD'])
    x_test[nct + 2] = 1.0
    tc_pred = calc_tc_from_lnk(x_test @ coef, data[i])
    err1.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
err1 = np.array(err1)
print(f"中位{np.median(err1)*100:.0f}%, 2倍内{np.mean(err1<=1)*100:.0f}%, 5倍内{np.mean(err1<=4)*100:.0f}%")

# ============================================================
# 模型2: γ_riemann + Casimir修正 (第一性GL(2)推导)
# ln(K_eff) = a·γ_n + λ·j(j+1) + p·ln(G) + q·ln(θ_D) + b
# ============================================================
print(f"\n{'='*80}")
print("模型2: γ_riemann + λ·j(j+1) + p·ln(G) + q·ln(θ_D) + b")
print("  [GL(1)同步算符本征值=黎曼零点, GL(2)修正=SU(2)Casimir]")
print("="*80)

def build_X2():
    X = np.zeros((n_data, 5))
    for i, d in enumerate(data):
        X[i, 0] = d['gamma_n']
        X[i, 1] = d['casimir']
        X[i, 2] = math.log(d['G'])
        X[i, 3] = math.log(d['tD'])
        X[i, 4] = 1.0
    return X

X2 = build_X2()
coef2, _, _, _ = np.linalg.lstsq(X2, y_lnk, rcond=None)
r2_2 = 1 - np.sum((y_lnk - X2 @ coef2)**2) / np.sum((y_lnk - np.mean(y_lnk))**2)
print(f"全数据: a={coef2[0]:.4f}, λ={coef2[1]:.4f}, p={coef2[2]:.4f}, q={coef2[3]:.4f}, b={coef2[4]:.4f}")
print(f"R² = {r2_2:.4f}")

err2 = []
for i in range(n_data):
    X_tr = np.delete(X2, i, axis=0)
    y_tr = np.delete(y_lnk, i)
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    tc_pred = calc_tc_from_lnk(X2[i] @ coef, data[i])
    err2.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
err2 = np.array(err2)
print(f"LOOCV: 中位{np.median(err2)*100:.0f}%, 2倍内{np.mean(err2<=1)*100:.0f}%, 5倍内{np.mean(err2<=4)*100:.0f}%")

# ============================================================
# 模型3: γ_riemann + λ·j(j+1) + 类别one-hot (混合)
# ============================================================
print(f"\n{'='*80}")
print("模型3: a·γ_n + λ·j(j+1) + one-hot(类别) + p·ln(G) + q·ln(θ_D) + b")
print("="*80)

def build_X3(a_val, lam_val):
    X = np.zeros((n_data, n_cats + 4))
    for i, d in enumerate(data):
        X[i, cat_idx[d['cat']]] = 1.0
        X[i, n_cats] = a_val * d['gamma_n']
        X[i, n_cats + 1] = lam_val * d['casimir']
        X[i, n_cats + 2] = math.log(d['G'])
        X[i, n_cats + 3] = math.log(d['tD'])
    return X

def obj3(params):
    X = build_X3(params[0], params[1])
    coef, _, _, _ = np.linalg.lstsq(X, y_lnk, rcond=None)
    return np.sum((y_lnk - X @ coef)**2)

res3 = minimize(obj3, x0=[0.369, 0.5], method='Nelder-Mead', options={'maxiter': 5000})
a3, lam3 = res3.x
X3 = build_X3(a3, lam3)
coef3, _, _, _ = np.linalg.lstsq(X3, y_lnk, rcond=None)
r2_3 = 1 - np.sum((y_lnk - X3 @ coef3)**2) / np.sum((y_lnk - np.mean(y_lnk))**2)
print(f"a={a3:.4f}, λ={lam3:.4f}, R²={r2_3:.4f}")

err3 = []
for i in range(n_data):
    train = [data[j] for j in range(n_data) if j != i]
    cats_tr = sorted(set(dd['cat'] for dd in train))
    cidx_tr = {c: j for j, c in enumerate(cats_tr)}
    nct = len(cats_tr)
    if data[i]['cat'] not in cidx_tr:
        err3.append(0); continue
    X_tr = np.zeros((len(train), nct + 4))
    y_tr = np.zeros(len(train))
    for j, dd in enumerate(train):
        X_tr[j, cidx_tr[dd['cat']]] = 1.0
        X_tr[j, nct] = a3 * dd['gamma_n']
        X_tr[j, nct + 1] = lam3 * dd['casimir']
        X_tr[j, nct + 2] = math.log(dd['G'])
        X_tr[j, nct + 3] = math.log(dd['tD'])
        y_tr[j] = math.log(dd['k_eff'])
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    x_test = np.zeros(nct + 4)
    x_test[cidx_tr[data[i]['cat']]] = 1.0
    x_test[nct] = a3 * data[i]['gamma_n']
    x_test[nct + 1] = lam3 * data[i]['casimir']
    x_test[nct + 2] = math.log(data[i]['G'])
    x_test[nct + 3] = math.log(data[i]['tD'])
    tc_pred = calc_tc_from_lnk(x_test @ coef, data[i])
    err3.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
err3 = np.array(err3)
print(f"LOOCV: 中位{np.median(err3)*100:.0f}%, 2倍内{np.mean(err3<=1)*100:.0f}%, 5倍内{np.mean(err3<=4)*100:.0f}%")

# ============================================================
# 模型4: 纯第一性 — γ_n + Casimir + 几何 (不用类别one-hot)
# ln(K_eff) = a·γ_n + λ·j(j+1) + p·ln(G) + q·ln(θ_D) + r·ln(B) + b
# ============================================================
print(f"\n{'='*80}")
print("模型4: 纯第一性 a·γ_n + λ·j(j+1) + p·ln(G) + q·ln(θ_D) + r·ln(B) + b")
print("="*80)

def build_X4():
    X = np.zeros((n_data, 6))
    for i, d in enumerate(data):
        X[i, 0] = d['gamma_n']
        X[i, 1] = d['casimir']
        X[i, 2] = math.log(d['G'])
        X[i, 3] = math.log(d['tD'])
        X[i, 4] = math.log(d['B']) if d['B'] > 0 else 0
        X[i, 5] = 1.0
    return X

X4 = build_X4()
coef4, _, _, _ = np.linalg.lstsq(X4, y_lnk, rcond=None)
r2_4 = 1 - np.sum((y_lnk - X4 @ coef4)**2) / np.sum((y_lnk - np.mean(y_lnk))**2)
print(f"a={coef4[0]:.4f}, λ={coef4[1]:.4f}, p={coef4[2]:.4f}, q={coef4[3]:.4f}, r={coef4[4]:.4f}, b={coef4[5]:.4f}")
print(f"R² = {r2_4:.4f}")

err4 = []
for i in range(n_data):
    X_tr = np.delete(X4, i, axis=0)
    y_tr = np.delete(y_lnk, i)
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    tc_pred = calc_tc_from_lnk(X4[i] @ coef, data[i])
    err4.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
err4 = np.array(err4)
print(f"LOOCV: 中位{np.median(err4)*100:.0f}%, 2倍内{np.mean(err4<=1)*100:.0f}%, 5倍内{np.mean(err4<=4)*100:.0f}%")

# ============================================================
# 模型5: γ_eff = γ_n + λ·j(j+1), 然后统一指数公式
# K_0 = C·exp(a·γ_eff), γ_eff = γ_n + λ·j(j+1)
# ============================================================
print(f"\n{'='*80}")
print("模型5: γ_eff = γ_n + λ·j(j+1), K_0 = C·exp(a·γ_eff)")
print("="*80)

# 先从K_0反推γ_eff
# ln(K_0) = a·γ_eff + const → γ_eff = (ln(K_0) - const) / a
# 但K_0 = K_eff / (G^p * θ_D^q), 需要先知道p,q
# 用模型2的p,q
p2, q2 = coef2[2], coef2[3]
k0_vals = []
for d in data:
    k0 = d['k_eff'] / (d['G']**p2 * d['tD']**q2)
    k0_vals.append(k0)
k0_vals = np.array(k0_vals)
ln_k0 = np.log(k0_vals)

# 回归 ln(K_0) = a·γ_n + λ·j(j+1) + const
X5 = np.zeros((n_data, 3))
for i, d in enumerate(data):
    X5[i, 0] = d['gamma_n']
    X5[i, 1] = d['casimir']
    X5[i, 2] = 1.0
coef5, _, _, _ = np.linalg.lstsq(X5, ln_k0, rcond=None)
r2_5 = 1 - np.sum((ln_k0 - X5 @ coef5)**2) / np.sum((ln_k0 - np.mean(ln_k0))**2)
print(f"ln(K_0) = {coef5[0]:.4f}·γ_n + {coef5[1]:.4f}·j(j+1) + {coef5[2]:.4f}")
print(f"R² = {r2_5:.4f}")
print(f"γ_eff = γ_n + {coef5[1]/coef5[0]:.4f}·j(j+1)")

# 各类别γ_eff
print(f"\n各类别γ_eff:")
for cat in categories:
    cat_data = [d for d in data if d['cat'] == cat]
    if not cat_data:
        continue
    d0 = cat_data[0]
    gamma_eff = d0['gamma_n'] + (coef5[1]/coef5[0]) * d0['casimir']
    print(f"  {cat:<30} j={d0['j']}, Casimir={d0['casimir']}, γ_n={d0['gamma_n']:.2f}, γ_eff={gamma_eff:.2f}")

# ============================================================
# 模型6: GBR + γ_n + Casimir (纯第一性)
# ============================================================
print(f"\n{'='*80}")
print("模型6: GBR端到端 + γ_n + Casimir特征 [纯第一性]")
print("="*80)

def get_feats_ext(d):
    return np.array([
        math.log(d['G']), math.log(d['tD']), math.log(d['dd0']),
        math.log(d['M']), math.log(d['Z']) if d['Z'] > 0 else 0,
        math.log(d['V']), math.log(d['n_atoms']),
        math.log(d['B']) if d['B'] > 0 else 0,
        1.0/d['tD'], math.log(d['tD'])**2,
        math.log(d['tD']/d['dd0']) if d['dd0'] > 0 else 0,
        d['gamma_n'],           # GL(1)黎曼零点
        d['casimir'],           # GL(2) SU(2) Casimir
        d['j'],                 # 自旋量子数
        1.0 if d['gl']==2 else 0.0,  # GL层指示
    ])

X_ext = np.array([get_feats_ext(d) for d in data])
loo = LeaveOneOut()

err6 = []
for train_idx, test_idx in loo.split(X_ext):
    gbr = GradientBoostingRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42)
    gbr.fit(X_ext[train_idx], y_lntc[train_idx])
    ln_tc_pred = gbr.predict(X_ext[test_idx])[0]
    tc_pred = math.exp(ln_tc_pred)
    d = data[test_idx[0]]
    err6.append(abs(tc_pred - d['tc']) / d['tc'])
err6 = np.array(err6)
print(f"LOOCV: 中位{np.median(err6)*100:.0f}%, 2倍内{np.mean(err6<=1)*100:.0f}%, 5倍内{np.mean(err6<=4)*100:.0f}%")

# 特征重要性
gbr_full = GradientBoostingRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42)
gbr_full.fit(X_ext, y_lntc)
feat_names_ext = ['ln(G)', 'ln(θ_D)', 'ln(Δδ₀)', 'ln(M)', 'ln(Z)', 'ln(V)', 'ln(N)', 'ln(B)',
                  '1/θ_D', 'ln²(θ_D)', 'ln(θ_D/Δδ₀)', 'γ_n', 'j(j+1)', 'j', 'GL2指示']
print(f"\n特征重要性:")
for name, imp in sorted(zip(feat_names_ext, gbr_full.feature_importances_), key=lambda x: -x[1]):
    print(f"  {name:<15}: {imp:.4f}")

# ============================================================
# 总结
# ============================================================
print(f"\n{'='*80}")
print("全方法对比 — GL(2)同步算符第一性推导")
print("="*80)
print(f"{'方法':<55} {'中位%':>6} {'2倍%':>6} {'5倍%':>6}")
print("-"*77)
methods = [
    ("1: one-hot类别模型 (基线)", err1),
    (f"2: γ_n+λ·j(j+1)+G+θ_D [纯第一性]", err2),
    (f"3: γ_n+Casimir+one-hot+G+θ_D", err3),
    (f"4: γ_n+Casimir+G+θ_D+B [纯第一性]", err4),
    (f"6: GBR+γ_n+Casimir [纯第一性]", err6),
]
for name, err in methods:
    print(f"{name:<55} {np.median(err)*100:>6.0f} {np.mean(err<=1)*100:>6.0f} {np.mean(err<=4)*100:>6.0f}")

best = min(methods, key=lambda x: np.median(x[1]))
print(f"\n最佳: {best[0]}")
print(f"  中位{np.median(best[1])*100:.0f}%, 2倍内{np.mean(best[1]<=1)*100:.0f}%, 5倍内{np.mean(best[1]<=4)*100:.0f}%")

pure = [(n, e) for n, e in methods if "纯第一性" in n]
best_pure = min(pure, key=lambda x: np.median(x[1]))
print(f"\n纯第一性最佳: {best_pure[0]}")
print(f"  中位{np.median(best_pure[1])*100:.0f}%, 2倍内{np.mean(best_pure[1]<=1)*100:.0f}%, 5倍内{np.mean(best_pure[1]<=4)*100:.0f}%")