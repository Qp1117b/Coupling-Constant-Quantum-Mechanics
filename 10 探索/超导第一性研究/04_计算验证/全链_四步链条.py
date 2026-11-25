# -*- coding: utf-8 -*-
"""
四步链条口径修正的数值示意（无拟合，直接由口径生成）。

① 差异化：差异方差上升；
② 扩大化：接入节点数上升；
③ 平均化：差异方差被拉向同一平均（下降）；
④ 危机化：平均量/线持续下降（变负＝推论），且带内化波动节奏。
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
OUT_PNG = os.path.join(HERE, "全链_四步链条.png")
OUT_CSV = os.path.join(HERE, "全链_四步链条.csv")


def main():
    rows = []
    rng = np.random.default_rng(20261122)
    t = np.linspace(0, 1, 200)

    # ① 差异化：方差上升（指数趋饱和）
    var1 = 1 - np.exp(-4 * t)
    print("① 差异化：方差 0 -> %.3f" % var1[-1])
    for x, y in zip(t[::40], var1[::40]):
        rows.append(("differentiation", x, y, np.nan, np.nan))

    # ② 扩大化：节点数上升（逻辑斯蒂）
    nodes = 50 / (1 + 9 * np.exp(-8 * t))
    print("② 扩大化：节点 5 -> %.1f" % nodes[-1])
    for x, y in zip(t[::40], nodes[::40]):
        rows.append(("expansion", x, y, np.nan, np.nan))

    # ③ 平均化：方差下降（残余底）
    var3 = 0.15 + 0.85 * np.exp(-5 * t)
    print("③ 平均化：方差 1 -> %.3f（残余底）" % var3[-1])
    for x, y in zip(t[::40], var3[::40]):
        rows.append(("averaging", x, y, np.nan, np.nan))

    # ④ 危机化：平均线下降 + 内化波动
    avg = 1.0 - 0.6 * t                       # 平均量持续下降
    osc = 0.03 * np.sin(20 * np.pi * t)       # 内化波动节奏
    avg_osc = avg + osc
    rate = np.gradient(avg, t)                # 增长率（恒负 = 变负推论）
    print("④ 危机化：平均线 1.0 -> %.3f，增长率 %.3f -> %.3f（变负）"
          % (avg_osc[-1], rate[0], rate[-1]))
    for x, y, z in zip(t[::40], avg_osc[::40], rate[::40]):
        rows.append(("crisis", x, y, z, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.4))

    ax[0, 0].plot(t, var1, lw=2.4, color="tab:blue")
    ax[0, 0].set_xlabel("进程")
    ax[0, 0].set_ylabel(r"差异方差 $\sigma^2$")
    ax[0, 0].set_title("① 差异化：差异产生")
    ax[0, 0].grid(alpha=0.3)

    ax[0, 1].plot(t, nodes, lw=2.4, color="tab:green")
    ax[0, 1].set_xlabel("进程")
    ax[0, 1].set_ylabel(r"接入节点 $N_t$")
    ax[0, 1].set_title("② 扩大化：差异扩张")
    ax[0, 1].grid(alpha=0.3)

    ax[1, 0].plot(t, var3, lw=2.4, color="tab:orange")
    ax[1, 0].axhline(0.15, color="0.4", ls="--", lw=1.2, label="残余底")
    ax[1, 0].set_xlabel("进程")
    ax[1, 0].set_ylabel(r"差异方差 $\sigma^2$")
    ax[1, 0].set_title("③ 平均化：差异被拉向同一平均")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3)

    ax[1, 1].plot(t, avg, lw=2.0, color="tab:red", label="平均线")
    ax[1, 1].plot(t, avg_osc, lw=1.2, color="tab:purple", alpha=0.8,
                  label="内化波动")
    ax2 = ax[1, 1].twinx()
    ax2.plot(t, rate, lw=1.8, color="tab:gray", ls="--", label="增长率（<0）")
    ax2.set_ylabel("增长率", color="tab:gray")
    ax[1, 1].set_xlabel("进程")
    ax[1, 1].set_ylabel("平均量")
    ax[1, 1].set_title("④ 危机化：平均线下降；变负为推论")
    ax[1, 1].legend(fontsize=7, loc="lower left")
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
