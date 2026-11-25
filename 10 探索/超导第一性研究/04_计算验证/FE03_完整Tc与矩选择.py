# -*- coding: utf-8 -*-
"""
FE03 CANDIDATE (NOT LANDED): full Tc with FE01 scale + mu* + moment choice.
Core result: using CQM moment e^{-1/3} instead of Eliashberg e^{-1/2}
overestimates absolute Tc by e^{1/6} = 18.1% (linear prefactor).
Panels:
 A  Tc vs lambda for two moments (mu*=0.1) -- e^{1/6} gap
 B  Tc vs mu* at fixed lambda -- Coulomb suppression
 C  moment bias ratio Tc_CQM/Tc_Eliash = e^{1/6} (constant 1.181)
 D  back-substitution with round-61 inverted (lam,mu*): self-consistency, NOT independent validation
Allen-Dynes Webb Eq2. No fitting (D uses measured Tc-derived params -> selfcheck only).
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
OUT_PNG = os.path.join(HERE, "FE03_完整Tc与矩选择.png")
OUT_CSV = os.path.join(HERE, "FE03_完整Tc与矩选择.csv")

E13 = math.exp(-1 / 3)
E12 = math.exp(-1 / 2)
BIAS = math.exp(1 / 6)
THETA_D = 200.0  # representative, from FE01 scale (external)


def tc_ad(wln, lam, must):
    den = lam - must * (1 + 0.62 * lam)
    if den <= 0:
        return float("nan")
    return wln / 1.2 * math.exp(-1.04 * (1 + lam) / den)


def main():
    rows = []
    print(f"FE03 candidate: moment ratio e^(1/6) = {BIAS:.4f} -> CQM moment overestimates Tc by {BIAS-1:.1%}")

    # A: Tc vs lambda, two moments
    lams = np.linspace(0.3, 1.0, 200)
    print("\nA Tc vs lambda (mu*=0.1, theta_D=200K):")
    for lam in (0.4, 0.6, 0.8):
        t1 = tc_ad(E13 * THETA_D, lam, 0.1)   # CQM moment
        t2 = tc_ad(E12 * THETA_D, lam, 0.1)   # Eliash moment
        print(f"  lam={lam:.2f}: Tc_CQM={t1:.2f}K  Tc_Eliash={t2:.2f}K  ratio={t1/t2:.4f}")
    for lam in lams:
        rows.append(("Tc_vs_lam", lam, tc_ad(E13*THETA_D, lam, 0.1),
                     tc_ad(E12*THETA_D, lam, 0.1), ""))

    # B: mu* suppression
    musts = np.linspace(0, 0.25, 200)
    print("\nB Tc vs mu* (lam=0.7, Eliash moment):")
    for ms in (0.0, 0.1, 0.2):
        print(f"  mu*={ms:.2f}: Tc={tc_ad(E12*THETA_D, 0.7, ms):.2f}K")
    for ms in musts:
        rows.append(("Tc_vs_mustar", ms, tc_ad(E12*THETA_D, 0.7, ms), 0, ""))

    # C: moment bias (constant)
    print(f"\nC moment bias constant: {BIAS:.4f} (should be independent of lambda)")
    for lam in (0.4, 0.6, 0.8, 1.0):
        t1 = tc_ad(E13*THETA_D, lam, 0.1)
        t2 = tc_ad(E12*THETA_D, lam, 0.1)
        rows.append(("bias", lam, t1/t2, BIAS, ""))

    # D: back-substitution with round-61 inverted (lam,mu*) -- self-consistency only
    # round-61 sample solutions (element, Tc_exp, lam, mu*) from double-observation inversion
    SAMPLES = [("Pb", 7.20, 1.294, 0.106), ("V", 5.40, 0.939, 0.253),
               ("Ta", 4.40, 0.801, 0.176), ("Nb", 9.25, 0.566, 0.13)]
    print("\nD back-substitution (self-consistency, NOT independent validation):")
    print(f"{'el':<4}{'Tc_exp':>8}{'Tc_FE03':>9}{'ratio':>8}")
    backs = []
    for name, tc_exp, lam, ms in SAMPLES:
        # need wln that reproduces Tc_exp with these (lam,ms): invert
        den = lam - ms * (1 + 0.62 * lam)
        wln_req = tc_exp * 1.2 * math.exp(1.04 * (1 + lam) / den)
        tc_fit = tc_ad(wln_req, lam, ms)
        backs.append((name, tc_exp, tc_fit, tc_fit/tc_exp))
        print(f"{name:<4}{tc_exp:>8.2f}{tc_fit:>9.3f}{tc_fit/tc_exp:>8.4f}")
        rows.append(("backsub", tc_exp, tc_fit, tc_fit/tc_exp, name))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y2", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.4, 9.6))

    ax[0, 0].plot(lams, [tc_ad(E13*THETA_D, l, 0.1) for l in lams],
                  lw=2.2, label="CQM moment $e^{-1/3}$", color="tab:red")
    ax[0, 0].plot(lams, [tc_ad(E12*THETA_D, l, 0.1) for l in lams],
                  lw=2.2, label="Eliash moment $e^{-1/2}$", color="tab:blue")
    ax[0, 0].set_xlabel(r"$\lambda$")
    ax[0, 0].set_ylabel(r"$T_c$ (K)")
    ax[0, 0].set_title("A  two moments: systematic $e^{1/6}$ gap")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    ax[0, 1].plot(musts, [tc_ad(E12*THETA_D, 0.7, m) for m in musts],
                  lw=2.4, color="tab:purple")
    ax[0, 1].set_xlabel(r"$\mu^*$")
    ax[0, 1].set_ylabel(r"$T_c$ (K)")
    ax[0, 1].set_title(r"B  Coulomb suppression ($\lambda=0.7$)")
    ax[0, 1].grid(alpha=0.3)

    bias_lams = [0.4, 0.6, 0.8, 1.0]
    bias_vals = [tc_ad(E13*THETA_D, l, 0.1)/tc_ad(E12*THETA_D, l, 0.1) for l in bias_lams]
    ax[1, 0].plot(bias_lams, bias_vals, "o", color="tab:orange", ms=8, label="computed")
    ax[1, 0].axhline(BIAS, color="k", ls="--", lw=1.4, label=f"$e^{{1/6}}={BIAS:.4f}$")
    ax[1, 0].set_xlabel(r"$\lambda$")
    ax[1, 0].set_ylabel(r"$T_c^{CQM}/T_c^{Eliash}$")
    ax[1, 0].set_title(r"C  moment bias is constant 18.1%")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3)

    names = [b[0] for b in backs]
    ratios = [b[3] for b in backs]
    ax[1, 1].bar(names, [b[2] for b in backs], color="tab:green", alpha=0.8, label="FE03 fit")
    ax[1, 1].plot(names, [b[1] for b in backs], "o", color="black", ms=7, label="Tc_exp")
    ax[1, 1].set_ylabel(r"$T_c$ (K)")
    ax[1, 1].set_title(r"D  self-consistency (NOT validation)")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)
    print("NOTE: FE03 candidate NOT landed; panel D is self-consistency using measured-derived")
    print("      (lam,mu*) -- NOT an independent prediction. External Allen-Dynes + FE01 scale.")


if __name__ == "__main__":
    main()
