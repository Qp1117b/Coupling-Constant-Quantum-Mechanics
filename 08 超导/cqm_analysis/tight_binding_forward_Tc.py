"""
零成本验证：从紧束缚能带→Fermi面曲率→δ_intrinsic→前向Tc

不依赖外部数据库，用紧束缚模型构造Nb的Fermi面，
独立计算δ_intrinsic，然后前向计算Tc与实验比较。

这是CQM从拟合框架→预言框架的关键测试。
"""

import numpy as np
from scipy import integrate

# CQM常数
HBAR = 1.0546e-34
KB = 1.381e-23
AMU = 1.66e-27
BETA = 8 * np.pi + 1
GAMMA_1 = 14.134725
GAMMA_2 = 21.022040
GAP = GAMMA_2 - GAMMA_1
C2 = 2.0 / 3.0
DELTA_C = 1.0 / BETA

# ============================================================
# 1. Nb紧束缚模型（BCC, d轨道）
# ============================================================

def nb_energy_bcc(kx, ky, kz, t1=-0.5, t2=0.1, t3=0.05, mu=1.0):
    """Nb BCC紧束缚模型（简化d带）

    BCC最近邻: (±1,±1,±1)/2
    BCC次近邻: (±1,0,0), (0,±1,0), (0,0,±1)

    E(k) = μ + t1*Σcos(k·R1) + t2*Σcos(k·R2) + t3*Σcos(k·R3)
    """
    # BCC最近邻 (a/2)(±1,±1,±1)
    nn1 = 0
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            for sz in [-1, 1]:
                nn1 += np.cos(0.5*(sx*kx + sy*ky + sz*kz))

    # BCC次近邻 (±1,0,0)等
    nn2 = 2*(np.cos(kx) + np.cos(ky) + np.cos(kz))

    # 第三近邻 (a)(±1,±1,0)等
    nn3 = 0
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            nn3 += np.cos(sx*kx + sy*ky)
            nn3 += np.cos(sx*kx + sy*kz)
            nn3 += np.cos(sx*ky + sy*kz)

    return mu + t1 * nn1 + t2 * nn2 + t3 * nn3

def energy_gradient(kx, ky, kz, t1=-0.5, t2=0.1, t3=0.05, mu=1.0, dk=1e-5):
    """数值梯度"""
    Ex = (nb_energy_bcc(kx+dk,ky,kz,t1,t2,t3,mu) - nb_energy_bcc(kx-dk,ky,kz,t1,t2,t3,mu)) / (2*dk)
    Ey = (nb_energy_bcc(kx,ky+dk,kz,t1,t2,t3,mu) - nb_energy_bcc(kx,ky-dk,kz,t1,t2,t3,mu)) / (2*dk)
    Ez = (nb_energy_bcc(kx,ky,kz+dk,t1,t2,t3,mu) - nb_energy_bcc(kx,ky,kz-dk,t1,t2,t3,mu)) / (2*dk)
    return np.array([Ex, Ey, Ez])

def energy_hessian(kx, ky, kz, t1=-0.5, t2=0.1, t3=0.05, mu=1.0, dk=1e-4):
    """数值Hessian"""
    E = nb_energy_bcc(kx, ky, kz, t1, t2, t3, mu)
    Exx = (nb_energy_bcc(kx+dk,ky,kz,t1,t2,t3,mu) - 2*E + nb_energy_bcc(kx-dk,ky,kz,t1,t2,t3,mu)) / dk**2
    Eyy = (nb_energy_bcc(kx,ky+dk,kz,t1,t2,t3,mu) - 2*E + nb_energy_bcc(kx,ky-dk,kz,t1,t2,t3,mu)) / dk**2
    Ezz = (nb_energy_bcc(kx,ky,kz+dk,t1,t2,t3,mu) - 2*E + nb_energy_bcc(kx,ky,kz-dk,t1,t2,t3,mu)) / dk**2
    Exy = (nb_energy_bcc(kx+dk,ky+dk,kz,t1,t2,t3,mu) - nb_energy_bcc(kx+dk,ky-dk,kz,t1,t2,t3,mu)
         - nb_energy_bcc(kx-dk,ky+dk,kz,t1,t2,t3,mu) + nb_energy_bcc(kx-dk,ky-dk,kz,t1,t2,t3,mu)) / (4*dk**2)
    Exz = (nb_energy_bcc(kx+dk,ky,kz+dk,t1,t2,t3,mu) - nb_energy_bcc(kx+dk,ky,kz-dk,t1,t2,t3,mu)
         - nb_energy_bcc(kx-dk,ky,kz+dk,t1,t2,t3,mu) + nb_energy_bcc(kx-dk,ky,kz-dk,t1,t2,t3,mu)) / (4*dk**2)
    Eyz = (nb_energy_bcc(kx,ky+dk,kz+dk,t1,t2,t3,mu) - nb_energy_bcc(kx,ky+dk,kz-dk,t1,t2,t3,mu)
         - nb_energy_bcc(kx,ky-dk,kz+dk,t1,t2,t3,mu) + nb_energy_bcc(kx,ky-dk,kz-dk,t1,t2,t3,mu)) / (4*dk**2)
    return np.array([[Exx, Exy, Exz], [Exy, Eyy, Eyz], [Exz, Eyz, Ezz]])

