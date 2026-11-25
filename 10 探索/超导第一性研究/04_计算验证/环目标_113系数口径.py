# -*- coding: utf-8 -*-
"""
1.13 系数与 omega_log 对数矩口径核查的数值核对（非拟合）。

四面板：
A BCS 前因子 1.13*omega_D vs CQM 1.13*e^{-1/3}*omega_D（差 e^{-1/3}）；
B gap ratio 2pi/e^gamma 与前因子频率无关（扫 omega 恒 3.528）；
C e^{-1/3} 刻度因子 < 1；
D V2 反解 lambda 用两口径的对比（显示差异小，主因是 mu* 缺失）。
"""

import csv
import os
from math import pi, exp, log

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "环目标_113系数口径.png")
OUT_CSV = os.path.join(HERE, "环目标_113系数口径.csv")

GAMMA = 0.5772156649
RATIO = 2 * pi / exp(GAMMA)
FACTOR = exp(-1 / 3)

# Webb 2015 Table III 子集
DATA = [("Al", 1.18, 428), ("Nb", 9.25, 275), ("Pb", 7.2, 105),
        ("Sn", 3.7, 200), ("Cd", 0.52, 209)]


def main():
    rows = []
    Ths = np.linspace(50, 500, 200)
    pref_bcs = 1.13 * Ths
    pref_cqm = 1.13 * FACTOR * Ths
    print(f"A 前因子: BCS=1.13*theta_D, CQM=1.13*e^(-1/3)*theta_D (e^(-1/3)={FACTOR:.4f})")
    for th, b, c in zip(Ths[::50], pref_bcs[::50], pref_cqm[::50]):
        rows.append(("prefactor", th, b, c, np.nan))

    # B gap ratio 与前因子无关
    print(f"\nB gap ratio 2pi/e^gamma = {RATIO:.4f}（与前因子 omega 无关）")
    omegas = np.logspace(0, 4, 200)  # 任意前因子能标
    for w in omegas[::40]:
        rows.append(("ratio", w, RATIO, RATIO, np.nan))

    # C 刻度因子
    print(f"C e^(-1/3) = {FACTOR:.4f} < 1")
    rows.append(("scale", 0, FACTOR, 1.0, np.nan))

    # D V2 反解两口径
    print("\nD V2 反解 lambda（BCS 前因子 1.13 vs CQM 1.13*e^{-1/3}）")
    print(f"{'元素':<4}{'lam_BCS前因子':>14}{'lam_CQM前因子':>14}")
    for name, tc, th in DATA:
        inv_bcs = log(1.13 * th / tc)
        inv_cqm = log(1.13 * FACTOR * th / tc)
        lb, lc = 1 / inv_bcs, 1 / inv_cqm
        print(f"{name:<4}{lb:>14.4f}{lc:>14.4f}")
        rows.append(("inverse", tc, lb, lc, f"{name}|{th}"))
    print("  差异约 e^{-1/3} 平移，远小于缺 mu* 造成的差距（Eliashberg lam 更大）")

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.4, 9.6))

    ax[0, 0].plot(Ths, pref_bcs, lw=2.4, color="tab:blue", label=r"BCS $1.13\,\theta_D$")
    ax[0, 0].plot(Ths, pref_cqm, lw=2.4, color="tab:orange",
                  label=r"CQM $1.13e^{-1/3}\theta_D$")
    ax[0, 0].set_xlabel(r"$\theta_D$（K）")
    ax[0, 0].set_ylabel("前因子能标")
    ax[0, 0].set_title("A  BCS 截断 vs CQM 对数矩前因子")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    ax[0, 1].semilogx(omegas, [RATIO] * len(omegas), lw=2.4, color="tab:green")
    ax[0, 1].axhline(RATIO, color="tab:red", ls="--", lw=1.4)
    ax[0, 1].set_xlabel(r"前因子能标 $\omega$（任意）")
    ax[0, 1].set_ylabel(r"$2\Delta/k_BT^*$")
    ax[0, 1].set_title(f"B  gap ratio 恒为 {RATIO:.3f}（与前因子无关）")
    ax[0, 1].grid(alpha=0.3, which="both")

    ax[1, 0].bar(["$e^{-1/3}$"], [FACTOR], color="tab:purple", alpha=0.85, width=0.4)
    ax[1, 0].axhline(1, color="tab:red", ls="--", lw=1.4)
    ax[1, 0].set_ylabel("刻度因子")
    ax[1, 0].set_title(f"C  CQM/BCS 前因子比 = {FACTOR:.4f} < 1")
    ax[1, 0].grid(alpha=0.3, axis="y")

    names = [d[0] for d in DATA]
    bs = [1 / log(1.13 * d[2] / d[1]) for d in DATA]
    cs = [1 / log(1.13 * FACTOR * d[2] / d[1]) for d in DATA]
    x = np.arange(len(names))
    ax[1, 1].bar(x - 0.18, bs, 0.36, label="BCS 前因子", color="tab:blue", alpha=0.8)
    ax[1, 1].bar(x + 0.18, cs, 0.36, label="CQM 前因子", color="tab:orange", alpha=0.8)
    ax[1, 1].set_xticks(x)
    ax[1, 1].set_xticklabels(names)
    ax[1, 1].set_ylabel("反解 $\\lambda$")
    ax[1, 1].set_title("D  两口径反解对比（主因仍是缺 $\\mu^*$）")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
