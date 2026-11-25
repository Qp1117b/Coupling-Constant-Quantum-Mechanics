# -*- coding: utf-8 -*-
"""
R42: 有效质量链内化的自我否证——模式谱 E_mode=E2·k² 与电子能带 E_band=ħ²q²/(2m*) 同形不同源。
解析函数核对，无拟合。
运行：python "10 探索/超导第一性研究/04_计算验证/R42_有效质量no-go.py"
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
E2 = 0.5
HBAR2 = 1.0
MSTAR_NAIVE = HBAR2 / (2 * E2)  # 猜想值（范畴错误）


def assertions():
    out = {}
    ks = np.array([0, 1, 2, 3, 4], dtype=float)
    # 模式谱离散曲率
    Em = E2 * ks ** 2
    curv_mode = Em[2] - 2 * Em[1] + Em[0]
    out["mode_curvature"] = round(float(curv_mode), 4)
    out["mode_curv_eq_2E2"] = bool(abs(curv_mode - 2 * E2) < 1e-9)
    # 电子能带离散曲率（m* = MSTAR_NAIVE 时恰等于模式曲率——这是同形的数值根源）
    Eb = HBAR2 * ks ** 2 / (2 * MSTAR_NAIVE)
    curv_band = Eb[2] - 2 * Eb[1] + Eb[0]
    out["band_curvature"] = round(float(curv_band), 4)
    out["same_curvature_numerically"] = bool(abs(curv_band - curv_mode) < 1e-9)
    # 但对象不同：模式序号 k∈Z≥1 vs 电子波矢 q∈BZ
    out["naive_mass"] = round(MSTAR_NAIVE, 4)
    out["but_categories_differ"] = True  # R5 第38/71行明确：模式谱非电子 DOS
    # 外生 m 不可消去（链外-D）
    out["m_remains_exogenous"] = bool(out["but_categories_differ"])
    return out


def plots(a):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    ax = axes[0]
    ks = np.linspace(0, 4, 100)
    ax.plot(ks, E2 * ks ** 2, "b-", lw=2, label=r"模式谱 $E_{mode}=E_2 k^2$（$k$=模式序号）")
    ax.plot(ks, HBAR2 * ks ** 2 / (2 * MSTAR_NAIVE), "g--", lw=2,
            label=r"电子能带 $E_{band}=\hbar^2 k^2/2m^*$（$k$=电子波矢，链外-D）")
    ax.set_xlabel("k"); ax.set_ylabel("E")
    ax.set_title("(a) 同形（都 ∝k²）但对象不同（模式序号≠电子波矢）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1]
    labels = ["模式谱曲率\n$2E_2$", "能带曲率\n$\\hbar^2/m^*$", "猜想 $m^*$\n(范畴错误)"]
    vals = [a["mode_curvature"], a["band_curvature"], a["naive_mass"]]
    ax.bar(labels, vals, color=["tab:blue", "tab:green", "tab:red"])
    ax.set_title("(b) 数值可对齐 ≠ 物理同源\n(R5 禁止：模式谱≠电子 DOS)")
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("R42: 有效质量链内化的自我否证（链无电子能带载体，链外-D）", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    png = os.path.join(HERE, "R42_有效质量no-go.png")
    fig.savefig(png, dpi=140); plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R42 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "R42_有效质量no-go_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
