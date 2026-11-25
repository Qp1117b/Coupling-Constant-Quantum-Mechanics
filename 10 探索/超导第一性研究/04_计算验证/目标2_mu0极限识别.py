# -*- coding: utf-8 -*-
"""
R24: (目标.2) 的 μ*=0 极限识别——端到端高估来源的结构核对。
无拟合（是结构识别，不是调参）。仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/目标2_mu0极限识别.py"
"""
import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))


def chain(lam, w):
    return 1.13 * math.exp(-1 / 6) * w * math.exp(-(1 + lam) / lam)


def ad(lam, mu, w):
    return w / 1.2 * math.exp(-1.04 * (1 + lam) / (lam - mu * (1 + 0.62 * lam)))


def assertions():
    out = {}
    # 比值恒等：chain 指数 / AD(mu=0) 指数 = 1/1.04
    for lam in [0.4, 0.6, 1.0, 2.0]:
        ch_exp = (1 + lam) / lam
        ad0_exp = 1.04 * (1 + lam) / lam
        out[f"ratio_lam{lam}"] = ch_exp / ad0_exp
    out["ratio_target"] = 1 / 1.04
    out["ratio_constant"] = all(
        abs(out[f"ratio_lam{l}"] - 1 / 1.04) < 1e-12 for l in [0.4, 0.6, 1.0, 2.0]
    )
    # 端到端高估倍数（chain mu=0 vs AD with mu）
    data = [("Mo2NF2_CDW", 0.40, 0.10, 219, 1.0),
            ("Mo2NF2_strain", 0.53, 0.10, 272, 4.0),
            ("MgB2_iso", 0.61, 0.12, 737, 19.0)]
    for name, lam, mu, w, exp in data:
        out[f"overestimate_{name}"] = chain(lam, w) / ad(lam, mu, w)
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    lams = np.linspace(0.2, 3.0, 200)

    ax = axes[0, 0]
    ax.plot(lams, [(1 + l) / l for l in lams], "b-", lw=2, label=r"链 (目标.2)：$(1+\lambda)/\lambda$")
    ax.plot(lams, [1.04 * (1 + l) / l for l in lams], "r--", lw=2, label=r"AD $\mu^\ast=0$：$1.04(1+\lambda)/\lambda$")
    ax.set_xlabel(r"$\lambda$"); ax.set_ylabel("指数系数")
    ax.set_title("(a) 两指数差 1.04 因子（μ*=0 极限）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ratios = np.array([a[f"ratio_lam{l}"] for l in [0.4, 0.6, 1.0, 2.0]])
    ax.plot([0.4, 0.6, 1.0, 2.0], ratios, "go-", lw=2)
    ax.axhline(1 / 1.04, color="k", ls="--", label=r"$1/1.04=0.9615$")
    ax.set_xlabel(r"$\lambda$"); ax.set_ylabel("比值")
    ax.set_title("(b) 比值恒为 1/1.04（∀λ）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    names = ["Mo2NF2\nCDW", "Mo2NF2\nstrain", "MgB2\niso"]
    over = [a[f"overestimate_{n}"] for n in ["Mo2NF2_CDW", "Mo2NF2_strain", "MgB2_iso"]]
    ax.bar(names, over, color="tab:orange")
    ax.axhline(1, color="k", ls="--", label="无高估")
    ax.set_ylabel("chain/AD 倍数")
    ax.set_title("(c) 端到端高估来源：忽略 μ*")
    ax.legend(fontsize=8); ax.grid(alpha=0.3, axis="y")

    ax = axes[1, 1]
    mus = np.linspace(0, 0.2, 200)
    lam = 0.6
    exps = [1.04 * (1 + lam) / (lam - mu * (1 + 0.62 * lam)) for mu in mus]
    ax.plot(mus, exps, "purple", lw=2)
    ax.axhline(1.04 * (1 + lam) / lam, color="b", ls="--", label=r"$\mu^\ast=0$（链极限）")
    ax.set_xlabel(r"$\mu^\ast$"); ax.set_ylabel("AD 指数系数")
    ax.set_title("(d) μ* 增大指数⇒压低 Tc（偶然层）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    fig.suptitle("R24: (目标.2) 的 μ*=0 极限识别（结构识别，无拟合）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "目标2_mu0极限识别.png")
    fig.savefig(png, dpi=140); plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R24 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "目标2_mu0极限识别_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
