# -*- coding: utf-8 -*-
"""
Lin-6 disambiguation + charge-4e/6e experimental support (quantitative).
Authority 06: Phi_n = h/(ne) (measured h/ne), Phi_n/Phi_2 = 2/n;
winding reading total flux n*h/2e -> ratio n/2 (opposite). Resolution:
two different objects share symbol Phi_n:
  unit h/(ne)      -> 2/n (DECREASING, matches 12.A3 first-band dominance, MEASURED)
  total n*h/(2e)   -> n/2 (INCREASING)
Experiment Ge et al. PRX 2024: h/2e (n=2), h/4e (n=4), h/6e (n=6) quantified.
"""
import csv, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "临6_磁通归一消歧与4e实验.png")
OUT_CSV = os.path.join(HERE, "临6_磁通归一消歧与4e实验.csv")

h = 6.62607015e-34  # J s (exact SI)
e = 1.602176634e-19  # C (exact SI)
Phi0 = h / (2 * e)   # h/2e = 2.0678e-15 Wb

def flux_unit(n): return h / (n * e)   # Phi_n = h/(ne)
def flux_total(n): return n * h / (2 * e)

def main():
    rows = []
    print("Lin-6 flux normalization disambiguation")
    print(f"Phi_0 = h/2e = {Phi0:.4e} Wb (measured standard)")
    print(f"{'n':>3}{'unit h/ne (Wb)':>18}{'unit/Phi_2':>12}{'total n*h/2e':>16}{'total/Phi_2':>13}")
    for n in (2, 4, 6):
        u, t = flux_unit(n), flux_total(n)
        ur, tr = u / flux_unit(2), t / flux_total(2)
        print(f"{n:>3}{u:>18.4e}{ur:>12.4f}{t:>16.4e}{tr:>13.4f}")
        rows.append((n, u, ur, t, tr))

    print("\nExperiment (Ge et al. PRX 14 021025 2024, arXiv:2201.10352):")
    print("  CsV3Sb5 ring: h/2e (n=2, charge-2e), h/4e (n=4, charge-4e), h/6e (n=6, charge-6e)")
    print("  => n=4,6 high modes of CQM 12.A are PHYSICALLY REALIZED (not forbidden)")
    print("  => flux unit h/(ne) is MEASURED -> Phi_n/Phi_2=2/n (unit reading) is physical")
    print("\nResolution: 'two readings opposite' = symbol overloading, not contradiction:")
    print("  Phi_n^unit = h/(ne): ratio 2/n (decreasing) -- matches 12.A3 'first band dominates'")
    print("  Phi_n^total = n h/(2e): ratio n/2 (increasing) -- different object (total flux)")

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh); wr.writerow(["n","flux_unit_h_ne","unit_ratio","flux_total","total_ratio"])
        wr.writerows(rows)

    fig, ax = plt.subplots(1, 2, figsize=(12.5, 5))
    ns = np.arange(2, 11, 2)
    ax[0].plot(ns, [2/n for n in ns], "o-", lw=2.4, color="tab:blue", label=r"unit $2/n$ (measured $h/ne$)")
    ax[0].plot(ns, [n/2 for n in ns], "s-", lw=2.4, color="tab:red", label=r"total $n/2$ (different object)")
    ax[0].axhline(1, color="gray", ls=":", lw=1)
    ax[0].set_xlabel("n (even modes)")
    ax[0].set_ylabel(r"$\Phi_n/\Phi_2$")
    ax[0].set_title("Lin-6: two readings are reciprocal (symbol disambiguation)")
    ax[0].legend(fontsize=8); ax[0].grid(alpha=0.3)

    # experimental flux units h/ne for n=2,4,6
    exp_n = [2, 4, 6]
    exp_flux = [flux_unit(n) for n in exp_n]
    ax[1].bar([f"h/{n}e (n={n})" for n in exp_n], exp_flux, color="tab:green", alpha=0.85)
    ax[1].set_ylabel("flux quantum (Wb)")
    ax[1].set_title("Ge et al. PRX2024: h/4e, h/6e observed (charge-4e/6e)")
    ax[1].grid(alpha=0.3, axis="y")

    fig.tight_layout(); fig.savefig(OUT_PNG, dpi=150); plt.close(fig)
    print("\nsaved:", OUT_PNG, OUT_CSV)
    print("NOTE: Lin-6 STATUS NOT CHANGED (red line: no status upgrade); this is structural evidence.")
    print("      Ge et al. gives EXPERIMENTAL support for n=4,6 modes and Phi_n=h/(ne) definition.")

if __name__ == "__main__":
    main()
