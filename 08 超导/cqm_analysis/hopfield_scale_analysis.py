"""分析Hopfield标度因子的物理来源

标度因子 = λep(经验) / λep(Hopfield原始)
变异系数2.25 → 标度因子不是常数, 需要找到它的物理依赖

分析标度因子与以下材料特征的关系:
  1. 谱隙sg
  2. 跨原子耦合Σ|Tij|²
  3. 平均原子质量M
  4. Debye温度θD
  5. C_mol谱的各向异性
  6. 价电子数
  7. 原子半径
"""
import math, csv, os, re, sys
import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework')
from atom_db import ATOM_DB

BETA = 8 * math.pi + 1
C2 = 2.0 / 3.0
B_THEORY = 8 * math.pi / 3
MU_THEORY = 1.0 / (2 * math.sqrt(2))
LAM0_THEORY = 1.0 / math.e
A_THEORY = 8 * math.pi**3 / 3 * (1 - MU_THEORY)
AG_THEORY = 3.0 / (4 * math.pi * (1 - MU_THEORY))
GAMMA_D_GL2 = 2.196681962

RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832,
                 52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
                 67.079811, 69.526405, 72.067158, 75.704690, 77.144840]
GAMMA_1, GAMMA_2 = RIEMANN_ZEROS[0], RIEMANN_ZEROS[1]
DELTA_GAMMA = GAMMA_2 - GAMMA_1

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
LN2 = math.log(2)
C_GAMMA = 7.77e11

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
        for l in range(n): order.append((n+l, n, l))
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
    return [(l, occ, 2*(2*l+1)) for (n, l), occ in sorted(config.items(), reverse=True) if n >= max_n - 1]

def build_Cmol(atoms):
    els = list(atoms.keys()); blocks = []; bi = []; couplings = []
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        for l, occ, cap in valence_orbitals(z):
            if l == 0: blocks.append(A1.copy()); bi.append((el, 's', 1))
            elif l == 1: blocks.append(A3.copy()); bi.append((el, 'p', 3))
            elif l == 2: blocks.append(A4.copy()); bi.append((el, 'd', 4))
    if not blocks: return np.array([[2.0]]), bi, []
    size = sum(b.shape[0] for b in blocks); C = np.zeros((size, size)); idx = 0
    for b in blocks: s = b.shape[0]; C[idx:idx+s, idx:idx+s] = b; idx += s
    idx_i = 0
    for i, binfo in enumerate(bi):
        si = binfo[2]; idx_j = idx_i + si
        for j, bjinfo in enumerate(bi[i+1:], start=i+1):
            sj = bjinfo[2]; ri = ATOM_DB.get(binfo[0], (1, 0, 1.5, 8))[2]; rj = ATOM_DB.get(bjinfo[0], (1, 0, 1.5, 8))[2]
            t0 = 0.1 * math.exp(-(ri + rj) / 3.0)
            if (binfo[1] == 'd' and bjinfo[1] == 'p') or (binfo[1] == 'p' and bjinfo[1] == 'd'): t0 *= 1.5
            for a in range(si):
                for b in range(sj): C[idx_i+a, idx_j+b] = t0; C[idx_j+b, idx_i+a] = t0
            couplings.append(t0)
            idx_j += sj
        idx_i += si
    return C, bi, couplings

def atom_features(atoms):
    els = list(atoms.keys()); n_atoms = sum(atoms.values())
    inv_mass = sum(atoms[el]/ATOM_DB[el][0] for el in els)/n_atoms
    dp = 0; d0 = 0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50); vo = valence_orbitals(z)
        hd = hp = False
        for l, occ, cap in vo:
            if l == 2: hd = True
            if l == 1: hp = True
            if l == 2 and occ == 0: d0 += atoms[el]
        if hd and hp: dp += atoms[el]
    f_count = 0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        for (n, l), occ in madelung_config(z).items():
            if l == 3 and 0 < occ < 14: f_count += atoms[el]; break
    return {'inv_mass': inv_mass, 'dp': dp/n_atoms, 'o': atoms.get('O',0)/n_atoms,
            'f': f_count/n_atoms, 'd0': d0/n_atoms}

