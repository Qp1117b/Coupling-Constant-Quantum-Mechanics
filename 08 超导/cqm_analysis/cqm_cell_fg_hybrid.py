"""CQM晶胞FG：元素FG拓扑 + 晶胞FG晶格参数修正

关键认识：
- δ_v是纤维丛和乐（拓扑量），从元素FG核壳层结构给出
- Δδ₀²从元素FG抽象Regge多面体梯度给出
- 晶胞FG提供晶格常数(a,c)和配位数z，修正声子谱标度

修正方案：
- l_char用晶胞最近邻距离（不是共价半径）
- Debye频率用晶胞Debye温度
- 配位数z修正梯度（z越大，角亏对位移越敏感）
"""
import numpy as np
import os
import sys
import json

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


def step_a_angle_deficit(positions, faces):
    """2D逐顶点角亏"""
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


def compute_gradient_per_vertex(positions, faces, eps=1e-6):
    """各顶点角亏梯度平方的平均 (1/N)Σ_v |∇δ_v|²"""
    n = len(positions)
    if n == 0 or len(faces) == 0:
        return 0.0
    n_dims = positions.shape[1]
    total = 0.0
    for v in range(n):
        for i in range(n):
            for alpha in range(n_dims):
                pp = positions.copy(); pm = positions.copy()
                pp[i, alpha] += eps; pm[i, alpha] -= eps
                dp = step_a_angle_deficit(pp, faces)
                dm = step_a_angle_deficit(pm, faces)
                deriv = (dp[v] - dm[v]) / (2 * eps)
                total += deriv ** 2
    return total / n


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


