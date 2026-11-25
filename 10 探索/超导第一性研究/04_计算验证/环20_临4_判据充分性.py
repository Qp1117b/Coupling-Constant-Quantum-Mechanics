# -*- coding: utf-8 -*-
"""
环 20／临-4 判据充分性否证的数值核对。

1. 三点反例构型 tau=(1,-1,0), v=(0,0,1)；
2. 逐对贡献 (tau_i-tau_j)(v_i-v_j) = 0,-1,+1 相加为零；
3. dot D=0 的超平面：固定 tau，v3 任意时 dot D 恒零而速度不等（无判别力）；
4. 必要≠充分的集合包含示意。

由 (4.1) 直接计算，无拟合。
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
OUT_PNG = os.path.join(HERE, "环20_临4_判据充分性.png")
OUT_CSV = os.path.join(HERE, "环20_临4_判据充分性.csv")

TAU = np.array([1.0, -1.0, 0.0])
V = np.array([0.0, 0.0, 1.0])


def ddot(tau, v):
    pairs = [(0, 1), (0, 2), (1, 2)]
    return 2 * sum((tau[i] - tau[j]) * (v[i] - v[j]) for i, j in pairs)


def main():
    rows = []
    pairs = [(0, 1), (0, 2), (1, 2)]

    # A 构型
    print("A 三点反例构型")
    for i in range(3):
        print(f"  节点 {i}: tau={TAU[i]}, v={V[i]}")
        rows.append(("config", i, TAU[i], V[i], np.nan))

    # B 逐对贡献
    print("\nB 逐对贡献")
    terms = []
    for i, j in pairs:
        t = (TAU[i] - TAU[j]) * (V[i] - V[j])
        terms.append(t)
        print(f"  对({i},{j}): (tau_i-tau_j)={TAU[i]-TAU[j]:.1f}, "
              f"(v_i-v_j)={V[i]-V[j]:.1f}, 积={t:.1f}")
        rows.append(("term", i * 3 + j, t, np.nan, np.nan))
    print(f"  求和={sum(terms):.1f}, dot D={2*sum(terms):.1f}")

    # C dot D=0 超平面：v3 任意
    print("\nC dot D=0 超平面（无判别力）")
    vs = np.linspace(-2, 2, 200)
    ddots = []
    gaps = []
    for a in vs:
        vv = np.array([0.0, 0.0, a])
        ddots.append(ddot(TAU, vv))
        gaps.append(abs(vv[2] - vv[0]))
    ddots = np.array(ddots)
    print(f"  v3 从 -2 到 2：dot D 最大偏差={np.max(np.abs(ddots)):.3e}（恒 0）")
    print(f"  但 |v3-v1| 从 {gaps[0]:.1f} 到 {gaps[-1]:.1f}（速度不等）")
    for a, d, g in zip(vs[::40], ddots[::40], gaps[::40]):
        rows.append(("hyperplane", a, d, g, np.nan))

    # D 集合包含示意
    print("\nD 必要≠充分")
    print("  全对冻结子空间 < dot D=0 超平面（严格包含）")
    rows.append(("sets", 1, 1, 3, np.nan))  # 冻结=1维，超平面=3维示意

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.4))

    ax[0, 0].stem([0, 1, 2], TAU, linefmt="C0-", markerfmt="C0o",
                  basefmt=" ", label=r"$\tau$")
    ax[0, 0].stem([0, 1, 2], V, linefmt="C1-", markerfmt="C1s",
                  basefmt=" ", label=r"$v$")
    ax[0, 0].set_xlabel("节点")
    ax[0, 0].set_title("A  三点反例构型")
    ax[0, 0].legend(fontsize=9)
    ax[0, 0].grid(alpha=0.3)

    ax[0, 1].bar(["(0,1)", "(0,2)", "(1,2)"], terms,
                 color=["tab:blue", "tab:red", "tab:green"], alpha=0.85)
    ax[0, 1].axhline(0, color="0.3", lw=1)
    ax[0, 1].set_ylabel(r"$(\tau_i-\tau_j)(v_i-v_j)$")
    ax[0, 1].set_title("B  逐对贡献 0,-1,+1 相加为零")
    ax[0, 1].grid(alpha=0.3, axis="y")

    ax[1, 0].plot(vs, ddots, lw=2.2, color="tab:blue", label=r"$\dot D=0$")
    ax2 = ax[1, 0].twinx()
    ax2.plot(vs, gaps, lw=2.0, color="tab:red", label=r"$|v_3-v_1|$")
    ax[1, 0].set_xlabel(r"$v_3$")
    ax[1, 0].set_ylabel(r"$\dot D$", color="tab:blue")
    ax2.set_ylabel("速度差", color="tab:red")
    ax[1, 0].set_title("C  驻定不蕴含冻结（无判别力）")
    ax[1, 0].grid(alpha=0.3)

    ax[1, 1].add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False,
                                     edgecolor="tab:blue", lw=2))
    ax[1, 1].add_patch(plt.Rectangle((0.2, 0.2), 0.4, 0.4,
                                     facecolor="tab:green", alpha=0.35,
                                     edgecolor="tab:green", lw=2))
    ax[1, 1].text(0.4, 0.4, "全对冻结\n（必要）", ha="center", va="center", fontsize=10)
    ax[1, 1].text(0.5, 0.92, r"$\dot D=0$ 超平面（必要非充分）",
                  ha="center", fontsize=9)
    ax[1, 1].set_xlim(0, 1)
    ax[1, 1].set_ylim(0, 1)
    ax[1, 1].axis("off")
    ax[1, 1].set_title("D  必要集合严格包含充分集合")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
