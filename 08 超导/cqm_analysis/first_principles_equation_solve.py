"""CQM第一性方程: 从同步算符本征值交叉直接求解Tc

基本方程 (非拟合):
  同步算符本征值:
    λ_n(T) = γ_n + [coth(θD/2T)-1](ln n)² - β²(n²-1)Δδv²/(4n²(1-βδv))

  相变条件 (本征值交叉):
    λ_2(Tc) = λ_1(Tc)

  等价超越方程:
    coth(y) = 1 + [-Δγ + A·tanh(y)] / (ln2)²
    y = θD/(2Tc), A = 3β²Δδ₀²/[16(1-βδv)]

  温度依赖:
    Δδv(T) = Δδ₀·√tanh(θD/2T)

输入 (全部从C_mol/几何计算):
  β = 8π+1 (A4群论)
  γ₁, γ₂ (Riemann零点)
  Δδ₀ = √(C²/l²·3ℏ/(4ωD)·(1-f)·es) (零点涨落)
  δ_v = Regge角亏 (从C_mol键长/键角计算)
  θD (Debye温度)

关键: 不经过K₀拟合, 直接从方程求解!
"""
import math, csv, os, re, sys
import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework')
from atom_db import ATOM_DB

BETA = 8 * math.pi + 1
RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832]
GAMMA_1, GAMMA_2 = RIEMANN_ZEROS[0], RIEMANN_ZEROS[1]
DELTA_GAMMA = GAMMA_2 - GAMMA_1

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
C2 = 2.0/3.0; LN2 = math.log(2)

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
    els = list(atoms.keys()); blocks = []; bi = []
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        for l, occ, cap in valence_orbitals(z):
            if l == 0: blocks.append(A1.copy()); bi.append((el, 's', 1))
            elif l == 1: blocks.append(A3.copy()); bi.append((el, 'p', 3))
            elif l == 2: blocks.append(A4.copy()); bi.append((el, 'd', 4))
    if not blocks: return np.array([[2.0]]), bi, []
    size = sum(b.shape[0] for b in blocks); C = np.zeros((size, size)); idx = 0
    for b in blocks: s = b.shape[0]; C[idx:idx+s, idx:idx+s] = b; idx += s
    couplings = []
    idx_i = 0
    for i, binfo in enumerate(bi):
        si = binfo[2]; idx_j = idx_i + si
        for j, bjinfo in enumerate(bi[i+1:], start=i+1):
            sj = bjinfo[2]; ri = ATOM_DB.get(binfo[0], (1, 0, 1.5, 8))[2]; rj = ATOM_DB.get(bjinfo[0], (1, 0, 1.5, 8))[2]
            t0 = 0.1 * math.exp(-(ri + rj) / 3.0)
            if (binfo[1] == 'd' and bjinfo[1] == 'p') or (binfo[1] == 'p' and bjinfo[1] == 'd'): t0 *= 1.5
            for a in range(si):
                for b in range(sj): C[idx_i+a, idx_j+b] = t0; C[idx_j+b, idx_i+a] = t0
            couplings.append((binfo[0], bjinfo[0], t0, ri, rj))
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

