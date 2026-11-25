# -*- coding: utf-8 -*-
"""
R32: 13.A2 分档结构——空洞性、有限窗口、覆盖半径 ln2 上界。
数据为链内解析阶梯（2 ln(2k)），无拟合。
运行：python "10 探索/超导第一性研究/04_计算验证/R32_阶梯分档结构.py"
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
LN2 = math.log(2)


def ladder(K):
    """截断阶梯 Λ_K = {2 ln(2k)}_{k<=K}。"""
    return np.array([2 * math.log(2 * k) for k in range(1, K + 1)])


def nearest(r, Lam):
    return float(np.min(np.abs(Lam - r)))


def assertions():
    out = {}
    # (R32.1) 相邻间距 Δ_k = 2 ln(1+1/k)
    ks = np.arange(1, 1001)
    gaps = np.array([2 * math.log(1 + 1 / k) for k in ks])
    # 单调递减
    out["gaps_monotone_dec"] = bool(np.all(np.diff(gaps) < 0))
    out["gap1_equals_2ln2"] = bool(abs(gaps[0] - 2 * LN2) < 1e-12)
    out["max_gap_is_2ln2"] = bool(abs(gaps.max() - 2 * LN2) < 1e-12)
    # Δ_k → 0（空洞性）
    out["gap_1000"] = float(gaps[-1])
    out["gap_tends_to_zero"] = bool(gaps[-1] < 0.003)
    # 覆盖半径上界：落在窗口内的 r_i，eta_min <= ln2
    for K in [5, 20, 100]:
        Lam = ladder(K)
        rs = np.linspace(Lam[0], Lam[-1], 500)
        eta_min = max(nearest(r, Lam) for r in rs)
        out[f"eta_min_K{K}"] = float(eta_min)
        out[f"eta_min_le_ln2_K{K}"] = bool(eta_min <= LN2 + 1e-9)
    # 有限窗口：窗口外的 r 最近邻距离可任意大（有限截断无法覆盖）
    Lam = ladder(10)
    out["r_outside_window_unbounded"] = bool(nearest(100.0, Lam) > 10)
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ax = axes[0, 0]
    ks = np.arange(1, 21)
    Lam = ladder(20)
    ax.stem(ks, Lam, basefmt=" ", linefmt="C0-", markerfmt="C0o")
    ax.set_xlabel("档序 k"); ax.set_ylabel(r"刻度 $2\ln(2k)$")
    ax.set_title("(a) 截断阶梯 Λ_K（K=20）"); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ks = np.logspace(0, 4, 200)
    gaps = [2 * math.log(1 + 1 / k) for k in ks]
    ax.loglog(ks, gaps, "b-", lw=2, label=r"$\Delta_k=2\ln(1+1/k)$")
    ax.axhline(2 * LN2, color="r", ls="--", label=r"$\Delta_1=2\ln2$")
    ax.set_xlabel("档序 k"); ax.set_ylabel(r"相邻间距 $\Delta_k$")
    ax.set_title("(b) 间距单调递减→0（无截断判据空洞）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    Ks = [5, 10, 20, 50, 100]
    etas = []
    for K in Ks:
        Lam = ladder(K)
        rs = np.linspace(Lam[0], Lam[-1], 500)
        etas.append(max(nearest(r, Lam) for r in rs))
    ax.plot(Ks, etas, "g-o", lw=2, label=r"$\eta_{\min}$（实测）")
    ax.axhline(LN2, color="r", ls="--", label=r"上界 $\ln2$")
    ax.set_xscale("log")
    ax.set_xlabel("截断档数 K"); ax.set_ylabel("最小分档半宽")
    ax.set_title("(c) 覆盖半径 ≤ ln2（与 K 无关）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 1]
    Lam = ladder(10)
    rs = np.linspace(0, 12, 600)
    dists = np.array([nearest(r, Lam) for r in rs])
    ax.plot(rs, dists, "purple", lw=2)
    ax.axhline(LN2, color="r", ls="--", label=r"$\ln2$")
    ax.set_xlabel(r"比值 $r=\delta v_\tau/\bar v_\tau$"); ax.set_ylabel(r"最近邻距离")
    ax.set_title("(d) 窗口外最近邻距离无界（有限 K 需窗口约束）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    fig.suptitle("R32: (13.A2) 分档结构——空洞性 / 有限窗口 / 覆盖半径（非拟合）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "R32_阶梯分档结构.png")
    fig.savefig(png, dpi=140); plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R32 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "R32_阶梯分档结构_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
