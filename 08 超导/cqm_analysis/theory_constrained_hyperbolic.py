"""理论约束双曲映射: gamma_n = 53.4 - 8.37/lambda_ep

从CQM理论文档两个独立K_0拟合导出:
  K_0 = 7.77e11 * exp(0.369*gamma_n)  (R^2=0.960)
  K_0 = 2.85e20 * exp(-3.09/lambda_ep)  (R^2=0.848)
匹配: 0.369*gamma_n = -3.09/lambda_ep + ln(2.85e20/7.77e11)
  => gamma_n = 53.4 - 8.37/lambda_ep

A=53.4, B=8.37 从理论导出, 非网格搜索!
只需搜索 lambda_ep = lambda_0 + alpha*inv_mass + beta*dp + gamma*o + delta*log_sg + eps*aniso
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework'); from atom_db import ATOM_DB
sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_analysis')
import csv, re, math, numpy as np
from collections import defaultdict
from cqm_no_classification_framework import (
    parse_formula, build_first_principles_Cmol, interpolate_gamma_n,
    predict_tc_first_principles, RIEMANN_ZEROS,
    HBAR, KB, AMU, C2, LN2,
    madelung_config, valence_orbitals, ATOMIC_NUMBERS, compute_atom_features
)

# 理论常数 (从CQM文档导出, 非网格搜索)
A_THEORY = 53.4  # gamma_n上限(强耦合极限)
B_THEORY = 8.37  # 耦合强度尺度

data = []
with open(r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_analysis\superconductors_deduplicated.csv', 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc > 0: data.append({'formula': row['材料(化学式)'], 'cat': row['类别'], 'tc_exp': tc})

print(f"加载 {len(data)} 个材料")
print(f"\n理论约束: gamma_n = {A_THEORY} - {B_THEORY}/lambda_ep; B=8.37")

# 预计算
precomputed = []
for d in data:
    atoms = parse_formula(d['formula'])
    if not atoms: continue
    C_mol, block_info = build_first_principles_Cmol(atoms)
    eigvals = np.sort(np.linalg.eigvalsh(C_mol))
    n_dim = len(eigvals)
    if n_dim < 2: continue

    els = list(atoms.keys())
    n_atoms = sum(atoms.values())
    sg = eigvals[1] - eigvals[0]
    ev_mean = np.mean(eigvals)
    anisotropy = np.std(eigvals / ev_mean) if ev_mean > 0 else 0

    atom_features = compute_atom_features(atoms)
    inv_mass_avg = atom_features['inv_mass_avg']
    dp_hybrid = atom_features['dp_hybrid']
    o_fraction = atom_features['o_fraction']
    f_fraction = atom_features['f_fraction']
    d0_fraction = atom_features['d0_fraction']

    total_m = sum(atoms[el] * ATOM_DB[el][0] for el in els)
    avg_r = sum(atoms[el] * ATOM_DB[el][2] for el in els) / n_atoms
    l = 2 * avg_r * 1e-10
    theta_d = sum(atoms[el] * ATOM_DB[el][1] for el in els) / n_atoms
    if theta_d <= 0: continue

    n_eff = max(2, n_atoms)
    f_corr = 1.0 - 0.3 * (1.0 - 1.0/n_eff)
    edge_sum = 0
    for i in range(len(els)):
        for j in range(i+1, len(els)):
            mi = atoms[els[i]] * ATOM_DB[els[i]][0] * AMU
            mj = atoms[els[j]] * ATOM_DB[els[j]][0] * AMU
            edge_sum += (1.0/mi + 1.0/mj)
    if not edge_sum:
        mi = total_m * AMU / n_atoms
        edge_sum = max(1, n_eff*(n_eff-1)/2) * 2.0 / mi

    G = (1.0/l) * math.sqrt((1.0-f_corr) * edge_sum)
    omega_d = theta_d * KB / HBAR
    dd0_sq = (C2/l**2) * (3*HBAR/(4*omega_d)) * (1-f_corr) * edge_sum
    dd0 = math.sqrt(abs(dd0_sq))
    suppress = math.exp(-15.0 * f_fraction) * math.exp(-3.0 * d0_fraction)
    G_safe = max(G, 1e-6)
    tc_coeff = math.sqrt(8 * dd0**2 * 7.77e11 * G_safe**(-3.0/4.0) * theta_d**(9.0/8.0) * theta_d / (9 * LN2)) * suppress

    sg_safe = max(sg, 0.05)
    precomputed.append({
        'formula': d['formula'], 'cat': d['cat'], 'tc_exp': d['tc_exp'],
        'log_inv_sg': math.log(1.0/sg_safe), 'anisotropy': anisotropy,
        'inv_mass_avg': inv_mass_avg, 'dp_hybrid': dp_hybrid, 'o_fraction': o_fraction,
        'tc_coeff': tc_coeff,
    })

print(f"有效: {len(precomputed)}")

# ============================================================
# 理论约束双曲映射: gamma_n = A - B/lambda_ep
# A=53.4, B=8.37 固定(理论导出)
# lambda_ep = lam0 + a*inv_mass + b*dp + c*o + d*log_sg + e*aniso
# 只搜索 lam0, a, b, c, d, e
# ============================================================

def eval_theory(lam0, a, b, c, d, e):
    errs = []
    for p in precomputed:
        lam = lam0 + a*p['inv_mass_avg'] + b*p['dp_hybrid'] + c*p['o_fraction'] + d*p['log_inv_sg'] + e*p['anisotropy']
        if lam <= 0.01:
            lam = 0.01
        gamma_n = A_THEORY - B_THEORY / lam
        if gamma_n < 1:
            gamma_n = RIEMANN_ZEROS[0]
        tc_pred = p['tc_coeff'] * math.exp(0.369 * gamma_n / 2.0)
        if tc_pred > 0:
            ratio = tc_pred / p['tc_exp']
            errs.append(max(ratio, 1.0/ratio) - 1.0)
    errs = np.array(errs)
    return np.median(errs), np.sum(errs<1)*100/len(errs), np.sum(errs<4)*100/len(errs)

# 线性基准
def eval_linear(base, a, b, c, d, e):
    errs = []
    for p in precomputed:
        n_cont = base + a*p['log_inv_sg'] + b*p['anisotropy'] + c*p['inv_mass_avg'] + d*p['dp_hybrid'] + e*p['o_fraction']
        gamma_n = interpolate_gamma_n(max(1.0, n_cont))
        tc_pred = p['tc_coeff'] * math.exp(0.369 * gamma_n / 2.0)
        if tc_pred > 0:
            ratio = tc_pred / p['tc_exp']
            errs.append(max(ratio, 1.0/ratio) - 1.0)
    errs = np.array(errs)
    return np.median(errs), np.sum(errs<1)*100/len(errs), np.sum(errs<4)*100/len(errs)

med_lin, p2_lin, p5_lin = eval_linear(4.00, 0.50, 0.35, 13.00, 0.05, 5.50)
print(f"\n线性(当前): 中位{med_lin*100:.1f}%  2倍内{p2_lin:.1f}%  5倍内{p5_lin:.1f}%")

# ============================================================
# 网格搜索 lambda_ep 系数 (A,B固定)
# ============================================================

print(f"\n网格搜索 lambda_ep 系数 (A={A_THEORY}, B={B_THEORY} 固定)...")
best_score = 0; best_params = None

# lambda_ep范围估计:
# 典型超导体 lambda_ep ~ 0.1-2.0
# inv_mass_avg ~ 0.005-0.5, 系数a ~ 1-5
# dp_hybrid ~ 0-5, 系数b ~ 0-0.5
# o_fraction ~ 0-0.75, 系数c ~ 0-2
# log(1/sg) ~ 0-3, 系数d ~ 0-0.5
# aniso ~ 0-0.6, 系数e ~ 0-1

for lam0 in np.arange(0.05, 0.5, 0.05):
    for a in np.arange(0.5, 5.0, 0.5):
        for c in np.arange(0.0, 3.0, 0.5):
            for d in np.arange(0.0, 0.5, 0.1):
                for e in np.arange(0.0, 1.0, 0.2):
                    med, p2, p5 = eval_theory(lam0, a, 0.0, c, d, e)
                    score = p2 + 0.5 * p5
                    if score > best_score:
                        best_score = score
                        best_params = (lam0, a, 0.0, c, d, e, med, p2, p5)

lam0, a, b, c, d, e, med, p2, p5 = best_params
print(f"\n粗最佳: lam0={lam0:.2f} a={a:.1f} b={b:.1f} c={c:.1f} d={d:.1f} e={e:.1f}")
print(f"  中位{med*100:.1f}%  2倍内{p2:.1f}%  5倍内{p5:.1f}%")

# 加入dp_hybrid
print(f"\n加入dp_hybrid...")
for b in np.arange(0.0, 0.5, 0.05):
    med, p2, p5 = eval_theory(lam0, a, b, c, d, e)
    score = p2 + 0.5 * p5
    if score > best_score:
        best_score = score
        best_params = (lam0, a, b, c, d, e, med, p2, p5)

lam0, a, b, c, d, e, med, p2, p5 = best_params
print(f"  b={b:.2f}: 中位{med*100:.1f}%  2倍内{p2:.1f}%  5倍内{p5:.1f}%")

# 精细
print(f"\n精细搜索...")
for lam0 in np.arange(max(0.01, best_params[0]-0.05), best_params[0]+0.06, 0.02):
    for a in np.arange(max(0.1, best_params[1]-0.3), best_params[1]+0.4, 0.1):
        for b in np.arange(max(0, best_params[2]-0.05), best_params[2]+0.06, 0.02):
            for c in np.arange(max(0, best_params[3]-0.3), best_params[3]+0.4, 0.1):
                for d in np.arange(max(0, best_params[4]-0.05), best_params[4]+0.06, 0.02):
                    for e in np.arange(max(0, best_params[5]-0.1), best_params[5]+0.15, 0.05):
                        med, p2, p5 = eval_theory(lam0, a, b, c, d, e)
                        score = p2 + 0.5 * p5
                        if score > best_score:
                            best_score = score
                            best_params = (lam0, a, b, c, d, e, med, p2, p5)

lam0, a, b, c, d, e, med, p2, p5 = best_params
print(f"精细最佳: lam0={lam0:.3f} a={a:.2f} b={b:.3f} c={c:.2f} d={d:.3f} e={e:.2f}")
print(f"  中位{med*100:.1f}%  2倍内{p2:.1f}%  5倍内{p5:.1f}%")

# ============================================================
# 也搜索A和B (验证理论值)
# ============================================================

print(f"\n验证A,B理论值 (允许A,B变化)...")
best_score2 = 0; best_params2 = None

for A in np.arange(45, 60, 2.0):
    for B in np.arange(5, 12, 1.0):
        for lam0 in np.arange(0.05, 0.3, 0.05):
            for a in np.arange(0.5, 4.0, 0.5):
                for c in np.arange(0.0, 2.5, 0.5):
                    errs = []
                    for p in precomputed:
                        lam = lam0 + a*p['inv_mass_avg'] + c*p['o_fraction']
                        lam = max(0.01, lam)
                        gn = A - B / lam
                        if gn < 1: gn = RIEMANN_ZEROS[0]
                        tc_pred = p['tc_coeff'] * math.exp(0.369 * gn / 2.0)
                        if tc_pred > 0:
                            ratio = tc_pred / p['tc_exp']
                            errs.append(max(ratio, 1.0/ratio) - 1.0)
                    errs = np.array(errs)
                    p2 = np.sum(errs<1)*100/len(errs); p5 = np.sum(errs<4)*100/len(errs)
                    score = p2 + 0.5 * p5
                    if score > best_score2:
                        best_score2 = score
                        best_params2 = (A, B, lam0, a, c, np.median(errs), p2, p5)

A_fit, B_fit, _, _, _, med_fit, p2_fit, p5_fit = best_params2
print(f"拟合A={A_fit:.0f} B={B_fit:.1f}: 中位{med_fit*100:.1f}%  2倍内{p2_fit:.1f}%  5倍内{p5_fit:.1f}%")
print(f"理论A={A_THEORY} B={B_THEORY}")
print(f"差异: dA={A_fit-A_THEORY:+.1f} dB={B_fit-B_THEORY:+.1f}")

# ============================================================
# 详细结果 (理论A,B)
# ============================================================

print(f"\n{'='*60}")
print(f"理论约束双曲映射:")
print(f"  gamma_n = {A_THEORY} - {B_THEORY}/lambda_ep")
print(f"  lambda_ep = {lam0:.3f} + {a:.2f}*inv_mass + {b:.3f}*dp + {c:.2f}*o + {d:.3f}*log_sg + {e:.2f}*aniso")

results = []
for p in precomputed:
    lam = lam0 + a*p['inv_mass_avg'] + b*p['dp_hybrid'] + c*p['o_fraction'] + d*p['log_inv_sg'] + e*p['anisotropy']
    lam = max(0.01, lam)
    gamma_n = A_THEORY - B_THEORY / lam
    if gamma_n < 1: gamma_n = RIEMANN_ZEROS[0]
    tc_pred = p['tc_coeff'] * math.exp(0.369 * gamma_n / 2.0)
    if tc_pred > 0:
        ratio = tc_pred / p['tc_exp']
        err = max(ratio, 1.0/ratio) - 1.0
        results.append({**p, 'tc_pred': tc_pred, 'error': err, 'gamma_n': gamma_n, 'lambda_ep': lam})

errs = np.array([r['error'] for r in results])
print(f"\n理论双曲: 中位{np.median(errs)*100:.1f}%  2倍内{np.sum(errs<1)*100/len(errs):.1f}%  5倍内{np.sum(errs<4)*100/len(errs):.1f}%")
print(f"线性(对比): 中位{med_lin*100:.1f}%  2倍内{p2_lin:.1f}%  5倍内{p5_lin:.1f}%")

# 按类别
print(f"\n按类别:")
cat_th = defaultdict(list); cat_lin = defaultdict(list)
for r in results: cat_th[r['cat']].append(r['error'])
for p in precomputed:
    n_cont = 4.00 + 0.50*p['log_inv_sg'] + 0.35*p['anisotropy'] + 13.00*p['inv_mass_avg'] + 0.05*p['dp_hybrid'] + 5.50*p['o_fraction']
    gamma_n = interpolate_gamma_n(max(1.0, n_cont))
    tc_pred = p['tc_coeff'] * math.exp(0.369 * gamma_n / 2.0)
    if tc_pred > 0:
        err = max(tc_pred/p['tc_exp'], p['tc_exp']/tc_pred) - 1.0
        cat_lin[p['cat']].append(err)

for cat in sorted(cat_th.keys()):
    e_t = cat_th[cat]; e_l = cat_lin.get(cat, [])
    print(f"  {cat:25s}: 理论{np.median(e_t)*100:5.0f}%/{np.sum(np.array(e_t)<1)*100/len(e_t):3.0f}%  "
          f"线性{np.median(e_l)*100:5.0f}%/{np.sum(np.array(e_l)<1)*100/len(e_l):3.0f}%  ({len(e_t)})")

# 最好/最差
print(f"\n最好10个:")
for r in sorted(results, key=lambda x: x['error'])[:10]:
    print(f"  {r['formula']:15s} exp={r['tc_exp']:8.1f}K pred={r['tc_pred']:10.1f}K err={r['error']*100:.0f}% gamma={r['gamma_n']:.1f} lam={r['lambda_ep']:.3f}")

print(f"\n最差10个:")
for r in sorted(results, key=lambda x: x['error'], reverse=True)[:10]:
    print(f"  {r['formula']:15s} exp={r['tc_exp']:8.1f}K pred={r['tc_pred']:10.1f}K err={r['error']*100:.0f}% gamma={r['gamma_n']:.1f} lam={r['lambda_ep']:.3f}")

# lambda_ep分布
print(f"\n--- lambda_ep按类别 ---")
cat_lam = defaultdict(list)
for r in results: cat_lam[r['cat']].append(r['lambda_ep'])
for cat in sorted(cat_lam.keys()):
    lams = cat_lam[cat]
    print(f"  {cat:25s}: lam中位{np.median(lams):.3f}  范围[{min(lams):.3f}, {max(lams):.3f}]")

# 物理验证
print(f"\n--- 物理验证 ---")
print(f"  理论: K_0 = 7.77e11*exp(0.369*gamma_n) = 2.85e20*exp(-3.09/lambda_ep)")
print(f"  => gamma_n = {A_THEORY} - {B_THEORY}/lambda_ep")
print(f"  典型lambda_ep=0.5: gamma_n = {A_THEORY - B_THEORY/0.5:.1f}")
print(f"  典型lambda_ep=1.0: gamma_n = {A_THEORY - B_THEORY/1.0:.1f}")
print(f"  典型lambda_ep=2.0: gamma_n = {A_THEORY - B_THEORY/2.0:.1f}")
print(f"  拟合A={A_fit:.0f} B={B_fit:.1f} vs 理论A={A_THEORY} B={B_THEORY}")