# -*- coding: utf-8 -*-
"""
目标区／D1 theta 端子的数值核对。

1. 前若干零点的 T_theta,n 阶梯（C=1 示意）；
2. Gamma_n ∝ gamma_n^2 与 T_theta,n 的线性关系；
3. min 选择随零点数稳定性；
4. 统一阻尼（RH）下的退化 vs 本轮梯度族。

无拟合；由 (D1.1)-(D1.3) 直接计算。
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
OUT_PNG = os.path.join(HERE, "目标_D1_Ttheta.png")
OUT_CSV = os.path.join(HERE, "目标_D1_Ttheta.csv")

# 前 10 个非平凡零点纵坐标（数值示意）
GAMMAS = np.array([14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                   37.586178, 40.918719, 43.327073, 48.005151, 49.773832])


def main():
    rows = []
    T = GAMMAS ** 2
    print("T_theta,n = C * gamma_n^2 (C=1)")
    for n, (g, t) in enumerate(zip(GAMMAS, T), start=1):
        print(f"  n={n:2d}: gamma={g:.6f}, T_theta={t:.4f}")
        rows.append(("theta", n, float(t), float(g), np.nan))

    print(f"\nmin 稳定性：前3={T[:3].min():.4f}, 前6={T[:6].min():.4f}, 前10={T.min():.4f}")
    for k in (3, 6, 10):
        rows.append(("min_stable", k, float(T[:k].min()), float(T[0]), np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A ladder
    ns = np.arange(1, 11)
    ax[0, 0].bar(ns, T, color="tab:blue", alpha=0.85)
    ax[0, 0].plot([1], [T[0]], "o", color="tab:red", ms=8, label="min = n=1")
    ax[0, 0].set_xlabel(r"零点序号 $n$")
    ax[0, 0].set_ylabel(r"$T_{\theta,n}$（C=1）")
    ax[0, 0].set_title("A  每模一个 theta 温度")
    ax[0, 0].legend(fontsize=9)
    ax[0, 0].grid(alpha=0.3, axis="y")

    # B linear in gamma^2
    ax[0, 1].plot(GAMMAS ** 2, T, "o-", lw=2.0, color="tab:purple")
    ax[0, 1].set_xlabel(r"$\gamma_n^2$")
    ax[0, 1].set_ylabel(r"$T_{\theta,n}$")
    ax[0, 1].set_title(r"B  $T_\theta\propto\gamma_n^2$")
    ax[0, 1].grid(alpha=0.3)

    # C min stability
    ks = np.array([3, 6, 10])
    mins = np.array([T[:k].min() for k in ks])
    ax[1, 0].plot(ks, mins, "o-", lw=2.2, color="tab:green",
                  label=r"$\min_n T_{\theta,n}$")
    ax[1, 0].axhline(T[0], color="tab:red", ls="--", lw=1.4, label=r"$n=1$")
    ax[1, 0].set_xlabel("纳入的零点数")
    ax[1, 0].set_title("C  min 始终由最低零点给出")
    ax[1, 0].legend(fontsize=9)
    ax[1, 0].grid(alpha=0.3)

    # D uniform vs ladder
    x = np.arange(1, 11)
    ax[1, 1].plot(x, T / T[0], "o-", lw=2.2, color="tab:blue",
                  label="本轮梯度族")
    ax[1, 1].axhline(1.0, color="tab:red", ls="--", lw=2.0,
                     label="RH 统一阻尼（外部假设）")
    ax[1, 1].set_xlabel(r"$n$")
    ax[1, 1].set_ylabel(r"$T_{\theta,n}/T_{\theta,1}$")
    ax[1, 1].set_title("D  统一性需 RH（链内不可供给）")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