def fermi_surface_curvature(kx, ky, kz, t1=-0.5, t2=0.1, t3=0.05, mu=1.0):
    """计算Fermi面Gaussian曲率

    Fermi面是E(k)=E_F的等能面。
    曲率从Hessian和梯度计算:

    法向量 n = ∇E / |∇E|
    投影Hessian到Fermi面切空间: H_proj = H - (n·H·n) * n⊗n
    主曲率 κ_i = H_proj的本征值 / |∇E|
    Gaussian曲率 K_G = κ₁ * κ₂
    """
    grad = energy_gradient(kx, ky, kz, t1, t2, t3, mu)
    gnorm = np.linalg.norm(grad)

    if gnorm < 1e-10:
        return 0.0, 0.0

    H = energy_hessian(kx, ky, kz, t1, t2, t3, mu)

    # 法向量
    n = grad / gnorm

    # 投影Hessian到切空间
    P = np.eye(3) - np.outer(n, n)  # 投影矩阵
    H_proj = P @ H @ P

    # 主曲率 = H_proj的本征值 / |∇E|
    eigenvalues = np.linalg.eigvalsh(H_proj)
    # 取最大的两个（第三个应该≈0，沿法线方向）
    kappas = np.sort(np.abs(eigenvalues))[-2:] / gnorm

    K_G = kappas[0] * kappas[1]  # Gaussian曲率
    K_mean = (kappas[0] + kappas[1]) / 2  # 平均曲率

    return K_G, K_mean

# ============================================================
# 2. 寻找Fermi面并计算δ_intrinsic
# ============================================================

print("=" * 90)
print("零成本验证：从紧束缚能带→Fermi面曲率→δ_intrinsic→前向Tc")
print("=" * 90)

# 参数扫描找到合理的紧束缚参数（使Fermi面非球形）
# Nb有5个价电子(4d⁴5s¹), BCC
# 调整μ使填充合理

print("\n--- Step 1: 紧束缚能带 ---")
print("Nb BCC紧束缚: E(k) = μ + t1·Σcos(k·R_nn) + t2·Σcos(k·R_2nn) + t3·Σcos(k·R_3nn)")
print("参数: t1=-0.5, t2=0.1, t3=0.05, μ=1.0")

# 检查能带范围
k_test = np.linspace(-np.pi, np.pi, 50)
energies = []
for kx in k_test:
    for ky in k_test:
        for kz in k_test:
            energies.append(nb_energy_bcc(kx, ky, kz))
energies = np.array(energies)
print(f"能带范围: [{energies.min():.4f}, {energies.max():.4f}]")

# Fermi能级（调整使填充约5电子/晶胞）
E_F = 0.0  # 试探
print(f"Fermi能级(试探): E_F = {E_F}")

# ============================================================
# 3. 在Fermi面上采样并计算曲率
# ============================================================

print("\n--- Step 2: Fermi面采样与曲率计算 ---")

# 在BZ中均匀采样，找Fermi面上的点
n_k = 80
kx_range = np.linspace(-np.pi, np.pi, n_k)
ky_range = np.linspace(-np.pi, np.pi, n_k)
kz_range = np.linspace(-np.pi, np.pi, n_k)

