"""CQM元素晶体结构数据库

包含常压下元素超导体的晶体结构数据：
- 晶系、空间群、晶格常数、Wyckoff位置
- 数据来源：实验X射线衍射
"""

# 元素晶体结构表
# 格式: 'symbol': (mass_amu, debye_T_K, structure_type, lattice_params, n_neighbors)
# structure_type: 'BCC', 'FCC', 'HCP', 'TET', 'RHL', 'ORT'
# lattice_params: (a,) for cubic, (a,c) for HCP/tet, (a,b,c) for orthorhombic
# n_neighbors: 最近邻配位数

CRYSTAL_DB = {
    # BCC (Im-3m, 229) - 2 atoms/cell, positions: (0,0,0), (1/2,1/2,1/2)
    'Nb': (92.91, 275, 'BCC', (3.30,), 8),
    'V':  (50.94, 383, 'BCC', (3.02,), 8),
    'Ta': (180.95, 240, 'BCC', (3.31,), 8),
    'Mo': (95.96, 425, 'BCC', (3.15,), 8),
    'W':  (183.84, 400, 'BCC', (3.16,), 8),
    'Cr': (52.00, 435, 'BCC', (2.88,), 8),
    'Fe': (55.85, 470, 'BCC', (2.87,), 8),
    'Ba': (137.33, 110, 'BCC', (5.02,), 8),
    'Li': (6.94, 344, 'BCC', (3.49,), 8),

    # FCC (Fm-3m, 225) - 4 atoms/cell, positions: (0,0,0), (0,1/2,1/2), (1/2,0,1/2), (1/2,1/2,0)
    'Pb': (207.20, 105, 'FCC', (4.95,), 12),
    'Al': (26.98, 428, 'FCC', (4.05,), 12),
    'Ir': (192.22, 420, 'FCC', (3.83,), 12),
    'Rh': (102.91, 480, 'FCC', (3.80,), 12),
    'Pd': (106.42, 274, 'FCC', (3.89,), 12),
    'Pt': (195.08, 240, 'FCC', (3.92,), 12),
    'Cu': (63.55, 343, 'FCC', (3.61,), 12),
    'Ag': (107.87, 215, 'FCC', (4.09,), 12),
    'Au': (196.97, 170, 'FCC', (4.08,), 12),
    'Ni': (58.69, 450, 'FCC', (3.52,), 12),
    'Ca': (40.08, 230, 'FCC', (5.58,), 12),
    'Th': (232.04, 163, 'FCC', (5.08,), 12),

    # HCP (P6_3/mmc, 194) - 2 atoms/cell, positions: (1/3,2/3,1/4), (2/3,1/3,3/4)
    'Tc':  (98.00, 450, 'HCP', (2.74, 4.39), 12),
    'Tl':  (204.38, 78, 'HCP', (3.46, 5.52), 12),
    'Re':  (186.21, 430, 'HCP', (2.76, 4.46), 12),
    'Zn':  (65.38, 327, 'HCP', (2.66, 4.95), 12),
    'Os':  (190.23, 500, 'HCP', (2.74, 4.32), 12),
    'Zr':  (91.22, 291, 'HCP', (3.23, 5.15), 12),
    'Cd':  (112.41, 209, 'HCP', (2.98, 5.62), 12),
    'Ru':  (101.07, 540, 'HCP', (2.71, 4.28), 12),
    'Ti':  (47.87, 420, 'HCP', (2.95, 4.68), 12),
    'Hf':  (178.49, 252, 'HCP', (3.20, 5.05), 12),
    'Be':  (9.01, 1440, 'HCP', (2.29, 3.58), 12),
    'Mg':  (24.31, 400, 'HCP', (3.21, 5.21), 12),
    'Co':  (58.93, 445, 'HCP', (2.51, 4.07), 12),
    'Lu':  (174.97, 200, 'HCP', (3.50, 5.55), 12),
    'Sc':  (44.96, 360, 'HCP', (3.31, 5.27), 12),
    'Y':   (88.91, 280, 'HCP', (3.65, 5.73), 12),
    'La':  (138.91, 142, 'HCP', (3.75, 6.07), 12),  # α-La dhcp, 用hcp近似
    'Gd':  (157.25, 200, 'HCP', (3.64, 5.78), 12),

    # Tetragonal (I4_1/amd for β-Sn, I4/mmm for In)
    'Sn':  (118.71, 200, 'TET', (5.83, 3.18), 6),   # β-Sn (白锡)
    'In':  (114.82, 108, 'TET', (4.59, 4.94), 12),  # 面心四方

    # Rhombohedral (R-3m for Hg)
    'Hg':  (200.59, 72, 'RHL', (3.46, 6.71), 6),    # a=3.46, c=6.71 (六角 Setting)
}


