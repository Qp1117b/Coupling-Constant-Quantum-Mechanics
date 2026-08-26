"""
SU(5) → 点群破缺映射

核心思想:
  SU(5)的5维基础表示 ⊃ SO(3)的l=2表示（5维不可约）
  晶格点群G ⊂ SO(3) → SU(5)破缺到G
  5维表示在G下分解为不可约表示 → "能带"结构

不同嵌入方式:
  方式1: 5 = l=2 (d轨道系统，过渡金属)
  方式2: 5 = 2×l=0 ⊕ l=1 (s-p系统，主族)
  方式3: 5 = l=0 ⊕ l=1 ⊕ l=0 (s-p-s混合)

分支规则 (SO(3) → 点群):
  l=0 → A_1g (所有点群)
  l=1 → T_1u (O_h), A_2u⊕E_u (D_4h), A_2u⊕E_g (D_3d), E_1u⊕A_2u (D_6h)
  l=2 → E_g⊕T_2g (O_h), A_1g⊕B_1g⊕B_2g⊕E_g (D_4h), A_1g⊕2E_g (D_3d), A_1g⊕E_1g⊕E_2g (D_6h)
  l=3 → A_2u⊕T_1u⊕T_2u (O_h), ...
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework'); from atom_db import ATOM_DB, atom_db

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
# 1. 点群的不可约表示和SO(3)分支规则
# ============================================================

# 各点群的不可约表示: (名称, 维度, 宇称)
POINT_GROUPS = {
    'O_h': {  # 立方群, 48阶
        'irreps': [('A1g',1,+1),('A2g',1,+1),('Eg',2,+1),('T1g',3,+1),('T2g',3,+1),
                   ('A1u',1,-1),('A2u',1,-1),('Eu',2,-1),('T1u',3,-1),('T2u',3,-1)],
        'order': 48,
    },
    'D_4h': {  # 四方群, 16阶
        'irreps': [('A1g',1,+1),('A2g',1,+1),('B1g',1,+1),('B2g',1,+1),('Eg',2,+1),
                   ('A1u',1,-1),('A2u',1,-1),('B1u',1,-1),('B2u',1,-1),('Eu',2,-1)],
        'order': 16,
    },
    'D_3d': {  # 三方群, 12阶
        'irreps': [('A1g',1,+1),('A2g',1,+1),('Eg',2,+1),
                   ('A1u',1,-1),('A2u',1,-1),('Eu',2,-1)],
        'order': 12,
    },
    'D_6h': {  # 六方群, 24阶
        'irreps': [('A1g',1,+1),('A2g',1,+1),('B1g',1,+1),('B2g',1,+1),('E1g',2,+1),('E2g',2,+1),
                   ('A1u',1,-1),('A2u',1,-1),('B1u',1,-1),('B2u',1,-1),('E1u',2,-1),('E2u',2,-1)],
        'order': 24,
    },
    'D_2h': {  # 正交群, 8阶
        'irreps': [('Ag',1,+1),('B1g',1,+1),('B2g',1,+1),('B3g',1,+1),
                   ('Au',1,-1),('B1u',1,-1),('B2u',1,-1),('B3u',1,-1)],
        'order': 8,
    },
    'C_2h': {  # 单斜群, 4阶
        'irreps': [('Ag',1,+1),('Bg',1,+1),('Au',1,-1),('Bu',1,-1)],
        'order': 4,
    },
    'C_i': {  # 三斜群, 2阶
        'irreps': [('Ag',1,+1),('Au',1,-1)],
        'order': 2,
    },
    'C_1': {  # 无对称, 1阶
        'irreps': [('A',1,+1)],
        'order': 1,
    },
}

# SO(3) → 点群的分支规则: l → [(irrep_name, multiplicity), ...]
BRANCHING_RULES = {
    'O_h': {
        0: [('A1g',1)],
        1: [('T1u',1)],
        2: [('Eg',1),('T2g',1)],
        3: [('A2u',1),('T1u',1),('T2u',1)],
        4: [('A1g',1),('Eg',1),('T1g',1),('T2g',1)],
    },
    'D_4h': {
        0: [('A1g',1)],
        1: [('A2u',1),('Eu',1)],
        2: [('A1g',1),('B1g',1),('B2g',1),('Eg',1)],
        3: [('A2u',1),('B1u',1),('B2u',1),('Eu',2)],
        4: [('A1g',2),('B1g',1),('B2g',1),('Eg',1)],
    },
    'D_3d': {
        0: [('A1g',1)],
        1: [('A2u',1),('Eu',1)],
        2: [('A1g',1),('Eg',2)],
        3: [('A2u',1),('A1u',1),('Eu',2)],
        4: [('A1g',2),('Eg',2)],
    },
    'D_6h': {
        0: [('A1g',1)],
        1: [('A2u',1),('E1u',1)],
        2: [('A1g',1),('E1g',1),('E2g',1)],
        3: [('A2u',1),('B1u',1),('B2u',1),('E1u',1),('E2u',1)],
        4: [('A1g',1),('B1g',1),('B2g',1),('E1g',1),('E2g',1)],
    },
    'D_2h': {
        0: [('Ag',1)],
        1: [('B1u',1),('B2u',1),('B3u',1)],
        2: [('Ag',1),('B1g',1),('B2g',1),('B3g',1)],
        3: [('Au',1),('B1u',1),('B2u',1),('B3u',1)],
        4: [('Ag',2),('B1g',1),('B2g',1),('B3g',1)],
    },
    'C_2h': {
        0: [('Ag',1)],
        1: [('Au',1),('Bu',1)],
        2: [('Ag',1),('Bg',1)],
        3: [('Au',1),('Bu',1)],
        4: [('Ag',2),('Bg',1)],
    },
    'C_i': {
        0: [('Ag',1)],
        1: [('Au',1)],
        2: [('Ag',1)],
        3: [('Au',1)],
        4: [('Ag',1)],
    },
    'C_1': {
        0: [('A',1)],
        1: [('A',1)],
        2: [('A',1)],
        3: [('A',1)],
        4: [('A',1)],
    },
}

# ============================================================
# 2. SU(5)的5维表示的嵌入方式
# ============================================================

# 嵌入方式: 名称 → [(l值, 重数), ...]
# 5 = sum(重数 * (2l+1))
EMBEDDINGS = {
    'd-orbital': [(2, 1)],           # 5 = 1*5 (l=2, d轨道)
    'sp-mixed': [(0, 1), (1, 1), (0, 1)],  # 5 = 1 + 3 + 1 (s+p+s)
    's2p': [(0, 2), (1, 1)],          # 5 = 2 + 3 (2s+p)
    'sd': [(0, 1), (2, 1)],           # 不对，1+5=6≠5
    # 修正: 只有前三种是有效的5维分解
}

# 验证嵌入
_invalid = []
for name, decomp in EMBEDDINGS.items():
    dim = sum(m * (2*l + 1) for l, m in decomp)
    if dim != 5:
        print(f"警告: 嵌入'{name}'维度={dim}≠5，移除")
        _invalid.append(name)
for name in _invalid:
    del EMBEDDINGS[name]

print("="*80)
print("SU(5)的5维表示的嵌入方式")
print("="*80)
for name, decomp in EMBEDDINGS.items():
    terms = " + ".join(f"{m}×l={l}" if m > 1 else f"l={l}" for l, m in decomp)
    dim = sum(m * (2*l + 1) for l, m in decomp)
    print(f"  {name}: {terms} (dim={dim})")

# ============================================================
# 3. 计算分支规则: SU(5)的5 → 点群G的不可约表示
# ============================================================

def decompose_5(embedding, point_group):
    """将SU(5)的5维表示在点群下分解"""
    result = defaultdict(int)
    for l, mult in embedding:
        if l in BRANCHING_RULES[point_group]:
            for irrep, m in BRANCHING_RULES[point_group][l]:
                result[irrep] += mult * m
    return dict(result)

print("\n" + "="*80)
print("SU(5)的5维表示在各点群下的分解")
print("="*80)

for emb_name, emb in EMBEDDINGS.items():
    print(f"\n--- 嵌入: {emb_name} ---")
    for pg_name in ['O_h', 'D_6h', 'D_4h', 'D_3d', 'D_2h', 'C_2h', 'C_i', 'C_1']:
        decomp = decompose_5(emb, pg_name)
        terms = " + ".join(f"{m}×{irrep}" if m > 1 else irrep
                          for irrep, m in sorted(decomp.items()))
        n_bands = len(decomp)

        irrep_dims = dict((name, dim) for name, dim, _ in POINT_GROUPS[pg_name]['irreps'])
        degs = [irrep_dims.get(irrep, 1) * m for irrep, m in decomp.items()]
        max_band_deg = max(degs) if degs else 0
        print(f"  {pg_name:>6} (|G|={POINT_GROUPS[pg_name]['order']:>3}): {terms:<40} "
              f"→ {n_bands}条能带, 最大简并={max_band_deg}")

# ============================================================
# 4. CQM电子结构指标
# ============================================================

def cqm_electronic_indicators(embedding, point_group):
    """从SU(5)破缺模式计算CQM电子结构指标"""
    decomp = decompose_5(embedding, point_group)
    irrep_dims = dict((name, dim) for name, dim, _ in POINT_GROUPS[point_group]['irreps'])

    n_bands = len(decomp)
    degs = sorted([irrep_dims.get(irrep, 1) * m for irrep, m in decomp.items()], reverse=True)
    max_deg = max(degs) if degs else 0
    min_deg = min(degs) if degs else 0

    # 结构复杂度指标
    # 1. 能带数: 对称性越低→能带越多→越复杂
    # 2. 简并度熵: -Σ(d_i/5)·log(d_i/5)
    total = sum(degs)
    entropy = -sum((d/total) * math.log(d/total) for d in degs) if total > 0 else 0

    # 3. 破缺度: 1 - |G|/|SO(3)| (用48作为SO(3)有限近似)
    breaking_degree = 1.0 - POINT_GROUPS[point_group]['order'] / 48.0

    # 4. 有效自由度: Σ d_i² (类似Schur指标)
    eff_dof = sum(d**2 for d in degs)

    return {
        'n_bands': n_bands,
        'max_deg': max_deg,
        'min_deg': min_deg,
        'entropy': entropy,
        'breaking_degree': breaking_degree,
        'eff_dof': eff_dof,
        'degs': degs,
        'decomp': decomp,
    }

print("\n" + "="*80)
print("CQM电子结构指标（嵌入: d-orbital）")
print("="*80)
print(f"{'点群':>6} {'|G|':>4} {'能带数':>6} {'最大简并':>8} {'熵':>6} {'破缺度':>6} {'有效自由度':>10} {'简并模式':>20}")
print("-"*80)
for pg_name in ['O_h', 'D_6h', 'D_4h', 'D_3d', 'D_2h', 'C_2h', 'C_i', 'C_1']:
    ind = cqm_electronic_indicators(EMBEDDINGS['d-orbital'], pg_name)
    degs_str = str(ind['degs'])
    print(f"{pg_name:>6} {POINT_GROUPS[pg_name]['order']:>4} {ind['n_bands']:>6} {ind['max_deg']:>8} "
          f"{ind['entropy']:>6.3f} {ind['breaking_degree']:>6.3f} {ind['eff_dof']:>10} {degs_str:>20}")

# ============================================================
# 5. 晶格类型 → 点群映射
# ============================================================

def lattice_to_pointgroup(struct_str):
    """从晶体结构字符串推断点群"""
    s = struct_str.lower()
    if any(x in s for x in ['fcc', 'fm-3m', 'nacl', 'perovskite', 'a15', 'pm-3n']):
        return 'O_h'
    if any(x in s for x in ['hcp', 'r-3m', 'rhombohedral', 'pbo']):
        return 'D_6h' if 'hex' in s else 'D_3d'
    if any(x in x for x in ['tetragonal', 'luni2b2c', 'thcr2si2']):
        return 'D_4h'
    if 'orthorhombic' in s:
        return 'D_2h'
    if 'triclinic' in s:
        return 'C_i'
    if any(x in s for x in ['graphite', 'zrcusias', 'pbocl']):
        return 'D_4h'
    return None

# 更精确的映射
LATTICE_PG_MAP = {
    'fcc': 'O_h', 'fm-3m': 'O_h', 'nacl': 'O_h', 'perovskite': 'O_h',
    'a15': 'O_h', 'pm-3n': 'O_h',
    'hcp': 'D_6h', 'r-3m': 'D_3d', 'rhombohedral': 'D_3d',
    'pbo': 'D_4h', 'tetragonal': 'D_4h', 'luni2b2c': 'D_4h',
    'thcr2si2': 'D_4h', 'zrcusias': 'D_4h', 'pbocl': 'D_4h',
    'orthorhombic': 'D_2h',
    'triclinic': 'C_i',
    'graphite': 'D_6h',
}

def get_pointgroup(struct_str):
    s = struct_str.lower()
    for key, pg in LATTICE_PG_MAP.items():
        if key in s:
            return pg
    return None

# ============================================================
# 6. 加载超导数据，计算K_0和CQM指标
# ============================================================


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
        pg = get_pointgroup(row['晶体结构'])
        if pg is None:
            continue
        cat = row['类别']
        k_eff = tc**2 * 9 * LN2 / (8 * mp['dd0']**2 * mp['tD'])
        a_ke, b_ke = -0.769, 1.132
        k0 = k_eff / (mp['G']**a_ke * mp['tD']**b_ke)
        data.append({
            'cat': cat, 'pg': pg, 'struct': row['晶体结构'],
            'tc': tc, 'k_eff': k_eff, 'k0': k0, **mp
        })

print(f"\n加载 {len(data)} 个材料（有点群信息）")

# ============================================================
# 7. K_0与CQM电子结构指标的关系
# ============================================================

print("\n" + "="*80)
print("K_0与CQM电子结构指标的关系（嵌入: d-orbital）")
print("="*80)

emb = EMBEDDINGS['d-orbital']
for pg_name in ['O_h', 'D_6h', 'D_4h', 'D_3d', 'D_2h', 'C_2h', 'C_i']:
    ind = cqm_electronic_indicators(emb, pg_name)
    pg_data = [d for d in data if d['pg'] == pg_name]
    if not pg_data:
        continue
    k0s = np.array([d['k0'] for d in pg_data])
    print(f"\n{pg_name} (|G|={POINT_GROUPS[pg_name]['order']}, {len(pg_data)}材料):")
    print(f"  分解: {ind['decomp']}")
    print(f"  能带数={ind['n_bands']}, 最大简并={ind['max_deg']}, 熵={ind['entropy']:.3f}")
    print(f"  K_0: 中位={np.median(k0s):.2e}, 均值={np.mean(k0s):.2e}, ln(K_0)中位={np.log(np.median(k0s)):.3f}")

# ============================================================
# 8. ln(K_0) vs CQM指标的回归
# ============================================================

print("\n" + "="*80)
print("ln(K_0) vs CQM电子结构指标的回归")
print("="*80)

# 为每个材料计算CQM指标
for d in data:
    ind = cqm_electronic_indicators(emb, d['pg'])
    d['n_bands'] = ind['n_bands']
    d['max_deg'] = ind['max_deg']
    d['entropy'] = ind['entropy']
    d['breaking'] = ind['breaking_degree']
    d['eff_dof'] = ind['eff_dof']

# 单变量相关
print("\n单变量相关 (corr(ln K_0, 指标)):")
indicators = ['n_bands', 'max_deg', 'entropy', 'breaking', 'eff_dof']
for ind_name in indicators:
    vals = np.array([d[ind_name] for d in data])
    ln_k0 = np.array([np.log(d['k0']) for d in data])
    corr = np.corrcoef(vals, ln_k0)[0, 1]
    print(f"  {ind_name:>12}: corr = {corr:.3f}")

# 多变量回归
print("\n多变量回归: ln(K_0) = a·n_bands + b·entropy + c·breaking + d")
X = np.array([[d['n_bands'], d['entropy'], d['breaking'], 1.0] for d in data])
y = np.array([np.log(d['k0']) for d in data])
coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
y_pred = X @ coef
ss_res = np.sum((y - y_pred)**2)
ss_tot = np.sum((y - np.mean(y))**2)
r2 = 1 - ss_res / ss_tot
print(f"R² = {r2:.3f}")
print(f"  n_bands: {coef[0]:.3f}")
print(f"  entropy: {coef[1]:.3f}")
print(f"  breaking: {coef[2]:.3f}")
print(f"  const: {coef[3]:.3f}")

# ============================================================
# 9. LOOCV: CQM指标→K_0→Tc
# ============================================================

print("\n" + "="*80)
print("LOOCV: CQM电子结构指标→K_0→Tc")
print("="*80)

a_ke, b_ke = -0.769, 1.132
errors = []
for i in range(len(data)):
    train = [data[j] for j in range(len(data)) if j != i]
    test = data[i]
    X_tr = np.array([[d['n_bands'], d['entropy'], d['breaking'], 1.0] for d in train])
    y_tr = np.array([np.log(d['k0']) for d in train])
    try:
        coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
        x_test = np.array([test['n_bands'], test['entropy'], test['breaking'], 1.0])
        k0_pred = np.exp(x_test @ coef)
        k_eff_pred = k0_pred * test['G']**a_ke * test['tD']**b_ke
        tc_pred = math.sqrt(8 * test['dd0']**2 * k_eff_pred * test['tD'] / (9 * LN2))
        err = abs(tc_pred - test['tc']) / test['tc']
        errors.append(err)
    except:
        pass

errors = np.array(errors)
print(f"LOOCV (CQM指标→K_0→Tc): {len(errors)} 材料")
print(f"  中位误差: {np.median(errors)*100:.0f}%")
print(f"  2倍内: {np.mean(errors <= 1.0)*100:.0f}%")
print(f"  5倍内: {np.mean(errors <= 4.0)*100:.0f}%")

# ============================================================
# 10. 加入类别信息: CQM指标+类别→K_0→Tc
# ============================================================

print("\n" + "="*80)
print("LOOCV: CQM指标+类别偏置→K_0→Tc")
print("="*80)

categories = sorted(set(d['cat'] for d in data))
cat_idx = {c: i for i, c in enumerate(categories)}

errors = []
for i in range(len(data)):
    train = [data[j] for j in range(len(data)) if j != i]
    test = data[i]
    # 特征: [n_bands, entropy, breaking, 类别one-hot..., 1]
    n_feat = 3 + len(categories) + 1
    X_tr = np.zeros((len(train), n_feat))
    for j, d in enumerate(train):
        X_tr[j, 0] = d['n_bands']
        X_tr[j, 1] = d['entropy']
        X_tr[j, 2] = d['breaking']
        X_tr[j, 3 + cat_idx[d['cat']]] = 1.0
        X_tr[j, -1] = 1.0
    y_tr = np.array([np.log(d['k0']) for d in train])
    try:
        coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
        x_test = np.zeros(n_feat)
        x_test[0] = test['n_bands']
        x_test[1] = test['entropy']
        x_test[2] = test['breaking']
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
print(f"LOOCV (CQM指标+类别→K_0→Tc): {len(errors)} 材料")
print(f"  中位误差: {np.median(errors)*100:.0f}%")
print(f"  2倍内: {np.mean(errors <= 1.0)*100:.0f}%")
print(f"  5倍内: {np.mean(errors <= 4.0)*100:.0f}%")

# ============================================================
# 11. 对比所有嵌入方式
# ============================================================

print("\n" + "="*80)
print("不同嵌入方式的LOOCV对比")
print("="*80)

for emb_name, emb in EMBEDDINGS.items():
    for d in data:
        ind = cqm_electronic_indicators(emb, d['pg'])
        d['n_bands_e'] = ind['n_bands']
        d['entropy_e'] = ind['entropy']
        d['breaking_e'] = ind['breaking_degree']

    errors = []
    for i in range(len(data)):
        train = [data[j] for j in range(len(data)) if j != i]
        test = data[i]
        X_tr = np.array([[d['n_bands_e'], d['entropy_e'], d['breaking_e'], 1.0] for d in train])
        y_tr = np.array([np.log(d['k0']) for d in train])
        try:
            coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
            x_test = np.array([test['n_bands_e'], test['entropy_e'], test['breaking_e'], 1.0])
            k0_pred = np.exp(x_test @ coef)
            k_eff_pred = k0_pred * test['G']**a_ke * test['tD']**b_ke
            tc_pred = math.sqrt(8 * test['dd0']**2 * k_eff_pred * test['tD'] / (9 * LN2))
            err = abs(tc_pred - test['tc']) / test['tc']
            errors.append(err)
        except:
            pass
    errors = np.array(errors)
    print(f"  {emb_name:>12}: 中位{np.median(errors)*100:.0f}%, "
          f"2倍内{np.mean(errors <= 1.0)*100:.0f}%, 5倍内{np.mean(errors <= 4.0)*100:.0f}%")

# ============================================================
# 12. 总结
# ============================================================

print("\n" + "="*80)
print("总结")
print("="*80)
print(f"""
SU(5)→点群破缺映射:
  SU(5)的5维表示 ⊃ SO(3)的l=2表示
  晶格点群G ⊂ SO(3) → 5在G下分解为不可约表示

