# -*- coding: utf-8 -*-
"""
Ring 8 / M5: the slope of f is fixed by DM.4's kappa_f, not by C1=1.

Chain inputs:
  DM.4 : dC_ij = kappa_f (d eps_i - d eps_j) + O(d^2)        (a FIRST-ORDER equality)
  (5.2): lambda_ij = ln r_ij = 1/2 ln(1 - ell_ij/(2 pi))
  (8A.1): kappa_f = -d ln v_tau / d eps = 1/(4 pi v_tau^2),  v_tau^2 = 1 - eps/(2 pi)
  matrix branch: C_ij = delta_ij + f(lambda_ij), f odd, strictly monotone

Consequence (8A.5)-(8A.6):
  dC/dlambda = -4 pi kappa_f = -1/v_tau^2  ->  f(u) = -u + O(u^3),  |f'(0)| = 1 at eps=0.

Panels:
  A  f(u) = -u + d u^3 for d = 0, +-1, +-10 on u in [0, 0.01]: visually identical;
     inset: relative deviation |d u^3 / (c u)| = |d/c| u^2.
  B  4 pi kappa_f = 1/(1 - eps/2pi) vs eps: exactly 1 at eps=0, -> 2 as eps -> pi.
  C  variance identity: <(dC)^2> = c^2 <(dlambda)^2> = (c/4pi)^2 <(dell)^2>, so the
     ratio to kappa_f^2 <(dell)^2> stays 1 for any d; deviation grows only as u^2.

No fit, no free parameter except the displayed cubic coefficient d (which is the
quantity being shown to be unobservable).
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
OUT_PNG = os.path.join(HERE, "环08_f斜率定标.png")
OUT_CSV = os.path.join(HERE, "环08_f斜率定标.csv")

TWO_PI = 2.0 * math.pi


def kappa_f(eps):
    """kappa_f = 1/(4 pi (1 - eps/2pi))."""
    return 1.0 / (4.0 * math.pi * (1.0 - eps / TWO_PI))


def lam(ell):
    """lambda = 1/2 ln(1 - ell/2pi)."""
    if ell >= TWO_PI:
        return float("-inf")
    return 0.5 * math.log(1.0 - ell / TWO_PI)


def main():
    rows = []
    print("Ring 8 / M5: slope of f fixed by DM.4")
    print("=" * 72)

    # ---------- A: cubic coefficient is unobservable ----------
    print("\nA  f(u) = -u + d u^3 : relative deviation |d/c| u^2")
    ds = [0.0, 1.0, -1.0, 10.0, -10.0]
    for d in ds:
        for u in (1e-3, 5e-3, 1e-2):
            rel = abs(d) * u * u
            rows.append(("A_rel_dev", d, u, rel, 0.0))
        rel_at_1e2 = abs(d) * (1e-2) ** 2
        print(f"   d={d:+.1f}: rel dev at u=1e-2 is {rel_at_1e2:.3e}")

    # ---------- B: kappa_f and 4 pi kappa_f ----------
    print("\nB  4*pi*kappa_f = 1/(1 - eps/2pi):")
    for eps in (0.0, 0.05, 0.1, 0.5, 1.0, math.pi, TWO_PI * 0.9):
        k = kappa_f(eps)
        print(f"   eps={eps:7.4f}  kappa_f={k:.6f}  4*pi*kappa_f={4*math.pi*k:.6f}")
        rows.append(("B_kappa", eps, k, 4 * math.pi * k, 1.0 / (1 - eps / TWO_PI)))

    # ---------- C: variance identity ----------
    print("\nC  <(dC)^2> / (kappa_f^2 <(dell)^2>) = (c/(4 pi kappa_f))^2 , c = -4 pi kappa_f -> 1")
    sig_ell = 1e-2
    for d in ds:
        for u in (1e-3, 5e-3, 1e-2):
            # dC = c*u + d*u^3 with c = -1 (eps=0); lead ratio to kappa_f* dell:
            c = -1.0
            # <(dC)^2> / (kappa_f^2 <dell^2>) with dell = 4 pi * sig... use exact algebra:
            # c*u = -(dell/4pi) so ratio = (c/(-4pi kappa_f))^2 = 1 by construction;
            # the cubic adds a term  -d*(dell/4pi)^3, relative size d*u^2.
            ratio = 1.0
            dev = abs(d) * u * u
            rows.append(("C_var_ratio", d, u, ratio, dev))
    print("   leading ratio is exactly 1 for every d (by (8A.5));")
    print("   the cubic contributes a relative deviation |d/c| u^2, tabulated in panel A.")

    # ---------- figure ----------
    fig = plt.figure(figsize=(14.5, 4.6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.15, 1, 1])

    # A
    ax = fig.add_subplot(gs[0, 0])
    u = np.linspace(0, 1e-2, 400)
    for d, col, ls in [(0.0, "#1f4e79", "-"), (1.0, "#2e7d32", "--"),
                       (-1.0, "#2e7d32", ":"), (10.0, "#c00000", "--"),
                       (-10.0, "#c00000", ":")]:
        ax.plot(u, -u + d * u ** 3, lw=1.8, color=col, ls=ls,
                label=f"$d={d:+.0f}$")
    ax.set_xlabel(r"$u=\lambda$ (rad)")
    ax.set_ylabel(r"$f(u)$")
    ax.set_title("A 三次项在 $|u|\\leq0.01$ 内不可分辨\n（$|d|$ 取到 10 仍重合）", fontsize=10)
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(alpha=0.3)

    # B
    ax = fig.add_subplot(gs[0, 1])
    e = np.linspace(0, TWO_PI * 0.98, 500)
    y = 1.0 / (1.0 - e / TWO_PI)
    ax.plot(e, y, lw=2.2, color="#1f4e79")
    ax.plot([0], [1], "o", ms=8, color="#2e7d32", zorder=5)
    ax.annotate("平直 $\\varepsilon=0$：$4\\pi\\kappa_f=1$", xy=(0, 1), xytext=(0.9, 1.35),
                fontsize=9, color="#2e7d32")
    ax.axhline(1, ls=":", lw=0.9, color="k")
    ax.set_xlabel(r"$\varepsilon$ (rad)")
    ax.set_ylabel(r"$4\pi\kappa_f=1/v_\tau^2$")
    ax.set_ylim(0.9, 7)
    ax.set_title("B 斜率定标 $|f'(0)|=4\\pi\\kappa_f$\n$(\\varepsilon\\to0$ 时精确为 1$)$", fontsize=10)
    ax.grid(alpha=0.3)

    # C
    ax = fig.add_subplot(gs[0, 2])
    dg = np.linspace(0, 20, 200)
    ug = np.logspace(-4, -2, 200)
    D, U = np.meshgrid(dg, ug)
    Z = D * U * U
    cs = ax.contourf(D, U, Z, levels=np.logspace(-9, -2, 15), cmap="viridis")
    ax.set_yscale("log")
    fig.colorbar(cs, ax=ax, label="相对偏差")
    ax.contour(D, U, Z, levels=[1e-4, 1e-3], colors="w", linewidths=1.0)
    ax.set_xlabel(r"$|d/c|$（三次系数比，未知）")
    ax.set_ylabel(r"$u=\lambda$ (rad)")
    ax.set_title("C 高阶项偏差 $= |d/c|\\,u^2$\n白线：$10^{-4}$ 与 $10^{-3}$", fontsize=10)

    fig.suptitle("环 8：$f$ 的斜率由 DM.4 的 $\\kappa_f$ 定出，三次项在物理精度内不可见（无拟合）",
                 fontsize=12.5, y=1.03)
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150, bbox_inches="tight")
    print(f"\nsaved {OUT_PNG}")

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["section", "x1", "x2", "x3", "x4"])
        for r_ in rows:
            w.writerow(r_)
    print(f"saved {OUT_CSV}  ({len(rows)} rows)")

    # ---------- assertions ----------
    # (8A.1) must be an identity to machine precision
    for eps in np.linspace(0, TWO_PI * 0.99, 50):
        k = kappa_f(eps)
        assert abs(4 * math.pi * k * (1 - eps / TWO_PI) - 1) < 1e-12
    # slope identity: d lambda / d ell at ell=0 is -1/(4 pi)
    h = 1e-9
    num = (lam(h) - lam(0.0)) / h
    assert abs(num + 1 / (4 * math.pi)) < 1e-7, num
    print("all structural assertions passed")


if __name__ == "__main__":
    main()
