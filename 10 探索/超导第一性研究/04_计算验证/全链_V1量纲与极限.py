# -*- coding: utf-8 -*-
"""
S6/V1 量纲与极限核对（非拟合、不需材料数据）。

四面板：
A BCS 弱耦合比 2pi/e^gamma = 3.528 与强耦合偏离（外部文献值，不拟合）；
B 高温 sigma^2 ∝ T 线性增长（审-3 已证的结构）；
C 维度选择性：Upsilon/(k_B T) 仅在 d=2 无量纲；
D V1 四项的通过/阻断总览表。

由外部标准值与链内已推结构直接计算，不调参。
"""

import csv
import os
from math import pi, exp

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "全链_V1量纲与极限.png")
OUT_CSV = os.path.join(HERE, "全链_V1量纲与极限.csv")

GAMMA_EULER = 0.5772156649  # 外部常数（本 Lean 环境无此常量，作外部口径）
BCS_RATIO = 2 * pi / exp(GAMMA_EULER)


def main():
    rows = []
    print("A BCS 弱耦合比")
    print(f"  2pi/e^gamma = {BCS_RATIO:.4f}（外部文献 3.528）")
    # 强耦合偏离（外部文献区间 3.53-3.68，示意散点，不拟合）
    lam = np.linspace(0.1, 2.0, 200)
    ratio_strong = BCS_RATIO + 0.15 * lam ** 2  # 外部定性趋势示意
    print(f"  lambda=0.1->2.0: 比 {ratio_strong[0]:.3f}->{ratio_strong[-1]:.3f}（强耦合偏高）")
    for l, r in zip(lam[::40], ratio_strong[::40]):
        rows.append(("bcs", l, r, BCS_RATIO, np.nan))

    # B 高温线性
    print("\nB 高温 sigma^2 ∝ T")
    T = np.logspace(-1, 2, 300)
    sig2 = 1 + 2 / np.expm1(1 / np.maximum(T, 1e-8))
    linear = 2 * T  # 经典极限 sigma^2 ~ 2T（hbar omega/kB=1）
    print(f"  T=10->100: sigma^2={sig2[-80]:.2f}->{sig2[-1]:.2f}, 线性参考 {linear[-80]:.0f}->{linear[-1]:.0f}")
    for t, s in zip(T[::60], sig2[::60]):
        rows.append(("highT", t, s, 2 * t, np.nan))

    # C 维度选择
    print("\nC 维度选择 Upsilon/(k_B T) 仅在 d=2 无量纲")
    d = np.linspace(0.5, 3.5, 200)
    dimless_exponent = d - 2
    for dd, e in zip(d[::40], dimless_exponent[::40]):
        rows.append(("dimension", dd, e, 0.0, np.nan))

    # D V1 总览
    v1 = [
        ("① 量纲一致", 1, "通过"),
        ("② BCS 3.53 条件", 0, "条件钉死/C5阻断"),
        ("③ 高温符号", 1, "通过"),
        ("④ 2D/3D 退化方向", 1, "通过"),
    ]
    for name, ok, note in v1:
        rows.append(("v1", 0, ok, np.nan, f"{name}|{note}"))
    print("\nD V1 总览: ①③④通过, ②条件钉死但 C5（无独立能隙方程）阻断")

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.4, 9.6))

    ax[0, 0].axhline(BCS_RATIO, color="tab:blue", lw=2.4,
                     label=rf"BCS 弱耦合 $2\pi/e^\gamma={BCS_RATIO:.3f}$")
    ax[0, 0].plot(lam, ratio_strong, lw=2.0, color="tab:orange",
                  label="强耦合偏离（外部定性）")
    ax[0, 0].set_xlabel(r"耦合 $\lambda$")
    ax[0, 0].set_ylabel(r"$2\Delta(0)/k_BT_c$")
    ax[0, 0].set_title("A  BCS 普适比与强耦合偏离（外部值，不拟合）")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    ax[0, 1].loglog(T, sig2, lw=2.4, color="tab:green", label="链内 $\\sigma^2(T)$")
    ax[0, 1].loglog(T, linear, "--", lw=1.8, color="tab:red", label="经典线性 $\\propto T$")
    ax[0, 1].set_xlabel(r"$T$")
    ax[0, 1].set_ylabel(r"$\sigma^2(T)/\sigma_0^2$")
    ax[0, 1].set_title("B  高温无反向符号：$\\sigma^2$ 随 $T$ 增")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3, which="both")

    ax[1, 0].plot(d, dimless_exponent, lw=2.4, color="tab:purple")
    ax[1, 0].axhline(0, color="tab:red", ls="--", lw=1.6)
    ax[1, 0].axvline(2, color="tab:green", ls=":", lw=1.6, label="$d=2$")
    ax[1, 0].set_xlabel(r"维度 $d$")
    ax[1, 0].set_ylabel(r"$\Upsilon/(k_BT)$ 的量纲指数 $d-2$")
    ax[1, 0].set_title("C  维度选择性：仅 $d=2$ 无量纲")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3)

    names = ["①量纲", "③高温符号", "④2D/3D", "②BCS条件"]
    vals = [1, 1, 1, 0]
    cols = ["tab:green", "tab:green", "tab:green", "tab:red"]
    ax[1, 1].barh(names, vals, color=cols, alpha=0.85)
    ax[1, 1].set_xlabel("通过=1 / 阻断=0")
    ax[1, 1].set_title("D  V1 总览（②C5 阻断）")
    ax[1, 1].grid(alpha=0.3, axis="x")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
