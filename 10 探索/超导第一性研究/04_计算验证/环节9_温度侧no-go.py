# -*- coding: utf-8 -*-
"""
R7: 温度侧 no-go——链唯一热核 coth（玻色）≠ 隙方程热核 tanh（费米）。
只检验不等式/互倒数/格点不交，不拟合。仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/环节9_温度侧no-go.py"
"""
import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))


def assertions():
    out = {}
    x = np.linspace(0.05, 5, 2000)
    tanhx = np.tanh(x)
    cothx = 1 / tanhx

    out["coth_minus_tanh_min"] = float(np.min(cothx - tanhx))
    out["coth_always_gt_one"] = bool(np.all(cothx > 1))
    out["tanh_always_lt_one"] = bool(np.all(tanhx < 1))
    out["reciprocal_max_dev"] = float(np.max(np.abs(cothx * tanhx - 1)))

    # 1+2nB 与 1-2nF 的差（xi>0）
    xi = np.linspace(0.05, 5, 2000)
    nb = 1 / (np.exp(xi) - 1)
    nf = 1 / (np.exp(xi) + 1)
    fB = 1 + 2 * nb
    fF = 1 - 2 * nf
    out["fB_gt_fF_always"] = bool(np.all(fB > fF))
    out["fB_minus_fF_min"] = float(np.min(fB - fF))

    # Matsubara 格点不交：2n != 2m+1（有限范围核对）
    ns = np.arange(-50, 51)
    evens = set(2 * ns)
    odds = {2 * m + 1 for m in ns}
    out["grids_intersection_size"] = len(evens & odds)
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # (a) coth vs tanh
    ax = axes[0, 0]
    x = np.linspace(0.05, 5, 600)
    ax.plot(x, 1 / np.tanh(x), "b-", lw=2, label=r"链热核 $\coth x=1+2n_B$")
    ax.plot(x, np.tanh(x), "r-", lw=2, label=r"隙方程热核 $\tanh x=1-2n_F$")
    ax.axhline(1, color="k", ls="--", lw=1)
    ax.set_xlabel(r"$x=\hbar\omega/2k_BT$")
    ax.set_ylabel(r"热核值")
    ax.set_title("(a) coth > 1 > tanh：永不相交")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (b) 互倒数
    ax = axes[0, 1]
    ax.plot(x, (1 / np.tanh(x)) * np.tanh(x), "g-", lw=2)
    ax.axhline(1, color="k", ls="--", lw=1)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$\coth x\cdot\tanh x$")
    ax.set_title("(b) 互倒数恒为 1（统计对偶，非同一）")
    ax.grid(alpha=0.3)

    # (c) 1+2nB 与 1-2nF 的温度演化
    ax = axes[1, 0]
    xi = np.linspace(0.05, 5, 600)
    ax.plot(xi, 1 + 2 / (np.exp(xi) - 1), "b-", lw=2, label=r"$1+2n_B=\coth$")
    ax.plot(xi, 1 - 2 / (np.exp(xi) + 1), "r-", lw=2, label=r"$1-2n_F=\tanh$")
    ax.axhline(1, color="k", ls="--", lw=1)
    ax.set_xlabel(r"$\beta\xi$")
    ax.set_ylabel(r"热因子")
    ax.set_title("(c) 链入口在上、隙方程核在下")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (d) Matsubara 格点：整数 vs 半整数
    ax = axes[1, 1]
    n = np.arange(-5, 6)
    ax.scatter(2 * n, np.zeros_like(n), c="blue", s=70, label=r"玻色 $2n\pi/\beta$")
    ax.scatter(2 * n + 1, np.zeros_like(n), c="red", s=70, marker="x", label=r"费米 $(2n+1)\pi/\beta$")
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlabel(r"$\omega_n\beta/\pi$")
    ax.set_yticks([])
    ax.set_title("(d) 两套 Matsubara 格点无交集")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, axis="x")

    fig.suptitle("R7: 环节⑨ 温度侧 no-go（玻色 coth ≠ 费米 tanh，无拟合）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "环节9_温度侧no-go.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R7 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "环节9_温度侧no-go_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