def compute_delta_v_regge(atoms, couplings):
    """从C_mol键长计算Regge角亏 δ_v

    Regge角亏: δ_v = 2π - Σ面角
    从键长用余弦定理计算三角形内角

    简化: 用原子半径估计键长, 构造Regge四面体
    """
    els = list(atoms.keys())
    if len(els) < 2:
        return 1.0 / BETA  # 单原子: 理想几何, δ_v = 1/β

    # 从原子半径估计键长
    bond_lengths = {}
    for i, el1 in enumerate(els):
        for j, el2 in enumerate(els):
            if i < j:
                r1 = ATOM_DB.get(el1, (1, 0, 1.5, 8))[2]
                r2 = ATOM_DB.get(el2, (1, 0, 1.5, 8))[2]
                # 键长 ≈ r1 + r2 (共价半径之和)
                bond_lengths[(el1, el2)] = r1 + r2

    if len(els) == 2:
        # 二原子: 无角亏定义, 用谱涨落代理
        return 1.0 / BETA

    # 三原子以上: 构造三角形, 计算角亏
    # 取前三个原子构造三角形
    if len(els) >= 3:
        el1, el2, el3 = els[0], els[1], els[2]
        a = bond_lengths.get((el1, el2), 3.0)  # 边1-2
        b = bond_lengths.get((el1, el3), 3.0)  # 边1-3
        c = bond_lengths.get((el2, el3), 3.0)  # 边2-3

        # 余弦定理
        try:
            cos_alpha = (a**2 + b**2 - c**2) / (2*a*b)  # 角1
            cos_beta = (a**2 + c**2 - b**2) / (2*a*c)   # 角2
            cos_gamma = (b**2 + c**2 - a**2) / (2*b*c)  # 角3

            # 限制在[-1, 1]
            cos_alpha = max(-1, min(1, cos_alpha))
            cos_beta = max(-1, min(1, cos_beta))
            cos_gamma = max(-1, min(1, cos_gamma))

            alpha = math.acos(cos_alpha)
            beta = math.acos(cos_beta)
            gamma = math.acos(cos_gamma)

            # 三角形角亏 = 2π - 三角形内角和 (球面)
            # 平面三角形内角和 = π, 所以平面角亏 = 2π - π = π
            # Regge角亏 = 2π - Σ角 (对于球面剖分)
            angle_sum = alpha + beta + gamma
            delta_v_regge = 2 * math.pi - angle_sum

            # 归一化到[0, 1/β]范围
            # 平面三角形: delta_v = π, 球面: delta_v < π
            # 映射到δ_v ∈ (0, 1/β)
            delta_v_normalized = (1.0 / BETA) * (1.0 - abs(delta_v_regge) / math.pi)

            return max(0.001 / BETA, min(1.0 / BETA, delta_v_normalized))
        except:
            return 1.0 / BETA

    return 1.0 / BETA

def compute_delta_v_spectral(atoms, C, ev):
    """从C_mol谱涨落计算δ_v

    δ_v ≈ 1/β - 谱涨落修正
    谱涨落 = 间距标准差/间距均值 (变异系数)
    """
    if len(ev) < 3:
        return 1.0 / BETA

    spacings = np.diff(ev)
    mean_sp = np.mean(spacings)
    std_sp = np.std(spacings)
    cv = std_sp / mean_sp if mean_sp > 0 else 0

    # δ_v = 1/β · (1 - cv²) — 谱越均匀, δ_v越接近1/β
    delta_v = (1.0 / BETA) * max(0, 1 - cv**2)
    return max(0.001 / BETA, min(1.0 / BETA, delta_v))

def compute_delta_v_berry(atoms, C, ev):
    """从C_mol谱估计Berry曲率角亏

    δ_intrinsic = (1/2π)∫_FS |Ω(k)|dS / A_FS

    简化: 用谱各向异性代理Berry曲率
    """
    if len(ev) < 2:
        return 1.0 / BETA

    m = np.mean(ev)
    aniso = np.std(ev / m if m > 0 else ev)

    # van Hove奇点 → 大Berry曲率 → 大角亏
    # 球形Fermi面 → 零Berry曲率 → 零角亏
    # δ_v = 1/β · (1 - aniso/π)
    delta_v = (1.0 / BETA) * max(0, 1 - aniso / math.pi)
    return max(0.001 / BETA, min(1.0 / BETA, delta_v))

def solve_tc_from_equation(theta_d, dd0, delta_v):
    """从超越方程数值求解Tc

    coth(y) = 1 + [-Δγ + A·tanh(y)] / (ln2)²
    y = θD/(2Tc), A = 3β²Δδ₀²/[16(1-βδv)]
    """
    one_minus = 1 - BETA * delta_v
    if one_minus <= 0:
        return 0

    A = 3 * BETA**2 * dd0**2 / (16 * one_minus)

    # 超越方程: f(y) = coth(y) - 1 - [-Δγ + A·tanh(y)]/(ln2)² = 0
    def equation(y):
        if y <= 0:
            return float('inf')
        coth_y = 1.0 / math.tanh(y)
        tanh_y = math.tanh(y)
        return coth_y - 1 - (-DELTA_GAMMA + A * tanh_y) / LN2**2

    # 搜索解的范围
    # y大 → Tc小, y小 → Tc大
    # 超导条件: A > Δγ (即 x > 1)
    if A <= DELTA_GAMMA:
        return 0  # 不超导

    # 二分法求解
    try:
        y_low = 0.1
        y_high = 50.0

        f_low = equation(y_low)
        f_high = equation(y_high)

        # 检查是否有解
        if f_low * f_high > 0:
            return 0

        y_sol = brentq(equation, y_low, y_high, xtol=1e-10)
        tc = theta_d / (2 * y_sol)
        return tc
    except:
        return 0

