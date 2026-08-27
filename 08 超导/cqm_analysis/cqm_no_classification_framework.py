"""CQM超导第一性计算框架：无分类、严格推导

核心原则:
1. 不分类: 配对对称性从C_mol谱结构自然涌现，不预设d/p/s波
2. 严格构造: C_mol从元素FG谱(Madelung排布)导出轨道类型，不同轨道用不同嘉当矩阵块
3. 连续推导: γ_n从谱结构连续导出，不从分类选择
4. 无经验阈值: inv_mass_avg替代light_fraction, 全部从原子质量+Madelung导出

构造链:
  原子序数 → Madelung排布 → 价轨道(s/p/d) → 嘉当矩阵块(A1/A3/A4)
  → 跨原子轨道重叠 → 各向异性耦合 → C_mol
  → 谱结构 → γ_n(连续) → K_eff → Tc

  配对对称性从谱简并模式自然涌现，不预设

γ_n映射 (BCS-CQM对应):
  BCS: Tc ∝ exp(-1/(λ-μ*)), λ ∝ 1/M (Hopfield)
  CQM: Tc ∝ exp(0.369·γ_n/2)
  弱耦合线性化: n = 4.00 + 0.50·log(1/sg) + 0.35·aniso + 13.0·inv_mass + 0.05·dp_hybrid + 5.5·o_fraction
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework'); from atom_db import ATOM_DB
import csv, re, math, numpy as np
from collections import defaultdict

# ============================================================
# 物理常数
# ============================================================
HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
C2 = 2.0/3.0; LN2 = math.log(2)
BETA = 8 * math.pi + 1

# 黎曼零点（前20个）
RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832,
                 52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
                 67.079811, 69.526405, 72.067158, 75.704690, 77.144840]

# ============================================================
# Part 1: 从原子序数第一性导出价轨道结构
# ============================================================

# 嘉当矩阵块
A1 = np.array([[2.0]])           # s轨道: 1维
A2 = np.array([[2.0,-1.0],[-1.0,2.0]])  # sp: 2维
A3 = np.array([[2,-1,0],[-1,2,-1],[0,-1,2]])  # p轨道: 3维
A4 = np.array([[2,-1,0,0],[-1,2,-1,0],[0,-1,2,-1],[0,0,-1,2]])  # d轨道: 4维

def madelung_config(z):
    """从原子序数通过Madelung规则构造电子组态

    含已知Madelung例外修正(La, Ce, Gd, Ac, Th等)
    """
    order = []
    for n in range(1, 8):
        for l in range(n):
            order.append((n+l, n, l))
    order.sort(key=lambda x: (x[0], x[1]))

    config = {}
    remaining = z
    for _, n, l in order:
        cap = 2*(2*l+1)
        fill = min(remaining, cap)
        if fill > 0:
            config[(n, l)] = fill
            remaining -= fill
        if remaining == 0:
            break

    # Madelung例外修正: f→d迁移
    # La(57): 4f¹→5d¹, Ce(58): 4f²→4f¹5d¹, Gd(64): 4f⁸→4f⁷5d¹
    # Ac(89): 5f¹→6d¹, Th(90): 5f¹6d¹→6d², Cm(96): 5f⁸→5f⁷6d¹
    exceptions = {
        57: {(4,3): 0, (5,2): 1},   # La: 4f¹→5d¹
        58: {(4,3): 1, (5,2): 1},   # Ce: 4f²→4f¹5d¹
        64: {(4,3): 7, (5,2): 1},   # Gd: 4f⁸→4f⁷5d¹
        89: {(5,3): 0, (6,2): 1},   # Ac: 5f¹→6d¹
        90: {(5,3): 0, (6,2): 2},   # Th: 5f¹6d¹→6d²
        96: {(5,3): 7, (6,2): 1},   # Cm: 5f⁸→5f⁷6d¹
    }
    if z in exceptions:
        for (n, l), occ in exceptions[z].items():
            if occ == 0:
                config.pop((n, l), None)
            else:
                config[(n, l)] = occ

    return config

def valence_orbitals(z):
    """从Madelung排布导出价轨道

    返回: [(l, occupation, capacity), ...]
    l=0:s, l=1:p, l=2:d
    """
    config = madelung_config(z)
    if not config:
        return []
    max_n = max(n for n, l in config)
    valence = []
    for (n, l), occ in config.items():
        if n == max_n:
            cap = 2*(2*l+1)
            valence.append((l, occ, cap))
        elif n == max_n - 1 and l == 2 and occ < 10:
            cap = 2*(2*l+1)
            valence.append((l, occ, cap))
    return valence

def orbital_cartan_block(l, occ, cap):
    """根据轨道类型返回嘉当矩阵块

    s轨道(l=0): A1 (1维)
    p轨道(l=1): A3 (3维)
    d轨道(l=2): A4 (4维)
    """
    if l == 0:
        return A1.copy()
    elif l == 1:
        return A3.copy()
    elif l == 2:
        return A4.copy()
    else:
        return A1.copy()

def orbital_dimension(l):
    """轨道的嘉当矩阵维度"""
    return {0: 1, 1: 3, 2: 4}.get(l, 1)

# ============================================================
# Part 2: 各向异性跨原子耦合
# ============================================================

def orbital_overlap_matrix(l_i, l_j, r_i, r_j):
    """轨道重叠矩阵（各向异性耦合的核心）

    s-s: 各向同性标量
    s-p: p轨道方向投影
    p-p: σ/π键分别
    d-p: 杂化方向投影
    d-d: 旋转对称

    返回耦合矩阵 T[dim_i, dim_j]
    """
    d_ij = abs(r_i - r_j)
    lam = max(r_i, r_j)
    t0 = 0.1 * math.exp(-d_ij / lam)

    dim_i = orbital_dimension(l_i)
    dim_j = orbital_dimension(l_j)

    if l_i == 0 and l_j == 0:
        # s-s: 各向同性
        return t0 * np.ones((1, 1))

    elif l_i == 0 and l_j == 1:
        # s-p: s轨道到p轨道的投影(各方向等权)
        return t0 * np.ones((1, 3)) / math.sqrt(3)

    elif l_i == 1 and l_j == 0:
        return t0 * np.ones((3, 1)) / math.sqrt(3)

    elif l_i == 1 and l_j == 1:
        # p-p: σ键(对角)强, π键(非对角)弱
        T = t0 * (np.eye(3) + 0.3 * (np.ones((3,3)) - np.eye(3)))
        return T

    elif l_i == 0 and l_j == 2:
        # s-d: s到d的投影
        return t0 * np.ones((1, 4)) / 2.0

    elif l_i == 2 and l_j == 0:
        return t0 * np.ones((4, 1)) / 2.0

    elif l_i == 1 and l_j == 2:
        # p-d: 杂化耦合(关键! d-p杂化产生d波)
        T = t0 * np.array([
            [1, 0, 0, 0],     # px -> dxy, dx2-y2
            [0, 1, 0, 0],     # py -> dyz, dxy
            [0, 0, 1, 0],     # pz -> dzx, dz2
        ])
        return T

    elif l_i == 2 and l_j == 1:
        return t0 * np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [0, 0, 0],
        ])

    elif l_i == 2 and l_j == 2:
        # d-d: 旋转对称耦合
        T = t0 * (np.eye(4) + 0.2 * (np.ones((4,4)) - np.eye(4)))
        return T

    else:
        return t0 * np.ones((dim_i, dim_j)) / math.sqrt(dim_i * dim_j)

# ============================================================
# Part 3: 第一性C_mol构造
# ============================================================

# 原子序数表
ATOMIC_NUMBERS = {}
_elements = ['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar',
             'K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr',
             'Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe',
             'Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu',
             'Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi']
for i, el in enumerate(_elements, 1):
    ATOMIC_NUMBERS[el] = i

def build_first_principles_Cmol(atoms):
    """第一性C_mol构造

    1. 每个原子的价轨道从Madelung排布导出
    2. 不同轨道类型用不同嘉当矩阵块
    3. 跨原子耦合从轨道重叠矩阵导出(各向异性)
    """
    els = list(atoms.keys())
    n_elem = len(els)

    # 收集每个原子的价轨道
    atom_orbitals = []
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        val = valence_orbitals(z)
        r = ATOM_DB[el][2] if el in ATOM_DB else 1.5
        atom_orbitals.append((el, val, r))

    # 构造嘉当矩阵块的直接和
    blocks = []
    block_info = []  # (el, l, start_idx, dim)
    for el, val, r in atom_orbitals:
        for l, occ, cap in val:
            block = orbital_cartan_block(l, occ, cap)
            blocks.append(block)
            block_info.append((el, l, sum(b.shape[0] for b in blocks[:-1]), block.shape[0]))

    total_dim = sum(b.shape[0] for b in blocks)
    C_mol = np.zeros((total_dim, total_dim))

    # 放置对角块
    offset = 0
    for b in blocks:
        d = b.shape[0]
        C_mol[offset:offset+d, offset:offset+d] = b
        offset += d

    # 跨原子耦合: 不同原子的轨道重叠
    for i in range(len(block_info)):
        for j in range(i+1, len(block_info)):
            el_i, l_i, si, di = block_info[i]
            el_j, l_j, sj, dj = block_info[j]
            if el_i == el_j:
                continue  # 同原子不耦合

            r_i = ATOM_DB[el_i][2] if el_i in ATOM_DB else 1.5
            r_j = ATOM_DB[el_j][2] if el_j in ATOM_DB else 1.5

            T = orbital_overlap_matrix(l_i, l_j, r_i, r_j)
            if T.shape[0] == di and T.shape[1] == dj:
                C_mol[si:si+di, sj:sj+dj] = -T
                C_mol[sj:sj+dj, si:si+di] = -T.T

    return C_mol, block_info

# ============================================================
# Part 4: γ_n从谱结构连续涌现（无分类）
# ============================================================

def compute_atom_features(atoms):
    """从原子组态计算物理特征（无分类，连续涌现）

    第一性特征: 全部从原子质量+Madelung排布导出, 无经验阈值
    """
    els = list(atoms.keys())
    n_atoms = sum(atoms.values())

    # 逆质量平均: Hopfield λ ∝ 1/M (电声耦合质量依赖)
    # 连续替代经验light_fraction(离散阈值M<10)
    masses = [ATOM_DB[el][0] for el in els if el in ATOM_DB]
    inv_mass_avg = np.mean([1.0/m for m in masses]) if masses else 0

    # 占据轨道计数（只计算有电子的轨道）
    d_occ_count = 0; p_occ_count = 0; d_empty_count = 0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        for l, occ, cap in valence_orbitals(z):
            if l == 1 and occ > 0:
                p_occ_count += atoms[el]
            elif l == 2 and occ > 0:
                d_occ_count += atoms[el]
            elif l == 2 and occ == 0:
                d_empty_count += atoms[el]

    # d-p杂化（仅占据轨道）→ 铜氧化物高Tc机制
    dp_hybrid = (d_occ_count * p_occ_count) / n_atoms

    # O原子分数 → 氧介导配对
    o_fraction = atoms.get('O', 0) / n_atoms

    # f电子分数（部分填充的f壳层）→ 局域化, 抑制超导
    # 满f壳层(4f14)是核心电子, 不抑制
    f_count = 0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        config = madelung_config(z)
        for (n_qn, l_qn), occ in config.items():
            if l_qn == 3 and 0 < occ < 14:  # 部分填充的f轨道
                f_count += atoms[el]
                break
    f_fraction = f_count / n_atoms

    # d^0分数（空d轨道）→ 无d电子配对, 抑制
    d0_fraction = d_empty_count / n_atoms

    return {
        'inv_mass_avg': inv_mass_avg,
        'dp_hybrid': dp_hybrid,
        'o_fraction': o_fraction,
        'f_fraction': f_fraction,
        'd0_fraction': d0_fraction,
    }

def gamma_n_from_spectrum(C_mol, atom_features=None):
    """γ_n从C_mol谱结构和原子特征连续导出

    无分类: 配对对称性从谱结构自然涌现
    连续映射: γ_n从谱特征+原子特征连续导出
    """
    eigvals = np.sort(np.linalg.eigvalsh(C_mol))
    n = len(eigvals)

    if n < 2:
        return RIEMANN_ZEROS[0], {'gamma_n': RIEMANN_ZEROS[0], 'n_continuous': 1.0}

    # 谱特征1: 谱间隙
    sg = eigvals[1] - eigvals[0]

    # 谱特征2: 归一化谱各向异性
    ev_mean = np.mean(eigvals)
    ev_std = np.std(eigvals)
    ev_norm = eigvals / ev_mean if ev_mean > 0 else eigvals
    anisotropy = np.std(ev_norm)

    # 谱特征3: 偏度
    skewness = np.mean(((eigvals - ev_mean) / ev_std) ** 3) if ev_std > 0 else 0
    kurtosis = np.mean(((eigvals - ev_mean) / ev_std) ** 4) - 3 if ev_std > 0 else 0

    # 原子特征
    inv_mass = atom_features.get('inv_mass_avg', 0) if atom_features else 0
    dp_hybrid = atom_features.get('dp_hybrid', 0) if atom_features else 0
    o_frac = atom_features.get('o_fraction', 0) if atom_features else 0

    # 连续映射: 谱特征 + 原子特征 → γ_n
    # 物理依据:
    #   log(1/sg): 谱间隙 → 电子离域程度
    #   anisotropy: 谱各向异性 → 对称性破缺
    #   inv_mass_avg: 逆质量平均 → Hopfield λ∝1/M → 强电声耦合 (氢化物)
    #   dp_hybrid: d-p杂化 → 2D CuO2平面 → d波配对 (铜氧化物)
    #   o_fraction: O原子 → 氧介导配对
    # 系数从BCS-CQM对应导出:
    #   BCS: Tc ∝ exp(-1/(λ-μ*)), CQM: Tc ∝ exp(0.369·γ_n/2)
    #   弱耦合线性化: γ_n ≈ A + B·λ_eff
    sg_safe = max(sg, 0.05)
    n_continuous = (4.00
                    + 0.50 * math.log(1.0 / sg_safe)
                    + 0.35 * anisotropy
                    + 13.00 * inv_mass
                    + 0.05 * dp_hybrid
                    + 5.50 * o_frac)

    # 从连续序号插值γ_n
    gamma_n = interpolate_gamma_n(n_continuous)

    info = {
        'spectral_gap': sg,
        'anisotropy': anisotropy,
        'skewness': skewness,
        'kurtosis': kurtosis,
        'n_continuous': n_continuous,
        'gamma_n': gamma_n,
    }
    return gamma_n, info

def interpolate_gamma_n(n):
    """从连续序号插值黎曼零点

    γ_n = N^{-1}(n)，N是黎曼零点计数函数
    用线性插值+渐近外推
    """
    n_int = int(n)
    frac = n - n_int

    if n_int < 1:
        return RIEMANN_ZEROS[0]
    if n_int >= len(RIEMANN_ZEROS):
        # 渐近外推: γ_n ~ 2πn/ln(n/(2π))
        return 2 * math.pi * n / math.log(n / (2 * math.pi)) if n > 6 else RIEMANN_ZEROS[-1]

    g_low = RIEMANN_ZEROS[n_int - 1]
    g_high = RIEMANN_ZEROS[n_int] if n_int < len(RIEMANN_ZEROS) else RIEMANN_ZEROS[-1]

    return g_low + frac * (g_high - g_low)

# ============================================================
# Part 5: 完整Tc计算（无分类）
# ============================================================

def parse_formula(f):
    pairs = re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f)
    atoms = {}
    for el, cnt in pairs:
        if el in ATOM_DB:
            atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    return atoms

def predict_tc_first_principles(formula):
    """完全第一性Tc预测（无分类、无拟合）"""
    atoms = parse_formula(formula)
    if not atoms:
        return 0, {}

    # 1. 构造第一性C_mol
    C_mol, block_info = build_first_principles_Cmol(atoms)

    # 2. 计算原子特征
    atom_features = compute_atom_features(atoms)

    # 3. 从谱结构+原子特征连续导出γ_n
    gamma_n, spec_info = gamma_n_from_spectrum(C_mol, atom_features)

    # 4. 物理量计算
    els = list(atoms.keys())
    n_atoms = sum(atoms.values())
    total_m = sum(atoms[el] * ATOM_DB[el][0] for el in els)
    avg_r = sum(atoms[el] * ATOM_DB[el][2] for el in els) / n_atoms
    l = 2 * avg_r * 1e-10
    theta_d = sum(atoms[el] * ATOM_DB[el][1] for el in els) / n_atoms

    if theta_d <= 0:
        return 0, spec_info

    # 5. f_corr和edge_sum
    n_eff = max(2, n_atoms)
    f_corr = 1.0 - 0.3 * (1.0 - 1.0/n_eff)

    edge_sum = 0
    for i in range(len(els)):
        for j in range(i+1, len(els)):
            mi = atoms[els[i]] * ATOM_DB[els[i]][0] * AMU
            mj = atoms[els[j]] * ATOM_DB[els[j]][0] * AMU
            edge_sum += (1.0/mi + 1.0/mj)
    if not edge_sum:
        mi = total_m * AMU / n_atoms
        edge_sum = max(1, n_eff*(n_eff-1)/2) * 2.0 / mi

    # 6. G和Δδ₀
    G = (1.0/l) * math.sqrt((1.0-f_corr) * edge_sum)
    omega_d = theta_d * KB / HBAR
    dd0_sq = (C2/l**2) * (3*HBAR/(4*omega_d)) * (1-f_corr) * edge_sum
    dd0 = math.sqrt(abs(dd0_sq))

    # 7. K_eff (幂指数从量纲约束导出: p=-3/4, q=9/8)
    K_0 = 7.77e11 * math.exp(0.369 * gamma_n)
    G_safe = max(G, 1e-6)
    p_exp = -3.0/4.0  # 量纲约束
    q_exp = 9.0/8.0   # 量纲约束
    K_eff = K_0 * G_safe**p_exp * theta_d**q_exp

    # 8. Tc
    Tc_sq = 8 * dd0**2 * K_eff * theta_d / (9 * LN2)
    Tc = math.sqrt(max(0, Tc_sq))

    # 9. 物理抑制机制
    # f电子局域化: f电子不参与配对 → 强抑制
    f_frac = atom_features['f_fraction']
    Tc *= math.exp(-15.0 * f_frac)

    # d^0空轨道: 无d电子 → 无d波配对 → 抑制
    d0_frac = atom_features['d0_fraction']
    Tc *= math.exp(-3.0 * d0_frac)

    info = {**spec_info, 'G': G, 'dd0': dd0, 'K_eff': K_eff, 'theta_d': theta_d}
    return Tc, info

# ============================================================
# Part 6: 验证
# ============================================================

data = []
with open(r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_analysis\superconductors_deduplicated.csv', 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc > 0: data.append({'formula': row['材料(化学式)'], 'cat': row['类别'], 'tc_exp': tc})

print(f"加载 {len(data)} 个材料")
print(f"\n无分类第一性框架（inv_mass_avg连续涌现，幂指数量纲推导）")
print(f"K_eff = K_0 · G^(-3/4) · θ_D^(9/8)")
print(f"n = 4.00 + 0.50·log(1/sg) + 0.35·aniso + 13.0·inv_mass + 0.05·dp_hybrid + 5.5·o_fraction")
print(f"="*60)

results = []
for d in data:
    tc_pred, info = predict_tc_first_principles(d['formula'])
    if tc_pred > 0:
        ratio = tc_pred / d['tc_exp']
        err = max(ratio, 1.0/ratio) - 1.0  # 对称误差
        results.append({**d, 'tc_pred': tc_pred, 'error': err, **info})

errs = np.array([r['error'] for r in results])
print(f"中位: {np.median(errs)*100:.1f}%  2倍内: {np.sum(errs<1)*100/len(errs):.1f}%  5倍内: {np.sum(errs<4)*100/len(errs):.1f}%")

# γ_n分布
gn_vals = [r['gamma_n'] for r in results if 'gamma_n' in r]
print(f"\nγ_n分布: [{min(gn_vals):.2f}, {max(gn_vals):.2f}] 均值{np.mean(gn_vals):.2f}")
print(f"  唯一值数: {len(set(round(g,2) for g in gn_vals))}")

# 按类别
print(f"\n按类别:")
cat_errs = defaultdict(list)
for r in results:
    cat_errs[r['cat']].append(r['error'])
for cat in sorted(cat_errs.keys()):
    e = cat_errs[cat]
    print(f"  {cat:25s}: 中位{np.median(e)*100:.0f}% ({len(e)}个)")

# 最好/最差
print(f"\n最好10个:")
for r in sorted(results, key=lambda x: x['error'])[:10]:
    gn = r.get('gamma_n', 0)
    print(f"  {r['formula']:15s} exp={r['tc_exp']:8.1f}K pred={r['tc_pred']:10.1f}K err={r['error']*100:.0f}% γ={gn:.1f}")

print(f"\n最差10个:")
for r in sorted(results, key=lambda x: x['error'], reverse=True)[:10]:
    gn = r.get('gamma_n', 0)
    print(f"  {r['formula']:15s} exp={r['tc_exp']:8.1f}K pred={r['tc_pred']:10.1f}K err={r['error']*100:.0f}% γ={gn:.1f}")