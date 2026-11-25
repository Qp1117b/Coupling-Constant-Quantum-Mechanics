# -*- coding: utf-8 -*-
"""
FE04 CANDIDATE: confirm CQM prefactor = literature e^{-3/2} (Chubukov PRB2020, Marsiglio Eq37).
Checks (no fitting):
  1.13*e^{-1/6}*e^{-1/3} = 1.13*e^{-1/2} = 1.13/sqrt(e)  (log-moment conversion)
  1.13*e^{-3/2} = 0.252  (Chubukov Eq III.29)
  CQM展开 chain: 1.13 e^{-1/6}(e^{-1/3}theta) e^{-(1+lam)/lam}
                = 1.13 e^{-3/2} theta e^{-1/lam}
External: Chubukov arXiv:1910.04579; Marsiglio arXiv:1807.04907.
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
OUT_PNG = os.path.join(HERE, "FE04_前因子核对.png")
OUT_CSV = os.path.join(HERE, "FE04_前因子核对.csv")


def main():
    rows = []
    # Step 1: log-moment conversion
    e16, e13, e12 = math.exp(-1/6), math.exp(-1/3), math.exp(-1/2)
    lhs, rhs = e16 * e13, e12
    print("1) log-moment conversion: e^{-1/6}*e^{-1/3} = e^{-1/2}")
    print(f"   lhs={lhs:.10f}  rhs={rhs:.10f}  diff={abs(lhs-rhs):.2e}")
    rows.append(("conv", e16, e13, lhs, rhs))

    # Step 2: prefactor = 1.13/sqrt(e)
    p_log = 1.13 * e12
    p_marsiglio = 1.13 / math.sqrt(math.e)
    print("\n2) prefactor: 1.13*e^{-1/2} = 1.13/sqrt(e)")
    print(f"   CQM={p_log:.10f}  Marsiglio={p_marsiglio:.10f}  diff={abs(p_log-p_marsiglio):.2e}")

    # Step 3: total e^{-3/2} and 0.252
    p_total = 1.13 * math.exp(-3/2)
    print("\n3) total: 1.13*e^{-3/2} = 0.252 (Chubukov III.29)")
    print(f"   1.13*e^{{-3/2}}={p_total:.10f}  literature 0.252  diff={abs(p_total-0.252):.4f}")
    rows.append(("total", e12, math.exp(-1), p_total, 0.252))

    # Step 4: full chain identity over lambda
    print("\n4) full chain: CQM展开 = literature (theta=200K)")
    theta = 200.0
    lams = np.linspace(0.1, 0.8, 200)
    maxdiff = 0.0
    for lam in lams:
        cqm = 1.13 * e16 * (e13 * theta) * math.exp(-(1+lam)/lam)
        lit = 1.13 * math.exp(-3/2) * theta * math.exp(-1/lam)
        maxdiff = max(maxdiff, abs(cqm - lit))
        rows.append(("chain", lam, cqm, lit, abs(cqm-lit)))
    print(f"   max|CQM-literature| over lambda in [0.1,0.8] = {maxdiff:.2e} K")

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y2", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(1, 2, figsize=(12.5, 5.0))

    # left: prefactor comparison bars
    labels = ["$1.13e^{-1/2}$\n(CQM)", "$1.13/\\sqrt{e}$\n(Marsiglio)", "$1.13e^{-3/2}$\n(Chubukov)", "0.252"]
    vals = [p_log, p_marsiglio, p_total, 0.252]
    # normalize first two (they are the e^{-1/2} level) and last two (e^{-3/2} level)
    ax[0].bar(labels[:2], vals[:2], color="tab:blue", alpha=0.85)
    ax[0].set_ylabel("prefactor value")
    ax[0].set_title(r"Stage 1: $e^{-1/2}$ level (identical)")
    ax[0].grid(alpha=0.3, axis="y")

    ax2 = ax[1]
    ax2.bar(["$1.13e^{-3/2}$", "0.252"], [p_total, 0.252], color="tab:green", alpha=0.85)
    ax2.set_ylabel("prefactor value")
    ax2.set_title(r"Stage 2: $e^{-3/2}$ level (=0.252)")
    ax2.grid(alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)
    print("NOTE: confirms CQM构造式 matches independent first-principles literature")
    print("      (Chubukov PRB2020 EqIII.29 + Marsiglio Eq37); NOT a CQM first-principles proof.")


if __name__ == "__main__":
    main()
