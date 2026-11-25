# -*- coding: utf-8 -*-
"""
END-TO-END JUDGEMENT with INDEPENDENT parameters (first time in 70 rounds).
For the first time we have (lambda, mu*, omega_log) that are NOT back-solved
from Tc -- they are ab-initio inputs from published papers:
  MgB2  (Choi et al. PRB66 020513 2002, arXiv:cond-mat/0111182):
        lambda=0.61, mu*=0.12, Tc=39 K, alpha_B=0.31.
        NOTE: Tc=39 needs TWO-GAP / anisotropic Eliashberg; single-gap AD gives ~17K.
  Mo2NF2 (Seyyangnok et al. 2026, arXiv:2603.06284):
        CDW: lambda=0.40, wlog=219K, Tc~1K; strain: lambda=0.53, wlog=272K, Tc~4K.
  BP3   (Seyyangnok et al. 2026, arXiv:2604.10026):
        lambda=1.59, Tc=9.7K (need wlog, not given -> skip AD, use as bound).

Test: CQM candidate Tc (FE03 structure: 1.13 e^{-3/2} wlog/1.2? -> see formula)
   Allen-Dynes: Tc = wlog/1.2 * exp[-1.04(1+lam)/(lam - mustar(1+0.62 lam))]
   Using omega_log with the CORRECT Eliashberg moment (FE03 conclusion).
Compare Tc_AD to literature Tc. This is a PREDICTION test (params independent).
No fitting.

IMPORTANT honesty: MgB2 is anisotropic/two-gap; single-gap AD underestimates.
This itself is a result: shows CQM single-band candidate cannot capture two-gap systems.
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
OUT_PNG = os.path.join(HERE, "端到端_独立参数Tc判定.png")
OUT_CSV = os.path.join(HERE, "端到端_独立参数Tc判定.csv")


def tc_ad(wlog, lam, mustar):
    den = lam - mustar * (1 + 0.62 * lam)
    if den <= 0:
        return float("nan")
    return wlog / 1.2 * math.exp(-1.04 * (1 + lam) / den)


def main():
    rows = []
    # Independent parameter sets from literature
    # (name, lambda, mu*, omega_log K (None if not given), Tc_lit K, two_gap flag, source)
    DATA = [
        ("Mo2NF2-CDW", 0.40, 0.10, 219.0, 1.0, False, "arXiv:2603.06284"),
        ("Mo2NF2-str", 0.53, 0.10, 272.0, 4.0, False, "arXiv:2603.06284"),
        ("MgB2",       0.61, 0.12, None, 39.0, True,  "arXiv:cond-mat/0111182"),
    ]
    print("END-TO-END Tc judgement with INDEPENDENT ab-initio parameters")
    print("(lambda, mu*, omega_log NOT back-solved from Tc)")
    print(f"{'system':<14}{'lam':>6}{'mu*':>6}{'wlog':>7}{'Tc_AD':>8}{'Tc_lit':>8}{'ratio':>8}")
    for name, lam, ms, wlog, tc_lit, two_gap, src in DATA:
        if wlog is None:
            # For MgB2, omega_log not in abstract; use known literature value ~ 670K (phonon ~ 100meV)
            # Mark as external assumption, clearly flagged.
            wlog = 670.0
            print(f"  [NOTE] {name}: omega_log not in abstract; using lit ~670K (FLAGGED external)")
        tc = tc_ad(wlog, lam, ms)
        ratio = tc / tc_lit if tc_lit else float("nan")
        print(f"{name:<14}{lam:>6.2f}{ms:>6.2f}{wlog:>7.0f}{tc:>8.2f}{tc_lit:>8.2f}{ratio:>8.2f}")
        rows.append((name, lam, ms, wlog, tc, tc_lit, ratio, two_gap, src))

    # Mo2NF2 with mu* uncertainty scan (mu* not given in abstract for these)
    print("\nMo2NF2 mu* sensitivity (lambda=0.40, wlog=219K):")
    print(f"{'mu*':>6}{'Tc_AD':>8}{'Tc_lit=1K':>10}")
    for ms in (0.05, 0.10, 0.15, 0.20):
        tc = tc_ad(219.0, 0.40, ms)
        print(f"{ms:>6.2f}{tc:>8.3f}{'':>10}")
        rows.append(("Mo2NF2_mu_scan", 0.40, ms, 219.0, tc, 1.0, tc/1.0, False, ""))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["system", "lambda", "mustar", "wlog", "Tc_AD", "Tc_lit", "ratio", "two_gap", "source"])
        wr.writerows(rows)

    # Figure: Tc_AD vs Tc_lit for systems (log scale)
    fig, ax = plt.subplots(1, 2, figsize=(13, 5.4))
    single = [r for r in rows if isinstance(r[0], str) and r[0] in
              ("Mo2NF2-CDW", "Mo2NF2-str", "MgB2")]
    names = [r[0] for r in single]
    tc_ads = [r[4] for r in single]
    tc_lits = [r[5] for r in single]
    x = np.arange(len(names))
    ax[0].bar(x - 0.18, tc_ads, 0.36, label="Tc_AD (CQM candidate)", color="tab:blue", alpha=0.85)
    ax[0].bar(x + 0.18, tc_lits, 0.36, label="Tc_lit (independent)", color="tab:orange", alpha=0.85)
    ax[0].set_xticks(x)
    ax[0].set_xticklabels(names, fontsize=9)
    ax[0].set_ylabel("Tc (K)")
    ax[0].set_title("End-to-end: CQM candidate vs literature")
    ax[0].legend(fontsize=8)
    ax[0].grid(alpha=0.3, axis="y")

    ms_scan = [0.05, 0.10, 0.15, 0.20]
    tc_scan = [tc_ad(219.0, 0.40, m) for m in ms_scan]
    ax[1].plot(ms_scan, tc_scan, "o-", lw=2.2, color="tab:purple")
    ax[1].axhline(1.0, color="red", ls="--", lw=1.4, label="Tc_lit ~ 1K")
    ax[1].set_xlabel(r"$\mu^*$")
    ax[1].set_ylabel("Tc_AD (K)")
    ax[1].set_title("Mo2NF2: mu* sensitivity (not given in abstract)")
    ax[1].legend(fontsize=8)
    ax[1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)
    print("NOTE: MgB2 two-gap -> single-gap AD underestimates (expected);")
    print("      Mo2NF2 wlog from abstract; mu* scanned (not given).")
    print("      This is a PREDICTION test with independent params, NOT back-substitution.")


if __name__ == "__main__":
    main()
