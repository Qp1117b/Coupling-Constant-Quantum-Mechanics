"""CQM统一Tc公式：拓扑贡献 + 多体修正

统一公式从本征值交叉严格导出：
    γ₂ - γ₁ = A₂₀·tanh(θ_D/(2Tc)) + 2·λ_ep·ln(θ_D/Tc)

其中：
    A₂₀ = 3β²·Δδ₀² / (16·(1-βδ_v))    —— 拓扑贡献（CQM纤维丛曲率涨落）
    λ_ep                                 —— 电子-声子耦合（多体自能对数修正）
    B₂ = 2                               —— Cooper对贡献

极限情况：
    弱耦合（λ_ep → 0）：退化为CQM闭式 Tc = θ_D/(2·arccoth(x)), x = A₂₀/(γ₂-γ₁)
    强耦合（A₂₀ → 0）：退化为BCS形式 Tc = θ_D·exp(-(γ₂-γ₁)/(2·λ_ep))
"""
import numpy as np
import json
import os
import sys
from scipy.optimize import brentq

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cqm_framework'))
from atom_db import atom_db
from crystal_db import get_crystal, generate_atom_positions

# CQM物理常数
BETA = 8 * np.pi + 1
C_SQUARED = 2.0 / 3.0
HBAR = 1.054571817e-34
KB = 1.380649e-23
AMU_TO_KG = 1.66054e-27
ANGSTROM_TO_M = 1e-10

GAMMA_1 = 14.134725
GAMMA_2 = 21.022040
DGAMMA = GAMMA_2 - GAMMA_1  # ≈ 6.887
B_COOPER = 2  # Cooper对贡献 B₂


# ============================================================
# 1. 拓扑贡献 A₂₀ 的计算
# ============================================================

def compute_A20(delta_v, delta_fluct):
    """计算拓扑贡献 A₂₀ = 3β²·Δδ₀² / (16·(1-βδ_v))

    输入：
    - delta_v: 物理角亏（纤维丛和乐）
    - delta_fluct: 角亏涨落 Δδ₀²（底空间曲率量子涨落）

    返回：A₂₀
    """
    denom = 1 - BETA * delta_v
    if denom < 1e-15:
        return 0.0
    return 3 * BETA**2 * delta_fluct / (16 * denom)


# ============================================================
# 2. 统一Tc方程的数值求解
# ============================================================

def unified_tc_equation(Tc, A20, lambda_ep, theta_D):
    """统一Tc方程的残差函数

    f(Tc) = A₂₀·tanh(θ_D/(2Tc)) + 2·λ_ep·ln(θ_D/Tc) - (γ₂-γ₁) = 0

    超导条件：f(Tc) = 0 有正解
    """
    if Tc <= 0 or Tc >= theta_D:
        return -DGAMMA

    tanh_term = A20 * np.tanh(theta_D / (2 * Tc))
    log_term = B_COOPER * lambda_ep * np.log(theta_D / Tc)

    return tanh_term + log_term - DGAMMA


def solve_unified_tc(A20, lambda_ep, theta_D, Tc_min=1e-6, Tc_max=None):
    """求解统一Tc方程，返回Tc

    方法：Brent求根法在[Tc_min, Tc_max]区间搜索
    """
    if Tc_max is None:
        Tc_max = theta_D * 0.999

    # 检查是否有解
    f_min = unified_tc_equation(Tc_min, A20, lambda_ep, theta_D)
    f_max = unified_tc_equation(Tc_max, A20, lambda_ep, theta_D)

    # f(Tc→0) = A₂₀·1 + 2·λ·∞ - DGAMMA → +∞（如果λ>0）
    # f(Tc→θ_D) = A₂₀·tanh(0.5) + 0 - DGAMMA
    f_at_thetaD = A20 * np.tanh(0.5) - DGAMMA

    # 如果在Tc→θ_D处f>0，说明即使Tc=θ_D也不够，无超导
    if f_at_thetaD > 0 and lambda_ep <= 0:
        return 0.0, False

    # 如果在Tc_min处f<0，说明需要更小的Tc（但物理上不合理）
    if f_min < 0:
        return 0.0, False

    # 如果f_min和f_max同号，可能无解
    if f_min * f_max > 0:
        # 检查是否在整个区间都为正（有解但超出范围）
        if f_min > 0 and f_max > 0:
            return 0.0, False
        return 0.0, False

    try:
        Tc = brentq(unified_tc_equation, Tc_min, Tc_max,
                    args=(A20, lambda_ep, theta_D),
                    xtol=1e-12, rtol=1e-12)
        return Tc, True
    except (ValueError, RuntimeError):
        return 0.0, False


