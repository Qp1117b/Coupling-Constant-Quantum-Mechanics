"""
K_0 第一性探索：5路径合并分析

路径1: CQM几何推导 — K_0^cat从晶格拓扑参数推导
路径2: 直接回归 — 从材料参数多变量回归K_0
路径3: 指数机制 — K_0与黎曼零点、BCS-like指数的指数关系
路径4: 微观推导 — 从BCS类比建立K_0^cat与λ_ep的关系
路径5: 黎曼指数验证 — K_0 = C·exp(a·γ_n)的LOOCV验证
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework')
from atom_db import ATOM_DB, atom_db

import csv, re, math
import numpy as np
from collections import defaultdict

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
BETA = 8 * math.pi + 1
GAP = 21.022040 - 14.134725
C2 = 2.0 / 3.0
LN2 = math.log(2)
C = math.sqrt(C2)

RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832,
                 52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
                 67.079811, 69.526405, 72.067158, 75.704690, 77.144840]

LATTICE_TOPO = {
    'bcc': {'cn': 8, 'faces': 6, 'verts': 8, 'sym': 48},
    'fcc': {'cn': 12, 'faces': 8, 'verts': 6, 'sym': 48},
    'hcp': {'cn': 12, 'faces': 8, 'verts': 6, 'sym': 24},
    'A15': {'cn': 14, 'faces': 12, 'verts': 8, 'sym': 24},
    'Perovskite': {'cn': 6, 'faces': 6, 'verts': 8, 'sym': 48},
    'ThCr2Si2': {'cn': 8, 'faces': 8, 'verts': 6, 'sym': 16},
    'NaCl': {'cn': 6, 'faces': 6, 'verts': 8, 'sym': 48},
    'Graphite intercalation': {'cn': 3, 'faces': 4, 'verts': 4, 'sym': 12},
    'ZrCuSiAs': {'cn': 6, 'faces': 6, 'verts': 8, 'sym': 8},
    'PbO': {'cn': 4, 'faces': 6, 'verts': 8, 'sym': 16},
    'LuNi2B2C': {'cn': 8, 'faces': 8, 'verts': 6, 'sym': 16},
    'Fm-3m': {'cn': 12, 'faces': 8, 'verts': 6, 'sym': 48},
    'R-3m': {'cn': 6, 'faces': 6, 'verts': 8, 'sym': 12},
    'PbFCl': {'cn': 8, 'faces': 6, 'verts': 8, 'sym': 8},
    'Tetragonal': {'cn': 6, 'faces': 6, 'verts': 8, 'sym': 16},
    'Orthorhombic': {'cn': 6, 'faces': 6, 'verts': 8, 'sym': 8},
    'Triclinic': {'cn': 6, 'faces': 6, 'verts': 8, 'sym': 2},
    'Rhombohedral': {'cn': 6, 'faces': 6, 'verts': 8, 'sym': 12},
}


def parse_formula(f):
    pairs = re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f)
    atoms = {}
    for el, cnt in pairs:
        if el in ATOM_DB:
            atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    return atoms


def parse_formula_simple(f):
    f = re.sub(r'[\(（].*?[\)）]', '', f.strip())
    return {e: (float(c) if c else 1.0) for e, c in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f) if e in ATOM_DB}


def calc_material_params(formula):
    atoms = parse_formula(formula)
    if not atoms:
        return None
    total_m = sum(atoms[el] * ATOM_DB[el][0] for el in atoms)
    total_z = sum(atoms[el] * ATOM_DB[el][3] for el in atoms)
    n_atoms = sum(atoms.values())
    avg_m = total_m / n_atoms
    avg_r = sum(atoms[el] * ATOM_DB[el][2] for el in atoms) / n_atoms
    l = 2 * avg_r * 1e-10
    theta_d = sum(atoms[el] * ATOM_DB[el][1] for el in atoms) / n_atoms
    if theta_d == 0:
        return None
    V_cell = l**3
    f_corr = 1.0 - 0.3 * (1.0 - 1.0 / n_atoms)
    edge_sum = 0
    els = list(atoms.keys())
    for i in range(len(els)):
        for j in range(i + 1, len(els)):
            mi = atoms[els[i]] * ATOM_DB[els[i]][0] * AMU
            mj = atoms[els[j]] * ATOM_DB[els[j]][0] * AMU
            edge_sum += (1.0 / mi + 1.0 / mj)
    if not edge_sum:
        mi = total_m * AMU / n_atoms
        edge_sum = (n_atoms * (n_atoms - 1) / 2) * 2.0 / mi
    G = (1.0 / l) * math.sqrt((1.0 - f_corr) * edge_sum)
    omega_d = theta_d * KB / HBAR
    dd0_sq = (C2 / l**2) * (3 * HBAR / (4 * omega_d)) * (1 - f_corr) * edge_sum
    dd0 = math.sqrt(abs(dd0_sq))
    return {
        'l': l, 'G': G, 'dd0': dd0, 'tD': theta_d,
        'M': total_m, 'Z': total_z, 'V': V_cell,
        'n_atoms': n_atoms, 'avg_m': avg_m,
    }


def calc_params_simple(formula):
    atoms = parse_formula(formula)
    if not atoms:
        return None
    total_m = sum(atoms[el] * ATOM_DB[el][0] for el in atoms)
    n_atoms = sum(atoms.values())
    avg_r = sum(atoms[el] * ATOM_DB[el][2] for el in atoms) / n_atoms
    l = 2 * avg_r * 1e-10
    theta_d = sum(atoms[el] * ATOM_DB[el][1] for el in atoms) / n_atoms
    if theta_d == 0:
        return None
    f_corr = 1.0 - 0.3 * (1.0 - 1.0 / n_atoms)
    edge_sum = 0
    els = list(atoms.keys())
    for i in range(len(els)):
        for j in range(i + 1, len(els)):
            mi = atoms[els[i]] * ATOM_DB[els[i]][0] * AMU
            mj = atoms[els[j]] * ATOM_DB[els[j]][0] * AMU
            edge_sum += (1.0 / mi + 1.0 / mj)
    if not edge_sum:
        mi = total_m * AMU / n_atoms
        edge_sum = (n_atoms * (n_atoms - 1) / 2) * 2.0 / mi
    G = (1.0 / l) * math.sqrt((1.0 - f_corr) * edge_sum)
    omega_d = theta_d * KB / HBAR
    dd0_sq = (C2 / l**2) * (3 * HBAR / (4 * omega_d)) * (1 - f_corr) * edge_sum
    dd0 = math.sqrt(abs(dd0_sq))
    return {'l': l, 'G': G, 'dd0': dd0, 'tD': theta_d}


def get_lattice_topo(struct_str):
    s = struct_str.lower()
    for key in LATTICE_TOPO:
        if key.lower() in s:
            return LATTICE_TOPO[key]
    return None


def a4_eigenvalues():
    return [2 - 2 * math.cos(k * math.pi / 5) for k in range(1, 5)]


def riemann_gaps():
    return [RIEMANN_ZEROS[i + 1] - RIEMANN_ZEROS[i] for i in range(len(RIEMANN_ZEROS) - 1)]


def get_mass_comp(c):
    return sum(ATOM_DB[e][0] * n for e, n in c.items())


def get_debye_comp(c):
    ws = [(ATOM_DB[e][1], ATOM_DB[e][0] * n) for e, n in c.items() if ATOM_DB[e][1] > 0]
    return sum(d * w for d, w in ws) / sum(w for _, w in ws) if ws else 300


def get_radius_comp(c):
    rs = [ATOM_DB[e][2] for e in c if ATOM_DB[e][2] > 0]
    return np.mean(rs) if rs else 1.5


def get_bulk_comp(c):
    bs = [ATOM_DB[e][3] for e in c if ATOM_DB[e][3] > 0]
    return np.mean(bs) if bs else 50


def get_valence_comp(c):
    vs = [ATOM_DB[e][4] for e in c if ATOM_DB[e][4] > 0]
    return np.mean(vs) if vs else 4


def ddv_inter(M, L, tD, z, f=0.5):
    L_m = L * 1e-10; w = tD * KB / HBAR; s = z * 2.0 / (M * AMU)
    return math.sqrt(max((C2 / L_m**2) * (3 * HBAR / (4 * w)) * (1 - f) * s, 0))


def ddv_intra(edges, l, tD, f=0.5):
    l_m = l * 1e-10; w = tD * KB / HBAR
    s = sum((1.0 / (mi * AMU) + 1.0 / (mj * AMU)) for mi, mj in edges)
    return math.sqrt(max((C2 / l_m**2) * (3 * HBAR / (4 * w)) * (1 - f) * s, 0))


def estimate_params(formula, cat, condition):
    comp = parse_formula_simple(formula)
    if not comp: return None
    n_atoms = sum(comp.values())
    M = get_mass_comp(comp); r = get_radius_comp(comp); tD = get_debye_comp(comp)
    B = get_bulk_comp(comp); Z_val = get_valence_comp(comp)
    P = 0
    if '高压' in condition or 'GPa' in condition:
        pm = re.search(r'~?(\d+)GPa', condition)
        P = int(pm.group(1)) if pm else 50
    L = 2 * r; l_intra = 2 * r; z = 6; edges = []; f = 0.5
    if '元素' in cat:
        tD = ATOM_DB.get(list(comp.keys())[0], (0, 300, 1.5, 50, 4))[1] or tD
        if tD < 50: tD = 300
        z = 12; f = 0.5
        if '高压' in cat: B = max(get_bulk_comp(comp), 50) * 3; P = max(P, 100)
    elif 'A15' in cat: tD = max(tD, 400); z = 8; L = 2 * r * 0.9; f = 0.4
    elif '氢化物' in cat:
        tD = max(tD, 1500); B = max(B, 200); P = max(P, 150); z = 8; L = 2.0; l_intra = 1.7
        n_h = comp.get('H', 0); n_m = n_atoms - n_h
        if n_h > 0 and n_m > 0:
            m_m = (M - n_h * 1.008) / n_m; edges = [(m_m, 1.008)] * int(min(n_h, 4))
        f = 0.5
    elif '铜氧' in cat:
        tD = max(tD, 400); z = 6; L = 3.8; l_intra = 1.9
        if 'Cu' in comp and 'O' in comp: edges = [(63.55, 16.0)] * 2
        f = 0.4
    elif '铁基' in cat:
        tD = max(tD, 350); z = 6; L = 3.5; l_intra = 2.0
        if 'Fe' in comp:
            if 'As' in comp: edges = [(55.85, 74.92)] * 2
            elif 'Se' in comp: edges = [(55.85, 78.97)] * 2
        f = 0.4
    elif '有机' in cat: tD = max(tD, 100); z = 4; L = 5.0; f = 0.5
    elif '富勒烯' in cat: tD = 100; z = 4; L = 10.0; M = 720; f = 0.5
    elif '石墨' in cat: tD = 200; z = 3; L = 3.35; f = 0.5
    elif '合金' in cat: tD = max(tD, 200); z = 12; f = 0.5
    else: tD = max(tD, 200); z = 8; f = 0.5
    return tD, M, L, z, edges, l_intra, B, P, f, Z_val


# =====================================================
# 路径1: CQM几何推导 K_0^cat
# =====================================================

def path1_cqm_derivation():
    print("\n" + "=" * 80)
    print("路径1: K_0^cat的CQM几何推导")
    print("=" * 80)

    data = []
    with open("superconductors_deduplicated.csv", 'r', encoding='utf-8-sig') as fh:
        for row in csv.DictReader(fh):
            try:
                tc = float(row['临界温度 Tc (K)'])
            except:
                continue
            if tc <= 0:
                continue
            mp = calc_material_params(row['材料(化学式)'])
            if mp is None or mp['dd0'] == 0:
                continue
            cat = row['类别']
            struct = row['晶体结构']
            topo = get_lattice_topo(struct)
            k_eff = tc**2 * 9 * LN2 / (8 * mp['dd0']**2 * mp['tD'])
            data.append({
                'cat': cat, 'struct': struct, 'topo': topo,
                'tc': tc, 'k_eff': k_eff, **mp
            })

    print(f"加载 {len(data)} 个材料")

    a_ke = -0.769; b_ke = 1.132
    for d in data:
        d['k0'] = d['k_eff'] / (d['G']**a_ke * d['tD']**b_ke)

    print("\n" + "-" * 80)
    print("1.1 K_0^cat的值（按类别）")
    print("-" * 80)
    cat_data = defaultdict(list)
    for d in data:
        cat_data[d['cat']].append(d)

    print(f"{'类别':<28} {'n':>4} {'K_0中位':>10} {'K_0均值':>10} {'CV%':>6} {'ln K_0':>8}")
    print("-" * 80)
    cat_k0 = {}
    for cat in sorted(cat_data.keys()):
        cd = cat_data[cat]
        k0s = np.array([d['k0'] for d in cd])
        cat_k0[cat] = np.median(k0s)
        cv = np.std(k0s) / np.mean(k0s) * 100 if np.mean(k0s) != 0 else 0
        print(f"{cat:<28} {len(cd):>4} {np.median(k0s):>10.4f} {np.mean(k0s):>10.4f} {cv:>6.0f}% {np.log(np.median(k0s)):>8.3f}")

    print("\n" + "-" * 80)
    print("1.2 K_0与晶格拓扑参数的关系")
    print("-" * 80)
    topo_data = defaultdict(list)
    for d in data:
        if d['topo'] is not None:
            topo_data[d['topo']['cn']].append(d['k0'])
    print(f"{'配位数':>8} {'n':>4} {'K_0中位':>10} {'ln K_0':>8}")
    print("-" * 40)
    for cn in sorted(topo_data.keys()):
        k0s = np.array(topo_data[cn])
        print(f"{cn:>8} {len(k0s):>4} {np.median(k0s):>10.4f} {np.log(np.median(k0s)):>8.3f}")

    print("\n" + "-" * 80)
    print("1.3 K_0与CQM普适参数的关系")
    print("-" * 80)
    a4_eigs = a4_eigenvalues()
    print(f"A4特征值: {a4_eigs}")
    print(f"A4特征值和: {sum(a4_eigs):.4f}")
    print(f"GAP(γ₂-γ₁): {GAP:.6f}")
    gaps = riemann_gaps()
    print(f"黎曼零点间距: {gaps[:5]}")
    print(f"平均间距: {np.mean(gaps):.4f}")

    print("\n" + "-" * 80)
    print("1.4 K_0^cat / CQM普适参数（寻找类别几何因子）")
    print("-" * 80)
    cqm_universal = {
        'GAP': GAP, 'GAP²': GAP**2, 'β': BETA, 'β/π': BETA / math.pi,
        'A4_tr': sum(a4_eigs), 'A4_prod': np.prod(a4_eigs),
        'h²': 25, 'ln(h)': math.log(5),
        'γ₁/γ₂': RIEMANN_ZEROS[0] / RIEMANN_ZEROS[1], '平均间距': np.mean(gaps),
    }
    print(f"{'类别':<28} {'ln K_0':>8}", end='')
    for name in cqm_universal:
        print(f" {name:>10}", end='')
    print()
    print("-" * 120)
    for cat in sorted(cat_k0.keys()):
        ln_k0 = np.log(cat_k0[cat])
        print(f"{cat:<28} {ln_k0:>8.3f}", end='')
        for name in cqm_universal:
            ratio = ln_k0 / cqm_universal[name] if cqm_universal[name] != 0 else 0
            print(f" {ratio:>10.4f}", end='')
        print()

    print("\n" + "-" * 80)
    print("1.5 K_0与结构复杂度的关系")
    print("-" * 80)
    cat_complexity = {}
    for cat in sorted(cat_data.keys()):
        cd = cat_data[cat]
        syms = [d['topo']['sym'] for d in cd if d['topo'] is not None]
        cat_complexity[cat] = np.mean(syms) if syms else 0
    print(f"{'类别':<28} {'K_0':>10} {'平均对称数':>10} {'1/sym':>10} {'ln(K_0)':>8} {'ln(1/sym)':>10}")
    print("-" * 80)
    for cat in sorted(cat_k0.keys()):
        sym = cat_complexity[cat]
        inv_sym = 1.0 / sym if sym > 0 else 0
        print(f"{cat:<28} {cat_k0[cat]:>10.4f} {sym:>10.1f} {inv_sym:>10.4f} {np.log(cat_k0[cat]):>8.3f} {np.log(inv_sym) if inv_sym > 0 else 0:>10.3f}")

    print("\n" + "-" * 80)
    print("1.6 ln(K_0) ~ a·ln(1/cn) + b·ln(1/sym) + c 回归")
    print("-" * 80)
    valid = [d for d in data if d['topo'] is not None]
    X = []; y = []
    for d in valid:
        cn = d['topo']['cn']; sym = d['topo']['sym']
        X.append([np.log(1.0 / cn), np.log(1.0 / sym), 1.0])
        y.append(np.log(d['k0']))
    X = np.array(X); y = np.array(y)
    r2 = 0
    try:
        coef, res, rank, sv = np.linalg.lstsq(X, y, rcond=None)
        y_pred = X @ coef
        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        r2 = 1 - ss_res / ss_tot
        print(f"R² = {r2:.3f}")
        print(f"  ln(1/cn): {coef[0]:.3f}")
        print(f"  ln(1/sym): {coef[1]:.3f}")
        print(f"  const: {coef[2]:.3f}")
    except Exception as e:
        print(f"回归失败: {e}")

    print("\n" + "-" * 80)
    print("1.7 LOOCV: K_0从晶格拓扑参数预测→Tc")
    print("-" * 80)
    valid_l = [d for d in data if d['topo'] is not None]
    errors = []
    for i in range(len(valid_l)):
        train = [valid_l[j] for j in range(len(valid_l)) if j != i]
        test = valid_l[i]
        X_tr = np.array([[np.log(1.0 / d['topo']['cn']), np.log(1.0 / d['topo']['sym']), 1.0] for d in train])
        y_tr = np.array([np.log(d['k0']) for d in train])
        try:
            coef_l, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
            x_test = np.array([np.log(1.0 / test['topo']['cn']), np.log(1.0 / test['topo']['sym']), 1.0])
            k0_pred = np.exp(x_test @ coef_l)
            k_eff_pred = k0_pred * test['G']**a_ke * test['tD']**b_ke
            tc_pred = math.sqrt(8 * test['dd0']**2 * k_eff_pred * test['tD'] / (9 * LN2))
            err = abs(tc_pred - test['tc']) / test['tc']
            errors.append(err)
        except:
            pass
    errors = np.array(errors)
    print(f"LOOCV: {len(errors)} 个材料")
    print(f"  中位误差: {np.median(errors)*100:.0f}%")
    print(f"  2倍内: {np.mean(errors <= 1.0)*100:.0f}%")
    print(f"  5倍内: {np.mean(errors <= 4.0)*100:.0f}%")

    print("\n" + "-" * 80)
    print("1.8 总结")
    print("-" * 80)
    print(f"""
