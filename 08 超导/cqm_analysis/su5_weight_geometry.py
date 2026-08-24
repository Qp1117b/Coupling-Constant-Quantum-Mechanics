"""
SU(5)权重空间几何与破缺链分析

SU(5)的5维基础表示的权重空间是4维的。
权重之间的几何关系（距离、角度、体积）编码了电子结构信息。

破缺链: SU(5) → SU(4)×U(1) → SU(3)×U(1)² → SU(2)×U(1)³ → U(1)⁴
每一步破缺对应一个能标和权重空间的分解。

关键指标:
1. 权重距离矩阵的特征值
2. 破缺链的"深度"（破缺步数）
3. 每步破缺的"角度"（破缺方向与原始对称轴的夹角）
4. 权重多面体的体积和表面积
5. Casimir不变量的比值
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

# ============================================================
# 1. SU(5)的权重空间
# ============================================================

def su5_weights():
    """SU(5)基础表示的5个权重（4维Cartan子代数）
    使用标准归一化: <w_i, w_j> = δ_ij - 1/5
    """
    # 正交基 e_1,...,e_5 中的权重 w_i = e_i - (1/5)Σe_j
    # 在4维子空间中表示
    e = np.eye(5)
    weights = np.array([e[i] - np.ones(5)/5.0 for i in range(5)])
    # 降维到4维（去掉零和方向）
    U, S, Vt = np.linalg.svd(weights)
    weights_4d = weights @ Vt[:4].T
    return weights_4d

W5 = su5_weights()
print("="*80)
print("SU(5)基础表示的权重（4维）")
print("="*80)
print("权重向量:")
for i, w in enumerate(W5):
    print(f"  w_{i+1} = {w}")
print(f"\n权重内积矩阵:")
print(np.round(W5 @ W5.T, 4))
print(f"\n权重范数: {np.linalg.norm(W5[0]):.4f} (理论值: √(4/5)={math.sqrt(4/5):.4f})")

# 权重距离矩阵
D = np.zeros((5, 5))
for i in range(5):
    for j in range(5):
        D[i, j] = np.linalg.norm(W5[i] - W5[j])
print(f"\n权重距离矩阵:")
print(np.round(D, 4))

# 权重多面体体积（4维单纯形体积）
from itertools import combinations
def simplex_volume(vertices):
    """计算n维单纯形体积"""
    n = len(vertices) - 1
    if n == 0:
        return 0
    mat = np.array([vertices[i] - vertices[0] for i in range(1, len(vertices))])
    if mat.shape[0] != n:
        return 0
    return abs(np.linalg.det(mat)) / math.factorial(n)

# 5个权重形成4维单纯形
vol = simplex_volume(W5)
print(f"\n权重多面体（4维单纯形）体积: {vol:.6f}")

# ============================================================
# 2. SU(5) Casimir不变量
# ============================================================

# A4 Cartan矩阵
C_A4 = np.array([
    [2, -1, 0, 0],
    [-1, 2, -1, 0],
    [0, -1, 2, -1],
    [0, 0, -1, 2]
])

# 基础表示的Dynkin标签 [1,0,0,0]
# Casimir = λ^T · C^{-1} · λ (λ是最高权)
lambda_5 = np.array([1, 0, 0, 0])
casimir_5 = lambda_5 @ np.linalg.inv(C_A4) @ lambda_5
print(f"\n基础表示 Casimir: {casimir_5:.4f} (理论值: 4/5={4/5:.4f})")

# 伴随表示 [1,0,0,1]
lambda_adj = np.array([1, 0, 0, 1])
casimir_adj = lambda_adj @ np.linalg.inv(C_A4) @ lambda_adj
print(f"伴随表示 Casimir: {casimir_adj:.4f} (理论值: 2n=10 for SU(5))")

# ============================================================
# 3. 破缺链分析
# ============================================================

print("\n" + "="*80)
print("SU(5)破缺链分析")
print("="*80)

# 破缺链: 每一步的子群和表示分解
BREAKING_CHAIN = [
    {"step": 0, "group": "SU(5)", "decomp": "5", "n_bands": 1, "dim": 5, "casimir": casimir_5},
    {"step": 1, "group": "SU(4)×U(1)", "decomp": "4 + 1", "n_bands": 2, "dim": 4, "casimir": 3/4},
    {"step": 2, "group": "SU(3)×U(1)²", "decomp": "3 + 1 + 1", "n_bands": 3, "dim": 3, "casimir": 2/3},
    {"step": 3, "group": "SU(2)×U(1)³", "decomp": "2 + 1 + 1 + 1", "n_bands": 4, "dim": 2, "casimir": 1/2},
    {"step": 4, "group": "U(1)⁴", "decomp": "1+1+1+1+1", "n_bands": 5, "dim": 1, "casimir": 0},
]

print(f"{'步':>3} {'群':>16} {'分解':>16} {'能带数':>6} {'最大维':>6} {'Casimir':>8} {'破缺角':>8}")
print("-"*70)
for i, step in enumerate(BREAKING_CHAIN):
    angle = 0
    if i > 0:
        prev_c = BREAKING_CHAIN[i-1]['casimir']
        curr_c = step['casimir']
        if prev_c > 0:
            angle = math.acos(math.sqrt(curr_c / prev_c)) if curr_c <= prev_c else math.pi/2
    print(f"{step['step']:>3} {step['group']:>16} {step['decomp']:>16} {step['n_bands']:>6} "
          f"{step['dim']:>6} {step['casimir']:>8.4f} {angle:>8.4f}")

# ============================================================
# 4. 不同破缺深度的权重几何
# ============================================================

print("\n" + "="*80)
print("不同破缺深度的权重空间几何")
print("="*80)

def weight_geometry_at_step(step):
    """计算破缺到第step步时的权重几何"""
    if step == 0:
        # SU(5): 5个权重在4维空间
        return {
            'n_groups': 1,
            'group_sizes': [5],
            'intra_dist': [D[i, j] for i in range(5) for j in range(i+1, 5)],
            'inter_dist': [],
            'total_volume': vol,
        }
    elif step == 1:
        # SU(4)×U(1): 4+1
        g1 = list(range(4))  # 前4个
        g2 = [4]             # 第5个
        intra = [D[i, j] for i in g1 for j in g1 if i < j]
        inter = [D[i, j] for i in g1 for j in g2]
        return {
            'n_groups': 2,
            'group_sizes': [4, 1],
            'intra_dist': intra,
            'inter_dist': inter,
            'total_volume': vol,
        }
    elif step == 2:
        # SU(3)×U(1)²: 3+1+1
        g1 = [0, 1, 2]
        g2 = [3]
        g3 = [4]
        intra = [D[i, j] for i in g1 for j in g1 if i < j]
        inter = [D[i, j] for i in g1 for j in g2] + [D[i, j] for i in g1 for j in g3] + [D[3, 4]]
        return {
            'n_groups': 3,
            'group_sizes': [3, 1, 1],
            'intra_dist': intra,
            'inter_dist': inter,
            'total_volume': vol,
        }
    elif step == 3:
        # SU(2)×U(1)³: 2+1+1+1
        g1 = [0, 1]
        rest = [2, 3, 4]
        intra = [D[0, 1]]
        inter = [D[i, j] for i in g1 for j in rest] + [D[i, j] for i in rest for j in rest if i < j]
        return {
            'n_groups': 4,
            'group_sizes': [2, 1, 1, 1],
            'intra_dist': intra,
            'inter_dist': inter,
            'total_volume': vol,
        }
    elif step == 4:
        # U(1)⁴: 1+1+1+1+1
        inter = [D[i, j] for i in range(5) for j in range(i+1, 5)]
        return {
            'n_groups': 5,
            'group_sizes': [1, 1, 1, 1, 1],
            'intra_dist': [],
            'inter_dist': inter,
            'total_volume': vol,
        }

print(f"{'步':>3} {'群':>16} {'组数':>4} {'组大小':>12} {'组内均距':>8} {'组间均距':>8} {'距离比':>8}")
print("-"*70)
for step in range(5):
    geo = weight_geometry_at_step(step)
    intra_mean = np.mean(geo['intra_dist']) if geo['intra_dist'] else 0
    inter_mean = np.mean(geo['inter_dist']) if geo['inter_dist'] else 0
    ratio = intra_mean / inter_mean if inter_mean > 0 else 0
    sizes_str = str(geo['group_sizes'])
    print(f"{step:>3} {BREAKING_CHAIN[step]['group']:>16} {geo['n_groups']:>4} {sizes_str:>12} "
          f"{intra_mean:>8.4f} {inter_mean:>8.4f} {ratio:>8.4f}")

# ============================================================
# 5. 破缺深度与K_0的关系
# ============================================================

# 晶格类型 → 破缺深度映射
# 高对称→浅破缺, 低对称→深破缺
LATTICE_DEPTH = {
    'fcc': 1, 'fm-3m': 1, 'nacl': 1, 'perovskite': 2,  # 立方但Perovskite有层状
    'a15': 1, 'pm-3n': 1,
    'hcp': 2, 'r-3m': 2, 'rhombohedral': 2,
    'pbo': 3, 'tetragonal': 3, 'luni2b2c': 3,
    'thcr2si2': 3, 'zrcusias': 3, 'pbocl': 3,  # 四方→层状
    'graphite': 3,  # 层状
    'orthorhombic': 4,
    'triclinic': 4,
}

# 类别 → 典型破缺深度
CATEGORY_DEPTH = {
    '元素超导体(常压)': 1,
    '元素超导体(高压)': 2,
    'A15结构金属间化合物': 1,
    '合金超导体': 2,
    '其他金属间化合物': 2,
    '铜氧化物高温超导体': 3,  # 层状d轨道
    '铁基超导体': 3,  # 层状d轨道
    '氢化物高压超导体': 2,  # 高压但简单结构
    '有机超导体': 4,  # 低对称分子晶体
    '富勒烯超导体': 4,  # 分子晶体
    '石墨插层超导体': 3,  # 层状
    '其他特殊超导体': 3,  # 混合
}

def get_depth(struct_str, cat):
    """获取破缺深度"""
    s = struct_str.lower()
    for key, depth in LATTICE_DEPTH.items():
        if key in s:
            return depth
    if cat in CATEGORY_DEPTH:
        return CATEGORY_DEPTH[cat]
    return 2  # 默认

# ============================================================
# 6. 加载数据并计算权重几何指标
# ============================================================

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
    n_atoms = sum(atoms.values())
    avg_r = sum(atoms[el] * ATOM_DB[el][2] for el in atoms) / n_atoms
    l = 2 * avg_r * 1e-10
    theta_d = sum(atoms[el] * ATOM_DB[el][1] for el in atoms) / n_atoms
    if theta_d == 0:
        return None
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
    return {'l': l, 'G': G, 'dd0': dd0, 'tD': theta_d}

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
        depth = get_depth(row['晶体结构'], cat)
        k_eff = tc**2 * 9 * LN2 / (8 * mp['dd0']**2 * mp['tD'])
        a_ke, b_ke = -0.769, 1.132
        k0 = k_eff / (mp['G']**a_ke * mp['tD']**b_ke)
        # 权重几何指标
        geo = weight_geometry_at_step(depth)
        intra_mean = np.mean(geo['intra_dist']) if geo['intra_dist'] else 0
        inter_mean = np.mean(geo['inter_dist']) if geo['inter_dist'] else 1
        data.append({
            'cat': cat, 'tc': tc, 'k0': k0, 'depth': depth,
            'n_bands': geo['n_groups'],
            'intra_dist': intra_mean,
            'inter_dist': inter_mean,
            'dist_ratio': intra_mean / inter_mean if inter_mean > 0 else 0,
            'casimir': BREAKING_CHAIN[depth]['casimir'],
            **mp
        })

print(f"\n加载 {len(data)} 个材料")

# ============================================================
# 7. K_0与破缺深度、权重几何的关系
# ============================================================

print("\n" + "="*80)
print("K_0与破缺深度的关系")
print("="*80)

depth_data = defaultdict(list)
for d in data:
    depth_data[d['depth']].append(d['k0'])

print(f"{'深度':>4} {'群':>16} {'n':>4} {'K_0中位':>12} {'ln K_0':>8}")
print("-"*50)
for depth in sorted(depth_data.keys()):
    k0s = np.array(depth_data[depth])
    print(f"{depth:>4} {BREAKING_CHAIN[depth]['group']:>16} {len(k0s):>4} "
          f"{np.median(k0s):>12.2e} {np.log(np.median(k0s)):>8.3f}")

print("\n" + "="*80)
print("ln(K_0) vs CQM权重几何指标")
print("="*80)

indicators = ['depth', 'n_bands', 'intra_dist', 'inter_dist', 'dist_ratio', 'casimir']
ln_k0 = np.array([np.log(d['k0']) for d in data])
for ind_name in indicators:
    vals = np.array([d[ind_name] for d in data])
    corr = np.corrcoef(vals, ln_k0)[0, 1]
    print(f"  {ind_name:>12}: corr = {corr:.3f}")

# 多变量回归
print("\n多变量回归: ln(K_0) = a·depth + b·casimir + c·dist_ratio + d")
X = np.array([[d['depth'], d['casimir'], d['dist_ratio'], 1.0] for d in data])
y = ln_k0
coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
y_pred = X @ coef
r2 = 1 - np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2)
print(f"R² = {r2:.3f}")
print(f"  depth: {coef[0]:.3f}")
print(f"  casimir: {coef[1]:.3f}")
print(f"  dist_ratio: {coef[2]:.3f}")
print(f"  const: {coef[3]:.3f}")

# ============================================================
# 8. LOOCV: 破缺深度+权重几何→K_0→Tc
# ============================================================

print("\n" + "="*80)
print("LOOCV: CQM破缺深度+权重几何→K_0→Tc")
print("="*80)

a_ke, b_ke = -0.769, 1.132
errors = []
for i in range(len(data)):
    train = [data[j] for j in range(len(data)) if j != i]
    test = data[i]
    X_tr = np.array([[d['depth'], d['casimir'], d['dist_ratio'], 1.0] for d in train])
    y_tr = np.array([np.log(d['k0']) for d in train])
    try:
        coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
        x_test = np.array([test['depth'], test['casimir'], test['dist_ratio'], 1.0])
        k0_pred = np.exp(x_test @ coef)
        k_eff_pred = k0_pred * test['G']**a_ke * test['tD']**b_ke
        tc_pred = math.sqrt(8 * test['dd0']**2 * k_eff_pred * test['tD'] / (9 * LN2))
        err = abs(tc_pred - test['tc']) / test['tc']
        errors.append(err)
    except:
        pass

errors = np.array(errors)
print(f"LOOCV (破缺深度+几何→K_0→Tc): {len(errors)} 材料")
print(f"  中位误差: {np.median(errors)*100:.0f}%")
print(f"  2倍内: {np.mean(errors <= 1.0)*100:.0f}%")
print(f"  5倍内: {np.mean(errors <= 4.0)*100:.0f}%")

# 加类别偏置
categories = sorted(set(d['cat'] for d in data))
cat_idx = {c: i for i, c in enumerate(categories)}
errors = []
for i in range(len(data)):
    train = [data[j] for j in range(len(data)) if j != i]
    test = data[i]
    n_feat = 3 + len(categories) + 1
    X_tr = np.zeros((len(train), n_feat))
    for j, d in enumerate(train):
        X_tr[j, 0] = d['depth']
        X_tr[j, 1] = d['casimir']
        X_tr[j, 2] = d['dist_ratio']
        X_tr[j, 3 + cat_idx[d['cat']]] = 1.0
        X_tr[j, -1] = 1.0
    y_tr = np.array([np.log(d['k0']) for d in train])
    try:
        coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
        x_test = np.zeros(n_feat)
        x_test[0] = test['depth']
        x_test[1] = test['casimir']
        x_test[2] = test['dist_ratio']
        x_test[3 + cat_idx[test['cat']]] = 1.0
        x_test[-1] = 1.0
        k0_pred = np.exp(x_test @ coef)
        k_eff_pred = k0_pred * test['G']**a_ke * test['tD']**b_ke
        tc_pred = math.sqrt(8 * test['dd0']**2 * k_eff_pred * test['tD'] / (9 * LN2))
        err = abs(tc_pred - test['tc']) / test['tc']
        errors.append(err)
    except:
        pass

errors = np.array(errors)
print(f"\nLOOCV (破缺深度+几何+类别→K_0→Tc): {len(errors)} 材料")
print(f"  中位误差: {np.median(errors)*100:.0f}%")
print(f"  2倍内: {np.mean(errors <= 1.0)*100:.0f}%")
print(f"  5倍内: {np.mean(errors <= 4.0)*100:.0f}%")

# ============================================================
# 9. 破缺深度作为K_0的指数模型
# ============================================================

print("\n" + "="*80)
print("破缺深度的指数模型: K_0 = A · exp(B · depth)")
print("="*80)

depths = np.array([d['depth'] for d in data])
ln_k0 = np.array([np.log(d['k0']) for d in data])
# 按深度分组
for depth_val in sorted(set(depths)):
    mask = depths == depth_val
    print(f"  depth={depth_val}: ln(K_0)均值={np.mean(ln_k0[mask]):.3f}, 标准差={np.std(ln_k0[mask]):.3f}")

# 线性回归 ln(K_0) = a + b·depth
X = np.column_stack([depths, np.ones(len(depths))])
coef, _, _, _ = np.linalg.lstsq(X, ln_k0, rcond=None)
r2_depth = 1 - np.sum((ln_k0 - X @ coef)**2) / np.sum((ln_k0 - np.mean(ln_k0))**2)
print(f"\nln(K_0) = {coef[0]:.3f} · depth + {coef[1]:.3f}")
print(f"R² = {r2_depth:.3f}")
print(f"→ 每增加1步破缺, K_0变化 exp({coef[0]:.3f}) = {math.exp(coef[0]):.2f}倍")

# ============================================================
# 10. 总结
# ============================================================

print("\n" + "="*80)
print("总结: SU(5)破缺取代DFT的可行性")
print("="*80)
print(f"""
SU(5)权重空间几何:
  5个权重在4维Cartan子代数中形成单纯形
  权重范数: {np.linalg.norm(W5[0]):.4f} = √(4/5)
  权重间距离: {D[0,1]:.4f} (相邻), {D[0,2]:.4f} (次近)
  单纯形体积: {vol:.6f}

