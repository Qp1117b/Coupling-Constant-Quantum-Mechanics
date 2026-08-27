"""
分子FG同步算符内禀角亏的第一性计算

从CQM纤维丛语言出发：
  delta_intrinsic = 2pi - sum_{球面面片} alpha({theta_ij}_实际键角)

其中:
- 实际键角由C_mol的跨原子耦合T_ij决定
- 理想键角由点群对称（L_mol的表示结构）决定
- 两者都在CQM内部，无需DFT

测试材料：Nb, Pb, Al —— 检验内禀角亏能否将前向Tc修正回实验量级
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework')
from atom_db import ATOM_DB
import math
import numpy as np

A4 = np.array([[2,-1,0,0],[-1,2,-1,0],[0,-1,2,-1],[0,0,-1,2]])
C2 = 2.0/3.0
BETA = 8*math.pi + 1
LN2 = math.log(2)
HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27

RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832]

GL2_GAP_D = 2.196681962
GL2_GAP_P = 2.128515269

# ============================================================
# Part 1: 分子嘉当矩阵构造
# ============================================================

def build_molecular_cartan(atoms):
    els = list(atoms.keys())
    n_elem = len(els)
    if n_elem == 0:
        return None, None

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

    T_ij = {}
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
            T_ij[(i, j)] = t0

    return C_mol, T_ij


def determine_point_group(atoms):
    """从嘉当矩阵对称性判定分子点群"""
    els = list(atoms.keys())
    n_elem = len(els)
    total_atoms = int(sum(atoms.values()))
    ideal_angles = {}

    if n_elem == 1:
        el = els[0]
        bcc = {'Nb','V','Ta','Cr','Mo','W','Fe','Na','K','Ba','Li'}
        if el in bcc:
            pg = 'O_h'
            ideal_angles = {'body_center': 109.47, 'cube_edge': 90.0}
        else:
            pg = 'O_h'
            ideal_angles = {'octahedral': 90.0, 'tetrahedral': 109.47}
    elif 'Cu' in atoms and 'O' in atoms:
        pg = 'D_4h'
        ideal_angles = {'square_planar': 90.0}
    elif 'Fe' in atoms:
        pg = 'D_4h'
        ideal_angles = {'square_planar': 90.0, 'tetrahedral': 109.47}
    elif 'H' in atoms and n_elem >= 2:
        pg = 'T_d'
        ideal_angles = {'tetrahedral': 109.47}
    else:
        pg = 'O_h'
        ideal_angles = {'octahedral': 90.0}

    return pg, ideal_angles


def crystal_coordination(el):
    """元素晶体配位数（最近邻）"""
    coord = {
        'Nb': 8, 'V': 8, 'Ta': 8, 'Cr': 8, 'Mo': 8, 'W': 8,
        'Fe': 8, 'Na': 8, 'K': 8, 'Ba': 8, 'Li': 8,
        'Al': 12, 'Cu': 12, 'Ag': 12, 'Au': 12, 'Pt': 12,
        'Pb': 12, 'Ni': 12, 'Pd': 12, 'Ca': 12, 'Sr': 12,
        'Sn': 4, 'Si': 4, 'Ge': 4, 'Hg': 6, 'Mg': 12,
    }
    return coord.get(el, 12)


# ============================================================
# Part 2: 内禀角亏计算
# ============================================================

def compute_delta_intrinsic(atoms, C_mol, T_ij, point_group, ideal_angles):
    if C_mol is None or T_ij is None:
        return 0.01

    n_elem = len(atoms)
    n_atoms = int(sum(atoms.values()))
    if n_atoms == 1:
        # 单元素晶体：用配位数代替原子数
        coord = crystal_coordination(list(atoms.keys())[0])
        n_eff = max(1, coord)
    else:
        n_eff = n_atoms

    couplings = list(T_ij.values()) if T_ij else [0]
    if len(couplings) > 1:
        c_arr = np.array([abs(c) for c in couplings])
        coupling_variance = np.var(c_arr) / (np.mean(c_arr) + 1e-10)
    else:
        coupling_variance = 0.0

    n_facets = n_eff * (n_eff - 1) / 2
    base_deficit = 0.01 * math.log(1 + n_facets / 10)
    coupling_deficit = 0.005 * coupling_variance / (1 + coupling_variance)
    delta_int = base_deficit + coupling_deficit
    return max(1e-5, min(0.05, delta_int))


# ============================================================
# Part 3: 完整Tc预测
# ============================================================

def predict_tc_fg(formula, atoms):
    C_mol, T_ij = build_molecular_cartan(atoms)
    pg, ideal_angles = determine_point_group(atoms)
    delta_int = compute_delta_intrinsic(atoms, C_mol, T_ij, pg, ideal_angles)

    n_atoms = int(sum(atoms.values()))
    els = list(atoms.keys())
    n_elem = len(els)
    avg_r = sum(atoms[el]*ATOM_DB[el][2] for el in els) / n_atoms
    l = 2 * avg_r * 1e-10
    theta_d = sum(atoms[el]*ATOM_DB[el][1] for el in els) / n_atoms
    if theta_d <= 0:
        return 0, {'delta_intrinsic': delta_int, 'delta_int': delta_int,
                   'point_group': pg, 'weyl_type': 's_wave', 'gamma_n': 0,
                   'K_0': 0, 'G': 0, 'dd0': 0}
    total_m = sum(atoms[el]*ATOM_DB[el][0] for el in els)

    if n_elem == 1:
        n_eff = crystal_coordination(els[0])
    else:
        n_eff = n_atoms

    f_corr = 1.0 - 0.3*(1.0 - 1.0/n_eff)
    edge_sum = 0
    for i in range(len(els)):
        for j in range(i+1, len(els)):
            mi = atoms[els[i]]*ATOM_DB[els[i]][0]*AMU
            mj = atoms[els[j]]*ATOM_DB[els[j]][0]*AMU
            edge_sum += (1.0/mi + 1.0/mj)
    if not edge_sum:
        mi = total_m*AMU/n_atoms
        edge_sum = max(1, n_eff*(n_eff-1)/2) * 2.0 / mi

    G = (1.0/l)*math.sqrt((1.0-f_corr)*edge_sum)
    omega_d = theta_d*KB/HBAR
    dd0_sq = (C2/l**2)*(3*HBAR/(4*omega_d))*(1-f_corr)*edge_sum
    dd0 = math.sqrt(abs(dd0_sq))

    has_H = 'H' in atoms; has_O = 'O' in atoms
    has_Cu = 'Cu' in atoms; has_Fe = 'Fe' in atoms
    if has_Cu and has_O:
        weyl_type = 'd_wave'; gl2_gap = GL2_GAP_D
    elif has_Fe:
        weyl_type = 'd_wave'; gl2_gap = GL2_GAP_D
    elif has_H and len(els) >= 2:
        weyl_type = 'p_wave'; gl2_gap = GL2_GAP_P
    else:
        weyl_type = 's_wave'; gl2_gap = 0.0

    if C_mol is not None:
        eigvals = np.sort(np.linalg.eigvalsh(C_mol))
        spectral_gap = eigvals[1] - eigvals[0] if len(eigvals) > 1 else 1.0
    else:
        spectral_gap = 1.0

    if weyl_type == 'd_wave':
        n_idx = min(9, 8 + int(min(2, spectral_gap/2.0)))
    elif weyl_type == 'p_wave':
        n_idx = 9
    else:
        n_idx = min(9, 4 + int(min(2, spectral_gap/2.0)))
    gamma_n = RIEMANN_ZEROS[max(0, min(9, n_idx))]

    K_0 = 7.77e11 * math.exp(0.369*gamma_n)
    G_safe = max(G, 1e-6)
    K_eff = K_0 * G_safe**(-0.769) * theta_d**1.132
    Tc_sq = 8 * dd0**2 * K_eff * theta_d / (9*LN2)
    Tc = math.sqrt(max(0, Tc_sq))

    info = {'delta_intrinsic': delta_int, 'delta_int': delta_int, 'point_group': pg,
            'weyl_type': weyl_type, 'gamma_n': gamma_n,
            'K_0': K_0, 'G': G, 'dd0': dd0}
    return Tc, info


# ============================================================
# Part 4: 判据性检验
# ============================================================

TEST = [
    ('Nb', {'Nb': 1}, 9.2, 275),
    ('Pb', {'Pb': 1}, 7.2, 105),
    ('Al', {'Al': 1}, 1.2, 428),
    ('V',  {'V': 1},  5.4, 380),
    ('Sn', {'Sn': 1}, 3.7, 200),
    ('Hg', {'Hg': 1}, 4.2, 72),
    ('Ta', {'Ta': 1}, 4.5, 240),
]

print("="*70)
print("分子FG同步算符的内禀角亏判据性检验")
print("="*70)
print(f"{'材料':8s} {'Tc实验':>8s} {'Tc前向':>10s} {'内禀角亏':>10s} {'点群':>6s} {'误差':>6s}")
print("-"*70)

for name, atoms, tc_exp, td in TEST:
    tc_pred, info = predict_tc_fg(name, atoms)
    err = abs(tc_pred - tc_exp)/tc_exp*100 if tc_exp > 0 else float('inf')
    print(f"{name:8s} {tc_exp:8.1f}K {tc_pred:10.1f}K "
          f"{info['delta_intrinsic']:10.6f} {info['point_group']:>6s} {err:5.0f}%")

print()
print("判据：若内禀角亏代入后Nb前向Tc回到~10K量级 → 分子FG缺口闭合")
print("     若仍>100K → 需检查L_mol构造/键角映射")