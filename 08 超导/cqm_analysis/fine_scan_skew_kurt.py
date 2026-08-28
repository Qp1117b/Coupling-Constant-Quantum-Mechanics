"""精细扫描偏度/峰度系数，验证c_skew=c_kurt=t0_base=0.1假设

物理推导:
  嘉当矩阵 = 能动张量
  耦合常数 t0 = 0.1·exp(-(ri+rj)/3) 出现在嘉当矩阵构造中
  能动张量的高阶矩(偏度/峰度)也应以同一t0耦合进入n_c
  因此 c_skew = c_kurt = t0_base = 0.1
"""
import sys, os, csv, re, math
import numpy as np

sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework')
from atom_db import ATOM_DB

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
C2 = 2.0/3.0; LN2 = math.log(2)
BETA = 8 * math.pi + 1
AG_THEORY = 3.0 / (4 * math.pi * (1 - 1.0/(2*math.sqrt(2))))
C_GAMMA = 7.77e11
COEF_EQUATION8 = 3 * BETA**2 / 16
GAMMA_D_GL2 = 2.196681962
C_ANISO = GAMMA_D_GL2 / (2 * math.pi)
B_THEORY = 8 * math.pi / 3
LAM0_THEORY = 1.0 / math.e
C_O = B_THEORY**2 * 0.25 / (3 * 8 * LAM0_THEORY**2)
C_F_SUPP = BETA / math.sqrt(3)
T0_BASE = 0.1  # 嘉当矩阵耦合常数基底

RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832,
                 52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
                 67.079811, 69.526405, 72.067158, 75.704690, 77.144840]

ATOMIC_NUMBERS = {}
for i, el in enumerate(['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar',
             'K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr',
             'Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe',
             'Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu',
             'Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi'], 1):
    ATOMIC_NUMBERS[el] = i
for _el, _z in [('Th',90),('Pa',91),('U',92),('Np',93),('Pu',94),('Am',95),('Cm',96)]:
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

def build_Cmol(atoms, s_root=0.5):
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
            t0 = T0_BASE * math.exp(-(ri + rj) / 3.0)
            if (binfo[1] == 'd' and bjinfo[1] == 'p') or (binfo[1] == 'p' and bjinfo[1] == 'd'): t0 *= 1.5
            if s_root != 0 and mi != mj:
                t0 *= math.cosh(s_root * math.log(mi / mj))
            for a in range(si):
                for b in range(sj): C[idx_i+a, idx_j+b] = t0; C[idx_j+b, idx_i+a] = t0
            idx_j += sj
        idx_i += si
    return C, bi

def interpolate_gamma_n(n):
    n_int = int(n); frac = n - n_int
    if n_int < 1: return RIEMANN_ZEROS[0]
    if n_int >= len(RIEMANN_ZEROS):
        return 2 * math.pi * n / math.log(n / (2 * math.pi)) if n > 6 else RIEMANN_ZEROS[-1]
    g_low = RIEMANN_ZEROS[n_int - 1]
    g_high = RIEMANN_ZEROS[n_int] if n_int < len(RIEMANN_ZEROS) else RIEMANN_ZEROS[-1]
    return g_low + frac * (g_high - g_low)

def sym_err(p, e):
    if p <= 0 or e <= 0: return float('inf')
    return max(p/e, e/p) - 1

def parse_formula(f):
    atoms = {}
    for el, cnt in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f):
        if el in ATOM_DB: atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    return atoms

def compute_features(atoms):
    els = list(atoms.keys()); n_atoms = sum(atoms.values())
    dp = 0; d0 = 0; f_count = 0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50); vo = valence_orbitals(z)
        hd = hp = False
        for l, occ, cap in vo:
            if l == 2: hd = True
            if l == 1: hp = True
            if l == 2 and occ == 0: d0 += atoms[el]
        if hd and hp: dp += atoms[el]
        config = madelung_config(z)
        for (n, l), occ in config.items():
            if l == 3 and 0 < occ < 14: f_count += atoms[el]; break
    return dp/n_atoms, d0/n_atoms, f_count/n_atoms, atoms.get('O',0)/n_atoms

