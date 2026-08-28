"""测试氧化物o_fraction修正和重费米子修正

氧化物问题: SrTiO3(Ti d⁰)被o_fraction过度增强, 但d⁰无d电子配对
重费米子问题: CeCu2Si2(Cu d¹⁰满)f抑制太弱, 但f+满d=重费米子=强抑制
"""

import sys, os, math, csv
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cqm_no_classification_framework import *

def compute_d_filling_features(atoms):
    """计算d轨道填充特征"""
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
        'd_partial_fraction': d_partial_count / n_atoms,
        'd_empty_fraction': d_empty_count / n_atoms,
        'd_full_fraction': d_full_count / n_atoms,
        'd_filling_avg': d_filling_sum / n_atoms,
    }

def predict_tc_modified(formula, mode='baseline', alpha=1.0):
    """修改版Tc预测"""
    atoms = parse_formula(formula)
    if not atoms:
        return 0, {}

    C_mol, block_info = build_first_principles_Cmol(atoms, s_root=0.5)
    if C_mol is None:
        return 0, {}

    atom_features = compute_atom_features(atoms)
    d_features = compute_d_filling_features(atoms)

    els = list(atoms.keys())
    n_atoms = sum(atoms.values())
    total_m = sum(atoms[el] * ATOM_DB[el][0] for el in els)
    avg_r = sum(atoms[el] * ATOM_DB[el][2] for el in els) / n_atoms
    l = max(2 * avg_r * 1e-10, 1e-20)
    theta_d = sum(atoms[el] * ATOM_DB[el][1] for el in els) / n_atoms
    if theta_d <= 0:
        return 0, {}

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

    # 修改gamma_n_from_spectrum以支持o_fraction修正
    # 需要直接修改n_continuous中的o_frac项
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
    f_frac = atom_features.get('f_fraction', 0)
    d0_frac = atom_features.get('d0_fraction', 0)

    d_partial = d_features['d_partial_fraction']
    d_empty = d_features['d_empty_fraction']
    d_full = d_features['d_full_fraction']
    d_filling = d_features['d_filling_avg']

    COEF_EQ8 = 3 * BETA**2 / 16
    eq8_term = 1.5 * COEF_EQ8 * dd0_sq
    sg_safe = max(sg, 0.05)

    # o_fraction修正: 修改o_frac在n_continuous中的值
    o_frac_effective = o_frac  # 默认不修正

    if mode in ('o_no_d0', 'o_no_d0_plus_hf'):
        # d⁰不增强: o_frac * (1 - d_empty * alpha)
        o_frac_effective = o_frac * (1 - d_empty * alpha)
    elif mode in ('o_d_filling', 'o_d_filling_plus_hf'):
        # d填充因子调制: o_frac * d_filling * alpha
        o_frac_effective = o_frac * d_filling * alpha
    elif mode == 'o_d_partial':
        # 只有部分填充d才增强: o_frac * d_partial * alpha
        o_frac_effective = o_frac * d_partial * alpha
    elif mode == 'o_no_d0_strong':
        # d⁰完全消除: 如果有d⁰, o_frac *= (1 - d_empty/d_total_metals)
        o_frac_effective = o_frac * max(0, 1 - d_empty * alpha)

    n_continuous = (4.00
                    + 0.50 * math.log(1.0 / sg_safe)
                    + C_ANISO * anisotropy
                    + T0_BASE * skewness
                    + T0_BASE * kurtosis
                    + eq8_term
                    + 0.05 * dp_hybrid
                    + C_O * o_frac_effective
                    - 0.75 / cond_A)

    gamma_n = interpolate_gamma_n(n_continuous)

    K_0 = C_GAMMA * math.exp(AG_THEORY * gamma_n)
    G_safe = max(G, 1e-6)
    K_eff = K_0 * G_safe**(-3/4) * theta_d**(9/8)

    Tc_sq = 8 * dd0**2 * K_eff * theta_d / (9 * LN2)
    Tc = math.sqrt(max(0, Tc_sq))

    # f电子抑制
    f_coeff = 0.5  # 默认s_root
    if mode in ('hf_f_no_d',):
        # f + 无部分d → 强抑制
        f_coeff = 0.5 + (alpha - 0.5) * (1 - d_partial)
    elif mode in ('hf_f_d_full', 'o_no_d0_plus_hf', 'o_d_filling_plus_hf'):
        # f + d满 → 强抑制
        f_coeff = 0.5 + (alpha - 0.5) * d_full

    Tc *= math.exp(-C_F_SUPP * f_frac * f_coeff)
    Tc *= math.exp(-3.0 * d0_frac)

    return Tc, {'gamma_n': gamma_n, 'n_continuous': n_continuous}