def analyze_hopfield(formula):
    atoms = {}
    for el, cnt in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', formula):
        if el in ATOM_DB: atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    if not atoms: return None

    C, bi, couplings = build_Cmol(atoms)
    af = atom_features(atoms)
    ev = np.sort(np.linalg.eigvalsh(C))
    if len(ev) < 2: return None
    sg = max(ev[1] - ev[0], 0.05)
    m_ev = np.mean(ev); aniso = np.std(ev / m_ev if m_ev > 0 else ev)

    els = list(atoms.keys()); n_atoms = sum(atoms.values())
    avg_r = sum(atoms[el] * ATOM_DB[el][2] for el in els) / n_atoms
    l = max(2 * avg_r * 1e-10, 1e-20)
    theta_d = sum(atoms[el] * ATOM_DB[el][1] for el in els) / n_atoms
    if theta_d <= 0: return None

    # 经验映射λep
    c_aniso = GAMMA_D_GL2 / (2 * math.pi)
    c_o = B_THEORY**2 * 0.25 / (3 * 8 * LAM0_THEORY**2)
    nc = 4.00 + 0.50 * math.log(1/sg) + c_aniso * aniso + 13.0 * af['inv_mass'] + 0.05 * af['dp'] + c_o * af['o']
    ni = int(nc); frac = nc - ni
    if ni < 1: gn = RIEMANN_ZEROS[0]
    elif ni >= len(RIEMANN_ZEROS): gn = 2 * math.pi * nc / math.log(nc / (2 * math.pi)) if nc > 6 else RIEMANN_ZEROS[-1]
    else: gn = RIEMANN_ZEROS[ni-1] + frac * (RIEMANN_ZEROS[ni] - RIEMANN_ZEROS[ni-1])
    lambda_ep_emp = B_THEORY / (A_THEORY - gn) if A_THEORY > gn else 0.3

    # Hopfield原始量
    N0 = 1.0 / sg
    g2 = sum(t**2 for t in couplings) if couplings else 0.01
    M_avg = sum(atoms[el] * ATOM_DB[el][0] for el in els) * AMU / n_atoms
    omega_d = theta_d * KB / HBAR
    omega_d2 = omega_d**2
    t_scale = 0.1 * 1.6e-19  # 0.1 eV

    lambda_ep_raw = N0 * g2 / (M_avg * omega_d2 * l**2) * t_scale

    if lambda_ep_raw <= 0: return None

    # 标度因子 = λep(经验) / λep(原始)
    scale = lambda_ep_emp / lambda_ep_raw

    # 收集所有可能相关的特征
    n_valence = sum(sum(occ for _, occ, _ in valence_orbitals(ATOMIC_NUMBERS.get(el, 50))) * atoms[el] for el in els) / n_atoms
    n_couplings = len(couplings)
    avg_coupling = np.mean(couplings) if couplings else 0
    max_ev = ev[-1]; min_ev = ev[0]
    spectral_radius = max_ev - min_ev
    dim_Cmol = C.shape[0]
    trace_C = np.trace(C)

    return {
        'scale': scale, 'lambda_ep_emp': lambda_ep_emp, 'lambda_ep_raw': lambda_ep_raw,
        'sg': sg, 'aniso': aniso, 'N0': N0, 'g2': g2, 'M_avg': M_avg,
        'omega_d': omega_d, 'theta_d': theta_d, 'l': l, 'avg_r': avg_r,
        'n_atoms': n_atoms, 'n_valence': n_valence, 'n_couplings': n_couplings,
        'avg_coupling': avg_coupling, 'spectral_radius': spectral_radius,
        'dim_Cmol': dim_Cmol, 'trace_C': trace_C,
        'max_ev': max_ev, 'min_ev': min_ev,
        'inv_mass': af['inv_mass'], 'dp': af['dp'], 'o': af['o'],
        'f': af['f'], 'd0': af['d0'],
    }