dE = 0.05  # Fermi面厚度
fs_points = []

for ix, kx in enumerate(kx_range):
    for iy, ky in enumerate(ky_range):
        for iz, kz in enumerate(kz_range):
            E = nb_energy_bcc(kx, ky, kz)
            if abs(E - E_F) < dE:
                K_G, K_mean = fermi_surface_curvature(kx, ky, kz)
                grad = energy_gradient(kx, ky, kz)
                gnorm = np.linalg.norm(grad)
                if gnorm > 0.01:
                    # Fermi面面积元 dS ≈ dk³ / |∇E| (近似)
                    dS = (2*np.pi/n_k)**3 / gnorm
                    fs_points.append((kx, ky, kz, E, K_G, K_mean, dS, gnorm))

print(f"Fermi面上采样点数: {len(fs_points)}")

if len(fs_points) > 0:
    K_Gs = np.array([p[4] for p in fs_points])
    dSs = np.array([p[6] for p in fs_points])

    # 总Fermi面面积
    A_FS = np.sum(dSs)

    # 平均Gaussian曲率
    K_bar = np.sum(K_Gs * dSs) / A_FS

    # δ_intrinsic (Fermi面曲率变化率)
    delta_curv = (1/(2*np.pi)) * np.sum(np.abs(K_Gs - K_bar) * dSs) / (A_FS * abs(K_bar) if abs(K_bar) > 1e-10 else 1)

    # δ_intrinsic (Berry曲率替代: 用|K_G|的归一化积分)
    delta_abs = (1/(2*np.pi)) * np.sum(np.abs(K_Gs) * dSs) / A_FS

    print(f"\nFermi面几何性质:")
    print(f"  总面积(近似): A_FS = {A_FS:.4f}")
    print(f"  平均Gaussian曲率: K̄_G = {K_bar:.6f}")
    print(f"  K_G范围: [{K_Gs.min():.4f}, {K_Gs.max():.4f}]")
    print(f"  K_G标准差: {np.std(K_Gs):.6f}")
    print(f"  曲率变化率 δ_curv = {delta_curv:.6f}")
    print(f"  |K_G|归一化 δ_abs = {delta_abs:.6f}")
    print(f"  1/β = {DELTA_C:.6f}")
    print(f"  δ_curv/(1/β) = {delta_curv/DELTA_C:.4f}")
    print(f"  δ_abs/(1/β) = {delta_abs/DELTA_C:.4f}")

# ============================================================
# 4. 参数扫描——不同μ值下的δ_intrinsic
# ============================================================

print("\n--- Step 3: 参数扫描——不同Fermi能级下的δ_intrinsic ---")
print(f"{'E_F':>8} {'FS点数':>8} {'K̄_G':>10} {'δ_curv':>10} {'δ_abs':>10} {'δ_curv/(1/β)':>12}")
print("-" * 65)

delta_vs_EF = []

for mu_val in np.linspace(-2.0, 4.0, 21):
    E_F_test = 0.0  # Fermi能级固定在0, 改变μ相当于改变填充
    fs_pts = []
    for kx in kx_range:
        for ky in ky_range:
            for kz in kz_range:
                E = nb_energy_bcc(kx, ky, kz, mu=mu_val)
                if abs(E - E_F_test) < dE:
                    K_G, _ = fermi_surface_curvature(kx, ky, kz, mu=mu_val)
                    grad = energy_gradient(kx, ky, kz, mu=mu_val)
                    gnorm = np.linalg.norm(grad)
                    if gnorm > 0.01:
                        dS = (2*np.pi/n_k)**3 / gnorm
                        fs_pts.append((K_G, dS))

    if len(fs_pts) > 20:
        K_Gs = np.array([p[0] for p in fs_pts])
        dSs = np.array([p[1] for p in fs_pts])
        A = np.sum(dSs)
        Kb = np.sum(K_Gs * dSs) / A
        dc = (1/(2*np.pi)) * np.sum(np.abs(K_Gs - Kb) * dSs) / (A * abs(Kb) if abs(Kb) > 1e-10 else 1)
        da = (1/(2*np.pi)) * np.sum(np.abs(K_Gs) * dSs) / A
        delta_vs_EF.append((mu_val, dc, da))
        print(f"{mu_val:>8.2f} {len(fs_pts):>8} {Kb:>10.4f} {dc:>10.6f} {da:>10.6f} {dc/DELTA_C:>12.4f}")

