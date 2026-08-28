"""CQM统一从纤维丛到Tc的计算链

给定任意层FG的纤维丛 (M_ℓ, P_ℓ, π_ℓ, G_ℓ) 的Regge剖分，
执行统一步骤A-F计算Tc：

A: Regge剖分 → 逐顶点角亏 δ_v（底空间曲率集中，Gauss-Bonnet）
B: 联络 A_ℓ 离散化 → 动力学矩阵 D_ij（Regge作用量变分）
C: 纤维上量子谐振子 → 声子频率 ω_q（本征值对角化）
D: 底空间曲率量子涨落 → 角亏涨落 Δδ₀²
E: 主丛谱算符 → 同步算符本征值 λ_n(T)
F: 本征值交叉 λ₂(Tc)=λ₁(Tc) → Tc闭式
"""
import numpy as np
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cqm_framework'))
from atom_db import atom_db

# CQM物理常数
BETA = 8 * np.pi + 1          # Klein四元群和乐 ≈ 26.13
C_SQUARED = 2.0 / 3.0         # 几何因子4/3 × 边共享因子1/2
HBAR = 1.054571817e-34        # 约化普朗克常数 (J·s)
KB = 1.380649e-23             # 玻尔兹曼常数 (J/K)
AMU_TO_KG = 1.66054e-27       # 原子质量单位 → kg

# 黎曼零点（前几个虚部）
GAMMA = [14.134725, 21.022040, 25.010857, 30.424876, 32.935061]
GAMMA_1 = GAMMA[0]  # γ₁ ≈ 14.1347
GAMMA_2 = GAMMA[1]  # γ₂ ≈ 21.0220


# ============================================================
# 步骤A：逐顶点角亏（底空间曲率集中，Gauss-Bonnet）
# ============================================================

def step_a_angle_deficit(positions, faces):
    """步骤A：逐顶点计算角亏 δ_v = 2π - Σθ_i

    角亏是底空间曲率在顶点处的集中，
    等价于和乐 W_v = exp(i*δ_v*T) ∈ G_ℓ
    """
    n_vertices = len(positions)
    if n_vertices == 0 or len(faces) == 0:
        return np.zeros(n_vertices)

    angle_sums = np.zeros(n_vertices)

    for face in faces:
        i, j, k = face
        vi, vj, vk = positions[i], positions[j], positions[k]

        for v_idx, (a, b, c) in [(i, (vj, vi, vk)), (j, (vi, vj, vk)), (k, (vi, vk, vj))]:
            va = a - b
            vb = c - b
            cos_angle = np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb) + 1e-15)
            cos_angle = np.clip(cos_angle, -1.0, 1.0)
            angle_sums[v_idx] += np.arccos(cos_angle)

    deficits = 2 * np.pi - angle_sums
    return deficits


# ============================================================
# 步骤B：动力学矩阵（联络 A_ℓ 离散化）
# ============================================================

def step_b_dynamical_matrix(positions, edges, masses):
    """步骤B：从Regge几何构造2D动力学矩阵

    联络 A_ℓ 离散化为力常数矩阵 K_ij = ∂²V_Regge/∂u_i∂u_j
    动力学矩阵 D_ij = K_ij / √(m_i·m_j)

    2D中心力弹簧模型：每条边沿边方向有弹簧常数 k = C²/l²
    """
    n = len(positions)
    n_dims = positions.shape[1] if positions.ndim > 1 else 1
    if n == 0:
        return np.zeros((0, 0))

    # 2D力常数矩阵（每个顶点n_dims个自由度）
    K = np.zeros((n * n_dims, n * n_dims))

    for i, j in edges:
        delta = positions[i] - positions[j]
        l = np.linalg.norm(delta)
        if l < 1e-10:
            continue
        # 单位向量沿边方向
        n_vec = delta / l
        # 弹簧常数
        k_spring = C_SQUARED / l**2
        # 2D力常数矩阵
        for alpha in range(n_dims):
            for beta in range(n_dims):
                val = k_spring * n_vec[alpha] * n_vec[beta]
                K[i*n_dims+alpha, i*n_dims+alpha] += val
                K[j*n_dims+beta, j*n_dims+beta] += val
                K[i*n_dims+alpha, j*n_dims+beta] -= val
                K[j*n_dims+beta, i*n_dims+alpha] -= val

    # 动力学矩阵 D = K / √(m_i·m_j)
    D = np.zeros_like(K)
    for a in range(n * n_dims):
        for b in range(n * n_dims):
            i_a, alpha_a = a // n_dims, a % n_dims
            i_b, alpha_b = b // n_dims, b % n_dims
            if i_a < len(masses) and i_b < len(masses):
                m_prod = masses[i_a] * masses[i_b]
                if m_prod > 0:
                    D[a, b] = K[a, b] / np.sqrt(m_prod)

    return D


