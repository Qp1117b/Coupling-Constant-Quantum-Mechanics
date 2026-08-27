"""从实验Tc反推δ_v，分析δ_v与C_mol谱特征的关系

arccoth闭式: Tc = θ_D / (2·arccoth(x))
x = β²(n²-1)Δδ₀² / [4n²(1-βδ_v)(γ_n - γ₁)]

反推: 给定Tc_exp, 求δ_v
  x = coth(θ_D / (2·Tc_exp))
  1-βδ_v = β²(n²-1)Δδ₀² / [4n²·x·(γ_n-γ₁)]
  δ_v = (1/β)·[1 - β²(n²-1)Δδ₀² / (4n²·x·(γ_n-γ₁))]

然后分析δ_v vs C_mol谱特征(谱间隙, 各向异性, 简并度等)
"""
import sys, os, math, csv, re
import numpy as np

sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework')
from atom_db import ATOM_DB

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
C2 = 2.0/3.0; LN2 = math.log(2)
BETA = 8 * math.pi + 1

RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832,
                 52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
                 67.079811, 69.526405, 72.067158, 75.704690, 77.144840]
GAMMA_1 = RIEMANN_ZEROS[0]

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

A1 = np.array([[2.0]])
A3 = np.array([[2,-1,0],[-1,2,-1],[0,-1,2]])
A4 = np.array([[2,-1,0,0],[-1,2,-1,0],[0,-1,2,-1],[0,0,-1,2]])

def madelung_config(z):
    order = []
    for n in range(1, 8):
        for l in range(n):
            order.append((n+l, n, l))
    order.sort(key=lambda x: (x[0], x[1]))
    config = {}; remaining = z
    for _, n, l in order:
        cap = 2*(2*l+1); fill = min(remaining, cap)
        if fill > 0: config[(n, l)] = fill; remaining -= fill
        if remaining == 0: break
    exceptions = {57: {(4,3): 0, (5,2): 1}, 58: {(4,3): 1, (5,2): 1}, 64: {(4,3): 7, (5,2): 1},
                  89: {(5,3): 0, (6,2): 1}, 90: {(5,3): 0, (6,2): 2}, 96: {(5,3): 7, (6,2): 1}}
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
            cap = 2*(2*l+1); valence.append((l, occ, cap))
    return valence

def build_first_principles_Cmol(atoms):
    els = list(atoms.keys())
    blocks = []; block_info = []
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50); vo = valence_orbitals(z)
        for l, occ, cap in vo:
            if l == 0: blocks.append(A1.copy()); block_info.append((el, 's', 1))
            elif l == 1: blocks.append(A3.copy()); block_info.append((el, 'p', 3))
            elif l == 2: blocks.append(A4.copy()); block_info.append((el, 'd', 4))
    if not blocks: return np.array([[2.0]]), [('X', 's', 1)]
    size = sum(b.shape[0] for b in blocks)
    C = np.zeros((size, size)); idx = 0
    for b in blocks:
        s = b.shape[0]; C[idx:idx+s, idx:idx+s] = b; idx += s
    idx_i = 0
    for i, bi in enumerate(block_info):
        si = bi[2]; idx_j = idx_i + si
        for j, bj in enumerate(block_info[i+1:], start=i+1):
            sj = bj[2]; el_i, el_j = bi[0], bj[0]
            ri = ATOM_DB.get(el_i, (1, 0, 1.5, 8))[2]; rj = ATOM_DB.get(el_j, (1, 0, 1.5, 8))[2]
            d = ri + rj; t0 = 0.1 * math.exp(-d / 3.0)
            li, lj = bi[1], bj[1]
            if (li == 'd' and lj == 'p') or (li == 'p' and lj == 'd'): t0 *= 1.5
            for a in range(si):
                for b in range(sj):
                    C[idx_i + a, idx_j + b] = t0; C[idx_j + b, idx_i + a] = t0
            idx_j += sj
        idx_i += si
    return C, block_info

