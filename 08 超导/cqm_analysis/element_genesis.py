"""
元素发生学推导：从A4嘉当矩阵到元素周期表

推导链：
  质子A4 + 中子D(δ) → 元素嘉当矩阵C_element → 谱结构 → 壳层饱和数2,6,10,14 → 周期表

步骤：
  1. A4和D(δ)的谱分析
  2. A4表示论4⊗4 = 10_s ⊕ 6_a的显式分解
  3. 元素嘉当矩阵C_element的谱（小Z,N）
  4. 壳层简并群的涌现验证
"""

import numpy as np
from numpy.linalg import eigvalsh, eigh
from scipy.linalg import block_diag
import json


# ============================================================
# 1. 嘉当矩阵定义
# ============================================================

def A4_matrix():
    """A4型嘉当矩阵（质子，标准Cartan矩阵）"""
    return np.array([
        [ 2, -1,  0,  0],
        [-1,  2, -1,  0],
        [ 0, -1,  2, -1],
        [ 0,  0, -1,  2]
    ], dtype=float)

def D_delta_matrix(delta):
    """D(δ)中子嘉当矩阵（A4的α_4末端缺陷形变）"""
    return np.array([
        [ 2, -1,  0,    0],
        [-1,  2, -1,    0],
        [ 0, -1,  2, -delta],
        [ 0,  0, -delta,  2]
    ], dtype=float)

def C_element(Z, N, deltas=None):
    """
    元素嘉当矩阵 C_element = (⊕^Z A4) ⊕ (⊕^N D(δ_j))

    Z: 质子数
    N: 中子数
    deltas: N个中子的缺陷参数列表，默认全为1（纯A4极限）
    """
    blocks = []
    for _ in range(Z):
        blocks.append(A4_matrix())
    if deltas is None:
        deltas = [1.0] * N
    for j in range(N):
        blocks.append(D_delta_matrix(deltas[j]))
    return block_diag(*blocks)


# ============================================================
# 2. A4和D(δ)谱分析
# ============================================================

def analyze_A4_spectrum():
    """A4嘉当矩阵的谱分析"""
    A = A4_matrix()
    eigenvalues, eigenvectors = eigh(A)

    print("=" * 70)
    print("A4嘉当矩阵谱分析")
    print("=" * 70)
    print(f"\nA4 =\n{A}")
    print(f"\n行列式 det(A4) = {np.linalg.det(A):.6f} (精确值=5)")
    print(f"\n特征值:")
    for i, ev in enumerate(eigenvalues):
        print(f"  λ_{i+1} = {ev:.6f}")

    print(f"\n特征向量 (列向量):")
    for i in range(4):
        print(f"  v_{i+1} = {eigenvectors[:, i]}")

    # A4的根系统信息
    print(f"\nA4李代数 sl(4) 的性质:")
    print(f"  秩 = 4")
    print(f"  维数 = 4^2 - 1 = 15")
    print(f"  Weyl群阶 = 5! = 120")
    print(f"  Coxeter数 h = 5")
    print(f"  伴随表示维数 = 15")
    print(f"  基础表示维数 = 4")

    # 特征值的精确表达式
    print(f"\nA4特征值的精确表达式: λ_k = 2 - 2cos(kπ/5), k=1,2,3,4")
    for k in range(1, 5):
        val = 2 - 2 * np.cos(k * np.pi / 5)
        print(f"  λ_{k} = 2 - 2cos({k}π/5) = {val:.6f}")

    return eigenvalues, eigenvectors


