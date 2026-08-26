"""
完整第一性Tc计算链路 — 显式公式版

目标: 给出每个材料从晶体结构到Tc的完整显式计算链路
  材料化学式 → 原子参数 → Δδ₀, G, θ_D, B → γ_eff → K_eff → Tc

关键: 用显式公式(非GBR黑盒), 分别对GL(1)/GL(2)优化
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
    """完整计算链: 化学式 → 所有CQM几何参数"""
    atoms = parse_formula(formula)
    if not atoms:
        return None
    # 环节1: 原子参数
    total_m = sum(atoms[el] * ATOM_DB[el][0] for el in atoms)
    total_z = sum(atoms[el] * ATOM_DB[el][3] for el in atoms)
    n_atoms = sum(atoms.values())
    avg_r = sum(atoms[el] * ATOM_DB[el][2] for el in atoms) / n_atoms
    l = 2 * avg_r * 1e-10  # 键长(米)
    theta_d = sum(atoms[el] * ATOM_DB[el][1] for el in atoms) / n_atoms
    if theta_d == 0:
        return None
    V_cell = l**3
    f_corr = 1.0 - 0.3 * (1.0 - 1.0/n_atoms)
    # 环节2: 边求和(质量倒数对)
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
    # 环节3: 结构因子G
    G = (1.0/l) * math.sqrt((1.0 - f_corr) * edge_sum)
    # 环节4: 角亏涨落Δδ₀
    omega_d = theta_d * KB / HBAR
    dd0_sq = (C2 / l**2) * (3*HBAR / (4*omega_d)) * (1 - f_corr) * edge_sum
    dd0 = math.sqrt(abs(dd0_sq))
    # 环节5: 体模量B
    B_est = total_m * theta_d**2 * KB / V_cell * 1e-3
    return {
        'formula': formula, 'atoms': atoms,
        'M': total_m, 'Z': total_z, 'N': n_atoms,
        'l': l, 'theta_D': theta_d, 'V': V_cell,
        'f_corr': f_corr, 'edge_sum': edge_sum,
        'G': G, 'dd0': dd0, 'B': B_est,
        'omega_D': omega_d,
    }

# ============================================================
# 加载数据
# ============================================================
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
print(f"加载 {n_data} 个材料")
print(f"GL(1): {sum(1 for d in data if d['gl']==1)}, GL(2): {sum(1 for d in data if d['gl']==2)}")

# ============================================================
# 最优显式公式搜索
# ln(K_eff) = a·γ_eff + p·ln(G) + q·ln(θ_D) + r·ln(B) + s·ln(N) + b
# γ_eff = γ_n + λ·j(j+1)
# 对GL(1)和GL(2)分别优化参数
# ============================================================

def compute_tc(params, d):
    """从参数和材料几何计算Tc"""
    a, lam, p, q, r, s, b = params
    gamma_eff = d['gamma_n'] + lam * d['casimir']
    ln_k = a * gamma_eff + p * math.log(d['G']) + q * math.log(d['theta_D']) + r * math.log(d['B']) + s * math.log(d['N']) + b
    k_eff = math.exp(ln_k)
    tc = math.sqrt(8 * d['dd0']**2 * k_eff * d['theta_D'] / (9 * LN2))
    return tc, gamma_eff, k_eff

# --- 全局统一公式 ---
print(f"\n{'='*80}")
print("搜索1: 全局统一显式公式")
print("="*80)

y_lnk = np.array([math.log(d['k_eff']) for d in data])

def build_X_unified(lam):
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

def obj_unified(lam):
    X = build_X_unified(lam[0])
    coef, _, _, _ = np.linalg.lstsq(X, y_lnk, rcond=None)
    return np.sum((y_lnk - X @ coef)**2)

res = minimize(obj_unified, x0=[0.8], method='Nelder-Mead', options={'maxiter': 5000})
lam_opt = res.x[0]
X_u = build_X_unified(lam_opt)
coef_u, _, _, _ = np.linalg.lstsq(X_u, y_lnk, rcond=None)
r2_u = 1 - np.sum((y_lnk - X_u @ coef_u)**2) / np.sum((y_lnk - np.mean(y_lnk))**2)
params_u = [coef_u[0], lam_opt, coef_u[1], coef_u[2], coef_u[3], coef_u[4], coef_u[5]]
print(f"γ_eff = γ_n + {lam_opt:.4f}·j(j+1)")
print(f"ln(K_eff) = {coef_u[0]:.4f}·γ_eff + {coef_u[1]:.4f}·ln(G) + {coef_u[2]:.4f}·ln(θ_D) + {coef_u[3]:.4f}·ln(B) + {coef_u[4]:.4f}·ln(N) + {coef_u[5]:.4f}")
print(f"R² = {r2_u:.4f}")

# LOOCV
err_u = []
for i in range(n_data):
    X_tr = np.delete(X_u, i, axis=0)
    y_tr = np.delete(y_lnk, i)
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    gamma_eff = data[i]['gamma_n'] + lam_opt * data[i]['casimir']
    ln_k = coef[0]*gamma_eff + coef[1]*math.log(data[i]['G']) + coef[2]*math.log(data[i]['theta_D']) + coef[3]*math.log(data[i]['B']) + coef[4]*math.log(data[i]['N']) + coef[5]
    tc_pred = math.sqrt(8 * data[i]['dd0']**2 * math.exp(ln_k) * data[i]['theta_D'] / (9 * LN2))
    err_u.append(abs(tc_pred - data[i]['tc']) / data[i]['tc'])
err_u = np.array(err_u)
print(f"LOOCV: 中位{np.median(err_u)*100:.0f}%, 2倍内{np.mean(err_u<=1)*100:.0f}%, 5倍内{np.mean(err_u<=4)*100:.0f}%")

# --- GL(1)/GL(2)分别优化 ---
print(f"\n{'='*80}")
print("搜索2: GL(1)/GL(2)分别优化显式公式")
print("="*80)

gl1_data = [d for d in data if d['gl'] == 1]
gl2_data = [d for d in data if d['gl'] == 2]

def optimize_subset(subset, label):
    n = len(subset)
    y = np.array([math.log(d['k_eff']) for d in subset])
    # 特征: γ_n, ln(G), ln(θ_D), ln(B), ln(N), ln(V), ln(M), 1
    feat_names = ['γ_n', 'ln(G)', 'ln(θ_D)', 'ln(B)', 'ln(N)', 'ln(V)', 'ln(M)', '1']
    X = np.zeros((n, len(feat_names)))
    for i, d in enumerate(subset):
        X[i, 0] = d['gamma_n']
        X[i, 1] = math.log(d['G'])
        X[i, 2] = math.log(d['theta_D'])
        X[i, 3] = math.log(d['B'])
        X[i, 4] = math.log(d['N'])
        X[i, 5] = math.log(d['V'])
        X[i, 6] = math.log(d['M'])
        X[i, 7] = 1.0
    coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    r2 = 1 - np.sum((y - X @ coef)**2) / np.sum((y - np.mean(y))**2) if np.sum((y - np.mean(y))**2) > 0 else 0

    # LOOCV
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
    print(f"  ln(K_eff) = " + " + ".join(f"{coef[j]:.4f}·{feat_names[j]}" for j in range(len(feat_names))))
    print(f"  R² = {r2:.4f}")
    print(f"  LOOCV: 中位{np.median(errs)*100:.0f}%, 2倍内{np.mean(errs<=1)*100:.0f}%, 5倍内{np.mean(errs<=4)*100:.0f}%")
    return {'coef': coef, 'r2': r2, 'err': errs, 'feat_names': feat_names, 'X': X}

res_gl1 = optimize_subset(gl1_data, "GL(1)常规超导")
res_gl2 = optimize_subset(gl2_data, "GL(2)非常规超导")

# 合并LOOCV
err_split = np.concatenate([res_gl1['err'], res_gl2['err']])
print(f"\n合并: 中位{np.median(err_split)*100:.0f}%, 2倍内{np.mean(err_split<=1)*100:.0f}%, 5倍内{np.mean(err_split<=4)*100:.0f}%")

# --- GL(2)用γ_eff = γ_n + λ·j(j+1) ---
print(f"\n{'='*80}")
print("搜索3: GL(2)用γ_eff = γ_n + λ·j(j+1)")
print("="*80)

def build_X_gl2_eff(lam):
    n = len(gl2_data)
    X = np.zeros((n, 7))
    for i, d in enumerate(gl2_data):
        gamma_eff = d['gamma_n'] + lam * d['casimir']
        X[i, 0] = gamma_eff
        X[i, 1] = math.log(d['G'])
        X[i, 2] = math.log(d['theta_D'])
        X[i, 3] = math.log(d['B'])
        X[i, 4] = math.log(d['N'])
        X[i, 5] = math.log(d['V'])
        X[i, 6] = 1.0
    return X

y_gl2 = np.array([math.log(d['k_eff']) for d in gl2_data])

def obj_gl2(lam):
    X = build_X_gl2_eff(lam[0])
    coef, _, _, _ = np.linalg.lstsq(X, y_gl2, rcond=None)
    return np.sum((y_gl2 - X @ coef)**2)

res_lam = minimize(obj_gl2, x0=[0.5], method='Nelder-Mead', options={'maxiter': 5000})
lam2 = res_lam.x[0]
X_gl2 = build_X_gl2_eff(lam2)
coef_gl2, _, _, _ = np.linalg.lstsq(X_gl2, y_gl2, rcond=None)
r2_gl2 = 1 - np.sum((y_gl2 - X_gl2 @ coef_gl2)**2) / np.sum((y_gl2 - np.mean(y_gl2))**2)
print(f"γ_eff = γ_n + {lam2:.4f}·j(j+1)")
feat_names_gl2 = ['γ_eff', 'ln(G)', 'ln(θ_D)', 'ln(B)', 'ln(N)', 'ln(V)', '1']
print(f"ln(K_eff) = " + " + ".join(f"{coef_gl2[j]:.4f}·{feat_names_gl2[j]}" for j in range(len(feat_names_gl2))))
print(f"R² = {r2_gl2:.4f}")

err_gl2_eff = []
for i in range(len(gl2_data)):
    X_tr = np.delete(X_gl2, i, axis=0)
    y_tr = np.delete(y_gl2, i)
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    ln_k = X_gl2[i] @ coef
    tc_pred = math.sqrt(8 * gl2_data[i]['dd0']**2 * math.exp(ln_k) * gl2_data[i]['theta_D'] / (9 * LN2))
    err_gl2_eff.append(abs(tc_pred - gl2_data[i]['tc']) / gl2_data[i]['tc'])
err_gl2_eff = np.array(err_gl2_eff)
print(f"LOOCV: 中位{np.median(err_gl2_eff)*100:.0f}%, 2倍内{np.mean(err_gl2_eff<=1)*100:.0f}%, 5倍内{np.mean(err_gl2_eff<=4)*100:.0f}%")

err_split_eff = np.concatenate([res_gl1['err'], err_gl2_eff])
print(f"GL(1)+GL(2)_eff合并: 中位{np.median(err_split_eff)*100:.0f}%, 2倍内{np.mean(err_split_eff<=1)*100:.0f}%, 5倍内{np.mean(err_split_eff<=4)*100:.0f}%")

# ============================================================
# 最优结果: 用全局统一公式的LOOCV预测值
# ============================================================
print(f"\n{'='*80}")
print("完整计算链路 — 每个材料的Tc预测")
print("="*80)

# 用全局统一公式
a_f, lam_f, p_f, q_f, r_f, s_f, b_f = params_u
print(f"\n公式:")
print(f"  γ_eff = γ_n + {lam_f:.4f}·j(j+1)")
print(f"  ln(K_eff) = {a_f:.4f}·γ_eff + {p_f:.4f}·ln(G) + {q_f:.4f}·ln(θ_D) + {r_f:.4f}·ln(B) + {s_f:.4f}·ln(N) + {b_f:.4f}")
print(f"  Tc = √(8·Δδ₀²·K_eff·θ_D / (9·ln2))")

# LOOCV预测
predictions = []
for i in range(n_data):
    X_tr = np.delete(X_u, i, axis=0)
    y_tr = np.delete(y_lnk, i)
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    gamma_eff = data[i]['gamma_n'] + lam_opt * data[i]['casimir']
    ln_k = coef[0]*gamma_eff + coef[1]*math.log(data[i]['G']) + coef[2]*math.log(data[i]['theta_D']) + coef[3]*math.log(data[i]['B']) + coef[4]*math.log(data[i]['N']) + coef[5]
    k_eff = math.exp(ln_k)
    tc_pred = math.sqrt(8 * data[i]['dd0']**2 * k_eff * data[i]['theta_D'] / (9 * LN2))
    err = abs(tc_pred - data[i]['tc']) / data[i]['tc']
    predictions.append({
        'formula': data[i]['formula'],
        'cat': data[i]['cat'],
        'gl': data[i]['gl'],
        'j': data[i]['j'],
        'gamma_n': data[i]['gamma_n'],
        'gamma_eff': gamma_eff,
        'G': data[i]['G'],
        'theta_D': data[i]['theta_D'],
        'dd0': data[i]['dd0'],
        'B': data[i]['B'],
        'N': data[i]['N'],
        'k_eff': k_eff,
        'tc_pred': tc_pred,
        'tc_exp': data[i]['tc'],
        'err': err,
    })

# 按误差排序输出
predictions.sort(key=lambda x: x['err'])

print(f"\n{'材料':<25} {'GL':>3} {'j':>2} {'γ_eff':>7} {'Tc_exp':>8} {'Tc_pred':>8} {'误差%':>7}")
print("-"*70)
for p in predictions[:20]:
    print(f"{p['formula']:<25} GL{p['gl']} {p['j']:>2} {p['gamma_eff']:>7.2f} {p['tc_exp']:>8.2f} {p['tc_pred']:>8.2f} {p['err']*100:>7.1f}%")
print("  ...")
for p in predictions[-10:]:
    print(f"{p['formula']:<25} GL{p['gl']} {p['j']:>2} {p['gamma_eff']:>7.2f} {p['tc_exp']:>8.2f} {p['tc_pred']:>8.2f} {p['err']*100:>7.1f}%")

# 详细计算链路示例
print(f"\n{'='*80}")
print("详细计算链路示例")
print("="*80)

for pred in predictions[:3]:
    print(f"\n--- {pred['formula']} (Tc_exp={pred['tc_exp']:.2f}K) ---")
    print(f"  类别: {pred['cat']}, GL({pred['gl']}), j={pred['j']}")
    print(f"  环节1: γ_n = {pred['gamma_n']:.4f} (黎曼零点)")
    print(f"  环节2: γ_eff = {pred['gamma_n']:.4f} + {lam_opt:.4f}×{pred['j']*(pred['j']+1)} = {pred['gamma_eff']:.4f}")
    print(f"  环节3: G = {pred['G']:.4e}, θ_D = {pred['theta_D']:.2f}K, Δδ₀ = {pred['dd0']:.4e}")
    print(f"  环节4: B = {pred['B']:.4e}, N = {pred['N']}")
    ln_k_val = a_f*pred['gamma_eff'] + p_f*math.log(pred['G']) + q_f*math.log(pred['theta_D']) + r_f*math.log(pred['B']) + s_f*math.log(pred['N']) + b_f
    print(f"  环节5: ln(K_eff) = {a_f:.4f}×{pred['gamma_eff']:.4f} + {p_f:.4f}×{math.log(pred['G']):.4f} + {q_f:.4f}×{math.log(pred['theta_D']):.4f} + {r_f:.4f}×{math.log(pred['B']):.4f} + {s_f:.4f}×{math.log(pred['N']):.4f} + {b_f:.4f}")
    print(f"         = {ln_k_val:.4f}")
    print(f"  环节6: K_eff = exp({ln_k_val:.4f}) = {pred['k_eff']:.4e}")
    tc_calc = math.sqrt(8 * pred['dd0']**2 * pred['k_eff'] * pred['theta_D'] / (9 * LN2))
    print(f"  环节7: Tc = √(8×{pred['dd0']**2:.4e}×{pred['k_eff']:.4e}×{pred['theta_D']:.2f} / (9×{LN2:.4f}))")
    print(f"         = {tc_calc:.4f} K")
    print(f"  实验: Tc = {pred['tc_exp']:.4f} K, 误差 = {pred['err']*100:.1f}%")

# ============================================================
# 精度统计
# ============================================================
errs_all = np.array([p['err'] for p in predictions])
errs_gl1 = np.array([p['err'] for p in predictions if p['gl'] == 1])
errs_gl2 = np.array([p['err'] for p in predictions if p['gl'] == 2])

print(f"\n{'='*80}")
print("精度统计")
print("="*80)
print(f"{'类别':<25} {'n':>4} {'中位%':>7} {'均值%':>7} {'2倍%':>6} {'5倍%':>6} {'10倍%':>6}")
print("-"*65)
for label, errs in [("全部", errs_all), ("GL(1)常规", errs_gl1), ("GL(2)非常规", errs_gl2)]:
    print(f"{label:<25} {len(errs):>4} {np.median(errs)*100:>7.1f} {np.mean(errs)*100:>7.1f} {np.mean(errs<=1)*100:>6.0f} {np.mean(errs<=4)*100:>6.0f} {np.mean(errs<=9)*100:>6.0f}")

# 各类别详细
print(f"\n各类别精度:")
for cat in sorted(set(p['cat'] for p in predictions)):
    cat_errs = np.array([p['err'] for p in predictions if p['cat'] == cat])
    gl = [p['gl'] for p in predictions if p['cat'] == cat][0]
    print(f"  {cat:<30} [GL{gl}] n={len(cat_errs):>3}, 中位{np.median(cat_errs)*100:>5.0f}%, 2倍内{np.mean(cat_errs<=1)*100:>3.0f}%, 5倍内{np.mean(cat_errs<=4)*100:>3.0f}%")

# ============================================================
# 总结
# ============================================================
print(f"\n{'='*80}")
print("总结 — 完整第一性Tc计算链路")
print("="*80)
print(f"公式: Tc = √(8·Δδ₀²·K_eff·θ_D / (9·ln2))")
print(f"      K_eff = exp({a_f:.4f}·γ_eff + {p_f:.4f}·ln(G) + {q_f:.4f}·ln(θ_D) + {r_f:.4f}·ln(B) + {s_f:.4f}·ln(N) + {b_f:.4f})")
print(f"      γ_eff = γ_n + {lam_opt:.4f}·j(j+1)")
print(f"      γ_n = 黎曼零点 (GL(1)电磁因子同步算符本征值)")
print(f"      j(j+1) = SU(2) Casimir (GL(2)自旋因子同步算符本征值)")
print(f"      Δδ₀ = √(C²/l² · 3ℏ/(4ω_D) · (1-f) · Σ(1/m_i+1/m_j))")
print(f"      G = (1/l)·√((1-f)·Σ(1/m_i+1/m_j))")
print(f"")
print(f"精度: 中位{np.median(errs_all)*100:.0f}%, 2倍内{np.mean(errs_all<=1)*100:.0f}%, 5倍内{np.mean(errs_all<=4)*100:.0f}%")
print(f"      GL(1): 中位{np.median(errs_gl1)*100:.0f}%, GL(2): 中位{np.median(errs_gl2)*100:.0f}%")