# -*- coding: utf-8 -*-
"""
环 19 相位刚度：BKT 重整化、裸刚度上界、渗流刚度与相界。

归一化：Upsilon_bond = 1, k_B = 1, omega_D = 1, hbar = 1.
本脚本只核对解析形状、不等式与交点，不做数据拟合。

外部基准（只作核对，不是 CQM 推导）：
  二维方格 XY：T_BKT/J = 0.89294，普适跳变 Upsilon_R/J = 2T_BKT/(pi J) = 0.5684.
  渗流刚度指数：2D t_Upsilon ~ 1.3（Loh et al. 2014）。
  无限簇指数：2D beta = 5/36.
"""

import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_CSV = os.path.join(HERE, "环19_相位刚度.csv")
OUT_PNG = os.path.join(HERE, "环19_相位刚度.png")
OUT_SUM = os.path.join(HERE, "环19_相位刚度_摘要.csv")

OMEGA_D = 1.0
PC_SITE = 0.59274605079210   # 审-4 回改：Φ 自变量是座比例 p_pair，阈值为座渗流
T_U = 1.3              # superfluid-stiffness exponent, 2D (external)
BETA_INF = 5.0 / 36.0  # P_inf exponent, 2D (external)
C_CORE_LIST = [2.0, 5.0]  # vortex core energy in units of K0; shape parameter

# ---------------------------------------------------------------- Debye weight


def w_debye(T):
    """V_coh/Z = 2 * int_0^1 x tanh(x/(2T)) dx, with omega_D = 1."""
    if T <= 0.0:
        return 1.0
    x = np.linspace(0.0, 1.0, 8001)
    return 2.0 * np.trapezoid(x * np.tanh(x / (2.0 * T)), x)


def K_bare(T, U0=1.0):
    if T <= 0.0:
        return float("inf")
    return U0 * w_debye(T) / T


def bisect(f, lo, hi, tol=1e-10, n=200):
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0.0:
        raise ValueError(f"root not bracketed: f({lo})={flo}, f({hi})={fhi}")
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if abs(fm) < tol or 0.5 * (hi - lo) < tol:
            return mid
        if flo * fm <= 0.0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


def T_bare(U0=1.0):
    """Bare crossing: U0 * w(T) = 2 T / pi."""
    return bisect(lambda T: U0 * w_debye(T) - 2.0 * T / math.pi, 1e-8, 50.0)


# ---------------------------------------------------------------- Kosterlitz RG


def rg_flow(K0, y0, lmax=10.0, n=12000):
    """Integrate du/dl = 4 pi^2 y^2, dy/dl = (2 - pi K) y, u = 1/K.

    The coefficient 4 pi^2 follows the convention of Nelson's review (51);
    only the fixed point K = 2/pi and the direction are used.  The step is
    kept small because the fixed point is marginal: a coarse RK4 step can
    overshoot and produce a spurious runaway.
    """
    u = 1.0 / K0
    y = y0
    us = [u]
    ys = [y]
    ls = [0.0]
    dl = lmax / n
    for i in range(n):
        def deriv(uu, yy):
            return 4.0 * math.pi ** 2 * yy * yy, (2.0 - math.pi / uu) * yy
        k1u, k1y = deriv(u, y)
        k2u, k2y = deriv(u + 0.5 * dl * k1u, y + 0.5 * dl * k1y)
        k3u, k3y = deriv(u + 0.5 * dl * k2u, y + 0.5 * dl * k2y)
        k4u, k4y = deriv(u + dl * k3u, y + dl * k3y)
        u += dl * (k1u + 2 * k2u + 2 * k3u + k4u) / 6.0
        y += dl * (k1y + 2 * k2y + 2 * k3y + k4y) / 6.0
        us.append(u)
        ys.append(y)
        ls.append((i + 1) * dl)
        if y > 10.0:
            break
    return np.array(ls), np.array(us), np.array(ys)


def is_superfluid(K0, y0):
    """Classify a flow: superfluid if the fugacity decreases."""
    if y0 <= 1e-300:
        return True
    _, _, ys = rg_flow(K0, y0)
    return ys[-1] < ys[0]


