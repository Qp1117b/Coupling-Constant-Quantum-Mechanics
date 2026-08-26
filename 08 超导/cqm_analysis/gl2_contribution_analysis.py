"""
GL(2) 贡献分析：5路径合并分析

路径1: GL(1)/GL(2)分层分析 — 常规超导(黎曼零点) vs 非常规(模形式零点)
路径2: 贡献分解 — γ_n和GL2修正项的真实贡献分析
路径3: 交叉非线性 — GL(2)零点差的非线性进入方式
路径4: 同步算符 — GL(2)同步算符的第一性推导
路径5: 零点差vs Casimir — GL(2)零点差与j(j+1) Casimir修正对比
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework')
from atom_db import ATOM_DB, atom_db

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

MODULAR_ZEROS = [9.222379, 13.907111, 17.442776, 19.656513, 22.184253,
                 23.744231, 26.110258, 27.849594, 29.913455, 31.683538]

GL1_ZERO_GAP = 21.022040 - 14.134725
GL2_ZERO_GAP_D = 0.367
GL2_ZERO_GAP_P = 0.346
GAMMA1 = 14.134725
GAMMA2 = 21.022040

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
CAT_TO_SPIN_J = {
    '元素超导体(常压)': 0, '元素超导体(高压)': 0, 'A15结构金属间化合物': 0,
    '合金超导体': 0, '其他金属间化合物': 0, '氢化物高压超导体': 0,
    '石墨插层超导体': 0, '其他特殊超导体': 0,
    '铜氧化物高温超导体': 2, '铁基超导体': 1, '有机超导体': 1, '富勒烯超导体': 1,
}

CAT_TO_N_GL1_FIXED = {
    '石墨插层超导体': 1, 'A15结构金属间化合物': 7,
    '元素超导体(常压)': 5, '元素超导体(高压)': 6,
    '其他金属间化合物': 4, '合金超导体': 4,
    '氢化物高压超导体': 10, '其他特殊超导体': 5,
}
CAT_TO_N_GL2_FIXED = {
    '有机超导体': 3, '富勒烯超导体': 2, '铁基超导体': 5, '铜氧化物高温超导体': 7,
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
    f_corr = 1.0 - 0.3 * (1.0 - 1.0 / n_atoms)
    edge_sum = 0
    els = list(atoms.keys())
    for i in range(len(els)):
        for j in range(i + 1, len(els)):
            mi = atoms[els[i]] * ATOM_DB[els[i]][0] * AMU
            mj = atoms[els[j]] * ATOM_DB[els[j]][0] * AMU
            edge_sum += (1.0 / mi + 1.0 / mj)
    if not edge_sum:
        mi = total_m * AMU / n_atoms
        edge_sum = (n_atoms * (n_atoms - 1) / 2) * 2.0 / mi
    G = (1.0 / l) * math.sqrt((1.0 - f_corr) * edge_sum)
    omega_d = theta_d * KB / HBAR
    dd0_sq = (C2 / l**2) * (3 * HBAR / (4 * omega_d)) * (1 - f_corr) * edge_sum
    dd0 = math.sqrt(abs(dd0_sq))
    B_est = total_m * theta_d**2 * KB / V_cell * 1e-3
    return {'l': l, 'G': G, 'dd0': dd0, 'tD': theta_d,
            'M': total_m, 'Z': total_z, 'V': V_cell,
            'n_atoms': n_atoms, 'B': B_est}


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
    f_corr = 1.0 - 0.3 * (1.0 - 1.0 / n_atoms)
    edge_sum = 0
    els = list(atoms.keys())
    for i in range(len(els)):
        for j in range(i + 1, len(els)):
            mi = atoms[els[i]] * ATOM_DB[els[i]][0] * AMU
            mj = atoms[els[j]] * ATOM_DB[els[j]][0] * AMU
            edge_sum += (1.0 / mi + 1.0 / mj)
    if not edge_sum:
        mi = total_m * AMU / n_atoms
        edge_sum = (n_atoms * (n_atoms - 1) / 2) * 2.0 / mi
    G = (1.0 / l) * math.sqrt((1.0 - f_corr) * edge_sum)
    omega_d = theta_d * KB / HBAR
    dd0_sq = (C2 / l**2) * (3 * HBAR / (4 * omega_d)) * (1 - f_corr) * edge_sum
    dd0 = math.sqrt(abs(dd0_sq))
    B_est = total_m * theta_d**2 * KB / V_cell * 1e-3
    has_f = any(el in HEAVY_FERMION_ELEMENTS for el in atoms)
    return {'formula': formula, 'M': total_m, 'Z': total_z, 'N': n_atoms,
            'l': l, 'theta_D': theta_d, 'V': V_cell,
            'G': G, 'dd0': dd0, 'B': B_est, 'has_f': has_f}


def calc_tc_from_lnk(ln_k, d):
    k_eff = math.exp(ln_k)
    return math.sqrt(8 * d['dd0']**2 * k_eff * d['tD'] / (9 * LN2))


def get_feats(d):
    return np.array([
        math.log(d['G']), math.log(d['tD']), math.log(d['dd0']),
        math.log(d['M']), math.log(d['Z']) if d['Z'] > 0 else 0,
        math.log(d['V']), math.log(d['n_atoms']),
        math.log(d['B']) if d['B'] > 0 else 0,
        1.0 / d['tD'], math.log(d['tD'])**2,
        math.log(d['tD'] / d['dd0']) if d['dd0'] > 0 else 0,
    ])


# =====================================================
# 路径1: GL(1)/GL(2)分层分析
# =====================================================

def path1_gl2_layered():
    print("\n" + "=" * 80)
    print("路径1: GL(1)/GL(2)分层分析")
    print("=" * 80)

    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.model_selection import LeaveOneOut

    FEAT_NAMES = ['ln(G)', 'ln(θ_D)', 'ln(Δδ₀)', 'ln(M)', 'ln(Z)',
                  'ln(V)', 'ln(N)', 'ln(B)', '1/θ_D', 'ln²(θ_D)', 'ln(θ_D/Δδ₀)']

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
            data.append({'cat': cat, 'tc': tc, 'k_eff': k_eff, 'gl': gl_layer, **mp})

    n_data = len(data)
    categories = sorted(set(d['cat'] for d in data))
    cat_idx = {c: i for i, c in enumerate(categories)}
    n_cats = len(categories)
    y_lnk = np.array([math.log(d['k_eff']) for d in data])
    y_lntc = np.array([math.log(d['tc']) for d in data])
    X_geom = np.array([get_feats(d) for d in data])

    print(f"加载 {n_data} 个材料")
    gl1_data = [d for d in data if d['gl'] == 1]
    gl2_data = [d for d in data if d['gl'] == 2]
    print(f"GL(1)常规超导: {len(gl1_data)} 个")
    print(f"GL(2)非常规超导: {len(gl2_data)} 个")

    print("\n1.1 GL(1) vs GL(2) 的ln(K_eff)分布")
    lnk_gl1 = [math.log(d['k_eff']) for d in gl1_data]
    lnk_gl2 = [math.log(d['k_eff']) for d in gl2_data]
    print(f"GL(1): 均值={np.mean(lnk_gl1):.2f}, 范围=[{min(lnk_gl1):.2f}, {max(lnk_gl1):.2f}]")
    print(f"GL(2): 均值={np.mean(lnk_gl2):.2f}, 范围=[{min(lnk_gl2):.2f}, {max(lnk_gl2):.2f}]")

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

    print("\n1.2 GL(1)/GL(2)分别联合优化")
    res_gl1 = joint_optimize(gl1_data, "GL(1)常规超导")
    res_gl2 = joint_optimize(gl2_data, "GL(2)非常规超导")

    print("\n1.3 GL分层one-hot模型")
    for d in data:
        if d['gl'] == 1:
            n = CAT_TO_N_GL1_FIXED.get(d['cat'], 5)
            d['gamma'] = RIEMANN_ZEROS[n - 1]
        elif d['gl'] == 2:
            n = CAT_TO_N_GL2_FIXED.get(d['cat'], 3)
            d['gamma'] = MODULAR_ZEROS[n - 1]
        else:
            d['gamma'] = RIEMANN_ZEROS[4]

    err_gl = []
    for i in range(n_data):
        train = [j for j in range(n_data) if j != i]
        X_tr = np.zeros((len(train), 5))
        y_tr = np.zeros(len(train))
        for j, idx in enumerate(train):
            d = data[idx]
            X_tr[j, 0] = d['gamma'] if d['gl'] == 1 else 0
            X_tr[j, 1] = d['gamma'] if d['gl'] == 2 else 0
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
    print(f"GL分层γ(黎曼+模形式) LOOCV: 中位{np.median(err_gl)*100:.0f}%, 2倍内{np.mean(err_gl<=1)*100:.0f}%, 5倍内{np.mean(err_gl<=4)*100:.0f}%")

    print("\n1.4 GBR + GL分层特征")
    X_gl_feat = np.zeros((n_data, len(FEAT_NAMES) + 2))
    for i, d in enumerate(data):
        X_gl_feat[i, :len(FEAT_NAMES)] = get_feats(d)
        X_gl_feat[i, len(FEAT_NAMES)] = 1.0 if d['gl'] == 1 else 0.0
        X_gl_feat[i, len(FEAT_NAMES) + 1] = 1.0 if d['gl'] == 2 else 0.0

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

    methods = []
    if res_gl1: methods.append(("GL(1)单独优化", res_gl1['err']))
    if res_gl2: methods.append(("GL(2)单独优化", res_gl2['err']))
    methods.append(("GL分层γ", err_gl))
    methods.append(("GBR+GL指示特征", err_gbr_gl))
    print(f"\n全方法对比:")
    print(f"{'方法':<55} {'中位%':>6} {'2倍%':>6} {'5倍%':>6}")
    for name, err in methods:
        print(f"{name:<55} {np.median(err)*100:>6.0f} {np.mean(err<=1)*100:>6.0f} {np.mean(err<=4)*100:>6.0f}")


# =====================================================
# 路径2: 贡献分解
# =====================================================

def path2_contribution_decomposition():
    print("\n" + "=" * 80)
    print("路径2: GL(2)修正项真实贡献分析")
    print("=" * 80)

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
                n_mode = 1; j = 0; pairing = 's'
            else:
                n_mode = CAT_TO_N.get(cat, 5)
            gamma_n = RIEMANN_ZEROS[n_mode - 1]
            casimir = j * (j + 1)
            zero_gap = GL2_ZERO_GAP_D if pairing == 'd' else (GL2_ZERO_GAP_P if pairing == 'p' else 0.0)
            k_eff = tc**2 * 9 * LN2 / (8 * mp['dd0']**2 * mp['theta_D'])
            data.append({**mp, 'cat': cat, 'tc': tc, 'k_eff': k_eff,
                         'gl': gl, 'j': j, 'casimir': casimir,
                         'pairing': pairing, 'zero_gap': zero_gap,
                         'gamma_n': gamma_n, 'n_mode': n_mode})

    n_data = len(data)
    y_lnk = np.array([math.log(d['k_eff']) for d in data])

    def run_scheme(name, gamma_n_func, feat_func, lam_init=0.39):
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
            predictions.append({'formula': d['formula'], 'cat': d['cat'], 'gl': d['gl'],
                                'tc_pred': tc_pred, 'tc_exp': d['tc'], 'err': err})
        errs = np.array([p['err'] for p in predictions])
        is_gl2 = np.array([p['gl'] == 2 for p in predictions])
        return {'name': name, 'lam': lam_opt, 'R2': R2, 'errs': errs, 'is_gl2': is_gl2, 'predictions': predictions}

    f_casimir = lambda d: d['casimir']
    f_zero_gap = lambda d: d['zero_gap']
    f_zero = lambda d: 0.0
    gamma_n_orig = lambda d: d['gamma_n']
    gamma_n_fixed5 = lambda d: RIEMANN_ZEROS[4]

    schemes = [
        ("A: 原方案 (γ_n + λ·j(j+1))", gamma_n_orig, f_casimir, 0.39),
        ("E: 无GL2修正 (γ_n only)", gamma_n_orig, f_zero, 0.0),
        ("F: 无GL2修正 + 零点差", gamma_n_orig, f_zero_gap, 5.0),
        ("G: 固定n=5 + j(j+1)修正", gamma_n_fixed5, f_casimir, 0.39),
        ("H: 固定n=5 + 无修正", gamma_n_fixed5, f_zero, 0.0),
    ]

    print(f"材料数: {n_data}")
    results = {}
    for name, gn_func, feat, lam_init in schemes:
        res = run_scheme(name, gn_func, feat, lam_init)
        results[name] = res

    print(f"\n方案对比：分解γ_n和GL2修正的贡献")
    print(f"{'方案':<40} {'λ':>8} {'R²':>7} {'全部中位%':>10} {'GL2中位%':>9} {'GL2 2倍%':>8} {'GL2 5倍%':>8}")
    print("-" * 85)
    for name, _, _, _ in schemes:
        res = results[name]
        e_all = res['errs']; e_gl2 = res['errs'][res['is_gl2']]
        print(f"{name:<40} {res['lam']:>8.4f} {res['R2']:>7.4f} {np.median(e_all)*100:>10.1f} {np.median(e_gl2)*100:>9.1f} {np.mean(e_gl2<=1)*100:>8.0f} {np.mean(e_gl2<=4)*100:>8.0f}")

    r_A = results["A: 原方案 (γ_n + λ·j(j+1))"]
    r_E = results["E: 无GL2修正 (γ_n only)"]
    print(f"\n核心结论: j(j+1)贡献 = {np.median(r_A['errs'][r_A['is_gl2']])*100 - np.median(r_E['errs'][r_E['is_gl2']])*100:+.1f}%")


# =====================================================
# 路径3: 交叉非线性
# =====================================================

def path3_crossing_nonlinear():
    print("\n" + "=" * 80)
    print("路径3: 本征值交叉实现——GL(2)零点差的非线性进入方式")
    print("=" * 80)

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
                n_mode = 1; j = 0; pairing = 's'
            else:
                n_mode = CAT_TO_N.get(cat, 5)
            gamma_n = RIEMANN_ZEROS[n_mode - 1]
            casimir = j * (j + 1)
            zero_gap = GL2_ZERO_GAP_D if pairing == 'd' else (GL2_ZERO_GAP_P if pairing == 'p' else 0.0)
            k_eff = tc**2 * 9 * LN2 / (8 * mp['dd0']**2 * mp['theta_D'])
            data.append({**mp, 'cat': cat, 'tc': tc, 'k_eff': k_eff,
                         'gl': gl, 'j': j, 'casimir': casimir,
                         'pairing': pairing, 'zero_gap': zero_gap,
                         'gamma_n': gamma_n, 'n_mode': n_mode})

    n_data = len(data)
    y_lnk = np.array([math.log(d['k_eff']) for d in data])

    def run_scheme(name, gamma_eff_func, lam_init):
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
            predictions.append({'formula': d['formula'], 'cat': d['cat'], 'gl': d['gl'],
                                'tc_pred': tc_pred, 'tc_exp': d['tc'], 'err': err})
        errs = np.array([p['err'] for p in predictions])
        is_gl2 = np.array([p['gl'] == 2 for p in predictions])
        return {'name': name, 'lam': lam_opt, 'R2': R2, 'errs': errs, 'is_gl2': is_gl2, 'predictions': predictions}

    g_A = lambda d, lam: d['gamma_n'] + lam * d['casimir']
    g_B = lambda d, lam: d['gamma_n'] + lam * d['zero_gap']
    g_I = lambda d, lam: d['gamma_n'] + lam * d['zero_gap']**2
    g_J = lambda d, lam: d['gamma_n'] * (1 + lam * d['zero_gap'])
    g_K = lambda d, lam: d['gamma_n'] + lam * d['zero_gap'] / d['gamma_n']
    g_N = lambda d, lam: d['gamma_n'] + lam * d['zero_gap'] * d['gamma_n']

    schemes = [
        ("A: 线性j(j+1) [基准]", g_A, 0.39),
        ("B: 线性Δγ_f", g_B, 5.0),
        ("I: 平方(Δγ_f)²", g_I, 50.0),
        ("J: 乘法 γ_n·(1+λ·Δγ_f)", g_J, 1.0),
        ("K: 相对 Δγ_f/γ_n", g_K, 100.0),
        ("N: 耦合 Δγ_f·γ_n", g_N, 0.05),
    ]

    print(f"材料数: {n_data}")
    results = {}
    for name, g_func, lam_init in schemes:
        res = run_scheme(name, g_func, lam_init)
        results[name] = res

    print(f"\n方案对比结果")
    print(f"{'方案':<30} {'λ':>10} {'R²':>7} {'全部中位%':>10} {'GL2中位%':>9} {'GL2 2倍%':>8} {'GL2 5倍%':>8}")
    print("-" * 85)
    for name, _, _ in schemes:
        res = results[name]
        e_all = res['errs']; e_gl2 = res['errs'][res['is_gl2']]
        print(f"{name:<30} {res['lam']:>10.4f} {res['R2']:>7.4f} {np.median(e_all)*100:>10.1f} {np.median(e_gl2)*100:>9.1f} {np.mean(e_gl2<=1)*100:>8.0f} {np.mean(e_gl2<=4)*100:>8.0f}")

    best_gl2 = min(schemes, key=lambda s: np.median(results[s[0]]['errs'][results[s[0]]['is_gl2']]))
    print(f"\n最佳方案: {best_gl2[0]}")


# =====================================================
# 路径4: 同步算符
# =====================================================

def path4_sync_operator():
    print("\n" + "=" * 80)
    print("路径4: GL(2)同步算符的第一性推导")
    print("=" * 80)

    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.model_selection import LeaveOneOut

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

    print("\n4.1 基线 one-hot类别模型")
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

    print("\n4.2 γ_riemann + λ·j(j+1) + p·ln(G) + q·ln(θ_D) + b [纯第一性]")
    X2 = np.zeros((n_data, 5))
    for i, d in enumerate(data):
        X2[i, 0] = d['gamma_n']; X2[i, 1] = d['casimir']
        X2[i, 2] = math.log(d['G']); X2[i, 3] = math.log(d['tD']); X2[i, 4] = 1.0
    coef2, _, _, _ = np.linalg.lstsq(X2, y_lnk, rcond=None)
    r2_2 = 1 - np.sum((y_lnk - X2 @ coef2)**2) / np.sum((y_lnk - np.mean(y_lnk))**2)
    print(f"a={coef2[0]:.4f}, λ={coef2[1]:.4f}, p={coef2[2]:.4f}, q={coef2[3]:.4f}, b={coef2[4]:.4f}, R²={r2_2:.4f}")

    err2 = []
    for i in range(n_data):
        X_tr = np.delete(X2, i, axis=0); y_tr = np.delete(y_lnk, i)
        coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
        tc_pred = calc_tc_from_lnk(X2[i] @ coef, data[i])
        err2.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
    err2 = np.array(err2)
    print(f"LOOCV: 中位{np.median(err2)*100:.0f}%, 2倍内{np.mean(err2<=1)*100:.0f}%, 5倍内{np.mean(err2<=4)*100:.0f}%")

    print("\n4.6 GBR端到端 + γ_n + Casimir特征 [纯第一性]")
    def get_feats_ext(d):
        return np.array([
            math.log(d['G']), math.log(d['tD']), math.log(d['dd0']),
            math.log(d['M']), math.log(d['Z']) if d['Z'] > 0 else 0,
            math.log(d['V']), math.log(d['n_atoms']),
            math.log(d['B']) if d['B'] > 0 else 0,
            1.0 / d['tD'], math.log(d['tD'])**2,
            math.log(d['tD'] / d['dd0']) if d['dd0'] > 0 else 0,
            d['gamma_n'], d['casimir'], d['j'],
            1.0 if d['gl'] == 2 else 0.0,
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

    print(f"\n全方法对比:")
    print(f"{'方法':<55} {'中位%':>6} {'2倍%':>6} {'5倍%':>6}")
    methods = [
        ("one-hot类别模型 (基线)", err1),
        ("γ_n+λ·j(j+1)+G+θ_D [纯第一性]", err2),
        ("GBR+γ_n+Casimir [纯第一性]", err6),
    ]
    for name, err in methods:
        print(f"{name:<55} {np.median(err)*100:>6.0f} {np.mean(err<=1)*100:>6.0f} {np.mean(err<=4)*100:>6.0f}")


# =====================================================
# 路径5: 零点差 vs Casimir
# =====================================================

def path5_zero_gap_vs_casimir():
    print("\n" + "=" * 80)
    print("路径5: GL(2)零点差 vs j(j+1) Casimir修正")
    print("=" * 80)

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
                n_mode = 1; j = 0; pairing = 's'
            else:
                n_mode = CAT_TO_N.get(cat, 5)
            gamma_n = RIEMANN_ZEROS[n_mode - 1]
            casimir = j * (j + 1)
            zero_gap = GL2_ZERO_GAP_D if pairing == 'd' else (GL2_ZERO_GAP_P if pairing == 'p' else 0.0)
            zero_gap_norm = zero_gap / GL1_ZERO_GAP
            k_eff = tc**2 * 9 * LN2 / (8 * mp['dd0']**2 * mp['theta_D'])
            data.append({**mp, 'cat': cat, 'tc': tc, 'k_eff': k_eff,
                         'gl': gl, 'j': j, 'casimir': casimir,
                         'pairing': pairing, 'zero_gap': zero_gap,
                         'zero_gap_norm': zero_gap_norm,
                         'gamma_n': gamma_n, 'n_mode': n_mode})

    n_data = len(data)
    y_lnk = np.array([math.log(d['k_eff']) for d in data])

    print(f"材料数: {n_data}")
    print(f"GL(1)零点差 Δγ₁ = γ₂-γ₁ = {GL1_ZERO_GAP:.4f}")

    def run_scheme(name, feat_func, lam_init):
        def build_X(lam):
            X = np.zeros((n_data, 7))
            for i, d in enumerate(data):
                gamma_eff = d['gamma_n'] + lam[0] * feat_func(d)
                X[i, 0] = gamma_eff
                X[i, 1] = math.log(d['G']); X[i, 2] = math.log(d['theta_D'])
                X[i, 3] = math.log(d['B']); X[i, 4] = math.log(d['N'])
                X[i, 5] = math.log(d['V']); X[i, 6] = 1.0
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
            X_tr = np.delete(X_final, i, axis=0); y_tr = np.delete(y_lnk, i)
            coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
            d = data[i]
            gamma_eff = d['gamma_n'] + lam_opt * feat_func(d)
            ln_k = coef[0]*gamma_eff + coef[1]*math.log(d['G']) + coef[2]*math.log(d['theta_D']) + coef[3]*math.log(d['B']) + coef[4]*math.log(d['N']) + coef[5]*math.log(d['V']) + coef[6]
            k_eff = math.exp(ln_k)
            tc_pred = math.sqrt(8 * d['dd0']**2 * k_eff * d['theta_D'] / (9 * LN2))
            err = abs(tc_pred - d['tc']) / d['tc']
            predictions.append({'formula': d['formula'], 'cat': d['cat'], 'gl': d['gl'],
                                'pairing': d['pairing'], 'tc_pred': tc_pred,
                                'tc_exp': d['tc'], 'err': err})

        errs = np.array([p['err'] for p in predictions])
        is_gl2 = np.array([p['gl'] == 2 for p in predictions])
        return {'name': name, 'lam': lam_opt, 'R2': R2, 'errs': errs, 'is_gl2': is_gl2, 'predictions': predictions}

    f_casimir = lambda d: d['casimir']
    f_zero_gap = lambda d: d['zero_gap']
    f_zero_gap_norm = lambda d: d['zero_gap_norm']

    res_A = run_scheme("A: j(j+1) Casimir [原方案]", f_casimir, 0.39)
    res_B = run_scheme("B: GL(2)零点差 Δγ_f", f_zero_gap, 5.0)
    res_C = run_scheme("C: 标准化零点差 Δγ_f/Δγ₁", f_zero_gap_norm, 30.0)

    print(f"\n方案对比结果")
    print(f"{'方案':<35} {'λ':>8} {'R²':>7} {'全部中位%':>10} {'GL2中位%':>9} {'GL2 2倍%':>8} {'GL2 5倍%':>8}")
    print("-" * 85)
    for res in [res_A, res_B, res_C]:
        e_all = res['errs']; e_gl2 = res['errs'][res['is_gl2']]
        print(f"{res['name']:<35} {res['lam']:>8.4f} {res['R2']:>7.4f} {np.median(e_all)*100:>10.1f} {np.median(e_gl2)*100:>9.1f} {np.mean(e_gl2<=1)*100:>8.0f} {np.mean(e_gl2<=4)*100:>8.0f}")

    e_gl2_A = res_A['errs'][res_A['is_gl2']]
    e_gl2_B = res_B['errs'][res_B['is_gl2']]
    print(f"\n结论: 方案A GL2中位{np.median(e_gl2_A)*100:.1f}% vs 方案B {np.median(e_gl2_B)*100:.1f}%")


# =====================================================
# 主入口
# =====================================================

if __name__ == "__main__":
    path1_gl2_layered()
    path2_contribution_decomposition()
    path3_crossing_nonlinear()
    path4_sync_operator()
    path5_zero_gap_vs_casimir()