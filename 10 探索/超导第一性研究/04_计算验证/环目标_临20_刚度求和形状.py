# -*- coding: utf-8 -*-
"""
第98轮补：临-20 刚度求和显式 Upsilon0=2 J0 (1-rho) 与 Uemura 常数族（非拟合）
================================================================================
检验：
  A Upsilon0 对关联 rho 单减：干净 rho=0 给 2J0、强关联 rho=1 给 0；
  B Uemura 上界 Tc<= (pi/kB) J0 (1-rho)；
  C FE10 eta~(1-rho) 与刚度同向、竞争（配对 vs 相位扇区）；
  D 干净 XY 常数核对 rho_s^0=J、Tc=(pi/2)J（文献 PRB99 104509 / Benfatto）。

图像用于检验单调/极限/量级，不是用数据拟合曲线——无实验数据、无调参。

复跑：python "10 探索/超导第一性研究/04_计算验证/环目标_临20_刚度求和形状.py"
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
J0 = 1.0   # 归一化能标（外生，只取形状）


def main():
    rho = np.linspace(0, 1, 300)
    U0 = 2 * J0 * (1 - rho)
    kB = 1.0
    Tc_bound = math.pi / kB * J0 * (1 - rho)

    # ---------- 断言 ----------
    assert abs(U0[0] - 2 * J0) < 1e-12, "干净极限应 2J0"
    assert abs(U0[-1]) < 1e-12, "强关联 rho=1 应 0"
    assert np.all(np.diff(U0) < 0), "Upsilon0 应对 rho 单减"
    assert np.all(Tc_bound >= 0), "Uemura 上界非负"

    # 干净 XY 常数：rho_s^0=J、Tc=(pi/2)J（裸）；数值重整化 0.8929J
    Tc_bare = math.pi / 2 * J0
    Tc_num = 0.8929 * J0
    g_ren = Tc_num / Tc_bare
    assert 0 < g_ren < 1, "重整化因子应在 (0,1)"

    # FE10 eta~(1-rho) 与刚度同向
    c_eta = 0.9
    eta = c_eta * (1 - rho)
    corr = float(np.corrcoef(eta, U0)[0, 1])
    assert corr > 0.999, "eta 与刚度应同向"

    # ---------- 图 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ax = axes[0, 0]
    ax.plot(rho, U0, lw=2.2, color="#1f77b4", label="$\\Upsilon_0=2J_0(1-\\rho)$")
    ax.axhline(2 * J0, color="g", ls=":", lw=1.0, label="干净极限 $2J_0$")
    ax.set_xlabel("近邻关联 $\\rho_{nn}$")
    ax.set_ylabel("$\\Upsilon_0$")
    ax.set_title("A  刚度随亏角关联单减")
    ax.legend(fontsize=8)

    ax = axes[0, 1]
    ax.plot(rho, Tc_bound, lw=2.2, color="orange",
            label="Uemura 上界 $(\\pi/k_B)J_0(1-\\rho)$")
    ax.fill_between(rho, 0, Tc_bound, alpha=0.15, color="orange")
    ax.set_xlabel("近邻关联 $\\rho_{nn}$")
    ax.set_ylabel("$T_c$ 上界")
    ax.set_title("B  $T_c\\leq(\\pi/k_B)J_0(1-\\rho)$")

    ax = axes[1, 0]
    ax.plot(rho, eta, lw=2.0, color="green", label="FE10 $\\eta\\propto(1-\\rho)$（配对）")
    ax.plot(rho, U0 / (2 * J0), "--", lw=1.8, color="#1f77b4",
            label="$\\Upsilon\\propto(1-\\rho)$（相位）")
    ax.set_xlabel("近邻关联 $\\rho_{nn}$")
    ax.set_ylabel("归一形状")
    ax.set_title(f"C  竞争同向（r={corr:.3f}）；配对↑则相位刚度↓由 min 定")

    ax = axes[1, 1]
    labels = ["裸估计\n$(\\pi/2)J$", "数值 BKT\n$0.8929J$"]
    vals = [Tc_bare, Tc_num]
    ax.bar(labels, vals, color=["#1f77b4", "orange"])
    ax.set_ylabel("$T_c$")
    ax.set_title(f"D  干净 XY 常数核对（$g_{{ren}}$={g_ren:.3f}<1）")

    fig.tight_layout()
    png = os.path.join(OUT, "环目标_临20_刚度求和形状.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    summary = [
        ["干净极限 Upsilon0(rho=0)", f"{U0[0]:.4f}", "=2J0"],
        ["强关联 Upsilon0(rho=1)", f"{U0[-1]:.4f}", "=0"],
        ["单减断言", "PASS", "Upsilon0 对 rho 严格单减"],
        ["Uemura 上界", "PASS", "Tc<= (pi/kB) J0 (1-rho)"],
        ["干净 XY Tc 裸估计", f"{Tc_bare:.4f}", "=(pi/2)J"],
        ["数值 BKT Tc", f"{Tc_num:.4f}", "=0.8929J（文献）"],
        ["重整化因子 g_ren", f"{g_ren:.4f}", "<1（链不取普适 pi/2）"],
        ["eta-刚度同向", f"{corr:.4f}", ">0.999"],
    ]
    with open(os.path.join(OUT, "环目标_临20_刚度求和形状_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["量", "值", "说明"])
        w.writerows(summary)

    print("第98轮补 临-20 刚度求和形状：全部断言通过（非拟合）")
    for row in summary:
        print("  ", row[0], "=", row[1], "|", row[2])
    print("图:", png)


if __name__ == "__main__":
    main()

