"""
GL(2)零点差 vs j(j+1) Casimir修正：超导Tc预测精度对比

理论背景:
  C_f = 0 (rank=0椭圆曲线, 函数方程严格推导)
  → GL(2)不通过谱量子C_f进入Tc
  → GL(2)通过零点差 γ₂^(f)-γ₁^(f) 进入本征值交叉

对比方案:
  A (原方案): γ_eff = γ_n + λ·j(j+1),  j(j+1) ∈ {0, 2, 6}
  B (零点差): γ_eff = γ_n + λ·Δγ_f,    Δγ_f ∈ {0, 0.346, 0.367}
  C (标准化): γ_eff = γ_n + λ·(Δγ_f/Δγ_1),  归一化到GL(1)零点差
  D (双参数): γ_eff = γ_n + λ₁·j(j+1) + λ₂·Δγ_f

关键比值对比:
  j(j+1)比值: d/p = 6/2 = 3.0
  GL(2)零点差比值: d/p ≈ 0.367/0.346 ≈ 1.06
  → 若方案B优于方案A, 说明GL(2)零点差是更基本的参数
"""
import csv, re, math
import numpy as np
from scipy.optimize import minimize

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
BETA = 8 * math.pi + 1
C2 = 2.0 / 3.0
LN2 = math.log(2)

RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832]

GL1_ZERO_GAP = 21.022040 - 14.134725

GL2_ZERO_GAP_D = 0.367
GL2_ZERO_GAP_P = 0.346

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

