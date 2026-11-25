# -*- coding: utf-8 -*-
"""
环 19／`审-11` 的数值核对。

1. a(T)/(zJ) 与 b(T)/(zJ) 随 T/T0 的曲线（a 过零、b 单调下降、b(T0)=1/8）；
2. 平均场 vs 精确 Tc/J（Ising、XY、Heisenberg，简单立方）；
3. Ginzburg 临界区宽度 t_G 对 N=xi/a（d=2 斜率 -2，d=3 斜率 -6），标出超导体带；
4. 二维阶梯：平均场 2J → 裸刚度 BKT 1.571J → 精确 0.893J。

外部数值只进对照表，不参与曲线。
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
OUT_PNG = os.path.join(HERE, "环19_审11_Landau.png")
OUT_CSV = os.path.join(HERE, "环19_审11_Landau.csv")


def a_over_zJ(t):
    """a(T)/(zJ) with t = T/T0: (1/2)(1 - 1/t)."""
    t = np.asarray(t, dtype=float)
    return 0.5 * (1.0 - 1.0 / t)


def b_over_zJ(t):
    """b(T)/(zJ) with t = T/T0 and k_B T0 = zJ/2: 1/(8 t^3)."""
    t = np.asarray(t, dtype=float)
    return 1.0 / (8.0 * t ** 3)


def main():
    rows = []

    # ---------------- 1. 系数曲线
    for t in (0.5, 0.8, 1.0, 1.25, 2.0, 4.0):
        rows.append(("a_over_zJ", t, float(a_over_zJ(t)), 0.0, np.nan))
        rows.append(("b_over_zJ", t, float(b_over_zJ(t)), 0.125, np.nan))
    print("a(0.8)/zJ =", float(a_over_zJ(0.8)), " a(1.25)/zJ =", float(a_over_zJ(1.25)))
    print("b(1)/zJ =", float(b_over_zJ(1.0)), " (target 0.125)")
    print("b(2)/zJ =", float(b_over_zJ(2.0)), " (target 1/64 =", 1 / 64, ")")

    # ---------------- 2. 平均场 vs 精确（简单立方，z=6）
    models = [
        ("Ising", 1, 6.0, 4.511525),
        ("XY", 2, 3.0, 2.2019),
        ("Heisenberg", 3, 2.0, 1.442928),
    ]
    print("\n模型      MF Tc/J   精确 Tc/J   比值      偏差")
    for name, n, mf, ex in models:
        ratio = ex / mf
        dev = (ex - mf) / mf
        print(f"{name:10s} {mf:8.4f} {ex:10.6f} {ratio:9.5f} {dev*100:8.2f}%")
        rows.append(("tc_compare", n, mf, ex, ratio))

    # ---------------- 3. Ginzburg 宽度
    print("\nGinzburg  t_G = N^(-2d/(4-d))")
    for d in (2, 3):
        expo = 2 * d / (4 - d)
        for N in (1.0, 10.0, 100.0, 1000.0):
            tg = N ** (-expo)
            rows.append((f"tG_d{d}", N, tg, expo, np.nan))
            print(f"  d={d}  N={N:7.1f}  t_G={tg:.3e}  (exponent {expo:.3f})")

    # ---------------- 4. 二维阶梯
    ladder = [("平均场 T0", 2.0), ("裸刚度 BKT", np.pi / 2), ("精确 BKT", 0.8933)]
    print("\n二维阶梯（z=4，以 J 为单位）")
    for lab, val in ladder:
        print(f"  {lab}: {val:.4f}")
        rows.append(("ladder_2d", val, np.nan, np.nan, np.nan))

    # ---------------- CSV
    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    # ---------------- 画图
    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A: 系数
    tt = np.linspace(0.4, 4.0, 800)
    ax[0, 0].plot(tt, a_over_zJ(tt), lw=2.2, color="tab:blue", label=r"$a(T)/(zJ)$")
    ax[0, 0].plot(tt, b_over_zJ(tt), lw=2.2, color="tab:red", label=r"$b(T)/(zJ)$")
    ax[0, 0].axhline(0.0, color="0.35", lw=0.9, ls=":")
    ax[0, 0].axvline(1.0, color="0.35", lw=0.9, ls="--")
    ax[0, 0].plot([1.0], [0.125], "o", color="tab:red", ms=6)
    ax[0, 0].annotate(r"$b(T_0)/(zJ)=1/8$", xy=(1.0, 0.125), xytext=(1.35, 0.30),
                      fontsize=9, arrowprops=dict(arrowstyle="->", lw=0.8))
    ax[0, 0].text(1.03, -0.35, r"$T_0$", fontsize=10)
    ax[0, 0].set_xlabel(r"$t=T/T_0$")
    ax[0, 0].set_ylabel("系数（以 $zJ$ 为单位）")
    ax[0, 0].set_title("A  平均场 Landau 系数")
    ax[0, 0].set_ylim(-0.75, 1.05)
    ax[0, 0].legend(fontsize=9)
    ax[0, 0].grid(alpha=0.3)

    # B: MF vs 精确
    names = [m[0] for m in models]
    mf_vals = [m[2] for m in models]
    ex_vals = [m[3] for m in models]
    x = np.arange(len(names))
    w = 0.36
    ax[0, 1].bar(x - w / 2, mf_vals, w, label="平均场", color="tab:gray", alpha=0.85)
    ax[0, 1].bar(x + w / 2, ex_vals, w, label="精确（MC）", color="tab:green", alpha=0.85)
    for i, (m, e) in enumerate(zip(mf_vals, ex_vals)):
        ax[0, 1].text(i, max(m, e) + 0.12, f"{e/m:.3f}", ha="center", fontsize=9)
    ax[0, 1].set_xticks(x)
    ax[0, 1].set_xticklabels([f"{n}\n(n={m[1]})" for n, m in zip(names, models)])
    ax[0, 1].set_ylabel(r"$k_BT_c/J$")
    ax[0, 1].set_title("B  平均场高估 $T_c$（简单立方，$z=6$）")
    ax[0, 1].legend(fontsize=9)
    ax[0, 1].grid(alpha=0.3, axis="y")

    # C: Ginzburg
    NN = np.logspace(0.0, 3.5, 600)
    ax[1, 0].loglog(NN, NN ** -2.0, lw=2.2, color="tab:orange", label=r"$d=2:\ N^{-2}$")
    ax[1, 0].loglog(NN, NN ** -6.0, lw=2.2, color="tab:blue", label=r"$d=3:\ N^{-6}$")
    ax[1, 0].axvspan(1e2, 1e3, color="tab:green", alpha=0.15)
    ax[1, 0].text(1.5e2, 3e-3, "常规三维\n超导体", fontsize=8, color="tab:green")
    ax[1, 0].set_xlabel(r"$N=\xi_0/a$")
    ax[1, 0].set_ylabel(r"$t_G$")
    ax[1, 0].set_title("C  Ginzburg 临界区宽度与环 6 的 $N$")
    ax[1, 0].set_ylim(1e-20, 10.0)
    ax[1, 0].legend(fontsize=9, loc="lower left")
    ax[1, 0].grid(alpha=0.3, which="both")

    # D: 二维阶梯
    labs = [l for l, _ in ladder]
    vals = [v for _, v in ladder]
    ax[1, 1].barh(labs[::-1], vals[::-1], color=["tab:blue", "tab:orange", "tab:red"][::-1],
                  alpha=0.85)
    for i, v in enumerate(vals[::-1]):
        ax[1, 1].text(v + 0.04, i, f"{v:.3f}", va="center", fontsize=10)
    ax[1, 1].set_xlabel(r"$k_BT/J$（$z=4$，以 $J$ 为单位）")
    ax[1, 1].set_title("D  二维：平均场 → 裸刚度 BKT → 精确")
    ax[1, 1].set_xlim(0.0, 2.4)
    ax[1, 1].grid(alpha=0.3, axis="x")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