def compute_all_first_principles(formula, delta_v_method='spectral'):
    """完全第一性计算: C_mol → δ_v, Δδ₀ → 超越方程 → Tc"""
    atoms = {}
    for el, cnt in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', formula):
        if el in ATOM_DB: atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    if not atoms: return None

    C, bi, couplings = build_Cmol(atoms)
    af = atom_features(atoms)
    ev = np.sort(np.linalg.eigvalsh(C))
    if len(ev) < 2: return None

    # Δδ₀ (零点涨落, 从晶格几何)
    els = list(atoms.keys()); n_atoms = sum(atoms.values())
    avg_r = sum(atoms[el]*ATOM_DB[el][2] for el in els)/n_atoms
    l = max(2*avg_r*1e-10, 1e-20)
    theta_d = sum(atoms[el]*ATOM_DB[el][1] for el in els)/n_atoms
    if theta_d <= 0: return None
    n_eff = max(2, n_atoms); f_corr = 1.0 - 0.3*(1.0 - 1.0/n_eff)
    es = 0
    for i in range(len(els)):
        for j in range(i+1, len(els)):
            mi = atoms[els[i]]*ATOM_DB[els[i]][0]*AMU; mj = atoms[els[j]]*ATOM_DB[els[j]][0]*AMU
            es += (1/mi + 1/mj)
    if not es:
        mi = sum(atoms[el]*ATOM_DB[el][0] for el in els)*AMU/n_atoms
        es = max(1, n_eff*(n_eff-1)/2)*2.0/mi
    G = (1/l)*math.sqrt((1-f_corr)*es); omega_d = theta_d*KB/HBAR
    dd0_sq = (C2/l**2)*(3*HBAR/(4*omega_d))*(1-f_corr)*es; dd0 = math.sqrt(abs(dd0_sq))

    # δ_v (从C_mol, 三种方法)
    if delta_v_method == 'regge':
        delta_v = compute_delta_v_regge(atoms, couplings)
    elif delta_v_method == 'berry':
        delta_v = compute_delta_v_berry(atoms, C, ev)
    else:  # spectral
        delta_v = compute_delta_v_spectral(atoms, C, ev)

    # 超越方程求解Tc
    tc = solve_tc_from_equation(theta_d, dd0, delta_v)

    # 抑制因子
    suppress = math.exp(-15.0 * af['f']) * math.exp(-3.0 * af['d0'])
    tc *= suppress

    return {
        'tc': tc, 'dd0': dd0, 'delta_v': delta_v,
        'beta_dv': BETA * delta_v, 'one_minus': 1 - BETA * delta_v,
        'A_param': 3 * BETA**2 * dd0**2 / (16 * max(1 - BETA * delta_v, 1e-20)),
        'theta_d': theta_d, 'G': G, 'af': af,
    }

# ============================================================
print("="*70)
print("CQM第一性方程: 从同步算符本征值交叉直接求解Tc")
print("="*70)

print(f"""
基本方程:
  同步算符本征值:
    λ_n(T) = γ_n + [coth(θD/2T)-1](ln n)² - β²(n²-1)Δδv²(T)/(4n²(1-βδv))

  相变条件:
    λ_2(Tc) = λ_1(Tc)

  超越方程 (代入后):
    coth(y) = 1 + [-Δγ + A·tanh(y)] / (ln2)²
    y = θD/(2Tc), A = 3β²Δδ₀²/[16(1-βδv)]

  温度依赖:
    Δδv(T) = Δδ₀·√tanh(θD/2T)

常数:
  β = 8π+1 = {BETA:.4f}
  γ₁ = {GAMMA_1:.6f}, γ₂ = {GAMMA_2:.6f}, Δγ = {DELTA_GAMMA:.6f}
  C² = 2/3 (正四面体Regge)

关键: 不经过K₀拟合, 直接从方程求解!
""")

