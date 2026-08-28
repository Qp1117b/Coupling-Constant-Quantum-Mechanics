"""从Weyl群根向量归一化推导转换矩阵S

嘉当矩阵: C_ij = 2(α_i, α_j)/(α_j, α_j)
根向量含质量归一化: α_i → α_i · m_i^s
→ C_ij' = C_ij^0 · (m_i/m_j)^s  (非对称!)

物理哈密顿量需Hermitian:
  H_ij = C_ij^0 · [(m_i/m_j)^s + (m_j/m_i)^s] / 2
       = C_ij^0 · cosh(s·ln(m_i/m_j))

对角元不变: H_ii = C_ii = 2
非对角元: 轻重原子混合时增强

特例:
  s=0: H=C (原始)
  s=1/2: H_ij = C_ij · (m_i+m_j)/(2√(m_i·m_j))  (算术/几何平均)
  s=1: H_ij = C_ij · (m_i²+m_j²)/(2·m_i·m_j)

从CQM: s来自自旋-轨道耦合 A_spin ~ ℏ/(mc)·σ·(∇V)
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
AG_THEORY = 3.0 / (4 * math.pi * (1 - MU_THEORY))
GAMMA_D_GL2 = 2.196681962

RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832,
                 52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
                 67.079811, 69.526405, 72.067158, 75.704690, 77.144840]

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
LN2 = math.log(2)
C_GAMMA = 7.77e11
COEF_EQUATION8 = 3 * BETA**2 / 16

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

def build_Cmol_root_mass(atoms, s=0.0):
    """从根向量归一化推导的质量修正嘉当矩阵

    H_ij = C_ij^0 · cosh(s·ln(m_i/m_j))  (非对角)
    H_ii = C_ii = 2  (对角不变)

    s=0: 原始
    s=0.5: 算术/几何平均
    """
    els = list(atoms.keys()); blocks = []; bi = []
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        for l, occ, cap in valence_orbitals(z):
            if l == 0: blocks.append(A1.copy()); bi.append((el, 's', 1))
            elif l == 1: blocks.append(A3.copy()); bi.append((el, 'p', 3))
            elif l == 2: blocks.append(A4.copy()); bi.append((el, 'd', 4))
    if not blocks: return np.array([[2.0]]), bi
    size = sum(b.shape[0] for b in blocks); C = np.zeros((size, size)); idx = 0
    for b in blocks:
        s_sz = b.shape[0]; C[idx:idx+s_sz, idx:idx+s_sz] = b; idx += s_sz
    idx_i = 0
    for i, binfo in enumerate(bi):
        si = binfo[2]; idx_j = idx_i + si
        mi = ATOM_DB[binfo[0]][0]
        for j, bjinfo in enumerate(bi[i+1:], start=i+1):
            sj = bjinfo[2]; ri = ATOM_DB[binfo[0]][2]; rj = ATOM_DB[bjinfo[0]][2]
            mj = ATOM_DB[bjinfo[0]][0]
            t0 = 0.1 * math.exp(-(ri + rj) / 3.0)
            if (binfo[1] == 'd' and bjinfo[1] == 'p') or (binfo[1] == 'p' and bjinfo[1] == 'd'): t0 *= 1.5
            # 根向量质量归一化: cosh(s·ln(mi/mj))
            if s != 0 and mi != mj:
                mass_factor = math.cosh(s * math.log(mi / mj))
            else:
                mass_factor = 1.0
            t0 *= mass_factor
            for a in range(si):
                for b in range(sj): C[idx_i+a, idx_j+b] = t0; C[idx_j+b, idx_i+a] = t0
            idx_j += sj
        idx_i += si
    return C, bi

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

def solve_tc(formula, s=0.0, eq8_coef=1.5):
    atoms = {}
    for el, cnt in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', formula):
        if el in ATOM_DB: atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    if not atoms: return None
    C, bi = build_Cmol_root_mass(atoms, s=s)
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
    c_aniso = GAMMA_D_GL2 / (2 * math.pi)
    c_o = B_THEORY**2 * 0.25 / (3 * 8 * LAM0_THEORY**2)
    eq8_term = eq8_coef * COEF_EQUATION8 * dd0_sq
    nc = (4.00 + 0.50 * math.log(1/sg) + c_aniso * aniso
          + eq8_term + 0.05 * af['dp'] + c_o * af['o'])
    ni = int(nc); frac = nc - ni
    if ni < 1: gn = RIEMANN_ZEROS[0]
    elif ni >= len(RIEMANN_ZEROS): gn = 2 * math.pi * nc / math.log(nc / (2 * math.pi)) if nc > 6 else RIEMANN_ZEROS[-1]
    else: gn = RIEMANN_ZEROS[ni-1] + frac * (RIEMANN_ZEROS[ni] - RIEMANN_ZEROS[ni-1])
    K0 = C_GAMMA * math.exp(AG_THEORY * gn)
    K_eff = K0 * max(G, 1e-6)**(-0.75) * theta_d**(1.125)
    f_supp = BETA / math.sqrt(3)
    suppress = math.exp(-f_supp * af['f']) * math.exp(-3.0 * af['d0'])
    Tc = math.sqrt(8 * dd0**2 * K_eff * theta_d / (9 * LN2)) * suppress
    return Tc

data = []
with open(os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv'), 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc > 0: data.append({'f': row['材料(化学式)'], 'cat': row['类别'], 'tc': tc})

def sym_err(p, e):
    if p <= 0 or e <= 0: return float('inf')
    return max(p/e, e/p) - 1

def eval_full(s=0.0, eq8_coef=1.5, verbose=True):
    errs = []; cat_errs = {}
    for d in data:
        tc_pred = solve_tc(d['f'], s=s, eq8_coef=eq8_coef)
        if tc_pred is None or tc_pred <= 0: continue
        e = sym_err(tc_pred, d['tc'])
        errs.append(e)
        if d['cat'] not in cat_errs: cat_errs[d['cat']] = []
        cat_errs[d['cat']].append(e)
    errs.sort()
    w2 = sum(1 for e in errs if e <= 1.0) / len(errs) * 100
    w5 = sum(1 for e in errs if e <= 4.0) / len(errs) * 100
    if verbose:
        print(f"  n={len(errs)}, 中位{errs[len(errs)//2]*100:.1f}%, 2倍内{w2:.1f}%, 5倍内{w5:.1f}%")
        for cat in ['氢化物高压超导体', '元素超导体(常压)', '铜氧化物高温超导体', '有机超导体', '石墨插层超导体', 'A15结构金属间化合物']:
            if cat in cat_errs and len(cat_errs[cat]) >= 3:
                ce = sorted(cat_errs[cat])
                cw2 = sum(1 for e in ce if e <= 1.0) / len(ce) * 100
                print(f"    {cat:20s}: 2倍内{cw2:.0f}% 中位{ce[len(ce)//2]*100:.0f}%")
    return w2

print("="*70)
print("从Weyl群根向量归一化推导转换矩阵S")
print("H_ij = C_ij · cosh(s·ln(m_i/m_j))")
print("="*70)

# s扫描(eq8=1.5)
print("\ns扫描(eq8=1.5, 方程8+根向量质量):")
for s in [0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0]:
    print(f"s={s:.1f}:", end="")
    eval_full(s=s, eq8_coef=1.5, verbose=False)

# s扫描(eq8=0, 纯根向量质量)
print("\ns扫描(eq8=0, 纯根向量质量替代方程8):")
for s in [0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0]:
    print(f"s={s:.1f}:", end="")
    eval_full(s=s, eq8_coef=0, verbose=False)

# (s, eq8)联合扫描
print("\n(s, eq8)联合扫描:")
best_w2 = 0; best = (0, 0)
for s in [0, 0.1, 0.2, 0.3, 0.5]:
    for eq8 in [0, 0.5, 1.0, 1.5, 2.0]:
        w2 = eval_full(s=s, eq8_coef=eq8, verbose=False)
        if w2 > best_w2:
            best_w2 = w2; best = (s, eq8)
            print(f"  s={s:.1f}, eq8={eq8:.1f}: 2倍内{w2:.1f}% ★")

print(f"\n最佳: s={best[0]:.1f}, eq8={best[1]:.1f}, 2倍内{best_w2:.1f}%")
print(f"\n详细:")
eval_full(s=best[0], eq8_coef=best[1], verbose=True)

# 物理分析
print(f"\n{'='*70}")
print("物理分析: cosh(s·ln(mi/mj))对不同原子对的效应")
print("="*70)
pairs = [('H','La'), ('H','S'), ('H','C'), ('C','Rb'), ('C','Pb'), ('Nb','Sn'), ('O','Cu'), ('Fe','Se')]
s_best = best[0]
for el1, el2 in pairs:
    m1 = ATOM_DB[el1][0]; m2 = ATOM_DB[el2][0]
    factor = math.cosh(s_best * math.log(m1/m2)) if m1 != m2 else 1.0
    print(f"  {el1}-{el2} (m={m1:.0f}/{m2:.0f}): cosh({s_best}·ln({m1/m2:.2f})) = {factor:.3f}")