def compute_atom_features(atoms):
    els = list(atoms.keys()); n_atoms = sum(atoms.values())
    inv_mass_avg = sum(atoms[el] / ATOM_DB[el][0] for el in els) / n_atoms
    dp_hybrid = 0; d_empty_count = 0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50); vo = valence_orbitals(z)
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
        z = ATOMIC_NUMBERS.get(el, 50); config = madelung_config(z)
        for (n_qn, l_qn), occ in config.items():
            if l_qn == 3 and 0 < occ < 14: f_count += atoms[el]; break
    f_fraction = f_count / n_atoms; d0_fraction = d_empty_count / n_atoms
    return {'inv_mass_avg': inv_mass_avg, 'dp_hybrid': dp_hybrid, 'o_fraction': o_fraction,
            'f_fraction': f_fraction, 'd0_fraction': d0_fraction}

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
    if n < 2: return RIEMANN_ZEROS[0], {'n_continuous': 1.0}
    sg = eigvals[1] - eigvals[0]
    ev_mean = np.mean(eigvals); ev_norm = eigvals / ev_mean if ev_mean > 0 else eigvals
    anisotropy = np.std(ev_norm)
    inv_mass = atom_features.get('inv_mass_avg', 0) if atom_features else 0
    dp_hybrid = atom_features.get('dp_hybrid', 0) if atom_features else 0
    o_frac = atom_features.get('o_fraction', 0) if atom_features else 0
    sg_safe = max(sg, 0.05)
    n_continuous = (4.00 + 0.50 * math.log(1.0 / sg_safe) + 0.35 * anisotropy
                    + 13.00 * inv_mass + 0.05 * dp_hybrid + 5.50 * o_frac)
    gamma_n = interpolate_gamma_n(n_continuous)
    return gamma_n, {'spectral_gap': sg, 'anisotropy': anisotropy, 'n_continuous': n_continuous}

def parse_formula(f):
    pairs = re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f)
    atoms = {}
    for el, cnt in pairs:
        if el in ATOM_DB: atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    return atoms

def compute_physical_quantities(atoms):
    """计算Δδ_0(intra), Δδ_0(inter), θ_D, G, l, L"""
    els = list(atoms.keys()); n_atoms = sum(atoms.values())
    avg_r = sum(atoms[el] * ATOM_DB[el][2] for el in els) / n_atoms
    l = 2 * avg_r * 1e-10  # 原子间距
    L = 2 * max(ATOM_DB[el][2] for el in els) * 1e-10  # 晶胞间距离(用最大半径)
    theta_d = sum(atoms[el] * ATOM_DB[el][1] for el in els) / n_atoms
    if theta_d <= 0: return None

    n_eff = max(2, n_atoms)
    f_corr = 1.0 - 0.3 * (1.0 - 1.0/n_eff)

    # intra edges (原子间)
    edge_sum_intra = 0
    for i in range(len(els)):
        for j in range(i+1, len(els)):
            mi = atoms[els[i]] * ATOM_DB[els[i]][0] * AMU
            mj = atoms[els[j]] * ATOM_DB[els[j]][0] * AMU
            edge_sum_intra += (1.0/mi + 1.0/mj)
    if not edge_sum_intra:
        total_m = sum(atoms[el] * ATOM_DB[el][0] for el in els)
        mi = total_m * AMU / n_atoms
        edge_sum_intra = max(1, n_eff*(n_eff-1)/2) * 2.0 / mi

    # inter (晶胞间): 2z/M_cell
    total_m_kg = sum(atoms[el] * ATOM_DB[el][0] for el in els) * AMU
    z_coord = 8  # 典型配位数
    inter_term = 2 * z_coord / total_m_kg

    omega_d = theta_d * KB / HBAR

    # Δδ_intra²
    dd0_intra_sq = (C2/l**2) * (3*HBAR/(4*omega_d)) * (1-f_corr) * edge_sum_intra

    # Δδ_inter²
    dd0_inter_sq = (C2/L**2) * (3*HBAR/(4*omega_d)) * (1-f_corr) * inter_term

    # 双尺度
    dd0_sq = dd0_intra_sq + dd0_inter_sq
    dd0 = math.sqrt(abs(dd0_sq))

    G = (1.0/l) * math.sqrt((1.0-f_corr) * edge_sum_intra)

    return {
        'dd0': dd0, 'dd0_intra': math.sqrt(abs(dd0_intra_sq)),
        'dd0_inter': math.sqrt(abs(dd0_inter_sq)),
        'theta_d': theta_d, 'G': G, 'l': l, 'L': L,
        'dd0_intra_frac': math.sqrt(abs(dd0_intra_sq))/dd0 if dd0 > 0 else 0,
        'dd0_inter_frac': math.sqrt(abs(dd0_inter_sq))/dd0 if dd0 > 0 else 0,
    }

