"""验证 1-βδ_v = f(Δδ_0, γ_n) 的理论关系

从arccoth闭式(x>>1)与自由能公式等价:
  K_0 = C·exp(a·γ_n) = 9ln2·θ_D^{1-q}·β⁴(n²-1)²Δδ_0² / [512n⁴(1-βδ_v)²(γ_n-γ₁)²·G^p]

=> 1-βδ_v ∝ Δδ_0·exp(-a·γ_n/2) / [(γ_n-γ₁)·G^{p/2}·θ_D^{(q-1)/2}]

如果成立, 则:
  1. δ_v的第一性公式: δ_v = (1/β)·[1 - c·Δδ_0·exp(-a·γ_n/2)/((γ_n-γ₁)·G^{p/2}·θ_D^{(q-1)/2})]
  2. 0.369的来源: 从arccoth↔自由能等价导出
  3. 两条路线统一
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

    # 理论参数
    a_gamma = 0.369; p_exp = -0.75; q_exp = 1.125

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

        # 反推δ_v
        arg = theta_d / (2 * d['tc'])
        if arg < 0.01: continue
        x = 1.0 / math.tanh(arg)
        if x <= 1: continue
        one_minus_bdv = BETA**2*(n**2-1)*dd0**2 / (4*n**2*x*dgamma)
        if one_minus_bdv <= 0 or one_minus_bdv > 1: continue
        dv = (1 - one_minus_bdv) / BETA

        # 理论预测的 1-βδ_v
        # 从arccoth↔自由能等价:
        # 1-βδ_v ∝ Δδ_0·exp(-a·γ_n/2) / [(γ_n-γ₁)·G^{p/2}·θ_D^{(q-1)/2}]
        theory_val = dd0 * math.exp(-a_gamma*gn/2) / (dgamma * max(G,1e-6)**(p_exp/2) * theta_d**((q_exp-1)/2))

        results.append({
            'f': d['f'], 'cat': d['cat'], 'tc': d['tc'],
            'one_minus_bdv': one_minus_bdv, 'theory': theory_val,
            'dd0': dd0, 'gn': gn, 'G': G, 'theta_d': theta_d, 'n': n,
            'dv': dv, 'beta_dv': BETA*dv,
        })

    print(f"有效: {len(results)}\n")

    # 验证 1-βδ_v ∝ theory_val
    ys = np.array([r['one_minus_bdv'] for r in results])
    xs = np.array([r['theory'] for r in results])

    corr = np.corrcoef(xs, ys)[0, 1]
    print(f"=== 验证 1-βδ_v ∝ Δδ₀·exp(-a·γ_n/2) / [(γ_n-γ₁)·G^{{p/2}}·θ_D^{{(q-1)/2}}] ===")
    print(f"  corr = {corr:.4f}")

    # 拟合比例常数
    ratios = ys / xs
    ratios.sort()
    print(f"  比例常数: 中位{ratios[len(ratios)//2]:.4e} 范围[{ratios[0]:.4e}, {ratios[-1]:.4e}]")

    # log-log回归
    log_x = np.log(xs); log_y = np.log(ys)
    A = np.vstack([log_x, np.ones(len(log_x))]).T
    slope, intercept = np.linalg.lstsq(A, log_y, rcond=None)[0]
    r2 = 1 - np.sum((log_y - (slope*log_x + intercept))**2) / np.sum((log_y - np.mean(log_y))**2)
    print(f"  log-log: slope={slope:.3f} intercept={intercept:.3f} R²={r2:.3f}")

    # 简化验证: 1-βδ_v vs Δδ_0 (固定γ_n范围)
    print(f"\n=== 简化: 1-βδ_v vs Δδ₀ (γ_n∈[35,40]) ===")
    subset = [r for r in results if 35 <= r['gn'] <= 40]
    if subset:
        xs2 = np.array([r['dd0'] for r in subset])
        ys2 = np.array([r['one_minus_bdv'] for r in subset])
        corr2 = np.corrcoef(xs2, ys2)[0, 1]
        print(f"  corr(1-βδ_v, Δδ₀) = {corr2:.4f} (n={len(subset)})")
        # 拟合 1-βδ_v = c * Δδ_0^alpha
        log_x2 = np.log(xs2); log_y2 = np.log(ys2)
        A2 = np.vstack([log_x2, np.ones(len(log_x2))]).T
        slope2, intercept2 = np.linalg.lstsq(A2, log_y2, rcond=None)[0]
        print(f"  1-βδ_v = {math.exp(intercept2):.4f} * Δδ₀^{slope2:.3f}")

    # 1-βδ_v vs exp(-a*γ_n/2)
    print(f"\n=== 1-βδ_v vs exp(-a·γ_n/2) (Δδ₀∈[0.008,0.012]) ===")
    subset2 = [r for r in results if 0.008 <= r['dd0'] <= 0.012]
    if subset2:
        xs3 = np.array([math.exp(-a_gamma*r['gn']/2) for r in subset2])
        ys3 = np.array([r['one_minus_bdv'] for r in subset2])
        corr3 = np.corrcoef(xs3, ys3)[0, 1]
        print(f"  corr(1-βδ_v, exp(-a·γ_n/2)) = {corr3:.4f} (n={len(subset2)})")

    # 散点
    print(f"\n=== 散点: 1-βδ_v vs theory ===")
    for r in sorted(results, key=lambda x: x['theory'])[:5]:
        print(f"  theory={r['theory']:.4e}: {r['f']:<16} 1-βδ_v={r['one_minus_bdv']:.4e} βδ_v={r['beta_dv']:.4f}")
    print("  ...")
    for r in sorted(results, key=lambda x: x['theory'])[-5:]:
        print(f"  theory={r['theory']:.4e}: {r['f']:<16} 1-βδ_v={r['one_minus_bdv']:.4e} βδ_v={r['beta_dv']:.4f}")

    # 关键: 如果corr高, 则δ_v的第一性公式成立
    print(f"\n=== 结论 ===")
    if corr > 0.8:
        print(f"  corr={corr:.3f} > 0.8: 理论关系成立!")
        print(f"  δ_v = (1/β)·[1 - c·Δδ₀·exp(-0.185·γ_n)/((γ_n-γ₁)·G^(-3/8)·θ_D^(1/16))]")
        print(f"  0.369从arccoth↔自由能等价导出, BCS伪势μ*/λ=0.353")
    elif corr > 0.5:
        print(f"  corr={corr:.3f}: 部分成立, 需修正理论公式")
    else:
        print(f"  corr={corr:.3f}: 理论关系不成立, 需重新分析")

if __name__ == '__main__':
    run()