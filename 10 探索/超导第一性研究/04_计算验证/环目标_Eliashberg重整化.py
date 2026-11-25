# -*- coding: utf-8 -*-
"""
Eliashberg 质量增强 1+lambda 缺失——P4 根因的数值核对（非拟合）。

四面板：
A BCS 裸指数 e^{-1/lam} vs Eliashberg e^{-(1+lam)/lam}（差 e^{-1} 因子）；
B 8 元素两口径反解 lambda（CQM 13型 vs Eliashberg 37型）；
C E/C 比值 vs 1+lambda_C（质量增强定性特征）；
D P4 根因分解示意。
"""

import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "环目标_Eliashberg重整化.png")
OUT_CSV = os.path.join(HERE, "环目标_Eliashberg重整化.csv")

PREF37 = 1.13 / math.sqrt(math.e)

# Webb 2015 Table III; lam_C from CQM 第53轮反解; lam_E from Eq37 反解（见推导卡表）
DATA = [
    ("Al", 1.18, 428, 0.176, 0.221),
    ("Nb", 9.25, 275, 0.314, 0.496),
    ("Pb", 7.2, 105, 0.405, 0.768),
    ("Sn", 3.7, 200, 0.265, 0.383),
    ("Cd", 0.52, 209, 0.173, 0.217),
    ("Ta", 4.4, 240, 0.264, 0.382),
    ("V", 5.4, 380, 0.247, 0.348),
    ("In", 3.4, 108, 0.308, 0.481),
]


def main():
    rows = []
    lams = np.linspace(0.05, 0.6, 200)
    bcs = np.exp(-1 / lams)
    el = np.exp(-(1 + lams) / lams)
    print(f"A 重整化因子: exp(-(1+lam)/lam) = exp(-1/lam)*e^-1 (e^-1={math.exp(-1):.4f})")
    for l, b, e in zip(lams[::50], bcs[::50], el[::50]):
        rows.append(("exponent", l, b, e, np.nan))

    print("\nB 8 元素两口径反解 lambda")
    print(f"{'el':<4}{'lam_CQM':>9}{'lam_E37':>9}{'E/C':>8}{'1+C':>7}")
    names = [d[0] for d in DATA]
    lc = np.array([d[3] for d in DATA])
    le = np.array([d[4] for d in DATA])
    for name, _, _, c, e in DATA:
        print(f"{name:<4}{c:>9.3f}{e:>9.3f}{e/c:>8.3f}{1+c:>7.3f}")
        rows.append(("inverse", c, e, e / c, name))

    # C E/C vs 1+lambda_C
    print("\nC E/C 单调随 lambda_C 增（质量增强定性特征）")
    ratios = le / lc
    for name, r in zip(names, ratios):
        rows.append(("ratio", 0, r, np.nan, name))

    # D P4 根因
    print("D P4 根因: 缺 1+lam 重整化(主) + 缺 mu*(次) + 对数矩口径(次)")
    for k, note in enumerate(["1+lam 重整化", "mu* 缺失", "对数矩 e^-1/3"]):
        rows.append(("cause", k, 1, np.nan, note))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.4, 9.6))

    ax[0, 0].semilogy(lams, bcs, lw=2.4, color="tab:blue", label="BCS $e^{-1/\\lambda}$")
    ax[0, 0].semilogy(lams, el, lw=2.4, color="tab:red",
                      label="Eliashberg $e^{-(1+\\lambda)/\\lambda}$")
    ax[0, 0].set_xlabel(r"$\lambda$")
    ax[0, 0].set_ylabel("指数因子")
    ax[0, 0].set_title("A  质量增强把 Tc 压低 $e^{-1}$ 倍")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3, which="both")

    ax[0, 1].plot(lc, le, "o", color="tab:green", ms=6)
    ax[0, 1].plot([0, 0.9], [0, 0.9], "--", color="0.5", lw=1.2, label="相等线")
    for x, y, t in zip(lc, le, names):
        ax[0, 1].annotate(t, (x, y), fontsize=8)
    ax[0, 1].set_xlabel(r"$\lambda_{CQM}$ (13型)")
    ax[0, 1].set_ylabel(r"$\lambda_{E37}$ (37型)")
    ax[0, 1].set_title("B  两口径反解（Eliashberg 系统性更大）")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    ax[1, 0].plot(lc, ratios, "o-", lw=2.0, color="tab:purple")
    ax[1, 0].plot(lc, 1 + lc, "s--", lw=1.8, color="tab:orange", label=r"$1+\lambda_{CQM}$")
    ax[1, 0].set_xlabel(r"$\lambda_{CQM}$")
    ax[1, 0].set_ylabel("比值")
    ax[1, 0].set_title("C  E/C 随耦合增（质量增强定性特征）")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3)

    causes = ["1+$\\lambda$ 重整化", "$\\mu^*$ 缺失", "对数矩 $e^{-1/3}$"]
    ax[1, 1].barh(causes, [3, 2, 1], color=["tab:red", "tab:orange", "tab:olive"],
                  alpha=0.85)
    ax[1, 1].set_xlabel("根因权重（示意）")
    ax[1, 1].set_title("D  P4 根因分解")
    ax[1, 1].grid(alpha=0.3, axis="x")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
