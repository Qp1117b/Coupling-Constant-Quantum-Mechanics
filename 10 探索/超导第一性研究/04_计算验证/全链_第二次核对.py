# -*- coding: utf-8 -*-
"""
全链第二次核对（第 27–36 轮）的账面图像。

1. 四态分布 A=18 / B=6 / C+D=11；
2. §16 账面：行数 41→51，唯一编号恒 35，重复 6→16；
3. 推进唯一编号 14→24（示意阶梯）；
4. 新增 10 项的态分布。

账面数据来自主链 §16 的表面积分，无拟合。
"""

import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "全链_第二次核对.png")
OUT_CSV = os.path.join(HERE, "全链_第二次核对.csv")

NEW = [
    ("审-13", "B"), ("G19", "A"), ("临-26", "A"), ("D1", "A"), ("临-19", "A"),
    ("临-24", "A"), ("临-11", "A"), ("临-17", "A"), ("临-1", "A"), ("临-18", "A"),
]


def main():
    rows = []
    for k, v in [("A", 18), ("B", 6), ("C+D", 11)]:
        rows.append(("state", k, v, 35, np.nan))
    for k, v in [("rows_audit1", 41), ("rows_audit2", 51), ("unique", 35),
                 ("dups_audit1", 6), ("dups_audit2", 16),
                 ("advanced_audit1", 14), ("advanced_audit2", 24)]:
        rows.append(("ledger", k, v, np.nan, np.nan))
    for g, s in NEW:
        rows.append(("new_item", g, 1 if s == "A" else 0, np.nan, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    ax[0, 0].bar(["A 形状已推", "B 已判否", "C+D 外生/未动"], [18, 6, 11],
                 color=["tab:blue", "tab:red", "tab:gray"], alpha=0.85)
    for i, v in enumerate([18, 6, 11]):
        ax[0, 0].text(i, v + 0.3, str(v), ha="center", fontsize=10)
    ax[0, 0].set_ylabel("唯一缺口编号数")
    ax[0, 0].set_title("A  四态分布（共 35）")
    ax[0, 0].set_ylim(0, 22)
    ax[0, 0].grid(alpha=0.3, axis="y")

    labels = ["行数", "唯一编号", "重复行"]
    a1 = [41, 35, 6]
    a2 = [51, 35, 16]
    x = np.arange(3)
    ax[0, 1].bar(x - 0.18, a1, 0.36, label="第一次（第26轮）", color="tab:blue", alpha=0.8)
    ax[0, 1].bar(x + 0.18, a2, 0.36, label="第二次（第36轮）", color="tab:orange", alpha=0.8)
    ax[0, 1].set_xticks(x)
    ax[0, 1].set_xticklabels(labels)
    ax[0, 1].set_title("B  §16 账面变化")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3, axis="y")

    ax[1, 0].step([0, 26, 36, 40], [0, 14, 24, 24], where="post", lw=2.2,
                  color="tab:green")
    ax[1, 0].plot([26, 36], [14, 24], "o", color="tab:green", ms=7)
    ax[1, 0].set_xlabel("轮次")
    ax[1, 0].set_ylabel("已实质推进的唯一编号数")
    ax[1, 0].set_title(r"C  推进数 14 $\to$ 24（示意阶梯）")
    ax[1, 0].set_ylim(0, 28)
    ax[1, 0].grid(alpha=0.3)

    names = [g for g, _ in NEW]
    vals = [1 if s == "A" else 0 for _, s in NEW]
    ax[1, 1].barh(names, vals, color=["tab:blue" if v else "tab:red" for v in vals], alpha=0.85)
    ax[1, 1].set_xlabel("A=1 / B=0")
    ax[1, 1].set_title("D  新增 10 项的判定（B 仅审-13）")
    ax[1, 1].set_xlim(0, 1.2)
    ax[1, 1].grid(alpha=0.3, axis="x")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("账面：51 行 / 35 唯一 / 24 推进（A18+B6）/ 11 余")
    print("saved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