# ============================================================
# 5. 前向计算Tc
# ============================================================

print("\n--- Step 4: 前向计算Tc ---")

# Nb材料参数
M_Nb = 92.91  # amu
L_Nb = 3.30e-10  # m (BCC最近邻 a√3/2)
z_Nb = 8  # BCC配位数
theta_D_Nb = 275  # K
Tc_exp_Nb = 9.2  # K

# Debye f
k_D = (6 * np.pi**2 * 2 / 3.30**3)**(1/3)  # BCC: n=2/a³
R_Nb = 3.30 * np.sqrt(3) / 2  # BCC最近邻
f_debye = (np.sin(k_D * R_Nb / 2) / (k_D * R_Nb / 2))**2

print(f"\nNb参数:")
print(f"  M = {M_Nb} amu, L = {3.30*np.sqrt(3)/2:.3f} Å, z = {z_Nb}, θ_D = {theta_D_Nb} K")
print(f"  k_D = {k_D:.4f} Å⁻¹, k_D·R = {k_D*R_Nb:.4f}")
print(f"  f(Debye) = {f_debye:.6f}")
print(f"  Tc_exp = {Tc_exp_Nb} K")

# Δδ₀ (从材料结构独立计算)
omega_D = theta_D_Nb * KB / HBAR
s_inter = z_Nb * 2.0 / (M_Nb * AMU)
ddv0_sq = (C2 / L_Nb**2) * (3*HBAR/(4*omega_D)) * (1 - f_debye) * s_inter
ddv0 = np.sqrt(ddv0_sq)
print(f"\n  Δδ₀(独立计算) = {ddv0:.6f}")

# 前向计算Tc（用不同δ_intrinsic值）
print(f"\n  前向计算Tc（不同δ_intrinsic假设）:")
print(f"  {'δ_intrinsic':>14} {'δ_v':>10} {'x':>10} {'Tc_calc':>10} {'Tc_calc/Tc_exp':>14}")
print("  " + "-" * 65)

for delta_intr in [0, 0.01, 0.02, 0.03, 0.035, 0.037, 0.038, DELTA_C, 0.039, 0.04, 0.05]:
    dv = delta_intr  # 常压, δ_pressure=0
    if BETA * dv >= 1:
        print(f"  {delta_intr:>14.6f} {dv:>10.6f} {'∞':>10} {'∞':>10} {'∞':>14}")
        continue
    x = 3 * BETA**2 * ddv0**2 / (16 * (1 - BETA*dv) * GAP)
    if x > 1:
        arccoth_x = 0.5 * np.log((x+1)/(x-1))
        tc_calc = theta_D_Nb / (2 * arccoth_x)
        ratio = tc_calc / Tc_exp_Nb
        print(f"  {delta_intr:>14.6f} {dv:>10.6f} {x:>10.4f} {tc_calc:>10.2f} {ratio:>14.4f}")
    else:
        print(f"  {delta_intr:>14.6f} {dv:>10.6f} {x:>10.4f} {'0':>10} {'0':>14}")

# 反推δ_v
x_exp = 1.0 / np.tanh(theta_D_Nb / (2 * Tc_exp_Nb))
om_exp = 3 * BETA**2 * ddv0**2 / (16 * x_exp * GAP)
dv_rev = (1 - om_exp) / BETA
print(f"\n  反推δ_v = {dv_rev:.6f} (从实验Tc={Tc_exp_Nb}K)")
print(f"  反推δ_v/(1/β) = {dv_rev/DELTA_C:.4f}")

# ============================================================
# 6. 关键检验——δ_intrinsic从Fermi面独立计算能否给出正确Tc?
# ============================================================

print("\n" + "=" * 90)
print("Step 5: 关键检验——独立计算的δ_intrinsic能否预言Tc?")
print("=" * 90)