def get_crystal(symbol):
    """获取元素晶体结构数据

    返回: (mass_amu, debye_T, structure_type, lattice_params, n_neighbors)
    """
    return CRYSTAL_DB.get(symbol, None)


def generate_atom_positions(structure_type, lattice_params, n_shells=2):
    """生成晶胞+近邻的3D原子位置

    n_shells: 包含的近邻壳层数（1=最近邻，2=次近邻）
    返回: positions (N, 3) in Angstrom
    """
    import numpy as np

    if structure_type == 'BCC':
        a = lattice_params[0]
        # BCC: 原子在 (0,0,0) + (1/2,1/2,1/2) + 整数平移
        basis = np.array([[0, 0, 0], [0.5, 0.5, 0.5]]) * a
        # 生成超胞
        positions = []
        for nx in range(-n_shells, n_shells + 1):
            for ny in range(-n_shells, n_shells + 1):
                for nz in range(-n_shells, n_shells + 1):
                    for b in basis:
                        pos = b + np.array([nx, ny, nz]) * a
                        positions.append(pos)
        return np.array(positions)

    elif structure_type == 'FCC':
        a = lattice_params[0]
        basis = np.array([[0, 0, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0]]) * a
        positions = []
        for nx in range(-n_shells, n_shells + 1):
            for ny in range(-n_shells, n_shells + 1):
                for nz in range(-n_shells, n_shells + 1):
                    for b in basis:
                        pos = b + np.array([nx, ny, nz]) * a
                        positions.append(pos)
        return np.array(positions)

    elif structure_type == 'HCP':
        a, c = lattice_params
        # HCP六角晶胞: 原子在 (1/3,2/3,1/4) 和 (2/3,1/3,3/4)
        # 用正交近似: a1=(a,0,0), a2=(a/2, a*√3/2, 0), a3=(0,0,c)
        a1 = np.array([a, 0, 0])
        a2 = np.array([a / 2, a * np.sqrt(3) / 2, 0])
        a3 = np.array([0, 0, c])
        basis_frac = np.array([[1/3, 2/3, 1/4], [2/3, 1/3, 3/4]])
        positions = []
        for n1 in range(-n_shells, n_shells + 1):
            for n2 in range(-n_shells, n_shells + 1):
                for n3 in range(-n_shells, n_shells + 1):
                    for b in basis_frac:
                        pos = b[0] * a1 + b[1] * a2 + b[2] * a3 + \
                              n1 * a1 + n2 * a2 + n3 * a3
                        positions.append(pos)
        return np.array(positions)

    elif structure_type == 'TET':
        a, c = lattice_params
        # 四方晶胞 (In: 面心四方, Sn: 体心四方)
        if lattice_params[0] > 5:  # β-Sn
            basis = np.array([[0, 0, 0], [0.5, 0.5, 0.5]]) * np.array([a, a, c])
        else:  # In
            basis = np.array([[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5]]) * np.array([a, a, c])
        positions = []
        for nx in range(-n_shells, n_shells + 1):
            for ny in range(-n_shells, n_shells + 1):
                for nz in range(-n_shells, n_shells + 1):
                    for b in basis:
                        pos = b + np.array([nx * a, ny * a, nz * c])
                        positions.append(pos)
        return np.array(positions)

    elif structure_type == 'RHL':
        a, c = lattice_params
        # 六角Setting的RHL: Hg
        a1 = np.array([a, 0, 0])
        a2 = np.array([a / 2, a * np.sqrt(3) / 2, 0])
        a3 = np.array([0, 0, c])
        basis_frac = np.array([[0, 0, 0], [1/3, 2/3, 1/3], [2/3, 1/3, 2/3]])
        positions = []
        for n1 in range(-n_shells, n_shells + 1):
            for n2 in range(-n_shells, n_shells + 1):
                for n3 in range(-n_shells, n_shells + 1):
                    for b in basis_frac:
                        pos = b[0] * a1 + b[1] * a2 + b[2] * a3 + \
                              n1 * a1 + n2 * a2 + n3 * a3
                        positions.append(pos)
        return np.array(positions)

    return np.array([])


def find_neighbors(positions, center_idx, n_neighbors):
    """找到离center_idx最近的n_neighbors个原子的索引"""
    import numpy as np
    dists = np.array([np.linalg.norm(positions[i] - positions[center_idx])
                      for i in range(len(positions))])
    dists[center_idx] = np.inf  # 排除自己
    indices = np.argsort(dists)[:n_neighbors]
    return indices, dists[indices]