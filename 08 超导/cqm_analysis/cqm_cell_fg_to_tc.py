"""CQM晶胞FG：从晶体结构到Tc的统一计算链（优化版）

只取中心原子+最近邻构造局部Regge剖分，避免大系统梯度计算。
"""
import numpy as np
import os
import sys
from scipy.spatial import Delaunay, ConvexHull

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cqm_framework'))
from crystal_db import get_crystal, generate_atom_positions
from atom_db import atom_db

BETA = 8 * np.pi + 1
C_SQUARED = 2.0 / 3.0
HBAR = 1.054571817e-34
KB = 1.380649e-23
AMU_TO_KG = 1.66054e-27
ANGSTROM_TO_M = 1e-10
GAMMA_1 = 14.134725
GAMMA_2 = 21.022040


def solid_angle(v0, v1, v2, v3):
    """四面体(v0,v1,v2,v3)在v0处的立体角"""
    a = v1 - v0; b = v2 - v0; c = v3 - v0
    det_abc = np.dot(a, np.cross(b, c))
    na, nb, nc = np.linalg.norm(a), np.linalg.norm(b), np.linalg.norm(c)
    denom = na*nb*nc + np.dot(a,b)*nc + np.dot(a,c)*nb + np.dot(b,c)*na
    if abs(denom) < 1e-15:
        return 0.0
    return 2.0 * np.arctan(abs(det_abc) / denom)


def compute_angle_deficits_3d(positions, tetrahedra):
    """3D逐顶点立体角亏 δ_v = 4π - ΣΩ_f"""
    n = len(positions)
    if n == 0 or len(tetrahedra) == 0:
        return np.zeros(n)
    sa_sums = np.zeros(n)
    for tet in tetrahedra:
        verts = [positions[tet[j]] for j in range(4)]
        for i in range(4):
            center = verts[i]
            others = [verts[j] for j in range(4) if j != i]
            sa_sums[tet[i]] += solid_angle(center, others[0], others[1], others[2])
    return 4 * np.pi - sa_sums


def construct_local_regge(positions, center_idx, nn_dist):
    """构造中心原子+最近邻的局部Regge剖分

    取中心原子和其最近邻，用ConvexHull+Delaunay构造四面体网格。
    """
    # 找最近邻（距离 < 1.5 * nn_dist）
    dists = np.array([np.linalg.norm(positions[i] - positions[center_idx])
                      for i in range(len(positions))])
    local_indices = np.where(dists < 1.5 * nn_dist)[0]

    if len(local_indices) < 5:
        return np.array([]), [], []

    local_positions = positions[local_indices]

    # Delaunay三角剖分
    try:
        tri = Delaunay(local_positions)
    except Exception:
        return np.array([]), [], []

    tetrahedra = []
    edges_set = set()

    for tet in tri.simplices:
        verts = local_positions[tet]
        max_edge = max(np.linalg.norm(verts[i] - verts[j])
                       for i in range(4) for j in range(i+1, 4))
        if max_edge < 1.5 * nn_dist:
            tetrahedra.append(tuple(tet))
            for i in range(4):
                for j in range(i+1, 4):
                    edges_set.add((min(tet[i], tet[j]), max(tet[i], tet[j])))

    return local_positions, list(edges_set), tetrahedra


def build_dynamical_matrix_3d(positions, edges, masses):
    """3D弹簧网络动力学矩阵"""
    n = len(positions)
    if n == 0:
        return np.zeros((0, 0))

    K = np.zeros((n * 3, n * 3))
    for i, j in edges:
        delta = positions[i] - positions[j]
        l = np.linalg.norm(delta)
        if l < 1e-10:
            continue
        n_vec = delta / l
        k = C_SQUARED / l**2
        for a in range(3):
            for b in range(3):
                val = k * n_vec[a] * n_vec[b]
                K[i*3+a, i*3+a] += val
                K[j*3+b, j*3+b] += val
                K[i*3+a, j*3+b] -= val
                K[j*3+b, i*3+a] -= val

    D = np.zeros_like(K)
    for a in range(n * 3):
        for b in range(n * 3):
            ia, ib = a // 3, b // 3
            if ia < len(masses) and ib < len(masses):
                mp = masses[ia] * masses[ib]
                if mp > 0:
                    D[a, b] = K[a, b] / np.sqrt(mp)
    return D


