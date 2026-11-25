# -*- coding: utf-8 -*-
"""
环 13／临-11 自平均标度的数值核对。

1. 独立样本均值标准误 ~ sigma/sqrt(n)（双对数斜率 -0.5）；
2. 正相关样本（c_bar=0.1）的方差平台 -> c_bar；
3. 相对方差 R：独立 -> 0，相关 -> c_bar/mu^2；
4. 与临-24 的相位相干 M^{-1/2} 对照（同斜率、不同对象）。

由 (11A.1)-(11A.4) 直接计算，无拟合。
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
OUT_PNG = os.path.join(HERE, "环13_临11自平均.png")
OUT_CSV = os.path.join(HERE, "环13_临11自平均.csv")

SIGMA2 = 1.0
CBAR = 0.1
MU = 1.0


def var_indep(n):
    return SIGMA2 / n


def var_corr(n):
    return SIGMA2 / n + (n - 1) / n * CBAR


def main():
    rows = []
    ns = np.logspace(0, 4, 200)
    print("方差与标准误")
    for n in (10, 100, 1000, 10000):
        vi, vc = var_indep(n), var_corr(n)
        print(f"  n={n:6d}: Var_ind={vi:.6f}, stderr={np.sqrt(vi):.6f}, Var_corr={vc:.6f}")
        rows.append(("variance", n, vi, vc, np.nan))
    slope = np.polyfit(np.log(ns), np.log(np.sqrt(var_indep(ns))), 1)[0]
    print(f"  标准误双对数斜率={slope:.4f} (target -0.5)")

    for n in (10, 100, 1000, 10000):
        Ri = var_indep(n) / MU ** 2
        Rc = var_corr(n) / MU ** 2
        rows.append(("relative", n, Ri, Rc, np.nan))
    print(f"  相关极限 Var_corr(1e4)={var_corr(1e4):.6f} -> c_bar={CBAR}")

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A stderr
    ax[0, 0].loglog(ns, np.sqrt(var_indep(ns)), lw=2.2, color="tab:blue",
                    label=rf"斜率 ${slope:.2f}$")
    ax[0, 0].loglog(ns, 1 / np.sqrt(ns), "--", color="tab:red", label=r"$n^{-1/2}$")
    ax[0, 0].set_xlabel(r"$n=|D_i|$")
    ax[0, 0].set_ylabel(r"标准误")
    ax[0, 0].set_title("A  独立样本：$|D_i|^{-1/2}$ 标度")
    ax[0, 0].legend(fontsize=9)
    ax[0, 0].grid(alpha=0.3, which="both")

    # B variance with correlations
    ax[0, 1].semilogx(ns, var_indep(ns), lw=2.2, color="tab:blue", label="独立")
    ax[0, 1].semilogx(ns, var_corr(ns), lw=2.2, color="tab:orange",
                      label=rf"相关 $\bar c={CBAR}$")
    ax[0, 1].axhline(CBAR, color="tab:red", ls="--", lw=1.4, label=r"极限 $\bar c$")
    ax[0, 1].set_xlabel(r"$n$")
    ax[0, 1].set_ylabel("Var(mean)")
    ax[0, 1].set_title("B  相关导致方差平台")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    # C relative variance
    ax[1, 0].loglog(ns, var_indep(ns) / MU ** 2, lw=2.2, color="tab:blue", label="独立 -> 0")
    ax[1, 0].loglog(ns, var_corr(ns) / MU ** 2, lw=2.2, color="tab:orange",
                    label="相关 -> 非零")
    ax[1, 0].set_xlabel(r"$n$")
    ax[1, 0].set_ylabel(r"相对方差 $R$")
    ax[1, 0].set_title("C  自平均判据")
    ax[1, 0].legend(fontsize=9)
    ax[1, 0].grid(alpha=0.3, which="both")

    # D compare with 临-24
    nn = np.array([10, 100, 1000, 10000])
    ax[1, 1].loglog(nn, 1 / np.sqrt(nn), "o-", lw=2.2, color="tab:purple",
                    label="抽样误差（临-11）")
    ax[1, 1].loglog(nn, 1 / np.sqrt(nn), "s--", lw=1.8, color="tab:green",
                    label="相位相干（临-24）")
    ax[1, 1].set_xlabel(r"样本数 $n$ / 活跃键数 $M$")
    ax[1, 1].set_ylabel("标度")
    ax[1, 1].set_title("D  同指数、不同对象")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3, which="both")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