def run_test(mode, alpha=1.0):
    data_file = os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv')
    results = []
    with open(data_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            formula = row['材料(化学式)']
            try:
                T_exp = float(row['临界温度 Tc (K)'].replace('~','').replace('>','').replace('<',''))
            except:
                continue
            category = row.get('类别', '')
            Tc_pred, info = predict_tc_modified(formula, mode, alpha)
            if Tc_pred <= 0:
                continue
            err = abs(Tc_pred - T_exp) / max(T_exp, 0.001)
            results.append((formula, T_exp, Tc_pred, err, category, info.get('gamma_n', 0)))

    within_2x = sum(1 for r in results if r[3] < 1.0)
    within_5x = sum(1 for r in results if r[3] < 4.0)
    median_err = np.median([r[3] for r in results]) * 100
    categories = {}
    for r in results:
        cat = r[4]
        if cat not in categories: categories[cat] = []
        categories[cat].append(r[3])
    return results, within_2x, within_5x, median_err, categories

def print_results(label, results, w2, w5, med, cats):
    n = len(results)
    print(f"\n{label}:")
    print(f"  2倍内: {w2}/{n} = {w2/n*100:.1f}%  5倍内: {w5}/{n} = {w5/n*100:.1f}%  中位: {med:.1f}%")
    for cat in ['其他特殊超导体', '其他金属间化合物', '铁基超导体', '铜氧化物高温超导体']:
        if cat in cats:
            errs = cats[cat]
            w2c = sum(1 for e in errs if e < 1.0)
            print(f"    {cat}: 中位{np.median(errs)*100:.0f}% 2倍内{w2c}/{len(errs)}={w2c/len(errs)*100:.0f}%")
    worst = sorted(results, key=lambda x: x[3], reverse=True)[:3]
    for r in worst:
        print(f"    最差: {r[0]:20s} exp={r[1]:8.1f}K pred={r[2]:10.1f}K err={r[3]*100:.0f}%")

if __name__ == '__main__':
    print("=" * 70)
    print("氧化物o_fraction修正 + 重费米子修正测试")
    print("=" * 70)

    results, w2, w5, med, cats = run_test('baseline')
    print_results("基线(当前框架 52.8%)", results, w2, w5, med, cats)

    print("\n--- 氧化物修正 ---")
    for mode in ['o_no_d0', 'o_d_filling', 'o_d_partial', 'o_no_d0_strong']:
        for alpha in [0.5, 1.0, 1.5, 2.0]:
            results, w2, w5, med, cats = run_test(mode, alpha)
            print_results(f"{mode} alpha={alpha}", results, w2, w5, med, cats)

    print("\n--- 重费米子修正 ---")
    for mode in ['hf_f_no_d', 'hf_f_d_full']:
        for alpha in [1.0, 2.0, 3.0, 5.0]:
            results, w2, w5, med, cats = run_test(mode, alpha)
            print_results(f"{mode} alpha={alpha}", results, w2, w5, med, cats)

    print("\n--- 组合修正 ---")
    for mode in ['o_no_d0_plus_hf', 'o_d_filling_plus_hf']:
        for alpha in [1.0, 2.0, 3.0]:
            results, w2, w5, med, cats = run_test(mode, alpha)
            print_results(f"{mode} alpha={alpha}", results, w2, w5, med, cats)