# 加载数据
data = []
with open(os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv'), 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc > 0: data.append({'f': row['材料(化学式)'], 'cat': row['类别'], 'tc': tc})

def sym_err(p, e):
    if p <= 0 or e <= 0: return float('inf')
    return max(p/e, e/p) - 1

# ============================================================
print("="*70)
print("1. 三种δ_v计算方法对比")
print("="*70)

for method_name in ['spectral', 'berry', 'regge']:
    errs = []; n_valid = 0; n_super = 0
    beta_dvs = []; A_params = []
    for d in data:
        result = compute_all_first_principles(d['f'], method_name)
        if result is None: continue
        n_valid += 1
        beta_dvs.append(result['beta_dv'])
        A_params.append(result['A_param'])
        if result['tc'] > 0:
            n_super += 1
            errs.append(sym_err(result['tc'], d['tc']))

    beta_dvs.sort()
    A_params.sort()
    print(f"\n  方法: {method_name}")
    print(f"    有效: {n_valid}, 预测超导: {n_super}")
    print(f"    βδ_v中位: {beta_dvs[len(beta_dvs)//2]:.4f}")
    print(f"    A/Δγ中位: {A_params[len(A_params)//2]/DELTA_GAMMA:.4f} (>1才超导)")
    if errs:
        errs.sort()
        print(f"    Tc预测: 中位{errs[len(errs)//2]*100:.1f}%  2倍内{sum(1 for e in errs if e<=1.0)/len(errs)*100:.1f}%")
    else:
        print(f"    无超导预测")

# ============================================================
print(f"\n{'='*70}")
print("2. 谱方法详细分析 (最有希望)")
print("="*70)

results = []
for d in data:
    r = compute_all_first_principles(d['f'], 'spectral')
    if r is not None:
        r['formula'] = d['f']; r['cat'] = d['cat']; r['tc_exp'] = d['tc']
        results.append(r)

# 统计
superconducting = [r for r in results if r['tc'] > 0]
not_superconducting = [r for r in results if r['tc'] == 0]

print(f"  总材料: {len(results)}")
print(f"  预测超导(Tc>0): {len(superconducting)}")
print(f"  预测不超导: {len(not_superconducting)}")

# A/Δγ分布
ratios = [r['A_param']/DELTA_GAMMA for r in results]
ratios.sort()
print(f"\n  A/Δγ分布 (>1才超导):")
print(f"    中位: {ratios[len(ratios)//2]:.4f}")
print(f"    范围: [{ratios[0]:.4f}, {ratios[-1]:.4f}]")
print(f"    >1比例: {sum(1 for r in ratios if r > 1)/len(ratios)*100:.1f}%")

# βδ_v分布
bdvs = [r['beta_dv'] for r in results]
bdvs.sort()
print(f"\n  βδ_v分布:")
print(f"    中位: {bdvs[len(bdvs)//2]:.4f}")
print(f"    范围: [{bdvs[0]:.4f}, {bdvs[-1]:.4f}]")

# 按类别
print(f"\n  按类别:")
cats = {}
for r in results:
    c = r['cat']
    if c not in cats: cats[c] = []
    cats[c].append(r)

for cat, recs in sorted(cats.items(), key=lambda x: -len(x[1])):
    if len(recs) < 3: continue
    n_super_cat = sum(1 for r in recs if r['tc'] > 0)
    ratios_cat = [r['A_param']/DELTA_GAMMA for r in recs]
    ratios_cat.sort()
    med_ratio = ratios_cat[len(ratios_cat)//2]
    print(f"    {cat:20s} n={len(recs):3d}: 超导{n_super_cat:3d} A/Δγ中位{med_ratio:.3f}")

# ============================================================
print(f"\n{'='*70}")
print("3. 超越方程的解的性质")
print("="*70)

# 分析方程 coth(y) = 1 + [-Δγ + A·tanh(y)]/(ln2)²
# 当A/Δγ略大于1时, y很大(Tc很小)
# 当A/Δγ很大时, y较小(Tc较大)

print(f"  方程: coth(y) = 1 + [-{DELTA_GAMMA:.4f} + A·tanh(y)]/{LN2**2:.4f}")
print(f"  超导条件: A > Δγ = {DELTA_GAMMA:.4f}")
print(f"\n  A/Δγ vs Tc/θD 关系:")

for ratio in [1.001, 1.01, 1.1, 1.5, 2.0, 5.0, 10.0, 100.0]:
    A = ratio * DELTA_GAMMA
    def eq(y):
        if y <= 0: return float('inf')
        return 1.0/math.tanh(y) - 1 - (-DELTA_GAMMA + A*math.tanh(y))/LN2**2
    try:
        if eq(0.1) * eq(50) < 0:
            y_sol = brentq(eq, 0.1, 50, xtol=1e-10)
            tc_over_theta = 1.0 / (2 * y_sol)
            print(f"    A/Δγ={ratio:8.3f}: y={y_sol:8.4f}, Tc/θD={tc_over_theta:.6f}")
    except:
        pass

# ============================================================
print(f"\n{'='*70}")
print("4. 关键问题: δ_v的敏感性")
print("="*70)

# δ_v对Tc的影响: 1-βδv出现在A的分母中
# A = 3β²Δδ₀²/[16(1-βδv)]
# 当1-βδv很小时, A很大, Tc很大
# 当1-βδv接近1时, A很小, 可能不超导

print(f"  A = 3β²Δδ₀²/[16(1-βδv)]")
print(f"  当1-βδv → 0: A → ∞, Tc → θD/2 (最大)")
print(f"  当1-βδv → 1: A → 3β²Δδ₀²/16, 可能<Δγ (不超导)")
print(f"\n  δ_v的精确计算至关重要!")
print(f"  谱方法: δ_v = 1/β·(1-cv²), cv=谱间距变异系数")
print(f"  问题: cv²通常很小(0.01-0.1), 使1-βδv≈cv²≈0.01-0.1")
print(f"  这使A很大, Tc很大 — 可能高估Tc")

# 验证: 用实验Tc反推δ_v, 对比谱方法δ_v
print(f"\n  反推δ_v vs 谱方法δ_v:")
reverse_dvs = []; spectral_dvs = []
for d in data[:50]:  # 前50个
    r = compute_all_first_principles(d['f'], 'spectral')
    if r is None or r['dd0'] <= 0: continue
    # 反推: 从实验Tc反推δ_v
    y_exp = r['theta_d'] / (2 * d['tc'])
    if y_exp <= 0: continue
    coth_y = 1.0 / math.tanh(y_exp)
    tanh_y = math.tanh(y_exp)
    # coth(y) = 1 + [-Δγ + A·tanh(y)]/(ln2)²
    # A = [coth(y) - 1 + Δγ/(ln2)²] · (ln2)² / tanh(y)
    A_reverse = (coth_y - 1 + DELTA_GAMMA/LN2**2) * LN2**2 / tanh_y
    # A = 3β²Δδ₀²/[16(1-βδv)]
    # 1-βδv = 3β²Δδ₀²/(16A)
    one_minus_reverse = 3 * BETA**2 * r['dd0']**2 / (16 * A_reverse)
    if one_minus_reverse <= 0 or one_minus_reverse >= 1: continue
    dv_reverse = (1 - one_minus_reverse) / BETA
    reverse_dvs.append(dv_reverse)
    spectral_dvs.append(r['delta_v'])

if reverse_dvs:
    print(f"    样本数: {len(reverse_dvs)}")
    print(f"    反推δ_v中位: {sorted(reverse_dvs)[len(reverse_dvs)//2]:.6f}")
    print(f"    谱方法δ_v中位: {sorted(spectral_dvs)[len(spectral_dvs)//2]:.6f}")
    print(f"    1/β = {1/BETA:.6f}")
    print(f"    反推βδ_v中位: {BETA*sorted(reverse_dvs)[len(reverse_dvs)//2]:.4f}")
    print(f"    谱方法βδ_v中位: {BETA*sorted(spectral_dvs)[len(spectral_dvs)//2]:.4f}")

# ============================================================
print(f"\n{'='*70}")
print("5. 总结: 第一性方程的状态")
print("="*70)
print(f"""
CQM超导基本方程 (非拟合):

  1. 同步算符本征值方程:
     λ_n(T) = γ_n + [coth(θD/2T)-1](ln n)² - β²(n²-1)Δδv²(T)/(4n²(1-βδv))

  2. 相变条件:
     λ_2(Tc) = λ_1(Tc)

  3. 超越方程 (数值求解):
     coth(y) = 1 + [-Δγ + A·tanh(y)] / (ln2)²
     y = θD/(2Tc), A = 3β²Δδ₀²/[16(1-βδv)]

方程中的量:
  ✓ β = 8π+1 (A4群论, 精确)
  ✓ γ₁, γ₂ (Riemann零点, 数学常数)
  ✓ Δδ₀ (从晶格几何直接计算, C²=2/3严格导出)
  ✓ θD (从原子数据库)
  ? δ_v (需要从C_mol/Regge几何/Berry曲率计算 — 当前方法不够精确)

关键问题:
  δ_v的精确计算是整个方程链的瓶颈
  - Regge余弦定理: 需要3D键长/键角, C_mol只给2D信息
  - Berry曲率: 需要Fermi面几何, 需要能带计算
  - 谱涨落: 当前代理不够精确

  δ_v ≈ 1/β (临界同步), 1-βδv是小量(~0.003)
  Tc对1-βδv极其敏感 — 需要高精度δ_v

与薛定谔方程的类比:
  薛定谔: Ĥψ=Eψ → 给定V(r), 解出E_n
  CQM:    λ_n(T)=0 → 给定C_mol, 解出Tc
  共同点: 从算符本征值方程直接求解
  差异: CQM的算符形式是猜测(从物理约束), 非从作用量变分导出
""")