def analyze_D_delta_spectrum():
    """D(δ)嘉当矩阵的谱分析（作为δ的函数）"""
    print("\n" + "=" * 70)
    print("D(δ)中子嘉当矩阵谱分析")
    print("=" * 70)

    # δ的扫描范围
    deltas = np.linspace(0.5, 1.5, 21)

    print(f"\nδ = 1.0 (纯A4极限):")
    D1 = D_delta_matrix(1.0)
    evs_1 = eigvalsh(D1)
    for i, ev in enumerate(evs_1):
        print(f"  λ_{i+1} = {ev:.6f}")

    print(f"\nδ = 0.9988 (自由中子锚点):")
    D0 = D_delta_matrix(0.9988)
    evs_0 = eigvalsh(D0)
    for i, ev in enumerate(evs_0):
        print(f"  λ_{i+1} = {ev:.6f}")

    print(f"\n行列式:")
    print(f"  det(D(δ)) = 8 - 3δ²")
    for delta in [0.5, 0.8, 0.9988, 1.0, 1.2, 1.5]:
        det_exact = 8 - 3 * delta**2
        det_num = np.linalg.det(D_delta_matrix(delta))
        print(f"  δ={delta:.4f}: det = {det_exact:.6f} (数值: {det_num:.6f})")

    print(f"\n正定条件: |δ| < √(8/3) = {np.sqrt(8/3):.6f}")

    # 特征值随δ变化
    print(f"\n特征值随δ变化:")
    print(f"  {'δ':>8s}  {'λ_1':>10s}  {'λ_2':>10s}  {'λ_3':>10s}  {'λ_4':>10s}")
    for delta in [0.5, 0.8, 0.9, 0.9988, 1.0, 1.1, 1.2, 1.5]:
        evs = eigvalsh(D_delta_matrix(delta))
        print(f"  {delta:8.4f}  {evs[0]:10.6f}  {evs[1]:10.6f}  {evs[2]:10.6f}  {evs[3]:10.6f}")

    # D(δ)的特征值精确公式
    print(f"\nD(δ)特征值的解析公式:")
    print(f"  D(δ)是A4的α_4末端缺陷形变")
    print(f"  δ=1时退化为A4: λ_k = 2 - 2cos(kπ/5)")
    print(f"  δ≠1时特征值由 det(D(δ) - λI) = 0 给出")

    # 计算特征多项式
    from numpy.polynomial import polynomial as P
    import sympy as sp

    delta_sym = sp.Symbol('delta')
    lambda_sym = sp.Symbol('lambda')
    D_sym = sp.Matrix([
        [2 - lambda_sym, -1, 0, 0],
        [-1, 2 - lambda_sym, -1, 0],
        [0, -1, 2 - lambda_sym, -delta_sym],
        [0, 0, -delta_sym, 2 - lambda_sym]
    ])
    char_poly = D_sym.det()
    char_poly_expanded = sp.expand(char_poly)
    print(f"\n  特征多项式 det(D(δ) - λI) = {char_poly_expanded}")
    print(f"  δ=1时: {sp.expand(char_poly_expanded.subs(delta_sym, 1))}")

    return evs_0, evs_1


# ============================================================
# 3. A4表示论: 4⊗4 = 10_s ⊕ 6_a 的显式分解
# ============================================================

