# -*- coding: utf-8 -*-
"""
环 26／临-24 全对归一的数值核对。

1. 随机相位 R ~ M^{-1/2}（双对数斜率 -0.5）；
2. 活跃数归一 vs 总数归一（M/N 稀释）；
3. R∈[0,1] 数值核对；
4. 全相干给 R=1。

由 (24.1)-(24.3) 直接计算，无拟合。
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
OUT_PNG = os.path.join(HERE, "环26_临24_全对归一.png")
OUT_CSV = os.path.join(HERE, "环26_临24_全对归一.csv")


def coherence(M, rng, trials=200):
    vals = []
    for _ in range(trials):
        ph = rng.uniform(0, 2 * np.pi, M)
        z = np.exp(1j * ph)
        vals.append(abs(z.sum()) / M)
    return np.array(vals)


def main():
    rng = np.random.default_rng(20261122)
    rows = []
    sizes = np.array([4, 9, 16, 25, 49, 100, 225, 400])
    means = np.array([coherence(int(m), rng).mean() for m in sizes])
    print("随机相位 R 的均值")
    for m, v in zip(sizes, means):
        print(f"  M={m:4d}: R_mean={v:.6f}, 1/sqrt(M)={1/np.sqrt(m):.6f}")
        rows.append(("random", int(m), float(v), float(1 / np.sqrt(m)), np.nan))
    slope = np.polyfit(np.log(sizes), np.log(means), 1)[0]
    print(f"  双对数斜率={slope:.4f} (target -0.5)")

    print("\n活跃数归一 vs 总数归一 (N=400)")
    N = 400
    for M in (50, 100, 200, 400):
        r = coherence(M, rng, 50).mean()
        rtot = r * M / N
        print(f"  M={M}: R_active={r:.4f}, R_total={rtot:.4f}, 稀释因子={M/N:.3f}")
        rows.append(("dilution", M, float(r), float(rtot), M / N))

    vals = coherence(64, rng, 500)
    print(f"\nR 范围: [{vals.min():.6f}, {vals.max():.6f}]")
    rows.append(("range", 64, float(vals.min()), float(vals.max()), np.nan))
    rows.append(("full_coherence", 64, 1.0, 1.0, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    ax[0, 0].loglog(sizes, means, "o-", lw=2.0, color="tab:blue",
                    label=rf"实验斜率 ${slope:.2f}$")
    ax[0, 0].loglog(sizes, 1 / np.sqrt(sizes), "--", color="tab:red",
                    label=r"$M^{-1/2}$")
    ax[0, 0].set_xlabel("M（活跃键数）")
    ax[0, 0].set_ylabel("R 的均值")
    ax[0, 0].set_title("A  随机相位给出的有限尺寸标度")
    ax[0, 0].legend(fontsize=9)
    ax[0, 0].grid(alpha=0.3, which="both")

    Ms = np.array([50, 100, 200, 400])
    r_act = np.array([coherence(int(m), rng, 50).mean() for m in Ms])
    ax[0, 1].plot(Ms, r_act, "o-", lw=2.2, color="tab:green", label="活跃数归一")
    ax[0, 1].plot(Ms, r_act * Ms / N, "s-", lw=2.2, color="tab:orange",
                  label="总数归一（稀释）")
    ax[0, 1].set_xlabel("M")
    ax[0, 1].set_ylabel("R")
    ax[0, 1].set_title("B  归一分母决定读数")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    ax[1, 0].hist(vals, bins=40, color="tab:purple", alpha=0.8)
    ax[1, 0].axvline(0, color="0.3", lw=1.0)
    ax[1, 0].axvline(1, color="tab:red", ls="--", lw=1.4)
    ax[1, 0].set_xlabel("R")
    ax[1, 0].set_title("C  R ∈ [0,1] 数值核对")

    ax[1, 1].bar(["全同相", "随机相位"], [1.0, vals.mean()],
                 color=["tab:green", "tab:blue"], alpha=0.85)
    ax[1, 1].set_ylabel("R")
    ax[1, 1].set_title("D  全相干给 R=1")
    ax[1, 1].set_ylim(0, 1.1)
    ax[1, 1].grid(alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
