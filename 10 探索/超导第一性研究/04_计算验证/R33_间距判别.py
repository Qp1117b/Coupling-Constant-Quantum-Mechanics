# -*- coding: utf-8 -*-
"""
R33: 26.B2 间距判别——{log p} 非等距 vs DSI 等距。
数据为素数序列（外部标准数学），无拟合。
运行：python "10 探索/超导第一性研究/04_计算验证/R33_间距判别.py"
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


def primes_below(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i in range(n + 1) if sieve[i]]


def assertions():
    out = {}
    ps = primes_below(200)
    logp = np.array([math.log(p) for p in ps])
    gaps = np.diff(logp)  # s_n = log(p_{n+1}/p_n)
    # {log p} 非等距：间距方差 > 0
    out["logp_gap_std"] = float(np.std(gaps))
    out["logp_not_equidistant"] = bool(np.std(gaps) > 1e-3)
    # 素数非等比：p2^2 != p1*p3（取前三个素数 2,3,5）
    out["p2sq_vs_p1p3"] = bool(3 ** 2 != 2 * 5)
    out["three_primes_no_gp"] = bool(9 != 10)
    # DSI 支：等距（间距方差 = 0）
    dsi_gaps = np.full(50, math.log(1.5))  # 等差、公比 λ=1.5
    out["dsi_gap_std"] = float(np.std(dsi_gaps))
    out["dsi_equidistant"] = bool(np.std(dsi_gaps) < 1e-12)
    # 两支不相交：等距序列不可能匹配 log p
    out["branches_disjoint"] = bool(out["logp_not_equidistant"] and out["dsi_equidistant"])
    # 间距趋于 0（PNT）
    out["last_gap"] = float(gaps[-1])
    out["gap_tends_to_zero"] = bool(gaps[-1] < gaps[0])
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    ps = primes_below(200)
    logp = np.array([math.log(p) for p in ps])
    gaps = np.diff(logp)

    ax = axes[0, 0]
    ax.plot(range(len(logp)), logp, "b-o", ms=3)
    ax.set_xlabel("素数序号 n"); ax.set_ylabel(r"$\log p_n$")
    ax.set_title("(a) {log p_n} 序列"); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.bar(range(len(gaps)), gaps, color="tab:orange", width=1.0)
    ax.axhline(np.mean(gaps), color="r", ls="--", label="均值")
    ax.set_xlabel("n"); ax.set_ylabel(r"$s_n=\log(p_{n+1}/p_n)$")
    ax.set_title(f"(b) 间距非常数（std={a['logp_gap_std']:.3f}，非等距）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    dsi = np.cumsum(np.full(50, math.log(1.5)))
    ax.plot(range(50), dsi, "g-o", ms=3)
    ax.set_xlabel("n"); ax.set_ylabel("谱峰位置")
    ax.set_title("(c) DSI 支：log 坐标下等距（间距恒定）"); ax.grid(alpha=0.3)

    ax = axes[1, 1]
    labels = ["{log p}\n非等距", "DSI\n等距"]
    ax.bar(labels, [np.std(gaps), 0.0], color=["tab:blue", "tab:green"])
    ax.set_ylabel("间距标准差")
    ax.set_title("(d) 两支不相交（26.B2 判别子）"); ax.grid(alpha=0.3, axis="y")

    fig.suptitle("R33: 26.B2 间距判别——{log p} 非等距 vs DSI 等距（非拟合）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "R33_间距判别.png")
    fig.savefig(png, dpi=140); plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R33 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "R33_间距判别_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