# ============================================================
# 步骤C：声子频率（纤维上量子谐振子本征值）
# ============================================================

def step_c_phonon_frequencies(D):
    """步骤C：从动力学矩阵本征值计算声子频率和本征矢

    ω_q² = eig(D)
    ω_q = √(eig(D))
    Debye频率 ω_D = max(ω_q)
    """
    if D.shape[0] == 0:
        return np.array([]), 0.0, np.zeros((0, 0))

    eigenvalues, eigenvectors = np.linalg.eigh(D)
    # 只取正本征值（物理频率）
    eigenvalues = np.maximum(eigenvalues, 0)
    frequencies = np.sqrt(eigenvalues)

    debye_freq = np.max(frequencies) if len(frequencies) > 0 else 0.0

    return frequencies, debye_freq, eigenvectors


# ============================================================
# 步骤D：角亏涨落（底空间曲率零温量子涨落）
# ============================================================

def compute_delta_gradient_full(positions, faces, eps=1e-6):
    """数值计算各顶点角亏对原子位置的梯度

    返回 grad_delta[v, i*n_dims+alpha] = ∂δ_v/∂p_{i,alpha}
    形状：(n_vertices, n_vertices * n_dims)
    """
    positions = np.array(positions, dtype=float)
    n_vertices = len(positions)
    if n_vertices == 0 or len(faces) == 0:
        return np.zeros((0, 0))

    n_dims = positions.shape[1] if positions.ndim > 1 else 1
    grad = np.zeros((n_vertices, n_vertices * n_dims))

    for v in range(n_vertices):
        for i in range(n_vertices):
            for alpha in range(n_dims):
                pos_plus = positions.copy()
                pos_minus = positions.copy()
                pos_plus[i, alpha] += eps
                pos_minus[i, alpha] -= eps

                deficits_plus = step_a_angle_deficit(pos_plus, faces)
                deficits_minus = step_a_angle_deficit(pos_minus, faces)

                grad[v, i * n_dims + alpha] = (deficits_plus[v] - deficits_minus[v]) / (2 * eps)

    return grad


def step_d_angle_fluctuation(positions, faces, edges, masses_kg, D, l_char, theta_D):
    """步骤D：用完整声子谱计算角亏涨落 Δδ₀²

    Δδ₀² = (1/N) Σ_v Σ_{q: ω_q>0} |∂δ_v/∂a_q|² × ℏ/(2·ω_q)

    其中：
    - ∂δ_v/∂a_q = (1/l_char) × Σ_{a} (∂δ_v/∂p_a) × e_q[a] / √m_a
    - ω_q = ω_D × √(λ_q/λ_max)  （Debye频率标定的物理频率）
    - e_q是D的本征矢，m_a是坐标a对应的原子质量(kg)

    量纲：[1/(m·√kg)]² × [J·s/(1/s)] = [1/(m²·kg)] × [kg·m²] = 无量纲 ✓
    """
    positions = np.array(positions, dtype=float)
    n_vertices = len(positions)
    n_dims = positions.shape[1] if positions.ndim > 1 else 1
    if n_vertices == 0 or D.shape[0] == 0:
        return 0.0

    # 1. 动力学矩阵本征值和本征矢
    eigenvalues, eigenvectors = np.linalg.eigh(D)
    mask = eigenvalues > 1e-10
    if not np.any(mask):
        return 0.0

    lambda_q = eigenvalues[mask]
    e_q = eigenvectors[:, mask]
    lambda_max = np.max(lambda_q)

    # 2. Debye频率标定
    omega_D = KB * theta_D / HBAR
    omega_q = omega_D * np.sqrt(lambda_q / lambda_max)

    # 3. 角亏梯度
    grad = compute_delta_gradient_full(positions, faces)

    # 4. 质量加权因子 1/√m_a
    inv_sqrt_m = np.zeros(n_vertices * n_dims)
    for i in range(n_vertices):
        for alpha in range(n_dims):
            a = i * n_dims + alpha
            if i < len(masses_kg) and masses_kg[i] > 0:
                inv_sqrt_m[a] = 1.0 / np.sqrt(masses_kg[i])

    # 5. 投影到本征矢并求和
    # G_v,q = Σ_a grad[v,a] × e_q[a] / √m_a
    delta_fluct = 0.0
    for v in range(n_vertices):
        for qi in range(len(lambda_q)):
            G_vq = np.dot(grad[v, :] * inv_sqrt_m, e_q[:, qi])
            delta_fluct += G_vq**2 / omega_q[qi]

    # 6. 物理常数因子
    delta_fluct *= HBAR / (2 * l_char**2 * n_vertices)

    return delta_fluct


