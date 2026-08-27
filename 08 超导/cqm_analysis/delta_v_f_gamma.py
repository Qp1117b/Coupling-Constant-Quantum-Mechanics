"""分析 1-βδ_v / Δδ₀² 与 γ_n 的精确关系

发现: 当γ_n固定时, 1-βδ_v ≈ c·Δδ₀² (corr=0.973)
=> 1-βδ_v = Δδ₀² · f(γ_n)

求f(γ_n)的精确形式
"""
import sys, os, math, csv, re
import numpy as np

sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework')
from atom_db import ATOM_DB

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
C2 = 2.0/3.0; LN2 = math.log(2)
BETA = 8 * math.pi + 1
RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832,
                 52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
                 67.079811, 69.526405, 72.067158, 75.704690, 77.144840]
GAMMA_1 = RIEMANN_ZEROS[0]

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

def gamma_n_map(C_mol, af):
    ev = np.sort(np.linalg.eigvalsh(C_mol))
    if len(ev) < 2: return RIEMANN_ZEROS[0], 1.0
    sg = max(ev[1]-ev[0], 0.05); m = np.mean(ev); aniso = np.std(ev/m if m > 0 else ev)
    nc = 4.00 + 0.50*math.log(1/sg) + 0.35*aniso + 13.0*af['inv_mass'] + 0.05*af['dp'] + 5.5*af['o']
    ni = int(nc); frac = nc - ni
    if ni < 1: return RIEMANN_ZEROS[0], nc
    if ni >= len(RIEMANN_ZEROS): return 2*math.pi*nc/math.log(nc/(2*math.pi)) if nc > 6 else RIEMANN_ZEROS[-1], nc
    return RIEMANN_ZEROS[ni-1] + frac*(RIEMANN_ZEROS[ni]-RIEMANN_ZEROS[ni-1]), nc

def parse(f):
    atoms = {}
    for el, cnt in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f):
        if el in ATOM_DB: atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    return atoms

def phys_quantities(atoms):
    els = list(atoms.keys()); n_atoms = sum(atoms.values())
    avg_r = sum(atoms[el]*ATOM_DB[el][2] for el in els)/n_atoms
    l = 2*avg_r*1e-10; L = 2*max(ATOM_DB[el][2] for el in els)*1e-10
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
    total_m = sum(atoms[el]*ATOM_DB[el][0] for el in els)*AMU
    inter = 2*8/total_m; omega_d = theta_d*KB/HBAR
    dd0_i = (C2/l**2)*(3*HBAR/(4*omega_d))*(1-f_corr)*es
    dd0_e = (C2/L**2)*(3*HBAR/(4*omega_d))*(1-f_corr)*inter
    dd0 = math.sqrt(abs(dd0_i + dd0_e))
    G = (1/l)*math.sqrt((1-f_corr)*es)
    return dd0, theta_d, G

