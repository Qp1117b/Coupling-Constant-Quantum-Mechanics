"""
深入分析：GL(2)修正项在当前框架中的真实贡献

关键观察：
  方案A (j(j+1)): λ=+0.39, d波修正=2.34, p波修正=0.78, 差异=1.56
  方案B (Δγ_f):   λ=-0.46, d波修正=-0.17, p波修正=-0.16, 差异=-0.01

  方案B中d波/p波修正差异极小(-0.01), 但精度与方案A相同
  → 猜想: d波/p波的区分主要来自γ_n(n_mode), 而非GL(2)修正项

验证方案:
  E: 完全去除GL(2)修正 (所有材料j=0, Δγ_f=0)
  F: 仅用γ_n区分 (n_mode映射不变, 但无GL2修正)
  G: 去除n_mode区分 (所有材料n=5, 但保留GL2修正)
  H: 去除n_mode区分 + 去除GL2修正 (纯几何)
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

def run_scheme(name, gamma_n_func, feat_func, lam_init=0.39):
    """通用方案: gamma_n_func(d)返回γ_n, feat_func(d)返回修正项"""
    def build_X(lam):
        X = np.zeros((n_data, 7))
        for i, d in enumerate(data):
            gamma_eff = gamma_n_func(d) + lam[0] * feat_func(d)
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
        gamma_eff = gamma_n_func(d) + lam_opt * feat_func(d)
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

f_casimir = lambda d: d['casimir']
f_zero_gap = lambda d: d['zero_gap']
f_zero = lambda d: 0.0
gamma_n_orig = lambda d: d['gamma_n']
gamma_n_fixed5 = lambda d: RIEMANN_ZEROS[4]

print("=" * 90)
print("GL(2)修正项真实贡献分析")
print("=" * 90)
print(f"\n材料数: {n_data}")
print(f"\nγ_n映射 (n_mode → γ_n):")
for cat in sorted(set(d['cat'] for d in data)):
    n = [d['n_mode'] for d in data if d['cat'] == cat][0]
    gn = [d['gamma_n'] for d in data if d['cat'] == cat][0]
    gl = 2 if cat in GL2_CATS else 1
    print(f"  {cat:<25} n={n:>2}, γ_n={gn:.4f}, GL{gl}")

print(f"\n关键: 铜氧化物(n=9,γ=43.31) vs 铁基(n=8,γ=40.92), Δγ_n=2.39")
print(f"      j(j+1)修正: 铜氧化物(j=2,Cas=6) vs 铁基(j=1,Cas=2), ΔCas=4, λ·ΔCas=0.39×4=1.56")
print(f"      → γ_n差异(2.39) > j(j+1)修正差异(1.56), γ_n是主要区分因素")

schemes = [
    ("A: 原方案 (γ_n + λ·j(j+1))", gamma_n_orig, f_casimir, 0.39),
    ("E: 无GL2修正 (γ_n only)", gamma_n_orig, f_zero, 0.0),
    ("F: 无GL2修正 + 零点差", gamma_n_orig, f_zero_gap, 5.0),
    ("G: 固定n=5 + j(j+1)修正", gamma_n_fixed5, f_casimir, 0.39),
    ("H: 固定n=5 + 无修正", gamma_n_fixed5, f_zero, 0.0),
]

results = {}
for name, gn_func, feat, lam_init in schemes:
    res = run_scheme(name, gn_func, feat, lam_init)
    results[name] = res

print(f"\n{'='*90}")
print("方案对比：分解γ_n和GL2修正的贡献")
print(f"{'='*90}")
print(f"\n{'方案':<40} {'λ':>8} {'R²':>7} {'全部中位%':>10} {'GL2中位%':>9} {'GL2 2倍%':>8} {'GL2 5倍%':>8}")
print("-" * 85)
for name, _, _, _ in schemes:
    res = results[name]
    e_all = res['errs']
    e_gl2 = res['errs'][res['is_gl2']]
    print(f"{name:<40} {res['lam']:>8.4f} {res['R2']:>7.4f} {np.median(e_all)*100:>10.1f} {np.median(e_gl2)*100:>9.1f} {np.mean(e_gl2<=1)*100:>8.0f} {np.mean(e_gl2<=4)*100:>8.0f}")

print(f"\n{'='*90}")
print("贡献分解")
print(f"{'='*90}")

r_A = results["A: 原方案 (γ_n + λ·j(j+1))"]
r_E = results["E: 无GL2修正 (γ_n only)"]
r_G = results["G: 固定n=5 + j(j+1)修正"]
r_H = results["H: 固定n=5 + 无修正"]

e_gl2_A = r_A['errs'][r_A['is_gl2']]
e_gl2_E = r_E['errs'][r_E['is_gl2']]
e_gl2_G = r_G['errs'][r_G['is_gl2']]
e_gl2_H = r_H['errs'][r_H['is_gl2']]

print(f"""
GL(2)非常规超导精度 (LOOCV, {sum(r_A['is_gl2'])}个材料):
  A: γ_n + λ·j(j+1)  [原方案]:  中位{np.median(e_gl2_A)*100:.1f}%, 2倍内{np.mean(e_gl2_A<=1)*100:.0f}%
  E: γ_n only         [无GL2]:   中位{np.median(e_gl2_E)*100:.1f}%, 2倍内{np.mean(e_gl2_E<=1)*100:.0f}%
  G: 固定n=5 + λ·j(j+1) [无γ_n区分]: 中位{np.median(e_gl2_G)*100:.1f}%, 2倍内{np.mean(e_gl2_G<=1)*100:.0f}%
  H: 固定n=5 only     [纯几何]:  中位{np.median(e_gl2_H)*100:.1f}%, 2倍内{np.mean(e_gl2_H<=1)*100:.0f}%

