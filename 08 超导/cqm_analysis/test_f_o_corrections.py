"""修正f电子抑制和o_fraction项

问题1: 稀土铁基超导体(ReFeAsO)被低估50x
  - f电子抑制exp(-C_F_SUPP * f_fraction)太强
  - f电子在稀土层, 超导在FeAs层 → f电子不应抑制

问题2: 氧化物超导体(SrTiO3, TiO, NbO)被高估100x
  - o_fraction项C_O*o_frac对非铜氧化物过度增强
  - 氧介导配对只在CuO2平面有效 → 需要d-p杂化

修正方案:
  A. f电子抑制: 用f电子数(非原子分数) + d电子共存时减弱
  B. o_fraction: 乘以dp_hybrid(氧配对需要d-p杂化)
  C. 组合A+B
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework'); from atom_db import ATOM_DB
import csv, math, numpy as np
sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_analysis')
from cqm_no_classification_framework import *

data = []
with open(r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_analysis\superconductors_deduplicated.csv', 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc > 0: data.append({'formula': row['材料(化学式)'], 'cat': row['类别'], 'tc_exp': tc})


def predict_tc_modified(formula, f_mode='original', o_mode='original',
                         f_alpha=1.0, o_alpha=1.0):
    """修正的Tc预测

    f_mode:
      'original': exp(-C_F_SUPP * f_fraction)
      'f_count': exp(-C_F_SUPP * f_electron_fraction) (用f电子数)
      'f_with_d': exp(-C_F_SUPP * f_fraction / (1 + alpha*d_fraction))
      'f_count_with_d': 组合

    o_mode:
      'original': C_O * o_fraction
      'o_with_dp': C_O * o_fraction * (dp_hybrid + 0.1)  (需要d-p杂化)
      'o_with_dp_strong': C_O * o_fraction * dp_hybrid
    """
    atoms = parse_formula(formula)
    if not atoms:
        return 0, {}

    C_mol, block_info = build_first_principles_Cmol(atoms, s_root=0.5)
    atom_features = compute_atom_features(atoms)

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

    # 修改gamma_n计算中的o_fraction项
    dp_hybrid = atom_features.get('dp_hybrid', 0)
    o_frac = atom_features.get('o_fraction', 0)

    # 计算修改的o_fraction贡献
    if o_mode == 'original':
        o_contribution = C_O * o_frac
    elif o_mode == 'o_with_dp':
        o_contribution = C_O * o_frac * (dp_hybrid + 0.1)
    elif o_mode == 'o_with_dp_strong':
        o_contribution = C_O * o_frac * max(dp_hybrid, 0.01)
    else:
        o_contribution = C_O * o_frac

    # 临时修改gamma_n_from_spectrum中的o_fraction
    # 通过直接计算
    eigvals = np.sort(np.linalg.eigvalsh(C_mol))
    n = len(eigvals)
    if n < 2:
        return 0, {}

    sg = eigvals[1] - eigvals[0]
    ev_mean = np.mean(eigvals)
    ev_std = np.std(eigvals)
    ev_norm = eigvals / ev_mean if ev_mean > 0 else eigvals
    anisotropy = np.std(ev_norm)
    skewness = np.mean(((eigvals - ev_mean) / ev_std) ** 3) if ev_std > 0 else 0
    kurtosis = np.mean(((eigvals - ev_mean) / ev_std) ** 4) - 3 if ev_std > 0 else 0
    cond_A = eigvals[-1] / eigvals[0] if eigvals[0] > 0 else 1000.0

    COEF_EQ8 = 3 * BETA**2 / 16
    eq8_term = 1.5 * COEF_EQ8 * dd0_sq

    sg_safe = max(sg, 0.05)
    n_continuous = (4.00
                    + 0.50 * math.log(1.0 / sg_safe)
                    + C_ANISO * anisotropy
                    + T0_BASE * skewness
                    + T0_BASE * kurtosis
                    + eq8_term
                    + 0.05 * dp_hybrid
                    + o_contribution
                    - 0.75 / cond_A)

    gamma_n = interpolate_gamma_n(n_continuous)

    K_0 = C_GAMMA * math.exp(AG_THEORY * gamma_n)
    G_safe = max(G, 1e-6)
    K_eff = K_0 * G_safe**(-3.0/4.0) * theta_d**(9.0/8.0)

    Tc_sq = 8 * dd0**2 * K_eff * theta_d / (9 * LN2)
    Tc = math.sqrt(max(0, Tc_sq))

    # 修改f电子抑制
    f_frac = atom_features['f_fraction']

    # 计算d电子分数
    d_count = 0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        vo = valence_orbitals(z)
        for l_qn, occ, cap in vo:
            if l_qn == 2:
                d_count += occ * atoms[el]
    d_fraction = d_count / (n_atoms * 10)  # 归一化(最多10个d电子)

    # 计算f电子数分数
    f_e_count = 0
    total_e = 0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        config = madelung_config(z)
        for (n_qn, l_qn), occ in config.items():
            total_e += occ * atoms[el]
            if l_qn == 3 and 0 < occ < 14:
                f_e_count += occ * atoms[el]
    f_electron_fraction = f_e_count / max(total_e, 1)

    if f_mode == 'original':
        f_suppression = math.exp(-C_F_SUPP * f_frac)
    elif f_mode == 'f_count':
        f_suppression = math.exp(-C_F_SUPP * f_electron_fraction * f_alpha)
    elif f_mode == 'f_with_d':
        f_suppression = math.exp(-C_F_SUPP * f_frac / (1 + f_alpha * d_fraction))
    elif f_mode == 'f_count_with_d':
        f_suppression = math.exp(-C_F_SUPP * f_electron_fraction / (1 + f_alpha * d_fraction))
    elif f_mode == 'f_if_no_d':
        # 有d电子时减弱f抑制
        if d_count > 0:
            f_suppression = math.exp(-C_F_SUPP * f_electron_fraction * 0.3)
        else:
            f_suppression = math.exp(-C_F_SUPP * f_frac)
    else:
        f_suppression = math.exp(-C_F_SUPP * f_frac)

    Tc *= f_suppression

    d0_frac = atom_features['d0_fraction']
    Tc *= math.exp(-3.0 * d0_frac)

    return Tc, {'gamma_n': gamma_n, 'n_continuous': n_continuous, 'cond_A': cond_A,
                'f_suppression': f_suppression, 'o_contribution': o_contribution}


def evaluate(f_mode='original', o_mode='original', f_alpha=1.0, o_alpha=1.0):
    results = []
    for d in data:
        tc_pred, info = predict_tc_modified(d['formula'], f_mode=f_mode, o_mode=o_mode,
                                             f_alpha=f_alpha, o_alpha=o_alpha)
        if tc_pred > 0:
            ratio = tc_pred / d['tc_exp']
            err = max(ratio, 1.0/ratio) - 1.0
            results.append({**d, 'tc_pred': tc_pred, 'error': err, 'ratio': ratio, 'info': info})
    errs = np.array([r['error'] for r in results])
    within_2x = np.sum(errs < 1) * 100 / len(errs)
    median_err = np.median(errs) * 100
    return within_2x, median_err, results


# ============================================================
# 1. 基线
# ============================================================

print("="*80)
print("基线: 50.8%")
print("="*80)

w2x, med, results = evaluate()
print(f"2倍内={w2x:.1f}% 中位={med:.1f}%")

# ============================================================
# 2. 测试o_fraction修正
# ============================================================

print(f"\n{'='*80}")
print("测试o_fraction修正")
print("="*80)

for o_mode in ['original', 'o_with_dp', 'o_with_dp_strong']:
    w2x, med, results = evaluate(o_mode=o_mode)
    print(f"\n{o_mode}: 2倍内={w2x:.1f}% 中位={med:.1f}%")

    # 关键材料
    for formula in ['SrTiO3', 'TiO', 'NbO', 'WO3', 'Bi2Sr2CaCu2O8+δ', 'Ba1-xKxBiO3']:
        r = next((r for r in results if r['formula'] == formula), None)
        if r:
            print(f"  {formula:20s} exp={r['tc_exp']:8.2f}K pred={r['tc_pred']:10.2f}K err={r['error']*100:.0f}% o_contrib={r['info']['o_contribution']:.2f}")

# ============================================================
# 3. 测试f电子抑制修正
# ============================================================

print(f"\n{'='*80}")
print("测试f电子抑制修正")
print("="*80)

for f_mode in ['original', 'f_count', 'f_with_d', 'f_count_with_d', 'f_if_no_d']:
    # 扫描f_alpha
    best_alpha = 1.0
    best_w2x = 0
    for alpha in np.arange(0.5, 20, 0.5):
        w2x, med, _ = evaluate(f_mode=f_mode, f_alpha=alpha)
        if w2x > best_w2x:
            best_w2x = w2x
            best_alpha = alpha

    w2x, med, results = evaluate(f_mode=f_mode, f_alpha=best_alpha)
    print(f"\n{f_mode} (alpha={best_alpha:.1f}): 2倍内={w2x:.1f}% 中位={med:.1f}%")

    # 铁基超导体
    fe = [r for r in results if r['cat'] == '铁基超导体']
    fe_errs = np.array([r['error'] for r in fe])
    print(f"  铁基: 中位{np.median(fe_errs)*100:.0f}% 2倍内{np.sum(fe_errs<1)*100/len(fe_errs):.0f}%")

    # 关键材料
    for formula in ['NdFeAsO1-xFx', 'GdFeAsO1-xFx', 'CeFeAsO1-xFx', 'CeCu2Si2', 'UBe13']:
        r = next((r for r in results if r['formula'] == formula), None)
        if r:
            print(f"  {formula:20s} exp={r['tc_exp']:8.2f}K pred={r['tc_pred']:10.2f}K err={r['error']*100:.0f}% f_supp={r['info']['f_suppression']:.4f}")

# ============================================================
# 4. 组合最优o_mode和f_mode
# ============================================================

print(f"\n{'='*80}")
print("组合最优修正")
print("="*80)

# 测试组合
for o_mode in ['o_with_dp', 'o_with_dp_strong']:
    for f_mode in ['f_count_with_d', 'f_if_no_d']:
        best_alpha = 1.0
        best_w2x = 0
        for alpha in np.arange(0.5, 20, 0.5):
            w2x, med, _ = evaluate(f_mode=f_mode, o_mode=o_mode, f_alpha=alpha)
            if w2x > best_w2x:
                best_w2x = w2x
                best_alpha = alpha

        w2x, med, results = evaluate(f_mode=f_mode, o_mode=o_mode, f_alpha=best_alpha)
        marker = " ★" if w2x > 50.8 else ""
        print(f"\n{o_mode} + {f_mode} (alpha={best_alpha:.1f}): 2倍内={w2x:.1f}% 中位={med:.1f}%{marker}")

        if w2x > 50.8:
            # 按类别
            cat_errs = defaultdict(list)
            for r in results:
                cat_errs[r['cat']].append(r['error'])
            for cat in sorted(cat_errs.keys()):
                e = cat_errs[cat]
                print(f"  {cat:25s}: 中位{np.median(e)*100:.0f}% 2倍内{np.sum(np.array(e)<1)*100/len(e):.0f}% ({len(e)}个)")