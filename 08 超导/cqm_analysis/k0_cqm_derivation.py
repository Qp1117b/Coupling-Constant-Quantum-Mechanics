"""
K_0的CQM几何推导尝试

K_0^cat是曲率刚度的类别常数。
在CQM中，曲率来自Regge剖分的角亏。
不同类别的超导体有不同的晶格结构→不同的Regge剖分→不同的K_0。

尝试从CQM几何参数导出K_0:
1. 晶格类型 → Regge剖分拓扑 → K_0
2. 配位数/结构复杂度 → K_0
3. CQM普适参数（黎曼零点、A4群）× 类别几何因子 → K_0
"""

import csv, re, math
import numpy as np
from collections import defaultdict

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
BETA = 8 * math.pi + 1
GAP = 21.022040 - 14.134725
C2 = 2.0 / 3.0
LN2 = math.log(2)
C = math.sqrt(C2)

ATOM_DB = {
    'H': (1.008, 0, 0.46, 0), 'He': (4.003, 0, 0.31, 0),
    'Li': (6.94, 344, 1.52, 11), 'Be': (9.01, 1440, 1.12, 130),
    'B': (10.81, 1480, 0.87, 185), 'C': (12.01, 2230, 0.77, 338),
    'N': (14.01, 0, 0.75, 0), 'O': (16.00, 0, 0.73, 0),
    'F': (19.00, 0, 0.72, 0), 'Ne': (20.18, 0, 0.71, 0),
    'Na': (22.99, 158, 1.86, 7), 'Mg': (24.31, 400, 1.60, 35),
    'Al': (26.98, 428, 1.43, 76), 'Si': (28.09, 645, 1.18, 100),
    'P': (30.97, 0, 1.10, 0), 'S': (32.06, 0, 1.05, 0),
    'Cl': (35.45, 0, 1.02, 0), 'K': (39.10, 91, 2.27, 3),
    'Ca': (40.08, 230, 1.97, 15), 'Sc': (44.96, 360, 1.62, 44),
    'Ti': (47.87, 420, 1.47, 110), 'V': (50.94, 383, 1.34, 162),
    'Cr': (52.00, 435, 1.28, 160), 'Mn': (54.94, 410, 1.27, 120),
    'Fe': (55.85, 470, 1.26, 170), 'Co': (58.93, 445, 1.25, 180),
    'Ni': (58.69, 450, 1.24, 180), 'Cu': (63.55, 343, 1.28, 140),
    'Zn': (65.38, 327, 1.34, 70), 'Ga': (69.72, 240, 1.35, 40),
    'Ge': (72.63, 374, 1.22, 75), 'As': (74.92, 0, 1.21, 0),
    'Se': (78.97, 0, 1.20, 0), 'Br': (79.90, 0, 1.20, 0),
    'Rb': (85.47, 56, 2.48, 2), 'Sr': (87.62, 147, 2.15, 12),
    'Y': (88.91, 280, 1.80, 37), 'Zr': (91.22, 291, 1.60, 95),
    'Nb': (92.91, 275, 1.46, 170), 'Mo': (95.96, 425, 1.39, 230),
    'Tc': (98.00, 0, 1.36, 0), 'Ru': (101.07, 0, 1.34, 220),
    'Rh': (102.91, 0, 1.34, 150), 'Pd': (106.42, 274, 1.37, 180),
    'Ag': (107.87, 215, 1.44, 100), 'Cd': (112.41, 209, 1.49, 42),
    'In': (114.82, 108, 1.62, 11), 'Sn': (118.71, 200, 1.58, 50),
    'Sb': (121.76, 0, 1.61, 0), 'Te': (127.60, 0, 1.60, 0),
    'I': (126.90, 0, 1.63, 0), 'Cs': (132.91, 38, 2.65, 2),
    'Ba': (137.33, 110, 2.22, 9), 'La': (138.91, 142, 1.87, 24),
    'Ce': (140.12, 0, 1.82, 22), 'Pr': (140.91, 0, 1.82, 21),
    'Nd': (144.24, 0, 1.82, 20), 'Sm': (150.36, 0, 1.81, 18),
    'Eu': (151.96, 0, 1.81, 8), 'Gd': (157.25, 0, 1.80, 25),
    'Tb': (158.93, 0, 1.79, 25), 'Dy': (162.50, 0, 1.79, 25),
    'Ho': (164.93, 0, 1.78, 26), 'Er': (167.26, 0, 1.78, 26),
    'Tm': (168.93, 0, 1.77, 28), 'Yb': (173.05, 0, 1.77, 10),
    'Lu': (174.97, 0, 1.77, 30), 'Hf': (178.49, 252, 1.59, 110),
    'Ta': (180.95, 240, 1.46, 200), 'W': (183.84, 400, 1.39, 310),
    'Re': (186.21, 430, 1.37, 370), 'Os': (190.23, 500, 1.35, 400),
    'Ir': (192.22, 420, 1.36, 355), 'Pt': (195.08, 240, 1.39, 230),
    'Au': (196.97, 170, 1.44, 180), 'Hg': (200.59, 0, 1.51, 25),
    'Tl': (204.38, 78, 1.70, 8), 'Pb': (207.20, 105, 1.75, 23),
    'Bi': (208.98, 0, 1.70, 0), 'Th': (232.04, 163, 1.80, 54),
    'Pa': (231.04, 0, 1.80, 0), 'U': (238.03, 207, 1.75, 100),
}