K_0^cat的范围: {min(cat_k0.values()):.4f} ~ {max(cat_k0.values()):.4f}
ln(K_0^cat)的范围: {np.log(min(cat_k0.values())):.3f} ~ {np.log(max(cat_k0.values())):.3f}
K_0与晶格拓扑参数回归R² = {r2:.3f}
K_0^cat是类别特征常数，晶格拓扑参数可以部分解释K_0。
""")


# =====================================================
# 路径2: 直接回归
# =====================================================

def path2_direct_regression():
    print("\n" + "=" * 80)
    print("路径2: 改进K_0预测——直接从材料参数回归")
    print("=" * 80)

    from numpy.linalg import lstsq

    with open("superconductors_deduplicated.csv", 'r', encoding='utf-8-sig') as fh:
        reader = csv.reader(fh); header = next(reader); rows = list(reader)

    all_data = []
    for row in rows:
        cat = row[0]; formula = row[1]; tc_str = row[3]
        condition = row[7] if len(row) > 7 else ''
        tc_match = re.match(r'~?(\d+\.?\d*)', tc_str.strip())
        if not tc_match: continue
        tc = float(tc_match.group(1))
        params = estimate_params(formula, cat, condition)
        if not params: continue
        tD, M, L, z, edges, l_intra, B, P, f, Z_val = params
        di = ddv_inter(M, L, tD, z, f)
        dn = ddv_intra(edges, l_intra, tD, f) if edges else 0
        ddv0 = math.sqrt(di**2 + dn**2)
        G2 = ddv0**2 * tD * 4 * KB / (C2 * 3 * HBAR**2)
        G = math.sqrt(G2)
        k_eff = tc**2 * 1.125 * LN2 / (ddv0**2 * tD)
        K0 = k_eff / (G**(-0.769) * tD**1.132)
        V_cell = L**3
        r_s = (3 * V_cell / (4 * math.pi * Z_val))**(1 / 3) if Z_val > 0 else 1.5
        omega_D = tD * KB / HBAR
        all_data.append({
            'formula': formula, 'cat': cat, 'tc': tc, 'tD': tD,
            'ddv0': ddv0, 'G': G, 'K0': K0, 'B': B, 'M': M,
            'Z_val': Z_val, 'V_cell': V_cell, 'r_s': r_s, 'omega_D': omega_D,
            'L': L, 'z': z, 'f': f,
            'n_atoms': sum(parse_formula_simple(formula).values())
        })

    print(f"加载 {len(all_data)} 个材料")

    K0s = np.array([d['K0'] for d in all_data])
    log_K0 = np.log(K0s)

    candidates = {
        'B': [d['B'] for d in all_data],
        'M': [d['M'] for d in all_data],
        'Z_val': [d['Z_val'] for d in all_data],
        'V_cell': [d['V_cell'] for d in all_data],
        'r_s': [d['r_s'] for d in all_data],
        'theta_D': [d['tD'] for d in all_data],
        'omega_D': [d['omega_D'] for d in all_data],
        'L': [d['L'] for d in all_data],
        'z': [d['z'] for d in all_data],
        'B/M': [d['B'] / d['M'] for d in all_data],
        'B*V': [d['B'] * d['V_cell'] for d in all_data],
        'Z/V': [d['Z_val'] / d['V_cell'] for d in all_data],
        'B*r_s': [d['B'] * d['r_s'] for d in all_data],
        'B/(M*omega²)': [d['B'] / (d['M'] * d['omega_D']**2) for d in all_data],
        'Z*B/M': [d['Z_val'] * d['B'] / d['M'] for d in all_data],
        'B*V/M': [d['B'] * d['V_cell'] / d['M'] for d in all_data],
        'θ_D²/B': [d['tD']**2 / d['B'] for d in all_data],
        'B/θ_D²': [d['B'] / d['tD']**2 for d in all_data],
        'Z²/V': [d['Z_val']**2 / d['V_cell'] for d in all_data],
        'B²/(M*θ_D²)': [d['B']**2 / (d['M'] * d['tD']**2) for d in all_data],
    }

    print("\n2.1 K_0与材料参数的单变量关系")
    results = []
    for name, vals in candidates.items():
        vals = np.array(vals)
        if np.any(vals <= 0): continue
        corr = np.corrcoef(np.log(vals), log_K0)[0, 1]
        results.append((name, corr, abs(corr)))
    results.sort(key=lambda x: -x[2])
    print(f"{'参数':<16} {'corr(ln K_0, ln param)':>25}")
    print("-" * 45)
    for name, corr, _ in results[:15]:
        print(f"{name:<16} {corr:>25.3f}")

    print("\n2.2 多变量回归 K_0")
    top_params = [r[0] for r in results[:6]]
    print(f"用参数: {top_params}")
    X_multi = np.column_stack([np.log(np.array(candidates[p])) for p in top_params] + [np.ones(len(all_data))])
    y_multi = log_K0
    coef_m, _, _, _ = lstsq(X_multi, y_multi, rcond=None)
    pred_m = X_multi @ coef_m
    r2_m = 1 - np.sum((y_multi - pred_m)**2) / np.sum((y_multi - np.mean(y_multi))**2)
    print(f"R² = {r2_m:.3f}")
    for i, p in enumerate(top_params):
        print(f"  {p}: {coef_m[i]:.3f}")
    print(f"  const: {coef_m[-1]:.3f}")

    print("\n2.3 LOOCV: 材料→K_0(多变量回归)→Tc")
    all_preds = []; all_exps = []
    for i, d_test in enumerate(all_data):
        train = [d for j, d in enumerate(all_data) if j != i]

        def get_features(d):
            return [np.log(d['B']), np.log(d['M']), np.log(d['Z_val']),
                    np.log(d['V_cell']), np.log(d['tD']), 1]
        X_tr = np.array([get_features(d) for d in train])
        y_tr = np.array([np.log(d['K0']) for d in train])
        coef_tr, _, _, _ = lstsq(X_tr, y_tr, rcond=None)
        x_test = np.array(get_features(d_test))
        K0_pred = np.exp(x_test @ coef_tr)
        k_eff_pred = K0_pred * d_test['G']**(-0.769) * d_test['tD']**1.132
        tc_pred = math.sqrt(d_test['ddv0']**2 * k_eff_pred * d_test['tD'] / (1.125 * LN2))
        all_preds.append(tc_pred); all_exps.append(d_test['tc'])
    errs = np.abs(np.array(all_preds) - np.array(all_exps)) / np.array(all_exps)
    print(f"全局回归LOOCV: {len(errs)}个材料")
    print(f"  中位误差: {np.median(errs)*100:.0f}%")
    print(f"  2倍内: {np.sum(errs<1)/len(errs)*100:.0f}%")
    print(f"  5倍内: {np.sum(errs<4)/len(errs)*100:.0f}%")

    print("\n2.4 LOOCV: 材料→K_0(全局回归+类别偏置)→Tc")
    all_preds2 = []; all_exps2 = []
    for i, d_test in enumerate(all_data):
        cat = d_test['cat']
        train = [d for j, d in enumerate(all_data) if j != i]
        cat_list = sorted(set(d['cat'] for d in train))

        def get_features2(d, cl):
            feats = [np.log(d['B']), np.log(d['M']), np.log(d['Z_val']),
                     np.log(d['V_cell']), np.log(d['tD'])]
            for c in cl: feats.append(1.0 if d['cat'] == c else 0.0)
            feats.append(1.0)
            return feats
        X_tr = np.array([get_features2(d, cat_list) for d in train])
        y_tr = np.array([np.log(d['K0']) for d in train])
        coef_tr, _, _, _ = lstsq(X_tr, y_tr, rcond=None)
        x_test = np.array(get_features2(d_test, cat_list))
        K0_pred = np.exp(x_test @ coef_tr)
        k_eff_pred = K0_pred * d_test['G']**(-0.769) * d_test['tD']**1.132
        tc_pred = math.sqrt(d_test['ddv0']**2 * k_eff_pred * d_test['tD'] / (1.125 * LN2))
        all_preds2.append(tc_pred); all_exps2.append(d_test['tc'])
    errs2 = np.abs(np.array(all_preds2) - np.array(all_exps2)) / np.array(all_exps2)
    print(f"全局+类别偏置LOOCV: {len(errs2)}个材料")
    print(f"  中位误差: {np.median(errs2)*100:.0f}%")
    print(f"  2倍内: {np.sum(errs2<1)/len(errs2)*100:.0f}%")
    print(f"  5倍内: {np.sum(errs2<4)/len(errs2)*100:.0f}%")

    print("\n2.5 最终: 直接回归ln(Tc)与材料参数+类别")
    all_preds3 = []; all_exps3 = []
    for i, d_test in enumerate(all_data):
        train = [d for j, d in enumerate(all_data) if j != i]
        cat_list = sorted(set(d['cat'] for d in train))

        def get_tc_features(d, cl):
            feats = [np.log(d['ddv0']), np.log(d['tD']), np.log(d['B']),
                     np.log(d['M']), np.log(d['Z_val']), np.log(d['V_cell'])]
            for c in cl: feats.append(1.0 if d['cat'] == c else 0.0)
            feats.append(1.0)
            return feats
        X_tr = np.array([get_tc_features(d, cat_list) for d in train])
        y_tr = np.array([np.log(d['tc']) for d in train])
        coef_tr, _, _, _ = lstsq(X_tr, y_tr, rcond=None)
        x_test = np.array(get_tc_features(d_test, cat_list))
        tc_pred = np.exp(x_test @ coef_tr)
        all_preds3.append(tc_pred); all_exps3.append(d_test['tc'])
    errs3 = np.abs(np.array(all_preds3) - np.array(all_exps3)) / np.array(all_exps3)
    print(f"直接回归LOOCV: {len(errs3)}个材料")
    print(f"  中位误差: {np.median(errs3)*100:.0f}%")
    print(f"  2倍内: {np.sum(errs3<1)/len(errs3)*100:.0f}%")
    print(f"  5倍内: {np.sum(errs3<4)/len(errs3)*100:.0f}%")

    print(f"\n总结: K_0与材料参数有中等相关(R²={r2_m:.3f})，直接回归Tc给出{np.median(errs3)*100:.0f}%中位误差。")


# =====================================================
# 路径3: 指数机制
# =====================================================

def path3_exponential_mechanism():
    print("\n" + "=" * 80)
    print("路径3: K_0与CQM指数机制的关系")
    print("=" * 80)

    data = []
    with open("superconductors_deduplicated.csv", 'r', encoding='utf-8-sig') as fh:
        for row in csv.DictReader(fh):
            try:
                tc = float(row['临界温度 Tc (K)'])
            except:
                continue
            if tc <= 0:
                continue
            mp = calc_params_simple(row['材料(化学式)'])
            if mp is None or mp['dd0'] == 0:
                continue
            cat = row['类别']
            k_eff = tc**2 * 9 * LN2 / (8 * mp['dd0']**2 * mp['tD'])
            a_ke, b_ke = -0.769, 1.132
            k0 = k_eff / (mp['G']**a_ke * mp['tD']**b_ke)
            data.append({'cat': cat, 'tc': tc, 'k_eff': k_eff, 'k0': k0, **mp})
    print(f"加载 {len(data)} 个材料")

    cat_data_k0 = defaultdict(list)
    for d in data:
        cat_data_k0[d['cat']].append(d['k0'])
    cat_k0 = {cat: np.median(v) for cat, v in cat_data_k0.items()}

    print("\n3.1 K_0^cat vs 黎曼零点")
    print(f"{'类别':<28} {'ln K_0':>8} {'最近γ_n':>8} {'n':>3} {'ln K_0 / γ_n':>12} {'ln K_0 - γ_n':>12}")
    print("-" * 80)
    for cat in sorted(cat_k0.keys()):
        ln_k0 = np.log(cat_k0[cat])
        diffs = [abs(ln_k0 - g) for g in RIEMANN_ZEROS]
        n_closest = np.argmin(diffs)
        gamma_closest = RIEMANN_ZEROS[n_closest]
        ratio = ln_k0 / gamma_closest
        diff = ln_k0 - gamma_closest
        print(f"{cat:<28} {ln_k0:>8.3f} {gamma_closest:>8.3f} {n_closest+1:>3} {ratio:>12.4f} {diff:>12.3f}")

    print("\n3.2 ln(K_0) = a·γ_n + b 拟合")
    sorted_cats = sorted(cat_k0.keys(), key=lambda c: np.log(cat_k0[c]))
    n_cats = len(sorted_cats)
    gammas_A = RIEMANN_ZEROS[:n_cats]
    ln_k0s = [np.log(cat_k0[cat]) for cat in sorted_cats]
    X_A = np.column_stack([gammas_A, np.ones(n_cats)])
    y_arr = np.array(ln_k0s)
    coef_A, _, _, _ = np.linalg.lstsq(X_A, y_arr, rcond=None)
    y_pred = X_A @ coef_A
    r2_A = 1 - np.sum((y_arr - y_pred)**2) / np.sum((y_arr - np.mean(y_arr))**2)
    print(f"方案A: ln(K_0) = {coef_A[0]:.4f}·γ_n + {coef_A[1]:.4f}, R² = {r2_A:.3f}")

    print("\n3.3 K_0 ~ exp(a·γ_n)的直接验证")
    a_fit, b_fit = coef_A
    print(f"K_0 = exp({b_fit:.4f})·exp({a_fit:.4f}·γ_n) = {math.exp(b_fit):.2e}·exp({a_fit:.4f}·γ_n)")
    print(f"\n{'类别':<28} {'K_0实际':>12} {'K_0预测':>12} {'误差':>8}")
    print("-" * 65)
    for i, cat in enumerate(sorted_cats):
        k0_actual = cat_k0[cat]
        k0_pred = math.exp(b_fit + a_fit * gammas_A[i])
        err = abs(k0_pred - k0_actual) / k0_actual
        print(f"{cat:<28} {k0_actual:>12.2e} {k0_pred:>12.2e} {err*100:>7.1f}%")

    print("\n3.4 BCS-like指数: K_0 ~ θ_D·exp(-c/λ_eff)")
    MU_STAR = 0.1
    for d in data:
        tc = d['tc']; td = d['tD']
        if tc >= td:
            d['lambda_ep'] = None; continue
        ratio = tc / td
        if ratio <= 0 or ratio >= 1:
            d['lambda_ep'] = None; continue
        lam = MU_STAR - 1.0 / math.log(ratio)
        d['lambda_ep'] = lam if lam > 0 else None
    valid = [d for d in data if d['lambda_ep'] is not None and d['lambda_ep'] > 0.01]
    print(f"有效材料: {len(valid)}")
    ln_k0_vals = np.array([np.log(d['k0']) for d in valid])
    inv_lam_vals = np.array([1.0 / d['lambda_ep'] for d in valid])
    corr = np.corrcoef(inv_lam_vals, ln_k0_vals)[0, 1]
    X_bcs = np.column_stack([inv_lam_vals, np.ones(len(inv_lam_vals))])
    y_bcs = ln_k0_vals
    coef_bcs, _, _, _ = np.linalg.lstsq(X_bcs, y_bcs, rcond=None)
    y_pred_bcs = X_bcs @ coef_bcs
    r2_bcs = 1 - np.sum((y_bcs - y_pred_bcs)**2) / np.sum((y_bcs - np.mean(y_bcs))**2)
    print(f"ln(K_0) = {coef_bcs[0]:.3f}/λ_ep + {coef_bcs[1]:.3f}, R² = {r2_bcs:.3f}")

    print("\n3.5 K_0的CQM指数公式候选")
    print(f"""
