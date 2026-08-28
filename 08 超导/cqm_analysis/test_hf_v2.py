"""测试重费米子修正v2: f原子分数 × (1-d_partial) 作为额外抑制

核心思路:
  - 铁基超导体: f电子在稀土层, Fe d电子在费米面 → f是旁观者 → 弱抑制(电子分数×0.5)
  - 重费米子: f电子在费米面, 无d电子 → f参与Kondo → 强抑制(原子分数)
  - 连续参数: d_partial_fraction区分两种情况
"""

import sys, os, math, csv
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cqm_no_classification_framework import *

def compute_d_features(atoms):
    els = list(atoms.keys())
    n_atoms = sum(atoms.values())
    d_partial_count = 0
    d_empty_count = 0
    d_full_count = 0
    d_filling_sum = 0.0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        vo = valence_orbitals(z)
        for l, occ, cap in vo:
            if l == 2:
                if occ == 0: d_empty_count += atoms[el]
                elif occ == cap: d_full_count += atoms[el]
                else: d_partial_count += atoms[el]
                x = occ / cap if cap > 0 else 0
                d_filling_sum += 4 * x * (1 - x) * atoms[el]
                break
    return {
        'd_partial': d_partial_count / n_atoms,
        'd_empty': d_empty_count / n_atoms,
        'd_full': d_full_count / n_atoms,
        'd_filling': d_filling_sum / n_atoms,
    }

def compute_f_atom_fraction(atoms):
    """原子分数: 有f电子的原子数/总原子数"""
    els = list(atoms.keys())
    n_atoms = sum(atoms.values())
    f_count = 0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        config = madelung_config(z)
        for (n_qn, l_qn), occ in config.items():
            if l_qn == 3 and 0 < occ < 14:
                f_count += atoms[el]
                break
    return f_count / n_atoms

def predict_tc_v2(formula, mode='baseline', alpha=1.0, beta=1.0):
    atoms = parse_formula(formula)
    if not atoms: return 0, {}

    C_mol, block_info = build_first_principles_Cmol(atoms, s_root=0.5)
    if C_mol is None: return 0, {}

    atom_features = compute_atom_features(atoms)
    d_feat = compute_d_features(atoms)
    f_atom = compute_f_atom_fraction(atoms)

    els = list(atoms.keys())
    n_atoms = sum(atoms.values())
    total_m = sum(atoms[el] * ATOM_DB[el][0] for el in els)
    avg_r = sum(atoms[el] * ATOM_DB[el][2] for el in els) / n_atoms
    l = max(2 * avg_r * 1e-10, 1e-20)
    theta_d = sum(atoms[el] * ATOM_DB[el][1] for el in els) / n_atoms
    if theta_d <= 0: return 0, {}

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

    eigvals = np.sort(np.linalg.eigvalsh(C_mol).real)
    sg = eigvals[1] - eigvals[0] if len(eigvals) > 1 else 0.01
    ev_mean = np.mean(eigvals)
    ev_std = np.std(eigvals)
    anisotropy = ev_std / ev_mean if ev_mean > 0 else 0
    skewness = np.mean(((eigvals - ev_mean) / ev_std) ** 3) if ev_std > 0 else 0
    kurtosis = np.mean(((eigvals - ev_mean) / ev_std) ** 4) - 3 if ev_std > 0 else 0
    cond_A = eigvals[-1] / eigvals[0] if eigvals[0] > 0 else 1000.0

    dp_hybrid = atom_features.get('dp_hybrid', 0)
    o_frac = atom_features.get('o_fraction', 0)
    f_elec = atom_features.get('f_fraction', 0)
    d0_frac = atom_features.get('d0_fraction', 0)

    d_partial = d_feat['d_partial']
    d_filling = d_feat['d_filling']

    COEF_EQ8 = 3 * BETA**2 / 16
    eq8_term = 1.5 * COEF_EQ8 * dd0_sq
    sg_safe = max(sg, 0.05)

    # o_fraction修正
    o_eff = o_frac
    if 'o_df' in mode:
        o_eff = o_frac * d_filling * alpha

    n_continuous = (4.00
                    + 0.50 * math.log(1.0 / sg_safe)
                    + C_ANISO * anisotropy
                    + T0_BASE * skewness
                    + T0_BASE * kurtosis
                    + eq8_term
                    + 0.05 * dp_hybrid
                    + C_O * o_eff
                    - 0.75 / cond_A)

    gamma_n = interpolate_gamma_n(n_continuous)
    K_0 = C_GAMMA * math.exp(AG_THEORY * gamma_n)
    G_safe = max(G, 1e-6)
    K_eff = K_0 * G_safe**(-3/4) * theta_d**(9/8)
    Tc_sq = 8 * dd0**2 * K_eff * theta_d / (9 * LN2)
    Tc = math.sqrt(max(0, Tc_sq))

    # f电子抑制 (电子分数 × s_root)
    Tc *= math.exp(-C_F_SUPP * f_elec * 0.5)

    # 重费米子额外抑制: f原子分数 × (1-d_partial) × beta
    # 当有部分填充d时(铁基): 1-d_partial≈0 → 无额外抑制
    # 当无部分填充d时(重费米子): 1-d_partial=1 → 强额外抑制
    if 'hf' in mode:
        hf_supp = f_atom * (1 - d_partial) * beta
        Tc *= math.exp(-C_F_SUPP * hf_supp)

    Tc *= math.exp(-3.0 * d0_frac)
    return Tc, {'gamma_n': gamma_n}