# ============================================================
# 步骤E：同步算符本征值（主丛谱算符）
# ============================================================

def step_e_sync_eigenvalues(delta_v, delta_fluct, T, theta_D):
    """步骤E：计算同步算符本征值 λ_n(T)

    λ_n(T) = γ_n - β²·Δδ_v(T)²·(n²-1) / (4n²·(1-βδ_v))

    其中 Δδ_v(T) = Δδ₀·√(tanh(ℏΩ₀/(2k_BT)))
    """
    if 1 - BETA * delta_v < 1e-15:
        return None

    # 温度依赖的角亏涨落
    if T > 0:
        tanh_arg = HBAR * theta_D / (2 * KB * T)
        if tanh_arg > 500:
            temp_factor = 1.0
        else:
            temp_factor = np.sqrt(np.tanh(tanh_arg))
    else:
        temp_factor = 1.0

    delta_v_T = np.sqrt(delta_fluct) * temp_factor

    # 本征值
    eigenvalues = []
    for n in range(1, len(GAMMA) + 1):
        gamma_n = GAMMA[n-1]
        lambda_n = gamma_n - BETA**2 * delta_v_T**2 * (n**2 - 1) / (4 * n**2 * (1 - BETA * delta_v))
        eigenvalues.append(lambda_n)

    return eigenvalues


# ============================================================
# 步骤F：Tc闭式（本征值交叉 λ₂(Tc)=λ₁(Tc)）
# ============================================================

def step_f_tc_formula(delta_v, delta_fluct, theta_D):
    """步骤F：从本征值交叉计算Tc闭式

    Tc = θ_D / (2·arccoth(x))
    x = 3β²·Δδ₀² / (16·(1-βδ_v)·(γ₂-γ₁))

    超导条件：x > 1
    """
    if 1 - BETA * delta_v < 1e-15:
        return 0.0, 0.0, False

    x = 3 * BETA**2 * delta_fluct / (16 * (1 - BETA * delta_v) * (GAMMA_2 - GAMMA_1))

    if x <= 1.0:
        return 0.0, x, False  # 不超导

    # arccoth(x) = 0.5·ln((x+1)/(x-1))
    arccoth_x = 0.5 * np.log((x + 1) / (x - 1))

    if arccoth_x < 1e-15:
        return 0.0, x, False

    Tc = theta_D / (2 * arccoth_x)

    return Tc, x, True


# ============================================================
# 统一计算链：从Regge剖分到Tc
# ============================================================