def T_bkt_rg(U0=1.0, c=5.0):
    """BKT temperature from the RG separatrix, with y0 = exp(-c K0)."""
    def sf(T):
        K0 = K_bare(T, U0)
        return is_superfluid(K0, math.exp(-c * K0))
    lo, hi = 1e-6, 50.0
    # expand if the bracket is not yet correct
    while not sf(lo):
        lo *= 0.5
    while sf(hi):
        hi *= 2.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if sf(mid):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------- percolation


def Phi_power(p, pc=PC_SITE, expo=T_U):
    if p <= pc:
        return 0.0
    return ((p - pc) / (1.0 - pc)) ** expo


def p_star(T, U0=1.0, pc=PC_SITE, expo=T_U):
    """Temperature-dependent bond threshold from U0 w(T) Phi(p) = 2T/pi."""
    arg = 2.0 * T / (math.pi * U0 * w_debye(T))
    if arg <= 0.0:
        return pc
    if arg >= 1.0:
        return 1.0
    return pc + (1.0 - pc) * arg ** (1.0 / expo)


# ---------------------------------------------------------------- main


def main():
    TBKT_XY = 0.89294
    JUMP_XY = 2.0 * TBKT_XY / math.pi

    rows = []
    summary = []

    # --- panel A: RG trajectories
    K0_list = [0.45, 0.55, 0.6366, 0.80, 1.20]
    for K0 in K0_list:
        y0 = math.exp(-5.0 * K0)
        ls, us, ys = rg_flow(K0, y0, lmax=10.0)
        for l, u, y in zip(ls, us, ys):
            rows.append(("A", K0, l, 1.0 / u, y))

    # --- panel B: T_bare vs T_BKT for two core energies
    U0_list = [0.5, 1.0, 2.0, 4.0]
    for c in C_CORE_LIST:
        for U0 in U0_list:
            tb = T_bare(U0)
            tr = T_bkt_rg(U0, c)
            rows.append(("B", c, U0, tb, tr))
            summary.append(("T_bare", c, U0, tb, ""))
            summary.append(("T_BKT_RG", c, U0, tr, ""))
            summary.append(("ratio", c, U0, tr / tb, ""))

    # --- panel C: percolation stiffness
    p_grid = np.linspace(PC_SITE, 1.0, 401)
    for p in p_grid:
        rows.append(("C", p, Phi_power(p), Phi_power(p, expo=BETA_INF), 0.0))

    # --- panel D: phase boundary p_*(T)
    T_grid = np.linspace(0.0, T_bare(1.0) * 1.02, 401)
    for T in T_grid:
        rows.append(("D", T, p_star(T), 0.0, 0.0))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["panel", "x", "y", "z", "w"])
        w.writerows(rows)

    with open(OUT_SUM, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["quantity", "c_core", "U0", "value", "note"])
        w.writerow(["T_BKT_XY", "", "", TBKT_XY, "external anchor, J=1"])
        w.writerow(["jump_XY", "", "", JUMP_XY, "2*T_BKT/pi"])
        w.writerows(summary)

    # ------------------------------------------------------------ figure
    fig, ax = plt.subplots(2, 2, figsize=(12.5, 10.0))

    # A: RG flow in (K, y)
    for K0 in K0_list:
        y0 = math.exp(-5.0 * K0)
        ls, us, ys = rg_flow(K0, y0, lmax=10.0)
        ax[0, 0].plot(1.0 / us, ys, lw=1.6, label=f"K0={K0:.3f}")
    ax[0, 0].axvline(2.0 / math.pi, color="k", ls="--", lw=1.0,
                     label=r"$K_*=2/\pi$")
    ax[0, 0].set_xlabel(r"$K=\Upsilon/(k_BT)$")
    ax[0, 0].set_ylabel(r"$y$")
    ax[0, 0].set_yscale("log")
    ax[0, 0].set_xlim(0.0, 1.4)
    ax[0, 0].set_ylim(1e-12, 10.0)
    ax[0, 0].set_title("A  Kosterlitz RG 流：分离线落在 $K_*=2/\\pi$")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    # B: T_bare vs T_BKT
    for c, marker in zip(C_CORE_LIST, ["o", "s"]):
        tb = [T_bare(U0) for U0 in U0_list]
        tr = [T_bkt_rg(U0, c) for U0 in U0_list]
        ax[0, 1].plot(U0_list, tb, marker + "-", lw=1.6,
                      label=f"$T_{{\\rm bare}}$, c={c:g}")
        ax[0, 1].plot(U0_list, tr, marker + "--", lw=1.6,
                      label=f"$T_{{\\rm BKT}}$, c={c:g}")
    ax[0, 1].set_xlabel(r"$\Upsilon_0$")
    ax[0, 1].set_ylabel("温度")
    ax[0, 1].set_title(r"B  裸交点只是上界：$T_{\rm BKT}\leq T_{\rm bare}$")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    # C: percolation exponents
    delta = np.linspace(1e-4, 1.0 - PC_SITE, 800)
    p = PC_SITE + delta
    ax[1, 0].loglog(delta, delta ** T_U, lw=1.8,
                    label=r"$\Upsilon_{\rm eff}\sim\delta^{t_\Upsilon}$, $t_\Upsilon=1.3$")
    ax[1, 0].loglog(delta, delta ** BETA_INF, lw=1.8, ls="--",
                    label=r"$P_\infty\sim\delta^{\beta}$, $\beta=5/36$")
    ax[1, 0].set_xlabel(r"$\delta=p-p_c$")
    ax[1, 0].set_ylabel("归一化读出")
    ax[1, 0].set_title("C  刚度指数 $t_\\Upsilon\\approx1.3$ 不是 $P_\\infty$ 的 $\\beta$")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3, which="both")

    # D: phase boundary p_*(T)
    Tb = T_bare(1.0)
    Ts = np.linspace(0.0, Tb, 600)
    ps = np.array([p_star(T) for T in Ts])
    ax[1, 1].plot(Ts, ps, lw=2.0, label=r"$p_*(T)$（刚度阈值）")
    ax[1, 1].axhline(PC_SITE, color="k", ls=":", lw=1.0,
                     label=r"$p_c({\rm site})=0.592746$")
    ax[1, 1].axvline(Tb, color="gray", ls="--", lw=1.0,
                     label=r"$T_{\rm bare}$")
    # illustrative trajectories (not the 环15 distribution)
    for q0, kappa in [(0.95, 2.0), (0.80, 1.0), (0.65, 0.7)]:
        qs = q0 * np.array([w_debye(T) for T in Ts]) ** kappa
        ax[1, 1].plot(Ts, qs, lw=1.0, ls="--",
                      label=f"示意 $q(T)$, q0={q0:g}, k={kappa:g}")
    ax[1, 1].set_xlabel("$T$")
    ax[1, 1].set_ylabel("键占据比例 $q$")
    ax[1, 1].set_title("D  相界 $p_*(T)$：$p_c$ 只是 $T=0$ 端点")
    ax[1, 1].legend(fontsize=7)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)

    # ------------------------------------------------------------ printed checks
    print(f"T_BKT(XY) = {TBKT_XY:.6f}, jump = {JUMP_XY:.6f}")
    for c in C_CORE_LIST:
        ratios = []
        for U0 in U0_list:
            tb = T_bare(U0)
            tr = T_bkt_rg(U0, c)
            ratios.append(tr / tb)
        print(f"c={c:g}: T_BKT/T_bare = " +
              ", ".join(f"{r:.6f}" for r in ratios) +
              f"  max={max(ratios):.6f}")
    for d in [1e-2, 1e-3, 1e-4]:
        pt = d ** T_U
        pb = d ** BETA_INF
        print(f"delta={d:g}: Phi_t={pt:.6e}, P_inf={pb:.6e}, ratio={pt/pb:.6e}")
    print(f"T_bare(U0=1) = {T_bare(1.0):.6f}")
    for T in [0.1, 0.3, 0.5, 0.65]:
        print(f"p_*(T={T}) = {p_star(T):.6f}")
    print(f"p_*(0) = {p_star(0.0):.6f}, p_*(T_bare) = {p_star(T_bare(1.0)):.6f}")
    print("note: T > T_bare has no solution; p_* is clamped at 1 in the plot.")


if __name__ == "__main__":
    main()
