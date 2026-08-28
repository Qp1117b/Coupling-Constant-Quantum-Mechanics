"""CQM晶胞FG：2D投影法从晶体结构到Tc

3D晶体几何平坦→角亏为零。投影到2D高对称面→非零角亏→反映晶面拓扑。
A: 3D晶胞→2D投影→Delaunay三角剖分→2D角亏δ_v
B: 2D动力学矩阵→声子谱
C: 角亏涨落Δδ₀²→Tc闭式
"""
import numpy as np
import os
import sys
from scipy.spatial import Delaunay

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


def project_to_2d(positions_3d, normal):
    """将3D位置投影到垂直于normal的2D面"""
    normal = np.array(normal, dtype=float)
    normal = normal / np.linalg.norm(normal)
    # 构造2D基向量（垂直于normal）
    if abs(normal[2]) < 0.9:
        e1 = np.cross(normal, [0, 0, 1])
    else:
        e1 = np.cross(normal, [1, 0, 0])
    e1 = e1 / np.linalg.norm(e1)
    e2 = np.cross(normal, e1)
    e2 = e2 / np.linalg.norm(e2)

    projected = np.column_stack([
        positions_3d @ e1,
        positions_3d @ e2
    ])
    return projected


def step_a_2d_angle_deficit(positions, faces):
    """2D逐顶点角亏 δ_v = 2π - Σθ_i"""
    n = len(positions)
    if n == 0 or len(faces) == 0:
        return np.zeros(n)

    angle_sums = np.zeros(n)
    for face in faces:
        i, j, k = face
        vi, vj, vk = positions[i], positions[j], positions[k]
        for v_idx, (a, b, c) in [(i, (vj, vi, vk)), (j, (vi, vj, vk)), (k, (vi, vk, vj))]:
            va = a - b; vb = c - b
            cos_a = np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb) + 1e-15)
            cos_a = np.clip(cos_a, -1.0, 1.0)
            angle_sums[v_idx] += np.arccos(cos_a)

    return 2 * np.pi - angle_sums


def construct_2d_regge(positions_2d, center_idx, nn_dist):
    """2D Delaunay三角剖分"""
    dists = np.array([np.linalg.norm(positions_2d[i] - positions_2d[center_idx])
                      for i in range(len(positions_2d))])
    local_mask = dists < 2.0 * nn_dist
    local_indices = np.where(local_mask)[0]

    if len(local_indices) < 4:
        return np.array([]), [], []

    local_pos = positions_2d[local_indices]

    try:
        tri = Delaunay(local_pos)
    except Exception:
        return np.array([]), [], []

    faces = []
    edges_set = set()

    for simplex in tri.simplices:
        verts = local_pos[simplex]
        max_edge = max(np.linalg.norm(verts[i] - verts[j])
                       for i in range(3) for j in range(i+1, 3))
        if max_edge < 1.8 * nn_dist:
            faces.append(tuple(simplex))
            for i in range(3):
                for j in range(i+1, 3):
                    edges_set.add((min(simplex[i], simplex[j]), max(simplex[i], simplex[j])))

    return local_pos, list(edges_set), faces


def build_2d_dynamical_matrix(positions, edges, masses):
    """2D动力学矩阵"""
    n = len(positions)
    if n == 0:
        return np.zeros((0, 0))

    K = np.zeros((n * 2, n * 2))
    for i, j in edges:
        delta = positions[i] - positions[j]
        l = np.linalg.norm(delta)
        if l < 1e-10:
            continue
        n_vec = delta / l
        k = C_SQUARED / l**2
        for a in range(2):
            for b in range(2):
                val = k * n_vec[a] * n_vec[b]
                K[i*2+a, i*2+a] += val
                K[j*2+b, j*2+b] += val
                K[i*2+a, j*2+b] -= val
                K[j*2+b, i*2+a] -= val

    D = np.zeros_like(K)
    for a in range(n * 2):
        for b in range(n * 2):
            ia, ib = a // 2, b // 2
            if ia < len(masses) and ib < len(masses):
                mp = masses[ia] * masses[ib]
                if mp > 0:
                    D[a, b] = K[a, b] / np.sqrt(mp)
    return D


def compute_2d_gradient(positions, faces, center_idx, eps=1e-4):
    """中心原子角亏对所有原子位置的2D梯度"""
    n = len(positions)
    if n == 0 or len(faces) == 0:
        return np.zeros(n * 2)

    grad = np.zeros(n * 2)
    for i in range(n):
        for alpha in range(2):
            pos_plus = positions.copy()
            pos_minus = positions.copy()
            pos_plus[i, alpha] += eps
            pos_minus[i, alpha] -= eps

            d_plus = step_a_2d_angle_deficit(pos_plus, faces)
            d_minus = step_a_2d_angle_deficit(pos_minus, faces)

            grad[i*2+alpha] = (d_plus[center_idx] - d_minus[center_idx]) / (2 * eps)
    return grad