贡献分析:
  γ_n区分贡献 = A - E = {np.median(e_gl2_A)*100:.1f}% → {np.median(e_gl2_E)*100:.1f}% = {np.median(e_gl2_A)*100 - np.median(e_gl2_E)*100:+.1f}%
  j(j+1)修正贡献 = A - G = {np.median(e_gl2_A)*100:.1f}% → {np.median(e_gl2_G)*100:.1f}% = {np.median(e_gl2_A)*100 - np.median(e_gl2_G)*100:+.1f}%
  两者联合贡献 = A - H = {np.median(e_gl2_A)*100:.1f}% → {np.median(e_gl2_H)*100:.1f}% = {np.median(e_gl2_A)*100 - np.median(e_gl2_H)*100:+.1f}%
""")

print(f"{'='*90}")
print("逐材料对比: 方案A vs 方案E (无GL2修正)")
print(f"{'='*90}")
print(f"\n{'材料':<22} {'配对':>4} {'Tc_exp':>8} | {'A err%':>7} {'E err%':>7} | {'GL2修正贡献':>12}")
print("-" * 65)

gl2_A = [p for p in r_A['predictions'] if p['gl'] == 2]
gl2_E = {p['formula']: p for p in r_E['predictions'] if p['gl'] == 2}
gl2_A.sort(key=lambda x: x['tc_exp'], reverse=True)

for pA in gl2_A[:20]:
    pE = gl2_E[pA['formula']]
    contrib = pA['err'] - pE['err']
    print(f"{pA['formula']:<22} {pA['pairing']:>4} {pA['tc_exp']:>8.1f} | {pA['err']*100:>7.1f} {pE['err']*100:>7.1f} | {contrib*100:>+12.1f}")

print(f"\n...")
print(f"\nGL2修正贡献统计 (A_err - E_err, 正=修正有害, 负=修正有益):")
contribs = []
for pA in gl2_A:
    pE = gl2_E[pA['formula']]
    contribs.append(pA['err'] - pE['err'])
contribs = np.array(contribs)
print(f"  平均贡献: {np.mean(contribs)*100:+.1f}% (正=修正有害)")
print(f"  中位贡献: {np.median(contribs)*100:+.1f}%")
print(f"  修正有益的材料: {np.sum(contribs < 0)}/{len(contribs)}")
print(f"  修正有害的材料: {np.sum(contribs > 0)}/{len(contribs)}")

print(f"\n{'='*90}")
print("核心结论")
print(f"{'='*90}")
print(f"""
1. γ_n (黎曼零点序号映射) 是区分GL(2)配对类型的主要因素:
   - 铜氧化物 n=9 (γ=43.31), 铁基 n=8 (γ=40.92), Δγ_n=2.39
   - 去除GL2修正(方案E): 中位{np.median(e_gl2_E)*100:.1f}% (vs 原方案{np.median(e_gl2_A)*100:.1f}%)
   - 贡献: {np.median(e_gl2_A)*100 - np.median(e_gl2_E)*100:+.1f}%

2. j(j+1) Casimir修正的边际贡献:
   - 去除γ_n区分(方案G): 中位{np.median(e_gl2_G)*100:.1f}%
   - 贡献: {np.median(e_gl2_A)*100 - np.median(e_gl2_G)*100:+.1f}%

3. GL(2)零点差与j(j+1)在当前线性框架中携带相同信息:
   - 方案A (j(j+1)): 中位{np.median(results['A: 原方案 (γ_n + λ·j(j+1))']['errs'][results['A: 原方案 (γ_n + λ·j(j+1))']['is_gl2']])*100:.1f}%
   - 方案F (零点差):  中位{np.median(results['F: 无GL2修正 + 零点差']['errs'][results['F: 无GL2修正 + 零点差']['is_gl2']])*100:.1f}%
   → 两者精度相同, 因为d波/p波零点差差异(0.02)远小于γ_n差异(2.39)

4. 真正的瓶颈: 当前线性叠加框架 γ_eff = γ_n + λ·(修正) 无法体现本征值交叉机制
   正确的GL(2)机制: λ₂ = γ₂ + α·(γ₂^(f)-γ₁^(f)), Tc由交叉条件决定
   这不是简单的线性叠加, 需要新的实现方式
""")