# -*- coding: utf-8 -*-
"""
Review: can Pb two-band structure explain the single-band gap-ratio deviation?
Experiment (Ruby et al. PRL114 157001 2015, arXiv:1409.6638):
  Pb two gaps separated by 150 ueV ~ 10%; Tc=7.2K, coherence 83nm.
  pairing-energy difference ~10% (exp) vs ~30% (SCDFT Floris PRB75 054508).
CQM 12.A: operator mode set n in {2,4,6,...}, {2} first band, n=4 higher mode,
  weight Phi_n/Phi_2 = 2/n (12.A3); multi-band = superposition of modes.
Model: effective tunneling gap ratio = weighted average of two band ratios.
  Single-band Mitrovic gives 2Delta/kTc = 4.198 for Pb; experiment 4.29 (dev -2.1%).
  If band 2 (pp-dd, larger gap) has ratio r2 and band 1 (ss-pp) r1, with weight w,
  the observed tunneling ratio is w*r1+(1-w)*r2 (interband scattering mixes).
This is a MATERIAL-side explanation of the deviation, NOT a CQM derivation.
No fitting: we scan the experimental 10% gap splitting and published weight range.
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
OUT_PNG = os.path.join(HERE, "审_双带Pb与gap比偏差.png")
OUT_CSV = os.path.join(HERE, "审_双带Pb与gap比偏差.csv")

EXP_RATIO = 4.29          # Pb experimental gap ratio (Webb/literature)
SINGLE_BAND = 4.198       # round-58 single-band Mitrovic for Pb
D_GAP = 0.10              # experimental pairing-energy difference ~10%

def main():
    rows = []
    # Two-band model: r2 = r1*(1+D), observed = w*r1 + (1-w)*r2
    # Calibrate so that single-band prediction is the w=1 limit baseline.
    # If w=1 (pure band1), ratio=r1; to match single-band 4.198 set r1=4.198.
    r1 = SINGLE_BAND
    print("Two-band superposition scan for Pb (experiment ratio=4.29, single-band=4.198):")
    print(f"D gap = {D_GAP:.0%} (Ruby 2015) -> r2 = r1*(1+D) = {r1*(1+D_GAP):.3f}")
    ws = np.linspace(0, 1, 100)  # weight on band1 (ss-pp, smaller gap)
    print(f"{'w1':>6}{'ratio_2band':>13}{'dev%':>8}")
    for w in (1.0, 0.8, 0.65, 0.5):
        r2 = r1 * (1 + D_GAP)
        robs = w * r1 + (1 - w) * r2
        dev = (robs - EXP_RATIO) / EXP_RATIO
        print(f"{w:>6.2f}{robs:>13.3f}{dev:>+8.1%}")
    for w in ws:
        r2 = r1 * (1 + D_GAP)
        robs = w * r1 + (1 - w) * r2
        dev = (robs - EXP_RATIO) / EXP_RATIO
        rows.append(("two_band", w, robs, dev, ""))

    # CQM 12.A3 weight: Phi_n/Phi_2 = 2/n. For n=4 vs n=2: 2/4 = 0.5
    w_cqm = 2 / 4  # relative weight of n=4 band to n=2 band
    # normalized: w1 (n=2) : w2 (n=4) = 1 : 0.5 -> w1 = 1/1.5
    w1_cqm = 1 / (1 + w_cqm)
    r2 = r1 * (1 + D_GAP)
    robs_cqm = w1_cqm * r1 + (1 - w1_cqm) * r2
    print(f"\nCQM 12.A3 weight Phi_4/Phi_2 = 2/4 = 0.5 -> w1={w1_cqm:.3f}")
    print(f"  two-band ratio = {robs_cqm:.3f}, dev vs exp = {(robs_cqm-EXP_RATIO)/EXP_RATIO:+.1%}")
    rows.append(("cqm_weight", w1_cqm, robs_cqm, (robs_cqm-EXP_RATIO)/EXP_RATIO, "12.A3"))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "w1", "ratio", "dev", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(figsize=(8, 5.4))
    ratios = [w * r1 + (1 - w) * r1 * (1 + D_GAP) for w in ws]
    ax.plot(ws, ratios, lw=2.4, color="tab:blue", label="two-band superposition")
    ax.axhline(EXP_RATIO, color="red", ls="--", lw=1.5, label="experiment 4.29")
    ax.axhline(SINGLE_BAND, color="gray", ls=":", lw=1.5, label="single-band 4.198")
    ax.axvline(w1_cqm, color="green", ls="-.", lw=1.5, label=f"CQM 12.A3 w1={w1_cqm:.2f}")
    ax.set_xlabel(r"weight on band 1 ($w_1$)")
    ax.set_ylabel("effective gap ratio")
    ax.set_title("Two-band effect on Pb gap ratio (material-side explanation)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)
    print("NOTE: material-side explanation of deviation, NOT a CQM derivation.")
    print("      interband scattering (Ruby 2015) reduces splitting -> w in between.")


if __name__ == "__main__":
    main()
