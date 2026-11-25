"""Ring 15: sign check for the n_cell = N_eff(T) leading correction.

Pure algebra, no data fit:
  x/x0 = (1 - b t)/(1 - a t),  t = (T/omega_D)^2,  a = pi^2/3.
  The leading coefficient is a - b.

Outputs:
  环15_nT方向.csv
  环15_nT方向.png
"""

import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_CSV = os.path.join(HERE, "环15_nT方向.csv")
OUT_PNG = os.path.join(HERE, "环15_nT方向.png")

A = math.pi**2 / 3.0
T_GRID = np.linspace(0.0, 0.45, 400)


def ratio(T, b_over_a):
    b = b_over_a * A
    return (1.0 - b * T**2) / (1.0 - A * T**2)


def main():
    ratios = {br: ratio(T_GRID, br) for br in [0.0, 0.5, 1.0, 1.5]}

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["T_over_omegaD", "ratio_b0", "ratio_b0.5a",
                     "ratio_b1a", "ratio_b1.5a"])
        for i, t in enumerate(T_GRID):
            wr.writerow([t, ratios[0.0][i], ratios[0.5][i],
                         ratios[1.0][i], ratios[1.5][i]])

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))

    ax = axes[0]
    for br, lab in [(0.0, "b=0 (fixed n)"), (0.5, "b=0.5a"),
                    (1.0, "b=a"), (1.5, "b=1.5a")]:
        ax.plot(T_GRID, ratios[br], lw=2.0, label=lab)
    ax.set_xlabel(r"$T/\omega_D$")
    ax.set_ylabel(r"$x/x_0$")
    ax.set_title(r"(a) normalized argument: $(1-bt)/(1-at)$")
    ax.legend()
    ax.grid(alpha=0.3)

    ax = axes[1]
    br = np.linspace(0.0, 2.0, 400)
    coeff = 1.0 - br
    ax.plot(br, coeff, lw=2.2, color="C0")
    ax.axhline(0.0, color="k", lw=1.0)
    ax.axvline(1.0, color="C3", ls="--", lw=1.5)
    ax.fill_between(br, coeff, 0.0, where=(br > 1.0),
                    color="C1", alpha=0.25, label="direction violated")
    ax.set_xlabel(r"$b/a$")
    ax.set_ylabel(r"$(a-b)/a$")
    ax.set_title(r"(b) leading coefficient sign: zero at $b=a$")
    ax.legend()
    ax.grid(alpha=0.3)

    fig.suptitle("Ring 15: n_cell = N_eff(T) leading correction; pure algebra, not a data fit",
                 fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT_PNG, dpi=160)
    print("A =", A)
    for br in [0.0, 0.5, 1.0, 1.5]:
        print(f"b/a={br}: ratio(T=0.45)={ratio(0.45, br):.6f}")
    print("files:", OUT_CSV, OUT_PNG)


if __name__ == "__main__":
    main()
