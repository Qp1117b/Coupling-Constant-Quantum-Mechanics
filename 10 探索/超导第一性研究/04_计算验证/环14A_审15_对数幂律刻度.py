# -*- coding: utf-8 -*-
"""
环 14.A／审-15 对数-幂律刻度相容性的数值核对。

1. Delta ln E_n 递减 vs Delta E_n 递增（同一谱的两种坐标——"冲突"是假象）；
2. 幂律谱 E_n=E_1 n^p 的双对数斜率（p=1/2/2）；
3. 态密度 g(omega)：3D 声学 ∝omega^2，2D 弯曲为常数；
4. 计数对数 ln N(E) 随 ln E 线性（斜率 = p）。

由 (15.1) 与标准态密度公式直接计算，无拟合。
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
OUT_PNG = os.path.join(HERE, "环14A_审15_对数幂律刻度.png")
OUT_CSV = os.path.join(HERE, "环14A_审15_对数幂律刻度.csv")


def main():
    rows = []
    ns = np.arange(1, 41)

    # A 两种坐标下的步长
    print("A 同一谱的两种步长")
    d_ln = 2 * np.log((ns + 1) / ns)          # CQM p=2 对数步长
    d_raw = (ns + 1.0) ** 2 - ns ** 2          # 原始步长 2n+1
    for n, a, b in zip(ns[::8], d_ln[::8], d_raw[::8]):
        print(f"  n={n}: Delta ln E={a:.6f}（递减）, Delta E={b:.1f}（递增）")
        rows.append(("steps", n, a, b, np.nan))

    # B 双对数斜率
    print("\nB 幂律谱双对数斜率")
    big_n = np.arange(2, 2001)
    for p in (1, 2):
        sl = np.polyfit(np.log(big_n), np.log(big_n.astype(float) ** p), 1)[0]
        print(f"  p={p}: 斜率={sl:.6f}")
        rows.append(("spectrum", p, sl, p, np.nan))

    # C 态密度
    print("\nC 态密度")
    om = np.linspace(0.1, 2, 200)
    g_3d = om ** 2              # 3D 声学：g ∝ omega^2
    g_2d = np.ones_like(om)     # 2D 弯曲：g = const
    print(f"  g_3d(0.5)={0.5**2:.4f}, g_2d(0.5)=1.0（常数）")
    for o in (0.5, 1.0, 1.5):
        rows.append(("dos", o, o ** 2, 1.0, np.nan))

    # D 计数对数线性
    print("\nD 计数对数")
    Es = np.logspace(-2, 2, 200)
    lnN = np.log(2.0 * Es ** 2)   # N0=2, N=N0 E^2
    sl2 = np.polyfit(np.log(Es), lnN, 1)[0]
    print(f"  ln N 对 ln E 斜率={sl2:.6f}（应 = 2）")
    for e in (0.01, 0.1, 1.0, 100.0):
        rows.append(("count", e, np.log(2.0 * e ** 2), np.nan, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.4))

    ax[0, 0].plot(ns, d_ln, lw=2.2, color="tab:blue", label=r"$\Delta\ln E_n\sim 2/n$")
    ax2 = ax[0, 0].twinx()
    ax2.plot(ns, d_raw, lw=2.2, color="tab:orange", label=r"$\Delta E_n=2n+1$")
    ax[0, 0].set_xlabel(r"$n$")
    ax[0, 0].set_ylabel(r"$\Delta\ln E_n$", color="tab:blue")
    ax2.set_ylabel(r"$\Delta E_n$", color="tab:orange")
    ax[0, 0].set_title("A  同一谱的两种坐标：一减一增")
    ax[0, 0].grid(alpha=0.3)

    for p, col in [(1, "tab:green"), (2, "tab:red")]:
        ax[0, 1].loglog(big_n, big_n.astype(float) ** p, lw=2.2,
                        color=col, label=rf"$E_n\propto n^{{{p}}}$")
    ax[0, 1].set_xlabel(r"$n$")
    ax[0, 1].set_ylabel(r"$E_n$")
    ax[0, 1].set_title("B  幂律谱双对数斜率 = $p$")
    ax[0, 1].legend(fontsize=9)
    ax[0, 1].grid(alpha=0.3, which="both")

    ax[1, 0].plot(om, g_3d, lw=2.2, color="tab:blue", label="3D 声学 $\\propto\\omega^2$")
    ax[1, 0].plot(om, g_2d, lw=2.2, color="tab:orange", label="2D 弯曲常数")
    ax[1, 0].set_xlabel(r"$\omega$")
    ax[1, 0].set_ylabel(r"$g(\omega)$")
    ax[1, 0].set_title("C  态密度的维数依赖（外部）")
    ax[1, 0].legend(fontsize=9)
    ax[1, 0].grid(alpha=0.3)

    ax[1, 1].plot(np.log(Es), lnN, lw=2.4, color="tab:purple",
                  label=rf"$\ln N=\ln N_0+p\ln E$（斜率 {sl2:.3f}）")
    ax[1, 1].set_xlabel(r"$\ln E$")
    ax[1, 1].set_ylabel(r"$\ln N$")
    ax[1, 1].set_title(r"D  计数坐标对数线性（粗化后 $S=\ln\Gamma$）")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