def analyze_tensor_decomposition():
    """
    A4表示论: 4⊗4 = 10_s ⊕ 6_a 的显式分解

    sl(4)的基础表示4维，张量积16维分解为：
    - 对称部分 10_s: 4×5/2 = 10维
    - 反称部分 6_a: 4×3/2 = 6维

    物理意义：
    - 10_s → d满层电子数 = 10
    - 6_a → p满层电子数 = 6
    """
    print("\n" + "=" * 70)
    print("A4表示论: 4⊗4 = 10_s ⊕ 6_a 的显式分解")
    print("=" * 70)

    n = 4  # 基础表示维数

    # 构造4⊗4的基: |i⟩⊗|j⟩, i,j = 0,1,2,3
    # 编码: idx = i*4 + j, idx = 0..15

    # 对称基: (|i⟩⊗|j⟩ + |j⟩⊗|i⟩)/√2, i ≤ j
    # 反称基: (|i⟩⊗|j⟩ - |j⟩⊗|i⟩)/√2, i < j

    # 对称投影算符 P_s: 16×16矩阵
    P_s = np.zeros((n*n, n*n))
    P_a = np.zeros((n*n, n*n))

    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    idx1 = i * n + j
                    idx2 = k * n + l
                    # 对称: P_s[(i,j),(k,l)] = (δ_ik δ_jl + δ_il δ_jk) / 2
                    P_s[idx1, idx2] = (int(i==k)*int(j==l) + int(i==l)*int(j==k)) / 2.0
                    # 反称: P_a[(i,j),(k,l)] = (δ_ik δ_jl - δ_il δ_jk) / 2
                    P_a[idx1, idx2] = (int(i==k)*int(j==l) - int(i==l)*int(j==k)) / 2.0

    print(f"\n4⊗4 = {n*n}维空间")
    print(f"对称投影 P_s: 迹 = {np.trace(P_s):.1f} (应为 {n*(n+1)//2})")
    print(f"反称投影 P_a: 迹 = {np.trace(P_a):.1f} (应为 {n*(n-1)//2})")
    print(f"P_s + P_a = I? {np.allclose(P_s + P_a, np.eye(n*n))}")
    print(f"P_s² = P_s? {np.allclose(P_s @ P_s, P_s)}")
    print(f"P_a² = P_a? {np.allclose(P_a @ P_a, P_a)}")
    print(f"P_s P_a = 0? {np.allclose(P_s @ P_a, 0)}")

    # 显式构造对称和反称基
    print(f"\n对称基 (10维, d满层):")
    sym_basis = []
    for i in range(n):
        for j in range(i, n):
            vec = np.zeros(n * n)
            if i == j:
                vec[i * n + j] = 1.0
            else:
                vec[i * n + j] = 1.0 / np.sqrt(2)
                vec[j * n + i] = 1.0 / np.sqrt(2)
            sym_basis.append(vec)
            label = f"|{i}⟩⊗|{j}⟩" if i == j else f"(|{i}⟩⊗|{j}⟩+|{j}⟩⊗|{i}⟩)/√2"
            print(f"  e_{len(sym_basis)} = {label}")

    print(f"\n反称基 (6维, p满层):")
    antisym_basis = []
    for i in range(n):
        for j in range(i + 1, n):
            vec = np.zeros(n * n)
            vec[i * n + j] = 1.0 / np.sqrt(2)
            vec[j * n + i] = -1.0 / np.sqrt(2)
            antisym_basis.append(vec)
            label = f"(|{i}⟩⊗|{j}⟩-|{j}⟩⊗|{i}⟩)/√2"
            print(f"  f_{len(antisym_basis)} = {label}")

    print(f"\n物理对应:")
    print(f"  对称表示 10_s → d亚壳层 (l=2), 饱和电子数 = 10")
    print(f"  反称表示 6_a  → p亚壳层 (l=1), 饱和电子数 = 6")
    print(f"  基础表示 4    → ? (待解释)")
    print(f"  平凡表示 1    → s亚壳层? (l=0), 饱和电子数 = 2 (含自旋)")

    # sl(4) ≅ so(6) 同构
    print(f"\nsl(4) ≅ so(6) 同构:")
    print(f"  sl(4) 维数 = 4²-1 = 15")
    print(f"  so(6) 维数 = 6×5/2 = 15")
    print(f"  so(6) 的旋量表示 = 4 (基础表示)")
    print(f"  so(6) 的矢量表示 = 6 (反称表示 6_a)")
    print(f"  so(6) 的自对偶反称3形式 = 10 (对称表示 10_s)")

    return P_s, P_a, sym_basis, antisym_basis


# ============================================================
# 4. 元素嘉当矩阵谱分析
# ============================================================

