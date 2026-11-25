# -*- coding: utf-8 -*-
"""
环 8／`M5` 齐次线性化的数值核对。

1. 四个代表性 D 矩阵的秩、零化度、基；
2. dim ker = 1 例：同一形状 g 的三个尺度倍（形状唯一、尺度自由）；
3. D=0 例：f=x 与 f=x^3 两个不同形状都满足；
4. 残差 |D f| 核对。

D 由有符号邻居计数规则 (M5.1) 直接构造，无拟合参数。
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
OUT_PNG = os.path.join(HERE, "环08_M5齐次线性.png")
OUT_CSV = os.path.join(HERE, "环08_M5齐次线性.csv")

CASES = {
    "D=0 (中心对称)": np.zeros((1, 4)),
    "D=[1,1,1] (非对称3价)": np.array([[1.0, 1.0, 1.0]]),
    "rank2/m3 (形状唯一)": np.array([[1.0, 1.0, 0.0], [1.0, 0.0, 1.0]]),
    "rank3/m3 (仅零解)": np.array([[1.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0]]),
}


def null_space(A, tol=1e-10):
    """SVD 零空间基。"""
    _, s, vh = np.linalg.svd(A, full_matrices=True)
    m = A.shape[1]
    ns = (s.shape[0], m)
    # 用 vh 的后几行
    rank = int(np.sum(s > tol))
    return vh[rank:].T, rank


def main():
    rows = []
    kerdims = []
    print("案例                             秩   m   dim ker")
    for name, D in CASES.items():
        m = D.shape[1]
        N, rank = null_space(D)
        k = m - rank
        kerdims.append(k)
        print(f"  {name:32s} {rank:2d}  {m:2d}  {k:2d}")
        rows.append((name, rank, m, k, np.nan))
        if N.shape[1]:
            rows.append((name + " 基", 0, 0, 0, np.linalg.norm(N[:, 0])))

    # ---- dim ker = 1 例的形状与尺度
    D2 = CASES["rank2/m3 (形状唯一)"]
    N2, _ = null_space(D2)
    g = N2[:, 0]
    if g[0] < 0:
        g = -g
    print("\n形状唯一例的核基 g =", np.round(g, 6))
    print("  |D g| =", np.linalg.norm(D2 @ g))
    alphas = np.linspace(-1, 2, 200)
    tt = np.array([1.0, 2.0, 3.0])

    # ---- D=0 例：x 与 x^3 都解
    xs = np.linspace(-2, 2, 400)
    print("\nD=0 例：两个不同奇函数在对称壳层上均满足")
    print("  x  在 a,-a,b,-b 上的行和 =", sum(f(x) for f in [lambda z: z] for x in [0.8, -0.8, 1.3, -1.3]))
    print("  x^3 的行和 =", sum(x ** 3 for x in [0.8, -0.8, 1.3, -1.3]))

    # ---- 残差
    f_test = np.array([1.0, -0.5, 2.0, -1.0])
    for name, D in CASES.items():
        if D.shape[1] == f_test.shape[0]:
            res = np.linalg.norm(D @ f_test)
            rows.append((name + " 残差", 0, 0, 0, res))

    # ---- CSV
    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "rank", "m", "dim_ker", "extra"])
        wr.writerows(rows)

    # ---- 画图
    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A: 零化度
    names = ["D=0", "[1,1,1]", "rank2/m3", "rank3/m3"]
    ax[0, 0].bar(names, kerdims, color=["tab:green", "tab:orange", "tab:blue", "tab:red"], alpha=0.85)
    for i, k in enumerate(kerdims):
        lab = "仅零解" if k == 0 else ("形状唯一" if k == 1 else "形状不唯一")
        ax[0, 0].text(i, k + 0.08, f"dim={k}\n{lab}", ha="center", fontsize=8)
    ax[0, 0].set_ylabel(r"$\dim\ker D$")
    ax[0, 0].set_title("A  四例的零化度（C1=1 的解族维数）")
    ax[0, 0].set_ylim(0, 5.2)
    ax[0, 0].grid(alpha=0.3, axis="y")

    # B: 形状唯一例的尺度倍
    alphas_idx = np.arange(1, len(g) + 1)
    for c in (1.0, 2.0, -0.5):
        ax[0, 1].plot(alphas_idx, c * g, "o-", lw=1.8, label=f"c={c:g}")
    ax[0, 1].plot(alphas_idx, np.zeros_like(alphas_idx), color="0.35", lw=1.0)
    ax[0, 1].set_xlabel("alpha 编号")
    ax[0, 1].set_ylabel(r"$f(\alpha)$")
    ax[0, 1].set_title(r"B  $\dim\ker=1$：形状相同、尺度自由")
    ax[0, 1].legend(fontsize=9)
    ax[0, 1].grid(alpha=0.3)

    # C: D=0 例两个不同形状
    ax[1, 0].plot(xs, xs, lw=2.0, color="tab:blue", label=r"$f(x)=x$")
    ax[1, 0].plot(xs, xs ** 3, lw=2.0, color="tab:orange", label=r"$f(x)=x^3$")
    ax[1, 0].axhline(0.0, color="0.35", lw=0.9)
    ax[1, 0].set_xlabel(r"$x$")
    ax[1, 0].set_ylabel(r"$f(x)$")
    ax[1, 0].set_title(r"C  $D=0$：两个不同奇函数都是解")
    ax[1, 0].legend(fontsize=9)
    ax[1, 0].grid(alpha=0.3)

    # D: 几何示意（有符号计数）
    shell = np.array([0.8, -0.8, 1.3, -1.3])
    colors = ["tab:blue" if v > 0 else "tab:orange" for v in shell]
    ax[1, 1].bar(np.arange(4), shell, color=colors, alpha=0.85)
    ax[1, 1].axhline(0.0, color="0.35", lw=1.0)
    ax[1, 1].set_xticks(np.arange(4))
    ax[1, 1].set_xticklabels([r"$+\alpha$", r"$-\alpha$", r"$+\beta$", r"$-\beta$"])
    ax[1, 1].set_ylabel(r"边值 $\lambda$")
    ax[1, 1].set_title("D  中心对称壳层：成对抵消 => D=0")
    ax[1, 1].grid(alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
