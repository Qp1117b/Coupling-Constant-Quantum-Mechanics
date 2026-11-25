# -*- coding: utf-8 -*-
"""
FE07 method self-check: reproduce Mo2NF2 literature Tc with EXACT paper parameters
and EXACT Allen-Dynes Eq(1). The paper (arXiv:2603.06284) gives:
  CDW:  lambda=0.40, omega_log=219K -> Tc~1K
  strain: lambda=0.53, omega_log=272K -> Tc~4K
Paper does not state mu* explicitly; AD standard mu*=0.10 implied.
Scan mu* to find which value reproduces paper Tc -> establishes implied mu*.
Also confirms paper omega_log definition = alpha^2F/omega weight (round-62 conclusion).
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
OUT_PNG = os.path.join(HERE, "FE07_文献方法自检.png")
OUT_CSV = os.path.join(HERE, "FE07_文献方法自检.csv")

def tc_ad(wlog, lam, mustar):
    den = lam - mustar * (1 + 0.62 * lam)
    return wlog / 1.2 * math.exp(-1.04 * (1 + lam) / den) if den > 0 else float("nan")

def implied_mu(tc_target, wlog, lam):
    # solve tc_ad = tc_target for mu* by bisection
    lo, hi = 0.0, 0.3
    f = lambda m: tc_ad(wlog, lam, m) - tc_target
    if f(lo) * f(hi) > 0:
        return None
    for _ in range(100):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2

def main():
    rows = []
    print("FE07 method self-check: reproduce Mo2NF2 (arXiv:2603.06284) Tc")
    print("Paper: CDW lambda=0.40 wlog=219 -> Tc~1K; strain lambda=0.53 wlog=272 -> Tc~4K")
    print("Paper uses Allen-Dynes Eq(1); mu* not stated -> find implied mu*.\n")
    systems = [("CDW", 0.40, 219, 1.0), ("strain", 0.53, 272, 4.0)]
    for name, lam, wlog, tc_lit in systems:
        mu_imp = implied_mu(tc_lit, wlog, lam)
        tc_at010 = tc_ad(wlog, lam, 0.10)
        print(f"{name}: mu*_implied={mu_imp:.4f}; Tc(mu*=0.10)={tc_at010:.3f}K vs paper {tc_lit}K")
        rows.append((name, lam, wlog, tc_lit, tc_at010, mu_imp))
        for m in np.linspace(0.05, 0.2, 50):
            rows.append((name+"_scan", lam, wlog, m, tc_ad(wlog, lam, m), tc_lit))
    print("\n=> if implied mu* ~ 0.10, paper used standard value; our reproduction is faithful,")
    print("   but NOT an independent prediction (mu* not independently given). Confirms L2 classification.")
    print("\n=> Paper Eq(3): omega_ln=exp[(2/lam)int(alpha2F/omega)ln(omega)] --")
    print("   this is the alpha^2F/omega weight (round-62 'e^{-1/2} moment'), independently confirming")
    print("   that Eliashberg omega_ln != CQM 3y^2 DOS moment.")

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["system", "lambda", "omega_log", "mu_or_target", "Tc", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(figsize=(9, 5.6))
    for name, lam, wlog, tc_lit in systems:
        ms = np.linspace(0.05, 0.2, 100)
        ax.plot(ms, [tc_ad(wlog, lam, m) for m in ms], lw=2.2, label=f"{name} (lam={lam})")
        ax.axhline(tc_lit, ls=":", lw=1, color="gray")
    ax.set_xlabel(r"$\mu^*$")
    ax.set_ylabel(r"$T_c$ (K)")
    ax.set_title("FE07: implied mu* to reproduce paper Tc (not independent)")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG, OUT_CSV)

if __name__ == "__main__":
    main()
