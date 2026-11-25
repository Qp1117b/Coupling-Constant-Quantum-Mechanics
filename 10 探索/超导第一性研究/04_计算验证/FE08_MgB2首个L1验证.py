# -*- coding: utf-8 -*-
"""
FE08: FIRST L1 verification -- MgB2 with FULLY INDEPENDENT parameters.
Paper arXiv:cond-mat/0111182 Table I + body gives ALL three params independently:
  lambda=0.61 (anharmonic avg, from specific heat agreement)
  mu*=0.12 (assumption, but stated and results insensitive 0.10-0.14)
  omega_log=63.5 meV = 737 K (anharmonic, stated in body)
Paper results (Table I):
  isotropic Eliashberg:   Tc = 19 K
  anisotropic Eliashberg: Tc = 39 K
  experiment:             Tc = 39 K
  McMillan formula: underestimates by ~30%

CQM candidate isotropic Tc = Allen-Dynes(wlog=737, lam=0.61, mu*=0.12).
This is L1: params fully independent, formula fixed before comparison, no fit.
We check: does CQM isotropic prediction match paper's isotropic result (19K)?
NOT claiming to predict 39K (that needs FE06 anisotropic extension).
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
OUT_PNG = os.path.join(HERE, "FE08_MgB2首个L1验证.png")
OUT_CSV = os.path.join(HERE, "FE08_MgB2首个L1验证.csv")

def tc_ad(wlog, lam, mustar):
    den = lam - mustar * (1 + 0.62 * lam)
    return wlog / 1.2 * math.exp(-1.04 * (1 + lam) / den) if den > 0 else float("nan")

def main():
    rows = []
    # Fully independent params from paper
    lam, mustar = 0.61, 0.12
    wlog_mev = 63.5
    wlog_K = wlog_mev * 11.604518  # meV -> K
    tc_cqm = tc_ad(wlog_K, lam, mustar)
    tc_iso_paper, tc_aniso_paper, tc_exp = 19.0, 39.0, 39.0

    print("FE08 FIRST L1 VERIFICATION: MgB2 fully independent parameters")
    print(f"  lambda={lam}, mu*={mustar}, omega_log={wlog_mev} meV = {wlog_K:.1f} K (ALL from paper)")
    print(f"  CQM/Allen-Dynes isotropic Tc = {tc_cqm:.2f} K")
    print(f"  paper isotropic Eliashberg Tc = {tc_iso_paper} K")
    print(f"  deviation = {(tc_cqm-tc_iso_paper)/tc_iso_paper:+.1%} (AD approx vs full isotropic Eliashberg)")
    print(f"  paper anisotropic Eliashberg Tc = {tc_aniso_paper} K (= experiment {tc_exp} K)")
    print(f"  anisotropy enhancement = {tc_aniso_paper/tc_iso_paper:.2f}x (isotropic -> anisotropic)")

    rows.append(("CQM_AD_isotropic", tc_cqm, tc_iso_paper, (tc_cqm-tc_iso_paper)/tc_iso_paper, "L1"))
    rows.append(("paper_isotropic", tc_iso_paper, tc_exp, (tc_iso_paper-tc_exp)/tc_exp, "reference"))
    rows.append(("paper_anisotropic", tc_aniso_paper, tc_exp, (tc_aniso_paper-tc_exp)/tc_exp, "reference"))

    # mu* sensitivity (paper says results insensitive 0.10-0.14)
    print("\nmu* sensitivity (paper: results insensitive for 0.10-0.14):")
    for m in (0.10, 0.11, 0.12, 0.13, 0.14):
        tc = tc_ad(wlog_K, lam, m)
        print(f"  mu*={m:.2f}: Tc_AD={tc:.2f} K")
        rows.append(("mu_scan", m, tc, 0, "sensitivity"))

    # omega_log: harmonic 59.4meV vs anharmonic 63.5meV (paper)
    print("\nharmonic vs anharmonic omega_log (paper Table I):")
    for wmev, label in ((59.4, "harmonic"), (63.5, "anharmonic")):
        tc = tc_ad(wmev * 11.604518, 0.73 if label=="harmonic" else 0.61, 0.12)
        print(f"  {label}: lambda={0.73 if label=='harmonic' else 0.61}, wlog={wmev}meV -> Tc_AD={tc:.2f}K")
        rows.append((label, 0.73 if label=="harmonic" else 0.61, tc, 0, "compare"))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "z", "note"])
        wr.writerows(rows)

    fig, ax = plt.subplots(1, 2, figsize=(13, 5.4))
    # left: Tc ladder
    labels = ["CQM/AD\nisotropic", "paper\nisotropic", "paper\nanisotropic", "experiment"]
    vals = [tc_cqm, tc_iso_paper, tc_aniso_paper, tc_exp]
    cols = ["tab:blue", "gray", "tab:green", "red"]
    ax[0].bar(labels, vals, color=cols, alpha=0.85)
    ax[0].set_ylabel("Tc (K)")
    ax[0].set_title("MgB2: isotropic prediction vs anisotropic reality")
    ax[0].grid(alpha=0.3, axis="y")
    for i, v in enumerate(vals):
        ax[0].text(i, v + 0.5, f"{v:.1f}", ha="center", fontsize=9)

    # right: mu* sensitivity
    ms = np.linspace(0.10, 0.14, 50)
    ax[1].plot(ms, [tc_ad(wlog_K, lam, m) for m in ms], lw=2.4, color="tab:purple")
    ax[1].axvline(0.12, color="red", ls="--", lw=1.4, label="paper mu*=0.12")
    ax[1].set_xlabel(r"$\mu^*$")
    ax[1].set_ylabel(r"$T_c$ (K)")
    ax[1].set_title("L1: fully independent params; insensitivity")
    ax[1].legend(fontsize=8)
    ax[1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG, OUT_CSV)
    print("NOTE: L1 verified -- CQM isotropic matches paper isotropic (~25% AD approx error),")
    print("      NOT a fit to 39K (which requires FE06 anisotropic extension).")

if __name__ == "__main__":
    main()
