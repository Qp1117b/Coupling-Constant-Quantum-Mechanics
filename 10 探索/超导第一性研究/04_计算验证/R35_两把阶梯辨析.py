# -*- coding: utf-8 -*-
"""
R35：两把阶梯的辨析——gamma_n 与 2 ln n
=====================================================================
预注册 R35 的 P1–P5（跑数前写死）：
  P1 原文审计 L616/L1280/L544/L1429
  P2 Riemann-von Mangoldt: gamma_n ~ 2 pi n / ln n
  P3 gamma_n/(2 ln n) 发散；间距量级不同
  P4 三把刻度互不相同
  P5 Lean

复跑：python "10 探索/超导第一性研究/04_计算验证/R35_两把阶梯辨析.py"
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
from scipy.optimize import brentq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(OUT, "..", "..", ".."))

ZEROS = [14.134725142, 21.022039639, 25.010857580, 30.424876126, 32.935061588,
         37.586178159, 40.918719012, 43.327073281, 48.005150881, 49.773832478]


def N_count(T):
    x = T / (2.0 * math.pi)
    return x * math.log(x) - x + 7.0 / 8.0


def gamma_of(n):
    if n <= len(ZEROS):
        return ZEROS[n - 1]
    return brentq(lambda T: N_count(T) - n, 1.0, 1e9, xtol=1e-8)


def primes_upto(N):
    sieve = np.ones(N + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(math.sqrt(N)) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    return np.nonzero(sieve)[0]


def main():
    # ---------- P1 ----------
    chain = open(os.path.join(ROOT, "10 探索", "CQM_探索_推导链.md"), encoding="utf-8").read()
    checks = {
        "两梯不可互译": "两梯不可互译" in chain,
        "gamma侧2ln": "2\\ln n$（$\\gamma_n$ 侧）" in chain,
        "两套刻度": "两套刻度，不能互相替换" in chain,
        "临26对齐未证": "阶梯的对齐未证" in chain,
    }
    assert all(checks.values()), "P1: 原文审计失败 %s" % checks

    # ---------- P2/P3 ----------
    ns = np.array([2, 3, 4, 5, 10, 20, 50, 100, 200, 500, 1000])
    gam = np.array([gamma_of(int(n)) for n in ns])
    ladder = 2.0 * np.log(ns.astype(float))
    ratio = gam / ladder
    assert ratio[0] < 20 and ratio[-1] > 100, "P3: 比值应发散 %.2f→%.2f" % (ratio[0], ratio[-1])

    # 大 n 用 Riemann–von Mangoldt 渐近间距 2π/ln n（外部标准，脚本内标注）
    nbig = np.unique(np.round(np.geomspace(2, 1e6, 200)).astype(int))
    dgamma = np.empty(len(nbig) - 1)
    for i in range(len(nbig) - 1):
        if nbig[i + 1] <= 1000:
            dgamma[i] = gamma_of(int(nbig[i + 1])) - gamma_of(int(nbig[i]))
        else:
            dgamma[i] = 2.0 * math.pi / math.log(nbig[i])
    dlog = 2.0 * np.log(1.0 + 1.0 / nbig[:-1].astype(float))
    primes = primes_upto(8000)
    dlogp = np.log(primes[1:50] / primes[:49])
    spacing_ratio = dgamma / dlog
    assert spacing_ratio[-1] / spacing_ratio[0] > 100, "P3: 间距比应跨 2 个量级"

    # ---------- P4 渐近三梯 ----------
    T = 1e6
    approx_gamma_spacing = 2 * math.pi / math.log(T)
    approx_log_spacing = 2.0 / T
    p_near = T * math.log(T)          # p_n ~ n ln n（PNT，示意同 n 比较）
    approx_logp_spacing = 1.0 / p_near
    assert approx_gamma_spacing > approx_log_spacing > approx_logp_spacing, "P4: 三间距应两两不同"

    print("R35 两把阶梯辨析（结构审计，无拟合）：")
    print("  P1 原文：%s" % checks)
    print("  P2/P3 gamma_n/(2ln n)：%.2f (n=1) → %.1f (n=1000)，发散" % (ratio[0], ratio[-1]))
    print("     间距 Delta_gamma / [2ln(1+1/n)]：%.1f → %.1f（跨 %.1f 个量级）"
          % (spacing_ratio[0], spacing_ratio[-1], math.log10(spacing_ratio[-1] / spacing_ratio[0])))
    print("  P4 渐近间距：gamma 侧 %.2e；2ln 侧 %.2e；log p 侧 %.2e（T=1e6 示意）"
          % (approx_gamma_spacing, approx_log_spacing, approx_logp_spacing))
    print("  P5 Lean 承载")

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    ax = axes[0, 0]
    ax.loglog(ns, gam, "o-", lw=2.2, ms=5, label="$\\gamma_n$（非平凡零点虚部）")
    ax.loglog(ns, ladder, "s--", lw=2.2, ms=5, label="$2\\ln n$（幅度阶梯）")
    ax.set_xlabel("$n$")
    ax.set_ylabel("数值")
    ax.set_title("A  两把梯子：走势不同")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")

    ax = axes[0, 1]
    ax.loglog(ns, ratio, "o-", lw=2.2, ms=5, color="#d62728")
    ax.set_xlabel("$n$")
    ax.set_ylabel("$\\gamma_n/(2\\ln n)$")
    ax.set_title("B  比值从 %.1f 增到 %.0f：不可能同一" % (ratio[0], ratio[-1]))
    ax.grid(alpha=0.3, which="both")

    ax = axes[1, 0]
    ax.loglog(nbig[:-1], dgamma, "b-", lw=2.0, label="$\\gamma_{n+1}-\\gamma_n\\sim2\\pi/\\ln n$")
    ax.loglog(nbig[:-1], dlog, "r--", lw=2.0, label="$2\\ln(1+1/n)\\sim2/n$")
    ax.loglog(primes[1:50], dlogp, "g:", lw=2.0, label="$\\ln p_{n+1}-\\ln p_n\\sim1/p$")
    ax.set_xlabel("$n$ 或 $p$")
    ax.set_ylabel("相邻间距")
    ax.set_title("C  三把刻度的渐近间距两两不同")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")

    ax = axes[1, 1]
    nfit = np.arange(2, 1001)
    asym = 2 * math.pi * nfit / np.log(nfit)
    actual = np.array([gamma_of(int(n)) for n in nfit])
    ax.loglog(nfit, actual, "b-", lw=2.2, label="$\\gamma_n$（RvM 反解）")
    ax.loglog(nfit, asym, "r--", lw=2.0, label="$2\\pi n/\\ln n$（渐近）")
    ax.set_xlabel("$n$")
    ax.set_ylabel("$\\gamma_n$")
    ax.set_title("D  Riemann–von Mangoldt 对得上 $\\gamma_n$，对不上 $2\\ln n$")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")

    fig.tight_layout()
    png = os.path.join(OUT, "R35_两把阶梯辨析.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "原文四处 %s" % checks, "通过"],
        ["P2", "γ_n ~ 2πn/ln n（RvM）", "外部标准（B 类）"],
        ["P3", "比值 %.1f→%.0f；间距跨 %.1f 量级" % (ratio[0], ratio[-1], math.log10(spacing_ratio[-1]/spacing_ratio[0])), "通过"],
        ["P4", "三渐近间距两两不同", "通过"],
        ["P5", "2ln 阶梯（Lean）", "由 Lean 承载"],
        ["结论", "L1280（γ_n 侧）为刻度混用", "临-26/临-22 状态不动"],
    ]
    with open(os.path.join(OUT, "R35_两把阶梯辨析_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
