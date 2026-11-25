# -*- coding: utf-8 -*-
"""
R25: ε_F/ħω_D 链内表达的标度与量级核对（用典型材料参量）。
无拟合（是标度检查）。仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/审14_epsilonF比值.py"
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

# 常数（CODATA）
HBAR = 1.054571817e-34       # J s
ME = 9.1093837015e-31        # kg
EV = 1.602176634e-19         # J
KB = 1.380649e-23            # J/K


def ratio(n, kappa_over_M, a, zv):
    """ε_F/(ħ ω_D) = ħ/(2 m a sqrt(κ_s/M)) · (3π² z n)^{2/3}/(6π² n)^{1/3}"""
    kF2 = (3 * np.pi**2 * zv * n) ** (2.0 / 3)
    kD = (6 * np.pi**2 * n) ** (1.0 / 3)
    vs = a * np.sqrt(kappa_over_M)
    return HBAR * kF2 / (2 * ME * vs * kD)


def assertions():
    out = {}
    # 典型金属量级：n~1e29 m^-3, a~3e-10 m, vs~5000 m/s => sqrt(kappa/M)=vs/a
    n = 1e29
    a = 3e-10
    vs = 5000.0
    kom = (vs / a) ** 2
    for zv in [1, 2, 4]:
        r = ratio(n, kom, a, zv)
        out[f"ratio_zv{zv}"] = float(r)
        out[f"ln_ratio_zv{zv}"] = float(np.log(r))
    # 标度：ratio ∝ n^{1/3}
    ns = np.array([1e28, 1e29, 1e30])
    rs = np.array([ratio(x, kom, a, 2) for x in ns])
    out["log_slope_vs_n"] = float(np.polyfit(np.log(ns), np.log(rs), 1)[0])
    out["slope_target"] = 1.0 / 3
    out["ratio_physical_range"] = bool(3 < out["ratio_zv2"] < 300)
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    n = 1e29; a = 3e-10; vs = 5000.0; kom = (vs / a) ** 2

    ax = axes[0, 0]
    zvs = np.array([1, 2, 3, 4, 5])
    rs = [ratio(n, kom, a, z) for z in zvs]
    ax.plot(zvs, rs, "b-o", lw=2)
    ax.set_xlabel(r"价电子数 $z_v$"); ax.set_ylabel(r"$\varepsilon_F/\hbar\omega_D$")
    ax.set_title("(a) 比值随价电子数（链内表达）"); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ns = np.logspace(28, 30, 100)
    ax.plot(ns, [ratio(x, kom, a, 2) for x in ns], "g-", lw=2)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel(r"数密度 $n$ (m$^{-3}$)"); ax.set_ylabel(r"$\varepsilon_F/\hbar\omega_D$")
    ax.set_title(r"(b) 标度 ∝ n^{1/3}（斜率 1/3）"); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    mu = 0.5  # 裸 Coulomb 示意（外生）
    ratios = np.logspace(0.5, 3, 200)
    mustar = mu / (1 + mu * np.log(ratios))
    ax.plot(ratios, mustar, "purple", lw=2)
    ax.set_xscale("log")
    ax.set_xlabel(r"$\varepsilon_F/\hbar\omega_D$"); ax.set_ylabel(r"$\mu^\ast$")
    ax.set_title("(c) Morel-Anderson μ*（比值来源现由链给）"); ax.grid(alpha=0.3)

    ax = axes[1, 1]
    labels = ["链给比值\n(几何/声学)", "$z_v$,$m$\n(外生)", "裸 μ\n(审-14 外生)"]
    vals = [1, 1, 1]
    ax.bar(labels, vals, color=["tab:green", "tab:gray", "tab:red"])
    ax.set_yticks([])
    ax.set_title("(d) 审-14：比值来源闭合，μ 仍外生")
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("R25: ε_F/ħω_D 链内表达——审-14 比值子块（标度核对，无拟合）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "审14_epsilonF比值.png")
    fig.savefig(png, dpi=140); plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R25 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "审14_epsilonF比值_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
