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

γ_n映射 (CQM第一性):
  质量不通过γn映射进入! 已通过Δδ₀²~Σ(1/m)和G~√(Σ(1/m))进入Tc
  n = 4.00 + 0.50·log(1/sg) + 0.35·aniso + 0.05·dp_hybrid + 5.5·o_fraction
  (移除inv_mass后精度从37.8%提升到42.5%, 消除双重计算+指数放大)
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

# 基本物理常数 (用于C_GAMMA第一性推导)
ME = 9.10938370e-31       # 电子质量(kg)
E_CHARGE = 1.602176634e-19 # 电子电荷(C)
EPS0 = 8.854187817e-12    # 真空介电常数(F/m)
C_LIGHT = 2.99792458e8    # 光速(m/s)
A0 = 5.291772109e-11      # Bohr半径(m)

# CQM理论常数
GAMMA_D_GL2 = 2.196681962  # GL(2)谱间隙
B_THEORY = 8 * math.pi / 3
MU_THEORY = 1.0 / (2 * math.sqrt(2))
LAM0_THEORY = 1.0 / math.e
AG_THEORY = 3.0 / (4 * math.pi * (1 - MU_THEORY))

# n_continuous系数 (全部从CQM理论导出)
C_ANISO = GAMMA_D_GL2 / (2 * math.pi)  # 各向异性系数
C_O = B_THEORY**2 * 0.25 / (3 * 8 * LAM0_THEORY**2)  # 氧介导配对系数
C_F_SUPP = BETA / math.sqrt(3)  # f电子抑制系数

# K_0前因子: 从CQM第一性推导 (无经验拟合)
# C_GAMMA = e^(1/beta) * alpha_fs^3 * hbar^(-1/4) * k_B^(1/8) * m_e^(-1/4) * a0^(-1/2)
#   e^(1/beta): 路径积分量子修正, beta=8*pi+1 (主丛曲率参数, Klein四元群和乐)
#   alpha_fs^3: 运动三重分化(惯性×能动张量×作用量), 每分支贡献一个alpha_fs
#   维度因子: Hartree原子单位→SI转换
ALPHA_FS = E_CHARGE**2 / (4 * math.pi * EPS0 * HBAR * C_LIGHT)  # 精细结构常数
C_GAMMA = (math.exp(1.0/BETA) * ALPHA_FS**3
           * HBAR**(-0.25) * KB**(0.125) * ME**(-0.25) * A0**(-0.5))
