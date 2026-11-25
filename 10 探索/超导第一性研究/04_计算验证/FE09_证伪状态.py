# -*- coding: utf-8 -*-
"""
R11: FE09 证伪状态——精确 Al 数据 3.53 vs BCS 下界 vs FE09 非普适曲线。
只检验下界结构与数据一致性，不拟合。仅用 numpy + scipy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/FE09_证伪状态.py"
"""
import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
KMAX = 200000
k = np.arange(1, KMAX + 1, dtype=float)
E = k**2
W5 = 1 / k**5
Z5 = float(np.sum(W5))
BCS_BASE = 2 * math.pi / math.exp(0.5772156649)  # 3.5278
AL_PRECISE = 3.53  # 精密隧穿（文献卡 R11）


def S5(D, T):
    x = np.sqrt(E**2 + D**2)
    return float(np.sum(W5 * E / x * np.tanh(x / (2 * T)))) if T > 0 else float(np.sum(W5 * E / x))


def bcs_ratio(t):
    return BCS_BASE * (1 + 12.5 * t**2 * np.log(1 / (2 * t)))


def assertions():
    out = {}
    # BCS 修正非负 ⇒ r >= 3.53（在 t∈(0,0.5]）
    ts = np.linspace(0.001, 0.5, 500)
    rs = bcs_ratio(ts)
    out["bcs_min_ratio"] = float(np.min(rs))
    out["bcs_all_ge_base"] = bool(np.all(rs >= BCS_BASE - 1e-12))
    out["bcs_base"] = float(BCS_BASE)

    # 精确 Al 落在 BCS 基线附近（偏差 <0.5%）
    out["al_precise_ratio"] = AL_PRECISE
    out["al_vs_bcs_relerr"] = float(abs(AL_PRECISE - BCS_BASE) / BCS_BASE)
    out["al_supports_bcs_within_half_pct"] = bool(out["al_vs_bcs_relerr"] < 0.005)

    # 旧 Kittel 2 位数据（R6）偏离更大
    out["al_kittel_2digit_ratio"] = 3.344
    out["al_kittel_relerr"] = float(abs(3.344 - BCS_BASE) / BCS_BASE)

    # FE09 要给 3.53 需 Lambda' 近阈（求根）
    target = 1 / 1.0
    lam_for_353 = []
    for L in np.linspace(0.97, 3.0, 300):
        if 1 / L >= Z5:
            continue
        D0 = brentq(lambda D: S5(D, 0) - 1 / L, 1e-10, 1e7)
        Tc = brentq(lambda T: S5(0, T) - 1 / L, 1e-10, 1e7)
        lam_for_353.append((2 * D0 / Tc, L))
    grid = np.array(lam_for_353)
    L_needed = float(np.interp(AL_PRECISE, grid[:, 0], grid[:, 1]))
    out["lambda_prime_needed_for_al"] = L_needed
    out["fe09_upper_limit"] = float(2 * brentq(lambda D: S5(D, 0) - 1 / 5, 1e-10, 1e7) /
                                    brentq(lambda T: S5(0, T) - 1 / 5, 1e-10, 1e7))
    out["fe09_cannot_reach_PbHg"] = bool(out["fe09_upper_limit"] < 4.4)
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # (a) BCS gap ratio vs Tc/omega_ln（下界 3.53）
    ax = axes[0, 0]
    ts = np.linspace(0.001, 0.5, 300)
    ax.plot(ts, bcs_ratio(ts), "b-", lw=2, label="BCS/Eliashberg (Webb 式6)")
    ax.axhline(BCS_BASE, color="k", ls="--", lw=1.5, label=f"普适基线 {BCS_BASE:.3f}")
    ax.set_xlabel(r"$T_c/\omega_{\ln}$")
    ax.set_ylabel(r"$2\Delta/k_BT_c$")
    ax.set_title("(a) BCS：r ≥ 3.53，随耦合上升")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (b) FE09 gap ratio vs Lambda'（可 <3.53，上限 3.95）
    ax = axes[0, 1]
    Ls = np.linspace(0.97, 5.0, 120)
    rs = []
    for L in Ls:
        if 1 / L >= Z5:
            rs.append(float("nan")); continue
        D0 = brentq(lambda D: S5(D, 0) - 1 / L, 1e-10, 1e7)
        Tc = brentq(lambda T: S5(0, T) - 1 / L, 1e-10, 1e7)
        rs.append(2 * D0 / Tc)
    ax.plot(Ls, rs, "purple", lw=2, label="FE09（核 1/k^5）")
    ax.axhline(BCS_BASE, color="r", ls="--", lw=1.5, label="BCS 3.528")
    ax.axhline(4.40, color="gray", ls=":", lw=1.5, label="Pb 实测 4.40（超 FE09 上限）")
    ax.set_xlabel(r"$\Lambda'$")
    ax.set_ylabel(r"$2\Delta/k_BT_c$")
    ax.set_title("(b) FE09：可 <3.53，上限 3.95")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (c) 精密 Al 点 vs 旧 2 位数据
    ax = axes[1, 0]
    labels = ["Kittel 1976\n(2位)", "精密隧穿", "BCS 基线"]
    vals = [3.344, AL_PRECISE, BCS_BASE]
    cols = ["gray", "tab:green", "red"]
    ax.bar(labels, vals, color=cols)
    ax.set_ylabel(r"$2\Delta/k_BT_c$")
    ax.set_title("(c) Al：精密值 3.53 支持 BCS，旧值是精度假象")
    ax.grid(alpha=0.3, axis="y")

    # (d) 判别性实验示意：r vs 独立 lambda
    ax = axes[1, 1]
    lam = np.linspace(0.3, 2.0, 100)
    ax.plot(lam, np.full_like(lam, BCS_BASE), "b-", lw=2, label="BCS：平台 3.53")
    ax.plot(lam, BCS_BASE * (1 + 0.15 * lam**2 * np.log(1 / (0.2 * lam + 1e-9))),
            "b:", lw=1.5, alpha=0.6)
    ax.scatter([0.4], [AL_PRECISE], c="green", s=90, zorder=5, label="Al 精密点")
    ax.axhline(3.95, color="purple", ls=":", lw=1.5, label="FE09 上限 3.95")
    ax.set_xlabel(r"独立耦合 $\lambda$（隧穿 $\alpha^2F$ 反演）")
    ax.set_ylabel(r"$2\Delta/k_BT_c$")
    ax.set_title("(d) 判别实验：平台(BCS) vs 上升(FE09)")
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3)

    fig.suptitle("R11: FE09 证伪状态——精密数据暂不支持，需判别性实验", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "FE09_证伪状态.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R11 数值断言 ===")
    for k_, v in a.items():
        print(f"{k_:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "FE09_证伪状态_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["assertion", "value"])
        for k_, v in a.items():
            w.writerow([k_, v])
    print(f"\n图像: {p}\n断言表: {path}")
