"""诊断方程组自洽性问题

两条路径:
  路径1 (方程11+14): 自由能公式 Tc² = 8·Δδ₀²·K_eff·θD/(9·ln2)
  路径2 (方程8+9+10): arccoth闭式 — 从本征值交叉直接求解

问题: 路径2用了近似(忽略(ln2)²项), 导致22.8%差异

精确推导:
  从λ₂(Tc) = λ₁(Tc):
    Δγ + (x-1)·(ln2)² = 3β²Δδ₀²/(16x·(1-βδv))
  其中 x = coth(θD/2Tc)

  令 A=(ln2)², B=3β²Δδ₀²/(16(1-βδv)):
    A·x² + (Δγ-A)·x - B = 0
    x = [(A-Δγ) + √((Δγ-A)² + 4AB)] / (2A)

  精确Tc = θD/(2·arccoth(x))

  近似(忽略A): x ≈ B/Δγ → 之前的arccoth闭式
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
A_LN2_SQ = LN2**2  # (ln2)² ≈ 0.4805
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

    # 路径1: 自由能公式 (方程11+14)
    Tc_free = math.sqrt(8 * dd0**2 * K_eff * theta_d / (9 * LN2)) * suppress

    # 路径2a: 近似arccoth闭式 (忽略(ln2)²项)
    # 从方程17计算δ_v
    arg = 9 * LN2 * theta_d / (32 * dd0**2 * K_eff)
    if arg > 0:
        x_eq17 = 1.0 / math.tanh(math.sqrt(arg))
        one_minus_approx = 3 * BETA**2 * dd0**2 / (16 * DELTA_GAMMA * x_eq17) if x_eq17 > 1 else 0
        delta_v_approx = (1 - one_minus_approx) / BETA if 0 < one_minus_approx < 1 else 1.0 / BETA
    else:
        delta_v_approx = 1.0 / BETA
        one_minus_approx = 0

    one_minus_approx = max(1 - BETA * delta_v_approx, 1e-10)
    x_approx = 3 * BETA**2 * dd0**2 / (16 * one_minus_approx * DELTA_GAMMA)
    Tc_approx = theta_d / (2 * math.atanh(1.0 / x_approx)) * suppress if x_approx > 1 else 0

    # 路径2b: 精确闭式解 (包含(ln2)²项)
    # A·x² + (Δγ-A)·x - B = 0
    # x = [(A-Δγ) + √((Δγ-A)² + 4AB)] / (2A)
    A_coeff = A_LN2_SQ
    B_coeff = 3 * BETA**2 * dd0**2 / (16 * one_minus_approx)
    discriminant = (DELTA_GAMMA - A_coeff)**2 + 4 * A_coeff * B_coeff
    if discriminant >= 0:
        x_exact = (A_coeff - DELTA_GAMMA + math.sqrt(discriminant)) / (2 * A_coeff)
        Tc_exact = theta_d / (2 * math.atanh(1.0 / x_exact)) * suppress if x_exact > 1 else 0
    else:
        Tc_exact = 0

    # 路径2c: 精确闭式解 + 精确δ_v (从精确Tc反推δ_v)
    # 如果Tc_free是正确的, 那么从精确闭式解可以反推1-βδv
    # A·x² + (Δγ-A)·x - B = 0, B = 3β²Δδ₀²/(16(1-βδv))
    # 给定Tc → x = coth(θD/2Tc) → B = A·x² + (Δγ-A)·x → 1-βδv = 3β²Δδ₀²/(16B)
    if Tc_free > 0:
        y_free = theta_d / (2 * Tc_free / suppress)  # 注意suppress
        x_from_free = 1.0 / math.tanh(y_free) if y_free > 0 else 1
        B_from_free = A_coeff * x_from_free**2 + (DELTA_GAMMA - A_coeff) * x_from_free
        one_minus_from_free = 3 * BETA**2 * dd0**2 / (16 * B_from_free) if B_from_free > 0 else 0
        delta_v_from_free = (1 - one_minus_from_free) / BETA if 0 < one_minus_from_free < 1 else 1.0 / BETA
    else:
        delta_v_from_free = 1.0 / BETA
        one_minus_from_free = 0

    return {
        'Tc_free': Tc_free, 'Tc_approx': Tc_approx, 'Tc_exact': Tc_exact,
        'dd0': dd0, 'K_eff': K_eff, 'theta_d': theta_d, 'gn': gn,
        'lambda_ep': lambda_ep, 'suppress': suppress,
        'delta_v_approx': delta_v_approx, 'delta_v_from_free': delta_v_from_free,
        'one_minus_approx': one_minus_approx,
        'one_minus_from_free': one_minus_from_free,
        'beta_dv_approx': BETA * delta_v_approx,
        'beta_dv_from_free': BETA * delta_v_from_free,
    }

# ========== 主程序 ==========
print("="*70)
print("诊断方程组自洽性")
print("="*70)
print(f"\n(ln2)² = {A_LN2_SQ:.6f}")
print(f"Δγ = γ₂-γ₁ = {DELTA_GAMMA:.6f}")
print(f"(ln2)²/Δγ = {A_LN2_SQ/DELTA_GAMMA:.4f} → {'不可忽略!' if A_LN2_SQ/DELTA_GAMMA > 0.05 else '可忽略'}")

# 加载数据
data = []
with open(os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv'), 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc > 0: data.append({'f': row['材料(化学式)'], 'cat': row['类别'], 'tc': tc})

print(f"\n样本数: {len(data)}")

# 诊断三种路径
results = []
for d in data:
    r = compute_all(d['f'])
    if r is None: continue
    r['formula'] = d['f']; r['tc_exp'] = d['tc']; r['cat'] = d['cat']
    results.append(r)

print(f"\n有效结果: {len(results)}")

# 比较三种路径
diff_approx = [abs(r['Tc_free'] - r['Tc_approx'])/r['Tc_free'] for r in results if r['Tc_approx'] > 0]
diff_exact = [abs(r['Tc_free'] - r['Tc_exact'])/r['Tc_free'] for r in results if r['Tc_exact'] > 0]

diff_approx.sort(); diff_exact.sort()
print(f"\n路径1(自由能) vs 路径2a(近似arccoth, 忽略(ln2)²):")
print(f"  最大差异: {max(diff_approx)*100:.2f}%")
print(f"  中位差异: {diff_approx[len(diff_approx)//2]*100:.2f}%")
print(f"  90分位: {diff_approx[int(len(diff_approx)*0.9)]*100:.2f}%")

print(f"\n路径1(自由能) vs 路径2b(精确arccoth, 包含(ln2)²):")
print(f"  最大差异: {max(diff_exact)*100:.2f}%")
print(f"  中位差异: {diff_exact[len(diff_exact)//2]*100:.2f}%")
print(f"  90分位: {diff_exact[int(len(diff_exact)*0.9)]*100:.2f}%")

# 分析δ_v
print(f"\nδ_v分析:")
beta_dv_approx = [r['beta_dv_approx'] for r in results]
beta_dv_from_free = [r['beta_dv_from_free'] for r in results]
beta_dv_approx.sort(); beta_dv_from_free.sort()
print(f"  βδ_v(近似): 中位={beta_dv_approx[len(beta_dv_approx)//2]:.6f}, 范围=[{beta_dv_approx[0]:.6f}, {beta_dv_approx[-1]:.6f}]")
print(f"  βδ_v(从自由能反推): 中位={beta_dv_from_free[len(beta_dv_from_free)//2]:.6f}, 范围=[{beta_dv_from_free[0]:.6f}, {beta_dv_from_free[-1]:.6f}]")

# 关键问题: δ_v从方程17(近似) vs δ_v从自由能反推
print(f"\n关键: δ_v从方程17(近似) vs δ_v从自由能公式反推")
dv_diff = [abs(r['delta_v_approx'] - r['delta_v_from_free'])/max(r['delta_v_approx'], 1e-10) for r in results]
dv_diff.sort()
print(f"  δ_v相对差异: 中位={dv_diff[len(dv_diff)//2]*100:.2f}%, 最大={max(dv_diff)*100:.2f}%")

# 展示几个具体例子
print(f"\n具体例子 (前10个):")
print(f"  {'材料':15s} {'Tc自由能':>10s} {'Tc近似':>10s} {'Tc精确':>10s} {'差异近似':>8s} {'差异精确':>8s} {'βδv近似':>10s} {'βδv反推':>10s}")
for r in results[:10]:
    da = abs(r['Tc_free'] - r['Tc_approx'])/r['Tc_free']*100 if r['Tc_approx'] > 0 else -1
    de = abs(r['Tc_free'] - r['Tc_exact'])/r['Tc_free']*100 if r['Tc_exact'] > 0 else -1
    print(f"  {r['formula']:15s} {r['Tc_free']:10.2f} {r['Tc_approx']:10.2f} {r['Tc_exact']:10.2f} {da:7.2f}% {de:7.2f}% {r['beta_dv_approx']:10.6f} {r['beta_dv_from_free']:10.6f}")

# 结论
print(f"\n{'='*70}")
print("结论")
print("="*70)
if max(diff_exact) < 0.01:
    print("精确闭式解与自由能公式完全一致 → 方程组自洽!")
    print("问题根源: 近似arccoth闭式忽略了(ln2)²项")
    print("修复: 用精确闭式解替换近似arccoth闭式")
elif max(diff_exact) < max(diff_approx) * 0.1:
    print(f"精确闭式解显著改善: 差异从{max(diff_approx)*100:.2f}%降至{max(diff_exact)*100:.2f}%")
    print("但仍有残差, 可能需要进一步修正δ_v等价关系")
else:
    print(f"精确闭式解未显著改善: {max(diff_exact)*100:.2f}% vs {max(diff_approx)*100:.2f}%")
    print("问题可能在于δ_v等价关系本身, 或自由能公式需要修正")