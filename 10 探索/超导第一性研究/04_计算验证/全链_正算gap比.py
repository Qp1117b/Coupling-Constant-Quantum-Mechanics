# -*- coding: utf-8 -*-
"""
全链正算 gap ratio 与实验对照（非反解、非拟合）——首次从头算到尾验证。

CQM 完整输出（已对齐 Eliashberg Eq37）：
  omega_log = e^{-1/3} theta_D   (目标.3)
  T* = T_c  (对齐后)
Webb 2015 Eq6 (Mitrović):
  2Delta_0/(k_B T_c) = 3.53 [1 + 12.5 (T_c/omega_ln)^2 ln(omega_ln/(2 T_c))]
此式不含 mu*——gap ratio 在 Eliashberg 里只依赖 T_c/omega_ln。

四面板：A 正算 gap ratio vs T_c/omega；B 与各元素实验值对照；
C 强耦合偏离随耦合增；D 同位素指数 CQM 端点 vs 实验（Webb Table III）。
"""

import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "全链_正算gap比.png")
OUT_CSV = os.path.join(HERE, "全链_正算gap比.csv")

E3 = math.exp(-1 / 3)
BCS = 3.53

# Webb 2015 Table III: element, Tc(K), theta_D(K), isotope alpha_exp (or None)
# 实验 gap ratio 典型值（文献标准值，数量级对照）
DATA = [
    ("Al", 1.18, 428, 0.345, 3.44),
    ("Sn", 3.70, 200, 0.46, 3.51),
    ("Pb", 7.20, 105, 0.48, 4.29),
    ("Nb", 9.25, 275, None, 3.80),
    ("V",  5.40, 380, 0.15, 3.60),
    ("Cd", 0.52, 209, 0.50, 3.37),
    ("Ta", 4.40, 240, 0.35, 3.65),
    ("In", 3.40, 108, None, 3.50),
]


def mitrovic(tc, wlog):
    """Webb Eq6: gap ratio from Eliashberg, no mu*."""
    x = tc / wlog
    return BCS * (1 + 12.5 * x * x * math.log(wlog / (2 * tc)))


def main():
    rows = []
    # A 正算曲线
    xs = np.logspace(-3, -0.7, 200)  # T_c/omega_ln
    ratios = [BCS * (1 + 12.5 * x * x * math.log(1 / (2 * x))) for x in xs]
    print("A Mitrovic 正算 gap ratio: T_c/omega_ln -> 0 时趋于 3.53")
    for x, r in zip(xs[::50], ratios[::50]):
        rows.append(("curve", x, r, BCS, np.nan))
    print(f"  x=1e-3: {ratios[0]:.4f}; x=0.2: {ratios[-1]:.4f}")

    # B 元素正算 vs 实验
    print("\nB 元素正算 (CQM: omega_log=e^{-1/3}theta_D) vs 实验 gap ratio")
    print(f"{'el':<4}{'Tc/wlog':>10}{'理论':>8}{'实验':>8}{'偏差':>8}")
    names, xs_el, ths, exps = [], [], [], []
    for name, tc, th, alpha, gexp in DATA:
        wlog = E3 * th
        gth = mitrovic(tc, wlog)
        names.append(name); xs_el.append(tc/wlog); ths.append(gth); exps.append(gexp)
        err = (gth - gexp) / gexp
        print(f"{name:<4}{tc/wlog:>10.4f}{gth:>8.3f}{gexp:>8.3f}{err:>+8.1%}")
        rows.append(("element", tc/wlog, gth, gexp, f"{name}|{err:.4f}"))
    ths = np.array(ths); exps = np.array(exps)
    print(f"  平均 |偏差| = {np.mean(np.abs(ths-exps)/exps):.1%}")

    # C 强耦合偏离
    print("\nC 偏离 BCS 随耦合(T_c/omega)增")
    for name, x, g in zip(names, xs_el, ths):
        rows.append(("deviation", x, g - BCS, np.nan, name))

    # D 同位素指数: CQM 端点 {0, 1/2} vs 实验
    print("\nD 同位素指数: CQM 端点 alpha∈{0,1/2} (审-10) vs 实验")
    alphas = [d[3] for d in DATA if d[3] is not None]
    print(f"  实验 alpha 范围: {min(alphas):.2f} - {max(alphas):.2f}（落在 [0,1/2] 内）")
    for name, tc, th, alpha, gexp in DATA:
        if alpha is not None:
            rows.append(("isotope", 0, alpha, np.nan, name))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.4, 9.6))

    ax[0, 0].semilogx(xs, ratios, lw=2.4, color="tab:blue")
    ax[0, 0].axhline(BCS, color="tab:red", ls="--", lw=1.4, label="BCS 3.53")
    ax[0, 0].set_xlabel(r"$T_c/\omega_{\ln}$")
    ax[0, 0].set_ylabel(r"$2\Delta_0/k_BT_c$")
    ax[0, 0].set_title("A  Mitrović 正算（无 $\\mu^*$）")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3, which="both")

    x = np.arange(len(names))
    ax[0, 1].bar(x - 0.18, ths, 0.36, label="CQM 正算", color="tab:blue", alpha=0.8)
    ax[0, 1].bar(x + 0.18, exps, 0.36, label="实验", color="tab:orange", alpha=0.8)
    ax[0, 1].set_xticks(x)
    ax[0, 1].set_xticklabels(names)
    ax[0, 1].set_ylabel("gap ratio")
    ax[0, 1].set_title("B  正算 vs 实验（首次从头算到尾）")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3, axis="y")

    ax[1, 0].plot(xs_el, ths - BCS, "o", color="tab:purple", ms=6)
    for nm, xx, yy in zip(names, xs_el, ths):
        ax[1, 0].annotate(nm, (xx, yy - BCS), fontsize=8)
    ax[1, 0].set_xlabel(r"$T_c/\omega_{\ln}$")
    ax[1, 0].set_ylabel(r"$\Delta$ gap ratio $-3.53$")
    ax[1, 0].set_title("C  强耦合偏离随 $T_c/\\omega$ 增")
    ax[1, 0].grid(alpha=0.3)

    a_names = [d[0] for d in DATA if d[3] is not None]
    a_vals = [d[3] for d in DATA if d[3] is not None]
    ax[1, 1].bar(a_names, a_vals, color="tab:green", alpha=0.8)
    ax[1, 1].axhline(0.5, color="tab:red", ls="--", lw=1.4, label="CQM 端点 1/2")
    ax[1, 1].axhline(0, color="tab:blue", ls=":", lw=1.4, label="CQM 端点 0")
    ax[1, 1].set_ylabel("同位素指数 $\\alpha$")
    ax[1, 1].set_title("D  CQM 端点 vs 实验（无 $\\mu^*$ 仅端点）")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
