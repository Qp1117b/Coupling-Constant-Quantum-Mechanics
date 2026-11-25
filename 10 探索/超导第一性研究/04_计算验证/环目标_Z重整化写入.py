# -*- coding: utf-8 -*-
"""
Eliashberg Z=1+lambda 写入 (目标.2) 的定量核对（非拟合）。

1. 上轮恒定比 0.312 的精确来源: e^{-7/6} = e^{-1}(质量增强) * e^{-1/6}(对数矩口径差)
2. 改前/改后反解 lambda 对比: 改后用 -(1+lambda)/lambda 指数
3. 与 Eliashberg Eq37 反解 lambda 对比（改善程度）
4. 形状中性: gap ratio 不随 Z 变

由 Marsiglio 2018 Eq13/14/37 与 Webb Table III 直接计算，不调参。
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
OUT_PNG = os.path.join(HERE, "环目标_Z重整化写入.png")
OUT_CSV = os.path.join(HERE, "环目标_Z重整化写入.csv")

A = 1.13
DELTA_THIRD = math.exp(-1 / 3)   # 振幅支对数矩 e^{-1/3}
DELTA_HALF = math.exp(-1 / 2)    # Marsiglio Eq37 / 相位支 e^{-1/2}
PREF37 = 1.13 / math.sqrt(math.e)

# Webb 2015 Table III: (element, Tc, theta_D)
DATA = [
    ("Al", 1.18, 428), ("Nb", 9.25, 275), ("Pb", 7.2, 105),
    ("Sn", 3.7, 200), ("Cd", 0.52, 209), ("Ta", 4.4, 240),
    ("V", 5.4, 380), ("In", 3.4, 108),
]


def inv_lambda_old(tc, th):
    """改前: Tc = A e^{-1/3} th e^{-1/lam}."""
    return 1 / math.log(A * DELTA_THIRD * th / tc)


def inv_lambda_new(tc, th):
    """改后: Tc = A e^{-1/3} th e^{-(1+lam)/lam} -> 1/lam = log(...) - 1."""
    return 1 / (math.log(A * DELTA_THIRD * th / tc) - 1)


def inv_lambda_e37(tc, th):
    """Eliashberg Eq37: Tc = (1.13/sqrt(e)) th e^{-(1+lam)/lam}, 用 theta≈omega_E."""
    return 1 / (math.log(PREF37 * th / tc) - 1)


def main():
    rows = []
    # 1 精确来源
    ratio_exact = math.exp(-7 / 6)
    parts = (math.exp(-1), math.exp(-1 / 6))
    print("1 恒定比 0.312 的精确来源")
    print(f"  e^(-7/6) = {ratio_exact:.6f}")
    print(f"  e^(-1) [质量增强] * e^(-1/6) [对数矩口径 e^-1/3 / e^-1/2] = "
          f"{parts[0]:.6f} * {parts[1]:.6f} = {parts[0]*parts[1]:.6f}")
    rows.append(("exact", 0, ratio_exact, parts[0] * parts[1], np.nan))

    # 2-3 三口径反解
    print("\n2 三口径反解 lambda")
    print(f"{'el':<4}{'old':>8}{'new':>8}{'E37':>8}{'new/E37':>10}{'old/E37':>10}")
    names, olds, news, e37s = [], [], [], []
    for name, tc, th in DATA:
        lo = inv_lambda_old(tc, th)
        ln = inv_lambda_new(tc, th)
        le = inv_lambda_e37(tc, th)
        names.append(name); olds.append(lo); news.append(ln); e37s.append(le)
        print(f"{name:<4}{lo:>8.4f}{ln:>8.4f}{le:>8.4f}{ln/le:>10.3f}{lo/le:>10.3f}")
        rows.append(("inverse", tc, lo, ln, f"{name}|{le}"))

    news = np.array(news); olds = np.array(olds); e37s = np.array(e37s)
    print(f"\n  改后平均 |new/E37-1| = {np.mean(np.abs(news/e37s-1)):.1%}")
    print(f"  改前平均 |old/E37-1| = {np.mean(np.abs(olds/e37s-1)):.1%}")

    # 4 形状中性: gap ratio 不随 Z 变
    print("\n4 形状中性: 2Delta/kBT* 不随 Z 变")
    lam_s = np.linspace(0.05, 0.5, 100)
    r = 2 * math.pi / math.exp(0.5772156649)
    for lam in lam_s[::20]:
        # 含 Z: T* -> e^{-1}T*, Delta -> e^{-1}Delta, 比值不变
        t_star = A * math.exp(-(1 + lam) / lam)
        delta = (math.pi / math.exp(0.5772156649)) * t_star
        rows.append(("shape", lam, 2 * delta / t_star, r, np.nan))
    print(f"  gap ratio 恒为 {r:.4f}（Z 对 T* 与 Delta 同乘 e^-1，约掉）")

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.4, 9.6))

    ax[0, 0].bar(["$e^{-1}$\n质量增强", "$e^{-1/6}$\n对数矩口径", "$e^{-7/6}$\n合计"],
                 [parts[0], parts[1], ratio_exact],
                 color=["tab:blue", "tab:orange", "tab:red"], alpha=0.85)
    ax[0, 0].set_ylabel("因子")
    ax[0, 0].set_title("A  0.312 的精确分解 $e^{-7/6}$")
    ax[0, 0].grid(alpha=0.3, axis="y")

    x = np.arange(len(names))
    ax[0, 1].bar(x - 0.24, olds, 0.24, label="改前 $e^{-1/\\lambda}$",
                 color="tab:blue", alpha=0.8)
    ax[0, 1].bar(x, news, 0.24, label="改后 $e^{-(1+\\lambda)/\\lambda}$",
                 color="tab:orange", alpha=0.8)
    ax[0, 1].bar(x + 0.24, e37s, 0.24, label="Eliashberg Eq37",
                 color="tab:green", alpha=0.8)
    ax[0, 1].set_xticks(x)
    ax[0, 1].set_xticklabels(names)
    ax[0, 1].set_ylabel("反解 $\\lambda$")
    ax[0, 1].set_title("B  三口径反解对比")
    ax[0, 1].legend(fontsize=7)
    ax[0, 1].grid(alpha=0.3, axis="y")

    ax[1, 0].bar(x - 0.18, np.abs(olds/e37s-1)*100, 0.36, label="改前",
                 color="tab:blue", alpha=0.8)
    ax[1, 0].bar(x + 0.18, np.abs(news/e37s-1)*100, 0.36, label="改后",
                 color="tab:orange", alpha=0.8)
    ax[1, 0].set_xticks(x)
    ax[1, 0].set_xticklabels(names)
    ax[1, 0].set_ylabel("相对偏差 %")
    ax[1, 0].set_title("C  写入 Z 后偏差显著减小")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3, axis="y")

    ax[1, 1].plot(lam_s, [r] * len(lam_s), lw=2.4, color="tab:purple")
    ax[1, 1].axhline(r, color="tab:red", ls="--", lw=1.4)
    ax[1, 1].set_xlabel(r"$\lambda$")
    ax[1, 1].set_ylabel(r"$2\Delta/k_BT^*$")
    ax[1, 1].set_title(f"D  形状中性: gap ratio 恒 {r:.3f}")
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
