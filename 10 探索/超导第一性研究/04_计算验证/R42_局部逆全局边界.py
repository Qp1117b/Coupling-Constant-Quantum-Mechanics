# -*- coding: utf-8 -*-
"""
R42：审-1 局部反函数的全局边界——阈值与亏角域
=====================================================================
预注册 R42 的 P1–P5（跑数前写死）：
  P1 工作台原文审计
  P2 Hadamard 全局反函数（B 类）
  P3 lambda*=sqrt(c/3|d|)，epsilon*=2pi(1-exp(-2lambda*))
  P4 局部够判据、全局不成立
  P5 Lean 阈值代数

复跑：python "10 探索/超导第一性研究/04_计算验证/R42_局部逆全局边界.py"
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

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(OUT, "..", "..", ".."))


def main():
    # ---------- P1 ----------
    card = open(os.path.join(ROOT, "10 探索", "超导第一性研究", "03_推导工作台",
                             "环08_审1_矩阵分支的Hessian重证与f逆的锚邻域闭合.md"),
                encoding="utf-8").read()
    checks = {
        "局部逆": "锚邻域" in card and "f^{-1}" in card,
        "阈值": "$\\sqrt{c/(3|d|)}$" in card or "\\sqrt{c/(3|d|)}" in card,
        "不声称全局": "不声称" in card and "全局可逆" in card,
        "8A4": "8A.4" in card,
    }
    assert all(checks.values()), "P1: 工作台审计失败 %s" % checks

    # ---------- P3 ----------
    c, d = 1.0, 10.0
    lam_star = math.sqrt(c / (3 * d))
    eps_star = 2 * math.pi * (1 - math.exp(-2 * lam_star))
    sigma = 0.1
    lam_typ = sigma / (4 * math.pi)     # lambda ≈ -eps/(4pi)
    assert abs(lam_star - 0.182574) < 1e-5, "P3: lambda*=%.6f" % lam_star
    assert 1.8 < eps_star < 2.1, "P3: eps*=%.4f" % eps_star
    assert lam_typ < lam_star / 10, "P3: 典型涨落应远小于阈值"

    # 导数变号验证
    lams = np.linspace(-0.4, 0.4, 800)
    fp = -c + 3 * d * lams ** 2
    assert fp[400] < 0 and fp[0] > 0 and fp[-1] > 0, "P3: f' 应在阈值外变号"

    print("R42 局部逆的全局边界（结构定量，无拟合）：")
    print("  P1 工作台：%s" % checks)
    print("  P2 外部：Hadamard 全局反函数要求导数处处非零（B 类）")
    print("  P3 lambda*=sqrt(c/3|d|)=%.6f rad（c=1,|d|=10）" % lam_star)
    print("     epsilon*=2pi(1-exp(-2lambda*))=%.4f rad（ %.1f%% of 2pi ）" % (eps_star, 100*eps_star/(2*math.pi)))
    print("     sigma_eps=0.1 -> |lambda|~%.5f << lambda*" % lam_typ)
    print("  P4 判据层局部逆足够；全局可逆在上述域外不成立")
    print("  P5 Lean 阈值代数")

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    ax = axes[0, 0]
    ax.plot(lams, -c * lams + d * lams ** 3, "b-", lw=2.2, label="$f(\\lambda)=-\\lambda+10\\lambda^3$")
    ax.axvline(lam_star, color="r", ls="--", lw=1.4, label="$\\lambda_*=%.3f$" % lam_star)
    ax.set_xlabel("$\\lambda$")
    ax.set_ylabel("$f(\\lambda)$")
    ax.set_title("A  三次近似下的逆函数多值起点")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.plot(lams, fp, "k-", lw=2.2, label="$f'=-1+30\\lambda^2$")
    ax.axhline(0, color="gray", lw=1)
    ax.axvline(-lam_star, color="r", ls="--", lw=1.2)
    ax.axvline(lam_star, color="r", ls="--", lw=1.2)
    ax.set_xlabel("$\\lambda$")
    ax.set_ylabel("$f'(\\lambda)$")
    ax.set_title("B  阈值外导数变号（全局单射失效）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    eps = np.linspace(0, 2 * math.pi, 500)
    lam_of_eps = np.log(np.sqrt(np.clip(1 - eps / (2 * math.pi), 1e-12, 1)))
    ax.plot(eps, lam_of_eps, "b-", lw=2.2)
    ax.axvline(eps_star, color="r", ls="--", lw=1.4, label="$\\varepsilon_*=%.2f$ rad" % eps_star)
    ax.axhline(-lam_star, color="r", ls=":", lw=1.2)
    ax.set_xlabel("$\\varepsilon$ (rad)")
    ax.set_ylabel("$\\lambda=\\ln\\sqrt{1-\\varepsilon/2\\pi}$")
    ax.set_title("C  亏角域中的可逆边界")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1, 1]
    ax.bar(["典型涨落", "阈值"], [lam_typ, lam_star], color=["#2ca02c", "#d62728"], alpha=0.85)
    ax.set_yscale("log")
    ax.set_ylabel("$|\\lambda|$ (rad)")
    ax.set_title("D  判据层在锚邻域内；大亏角域外需全局逆")
    ax.grid(alpha=0.3, axis="y")

    fig.tight_layout()
    png = os.path.join(OUT, "R42_局部逆全局边界.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "工作台四处 %s" % checks, "通过"],
        ["P2", "Hadamard 导数非零（B 类）", "外部标准"],
        ["P3", "lambda*=%.4f；eps*=%.2f rad" % (lam_star, eps_star), "通过"],
        ["P4", "局部够判据、全局不成立", "审-1 不闭合"],
        ["P5", "阈值代数（Lean）", "由 Lean 承载"],
        ["结论", "局部/全局边界定量化", "状态不动"],
    ]
    with open(os.path.join(OUT, "R42_局部逆全局边界_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
