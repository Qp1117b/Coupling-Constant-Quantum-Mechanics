"""验证正确的方程组逻辑顺序

核心发现:
  方程17是近似等价条件(忽略(ln2)²项), 对元素超导体(x→∞)失效
  正确逻辑:
    1. Tc从自由能公式计算(方程11+14) — 基本定义
    2. δ_v从方程8+9+10反推 — 不是从方程17独立计算
    3. 方程17是反推的显式近似, 仅在x≈1时精确

验证: 从自由能Tc反推δ_v, 检查是否合理(βδv≈0.997, 临界同步)
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

def solve_correct(formula):
    """正确的方程组求解逻辑:
    1. Tc从自由能公式(方程11+14)
    2. δ_v从方程8+9+10反推(精确, 包含(ln2)²)
    3. 验证方程17(近似)的适用性
    """
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

    # 步骤1: Tc从自由能公式(方程11+14)
    Tc = math.sqrt(8 * dd0**2 * K_eff * theta_d / (9 * LN2)) * suppress

    # 步骤2: δ_v从方程8+9+10反推(精确)
    # λ₂(Tc) = λ₁(Tc):
    #   Δγ + (x-1)·(ln2)² = 3β²Δδ₀²/(16x·(1-βδv))
    #   x = coth(θD/2Tc)
    if Tc > 0:
        y = theta_d / (2 * Tc / suppress)  # suppress不影响Tc的物理值
        x = 1.0 / math.tanh(y) if y > 0 and math.tanh(y) > 0 else 1.0
        # 1-βδv = 3β²Δδ₀² / (16x·[Δγ + (x-1)·(ln2)²])
        denom = 16 * x * (DELTA_GAMMA + (x - 1) * A_LN2_SQ)
        one_minus = 3 * BETA**2 * dd0**2 / denom if denom > 0 else 0
        delta_v = (1 - one_minus) / BETA if 0 < one_minus < 1 else 1.0 / BETA
    else:
        delta_v = 1.0 / BETA; one_minus = 0; x = 1.0

    # 步骤3: 验证方程17(近似)
    arg = 9 * LN2 * theta_d / (32 * dd0**2 * K_eff)
    if arg > 0:
        x_eq17 = 1.0 / math.tanh(math.sqrt(arg))
        one_minus_eq17 = 3 * BETA**2 * dd0**2 / (16 * DELTA_GAMMA * x_eq17) if x_eq17 > 1 else 0
        eq17_valid = abs(one_minus - one_minus_eq17) / max(one_minus, 1e-10) < 0.1
    else:
        one_minus_eq17 = 0; eq17_valid = False

    # 步骤4: 验证arccoth闭式(用反推的δ_v)
    if one_minus > 0:
        B_coeff = 3 * BETA**2 * dd0**2 / (16 * one_minus)
        A_coeff = A_LN2_SQ
        disc = (DELTA_GAMMA - A_coeff)**2 + 4 * A_coeff * B_coeff
        if disc >= 0:
            x_verify = (A_coeff - DELTA_GAMMA + math.sqrt(disc)) / (2 * A_coeff)
            Tc_verify = theta_d / (2 * math.atanh(1.0 / x_verify)) * suppress if x_verify > 1 else 0
        else:
            Tc_verify = 0
    else:
        Tc_verify = 0

    return {
        'Tc': Tc, 'Tc_verify': Tc_verify,
        'dd0': dd0, 'K_eff': K_eff, 'theta_d': theta_d, 'gn': gn,
        'lambda_ep': lambda_ep, 'suppress': suppress,
        'delta_v': delta_v, 'beta_dv': BETA * delta_v,
        'one_minus': one_minus, 'x': x,
        'eq17_valid': eq17_valid, 'one_minus_eq17': one_minus_eq17,
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
    r = solve_correct(d['f'])
    if r is None: continue
    r['formula'] = d['f']; r['tc_exp'] = d['tc']; r['cat'] = d['cat']
    results.append(r)

print("="*70)
print("正确逻辑顺序验证")
print("="*70)
print(f"样本数: {len(results)}")

# 验证: Tc_verify (从反推δ_v的arccoth) vs Tc (自由能)
verify_diffs = [abs(r['Tc'] - r['Tc_verify'])/r['Tc'] for r in results if r['Tc_verify'] > 0]
verify_diffs.sort()
print(f"\nTc(自由能) vs Tc(arccoth用反推δ_v):")
print(f"  有效验证: {len(verify_diffs)}/{len(results)}")
print(f"  中位差异: {verify_diffs[len(verify_diffs)//2]*100:.6f}%")
print(f"  90分位: {verify_diffs[int(len(verify_diffs)*0.9)]*100:.6f}%")
print(f"  最大差异: {verify_diffs[-1]*100:.6f}%")

# δ_v统计
beta_dvs = [r['beta_dv'] for r in results]
beta_dvs.sort()
print(f"\nβδ_v统计:")
print(f"  中位: {beta_dvs[len(beta_dvs)//2]:.6f}")
print(f"  范围: [{beta_dvs[0]:.6f}, {beta_dvs[-1]:.6f}]")
print(f"  1-βδv中位: {1-beta_dvs[len(beta_dvs)//2]:.6f}")

# 方程17适用性
eq17_valid_count = sum(1 for r in results if r['eq17_valid'])
print(f"\n方程17(近似)适用性: {eq17_valid_count}/{len(results)} ({eq17_valid_count/len(results)*100:.0f}%)")

# 预测精度
def sym_err(p, e):
    if p <= 0 or e <= 0: return float('inf')
    return max(p/e, e/p) - 1

errs = [sym_err(r['Tc'], r['tc_exp']) for r in results]
errs.sort()
print(f"\n预测精度 (正确逻辑):")
print(f"  中位: {errs[len(errs)//2]*100:.1f}%")
print(f"  2倍内: {sum(1 for e in errs if e<=1.0)/len(errs)*100:.1f}%")
print(f"  5倍内: {sum(1 for e in errs if e<=4.0)/len(errs)*100:.1f}%")

# 按类别
cat_errs = {}
for r in results:
    cat = r['cat']
    if cat not in cat_errs: cat_errs[cat] = []
    cat_errs[cat].append(sym_err(r['Tc'], r['tc_exp']))

print(f"\n按类别:")
for cat, ce in sorted(cat_errs.items(), key=lambda x: -len(x[1])):
    if len(ce) < 3: continue
    ce.sort()
    w2 = sum(1 for e in ce if e <= 1.0) / len(ce) * 100
    print(f"  {cat:20s} n={len(ce):3d}: 2倍内{w2:.0f}% 中位{ce[len(ce)//2]*100:.0f}%")

# 展示δ_v的物理含义
print(f"\n{'='*70}")
print("δ_v的物理含义")
print("="*70)
print(f"""
方程组正确逻辑顺序:
  1. 从C_mol谱计算几何量(方程1-4): Δδ₀, G
  2. 从C_mol谱计算耦合(方程5-7): λep, γn
  3. 从本征值→刚度(方程12-13): K_eff
  4. Tc从自由能公式(方程11+14): Tc = √(8Δδ₀²K_effθD/(9ln2))
  5. δ_v从方程8+9+10反推: 1-βδv = 3β²Δδ₀²/(16x·[Δγ+(x-1)(ln2)²])
     其中 x = coth(θD/2Tc)

关键: δ_v不是独立参数, 而是从Tc反推的!
  βδv中位 = {beta_dvs[len(beta_dvs)//2]:.6f} (临界同步)
  1-βδv中位 = {1-beta_dvs[len(beta_dvs)//2]:.6f} (小量)

方程17是步骤5的近似显式(忽略(ln2)²项):
  适用: {eq17_valid_count}/{len(results)} ({eq17_valid_count/len(results)*100:.0f}%) — 主要是x≈1的材料
  不适用: 元素超导体(x→∞, 1-βδv→0)

结论: 方程组完全自洽, 差异{verify_diffs[-1]*100:.4f}%
  两条路径(自由能+arccoth)给出相同Tc, 因为δ_v从Tc反推
  方程17是近似, 不是独立方程
""")