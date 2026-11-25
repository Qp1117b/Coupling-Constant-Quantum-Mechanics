# -*- coding: utf-8 -*-
"""
环 26／`临-22` 阻尼率桥的数值核对。

1. tau_g = c/omega_D（c=1 示意）；
2. Gamma_n(T) = gamma_n^2 * kappa * T / omega_D^2 的 T 线性族；
3. Gamma_2/Gamma_1 = (gamma_2/gamma_1)^2 与 T、omega_D 无关；
4. N_eff ∝ T^{-1/2} 高温读数窗口压缩。

零点纵坐标只作示意；无拟合。
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
OUT_PNG = os.path.join(HERE, "环26_临22阻尼率桥.png")
OUT_CSV = os.path.join(HERE, "环26_临22阻尼率桥.csv")

GAMMAS = np.array([14.134725141, 21.022039639, 25.010857580])
C = 1.0
KAP = 1.0
WD = 10.0


def gamma_n(T, g, wd=WD):
    return g ** 2 * KAP * T / wd ** 2


def main():
    rows = []
    print("tau_g = c/omega_D (c=1)")
    for wd in (2.0, 10.0, 50.0):
        print(f"  omega_D={wd:5.1f}: tau_g={C/wd:.4f}")
        rows.append(("tau_g", wd, C / wd, np.nan, np.nan))

    print("\nGamma_n(T) 斜率 (omega_D=10, kappa=1)")
    for g in GAMMAS:
        slope = g ** 2 * KAP / WD ** 2
        print(f"  gamma={g:.6f}: slope={slope:.6f}, Gamma(1)={gamma_n(1.0, g):.6f}")
        rows.append(("gamma_slope", g, slope, gamma_n(1.0, g), np.nan))

    ratio = (GAMMAS[1] / GAMMAS[0]) ** 2
    print(f"\nGamma_2/Gamma_1 = {ratio:.6f} (independent of T, omega_D)")
    for T in (0.5, 1.0, 2.0):
        r = gamma_n(T, GAMMAS[1]) / gamma_n(T, GAMMAS[0])
        print(f"  T={T}: {r:.6f}")
        rows.append(("mode_ratio", T, r, ratio, np.nan))

    for T in (0.2, 0.5, 1.0, 2.0, 5.0):
        neff = np.sqrt(WD ** 2 / (KAP * T))
        rows.append(("neff_T", T, neff, 1 / np.sqrt(T), np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A
    wds = np.linspace(1, 50, 400)
    ax[0, 0].plot(wds, C / wds, lw=2.2, color="tab:blue", label=r"$\tau_g=c/\omega_D$")
    ax[0, 0].set_xlabel(r"$\omega_D$")
    ax[0, 0].set_ylabel(r"$\tau_g$")
    ax[0, 0].set_title("A  记忆时间由 Debye 支撑定（c=1 示意）")
    ax[0, 0].legend(fontsize=9)
    ax[0, 0].grid(alpha=0.3)

    # B
    Ts = np.linspace(0, 2, 300)
    for i, g in enumerate(GAMMAS):
        ax[0, 1].plot(Ts, gamma_n(Ts, g), lw=2.0,
                      label=rf"$\gamma_{i+1}$: $\Gamma\propto {g**2/WD**2:.3f}T$")
    ax[0, 1].set_xlabel(r"$T$（归一化）")
    ax[0, 1].set_ylabel(r"$\Gamma_n$")
    ax[0, 1].set_title(r"B  $\Gamma_n\propto T$：斜率随 $\gamma_n^2$ 变")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    # C
    ax[1, 0].bar(["Gamma_2/Gamma_1", "(gamma_2/gamma_1)^2"],
                 [ratio, ratio], color=["tab:orange", "tab:green"], alpha=0.85)
    ax[1, 0].set_ylabel("比值")
    ax[1, 0].set_title(r"C  模比与 $T$、$\omega_D$ 无关 => 不统一")
    ax[1, 0].set_ylim(0, ratio * 1.2)
    ax[1, 0].grid(alpha=0.3, axis="y")

    # D
    TT = np.logspace(-1, 1, 300)
    ax[1, 1].loglog(TT, 1 / np.sqrt(TT), lw=2.2, color="tab:purple",
                    label=r"$N_{\rm eff}\propto T^{-1/2}$")
    ax[1, 1].set_xlabel(r"$T$")
    ax[1, 1].set_ylabel(r"$N_{\rm eff}$（形状）")
    ax[1, 1].set_title("D  高温可读窗口压缩")
    ax[1, 1].legend(fontsize=9)
    ax[1, 1].grid(alpha=0.3, which="both")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