# ============================================================
# 3. 从实验Tc反推 λ_ep
# ============================================================

def extract_lambda_ep(A20, Tc_exp, theta_D):
    """从实验Tc反推电子-声子耦合常数 λ_ep

    λ_ep = [(γ₂-γ₁) - A₂₀·tanh(θ_D/(2Tc))] / [2·ln(θ_D/Tc)]
    """
    if Tc_exp <= 0 or Tc_exp >= theta_D:
        return 0.0

    tanh_term = A20 * np.tanh(theta_D / (2 * Tc_exp))
    log_term = 2 * np.log(theta_D / Tc_exp)

    if abs(log_term) < 1e-15:
        return 0.0

    lambda_ep = (DGAMMA - tanh_term) / log_term
    return lambda_ep


# ============================================================
# 4. 极限情况验证
# ============================================================

def cqm_only_tc(A20, theta_D):
    """纯CQM闭式（λ_ep=0极限）

    Tc = θ_D / (2·arccoth(x)),  x = A₂₀ / (γ₂-γ₁)
    超导条件：x > 1
    """
    x = A20 / DGAMMA
    if x <= 1.0:
        return 0.0, x, False
    arccoth_x = 0.5 * np.log((x + 1) / (x - 1))
    if arccoth_x < 1e-15:
        return 0.0, x, False
    Tc = theta_D / (2 * arccoth_x)
    return Tc, x, True


def bcs_only_tc(lambda_ep, theta_D):
    """纯BCS极限（A₂₀=0极限）

    Tc = θ_D · exp(-(γ₂-γ₁) / (2·λ_ep))
    """
    if lambda_ep <= 0:
        return 0.0, False
    exponent = -DGAMMA / (B_COOPER * lambda_ep)
    if exponent < -500:
        return 0.0, False
    Tc = theta_D * np.exp(exponent)
    return Tc, True


# ============================================================
# 5. 从元素FG数据计算 A₂₀
# ============================================================

def compute_element_A20(element_fg_entry, symbol):
    """从元素FG纤维丛数据计算A₂₀

    使用混合方案：元素FG拓扑 + 晶胞FG晶格参数
    """
    crystal = get_crystal(symbol)
    if crystal is None:
        _, theta_D, _, _ = atom_db(symbol)
        l_char = 2e-10
    else:
        _, theta_D, struct_type, lattice_params, _ = crystal
        all_pos = generate_atom_positions(struct_type, lattice_params, n_shells=1)
        dists = np.array([np.linalg.norm(p) for p in all_pos])
        center = np.argmin(dists)
        all_d = np.array([np.linalg.norm(all_pos[i] - all_pos[center])
                          for i in range(len(all_pos))])
        all_d[center] = np.inf
        nn_dist = np.min(all_d)
        l_char = nn_dist * ANGSTROM_TO_M

    # 元素FG数据
    positions = np.array(element_fg_entry['positions'])
    edges = element_fg_entry['edges']
    faces = element_fg_entry['faces']
    delta_v = element_fg_entry.get('physical_delta_v', 0)

    mass_amu = element_fg_entry.get('mass', atom_db(symbol)[0])
    mass_kg = mass_amu * AMU_TO_KG

    if len(positions) == 0 or len(faces) == 0:
        return 0.0, delta_v, theta_D, l_char

    # 角亏梯度
    n = len(positions)
    n_dims = positions.shape[1]
    grad = np.zeros((n, n * n_dims))
    eps = 1e-6
    for v in range(n):
        for i in range(n):
            for alpha in range(n_dims):
                pp = positions.copy(); pm = positions.copy()
                pp[i, alpha] += eps; pm[i, alpha] -= eps
                dp = _angle_deficit(pp, faces)
                dm = _angle_deficit(pm, faces)
                grad[v, i*n_dims+alpha] = (dp[v] - dm[v]) / (2 * eps)

    # 2D动力学矩阵
    masses = np.array([mass_kg] * n)
    D = _dyn_matrix(positions, edges, masses)

    eigenvalues, eigenvectors = np.linalg.eigh(D)
    mask = eigenvalues > 1e-10
    if not np.any(mask):
        return 0.0, delta_v, theta_D, l_char

    lambda_q = eigenvalues[mask]
    e_q = eigenvectors[:, mask]
    lambda_max = np.max(lambda_q)

    omega_D = KB * theta_D / HBAR
    omega_q = omega_D * np.sqrt(lambda_q / lambda_max)

    inv_sqrt_m = np.zeros(n * n_dims)
    for i in range(n):
        for a in range(n_dims):
            inv_sqrt_m[i*n_dims+a] = 1.0 / np.sqrt(masses[i])

    delta_fluct = 0.0
    for v in range(n):
        for qi in range(len(lambda_q)):
            G_vq = np.dot(grad[v, :] * inv_sqrt_m, e_q[:, qi])
            delta_fluct += G_vq**2 / omega_q[qi]

    delta_fluct *= HBAR / (2 * l_char**2 * n)

    A20 = compute_A20(delta_v, delta_fluct)
    return A20, delta_v, theta_D, l_char


