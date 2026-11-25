# -*- coding: utf-8 -*-
"""
R33：临-5 高通道权重 1/k 的归一性审计
=====================================================================
预注册 R33 的 P1–P5（跑数前写死）：
  P1 原文审计 12.A1/A2/A3/L483
  P2 外部调和级数发散 H_K ~ ln K + gamma
  P3 H_K 增、w1=1/H_K 减，K=1e6 时 w1<0.1
  P4 无限极限与"第一档主导"矛盾 ⇒ 截断外生
  P5 Lean 承载

复跑：python "10 探索/超导第一性研究/04_计算验证/R33_临5权重归一性.py"
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
GAMMA = 0.5772156649015329


def main():
    # ---------- P1：原文审计 ----------
    chain = open(os.path.join(ROOT, "10 探索", "CQM_探索_推导链.md"), encoding="utf-8").read()
    checks = {
        "无限集": "2\\mathbb Z_{\\ge1}" in chain,
        "局域填档": "J_{ij}\\ge J_{\\rm cr}" in chain,
        "1/k阶梯": "\\frac{2}{n}=\\frac1k" in chain,
        "第一档主导": "第一档主导" in chain,
    }
    assert all(checks.values()), "P1: 原文审计失败 %s" % checks

    # ---------- P2/P3：调和归一 ----------
    Ks = np.array([2, 3, 4, 5, 10, 20, 50, 100, 1000, 10**4, 10**5, 10**6])
    HK = np.array([sum(1.0 / k for k in range(1, int(K) + 1)) for K in Ks])
    w1 = 1.0 / HK
    assert np.all(np.diff(HK) > 0), "P3: H_K 应严格增"
    assert np.all(np.diff(w1) < 0), "P3: w1 应严格减"
    assert w1[-1] < 0.1, "P3: K=1e6 时 w1=%.4f 应 <0.1" % w1[-1]

    # 与 ln K + gamma 对照
    large = Ks >= 10
    approx = np.log(Ks[large].astype(float)) + GAMMA
    rel = float(np.max(np.abs(HK[large] - approx) / HK[large]))
    assert rel < 0.02, "P2: 渐近对照偏差 %.3f" % rel

    # ---------- P4：矛盾登记 ----------
    # 无限极限 w1 -> 0 与 L483 "第一档主导" 不相容；截断 K 必须外生。
    assert HK[-1] > 10 and w1[-1] < 0.1, "P4: 极限行为确认"
    # 示意：若要求 w1>=0.5（主导），需 H_K<=2，即 K<=3
    K_dominant = [int(K) for K, w in zip(Ks, w1) if w >= 0.5]
    assert K_dominant and max(K_dominant) <= 4, "P4: 主导需小 K"

    print("R33 临-5 权重归一性（结构 no-go，无拟合）：")
    print("  P1 原文：%s" % checks)
    print("  P2 外部：H_K = ln K + gamma + O(1/K)，发散（arXiv:0706.2513）")
    print("  P3 归一：H_K 增、w1=1/H_K 减；K=1e6 时 w1=%.4f（渐近相对偏差 %.2e）" % (w1[-1], rel))
    print("  P4 主导要求 w1>=0.5 ⇒ K<=%d；无限模式集(12.A1)与'第一档主导'不相容" % max(K_dominant))
    print("      12.A2 只给局域条件，无 J_cr/涨落分布 ⇒ 截断外生")
    print("  P5 Lean 承载")

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    ax = axes[0, 0]
    Ksmooth = np.arange(2, 1001)
    Hsmooth = np.array([sum(1.0 / k for k in range(1, int(K) + 1)) for K in Ksmooth])
    ax.plot(Ksmooth, Hsmooth, "b-", lw=2.2, label="$H_K=\\sum_{k=1}^K1/k$")
    ax.plot(Ksmooth, np.log(Ksmooth.astype(float)) + GAMMA, "r--", lw=2.0,
            label="$\\ln K+\\gamma$")
    ax.set_xlabel("通道截断 $K$")
    ax.set_ylabel("$H_K$")
    ax.set_title("A  调和归一因子发散（$H_K\\sim\\ln K$）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.semilogx(Ks, w1, "o-", lw=2.2, ms=6, color="#d62728")
    ax.axhline(0.5, color="gray", ls="--", lw=1.2, label="主导阈值 $w_1>0.5$")
    ax.set_xlabel("通道截断 $K$")
    ax.set_ylabel("$w_1=1/H_K$")
    ax.set_title("B  第一档权重随 $K$ 增而趋 0")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")

    ax = axes[1, 0]
    Ksmall = np.arange(1, 16)
    wsmall = np.array([1.0 / sum(1.0 / k for k in range(1, int(K) + 1)) for K in Ksmall])
    ax.bar(Ksmall, wsmall, color=["#2ca02c" if w >= 0.5 else "#d62728" for w in wsmall], alpha=0.85)
    ax.axhline(0.5, color="gray", ls="--", lw=1.2)
    ax.set_xlabel("通道数 $K$")
    ax.set_ylabel("$w_1$")
    ax.set_title("C  \"第一档主导\"只在 $K<4$ 成立")
    ax.grid(alpha=0.3, axis="y")

    ax = axes[1, 1]
    ax.loglog(Ks, w1, "o-", lw=2.2, ms=6, label="归一后 $w_1=1/H_K$")
    ax.loglog(Ks, 1.0 / Ks, "k--", lw=1.8, label="未归一 $1/k$ 梯度")
    ax.set_xlabel("$K$")
    ax.set_ylabel("权重")
    ax.set_title("D  无限集 12.A1 需外生截断 $K$（`临-5` 未闭合）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")

    fig.tight_layout()
    png = os.path.join(OUT, "R33_临5权重归一性.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "原文四处 %s" % checks, "通过"],
        ["P2", "H_K~ln K+gamma，发散", "外部标准（B 类）"],
        ["P3", "w1(1e6)=%.4f，单调减" % w1[-1], "通过"],
        ["P4", "主导需 K<=%d；截断外生" % max(K_dominant), "no-go"],
        ["P5", "调和递归与单调（Lean）", "由 Lean 承载"],
        ["结论", "临-5 归一性不能由 12.A3 单独闭合", "状态不动"],
    ]
    with open(os.path.join(OUT, "R33_临5权重归一性_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