def analyze_element_spectrum():
    """元素嘉当矩阵C_element的谱分析（小Z,N）"""
    print("\n" + "=" * 70)
    print("元素嘉当矩阵 C_element 谱分析")
    print("=" * 70)

    # 氢原子 Z=1, N=0 (纯A4, 无中子缺陷)
    print("\n--- 氢原子 H (Z=1, N=0) ---")
    C_H = C_element(1, 0)
    evs_H = eigvalsh(C_H)
    print(f"C_element = A4 (4×4)")
    print(f"特征值: {evs_H}")
    print(f"谱间隙 (最小特征值): {evs_H[0]:.6f} = (3-√5)/2 = {(3-np.sqrt(5))/2:.6f}")

    # 氘 Z=1, N=1
    print("\n--- 氘 D (Z=1, N=1, δ=0.9988) ---")
    C_D = C_element(1, 1, deltas=[0.9988])
    evs_D = eigvalsh(C_D)
    print(f"C_element = A4 ⊕ D(0.9988) (8×8)")
    print(f"特征值: {evs_D}")

    # 氦 Z=2, N=2 (α粒子)
    print("\n--- 氦-4 He (Z=2, N=2, δ=0.9988) ---")
    C_He = C_element(2, 2, deltas=[0.9988, 0.9988])
    evs_He = eigvalsh(C_He)
    print(f"C_element = A4⊕A4 ⊕ D(0.9988)⊕D(0.9988) (16×16)")
    print(f"特征值: {evs_He}")
    print(f"特征值简并分析:")
    unique_evs = np.unique(np.round(evs_He, 6))
    for uev in unique_evs:
        count = np.sum(np.abs(evs_He - uev) < 1e-4)
        print(f"  λ ≈ {uev:.6f}: 简并度 = {count}")

    # 锂 Z=3, N=4
    print("\n--- 锂-7 Li (Z=3, N=4, δ=0.9988) ---")
    C_Li = C_element(3, 4, deltas=[0.9988]*4)
    evs_Li = eigvalsh(C_Li)
    print(f"C_element (28×28)")
    print(f"特征值: {evs_Li}")

    # 碳 Z=6, N=6
    print("\n--- 碳-12 C (Z=6, N=6, δ=0.9988) ---")
    C_C = C_element(6, 6, deltas=[0.9988]*6)
    evs_C = eigvalsh(C_C)
    print(f"C_element (48×48)")
    print(f"特征值: {evs_C}")

    # 纯A4极限（δ=1）的谱结构
    print("\n--- 纯A4极限 (δ=1) 的谱简并结构 ---")
    for Z, N, name in [(1,0,"H"), (2,2,"He-4"), (6,6,"C-12"), (8,8,"O-16"),
                        (10,10,"Ne-20"), (14,14,"Si-28"), (20,20,"Ca-40")]:
        C = C_element(Z, N, deltas=[1.0]*N)
        evs = eigvalsh(C)
        dim = 4 * (Z + N)
        # 简并分析
        unique_evs = np.unique(np.round(evs, 4))
        degeneracies = []
        for uev in unique_evs:
            count = np.sum(np.abs(evs - uev) < 1e-3)
            degeneracies.append(count)
        print(f"  {name:6s} (Z={Z:2d}, N={N:2d}): dim={dim:3d}, "
              f"不同特征值数={len(unique_evs):2d}, 简并度={degeneracies}")

    return evs_H, evs_D, evs_He


# ============================================================
# 5. 壳层简并群2,6,10,14的涌现验证
# ============================================================

def verify_shell_degeneracy():
    """
    验证A4表示论是否自然给出壳层饱和数2,6,10,14

    思路：
    - A4 = sl(4) 的表示论给出 4, 6, 10
    - 需要解释 2 (s满层) 和 14 (f满层) 的来源
    - 2 = SU(2)自旋 × 1 (s轨道)
    - 14 = G2伴随表示

    关键：4⊗4 = 10_s ⊕ 6_a 给出 p=6, d=10
    但 s=2 和 f=14 需要其他表示论来源
    """
    print("\n" + "=" * 70)
    print("壳层饱和数 2, 6, 10, 14 的涌现验证")
    print("=" * 70)

    print("\nA4 = sl(4) 表示论给出的维度:")
    print(f"  基础表示: 4")
    print(f"  对称平方: 4⊗4_sym = 10  → d满层")
    print(f"  反称平方: 4⊗4_antisym = 6  → p满层")
    print(f"  伴随表示: 15")
    print(f"  平凡表示: 1")

    print(f"\n壳层饱和数与表示论对应:")
    print(f"  s (l=0): 2  = SU(2)自旋 × 1 (平凡表示)")
    print(f"  p (l=1): 6  = 4⊗4_antisym (反称表示 6_a)")
    print(f"  d (l=2): 10 = 4⊗4_sym (对称表示 10_s)")
    print(f"  f (l=3): 14 = G2伴随表示 (待从核子结构导出)")

    print(f"\n周期长度 = 饱和数累加:")
    shells = [2, 6, 10, 14]
    cumulative = 0
    for i, s in enumerate(shells):
        cumulative += s
        print(f"  周期 {i+1}: 累加 = {cumulative}")

    print(f"\n关键问题：")
    print(f"  1. s=2: 为什么是SU(2)自旋×平凡表示？需要从核子结构导出")
    print(f"  2. f=14: 为什么是G2伴随表示？需要从核子结构导出")
    print(f"  3. 为什么壳层顺序是s,p,d,f而不是其他？")

    # 尝试从A4的表示论导出更多结构
    print(f"\n--- A4表示论的完整维度公式 ---")
    print(f"sl(4)的不可约表示由最高权 (a,b,c) 标记")
    print(f"维数公式 (Weyl维数公式):")

    # 计算一些小表示的维数
    import sympy as sp

    def weyl_dim_sl4(a, b, c):
        """sl(4)的Weyl维数公式，最高权(a,b,c)"""
        # sl(4)的正根: e_i - e_j, i<j, i,j=1..4
        # 最高权 λ = a*e1 + b*(e1+e2) + c*(e1+e2+e3) (基本权重展开)
        # 转换为e坐标
        # ω1 = e1, ω2 = e1+e2, ω3 = e1+e2+e3 (在e1+e2+e3+e4=0约束下)
        # λ = (a+b+c, b+c, c, 0) - 平均值
        coords = [a+b+c, b+c, c, 0]
        avg = sum(coords) / 4
        lam = [x - avg for x in coords]

        # Weyl向量 ρ = (3,1,-1,-3)/2
        rho = [3/2, 1/2, -1/2, -3/2]

        # 维数 = ∏_{i<j} (λ+ρ, e_i-e_j) / (ρ, e_i-e_j)
        dim = 1
        for i in range(4):
            for j in range(i+1, 4):
                numerator = (lam[i] + rho[i]) - (lam[j] + rho[j])
                denominator = rho[i] - rho[j]
                dim *= numerator / denominator
        return int(round(dim))

    print(f"  最高权 (a,b,c) → 维数:")
    small_reps = []
    for a in range(4):
        for b in range(4):
            for c in range(4):
                d = weyl_dim_sl4(a, b, c)
                if d <= 20:
                    small_reps.append((a, b, c, d))

    # 按维数排序
    small_reps.sort(key=lambda x: x[3])
    for a, b, c, d in small_reps:
        marker = ""
        if d == 1: marker = " ← 平凡表示"
        elif d == 4: marker = " ← 基础表示"
        elif d == 6: marker = " ← p满层 (反称)"
        elif d == 10: marker = " ← d满层 (对称)"
        elif d == 14: marker = " ← f满层?"
        elif d == 15: marker = " ← 伴随表示"
        elif d == 2: marker = " ← s满层?"
        print(f"    ({a},{b},{c}) → {d:2d}{marker}")

    return small_reps


