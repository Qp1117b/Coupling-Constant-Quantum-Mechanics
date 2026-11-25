# -*- coding: utf-8 -*-
"""
R15: Tc(kappa_s) = B sqrt(kappa) exp(-A kappa) 的最大值——数值与图像检验。
A=B=1 归一化（外生归一不进形状检验）；无拟合。仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/环10_最大Tc与最佳键刚度.py"
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
A = 1.0
B = 1.0


def Tc(k):
    return B * np.sqrt(k) * np.exp(-A * k)


def assertions():
    out = {}
    kstar = 1 / (2 * A)
    Tmax = B / math.sqrt(2 * A * math.e)
    out["kappa_star"] = kstar
    out["Tc_max"] = float(Tmax)
    out["Tc_at_kstar"] = float(Tc(kstar))
    out["peak_relerr"] = float(abs(Tc(kstar) - Tmax) / Tmax)
    # 上界断言：全网格 Tc <= Tmax
    ks = np.logspace(-3, 2, 5000)
    out["max_over_grid"] = float(np.max(Tc(ks)))
    out["all_below_bound"] = bool(np.all(Tc(ks) <= Tmax * (1 + 1e-9)))
    # 两端衰减
    out["Tc_low_k"] = float(Tc(1e-3))
    out["Tc_high_k"] = float(Tc(1e2))
    out["nonmonotonic"] = bool(Tc(1e-3) < Tc(kstar) and Tc(1e2) < Tc(kstar))
    # 核心不等式 u exp(-u) <= exp(-1)
    us = np.logspace(-3, 3, 1000)
    out["u_exp_inequality_min_gap"] = float(np.min(np.exp(-1) - us * np.exp(-us)))
    out["u_exp_holds"] = bool(out["u_exp_inequality_min_gap"] >= -1e-12)
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # (a) Tc(kappa) 主曲线与峰值
    ax = axes[0, 0]
    ks = np.logspace(-3, 2, 500)
    ax.semilogx(ks, Tc(ks), "b-", lw=2, label=r"$T_c=B\sqrt{\kappa_s}e^{-A\kappa_s}$")
    ax.axvline(a["kappa_star"], color="r", ls="--", lw=1.5,
               label=f"最佳 $\\kappa_s^\\ast={a['kappa_star']:.3f}$")
    ax.axhline(a["Tc_max"], color="gray", ls=":", lw=1.5,
               label=f"峰值 $T_c^{{\\max}}={a['Tc_max']:.3f}$")
    ax.set_xlabel(r"键刚度 $\kappa_s$")
    ax.set_ylabel(r"$T_c$（归一化）")
    ax.set_title("(a) Tc 对键刚度非单调：存在极大值")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (b) 两因子竞争：sqrt(k) 升、exp(-Ak) 降
    ax = axes[0, 1]
    ax.semilogx(ks, np.sqrt(ks), "g-", lw=2, label=r"前因子 $\sqrt{\kappa_s}$（升）")
    ax.semilogx(ks, np.exp(-A * ks), "r-", lw=2, label=r"指数 $e^{-A\kappa_s}$（降）")
    ax.set_xlabel(r"键刚度 $\kappa_s$")
    ax.set_ylabel("因子大小（归一化）")
    ax.set_title("(b) 竞争机制：两端压制，中间有峰")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (c) u exp(-u) <= exp(-1)
    ax = axes[1, 0]
    us = np.linspace(0.01, 5, 500)
    ax.plot(us, us * np.exp(-us), "purple", lw=2, label=r"$ue^{-u}$")
    ax.axhline(np.exp(-1), color="k", ls="--", lw=1.5, label=r"上界 $e^{-1}$")
    ax.scatter([1.0], [np.exp(-1)], c="red", s=70, zorder=5, label="u=1 取等号")
    ax.set_xlabel(r"$u=2A\kappa_s$")
    ax.set_ylabel(r"$ue^{-u}$")
    ax.set_title("(c) 核心不等式（Lean 已证）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (d) 与 2025 Nat Commun 权衡定性对照（示意）
    ax = axes[1, 1]
    lams = np.linspace(0.2, 4, 200)
    w = 1 / lams  # omega ~ 1/lambda 的权衡示意（McMillan）
    tc = w * np.exp(-1 / lams)
    ax.plot(lams, tc / np.max(tc), "orange", lw=2, label="权衡示意（ω~1/λ）")
    ax.set_xlabel(r"耦合 $\lambda$（示意）")
    ax.set_ylabel(r"$T_c$（归一化）")
    ax.set_title("(d) 与 2025 权衡定性同形（非数值对照）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    fig.suptitle("R15: 链几何导出的最大 Tc 与最佳键刚度（条件结果，无拟合）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "环10_最大Tc与最佳键刚度.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R15 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "环10_最大Tc与最佳键刚度_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
