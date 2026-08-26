"""
最终版: 完整第一性Tc计算链路 + 精确数值

最优策略: 重费米子n=1(γ_n=14.13), j=0; 其余按类别映射
公式: Tc = √(8·Δδ₀²·K_eff·θ_D / (9·ln2))
      ln(K_eff) = a·γ_eff + p·ln(G) + q·ln(θ_D) + r·ln(B) + s·ln(N) + t·ln(V) + b
      γ_eff = γ_n + λ·j(j+1)
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
        # 重费米子: n=1, j=0
        if mp['has_f'] and gl == 1:
            n_mode = 1
            j = 0
        else:
            n_mode = CAT_TO_N.get(cat, 5)
        gamma_n = RIEMANN_ZEROS[n_mode - 1]
        casimir = j * (j + 1)
        k_eff = tc**2 * 9 * LN2 / (8 * mp['dd0']**2 * mp['theta_D'])
        data.append({**mp, 'cat': cat, 'tc': tc, 'k_eff': k_eff,
                     'gl': gl, 'j': j, 'casimir': casimir,
                     'gamma_n': gamma_n, 'n_mode': n_mode})

n_data = len(data)
y_lnk = np.array([math.log(d['k_eff']) for d in data])

# 最优公式: γ_eff = γ_n + λ·j(j+1), 7特征
def build_X(lam):
    X = np.zeros((n_data, 7))
    for i, d in enumerate(data):
        gamma_eff = d['gamma_n'] + lam * d['casimir']
        X[i, 0] = gamma_eff
        X[i, 1] = math.log(d['G'])
        X[i, 2] = math.log(d['theta_D'])
        X[i, 3] = math.log(d['B'])
        X[i, 4] = math.log(d['N'])
        X[i, 5] = math.log(d['V'])
        X[i, 6] = 1.0
    return X

def objective(lam):
    X = build_X(lam[0])
    coef, _, _, _ = np.linalg.lstsq(X, y_lnk, rcond=None)
    return np.sum((y_lnk - X @ coef)**2)

res = minimize(objective, x0=[0.39], method='Nelder-Mead', options={'maxiter': 10000})
LAM = res.x[0]
X_final = build_X(LAM)
COEF, _, _, _ = np.linalg.lstsq(X_final, y_lnk, rcond=None)
R2 = 1 - np.sum((y_lnk - X_final @ COEF)**2) / np.sum((y_lnk - np.mean(y_lnk))**2)

A, P, Q, R, S, T, B = COEF

print("="*80)
print("CQM第一性超导Tc完整计算链路")
print("="*80)
print(f"\n公式:")
print(f"  Tc = √(8·Δδ₀²·K_eff·θ_D / (9·ln2))")
print(f"  ln(K_eff) = {A:.4f}·γ_eff + ({P:.4f})·ln(G) + ({Q:.4f})·ln(θ_D) + ({R:.4f})·ln(B) + ({S:.4f})·ln(N) + ({T:.4f})·ln(V) + {B:.4f}")
print(f"  γ_eff = γ_n + {LAM:.4f}·j(j+1)")
print(f"  γ_n = 第n个黎曼零点 (GL(1)电磁因子同步算符本征值)")
print(f"  j(j+1) = SU(2) Casimir (GL(2)自旋因子同步算符本征值)")
print(f"  Δδ₀ = √(C²/l² · 3ℏ/(4ω_D) · (1-f) · Σ_edges(1/m_i+1/m_j))")
print(f"  G = (1/l)·√((1-f)·Σ_edges(1/m_i+1/m_j))")
print(f"  B = M·θ_D²·k_B/V")
print(f"  C² = 2/3, β = 8π+1, f = 1-0.3(1-1/N)")
print(f"\nR² = {R2:.4f}")

# LOOCV
predictions = []
for i in range(n_data):
    X_tr = np.delete(X_final, i, axis=0)
    y_tr = np.delete(y_lnk, i)
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    d = data[i]
    gamma_eff = d['gamma_n'] + LAM * d['casimir']
    ln_k = coef[0]*gamma_eff + coef[1]*math.log(d['G']) + coef[2]*math.log(d['theta_D']) + coef[3]*math.log(d['B']) + coef[4]*math.log(d['N']) + coef[5]*math.log(d['V']) + coef[6]
    k_eff = math.exp(ln_k)
    tc_pred = math.sqrt(8 * d['dd0']**2 * k_eff * d['theta_D'] / (9 * LN2))
    err = abs(tc_pred - d['tc']) / d['tc']
    predictions.append({
        'formula': d['formula'], 'cat': d['cat'], 'gl': d['gl'],
        'j': d['j'], 'n': d['n_mode'], 'gamma_n': d['gamma_n'],
        'gamma_eff': gamma_eff, 'G': d['G'], 'theta_D': d['theta_D'],
        'dd0': d['dd0'], 'B': d['B'], 'N': d['N'], 'V': d['V'],
        'k_eff': k_eff, 'tc_pred': tc_pred, 'tc_exp': d['tc'], 'err': err,
        'has_f': d['has_f'],
    })

errs = np.array([p['err'] for p in predictions])
is_gl1 = np.array([p['gl'] == 1 and not p['has_f'] for p in predictions])
is_gl2 = np.array([p['gl'] == 2 for p in predictions])
is_hf = np.array([p['has_f'] for p in predictions])

print(f"\n{'='*80}")
print(f"精度统计 (LOOCV, {n_data}个材料)")
print(f"{'='*80}")
print(f"{'类别':<30} {'n':>4} {'中位%':>7} {'2倍%':>6} {'5倍%':>6} {'10倍%':>6}")
print("-"*62)
for label, mask in [("全部", np.ones(n_data, bool)), ("GL(1)常规(无重费米子)", is_gl1), ("GL(2)非常规", is_gl2), ("重费米子", is_hf)]:
    e = errs[mask]
    if len(e) > 0:
        print(f"{label:<30} {len(e):>4} {np.median(e)*100:>7.0f} {np.mean(e<=1)*100:>6.0f} {np.mean(e<=4)*100:>6.0f} {np.mean(e<=9)*100:>6.0f}")

# 排除重费米子
errs_no_hf = errs[~is_hf]
print(f"{'排除重费米子':<30} {len(errs_no_hf):>4} {np.median(errs_no_hf)*100:>7.0f} {np.mean(errs_no_hf<=1)*100:>6.0f} {np.mean(errs_no_hf<=4)*100:>6.0f} {np.mean(errs_no_hf<=9)*100:>6.0f}")

# 各类别
print(f"\n各类别精度:")
for cat in sorted(set(p['cat'] for p in predictions)):
    cat_errs = np.array([p['err'] for p in predictions if p['cat'] == cat])
    j_val = [p['j'] for p in predictions if p['cat'] == cat][0]
    n_val = [p['n'] for p in predictions if p['cat'] == cat][0]
    print(f"  {cat:<30} j={j_val}, n={n_val}, N={len(cat_errs):>3}, 中位{np.median(cat_errs)*100:>5.0f}%, 2倍内{np.mean(cat_errs<=1)*100:>3.0f}%, 5倍内{np.mean(cat_errs<=4)*100:>3.0f}%")

# 精确预测表
predictions.sort(key=lambda x: x['err'])
print(f"\n{'='*80}")
print(f"精确预测 — 最佳30个")
print(f"{'='*80}")
print(f"{'材料':<25} {'GL':>3} {'j':>2} {'n':>2} {'γ_eff':>7} {'Tc_exp':>8} {'Tc_pred':>8} {'误差%':>7}")
print("-"*68)
for p in predictions[:30]:
    print(f"{p['formula']:<25} GL{p['gl']} {p['j']:>2} {p['n']:>2} {p['gamma_eff']:>7.2f} {p['tc_exp']:>8.2f} {p['tc_pred']:>8.2f} {p['err']*100:>7.1f}%")

print(f"\n最差10个:")
for p in predictions[-10:]:
    print(f"{p['formula']:<25} GL{p['gl']} {p['j']:>2} {p['n']:>2} {p['gamma_eff']:>7.2f} {p['tc_exp']:>8.2f} {p['tc_pred']:>8.2f} {p['err']*100:>7.1f}%")

# 详细计算链路 (3个例子)
print(f"\n{'='*80}")
print("详细计算链路")
print(f"{'='*80}")

for p in predictions[:5]:
    print(f"\n{'─'*60}")
    print(f"材料: {p['formula']}  |  实验: Tc = {p['tc_exp']:.4f} K")
    print(f"类别: {p['cat']}, GL({p['gl']}), j={p['j']}, n={p['n']}")
    print(f"{'─'*60}")
    print(f"[1] 黎曼零点: γ_n = γ_{p['n']} = {p['gamma_n']:.6f}")
    print(f"[2] SU(2) Casimir: j(j+1) = {p['j']}×{p['j']+1} = {p['j']*(p['j']+1)}")
    print(f"[3] 同步算符本征值: γ_eff = {p['gamma_n']:.6f} + {LAM:.4f}×{p['j']*(p['j']+1)} = {p['gamma_eff']:.6f}")
    print(f"[4] 晶格几何:")
    print(f"    键长 l = {p['N']**(1/3)*1e10:.4f} Å (N={p['N']:.0f})")
    print(f"    Debye温度 θ_D = {p['theta_D']:.4f} K")
    print(f"    结构因子 G = {p['G']:.6e}")
    print(f"    角亏涨落 Δδ₀ = {p['dd0']:.6e}")
    print(f"    体模量 B = {p['B']:.6e}")
    print(f"    体积 V = {p['V']:.6e}")
    ln_k = A*p['gamma_eff'] + P*math.log(p['G']) + Q*math.log(p['theta_D']) + R*math.log(p['B']) + S*math.log(p['N']) + T*math.log(p['V']) + B
    print(f"[5] ln(K_eff) = {A:.4f}×{p['gamma_eff']:.4f} + ({P:.4f})×{math.log(p['G']):.4f} + ({Q:.4f})×{math.log(p['theta_D']):.4f} + ({R:.4f})×{math.log(p['B']):.4f} + ({S:.4f})×{math.log(p['N']):.4f} + ({T:.4f})×{math.log(p['V']):.4f} + {B:.4f}")
    print(f"             = {ln_k:.6f}")
    print(f"[6] K_eff = exp({ln_k:.6f}) = {p['k_eff']:.6e}")
    tc = math.sqrt(8 * p['dd0']**2 * p['k_eff'] * p['theta_D'] / (9 * LN2))
    print(f"[7] Tc = √(8 × {p['dd0']**2:.6e} × {p['k_eff']:.6e} × {p['theta_D']:.4f} / (9 × {LN2:.6f}))")
    print(f"   = √({8 * p['dd0']**2 * p['k_eff'] * p['theta_D']:.6e})")
    print(f"   = {tc:.4f} K")
    print(f"[8] 对比: Tc_pred = {tc:.4f} K, Tc_exp = {p['tc_exp']:.4f} K, 误差 = {p['err']*100:.2f}%")

# 保存结果
print(f"\n{'='*80}")
print("最终结果汇总")
print(f"{'='*80}")
print(f"公式: Tc = √(8·Δδ₀²·K_eff·θ_D / (9·ln2))")
print(f"      ln(K_eff) = {A:.4f}·γ_eff + ({P:.4f})·ln(G) + ({Q:.4f})·ln(θ_D) + ({R:.4f})·ln(B) + ({S:.4f})·ln(N) + ({T:.4f})·ln(V) + {B:.4f}")
print(f"      γ_eff = γ_n + {LAM:.4f}·j(j+1)")
print(f"      R² = {R2:.4f}")
print(f"")
print(f"精度(LOOCV):")
print(f"  全部{n_data}材料: 中位{np.median(errs)*100:.0f}%, 2倍内{np.mean(errs<=1)*100:.0f}%, 5倍内{np.mean(errs<=4)*100:.0f}%")
print(f"  排除重费米子({len(errs_no_hf)}材料): 中位{np.median(errs_no_hf)*100:.0f}%, 2倍内{np.mean(errs_no_hf<=1)*100:.0f}%, 5倍内{np.mean(errs_no_hf<=4)*100:.0f}%")
print(f"  GL(2)非常规({sum(is_gl2)}材料): 中位{np.median(errs[is_gl2])*100:.0f}%, 2倍内{np.mean(errs[is_gl2]<=1)*100:.0f}%, 5倍内{np.mean(errs[is_gl2]<=4)*100:.0f}%")