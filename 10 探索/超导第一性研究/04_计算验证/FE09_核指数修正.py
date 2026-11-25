# -*- coding: utf-8 -*-
"""
R10: FE09 隙方程核指数修正——p=3(旧,作废) -> p=5(修正), 附 p 稳健性扫描。
解 1 = Lambda sum 1/k^p * E/sqrt(E^2+D^2) tanh(...); 无拟合。
仅用 numpy + scipy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/FE09_核指数修正.py"
"""
import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from scipy.special import zeta

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
KMAX = 200000
k = np.arange(1, KMAX + 1, dtype=float)
E = k**2
R6 = ["Al", "Cd", "Ga", "Mo", "Ta", "Sn", "V", "Zn"]
R6_R = [3.344, 3.348, 3.546, 3.406, 3.692, 3.608, 3.439, 3.277]


def make_S(p):
    w = 1 / k**p
    def S(D, T):
        x = np.sqrt(E**2 + D**2)
        return float(np.sum(w * E / x * np.tanh(x / (2 * T)))) if T > 0 else float(np.sum(w * E / x))
    return S, float(np.sum(w))


def solve(S, zm, Lam):
    if 1 / Lam >= zm:
        return None, None
    D0 = brentq(lambda D: S(D, 0) - 1 / Lam, 1e-10, 1e7)
    Tc = brentq(lambda T: S(0, T) - 1 / Lam, 1e-10, 1e7)
    return D0, Tc


def assertions():
    out = {}
    S3, z3 = make_S(3)
    S5, z5 = make_S(5)
    out["zeta3"] = z3
    out["zeta5"] = z5
    out["zeta5_exact_pi4_90"] = float(zeta(5, 1))
    out["lambda_c_old_p3"] = 1 / z3
    out["lambda_c_new_p5"] = 1 / z5
    out["threshold_increases_with_p"] = bool(1 / z5 > 1 / z3)

    D0, Tc = solve(S5, z5, 1.05)
    out["ratio_p5_near_threshold"] = float(2 * D0 / Tc)
    D0h, Tch = solve(S5, z5, 5.0)
    out["ratio_p5_strong"] = float(2 * D0h / Tch)
    out["nonuniversal_preserved"] = bool(out["ratio_p5_strong"] - out["ratio_p5_near_threshold"] > 1.0)
    out["strong_limit_gt_bcs"] = bool(out["ratio_p5_strong"] > 2 * math.pi / math.exp(0.5772156649))

    # p 稳健性：上限 gap ratio 随 p 变化但都 > BCS
    ups = []
    for p in [3, 4, 5, 6]:
        Sp, zp = make_S(p)
        Dh, Th = solve(Sp, zp, 5.0)
        ups.append(2 * Dh / Th)
    out["gap_ratio_upper_p3_p6"] = ",".join(f"{v:.3f}" for v in ups)
    out["all_uppers_exceed_bcs"] = bool(all(v > 3.528 for v in ups))
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    bcs = 2 * math.pi / math.exp(0.5772156649)

    # (a) 核指数 p=3 vs p=5: gap ratio vs Lambda
    ax = axes[0, 0]
    Ls = np.linspace(0.97, 5.0, 100)
    for p, col in [(3, "gray"), (5, "purple")]:
        Sp, zp = make_S(p)
        rs = []
        for L in Ls:
            D, T = solve(Sp, zp, L)
            rs.append(2 * D / T if D else float("nan"))
        ax.plot(Ls, rs, color=col, lw=2, label=f"核 $1/k^{{{p}}}$" + ("（旧·作废）" if p == 3 else "（修正）"))
    ax.axhline(bcs, color="r", ls="--", lw=1.5, label="BCS 3.528")
    ax.set_xlabel(r"$\Lambda$")
    ax.set_ylabel(r"$2\Delta/k_BT_c$")
    ax.set_title("(a) 修正前后：定性保持，定量改变")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (b) 阈值随 p
    ax = axes[1 - 1, 1]
    ps = np.array([3, 4, 5, 6])
    lc = np.array([1 / float(np.sum(1 / k**p)) for p in ps])
    ax.plot(ps, lc, "o-", color="teal", lw=2)
    ax.set_xlabel(r"核指数 $p$")
    ax.set_ylabel(r"阈值 $\Lambda_c=1/\zeta(p)$")
    ax.set_title(r"(b) 阈值随 p 单调升；修正值 p=5")
    ax.grid(alpha=0.3)

    # (c) gap ratio 上限随 p
    ax = axes[1, 0]
    ups = []
    for p in ps:
        Sp, zp = make_S(int(p))
        D, T = solve(Sp, zp, 5.0)
        ups.append(2 * D / T)
    ax.plot(ps, ups, "o-", color="darkorange", lw=2)
    ax.axhline(bcs, color="r", ls="--", lw=1.5, label="BCS 3.528")
    ax.set_xlabel(r"核指数 $p$")
    ax.set_ylabel("gap ratio 上限")
    ax.set_title("(c) 非普适性对 p 稳健")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (d) 数据定位（修正核 p=5）
    ax = axes[1, 1]
    Sp, zp = make_S(5)
    grid = []
    for L in np.linspace(0.97, 5.0, 200):
        D, T = solve(Sp, zp, L)
        if D:
            grid.append((2 * D / T, L))
    grid = np.array(grid)
    lam_data = np.interp(R6_R, grid[:, 0], grid[:, 1])
    ax.scatter(R6_R, lam_data, c="tab:blue", s=50)
    ax.set_xlabel("R6 实测 gap ratio")
    ax.set_ylabel(r"修正定位 $\Lambda'$")
    ax.set_title(r"(d) 弱耦合数据定位 $\Lambda'\in[1.2,1.5]$（L4）")
    ax.grid(alpha=0.3)

    fig.suptitle("R10: FE09 核指数修正 p=3→5（阈值超导候选，框架扩展）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "FE09_核指数修正.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R10 数值断言 ===")
    for k_, v in a.items():
        print(f"{k_:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "FE09_核指数修正_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["assertion", "value"])
        for k_, v in a.items():
            w.writerow([k_, v])
    print(f"\n图像: {p}\n断言表: {path}")
