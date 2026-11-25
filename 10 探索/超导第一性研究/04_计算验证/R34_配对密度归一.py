# -*- coding: utf-8 -*-
"""
R34：临-26 的 2 配对基准密度归一
=====================================================================
预注册 R34 的 P1–P5（跑数前写死）：
  P1 13.A6 两式审计
  P2 外部测度标准：概率密度总质量 1；<1 为次概率
  P3 sum rho2=1；sum rhon=2/n
  P4 与 12.3 同数不同物
  P5 Lean 3 点域代数

复跑：python "10 探索/超导第一性研究/04_计算验证/R34_配对密度归一.py"
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
    # ---------- P1：原文审计 ----------
    chain = open(os.path.join(ROOT, "10 探索", "CQM_探索_推导链.md"), encoding="utf-8").read()
    checks = {
        "基准密度定义": "p_{\\rm pair}^{(2)}(i)/\\sum_{j\\in D_i}p_{\\rm pair}^{(2)}(j)" in chain,
        "高通道降权": "\\rho_{\\rm pair}^{(n)}=\\frac{2}{n}\\rho_{\\rm pair}^{(2)}" in chain,
        "结构非等式": "结构分解" in chain and "不是已证等式" in chain,
        "临-26物理归一": "2 配对基准密度的物理归一未证" in chain,
    }
    assert all(checks.values()), "P1: 原文审计失败 %s" % checks

    # ---------- P3：3 点域归一 ----------
    p2 = np.array([0.3, 1.7, 0.8])          # 示意 p^{(2)}(i)（外生）
    rho2 = p2 / p2.sum()
    assert abs(float(rho2.sum()) - 1.0) < 1e-12, "P3: rho2 未归一"

    ns = np.arange(2, 21, 2)
    masses = []
    for n in ns:
        rhon = (2.0 / n) * rho2
        m = float(rhon.sum())
        masses.append(m)
        assert abs(m - 2.0 / n) < 1e-12, "P3: n=%d 总质量错 %.6f" % (n, m)
    masses = np.array(masses)
    assert abs(masses[0] - 1.0) < 1e-12 and np.all(masses[1:] < 1.0), "P3: n>2 应为次概率"

    # ---------- P4：同数不同物 ----------
    # 12.3 的荷量子归一读 Φ_n/Φ_2=2/n，与密度总质量同数；R32 已判对象不同。
    flux_unit_ratio = 2.0 / ns
    assert np.max(np.abs(masses - flux_unit_ratio)) < 1e-12, "P4: 同数确认"

    print("R34 配对密度归一（结构恒等式，无拟合）：")
    print("  P1 原文：%s" % checks)
    print("  P2 外部：概率密度总质量 1；<1 为有限测度／次概率（B 类）")
    print("  P3 sum rho2 = %.12f；sum rhon = 2/n（n=2 为 1，n>2 为次概率）" % rho2.sum())
    print("  P4 密度总质量 2/n 与 12.3 单位磁通量子比同数不同物（R32）")
    print("  P5 Lean 3 点域代数")

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    ax = axes[0, 0]
    ax.bar(["$i_1$", "$i_2$", "$i_3$"], rho2, color="#1f77b4", alpha=0.85)
    ax.axhline(1.0 / 3, color="gray", ls=":", lw=1.2)
    ax.set_ylabel("$\\rho^{(2)}(i)$")
    ax.set_title("A  2 配对基准密度（3 点域示意，$\\sum=1$）")
    ax.grid(alpha=0.3, axis="y")

    ax = axes[0, 1]
    ax.plot(ns, masses, "o-", lw=2.2, ms=6, color="#d62728", label="$\\sum_i\\rho^{(n)}(i)=2/n$")
    ax.axhline(1.0, color="gray", ls="--", lw=1.4, label="概率归一质量 $=1$")
    ax.set_xlabel("$n$")
    ax.set_ylabel("总质量")
    ax.set_ylim(0, 1.15)
    ax.set_title("B  $n>2$ 为次概率质量（不是概率密度）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    width = 0.26
    for idx, (n, color) in enumerate([(2, "#2ca02c"), (4, "#1f77b4"), (8, "#d62728")]):
        rhon = (2.0 / n) * rho2
        ax.bar(np.arange(3) + (idx - 1) * width, rhon, width, color=color,
               alpha=0.85, label="$n=%d$（质量 $%.3f$）" % (n, rhon.sum()))
    ax.set_xticks(np.arange(3))
    ax.set_xticklabels(["$i_1$", "$i_2$", "$i_3$"])
    ax.set_ylabel("$\\rho^{(n)}(i)$")
    ax.set_title("C  高通道降权：形状相同、总质量递减")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, axis="y")

    ax = axes[1, 1]
    ax.plot(ns, masses, "o-", lw=2.2, ms=6, label="密度总质量 $2/n$")
    ax.plot(ns, flux_unit_ratio, "s--", lw=1.8, ms=5, label="12.3 单位磁通量子比 $2/n$")
    ax.annotate("同数不同物\n（R32 对象辨析）", (6, 0.24), fontsize=9)
    ax.set_xlabel("$n$")
    ax.set_ylabel("数值")
    ax.set_title("D  数值恒等不推出物理同一")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    fig.tight_layout()
    png = os.path.join(OUT, "R34_配对密度归一.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "13.A6 四处 %s" % checks, "通过"],
        ["P2", "概率密度质量 1；<1 次概率", "外部标准（B 类）"],
        ["P3", "sum rho2=1；sum rhon=2/n", "构造恒等式"],
        ["P4", "与 12.3 同数不同物", "不升格"],
        ["P5", "3 点域代数（Lean）", "由 Lean 承载"],
        ["结论", "数学归一成立；物理归一仍缺", "临-26 状态不动"],
    ]
    with open(os.path.join(OUT, "R34_配对密度归一_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
