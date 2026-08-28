"""测试重费米子修正v3: 用d_partial_count(原子数)调制

问题: d_partial_fraction对SmFeAsO=0.25(Fe是4原子中1个), (1-0.25)=0.75仍强抑制
解决: 用exp(-k*d_partial_count)替代(1-d_partial_fraction)
  - CeCu2Si2: d_count=0 → exp(0)=1 → 完全抑制
  - SmFeAsO: d_count=1 → exp(-k) → 需要很小
"""

import sys, os, math, csv
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cqm_no_classification_framework import *

def compute_features(atoms):
    els = list(atoms.keys())
    n_atoms = sum(atoms.values())
    d_partial_count = 0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        vo = valence_orbitals(z)
        for l, occ, cap in vo:
            if l == 2 and 0 < occ < cap:
                d_partial_count += atoms[el]
                break
    f_atom_count = 0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        config = madelung_config(z)
        for (n_qn, l_qn), occ in config.items():
            if l_qn == 3 and 0 < occ < 14:
                f_atom_count += atoms[el]
                break
    return d_partial_count, f_atom_count / n_atoms

def predict_tc_v3(formula, mode='baseline', k=2.0, beta_hf=1.5):
    atoms = parse_formula(formula)
    if not atoms: return 0, {}
    C_mol, block_info = build_first_principles_Cmol(atoms, s_root=0.5)
    if C_mol is None: return 0, {}
    atom_features = compute_atom_features(atoms)
    d_p_count, f_atom = compute_features(atoms)

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

    gamma_n, spec_info = gamma_n_from_spectrum(C_mol, atom_features, dd0_sq)
    K_0 = C_GAMMA * math.exp(AG_THEORY * gamma_n)
    G_safe = max(G, 1e-6)
    K_eff = K_0 * G_safe**(-3/4) * theta_d**(9/8)
    Tc_sq = 8 * dd0**2 * K_eff * theta_d / (9 * LN2)
    Tc = math.sqrt(max(0, Tc_sq))

    f_frac = atom_features['f_fraction']
    Tc *= math.exp(-C_F_SUPP * f_frac * 0.5)

    if mode == 'hf_exp':
        # exp(-k * d_partial_count) 调制
        hf_factor = math.exp(-k * d_p_count)
        Tc *= math.exp(-C_F_SUPP * f_atom * hf_factor * beta_hf)

    d0_frac = atom_features['d0_fraction']
    Tc *= math.exp(-3.0 * d0_frac)
    return Tc, {}

def run_test(mode='baseline', k=2.0, beta_hf=1.5):
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
            Tc_pred, _ = predict_tc_v3(formula, mode, k, beta_hf)
            if Tc_pred <= 0: continue
            err = abs(Tc_pred - T_exp) / max(T_exp, 0.001)
            results.append((formula, T_exp, Tc_pred, err, category))
    w2 = sum(1 for r in results if r[3] < 1.0)
    med = np.median([r[3] for r in results]) * 100
    cats = {}
    for r in results:
        c = r[4]
        if c not in cats: cats[c] = []
        cats[c].append(r[3])
    return results, w2, med, cats

def pr(label, results, w2, med, cats):
    n = len(results)
    print(f"\n{label}: {w2}/{n}={w2/n*100:.1f}% 2x  med={med:.1f}%")
    for c in ['其他金属间化合物', '铁基超导体', '铜氧化物高温超导体']:
        if c in cats:
            e = cats[c]
            w = sum(1 for x in e if x < 1.0)
            print(f"    {c}: med={np.median(e)*100:.0f}% 2x={w}/{len(e)}")
    worst = sorted(results, key=lambda x: x[3], reverse=True)[:3]
    for r in worst:
        print(f"    worst: {r[0]:20s} exp={r[1]:8.1f} pred={r[2]:10.1f} err={r[3]*100:.0f}%")

if __name__ == '__main__':
    print("="*60)
    print("重费米子修正v3: exp(-k*d_count)调制")
    print("="*60)

    r,w2,med,c = run_test('baseline')
    pr("基线", r, w2, med, c)

    for k in [1.0, 2.0, 3.0, 5.0, 8.0, 10.0]:
        for beta_hf in [1.0, 1.5, 2.0, 3.0]:
            r,w2,med,c = run_test('hf_exp', k, beta_hf)
            pr(f"hf_exp k={k} beta={beta_hf}", r, w2, med, c)