def compute_gradient_local(positions, tetrahedra, center_idx, eps=1e-4):
    """只计算中心原子角亏对所有原子位置的梯度

    grad[i*3+alpha] = ∂δ_{center}/∂p_{i,alpha}
    """
    n = len(positions)
    if n == 0 or len(tetrahedra) == 0:
        return np.zeros(n * 3)

    grad = np.zeros(n * 3)
    for i in range(n):
        for alpha in range(3):
            pos_plus = positions.copy()
            pos_minus = positions.copy()
            pos_plus[i, alpha] += eps
            pos_minus[i, alpha] -= eps

            d_plus = compute_angle_deficits_3d(pos_plus, tetrahedra)
            d_minus = compute_angle_deficits_3d(pos_minus, tetrahedra)

            grad[i*3+alpha] = (d_plus[center_idx] - d_minus[center_idx]) / (2 * eps)
    return grad


def cell_fg_to_tc(symbol, delta_v_override=None):
    """从晶胞FG计算元素Tc"""
    crystal = get_crystal(symbol)
    if crystal is None:
        return 0.0, {'error': f'No crystal data for {symbol}'}

    mass_amu, theta_D, struct_type, lattice_params, n_nn = crystal
    results = {'symbol': symbol, 'structure': struct_type, 'theta_D': theta_D}

    # 生成3D原子位置
    all_positions = generate_atom_positions(struct_type, lattice_params, n_shells=2)
    if len(all_positions) == 0:
        return 0.0, {'error': 'No positions'}

    # 找中心原子
    dists_origin = np.array([np.linalg.norm(p) for p in all_positions])
    center_idx = np.argmin(dists_origin)

    # 最近邻距离
    all_dists = np.array([np.linalg.norm(all_positions[i] - all_positions[center_idx])
                          for i in range(len(all_positions))])
    all_dists[center_idx] = np.inf
    nn_dist = np.min(all_dists)

    # 构造局部Regge剖分
    local_pos, edges, tetrahedra = construct_local_regge(all_positions, center_idx, nn_dist)
    if len(tetrahedra) == 0:
        return 0.0, {**results, 'error': 'No tetrahedra'}

    # 重新找center在local中的索引
    local_dists = np.array([np.linalg.norm(local_pos[i] - all_positions[center_idx])
                            for i in range(len(local_pos))])
    local_center = np.argmin(local_dists)

    results['n_atoms'] = len(local_pos)
    results['n_tetrahedra'] = len(tetrahedra)
    results['nn_dist'] = nn_dist

    # 步骤A：3D角亏
    deficits = compute_angle_deficits_3d(local_pos, tetrahedra)

    if delta_v_override is not None:
        delta_v = delta_v_override
    else:
        delta_v = abs(deficits[local_center])
    results['delta_v'] = delta_v
    results['beta_delta_v'] = BETA * delta_v

    # 步骤B：动力学矩阵
    mass_kg = mass_amu * AMU_TO_KG
    masses = np.array([mass_kg] * len(local_pos))
    D = build_dynamical_matrix_3d(local_pos, edges, masses)

    # 步骤C：声子谱
    eigenvalues, eigenvectors = np.linalg.eigh(D)
    mask = eigenvalues > 1e-10
    n_modes = np.sum(mask)
    results['n_modes'] = n_modes

    if n_modes == 0:
        return 0.0, {**results, 'error': 'No phonon modes'}

    lambda_q = eigenvalues[mask]
    e_q = eigenvectors[:, mask]
    lambda_max = np.max(lambda_q)

    omega_D = KB * theta_D / HBAR
    omega_q = omega_D * np.sqrt(lambda_q / lambda_max)

    # 步骤D：角亏涨落
    grad = compute_gradient_local(local_pos, tetrahedra, local_center)

    n = len(local_pos)
    inv_sqrt_m = np.zeros(n * 3)
    for i in range(n):
        for a in range(3):
            inv_sqrt_m[i*3+a] = 1.0 / np.sqrt(masses[i])

    l_char = nn_dist * ANGSTROM_TO_M

    delta_fluct = 0.0
    for qi in range(n_modes):
        G_q = np.dot(grad * inv_sqrt_m, e_q[:, qi])
        delta_fluct += G_q**2 / omega_q[qi]

    delta_fluct *= HBAR / (2 * l_char**2)
    results['delta_fluct'] = delta_fluct

    # 步骤F：Tc
    Tc, x, is_sc = step_f_tc(delta_v, delta_fluct, theta_D)
    results['x'] = x
    results['is_superconducting'] = is_sc
    results['Tc'] = Tc

    return Tc, results