def parse_formula(f):
    pairs = re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f)
    atoms = {}
    for el, cnt in pairs:
        if el in ATOM_DB:
            atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    return atoms

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
    f_corr = 1.0 - 0.3 * (1.0 - 1.0/n_atoms)
    edge_sum = 0
    els = list(atoms.keys())
    for i in range(len(els)):
        for j in range(i+1, len(els)):
            mi = atoms[els[i]] * ATOM_DB[els[i]][0] * AMU
            mj = atoms[els[j]] * ATOM_DB[els[j]][0] * AMU
            edge_sum += (1.0/mi + 1.0/mj)
    if not edge_sum:
        mi = total_m * AMU / n_atoms
        edge_sum = (n_atoms * (n_atoms-1) / 2) * 2.0 / mi
    G = (1.0/l) * math.sqrt((1.0 - f_corr) * edge_sum)
    omega_d = theta_d * KB / HBAR
    dd0_sq = (C2 / l**2) * (3*HBAR / (4*omega_d)) * (1 - f_corr) * edge_sum
    dd0 = math.sqrt(abs(dd0_sq))
    return {
        'l': l, 'G': G, 'dd0': dd0, 'tD': theta_d,
        'M': total_m, 'Z': total_z, 'V': V_cell,
        'n_atoms': n_atoms, 'avg_m': avg_m,
    }

# A4群特征值
def a4_eigenvalues():
    return [2 - 2*math.cos(k*math.pi/5) for k in range(1, 5)]

# 黎曼零点（前几个）
RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832]

def riemann_gaps():
    return [RIEMANN_ZEROS[i+1] - RIEMANN_ZEROS[i] for i in range(len(RIEMANN_ZEROS)-1)]

# 晶格类型 → 配位数/拓扑参数
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

def get_lattice_topo(struct_str):
    s = struct_str.lower()
    for key in LATTICE_TOPO:
        if key.lower() in s:
            return LATTICE_TOPO[key]
    return None

# 加载数据
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

# 从k_eff_derivation.py的拟合结果
a_ke = -0.769
b_ke = 1.132

# 计算每个材料的K_0
for d in data:
    d['k0'] = d['k_eff'] / (d['G']**a_ke * d['tD']**b_ke)

# 1. K_0^cat的值
print("\n" + "="*80)
print("1. K_0^cat的值（按类别）")
print("="*80)
cat_data = defaultdict(list)
for d in data:
    cat_data[d['cat']].append(d)

print(f"{'类别':<28} {'n':>4} {'K_0中位':>10} {'K_0均值':>10} {'CV%':>6} {'ln K_0':>8}")
print("-"*80)
cat_k0 = {}
for cat in sorted(cat_data.keys()):
    cd = cat_data[cat]
    k0s = np.array([d['k0'] for d in cd])
    cat_k0[cat] = np.median(k0s)
    cv = np.std(k0s)/np.mean(k0s)*100 if np.mean(k0s) != 0 else 0
    print(f"{cat:<28} {len(cd):>4} {np.median(k0s):>10.4f} {np.mean(k0s):>10.4f} {cv:>6.0f}% {np.log(np.median(k0s)):>8.3f}")

# 2. K_0与晶格拓扑参数的关系
print("\n" + "="*80)
print("2. K_0与晶格拓扑参数的关系")
print("="*80)

topo_data = defaultdict(list)
for d in data:
    if d['topo'] is not None:
        topo_data[d['topo']['cn']].append(d['k0'])

print(f"{'配位数':>8} {'n':>4} {'K_0中位':>10} {'ln K_0':>8}")
print("-"*40)
for cn in sorted(topo_data.keys()):
    k0s = np.array(topo_data[cn])
    print(f"{cn:>8} {len(k0s):>4} {np.median(k0s):>10.4f} {np.log(np.median(k0s)):>8.3f}")

# 3. K_0与CQM普适参数的关系
print("\n" + "="*80)
print("3. K_0与CQM普适参数的关系")
print("="*80)

a4_eigs = a4_eigenvalues()
print(f"A4特征值: {a4_eigs}")
print(f"A4特征值和: {sum(a4_eigs):.4f}")
print(f"A4特征值积: {np.prod(a4_eigs):.4f}")
print(f"Coxeter数 h=5")

gaps = riemann_gaps()
print(f"黎曼零点间距: {gaps[:5]}")
print(f"平均间距: {np.mean(gaps):.4f}")
print(f"GAP(γ₂-γ₁): {GAP:.6f}")

# 4. K_0^cat = CQM普适常数 × 类别几何因子?
print("\n" + "="*80)
print("4. K_0^cat / CQM普适参数（寻找类别几何因子）")
print("="*80)

