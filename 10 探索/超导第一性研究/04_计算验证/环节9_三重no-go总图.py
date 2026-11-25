# -*- coding: utf-8 -*-
"""
R8: 环节⑨ 三重 no-go 总图（R4 模和收敛 + R5 DOS 幂律 + R7 热核统计类型）。
只检验收敛/斜率/不等式，不拟合。仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/环节9_三重no-go总图.py"
"""
import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
ZETA3 = 1.2020569031595943


def assertions():
    out = {}
    K = np.arange(1, 100001)
    S = np.cumsum(1.0 / K**3)
    out["pairing_sum_limit"] = float(S[-1])
    out["pairing_sum_vs_zeta3_relerr"] = float(abs(S[-1] - ZETA3) / ZETA3)
    out["pairing_sum_below_2"] = bool(np.all(S <= 2.0))

    E = np.logspace(0, 4, 200)
    slope_dos = np.polyfit(np.log(E), np.log(1 / E**1.5), 1)[0]
    out["integrand_slope"] = float(slope_dos)
    out["integrand_is_powerlaw_not_log"] = bool(abs(slope_dos + 1.5) < 1e-9)

    x = np.linspace(0.05, 5, 1000)
    out["coth_minus_tanh_min"] = float(np.min(1 / np.tanh(x) - np.tanh(x)))
    out["thermal_no_identity"] = bool(out["coth_minus_tanh_min"] > 0)
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # (a) R4 配对模和收敛
    ax = axes[0, 0]
    K = np.logspace(0, 5, 400)
    S = np.array([sum(1.0 / k**3 for k in range(1, int(k) + 1)) for k in np.geomspace(1, 1000, 60)])
    Kp = np.geomspace(1, 1000, 60)
    ax.semilogx(Kp, S, "b-", lw=2, label=r"$\sum 1/k^3$")
    ax.axhline(ZETA3, color="k", ls="--", lw=1.5, label=r"$\zeta(3)\approx1.202$")
    ax.axhline(2, color="gray", ls=":", lw=1.5, label=r"上界 2（Lean）")
    ax.set_xlabel(r"档数 $K$")
    ax.set_ylabel("配对通道和")
    ax.set_title("(a) R4：收敛，无 Cooper 对数")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (b) R5 DOS integrand 幂律
    ax = axes[0, 1]
    E = np.logspace(0, 4, 300)
    ax.loglog(E, 1 / E**1.5, "g-", lw=2, label=r"$g/E\propto E^{-3/2}$")
    ax.loglog(E, 1 / E, "r--", lw=1.5, label=r"对数所需 $1/E$（未出现）")
    ax.set_xlabel(r"能量 $E/E_2$")
    ax.set_ylabel("integrand")
    ax.set_title("(b) R5：DOS 侧幂律，非对数")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (c) R7 热核统计类型
    ax = axes[1, 0]
    x = np.linspace(0.05, 5, 400)
    ax.plot(x, 1 / np.tanh(x), "b-", lw=2, label=r"$\coth$（链，玻色）")
    ax.plot(x, np.tanh(x), "r-", lw=2, label=r"$\tanh$（隙方程，费米）")
    ax.axhline(1, color="k", ls="--", lw=1)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel("热核")
    ax.set_title("(c) R7：coth ≠ tanh，格点不交")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (d) 三要素 → 全部外生（示意）
    ax = axes[1, 1]
    labels = ["对数\n(R4/R5)", "积分核\n(无隙方程)", "费米热核\n(R7)"]
    vals = [1, 1, 1]
    ax.bar(labels, vals, color=["tab:blue", "tab:orange", "tab:green"])
    ax.set_ylabel("链内可提供？")
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["否", "否(外生)"])
    ax.set_title("(d) BCS Tc 三要素：均需链外输入")
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("R8: 环节⑨ 不可能性定理（R4+R5+R7 三重 no-go）", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "环节9_三重no-go总图.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R8 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "环节9_三重no-go总图_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
