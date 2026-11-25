# -*- coding: utf-8 -*-
"""
环 4／`W-3prime` 的数值核对：亏角映射的核。

1. 球面三角化计数 E=3V-6，核下界 dim>=E-V=2V-6；
2. 一般四面体的显式线性化 Jacobian (4x6)，数值秩与核维数；
3. 核向量 x：||Jx||≈0 而 ||x||>0。

计数与 Jacobian 直接计算，无拟合。
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
OUT_PNG = os.path.join(HERE, "环04_W3prime简正模.png")
OUT_CSV = os.path.join(HERE, "环04_W3prime简正模.csv")

EDGES = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
FACES = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]


def edge_index(i, j):
    a, b = min(i, j), max(i, j)
    return EDGES.index((a, b))


def deficits(l, faces=FACES):
    """顶点亏角：2*pi 减去各面在该顶点的内角之和。"""
    out = np.zeros(4)
    for (i, j, k) in faces:
        lij, lik, ljk = l[edge_index(i, j)], l[edge_index(i, k)], l[edge_index(j, k)]
        for v, a, b, c in ((i, lij, lik, ljk), (j, lij, ljk, lik), (k, lik, ljk, lij)):
            cosv = (a * a + b * b - c * c) / (2 * a * b)
            cosv = np.clip(cosv, -1.0, 1.0)
            out[v] -= np.arccos(cosv)
    return out + 2 * np.pi


def null_space(A, tol=1e-8):
    _, s, vh = np.linalg.svd(A, full_matrices=True)
    rank = int(np.sum(s > tol))
    return vh[rank:].T, rank


def main():
    rows = []

    # ---- 计数
    print("球面三角化计数（E=3V-6，核下界 2V-6）")
    vs = np.arange(4, 13)
    bounds = []
    for V in vs:
        E = 3 * V - 6
        bound = E - V
        bounds.append(bound)
        print(f"  V={V:2d}  E={E:2d}  dim ker >= {bound:2d}")
        rows.append(("count", V, E, bound, np.nan))

    # ---- 四面体 Jacobian
    pts = np.array([[0.0, 0.0, 0.0], [1.0, 0.2, 0.1], [0.3, 1.1, -0.2],
                    [0.2, -0.1, 0.9]])
    l0 = np.array([np.linalg.norm(pts[i] - pts[j]) for i, j in EDGES])
    h = 1e-6
    J = np.zeros((4, 6))
    for col in range(6):
        lp = l0.copy()
        lm = l0.copy()
        lp[col] += h
        lm[col] -= h
        J[:, col] = (deficits(lp) - deficits(lm)) / (2 * h)
    rank_t = int(np.linalg.matrix_rank(J))
    N, _ = null_space(J)
    kdim = 6 - rank_t
    print(f"\n四面体 Jacobian 秩={rank_t}, 核维数={kdim}, 下界=2")
    print("  奇异值:", np.round(np.linalg.svd(J)[1], 6))
    rows.append(("tetra_rank", rank_t, 6, kdim, np.nan))

    # 核向量验证
    x = N[:, 0] if N.shape[1] else np.zeros(6)
    x = x / np.linalg.norm(x)
    resid = np.linalg.norm(J @ x)
    print(f"  核向量 x: ||x||=1, ||Jx||={resid:.3e}")
    print("  x =", np.round(x, 6))
    rows.append(("null_vector", 0, float(np.linalg.norm(x)), float(resid), np.nan))

    # ---- CSV
    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    # ---- 画图
    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A 计数
    ax[0, 0].plot(vs, 3 * vs - 6, "o-", lw=2.0, color="tab:blue", label=r"$E=3V-6$")
    ax[0, 0].plot(vs, vs, "s--", lw=1.8, color="tab:red", label=r"$V$（单射所需上界）")
    ax[0, 0].fill_between(vs, vs, 3 * vs - 6, color="tab:orange", alpha=0.2)
    ax[0, 0].set_xlabel(r"$V$")
    ax[0, 0].set_ylabel("边数 / 顶点数")
    ax[0, 0].set_title("A  E > V => 亏角映射不可能单射")
    ax[0, 0].legend(fontsize=9)
    ax[0, 0].grid(alpha=0.3)

    # B 下界
    ax[0, 1].bar(vs, bounds, color="tab:green", alpha=0.8)
    for V, b in zip(vs, bounds):
        ax[0, 1].text(V, b + 0.2, str(b), ha="center", fontsize=8)
    ax[0, 1].set_xlabel(r"$V$")
    ax[0, 1].set_ylabel(r"$\dim\ker \geq 2V-6$")
    ax[0, 1].set_title("B  核的最小维数")
    ax[0, 1].grid(alpha=0.3, axis="y")

    # C 四面体奇异值
    sv = np.linalg.svd(J)[1]
    ax[1, 0].bar(np.arange(1, len(sv) + 1), sv, color="tab:purple", alpha=0.85)
    ax[1, 0].axhline(0.0, color="0.35", lw=1.0)
    ax[1, 0].set_xlabel("奇异值编号")
    ax[1, 0].set_ylabel(r"$\sigma$")
    ax[1, 0].set_title(rf"C  四面体 $4\times6$ Jacobian（秩={rank_t}）")
    ax[1, 0].grid(alpha=0.3, axis="y")

    # D 核向量效果
    ax[1, 1].bar(["||x||（边长扰动）", "||Jx||（亏角变化）"],
                 [np.linalg.norm(x), resid], color=["tab:orange", "tab:blue"], alpha=0.85)
    ax[1, 1].set_yscale("log")
    ax[1, 1].set_title("D  核模：边长变了，亏角没变")
    ax[1, 1].grid(alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
