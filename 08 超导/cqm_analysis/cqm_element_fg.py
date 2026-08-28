"""CQM元素FG穷尽列举：118元素→纤维丛→嘉当矩阵→Regge剖分→预计算表

每层FG是一个主丛 (M_ℓ, P_ℓ, π_ℓ, G_ℓ)。
元素FG的底空间 M_el = Z个质子和N个中子的空间分布。
从Z第一性构造纤维丛：Z→核子数→核壳层→嘉当矩阵→Dynkin图→Regge剖分→角亏δ_v。
电子轨道是元素FG的谱体现（U(1)耦合常数涨落+SO(2)/SU(2)影响+同位素影响）。
"""
import numpy as np
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cqm_framework'))
from atom_db import atom_db

# ============================================================
# 1. 从Z到核子分布
# ============================================================

# 稳定同位素的中子数N（选择最丰富或最稳定的同位素）
STABLE_N = {
    1:0, 2:2, 3:4, 4:5, 5:6, 6:6, 7:7, 8:8, 9:10, 10:10,
    11:12, 12:12, 13:14, 14:14, 15:16, 16:16, 17:18, 18:22, 19:20, 20:20,
    21:24, 22:26, 23:28, 24:28, 25:30, 26:30, 27:32, 28:30, 29:34, 30:34,
    31:40, 32:40, 33:42, 34:44, 35:45, 36:48, 37:48, 38:46, 39:50, 40:50,
    41:52, 42:54, 43:55, 44:58, 45:58, 46:60, 47:62, 48:64, 49:66, 50:68,
    51:70, 52:70, 53:74, 54:77, 55:78, 56:81, 57:82, 58:82, 59:82, 60:82,
    61:82, 62:88, 63:89, 64:90, 65:94, 66:97, 67:98, 68:99, 69:100, 70:103,
    71:104, 72:106, 73:108, 74:110, 75:112, 76:114, 77:116, 78:117, 79:118, 80:120,
    81:124, 82:125, 83:128, 84:125, 85:136, 86:136, 87:136, 88:138, 89:138, 90:142,
    91:140, 92:146, 93:144, 94:150, 95:150, 96:150, 97:154, 98:152, 99:157, 100:157,
    101:157, 102:157, 103:159, 104:157, 105:157, 106:160, 107:1609, 108:161, 109:170, 110:171,
    111:173, 112:173, 113:173, 114:173, 115:173, 116:173, 117:173, 118:173,
}

# 元素符号
ELEMENT_SYMBOLS = [
    'H','He','Li','Be','B','C','N','O','F','Ne',
    'Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca',
    'Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn',
    'Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr',
    'Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn',
    'Sb','Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd',
    'Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb',
    'Lu','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg',
    'Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac','Th',
    'Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm',
    'Md','No','Lr','Rf','Db','Sg','Bh','Hs','Mt','Ds',
    'Rg','Cn','Nh','Fl','Mc','Lv','Ts','Og',
]

def get_nucleons(Z):
    """从原子序数Z获取质子数和中子数"""
    protons = Z
    neutrons = STABLE_N.get(Z, round(Z * 1.2))
    return protons, neutrons


# ============================================================
# 2. 核壳层结构→嘉当矩阵
# ============================================================

# 核壳层（从SU(5)破缺→A4嘉当矩阵→壳层{2,6,10,14}）
NUCLEAR_SHELLS = [2, 6, 10, 14, 18, 22, 26, 32]

def get_shell_occupation(Z_or_N):
    """获取核子在各壳层的占据数"""
    remaining = Z_or_N
    occupations = []
    for capacity in NUCLEAR_SHELLS:
        if remaining <= 0:
            occupations.append(0)
        elif remaining >= capacity:
            occupations.append(capacity)
            remaining -= capacity
        else:
            occupations.append(remaining)
            remaining = 0
    return occupations

def get_valence_shell_occupation(Z_or_N):
    """获取最外层未满壳层的占据数和容量

    满壳层→无角亏（球形对称）
    未满壳层→有角亏（形变）
    """
    remaining = Z_or_N
    for i, capacity in enumerate(NUCLEAR_SHELLS):
        if remaining <= 0:
            return 0, 0, i  # 空壳层
        if remaining >= capacity:
            remaining -= capacity
        else:
            return remaining, capacity, i  # 未满壳层
    return remaining, NUCLEAR_SHELLS[-1], len(NUCLEAR_SHELLS)  # 超出已知壳层

def get_cartan_type(occupation, capacity):
    """从最外层未满壳层确定嘉当矩阵类型

    满壳层(occupation=capacity)→A1（对称，无角亏）
    部分占据→A3或A4（破缺，有角亏）
    """
    if occupation == 0 or occupation == capacity:
        return 'A1'  # 满壳层或空壳层→对称
    # 未满壳层→根据占据比例确定嘉当矩阵
    fill_ratio = occupation / capacity
    if fill_ratio <= 0.25 or fill_ratio >= 0.75:
        return 'A3'  # 轻度或重度占据→p壳层对称性
    else:
        return 'A4'  # 中度占据→d壳层对称性