def regge_to_tc(positions, edges, faces, masses, theta_D, l_char, delta_v_override=None):
    """统一计算链：从Regge剖分到Tc

    输入：
    - positions: 顶点位置数组
    - edges: 边列表
    - faces: 面列表
    - masses: 顶点质量数组
    - theta_D: Debye温度（K）
    - l_char: 特征长度（最近邻距离，m）
    - delta_v_override: 可选的物理角亏（从核子分布计算）

    输出：
    - Tc: 临界温度（K）
    - 详细结果字典
    """
    results = {}

    # 步骤A：角亏
    deficits = step_a_angle_deficit(positions, faces)
    if delta_v_override is not None:
        delta_v = delta_v_override
    else:
        delta_v = np.mean(np.abs(deficits)) if len(deficits) > 0 else 0.0
    results['delta_v'] = delta_v
    results['beta_delta_v'] = BETA * delta_v

    # 步骤B：动力学矩阵（2D）
    D = step_b_dynamical_matrix(positions, edges, masses)
    results['dynamical_matrix_shape'] = D.shape

    # 步骤C：声子频率和本征矢
    frequencies, debye_freq, eigenvectors = step_c_phonon_frequencies(D)
    results['n_phonon_modes'] = len(frequencies)
    results['debye_freq'] = debye_freq

    # 步骤D：角亏涨落（完整声子谱，投影到本征矢）
    delta_fluct = step_d_angle_fluctuation(positions, faces, edges, masses, D, l_char, theta_D)
    results['delta_fluct'] = delta_fluct

    # 步骤F：Tc闭式
    Tc, x, is_superconducting = step_f_tc_formula(delta_v, delta_fluct, theta_D)
    results['x'] = x
    results['is_superconducting'] = is_superconducting
    results['Tc'] = Tc

    return Tc, results


# ============================================================
# 从元素FG表计算单元素Tc
# ============================================================

def element_tc(element_fg, theta_D=None, l_char=None):
    """从元素FG纤维丛数据计算Tc

    输入：元素FG表中的条目
    输出：Tc和详细结果
    """
    positions = np.array(element_fg['positions'])
    edges = element_fg['edges']
    faces = element_fg['faces']
    mass = element_fg['mass'] * 1.66054e-27  # amu → kg
    masses = np.array([mass] * len(positions))

    # Debye温度
    if theta_D is None:
        _, debye_T, _, _ = atom_db(element_fg['symbol'])
        theta_D = debye_T if debye_T > 0 else 300

    if l_char is None:
        _, _, cov_r, _ = atom_db(element_fg['symbol'])
        l_char = cov_r * 1e-10 if cov_r > 0 else 2e-10

    # 物理角亏
    delta_v_override = element_fg.get('physical_delta_v', None)

    return regge_to_tc(positions, edges, faces, masses, theta_D, l_char, delta_v_override)


# ============================================================
# 主程序：验证
# ============================================================

if __name__ == '__main__':
    print("=" * 60)
    print("CQM统一从纤维丛到Tc的计算链")
    print("剖分→角亏→动力学矩阵→声子→涨落→Tc闭式")
    print("=" * 60)

    # 加载元素FG表
    table_path = os.path.join(os.path.dirname(__file__), 'element_fg_table.json')
    with open(table_path, 'r', encoding='utf-8') as f:
        element_table = json.load(f)

    print(f"加载元素FG表：{len(element_table)}个元素\n")

    # 已知超导元素及其Tc
    known_superconductors = {
        'Al': 1.2, 'Pb': 7.2, 'Hg': 4.15, 'Nb': 9.2, 'V': 5.4,
        'Sn': 3.72, 'Zn': 0.85, 'La': 6.0, 'Zr': 0.55, 'Cd': 0.56,
        'In': 3.4, 'Tl': 2.4, 'Re': 1.7, 'W': 0.01, 'Be': 0.026,
        'Mo': 0.92, 'Ru': 0.49, 'Os': 0.66, 'Ir': 0.14, 'Ti': 0.39,
        'Ta': 4.48, 'Pa': 1.4, 'Th': 1.37, 'Lu': 0.1, 'Hf': 0.13,
    }

    print(f"{'元素':>4s} {'δ_v':>10s} {'βδ_v':>8s} {'Δδ₀²':>12s} {'x':>10s} {'Tc预测':>10s} {'Tc实验':>10s} {'超导?':>6s}")
    print("-" * 80)

    for elem in element_table:
        symbol = elem['symbol']
        if symbol not in known_superconductors:
            continue

        Tc, results = element_tc(elem)
        Tc_exp = known_superconductors[symbol]

        print(f"{symbol:>4s} {results['delta_v']:10.6f} {results['beta_delta_v']:8.4f} "
              f"{results['delta_fluct']:12.4e} "
              f"{results['x']:10.4f} {Tc:10.4f} {Tc_exp:10.4f} "
              f"{'是' if results['is_superconducting'] else '否':>6s}")

    print("\n完成。")