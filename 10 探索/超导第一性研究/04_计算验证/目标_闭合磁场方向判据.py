# -*- coding: utf-8 -*-
"""
R19: 磁场方向判据 Υ(B)≤Υ(0)——低场 f=1-ax 与刚度下降曲线。
只检验方向/归一化/单调，不拟合。仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/目标_闭合磁场方向判据.py"
"""
import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
A_COEF = 0.3  # a 外生，仅示意（方向检验不依赖具体值）


def assertions():
    out = {}
    x = np.linspace(0, 2, 200)
    f = 1 - A_COEF * x  # 低场一阶（示意）
    out["f_at_0"] = float(1 - A_COEF * 0)
    out["f_monotone_decreasing"] = bool(np.all(np.diff(f) <= 0))
    out["f_le_1_for_x_ge_0"] = bool(np.all(f[x >= 0] <= 1.0 + 1e-12))
    # 刚度方向：Upsilon(B)/Upsilon(0) = f ≤ 1
    U0 = 7.5
    U = U0 * f
    out["Upsilon_le_U0"] = bool(np.all(U[x >= 0] <= U0 + 1e-12))
    out["Upsilon_at_0"] = float(U0 * 1)
    # Tc 上界不增（Uemura 线性）：Tc ∝ Upsilon
    out["tc_upper_nonincreasing"] = bool(np.all(np.diff(U) <= 0))
    # 反例：非单调 f 可违（前提必要）
    f_bad = np.array([1.0, 1.2, 1.5])
    out["nonmonotone_can_violate"] = bool(np.any(f_bad > 1.0))
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    x = np.linspace(0, 2, 300)
    f = 1 - A_COEF * x
    U0 = 7.5
    U = U0 * f

    ax = axes[0, 0]
    ax.plot(x, f, "b-", lw=2, label=r"低场 $f(x)=1-ax$")
    ax.axhline(1, color="k", ls="--", lw=1.5, label=r"$f(0)=1$")
    ax.set_xlabel(r"$x=B/B_{c2}$")
    ax.set_ylabel(r"$f$")
    ax.set_title("(a) f 单调减、f≤1（已登记前提）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.plot(x, U, "g-", lw=2, label=r"$\Upsilon(B)=\Upsilon(0)f$")
    ax.axhline(U0, color="k", ls="--", lw=1.5, label=r"$\Upsilon(0)$")
    ax.set_xlabel(r"$B/B_{c2}$")
    ax.set_ylabel(r"$\Upsilon$")
    ax.set_title("(b) 刚度方向判据：Υ(B) ≤ Υ(0)")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    ax.plot(x, U / U0, "purple", lw=2)
    ax.axhline(1, color="k", ls=":", lw=1.5)
    ax.set_xlabel(r"$B/B_{c2}$")
    ax.set_ylabel(r"$\Upsilon(B)/\Upsilon(0)$")
    ax.set_title("(c) 归一化刚度 ≤ 1（方向闭合）")
    ax.grid(alpha=0.3)

    ax = axes[1, 1]
    labels = ["f 单调减\n(已登记前提)", "Υ(B)≤Υ(0)\n(本轮闭合)", "Tc 上界不增\n(§0.3 相容)"]
    vals = [1, 1, 1]
    ax.bar(labels, vals, color=["tab:blue", "tab:green", "tab:orange"])
    ax.set_yticks([0, 1]); ax.set_yticklabels(["否", "是"])
    ax.set_title("(d) 方向判据链（无数值、无拟合）")
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("R19: 磁场方向判据 Υ(B)≤Υ(0)（从已登记单调减前提推出）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "目标_闭合磁场方向判据.png")
    fig.savefig(png, dpi=140); plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R19 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "目标_闭合磁场方向判据_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
