"""用改进的Hopfield方程(标度因子从C_mol谱回归)预测Tc

标度因子 = exp(const + 1.59·log(θD) - 0.24·log(ωD) - 5.62·inv_mass
                + 0.35·log(trace_C) - 1.48·log(g2) + ...)

改进Hopfield: λep = N(0)·|g|²/(M·ωD²) × C_scale(C_mol谱)

验证: 用改进Hopfield方程预测Tc, 与经验映射对比
"""
import math, csv, os, re, sys
import numpy as np

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

def compute_lambda_ep_hopfield_improved(atoms, C, ev, couplings, theta_d, l, af):
    """改进Hopfield方程: λep = N(0)·|g|²/(M·ωD²) × C_scale(C_mol谱)

    C_scale从C_mol谱特征回归 (R²=0.949)
    """
    els = list(atoms.keys()); n_atoms = sum(atoms.values())
    sg = max(ev[1] - ev[0], 0.05)

    N0 = 1.0 / sg
    g2 = sum(t**2 for t in couplings) if couplings else 0.01
    M_avg = sum(atoms[el] * ATOM_DB[el][0] for el in els) * AMU / n_atoms
    omega_d = theta_d * KB / HBAR
    omega_d2 = omega_d**2
    t_scale = 0.1 * 1.6e-19

    lambda_ep_raw = N0 * g2 / (M_avg * omega_d2 * l**2) * t_scale

    # 改进标度因子: 从C_mol谱特征
    trace_C = np.trace(C)
    log_scale = (-0.07
                 + 1.59 * math.log(theta_d)
                 - 0.24 * math.log(omega_d)
                 - 5.62 * af['inv_mass']
                 + 0.35 * math.log(max(trace_C, 1e-10))
                 - 1.48 * math.log(max(g2, 1e-10)))
    C_scale = math.exp(log_scale)

    lambda_ep = lambda_ep_raw * C_scale
    return max(0.01, min(3.0, lambda_ep))

def solve_tc(formula, method='empirical'):
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
    n_eff = max(2, n_atoms); f_corr = 1.0 - 0.3 * (1.0 - 1.0 / n_eff)
    es = 0
    for i in range(len(els)):
        for j in range(i+1, len(els)):
            mi = atoms[els[i]] * ATOM_DB[els[i]][0] * AMU; mj = atoms[els[j]] * ATOM_DB[els[j]][0] * AMU
            es += (1/mi + 1/mj)
    if not es:
        mi = sum(atoms[el] * ATOM_DB[el][0] for el in els) * AMU / n_atoms
        es = max(1, n_eff * (n_eff-1) / 2) * 2.0 / mi

    omega_d = theta_d * KB / HBAR
    dd0_sq = (C2 / l**2) * (3 * HBAR / (4 * omega_d)) * (1 - f_corr) * es
    dd0 = math.sqrt(abs(dd0_sq))
    G = (1 / l) * math.sqrt((1 - f_corr) * es)

    # λep计算
    if method == 'empirical':
        c_aniso = GAMMA_D_GL2 / (2 * math.pi)
        c_o = B_THEORY**2 * 0.25 / (3 * 8 * LAM0_THEORY**2)
        nc = 4.00 + 0.50 * math.log(1/sg) + c_aniso * aniso + 13.0 * af['inv_mass'] + 0.05 * af['dp'] + c_o * af['o']
        ni = int(nc); frac = nc - ni
        if ni < 1: gn = RIEMANN_ZEROS[0]
        elif ni >= len(RIEMANN_ZEROS): gn = 2 * math.pi * nc / math.log(nc / (2 * math.pi)) if nc > 6 else RIEMANN_ZEROS[-1]
        else: gn = RIEMANN_ZEROS[ni-1] + frac * (RIEMANN_ZEROS[ni] - RIEMANN_ZEROS[ni-1])
        lambda_ep = B_THEORY / (A_THEORY - gn) if A_THEORY > gn else 0.3
    elif method == 'hopfield':
        lambda_ep = compute_lambda_ep_hopfield_improved(atoms, C, ev, couplings, theta_d, l, af)
        gn = A_THEORY - B_THEORY / lambda_ep

    K0 = C_GAMMA * math.exp(AG_THEORY * gn)
    K_eff = K0 * max(G, 1e-6)**(-0.75) * theta_d**(1.125)
    suppress = math.exp(-15.0 * af['f']) * math.exp(-3.0 * af['d0'])
    Tc = math.sqrt(8 * dd0**2 * K_eff * theta_d / (9 * LN2)) * suppress

    return {'Tc': Tc, 'lambda_ep': lambda_ep, 'gn': gn}