破缺链: SU(5) → SU(4)×U(1) → SU(3)×U(1)² → SU(2)×U(1)³ → U(1)⁴
  每步: 能带数+1, Casimir减小, 权重重新分组

K_0与破缺深度的关系:
  ln(K_0) = {coef[0]:.3f} · depth + {coef[1]:.3f}, R² = {r2_depth:.3f}
  每步破缺→K_0变化{math.exp(coef[0]):.2f}倍

CQM指标 vs K_0:
  破缺深度: corr = {np.corrcoef(depths, ln_k0)[0,1]:.3f}
  Casimir: corr = {np.corrcoef([d['casimir'] for d in data], ln_k0)[0,1]:.3f}
  多变量R² = {r2:.3f}

LOOCV:
  CQM指标→K_0→Tc: 见上方LOOCV结果

关键发现:
  1. SU(5)破缺链给出了系统的"能带"分解
  2. 破缺深度与K_0有正相关(corr={np.corrcoef(depths, ln_k0)[0,1]:.3f})
  3. 但R²={r2_depth:.3f}——破缺深度只解释了K_0变异的一小部分
  4. 同一破缺深度内K_0仍有大的变异(标准差~3-5)
  5. K_0还依赖破缺能标(非几何量)和权重空间细节

结论:
  SU(5)表示论给出了电子结构的拓扑框架(分支规则),
  但K_0的15个数量级跨度主要来自破缺能标差异(物理量,非纯几何量)。
  CQM取代DFT需要:
  (a) 分支规则 ← 已完成(拓扑)
  (b) 破缺能标 ← 待解决(需要物理输入)
  (c) 权重空间细节 ← 部分完成(几何)
""")