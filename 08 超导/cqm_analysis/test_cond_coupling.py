"""用嘉当矩阵条件数(各向异性)作为耦合修正

物理动机:
  条件数 = max_eigenval / min_eigenval
  低条件数 → 矩阵近各向同性 → 无优先配对方向 → 弱超导
  高条件数 → 矩阵各向异性 → 有优先配对方向 → 强超导

  Be: cond=1.05 (两个s轨道几乎简并) → 弱配对 ✓
  Nb: cond=13.49 (d+s+p+s块, 高各向异性) → 强配对 ✓
  W: cond=13.90 (相同结构) → 无法区分 ✗

  但条件数能区分Be(弱)和过渡金属(强), 即使不能区分Nb和W

CQM第一性推导:
  嘉当矩阵 = 能动张量 = 哈密顿量
  条件数 = 能动张量各向异性 = 配对方向选择性
  log(cond) → 配对方向的相空间体积
  1/log(cond) → 配对方向的逆相空间 = 弱配对惩罚

  n_c -= alpha / log(cond_A)
  低cond → 大惩罚 → 低n_c → 低γ_n → 低K_0 → 低Tc
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework'); from atom_db import ATOM_DB
import csv, re, math, numpy as np
sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_analysis')
from cqm_no_classification_framework import *


def predict_tc_with_cond_correction(formula, alpha=0.0, mode='inv_log'):
    """加入条件数修正的Tc预测"""
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

    # 计算条件数修正
    eigvals = np.sort(np.linalg.eigvalsh(C_mol))
    cond_A = eigvals[-1] / eigvals[0] if eigvals[0] > 0 else 1000
    spectral_flatness = np.exp(np.mean(np.log(eigvals + 1e-30))) / np.mean(eigvals)

    correction_nc = 0.0
    if alpha != 0:
        if mode == 'inv_log':
            # 1/log(cond): 低cond大惩罚
            correction_nc = -alpha / max(math.log(cond_A), 0.01)
        elif mode == 'inv_cond':
            # 1/cond: 低cond大惩罚
            correction_nc = -alpha / cond_A
        elif mode == 'flatness':
            # flatness惩罚: 高flatness(低各向异性)大惩罚
            correction_nc = -alpha * spectral_flatness
        elif mode == 'inv_flatness':
            # 1/flatness: 低flatness(高各向异性)奖励
            correction_nc = alpha * (1.0 - spectral_flatness)
        elif mode == 'log_cond':
            # log(cond): 高cond奖励
            correction_nc = alpha * math.log(cond_A)
        elif mode == 'flatness_penalty':
            # 只惩罚高flatness(>0.9), 不影响其他
            excess = max(0, spectral_flatness - 0.85)
            correction_nc = -alpha * excess**2
        elif mode == 'cond_combined':
            # 组合: 条件数+谱平坦度
            correction_nc = -alpha / max(math.log(cond_A), 0.01) * (1 + spectral_flatness)

    # 修改gamma_n计算
    gamma_n, spec_info = gamma_n_from_spectrum(C_mol, atom_features, dd0_sq)

    # 重新计算gamma_n with correction
    n_c_original = spec_info['n_continuous']
    n_c_corrected = n_c_original + correction_nc
    if n_c_corrected < 1 or np.isnan(n_c_corrected):
        n_c_corrected = 1.0
    gamma_n_corrected = interpolate_gamma_n(n_c_corrected)

    K_0 = C_GAMMA * math.exp(AG_THEORY * gamma_n_corrected)
    G_safe = max(G, 1e-6)
    K_eff = K_0 * G_safe**(-3.0/4.0) * theta_d**(9.0/8.0)

    Tc_sq = 8 * dd0**2 * K_eff * theta_d / (9 * LN2)
    Tc = math.sqrt(max(0, Tc_sq))

    f_frac = atom_features['f_fraction']
    Tc *= math.exp(-C_F_SUPP * f_frac)
    d0_frac = atom_features['d0_fraction']
    Tc *= math.exp(-3.0 * d0_frac)

    info = {**spec_info, 'cond_A': cond_A, 'flatness': spectral_flatness,
            'n_c_original': n_c_original, 'n_c_corrected': n_c_corrected,
            'gamma_n_corrected': gamma_n_corrected}
    return Tc, info


# ============================================================
# 加载数据
# ============================================================

data = []
with open(r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_analysis\superconductors_deduplicated.csv', 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc > 0: data.append({'formula': row['材料(化学式)'], 'cat': row['类别'], 'tc_exp': tc})


def evaluate(alpha, mode):
    results = []
    for d in data:
        tc_pred, info = predict_tc_with_cond_correction(d['formula'], alpha=alpha, mode=mode)
        if tc_pred > 0:
            ratio = tc_pred / d['tc_exp']
            err = max(ratio, 1.0/ratio) - 1.0
            results.append({**d, 'tc_pred': tc_pred, 'error': err, 'info': info})
    errs = np.array([r['error'] for r in results])
    within_2x = np.sum(errs < 1) * 100 / len(errs)
    median_err = np.median(errs) * 100
    return within_2x, median_err, results


# ============================================================
# 1. 先看各材料的条件数和平坦度
# ============================================================

print("="*80)
print("各材料条件数和谱平坦度")
print("="*80)

# 元素超导体
print("\n元素超导体(常压):")
for d in data:
    if d['cat'] != '元素超导体(常压)':
        continue
    tc_pred, info = predict_tc_with_cond_correction(d['formula'], alpha=0)
    if tc_pred > 0:
        print(f"  {d['formula']:6s} Tc={d['tc_exp']:8.4f}K pred={tc_pred:8.2f}K  "
              f"cond={info['cond_A']:6.2f}  flat={info['flatness']:.4f}  "
              f"n_c={info['n_c_original']:.3f}  γ={info['gamma_n']:.1f}")

# ============================================================
# 2. 扫描不同模式和参数
# ============================================================

modes = ['inv_log', 'inv_cond', 'flatness', 'inv_flatness', 'log_cond',
         'flatness_penalty', 'cond_combined']

print(f"\n{'='*80}")
print("参数扫描")
print("="*80)

best_result = (0, 0, '', 0, 0)

for mode in modes:
    print(f"\n模式: {mode}")
    print(f"{'alpha':>8s} {'2倍内':>8s} {'中位':>8s} {'元素2倍内':>10s} {'元素中位':>10s}")

    alpha_range = np.arange(0.0, 2.0, 0.05) if mode != 'flatness_penalty' else np.arange(0.0, 200, 5)

    for alpha in alpha_range:
        w2x, med, results = evaluate(alpha, mode)

        elem = [r for r in results if r['cat'] == '元素超导体(常压)']
        elem_errs = np.array([r['error'] for r in elem])
        e2x = np.sum(elem_errs < 1) * 100 / len(elem_errs)
        emed = np.median(elem_errs) * 100

        marker = ""
        if w2x > 50.3:
            marker = " ★"
        if w2x > best_result[1]:
            best_result = (alpha, w2x, mode, med, emed)

        if alpha == 0 or w2x > 50 or marker:
            print(f"{alpha:8.3f} {w2x:7.1f}% {med:7.1f}% {e2x:9.1f}% {emed:9.1f}%{marker}")

print(f"\n最优: alpha={best_result[0]:.3f}, mode={best_result[2]}, 2倍内={best_result[1]:.1f}%, 中位={best_result[3]:.1f}%")

# ============================================================
# 3. 最优参数详细分析
# ============================================================

if best_result[1] > 50.3:
    print(f"\n{'='*80}")
    print(f"改进! alpha={best_result[0]:.3f}, mode={best_result[2]}")
    print("="*80)

    _, _, results = evaluate(best_result[0], best_result[2])

    print(f"\n按类别:")
    cat_errs = defaultdict(list)
    for r in results:
        cat_errs[r['cat']].append(r['error'])
    for cat in sorted(cat_errs.keys()):
        e = cat_errs[cat]
        print(f"  {cat:25s}: 中位{np.median(e)*100:.0f}% 2倍内{np.sum(np.array(e)<1)*100/len(e):.0f}% ({len(e)}个)")

    print(f"\n元素超导体(常压)详细:")
    elem = [r for r in results if r['cat'] == '元素超导体(常压)']
    elem.sort(key=lambda x: x['tc_exp'])
    for r in elem:
        info = r['info']
        print(f"  {r['formula']:6s} exp={r['tc_exp']:8.4f}K pred={r['tc_pred']:10.3f}K err={r['error']*100:.0f}% "
              f"cond={info['cond_A']:.1f} flat={info['flatness']:.3f} "
              f"n_c={info['n_c_corrected']:.3f}")

# ============================================================
# 4. 尝试组合: 条件数 + 其他修正
# ============================================================

print(f"\n{'='*80}")
print("组合修正: 条件数 + 谱平坦度 + 谱熵")
print("="*80)

def predict_tc_combined(formula, a_cond=0, a_flat=0, a_entropy=0):
    """组合修正"""
    atoms = parse_formula(formula)
    if not atoms:
        return 0, {}

    C_mol, _ = build_first_principles_Cmol(atoms, s_root=0.5)
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

    eigvals = np.sort(np.linalg.eigvalsh(C_mol))
    cond_A = eigvals[-1] / eigvals[0] if eigvals[0] > 0 else 1000
    flatness = np.exp(np.mean(np.log(eigvals + 1e-30))) / np.mean(eigvals)
    probs = eigvals / np.sum(eigvals)
    entropy = -np.sum(probs * np.log(probs + 1e-30))

    correction = 0
    if a_cond != 0:
        correction += -a_cond / max(math.log(cond_A), 0.01)
    if a_flat != 0:
        correction += -a_flat * flatness
    if a_entropy != 0:
        correction += a_entropy * (entropy - 1.5)  # 归一化

    gamma_n, spec_info = gamma_n_from_spectrum(C_mol, atom_features, dd0_sq)
    n_c = spec_info['n_continuous'] + correction
    gamma_n = interpolate_gamma_n(n_c)

    K_0 = C_GAMMA * math.exp(AG_THEORY * gamma_n)
    G_safe = max(G, 1e-6)
    K_eff = K_0 * G_safe**(-3.0/4.0) * theta_d**(9.0/8.0)
    Tc_sq = 8 * dd0**2 * K_eff * theta_d / (9 * LN2)
    Tc = math.sqrt(max(0, Tc_sq))

    f_frac = atom_features['f_fraction']
    Tc *= math.exp(-C_F_SUPP * f_frac)
    d0_frac = atom_features['d0_fraction']
    Tc *= math.exp(-3.0 * d0_frac)
    return Tc, spec_info


# 网格搜索
print("\n网格搜索: a_cond × a_flat")
best_combined = (0, 0, 0, 0)
for a_cond in np.arange(0.0, 0.5, 0.05):
    for a_flat in np.arange(0.0, 1.0, 0.1):
        results = []
        for d in data:
            tc_pred, _ = predict_tc_combined(d['formula'], a_cond=a_cond, a_flat=a_flat)
            if tc_pred > 0:
                ratio = tc_pred / d['tc_exp']
                err = max(ratio, 1.0/ratio) - 1.0
                results.append(err)
        w2x = np.sum(np.array(results) < 1) * 100 / len(results)
        if w2x > best_combined[3]:
            best_combined = (a_cond, a_flat, 0, w2x)
            if w2x > 50.3:
                print(f"  a_cond={a_cond:.3f} a_flat={a_flat:.3f}: 2倍内={w2x:.1f}% ★")

print(f"\n最优组合: a_cond={best_combined[0]:.3f} a_flat={best_combined[1]:.3f}: 2倍内={best_combined[3]:.1f}%")