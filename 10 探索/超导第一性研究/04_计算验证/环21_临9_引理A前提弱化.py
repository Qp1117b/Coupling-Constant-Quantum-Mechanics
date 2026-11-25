# -*- coding: utf-8 -*-
"""
环 21／临-9 引理 A 前提弱化的数值核对。

1. 格点间距 alpha=gamma_1/Q 与零点平均间距 2*pi/ln(T) 的交叉；
2. Riemann-von Mangoldt 计数 N(T)~T ln T/(2pi) 与格点容量 T/alpha（线性）的交叉；
3. 同相条件的模满足率（只有 c=0 全部满足）；
4. 三步弱化的逻辑链（集合包含示意）。

由 (9.1)(9.2) 与已知计数公式直接计算，无拟合。
"""

import csv
import os
from fractions import Fraction

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "环21_临9_引理A前提弱化.png")
OUT_CSV = os.path.join(HERE, "环21_临9_引理A前提弱化.csv")

GAMMAS = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862]
G1 = GAMMAS[0]
Q_FIX = 25


def main():
    rows = []

    # A 格点间距 vs 零点平均间距
    print("A 格点间距与零点平均间距")
    Ts = np.logspace(2, 8, 300)
    alpha = G1 / Q_FIX
    avg_spacing = 2 * np.pi / np.log(Ts)
    cross = Ts[np.argmin(np.abs(avg_spacing - alpha))]
    print(f"  alpha=gamma1/Q={alpha:.6f}")
    print(f"  交叉 T≈{cross:.3e}：此后零点平均间距 < 固定格距")
    for T in (1e2, 1e4, 1e6, 1e8):
        rows.append(("spacing", T, 2 * np.pi / np.log(T), alpha, np.nan))

    # B 计数 vs 格点容量
    print("\nB 计数超线性 vs 格点容量线性")
    NT = Ts * np.log(Ts) / (2 * np.pi)
    cap = Ts / alpha + 1
    idx = np.argmin(np.abs(NT - cap))
    print(f"  交叉 T≈{Ts[idx]:.3e}：此后格点无法容纳所有零点")
    for i in (50, 150, 250):
        rows.append(("counting", Ts[i], NT[i], cap[i], np.nan))

    # C 同相条件的模满足率
    print("\nC 同相条件满足率")
    cs = np.linspace(0, 0.5, 200)
    eps = 1e-3
    rates = []
    for c in cs:
        phases = np.array(GAMMAS) * c / (2 * np.pi)
        frac = np.abs(phases - np.round(phases))
        rates.append(float(np.mean(frac < eps)))
    rates = np.array(rates)
    print(f"  c=0 满足率={rates[0]:.3f}，c>0 最大满足率={rates[1:].max():.3f}")
    for i in (0, 40, 100, 199):
        rows.append(("phase", cs[i], rates[i], np.nan, np.nan))

    # D 有理逼近分母（示意：数值逼近不能证明无界）
    print("\nD 前 6 个零点的有理逼近分母")
    dens = []
    for i, g in enumerate(GAMMAS):
        fr = Fraction(g / G1).limit_denominator(10 ** 6)
        dens.append(fr.denominator)
        print(f"  n={i+1}: gamma_n/gamma_1≈{g/G1:.6f}, 逼近分母≈{fr.denominator}")
        rows.append(("denominator", i + 1, dens[-1], g / G1, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.4))

    ax[0, 0].loglog(Ts, avg_spacing, lw=2.2, color="tab:blue",
                    label=r"零点平均间距 $2\pi/\ln T$")
    ax[0, 0].axhline(alpha, color="tab:red", ls="--", lw=1.6,
                     label=rf"格距 $\alpha=\gamma_1/Q={alpha:.3f}$")
    ax[0, 0].axvline(cross, color="tab:green", ls=":", lw=1.4)
    ax[0, 0].set_xlabel(r"$T$")
    ax[0, 0].set_ylabel("间距")
    ax[0, 0].set_title("A  高零点处平均间距小于固定格距")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3, which="both")

    ax[0, 1].loglog(Ts, NT, lw=2.2, color="tab:blue",
                    label=r"$N(T)\sim T\ln T/(2\pi)$")
    ax[0, 1].loglog(Ts, cap, lw=2.2, color="tab:orange",
                    label=r"格点容量 $T/\alpha$（线性）")
    ax[0, 1].axvline(Ts[idx], color="tab:green", ls=":", lw=1.4)
    ax[0, 1].set_xlabel(r"$T$")
    ax[0, 1].set_ylabel("计数")
    ax[0, 1].set_title("B  超线性计数终将超过线性格点容量")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3, which="both")

    ax[1, 0].plot(cs, rates, lw=2.2, color="tab:purple")
    ax[1, 0].set_xlabel(r"$c=H/2\pi$")
    ax[1, 0].set_ylabel("同相模满足率")
    ax[1, 0].set_title("C  只有 $c=0$ 使全部模同相")
    ax[1, 0].grid(alpha=0.3)

    ax[1, 1].bar(["一对无理比", "分母无界", "引理 A 成立"], [3, 2, 1],
                 color=["tab:blue", "tab:orange", "tab:green"], alpha=0.85)
    ax[1, 1].set_ylabel("前提强度（示意：越左越强）")
    ax[1, 1].set_title("D  三步弱化（左强 -> 中 -> 右弱）\n数值逼近分母不能证明无界性")
    ax[1, 1].grid(alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
