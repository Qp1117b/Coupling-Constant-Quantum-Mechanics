# -*- coding: utf-8 -*-
"""
Isotope exponent intermediate value via chain-external mu* shape (M.1).

T10.3 (round-10 card) proved CQM endpoints alpha in {0,1/2} and said
"0<alpha<1/2 needs an EXTERNAL component (mu*)". Round 60 shaped mu*.
This script connects that external component:

  alpha = 1/2 [1 - 1.04(1+lam)(1+0.62 lam) mu*^2 / (lam - mu*(1+0.62 lam))^2]

derived from: omega_log ~ M^{-1/2}, dL/dlnM=+1/2 (L=ln(eps_F/hbar w_D)),
d mu*/dL = -(mu*)^2  (M.1 shape), Allen-Dynes Eq2.

NO fitting: panel C solves (lam, mu*) from TWO independent measurements
(Tc and alpha) using CQM omega_log=e^{-1/3} theta_D; panel D back-substitutes
to verify both are reproduced. External source: Webb 2015 Table III.

⚠ 口径已修正（第94轮 R-103，防干扰注记）：本脚本用 e^{-1/3}θ_D（CQM 振幅支
3y² 矩）代入 Allen–Dynes 式，但该式 ω_ln 按定义是 α²F/ν 权重 = e^{-1/2}θ_D
（第92轮链内导出）。两矩比 e^{1/6}。权威复跑请用
`环10_审14_双观测omega口径修正.py`（新口径 e^{-1/2}）。本脚本保留作历史
记录、不删除、可追溯；新口径下 13/13 可解、常规 μ* 区间同为 8/13（稳健性
检验，旧结论未被推翻）。
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
OUT_PNG = os.path.join(HERE, "环10_同位素中间值双观测.png")
OUT_CSV = os.path.join(HERE, "环10_同位素中间值双观测.csv")
E3 = math.exp(-1 / 3)

# Webb 2015 Table III: name, Tc(K), theta_D(K), alpha_exp (measured column)
# elements with a measured alpha value (blank-alpha entries omitted)
DATA = [
    ("Pb", 7.20, 105, 0.48),
    ("Hg", 4.15, 72, 0.50),
    ("Sn", 3.70, 200, 0.46),
    ("Tl", 2.40, 78.5, 0.50),
    ("V",  5.40, 380, 0.15),
    ("Ta", 4.40, 240, 0.35),
    ("Re", 1.70, 430, 0.38),
    ("Mo", 0.92, 450, 0.37),
    ("Os", 0.70, 500, 0.21),
    ("Zn", 0.85, 327, 0.30),
    ("Cd", 0.52, 209, 0.50),
    ("Zr", 0.60, 291, 0.00),
    ("Ru", 0.50, 600, 0.00),
]


def alpha_of(lam, must):
    """alpha from CQM-shaped mu* (external component)."""
    b = 1 + 0.62 * lam
    D = lam - must * b
    if D <= 0:
        return float("nan")
    C = 1.04 * (1 + lam) * b * must**2 / D**2
    if C >= 1:
        return float("nan")  # alpha<0 anomalous, out of scope
    return 0.5 * (1 - C)


def tc_ad(wlog, lam, must):
    b = 1 + 0.62 * lam
    D = lam - must * b
    if D <= 0:
        return float("nan")
    return wlog / 1.2 * math.exp(-1.04 * (1 + lam) / D)


def solve_double(tc, theta, a_exp):
    """Solve (lam,must) from BOTH Tc and alpha, with CQM omega_log.
    E = ln(1.2 Tc / wlog) < 0;  D = -1.04(1+lam)/E must equal lam-must*b.
    From alpha equation after eliminating D:
      b*must^2*E^2/(1.04*(1+lam)) = 1 - 2 a_exp,  must=(lam + 1.04(1+lam)/E)/b.
    Bisection on lam.
    """
    wlog = E3 * theta
    E = math.log(1.2 * tc / wlog)
    if E >= 0:
        return None
    A = -1.04 / E  # D = A*(1+lam)
    if A >= 1:
        return None

    def f(lam):
        b = 1 + 0.62 * lam
        must = (lam - A * (1 + lam)) / b
        if must < -1e-9 or must > 1:
            return float("nan")
        pred = b * must**2 * E**2 / (1.04 * (1 + lam))
        return pred - (1 - 2 * a_exp)

    lo = A / (1 - A)  # must=0 boundary (alpha=1/2 endpoint lives here)
    # upper bound where must hits 1: lam(0.38 - A) = 1 + A  (A<0.38)
    if A < 0.38:
        hi = min(20.0, (1 + A) / (0.38 - A) * 0.9999)
    else:
        hi = 20.0
    if hi <= lo:
        return None
    if abs(1 - 2 * a_exp) < 1e-9:  # alpha=1/2 endpoint => mu*=0 exactly
        return lo, 0.0, wlog
    flo = f(lo)
    fhi = f(hi)
    if not (np.isfinite(flo) and np.isfinite(fhi)) or flo * fhi > 0:
        return None
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if not np.isfinite(fm):
            hi = mid
            continue
        if flo * fm <= 0:
            hi = mid
            fhi = fm
        else:
            lo = mid
            flo = fm
    lam = 0.5 * (lo + hi)
    b = 1 + 0.62 * lam
    must = (lam - A * (1 + lam)) / b
    if must < -1e-6 or must > 1 + 1e-6:
        return None
    must = max(0.0, must)  # clip round-off at mu*=0 endpoint
    return lam, must, wlog


def main():
    rows = []

    # Panel A: alpha vs mu* for several lambda
    print("A alpha vs mu* (alpha<1/2 for mu*>0)")
    mus = np.linspace(0, 0.3, 200)
    for lam in (0.5, 1.0, 1.5):
        vals = [alpha_of(lam, m) for m in mus]
        print(f"  lam={lam}: alpha(0)=0.5, alpha(0.1)={alpha_of(lam,0.1):.4f}, "
              f"alpha(0.2)={alpha_of(lam,0.2):.4f}")
        for m, v in zip(mus[::40], vals[::40]):
            rows.append(("alpha_curve", lam, m, v, ""))

    # Panel C: double-observation solve
    print("\nC double-observation solve (Tc & alpha -> lam,must)")
    print(f"{'el':<4}{'Tc':>6}{'alpha':>7}{'wlog':>8}{'lam':>8}{'mu*':>8}"
          f"{'Tc_fit':>8}{'a_fit':>8}{'in[.1,.3]':>10}")
    sols = []
    for name, tc, theta, a_exp in DATA:
        sol = solve_double(tc, theta, a_exp)
        if sol is None:
            print(f"{name:<4}{tc:>6.2f}{a_exp:>7.2f}{'---':>8}{'no solve':>16}")
            continue
        lam, must, wlog = sol
        tc_fit = tc_ad(wlog, lam, must)
        a_fit = alpha_of(lam, must)
        inrange = 0.10 <= must <= 0.30
        sols.append((name, must, inrange, lam, tc, a_exp, tc_fit, a_fit))
        print(f"{name:<4}{tc:>6.2f}{a_exp:>7.2f}{wlog:>8.1f}{lam:>8.3f}{must:>8.3f}"
              f"{tc_fit:>8.3f}{a_fit:>8.3f}{str(inrange):>10}")
        rows.append(("solve", tc, a_exp, must, f"{name}|lam={lam:.4f}|inrange={inrange}"))
        rows.append(("backTc", tc, tc_exp if False else tc, tc_fit, name))
        rows.append(("backA", a_exp, a_exp, a_fit, name))

    if sols:
        infr = sum(1 for s in sols if s[2])
        print(f"\n  mu* in [0.10,0.30]: {infr}/{len(sols)} of double-observation solutions")

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "p1", "p2", "y", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.4, 9.6))

    for lam in (0.5, 1.0, 1.5):
        ax[0, 0].plot(mus, [alpha_of(lam, m) for m in mus], lw=2.2, label=f"lambda={lam}")
    ax[0, 0].axhline(0.5, color="k", ls="--", lw=1.2, label="CQM endpoint 1/2")
    ax[0, 0].set_xlabel(r"$\mu^*$ (chain-external shape)")
    ax[0, 0].set_ylabel(r"$\alpha$")
    ax[0, 0].set_title(r"A  $\alpha<1/2$ from $\mu^*$ competition")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    # Panel B: alpha(lam,mu*) contour
    lamg = np.linspace(0.3, 2.0, 120)
    mug = np.linspace(0.0, 0.3, 120)
    LL, MM = np.meshgrid(lamg, mug)
    AA = np.vectorize(alpha_of)(LL, MM)
    ct = ax[0, 1].contourf(LL, MM, AA, levels=20, cmap="viridis")
    plt.colorbar(ct, ax=ax[0, 1])
    for name, tc, theta, a_exp in DATA:
        for s in sols:
            if s[0] == name:
                ax[0, 1].plot(s[3], s[1], "r*", ms=9)
                ax[0, 1].annotate(name, (s[3], s[1]), fontsize=7, color="white")
    ax[0, 1].set_xlabel(r"$\lambda$")
    ax[0, 1].set_ylabel(r"$\mu^*$")
    ax[0, 1].set_title(r"B  $\alpha(\lambda,\mu^*)$ + double-observation solutions")
    ax[0, 1].grid(alpha=0.2)

    # Panel C: solved mu* per element
    names = [s[0] for s in sols]
    musts = [s[1] for s in sols]
    colors = ["tab:green" if s[2] else "tab:red" for s in sols]
    ax[1, 0].bar(names, musts, color=colors, alpha=0.85)
    ax[1, 0].axhspan(0.10, 0.30, color="gray", alpha=0.2, label="canonical mu* 0.1-0.3")
    ax[1, 0].set_ylabel(r"solved $\mu^*$")
    ax[1, 0].set_title(r"C  $\mu^*$ solved from ($T_c,\alpha$)")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3, axis="y")

    # Panel D: back-substitution check alpha_fit vs alpha_exp
    a_exps = [s[5] for s in sols]
    a_fits = [s[7] for s in sols]
    ax[1, 1].plot(a_exps, a_fits, "o", color="tab:blue", ms=7)
    ax[1, 1].plot([0, 0.55], [0, 0.55], "k--", lw=1.2, label="exact")
    ax[1, 1].set_xlabel(r"$\alpha^{exp}$ (Webb Table III)")
    ax[1, 1].set_ylabel(r"$\alpha^{fit}$ (back-substitution)")
    ax[1, 1].set_title("D  double-observation self-consistency")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)
    print("NOTE: mu* is CHAIN-EXTERNAL (T10.3); this connects the external component,")
    print("      not a pure CQM derivation. No fitting: (lam,mu*) from 2 measurements.")


if __name__ == "__main__":
    main()
