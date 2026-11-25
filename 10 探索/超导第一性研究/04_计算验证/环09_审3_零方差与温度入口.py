# -*- coding: utf-8 -*-
"""
环 9／审-3 零方差钉死与温度唯一入口的数值核对。

1. sigma^2(T)/sigma_0^2 = 1+2n_B = coth(hbar omega / 2 kT) 随 T 从 1 升到经典线性；
2. 零点项 sigma_0^2（恒定）与热项 2 n_B sigma_0^2（随 T 增）的分解；
3. (4.1) 的 sigma^2(T)（随 T 升）与 (9.1)(10.2) 的 sigma_0^2（恒定）对照；
4. 符号对齐：热方差增大时左尾判据 p_pair 的变化示意。

由 (3.1) 直接计算，无拟合。
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
OUT_PNG = os.path.join(HERE, "环09_审3_零方差与温度入口.png")
OUT_CSV = os.path.join(HERE, "环09_审3_零方差与温度入口.csv")

S0 = 1.0  # sigma_0^2 归一为 1（材料值外生）


def nB(x):
    """x = hbar omega / k_B T。"""
    return 1.0 / np.expm1(np.clip(x, 1e-8, 700))


def main():
    rows = []
    Ts = np.logspace(-2, 2, 400)  # 归一化温度 T / (hbar omega / k_B)

    # A sigma^2(T)/sigma_0^2
    x = 1.0 / Ts
    factor = 1 + 2 * nB(x)
    coth = 1.0 / np.tanh(x / 2)
    print("A sigma^2(T)/sigma_0^2")
    for t, f, c in zip(Ts[::80], factor[::80], coth[::80]):
        print(f"  T={t:.3f}: factor={f:.4f}, coth={c:.4f}")
        rows.append(("factor", t, f, c, np.nan))
    print(f"  coth 恒等式最大误差={np.max(np.abs(factor-coth)):.3e}")

    # B 分解
    zero = np.full_like(Ts, S0)
    thermal = factor - 1.0
    print("\nB 零点/热分解")
    for t, z, th in zip(Ts[::80], zero[::80], thermal[::80]):
        print(f"  T={t:.3f}: 零点={z:.3f}, 热={th:.4f}")
        rows.append(("split", t, z, th, np.nan))

    # C (4.1) vs (9.1)(10.2)
    print("\nC (4.1) 随 T vs (9.1)(10.2) 恒定")
    for t, f in zip(Ts[::80], factor[::80]):
        print(f"  T={t:.3f}: (4.1)={S0*f:.3f}, (9.1)(10.2)={S0:.3f}")
        rows.append(("entrance", t, S0 * f, S0, np.nan))

    # D 符号对齐示意：p_pair 随热方差（左尾）
    print("\nD 符号对齐（p_pair 随热方差）")
    sigma_th = np.linspace(0, 2, 200)
    # 左尾事件：阈值以下概率随方差增（示意：erfc 型）
    # p_pair ~ 0.5*erfc((x_c - mean)/(sqrt(2)*sigma))，取 mean=1, x_c=1.2
    from math import erf, sqrt
    p_pair = np.array([0.5 * (1 - erf((1.2 - 1.0) / (sqrt(2) * (1.0 + 0.3 * s))))
                       for s in sigma_th])
    print(f"  sigma_th=0: p_pair={p_pair[0]:.4f}; sigma_th=2: p_pair={p_pair[-1]:.4f}")
    for s, p in zip(sigma_th[::40], p_pair[::40]):
        rows.append(("sign", s, p, np.nan, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.4))

    ax[0, 0].semilogx(Ts, factor, lw=2.4, color="tab:blue", label=r"$1+2n_B$")
    ax[0, 0].semilogx(Ts, coth, "--", lw=1.6, color="tab:red", label=r"$\coth(\hbar\omega/2k_BT)$")
    ax[0, 0].axhline(1, color="0.4", ls=":", lw=1.2)
    ax[0, 0].set_xlabel(r"$T\,/\,(\hbar\omega/k_B)$")
    ax[0, 0].set_ylabel(r"$\sigma^2(T)/\sigma_0^2$")
    ax[0, 0].set_title("A  热因子从 1 升到经典线性")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    ax[0, 1].semilogx(Ts, zero, lw=2.2, color="tab:green", label=r"零点 $\sigma_0^2$")
    ax[0, 1].semilogx(Ts, thermal, lw=2.2, color="tab:orange", label=r"热 $2n_B\sigma_0^2$")
    ax[0, 1].set_xlabel(r"$T\,/\,(\hbar\omega/k_B)$")
    ax[0, 1].set_ylabel(r"方差贡献")
    ax[0, 1].set_title("B  零点项恒定、热项随 $T$ 增")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    ax[1, 0].semilogx(Ts, S0 * factor, lw=2.4, color="tab:blue", label="(4.1) 随 $T$")
    ax[1, 0].axhline(S0, color="tab:red", ls="--", lw=2.0, label="(9.1)(10.2) 用 $\\sigma_0^2$")
    ax[1, 0].set_xlabel(r"$T\,/\,(\hbar\omega/k_B)$")
    ax[1, 0].set_ylabel(r"$\sigma^2$")
    ax[1, 0].set_title("C  温度唯一入口：(9.1)(10.2) 不含 $T$")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3)

    ax[1, 1].plot(sigma_th, p_pair, lw=2.2, color="tab:purple")
    ax[1, 1].set_xlabel(r"热方差 $\sigma_{\rm th}^2$")
    ax[1, 1].set_ylabel(r"左尾 $p_{\rm pair}$")
    ax[1, 1].set_title("D  符号对齐：热方差升 ⇒ 左尾判据变化")
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
