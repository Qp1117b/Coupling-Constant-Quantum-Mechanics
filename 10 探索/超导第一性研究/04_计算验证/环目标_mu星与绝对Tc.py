# -*- coding: utf-8 -*-
"""
mu* shape (M.1) + absolute-Tc sensitivity (Allen-Dynes M.2).

NO fabricated material data. Two layers:
  - M.1 shape (strict): mu* = mu/(1+mu L), L=ln(eps_F/hbar w_D).
  - M.2 sensitivity/inverse (structural): Tc from Allen-Dynes with CQM
    omega_log = e^{-1/3} theta_D; show how mu* controls absolute Tc and
    invert for lambda(lambda | Tc_exp, mu*) using Webb Table III Tc.
We do NOT claim pure first-principles absolute Tc: eps_F, mu, lambda, mu*
are external; CQM supplies omega_log only.

Panels:
  A  M.1 shape family: mu* vs mu for L in {2,4,8}; mu*<mu, monotone.
  B  M.1 adiabatic limit: mu* vs L (fixed mu), with 1/L asymptote.
  C  Allen-Dynes sensitivity: Tc vs mu* at fixed lambda, omega_log.
  D  Inverse contour: lambda(mu* | Tc_exp) for 8 elements; Eq37 lambda=0 mark.
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
OUT_PNG = os.path.join(HERE, "环目标_mu星与绝对Tc.png")
OUT_CSV = os.path.join(HERE, "环目标_mu星与绝对Tc.csv")

E3 = math.exp(-1 / 3)  # CQM omega_log / theta_D

# Webb 2015 Table III (Tc, theta_D) -- experimentally measured, cited in cart.
DATA = [
    ("Al", 1.18, 428),
    ("Sn", 3.70, 200),
    ("Pb", 7.20, 105),
    ("Nb", 9.25, 275),
    ("V ", 5.40, 380),
    ("Cd", 0.52, 209),
    ("Ta", 4.40, 240),
    ("In", 3.40, 108),
]


def mustar(mu, L):
    return mu / (1 + mu * L)


def allen_dynes_Tc(wlog, lam, must):
    """Allen-Dynes (M.2), kB=1, wlog in K. mu* enters denominator."""
    den = lam - must * (1 + 0.62 * lam)
    if den <= 0:
        return float("nan")
    return wlog / 1.2 * math.exp(-1.04 * (1 + lam) / den)


def invert_lambda(wlog, tc_exp, must):
    """Solve Tc_AD(lam|must)=tc_exp for lam (closed form).
    y = ln(wlog/(1.2 tc)); lam = (1.04 + y must)/(y(1-0.62 must) - 1.04)."""
    y = math.log(wlog / (1.2 * tc_exp))
    den = y * (1 - 0.62 * must) - 1.04
    if den <= 0:
        return float("nan")
    return (1.04 + y * must) / den


def main():
    rows = []

    # Panel A: shape family
    mus = np.linspace(0.01, 3.0, 200)
    print("A M.1 shape family: mu* = mu/(1+mu L)")
    for L in (2.0, 4.0, 8.0):
        ys = [mustar(m, L) for m in mus]
        print(f"  L={L}: mu*(0.5)={mustar(0.5,L):.4f}  mu*(2)={mustar(2,L):.4f}  1/L={1/L:.4f}")
        for m, y in zip(mus[::40], ys[::40]):
            rows.append(("shape", L, m, y, ""))

    # Panel B: adiabatic limit
    Ls = np.linspace(0.5, 12.0, 200)
    mu_fix = 1.0
    print("\nB adiabatic limit (fixed mu=1): mu* -> 1/L as L grows")
    for L in (1, 2, 4, 8, 12):
        print(f"  L={L}: mu*={mustar(mu_fix,L):.4f}  1/L={1/L:.4f}")
    for L in Ls[::20]:
        rows.append(("limit", mu_fix, L, mustar(mu_fix, L), ""))
        rows.append(("asymptote", mu_fix, L, 1 / L, ""))

    # Panel C: Allen-Dynes sensitivity
    print("\nC Allen-Dynes sensitivity: Tc vs mu* (lambda=0.8, wlog=200K)")
    lam_fix, wlog_fix = 0.8, 200.0
    musts = np.linspace(0, 0.3, 200)
    for ms in (0.0, 0.1, 0.2, 0.3):
        tc = allen_dynes_Tc(wlog_fix, lam_fix, ms)
        print(f"  mu*={ms:.2f}: Tc={tc:.3f} K")
    for ms in musts[::20]:
        rows.append(("sens", lam_fix, ms, allen_dynes_Tc(wlog_fix, lam_fix, ms), ""))

    # Panel D: inverse contour using Webb Tc (no fabricated lambda/mu*)
    print("\nD inverse contour: lambda needed to match Tc_exp at each mu*")
    print(f"{'el':<4}{'Tc':>6}{'wlog':>8}{'lam(ms=0)':>11}{'lam(0.1)':>10}{'lam(0.2)':>10}")
    ms_grid = np.linspace(0, 0.25, 120)
    for name, tc, theta in DATA:
        wlog = E3 * theta
        l0 = invert_lambda(wlog, tc, 0.0)
        l1 = invert_lambda(wlog, tc, 0.1)
        l2 = invert_lambda(wlog, tc, 0.2)
        print(f"{name:<4}{tc:>6.2f}{wlog:>8.1f}{l0:>11.3f}{l1:>10.3f}{l2:>10.3f}")
        for ms in ms_grid:
            rows.append(("inverse", tc, ms, invert_lambda(wlog, tc, ms), name.strip()))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "p1", "p2", "y", "extra"])
        wr.writerows(rows)

    # ---- figure ----
    fig, ax = plt.subplots(2, 2, figsize=(13.4, 9.6))

    for L in (2.0, 4.0, 8.0):
        ax[0, 0].plot(mus, [mustar(m, L) for m in mus], lw=2.2, label=f"L={L}")
    ax[0, 0].plot(mus, mus, "k--", lw=1.2, label=r"$\mu^*=\mu$")
    ax[0, 0].set_xlabel(r"$\mu$ (bare Coulomb)")
    ax[0, 0].set_ylabel(r"$\mu^*$")
    ax[0, 0].set_title(r"A  M.1 shape: $\mu^*<\mu$, monotone")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    ax[0, 1].plot(Ls, [mustar(mu_fix, L) for L in Ls], lw=2.2, label=r"$\mu^*$ (mu=1)")
    ax[0, 1].plot(Ls, 1 / Ls, "r--", lw=1.4, label=r"$1/L$ asymptote")
    ax[0, 1].set_xlabel(r"$L=\ln(\epsilon_F/\hbar\omega_D)$")
    ax[0, 1].set_ylabel(r"$\mu^*$")
    ax[0, 1].set_title(r"B  adiabatic limit: $\mu^*\to 1/L$")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    ax[1, 0].plot(musts, [allen_dynes_Tc(wlog_fix, lam_fix, m) for m in musts],
                  lw=2.4, color="tab:purple")
    ax[1, 0].set_xlabel(r"$\mu^*$")
    ax[1, 0].set_ylabel(r"$T_c$ (K)")
    ax[1, 0].set_title(r"C  Allen-Dynes sensitivity ($\lambda=0.8,\omega_{\log}=200$K)")
    ax[1, 0].grid(alpha=0.3)

    for name, tc, theta in DATA:
        wlog = E3 * theta
        ax[1, 1].plot(ms_grid, [invert_lambda(wlog, tc, m) for m in ms_grid],
                      lw=1.6, label=name.strip())
    ax[1, 1].set_xlabel(r"$\mu^*$ (external material value)")
    ax[1, 1].set_ylabel(r"$\lambda$ needed to match $T_c^{exp}$")
    ax[1, 1].set_title(r"D  inverse: CQM $\omega_{\log}$ + AD -> $\lambda(\mu^*)$")
    ax[1, 1].legend(fontsize=7, ncol=2)
    ax[1, 1].set_ylim(0, 3)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)
    print("\nNOTE: absolute Tc NOT pure first-principles; eps_F, mu, lambda, mu* external;")
    print("      CQM supplies omega_log=e^{-1/3} theta_D only.")


if __name__ == "__main__":
    main()
