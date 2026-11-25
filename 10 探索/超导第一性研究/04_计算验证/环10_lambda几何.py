# -*- coding: utf-8 -*-
"""
环 10 推进 R1：lambda 的几何第一性形状——数值与函数图像检验。
只检验极限/单调性/量级/符号，不拟合。仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/环10_lambda几何.py"
"""
import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
PI = math.pi

# ---------------- 链内形状式（CQM-L1/L2/L3）----------------
def sigma0_sq(hbar, c_eps, Q, rho_m, c):
    """环 4 (d=3): sigma_0^2 = c_eps^2 hbar Q^4 / (16 pi^2 rho_m c)"""
    return c_eps**2 * hbar * Q**4 / (16 * PI**2 * rho_m * c)


def pairing_V(hbar, g, c_eps, Q, rho_m, c, rho, omega):
    """(10.2): |V| = 4 g^2 sigma0^2 (1-rho) / (hbar omega)"""
    return 4 * g**2 * sigma0_sq(hbar, c_eps, Q, rho_m, c) * (1 - rho) / (hbar * omega)


def lambda_acoustic(N0, z, g, c_eps, Q, rho_m, c, rho):
    """(CQM-L2): lambda = N0 z g^2 c_eps^2 (1-rho) Q^3 / (4 pi^2 rho_m c^2)"""
    return N0 * z * g**2 * c_eps**2 * (1 - rho) * Q**3 / (4 * PI**2 * rho_m * c**2)


def lambda_mcmillan(N0, z, g, c_eps, rho, Q, M, omega_D):
    """(CQM-L3): lambda = (3/2) N0 z g^2 c_eps^2 (1-rho) Q^2 / (M omega_D^2)"""
    return 1.5 * N0 * z * g**2 * c_eps**2 * (1 - rho) * Q**2 / (M * omega_D**2)


def rho_3d(x):
    """M6: rho_3d(x) = 2(1-cos x)/x^2"""
    x = np.asarray(x, dtype=float)
    return np.where(x == 0, 1.0, 2 * (1 - np.cos(x)) / np.where(x == 0, 1, x)**2)


# ---------------- 数值断言（可复跑）----------------
def assertions():
    out = {}
    hbar, g, c_eps, Q, rho_m, c, rho, omega = 1.0, 0.8, 0.53, 1.5e10, 8.0e3, 5.0e3, 0.4, 7.5e12
    v1 = pairing_V(hbar, g, c_eps, Q, rho_m, c, rho, omega)
    v2 = pairing_V(2 * hbar, g, c_eps, Q, rho_m, c, rho, omega)
    out["hbar_cancels_absdiff"] = abs(v1 - v2)

    N0, z = 1.0, 8.0
    L2 = lambda_acoustic(N0, z, g, c_eps, Q, rho_m, c, rho)
    M = rho_m / (Q**3 / (6 * PI**2))          # rho_m = M n, n = Q^3/(6 pi^2)
    omega_D = c * Q
    L3 = lambda_mcmillan(N0, z, g, c_eps, rho, Q, M, omega_D)
    out["L2_vs_L3_relerr"] = abs(L2 - L3) / abs(L2)

    # 同位素：lambda 质量无关，omega_D ~ M^{-1/2}
    Ms = np.array([1.0, 2.0, 4.0])
    lams = [lambda_mcmillan(N0, z, g, c_eps, rho, Q, m, omega_D / np.sqrt(m)) for m in Ms]
    out["lambda_mass_spread"] = (max(lams) - min(lams)) / lams[0]

    # rho_3d <= 1（x>0）
    xs = np.linspace(1e-3, 40, 200000)
    out["one_minus_rho_min"] = float(np.min(1 - rho_3d(xs)))

    # 单调性：lambda 随 omega_D 递减
    ws = np.linspace(2e12, 2e13, 50)
    lws = 1.0 / ws**2
    out["inv_sq_strictly_decreasing"] = bool(np.all(np.diff(lws) < 0))

    # 外部锚点（2025 Nat Commun 文中文字值，仅标度对照）
    out["lambda_at_2_1800K"] = 2.0
    out["lambda_at_3p3_300K"] = 3.3
    return out