def cartan_matrix(cartan_type):
    """构造嘉当矩阵"""
    if cartan_type is None or cartan_type == 'A1':
        return np.array([[2]], dtype=float)
    elif cartan_type == 'A3':
        return np.array([
            [2, -1, 0],
            [-1, 2, -1],
            [0, -1, 2],
        ], dtype=float)
    elif cartan_type == 'A4':
        return np.array([
            [2, -1, 0, 0],
            [-1, 2, -1, 0],
            [0, -1, 2, -1],
            [0, 0, -1, 2],
        ], dtype=float)
    else:
        return np.array([[2]], dtype=float)

def dynkin_graph(cartan_type):
    """从嘉当矩阵类型获取Dynkin图（顶点+边）"""
    if cartan_type is None or cartan_type == 'A1':
        return [0], []
    elif cartan_type == 'A3':
        return [0, 1, 2], [(0, 1), (1, 2)]
    elif cartan_type == 'A4':
        return [0, 1, 2, 3], [(0, 1), (1, 2), (2, 3)]
    else:
        return [0], []


# ============================================================
# 3. 从Dynkin图到2D Regge剖分
# ============================================================

def regge_subdivision(cartan_type, deform=0.0, valence_occ=0, valence_cap=0):
    """从核子分布形变构造2D Regge剖分

    核子分布的2D投影：
    - 满壳层→球形→δ_v≈0
    - 未满壳层→形变→δ_v≠0
    - 形变程度由deform和占据比例给出

    剖分方式：中心顶点+n个边界顶点的星形剖分
    n从嘉当矩阵类型给出（A1→1, A3→3, A4→4）
    """
    # 边界顶点数
    n_boundary = {'A1': 1, 'A3': 3, 'A4': 4}.get(cartan_type, 1)

    if n_boundary == 1:
        # A1：单个顶点，无角亏
        positions = np.array([[0.0, 0.0]])
        edges = []
        faces = []
        return positions, edges, faces

    # 星形剖分：中心顶点+n个边界顶点
    # 边界顶点位置从形变参数调制
    positions = [np.array([0.0, 0.0])]  # 中心顶点

    fill_ratio = valence_occ / max(valence_cap, 1) if valence_cap > 0 else 0.5

    for i in range(n_boundary):
        angle = 2 * np.pi * i / n_boundary
        # 形变调制：不同方向的半径不同
        r = 1.0 + deform * 0.5 * np.cos(2 * angle + fill_ratio * np.pi)
        positions.append(np.array([r * np.cos(angle), r * np.sin(angle)]))

    positions = np.array(positions)

    # 边：中心到每个边界顶点 + 边界顶点间连接
    edges = [(0, i+1) for i in range(n_boundary)]
    edges += [(i+1, (i+1) % n_boundary + 1) for i in range(n_boundary)]

    # 面：每个扇形是一个三角形
    faces = [(0, i+1, (i+1) % n_boundary + 1) for i in range(n_boundary)]

    return positions, edges, faces


# ============================================================
# 4. 角亏计算（底空间曲率集中，Gauss-Bonnet）
# ============================================================

