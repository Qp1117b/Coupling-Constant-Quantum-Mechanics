# -*- coding: utf-8 -*-
"""
FE02 CANDIDATE (NOT LANDED): quantitative no-go -- number-theoretic energy scale
is circular. Authority lin-22: Gamma_n ~ gamma_n^2 T / w^2 (w=omega_D external).
Panels:
 A  Gamma_1 vs w at fixed T: ~ 1/w^2 (decreasing) -> scale depends on the very w it would replace
 B  Gamma_1 vs T linear at fixed w
 C  lin-8: rate_n - rate_m = (gamma_n^2-gamma_m^2) sigma_v^2 tau_g != 0 for distinct modes
 D  self-consistency w^4 = k C g2 T: w depends on T & external C, NOT gamma alone
No fitting. gamma_1 ~ 14.1347 (first Riemann zero, universal); w,C,T external.
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
OUT_PNG = os.path.join(HERE, "FE02_数论能标循环.png")
OUT_CSV = os.path.join(HERE, "FE02_数论能标循环.csv")

GAMMA1 = 14.134725141734693  # first nontrivial Riemann zero imaginary part
G2 = GAMMA1 ** 2


def gamma1_rate(T, w, C=1.0):
    return C * G2 * T / w ** 2


def main():
    rows = []
    # A: Gamma_1 vs w (fixed T)
    ws = np.linspace(1, 20, 200)
    print("A Gamma_1 ~ 1/w^2 (T=1, C=1): scale depends on external w")
    for w in (2, 5, 10, 20):
        print(f"  w={w:>4}: Gamma_1={gamma1_rate(1.0, w):.4f}")
    for w in ws:
        rows.append(("Gamma_vs_w", w, gamma1_rate(1.0, w), "", ""))

    # B: Gamma_1 vs T linear
    Ts = np.linspace(0, 2, 100)
    for T in Ts[::20]:
        rows.append(("Gamma_vs_T", T, gamma1_rate(T, 5.0), "", ""))
    print(f"\nB Gamma_1 linear in T: Gamma_1(T=1,w=5)={gamma1_rate(1,5):.4f}")

    # C: lin-8 mode-rate splitting (gamma_1 vs gamma_2)
    gamma2 = 21.022039638771554
    g2_1, g2_2 = GAMMA1 ** 2, gamma2 ** 2
    sv2tau = 0.01  # external positive
    print(f"\nC lin-8: (gamma_2^2-gamma_1^2) sv2tau = {(g2_2-g2_1)*sv2tau:.3f} (nonzero => no alignment)")
    for n in range(5):
        rows.append(("l8_split", n, (g2_2 - g2_1) * sv2tau, "", ""))

    # D: self-consistency w^4 = k C g2 T
    k, C = 0.01, 1.0
    print("\nD self-consistency w^4 = k C g2 T:")
    for T in (1, 4, 9):
        w4 = k * C * G2 * T
        w = w4 ** 0.25
        print(f"  T={T}: w={w:.4f} (w^4={w4:.2f}) -- depends on T & k,C, not gamma alone")
        rows.append(("self_consistent_w", T, w, "", ""))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "aux", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.4, 9.6))

    ax[0, 0].plot(ws, [gamma1_rate(1.0, w) for w in ws], lw=2.4, color="tab:red")
    ax[0, 0].set_xlabel(r"$w=\omega_D$ (external)")
    ax[0, 0].set_ylabel(r"$\Gamma_1$")
    ax[0, 0].set_title(r"A  lin-22: $\Gamma_1\propto 1/\omega_D^2$ (circular)")
    ax[0, 0].grid(alpha=0.3)

    ax[0, 1].plot(Ts, [gamma1_rate(T, 5.0) for T in Ts], lw=2.4, color="tab:blue")
    ax[0, 1].set_xlabel(r"$T$ (external)")
    ax[0, 1].set_ylabel(r"$\Gamma_1$")
    ax[0, 1].set_title(r"B  $\Gamma_1\propto T$ at fixed $\omega_D$")
    ax[0, 1].grid(alpha=0.3)

    ax[1, 0].bar(["rate_1-rate_2"], [(g2_1 - g2_2) * sv2tau], color="tab:purple", alpha=0.85)
    ax[1, 0].axhline(0, color="k", lw=1)
    ax[1, 0].set_ylabel(r"$\Delta$rate")
    ax[1, 0].set_title(r"C  lin-8: mode rates cannot align ($\neq 0$)")
    ax[1, 0].grid(alpha=0.3, axis="y")

    Ts2 = np.linspace(0.5, 10, 100)
    ws_sc = [(k * C * G2 * T) ** 0.25 for T in Ts2]
    ax[1, 1].plot(Ts2, ws_sc, lw=2.4, color="tab:green")
    ax[1, 1].set_xlabel(r"$T$")
    ax[1, 1].set_ylabel(r"self-consistent $w$")
    ax[1, 1].set_title(r"D  $w^4=kC\gamma_1^2T$: needs external $T,k,C$")
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)
    print("NOTE: FE02 is a NEGATIVE result (candidate, not landed): number theory alone")
    print("      cannot fix the energy scale; external omega_D/T/C are unavoidable.")


if __name__ == "__main__":
    main()