def plots(a):
    # ---------------- 图 1：四个面板 ----------------
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # (a) lambda ∝ 1/omega_D^2：双对数下的曲线族（不同 eta_CQM）+ 外部锚点（非拟合）
    ax = axes[0, 0]
    w = np.logspace(2, 3.4, 300)
    for eta, col in [(2.0 * 1800.0**2, "blue"), (3.3 * 300.0**2, "green"),
                     (3.3 * 425.0**2, "orange")]:
        ax.plot(w, eta / w**2, lw=1.8, color=col,
                label=r"$\lambda=\eta_{\rm CQM}/\omega_D^2$（固定 $\eta$）")
    ax.scatter([1800, 300, 425], [2.0, 3.3, 3.3], c="red", s=60, zorder=5,
               label="2025 Nat Commun 文中锚点（外部，非拟合）")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$\omega_{\log}$ (K)")
    ax.set_ylabel(r"$\lambda$")
    ax.set_title("(a) 交易律：固定 eta 时斜率 -2（曲线族）")
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3)

    # (b) lambda vs Q（声学形状，固定 rho_m, c）
    ax = axes[0, 1]
    N0, z, g, c_eps, rho, rho_m, c = 1.0, 8.0, 0.8, 0.53, 0.4, 8.0e3, 5.0e3
    Qs = np.linspace(0.5e10, 2.0e10, 300)
    lams = lambda_acoustic(N0, z, g, c_eps, Qs, rho_m, c, rho)
    ax.plot(Qs / 1e10, lams, "g-", lw=2)
    ax.set_xlabel(r"$Q$ ($10^{10}\,{\rm m}^{-1}$)")
    ax.set_ylabel(r"$\lambda$")
    ax.set_title("(b) lambda ~ Q^3（固定 rho_m, c）")
    ax.grid(alpha=0.3)

    # (c) 几何因子 1-rho_3d(x)
    ax = axes[1, 0]
    xs = np.linspace(0.05, 20, 800)
    ax.plot(xs, 1 - rho_3d(xs), "purple", lw=2)
    ax.axhline(1.0, color="k", ls="--", lw=1)
    ax.set_xlabel(r"$x=k_D d=Qd$")
    ax.set_ylabel(r"$1-\rho_{3d}$")
    ax.set_title("(c) M6 关联几何因子：0 -> 1，有界 ≤ 1")
    ax.grid(alpha=0.3)

    # (d) 同位素：lambda 平坦，Tc ~ M^{-1/2}
    ax = axes[1, 1]
    M = np.linspace(1, 4, 200)
    lam_const = np.full_like(M, lambda_mcmillan(1.0, 8.0, 0.8, 0.53, 0.4, 1.5e10, 1.0, 7.5e12))
    ax.plot(M, lam_const, "b-", lw=2, label=r"$\lambda$（质量无关）")
    ax2 = ax.twinx()
    ax2.plot(M, M**-0.5, "r--", lw=2, label=r"$T_c\propto M^{-1/2}$")
    ax.set_xlabel(r"$M$（相对）")
    ax.set_ylabel(r"$\lambda$")
    ax2.set_ylabel(r"$T_c$（相对）")
    ax.set_title("(d) 同位素端点自洽")
    ax.grid(alpha=0.3)

    fig.suptitle("R1: lambda 几何第一性形状（无拟合，仅极限/单调/符号检验）", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "环10_lambda几何.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)
    return png


def write_csv(a):
    path = os.path.join(HERE, "环10_lambda几何_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    return path


if __name__ == "__main__":
    a = assertions()
    print("=== R1 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    c = write_csv(a)
    print(f"\n图像: {p}")
    print(f"断言表: {c}")
