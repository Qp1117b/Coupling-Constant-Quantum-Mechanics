# -*- coding: utf-8 -*-
"""
FE01 framework-extension CANDIDATE (NOT LANDED): dimensional postulate -> Tc.
Numerical sanity of the candidate scale (NO fitting):
  omega_D = sqrt(kappa/M) * k_D,  k_D=(6 pi^2 n)^{1/3},  theta_D = hbar omega_D/kB
  Tc = 1.13 e^{-1/6} theta_D e^{-(1+lam)/lam}
Panels:
 A  Tc vs lambda (fixed M,kappa,n) -- BCS-like dome-free monotone in lambda
 B  isotope: ln Tc vs ln M slope = -1/2 (alpha=1/2), from postulate
 C  theta_D vs sqrt(kappa/M) linear through origin
 D  back-infer kappa/M from Webb Table III theta_D at fixed n -> magnitude check
All external constants (hbar,kB,Webb theta_D) are cited, not fitted.
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
OUT_PNG = os.path.join(HERE, "FE01_能标闭合.png")
OUT_CSV = os.path.join(HERE, "FE01_能标闭合.csv")

HBAR = 1.054571817e-34   # J s (CODATA)
KB = 1.380649e-23        # J/K (exact, SI 2019)
PREF = 1.13 * math.exp(-1 / 6)

# Webb 2015 Table III (element, theta_D K) -- cited
DATA = [("Al", 428), ("Sn", 200), ("Pb", 105), ("Nb", 275),
        ("V", 380), ("Cd", 209), ("Ta", 240), ("In", 108)]


def kD(n):
    return (6 * math.pi ** 2 * n) ** (1 / 3)


def thetaD(kappa, M, n, a=1.0):
    # omega_D = a sqrt(kappa/M) k_D ; theta_D = hbar omega_D / kB
    return HBAR * a * math.sqrt(kappa / M) * kD(n) / KB


def tc(theta, lam):
    return PREF * theta * math.exp(-(1 + lam) / lam)


def main():
    rows = []
    # representative metal: n ~ 1e29 m^-3, M ~ 100 amu, kappa tuned so theta_D~200K
    n0 = 1.0e29
    amu = 1.66053906660e-27
    M0 = 100 * amu
    # solve kappa for theta_D = 200 K
    kappa0 = (200 * KB / (HBAR * kD(n0))) ** 2 * M0

    print("FE01 CANDIDATE dimensional-postulate sanity (no fitting)")
    print(f"n0={n0:.2e} m^-3, M0={M0/amu:.0f} amu -> kappa for theta_D=200K:")
    print(f"  kappa0 = {kappa0:.4e} N/m")
    print(f"  thetaD(kappa0) = {thetaD(kappa0, M0, n0):.2f} K (target 200)")

    # Panel A: Tc vs lambda
    lams = np.linspace(0.15, 0.8, 200)
    print("\nA Tc vs lambda (theta_D=200K):")
    for lam in (0.2, 0.3, 0.5, 0.8):
        print(f"  lam={lam:.2f}: Tc={tc(200,lam):.3f} K")
    for lam in lams:
        rows.append(("Tc_vs_lam", lam, tc(200, lam), "", ""))

    # Panel B: isotope slope
    Ms = np.logspace(np.log10(20 * amu), np.log10(250 * amu), 100)
    lnM = np.log(Ms)
    lnTc = np.log([tc(thetaD(kappa0, M, n0), 0.4) for M in Ms])
    slope, intercept = np.polyfit(lnM, lnTc, 1)
    print(f"\nB isotope slope dlnTc/dlnM = {slope:.4f} (expected -0.5, alpha=0.5)")
    for m, ltc in zip(Ms[::20], lnTc[::20]):
        rows.append(("isotope", math.log(m), ltc, "", ""))

    # Panel C: theta_D vs sqrt(kappa/M)
    ratios = np.linspace(1e-4, 1e-2, 100)  # kappa/M in SI (N m/kg = m^2/s^2)
    thetas = [HBAR * math.sqrt(r) * kD(n0) / KB for r in ratios]
    print("\nC theta_D linear in sqrt(kappa/M):")
    print(f"  sqrt(kappa/M)=1e-3 -> theta_D={HBAR*1e-3*kD(n0)/KB:.1f} K")
    for r, th in zip(ratios[::20], thetas[::20]):
        rows.append(("thetaD_scale", math.sqrt(r), th, "", ""))

    # Panel D: back-infer kappa/M from Webb theta_D at fixed n
    print("\nD kappa/M needed per element (n=1e29 m^-3):")
    backs = []
    for name, theta in DATA:
        km = (theta * KB / (HBAR * kD(n0))) ** 2  # kappa/M = (theta kB/(hbar kD))^2
        backs.append((name, km))
        print(f"  {name:<3} theta_D={theta:>3}K -> kappa/M={km:.4e} m^2/s^2")
        rows.append(("back_infer", theta, km, "", name))
    kms = [b[1] for b in backs]

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "aux", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.4, 9.6))

    ax[0, 0].plot(lams, [tc(200, l) for l in lams], lw=2.4, color="tab:blue")
    ax[0, 0].set_xlabel(r"$\lambda$")
    ax[0, 0].set_ylabel(r"$T_c$ (K)")
    ax[0, 0].set_title(r"A  $T_c$ vs $\lambda$ ($\theta_D=200$K, candidate)")
    ax[0, 0].grid(alpha=0.3)

    ax[0, 1].plot(lnM, lnTc, lw=2.2, color="tab:green",
                  label=f"slope={slope:.4f}")
    ax[0, 1].set_xlabel(r"$\ln M$")
    ax[0, 1].set_ylabel(r"$\ln T_c$")
    ax[0, 1].set_title(r"B  isotope: slope $-1/2$ ($\alpha=1/2$)")
    ax[0, 1].legend(fontsize=9)
    ax[0, 1].grid(alpha=0.3)

    ax[1, 0].plot([math.sqrt(r) for r in ratios], thetas, lw=2.2, color="tab:purple")
    ax[1, 0].set_xlabel(r"$\sqrt{\kappa/M}$ (m/s)")
    ax[1, 0].set_ylabel(r"$\theta_D$ (K)")
    ax[1, 0].set_title(r"C  Debye scale linear in $\sqrt{\kappa/M}$")
    ax[1, 0].grid(alpha=0.3)

    names = [b[0] for b in backs]
    ax[1, 1].bar(names, kms, color="tab:orange", alpha=0.85)
    ax[1, 1].set_ylabel(r"$\kappa/M$ (m$^2$/s$^2$)")
    ax[1, 1].set_title(r"D  magnitude check: $\kappa/M$ from Webb $\theta_D$")
    ax[1, 1].grid(alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)
    print("NOTE: FE01 is a CANDIDATE framework extension (NOT landed).")
    print("      kappa, M, n, lambda remain material inputs; no absolute Tc prediction.")
    print("      Isotope slope -1/2 is a self-consistency check of the postulate.")


if __name__ == "__main__":
    main()
