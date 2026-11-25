# -*- coding: utf-8 -*-
"""
R40: R8 前提推广审计——几何权重模和的对数 vs BCS 对数（不同源）。
数据为解析函数核对，无拟合。
运行：python "10 探索/超导第一性研究/04_计算验证/R40_R8前提审计.py"
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


def log_gen(q, N=200000):
    """sum_{k=1}^N q^k / k，数值核对 = -ln(1-q)。"""
    k = np.arange(1, N + 1)
    return float(np.sum(q ** k / k))


def assertions():
    out = {}
    # 对数生成函数核对
    for q in [0.3, 0.5, 0.9]:
        s = log_gen(q)
        exact = -math.log(1 - q)
        out[f"log_gen_q{q}"] = bool(abs(s - exact) < 1e-4)
    # BCS 对数 ln(wD/EF)；典型 wD/EF ~ 1e-2 -> ln100
    bcs_log = math.log(100)
    out["bcs_log_ln100"] = round(bcs_log, 4)
    # 匹配所需 q：1/(1-q)=100 -> q=0.99
    q_match = 1 - 1 / 100
    out["q_to_match_bcs"] = round(q_match, 4)
    out["first_share_at_match"] = round(1 - q_match, 4)
    out["not_first_dominant"] = bool(1 - q_match < 0.5)
    # 物理区 q<=0.5: 对数 <= ln2 ~ 0.69，远小于 BCS 对数
    phys_log = -math.log(1 - 0.5)
    out["phys_region_log_q0.5"] = round(phys_log, 4)
    out["phys_log_much_smaller"] = bool(phys_log < bcs_log / 3)
    # 区分不同源：两者数值相等需脱离物理区
    out["different_origin"] = bool(out["not_first_dominant"] and out["phys_log_much_smaller"])
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ax = axes[0, 0]
    qs = np.linspace(0.05, 0.95, 100)
    ax.plot(qs, [-math.log(1 - q) for q in qs], "b-", lw=2, label=r"$-\ln(1-q)=\sum q^k/k$")
    for q in [0.3, 0.5, 0.9]:
        ax.plot(q, -math.log(1 - q), "ro")
    ax.set_xlabel("q"); ax.set_ylabel("几何权重模和的对数")
    ax.set_title(r"(a) 对数生成函数核对（数值=解析）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.axhline(a["bcs_log_ln100"], color="r", ls="--", lw=2, label=r"BCS $\ln(\omega_D/E_F)=\ln100$")
    ax.plot(qs, [-math.log(1 - q) for q in qs], "b-", lw=2, label=r"几何权重 $-\ln(1-q)$")
    ax.axvline(0.5, color="g", ls=":", label="物理区 q≤0.5")
    ax.axvline(a["q_to_match_bcs"], color="orange", ls=":", label="匹配 BCS 需 q≈0.99")
    ax.set_xlabel("q"); ax.set_ylabel("对数值")
    ax.set_title("(b) 数值相等需 q≈0.99（脱离第一档主导）")
    ax.legend(fontsize=7); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    ax.plot(qs, [1 - q for q in qs], "purple", lw=2)
    ax.axhline(0.5, color="k", ls="--", label="第一档主导线 0.5")
    ax.plot(a["q_to_match_bcs"], 1 - a["q_to_match_bcs"], "ro", ms=10, label="匹配 BCS 点 (0.01)")
    ax.set_xlabel("q"); ax.set_ylabel("第一档占比 1-q")
    ax.set_title("(c) 匹配 BCS 对数处第一档占比→0（与 R35 矛盾）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 1]
    labels = [r"几何对数\n(衰减参数 t)", r"BCS 对数\n(能标比 ω_D/E_F)"]
    ax.bar(labels, [a["phys_region_log_q0.5"], a["bcs_log_ln100"]], color=["tab:blue", "tab:red"])
    ax.set_ylabel("对数值（物理区 q=0.5）")
    ax.set_title("(d) 不同源：数值与物理含义均不同")
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("R40: R8 前提推广审计——几何权重对数≠BCS 对数（R8 被强化，非绕过）", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "R40_R8前提审计.png")
    fig.savefig(png, dpi=140); plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R40 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "R40_R8前提审计_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
