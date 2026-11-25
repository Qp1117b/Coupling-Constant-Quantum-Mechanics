# -*- coding: utf-8 -*-
"""
R44：第七纯数 S_J = 4 pi e^gamma / (7 zeta3)
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
ROOT = os.path.abspath(os.path.join(OUT, "..", "..", ".."))
GAMMA = 0.5772156649015329
ZETA3 = 1.2020569031595943


def main():
    # ---------- P1 ----------
    ledger = open(os.path.join(ROOT, "10 探索", "超导第一性研究", "00_当前有效口径表.md"),
                  encoding="utf-8").read()
    checks = {
        "R6斜率": "2.65" in ledger and "约瑟夫森" in ledger,
        "R2": "12/(7" in ledger or "12/(7\\zeta" in ledger,
        "R1": "2\\pi/e^\\gamma" in ledger,
    }
    assert all(checks.values()), "P1: 原文审计失败 %s" % checks

    # ---------- P3：纯数 ----------
    SJ = 4 * math.pi * math.exp(GAMMA) / (7 * ZETA3)
    ab_slope = 2.67                      # AB erratum
    rel = abs(SJ - ab_slope) / ab_slope
    assert rel < 0.01, "P3: 相对差 %.4f" % rel

    # AB 曲线数值斜率（BCS 插值 gap）
    delta0_over_tc = math.pi / math.exp(GAMMA)
    def ic_ratio(t):
        d = delta0_over_tc * math.tanh(1.74 * math.sqrt(max(1.0 / t - 1.0, 0.0)))
        x = d / (2 * t)
        return (d / delta0_over_tc) * math.tanh(x)
    ts = np.linspace(0.9, 0.999, 200)
    slopes = []
    for t in ts[:-1]:
        h = 1e-5
        dI = (ic_ratio(min(t + h, 1 - 1e-12)) - ic_ratio(t)) / h
        slopes.append(abs(dI))
    slopes = np.array(slopes)
    assert abs(slopes[-1] - SJ) / SJ < 0.05, "P3: 数值斜率 %.3f vs %.3f" % (slopes[-1], SJ)

    print("R44 第七纯数（代数，无拟合）：")
    print("  P1 登记：%s" % checks)
    print("  S_J = 4 pi e^gamma / (7 zeta3) = %.6f" % SJ)
    print("  AB 勘误斜率 %.2f，相对差 %.2f%%" % (ab_slope, 100 * rel))
    print("  AB+BCS 插值数值斜率（t→1）%.4f" % slopes[-1])
    print("  P4 无新生成元；P5 Lean")

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    ax = axes[0, 0]
    tv = np.linspace(0.4, 1.0, 300)
    ic = np.array([ic_ratio(t) for t in tv])
    ax.plot(tv, ic, "b-", lw=2.4, label="AB $I_c(T)/I_c(0)$（B 类工具）")
    ax.set_xlabel("$T/T_c$")
    ax.set_ylabel("$I_c/I_c(0)$")
    ax.set_title("A  约瑟夫森临界电流温度曲线")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.plot(ts[:-1], slopes, "o-", lw=2.2, ms=4, color="#d62728", label="AB+BCS 数值斜率")
    ax.axhline(SJ, color="k", ls="--", lw=1.5, label="$S_J=%.4f$" % SJ)
    ax.axhline(ab_slope, color="gray", ls=":", lw=1.4, label="AB 勘误 %.2f" % ab_slope)
    ax.set_xlabel("$T/T_c$")
    ax.set_ylabel("归一化斜率")
    ax.set_title("B  近 $T_c$ 斜率收敛到 $S_J$")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    names = ["$R_1$", "$R_2$", "$S_J$"]
    vals = [2 * math.pi / math.exp(GAMMA), 12 / (7 * ZETA3), SJ]
    ax.bar(names, vals, color=["#1f77b4", "#2ca02c", "#d62728"], alpha=0.85)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.06, "%.4f" % v, ha="center", fontsize=9)
    ax.set_ylim(0, 4.2)
    ax.set_title("C  第七纯数与既有纯数同量级")
    ax.grid(alpha=0.3, axis="y")

    ax = axes[1, 1]
    ax.text(0.04, 0.80, "成立", fontsize=12, weight="bold", color="#2ca02c")
    ax.text(0.04, 0.65, "· 链内 gap 近 $T_c$ 展开\n· AB $T\\to0$ 与有限温式\n· $S_J$ 由 $e^\\gamma,\\zeta_3,\\pi$ 生成", fontsize=10)
    ax.text(0.04, 0.38, "边界", fontsize=12, weight="bold", color="#d62728")
    ax.text(0.04, 0.23, "· 不闭合缺口\n· 不声称 CQM 推出 AB 式\n· 高透明 SNS 不在范围", fontsize=10)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_title("D  纯数登记的边界")

    fig.tight_layout()
    png = os.path.join(OUT, "R44_第七纯数.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "R-119/R-112 登记 %s" % checks, "通过"],
        ["P2", "AB 勘误 2.67；BCS gap 近 Tc", "B 类"],
        ["P3", "S_J=%.6f；与 2.67 差 %.2f%%" % (SJ, 100 * rel), "通过"],
        ["P4", "无新生成元", "纯数登记"],
        ["P5", "代数证明（Lean）", "由 Lean 承载"],
        ["结论", "第七纯数 S_J 登记", "状态不动"],
    ]
    with open(os.path.join(OUT, "R44_第七纯数_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
