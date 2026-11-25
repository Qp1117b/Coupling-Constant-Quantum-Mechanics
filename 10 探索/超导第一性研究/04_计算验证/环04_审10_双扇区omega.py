# -*- coding: utf-8 -*-
"""
环 4／`审-10` 收口的数值核对：omega_log 按扇区分裂。

1. prefactor e^{-1/d} 随 d，标出 d=2 (相位) 与 d=3 (振幅)；
2. 两维度 Debye w_d(T)，低温 T^2 / T^3；
3. 数值积分 int_0^1 d y^{d-1} ln y = -1/d；
4. 两扇区 T* 与 T_BKT 的示意与 min。

全部由 (L10.1)(L10.2) 直接计算，无拟合。
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
OUT_PNG = os.path.join(HERE, "环04_审10_双扇区omega.png")
OUT_CSV = os.path.join(HERE, "环04_审10_双扇区omega.csv")


def w_debye(x, d):
    """w_d(T) = d int_0^1 y^{d-1} tanh(y/2x) dy, x = T/omega_D."""
    y = np.linspace(0.0, 1.0, 4001)
    f = d * y ** (d - 1) * np.tanh(y / (2 * x))
    return np.trapezoid(f, y)


def main():
    rows = []
    p2, p3 = np.exp(-1 / 2), np.exp(-1 / 3)
    print(f"prefactor d=2: {p2:.6f}, d=3: {p3:.6f}, ratio: {p3/p2:.6f} (target e^(1/6)={np.exp(1/6):.6f})")
    for d in (1, 2, 3, 4, 5):
        rows.append(("prefactor", d, float(np.exp(-1 / d)), -1 / d, np.nan))

    # 积分核对
    print("\n数值积分 int_0^1 d y^{d-1} ln y")
    y = np.linspace(1e-9, 1.0, 200001)
    for d in (1, 2, 3, 4, 5):
        val = np.trapezoid(d * y ** (d - 1) * np.log(y), y)
        print(f"  d={d}: {val:.10f}  target {-1/d:.10f}")
        rows.append(("moment_integral", d, float(val), -1 / d, np.nan))

    # w(T)
    print("\nw_d(T) 低温核对")
    for x in (0.02, 0.05, 0.1):
        w2, w3 = w_debye(x, 2), w_debye(x, 3)
        print(f"  x={x:.2f}: 1-w2={1-w2:.6e} (∝x^2={x*x:.4e}), 1-w3={1-w3:.6e} (∝x^3={x**3:.4e})")
        rows.append(("w2", x, 1 - w2, x * x, np.nan))
        rows.append(("w3", x, 1 - w3, x ** 3, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A
    ds = np.linspace(1, 5, 400)
    ax[0, 0].plot(ds, np.exp(-1 / ds), lw=2.2, color="tab:blue",
                  label=r"$e^{-1/d}$")
    ax[0, 0].plot([2], [p2], "o", color="tab:green", ms=8,
                  label=r"相位支 $d=2$")
    ax[0, 0].plot([3], [p3], "o", color="tab:orange", ms=8,
                  label=r"振幅支 $d=3$")
    ax[0, 0].set_xlabel(r"$d$")
    ax[0, 0].set_ylabel(r"$\omega_{\log}/\omega_D$")
    ax[0, 0].set_title("A  两扇区的对数矩前因子")
    ax[0, 0].legend(fontsize=9)
    ax[0, 0].grid(alpha=0.3)

    # B
    xs = np.linspace(0.01, 1.0, 300)
    ax[0, 1].plot(xs, [w_debye(x, 2) for x in xs], lw=2.2,
                  color="tab:green", label=r"相位支 $w_2$（低温 $T^2$）")
    ax[0, 1].plot(xs, [w_debye(x, 3) for x in xs], lw=2.2,
                  color="tab:orange", label=r"振幅支 $w_3$（低温 $T^3$）")
    ax[0, 1].set_xlabel(r"$x=T/\omega_D$")
    ax[0, 1].set_ylabel(r"$w_d$")
    ax[0, 1].set_title(r"B  两维度 $w_d(T)$ 各属其扇区")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    # C
    dd = np.array([1, 2, 3, 4, 5])
    vals = [-1 / d for d in dd]
    ax[1, 0].plot(dd, vals, "o-", lw=2.0, color="tab:purple")
    ax[1, 0].set_xlabel(r"$d$")
    ax[1, 0].set_ylabel(r"$\int_0^1 d y^{d-1}\ln y$")
    ax[1, 0].set_title(r"C  对数矩：解析值 $-1/d$")
    ax[1, 0].grid(alpha=0.3)

    # D: 两扇区温度（示意）
    lam = np.linspace(0.2, 1.2, 300)
    Tstar = 1.13 * p3 * np.exp(-1 / lam)
    TBKT = 0.35 * np.ones_like(lam) * p2
    ax[1, 1].plot(lam, Tstar, lw=2.2, color="tab:orange",
                  label=r"$T^*$（3D 矩 $e^{-1/3}$）")
    ax[1, 1].plot(lam, TBKT, lw=2.2, color="tab:green",
                  label=r"$T_{\rm BKT}$（2D 矩 $e^{-1/2}$ 进 $w$）")
    ax[1, 1].plot(lam, np.minimum(Tstar, TBKT), lw=2.0, ls="--",
                  color="tab:red", label=r"$T_c=\min$")
    ax[1, 1].set_xlabel(r"$\lambda$（示意）")
    ax[1, 1].set_ylabel("归一化温度")
    ax[1, 1].set_title(r"D  两扇区各用自己的 $\omega_{\log}$")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
