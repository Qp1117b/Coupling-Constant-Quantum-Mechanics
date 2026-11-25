# -*- coding: utf-8 -*-
"""
环 22／审-12 并存窗口的数值核对。

1. p_c(L) = p_c - C L^{-3/4} 随 L 下移收敛；
2. 局域阈值 p_c^loc = p_c - C n_eff^{-3/8} 随参与比上移；
3. 窗口宽度 ∝ n_eff^{-3/8} 的双对数斜率（应 = -3/8）；
4. 容量下限 n_eff > (C/p_c)^{8/3} 与窗口塌缩。

取 C=0.05，点渗流 p_c=0.592746 与键渗流 p_c=1/2 两口径对照。
由 (12.1)-(12.3) 直接计算，无拟合。
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
OUT_PNG = os.path.join(HERE, "环22_审12_并存窗口.png")
OUT_CSV = os.path.join(HERE, "环22_审12_并存窗口.csv")

C_COEF = 0.05
PC_SITE = 0.592746
PC_BOND = 0.5


def p_finite(L, pc):
    return pc - C_COEF * L ** (-0.75)


def p_loc(neff, pc):
    return pc - C_COEF * neff ** (-3.0 / 8.0)


def main():
    rows = []

    # A 有限尺寸下移
    print("A 有限尺寸阈值下移")
    Ls = np.linspace(4, 400, 300)
    for L in (4, 10, 100, 400):
        ps, pb = p_finite(L, PC_SITE), p_finite(L, PC_BOND)
        print(f"  L={L}: p_site={ps:.6f}, p_bond={pb:.6f}")
        rows.append(("finite", L, ps, pb, np.nan))

    # B 局域阈值随 neff 上移
    print("\nB 局域伪临界阈值")
    neffs = np.logspace(0, 5, 300)
    for n in (1, 10, 100, 10000):
        ps, pb = p_loc(n, PC_SITE), p_loc(n, PC_BOND)
        print(f"  n_eff={n}: p_loc(site)={ps:.6f}, p_loc(bond)={pb:.6f}")
        rows.append(("local", n, ps, pb, np.nan))

    # C 窗口宽度标度
    print("\nC 窗口宽度标度")
    widths = PC_SITE - p_loc(neffs, PC_SITE)
    sl, ic = np.polyfit(np.log(neffs), np.log(widths), 1)
    print(f"  双对数斜率={sl:.6f}（应 = -3/8 = {-3/8:.6f}）")
    for n in (10, 100, 1000):
        rows.append(("width", n, PC_SITE - p_loc(n, PC_SITE), np.nan, np.nan))

    # D 容量下限
    print("\nD 容量下限")
    nmin_s = (C_COEF / PC_SITE) ** (8.0 / 3.0)
    nmin_b = (C_COEF / PC_BOND) ** (8.0 / 3.0)
    print(f"  n_min(site)={nmin_s:.4f}, n_min(bond)={nmin_b:.4f}")
    for pc, nm in [(PC_SITE, nmin_s), (PC_BOND, nmin_b)]:
        print(f"    pc={pc}: n_eff={nm:.2f} 时 p_loc={p_loc(nm, pc):.6f}")
        rows.append(("capacity", pc, nm, p_loc(nm, pc), np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.4))

    ax[0, 0].plot(Ls, [p_finite(L, PC_SITE) for L in Ls], lw=2.2,
                  color="tab:blue", label=r"点渗流 $p_c=0.592746$")
    ax[0, 0].plot(Ls, [p_finite(L, PC_BOND) for L in Ls], lw=2.2,
                  color="tab:orange", label=r"键渗流 $p_c=1/2$")
    ax[0, 0].axhline(PC_SITE, color="tab:blue", ls="--", lw=1, alpha=0.6)
    ax[0, 0].axhline(PC_BOND, color="tab:orange", ls="--", lw=1, alpha=0.6)
    ax[0, 0].set_xscale("log")
    ax[0, 0].set_xlabel(r"线性尺寸 $L$")
    ax[0, 0].set_ylabel(r"$p_c(L)$")
    ax[0, 0].set_title(r"A  有限尺寸阈值下移（$\Delta p\sim L^{-3/4}$）")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3, which="both")

    ax[0, 1].plot(neffs, [p_loc(n, PC_SITE) for n in neffs], lw=2.2,
                  color="tab:blue", label="点渗流")
    ax[0, 1].plot(neffs, [p_loc(n, PC_BOND) for n in neffs], lw=2.2,
                  color="tab:orange", label="键渗流")
    ax[0, 1].set_xscale("log")
    ax[0, 1].set_xlabel(r"参与比 $n_{\rm eff}$")
    ax[0, 1].set_ylabel(r"$p_c^{\rm loc}$")
    ax[0, 1].set_title(r"B  局域阈值随 $n_{\rm eff}$ 上移")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3, which="both")

    ax[1, 0].loglog(neffs, widths, lw=2.4, color="tab:green",
                    label=rf"$\Delta p=C n^{{-3/8}}$（拟合斜率 {sl:.4f}）")
    ax[1, 0].loglog(neffs, C_COEF * neffs ** (-3.0 / 8.0), "--",
                   lw=1.8, color="tab:red", label=r"理论 $-3/8$")
    ax[1, 0].set_xlabel(r"$n_{\rm eff}$")
    ax[1, 0].set_ylabel(r"并存窗口宽度 $\Delta p$")
    ax[1, 0].set_title("C  双对数斜率核对：$-3/8$")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3, which="both")

    ns = np.logspace(-2, 2, 300)
    ax[1, 1].plot(ns, [p_loc(n, PC_SITE) for n in ns], lw=2.2, color="tab:blue")
    ax[1, 1].axhline(0, color="tab:red", ls="--", lw=1.2)
    ax[1, 1].axvline(nmin_s, color="tab:green", ls=":", lw=1.6,
                     label=rf"$n_{{\min}}=(C/p_c)^{{8/3}}={nmin_s:.3f}$")
    ax[1, 1].set_xscale("log")
    ax[1, 1].set_xlabel(r"参与比 $n_{\rm eff}$")
    ax[1, 1].set_ylabel(r"$p_c^{\rm loc}$")
    ax[1, 1].set_title("D  窗口存在的容量下限（$p_c^{\\rm loc}>0$）")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3, which="both")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