def cell_fg_to_tc_2d(symbol, delta_v_override=None):
    """2D投影法：从晶胞FG计算Tc"""
    crystal = get_crystal(symbol)
    if crystal is None:
        return 0.0, {'error': f'No crystal data for {symbol}'}

    mass_amu, theta_D, struct_type, lattice_params, n_nn = crystal
    results = {'symbol': symbol, 'structure': struct_type, 'theta_D': theta_D}

    # 选择投影面法向量
    normals = {
        'BCC': [1, 1, 0],      # (110)面
        'FCC': [1, 1, 1],      # (111)面
        'HCP': [0, 0, 1],      # (0001)面
        'TET': [0, 0, 1],      # (001)面
        'RHL': [0, 0, 1],      # (0001)面
    }
    normal = normals.get(struct_type, [0, 0, 1])

    # 生成3D原子位置
    all_pos_3d = generate_atom_positions(struct_type, lattice_params, n_shells=2)
    if len(all_pos_3d) == 0:
        return 0.0, {'error': 'No positions'}

    # 投影到2D
    all_pos_2d = project_to_2d(all_pos_3d, normal)

    # 去除重复点（投影后可能重叠）
    unique_pos = []
    unique_indices = []
    for i in range(len(all_pos_2d)):
        is_dup = False
        for j in unique_indices:
            if np.linalg.norm(all_pos_2d[i] - all_pos_2d[j]) < 0.01:
                is_dup = True
                break
        if not is_dup:
            unique_pos.append(all_pos_2d[i])
            unique_indices.append(i)
    all_pos_2d = np.array(unique_pos)

    # 找中心原子
    dists_origin = np.array([np.linalg.norm(all_pos_2d[i]) for i in range(len(all_pos_2d))])
    center_idx = np.argmin(dists_origin)

    # 最近邻距离
    all_dists = np.array([np.linalg.norm(all_pos_2d[i] - all_pos_2d[center_idx])
                          for i in range(len(all_pos_2d))])
    all_dists[center_idx] = np.inf
    nn_dist = np.min(all_dists)

    # 构造2D Regge剖分
    local_pos, edges, faces = construct_2d_regge(all_pos_2d, center_idx, nn_dist)
    if len(faces) == 0:
        return 0.0, {**results, 'error': 'No faces'}

    # 重新找center在local中的索引
    local_dists = np.array([np.linalg.norm(local_pos[i] - all_pos_2d[center_idx])
                            for i in range(len(local_pos))])
    local_center = np.argmin(local_dists)

    results['n_atoms'] = len(local_pos)
    results['n_faces'] = len(faces)
    results['nn_dist'] = nn_dist

    # 步骤A：2D角亏
    deficits = step_a_2d_angle_deficit(local_pos, faces)

    if delta_v_override is not None:
        delta_v = delta_v_override
    else:
        delta_v = abs(deficits[local_center])
    results['delta_v'] = delta_v
    results['beta_delta_v'] = BETA * delta_v
    results['geometric_deficit'] = abs(deficits[local_center])

    # 步骤B：2D动力学矩阵
    mass_kg = mass_amu * AMU_TO_KG
    masses = np.array([mass_kg] * len(local_pos))
    D = build_2d_dynamical_matrix(local_pos, edges, masses)

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
    grad = compute_2d_gradient(local_pos, faces, local_center)

    n = len(local_pos)
    inv_sqrt_m = np.zeros(n * 2)
    for i in range(n):
        for a in range(2):
            inv_sqrt_m[i*2+a] = 1.0 / np.sqrt(masses[i])

    l_char = nn_dist * ANGSTROM_TO_M

    delta_fluct = 0.0
    for qi in range(n_modes):
        G_q = np.dot(grad * inv_sqrt_m, e_q[:, qi])
        delta_fluct += G_q**2 / omega_q[qi]

    delta_fluct *= HBAR / (2 * l_char**2)
    results['delta_fluct'] = delta_fluct

    # 步骤F：Tc
    if 1 - BETA * delta_v < 1e-15:
        Tc, x, is_sc = 0.0, 0.0, False
    else:
        x = 3 * BETA**2 * delta_fluct / (16 * (1 - BETA * delta_v) * (GAMMA_2 - GAMMA_1))
        if x <= 1.0:
            Tc, is_sc = 0.0, False
        else:
            arccoth_x = 0.5 * np.log((x + 1) / (x - 1))
            Tc = theta_D / (2 * arccoth_x) if arccoth_x > 1e-15 else 0.0
            is_sc = True

    results['x'] = x
    results['is_superconducting'] = is_sc
    results['Tc'] = Tc

    return Tc, results


if __name__ == '__main__':
    print("=" * 70)
    print("CQM晶胞FG 2D投影法：从晶体结构到Tc")
    print("3D晶胞→2D高对称面投影→Delaunay→角亏→声子→Tc")
    print("=" * 70)

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
        dv_override = delta_v_table.get(symbol, None)
        Tc, res = cell_fg_to_tc_2d(symbol, delta_v_override=dv_override)
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
        Tc, res = cell_fg_to_tc_2d(symbol, delta_v_override=dv_override)
        if 'error' in res:
            print(f"{symbol:>4s} ERROR: {res['error']}")
            continue
        print(f"{symbol:>4s} {res['structure']:>4s} {res['n_atoms']:4d} {res['delta_v']:10.6f} {res['beta_delta_v']:8.4f} "
              f"{res['delta_fluct']:12.4e} {res['x']:10.4f} {Tc:10.4f} {'--':>10s} "
              f"{'是' if res['is_superconducting'] else '否':>4s}")

    print("\n完成。")