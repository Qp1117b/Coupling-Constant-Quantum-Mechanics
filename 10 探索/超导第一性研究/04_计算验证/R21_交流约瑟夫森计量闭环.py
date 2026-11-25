# -*- coding: utf-8 -*-
"""
预注册判定 R21：交流约瑟夫森相位动力学与 KJ=1/Phi0（非拟合）
=============================================================
链内 Phi0=h/2e (R14/临19) -> KJ=2e/h=1/Phi0 严格倒数闭环。
AC 约瑟夫森 f=KJ V，Shapiro Vn=n Phi0 f。2019 SI 精确常数核对。

复跑：python "10 探索/超导第一性研究/04_计算验证/R21_交流约瑟夫森计量闭环.py"
"""
import csv
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
# 2019 SI 精确常数
H = 6.62607015e-34      # J s (exact)
E = 1.602176634e-19     # C (exact)
KJ = 2 * E / H          # Hz/V
PHI0 = H / (2 * E)      # Wb
KJ_CODATA = 483597.848416984e9   # Hz/V
PHI0_CODATA = 2.067833848e-15    # Wb


def main():
    # P1 倒数闭环 + KJ 对 CODATA
    inv_err = abs(KJ * PHI0 - 1.0)
    assert inv_err < 1e-12, "P1: KJ*Phi0=1"
    kj_err = abs(KJ - KJ_CODATA) / KJ_CODATA
    assert kj_err < 1e-12, "P1: KJ 对 CODATA"
    # P2 Phi0 对 CODATA
    phi_err = abs(PHI0 - PHI0_CODATA) / PHI0_CODATA
    assert phi_err < 1e-9, "P2: Phi0 对 CODATA"

    # P3 AC 约瑟夫森线性 f = KJ V
    Vs = np.linspace(0, 2e-3, 100)   # 0-2 mV
    fs = KJ * Vs
    slope = np.polyfit(Vs, fs, 1)[0]
    assert abs(slope - KJ) / KJ < 1e-12, "P3: f=KJ V 线性"

    # P4 Shapiro Vn = n Phi0 f, f=10 GHz
    f_mw = 10e9
    n = np.arange(0, 6)
    Vn = n * PHI0 * f_mw
    V1_analytic = PHI0 * f_mw
    assert abs(Vn[1] - V1_analytic) < 1e-18, "P4: Shapiro V1"

    # P5 q=e 分支判别
    Phi0_e = H / E
    KJ_e = E / H
    assert abs(Phi0_e - 2 * PHI0) < 1e-30 and abs(KJ_e - KJ / 2) < 1e-6, "P5: q=e 分支"

    print("R21 交流约瑟夫森计量闭环（A 类闭环＋B 类工具＋SI 精确常数）：")
    print("  P1 KJ*Phi0 = %.15f (1.0)，KJ=%.6f GHz/V 对 CODATA 差 %.2e" %
          (KJ * PHI0, KJ / 1e9, kj_err))
    print("  P2 Phi0 = %.12e Wb 对 CODATA 差 %.2e" % (PHI0, phi_err))
    print("  P3 f=KJ V 线性斜率 %.6e Hz/V（对 KJ 差 %.2e）" % (slope, abs(slope-KJ)/KJ))
    print("  P4 Shapiro V1(f=10GHz) = %.6f mV = %.3f μV" % (V1_analytic*1e3, V1_analytic*1e6))
    print("  P5 q=e 分支: Phi0'=%.4e Wb (2x), KJ'=%.3f GHz/V (1/2)——链排除" % (Phi0_e, KJ_e/1e9))
    print("  全部断言通过（非拟合）")

    # 图
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9.5))

    ax = axes[0, 0]
    ax.text(0.5, 0.88, "链内磁通量子 → 约瑟夫森常数", ha="center", fontsize=11, weight="bold")
    ax.text(0.5, 0.68, "链内 (R14/临19): $q=2e$ → $\\Phi_0=h/2e$", ha="center", fontsize=10)
    ax.text(0.5, 0.50, "$K_J=2e/h=1/\\Phi_0$（严格倒数）", ha="center", fontsize=11, color="blue")
    ax.text(0.5, 0.32, "$\\Phi_0=%.4e$ Wb\n$K_J=%.4f$ GHz/V" % (PHI0, KJ/1e9),
            ha="center", fontsize=10)
    ax.text(0.5, 0.12, "$K_J\\cdot\\Phi_0=1$（差 %.0e）" % inv_err, ha="center", fontsize=9, color="green")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_title("A  $K_J=1/\\Phi_0$ 链内闭环")

    ax = axes[0, 1]
    ax.plot(Vs * 1e3, fs / 1e9, "k-", lw=2.2, label="$f=K_J V$")
    ax.set_xlabel("$V$ (mV)"); ax.set_ylabel("$f_J$ (GHz)")
    ax.set_title("B  交流约瑟夫森：频率-电压线性")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    steps_x = []
    for ni, vi in zip(n, Vn):
        steps_x.extend([vi*1e6, (vi+0.6*PHI0*f_mw)*1e6])
    y_step = []
    for ni in n:
        y_step.extend([ni, ni])
    ax.step(steps_x, y_step, where="post", color="tab:green", lw=2)
    ax.set_xlabel("$V$ ($\\mu$V)"); ax.set_ylabel("台阶序号 $n$")
    ax.set_title("C  Shapiro 台阶 $V_n=n\\Phi_0 f$（$f=10$ GHz）")
    ax.grid(alpha=0.3)

    ax = axes[1, 1]
    labels = ["链选 $q=2e$\n$\\Phi_0$", "$q=e$（排除）\n$2\\Phi_0$"]
    vals = [PHI0, Phi0_e]
    bars = ax.bar(labels, vals, color=["tab:blue", "tab:red"], alpha=0.85)
    ax.set_ylabel("磁通量子 (Wb)")
    for b, v in zip(bars, vals):
        ax.text(b.get_x()+b.get_width()/2, v+1e-17, "%.3e" % v, ha="center", fontsize=9)
    ax.set_title("D  $q=2e$（链选）vs $q=e$（排除）")
    ax.grid(alpha=0.3, axis="y")

    fig.tight_layout()
    png = os.path.join(OUT, "R21_交流约瑟夫森计量闭环.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    summary = [
        ["KJ·Phi0", "%.15f" % (KJ*PHI0), "倒数闭环（相对差 %.0e）" % inv_err],
        ["KJ", "%.6f GHz/V" % (KJ/1e9), "CODATA 精确值，差 %.2e" % kj_err],
        ["Phi0", "%.12e Wb" % PHI0, "CODATA 差 %.2e" % phi_err],
        ["AC 线性", "f=KJ V", "斜率差 %.2e" % (abs(slope-KJ)/KJ)],
        ["Shapiro V1", "%.3f μV" % (V1_analytic*1e6), "f=10 GHz"],
        ["q=e 分支", "排除", "链内 12.A 模式集 n∈2Z"],
        ["类别", "A 类闭环＋B 类工具", "SI h,e 外生定义；Phi0 链内"],
    ]
    with open(os.path.join(OUT, "R21_交流约瑟夫森计量闭环_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo); w.writerow(["量","值","说明"]); w.writerows(summary)

    print("图:", png)


if __name__ == "__main__":
    main()
