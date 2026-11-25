# -*- coding: utf-8 -*-
"""
R4: 自我审计——12.A 模和 vs 配对通道模和。
证明 R2 的对数是「计数对数」，而 (10.2) 的 1/omega 分母使配对模和收敛（无 Cooper 对数）。
只检验极限/收敛/恒等，不拟合。仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/环节9_自我审计.py"
"""
import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
ZETA3 = 1.2020569031595943  # Apéry 常数（外部数学常数）

E2 = 1.0  # 归一化（E_k = E2 k^2）


def w_sum(K):
    """R2 的加权计数和 sum_{k=1}^K 1/k = H_K"""
    k = np.arange(1, K + 1, dtype=np.float64)
    return np.cumsum(1.0 / k)


def wV_sum(K):
    """配对通道模和 sum (1/k)(1/E_k) = (1/E2) sum 1/k^3"""
    k = np.arange(1, K + 1, dtype=np.float64)
    return np.cumsum(1.0 / (E2 * k**3))


def assertions():
    out = {}
    Ks = np.array([10, 100, 1000, 10000, 100000])
    Hs = np.array([w_sum(k)[-1] for k in Ks])
    Vs = np.array([wV_sum(k)[-1] for k in Ks])

    # (a) R2 计数和 ~ (1/2) ln E = ln K（K=sqrt(E/E2)）
    coeff = Hs[-1] / np.log(Ks[-1])
    out["counting_log_coeff"] = float(coeff)
    out["counting_log_target"] = 1.0

    # (b) 配对通道和收敛到 zeta(3)/E2
    out["pairing_sum_at_1e5"] = float(Vs[-1])
    out["zeta3_target"] = ZETA3
    out["pairing_sum_relerr_at_1e5"] = float(abs(Vs[-1] - ZETA3) / ZETA3)

    # (c) 全局 ≤ 2/E2（Lean 定理的数值核对）
    Kbig = 1000000
    out["pairing_sum_global_max"] = float(wV_sum(Kbig)[-1])
    out["bound_2_over_E2"] = 2.0 / E2

    # (d) 单项恒等 (1/k)(1/(E2 k^2)) = 1/(E2 k^3)
    k = 7.0
    lhs = (1 / k) * (1 / (E2 * k**2))
    rhs = 1 / (E2 * k**3)
    out["term_identity_relerr"] = float(abs(lhs - rhs) / abs(rhs))

    # (e) 两项在 K=1e5 的量级差：计数对数 ~11.5 vs 配对和 ~1.2（有界）
    out["log_vs_convergent_ratio"] = float(Hs[-1] / Vs[-1])
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    K = 20000
    karr = np.arange(1, K + 1)

    # (a) 两条部分和：对数增长 vs 收敛平台
    ax = axes[0, 0]
    ax.plot(karr, w_sum(K), "b-", lw=1.8, label=r"$\sum w_k=H_K\sim\ln K$（计数对数）")
    ax.plot(karr, wV_sum(K), "r-", lw=2, label=r"$\sum w_k|V_k|\to\zeta(3)/E_2$（收敛）")
    ax.set_xlabel(r"档数 $K$")
    ax.set_ylabel(r"部分和")
    ax.set_title("(a) R2 计数对数 vs 配对通道收敛")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (b) 计数和 vs ln K（线性，斜率 1）
    ax = axes[0, 1]
    Ks = np.logspace(1, 5, 400).astype(np.int64)
    Hs = np.array([w_sum(int(k))[-1] for k in Ks])
    ax.semilogx(Ks, Hs, "g-", lw=2)
    ax.set_xlabel(r"档数 $K$")
    ax.set_ylabel(r"$H_K$")
    ax.set_title(r"(b) $H_K\sim\ln K$（R2 的对数是计数对数）")
    ax.grid(alpha=0.3)

    # (c) 配对通道和收敛到 zeta(3)
    ax = axes[1, 0]
    ax.semilogx(karr, wV_sum(K), "purple", lw=2, label=r"$\sum 1/k^3$")
    ax.axhline(ZETA3, color="k", ls="--", lw=1.5, label=r"$\zeta(3)\approx1.202$")
    ax.axhline(2.0, color="gray", ls=":", lw=1.5, label=r"上界 $2$（Lean）")
    ax.set_xlabel(r"档数 $K$")
    ax.set_ylabel(r"$\sum w_k|V_k|$")
    ax.set_title("(c) 配对模和收敛：无 Cooper 对数")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (d) 示意：1/omega 分母把 1/k 压成 1/k^3
    ax = axes[1, 1]
    kk = np.arange(1, 51)
    ax.loglog(kk, 1 / kk, "b-", lw=2, label=r"$w_k=1/k$（对数发散）")
    ax.loglog(kk, 1 / kk**3, "r-", lw=2, label=r"$w_k/E_k=1/k^3$（收敛）")
    ax.set_xlabel(r"档号 $k$")
    ax.set_ylabel(r"单项大小")
    ax.set_title("(d) (10.2) 的 1/omega 分母改变收敛性")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    fig.suptitle("R4 自我审计：R2/R3 的 Cooper 对数主张被 no-go 回改（无拟合）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "环节9_自我审计.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R4 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "环节9_自我审计_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
