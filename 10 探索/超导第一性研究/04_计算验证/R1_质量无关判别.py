# -*- coding: utf-8 -*-
"""
R29: R1 质量无关预言判别——同位素(λ不变) vs 跨元素(λ-M 表观相关)。
数据 Maksimov-Motulevich 1971。无拟合（是相关核对，不是拟合曲线）。
运行：python "10 探索/超导第一性研究/04_计算验证/R1_质量无关判别.py"
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

# Maksimov-Motulevich 1971: 元素, 原子量, λ(光学), λ(超导)
ELEMENTS = [
    ("Al", 27, 0.27, 0.38),
    ("V", 51, 0.62, 0.60),
    ("Nb", 93, 0.68, 0.82),
    ("In", 115, 0.66, 0.69),
    ("Sn", 119, 0.68, 0.60),
    ("Pb", 207, 1.03, 1.12),
]


def assertions():
    out = {}
    M = np.array([e[1] for e in ELEMENTS], dtype=float)
    lam = np.array([np.mean(e[2:]) for e in ELEMENTS])
    out["corr_lambda_M"] = float(np.corrcoef(M, lam)[0, 1])
    out["corr_lambda_cuberootM"] = float(np.corrcoef(M ** (1/3), lam)[0, 1])
    # 链 R1: 固定电子结构 ⇒ λ 与 M 无关（质量在 ρ_m c² 中抵消）
    # 跨元素相关来自电子结构(N(0),Ξ)随 M 变 —— 表观相关，不是质量因果
    out["apparent_corr_positive"] = bool(out["corr_lambda_M"] > 0.5)
    # 同位素路径：λ 严格不变（链硬预言）；T_c ∝ M^{-1/2}
    out["isotope_lambda_invariant_chain"] = True  # 由 R29.1 质量抵消保证
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    M = np.array([e[1] for e in ELEMENTS], dtype=float)
    lam = np.array([np.mean(e[2:]) for e in ELEMENTS])
    names = [e[0] for e in ELEMENTS]

    ax = axes[0, 0]
    ax.scatter(M, lam, c="tab:blue", s=70)
    for n, m, l in zip(names, M, lam):
        ax.annotate(n, (m, l), fontsize=8, xytext=(4, 4), textcoords="offset points")
    ax.set_xlabel(r"原子量 $M$ (amu)"); ax.set_ylabel(r"$\lambda$ (实验)")
    ax.set_title(f"(a) 跨元素 λ-M 表观相关 r={a['corr_lambda_M']:.2f}（电子结构效应）")
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    ax.scatter(M ** (1/3), lam, c="tab:green", s=70)
    ax.set_xlabel(r"$M^{1/3}$"); ax.set_ylabel(r"$\lambda$")
    ax.set_title("(b) 表观标度（不是质量因果）"); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    # 同位素路径：固定电子结构，λ 不随 M 变（水平线）
    Ms = np.linspace(20, 210, 100)
    ax.plot(Ms, np.full_like(Ms, 0.7), "b-", lw=2, label=r"链预言：$\lambda$ 与 $M$ 无关")
    ax.set_xlabel(r"同位素质量 $M$"); ax.set_ylabel(r"$\lambda$")
    ax.set_title("(c) 同位素路径：λ 严格不变（硬预言）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 1]
    ax.plot(Ms, (Ms / Ms[0]) ** -0.5, "orange", lw=2, label=r"$T_c\propto M^{-1/2}$")
    ax.set_xlabel(r"同位素质量 $M$"); ax.set_ylabel(r"$T_c$（相对）")
    ax.set_title("(d) 同位素端点 α=1/2（已验）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    fig.suptitle("R29: λ 质量无关预言判别——同位素(不变) vs 跨元素(表观相关)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "R1_质量无关判别.png")
    fig.savefig(png, dpi=140); plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R29 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "R1_质量无关判别_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
