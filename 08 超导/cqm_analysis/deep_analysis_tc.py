"""
深入分析: GL(1)误差来源 + 重费米子GL层 + 进一步精确化

问题: GL(1)中位65%, 被重费米子(Tc极低)拖累
假设: 重费米子涉及f电子, 可能j=3(f波配对), 属于GL(2)而非GL(1)
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework'); from atom_db import ATOM_DB, atom_db

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


# 重费米子材料列表 (含Ce, Yb, U, Pr等f电子元素)
HEAVY_FERMION_ELEMENTS = {'Ce', 'Yb', 'U', 'Pr', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Lu', 'Nd', 'Yb', 'Np', 'Pu'}

# 铁电超导体
FERROELECTRIC_SC = {'SrTiO3', 'KTaO3', 'BaTiO3', 'PbTiO3'}

CAT_TO_N = {
    '石墨插层超导体': 1, '有机超导体': 3, 'A15结构金属间化合物': 7,
    '铁基超导体': 8, '铜氧化物高温超导体': 9, '氢化物高压超导体': 10,
    '元素超导体(常压)': 5, '元素超导体(高压)': 6, '其他金属间化合物': 4,
    '其他特殊超导体': 5, '合金超导体': 4, '富勒烯超导体': 3,
}
CAT_TO_J = {
    '铜氧化物高温超导体': 2, '铁基超导体': 1, '有机超导体': 1, '富勒烯超导体': 1,
}

GL1_CATS = {
    '元素超导体(常压)', '元素超导体(高压)', 'A15结构金属间化合物',
    '合金超导体', '其他金属间化合物', '氢化物高压超导体',
    '石墨插层超导体', '其他特殊超导体',
}
GL2_CATS = {
    '铜氧化物高温超导体', '铁基超导体', '有机超导体', '富勒烯超导体',
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
    has_f_electron = any(el in HEAVY_FERMION_ELEMENTS for el in atoms)
    is_ferroelectric = formula in FERROELECTRIC_SC
    return {
        'formula': formula, 'atoms': atoms,
        'M': total_m, 'Z': total_z, 'N': n_atoms,
        'l': l, 'theta_D': theta_d, 'V': V_cell,
        'f_corr': f_corr, 'edge_sum': edge_sum,
        'G': G, 'dd0': dd0, 'B': B_est,
        'has_f': has_f_electron, 'is_ferro': is_ferroelectric,
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
# 分析1: GL(1)误差来源 — 识别重费米子和铁电体
# ============================================================
print("="*80)
print("分析1: GL(1)误差来源识别")
print("="*80)

# 用全局统一公式参数
lam_opt = 0.2343
def build_X(lam):
    X = np.zeros((n_data, 6))
    for i, d in enumerate(data):
        gamma_eff = d['gamma_n'] + lam * d['casimir']
        X[i, 0] = gamma_eff
        X[i, 1] = math.log(d['G'])
        X[i, 2] = math.log(d['theta_D'])
        X[i, 3] = math.log(d['B'])
        X[i, 4] = math.log(d['N'])
        X[i, 5] = 1.0
    return X

X_all = build_X(lam_opt)
coef_all, _, _, _ = np.linalg.lstsq(X_all, y_lnk, rcond=None)

# 计算每个材料的误差
for d in data:
    gamma_eff = d['gamma_n'] + lam_opt * d['casimir']
    ln_k = coef_all[0]*gamma_eff + coef_all[1]*math.log(d['G']) + coef_all[2]*math.log(d['theta_D']) + coef_all[3]*math.log(d['B']) + coef_all[4]*math.log(d['N']) + coef_all[5]
    tc_pred = math.sqrt(8 * d['dd0']**2 * math.exp(ln_k) * d['theta_D'] / (9 * LN2))
    d['tc_pred'] = tc_pred
    d['err'] = abs(tc_pred - d['tc']) / d['tc']

# GL(1)材料按误差排序
gl1_data = [d for d in data if d['gl'] == 1]
gl1_data.sort(key=lambda x: -x['err'])

print(f"\nGL(1)误差最大的20个材料:")
print(f"{'材料':<25} {'Tc_exp':>7} {'Tc_pred':>8} {'误差%':>8} {'f电子':>5} {'铁电':>5}")
print("-"*65)
for d in gl1_data[:20]:
    print(f"{d['formula']:<25} {d['tc']:>7.2f} {d['tc_pred']:>8.2f} {d['err']*100:>8.0f}% {'是' if d['has_f'] else '否':>5} {'是' if d['is_ferro'] else '否':>5}")

# 统计
hf_count = sum(1 for d in gl1_data if d['has_f'])
fe_count = sum(1 for d in gl1_data if d['is_ferro'])
print(f"\nGL(1)中含f电子材料: {hf_count}/{len(gl1_data)}")
print(f"GL(1)中铁电体: {fe_count}/{len(gl1_data)}")

# 排除f电子和铁电体后的GL(1)精度
gl1_clean = [d for d in gl1_data if not d['has_f'] and not d['is_ferro']]
errs_gl1_clean = np.array([d['err'] for d in gl1_clean])
print(f"\nGL(1)排除f电子+铁电体后: n={len(gl1_clean)}, 中位{np.median(errs_gl1_clean)*100:.0f}%, 2倍内{np.mean(errs_gl1_clean<=1)*100:.0f}%, 5倍内{np.mean(errs_gl1_clean<=4)*100:.0f}%")

# ============================================================
# 分析2: 重费米子作为GL(2) j=3 (f波配对)
# ============================================================
print(f"\n{'='*80}")
print("分析2: 重费米子重新分类为GL(2) j=3 (f波配对)")
print("="*80)

# 重新分类: 含f电子的材料 → GL(2), j=3
for d in data:
    if d['has_f'] and d['gl'] == 1:
        d['gl_new'] = 2
        d['j_new'] = 3
        d['casimir_new'] = 3 * 4  # j=3, Casimir=12
    elif d['is_ferro']:
        d['gl_new'] = 2
        d['j_new'] = 1  # 铁电体: 声子+极化耦合, j=1
        d['casimir_new'] = 2
    else:
        d['gl_new'] = d['gl']
        d['j_new'] = d['j']
        d['casimir_new'] = d['casimir']

gl1_new = [d for d in data if d['gl_new'] == 1]
gl2_new = [d for d in data if d['gl_new'] == 2]
print(f"重新分类后: GL(1)={len(gl1_new)}, GL(2)={len(gl2_new)}")
print(f"  其中重费米子(j=3): {sum(1 for d in data if d.get('j_new')==3)}")
print(f"  铁电体(j=1): {sum(1 for d in data if d['is_ferro'])}")

# 用新分类重新优化
def build_X_new(lam):
    X = np.zeros((n_data, 6))
    for i, d in enumerate(data):
        gamma_eff = d['gamma_n'] + lam * d['casimir_new']
        X[i, 0] = gamma_eff
        X[i, 1] = math.log(d['G'])
        X[i, 2] = math.log(d['theta_D'])
        X[i, 3] = math.log(d['B'])
        X[i, 4] = math.log(d['N'])
        X[i, 5] = 1.0
    return X

def obj_new(lam):
    X = build_X_new(lam[0])
    coef, _, _, _ = np.linalg.lstsq(X, y_lnk, rcond=None)
    return np.sum((y_lnk - X @ coef)**2)

res_new = minimize(obj_new, x0=[0.234], method='Nelder-Mead', options={'maxiter': 5000})
lam_new = res_new.x[0]
X_new = build_X_new(lam_new)
coef_new, _, _, _ = np.linalg.lstsq(X_new, y_lnk, rcond=None)
r2_new = 1 - np.sum((y_lnk - X_new @ coef_new)**2) / np.sum((y_lnk - np.mean(y_lnk))**2)
print(f"\nγ_eff = γ_n + {lam_new:.4f}·j(j+1)")
print(f"ln(K_eff) = {coef_new[0]:.4f}·γ_eff + {coef_new[1]:.4f}·ln(G) + {coef_new[2]:.4f}·ln(θ_D) + {coef_new[3]:.4f}·ln(B) + {coef_new[4]:.4f}·ln(N) + {coef_new[5]:.4f}")
print(f"R² = {r2_new:.4f}")

# LOOCV
err_new = []
for i in range(n_data):
    X_tr = np.delete(X_new, i, axis=0)
    y_tr = np.delete(y_lnk, i)
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    gamma_eff = data[i]['gamma_n'] + lam_new * data[i]['casimir_new']
    ln_k = coef[0]*gamma_eff + coef[1]*math.log(data[i]['G']) + coef[2]*math.log(data[i]['theta_D']) + coef[3]*math.log(data[i]['B']) + coef[4]*math.log(data[i]['N']) + coef[5]
    tc_pred = math.sqrt(8 * data[i]['dd0']**2 * math.exp(ln_k) * data[i]['theta_D'] / (9 * LN2))
    err_new.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
err_new = np.array(err_new)

err_gl1_new = np.array([err_new[i] for i, d in enumerate(data) if d['gl_new'] == 1])
err_gl2_new = np.array([err_new[i] for i, d in enumerate(data) if d['gl_new'] == 2])
err_hf = np.array([err_new[i] for i, d in enumerate(data) if d.get('j_new') == 3])

print(f"\nLOOCV精度:")
print(f"  全部: 中位{np.median(err_new)*100:.0f}%, 2倍内{np.mean(err_new<=1)*100:.0f}%, 5倍内{np.mean(err_new<=4)*100:.0f}%")
print(f"  GL(1)常规: 中位{np.median(err_gl1_new)*100:.0f}%, 2倍内{np.mean(err_gl1_new<=1)*100:.0f}%, 5倍内{np.mean(err_gl1_new<=4)*100:.0f}%")
print(f"  GL(2)非常规: 中位{np.median(err_gl2_new)*100:.0f}%, 2倍内{np.mean(err_gl2_new<=1)*100:.0f}%, 5倍内{np.mean(err_gl2_new<=4)*100:.0f}%")
if len(err_hf) > 0:
    print(f"  重费米子(j=3): 中位{np.median(err_hf)*100:.0f}%, 2倍内{np.mean(err_hf<=1)*100:.0f}%, 5倍内{np.mean(err_hf<=4)*100:.0f}%")

# ============================================================
# 分析3: GL(1)/GL(2)分别优化 + 重费米子j=3
# ============================================================
print(f"\n{'='*80}")
print("分析3: GL(1)/GL(2)/重费米子 分别优化")
print("="*80)

gl1_final = [d for d in data if d['gl_new'] == 1]
gl2_final = [d for d in data if d['gl_new'] == 2 and d.get('j_new') != 3]
hf_final = [d for d in data if d.get('j_new') == 3]

def optimize_subset_detail(subset, label):
    n = len(subset)
    if n < 5:
        print(f"{label}: 数据太少 ({n})")
        return np.array([])
    y = np.array([math.log(d['k_eff']) for d in subset])
    feat_names = ['γ_n', 'ln(G)', 'ln(θ_D)', 'ln(B)', 'ln(N)', 'ln(V)', '1']
    X = np.zeros((n, len(feat_names)))
    for i, d in enumerate(subset):
        X[i, 0] = d['gamma_n']
        X[i, 1] = math.log(d['G'])
        X[i, 2] = math.log(d['theta_D'])
        X[i, 3] = math.log(d['B'])
        X[i, 4] = math.log(d['N'])
        X[i, 5] = math.log(d['V'])
        X[i, 6] = 1.0
    coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    r2 = 1 - np.sum((y - X @ coef)**2) / np.sum((y - np.mean(y))**2) if np.sum((y - np.mean(y))**2) > 0 else 0

    errs = []
    for i in range(n):
        X_tr = np.delete(X, i, axis=0)
        y_tr = np.delete(y, i)
        coef_l, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
        ln_k = X[i] @ coef_l
        tc_pred = math.sqrt(8 * subset[i]['dd0']**2 * math.exp(ln_k) * subset[i]['theta_D'] / (9 * LN2))
        errs.append(abs(tc_pred - subset[i]['tc']) / subset[i]['tc'])
    errs = np.array(errs)

    print(f"\n{label} (n={n}):")
    print(f"  R² = {r2:.4f}")
    print(f"  LOOCV: 中位{np.median(errs)*100:.0f}%, 2倍内{np.mean(errs<=1)*100:.0f}%, 5倍内{np.mean(errs<=4)*100:.0f}%")
    return errs

err_g1 = optimize_subset_detail(gl1_final, "GL(1)常规(排除重费米子)")
err_g2 = optimize_subset_detail(gl2_final, "GL(2)非常规(排除重费米子)")
err_hf3 = optimize_subset_detail(hf_final, "重费米子(j=3)")

all_errs = [e for e in [err_g1, err_g2, err_hf3] if len(e) > 0]
if all_errs:
    err_combined = np.concatenate(all_errs)
    print(f"\n合并: 中位{np.median(err_combined)*100:.0f}%, 2倍内{np.mean(err_combined<=1)*100:.0f}%, 5倍内{np.mean(err_combined<=4)*100:.0f}%")

# ============================================================
# 分析4: 最优统一公式 — 重费米子j=3, 全局优化
# ============================================================
print(f"\n{'='*80}")
print("分析4: 最优统一公式 (重费米子j=3)")
print("="*80)

# 搜索最优lam和特征组合
def build_X_opt(lam):
    X = np.zeros((n_data, 7))
    for i, d in enumerate(data):
        gamma_eff = d['gamma_n'] + lam * d['casimir_new']
        X[i, 0] = gamma_eff
        X[i, 1] = math.log(d['G'])
        X[i, 2] = math.log(d['theta_D'])
        X[i, 3] = math.log(d['B'])
        X[i, 4] = math.log(d['N'])
        X[i, 5] = math.log(d['V'])
        X[i, 6] = 1.0
    return X

def obj_opt(lam):
    X = build_X_opt(lam[0])
    coef, _, _, _ = np.linalg.lstsq(X, y_lnk, rcond=None)
    return np.sum((y_lnk - X @ coef)**2)

res_opt = minimize(obj_opt, x0=[0.234], method='Nelder-Mead', options={'maxiter': 10000})
lam_opt2 = res_opt.x[0]
X_opt = build_X_opt(lam_opt2)
coef_opt, _, _, _ = np.linalg.lstsq(X_opt, y_lnk, rcond=None)
r2_opt = 1 - np.sum((y_lnk - X_opt @ coef_opt)**2) / np.sum((y_lnk - np.mean(y_lnk))**2)

print(f"γ_eff = γ_n + {lam_opt2:.4f}·j(j+1)")
feat_names_opt = ['γ_eff', 'ln(G)', 'ln(θ_D)', 'ln(B)', 'ln(N)', 'ln(V)', '1']
print(f"ln(K_eff) = " + " + ".join(f"{coef_opt[j]:.4f}·{feat_names_opt[j]}" for j in range(len(feat_names_opt))))
print(f"R² = {r2_opt:.4f}")

err_opt = []
for i in range(n_data):
    X_tr = np.delete(X_opt, i, axis=0)
    y_tr = np.delete(y_lnk, i)
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    ln_k = X_opt[i] @ coef
    tc_pred = math.sqrt(8 * data[i]['dd0']**2 * math.exp(ln_k) * data[i]['theta_D'] / (9 * LN2))
    err_opt.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
err_opt = np.array(err_opt)

# 分层统计
err_g1_opt = np.array([err_opt[i] for i, d in enumerate(data) if d['gl_new'] == 1])
err_g2_opt = np.array([err_opt[i] for i, d in enumerate(data) if d['gl_new'] == 2 and d.get('j_new') != 3])
err_hf_opt = np.array([err_opt[i] for i, d in enumerate(data) if d.get('j_new') == 3])

print(f"\nLOOCV精度:")
print(f"{'类别':<30} {'n':>4} {'中位%':>7} {'2倍%':>6} {'5倍%':>6}")
print("-"*56)
for label, errs in [("全部", err_opt), ("GL(1)常规", err_g1_opt), ("GL(2)非常规", err_g2_opt), ("重费米子j=3", err_hf_opt)]:
    if len(errs) > 0:
        print(f"{label:<30} {len(errs):>4} {np.median(errs)*100:>7.0f} {np.mean(errs<=1)*100:>6.0f} {np.mean(errs<=4)*100:>6.0f}")

# 各类别详细
print(f"\n各类别精度:")
for cat in sorted(set(d['cat'] for d in data)):
    cat_errs = np.array([err_opt[i] for i, d in enumerate(data) if d['cat'] == cat])
    j_val = [d.get('j_new', 0) for i, d in enumerate(data) if d['cat'] == cat][0]
    print(f"  {cat:<30} j={j_val}, n={len(cat_errs):>3}, 中位{np.median(cat_errs)*100:>5.0f}%, 2倍内{np.mean(cat_errs<=1)*100:>3.0f}%, 5倍内{np.mean(cat_errs<=4)*100:>3.0f}%")

# ============================================================
# 分析5: 精确预测值输出
# ============================================================
print(f"\n{'='*80}")
print("精确预测 — 按误差排序")
print("="*80)

preds = []
for i, d in enumerate(data):
    gamma_eff = d['gamma_n'] + lam_opt2 * d['casimir_new']
    preds.append({
        'formula': d['formula'], 'cat': d['cat'],
        'j': d.get('j_new', 0), 'gamma_eff': gamma_eff,
        'tc_exp': d['tc'], 'tc_pred': math.sqrt(8 * d['dd0']**2 * math.exp(X_opt[i] @ coef_opt) * d['theta_D'] / (9 * LN2)),
        'err': err_opt[i],
    })
preds.sort(key=lambda x: x['err'])

print(f"\n最佳30个预测:")
print(f"{'材料':<25} {'j':>2} {'γ_eff':>7} {'Tc_exp':>8} {'Tc_pred':>8} {'误差%':>7}")
print("-"*62)
for p in preds[:30]:
    print(f"{p['formula']:<25} {p['j']:>2} {p['gamma_eff']:>7.2f} {p['tc_exp']:>8.2f} {p['tc_pred']:>8.2f} {p['err']*100:>7.1f}%")

print(f"\n最差10个预测:")
for p in preds[-10:]:
    print(f"{p['formula']:<25} {p['j']:>2} {p['gamma_eff']:>7.2f} {p['tc_exp']:>8.2f} {p['tc_pred']:>8.2f} {p['err']*100:>7.1f}%")

# ============================================================
# 总结
# ============================================================
print(f"\n{'='*80}")
print("总结 — 深入分析后的完整第一性Tc预测")
print("="*80)
print(f"公式: Tc = √(8·Δδ₀²·K_eff·θ_D / (9·ln2))")
print(f"      ln(K_eff) = {coef_opt[0]:.4f}·γ_eff + {coef_opt[1]:.4f}·ln(G) + {coef_opt[2]:.4f}·ln(θ_D) + {coef_opt[3]:.4f}·ln(B) + {coef_opt[4]:.4f}·ln(N) + {coef_opt[5]:.4f}·ln(V) + {coef_opt[6]:.4f}")
print(f"      γ_eff = γ_n + {lam_opt2:.4f}·j(j+1)")
print(f"")
print(f"GL分层:")
print(f"  GL(1)常规超导: j=0, γ_eff=γ_n (s波声子配对)")
print(f"  GL(2)非常规超导: j=1(d波/铁基)或j=2(d波/铜氧化物), γ_eff=γ_n+λ·j(j+1)")
print(f"  重费米子: j=3(f波), γ_eff=γ_n+λ·12")
print(f"")
print(f"精度: 全部中位{np.median(err_opt)*100:.0f}%, 2倍内{np.mean(err_opt<=1)*100:.0f}%, 5倍内{np.mean(err_opt<=4)*100:.0f}%")
if len(err_g2_opt) > 0:
    print(f"      GL(2)中位{np.median(err_g2_opt)*100:.0f}%, 2倍内{np.mean(err_g2_opt<=1)*100:.0f}%, 5倍内{np.mean(err_g2_opt<=4)*100:.0f}%")
if len(err_g1_opt) > 0:
    print(f"      GL(1)中位{np.median(err_g1_opt)*100:.0f}%, 2倍内{np.mean(err_g1_opt<=1)*100:.0f}%, 5倍内{np.mean(err_g1_opt<=4)*100:.0f}%")