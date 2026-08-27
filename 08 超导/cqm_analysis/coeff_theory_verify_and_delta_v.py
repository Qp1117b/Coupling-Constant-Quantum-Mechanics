"""验证γ_n映射系数的解析公式 + δ_v从C_mol谱传递推导

1. 验证 c_o = B²·t²/(3·U·λ_0²)
2. 分析dp_hybrid能标2531的物理含义
3. 从arccoth↔自由能等价导出δ_v的精确关系
4. 测试δ_v能否从C_mol谱特征预测
"""
import math, csv, os, re, sys
import numpy as np

sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework')
from atom_db import ATOM_DB

BETA = 8 * math.pi + 1
RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832,
                 52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
                 67.079811, 69.526405, 72.067158, 75.704690, 77.144840]
GAMMA_1, GAMMA_2 = RIEMANN_ZEROS[0], RIEMANN_ZEROS[1]

A_GAMMA = 0.369; B_LAMBDA = 3.09
C_GAMMA = 7.77e11; C_LAMBDA = 2.85e20
A_THEORY = math.log(C_LAMBDA / C_GAMMA) / A_GAMMA
B_THEORY = B_LAMBDA / A_GAMMA

GAMMA_D_GL2 = 2.196681962; GAMMA_P_GL2 = 2.128515269; GAMMA_S_GL2 = 0.0

LAM0 = B_THEORY / (A_THEORY - RIEMANN_ZEROS[3])  # 从偏置n=4反推, γ(4)=30.4249

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
    if not blocks: return np.array([[2.0]]), bi
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

def cmol_features(formula):
    """从C_mol谱提取特征"""
    atoms = {}
    for el, cnt in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', formula):
        if el in ATOM_DB: atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    if not atoms: return None
    C, bi = build_Cmol(atoms); af = atom_features(atoms)
    ev = np.sort(np.linalg.eigvalsh(C))
    if len(ev) < 2: return None
    sg = max(ev[1]-ev[0], 0.05); m = np.mean(ev); aniso = np.std(ev/m if m > 0 else ev)
    els = list(atoms.keys()); n_atoms = sum(atoms.values())
    avg_r = sum(atoms[el]*ATOM_DB[el][2] for el in els)/n_atoms
    l = max(2*avg_r*1e-10, 1e-20); theta_d = sum(atoms[el]*ATOM_DB[el][1] for el in els)/n_atoms
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

    nc = 4.00 + 0.50*math.log(1/sg) + 0.35*aniso + 13.0*af['inv_mass'] + 0.05*af['dp'] + 5.5*af['o']
    ni = int(nc); frac = nc - ni
    if ni < 1: gn = RIEMANN_ZEROS[0]
    elif ni >= len(RIEMANN_ZEROS): gn = 2*math.pi*nc/math.log(nc/(2*math.pi)) if nc > 6 else RIEMANN_ZEROS[-1]
    else: gn = RIEMANN_ZEROS[ni-1] + frac*(RIEMANN_ZEROS[ni]-RIEMANN_ZEROS[ni-1])

    return {'atoms': atoms, 'ev': ev, 'sg': sg, 'aniso': aniso, 'dd0': dd0,
            'G': G, 'theta_d': theta_d, 'gn': gn, 'af': af, 'n_atoms': n_atoms,
            'f_corr': f_corr, 'l': l, 'omega_d': omega_d}

# ============================================================
print("="*70)
print("1. 验证o_fraction系数: c_o = B²·t²/(3·U·λ_0²)")
print("="*70)

t_typ, U_typ = 0.5, 8.0
J_se = t_typ**2 / U_typ
c_o_theory = B_THEORY**2 * t_typ**2 / (3 * U_typ * LAM0**2)
c_o_emp = 5.5
print(f"  B={B_THEORY:.2f}, t={t_typ}eV, U={U_typ}eV, λ_0={LAM0:.4f}")
print(f"  c_o(理论) = B²·t²/(3·U·λ_0²) = {B_THEORY**2:.2f}·{t_typ**2:.2f}/(3·{U_typ}·{LAM0**2:.4f})")
print(f"            = {B_THEORY**2*t_typ**2:.4f}/{3*U_typ*LAM0**2:.4f} = {c_o_theory:.4f}")
print(f"  c_o(经验) = {c_o_emp}")
print(f"  差异: {abs(c_o_theory-c_o_emp)/c_o_emp*100:.2f}%")
print(f"\n  物理推导:")
print(f"    超交换 J = t²/U = {J_se:.4f} eV")
print(f"    3D方向平均: J_eff = J/3 = {J_se/3:.4f} eV")
print(f"    α_o = B·J_eff = B·t²/(3U) = {B_THEORY*J_se/3:.5f}")
print(f"    c_o = B·α_o/λ_0² = B²·t²/(3Uλ_0²) ✓")

