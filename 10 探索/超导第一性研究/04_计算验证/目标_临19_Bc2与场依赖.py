# -*- coding: utf-8 -*-
"""
目标区／临-19 的数值核对。

1. B_c2 = Phi0/(2 pi xi^2) 随 xi 的双曲线（Phi0=h/2e）；
2. f_a(x)=1-a x 低场近似（a=0.2,0.5,0.8）；
3. 归一化初始斜率 -a；
4. q=e 与 q=2e 的磁通量子对比（链选 q=2e）。

外部物理常数只作数值示意；曲线由 (L19.1)-(L19.5) 直接计算。
"""

import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "目标_临19_Bc2与场依赖.png")
OUT_CSV = os.path.join(HERE, "目标_临19_Bc2与场依赖.csv")

H = 6.62607015e-34   # J s
E = 1.602176634e-19  # C
PHI0 = H / (2 * E)
PI = np.pi


def main():
    rows = []
    print(f"Phi0 = h/(2e) = {PHI0:.6e} Wb")
    rows.append(("phi0", 2, PHI0, H / E, np.nan))

    print("\nBc2 vs xi")
    for xi_nm in (2, 5, 10, 20, 50, 100):
        xi = xi_nm * 1e-9
        bc2 = PHI0 / (2 * PI * xi ** 2)
        print(f"  xi={xi_nm:3d} nm: Bc2={bc2:.4f} T")
        rows.append(("bc2", xi_nm, bc2, np.nan, np.nan))

    print("\n低场斜率")
    for a in (0.2, 0.5, 0.8):
        print(f"  a={a}: f'(0)={-a}, f(0.2)={1-a*0.2:.3f}")
        rows.append(("slope", a, -a, 1 - a * 0.2, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A Bc2
    xis = np.linspace(2, 100, 400)
    bc2s = PHI0 / (2 * PI * (xis * 1e-9) ** 2)
    ax[0, 0].plot(xis, bc2s, lw=2.2, color="tab:blue")
    ax[0, 0].set_xlabel(r"$\xi$ (nm)")
    ax[0, 0].set_ylabel(r"$B_{c2}$ (T)")
    ax[0, 0].set_title(r"A  $B_{c2}=\Phi_0/(2\pi\xi^2)$")
    ax[0, 0].grid(alpha=0.3, which="both")

    # B f
    x = np.linspace(0, 1, 200)
    for a in (0.2, 0.5, 0.8):
        ax[0, 1].plot(x, 1 - a * x, lw=2.0, label=rf"$a={a}$")
    ax[0, 1].set_xlabel(r"$x=B/B_{c2}$")
    ax[0, 1].set_ylabel(r"$f(x)$")
    ax[0, 1].set_title(r"B  低场近似 $f=1-a x$")
    ax[0, 1].legend(fontsize=9)
    ax[0, 1].grid(alpha=0.3)

    # C slope
    aa = np.array([0.2, 0.5, 0.8])
    ax[1, 0].bar(aa, -aa, width=0.08, color="tab:orange", alpha=0.85)
    ax[1, 0].set_xlabel(r"$a$")
    ax[1, 0].set_ylabel(r"初始斜率 $-a$")
    ax[1, 0].set_title("C  归一化初始斜率（a 外生）")
    ax[1, 0].grid(alpha=0.3, axis="y")

    # D flux quantum
    ax[1, 1].bar(["q=e（链排除）", "q=2e（链选）"], [H / E, H / (2 * E)],
                 color=["tab:red", "tab:green"], alpha=0.85)
    ax[1, 1].set_ylabel(r"$\Phi_0=h/q$ (Wb)")
    ax[1, 1].set_title("D  配对电荷决定磁通量子")
    ax[1, 1].grid(alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
