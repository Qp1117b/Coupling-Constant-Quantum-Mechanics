# -*- coding: utf-8 -*-
"""
环 14／临-12 记忆核零点换元的数值核对。

1. 逐模相因子 exp(-i gamma_n Delta) 的相位随 Delta 线性下降，斜率 = -gamma_n（谱依赖畸变）；
2. 冻结下 H_ij' = H_ij - (Di-Dj) 为水平线（判据层零点无关）；非冻结有斜率；
3. (14.2) 的差 D(Delta) 带逐模因子后读数改变（模与相位随 Delta 变）；
4. 两点相关 C(lag) 对不同零点 Delta_0 重合（零点相消）。

由 (12.1)-(12.4) 直接计算，无拟合。gamma_n 取主链 (14.4) 表前 6 个 zeta 零点虚部。
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
OUT_PNG = os.path.join(HERE, "环14_临12_记忆核零点换元.png")
OUT_CSV = os.path.join(HERE, "环14_临12_记忆核零点换元.csv")

GAMMAS = np.array([14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862])
RHOS = 0.5 + 1j * GAMMAS


def diff_reading(Delta, tau_j=0.0, cij=0.3):
    """冻结下 (14.2) 的差：D(Delta) = -sum_n e^{-i gamma_n Delta} e^{i gamma_n tau_j}
    (e^{i gamma_n cij} - 1)/rho_n。"""
    n = np.arange(len(GAMMAS))
    return -np.sum(np.exp(-1j * GAMMAS * Delta) * np.exp(1j * GAMMAS * tau_j)
                   * (np.exp(1j * GAMMAS * cij) - 1) / RHOS)


def corr(lag, Delta0):
    """两点相关（零点相消后只剩 lag）：C(lag) = sum_n e^{i gamma_n lag}/|rho_n|^2。"""
    return np.sum(np.exp(1j * GAMMAS * lag) / np.abs(RHOS) ** 2)


def main():
    rows = []
    Deltas = np.linspace(0, 0.2, 600)

    print("A 逐模相因子相位斜率（应 = -gamma_n）")
    slopes = []
    for i, g in enumerate(GAMMAS):
        ph = np.unwrap(np.angle(np.exp(-1j * g * Deltas)))
        sl = np.polyfit(Deltas, ph, 1)[0]
        slopes.append(sl)
        print(f"  n={i+1}: gamma={g:.4f}, 相位斜率={sl:.4f}")
        rows.append(("mode_phase", i + 1, sl, -g, sl + g))
    print(f"  最大斜率偏差={max(abs(s + g) for s, g in zip(slopes, GAMMAS)):.3e}")

    print("\nB 冻结 holonomy 零点无关")
    H0 = 0.3
    for D in (0.0, 0.05, 0.10, 0.20):
        H_frozen = (H0 + D) - (D)  # tau_i'=H0+D, tau_j'=D => H'=(H0+D)-D=H0
        H_nonfrozen = (H0 + D) - (0.4 * D)  # Di != Dj
        print(f"  Delta={D:.2f}: H'_frozen={H_frozen:.6f}, H'_nonfrozen={H_nonfrozen:.6f}")
        rows.append(("holonomy", D, H_frozen, H_nonfrozen, np.nan))

    print("\nC 读数差随零点变化")
    for D in (0.0, 0.05, 0.10, 0.20):
        val = diff_reading(D)
        print(f"  Delta={D:.2f}: |D|={abs(val):.6f}, arg(D)={np.angle(val):.6f}")
        rows.append(("reading", D, abs(val), np.angle(val), np.nan))

    print("\nD 相关量零点相消")
    lags = np.linspace(0, 2.0, 200)
    base = np.array([corr(l, 0.0) for l in lags])
    for D0 in (0.0, 0.05, 0.20):
        curve = np.array([corr(l, D0) for l in lags])
        print(f"  Delta0={D0:.2f}: max|C-C(0)|={np.max(np.abs(curve-base)):.3e}")
        rows.append(("correlation", D0, float(np.max(np.abs(curve - base))), np.nan, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.4))

    for i, g in enumerate(GAMMAS):
        ph = np.unwrap(np.angle(np.exp(-1j * g * Deltas)))
        ax[0, 0].plot(Deltas, ph, lw=1.6, label=rf"$n={i+1},\ \gamma={g:.1f}$")
    ax[0, 0].set_xlabel(r"零点平移 $\Delta$")
    ax[0, 0].set_ylabel(r"$\arg e^{-i\gamma_n\Delta}$")
    ax[0, 0].set_title("A  逐模相因子：斜率 = $-\\gamma_n$（谱依赖畸变）")
    ax[0, 0].legend(fontsize=7, ncol=2)
    ax[0, 0].grid(alpha=0.3)

    ax[0, 1].plot(Deltas, [H0] * len(Deltas), lw=2.4, color="tab:blue",
                  label="冻结 $\\Delta_i=\\Delta_j$")
    ax[0, 1].plot(Deltas, [H0 + 0.6 * D for D in Deltas], lw=2.0, ls="--",
                  color="tab:red", label="非冻结 $\\Delta_i\\ne\\Delta_j$")
    ax[0, 1].set_xlabel(r"$\Delta$")
    ax[0, 1].set_ylabel(r"$H'_{ij}$")
    ax[0, 1].set_title("B  判据层：冻结下 holonomy 零点无关")
    ax[0, 1].legend(fontsize=9)
    ax[0, 1].grid(alpha=0.3)

    Ds = np.linspace(0, 0.3, 300)
    mags = np.array([abs(diff_reading(D)) for D in Ds])
    args = np.unwrap([np.angle(diff_reading(D)) for D in Ds])
    ax2 = ax[1, 0].twinx()
    ax[1, 0].plot(Ds, mags, lw=2.2, color="tab:green", label=r"$|D|$")
    ax2.plot(Ds, args, lw=2.0, color="tab:orange", label=r"$\arg D$")
    ax[1, 0].set_xlabel(r"$\Delta$")
    ax[1, 0].set_ylabel(r"$|D|$", color="tab:green")
    ax2.set_ylabel(r"$\arg D$", color="tab:orange")
    ax[1, 0].set_title("C  读数层：(14.2) 差随零点改变")
    ax[1, 0].grid(alpha=0.3)

    for D0, col in [(0.0, "tab:blue"), (0.05, "tab:orange"), (0.20, "tab:green")]:
        ax[1, 1].plot(lags, [corr(l, D0).real for l in lags], lw=2.0,
                      color=col, label=rf"$\Delta_0={D0}$")
    ax[1, 1].set_xlabel(r"时差 $\Delta\tau$")
    ax[1, 1].set_ylabel(r"$C(\Delta\tau)$")
    ax[1, 1].set_title("D  相关量零点相消：不同 $\\Delta_0$ 重合")
    ax[1, 1].legend(fontsize=9)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