# 验证: 用不同t, U值测试公式敏感性
print(f"\n  敏感性分析 (不同t, U):")
for t, U in [(0.3, 5), (0.5, 8), (0.7, 10), (0.4, 6), (0.6, 12)]:
    c = B_THEORY**2 * t**2 / (3 * U * LAM0**2)
    print(f"    t={t}, U={U}: c_o={c:.3f}")

# ============================================================
print(f"\n{'='*70}")
print("2. dp_hybrid能标分析")
print("="*70)

c_dp_emp = 0.05
alpha_dp = c_dp_emp * LAM0**2 / B_THEORY
casimir_d = 2.0  # j=1, j(j+1)=2
energy_scale = casimir_d / alpha_dp
print(f"  α_dp = {alpha_dp:.6f}")
print(f"  Casimir_d = j(j+1) = 2 (j=1, d波)")
print(f"  能标 = Casimir_d/α_dp = {energy_scale:.1f}")

# 尝试各种理论组合
print(f"\n  尝试理论匹配:")
candidates = {
    'B²': B_THEORY**2,
    'β²': BETA**2,
    'β³': BETA**3,
    '(2π)²': (2*math.pi)**2,
    '(2π)³': (2*math.pi)**3,
    'B²·γ₁': B_THEORY**2 * GAMMA_1,
    'B²·(γ₂-γ₁)': B_THEORY**2 * (GAMMA_2-GAMMA_1),
    'β²·B': BETA**2 * B_THEORY,
    'B·β²/2': B_THEORY * BETA**2 / 2,
    'B³': B_THEORY**3,
    'β·B²': BETA * B_THEORY**2,
    '2·B²·π': 2 * B_THEORY**2 * math.pi,
    'B²·(γ₁+γ₂)/2': B_THEORY**2 * (GAMMA_1+GAMMA_2)/2,
    'B²·ln(θ_D_typ)': B_THEORY**2 * math.log(400),  # 典型θ_D~400K
    'β²·ln(β)': BETA**2 * math.log(BETA),
    'B²·π/2': B_THEORY**2 * math.pi / 2,
}
for name, val in candidates.items():
    ratio = energy_scale / val
    if 0.8 < ratio < 1.2:
        print(f"    {name} = {val:.1f}, 能标/{name} = {ratio:.4f} {'✓' if 0.95<ratio<1.05 else ''}")

# dp_hybrid可能是二阶微扰, 不需要精确匹配
print(f"\n  结论: dp_hybrid系数={c_dp_emp}是弱修正(比aniso小7倍)")
print(f"  能标{energy_scale:.0f}可能来自dp杂化的二阶微扰t_dp²/Δ_dp")
print(f"  不需要精确解析形式, 保留为唯象小修正")

# ============================================================
print(f"\n{'='*70}")
print("3. δ_v从arccoth↔自由能等价精确导出")
print("="*70)

print(f"\n  arccoth闭式: Tc = θ_D/(2·arccoth(x))")
print(f"  自由能公式: Tc² = 8Δδ₀²·K_eff·θ_D/(9·ln2)")
print(f"  等价 => arccoth(x)² = 9·ln2·θ_D/(32·Δδ₀²·K_eff)")
print(f"  其中 x = 3β²Δδ₀²/[16(1-βδ_v)(γ₂-γ₁)]")
print(f"\n  => 1-βδ_v = 3β²Δδ₀²/[16·(γ₂-γ₁)·coth(√(9·ln2·θ_D/(32·Δδ₀²·K_eff)))]")

def delta_v_from_equivalence(dd0, theta_d, gn, G):
    """从arccoth↔自由能等价导出δ_v"""
    K0 = 7.77e11 * math.exp(0.369 * gn)
    K_eff = K0 * max(G, 1e-6)**(-0.75) * theta_d**(1.125)
    arg = 9 * LN2 * theta_d / (32 * dd0**2 * K_eff)
    if arg <= 0: return None
    x = 1.0 / math.tanh(math.sqrt(arg))  # coth(sqrt(arg))
    if x <= 1: return None
    one_minus_beta_dv = 3 * BETA**2 * dd0**2 / (16 * (GAMMA_2 - GAMMA_1) * x)
    if one_minus_beta_dv <= 0 or one_minus_beta_dv >= 1: return None
    dv = (1 - one_minus_beta_dv) / BETA
    return dv

