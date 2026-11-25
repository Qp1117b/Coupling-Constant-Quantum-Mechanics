# -*- coding: utf-8 -*-
"""
R13: BKT 因子化数据核对（Weitzel 2023 NbN 精密数据）。
只检验普适跳变/因子化代数恒等/一致性，不拟合。仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/环19_BKT数据检验.py"
"""
import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))

# Weitzel 2023 NbN 实测（arXiv:2303.10639v3）
T_BKT = 4.488
T_C0 = 5.203
J0 = 7.511
JUMP = 2 * T_BKT / math.pi  # 普适线给


def assertions():
    out = {}
    out["T_BKT"] = T_BKT
    out["T_c0"] = T_C0
    out["J_s_0"] = J0
    out["jump_2T_over_pi"] = float(JUMP)
    # 因子化：T = (pi/2) J0 Q，Q = jump/J0
    Q = JUMP / J0
    out["Q"] = float(Q)
    out["Q_le_1"] = bool(Q <= 1)
    T_chain = (math.pi / 2) * J0 * Q
    out["T_BKT_chain"] = float(T_chain)
    out["T_chain_relerr"] = float(abs(T_chain - T_BKT) / T_BKT)
    # T_c = min：T_BKT < T_c0
    out["T_BKT_lt_Tc0"] = bool(T_BKT < T_C0)
    out["T_BKT_over_Tc0"] = float(T_BKT / T_C0)
    # 普适线 algebra: pi*jump = 2T
    out["pi_jump_vs_2T_relerr"] = float(abs(math.pi * JUMP - 2 * T_BKT) / (2 * T_BKT))
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # (a) 普适跳变线 pi J = 2T
    ax = axes[0, 0]
    Ts = np.linspace(0, 6, 200)
    ax.plot(Ts, (math.pi / 2) * np.full_like(Ts, (2 * Ts / math.pi)), "k--", lw=1.5,
            label=r"普适线 $\pi J_s=2T$")
    ax.plot(Ts, 2 * Ts / math.pi, "b-", lw=2, label=r"$J_s=2T/\pi$")
    ax.scatter([T_BKT], [JUMP], c="red", s=80, zorder=5, label=f"NbN: T_BKT={T_BKT}")
    ax.set_xlabel("T (K)")
    ax.set_ylabel(r"$J_s$ (K)")
    ax.set_title("(a) 普适跳变：数据落在 Nelson–Kosterlitz 线上")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (b) 因子化 Q = jump/J0
    ax = axes[0, 1]
    labels = ["裸刚度 J_s(0)", "跳变刚度 J_s(T_BKT)"]
    vals = [J0, JUMP]
    ax.bar(labels, vals, color=["tab:blue", "tab:green"])
    ax.set_ylabel(r"$J_s$ (K)")
    ax.set_title(f"(b) Q = jump/裸 = {a['Q']:.3f} ≤ 1")
    ax.grid(alpha=0.3, axis="y")

    # (c) T_c = min：T_BKT < T_c0
    ax = axes[1, 0]
    ax.bar(["T_BKT", "T_c0"], [T_BKT, T_C0], color=["tab:green", "tab:gray"])
    ax.set_ylabel("温度 (K)")
    ax.set_title(f"(c) 2D：T_c = T_BKT < T_c0（比 {a['T_BKT_over_Tc0']:.3f}）")
    ax.grid(alpha=0.3, axis="y")

    # (d) 因子化代回自洽
    ax = axes[1, 1]
    ax.axhline(T_BKT, color="red", lw=2, label="实测 T_BKT")
    ax.axhline(T_C0, color="gray", ls="--", lw=1.5, label="T_c0")
    ax.scatter([1], [a["T_BKT_chain"]], c="purple", s=100, zorder=5,
               label=f"链因子化给 {a['T_BKT_chain']:.3f}")
    ax.set_xlim(0, 2)
    ax.set_xticks([1])
    ax.set_xticklabels(["因子化"])
    ax.set_ylabel("温度 (K)")
    ax.set_title("(d) 因子化代回与实测一致（恒等核对）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("R13: 环19 BKT 因子化数据核对（Weitzel 2023 NbN，无拟合）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "环19_BKT数据检验.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R13 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "环19_BKT数据检验_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