def compute_angle_deficit(positions, faces):
    """逐顶点计算角亏 δ_v = 2π - Σθ_i

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

def compute_physical_delta_v(Z, N, p_val_occ, p_val_cap, n_val_occ, n_val_cap, cartan_type):
    """从纤维丛曲率计算角亏 δ_v

    δ_v从两个因素给出：
    1. 嘉当矩阵类型（A1/A3/A4）→ 基本对称性破缺
    2. 壳层占据比例 → 形变调制

    标度从CQM常数给出：β=8π+1, 超导条件βδ_v≈1
    """
    beta = 8 * np.pi + 1

    # 因素1：嘉当矩阵类型的基本角亏
    type_delta = {'A1': 0.0, 'A3': 0.5, 'A4': 1.0}.get(cartan_type, 0.0)

    # 因素2：壳层占据形变
    def shell_deform(occ, cap):
        if cap > 0 and 0 < occ < cap:
            r = occ / cap
            return r * (1 - r) * 4  # 4×抛物线，最大值=1
        return 0.0

    p_deform = shell_deform(p_val_occ, p_val_cap)
    n_deform = shell_deform(n_val_occ, n_val_cap)
    total_deform = (p_deform + n_deform) / 2  # 平均

    # δ_v = (1/β) × (类型因子 + 形变因子) / 2
    # 超导元素βδ_v ≈ 0.9-1.0，非超导元素βδ_v < 0.9
    delta_v = (1.0 / beta) * (type_delta + total_deform) / 2

    return delta_v


# ============================================================
# 5. 元素FG纤维丛构造
# ============================================================

def construct_element_fg(Z):
    """为元素Z构造FG纤维丛

    返回纤维丛四元组 (M_el, P_el, π_el, G_el) 的离散化：
    - 底空间 M_el 的Regge剖分（顶点位置+边+面）
    - 结构群 G_el（从核壳层对称性给出）
    - 角亏 δ_v（底空间曲率集中）
    """
    protons, neutrons = get_nucleons(Z)
    symbol = ELEMENT_SYMBOLS[Z-1] if Z <= len(ELEMENT_SYMBOLS) else f'Z{Z}'

    # 核壳层占据
    p_shells = get_shell_occupation(protons)
    n_shells = get_shell_occupation(neutrons)

    # 从最外层未满壳层确定嘉当矩阵类型
    p_val_occ, p_val_cap, p_val_idx = get_valence_shell_occupation(protons)
    n_val_occ, n_val_cap, n_val_idx = get_valence_shell_occupation(neutrons)

    # 质子和中子各自的最外层嘉当矩阵类型
    p_cartan = get_cartan_type(p_val_occ, p_val_cap)
    n_cartan = get_cartan_type(n_val_occ, n_val_cap)

    # 取更复杂的嘉当矩阵块作为主导
    type_order = {'A1': 0, 'A3': 1, 'A4': 2}
    dominant_type = p_cartan if type_order[p_cartan] >= type_order[n_cartan] else n_cartan

    # 形变参数：未满壳层的占据比例偏离0.5的程度
    p_deform = abs(p_val_occ / max(p_val_cap, 1) - 0.5) * 2 if p_val_cap > 0 else 0
    n_deform = abs(n_val_occ / max(n_val_cap, 1) - 0.5) * 2 if n_val_cap > 0 else 0
    deform = max(p_deform, n_deform)

    # 构造嘉当矩阵
    C = cartan_matrix(dominant_type)

    # 从Dynkin图到Regge剖分（形变调制）
    val_occ = p_val_occ if type_order[p_cartan] >= type_order[n_cartan] else n_val_occ
    val_cap = p_val_cap if type_order[p_cartan] >= type_order[n_cartan] else n_val_cap
    positions, edges, faces = regge_subdivision(dominant_type, deform, val_occ, val_cap)

    # 计算角亏（底空间曲率集中）
    # 从几何剖分计算
    deficits = compute_angle_deficit(positions, faces)
    # 从核物理形变计算（物理角亏）
    physical_delta_v = compute_physical_delta_v(
        protons, neutrons, p_val_occ, p_val_cap, n_val_occ, n_val_cap, dominant_type)

    # 纤维丛数据
    fg_bundle = {
        'Z': Z,
        'symbol': symbol,
        'protons': protons,
        'neutrons': neutrons,
        'mass': atom_db(symbol)[0],
        'p_shells': p_shells,
        'n_shells': n_shells,
        'cartan_type': dominant_type,
        'deform': deform,
        'p_valence': (p_val_occ, p_val_cap),
        'n_valence': (n_val_occ, n_val_cap),
        'cartan_matrix': C.tolist(),
        'positions': positions.tolist(),
        'edges': edges,
        'faces': faces,
        'angle_deficits': deficits.tolist(),
        'physical_delta_v': physical_delta_v,
        'mean_delta_v': physical_delta_v,
        'max_delta_v': physical_delta_v,
    }

    return fg_bundle


# ============================================================
# 6. 穷尽列举118个元素
# ============================================================

def enumerate_all_elements():
    """穷尽列举118个元素的FG纤维丛"""
    results = []
    for Z in range(1, 119):
        fg = construct_element_fg(Z)
        results.append(fg)
    return results


def save_element_fg_table(results, filepath=None):
    """保存元素FG纤维丛表"""
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), 'element_fg_table.json')

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"元素FG纤维丛表已保存：{filepath}")
    print(f"共 {len(results)} 个元素")

    # 统计
    types = {}
    for r in results:
        t = r['cartan_type']
        types[t] = types.get(t, 0) + 1

    print(f"嘉当矩阵类型分布：{types}")

    # 超导元素（βδ_v ≈ 1）
    beta = 8 * np.pi + 1
    print(f"\nβ = {beta:.4f}")
    print(f"超导条件：βδ_v ≈ 1，即 δ_v ≈ {1/beta:.6f}")
    print(f"\n角亏接近1/β的元素（前20个）：")

    candidates = [(r['symbol'], r['mean_delta_v'], beta * r['mean_delta_v'])
                  for r in results if r['mean_delta_v'] > 0]
    candidates.sort(key=lambda x: abs(x[2] - 1.0))

    for symbol, delta_v, beta_delta in candidates[:20]:
        print(f"  {symbol:>3s}: δ_v = {delta_v:.6f}, βδ_v = {beta_delta:.4f}")


# ============================================================
# 主程序
# ============================================================

if __name__ == '__main__':
    print("=" * 60)
    print("CQM元素FG穷尽列举")
    print("118元素→纤维丛→嘉当矩阵→Regge剖分→预计算表")
    print("=" * 60)

    results = enumerate_all_elements()
    save_element_fg_table(results)

    print("\n完成。")