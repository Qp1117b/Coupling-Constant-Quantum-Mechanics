# -*- coding: utf-8 -*-
"""
环 26／临-8 有限模读出定理的数值核对（不拟合）。

1. 截断误差尾部 sum_{n>N} |W_n|/|rho_n| 随 N 衰减（不同 sigma_v^2 tau_g）；
2. 读出窗口 gamma_n sigma_v sqrt(tau_g) 随 n 增长穿过阈值 sqrt(<v>/2)，定 N*；
3. 有效核部分和对全和的逼近（相对误差随 N* 降）；
4. no-go 保持：两模 W_n 率不同（逐模不等）的数值确认。

由 (8F.1)(8F.2) 直接计算，无拟合。sigma_v^2 tau_g 取示意值（外生）。
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
OUT_PNG = os.path.join(HERE, "环26_临8_有限模读出.png")
OUT_CSV = os.path.join(HERE, "环26_临8_有限模读出.csv")

GAMMAS = np.array([14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862,
                   40.9187, 43.3271, 48.0052, 49.7738, 52.9703, 56.4462])


def main():
    rows = []
    t = 1.0
    alpha = 0.5

    # A 截断误差尾部
    print("A 截断误差尾部随 N 衰减")
    Ns = np.arange(1, len(GAMMAS) + 1)
    for k in (0.0005, 0.002, 0.008):
        Gamma = GAMMAS ** 2 * k
        W = np.exp(-(alpha + Gamma - 0.5) * t)
        rho = np.sqrt(0.25 + GAMMAS ** 2)
        terms = W / rho
        tails = np.array([np.sum(terms[N:]) for N in range(len(terms))])
        print(f"  k={k}: N=1 尾部={tails[0]:.3e}, N=6 尾部={tails[5]:.3e}")
        for N, tl in zip(Ns[::3], tails[::3]):
            rows.append(("tail", N, tl, k, np.nan))

    # B 读出窗口定 N*
    print("\nB 读出窗口定 N*")
    sig2tau = 0.002
    sv = np.sqrt(sig2tau)
    vmean_half = 1.0  # sqrt(<v>/2) 阈值（示意）
    quant = GAMMAS * sv  # gamma_n sigma_v sqrt(tau_g) = gamma_n sqrt(sig2tau)
    readable = quant < vmean_half
    Nstar = int(np.sum(readable))
    print(f"  sig2tau={sig2tau}: 阈值 sqrt(<v>/2)={vmean_half}")
    print(f"  gamma*sv = {np.round(quant,3).tolist()}")
    print(f"  可读模数 N*={Nstar}（前 {Nstar} 个满足窗口条件）")
    for i, q in enumerate(quant):
        rows.append(("window", i + 1, q, vmean_half, int(readable[i])))

    # C 有效核对全和逼近
    print("\nC 有效核部分和逼近")
    k = 0.002
    Gamma = GAMMAS ** 2 * k
    W = np.exp(-(alpha + Gamma - 0.5) * t)
    rho = np.sqrt(0.25 + GAMMAS ** 2)
    terms = np.exp(1j * GAMMAS * t) / rho * W
    full = np.sum(terms)
    for N in (2, 4, 6, 8, 10):
        approx = np.sum(terms[:N])
        rel = abs(approx - full) / abs(full)
        print(f"  N={N}: 相对误差={rel:.3e}")
        rows.append(("approx", N, rel, np.nan, np.nan))

    # D no-go 保持
    print("\nD no-go 保持：两模率不同")
    rates = alpha + Gamma
    print(f"  alpha+Gamma_n = {np.round(rates[:6],4).tolist()}（依 n 变，≠1/2）")
    for i in range(6):
        rows.append(("nogo", i + 1, rates[i], 0.5, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.4, 9.6))

    colors = ["tab:blue", "tab:orange", "tab:green"]
    for k, col in zip((0.0005, 0.002, 0.008), colors):
        Gamma = GAMMAS ** 2 * k
        W = np.exp(-(alpha + Gamma - 0.5) * t)
        rho = np.sqrt(0.25 + GAMMAS ** 2)
        terms = W / rho
        tails = [np.sum(terms[N:]) for N in range(len(terms))]
        ax[0, 0].semilogy(Ns, tails, "o-", ms=3, lw=1.6, color=col,
                          label=f"k={k}")
    ax[0, 0].set_xlabel("截断模数 $N$")
    ax[0, 0].set_ylabel("尾部误差界")
    ax[0, 0].set_title("A  截断误差随 N 衰减")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3, which="both")

    ax[0, 1].plot(np.arange(1, len(quant) + 1), quant, "o-", lw=2.0,
                  color="tab:blue")
    ax[0, 1].axhline(vmean_half, color="tab:red", ls="--", lw=1.6,
                     label=r"阈值 $\sqrt{\langle v\rangle/2}$")
    ax[0, 1].axvline(Nstar, color="tab:green", ls=":", lw=1.6,
                     label=rf"$N_*={Nstar}$（可读模数）")
    ax[0, 1].set_xlabel(r"模序号 $n$")
    ax[0, 1].set_ylabel(r"$\gamma_n\sqrt{\sigma_v^2\tau_g}$")
    ax[0, 1].set_title("B  读出窗口定 N*（26.A4）")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    Nlist = [2, 4, 6, 8, 10]
    rels = []
    for N in Nlist:
        approx = np.sum(terms[:N])
        rels.append(abs(approx - full) / abs(full))
    ax[1, 0].semilogy(Nlist, rels, "o-", lw=2.2, color="tab:purple")
    ax[1, 0].set_xlabel("截断模数 $N$")
    ax[1, 0].set_ylabel("相对误差")
    ax[1, 0].set_title("C  低阶部分和逼近全和")
    ax[1, 0].grid(alpha=0.3, which="both")

    ax[1, 1].plot(np.arange(1, 7), rates[:6], "o-", lw=2.2, color="tab:red",
                  label=r"$\alpha+\Gamma_n$（依 n）")
    ax[1, 1].axhline(0.5, color="0.4", ls="--", lw=1.4, label="目标率 1/2")
    ax[1, 1].set_xlabel(r"模序号 $n$")
    ax[1, 1].set_ylabel("衰减率")
    ax[1, 1].set_title("D  no-go 保持：率依 n 变，恒等焊接不可能")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