def run():
    data = []
    with open(os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv'), 'r', encoding='utf-8-sig') as fh:
        for row in csv.DictReader(fh):
            try: tc = float(row['临界温度 Tc (K)'])
            except: continue
            if tc > 0: data.append({'f': row['材料(化学式)'], 'cat': row['类别'], 'tc': tc})

    print(f"加载 {len(data)} 个材料\n")

    results = []
    for d in data:
        atoms = parse(d['f'])
        if not atoms: continue
        C, _ = build_Cmol(atoms); af = atom_features(atoms)
        gn, nc = gamma_n_map(C, af); pq = phys_quantities(atoms)
        if pq is None: continue
        dd0, theta_d, G = pq
        n = max(2.0, nc); dgamma = gn - GAMMA_1
        if dgamma <= 0: continue

        arg = theta_d / (2 * d['tc'])
        if arg < 0.01: continue
        x = 1.0 / math.tanh(arg)
        if x <= 1: continue
        one_minus_bdv = BETA**2*(n**2-1)*dd0**2 / (4*n**2*x*dgamma)
        if one_minus_bdv <= 0 or one_minus_bdv > 1: continue

        # f(γ_n) = (1-βδ_v) / Δδ₀²
        f_gamma = one_minus_bdv / dd0**2 if dd0 > 0 else 0

        results.append({
            'f': d['f'], 'cat': d['cat'], 'tc': d['tc'],
            'one_minus_bdv': one_minus_bdv, 'f_gamma': f_gamma,
            'dd0': dd0, 'gn': gn, 'G': G, 'theta_d': theta_d, 'n': n,
            'dgamma': dgamma, 'x': x,
        })

    print(f"有效: {len(results)}\n")

    # f(γ_n) = (1-βδ_v) / Δδ₀² 的分布
    fgs = [r['f_gamma'] for r in results]
    fgs.sort()
    print(f"=== f(γ_n) = (1-βδ_v)/Δδ₀² 统计 ===")
    print(f"  范围: [{fgs[0]:.2f}, {fgs[-1]:.2f}]")
    print(f"  中位: {fgs[len(fgs)//2]:.2f}")

    # f(γ_n) vs γ_n
    print(f"\n=== f(γ_n) vs γ_n 相关性 ===")
    gns = np.array([r['gn'] for r in results])
    fgs_arr = np.array([r['f_gamma'] for r in results])
    corr = np.corrcoef(gns, fgs_arr)[0, 1]
    print(f"  corr(f(γ_n), γ_n) = {corr:.4f}")

    # log-log
    log_gn = np.log(gns); log_fg = np.log(fgs_arr)
    A = np.vstack([log_gn, np.ones(len(log_gn))]).T
    slope, intercept = np.linalg.lstsq(A, log_fg, rcond=None)[0]
    r2 = 1 - np.sum((log_fg - (slope*log_gn + intercept))**2) / np.sum((log_fg - np.mean(log_fg))**2)
    print(f"  f(γ_n) = {math.exp(intercept):.4f} * γ_n^{slope:.3f}, R²={r2:.3f}")

    # f(γ_n) vs (γ_n - γ_1)
    print(f"\n=== f(γ_n) vs (γ_n - γ₁) ===")
    dgams = np.array([r['dgamma'] for r in results])
    corr2 = np.corrcoef(dgams, fgs_arr)[0, 1]
    print(f"  corr(f, γ_n-γ₁) = {corr2:.4f}")
    log_dg = np.log(dgams)
    A2 = np.vstack([log_dg, np.ones(len(log_dg))]).T
    slope2, intercept2 = np.linalg.lstsq(A2, log_fg, rcond=None)[0]
    r2_2 = 1 - np.sum((log_fg - (slope2*log_dg + intercept2))**2) / np.sum((log_fg - np.mean(log_fg))**2)
    print(f"  f = {math.exp(intercept2):.4f} * (γ_n-γ₁)^{slope2:.3f}, R²={r2_2:.3f}")

    # f(γ_n) vs exp(a*γ_n)
    print(f"\n=== f(γ_n) vs exp(0.369·γ_n) ===")
    exps = np.array([math.exp(0.369*r['gn']) for r in results])
    corr3 = np.corrcoef(exps, fgs_arr)[0, 1]
    print(f"  corr(f, exp(0.369·γ_n)) = {corr3:.4f}")
    log_exp = np.log(exps)
    A3 = np.vstack([log_exp, np.ones(len(log_exp))]).T
    slope3, intercept3 = np.linalg.lstsq(A3, log_fg, rcond=None)[0]
    r2_3 = 1 - np.sum((log_fg - (slope3*log_exp + intercept3))**2) / np.sum((log_fg - np.mean(log_fg))**2)
    print(f"  f = {math.exp(intercept3):.4f} * exp(0.369·γ_n)^{slope3:.3f}, R²={r2_3:.3f}")

    # f(γ_n) vs n
    print(f"\n=== f(γ_n) vs n ===")
    ns = np.array([r['n'] for r in results])
    corr4 = np.corrcoef(ns, fgs_arr)[0, 1]
    print(f"  corr(f, n) = {corr4:.4f}")

    # f(γ_n) vs n²
    ns2 = ns**2
    corr5 = np.corrcoef(ns2, fgs_arr)[0, 1]
    print(f"  corr(f, n²) = {corr5:.4f}")

    # f(γ_n) vs (n²-1)/n²
    ns_ratio = (ns**2 - 1) / ns**2
    corr6 = np.corrcoef(ns_ratio, fgs_arr)[0, 1]
    print(f"  corr(f, (n²-1)/n²) = {corr6:.4f}")

    # f(γ_n) vs (n²-1)/(n²·(γ_n-γ₁))
    ns_dgamma = (ns**2 - 1) / (ns**2 * dgams)
    corr7 = np.corrcoef(ns_dgamma, fgs_arr)[0, 1]
    print(f"  corr(f, (n²-1)/(n²·(γ_n-γ₁))) = {corr7:.4f}")

    # f(γ_n) vs β²(n²-1)/(4n²(γ_n-γ₁))
    theory_f = BETA**2 * (ns**2 - 1) / (4 * ns**2 * dgams)
    corr8 = np.corrcoef(theory_f, fgs_arr)[0, 1]
    print(f"  corr(f, β²(n²-1)/(4n²(γ_n-γ₁))) = {corr8:.4f}")

    # 散点
    print(f"\n=== 散点: f(γ_n) vs γ_n ===")
    for r in sorted(results, key=lambda x: x['gn'])[:8]:
        print(f"  γ={r['gn']:.1f}: {r['f']:<16} f={r['f_gamma']:.2f} 1-βδ_v={r['one_minus_bdv']:.4e} Δδ₀={r['dd0']:.4f}")
    print("  ...")
    for r in sorted(results, key=lambda x: x['gn'])[-8:]:
        print(f"  γ={r['gn']:.1f}: {r['f']:<16} f={r['f_gamma']:.2f} 1-βδ_v={r['one_minus_bdv']:.4e} Δδ₀={r['dd0']:.4f}")

    # 关键: 1-βδ_v = Δδ₀² · f(γ_n), 找到f(γ_n)后可以:
    # 1. 从C_mol计算Δδ₀和γ_n
    # 2. δ_v = (1/β)·[1 - Δδ₀²·f(γ_n)]
    # 3. 代入arccoth闭式计算Tc
    # 如果f(γ_n) = c·(γ_n-γ₁)^alpha, 则:
    # 1-βδ_v = c·Δδ₀²·(γ_n-γ₁)^alpha

    print(f"\n=== 最终关系 ===")
    print(f"  1-βδ_v = Δδ₀² · f(γ_n)")
    print(f"  f(γ_n) = {math.exp(intercept2):.4f} · (γ_n-γ₁)^{slope2:.3f}, R²={r2_2:.3f}")
    print(f"  => 1-βδ_v = {math.exp(intercept2):.4f} · Δδ₀² · (γ_n-γ₁)^{slope2:.3f}")
    print(f"  => δ_v = (1/β)·[1 - {math.exp(intercept2):.4f}·Δδ₀²·(γ_n-γ₁)^{slope2:.3f}]")

    # 验证: 用这个δ_v公式代入arccoth闭式
    print(f"\n=== 验证: 用δ_v公式代入arccoth闭式 ===")
    c_val = math.exp(intercept2)
    alpha_val = slope2

    errors = []
    for r in results:
        # δ_v from formula
        dv_formula = (1.0/BETA) * (1 - c_val * r['dd0']**2 * r['dgamma']**alpha_val)
        if dv_formula <= 0: continue
        one_minus_bdv_formula = 1 - BETA * dv_formula
        if one_minus_bdv_formula <= 0: continue

        # arccoth闭式
        x_pred = BETA**2 * (r['n']**2-1) * r['dd0']**2 / (4 * r['n']**2 * one_minus_bdv_formula * r['dgamma'])
        if x_pred <= 1: continue
        ac = 0.5 * math.log((x_pred + 1) / (x_pred - 1))
        if ac <= 0: continue
        tc_pred = r['theta_d'] / (2 * ac)

        # 抑制
        atoms = parse(r['f'])
        af = atom_features(atoms)
        tc_pred *= math.exp(-15.0 * af['f']) * math.exp(-3.0 * af['d0'])

        if tc_pred > 0:
            err = max(tc_pred/r['tc'], r['tc']/tc_pred) - 1
            errors.append(err)

    if errors:
        errors.sort()
        med = errors[len(errors)//2] * 100
        w2 = sum(1 for e in errors if e <= 1.0) / len(errors) * 100
        w5 = sum(1 for e in errors if e <= 4.0) / len(errors) * 100
        print(f"  arccoth闭式(δ_v公式): 中位{med:.1f}% 2倍内{w2:.1f}% 5倍内{w5:.1f}% ({len(errors)}个)")
        print(f"  对比自由能公式: 中位98.0% 2倍内50.8% 5倍内73.8%")

if __name__ == '__main__':
    run()