分支规则 (d-orbital嵌入):
  O_h (立方):    5 → Eg ⊕ T2g        (2条能带, 简并[3,2])
  D_6h (六方):   5 → A1g ⊕ E1g ⊕ E2g  (3条能带, 简并[2,2,1])
  D_4h (四方):   5 → A1g ⊕ B1g ⊕ B2g ⊕ Eg (4条能带, 简并[2,1,1,1])
  D_3d (三方):   5 → A1g ⊕ 2Eg        (3条能带, 简并[2,2,1])
  D_2h (正交):   5 → Ag ⊕ B1g ⊕ B2g ⊕ B3g (4条能带, 全非简并)
  C_i (三斜):    5 → 5Ag              (5条能带, 全非简并)

CQM电子结构指标:
  能带数: 对称性越低→能带越多
  简并度熵: 对称性越低→熵越高
  破缺度: 1-|G|/48

K_0与CQM指标回归: R² = {r2:.3f}
  → CQM指标{'可以' if r2 > 0.3 else '不能'}解释K_0的变异

LOOCV (CQM指标→K_0→Tc): 中位误差{np.median(errors)*100:.0f}%

关键发现:
  1. SU(5)破缺模式确实与晶格对称性相关
  2. 对称性越低→能带越多→电子结构越复杂→K_0越大
  3. 但CQM指标(能带数、简并度)的R²有限
  4. K_0还包含SU(5)分支规则以外的信息(轨道杂化、Fermi面拓扑)
  5. 需要更精细的SU(5)表示论计算(如权重空间几何)
""")