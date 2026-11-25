# -*- coding: utf-8 -*-
"""
审-10：截断口径、维度一致性与同位素指数的条件分类。

核对：
  1. w(T) 的维度：2D Debye 权重 2y 给低温 T^2（系数 pi^2/3），
     3D 权重 3y^2 给低温 T^3；CQM 的 w(T) 是 2D，故 (目标.3) 的
     3y^2 权重与之不一致，应回改为 e^{-1/2}。
  2. omega_log 的对数矩：2D 给 exp(-1/2)=0.6065，3D 给 exp(-1/3)=0.7165。
  3. 同位素指数：由 T_c = (pi/2) Upsilon_0 Q(T_c/omega_D) 的标度，
     若 Upsilon_0 质量无关则 alpha -> 0（小 Upsilon_0/omega_D 极限），
     若 Upsilon_0 ∝ omega_D 则 alpha = 1/2。

只做解析形状、维度核对与标度分类，不拟合实验。
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
OUT_PNG = os.path.join(HERE, "环10_审10截断与同位素.png")
OUT_CSV = os.path.join(HERE, "环10_审10截断与同位素.csv")
OUT_SUM = os.path.join(HERE, "环10_审10截断与同位素_摘要.csv")

G = 0.622281   # 目标区得到的涡旋损耗因子（c=2）


def w_debye(T, omegaD=1.0, dim=2):
    """w(T; omegaD) 只依赖 T/omegaD。dim=2 权重 2y，dim=3 权重 3y^2。"""
    if T <= 0:
        return 1.0
    y = np.linspace(0.0, 1.0, 4001)
    weight = 2.0 * y if dim == 2 else 3.0 * y ** 2
    x = omegaD * y
    return float(np.trapezoid(weight * np.tanh(x / (2.0 * T)), y))


def solve_Tc(U0, omegaD, g=G):
    """自洽解 T_c = (pi/2) U0 g w(T_c/omegaD)，忽略 Phi 比（Q 上界形状）。"""
    Tc = math.pi * U0 * g / 2.0
    for _ in range(300):
        new = math.pi * U0 * g * w_debye(Tc, omegaD) / 2.0
        if abs(new - Tc) < 1e-14:
            Tc = new
            break
        Tc = new
    return Tc


def main():
    rows = []
    T_grid = np.linspace(1e-3, 1.2, 300)
    for T in T_grid:
        w2 = w_debye(T, 1.0, 2)
        w3 = w_debye(T, 1.0, 3)
        rows.append(("A", T, w2, w3))

    # omega_log 对数矩（解析值已在 Lean）
    omega2 = math.exp(-0.5)
    omega3 = math.exp(-1.0 / 3.0)
    rows.append(("B", 2, omega2, omega2 / omega3))
    rows.append(("B", 3, omega3, 1.0))

    # 同位素：固定 U0 与 U0 ∝ omegaD 两支
    omega_grid = np.geomspace(0.2, 5.0, 60)
    for om in omega_grid:
        tc_fixed = solve_Tc(0.2, om)
        tc_scaled = solve_Tc(0.2 * om, om)
        rows.append(("C", om, tc_fixed, tc_scaled))

    # 有效 alpha = (1/2) dlnTc/dlnomegaD
    def alpha_of(vals):
        ln_om = np.log(omega_grid)
        ln_tc = np.log(np.array(vals))
        return 0.5 * np.gradient(ln_tc, ln_om)

    a_fixed = alpha_of([solve_Tc(0.2, om) for om in omega_grid])
    a_scaled = alpha_of([solve_Tc(0.2 * om, om) for om in omega_grid])

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["panel", "x", "y1", "y2"])
        wr.writerows(rows)

    with open(OUT_SUM, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["quantity", "value", "note"])
        wr.writerow(["omega_log_2D_over_omegaD", omega2, "exp(-1/2)"])
        wr.writerow(["omega_log_3D_over_omegaD", omega3, "exp(-1/3), old (目标.3)"])
        wr.writerow(["ratio", omega2 / omega3, "2D/3D"])
        wr.writerow(["alpha_fixed_U0_end", a_fixed[0], "small omegaD end"])
        wr.writerow(["alpha_fixed_U0_other", a_fixed[-1], "large omegaD end"])
        wr.writerow(["alpha_scaled_U0_end", a_scaled[0], "U0 proportional omegaD"])
        wr.writerow(["alpha_scaled_U0_other", a_scaled[-1], "should be 0.5"])

    fig, ax = plt.subplots(2, 2, figsize=(12.5, 10.0))

    ax[0, 0].plot(T_grid, [w_debye(T, 1.0, 2) for T in T_grid], lw=1.8,
                  label="2D 权重 $2y$（CQM 现行）")
    ax[0, 0].plot(T_grid, [w_debye(T, 1.0, 3) for T in T_grid], lw=1.8,
                  label="3D 权重 $3y^2$")
    ax[0, 0].set_xlabel("$T/\\omega_D$")
    ax[0, 0].set_ylabel("$w$")
    ax[0, 0].set_title("A  $w(T)$ 的维度：低温 $T^2$ vs $T^3$")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    dims = ["2D $2y$", "3D $3y^2$"]
    vals = [omega2, omega3]
    ax[0, 1].bar(dims, vals, color=["tab:blue", "tab:orange"])
    ax[0, 1].axhline(omega2, color="tab:blue", ls=":", lw=1.0)
    ax[0, 1].set_ylabel("$\\omega_{\\log}/\\omega_D$")
    ax[0, 1].set_title("B  对数矩：0.6065（2D）vs 0.7165（3D）")
    ax[0, 1].grid(alpha=0.3, axis="y")

    ax[1, 0].loglog(omega_grid, [solve_Tc(0.2, om) for om in omega_grid],
                    lw=1.8, label=r"$\Upsilon_0$ 质量无关")
    ax[1, 0].loglog(omega_grid, [solve_Tc(0.2 * om, om) for om in omega_grid],
                    lw=1.8, label=r"$\Upsilon_0\propto\omega_D$")
    ax[1, 0].set_xlabel("$\\omega_D$")
    ax[1, 0].set_ylabel("$T_c$")
    ax[1, 0].set_title("C  两支同位素标度")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3, which="both")

    ax[1, 1].semilogx(omega_grid, a_fixed, lw=1.8, label=r"$\Upsilon_0$ 固定")
    ax[1, 1].semilogx(omega_grid, a_scaled, lw=1.8,
                      label=r"$\Upsilon_0\propto\omega_D$")
    ax[1, 1].axhline(0.5, color="k", ls="--", lw=1.0, label="BCS 极限 1/2")
    ax[1, 1].set_xlabel("$\\omega_D$")
    ax[1, 1].set_ylabel(r"$\alpha=\frac{1}{2} d\ln T_c/d\ln\omega_D$")
    ax[1, 1].set_ylim(-0.05, 0.65)
    ax[1, 1].set_title("D  同位素指数的两个条件端点")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)

    print(f"omega_log 2D/omegaD = {omega2:.6f}, 3D = {omega3:.6f}, ratio = {omega2/omega3:.6f}")
    print(f"alpha (U0 fixed): first={a_fixed[0]:.6f}, last={a_fixed[-1]:.6f}")
    print(f"alpha (U0 ~ omegaD): first={a_scaled[0]:.6f}, last={a_scaled[-1]:.6f}")


if __name__ == "__main__":
    main()
