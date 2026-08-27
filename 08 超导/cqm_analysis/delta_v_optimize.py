"""优化δ_v公式: 分析x分布和残差

发现: f(γ_n) = (1-βδ_v)/Δδ₀² 与 (n²-1)/(n²·(γ_n-γ₁)) corr=0.968
=> 1-βδ_v ≈ c·Δδ₀²·(n²-1)/(n²·(γ_n-γ₁))·g(其他特征)

arccoth闭式(δ_v公式)给出2倍内44.4%, 优化目标: 超过50.8%
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

        results.append({
            'f': d['f'], 'cat': d['cat'], 'tc': d['tc'],
            'one_minus_bdv': one_minus_bdv, 'dd0': dd0, 'gn': gn,
            'G': G, 'theta_d': theta_d, 'n': n, 'dgamma': dgamma, 'x': x,
            'af': af,
        })

    print(f"有效: {len(results)}\n")

    # x分布
    xs = [r['x'] for r in results]
    xs.sort()
    print(f"=== x = coth(θ_D/(2·Tc)) 分布 ===")
    print(f"  范围: [{xs[0]:.4f}, {xs[-1]:.4f}]")
    print(f"  中位: {xs[len(xs)//2]:.4f}")
    print(f"  1/3分位: {xs[len(xs)//3]:.4f}, 2/3分位: {xs[2*len(xs)//3]:.4f}")

    # 1-βδ_v = Δδ₀²·β²(n²-1) / [4n²·x·(γ_n-γ₁)]
    # 如果x ≈ const, 则 1-βδ_v ∝ Δδ₀²·(n²-1)/(n²·(γ_n-γ₁))
    # 检查 x vs 各种特征
    print(f"\n=== x vs 特征 ===")
    for feat_name, feat_func in [
        ('γ_n', lambda r: r['gn']),
        ('n', lambda r: r['n']),
        ('Δδ₀', lambda r: r['dd0']),
        ('θ_D', lambda r: r['theta_d']),
        ('G', lambda r: r['G']),
        ('inv_mass', lambda r: r['af']['inv_mass']),
        ('Tc', lambda r: r['tc']),
    ]:
        vals = np.array([feat_func(r) for r in results])
        xarr = np.array([r['x'] for r in results])
        if np.std(vals) < 1e-10: continue
        c = np.corrcoef(vals, xarr)[0, 1]
        print(f"  corr(x, {feat_name}) = {c:+.3f}")

    # 关键: 1-βδ_v / [Δδ₀²·(n²-1)/(n²·(γ_n-γ₁))] = β²/(4x)
    # => 4x/β² = (n²-1)/(n²·(γ_n-γ₁)) / [(1-βδ_v)/Δδ₀²]
    # 如果这个比值是常数, 则x是常数
    ratios = []
    for r in results:
        denom = r['dd0']**2 * (r['n']**2-1) / (r['n']**2 * r['dgamma'])
        if denom > 0:
            ratio = r['one_minus_bdv'] / denom  # = β²/(4x)
            ratios.append(ratio)

    ratios.sort()
    print(f"\n=== (1-βδ_v) / [Δδ₀²·(n²-1)/(n²·(γ_n-γ₁))] = β²/(4x) ===")
    print(f"  范围: [{ratios[0]:.4f}, {ratios[-1]:.4f}]")
    print(f"  中位: {ratios[len(ratios)//2]:.4f}")
    print(f"  β²/4 = {BETA**2/4:.1f}")
    print(f"  => x中位 = β²/(4·中位) = {BETA**2/(4*ratios[len(ratios)//2]):.4f}")

    # 优化: 1-βδ_v = c·Δδ₀^a · (γ_n-γ₁)^b · θ_D^d · G^e
    print(f"\n=== 多变量幂律拟合 1-βδ_v ===")
    # log(1-βδ_v) = log(c) + a·log(Δδ₀) + b·log(γ_n-γ₁) + d·log(θ_D) + e·log(G)
    X = []
    y = []
    for r in results:
        if r['one_minus_bdv'] <= 0 or r['dd0'] <= 0 or r['G'] <= 0: continue
        row = [1, math.log(r['dd0']), math.log(r['dgamma']), math.log(r['theta_d']), math.log(r['G'])]
        X.append(row)
        y.append(math.log(r['one_minus_bdv']))

    X = np.array(X); y = np.array(y)
    # Ridge
    lam = 0.01
    XtX = X.T @ X + lam * np.eye(X.shape[1])
    beta = np.linalg.solve(XtX, X.T @ y)
    y_pred = X @ beta
    r2 = 1 - np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2)
    print(f"  R² = {r2:.3f}")
    print(f"  1-βδ_v = {math.exp(beta[0]):.4f} · Δδ₀^{beta[1]:.3f} · (γ_n-γ₁)^{beta[2]:.3f} · θ_D^{beta[3]:.3f} · G^{beta[4]:.3f}")

    # 用这个公式验证arccoth闭式
    c_opt = math.exp(beta[0]); a_opt = beta[1]; b_opt = beta[2]; d_opt = beta[3]; e_opt = beta[4]

    errors = []
    for r in results:
        ombdv = c_opt * r['dd0']**a_opt * r['dgamma']**b_opt * r['theta_d']**d_opt * r['G']**e_opt
        if ombdv <= 0 or ombdv >= 1: continue
        x_pred = BETA**2 * (r['n']**2-1) * r['dd0']**2 / (4 * r['n']**2 * ombdv * r['dgamma'])
        if x_pred <= 1: continue
        ac = 0.5 * math.log((x_pred + 1) / (x_pred - 1))
        if ac <= 0: continue
        tc_pred = r['theta_d'] / (2 * ac)
        tc_pred *= math.exp(-15.0 * r['af']['f']) * math.exp(-3.0 * r['af']['d0'])
        if tc_pred > 0:
            err = max(tc_pred/r['tc'], r['tc']/tc_pred) - 1
            errors.append((err, r, tc_pred))

    if errors:
        errs = [e[0] for e in errors]
        errs.sort()
        med = errs[len(errs)//2] * 100
        w2 = sum(1 for e in errs if e <= 1.0) / len(errs) * 100
        w5 = sum(1 for e in errs if e <= 4.0) / len(errs) * 100
        print(f"\n  arccoth闭式(优化δ_v): 中位{med:.1f}% 2倍内{w2:.1f}% 5倍内{w5:.1f}% ({len(errs)}个)")
        print(f"  对比自由能公式: 中位98.0% 2倍内50.8% 5倍内73.8%")

        # 按类别
        print(f"\n  按类别:")
        cats = sorted(set(e[1]['cat'] for e in errors))
        for cat in cats:
            subset = [e for e in errors if e[1]['cat'] == cat]
            if len(subset) < 3: continue
            ce = sorted([e[0] for e in subset])
            m = ce[len(ce)//2] * 100
            w = sum(1 for e in ce if e <= 1.0) / len(ce) * 100
            print(f"    {cat:<25} 中位{m:.0f}% 2倍内{w:.0f}% ({len(subset)})")

        # 最好/最差
        errors.sort(key=lambda x: x[0])
        print(f"\n  最好10:")
        for err, r, tc_pred in errors[:10]:
            print(f"    {r['f']:<16} exp={r['tc']:>7.1f}K pred={tc_pred:>7.1f}K err={err*100:.0f}%")
        print(f"  最差10:")
        for err, r, tc_pred in errors[-10:]:
            print(f"    {r['f']:<16} exp={r['tc']:>7.1f}K pred={tc_pred:>7.1f}K err={err*100:.0f}%")

if __name__ == '__main__':
    run()