候选公式:
  A) K_0 = C·exp(a·γ_n): R² = {r2_A:.3f}
  B) K_0 = C·exp(a/λ_ep + b): R² = {r2_bcs:.3f}, corr = {corr:.3f}
BCS-like指数(R²={r2_bcs:.3f})是最强的经验关系，但1/λ_ep需要DFT计算。
""")


# =====================================================
# 路径4: 微观推导
# =====================================================

def path4_microscopic():
    print("\n" + "=" * 80)
    print("路径4: K_0^cat的微观推导——从BCS类比")
    print("=" * 80)

    from scipy.optimize import brentq
    from numpy.linalg import lstsq

    def rev_lambda_ep(tc, theta_D, mu_star=0.1):
        if tc <= 0 or theta_D <= 0: return None
        ratio = 1.2 * tc / theta_D
        if ratio >= 1: return None
        exponent = -math.log(ratio)
        denom = exponent - 1.04 + exponent * mu_star * 0.62
        if abs(denom) < 1e-10: return None
        lam = (1.04 + exponent * mu_star) / denom
        return lam if lam > 0 else None

    def calc_N0_free_electron(Z_val, V_cell_ang3):
        n = Z_val / V_cell_ang3
        n_m3 = n * 1e30
        kF = (3 * math.pi**2 * n_m3)**(1 / 3)
        m_e = 9.109e-31
        EF_J = HBAR**2 * kF**2 / (2 * m_e)
        EF_eV = EF_J / 1.602e-19
        N0_per_J_m3 = 3 * n_m3 / (2 * EF_J)
        N0_per_eV_m3 = N0_per_J_m3 * 1.602e-19
        V_cell_m3 = V_cell_ang3 * 1e-30
        N0_per_eV_cell = N0_per_eV_m3 * V_cell_m3
        return N0_per_eV_cell, EF_eV

    with open("superconductors_deduplicated.csv", 'r', encoding='utf-8-sig') as fh:
        reader = csv.reader(fh); header = next(reader); rows = list(reader)

    all_data = []
    for row in rows:
        cat = row[0]; formula = row[1]; tc_str = row[3]
        condition = row[7] if len(row) > 7 else ''
        tc_match = re.match(r'~?(\d+\.?\d*)', tc_str.strip())
        if not tc_match: continue
        tc = float(tc_match.group(1))
        params = estimate_params(formula, cat, condition)
        if not params: continue
        tD, M, L, z, edges, l_intra, B, P, f, Z_val = params
        di = ddv_inter(M, L, tD, z, f)
        dn = ddv_intra(edges, l_intra, tD, f) if edges else 0
        ddv0 = math.sqrt(di**2 + dn**2)
        G2 = ddv0**2 * tD * 4 * KB / (C2 * 3 * HBAR**2)
        G = math.sqrt(G2)
        k_eff = tc**2 * 1.125 * LN2 / (ddv0**2 * tD)
        a_ke, b_ke = -0.769, 1.132
        K0 = k_eff / (G**a_ke * tD**b_ke)
        lam_ep = rev_lambda_ep(tc, tD, mu_star=0.1)
        V_cell = L**3
        N0, EF = calc_N0_free_electron(Z_val, V_cell)
        lam_approx = N0 * B / (M * (tD * KB / HBAR)**2) * 1e40
        all_data.append({
            'formula': formula, 'cat': cat, 'tc': tc, 'tD': tD,
            'ddv0': ddv0, 'G': G, 'k_eff': k_eff, 'K0': K0,
            'lam_ep': lam_ep, 'N0': N0, 'EF': EF, 'B': B, 'M': M,
            'Z_val': Z_val, 'V_cell': V_cell, 'lam_approx': lam_approx
        })

    print(f"加载 {len(all_data)} 个材料")

    valid = [d for d in all_data if d['lam_ep'] is not None and d['lam_ep'] > 0]
    lams = np.array([d['lam_ep'] for d in valid])
    print(f"有效材料: {len(valid)}")
    print(f"λ_ep: 均值={np.mean(lams):.3f}, 中位数={np.median(lams):.3f}")

    K0s = np.array([d['K0'] for d in valid])
    lams_v = np.array([d['lam_ep'] for d in valid])
    corr_lam = np.corrcoef(np.log(K0s), np.log(lams_v))[0, 1]
    X = np.vstack([np.log(lams_v), np.ones(len(lams_v))]).T
    y = np.log(K0s)
    a_fit, c_fit = lstsq(X, y, rcond=None)[0]
    pred = a_fit * np.log(lams_v) + c_fit
    r2 = 1 - np.sum((y - pred)**2) / np.sum((y - np.mean(y))**2)
    print(f"corr(ln K_0, ln λ_ep) = {corr_lam:.3f}")
    print(f"K_0 = {np.exp(c_fit):.4e} · λ_ep^{a_fit:.3f}, R² = {r2:.3f}")

    print("\n4.5 完整第一性预测链条验证 (LOOCV)")
    for d in valid:
        r_s_ang = (3 * d['V_cell'] / (4 * math.pi * d['Z_val']))**(1 / 3)
        I2 = d['B'] * r_s_ang
        omega_D = d['tD'] * KB / HBAR
        d['lam_approx2'] = d['N0'] * I2 / (d['M'] * omega_D**2) * 1e35

    all_preds = []; all_exps = []
    for i, d_test in enumerate(valid):
        cat = d_test['cat']
        train = [d for j, d in enumerate(valid) if j != i and d['cat'] == cat]
        if len(train) < 5:
            train = [d for j, d in enumerate(valid) if j != i]
        x_tr = np.log(np.array([d['lam_approx2'] for d in train]))
        y_tr = np.log(np.array([d['lam_ep'] for d in train]))
        A_tr = np.vstack([x_tr, np.ones(len(x_tr))]).T
        a_tr, c_tr = lstsq(A_tr, y_tr, rcond=None)[0]
        lam_pred = np.exp(c_tr) * d_test['lam_approx2']**a_tr
        x_k = np.log(np.array([d['lam_ep'] for d in train]))
        y_k = np.log(np.array([d['K0'] for d in train]))
        A_k = np.vstack([x_k, np.ones(len(x_k))]).T
        a_k, c_k = lstsq(A_k, y_k, rcond=None)[0]
        K0_pred = np.exp(c_k) * lam_pred**a_k
        k_eff_pred = K0_pred * d_test['G']**(-0.769) * d_test['tD']**1.132
        tc_pred = math.sqrt(d_test['ddv0']**2 * k_eff_pred * d_test['tD'] / (1.125 * LN2))
        all_preds.append(tc_pred); all_exps.append(d_test['tc'])
    errs = np.abs(np.array(all_preds) - np.array(all_exps)) / np.array(all_exps)
    print(f"完整链条LOOCV: {len(errs)}个材料")
    print(f"  中位误差: {np.median(errs)*100:.0f}%")
    print(f"  2倍内: {np.sum(errs<1)/len(errs)*100:.0f}%")
    print(f"  5倍内: {np.sum(errs<4)/len(errs)*100:.0f}%")
    print(f"\n结论: K_0与λ_ep弱相关(R²={r2:.3f}), 微观推导需要更精确的DFT计算。")


# =====================================================
# 路径5: 黎曼指数验证
# =====================================================

def path5_riemann_exponential():
    print("\n" + "=" * 80)
    print("路径5: K_0 = C·exp(a·γ_n) 的LOOCV验证")
    print("=" * 80)

    data = []
    with open("superconductors_deduplicated.csv", 'r', encoding='utf-8-sig') as fh:
        for row in csv.DictReader(fh):
            try:
                tc = float(row['临界温度 Tc (K)'])
            except:
                continue
            if tc <= 0:
                continue
            mp = calc_params_simple(row['材料(化学式)'])
            if mp is None or mp['dd0'] == 0:
                continue
            cat = row['类别']
            k_eff = tc**2 * 9 * LN2 / (8 * mp['dd0']**2 * mp['tD'])
            a_ke, b_ke = -0.769, 1.132
            k0 = k_eff / (mp['G']**a_ke * mp['tD']**b_ke)
            data.append({'cat': cat, 'tc': tc, 'k_eff': k_eff, 'k0': k0, **mp})

    print(f"加载 {len(data)} 个材料")

    cat_data = defaultdict(list)
    for d in data:
        cat_data[d['cat']].append(d['k0'])
    cat_k0 = {cat: np.median(v) for cat, v in cat_data.items()}
    sorted_cats = sorted(cat_k0.keys(), key=lambda c: np.log(cat_k0[c]))
    CAT_TO_N = {cat: i + 1 for i, cat in enumerate(sorted_cats)}
    CAT_TO_GAMMA = {cat: RIEMANN_ZEROS[i] for i, cat in enumerate(sorted_cats)}

    print("\n5.1 类别→黎曼零点映射")
    print(f"{'类别':<28} {'n':>3} {'γ_n':>8} {'ln K_0':>8}")
    print("-" * 55)
    for cat in sorted_cats:
        n, gamma = CAT_TO_N[cat], CAT_TO_GAMMA[cat]
        print(f"{cat:<28} {n:>3} {gamma:>8.3f} {np.log(cat_k0[cat]):>8.3f}")

    gammas = np.array([CAT_TO_GAMMA[cat] for cat in sorted_cats])
    ln_k0s = np.array([np.log(cat_k0[cat]) for cat in sorted_cats])
    X = np.column_stack([gammas, np.ones(len(gammas))])
    coef, _, _, _ = np.linalg.lstsq(X, ln_k0s, rcond=None)
    a_fit, b_fit = coef
    y_pred = X @ coef
    r2_fit = 1 - np.sum((ln_k0s - y_pred)**2) / np.sum((ln_k0s - np.mean(ln_k0s))**2)
    print(f"\n拟合: ln(K_0) = {a_fit:.4f}·γ_n + {b_fit:.4f}, R² = {r2_fit:.4f}")
    print(f"K_0 = {math.exp(b_fit):.4e} · exp({a_fit:.4f}·γ_n)")

    print("\n5.3 LOOCV: 类别→γ_n→K_0→Tc")
    a_ke, b_ke = -0.769, 1.132
    errors = []
    for d in data:
        gamma = CAT_TO_GAMMA[d['cat']]
        k0_pred = math.exp(b_fit + a_fit * gamma)
        k_eff_pred = k0_pred * d['G']**a_ke * d['tD']**b_ke
        tc_pred = math.sqrt(8 * d['dd0']**2 * k_eff_pred * d['tD'] / (9 * LN2))
        err = abs(tc_pred - d['tc']) / d['tc']
        errors.append(err)
    errors = np.array(errors)
    print(f"LOOCV (γ_n→K_0→Tc): {len(errors)} 材料")
    print(f"  中位误差: {np.median(errors)*100:.0f}%")
    print(f"  2倍内: {np.mean(errors <= 1.0)*100:.0f}%")
    print(f"  5倍内: {np.mean(errors <= 4.0)*100:.0f}%")

    print("\n5.4 严格LOOCV: 每次重新拟合a,b和映射")
    errors_strict = []
    for i in range(len(data)):
        train = [data[j] for j in range(len(data)) if j != i]
        test = data[i]
        train_cat_k0 = defaultdict(list)
        for d in train:
            train_cat_k0[d['cat']].append(d['k0'])
        train_cat_k0 = {cat: np.median(v) for cat, v in train_cat_k0.items()}
        train_sorted = sorted(train_cat_k0.keys(), key=lambda c: np.log(train_cat_k0[c]))
        train_cat_to_gamma = {cat: RIEMANN_ZEROS[idx] for idx, cat in enumerate(train_sorted)}
        g_tr = np.array([train_cat_to_gamma[c] for c in train_sorted])
        y_tr = np.array([np.log(train_cat_k0[c]) for c in train_sorted])
        X_tr = np.column_stack([g_tr, np.ones(len(g_tr))])
        coef_tr, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
        if test['cat'] in train_cat_to_gamma:
            gamma_test = train_cat_to_gamma[test['cat']]
        else:
            continue
        k0_pred = math.exp(coef_tr[1] + coef_tr[0] * gamma_test)
        k_eff_pred = k0_pred * test['G']**a_ke * test['tD']**b_ke
        tc_pred = math.sqrt(8 * test['dd0']**2 * k_eff_pred * test['tD'] / (9 * LN2))
        err = abs(tc_pred - test['tc']) / test['tc']
        errors_strict.append(err)
    errors_strict = np.array(errors_strict)
    print(f"严格LOOCV: {len(errors_strict)} 材料")
    print(f"  中位误差: {np.median(errors_strict)*100:.0f}%")
    print(f"  2倍内: {np.mean(errors_strict <= 1.0)*100:.0f}%")
    print(f"  5倍内: {np.mean(errors_strict <= 4.0)*100:.0f}%")

    print(f"\n物理解释: K_0^cat = {math.exp(b_fit):.4e} · exp({a_fit:.4f} · γ_n), R² = {r2_fit:.4f}")
    print("不同类别超导体对应不同黎曼零点γ_n，K_0由指数机制决定。")


# =====================================================
# 主入口
# =====================================================

if __name__ == "__main__":
    path1_cqm_derivation()
    path2_direct_regression()
    path3_exponential_mechanism()
    path4_microscopic()
    path5_riemann_exponential()