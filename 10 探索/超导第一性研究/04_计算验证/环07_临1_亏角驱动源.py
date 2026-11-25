# -*- coding: utf-8 -*-
"""
环 7／临-1 亏角驱动源的数值核对。

1. 余弦定理给的偏导数与有限差分核对；
2. 六三角扇形在均匀缩放下亏角不变（几何一致性）；
3. 单条外边扰动给 epsilon 变化与符号；
4. epsilon_dot = chi * Edot 的线性族。

由 (1A.1)-(1A.3) 直接计算，无拟合。
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
OUT_PNG = os.path.join(HERE, "环07_临1_亏角驱动源.png")
OUT_CSV = os.path.join(HERE, "环07_临1_亏角驱动源.csv")


def angle_at_O(r1, r2, s):
    """三角形在中心顶点的角（余弦定理）。"""
    x = (r1 ** 2 + r2 ** 2 - s ** 2) / (2 * r1 * r2)
    return np.arccos(np.clip(x, -1, 1))


def deficit(r, s):
    """六三角扇形的中心亏角。"""
    return 2 * np.pi - sum(angle_at_O(r[i], r[(i + 1) % 6], s[i]) for i in range(6))


def main():
    rows = []
    a, b, c = 1.0, 1.0, 1.0
    theta = angle_at_O(a, b, c)
    sin = np.sin(theta)
    dtheta_dc_analytic = c / (a * b * sin)
    dtheta_da_analytic = (b * np.cos(theta) - a) / (a * b * sin)
    h = 1e-6
    dtheta_dc_fd = (angle_at_O(a, b, c + h) - angle_at_O(a, b, c - h)) / (2 * h)
    dtheta_da_fd = (angle_at_O(a + h, b, c) - angle_at_O(a - h, b, c)) / (2 * h)
    print("偏导数核对")
    print(f"  dtheta/dc: analytic={dtheta_dc_analytic:.6f}, fd={dtheta_dc_fd:.6f}")
    print(f"  dtheta/da: analytic={dtheta_da_analytic:.6f}, fd={dtheta_da_fd:.6f}")
    rows.append(("partial", 0, dtheta_dc_analytic, dtheta_dc_fd, np.nan))
    rows.append(("partial", 1, dtheta_da_analytic, dtheta_da_fd, np.nan))

    print("\n均匀缩放的亏角（应恒为 0）")
    r = np.ones(6)
    s = np.ones(6)
    print(f"  epsilon(1)={deficit(r, s):.3e}")
    for lam in (0.5, 1.0, 2.0, 5.0):
        e = deficit(lam * r, lam * s)
        print(f"  lambda={lam}: epsilon={e:.3e}")
        rows.append(("scaling", lam, e, 0.0, np.nan))

    print("\n单条外边扰动")
    ds = np.linspace(-0.3, 0.3, 200)
    eps = []
    for d in ds:
        sp = s.copy()
        sp[0] += d
        eps.append(deficit(r, sp))
    eps = np.array(eps)
    slope = np.polyfit(ds, eps, 1)[0]
    print(f"  d(epsilon)/d(s0) ~ {slope:.6f} (斜率)")
    for d in (-0.2, 0.0, 0.2):
        i = int(np.argmin(np.abs(ds - d)))
        rows.append(("perturb", ds[i], eps[i], np.nan, np.nan))

    print("\nepsilon_dot = chi * Edot")
    for dcoef in (0.1, 0.3, 0.5):
        chi = slope * dcoef
        for Edot in (0.5, 1.0, 2.0):
            rows.append(("drive", Edot, chi * Edot, chi, dcoef))
        print(f"  d_edge/dE={dcoef}: chi={chi:.6f}")

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    ax[0, 0].bar(["dtheta/dc", "dtheta/da"],
                 [dtheta_dc_analytic, dtheta_da_analytic], width=0.35,
                 color="tab:blue", alpha=0.85, label="解析")
    ax[0, 0].bar(np.array([0, 1]) + 0.35, [dtheta_dc_fd, dtheta_da_fd], width=0.35,
                 color="tab:orange", alpha=0.85, label="有限差分")
    ax[0, 0].set_title("A  余弦定理偏导数核对")
    ax[0, 0].legend(fontsize=9)
    ax[0, 0].grid(alpha=0.3, axis="y")

    lams = np.linspace(0.2, 5, 100)
    ax[0, 1].plot(lams, [deficit(lam * r, lam * s) for lam in lams], lw=2.2,
                  color="tab:green")
    ax[0, 1].set_xlabel(r"均匀缩放 $\lambda$")
    ax[0, 1].set_ylabel(r"$\varepsilon$")
    ax[0, 1].set_title("B  均匀缩放不改变亏角")
    ax[0, 1].grid(alpha=0.3)

    ax[1, 0].plot(ds, eps, lw=2.2, color="tab:purple")
    ax[1, 0].axhline(0, color="0.35", lw=1.0)
    ax[1, 0].set_xlabel(r"单边扰动 $\delta$")
    ax[1, 0].set_ylabel(r"$\varepsilon$")
    ax[1, 0].set_title(r"C  非均匀驱动才改变亏角")
    ax[1, 0].grid(alpha=0.3)

    Ed = np.linspace(0, 2, 100)
    for dcoef in (0.1, 0.3, 0.5):
        ax[1, 1].plot(Ed, slope * dcoef * Ed, lw=2.0,
                      label=rf"$d_e={dcoef}$")
    ax[1, 1].set_xlabel(r"$\dot E$")
    ax[1, 1].set_ylabel(r"$\dot\varepsilon$")
    ax[1, 1].set_title(r"D  $\dot\varepsilon=\chi\dot E$（$\chi$ = 几何×材料）")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