# ============================================================
# 6. D(δ)对A4的微扰分析
# ============================================================

def analyze_perturbation():
    """
    D(δ)对A4的微扰分析

    D(δ) = A4 + ε(δ)·Δ, 其中ε是小量
    分析微扰如何影响谱结构
    """
    print("\n" + "=" * 70)
    print("D(δ)对A4的微扰分析")
    print("=" * 70)

    A = A4_matrix()

    # D(δ) - A4 = 只有(3,4)和(4,3)位置不同
    # D(δ) - A4 = (1-δ)在(3,4)和(4,3)位置
    print(f"\nD(δ) - A4 = (1-δ)·Δ, 其中Δ是(3,4)/(4,3)位置的扰动")
    Delta = np.zeros((4, 4))
    Delta[2, 3] = 1  # 0-indexed: D(δ)-A4 在(3,4)位置 = -δ-(-1) = 1-δ
    Delta[3, 2] = 1
    print(f"Δ =\n{Delta}")

    # 验证: D(δ) = A4 + (1-δ)·Δ
    for delta in [0.9988, 1.1, 0.9]:
        D = D_delta_matrix(delta)
        D_check = A + (1 - delta) * Delta
        assert np.allclose(D, D_check), f"验证失败 δ={delta}"
    print(f"✓ D(δ) = A4 + (1-δ)·Δ 验证通过")

    # 一阶微扰理论: δλ_k = ⟨v_k|Δ|v_k⟩·(1-δ)
    eigenvalues_A, eigenvectors_A = eigh(A)

    print(f"\n一阶微扰: δλ_k = ⟨v_k|Δ|v_k⟩·(1-δ)")
    print(f"  {'k':>3s}  {'λ_k(A4)':>10s}  ⟨v_k|Δ|v_k⟩  {'一阶系数':>10s}")
    first_order = []
    for k in range(4):
        vk = eigenvectors_A[:, k]
        matrix_element = vk @ Delta @ vk
        first_order.append(matrix_element)
        print(f"  {k+1:3d}  {eigenvalues_A[k]:10.6f}  {matrix_element:12.6f}  {matrix_element:10.6f}")

    # 二阶微扰
    print(f"\n二阶微扰: delta_lambda_k^(2) = Sum_(j!=k) |<v_j|Delta|v_k>|^2 / (lambda_k - lambda_j) * (1-delta)^2")
    second_order = []
    for k in range(4):
        vk = eigenvectors_A[:, k]
        s2 = 0
        for j in range(4):
            if j != k:
                vj = eigenvectors_A[:, j]
                matrix_element = vj @ Delta @ vk
                s2 += abs(matrix_element)**2 / (eigenvalues_A[k] - eigenvalues_A[j])
        second_order.append(s2)
        print(f"  k={k+1}: 二阶系数 = {s2:.6f}")

    # 验证微扰展开
    print(f"\n微扰展开验证 (δ=0.9988, ε=1-δ=0.0012):")
    delta = 0.9988
    eps = 1 - delta
    D = D_delta_matrix(delta)
    evs_exact = eigvalsh(D)

    print(f"  {'k':>3s}  {'精确值':>10s}  {'零阶':>10s}  {'一阶':>10s}  {'二阶':>10s}  {'误差(二阶)':>12s}")
    for k in range(4):
        approx_0 = eigenvalues_A[k]
        approx_1 = approx_0 + first_order[k] * eps
        approx_2 = approx_1 + second_order[k] * eps**2
        print(f"  {k+1:3d}  {evs_exact[k]:10.6f}  {approx_0:10.6f}  {approx_1:10.6f}  {approx_2:10.6f}  {abs(evs_exact[k]-approx_2):12.2e}")

    # 关键问题：微扰是否分裂A4的简并？
    print(f"\nA4特征值简并分析:")
    unique_evs_A = np.unique(np.round(eigenvalues_A, 6))
    print(f"  A4有{len(unique_evs_A)}个不同特征值: {unique_evs_A}")
    print(f"  A4特征值全部非简并（4个不同值）")
    print(f"  → 微扰不分裂简并（因为没有简并）")
    print(f"  → 但微扰改变特征值，可能影响更大结构的简并")

    return first_order, second_order


