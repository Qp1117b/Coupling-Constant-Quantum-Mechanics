# -*- coding: utf-8 -*-
"""
R39：第六纯数与五纯数网络的代数闭环
=====================================================================
预注册 R39 的 P1–P5（跑数前写死）：
  P1 六纯数登记审计
  P2 AB T->0 关系（B 类）
  P3 R6=R1*R3^2/16, R6/R1=pi/4
  P4 不引入新生成元
  P5 Lean 代数恒等式

复跑：python "10 探索/超导第一性研究/04_计算验证/R39_六纯数闭环.py"
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
    lean5 = open(os.path.join(ROOT, "10 探索", "超导第一性研究", "05_Lean验证",
                              "FiveRatioNetwork.lean"), encoding="utf-8").read()
    checks = {
        "R6登记": "第 6 纯数" in ledger and "2.77069" in ledger,
        "五纯数网络": "五纯数一致性网络" in ledger,
        "R3平方": "R3_sq" in lean5 and "4 * Real.pi" in lean5,
        "R4恒等式": "R_4\\cdot2\\kappa^2=R_2" in ledger,
    }
    assert all(checks.values()), "P1: 登记审计失败 %s" % checks

    # ---------- P3：六纯数 ----------
    R1 = 2 * math.pi / math.exp(GAMMA)
    R2 = 12 / (7 * ZETA3)
    R3 = 2 * math.sqrt(math.pi)
    R4 = 3 / (4 * math.exp(2 * GAMMA))
    kappa = 2 * math.sqrt(2) * math.exp(GAMMA) / math.sqrt(7 * ZETA3)
    R6 = math.pi ** 2 / (2 * math.exp(GAMMA))

    resid = {
        "R3^2=4pi": abs(R3 ** 2 - 4 * math.pi),
        "R4*2k^2=R2": abs(R4 * 2 * kappa ** 2 - R2),
        "R6=R1*R3^2/16": abs(R6 - R1 * R3 ** 2 / 16),
        "R6/R1=pi/4": abs(R6 / R1 - math.pi / 4),
    }
    # 预注册阈值为相对残差 <1e-15（双精度绝对舍入约 1e-15）
    for k, v in resid.items():
        scale = max(abs(R6), abs(R1), abs(R3), abs(R2), 1.0)
        assert v / scale < 1e-15, "P3: %s 相对残差 %.3e" % (k, v / scale)

    print("R39 六纯数闭环（代数，无拟合）：")
    print("  P1 登记：%s" % checks)
    print("  R1=%.6f  R2=%.6f  R3=%.6f  R4=%.6f  kappa=%.6f  R6=%.6f"
          % (R1, R2, R3, R4, kappa, R6))
    for k, v in resid.items():
        print("    %-18s 残差 %.3e" % (k, v))
    print("  P4 第六纯数由 R1 与 R3 生成：R6=R1*R3^2/16=(pi/4)R1")
    print("  P5 Lean 代数恒等式")

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    ax = axes[0, 0]
    names = ["$R_1$", "$R_2$", "$R_3$", "$R_4$", "$\\kappa$", "$R_6$"]
    vals = [R1, R2, R3, R4, kappa, R6]
    ax.bar(names, vals, color=["#1f77b4"] * 5 + ["#d62728"], alpha=0.85)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.08, "%.4f" % v, ha="center", fontsize=9)
    ax.set_ylim(0, 4.2)
    ax.set_ylabel("纯数")
    ax.set_title("A  六个链内无参数纯数（$R_6$ 红）")
    ax.grid(alpha=0.3, axis="y")

    ax = axes[0, 1]
    ks = list(resid.keys())
    vs = [max(v, 1e-18) for v in resid.values()]
    ax.bar(range(4), vs, color="#2ca02c", alpha=0.85)
    ax.set_yscale("log")
    ax.set_xticks(range(4))
    ax.set_xticklabels(ks, fontsize=8)
    ax.set_ylabel("绝对残差")
    ax.set_title("B  四条恒等式残差（双精度舍入）")
    ax.grid(alpha=0.3, which="both", axis="y")

    ax = axes[1, 0]
    ax.text(0.02, 0.83, "生成元层", fontsize=12, weight="bold")
    ax.text(0.05, 0.68, "$e^\\gamma$     $\\zeta_3$     $\\pi$", fontsize=13)
    ax.annotate("", xy=(0.22, 0.45), xytext=(0.16, 0.65), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.50, 0.45), xytext=(0.50, 0.65), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.78, 0.45), xytext=(0.82, 0.65), arrowprops=dict(arrowstyle="->"))
    ax.text(0.05, 0.35, "$R_1=2\\pi/e^\\gamma$", fontsize=10, color="#1f77b4")
    ax.text(0.38, 0.35, "$R_2,R_4,\\kappa$", fontsize=10, color="#1f77b4")
    ax.text(0.72, 0.35, "$R_3=2\\sqrt{\\pi}$", fontsize=10, color="#1f77b4")
    ax.annotate("", xy=(0.50, 0.14), xytext=(0.22, 0.30), arrowprops=dict(arrowstyle="->", color="#d62728"))
    ax.annotate("", xy=(0.50, 0.14), xytext=(0.78, 0.30), arrowprops=dict(arrowstyle="->", color="#d62728"))
    ax.text(0.34, 0.06, "$R_6=R_1R_3^2/16$", fontsize=12, color="#d62728", weight="bold")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_title("C  第六纯数由 $R_1$ 与 $R_3$ 生成")

    ax = axes[1, 1]
    ax.text(0.05, 0.78, "成立", fontsize=12, weight="bold", color="#2ca02c")
    ax.text(0.05, 0.63, "· 六纯数代数闭环\n· $R_6=(\\pi/4)R_1$\n· AB $T\\to0$ 给 $I_cR_n=\\pi\\Delta_0/2e$", fontsize=10)
    ax.text(0.05, 0.38, "边界", fontsize=12, weight="bold", color="#d62728")
    ax.text(0.05, 0.23, "· 不闭合任何缺口\n· 不重判 2 生成元口径\n· 隧道极限外（高透明 SNS）不在范围", fontsize=10)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_title("D  代数闭环的边界")

    fig.tight_layout()
    png = os.path.join(OUT, "R39_六纯数闭环.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "六纯数登记 %s" % checks, "通过"],
        ["P2", "AB T->0：IcRn=pi*Delta0/2e", "外部标准（B 类）"],
        ["P3", "四条恒等式残差 <1e-15", "通过"],
        ["P4", "R6 由 R1 与 R3 生成", "无新生成元"],
        ["P5", "代数恒等式（Lean）", "由 Lean 承载"],
        ["结论", "第六纯数并入五纯数网络", "状态不动"],
    ]
    with open(os.path.join(OUT, "R39_六纯数闭环_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