# 主程序
data = []
with open(os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv'), 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc > 0: data.append({'f': row['材料(化学式)'], 'cat': row['类别'], 'tc': tc})

def sym_err(p, e):
    if p <= 0 or e <= 0: return float('inf')
    return max(p/e, e/p) - 1

# 方法A: 经验映射
errs_A = []; cat_A = {}
for d in data:
    r = solve_tc(d['f'], 'empirical')
    if r is None or r['Tc'] <= 0: continue
    e = sym_err(r['Tc'], d['tc'])
    errs_A.append(e)
    if d['cat'] not in cat_A: cat_A[d['cat']] = []
    cat_A[d['cat']].append(e)

# 方法B: 改进Hopfield
errs_B = []; cat_B = {}
for d in data:
    r = solve_tc(d['f'], 'hopfield')
    if r is None or r['Tc'] <= 0: continue
    e = sym_err(r['Tc'], d['tc'])
    errs_B.append(e)
    if d['cat'] not in cat_B: cat_B[d['cat']] = []
    cat_B[d['cat']].append(e)

errs_A.sort(); errs_B.sort()

print("="*70)
print("改进Hopfield方程 vs 经验映射")
print("="*70)

print(f"\n方法A (经验映射λep):")
print(f"  n={len(errs_A)}, 中位{errs_A[len(errs_A)//2]*100:.1f}%, 2倍内{sum(1 for e in errs_A if e<=1.0)/len(errs_A)*100:.1f}%, 5倍内{sum(1 for e in errs_A if e<=4.0)/len(errs_A)*100:.1f}%")

print(f"\n方法B (改进Hopfield, 标度因子从C_mol谱):")
print(f"  n={len(errs_B)}, 中位{errs_B[len(errs_B)//2]*100:.1f}%, 2倍内{sum(1 for e in errs_B if e<=1.0)/len(errs_B)*100:.1f}%, 5倍内{sum(1 for e in errs_B if e<=4.0)/len(errs_B)*100:.1f}%")

print(f"\n按类别对比:")
print(f"  {'类别':20s} {'n':>3s} {'A-2倍内':>8s} {'B-2倍内':>8s} {'A-中位':>8s} {'B-中位':>8s}")
for cat in sorted(set(list(cat_A.keys()) + list(cat_B.keys())), key=lambda c: -len(cat_A.get(c, []))):
    ea = cat_A.get(cat, []); eb = cat_B.get(cat, [])
    if len(ea) < 3: continue
    ea.sort(); eb.sort()
    a2 = sum(1 for e in ea if e <= 1.0) / len(ea) * 100
    b2 = sum(1 for e in eb if e <= 1.0) / len(eb) * 100
    am = ea[len(ea)//2] * 100
    bm = eb[len(eb)//2] * 100
    print(f"  {cat:20s} {len(ea):3d} {a2:7.0f}% {b2:7.0f}% {am:7.0f}% {bm:7.0f}%")

# λep对比
print(f"\nλep对比 (前20个):")
print(f"  {'材料':15s} {'λep经验':>8s} {'λepHopf':>8s} {'差异':>8s}")
for d in data[:20]:
    ra = solve_tc(d['f'], 'empirical')
    rb = solve_tc(d['f'], 'hopfield')
    if ra and rb:
        diff = abs(ra['lambda_ep'] - rb['lambda_ep']) / ra['lambda_ep'] * 100
        print(f"  {d['f']:15s} {ra['lambda_ep']:8.3f} {rb['lambda_ep']:8.3f} {diff:7.1f}%")