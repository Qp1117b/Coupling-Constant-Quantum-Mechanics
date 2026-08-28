"""测试无d轨道抑制v2: no_d × exp(-k×d_count) 调制

问题: no_d对铜氧化物也高(O无d), 导致铜氧化物被抑制
解决: no_d × exp(-k×d_partial_count)
  - 有机/石墨(d_count=0): no_d×1 → 强抑制
  - 铜氧化物(d_count=1): no_d×exp(-k) → 弱抑制
  - A15(d_count>0, no_d=0): 0 → 无抑制
"""

import sys, os, math, csv
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cqm_no_classification_framework import *

def compute_features(atoms):
    els = list(atoms.keys())
    n_atoms = sum(atoms.values())
    no_d_count = 0
    d_partial_count = 0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        vo = valence_orbitals(z)
        has_d = False
        for l, occ, cap in vo:
            if l == 2:
                has_d = True
                if 0 < occ < cap:
                    d_partial_count += atoms[el]
        if not has_d:
            no_d_count += atoms[el]
    return no_d_count / n_atoms, d_partial_count

def predict_tc_v2(formula, alpha=0.0, k=3.0):
    atoms = parse_formula(formula)
    if not atoms: return 0, {}
    C_mol, block_info = build_first_principles_Cmol(atoms, s_root=0.5)
    if C_mol is None: return 0, {}
    atom_features = compute_atom_features(atoms)
    no_d, d_p_count = compute_features(atoms)

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
    d0_frac = atom_features['d0_fraction']
    Tc *= math.exp(-3.0 * d0_frac)

    # π电子配对抑制: no_d × exp(-k×d_count) → 无d时强抑制, 有d时弱抑制
    if alpha > 0:
        pi_factor = no_d * math.exp(-k * d_p_count)
        Tc *= math.exp(-alpha * pi_factor)

    return Tc, {}

def run_test(alpha=0.0, k=3.0):
    data_file = os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv')
    results = []
    with open(data_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            formula = row['材料(化学式)']
            try: tc = float(row['临界温度 Tc (K)'])
            except: continue
            if tc <= 0: continue
            category = row.get('类别', '')
            Tc_pred, _ = predict_tc_v2(formula, alpha, k)
            if Tc_pred <= 0: continue
            ratio = Tc_pred / tc
            err = max(ratio, 1.0/ratio) - 1.0
            results.append((formula, tc, Tc_pred, ratio, err, category))
    w2 = sum(1 for r in results if r[4] < 1.0)
    w5 = sum(1 for r in results if r[4] < 4.0)
    med = np.median([r[4] for r in results]) * 100
    cats = {}
    for r in results:
        c = r[5]
        if c not in cats: cats[c] = []
        cats[c].append(r)
    return results, w2, w5, med, cats

def pr(label, results, w2, w5, med, cats):
    n = len(results)
    print(f"\n{label}: {w2}/{n}={w2/n*100:.1f}% 2x  {w5}/{n}={w5/n*100:.1f}% 5x  med={med:.1f}%")
    for c in ['有机超导体', '石墨插层超导体', '铜氧化物高温超导体', '铁基超导体',
              'A15结构金属间化合物', '其他特殊超导体', '富勒烯超导体']:
        if c in cats:
            r = cats[c]
            w = sum(1 for x in r if x[4] < 1.0)
            print(f"    {c}: med={np.median([x[4] for x in r])*100:.0f}% 2x={w}/{len(r)}")

if __name__ == '__main__':
    print("="*60)
    print("π电子配对抑制v2: no_d × exp(-k×d_count)")
    print("="*60)

    r,w2,w5,med,c = run_test(0.0)
    pr("基线(52.8%)", r, w2, w5, med, c)

    for k in [2.0, 3.0, 5.0]:
        print(f"\n--- k={k} ---")
        for alpha in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0]:
            r,w2,w5,med,c = run_test(alpha, k)
            pr(f"alpha={alpha} k={k}", r, w2, w5, med, c)