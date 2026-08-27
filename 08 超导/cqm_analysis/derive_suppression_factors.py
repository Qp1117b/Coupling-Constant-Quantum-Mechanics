"""从第一性推导抑制因子系数

当前: suppress = exp(-15·f_frac) · exp(-3·d0_frac)
f_frac = f电子原子比例, d0_frac = d^0空轨道原子比例

物理推导:
  f电子抑制系数15:
    - β = 8π+1 ≈ 26.13 (A4群论)
    - β/√3 ≈ 15.08 ≈ 15 (√3来自3D空间f电子局域化)
    - 物理含义: f电子在3D空间局域化, 角亏屏蔽因子 = β/√3

  d0抑制系数3:
    - l_d = 2 (d轨道角动量)
    - l_d + 1 = 3 (d0构型: d轨道全空, 角动量+1的量子修正)
    - 或: A4矩阵维度4, 减1 = 3 (去除平凡自由度)

验证: 从材料数据拟合最优系数, 与理论值对比
"""
import math, csv, os, re, sys
import numpy as np
from scipy.optimize import minimize

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

def compute_base_tc(formula):
    """计算不含抑制因子的Tc"""
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

    c_aniso = GAMMA_D_GL2 / (2 * math.pi)
    c_o = B_THEORY**2 * 0.25 / (3 * 8 * LAM0_THEORY**2)
    nc = 4.00 + 0.50 * math.log(1/sg) + c_aniso * aniso + 13.0 * af['inv_mass'] + 0.05 * af['dp'] + c_o * af['o']
    ni = int(nc); frac = nc - ni
    if ni < 1: gn = RIEMANN_ZEROS[0]
    elif ni >= len(RIEMANN_ZEROS): gn = 2 * math.pi * nc / math.log(nc / (2 * math.pi)) if nc > 6 else RIEMANN_ZEROS[-1]
    else: gn = RIEMANN_ZEROS[ni-1] + frac * (RIEMANN_ZEROS[ni] - RIEMANN_ZEROS[ni-1])

    K0 = C_GAMMA * math.exp(AG_THEORY * gn)
    K_eff = K0 * max(G, 1e-6)**(-0.75) * theta_d**(1.125)
    Tc_base = math.sqrt(8 * dd0**2 * K_eff * theta_d / (9 * LN2))

    return {'Tc_base': Tc_base, 'f': af['f'], 'd0': af['d0']}