# 主程序
data = []
with open(os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv'), 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc > 0: data.append({'f': row['材料(化学式)'], 'cat': row['类别'], 'tc': tc})

results = []
for d in data:
    r = analyze_hopfield(d['f'])
    if r is None: continue
    r['formula'] = d['f']; r['cat'] = d['cat']
    results.append(r)

print("="*70)
print("Hopfield标度因子物理来源分析")
print("="*70)
print(f"样本数: {len(results)}")

scales = [r['scale'] for r in results]
scales.sort()
print(f"标度因子: 中位={scales[len(scales)//2]:.1f}, 范围=[{scales[0]:.1f}, {scales[-1]:.1f}]")
print(f"变异系数: {np.std(scales)/np.mean(scales):.2f}")

# 分析log(scale)与各特征的偏相关
log_scales = np.array([math.log(r['scale']) for r in results])

features = {
    'log(sg)': np.array([math.log(r['sg']) for r in results]),
    'log(aniso)': np.array([math.log(max(r['aniso'], 1e-10)) for r in results]),
    'log(N0)': np.array([math.log(r['N0']) for r in results]),
    'log(g2)': np.array([math.log(r['g2']) for r in results]),
    'log(M)': np.array([math.log(r['M_avg']) for r in results]),
    'log(ωD)': np.array([math.log(r['omega_d']) for r in results]),
    'log(θD)': np.array([math.log(r['theta_d']) for r in results]),
    'log(l)': np.array([math.log(r['l']) for r in results]),
    'log(avg_r)': np.array([math.log(r['avg_r']) for r in results]),
    'n_atoms': np.array([r['n_atoms'] for r in results]),
    'n_valence': np.array([r['n_valence'] for r in results]),
    'n_couplings': np.array([r['n_couplings'] for r in results]),
    'log(avg_coup)': np.array([math.log(max(r['avg_coupling'], 1e-10)) for r in results]),
    'log(spec_rad)': np.array([math.log(max(r['spectral_radius'], 1e-10)) for r in results]),
    'dim_Cmol': np.array([r['dim_Cmol'] for r in results]),
    'log(trace_C)': np.array([math.log(max(r['trace_C'], 1e-10)) for r in results]),
    'inv_mass': np.array([r['inv_mass'] for r in results]),
    'dp': np.array([r['dp'] for r in results]),
    'o_frac': np.array([r['o'] for r in results]),
}

print(f"\nlog(标度因子)与各特征偏相关:")
corrs = []
for name, vals in features.items():
    if np.std(vals) < 1e-10: continue
    corr = np.corrcoef(log_scales, vals)[0, 1]
    corrs.append((abs(corr), corr, name))
corrs.sort(reverse=True)
for _, corr, name in corrs:
    print(f"  {name:15s}: r = {corr:+.3f}")

# 多变量回归: log(scale) = a + b1*x1 + b2*x2 + ...
# 用前5个最相关特征
top_features = [name for _, _, name in corrs[:5]]
print(f"\n多变量回归: log(scale) ~ {top_features}")

X = np.column_stack([features[f] for f in top_features])
X = np.column_stack([np.ones(len(X)), X])
# 最小二乘
beta, _, _, _ = np.linalg.lstsq(X, log_scales, rcond=None)
pred = X @ beta
residual = log_scales - pred
r2 = 1 - np.var(residual) / np.var(log_scales)
print(f"  R² = {r2:.3f}")
print(f"  系数: {dict(zip(['const'] + top_features, beta))}")

# 残差变异系数
residual_scale = np.exp(residual)
print(f"  残差标度因子: 变异系数={np.std(residual_scale)/np.mean(residual_scale):.2f}")
print(f"  残差范围: [{np.min(residual_scale):.2f}, {np.max(residual_scale):.2f}]")

# 尝试更多特征
top_features_10 = [name for _, _, name in corrs[:10]]
print(f"\n用10个特征: log(scale) ~ {top_features_10}")
X10 = np.column_stack([features[f] for f in top_features_10])
X10 = np.column_stack([np.ones(len(X10)), X10])
beta10, _, _, _ = np.linalg.lstsq(X10, log_scales, rcond=None)
pred10 = X10 @ beta10
residual10 = log_scales - pred10
r2_10 = 1 - np.var(residual10) / np.var(log_scales)
residual10_scale = np.exp(residual10)
print(f"  R² = {r2_10:.3f}")
print(f"  残差变异系数={np.std(residual10_scale)/np.mean(residual10_scale):.2f}")

# 关键: 如果标度因子可以用C_mol谱特征解释, 那Hopfield方程就是第一性的
# 标度因子 = f(sg, aniso, N0, g2, M, ωD, ...)
print(f"\n{'='*70}")
print("结论")
print("="*70)
if r2_10 > 0.8:
    print(f"标度因子可用C_mol谱特征解释 (R²={r2_10:.3f})")
    print("=> Hopfield方程是第一性的, 标度因子从C_mol谱导出")
    print(f"=> 改进Hopfield: λep = N(0)·|g|²/(M·ωD²) × f(C_mol谱)")
elif r2_10 > 0.5:
    print(f"标度因子部分可用C_mol谱特征解释 (R²={r2_10:.3f})")
    print("=> 需要更多物理量(如Fermi面信息)来解释标度因子")
else:
    print(f"标度因子不能用C_mol谱特征解释 (R²={r2_10:.3f})")
    print("=> Hopfield方程需要根本性改进, 或标度因子来自C_mol以外的信息")