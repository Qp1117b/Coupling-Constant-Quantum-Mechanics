# -*- coding: utf-8 -*-
"""
R36：用链内参与比 n_eff 给 1/k 权重截断——候选评估
=====================================================================
预注册 R36 的 P1–P5（跑数前写死）：
  P1 原文审计 临-21/12.A2/12.A3/R33
  P2 IPR 标准 n_eff in [1,N]
  P3 三类 p 分布给 n_eff；K=round(n_eff)；w1=1/H_K 随 n_eff 减
  P4 候选不闭合缺口
  P5 Lean

复跑：python "10 探索/超导第一性研究/04_计算验证/R36_参与比作截断.py"
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


def n_eff(p):
    return 1.0 / np.sum(p ** 2)


def H(K):
    return sum(1.0 / k for k in range(1, max(1, int(round(K))) + 1))


def main():
    # ---------- P1 ----------
    chain = open(os.path.join(ROOT, "10 探索", "CQM_探索_推导链.md"), encoding="utf-8").read()
    r33 = open(os.path.join(ROOT, "10 探索", "超导第一性研究", "06_决策记录",
                            "2026-11-24_第123轮_临5权重归一性.md"), encoding="utf-8").read()
    checks = {
        "临21参与比": "1/\\sum_i p_i^2" in chain,
        "12A2": "J_{ij}\\ge J_{\\rm cr}" in chain,
        "12A3": "\\frac{2}{n}=\\frac1k" in chain,
        "R33截断": "截断外生" in r33,
    }
    assert all(checks.values()), "P1: 原文审计失败 %s" % checks

    # ---------- P2/P3：三类分布 ----------
    N = 64
    p_uniform = np.ones(N) / N
    ell = 8.0
    p_loc = np.exp(-np.arange(N) / ell)
    p_loc /= p_loc.sum()
    rng = np.random.default_rng(7)
    p_rand = rng.dirichlet(np.ones(N) * 0.6)

    cases = {"均匀": p_uniform, "局域 ℓ=8": p_loc, "随机 Dirichlet": p_rand}
    results = {}
    for name, p in cases.items():
        ne = n_eff(p)
        assert 1.0 - 1e-12 <= ne <= N + 1e-12, "P2: n_eff 越界"
        K = max(1, int(round(ne)))
        results[name] = (ne, K, 1.0 / H(K))
    assert abs(results["均匀"][0] - N) < 1e-12, "P2: 等权应给 N"
    assert results["局域 ℓ=8"][0] < results["随机 Dirichlet"][0] < results["均匀"][0], "P3: n_eff 排序错"

    # n_eff 随局域长度 ℓ 增；w1 随 n_eff 减
    ells = np.geomspace(0.5, 128, 40)
    ne_list = []
    for e in ells:
        pe = np.exp(-np.arange(N) / e)
        pe /= pe.sum()
        ne_list.append(n_eff(pe))
    ne_list = np.array(ne_list)
    assert np.all(np.diff(ne_list) > 0), "P3: n_eff 应随 ℓ 增"
    w1_list = np.array([1.0 / H(ne) for ne in ne_list])
    assert np.all(np.diff(w1_list) <= 0), "P3: w1 应随 n_eff 减"

    print("R36 参与比作截断（候选评估，无拟合）：")
    print("  P1 原文：%s" % checks)
    print("  P2 IPR 标准：1<=n_eff<=N；均匀 %d、局域 %.2f、随机 %.2f"
          % (N, results["局域 ℓ=8"][0], results["随机 Dirichlet"][0]))
    print("  P3 K=round(n_eff)：%s" % {k: (round(v[0], 2), v[1], round(v[2], 4)) for k, v in results.items()})
    print("     方向：ℓ 增 → n_eff 增 → w1=1/H_K 减（与 L483 相容）")
    print("  P4 候选不闭合临-5/临-21；P5 Lean")

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    ax = axes[0, 0]
    x = np.arange(N)
    ax.plot(x, p_uniform, "b-", lw=2.0, label="均匀($n_{eff}=64$)")
    ax.plot(x, p_loc, "r-", lw=2.0, label="局域 ℓ=8($n_{eff}=%.1f$)" % results["局域 ℓ=8"][0])
    ax.plot(x, p_rand, "g:", lw=1.8, label="随机($n_{eff}=%.1f$)" % results["随机 Dirichlet"][0])
    ax.set_xlabel("格点 $i$")
    ax.set_ylabel("$p_i$")
    ax.set_title("A  三类参与分布（示意）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.semilogx(ells, ne_list, "o-", lw=2.2, ms=4, color="#1f77b4")
    ax.axhline(1, color="gray", ls=":", lw=1.2)
    ax.axhline(N, color="gray", ls=":", lw=1.2)
    ax.set_xlabel("局域长度 ℓ")
    ax.set_ylabel("$n_{eff}=1/\\sum p_i^2$")
    ax.set_title("B  参与比随均匀度增（界 [1,64]）")
    ax.grid(alpha=0.3, which="both")

    ax = axes[1, 0]
    ax.semilogx(ne_list, w1_list, "o-", lw=2.2, ms=4, color="#d62728")
    ax.set_xlabel("$n_{eff}$")
    ax.set_ylabel("$w_1=1/H_{round(n_{eff})}$")
    ax.set_xticks([2, 5, 10, 20, 50])
    ax.set_xticklabels(["2", "5", "10", "20", "50"])
    ax.set_title("C  材料越均匀，第一档权重越小（预注册方向）")
    ax.grid(alpha=0.3, which="both")

    ax = axes[1, 1]
    labels = ["临-21 参与比", "识别假设\nK=round(n_eff)", "w1=1/H_K", "第一档权重读数"]
    vals = [1, 1, 1, 0]
    colors = ["#2ca02c", "#9467bd", "#2ca02c", "#d62728"]
    ax.bar(range(4), vals, color=colors, alpha=0.85)
    ax.set_xticks(range(4))
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("是否链内")
    ax.set_ylim(0, 1.3)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["否", "是"])
    ax.set_title("D  识别是假设：不闭合临-5/临-21")
    ax.grid(alpha=0.3, axis="y")

    fig.tight_layout()
    png = os.path.join(OUT, "R36_参与比作截断.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "原文四处 %s" % checks, "通过"],
        ["P2", "n_eff in [1,N]；均匀给 64", "通过"],
        ["P3", "K=round(n_eff)；w1 随 n_eff 减", "通过"],
        ["P4", "识别为假设，不闭合缺口", "状态不动"],
        ["P5", "界与单调（Lean）", "由 Lean 承载"],
        ["结论", "候选一致但未闭合", "状态不动"],
    ]
    with open(os.path.join(OUT, "R36_参与比作截断_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
