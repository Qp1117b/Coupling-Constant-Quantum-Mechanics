"""
本征值交叉实现：GL(2)零点差的正确进入方式

理论:
  当前框架: γ_eff = γ_n + λ·(修正)  [线性叠加]
  正确机制: 本征值交叉 Tc = (E₂-E₁)/(S₂-S₁)
    E₁ ~ γ₁²  (GL(1)基态)
    E₂ ~ (γ₂ + α·Δγ_f)²  (GL(2)态, 含零点差修正)
    → GL(2)零点差以非线性方式进入

测试方案:
  I: γ_eff = γ_n + λ·(Δγ_f)²     [平方修正]
  J: γ_eff = γ_n·(1 + λ·Δγ_f)    [乘法修正]
  K: γ_eff = γ_n + λ·Δγ_f/γ_n    [相对修正]
  L: γ_eff = γ_n + λ·(Δγ_f)²/γ_n [平方相对]
  M: ln(K_eff) = a·γ_n² + b·(γ₂+α·Δγ_f)² - c·γ₁² + ... [直接交叉]
  N: γ_eff = γ_n + λ·Δγ_f·γ_n    [耦合修正]
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

GAMMA1 = 14.134725
GAMMA2 = 21.022040
GL1_ZERO_GAP = GAMMA2 - GAMMA1
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
        k_eff = tc**2 * 9 * LN2 / (8 * mp['dd0']**2 * mp['theta_D'])
        data.append({**mp, 'cat': cat, 'tc': tc, 'k_eff': k_eff,
                     'gl': gl, 'j': j, 'casimir': casimir,
                     'pairing': pairing, 'zero_gap': zero_gap,
                     'gamma_n': gamma_n, 'n_mode': n_mode})

n_data = len(data)
y_lnk = np.array([math.log(d['k_eff']) for d in data])

def run_scheme(name, gamma_eff_func, lam_init):
    """gamma_eff_func(d, lam)返回γ_eff"""
    def build_X(lam):
        X = np.zeros((n_data, 7))
        for i, d in enumerate(data):
            gamma_eff = gamma_eff_func(d, lam[0])
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
        gamma_eff = gamma_eff_func(d, lam_opt)
        ln_k = coef[0]*gamma_eff + coef[1]*math.log(d['G']) + coef[2]*math.log(d['theta_D']) + coef[3]*math.log(d['B']) + coef[4]*math.log(d['N']) + coef[5]*math.log(d['V']) + coef[6]
        k_eff = math.exp(ln_k)
        tc_pred = math.sqrt(8 * d['dd0']**2 * k_eff * d['theta_D'] / (9 * LN2))
        err = abs(tc_pred - d['tc']) / d['tc']
        predictions.append({
            'formula': d['formula'], 'cat': d['cat'], 'gl': d['gl'],
            'pairing': d['pairing'], 'tc_pred': tc_pred,
            'tc_exp': d['tc'], 'err': err, 'has_f': d['has_f'],
        })

    errs = np.array([p['err'] for p in predictions])
    is_gl2 = np.array([p['gl'] == 2 for p in predictions])
    return {'name': name, 'lam': lam_opt, 'R2': R2,
            'errs': errs, 'is_gl2': is_gl2, 'predictions': predictions}

g_A = lambda d, lam: d['gamma_n'] + lam * d['casimir']
g_B = lambda d, lam: d['gamma_n'] + lam * d['zero_gap']
g_I = lambda d, lam: d['gamma_n'] + lam * d['zero_gap']**2
g_J = lambda d, lam: d['gamma_n'] * (1 + lam * d['zero_gap'])
g_K = lambda d, lam: d['gamma_n'] + lam * d['zero_gap'] / d['gamma_n']
g_L = lambda d, lam: d['gamma_n'] + lam * d['zero_gap']**2 / d['gamma_n']
g_N = lambda d, lam: d['gamma_n'] + lam * d['zero_gap'] * d['gamma_n']
g_O = lambda d, lam: d['gamma_n'] + lam * d['zero_gap'] * d['casimir']

schemes = [
    ("A: 线性j(j+1) [基准]", g_A, 0.39),
    ("B: 线性Δγ_f", g_B, 5.0),
    ("I: 平方(Δγ_f)²", g_I, 50.0),
    ("J: 乘法 γ_n·(1+λ·Δγ_f)", g_J, 1.0),
    ("K: 相对 Δγ_f/γ_n", g_K, 100.0),
    ("L: 平方相对 (Δγ_f)²/γ_n", g_L, 500.0),
    ("N: 耦合 Δγ_f·γ_n", g_N, 0.05),
    ("O: 交叉 Δγ_f·j(j+1)", g_O, 1.0),
]

print("=" * 95)
print("非线性本征值交叉方案：GL(2)零点差的正确进入方式")
print("=" * 95)
print(f"\n材料数: {n_data}")
print(f"GL(2) d波零点差 = {GL2_ZERO_GAP_D}, p波零点差 = {GL2_ZERO_GAP_P}")
print(f"零点差比值 d/p = {GL2_ZERO_GAP_D/GL2_ZERO_GAP_P:.4f} (vs j(j+1)比值 = 3.0)")

results = {}
for name, g_func, lam_init in schemes:
    res = run_scheme(name, g_func, lam_init)
    results[name] = res

print(f"\n{'='*95}")
print("方案对比结果")
print(f"{'='*95}")
print(f"\n{'方案':<30} {'λ':>10} {'R²':>7} {'全部中位%':>10} {'GL2中位%':>9} {'GL2 2倍%':>8} {'GL2 5倍%':>8}")
print("-" * 85)
for name, _, _ in schemes:
    res = results[name]
    e_all = res['errs']
    e_gl2 = res['errs'][res['is_gl2']]
    print(f"{name:<30} {res['lam']:>10.4f} {res['R2']:>7.4f} {np.median(e_all)*100:>10.1f} {np.median(e_gl2)*100:>9.1f} {np.mean(e_gl2<=1)*100:>8.0f} {np.mean(e_gl2<=4)*100:>8.0f}")

print(f"\n{'='*95}")
print("分类别精度 (铜氧化物 vs 铁基)")
print(f"{'='*95}")
print(f"\n{'方案':<30} | {'铜氧化物中位%':>14} {'铜氧化物2倍%':>13} | {'铁基中位%':>10} {'铁基2倍%':>9}")
print("-" * 85)
for name, _, _ in schemes:
    res = results[name]
    e_cup = np.array([p['err'] for p in res['predictions'] if p['cat'] == '铜氧化物高温超导体'])
    e_fe = np.array([p['err'] for p in res['predictions'] if p['cat'] == '铁基超导体'])
    print(f"{name:<30} | {np.median(e_cup)*100:>14.1f} {np.mean(e_cup<=1)*100:>13.0f} | {np.median(e_fe)*100:>10.1f} {np.mean(e_fe<=1)*100:>9.0f}")

print(f"\n{'='*95}")
print("本征值交叉直接实现")
print(f"{'='*95}")

def run_crossing_scheme(name, lam_init):
    """直接本征值交叉: ln(K_eff) = a·γ₁² + b·(γ₂+λ·Δγ_f)² + p·ln(G) + ..."""
    def build_X(lam):
        X = np.zeros((n_data, 8))
        for i, d in enumerate(data):
            gamma2_eff = GAMMA2 + lam[0] * d['zero_gap']
            X[i, 0] = GAMMA1**2
            X[i, 1] = gamma2_eff**2
            X[i, 2] = math.log(d['G'])
            X[i, 3] = math.log(d['theta_D'])
            X[i, 4] = math.log(d['B'])
            X[i, 5] = math.log(d['N'])
            X[i, 6] = math.log(d['V'])
            X[i, 7] = 1.0
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
        gamma2_eff = GAMMA2 + lam_opt * d['zero_gap']
        ln_k = coef[0]*GAMMA1**2 + coef[1]*gamma2_eff**2 + coef[2]*math.log(d['G']) + coef[3]*math.log(d['theta_D']) + coef[4]*math.log(d['B']) + coef[5]*math.log(d['N']) + coef[6]*math.log(d['V']) + coef[7]
        k_eff = math.exp(ln_k)
        tc_pred = math.sqrt(8 * d['dd0']**2 * k_eff * d['theta_D'] / (9 * LN2))
        err = abs(tc_pred - d['tc']) / d['tc']
        predictions.append({
            'formula': d['formula'], 'cat': d['cat'], 'gl': d['gl'],
            'pairing': d['pairing'], 'tc_pred': tc_pred,
            'tc_exp': d['tc'], 'err': err, 'has_f': d['has_f'],
        })

    errs = np.array([p['err'] for p in predictions])
    is_gl2 = np.array([p['gl'] == 2 for p in predictions])
    return {'name': name, 'lam': lam_opt, 'R2': R2,
            'errs': errs, 'is_gl2': is_gl2, 'predictions': predictions}

res_M = run_crossing_scheme("M: 直接交叉 γ₁²+(γ₂+λ·Δγ_f)²", 1.0)
e_all_M = res_M['errs']
e_gl2_M = res_M['errs'][res_M['is_gl2']]
e_cup_M = np.array([p['err'] for p in res_M['predictions'] if p['cat'] == '铜氧化物高温超导体'])
e_fe_M = np.array([p['err'] for p in res_M['predictions'] if p['cat'] == '铁基超导体'])

print(f"\n方案M: ln(K_eff) = a·γ₁² + b·(γ₂+λ·Δγ_f)² + p·ln(G) + ...")
print(f"  λ = {res_M['lam']:.4f}, R² = {res_M['R2']:.4f}")
print(f"  全部中位{np.median(e_all_M)*100:.1f}%, GL2中位{np.median(e_gl2_M)*100:.1f}%, 2倍内{np.mean(e_gl2_M<=1)*100:.0f}%, 5倍内{np.mean(e_gl2_M<=4)*100:.0f}%")
print(f"  铜氧化物中位{np.median(e_cup_M)*100:.1f}%, 铁基中位{np.median(e_fe_M)*100:.1f}%")

print(f"\n{'='*95}")
print("最终结论")
print(f"{'='*95}")

best_gl2 = min(schemes, key=lambda s: np.median(results[s[0]]['errs'][results[s[0]]['is_gl2']]))
best_res = results[best_gl2[0]]
e_best_gl2 = best_res['errs'][best_res['is_gl2']]
e_A_gl2 = results["A: 线性j(j+1) [基准]"]['errs'][results["A: 线性j(j+1) [基准]"]['is_gl2']]

print(f"""
关键发现:
  1. 所有方案在当前框架下精度相近 (GL2中位~35-36%)
  2. 最佳方案: {best_gl2[0]}
     GL2中位{np.median(e_best_gl2)*100:.1f}% (vs 基准{np.median(e_A_gl2)*100:.1f}%)
  3. 非线性方案未能显著提升精度

根本原因:
  - d波/p波零点差差异极小: Δγ_d-Δγ_p = {GL2_ZERO_GAP_D-GL2_ZERO_GAP_P:.3f}
  - γ_n差异远大于零点差差异: Δγ_n(铜氧-铁基) = {RIEMANN_ZEROS[8]-RIEMANN_ZEROS[7]:.3f}
  - 在线性回归框架中, 零点差的微小差异被γ_n的大差异淹没

理论意义:
  - C_f = 0 (rank=0) 理论正确, 但意味着GL(2)零点差不通过谱量子进入Tc
  - GL(2)零点差应通过本征值交叉进入, 但需要更精细的物理模型
  - 当前框架的瓶颈不在GL(2)修正项的形式, 而在整体Tc公式的结构
  - 需要从底空间几何直接计算配对对称性, 而非依赖类别映射
""")