def compute_cmol_features(C_mol):
    """从C_mol谱计算各种特征"""
    eigvals = np.sort(np.linalg.eigvalsh(C_mol))
    n = len(eigvals)
    if n < 2: return {}

    sg = eigvals[1] - eigvals[0]
    ev_mean = np.mean(eigvals); ev_std = np.std(eigvals)
    ev_norm = eigvals / ev_mean if ev_mean > 0 else eigvals
    anisotropy = np.std(ev_norm)

    # 谱重心
    centroid = ev_mean

    # 谱宽度
    width = eigvals[-1] - eigvals[0]

    # 谱简并度(近似)
    degeneracies = []
    for i in range(n):
        deg = sum(1 for j in range(n) if abs(eigvals[i] - eigvals[j]) < 0.01)
        degeneracies.append(deg)
    max_degen = max(degeneracies)

    # 谱偏度
    skewness = np.mean(((eigvals - ev_mean) / ev_std) ** 3) if ev_std > 0 else 0

    # 谱峭度
    kurtosis = np.mean(((eigvals - ev_mean) / ev_std) ** 4) - 3 if ev_std > 0 else 0

    # 对角块强度 vs 跨原子耦合
    diag_mean = np.mean(np.diag(C_mol))
    off_diag = C_mol - np.diag(np.diag(C_mol))
    off_diag_norm = np.linalg.norm(off_diag) / np.linalg.norm(C_mol) if np.linalg.norm(C_mol) > 0 else 0

    # 条件数
    cond = abs(eigvals[-1] / eigvals[0]) if abs(eigvals[0]) > 1e-10 else 0

    return {
        'spectral_gap': sg, 'anisotropy': anisotropy, 'centroid': centroid,
        'width': width, 'max_degen': max_degen, 'skewness': skewness,
        'kurtosis': kurtosis, 'diag_mean': diag_mean, 'off_diag_ratio': off_diag_norm,
        'cond': cond, 'n_dim': n,
    }

def reverse_delta_v(tc_exp, theta_d, dd0, gamma_n, n):
    """从实验Tc反推δ_v

    x = coth(θ_D / (2·Tc))
    1-βδ_v = β²(n²-1)Δδ₀² / [4n²·x·(γ_n-γ₁)]
    δ_v = (1/β)·[1 - β²(n²-1)Δδ₀²/(4n²·x·(γ_n-γ₁))]
    """
    if tc_exp <= 0 or theta_d <= 0 or dd0 <= 0: return None

    arg = theta_d / (2 * tc_exp)
    if arg < 1: return None  # coth需要arg > 0, 但coth(x) > 1 for x > 0

    x = 1.0 / math.tanh(arg)  # coth = 1/tanh
    if x <= 1: return None

    dgamma = gamma_n - GAMMA_1
    if dgamma <= 0: return None

    numerator = BETA**2 * (n**2 - 1) * dd0**2
    denominator = 4 * n**2 * x * dgamma

    one_minus_beta_delta = numerator / denominator
    if one_minus_beta_delta <= 0 or one_minus_beta_delta > 1: return None

    delta_v = (1.0 - one_minus_beta_delta) / BETA
    return delta_v

