# -*- coding: utf-8 -*-
"""
全链第三次核对（第 37 轮）的账面图像。

1. 四态分布 A=19 / B=6 / C+D=10；
2. §16 账面：行数 51→52，唯一编号恒 35，重复 16→17；
3. 推进唯一编号 24→25（新增临-12，A 类）。

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
OUT_PNG = os.path.join(HERE, "全链_第三次核对.png")
OUT_CSV = os.path.join(HERE, "全链_第三次核对.csv")


def main():
    rows = []
    for k, v in [("A", 19), ("B", 6), ("C+D", 10)]:
        rows.append(("state", k, v, 35, np.nan))
    for k, v in [("rows_audit2", 51), ("rows_audit3", 52), ("unique", 35),
                 ("dups_audit2", 16), ("dups_audit3", 17),
                 ("advanced_audit2", 24), ("advanced_audit3", 25),
                 ("A_audit2", 18), ("A_audit3", 19)]:
        rows.append(("ledger", k, v, np.nan, np.nan))
    rows.append(("new_item", "临-12", 1, np.nan, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(1, 3, figsize=(15.6, 4.6))

    ax[0].bar(["A 形状已推", "B 已判否", "C+D 外生/未动"], [19, 6, 10],
              color=["tab:blue", "tab:red", "tab:gray"], alpha=0.85)
    for i, v in enumerate([19, 6, 10]):
        ax[0].text(i, v + 0.3, str(v), ha="center", fontsize=10)
    ax[0].set_ylabel("唯一缺口编号数")
    ax[0].set_title("A  四态分布（共 35）")
    ax[0].set_ylim(0, 23)
    ax[0].grid(alpha=0.3, axis="y")

    labels = ["行数", "唯一编号", "重复行"]
    x = np.arange(3)
    ax[1].bar(x - 0.18, [51, 35, 16], 0.36, label="第二次（第36轮）",
              color="tab:blue", alpha=0.8)
    ax[1].bar(x + 0.18, [52, 35, 17], 0.36, label="第三次（第37轮）",
              color="tab:orange", alpha=0.8)
    ax[1].set_xticks(x)
    ax[1].set_xticklabels(labels)
    ax[1].set_title("B  §16 账面变化")
    ax[1].legend(fontsize=8)
    ax[1].grid(alpha=0.3, axis="y")

    ax[2].step([0, 26, 36, 37, 40], [0, 14, 24, 25, 25], where="post",
               lw=2.2, color="tab:green")
    ax[2].plot([26, 36, 37], [14, 24, 25], "o", color="tab:green", ms=7)
    ax[2].annotate("临-12", (37, 25), textcoords="offset points",
                   xytext=(-8, 12), fontsize=9)
    ax[2].set_xlabel("轮次")
    ax[2].set_ylabel("已实质推进的唯一编号数")
    ax[2].set_title(r"C  推进数 24 $\to$ 25（新增临-12）")
    ax[2].set_ylim(0, 29)
    ax[2].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("账面：52 行 / 35 唯一 / 25 推进（A19+B6）/ 10 余")
    print("saved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