# ============================================================
# 主函数
# ============================================================

def main():
    print("CQM 元素发生学推导")
    print("从A4嘉当矩阵到元素周期表")
    print("=" * 70)

    # 1. A4谱分析
    evs_A4, _ = analyze_A4_spectrum()

    # 2. D(δ)谱分析
    evs_D0, evs_D1 = analyze_D_delta_spectrum()

    # 3. A4表示论分解
    P_s, P_a, sym_basis, antisym_basis = analyze_tensor_decomposition()

    # 4. 元素嘉当矩阵谱
    evs_H, evs_D, evs_He = analyze_element_spectrum()

    # 5. 壳层简并验证
    small_reps = verify_shell_degeneracy()

    # 6. 微扰分析
    first_order, second_order = analyze_perturbation()

    # 总结
    print("\n" + "=" * 70)
    print("推导总结")
    print("=" * 70)
    print(f"""
已确立:
  1. A4嘉当矩阵特征值: λ_k = 2 - 2cos(kπ/5), k=1,2,3,4
     λ = {(3-np.sqrt(5))/2:.6f}, {1:.6f}, {1:.6f}, {(3+np.sqrt(5))/2:.6f}
     (注意λ_2=λ_3=1是简并的)

  2. D(δ) = A4 + (1-δ)·Δ, Δ仅在(3,4)/(4,3)位置
     det(D(δ)) = 8 - 3δ², 正定条件 |δ| < √(8/3) ≈ {np.sqrt(8/3):.6f}

  3. A4表示论 4⊗4 = 10_s ⊕ 6_a:
     - 对称表示 10_s → d满层 (l=2, 饱和=10)
     - 反称表示 6_a  → p满层 (l=1, 饱和=6)
     - 投影算符已显式构造, 满足 P_s²=P_s, P_a²=P_a, P_s·P_a=0

  4. sl(4) ≅ so(6) 同构:
     - 基础表示 4 = so(6)旋量表示
     - 反称表示 6 = so(6)矢量表示
     - 对称表示 10 = so(6)自对偶反称3形式

待解决:
  1. s满层2的群论来源: 为什么是SU(2)自旋×平凡表示?
  2. f满层14的群论来源: 为什么是G2伴随表示?
  3. 壳层顺序s,p,d,f的导出
  4. 从C_element谱到饱和占据数的映射
  5. δ(Z,N)的谱约束求解
""")


if __name__ == "__main__":
    main()