# 主程序
data = []
with open(os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv'), 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc > 0: data.append({'f': row['材料(化学式)'], 'cat': row['类别'], 'tc': tc})

# 计算所有材料的base Tc
samples = []
for d in data:
    r = compute_base_tc(d['f'])
    if r is None or r['Tc_base'] <= 0: continue
    r['formula'] = d['f']; r['cat'] = d['cat']; r['tc_exp'] = d['tc']
    samples.append(r)

print("="*70)
print("抑制因子系数第一性推导")
print("="*70)

# 理论值
f_theory = BETA / math.sqrt(3)  # β/√3
d0_theory_1 = 3  # l_d + 1
d0_theory_2 = B_THEORY / math.pi  # B/π ≈ 2.67

print(f"\n理论推导:")
print(f"  f电子抑制系数:")
print(f"    β/√3 = {f_theory:.4f} (√3来自3D空间f电子局域化)")
print(f"    5π = {5*math.pi:.4f}")
print(f"    3π+5 = {3*math.pi+5:.4f}")
print(f"  d0抑制系数:")
print(f"    l_d+1 = {d0_theory_1} (d轨道角动量l=2, +1量子修正)")
print(f"    B/π = {d0_theory_2:.4f} (3D态密度/π)")
print(f"    2l_d-1 = {2*2-1} (d轨道角动量关系)")

# 从数据拟合最优系数
# Tc = Tc_base · exp(-α_f · f) · exp(-α_d0 · d0)
# log(Tc_exp/Tc_base) = -α_f · f - α_d0 · d0
# 线性回归!

y = np.array([math.log(s['tc_exp'] / s['Tc_base']) for s in samples])
X_f = np.array([s['f'] for s in samples])
X_d0 = np.array([s['d0'] for s in samples])

# 只用有f电子或d0的材料来拟合
has_f = [i for i, s in enumerate(samples) if s['f'] > 0]
has_d0 = [i for i, s in enumerate(samples) if s['d0'] > 0]
has_both = [i for i, s in enumerate(samples) if s['f'] > 0 or s['d0'] > 0]

print(f"\n数据统计:")
print(f"  有f电子的材料: {len(has_f)}")
print(f"  有d0的材料: {len(has_d0)}")
print(f"  有f或d0的材料: {len(has_both)}")

# 多变量回归: y = a + b·f + c·d0
X = np.column_stack([np.ones(len(samples)), X_f, X_d0])
beta_fit, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
pred = X @ beta_fit
r2 = 1 - np.var(y - pred) / np.var(y)

print(f"\n全数据回归: log(Tc_exp/Tc_base) = a + b·f + c·d0")
print(f"  a = {beta_fit[0]:.4f} (应为0)")
print(f"  b = {beta_fit[1]:.4f} (f电子抑制系数, 理论{f_theory:.4f})")
print(f"  c = {beta_fit[2]:.4f} (d0抑制系数, 理论{d0_theory_1})")
print(f"  R² = {r2:.3f}")

# 只用有f或d0的材料
if has_both:
    y_sub = y[has_both]
    X_sub = np.column_stack([np.ones(len(has_both)), X_f[has_both], X_d0[has_both]])
    beta_sub, _, _, _ = np.linalg.lstsq(X_sub, y_sub, rcond=None)
    pred_sub = X_sub @ beta_sub
    r2_sub = 1 - np.var(y_sub - pred_sub) / np.var(y_sub) if np.var(y_sub) > 0 else 0

    print(f"\n有f或d0材料回归 (n={len(has_both)}):")
    print(f"  a = {beta_sub[0]:.4f}")
    print(f"  b = {beta_sub[1]:.4f} (f电子抑制系数)")
    print(f"  c = {beta_sub[2]:.4f} (d0抑制系数)")
    print(f"  R² = {r2_sub:.3f}")

# 分别拟合f和d0
if has_f:
    y_f = y[has_f]
    X_f_only = np.column_stack([np.ones(len(has_f)), X_f[has_f]])
    beta_f, _, _, _ = np.linalg.lstsq(X_f_only, y_f, rcond=None)
    print(f"\n仅f电子材料 (n={len(has_f)}):")
    print(f"  f电子抑制系数 = {-beta_f[1]:.4f} (理论β/√3={f_theory:.4f}, 差异{abs(-beta_f[1]-f_theory)/f_theory*100:.1f}%)")

if has_d0:
    y_d0 = y[has_d0]
    X_d0_only = np.column_stack([np.ones(len(has_d0)), X_d0[has_d0]])
    beta_d0, _, _, _ = np.linalg.lstsq(X_d0_only, y_d0, rcond=None)
    print(f"\n仅d0材料 (n={len(has_d0)}):")
    print(f"  d0抑制系数 = {-beta_d0[1]:.4f} (理论l_d+1={d0_theory_1}, 差异{abs(-beta_d0[1]-d0_theory_1)/d0_theory_1*100:.1f}%)")

# 验证: 用理论系数vs拟合系数的预测精度
def eval_precision(alpha_f, alpha_d0):
    errs = []
    for s in samples:
        tc_pred = s['Tc_base'] * math.exp(-alpha_f * s['f']) * math.exp(-alpha_d0 * s['d0'])
        if tc_pred <= 0 or s['tc_exp'] <= 0: continue
        errs.append(max(tc_pred/s['tc_exp'], s['tc_exp']/tc_pred) - 1)
    errs.sort()
    return errs

print(f"\n{'='*70}")
print("预测精度对比")
print("="*70)

# 当前系数(15, 3)
errs_current = eval_precision(15.0, 3.0)
# 理论系数(β/√3, l_d+1)
errs_theory = eval_precision(f_theory, d0_theory_1)
# 拟合系数
errs_fit = eval_precision(-beta_fit[1], -beta_fit[2])

print(f"  当前(15, 3):       中位{errs_current[len(errs_current)//2]*100:.1f}%, 2倍内{sum(1 for e in errs_current if e<=1.0)/len(errs_current)*100:.1f}%")
print(f"  理论(β/√3, l_d+1): 中位{errs_theory[len(errs_theory)//2]*100:.1f}%, 2倍内{sum(1 for e in errs_theory if e<=1.0)/len(errs_theory)*100:.1f}%")
print(f"  拟合({-beta_fit[1]:.2f}, {-beta_fit[2]:.2f}): 中位{errs_fit[len(errs_fit)//2]*100:.1f}%, 2倍内{sum(1 for e in errs_fit if e<=1.0)/len(errs_fit)*100:.1f}%")

# 最优搜索
def objective(params):
    errs = eval_precision(params[0], params[1])
    return sum(e**2 for e in errs) / len(errs)

result = minimize(objective, [15.0, 3.0], method='Nelder-Mead')
errs_opt = eval_precision(result.x[0], result.x[1])
print(f"  最优({result.x[0]:.2f}, {result.x[1]:.2f}): 中位{errs_opt[len(errs_opt)//2]*100:.1f}%, 2倍内{sum(1 for e in errs_opt if e<=1.0)/len(errs_opt)*100:.1f}%")

print(f"\n结论:")
print(f"  f电子抑制系数: 理论β/√3={f_theory:.4f}, 拟合{-beta_fit[1]:.2f}, 最优{result.x[0]:.2f}")
print(f"  d0抑制系数: 理论l_d+1={d0_theory_1}, 拟合{-beta_fit[2]:.2f}, 最优{result.x[1]:.2f}")