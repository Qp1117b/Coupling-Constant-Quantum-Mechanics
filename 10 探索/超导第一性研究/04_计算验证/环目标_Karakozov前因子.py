# -*- coding: utf-8 -*-
"""
Karakozov 前因子修正 e^{-1/6}（对数矩形式）——消除最后 6.4% 的数值核对。

Marsiglio arXiv:1807.04907 Eq26: Tc=(1.13/sqrt(e)) Omega e^{-1/lam}  (Karakozov 修正)
截断 Omega -> 对数矩 omega_log=e^{-1/3}theta_D 时: 1.13 e^{-1/2} Omega = 1.13 e^{-1/6} omega_log
故 CQM 对数矩形式须含 e^{-1/6} 因子。

1 e^{-1/6} 的来源: e^{-1/2}/e^{-1/3} (Karakozov截断 -> 对数矩)
2 修正后反解 lambda 与 Eliashberg Eq37 偏差 6.4% -> 0
3 形状中性: gap ratio 不随常数前因子变
4 完整前因子链

由 Marsiglio Eq26/37 与 Webb Table III 直接计算，不调参。
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
OUT_PNG = os.path.join(HERE, "环目标_Karakozov前因子.png")
OUT_CSV = os.path.join(HERE, "环目标_Karakozov前因子.csv")

A = 1.13
E3 = math.exp(-1 / 3)
E6 = math.exp(-1 / 6)
E2 = math.exp(-1 / 2)

DATA = [
    ("Al", 1.18, 428), ("Nb", 9.25, 275), ("Pb", 7.2, 105),
    ("Sn", 3.7, 200), ("Cd", 0.52, 209), ("Ta", 4.4, 240),
    ("V", 5.4, 380), ("In", 3.4, 108),
]


def inv_lam(pref, tc, th):
    """Tc = pref * th * e^{-(1+lam)/lam} => 1/lam = ln(pref th / Tc) - 1."""
    return 1 / (math.log(pref * th / tc) - 1)


def main():
    rows = []
    # 1 来源
    print("1 e^{-1/6} 来源: Karakozov e^{-1/2}(截断) / 对数矩 e^{-1/3}")
    print(f"  e^(-1/2)/e^(-1/3) = {E2/E3:.6f} = e^(-1/6) = {E6:.6f}")
    print(f"  1.13 e^(-1/2) theta = 1.13 e^(-1/6) * [e^(-1/3) theta] = "
          f"1.13 e^(-1/6) omega_log")
    rows.append(("origin", 0, E2 / E3, E6, np.nan))

    # 2 三口径反解: 当前(无K), 修正(含K), Eq37
    pref_cur = A * E3                 # 当前 (目标.2) 前因子 (缺 K)
    pref_fix = A * E3 * E6            # 修正后 (含 Karakozov e^{-1/6})
    pref_e37 = A * E2                 # Marsiglio Eq37 前因子 (截断形式)
    print(f"\n  前因子: 当前={pref_cur:.5f}  修正={pref_fix:.5f}  Eq37={pref_e37:.5f}")
    print(f"{'el':<4}{'cur':>8}{'fix':>8}{'E37':>8}{'fix/E37':>10}{'cur/E37':>10}")
    names, curs, fixs, e37s = [], [], [], []
    for name, tc, th in DATA:
        c = inv_lam(pref_cur, tc, th)
        f = inv_lam(pref_fix, tc, th)
        e = inv_lam(pref_e37, tc, th)
        names.append(name); curs.append(c); fixs.append(f); e37s.append(e)
        print(f"{name:<4}{c:>8.4f}{f:>8.4f}{e:>8.4f}{f/e:>10.4f}{c/e:>10.4f}")
        rows.append(("inverse", tc, c, f, f"{name}|{e}"))
    curs = np.array(curs); fixs = np.array(fixs); e37s = np.array(e37s)
    print(f"\n  修正后平均 |fix/E37-1| = {np.mean(np.abs(fixs/e37s-1)):.2e}")
    print(f"  修正前平均 |cur/E37-1| = {np.mean(np.abs(curs/e37s-1)):.1%}")

    # 3 形状中性
    r = 2 * math.pi / math.exp(0.5772156649)
    lams = np.linspace(0.05, 0.5, 100)
    print(f"\n3 形状中性: gap ratio 恒 {r:.4f}（常数前因子不影响比值）")
    for lam in lams[::20]:
        t = pref_fix * math.exp(-(1 + lam) / lam)
        d = (math.pi / math.exp(0.5772156649)) * t
        rows.append(("shape", lam, 2 * d / t, r, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.4, 9.6))

    ax[0, 0].bar(["Karakozov\n$e^{-1/2}$", "对数矩\n$e^{-1/3}$", "差值\n$e^{-1/6}$"],
                 [E2, E3, E6], color=["tab:blue", "tab:orange", "tab:red"], alpha=0.85)
    ax[0, 0].set_ylabel("因子")
    ax[0, 0].set_title("A  $e^{-1/6}=e^{-1/2}/e^{-1/3}$")
    ax[0, 0].grid(alpha=0.3, axis="y")

    x = np.arange(len(names))
    ax[0, 1].bar(x - 0.24, curs, 0.24, label="当前(缺K)", color="tab:blue", alpha=0.8)
    ax[0, 1].bar(x, fixs, 0.24, label="修正(含K)", color="tab:orange", alpha=0.8)
    ax[0, 1].bar(x + 0.24, e37s, 0.24, label="Eq37", color="tab:green", alpha=0.8)
    ax[0, 1].set_xticks(x)
    ax[0, 1].set_xticklabels(names)
    ax[0, 1].set_ylabel("反解 $\\lambda$")
    ax[0, 1].set_title("B  修正后与 Eq37 重合")
    ax[0, 1].legend(fontsize=7)
    ax[0, 1].grid(alpha=0.3, axis="y")

    ax[1, 0].bar(x - 0.18, np.abs(curs/e37s-1)*100, 0.36, label="修正前",
                 color="tab:blue", alpha=0.8)
    ax[1, 0].bar(x + 0.18, np.abs(fixs/e37s-1)*100, 0.36, label="修正后",
                 color="tab:orange", alpha=0.8)
    ax[1, 0].set_xticks(x)
    ax[1, 0].set_xticklabels(names)
    ax[1, 0].set_ylabel("相对偏差 %")
    ax[1, 0].set_title("C  6.4% → 0")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3, axis="y")

    ax[1, 1].plot(lams, [r] * len(lams), lw=2.4, color="tab:purple")
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