def run_analysis():
    data = []
    with open(os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv'), 'r', encoding='utf-8-sig') as fh:
        for row in csv.DictReader(fh):
            try: tc = float(row['临界温度 Tc (K)'])
            except: continue
            if tc > 0:
                data.append({'formula': row['材料(化学式)'], 'cat': row['类别'], 'tc_exp': tc})

    print(f"加载 {len(data)} 个材料")
    print(f"β = {BETA:.2f}, 1/β = {1/BETA:.4f}\n")

    results = []
    for d in data:
        atoms = parse_formula(d['formula'])
        if not atoms: continue

        C_mol, _ = build_first_principles_Cmol(atoms)
        atom_features = compute_atom_features(atoms)
        gamma_n, spec_info = gamma_n_from_spectrum(C_mol, atom_features)
        pq = compute_physical_quantities(atoms)
        if pq is None: continue

        n = max(2.0, spec_info['n_continuous'])
        cmol_feat = compute_cmol_features(C_mol)

        # 反推δ_v
        delta_v = reverse_delta_v(d['tc_exp'], pq['theta_d'], pq['dd0'], gamma_n, n)

        # 物理抑制
        f_frac = atom_features['f_fraction']
        d0_frac = atom_features['d0_fraction']

        r = {
            'formula': d['formula'], 'cat': d['cat'], 'tc_exp': d['tc_exp'],
            'gamma_n': gamma_n, 'n': n,
            'dd0': pq['dd0'], 'dd0_intra': pq['dd0_intra'], 'dd0_inter': pq['dd0_inter'],
            'dd0_inter_frac': pq['dd0_inter_frac'],
            'theta_d': pq['theta_d'], 'G': pq['G'],
            'delta_v': delta_v, 'beta_delta_v': BETA * delta_v if delta_v else None,
            'f_frac': f_frac, 'd0_frac': d0_frac,
            'inv_mass': atom_features['inv_mass_avg'],
            **cmol_feat,
        }
        results.append(r)

    valid = [r for r in results if r['delta_v'] is not None and r['delta_v'] > 0]
    print(f"有效反推: {len(valid)}/{len(results)}")

    # δ_v统计
    dvs = [r['delta_v'] for r in valid]
    dvs.sort()
    print(f"\n=== δ_v反推统计 ===")
    print(f"  范围: [{dvs[0]:.4f}, {dvs[-1]:.4f}]")
    print(f"  中位: {dvs[len(dvs)//2]:.4f}")
    print(f"  1/β = {1/BETA:.4f}")
    print(f"  βδ_v中位: {BETA*dvs[len(dvs)//2]:.3f}")

    # 按类别
    print(f"\n=== δ_v按类别 ===")
    cats = sorted(set(r['cat'] for r in valid))
    for cat in cats:
        subset = [r for r in valid if r['cat'] == cat]
        if len(subset) < 3: continue
        dvs_c = sorted([r['delta_v'] for r in subset])
        bds = sorted([r['beta_delta_v'] for r in subset])
        print(f"  {cat:<25} δ_v中位={dvs_c[len(dvs_c)//2]:.4f} βδ_v中位={bds[len(bds)//2]:.3f} ({len(subset)})")

    # δ_v vs C_mol特征相关性
    print(f"\n=== δ_v vs C_mol特征相关性 ===")
    features = ['spectral_gap', 'anisotropy', 'centroid', 'width', 'max_degen',
                'skewness', 'kurtosis', 'diag_mean', 'off_diag_ratio', 'cond', 'n_dim',
                'inv_mass', 'gamma_n', 'dd0', 'theta_d', 'G']

    for feat in features:
        xs = [r[feat] for r in valid if r[feat] is not None]
        ys = [r['delta_v'] for r in valid if r[feat] is not None]
        if len(xs) < 10: continue
        xs = np.array(xs); ys = np.array(ys)
        if np.std(xs) < 1e-10: continue
        corr = np.corrcoef(xs, ys)[0, 1]
        print(f"  corr(δ_v, {feat:<20s}) = {corr:+.3f}")

    # βδ_v vs 特征
    print(f"\n=== βδ_v vs C_mol特征相关性 ===")
    for feat in ['spectral_gap', 'anisotropy', 'inv_mass', 'gamma_n', 'dd0', 'theta_d']:
        xs = [r[feat] for r in valid if r[feat] is not None]
        ys = [r['beta_delta_v'] for r in valid if r[feat] is not None]
        if len(xs) < 10: continue
        xs = np.array(xs); ys = np.array(ys)
        if np.std(xs) < 1e-10: continue
        corr = np.corrcoef(xs, ys)[0, 1]
        print(f"  corr(βδ_v, {feat:<20s}) = {corr:+.3f}")

    # 双尺度Δδ_0分析
    print(f"\n=== 双尺度Δδ_0 ===")
    inter_fracs = [r['dd0_inter_frac'] for r in valid]
    inter_fracs.sort()
    print(f"  inter占比: 中位{inter_fracs[len(inter_fracs)//2]:.3f}")
    print(f"  intra占比: 中位{1-inter_fracs[len(inter_fracs)//2]:.3f}")

    # δ_v与1/β的接近度
    print(f"\n=== δ_v与1/β的接近度 ===")
    for r in sorted(valid, key=lambda x: abs(x['beta_delta_v'] - 1))[:15]:
        print(f"  {r['formula']:<16} δ_v={r['delta_v']:.4f} βδ_v={r['beta_delta_v']:.3f} "
              f"Tc={r['tc_exp']:.1f}K Δδ₀={r['dd0']:.4f} γ={r['gamma_n']:.1f}")

    # δ_v与γ_n的关系
    print(f"\n=== δ_v vs γ_n 散点 ===")
    for r in sorted(valid, key=lambda x: x['gamma_n'])[:10]:
        print(f"  γ={r['gamma_n']:.1f}: {r['formula']:<16} δ_v={r['delta_v']:.4f} βδ_v={r['beta_delta_v']:.3f}")
    print("  ...")
    for r in sorted(valid, key=lambda x: x['gamma_n'])[-10:]:
        print(f"  γ={r['gamma_n']:.1f}: {r['formula']:<16} δ_v={r['delta_v']:.4f} βδ_v={r['beta_delta_v']:.3f}")

    # 回归 δ_v = f(C_mol特征)
    print(f"\n=== 多变量回归 δ_v ===")
    from numpy.linalg import lstsq
    feat_list = ['spectral_gap', 'anisotropy', 'inv_mass', 'gamma_n', 'dd0', 'theta_d', 'n_dim']
    X = []
    for r in valid:
        row = [1.0]  # bias
        for f in feat_list:
            v = r.get(f, 0)
            if v is not None:
                row.append(v)
            else:
                row.append(0)
        X.append(row)
    X = np.array(X)
    y = np.array([r['delta_v'] for r in valid])

    # Ridge回归
    lam = 1.0
    XtX = X.T @ X + lam * np.eye(X.shape[1])
    Xty = X.T @ y
    beta = np.linalg.solve(XtX, Xty)
    y_pred = X @ beta
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    print(f"  R² = {r2:.3f}")
    print(f"  特征: {feat_list}")
    print(f"  系数: {beta}")

if __name__ == '__main__':
    run_analysis()