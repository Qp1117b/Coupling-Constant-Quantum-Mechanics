"""
Tc前向公式探索：5策略合并分析

核心: 前向Tc公式搜索（主函数）
策略1: 对数近似公式 — 用对数近似绕过δ_v的临界点敏感问题
策略2: 紧束缚验证 — 从紧束缚能带→Fermi面曲率→前向Tc
策略3: 替代路径 — 探索替代Tc推导路径(热涨落/Kuramoto/多项式)
策略4: BCS-like参数化 — BCS-like重新参数化探索
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework')
from atom_db import ATOM_DB, atom_db

import csv, re, math
import numpy as np
from collections import defaultdict
from scipy.optimize import minimize_scalar, minimize

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
BETA = 8 * math.pi + 1
GAP = 21.022040 - 14.134725
C2_REGGE = 2.0 / 3.0
DELTA_C = 1.0 / BETA


def arccoth(x):
    if x > 1.001:
        return 0.5 * np.log((x + 1) / (x - 1))
    return 100


def tc_from_x(x, theta_D):
    if x <= 1: return 0
    return theta_D / (2 * arccoth(x))


def ddv0_calc(M_amu, L_ang, theta_D, z, f=0.5):
    L = L_ang * 1e-10; w = theta_D * KB / HBAR
    s = z * 2.0 / (M_amu * AMU)
    return np.sqrt(max((C2_REGGE / L**2) * (3 * HBAR / (4 * w)) * (1 - f) * s, 0))


# =====================================================
# 主函数: 前向Tc公式搜索
# =====================================================

def main_forward_tc_formula_search():
    print("=" * 100)
    print("前向Tc公式搜索：用CV(曲率变异系数)前向预测Tc")
    print("=" * 100)

    materials = [
        ("Cu", False, 0.0, 0.000, 63.55, 3.61, 343, 11, "球形Fermi面"),
        ("Ag", False, 0.0, 0.000, 107.9, 4.09, 225, 11, "球形Fermi面"),
        ("Au", False, 0.0, 0.000, 197.0, 4.08, 170, 11, "球形Fermi面"),
        ("Na", False, 0.0, 0.069, 22.99, 4.23, 156, 9, "近球形"),
        ("K", False, 0.0, 0.069, 39.10, 5.23, 91, 13, "近球形"),
        ("Al", True, 1.2, 0.198, 26.98, 2.86, 428, 12, "FCC轻微变形"),
        ("Pb", True, 7.2, 0.318, 207.2, 3.50, 105, 14, "FCC接触BZ"),
        ("Nb", True, 9.2, 0.674, 92.91, 2.86, 275, 8, "BCC嵌套"),
        ("V", True, 5.4, 0.833, 50.94, 2.62, 383, 8, "BCC嵌套"),
        ("Nb3Sn", True, 18.0, 1.088, None, None, 400, None, "A15平坦"),
        ("V3Si", True, 17.1, 1.502, None, None, 500, None, "A15平坦"),
        ("CuO2", True, 95.0, 0.371, None, None, 400, None, "van Hove"),
        ("LSCO", True, 40.0, 0.683, None, None, 350, None, "近van Hove"),
        ("Org", True, 12.0, 3.162, None, None, 100, None, "准1D圆柱"),
    ]

    for i, (n, sc, tc, cv, M, L, tD, Z, d) in enumerate(materials):
        if M is not None:
            materials[i] = (n, sc, tc, cv, M, L, tD, Z, d, ddv0_calc(M, L, tD, Z))
        else:
            materials[i] = (n, sc, tc, cv, M, L, tD, Z, d, None)

    def formula_1(ddv0, cv, theta_D, alpha):
        if ddv0 is None: return None
        x = alpha * ddv0**2 * cv / GAP
        return tc_from_x(x, theta_D)

    def formula_2(ddv0, cv, theta_D, alpha):
        if ddv0 is None: return None
        x = alpha * ddv0**2 * cv**2 / GAP
        return tc_from_x(x, theta_D)

    def formula_3(ddv0, cv, theta_D, alpha):
        if ddv0 is None: return None
        x = alpha * ddv0**2 * np.tanh(cv) / GAP
        return tc_from_x(x, theta_D)

    def formula_4(ddv0, cv, theta_D, alpha):
        if ddv0 is None: return None
        x = alpha * ddv0**2 * (1 - np.exp(-cv)) / GAP
        return tc_from_x(x, theta_D)

    def formula_5(ddv0, cv, theta_D, alpha):
        if ddv0 is None: return None
        delta_v = (1.0 / BETA) * np.exp(-alpha * cv)
        if BETA * delta_v >= 1: return 0
        x = 3 * BETA**2 * ddv0**2 / (16 * (1 - BETA * delta_v) * GAP)
        return tc_from_x(x, theta_D)

    def formula_6(ddv0, cv, theta_D, alpha):
        if ddv0 is None: return None
        delta_v = (1.0 / BETA) / (1 + alpha * cv)
        if BETA * delta_v >= 1: return 0
        x = 3 * BETA**2 * ddv0**2 / (16 * (1 - BETA * delta_v) * GAP)
        return tc_from_x(x, theta_D)

    def formula_7(ddv0, cv, theta_D, alpha):
        if ddv0 is None: return None
        delta_v = (1.0 / BETA) * (1 - np.tanh(alpha * cv)) / 2
        if BETA * delta_v >= 1: return 0
        x = 3 * BETA**2 * ddv0**2 / (16 * (1 - BETA * delta_v) * GAP)
        return tc_from_x(x, theta_D)

    def formula_8(ddv0, cv, theta_D, alpha):
        if ddv0 is None: return None
        ddv0_total = np.sqrt(ddv0**2 + alpha * cv)
        x = 3 * BETA**2 * ddv0_total**2 / (16 * GAP)
        return tc_from_x(x, theta_D)

    def formula_9(ddv0, cv, theta_D, alpha):
        if ddv0 is None: return None
        ddv0_total = ddv0 * np.sqrt(1 + alpha * cv)
        x = 3 * BETA**2 * ddv0_total**2 / (16 * GAP)
        return tc_from_x(x, theta_D)

    formulas = [
        ("F1: x=α·Δδ₀²·CV/GAP", formula_1),
        ("F2: x=α·Δδ₀²·CV²/GAP", formula_2),
        ("F3: x=α·Δδ₀²·tanh(CV)/GAP", formula_3),
        ("F4: x=α·Δδ₀²·(1-e^{-CV})/GAP", formula_4),
        ("F5: δ_v=(1/β)e^{-αCV}", formula_5),
        ("F6: δ_v=(1/β)/(1+αCV)", formula_6),
        ("F7: δ_v=(1/β)(1-tanh(αCV))/2", formula_7),
        ("F8: Δδ²=Δδ₀²+α·CV", formula_8),
        ("F9: Δδ²=Δδ₀²(1+α·CV)", formula_9),
    ]

    fit_mats = [m for m in materials if m[1] and m[9] is not None]
    print(f"\n拟合材料({len(fit_mats)}个):")
    for m in fit_mats:
        print(f"  {m[0]:<6} Tc_exp={m[2]:>5.1f}K  CV={m[3]:.3f}  Δδ₀={m[9]:.4f}")

    print("\n" + "-" * 100)
    print(f"{'公式':<35} {'最佳α':>10} {'RMSE(K)':>8} {'最大比值':>8} {'最小比值':>8} {'评分':>8}")
    print("-" * 100)

    results = []
    for name, func in formulas:
        def objective(log_alpha):
            alpha = np.exp(log_alpha)
            sse = 0
            for m in fit_mats:
                tc_calc = func(m[9], m[3], m[6], alpha)
                if tc_calc is None: return 1e10
                sse += (tc_calc - m[2])**2
            return sse

        res = minimize_scalar(objective, bounds=(-20, 20), method='bounded')
        alpha_best = np.exp(res.x)
        rmse = np.sqrt(res.fun / len(fit_mats))

        ratios = []
        for m in fit_mats:
            tc_calc = func(m[9], m[3], m[6], alpha_best)
            if tc_calc and tc_calc > 0 and m[2] > 0:
                ratios.append(tc_calc / m[2])
        if ratios:
            max_r = max(ratios); min_r = min(ratios)
            ratio_spread = max_r / min_r if min_r > 0 else 100
            score = rmse * ratio_spread
        else:
            max_r = min_r = 0; score = 1e10
        results.append((name, func, alpha_best, rmse, max_r, min_r, score))
        print(f"{name:<35} {alpha_best:>10.4f} {rmse:>8.2f} {max_r:>8.2f} {min_r:>8.2f} {score:>8.1f}")

    best = min(results, key=lambda r: r[5])
    print(f"\n最佳公式: {best[0]}, α={best[2]:.4f}, RMSE={best[3]:.2f}K")


# =====================================================
# 策略1: 对数近似
# =====================================================

def strategy_log_approx():
    print("\n" + "=" * 90)
    print("策略1: 前向Tc计算——对数近似公式")
    print("  Tc = θ_D / ln(2λ/η),  η = α·CV - η_c")
    print("=" * 90)

    materials = [
        ("Cu", False, 0.0, 0.000, 63.55, 3.61, 343, 11),
        ("Ag", False, 0.0, 0.000, 107.9, 4.09, 225, 11),
        ("Au", False, 0.0, 0.000, 197.0, 4.08, 170, 11),
        ("Na", False, 0.0, 0.069, 22.99, 4.23, 156, 9),
        ("K", False, 0.0, 0.069, 39.10, 5.23, 91, 13),
        ("Al", True, 1.2, 0.198, 26.98, 2.86, 428, 12),
        ("Pb", True, 7.2, 0.318, 207.2, 3.50, 105, 14),
        ("Nb", True, 9.2, 0.674, 92.91, 2.86, 275, 8),
        ("V", True, 5.4, 0.833, 50.94, 2.62, 383, 8),
    ]

    def lambda_calc(ddv0):
        return 3 * BETA**2 * ddv0**2 / (16 * GAP)

    data = []
    for name, is_sc, tc, cv, M, L, tD, Z in materials:
        ddv0 = ddv0_calc(M, L, tD, Z)
        lam = lambda_calc(ddv0)
        data.append((name, is_sc, tc, cv, ddv0, lam, tD))

    def tc_log_approx(lam, cv, theta_D, alpha, eta_c):
        eta = alpha * cv - eta_c
        if eta <= 0: return 0
        arg = 2 * lam / eta
        if arg <= 1: return 0
        return theta_D / np.log(arg)

    sc_data = [d for d in data if d[1]]

    def objective(params):
        alpha, eta_c = params
        if alpha <= 0: return 1e10
        sse = 0
        for name, is_sc, tc, cv, ddv0, lam, tD in sc_data:
            tc_calc = tc_log_approx(lam, cv, tD, alpha, eta_c)
            sse += (tc_calc - tc)**2
        nsc_data = [d for d in data if not d[1]]
        for name, is_sc, tc, cv, ddv0, lam, tD in nsc_data:
            tc_calc = tc_log_approx(lam, cv, tD, alpha, eta_c)
            if tc_calc > 0:
                sse += 10 * tc_calc**2
        return sse

    best = None
    for log_alpha in np.linspace(-5, 5, 50):
        for eta_c in np.linspace(-0.1, 0.1, 50):
            res = objective([np.exp(log_alpha), eta_c])
            if best is None or res < best[0]:
                best = (res, np.exp(log_alpha), eta_c)
    res = minimize(objective, [best[1], best[2]], method='Nelder-Mead',
                   options={'xatol': 1e-10, 'fatol': 1e-10, 'maxiter': 10000})
    alpha_best, eta_c_best = res.x
    rmse = np.sqrt(res.fun / len(sc_data))

    print(f"拟合结果: α = {alpha_best:.6f}, η_c = {eta_c_best:.6f}, RMSE = {rmse:.2f}K")
    print(f"临界CV = η_c/α = {eta_c_best/alpha_best:.4f}")

    print(f"\n{'名称':<6} {'Tc_exp':>7} {'Tc_calc':>8} {'CV':>6} {'η':>8} {'λ':>8}")
    print("-" * 50)
    for name, is_sc, tc, cv, ddv0, lam, tD in data:
        eta = alpha_best * cv - eta_c_best
        tc_calc = tc_log_approx(lam, cv, tD, alpha_best, eta_c_best)
        tc_e_s = f"{tc:.1f}" if tc > 0 else "—"
        tc_c_s = f"{tc_calc:.2f}" if tc_calc > 0 else "0"
        eta_s = f"{eta:.6f}" if eta > 0 else f"{eta:.6f}✗"
        print(f"{name:<6} {tc_e_s:>7} {tc_c_s:>8} {cv:>6.3f} {eta_s:>8} {lam:>8.5f}")


# =====================================================
# 策略2: 紧束缚验证
# =====================================================

def strategy_tight_binding():
    print("\n" + "=" * 90)
    print("策略2: 从紧束缚能带→Fermi面曲率→前向Tc")
    print("=" * 90)

    def nb_energy_bcc(kx, ky, kz, t1=-0.5, t2=0.1, t3=0.05, mu=1.0):
        nn1 = sum(np.cos(0.5*(sx*kx + sy*ky + sz*kz))
                  for sx in [-1, 1] for sy in [-1, 1] for sz in [-1, 1])
        nn2 = 2*(np.cos(kx) + np.cos(ky) + np.cos(kz))
        nn3 = sum(np.cos(sx*kx + sy*ky) + np.cos(sx*kx + sy*kz) + np.cos(sx*ky + sy*kz)
                  for sx in [-1, 1] for sy in [-1, 1])
        return mu + t1 * nn1 + t2 * nn2 + t3 * nn3

    def energy_gradient(kx, ky, kz, t1=-0.5, t2=0.1, t3=0.05, mu=1.0, dk=1e-5):
        Ex = (nb_energy_bcc(kx+dk,ky,kz,t1,t2,t3,mu) - nb_energy_bcc(kx-dk,ky,kz,t1,t2,t3,mu)) / (2*dk)
        Ey = (nb_energy_bcc(kx,ky+dk,kz,t1,t2,t3,mu) - nb_energy_bcc(kx,ky-dk,kz,t1,t2,t3,mu)) / (2*dk)
        Ez = (nb_energy_bcc(kx,ky,kz+dk,t1,t2,t3,mu) - nb_energy_bcc(kx,ky,kz-dk,t1,t2,t3,mu)) / (2*dk)
        return np.array([Ex, Ey, Ez])

    def energy_hessian(kx, ky, kz, t1=-0.5, t2=0.1, t3=0.05, mu=1.0, dk=1e-4):
        E = nb_energy_bcc(kx, ky, kz, t1, t2, t3, mu)
        Exx = (nb_energy_bcc(kx+dk,ky,kz,t1,t2,t3,mu)-2*E+nb_energy_bcc(kx-dk,ky,kz,t1,t2,t3,mu))/dk**2
        Eyy = (nb_energy_bcc(kx,ky+dk,kz,t1,t2,t3,mu)-2*E+nb_energy_bcc(kx,ky-dk,kz,t1,t2,t3,mu))/dk**2
        Ezz = (nb_energy_bcc(kx,ky,kz+dk,t1,t2,t3,mu)-2*E+nb_energy_bcc(kx,ky,kz-dk,t1,t2,t3,mu))/dk**2
        Exy = (nb_energy_bcc(kx+dk,ky+dk,kz,t1,t2,t3,mu)-nb_energy_bcc(kx+dk,ky-dk,kz,t1,t2,t3,mu)
               -nb_energy_bcc(kx-dk,ky+dk,kz,t1,t2,t3,mu)+nb_energy_bcc(kx-dk,ky-dk,kz,t1,t2,t3,mu))/(4*dk**2)
        Exz = (nb_energy_bcc(kx+dk,ky,kz+dk,t1,t2,t3,mu)-nb_energy_bcc(kx+dk,ky,kz-dk,t1,t2,t3,mu)
               -nb_energy_bcc(kx-dk,ky,kz+dk,t1,t2,t3,mu)+nb_energy_bcc(kx-dk,ky,kz-dk,t1,t2,t3,mu))/(4*dk**2)
        Eyz = (nb_energy_bcc(kx,ky+dk,kz+dk,t1,t2,t3,mu)-nb_energy_bcc(kx,ky+dk,kz-dk,t1,t2,t3,mu)
               -nb_energy_bcc(kx,ky-dk,kz+dk,t1,t2,t3,mu)+nb_energy_bcc(kx,ky-dk,kz-dk,t1,t2,t3,mu))/(4*dk**2)
        return np.array([[Exx, Exy, Exz], [Exy, Eyy, Eyz], [Exz, Eyz, Ezz]])

    def fermi_surface_curvature(kx, ky, kz, t1=-0.5, t2=0.1, t3=0.05, mu=1.0):
        grad = energy_gradient(kx, ky, kz, t1, t2, t3, mu)
        gnorm = np.linalg.norm(grad)
        if gnorm < 1e-10:
            return 0.0, 0.0
        H = energy_hessian(kx, ky, kz, t1, t2, t3, mu)
        n = grad / gnorm
        P = np.eye(3) - np.outer(n, n)
        H_proj = P @ H @ P
        eigenvalues = np.linalg.eigvalsh(H_proj)
        kappas = np.sort(np.abs(eigenvalues))[-2:] / gnorm
        K_G = kappas[0] * kappas[1]
        K_mean = (kappas[0] + kappas[1]) / 2
        return K_G, K_mean

    print("\nNb BCC紧束缚: E(k) = μ + t1·Σcos(k·R_nn) + t2·Σcos(k·R_2nn) + t3·Σcos(k·R_3nn)")
    k_test = np.linspace(-np.pi, np.pi, 50)
    energies = []
    for kx in k_test:
        for ky in k_test:
            for kz in k_test:
                energies.append(nb_energy_bcc(kx, ky, kz))
    energies = np.array(energies)
    print(f"能带范围: [{energies.min():.4f}, {energies.max():.4f}]")

    print("\nFermi面采样与曲率计算...")
    n_k = 30; dE = 0.05
    kx_range = np.linspace(-np.pi, np.pi, n_k)
    ky_range = np.linspace(-np.pi, np.pi, n_k)
    kz_range = np.linspace(-np.pi, np.pi, n_k)

    fs_points = []
    for ix, kx in enumerate(kx_range):
        for iy, ky in enumerate(ky_range):
            for iz, kz in enumerate(kz_range):
                E = nb_energy_bcc(kx, ky, kz)
                if abs(E - 0.0) < dE:
                    K_G, K_mean = fermi_surface_curvature(kx, ky, kz)
                    grad = energy_gradient(kx, ky, kz)
                    gnorm = np.linalg.norm(grad)
                    if gnorm > 0.01:
                        dS = (2*np.pi/n_k)**3 / gnorm
                        fs_points.append((kx, ky, kz, E, K_G, K_mean, dS, gnorm))

    print(f"Fermi面上采样点数: {len(fs_points)}")

    if len(fs_points) > 0:
        K_Gs = np.array([p[4] for p in fs_points])
        dSs = np.array([p[6] for p in fs_points])
        A_FS = np.sum(dSs)
        K_bar = np.sum(K_Gs * dSs) / A_FS
        delta_abs = (1/(2*np.pi)) * np.sum(np.abs(K_Gs) * dSs) / A_FS
        print(f"  总面积: A_FS = {A_FS:.4f}")
        print(f"  平均Gaussian曲率: K̄_G = {K_bar:.6f}")
        print(f"  |K_G|归一化 δ_abs = {delta_abs:.6f}")
        print(f"  1/β = {DELTA_C:.6f}")
        print(f"  δ_abs/(1/β) = {delta_abs/DELTA_C:.4f}")

    print(f"\n关键: Fermi面曲率可以独立计算，δ_intrinsic公式为两种候选。")


# =====================================================
# 策略3: 替代Tc推导路径
# =====================================================

def strategy_alternative_paths():
    print("\n" + "=" * 90)
    print("策略3: 替代Tc推导路径探索")
    print("=" * 90)

    from scipy.optimize import brentq

    theta_D = 275.0; Tc_exp = 9.2
    x_rev = 1.0 / np.tanh(theta_D / (2 * Tc_exp))
    A_rev = x_rev * GAP
    dd0 = 0.031

    print(f"Nb参数: θ_D={theta_D}K, Tc_exp={Tc_exp}K")
    print(f"反推: x={x_rev:.10f}, A={A_rev:.6f}")

    print("\n路径A：热涨落混合条件")
    for alpha in [0.01, 0.1, 1.0, 10.0]:
        def eq_A(T):
            if T <= 0: return 1e10
            return GAP - A_rev * np.tanh(theta_D / (2*T)) - alpha * T / theta_D
        try:
            Tc_A = brentq(eq_A, 0.1, 1000)
            A_pert = A_rev * 1.01
            def eq_A_pert(T):
                return GAP - A_pert * np.tanh(theta_D / (2*T)) - alpha * T / theta_D
            Tc_A_pert = brentq(eq_A_pert, 0.1, 1000)
            sens = abs(Tc_A_pert - Tc_A) / Tc_A / 0.01
            print(f"  α={alpha:5.2f}: Tc={Tc_A:.2f}K, 敏感度={sens:.1f}")
        except:
            print(f"  α={alpha:5.2f}: 无解")

    print("\n路径B：线性温度近似")
    Tc_B = theta_D * (1 - np.sqrt(GAP / A_rev))
    print(f"  Tc = θ_D·(1 - √(GAP/A)) = {Tc_B:.2f}K (实验{Tc_exp}K)")

    print("\n路径C：平方根参数化")
    eta = (A_rev - GAP) / GAP
    Tc_C = theta_D * np.sqrt(eta / 2)
    print(f"  η = {eta:.3e}, Tc ≈ θ_D·√(η/2) = {Tc_C:.2f}K")

    print("\n路径E：Kuramoto型同步阈值")
    rhs = 2 * GAP / (np.pi * BETA * dd0**2)
    print(f"  右边 = 2·GAP/(π·β·Δδ₀²) = {rhs:.4f}")
    if rhs < 1:
        Tc_E = theta_D / (2 * np.arctanh(rhs))
        print(f"  Tc = θ_D/(2·arctanh(右边)) = {Tc_E:.2f}K")
    else:
        print(f"  无超导（阈值未达到）")

    print("\n路径F：多项式温度依赖")
    for p in [1, 2, 3, 4]:
        Tc_F = theta_D * (1 - (GAP / A_rev)**0.5)**(1/p)
        A_pert = A_rev * 1.01
        Tc_F_pert = theta_D * (1 - (GAP / A_pert)**0.5)**(1/p)
        sens_F = abs(Tc_F_pert - Tc_F) / Tc_F / 0.01
        print(f"  p={p}: Tc={Tc_F:.2f}K, 敏感度={sens_F:.2f}")

    print(f"\n最有希望：路径E（Kuramoto型同步阈值）——无1/(1-βδ_v)发散因子。")


# =====================================================
# 策略4: BCS-like重新参数化
# =====================================================

def strategy_bcs_like_reparam():
    print("\n" + "=" * 90)
    print("策略4: BCS-like重新参数化")
    print("=" * 90)
    from numpy.linalg import lstsq

    def parse_f(f):
        f = re.sub(r'[\(（].*?[\)）]', '', f.strip())
        return {e: (float(c) if c else 1.0) for e, c in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f) if e in ATOM_DB}

    def get_mass(c): return sum(ATOM_DB[e][0]*n for e, n in c.items())
    def get_debye(c):
        ws = [(ATOM_DB[e][1], ATOM_DB[e][0]*n) for e, n in c.items() if ATOM_DB[e][1]>0]
        return sum(d*w for d, w in ws)/sum(w for _, w in ws) if ws else 300
    def get_radius(c):
        rs = [ATOM_DB[e][2] for e in c if ATOM_DB[e][2]>0]
        return np.mean(rs) if rs else 1.5
    def get_bulk(c):
        bs = [ATOM_DB[e][3] for e in c if ATOM_DB[e][3]>0]
        return np.mean(bs) if bs else 50

    def ddv_inter_(M, L, tD, z, f=0.5):
        L_m = L*1e-10; w = tD*KB/HBAR; s = z*2.0/(M*AMU)
        return math.sqrt(max((C2_REGGE/L_m**2)*(3*HBAR/(4*w))*(1-f)*s, 0))

    def ddv_intra_(edges, l, tD, f=0.5):
        l_m = l*1e-10; w = tD*KB/HBAR
        s = sum((1.0/(mi*AMU)+1.0/(mj*AMU)) for mi, mj in edges)
        return math.sqrt(max((C2_REGGE/l_m**2)*(3*HBAR/(4*w))*(1-f)*s, 0))

    def estimate_p(formula, cat, condition):
        comp = parse_f(formula)
        if not comp: return None
        n_atoms = sum(comp.values())
        M = get_mass(comp); r = get_radius(comp); tD = get_debye(comp); B = get_bulk(comp)
        P = 0
        if '高压' in condition or 'GPa' in condition:
            pm = re.search(r'~?(\d+)GPa', condition)
            P = int(pm.group(1)) if pm else 50
        L = 2*r; l_intra = 2*r; z = 6; edges = []; f = 0.5
        if '元素' in cat:
            tD = ATOM_DB.get(list(comp.keys())[0], (0,300,1.5,50))[1] or tD
            if tD < 50: tD = 300
            z = 12; f = 0.5
        elif 'A15' in cat: tD = max(tD,400); z = 8; L = 2*r*0.9; f = 0.4
        elif '氢化物' in cat:
            tD = max(tD,1500); B = max(B,200); z = 8; L = 2.0; l_intra = 1.7
            n_h = comp.get('H',0); n_m = n_atoms - n_h
            if n_h > 0 and n_m > 0:
                m_m = (M - n_h*1.008)/n_m; edges = [(m_m,1.008)]*int(min(n_h,4))
            f = 0.5
        elif '铜氧' in cat:
            tD = max(tD,400); z = 6; L = 3.8; l_intra = 1.9
            if 'Cu' in comp and 'O' in comp: edges = [(63.55,16.0)]*2
            f = 0.4
        elif '铁基' in cat:
            tD = max(tD,350); z = 6; L = 3.5; l_intra = 2.0
            if 'Fe' in comp:
                if 'As' in comp: edges = [(55.85,74.92)]*2
                elif 'Se' in comp: edges = [(55.85,78.97)]*2
            f = 0.4
        elif '有机' in cat: tD = max(tD,100); z = 4; L = 5.0; f = 0.5
        elif '富勒烯' in cat: tD = 100; z = 4; L = 10.0; M = 720; f = 0.5
        elif '石墨' in cat: tD = 200; z = 3; L = 3.35; f = 0.5
        elif '合金' in cat: tD = max(tD,200); z = 12; f = 0.5
        else: tD = max(tD,200); z = 8; f = 0.5
        return tD, M, L, z, edges, l_intra, B, P, f

    with open("superconductors_deduplicated.csv", 'r', encoding='utf-8-sig') as fh:
        reader = csv.reader(fh); header = next(reader); rows = list(reader)

    all_data = []
    for row in rows:
        cat = row[0]; formula = row[1]; tc_str = row[3]
        condition = row[7] if len(row) > 7 else ''
        tc_match = re.match(r'~?(\d+\.?\d*)', tc_str.strip())
        if not tc_match: continue
        tc = float(tc_match.group(1))
        params = estimate_p(formula, cat, condition)
        if not params: continue
        tD, M, L, z, edges, l_intra, B, P, f = params
        di = ddv_inter_(M, L, tD, z, f)
        dn = ddv_intra_(edges, l_intra, tD, f) if edges else 0
        ddv0 = math.sqrt(di**2 + dn**2)
        lam = 3 * BETA**2 * ddv0**2 / (16 * GAP)
        all_data.append({'formula': formula, 'cat': cat, 'tc': tc, 'tD': tD,
                         'ddv0': ddv0, 'lam': lam})

    print(f"加载 {len(all_data)} 个材料")

    print("\n形式5: ln(Tc) = a·ln(θ_D) + b·ln(Δδ₀) + c")
    X = np.array([[np.log(d['tD']), np.log(d['ddv0']), 1] for d in all_data])
    y = np.array([np.log(d['tc']) for d in all_data])
    coef, _, _, _ = lstsq(X, y, rcond=None)
    tc_pred = np.exp(X @ coef)
    y_exp = np.array([d['tc'] for d in all_data])
    errs = np.abs(tc_pred - y_exp) / y_exp
    print(f"  a={coef[0]:.3f}, b={coef[1]:.3f}, c={coef[2]:.3f}")
    print(f"  中位误差={np.median(errs)*100:.0f}%, 2倍内={np.sum(errs<1)/len(errs)*100:.0f}%")

    print("\n形式6: ln(Tc) = a·ln(θ_D) + b·ln(λ) + c")
    X6 = np.array([[np.log(d['tD']), np.log(d['lam']), 1] for d in all_data if d['lam'] > 0])
    y6 = np.array([np.log(d['tc']) for d in all_data if d['lam'] > 0])
    coef6, _, _, _ = lstsq(X6, y6, rcond=None)
    tc_pred6 = np.exp(X6 @ coef6)
    errs6 = np.abs(tc_pred6 - np.exp(y6)) / np.exp(y6)
    print(f"  a={coef6[0]:.3f}, b={coef6[1]:.3f}, c={coef6[2]:.3f}")
    print(f"  中位误差={np.median(errs6)*100:.0f}%, 2倍内={np.sum(errs6<1)/len(errs6)*100:.0f}%")

    print("\n留一法交叉验证 (LOOCV, 类别校准):")
    cat_data = defaultdict(list)
    for d in all_data: cat_data[d['cat']].append(d)
    all_preds_loo = []; all_exps_loo = []
    for i, d_test in enumerate(all_data):
        cat = d_test['cat']
        train = [d for j, d in enumerate(all_data) if j != i and d['cat'] == cat]
        if len(train) < 5:
            train = [d for j, d in enumerate(all_data) if j != i]
        X_tr = np.array([[np.log(d['tD']), np.log(d['ddv0']), 1] for d in train])
        y_tr = np.array([np.log(d['tc']) for d in train])
        try:
            coef_tr, _, _, _ = lstsq(X_tr, y_tr, rcond=None)
            x_test = np.array([np.log(d_test['tD']), np.log(d_test['ddv0']), 1])
            tc_pred_val = np.exp(x_test @ coef_tr)
            all_preds_loo.append(tc_pred_val); all_exps_loo.append(d_test['tc'])
        except:
            pass
    errs_loo = np.abs(np.array(all_preds_loo) - np.array(all_exps_loo)) / np.array(all_exps_loo)
    print(f"  中位误差: {np.median(errs_loo)*100:.0f}%")
    print(f"  2倍内: {np.sum(errs_loo<1)/len(errs_loo)*100:.0f}%")
    print(f"  5倍内: {np.sum(errs_loo<4)/len(errs_loo)*100:.0f}%")


# =====================================================
# 主入口
# =====================================================

if __name__ == "__main__":
    main_forward_tc_formula_search()
    strategy_log_approx()
    strategy_tight_binding()
    strategy_alternative_paths()
    strategy_bcs_like_reparam()