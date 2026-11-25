# -*- coding: utf-8 -*-
"""
R37：二维参与比的 O(1) 系数依赖衰减轮廓
=====================================================================
预注册 R37 的 P1–P5（跑数前写死）：
  P1 原文审计 临-21 三候选/无一般序/pi 读数
  P2 IPR 标准与二维积分（B 类）
  P3 三类轮廓的 C=n_eff/(xi/a)^2 排序 pi<4pi<8pi
  P4 系数不定 => xi 单独不能定 n_eff
  P5 Lean 一般权重恒等式

复跑：python "10 探索/超导第一性研究/04_计算验证/R37_参与比系数轮廓依赖.py"
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


def n_eff(w):
    return float(np.sum(w) ** 2 / np.sum(w ** 2))


def main():
    # ---------- P1 ----------
    chain = open(os.path.join(ROOT, "10 探索", "CQM_探索_推导链.md"), encoding="utf-8").read()
    checks = {
        "三候选未定": "取相干长度、能窗宽度、还是费米面壳层" in chain,
        "无一般序": "无一般序" in chain,
        "pi读数": "$\\pi(\\xi/a)^2$" in chain or "pi(\\xi/a)^2" in chain,
        "权重外生": "权重选择与材料归一外生" in chain,
    }
    assert all(checks.values()), "P1: 原文审计失败 %s" % checks

    # ---------- P3：三类轮廓 ----------
    L = 501
    a = 1.0
    coord = (np.arange(L) - L // 2) * a
    X, Y = np.meshgrid(coord, coord, indexing="ij")
    R = np.sqrt(X ** 2 + Y ** 2)

    xis = [8.0, 16.0, 32.0, 48.0]
    profiles = {
        "均匀圆盘": lambda r, xi: (r <= xi).astype(float),
        "高斯": lambda r, xi: np.exp(-r ** 2 / (2 * xi ** 2)),
        "指数": lambda r, xi: np.exp(-r / xi),
    }
    theo = {"均匀圆盘": math.pi, "高斯": 4 * math.pi, "指数": 8 * math.pi}

    coeff = {name: [] for name in profiles}
    for xi in xis:
        for name, f in profiles.items():
            w = f(R, xi)
            ne = n_eff(w)
            coeff[name].append(ne / xi ** 2)
    coeff = {k: np.array(v) for k, v in coeff.items()}

    # 大 xi 的相对误差
    rel = {k: abs(v[-1] - theo[k]) / theo[k] for k, v in coeff.items()}
    assert all(r < 0.10 for r in rel.values()), "P3: 系数相对误差 %s" % rel
    assert coeff["均匀圆盘"][-1] < coeff["高斯"][-1] < coeff["指数"][-1], "P3: 系数排序错"

    print("R37 参与比系数轮廓依赖（结构审计，无拟合）：")
    print("  P1 原文：%s" % checks)
    for k in profiles:
        print("  %s：C=%.3f (xi=48)，理论 %.3f，相对误差 %.2f%%"
              % (k, coeff[k][-1], theo[k], 100 * rel[k]))
    print("  系数比 8pi/pi = 8.00：xi 单独不能定 n_eff")
    print("  P4 与链内‘无一般序、权重外生’一致；P5 Lean")

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    ax = axes[0, 0]
    rr = np.linspace(0, 100, 400)
    for name, f in profiles.items():
        ax.plot(rr, f(rr, 32.0), lw=2.2, label=name)
    ax.set_xlabel("$r/a$")
    ax.set_ylabel("$w(r)$（归一化前）")
    ax.set_title("A  三种二维权重轮廓（$\\xi=32a$）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.plot(xis, coeff["均匀圆盘"], "o-", lw=2.2, ms=6, label="均匀盘：$\\pi$")
    ax.plot(xis, coeff["高斯"], "s-", lw=2.2, ms=6, label="高斯：$4\\pi$")
    ax.plot(xis, coeff["指数"], "^-", lw=2.2, ms=6, label="指数：$8\\pi$")
    for k, val in theo.items():
        ax.axhline(val, color="gray", ls=":", lw=1.0)
    ax.set_xlabel("$\\xi/a$")
    ax.set_ylabel("$C=n_{eff}/(\\xi/a)^2$")
    ax.set_title("B  $O(1)$ 系数依赖轮廓（$\\pi$ / $4\\pi$ / $8\\pi$）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    bars = ax.bar(range(3), [coeff[k][-1] for k in ["均匀圆盘", "高斯", "指数"]],
                  color=["#2ca02c", "#1f77b4", "#d62728"], alpha=0.85)
    ax.set_xticks(range(3))
    ax.set_xticklabels(["均匀盘", "高斯", "指数"])
    ax.set_ylabel("$C$（$\\xi=48a$）")
    ax.set_title("C  系数相差 8 倍：$C$ 不是普适常数")
    ax.grid(alpha=0.3, axis="y")

    ax = axes[1, 1]
    ax.text(0.05, 0.75, "链内 `临-21`：", fontsize=12, weight="bold")
    ax.text(0.05, 0.60, "· 三候选无一般序\n· $\\pi(\\xi/a)^2$ 仅等权 cutoff 读数\n· 权重选择外生", fontsize=10)
    ax.text(0.05, 0.32, "本轮定量坐实：", fontsize=12, weight="bold", color="#d62728")
    ax.text(0.05, 0.17, "$C\\in[\\pi,8\\pi]$ 依赖轮廓\n$\\xi$ 单独不能定 $n_{eff}$\n`临-21`/`临-5` 状态不动", fontsize=10, color="#d62728")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("D  结论：无一般序被定量化")

    fig.tight_layout()
    png = os.path.join(OUT, "R37_参与比系数轮廓依赖.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "原文四处 %s" % checks, "通过"],
        ["P2", "IPR 与二维积分（B 类）", "外部标准"],
        ["P3", "C=%.2f/%.2f/%.2f" % tuple(coeff[k][-1] for k in ["均匀圆盘","高斯","指数"]), "通过"],
        ["P4", "系数相差 8 倍", "xi 不能单独定 n_eff"],
        ["P5", "一般权重恒等式（Lean）", "由 Lean 承载"],
        ["结论", "无一般序被定量化", "状态不动"],
    ]
    with open(os.path.join(OUT, "R37_参与比系数轮廓依赖_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