def cell_fg_tc(symbol, element_fg_entry):
    """晶胞FG计算Tc：元素FG拓扑 + 晶胞FG晶格参数"""
    crystal = get_crystal(symbol)
    if crystal is None:
        return 0.0, {'error': f'No crystal data for {symbol}'}

    mass_amu, theta_D, struct_type, lattice_params, z_coord = crystal
    results = {'symbol': symbol, 'structure': struct_type, 'theta_D': theta_D, 'z': z_coord}

    # === 元素FG部分：拓扑参数 ===
    positions = np.array(element_fg_entry['positions'])
    edges = element_fg_entry['edges']
    faces = element_fg_entry['faces']
    delta_v = element_fg_entry.get('physical_delta_v', 0)

    results['delta_v'] = delta_v
    results['beta_delta_v'] = BETA * delta_v

    # 角亏梯度（从元素FG抽象Regge多面体）
    grad_sq = compute_gradient_per_vertex(positions, faces)
    results['grad_sq'] = grad_sq

    # === 晶胞FG部分：晶格参数 ===
    # 计算晶胞最近邻距离
    all_pos = generate_atom_positions(struct_type, lattice_params, n_shells=1)
    dists_origin = np.array([np.linalg.norm(p) for p in all_pos])
    center = np.argmin(dists_origin)
    all_d = np.array([np.linalg.norm(all_pos[i] - all_pos[center])
                      for i in range(len(all_pos))])
    all_d[center] = np.inf
    nn_dist = np.min(all_d)  # 最近邻距离 (Å)

    # 用晶胞最近邻距离作为特征长度（不是共价半径）
    l_char = nn_dist * ANGSTROM_TO_M
    results['l_char'] = l_char
    results['nn_dist_A'] = nn_dist

    # === 混合计算：元素FG梯度 + 晶胞FG声子谱 ===
    mass_kg = mass_amu * AMU_TO_KG

    # 元素FG动力学矩阵
    masses = np.array([mass_kg] * len(positions))
    D = build_2d_dynamical_matrix(positions, edges, masses)

    eigenvalues, eigenvectors = np.linalg.eigh(D)
    mask = eigenvalues > 1e-10
    n_modes = np.sum(mask)
    results['n_modes'] = n_modes

    if n_modes == 0:
        return 0.0, {**results, 'error': 'No modes'}

    lambda_q = eigenvalues[mask]
    e_q = eigenvectors[:, mask]
    lambda_max = np.max(lambda_q)

    # Debye频率标定（用晶胞FG的Debye温度）
    omega_D = KB * theta_D / HBAR
    omega_q = omega_D * np.sqrt(lambda_q / lambda_max)

    # 角亏梯度（每个顶点的梯度向量）
    n = len(positions)
    n_dims = positions.shape[1]
    grad = np.zeros((n, n * n_dims))
    eps = 1e-6
    for v in range(n):
        for i in range(n):
            for alpha in range(n_dims):
                pp = positions.copy(); pm = positions.copy()
                pp[i, alpha] += eps; pm[i, alpha] -= eps
                dp = step_a_angle_deficit(pp, faces)
                dm = step_a_angle_deficit(pm, faces)
                grad[v, i*n_dims+alpha] = (dp[v] - dm[v]) / (2 * eps)

    # 质量加权
    inv_sqrt_m = np.zeros(n * n_dims)
    for i in range(n):
        for a in range(n_dims):
            inv_sqrt_m[i*n_dims+a] = 1.0 / np.sqrt(masses[i])

    # 投影到声子本征矢
    delta_fluct = 0.0
    for v in range(n):
        for qi in range(n_modes):
            G_vq = np.dot(grad[v, :] * inv_sqrt_m, e_q[:, qi])
            delta_fluct += G_vq**2 / omega_q[qi]

    delta_fluct *= HBAR / (2 * l_char**2 * n)
    results['delta_fluct'] = delta_fluct

    # Tc闭式
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
    print("CQM晶胞FG：元素FG拓扑 + 晶胞FG晶格参数")
    print("=" * 70)

    table_path = os.path.join(os.path.dirname(__file__), 'element_fg_table.json')
    with open(table_path, 'r', encoding='utf-8') as f:
        element_table = json.load(f)
    elem_dict = {e['symbol']: e for e in element_table}

    known_sc = {
        'Nb': 9.25, 'Pb': 7.2, 'V': 5.4, 'Ta': 4.48, 'Hg': 4.15,
        'Sn': 3.72, 'In': 3.41, 'Tl': 2.39, 'Re': 1.7, 'Al': 1.19,
        'Mo': 0.92, 'Zn': 0.85, 'Os': 0.66, 'Zr': 0.61, 'Cd': 0.52,
        'Ru': 0.49, 'Ti': 0.4, 'Hf': 0.13, 'Ir': 0.11, 'Be': 0.026,
        'W': 0.015,
    }
    non_sc = ['Cu', 'Ag', 'Au', 'Ni', 'Cr', 'Fe', 'Mg', 'Rh', 'Pd', 'Pt', 'Th']

    print(f"\n{'元素':>4s} {'结构':>4s} {'z':>3s} {'δ_v':>10s} {'βδ_v':>8s} {'l_char(Å)':>10s} {'Δδ₀²':>12s} {'x':>10s} {'Tc预测':>10s} {'Tc实验':>10s} {'超导?':>4s}")
    print("-" * 100)

    for symbol in sorted(known_sc.keys()):
        if symbol not in elem_dict:
            continue
        Tc, res = cell_fg_tc(symbol, elem_dict[symbol])
        if 'error' in res:
            print(f"{symbol:>4s} ERROR: {res['error']}")
            continue
        Tc_exp = known_sc[symbol]
        print(f"{symbol:>4s} {res['structure']:>4s} {res['z']:3d} {res['delta_v']:10.6f} {res['beta_delta_v']:8.4f} "
              f"{res['nn_dist_A']:10.4f} {res['delta_fluct']:12.4e} {res['x']:10.4f} {Tc:10.4f} {Tc_exp:10.4f} "
              f"{'是' if res['is_superconducting'] else '否':>4s}")

    print(f"\n--- 非超导元素（对照）---")
    for symbol in non_sc:
        if symbol not in elem_dict:
            continue
        Tc, res = cell_fg_tc(symbol, elem_dict[symbol])
        if 'error' in res:
            print(f"{symbol:>4s} ERROR: {res['error']}")
            continue
        print(f"{symbol:>4s} {res['structure']:>4s} {res['z']:3d} {res['delta_v']:10.6f} {res['beta_delta_v']:8.4f} "
              f"{res['nn_dist_A']:10.4f} {res['delta_fluct']:12.4e} {res['x']:10.4f} {Tc:10.4f} {'--':>10s} "
              f"{'是' if res['is_superconducting'] else '否':>4s}")

    print("\n完成。")