# -*- coding: utf-8 -*-
"""
环 23／`审-13` 亏格修正的数值核对。

1. g=0,1,2,3（b=0）的环空间维数、面边界维数、余维 2g；
2. 给定 V,E 时 F 随 g 的欧拉约束；
3. 带边界 b=0,1,2,3 的余维 2g+b；
4. 精确域 (g,b)=(0,0) 的高亮。

由 (13.1)(13.2) 直接计算，无拟合。
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
OUT_PNG = os.path.join(HERE, "环23_审13_亏格修正.png")
OUT_CSV = os.path.join(HERE, "环23_审13_亏格修正.csv")


def main():
    rows = []
    V, E = 20, 45
    print("闭曲面 b=0：余维 = 2g")
    for g in (0, 1, 2, 3):
        F = 2 - 2 * g - V + E
        dimZ = E - V + 1
        dimFace = F - 1
        codim = dimZ - dimFace
        print(f"  g={g}: F={F}, dimZ={dimZ}, dimFace={dimFace}, codim={codim}")
        rows.append(("closed", g, dimZ, dimFace, codim))

    print("\n带边界：余维 = 2g + b")
    for g in (0, 1):
        for b in (0, 1, 2, 3):
            codim = 2 * g + b
            print(f"  g={g}, b={b}: codim={codim}")
            rows.append(("boundary", g + b / 10.0, codim, 2 * g, b))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A 闭曲面维数
    gs = np.arange(4)
    dimZ = E - V + 1
    dimFaces = np.array([(2 - 2 * g - V + E) - 1 for g in gs])
    codims = dimZ - dimFaces
    ax[0, 0].bar(gs - 0.18, np.full(4, dimZ), 0.36, color="tab:blue", alpha=0.85,
                 label=r"$\dim Z_1=E-V+1$")
    ax[0, 0].bar(gs + 0.18, dimFaces, 0.36, color="tab:orange", alpha=0.85,
                 label=r"面边界 $F-1$")
    for i, c in enumerate(codims):
        ax[0, 0].text(i, dimZ + 0.4, f"缺 {c}", ha="center", fontsize=9, color="tab:red")
    ax[0, 0].set_xticks(gs)
    ax[0, 0].set_xticklabels([f"g={g}" for g in gs])
    ax[0, 0].set_title("A  闭曲面：面边界比环空间少 2g 维")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3, axis="y")

    # B Euler 约束
    ax[0, 1].plot(gs, [2 - 2 * g - V + E for g in gs], "o-", lw=2.2,
                  color="tab:purple", label=r"$F=2-2g-V+E$")
    ax[0, 1].set_xlabel(r"亏格 $g$")
    ax[0, 1].set_ylabel("面数 F")
    ax[0, 1].set_title(r"B  Euler 约束 F 随 g 下降")
    ax[0, 1].legend(fontsize=9)
    ax[0, 1].grid(alpha=0.3)

    # C 带边界
    bs = np.arange(4)
    for g in (0, 1, 2):
        ax[1, 0].plot(bs, 2 * g + bs, "o-", lw=2.0, label=rf"$g={g}$: $2g+b$")
    ax[1, 0].set_xlabel("边界数 b")
    ax[1, 0].set_ylabel("余维（缺失绕数标签）")
    ax[1, 0].set_title("C  带边界曲面：余维 = 2g + b")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3)

    # D 精确域
    ax[1, 1].scatter([0], [0], s=200, color="tab:green", zorder=5)
    ax[1, 1].text(0.15, 0.2, r"精确域 $(g,b)=(0,0)$" + "\n闭球面：余维 0", fontsize=10)
    ax[1, 1].scatter([1, 2, 3], [1, 2, 3], s=90, color="tab:orange", zorder=5,
                     label="平面片 g=0, b>0")
    ax[1, 1].set_xlim(-0.5, 3.8)
    ax[1, 1].set_ylim(-0.5, 3.8)
    ax[1, 1].set_xlabel("边界数 b")
    ax[1, 1].set_ylabel("余维（g=0）")
    ax[1, 1].set_title("D  主链适用域：只有闭球面精确")
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
