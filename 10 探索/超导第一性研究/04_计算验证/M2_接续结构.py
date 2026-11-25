# -*- coding: utf-8 -*-
"""
R26: M2 接续结构——κ_f/g 比值与共享因子消去核对。
无拟合（代数恒等核对）。仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/M2_接续结构.py"
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


def variance(k, s, r):
    return 2 * k**2 * s * (1 - r)


def pairing(g, s, r, hw):
    return 4 * g**2 * s * (1 - r) / hw


def assertions():
    out = {}
    k, g, r, hw = 0.0796, 1.0, 0.4, 1.0
    # 比值公式
    for s in [0.5, 1.0, 2.0]:
        ratio = variance(k, s, r) / pairing(g, s, r, hw)
        formula = (hw / 2) * (k / g)**2
        out[f"ratio_s{s}"] = float(ratio)
        out[f"formula_match_s{s}"] = bool(abs(ratio - formula) < 1e-12)
    # 与 s 无关
    out["independent_of_shared"] = bool(
        abs(out["ratio_s0.5"] - out["ratio_s2.0"]) < 1e-12
    )
    out["kappa_over_g_squared"] = float((k / g)**2)
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    k, g, r, hw = 0.0796, 1.0, 0.4, 1.0

    ax = axes[0, 0]
    ss = np.linspace(0.2, 2.0, 100)
    ax.plot(ss, [variance(k, s, r) for s in ss], "b-", lw=2, label="(9.1) 方差读出")
    ax.plot(ss, [pairing(g, s, r, hw) for s in ss], "g-", lw=2, label="(10.2) 配对强度")
    ax.set_xlabel(r"共享因子 $\sigma_0^2$"); ax.set_ylabel("值")
    ax.set_title("(a) 两式共享 σ²(1-ρ)")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ratios = [variance(k, s, r) / pairing(g, s, r, hw) for s in ss]
    ax.plot(ss, ratios, "purple", lw=2)
    ax.axhline((hw/2)*(k/g)**2, color="k", ls="--", label=r"$(\hbar\omega/2)(\kappa_f/g)^2$")
    ax.set_xlabel(r"$\sigma_0^2$"); ax.set_ylabel("方差/配对")
    ax.set_title("(b) 比值与共享因子无关（消去）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    gs = np.linspace(0.5, 2.0, 100)
    ax.plot(gs, [(hw/2)*(k/x)**2 for x in gs], "orange", lw=2)
    ax.set_xlabel(r"$g$（外生）"); ax.set_ylabel(r"$(\hbar\omega/2)(\kappa_f/g)^2$")
    ax.set_title("(c) 接续比随 g（κ_f=1/4π）"); ax.grid(alpha=0.3)

    ax = axes[1, 1]
    labels = ["(9.1)\nκ_f 响应", "接续比\nκ_f/g", "(10.2)\ng 响应"]
    vals = [1, 1, 1]
    ax.bar(labels, vals, color=["tab:blue", "tab:purple", "tab:green"])
    ax.set_yticks([])
    ax.set_title("(d) M2：方差→接续比→配对（结构）")
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("R26: M2 接续结构 κ_f/g（代数恒等，无拟合）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "M2_接续结构.png")
    fig.savefig(png, dpi=140); plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R26 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "M2_接续结构_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
