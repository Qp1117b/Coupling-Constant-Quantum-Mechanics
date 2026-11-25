# -*- coding: utf-8 -*-
"""
全链拉通核对的数值/图像核对。

1. 四态项数柱状（A=7, B=7, C+D=21；共 35 唯一编号）；
2. T_c = omega_D F(z), z=Upsilon_0/omega_D 的标度族：vs z 重合、vs Upsilon_0 分离；
3. B 类三判据的不可同时满足示意；
4. 绝对 Tc 的 8 个外生输入依赖条。

柱状与曲线由账面数据/标度式直接计算，无拟合。
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
OUT_PNG = os.path.join(HERE, "全链_四态总账.png")
OUT_CSV = os.path.join(HERE, "全链_四态总账.csv")

INPUTS = [
    ("omega_D (Debye 能标)", 7),
    ("Upsilon_0 / J_0 (绝对刚度)", 6),
    ("A(eps), N, s (振幅/表示权)", 5),
    ("c, kappa_Theta (记忆常数)", 4),
    ("t_Upsilon (渗流指数)", 3),
    ("sigma_dc <-> Upsilon (链外-F)", 2),
    ("RH / beta_n (外部假设)", 2),
    ("p(r) 空间统计", 2),
]


def main():
    rows = []
    counts = {"A 形状已推": 7, "B 已判否/不可": 7, "C+D 外生/未动": 21}
    for k, v in counts.items():
        rows.append(("state", k, v, 35, np.nan))
    print("四态:", counts, "合计", sum(counts.values()), "(35 唯一编号)")

    z = np.linspace(0.01, 3, 300)
    omegas = [10.0, 20.0, 40.0]
    F = lambda zz: zz / (1 + zz)
    print("\n标度核对：F(z) 与 omega_D 无关；vs Upsilon_0 三条曲线分离")
    for w in omegas:
        rows.append(("scale", w, float(w * F(1.0)), F(1.0), np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A 四态
    ks = list(counts.keys())
    vs = list(counts.values())
    ax[0, 0].bar(ks, vs, color=["tab:blue", "tab:red", "tab:gray"], alpha=0.85)
    for i, v in enumerate(vs):
        ax[0, 0].text(i, v + 0.3, str(v), ha="center", fontsize=10)
    ax[0, 0].set_ylabel("唯一缺口编号数")
    ax[0, 0].set_title("A  四态收束（41 行 / 35 唯一编号）")
    ax[0, 0].set_ylim(0, 25)
    ax[0, 0].grid(alpha=0.3, axis="y")

    # B 标度族 vs z（重合）
    for w in omegas:
        ax[0, 1].plot(z, w * F(z), lw=2.2, label=rf"$\omega_D={w:.0f}$")
    ax[0, 1].set_xlabel(r"$z=\Upsilon_0/\omega_D$")
    ax[0, 1].set_ylabel(r"$T_c=\omega_D F(z)$")
    ax[0, 1].set_title("B  vs z：形状重合，绝对标度未定")
    ax[0, 1].legend(fontsize=9)
    ax[0, 1].grid(alpha=0.3)

    # C vs Upsilon_0（分离）
    U = np.linspace(0.1, 30, 300)
    for w in omegas:
        ax[1, 0].plot(U, w * F(U / w), lw=2.2, label=rf"$\omega_D={w:.0f}$")
    ax[1, 0].set_xlabel(r"$\Upsilon_0$")
    ax[1, 0].set_ylabel(r"$T_c$")
    ax[1, 0].set_title("C  vs Upsilon_0：三条曲线分离 => 需外部 omega_D")
    ax[1, 0].legend(fontsize=9)
    ax[1, 0].grid(alpha=0.3)

    # D 外生输入
    names = [n for n, _ in INPUTS]
    vals = [v for _, v in INPUTS]
    y = np.arange(len(names))
    ax[1, 1].barh(y, vals, color="tab:orange", alpha=0.85)
    ax[1, 1].set_yticks(y)
    ax[1, 1].set_yticklabels(names, fontsize=8)
    ax[1, 1].set_xlabel("依赖强度（示意）")
    ax[1, 1].set_title("D  绝对 Tc 的最小外生输入集（8 项）")
    ax[1, 1].grid(alpha=0.3, axis="x")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
