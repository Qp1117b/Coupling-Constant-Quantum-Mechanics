# -*- coding: utf-8 -*-
"""
环 9／`审-2` 的数值核对：kappa_f 的几何来源。

1. kappa_f(e) = 1/(4 pi (1 - e/2pi)) 的曲线与零点值；
2. 矩阵分支线性系数 c(e) = v_tau^2 = 1 - e/2pi；
3. 线性化误差 |精确 Delta lambda - 线性| / |精确| 随 Delta 缩小；
4. c = 4 pi (1-e/2pi) kappa_f 的关系族与锚点。

全部由 (K2.2)(K2.4)(K2.6) 直接计算，无拟合。
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
OUT_PNG = os.path.join(HERE, "环09_审2_kappa_f.png")
OUT_CSV = os.path.join(HERE, "环09_审2_kappa_f.csv")

TWO_PI = 2.0 * np.pi


def phi(e):
    return 0.5 * np.log(1.0 - e / TWO_PI)


def kappa(e):
    return 1.0 / (4.0 * np.pi * (1.0 - e / TWO_PI))


def cscale(e):
    return 1.0 - e / TWO_PI


def main():
    rows = []
    print("kappa_f(0) =", kappa(0.0), " (target 1/(4pi) =", 1 / (4 * np.pi), ")")
    print("c(0) =", cscale(0.0), " (target 1)")
    print("kappa_f(2pi - 0.1) =", kappa(TWO_PI - 0.1))
    rows.append(("kappa_zero", 0.0, float(kappa(0.0)), 1 / (4 * np.pi), np.nan))
    rows.append(("c_zero", 0.0, float(cscale(0.0)), 1.0, np.nan))

    # 线性化误差
    print("\n线性化误差（e0=0）")
    for d in (1e-1, 1e-2, 1e-3, 1e-4):
        exact = phi(d) - phi(0.0)
        linear = 0.5 * (-1.0 / (2 * np.pi)) * d
        rel = abs(exact - linear) / abs(exact)
        print(f"  Delta={d:.1e}  rel_err={rel:.6e}")
        rows.append(("lin_err", d, float(rel), np.nan, np.nan))

    # c 关系核对
    for e in (0.0, 1.0, 3.0, 5.0):
        k = kappa(e)
        c = 4 * np.pi * (1 - e / TWO_PI) * k
        print(f"e={e:.1f}: c=4pi(1-e/2pi)kappa = {c:.12f}, v2 = {cscale(e):.12f}")
        rows.append(("c_relation", e, c, cscale(e), np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A: kappa
    ee = np.linspace(-6.0, 6.0, 1500)
    ax[0, 0].plot(ee, kappa(ee), lw=2.2, color="tab:blue",
                  label=r"$\kappa_f=1/[4\pi(1-\varepsilon/2\pi)]$")
    ax[0, 0].axvline(TWO_PI, color="tab:red", ls="--", lw=1.2,
                     label=r"$\varepsilon=2\pi$")
    ax[0, 0].plot([0], [kappa(0)], "o", color="tab:green", ms=7)
    ax[0, 0].annotate(r"$\kappa_f(0)=1/(4\pi)$", xy=(0, kappa(0)),
                      xytext=(1.0, 0.5), fontsize=9,
                      arrowprops=dict(arrowstyle="->", lw=0.8))
    ax[0, 0].set_xlabel(r"$\varepsilon_0$")
    ax[0, 0].set_ylabel(r"$\kappa_f$")
    ax[0, 0].set_title(r"A  FG 接口的亏角—钟速对数响应")
    ax[0, 0].set_ylim(0, 1.2)
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    # B: c = 1 with geometric kappa; contrast with frozen kappa
    ax[0, 1].plot(ee, np.ones_like(ee), lw=2.4, color="tab:green",
                  label=r"几何 $\kappa_f(\varepsilon)$：$c\equiv1$")
    ax[0, 1].plot(ee, cscale(ee), lw=1.8, ls="--", color="tab:orange",
                  label=r"若 $\kappa_f$ 固定在锚点：$c=v_\tau^2$")
    ax[0, 1].axhline(0.0, color="0.35", lw=0.9)
    ax[0, 1].plot([0], [1], "o", color="tab:red", ms=7)
    ax[0, 1].annotate(r"锚点 $\kappa_f=1/(4\pi)$", xy=(0, 1), xytext=(1.2, 1.35),
                      fontsize=9, arrowprops=dict(arrowstyle="->", lw=0.8))
    ax[0, 1].set_xlabel(r"$\varepsilon_0$")
    ax[0, 1].set_ylabel(r"$c$")
    ax[0, 1].set_title(r"B  矩阵分支线性系数：$c\equiv1$")
    ax[0, 1].set_ylim(-0.5, 1.8)
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    # C: 线性化误差
    ds = np.logspace(-4, 0, 200)
    exact = phi(ds) - phi(0.0)
    linear = 0.5 * (-1.0 / (2 * np.pi)) * ds
    rel = np.abs(exact - linear) / np.abs(exact)
    ax[1, 0].loglog(ds, rel, lw=2.2, color="tab:purple")
    ax[1, 0].set_xlabel(r"$\Delta$")
    ax[1, 0].set_ylabel("相对误差")
    ax[1, 0].set_title(r"C  (K2.3) 线性化误差随 $\Delta$ 缩小")
    ax[1, 0].grid(alpha=0.3, which="both")

    # D: c-kappa 关系族
    ks = np.linspace(0.02, 0.16, 300)
    for e0 in (0.0, 1.0, 3.0, 5.0):
        ax[1, 1].plot(ks, 4 * np.pi * (1 - e0 / TWO_PI) * ks,
                      lw=1.8, label=rf"$\varepsilon_0={e0:.0f}$")
    ax[1, 1].plot([1 / (4 * np.pi)], [1], "o", color="tab:red", ms=8,
                  label="锚点")
    for e0 in (0.0, 1.0, 3.0, 5.0):
        ax[1, 1].plot([kappa(e0)], [1], "o", color="tab:blue", ms=6)
    ax[1, 1].set_xlabel(r"$\kappa_f$")
    ax[1, 1].set_ylabel(r"$c=4\pi v_\tau^2\kappa_f$")
    ax[1, 1].set_title(r"D  (K2.6) 关系族与锚点")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
