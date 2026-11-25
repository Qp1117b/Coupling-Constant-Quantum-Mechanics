# -*- coding: utf-8 -*-
"""
FE09: 链核 1/k^3 的阈值超导候选——数值与图像检验。
解 gap equation S(Delta,T)=1/Lambda；无拟合（Lambda 为扫描参数，非拟合数据）。
仅用 numpy + scipy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/FE09_阈值超导.py"
"""
import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
KMAX = 200000
k = np.arange(1, KMAX + 1, dtype=float)
W = 1 / k**3
E = k**2  # E2 = 1 归一化
ZETA3 = float(np.sum(W))
LAMBDA_C = 1 / ZETA3

# R6 弱耦合实测 gap ratio（用于事后定位对照，L4，非独立预测）
R6_ELEMENTS = ["Al", "Cd", "Ga", "Mo", "Ta", "Sn", "V", "Zn"]
R6_RATIOS = [3.344, 3.348, 3.546, 3.406, 3.692, 3.608, 3.439, 3.277]


def S(D, T):
    x = np.sqrt(E**2 + D**2)
    if T <= 0:
        return float(np.sum(W * E / x))
    return float(np.sum(W * E / x * np.tanh(x / (2 * T))))


def solve_gap(Lam):
    target = 1 / Lam
    if target >= ZETA3:
        return None, None
    D0 = brentq(lambda D: S(D, 0) - target, 1e-10, 1e7)
    Tc = brentq(lambda T: S(0, T) - target, 1e-10, 1e7)
    return D0, Tc


def assertions():
    out = {}
    out["zeta3"] = ZETA3
    out["lambda_c"] = float(LAMBDA_C)
    out["lambda_c_lower_bound_0.5"] = bool(LAMBDA_C >= 0.5)
    # 近阈 gap ratio 远小于 BCS 3.528
    Lams = [0.84, 0.90, 1.00, 1.20, 1.50, 3.00]
    rows = []
    for L in Lams:
        D0, Tc = solve_gap(L)
        rows.append((L, D0, Tc, 2 * D0 / Tc))
    out["ratio_near_threshold"] = float(rows[0][3])
    out["ratio_strong_chain"] = float(rows[-1][3])
    out["ratio_nonuniversal"] = bool(rows[-1][3] - rows[0][3] > 1.0)
    out["ratio_limit_below_data_max"] = bool(rows[-1][3] < 4.4)  # Pb 4.40 超模型上限
    out["weak_data_mean_ratio"] = float(np.mean(R6_RATIOS))
    # 事后定位的 Lambda 区间
    loc = []
    for L in np.linspace(0.84, 3.0, 200):
        D0, Tc = solve_gap(L)
        if D0 is not None:
            loc.append((2 * D0 / Tc, L))
    grid = np.array(loc)
    lam_for_data = np.interp(R6_RATIOS, grid[:, 0], grid[:, 1])
    out["lambda_for_weak_data_min"] = float(np.min(lam_for_data))
    out["lambda_for_weak_data_max"] = float(np.max(lam_for_data))
    return out, rows


def plots(a, rows):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # (a) S(Delta,0)
    ax = axes[0, 0]
    Ds = np.logspace(-3, 4, 100)
    ax.plot(Ds, [S(D, 0) for D in Ds], "b-", lw=2)
    ax.axhline(ZETA3, color="k", ls="--", lw=1.5, label=r"$S(0,0)=\zeta(3)$")
    ax.set_xscale("log")
    ax.set_xlabel(r"$\Delta/E_2$")
    ax.set_ylabel(r"$S(\Delta,0)$")
    ax.set_title(r"(a) 右端最大值 zeta(3) ⇒ 阈值")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (b) S(0,T)
    ax = axes[0, 1]
    Ts = np.logspace(-3, 3, 100)
    ax.plot(Ts, [S(0, T) for T in Ts], "g-", lw=2)
    ax.axhline(ZETA3, color="k", ls="--", lw=1.5)
    ax.set_xscale("log")
    ax.set_xlabel(r"$k_BT/E_2$")
    ax.set_ylabel(r"$S(0,T)$")
    ax.set_title("(b) 温度扫描给 Tc")
    ax.grid(alpha=0.3)

    # (c) gap ratio vs Lambda
    ax = axes[1, 0]
    Ls = np.linspace(0.833, 3.0, 120)
    ratios = []
    for L in Ls:
        D0, Tc = solve_gap(L)
        ratios.append(2 * D0 / Tc if D0 is not None else float("nan"))
    ax.plot(Ls, ratios, "purple", lw=2, label=r"链核 $1/k^3$：非普适")
    ax.axhline(2 * math.pi / math.exp(0.5772156649), color="r", ls="--", lw=1.5,
               label=r"BCS $2\pi/e^\gamma=3.528$（普适）")
    ax.set_xlabel(r"$\Lambda$")
    ax.set_ylabel(r"$2\Delta(0)/k_BT_c$")
    ax.set_title("(c) 非普适 gap ratio：1.57 → 3.85")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (d) 与 R6 数据对照（事后定位，L4）
    ax = axes[1, 1]
    ax.bar(R6_ELEMENTS, R6_RATIOS, color="tab:blue", label="R6 弱耦合实测")
    ax.axhline(2 * math.pi / math.exp(0.5772156649), color="r", ls="--", lw=1.5, label="BCS 3.528")
    ax.axhline(3.85, color="gray", ls=":", lw=1.5, label="链核模型上限 3.85")
    ax.set_ylabel(r"$2\Delta/k_BT_c$")
    ax.set_title("(d) 数据落在模型区间（事后定位 L4）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("FE09: 链核 1/k^3 的阈值超导候选（框架扩展，非链内已证）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "FE09_阈值超导.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)
    return png


if __name__ == "__main__":
    a, rows = assertions()
    print("=== FE09 数值断言与 gap ratio 表 ===")
    for k_, v in a.items():
        print(f"{k_:32s} = {v}")
    print("\nLambda   Delta0    Tc      2D/Tc")
    for L, D0, Tc, r in rows:
        print(f"{L:6.2f}  {D0:8.4f}  {Tc:7.4f}  {r:7.3f}")
    p = plots(a, rows)
    path = os.path.join(HERE, "FE09_阈值超导_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["assertion", "value"])
        for k_, v in a.items():
            w.writerow([k_, v])
    print(f"\n图像: {p}\n断言表: {path}")
