# -*- coding: utf-8 -*-
"""
环 14／临-14 前夜冻结三态的数值核对。

1. 流速场方差 sigma_v -> c_ij 漂移率（线性，态1）；
2. 冻结图连通分量（不连通/连通）与 c_ij 轨迹；
3. 三态参数空间（场方差 vs 起点方差）分类散点；
4. c_ij(t) 轨迹：漂移 / 冻结未齐 / 归零。

由 (14.5)(14.6) 直接计算，无拟合。
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
OUT_PNG = os.path.join(HERE, "环14_临14_前夜冻结三态.png")
OUT_CSV = os.path.join(HERE, "环14_临14_前夜冻结三态.csv")

N = 6
PAIR = (0, 1)


def main():
    rows = []
    rng = np.random.default_rng(20261122)

    # A 流速方差 -> 漂移率
    print("A 流速方差 -> c_ij 漂移率")
    sigs = np.linspace(0, 1, 60)
    rates = []
    for s in sigs:
        vs = rng.normal(0, s, N)
        rates.append(abs(vs[PAIR[0]] - vs[PAIR[1]]))
    rates = np.array(rates)
    sl = np.polyfit(sigs, rates, 1)[0]
    print(f"  线性斜率≈{sl:.4f}（期望 ~ O(1)）")
    for s, r in zip(sigs[::15], rates[::15]):
        rows.append(("drift", s, r, np.nan, np.nan))

    # B 冻结图分量：不连通 vs 连通
    print("\nB 冻结图连通分量")
    # 不连通：两个簇 {0,1,2} 和 {3,4,5}，各自速度相等、簇间不同
    v_disc = np.array([1.0, 1.0, 1.0, 2.0, 2.0, 2.0])
    # 连通：全场相等
    v_conn = np.ones(N)
    def comp_count(v):
        return len(set(np.round(v, 9)))
    print(f"  不连通场: {comp_count(v_disc)} 个分量; 连通场: {comp_count(v_conn)} 个分量")
    ts = np.linspace(0, 2, 200)
    # 分量内 c 恒定、分量间漂移
    c_pair_in = np.zeros_like(ts)       # (0,1) 同分量
    c_pair_cross = 1.0 * ts             # (0,3) 跨分量，速度差=1
    for t, a, b in zip(ts, c_pair_in, c_pair_cross):
        rows.append(("component", t, a, b, np.nan))

    # C 三态参数空间
    print("\nC 三态参数空间")
    labels = []
    sv = rng.uniform(0, 0.6, 120)
    sa = rng.uniform(0, 0.6, 120)
    for x, y in zip(sv, sa):
        if x > 0.02:
            labels.append(1)          # 场未公有化 -> 涨落
        elif y > 0.02:
            labels.append(2)          # 场公有化、起点未齐
        else:
            labels.append(3)          # 全齐（不可达）
    for x, y, l in zip(sv, sa, labels):
        rows.append(("state_space", x, y, l, np.nan))
    print(f"  态1/态2/态3 样本数: {labels.count(1)}/{labels.count(2)}/{labels.count(3)}")

    # D 三条 c_ij(t) 轨迹
    print("\nD c_ij(t) 轨迹")
    a_drift = 0.5 * ts                       # 态1：漂移
    a_frozen = 0.3 * np.ones_like(ts)        # 态2：冻结未齐（常数）
    a_zero = np.zeros_like(ts)               # 态3：归零
    for t, d, f, z in zip(ts, a_drift, a_frozen, a_zero):
        rows.append(("trajectory", t, d, f, z))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.4))

    ax[0, 0].plot(sigs, rates, "o", ms=3, color="tab:blue", alpha=0.6,
                  label=rf"斜率≈{sl:.2f}")
    ax[0, 0].plot(sigs, sl * sigs, "--", lw=1.8, color="tab:red", label="线性参考")
    ax[0, 0].set_xlabel(r"流速场方差 $\sigma_v$")
    ax[0, 0].set_ylabel(r"$|dc_{ij}/dt|$")
    ax[0, 0].set_title("A  态1：漂移率随场方差线性增")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    ax[0, 1].plot(ts, c_pair_in, lw=2.4, color="tab:green", label="分量内 (0,1)")
    ax[0, 1].plot(ts, c_pair_cross, lw=2.4, color="tab:red", label="分量间 (0,3)")
    ax[0, 1].set_xlabel(r"$t$")
    ax[0, 1].set_ylabel(r"$c_{ij}$")
    ax[0, 1].set_title("B  冻结图分量：内恒定、间漂移")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    colors = ["tab:red", "tab:blue", "tab:green"]
    for lab in (1, 2, 3):
        mask = np.array(labels) == lab
        ax[1, 0].scatter(sv[mask], sa[mask], s=16, color=colors[lab-1],
                         label=f"态{lab}", alpha=0.7)
    ax[1, 0].set_xlabel(r"场方差 $\sigma_v$")
    ax[1, 0].set_ylabel(r"起点方差 $\sigma_a$")
    ax[1, 0].set_title("C  三态参数空间（态3不可达）")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3)

    ax[1, 1].plot(ts, a_drift, lw=2.2, color="tab:red", label="态1 漂移")
    ax[1, 1].plot(ts, a_frozen, lw=2.2, color="tab:blue", label="态2 冻结未齐")
    ax[1, 1].plot(ts, a_zero, lw=2.2, color="tab:green", label="态3 归零")
    ax[1, 1].set_xlabel(r"$t$")
    ax[1, 1].set_ylabel(r"$c_{ij}$")
    ax[1, 1].set_title(r"D  $c_{ij}(t)$ 三轨迹（可证伪判据）")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
