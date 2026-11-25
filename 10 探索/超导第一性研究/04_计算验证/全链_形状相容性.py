# -*- coding: utf-8 -*-
"""
全链形状相容性综合检验（非拟合）。

把已推形状串到共同 T/p 轴，只验证结构相容、不调参贴合实验。
四面板：
A 热因子 sigma^2(T)=sigma_0^2[1+2n_B] 随 T 升；
B 配对判据 p_pair(T) 左尾随方差升（前夜配对）vs 相位刚度 Upsilon_R 降 -> T_BKT 截断；
C 退相干窗口 gamma*~1/sigma_a 与 R_n 随频率衰减；
D T_c = min{T*, T_BKT, T_theta} 给 dome 形状（形状自洽，非拟合数据）。

外生参数只用主链已登记数值口径并明确标注；不给绝对 T_c。
由已推形状直接计算，无拟合。
"""

import csv
import os

import numpy as np
from math import erf, sqrt

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "全链_形状相容性.png")
OUT_CSV = os.path.join(HERE, "全链_形状相容性.csv")

# 外生口径（主链已登记，仅用于形状示意，不拟合实验）
BKT_RATIO_LO, BKT_RATIO_HI = 0.7441, 0.7831  # T_BKT/T_bare, c=2
PC_SITE = 0.592746
SIGMA_A = 0.02  # 冻结固有时宽度（临-17，材料值示意）

EXTERNAL = [
    ("sigma_0^2", "零点方差（审-3）", "声子谱/耦合，链外-D"),
    ("t_Upsilon", "Uemura 指数（M8）", "外部普适指数≈1.3"),
    ("J, c", "相位刚度/BKT 重整化（临-20）", "交换积分与 c"),
    ("sigma_a", "冻结固有时宽度（临-17）", "材料微结构"),
    ("T*, T_BKT, T_theta", "三温度数值（D1/审-11）", "外生能标"),
]


def nB(T, hbar_omega_over_kB=1.0):
    x = hbar_omega_over_kB / np.maximum(T, 1e-8)
    return 1.0 / np.expm1(np.clip(x, 1e-8, 700))


def main():
    rows = []
    Ts = np.logspace(-2, 2, 400)  # T / (hbar omega / k_B)

    # A 热因子
    factor = 1 + 2 * nB(Ts)
    print("A 热因子 sigma^2/sigma_0^2")
    print(f"  T=0.01: {factor[0]:.4f}, T=100: {factor[-1]:.2f}（单调升）")
    for t, f in zip(Ts[::80], factor[::80]):
        rows.append(("thermal", t, f, np.nan, np.nan))

    # B 配对判据（左尾，随方差升）vs 相位刚度（随 T 降）
    p_pair = np.array([0.5 * (1 - erf((1.2 - 1.0) / (sqrt(2) * (1.0 + 0.25 * (f - 1)))))
                       for f in factor])
    ups = 1.0 / (1.0 + Ts ** 3)  # 相位刚度示意：随 T 降（形状，不拟合）
    T_bkt = 0.7441  # 取比值下界作示意（外生口径）
    print(f"\nB p_pair: {p_pair[0]:.4f} -> {p_pair[-1]:.4f}（升）; "
          f"Upsilon: {ups[0]:.3f} -> {ups[-1]:.3f}（降）")
    for t, p, u in zip(Ts[::80], p_pair[::80], ups[::80]):
        rows.append(("compete", t, p, u, np.nan))

    # C 退相干窗口与 R_n
    gammas = np.array([14.1347, 21.0220, 25.0109, 30.4249, 37.5862])
    Rn = np.exp(-0.5 * gammas ** 2 * SIGMA_A ** 2)
    window = 1.0 / SIGMA_A
    print(f"\nC sigma_a={SIGMA_A}: 窗口 gamma*≈{window:.1f}; "
          f"R_n={np.round(Rn, 4).tolist()}")
    for g, r in zip(gammas, Rn):
        rows.append(("decoherence", g, r, window, np.nan))

    # D dome：T*(p) 升、T_BKT(p) 降，min 给单峰（形状，非拟合）
    p = np.linspace(0.05, 0.30, 300)
    Tstar = 120 * (p - 0.05) / (0.30 - 0.05)          # 上升支示意
    Tbkt = 90 * (0.30 - p) / (0.30 - 0.05)            # 下降支示意
    Ttheta = 200 * np.ones_like(p)                    # 阻尼支不限制（示意）
    Tc = np.minimum(np.minimum(Tstar, Tbkt), Ttheta)
    ipk = int(np.argmax(Tc))
    print(f"\nD dome 峰位 p≈{p[ipk]:.3f}, T_c^shape≈{Tc[ipk]:.1f}（形状，非实验值）")
    for pp, ts, tb, tc in zip(p[::40], Tstar[::40], Tbkt[::40], Tc[::40]):
        rows.append(("dome", pp, tc, min(ts, tb), np.nan))

    # 外生缺口清单
    for name, meaning, src in EXTERNAL:
        rows.append(("external", 0, 0, np.nan, f"{name}|{meaning}|{src}"))
    print("\n外生输入清单（绝对 T_c 仍需这些材料值）:")
    for name, meaning, src in EXTERNAL:
        print(f"  {name}: {meaning} [{src}]")

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.4, 9.6))

    ax[0, 0].semilogx(Ts, factor, lw=2.4, color="tab:blue")
    ax[0, 0].set_xlabel(r"$T\,/\,(\hbar\omega/k_B)$")
    ax[0, 0].set_ylabel(r"$\sigma^2(T)/\sigma_0^2$")
    ax[0, 0].set_title("A  热方差随 T 升（(4.1)，非拟合）")
    ax[0, 0].grid(alpha=0.3, which="both")

    ax[0, 1].semilogx(Ts, p_pair, lw=2.2, color="tab:green", label=r"$p_{\rm pair}$ 升")
    ax[0, 1].semilogx(Ts, ups, lw=2.2, color="tab:red", label=r"$\Upsilon_R$ 降")
    ax[0, 1].axvline(T_bkt, color="0.4", ls="--", lw=1.2,
                     label=r"$T_{\rm BKT}$ 截断（外生口径）")
    ax[0, 1].set_xlabel(r"$T$")
    ax[0, 1].set_ylabel("形状（归一）")
    ax[0, 1].set_title("B  配对升 vs 相位降 -> min 截断")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3, which="both")

    ax[1, 0].plot(gammas, Rn, "o-", lw=2.2, color="tab:purple")
    ax[1, 0].axvline(window, color="tab:red", ls="--", lw=1.4,
                     label=rf"$\gamma_*\approx1/\sigma_a\approx{window:.0f}$")
    ax[1, 0].set_xlabel(r"$\gamma_n$")
    ax[1, 0].set_ylabel(r"$R_n$")
    ax[1, 0].set_title("C  高频退相干（临-17，外生 sigma_a）")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3)

    ax[1, 1].plot(p, Tstar, lw=1.8, color="tab:green", ls="--", label=r"$T^*$ 升")
    ax[1, 1].plot(p, Tbkt, lw=1.8, color="tab:red", ls="--", label=r"$T_{\rm BKT}$ 降")
    ax[1, 1].plot(p, Tc, lw=3.0, color="tab:blue", label=r"$T_c=\min$（dome 形状）")
    ax[1, 1].plot(p[ipk], Tc[ipk], "o", ms=9, color="tab:blue")
    ax[1, 1].set_xlabel(r"掺杂 $p$（示意）")
    ax[1, 1].set_ylabel("温度（形状归一）")
    ax[1, 1].set_title("D  三温度取 min 自洽给 dome（非实验拟合）")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
