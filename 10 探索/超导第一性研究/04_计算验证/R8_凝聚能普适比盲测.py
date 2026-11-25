# -*- coding: utf-8 -*-
"""
预注册判定 R8：凝聚能普适比 Econd/(gamma Tc^2)=3/(4 e^{2 gamma_E})=0.236（非拟合）
================================================================================
检验第97轮链内纯数（第89轮凝聚能 + C5 gap + Sommerfeld 消元）。
判据在 07_数据与现象/预注册判定_R8.md 跑数前写死。全部独立实测数据。

复跑：python "10 探索/超导第一性研究/04_计算验证/R8_凝聚能普适比盲测.py"
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
GAMMA_E = 0.5772156649015329
RATIO = 3.0 / (4.0 * math.exp(2 * GAMMA_E))   # 0.23643（CQM 第97轮）
MU0 = 4 * math.pi * 1e-7

# WMI Table 2: (element, Tc[K], gamma[J/m3K2], Bc0[mT], coupling_class 0=weak,1=inter,2=strong)
DATA = [
    ("Al", 1.2, 135, 10, 0),
    ("Nb", 9.2, 704, 206, 2),
    ("Pb", 7.2, 164, 80, 2),
]
# SSRN 引 Kim 实验拟合 Econd/gamma = 0.2 Tc^2.06（多材料，作对照线）


def main():
    elems = [d[0] for d in DATA]
    Tc = np.array([d[1] for d in DATA], dtype=float)
    gam = np.array([d[2] for d in DATA], dtype=float)
    Bc = np.array([d[3] for d in DATA], dtype=float) * 1e-3
    cls = [d[4] for d in DATA]

    Econd_meas = Bc**2 / (2 * MU0)              # 实测凝聚能密度
    Econd_pred = RATIO * gam * Tc**2            # CQM 预言
    ratio_meas = Econd_meas / (gam * Tc**2)     # 实测普适比
    rel_err = np.abs(Econd_pred - Econd_meas) / Econd_meas

    # ---------- P1: 弱耦合 Al 相对偏差 <=20% ----------
    al_idx = elems.index("Al")
    p1_pass = bool(rel_err[al_idx] <= 0.20)
    p1_dev = float(rel_err[al_idx])

    # ---------- P2: 三元素量级/符号一致 <25%，强耦合偏差单调增大（允许） ----------
    p2_pass = bool(np.all(rel_err < 0.25))
    devs = [float(x) for x in rel_err]
    # 纯数与文献 GL-BCS 0.236 一致
    assert abs(RATIO - 0.236) < 0.001

    assert p1_pass, f"P1 失败：Al 偏差 {p1_dev:.1%}"
    assert p2_pass, f"P2 失败：偏差 {devs}"

    # ---------- 图 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ax = axes[0, 0]
    Tc2 = Tc**2
    ax.scatter(Tc2, ratio_meas, s=80, c=["green", "red", "red"])
    tline = np.linspace(0.5, 90, 100)
    ax.plot(tline, np.full_like(tline, RATIO), "k--", lw=1.2,
            label=f"CQM 纯数 {RATIO:.3f}")
    ax.plot(tline, 0.2 * tline**1.03, "b:", lw=1.2,
            label="Kim 实验拟合 $0.2T_c^{2.06}$")
    ax.set_xlabel("$T_c^2$ (K²)")
    ax.set_ylabel("$E_{cond}/\\gamma_0$ (J/m³)")
    ax.set_title("A  凝聚能普适比：CQM 纯数 vs 实测")
    ax.legend(fontsize=8)

    ax = axes[0, 1]
    x = np.arange(len(elems))
    ax.bar(x - 0.2, Econd_meas, 0.4, color="#1f77b4", label="实测 $B_c^2/2\\mu_0$")
    ax.bar(x + 0.2, Econd_pred, 0.4, color="orange", label="CQM $0.236\\gamma T_c^2$")
    ax.set_xticks(x, elems)
    ax.set_ylabel("$E_{cond}$ (J/m³)")
    ax.set_title("B  凝聚能：实测 vs CQM 拉通关系")
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    ax.bar(elems, [d * 100 for d in devs],
           color=["green" if c == 0 else "red" for c in cls])
    ax.axhline(20, color="k", ls="--", lw=1.0, label="P1 阈值 20%")
    ax.set_ylabel("相对偏差 (%)")
    ax.set_title("C  相对偏差（强耦合系统性增大＝预注册允许）")
    ax.legend(fontsize=8)

    ax = axes[1, 1]
    Bc_pred = np.sqrt(2 * MU0 * Econd_pred)
    ax.scatter(Bc * 1e3, Bc_pred * 1e3, s=80)
    ax.plot([0, 220], [0, 220], "k--", lw=1.0, label="y=x")
    ax.set_xlabel("实测 $B_c(0)$ (mT)")
    ax.set_ylabel("CQM 预言 $B_c(0)$ (mT)")
    ax.set_title("D  临界场拉通 (19F.8)")
    ax.legend(fontsize=8)

    fig.tight_layout()
    png = os.path.join(OUT, "R8_凝聚能普适比盲测.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    summary = [
        ["CQM 纯数 3/(4e^{2γE})", f"{RATIO:.6f}", "与 SSRN GL-BCS 0.236 一致"],
        ["P1 弱耦合 Al 偏差", f"{p1_dev:.1%}", "≤20% 通过"],
        ["P2 三元素偏差", f"{max(devs):.1%}", "<25% 通过"],
        ["Al 实测普适比", f"{ratio_meas[al_idx]:.4f}", "vs 0.236"],
        ["数据", "WMI Table2 Al/Nb/Pb", "独立实测、无拟合"],
    ]
    with open(os.path.join(OUT, "R8_凝聚能普适比盲测_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["量", "值", "说明"])
        w.writerows(summary)

    print("R8 凝聚能普适比盲测：预注册判据全部通过（非拟合）")
    for row in summary:
        print("  ", row[0], "=", row[1], "|", row[2])
    print("图:", png)


if __name__ == "__main__":
    main()