# 加载数据
data = []
with open(os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv'), 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc > 0: data.append({'f': row['材料(化学式)'], 'cat': row['类别'], 'tc': tc})

# 计算每个材料的δ_v(从等价关系)和C_mol特征
records = []
for d in data:
    feat = cmol_features(d['f'])
    if feat is None: continue
    dv = delta_v_from_equivalence(feat['dd0'], feat['theta_d'], feat['gn'], feat['G'])
    if dv is None or dv <= 0: continue
    af = feat['af']
    # f电子和d0抑制
    suppress = math.exp(-15.0 * af['f']) * math.exp(-3.0 * af['d0'])
    if suppress < 0.01: continue
    records.append({
        'formula': d['f'], 'cat': d['cat'], 'tc': d['tc'],
        'dv': dv, 'beta_dv': BETA * dv, 'one_minus': 1 - BETA * dv,
        'dd0': feat['dd0'], 'G': feat['G'], 'theta_d': feat['theta_d'],
        'gn': feat['gn'], 'sg': feat['sg'], 'aniso': feat['aniso'],
        'inv_mass': af['inv_mass'], 'dp': af['dp'], 'o': af['o'],
        'f': af['f'], 'd0': af['d0'], 'n_atoms': feat['n_atoms'],
    })

print(f"\n  有效记录: {len(records)}")

# 统计βδ_v分布
beta_dvs = [r['beta_dv'] for r in records]
beta_dvs.sort()
med = beta_dvs[len(beta_dvs)//2]
print(f"  βδ_v中位 = {med:.4f}")
print(f"  βδ_v范围: [{min(beta_dvs):.4f}, {max(beta_dvs):.4f}]")
print(f"  1-βδ_v中位 = {1-med:.6f}")

# ============================================================
print(f"\n{'='*70}")
print("4. δ_v从C_mol谱特征预测 (第一性回归)")
print("="*70)

# 目标: 1-βδ_v = f(C_mol特征)
# 特征: Δδ₀, γ_n, θ_D, G, sg, aniso, inv_mass, dp, o
from numpy.linalg import lstsq

y = np.array([r['one_minus'] for r in records])
y_log = np.log(y)

# 特征矩阵 (对数空间)
features = []
feat_names = []
for r in records:
    features.append([
        1.0,
        math.log(r['dd0']),
        math.log(r['gn'] - GAMMA_1),
        math.log(r['theta_d']),
        math.log(r['G']),
        math.log(1.0 / r['sg']),
        r['aniso'],
        r['inv_mass'],
        r['dp'],
        r['o'],
    ])
X = np.array(features)
feat_names = ['const', 'log(Δδ₀)', 'log(γ_n-γ₁)', 'log(θ_D)', 'log(G)',
              'log(1/sg)', 'aniso', 'inv_mass', 'dp', 'o']

# Ridge回归
for ridge_alpha in [0, 0.01, 0.1, 1.0]:
    if ridge_alpha == 0:
        coef, _, _, _ = lstsq(X, y_log, rcond=None)
    else:
        XtX = X.T @ X + ridge_alpha * np.eye(X.shape[1])
        coef = np.linalg.solve(XtX, X.T @ y_log)
    y_pred = X @ coef
    residuals = y_pred - y_log
    r2 = 1 - np.var(residuals) / np.var(y_log) if np.var(y_log) > 0 else 0
    # 对称误差
    y_exp_pred = np.exp(y_pred)
    errs = [max(p/e, e/p) - 1 for p, e in zip(y_exp_pred, y)]
    errs.sort()
    med_err = errs[len(errs)//2] * 100
    w2 = sum(1 for e in errs if e <= 1.0) / len(errs) * 100
    if ridge_alpha in [0, 0.1]:
        print(f"\n  Ridge α={ridge_alpha}: R²={r2:.4f}, 中位{med_err:.1f}%, 2倍内{w2:.1f}%")
        for n, c in zip(feat_names, coef):
            print(f"    {n:15s}: {c:+.4f}")

# ============================================================
print(f"\n{'='*70}")
print("5. δ_v的物理约束检验")
print("="*70)

# 关键检验: 1-βδ_v是否主要依赖Δδ₀和γ_n?
print(f"\n  简化模型: 1-βδ_v = c·Δδ₀^a·(γ_n-γ₁)^b")
X_simple = np.array([[1.0, math.log(r['dd0']), math.log(r['gn']-GAMMA_1)] for r in records])
coef_s, _, _, _ = lstsq(X_simple, y_log, rcond=None)
y_pred_s = X_simple @ coef_s
r2_s = 1 - np.var(y_pred_s - y_log) / np.var(y_log)
print(f"  R² = {r2_s:.4f}")
print(f"  c = exp({coef_s[0]:.4f}) = {math.exp(coef_s[0]):.4f}")
print(f"  a(Δδ₀) = {coef_s[1]:.4f}")
print(f"  b(γ_n-γ₁) = {coef_s[2]:.4f}")

# 加θ_D
X3 = np.array([[1.0, math.log(r['dd0']), math.log(r['gn']-GAMMA_1), math.log(r['theta_d'])] for r in records])
coef3, _, _, _ = lstsq(X3, y_log, rcond=None)
y_pred3 = X3 @ coef3
r2_3 = 1 - np.var(y_pred3 - y_log) / np.var(y_log)
print(f"\n  加θ_D: R² = {r2_3:.4f}, θ_D指数 = {coef3[3]:.4f}")

# 加G
X4 = np.array([[1.0, math.log(r['dd0']), math.log(r['gn']-GAMMA_1), math.log(r['theta_d']), math.log(r['G'])] for r in records])
coef4, _, _, _ = lstsq(X4, y_log, rcond=None)
y_pred4 = X4 @ coef4
r2_4 = 1 - np.var(y_pred4 - y_log) / np.var(y_log)
print(f"  加G:   R² = {r2_4:.4f}, G指数 = {coef4[4]:.4f}")

# ============================================================
print(f"\n{'='*70}")
print("6. 用δ_v(等价)计算arccoth闭式Tc并验证")
print("="*70)

def arccoth_tc(dd0, theta_d, gn, G, dv):
    """arccoth闭式Tc"""
    one_minus = 1 - BETA * dv
    if one_minus <= 0: return 0
    x = 3 * BETA**2 * dd0**2 / (16 * one_minus * (GAMMA_2 - GAMMA_1))
    if x <= 1: return 0
    tc = theta_d / (2 * math.atanh(1.0 / x))  # arccoth(x) = atanh(1/x)
    return tc

# 用等价δ_v计算Tc (应该精确匹配自由能公式)
errs_eq = []
for r in records:
    tc_pred = arccoth_tc(r['dd0'], r['theta_d'], r['gn'], r['G'], r['dv'])
    if tc_pred > 0:
        errs_eq.append(max(tc_pred/r['tc'], r['tc']/tc_pred) - 1)
errs_eq.sort()
print(f"  等价δ_v → arccoth Tc vs 实验:")
print(f"    中位{errs_eq[len(errs_eq)//2]*100:.1f}%  2倍内{sum(1 for e in errs_eq if e<=1.0)/len(errs_eq)*100:.1f}%")

# 用简化模型δ_v计算Tc
print(f"\n  简化模型δ_v → arccoth Tc:")
c_s, a_s, b_s = math.exp(coef_s[0]), coef_s[1], coef_s[2]
errs_simple = []
for r in records:
    one_minus = c_s * r['dd0']**a_s * (r['gn']-GAMMA_1)**b_s
    if one_minus <= 0 or one_minus >= 1: continue
    dv = (1 - one_minus) / BETA
    tc_pred = arccoth_tc(r['dd0'], r['theta_d'], r['gn'], r['G'], dv)
    if tc_pred > 0:
        errs_simple.append(max(tc_pred/r['tc'], r['tc']/tc_pred) - 1)
if errs_simple:
    errs_simple.sort()
    print(f"    δ_v = (1 - {c_s:.4f}·Δδ₀^{a_s:.3f}·(γ_n-γ₁)^{b_s:.3f})/β")
    print(f"    中位{errs_simple[len(errs_simple)//2]*100:.1f}%  2倍内{sum(1 for e in errs_simple if e<=1.0)/len(errs_simple)*100:.1f}%")

# ============================================================
print(f"\n{'='*70}")
print("总结")
print("="*70)
print(f"""
γ_n映射系数理论推导:
  偏置 n₀ = 4.00 = N⁻¹(A - B/λ₀), λ₀ = {LAM0:.4f}
  c_aniso = (γ_d-γ_s)/2π = 0.3496 (GL(2)零点差) ✓ 差异0.11%
  c_o = B²·t²/(3Uλ₀²) = {c_o_theory:.3f} (超交换+3D平均) ✓ 差异{abs(c_o_theory-5.5)/5.5*100:.2f}%
  c_mass = B·α_mass/λ₀², α_mass=0.2055 (Hopfield)
  c_log = B·α_log/λ₀², α_log=0.00790 (van Hove)
  c_dp = 0.05 (弱修正, 二阶微扰)

δ_v从等价关系导出:
  1-βδ_v = 3β²Δδ₀²/[16(γ₂-γ₁)·coth(√(9ln2·θ_D/(32Δδ₀²K_eff)))]
  简化: 1-βδ_v ≈ {c_s:.4f}·Δδ₀^{a_s:.3f}·(γ_n-γ₁)^{b_s:.3f}, R²={r2_s:.3f}
""")