cqm_universal = {
    'GAP': GAP,
    'GAP²': GAP**2,
    'β': BETA,
    'β/π': BETA / math.pi,
    'A4_tr': sum(a4_eigs),
    'A4_prod': np.prod(a4_eigs),
    'h²': 25,
    'ln(h)': math.log(5),
    'γ₁/γ₂': RIEMANN_ZEROS[0]/RIEMANN_ZEROS[1],
    '平均间距': np.mean(gaps),
}

print(f"{'类别':<28} {'ln K_0':>8}", end='')
for name in cqm_universal:
    print(f" {name:>10}", end='')
print()
print("-"*120)
for cat in sorted(cat_k0.keys()):
    ln_k0 = np.log(cat_k0[cat])
    print(f"{cat:<28} {ln_k0:>8.3f}", end='')
    for name in cqm_universal:
        ratio = ln_k0 / cqm_universal[name] if cqm_universal[name] != 0 else 0
        print(f" {ratio:>10.4f}", end='')
    print()

# 5. K_0与结构复杂度的关系
print("\n" + "="*80)
print("5. K_0与结构复杂度的关系")
print("="*80)

# 结构复杂度指标：对称性倒数（越低对称越复杂）
cat_complexity = {}
for cat in sorted(cat_data.keys()):
    cd = cat_data[cat]
    syms = [d['topo']['sym'] for d in cd if d['topo'] is not None]
    if syms:
        cat_complexity[cat] = np.mean(syms)
    else:
        cat_complexity[cat] = 0

print(f"{'类别':<28} {'K_0':>10} {'平均对称数':>10} {'1/sym':>10} {'ln(K_0)':>8} {'ln(1/sym)':>10}")
print("-"*80)
for cat in sorted(cat_k0.keys()):
    sym = cat_complexity[cat]
    inv_sym = 1.0/sym if sym > 0 else 0
    print(f"{cat:<28} {cat_k0[cat]:>10.4f} {sym:>10.1f} {inv_sym:>10.4f} {np.log(cat_k0[cat]):>8.3f} {np.log(inv_sym) if inv_sym > 0 else 0:>10.3f}")

# 6. K_0与配位数、对称数的回归
print("\n" + "="*80)
print("6. ln(K_0) ~ a·ln(1/cn) + b·ln(1/sym) + c 的回归")
print("="*80)

valid = [d for d in data if d['topo'] is not None]
X = []
y = []
for d in valid:
    cn = d['topo']['cn']
    sym = d['topo']['sym']
    X.append([np.log(1.0/cn), np.log(1.0/sym), 1.0])
    y.append(np.log(d['k0']))
X = np.array(X)
y = np.array(y)

# 最小二乘
try:
    coef, res, rank, sv = np.linalg.lstsq(X, y, rcond=None)
    y_pred = X @ coef
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res/ss_tot
    print(f"R² = {r2:.3f}")
    print(f"  ln(1/cn): {coef[0]:.3f}")
    print(f"  ln(1/sym): {coef[1]:.3f}")
    print(f"  const: {coef[2]:.3f}")
except Exception as e:
    print(f"回归失败: {e}")

# 7. LOOCV: K_0从拓扑参数预测
print("\n" + "="*80)
print("7. LOOCV: K_0从晶格拓扑参数预测→Tc")
print("="*80)

valid = [d for d in data if d['topo'] is not None]
errors = []
for i in range(len(valid)):
    train = [valid[j] for j in range(len(valid)) if j != i]
    test = valid[i]
    X_tr = np.array([[np.log(1.0/d['topo']['cn']), np.log(1.0/d['topo']['sym']), 1.0] for d in train])
    y_tr = np.array([np.log(d['k0']) for d in train])
    try:
        coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
        x_test = np.array([np.log(1.0/test['topo']['cn']), np.log(1.0/test['topo']['sym']), 1.0])
        k0_pred = np.exp(x_test @ coef)
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

# 8. 总结
print("\n" + "="*80)
print("8. 总结")
print("="*80)
print(f"""
K_0^cat的范围: {min(cat_k0.values()):.4f} ~ {max(cat_k0.values()):.4f}
ln(K_0^cat)的范围: {np.log(min(cat_k0.values())):.3f} ~ {np.log(max(cat_k0.values())):.3f}

K_0与晶格拓扑参数回归R² = {r2:.3f}
  → 晶格拓扑(配位数+对称数){'可以' if r2 > 0.5 else '不能'}解释K_0的大部分变异

LOOCV(拓扑→K_0→Tc): 中位误差{np.median(errors)*100:.0f}%

结论:
  - K_0^cat是类别特征常数，范围跨~{np.log(max(cat_k0.values()))-np.log(min(cat_k0.values())):.1f}个数量级
  - 晶格拓扑参数(配位数、对称数)R²={r2:.3f}
  - {'拓扑参数可以部分解释K_0' if r2 > 0.3 else '拓扑参数不能解释K_0'}
  - K_0^cat的微观来源仍需DFT数据(电子结构、Fermi面拓扑)
""")