print(f"""
紧束缚模型结果:
  - Fermi面Gaussian曲率可以独立计算
  - δ_curv (曲率变化率) = {delta_curv:.6f} (E_F=0, μ=1.0)
  - δ_abs (|K_G|归一化) = {delta_abs:.6f}
  - 1/β = {DELTA_C:.6f}
  - 反推δ_v = {dv_rev:.6f}

问题: 独立计算的δ是否接近反推值{dv_rev:.6f}?
  - δ_curv = {delta_curv:.6f}, 比值 = {delta_curv/dv_rev:.4f}
  - δ_abs = {delta_abs:.6f}, 比值 = {delta_abs/dv_rev:.4f}

如果独立δ接近反推值 → CQM是预言框架
如果独立δ远离反推值 → δ_intrinsic公式需要修正

关键不确定性:
  1. 紧束缚模型是简化的, 真实Nb能带更复杂
  2. δ_intrinsic公式有两种候选(Berry曲率 vs Fermi面曲率)
  3. 归一化方式不唯一
  4. 需要DFT能带验证

下一步:
  → 用DFT能带(从Materials Project或QE计算)替代紧束缚
  → 检验δ_intrinsic公式
  → 如果公式正确, 前向Tc应接近实验值
""")

# ============================================================
# 7. 不同紧束缚参数的影响
# ============================================================

print("=" * 90)
print("Step 6: 紧束缚参数对δ_intrinsic的影响")
print("=" * 90)

# 扫描t1参数（控制Fermi面形状）
print(f"\n不同t1(最近邻跃迁)对δ的影响:")
print(f"{'t1':>8} {'FS点数':>8} {'K̄_G':>10} {'δ_curv':>10} {'δ_abs':>10} {'δ_curv/(1/β)':>12}")
print("-" * 65)

for t1_val in [-0.8, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1]:
    fs_pts = []
    for kx in kx_range:
        for ky in ky_range:
            for kz in kz_range:
                E = nb_energy_bcc(kx, ky, kz, t1=t1_val)
                if abs(E - 0.0) < dE:
                    K_G, _ = fermi_surface_curvature(kx, ky, kz, t1=t1_val)
                    grad = energy_gradient(kx, ky, kz, t1=t1_val)
                    gnorm = np.linalg.norm(grad)
                    if gnorm > 0.01:
                        dS = (2*np.pi/n_k)**3 / gnorm
                        fs_pts.append((K_G, dS))

    if len(fs_pts) > 20:
        K_Gs = np.array([p[0] for p in fs_pts])
        dSs = np.array([p[1] for p in fs_pts])
        A = np.sum(dSs)
        Kb = np.sum(K_Gs * dSs) / A
        dc = (1/(2*np.pi)) * np.sum(np.abs(K_Gs - Kb) * dSs) / (A * abs(Kb) if abs(Kb) > 1e-10 else 1)
        da = (1/(2*np.pi)) * np.sum(np.abs(K_Gs) * dSs) / A
        print(f"{t1_val:>8.2f} {len(fs_pts):>8} {Kb:>10.4f} {dc:>10.6f} {da:>10.6f} {dc/DELTA_C:>12.4f}")

# ============================================================
# 8. 总结
# ============================================================

print("\n" + "=" * 90)
print("总结")
print("=" * 90)

print(f"""
验证状态:
  1. 紧束缚能带→Fermi面曲率→δ_intrinsic: 方法可行 ✓
  2. δ_intrinsic的数值: 需要与反推值{dv_rev:.4f}比较
  3. 前向Tc: 对δ_intrinsic极度敏感(1%差→数倍差)

关键发现:
  - Fermi面曲率可以独立计算(不需要DFT)
  - δ_intrinsic公式有两种候选, 需要确定正确的归一化
  - 紧束缚参数显著影响δ值 → 需要真实DFT能带

文献支撑:
  - Berry曲率计算: Xiao et al., RMP 2010
  - Fermi面曲率: 从Hessian直接计算
  - DFT能带: Materials Project / Quantum ESPRESSO
  - 声子谱f: DFPT (Baroni et al., RMP 2001)

最优先下一步:
  ① 安装pymatgen + mp_api
  ② 从Materials Project获取Nb真实DFT能带
  ③ 用真实能带计算δ_intrinsic
  ④ 前向计算Tc, 与实验9.2K比较
  ⑤ 如果成功 → 扩展到Pb, Al等其他超导体
""")