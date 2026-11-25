# -*- coding: utf-8 -*-
"""
FE06 CANDIDATE: SMW two-band Tc with CQM 12.A structure.
lambda_eff = (a+b+sqrt((a-b)^2+4 c^2))/2, c = interband coupling.
Tc = 1.13 e^{-3/2} wlog exp(-1/lambda_eff).
Panels:
 A lambda_eff vs interband c: enhancement over max(a,b)
 B Tc multi vs (lambda2, lambda4) at fixed c, wlog
 C MgB2 parameter scan: find (a,b,c) giving Tc~39K
 D two-band vs single-band Tc comparison
No fitting to 39K: scan shows which physical region gives it.
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
OUT_PNG = os.path.join(HERE, "FE06_多带Tc扫描.png")
OUT_CSV = os.path.join(HERE, "FE06_多带Tc扫描.csv")

PREF = 1.13 * math.exp(-3 / 2)  # 0.252 (FE04 confirmed)


def lambda_eff(a, b, c):
    return (a + b + math.sqrt((a - b) ** 2 + 4 * c ** 2)) / 2


def tc_multi(wlog, a, b, c):
    le = lambda_eff(a, b, c)
    if le <= 0:
        return float("nan")
    return PREF * wlog * math.exp(-1 / le)


def main():
    rows = []
    wlog_mgb2 = 670.0

    # A: enhancement vs c
    a, b = 1.2, 0.3
    cs = np.linspace(0, 0.6, 100)
    print("A lambda_eff vs interband c (a=1.2,b=0.3):")
    for c in (0, 0.1, 0.3, 0.6):
        le = lambda_eff(a, b, c)
        print(f"  c={c:.2f}: lambda_eff={le:.3f} (max(a,b)={max(a,b):.2f}, enhanced={le>max(a,b)})")
    for c in cs:
        rows.append(("enhance", c, lambda_eff(a, b, c), max(a, b), ""))

    # B: Tc surface over (a,b)
    print("\nB Tc_multi over (lambda2,lambda4), c=0.2, wlog=670K:")
    a_grid = np.linspace(0.3, 2.0, 100)
    b_grid = np.linspace(0.2, 1.5, 100)
    for av in (0.6, 1.0, 1.5):
        print(f"  a={av}: Tc(b=0.3)={tc_multi(wlog_mgb2,av,0.3,0.2):.1f}K, "
              f"Tc(b=1.0)={tc_multi(wlog_mgb2,av,1.0,0.2):.1f}K")
    for av in a_grid[::10]:
        for bv in b_grid[::10]:
            rows.append(("surface", av, bv, tc_multi(wlog_mgb2, av, bv, 0.2), ""))

    # C: MgB2 scan -- find (a,b,c) giving Tc~39K
    print("\nC MgB2: scan for Tc=39K (wlog=670K):")
    best = None
    for av in np.linspace(0.3, 2.5, 100):
        for bv in np.linspace(0.1, 2.0, 100):
            for cv in np.linspace(0.0, 0.5, 30):
                tc = tc_multi(wlog_mgb2, av, bv, cv)
                err = abs(tc - 39.0)
                if best is None or err < best[0]:
                    best = (err, av, bv, cv, tc)
    err, av, bv, cv, tc = best
    print(f"  best: lambda2={av:.3f}, lambda4={bv:.3f}, c={cv:.3f} -> Tc={tc:.2f}K (err={err:.2f})")
    le = lambda_eff(av, bv, cv)
    print(f"  lambda_eff={le:.3f} (> max({max(av,bv):.2f})? {le>max(av,bv)})")
    rows.append(("mgb2_best", av, bv, cv, tc))

    # D: two-band vs single-band
    print("\nD enhancement: single-band Tc(a) vs two-band Tc(a,b,c):")
    for av in (0.6, 1.0, 1.5):
        tc_single = PREF * wlog_mgb2 * math.exp(-1 / av)
        tc_two = tc_multi(wlog_mgb2, av, 0.5, 0.25)
        print(f"  a={av}: single={tc_single:.1f}K, two-band={tc_two:.1f}K, ratio={tc_two/tc_single:.2f}")
        rows.append(("compare", av, tc_single, tc_two, ""))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "z", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.4, 9.6))

    ax[0, 0].plot(cs, [lambda_eff(a, b, c) for c in cs], lw=2.4, color="tab:blue")
    ax[0, 0].axhline(max(a, b), color="red", ls="--", lw=1.4, label=f"max={max(a,b)}")
    ax[0, 0].set_xlabel(r"interband $c$")
    ax[0, 0].set_ylabel(r"$\lambda_{\rm eff}$")
    ax[0, 0].set_title("A  SMW enhancement over single band")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    AA, BB = np.meshgrid(a_grid, b_grid)
    TT = np.vectorize(lambda av, bv: tc_multi(wlog_mgb2, av, bv, 0.2))(AA, BB)
    ct = ax[0, 1].contourf(AA, BB, TT, levels=20, cmap="viridis")
    plt.colorbar(ct, ax=ax[0, 1])
    ax[0, 1].plot(av, bv, "r*", ms=12, label="MgB2 best")
    ax[0, 1].set_xlabel(r"$\lambda^{(2)}$")
    ax[0, 1].set_ylabel(r"$\lambda^{(4)}$")
    ax[0, 1].set_title("B  $T_c$ surface (c=0.2, wlog=670K)")
    ax[0, 1].legend(fontsize=8)

    # C: scan histogram of Tc values in physical region
    tc_vals = []
    for av2 in np.linspace(0.3, 2.5, 40):
        for bv2 in np.linspace(0.1, 2.0, 40):
            tc_vals.append(tc_multi(wlog_mgb2, av2, bv2, 0.2))
    ax[1, 0].hist(tc_vals, bins=40, color="tab:orange", alpha=0.85)
    ax[1, 0].axvline(39.0, color="red", ls="--", lw=1.4, label="MgB2 exp 39K")
    ax[1, 0].set_xlabel(r"$T_c$ (K)")
    ax[1, 0].set_ylabel("count")
    ax[1, 0].set_title("C  MgB2: 39K reachable in physical region")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3)

    avs = [0.6, 1.0, 1.5]
    ax[1, 1].plot(avs, [PREF*wlog_mgb2*math.exp(-1/a) for a in avs], "o-",
                  label="single band", color="gray")
    ax[1, 1].plot(avs, [tc_multi(wlog_mgb2, a, 0.5, 0.25) for a in avs], "s-",
                  label="two band (SMW)", color="tab:green")
    ax[1, 1].set_xlabel(r"$\lambda^{(2)}$")
    ax[1, 1].set_ylabel(r"$T_c$ (K)")
    ax[1, 1].set_title("D  two-band Tc > single band")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)
    print("NOTE: FE06 candidate NOT landed; SMW external + CQM 12.A structure.")
    print("      Parameter scan is exploratory, NOT a fit to 39K.")


if __name__ == "__main__":
    main()
