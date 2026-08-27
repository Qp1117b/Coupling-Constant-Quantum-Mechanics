"""找出自洽性差异最大的材料并分析原因"""
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
A_LN2_SQ = LN2**2
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

def compute_all(formula):
    atoms = {}
    for el, cnt in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', formula):
        if el in ATOM_DB: atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    if not atoms: return None

    C, bi, couplings = build_Cmol(atoms)
    af = atom_features(atoms)
    ev = np.sort(np.linalg.eigvalsh(C))
    if len(ev) < 2: return None
    sg = max(ev[1] - ev[0], 0.05)
    m = np.mean(ev); aniso = np.std(ev / m if m > 0 else ev)

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

    c_aniso = GAMMA_D_GL2 / (2 * math.pi)
    c_o = B_THEORY**2 * 0.25 / (3 * 8 * LAM0_THEORY**2)
    nc = 4.00 + 0.50 * math.log(1/sg) + c_aniso * aniso + 13.0 * af['inv_mass'] + 0.05 * af['dp'] + c_o * af['o']
    ni = int(nc); frac = nc - ni
    if ni < 1: gn = RIEMANN_ZEROS[0]
    elif ni >= len(RIEMANN_ZEROS): gn = 2 * math.pi * nc / math.log(nc / (2 * math.pi)) if nc > 6 else RIEMANN_ZEROS[-1]
    else: gn = RIEMANN_ZEROS[ni-1] + frac * (RIEMANN_ZEROS[ni] - RIEMANN_ZEROS[ni-1])
    lambda_ep = B_THEORY / (A_THEORY - gn) if A_THEORY > gn else 0.3

    K0 = C_GAMMA * math.exp(AG_THEORY * gn)
    K_eff = K0 * max(G, 1e-6)**(-0.75) * theta_d**(1.125)

    suppress = math.exp(-15.0 * af['f']) * math.exp(-3.0 * af['d0'])

    Tc_free = math.sqrt(8 * dd0**2 * K_eff * theta_d / (9 * LN2)) * suppress

    arg = 9 * LN2 * theta_d / (32 * dd0**2 * K_eff)
    if arg > 0:
        x_eq17 = 1.0 / math.tanh(math.sqrt(arg))
        one_minus = 3 * BETA**2 * dd0**2 / (16 * DELTA_GAMMA * x_eq17) if x_eq17 > 1 else 0
        delta_v = (1 - one_minus) / BETA if 0 < one_minus < 1 else 1.0 / BETA
    else:
        delta_v = 1.0 / BETA
        one_minus = 0

    one_minus = max(1 - BETA * delta_v, 1e-10)

    # 近似arccoth
    x_approx = 3 * BETA**2 * dd0**2 / (16 * one_minus * DELTA_GAMMA)
    if x_approx > 1:
        Tc_approx = theta_d / (2 * math.atanh(1.0 / x_approx)) * suppress
    else:
        Tc_approx = -1  # 标记无效

    # 精确arccoth
    A_coeff = A_LN2_SQ
    B_coeff = 3 * BETA**2 * dd0**2 / (16 * one_minus)
    discriminant = (DELTA_GAMMA - A_coeff)**2 + 4 * A_coeff * B_coeff
    if discriminant >= 0:
        x_exact = (A_coeff - DELTA_GAMMA + math.sqrt(discriminant)) / (2 * A_coeff)
        if x_exact > 1:
            Tc_exact = theta_d / (2 * math.atanh(1.0 / x_exact)) * suppress
        else:
            Tc_exact = -1
    else:
        Tc_exact = -1

    return {
        'Tc_free': Tc_free, 'Tc_approx': Tc_approx, 'Tc_exact': Tc_exact,
        'dd0': dd0, 'K_eff': K_eff, 'theta_d': theta_d, 'gn': gn,
        'lambda_ep': lambda_ep, 'suppress': suppress,
        'one_minus': one_minus, 'x_approx': x_approx,
        'beta_dv': BETA * delta_v,
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
    r = compute_all(d['f'])
    if r is None: continue
    r['formula'] = d['f']; r['tc_exp'] = d['tc']; r['cat'] = d['cat']
    results.append(r)

# 分类: 有效vs无效
valid_approx = [r for r in results if r['Tc_approx'] > 0]
invalid_approx = [r for r in results if r['Tc_approx'] < 0]
valid_exact = [r for r in results if r['Tc_exact'] > 0]
invalid_exact = [r for r in results if r['Tc_exact'] < 0]

print(f"总样本: {len(results)}")
print(f"近似arccoth: 有效{len(valid_approx)}, 无效{len(invalid_approx)} (x≤1)")
print(f"精确arccoth: 有效{len(valid_exact)}, 无效{len(invalid_exact)} (x≤1)")

# 对有效样本计算差异
diffs_approx = []
for r in valid_approx:
    diff = abs(r['Tc_free'] - r['Tc_approx'])/r['Tc_free']
    diffs_approx.append((diff, r))

diffs_approx.sort(key=lambda x: x[0])

print(f"\n近似arccoth (仅有效样本, n={len(valid_approx)}):")
print(f"  中位差异: {diffs_approx[len(diffs_approx)//2][0]*100:.4f}%")
print(f"  90分位: {diffs_approx[int(len(diffs_approx)*0.9)][0]*100:.4f}%")
print(f"  最大差异: {diffs_approx[-1][0]*100:.4f}%")

# 差异最大的10个
print(f"\n差异最大的10个 (近似arccoth):")
print(f"  {'材料':15s} {'Tc自由能':>10s} {'Tc近似':>10s} {'差异':>8s} {'x_approx':>10s} {'1-βδv':>10s}")
for diff, r in diffs_approx[-10:]:
    print(f"  {r['formula']:15s} {r['Tc_free']:10.2f} {r['Tc_approx']:10.2f} {diff*100:7.2f}% {r['x_approx']:10.4f} {r['one_minus']:10.6f}")

# 无效样本
print(f"\n无效样本 (x≤1, 近似arccoth, n={len(invalid_approx)}):")
print(f"  {'材料':15s} {'Tc自由能':>10s} {'x_approx':>10s} {'1-βδv':>10s} {'βδv':>10s}")
for r in invalid_approx[:20]:
    print(f"  {r['formula']:15s} {r['Tc_free']:10.2f} {r['x_approx']:10.4f} {r['one_minus']:10.6f} {r['beta_dv']:10.6f}")

# 精确arccoth分析
diffs_exact = []
for r in valid_exact:
    diff = abs(r['Tc_free'] - r['Tc_exact'])/r['Tc_free']
    diffs_exact.append((diff, r))
diffs_exact.sort(key=lambda x: x[0])

print(f"\n精确arccoth (仅有效样本, n={len(valid_exact)}):")
print(f"  中位差异: {diffs_exact[len(diffs_exact)//2][0]*100:.4f}%")
print(f"  90分位: {diffs_exact[int(len(diffs_exact)*0.9)][0]*100:.4f}%")
print(f"  最大差异: {diffs_exact[-1][0]*100:.4f}%")

print(f"\n差异最大的10个 (精确arccoth):")
print(f"  {'材料':15s} {'Tc自由能':>10s} {'Tc精确':>10s} {'差异':>8s}")
for diff, r in diffs_exact[-10:]:
    print(f"  {r['formula']:15s} {r['Tc_free']:10.2f} {r['Tc_exact']:10.2f} {diff*100:7.2f}%")

# 核心问题: 近似arccoth对大多数材料差异0%, 但有少数发散
# 精确arccoth反而更差 — 为什么?
print(f"\n{'='*70}")
print("核心分析: 为什么精确解反而更差?")
print("="*70)
# 精确解引入了(ln2)²项, 但这个项的物理含义是什么?
# 方程8: λn(T) = γn + [coth(θD/2T)-1](lnn)² - ...
# (lnn)²项是"热涨落修正" — n=2时为(ln2)²
# 近似解忽略这项 → 对大多数材料OK(因为x>>1, 这项相对小)
# 精确解包含这项 → 但可能改变了x的值, 导致某些材料x<1

# 检查: 近似解和精确解的x值差异
print(f"\n近似x vs 精确x (前20个有效样本):")
print(f"  {'材料':15s} {'x_approx':>10s} {'x_exact':>10s} {'差异':>8s}")
for r in results[:30]:
    if r['Tc_approx'] > 0 and r['Tc_exact'] > 0:
        A_coeff = A_LN2_SQ
        B_coeff = 3 * BETA**2 * r['dd0']**2 / (16 * r['one_minus'])
        disc = (DELTA_GAMMA - A_coeff)**2 + 4 * A_coeff * B_coeff
        if disc >= 0:
            x_exact = (A_coeff - DELTA_GAMMA + math.sqrt(disc)) / (2 * A_coeff)
            x_diff = abs(r['x_approx'] - x_exact) / r['x_approx']
            print(f"  {r['formula']:15s} {r['x_approx']:10.4f} {x_exact:10.4f} {x_diff*100:7.2f}%")