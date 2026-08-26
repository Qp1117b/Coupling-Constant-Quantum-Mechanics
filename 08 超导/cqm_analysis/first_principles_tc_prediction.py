"""
第一性超导预测推进：用纯几何特征替代类别校准

当前状态：
- one-hot类别模型: LOOCV中位45%（基线）
- GBR端到端纯第一性: 中位51%（黑盒）
- K_0^cat = 7.77e11 * exp(0.369 * gamma_n), R2=0.96

推进目标：
- 用分子FG同步算符特征（delta_intrinsic, spectral_gap, size_disorder）替代类别校准
- 实现可解释的纯第一性公式，LOOCV中位<=45%
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework'); from atom_db import ATOM_DB, atom_db

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

    # 分子FG同步算符特征（纯第一性）
    avg_valence = sum(atoms[el] * ATOM_DB[el][4] for el in atoms) / n_atoms if all(ATOM_DB[el][4] if len(ATOM_DB[el]) > 4 else False for el in atoms) else 4.0
    coordination_deviation = abs(avg_valence - 4.0) / 4.0
    if len(els) > 1:
        masses = [atoms[el] * ATOM_DB[el][0] for el in els]
        size_disorder = np.std(masses) / np.mean(masses) if np.mean(masses) > 0 else 0
    else:
        size_disorder = 0
    delta_intrinsic = max(0.001, coordination_deviation * 0.3 + size_disorder * 0.1)
    spectral_gap = max(0.1, avg_valence * 0.5)
    n_elem = len(els)

    return {'l': l, 'G': G, 'dd0': dd0, 'tD': theta_d,
            'M': total_m, 'Z': total_z, 'V': V_cell,
            'n_atoms': n_atoms, 'B': B_est,
            'delta_intrinsic': delta_intrinsic,
            'spectral_gap': spectral_gap,
            'size_disorder': size_disorder,
            'n_elem': n_elem,
            'coordination_deviation': coordination_deviation}


def load_data():
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
    return data


def loocv_metrics(errs):
    errs = np.array(errs)
    return (np.median(errs)*100, np.mean(errs)*100,
            np.sum(errs < 1)*100/len(errs), np.sum(errs < 4)*100/len(errs))


data = load_data()
n_data = len(data)
categories = sorted(set(d['cat'] for d in data))
print(f"加载 {n_data} 个材料, {len(categories)} 个类别")

# ============================================================
# 基线1: one-hot类别模型 (复现45%)
# ============================================================
print("\n" + "="*80)
print("基线1: one-hot类别模型 ln(K_eff) = Σβ_cat + p·ln(G) + q·ln(θ_D) + b")
print("="*80)

cat_idx = {c: i for i, c in enumerate(categories)}
n_cats = len(categories)
y_lnk = np.array([math.log(d['k_eff']) for d in data])

errs1 = []
for i in range(n_data):
    X = np.zeros((n_data, n_cats + 3))
    for j, d in enumerate(data):
        X[j, cat_idx[d['cat']]] = 1.0
        X[j, n_cats] = math.log(d['G'])
        X[j, n_cats+1] = math.log(d['tD'])
        X[j, n_cats+2] = 1.0
    X_tr = np.delete(X, i, axis=0)
    y_tr = np.delete(y_lnk, i)
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    ln_k_pred = X[i] @ coef
    k_pred = math.exp(ln_k_pred)
    tc_pred = math.sqrt(8 * data[i]['dd0']**2 * k_pred * data[i]['tD'] / (9 * LN2))
    errs1.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])

m1 = loocv_metrics(errs1)

print(f"  中位: {m1[0]:.1f}%  2倍内: {m1[2]:.1f}%  5倍内: {m1[3]:.1f}%")

# ============================================================
# 推进1: 纯几何特征替代类别one-hot
# ln(K_eff) = a·ln(δ_int) + b·ln(spectral_gap) + c·ln(size_disorder) + d·n_elem + p·ln(G) + q·ln(θ_D) + b
# ============================================================
print("\n" + "="*80)
print("推进1: 纯几何特征替代类别 ln(K_eff) = a·ln(δ_int) + b·ln(sp_gap) + c·ln(sd) + d·n_elem + p·ln(G) + q·ln(θ_D) + b")
print("="*80)

def get_geom_feats(d):
    return np.array([
        math.log(d['delta_intrinsic']),
        math.log(d['spectral_gap']),
        math.log(d['size_disorder'] + 0.001),
        d['n_elem'],
        math.log(d['G']),
        math.log(d['tD']),
        1.0,
    ])

errs2 = []
for i in range(n_data):
    X = np.array([get_geom_feats(d) for d in data])
    y = y_lnk
    X_tr = np.delete(X, i, axis=0)
    y_tr = np.delete(y, i)
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    ln_k_pred = X[i] @ coef
    k_pred = math.exp(ln_k_pred)
    tc_pred = math.sqrt(8 * data[i]['dd0']**2 * k_pred * data[i]['tD'] / (9 * LN2))
    errs2.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])

m2 = loocv_metrics(errs2)
print(f"  中位: {m2[0]:.1f}%  2倍内: {m2[2]:.1f}%  5倍内: {m2[3]:.1f}%")

# ============================================================
# 推进2: 扩展几何特征（含材料参数）
# ============================================================
print("\n" + "="*80)
print("推进2: 扩展几何特征 ln(K_eff) = a·ln(δ_int) + b·ln(sp_gap) + c·ln(sd) + d·n_elem + e·ln(M) + f·ln(Z) + g·ln(B) + h·ln(N) + p·ln(G) + q·ln(θ_D) + b")
print("="*80)

def get_ext_feats(d):
    return np.array([
        math.log(d['delta_intrinsic']),
        math.log(d['spectral_gap']),
        math.log(d['size_disorder'] + 0.001),
        d['n_elem'],
        math.log(d['M']),
        math.log(d['Z']) if d['Z'] > 0 else 0,
        math.log(d['B']) if d['B'] > 0 else 0,
        math.log(d['n_atoms']),
        math.log(d['G']),
        math.log(d['tD']),
        1.0,
    ])

errs3 = []
for i in range(n_data):
    X = np.array([get_ext_feats(d) for d in data])
    y = y_lnk
    X_tr = np.delete(X, i, axis=0)
    y_tr = np.delete(y, i)
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    ln_k_pred = X[i] @ coef
    k_pred = math.exp(ln_k_pred)
    tc_pred = math.sqrt(8 * data[i]['dd0']**2 * k_pred * data[i]['tD'] / (9 * LN2))
    errs3.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])

m3 = loocv_metrics(errs3)
print(f"  中位: {m3[0]:.1f}%  2倍内: {m3[2]:.1f}%  5倍内: {m3[3]:.1f}%")

# ============================================================
# 推进3: 黎曼零点指数机制 + 纯几何γ_n推导
# K_0 = C·exp(a·γ_n), γ_n从几何特征推导（非类别映射）
# ============================================================
print("\n" + "="*80)
print("推进3: 黎曼零点指数机制 + 纯几何γ_n推导")
print("="*80)

# 先用全部数据拟合 γ_n 与几何特征的关系
y_gamma = np.array([d['gamma_cat'] for d in data])

def get_gamma_feats(d):
    return np.array([
        math.log(d['delta_intrinsic']),
        math.log(d['spectral_gap']),
        math.log(d['size_disorder'] + 0.001),
        d['n_elem'],
        math.log(d['M']),
        math.log(d['Z']) if d['Z'] > 0 else 0,
        math.log(d['B']) if d['B'] > 0 else 0,
        math.log(d['n_atoms']),
        1.0,
    ])

errs4 = []
for i in range(n_data):
    # 步骤1: 从几何特征预测γ_n
    X_gamma = np.array([get_gamma_feats(d) for d in data])
    X_gamma_tr = np.delete(X_gamma, i, axis=0)
    y_gamma_tr = np.delete(y_gamma, i)
    coef_gamma, _, _, _ = np.linalg.lstsq(X_gamma_tr, y_gamma_tr, rcond=None)
    gamma_pred = X_gamma[i] @ coef_gamma

    # 步骤2: K_0 = C·exp(a·gamma_pred)
    # 步骤3: K_eff = K_0 · G^p · θ_D^q
    # 步骤4: 用剩余数据拟合 p, q, C, a
    X_keff = np.zeros((n_data - 1, 4))
    y_keff_tr = np.delete(y_lnk, i)
    idx = 0
    for j in range(n_data):
        if j == i:
            continue
        gj = X_gamma[j] @ coef_gamma
        X_keff[idx, 0] = gj  # gamma项
        X_keff[idx, 1] = math.log(data[j]['G'])
        X_keff[idx, 2] = math.log(data[j]['tD'])
        X_keff[idx, 3] = 1.0
        idx += 1
    coef_keff, _, _, _ = np.linalg.lstsq(X_keff, y_keff_tr, rcond=None)

    # 预测
    ln_k_pred = (gamma_pred * coef_keff[0] +
                 math.log(data[i]['G']) * coef_keff[1] +
                 math.log(data[i]['tD']) * coef_keff[2] +
                 coef_keff[3])
    k_pred = math.exp(ln_k_pred)
    tc_pred = math.sqrt(8 * data[i]['dd0']**2 * k_pred * data[i]['tD'] / (9 * LN2))
    errs4.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])

m4 = loocv_metrics(errs4)
print(f"  中位: {m4[0]:.1f}%  2倍内: {m4[2]:.1f}%  5倍内: {m4[3]:.1f}%")

# ============================================================
# 汇总
# ============================================================
print("\n" + "="*80)
print("汇总对比")
print("="*80)
print(f"{'方法':<50} {'中位%':>8} {'2倍内%':>8} {'5倍内%':>8}")
print(f"{'-'*74}")
print(f"{'基线1: one-hot类别模型':<50} {m1[0]:>8.1f} {m1[2]:>8.1f} {m1[3]:>8.1f}")
print(f"{'推进1: 纯几何特征(7维)':<50} {m2[0]:>8.1f} {m2[2]:>8.1f} {m2[3]:>8.1f}")
print(f"{'推进2: 扩展几何特征(11维)':<50} {m3[0]:>8.1f} {m3[2]:>8.1f} {m3[3]:>8.1f}")
print(f"{'推进3: 黎曼零点+几何γ_n推导':<50} {m4[0]:>8.1f} {m4[2]:>8.1f} {m4[3]:>8.1f}")

# 特征重要性
print("\n特征与ln(K_eff)相关系数:")
feats_names = ['ln(δ_int)', 'ln(sp_gap)', 'ln(sd)', 'n_elem', 'ln(M)', 'ln(Z)', 'ln(B)', 'ln(N)', 'ln(G)', 'ln(θ_D)']
for name, feat_func in [('geom', get_geom_feats), ('ext', get_ext_feats)]:
    print(f"  [{name}]")
    X = np.array([feat_func(d) for d in data])
    for j, fname in enumerate(feats_names[:X.shape[1]-1]):
        if np.std(X[:,j]) > 0:
            corr = np.corrcoef(X[:,j], y_lnk)[0,1]
            print(f"    {fname:15s}: r={corr:+.3f}")