def solve_tc_full(formula, c_skew=0.0, c_kurt=0.0):
    atoms = parse_formula(formula)
    if not atoms: return None
    C, bi = build_Cmol(atoms)
    els = list(atoms.keys()); n_atoms = sum(atoms.values())
    ev = np.sort(np.linalg.eigvalsh(C))
    if len(ev) < 2: return None
    sg = max(ev[1] - ev[0], 0.05)
    m_ev = np.mean(ev); ev_std = np.std(ev)
    aniso = np.std(ev / m_ev if m_ev > 0 else ev)
    skew = np.mean(((ev - m_ev) / ev_std) ** 3) if ev_std > 0 else 0
    kurt = np.mean(((ev - m_ev) / ev_std) ** 4) - 3 if ev_std > 0 else 0

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
    eq8_term = 1.5 * COEF_EQUATION8 * dd0_sq
    dp, d0, f_frac, o_frac = compute_features(atoms)

    nc = (4.00 + 0.50 * math.log(1/sg) + C_ANISO * aniso
          + eq8_term + 0.05 * dp + C_O * o_frac
          + c_skew * skew + c_kurt * kurt)
    gn = interpolate_gamma_n(nc)
    K0 = C_GAMMA * math.exp(AG_THEORY * gn)
    K_eff = K0 * max(G, 1e-6)**(-0.75) * theta_d**(1.125)
    suppress = math.exp(-C_F_SUPP * f_frac) * math.exp(-3.0 * d0)
    Tc = math.sqrt(8 * dd0**2 * K_eff * theta_d / (9 * LN2)) * suppress
    return Tc

data = []
with open(os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv'), 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc > 0: data.append({'f': row['材料(化学式)'], 'cat': row['类别'], 'tc': tc})

def eval_full(c_skew=0.0, c_kurt=0.0, label=""):
    errs = []
    for d in data:
        tc_pred = solve_tc_full(d['f'], c_skew=c_skew, c_kurt=c_kurt)
        if tc_pred is None or tc_pred <= 0: continue
        e = sym_err(tc_pred, d['tc'])
        errs.append(e)
    if not errs: return 0
    errs.sort()
    w2 = sum(1 for e in errs if e <= 1.0) / len(errs) * 100
    print(f"{label:55s}: n={len(errs):3d}, 2倍内{w2:.1f}%, 中位{errs[len(errs)//2]*100:.1f}%")
    return w2

print("="*80)
print("精细扫描偏度/峰度系数")
print(f"假设: c_skew = c_kurt = t0_base = {T0_BASE}")
print("="*80)

print("\n--- 基线 ---")
eval_full(label="基线(无高阶分量)")

print("\n--- 精细网格扫描 (0.05~0.20) ---")
best_w2 = 0; best = (0, 0)
for cs in np.arange(0.0, 0.21, 0.05):
    for ck in np.arange(0.0, 0.21, 0.05):
        w2 = eval_full(c_skew=round(cs,2), c_kurt=round(ck,2),
                       label=f"偏度={cs:.2f}, 峰度={ck:.2f}")
        if w2 > best_w2:
            best_w2 = w2; best = (round(cs,2), round(ck,2))

print(f"\n精细最佳: 偏度={best[0]:.2f}, 峰度={best[1]:.2f}, 2倍内{best_w2:.1f}%")

print("\n--- 验证t0_base假设: c_skew=c_kurt=t0_base ---")
eval_full(c_skew=T0_BASE, c_kurt=T0_BASE, label=f"c_skew=c_kurt=t0_base={T0_BASE}")

print("\n--- 对比: 不同t0_base值时的最优c_skew/c_kurt ---")
# 如果t0_base改变，最优c_skew/c_kurt是否也跟着变？
# 这需要修改build_Cmol中的T0_BASE，但这里我们只验证系数关系
# 用数学关系验证: c = t0_base = 0.1
for t0 in [0.05, 0.08, 0.10, 0.12, 0.15]:
    eval_full(c_skew=t0, c_kurt=t0, label=f"c_skew=c_kurt={t0:.2f}")

print("\n--- 偏度/峰度单独贡献分析 ---")
# 偏度贡献: c_skew * skew, 峰度贡献: c_kurt * kurt
# 统计这些贡献的典型大小
contribs_skew = []; contribs_kurt = []
for d in data:
    atoms = parse_formula(d['f'])
    if not atoms: continue
    C, bi = build_Cmol(atoms)
    ev = np.sort(np.linalg.eigvalsh(C))
    if len(ev) < 2: continue
    m_ev = np.mean(ev); ev_std = np.std(ev)
    if ev_std <= 0: continue
    skew = np.mean(((ev - m_ev) / ev_std) ** 3)
    kurt = np.mean(((ev - m_ev) / ev_std) ** 4) - 3
    contribs_skew.append(T0_BASE * skew)
    contribs_kurt.append(T0_BASE * kurt)

print(f"偏度贡献({T0_BASE}*skew): 均值={np.mean(contribs_skew):.4f}, std={np.std(contribs_skew):.4f}")
print(f"峰度贡献({T0_BASE}*kurt): 均值={np.mean(contribs_kurt):.4f}, std={np.std(contribs_kurt):.4f}")
print(f"对比: aniso贡献均值≈{C_ANISO*0.1:.4f}, eq8贡献均值≈{1.5*COEF_EQUATION8*1e-4:.4f}")