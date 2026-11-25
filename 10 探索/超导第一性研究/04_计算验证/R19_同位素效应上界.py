# -*- coding: utf-8 -*-
"""
预注册判定 R19：同位素效应 α=1/2 上界（非拟合）
================================================
链内声速 c_s ~ M^{-1/2} -> Theta_D ~ M^{-1/2} -> Tc ~ M^{-1/2} -> alpha=1/2。
McMillan 修正 <= 1/2；实验元素 alpha <= 0.5。

复跑：python "10 探索/超导第一性研究/04_计算验证/R19_同位素效应上界.py"
"""
import csv
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))

# Webb 2015 Table 3: element -> (alpha_exp, Tc, alpha_error or None)
ISOTOPE = {
    "Hg": (0.50, 4.15, 0.03), "Tl": (0.50, 2.40, 0.10),
    "Cd": (0.50, 0.52, 0.10), "Sn": (0.46, 3.70, 0.02),
    "Pb": (0.48, 7.20, 0.02), "Re": (0.38, 1.70, 0.03),
    "Mo": (0.37, 0.92, 0.05), "Zn": (0.30, 0.85, 0.02),
    "Os": (0.21, 0.70, 0.02), "Zr": (0.00, 0.60, 0.02),
    "Ru": (0.00, 0.50, 0.02),
}
WEAK = {"Hg", "Tl", "Cd", "Sn", "Pb"}
TRANSITION = {"Zr", "Ru", "Os", "Re", "Mo"}


def alpha_mcmillan(lam, mustar):
    """McMillan 同位素指数修正 (Illinois 讲义 Eq.4)。"""
    denom = lam - mustar * (1 + 0.62 * lam)
    if denom <= 0:
        return float("nan")
    corr = 1.04 * (1 + lam) * (1 + 0.62 * lam) * mustar**2 / denom**2
    return 0.5 * (1 - corr)


