# -*- coding: utf-8 -*-
"""
R40：审-7 三处"2"的对象辨析
=====================================================================
预注册 R40 的 P1–P5（跑数前写死）：
  P1 原文审计 审-7/临-7
  P2 外部标准 Phi0=h/2e, zeta(-2n)=0, N(0)=m kF/(2 pi^2 hbar^3)
  P3 单位/对象三分；自然单位 1/(2pi^2) != 2
  P4 审-7/临-7 不闭合
  P5 Lean

复跑：python "10 探索/超导第一性研究/04_计算验证/R40_三处2的对象辨析.py"
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


def main():
    # ---------- P1 ----------
    chain = open(os.path.join(ROOT, "10 探索", "CQM_探索_推导链.md"), encoding="utf-8").read()
    checks = {
        "审-7三处2": "$2e$、$\\zeta(-2)$、$N(0)$" in chain,
        "假连接": "假连接" in chain,
        "临-7不同源": "电子密度与配对荷不同源" in chain,
        "乘法内容": "Hecke 关系所需的乘法内容缺" in chain,
    }
    assert all(checks.values()), "P1: 原文审计失败 %s" % checks

    # ---------- P2/P3 ----------
    q_over_e = 2.0                      # 2e/e：用电荷单位归一
    zero_index = 2.0                    # zeta(-2) 的序号
    dos_natural = 1.0 / (2 * math.pi ** 2)   # m=kF=hbar=1 的单自旋 N(0)
    assert abs(dos_natural / q_over_e - 1 / (4 * math.pi ** 2)) < 1e-15
    ratio = q_over_e / dos_natural
    assert ratio > 10, "P3: 差异应 >10 倍，实测 %.1f" % ratio

    # 任意参考尺度可把 DOS 读成 2，但该尺度外生
    nref_for_two = dos_natural / 2.0
    assert abs(dos_natural / nref_for_two - 2.0) < 1e-12

    print("R40 三处'2'的对象辨析（结构审计，无拟合）：")
    print("  P1 原文：%s" % checks)
    print("  电荷：2e/e = 2.000（归一单位 e，电荷量纲）")
    print("  零点：zeta(-2) 序号 n = 2.000（无量纲整数）")
    print("  态密度：N(0) = 1/(2pi^2) = %.6f（自然单位，[E^-1 V^-1]）" % dos_natural)
    print("  与 2 相差 %.1f 倍；要读成 2 须选 N_ref=%.6f（外生）" % (ratio, nref_for_two))
    print("  P4 审-7/临-7 不闭合；P5 Lean")

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    ax = axes[0, 0]
    ax.axis("off")
    ax.text(0.02, 0.85, "$2e$", fontsize=16, weight="bold", color="#1f77b4")
    ax.text(0.02, 0.70, "对象：配对荷\n单位：电荷 [C]\n归一：$2e/e=2$\n来源：载流子成对", fontsize=10)
    ax.text(0.38, 0.85, "$\\zeta(-2)$", fontsize=16, weight="bold", color="#2ca02c")
    ax.text(0.38, 0.70, "对象：平凡零点序号\n单位：无量纲整数\n取值：$n=2$\n来源：$\\zeta(-n)=0$", fontsize=10)
    ax.text(0.75, 0.85, "$N(0)$", fontsize=16, weight="bold", color="#d62728")
    ax.text(0.75, 0.70, "对象：费米面态密度\n单位：$[E^{-1}V^{-1}]$\n自然单位：$1/2\\pi^2$\n来源：自旋/动量态计数", fontsize=9)
    ax.set_title("A  三处“2”：对象、单位、来源全不同")

    ax = axes[0, 1]
    labels = ["$2e/e$", "$\\zeta(-2)$ 序号", "$N(0)$ 自然单位"]
    vals = [q_over_e, zero_index, dos_natural]
    ax.bar(labels, vals, color=["#1f77b4", "#2ca02c", "#d62728"], alpha=0.85)
    ax.axhline(2.0, color="gray", ls="--", lw=1.2)
    ax.set_ylabel("无量纲读数")
    ax.set_ylim(0, 2.4)
    ax.set_title("B  前两者为 2，第三者差 %.1f 倍" % ratio)
    ax.grid(alpha=0.3, axis="y")

    ax = axes[1, 0]
    nrefs = np.logspace(-2, 0, 200)
    ratio_to_two = dos_natural / nrefs
    ax.plot(nrefs, ratio_to_two, "k-", lw=2.2, label="$N(0)/N_{ref}$")
    ax.axhline(2.0, color="r", ls="--", lw=1.4, label="读成 2")
    ax.plot([nref_for_two], [2.0], "o", ms=9, color="r")
    ax.set_xlabel("任意参考尺度 $N_{ref}$")
    ax.set_ylabel("$N(0)/N_{ref}$")
    ax.set_xscale("log")
    ax.set_title("C  DOS 读成 2 须外生参考尺度（与 $e$、序号无关）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")

    ax = axes[1, 1]
    ax.text(0.05, 0.80, "审-7 判定成立", fontsize=12, weight="bold", color="#d62728")
    ax.text(0.05, 0.65, "· $2e$ 不能由零点序号供给\n· 零点序号不能由 DOS 供给\n· DOS 不能以 $e$ 为单位归一", fontsize=10)
    ax.text(0.05, 0.35, "仍不闭合", fontsize=12, weight="bold")
    ax.text(0.05, 0.20, "· `审-7` 假连接（不升格）\n· `临-7` 电子密度与配对荷不同源\n· 26.B 乘法内容缺", fontsize=10)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_title("D  对象辨析不等于缺口闭合")

    fig.tight_layout()
    png = os.path.join(OUT, "R40_三处2的对象辨析.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "原文四处 %s" % checks, "通过"],
        ["P2", "Phi0=h/2e；zeta(-2)=0；N(0)=mkF/2pi^2hbar^3", "B 类标准"],
        ["P3", "DOS 自然值 %.6f，差 %.1f 倍" % (dos_natural, ratio), "对象不同"],
        ["P4", "审-7/临-7 不闭合", "状态不动"],
        ["P5", "不可同一（Lean）", "由 Lean 承载"],
        ["结论", "三处2是假连接", "状态不动"],
    ]
    with open(os.path.join(OUT, "R40_三处2的对象辨析_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
