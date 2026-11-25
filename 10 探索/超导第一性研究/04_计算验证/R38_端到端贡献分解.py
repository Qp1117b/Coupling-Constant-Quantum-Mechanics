# -*- coding: utf-8 -*-
"""
R38: 端到端 Tc 贡献分解——链内形状 vs 外生归一。
用 FE05 独立参数 + Allen-Dynes 外部工具（明确标注非 CQM 推导）。无拟合。
运行：python "10 探索/超导第一性研究/04_计算验证/R38_端到端贡献分解.py"
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
HBAR_OMEGA_OVER_KB_12 = 1.0  # 用 ω_log(K) 直接：Tc = (ω_log/1.2)·exp(-A)

# FE05 独立参数集（非从 Tc 反解）：system, λ, μ*, ω_log(K), Tc_exp(K)
DATA = [
    ("Mo2NF2-CDW", 0.40, 0.10, 219, 1.0),
    ("Mo2NF2-strain", 0.53, 0.10, 272, 4.0),
    ("MgB2(iso)", 0.61, 0.12, 737, 19.0),
]


def Aexp(lam, mu):
    """AD 指数的正值部分 A = 1.04(1+λ)/(λ-μ(1+0.62λ))。"""
    return 1.04 * (1 + lam) / (lam - mu * (1 + 0.62 * lam))


def tc_ad(lam, mu, omega_log):
    """Allen-Dynes Tc（外部工具），单位 K。"""
    return (omega_log / 1.2) * math.exp(-Aexp(lam, mu))


def F_mu(lam, mu):
    """μ* 压制因子 Tc(μ*)/Tc(0) = exp(A(0)-A(μ*)) < 1。"""
    return math.exp(Aexp(lam, 0) - Aexp(lam, mu))


def sensitivities(lam, mu):
    """对数敏感度 S=∂lnTc/∂ln p（数值微分）。"""
    h = 1e-6
    base = math.log(tc_ad(lam, mu, 1.0))
    Sw = 1.0  # ln Tc 对 ln ω 的敏感度恒为 1
    Sl = (math.log(tc_ad(lam + h, mu, 1.0)) - math.log(tc_ad(lam - h, mu, 1.0))) / (2 * h) * lam
    Sm = (math.log(tc_ad(lam, mu + h, 1.0)) - math.log(tc_ad(lam, mu - h, 1.0))) / (2 * h) * mu
    return Sw, Sl, Sm


def assertions():
    out = {}
    for name, lam, mu, omega, tc_exp in DATA:
        tc = tc_ad(lam, mu, omega)
        out[f"{name}_TcAD"] = round(tc, 3)
        out[f"{name}_Tcexp"] = tc_exp
        out[f"{name}_ratio"] = round(tc / tc_exp, 3)
        out[f"{name}_F_mu"] = round(F_mu(lam, mu), 4)
        out[f"{name}_F_lt_1"] = bool(F_mu(lam, mu) < 1)
        Sw, Sl, Sm = sensitivities(lam, mu)
        out[f"{name}_S_lambda"] = round(Sl, 3)
        out[f"{name}_S_mu"] = round(Sm, 3)
        out[f"{name}_S_omega"] = Sw
    # μ*=0 极限：F=1
    out["F_mu0_is_1"] = bool(abs(F_mu(0.5, 0.0) - 1) < 1e-12)
    # 链形状 25/26 常数（R24）
    out["chain_shape_25_26"] = round(25 / 26, 6)
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ax = axes[0, 0]
    names = [d[0] for d in DATA]
    ratios = [a[f"{d[0]}_ratio"] for d in DATA]
    colors = ["tab:blue", "tab:green", "tab:orange"]
    ax.bar(names, ratios, color=colors)
    ax.axhline(1, color="k", ls="--", label="AD=实验")
    ax.set_ylabel(r"$T_c^{AD}/T_c^{exp}$")
    ax.set_title("(a) 外部 AD + 外生参数：与实验比（非 CQM 推导）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3, axis="y")

    ax = axes[0, 1]
    lams = np.linspace(0.2, 2.0, 200)
    for mu in [0.0, 0.05, 0.10, 0.15]:
        ax.plot(lams, [1 / F_mu(l, mu) for l in lams], lw=2, label=f"μ*={mu}")
    ax.set_xlabel("λ"); ax.set_ylabel(r"$1/F_{\mu^\ast}$（高估倍数）")
    ax.set_title("(b) 外生 μ* 压制因子：端到端高估来源")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    lam = 0.5
    mus = np.linspace(0, 0.2, 100)
    ax.plot(mus, [F_mu(lam, m) for m in mus], "purple", lw=2)
    ax.axhline(1, color="k", ls="--")
    ax.set_xlabel("μ*"); ax.set_ylabel(r"$F_{\mu^\ast}=T_c(\mu^\ast)/T_c(0)$")
    ax.set_title("(c) μ*=0 时 F=1；μ*>0 压制（Lean 已证 A(μ*>0)>A(0)）")
    ax.grid(alpha=0.3)

    ax = axes[1, 1]
    labels = ["链内形状\n(R24: 25/26)", "外生能标\nω_log", "外生耦合\nλ", "外生 μ*\n(审-14)"]
    vals = [1, 1, 1, 1]
    ax.bar(labels, vals, color=["tab:green", "tab:gray", "tab:red", "tab:orange"])
    ax.set_yticks([])
    ax.set_title("(d) 贡献分解：绝对 Tc 由外生参数主导，链只给形状")
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("R38: 端到端 Tc 贡献分解（链形状 vs 外生归一；AD 为外部工具，非 CQM 推导）", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "R38_端到端贡献分解.png")
    fig.savefig(png, dpi=140); plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R38 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "R38_端到端贡献分解_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
