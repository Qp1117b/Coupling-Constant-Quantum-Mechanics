# -*- coding: utf-8 -*-
"""
环 22／临-17 冻结偏移余边缘的数值核对。

1. 随机 a_i 生成 c_ij，核对反对称与三环和乐残差；
2. 向量化 c 的秩 = N-1；
3. R_n = exp(-gamma_n^2 sigma_a^2/2) 的高斯衰减；
4. 可读窗口 gamma_* ~ 1/sigma_a。

由 (17.1)-(17.3) 直接计算，无拟合。
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
OUT_PNG = os.path.join(HERE, "环22_临17_冻结偏移.png")
OUT_CSV = os.path.join(HERE, "环22_临17_冻结偏移.csv")

GAMMAS = np.array([14.134725, 21.022040, 25.010858, 30.424876, 32.935062])


def main():
    rng = np.random.default_rng(20261122)
    N = 6
    a = rng.normal(size=N)
    c = a[:, None] - a[None, :]
    rows = []

    anti = np.abs(c + c.T).max()
    cyclo = 0.0
    for i in range(N):
        for j in range(N):
            for k in range(N):
                cyclo = max(cyclo, abs(c[i, j] + c[j, k] - c[i, k]))
    print(f"反对称残差={anti:.3e}, 三环和乐残差={cyclo:.3e}")
    rows.append(("cocycle", N, float(anti), float(cyclo), np.nan))

    rows_c, cols_c = [], []
    for i in range(N):
        for j in range(N):
            if i != j:
                row = np.zeros(N)
                row[i] = 1.0
                row[j] = -1.0
                rows_c.append(row)
                cols_c.append(c[i, j])
    A = np.array(rows_c)
    vec_c = np.array(cols_c)
    rank = np.linalg.matrix_rank(A)
    resid = np.max(np.abs(A @ a - vec_c))
    print(f"映射 a->c 的矩阵秩={rank} (target N-1={N-1}), 生成残差={resid:.3e}")
    rows.append(("rank", N, float(rank), float(N - 1), float(resid)))

    print("\nR_n 高斯衰减")
    for sa in (0.01, 0.02, 0.05):
        R = np.exp(-(GAMMAS * sa) ** 2 / 2)
        for g, r in zip(GAMMAS, R):
            rows.append(("coherence", sa, float(g), float(r), np.nan))
        print(f"  sigma_a={sa}: R(gamma_1)={R[0]:.6f}, R(gamma_5)={R[-1]:.3e}")
    for sa in (0.01, 0.02, 0.05):
        print(f"  gamma_* ~ 1/sigma_a = {1/sa:.1f}")

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A c matrix
    im = ax[0, 0].imshow(c, cmap="RdBu_r")
    ax[0, 0].set_title(r"A  $c_{ij}=a_i-a_j$（$N=6$）")
    fig.colorbar(im, ax=ax[0, 0], fraction=0.046)

    # B residue
    ax[0, 1].bar(["反对称", "三环和乐"], [anti, cyclo], color=["tab:green", "tab:blue"], alpha=0.85)
    ax[0, 1].set_yscale("log")
    ax[0, 1].set_title("B  余边缘残差（数值零）")
    ax[0, 1].grid(alpha=0.3, axis="y")

    # C coherence
    g = np.linspace(0, 40, 400)
    for sa in (0.01, 0.02, 0.05):
        ax[1, 0].plot(g, np.exp(-(g * sa) ** 2 / 2), lw=2.0, label=rf"$\sigma_a={sa}$")
    ax[1, 0].set_xlabel(r"$\gamma_n$")
    ax[1, 0].set_ylabel(r"$R_n$")
    ax[1, 0].set_title(r"C  $R_n=\exp(-\gamma_n^2\sigma_a^2/2)$")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3)

    # D window
    sas = np.array([0.005, 0.01, 0.02, 0.05, 0.1])
    ax[1, 1].loglog(sas, 1 / sas, "o-", lw=2.2, color="tab:purple")
    ax[1, 1].set_xlabel(r"$\sigma_a$")
    ax[1, 1].set_ylabel(r"$\gamma_*\sim1/\sigma_a$")
    ax[1, 1].set_title("D  可读窗口宽度")
    ax[1, 1].grid(alpha=0.3, which="both")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
