# -*- coding: utf-8 -*-
"""
Recompute gap ratio using the CORRECT Eliashberg log-moment.
Round 58 used omega_ln = e^{-1/3} theta_D (CQM 3y^2 electronic-DOS moment).
Webb 2015 Eq3 defines omega_ln with weight alpha^2F/nu; for a Debye phonon
spectrum alpha^2F ~ nu^2 this gives weight 2y and omega_ln = e^{-1/2} theta_D.

Compare BOTH choices against experimental gap ratios (Webb/standard values):
  Mitrovic (Webb Eq6): 2Delta0/kBTc = 3.53[1+12.5 (Tc/wln)^2 ln(wln/2Tc)]
No fitting; input Tc, theta_D are measured; only the moment definition changes.
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
OUT_PNG = os.path.join(HERE, "审_Eliashberg矩重算gap比.png")
OUT_CSV = os.path.join(HERE, "审_Eliashberg矩重算gap比.csv")

E13 = math.exp(-1 / 3)
E12 = math.exp(-1 / 2)
BCS = 3.53

# name, Tc(K), theta_D(K), experimental gap ratio (standard literature values)
DATA = [
    ("Al", 1.18, 428, 3.44),
    ("Sn", 3.70, 200, 3.51),
    ("Pb", 7.20, 105, 4.29),
    ("Nb", 9.25, 275, 3.80),
    ("V",  5.40, 380, 3.60),
    ("Cd", 0.52, 209, 3.37),
    ("Ta", 4.40, 240, 3.65),
    ("In", 3.40, 108, 3.50),
]


def mitrovic(tc, wln):
    x = tc / wln
    if x >= 0.5:
        return float("nan")
    return BCS * (1 + 12.5 * x * x * math.log(1 / (2 * x)))


def main():
    rows = []
    print("Gap ratio with two log-moment definitions (Mitrovic Webb Eq6):")
    print(f"{'el':<4}{'exp':>7}{'CQM e^-1/3':>12}{'err%':>8}{'Eliash e^-1/2':>15}{'err%':>8}")
    err_cqm, err_el = [], []
    for name, tc, th, gexp in DATA:
        g_cqm = mitrovic(tc, E13 * th)
        g_el = mitrovic(tc, E12 * th)
        e_cqm = (g_cqm - gexp) / gexp
        e_el = (g_el - gexp) / gexp
        err_cqm.append(e_cqm)
        err_el.append(e_el)
        print(f"{name:<4}{gexp:>7.2f}{g_cqm:>12.3f}{e_cqm:>+8.1%}{g_el:>15.3f}{e_el:>+8.1%}")
        rows.append((name, gexp, g_cqm, g_el, e_cqm, e_el))
    m_cqm = np.mean(np.abs(err_cqm))
    m_el = np.mean(np.abs(err_el))
    print(f"\nmean |err| CQM e^-1/3 : {m_cqm:.1%}")
    print(f"mean |err| Eliash e^-1/2: {m_el:.1%}")

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["el", "gap_exp", "gap_CQM_e13", "gap_Eliash_e12",
                     "err_CQM", "err_Eliash"])
        wr.writerows(rows)

    names = [r[0] for r in rows]
    gexp = np.array([r[1] for r in rows])
    gcqm = np.array([r[2] for r in rows])
    gel = np.array([r[3] for r in rows])
    x = np.arange(len(names))

    fig, ax = plt.subplots(1, 2, figsize=(13.4, 5.4))
    ax[0].bar(x - 0.25, gexp, 0.25, label="experiment", color="gray", alpha=0.8)
    ax[0].bar(x, gcqm, 0.25, label="CQM moment $e^{-1/3}$", color="tab:blue", alpha=0.85)
    ax[0].bar(x + 0.25, gel, 0.25, label="Eliashberg moment $e^{-1/2}$", color="tab:red", alpha=0.85)
    ax[0].set_xticks(x)
    ax[0].set_xticklabels(names)
    ax[0].set_ylabel("gap ratio")
    ax[0].set_title(f"Two moments: mean |err| {m_cqm:.1%} vs {m_el:.1%}")
    ax[0].legend(fontsize=8)
    ax[0].grid(alpha=0.3, axis="y")

    ax[1].plot(x, err_cqm, "o-", label="CQM $e^{-1/3}$", color="tab:blue", lw=2)
    ax[1].plot(x, err_el, "s-", label="Eliashberg $e^{-1/2}$", color="tab:red", lw=2)
    ax[1].axhline(0, color="k", lw=1)
    ax[1].set_xticks(x)
    ax[1].set_xticklabels(names)
    ax[1].set_ylabel("relative error")
    ax[1].set_title("Moment definition matters for gap ratio")
    ax[1].legend(fontsize=8)
    ax[1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)
    print("NOTE: both are external Mitrovic formula; only the moment definition differs.")
    print("      This is a consistency check of WHICH moment to feed in, not a CQM derivation.")


if __name__ == "__main__":
    main()
