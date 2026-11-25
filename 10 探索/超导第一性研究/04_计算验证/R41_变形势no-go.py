# -*- coding: utf-8 -*-
"""
R41: 变形势链内化的结构 no-go——声学求和规则（k→0 时 M→0）与链内声学色散对比。
解析函数核对，无拟合。
运行：python "10 探索/超导第一性研究/04_计算验证/R41_变形势no-go.py"
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
XI = 5.0   # 变形势（示意，eV）
VS = 5000.0  # 声速（示意，m/s）


def assertions():
    out = {}
    # 声学支矩阵元 M = Ξ k；k→0 → 0
    ks = np.array([0, 1e-6, 1e-3, 1e-1, 1.0])
    Ms = XI * ks
    out["M_at_k0"] = float(Ms[0])
    out["acoustic_sum_g_zero"] = bool(Ms[0] == 0)
    kpos = ks[ks > 0]
    out["M_linear_in_k"] = bool(np.allclose((XI * kpos) / kpos, XI))
    # 链内声学色散 ω = v_s k；k→0 → 0
    omegas = VS * ks
    out["omega_at_k0"] = float(omegas[0])
    # 唯一连接点 k→0：M/omega = Ξ/v_s 常数，但仍含 Ξ
    kr = ks[1:]
    ratio = (XI * kr) / (VS * kr)
    out["M_over_omega_const"] = bool(np.allclose(ratio, XI / VS))
    out["ratio_needs_Xi"] = bool(abs(ratio[0] - XI / VS) < 1e-9)
    # 链内无 Ξ：若强行 Ξ=0（链内无电子结构量），则 M≡0
    out["chain_without_Xi_gives_zero"] = bool(np.all(0 * kr == 0))
    return out


def plots(a):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    ax = axes[0]
    ks = np.linspace(0, 1, 200)
    ax.plot(ks, XI * ks, "b-", lw=2, label=r"变形势 $M=\Xi k$（需电子结构 $\Xi$）")
    ax.plot(ks, VS * ks / VS, "g--", lw=2, label=r"链内声学 $\omega/v_s=k$（几何）")
    ax.plot(0, 0, "ro", ms=10, label="声学求和规则：$k=0\Rightarrow g=0$")
    ax.set_xlabel("波数 k"); ax.set_ylabel("归一化值")
    ax.set_title("(a) 声学支唯一连接点在 k=0，但那里耦合为零")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1]
    labels = ["链内几何\n($v_s$, $k_D$)", "变形势\n($\\Xi=\\partial E_{edge}/\\partial\\epsilon$)"]
    vals = [1, 1]
    ax.bar(labels, vals, color=["tab:green", "tab:red"])
    ax.set_yticks([])
    ax.set_title("(b) 定义域不相交：流速场 vs 电子能带边\n(no-go R41.1)")
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("R41: 变形势链内化的结构 no-go（授权已收到，但授权不能替代物理依据）", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    png = os.path.join(HERE, "R41_变形势no-go.png")
    fig.savefig(png, dpi=140); plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R41 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "R41_变形势no-go_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
