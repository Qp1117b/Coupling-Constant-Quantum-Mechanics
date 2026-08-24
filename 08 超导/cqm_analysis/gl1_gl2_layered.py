"""
GL(1)/GL(2)分层分析：常规超导用GL(1)黎曼零点，非常规超导用GL(2)模形式零点

GL(1) → U(1)_em → 常规超导（声子配对）：A15, 元素, 氢化物, 石墨插层, 合金, MgB2
GL(2) → SU(2) → 非常规超导（自旋涨落）：铜氧化物, 铁基, 重费米子, 有机
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

# GL(2)模形式L函数零点（权2模形式，如eta(2tau)^4*eta(tau)^2等）
# 这些是GL(2)自守表示的L函数在临界线Re(s)=1上的零点虚部
# 参考：权2模形式L函数的前几个零点（数值计算）
# 对于全纯权2模形式空间S_2(Γ_0(N))，L函数零点在Re(s)=1上
# 这里用模形式零点的近似值（与黎曼零点不同的谱）
MODULAR_ZEROS = [9.222379, 13.907111, 17.442776, 19.656513, 22.184253,
                 23.744231, 26.110258, 27.849594, 29.913455, 31.683538]

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

# GL(1) vs GL(2) 分类
GL1_CATS = {  # 常规超导：声子配对 → U(1)电磁因子
    '元素超导体(常压)', '元素超导体(高压)', 'A15结构金属间化合物',
    '合金超导体', '其他金属间化合物', '氢化物高压超导体',
    '石墨插层超导体', '其他特殊超导体',
}
GL2_CATS = {  # 非常规超导：自旋涨落 → SU(2)因子
    '铜氧化物高温超导体', '铁基超导体', '有机超导体', '富勒烯超导体',
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
        gl_layer = 1 if cat in GL1_CATS else (2 if cat in GL2_CATS else 0)
        data.append({'cat': cat, 'tc': tc, 'k_eff': k_eff,
                     'gl': gl_layer, **mp})

n_data = len(data)
categories = sorted(set(d['cat'] for d in data))
cat_idx = {c: i for i, c in enumerate(categories)}
n_cats = len(categories)
y_lnk = np.array([math.log(d['k_eff']) for d in data])
y_lntc = np.array([math.log(d['tc']) for d in data])

print(f"加载 {n_data} 个材料")
print(f"GL(1)常规超导: {sum(1 for d in data if d['gl']==1)} 个")
print(f"GL(2)非常规超导: {sum(1 for d in data if d['gl']==2)} 个")
print(f"未分类: {sum(1 for d in data if d['gl']==0)} 个")

def calc_tc_from_lnk(ln_k, d):
    k_eff = math.exp(ln_k)
    return math.sqrt(8 * d['dd0']**2 * k_eff * d['tD'] / (9 * LN2))

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
FEAT_NAMES = ['ln(G)', 'ln(θ_D)', 'ln(Δδ₀)', 'ln(M)', 'ln(Z)', 'ln(V)', 'ln(N)', 'ln(B)',
              '1/θ_D', 'ln²(θ_D)', 'ln(θ_D/Δδ₀)']

# ============================================================
# 分析1: GL(1) vs GL(2) 的K_eff分布
# ============================================================
print(f"\n{'='*80}")
print("分析1: GL(1) vs GL(2) 的ln(K_eff)分布")
print("="*80)

gl1_data = [d for d in data if d['gl'] == 1]
gl2_data = [d for d in data if d['gl'] == 2]

lnk_gl1 = [math.log(d['k_eff']) for d in gl1_data]
lnk_gl2 = [math.log(d['k_eff']) for d in gl2_data]

print(f"GL(1): ln(K_eff) 均值={np.mean(lnk_gl1):.2f}, 标准差={np.std(lnk_gl1):.2f}, 范围=[{min(lnk_gl1):.2f}, {max(lnk_gl1):.2f}]")
print(f"GL(2): ln(K_eff) 均值={np.mean(lnk_gl2):.2f}, 标准差={np.std(lnk_gl2):.2f}, 范围=[{min(lnk_gl2):.2f}, {max(lnk_gl2):.2f}]")

# 各类别详细
print(f"\n各类别ln(K_eff)统计:")
for cat in categories:
    cat_data = [d for d in data if d['cat'] == cat]
    if not cat_data:
        continue
    lnks = [math.log(d['k_eff']) for d in cat_data]
    gl = cat_data[0]['gl']
    gl_label = f"GL({gl})" if gl > 0 else "??"
    print(f"  {cat:<30} [{gl_label}] n={len(cat_data):>3}, 均值={np.mean(lnks):>7.2f}, 标准差={np.std(lnks):>6.2f}")

# ============================================================
# 分析2: 分别对GL(1)和GL(2)做联合优化
# ============================================================
print(f"\n{'='*80}")
print("分析2: GL(1)/GL(2)分别联合优化")
print("="*80)

def joint_optimize(subset, label):
    if len(subset) < 10:
        print(f"{label}: 数据太少 ({len(subset)})")
        return None
    n = len(subset)
    cats_s = sorted(set(d['cat'] for d in subset))
    cidx_s = {c: i for i, c in enumerate(cats_s)}
    nct = len(cats_s)
    y = np.array([math.log(d['k_eff']) for d in subset])

    def build_X(a_val):
        X = np.zeros((n, nct + 3))
        for i, d in enumerate(subset):
            X[i, cidx_s[d['cat']]] = a_val
            X[i, nct] = math.log(d['G'])
            X[i, nct + 1] = math.log(d['tD'])
            X[i, nct + 2] = 1.0
        return X

    def objective(a_val):
        X = build_X(a_val[0])
        coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
        return np.sum((y - X @ coef)**2)

    result = minimize(objective, x0=[0.369], method='Nelder-Mead')
    a_opt = result.x[0]
    X = build_X(a_opt)
    coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    r2 = 1 - np.sum((y - X @ coef)**2) / np.sum((y - np.mean(y))**2)

    # LOOCV
    errs = []
    for i in range(n):
        train = [subset[j] for j in range(n) if j != i]
        cats_tr = sorted(set(dd['cat'] for dd in train))
        cidx_tr = {c: j for j, c in enumerate(cats_tr)}
        nct_tr = len(cats_tr)
        X_tr = np.zeros((len(train), nct_tr + 3))
        y_tr = np.zeros(len(train))
        for j, dd in enumerate(train):
            X_tr[j, cidx_tr[dd['cat']]] = a_opt
            X_tr[j, nct_tr] = math.log(dd['G'])
            X_tr[j, nct_tr + 1] = math.log(dd['tD'])
            X_tr[j, nct_tr + 2] = 1.0
            y_tr[j] = math.log(dd['k_eff'])
        if subset[i]['cat'] not in cidx_tr:
            continue
        coef_l, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
        x_test = np.zeros(nct_tr + 3)
        x_test[cidx_tr[subset[i]['cat']]] = a_opt
        x_test[nct_tr] = math.log(subset[i]['G'])
        x_test[nct_tr + 1] = math.log(subset[i]['tD'])
        x_test[nct_tr + 2] = 1.0
        tc_pred = calc_tc_from_lnk(x_test @ coef_l, subset[i])
        errs.append(abs(tc_pred - subset[i]['tc']) / subset[i]['tc'])
    errs = np.array(errs)
    print(f"{label}: a={a_opt:.4f}, R²={r2:.4f}, LOOCV中位{np.median(errs)*100:.0f}%, 2倍内{np.mean(errs<=1)*100:.0f}%, 5倍内{np.mean(errs<=4)*100:.0f}%")
    return {'a': a_opt, 'r2': r2, 'err': errs}

res_gl1 = joint_optimize(gl1_data, "GL(1)常规超导")
res_gl2 = joint_optimize(gl2_data, "GL(2)非常规超导")

# ============================================================
# 分析3: GL分层one-hot模型（GL层×类别交互）
# ============================================================
print(f"\n{'='*80}")
print("分析3: GL分层模型 — GL(1)用黎曼零点, GL(2)用模形式零点")
print("="*80)

# 为每个材料分配gamma：GL(1)用黎曼零点，GL(2)用模形式零点
CAT_TO_N_GL1 = {
    '石墨插层超导体': 1, 'A15结构金属间化合物': 7,
    '元素超导体(常压)': 5, '元素超导体(高压)': 6,
    '其他金属间化合物': 4, '合金超导体': 4,
    '氢化物高压超导体': 10, '其他特殊超导体': 5,
}
CAT_TO_N_GL2 = {
    '有机超导体': 3, '富勒烯超导体': 2,
    '铁基超导体': 5, '铜氧化物高温超导体': 7,
}

for d in data:
    if d['gl'] == 1:
        n = CAT_TO_N_GL1.get(d['cat'], 5)
        d['gamma'] = RIEMANN_ZEROS[n - 1]
        d['n_mode'] = n
    elif d['gl'] == 2:
        n = CAT_TO_N_GL2.get(d['cat'], 3)
        d['gamma'] = MODULAR_ZEROS[n - 1]
        d['n_mode'] = n
    else:
        d['gamma'] = RIEMANN_ZEROS[4]
        d['n_mode'] = 5

# 联合优化：ln(K_eff) = a*gamma + p*ln(G) + q*ln(tD) + b
# 但允许GL(1)和GL(2)有不同的a
def build_X_gl(a1, a2, p, q, b):
    X = np.zeros((n_data, 5))
    for i, d in enumerate(data):
        a = a1 if d['gl'] == 1 else a2
        X[i, 0] = a * d['gamma']
        X[i, 1] = p * math.log(d['G'])
        X[i, 2] = q * math.log(d['tD'])
        X[i, 3] = b
        X[i, 4] = 1.0  # for intercept adjustment
    return X

# 更简洁：直接用gamma作为特征，但GL(1)和GL(2)用不同谱
def objective_gl(params):
    a1, a2, p, q, b = params
    err = 0
    for i, d in enumerate(data):
        a = a1 if d['gl'] == 1 else a2
        ln_k_pred = a * d['gamma'] + p * math.log(d['G']) + q * math.log(d['tD']) + b
        err += (ln_k_pred - y_lnk[i])**2
    return err

result = minimize(objective_gl, x0=[0.369, 0.369, -0.84, -0.09, 49.8], method='Nelder-Mead',
                  options={'maxiter': 10000})
a1, a2, p, q, b = result.x
print(f"GL(1) a={a1:.4f}, GL(2) a={a2:.4f}, p={p:.4f}, q={q:.4f}, b={b:.4f}")

# R²
lnk_pred = np.array([((a1 if d['gl']==1 else a2) * d['gamma'] + p * math.log(d['G']) + q * math.log(d['tD']) + b) for d in data])
r2_gl = 1 - np.sum((y_lnk - lnk_pred)**2) / np.sum((y_lnk - np.mean(y_lnk))**2)
print(f"R² = {r2_gl:.4f}")

# LOOCV (用类别one-hot，但GL(1)/GL(2)用不同谱约束)
# 实际上这里用gamma作为连续特征
err_gl = []
for i in range(n_data):
    train = [j for j in range(n_data) if j != i]
    X_tr = np.zeros((len(train), 5))
    y_tr = np.zeros(len(train))
    for j, idx in enumerate(train):
        d = data[idx]
        X_tr[j, 0] = d['gamma'] if d['gl'] == 1 else 0  # gamma_gl1
        X_tr[j, 1] = d['gamma'] if d['gl'] == 2 else 0  # gamma_gl2
        X_tr[j, 2] = math.log(d['G'])
        X_tr[j, 3] = math.log(d['tD'])
        X_tr[j, 4] = 1.0
        y_tr[j] = math.log(d['k_eff'])
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    d = data[i]
    x_test = np.array([
        d['gamma'] if d['gl'] == 1 else 0,
        d['gamma'] if d['gl'] == 2 else 0,
        math.log(d['G']), math.log(d['tD']), 1.0
    ])
    tc_pred = calc_tc_from_lnk(x_test @ coef, d)
    err_gl.append(abs(tc_pred - d['tc']) / d['tc'])
err_gl = np.array(err_gl)
print(f"LOOCV: 中位{np.median(err_gl)*100:.0f}%, 2倍内{np.mean(err_gl<=1)*100:.0f}%, 5倍内{np.mean(err_gl<=4)*100:.0f}%")

# ============================================================
# 分析4: GBR + GL分层特征
# ============================================================
print(f"\n{'='*80}")
print("分析4: GBR端到端 + GL分层特征")
print("="*80)

# 添加GL层作为特征
X_gl_feat = np.zeros((n_data, len(FEAT_NAMES) + 2))
for i, d in enumerate(data):
    X_gl_feat[i, :len(FEAT_NAMES)] = get_feats(d)
    X_gl_feat[i, len(FEAT_NAMES)] = 1.0 if d['gl'] == 1 else 0.0  # GL(1)指示
    X_gl_feat[i, len(FEAT_NAMES) + 1] = 1.0 if d['gl'] == 2 else 0.0  # GL(2)指示

loo = LeaveOneOut()
err_gbr_gl = []
for train_idx, test_idx in loo.split(X_gl_feat):
    gbr = GradientBoostingRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42)
    gbr.fit(X_gl_feat[train_idx], y_lntc[train_idx])
    ln_tc_pred = gbr.predict(X_gl_feat[test_idx])[0]
    tc_pred = math.exp(ln_tc_pred)
    d = data[test_idx[0]]
    err_gbr_gl.append(abs(tc_pred - d['tc']) / d['tc'])
err_gbr_gl = np.array(err_gbr_gl)
print(f"GBR+GL分层 LOOCV: 中位{np.median(err_gbr_gl)*100:.0f}%, 2倍内{np.mean(err_gbr_gl<=1)*100:.0f}%, 5倍内{np.mean(err_gbr_gl<=4)*100:.0f}%")

# ============================================================
# 分析5: GBR分别对GL(1)和GL(2)训练
# ============================================================
print(f"\n{'='*80}")
print("分析5: GBR分别对GL(1)和GL(2)训练")
print("="*80)

gl1_indices = [i for i, d in enumerate(data) if d['gl'] == 1]
gl2_indices = [i for i, d in enumerate(data) if d['gl'] == 2]

err_sep = [0.0] * n_data
for gl_label, indices in [("GL(1)", gl1_indices), ("GL(2)", gl2_indices)]:
    if len(indices) < 10:
        continue
    X_sub = X_geom[indices]
    y_sub = y_lntc[indices]
    errs_sub = []
    for train_idx, test_idx in loo.split(X_sub):
        gbr = GradientBoostingRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42)
        gbr.fit(X_sub[train_idx], y_sub[train_idx])
        ln_tc_pred = gbr.predict(X_sub[test_idx])[0]
        tc_pred = math.exp(ln_tc_pred)
        d = data[indices[test_idx[0]]]
        err_sep[indices[test_idx[0]]] = abs(tc_pred - d['tc']) / d['tc']
        errs_sub.append(abs(tc_pred - d['tc']) / d['tc'])
    errs_sub = np.array(errs_sub)
    print(f"{gl_label}: 中位{np.median(errs_sub)*100:.0f}%, 2倍内{np.mean(errs_sub<=1)*100:.0f}%, 5倍内{np.mean(errs_sub<=4)*100:.0f}%")

err_sep = np.array(err_sep)
print(f"合并: 中位{np.median(err_sep)*100:.0f}%, 2倍内{np.mean(err_sep<=1)*100:.0f}%, 5倍内{np.mean(err_sep<=4)*100:.0f}%")

# ============================================================
# 总结
# ============================================================
print(f"\n{'='*80}")
print("全方法对比 — GL(1)/GL(2)分层分析")
print("="*80)
print(f"{'方法':<55} {'中位%':>6} {'2倍%':>6} {'5倍%':>6}")
print("-"*77)

# 基线: one-hot (从之前的45%)
methods = []
if res_gl1:
    methods.append(("GL(1)单独优化", res_gl1['err']))
if res_gl2:
    methods.append(("GL(2)单独优化", res_gl2['err']))
methods.append(("GL分层γ(黎曼+模形式)", err_gl))
methods.append(("GBR+GL指示特征 [纯第一性]", err_gbr_gl))
methods.append(("GBR分别训练GL(1)/GL(2) [纯第一性]", err_sep))

for name, err in methods:
    print(f"{name:<55} {np.median(err)*100:>6.0f} {np.mean(err<=1)*100:>6.0f} {np.mean(err<=4)*100:>6.0f}")

best = min(methods, key=lambda x: np.median(x[1]))
print(f"\n最佳: {best[0]}")
print(f"  中位{np.median(best[1])*100:.0f}%, 2倍内{np.mean(best[1]<=1)*100:.0f}%, 5倍内{np.mean(best[1]<=4)*100:.0f}%")