def step_f_tc(delta_v, delta_fluct, theta_D):
    if 1 - BETA * delta_v < 1e-15:
        return 0.0, 0.0, False
    x = 3 * BETA**2 * delta_fluct / (16 * (1 - BETA * delta_v) * (GAMMA_2 - GAMMA_1))
    if x <= 1.0:
        return 0.0, x, False
    arccoth_x = 0.5 * np.log((x + 1) / (x - 1))
    if arccoth_x < 1e-15:
        return 0.0, x, False
    return theta_D / (2 * arccoth_x), x, True


if __name__ == '__main__':
    print("=" * 70)
    print("CQM晶胞FG：从晶体结构到Tc")
    print("δ_v从元素FG(纤维丛和乐) + Δδ₀²从晶胞FG(3D声子谱)")
    print("=" * 70)

    # 加载元素FG表获取δ_v
    import json
    table_path = os.path.join(os.path.dirname(__file__), 'element_fg_table.json')
    with open(table_path, 'r', encoding='utf-8') as f:
        element_table = json.load(f)
    delta_v_table = {e['symbol']: e.get('physical_delta_v', 0) for e in element_table}

    known_sc = {
        'Nb': 9.25, 'Pb': 7.2, 'V': 5.4, 'Ta': 4.48, 'Hg': 4.15,
        'Sn': 3.72, 'In': 3.41, 'Tl': 2.39, 'Re': 1.7, 'Al': 1.19,
        'Mo': 0.92, 'Zn': 0.85, 'Os': 0.66, 'Zr': 0.61, 'Cd': 0.52,
        'Ru': 0.49, 'Ti': 0.4, 'Hf': 0.13, 'Ir': 0.11, 'Be': 0.026,
        'W': 0.015,
    }
    non_sc = ['Cu', 'Ag', 'Au', 'Ni', 'Cr', 'Fe', 'Mg', 'Rh', 'Pd', 'Pt', 'Th']

    print(f"\n{'元素':>4s} {'结构':>4s} {'N':>4s} {'δ_v':>10s} {'βδ_v':>8s} {'Δδ₀²':>12s} {'x':>10s} {'Tc预测':>10s} {'Tc实验':>10s} {'超导?':>4s}")
    print("-" * 85)

    for symbol in sorted(known_sc.keys()):
        # 用元素FG的δ_v
        dv_override = delta_v_table.get(symbol, None)
        Tc, res = cell_fg_to_tc(symbol, delta_v_override=dv_override)
        if 'error' in res:
            print(f"{symbol:>4s} ERROR: {res['error']}")
            continue
        Tc_exp = known_sc[symbol]
        print(f"{symbol:>4s} {res['structure']:>4s} {res['n_atoms']:4d} {res['delta_v']:10.6f} {res['beta_delta_v']:8.4f} "
              f"{res['delta_fluct']:12.4e} {res['x']:10.4f} {Tc:10.4f} {Tc_exp:10.4f} "
              f"{'是' if res['is_superconducting'] else '否':>4s}")

    print(f"\n--- 非超导元素（对照）---")
    for symbol in non_sc:
        dv_override = delta_v_table.get(symbol, None)
        Tc, res = cell_fg_to_tc(symbol, delta_v_override=dv_override)
        if 'error' in res:
            print(f"{symbol:>4s} ERROR: {res['error']}")
            continue
        print(f"{symbol:>4s} {res['structure']:>4s} {res['n_atoms']:4d} {res['delta_v']:10.6f} {res['beta_delta_v']:8.4f} "
              f"{res['delta_fluct']:12.4e} {res['x']:10.4f} {Tc:10.4f} {'--':>10s} "
              f"{'是' if res['is_superconducting'] else '否':>4s}")

    print("\n完成。")
