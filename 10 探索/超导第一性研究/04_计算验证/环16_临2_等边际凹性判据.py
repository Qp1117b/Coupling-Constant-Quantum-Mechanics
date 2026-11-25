# -*- coding: utf-8 -*-
"""
环 16／临-2 等边际凹性判据的数值核对。

1. (16.A1) 饱和型、(16.A2) 幂律型的 lambda(n) 与边际 m(n)；
2. 单步转移增益 m(i)-m(j-1) 扫描：凹情形全正、凸情形全负；
3. 凹分配（内点均等）vs 凸分配（角点赢家通吃）；
4. 影子价格 mu 随容量 n_eff 下降。

由 (2.3)-(2.5) 直接计算，无拟合。
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
OUT_PNG = os.path.join(HERE, "环16_临2_等边际凹性判据.png")
OUT_CSV = os.path.join(HERE, "环16_临2_等边际凹性判据.csv")

LINF, N0 = 1.0, 2.0
LAM0, BETA = 1.0, 0.5
BETA_CONVEX = 1.5


def lam_sat(n):
    return LINF * (1 - np.exp(-np.asarray(n, dtype=float) / N0))


def lam_pow(n, beta):
    return LAM0 * np.asarray(n, dtype=float) ** beta


def marg(f, n):
    return f(n + 1) - f(n)


def main():
    rows = []
    ns = np.arange(0, 21)

    # A 两候选的 lambda 与边际
    ms_sat = marg(lam_sat, ns)
    ms_pow = marg(lambda n: lam_pow(n, BETA), ns)
    print("A 边际递减核对")
    for n in (0, 5, 10, 20):
        print(f"  n={n}: m_sat={ms_sat[n]:.6f}, m_pow={ms_pow[n]:.6f}")
        rows.append(("marg", n, float(ms_sat[n]), float(ms_pow[n]), np.nan))
    print(f"  m_sat 严格递减: {bool(np.all(np.diff(ms_sat) < 0))}")
    print(f"  m_pow 严格递减: {bool(np.all(np.diff(ms_pow) < -1e-12))}")

    # B 转移增益 m(i)-m(j-1) 扫描
    print("\nB 单步转移增益")
    I, J = np.meshgrid(np.arange(0, 8), np.arange(2, 10))
    mask = I + 1 < J
    gain_concave = np.where(mask, marg(lam_sat, I) - marg(lam_sat, J - 1), np.nan)
    gain_convex = np.where(mask,
                           marg(lambda n: lam_pow(n, BETA_CONVEX), I)
                           - marg(lambda n: lam_pow(n, BETA_CONVEX), J - 1),
                           np.nan)
    valid_c = gain_concave[~np.isnan(gain_concave)]
    valid_v = gain_convex[~np.isnan(gain_convex)]
    print(f"  凹情形增益最小值={valid_c.min():.6f}（应 >0）")
    print(f"  凸情形增益最大值={valid_v.max():.6f}（应 <0）")
    for a, b, c, d in zip(I.ravel()[::12], J.ravel()[::12],
                          gain_concave.ravel()[::12], gain_convex.ravel()[::12]):
        rows.append(("transfer", int(a), int(b), float(c) if not np.isnan(c) else np.nan,
                     float(d) if not np.isnan(d) else np.nan))

    # C 凹 vs 凸分配（总预算 12，三域）
    print("\nC 分配模式")
    total, K = 12, 3
    split_even = [total // K] * K
    split_corner = [total] + [0] * (K - 1)
    tot_even = float(np.sum(lam_pow(split_even, BETA)))
    tot_corner = float(np.sum(lam_pow(split_corner, BETA)))
    tot_even_v = float(np.sum(lam_pow(split_even, BETA_CONVEX)))
    tot_corner_v = float(np.sum(lam_pow(split_corner, BETA_CONVEX)))
    print(f"  凹(beta=0.5): 均等={tot_even:.4f} > 角点={tot_corner:.4f}")
    print(f"  凸(beta=1.5): 均等={tot_even_v:.4f} < 角点={tot_corner_v:.4f}")
    for k in range(K):
        rows.append(("alloc", k, split_even[k], split_corner[k], np.nan))

    # D 影子价格 mu 随 n_eff 下降
    print("\nD 影子价格")
    neffs = np.linspace(1, 100, 200)
    # 均等分配 n_k = neff/K，总 lambda = K*linf*(1-exp(-neff/(K*n0)))
    # mu = d(total)/d(neff) = linf*exp(-neff/(K*n0))
    mus = LINF * np.exp(-neffs / (K * N0))
    for x in (1, 10, 50, 100):
        mu = LINF * np.exp(-x / (K * N0))
        print(f"  n_eff={x}: mu={mu:.6f}")
        rows.append(("shadow", x, mu, np.nan, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.4))

    ax[0, 0].plot(ns, lam_sat(ns), lw=2.2, label=r"$\lambda^{(1)}$ 饱和型")
    ax[0, 0].plot(ns, lam_pow(ns, BETA), lw=2.2, label=r"$\lambda^{(2)}$ 幂律型")
    ax[0, 0].set_xlabel(r"$n$")
    ax[0, 0].set_ylabel(r"$\lambda(n)$")
    ax[0, 0].set_title("A  两候选：函数值递增")
    ax[0, 0].legend(fontsize=9)
    ax[0, 0].grid(alpha=0.3)

    ax2 = ax[0, 1].twinx()
    ax[0, 1].plot(ns[1:], ms_sat[1:], lw=2.2, color="tab:blue", label=r"$m^{(1)}$")
    ax2.plot(ns[1:], ms_pow[1:], lw=2.2, color="tab:orange", label=r"$m^{(2)}$")
    ax[0, 1].set_xlabel(r"$n$")
    ax[0, 1].set_ylabel(r"$m^{(1)}$", color="tab:blue")
    ax2.set_ylabel(r"$m^{(2)}$", color="tab:orange")
    ax[0, 1].set_title("B  离散边际：两候选都递减")
    ax[0, 1].grid(alpha=0.3)

    x = np.arange(K)
    ax[1, 0].bar(x - 0.18, split_even, 0.36, label="凹：均等（内点）",
                 color="tab:blue", alpha=0.85)
    ax[1, 0].bar(x + 0.18, split_corner, 0.36, label="凸：角点（赢家通吃）",
                 color="tab:red", alpha=0.85)
    ax[1, 0].set_xlabel("域编号")
    ax[1, 0].set_ylabel(r"$n_k$")
    ax[1, 0].set_title("C  凹/凸决定分配模式")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3, axis="y")

    ax[1, 1].plot(neffs, mus, lw=2.4, color="tab:green")
    ax[1, 1].set_xlabel(r"容量 $n_{\rm eff}$")
    ax[1, 1].set_ylabel(r"影子价格 $\mu$")
    ax[1, 1].set_title("D  容量越充裕，等边际乘子越低")
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
