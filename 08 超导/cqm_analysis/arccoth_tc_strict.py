"""arccoth闭式Tc计算：从§11.6/§11.10严格推导

核心思路：
  §11.6本征值: λ_n(T) = γ_n + [coth(θ_D/2T)-1](ln n)² - β²(n²-1)Δδ_v²/(4n²(1-βδ_v))
  本征值交叉: λ_1(T_c) = λ_n(T_c)
  => Tc闭式（不需要K_0, G, 0.369!）

两条路线：
  A. 简化闭式（§11.10，省略温度修正）:
     Tc = θ_D / (2·arccoth(x_n))
     x_n = β²(n²-1)Δδ_0² / [4n²(1-βδ_v)(γ_n - γ_1)]

  B. 完整闭式（含温度修正，解二次方程）:
     (ln n)²·y² - [(ln n)² + γ_n - γ_1]·y + β²(n²-1)Δδ_0²/[4n²(1-βδ_v)] = 0
     Tc = θ_D / (2·arccoth(y))

对比当前自由能公式:
  Tc = sqrt(8·Δδ_0²·K_0·G^p·θ_D^q·θ_D/(9·ln2))
  K_0 = 7.77e11·exp(0.369·γ_n)  ← 经验拟合!
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import math, csv, numpy as np

# 从框架导入核心函数（避免执行主代码）
import importlib.util
spec = importlib.util.spec_from_file_location(
    "framework", os.path.join(os.path.dirname(__file__), "cqm_no_classification_framework.py"))
# 不能直接import（会执行主代码），手动复制需要的函数

sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework')
from atom_db import ATOM_DB

# ============================================================
# 物理常数
# ============================================================
HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
C2 = 2.0/3.0; LN2 = math.log(2)
BETA = 8 * math.pi + 1  # ≈ 26.13, 从A4群论导出

RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832,
                 52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
                 67.079811, 69.526405, 72.067158, 75.704690, 77.144840]
GAMMA_1 = RIEMANN_ZEROS[0]  # 14.13

ATOMIC_NUMBERS = {}
for _el, _z in [('H',1),('He',2),('Li',3),('Be',4),('B',5),('C',6),('N',7),('O',8),('F',9),('Ne',10),
    ('Na',11),('Mg',12),('Al',13),('Si',14),('P',15),('S',16),('Cl',17),('Ar',18),('K',19),('Ca',20),
    ('Sc',21),('Ti',22),('V',23),('Cr',24),('Mn',25),('Fe',26),('Co',27),('Ni',28),('Cu',29),('Zn',30),
    ('Ga',31),('Ge',32),('As',33),('Se',34),('Br',35),('Kr',36),('Rb',37),('Sr',38),('Y',39),('Zr',40),
    ('Nb',41),('Mo',42),('Tc',43),('Ru',44),('Rh',45),('Pd',46),('Ag',47),('Cd',48),('In',49),('Sn',50),
    ('Sb',51),('Te',52),('I',53),('Xe',54),('Cs',55),('Ba',56),('La',57),('Ce',58),('Pr',59),('Nd',60),
    ('Gd',64),('Tb',65),('Dy',66),('Ho',67),('Er',68),('Tm',69),('Yb',70),('Lu',71),('Hf',72),('Ta',73),
    ('W',74),('Re',75),('Os',76),('Ir',77),('Pt',78),('Au',79),('Hg',80),('Tl',81),('Pb',82),('Bi',83),
    ('Th',90),('Pa',91),('U',92),('Np',93),('Pu',94),('Am',95),('Cm',96)]:
    ATOMIC_NUMBERS[_el] = _z

# ============================================================
# 从框架复制核心函数
# ============================================================
A1 = np.array([[2.0]])
A3 = np.array([[2,-1,0],[-1,2,-1],[0,-1,2]])
A4 = np.array([[2,-1,0,0],[-1,2,-1,0],[0,-1,2,-1],[0,0,-1,2]])

def madelung_config(z):
    order = []
    for n in range(1, 8):
        for l in range(n):
            order.append((n+l, n, l))
    order.sort(key=lambda x: (x[0], x[1]))
    config = {}
    remaining = z
    for _, n, l in order:
        cap = 2*(2*l+1)
        fill = min(remaining, cap)
        if fill > 0:
            config[(n, l)] = fill
            remaining -= fill
        if remaining == 0:
            break
    exceptions = {
        57: {(4,3): 0, (5,2): 1}, 58: {(4,3): 1, (5,2): 1}, 64: {(4,3): 7, (5,2): 1},
        89: {(5,3): 0, (6,2): 1}, 90: {(5,3): 0, (6,2): 2}, 96: {(5,3): 7, (6,2): 1},
    }
    if z in exceptions:
        for (n, l), occ in exceptions[z].items():
            if occ == 0: config.pop((n, l), None)
            else: config[(n, l)] = occ
    return config

def valence_orbitals(z):
    config = madelung_config(z)
    if not config: return []
    max_n = max(n for n, l in config)
    valence = []
    for (n, l), occ in sorted(config.items(), reverse=True):
        if n >= max_n - 1:
            cap = 2*(2*l+1)
            valence.append((l, occ, cap))
    return valence

def build_first_principles_Cmol(atoms):
    els = list(atoms.keys())
    blocks = []
    block_info = []
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        vo = valence_orbitals(z)
        for l, occ, cap in vo:
            if l == 0:
                blocks.append(A1.copy()); block_info.append((el, 's', 1))
            elif l == 1:
                blocks.append(A3.copy()); block_info.append((el, 'p', 3))
            elif l == 2:
                blocks.append(A4.copy()); block_info.append((el, 'd', 4))
    if not blocks:
        return np.array([[2.0]]), [('X', 's', 1)]
    size = sum(b.shape[0] for b in blocks)
    C = np.zeros((size, size))
    idx = 0
    for b in blocks:
        s = b.shape[0]
        C[idx:idx+s, idx:idx+s] = b
        idx += s
    # 跨原子耦合
    idx_i, idx_j = 0, 0
    for i, bi in enumerate(block_info):
        si = bi[2]
        idx_j = idx_i + si
        for j, bj in enumerate(block_info[i+1:], start=i+1):
            sj = bj[2]
            el_i, el_j = bi[0], bj[0]
            ri = ATOM_DB.get(el_i, (1, 0, 1.5, 8))[2]
            rj = ATOM_DB.get(el_j, (1, 0, 1.5, 8))[2]
            d = ri + rj
            t0 = 0.1 * math.exp(-d / 3.0)
            li, lj = bi[1], bj[1]
            if (li == 'd' and lj == 'p') or (li == 'p' and lj == 'd'):
                t0 *= 1.5
            for a in range(si):
                for b in range(sj):
                    C[idx_i + a, idx_j + b] = t0
                    C[idx_j + b, idx_i + a] = t0
            idx_j += sj
        idx_i += si
    return C, block_info

def compute_atom_features(atoms):
    els = list(atoms.keys())
    n_atoms = sum(atoms.values())
    inv_mass_avg = sum(atoms[el] / ATOM_DB[el][0] for el in els) / n_atoms
    dp_hybrid = 0
    d_empty_count = 0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        vo = valence_orbitals(z)
        has_d, has_p = False, False
        for l, occ, cap in vo:
            if l == 2: has_d = True
            if l == 1: has_p = True
            if l == 2 and occ == 0: d_empty_count += atoms[el]
        if has_d and has_p: dp_hybrid += atoms[el]
    dp_hybrid /= n_atoms
    o_fraction = atoms.get('O', 0) / n_atoms
    f_count = 0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        config = madelung_config(z)
        for (n_qn, l_qn), occ in config.items():
            if l_qn == 3 and 0 < occ < 14:
                f_count += atoms[el]; break
    f_fraction = f_count / n_atoms
    d0_fraction = d_empty_count / n_atoms
    return {'inv_mass_avg': inv_mass_avg, 'dp_hybrid': dp_hybrid,
            'o_fraction': o_fraction, 'f_fraction': f_fraction, 'd0_fraction': d0_fraction}

def interpolate_gamma_n(n):
    n_int = int(n); frac = n - n_int
    if n_int < 1: return RIEMANN_ZEROS[0]
    if n_int >= len(RIEMANN_ZEROS):
        return 2 * math.pi * n / math.log(n / (2 * math.pi)) if n > 6 else RIEMANN_ZEROS[-1]
    g_low = RIEMANN_ZEROS[n_int - 1]
    g_high = RIEMANN_ZEROS[n_int] if n_int < len(RIEMANN_ZEROS) else RIEMANN_ZEROS[-1]
    return g_low + frac * (g_high - g_low)

def gamma_n_from_spectrum(C_mol, atom_features=None):
    eigvals = np.sort(np.linalg.eigvalsh(C_mol))
    n = len(eigvals)
    if n < 2: return RIEMANN_ZEROS[0], {'gamma_n': RIEMANN_ZEROS[0], 'n_continuous': 1.0}
    sg = eigvals[1] - eigvals[0]
    ev_mean = np.mean(eigvals); ev_std = np.std(eigvals)
    ev_norm = eigvals / ev_mean if ev_mean > 0 else eigvals
    anisotropy = np.std(ev_norm)
    inv_mass = atom_features.get('inv_mass_avg', 0) if atom_features else 0
    dp_hybrid = atom_features.get('dp_hybrid', 0) if atom_features else 0
    o_frac = atom_features.get('o_fraction', 0) if atom_features else 0
    sg_safe = max(sg, 0.05)
    n_continuous = (4.00 + 0.50 * math.log(1.0 / sg_safe) + 0.35 * anisotropy
                    + 13.00 * inv_mass + 0.05 * dp_hybrid + 5.50 * o_frac)
    gamma_n = interpolate_gamma_n(n_continuous)
    return gamma_n, {'spectral_gap': sg, 'anisotropy': anisotropy, 'n_continuous': n_continuous, 'gamma_n': gamma_n}

def parse_formula(f):
    import re
    pairs = re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f)
    atoms = {}
    for el, cnt in pairs:
        if el in ATOM_DB:
            atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    return atoms

# ============================================================
# arccoth闭式Tc计算
# ============================================================

def compute_delta_0_and_theta(atoms):
    """计算Δδ_0和θ_D（与主框架一致）"""
    els = list(atoms.keys())
    n_atoms = sum(atoms.values())
    avg_r = sum(atoms[el] * ATOM_DB[el][2] for el in els) / n_atoms
    l = 2 * avg_r * 1e-10
    theta_d = sum(atoms[el] * ATOM_DB[el][1] for el in els) / n_atoms
    if theta_d <= 0: return 0, 0, 0, 0

    n_eff = max(2, n_atoms)
    f_corr = 1.0 - 0.3 * (1.0 - 1.0/n_eff)

    edge_sum = 0
    for i in range(len(els)):
        for j in range(i+1, len(els)):
            mi = atoms[els[i]] * ATOM_DB[els[i]][0] * AMU
            mj = atoms[els[j]] * ATOM_DB[els[j]][0] * AMU
            edge_sum += (1.0/mi + 1.0/mj)
    if not edge_sum:
        total_m = sum(atoms[el] * ATOM_DB[el][0] for el in els)
        mi = total_m * AMU / n_atoms
        edge_sum = max(1, n_eff*(n_eff-1)/2) * 2.0 / mi

    G = (1.0/l) * math.sqrt((1.0-f_corr) * edge_sum)
    omega_d = theta_d * KB / HBAR
    dd0_sq = (C2/l**2) * (3*HBAR/(4*omega_d)) * (1-f_corr) * edge_sum
    dd0 = math.sqrt(abs(dd0_sq))

    return dd0, theta_d, G, l

def arccoth(x):
    """反双曲余切: arccoth(x) = 0.5·ln((x+1)/(x-1)), x > 1"""
    if x <= 1: return float('inf')
    return 0.5 * math.log((x + 1) / (x - 1))

def predict_tc_arccoth_simple(formula, delta_v=0.0):
    """简化arccoth闭式（§11.10，省略温度修正）

    Tc = θ_D / (2·arccoth(x_n))
    x_n = β²(n²-1)Δδ_0² / [4n²(1-βδ_v)(γ_n - γ_1)]
    """
    atoms = parse_formula(formula)
    if not atoms: return 0, {}

    C_mol, _ = build_first_principles_Cmol(atoms)
    atom_features = compute_atom_features(atoms)
    gamma_n, spec_info = gamma_n_from_spectrum(C_mol, atom_features)

    dd0, theta_d, G, l = compute_delta_0_and_theta(atoms)
    if theta_d <= 0 or dd0 <= 0: return 0, {**spec_info, 'dd0': dd0, 'theta_d': theta_d}

    n = max(2.0, spec_info['n_continuous'])
    one_minus_beta_delta = 1.0 - BETA * delta_v
    if one_minus_beta_delta <= 0: return 0, {**spec_info, 'dd0': dd0, 'theta_d': theta_d}

    dgamma = gamma_n - GAMMA_1
    if dgamma <= 0: return 0, {**spec_info, 'dd0': dd0, 'theta_d': theta_d}

    # x_n = β²(n²-1)Δδ_0² / [4n²(1-βδ_v)(γ_n - γ_1)]
    numerator = BETA**2 * (n**2 - 1) * dd0**2
    denominator = 4 * n**2 * one_minus_beta_delta * dgamma
    x = numerator / denominator

    if x <= 1.0:
        return 0, {**spec_info, 'dd0': dd0, 'theta_d': theta_d, 'x': x, 'n': n, 'supercond': False}

    ac = arccoth(x)
    if ac <= 0 or ac == float('inf'):
        return 0, {**spec_info, 'dd0': dd0, 'theta_d': theta_d, 'x': x, 'n': n, 'supercond': False}

    Tc = theta_d / (2 * ac)

    # 物理抑制
    Tc *= math.exp(-15.0 * atom_features['f_fraction'])
    Tc *= math.exp(-3.0 * atom_features['d0_fraction'])

    return Tc, {**spec_info, 'dd0': dd0, 'theta_d': theta_d, 'x': x, 'n': n, 'supercond': True}

def predict_tc_arccoth_full(formula, delta_v=0.0):
    """完整arccoth闭式（含温度修正，解二次方程）

    (ln n)²·y² - [(ln n)² + γ_n - γ_1]·y + β²(n²-1)Δδ_0²/[4n²(1-βδ_v)] = 0
    Tc = θ_D / (2·arccoth(y))
    """
    atoms = parse_formula(formula)
    if not atoms: return 0, {}

    C_mol, _ = build_first_principles_Cmol(atoms)
    atom_features = compute_atom_features(atoms)
    gamma_n, spec_info = gamma_n_from_spectrum(C_mol, atom_features)

    dd0, theta_d, G, l = compute_delta_0_and_theta(atoms)
    if theta_d <= 0 or dd0 <= 0: return 0, {}

    n = max(2.0, spec_info['n_continuous'])
    one_minus_beta_delta = 1.0 - BETA * delta_v
    if one_minus_beta_delta <= 0: return 0, {}

    dgamma = gamma_n - GAMMA_1
    if dgamma <= 0: return 0, {}

    ln_n = math.log(n)
    ln_n_sq = ln_n**2
    A_coeff = ln_n_sq
    B_coeff = -(ln_n_sq + dgamma)
    C_coeff = BETA**2 * (n**2 - 1) * dd0**2 / (4 * n**2 * one_minus_beta_delta)

    disc = B_coeff**2 - 4 * A_coeff * C_coeff
    if disc < 0:
        return 0, {**spec_info, 'dd0': dd0, 'theta_d': theta_d, 'disc': disc, 'supercond': False}

    # 取使y > 1且Tc > 0的根
    y1 = (-B_coeff + math.sqrt(disc)) / (2 * A_coeff)
    y2 = (-B_coeff - math.sqrt(disc)) / (2 * A_coeff)

    # 选择y > 1的根（arccoth需要y > 1）
    y = y1 if y1 > 1 else (y2 if y2 > 1 else None)
    if y is None or y <= 1:
        return 0, {**spec_info, 'dd0': dd0, 'theta_d': theta_d, 'y1': y1, 'y2': y2, 'supercond': False}

    ac = arccoth(y)
    if ac <= 0 or ac == float('inf'):
        return 0, {**spec_info, 'dd0': dd0, 'theta_d': theta_d, 'supercond': False}

    Tc = theta_d / (2 * ac)

    Tc *= math.exp(-15.0 * atom_features['f_fraction'])
    Tc *= math.exp(-3.0 * atom_features['d0_fraction'])

    return Tc, {**spec_info, 'dd0': dd0, 'theta_d': theta_d, 'y': y, 'n': n, 'supercond': True}

def predict_tc_free_energy(formula):
    """自由能公式（当前主框架，对比用）"""
    atoms = parse_formula(formula)
    if not atoms: return 0, {}

    C_mol, _ = build_first_principles_Cmol(atoms)
    atom_features = compute_atom_features(atoms)
    gamma_n, spec_info = gamma_n_from_spectrum(C_mol, atom_features)

    dd0, theta_d, G, l = compute_delta_0_and_theta(atoms)
    if theta_d <= 0 or dd0 <= 0: return 0, {}

    G_safe = max(G, 1e-6)
    K_0 = 7.77e11 * math.exp(0.369 * gamma_n)
    K_eff = K_0 * G_safe**(-0.75) * theta_d**(1.125)
    Tc_sq = 8 * dd0**2 * K_eff * theta_d / (9 * LN2)
    Tc = math.sqrt(max(0, Tc_sq))

    Tc *= math.exp(-15.0 * atom_features['f_fraction'])
    Tc *= math.exp(-3.0 * atom_features['d0_fraction'])

    return Tc, {**spec_info, 'dd0': dd0, 'theta_d': theta_d, 'G': G, 'K_eff': K_eff}

# ============================================================
# 验证
# ============================================================
def symmetric_error(pred, exp):
    if pred <= 0 or exp <= 0: return float('inf')
    return max(pred/exp, exp/pred) - 1

def run_validation():
    data = []
    with open(os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv'), 'r', encoding='utf-8-sig') as fh:
        for row in csv.DictReader(fh):
            try: tc = float(row['临界温度 Tc (K)'])
            except: continue
            if tc > 0:
                data.append({'formula': row['材料(化学式)'], 'cat': row['类别'], 'tc_exp': tc})

    print(f"加载 {len(data)} 个材料\n")
    print(f"β = {BETA:.2f}, γ₁ = {GAMMA_1:.2f}")
    print(f"理论: Tc = θ_D / (2·arccoth(x)), x = β²(n²-1)Δδ₀² / [4n²(1-βδ_v)(γ_n - γ₁)]")
    print(f"不需要 K_0, G, 0.369!\n")

    results = {'simple': [], 'full': [], 'free_energy': []}

    for d in data:
        f = d['formula']; tc_exp = d['tc_exp']

        tc_s, info_s = predict_tc_arccoth_simple(f)
        tc_f, info_f = predict_tc_arccoth_full(f)
        tc_e, info_e = predict_tc_free_energy(f)

        results['simple'].append(symmetric_error(tc_s, tc_exp) if tc_s > 0 else float('inf'))
        results['full'].append(symmetric_error(tc_f, tc_exp) if tc_f > 0 else float('inf'))
        results['free_energy'].append(symmetric_error(tc_e, tc_exp) if tc_e > 0 else float('inf'))

        d['tc_simple'] = tc_s; d['tc_full'] = tc_f; d['tc_free'] = tc_e
        d['info_s'] = info_s; d['info_f'] = info_f

    def stats(errs):
        errs_f = [e for e in errs if e < float('inf')]
        n_total = len(errs)
        n_valid = len(errs_f)
        if not errs_f: return 0, 0, 0, n_valid, n_total
        errs_f.sort()
        med = errs_f[len(errs_f)//2]
        within2 = sum(1 for e in errs_f if e <= 1.0) / n_total * 100
        within5 = sum(1 for e in errs_f if e <= 4.0) / n_total * 100
        return med*100, within2, within5, n_valid, n_total

    print("="*70)
    print(f"{'方法':<30} {'中位%':>8} {'2倍内':>8} {'5倍内':>8} {'有效':>6}")
    print("-"*70)
    for name, key in [('arccoth简化(δ_v=0)', 'simple'),
                       ('arccoth完整(δ_v=0)', 'full'),
                       ('自由能公式(对比)', 'free_energy')]:
        med, w2, w5, nv, nt = stats(results[key])
        print(f"{name:<30} {med:>7.1f}% {w2:>7.1f}% {w5:>7.1f}% {nv:>3}/{nt}")

    # 按类别
    print(f"\n按类别:")
    cats = sorted(set(d['cat'] for d in data))
    header = f"  {'类别':<25} {'简化中位':>8}/{'2倍':>4}  {'完整中位':>8}/{'2倍':>4}  {'自由能中位':>8}/{'2倍':>4}"
    print(header)
    for cat in cats:
        subset = [d for d in data if d['cat'] == cat]
        if len(subset) < 3: continue
        errs_s = [symmetric_error(d['tc_simple'], d['tc_exp']) if d['tc_simple'] > 0 else float('inf') for d in subset]
        errs_f = [symmetric_error(d['tc_full'], d['tc_exp']) if d['tc_full'] > 0 else float('inf') for d in subset]
        errs_e = [symmetric_error(d['tc_free'], d['tc_exp']) if d['tc_free'] > 0 else float('inf') for d in subset]

        def cat_stats(errs):
            ef = sorted([e for e in errs if e < float('inf')])
            if not ef: return 0, 0
            med = ef[len(ef)//2] * 100
            w2 = sum(1 for e in ef if e <= 1.0) / len(errs) * 100
            return med, w2

        ms, ws = cat_stats(errs_s)
        mf, wf = cat_stats(errs_f)
        me, we = cat_stats(errs_e)
        print(f"  {cat:<25} {ms:>7.0f}%/{ws:>3.0f}%  {mf:>7.0f}%/{wf:>3.0f}%  {me:>7.0f}%/{we:>3.0f}%  ({len(subset)})")

    # 最好/最差
    print(f"\n--- arccoth简化 最好10个 ---")
    data_valid = [d for d in data if d['tc_simple'] > 0]
    data_valid.sort(key=lambda d: symmetric_error(d['tc_simple'], d['tc_exp']))
    for d in data_valid[:10]:
        err = symmetric_error(d['tc_simple'], d['tc_exp']) * 100
        n = d['info_s'].get('n', 0)
        x = d['info_s'].get('x', 0)
        print(f"  {d['formula']:<16} exp={d['tc_exp']:>8.1f}K pred={d['tc_simple']:>8.1f}K err={err:>4.0f}% n={n:.1f} x={x:.2f}")

    print(f"\n--- arccoth简化 最差10个 ---")
    data_valid.sort(key=lambda d: symmetric_error(d['tc_simple'], d['tc_exp']), reverse=True)
    for d in data_valid[:10]:
        err = symmetric_error(d['tc_simple'], d['tc_exp']) * 100
        n = d['info_s'].get('n', 0)
        x = d['info_s'].get('x', 0)
        print(f"  {d['formula']:<16} exp={d['tc_exp']:>8.1f}K pred={d['tc_simple']:>8.1f}K err={err:>4.0f}% n={n:.1f} x={x:.2f}")

    # 不超导的（x <= 1）
    no_sc = [d for d in data if d['tc_simple'] == 0]
    print(f"\n--- arccoth简化 判为不超导({len(no_sc)}个) ---")
    for d in no_sc[:10]:
        x = d['info_s'].get('x', 0)
        n = d['info_s'].get('n', 0)
        dd0 = d['info_s'].get('dd0', 0)
        print(f"  {d['formula']:<16} exp={d['tc_exp']:>8.1f}K x={x:.3f} n={n:.1f} Δδ₀={dd0:.4f}")

    # Δδ_0分布
    print(f"\n--- Δδ₀分布 ---")
    dd0s = [d['info_s'].get('dd0', 0) for d in data if d['info_s'].get('dd0', 0) > 0]
    if dd0s:
        dd0s.sort()
        print(f"  范围: [{dd0s[0]:.4f}, {dd0s[-1]:.4f}]")
        print(f"  中位: {dd0s[len(dd0s)//2]:.4f}")
        print(f"  临界Δδ_c≈0.20: {sum(1 for x in dd0s if x < 0.20)}个低于临界")

if __name__ == '__main__':
    run_validation()