def main():
    # P1 链内 α=1/2（mu*=0）
    assert abs(alpha_mcmillan(0.8, 0.0) - 0.5) < 1e-12, "P1: mu*=0 -> alpha=1/2"

    # P2 实验全部 <= 0.5（含误差上沿也不超太多）
    max_alpha = max(v[0] for v in ISOTOPE.values())
    assert max_alpha <= 0.5, "P2: 实验 alpha <= 0.5"

    # P3 弱耦合非过渡金属 alpha 在 [0.44, 0.5]
    weak_vals = [ISOTOPE[k][0] for k in WEAK]
    assert all(0.44 <= v <= 0.5 for v in weak_vals), "P3: 弱耦合 alpha 接近上界"

    # P4 过渡金属/低 Tc 趋 0
    trans_vals = [ISOTOPE[k][0] for k in TRANSITION]
    assert min(trans_vals) <= 0.05 and max(trans_vals) < 0.45, "P4: 过渡金属 alpha 低"

    # P5 McMillan 扫描全部 <= 0.5
    lams = np.linspace(0.3, 3.0, 100)
    mus = np.linspace(0.0, 0.2, 60)
    max_scan = -1
    for lam in lams:
        for mu in mus:
            a = alpha_mcmillan(lam, mu)
            if not math.isnan(a):
                max_scan = max(max_scan, a)
    assert max_scan <= 0.5 + 1e-9, "P5: McMillan alpha <= 0.5"

    print("R19 同位素效应上界（A 类机制身份＋B 类修正工具）：")
    print("  P1 链内 mu*=0: alpha=%.4f（纯 BCS 上界）" % alpha_mcmillan(0.8, 0.0))
    print("  P2 实验最大 alpha=%.2f（Hg/Tl/Cd）<= 0.5" % max_alpha)
    print("  P3 弱耦合非过渡金属 alpha: " + ", ".join("%s=%.2f" % (k, ISOTOPE[k][0]) for k in WEAK))
    print("  P4 过渡金属 alpha: " + ", ".join("%s=%.2f" % (k, ISOTOPE[k][0]) for k in TRANSITION))
    print("  P5 McMillan 扫描最大 alpha=%.6f <= 0.5" % max_scan)
    print("  全部断言通过（非拟合）")

    # 图
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9.5))

    ax = axes[0, 0]
    for k, (a, tc, err) in ISOTOPE.items():
        c = "tab:blue" if k in WEAK else ("tab:orange" if k in TRANSITION else "gray")
        ax.errorbar(tc, a, yerr=err, fmt="o", color=c, ms=6)
        ax.annotate(k, (tc, a), textcoords="offset points", xytext=(4, 3), fontsize=8)
    ax.axhline(0.5, color="red", ls="--", lw=1.5, label="链内上界 $\\alpha=1/2$")
    ax.set_xlabel("$T_c$ (K)"); ax.set_ylabel("同位素指数 $\\alpha$")
    ax.set_ylim(-0.1, 0.65)
    ax.set_title("A  元素同位素指数（Webb 2015），全部 ≤ 上界")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    lam_grid = np.linspace(0.4, 2.5, 200)
    for mu in [0.05, 0.10, 0.15, 0.20]:
        a_grid = [alpha_mcmillan(l, mu) for l in lam_grid]
        ax.plot(lam_grid, a_grid, lw=1.6, label="$\\mu^*=%.2f$" % mu)
    ax.axhline(0.5, color="red", ls="--", lw=1.5, label="上界 1/2")
    ax.set_xlabel("$\\lambda$"); ax.set_ylabel("$\\alpha$")
    ax.set_ylim(0, 0.55)
    ax.set_title("B  McMillan 修正：任意 $(\\lambda,\\mu^*)$ 均 ≤ 1/2")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    steps = ["$\\varepsilon\\propto 1/\\sqrt{M}$\n谐振子几何(环2)",
             "$c_s\\propto\\sqrt{k/\\rho}\\propto M^{-1/2}$\n声速(环2/8)",
             "$\\Theta_D=(\\hbar c_s/k_B)(6\\pi^2n)^{1/3}$\n(环8)",
             "$T_c=\\frac{2e^\\gamma}{\\pi}\\Theta_D e^{-1/\\lambda}$\n(C5)",
             "$\\alpha=-d\\ln T_c/d\\ln M=1/2$\n链内纯数"]
    for i, s in enumerate(steps):
        ax.text(0.5, 0.9 - i*0.18, s, ha="center", va="center", fontsize=9,
                color=("blue" if i == 4 else "black"))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_title("C  链内推导：几何→声速→$\\Theta_D$→$T_c$→$\\alpha=1/2$")

    ax = axes[1, 1]
    weak_mean = np.mean(weak_vals)
    trans_mean = np.mean(trans_vals)
    ax.bar(["弱耦合非过渡金属\n(Hg/Tl/Cd/Sn/Pb)", "过渡金属/低Tc\n(Zr/Ru/Os/Re/Mo)"],
           [weak_mean, trans_mean], color=["tab:blue", "tab:orange"], alpha=0.85)
    ax.axhline(0.5, color="red", ls="--", lw=1.4, label="上界 0.5")
    for i, v in enumerate([weak_mean, trans_mean]):
        ax.text(i, v + 0.01, "%.3f" % v, ha="center", fontsize=10)
    ax.set_ylabel("平均 $\\alpha$"); ax.set_ylim(0, 0.6)
    ax.set_title("D  上界附近 vs 趋 0（外生 $\\mu^*$ 修正）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3, axis="y")

    fig.tight_layout()
    png = os.path.join(OUT, "R19_同位素效应上界.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    summary = [
        ["链内 alpha", "0.5", "cs∝M^{-1/2}(几何)→Theta_D→Tc（A 类纯数）"],
        ["上界", "<=0.5", "McMillan 修正≥0；实验无 >0.5"],
        ["弱耦合平均 alpha", "%.3f" % weak_mean, "Hg/Tl/Cd/Sn/Pb，接近上界"],
        ["过渡金属平均 alpha", "%.3f" % trans_mean, "外生 mu* 修正，预注册允许"],
        ["类别", "A 类机制身份＋B 类修正工具", "mu* 外生(第60轮归口)"],
        ["边界", "反常同位素(U -2/PdH -0.25)", "链外现象，只登记不解释"],
    ]
    with open(os.path.join(OUT, "R19_同位素效应上界_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo); w.writerow(["量","值","说明"]); w.writerows(summary)

    print("图:", png)


if __name__ == "__main__":
    main()