def _angle_deficit(positions, faces):
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


def _dyn_matrix(positions, edges, masses):
    n = len(positions)
    if n == 0:
        return np.zeros((0, 0))
    n_dims = positions.shape[1]
    K = np.zeros((n * n_dims, n * n_dims))
    for i, j in edges:
        delta = positions[i] - positions[j]
        l = np.linalg.norm(delta)
        if l < 1e-10:
            continue
        n_vec = delta / l
        k = C_SQUARED / l**2
        for a in range(n_dims):
            for b in range(n_dims):
                val = k * n_vec[a] * n_vec[b]
                K[i*n_dims+a, i*n_dims+a] += val
                K[j*n_dims+b, j*n_dims+b] += val
                K[i*n_dims+a, j*n_dims+b] -= val
                K[j*n_dims+b, i*n_dims+a] -= val
    D = np.zeros_like(K)
    for a in range(n * n_dims):
        for b in range(n * n_dims):
            ia, ib = a // n_dims, b // n_dims
            if ia < len(masses) and ib < len(masses):
                mp = masses[ia] * masses[ib]
                if mp > 0:
                    D[a, b] = K[a, b] / np.sqrt(mp)
    return D


# ============================================================
# 6. 主程序：验证统一公式
# ============================================================

KNOWN_SC = {
    'Nb': 9.25, 'Pb': 7.2, 'V': 5.4, 'Ta': 4.48, 'Hg': 4.15,
    'Sn': 3.72, 'In': 3.41, 'Tl': 2.39, 'Re': 1.7, 'Al': 1.19,
    'Mo': 0.92, 'Zn': 0.85, 'Os': 0.66, 'Zr': 0.61, 'Cd': 0.52,
    'Ru': 0.49, 'Ti': 0.4, 'Hf': 0.13, 'Ir': 0.11, 'Be': 0.026,
    'W': 0.015, 'La': 6.0, 'Lu': 0.1, 'Th': 1.37,
}

NON_SC = ['Cu', 'Ag', 'Au', 'Ni', 'Cr', 'Fe', 'Mg', 'Rh', 'Pd', 'Pt',
          'Na', 'K', 'Rb', 'Cs', 'Ca', 'Sr', 'Ba', 'Li', 'Sc', 'Y',
          'Mn', 'Co', 'Ga', 'Ge', 'Si', 'C', 'B']


