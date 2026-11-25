# -*- coding: utf-8 -*-
"""
目标补充／`审-14` 的数值核对：Gamma 的谱来源与替代 T 入口的否定。

1. Gamma(x)=1+x^n 与 beta(x)=n x^{n-1}/(1+x^n)（n=1,2,3）；
2. 峰位 x*=(n-1)^{1/n} 与 Tc/E0=(n-1)^{-(n-1)/n}；
3. Debye 累积模数 N(w) ∝ w^d 的幂律核对；
4. 观测 Tc/theta_D 与 (A14.3) 预言 0.63 的对比。

外部数值只作对照；曲线由 (补.1)-(补.3) 直接计算。
"""

import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "目标_审14_Gamma.png")
OUT_CSV = os.path.join(HERE, "目标_审14_Gamma.csv")

MATERIALS = [("Al", 1.2, 428.0), ("Nb", 9.25, 275.0), ("Pb", 7.2, 105.0)]


def beta_shape(x, n):
    return n * x ** (n - 1) / (1 + x ** n)


def main():
    rows = []
    pred = 2.0 ** (-2.0 / 3.0)
    print(f"Tc/E0 at n=3 = {pred:.6f}")

    print("\n峰位与 Tc 因子")
    for n in range(2, 8):
        xs = (n - 1) ** (1.0 / n)
        tf = (n - 1) ** (-(n - 1) / n)
        print(f"  n={n}: x*={xs:.6f}, Tc/E0={tf:.6f}")
        rows.append(("peak", n, xs, tf, np.nan))

    print("\nDebye 累积幂律（int_0^1 d y^{d-1} dy = 1，斜率 d）")
    y = np.linspace(1e-6, 1.0, 200000)
    for d in (1, 2, 3):
        val = np.trapezoid(d * y ** (d - 1), y)
        print(f"  d={d}: integral={val:.8f} (target 1)")
        rows.append(("debye", d, val, 1.0, np.nan))

    print("\n观测 Tc/theta_D 与预言对比")
    ratios = []
    for name, tc, td in MATERIALS:
        r = tc / td
        ratios.append(r)
        print(f"  {name}: {r:.6f} vs {pred:.6f} (factor {pred/r:.1f})")
        rows.append(("observation", tc, r, pred, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A: beta
    xx = np.linspace(0.01, 4, 800)
    for n in (1, 2, 3):
        ax[0, 0].plot(xx, beta_shape(xx, n), lw=2.0, label=rf"$n={n}$")
    ax[0, 0].set_xlabel(r"$x=E/E_0$")
    ax[0, 0].set_ylabel(r"$\beta$（形状）")
    ax[0, 0].set_title(r"A  $\beta$ 单峰性：$n=1$ 无峰")
    ax[0, 0].legend(fontsize=9)
    ax[0, 0].grid(alpha=0.3)

    # B: peak and Tc factor
    ns = np.arange(2, 11)
    xs = [(n - 1) ** (1.0 / n) for n in ns]
    tfs = [(n - 1) ** (-(n - 1) / n) for n in ns]
    ax[0, 1].plot(ns, xs, "o-", lw=2.0, color="tab:blue", label=r"$x_*=(n-1)^{1/n}$")
    ax[0, 1].plot(ns, tfs, "s-", lw=2.0, color="tab:orange",
                  label=r"$T_c/E_0=(n-1)^{-(n-1)/n}$")
    ax[0, 1].set_xlabel(r"$n$")
    ax[0, 1].set_title("B  峰位与峰温因子")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    # C: Debye cumulative
    om = np.logspace(-2, 0, 300)
    for d in (1, 2, 3):
        ax[1, 0].loglog(om, om ** d, lw=2.0, label=rf"$d={d}$: $N\propto\omega^{d}$")
    ax[1, 0].set_xlabel(r"$\omega/\omega_D$")
    ax[1, 0].set_ylabel(r"累积模数（形状）")
    ax[1, 0].set_title("C  Debye 累积幂次 = 谱维数")
    ax[1, 0].legend(fontsize=9)
    ax[1, 0].grid(alpha=0.3, which="both")

    # D: comparison
    names = [m[0] for m in MATERIALS]
    ax[1, 1].bar(np.arange(3) - 0.18, ratios, 0.36, color="tab:green", alpha=0.85,
                 label="观测 $T_c/\\theta_D$")
    ax[1, 1].bar(np.arange(3) + 0.18, [pred] * 3, 0.36, color="tab:red", alpha=0.85,
                 label="(A14.3) 预言")
    ax[1, 1].set_yscale("log")
    ax[1, 1].set_xticks(np.arange(3))
    ax[1, 1].set_xticklabels(names)
    ax[1, 1].set_ylabel("比值（对数）")
    ax[1, 1].set_title("D  Debye 入口的 Tc 高估 1-2 个量级")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
