# -*- coding: utf-8 -*-
"""
预注册判定 R7：比热跳变普适常数与强耦合单调趋势（非拟合）
============================================================
检验第95轮 Ehrenfest 判定给出的预言：弱耦合 ΔC/γTc=12/(7ζ3)=1.426。
判据在 07_数据与现象/预注册判定_R7.md 已写死（跑数前），本脚本只执行。
数据全部独立实测文献，无一从 CQM 反解。

复跑：python "10 探索/超导第一性研究/04_计算验证/R7_比热跳变普适常数盲测.py"
"""
import csv
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
ZETA3 = 1.202056903159594
BC = 12.0 / (7.0 * ZETA3)   # 1.426（CQM 第95轮预言）

# 独立实测数据：IJPM 2026 表 + WMI 讲义 Table2
# (element, dC/gTc, gap_ratio 2Δ/kBTc, coupling_class 0=weak,1=inter,2=strong)
DATA = [
    ("Al", 1.45, 3.4, 0),
    ("Cd", 1.36, 3.2, 0),
    ("Sn", 1.60, 3.5, 1),
    ("In", 1.73, 3.6, 1),
    ("Ta", 1.59, 3.6, 1),
    ("Nb", 1.93, 3.8, 2),
    ("Pb", 2.71, 4.3, 2),
    ("Hg", 2.37, 4.6, 2),
]


def main():
    elems = [d[0] for d in DATA]
    dC = np.array([d[1] for d in DATA])
    gap = np.array([d[2] for d in DATA])
    cls = np.array([d[3] for d in DATA])

    # ---------- P1: 弱耦合子集 vs 1.426 ----------
    weak = cls == 0
    weak_vals = dC[weak]
    rel_err = np.abs(weak_vals - BC) / BC
    p1_pass = bool(np.all(rel_err <= 0.08))
    max_rel = float(np.max(rel_err))

    # ---------- P2: 耦合分类单调 ----------
    means = [dC[cls == k].mean() for k in [0, 1, 2]]
    p2_pass = bool(means[0] < means[1] < means[2])

    # ---------- P3: 比热跳变与 gap ratio 同向 ----------
    corr = float(np.corrcoef(dC, gap)[0, 1])
    p3_pass = bool(corr > 0)

    assert p1_pass, f"P1 失败：弱耦合偏差 {max_rel:.3%}"
    assert p2_pass, f"P2 失败：分类均值 {means}"
    assert p3_pass, f"P3 失败：相关 {corr}"

    # ---------- 图 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ax = axes[0, 0]
    colors = ["green" if c == 0 else "orange" if c == 1 else "red" for c in cls]
    ax.bar(elems, dC, color=colors)
    ax.axhline(BC, color="k", ls="--", lw=1.2, label=f"CQM 弱耦合 {BC:.3f}")
    ax.set_ylabel("ΔC/γTc")
    ax.set_title("A  实测比热跳变 vs CQM 弱耦合预言")
    ax.legend(fontsize=8)

    ax = axes[0, 1]
    ax.bar([elems[i] for i in range(len(elems)) if weak[i]], weak_vals,
           color="green")
    ax.axhline(BC, color="k", ls="--", lw=1.2, label=f"{BC:.3f}")
    ax.set_ylabel("ΔC/γTc")
    ax.set_title(f"B  弱耦合子集（最大偏差 {max_rel:.1%} ≤ 8%）")
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    ax.scatter(gap, dC, c=cls, cmap="viridis", s=80)
    ax.set_xlabel("2Δ(0)/kBTc")
    ax.set_ylabel("ΔC/γTc")
    ax.set_title(f"C  P3 同向性（Pearson r={corr:.3f}>0）")

    ax = axes[1, 1]
    labels = ["weak", "intermediate", "strong"]
    ax.bar(labels, means, color=["green", "orange", "red"])
    ax.set_ylabel("平均 ΔC/γTc")
    ax.set_title(f"D  P2 单调（{'<'.join(f'{m:.2f}' for m in means)}）")

    fig.tight_layout()
    png = os.path.join(OUT, "R7_比热跳变普适常数盲测.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    summary = [
        ["P1 弱耦合普适", "PASS" if p1_pass else "FAIL",
         f"最大偏差 {max_rel:.1%}（判据≤8%）"],
        ["P2 强耦合单调", "PASS" if p2_pass else "FAIL",
         f"分类均值 {'<'.join(f'{m:.2f}' for m in means)}"],
        ["P3 同向性", "PASS" if p3_pass else "FAIL",
         f"Pearson r={corr:.3f}>0"],
        ["CQM 预言值", f"{BC:.6f}", "=12/(7ζ(3))（第95轮）"],
        ["数据点", f"{len(DATA)} 元素", "IJPM2026 + WMI讲义，独立实测"],
    ]
    with open(os.path.join(OUT, "R7_比热跳变普适常数盲测_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["判据", "结果", "说明"])
        w.writerows(summary)

    print("R7 比热跳变普适常数盲测：预注册三项判据全部通过（非拟合）")
    for row in summary:
        print("  ", row[0], "=", row[1], "|", row[2])
    print("图:", png)


if __name__ == "__main__":
    main()
