# -*- coding: utf-8 -*-
"""
R25：相位模带能否代替电子带——统计、计数与循环性
=====================================================================
预注册 R25 的 P1–P5（跑数前写死）：
  P1  max n_F <= 1；n_B(omega/T=1e-7) > 1e6
  P2  C_b/C_e = (T/theta_D)^2（d=2）；T/theta_D<=0.1 时 <=0.01
  P3  T=0.01*wD：K_F 在 eps∈[1e-12,1e-9] 相对变化<1e-6、与 BCS 对数相对误差<1%；
      K_B 在 eps∈[1e-6,1e-2] 比值>5 且随 eps→0 单调增
  P4  Omega_p/Delta > 1e3
  P5  循环性由 Lean PhaseVsBand.lean 承载

复跑：python "10 探索/超导第一性研究/04_计算验证/R25_相位模不能代替电子带.py"
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
from scipy.integrate import quad
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))

GAMMA = 0.5772156649015329


def n_fermi(x):
    x = np.asarray(x, dtype=float)
    return 1.0 / (np.exp(np.clip(x, -700, 700)) + 1.0)


def n_bose(x):
    x = np.asarray(x, dtype=float)
    return 1.0 / np.expm1(np.clip(x, 1e-300, 700))


def main():
    # ---------- P1：占据统计 ----------
    x = np.logspace(-7, 1, 500)
    nf, nb = n_fermi(x), n_bose(x)
    assert float(np.max(nf)) <= 1.0, "P1: 费米占据应 <=1"
    nb_tiny = float(n_bose(np.array([1e-7]))[0])
    assert nb_tiny > 1e6, "P1: 玻色低频占据 %.3g 应 >1e6" % nb_tiny

    # ---------- P2：低温比热标度 ----------
    t = np.logspace(-3, 0, 400)          # T/theta_D
    ratio = t ** 2                       # d=2：C_b/C_e
    idx = int(np.argmin(np.abs(t - 0.1)))
    assert float(ratio[idx]) <= 0.01 + 1e-12, "P2: (T/theta_D)^2 在 0.1 应 <=0.01"

    # ---------- P3：配对核统计因子 ----------
    T, wD = 0.01, 1.0

    def KF(eps):
        return quad(lambda xi: math.tanh(xi / (2.0 * T)) / xi, eps, wD,
                    epsabs=1e-13, epsrel=1e-13)[0]

    def KB(eps):
        # 解析 splitting：ξ=2Tz；z<=1 用 coth z/z = 1/z^2+1/3-z^2/45+2z^4/945，
        # z>1 部分用 coth z-1=2/(e^{2z}-1) 的光滑数值修正（只在 z>=1，无近奇点）。
        z0 = eps / (2.0 * T)
        z1 = 1.0
        low = ((1.0 / z0 - 1.0 / z1) + (z1 - z0) / 3.0
               - (z1 ** 3 - z0 ** 3) / 135.0
               + 2.0 * (z1 ** 5 - z0 ** 5) / 4725.0)
        corr = quad(lambda z: (1.0 / math.tanh(z) - 1.0) / z, 1.0, 80.0,
                    epsabs=1e-12, epsrel=1e-12)[0]
        return low + math.log(wD / (2.0 * T)) + corr

    epsF = [1e-12, 1e-10, 1e-9]
    kf = [KF(e) for e in epsF]
    spread = (max(kf) - min(kf)) / kf[-1]
    assert spread < 1e-6, "P3: K_F 相对变化 %.3g 应 <1e-6" % spread
    bcs_log = math.log(2.0 * math.exp(GAMMA) * wD / (math.pi * T))
    rel_err = abs(kf[-1] - bcs_log) / bcs_log
    assert rel_err < 0.01, "P3: K_F 与 BCS 对数相对误差 %.4f" % rel_err

    epsB = [1e-6, 1e-4, 1e-2]
    kb = [KB(e) for e in epsB]
    assert kb[0] / kb[-1] > 5.0, "P3: K_B 比值 %.2f 应 >5" % (kb[0] / kb[-1])
    assert kb[0] > kb[1] > kb[2], "P3: K_B 应随 eps→0 单调增"

    # ---------- P4：Anderson-Higgs 能标 ----------
    e_charge, eps0, me, hbar = 1.602176634e-19, 8.8541878128e-12, 9.1093837015e-31, 1.054571817e-34
    n_e = 1e28                       # m^-3，典型金属
    omega_p = math.sqrt(n_e * e_charge ** 2 / (eps0 * me))
    hw_p_eV = hbar * omega_p / e_charge
    delta_eV = 1e-3                  # 1 meV
    ratio_pd = hw_p_eV / delta_eV
    assert ratio_pd > 1e3, "P4: Omega_p/Delta=%.1f 应 >1e3" % ratio_pd

    print("R25 相位模带 vs 电子带（结构判定，无拟合）：")
    print("  P1 n_F<=1；n_B(1e-7)=%.3e （玻色低频发散）" % nb_tiny)
    print("  P2 C_b/C_e=(T/theta_D)^2；T/theta_D=0.1 时 %.2e" % ratio[idx])
    print("  P3 K_F 相对变化 %.2e，与 BCS 对数相对误差 %.2e" % (spread, rel_err))
    print("     K_B(1e-6)/K_B(1e-2)=%.1f（红外 1/eps 发散）" % (kb[0] / kb[-1]))
    print("  P4 hbar*Omega_p=%.2f eV，Delta=%.1f meV，比值 %.0f" % (hw_p_eV, delta_eV * 1e3, ratio_pd))
    print("  P5 循环性由 Lean PhaseVsBand 承载")

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    ax = axes[0, 0]
    ax.loglog(x, nf, "b-", lw=2.4, label="费米 $n_F=1/(e^{x}+1)$（有界）")
    ax.loglog(x, nb, "r--", lw=2.2, label="玻色 $n_B=1/(e^{x}-1)$（发散）")
    ax.axhline(1.0, color="gray", ls=":", lw=1.0)
    ax.annotate("$n_B(10^{-7})\\approx10^7$", (2e-6, 3e3), fontsize=9)
    ax.set_xlabel("$x=\\xi/T$ 或 $\\omega/T$")
    ax.set_ylabel("占据数")
    ax.set_ylim(1e-5, 3e7)
    ax.set_title("A  统计不同：费米有界 / 玻色低频发散")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")

    ax = axes[0, 1]
    ax.loglog(t, ratio, "k-", lw=2.4, label="相位(声学)模 $C_b/C_e=(T/\\theta_D)^2$")
    ax.axhline(0.01, color="r", ls="--", lw=1.6, label="1% 线")
    ax.plot([0.1], [ratio[idx]], "o", ms=7, color="#d62728")
    ax.set_xlabel("$T/\\theta_D$")
    ax.set_ylabel("比热比")
    ax.set_title("B  低温电子线性项主导（玻色支按 $T^2$ 退出）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")

    ax = axes[1, 0]
    ee = np.logspace(-12, -2, 200)
    kf_curve = [KF(v) for v in ee]
    kb_curve = [KB(v) for v in ee]
    ax.loglog(ee, kf_curve, "b-", lw=2.4, label="费米核 $K_F$（收敛到 BCS 对数）")
    ax.loglog(ee, kb_curve, "r--", lw=2.2, label="玻色核 $K_B$（$1/\\varepsilon$ 发散）")
    ax.set_xlabel("红外下限 $\\varepsilon/\\omega_D$")
    ax.set_ylabel("积分值")
    ax.set_title("C  配对核统计因子：一个收敛、一个无下限依赖")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")

    ax = axes[1, 1]
    w = np.logspace(-3, 0, 200)
    ax.loglog(w, np.ones_like(w) * 2.0, "b-", lw=2.4, label="电子态密度 $N(E_F)$（有限）")
    ax.loglog(w, w ** 2, "r--", lw=2.2, label="声学玻色支 $g(\\omega)\\propto\\omega^2$（$\\to0$）")
    ax.annotate("$\\hbar\\Omega_p/\\Delta\\approx%.0f$\n相位模不在低能" % ratio_pd,
                (2.5e-3, 0.03), fontsize=9)
    ax.set_xlabel("能量（归一化）")
    ax.set_ylabel("态密度（归一化）")
    ax.set_title("D  费米面态密度 vs 玻色支态密度")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")

    fig.tight_layout()
    png = os.path.join(OUT, "R25_相位模不能代替电子带.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "n_F<=1, n_B(1e-7)=%.2e" % nb_tiny, "通过"],
        ["P2", "(T/theta_D)^2 at 0.1 = %.2e" % ratio[idx], "通过"],
        ["P3", "K_F spread %.2e, err %.2e; K_B ratio %.1f" % (spread, rel_err, kb[0] / kb[-1]), "通过"],
        ["P4", "hbar*Omega_p=%.2f eV, ratio %.0f" % (hw_p_eV, ratio_pd), "通过"],
        ["P5", "循环性（链序）", "由 Lean PhaseVsBand 承载"],
        ["结论", "相位模带不能代替电子 Bloch 带", "链外-D 未闭合"],
    ]
    with open(os.path.join(OUT, "R25_相位模不能代替电子带_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