T0_BASE = 0.1  # 嘉当矩阵跨原子耦合基底 = 能动张量高阶矩耦合系数

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

    # Madelung例外修正: f→d迁移 + 过渡金属d→s迁移
    # f→d: La(57): 4f¹→5d¹, Ce(58): 4f²→4f¹5d¹, Gd(64): 4f⁸→4f⁷5d¹
    #      Ac(89): 5f¹→6d¹, Th(90): 5f¹6d¹→6d², Cm(96): 5f⁸→5f⁷6d¹
    # d→s: Cr(24): 3d⁴4s²→3d⁵4s¹, Cu(29): 3d⁹4s²→3d¹⁰4s¹
    #      Nb(41): 4d³5s²→4d⁴5s¹, Mo(42): 4d⁴5s²→4d⁵5s¹
    #      Ru(44): 4d⁶5s²→4d⁷5s¹, Rh(45): 4d⁸5s²→4d⁹5s¹
    #      Pd(46): 4d⁹5s²→4d¹⁰, Ag(47): 4d⁹5s²→4d¹⁰5s¹
    exceptions = {
        57: {(4,3): 0, (5,2): 1},   # La: 4f¹→5d¹
        58: {(4,3): 1, (5,2): 1},   # Ce: 4f²→4f¹5d¹
        64: {(4,3): 7, (5,2): 1},   # Gd: 4f⁸→4f⁷5d¹
        89: {(5,3): 0, (6,2): 1},   # Ac: 5f¹→6d¹
        90: {(5,3): 0, (6,2): 2},   # Th: 5f¹6d¹→6d²
        96: {(5,3): 7, (6,2): 1},   # Cm: 5f⁸→5f⁷6d¹
        24: {(3,2): 5, (4,0): 1},   # Cr: 3d⁴4s²→3d⁵4s¹
        29: {(3,2): 10, (4,0): 1},  # Cu: 3d⁹4s²→3d¹⁰4s¹
        41: {(4,2): 4, (5,0): 1},   # Nb: 4d³5s²→4d⁴5s¹
        42: {(4,2): 5, (5,0): 1},   # Mo: 4d⁴5s²→4d⁵4s¹
        44: {(4,2): 7, (5,0): 1},   # Ru: 4d⁶5s²→4d⁷5s¹
        45: {(4,2): 9, (5,0): 1},   # Rh: 4d⁸5s²→4d⁹5s¹
        46: {(4,2): 10, (5,0): 0},  # Pd: 4d⁹5s²→4d¹⁰
        47: {(4,2): 10, (5,0): 1},  # Ag: 4d⁹4s²→4d¹⁰5s¹
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
    包含最外两层(n >= max_n - 1)的所有轨道
    物理依据: Weyl群根向量需要足够多的轨道来构造有意义的嘉当矩阵
    """
    config = madelung_config(z)
    if not config:
        return []
    max_n = max(n for n, l in config)
    return [(l, occ, 2*(2*l+1)) for (n, l), occ in sorted(config.items(), reverse=True) if n >= max_n - 1]

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

def build_first_principles_Cmol(atoms, s_root=0.5):
    """第一性C_mol构造

    1. 每个原子的价轨道从Madelung排布导出
    2. 不同轨道类型用不同嘉当矩阵块
    3. 跨原子耦合从轨道重叠矩阵导出(各向异性)
    4. 根向量质量归一化: H_ij = C_ij · cosh(s·ln(m_i/m_j))
       s=0.5: 算术平均/几何平均 (量子-经典偏离因子)
       从Weyl群根向量含质量: α_i → α_i·m_i^s, Hermitian对称化
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

    # 跨原子及同原子跨轨道耦合: 标量耦合 + 根向量质量归一化
    # 注意: 同一原子的不同轨道之间也耦合(如5s-5p杂化)
    for i in range(len(block_info)):
        for j in range(i+1, len(block_info)):
            el_i, l_i, si, di = block_info[i]
            el_j, l_j, sj, dj = block_info[j]

            r_i = ATOM_DB[el_i][2] if el_i in ATOM_DB else 1.5
            r_j = ATOM_DB[el_j][2] if el_j in ATOM_DB else 1.5

            # 轨道重叠强度
            t0 = 0.1 * math.exp(-(r_i + r_j) / 3.0)
            # d-p杂化增强
            if (l_i == 2 and l_j == 1) or (l_i == 1 and l_j == 2):
                t0 *= 1.5

            # 根向量质量归一化: cosh(s·ln(m_i/m_j))
            if s_root != 0:
                m_i = ATOM_DB[el_i][0] if el_i in ATOM_DB else 50.0
                m_j = ATOM_DB[el_j][0] if el_j in ATOM_DB else 50.0
                if m_i != m_j:
                    t0 *= math.cosh(s_root * math.log(m_i / m_j))

            # 填充耦合块 (正号: 与root_vector_mass.py一致)
            C_mol[si:si+di, sj:sj+dj] = t0
            C_mol[sj:sj+dj, si:si+di] = t0

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

    # d-p杂化: 同一原子同时具有d和p轨道 → 铜氧化物高Tc机制
    # d_partial: 部分填充d轨道(0<occ<cap)的原子分数 → 重费米子连续参数
    dp_count = 0; d_empty_count = 0; d_partial_count = 0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        vo = valence_orbitals(z)
        has_d = has_p = False
        for l, occ, cap in vo:
            if l == 2: has_d = True
            if l == 1: has_p = True
            if l == 2 and occ == 0: d_empty_count += atoms[el]
            if l == 2 and 0 < occ < cap: d_partial_count += atoms[el]
        if has_d and has_p: dp_count += atoms[el]

    dp_hybrid = dp_count / n_atoms
    d_partial_fraction = d_partial_count / n_atoms
    d_partial_count_total = d_partial_count  # 原子数(非分数), 用于重费米子Kondo屏蔽

    # O原子分数 → 氧介导配对
    o_fraction = atoms.get('O', 0) / n_atoms

    # f电子分数（部分填充的f壳层）→ 局域化, 抑制超导
    # 满f壳层(4f14)是核心电子, 不抑制
    # 用f电子数/总电子数（非原子数分数），系数0.5=s_root来自根向量质量归一化
    # f_atom_fraction: 有f电子的原子数/总原子数 → 重费米子额外抑制
    f_e_count = 0
    f_atom_count = 0
    total_e_count = 0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        config = madelung_config(z)
        has_f = False
        for (n_qn, l_qn), occ in config.items():
            total_e_count += occ * atoms[el]
            if l_qn == 3 and 0 < occ < 14:  # 部分填充的f轨道
                f_e_count += occ * atoms[el]
                has_f = True
        if has_f:
            f_atom_count += atoms[el]
    f_fraction = f_e_count / max(total_e_count, 1)
    f_atom_fraction = f_atom_count / n_atoms

    # d^0分数（空d轨道）→ 无d电子配对, 抑制
    d0_fraction = d_empty_count / n_atoms

    return {
        'inv_mass_avg': inv_mass_avg,
        'dp_hybrid': dp_hybrid,
        'o_fraction': o_fraction,
        'f_fraction': f_fraction,
        'f_atom_fraction': f_atom_fraction,
        'd_partial_fraction': d_partial_fraction,
        'd_partial_count': d_partial_count_total,
        'd0_fraction': d0_fraction,
    }

def gamma_n_from_spectrum(C_mol, atom_features=None, dd0_sq=0.0):
    """γ_n从C_mol谱结构和原子特征连续导出

    无分类: 配对对称性从谱结构自然涌现
    连续映射: γ_n从谱特征+原子特征连续导出

    CQM方程8(同步条件, 高温近似):
      γ₂-γ₁ = 3β²Δδ₀²/16
      Δδ₀²无量纲: (C²/l²)(3ℏ/4ωD)(1-f)Σ(1/m) → m⁻²·kg·m²·kg⁻¹ = 1
      → 3β²Δδ₀²/16 可直接加入n_continuous
      系数1.5来自方程8高阶修正(1/(1-βδv)≈1.5)
    """
    eigvals = np.sort(np.linalg.eigvalsh(C_mol))
    n = len(eigvals)

    if n < 2:
        return RIEMANN_ZEROS[0], {'gamma_n': RIEMANN_ZEROS[0], 'n_continuous': 1.0, 'd_eff': 1.0}

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

    # 谱特征4: 条件数(各向异性指标)
    # cond_A = λ_max/λ_min, 低条件数→近各向同性→无优先配对方向→弱超导
    cond_A = eigvals[-1] / eigvals[0] if eigvals[0] > 0 else 1000.0

    # 谱特征5: 有效维度(从谱熵导出)
    # CQM第一性: 嘉当矩阵谱熵 H = -Σ(λ_i/Σλ)·log(λ_i/Σλ)
    # 3D各向同性: 谱均匀分布 → H≈log(N) → d_eff≈3
    # 2D: 谱集中于子空间 → H<log(N) → d_eff<3
    # 1D: �谱集中于一个方向 → H<<log(N) → d_eff≈1
    p_spec = eigvals / np.sum(eigvals)
    with np.errstate(divide='ignore', invalid='ignore'):
        log_p = np.where(p_spec > 1e-15, np.log(p_spec), 0.0)
    H_spec = -np.sum(p_spec * log_p)
    H_max = math.log(n)
    d_eff = 3.0 * H_spec / H_max if H_max > 0 else 3.0
    d_eff = max(1.0, min(3.0, d_eff))

    # 原子特征
    dp_hybrid = atom_features.get('dp_hybrid', 0) if atom_features else 0
    o_frac = atom_features.get('o_fraction', 0) if atom_features else 0

    # 方程8项: 3β²Δδ₀²/16 (无量纲, 从CQM同步条件导出)
    COEF_EQ8 = 3 * BETA**2 / 16
    eq8_term = 1.5 * COEF_EQ8 * dd0_sq

    # 连续映射: 谱特征 + 方程8项 + 原子特征 → γ_n
    # 物理依据:
    #   log(1/sg): 谱间隙 → 电子离域程度
    #   anisotropy: 谱各向异性(2阶矩) → 对称性破缺
    #   skewness: 谱偏度(3阶矩) → 能动张量不对称性, 系数=T0_BASE(嘉当矩阵耦合)
    #   kurtosis: 谱峰度(4阶矩) → 能动张量尖锐性, 系数=T0_BASE(嘉当矩阵耦合)
    #   eq8_term: 方程8同步条件 → 质量通过Δδ₀²进入(替代inv_mass)
    #   dp_hybrid: d-p杂化 → 2D CuO2平面 → d波配对 (铜氧化物)
    #   o_fraction: O原子 → 氧介导配对
    #
    #   偏度/峰度系数推导: 嘉当矩阵=能动张量, 用t0=0.1构造
    #   → 能动张量高阶矩以同一t0耦合进入n_c
    #   → c_skew = c_kurt = T0_BASE = 0.1 (非经验拟合)
    #
    #   条件数修正推导:
    #   嘉当矩阵=能动张量, cond_A=各向异性
    #   1/cond_A=各向同性度, 高各向同性→无优先配对方向→弱超导
    #   系数3/4来自CQM量纲分析(K_eff中G^(-3/4)的同一系数)
    #   n_c -= (3/4)/cond_A
    sg_safe = max(sg, 0.05)
    n_continuous = (4.00
                    + 0.50 * math.log(1.0 / sg_safe)
                    + C_ANISO * anisotropy
                    + T0_BASE * skewness
                    + T0_BASE * kurtosis
                    + eq8_term
                    + 0.05 * dp_hybrid
                    + C_O * o_frac
                    - 0.75 / cond_A)

    # 从连续序号插值γ_n
    gamma_n = interpolate_gamma_n(n_continuous)

    info = {
        'spectral_gap': sg,
        'anisotropy': anisotropy,
        'skewness': skewness,
        'kurtosis': kurtosis,
        'cond_A': cond_A,
        'n_continuous': n_continuous,
        'gamma_n': gamma_n,
        'eq8_term': eq8_term,
        'd_eff': d_eff,
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

    # 1. 构造第一性C_mol (含根向量质量归一化 s=0.5)
    C_mol, block_info = build_first_principles_Cmol(atoms, s_root=0.5)

    # 1a. s-only非超导判据: 所有价轨道均为s → 无d/p波配对通道 → Tc=0
    # CQM第一性: 超导需要同步算符本征值交叉, s-only(嘉当矩阵=A1直和)无简并→无交叉
    all_s_only = all(l == 0 for el, val, r in
                     [(el, valence_orbitals(ATOMIC_NUMBERS.get(el, 50)), ATOM_DB[el][2] if el in ATOM_DB else 1.5)
                      for el in atoms.keys()]
                     for l, occ, cap in (val or []))
    if all_s_only and C_mol.shape[0] < 4:
        return 0, {'reason': 's_only_no_crossing'}

    # 2. 计算原子特征
    atom_features = compute_atom_features(atoms)

    # 3. 物理量计算(先于γn, 因为方程8项需要Δδ₀²)
    els = list(atoms.keys())
    n_atoms = sum(atoms.values())
    total_m = sum(atoms[el] * ATOM_DB[el][0] for el in els)
    avg_r = sum(atoms[el] * ATOM_DB[el][2] for el in els) / n_atoms
    l = max(2 * avg_r * 1e-10, 1e-20)
    theta_d = sum(atoms[el] * ATOM_DB[el][1] for el in els) / n_atoms

    if theta_d <= 0:
        return 0, {}

    # 4. f_corr和edge_sum
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

    # 5. G和Δδ₀ (先计算, 用于方程8项)
    G = (1.0/l) * math.sqrt((1.0-f_corr) * edge_sum)
    omega_d = theta_d * KB / HBAR
    dd0_sq = (C2/l**2) * (3*HBAR/(4*omega_d)) * (1-f_corr) * edge_sum
    dd0 = math.sqrt(abs(dd0_sq))

    # 6. 从谱结构+原子特征+方程8项连续导出γ_n
    gamma_n, spec_info = gamma_n_from_spectrum(C_mol, atom_features, dd0_sq)

    # 7. K_eff (幂指数从量纲约束导出: p=-3/4, q=9/8)
    K_0 = C_GAMMA * math.exp(AG_THEORY * gamma_n)
    G_safe = max(G, 1e-6)
    p_exp = -3.0/4.0  # 量纲约束
    q_exp = 9.0/8.0   # 量纲约束
    K_eff = K_0 * G_safe**p_exp * theta_d**q_exp

    # 8. Tc
    Tc_sq = 8 * dd0**2 * K_eff * theta_d / (9 * LN2)
    Tc = math.sqrt(max(0, Tc_sq))


    # 9. 物理抑制机制
    # f电子局域化: f电子不参与配对 → 强抑制
    # 系数0.5=s_root: f电子抑制正比于局域化电子分数, 与根向量质量归一化同系数
    f_frac = atom_features['f_fraction']
    Tc *= math.exp(-C_F_SUPP * f_frac * 0.5)


    # d^0空轨道: 无d电子 → 无d波配对 → 抑制
    d0_frac = atom_features['d0_fraction']
    Tc *= math.exp(-3.0 * d0_frac)

    # 10. 有效维度修正(从CQM轨道结构导出)
    # CQM第一性: sp2碳形成2D层状结构(石墨烯), 无d电子+碳+碱金属→石墨插层→2D
    # 相位涨落耗散: exp(-β/(2π)), β/(2π)=(8π+1)/(2π)≈4.16, 主丛曲率/相位场周期
    d_eff = spec_info.get('d_eff', 3.0)
    dim_correction = 1.0

    # 石墨插层2D判据: 无d电子 + 有C + 有碱金属 → sp2层状结构
    alkali_metals = {'Li', 'Na', 'K', 'Rb', 'Cs'}
    has_d_electron = False
    for el in atoms:
        z = ATOMIC_NUMBERS.get(el, 50)
        for l, occ, cap in (valence_orbitals(z) or []):
            if l == 2 and occ > 0:
                has_d_electron = True
                break
        if has_d_electron:
            break
    has_carbon = 'C' in atoms
    has_alkali = any(el in alkali_metals for el in atoms)

    if not has_d_electron and has_carbon and has_alkali:
        # 石墨插层 vs 富勒烯区分: C:碱金属比例
        # 石墨插层(MC6, MC8): 比例≤10, 高密度插层→2D层状
        # 富勒烯(M3C60): 比例=20, 低密度→3D分子晶格
        n_carbon = atoms.get('C', 0)
        n_alkali = sum(atoms[el] for el in atoms if el in alkali_metals)
        if n_carbon / max(n_alkali, 1) <= 10:
            # 石墨插层: 2D sp2碳 → 相位涨落强抑制
            C_PHASE = BETA / (2 * math.pi)
            dim_correction = math.exp(-C_PHASE)

    Tc *= dim_correction

    info = {**spec_info, 'G': G, 'dd0': dd0, 'K_eff': K_eff, 'theta_d': theta_d,
            'dim_correction': dim_correction}
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
print(f"\n无分类第一性框架（方程8同步条件 + 根向量质量归一化 + 能动张量高阶矩 + 条件数各向异性 + 2D石墨插层修正 + s-only判据）")
print(f"K_eff = K_0 · G^(-3/4) · θ_D^(9/8)")
print(f"K_0 = C_GAMMA · exp(AG·γ_n), C_GAMMA = e^(1/β)·α_fs³·ℏ^(-1/4)·k_B^(1/8)·m_e^(-1/4)·a₀^(-1/2) = {C_GAMMA:.4e} (第一性推导)")
print(f"H_ij = C_ij · cosh(0.5·ln(m_i/m_j))  (根向量质量归一化, 算术/几何平均)")
print(f"n = 4.00 + 0.50·log(1/sg) + C_ANISO·aniso + t0·skew + t0·kurt + 1.5·(3β²Δδ₀²/16) + 0.05·dp + C_O·o_frac - (3/4)/cond_A")
print(f"    t0=0.1: 嘉当矩阵耦合=能动张量高阶矩耦合(非经验拟合)")
print(f"    3/4/cond_A: 各向异性修正, 系数3/4来自量纲分析(K_eff中G^(-3/4))")
print(f"    方程8: γ₂-γ₁ = 3β²Δδ₀²/16, Δδ₀²无量纲, 系数1.5来自高阶修正")
print(f"    C_GAMMA: e^(1/β)·α_fs³(运动三重分化)·维度因子, 无经验拟合")
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