CAT_TO_PAIRING = {
    '铜氧化物高温超导体': 'd', '铁基超导体': 'p', '有机超导体': 'p', '富勒烯超导体': 'p',
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
        pairing = CAT_TO_PAIRING.get(cat, 's')
        if mp['has_f'] and gl == 1:
            n_mode = 1
            j = 0
            pairing = 's'
        else:
            n_mode = CAT_TO_N.get(cat, 5)
        gamma_n = RIEMANN_ZEROS[n_mode - 1]
        casimir = j * (j + 1)
        if pairing == 'd':
            zero_gap = GL2_ZERO_GAP_D
        elif pairing == 'p':
            zero_gap = GL2_ZERO_GAP_P
        else:
            zero_gap = 0.0
        zero_gap_norm = zero_gap / GL1_ZERO_GAP
        k_eff = tc**2 * 9 * LN2 / (8 * mp['dd0']**2 * mp['theta_D'])
        data.append({**mp, 'cat': cat, 'tc': tc, 'k_eff': k_eff,
                     'gl': gl, 'j': j, 'casimir': casimir,
                     'pairing': pairing, 'zero_gap': zero_gap,
                     'zero_gap_norm': zero_gap_norm,
                     'gamma_n': gamma_n, 'n_mode': n_mode})

n_data = len(data)
y_lnk = np.array([math.log(d['k_eff']) for d in data])

print("=" * 90)
print("GL(2)零点差 vs j(j+1) Casimir修正：超导Tc预测精度对比")
print("=" * 90)
print(f"\n材料数: {n_data}")
print(f"GL(1)零点差 Δγ₁ = γ₂-γ₁ = {GL1_ZERO_GAP:.4f}")
print(f"GL(2) d波零点差 Δγ_d = {GL2_ZERO_GAP_D:.4f}")
print(f"GL(2) p波零点差 Δγ_p = {GL2_ZERO_GAP_P:.4f}")
print(f"j(j+1)比值 d/p = {6/2:.4f}")
print(f"GL(2)零点差比值 d/p = {GL2_ZERO_GAP_D/GL2_ZERO_GAP_P:.4f}")

def build_X_multi(feat_funcs, lams):
    """通用特征矩阵构造: feat_funcs是返回额外特征的函数列表"""
    n_extra = sum(f() for f in feat_funcs) if feat_funcs else 0
    n_cols = 6 + len(lams)
    X = np.zeros((n_data, n_cols))
    for i, d in enumerate(data):
        gamma_eff = d['gamma_n']
        for k, lam in enumerate(lams):
            gamma_eff += lam * feat_funcs[k](d)
        X[i, 0] = gamma_eff
        X[i, 1] = math.log(d['G'])
        X[i, 2] = math.log(d['theta_D'])
        X[i, 3] = math.log(d['B'])
        X[i, 4] = math.log(d['N'])
        X[i, 5] = math.log(d['V'])
        X[i, 6] = 1.0
    return X

def run_scheme(name, feat_func, lam_init, lam_bounds=None):
    """运行单个方案: feat_func(d)返回修正项, lam是优化参数"""
    def build_X(lam):
        X = np.zeros((n_data, 7))
        for i, d in enumerate(data):
            gamma_eff = d['gamma_n'] + lam[0] * feat_func(d)
            X[i, 0] = gamma_eff
            X[i, 1] = math.log(d['G'])
            X[i, 2] = math.log(d['theta_D'])
            X[i, 3] = math.log(d['B'])
            X[i, 4] = math.log(d['N'])
            X[i, 5] = math.log(d['V'])
            X[i, 6] = 1.0
        return X

    def objective(lam):
        X = build_X(lam)
        coef, _, _, _ = np.linalg.lstsq(X, y_lnk, rcond=None)
        return np.sum((y_lnk - X @ coef)**2)

    res = minimize(objective, x0=[lam_init], method='Nelder-Mead', options={'maxiter': 10000})
    lam_opt = res.x[0]
    X_final = build_X([lam_opt])
    COEF, _, _, _ = np.linalg.lstsq(X_final, y_lnk, rcond=None)
    R2 = 1 - np.sum((y_lnk - X_final @ COEF)**2) / np.sum((y_lnk - np.mean(y_lnk))**2)

    predictions = []
    for i in range(n_data):
        X_tr = np.delete(X_final, i, axis=0)
        y_tr = np.delete(y_lnk, i)
        coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
        d = data[i]
        gamma_eff = d['gamma_n'] + lam_opt * feat_func(d)
        ln_k = coef[0]*gamma_eff + coef[1]*math.log(d['G']) + coef[2]*math.log(d['theta_D']) + coef[3]*math.log(d['B']) + coef[4]*math.log(d['N']) + coef[5]*math.log(d['V']) + coef[6]
        k_eff = math.exp(ln_k)
        tc_pred = math.sqrt(8 * d['dd0']**2 * k_eff * d['theta_D'] / (9 * LN2))
        err = abs(tc_pred - d['tc']) / d['tc']
        predictions.append({
            'formula': d['formula'], 'cat': d['cat'], 'gl': d['gl'],
            'pairing': d['pairing'], 'j': d['j'], 'tc_pred': tc_pred,
            'tc_exp': d['tc'], 'err': err, 'has_f': d['has_f'],
        })

    errs = np.array([p['err'] for p in predictions])
    is_gl1 = np.array([p['gl'] == 1 and not p['has_f'] for p in predictions])
    is_gl2 = np.array([p['gl'] == 2 for p in predictions])
    is_hf = np.array([p['has_f'] for p in predictions])

    result = {
        'name': name, 'lam': lam_opt, 'R2': R2,
        'errs': errs, 'is_gl1': is_gl1, 'is_gl2': is_gl2, 'is_hf': is_hf,
        'predictions': predictions,
    }
    return result

def run_scheme_dual(name, feat_func1, feat_func2, lam_init):
    """双参数方案: γ_eff = γ_n + λ₁·f₁ + λ₂·f₂"""
    def build_X(lams):
        X = np.zeros((n_data, 7))
        for i, d in enumerate(data):
            gamma_eff = d['gamma_n'] + lams[0] * feat_func1(d) + lams[1] * feat_func2(d)
            X[i, 0] = gamma_eff
            X[i, 1] = math.log(d['G'])
            X[i, 2] = math.log(d['theta_D'])
            X[i, 3] = math.log(d['B'])
            X[i, 4] = math.log(d['N'])
            X[i, 5] = math.log(d['V'])
            X[i, 6] = 1.0
        return X

    def objective(lams):
        X = build_X(lams)
        coef, _, _, _ = np.linalg.lstsq(X, y_lnk, rcond=None)
        return np.sum((y_lnk - X @ coef)**2)

    res = minimize(objective, x0=lam_init, method='Nelder-Mead', options={'maxiter': 20000})
    lam1_opt, lam2_opt = res.x[0], res.x[1]
    X_final = build_X([lam1_opt, lam2_opt])
    COEF, _, _, _ = np.linalg.lstsq(X_final, y_lnk, rcond=None)
    R2 = 1 - np.sum((y_lnk - X_final @ COEF)**2) / np.sum((y_lnk - np.mean(y_lnk))**2)

    predictions = []
    for i in range(n_data):
        X_tr = np.delete(X_final, i, axis=0)
        y_tr = np.delete(y_lnk, i)
        coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
        d = data[i]
        gamma_eff = d['gamma_n'] + lam1_opt * feat_func1(d) + lam2_opt * feat_func2(d)
        ln_k = coef[0]*gamma_eff + coef[1]*math.log(d['G']) + coef[2]*math.log(d['theta_D']) + coef[3]*math.log(d['B']) + coef[4]*math.log(d['N']) + coef[5]*math.log(d['V']) + coef[6]
        k_eff = math.exp(ln_k)
        tc_pred = math.sqrt(8 * d['dd0']**2 * k_eff * d['theta_D'] / (9 * LN2))
        err = abs(tc_pred - d['tc']) / d['tc']
        predictions.append({
            'formula': d['formula'], 'cat': d['cat'], 'gl': d['gl'],
            'pairing': d['pairing'], 'j': d['j'], 'tc_pred': tc_pred,
            'tc_exp': d['tc'], 'err': err, 'has_f': d['has_f'],
        })

    errs = np.array([p['err'] for p in predictions])
    is_gl1 = np.array([p['gl'] == 1 and not p['has_f'] for p in predictions])
    is_gl2 = np.array([p['gl'] == 2 for p in predictions])
    is_hf = np.array([p['has_f'] for p in predictions])

    return {
        'name': name, 'lam1': lam1_opt, 'lam2': lam2_opt, 'R2': R2,
        'errs': errs, 'is_gl1': is_gl1, 'is_gl2': is_gl2, 'is_hf': is_hf,
        'predictions': predictions,
    }

f_casimir = lambda d: d['casimir']
f_zero_gap = lambda d: d['zero_gap']
f_zero_gap_norm = lambda d: d['zero_gap_norm']

print(f"\n运行4个方案...")

res_A = run_scheme("A: j(j+1) Casimir [原方案]", f_casimir, 0.39)
res_B = run_scheme("B: GL(2)零点差 Δγ_f", f_zero_gap, 5.0)
res_C = run_scheme("C: 标准化零点差 Δγ_f/Δγ₁", f_zero_gap_norm, 30.0)
res_D = run_scheme_dual("D: 双参数 j(j+1)+Δγ_f", f_casimir, f_zero_gap, [0.3, 3.0])

print(f"\n{'='*90}")
print("方案对比结果")
print(f"{'='*90}")
print(f"\n{'方案':<35} {'λ':>8} {'R²':>7} {'全部中位%':>10} {'GL2中位%':>9} {'GL2 2倍内%':>11} {'GL2 5倍内%':>10}")
print("-" * 95)

for res in [res_A, res_B, res_C]:
    e_all = res['errs']
    e_gl2 = res['errs'][res['is_gl2']]
    lam_str = f"{res['lam']:.4f}"
    print(f"{res['name']:<35} {lam_str:>8} {res['R2']:>7.4f} {np.median(e_all)*100:>10.1f} {np.median(e_gl2)*100:>9.1f} {np.mean(e_gl2<=1)*100:>11.1f} {np.mean(e_gl2<=4)*100:>10.1f}")

e_all_D = res_D['errs']
e_gl2_D = res_D['errs'][res_D['is_gl2']]
print(f"{res_D['name']:<35} {'见下':>8} {res_D['R2']:>7.4f} {np.median(e_all_D)*100:>10.1f} {np.median(e_gl2_D)*100:>9.1f} {np.mean(e_gl2_D<=1)*100:>11.1f} {np.mean(e_gl2_D<=4)*100:>10.1f}")
print(f"  方案D: λ₁(j(j+1)) = {res_D['lam1']:.4f}, λ₂(Δγ_f) = {res_D['lam2']:.4f}")

print(f"\n{'='*90}")
print("分类别详细精度对比")
print(f"{'='*90}")

cats_order = ['铜氧化物高温超导体', '铁基超导体', '有机超导体', '富勒烯超导体',
              'A15结构金属间化合物', '元素超导体(常压)', '元素超导体(高压)',
              '合金超导体', '其他金属间化合物', '氢化物高压超导体',
              '石墨插层超导体', '其他特殊超导体']

print(f"\n{'类别':<25} {'N':>4} | {'A中位%':>7} {'A 2倍%':>7} | {'B中位%':>7} {'B 2倍%':>7} | {'C中位%':>7} {'C 2倍%':>7} | {'D中位%':>7} {'D 2倍%':>7}")
print("-" * 110)
for cat in cats_order:
    errs_A = [p['err'] for p in res_A['predictions'] if p['cat'] == cat]
    errs_B = [p['err'] for p in res_B['predictions'] if p['cat'] == cat]
    errs_C = [p['err'] for p in res_C['predictions'] if p['cat'] == cat]
    errs_D = [p['err'] for p in res_D['predictions'] if p['cat'] == cat]
    if not errs_A:
        continue
    eA, eB, eC, eD = np.array(errs_A), np.array(errs_B), np.array(errs_C), np.array(errs_D)
    print(f"{cat:<25} {len(eA):>4} | {np.median(eA)*100:>7.1f} {np.mean(eA<=1)*100:>7.0f} | {np.median(eB)*100:>7.1f} {np.mean(eB<=1)*100:>7.0f} | {np.median(eC)*100:>7.1f} {np.mean(eC<=1)*100:>7.0f} | {np.median(eD)*100:>7.1f} {np.mean(eD<=1)*100:>7.0f}")

print(f"\n{'='*90}")
print("GL(2)非常规超导：逐材料对比 (方案A vs 方案B)")
print(f"{'='*90}")
print(f"\n{'材料':<22} {'配对':>4} {'j':>2} {'Tc_exp':>8} | {'A Tc_pred':>10} {'A err%':>7} | {'B Tc_pred':>10} {'B err%':>7} | {'改进%':>7}")
print("-" * 85)

gl2_preds_A = [p for p in res_A['predictions'] if p['gl'] == 2]
gl2_preds_B = {p['formula']: p for p in res_B['predictions'] if p['gl'] == 2}
gl2_preds_A.sort(key=lambda x: x['tc_exp'], reverse=True)

improvements = []
for pA in gl2_preds_A:
    pB = gl2_preds_B[pA['formula']]
    improve = (pA['err'] - pB['err']) / pA['err'] * 100
    improvements.append(improve)
    print(f"{pA['formula']:<22} {pA['pairing']:>4} {pA['j']:>2} {pA['tc_exp']:>8.1f} | {pA['tc_pred']:>10.2f} {pA['err']*100:>7.1f} | {pB['tc_pred']:>10.2f} {pB['err']*100:>7.1f} | {improve:>+7.1f}")

print(f"\n改进统计 (方案B vs 方案A, GL(2)非常规):")
improvements = np.array(improvements)
print(f"  平均改进: {np.mean(improvements):+.1f}%")
print(f"  中位改进: {np.median(improvements):+.1f}%")
print(f"  改进材料数: {np.sum(improvements > 0)}/{len(improvements)}")
print(f"  退步材料数: {np.sum(improvements < 0)}/{len(improvements)}")

print(f"\n{'='*90}")
print("结论")
print(f"{'='*90}")
e_gl2_A = res_A['errs'][res_A['is_gl2']]
e_gl2_B = res_B['errs'][res_B['is_gl2']]
e_gl2_C = res_C['errs'][res_C['is_gl2']]
e_gl2_D = res_D['errs'][res_D['is_gl2']]
e_all_A = res_A['errs']
e_all_B = res_B['errs']

print(f"""
GL(2)非常规超导精度 (LOOCV, {sum(res_A['is_gl2'])}个材料):
  方案A (j(j+1) Casimir):     中位{np.median(e_gl2_A)*100:.1f}%, 2倍内{np.mean(e_gl2_A<=1)*100:.0f}%, 5倍内{np.mean(e_gl2_A<=4)*100:.0f}%
  方案B (GL(2)零点差):        中位{np.median(e_gl2_B)*100:.1f}%, 2倍内{np.mean(e_gl2_B<=1)*100:.0f}%, 5倍内{np.mean(e_gl2_B<=4)*100:.0f}%
  方案C (标准化零点差):       中位{np.median(e_gl2_C)*100:.1f}%, 2倍内{np.mean(e_gl2_C<=1)*100:.0f}%, 5倍内{np.mean(e_gl2_C<=4)*100:.0f}%
  方案D (双参数):             中位{np.median(e_gl2_D)*100:.1f}%, 2倍内{np.mean(e_gl2_D<=1)*100:.0f}%, 5倍内{np.mean(e_gl2_D<=4)*100:.0f}%

全部材料精度 (LOOCV, {n_data}个材料):
  方案A: 中位{np.median(e_all_A)*100:.1f}%, 2倍内{np.mean(e_all_A<=1)*100:.0f}%, 5倍内{np.mean(e_all_A<=4)*100:.0f}%
  方案B: 中位{np.median(e_all_B)*100:.1f}%, 2倍内{np.mean(e_all_B<=1)*100:.0f}%, 5倍内{np.mean(e_all_B<=4)*100:.0f}%

关键比值:
  j(j+1)比值 d/p = {6/2:.4f}
  GL(2)零点差比值 d/p = {GL2_ZERO_GAP_D/GL2_ZERO_GAP_P:.4f}
  → 若方案B优于方案A: GL(2)零点差是更基本的参数, j(j+1)是其 semiclassical 近似
  → 若方案D优于方案A和B: 两种参数携带独立信息
""")