# -*- coding: utf-8 -*-
"""
FE07: UNIFIED verification judgement across all 71 rounds.
Classify each result into a verification LEVEL to prevent mistaking
explanation/back-substitution for genuine prediction:
  L1 genuine independent prediction (params fully independent, formula fixed)
  L2 semi-independent (some parameter assumed)
  L3 self-consistent back-substitution (params solved from target; not validation)
  L4 post-hoc explanation (explains known deviation, not prediction)
Output: unified table + figure. No fitting.
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
OUT_PNG = os.path.join(HERE, "FE07_统一验证判定.png")
OUT_CSV = os.path.join(HERE, "FE07_统一验证判定.csv")
PREF = 1.13 * math.exp(-3 / 2)  # 0.252

def tc_ad(wlog, lam, mustar):
    den = lam - mustar * (1 + 0.62 * lam)
    return wlog / 1.2 * math.exp(-1.04 * (1 + lam) / den) if den > 0 else float("nan")

def lambda_eff(a, b, c):
    return (a + b + math.sqrt((a - b) ** 2 + 4 * c * c)) / 2

def main():
    rows = []
    # Each: (system, observable, level, predicted, experimental, note)
    # L2 semi-independent: Mo2NF2 (mu* assumed)
    pred_cdw = tc_ad(219, 0.40, 0.10)
    pred_str = tc_ad(272, 0.53, 0.10)
    rows.append(("Mo2NF2-CDW", "Tc", "L2", pred_cdw, 1.0, "mu*=0.10 assumed; lambda,wlog independent ab initio"))
    rows.append(("Mo2NF2-strain", "Tc", "L2", pred_str, 4.0, "mu*=0.10 assumed; lambda,wlog independent"))
    # L1 genuine: need a system with ALL params independent. Use MgB2 with full params
    # from a DIFFERENT first-principles source that gives Tc prediction directly -- none in our set
    # -> honestly mark MgB2 Tc as L4 (post-hoc explanation via SMW)
    le_mgb2 = lambda_eff(0.30, 0.196, 0.431)
    pred_mgb2 = PREF * 670 * math.exp(-1 / le_mgb2)
    rows.append(("MgB2", "Tc", "L4", pred_mgb2, 39.0, "SMW two-band post-hoc; wlog external; lambda_eff=%.3f" % le_mgb2))
    # L4: Pb gap ratio two-band explanation (round 69)
    rows.append(("Pb", "gap ratio", "L4", 4.282, 4.29, "two-band superposition w1=0.8 explains single-band dev"))
    # L3: round 58 single-band gap ratio back-substitution (params partly from Tc)
    rows.append(("8 elements", "gap ratio", "L3", 3.53, 3.53, "Mitrovic single-band; Tc measured; ~2.7% dev; not independent"))
    # L4: isotope intermediate (round 61, mu* external component)
    rows.append(("elements", "isotope alpha", "L4", 0.5, 0.48, "chain-external mu* shape; endpoint alpha=1/2"))

    print("FE07 UNIFIED VERIFICATION JUDGEMENT")
    print(f"{'system':<16}{'observable':<14}{'level':<6}{'pred':>8}{'exp':>8}{'rel.dev':>9}")
    for sys, obs, lv, pred, exp, note in rows:
        dev = (pred - exp) / exp if exp else float("nan")
        print(f"{sys:<16}{obs:<14}{lv:<6}{pred:>8.3f}{exp:>8.3f}{dev:>+9.1%}")
    # summary by level
    print("\nBy level:")
    for lv in ("L1", "L2", "L3", "L4"):
        n = sum(1 for r in rows if r[2] == lv)
        print(f"  {lv}: {n} result(s)")
    l1 = sum(1 for r in rows if r[2] == "L1")
    print(f"\nL1 genuine independent predictions: {l1}  <-- honest count")

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["system", "observable", "level", "predicted", "experimental", "note"])
        wr.writerows(rows)

    fig, ax = plt.subplots(figsize=(11, 6))
    colors = {"L1": "green", "L2": "tab:blue", "L3": "gray", "L4": "orange"}
    labels = [f"{r[0]}\n({r[1]})" for r in rows]
    devs = [(r[3] - r[4]) / r[4] * 100 if r[4] else 0 for r in rows]
    cols = [colors[r[2]] for r in rows]
    ax.bar(labels, devs, color=cols, alpha=0.85)
    ax.axhline(0, color="k", lw=1)
    ax.axhspan(-10, 10, color="green", alpha=0.08, label="±10% band")
    ax.set_ylabel("relative deviation (%)")
    ax.set_title("Unified verification judgement (color = verification level)")
    handles = [plt.Rectangle((0,0),1,1,color=colors[l]) for l in ("L1","L2","L3","L4")]
    ax.legend(handles, ["L1 independent prediction", "L2 semi-independent",
                        "L3 back-substitution", "L4 post-hoc explanation"], fontsize=8)
    plt.xticks(rotation=15, fontsize=8)
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)
    print("NOTE: honest judgement -- L1 count is the true measure of predictive validation.")

if __name__ == "__main__":
    main()
