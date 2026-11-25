# -*- coding: utf-8 -*-
"""
环 6／G19 表示权量子化的数值核对。

1. cos(s*ell) 对 s=0, 1/2, 1 在 ell∈[0,2pi) 的曲线（半周期数 2s）；
2. alpha_lin = -4 pi s 的量子化阶梯（k=2s∈Z）；
3. 单值性核对：半整数格点 cos(2pi s)=±1，s=1/3 给 -0.5；
4. 绕铰链相位 exp(i s eps) 的三分支轨迹。

无拟合；由表示论公式直接计算。
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
OUT_PNG = os.path.join(HERE, "环06_G19表示权量子化.png")
OUT_CSV = os.path.join(HERE, "环06_G19表示权量子化.csv")

SS = [0.0, 0.5, 1.0]


def main():
    rows = []
    ell = np.linspace(0, 2 * np.pi, 600)
    print("单值性 cos(2 pi s)")
    for s in SS + [1 / 3]:
        c = np.cos(2 * np.pi * s)
        print(f"  s={s:.6f}: cos(2pi s)={c:.6f}")
        rows.append(("single_valued", s, c, np.nan, np.nan))

    print("\nalpha_lin 阶梯")
    for k in range(5):
        s = k / 2
        alpha = -4 * np.pi * s
        print(f"  k={k}, s={s:.1f}: alpha_lin={alpha:.6f} = -2pi*{k}")
        rows.append(("alpha", k, alpha, -2 * np.pi * k, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A cos(s ell)
    for s in SS:
        ax[0, 0].plot(ell, np.cos(s * ell), lw=2.2, label=rf"$s={s:g}$")
    ax[0, 0].set_xlabel(r"$\ell$")
    ax[0, 0].set_ylabel(r"$\cos(s\ell)$")
    ax[0, 0].set_title(r"A  几何相位因子的离散分类")
    ax[0, 0].legend(fontsize=9)
    ax[0, 0].grid(alpha=0.3)

    # B alpha ladder
    ks = np.arange(5)
    alphas = -2 * np.pi * ks
    ax[0, 1].bar(ks, alphas, color=["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"],
                 alpha=0.85)
    for k, a in zip(ks, alphas):
        ax[0, 1].text(k, a - 0.4, f"-2pi*{k}", ha="center", fontsize=8)
    ax[0, 1].set_xlabel(r"$k=2s$")
    ax[0, 1].set_ylabel(r"$\alpha_{\rm lin}$")
    ax[0, 1].set_title(r"B  $\alpha_{\rm lin}=2\pi k$，k 为整数")
    ax[0, 1].grid(alpha=0.3, axis="y")

    # C single-valued
    ss = np.linspace(0, 2, 600)
    ax[1, 0].plot(ss, np.cos(2 * np.pi * ss), lw=2.2, color="tab:blue",
                  label=r"$\cos(2\pi s)$")
    ax[1, 0].scatter(SS, [np.cos(2 * np.pi * s) for s in SS], color="tab:green",
                     s=80, zorder=5, label="半整数格点")
    ax[1, 0].scatter([1 / 3], [np.cos(2 * np.pi / 3)], color="tab:red", s=90,
                     zorder=5, label="s=1/3（排除）")
    ax[1, 0].axhline(1, color="0.5", ls=":")
    ax[1, 0].axhline(-1, color="0.5", ls=":")
    ax[1, 0].set_xlabel(r"$s$")
    ax[1, 0].set_title(r"C  单值性只容半整数")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3)

    # D phase winding
    eps = np.linspace(0, 2 * np.pi, 600)
    for s in SS[1:]:
        ax[1, 1].plot(eps, np.cos(s * eps), lw=2.0, label=rf"$s={s:g}$")
    ax[1, 1].set_xlabel(r"亏角 $\varepsilon$")
    ax[1, 1].set_ylabel(r"$e^{is\varepsilon}$ 的实部")
    ax[1, 1].set_title(r"D  绕铰链相位按 $\pi$ 跳变")
    ax[1, 1].legend(fontsize=9)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