def run_test(mode, alpha=1.0, beta=1.0):
    data_file = os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv')
    results = []
    with open(data_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            formula = row['材料(化学式)']
            try:
                T_exp = float(row['临界温度 Tc (K)'].replace('~','').replace('>','').replace('<',''))
            except: continue
            category = row.get('类别', '')
            Tc_pred, info = predict_tc_v2(formula, mode, alpha, beta)
            if Tc_pred <= 0: continue
            err = abs(Tc_pred - T_exp) / max(T_exp, 0.001)
            results.append((formula, T_exp, Tc_pred, err, category))
    w2 = sum(1 for r in results if r[3] < 1.0)
    w5 = sum(1 for r in results if r[3] < 4.0)
    med = np.median([r[3] for r in results]) * 100
    cats = {}
    for r in results:
        c = r[4]
        if c not in cats: cats[c] = []
        cats[c].append(r[3])
    return results, w2, w5, med, cats

def pr(label, results, w2, w5, med, cats):
    n = len(results)
    print(f"\n{label}: {w2}/{n}={w2/n*100:.1f}% 2x  {w5}/{n}={w5/n*100:.1f}% 5x  med={med:.1f}%")
    for c in ['其他特殊超导体', '其他金属间化合物', '铁基超导体', '铜氧化物高温超导体']:
        if c in cats:
            e = cats[c]
            w = sum(1 for x in e if x < 1.0)
            print(f"    {c}: med={np.median(e)*100:.0f}% 2x={w}/{len(e)}={w/len(e)*100:.0f}%")
    worst = sorted(results, key=lambda x: x[3], reverse=True)[:3]
    for r in worst:
        print(f"    worst: {r[0]:20s} exp={r[1]:8.1f} pred={r[2]:10.1f} err={r[3]*100:.0f}%")

if __name__ == '__main__':
    print("="*70)
    print("重费米子修正v2: f原子分数×(1-d_partial)额外抑制")
    print("="*70)

    r,w2,w5,med,c = run_test('baseline')
    pr("基线", r, w2, w5, med, c)

    print("\n--- 仅重费米子修正 ---")
    for beta in [0.5, 1.0, 1.5, 2.0, 3.0]:
        r,w2,w5,med,c = run_test('hf', beta=beta)
        pr(f"hf beta={beta}", r, w2, w5, med, c)

    print("\n--- 仅氧化物d填充修正 ---")
    for alpha in [0.5, 1.0, 1.5, 2.0]:
        r,w2,w5,med,c = run_test('o_df', alpha=alpha)
        pr(f"o_df alpha={alpha}", r, w2, w5, med, c)

    print("\n--- 组合: o_df + hf ---")
    for alpha in [0.5, 1.0]:
        for beta in [0.5, 1.0, 1.5, 2.0, 3.0]:
            r,w2,w5,med,c = run_test('o_df+hf', alpha, beta)
            pr(f"o_df a={alpha} + hf b={beta}", r, w2, w5, med, c)