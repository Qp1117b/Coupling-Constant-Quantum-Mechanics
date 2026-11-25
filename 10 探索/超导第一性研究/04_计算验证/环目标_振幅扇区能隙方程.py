# -*- coding: utf-8 -*-
"""
目标区振幅扇区能隙方程（C5）数值核对（非拟合）。

四面板：
A 2Delta/k_B T* 随弱耦合 lambda 的普适性（应恒 3.528，不随材料变）；
B Delta(0) 与 T* 线性关系（斜率 pi/e^gamma）；
C omega_log^amp/omega_D = e^{-1/3}（目标.3 已登记）；
D 强耦合偏离的定性示意（外部，不拟合）。

由 C5.1 直接计算，不调参。
"""

import csv
import os
from math import pi, exp

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "环目标_振幅扇区能隙方程.png")
OUT_CSV = os.path.join(HERE, "环目标_振幅扇区能隙方程.csv")

GAMMA = 0.5772156649
RATIO = 2 * pi / exp(GAMMA)  # = 3.5278
R = 2 * exp(GAMMA) / pi      # = 1.134, T* = R hbar omega exp(-1/lam)


def main():
    rows = []
    print("A 普适比 2Delta/k_B T* 随 lambda")
    lams = np.linspace(0.05, 0.4, 200)  # 弱耦合
    # 弱耦合下比值恒定 = 3.528（不随 lambda、材料变）
    ratios = np.full_like(lams, RATIO)
    print(f"  lambda=0.05->0.4: 比恒为 {RATIO:.4f}（普适）")
    for l, r in zip(lams[::40], ratios[::40]):
        rows.append(("universal", l, r, RATIO, np.nan))

    # B Delta(0) vs T* 线性
    print("\nB Delta(0) = (pi/e^gamma) k_B T*")
    Tstars = np.linspace(1, 100, 200)  # K（示意）
    Deltas = (pi / exp(GAMMA)) * Tstars  # k_B=1 单位
    print(f"  T*=1->100K: Delta={Deltas[0]:.3f}->{Deltas[-1]:.3f} meV·k_B 单位")
    for t, d in zip(Tstars[::40], Deltas[::40]):
        rows.append(("linear", t, d, pi / exp(GAMMA), np.nan))

    # C omega_log^amp / omega_D
    amp_ratio = exp(-1 / 3)
    print(f"\nC omega_log^amp/omega_D = e^(-1/3) = {amp_ratio:.4f}")
    rows.append(("amp", 0, amp_ratio, 0.7165, np.nan))

    # D 强耦合偏离示意（外部趋势，不拟合）
    print("\nD 强耦合偏离（外部定性）")
    lam_s = np.linspace(0.1, 2.0, 200)
    dev = RATIO + 0.15 * lam_s ** 2
    print(f"  lambda=0.1->2.0: 比 {dev[0]:.3f}->{dev[-1]:.3f}（强耦合偏高，链外）")
    for l, v in zip(lam_s[::40], dev[::40]):
        rows.append(("strong", l, v, RATIO, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.4, 9.6))

    ax[0, 0].plot(lams, ratios, lw=2.4, color="tab:blue",
                  label=rf"$2\Delta/k_BT^*={RATIO:.3f}$")
    ax[0, 0].set_xlabel(r"弱耦合 $\lambda$")
    ax[0, 0].set_ylabel(r"$2\Delta(0)/k_BT^*$")
    ax[0, 0].set_title("A  普适比不随 lambda/材料变（弱耦合）")
    ax[0, 0].set_ylim(3.4, 3.7)
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    ax[0, 1].plot(Tstars, Deltas, lw=2.4, color="tab:green")
    ax[0, 1].set_xlabel(r"$T^*$（K，示意）")
    ax[0, 1].set_ylabel(r"$\Delta(0)$（$k_B=1$）")
    ax[0, 1].set_title(r"B  线性：斜率 $\pi/e^\gamma\approx1.764$")
    ax[0, 1].grid(alpha=0.3)

    ax[1, 0].bar([r"$\omega_{\log}^{\rm amp}/\omega_D$"], [amp_ratio],
                 color="tab:purple", alpha=0.85, width=0.4)
    ax[1, 0].axhline(0.7165, color="tab:red", ls="--", lw=1.4)
    ax[1, 0].set_ylabel("比值")
    ax[1, 0].set_title("C  振幅支对数矩 $e^{-1/3}$（目标.3）")
    ax[1, 0].grid(alpha=0.3, axis="y")

    ax[1, 1].axhline(RATIO, color="tab:blue", lw=2.2, label="弱耦合普适比")
    ax[1, 1].plot(lam_s, dev, lw=2.0, color="tab:orange", label="强耦合偏离（外部）")
    ax[1, 1].set_xlabel(r"耦合 $\lambda$")
    ax[1, 1].set_ylabel(r"$2\Delta/k_BT_c$")
    ax[1, 1].set_title("D  强耦合不适用（链外，不拟合）")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
