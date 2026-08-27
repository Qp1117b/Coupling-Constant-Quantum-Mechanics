"""从C_mol谱直接计算δ_v — 不经过K_eff

δ_v物理含义: 能级间距变分参数
在CQM理论中 δ_v ≈ 1/β (临界点), 1-βδ_v是小量

尝试多种C_mol谱统计量作为δ_v定义:
1. 间距变异系数 cv = std(spacings)/mean(spacings)
2. 间距标准差
3. 谱隙/平均间距
4. 高阶间距比
5. 谱形参数
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

def compute_all_features(formula):
    atoms = {}
    for el, cnt in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', formula):
        if el in ATOM_DB: atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    if not atoms: return None
    C, bi = build_Cmol(atoms); af = atom_features(atoms)
    ev = np.sort(np.linalg.eigvalsh(C))
    if len(ev) < 3: return None

    spacings = np.diff(ev)
    sg = max(ev[1]-ev[0], 0.05)
    m = np.mean(ev); aniso = np.std(ev/m if m > 0 else ev)

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

    nc = 4.00 + 0.50*math.log(1/sg) + 0.35*aniso + 13.0*af['inv_mass'] + 0.05*af['dp'] + 5.5*af['o']
    ni = int(nc); frac = nc - ni
    if ni < 1: gn = RIEMANN_ZEROS[0]
    elif ni >= len(RIEMANN_ZEROS): gn = 2*math.pi*nc/math.log(nc/(2*math.pi)) if nc > 6 else RIEMANN_ZEROS[-1]
    else: gn = RIEMANN_ZEROS[ni-1] + frac*(RIEMANN_ZEROS[ni]-RIEMANN_ZEROS[ni-1])

    # C_mol谱统计量
    mean_sp = np.mean(spacings)
    std_sp = np.std(spacings)
    cv_sp = std_sp / mean_sp if mean_sp > 0 else 0  # 变异系数
    # 间距比
    ratios = spacings[1:] / spacings[:-1] if len(spacings) > 1 else np.array([1.0])
    # Wigner-Dyson型统计
    s_normalized = spacings / mean_sp  # 归一化间距
    # 谱刚性Delta_3 (简化)
    n_sp = len(spacings)
    delta3 = np.var(np.cumsum(s_normalized - 1)) / n_sp if n_sp > 0 else 0

    # 谱熵
    p = np.abs(spacings) / np.sum(np.abs(spacings))
    spec_entropy = -np.sum(p * np.log(p + 1e-20))

    # 最大间距/最小间距
    sp_ratio = max(spacings) / min(spacings) if min(spacings) > 0 else 1

    return {
        'atoms': atoms, 'ev': ev, 'spacings': spacings,
        'sg': sg, 'aniso': aniso, 'dd0': dd0, 'G': G, 'theta_d': theta_d, 'gn': gn,
        'af': af, 'n_atoms': n_atoms,
        'mean_sp': mean_sp, 'std_sp': std_sp, 'cv_sp': cv_sp,
        'sp_ratio': sp_ratio, 'spec_entropy': spec_entropy,
        'delta3': delta3, 'n_sp': n_sp,
        'min_sp': min(spacings), 'max_sp': max(spacings),
        'median_sp': np.median(spacings),
    }

def arccoth_tc(dd0, theta_d, gn, dv):
    """arccoth闭式Tc, δ_v直接输入"""
    one_minus = 1 - BETA * dv
    if one_minus <= 0: return 0
    x = 3 * BETA**2 * dd0**2 / (16 * one_minus * (GAMMA_2 - GAMMA_1))
    if x <= 1: return 0
    tc = theta_d / (2 * math.atanh(1.0 / x))
    return tc

def sym_err(p, e):
    if p <= 0 or e <= 0: return float('inf')
    return max(p/e, e/p) - 1

# 加载数据
data = []
with open(os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv'), 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc > 0: data.append({'f': row['材料(化学式)'], 'cat': row['类别'], 'tc': tc})

# 计算所有特征
records = []
for d in data:
    feat = compute_all_features(d['f'])
    if feat is None: continue
    af = feat['af']
    suppress = math.exp(-15.0 * af['f']) * math.exp(-3.0 * af['d0'])
    if suppress < 0.01: continue
    feat['formula'] = d['f']; feat['cat'] = d['cat']; feat['tc'] = d['tc']
    records.append(feat)

print(f"有效记录: {len(records)}")

# ============================================================
print(f"\n{'='*70}")
print("1. δ_v的多种C_mol谱定义 vs 1/β")
print("="*70)
print(f"  1/β = {1/BETA:.6f}")

# 从实验Tc反推δ_v (基准)
def delta_v_from_tc(tc, dd0, theta_d, gn):
    """从实验Tc反推δ_v"""
    arg = theta_d / (2 * tc)
    if arg <= 1: return None
    x = 1.0 / math.tanh(arg)  # coth(θ_D/2Tc)
    if x <= 1: return None
    one_minus = 3 * BETA**2 * dd0**2 / (16 * (GAMMA_2 - GAMMA_1) * x)
    if one_minus <= 0 or one_minus >= 1: return None
    return (1 - one_minus) / BETA

# 计算反推δ_v
for r in records:
    r['dv_reverse'] = delta_v_from_tc(r['tc'], r['dd0'], r['theta_d'], r['gn'])
    r['one_minus_reverse'] = 1 - BETA * r['dv_reverse'] if r['dv_reverse'] else None

valid = [r for r in records if r['dv_reverse'] and r['one_minus_reverse'] and r['one_minus_reverse'] > 0]
print(f"  有效反推δ_v记录: {len(valid)}")

# 对比各种δ_v定义
dv_defs = {
    '1/β (常数)': lambda r: 1.0/BETA,
    'cv_sp/β': lambda r: r['cv_sp'] / BETA,
    '1/β·(1-cv_sp²)': lambda r: (1.0/BETA) * (1 - r['cv_sp']**2),
    '1/β·exp(-cv_sp²)': lambda r: (1.0/BETA) * math.exp(-r['cv_sp']**2),
    '1/β·(1-1/sp_ratio)': lambda r: (1.0/BETA) * (1 - 1.0/r['sp_ratio']),
    '1/β·(1-δ₃)': lambda r: (1.0/BETA) * max(0, 1 - r['delta3']),
    'median_sp/mean_sp/β': lambda r: (r['median_sp']/r['mean_sp']) / BETA if r['mean_sp']>0 else 1/BETA,
    '1/β·(1-aniso/π)': lambda r: (1.0/BETA) * max(0, 1 - r['aniso']/math.pi),
    '1/β·exp(-aniso)': lambda r: (1.0/BETA) * math.exp(-r['aniso']),
    '1/β·(sg/mean_sp)': lambda r: (1.0/BETA) * (r['sg']/r['mean_sp']) if r['mean_sp']>0 else 1/BETA,
}

print(f"\n  {'定义':30s} {'βδ_v中位':>10s} {'1-βδ_v中位':>12s} {'Tc 2倍内':>10s} {'Tc中位%':>10s}")
print(f"  {'-'*75}")

for name, func in dv_defs.items():
    beta_dvs = []; tc_errs = []
    for r in valid:
        dv = func(r)
        if dv <= 0 or dv >= 1/BETA: continue
        beta_dvs.append(BETA * dv)
        tc_pred = arccoth_tc(r['dd0'], r['theta_d'], r['gn'], dv)
        if tc_pred > 0:
            tc_errs.append(sym_err(tc_pred, r['tc']))
    if not beta_dvs: continue
    beta_dvs.sort(); tc_errs.sort()
    med_bd = beta_dvs[len(beta_dvs)//2]
    med_om = 1 - med_bd
    med_err = tc_errs[len(tc_errs)//2] * 100 if tc_errs else 999
    w2 = sum(1 for e in tc_errs if e <= 1.0) / len(tc_errs) * 100 if tc_errs else 0
    print(f"  {name:30s} {med_bd:10.4f} {med_om:12.6f} {w2:10.1f} {med_err:10.1f}")

# ============================================================
print(f"\n{'='*70}")
print("2. 1-βδ_v的物理形式: 从C_mol谱直接预测")
print("="*70)

# 目标: 1-βδ_v = f(C_mol谱统计量)
# 从反推δ_v得到目标值
y = np.array([r['one_minus_reverse'] for r in valid])
y_log = np.log(y)

# 候选特征 (全部从C_mol谱导出, 不含K_eff)
feat_candidates = {
    'log(Δδ₀)': np.array([math.log(r['dd0']) for r in valid]),
    'log(γ_n-γ₁)': np.array([math.log(r['gn']-GAMMA_1) for r in valid]),
    'log(θ_D)': np.array([math.log(r['theta_d']) for r in valid]),
    'log(G)': np.array([math.log(r['G']) for r in valid]),
    'log(1/sg)': np.array([math.log(1.0/r['sg']) for r in valid]),
    'aniso': np.array([r['aniso'] for r in valid]),
    'log(cv_sp)': np.array([math.log(max(r['cv_sp'],1e-10)) for r in valid]),
    'log(sp_ratio)': np.array([math.log(r['sp_ratio']) for r in valid]),
    'log(spec_entropy)': np.array([math.log(max(r['spec_entropy'],1e-10)) for r in valid]),
    'log(delta3)': np.array([math.log(max(r['delta3'],1e-10)) for r in valid]),
    'log(n_sp)': np.array([math.log(r['n_sp']) for r in valid]),
    'inv_mass': np.array([r['af']['inv_mass'] for r in valid]),
    'dp': np.array([r['af']['dp'] for r in valid]),
    'o': np.array([r['af']['o'] for r in valid]),
}

# 逐步回归: 找最佳单特征, 然后加特征
from itertools import combinations

def ridge_fit(X, y, alpha=0.01):
    XtX = X.T @ X + alpha * np.eye(X.shape[1])
    return np.linalg.solve(XtX, X.T @ y)

def r2_score(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred)**2)
    ss_tot = np.sum((y_true - np.mean(y_true))**2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else 0

# 单特征R²
print(f"\n  单特征R² (预测log(1-βδ_v)):")
single_r2 = {}
for name, feat in feat_candidates.items():
    X = np.column_stack([np.ones(len(feat)), feat])
    coef = ridge_fit(X, y_log, 0.01)
    r2 = r2_score(y_log, X @ coef)
    single_r2[name] = r2
    print(f"    {name:25s}: R²={r2:.4f}")

# 前向逐步回归
print(f"\n  前向逐步回归:")
selected = []; remaining = list(feat_candidates.keys()); best_r2 = 0
for step in range(6):
    best_feat = None; best_step_r2 = best_r2
    for name in remaining:
        X = np.column_stack([np.ones(len(valid))] + [feat_candidates[n] for n in selected + [name]])
        coef = ridge_fit(X, y_log, 0.01)
        r2 = r2_score(y_log, X @ coef)
        if r2 > best_step_r2:
            best_step_r2 = r2; best_feat = name
    if best_feat:
        selected.append(best_feat); remaining.remove(best_feat); best_r2 = best_step_r2
        print(f"    步{step+1}: +{best_feat:25s} → R²={best_r2:.4f}")

# 最终模型
X_final = np.column_stack([np.ones(len(valid))] + [feat_candidates[n] for n in selected])
coef_final = ridge_fit(X_final, y_log, 0.01)
y_pred_final = X_final @ coef_final
r2_final = r2_score(y_log, y_pred_final)

print(f"\n  最终模型: R²={r2_final:.4f}")
print(f"  1-βδ_v = exp({coef_final[0]:.4f})", end="")
for i, name in enumerate(selected):
    print(f" · {name}^({coef_final[i+1]:.4f})", end="")
print()

# 验证Tc预测
errs = []
for i, r in enumerate(valid):
    one_minus = math.exp(y_pred_final[i])
    if one_minus <= 0 or one_minus >= 1: continue
    dv = (1 - one_minus) / BETA
    tc_pred = arccoth_tc(r['dd0'], r['theta_d'], r['gn'], dv)
    if tc_pred > 0:
        errs.append(sym_err(tc_pred, r['tc']))
if errs:
    errs.sort()
    print(f"  Tc预测: 中位{errs[len(errs)//2]*100:.1f}%  2倍内{sum(1 for e in errs if e<=1.0)/len(errs)*100:.1f}%")

# ============================================================
print(f"\n{'='*70}")
print("3. δ_v = 1/β - Δδ₀²·f(谱) 形式 (临界点展开)")
print("="*70)

# 1-βδ_v = β·(1/β - δ_v) = β·Δδ_v, 其中Δδ_v = 1/β - δ_v
# 所以 1-βδ_v = β·Δδ_v
# 从反推: Δδ_v = (1-βδ_v)/β
delta_dv = y / BETA  # Δδ_v = (1-βδ_v)/β
delta_dv_log = np.log(delta_dv)

print(f"  Δδ_v = 1/β - δ_v, 中位Δδ_v = {np.median(delta_dv):.6f}")
print(f"  Δδ_v/Δδ₀² 中位 = {np.median(delta_dv / np.array([r['dd0']**2 for r in valid])):.4f}")

# 检验 Δδ_v ∝ Δδ₀²·(γ_n-γ₁)^a
dd0_arr = np.array([r['dd0'] for r in valid])
gn_arr = np.array([r['gn']-GAMMA_1 for r in valid])
ratio = delta_dv / dd0_arr**2
print(f"  Δδ_v/Δδ₀² 范围: [{min(ratio):.4f}, {max(ratio):.4f}]")
print(f"  Δδ_v/Δδ₀²/θ_D 中位 = {np.median(ratio / np.array([r['theta_d'] for r in valid])):.6f}")

# 回归 Δδ_v = c·Δδ₀²·(γ_n-γ₁)^a·θ_D^b·G^c
X_dv = np.column_stack([
    np.ones(len(valid)),
    2*np.log(dd0_arr),
    np.log(gn_arr),
    np.log(np.array([r['theta_d'] for r in valid])),
    np.log(np.array([r['G'] for r in valid])),
])
coef_dv = ridge_fit(X_dv, delta_dv_log, 0.01)
r2_dv = r2_score(delta_dv_log, X_dv @ coef_dv)
print(f"\n  Δδ_v = c·Δδ₀²·(γ_n-γ₁)^a·θ_D^b·G^c")
print(f"  R² = {r2_dv:.4f}")
print(f"  c = {math.exp(coef_dv[0]):.6f}")
print(f"  a(γ_n-γ₁) = {coef_dv[2]:.4f}")
print(f"  b(θ_D) = {coef_dv[3]:.4f}")
print(f"  c(G) = {coef_dv[4]:.4f}")

# Tc预测
errs2 = []
y_pred_dv = X_dv @ coef_dv
for i, r in enumerate(valid):
    ddv = math.exp(y_pred_dv[i])
    dv = 1.0/BETA - ddv
    if dv <= 0: continue
    tc_pred = arccoth_tc(r['dd0'], r['theta_d'], r['gn'], dv)
    if tc_pred > 0:
        errs2.append(sym_err(tc_pred, r['tc']))
if errs2:
    errs2.sort()
    print(f"  Tc预测: 中位{errs2[len(errs2)//2]*100:.1f}%  2倍内{sum(1 for e in errs2 if e<=1.0)/len(errs2)*100:.1f}%")

# ============================================================
print(f"\n{'='*70}")
print("4. 按类别分析δ_v的C_mol谱预测")
print("="*70)

categories = {}
for r in valid:
    cat = r['cat']
    if cat not in categories: categories[cat] = []
    categories[cat].append(r)

for cat, recs in sorted(categories.items(), key=lambda x: -len(x[1])):
    if len(recs) < 3: continue
    errs_cat = []
    for r in recs:
        idx = next(j for j, v in enumerate(valid) if v['formula'] == r['formula'])
        one_minus = math.exp(y_pred_final[idx])
        if one_minus <= 0 or one_minus >= 1: continue
        dv = (1 - one_minus) / BETA
        tc_pred = arccoth_tc(r['dd0'], r['theta_d'], r['gn'], dv)
        if tc_pred > 0:
            errs_cat.append(sym_err(tc_pred, r['tc']))
    if errs_cat:
        errs_cat.sort()
        w2 = sum(1 for e in errs_cat if e <= 1.0) / len(errs_cat) * 100
        print(f"  {cat:20s} n={len(recs):3d}: 2倍内{w2:.0f}% 中位{errs_cat[len(errs_cat)//2]*100:.0f}%")

# ============================================================
print(f"\n{'='*70}")
print("5. 关键验证: 1-βδ_v ≈ 3β²Δδ₀²/[16(γ₂-γ₁)] (x≈1临界)")
print("="*70)

c_theory = 3 * BETA**2 / (16 * (GAMMA_2 - GAMMA_1))
print(f"  理论系数: 3β²/[16(γ₂-γ₁)] = 3·{BETA:.2f}²/[16·{GAMMA_2-GAMMA_1:.2f}] = {c_theory:.4f}")
print(f"  经验比值: β·Δδ_v/Δδ₀² 中位 = {np.median(delta_dv / dd0_arr**2)*BETA:.4f}")
print(f"  差异: {abs(c_theory - np.median(delta_dv / dd0_arr**2)*BETA)/c_theory*100:.1f}%")

# 逐材料验证
ratios_theory = []
for r in valid:
    one_minus_theory = c_theory * r['dd0']**2
    ratio = r['one_minus_reverse'] / one_minus_theory
    ratios_theory.append(ratio)
ratios_theory.sort()
print(f"\n  (1-βδ_v) / [3β²Δδ₀²/(16(γ₂-γ₁))] 分布:")
print(f"    中位 = {ratios_theory[len(ratios_theory)//2]:.4f}")
print(f"    范围 = [{ratios_theory[0]:.4f}, {ratios_theory[-1]:.4f}]")
print(f"    25%-75% = [{ratios_theory[len(ratios_theory)//4]:.4f}, {ratios_theory[3*len(ratios_theory)//4]:.4f}]")

# 用x≈1近似直接算Tc: Tc ≈ θ_D·√(1-βδ_v)·√(16(γ₂-γ₁)/(3β²Δδ₀²)) / 2
# 不对, x≈1时arccoth发散. 需要次阶修正.
# 从等价: arccoth(x)² = 9ln2·θ_D/(32Δδ₀²K_eff)
# x = coth(√(9ln2·θ_D/(32Δδ₀²K_eff)))
# 1-βδ_v = 3β²Δδ₀²/(16(γ₂-γ₁)·x)

print(f"\n  物理含义:")
print(f"    δ_v ≈ 1/β - 3β·Δδ₀²/[16(γ₂-γ₁)]")
print(f"    x = 3β²Δδ₀²/[16(1-βδ_v)(γ₂-γ₁)] ≈ 1 (临界同步)")
print(f"    Tc由次阶修正(通过K_eff)决定")
print(f"    δ_v不是独立参数 — 由Δδ₀(C_mol)主导!")