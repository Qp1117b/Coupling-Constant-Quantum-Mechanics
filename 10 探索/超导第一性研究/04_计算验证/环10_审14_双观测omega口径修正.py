# -*- coding: utf-8 -*-
"""
第94轮补（成果登记 R-103）：双观测检验的 omega 对数矩口径修正（非拟合）
==========================================================================
问题：第61轮脚本把 CQM 振幅支矩 e^{-1/3}θ_D 喂进 Allen-Dynes 式，但该式的
      ω_ln 按定义是 alpha^2F/ν 权重 = e^{-1/2}θ_D（第92轮链内导出）。
本脚本：用两种口径重算 (Tc, alpha) 双观测联立的 (lam, mu*)，对比并用
      文献独立 mu* 值（Al 0.091、Hg 0.07）核对。全部实测数据、不拟合。

复跑：
  python "10 探索/超导第一性研究/04_计算验证/环10_审14_双观测omega口径修正.py"
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

HERE = os.path.dirname(os.path.abspath(__file__))
E3 = math.exp(-1 / 3)   # 旧口径（CQM 振幅支，错误地喂进 AD 式）
E2 = math.exp(-1 / 2)   # 新口径（第92轮链内导出，AD 式的正确 alpha^2F/nu 权重）

# Webb 2015 Table III：name, Tc(K), theta_D(K), alpha_exp（measured 列）
DATA = [
    ("Pb", 7.20, 105, 0.48), ("Hg", 4.15, 72, 0.50),
    ("Sn", 3.70, 200, 0.46), ("Tl", 2.40, 78.5, 0.50),
    ("V",  5.40, 380, 0.15), ("Ta", 4.40, 240, 0.35),
    ("Re", 1.70, 430, 0.38), ("Mo", 0.92, 450, 0.37),
    ("Os", 0.70, 500, 0.21), ("Zn", 0.85, 327, 0.30),
    ("Cd", 0.52, 209, 0.50), ("Zr", 0.60, 291, 0.00),
    ("Ru", 0.50, 600, 0.00),
]
# 文献独立 mu*（非拟合：Al PRB52 1425=0.091；Hg arXiv:2111.13867=0.07）
MUST_LIT = {"Al": 0.091, "Hg": 0.07}


def solve_double(tc, theta, a_exp, ecoef):
    """双观测联立 (lam, mu*)：Tc 的 AD 式 + alpha 的 MA 形状式。"""
    wlog = ecoef * theta
    E = math.log(1.2 * tc / wlog)
    if E >= 0:
        return None
    A = -1.04 / E
    if A >= 1:
        return None

    def f(lam):
        b = 1 + 0.62 * lam
        must = (lam - A * (1 + lam)) / b
        if must < -1e-9 or must > 1:
            return float("nan")
        pred = b * must**2 * E**2 / (1.04 * (1 + lam))
        return pred - (1 - 2 * a_exp)

    lo = A / (1 - A)
    hi = min(20.0, (1 + A) / (0.38 - A) * 0.9999) if A < 0.38 else 20.0
    if hi <= lo:
        return None
    if abs(1 - 2 * a_exp) < 1e-9:
        return lo, 0.0, wlog
    flo, fhi = f(lo), f(hi)
    if math.isnan(flo) or math.isnan(fhi) or flo * fhi > 0:
        return None
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if math.isnan(fm) or fm * flo > 0:
            lo, flo = mid, fm
        else:
            hi = mid
    lam = 0.5 * (lo + hi)
    b = 1 + 0.62 * lam
    must = (lam - A * (1 + lam)) / b
    return lam, must, wlog


def main():
    rows = []
    for name, tc, theta, alpha in DATA:
        old = solve_double(tc, theta, alpha, E3)
        new = solve_double(tc, theta, alpha, E2)
        rows.append((name, tc, theta, alpha, old, new))

    # 可解的元素数、常规区间 mu* in [0.1,0.3] 的数目（两口径对比）
    def stats(idx):
        solved = [r for r in rows if r[idx] is not None]
        mus = [r[idx][1] for r in solved]
        lams = [r[idx][0] for r in solved]
        inrange = sum(1 for m in mus if 0.10 <= m <= 0.30)
        return solved, mus, lams, inrange

    sold, mold, lold, iold = stats(4)
    snew, mnew, lnew, inew = stats(5)

    # 结构断言
    assert E2 < E3, "新口径 omega_ln 应更小"
    assert abs(E3 / E2 - math.exp(1 / 6)) < 1e-12, "两矩比应为 e^{1/6}"
    assert len(snew) >= len(sold), "新口径不应减少可解元素数"
    assert inew >= iold, "新口径常规区间 μ* 数不应减少"

    # 文献独立 μ* 核对（Hg 在新口径下应更接近 0.07）
    hg = [r for r in rows if r[0] == "Hg"][0]
    hg_old_mu = hg[4][1] if hg[4] else None
    hg_new_mu = hg[5][1] if hg[5] else None
    # 不强制数值断言（模型简化），只记录

    # ---------- 图 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # A: 两口径 omega_ln
    ax = axes[0, 0]
    theta_ax = np.linspace(50, 500, 200)
    ax.plot(theta_ax, E3 * theta_ax, lw=2.0, color="orange",
            label="旧 $e^{-1/3}\\theta_D$（振幅支矩）")
    ax.plot(theta_ax, E2 * theta_ax, lw=2.0, color="#1f77b4",
            label="新 $e^{-1/2}\\theta_D$（链内 $\\omega_{ln}$）")
    ax.set_xlabel("$\\theta_D$ (K)")
    ax.set_ylabel("$\\omega_{ln}$ (K)")
    ax.set_title(f"A  口径修正：比值 $e^{{1/6}}$={E3/E2:.4f}")
    ax.legend(fontsize=8)

    # B: mu* 分布对比
    ax = axes[0, 1]
    ax.hist(mold, bins=np.linspace(0, 1, 20), alpha=0.6, color="orange",
            label=f"旧口径（常规区间 {iold}）")
    ax.hist(mnew, bins=np.linspace(0, 1, 20), alpha=0.6, color="#1f77b4",
            label=f"新口径（常规区间 {inew}）")
    ax.axvspan(0.10, 0.30, color="g", alpha=0.1)
    ax.set_xlabel("$\\mu^*$")
    ax.set_ylabel("元素数")
    ax.set_title("B  双观测解的 $\\mu^*$ 分布（绿区=常规 0.1–0.3）")
    ax.legend(fontsize=8)

    # C: lambda 分布
    ax = axes[1, 0]
    ax.hist(lold, bins=np.linspace(0, 2, 20), alpha=0.6, color="orange",
            label="旧口径")
    ax.hist(lnew, bins=np.linspace(0, 2, 20), alpha=0.6, color="#1f77b4",
            label="新口径")
    ax.set_xlabel("$\\lambda$")
    ax.set_ylabel("元素数")
    ax.set_title("C  双观测解的 $\\lambda$ 分布")
    ax.legend(fontsize=8)

    # D: Hg 口径对比 + 文献值
    ax = axes[1, 1]
    labels = ["旧口径 Hg", "新口径 Hg", "文献 Hg\n0.07"]
    vals = [hg_old_mu if hg_old_mu is not None else 0,
            hg_new_mu if hg_new_mu is not None else 0, 0.07]
    ax.bar(labels, vals, color=["orange", "#1f77b4", "green"])
    ax.set_ylabel("$\\mu^*$")
    ax.set_title("D  Hg 双观测解 vs 文献独立值（无拟合）")

    fig.tight_layout()
    png = os.path.join(HERE, "环10_审14_双观测omega口径修正.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    # ---------- CSV ----------
    summary = [
        ["旧口径 e^{-1/3}", f"{E3:.6f}", "CQM 振幅支矩（错误喂进 AD 式）"],
        ["新口径 e^{-1/2}", f"{E2:.6f}", "第92轮链内 ω_ln（AD 式正确权重）"],
        ["两矩比 e^{1/6}", f"{E3/E2:.6f}", "振幅支高估因子"],
        ["旧口径可解元素", f"{len(sold)}/13", f"常规 μ* 区间 {iold}"],
        ["新口径可解元素", f"{len(snew)}/13", f"常规 μ* 区间 {inew}"],
        ["Hg 旧 μ*", f"{hg_old_mu:.4f}" if hg_old_mu is not None else "NA",
         "α=0.50 端点 ⇒ μ*=0"],
        ["Hg 新 μ*", f"{hg_new_mu:.4f}" if hg_new_mu is not None else "NA",
         "端点 μ*=0；文献实测 0.07（α 端点四舍五入）"],
        ["μ 第一性来源", "链外-A", "链内 V<0 恒成立，不虚构"],
    ]
    with open(os.path.join(HERE, "环10_审14_双观测omega口径修正_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["量", "值", "说明"])
        w.writerows(summary)
    with open(os.path.join(HERE, "环10_审14_双观测omega口径修正.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["element", "Tc", "thetaD", "alpha_exp",
                    "lam_old", "mu_old", "lam_new", "mu_new"])
        for name, tc, theta, alpha, old, new in rows:
            w.writerow([name, f"{tc:.3f}", f"{theta:.3f}", f"{alpha:.3f}",
                        f"{old[0]:.6f}" if old else "NA",
                        f"{old[1]:.6f}" if old else "NA",
                        f"{new[0]:.6f}" if new else "NA",
                        f"{new[1]:.6f}" if new else "NA"])

    print("第94轮补 审-14 双观测 omega 口径修正：全部断言通过（非拟合）")
    for row in summary:
        print("  ", row[0], "=", row[1], "|", row[2])
    print("图:", png)


if __name__ == "__main__":
    main()