def main():
    print("=" * 80)
    print("CQM统一Tc公式：拓扑贡献 + 多体修正")
    print("γ₂-γ₁ = A₂₀·tanh(θ_D/(2Tc)) + 2·λ_ep·ln(θ_D/Tc)")
    print("=" * 80)
    print(f"\nβ = {BETA:.4f}, γ₂-γ₁ = {DGAMMA:.4f}, B₂ = {B_COOPER}\n")

    # 加载元素FG表
    table_path = os.path.join(os.path.dirname(__file__), 'element_fg_table.json')
    with open(table_path, 'r', encoding='utf-8') as f:
        element_table = json.load(f)
    elem_dict = {e['symbol']: e for e in element_table}

    # === 第一步：计算A₂₀，从实验Tc反推λ_ep ===
    print("-" * 80)
    print("第一步：计算A₂₀，从实验Tc反推λ_ep")
    print("-" * 80)
    print(f"{'元素':>4s} {'θ_D':>6s} {'δ_v':>10s} {'A₂₀':>10s} {'x_cqm':>8s} "
          f"{'Tc_exp':>8s} {'λ_ep':>8s} {'Tc_cqm':>10s} {'Tc_bcs':>10s} {'Tc_uni':>10s}")
    print("-" * 95)

    results = []
    for symbol in sorted(KNOWN_SC.keys()):
        if symbol not in elem_dict:
            continue
        A20, delta_v, theta_D, l_char = compute_element_A20(elem_dict[symbol], symbol)
        Tc_exp = KNOWN_SC[symbol]
        lambda_ep = extract_lambda_ep(A20, Tc_exp, theta_D)

        # 纯CQM和纯BCS极限
        Tc_cqm, x_cqm, _ = cqm_only_tc(A20, theta_D)
        Tc_bcs, _ = bcs_only_tc(lambda_ep, theta_D)

        # 统一公式验证（应该重现实验Tc）
        Tc_uni, _ = solve_unified_tc(A20, lambda_ep, theta_D)

        results.append({
            'symbol': symbol, 'A20': A20, 'delta_v': delta_v,
            'theta_D': theta_D, 'Tc_exp': Tc_exp, 'lambda_ep': lambda_ep,
            'x_cqm': x_cqm, 'Tc_cqm': Tc_cqm, 'Tc_bcs': Tc_bcs, 'Tc_uni': Tc_uni,
        })

        print(f"{symbol:>4s} {theta_D:6.1f} {delta_v:10.6f} {A20:10.4f} {x_cqm:8.4f} "
              f"{Tc_exp:8.3f} {lambda_ep:8.4f} {Tc_cqm:10.4f} {Tc_bcs:10.4f} {Tc_uni:10.4f}")

    # === 第二步：分析λ_ep的规律 ===
    print("\n" + "-" * 80)
    print("第二步：分析λ_ep与纤维丛结构的关系")
    print("-" * 80)

    print(f"\n{'元素':>4s} {'λ_ep':>8s} {'A₂₀':>10s} {'A₂₀/(γ₂-γ₁)':>12s} {'ln(θ_D/Tc)':>12s} "
          f"{'耦合区':>8s}")
    print("-" * 60)

    for r in results:
        ratio = r['A20'] / DGAMMA
        log_term = np.log(r['theta_D'] / r['Tc_exp']) if r['Tc_exp'] > 0 else 0
        if r['lambda_ep'] < 0.1:
            regime = '弱耦合'
        elif r['lambda_ep'] < 0.5:
            regime = '中耦合'
        else:
            regime = '强耦合'
        print(f"{r['symbol']:>4s} {r['lambda_ep']:8.4f} {r['A20']:10.4f} {ratio:12.4f} "
              f"{log_term:12.4f} {regime:>8s}")

    # === 第三步：非超导元素检查 ===
    print("\n" + "-" * 80)
    print("第三步：非超导元素检查（A₂₀和λ_ep都应该不够大）")
    print("-" * 80)
    print(f"{'元素':>4s} {'θ_D':>6s} {'δ_v':>10s} {'A₂₀':>10s} {'x_cqm':>8s} {'超导?(CQM)':>10s}")
    print("-" * 55)

    for symbol in NON_SC:
        if symbol not in elem_dict:
            continue
        A20, delta_v, theta_D, _ = compute_element_A20(elem_dict[symbol], symbol)
        _, x_cqm, is_sc = cqm_only_tc(A20, theta_D)
        print(f"{symbol:>4s} {theta_D:6.1f} {delta_v:10.6f} {A20:10.4f} {x_cqm:8.4f} "
              f"{'是' if is_sc else '否':>10s}")

    # === 第四步：关键发现总结 ===
    print("\n" + "=" * 80)
    print("关键发现")
    print("=" * 80)

    weak = [r for r in results if r['lambda_ep'] < 0.1]
    strong = [r for r in results if r['lambda_ep'] >= 0.5]

    print(f"\n弱耦合元素（λ_ep < 0.1）：{len(weak)}个")
    for r in weak:
        print(f"  {r['symbol']}: λ_ep={r['lambda_ep']:.4f}, A₂₀/(γ₂-γ₁)={r['A20']/DGAMMA:.4f}, "
              f"Tc={r['Tc_exp']:.3f}K")

    print(f"\n强耦合元素（λ_ep ≥ 0.5）：{len(strong)}个")
    for r in strong:
        print(f"  {r['symbol']}: λ_ep={r['lambda_ep']:.4f}, A₂₀/(γ₂-γ₁)={r['A20']/DGAMMA:.4f}, "
              f"Tc={r['Tc_exp']:.3f}K")

    # 保存结果
    output_path = os.path.join(os.path.dirname(__file__), 'unified_tc_results.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存：{output_path}")


if __name__ == '__main__':
    main()