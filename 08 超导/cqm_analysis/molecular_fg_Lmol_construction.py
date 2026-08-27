"""
分子FG同步算符结构项 L_mol 的点群表示论构造

从CQM纤维丛语言出发（FG层级文档 §6.2）：
  L_mol = Σ_Γ λ_Γ^mol · Π_Γ^mol

其中:
- Γ 遍历分子点群的不可约表示
- Π_Γ^mol = (d_Γ/|G|) Σ_g χ_Γ(g)* ρ(g) 是点群投影算符
- λ_Γ^mol = μ_Γ - μ_min，μ_Γ是嘉当矩阵谱在该表示扇区的重心

验证: H₂, CH₄, NH₃, H₂O 的分子轨道能级排序
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework')
from atom_db import ATOM_DB
import math
import numpy as np
from itertools import product

A4 = np.array([[2,-1,0,0],[-1,2,-1,0],[0,-1,2,-1],[0,0,-1,2]])

RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832]


# ============================================================
# Part 1: 点群不可约表示
# ============================================================

def td_irreps():
    """T_d群的不可约表示（特征标表）
    T_d群 |G|=24，5个不可约表示: A1(1), A2(1), E(2), T1(3), T2(3)
    共轭类: E(1), 8C3(8), 3C2(3), 6S4(6), 6σd(6)
    """
    classes = ['E', 'C3', 'C2', 'S4', 'sigma_d']
    class_sizes = [1, 8, 3, 6, 6]
    irrep_names = ['A1', 'A2', 'E', 'T1', 'T2']
    irrep_dims = [1, 1, 2, 3, 3]
    # 特征标表 [行=irrep, 列=class]
    characters = np.array([
        [1,  1,  1,  1,  1],   # A1
        [1,  1,  1, -1, -1],   # A2
        [2, -1,  2,  0,  0],   # E
        [3,  0, -1,  1, -1],   # T1
        [3,  0, -1, -1,  1],   # T2
    ])
    return {
        'name': 'T_d', 'order': 24,
        'classes': classes, 'class_sizes': class_sizes,
        'irrep_names': irrep_names, 'irrep_dims': irrep_dims,
        'characters': characters
    }


def d4h_irreps():
    """D_4h群的不可约表示（特征标表）
    D_4h群 |G|=16，10个不可约表示（都是1维或2维）
    简化: 只用D4部分（|G|=8，5个不可约表示）
    """
    classes = ['E', 'C4', 'C2', "C2'", 'C2d']
    class_sizes = [1, 2, 1, 2, 2]
    irrep_names = ['A1', 'A2', 'B1', 'B2', 'E']
    irrep_dims = [1, 1, 1, 1, 2]
    characters = np.array([
        [1,  1,  1,  1,  1],   # A1
        [1,  1,  1, -1, -1],   # A2
        [1, -1,  1,  1, -1],   # B1
        [1, -1,  1, -1,  1],   # B2
        [2,  0, -2,  0,  0],   # E
    ])
    return {
        'name': 'D4', 'order': 8,
        'classes': classes, 'class_sizes': class_sizes,
        'irrep_names': irrep_names, 'irrep_dims': irrep_dims,
        'characters': characters
    }


def c2v_irreps():
    """C_2v群的不可约表示（特征标表）
    C_2v群 |G|=4，4个1维不可约表示
    """
    classes = ['E', 'C2', 'sv', "sv'"]
    class_sizes = [1, 1, 1, 1]
    irrep_names = ['A1', 'A2', 'B1', 'B2']
    irrep_dims = [1, 1, 1, 1]
    characters = np.array([
        [1,  1,  1,  1],   # A1
        [1,  1, -1, -1],   # A2
        [1, -1,  1, -1],   # B1
        [1, -1, -1,  1],   # B2
    ])
    return {
        'name': 'C2v', 'order': 4,
        'classes': classes, 'class_sizes': class_sizes,
        'irrep_names': irrep_names, 'irrep_dims': irrep_dims,
        'characters': characters
    }


# ============================================================
# Part 2: 分子嘉当矩阵构造
# ============================================================

def build_molecular_cartan(atoms):
    """构造分子嘉当矩阵 C_mol = ⊕_k C_el(k) + Σ T_ij"""
    els = list(atoms.keys())
    n_elem = len(els)
    if n_elem == 0:
        return None

    blocks = []
    for el in els:
        count = int(atoms[el])
        if count > 0:
            blocks.append(np.kron(np.eye(count), A4))
        else:
            blocks.append(A4.copy())

    total_dim = sum(b.shape[0] for b in blocks)
    C_mol = np.zeros((total_dim, total_dim))
    offset = 0
    dims = []
    for b in blocks:
        d = b.shape[0]
        C_mol[offset:offset+d, offset:offset+d] = b
        dims.append(d)
        offset += d

    for i in range(n_elem):
        for j in range(i+1, n_elem):
            ri = ATOM_DB[els[i]][2]
            rj = ATOM_DB[els[j]][2]
            dij = abs(ri - rj)
            lam = max(ri, rj)
            t0 = 0.1 * math.exp(-dij / lam)
            si = sum(dims[:i])
            sj = sum(dims[:j])
            for k in range(min(4, C_mol.shape[0]-si, C_mol.shape[0]-sj)):
                if si+k < C_mol.shape[0] and sj+k < C_mol.shape[0]:
                    C_mol[si+k, sj+k] = -t0
                    C_mol[sj+k, si+k] = -t0

    return C_mol


# ============================================================
# Part 3: L_mol 构造
# ============================================================

def compute_lambda_gamma(C_mol, irrep_info, n_orbital_basis):
    """从嘉当矩阵谱计算各不可约表示扇区的谱重心

    λ_Γ^mol = μ_Γ - μ_min
    μ_Γ = (1/|扇区_Γ|) Σ λ∈扇区_Γ λ
    """
    eigvals = np.sort(np.linalg.eigvalsh(C_mol))
    n_total = len(eigvals)

    chars = irrep_info['characters']
    dims = irrep_info['irrep_dims']
    order = irrep_info['order']
    class_sizes = irrep_info['class_sizes']
    n_irreps = len(dims)

    # 每个不可约表示在n_orbital_basis维空间中出现的次数
    # a_Γ = (1/|G|) Σ_class |class| * χ_Γ(class) * χ_reg(class)
    # 对于正则表示，χ_reg(E)=n_basis, χ_reg(g≠E)=0
    # 所以 a_Γ = (d_Γ/n_basis) * n_basis = d_Γ（正则表示中每个irrep出现d_Γ次）
    # 但我们不用正则表示，用n_orbital_basis维的自然表示
    # 简化：按维度比例分配本征值

    lambda_gamma = {}
    idx = 0
    for i, name in enumerate(irrep_info['irrep_names']):
        d = dims[i]
        # 该表示在谱中占据 d * (n_total / sum(d^2)) 个本征值
        # sum(d^2) = |G|（对于完整群）
        # 简化：按d^2比例分配
        n_sector = max(1, int(round(n_total * d**2 / sum(dd**2 for dd in dims))))

        if idx + n_sector <= n_total:
            sector_eigvals = eigvals[idx:idx+n_sector]
            idx += n_sector
        else:
            sector_eigvals = eigvals[idx:]
            idx = n_total

        mu_gamma = np.mean(sector_eigvals) if len(sector_eigvals) > 0 else 0
        lambda_gamma[name] = mu_gamma

    # λ_Γ = μ_Γ - μ_min
    mu_min = min(lambda_gamma.values())
    for name in lambda_gamma:
        lambda_gamma[name] = lambda_gamma[name] - mu_min

    return lambda_gamma


def construct_Lmol(C_mol, irrep_info):
    """构造 L_mol = Σ_Γ λ_Γ · Π_Γ

    简化实现：L_mol是对角矩阵，对角元为各扇区的λ_Γ值
    """
    n = C_mol.shape[0]
    eigvals, eigvecs = np.linalg.eigh(C_mol)

    dims = irrep_info['irrep_dims']
    n_irreps = len(dims)

    # 按不可约表示维度比例分配本征值到扇区
    Lmol = np.zeros((n, n))
    idx = 0
    lambda_vals = compute_lambda_gamma(C_mol, irrep_info, n)

    for i, name in enumerate(irrep_info['irrep_names']):
        d = dims[i]
        n_sector = max(1, int(round(n * d**2 / sum(dd**2 for dd in dims))))
        n_sector = min(n_sector, n - idx)

        if n_sector > 0:
            lam = lambda_vals[name]
            for k in range(n_sector):
                if idx + k < n:
                    Lmol[idx+k, idx+k] = lam
            idx += n_sector

    return Lmol, lambda_vals


# ============================================================
# Part 4: 分子轨道谱计算
# ============================================================

def compute_molecular_orbitals(atoms, point_group_name):
    """计算分子轨道谱 E_mol(n, Γ) = N(γ_n) + λ_Γ^mol"""
    C_mol = build_molecular_cartan(atoms)
    if C_mol is None:
        return None

    if point_group_name == 'T_d':
        irrep_info = td_irreps()
    elif point_group_name == 'D4':
        irrep_info = d4h_irreps()
    elif point_group_name == 'C2v':
        irrep_info = c2v_irreps()
    else:
        return None

    Lmol, lambda_vals = construct_Lmol(C_mol, irrep_info)

    # 分子轨道能级 E_mol(n, Γ) = N(γ_n) + λ_Γ^mol
    # N(γ_n) = n（黎曼零点计数函数的序号）
    n_basis = C_mol.shape[0]
    orbital_energies = []

    for n in range(1, n_basis + 1):
        N_gamma = n  # 序号语境
        for gamma_name, lam in lambda_vals.items():
            E = N_gamma + lam
            orbital_energies.append((E, n, gamma_name))

    orbital_energies.sort(key=lambda x: x[0])
    return orbital_energies, lambda_vals, irrep_info


# ============================================================
# Part 5: 小分子验证
# ============================================================

TEST_MOLECULES = [
    ('H2',  {'H': 2},  'C2v',  ['sigma_g', 'sigma_u']),
    ('CH4', {'C': 1, 'H': 4}, 'T_d',   ['A1', 'T2', 'A1', 'T2']),
    ('NH3', {'N': 1, 'H': 3}, 'C2v',   ['A1', 'E', 'A1', 'E']),
    ('H2O', {'O': 1, 'H': 2}, 'C2v',   ['A1', 'B2', 'A1', 'B1']),
]

print("="*70)
print("分子FG同步算符 L_mol 的点群表示论构造")
print("="*70)

for name, atoms, pg, expected_order in TEST_MOLECULES:
    result = compute_molecular_orbitals(atoms, pg)
    if result is None:
        print(f"\n{name}: 无法计算")
        continue

    orbitals, lambda_vals, irrep_info = result

    print(f"\n{'─'*50}")
    print(f"分子: {name}  点群: {irrep_info['name']}  原子: {atoms}")
    print(f"  λ_Γ^mol: {lambda_vals}")
    print(f"  分子轨道能级排序（前10）:")
    for i, (E, n, gamma) in enumerate(orbitals[:10]):
        print(f"    {i+1:2d}. E={E:7.3f}  (n={n}, Γ={gamma})")

print(f"\n{'─'*50}")
print("判据：轨道能级排序是否复现实验填充顺序")
print("  CH₄: A1 < T2 < A1 < T2 （成键σ < 反键σ*）")
print("  H₂O: A1 < B2 < A1 < B1 （2a1 < 1b2 < 3a1 < 1b1）")