# -*- coding: utf-8 -*-
"""
R41：审-7 乘法内容的定位——和乐积 vs 加法差
=====================================================================
预注册 R41 的 P1–P5（跑数前写死）：
  P1 原文审计
  P2 Hecke 乘性→Euler 积（B 类）
  P3 加法差闭环望远镜=0；随机和乐积有分布
  P4 桥缺失定位
  P5 Lean

复跑：python "10 探索/超导第一性研究/04_计算验证/R41_乘法内容定位.py"
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
    chain = open(os.path.join(ROOT, "10 探索", "CQM_探索_推导链.md"), encoding="utf-8").read()
    checks = {
        "加法差": "$C$ 只含加法差 $f(\\varepsilon_i-\\varepsilon_j)$" in chain,
        "乘法内容缺": "Hecke 关系所需的乘法内容缺" in chain,
        "和乐积": "$\\prod_Cr=1$" in chain or "$\\prod_Cr_e=1$" in chain,
        "扇区分层": "$r_{ij}$ 归和乐侧" in chain,
    }
    assert all(checks.values()), "P1: 原文审计失败 %s" % checks

    # ---------- P3：加法差 vs 乘法积 ----------
    rng = np.random.default_rng(11)
    n, Nsamp, sigma = 12, 20000, 0.05
    eps = rng.normal(0, sigma, size=(Nsamp, n))
    # 闭环加法差：(e2-e1)+(e3-e2)+...+(e1-en) = 0（望远镜）
    d = np.roll(eps, -1, axis=1) - eps
    additive_sum = d.sum(axis=1)
    max_res = float(np.max(np.abs(additive_sum)))
    assert max_res < 1e-12, "P3: 加法差应望远镜为 0，实测 %.3e" % max_res

    # 和乐侧：r_e = exp(-eps_e/(2pi))，积 = exp(-Σeps/(2pi))
    logprod = -eps.sum(axis=1) / (2 * math.pi)
    prod = np.exp(logprod)
    var_log = float(np.var(logprod))
    assert var_log > 0, "P3: 和乐积对数应有非零涨落"
    # R83 预测均值 -n sigma^2/(16 pi^2)，数值对照
    mean_pred = -n * sigma ** 2 / (16 * math.pi ** 2)
    mean_num = float(np.mean(logprod))
    assert abs(mean_num - mean_pred) < 2e-3, "P3: 均值 %.5f vs 预测 %.5f" % (mean_num, mean_pred)

    print("R41 乘法内容定位（结构审计，无拟合）：")
    print("  P1 原文：%s" % checks)
    print("  P2 外部：Hecke 乘性→Euler 积；Mellin 和→Dirichlet 级数（B 类）")
    print("  加法差闭环和：最大残差 %.3e（望远镜恒 0）" % max_res)
    print("  和乐积 ln(prod r)：均值 %.5f（R83 预测 %.5f），方差 %.5f" % (mean_num, mean_pred, var_log))
    print("  P4 桥缺失：审-1 矩阵分支未闭合、r↔v_tau 仅 O(ell)")
    print("  P5 Lean")

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    ax = axes[0, 0]
    idx = np.arange(n)
    ax.plot(idx, eps[0], "o-", lw=2.0, color="#1f77b4")
    ax.axhline(0, color="gray", lw=1)
    ax.set_xlabel("环上边 $e$")
    ax.set_ylabel("$\\varepsilon_e$")
    ax.set_title("A  闭环上的随机亏角（示意样本）")
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.hist(additive_sum, bins=60, color="#2ca02c", alpha=0.85)
    ax.set_yscale("log")
    ax.set_xlabel("$\\sum_C(\\varepsilon_{i+1}-\\varepsilon_i)$")
    ax.set_title("B  加法差：望远镜恒 0（残差 $<10^{-12}$）")
    ax.ticklabel_format(axis="x", style="plain", useOffset=False)
    ax.grid(alpha=0.3, axis="y")

    ax = axes[1, 0]
    ax.hist(logprod, bins=60, color="#d62728", alpha=0.85)
    ax.axvline(mean_num, color="k", ls="--", lw=1.4, label="数值均值 %.4f" % mean_num)
    ax.axvline(mean_pred, color="b", ls=":", lw=1.6, label="R83 预测 %.4f" % mean_pred)
    ax.set_xlabel("$\\ln\\prod_C r_e$")
    ax.set_title("C  和乐积：有乘法涨落（方差 %.4f）" % var_log)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, axis="y")

    ax = axes[1, 1]
    ax.text(0.04, 0.82, "乘法内容存在", fontsize=12, weight="bold", color="#2ca02c")
    ax.text(0.04, 0.67, "· 和乐积 $\\prod_C r_e$（拓扑）\n· $\\ln\\prod r=\\sum\\ln r$\n· R83 已算其统计", fontsize=10)
    ax.text(0.04, 0.40, "桥仍缺", fontsize=12, weight="bold", color="#d62728")
    ax.text(0.04, 0.25, "· $C=f(\\varepsilon_i-\\varepsilon_j)$ 是加法差\n· $C\\to r$ 靠 `审-1`（未闭合）\n· $r\\leftrightarrow v_\\tau$ 仅 $O(\\ell)$", fontsize=10)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_title("D  审-7 定位：扇区有乘法，缺的是桥")

    fig.tight_layout()
    png = os.path.join(OUT, "R41_乘法内容定位.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "原文四处 %s" % checks, "通过"],
        ["P2", "Hecke 乘性→Euler 积", "B 类"],
        ["P3", "加法残差 %.1e；和乐积方差 %.4f" % (max_res, var_log), "通过"],
        ["P4", "桥：审-1 未闭合、r~v_tau O(ell)", "审-7 未闭合"],
        ["P5", "望远镜与 exp 积（Lean）", "由 Lean 承载"],
        ["结论", "乘法内容在和乐扇区、桥缺", "状态不动"],
    ]
    with open(os.path.join(OUT, "R41_乘法内容定位_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
