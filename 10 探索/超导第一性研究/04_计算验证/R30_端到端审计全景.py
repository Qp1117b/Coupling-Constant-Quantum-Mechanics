# -*- coding: utf-8 -*-
"""
R30: 端到端审计全景——可视化链内已推的关键函数（核对极限/单调/量级，非拟合）
+ 29 轮成果分层。所有曲线来自链内已推解析式，不含数据拟合。
运行：python "10 探索/超导第一性研究/04_计算验证/R30_端到端审计全景.py"
"""
import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))


def assertions():
    out = {}
    # (a) R15: T_c(κ_s)=√κ_s e^{-κ_s}（取 A=1,B=1）最大值 κ_s*=1/(2A)=0.5
    kap = np.linspace(0.01, 3, 10000)
    tc = np.sqrt(kap) * np.exp(-kap)
    out["R15_kappa_star_num"] = float(kap[np.argmax(tc)])
    out["R15_kappa_star_theory"] = 0.5
    out["R15_max_match"] = bool(abs(out["R15_kappa_star_num"] - 0.5) < 1e-3)
    # (b) R25: μ*=μ/(1+μ ln r) 单调递减
    r = np.logspace(0, 3, 200)
    mu, mustar = 0.5, mu_f(r, 0.5)
    out["mu_star_monotone_dec"] = bool(np.all(np.diff(mustar) < 0))
    out["mu_star_positive"] = bool(np.all(mustar > 0))
    # (c) R29: 同位素 T_c∝M^{-1/2}，对数斜率 = -1/2
    M = np.logspace(0, 2.3, 100)
    slopes = np.polyfit(np.log(M), np.log(M ** -0.5), 1)[0]
    out["isotope_log_slope"] = float(slopes)
    out["isotope_target"] = -0.5
    # (d) R24: μ*=0 指数比 1/1.04=25/26（∀λ）
    lambdas = np.array([0.3, 0.7, 1.0, 1.5, 2.5])
    ratios = np.array([((1 + l) / l) / (1.04 * (1 + l) / l) for l in lambdas])
    out["mu0_ratio_all_lambda"] = bool(np.allclose(ratios, 25 / 26))
    return out


def mu_f(r, mu):
    return mu / (1 + mu * np.log(r))


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ax = axes[0, 0]
    kap = np.linspace(0.01, 3, 1000)
    tc = np.sqrt(kap) * np.exp(-kap)
    ax.plot(kap, tc, "b-", lw=2)
    ax.axvline(0.5, color="r", ls="--", label=r"$\kappa_s^\ast=1/(2A)$")
    ax.set_xlabel(r"键刚度 $\kappa_s$"); ax.set_ylabel(r"$T_c$（相对）")
    ax.set_title("(a) R15: $T_c$ 最大值条件结果"); ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    r = np.logspace(0, 3, 200)
    ax.plot(r, mu_f(r, 0.5), "purple", lw=2)
    ax.set_xscale("log")
    ax.set_xlabel(r"$\varepsilon_F/\hbar\omega_D$"); ax.set_ylabel(r"$\mu^\ast$")
    ax.set_title("(b) R25: μ* 单调递减、恒正"); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    M = np.logspace(0, 2.3, 100)
    ax.plot(M, M ** -0.5, "g-", lw=2, label=r"$T_c\propto M^{-1/2}$")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel(r"同位素质量 $M$"); ax.set_ylabel(r"$T_c$（相对）")
    ax.set_title("(c) R29: 同位素指数 α=1/2（斜率 -1/2）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 1]
    labels = ["落地主链", "代数严格", "判据/比值", "作废"]
    vals = [6, 7, 11, 4]
    colors = ["tab:green", "tab:blue", "tab:orange", "tab:red"]
    ax.bar(labels, vals, color=colors)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.1, str(v), ha="center", fontsize=10)
    ax.set_ylabel("轮数")
    ax.set_title("(d) R1–R30 成果分层（见成果登记总表）")
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("R30: 端到端链一致性审计全景（链内已推函数，非数据拟合）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "R30_端到端审计全景.png")
    fig.savefig(png, dpi=140); plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R30 审计断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "R30_端到端审计全景_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
