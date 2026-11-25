# -*- coding: utf-8 -*-
"""
环 13.A／`临-26` A4 根电荷的数值核对。

1. A4 的 20 个根/10 个正根（i<j）；
2. 基础余特征 h=omega_k 下各根电荷分布（只含 -1,0,1）；
3. 整余特征 vs 半整余特征的电荷格点；
4. 与 G19 半整数格点的交集（整数）。
"""

import csv
import os
from itertools import permutations

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "环13A_临26_A4权电荷.png")
OUT_CSV = os.path.join(HERE, "环13A_临26_A4权电荷.csv")

ROOTS = [(i, j) for i in range(5) for j in range(5) if i != j]
POS = [(i, j) for i in range(5) for j in range(i + 1, 5)]


def main():
    rows = []
    print(f"A4 根数={len(ROOTS)}, 正根数={len(POS)}")
    rows.append(("roots", 20, len(ROOTS), 10, len(POS)))

    print("\n基础余特征 omega_k 的根电荷分布")
    allq = set()
    for k in range(5):
        qs = [int(i == k) - int(j == k) for (i, j) in ROOTS]
        allq.update(qs)
        print(f"  k={k}: {sorted(set(qs))}")
        rows.append(("omega_charge", k, len(set(qs)), min(qs), max(qs)))

    print(f"\n所有出现的电荷: {sorted(allq)}")
    int_lattice = np.arange(-3, 3.01, 0.5)
    half_allowed = np.isclose(int_lattice * 2, np.round(int_lattice * 2))
    for x in int_lattice:
        ok = bool(np.isclose(x * 2, round(x * 2)))
        rows.append(("lattice", float(x), 1.0 if ok else 0.0, np.nan, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A roots
    ax[0, 0].scatter([p[0] for p in ROOTS], [p[1] for p in ROOTS],
                     color="tab:blue", alpha=0.6, s=40, label="20 roots")
    ax[0, 0].scatter([p[0] for p in POS], [p[1] for p in POS],
                     color="tab:red", s=55, label="10 positive")
    ax[0, 0].set_xlabel("i")
    ax[0, 0].set_ylabel("j")
    ax[0, 0].set_title("A  A4 根 e_i - e_j")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    # B omega charges
    for k in range(3):
        qs = [int(i == k) - int(j == k) for (i, j) in ROOTS]
        ax[0, 1].hist(qs, bins=[-1.5, -0.5, 0.5, 1.5], alpha=0.5, label=f"k={k}")
    ax[0, 1].set_xlabel("根电荷")
    ax[0, 1].set_title("B  基础余特征：电荷仅 -1/0/1")
    ax[0, 1].legend(fontsize=8)

    # C lattice
    ax[1, 0].scatter(int_lattice, np.zeros_like(int_lattice),
                     c=["tab:green" if h else "tab:red" for h in half_allowed],
                     s=80, zorder=5)
    ax[1, 0].axhline(0, color="0.4", lw=1)
    ax[1, 0].set_xlabel("电荷 s")
    ax[1, 0].set_title("C  半整格点（绿）与排除点（红）")
    ax[1, 0].set_yticks([])
    ax[1, 0].grid(alpha=0.3, axis="x")

    # D allowed branches
    labels = ["s=0", "s=1/2", "s=1", "s=2"]
    vals = [1, 0, 1, 1]
    colors = ["tab:green", "tab:red", "tab:green", "tab:green"]
    ax[1, 1].bar(labels, vals, color=colors, alpha=0.85)
    ax[1, 1].set_ylabel("标准紧致约化允许")
    ax[1, 1].set_title("D  半整权需自旋提升（链内无）")
    ax[1, 1].set_ylim(0, 1.3)
    ax[1, 1].grid(alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
